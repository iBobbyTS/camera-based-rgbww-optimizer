from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.measurement.chart_response_basis import CHANNELS
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import (
    FrozenHsiUncertaintyEvaluator,
    feature_ids_sha256,
    target_kind,
    validate_uncertainty_artifact,
)
from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    HsiPolicyV2,
    conservative_class_variance,
    evaluate_confirmation_spread,
    evaluate_reference_difference,
    summarize_within_block,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.optimization.hsi_budget import (
    HsiPhysicalBudget,
    HsiPhysicalBudgetExhausted,
    HsiSolverBudgetLimits,
)
from camera_based_rgbww_optimizer.optimization.hsi_feedback import (
    HsiMeasurementRejected,
    run_hsi_feedback,
    run_hsi_feedback_multiseed,
)
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    HsiRejectedFeaturesError,
    P7_RESULT_STATUSES,
    evaluate_hsi_observation,
    evaluate_hsi_observation_v2,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
from camera_based_rgbww_optimizer.optimization.measure_cct_multipatch_pilot import WeakSignalEnvelopeExhausted
from camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold import _verify_readback
from camera_based_rgbww_optimizer.optimization.multipatch_solver import solve_piecewise_basis_seed
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "strip-hsi-pilot"
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-pilot.json"
DEFAULT_V2_CONFIG = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-pilot-v2.json"
DEFAULT_MANIFOLD_CONFIG = PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_UNCERTAINTY_CONFIG = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-uncertainty.json"
DEFAULT_POLICY_V2_CONFIG = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-policy-v2-waiting.json"
DEFAULT_BASIS_ANALYSIS = Path(
    "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/"
    "p2-five-channel-basis-20260716-005935/basis-analysis.json"
)
FROZEN_BASIS_SHA256 = "5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1"
FROZEN_MANIFOLD_SHA256 = "20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34"
LATEST_LOCATION_SHA256 = "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"
EXPECTED_TARGET_COUNT = 13
TARGET_SET_COUNTS = {"sentinel": 4, "remaining": 9}
TARGET_SET_NAMES = ("sentinel", "remaining", "boundary", "holdout")


class ReferenceDriftError(RuntimeError):
    pass


def build_strip_hsi_pilot_plan(
    *,
    config_path: str | Path | None = None,
    manifold_config_path: str | Path = DEFAULT_MANIFOLD_CONFIG,
    basis_analysis_path: str | Path = DEFAULT_BASIS_ANALYSIS,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    uncertainty_config_path: str | Path = DEFAULT_UNCERTAINTY_CONFIG,
    policy_v2_config_path: str | Path = DEFAULT_POLICY_V2_CONFIG,
    curve_path: str | Path = esphome.DEFAULT_CURVE_PATH,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    camera_backend: str = "remote",
    target_set: str = "sentinel",
    parent_analysis_path: str | Path | None = None,
    target_file_path: str | Path | None = None,
    policy_version: str | None = None,
) -> dict[str, Any]:
    if policy_version not in {"v1", "v2"}:
        raise ValueError("P7 runner requires explicit policy_version=v1 or v2")
    config_path = Path(config_path) if config_path is not None else (
        DEFAULT_V2_CONFIG if policy_version == "v2" else DEFAULT_CONFIG
    )
    if camera_backend != "remote":
        raise ValueError("new P7 experiments require camera_backend=remote")
    config_ref = _file_reference(Path(config_path))
    config = _load_json(Path(config_path))
    if config.get("schema_version") != 2 or config.get("phase") != "P7-pilot" or config.get("branch") != "full_periodic_2d_HB":
        raise ValueError("P7 pilot config must freeze the full_periodic_2d_HB branch")
    if policy_version == "v2":
        _validate_solver_budget_config(config["solver"])
    if target_set not in TARGET_SET_NAMES:
        raise ValueError("P7 target_set must be sentinel, remaining, boundary, or holdout")
    manifold_ref = _file_reference(Path(manifold_config_path))
    if manifold_ref["sha256"] != FROZEN_MANIFOLD_SHA256:
        raise ValueError("P7 Ray HSI manifold hash does not match Gate-5")
    manifold = RayHsiManifold.load(manifold_config_path)
    policy_ref: dict[str, Any]
    if policy_version == "v1":
        policy_ref = _file_reference(Path(uncertainty_config_path))
        uncertainty = FrozenHsiUncertaintyEvaluator.load(uncertainty_config_path)
        frozen_features = uncertainty.artifact["feature_set"]
        if frozen_features.get("count") != len(manifold.coordinate_feature_ids) or frozen_features.get("sha256") != feature_ids_sha256(manifold.coordinate_feature_ids):
            raise ValueError("P7 uncertainty artifact feature order does not match the frozen manifold")
    else:
        policy_ref = _file_reference(Path(policy_v2_config_path))
        policy = HsiPolicyV2.load(policy_v2_config_path)
        if not policy.formal_capture_eligible:
            raise ValueError("P7 v2 formal runner rejects waiting/candidate policy artifacts")
        if policy.artifact["feature_set"]["ids"] != list(manifold.coordinate_feature_ids):
            raise ValueError("P7 v2 policy feature order does not match the frozen manifold")
    basis_ref = _file_reference(Path(basis_analysis_path))
    if basis_ref["sha256"] != FROZEN_BASIS_SHA256:
        raise ValueError("P7 basis hash does not match Gate-2")
    basis = _load_json(Path(basis_analysis_path))
    if basis.get("status") != "ready_for_manual_branch_review" or basis.get("channels") != list(CHANNELS):
        raise ValueError("P7 requires the frozen five-channel P2 basis")
    location_ref = _file_reference(Path(location_config_path))
    if location_ref["sha256"] != LATEST_LOCATION_SHA256 or basis.get("location_config_sha256") != location_ref["sha256"]:
        raise ValueError("P7 requires the latest location shared with P2")
    observer_ref = _file_reference(Path(observer_config_path))
    observer = _load_json(Path(observer_config_path))
    envelope = observer.get("validation", {}).get("exposure_envelope", {})
    if observer.get("validation", {}).get("raw_response_model") != "identity" or observer.get("statistics", {}).get("combine_green") is not False:
        raise ValueError("P7 requires identity RAW and separate G1/G2")
    if envelope.get("minimum_factor") != 1.0 or envelope.get("maximum_factor") != 1.25:
        raise ValueError("P7 requires the validated 1.0x..1.25x exposure envelope")

    sentinel = [(int(item["hue"]), int(item["sat"])) for item in config["target_sets"]["sentinel"]]
    remaining = [(int(item["hue"]), int(item["sat"])) for item in config["target_sets"]["remaining"]]
    expected_combined = {(0, 0)} | {(hue, sat) for hue in (0, 60, 120, 180, 240, 300) for sat in (50, 100)}
    if len(sentinel) != 4 or len(remaining) != 9 or len(set(sentinel + remaining)) != EXPECTED_TARGET_COUNT or set(sentinel + remaining) != expected_combined:
        raise ValueError("P7 sentinel and remaining target sets must form the exact frozen 4+9 grid")
    target_file_ref = None
    if target_set in {"sentinel", "remaining"}:
        requested_rows = config["target_sets"][target_set]
    else:
        if target_file_path is None:
            raise ValueError(f"P7 {target_set} target set requires --target-file")
        target_file_ref = _file_reference(Path(target_file_path))
        target_file = _load_json(Path(target_file_path))
        requested_rows = target_file.get("targets", [])
        if not requested_rows:
            raise ValueError(f"P7 {target_set} target file has no targets")
    if target_set != "sentinel" and parent_analysis_path is None:
        raise ValueError(f"P7 {target_set} target set requires a frozen parent analysis")
    targets = []
    previous_seed: dict[str, int] | None = None
    solver_max_code = int(config["solver"]["max_code"])
    for index, requested_row in enumerate(requested_rows):
        hue = int(requested_row["hue"])
        sat = int(requested_row["sat"])
        max_code = int(requested_row.get("max_code", solver_max_code))
        if max_code not in {solver_max_code, *map(int, config["solver"]["scale_relaxed_max_codes"])}:
            raise ValueError("P7 target max_code must be 4095, 3072, or 2048")
        target = manifold.target_at(hue, sat)
        seed = solve_piecewise_basis_seed(
            basis,
            target.features,
            feature_ids=manifold.coordinate_feature_ids,
            initial_command=previous_seed,
            max_code=max_code,
        )
        previous_seed = {channel: int(seed["best"]["command"][channel]) for channel in CHANNELS}
        seed_candidates = sorted(
            seed["candidates"], key=lambda item: float(item["predicted_relative_rmse"]),
        )[:2]
        confirmation_count = int(requested_row.get(
            "confirmation_count",
            config["confirmation"]["boundary_scale_relaxed_holdout_repeats"]
            if target_set in {"boundary", "holdout"} or max_code != solver_max_code
            else config["confirmation"]["ordinary_repeats"],
        ))
        budget = HsiSolverBudgetLimits(confirmations_per_group=confirmation_count)
        targets.append({
            "index": index,
            "hue": int(hue),
            "sat": int(sat),
            "intensity_percent": 100.0,
            "target_feature_sha256": _mapping_sha256({feature: target.features[feature] for feature in manifold.coordinate_feature_ids}),
            "coordinate_feature_count": len(manifold.coordinate_feature_ids),
            "target_kind": target_kind(manifold, hue, sat),
            "confirmation_count": confirmation_count,
            "max_code": max_code,
            "full_scale_policy": max_code == solver_max_code,
            "seed": seed,
            "distinct_face_seeds": seed_candidates,
            "solver_budget": budget.to_jsonable(),
        })
    return {
        "schema_version": 2 if policy_version == "v2" else 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_strip_hsi_pilot",
            "phase": "P7-pilot",
            "policy_version": policy_version,
            "gate6_eligibility": "requires_new_named_authorization_and_planner_frozen_policy" if policy_version == "v2" else "invalidated_by_PLAN_8_7",
            "branch": "full_periodic_2d_HB",
            "target_count": len(targets),
            "target_set": target_set,
            "expected_combined_grid": [{"hue": hue, "sat": sat} for hue, sat in sorted(expected_combined)],
            "coordinate_feature_ids": list(manifold.coordinate_feature_ids),
            "raw_response_model": "identity",
            "validated_exposure_envelope": copy.deepcopy(envelope),
            "camera_auto_exposure": {"target_max": int(target_max), "min_shutter_speed": str(min_shutter_speed), "max_shutter_speed": str(max_shutter_speed)},
            "source_isolation": "Ray is explicitly off before every ambient or strip capture",
        },
        "inputs": {
            "pilot_config": config_ref,
            "ray_hsi_manifold": manifold_ref,
            "basis_analysis": basis_ref,
            "location_config": location_ref,
            "raw_observer_config": observer_ref,
            ("policy_v2_artifact" if policy_version == "v2" else "uncertainty_artifact"): policy_ref,
            "code_duty_curve": _file_reference(Path(curve_path)),
            **({"parent_analysis": _file_reference(Path(parent_analysis_path))} if parent_analysis_path is not None else {}),
            **({"target_file": target_file_ref} if target_file_ref is not None else {}),
        },
        "devices": {"camera": {"backend": camera_backend, "credentials": "loaded_by_script_not_recorded"}},
        "targets": targets,
        "reference_anchors": _reference_anchor_plan(config["reference_anchors"], policy_version=policy_version),
        "cleanup": {"python": "required", "shell": "required_via_wrapper_trap", "strip_and_ray": "both"},
    }


def write_strip_hsi_pilot_dry_run(*, output_root: str | Path, run_name: str | None, **kwargs: Any) -> Path:
    plan = build_strip_hsi_pilot_plan(**kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = _utc_now()
    root = Path(output_root) / (run_name or datetime.now().strftime("p7-strip-hsi-pilot-dryrun-%Y%m%d-%H%M%S"))
    root.mkdir(parents=True, exist_ok=False)
    output = root / "plan.json"
    _write_json(output, plan)
    if plan["measurement"]["policy_version"] == "v1":
        uncertainty = _load_json(Path(plan["inputs"]["uncertainty_artifact"]["path"]))
        validation = validate_uncertainty_artifact(
            uncertainty,
            expected_feature_ids=plan["measurement"]["coordinate_feature_ids"],
        )
        validation.update({
            "created_at": _utc_now(),
            "uncertainty_artifact": copy.deepcopy(plan["inputs"]["uncertainty_artifact"]),
            "device_calls_performed": False,
        })
        _write_json(root / "uncertainty-validation.json", validation)
        if validation["status"] != "pass":
            raise ValueError("P7 uncertainty artifact failed offline validation")
    else:
        policy = HsiPolicyV2.load(plan["inputs"]["policy_v2_artifact"]["path"])
        _write_json(root / "policy-v2-validation.json", {
            "status": "pass" if policy.formal_capture_eligible else "fail",
            "policy_artifact": copy.deepcopy(plan["inputs"]["policy_v2_artifact"]),
            "feature_order_matches": policy.artifact["feature_set"]["ids"] == plan["measurement"]["coordinate_feature_ids"],
            "device_calls_performed": False,
        })
    return output


def execute_strip_hsi_pilot_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    capture_step_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_off_fn: Callable[[], Mapping[str, Any]],
    ray_set_hsi_fn: Callable[..., Mapping[str, Any]] | None = None,
    ray_get_hsi_fn: Callable[[], Mapping[str, Any]] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    provenance_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> Path:
    plan_data = copy.deepcopy(dict(plan))
    target_set = str(plan_data.get("measurement", {}).get("target_set"))
    expected_count = int(plan_data.get("measurement", {}).get("target_count", -1))
    if plan_data.get("measurement", {}).get("phase") != "P7-pilot" or target_set not in TARGET_SET_NAMES or expected_count <= 0 or len(plan_data.get("targets", [])) != expected_count:
        raise ValueError("P7 executor requires a complete frozen sentinel or remaining target set")
    if plan_data["measurement"].get("policy_version") != "v2":
        raise ValueError("formal P7 acquisition requires explicit policy_version=v2; v1 is replay-only")
    _verify_input_hashes(plan_data["inputs"])
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 1,
        "phase": "P7-pilot",
        "target_set": target_set,
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "completed_target_count": 0,
        "inputs": plan_data["inputs"],
        "measurement": plan_data["measurement"],
        "provenance": {"status": "pending" if provenance_fn else "not_collected"},
    }
    _write_json(root / "run.json", run)
    config = _load_json(Path(plan_data["inputs"]["pilot_config"]["path"]))
    manifold = RayHsiManifold.load(plan_data["inputs"]["ray_hsi_manifold"]["path"])
    policy = HsiPolicyV2.load(plan_data["inputs"]["policy_v2_artifact"]["path"])
    if not policy.formal_capture_eligible:
        raise ValueError("formal P7 acquisition rejects waiting/candidate v2 policy")
    required_features = tuple(plan_data["measurement"]["coordinate_feature_ids"])
    solver = config["solver"]
    confirmation = config["confirmation"]
    curve_config = _load_json(Path(plan_data["inputs"]["code_duty_curve"]["path"]))
    capture_index = 0
    exposure_ready: set[int] = set()
    ray_exposure_ready: set[tuple[int, int]] = set()
    previous_command: dict[str, int] | None = None
    failure: BaseException | None = None
    physical_budget: HsiPhysicalBudget | None = None
    reference_records: list[dict[str, Any]] = []
    reference_position_analyses: dict[str, dict[str, Any]] = {}

    def both_off(capture_id: str) -> None:
        strip_evidence = strip_light_fn(0, 0, 0, 0, 0)
        ray_response = ray_off_fn()
        _append_jsonl(root / "commands.jsonl", {
            "at": _utc_now(), "event": "both_off", "capture_id": capture_id,
            "strip_device_evidence": dict(strip_evidence), "ray_response": dict(ray_response),
        })
        validate_both_off(strip_evidence, ray_response, curve_config)

    def capture_source(
        *,
        purpose: str,
        target: Mapping[str, Any] | None,
        command: Mapping[str, int] | None = None,
        settled_confirmation: bool = False,
        exposure_factor: float | None = None,
        allow_weak_reacquire: bool = True,
        reacquire_of: str | None = None,
    ) -> dict[str, Any]:
        nonlocal capture_index, physical_budget
        target_index = -1 if target is None else int(target["index"])
        source = "ambient" if target is None else "strip"
        capture_id = f"{capture_index:04d}-{source}-{target_index:02d}-{purpose}"
        capture_index += 1
        both_off(capture_id)
        sleep_fn(float(confirmation["off_seconds"]))
        auto_exposure = source == "strip" and target_index not in exposure_ready and exposure_factor is None
        step = {
            "capture_id": capture_id,
            "index": capture_index - 1,
            "source": source,
            "purpose": purpose,
            "repeat_index": None,
            "exposure_factor": exposure_factor,
            "source_exposure_cache": None if source == "ambient" else f"strip:{target_index}",
            "auto_exposure": auto_exposure,
            "other_source_must_be_off": True,
            "ray": None,
            "strip_command": None,
            "analysis_context": {"phase": "P7-pilot", "target_index": target_index, "purpose": purpose, "weak_signal_reacquire": exposure_factor is not None},
        }
        if source == "strip" and physical_budget is not None:
            if physical_budget.remaining() < 1:
                raise HsiPhysicalBudgetExhausted(physical_budget.evidence(phase=purpose, requested=1))
            step["physical_capture_budget_remaining"] = physical_budget.remaining()
        if source == "strip":
            if command is None:
                raise ValueError("P7 strip capture requires a command")
            normalized = {channel: int(command[channel]) for channel in CHANNELS}
            step["strip_command"] = normalized
            device_evidence = strip_light_fn(*(normalized[channel] for channel in CHANNELS))
            expected_response = esphome._build_payload(*(normalized[channel] for channel in CHANNELS), curve=curve_config)
            _append_jsonl(root / "commands.jsonl", {
                "at": _utc_now(), "event": "strip_on_readback_verified", "capture_id": capture_id,
                "requested_command": normalized, "expected_response": expected_response,
                "device_evidence": dict(device_evidence), "device_state_verified": True,
            })
        sleep_fn(float(confirmation["settled_seconds"]) if settled_confirmation else float(confirmation["feedback_settle_seconds"]))
        try:
            capture = dict(capture_step_fn(step))
            physical_count = int(capture.get("physical_capture_count", 1))
            if source == "strip" and physical_budget is not None:
                physical_budget.record(
                    phase=purpose,
                    physical_count=physical_count,
                    auto_exposure=auto_exposure,
                    weak_reacquire=exposure_factor is not None,
                )
            _append_jsonl(root / "captures.jsonl", {"capture_id": capture_id, "source": source, "purpose": purpose, "target_index": target_index, "capture": capture})
            if source == "strip":
                exposure_ready.add(target_index)
        finally:
            both_off(capture_id)
        if source == "ambient":
            return {"capture_id": capture_id, "capture": capture}
        report = _load_json(Path(capture["patch_statistics"]))
        try:
            features = required_hsi_features_from_report(report, required_features)
        except HsiRejectedFeaturesError as exc:
            if exc.weak_signal_only and exposure_factor == 1.25 and not allow_weak_reacquire:
                raise WeakSignalEnvelopeExhausted(source="strip", purpose=purpose.removesuffix("-weak-signal-reacquire"), capture_ids=[*([reacquire_of] if reacquire_of else []), capture_id], rejected=exc.rejected) from exc
            if not (
                allow_weak_reacquire and exc.weak_signal_only and exposure_factor is None
                and (physical_budget is None or physical_budget.allow_weak_reacquire())
            ):
                raise
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "weak_signal_reacquire", "capture_id": capture_id, "exposure_factor": 1.25, "rejected_features": [item["feature_id"] for item in exc.rejected]})
            return capture_source(purpose=f"{purpose}-weak-signal-reacquire", target=target, command=command, settled_confirmation=settled_confirmation, exposure_factor=1.25, allow_weak_reacquire=False, reacquire_of=capture_id)
        return {"capture_id": capture_id, "capture": capture, "feature_values": features}

    def capture_reference(anchor: Mapping[str, Any], *, position: str, anchor_index: int) -> dict[str, Any]:
        nonlocal capture_index
        if ray_set_hsi_fn is None or ray_get_hsi_fn is None:
            raise ValueError("P7 reference anchors require Ray HSI set/readback functions")
        hue = int(anchor["hue"])
        sat = int(anchor["sat"])
        state_key = (hue, sat)
        capture_id = f"{capture_index:04d}-ray-anchor-{position}-{anchor_index}-h{hue}-s{sat}"
        capture_index += 1
        both_off(capture_id)
        sleep_fn(float(confirmation["off_seconds"]))
        set_response = ray_set_hsi_fn(hue, sat, intensity_percent=float(plan_data["reference_anchors"]["intensity_percent"]))
        readback = ray_get_hsi_fn()
        expected = {
            "hue": hue,
            "sat": sat,
            "intensity": ray120c.intensity_percent_to_raw(float(plan_data["reference_anchors"]["intensity_percent"])),
        }
        _verify_readback(readback, expected, mode="hsi")
        _append_jsonl(root / "commands.jsonl", {
            "at": _utc_now(), "event": "ray_on_readback_verified", "capture_id": capture_id,
            "expected": expected, "set_response": dict(set_response), "readback": dict(readback),
        })
        sleep_fn(float(confirmation["settled_seconds"]))
        step = {
            "capture_id": capture_id,
            "index": capture_index - 1,
            "source": "ray",
            "purpose": f"reference_anchor_{position}",
            "repeat_index": int(anchor.get("repeat_index", anchor_index)),
            "exposure_factor": None,
            "source_exposure_cache": f"ray:h{hue}:s{sat}",
            "auto_exposure": state_key not in ray_exposure_ready,
            "other_source_must_be_off": True,
            "ray": {"mode": "hsi", **expected},
            "strip_command": None,
            "analysis_context": {"phase": "P7-pilot", "target_index": None, "purpose": f"reference_anchor_{position}"},
        }
        try:
            capture = dict(capture_step_fn(step))
            ray_exposure_ready.add(state_key)
            _append_jsonl(root / "captures.jsonl", {
                "capture_id": capture_id, "source": "ray", "purpose": f"reference_anchor_{position}",
                "target_index": None, "ray_state": {"hue": hue, "sat": sat, "intensity_percent": 100.0},
                "capture": capture,
            })
        finally:
            both_off(capture_id)
        report = _load_json(Path(capture["patch_statistics"]))
        features = required_hsi_features_from_report(report, required_features)
        record = {
            "position": position,
            "anchor_index": anchor_index,
            "capture_id": capture_id,
            "target": {"hue": hue, "sat": sat, "intensity_percent": 100.0},
            "set_response": dict(set_response),
            "readback": dict(readback),
            "repeat_index": int(anchor.get("repeat_index", anchor_index)),
            "feature_values": features,
        }
        _append_jsonl(root / "reference-anchors.jsonl", record)
        reference_records.append(record)
        return record

    def evaluate_reference_position(position: str) -> dict[str, Any]:
        by_state: dict[tuple[int, int], list[dict[str, float]]] = {}
        for record in reference_records:
            if record["position"] == position:
                target_key = (int(record["target"]["hue"]), int(record["target"]["sat"]))
                by_state.setdefault(target_key, []).append(record["feature_values"])
        results = []
        states = policy.artifact["reference_policy"].get("states") or {}
        for (hue, sat), samples in sorted(by_state.items()):
            if len(samples) < 3:
                raise ReferenceDriftError(f"P7 v2 {position} H{hue}/S{sat} requires a three-frame block")
            state_key = f"h{hue}-s{sat}"
            frozen = states.get(state_key)
            if not isinstance(frozen, Mapping):
                raise ValueError(f"P7 v2 policy lacks frozen reference state {state_key}")
            current = summarize_within_block(samples, required_features)
            region = frozen["center_compatibility_region"]
            evaluation = evaluate_reference_difference(
                frozen["frozen_center"], current["center"],
                left_variance=frozen["frozen_diagonal_variance"],
                left_count=int(frozen["frozen_count"]),
                right_variance=current["diagonal_variance"],
                right_count=int(current["count"]),
                feature_ids=required_features,
                guarded_limit=float(region["guarded_limit"]),
                unguarded_limit=float(region["unguarded_limit"]),
                statistic="reference_center_compatibility",
            )
            results.append({"state": state_key, "block": current, "evaluation": evaluation})
            if evaluation["decision"] == "fail":
                raise ReferenceDriftError(f"P7 {position} reference block {state_key} exceeds frozen coverage")
            if evaluation["decision"] == "unresolved":
                raise ReferenceDriftError(f"P7 {position} reference block {state_key} is uncertainty_unresolved")
        output = {"position": position, "states": results, "status": "pass"}
        if position == "post":
            pre_by_state = {
                item["state"]: item["block"] for item in reference_position_analyses["pre"]["states"]
            }
            stability = []
            for item in results:
                pre = pre_by_state.get(item["state"])
                if pre is None:
                    raise ReferenceDriftError(f"P7 post reference state {item['state']} has no pre block")
                region = states[item["state"]]["repeatability_region"]
                comparison = evaluate_reference_difference(
                    pre["center"], item["block"]["center"],
                    left_variance=pre["diagonal_variance"], left_count=int(pre["count"]),
                    right_variance=item["block"]["diagonal_variance"], right_count=int(item["block"]["count"]),
                    feature_ids=required_features,
                    guarded_limit=float(region["guarded_limit"]),
                    unguarded_limit=float(region["unguarded_limit"]),
                    statistic="reference_repeatability",
                )
                stability.append({"state": item["state"], "evaluation": comparison})
                if comparison["decision"] != "pass":
                    raise ReferenceDriftError(f"P7 pre/post reference {item['state']} is {comparison['decision']}")
            output["pre_post_stability"] = stability
        reference_position_analyses[position] = output
        _write_json(root / f"reference-{position}-analysis.json", output)
        return output

    def record_unreachable(target: Mapping[str, Any], stage: str, evidence: Mapping[str, Any]) -> None:
        _append_jsonl(root / "target-results.jsonl", {"status": "measurement_unreachable", "target": target, "stage": stage, "evidence": dict(evidence)})
        run["completed_target_count"] += 1
        _write_json(root / "run.json", run)

    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("P7 provenance collector must return a mapping")
            run["provenance"] = dict(provenance)
            _write_json(root / "run.json", run)
        capture_source(purpose="ambient", target=None)
        for anchor_index, anchor in enumerate(plan_data["reference_anchors"]["pre"]):
            capture_reference(anchor, position="pre", anchor_index=anchor_index)
        evaluate_reference_position("pre")
        for target in plan_data["targets"]:
            target_limits = HsiSolverBudgetLimits(
                confirmations_per_group=int(target["confirmation_count"]),
            )
            if target["solver_budget"] != target_limits.to_jsonable():
                raise ValueError(f"P7 target {target['index']} solver budget declaration drift")
            physical_budget = HsiPhysicalBudget(
                hard_cap=target_limits.physical_per_target,
                autoexposure_cap=target_limits.autoexposure_physical_captures_per_target,
                weak_reacquire_cap=target_limits.weak_signal_reacquire_physical_captures_per_target,
            )
            expected_target = manifold.target_at(float(target["hue"]), float(target["sat"]))
            expected_hash = _mapping_sha256({feature: expected_target.features[feature] for feature in required_features})
            if expected_hash != target["target_feature_sha256"]:
                raise ValueError(f"P7 target feature hash drift at target {target['index']}")

            def run_candidate(
                *, seeds: Sequence[Mapping[str, Any]],
                max_code: int, confirmation_count: int, label: str,
            ) -> dict[str, Any]:
                def feedback_capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool) -> dict[str, Any]:
                    try:
                        observation = capture_source(
                            purpose=f"{label}_{phase}", target=target, command=command,
                            settled_confirmation=settled_confirmation,
                        )
                    except WeakSignalEnvelopeExhausted as exc:
                        return {"measurement_rejected": True, "rejection_evidence": exc.evidence()}
                    except HsiPhysicalBudgetExhausted as exc:
                        return {"measurement_rejected": True, "rejection_evidence": exc.evidence}
                    evaluated = evaluate_hsi_observation_v2(
                        manifold,
                        observation["feature_values"],
                        target_hue=float(target["hue"]),
                        target_sat=float(target["sat"]),
                        command=command,
                        previous_command=previous_command,
                        repeatability_class=_repeatability_class(
                            target_sat=float(target["sat"]), max_code=max_code,
                            formal_max_code=int(solver["max_code"]),
                        ),
                        policy=policy,
                        max_code=max_code,
                    )
                    return {
                        **evaluated,
                        "capture_id": observation["capture_id"],
                        "feature_values": observation["feature_values"],
                    }

                limits = HsiSolverBudgetLimits(confirmations_per_group=confirmation_count)
                feedback = run_hsi_feedback_multiseed(
                    seeds=seeds,
                    capture_observation_fn=feedback_capture,
                    max_starts=limits.max_starts,
                    rounds_per_start=limits.feedback_attempts_per_start,
                    budget_limits=limits,
                    max_code=max_code,
                    probe_step_code=min(int(solver["probe_step_code"]), max_code),
                    max_step_code=min(int(solver["max_step_code"]), max_code),
                    damping=float(solver["damping"]),
                    group_order=("coordinate", "rendering"),
                )
                selected = feedback["selected_result"]
                confirmed_attempts = [
                    item for item in selected["confirmation_attempts"] if item.get("status") == "confirmed"
                ]
                evidence_samples = [
                    selected["samples"][sample_index]
                    for sample_index in confirmed_attempts[-1]["sample_indices"]
                ] if confirmed_attempts else []
                repeatability_class = _repeatability_class(
                    target_sat=float(target["sat"]), max_code=max_code,
                    formal_max_code=int(solver["max_code"]),
                )
                class_policy = policy.artifact["repeatability_policy"]["classes"][repeatability_class]
                spread = None
                if evidence_samples:
                    feature_samples = [sample["observation"]["feature_values"] for sample in evidence_samples]
                    spread = evaluate_confirmation_spread(
                        feature_samples,
                        feature_ids=required_features,
                        class_name=repeatability_class,
                        class_variance=conservative_class_variance(
                            class_policy["p1_floor_diagonal_variance"],
                            class_policy["targeted_variance"],
                            required_features,
                        ),
                        limit=class_policy["limits"][str(confirmation_count)],
                    )
                uncertainty_unresolved = any(
                    item["objective"].get("hsi_coordinate_equivalent") == "unresolved"
                    or item["objective"].get("hsi_coordinate_equivalent") == "uncertainty_unresolved"
                    for item in evidence_samples
                ) or (spread is not None and spread["decision"] != "pass")
                status = "uncertainty_unresolved" if uncertainty_unresolved else (
                    "faithful" if selected["goal_confirmed"] else (
                        "solver_budget_exhausted" if feedback["status"] == "solver_budget_exhausted"
                        else "measurement_unreachable" if feedback["status"] == "measurement_unreachable"
                        else "unconfirmed"
                    )
                )
                if status not in P7_RESULT_STATUSES:
                    raise AssertionError(f"unsupported P7 result status: {status}")
                return {
                    "measurement_rejected": False,
                    "max_code": max_code,
                    "confirmation_count": confirmation_count,
                    "feedback": feedback,
                    "confirmation_spread": spread,
                    "result_status": status,
                    "selected_command": selected["selected_command"],
                    "physical_budget": None if physical_budget is None else physical_budget.to_jsonable(),
                }

            try:
                result = run_candidate(
                    seeds=target["distinct_face_seeds"],
                    max_code=int(target["max_code"]), confirmation_count=int(target["confirmation_count"]),
                    label="candidate",
                )
            except HsiMeasurementRejected as exc:
                record_unreachable(target, "strip_feedback_setup", {"phase": exc.phase, "command": exc.command, **exc.evidence})
                continue
            except HsiPhysicalBudgetExhausted as exc:
                result = {
                    "measurement_rejected": False,
                    "result_status": "solver_budget_exhausted",
                    "selected_command": target["distinct_face_seeds"][0]["command"],
                    "feedback": {
                        "status": "solver_budget_exhausted",
                        "budget_exhaustion": exc.evidence,
                        "best_valid_sample": None,
                    },
                    "confirmation_spread": None,
                    "physical_budget": physical_budget.to_jsonable(),
                }
            if result["measurement_rejected"]:
                record_unreachable(target, "strip_final_verification", result["rejection_evidence"])
                continue
            scale_relaxed_diagnostics = []
            row = {
                "status": "complete",
                "target": target,
                "basis_seed": target["seed"],
                "feedback": result["feedback"],
                "confirmation_spread": result["confirmation_spread"],
                "result_status": result["result_status"],
                "gamut_status": result["result_status"],
                "selected_command": result["selected_command"],
                "scale_relaxed_diagnostics": scale_relaxed_diagnostics,
                "physical_budget": result["physical_budget"],
            }
            _append_jsonl(root / "target-results.jsonl", row)
            previous_command = {channel: int(result["selected_command"][channel]) for channel in CHANNELS}
            run["completed_target_count"] += 1
            _write_json(root / "run.json", run)
        for anchor_index, anchor in enumerate(plan_data["reference_anchors"]["post"]):
            capture_reference(anchor, position="post", anchor_index=anchor_index)
        evaluate_reference_position("post")
    except BaseException as exc:
        failure = exc
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
    finally:
        cleanup = {"at": _utc_now(), "steps": [step.to_jsonable() for step in all_off_fn()]}
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if run["completed_target_count"] == expected_count and all(item["ok"] for item in cleanup["steps"]) else "failed"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    if run["status"] != "complete":
        raise RuntimeError("P7 pilot did not complete all targets with successful cleanup")
    return root


def run_strip_hsi_pilot(
    plan: Mapping[str, Any], *, output_root: str | Path, run_name: str | None,
    curve_path: str | Path, camera_backend: camera_gphoto2.CameraBackend,
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("p7-strip-hsi-pilot-%Y%m%d-%H%M%S"))
    capture_step = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=run_dir / "camera",
        measurements_dir=run_dir / "measurements",
        scratch_dir=run_dir / "scratch",
        location_config_path=plan["inputs"]["location_config"]["path"],
        observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
        target_max=int(plan["measurement"]["camera_auto_exposure"]["target_max"]),
        min_shutter_speed=str(plan["measurement"]["camera_auto_exposure"]["min_shutter_speed"]),
        max_shutter_speed=str(plan["measurement"]["camera_auto_exposure"]["max_shutter_speed"]),
        iso=None,
        aperture=None,
        camera_backend=camera_backend,
        recorded_exposure_purpose="P7-pilot",
    )
    return execute_strip_hsi_pilot_plan(
        plan,
        run_dir=run_dir,
        capture_step_fn=capture_step,
        strip_light_fn=lambda cw, ww, r, g, b: esphome.verified_light(cw, ww, r, g, b, curve_path=curve_path),
        ray_off_fn=lambda: ray120c.set_cct(5600, intensity=0, gm=100),
        ray_set_hsi_fn=ray120c.set_hsi,
        ray_get_hsi_fn=ray120c.get_hsi,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(curve_path=curve_path, camera_backend=camera_backend, backend_name="remote"),
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or execute the P7 strip HSI pilot.")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--manifold-config", type=Path, default=DEFAULT_MANIFOLD_CONFIG)
    parser.add_argument("--basis-analysis", type=Path, default=DEFAULT_BASIS_ANALYSIS)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--uncertainty-config", type=Path, default=DEFAULT_UNCERTAINTY_CONFIG)
    parser.add_argument("--policy-v2-config", type=Path, default=DEFAULT_POLICY_V2_CONFIG)
    parser.add_argument("--policy-version", choices=("v1", "v2"), required=True)
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--target-max", type=int, default=19661)
    parser.add_argument("--min-shutter-speed", default="1/16000")
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--target-set", choices=TARGET_SET_NAMES, default="sentinel")
    parser.add_argument("--parent-analysis", type=Path)
    parser.add_argument("--target-file", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-high-output", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    kwargs = {
        "config_path": args.config,
        "manifold_config_path": args.manifold_config,
        "basis_analysis_path": args.basis_analysis,
        "location_config_path": args.location_config,
        "observer_config_path": args.raw_observer_config,
        "uncertainty_config_path": args.uncertainty_config,
        "policy_v2_config_path": args.policy_v2_config,
        "policy_version": args.policy_version,
        "curve_path": args.curve,
        "target_max": args.target_max,
        "min_shutter_speed": args.min_shutter_speed,
        "max_shutter_speed": args.max_shutter_speed,
        "camera_backend": args.camera_backend,
        "target_set": args.target_set,
        "parent_analysis_path": args.parent_analysis,
        "target_file_path": args.target_file,
    }
    if args.dry_run:
        print(write_strip_hsi_pilot_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
    if args.policy_version != "v2":
        raise ValueError("--execute only supports policy-version v2; v1 is replay-only")
    backend = camera_remote.create_camera_backend(args.camera_backend, env_file=args.remote_env_file, base_url=args.remote_base_url, timeout=args.remote_timeout)
    plan = build_strip_hsi_pilot_plan(**kwargs)
    print(run_strip_hsi_pilot(plan, output_root=args.output_dir, run_name=args.run_name, curve_path=args.curve, camera_backend=backend))
    return 0


def _verify_input_hashes(inputs: Mapping[str, Any]) -> None:
    for reference in inputs.values():
        path = Path(reference["path"])
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != reference["sha256"]:
            raise ValueError(f"input hash drift for {path}")


def _reference_anchor_plan(value: Mapping[str, Any], *, policy_version: str) -> dict[str, Any]:
    output = copy.deepcopy(dict(value))
    if policy_version != "v2":
        return output
    output["pre"] = [
        {**copy.deepcopy(anchor), "repeat_index": repeat_index}
        for anchor in value["pre"] for repeat_index in range(3)
    ]
    post_anchor = next(
        (anchor for anchor in value["post"] if int(anchor["hue"]) == 120 and int(anchor["sat"]) == 100),
        value["post"][0],
    )
    output["post"] = [
        {**copy.deepcopy(post_anchor), "repeat_index": repeat_index}
        for repeat_index in range(3)
    ]
    output["repeat_block_contract"] = {
        "pre_per_state": 3,
        "post_h120_s100": 3,
        "single_frame_anchor_forbidden": True,
    }
    return output


def _repeatability_class(*, target_sat: float, max_code: int, formal_max_code: int) -> str:
    if max_code != formal_max_code:
        if float(target_sat) != 0.0:
            raise ValueError("v2 scale-relaxed repeatability is frozen only for neutral targets")
        return "neutral_scale_relaxed"
    if float(target_sat) == 0.0:
        return "neutral_fullscale"
    if float(target_sat) == 100.0:
        return "sat100_fullscale"
    return "mid_sat_fullscale"


def _validate_solver_budget_config(solver: Mapping[str, Any]) -> None:
    ordinary = HsiSolverBudgetLimits(confirmations_per_group=3)
    boundary = HsiSolverBudgetLimits(confirmations_per_group=5)
    expected = {
        "max_distinct_face_starts": ordinary.max_starts,
        "max_feedback_capture_attempts_per_start": ordinary.feedback_attempts_per_start,
        "max_rebases_per_start": ordinary.rebase_count_per_start,
        "max_confirmation_groups_per_start": ordinary.confirmation_groups_per_start,
        "ordinary_max_logical_observations": ordinary.logical_per_target,
        "ordinary_max_physical_cr3": ordinary.physical_per_target,
        "n5_max_logical_observations": boundary.logical_per_target,
        "n5_max_physical_cr3": boundary.physical_per_target,
    }
    mismatches = {key: {"expected": value, "actual": solver.get(key)} for key, value in expected.items() if solver.get(key) != value}
    if mismatches:
        raise ValueError(f"P7 solver budget config does not match Planner freeze: {mismatches}")


def _file_reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _mapping_sha256(values: Mapping[str, float]) -> str:
    payload = json.dumps(dict(values), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
