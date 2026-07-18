from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    AUDIT_THRESHOLDS,
    DEFAULT_BOOTSTRAP_REPLICATES,
    DEFAULT_MC_SAMPLES,
    DEFAULT_MC_SEED,
    HsiPolicyV2,
    REPEATABILITY_CLASSES,
    calibrate_confirmation_group_limit,
    calibrate_direct_limits,
    calibrate_joint_regions,
    conservative_class_variance,
    evaluate_reference_difference,
    ordered_unit_shape,
    summarize_within_groups,
)
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import (
    load_ray_repeat_groups,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization.measure_hsi_reference_repeatability import (
    EXPERIMENT_NAME,
)
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    HsiRejectedFeaturesError,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
    recompute_physical_count,
    validate_attempt_event_grammar,
)


CLASS_COMMANDS = {
    "neutral_fullscale": ("h0-s0-fullscale",),
    "mid_sat_fullscale": ("h120-s50-fullscale",),
    "sat100_fullscale": ("h120-s100-fullscale", "h300-s100-fullscale"),
    "neutral_scale_relaxed": ("h0-s0-scale-relaxed-3072",),
}
HIGH_VARIANCE_RATIO = 1.5


def analyze_reference_repeatability_run(
    run_dir: str | Path,
    *, monte_carlo_samples: int = DEFAULT_MC_SAMPLES,
    bootstrap_replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = DEFAULT_MC_SEED,
    require_shell_cleanup: bool = True,
) -> dict[str, Any]:
    root = Path(run_dir)
    plan = _load_json(root / "plan.json")
    run = _load_json(root / "run.json")
    if plan.get("experiment") != EXPERIMENT_NAME or run.get("status") != "complete":
        raise ValueError("P7-R1 analyzer requires a completed exact named-experiment run")
    _verify_input_hashes(plan["inputs"])
    captures = _load_jsonl(root / "captures.jsonl")
    attempts = _load_jsonl(root / "capture-attempts.jsonl")
    commands = _load_jsonl(root / "commands.jsonl")
    if len(captures) != 82 or sum(bool(item.get("formal_measurement")) for item in captures) != 80:
        raise ValueError("P7-R1 analyzer requires exactly 82 logical and 80 formal captures")
    if list(root.rglob("*.npy")):
        raise ValueError("P7-R1 run must retain zero .npy files")
    cleanup = {
        "python": _cleanup_ok(root / "all-off-python.json"),
        "shell": _cleanup_ok(root / "all-off-shell.json") if (root / "all-off-shell.json").is_file() else False,
    }
    if not cleanup["python"] or (require_shell_cleanup and not cleanup["shell"]):
        raise ValueError("P7-R1 analyzer requires successful Python and shell cleanup")
    policy = HsiPolicyV2.load(plan["inputs"]["policy_v2_waiting"]["path"])
    if policy.formal_capture_eligible:
        raise ValueError("P7-R1 input policy must remain formal-ineligible")
    manifold = RayHsiManifold.load(plan["inputs"]["ray_hsi_manifold"]["path"])
    feature_ids = tuple(policy.artifact["feature_set"]["ids"])
    if feature_ids != tuple(manifold.coordinate_feature_ids):
        raise ValueError("P7-R1 policy/manifold feature-order mismatch")
    physical_audit = _audit_capture_contract(
        captures, attempts, commands, feature_ids, run=run,
        physical_contract=plan["measurement"]["physical_capture_audit"],
        plan=plan,
    )

    ray_current = _group_ray(captures)
    strip_current = _group_strip(captures)
    p6_root = Path(plan["inputs"]["p6_run_json"]["path"]).parent
    p6_groups = load_ray_repeat_groups(manifold, p6_root)
    ray_analysis, reference_states = _analyze_ray(
        ray_current, p6_groups, policy=policy, feature_ids=feature_ids,
        seed=seed, monte_carlo_samples=monte_carlo_samples,
    )
    strip_analysis, class_components = _analyze_strip(
        strip_current, policy=policy, feature_ids=feature_ids,
        seed=seed, monte_carlo_samples=monte_carlo_samples,
    )
    candidate, joint_report = _build_candidate(
        policy, manifold,
        reference_states=reference_states,
        class_components=class_components,
        seed=seed,
        monte_carlo_samples=monte_carlo_samples,
        bootstrap_replicates=bootstrap_replicates,
    )
    branch = select_reference_repeatability_branch(
        ray_analysis=ray_analysis,
        strip_analysis=strip_analysis,
        joint_report=joint_report,
    )
    blocking_evidence = {
        "ray_states": ray_analysis.get("failed_states", []),
        "strip_commands": strip_analysis.get("failed_commands", []),
        "joint_regions": joint_report.get("failed_regions", []),
    }
    return {
        "schema_version": 2,
        "experiment": EXPERIMENT_NAME,
        "status": "calibrated_waiting_for_planner",
        "formal_capture_eligible": False,
        "branch": branch,
        "blocking_evidence": blocking_evidence,
        "cleanup": cleanup,
        "capture_audit": {
            "logical_count": len(captures),
            "formal_ray_count": sum(item["source"] == "ray" for item in captures),
            "formal_strip_count": sum(item["source"] == "strip" for item in captures),
            "ambient_count": sum(item["source"] == "ambient" for item in captures),
            **physical_audit,
            "recorded_exposure_required": True,
            "source_isolation_and_readback": "pass",
            "retained_npy_count": 0,
        },
        "ray_reference": ray_analysis,
        "strip_repeatability": strip_analysis,
        "synthetic_joint_coverage": joint_report,
        "candidate_policy": candidate,
        "unmeasured_statistics": [
            "new_sentinel_v2 convergence",
            "remaining_9 convergence",
            "boundary behavior",
            "holdout behavior",
            "real empirical coordinate coverage outside the three P7-R1 Ray states",
        ],
    }


def select_reference_repeatability_branch(
    *, ray_analysis: Mapping[str, Any], strip_analysis: Mapping[str, Any],
    joint_report: Mapping[str, Any],
) -> str:
    failures = [
        item for item in (
            ray_analysis.get("failure_branch"),
            strip_analysis.get("failure_branch"),
            joint_report.get("failure_branch"),
        ) if item
    ]
    if failures:
        return "uncertainty_unresolved" if "uncertainty_unresolved" in failures else str(failures[0])
    if ray_analysis.get("reference_epoch_shift"):
        return "R-REFERENCE-EPOCH"
    if strip_analysis.get("classes_above_p1_floor"):
        return "R-STRIP-CLASS-HIGH"
    return "R-PASS"


def finalize_reference_repeatability_run(
    run_dir: str | Path, *, analysis: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> tuple[Path, Path]:
    root = Path(run_dir)
    report = dict(analysis or analyze_reference_repeatability_run(root, **kwargs))
    if report.get("status") != "calibrated_waiting_for_planner":
        raise ValueError("P7-R1 finalizer only writes a Planner-waiting candidate")
    HsiPolicyV2(report["candidate_policy"])
    report_path = root / "analysis.json"
    candidate_path = root / "strip-hsi-policy-v2-candidate.json"
    _write_json(report_path, report)
    _write_json(candidate_path, report["candidate_policy"])
    return report_path, candidate_path


def _analyze_ray(
    current: Mapping[str, Mapping[str, Sequence[Mapping[str, float]]]],
    p6_groups: Mapping[str, Sequence[Sequence[float]]],
    *, policy: HsiPolicyV2, feature_ids: Sequence[str], seed: int,
    monte_carlo_samples: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    states: dict[str, Any] = {}
    epoch_shift = False
    unstable = False
    unresolved = False
    failed_states: list[dict[str, Any]] = []
    frozen_variance = policy.artifact["reference_policy"]["ray_within_state_diagonal_variance"]
    for state_key, blocks in sorted(current.items()):
        summary = summarize_within_groups(blocks, feature_ids)
        if summary["status"] != "pass":
            unstable = True
            failed_states.append({"state": state_key, "branch": "repeatability_audit", "failures": summary["audit"]["failure_branches"]})
        p6_key = f"p6:{state_key.replace('-', ':')}"
        if p6_key not in p6_groups:
            raise ValueError(f"P6 run lacks exact state {p6_key}")
        p6_rows = np.asarray(p6_groups[p6_key], dtype=float)
        frozen_center = np.mean(p6_rows, axis=0)
        current_center = np.mean(np.vstack([
            np.vstack([ordered_unit_shape(row, feature_ids) for row in rows])
            for rows in blocks.values()
        ]), axis=0)
        current_variance = summary["diagonal_variance"]
        mean_covariance = (
            np.asarray(frozen_variance, dtype=float) / len(p6_rows)
            + np.asarray(current_variance, dtype=float) / summary["sample_count"]
        )
        center_region = calibrate_direct_limits(
            frozen_center, mean_covariance,
            seed=seed + len(states), samples=monte_carlo_samples,
        )
        compatibility = evaluate_reference_difference(
            frozen_center, current_center,
            left_variance=frozen_variance, left_count=len(p6_rows),
            right_variance=current_variance, right_count=summary["sample_count"],
            feature_ids=feature_ids,
            guarded_limit=center_region["guarded_limit"],
            unguarded_limit=center_region["unguarded_limit"],
            statistic="reference_center_compatibility",
        )
        a = summary["group_centers"]["A"]
        b = summary["group_centers"]["B"]
        repeat_covariance = 2.0 * np.asarray(current_variance, dtype=float) / len(blocks["A"])
        repeat_region = calibrate_direct_limits(
            a, repeat_covariance,
            seed=seed + 100 + len(states), samples=monte_carlo_samples,
        )
        repeatability = evaluate_reference_difference(
            a, b,
            left_variance=current_variance, left_count=len(blocks["A"]),
            right_variance=current_variance, right_count=len(blocks["B"]),
            feature_ids=feature_ids,
            guarded_limit=repeat_region["guarded_limit"],
            unguarded_limit=repeat_region["unguarded_limit"],
            statistic="reference_repeatability",
        )
        epoch_shift |= compatibility["decision"] == "fail" and repeatability["decision"] == "pass"
        unstable |= repeatability["decision"] == "fail"
        unresolved |= compatibility["decision"] == "unresolved" or repeatability["decision"] == "unresolved"
        if compatibility["decision"] != "pass" or repeatability["decision"] != "pass":
            failed_states.append({
                "state": state_key,
                "compatibility": compatibility["decision"],
                "pre_post_repeatability": repeatability["decision"],
            })
        states[state_key] = {
            "current": summary,
            "compatibility": compatibility,
            "pre_post_repeatability": repeatability,
            "frozen_center": frozen_center.tolist(),
            "frozen_diagonal_variance": list(frozen_variance),
            "frozen_count": len(p6_rows),
            "center_compatibility_region": center_region,
            "repeatability_region": repeat_region,
        }
    failure = "R-REFERENCE-UNSTABLE" if unstable else "uncertainty_unresolved" if unresolved else None
    return {
        "status": "pass" if failure is None and not epoch_shift else "failed_branch",
        "failure_branch": failure,
        "reference_epoch_shift": epoch_shift,
        "failed_states": failed_states,
        "states": states,
    }, states


def _analyze_strip(
    current: Mapping[str, Mapping[str, Sequence[Mapping[str, float]]]],
    *, policy: HsiPolicyV2, feature_ids: Sequence[str], seed: int,
    monte_carlo_samples: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    output: dict[str, Any] = {}
    components: dict[str, Any] = {}
    unresolved = False
    high_classes: list[str] = []
    failed_commands: list[dict[str, Any]] = []
    for class_index, class_name in enumerate(REPEATABILITY_CLASSES):
        groups: dict[str, Sequence[Mapping[str, float]]] = {}
        command_reports: dict[str, Any] = {}
        centers = []
        for command_key in CLASS_COMMANDS[class_name]:
            for block, rows in current[command_key].items():
                groups[f"{command_key}:{block}"] = rows
                centers.extend(rows)
            command_summary = summarize_within_groups(current[command_key], feature_ids)
            a_rows = current[command_key]["A"]
            b_rows = current[command_key]["B"]
            a = command_summary["group_centers"]["A"]
            b = command_summary["group_centers"]["B"]
            variance = command_summary["diagonal_variance"]
            shift_region = calibrate_direct_limits(
                a,
                2.0 * np.asarray(variance, dtype=float) / len(a_rows),
                seed=seed + 500 + class_index * 10 + len(command_reports),
                samples=monte_carlo_samples,
            )
            shift = evaluate_reference_difference(
                a, b,
                left_variance=variance, left_count=len(a_rows),
                right_variance=variance, right_count=len(b_rows),
                feature_ids=feature_ids,
                guarded_limit=shift_region["guarded_limit"],
                unguarded_limit=shift_region["unguarded_limit"],
                statistic="strip_command_block_stability",
            )
            command_reports[command_key] = {
                "within_command": command_summary,
                "block_center_shift": shift,
                "block_center_shift_region": shift_region,
            }
            if command_summary["status"] != "pass" or shift["decision"] != "pass":
                unresolved = True
                failed_commands.append({
                    "class": class_name,
                    "command": command_key,
                    "audit_status": command_summary["status"],
                    "block_center_shift": shift["decision"],
                    "failures": command_summary["audit"]["failure_branches"],
                })
        summary = summarize_within_groups(groups, feature_ids)
        unresolved |= summary["status"] != "pass"
        class_policy = policy.artifact["repeatability_policy"]["classes"][class_name]
        variance = conservative_class_variance(
            class_policy["p1_floor_diagonal_variance"],
            summary["diagonal_variance"], feature_ids,
        )
        floor = conservative_class_variance(
            class_policy["p1_floor_diagonal_variance"], None, feature_ids,
        )
        ratio = float(np.max(variance / floor))
        if ratio > HIGH_VARIANCE_RATIO:
            high_classes.append(class_name)
        center = np.mean(np.vstack([ordered_unit_shape(row, feature_ids) for row in centers]), axis=0)
        limits = {
            str(count): calibrate_confirmation_group_limit(
                center, variance, count=count,
                seed=seed + 200 + class_index * 10 + count,
                samples=monte_carlo_samples,
            ) for count in (3, 5)
        }
        output[class_name] = {
            "summary": summary,
            "p1_floor_max_plane_ratio": ratio,
            "above_p1_floor_threshold": ratio > HIGH_VARIANCE_RATIO,
            "limits": limits,
            "commands": command_reports,
        }
        components[class_name] = {
            "targeted_variance": summary["diagonal_variance"],
            "conservative_variance": variance.tolist(),
            "limits": limits,
            "audit": summary["audit"],
            "center": center.tolist(),
        }
    return {
        "status": "uncertainty_unresolved" if unresolved else "pass",
        "failure_branch": "uncertainty_unresolved" if unresolved else None,
        "classes_above_p1_floor": high_classes,
        "failed_commands": failed_commands,
        "high_variance_ratio_threshold": HIGH_VARIANCE_RATIO,
        "classes": output,
    }, components


def _build_candidate(
    policy: HsiPolicyV2, manifold: RayHsiManifold,
    *, reference_states: Mapping[str, Any], class_components: Mapping[str, Any],
    seed: int, monte_carlo_samples: int, bootstrap_replicates: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    artifact = copy.deepcopy(policy.artifact)
    artifact["status"] = "calibrated_waiting_for_planner"
    artifact["formal_capture_eligible"] = False
    artifact["reference_policy"]["status"] = "calibrated_waiting_for_planner"
    artifact["reference_policy"]["states"] = copy.deepcopy(dict(reference_states))
    artifact["reference_policy"]["audit_thresholds"] = dict(AUDIT_THRESHOLDS)
    for class_name, component in class_components.items():
        target = artifact["repeatability_policy"]["classes"][class_name]
        target["status"] = "calibrated_waiting_for_planner"
        target["targeted_variance"] = component["targeted_variance"]
        target["limits"] = component["limits"]
        target["audit"] = component["audit"]
    artifact["repeatability_policy"]["status"] = "calibrated_waiting_for_planner"
    artifact["repeatability_policy"]["audit_thresholds"] = dict(AUDIT_THRESHOLDS)

    region_specs = (
        ("sat0_exact_node", "neutral_fullscale", 0.0, 0.0, "exact_node"),
        ("sat0_exact_node", "neutral_scale_relaxed", 0.0, 0.0, "exact_node"),
        ("nonzero_exact_node", "mid_sat_fullscale", 120.0, 50.0, "exact_node"),
        ("nonzero_exact_node", "sat100_fullscale", 120.0, 100.0, "exact_node"),
        ("nonzero_regular", "mid_sat_fullscale", 150.0, 35.0, "regular"),
        ("nonzero_regular", "sat100_fullscale", 150.0, 100.0, "regular"),
        ("nonzero_high_curvature", "mid_sat_fullscale", 345.0, 50.0, "high_curvature"),
        ("nonzero_high_curvature", "sat100_fullscale", 345.0, 100.0, "high_curvature"),
    )
    coordinate_limits: dict[str, Any] = {}
    observer_limits: dict[str, Any] = {}
    reports: dict[str, Any] = {}
    failures = []
    ray_variance = np.asarray(artifact["match_components"]["ray_repeatability_diagonal_variance"], dtype=float)
    for offset, (kind, class_name, hue, sat, interpolation_name) in enumerate(region_specs):
        interpolation = np.asarray(
            artifact["match_components"]["interpolation"][interpolation_name]["diagonal_variance"],
            dtype=float,
        )
        strip_variance = np.asarray(class_components[class_name]["conservative_variance"], dtype=float)
        report = calibrate_joint_regions(
            manifold, target_hue=hue, target_sat=sat,
            diagonal_variance=ray_variance + strip_variance + interpolation,
            seed=seed + 1000 + offset,
            samples=monte_carlo_samples,
            bootstrap_replicates=bootstrap_replicates,
        )
        key = f"{kind}:{class_name}"
        reports[key] = report
        if report["status"] != "pass":
            failures.append(key)
            continue
        coordinate_limits[key] = {
            "component_scales": report["component_scales"],
            "guarded_limit": report["coordinate_region"]["guarded_limit"],
            "unguarded_limit": report["coordinate_region"]["unguarded_limit"],
        }
        observer_limits[key] = {
            "guarded_limit": report["observer_region"]["guarded_limit"],
            "unguarded_limit": report["observer_region"]["unguarded_limit"],
        }
    artifact["coordinate_policy"]["formal_limits"] = coordinate_limits
    artifact["coordinate_policy"]["monte_carlo_samples"] = monte_carlo_samples
    artifact["coordinate_policy"]["bootstrap_replicates"] = bootstrap_replicates
    artifact["observer_policy"]["formal_limits"] = observer_limits
    artifact["synthetic_joint_coverage"] = reports
    artifact["planner_freeze_required"] = True
    return artifact, {
        "status": "pass" if not failures else "uncertainty_unresolved",
        "failure_branch": None if not failures else "uncertainty_unresolved",
        "failed_regions": failures,
        "seed": seed,
        "sample_count_per_region": monte_carlo_samples,
        "bootstrap_replicates_per_region": bootstrap_replicates,
        "regions": reports,
    }


def _group_ray(captures: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, list[dict[str, float]]]]:
    output: dict[str, dict[str, list[dict[str, float]]]] = defaultdict(lambda: defaultdict(list))
    for record in captures:
        if record["source"] != "ray":
            continue
        step = record["plan_step"]
        state = step["state"]
        output[f"h{int(state['hue'])}-s{int(state['sat'])}"][str(step["block"])].append(record["feature_values"])
    return {key: dict(value) for key, value in output.items()}


def _group_strip(captures: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, list[dict[str, float]]]]:
    output: dict[str, dict[str, list[dict[str, float]]]] = defaultdict(lambda: defaultdict(list))
    for record in captures:
        if record["source"] == "strip":
            step = record["plan_step"]
            output[str(step["command_key"])][str(step["block"])].append(record["feature_values"])
    return {key: dict(value) for key, value in output.items()}


def _audit_capture_contract(
    captures: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    commands: Sequence[Mapping[str, Any]],
    feature_ids: Sequence[str],
    *, run: Mapping[str, Any], physical_contract: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    planned = plan.get("captures")
    if not isinstance(planned, list) or len(planned) != 82:
        raise ValueError("P7-R1 frozen plan must contain exactly 82 captures")
    planned_by_id = {str(item.get("capture_id")): item for item in planned}
    if len(planned_by_id) != len(planned):
        raise ValueError("P7-R1 frozen plan contains duplicate capture ids")
    curve = _load_json(Path(plan["inputs"]["code_duty_curve"]["path"]))
    attempts_by_logical: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        attempts_by_logical[str(attempt.get("logical_capture_id"))].append(attempt)
    commands_by_attempt: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for command in commands:
        commands_by_attempt[str(command.get("capture_id"))].append(command)
    recomputed_physical = 0
    recomputed_base_physical = 0
    recomputed_auto = 0
    recomputed_weak_physical = 0
    weak_attempt_count = 0
    auto_cache_misses = 0
    for record in captures:
        logical_id = str(record.get("capture_id"))
        step = planned_by_id.get(logical_id)
        if step is None or record.get("plan_step") != step:
            raise ValueError(f"P7-R1 logical capture {logical_id} differs from frozen plan")
        source = record.get("source")
        if source != step.get("source"):
            raise ValueError(f"P7-R1 logical capture {logical_id} source differs from frozen plan")
        if source not in {"ambient", "ray", "strip"}:
            raise ValueError("P7-R1 capture has invalid source")
        if source != "ambient":
            features = record.get("feature_values")
            if not isinstance(features, Mapping) or set(features) != set(feature_ids):
                raise ValueError("P7-R1 formal capture lacks the exact 58-feature set")
            if record.get("readback") is None:
                raise ValueError("P7-R1 formal capture lacks source readback evidence")
        logical_attempts = attempts_by_logical.get(logical_id, [])
        expected_ids = record.get("attempt_capture_ids")
        if not isinstance(expected_ids, list) or [item.get("attempt_capture_id") for item in logical_attempts] != expected_ids:
            raise ValueError(f"P7-R1 logical capture {logical_id} attempt provenance mismatch")
        if len(logical_attempts) not in {1, 2} or logical_attempts[0].get("attempt_kind") != "base":
            raise ValueError(f"P7-R1 logical capture {logical_id} has invalid base/reacquire attempts")
        selected = [item for item in logical_attempts if item.get("selected_for_formal") is True]
        if len(selected) != 1 or selected[0].get("attempt_capture_id") != record.get("selected_attempt_capture_id"):
            raise ValueError(f"P7-R1 logical capture {logical_id} selected attempt mismatch")
        if len(logical_attempts) == 2:
            if source == "ambient" or logical_attempts[1].get("attempt_kind") != "weak_signal_reacquire":
                raise ValueError(f"P7-R1 logical capture {logical_id} has invalid reacquire provenance")
            if not isinstance(logical_attempts[0].get("quality_rejection"), Mapping):
                raise ValueError(f"P7-R1 logical capture {logical_id} lost base rejection evidence")
        for attempt in logical_attempts:
            attempt_id = str(attempt.get("attempt_capture_id"))
            if attempt.get("source") != source:
                raise ValueError(f"P7-R1 attempt {attempt_id} source drift")
            physical = recompute_physical_count(attempt)
            capture = attempt.get("capture") or {}
            if int(capture.get("physical_capture_count", physical)) != physical:
                raise ValueError(f"P7-R1 attempt {attempt_id} physical count payload mismatch")
            if attempt.get("auto_exposure_audit") != capture.get("auto_exposure_audit"):
                raise ValueError(f"P7-R1 attempt {attempt_id} auto-exposure audit payload mismatch")
            raw = (capture.get("capture") or {}).get("saved_file")
            if not raw or not Path(raw).is_file() or Path(raw).stat().st_size <= 0:
                raise ValueError(f"P7-R1 attempt {attempt_id} lacks a retained nonempty CR3")
            report = _load_json(Path(capture["patch_statistics"]))
            exposure = report.get("exposure_metadata") or report.get("recorded_exposure") or report.get("exposure") or {}
            if exposure.get("status") != "recorded":
                raise ValueError(f"P7-R1 attempt {attempt_id} lacks recorded exposure provenance")
            events = commands_by_attempt.get(attempt_id, [])
            on = validate_attempt_event_grammar(
                events, source=str(source), plan_step=step, curve=curve,
                attempt_kind=str(attempt.get("attempt_kind")),
            )
            if source != "ambient":
                retained = on.get("readback") if source == "ray" else on.get("response")
                if retained != attempt.get("readback"):
                    raise ValueError(f"P7-R1 attempt {attempt_id} readback mismatch")
            recomputed_physical += physical
            if attempt.get("attempt_kind") == "base":
                recomputed_base_physical += physical
            if attempt.get("auto_exposure"):
                recomputed_auto += physical
                auto_cache_misses += 1
            if attempt.get("attempt_kind") == "weak_signal_reacquire":
                recomputed_weak_physical += physical
                weak_attempt_count += 1
        selected_capture = selected[0].get("capture")
        if record.get("capture") != selected_capture or record.get("readback") != selected[0].get("readback"):
            raise ValueError(f"P7-R1 logical capture {logical_id} does not retain its selected attempt")
        if source != "ambient":
            report = _load_json(Path(selected_capture["patch_statistics"]))
            try:
                recomputed_features = required_hsi_features_from_report(report, feature_ids)
            except HsiRejectedFeaturesError as exc:
                raise ValueError(f"P7-R1 logical capture {logical_id} selected attempt fails feature quality") from exc
            if record.get("feature_values") != recomputed_features:
                raise ValueError(f"P7-R1 logical capture {logical_id} feature provenance mismatch")
        if len(logical_attempts) == 2:
            rejection = logical_attempts[0].get("quality_rejection")
            if not isinstance(rejection, Mapping) or rejection.get("weak_signal_only") is not True:
                raise ValueError(f"P7-R1 logical capture {logical_id} base rejection is not weak-only")
            if selected[0].get("attempt_kind") != "weak_signal_reacquire" or selected[0].get("quality_rejection") is not None:
                raise ValueError(f"P7-R1 logical capture {logical_id} selected invalid weak reacquire")
        elif selected[0].get("quality_rejection") is not None:
            raise ValueError(f"P7-R1 logical capture {logical_id} selected rejected base")
    if set(attempts_by_logical) != {str(item["capture_id"]) for item in captures}:
        raise ValueError("P7-R1 attempt evidence contains unknown logical capture ids")
    maximum_total = int(physical_contract["maximum_total_physical_cr3"])
    maximum_weak = int(physical_contract["maximum_weak_signal_reacquire_cr3"])
    maximum_misses = int(physical_contract["unique_autoexposure_cache_misses"])
    counters = {
        "physical_cr3_count": recomputed_physical,
        "base_physical_cr3_count": recomputed_base_physical,
        "auto_exposure_physical_cr3_count": recomputed_auto,
        "auto_exposure_cache_miss_count": auto_cache_misses,
        "weak_signal_reacquire_count": weak_attempt_count,
        "weak_signal_reacquire_physical_cr3_count": recomputed_weak_physical,
    }
    expected_logical = len(planned)
    expected_formal = sum(bool(item.get("formal_measurement")) for item in planned)
    logical_counters = {
        "logical_captures_completed": expected_logical,
        "formal_captures_completed": expected_formal,
    }
    for key, value in logical_counters.items():
        if int(run.get(key, -1)) != value:
            raise ValueError(f"P7-R1 run counter mismatch for {key}")
    for key, value in counters.items():
        if int(run.get(key, -1)) != value:
            raise ValueError(f"P7-R1 run counter mismatch for {key}")
    maximum_auto = int(physical_contract["maximum_autoexposure_physical_cr3"])
    maximum_per_auto = int(physical_contract["maximum_physical_per_cache_miss"])
    if recomputed_physical > maximum_total or recomputed_weak_physical > maximum_weak or auto_cache_misses > maximum_misses or recomputed_auto > maximum_auto:
        raise ValueError("P7-R1 retained evidence exceeds frozen physical limits")
    if any(recompute_physical_count(item) > maximum_per_auto for item in attempts if item.get("auto_exposure")):
        raise ValueError("P7-R1 retained auto-exposure attempt exceeds per-cache-miss cap")
    if set(commands_by_attempt) != {str(item.get("attempt_capture_id")) for item in attempts}:
        raise ValueError("P7-R1 command evidence contains orphan attempt ids")
    return {
        "logical_count": len(captures),
        "formal_ray_count": sum(item["source"] == "ray" for item in captures),
        "formal_strip_count": sum(item["source"] == "strip" for item in captures),
        "ambient_count": sum(item["source"] == "ambient" for item in captures),
        **counters,
        **logical_counters,
        "maximum_total_physical_cr3": maximum_total,
        "physical_cap_status": str(physical_contract.get("absolute_cap_status")),
        "recorded_exposure_required": True,
        "source_isolation_and_readback": "pass",
        "commands_jsonl_audited": True,
        "attempt_evidence_recomputed": True,
        "retained_npy_count": 0,
    }


def _cleanup_ok(path: Path) -> bool:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, Mapping) and isinstance(value.get("steps"), list):
        return bool(value["steps"]) and all(bool(item.get("ok")) for item in value["steps"])
    if isinstance(value, list):
        return bool(value) and all(bool(item.get("ok")) for item in value)
    if isinstance(value, Mapping):
        return bool(value.get("ok") or value.get("status") in {"pass", "complete", "all_off"})
    return False


def _verify_input_hashes(inputs: Mapping[str, Any]) -> None:
    for reference in inputs.values():
        path = Path(reference["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
            raise ValueError(f"P7-R1 analyzer input hash drift for {path}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze/finalize a completed P7-R1 run into a formal-ineligible candidate.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--policy-version", choices=("v2",), required=True)
    parser.add_argument("--monte-carlo-samples", type=int, default=DEFAULT_MC_SAMPLES)
    parser.add_argument("--bootstrap-replicates", type=int, default=DEFAULT_BOOTSTRAP_REPLICATES)
    parser.add_argument("--seed", type=int, default=DEFAULT_MC_SEED)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report, candidate = finalize_reference_repeatability_run(
        args.run_dir,
        monte_carlo_samples=args.monte_carlo_samples,
        bootstrap_replicates=args.bootstrap_replicates,
        seed=args.seed,
    )
    print(report)
    print(candidate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
