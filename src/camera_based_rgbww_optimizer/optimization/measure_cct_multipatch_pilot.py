from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, camera_remote, esphome, ray120c, white_lut
from camera_based_rgbww_optimizer.measurement.chart_response_basis import CHANNELS
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.optimization import white_lut_feedback
from camera_based_rgbww_optimizer.optimization.multipatch_feedback import (
    FeedbackMeasurementRejected,
    run_multipatch_feedback,
)
from camera_based_rgbww_optimizer.optimization.multipatch_objective import (
    build_residual_groups,
    objective_from_residual_groups,
    observation_from_raw_report,
    RejectedOptimizationFeaturesError,
    repeatability_neutral_tolerance,
    validate_feature_split,
)
from camera_based_rgbww_optimizer.optimization.multipatch_solver import solve_piecewise_basis_seed
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "cct-multipatch-pilot"
DEFAULT_CONFIG = PROJECT_ROOT / "config/camera/cct-multipatch-pilot.json"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config/location/locations-20260714-211759.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config/camera/raw-observer.json"
DEFAULT_BASELINE_LUT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/"
    "14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json"
)
DEFAULT_BASIS_ANALYSIS = Path(
    "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/"
    "p2-five-channel-basis-20260716-005935/basis-analysis.json"
)
FROZEN_BASIS_SHA256 = "5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1"
LATEST_LOCATION_SHA256 = "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"


class WeakSignalEnvelopeExhausted(ValueError):
    def __init__(
        self,
        *,
        source: str,
        purpose: str,
        capture_ids: Sequence[str],
        rejected: Sequence[Mapping[str, Any]],
    ) -> None:
        super().__init__(
            f"{source} {purpose} remains below the RAW quality floor after 1.25x reacquisition"
        )
        self.source = str(source)
        self.purpose = str(purpose)
        self.capture_ids = [str(value) for value in capture_ids]
        self.rejected = [dict(item) for item in rejected]

    def evidence(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "purpose": self.purpose,
            "capture_ids": self.capture_ids,
            "exposure_factors": [1.0, 1.25],
            "rejected_features": self.rejected,
        }


def build_cct_multipatch_pilot_plan(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    basis_analysis_path: str | Path = DEFAULT_BASIS_ANALYSIS,
    baseline_lut_path: str | Path = DEFAULT_BASELINE_LUT,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    camera_backend: str = "remote",
) -> dict[str, Any]:
    if camera_backend != "remote":
        raise ValueError("new P4 experiments require camera_backend=remote")
    config_ref = _file_reference(Path(config_path))
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config.get("phase") != "P4" or config.get("branch") != "C-F":
        raise ValueError("P4 pilot config must freeze the C-F branch")

    basis_ref = _file_reference(Path(basis_analysis_path))
    if basis_ref["sha256"] != FROZEN_BASIS_SHA256:
        raise ValueError("P4 basis artifact hash does not match the frozen Gate-2 input")
    basis = json.loads(Path(basis_analysis_path).read_text(encoding="utf-8"))
    if basis.get("status") != "ready_for_manual_branch_review" or basis.get("analysis") != "chart_response_basis":
        raise ValueError("P4 requires the frozen P2 chart response basis analysis")
    if basis.get("channels") != list(CHANNELS) or basis.get("plane_order") != ["R", "G1", "G2", "B"]:
        raise ValueError("P4 requires the frozen five-channel, four-plane P2 basis")

    location_ref = _file_reference(Path(location_config_path))
    if location_ref["sha256"] != LATEST_LOCATION_SHA256:
        raise ValueError("P4 requires locations-20260714-211759.json with its frozen hash")
    if basis.get("location_config_sha256") != location_ref["sha256"]:
        raise ValueError("P2 basis and P4 location hashes do not match")
    observer_ref = _file_reference(Path(observer_config_path))
    observer = json.loads(Path(observer_config_path).read_text(encoding="utf-8"))
    if observer.get("validation", {}).get("raw_response_model") != "identity":
        raise ValueError("P4 requires the Gate-1 identity RAW response decision")
    if observer.get("statistics", {}).get("combine_green") is not False:
        raise ValueError("P4 requires separate R/G1/G2/B features")

    feature_config = config["features"]
    feature_split = validate_feature_split(
        basis["feature_order"],
        neutral_blocks=feature_config["neutral_blocks"],
        training_blocks=feature_config["training_blocks"],
        holdout_blocks=feature_config["holdout_blocks"],
    )
    lut_path = Path(baseline_lut_path)
    lut_ref = _file_reference(lut_path)
    lut = white_lut.load_white_lut(lut_path)

    targets = []
    captures = []
    target_index = 0
    for cct in config["target_grid"]["cct_K"]:
        for gm in config["target_grid"]["gm_raw"]:
            baseline_command = _lut_command(lut, int(cct), int(gm))
            target = {
                "index": target_index,
                "cct_K": int(cct),
                "gm_raw": int(gm),
                "baseline_command": baseline_command,
                "candidate_seed": "frozen_p2_basis_then_local_camera_feedback",
            }
            targets.append(target)
            captures.extend(_formal_capture_protocol(target))
            target_index += 1

    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_cct_multipatch_pilot",
            "phase": "P4",
            "branch": "C-F",
            "target_count": len(targets),
            "target_grid": config["target_grid"],
            "feature_split": feature_split,
            "feature_count": sum(len(values) for values in feature_split.values()),
            "objective": config["objective"],
            "solver": config["solver"],
            "confirmation": config["confirmation"],
            "forward_model_role": "seed_only",
            "execution_status": "hardware_runner_code_complete_waiting_for_dry_run_safety_review",
            "camera_auto_exposure": {
                "target_max": int(target_max),
                "min_shutter_speed": str(min_shutter_speed),
                "max_shutter_speed": str(max_shutter_speed),
                "source_caches": ["ray", "strip"],
            },
        },
        "inputs": {
            "pilot_config": config_ref,
            "basis_analysis": basis_ref,
            "baseline_lut": lut_ref,
            "location_config": location_ref,
            "raw_observer_config": observer_ref,
        },
        "devices": {
            "camera": {"backend": camera_backend, "credentials": "loaded_by_script_not_recorded"},
            "source_isolation": "exactly_one_of_ray_or_strip_may_be_on_for_each_capture",
        },
        "targets": targets,
        "formal_capture_protocol": captures,
        "adaptive_capture_budget": {
            "per_target_max_rounds": int(config["solver"]["max_rounds"]),
            "probe_channels_per_active_channel": 4,
            "thermal_rebase": "same_as_white_lut_feedback",
        },
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted_even_if_one_shutdown_fails",
        },
    }


def write_cct_multipatch_pilot_dry_run(
    *,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    run_name: str | None = None,
    **kwargs: Any,
) -> Path:
    plan = build_cct_multipatch_pilot_plan(**kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = datetime.now(timezone.utc).isoformat()
    resolved_name = run_name or datetime.now().strftime("p4-cct-multipatch-dryrun-%Y%m%d-%H%M%S")
    run_dir = Path(output_root) / resolved_name
    run_dir.mkdir(parents=True, exist_ok=False)
    output = run_dir / "plan.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output)
    return output


def execute_cct_multipatch_pilot_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    capture_step_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_set_cct_fn: Callable[..., Mapping[str, Any]],
    sleep_fn: Callable[[float], None] = time.sleep,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    observation_fn: Callable[..., Mapping[str, Any]] = observation_from_raw_report,
    provenance_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> Path:
    plan_data = copy.deepcopy(dict(plan))
    if plan_data.get("measurement", {}).get("phase") != "P4" or len(plan_data.get("targets", [])) != 12:
        raise ValueError("P4 executor requires the complete frozen 12-target plan")
    _verify_input_hashes(plan_data["inputs"])
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 1, "phase": "P4", "status": "running",
        "started_at": _utc_now(), "finished_at": None,
        "inputs": plan_data["inputs"], "measurement": plan_data["measurement"],
        "completed_target_count": 0,
        "provenance": {"status": "pending" if provenance_fn is not None else "not_collected"},
    }
    _write_json(root / "run.json", run)
    basis = json.loads(Path(plan_data["inputs"]["basis_analysis"]["path"]).read_text(encoding="utf-8"))
    config = json.loads(Path(plan_data["inputs"]["pilot_config"]["path"]).read_text(encoding="utf-8"))
    split = plan_data["measurement"]["feature_split"]
    neutral_blocks = config["features"]["neutral_blocks"]
    solver_config = config["solver"]
    confirmation = config["confirmation"]
    capture_index = 0
    failure: BaseException | None = None

    def capture_source(
        *, source: str, purpose: str, target: Mapping[str, Any] | None,
        command: Mapping[str, int] | None = None, auto_exposure: bool = False,
        settled_confirmation: bool = False,
        exposure_factor: float | None = None,
        allow_weak_reacquire: bool = True,
        reacquire_of_capture_id: str | None = None,
    ) -> dict[str, Any]:
        nonlocal capture_index
        target_index = -1 if target is None else int(target["index"])
        capture_id = f"{capture_index:04d}-{source}-{target_index:02d}-{purpose}"
        capture_index += 1
        _set_both_off(
            strip_light_fn, ray_set_cct_fn, command_log=root / "commands.jsonl",
            capture_id=capture_id, target=target,
        )
        sleep_fn(float(confirmation["off_seconds"]))
        step = {
            "capture_id": capture_id, "index": capture_index - 1, "source": source,
            "purpose": purpose, "repeat_index": None, "exposure_factor": exposure_factor,
            "source_exposure_cache": source if source in {"ray", "strip"} else None,
            "auto_exposure": bool(auto_exposure), "other_source_must_be_off": True,
            "ray": None, "strip_command": None,
            "analysis_context": {
                "phase": "P4", "target_index": target_index, "purpose": purpose,
                "weak_signal_reacquire": exposure_factor is not None,
            },
        }
        if source == "ray":
            assert target is not None
            step["ray"] = {"cct": int(target["cct_K"]), "gm": int(target["gm_raw"]), "intensity_percent": 100.0}
            response = ray_set_cct_fn(int(target["cct_K"]), intensity_percent=100.0, gm=int(target["gm_raw"]))
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "ray_on", "capture_id": capture_id, "response": dict(response)})
        elif source == "strip":
            if command is None:
                raise ValueError("strip capture requires a command")
            normalized = {channel: int(command[channel]) for channel in CHANNELS}
            step["strip_command"] = normalized
            response = strip_light_fn(*(normalized[channel] for channel in CHANNELS))
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "strip_on", "capture_id": capture_id, "requested_command": normalized, "response": dict(response)})
        elif source != "ambient":
            raise ValueError(f"unsupported P4 capture source: {source}")
        sleep_fn(float(confirmation["settle_seconds"]) if settled_confirmation else 1.0)
        try:
            capture = dict(capture_step_fn(step))
            _append_jsonl(root / "captures.jsonl", {"capture_id": capture_id, "source": source, "purpose": purpose, "target_index": target_index, "capture": capture})
        finally:
            if source == "ray" and target is not None:
                ray_set_cct_fn(int(target["cct_K"]), intensity=0, gm=int(target["gm_raw"]))
            elif source == "strip":
                strip_light_fn(0, 0, 0, 0, 0)
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": f"{source}_off", "capture_id": capture_id})
        if source == "ambient":
            return {"capture": capture}
        report = json.loads(Path(capture["patch_statistics"]).read_text(encoding="utf-8"))
        raw_file = Path(capture["capture"]["saved_file"])
        try:
            observation = dict(observation_fn(report, raw_file=raw_file))
        except RejectedOptimizationFeaturesError as exc:
            if exc.weak_signal_only and exposure_factor == 1.25 and not allow_weak_reacquire:
                raise WeakSignalEnvelopeExhausted(
                    source=source,
                    purpose=purpose.removesuffix("-weak-signal-reacquire"),
                    capture_ids=[
                        *([reacquire_of_capture_id] if reacquire_of_capture_id is not None else []),
                        capture_id,
                    ],
                    rejected=exc.rejected,
                ) from exc
            if not (allow_weak_reacquire and exc.weak_signal_only and exposure_factor is None):
                raise
            _append_jsonl(root / "commands.jsonl", {
                "at": _utc_now(), "event": "weak_signal_reacquire",
                "capture_id": capture_id,
                "rejected_features": [item["feature_id"] for item in exc.rejected],
                "exposure_factor": 1.25,
            })
            return capture_source(
                source=source,
                purpose=f"{purpose}-weak-signal-reacquire",
                target=target,
                command=command,
                auto_exposure=False,
                settled_confirmation=settled_confirmation,
                exposure_factor=1.25,
                allow_weak_reacquire=False,
                reacquire_of_capture_id=capture_id,
            )
        observation["capture_id"] = capture_id
        observation["capture"] = capture
        return observation

    def record_measurement_unreachable(
        target: Mapping[str, Any],
        *,
        stage: str,
        evidence: Mapping[str, Any],
        partial_feedback: Mapping[str, Any] | None = None,
    ) -> None:
        row = {
            "status": "measurement_unreachable",
            "target": target,
            "stage": str(stage),
            "reason": "weak_signal_after_max_validated_exposure",
            "validated_exposure_envelope": [1.0, 1.25],
            "evidence": dict(evidence),
        }
        if partial_feedback is not None:
            row["partial_feedback"] = dict(partial_feedback)
        _append_jsonl(root / "target-results.jsonl", row)
        run["completed_target_count"] += 1
        _write_json(root / "run.json", run)

    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("P4 provenance collector must return a mapping")
            run["provenance"] = dict(provenance)
            _write_json(root / "run.json", run)
        capture_source(source="ambient", purpose="ambient", target=None)
        for target in plan_data["targets"]:
            try:
                ray_observation = capture_source(
                    source="ray", purpose="ray_target", target=target, auto_exposure=True
                )
            except WeakSignalEnvelopeExhausted as exc:
                record_measurement_unreachable(
                    target, stage="ray_reference", evidence=exc.evidence()
                )
                continue
            try:
                baseline_observations = [
                    capture_source(
                        source="strip", purpose=("baseline_observation" if index == 0 else f"baseline_confirmation_{index-1}"),
                        target=target, command=target["baseline_command"], auto_exposure=index == 0,
                        settled_confirmation=index > 0,
                    )
                    for index in range(3)
                ]
            except WeakSignalEnvelopeExhausted as exc:
                record_measurement_unreachable(
                    target, stage="strip_baseline", evidence=exc.evidence()
                )
                continue
            neutral_tolerance = repeatability_neutral_tolerance(
                baseline_observations,
                neutral_blocks=neutral_blocks,
                absolute_floor=float(config["objective"]["neutral_chroma_absolute_floor"]),
            )
            cct_tolerance = white_lut_feedback.resolve_cct_tolerance_K(
                float(target["cct_K"]),
                minimum_tolerance_K=float(config["objective"]["white_point_tolerance"]["minimum_cct_K"]),
                tolerance_mired=float(config["objective"]["white_point_tolerance"]["cct_mired"]),
            )
            duv_tolerance = float(config["objective"]["white_point_tolerance"]["duv"])

            def evaluate(observation: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
                residuals = build_residual_groups(
                    observation, ray_observation, feature_split=split, neutral_blocks=neutral_blocks,
                    cct_tolerance_K=cct_tolerance, duv_tolerance=duv_tolerance,
                )
                objective = objective_from_residual_groups(
                    residuals, neutral_chroma_tolerance=neutral_tolerance
                )
                return residuals, objective

            baseline_results = []
            baseline_residual_sets = []
            for observation in baseline_observations:
                residuals, objective = evaluate(observation)
                baseline_residual_sets.append(residuals)
                baseline_results.append({"capture_id": observation["capture_id"], "residuals": {key: value.tolist() for key, value in residuals.items()}, "objective": objective})
            baseline_center_residuals = {
                group: np.median(
                    np.stack([item[group] for item in baseline_residual_sets]), axis=0
                )
                for group in ("neutral", "white", "training", "holdout")
            }
            baseline_center_objective = objective_from_residual_groups(
                baseline_center_residuals, neutral_chroma_tolerance=neutral_tolerance
            )
            seed = solve_piecewise_basis_seed(
                basis, ray_observation["feature_values"],
                feature_ids=[*split["neutral"], *split["training"], *split["holdout"]],
                initial_command=target["baseline_command"],
            )

            def feedback_capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool) -> dict[str, Any]:
                try:
                    observation = capture_source(
                        source="strip", purpose=f"candidate_{phase}", target=target,
                        command=command, settled_confirmation=settled_confirmation,
                    )
                except WeakSignalEnvelopeExhausted as exc:
                    return {
                        "measurement_rejected": True,
                        "rejection_evidence": exc.evidence(),
                    }
                residuals, objective = evaluate(observation)
                return {"residuals": residuals, "objective": objective, "white_point": observation["white_point"], "capture_id": observation["capture_id"]}

            try:
                feedback_result = run_multipatch_feedback(
                    initial_command=seed["best"]["command"],
                    active_channel=str(seed["best"]["active_channel"]),
                    capture_observation_fn=feedback_capture,
                    neutral_chroma_tolerance=neutral_tolerance,
                    max_code=int(solver_config["max_code"]), rounds=int(solver_config["max_rounds"]),
                    probe_step_code=int(solver_config["probe_step_code"]),
                    max_step_code=int(solver_config["max_step_code"]), damping=float(solver_config["damping"]),
                    confirmations=int(confirmation["independent_repeats"]), thermal_rebases=2,
                    acceptance_rank_key=baseline_center_objective["rank_key"],
                )
            except FeedbackMeasurementRejected as exc:
                evidence = dict(exc.evidence)
                evidence["feedback_phase"] = exc.phase
                evidence["command"] = exc.command
                record_measurement_unreachable(
                    target, stage="strip_feedback_setup", evidence=evidence
                )
                continue
            final_verification = []
            final_rejection = None
            if not feedback_result["goal_confirmed"]:
                for final_index in range(int(confirmation["independent_repeats"])):
                    final = feedback_capture(
                        feedback_result["selected_command"],
                        phase=f"final-verification-{final_index}",
                        settled_confirmation=True,
                    )
                    if final.get("measurement_rejected"):
                        final_rejection = dict(final["rejection_evidence"])
                        final_rejection["final_verification_index"] = final_index
                        break
                    final_verification.append({
                        "capture_id": final["capture_id"],
                        "residuals": {key: value.tolist() for key, value in final["residuals"].items()},
                        "objective": final["objective"],
                    })
            if final_rejection is not None:
                record_measurement_unreachable(
                    target,
                    stage="strip_final_verification",
                    evidence=final_rejection,
                    partial_feedback=feedback_result,
                )
                continue
            result = {
                "status": "complete",
                "target": target, "ray_capture_id": ray_observation["capture_id"],
                "neutral_chroma_tolerance": neutral_tolerance,
                "cct_tolerance_K": cct_tolerance, "duv_tolerance": duv_tolerance,
                "baseline": baseline_results,
                "baseline_center_objective": baseline_center_objective,
                "basis_seed": seed, "feedback": feedback_result,
                "final_verification": final_verification,
            }
            _append_jsonl(root / "target-results.jsonl", result)
            run["completed_target_count"] += 1
            _write_json(root / "run.json", run)
    except BaseException as exc:
        failure = exc
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
    finally:
        cleanup = _cleanup(strip_light_fn, ray_set_cct_fn, all_off_fn)
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if _cleanup_ok(cleanup) and run["completed_target_count"] == 12 else "failed"
            if run["status"] == "failed" and failure is None:
                failure = RuntimeError("P4 acquisition finished without complete targets or successful Python cleanup")
                _write_json(root / "failure.json", {"at": _utc_now(), "type": type(failure).__name__, "message": str(failure)})
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    return root


def _formal_capture_protocol(target: Mapping[str, Any]) -> list[dict[str, Any]]:
    prefix = f"{int(target['cct_K'])}K-gm{int(target['gm_raw'])}"
    items = [
        ("ray_target", "ray", None),
        ("baseline_observation", "strip", target["baseline_command"]),
        ("baseline_confirmation_0", "strip", target["baseline_command"]),
        ("baseline_confirmation_1", "strip", target["baseline_command"]),
        ("candidate_observation", "strip", "adaptive_candidate"),
        ("candidate_confirmation_0", "strip", "adaptive_candidate"),
        ("candidate_confirmation_1", "strip", "adaptive_candidate"),
    ]
    return [
        {
            "capture_id": f"{prefix}-{purpose}",
            "target_index": int(target["index"]),
            "purpose": purpose,
            "source": source,
            "strip_command": command,
            "other_source_must_be_off": True,
            "off_seconds_before": 1.0,
            "settle_seconds": 60.0 if "confirmation" in purpose else "shared_source_exposure_policy",
        }
        for purpose, source, command in items
    ]


def _lut_command(lut: Mapping[str, Any], cct: int, gm: int) -> dict[str, int]:
    command = white_lut.interpolate_white_lut(lut, cct, gm, clamp=False)["command"]
    resolved = {channel: int(command[channel]) for channel in CHANNELS}
    if max(resolved.values()) != 4095:
        raise ValueError(f"baseline LUT command for {cct}K/gm{gm} has no channel at 4095")
    return resolved


def _file_reference(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _verify_input_hashes(inputs: Mapping[str, Any]) -> None:
    for name, reference in inputs.items():
        if not isinstance(reference, Mapping) or "path" not in reference or "sha256" not in reference:
            raise ValueError(f"P4 input {name} is not a frozen file reference")
        if _file_reference(Path(reference["path"]))["sha256"] != str(reference["sha256"]):
            raise ValueError(f"P4 input hash changed after planning: {name}")


def run_cct_multipatch_pilot(
    plan: Mapping[str, Any],
    *,
    output_root: str | Path,
    run_name: str | None,
    curve_path: str | Path,
    camera_backend: camera_gphoto2.CameraBackend,
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("p4-cct-multipatch-%Y%m%d-%H%M%S"))
    exposure = plan["measurement"]["camera_auto_exposure"]
    capture_step = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=run_dir / "camera",
        measurements_dir=run_dir / "measurements",
        scratch_dir=run_dir / "scratch",
        location_config_path=plan["inputs"]["location_config"]["path"],
        observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
        target_max=int(exposure["target_max"]),
        min_shutter_speed=str(exposure["min_shutter_speed"]),
        max_shutter_speed=str(exposure["max_shutter_speed"]),
        iso=None,
        aperture=None,
        camera_backend=camera_backend,
        recorded_exposure_purpose="P4",
    )
    return execute_cct_multipatch_pilot_plan(
        plan,
        run_dir=run_dir,
        capture_step_fn=capture_step,
        strip_light_fn=lambda cw, ww, r, g, b: esphome.light(cw, ww, r, g, b, curve_path=curve_path),
        ray_set_cct_fn=ray120c.set_cct,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(
            curve_path=curve_path,
            camera_backend=camera_backend,
            backend_name="remote",
        ),
    )


def _set_both_off(
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_set_cct_fn: Callable[..., Mapping[str, Any]],
    *,
    command_log: Path,
    capture_id: str,
    target: Mapping[str, Any] | None,
) -> None:
    cct = 5600 if target is None else int(target["cct_K"])
    gm = 100 if target is None else int(target["gm_raw"])
    strip_light_fn(0, 0, 0, 0, 0)
    ray_set_cct_fn(cct, intensity=0, gm=gm)
    _append_jsonl(command_log, {"at": _utc_now(), "event": "both_off", "capture_id": capture_id})


def _cleanup(
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_set_cct_fn: Callable[..., Mapping[str, Any]],
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]],
) -> dict[str, Any]:
    try:
        steps = all_off_fn(
            strip_off_fn=lambda: dict(strip_light_fn(0, 0, 0, 0, 0)),
            ray_set_cct_fn=ray_set_cct_fn,
            ray_cct=5600,
            ray_gm=100,
        )
        return {
            "at": _utc_now(),
            "steps": [step.to_jsonable() if isinstance(step, all_off.ShutdownStep) else dict(step) for step in steps],
        }
    except BaseException as exc:
        return {"at": _utc_now(), "steps": [], "cleanup_exception": {"type": type(exc).__name__, "message": str(exc)}}


def _cleanup_ok(cleanup: Mapping[str, Any]) -> bool:
    steps = cleanup.get("steps")
    return (
        "cleanup_exception" not in cleanup
        and isinstance(steps, list)
        and len(steps) == 2
        and all(isinstance(step, Mapping) and bool(step.get("ok")) for step in steps)
    )


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or run the P4 4x3 CCT multipatch pilot")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="write an immutable offline plan without device access")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-high-output", action="store_true")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--basis-analysis", type=Path, default=DEFAULT_BASIS_ANALYSIS)
    parser.add_argument("--baseline-lut", type=Path, default=DEFAULT_BASELINE_LUT)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--target-max", type=int, default=19661)
    parser.add_argument("--min-shutter-speed", default="1/16000")
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    kwargs = dict(
        config_path=args.config,
        basis_analysis_path=args.basis_analysis,
        baseline_lut_path=args.baseline_lut,
        location_config_path=args.location_config,
        observer_config_path=args.observer_config,
        target_max=args.target_max,
        min_shutter_speed=args.min_shutter_speed,
        max_shutter_speed=args.max_shutter_speed,
        camera_backend=args.camera_backend,
    )
    if args.dry_run:
        output = write_cct_multipatch_pilot_dry_run(
            output_root=args.output_root, run_name=args.run_name, **kwargs,
        )
        print(output)
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    plan = build_cct_multipatch_pilot_plan(**kwargs)
    output = run_cct_multipatch_pilot(
        plan, output_root=args.output_root, run_name=args.run_name,
        curve_path=args.curve, camera_backend=backend,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
