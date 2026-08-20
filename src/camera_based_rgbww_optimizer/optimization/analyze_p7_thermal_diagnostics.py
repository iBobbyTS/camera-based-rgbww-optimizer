from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    calibrate_direct_limits,
    direct_whitened_norm,
    ordered_unit_shape,
)
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import (
    DEFAULT_P6_RUN,
    QUANTILE_METHOD,
    load_ray_repeat_groups,
)
from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
    parse_nominal_exposure,
    validate_recorded_exposure_setting,
)
from camera_based_rgbww_optimizer.measurement import raw_response_candidate
from camera_based_rgbww_optimizer.optimization import analyze_raw_observer_validation
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.control import esphome
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.analyze_hsi_reference_repeatability import (
    write_reference_epoch_v2_derived,
)


POST_FIX_REVALIDATION_SCHEMA = "p7_direct_ray_r6_post_fix_revalidation_v1"
LEGACY_EXPOSURE_FAILURE_MESSAGE = (
    "direct Ray R6 recorded exposure differs from frozen shutter"
)
POST_FIX_REVALIDATION_FILE = "post-fix-revalidation.json"
R6_VECTOR_REANALYSIS_SCHEMA = "p7_ray_r6_vector_reanalysis_v1"
POST_FIX_ORIGINAL_FILES = (
    "experiment-spec.json", "input-checkpoint.json", "run.json",
    "failure.json", "wrapper-result.json", "all-off-python.json",
    "all-off-shell.json", "all-off-shell.exit-status.txt",
)
TD_C_CORE_CONTRAST_SCHEMA = "guide5_td_c_core_contrasts_v2_1"
TD_C_CORE_CONTRAST_CLASSIFICATION = (
    "stable_order_invariant_nonzero_warm_A_cross_source_offset_established"
)
TD_C_CORE_CONTRAST_MC_SEED = 27072026
TD_C_CORE_CONTRAST_MC_SAMPLES = 20000
GUIDE6_SEED_NEGATIVE_SCHEMA = "guide6_h120_s100_seed_evidence_disposition_v3"
GUIDE6_SEED_COMMAND_HASH = "f70a07889065ad105bf25a9fda103ec2a708ef056f4ae17b0279ef3886b5cfde"
GUIDE6_SEED_COMMAND = {"cw": 518, "ww": 0, "r": 0, "g": 4095, "b": 0}
GUIDE6_SEED_LEGACY_ANALYSIS_SHA256 = (
    "c32dc70b5639ff0342dbef0c8dc2151d1bb1469fa717b3b17f9e032d57b5dd1b",
    "9651f2f3d706d2dd7b950737a58b93d71a947a841b1da44cda1b3b94261a0f87",
)
GUIDE6_SEED_TARGET_SCORES = (80.28514565625028, 80.8620601083101)
GUIDE8_ANALYSIS_SCHEMA = "guide8_ray_h120_s100_emission_exposure_analysis_v1"
TD_C_CORE_EXPECTED_SCORES = {
    "ray_pair_maximum": 4.7728227800,
    "strip_pair_maximum": 5.3379311421,
    "paired_offset_pair_maximum": 5.7765306838,
    "source_order": 3.2538875744,
}
TD_C_CORE_EXPECTED_SCORE_ABS_TOLERANCE = 5e-10
TD_C_ENDPOINT_SCHEMA = "guide5_td_c_fast_endpoint_holdout_analysis_v1"
TD_C_ENDPOINT_DECOMPOSITION_SCHEMA = "guide5_td_c_fast_endpoint_residual_decomposition_v1"
TD_C_ENDPOINT_DECOMPOSITION_V3_SCHEMA = "guide5_td_c_fast_endpoint_exact_context_decomposition_v3"
TD_C_ENDPOINT_DECOMPOSITION_V4_SCHEMA = "guide5_td_c_fast_endpoint_exact_context_decomposition_v4"
TD_C_ENDPOINT_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328"
)
TD_C_R6_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/guide4-ray-r6-20260808-20260808-153400-post-fix-valid/ray-r6"
)


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _guide8_zero_ambient_report(
    report: Mapping[str, Any], *, factor: float,
) -> dict[str, Any]:
    derived = copy.deepcopy(dict(report))
    required = set(
        json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    filtered_patches = []
    for patch in derived.get("patches", []):
        planes = {
            plane_name: plane for plane_name, plane in (patch.get("planes") or {}).items()
            if f"{patch.get('name')}::{plane_name}" in required
        }
        if planes:
            filtered = copy.deepcopy(dict(patch))
            filtered["planes"] = planes
            filtered_patches.append(filtered)
    derived["patches"] = filtered_patches
    context = dict(derived.get("analysis_context") or {})
    context.update({
        "source": "ray", "purpose": "linearity_bracket",
        "exposure_factor": float(factor), "exposure_status": "recorded",
        "exposure_seconds": float((derived.get("exposure_metadata") or {}).get("seconds", context.get("exposure_seconds"))),
    })
    derived["analysis_context"] = context
    ambient_patches = []
    for patch in derived.get("patches", []):
        ambient = {"name": patch.get("name"), "optimization_eligible": patch.get("optimization_eligible"), "planes": {}}
        for plane_name, plane in (patch.get("planes") or {}).items():
            zero_plane = copy.deepcopy(dict(plane))
            zero_plane.setdefault("metrics", {})["clipped_fraction"] = 0.0
            zero_plane.setdefault("statistics", {}).setdefault("black_corrected_normalized", {})["trimmed_mean"] = 0.0
            ambient["planes"][plane_name] = zero_plane
        ambient_patches.append(ambient)
    derived["ambient_reference"] = {"exposure_seconds": 1.0, "patches": ambient_patches}
    derived["ambient_exposure_metadata"] = {"seconds": 1.0}
    return derived


def _guide8_capture_report(capture: Mapping[str, Any]) -> dict[str, Any]:
    embedded = capture.get("patch_statistics_report")
    if isinstance(embedded, Mapping):
        return copy.deepcopy(dict(embedded))
    path = capture.get("patch_statistics")
    if not isinstance(path, str):
        raise ValueError("GUIDE8 capture lacks its retained patch-statistics report")
    value = _load_json(Path(path))
    if not isinstance(value, Mapping):
        raise ValueError("GUIDE8 patch-statistics report is not an object")
    return dict(value)


def _guide8_repeatability_reports() -> list[dict[str, Any]]:
    boundary = thermal.GUIDE8_P1_ACCEPTED_BOUNDARY_ARTIFACT
    accepted = _load_json(boundary)
    if (
        accepted.get("status") != "holdout_ready_for_manual_branch_review"
        or Path(str(accepted.get("repeatability_run"))).resolve()
        != thermal.GUIDE8_P1_REPEATABILITY_RUN.resolve()
    ):
        raise ValueError("GUIDE8 accepted P1 boundary artifact changed repeatability identity")
    reports = analyze_raw_observer_validation.load_validation_reports(
        thermal.GUIDE8_P1_REPEATABILITY_RUN
    )
    retained = [dict(report) for report in reports]
    actual_hash = raw_response_candidate._reports_sha256(retained)
    if actual_hash != accepted.get("repeatability_input_sha256"):
        raise ValueError("GUIDE8 P1 repeatability reports differ from accepted boundary evidence")
    return retained


def evaluate_guide8_pair_captures(
    faster_capture: Mapping[str, Any], slower_capture: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply the frozen identity P1 evaluator; no new norm or covariance is introduced."""
    faster = _guide8_capture_report(faster_capture)
    slower = _guide8_capture_report(slower_capture)
    fast_seconds = float((faster.get("exposure_metadata") or faster.get("analysis_context") or {})["seconds"] if "seconds" in (faster.get("exposure_metadata") or {}) else faster["analysis_context"]["exposure_seconds"])
    slow_seconds = float((slower.get("exposure_metadata") or slower.get("analysis_context") or {})["seconds"] if "seconds" in (slower.get("exposure_metadata") or {}) else slower["analysis_context"]["exposure_seconds"])
    if not math.isfinite(fast_seconds) or not math.isfinite(slow_seconds) or fast_seconds <= 0 or slow_seconds <= fast_seconds:
        raise ValueError("GUIDE8 pair has invalid recorded MakerNote exposure ordering")
    repeatability = _guide8_repeatability_reports()
    reports = [
        _guide8_zero_ambient_report(faster, factor=1.0),
        _guide8_zero_ambient_report(slower, factor=slow_seconds / fast_seconds),
    ]
    evaluation = raw_response_candidate.evaluate_response_model(
        reports, a=0.0, b=0.0, repeatability_reports=repeatability,
    )
    sigma = evaluation["summary"]["shape_residual_repeatability_sigma_non_reference"]
    passed = sigma["count"] == 58 and sigma["max"] is not None and float(sigma["max"]) <= 3.0
    return {
        "status": "pass" if passed else "fail", "pass": passed,
        "required_feature_count": 58, "maximum_repeatability_sigma": 3.0,
        "identity_response": {"a": 0.0, "b": 0.0},
        "recorded_exposure_ratio": slow_seconds / fast_seconds,
        "evaluation": evaluation,
        "evaluator_source_sha256": _sha256_path(Path(raw_response_candidate.__file__)),
        "accepted_boundary_artifact_sha256": _sha256_path(thermal.GUIDE8_P1_ACCEPTED_BOUNDARY_ARTIFACT),
        "repeatability_input_sha256": raw_response_candidate._reports_sha256(repeatability),
    }


def analyze_guide8_emission_exposure(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir).resolve()
    spec = _load_json(root / "experiment-spec.json")
    canonical = thermal.build_direct_plan(
        thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
    )
    stable_fields = (
        "guide_experiment_id", "variant", "captures", "capture_ids", "frozen_shutters",
        "budgets", "execution_authorization", "analysis_contract",
    )
    if any(spec.get(key) != canonical.get(key) for key in stable_fields):
        raise ValueError("GUIDE8 diagnostic spec differs from its canonical contract")
    run = _load_json(root / "run.json")
    if run.get("status") != "complete" or run.get("cleanup") != "pass":
        raise ValueError("GUIDE8 analysis requires complete acquisition and passing cleanup")
    evidence = _load_json(root / "guide8-emission-exposure.json")
    if evidence.get("schema") != "guide8_ray_emission_exposure_evidence_v1":
        raise ValueError("GUIDE8 execution evidence schema differs")
    branch = str(evidence.get("branch"))
    report: dict[str, Any] = {
        "schema": GUIDE8_ANALYSIS_SCHEMA,
        "status": "classified", "branch": branch,
        "classification": evidence.get("classification"),
        "derived_from_root": str(root),
        "experiment_spec_sha256": _sha256_path(root / "experiment-spec.json"),
        "execution_evidence_sha256": _sha256_path(root / "guide8-emission-exposure.json"),
        "observer_hash": _sha256_path(thermal.OBSERVER_PATH),
        "feature_hash": thermal.canonical_sha256(
            json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
        ),
        "quality_policy_hash": _sha256_path(thermal.POLICY_PATH),
        "invariance_evaluator_hash": _sha256_path(Path(raw_response_candidate.__file__)),
        "accepted_boundary_artifact_hash": _sha256_path(thermal.GUIDE8_P1_ACCEPTED_BOUNDARY_ARTIFACT),
        "formal_capture_count": 0,
        "physical_capture_count": int(evidence.get("physical_capture_count", -1)),
        "historical_1over5000_pooling": False,
    }
    if branch in {"E-C", "E-D"}:
        pair = evidence.get("pair_evaluation")
        if not isinstance(pair, Mapping) or pair.get("status") != "pass":
            raise ValueError("GUIDE8 qualifying branch lacks passing frozen evaluator evidence")
        measured = list(evidence.get("measured", ()))
        by_shutter = {
            str((item.get("step") or {}).get("nominal_shutter")): item.get("capture")
            for item in measured if isinstance(item, Mapping)
        }
        selected = str(evidence["selected_nominal_shutter"])
        guard = str(evidence["guard_nominal_shutter"])
        def recorded_seconds(shutter: str) -> float:
            capture = by_shutter.get(shutter)
            recorded = capture.get("recorded_exposure") if isinstance(capture, Mapping) else None
            if not isinstance(recorded, Mapping) or not isinstance(recorded.get("seconds"), (int, float)):
                raise ValueError("GUIDE8 selected pair lacks recorded MakerNote seconds")
            value = float(recorded["seconds"])
            if not math.isfinite(value) or value <= 0:
                raise ValueError("GUIDE8 selected pair has invalid recorded MakerNote seconds")
            return value
        report.update({
            "selected_nominal_shutter": selected,
            "guard_nominal_shutter": guard,
            "selected_recorded_exposure_seconds": recorded_seconds(selected),
            "guard_recorded_exposure_seconds": recorded_seconds(guard),
            "maximum_exposure_ratio": 1.25,
            "repeatability_evidence_hash": pair.get("repeatability_input_sha256"),
            "historical_1over5000_pooling": selected == "1/5000",
            "pooling_semantics": (
                "historical_1over5000_measurement_procedure_requalified"
                if selected == "1/5000" else
                "old_and_new_target_centers_must_not_be_pooled"
            ),
        })
    return report


def write_guide8_analysis_and_policy(
    run_dir: str | Path, *, analysis_output: str | Path,
    policy_output: str | Path = thermal.GUIDE8_EXPOSURE_POLICY_V2_PATH,
) -> tuple[Path, Path | None]:
    report = analyze_guide8_emission_exposure(run_dir)
    analysis_path = Path(analysis_output).resolve()
    if analysis_path.exists():
        raise FileExistsError("GUIDE8 derived analysis is immutable and already exists")
    policy_path: Path | None = None
    if report["branch"] in {"E-C", "E-D"}:
        policy_path = Path(policy_output).resolve()
        if policy_path.exists():
            raise FileExistsError("GUIDE8 exposure policy v2 is immutable and already exists")
    _write_text_atomic(
        analysis_path, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
    )
    if policy_path is not None:
        policy = {
            "schema": "ray_h120_s100_exposure_policy_v2",
            "state": "H120/S100/INT100",
            "operating_envelope": "fast_op120_reset600_v1",
            "selected_nominal_shutter": report["selected_nominal_shutter"],
            "guard_nominal_shutter": report["guard_nominal_shutter"],
            "selected_recorded_exposure_seconds": report["selected_recorded_exposure_seconds"],
            "guard_recorded_exposure_seconds": report["guard_recorded_exposure_seconds"],
            "maximum_exposure_ratio": 1.25,
            "observer_hash": report["observer_hash"], "feature_hash": report["feature_hash"],
            "quality_policy_hash": report["quality_policy_hash"],
            "invariance_evaluator_hash": report["invariance_evaluator_hash"],
            "accepted_boundary_artifact_hash": report["accepted_boundary_artifact_hash"],
            "repeatability_evidence_hash": report["repeatability_evidence_hash"],
            "derived_from_root": report["derived_from_root"],
            "derived_analysis_sha256": _sha256_path(analysis_path),
            "historical_1over5000_pooling": report["historical_1over5000_pooling"],
            "pooling_semantics": report["pooling_semantics"],
        }
        _write_text_atomic(
            policy_path, json.dumps(policy, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
    return analysis_path, policy_path


def analyze_thermal_run(
    run_dir: str | Path,
    *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    post_fix_revalidation: bool = False,
) -> dict[str, Any]:
    root = Path(run_dir).resolve()
    plan = _load_json(root / "experiment-spec.json")
    run = _load_json(root / "run.json")
    revalidation = (
        _validate_post_fix_revalidation(root, run)
        if post_fix_revalidation
        else None
    )
    if (
        plan.get("experiment_id") not in thermal.EXPERIMENT_IDS
        or run.get("experiment_id") != plan.get("experiment_id")
        or (run.get("status") != "complete" and revalidation is None)
        or run.get("cleanup") != "pass"
    ):
        raise ValueError("thermal analyzer requires a completed exact experiment")
    if plan.get("execution_authorization", {}).get("schema") == "direct_ray_r6_authority_v1":
        expected = thermal.build_ray_r6_spec()
        if plan != expected:
            raise ValueError("direct Ray R6 spec drifted")
        _validate_required_execution_artifacts(root)
        _validate_reproducibility_checkpoint(root, plan, run)
        captures = _load_jsonl(root / "captures.jsonl")
        physical = _load_jsonl(root / "physical-returns.jsonl")
        if len(captures) != 16 or len(physical) != 16:
            raise ValueError("direct Ray R6 requires exactly 16 accepted and physical rows")
        if [row.get("capture_id") for row in captures] != expected["capture_ids"]:
            raise ValueError("direct Ray R6 capture order drifted")
        if [row.get("capture_id") for row in physical] != expected["capture_ids"]:
            raise ValueError("direct Ray R6 physical order drifted")
        _validate_run_counts(run, plan, captures, physical)
        capture_settings = _validate_capture_settings_provenance(
            plan, run, captures,
            allow_implicit_aperture_reconciliation=revalidation is not None,
        )
        physical_by_id = _validate_physical_rows(root, captures, physical)
        expected_steps = {str(row["capture_id"]): row for row in expected["captures"]}
        for row in captures:
            capture_id = str(row["capture_id"])
            step = row.get("plan_step")
            capture = row.get("capture")
            if not isinstance(step, Mapping) or not isinstance(capture, Mapping):
                raise ValueError("direct Ray R6 capture artifact lacks its owners")
            expected_step = expected_steps.get(capture_id)
            if expected_step is None or dict(step) != dict(expected_step):
                raise ValueError("direct Ray R6 capture step differs from canonical spec")
            if any(row.get(key) != expected_step.get(key) for key in (
                "capture_id", "source_id", "state_id", "capture_role", "formal_measurement",
            )):
                raise ValueError("direct Ray R6 capture ledger differs from canonical spec")
            values = capture.get("feature_values")
            if (
                not isinstance(values, Mapping)
                or tuple(values) != tuple(feature_ids)
                or any(
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    for value in values.values()
                )
            ):
                raise ValueError("direct Ray R6 capture feature owner differs from frozen policy")
            direct_quality = capture.get("direct_quality")
            if (
                not isinstance(direct_quality, Mapping)
                or direct_quality.get("status") != "pass"
                or direct_quality.get("feature_count") != len(feature_ids)
            ):
                raise ValueError("direct Ray R6 RAW feature quality did not pass")
            _validate_recorded_exposure(capture, str(expected_step["nominal_shutter"]))
            strip_zero = capture.get("strip_zero_before_capture")
            requested_zero = strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
            observed_zero = strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
            if (
                not isinstance(requested_zero, Mapping)
                or any(int(value) != 0 for value in requested_zero.values())
                or not isinstance(observed_zero, Mapping)
                or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError("direct Ray R6 capture lacks verified strip-zero evidence")
            if capture_id not in physical_by_id:
                raise ValueError("direct Ray R6 capture lacks a physical return")
        quality = _load_json(root / "quality.json")
        expected_quality_rows = [
            {"capture_id": capture_id, "status": "pass", "feature_count": len(feature_ids)}
            for capture_id in expected["capture_ids"]
        ]
        if (
            quality.get("schema") != "p7_direct_ray_r6_quality_v1"
            or quality.get("status") != "pass"
            or quality.get("experiment_id") != thermal.TD_B
            or quality.get("capture_count") != 16
            or quality.get("rows") != expected_quality_rows
        ):
            raise ValueError("direct Ray R6 quality artifact did not pass")
        _validate_commands_and_gates(plan, root)
        _validate_cleanup_and_wrapper(
            root, post_fix_revalidation=post_fix_revalidation,
        )
        formal = []
        for row in captures:
            capture = row.get("capture")
            if not isinstance(capture, Mapping):
                raise ValueError("direct Ray R6 capture owner is missing")
            enriched = dict(row)
            enriched["feature_values"] = capture.get("feature_values")
            enriched["origin"] = "ray_r6"
            enriched["run_root"] = str(root)
            enriched["engineering_quality_status"] = "pass"
            formal.append(enriched)
        result = analyze_td_b(
            formal, feature_ids=feature_ids, r6_operational_contract=True,
        )
        report = {
            "schema": thermal.ANALYSIS_SCHEMA_V2,
            "status": "pass",
            "experiment_id": thermal.TD_B,
            "capture_count": 16,
            "direct_artifact_validation": "pass",
            **result,
        }
        if revalidation is not None:
            report["engineering_revalidation"] = {
                "schema": revalidation["schema"],
                "status": revalidation["status"],
                "artifact": POST_FIX_REVALIDATION_FILE,
                "sha256": _sha256(root / POST_FIX_REVALIDATION_FILE),
            }
            report["capture_settings_reconciliation"] = capture_settings
        return report
    if post_fix_revalidation:
        raise ValueError("post-fix revalidation only supports direct Ray R6")
    if str(plan.get("execution_authorization", {}).get("schema", "")).startswith("direct_"):
        direct_schema = str(plan.get("execution_authorization", {}).get("schema", ""))
        guide6_direct = direct_schema in {
            "direct_guide6_target_local_h120_s100_v1",
            "direct_guide7_f2_alternate_face_v1",
        }
        short_endpoint = direct_schema == "direct_guide7_f2_short_endpoint_v1"
        scale3072_stability = (
            direct_schema == "direct_guide7_f2_scale3072_stability_v1"
        )
        guide6_direct = guide6_direct or short_endpoint or scale3072_stability
        prerequisite = plan.get("scientific_prerequisite")
        if (
            not guide6_direct
            and (
            not isinstance(prerequisite, Mapping)
            or not isinstance(prerequisite.get("path"), str)
            or not isinstance(prerequisite.get("sha256"), str)
            )
        ):
            raise ValueError("direct downstream run lacks its scientific prerequisite")
        if not guide6_direct:
            prerequisite_path = Path(prerequisite["path"]).resolve()
            if (
                prerequisite_path.is_symlink()
                or not prerequisite_path.is_file()
                or hashlib.sha256(prerequisite_path.read_bytes()).hexdigest()
                != prerequisite["sha256"]
            ):
                raise ValueError("direct downstream prerequisite content hash drifted")
            prerequisite_value = _load_json(prerequisite_path)
            if plan.get("experiment_id") == thermal.TD_C:
                if not str(prerequisite_value.get("status", "")).endswith("_pass"):
                    raise ValueError("TD-C direct run lacks a passing combined analysis")
            elif prerequisite_value.get("formal_pass") is not True:
                raise ValueError("strip TD-B direct run lacks a passing Ray analysis")
        expected = thermal.build_direct_plan(
            str(plan["experiment_id"]),
            source=None if guide6_direct else plan.get("source"),
            variant=str(plan.get("variant", "core")),
        )
        if _stable_spec(plan) != _stable_spec(expected):
            raise ValueError("direct run spec differs from the canonical protocol")
        validation_plan = plan
        local_protocol_evidence = None
        if guide6_direct:
            runtime_plan_path = root / "adaptive-execution-plan.json"
            evidence_path = root / "local-controllability.json"
            if runtime_plan_path.is_file() and evidence_path.is_file():
                validation_plan = _load_json(runtime_plan_path)
                local_protocol_evidence = _load_json(evidence_path)
        _validate_required_execution_artifacts(
            root, allow_python_direct=guide6_direct,
            allow_short_endpoint=short_endpoint or scale3072_stability,
        )
        _validate_reproducibility_checkpoint(root, plan, run)
        captures = _load_jsonl(root / "captures.jsonl")
        physical = _load_jsonl(root / "physical-returns.jsonl")
        capture_settings = _validate_capture_settings_provenance(
            plan,
            run,
            captures,
            allow_implicit_aperture_reconciliation=True,
        )
        expected_ids = [str(step["capture_id"]) for step in validation_plan["captures"]]
        if [str(row.get("capture_id")) for row in captures] != expected_ids:
            raise ValueError("direct capture order differs from its spec")
        if [str(row.get("capture_id")) for row in physical] != expected_ids:
            raise ValueError("direct physical order differs from its spec")
        formal = [row for row in captures if row.get("formal_measurement")]
        ambients = [row for row in captures if not row.get("formal_measurement")]
        _validate_run_counts(run, validation_plan, captures, physical)
        physical_by_id = _validate_physical_rows(root, captures, physical)
        expected_steps = {
            str(step["capture_id"]): step for step in validation_plan["captures"]
        }
        for row in captures:
            capture = row.get("capture")
            step = row.get("plan_step")
            capture_id = str(row.get("capture_id"))
            expected_step = expected_steps.get(capture_id)
            if (
                not isinstance(capture, Mapping)
                or not isinstance(step, Mapping)
                or expected_step is None
                or dict(step) != dict(expected_step)
                or any(row.get(key) != expected_step.get(key) for key in (
                    "capture_id", "source_id", "state_id", "capture_role", "formal_measurement",
                ))
            ):
                raise ValueError("direct capture differs from the canonical protocol")
            values = capture.get("feature_values")
            if row.get("formal_measurement") and (
                not isinstance(values, Mapping)
                or tuple(values) != tuple(feature_ids)
                or any(
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    for value in values.values()
                )
            ):
                raise ValueError("direct capture lacks exact frozen feature values")
            if row.get("formal_measurement"):
                direct_quality = capture.get("direct_quality")
                if (
                    not isinstance(direct_quality, Mapping)
                    or direct_quality.get("status") != "pass"
                    or direct_quality.get("feature_count") != len(feature_ids)
                ):
                    raise ValueError("direct capture RAW feature quality did not pass")
                cache_key = thermal.shutter_cache_key_for_step(expected_step)
                nominal_shutter = plan.get("frozen_shutters", {}).get(cache_key)
                if not isinstance(nominal_shutter, str):
                    raise ValueError("direct capture lacks its frozen shutter")
                _validate_recorded_exposure(capture, nominal_shutter)
            if row.get("source_id") == "ray":
                zero = capture.get("strip_zero_before_capture")
                requested = zero.get("requested_payload") if isinstance(zero, Mapping) else None
                observed = zero.get("device_snapshot") if isinstance(zero, Mapping) else None
                if (
                    not isinstance(requested, Mapping)
                    or any(int(value) != 0 for value in requested.values())
                    or not isinstance(observed, Mapping)
                    or any(int(observed.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
                ):
                    raise ValueError("direct Ray capture lacks verified strip-zero evidence")
            elif (
                plan.get("execution_authorization", {}).get("schema")
                in {
                    "direct_td_c_fast_endpoint_holdout_v1",
                    "direct_guide6_target_local_h120_s100_v1",
                    "direct_guide7_f2_alternate_face_v1",
                    "direct_guide7_f2_short_endpoint_v1",
                    "direct_guide7_f2_scale3072_stability_v1",
                }
            ):
                ray_zero = capture.get("ray_zero_before_capture")
                ray_data = (
                    ray_zero.get("data")
                    or ((ray_zero.get("response") or {}).get("data"))
                    if isinstance(ray_zero, Mapping) else None
                )
                if not isinstance(ray_data, Mapping) or int(ray_data.get("intensity", -1)) != 0:
                    raise ValueError("direct strip endpoint capture lacks Ray-zero evidence")
            if capture_id not in physical_by_id:
                raise ValueError("direct capture lacks physical return")
        quality = _load_json(root / "quality.json")
        expected_quality_rows = [
            {"capture_id": str(row["capture_id"]), "status": "pass"}
            for row in validation_plan["captures"] if row.get("formal_measurement")
        ]
        if (
            quality.get("schema") != "p7_direct_protocol_quality_v1"
            or quality.get("status") != "pass"
            or quality.get("experiment_id") != plan["experiment_id"]
            or quality.get("capture_count") != len(formal)
            or quality.get("rows") != expected_quality_rows
        ):
            raise ValueError("direct quality artifact did not pass")
        if guide6_direct and local_protocol_evidence is not None and not short_endpoint:
            if local_protocol_evidence.get("counts", {}).get("total") != len(formal):
                raise ValueError("GUIDE6 adaptive evidence count differs from captures")
            local_commands = _load_jsonl(root / "commands.jsonl")
            if len(local_commands) != len(formal) * 3:
                raise ValueError("GUIDE6 command ledger lacks D/A/tested transitions")
            local_gates = _load_jsonl(root / "isolation-gates.jsonl")
            if len(local_gates) != len(formal) + 1:
                raise ValueError("GUIDE6 isolation ledger lacks per-measurement gates")
            if any(row.get("evidence", {}).get("status") != "pass" for row in local_gates):
                raise ValueError("GUIDE6 isolation ledger contains a failed gate")
        elif not (short_endpoint or scale3072_stability):
            _validate_commands_and_gates(plan, root)
        _validate_cleanup_and_wrapper(
            root, allow_python_direct=guide6_direct,
        )
        formal_rows = []
        for row in formal:
            enriched = dict(row)
            enriched["feature_values"] = row["capture"]["feature_values"]
            enriched["engineering_quality_status"] = "pass"
            enriched["run_root"] = str(root)
            formal_rows.append(enriched)
        if scale3072_stability:
            result = analyze_guide7_f2_scale3072_stability(
                formal_rows, feature_ids=feature_ids,
            )
        elif short_endpoint:
            result = analyze_guide7_f2_short_endpoint(
                formal_rows, feature_ids=feature_ids,
            )
        elif guide6_direct:
            result = analyze_td_c_direct_target_local(
                formal_rows,
                feature_ids=feature_ids,
                protocol_evidence=local_protocol_evidence,
            )
        elif plan.get("variant") == thermal.TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT:
            result = analyze_td_c_fast_endpoint_holdout(
                root,
                feature_ids=feature_ids,
                core_contrast_artifact=plan["inputs"]["td_c_core_contrasts"]["path"],
                combined_artifact=plan["inputs"]["combined_fast_history"]["path"],
            )
        elif plan.get("experiment_id") == thermal.TD_B:
            result = analyze_td_b(formal_rows, feature_ids=feature_ids)
        else:
            result = analyze_td_c(
                formal_rows, ambients=ambients, feature_ids=feature_ids,
                compatibility_fn=compatibility_fn,
            )
        return {
            "schema": thermal.ANALYSIS_SCHEMA_V2,
            "status": "pass",
            "experiment_id": plan["experiment_id"],
            "capture_count": len(formal_rows),
            "direct_artifact_validation": "pass",
            "capture_settings_reconciliation": capture_settings,
            **result,
        }
    raise ValueError("thermal analyzer supports direct protocol runs only")


def _stable_spec(value: Mapping[str, Any]) -> dict[str, Any]:
    stable = dict(value)
    stable.pop("created_at", None)
    stable.pop("scientific_prerequisite", None)
    return stable


def _validate_required_execution_artifacts(
    root: Path, *, allow_python_direct: bool = False,
    allow_short_endpoint: bool = False,
) -> None:
    required = [
        "captures.jsonl", "physical-returns.jsonl", "quality.json",
        "commands-audit.json", "isolation-gates.jsonl",
        "all-off-python.json",
        "input-checkpoint.json",
    ]
    if not allow_short_endpoint:
        required.append("commands.jsonl")
    if not allow_python_direct:
        required.extend((
            "all-off-shell.json", "all-off-shell.exit-status.txt",
            "wrapper-result.json",
        ))
    if any(
        not (root / name).is_file() or (root / name).is_symlink()
        for name in required
    ):
        raise ValueError("direct run lacks a required execution artifact")


def _validate_reproducibility_checkpoint(
    root: Path, plan: Mapping[str, Any], run: Mapping[str, Any],
) -> None:
    checkpoint = _load_json(root / "input-checkpoint.json")
    git = checkpoint.get("git")
    if (
        checkpoint.get("schema") != "p7_direct_reproducibility_checkpoint_v1"
        or not isinstance(git, Mapping)
        or not isinstance(git.get("commit"), str)
        or not git["commit"]
        or git.get("dirty") is not False
        or run.get("git") != dict(git)
        or run.get("reproducibility_checkpoint") != "input-checkpoint.json"
    ):
        raise ValueError("direct run Git checkpoint is missing or dirty")
    plan_inputs = plan.get("inputs")
    checkpoint_inputs = checkpoint.get("inputs")
    if not isinstance(plan_inputs, Mapping) or not isinstance(checkpoint_inputs, Mapping):
        raise ValueError("direct run reproducibility inputs are missing")
    for name in ("location", "code_duty_curve"):
        reference = plan_inputs.get(name)
        item = checkpoint_inputs.get(name)
        if (
            not isinstance(reference, Mapping)
            or not isinstance(item, Mapping)
            or item.get("sha256") != reference.get("sha256")
            or not isinstance(item.get("run_path"), str)
        ):
            raise ValueError(f"direct run {name} checkpoint differs from its spec")
        path = (root / item["run_path"]).resolve()
        if (
            path.is_symlink()
            or not path.is_file()
            or not path.is_relative_to(root)
            or item.get("byte_count") != path.stat().st_size
            or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]
        ):
            raise ValueError(f"direct run {name} checkpoint payload drifted")


def _validate_run_counts(
    run: Mapping[str, Any],
    plan: Mapping[str, Any],
    captures: Sequence[Mapping[str, Any]],
    physical: Sequence[Mapping[str, Any]],
) -> None:
    formal = sum(bool(row.get("formal_measurement")) for row in captures)
    ambient = len(captures) - formal
    if (
        len(captures) != len(plan.get("captures", ()))
        or len(physical) != len(captures)
        or run.get("completed_formal") != formal
        or run.get("accepted_formal_count") != formal
        or run.get("ambient_capture_count") != ambient
        or run.get("accepted_ambient_count") != ambient
        or run.get("physical_returned_cr3_count") != len(physical)
        or run.get("physical_cr3_count")
        != int(plan.get("setup_physical_cr3_count", 0)) + len(physical)
    ):
        raise ValueError("direct run counters differ from retained artifacts")


def _validate_capture_settings_provenance(
    plan: Mapping[str, Any],
    run: Mapping[str, Any],
    captures: Sequence[Mapping[str, Any]],
    *,
    allow_implicit_aperture_reconciliation: bool,
) -> dict[str, Any]:
    planned = plan.get("camera", {}).get("resolved_capture_settings")
    runtime = run.get("capture_settings_provenance")
    if not isinstance(planned, Mapping) or not isinstance(runtime, Mapping):
        raise ValueError("direct capture settings provenance is missing")
    if planned == runtime:
        return {"status": "exact", "runtime": dict(runtime)}
    if not allow_implicit_aperture_reconciliation or any(
        runtime.get(key) != planned.get(key)
        for key in ("owner", "iso", "image_format")
    ) or planned.get("aperture") != "f/4" or runtime.get("aperture") != "implicit auto":
        raise ValueError("direct capture settings differ from the frozen spec")
    actual_rows = []
    for row in captures:
        capture = row.get("capture")
        device_capture = capture.get("capture") if isinstance(capture, Mapping) else None
        if (
            not isinstance(device_capture, Mapping)
            or device_capture.get("iso") != runtime["iso"]
            or device_capture.get("image_format") != runtime["image_format"]
            or device_capture.get("aperture") != runtime["aperture"]
        ):
            raise ValueError("direct capture settings are not uniform across retained frames")
        actual_rows.append(str(row.get("capture_id")))
    return {
        "status": "accepted_uniform_implicit_aperture",
        "planned_aperture_projection": planned["aperture"],
        "runtime_aperture": runtime["aperture"],
        "iso": runtime["iso"],
        "image_format": runtime["image_format"],
        "capture_count": len(actual_rows),
        "scientific_interpretation": "aperture_setting_unchanged_value_not_reported",
    }


def _validate_physical_rows(
    root: Path,
    captures: Sequence[Mapping[str, Any]],
    physical: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    expected_ids = [str(row.get("capture_id")) for row in captures]
    if [str(row.get("capture_id")) for row in physical] != expected_ids:
        raise ValueError("direct physical-return order differs from captures")
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(physical, start=1):
        capture_id = str(row.get("capture_id"))
        if capture_id in by_id or row.get("physical_index") != index:
            raise ValueError("direct physical-return identity is duplicated or reordered")
        for prefix in ("cr3", "sidecar"):
            path = Path(str(row.get(f"{prefix}_path"))).resolve()
            if path.is_symlink() or not path.is_file() or not path.is_relative_to(root):
                raise ValueError("direct physical artifact escaped the run root")
            payload = path.read_bytes()
            if (
                not payload
                or row.get(f"{prefix}_byte_count") != len(payload)
                or row.get(f"{prefix}_sha256") != hashlib.sha256(payload).hexdigest()
            ):
                raise ValueError("direct physical artifact content differs from its ledger")
        if row.get("sidecar_validation_status") != "pass":
            raise ValueError("direct physical return was not accepted")
        by_id[capture_id] = row
    return by_id


def _validate_recorded_exposure(
    capture: Mapping[str, Any], nominal_shutter: str,
) -> None:
    recorded = capture.get("recorded_exposure")
    if not isinstance(recorded, Mapping):
        raise ValueError("direct recorded exposure metadata is missing")
    validate_recorded_exposure_setting(recorded, nominal_shutter)


def _execution_groups(
    experiment_id: str, captures: Sequence[Mapping[str, Any]],
) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if step.get("capture_role") == "ambient":
            groups.append([step])
            continue
        key = thermal.timing_sequence_identity(experiment_id, step)
        previous = (
            groups[-1][0]
            if groups and groups[-1][0].get("capture_role") == "formal"
            else None
        )
        previous_key = (
            None
            if previous is None
            else thermal.timing_sequence_identity(experiment_id, previous)
        )
        if (
            groups
            and previous is not None
            and key == previous_key
            and float(step["requested_elapsed_s"])
            > float(groups[-1][-1]["requested_elapsed_s"])
        ):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def _validate_commands_and_gates(
    plan: Mapping[str, Any], root: Path, *, require_audit: bool = True,
) -> None:
    groups = _execution_groups(str(plan["experiment_id"]), plan["captures"])
    command_steps = [group[0] for group in groups if group[0]["capture_role"] != "ambient"]
    commands = _load_jsonl(root / "commands.jsonl")
    td_c_warm = plan.get("execution_authorization", {}).get("schema") == "direct_td_c_core_authority_v1"
    endpoint_warm = plan.get("execution_authorization", {}).get("schema") == "direct_td_c_fast_endpoint_holdout_v1"
    expected_command_count = len(command_steps) * (3 if endpoint_warm else 2 if td_c_warm else 1)
    if len(commands) != expected_command_count:
        raise ValueError("direct command ledger count differs from protocol transitions")
    if td_c_warm or endpoint_warm:
        command_width = 3 if endpoint_warm else 2
        command_pairs = [commands[index:index + command_width] for index in range(0, len(commands), command_width)]
        for pair, step in zip(command_pairs, command_steps, strict=True):
            preconditions = (
                step.get("warm_precondition_sequence")
                if endpoint_warm else [step.get("warm_precondition")]
            )
            if (
                not isinstance(preconditions, list)
                or len(preconditions) != command_width - 1
                or any(
                    not isinstance(precondition, Mapping)
                    or pair[index].get("event") != "warm_precondition_command_readback_verified"
                    or pair[index].get("source_id") != step.get("source_id")
                    or pair[index].get("state_id") != precondition.get("state_id")
                    or pair[index].get("exact_command_hash") != precondition.get("exact_command_hash")
                    or pair[index].get("dwell_s") != 120
                    or pair[index].get("capture") is not False
                    for index, precondition in enumerate(preconditions)
                )
            ):
                raise ValueError("TD-C warm precondition command ledger differs from protocol")
        capture_commands = [pair[-1] for pair in command_pairs]
    else:
        capture_commands = commands
    for row, step in zip(capture_commands, command_steps, strict=True):
        if (
            row.get("event") != "command_readback_verified"
            or row.get("source_id") != step.get("source_id")
            or row.get("state_id") != step.get("state_id")
            or row.get("exact_command_hash") != step.get("exact_command_hash")
            or not isinstance(row.get("at"), str)
            or not isinstance(row.get("applied"), Mapping)
            or not row["applied"]
            or not isinstance(row.get("readback"), Mapping)
            or not row["readback"]
        ):
            raise ValueError("direct command ledger content differs from protocol transitions")

    direct_continuous_source = plan.get("execution_authorization", {}).get("schema") in {
        "direct_ray_r6_authority_v1", "direct_ray_history_session_v1",
        "direct_strip_history_session_v1",
        "direct_ray_fast_long_bridge_session_v1",
    }
    expected_gates: list[tuple[str, str]] = [("run_start", "both_off")]
    for group in groups:
        first = group[0]
        if first["capture_role"] == "ambient":
            expected_gates.append((str(first["isolation_gate_before"]), "both_off"))
        else:
            if td_c_warm or endpoint_warm:
                expected_gates.append((str(first["isolation_gate_before"]), "both_off"))
            gate_after = group[-1].get("isolation_gate_after")
            if gate_after:
                expected_gates.append((
                    str(gate_after),
                    "strip_zero_only" if direct_continuous_source else "both_off",
                ))
    gates = _load_jsonl(root / "isolation-gates.jsonl")
    if [(str(row.get("gate_id")), str(row.get("gate_kind"))) for row in gates] != expected_gates:
        raise ValueError("direct isolation gate sequence differs from protocol")
    for row in gates:
        evidence = row.get("evidence")
        if (
            not isinstance(row.get("at"), str)
            or not isinstance(evidence, Mapping)
            or evidence.get("status") != "pass"
            or not (
                evidence.get("strip_verified_off") is True
                or evidence.get("source_verified_zero") is True
            )
        ):
            raise ValueError("direct isolation gate did not prove strip zero")
        if row.get("gate_kind") == "both_off":
            if evidence.get("ray_verified_off") is not True or not isinstance(evidence.get("ray_off_command"), Mapping):
                raise ValueError("direct both-off gate did not prove Ray off")
        elif plan.get("execution_authorization", {}).get("schema") == "direct_strip_history_session_v1":
            if evidence.get("source_verified") != "ray" or evidence.get("ray_verified_off") is not True:
                raise ValueError("direct strip history gate did not prove Ray zero")
        elif evidence.get("ray_off_command") is not None or evidence.get("ray_verified_off") is True:
            raise ValueError("direct Ray history gate contains a Ray-off command")

    if require_audit:
        audit = _load_json(root / "commands-audit.json")
        if (
            audit.get("status") != "pass"
            or audit.get("formal_capture_count") != int(plan["budgets"]["formal_cap"])
            or audit.get("ambient_capture_count") != int(plan["budgets"]["ambient_cap"])
        ):
            raise ValueError("direct command audit differs from protocol budgets")
        if audit.get("derived_after_original_child_failure") is True:
            sources = audit.get("source_artifacts")
            expected_sources = ("commands.jsonl", "isolation-gates.jsonl", "captures.jsonl")
            if (
                not isinstance(sources, Mapping)
                or set(sources) != set(expected_sources)
                or any(sources[name] != _sha256(root / name) for name in expected_sources)
            ):
                raise ValueError("derived direct command audit source hashes drifted")


def _validate_cleanup(root: Path) -> None:
    python_cleanup = _load_json(root / "all-off-python.json")
    python_steps = python_cleanup.get("steps")
    if (
        python_cleanup.get("status") != "pass"
        or not isinstance(python_steps, list)
        or not python_steps
        or not all(isinstance(step, Mapping) and step.get("ok") is True for step in python_steps)
    ):
        raise ValueError("direct Python cleanup artifact did not pass")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if (
        not isinstance(shell_cleanup, list)
        or not shell_cleanup
        or not all(
            isinstance(step, Mapping) and step.get("ok") is True
            for step in shell_cleanup
        )
        or (root / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip()
        != "0"
    ):
        raise ValueError("direct shell cleanup artifact did not pass")


def _validate_cleanup_and_wrapper(
    root: Path, *, post_fix_revalidation: bool = False,
    allow_python_direct: bool = False,
) -> None:
    wrapper_paths = (
        root / "all-off-shell.json",
        root / "all-off-shell.exit-status.txt",
        root / "wrapper-result.json",
    )
    if allow_python_direct and not any(path.exists() for path in wrapper_paths):
        python_cleanup = _load_json(root / "all-off-python.json")
        run = _load_json(root / "run.json")
        steps = python_cleanup.get("steps")
        if (
            python_cleanup.get("status") != "pass"
            or not isinstance(steps, list)
            or not steps
            or not all(
                isinstance(step, Mapping) and step.get("ok") is True
                for step in steps
            )
            or run.get("status") != "complete"
            or run.get("cleanup") != "pass"
        ):
            raise ValueError("direct Python execution did not prove clean completion")
        return
    if allow_python_direct and not all(path.is_file() for path in wrapper_paths):
        raise ValueError("direct execution contains a partial wrapper artifact set")
    _validate_cleanup(root)
    wrapper = _load_json(root / "wrapper-result.json")
    if post_fix_revalidation:
        _validate_post_fix_revalidation(root, _load_json(root / "run.json"))
        return
    if (
        wrapper.get("status") != "complete"
        or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("direct wrapper artifact did not prove a clean exit")


def revalidate_direct_ray_r6_exposure_failure(
    run_dir: str | Path,
    *,
    feature_ids: Sequence[str],
    validator_commit: str,
) -> dict[str, Any]:
    """Revalidate one retained 16/16 run stopped by the superseded exposure gate."""

    root = Path(run_dir).resolve()
    if not _is_commit_id(validator_commit):
        raise ValueError("post-fix validator commit must be a 40-character hexadecimal ID")
    revalidation_path = root / POST_FIX_REVALIDATION_FILE
    commands_audit_path = root / "commands-audit.json"
    if revalidation_path.exists() or commands_audit_path.exists():
        raise FileExistsError("post-fix revalidation is one-shot and requires absent derived artifacts")

    plan = _load_json(root / "experiment-spec.json")
    run = _load_json(root / "run.json")
    failure = _load_json(root / "failure.json")
    wrapper = _load_json(root / "wrapper-result.json")
    _validate_legacy_exposure_failure(run, failure, wrapper)
    expected = thermal.build_ray_r6_spec()
    if plan != expected:
        raise ValueError("post-fix revalidation requires the exact direct Ray R6 spec")
    frozen_feature_ids = tuple(
        _feature_ids_from_artifact(thermal.POLICY_PATH)
    )
    if tuple(feature_ids) != frozen_feature_ids:
        raise ValueError("post-fix revalidation requires the frozen feature identity")

    original_hashes = {name: _sha256(root / name) for name in POST_FIX_ORIGINAL_FILES}
    _validate_reproducibility_checkpoint(root, plan, run)
    captures = _load_jsonl(root / "captures.jsonl")
    physical = _load_jsonl(root / "physical-returns.jsonl")
    _validate_run_counts(run, plan, captures, physical)
    _validate_physical_rows(root, captures, physical)
    _validate_commands_and_gates(plan, root, require_audit=False)
    _validate_cleanup(root)

    from camera_based_rgbww_optimizer.optimization import (
        measure_p7_thermal_diagnostics as measure,
    )

    quality_path = root / "quality.json"
    if not quality_path.is_file() or quality_path.is_symlink():
        raise ValueError("post-fix revalidation requires the retained quality artifact")
    quality_hash = _sha256(quality_path)
    quality = measure.validate_direct_ray_r6_post_capture(root, plan, None)
    if _sha256(quality_path) != quality_hash:
        raise ValueError("post-fix revalidation must not rewrite retained quality evidence")
    if quality.get("capture_count") != 16:
        raise ValueError("post-fix revalidation quality count differs from the frozen run")

    commands_audit = {
        "status": "pass",
        "formal_capture_count": int(plan["budgets"]["formal_cap"]),
        "ambient_capture_count": int(plan["budgets"]["ambient_cap"]),
        "derived_after_original_child_failure": True,
        "source_artifacts": {
            name: _sha256(root / name)
            for name in ("commands.jsonl", "isolation-gates.jsonl", "captures.jsonl")
        },
    }
    _write_text_atomic(
        commands_audit_path,
        json.dumps(commands_audit, indent=2, sort_keys=True, allow_nan=False) + "\n",
    )
    try:
        _validate_commands_and_gates(plan, root)
        if any(_sha256(root / name) != digest for name, digest in original_hashes.items()):
            raise ValueError("post-fix revalidation changed original execution evidence")
        evidence = {
            "schema": POST_FIX_REVALIDATION_SCHEMA,
            "status": "pass",
            "reason": "legacy_exact_float_exposure_setting_gate_superseded",
            "run_root": str(root),
            "validator_commit": validator_commit,
            "acquisition_git": dict(run["git"]),
            "original_failure_preserved": True,
            "original_child_exit": int(wrapper["child_exit_code"]),
            "original_artifacts": original_hashes,
            "derived_artifacts": {
                "quality.json": quality_hash,
                "commands-audit.json": _sha256(commands_audit_path),
            },
            "validated": [
                "exact_failure_identity", "reproducibility_checkpoint",
                "capture_and_physical_integrity", "command_and_isolation_sequence",
                "recorded_exposure_setting", "quality", "python_and_shell_cleanup",
            ],
        }
        _write_text_atomic(
            revalidation_path,
            json.dumps(evidence, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        _validate_post_fix_revalidation(root, run)
        return evidence
    except BaseException:
        revalidation_path.unlink(missing_ok=True)
        commands_audit_path.unlink(missing_ok=True)
        raise


def _validate_post_fix_revalidation(
    root: Path, run: Mapping[str, Any],
) -> dict[str, Any]:
    evidence = _load_json(root / POST_FIX_REVALIDATION_FILE)
    failure = _load_json(root / "failure.json")
    wrapper = _load_json(root / "wrapper-result.json")
    _validate_legacy_exposure_failure(run, failure, wrapper)
    if (
        evidence.get("schema") != POST_FIX_REVALIDATION_SCHEMA
        or evidence.get("status") != "pass"
        or evidence.get("reason") != "legacy_exact_float_exposure_setting_gate_superseded"
        or evidence.get("run_root") != str(root)
        or evidence.get("original_failure_preserved") is not True
        or evidence.get("original_child_exit") != 1
        or not _is_commit_id(evidence.get("validator_commit"))
        or evidence.get("acquisition_git") != run.get("git")
    ):
        raise ValueError("post-fix revalidation evidence is invalid")
    originals = evidence.get("original_artifacts")
    derived = evidence.get("derived_artifacts")
    if (
        not isinstance(originals, Mapping)
        or set(originals) != set(POST_FIX_ORIGINAL_FILES)
        or not isinstance(derived, Mapping)
        or set(derived) != {"quality.json", "commands-audit.json"}
    ):
        raise ValueError("post-fix revalidation hashes are missing")
    for name in POST_FIX_ORIGINAL_FILES:
        if originals[name] != _sha256(root / name):
            raise ValueError("post-fix original artifact hash drifted")
    for name in ("quality.json", "commands-audit.json"):
        if derived.get(name) != _sha256(root / name):
            raise ValueError("post-fix derived artifact hash drifted")
    return evidence


def _validate_legacy_exposure_failure(
    run: Mapping[str, Any], failure: Mapping[str, Any], wrapper: Mapping[str, Any],
) -> None:
    if (
        run.get("status") != "failed"
        or run.get("cleanup") != "pass"
        or failure.get("type") != "ValueError"
        or failure.get("message") != LEGACY_EXPOSURE_FAILURE_MESSAGE
        or not isinstance(failure.get("at"), str)
        or wrapper.get("status") != "child_failed"
        or wrapper.get("child_exit_code") != 1
        or wrapper.get("wrapper_exit_code") != 1
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("retained run is not the exact legacy exposure-only failure")


def _sha256(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or unsafe artifact: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_commit_id(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def _replay_timing_evidence(
    capture: Mapping[str, Any], payload: Mapping[str, Any], raw_path: Path, run_root: Path,
) -> tuple[dict[str, Any], str | None]:
    """Replay the retained remote-v2 timing receipt for offline compatibility tools."""
    del capture
    metadata_path = payload.get("remote_metadata_path")
    if not isinstance(metadata_path, str):
        raise ValueError("thermal capture lacks retained remote v2 metadata path")
    root = run_root.resolve()
    resolved_raw = raw_path.resolve()
    resolved_metadata = Path(metadata_path).resolve()
    if not resolved_raw.is_relative_to(root) or not resolved_metadata.is_relative_to(root):
        raise ValueError("thermal v2 CR3/sidecar owner is outside the current run")
    expected_metadata = resolved_raw.with_suffix(resolved_raw.suffix + ".metadata.json")
    if resolved_metadata != expected_metadata:
        raise ValueError("thermal v2 sidecar path does not belong to the retained CR3")
    sidecar = _load_json(resolved_metadata)
    remote_metadata, receipt = camera_remote_v2.split_and_validate_sidecar(
        sidecar, payload=resolved_raw.read_bytes(),
    )
    duplicate_metadata = payload.get("timing_metadata")
    if not isinstance(duplicate_metadata, Mapping) or dict(duplicate_metadata) != sidecar:
        raise ValueError("thermal duplicate timing metadata differs from retained sidecar")
    timing = receipt.get("timing_evidence")
    if not isinstance(timing, Mapping):
        raise ValueError("thermal v2 metadata lacks local timing evidence")
    if receipt.get("received_monotonic_s") != receipt.get("local_response_received_monotonic_s"):
        raise ValueError("thermal v2 successful-attempt response timing is inconsistent")
    replayed = camera_remote_v2.reconstruct_best_effort_timing(
        remote_metadata,
        local_request_started_monotonic_s=float(receipt["local_request_started_monotonic_s"]),
        local_response_received_monotonic_s=float(receipt["local_response_received_monotonic_s"]),
        local_readback_done_monotonic_s=float(timing["local_readback_done_monotonic_s"]),
    )
    if dict(timing) != replayed:
        raise ValueError("thermal local timing receipt was tampered")
    estimate = remote_metadata.get("exposure_start_estimate")
    method = estimate.get("method") if isinstance(estimate, Mapping) else None
    if replayed.get("tier") in thermal.ACCEPTED_TIMING_TIERS and method not in {
        "gphoto_event_minus_recorded_exposure",
        "gphoto_capture_return_minus_recorded_exposure",
    }:
        raise ValueError("thermal available timing estimate lacks a recognized method")
    return replayed, method


def analyze_td_a(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    timing_version: int = 2,
) -> dict[str, Any]:
    cycles: dict[str, dict[int, list[Mapping[str, float]]]] = defaultdict(lambda: defaultdict(list))
    for row in captures:
        step = row["plan_step"]
        features = _features(row, feature_ids)
        cycles[str(step["cycle_index"])][int(step["requested_elapsed_s"])].append(features)
    settling = thermal.settle_from_cycles(cycles, feature_ids, compatibility_fn=compatibility_fn)
    observed_by_slot: dict[int, list[float]] = defaultdict(list)
    for row in captures:
        observed = row.get("best_effort_exposure_start_elapsed_s")
        if observed is not None:
            observed_by_slot[int(row["plan_step"]["requested_elapsed_s"])].append(float(observed))
    groups = {
        f"cycle-{cycle}": [features for point in sorted(points) for features in points[point]]
        for cycle, points in cycles.items()
    }
    audit = thermal.summarize_group_audit(groups, feature_ids)
    if audit["trend_failed"] or audit["dominance_failed"]:
        settling = {"status": "settling_not_demonstrated_by_600", "t_settle_s": None, "six_hundred_is_validation_only": True}
    result = {
        "status": "td_a_pass" if settling["t_settle_s"] is not None else settling["status"],
        "within_cycle_settling": settling,
        "between_cycle_repeatability": audit,
        "state_specific_settle_time": {"A": settling["t_settle_s"]},
        "source_specific_settle_time": settling["t_settle_s"],
        "temperature_not_sufficient_proxy": False,
    }
    if timing_version == 1:
        return result
    if timing_version != 2:
        raise ValueError("unsupported TD-A timing analysis version")
    selected = settling["t_settle_s"]
    if selected is not None and not observed_by_slot.get(int(selected)):
        raise ValueError("TD-A v2 settled result lacks observed timing evidence")
    result.update({
        "source_specific_settle_observed_max_s": (
            None if selected is None else max(observed_by_slot[int(selected)])
        ),
    })
    return result


def analyze_td_b(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    r6_operational_contract: bool = False,
) -> dict[str, Any]:
    if r6_operational_contract:
        if len(captures) != 16:
            raise ValueError("Ray R6 analyzer requires complete 16/16 engineering/quality input")
        if tuple(str(row.get("capture_id")) for row in captures) != thermal.TD_B_R6_CAPTURE_IDS:
            raise ValueError("Ray R6 analyzer requires exact 000..015 order")
        if any(
            row.get("engineering_quality_status") != "pass"
            or row.get("origin") != "ray_r6"
            for row in captures
        ):
            raise ValueError("Ray R6 analyzer requires 16/16 accepted R6-only inputs")
        roots = {str(row.get("run_root")) for row in captures}
        if len(roots) != 1 or "" in roots:
            raise ValueError("Ray R6 analyzer prohibits old/new or cross-root pooling")
    source = str(captures[0]["plan_step"].get("source_id", "ray")) if captures else "ray"
    anchor_compatibility = compatibility_fn or frozen_same_state_compatibility(
        source=source, state="A", feature_ids=feature_ids,
    )
    state_points: dict[str, dict[int, list[Mapping[str, float]]]] = defaultdict(lambda: defaultdict(list))
    anchor_labels = {
        "initial_anchor": "A0",
        "return_after_D": "A_after_D",
        "return_after_B": "A_after_B",
        "return_after_C": "A_after_C",
    }
    anchors: list[tuple[str, np.ndarray]] = []
    for row in captures:
        step = row["plan_step"]
        feature = _features(row, feature_ids)
        if step.get("role") in anchor_labels:
            anchors.append((anchor_labels[str(step["role"])], _unit(feature, feature_ids)))
        else:
            state_points[str(step["state_id"])][int(step["requested_elapsed_s"])].append(feature)
    anchor_pair_diagnostics = []
    for left_index in range(len(anchors)):
        for right_index in range(left_index + 1, len(anchors)):
            left_label, left = anchors[left_index]
            right_label, right = anchors[right_index]
            if compatibility_fn is None:
                diagnostic = frozen_same_state_compatibility_diagnostic(
                    left, right, source=source, state="A", feature_ids=feature_ids,
                )
            else:
                passed = bool(anchor_compatibility(left, right))
                diagnostic = {
                    "statistic": "injected_same_state_compatibility",
                    "decision": "pass" if passed else "fail",
                }
            anchor_pair_diagnostics.append({
                "left": left_label,
                "right": right_label,
                **diagnostic,
            })
    history_pass = (
        [label for label, _ in anchors]
        == ["A0", "A_after_D", "A_after_B", "A_after_C"]
        and len(anchor_pair_diagnostics) == 6
        and all(item["decision"] == "pass" for item in anchor_pair_diagnostics)
    )
    state_results = {
        state: thermal.settle_from_cycles(
            {"switch": points}, feature_ids,
            compatibility_fn=(compatibility_fn or frozen_same_state_compatibility(
                source=source, state=state, feature_ids=feature_ids,
            )),
        )
        for state, points in state_points.items()
    }
    if r6_operational_contract:
        chronology = {
            state: _r6_state_chronology_diagnostic(
                points, feature_ids, source=source, state=state,
            )
            for state, points in sorted(state_points.items())
        }
        nonstationary_states = sorted(
            state for state, result in state_results.items()
            if result.get("t_settle_s") is None
        )
        return {
            "status": (
                "td_b_operational_600_complete_waiting_for_planner"
                if history_pass else "history_dependent_at_operational_dwell_600"
            ),
            "formal_pass": bool(history_pass),
            "return_anchor_history": "pass" if history_pass else "fail",
            "return_anchor_history_effect": "pass" if history_pass else "fail",
            "return_anchor_history_compatibility": {
                "status": "pass" if history_pass else "fail",
                "anchor_order": [label for label, _ in anchors],
                "pair_count": len(anchor_pair_diagnostics),
                "pairwise": anchor_pair_diagnostics,
            },
            "chronology_by_state": chronology,
            "steady_status": "not_demonstrated",
            "time_dependent_within_600": bool(nonstationary_states),
            "operational_endpoint_600_valid": bool(history_pass),
            "operational_dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "nonstationary_states": nonstationary_states,
            "state_specific_settle_time": {
                state: result["t_settle_s"] for state, result in state_results.items()
            },
            "strip_unlock_condition": "planner_accepts_complete_ray_r6_history_pass",
            "td_c_unlock_condition": "combined_td_b_pass",
        }
    status = "td_b_pass"
    if not history_pass:
        status = "history_dependent_at_current_protocol"
    elif any(result["t_settle_s"] is None for result in state_results.values()):
        status = "stop_thermal_extension_required"
    return {
        "status": status, "return_anchor_history_effect": "pass" if history_pass else "fail",
        "state_specific_settle_time": {state: result["t_settle_s"] for state, result in state_results.items()},
    }


def analyze_r6_anchor_vectors(
    evidence_dir: str | Path,
    *,
    feature_ids: Sequence[str],
    source_bundle_sha256: str | None = None,
    source_bundle_member: str | None = None,
    analyzer_commit: str | None = None,
) -> dict[str, Any]:
    """Diagnose retained R6 anchor geometry without reclassifying the failed run."""
    root = Path(evidence_dir).resolve()
    analysis = _load_json(root / "analysis.json")
    quality = _load_json(root / "quality.json")
    revalidation = _load_json(root / POST_FIX_REVALIDATION_FILE)
    captures = _load_jsonl(root / "captures.jsonl")
    covariates = _load_jsonl(root / "thermal-covariates.jsonl")
    if (
        analysis.get("status") != "history_dependent_at_operational_dwell_600"
        or analysis.get("formal_pass") is not False
        or analysis.get("return_anchor_history") != "fail"
        or analysis.get("operational_endpoint_600_valid") is not False
    ):
        raise ValueError("R6 vector reanalysis requires the retained history-negative analysis")
    if (
        quality.get("status") != "pass"
        or quality.get("capture_count") != 16
        or revalidation.get("status") != "pass"
        or revalidation.get("original_child_exit") != 1
        or revalidation.get("original_failure_preserved") is not True
    ):
        raise ValueError("R6 vector reanalysis requires accepted quality and preserved revalidation")
    if (
        len(captures) != 16
        or len(covariates) != 16
        or tuple(str(row.get("capture_id")) for row in captures)
        != thermal.TD_B_R6_CAPTURE_IDS
    ):
        raise ValueError("R6 vector reanalysis requires the exact retained 16-frame order")
    anchor_labels = {
        "initial_anchor": "A0",
        "return_after_D": "A_after_D",
        "return_after_B": "A_after_B",
        "return_after_C": "A_after_C",
    }
    anchors: list[dict[str, Any]] = []
    covariate_reconciliations: list[dict[str, Any]] = []
    for index, (row, covariate) in enumerate(zip(captures, covariates)):
        capture = row.get("capture")
        step = row.get("plan_step")
        if not isinstance(capture, Mapping) or not isinstance(step, Mapping):
            raise ValueError("R6 vector reanalysis capture lacks its retained owners")
        embedded_covariate = dict(capture.get("thermal_covariates") or {})
        if set(embedded_covariate) != set(covariate):
            raise ValueError("R6 vector reanalysis covariate key identity drifted")
        differing_covariates = {
            key for key in covariate
            if embedded_covariate.get(key) != covariate.get(key)
        }
        if differing_covariates - {"previous_state_dwell_s"}:
            raise ValueError("R6 vector reanalysis covariate ledger differs outside the corrected dwell field")
        if differing_covariates:
            covariate_reconciliations.append({
                "sequence_index": index,
                "field": "previous_state_dwell_s",
                "embedded_value": embedded_covariate.get("previous_state_dwell_s"),
                "canonical_ledger_value": covariate.get("previous_state_dwell_s"),
            })
        if int(covariate.get("sequence_index", -1)) != index:
            raise ValueError("R6 vector reanalysis covariate chronology drifted")
        role = str(step.get("role"))
        if role not in anchor_labels:
            continue
        values = capture.get("feature_values")
        if not isinstance(values, Mapping) or tuple(values) != tuple(feature_ids):
            raise ValueError("R6 vector reanalysis anchor differs from the frozen feature identity")
        anchors.append({
            "label": anchor_labels[role],
            "capture_id": str(row["capture_id"]),
            "unit_shape": ordered_unit_shape(values, feature_ids),
            "session_elapsed_s": float(covariate["session_elapsed_s"]),
            "source_on_elapsed_s": float(covariate["source_on_elapsed_s"]),
            "previous_state_id": covariate.get("previous_state_id"),
        })
    expected_labels = ["A0", "A_after_D", "A_after_B", "A_after_C"]
    if [str(anchor["label"]) for anchor in anchors] != expected_labels:
        raise ValueError("R6 vector reanalysis requires the exact four retained A anchors")

    pair_variance = _same_state_pair_variance(source="ray", state="A")
    if pair_variance.shape != (len(feature_ids),):
        raise ValueError("R6 common whitening covariance differs from feature identity")
    whitening_scale = np.sqrt(pair_variance)
    whitened = np.vstack([
        np.asarray(anchor["unit_shape"], dtype=float) / whitening_scale
        for anchor in anchors
    ])
    relative_whitened = whitened - whitened[0]
    centered = relative_whitened - np.mean(relative_whitened, axis=0)
    _u, singular_values, vh = np.linalg.svd(centered, full_matrices=False)
    variance_components = singular_values * singular_values
    total_variance = float(np.sum(variance_components))
    if total_variance <= 0.0:
        raise ValueError("R6 anchors do not identify a drift direction")
    explained = variance_components / total_variance
    direction = np.asarray(vh[0], dtype=float)
    if float((whitened[-1] - whitened[0]) @ direction) < 0.0:
        direction = -direction
    anchor_projections = centered @ direction

    step_vectors = np.diff(whitened, axis=0)
    step_pairs = (
        ("A0_to_A_after_D", 0),
        ("A_after_D_to_A_after_B", 1),
        ("A_after_B_to_A_after_C", 2),
    )
    step_diagnostics = [
        {
            "name": name,
            "norm": float(np.linalg.norm(step_vectors[index])),
            "projection_on_r6_drift_direction": float(step_vectors[index] @ direction),
            "orthogonal_residual_norm": float(np.linalg.norm(
                step_vectors[index] - (step_vectors[index] @ direction) * direction
            )),
        }
        for name, index in step_pairs
    ]
    step_cosines = []
    for left in range(len(step_vectors)):
        for right in range(left + 1, len(step_vectors)):
            step_cosines.append({
                "left": step_pairs[left][0],
                "right": step_pairs[right][0],
                "cosine": _vector_cosine(step_vectors[left], step_vectors[right]),
            })

    deltas = whitened - whitened[0]
    anchor_diagnostics = []
    for index, anchor in enumerate(anchors):
        projection = float(deltas[index] @ direction)
        residual = deltas[index] - projection * direction
        anchor_diagnostics.append({
            "label": anchor["label"],
            "capture_id": anchor["capture_id"],
            "previous_state_id": anchor["previous_state_id"],
            "session_elapsed_s": anchor["session_elapsed_s"],
            "source_on_elapsed_s": anchor["source_on_elapsed_s"],
            "projection_on_r6_drift_direction": projection,
            "orthogonal_residual_norm": float(np.linalg.norm(residual)),
        })

    mds = _classical_mds(whitened)
    chronology_relations = {}
    chronology = analysis.get("chronology_by_state")
    if not isinstance(chronology, Mapping) or set(chronology) != {"B", "C", "D"}:
        raise ValueError("R6 vector reanalysis requires complete D/B/C chronology evidence")
    for state in ("D", "B", "C"):
        state_value = chronology[state]
        slope_values = (
            state_value.get("direction", {}).get("slope_by_feature")
            if isinstance(state_value, Mapping) else None
        )
        if not isinstance(slope_values, Mapping) or tuple(slope_values) != tuple(feature_ids):
            raise ValueError("R6 chronology direction differs from frozen feature identity")
        common_whitened_slope = np.asarray(
            [float(slope_values[feature_id]) for feature_id in feature_ids], dtype=float,
        ) / whitening_scale
        chronology_relations[state] = {
            "cosine_with_r6_drift_direction": _vector_cosine(
                direction, common_whitened_slope,
            ),
            "projection_on_r6_drift_direction": float(common_whitened_slope @ direction),
            "orthogonal_residual_norm": float(np.linalg.norm(
                common_whitened_slope
                - (common_whitened_slope @ direction) * direction
            )),
        }

    elapsed = np.asarray([float(anchor["session_elapsed_s"]) for anchor in anchors])
    source_on = np.asarray([float(anchor["source_on_elapsed_s"]) for anchor in anchors])
    monotonic_projection = bool(np.all(np.diff(anchor_projections) > 0.0))
    pc1_dominates_remainder = bool(float(explained[0]) > float(np.sum(explained[1:])))
    support = pc1_dominates_remainder and monotonic_projection
    return {
        "schema": R6_VECTOR_REANALYSIS_SCHEMA,
        "status": (
            "rank1_drift_hypothesis_supported"
            if support else "rank1_drift_hypothesis_unsupported"
        ),
        "scientific_interpretation": {
            "history_dependence_observed": True,
            "history_origin": "not_identifiable_between_cumulative_period_effect_and_predecessor_carryover",
            "preferred_working_hypothesis": "approximately_rank1_cumulative_source_age_or_session_time_drift",
            "c_specific_carryover": "unproven",
            "causal_confounding_resolved": False,
            "r6_formal_pass": False,
            "r6_reclassification_allowed": False,
            "r6_use_for_new_experiment": "hypothesis_generation_and_frozen_drift_direction_only",
            "strip_combined_td_c": "locked",
        },
        "input_identity": {
            "evidence_dir": str(root),
            "evidence_dir_is_authority": source_bundle_sha256 is None,
            "source_bundle_sha256": source_bundle_sha256,
            "source_bundle_member": source_bundle_member,
            "analyzer_commit": analyzer_commit,
            "feature_ids_sha256": hashlib.sha256(
                ("\n".join(feature_ids) + "\n").encode("utf-8")
            ).hexdigest(),
            "artifacts": {
                name: _sha256(root / name)
                for name in (
                    "analysis.json", "captures.jsonl", "thermal-covariates.jsonl",
                    "quality.json", POST_FIX_REVALIDATION_FILE,
                )
            },
        },
        "covariate_reconciliation": {
            "canonical_owner": "thermal-covariates.jsonl",
            "allowed_differing_field": "previous_state_dwell_s",
            "difference_count": len(covariate_reconciliations),
            "differences": covariate_reconciliations,
            "all_other_fields_exact": True,
        },
        "common_whitening": {
            "space": "ordered_58_feature_unit_shape",
            "covariance": "two_times_frozen_ray_within_state_diagonal_variance",
            "feature_ids": list(feature_ids),
            "diagonal_variance": pair_variance.tolist(),
        },
        "difference_vector_cosines": step_cosines,
        "step_vectors": step_diagnostics,
        "pca": {
            "rank": int(np.linalg.matrix_rank(centered)),
            "singular_values": singular_values.tolist(),
            "explained_variance_ratio": explained.tolist(),
            "pc1_dominates_remainder": pc1_dominates_remainder,
        },
        "classical_mds": mds,
        "r6_drift_direction": {
            "orientation": "A0_toward_A_after_C_positive",
            "values_by_feature": {
                feature_id: float(direction[index])
                for index, feature_id in enumerate(feature_ids)
            },
            "sha256": hashlib.sha256(
                np.asarray(direction, dtype="<f8").tobytes()
            ).hexdigest(),
            "source": "R6_hypothesis_generation_only_frozen_before_new_experiment",
        },
        "anchor_projections": anchor_diagnostics,
        "time_relations": {
            "session_elapsed_s": _linear_relation(elapsed, anchor_projections),
            "source_on_elapsed_s": _linear_relation(source_on, anchor_projections),
            "sample_count": 4,
            "causal_claim_allowed": False,
        },
        "chronology_direction_relations": chronology_relations,
        "support_rule": {
            "kind": "diagnostic_non_gating_structural_rule",
            "pc1_dominates_sum_of_remaining_components": pc1_dominates_remainder,
            "anchor_projection_strictly_monotonic_in_observed_order": monotonic_projection,
            "measurement_threshold_changed": False,
        },
    }


def _vector_cosine(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = np.asarray(left, dtype=float)
    right_values = np.asarray(right, dtype=float)
    denominator = float(np.linalg.norm(left_values) * np.linalg.norm(right_values))
    if denominator <= 0.0:
        raise ValueError("R6 vector cosine requires nonzero vectors")
    return float((left_values @ right_values) / denominator)


def _linear_relation(x: Sequence[float], y: Sequence[float]) -> dict[str, float]:
    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    design = np.column_stack((np.ones(len(x_values)), x_values))
    coefficients, *_ = np.linalg.lstsq(design, y_values, rcond=None)
    fitted = design @ coefficients
    residual = y_values - fitted
    total = float(np.sum((y_values - np.mean(y_values)) ** 2))
    return {
        "intercept": float(coefficients[0]),
        "slope_per_second": float(coefficients[1]),
        "pearson_correlation": float(np.corrcoef(x_values, y_values)[0, 1]),
        "r_squared": 1.0 if total <= 0.0 else float(1.0 - np.sum(residual * residual) / total),
    }


def _classical_mds(values: np.ndarray) -> dict[str, Any]:
    count = len(values)
    squared_distances = np.sum(
        (values[:, None, :] - values[None, :, :]) ** 2, axis=2,
    )
    centering = np.eye(count) - np.ones((count, count)) / count
    gram = -0.5 * centering @ squared_distances @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    tolerance = max(float(eigenvalues[0]), 1.0) * np.finfo(float).eps * count
    positive = eigenvalues > tolerance
    positive_values = eigenvalues[positive]
    coordinates = eigenvectors[:, positive] * np.sqrt(positive_values)
    if coordinates.size and coordinates[-1, 0] < coordinates[0, 0]:
        coordinates[:, 0] *= -1.0
    return {
        "rank": int(np.sum(positive)),
        "eigenvalues": eigenvalues.tolist(),
        "positive_explained_variance_ratio": (
            [] if not len(positive_values)
            else (positive_values / np.sum(positive_values)).tolist()
        ),
        "coordinates": coordinates.tolist(),
    }


def analyze_td_c(
    captures: Sequence[Mapping[str, Any]], *, ambients: Sequence[Mapping[str, Any]],
    feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    p6_compare_fn: Callable[[Sequence[Mapping[str, Any]]], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    compatibility = compatibility_fn or frozen_same_state_compatibility(source="ray", feature_ids=feature_ids)
    sessions: dict[tuple[str, int], dict[str, Any]] = defaultdict(dict)
    for row in captures:
        step = row["plan_step"]
        session = sessions[(str(step["state_id"]), int(step["session_index"]))]
        session[str(step["source_id"])] = _unit(_features(row, feature_ids), feature_ids)
        if int(step["source_order"]) == 1:
            session["order"] = f"{step['source_id']}_first"
    difference_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
    ray_centers: dict[str, list[np.ndarray]] = defaultdict(list)
    strip_centers: dict[str, list[np.ndarray]] = defaultdict(list)
    order_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
    for (state, _session), sources in sorted(sessions.items()):
        if set(sources) != {"ray", "strip", "order"}:
            raise ValueError("TD-C session lacks exactly one Ray and one strip capture")
        difference = sources["strip"] - sources["ray"]
        difference_vectors[state].append(difference)
        ray_centers[state].append(sources["ray"])
        strip_centers[state].append(sources["strip"])
        order_vectors[str(sources["order"])].append(difference)
    compatibility_pass = all(thermal._all_pairs(values, compatibility) for values in difference_vectors.values())
    stable_center_pass = all(
        thermal._all_pairs(ray_centers[state], compatibility)
        and thermal._all_pairs(strip_centers[state], compatibility)
        for state in difference_vectors
    )
    ray_first = order_vectors.get("ray_first", [])
    strip_first = order_vectors.get("strip_first", [])
    order_pass = bool(ray_first and strip_first) and compatibility(
        np.mean(np.vstack(ray_first), axis=0), np.mean(np.vstack(strip_first), axis=0),
    )
    p6 = {"status": "locked_not_part_of_guide5_td_c_core"}
    ambient = {"status": "not_required", "capture_count": len(ambients)}
    gates = {
        "compatibility": "pass" if compatibility_pass else "fail",
        "order_effect": "pass" if order_pass else "fail",
        "stable_center": "pass" if stable_center_pass else "fail",
        "warm_A_cross_source_anchor": "pass" if stable_center_pass else "fail",
    }
    failures = [name for name, decision in gates.items() if decision != "pass"]
    return {
        "status": "td_c_core_pass_waiting_for_planner" if not failures else "td_c_gate_failed",
        "failure_branches": failures, "gates": gates,
        "within_session_compatibility": {"status": gates["compatibility"]},
        "balanced_order_effect": {"status": gates["order_effect"], "design": "ray_first_vs_strip_first"},
        "stable_center": {"status": gates["stable_center"]},
        "current_stable_center_vs_p6": p6,
        "ambient_trend": ambient,
        "comparison_design": "order_balanced_paired_comparison_not_classic_abba",
        "warm_precondition": "reset600_then_D120_then_A120",
        "td_c_expansion_locked": True,
    }


def analyze_td_c_direct_target_local(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    protocol_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Analyze one GUIDE6 target block without a cross-experiment prerequisite."""
    if protocol_evidence is not None:
        return analyze_guide6_local_controllability(
            captures,
            feature_ids=feature_ids,
            protocol_evidence=protocol_evidence,
        )
    by_role = {
        str(row["plan_step"]["role"]): row
        for row in captures
        if isinstance(row.get("plan_step"), Mapping)
    }
    required = {"ray_q_before", "ray_q_after", "strip_candidate"}
    if not required.issubset(by_role):
        raise ValueError("GUIDE6 target-local analysis lacks required target observations")
    ray_before = _unit(_features(by_role["ray_q_before"], feature_ids), feature_ids)
    ray_after = _unit(_features(by_role["ray_q_after"], feature_ids), feature_ids)
    strip_candidate = _unit(_features(by_role["strip_candidate"], feature_ids), feature_ids)
    ray_bracket = frozen_same_state_compatibility_diagnostic(
        ray_before, ray_after, source="ray", state="A", feature_ids=feature_ids,
    )
    ray_target = (ray_before + ray_after) / 2.0
    contrast_variance = (
        _same_state_variance(source="strip", state="A")
        + _same_state_variance(source="ray", state="A") / 2.0
    )
    contrast_limits = calibrate_direct_limits(
        strip_candidate - ray_target, contrast_variance, samples=1000,
    )
    contrast_score = direct_whitened_norm(
        strip_candidate - ray_target, contrast_variance,
    )
    contrast_pass = contrast_score <= float(contrast_limits["guarded_limit"])
    if ray_bracket["decision"] != "pass":
        branch = "S-REFERENCE"
        status = "guide6_s_reference_repeat_required"
    elif not contrast_pass:
        branch = "S-SOLVER-RETRY"
        status = "guide6_s_solver_retry_required"
    else:
        branch = "S-PASS"
        status = "guide6_s1_pass"
    return {
        "status": status,
        "guide6_branch": branch,
        "measurement_valid": True,
        "faithful": bool(contrast_pass),
        "method": "direct_target_local_ray_vs_strip_same_block",
        "cross_experiment_absolute_synthesis": False,
        "ray_before_after_bracket": ray_bracket,
        "target_local_contrast": {
            "statistic": str(contrast_limits["statistic"]),
            "score": float(contrast_score),
            "guarded_limit": float(contrast_limits["guarded_limit"]),
            "decision": "pass" if contrast_pass else "fail",
            "variance": "strip_A_per_capture + ray_A_per_capture / 2",
        },
        "steady_claim": False,
        "locked_later_stages": [
            "B_prepost", "cross_experiment_absolute_synthesis", "solver_sentinel", "P8",
        ],
    }


def analyze_guide7_f2_short_endpoint(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
) -> dict[str, Any]:
    by_role = {str(row["plan_step"]["role"]): row for row in captures}
    required = {"ray_q_before", "ray_q_after", "base_1", "base_2", "candidate_1", "candidate_2", "candidate_3"}
    if not required.issubset(by_role):
        raise ValueError("F2 short endpoint lacks its seven exact observations")
    ray_before = _unit(_features(by_role["ray_q_before"], feature_ids), feature_ids)
    ray_after = _unit(_features(by_role["ray_q_after"], feature_ids), feature_ids)
    ray_bracket = frozen_same_state_compatibility_diagnostic(ray_before, ray_after, source="ray", state="A", feature_ids=feature_ids)
    strip_var = _same_state_variance(source="strip", state="A")
    ray_var = _same_state_variance(source="ray", state="A")
    target = (ray_before + ray_after) / 2.0
    def score(role):
        vec = _unit(_features(by_role[role], feature_ids), feature_ids)
        variance = strip_var + ray_var / 2.0
        limits = calibrate_direct_limits(vec - target, variance, samples=1000)
        value = direct_whitened_norm(vec - target, variance)
        return {"score": float(value), "guarded_limit": float(limits["guarded_limit"]), "decision": "pass" if value <= float(limits["guarded_limit"]) else "fail"}
    bases = [score("base_1"), score("base_2")]
    candidates = [score(role) for role in ("candidate_1", "candidate_2", "candidate_3")]
    base_repeat = frozen_same_state_compatibility_diagnostic(_unit(_features(by_role["base_1"], feature_ids), feature_ids), _unit(_features(by_role["base_2"], feature_ids), feature_ids), source="strip", state="A", feature_ids=feature_ids)
    candidate_repeat = all(item["decision"] == "pass" for item in candidates)
    candidate_pass = all(item["decision"] == "pass" for item in candidates)
    if ray_bracket["decision"] != "pass":
        branch, classification = "S-E", "target_block_invalid"
    elif base_repeat["decision"] != "pass":
        branch, classification = "S-D", "H120_S100_CW_active_fullscale_fast_repeatability_unresolved"
    elif not candidate_repeat:
        branch, classification = "S-D", "H120_S100_CW_active_fullscale_fast_repeatability_unresolved"
    elif candidate_pass:
        branch, classification = "S-A", "H120_S100_CW_face_short_block_faithful"
    else:
        branch, classification = "S-B", "H120_S100_CW_face_stable_nonfaithful_under_short_fast_block"
    return {"status": "guide7_f2_short_endpoint_classified", "branch": branch, "classification": classification, "measurement_valid": branch != "S-E", "faithful": branch == "S-A", "ray_bracket": ray_bracket, "base_direct_contrasts": bases, "candidate_direct_contrasts": candidates, "base_repeatability": base_repeat, "candidate_repeatability": candidate_repeat, "next": "H120/S50" if branch == "S-A" else "GUIDE7_H120_S100_MAX_CODE_3072_DIAGNOSTIC" if branch in {"S-B", "S-C", "S-D"} else "S-MEASUREMENT", "gamut_inference": "prohibited", "steady_claim": False}


def analyze_guide7_f2_scale3072_stability(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
) -> dict[str, Any]:
    """Gate the 3072 route on reset-separated short-block repeatability first."""
    by_role = {str(row["plan_step"]["role"]): row for row in captures}
    repeat_roles = tuple(f"scale3072_repeat_{index}" for index in range(1, 4))
    required = {"ray_q_before", "ray_q_after", *repeat_roles}
    if set(by_role) != required:
        raise ValueError("GUIDE7 scale3072 stability run lacks its five exact observations")
    ray_before = _unit(_features(by_role["ray_q_before"], feature_ids), feature_ids)
    ray_after = _unit(_features(by_role["ray_q_after"], feature_ids), feature_ids)
    repeats = [
        _unit(_features(by_role[role], feature_ids), feature_ids)
        for role in repeat_roles
    ]
    ray_bracket = frozen_same_state_compatibility_diagnostic(
        ray_before, ray_after, source="ray", state="A", feature_ids=feature_ids,
    )
    repeatability = []
    for left_index in range(len(repeats)):
        for right_index in range(left_index + 1, len(repeats)):
            repeatability.append({
                "left": repeat_roles[left_index], "right": repeat_roles[right_index],
                **frozen_same_state_compatibility_diagnostic(
                    repeats[left_index], repeats[right_index],
                    source="strip", state="A", feature_ids=feature_ids,
                ),
            })
    ray_target = (ray_before + ray_after) / 2.0
    variance = (
        _same_state_variance(source="strip", state="A")
        + _same_state_variance(source="ray", state="A") / 2.0
    )
    direct = []
    for role, vector in zip(repeat_roles, repeats, strict=True):
        residual = vector - ray_target
        calibration_center = (
            residual if float(np.linalg.norm(residual)) > 1e-15
            else np.ones_like(residual)
        )
        limits = calibrate_direct_limits(calibration_center, variance, samples=1000)
        value = direct_whitened_norm(residual, variance)
        direct.append({
            "role": role, "score": float(value),
            "guarded_limit": float(limits["guarded_limit"]),
            "decision": "pass" if value <= float(limits["guarded_limit"]) else "fail",
        })
    stable = all(item["decision"] == "pass" for item in repeatability)
    faithful = stable and all(item["decision"] == "pass" for item in direct)
    if ray_bracket["decision"] != "pass":
        branch = "R-REFERENCE"
        classification = "scale3072_target_block_reference_invalid"
        next_action = "S-MEASUREMENT"
    elif not stable:
        branch = "R-UNSTABLE"
        classification = "scale3072_short_repeatability_unresolved"
        next_action = "GUIDE7_H120_S100_MAX_CODE_2048_STABILITY_DIAGNOSTIC"
    elif faithful:
        branch = "R-FAITHFUL"
        classification = "scale3072_stable_faithful_full_scale_operating_boundary"
        next_action = "H120/S50"
    else:
        branch = "R-STABLE-NONFAITHFUL"
        classification = "scale3072_stable_nonfaithful_closed_loop_required"
        next_action = "GUIDE7_H120_S100_MAX_CODE_3072_CLOSED_LOOP"
    return {
        "status": "guide7_f2_scale3072_stability_classified",
        "branch": branch, "classification": classification,
        "measurement_valid": branch != "R-REFERENCE", "faithful": faithful,
        "ray_bracket": ray_bracket,
        "strip_repeatability": repeatability,
        "direct_target_local_contrasts": direct,
        "tested_command": {"cw": 3072, "ww": 0, "r": 0, "g": 3072, "b": 0},
        "max_code": 3072, "stability_first": True,
        "probes_executed": 0, "solver_candidates_executed": 0,
        "next": next_action, "gamut_inference": "prohibited",
        "steady_claim": False,
    }


def analyze_guide6_local_controllability(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    protocol_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply only the frozen LC-A/B/C/D/E table to the first G-active block."""
    if (
        protocol_evidence.get("schema")
        != "guide6_h120_s100_direct_local_controllability_evidence_v1"
        or protocol_evidence.get("gamut_inference") != "prohibited"
        or protocol_evidence.get("terminal_multi_start_solver_unresolved") is not False
    ):
        raise ValueError("GUIDE6 local-controllability evidence contract differs")
    by_role = {
        str(row["plan_step"]["role"]): row
        for row in captures
        if isinstance(row.get("plan_step"), Mapping)
    }
    measured_roles = {
        str(step.get("role", ""))
        for step in protocol_evidence.get("measured_steps", ())
        if isinstance(step, Mapping)
    }
    probe_roles = {role for role in measured_roles if role.startswith("strip_probe_")}
    if not probe_roles:
        probe_roles = {role for role in by_role if role.startswith("strip_probe_")}
    if len(probe_roles) != 4:
        raise ValueError("direct local-controllability evidence lacks four probes")
    required = {
        "ray_q_before", "ray_q_after", "strip_base",
        "strip_base_anchor_after_probe_2", "strip_base_anchor_after_probe_4",
        *probe_roles,
    }
    if not required.issubset(by_role):
        raise ValueError("GUIDE6 local-controllability analysis lacks fixed observations")
    for row in by_role.values():
        source = str((row.get("plan_step") or {}).get("source_id", ""))
        capture = row.get("capture")
        if not isinstance(capture, Mapping):
            capture = row
        if source == "ray":
            zero = capture.get("strip_zero_before_capture")
            requested = zero.get("requested_payload") if isinstance(zero, Mapping) else None
            observed = zero.get("device_snapshot") if isinstance(zero, Mapping) else None
            if (
                not isinstance(requested, Mapping)
                or any(int(value) != 0 for value in requested.values())
                or not isinstance(observed, Mapping)
                or any(int(observed.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError("GUIDE6 Ray observation lacks verified strip-zero evidence")
        elif source == "strip":
            zero = capture.get("ray_zero_before_capture")
            data = (
                zero.get("data")
                or ((zero.get("response") or {}).get("data"))
                if isinstance(zero, Mapping) else None
            )
            if not isinstance(data, Mapping) or int(data.get("intensity", -1)) != 0:
                raise ValueError("GUIDE6 strip observation lacks verified Ray-zero evidence")
    ray_before = _unit(_features(by_role["ray_q_before"], feature_ids), feature_ids)
    ray_after = _unit(_features(by_role["ray_q_after"], feature_ids), feature_ids)
    ray_bracket = frozen_same_state_compatibility_diagnostic(
        ray_before, ray_after, source="ray", state="A", feature_ids=feature_ids,
    )
    base = _unit(_features(by_role["strip_base"], feature_ids), feature_ids)
    anchor_diagnostics = []
    for role in (
        "strip_base_anchor_after_probe_2", "strip_base_anchor_after_probe_4",
    ):
        anchor = _unit(_features(by_role[role], feature_ids), feature_ids)
        anchor_diagnostics.append(frozen_same_state_compatibility_diagnostic(
            base, anchor, source="strip", state="A", feature_ids=feature_ids,
        ))
    ray_target = (ray_before + ray_after) / 2.0
    variance = (
        _same_state_variance(source="strip", state="A")
        + _same_state_variance(source="ray", state="A") / 2.0
    )
    def direct_limits(center: np.ndarray) -> Mapping[str, Any]:
        calibration_center = center
        if float(np.linalg.norm(calibration_center)) <= 1e-15:
            calibration_center = np.ones_like(calibration_center)
        return calibrate_direct_limits(calibration_center, variance, samples=1000)

    def score(row: Mapping[str, Any]) -> dict[str, Any]:
        vector = _unit(_features(row, feature_ids), feature_ids)
        residual = vector - ray_target
        limits = direct_limits(residual)
        value = direct_whitened_norm(residual, variance)
        return {
            "score": float(value),
            "guarded_limit": float(limits["guarded_limit"]),
            "decision": "pass" if value <= float(limits["guarded_limit"]) else "fail",
        }

    base_score = score(by_role["strip_base"])
    candidate_roles = sorted(
        role for role in by_role if role.startswith("strip_solver_candidate_")
    )
    confirmation_roles = sorted(
        role for role in by_role
        if role.startswith("strip_confirmation_") or role.startswith("strip_repeat_")
    )
    if len(candidate_roles) > 4 or len(confirmation_roles) not in {0, 3}:
        raise ValueError("GUIDE6 candidate/confirmation count exceeds the frozen contract")
    candidates = [{"role": role, **score(by_role[role])} for role in candidate_roles]
    confirmations = [{"role": role, **score(by_role[role])} for role in confirmation_roles]
    confirmation_compatibility = []
    for left, right in zip(confirmation_roles, confirmation_roles[1:]):
        confirmation_compatibility.append(frozen_same_state_compatibility_diagnostic(
            _unit(_features(by_role[left], feature_ids), feature_ids),
            _unit(_features(by_role[right], feature_ids), feature_ids),
            source="strip", state="A", feature_ids=feature_ids,
        ))
    drift_pass = all(item["decision"] == "pass" for item in anchor_diagnostics)
    confirmations_pass = (
        len(confirmations) == 3
        and all(item["decision"] == "pass" for item in confirmations)
        and all(item["decision"] == "pass" for item in confirmation_compatibility)
    )
    candidate_pass = any(item["decision"] == "pass" for item in candidates)
    improved = any(item["score"] < base_score["score"] for item in candidates)
    jacobian = protocol_evidence.get("jacobian")
    probes_observable = (
        isinstance(jacobian, Mapping)
        and jacobian.get("effective_rank", 0) >= 1
        and len(protocol_evidence.get("measured_steps", ())) >= 9
    )
    if ray_bracket["decision"] != "pass" or not drift_pass:
        branch = "LC-E"
        classification = "target_block_reference_invalid"
    elif not probes_observable:
        branch = "LC-D"
        classification = "local_controllability_not_observable_under_frozen_exposure"
    elif candidate_pass and confirmations_pass:
        branch = "LC-A"
        classification = "H120_S100_direct_local_solver_pass"
    elif improved:
        branch = "LC-B"
        classification = "H120_S100_local_controllable_but_not_yet_faithful"
    else:
        branch = "LC-C"
        classification = "G_active_neighborhood_inadequate"
    guide7_f2 = protocol_evidence.get("guide7_f2") is True
    repeat_roles = [role for role in confirmation_roles if role.startswith("strip_repeat_")]
    repeat_stable = (
        len(repeat_roles) == 3
        and len(confirmation_compatibility) == 2
        and all(item["decision"] == "pass" for item in confirmation_compatibility)
    )
    if guide7_f2 and branch in {"LC-B", "LC-C"}:
        if not repeat_stable:
            branch = "LC-E"
            classification = "H120_S100_F2_best_command_not_repeatable"
        elif branch == "LC-B":
            classification = "H120_S100_stable_nonfaithful_after_two_fullscale_faces"
        else:
            classification = "H120_S100_two_fullscale_faces_locally_inadequate"
    continuation_generation = int(
        protocol_evidence.get("continuation_generation", 0)
    )
    return {
        "status": "guide6_local_controllability_classified",
        "guide6_branch": branch,
        "classification": classification,
        "measurement_valid": branch not in {"LC-D", "LC-E"},
        "faithful": branch == "LC-A",
        "method": "direct_target_local_ray_vs_strip_same_block",
        "cross_experiment_absolute_synthesis": False,
        "ray_before_after_bracket": ray_bracket,
        "strip_base_drift": {
            "decision": "pass" if drift_pass else "fail",
            "anchors": anchor_diagnostics,
        },
        "base_direct_contrast": base_score,
        "candidate_direct_contrasts": candidates,
        "confirmation_direct_contrasts": confirmations,
        "confirmation_same_state_compatibility": confirmation_compatibility,
        "gamut_inference": "prohibited",
        "terminal_multi_start_solver_unresolved": False,
        "next": (
            "GUIDE7_H120_S100_MAX_CODE_3072_DIAGNOSTIC"
            if guide7_f2 and branch in {"LC-B", "LC-C"}
            else {
            "LC-A": "continue_H120_S50_same_solver_contract",
            "LC-B": (
                "ADVISOR_GATE_REQUIRED_after_centered_continuation"
                if continuation_generation >= 1
                else "one_centered_new_root_continuation_permitted"
            ),
            "LC-C": "one_P2_seeded_active_set_screen_permitted",
            "LC-D": "S-MEASUREMENT",
            "LC-E": "one_new_root_reference_repeat_permitted",
            }[branch]
        ),
        "guide7_f2": guide7_f2,
        "active_face": protocol_evidence.get("active_face"),
        "best_nonfaithful_repeat_stable": repeat_stable if guide7_f2 else None,
        "continuation_generation": continuation_generation,
        "steady_claim": False,
        "locked_later_stages": [
            "13_node_grid", "B_prepost", "cross_experiment_absolute_synthesis",
            "boundary", "Gate-6", "P8",
        ],
    }
def analyze_guide6_seed_negative(
    root_1: str | Path, root_2: str | Path,
) -> dict[str, Any]:
    """Correct two immutable seed-only GUIDE6 analyses without refitting them."""
    roots = (Path(root_1).resolve(), Path(root_2).resolve())
    evidence: list[dict[str, Any]] = []
    candidate_hashes: set[str] = set()
    probe_count = 0
    solver_candidate_count = 0
    confirmation_count = 0
    for index, (root, expected_sha, expected_score) in enumerate(zip(
        roots, GUIDE6_SEED_LEGACY_ANALYSIS_SHA256, GUIDE6_SEED_TARGET_SCORES,
    ), start=1):
        legacy_path = root / "analysis.json"
        if legacy_path.is_symlink() or not legacy_path.is_file():
            raise ValueError(f"GUIDE6 seed root {index} lacks immutable legacy analysis")
        legacy_sha = _sha256(legacy_path)
        if legacy_sha != expected_sha:
            raise ValueError(f"GUIDE6 seed root {index} legacy analysis identity drifted")
        legacy = _load_json(legacy_path)
        score = float(legacy.get("target_local_contrast", {}).get("score", math.nan))
        rows = _load_jsonl(root / "captures.jsonl")
        candidate_rows = [
            row for row in rows
            if row.get("plan_step", {}).get("role") == "strip_candidate"
        ]
        if len(candidate_rows) != 1:
            raise ValueError(f"GUIDE6 seed root {index} lacks exactly one strip seed candidate")
        step = candidate_rows[0]["plan_step"]
        command = step.get("command")
        command_hash = str(step.get("exact_command_hash", ""))
        if command != GUIDE6_SEED_COMMAND or command_hash != GUIDE6_SEED_COMMAND_HASH:
            raise ValueError(f"GUIDE6 seed root {index} command differs from retained evidence")
        capture = candidate_rows[0].get("capture")
        ray_zero = capture.get("ray_zero_before_capture") if isinstance(capture, Mapping) else None
        ray_data = (
            ray_zero.get("data")
            or ((ray_zero.get("response") or {}).get("data"))
            if isinstance(ray_zero, Mapping) else None
        )
        ray_zero_valid = (
            isinstance(ray_data, Mapping)
            and int(ray_data.get("intensity", -1)) == 0
        )
        candidate_hashes.add(command_hash)
        roles = [str(row.get("plan_step", {}).get("role", "")) for row in rows]
        probe_count += sum("probe" in role for role in roles)
        solver_candidate_count += sum("solver_candidate" in role for role in roles)
        confirmation_count += sum("confirmation" in role for role in roles)
        evidence.append({
            "root_index": index,
            "root": str(root),
            "legacy_analysis": {"path": str(legacy_path), "sha256": legacy_sha},
            "legacy_status": legacy.get("status"),
            "legacy_target_score": score,
            "legacy_expected_score": expected_score,
            "ray_zero_before_capture": "pass" if ray_zero_valid else "missing_or_nonzero",
            "exact_command_hash": command_hash,
        })
    if probe_count or solver_candidate_count or confirmation_count or len(candidate_hashes) != 1:
        raise ValueError("accepted GUIDE6 seed roots contain unexpected solver activity")
    return {
        "schema": GUIDE6_SEED_NEGATIVE_SCHEMA,
        "status": "historical_evidence_rejected",
        "classification": "historical_cross_source_contaminated",
        "scientific_input_allowed": False,
        "legacy_status": "guide6_s_solver_retry_required",
        "solver_attempt_count": 0,
        "distinct_strip_candidate_count": 1,
        "probe_count": 0,
        "solver_generated_candidate_count": 0,
        "confirmation_count": 0,
        "exact_command": dict(GUIDE6_SEED_COMMAND),
        "exact_command_hash": GUIDE6_SEED_COMMAND_HASH,
        "rejection_reason": "strip candidate lacks capture-level Ray-zero evidence",
        "legacy_conclusion_allowed": False,
        "gamut_inference": "prohibited",
        "legacy_artifacts_modified": False,
        "roots": evidence,
        "locks": {
            "thirteen_node_grid": True,
            "B_prepost": True,
            "cross_experiment_absolute_synthesis": True,
            "boundary_gate6_p8": True,
        },
    }


def _source_level_contrast_limit(
    terms: Sequence[tuple[np.ndarray, np.ndarray, float]],
    *, seed: int = TD_C_CORE_CONTRAST_MC_SEED,
    samples: int = TD_C_CORE_CONTRAST_MC_SAMPLES,
) -> dict[str, Any]:
    """Calibrate a contrast from noisy source observations, never a difference center."""

    if samples < 1000 or not terms:
        raise ValueError("TD-C contrast Monte Carlo requires terms and at least 1000 samples")
    feature_count = len(terms[0][0])
    covariance = np.zeros(feature_count, dtype=float)
    contrast = np.zeros((samples, feature_count), dtype=float)
    nominal = np.zeros(feature_count, dtype=float)
    rng = np.random.default_rng(seed)
    for center, variance, coefficient in terms:
        center_values = np.asarray(center, dtype=float)
        variance_values = np.asarray(variance, dtype=float)
        if (
            center_values.shape != (feature_count,)
            or variance_values.shape != (feature_count,)
            or np.any(~np.isfinite(center_values))
            or np.any(~np.isfinite(variance_values))
            or np.any(variance_values <= 0.0)
        ):
            raise ValueError("TD-C source observation differs from the feature contract")
        noisy = center_values + rng.normal(
            0.0, np.sqrt(variance_values), size=(samples, feature_count),
        )
        norms = np.linalg.norm(noisy, axis=1)
        if np.any(~np.isfinite(norms)) or np.any(norms <= 0.0):
            raise ValueError("TD-C source-level Monte Carlo produced invalid unit observations")
        contrast += float(coefficient) * (noisy / norms[:, None])
        center_norm = float(np.linalg.norm(center_values))
        if center_norm <= 0.0:
            raise ValueError("TD-C source-level Monte Carlo requires nonzero centers")
        nominal += float(coefficient) * center_values / center_norm
        covariance += float(coefficient) ** 2 * variance_values
    contrast -= nominal
    scores = np.sqrt(np.sum(contrast * contrast / covariance, axis=1))
    limit = float(np.quantile(scores, 0.9973, method=QUANTILE_METHOD))
    return {
        "statistic": "source_level_unit_observation_contrast_whitened_norm",
        "seed": seed,
        "sample_count": samples,
        "quantile": 0.9973,
        "guarded_limit": limit,
        "unguarded_limit": limit,
        "empirical_coverage": float(np.mean(scores <= limit)),
        "difference_center_used": False,
    }


def _endpoint_history_source_pairs(
    root: Path, *, source: str, state: str, feature_ids: Sequence[str],
    evidence: Sequence[Mapping[str, Any]],
) -> list[tuple[np.ndarray, np.ndarray]]:
    builder = thermal.build_ray_history_session_spec if source == "ray" else thermal.build_strip_history_session_spec
    output: list[tuple[np.ndarray, np.ndarray]] = []
    for session_index in (1, 2, 3):
        session_root = root / f"session-{session_index}"
        identity = next(
            (row for row in evidence if int(row.get("session", 0)) == session_index),
            None,
        )
        if (
            not isinstance(identity, Mapping)
            or Path(str(identity.get("root"))).resolve() != session_root
            or identity.get("captures_sha256") != _sha256(session_root / "captures.jsonl")
            or identity.get("quality_sha256") != _sha256(session_root / "quality.json")
        ):
            raise ValueError("endpoint synthesis history bytes differ from canonical combined evidence")
        plan = _load_json(session_root / "experiment-spec.json")
        expected = builder(
            session_index, device_control_enabled=True,
            session_start_condition=plan.get("session_start_condition"),
        )
        if plan != expected:
            raise ValueError("endpoint synthesis history input differs from FAST protocol")
        rows = _load_jsonl(session_root / "captures.jsonl")
        values = {
            str(row["plan_step"]["anchor_label"]): _unit(
                row["capture"]["feature_values"], feature_ids,
            )
            for row in rows
        }
        output.append((values[state], values[f"A_after_{state}"]))
    return output


def analyze_td_c_fast_endpoint_holdout(
    experiment_root: str | Path, *, feature_ids: Sequence[str],
    core_contrast_artifact: str | Path, combined_artifact: str | Path,
) -> dict[str, Any]:
    """Gate the new B/C endpoint only on repeatability and independent synthesis."""

    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    if ids != tuple(_feature_ids_from_artifact(thermal.POLICY_PATH)):
        raise ValueError("TD-C endpoint requires the frozen 58-feature identity")
    core_path = Path(core_contrast_artifact).resolve()
    combined_path = Path(combined_artifact).resolve()
    core = _load_json(core_path)
    combined = _load_json(combined_path)
    if (
        core.get("schema") != TD_C_CORE_CONTRAST_SCHEMA
        or core.get("status") != "canonical_pass"
        or combined.get("schema") != "p7_combined_fast_history_coordinate_v1"
        or combined.get("status") != "canonical_pass"
    ):
        raise ValueError("TD-C endpoint requires accepted core and combined evidence")
    rows = _load_jsonl(root / "captures.jsonl")
    sessions: dict[int, dict[str, Any]] = defaultdict(dict)
    for row in rows:
        step = row["plan_step"]
        sessions[int(step["session_index"])][str(step["source_id"])] = _unit(
            row["capture"]["feature_values"], ids,
        )
        sessions[int(step["session_index"])]["state"] = str(step["state_id"])
    expected = {1: ("B", {"ray", "strip", "state"}), 2: ("C", {"ray", "strip", "state"}),
                3: ("B", {"ray", "strip", "state"}), 4: ("C", {"ray", "strip", "state"})}
    if any(index not in sessions or sessions[index].get("state") != state or set(sessions[index]) != keys
           for index, (state, keys) in expected.items()):
        raise ValueError("TD-C endpoint lacks four exact B/C paired sessions")

    legacy_core = _load_json(core_path)["legacy_analysis"]["path"]
    core_captures_path = Path(legacy_core).parent / "captures.jsonl"
    if _sha256(core_captures_path) != "9354c116fdd37a2613b9d5adf597a30946688b84d4accd15e5c12d562f26651d":
        raise ValueError("TD-C core captures differ from accepted immutable identity")
    core_rows = _load_jsonl(core_captures_path)
    core_centers = {source: [
        _unit(row["capture"]["feature_values"], ids) for row in core_rows
        if row["plan_step"]["source_id"] == source
    ] for source in ("ray", "strip")}
    ray_root = Path(combined["evidence"]["ray_sessions"][0]["root"]).parent
    strip_root = Path(combined["evidence"]["strip_sessions"][0]["root"]).parent
    state_reports: dict[str, Any] = {}
    for state, indices in (("B", (1, 3)), ("C", (2, 4))):
        ray_var = _same_state_variance(source="ray", state=state)
        strip_var = _same_state_variance(source="strip", state=state)
        ray_a_var = _same_state_variance(source="ray", state="A")
        strip_a_var = _same_state_variance(source="strip", state="A")
        endpoint_offsets = [sessions[index]["strip"] - sessions[index]["ray"] for index in indices]
        endpoint_mean = np.mean(np.vstack(endpoint_offsets), axis=0)
        repeat_terms = (
            (sessions[indices[1]]["strip"], strip_var, 1.0),
            (sessions[indices[1]]["ray"], ray_var, -1.0),
            (sessions[indices[0]]["strip"], strip_var, -1.0),
            (sessions[indices[0]]["ray"], ray_var, 1.0),
        )
        repeatability = _td_c_contrast_diagnostic(
            endpoint_offsets[1] - endpoint_offsets[0],
            2.0 * (strip_var + ray_var), terms=repeat_terms,
        )
        ray_pairs = _endpoint_history_source_pairs(
            ray_root, source="ray", state=state, feature_ids=ids,
            evidence=combined["evidence"]["ray_sessions"],
        )
        strip_pairs = _endpoint_history_source_pairs(
            strip_root, source="strip", state=state, feature_ids=ids,
            evidence=combined["evidence"]["strip_sessions"],
        )
        combined_values = [
            (strip_q - strip_a) - (ray_q - ray_a)
            for (ray_q, ray_a), (strip_q, strip_a) in zip(ray_pairs, strip_pairs, strict=True)
        ]
        combined_mean = np.mean(np.vstack(combined_values), axis=0)
        core_mean = np.mean(np.vstack(core_centers["strip"]), axis=0) - np.mean(
            np.vstack(core_centers["ray"]), axis=0,
        )
        synthesis = core_mean + combined_mean
        residual = endpoint_mean - synthesis
        endpoint_variance = (strip_var + ray_var) / 2.0
        core_variance = (strip_a_var + ray_a_var) / 4.0
        combined_variance = (strip_var + strip_a_var + ray_var + ray_a_var) / 3.0
        residual_terms: list[tuple[np.ndarray, np.ndarray, float]] = []
        for index in indices:
            residual_terms.extend(((sessions[index]["strip"], strip_var, 0.5), (sessions[index]["ray"], ray_var, -0.5)))
        for value in core_centers["strip"]:
            residual_terms.append((value, strip_a_var, -0.25))
        for value in core_centers["ray"]:
            residual_terms.append((value, ray_a_var, 0.25))
        for (ray_q, ray_a), (strip_q, strip_a) in zip(ray_pairs, strip_pairs, strict=True):
            residual_terms.extend(((strip_q, strip_var, -1/3), (strip_a, strip_a_var, 1/3),
                                   (ray_q, ray_var, 1/3), (ray_a, ray_a_var, -1/3)))
        agreement = _td_c_contrast_diagnostic(
            residual, endpoint_variance + core_variance + combined_variance,
            terms=residual_terms,
        )
        state_reports[state] = {
            "paired_offset_repeatability": repeatability,
            "independent_synthesis_agreement": agreement,
            "residual_covariance": (
                "new_endpoint_mean+(core_A_absolute_mean)+(combined_local_state_mean)"
            ),
            "pre_solver_offset_zero_gated": False,
            "combined_estimand_equivalence": (
                "balanced_Latin_square_GLS_state_mean_equals_mean_of_three_state_cells"
            ),
        }
    passed = all(
        report[key]["decision"] == "pass"
        for report in state_reports.values()
        for key in ("paired_offset_repeatability", "independent_synthesis_agreement")
    )
    return {
        "schema": TD_C_ENDPOINT_SCHEMA,
        "status": "canonical_pass" if passed else "canonical_scientific_fail",
        "classification": "fast_B_C_endpoint_holdout_pass" if passed else "fast_B_C_endpoint_holdout_failed",
        "capture_count": 8,
        "states": state_reports,
        "evidence": {"core": {"path": str(core_path), "sha256": _sha256(core_path),
                              "captures_sha256": _sha256(core_captures_path)},
                     "combined": {"path": str(combined_path), "sha256": _sha256(combined_path)}},
        "locks": {"legacy_td_c_expansion": True, "solver_sentinel_and_later": True},
        "advisor_review_required": True,
    }


def analyze_td_c_fast_endpoint_decomposition(
    endpoint_root: str | Path, *, feature_ids: Sequence[str],
    endpoint_analysis_artifact: str | Path, core_contrast_artifact: str | Path,
    combined_artifact: str | Path, r6_root: str | Path,
) -> dict[str, Any]:
    """Decompose endpoint synthesis residuals without refitting any parent artifact."""

    ids = tuple(feature_ids)
    endpoint_path = Path(endpoint_root).resolve()
    endpoint_report = _load_json(Path(endpoint_analysis_artifact).resolve())
    core_report = _load_json(Path(core_contrast_artifact).resolve())
    combined_report = _load_json(Path(combined_artifact).resolve())
    if endpoint_report.get("schema") != TD_C_ENDPOINT_SCHEMA or endpoint_report.get("capture_count") != 8:
        raise ValueError("endpoint decomposition requires the accepted eight-observation endpoint artifact")
    if core_report.get("status") != "canonical_pass" or combined_report.get("status") != "canonical_pass":
        raise ValueError("endpoint decomposition requires accepted immutable parent analyses")

    rows = _load_jsonl(endpoint_path / "captures.jsonl")
    endpoint_sessions: dict[int, dict[str, Any]] = defaultdict(dict)
    for row in rows:
        step = row["plan_step"]
        endpoint_sessions[int(step["session_index"])][str(step["source_id"])] = _unit(
            row["capture"]["feature_values"], ids,
        )
        endpoint_sessions[int(step["session_index"])]["state"] = str(step["state_id"])

    core_path = Path(core_report["legacy_analysis"]["path"]).resolve()
    core_rows = _load_jsonl(core_path.parent / "captures.jsonl")
    core_ray = [_unit(r["capture"]["feature_values"], ids) for r in core_rows if r["plan_step"]["source_id"] == "ray"]
    core_strip = [_unit(r["capture"]["feature_values"], ids) for r in core_rows if r["plan_step"]["source_id"] == "strip"]
    core_mean = np.mean(np.vstack(core_strip), axis=0) - np.mean(np.vstack(core_ray), axis=0)
    ray_history = combined_report["evidence"]["ray_sessions"]
    strip_history = combined_report["evidence"]["strip_sessions"]
    ray_root = Path(ray_history[0]["root"]).parent
    strip_root = Path(strip_history[0]["root"]).parent
    local_means: dict[str, np.ndarray] = {}
    for state in ("B", "C"):
        ray_pairs = _endpoint_history_source_pairs(ray_root, source="ray", state=state, feature_ids=ids, evidence=ray_history)
        strip_pairs = _endpoint_history_source_pairs(strip_root, source="strip", state=state, feature_ids=ids, evidence=strip_history)
        local_means[state] = np.mean(np.vstack([
            (strip_q - strip_a) - (ray_q - ray_a)
            for (ray_q, ray_a), (strip_q, strip_a) in zip(ray_pairs, strip_pairs, strict=True)
        ]), axis=0)

    vectors: dict[str, np.ndarray] = {}
    variances: dict[str, np.ndarray] = {}
    for state, indices in (("B", (1, 3)), ("C", (2, 4))):
        endpoint_mean = np.mean(np.vstack([
            endpoint_sessions[index]["strip"] - endpoint_sessions[index]["ray"]
            for index in indices
        ]), axis=0)
        vectors[f"endpoint_mean_{state}"] = endpoint_mean
        vectors[f"synthesis_residual_{state}"] = endpoint_mean - core_mean - local_means[state]
        variances[f"endpoint_mean_{state}"] = (
            _same_state_variance(source="strip", state=state)
            + _same_state_variance(source="ray", state=state)
        ) / 2.0
        variances[f"synthesis_residual_{state}"] = variances[f"endpoint_mean_{state}"] + (
            _same_state_variance(source="strip", state="A")
            + _same_state_variance(source="ray", state="A")
        ) / 4.0 + (
            _same_state_variance(source="strip", state=state)
            + _same_state_variance(source="strip", state="A")
            + _same_state_variance(source="ray", state=state)
            + _same_state_variance(source="ray", state="A")
        ) / 3.0

    r6_rows = _load_jsonl(Path(r6_root).resolve() / "captures.jsonl")
    anchors = {
        str(r["plan_step"].get("role")): _unit(r["capture"]["feature_values"], ids)
        for r in r6_rows if r["plan_step"].get("role") in {"return_after_D", "return_after_B", "return_after_C"}
    }
    anchor_vectors = {
        "A_after_B_minus_A_after_D": anchors["return_after_B"] - anchors["return_after_D"],
        "A_after_C_minus_A_after_D": anchors["return_after_C"] - anchors["return_after_D"],
    }
    anchor_variance = 2.0 * _same_state_variance(source="ray", state="A")
    vectors.update(anchor_vectors)
    variances["A_after_B_minus_A_after_D"] = anchor_variance
    variances["A_after_C_minus_A_after_D"] = anchor_variance
    for name, state in (("B", "B"), ("C", "C")):
        vectors[f"residual_minus_anchor_substitution_{name}"] = vectors[f"synthesis_residual_{name}"] - anchor_vectors[
            f"A_after_{name}_minus_A_after_D"
        ]
        variances[f"residual_minus_anchor_substitution_{name}"] = variances[f"synthesis_residual_{name}"] + anchor_variance
    vectors["B_minus_C_synthesis_residual"] = vectors["synthesis_residual_B"] - vectors["synthesis_residual_C"]
    variances["B_minus_C_synthesis_residual"] = (
        variances["synthesis_residual_B"] + variances["synthesis_residual_C"]
        - 2.0 * ((_same_state_variance(source="strip", state="A") + _same_state_variance(source="ray", state="A")) / 4.0)
    )
    return {
        "schema": TD_C_ENDPOINT_DECOMPOSITION_SCHEMA,
        "status": "offline_derived_no_parent_refit",
        "classification": "absolute_composition_rejected_endpoint_observations_retained",
        "vectors": {name: {feature: float(value[i]) for i, feature in enumerate(ids)} for name, value in vectors.items()},
        "scores": {name: direct_whitened_norm(value, variances[name]) for name, value in vectors.items()},
        "covariance": {
            "shared_observation_terms": "core_A_shared_between_B_and_C_is_cancelled_in_B_minus_C",
            "synthesis_residual": "endpoint_mean + core_A_absolute_mean + combined_local_state_mean",
            "refit_endpoint_data": False,
        },
        "evidence": {
            "endpoint": {"path": str(endpoint_path), "sha256": _sha256(Path(endpoint_analysis_artifact).resolve())},
            "core": {"path": str(core_path), "sha256": _sha256(Path(core_contrast_artifact).resolve())},
            "combined": {"path": str(Path(combined_artifact).resolve()), "sha256": _sha256(Path(combined_artifact).resolve())},
            "r6_root": str(Path(r6_root).resolve()),
        },
        "locks": {"new_B_anchor_direction": False, "C_validation": True, "solver_sentinel_and_later": True},
    }


def analyze_td_c_fast_endpoint_exact_context_v3(
    endpoint_root: str | Path, *, feature_ids: Sequence[str],
    endpoint_analysis_artifact: str | Path, core_contrast_artifact: str | Path,
    combined_artifact: str | Path,
) -> dict[str, Any]:
    return _analyze_td_c_fast_endpoint_exact_context(
        endpoint_root, feature_ids=feature_ids,
        endpoint_analysis_artifact=endpoint_analysis_artifact,
        core_contrast_artifact=core_contrast_artifact,
        combined_artifact=combined_artifact,
        sign_corrected=False,
    )


def analyze_td_c_fast_endpoint_exact_context_v4(
    endpoint_root: str | Path, *, feature_ids: Sequence[str],
    endpoint_analysis_artifact: str | Path, core_contrast_artifact: str | Path,
    combined_artifact: str | Path,
) -> dict[str, Any]:
    """Create the immutable GUIDE6 sign-corrected exact-context artifact."""
    return _analyze_td_c_fast_endpoint_exact_context(
        endpoint_root, feature_ids=feature_ids,
        endpoint_analysis_artifact=endpoint_analysis_artifact,
        core_contrast_artifact=core_contrast_artifact,
        combined_artifact=combined_artifact,
        sign_corrected=True,
    )


def _analyze_td_c_fast_endpoint_exact_context(
    endpoint_root: str | Path, *, feature_ids: Sequence[str],
    endpoint_analysis_artifact: str | Path, core_contrast_artifact: str | Path,
    combined_artifact: str | Path, sign_corrected: bool,
) -> dict[str, Any]:
    """Use only FAST cross-source primitive observations for the Advisor v3 gate.

    In particular, this deliberately has no R6 input.  Coefficients are aggregated
    by immutable observation identity before Monte Carlo so shared observations
    cancel algebraically instead of being counted as independent noise.
    """
    ids = tuple(feature_ids)
    endpoint_path = Path(endpoint_root).resolve()
    endpoint_report = _load_json(Path(endpoint_analysis_artifact).resolve())
    core_report = _load_json(Path(core_contrast_artifact).resolve())
    combined_report = _load_json(Path(combined_artifact).resolve())
    if endpoint_report.get("schema") != TD_C_ENDPOINT_SCHEMA or endpoint_report.get("capture_count") != 8:
        raise ValueError("v3 requires the accepted eight-observation endpoint artifact")
    if core_report.get("status") != "canonical_pass" or combined_report.get("status") != "canonical_pass":
        raise ValueError("v3 requires accepted immutable parent analyses")

    def rows(path: Path) -> list[dict[str, Any]]:
        return _load_jsonl(path / "captures.jsonl")

    endpoint_rows = rows(endpoint_path)
    endpoint: dict[int, dict[str, np.ndarray]] = defaultdict(dict)
    endpoint_keys: dict[tuple[int, str], str] = {}
    for i, row in enumerate(endpoint_rows):
        step = row["plan_step"]
        session, source = int(step["session_index"]), str(step["source_id"])
        endpoint[session][source] = _unit(row["capture"]["feature_values"], ids)
        endpoint_keys[(session, source)] = f"endpoint:{i}"

    # Resolve and identity-check the two FAST history source roots.
    histories: dict[str, list[dict[str, Any]]] = {}
    for source, entries_key in (("ray", "ray_sessions"), ("strip", "strip_sessions")):
        entries = combined_report.get("evidence", {}).get(entries_key)
        if not isinstance(entries, list) or len(entries) != 3:
            raise ValueError("v3 requires three immutable FAST history sessions per source")
        checked = []
        for entry in entries:
            root = Path(str(entry["root"])).resolve()
            if entry.get("captures_sha256") != _sha256(root / "captures.jsonl"):
                raise ValueError("FAST history captures identity differs from combined evidence")
            checked.append({"root": root, "rows": rows(root)})
        histories[source] = checked

    # Capture values and stable keys for exact D->A->B cells (sessions 1 and 2).
    history: dict[tuple[str, int, str], tuple[np.ndarray, str]] = {}
    for source, sessions in histories.items():
        for session_index, item in enumerate(sessions, 1):
            for i, row in enumerate(item["rows"]):
                step = row["plan_step"]
                label = str(step.get("anchor_label"))
                if label in {"B", "C", "A_after_D", "A_after_B", "A_after_C", "A0"}:
                    history[(source, session_index, label)] = (
                        _unit(row["capture"]["feature_values"], ids),
                        f"history:{source}:{session_index}:{i}",
                    )

    core_path = Path(core_report["legacy_analysis"]["path"]).resolve()
    core_rows = rows(core_path.parent)
    core: dict[str, list[tuple[np.ndarray, str]]] = defaultdict(list)
    for i, row in enumerate(core_rows):
        source = str(row["plan_step"]["source_id"])
        core[source].append((_unit(row["capture"]["feature_values"], ids), f"core:{source}:{i}"))
    if not core["ray"] or len(core["ray"]) != len(core["strip"]):
        raise ValueError("v3 requires the immutable balanced TD-C core observations")

    variances = {("ray", s): _same_state_variance(source="ray", state=s) for s in ("A", "B", "C")}
    variances.update({("strip", s): _same_state_variance(source="strip", state=s) for s in ("A", "B", "C")})

    def contrast(terms: dict[str, tuple[np.ndarray, np.ndarray, float]]) -> tuple[np.ndarray, dict[str, Any]]:
        vector = np.zeros(len(ids), dtype=float)
        mc_terms: list[tuple[np.ndarray, np.ndarray, float]] = []
        serialized = []
        for key, (value, variance, coefficient) in sorted(terms.items()):
            vector += coefficient * value
            mc_terms.append((value, variance, coefficient))
            serialized.append({"observation": key, "coefficient": coefficient})
        return vector, {"terms": serialized, "_terms_raw": mc_terms, "monte_carlo": _source_level_contrast_limit(mc_terms)}

    def add(terms: dict[str, tuple[np.ndarray, np.ndarray, float]], key: str, value: np.ndarray,
            variance: np.ndarray, coefficient: float) -> None:
        if key in terms:
            old_value, old_variance, old_coefficient = terms[key]
            if not np.array_equal(old_value, value) or not np.array_equal(old_variance, variance):
                raise ValueError("observation identity maps to inconsistent source data")
            terms[key] = (old_value, old_variance, old_coefficient + coefficient)
        else:
            terms[key] = (value, variance, coefficient)

    def endpoint_terms(state: str) -> dict[str, tuple[np.ndarray, np.ndarray, float]]:
        terms: dict[str, tuple[np.ndarray, np.ndarray, float]] = {}
        endpoint_sessions = (1, 3) if state == "B" else (2, 4)
        for session in endpoint_sessions:
            for source, sign in (("strip", 0.5), ("ray", -0.5)):
                add(terms, endpoint_keys[(session, source)], endpoint[session][source], variances[(source, state)], sign)
        return terms

    def core_a_terms(terms: dict[str, tuple[np.ndarray, np.ndarray, float]], coefficient: float) -> None:
        n = len(core["ray"])
        for source, sign in (("strip", -coefficient / n), ("ray", coefficient / n)):
            for value, key in core[source]:
                add(terms, key, value, variances[(source, "A")], sign)

    def local_terms(terms: dict[str, tuple[np.ndarray, np.ndarray, float]], state: str, coefficient: float, anchor: str) -> None:
        # local = mean[(strip_state-ray_state) - (strip_anchor-ray_anchor)] over exact D->A->B cells.
        for session in (1, 2):
            for source, sign in (("strip", 1.0), ("ray", -1.0)):
                for label, local_sign in ((state, 1.0), (anchor, -1.0)):
                    value, key = history[(source, session, label)]
                    add(terms, key, value, variances[(source, state if label == state else "A")], coefficient * sign * local_sign / 2.0)

    def make_synthesis(state: str, anchor: str) -> tuple[np.ndarray, dict[str, Any]]:
        terms = endpoint_terms(state)
        core_a_terms(terms, 1.0)
        local_terms(terms, state, 1.0, anchor)
        # v3 negated core twice.  v4 keeps core strip=-1/n and Ray=+1/n,
        # and negates only the local-coordinate primitive terms.
        for key, (value, variance, coefficient) in list(terms.items()):
            if key.startswith("endpoint:"):
                continue
            if sign_corrected and key.startswith("core:"):
                continue
            terms[key] = (value, variance, -coefficient)
        result = contrast(terms)
        if sign_corrected:
            # GUIDE6 freezes the finite-sample guard from v3.  Independent,
            # centered primitive noise is sign invariant, so retain v3's draw
            # orientation while serializing the corrected scientific coefficients.
            guard_terms = [
                (value, variance, -coefficient if key.startswith("core:") else coefficient)
                for key, (value, variance, coefficient) in sorted(terms.items())
            ]
            result[1]["monte_carlo"] = _source_level_contrast_limit(guard_terms)
            result[1]["monte_carlo"]["sign_equivalent_draw_orientation"] = (
                "v3_frozen_guard_core_sign_orientation"
            )
        return result

    pre_terms = make_synthesis("B", "A_after_D")
    post_terms = make_synthesis("B", "A_after_B")
    # Anchor direction h = local_pre - local_post; B observations cancel exactly.
    h_terms: dict[str, tuple[np.ndarray, np.ndarray, float]] = {}
    local_terms(h_terms, "B", 1.0, "A_after_D")
    local_terms(h_terms, "B", -1.0, "A_after_B")
    h_vec, h_meta = contrast(h_terms)

    # Build the B-minus-C post-synthesis residual from the same primitive sources.
    b_post_terms = {
        item["observation"]: raw
        for item, raw in zip(post_terms[1]["terms"], post_terms[1]["_terms_raw"], strict=True)
    }
    c_terms = endpoint_terms("C")
    core_a_terms(c_terms, 1.0)
    local_terms(c_terms, "C", 1.0, "A_after_C")
    for key, (value, variance, coefficient) in list(c_terms.items()):
        if not key.startswith("endpoint:") and not (sign_corrected and key.startswith("core:")):
            c_terms[key] = (value, variance, -coefficient)
    # e_B - e_C: merge B residual and negative C residual.
    bc_terms = dict(b_post_terms)
    for key, (value, variance, coefficient) in c_terms.items():
        add(bc_terms, key, value, variance, -coefficient)
    bc_vec, bc_meta = contrast(bc_terms)
    if sign_corrected:
        guard_terms = [
            (value, variance, -coefficient if key.startswith("core:") else coefficient)
            for key, (value, variance, coefficient) in sorted(bc_terms.items())
        ]
        bc_meta["monte_carlo"] = _source_level_contrast_limit(guard_terms)
        bc_meta["monte_carlo"]["sign_equivalent_draw_orientation"] = "v3_frozen_guard_core_sign_orientation"

    def report(vector: np.ndarray, meta: dict[str, Any], *, zero_gate: bool = True) -> dict[str, Any]:
        score_terms = meta.pop("_terms_raw")
        score = direct_whitened_norm(vector, sum((coefficient ** 2) * var for _, var, coefficient in score_terms))
        return {"score": score, "guarded_limit": meta["monte_carlo"]["guarded_limit"], "decision": "pass" if score <= meta["monte_carlo"]["guarded_limit"] else "fail", "hard_gate": zero_gate, "primitive_terms": meta["terms"], "monte_carlo": meta["monte_carlo"]}

    pre_vec, pre_meta = pre_terms
    post_vec, post_meta = post_terms
    identity = (post_vec - pre_vec - h_vec) if sign_corrected else (pre_vec - post_vec - h_vec)
    identity_max_abs = float(np.max(np.abs(identity)))
    identity_l2 = float(np.linalg.norm(identity))
    coefficient_identity: dict[str, float] = defaultdict(float)
    if sign_corrected:
        for item in post_meta["terms"]:
            coefficient_identity[item["observation"]] += float(item["coefficient"])
        for item in pre_meta["terms"]:
            coefficient_identity[item["observation"]] -= float(item["coefficient"])
        for item in h_meta["terms"]:
            coefficient_identity[item["observation"]] -= float(item["coefficient"])
        coefficient_identity = {
            key: value for key, value in coefficient_identity.items() if value != 0.0
        }
        if coefficient_identity or identity_max_abs > 1e-12 or identity_l2 > 1e-12:
            raise ValueError("v4 exact algebra identity failed")
    return {
        "schema": (
            TD_C_ENDPOINT_DECOMPOSITION_V4_SCHEMA
            if sign_corrected else TD_C_ENDPOINT_DECOMPOSITION_V3_SCHEMA
        ),
        "status": "offline_derived_no_parent_refit",
        "classification": (
            "B_local_coordinate_transfer_unresolved_with_anchor_direction_compatible"
            if sign_corrected else "partially_valid_not_gate_complete"
        ),
        "absolute_synthesis_status": "rejected" if sign_corrected else "under_review",
        "anchor_direction_status": "not_detected" if sign_corrected else "under_review",
        "B_C_relative_transfer_status": "failed_not_physical_cause" if sign_corrected else "under_review",
        "scientific_scope": "FAST_cross_source_exact_D_A_B_context_only",
        "r6_input_count": 0,
        "vectors": {"B_exact_pre_synthesis_residual": {f: float(v) for f, v in zip(ids, pre_vec)}, "B_exact_post_synthesis_residual": {f: float(v) for f, v in zip(ids, post_vec)}, "B_anchor_direction": {f: float(v) for f, v in zip(ids, h_vec)}, "B_minus_C_synthesis_residual": {f: float(v) for f, v in zip(ids, bc_vec)}},
        "contrasts": {"B_exact_pre_synthesis_residual": report(pre_vec, pre_meta), "B_exact_post_synthesis_residual": report(post_vec, post_meta), "B_anchor_direction": report(h_vec, h_meta), "B_minus_C_synthesis_residual": report(bc_vec, bc_meta)},
        "identity_error": identity_l2,
        "identity_max_abs": identity_max_abs,
        "identity_l2": identity_l2,
        "coefficient_identity_nonzero_terms": coefficient_identity if sign_corrected else None,
        "identity_error_vector": {f: float(v) for f, v in zip(ids, identity)},
        "identity": "e_post - e_pre - h_B = 0 by primitive coefficient cancellation",
        "evidence": {"endpoint_analysis": {"path": str(Path(endpoint_analysis_artifact).resolve()), "sha256": _sha256(Path(endpoint_analysis_artifact).resolve())}, "core_analysis": {"path": str(Path(core_contrast_artifact).resolve()), "sha256": _sha256(Path(core_contrast_artifact).resolve())}, "combined_analysis": {"path": str(Path(combined_artifact).resolve()), "sha256": _sha256(Path(combined_artifact).resolve())}},
        "locks": {
            "B_prepost_experiments": "deferred_diagnostic_only" if sign_corrected else True,
            "C_validation": True,
            "cross_experiment_absolute_synthesis": True,
            "direct_target_local_sentinel": False if sign_corrected else True,
            "solver_sentinel_and_later": not sign_corrected,
        },
    }


def _td_c_contrast_diagnostic(
    value: np.ndarray,
    variance: np.ndarray,
    *,
    terms: Sequence[tuple[np.ndarray, np.ndarray, float]],
    zero_is_gate: bool = True,
) -> dict[str, Any]:
    limits = _source_level_contrast_limit(terms)
    score = direct_whitened_norm(value, variance)
    compatible = score <= float(limits["guarded_limit"])
    return {
        "score": score,
        "guarded_limit": float(limits["guarded_limit"]),
        "decision": "pass" if compatible else "fail",
        "zero_compatibility": "compatible" if compatible else "fail_expected_pre_solver",
        "hard_gate": zero_is_gate,
        "monte_carlo": limits,
    }


def analyze_td_c_core_contrasts_v2_1(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
    legacy_analysis_artifact: str | Path,
) -> dict[str, Any]:
    """Correct TD-C core estimands without modifying the accepted legacy artifact."""

    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    if ids != tuple(_feature_ids_from_artifact(thermal.POLICY_PATH)):
        raise ValueError("TD-C corrected analysis requires the frozen 58-feature identity")
    legacy_path = Path(legacy_analysis_artifact).resolve()
    if legacy_path != root / "analysis.json":
        raise ValueError("TD-C corrected analysis requires the root legacy analysis")
    legacy = _load_json(legacy_path)
    if (
        _sha256(legacy_path)
        != "a4f4303b391c6eca5bf4a59fd1e95bf1b505b28bad4eda1c081f5d54d98a6aa0"
        or legacy.get("status") != "td_c_core_pass_waiting_for_planner"
        or legacy.get("capture_count") != 8
    ):
        raise ValueError("TD-C corrected analysis requires the accepted immutable legacy artifact")
    rows = _load_jsonl(root / "captures.jsonl")
    sessions: dict[int, dict[str, Any]] = defaultdict(dict)
    for row in rows:
        step = row.get("plan_step")
        if not isinstance(step, Mapping) or step.get("state_id") != "A":
            raise ValueError("TD-C corrected analysis requires the accepted A core captures")
        session_index = int(step["session_index"])
        source = str(step["source_id"])
        sessions[session_index][source] = _unit(
            _features(row, ids), ids,
        )
        if int(step["source_order"]) == 1:
            sessions[session_index]["order"] = f"{source}_first"
    if tuple(sorted(sessions)) != (1, 2, 3, 4) or any(
        set(session) != {"ray", "strip", "order"} for session in sessions.values()
    ):
        raise ValueError("TD-C corrected analysis requires four exact paired sessions")

    ray_variance = _same_state_variance(source="ray", state="A")
    strip_variance = _same_state_variance(source="strip", state="A")
    ray = [sessions[index]["ray"] for index in sorted(sessions)]
    strip = [sessions[index]["strip"] for index in sorted(sessions)]
    offsets = [strip[index] - ray[index] for index in range(4)]
    ray_null_center = np.mean(np.vstack(ray), axis=0)
    strip_null_center = np.mean(np.vstack(strip), axis=0)
    cross_source_zero_null_center = np.mean(
        np.vstack([ray_null_center, strip_null_center]), axis=0,
    )

    def pairwise(
        values: Sequence[np.ndarray],
        *,
        terms_for_pair: Callable[[int, int], Sequence[tuple[np.ndarray, np.ndarray, float]]],
        covariance: np.ndarray,
    ) -> list[dict[str, Any]]:
        output = []
        for left in range(4):
            for right in range(left + 1, 4):
                output.append({
                    "left_session": left + 1,
                    "right_session": right + 1,
                    **_td_c_contrast_diagnostic(
                        values[right] - values[left], covariance,
                        terms=terms_for_pair(left, right),
                    ),
                })
        return output

    ray_pairs = pairwise(
        ray,
        covariance=2.0 * ray_variance,
        terms_for_pair=lambda left, right: (
            (ray_null_center, ray_variance, 1.0),
            (ray_null_center, ray_variance, -1.0),
        ),
    )
    strip_pairs = pairwise(
        strip,
        covariance=2.0 * strip_variance,
        terms_for_pair=lambda left, right: (
            (strip_null_center, strip_variance, 1.0),
            (strip_null_center, strip_variance, -1.0),
        ),
    )
    offset_pairs = pairwise(
        offsets,
        covariance=2.0 * (ray_variance + strip_variance),
        terms_for_pair=lambda left, right: (
            (strip_null_center, strip_variance, 1.0),
            (ray_null_center, ray_variance, -1.0),
            (strip_null_center, strip_variance, -1.0),
            (ray_null_center, ray_variance, 1.0),
        ),
    )
    ray_first_indices = [
        index for index in range(4)
        if sessions[index + 1]["order"] == "ray_first"
    ]
    strip_first_indices = [
        index for index in range(4)
        if sessions[index + 1]["order"] == "strip_first"
    ]
    if len(ray_first_indices) != 2 or len(strip_first_indices) != 2:
        raise ValueError("TD-C corrected analysis requires two sessions per source order")
    order_value = np.mean(np.vstack([offsets[i] for i in strip_first_indices]), axis=0) - np.mean(
        np.vstack([offsets[i] for i in ray_first_indices]), axis=0,
    )
    order_terms = [
        (strip_null_center, strip_variance, coefficient)
        for indices, coefficient in ((strip_first_indices, 0.5), (ray_first_indices, -0.5))
        for index in indices
    ] + [
        (ray_null_center, ray_variance, -coefficient)
        for indices, coefficient in ((strip_first_indices, 0.5), (ray_first_indices, -0.5))
        for index in indices
    ]
    order = _td_c_contrast_diagnostic(
        order_value, ray_variance + strip_variance, terms=order_terms,
    )
    mean_offset = np.mean(np.vstack(offsets), axis=0)
    absolute_terms = [
        term
        for index in range(4)
        for term in (
            (cross_source_zero_null_center, strip_variance, 0.25),
            (cross_source_zero_null_center, ray_variance, -0.25),
        )
    ]
    absolute = _td_c_contrast_diagnostic(
        mean_offset, (ray_variance + strip_variance) / 4.0,
        terms=absolute_terms, zero_is_gate=False,
    )
    observed_scores = {
        "ray_pair_maximum": max(row["score"] for row in ray_pairs),
        "strip_pair_maximum": max(row["score"] for row in strip_pairs),
        "paired_offset_pair_maximum": max(row["score"] for row in offset_pairs),
        "source_order": float(order["score"]),
    }
    expected_scores_match = all(
        math.isclose(
            observed_scores[name], expected,
            rel_tol=0.0, abs_tol=TD_C_CORE_EXPECTED_SCORE_ABS_TOLERANCE,
        )
        for name, expected in TD_C_CORE_EXPECTED_SCORES.items()
    )
    passes = (
        all(
            row["decision"] == "pass"
            for row in (*ray_pairs, *strip_pairs, *offset_pairs)
        )
        and order["decision"] == "pass"
        and absolute["decision"] == "fail"
        and expected_scores_match
    )
    return {
        "schema": TD_C_CORE_CONTRAST_SCHEMA,
        "status": "canonical_pass" if passes else "advisor_recheck_required",
        "legacy_status": str(legacy["status"]),
        "refined_status": (
            TD_C_CORE_CONTRAST_CLASSIFICATION
            if passes else "td_c_core_corrected_estimand_pattern_mismatch"
        ),
        "legacy_analysis": {
            "path": str(legacy_path), "sha256": _sha256(legacy_path), "immutable": True,
        },
        "capture_count": 8,
        "ray_center_pairwise": {
            "covariance": "2*Sigma_R", "rows": ray_pairs,
            "maximum_score": observed_scores["ray_pair_maximum"],
        },
        "strip_center_pairwise": {
            "covariance": "2*Sigma_S_A", "rows": strip_pairs,
            "maximum_score": observed_scores["strip_pair_maximum"],
        },
        "paired_offset_pairwise": {
            "definition": "d_i=strip_i-ray_i",
            "covariance": "2*(Sigma_R+Sigma_S_A)", "rows": offset_pairs,
            "maximum_score": observed_scores["paired_offset_pair_maximum"],
        },
        "source_order_contrast": {
            "definition": "mean(strip_first_d)-mean(ray_first_d)",
            "covariance": "Sigma_R+Sigma_S_A", **order,
        },
        "absolute_offset": {
            "definition": "mean(strip_i-ray_i)",
            "covariance": "(Sigma_R+Sigma_S_A)/4",
            "mean_d_by_feature": {
                feature_id: float(mean_offset[index])
                for index, feature_id in enumerate(ids)
            },
            **absolute,
            "warm_A_cross_source_offset_estimable": True,
            "warm_A_cross_source_offset_repeatable": all(
                row["decision"] == "pass" for row in offset_pairs
            ),
            "warm_A_cross_source_match": False,
        },
        "measurement_contract": {
            "observer": "frozen", "feature_count": len(ids),
            "coverage": 0.9973, "source_level_monte_carlo": True,
            "difference_vector_used_as_unit_center": False,
            "steady_claim": False, "P6_comparison": "locked",
        },
        "advisor_expected_score_regression": {
            "expected": TD_C_CORE_EXPECTED_SCORES,
            "observed": observed_scores,
            "absolute_tolerance": TD_C_CORE_EXPECTED_SCORE_ABS_TOLERANCE,
            "status": "pass" if expected_scores_match else "fail",
        },
        "locks": {
            "fast_B_C_endpoint_holdout": not passes,
            "legacy_td_c_expansion": True,
            "solver_sentinel_and_later": True,
        },
    }


def analyze_ambient_trend(ambients: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not ambients:
        return {"status": "fail", "reason": "missing_ambient_evidence"}
    payloads = [(row.get("capture") or {}).get("ambient_diagnostic") or row.get("ambient_diagnostic") for row in ambients]
    if any(not isinstance(value, Mapping) for value in payloads):
        return {"status": "fail", "reason": "invalid_ambient_diagnostic"}
    geometry = {str(value.get("geometry_hash")) for value in payloads}
    black = np.asarray([value.get("black_levels") for value in payloads], dtype=float)
    if black.ndim != 2 or np.any(~np.isfinite(black)):
        return {"status": "fail", "reason": "invalid_black_level_provenance"}
    tolerance = min(float(value.get("black_level_tolerance_dn", 0.0)) for value in payloads)
    span = float(np.max(np.ptp(black, axis=0)))
    passed = len(geometry) == 1 and span <= tolerance
    return {
        "status": "pass" if passed else "fail", "geometry_hash_count": len(geometry),
        "black_level_max_span_dn": span, "black_level_tolerance_dn": tolerance,
    }


def _features(row: Mapping[str, Any], feature_ids: Sequence[str]) -> Mapping[str, float]:
    values = row.get("feature_values") or (row.get("capture") or {}).get("feature_values")
    if not isinstance(values, Mapping) or set(values) != set(feature_ids):
        raise ValueError("thermal capture lacks exact frozen feature provenance")
    return {key: float(values[key]) for key in feature_ids}


def _unit(row: Mapping[str, float], feature_ids: Sequence[str]) -> np.ndarray:
    return ordered_unit_shape(row, feature_ids)


def _same_state_variance(*, source: str, state: str) -> np.ndarray:
    policy = _load_json(thermal.POLICY_PATH)
    if source == "ray":
        variance = np.asarray(
            policy["reference_policy"]["ray_within_state_diagonal_variance"],
            dtype=float,
        )
    else:
        class_name = {
            "A": "sat100_fullscale", "D": "mid_sat_fullscale",
            "B": "neutral_fullscale", "C": "sat100_fullscale",
        }[state]
        variance = np.asarray(
            policy["repeatability_policy"]["classes"][class_name]["p1_floor_diagonal_variance"],
            dtype=float,
        )
    return variance


def _same_state_pair_variance(*, source: str, state: str) -> np.ndarray:
    return 2.0 * _same_state_variance(source=source, state=state)


def frozen_same_state_compatibility_diagnostic(
    left: Sequence[float], right: Sequence[float], *,
    source: str, state: str, feature_ids: Sequence[str],
) -> dict[str, Any]:
    pair_variance = _same_state_pair_variance(source=source, state=state)
    if pair_variance.shape != (len(feature_ids),):
        raise ValueError("frozen same-state covariance differs from feature contract")
    left_values = np.asarray(left, dtype=float)
    right_values = np.asarray(right, dtype=float)
    limits = calibrate_direct_limits(left_values, pair_variance, samples=1000)
    score = direct_whitened_norm(right_values - left_values, pair_variance)
    passed = score <= float(limits["guarded_limit"])
    return {
        "statistic": str(limits["statistic"]),
        "score": score,
        "guarded_limit": float(limits["guarded_limit"]),
        "unguarded_limit": float(limits["unguarded_limit"]),
        "decision": "pass" if passed else "fail",
    }


def _r6_state_chronology_diagnostic(
    points: Mapping[int, Sequence[Mapping[str, float]]],
    feature_ids: Sequence[str],
    *, source: str, state: str,
) -> dict[str, Any]:
    expected_points = tuple(thermal.TIMED_POINTS)
    if tuple(sorted(points)) != expected_points or any(len(points[point]) != 1 for point in expected_points):
        raise ValueError("Ray R6 chronology requires one 60/120/300/600 capture per switched state")
    ordered_features = [points[point][0] for point in expected_points]
    normalized = np.vstack([_unit(features, feature_ids) for features in ordered_features])
    chronology_axis = np.linspace(-0.5, 0.5, len(normalized))
    centered = normalized - np.mean(normalized, axis=0)
    slope = (chronology_axis @ centered) / float(chronology_axis @ chronology_axis)
    dominant_index = int(np.argmax(np.abs(slope)))
    variance = _same_state_variance(source=source, state=state)
    if variance.shape != (len(feature_ids),):
        raise ValueError("frozen chronology covariance differs from feature contract")
    trend_score = direct_whitened_norm(slope, variance)
    energy = np.sum(centered * centered / variance, axis=1)
    total_energy = float(np.sum(energy))
    dominance = (
        0.0 if total_energy <= 0.0
        else float(np.max(energy) / total_energy)
    )
    trend_limit = float(thermal.AUDIT_THRESHOLDS["trend_whitened_limit"])
    dominance_limit = float(
        thermal.AUDIT_THRESHOLDS["maximum_single_frame_variance_fraction"]
    )
    return {
        "elapsed_s": list(expected_points),
        "normalized_feature_values": [
            {feature_id: float(row[index]) for index, feature_id in enumerate(feature_ids)}
            for row in normalized
        ],
        "trend": {
            "score": trend_score,
            "limit": trend_limit,
            "decision": "pass" if trend_score <= trend_limit else "fail",
            "hard_gate_for_operational_600": False,
        },
        "dominance": {
            "maximum_single_frame_variance_fraction": dominance,
            "limit": dominance_limit,
            "decision": "pass" if dominance <= dominance_limit else "fail",
            "hard_gate_for_operational_600": False,
        },
        "direction": {
            "semantics": "least_squares_slope_over_ordered_60_120_300_600_unit_shapes",
            "slope_by_feature": {
                feature_id: float(slope[index])
                for index, feature_id in enumerate(feature_ids)
            },
            "dominant_feature_id": str(feature_ids[dominant_index]),
            "dominant_signed_slope": float(slope[dominant_index]),
            "l2": float(np.linalg.norm(slope)),
        },
        "audit_status": (
            "pass"
            if trend_score <= trend_limit and dominance <= dominance_limit
            else "scientific_chronology_signal_present"
        ),
        "covariance": "frozen_same_state_per_capture_diagonal_variance",
    }


def frozen_same_state_compatibility(
    *, source: str, feature_ids: Sequence[str], state: str = "A",
) -> Callable[[Sequence[float], Sequence[float]], bool]:
    def compatible(left: Sequence[float], right: Sequence[float]) -> bool:
        diagnostic = frozen_same_state_compatibility_diagnostic(
            left, right, source=source, state=state, feature_ids=feature_ids,
        )
        return diagnostic["decision"] == "pass"

    return compatible


def compare_current_ray_center_to_p6(
    captures: Sequence[Mapping[str, Any]], feature_ids: Sequence[str],
) -> dict[str, Any]:
    manifold = RayHsiManifold.load(thermal.MANIFOLD_PATH)
    p6 = load_ray_repeat_groups(manifold, DEFAULT_P6_RUN)
    output = {}
    compatibility = frozen_same_state_compatibility(source="ray", feature_ids=feature_ids)
    state_coordinates = {"A": (120, 100), "B": (0, 0), "C": (300, 100), "D": (120, 50)}
    for state in sorted({str(row["plan_step"]["state_id"]) for row in captures}):
        current = np.mean(np.vstack([
            _unit(_features(row, feature_ids), feature_ids)
            for row in captures if row["source_id"] == "ray" and row["plan_step"]["state_id"] == state
        ]), axis=0)
        hue, sat = state_coordinates[state]
        frozen_rows = p6[f"p6:h{hue}:s{sat}"]
        frozen = np.mean(np.asarray(frozen_rows, dtype=float), axis=0)
        output[state] = {"decision": "pass" if compatibility(frozen, current) else "fail"}
    return {"status": "pass" if all(item["decision"] == "pass" for item in output.values()) else "fail", "states": output}


def _feature_ids_from_artifact(path: Path) -> list[str]:
    artifact = _load_json(path)
    ids = artifact.get("feature_set", {}).get("ids") or artifact.get("ids")
    if not isinstance(ids, list) or not ids or any(not isinstance(item, str) or not item for item in ids):
        raise ValueError("thermal feature file lacks a non-empty string ID list")
    return ids


def _write_text_atomic(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(value, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_json_value(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"missing or unreadable JSON artifact: {path}") from exc
    if not text.strip():
        raise ValueError(f"empty JSON artifact: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON artifact: {path}") from exc


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _formal_groups(
    experiment_id: str, captures: Sequence[Mapping[str, Any]],
) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if not step.get("formal_measurement"):
            continue
        key = thermal.timing_sequence_identity(experiment_id, step)
        if groups:
            previous = groups[-1][0]
            previous_key = thermal.timing_sequence_identity(experiment_id, previous)
        else:
            previous_key = None
        if groups and key == previous_key and float(step["requested_elapsed_s"]) > float(groups[-1][-1]["requested_elapsed_s"]):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def _guarded_zero_diagnostic(
    value: np.ndarray, variance: np.ndarray, *, center: np.ndarray,
) -> dict[str, Any]:
    if value.shape != variance.shape or np.any(variance <= 0.0):
        raise ValueError("Ray history contrast covariance differs from the feature contract")
    limits = calibrate_direct_limits(center, variance, samples=1000)
    score = direct_whitened_norm(value, variance)
    limit = float(limits["guarded_limit"])
    return {
        "score": score, "guarded_limit": limit,
        "decision": "detected" if score > limit else "compatible_with_zero",
    }


def analyze_ray_history_experiment(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
    r6_vector_artifact: str | Path | None,
    source: str = "ray",
) -> dict[str, Any]:
    """Classify one frozen 3x3 history experiment without pooling R6 frames."""
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    frozen_ids = tuple(_feature_ids_from_artifact(thermal.POLICY_PATH))
    if ids != frozen_ids:
        raise ValueError("history analysis requires the frozen 58-feature identity")
    if source not in {"ray", "strip"}:
        raise ValueError("history analysis source must be ray or strip")
    drift_path: Path | None = None
    drift_artifact: Mapping[str, Any] = {}
    if source == "ray":
        if r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires the frozen R6 direction artifact")
        drift_path = Path(r6_vector_artifact).resolve()
        drift_artifact = _load_json(drift_path)
        direction_map = drift_artifact.get("r6_drift_direction", {}).get("values_by_feature")
        whitening = drift_artifact.get("common_whitening", {})
        if (
            drift_artifact.get("scientific_interpretation", {}).get("r6_formal_pass") is not False
            or drift_artifact.get("scientific_interpretation", {}).get("r6_reclassification_allowed") is not False
            or not isinstance(direction_map, Mapping)
            or tuple(direction_map) != ids
            or tuple(whitening.get("feature_ids", ())) != ids
        ):
            raise ValueError("Ray history analysis requires the frozen negative-R6 direction artifact")
        direction = np.asarray([direction_map[name] for name in ids], dtype=float)
        if not np.all(np.isfinite(direction)) or not math.isclose(
            float(np.linalg.norm(direction)), 1.0, rel_tol=1e-8, abs_tol=1e-8,
        ):
            raise ValueError("frozen R6 drift direction is not a finite unit vector")
        pair_variance = np.asarray(whitening.get("diagonal_variance"), dtype=float)
    else:
        direction = np.zeros(len(ids), dtype=float)
        pair_variance = _same_state_pair_variance(source="strip", state="A")
    expected_pair_variance = _same_state_pair_variance(source=source, state="A")
    if pair_variance.shape != (len(ids),) or not np.allclose(
        pair_variance, expected_pair_variance, rtol=0.0, atol=0.0,
    ):
        raise ValueError("history common whitening differs from the frozen source covariance")

    observations: list[dict[str, Any]] = []
    baseline_centers: list[np.ndarray] = []
    session_artifacts: list[dict[str, Any]] = []
    for session_index in (1, 2, 3):
        session_root = root / f"session-{session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        run = _load_json(session_root / "run.json")
        builder = (
            thermal.build_ray_history_session_spec
            if source == "ray" else thermal.build_strip_history_session_spec
        )
        expected = builder(
            session_index, device_control_enabled=True,
            session_start_condition=plan.get("session_start_condition"),
        )
        if plan != expected:
            raise ValueError("Ray history session differs from its exact cyclic design")
        _validate_required_execution_artifacts(session_root)
        _validate_reproducibility_checkpoint(session_root, plan, run)
        captures = _load_jsonl(session_root / "captures.jsonl")
        physical = _load_jsonl(session_root / "physical-returns.jsonl")
        _validate_run_counts(run, plan, captures, physical)
        _validate_physical_rows(session_root, captures, physical)
        _validate_commands_and_gates(plan, session_root)
        _validate_cleanup_and_wrapper(session_root)
        quality = _load_json(session_root / "quality.json")
        if (
            quality.get("schema") not in {
                "guide4_ray_history_session_quality_v1",
                "guide5_strip_history_session_quality_v1",
            }
            or quality.get("status") != "pass"
            or quality.get("session_index") != session_index
            or quality.get("capture_count") != 7
        ):
            raise ValueError("Ray history session quality artifact did not pass")
        by_role: dict[str, Mapping[str, Any]] = {}
        for row, expected_step in zip(captures, expected["captures"], strict=True):
            capture = row.get("capture")
            step = row.get("plan_step")
            if (
                not isinstance(capture, Mapping)
                or not isinstance(step, Mapping)
                or dict(step) != dict(expected_step)
                or str(row.get("capture_id")) != expected_step["capture_id"]
            ):
                raise ValueError("Ray history capture differs from its exact session spec")
            values = capture.get("feature_values")
            if (
                not isinstance(values, Mapping)
                or tuple(values) != ids
                or any(
                    isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(float(value)) for value in values.values()
                )
            ):
                raise ValueError("Ray history capture lacks the frozen feature vector")
            direct_quality = capture.get("direct_quality")
            if (
                not isinstance(direct_quality, Mapping)
                or direct_quality.get("status") != "pass"
                or direct_quality.get("feature_count") != len(ids)
            ):
                raise ValueError("Ray history capture quality did not pass")
            _validate_recorded_exposure(capture, str(expected_step["nominal_shutter"]))
            if source == "ray":
                strip_zero = capture.get("strip_zero_before_capture")
                requested_zero = (
                    strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
                )
                observed_zero = (
                    strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
                )
                if (
                    not isinstance(requested_zero, Mapping)
                    or any(int(value) != 0 for value in requested_zero.values())
                    or not isinstance(observed_zero, Mapping)
                    or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
                ):
                    raise ValueError("Ray history capture lacks verified strip-zero evidence")
            else:
                ray_zero = capture.get("ray_zero_before_capture")
                if not isinstance(ray_zero, Mapping):
                    raise ValueError("strip history capture lacks verified Ray-zero evidence")
            if expected_step["role"] in {"initial_anchor", "return_anchor"}:
                by_role[str(expected_step["anchor_label"])] = values
        baseline = _unit(by_role["A0"], ids)
        baseline_centers.append(baseline)
        for position, predecessor in enumerate(expected["session_order"], start=1):
            label = f"A_after_{predecessor}"
            delta = _unit(by_role[label], ids) - baseline
            whitened_delta = delta / np.sqrt(pair_variance)
            projection = float(whitened_delta @ direction)
            orthogonal = whitened_delta - projection * direction
            observations.append({
                "session": session_index, "position": position,
                "predecessor": predecessor, "delta": delta,
                "whitened_delta": whitened_delta,
                "projection": projection,
                "orthogonal_norm": float(np.linalg.norm(orthogonal)),
            })
        session_artifacts.append({
            "session": session_index, "root": str(session_root),
            "order": expected["session_order"], "quality_sha256": _sha256(session_root / "quality.json"),
        })

    # Treatment coding: intercept, session 2/3, position 2/3, predecessor B/C.
    design = np.asarray([
        [
            1.0,
            float(row["session"] == 2), float(row["session"] == 3),
            float(row["position"] == 2), float(row["position"] == 3),
            float(row["predecessor"] == "B"), float(row["predecessor"] == "C"),
        ]
        for row in observations
    ])
    response = np.vstack([row["delta"] for row in observations])
    calibration_center = np.mean(np.vstack(baseline_centers), axis=0)
    response_covariance = np.eye(9)
    for left in range(9):
        for right in range(9):
            if left != right and observations[left]["session"] == observations[right]["session"]:
                response_covariance[left, right] = 0.5
    covariance_inverse = np.linalg.inv(response_covariance)
    information = design.T @ covariance_inverse @ design
    coefficient_covariance = np.linalg.inv(information)
    coefficients = coefficient_covariance @ design.T @ covariance_inverse @ response
    fitted = design @ coefficients
    residuals = response - fitted

    def contrast(name: str, vector: Sequence[float]) -> dict[str, Any]:
        row = np.asarray(vector, dtype=float)
        effect = row @ coefficients
        variance_scalar = float(row @ coefficient_covariance @ row)
        diagnostic = _guarded_zero_diagnostic(
            effect, variance_scalar * pair_variance, center=calibration_center,
        )
        return {
            "name": name,
            "projection_on_r6_direction": float(
                (effect / np.sqrt(pair_variance)) @ direction
            ),
            "variance_scalar_relative_to_one_delta": variance_scalar,
            **diagnostic,
        }

    contrasts = {
        "common_warm_reentry_effect": contrast(
            "common_warm_reentry_effect", (1, 0, 0, 0, 0, 0, 0),
        ),
        "position_2_minus_1": contrast("position_2_minus_1", (0, 0, 0, 1, 0, 0, 0)),
        "position_3_minus_2": contrast("position_3_minus_2", (0, 0, 0, -1, 1, 0, 0)),
        "C_minus_D": contrast("C_minus_D", (0, 0, 0, 0, 0, 0, 1)),
        "C_minus_B": contrast("C_minus_B", (0, 0, 0, 0, 0, -1, 1)),
        "B_minus_D": contrast("B_minus_D", (0, 0, 0, 0, 0, 1, 0)),
    }
    position_projections = [
        0.0,
        float((coefficients[3] / np.sqrt(pair_variance)) @ direction),
        float((coefficients[4] / np.sqrt(pair_variance)) @ direction),
    ]
    period_detected = (
        position_projections[0] < position_projections[1] < position_projections[2]
        and all(
            contrasts[name]["decision"] == "detected"
            for name in ("position_2_minus_1", "position_3_minus_2")
        )
    )
    c_detected = all(
        contrasts[name]["decision"] == "detected"
        for name in ("C_minus_D", "C_minus_B")
    )
    other_state_effect = contrasts["B_minus_D"]["decision"] == "detected"
    orthogonal_large = any(
        _guarded_zero_diagnostic(
            (row["whitened_delta"] - row["projection"] * direction)
            * np.sqrt(pair_variance),
            pair_variance,
            center=calibration_center,
        )["decision"] == "detected"
        for row in observations
    )
    residual_large = False
    residual_rows = []
    residual_maker = np.eye(9) - design @ coefficient_covariance @ design.T @ covariance_inverse
    residual_covariance = residual_maker @ response_covariance @ residual_maker.T
    for index, residual in enumerate(residuals):
        variance_scalar = max(float(residual_covariance[index, index]), 1e-15)
        diagnostic = _guarded_zero_diagnostic(
            residual, variance_scalar * pair_variance, center=calibration_center,
        )
        residual_large |= diagnostic["decision"] == "detected"
        residual_rows.append({
            "session": observations[index]["session"],
            "position": observations[index]["position"],
            "predecessor": observations[index]["predecessor"],
            **diagnostic,
        })
    return_compatible = all(
        _guarded_zero_diagnostic(
            row["delta"], pair_variance, center=calibration_center,
        )["decision"]
        == "compatible_with_zero"
        for row in observations
    )
    nonlinear = residual_large or orthogonal_large or other_state_effect
    if nonlinear:
        classification = "nonlinear/non-additive"
    elif period_detected and c_detected:
        classification = "mixed"
    elif period_detected:
        classification = "period-only"
    elif c_detected:
        classification = "C-carryover-only"
    elif return_compatible:
        classification = "R6-not-reproduced"
    else:
        classification = "nonlinear/non-additive"
    return {
        "schema": "guide4_ray_history_order_balanced_analysis_v1",
        "status": "classified_waiting_advisor_review",
        "experiment_id": (
            thermal.RAY_HISTORY_3X3_EXPERIMENT_ID
            if source == "ray" else thermal.STRIP_HISTORY_3X3_EXPERIMENT_ID
        ),
        "classification": classification,
        "r6_formal_result_preserved": "valid_scientific_negative",
        "r6_frames_pooled": False,
        "frozen_r6_direction": (
            {
                "artifact": str(drift_path), "sha256": _sha256(drift_path),
                "direction_sha256": drift_artifact["r6_drift_direction"]["sha256"],
            }
            if source == "ray" else None
        ),
        "measurement_contract": {
            "feature_count": len(ids), "observer": "frozen",
            "operational_dwell_s": thermal.RAY_HISTORY_OPERATIONAL_DWELL_S,
            "thermal_error": "human_accepted_to_reduce_time_and_power",
            "steady_or_settled_claim": False,
            "covariance": "frozen_ray_within_state_diagonal_with_shared_A0_block_covariance",
            "guarded_coverage": "frozen_direct_limits",
        },
        "sessions": session_artifacts,
        "model": {
            "formula": "return_anchor_delta = session + sequence_position + immediate_predecessor_state + residual",
            "observation_count": 9, "parameter_count": 7, "residual_degrees_of_freedom": 2,
            "position_projections_on_r6_direction": position_projections,
            "contrasts": contrasts, "residuals": residual_rows,
        },
        "diagnostics": {
            "period_detected": period_detected, "C_carryover_detected": c_detected,
            "other_state_effect_detected": other_state_effect,
            "large_orthogonal_residual": orthogonal_large,
            "orthogonal_to_frozen_r6_direction_detected": orthogonal_large,
            "additive_model_rejected": residual_large,
            "all_return_deltas_compatible_with_zero": return_compatible,
        },
        "locks": {
            "strip": True, "combined_td_b": True, "td_c": True,
            "sentinel_and_later": True, "until": "classification_review_complete",
        },
    }


def analyze_ray_history_experiment_v2(
    experiment_root: str | Path,
    *, feature_ids: Sequence[str], r6_vector_artifact: str | Path | None,
    source: str = "ray",
) -> dict[str, Any]:
    """Derive the Advisor-5 common-reentry classification without changing v1 evidence."""
    legacy = analyze_ray_history_experiment(
        experiment_root, feature_ids=feature_ids,
        r6_vector_artifact=r6_vector_artifact,
        source=source,
    )
    diagnostics = legacy["diagnostics"]
    contrasts = legacy["model"]["contrasts"]
    additive_residual = bool(diagnostics["additive_model_rejected"])
    period = bool(diagnostics["period_detected"])
    predecessor = bool(
        diagnostics["C_carryover_detected"]
        or diagnostics["other_state_effect_detected"]
    )
    common = contrasts["common_warm_reentry_effect"]["decision"] == "detected"
    raw_compatible = bool(diagnostics["all_return_deltas_compatible_with_zero"])
    if additive_residual:
        classification = "interaction_or_nonadditive_unresolved"
    elif common and not period and not predecessor:
        classification = "common_warm_reentry_shift"
    elif period or predecessor:
        classification = "additive_period_or_carryover_effect"
    elif raw_compatible:
        classification = "no_history_effect_detected"
    else:
        classification = "underpowered_or_unclassified"
    original = Path(experiment_root).resolve() / "analysis.json"
    return {
        "schema": "guide4_ray_history_order_balanced_analysis_v2",
        "status": "classified_waiting_advisor_review",
        "experiment_id": legacy["experiment_id"],
        "legacy_classification": legacy["classification"],
        "classification": classification,
        "r6_rank1_direction_transfer": "rejected" if source == "ray" else "not_applicable",
        "r6_frames_pooled": False,
        "original_analysis_sha256": _sha256(original) if original.is_file() else None,
        "frozen_r6_direction": legacy["frozen_r6_direction"],
        "measurement_contract": legacy["measurement_contract"],
        "sessions": legacy["sessions"],
        "model": legacy["model"],
        "diagnostics": {
            "common_warm_reentry_detected": common,
            "period_main_effect_detected": period,
            "predecessor_main_effect_detected": predecessor,
            "additive_model_rejected": additive_residual,
            "nonlinear_interaction_demonstrated": additive_residual,
            "raw_return_deltas_compatible_with_zero": raw_compatible,
            "orthogonal_to_frozen_r6_direction_detected": bool(
                diagnostics["orthogonal_to_frozen_r6_direction_detected"]
            ),
        },
        "locks": {
            "strip_history_only": classification != "common_warm_reentry_shift",
            "combined_td_b": True, "td_c": True,
            "sentinel_and_later": True,
            "until": "advisor_review_complete",
        },
    }


def analyze_strip_history_experiment_v3(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
    legacy_analysis_artifact: str | Path,
) -> dict[str, Any]:
    """Correct the GUIDE5 common estimand while preserving the v2 artifact."""
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    legacy = analyze_ray_history_experiment_v2(
        root,
        feature_ids=ids,
        r6_vector_artifact=None,
        source="strip",
    )
    legacy_path = Path(legacy_analysis_artifact).resolve()
    legacy_artifact = _load_json(legacy_path)
    if (
        legacy_artifact.get("schema") != "guide4_ray_history_order_balanced_analysis_v2"
        or legacy_artifact.get("experiment_id") != legacy["experiment_id"]
        or legacy_artifact.get("classification") != legacy["classification"]
    ):
        raise ValueError("GUIDE5 v3 requires the exact matching immutable v2 artifact")

    observations: list[dict[str, Any]] = []
    baseline_centers: list[np.ndarray] = []
    for session_index in (1, 2, 3):
        session_root = root / f"session-{session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        captures = _load_jsonl(session_root / "captures.jsonl")
        by_role = {
            str(row["plan_step"]["anchor_label"]): row["capture"]["feature_values"]
            for row in captures
            if row["plan_step"]["role"] in {"initial_anchor", "return_anchor"}
        }
        baseline = _unit(by_role["A0"], ids)
        baseline_centers.append(baseline)
        for position, predecessor in enumerate(plan["session_order"], start=1):
            observations.append({
                "session": session_index,
                "position": position,
                "predecessor": predecessor,
                "delta": _unit(by_role[f"A_after_{predecessor}"], ids) - baseline,
            })

    design = np.asarray([
        [
            1.0,
            float(row["session"] == 2), float(row["session"] == 3),
            float(row["position"] == 2), float(row["position"] == 3),
            float(row["predecessor"] == "B"), float(row["predecessor"] == "C"),
        ]
        for row in observations
    ])
    response = np.vstack([row["delta"] for row in observations])
    response_covariance = np.eye(9)
    for left in range(9):
        for right in range(9):
            if left != right and observations[left]["session"] == observations[right]["session"]:
                response_covariance[left, right] = 0.5
    covariance_inverse = np.linalg.inv(response_covariance)
    information = design.T @ covariance_inverse @ design
    coefficient_covariance = np.linalg.inv(information)
    coefficients = coefficient_covariance @ design.T @ covariance_inverse @ response
    pair_variance = _same_state_pair_variance(source="strip", state="A")
    calibration_center = np.mean(np.vstack(baseline_centers), axis=0)

    def corrected_contrast(name: str, vector: Sequence[float]) -> dict[str, Any]:
        row = np.asarray(vector, dtype=float)
        variance_scalar = float(row @ coefficient_covariance @ row)
        return {
            "name": name,
            "coefficient_vector": [float(value) for value in row],
            "variance_scalar_relative_to_one_delta": variance_scalar,
            **_guarded_zero_diagnostic(
                row @ coefficients,
                variance_scalar * pair_variance,
                center=calibration_center,
            ),
        }

    balanced = corrected_contrast(
        "balanced_common_warm_reentry_effect",
        (1.0, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3),
    )
    session_contrasts = {
        "session2_minus_session1": corrected_contrast(
            "session2_minus_session1", (0, 1, 0, 0, 0, 0, 0),
        ),
        "session3_minus_session1": corrected_contrast(
            "session3_minus_session1", (0, 0, 1, 0, 0, 0, 0),
        ),
        "session3_minus_session2": corrected_contrast(
            "session3_minus_session2", (0, -1, 1, 0, 0, 0, 0),
        ),
    }
    raw_return_deltas = [
        {
            "session": int(row["session"]),
            "position": int(row["position"]),
            "predecessor": str(row["predecessor"]),
            "variance_scalar_relative_to_one_delta": 1.0,
            **_guarded_zero_diagnostic(
                row["delta"], pair_variance, center=calibration_center,
            ),
        }
        for row in observations
    ]

    diagnostics = legacy["diagnostics"]
    common_detected = balanced["decision"] == "detected"
    session_heterogeneity = any(
        item["decision"] == "detected" for item in session_contrasts.values()
    )
    if (
        common_detected
        and not diagnostics["period_main_effect_detected"]
        and not diagnostics["predecessor_main_effect_detected"]
        and not diagnostics["additive_model_rejected"]
    ):
        classification = (
            "common_warm_reentry_shift_with_session_block_heterogeneity"
            if session_heterogeneity
            else "common_warm_reentry_shift"
        )
        guide5_parent_branch = "S-A"
    else:
        classification = legacy["classification"]
        guide5_parent_branch = None

    return {
        "schema": "guide5_strip_history_order_balanced_analysis_v3",
        "status": "accepted_advisor_corrected_classification",
        "experiment_id": legacy["experiment_id"],
        "advisor_decision": "OPTION_3_CORRECT_THE_COMMON_CONTRAST",
        "analyzer_source": {
            "path": str(Path(__file__).resolve()),
            "sha256": _sha256(Path(__file__).resolve()),
        },
        "legacy_analysis_artifact": {
            "path": str(legacy_path),
            "sha256": _sha256(legacy_path),
            "classification": legacy["classification"],
            "immutable": True,
        },
        "legacy_classification": legacy["classification"],
        "corrected_classification": classification,
        "classification": classification,
        "guide5_parent_branch": guide5_parent_branch,
        "incorrect_legacy_common_estimand": "treatment_coded_baseline_cell_intercept",
        "correct_balanced_common_contrast": (
            "beta0 + (session2 + session3 + position2 + position3 "
            "+ predecessorB + predecessorC) / 3"
        ),
        "balanced_common_variance_scalar_relative_to_one_delta": (
            balanced["variance_scalar_relative_to_one_delta"]
        ),
        "balanced_common_score": balanced["score"],
        "balanced_common_guarded_limit": balanced["guarded_limit"],
        "balanced_common_decision": balanced["decision"],
        "balanced_common_contrast": balanced,
        "session_contrasts": session_contrasts,
        "session3_minus_session2_score": session_contrasts[
            "session3_minus_session2"
        ]["score"],
        "session_contrast_guarded_limit": session_contrasts[
            "session3_minus_session2"
        ]["guarded_limit"],
        "raw_return_deltas": raw_return_deltas,
        "model": legacy["model"],
        "legacy_diagnostics": diagnostics,
        "diagnostics": {
            "balanced_common_warm_reentry_detected": common_detected,
            "period_main_effect_detected": diagnostics["period_main_effect_detected"],
            "predecessor_main_effect_detected": (
                diagnostics["predecessor_main_effect_detected"]
            ),
            "additive_model_rejected": diagnostics["additive_model_rejected"],
            "nonlinear_interaction_demonstrated": diagnostics[
                "nonlinear_interaction_demonstrated"
            ],
            "raw_return_deltas_compatible_with_zero": diagnostics[
                "raw_return_deltas_compatible_with_zero"
            ],
            "session_block_heterogeneity_detected": session_heterogeneity,
            "cross_session_warm_center_frozen": not session_heterogeneity,
        },
        "scientific_interpretation": {
            "strip_fast_history_structure": "conditionally_accepted",
            "initial_vs_warm_split": "demonstrated" if common_detected else "not_detected",
            "predecessor_specific_split": "not_demonstrated",
            "position_specific_split": "not_demonstrated",
            "nonadditive_interaction": "not_demonstrated",
            "session_block_cause": "unknown",
            "new_strip_acquisition_required_now": False,
        },
        "locks": {
            "ray_fast_long_bridge": classification != (
                "common_warm_reentry_shift_with_session_block_heterogeneity"
            ),
            "combined_td_b": True,
            "td_c": True,
            "strip_solver": True,
            "sentinel_and_later": True,
        },
    }


def analyze_ray_fast_long_bridge(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
) -> dict[str, Any]:
    """Classify the four required GUIDE5 Ray fast/long holdout mini-sessions."""
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    if ids != tuple(_feature_ids_from_artifact(thermal.POLICY_PATH)):
        raise ValueError("Ray fast/long bridge requires the frozen 58-feature identity")

    sessions: dict[tuple[str, str], dict[str, Any]] = {}
    session_artifacts = []
    prerequisite_sha256: str | None = None
    for mini_session_index in range(1, 5):
        session_root = root / f"mini-session-{mini_session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        prerequisite = plan.get("scientific_prerequisite")
        expected = thermal.build_ray_fast_long_bridge_session_spec(
            mini_session_index,
            device_control_enabled=True,
            session_start_condition=plan.get("session_start_condition"),
            scientific_prerequisite=(
                prerequisite if isinstance(prerequisite, Mapping) else None
            ),
        )
        if plan != expected:
            raise ValueError("Ray fast/long bridge mini-session differs from exact design")
        if not isinstance(prerequisite, Mapping):
            raise ValueError("Ray fast/long bridge lacks strip analyzer-v3 prerequisite")
        if prerequisite_sha256 is None:
            prerequisite_sha256 = str(prerequisite.get("sha256"))
        elif prerequisite.get("sha256") != prerequisite_sha256:
            raise ValueError("Ray fast/long bridge crossed strip analyzer-v3 identities")
        run = _load_json(session_root / "run.json")
        _validate_required_execution_artifacts(session_root)
        _validate_reproducibility_checkpoint(session_root, plan, run)
        captures = _load_jsonl(session_root / "captures.jsonl")
        physical = _load_jsonl(session_root / "physical-returns.jsonl")
        _validate_run_counts(run, plan, captures, physical)
        _validate_physical_rows(session_root, captures, physical)
        _validate_commands_and_gates(plan, session_root)
        _validate_cleanup_and_wrapper(session_root)
        quality = _load_json(session_root / "quality.json")
        if (
            quality.get("schema") != "guide5_ray_fast_long_bridge_session_quality_v1"
            or quality.get("status") != "pass"
            or quality.get("capture_count") != 3
            or quality.get("mini_session_index") != mini_session_index
            or quality.get("bridge_state") != plan["bridge_state"]
            or quality.get("bridge_protocol") != plan["bridge_protocol"]
        ):
            raise ValueError("Ray fast/long bridge mini-session quality did not pass")
        by_role = {}
        for row, expected_step in zip(captures, expected["captures"], strict=True):
            capture = row.get("capture")
            step = row.get("plan_step")
            if (
                not isinstance(capture, Mapping)
                or not isinstance(step, Mapping)
                or dict(step) != dict(expected_step)
            ):
                raise ValueError("Ray fast/long bridge capture differs from its spec")
            values = capture.get("feature_values")
            if (
                not isinstance(values, Mapping)
                or tuple(values) != ids
                or any(
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    for value in values.values()
                )
            ):
                raise ValueError("Ray fast/long bridge capture lacks frozen features")
            _validate_recorded_exposure(capture, str(expected_step["nominal_shutter"]))
            by_role[str(expected_step["role"])] = _unit(values, ids)
        sessions[(str(plan["bridge_state"]), str(plan["bridge_protocol"]))] = {
            "A0": by_role["initial_anchor"],
            "Q": by_role["bridge_state"],
            "A_return": by_role["return_anchor"],
        }
        session_artifacts.append({
            "mini_session_index": mini_session_index,
            "state": plan["bridge_state"],
            "protocol": plan["bridge_protocol"],
            "reset_s": plan["reset_s"],
            "operational_dwell_s": plan["operational_dwell_s"],
            "root": str(session_root),
            "quality_sha256": _sha256(session_root / "quality.json"),
        })

    state_results = {}
    protocol_vectors: dict[str, dict[str, np.ndarray]] = {
        "Q_center": {}, "A_return": {}, "return_delta": {},
    }
    any_protocol_bias = False
    for state in ("C", "B"):
        fast = sessions[(state, "FAST")]
        long = sessions[(state, "LONG")]
        a_variance = _same_state_variance(source="ray", state="A")
        q_variance = _same_state_variance(source="ray", state=state)

        def diagnostic(
            value: np.ndarray, variance: np.ndarray, center: np.ndarray,
        ) -> dict[str, Any]:
            return _guarded_zero_diagnostic(value, variance, center=center)

        fast_return_delta = fast["A_return"] - fast["A0"]
        long_return_delta = long["A_return"] - long["A0"]
        q_difference = long["Q"] - fast["Q"]
        a_return_difference = long["A_return"] - fast["A_return"]
        protocol_difference = long_return_delta - fast_return_delta
        diagnostics = {
            "fast_A_return_minus_A0": diagnostic(
                fast_return_delta, 2.0 * a_variance,
                (fast["A_return"] + fast["A0"]) / 2.0,
            ),
            "long_A_return_minus_A0": diagnostic(
                long_return_delta, 2.0 * a_variance,
                (long["A_return"] + long["A0"]) / 2.0,
            ),
            "long_minus_fast_Q_center": diagnostic(
                q_difference, 2.0 * q_variance,
                (long["Q"] + fast["Q"]) / 2.0,
            ),
            "long_minus_fast_A_return": diagnostic(
                a_return_difference, 2.0 * a_variance,
                (long["A_return"] + fast["A_return"]) / 2.0,
            ),
            "matched_pair_protocol_difference": diagnostic(
                protocol_difference, 4.0 * a_variance,
                np.mean(np.vstack((fast["A0"], fast["A_return"], long["A0"], long["A_return"])), axis=0),
            ),
        }
        protocol_vectors["Q_center"][state] = q_difference
        protocol_vectors["A_return"][state] = a_return_difference
        protocol_vectors["return_delta"][state] = protocol_difference
        any_protocol_bias |= any(
            item["decision"] == "detected"
            for name, item in diagnostics.items()
            if name.startswith("long_minus_fast") or name == "matched_pair_protocol_difference"
        )
        state_results[state] = diagnostics

    a_variance = _same_state_variance(source="ray", state="A")
    b_variance = _same_state_variance(source="ray", state="B")
    c_variance = _same_state_variance(source="ray", state="C")
    centers = {
        "Q_center": np.mean(
            np.vstack([row["Q"] for row in sessions.values()]), axis=0,
        ),
        "A_return": np.mean(
            np.vstack([row["A_return"] for row in sessions.values()]), axis=0,
        ),
        "return_delta": np.mean(
            np.vstack([
                row["A0"] for row in sessions.values()
            ] + [
                row["A_return"] for row in sessions.values()
            ]),
            axis=0,
        ),
    }
    common_variances = {
        "Q_center": (b_variance + c_variance) / 2.0,
        "A_return": a_variance,
        "return_delta": 2.0 * a_variance,
    }
    state_variances = {
        "Q_center": 2.0 * b_variance + 2.0 * c_variance,
        "A_return": 4.0 * a_variance,
        "return_delta": 8.0 * a_variance,
    }
    common_diagnostics = {}
    state_dependent_diagnostics = {}
    for name, vectors in protocol_vectors.items():
        common_diagnostics[name] = _guarded_zero_diagnostic(
            (vectors["B"] + vectors["C"]) / 2.0,
            common_variances[name],
            center=centers[name],
        )
        state_dependent_diagnostics[name] = _guarded_zero_diagnostic(
            vectors["B"] - vectors["C"],
            state_variances[name],
            center=centers[name],
        )
    if any(
        item["decision"] == "detected"
        for item in state_dependent_diagnostics.values()
    ):
        classification = "state_dependent_protocol_bias_detected"
    elif any(
        item["decision"] == "detected" for item in common_diagnostics.values()
    ) or any_protocol_bias:
        classification = "common_protocol_bias_detected"
    else:
        classification = "thermal_bias_not_detected"
    return {
        "schema": "guide5_ray_fast_long_bridge_analysis_v1",
        "status": "classified_waiting_advisor_review",
        "experiment_id": thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
        "classification": classification,
        "capture_count": 12,
        "mini_session_count": 4,
        "long_session_count": 2,
        "strip_analyzer_v3_sha256": prerequisite_sha256,
        "sessions": session_artifacts,
        "states": state_results,
        "common_bias_compatibility": common_diagnostics,
        "state_dependent_bias_compatibility": state_dependent_diagnostics,
        "measurement_contract": {
            "observer": "frozen",
            "feature_count": len(ids),
            "covariance": "frozen_per_capture_diagonal",
            "guarded_coverage": "frozen_direct_limits",
            "long_data_role": "holdout_only",
            "fast_target_training": False,
            "covariance_change": False,
            "steady_or_settled_claim": False,
        },
        "locks": {
            "combined_td_b": True,
            "td_c": True,
            "strip_solver": True,
            "sentinel_and_later": True,
            "until": "advisor_review_complete",
        },
    }


def _bridge_session_vectors(
    experiment_root: str | Path, feature_ids: Sequence[str],
) -> dict[tuple[str, str], dict[str, np.ndarray]]:
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    sessions: dict[tuple[str, str], dict[str, np.ndarray]] = {}
    for mini_session_index in range(1, 5):
        session_root = root / f"mini-session-{mini_session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        rows = _load_jsonl(session_root / "captures.jsonl")
        by_role = {
            str(row["plan_step"]["role"]): _unit(
                row["capture"]["feature_values"], ids,
            )
            for row in rows
        }
        sessions[(str(plan["bridge_state"]), str(plan["bridge_protocol"]))] = {
            "A0": by_role["initial_anchor"],
            "Q": by_role["bridge_state"],
            "A_return": by_role["return_anchor"],
        }
    return sessions


def analyze_ray_fast_long_bridge_v2(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
    legacy_analysis_artifact: str | Path,
) -> dict[str, Any]:
    """Apply the Advisor-approved local-anchor Q contrast to immutable bridge data."""
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    canonical_v1 = analyze_ray_fast_long_bridge(root, feature_ids=ids)
    legacy_path = Path(legacy_analysis_artifact).resolve()
    legacy = _load_json(legacy_path)
    if (
        legacy.get("schema") != "guide5_ray_fast_long_bridge_analysis_v1"
        or legacy.get("classification") != canonical_v1["classification"]
        or legacy.get("capture_count") != 12
    ):
        raise ValueError("bridge v2 requires the matching immutable v1 artifact")
    sessions = _bridge_session_vectors(root, ids)
    local_differences: dict[str, np.ndarray] = {}
    a0_differences: dict[str, np.ndarray] = {}
    state_results: dict[str, Any] = {}
    for state in ("B", "C"):
        fast = sessions[(state, "FAST")]
        long = sessions[(state, "LONG")]
        local_fast = fast["Q"] - (fast["A0"] + fast["A_return"]) / 2.0
        local_long = long["Q"] - (long["A0"] + long["A_return"]) / 2.0
        local_difference = local_long - local_fast
        a0_difference = long["A0"] - fast["A0"]
        local_differences[state] = local_difference
        a0_differences[state] = a0_difference
        a_variance = _same_state_variance(source="ray", state="A")
        q_variance = _same_state_variance(source="ray", state=state)
        state_results[state] = {
            "A0_protocol_difference": _guarded_zero_diagnostic(
                a0_difference,
                2.0 * a_variance,
                center=(long["A0"] + fast["A0"]) / 2.0,
            ),
            "Q_local_anchor_protocol_difference": _guarded_zero_diagnostic(
                local_difference,
                2.0 * q_variance + a_variance,
                center=np.mean(np.vstack(tuple(fast.values()) + tuple(long.values())), axis=0),
            ),
            "A_reentry_displacement_protocol_difference": canonical_v1[
                "states"
            ][state]["matched_pair_protocol_difference"],
        }
    state_contrast = _guarded_zero_diagnostic(
        local_differences["B"] - local_differences["C"],
        2.0 * _same_state_variance(source="ray", state="B")
        + 2.0 * _same_state_variance(source="ray", state="C")
        + 2.0 * _same_state_variance(source="ray", state="A"),
        center=np.mean(np.vstack(list(local_differences.values())), axis=0),
    )
    expected = (
        state_results["B"]["Q_local_anchor_protocol_difference"]["decision"]
        == "compatible_with_zero"
        and state_results["C"]["Q_local_anchor_protocol_difference"]["decision"]
        == "detected"
        and state_contrast["decision"] == "detected"
    )
    return {
        "schema": "guide5_ray_fast_long_bridge_analysis_v2",
        "status": "accepted_advisor_refined_holdout" if expected else "advisor_recheck_required",
        "experiment_id": thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
        "parent_class": "state_dependent_protocol_bias_detected",
        "classification": (
            "state_dependent_Q_center_protocol_bias_detected_on_B_C_holdout"
            if expected else "local_anchor_detection_pattern_mismatch"
        ),
        "legacy_analysis_artifact": {
            "path": str(legacy_path), "sha256": _sha256(legacy_path),
            "immutable": True,
        },
        "capture_count": 12,
        "states": state_results,
        "state_contrast_of_Q_local_anchor_protocol_difference": state_contrast,
        "measurement_contract": {
            **canonical_v1["measurement_contract"],
            "fast_long_pooling": False,
            "common_fast_to_long_transfer": False,
            "extrapolation_beyond_B_C": False,
        },
        "locks": {
            "combined_td_b_offline": not expected,
            "td_c": True,
            "strip_solver": True,
            "sentinel_and_later": True,
        },
    }


def _history_local_coordinates(
    experiment_root: str | Path, *, source: str, feature_ids: Sequence[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    builder = (
        thermal.build_ray_history_session_spec
        if source == "ray" else thermal.build_strip_history_session_spec
    )
    observations: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for session_index in (1, 2, 3):
        session_root = root / f"session-{session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        expected = builder(
            session_index, device_control_enabled=True,
            session_start_condition=plan.get("session_start_condition"),
        )
        if plan != expected:
            raise ValueError(f"combined TD-B {source} session differs from exact FAST design")
        quality = _load_json(session_root / "quality.json")
        if quality.get("status") != "pass" or quality.get("capture_count") != 7:
            raise ValueError(f"combined TD-B {source} session quality did not pass")
        rows = _load_jsonl(session_root / "captures.jsonl")
        by_label = {
            str(row["plan_step"]["anchor_label"]): _unit(
                row["capture"]["feature_values"], ids,
            )
            for row in rows
        }
        for position, state in enumerate(expected["session_order"], start=1):
            observations.append({
                "session": session_index,
                "position": position,
                "state": state,
                "coordinate": by_label[state] - by_label[f"A_after_{state}"],
            })
        evidence.append({
            "session": session_index,
            "root": str(session_root),
            "order": expected["session_order"],
            "quality_sha256": _sha256(session_root / "quality.json"),
            "captures_sha256": _sha256(session_root / "captures.jsonl"),
        })
    return observations, evidence


def analyze_combined_fast_history_coordinate(
    ray_root: str | Path,
    strip_root: str | Path,
    *,
    feature_ids: Sequence[str],
    ray_history_analysis_artifact: str | Path,
    ray_analysis_artifact: str | Path,
    strip_analysis_artifact: str | Path,
) -> dict[str, Any]:
    """Compare matched FAST Ray/strip local coordinates without pooling centers."""
    ids = tuple(feature_ids)
    if ids != tuple(_feature_ids_from_artifact(thermal.POLICY_PATH)):
        raise ValueError("combined TD-B requires the frozen 58-feature identity")
    ray_history_analysis_path = Path(ray_history_analysis_artifact).resolve()
    ray_analysis_path = Path(ray_analysis_artifact).resolve()
    strip_analysis_path = Path(strip_analysis_artifact).resolve()
    ray_history_analysis = _load_json(ray_history_analysis_path)
    ray_analysis = _load_json(ray_analysis_path)
    strip_analysis = _load_json(strip_analysis_path)
    if (
        ray_history_analysis.get("schema")
        != "guide4_ray_history_order_balanced_analysis_v2"
        or ray_history_analysis.get("classification") != "common_warm_reentry_shift"
        or ray_analysis.get("schema") != "guide5_ray_fast_long_bridge_analysis_v2"
        or ray_analysis.get("status") != "accepted_advisor_refined_holdout"
        or strip_analysis.get("schema") != "guide5_strip_history_order_balanced_analysis_v3"
        or strip_analysis.get("classification")
        != "common_warm_reentry_shift_with_session_block_heterogeneity"
    ):
        raise ValueError("combined TD-B requires accepted bridge-v2 and strip-v3 evidence")
    ray, ray_evidence = _history_local_coordinates(
        ray_root, source="ray", feature_ids=ids,
    )
    strip, strip_evidence = _history_local_coordinates(
        strip_root, source="strip", feature_ids=ids,
    )
    identities = [(row["session"], row["position"], row["state"]) for row in ray]
    if identities != [(row["session"], row["position"], row["state"]) for row in strip]:
        raise ValueError("combined TD-B Ray/strip Latin-square cell identities differ")
    response = np.vstack([
        strip_row["coordinate"] - ray_row["coordinate"]
        for ray_row, strip_row in zip(ray, strip, strict=True)
    ])
    design = np.asarray([
        [
            1.0, float(row["session"] == 2), float(row["session"] == 3),
            float(row["position"] == 2), float(row["position"] == 3),
            float(row["state"] == "B"), float(row["state"] == "C"),
        ]
        for row in ray
    ])
    variances = np.vstack([
        _same_state_variance(source="strip", state=row["state"])
        + _same_state_variance(source="strip", state="A")
        + _same_state_variance(source="ray", state=row["state"])
        + _same_state_variance(source="ray", state="A")
        for row in ray
    ])
    coefficients = np.empty((7, len(ids)))
    coefficient_variances = np.empty((7, 7, len(ids)))
    fitted = np.empty_like(response)
    for feature_index in range(len(ids)):
        weights = np.diag(1.0 / variances[:, feature_index])
        covariance = np.linalg.inv(design.T @ weights @ design)
        beta = covariance @ design.T @ weights @ response[:, feature_index]
        coefficients[:, feature_index] = beta
        coefficient_variances[:, :, feature_index] = covariance
        fitted[:, feature_index] = design @ beta
    center = np.mean(np.vstack([
        row["coordinate"] for row in ray + strip
    ]), axis=0)

    def model_contrast(name: str, vector: Sequence[float]) -> dict[str, Any]:
        contrast_row = np.asarray(vector, dtype=float)
        effect = contrast_row @ coefficients
        variance = np.asarray([
            contrast_row @ coefficient_variances[:, :, index] @ contrast_row
            for index in range(len(ids))
        ])
        return {"name": name, **_guarded_zero_diagnostic(effect, variance, center=center)}

    session = {
        "session2_minus_session1": model_contrast("session2_minus_session1", (0, 1, 0, 0, 0, 0, 0)),
        "session3_minus_session1": model_contrast("session3_minus_session1", (0, 0, 1, 0, 0, 0, 0)),
        "session3_minus_session2": model_contrast("session3_minus_session2", (0, -1, 1, 0, 0, 0, 0)),
    }
    position = {
        "position2_minus_position1": model_contrast("position2_minus_position1", (0, 0, 0, 1, 0, 0, 0)),
        "position3_minus_position1": model_contrast("position3_minus_position1", (0, 0, 0, 0, 1, 0, 0)),
        "position3_minus_position2": model_contrast("position3_minus_position2", (0, 0, 0, -1, 1, 0, 0)),
    }
    state = {
        "B_minus_D": model_contrast("B_minus_D", (0, 0, 0, 0, 0, 1, 0)),
        "C_minus_D": model_contrast("C_minus_D", (0, 0, 0, 0, 0, 0, 1)),
        "C_minus_B": model_contrast("C_minus_B", (0, 0, 0, 0, 0, -1, 1)),
    }
    residuals = []
    for row_index, row in enumerate(ray):
        residuals.append({
            "session": row["session"], "position": row["position"], "state": row["state"],
            **_guarded_zero_diagnostic(
                response[row_index] - fitted[row_index], variances[row_index], center=center,
            ),
        })
    gate_pass = all(
        item["decision"] == "compatible_with_zero"
        for item in [*session.values(), *position.values(), *residuals]
    )
    return {
        "schema": "p7_combined_fast_history_coordinate_v1",
        "experiment_id": "combined_td_b",
        "status": "canonical_pass" if gate_pass else "canonical_scientific_fail",
        "classification": (
            "fast_local_anchor_coordinate_compatible_for_paired_source_comparison"
            if gate_pass else "fast_local_anchor_coordinate_block_or_residual_incompatible"
        ),
        "routine_envelope": "fast_op120_reset600_v1",
        "observation_count": 9,
        "source_capture_count": 42,
        "long_input_count": 0,
        "coordinate": "d=(Q_strip-A_after_Q_strip)-(Q_ray-A_after_Q_ray)",
        "absolute_cross_source_A_anchor": "not_yet_established",
        "evidence": {
            "ray_sessions": ray_evidence, "strip_sessions": strip_evidence,
            "ray_history_analysis": {"path": str(ray_history_analysis_path), "sha256": _sha256(ray_history_analysis_path)},
            "ray_analysis": {"path": str(ray_analysis_path), "sha256": _sha256(ray_analysis_path)},
            "strip_analysis": {"path": str(strip_analysis_path), "sha256": _sha256(strip_analysis_path)},
        },
        "model": {
            "formula": "d=session_block+position_block+state+residual",
            "session_contrasts": session,
            "position_contrasts": position,
            "state_terms_not_gated_at_zero": state,
            "additive_residuals": residuals,
        },
        "gate": {
            "evidence_identity": "pass", "no_pooling": "pass",
            "session": "pass" if all(v["decision"] == "compatible_with_zero" for v in session.values()) else "fail",
            "position": "pass" if all(v["decision"] == "compatible_with_zero" for v in position.values()) else "fail",
            "additive_residual": "pass" if all(v["decision"] == "compatible_with_zero" for v in residuals) else "fail",
        },
        "locks": {
            "td_c_core": not gate_pass,
            "td_c_expansion": True,
            "strip_solver": True,
            "sentinel_and_later": True,
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze P7 thermal diagnostics or derive P7-R1 epoch-v2 evidence.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--feature-ids", type=Path)
    parser.add_argument("--derive-r1-output", type=Path)
    parser.add_argument("--revalidate-exposure-failure", action="store_true")
    parser.add_argument("--validator-commit")
    parser.add_argument("--r6-vector-reanalysis-output", type=Path)
    parser.add_argument("--source-bundle-sha256")
    parser.add_argument("--source-bundle-member")
    parser.add_argument("--analyzer-commit")
    parser.add_argument("--ray-history-analysis", action="store_true")
    parser.add_argument("--ray-history-analysis-v2", action="store_true")
    parser.add_argument("--ray-history-analysis-v3", action="store_true")
    parser.add_argument("--ray-history-analysis-output", type=Path)
    parser.add_argument("--history-source", choices=("ray", "strip"), default="ray")
    parser.add_argument("--r6-vector-artifact", type=Path)
    parser.add_argument("--legacy-history-analysis-artifact", type=Path)
    parser.add_argument("--ray-fast-long-bridge-analysis", action="store_true")
    parser.add_argument("--ray-fast-long-bridge-analysis-output", type=Path)
    parser.add_argument("--ray-fast-long-bridge-analysis-v2", action="store_true")
    parser.add_argument("--legacy-bridge-analysis-artifact", type=Path)
    parser.add_argument("--combined-fast-history-analysis", action="store_true")
    parser.add_argument("--ray-history-root", type=Path)
    parser.add_argument("--strip-history-root", type=Path)
    parser.add_argument("--ray-history-analysis-artifact", type=Path)
    parser.add_argument("--bridge-v2-analysis-artifact", type=Path)
    parser.add_argument("--strip-v3-analysis-artifact", type=Path)
    parser.add_argument("--combined-fast-history-analysis-output", type=Path)
    parser.add_argument("--td-c-core-contrasts-v2-1", action="store_true")
    parser.add_argument("--legacy-td-c-core-analysis-artifact", type=Path)
    parser.add_argument("--td-c-core-contrasts-output", type=Path)
    parser.add_argument("--td-c-endpoint-decomposition", action="store_true")
    parser.add_argument("--td-c-endpoint-exact-context-v3", action="store_true")
    parser.add_argument("--td-c-endpoint-exact-context-v4", action="store_true")
    parser.add_argument("--td-c-endpoint-decomposition-output", type=Path)
    parser.add_argument("--td-c-endpoint-analysis-artifact", type=Path)
    parser.add_argument("--td-c-core-contrasts-artifact", type=Path)
    parser.add_argument("--td-c-combined-artifact", type=Path)
    parser.add_argument("--td-c-r6-root", type=Path)
    parser.add_argument("--guide6-seed-negative-root2", type=Path)
    parser.add_argument("--guide6-seed-negative-output", type=Path)
    parser.add_argument("--guide8-emission-exposure-output", type=Path)
    parser.add_argument("--guide8-exposure-policy-output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.guide8_emission_exposure_output is not None:
        analysis, policy = write_guide8_analysis_and_policy(
            args.run_dir,
            analysis_output=args.guide8_emission_exposure_output,
            policy_output=(
                thermal.GUIDE8_EXPOSURE_POLICY_V2_PATH
                if args.guide8_exposure_policy_output is None
                else args.guide8_exposure_policy_output
            ),
        )
        print(analysis)
        if policy is not None:
            print(policy)
        return 0
    if args.guide6_seed_negative_output is not None:
        if args.guide6_seed_negative_root2 is None:
            raise ValueError("GUIDE6 seed-negative derivation requires root2")
        output = args.guide6_seed_negative_output.resolve()
        if output.exists():
            raise FileExistsError("GUIDE6 seed-negative output is immutable and already exists")
        report = analyze_guide6_seed_negative(args.run_dir, args.guide6_seed_negative_root2)
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if args.derive_r1_output is not None:
        paths = write_reference_epoch_v2_derived(args.run_dir, args.derive_r1_output)
        print("\n".join(str(path) for path in paths))
        return 0
    if args.feature_ids is None:
        raise ValueError("--feature-ids is required for thermal run analysis")
    feature_ids = _feature_ids_from_artifact(args.feature_ids)
    if args.td_c_endpoint_exact_context_v4:
        required = (
            args.td_c_endpoint_analysis_artifact,
            args.td_c_core_contrasts_artifact,
            args.td_c_combined_artifact,
            args.td_c_endpoint_decomposition_output,
        )
        if any(value is None for value in required):
            raise ValueError("TD-C exact-context v4 requires endpoint, core, combined and output paths")
        output = args.td_c_endpoint_decomposition_output.resolve()
        if output.exists():
            raise FileExistsError("TD-C exact-context v4 output is immutable and already exists")
        report = analyze_td_c_fast_endpoint_exact_context_v4(
            args.run_dir,
            feature_ids=feature_ids,
            endpoint_analysis_artifact=args.td_c_endpoint_analysis_artifact,
            core_contrast_artifact=args.td_c_core_contrasts_artifact,
            combined_artifact=args.td_c_combined_artifact,
        )
        _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
        print(output)
        return 0
    if args.td_c_endpoint_exact_context_v3:
        required = (
            args.td_c_endpoint_analysis_artifact,
            args.td_c_core_contrasts_artifact,
            args.td_c_combined_artifact,
            args.td_c_endpoint_decomposition_output,
        )
        if any(value is None for value in required):
            raise ValueError("TD-C exact-context v3 requires endpoint, core, combined and output paths")
        output = args.td_c_endpoint_decomposition_output.resolve()
        if output.exists():
            raise FileExistsError("TD-C exact-context v3 output is immutable and already exists")
        report = analyze_td_c_fast_endpoint_exact_context_v3(
            args.run_dir,
            feature_ids=feature_ids,
            endpoint_analysis_artifact=args.td_c_endpoint_analysis_artifact,
            core_contrast_artifact=args.td_c_core_contrasts_artifact,
            combined_artifact=args.td_c_combined_artifact,
        )
        _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
        print(output)
        return 0
    if args.td_c_endpoint_decomposition:
        required = (
            args.td_c_endpoint_analysis_artifact,
            args.td_c_core_contrasts_artifact,
            args.td_c_combined_artifact,
            args.td_c_r6_root,
            args.td_c_endpoint_decomposition_output,
        )
        if any(value is None for value in required):
            raise ValueError("TD-C endpoint decomposition requires endpoint, core, combined, R6 and output paths")
        output = args.td_c_endpoint_decomposition_output.resolve()
        if output.exists():
            raise FileExistsError("TD-C endpoint decomposition output is immutable and already exists")
        report = analyze_td_c_fast_endpoint_decomposition(
            args.run_dir,
            feature_ids=feature_ids,
            endpoint_analysis_artifact=args.td_c_endpoint_analysis_artifact,
            core_contrast_artifact=args.td_c_core_contrasts_artifact,
            combined_artifact=args.td_c_combined_artifact,
            r6_root=args.td_c_r6_root,
        )
        _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
        print(output)
        return 0
    if args.td_c_core_contrasts_v2_1:
        if (
            args.legacy_td_c_core_analysis_artifact is None
            or args.td_c_core_contrasts_output is None
        ):
            raise ValueError("TD-C core contrasts v2.1 requires legacy analysis and output")
        output = args.td_c_core_contrasts_output.resolve()
        if output.exists():
            raise FileExistsError("TD-C core contrasts output is immutable and already exists")
        report = analyze_td_c_core_contrasts_v2_1(
            args.run_dir,
            feature_ids=feature_ids,
            legacy_analysis_artifact=args.legacy_td_c_core_analysis_artifact,
        )
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if args.combined_fast_history_analysis:
        required = (
            args.ray_history_root, args.strip_history_root,
            args.ray_history_analysis_artifact,
            args.bridge_v2_analysis_artifact, args.strip_v3_analysis_artifact,
            args.combined_fast_history_analysis_output,
        )
        if any(value is None for value in required):
            raise ValueError("combined FAST history analysis requires both roots, both analyses, and output")
        report = analyze_combined_fast_history_coordinate(
            args.ray_history_root, args.strip_history_root,
            feature_ids=feature_ids,
            ray_history_analysis_artifact=args.ray_history_analysis_artifact,
            ray_analysis_artifact=args.bridge_v2_analysis_artifact,
            strip_analysis_artifact=args.strip_v3_analysis_artifact,
        )
        _write_text_atomic(
            args.combined_fast_history_analysis_output.resolve(),
            json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(args.combined_fast_history_analysis_output.resolve())
        return 0
    if args.ray_fast_long_bridge_analysis_v2:
        if args.legacy_bridge_analysis_artifact is None or args.ray_fast_long_bridge_analysis_output is None:
            raise ValueError("bridge v2 requires immutable v1 artifact and output")
        report = analyze_ray_fast_long_bridge_v2(
            args.run_dir, feature_ids=feature_ids,
            legacy_analysis_artifact=args.legacy_bridge_analysis_artifact,
        )
        _write_text_atomic(
            args.ray_fast_long_bridge_analysis_output.resolve(),
            json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(args.ray_fast_long_bridge_analysis_output.resolve())
        return 0
    if args.ray_fast_long_bridge_analysis:
        output = args.ray_fast_long_bridge_analysis_output
        if output is None:
            raise ValueError(
                "Ray fast/long bridge analysis requires "
                "--ray-fast-long-bridge-analysis-output"
            )
        report = analyze_ray_fast_long_bridge(
            args.run_dir, feature_ids=feature_ids,
        )
        _write_text_atomic(
            output.resolve(), json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output.resolve())
        return 0
    if sum((
        args.ray_history_analysis,
        args.ray_history_analysis_v2,
        args.ray_history_analysis_v3,
    )) > 1:
        raise ValueError("v1, v2 and v3 Ray history analysis are mutually exclusive")
    if args.ray_history_analysis_v3:
        if args.history_source != "strip":
            raise ValueError("GUIDE5 v3 history correction is strip-only")
        if args.legacy_history_analysis_artifact is None:
            raise ValueError("v3 history analysis requires --legacy-history-analysis-artifact")
        output = args.ray_history_analysis_output
        if output is None:
            raise ValueError("v3 history analysis requires --ray-history-analysis-output")
        report = analyze_strip_history_experiment_v3(
            args.run_dir,
            feature_ids=feature_ids,
            legacy_analysis_artifact=args.legacy_history_analysis_artifact,
        )
        _write_text_atomic(
            output.resolve(), json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output.resolve())
        return 0
    if args.ray_history_analysis_v2:
        if args.history_source == "ray" and args.r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires --r6-vector-artifact")
        output = args.ray_history_analysis_output
        if output is None:
            raise ValueError("v2 Ray history analysis requires --ray-history-analysis-output")
        report = analyze_ray_history_experiment_v2(
            args.run_dir, feature_ids=feature_ids,
            r6_vector_artifact=args.r6_vector_artifact,
            source=args.history_source,
        )
        _write_text_atomic(
            output.resolve(), json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output.resolve())
        return 0
    if args.ray_history_analysis:
        if args.r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires --r6-vector-artifact")
        report = analyze_ray_history_experiment(
            args.run_dir, feature_ids=feature_ids,
            r6_vector_artifact=args.r6_vector_artifact,
        )
        output = args.run_dir.resolve() / "analysis.json"
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if args.r6_vector_artifact is not None:
        raise ValueError("--r6-vector-artifact requires --ray-history-analysis")
    if args.r6_vector_reanalysis_output is not None:
        if args.revalidate_exposure_failure or args.validator_commit is not None:
            raise ValueError("R6 vector reanalysis does not rerun exposure revalidation")
        if (
            args.analyzer_commit is None
            or len(args.analyzer_commit) != 40
            or any(character not in "0123456789abcdef" for character in args.analyzer_commit)
        ):
            raise ValueError("R6 vector reanalysis requires an exact analyzer commit")
        report = analyze_r6_anchor_vectors(
            args.run_dir,
            feature_ids=feature_ids,
            source_bundle_sha256=args.source_bundle_sha256,
            source_bundle_member=args.source_bundle_member,
            analyzer_commit=args.analyzer_commit,
        )
        output = args.r6_vector_reanalysis_output.resolve()
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if (
        args.source_bundle_sha256 is not None
        or args.source_bundle_member is not None
        or args.analyzer_commit is not None
    ):
        raise ValueError("source bundle identity requires --r6-vector-reanalysis-output")
    if args.revalidate_exposure_failure:
        if args.validator_commit is None:
            raise ValueError("--validator-commit is required for post-fix revalidation")
        revalidation_path = args.run_dir.resolve() / POST_FIX_REVALIDATION_FILE
        if revalidation_path.exists():
            retained = _validate_post_fix_revalidation(
                args.run_dir.resolve(), _load_json(args.run_dir.resolve() / "run.json"),
            )
            if retained.get("validator_commit") != args.validator_commit:
                raise ValueError("retained revalidation belongs to a different validator commit")
        else:
            revalidate_direct_ray_r6_exposure_failure(
                args.run_dir,
                feature_ids=feature_ids,
                validator_commit=args.validator_commit,
            )
    elif args.validator_commit is not None:
        raise ValueError("--validator-commit requires --revalidate-exposure-failure")
    report = analyze_thermal_run(
        args.run_dir,
        feature_ids=feature_ids,
        post_fix_revalidation=args.revalidate_exposure_failure,
    )
    output = args.run_dir / "analysis.json"
    _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
