from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    FROZEN_STATUS,
    HsiPolicyV2,
)
from camera_based_rgbww_optimizer.optimization.hsi_objective import P7_RESULT_STATUSES


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
    command_validation = _validate_commands(captures, commands)
    anchor_validation = _validate_v2_reference_blocks(root, plan)
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
        rows, plan, policy_artifact_sha256=policy.artifact_sha256,
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


def _validate_v2_reference_blocks(root: Path, plan: Mapping[str, Any]) -> dict[str, Any]:
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
    pre = _load_json(root / "reference-pre-analysis.json")
    post = _load_json(root / "reference-post-analysis.json")
    if pre.get("status") != "pass" or post.get("status") != "pass":
        raise ValueError("v2 P7 reference block analysis did not pass")
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
    *, policy_artifact_sha256: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    target_plan = {(int(item["hue"]), int(item["sat"])): item for item in plan["targets"]}
    points: list[dict[str, Any]] = []
    objective_count = 0
    for row in rows:
        key = (int(row["target"]["hue"]), int(row["target"]["sat"]))
        declared = target_plan[key]
        status = str(row.get("result_status"))
        if status not in P7_RESULT_STATUSES or row.get("gamut_status") != status:
            raise ValueError(f"v2 P7 target {key} has overlapping or unsupported result status")
        feedback = row.get("feedback")
        if not isinstance(feedback, Mapping) or feedback.get("kind") != "hsi_bounded_multiseed_feedback_v2":
            raise ValueError(f"v2 P7 target {key} lacks multiseed evidence")
        if feedback.get("budget_declaration") != declared.get("solver_budget"):
            raise ValueError(f"v2 P7 target {key} solver budget declaration drift")
        attempts = feedback.get("attempts")
        if not isinstance(attempts, list) or not 1 <= len(attempts) <= 2:
            raise ValueError(f"v2 P7 target {key} has invalid multiseed attempt count")
        selected_index = int(feedback.get("selected_start_index", -1))
        selected_rows = [item for item in attempts if int(item.get("start_index", -1)) == selected_index]
        if len(selected_rows) != 1 or selected_rows[0].get("result") != feedback.get("selected_result"):
            raise ValueError(f"v2 P7 target {key} selected_result provenance mismatch")
        selected = selected_rows[0]["result"]
        expected_confirmation_count = int(declared["confirmation_count"])
        confirmed_groups = [item for item in selected.get("confirmation_attempts", []) if item.get("status") == "confirmed"]
        if selected.get("goal_confirmed"):
            if len(confirmed_groups) != 1 or len(confirmed_groups[0].get("sample_indices", [])) != expected_confirmation_count:
                raise ValueError(f"v2 P7 target {key} has invalid confirmed group size")
        elif not selected.get("confirmation_attempts"):
            raise ValueError(f"v2 P7 target {key} lacks final-verification group evidence")
        for attempt in attempts:
            budget = attempt.get("result", {}).get("budget", {})
            if int(budget.get("logical_observations_used", -1)) > int(declared["solver_budget"]["max_logical_observations_per_start"]):
                raise ValueError(f"v2 P7 target {key} exceeds per-start logical budget")
            if int(budget.get("confirmation_groups_started", -1)) > int(declared["solver_budget"]["max_confirmation_groups_per_start"]):
                raise ValueError(f"v2 P7 target {key} exceeds confirmation-group budget")
        if int(feedback.get("logical_observations_used", -1)) > int(declared["solver_budget"]["max_logical_observations_per_target"]):
            raise ValueError(f"v2 P7 target {key} exceeds target logical budget")
        physical = row.get("physical_budget")
        if not isinstance(physical, Mapping):
            raise ValueError(f"v2 P7 target {key} lacks physical budget evidence")
        if int(physical.get("hard_cap", -1)) != int(declared["solver_budget"]["max_physical_cr3_per_target"]):
            raise ValueError(f"v2 P7 target {key} physical hard cap drift")
        if int(physical.get("physical_cr3_used", -1)) > int(physical["hard_cap"]):
            raise ValueError(f"v2 P7 target {key} exceeded physical hard cap")
        objectives = [sample.get("objective", {}) for attempt in attempts for sample in attempt.get("result", {}).get("samples", [])]
        if not objectives:
            raise ValueError(f"v2 P7 target {key} has no objective evidence")
        for objective in objectives:
            if objective.get("policy_artifact_sha256") != policy_artifact_sha256:
                raise ValueError(f"v2 P7 target {key} objective policy hash drift")
            for layer in ("hsi_coordinate_equivalent", "observer_equivalent", "color_rendering_residual"):
                if layer not in objective:
                    raise ValueError(f"v2 P7 target {key} lacks {layer}")
        objective_count += len(objectives)
        best = selected.get("best") or feedback.get("best_valid_sample")
        if not isinstance(best, Mapping):
            raise ValueError(f"v2 P7 target {key} lacks best-valid sample")
        best_objective = best["objective"]
        points.append({
            "hue": key[0], "sat": key[1], "status": "complete",
            "result_status": status, "goal_confirmed": bool(selected.get("goal_confirmed")),
            "selected_start_index": selected_index,
            "selected_command": row.get("selected_command"),
            "logical_observations_used": int(feedback["logical_observations_used"]),
            "physical_cr3_used": int(physical["physical_cr3_used"]),
            "confirmation_count": expected_confirmation_count,
            "confirmation_spread": row.get("confirmation_spread"),
            "hsi_coordinate_equivalent": best_objective["hsi_coordinate_equivalent"],
            "observer_equivalent": best_objective["observer_equivalent"],
            "color_rendering_residual": best_objective["color_rendering_residual"],
        })
    return ({
        "target_count": len(rows),
        "objective_count": objective_count,
        "policy_artifact_sha256": policy_artifact_sha256,
        "multiseed_provenance": "pass",
        "budget_audit": "pass",
        "confirmation_group_audit": "pass",
        "three_layer_result_audit": "pass",
        "status_exclusivity": "pass",
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
