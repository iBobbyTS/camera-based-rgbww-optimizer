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
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.optimization.hsi_feedback import HsiMeasurementRejected, run_hsi_feedback
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    HsiRejectedFeaturesError,
    evaluate_hsi_observation,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.measure_cct_multipatch_pilot import WeakSignalEnvelopeExhausted
from camera_based_rgbww_optimizer.optimization.multipatch_solver import solve_piecewise_basis_seed
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "strip-hsi-pilot"
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-pilot.json"
DEFAULT_MANIFOLD_CONFIG = PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_BASIS_ANALYSIS = Path(
    "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/"
    "p2-five-channel-basis-20260716-005935/basis-analysis.json"
)
FROZEN_BASIS_SHA256 = "5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1"
FROZEN_MANIFOLD_SHA256 = "20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34"
LATEST_LOCATION_SHA256 = "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"
EXPECTED_TARGET_COUNT = 13


def build_strip_hsi_pilot_plan(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    manifold_config_path: str | Path = DEFAULT_MANIFOLD_CONFIG,
    basis_analysis_path: str | Path = DEFAULT_BASIS_ANALYSIS,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    curve_path: str | Path = esphome.DEFAULT_CURVE_PATH,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    camera_backend: str = "remote",
) -> dict[str, Any]:
    if camera_backend != "remote":
        raise ValueError("new P7 experiments require camera_backend=remote")
    config_ref = _file_reference(Path(config_path))
    config = _load_json(Path(config_path))
    if config.get("phase") != "P7-pilot" or config.get("branch") != "full_periodic_2d_HB":
        raise ValueError("P7 pilot config must freeze the full_periodic_2d_HB branch")
    manifold_ref = _file_reference(Path(manifold_config_path))
    if manifold_ref["sha256"] != FROZEN_MANIFOLD_SHA256:
        raise ValueError("P7 Ray HSI manifold hash does not match Gate-5")
    manifold = RayHsiManifold.load(manifold_config_path)
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

    requested = [(0, 0)] + [
        (hue, sat)
        for hue in config["targets"]["hue_degrees"]
        for sat in config["targets"]["saturation_percent"]
    ]
    if len(requested) != EXPECTED_TARGET_COUNT:
        raise ValueError(f"P7 pilot requires exactly {EXPECTED_TARGET_COUNT} targets")
    targets = []
    previous_seed: dict[str, int] | None = None
    for index, (hue, sat) in enumerate(requested):
        target = manifold.target_at(hue, sat)
        seed = solve_piecewise_basis_seed(
            basis,
            target.features,
            feature_ids=manifold.coordinate_feature_ids,
            initial_command=previous_seed,
        )
        previous_seed = {channel: int(seed["best"]["command"][channel]) for channel in CHANNELS}
        targets.append({
            "index": index,
            "hue": int(hue),
            "sat": int(sat),
            "intensity_percent": 100.0,
            "target_feature_sha256": _mapping_sha256({feature: target.features[feature] for feature in manifold.coordinate_feature_ids}),
            "coordinate_feature_count": len(manifold.coordinate_feature_ids),
            "seed": seed,
        })
    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_strip_hsi_pilot",
            "phase": "P7-pilot",
            "branch": "full_periodic_2d_HB",
            "target_count": len(targets),
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
            "code_duty_curve": _file_reference(Path(curve_path)),
        },
        "devices": {"camera": {"backend": camera_backend, "credentials": "loaded_by_script_not_recorded"}},
        "targets": targets,
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
    return output


def execute_strip_hsi_pilot_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    capture_step_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_off_fn: Callable[[], Mapping[str, Any]],
    sleep_fn: Callable[[float], None] = time.sleep,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    provenance_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> Path:
    plan_data = copy.deepcopy(dict(plan))
    if plan_data.get("measurement", {}).get("phase") != "P7-pilot" or len(plan_data.get("targets", [])) != EXPECTED_TARGET_COUNT:
        raise ValueError("P7 executor requires the complete 13-target pilot")
    _verify_input_hashes(plan_data["inputs"])
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 1,
        "phase": "P7-pilot",
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
    required_features = tuple(plan_data["measurement"]["coordinate_feature_ids"])
    solver = config["solver"]
    confirmation = config["confirmation"]
    capture_index = 0
    exposure_ready: set[int] = set()
    previous_command: dict[str, int] | None = None
    failure: BaseException | None = None

    def both_off(capture_id: str) -> None:
        strip_response = strip_light_fn(0, 0, 0, 0, 0)
        _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "strip_off", "capture_id": capture_id, "response": dict(strip_response)})
        ray_response = ray_off_fn()
        _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "ray_off", "capture_id": capture_id, "response": dict(ray_response)})

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
        nonlocal capture_index
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
        if source == "strip":
            if command is None:
                raise ValueError("P7 strip capture requires a command")
            normalized = {channel: int(command[channel]) for channel in CHANNELS}
            step["strip_command"] = normalized
            response = strip_light_fn(*(normalized[channel] for channel in CHANNELS))
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "strip_on", "capture_id": capture_id, "requested_command": normalized, "response": dict(response)})
        sleep_fn(float(confirmation["settled_seconds"]) if settled_confirmation else float(confirmation["feedback_settle_seconds"]))
        try:
            capture = dict(capture_step_fn(step))
            _append_jsonl(root / "captures.jsonl", {"capture_id": capture_id, "source": source, "purpose": purpose, "target_index": target_index, "capture": capture})
            if source == "strip":
                exposure_ready.add(target_index)
        finally:
            if source == "strip":
                strip_light_fn(0, 0, 0, 0, 0)
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": f"{source}_off", "capture_id": capture_id})
        if source == "ambient":
            return {"capture_id": capture_id, "capture": capture}
        report = _load_json(Path(capture["patch_statistics"]))
        try:
            features = required_hsi_features_from_report(report, required_features)
        except HsiRejectedFeaturesError as exc:
            if exc.weak_signal_only and exposure_factor == 1.25 and not allow_weak_reacquire:
                raise WeakSignalEnvelopeExhausted(source="strip", purpose=purpose.removesuffix("-weak-signal-reacquire"), capture_ids=[*([reacquire_of] if reacquire_of else []), capture_id], rejected=exc.rejected) from exc
            if not (allow_weak_reacquire and exc.weak_signal_only and exposure_factor is None):
                raise
            _append_jsonl(root / "commands.jsonl", {"at": _utc_now(), "event": "weak_signal_reacquire", "capture_id": capture_id, "exposure_factor": 1.25, "rejected_features": [item["feature_id"] for item in exc.rejected]})
            return capture_source(purpose=f"{purpose}-weak-signal-reacquire", target=target, command=command, settled_confirmation=settled_confirmation, exposure_factor=1.25, allow_weak_reacquire=False, reacquire_of=capture_id)
        return {"capture_id": capture_id, "capture": capture, "feature_values": features}

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
        for target in plan_data["targets"]:
            expected_target = manifold.target_at(float(target["hue"]), float(target["sat"]))
            expected_hash = _mapping_sha256({feature: expected_target.features[feature] for feature in required_features})
            if expected_hash != target["target_feature_sha256"]:
                raise ValueError(f"P7 target feature hash drift at target {target['index']}")

            def feedback_capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool) -> dict[str, Any]:
                try:
                    observation = capture_source(purpose=f"candidate_{phase}", target=target, command=command, settled_confirmation=settled_confirmation)
                except WeakSignalEnvelopeExhausted as exc:
                    return {"measurement_rejected": True, "rejection_evidence": exc.evidence()}
                evaluated = evaluate_hsi_observation(
                    manifold,
                    observation["feature_values"],
                    target_hue=float(target["hue"]),
                    target_sat=float(target["sat"]),
                    command=command,
                    previous_command=previous_command,
                )
                return {**evaluated, "capture_id": observation["capture_id"]}

            seed = target["seed"]["best"]
            try:
                feedback = run_hsi_feedback(
                    initial_command=seed["command"],
                    active_channel=str(seed["active_channel"]),
                    capture_observation_fn=feedback_capture,
                    max_code=int(solver["max_code"]),
                    rounds=int(solver["max_rounds"]),
                    probe_step_code=int(solver["probe_step_code"]),
                    max_step_code=int(solver["max_step_code"]),
                    damping=float(solver["damping"]),
                    confirmations=int(confirmation["independent_repeats"]),
                    thermal_rebases=2,
                )
            except HsiMeasurementRejected as exc:
                record_unreachable(target, "strip_feedback_setup", {"phase": exc.phase, "command": exc.command, **exc.evidence})
                continue
            final_verification = []
            final_rejection = None
            if not feedback["goal_confirmed"]:
                for index in range(int(confirmation["independent_repeats"])):
                    final = feedback_capture(feedback["selected_command"], phase=f"final-verification-{index}", settled_confirmation=True)
                    if final.get("measurement_rejected"):
                        final_rejection = dict(final["rejection_evidence"])
                        break
                    final_verification.append({"capture_id": final["capture_id"], "residuals": {group: list(values) for group, values in final["residuals"].items()}, "objective": final["objective"]})
            if final_rejection is not None:
                record_unreachable(target, "strip_final_verification", final_rejection)
                continue
            final_pair_faithful = len(final_verification) == 2 and all(item["objective"]["feasible"] for item in final_verification)
            faithful = bool(feedback["goal_confirmed"] or final_pair_faithful)
            row = {
                "status": "complete",
                "target": target,
                "basis_seed": target["seed"],
                "feedback": feedback,
                "final_verification": final_verification,
                "gamut_status": "faithful" if faithful else "unconfirmed",
                "selected_command": feedback["selected_command"],
            }
            _append_jsonl(root / "target-results.jsonl", row)
            previous_command = {channel: int(feedback["selected_command"][channel]) for channel in CHANNELS}
            run["completed_target_count"] += 1
            _write_json(root / "run.json", run)
    except BaseException as exc:
        failure = exc
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
    finally:
        cleanup = {"at": _utc_now(), "steps": [step.to_jsonable() for step in all_off_fn()]}
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if run["completed_target_count"] == EXPECTED_TARGET_COUNT and all(item["ok"] for item in cleanup["steps"]) else "failed"
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
        strip_light_fn=lambda cw, ww, r, g, b: esphome.light(cw, ww, r, g, b, curve_path=curve_path),
        ray_off_fn=lambda: ray120c.set_cct(5600, intensity=0, gm=100),
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(curve_path=curve_path, camera_backend=camera_backend, backend_name="remote"),
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or execute the P7 strip HSI pilot.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--manifold-config", type=Path, default=DEFAULT_MANIFOLD_CONFIG)
    parser.add_argument("--basis-analysis", type=Path, default=DEFAULT_BASIS_ANALYSIS)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--target-max", type=int, default=19661)
    parser.add_argument("--min-shutter-speed", default="1/16000")
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
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
        "curve_path": args.curve,
        "target_max": args.target_max,
        "min_shutter_speed": args.min_shutter_speed,
        "max_shutter_speed": args.max_shutter_speed,
        "camera_backend": args.camera_backend,
    }
    if args.dry_run:
        print(write_strip_hsi_pilot_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
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
