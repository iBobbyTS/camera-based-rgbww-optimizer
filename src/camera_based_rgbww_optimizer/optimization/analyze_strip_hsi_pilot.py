from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    FROZEN_STATUS,
    HsiPolicyV2,
    conservative_class_variance,
    evaluate_confirmation_spread,
    evaluate_reference_difference,
    summarize_within_block,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    P7_RESULT_STATUSES,
    hsi_objective_sort_key,
    evaluate_hsi_observation_v2,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
    recompute_physical_count,
    validate_attempt_event_grammar,
)


TARGET_SET_COUNTS = {"sentinel": 4, "remaining": 9}
SENTINEL_TARGETS = {(0, 0), (120, 100), (120, 50), (300, 100)}
REMAINING_TARGETS = {(0, 50), (0, 100), (60, 50), (60, 100), (180, 50), (180, 100), (240, 50), (240, 100), (300, 50)}
PRIMARY_HUES = (0, 60, 120, 180, 240, 300)


def analyze_strip_hsi_pilot(
    run_dir: str | Path, *, policy_version: str,
) -> dict[str, Any]:
    if policy_version == "v1":
        return _analyze_strip_hsi_pilot_v1(run_dir)
    if policy_version == "v2":
        return _analyze_strip_hsi_pilot_v2(run_dir)
    raise ValueError("P7 analyzer requires explicit policy_version v1 or v2")


def _analyze_strip_hsi_pilot_v1(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    run = _load_json(root / "run.json")
    plan = _load_json(root / "plan.json")
    plan_policy = plan.get("measurement", {}).get("policy_version", "v1_legacy_capture_only")
    if plan_policy != "v1_legacy_capture_only":
        raise ValueError("legacy P7 analyzer accepts only policy v1 runs")
    if run.get("phase") != "P7-pilot" or run.get("status") != "complete":
        raise ValueError("P7 pilot analysis requires a completed P7-pilot run")
    target_set = str(run.get("target_set"))
    expected_count = int(plan.get("measurement", {}).get("target_count", -1))
    if target_set not in {"sentinel", "remaining", "boundary", "holdout"} or expected_count <= 0 or int(run.get("completed_target_count", -1)) != expected_count:
        raise ValueError("P7 pilot analysis requires a complete sentinel or remaining target set")
    if (root / "failure.json").exists():
        raise ValueError("P7 pilot run contains failure.json")
    python_cleanup = _load_json_value(root / "all-off-python.json")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if not _cleanup_ok(python_cleanup) or not _cleanup_ok(shell_cleanup):
        raise ValueError("P7 pilot requires successful Python and shell cleanup")
    if list(root.rglob("*.npy")):
        raise ValueError("P7 pilot must not retain .npy files")

    captures = _load_jsonl(root / "captures.jsonl")
    capture_validation = _validate_captures(captures)
    commands = _load_jsonl(root / "commands.jsonl")
    command_validation = _validate_commands(captures, commands)
    input_validation = _validate_input_hashes(plan)
    anchor_validation = _validate_anchors(root, plan)
    rows = _load_jsonl(root / "target-results.jsonl")
    if len(rows) != expected_count:
        raise ValueError(f"P7 target-results must contain {expected_count} rows, found {len(rows)}")
    by_target = {}
    for row in rows:
        target = row["target"]
        key = (int(target["hue"]), int(target["sat"]))
        if key in by_target:
            raise ValueError(f"duplicate P7 target row: {key}")
        by_target[key] = row
    expected = {(int(item["hue"]), int(item["sat"])) for item in plan["targets"]}
    if target_set == "sentinel" and expected != SENTINEL_TARGETS:
        raise ValueError("P7 sentinel target set drift")
    if target_set == "remaining" and expected != REMAINING_TARGETS:
        raise ValueError("P7 remaining target set drift")
    if set(by_target) != expected:
        raise ValueError("P7 target grid is incomplete or contains unexpected points")
    target_evidence_validation = _validate_target_evidence(rows, plan)

    points = [_point_summary(by_target[key]) for key in sorted(by_target)]
    unavailable = [point for point in points if point["status"] == "measurement_unreachable"]
    faithful = [point for point in points if point["gamut_status"] == "faithful"]
    unresolved = [point for point in points if point["gamut_status"] == "uncertainty_unresolved"]
    solver_exhausted = [point for point in points if point["gamut_status"] == "solver_budget_exhausted"]
    sentinel_auto_pass = target_set == "sentinel" and _faithful(by_target[(0, 0)]) and _faithful(by_target[(120, 50)]) and (
        _faithful(by_target[(120, 100)]) or _faithful(by_target[(300, 100)])
    ) and not unavailable and not unresolved and not solver_exhausted
    return {
        "schema_version": 1,
        "analysis": "strip_hsi_pilot_staged_analysis",
        "status": "ready_for_sentinel_branch" if target_set == "sentinel" else (
            "ready_for_combined_analysis" if target_set == "remaining" else f"ready_for_{target_set}_review"
        ),
        "target_set": target_set,
        "run_dir": str(root),
        "run_json_sha256": _sha256(root / "run.json"),
        "capture_validation": capture_validation,
        "command_validation": command_validation,
        "input_validation": input_validation,
        "anchor_validation": anchor_validation,
        "target_evidence_validation": target_evidence_validation,
        "cleanup": {"python": python_cleanup, "shell": shell_cleanup},
        "point_count": len(points),
        "faithful_point_count": len(faithful),
        "measurement_unreachable_point_count": len(unavailable),
        "points": points,
        "decision_hints": {
            "automatic_gate6_selection": False,
            "sentinel_automatic_conditions_numerically_satisfied": sentinel_auto_pass,
            "next_action": "audit_sentinel_then_run_remaining" if sentinel_auto_pass else "planner_branch_review",
        },
        "notes": [
            "Unconfirmed is not equivalent to physically unreachable; it only means the settled pilot gate was not proven.",
            "Any full-scale boundary must use s_exact_max_int100_fullscale and retain scale-relaxed diagnostics.",
            "This analyzer does not freeze Gate-6 or install a runtime LUT.",
        ],
    }


def analyze_combined_strip_hsi_pilot(
    sentinel_run_dir: str | Path,
    remaining_run_dir: str | Path,
    *,
    policy_version: str,
) -> dict[str, Any]:
    sentinel_root = Path(sentinel_run_dir)
    remaining_root = Path(remaining_run_dir)
    sentinel = analyze_strip_hsi_pilot(sentinel_root, policy_version=policy_version)
    remaining = analyze_strip_hsi_pilot(remaining_root, policy_version=policy_version)
    if sentinel.get("target_set") != "sentinel" or remaining.get("target_set") != "remaining":
        raise ValueError("combined P7 analysis requires sentinel then remaining runs")
    sentinel_plan = _load_json(sentinel_root / "plan.json")
    remaining_plan = _load_json(remaining_root / "plan.json")
    policy_key = "policy_v2_artifact" if policy_version == "v2" else "uncertainty_artifact"
    if sentinel_plan.get("measurement", {}).get("policy_version") != remaining_plan.get("measurement", {}).get("policy_version"):
        raise ValueError("combined P7 runs disagree on policy version")
    shared_inputs = (
        policy_key, "ray_hsi_manifold", "location_config",
        "raw_observer_config", "basis_analysis", "pilot_config", "code_duty_curve",
    )
    for name in shared_inputs:
        if sentinel_plan["inputs"][name]["sha256"] != remaining_plan["inputs"][name]["sha256"]:
            raise ValueError(f"combined P7 runs disagree on frozen input {name}")
    points = [*sentinel["points"], *remaining["points"]]
    keys = [(int(item["hue"]), int(item["sat"])) for item in points]
    expected = SENTINEL_TARGETS | REMAINING_TARGETS
    if len(keys) != 13 or len(set(keys)) != 13 or set(keys) != expected:
        raise ValueError("combined P7 analysis must contain exactly the frozen 13 unique targets")
    invalid_statuses = {"reference_drift", "uncertainty_unresolved"}
    blocking = [
        item for item in points
        if item.get("result_status", item.get("gamut_status")) in invalid_statuses
    ]
    valid_rows = [item for item in points if item.get("status") != "measurement_unreachable"]
    per_hue_valid = {
        hue: any(int(item["hue"]) == hue and int(item["sat"]) > 0 for item in valid_rows)
        for hue in PRIMARY_HUES
    }
    return {
        "schema_version": 2 if policy_version == "v2" else 1,
        "analysis": "p7_int100_fullscale_combined_13",
        "status": "ready_for_boundary_stage" if not blocking and all(per_hue_valid.values()) else "blocked_for_planner_review",
        "sentinel_run": {"path": str(sentinel_root), "run_json_sha256": _sha256(sentinel_root / "run.json")},
        "remaining_run": {"path": str(remaining_root), "run_json_sha256": _sha256(remaining_root / "run.json")},
        "shared_input_hashes": {name: sentinel_plan["inputs"][name]["sha256"] for name in shared_inputs},
        "policy_version": policy_version,
        "policy_artifact_sha256": sentinel_plan["inputs"][policy_key]["sha256"],
        "point_count": len(points),
        "points": sorted(points, key=lambda item: (int(item["hue"]), int(item["sat"]))),
        "blocking_statuses": blocking,
        "per_primary_hue_has_valid_nonzero_measurement": per_hue_valid,
        "boundary_name": "s_exact_max_int100_fullscale",
        "physical_gamut_inference": "prohibited",
        "automatic_gate6_selection": False,
    }


def _analyze_strip_hsi_pilot_v2(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    run = _load_json(root / "run.json")
    plan = _load_json(root / "plan.json")
    if plan.get("measurement", {}).get("policy_version") != "v2":
        raise ValueError("v2 P7 analyzer accepts only explicit policy_version=v2 runs")
    if run.get("phase") != "P7-pilot" or run.get("status") != "complete":
        raise ValueError("v2 P7 analysis requires a completed P7-pilot run")
    if (root / "failure.json").exists():
        raise ValueError("v2 P7 run contains failure.json")
    if list(root.rglob("*.npy")):
        raise ValueError("v2 P7 run must retain zero .npy files")
    python_cleanup = _load_json_value(root / "all-off-python.json")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if not _cleanup_ok(python_cleanup) or not _cleanup_ok(shell_cleanup):
        raise ValueError("v2 P7 requires successful Python and shell cleanup")

    input_validation = _validate_input_hashes(plan)
    policy_ref = plan.get("inputs", {}).get("policy_v2_artifact")
    if not isinstance(policy_ref, Mapping):
        raise ValueError("v2 P7 plan lacks policy_v2_artifact")
    policy = HsiPolicyV2.load(policy_ref["path"])
    if policy.artifact_sha256 != policy_ref.get("sha256"):
        raise ValueError("v2 P7 policy hash differs from the frozen plan")
    if policy.artifact.get("status") != FROZEN_STATUS or not policy.formal_capture_eligible:
        raise ValueError("v2 P7 analyzer requires a frozen formal-eligible policy")

    captures = _load_jsonl(root / "captures.jsonl")
    capture_validation = _validate_captures(captures)
    commands = _load_jsonl(root / "commands.jsonl")
    curve = _load_json(Path(plan["inputs"]["code_duty_curve"]["path"]))
    command_validation = _validate_v2_commands(captures, commands, plan=plan, curve=curve)
    anchor_validation = _validate_v2_reference_blocks(
        root, plan, captures=captures, commands=commands, curve=curve,
        policy=policy,
    )
    rows = _load_jsonl(root / "target-results.jsonl")
    expected_count = int(plan.get("measurement", {}).get("target_count", -1))
    if len(rows) != expected_count or int(run.get("completed_target_count", -1)) != expected_count:
        raise ValueError("v2 P7 target-results count is incomplete")
    expected_targets = {(int(item["hue"]), int(item["sat"])) for item in plan["targets"]}
    by_target: dict[tuple[int, int], Mapping[str, Any]] = {}
    for row in rows:
        key = (int(row["target"]["hue"]), int(row["target"]["sat"]))
        if key in by_target:
            raise ValueError(f"duplicate v2 P7 target row: {key}")
        by_target[key] = row
    if set(by_target) != expected_targets:
        raise ValueError("v2 P7 target grid is incomplete or unexpected")
    target_set = str(run.get("target_set"))
    if target_set == "sentinel" and expected_targets != SENTINEL_TARGETS:
        raise ValueError("v2 P7 sentinel target set drift")
    if target_set == "remaining" and expected_targets != REMAINING_TARGETS:
        raise ValueError("v2 P7 remaining target set drift")
    target_audit, points = _validate_v2_target_evidence(
        rows, plan, captures=captures, commands=commands,
        curve=curve, policy=policy, manifold=RayHsiManifold.load(
            plan["inputs"]["ray_hsi_manifold"]["path"],
        ),
    )
    blocking = [
        point for point in points
        if point["result_status"] in {"reference_drift", "uncertainty_unresolved", "solver_budget_exhausted", "measurement_unreachable"}
    ]
    return {
        "schema_version": 2,
        "analysis": "strip_hsi_pilot_v2_formal_analysis",
        "policy_version": "v2",
        "policy_provenance": {
            "path": str(policy_ref["path"]),
            "sha256": policy.artifact_sha256,
            "status": policy.artifact["status"],
            "formal_capture_eligible": True,
        },
        "status": "ready_for_sentinel_branch" if target_set == "sentinel" and not blocking else (
            "ready_for_combined_analysis" if target_set == "remaining" and not blocking else "blocked_for_planner_review"
        ),
        "target_set": target_set,
        "run_dir": str(root),
        "run_json_sha256": _sha256(root / "run.json"),
        "capture_validation": capture_validation,
        "command_validation": command_validation,
        "input_validation": input_validation,
        "anchor_validation": anchor_validation,
        "target_evidence_validation": target_audit,
        "cleanup": {"python": python_cleanup, "shell": shell_cleanup},
        "point_count": len(points),
        "points": points,
        "blocking_points": blocking,
        "automatic_gate6_selection": False,
    }


def _validate_v2_reference_blocks(
    root: Path, plan: Mapping[str, Any], *, captures: Sequence[Mapping[str, Any]],
    commands: Sequence[Mapping[str, Any]], curve: Mapping[str, Any],
    policy: HsiPolicyV2,
) -> dict[str, Any]:
    anchors = _load_jsonl(root / "reference-anchors.jsonl")
    if len(anchors) != 12:
        raise ValueError("v2 P7 requires exactly 12 reference anchor captures")
    expected = [
        (position, int(item["hue"]), int(item["sat"]), int(item["repeat_index"]))
        for position in ("pre", "post")
        for item in plan["reference_anchors"][position]
    ]
    actual = [
        (str(item["position"]), int(item["target"]["hue"]), int(item["target"]["sat"]), int(item["repeat_index"]))
        for item in anchors
    ]
    if actual != expected:
        raise ValueError("v2 P7 reference anchors are incomplete, reordered, or unexpected")
    captures_by_id = {str(item["capture_id"]): item for item in captures}
    commands_by_id = _group_commands(commands)
    expected_by_position = {
        position: {(int(item["hue"]), int(item["sat"]), int(item["repeat_index"])) for item in plan["reference_anchors"][position]}
        for position in ("pre", "post")
    }
    for anchor in anchors:
        capture_id = str(anchor["capture_id"])
        capture = captures_by_id.get(capture_id)
        key = (int(anchor["target"]["hue"]), int(anchor["target"]["sat"]), int(anchor["repeat_index"]))
        if capture is None or capture.get("source") != "ray" or capture.get("target_index") is not None or key not in expected_by_position[str(anchor["position"])]:
            raise ValueError("v2 P7 reference anchor capture provenance mismatch")
        step = {"state": {**anchor["target"], "intensity_percent": plan["reference_anchors"]["intensity_percent"]}}
        on = validate_attempt_event_grammar(
            commands_by_id.get(capture_id, []), source="ray", plan_step=step,
            curve=curve,
        )
        if anchor.get("readback") != on.get("readback"):
            raise ValueError("v2 P7 reference anchor readback differs from command evidence")
        report = _load_json(Path(capture["capture"]["patch_statistics"]))
        recomputed_features = required_hsi_features_from_report(
            report, policy.artifact["feature_set"]["ids"],
        )
        if anchor.get("feature_values") != recomputed_features:
            raise ValueError("v2 P7 reference anchor feature provenance mismatch")
    pre = _load_json(root / "reference-pre-analysis.json")
    post = _load_json(root / "reference-post-analysis.json")
    recomputed: dict[str, dict[str, Any]] = {}
    states = policy.artifact["reference_policy"].get("states") or {}
    feature_ids = policy.artifact["feature_set"]["ids"]
    for position in ("pre", "post"):
        by_state: dict[tuple[int, int], list[Mapping[str, float]]] = {}
        for anchor in anchors:
            if anchor["position"] == position:
                state = (int(anchor["target"]["hue"]), int(anchor["target"]["sat"]))
                by_state.setdefault(state, []).append(anchor["feature_values"])
        results = []
        for (hue, sat), samples in sorted(by_state.items()):
            state_key = f"h{hue}-s{sat}"
            frozen = states.get(state_key)
            if not isinstance(frozen, Mapping) or len(samples) != 3:
                raise ValueError("v2 P7 reference state lacks frozen or three-frame evidence")
            block = summarize_within_block(samples, feature_ids)
            region = frozen["center_compatibility_region"]
            evaluation = evaluate_reference_difference(
                frozen["frozen_center"], block["center"],
                left_variance=frozen["frozen_diagonal_variance"], left_count=int(frozen["frozen_count"]),
                right_variance=block["diagonal_variance"], right_count=int(block["count"]),
                feature_ids=feature_ids, guarded_limit=float(region["guarded_limit"]),
                unguarded_limit=float(region["unguarded_limit"]), statistic="reference_center_compatibility",
            )
            if evaluation["decision"] != "pass":
                raise ValueError("v2 P7 reference center compatibility did not pass from raw anchors")
            results.append({"state": state_key, "block": block, "evaluation": evaluation})
        output: dict[str, Any] = {"position": position, "states": results, "status": "pass"}
        if position == "post":
            pre_by_state = {item["state"]: item["block"] for item in recomputed["pre"]["states"]}
            stability = []
            for item in results:
                frozen = states[item["state"]]
                region = frozen["repeatability_region"]
                previous = pre_by_state.get(item["state"])
                if previous is None:
                    raise ValueError("v2 P7 post reference lacks matching pre block")
                evaluation = evaluate_reference_difference(
                    previous["center"], item["block"]["center"],
                    left_variance=previous["diagonal_variance"], left_count=int(previous["count"]),
                    right_variance=item["block"]["diagonal_variance"], right_count=int(item["block"]["count"]),
                    feature_ids=feature_ids, guarded_limit=float(region["guarded_limit"]),
                    unguarded_limit=float(region["unguarded_limit"]), statistic="reference_repeatability",
                )
                if evaluation["decision"] != "pass":
                    raise ValueError("v2 P7 pre/post stability did not pass from raw anchors")
                stability.append({"state": item["state"], "evaluation": evaluation})
            output["pre_post_stability"] = stability
        recomputed[position] = output
    if pre != recomputed["pre"] or post != recomputed["post"]:
        raise ValueError("v2 P7 reference analysis differs from raw-anchor recomputation")
    if len(pre.get("states", [])) != 3 or len(post.get("states", [])) != 1:
        raise ValueError("v2 P7 reference block state count drift")
    if len(post.get("pre_post_stability", [])) != 1:
        raise ValueError("v2 P7 pre/post stability evidence is incomplete")
    for item in [*pre["states"], *post["states"]]:
        if int(item.get("block", {}).get("count", -1)) != 3:
            raise ValueError("v2 P7 reference state must contain a three-capture repeat block")
        if item.get("evaluation", {}).get("decision") != "pass":
            raise ValueError("v2 P7 reference center compatibility did not pass")
    if post["pre_post_stability"][0].get("evaluation", {}).get("decision") != "pass":
        raise ValueError("v2 P7 reference pre/post stability did not pass")
    return {
        "anchor_count": 12,
        "pre_capture_count": 9,
        "post_capture_count": 3,
        "pre_state_count": 3,
        "post_state_count": 1,
        "center_compatibility": "pass",
        "pre_post_stability": "pass",
    }


def _validate_v2_target_evidence(
    rows: Sequence[Mapping[str, Any]], plan: Mapping[str, Any],
    *, captures: Sequence[Mapping[str, Any]], commands: Sequence[Mapping[str, Any]],
    curve: Mapping[str, Any], policy: HsiPolicyV2, manifold: RayHsiManifold,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if [row.get("target") for row in rows] != list(plan["targets"]):
        raise ValueError("v2 P7 target-results must exactly follow the frozen target plan")
    target_plan = {(int(item["hue"]), int(item["sat"])): item for item in plan["targets"]}
    capture_by_id = {str(item.get("capture_id")): item for item in captures}
    if len(capture_by_id) != len(captures):
        raise ValueError("v2 P7 contains duplicate capture ids")
    commands_by_id = _group_commands(commands)
    points: list[dict[str, Any]] = []
    objective_count = 0
    capture_owners: dict[str, str] = {}
    reconstructed_targets: list[dict[str, Any]] = []
    previous_command: Mapping[str, int] | None = None
    feature_ids = tuple(policy.artifact["feature_set"]["ids"])
    start_capture_ids: dict[tuple[int, int], set[str]] = {}
    for target_position, row in enumerate(rows):
        key = (int(row["target"]["hue"]), int(row["target"]["sat"]))
        declared = target_plan[key]
        reported_status = str(row.get("result_status"))
        if reported_status not in P7_RESULT_STATUSES or row.get("gamut_status") != reported_status:
            raise ValueError(f"v2 P7 target {key} has overlapping or unsupported result status")
        feedback = row.get("feedback")
        if not isinstance(feedback, Mapping) or feedback.get("kind") != "hsi_bounded_multiseed_feedback_v2":
            raise ValueError(f"v2 P7 target {key} lacks multiseed evidence")
        if feedback.get("budget_declaration") != declared.get("solver_budget"):
            raise ValueError(f"v2 P7 target {key} solver budget declaration drift")
        attempts = feedback.get("attempts")
        if not isinstance(attempts, list) or not 1 <= len(attempts) <= 2:
            raise ValueError(f"v2 P7 target {key} has invalid multiseed attempt count")
        start_indices = [int(item.get("start_index", -1)) for item in attempts]
        if start_indices != list(range(len(attempts))):
            raise ValueError(f"v2 P7 target {key} start indices are incomplete or reordered")
        expected_confirmation_count = int(declared["confirmation_count"])
        repeatability_class = _v2_repeatability_class(
            target_sat=float(declared["sat"]), max_code=int(declared["max_code"]),
            formal_max_code=4095,
        )
        recomputed_logical = 0
        derived_confirmed_attempts: list[Mapping[str, Any]] = []
        for attempt in attempts:
            start_index = int(attempt.get("start_index", -1))
            if start_index < 0:
                raise ValueError(f"v2 P7 target {key} has invalid start index")
            start_capture_ids.setdefault((target_position, start_index), set())
            result = attempt.get("result")
            if not isinstance(result, Mapping):
                raise ValueError(f"v2 P7 target {key} has malformed start result")
            samples = result.get("samples")
            rejections = result.get("measurement_rejections", [])
            budget = result.get("budget", {})
            if not isinstance(samples, list) or not isinstance(rejections, list):
                raise ValueError(f"v2 P7 target {key} has malformed logical evidence")
            logical = len(samples) + len(rejections)
            consumed = budget.get("consumed")
            reconstructed_consumed = {
                "initial": 0, "initial_probes": 0, "feedback_attempts": 0,
                "rebase_probes": 0, "confirmation_captures": 0,
            }
            phases = [str(item.get("phase")) for item in samples] + [str(item.get("phase")) for item in rejections]
            for phase in phases:
                if phase == "initial":
                    category = "initial"
                elif phase.startswith("probe-"):
                    category = "initial_probes"
                elif "rebase-" in phase:
                    category = "rebase_probes"
                elif phase.startswith("confirm-"):
                    category = "confirmation_captures"
                elif phase.startswith("feedback-"):
                    category = "feedback_attempts"
                else:
                    raise ValueError(f"v2 P7 target {key} has unclassified logical phase {phase}")
                reconstructed_consumed[category] += 1
            if consumed != reconstructed_consumed or sum(reconstructed_consumed.values()) != logical:
                raise ValueError(f"v2 P7 target {key} start logical ledger mismatch")
            if int(budget.get("logical_observations_used", -1)) != logical:
                raise ValueError(f"v2 P7 target {key} start logical count differs from raw evidence")
            if logical > int(declared["solver_budget"]["max_logical_observations_per_start"]):
                raise ValueError(f"v2 P7 target {key} exceeds per-start logical budget")
            groups = result.get("confirmation_attempts")
            if not isinstance(groups, list) or not groups:
                raise ValueError(f"v2 P7 target {key} lacks final-verification group evidence")
            if int(budget.get("confirmation_groups_started", -1)) != len(groups) or len(groups) > int(declared["solver_budget"]["max_confirmation_groups_per_start"]):
                raise ValueError(f"v2 P7 target {key} exceeds confirmation-group budget")
            rebase_ids = {phase.split("-probe-", 1)[0] for phase in phases if "rebase-" in phase}
            if int(budget.get("rebases_started", -1)) != len(rebase_ids):
                raise ValueError(f"v2 P7 target {key} rebase ledger mismatch")
            confirmed_group_count = 0
            for group in groups:
                indices = group.get("sample_indices")
                if not isinstance(indices, list) or len(indices) != len(set(map(int, indices))):
                    raise ValueError(f"v2 P7 target {key} has malformed confirmation indices")
                if group.get("status") in {"confirmed", "failed"} and len(indices) != expected_confirmation_count:
                    raise ValueError(f"v2 P7 target {key} has invalid confirmed group size")
                if group.get("status") not in {"confirmed", "failed", "partial"}:
                    raise ValueError(f"v2 P7 target {key} has unsupported confirmation group status")
                if group.get("status") == "partial" and len(indices) >= expected_confirmation_count:
                    raise ValueError(f"v2 P7 target {key} partial confirmation group is not partial")
                if int(group.get("captured_count", -1)) != len(indices) or int(group.get("expected_capture_count", -1)) != expected_confirmation_count:
                    raise ValueError(f"v2 P7 target {key} confirmation capture ledger mismatch")
                if bool(group.get("partial_group")) != (group.get("status") == "partial"):
                    raise ValueError(f"v2 P7 target {key} confirmation partial flag mismatch")
                if group.get("status") == "partial" and not (rejections or result.get("budget_exhaustion") or budget.get("exhaustion")):
                    raise ValueError(f"v2 P7 target {key} partial confirmation lacks stop evidence")
                candidate = group.get("candidate_command")
                for index in indices:
                    if int(index) < 0 or int(index) >= len(samples) or samples[int(index)].get("command") != candidate:
                        raise ValueError(f"v2 P7 target {key} confirmation command/index mismatch")
                feasible = [bool(samples[int(index)].get("objective", {}).get("feasible")) for index in indices]
                if int(group.get("feasible_capture_count", -1)) != sum(feasible):
                    raise ValueError(f"v2 P7 target {key} confirmation feasible count mismatch")
                if group.get("status") == "confirmed" and (len(indices) != expected_confirmation_count or not all(feasible)):
                    raise ValueError(f"v2 P7 target {key} confirmed group is not fully feasible")
                if group.get("status") == "failed" and all(feasible):
                    raise ValueError(f"v2 P7 target {key} failed group lacks a failed sample")
                derived_group_status = "partial" if len(indices) < expected_confirmation_count else (
                    "confirmed" if all(feasible) else "failed"
                )
                if group.get("status") != derived_group_status:
                    raise ValueError(f"v2 P7 target {key} confirmation status differs from replayed samples")
                confirmed_group_count += derived_group_status == "confirmed"
            for sample in samples:
                observation = sample.get("observation")
                capture_id = str(observation.get("capture_id")) if isinstance(observation, Mapping) else ""
                capture = capture_by_id.get(capture_id)
                phase = str(sample.get("phase"))
                if not capture_id or capture is None:
                    raise ValueError(f"v2 P7 target {key} sample capture id is missing, duplicate, or unknown")
                if int(capture.get("target_index", -1)) != int(declared["index"]) or capture.get("source") != "strip" or not str(capture.get("purpose", "")).endswith(phase):
                    raise ValueError(f"v2 P7 target {key} sample capture provenance mismatch")
                _claim_capture(capture_owners, capture_id, f"target-{target_position}:start-{start_index}:sample")
                start_capture_ids[(target_position, start_index)].add(capture_id)
                event_rows = [item for item in commands_by_id.get(capture_id, []) if item.get("event") != "weak_signal_reacquire"]
                on = validate_attempt_event_grammar(
                    event_rows, source="strip", plan_step={"command": sample.get("command")},
                    curve=curve,
                )
                if on.get("requested_command") != sample.get("command"):
                    raise ValueError(f"v2 P7 target {key} sample requested command mismatch")
                report = _load_json(Path(capture["capture"]["patch_statistics"]))
                replayed_features = required_hsi_features_from_report(report, feature_ids)
                if observation.get("feature_values") != replayed_features:
                    raise ValueError(f"v2 P7 target {key} sample RAW feature provenance mismatch")
                replayed = evaluate_hsi_observation_v2(
                    manifold, replayed_features,
                    target_hue=float(declared["hue"]), target_sat=float(declared["sat"]),
                    repeatability_class=repeatability_class, policy=policy,
                    command=sample.get("command"), previous_command=previous_command,
                    max_code=int(declared["max_code"]),
                )
                if not _json_numerically_equal(sample.get("residuals"), replayed["residuals"]) or not _json_numerically_equal(sample.get("objective"), replayed["objective"]):
                    raise ValueError(f"v2 P7 target {key} sample objective differs from RAW replay")
            for rejection in rejections:
                if not isinstance(rejection, Mapping):
                    raise ValueError(f"v2 P7 target {key} has malformed measurement rejection")
                phase = str(rejection.get("phase", ""))
                command = rejection.get("command")
                evidence = rejection.get("evidence")
                if not isinstance(command, Mapping) or set(command) != {"cw", "ww", "r", "g", "b"}:
                    raise ValueError(f"v2 P7 target {key} rejection lacks frozen command evidence")
                _validate_measurement_rejection_evidence(
                    evidence, phase=phase, command=command,
                    target_index=int(declared["index"]), target_key=key,
                )
                capture_ids = [str(value) for value in evidence["capture_ids"]]
                for capture_id in capture_ids:
                    capture = capture_by_id.get(capture_id)
                    if capture is None or int(capture.get("target_index", -1)) != int(declared["index"]):
                        raise ValueError(f"v2 P7 target {key} rejection capture provenance mismatch")
                    if not str(capture.get("purpose", "")).endswith(phase):
                        raise ValueError(f"v2 P7 target {key} rejection phase/capture mismatch")
                    _claim_capture(capture_owners, capture_id, f"target-{target_position}:start-{start_index}:rejection")
                    start_capture_ids[(target_position, start_index)].add(capture_id)
            budget_exhaustion = result.get("budget_exhaustion")
            if result.get("status") == "solver_budget_exhausted" and not isinstance(budget_exhaustion, Mapping):
                raise ValueError(f"v2 P7 target {key} solver exhaustion lacks pre-capture evidence")
            derived_goal_confirmed = confirmed_group_count > 0
            if bool(result.get("goal_confirmed")) != derived_goal_confirmed:
                raise ValueError(f"v2 P7 target {key} goal_confirmed differs from confirmation groups")
            if (result.get("status") == "goal_confirmed") != derived_goal_confirmed:
                raise ValueError(f"v2 P7 target {key} result status differs from confirmation groups")
            if derived_goal_confirmed:
                derived_confirmed_attempts.append(attempt)
            best = result.get("best")
            if best is not None and best not in samples:
                raise ValueError(f"v2 P7 target {key} best sample is not retained in its start")
            recomputed_logical += logical
        if int(feedback.get("logical_observations_used", -1)) != recomputed_logical:
            raise ValueError(f"v2 P7 target {key} target logical count differs from raw evidence")
        if recomputed_logical > int(declared["solver_budget"]["max_logical_observations_per_target"]):
            raise ValueError(f"v2 P7 target {key} exceeds target logical budget")

        confirmed_attempts = derived_confirmed_attempts
        valid_attempts = [item for item in attempts if item["result"].get("best") is not None]
        pool = confirmed_attempts or valid_attempts
        derived_attempt = min(pool, key=lambda item: hsi_objective_sort_key(item["result"]["best"]["objective"])) if pool else attempts[0]
        selected_index = int(derived_attempt["start_index"])
        selected = derived_attempt["result"]
        if int(feedback.get("selected_start_index", -1)) != selected_index or feedback.get("selected_result") != selected or feedback.get("best_valid_sample") != selected.get("best"):
            raise ValueError(f"v2 P7 target {key} selected_result provenance mismatch")
        overall_status = "goal_confirmed" if confirmed_attempts else "solver_budget_exhausted" if any(item["result"].get("status") == "solver_budget_exhausted" for item in attempts) else "measurement_unreachable" if all(item["result"].get("status") == "measurement_unreachable" for item in attempts) else "unconfirmed"
        if feedback.get("status") != overall_status or row.get("selected_command") != selected.get("selected_command"):
            raise ValueError(f"v2 P7 target {key} multiseed status/command derivation mismatch")
        physical = row.get("physical_budget")
        if not isinstance(physical, Mapping):
            raise ValueError(f"v2 P7 target {key} lacks physical budget evidence")
        expected_caps = {
            "hard_cap": int(declared["solver_budget"]["max_physical_cr3_per_target"]),
            "autoexposure_cap": int(declared["solver_budget"]["max_autoexposure_physical_captures_per_target"]),
            "weak_reacquire_cap": int(declared["solver_budget"]["max_weak_signal_reacquire_physical_captures_per_target"]),
        }
        if any(int(physical.get(name, -1)) != value for name, value in expected_caps.items()):
            raise ValueError(f"v2 P7 target {key} physical frozen sub-budget drift")
        target_captures = [
            item for item in captures
            if item.get("target_index") is not None and int(item["target_index"]) == int(declared["index"])
        ]
        recomputed_physical = 0
        recomputed_auto = 0
        recomputed_weak = 0
        physical_events = []
        for capture in target_captures:
            payload = capture.get("capture") or {}
            is_auto = bool(payload.get("auto_exposure_audit"))
            is_weak = str(capture.get("purpose", "")).endswith("weak-signal-reacquire")
            synthetic_attempt = {
                "auto_exposure": is_auto,
                "auto_exposure_audit": payload.get("auto_exposure_audit"),
                "physical_capture_count": payload.get("physical_capture_count", 1),
            }
            count = recompute_physical_count(synthetic_attempt)
            recomputed_physical += count
            recomputed_auto += count if is_auto else 0
            recomputed_weak += count if is_weak else 0
            physical_events.append({"phase": capture["purpose"], "physical_cr3": count, "auto_exposure": is_auto, "weak_reacquire": is_weak})
        if physical.get("events") != physical_events or int(physical.get("physical_cr3_used", -1)) != recomputed_physical:
            raise ValueError(f"v2 P7 target {key} physical ledger differs from retained captures")
        if recomputed_auto != int(physical.get("autoexposure_physical_cr3_used", -1)) or recomputed_weak != int(physical.get("weak_reacquire_physical_cr3_used", -1)):
            raise ValueError(f"v2 P7 target {key} physical sub-budget differs from retained captures")
        if recomputed_physical > int(physical["hard_cap"]) or recomputed_auto > int(physical["autoexposure_cap"]) or recomputed_weak > int(physical["weak_reacquire_cap"]):
            raise ValueError(f"v2 P7 target {key} exceeded physical hard cap")
        target_capture_by_id = {str(item["capture_id"]): item for item in target_captures}
        for event in commands:
            if event.get("event") != "weak_signal_reacquire":
                continue
            capture_id = str(event.get("capture_id"))
            base = target_capture_by_id.get(capture_id)
            reacquires = [
                item for item in target_captures
                if str(item.get("purpose")) == f"{base.get('purpose')}-weak-signal-reacquire"
            ] if base is not None else []
            if len(reacquires) == 1 and str(reacquires[0]["capture_id"]) in capture_owners and capture_id not in capture_owners:
                reacquire_owner = capture_owners[str(reacquires[0]["capture_id"])]
                match = re.search(r":start-(\d+):", reacquire_owner)
                if match is None:
                    raise ValueError(f"v2 P7 target {key} weak reacquire owner lacks start provenance")
                start_index = int(match.group(1))
                _claim_capture(capture_owners, capture_id, f"target-{target_position}:start-{start_index}:weak-base")
                start_capture_ids.setdefault((target_position, start_index), set()).add(capture_id)
        unconsumed = {str(item["capture_id"]) for item in target_captures} - set(capture_owners)
        if unconsumed:
            raise ValueError(f"v2 P7 target {key} contains orphan captures")
        target_capture_by_id = {str(item["capture_id"]): item for item in target_captures}
        target_start_capture_ids = {
            start_index: capture_ids
            for (owner_target, start_index), capture_ids in start_capture_ids.items()
            if owner_target == target_position
        }
        start_counters = _recompute_start_capture_counters(target_capture_by_id, target_start_capture_ids)
        for attempt in attempts:
            result = attempt["result"]
            budget_exhaustion = result.get("budget_exhaustion")
            if budget_exhaustion is None:
                continue
            start_index = int(attempt["start_index"])
            budget = result.get("budget")
            if not isinstance(budget, Mapping) or not isinstance(budget.get("exhaustion"), Mapping):
                raise ValueError(f"v2 P7 target {key} exhaustion is not duplicated in start budget")
            if dict(budget["exhaustion"]) != dict(budget_exhaustion):
                raise ValueError(f"v2 P7 target {key} exhaustion differs from start budget ledger")
            _validate_pre_capture_exhaustion(
                budget_exhaustion, target_key=key,
                expected_start_index=start_index,
                expected_counters=start_counters.get(start_index, {}),
                expected_budget=budget,
            )
        objectives = [sample.get("objective", {}) for attempt in attempts for sample in attempt.get("result", {}).get("samples", [])]
        if not objectives:
            raise ValueError(f"v2 P7 target {key} has no objective evidence")
        for objective in objectives:
            if objective.get("policy_artifact_sha256") != policy.artifact_sha256:
                raise ValueError(f"v2 P7 target {key} objective policy hash drift")
            for layer in ("hsi_coordinate_equivalent", "observer_equivalent", "color_rendering_residual"):
                if layer not in objective:
                    raise ValueError(f"v2 P7 target {key} lacks {layer}")
        objective_count += len(objectives)
        best = selected.get("best")
        if not isinstance(best, Mapping):
            raise ValueError(f"v2 P7 target {key} lacks best-valid sample")
        best_objective = best["objective"]
        confirmed_groups = [item for item in selected.get("confirmation_attempts", []) if item.get("status") == "confirmed"]
        evidence_samples = [selected["samples"][int(index)] for index in confirmed_groups[-1]["sample_indices"]] if confirmed_groups else []
        replayed_spread = None
        if evidence_samples:
            class_policy = policy.artifact["repeatability_policy"]["classes"][repeatability_class]
            replayed_spread = evaluate_confirmation_spread(
                [sample["observation"]["feature_values"] for sample in evidence_samples],
                feature_ids=feature_ids, class_name=repeatability_class,
                class_variance=conservative_class_variance(
                    class_policy["p1_floor_diagonal_variance"],
                    class_policy["targeted_variance"], feature_ids,
                ),
                limit=class_policy["limits"][str(expected_confirmation_count)],
            )
        if not _json_numerically_equal(row.get("confirmation_spread"), replayed_spread):
            raise ValueError(f"v2 P7 target {key} confirmation spread differs from RAW replay")
        unresolved = any(item.get("objective", {}).get("hsi_coordinate_equivalent") in {"unresolved", "uncertainty_unresolved"} for item in evidence_samples) or (replayed_spread is not None and replayed_spread.get("decision") != "pass")
        selected_confirmed = selected in [item["result"] for item in derived_confirmed_attempts]
        derived_status = "uncertainty_unresolved" if unresolved else "faithful" if selected_confirmed else "solver_budget_exhausted" if overall_status == "solver_budget_exhausted" else "measurement_unreachable" if overall_status == "measurement_unreachable" else "unconfirmed"
        if reported_status != derived_status:
            raise ValueError(f"v2 P7 target {key} result status differs from reconstructed evidence")
        reconstructed_targets.append({
            "target": {"hue": key[0], "sat": key[1]},
            "reported_logical_observations": int(feedback.get("logical_observations_used", -1)),
            "recomputed_logical_observations": recomputed_logical,
            "reported_physical_cr3": int(physical.get("physical_cr3_used", -1)),
            "recomputed_physical_cr3": recomputed_physical,
            "reported_result_status": reported_status,
            "recomputed_result_status": derived_status,
        })
        points.append({
            "hue": key[0], "sat": key[1], "status": "complete",
            "result_status": derived_status, "goal_confirmed": bool(selected.get("goal_confirmed")),
            "selected_start_index": selected_index,
            "selected_command": row.get("selected_command"),
            "logical_observations_used": int(feedback["logical_observations_used"]),
            "physical_cr3_used": int(physical["physical_cr3_used"]),
            "confirmation_count": expected_confirmation_count,
            "confirmation_spread": replayed_spread,
            "hsi_coordinate_equivalent": best_objective["hsi_coordinate_equivalent"],
            "observer_equivalent": best_objective["observer_equivalent"],
            "color_rendering_residual": best_objective["color_rendering_residual"],
        })
        previous_command = {channel: int(row["selected_command"][channel]) for channel in ("cw", "ww", "r", "g", "b")}
    return ({
        "target_count": len(rows),
        "objective_count": objective_count,
        "policy_artifact_sha256": policy.artifact_sha256,
        "multiseed_provenance": "pass",
        "budget_audit": "pass",
        "confirmation_group_audit": "pass",
        "three_layer_result_audit": "pass",
        "status_exclusivity": "pass",
        "capture_owner_audit": "pass",
        "feature_provenance_audit": "pass",
        "objective_replay_audit": "pass",
        "confirmation_derived_status_audit": "pass",
        "frozen_sub_budget_audit": "pass",
        "reconstructed_targets": reconstructed_targets,
    }, sorted(points, key=lambda item: (item["hue"], item["sat"])))


def _point_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    target = row["target"]
    if row.get("status") == "measurement_unreachable":
        return {"hue": int(target["hue"]), "sat": int(target["sat"]), "status": "measurement_unreachable", "gamut_status": "unconfirmed", "stage": row.get("stage")}
    feedback = row["feedback"]
    best = feedback["best"]["objective"]
    return {
        "hue": int(target["hue"]),
        "sat": int(target["sat"]),
        "status": "complete",
        "gamut_status": row.get("result_status", row["gamut_status"]),
        "goal_confirmed": bool(feedback["goal_confirmed"]),
        "selected_command": row["selected_command"],
        "max_code": int(target.get("max_code", 4095)),
        "full_scale_policy": bool(target.get("full_scale_policy", True)),
        "scale_relaxed_diagnostics": [
            {
                "max_code": item.get("max_code"),
                "result_status": item.get("result_status", "measurement_unreachable" if item.get("measurement_rejected") else None),
                "selected_command": item.get("selected_command"),
                "confirmation_spread": item.get("confirmation_spread"),
            }
            for item in row.get("scale_relaxed_diagnostics", [])
        ],
        "active_channel": feedback["active_channel"],
        "hue_error_degrees": best.get("hue_error_degrees"),
        "sat_error_percent": best.get("sat_error_percent"),
        "orthogonal_residual": best.get("orthogonal_residual"),
        "rounds_completed": int(feedback["rounds_completed"]),
        "settled_evidence_count": sum(len(item.get("sample_indices", [])) for item in feedback["confirmation_attempts"]) + len(row.get("final_verification", [])),
    }


def _claim_capture(owners: dict[str, str], capture_id: str, owner: str) -> None:
    previous = owners.get(capture_id)
    if previous is not None:
        raise ValueError(f"capture {capture_id} has duplicate owners: {previous}, {owner}")
    owners[capture_id] = owner


def _validate_measurement_rejection_evidence(
    evidence: Any, *, phase: str, command: Mapping[str, Any],
    target_index: int, target_key: tuple[int, int],
) -> None:
    if not isinstance(evidence, Mapping) or not evidence:
        raise ValueError(f"v2 P7 target {target_key} measurement rejection has empty evidence")
    if evidence.get("status") == "solver_budget_exhausted" or evidence.get("pre_capture_exhaustion") is True:
        raise ValueError(f"v2 P7 target {target_key} quality rejection impersonates pre-capture exhaustion")
    required = {"source", "purpose", "capture_ids", "exposure_factors", "rejected_features"}
    if not required.issubset(evidence):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection schema is incomplete")
    if not phase or not str(evidence.get("purpose", "")).endswith(phase):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection phase is missing")
    capture_ids = evidence.get("capture_ids")
    if not isinstance(capture_ids, list) or not capture_ids or len(capture_ids) != len(set(map(str, capture_ids))):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection requires unique capture ids")
    if str(evidence.get("source")) != "strip":
        raise ValueError(f"v2 P7 target {target_key} measurement rejection source drift")
    exposure_factors = evidence.get("exposure_factors")
    rejected_features = evidence.get("rejected_features")
    if (
        not isinstance(exposure_factors, list) or not exposure_factors
        or not isinstance(rejected_features, list) or not rejected_features
    ):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection lacks quality evidence")
    if any(not isinstance(item, Mapping) or not item for item in rejected_features):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection has malformed quality evidence")
    if set(command) != {"cw", "ww", "r", "g", "b"} or any(not isinstance(value, int) for value in command.values()):
        raise ValueError(f"v2 P7 target {target_key} measurement rejection command is invalid")
    if int(target_index) < 0:
        raise ValueError(f"v2 P7 target {target_key} measurement rejection target index is invalid")


def _validate_pre_capture_exhaustion(
    evidence: Any, *, target_key: tuple[int, int], expected_start_index: int,
    expected_counters: Mapping[str, int], expected_budget: Mapping[str, Any],
) -> None:
    if not isinstance(evidence, Mapping):
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion evidence is missing")
    required = {
        "pre_capture_exhaustion", "status", "sub_budget", "phase",
        "requested_physical_cr3", "physical_cr3_used",
        "autoexposure_physical_cr3_used", "weak_reacquire_physical_cr3_used",
        "capture_attempted", "start_index",
    }
    if not required.issubset(evidence) or evidence.get("pre_capture_exhaustion") is not True:
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion schema is incomplete")
    if evidence.get("status") != "solver_budget_exhausted" or evidence.get("capture_attempted") is not False:
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion status is invalid")
    if "capture_ids" in evidence:
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion cannot contain capture ids")
    if int(evidence.get("start_index", -1)) != int(expected_start_index):
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion start mismatch")
    if not str(evidence.get("sub_budget")) or not str(evidence.get("phase")):
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion lacks budget phase")
    if int(evidence.get("requested_physical_cr3", -1)) != 0:
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion requested a capture")
    for field in ("physical_cr3_used", "autoexposure_physical_cr3_used", "weak_reacquire_physical_cr3_used"):
        if not isinstance(evidence.get(field), (int, float)) or int(evidence[field]) < 0:
            raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion counter is invalid")
        if int(evidence[field]) != int(expected_counters.get(field, -1)):
            raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion counter differs from capture ledger")
    budget_exhaustion = expected_budget.get("exhaustion")
    if not isinstance(budget_exhaustion, Mapping) or dict(budget_exhaustion) != dict(evidence):
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion differs from budget ledger")
    if not _phase_matches_sub_budget(
        str(evidence.get("phase")), str(evidence.get("sub_budget")), expected_budget,
    ):
        raise ValueError(f"v2 P7 target {target_key} pre-capture exhaustion phase/sub-budget mismatch")


def _phase_matches_sub_budget(phase: str, sub_budget: str, budget: Mapping[str, Any]) -> bool:
    prefixes = {
        "initial": "initial",
        "initial_probes": "probe-",
        "rebase_probes": "rebase-",
        "feedback_attempts": "feedback-",
        "confirmation_captures": "confirm-",
    }
    if sub_budget in prefixes:
        return phase.startswith(prefixes[sub_budget])
    if sub_budget != "logical_observations":
        return False
    consumed = budget.get("consumed")
    limits = budget.get("limits")
    if not isinstance(consumed, Mapping) or not isinstance(limits, Mapping):
        return False
    category_limits = {
        "initial": ("initial", 1),
        "initial_probes": ("probe-", int(limits.get("rebase_probe_count", 0))),
        "rebase_probes": ("rebase-", int(limits.get("max_rebases_per_start", 0)) * int(limits.get("rebase_probe_count", 0))),
        "feedback_attempts": ("feedback-", int(limits.get("max_feedback_capture_attempts_per_start", 0))),
        "confirmation_captures": ("confirm-", int(limits.get("max_confirmation_groups_per_start", 0)) * int(limits.get("confirmation_captures_per_group", 0))),
    }
    return any(
        int(consumed.get(category, -1)) >= maximum and phase.startswith(prefix)
        for category, (prefix, maximum) in category_limits.items()
    )


def _recompute_start_capture_counters(
    captures_by_id: Mapping[str, Mapping[str, Any]],
    start_capture_ids: Mapping[int, set[str]],
) -> dict[int, dict[str, int]]:
    counters: dict[int, dict[str, int]] = {}
    for start_index, capture_ids in start_capture_ids.items():
        values = {
            "physical_cr3_used": 0,
            "autoexposure_physical_cr3_used": 0,
            "weak_reacquire_physical_cr3_used": 0,
        }
        for capture_id in capture_ids:
            capture = captures_by_id.get(capture_id)
            if capture is None:
                raise ValueError(f"capture ledger references unknown id {capture_id}")
            payload = capture.get("capture") or {}
            attempt = {
                "auto_exposure": bool(payload.get("auto_exposure_audit")),
                "auto_exposure_audit": payload.get("auto_exposure_audit"),
                "physical_capture_count": payload.get("physical_capture_count", 1),
            }
            count = recompute_physical_count(attempt)
            values["physical_cr3_used"] += count
            if attempt["auto_exposure"]:
                values["autoexposure_physical_cr3_used"] += count
            if str(capture.get("purpose", "")).endswith("weak-signal-reacquire"):
                values["weak_reacquire_physical_cr3_used"] += count
        counters[int(start_index)] = values
    return counters


def _json_numerically_equal(left: Any, right: Any, *, tolerance: float = 1e-12) -> bool:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return set(left) == set(right) and all(_json_numerically_equal(left[key], right[key], tolerance=tolerance) for key in left)
    if isinstance(left, Sequence) and not isinstance(left, (str, bytes)) and isinstance(right, Sequence) and not isinstance(right, (str, bytes)):
        return len(left) == len(right) and all(_json_numerically_equal(a, b, tolerance=tolerance) for a, b in zip(left, right))
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right)) <= tolerance
    return left == right


def _v2_repeatability_class(*, target_sat: float, max_code: int, formal_max_code: int) -> str:
    if max_code != formal_max_code:
        if target_sat != 0.0:
            raise ValueError("v2 scale-relaxed repeatability is frozen only for neutral targets")
        return "neutral_scale_relaxed"
    if target_sat == 0.0:
        return "neutral_fullscale"
    if target_sat == 100.0:
        return "sat100_fullscale"
    return "mid_sat_fullscale"


def _faithful(row: Mapping[str, Any]) -> bool:
    return row.get("status") == "complete" and row.get("gamut_status") == "faithful"


def _validate_captures(captures: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    raw_count = 0
    recorded_count = 0
    measurement_count = 0
    for record in captures:
        capture = record.get("capture", {})
        raw_path = Path(str(capture.get("capture", {}).get("saved_file", "")))
        if not raw_path.is_file() or raw_path.stat().st_size <= 0:
            raise ValueError(f"missing or empty CR3 for {record.get('capture_id')}")
        raw_count += 1
        report_path = Path(str(capture.get("patch_statistics", "")))
        if not report_path.is_file():
            raise ValueError(f"missing measurement report for {record.get('capture_id')}")
        measurement_count += 1
        report = _load_json(report_path)
        if report.get("exposure_metadata", {}).get("status") != "recorded":
            raise ValueError(f"capture {record.get('capture_id')} lacks recorded exposure")
        recorded_count += 1
    return {"capture_count": len(captures), "raw_count": raw_count, "measurement_count": measurement_count, "recorded_exposure_count": recorded_count, "npy_count": 0}


def _group_commands(
    commands: Sequence[Mapping[str, Any]],
) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for command in commands:
        capture_id = str(command.get("capture_id", ""))
        if not capture_id:
            raise ValueError("P7 command event lacks capture id")
        grouped.setdefault(capture_id, []).append(command)
    return grouped


def _validate_v2_commands(
    captures: Sequence[Mapping[str, Any]], commands: Sequence[Mapping[str, Any]],
    *, plan: Mapping[str, Any], curve: Mapping[str, Any],
) -> dict[str, Any]:
    by_capture = _group_commands(commands)
    capture_ids = {str(item["capture_id"]) for item in captures}
    if set(by_capture) != capture_ids:
        raise ValueError("v2 P7 command evidence contains orphan or missing capture ids")
    counts = {"strip": 0, "ray": 0, "ambient": 0}
    for capture in captures:
        capture_id = str(capture["capture_id"])
        source = str(capture.get("source"))
        events = [item for item in by_capture[capture_id] if item.get("event") != "weak_signal_reacquire"]
        if source == "strip":
            on = [item for item in events if item.get("event") == "strip_on_readback_verified"]
            if len(on) != 1:
                raise ValueError(f"v2 P7 strip capture {capture_id} lacks one exact source-on event")
            step = {"command": on[0].get("requested_command")}
        elif source == "ray":
            state = capture.get("ray_state")
            if not isinstance(state, Mapping):
                raise ValueError(f"v2 P7 Ray capture {capture_id} lacks frozen state provenance")
            step = {"state": state}
        elif source == "ambient":
            step = {}
        else:
            raise ValueError(f"v2 P7 capture {capture_id} has unsupported source")
        validate_attempt_event_grammar(events, source=source, plan_step=step, curve=curve)
        counts[source] += 1
    return {
        "capture_count": len(captures),
        "strip_capture_count": counts["strip"],
        "ray_capture_count": counts["ray"],
        "ambient_capture_count": counts["ambient"],
        "source_isolation": "pass",
        "requested_response_consistency": "pass",
        "frozen_plan_validation": "pass",
    }


def _validate_commands(
    captures: Sequence[Mapping[str, Any]], commands: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    by_capture: dict[str, list[Mapping[str, Any]]] = {}
    for command in commands:
        by_capture.setdefault(str(command.get("capture_id")), []).append(command)
    strip_count = 0
    ray_count = 0
    for capture in captures:
        capture_id = str(capture["capture_id"])
        events = by_capture.get(capture_id, [])
        names = [str(item.get("event")) for item in events]
        if len(names) < 2 or names[0:2] != ["strip_off", "ray_off"]:
            raise ValueError(f"capture {capture_id} does not begin with verified source isolation")
        source = capture.get("source")
        if source == "strip":
            strip_count += 1
            if "ray_on_readback_verified" in names or "strip_on" not in names or names[-1] != "strip_off":
                raise ValueError(f"strip capture {capture_id} has an invalid source command sequence")
            strip_on = next(item for item in events if item.get("event") == "strip_on")
            if strip_on.get("response_verified") is not True:
                raise ValueError(f"strip capture {capture_id} lacks verified requested/response consistency")
        elif source == "ray":
            ray_count += 1
            if "strip_on" in names or "ray_on_readback_verified" not in names or names[-1] != "ray_off":
                raise ValueError(f"Ray capture {capture_id} has an invalid source command sequence")
        elif source == "ambient":
            if "strip_on" in names or "ray_on_readback_verified" in names:
                raise ValueError(f"ambient capture {capture_id} turns on a source")
        else:
            raise ValueError(f"capture {capture_id} has unsupported source {source}")
    return {
        "capture_count": len(captures),
        "strip_capture_count": strip_count,
        "ray_capture_count": ray_count,
        "source_isolation": "pass",
        "requested_response_consistency": "pass",
    }


def _validate_input_hashes(plan: Mapping[str, Any]) -> dict[str, Any]:
    verified = []
    for name, reference in plan.get("inputs", {}).items():
        path = Path(str(reference.get("path", "")))
        if not path.is_file() or _sha256(path) != reference.get("sha256"):
            raise ValueError(f"P7 frozen input hash mismatch: {name}")
        verified.append(name)
    return {"verified_count": len(verified), "verified_inputs": sorted(verified)}


def _validate_anchors(root: Path, plan: Mapping[str, Any]) -> dict[str, Any]:
    anchors = _load_jsonl(root / "reference-anchors.jsonl")
    expected = [
        ("pre", int(item["hue"]), int(item["sat"]))
        for item in plan["reference_anchors"]["pre"]
    ] + [
        ("post", int(item["hue"]), int(item["sat"]))
        for item in plan["reference_anchors"]["post"]
    ]
    actual = [
        (str(item["position"]), int(item["target"]["hue"]), int(item["target"]["sat"]))
        for item in anchors
    ]
    if actual != expected:
        raise ValueError("P7 reference anchors are incomplete, reordered, or unexpected")
    if any(item.get("evaluation", {}).get("within_reference_coverage") is not True for item in anchors):
        raise ValueError("P7 reference anchor exceeds frozen coverage")
    return {"anchor_count": len(anchors), "pre_count": len(plan["reference_anchors"]["pre"]), "post_count": len(plan["reference_anchors"]["post"]), "reference_drift": False}


def _validate_target_evidence(rows: Sequence[Mapping[str, Any]], plan: Mapping[str, Any]) -> dict[str, Any]:
    targets = {
        (int(item["hue"]), int(item["sat"])): item for item in plan["targets"]
    }
    uncertainty_sha = str(plan["inputs"]["uncertainty_artifact"]["sha256"])
    objective_count = 0
    diagnostic_count = 0
    allowed_statuses = P7_RESULT_STATUSES

    def validate_result(result: Mapping[str, Any], *, expected_count: int, key: tuple[int, int]) -> int:
        feedback = result["feedback"]
        confirmed = [item for item in feedback.get("confirmation_attempts", []) if item.get("status") == "confirmed"]
        final = result.get("final_verification", [])
        if confirmed:
            if len(confirmed) != 1 or len(confirmed[0].get("sample_indices", [])) != expected_count:
                raise ValueError(f"P7 target {key} has an invalid confirmation count")
        elif len(final) != expected_count:
            raise ValueError(f"P7 target {key} lacks its predeclared final verification count")
        objectives = [sample["objective"] for sample in feedback.get("samples", [])] + [item["objective"] for item in final]
        for objective in objectives:
            if objective.get("uncertainty_artifact_sha256") != uncertainty_sha:
                raise ValueError(f"P7 target {key} changed uncertainty artifact during the run")
        command = result.get("selected_command", feedback.get("selected_command", {}))
        max_code = int(result.get("max_code", targets[key]["max_code"]))
        if max(map(int, command.values())) != max_code:
            raise ValueError(f"P7 target {key} violates its full-scale active-channel constraint")
        return len(objectives)

    for row in rows:
        key = (int(row["target"]["hue"]), int(row["target"]["sat"]))
        expected_count = int(targets[key]["confirmation_count"])
        if row.get("status") == "measurement_unreachable":
            continue
        status = row.get("result_status", row.get("gamut_status"))
        if status not in allowed_statuses:
            raise ValueError(f"P7 target {key} has unsupported or overlapping status {status}")
        objective_count += validate_result(row, expected_count=expected_count, key=key)
        for diagnostic in row.get("scale_relaxed_diagnostics", []):
            diagnostic_count += 1
            if diagnostic.get("measurement_rejected"):
                continue
            if int(diagnostic.get("max_code", 0)) not in {3072, 2048}:
                raise ValueError(f"P7 target {key} has an invalid scale-relaxed max_code")
            objective_count += validate_result(diagnostic, expected_count=5, key=key)
    return {"target_count": len(rows), "objective_count": objective_count, "scale_relaxed_diagnostic_count": diagnostic_count, "uncertainty_artifact_sha256": uncertainty_sha, "confirmation_policy": "pass", "status_exclusivity": "pass"}


def _cleanup_ok(value: Any) -> bool:
    steps = value.get("steps") if isinstance(value, Mapping) else value
    return isinstance(steps, list) and len(steps) == 2 and all(isinstance(step, Mapping) and step.get("ok") is True for step in steps)


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_json_value(path: Path) -> Any:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_strip_hsi_pilot_analysis(output: str | Path, analysis: Mapping[str, Any]) -> Path:
    path = Path(output)
    path.write_text(json.dumps(analysis, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a completed P7 strip HSI pilot.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--remaining-run", type=Path)
    parser.add_argument(
        "--policy-version", choices=("v1", "v2"), required=True,
        help="Policy version is mandatory; v1 and v2 analyzers never silently fall back.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = analyze_combined_strip_hsi_pilot(
        args.run_dir, args.remaining_run, policy_version=args.policy_version,
    ) if args.remaining_run else analyze_strip_hsi_pilot(
        args.run_dir, policy_version=args.policy_version,
    )
    print(write_strip_hsi_pilot_analysis(args.output or args.run_dir / "strip-hsi-pilot-analysis.json", analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
