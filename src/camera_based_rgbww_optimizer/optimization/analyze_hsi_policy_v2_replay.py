from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    DEFAULT_WAITING_OUTPUT,
    HsiPolicyV2,
    calibrate_component_scales,
    calibrate_confirmation_group_limit,
    calibrate_direct_limits,
    calibrate_joint_regions,
    evaluate_confirmation_spread,
    local_tangent_evaluate,
    ordered_unit_shape,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization.analyze_strip_hsi_pilot import analyze_strip_hsi_pilot
from camera_based_rgbww_optimizer.optimization.hsi_objective import required_hsi_features_from_report
from camera_based_rgbww_optimizer.optimization.hsi_budget import HsiSolverBudgetLimits
from camera_based_rgbww_optimizer.optimization.hsi_feedback import run_hsi_feedback_multiseed
from camera_based_rgbww_optimizer.optimization.measure_hsi_reference_repeatability import DEFAULT_SENTINEL_RUN


CHANNELS = ("cw", "ww", "r", "g", "b")


def analyze_v2_replay(
    run_dir: str | Path = DEFAULT_SENTINEL_RUN,
    *, policy_path: str | Path = DEFAULT_WAITING_OUTPUT,
    synthetic_samples: int = 5000,
) -> dict[str, Any]:
    root = Path(run_dir)
    policy = HsiPolicyV2.load(policy_path)
    manifold = RayHsiManifold.load()
    feature_ids = manifold.coordinate_feature_ids
    captures = _load_jsonl(root / "captures.jsonl")
    capture_reports = {
        str(item["capture_id"]): Path(item["capture"]["patch_statistics"])
        for item in captures
    }
    rows = _load_jsonl(root / "target-results.jsonl")
    v1 = analyze_strip_hsi_pilot(root, policy_version="v1")
    v1_bytes = (json.dumps(v1, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    existing_v1 = root / "analysis.json"
    v1_replay = {
        "policy_version": "v1",
        "recomputed_sha256": hashlib.sha256(v1_bytes).hexdigest(),
        "existing_analysis_sha256": _sha256(existing_v1),
        "byte_identical": existing_v1.read_bytes() == v1_bytes,
        "faithful_point_count": v1["faithful_point_count"],
        "formal_gate6_eligibility": False,
    }
    components = policy.artifact["match_components"]
    ray = np.asarray(components["ray_repeatability_diagonal_variance"], dtype=float)
    floor = np.asarray(
        policy.artifact["repeatability_policy"]["classes"]["neutral_fullscale"]["p1_floor_diagonal_variance"],
        dtype=float,
    )
    match = ray + floor
    anchor_replay = []
    for anchor in _load_jsonl(root / "reference-anchors.jsonl"):
        target = anchor["target"]
        features = _features(capture_reports[anchor["capture_id"]], feature_ids)
        target_features = manifold.target_at(target["hue"], target["sat"]).features
        direct_l2 = float(np.linalg.norm(
            ordered_unit_shape(features, feature_ids) - ordered_unit_shape(target_features, feature_ids)
        ))
        local = local_tangent_evaluate(
            manifold, features, target_hue=target["hue"], target_sat=target["sat"],
            diagonal_variance=match,
        )
        anchor_replay.append({
            "capture_id": anchor["capture_id"], "position": anchor["position"],
            "target": target, "direct_l2_to_frozen_exact_center": direct_l2,
            "local_tangent": _compact_local(local),
            "reference_center_compatibility": "not_calibrated_until_P7_R1",
            "reference_repeatability": "single_frame_invalid_under_v2",
        })
    point_replay = []
    for row in rows:
        target = row["target"]
        hue, sat = int(target["hue"]), int(target["sat"])
        class_name = _repeatability_class(sat=sat, max_code=int(target["max_code"]))
        final = row.get("final_verification", [])
        samples = [_features(capture_reports[item["capture_id"]], feature_ids) for item in final]
        spread = evaluate_confirmation_spread(
            samples, feature_ids=feature_ids, class_name=class_name,
            class_variance=floor, limit=None,
        )
        trace = _trace_replay(
            row, capture_reports=capture_reports, manifold=manifold,
            feature_ids=feature_ids, match_variance=match,
        )
        state_machine_replay = _multiseed_trace_replay(
            row, capture_reports=capture_reports, manifold=manifold,
            feature_ids=feature_ids, match_variance=match,
            synthetic_samples=max(1000, synthetic_samples),
        )
        point = {
            "target": {"hue": hue, "sat": sat, "max_code": int(target["max_code"])},
            "repeatability_class": class_name,
            "confirmation_spread": spread,
            "final_local_tangent": [
                _compact_local(local_tangent_evaluate(
                    manifold, values, target_hue=hue, target_sat=sat,
                    diagonal_variance=match,
                )) for values in samples
            ],
            "basis_seed_faces": [
                {"active_channel": item["active_channel"], "command": item["command"],
                 "predicted_relative_rmse": item["predicted_relative_rmse"]}
                for item in target["seed"]["candidates"]
            ],
            "recorded_trace_replay": trace,
            "proposed_multiseed_state_machine_replay": state_machine_replay,
            "hsi_coordinate_equivalent": "not_formally_evaluated_waiting_for_P7_R1",
            "observer_equivalent": "not_formally_evaluated_waiting_for_P7_R1",
            "color_rendering_residual_retained": True,
            "gate6_eligibility": False,
        }
        point_replay.append(point)
        for diagnostic in row.get("scale_relaxed_diagnostics", []):
            if int(diagnostic.get("max_code", 0)) != 3072 or not diagnostic.get("final_verification"):
                continue
            diagnostic_samples = [
                _features(capture_reports[item["capture_id"]], feature_ids)
                for item in diagnostic["final_verification"]
            ]
            point_replay.append({
                "target": {"hue": hue, "sat": sat, "max_code": 3072},
                "repeatability_class": "neutral_scale_relaxed",
                "confirmation_spread": evaluate_confirmation_spread(
                    diagnostic_samples, feature_ids=feature_ids,
                    class_name="neutral_scale_relaxed", class_variance=floor, limit=None,
                ),
                "hsi_coordinate_equivalent": "not_formally_evaluated_waiting_for_P7_R1",
                "observer_equivalent": "not_formally_evaluated_waiting_for_P7_R1",
                "color_rendering_residual_retained": True,
                "gate6_eligibility": False,
            })
    synthetic = _synthetic_coverage(manifold, match, samples=synthetic_samples)
    return {
        "schema_version": 2,
        "analysis": "p7_r0_hsi_policy_v2_offline_replay",
        "status": "ready_for_planner_review",
        "authorization": "offline_only",
        "inputs": {
            "run_json": _reference(root / "run.json"),
            "plan_json": _reference(root / "plan.json"),
            "target_results": _reference(root / "target-results.jsonl"),
            "policy_v2_waiting": _reference(Path(policy_path)),
        },
        "v1_replay": v1_replay,
        "v2_synthetic_coverage": synthetic,
        "reference_anchor_replay": anchor_replay,
        "old_sentinel_holdout_replay": point_replay,
        "solver_architecture": {
            "directional_residual": True,
            "finite_multiseed": True,
            "prediction_error_rebase": True,
            "proposed_max_distinct_face_starts": 2,
            "proposed_rounds_per_start": 8,
            "proposed_rebases_per_start": 2,
            "proposed_confirmations": 3,
            "ordinary_hard_caps": {"logical_observations": 54, "physical_cr3": 67},
            "n5_hard_caps": {"logical_observations": 62, "physical_cr3": 75},
            "budget_formula": "2 * (1 initial + 4 probes + 8 feedback attempts + 2*4 rebase probes + 2 confirmation groups)",
            "planner_freeze_required_before_capture": True,
        },
        "device_calls_performed": False,
        "formal_acceptance_calibration_from_sentinel": False,
        "locked": ["P7-R1 execute", "new sentinel", "remaining 9", "boundary", "holdout", "P8"],
    }


def _trace_replay(
    row: Mapping[str, Any], *, capture_reports: Mapping[str, Path],
    manifold: RayHsiManifold, feature_ids: Sequence[str], match_variance: Sequence[float],
) -> dict[str, Any]:
    target = row["target"]
    trace = []
    commands = []
    outputs = []
    for sample in row["feedback"]["samples"]:
        capture_id = sample.get("observation", {}).get("capture_id")
        if capture_id not in capture_reports:
            continue
        values = _features(capture_reports[capture_id], feature_ids)
        local = local_tangent_evaluate(
            manifold, values, target_hue=target["hue"], target_sat=target["sat"],
            diagonal_variance=match_variance,
        )
        vector = _local_vector(local)
        command = np.asarray([sample["command"][channel] / int(target["max_code"]) for channel in CHANNELS])
        prediction = None
        if len(commands) >= 6:
            design = np.column_stack((np.ones(len(commands)), np.vstack(commands)))
            coefficients, *_ = np.linalg.lstsq(design, np.vstack(outputs), rcond=None)
            prediction = np.r_[1.0, command] @ coefficients
        record = {
            "sample_index": sample["index"], "phase": sample["phase"],
            "command": sample["command"], "local": _compact_local(local),
            "predicted_directional_residual": None if prediction is None else prediction.tolist(),
            "actual_directional_residual": vector.tolist(),
            "prediction_error_l2": None if prediction is None else float(np.linalg.norm(vector - prediction)),
        }
        trace.append(record)
        commands.append(command)
        outputs.append(vector)
    finite_errors = [item["prediction_error_l2"] for item in trace if item["prediction_error_l2"] is not None]
    return {
        "steps": trace,
        "prediction_error_max": max(finite_errors) if finite_errors else None,
        "rebase_candidate_count": sum(value > 2.0 for value in finite_errors),
        "recorded_rebases": row["feedback"].get("thermal_rebases", []),
    }


def _multiseed_trace_replay(
    row: Mapping[str, Any], *, capture_reports: Mapping[str, Path],
    manifold: RayHsiManifold, feature_ids: Sequence[str],
    match_variance: Sequence[float], synthetic_samples: int,
) -> dict[str, Any]:
    target = row["target"]
    calibration = calibrate_joint_regions(
        manifold,
        target_hue=float(target["hue"]), target_sat=float(target["sat"]),
        diagonal_variance=match_variance,
        seed=27072026 + int(target["hue"]) + int(target["sat"]),
        samples=synthetic_samples,
        bootstrap_replicates=100,
    )
    if calibration["status"] != "pass":
        return {
            "status": "uncertainty_unresolved",
            "reason": calibration.get("failure_branch"),
            "state_machine_driven": False,
        }
    scales = np.asarray(calibration["component_scales"], dtype=float)
    guarded = float(calibration["coordinate_region"]["guarded_limit"])
    covariance = np.asarray(match_variance, dtype=float)
    observations: dict[tuple[int, ...], list[dict[str, Any]]] = {}
    for sample in row["feedback"]["samples"]:
        capture_id = sample.get("observation", {}).get("capture_id")
        if capture_id not in capture_reports:
            continue
        values = _features(capture_reports[capture_id], feature_ids)
        local = local_tangent_evaluate(
            manifold, values,
            target_hue=float(target["hue"]), target_sat=float(target["sat"]),
            diagonal_variance=match_variance,
        )
        if local["status"] != "evaluated":
            continue
        coordinate = np.asarray(_coordinate_vector(local), dtype=float) / scales
        rendering = np.asarray(local["directional_orthogonal_residual"], dtype=float) / np.sqrt(covariance)
        score = float(np.linalg.norm(coordinate))
        command_key = tuple(int(sample["command"][channel]) for channel in CHANNELS)
        observations.setdefault(command_key, []).append({
            "residuals": {"coordinate": coordinate.tolist(), "rendering": rendering.tolist()},
            "objective": {
                "kind": "ray_hsi_policy_v2_lexicographic",
                "feasible": score <= guarded,
                "hue_defined": float(target["sat"]) > 0.0,
                "hue_error_degrees": local.get("hue_error_degrees"),
                "sat_error_percent": float(local["sat_error_percent"]),
                "coordinate_guarded_limit": guarded,
                "coordinate_guarded_excess": max(score / guarded - 1.0, 0.0),
                "color_rendering_residual": local["color_rendering_residual"],
                "command_continuity_l1": 0.0,
            },
        })
    cursors: dict[tuple[int, ...], int] = defaultdict(int)
    missing: list[dict[str, Any]] = []

    def capture(command, *, phase, settled_confirmation):
        key = tuple(int(command[channel]) for channel in CHANNELS)
        choices = observations.get(key)
        if not choices:
            missing.append({"phase": phase, "command": dict(command), "settled_confirmation": settled_confirmation})
            return {
                "measurement_rejected": True,
                "rejection_evidence": {"status": "trace_support_missing", "phase": phase},
            }
        index = min(cursors[key], len(choices) - 1)
        cursors[key] += 1
        return choices[index]

    seeds = sorted(
        row["target"]["seed"]["candidates"],
        key=lambda item: float(item["predicted_relative_rmse"]),
    )[:2]
    limits = HsiSolverBudgetLimits(confirmations_per_group=3)
    result = run_hsi_feedback_multiseed(
        seeds=seeds,
        capture_observation_fn=capture,
        max_starts=2,
        rounds_per_start=8,
        budget_limits=limits,
        max_code=int(target["max_code"]),
        group_order=("coordinate", "rendering"),
    )
    return {
        "status": "trace_support_missing" if missing else result["status"],
        "state_machine_driven": True,
        "interpolation_of_missing_commands": False,
        "trace_support_missing": missing,
        "budget_declaration": result["budget_declaration"],
        "logical_observations_used": result["logical_observations_used"],
        "attempt_count": result["attempt_count"],
        "selected_start_index": result["selected_start_index"],
        "prediction_error_space": "v2_guarded_coordinate_and_whitened_rendering",
        "attempts": result["attempts"],
    }


def _synthetic_coverage(manifold: RayHsiManifold, variance: Sequence[float], *, samples: int) -> dict[str, Any]:
    output = {}
    for hue, sat in ((0, 0), (120, 50), (120, 100), (300, 100)):
        target = manifold.target_at(hue, sat)
        center = ordered_unit_shape(target.features, manifold.coordinate_feature_ids)
        direct = calibrate_direct_limits(center, variance, seed=27072026 + hue + sat, samples=samples)
        rng = np.random.default_rng(27072026 + hue + sat)
        coordinate_outputs = []
        for noise in rng.normal(0.0, np.sqrt(variance), size=(max(1000, samples // 5), len(center))):
            candidate = center + noise
            local = local_tangent_evaluate(
                manifold, dict(zip(manifold.coordinate_feature_ids, candidate, strict=True)),
                target_hue=hue, target_sat=sat, diagonal_variance=variance,
            )
            if local["status"] == "evaluated":
                coordinate_outputs.append(_coordinate_vector(local))
        scales = calibrate_component_scales(coordinate_outputs)
        repeat3 = calibrate_confirmation_group_limit(center, variance, count=3, samples=samples)
        repeat5 = calibrate_confirmation_group_limit(center, variance, count=5, samples=samples)
        output[f"h{hue}-s{sat}"] = {
            "direct_region": direct, "coordinate_component_scales": scales,
            "zero_scale": False, "condition": local.get("condition_number"),
            "repeat_group_limits": {"3": repeat3, "5": repeat5},
        }
    return {"status": "pass_synthetic_only_not_formal_limits", "targets": output}


def _features(report_path: Path, feature_ids: Sequence[str]) -> dict[str, float]:
    return required_hsi_features_from_report(_load_json(report_path), feature_ids)


def _coordinate_vector(local: Mapping[str, Any]) -> list[float]:
    return ([float(local["hue_error_degrees"])] if local.get("hue_defined") else []) + [float(local["sat_error_percent"])]


def _local_vector(local: Mapping[str, Any]) -> np.ndarray:
    if local.get("status") != "evaluated":
        return np.asarray([1e12])
    return np.r_[_coordinate_vector(local), np.asarray(local["directional_orthogonal_residual"], dtype=float)]


def _compact_local(local: Mapping[str, Any]) -> dict[str, Any]:
    return {key: local.get(key) for key in (
        "status", "hue_defined", "hue_error_degrees", "sat_error_percent",
        "condition_number", "observer_whitened_score", "color_rendering_residual",
    ) if key in local}


def _repeatability_class(*, sat: int, max_code: int) -> str:
    if max_code != 4095:
        return "neutral_scale_relaxed"
    if sat == 0:
        return "neutral_fullscale"
    if sat == 100:
        return "sat100_fullscale"
    return "mid_sat_fullscale"


def _reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": _sha256(path)}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay P7 sentinel under the offline-only HSI policy v2 architecture.")
    parser.add_argument("run_dir", type=Path, nargs="?", default=DEFAULT_SENTINEL_RUN)
    parser.add_argument("--policy-v2", type=Path, default=DEFAULT_WAITING_OUTPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--synthetic-samples", type=int, default=5000)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    value = analyze_v2_replay(args.run_dir, policy_path=args.policy_v2, synthetic_samples=args.synthetic_samples)
    output = args.output or args.run_dir / "p7-r0-v2-replay.json"
    output.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
