from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "ray-hsi-manifold"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_SEED = 20260717
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_SETTLE_SECONDS = 60.0
HUES = tuple(range(0, 360, 30))
PRIMARY_HUES = (0, 60, 120, 180, 240, 300)
SATURATIONS = (5, 20, 50, 80, 95, 100)
RGB_ENDPOINTS = {
    "r": (255, 0, 0),
    "y": (255, 255, 0),
    "g": (0, 255, 0),
    "c": (0, 255, 255),
    "b": (0, 0, 255),
    "m": (255, 0, 255),
}
RGB_TO_HUE = {"r": 0, "y": 60, "g": 120, "c": 180, "b": 240, "m": 300}
EXPECTED_CAPTURE_COUNT = 106

CaptureStepFn = Callable[[Mapping[str, Any]], Mapping[str, Any]]
SleepFn = Callable[[float], None]
StripOffFn = Callable[[], Mapping[str, Any]]
RayModeFn = Callable[..., Mapping[str, Any]]
CleanupFn = Callable[..., Sequence[all_off.ShutdownStep]]
ProvenanceFn = Callable[[], Mapping[str, Any]]


def build_ray_hsi_manifold_plan(
    *,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    off_seconds: float = DEFAULT_OFF_SECONDS,
    settle_seconds: float = DEFAULT_SETTLE_SECONDS,
    random_seed: int = DEFAULT_SEED,
    camera_backend: str = "remote",
) -> dict[str, Any]:
    if camera_backend != "remote":
        raise ValueError("new P6 experiments require camera_backend=remote")
    if off_seconds < 0 or settle_seconds < 0:
        raise ValueError("off_seconds and settle_seconds must be non-negative")
    if not 1 <= int(target_max) <= 65535:
        raise ValueError("target_max must be between 1 and 65535")

    location_path = Path(location_config_path)
    observer_path = Path(observer_config_path)
    observer = json.loads(observer_path.read_text(encoding="utf-8"))
    validation = observer.get("validation", {})
    envelope = validation.get("exposure_envelope", {})
    if validation.get("raw_response_model") != "identity":
        raise ValueError("P6 requires the Gate-1 identity RAW response decision")
    if envelope.get("minimum_factor") != 1.0 or envelope.get("maximum_factor") != 1.25:
        raise ValueError("P6 requires the validated 1.0x..1.25x exposure envelope")
    if observer.get("statistics", {}).get("combine_green") is not False:
        raise ValueError("P6 requires four-plane G-C observer configuration")

    captures: list[dict[str, Any]] = []

    def add_capture(
        *,
        purpose: str,
        mode: str | None,
        state: Mapping[str, Any] | None,
        repeat_index: int | None = None,
        auto_exposure: bool = False,
        cache: str | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        index = len(captures)
        source = "ambient" if mode is None else "ray"
        captures.append(
            {
                "capture_id": f"{index:04d}-{source}-{purpose}",
                "index": index,
                "source": source,
                "purpose": purpose,
                "repeat_index": repeat_index,
                "exposure_factor": None,
                "source_exposure_cache": cache,
                "auto_exposure": bool(auto_exposure),
                "off_seconds_before": float(off_seconds),
                "settle_seconds": float(settle_seconds),
                "ray_mode": mode,
                "ray_state": None if state is None else dict(state),
                "ray": None,
                "strip_command": None,
                "other_source_must_be_off": True,
                "analysis_context": dict(context or {}),
            }
        )

    add_capture(purpose="ambient", mode=None, state=None)
    for hue in PRIMARY_HUES:
        add_capture(
            purpose="sat0_repeat",
            mode="hsi",
            state={"hue": hue, "sat": 0, "intensity_percent": 100.0},
            repeat_index=0,
            auto_exposure=True,
            cache=f"hsi:{hue}:0",
            context={"family": "sat0", "hue": hue, "sat": 0},
        )
    for name, rgb in RGB_ENDPOINTS.items():
        add_capture(
            purpose="rgb_endpoint",
            mode="rgb",
            state={"r": rgb[0], "g": rgb[1], "b": rgb[2], "intensity_percent": 100.0},
            repeat_index=0,
            auto_exposure=True,
            cache=f"rgb:{name}",
            context={"family": "rgb_endpoint", "endpoint": name, "matching_hue": RGB_TO_HUE[name]},
        )

    coarse_states = [(hue, sat) for hue in HUES for sat in SATURATIONS]
    random.Random(random_seed).shuffle(coarse_states)
    anchor_repeat = 1
    for state_index, (hue, sat) in enumerate(coarse_states, start=1):
        add_capture(
            purpose="hsi_coarse",
            mode="hsi",
            state={"hue": hue, "sat": sat, "intensity_percent": 100.0},
            repeat_index=0,
            auto_exposure=True,
            cache=f"hsi:{hue}:{sat}",
            context={"family": "hsi_coarse", "state_index": state_index, "hue": hue, "sat": sat},
        )
        if state_index in {24, 48, 72}:
            add_capture(
                purpose="sat0_anchor",
                mode="hsi",
                state={"hue": 0, "sat": 0, "intensity_percent": 100.0},
                repeat_index=anchor_repeat,
                cache="hsi:0:0",
                context={"family": "sat0", "hue": 0, "sat": 0, "after_coarse_state": state_index},
            )
            anchor_repeat += 1

    for hue in PRIMARY_HUES:
        add_capture(
            purpose="hsi_endpoint_repeat",
            mode="hsi",
            state={"hue": hue, "sat": 100, "intensity_percent": 100.0},
            repeat_index=1,
            cache=f"hsi:{hue}:100",
            context={"family": "hsi_coarse", "hue": hue, "sat": 100},
        )
    for name, rgb in RGB_ENDPOINTS.items():
        add_capture(
            purpose="rgb_endpoint",
            mode="rgb",
            state={"r": rgb[0], "g": rgb[1], "b": rgb[2], "intensity_percent": 100.0},
            repeat_index=1,
            cache=f"rgb:{name}",
            context={"family": "rgb_endpoint", "endpoint": name, "matching_hue": RGB_TO_HUE[name]},
        )
    for hue in PRIMARY_HUES:
        add_capture(
            purpose="sat0_repeat",
            mode="hsi",
            state={"hue": hue, "sat": 0, "intensity_percent": 100.0},
            repeat_index=4 if hue == 0 else 1,
            cache=f"hsi:{hue}:0",
            context={"family": "sat0", "hue": hue, "sat": 0},
        )

    if len(captures) != EXPECTED_CAPTURE_COUNT:
        raise AssertionError(f"P6 plan must contain {EXPECTED_CAPTURE_COUNT} captures, got {len(captures)}")
    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_ray_hsi_manifold",
            "phase": "P6",
            "intensity_percent": 100.0,
            "hues": list(HUES),
            "primary_hues": list(PRIMARY_HUES),
            "saturations": list(SATURATIONS),
            "base_state_count": 73,
            "capture_count": EXPECTED_CAPTURE_COUNT,
            "random_seed": int(random_seed),
            "feature_planes": ["R", "G1", "G2", "B"],
            "raw_response_model": "identity",
            "validated_exposure_envelope": copy.deepcopy(envelope),
            "camera_auto_exposure": {
                "target_max": int(target_max),
                "min_shutter_speed": str(min_shutter_speed),
                "max_shutter_speed": str(max_shutter_speed),
            },
            "source_isolation": "strip is explicitly off for every capture; only Ray may be enabled",
            "readback": "required immediately after every Ray command",
        },
        "inputs": {
            "location_config": _file_reference(location_path),
            "raw_observer_config": _file_reference(observer_path),
        },
        "devices": {"camera": {"backend": camera_backend, "credentials": "loaded_by_script_not_recorded"}},
        "captures": captures,
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted even though P6 only enables Ray",
        },
    }


def write_ray_hsi_manifold_dry_run(
    *, output_root: str | Path, run_name: str | None, **plan_kwargs: Any
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_ray_hsi_manifold_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = _utc_now()
    plan["run_dir"] = str(run_dir)
    output = run_dir / "plan.json"
    _write_json(output, plan)
    return output


def execute_ray_hsi_manifold_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    strip_off_fn: StripOffFn,
    ray_set_hsi_fn: RayModeFn,
    ray_get_hsi_fn: RayModeFn,
    ray_set_rgb_fn: RayModeFn,
    ray_get_rgb_fn: RayModeFn,
    ray_off_fn: Callable[[], Mapping[str, Any]],
    capture_step_fn: CaptureStepFn,
    sleep_fn: SleepFn,
    cleanup_fn: CleanupFn = all_off.turn_everything_off,
    provenance_fn: ProvenanceFn | None = None,
) -> Path:
    plan_data = copy.deepcopy(dict(plan))
    _validate_executable_plan(plan_data)
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 1,
        "run_id": root.name,
        "phase": "P6",
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "completed_capture_count": 0,
        "inputs": copy.deepcopy(plan_data["inputs"]),
        "measurement": copy.deepcopy(plan_data["measurement"]),
        "devices": copy.deepcopy(plan_data["devices"]),
        "provenance": {"status": "pending" if provenance_fn else "not_collected"},
    }
    _write_json(root / "run.json", run)
    failure: BaseException | None = None
    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("P6 provenance collector must return a mapping")
            run["provenance"] = copy.deepcopy(dict(provenance))
            _write_json(root / "run.json", run)
        for step in plan_data["captures"]:
            _prepare_source(
                step,
                strip_off_fn=strip_off_fn,
                ray_set_hsi_fn=ray_set_hsi_fn,
                ray_get_hsi_fn=ray_get_hsi_fn,
                ray_set_rgb_fn=ray_set_rgb_fn,
                ray_get_rgb_fn=ray_get_rgb_fn,
                ray_off_fn=ray_off_fn,
                sleep_fn=sleep_fn,
                command_log=root / "commands.jsonl",
            )
            try:
                _append_jsonl(root / "commands.jsonl", {"event": "capture_requested", "at": _utc_now(), "capture_id": step["capture_id"], "source": step["source"]})
                capture = dict(capture_step_fn(copy.deepcopy(step)))
                _append_jsonl(
                    root / "captures.jsonl",
                    {
                        "capture_id": step["capture_id"],
                        "source": step["source"],
                        "purpose": step["purpose"],
                        "repeat_index": step["repeat_index"],
                        "analysis_context": copy.deepcopy(step["analysis_context"]),
                        "ray_mode": step["ray_mode"],
                        "ray_state": copy.deepcopy(step["ray_state"]),
                        "capture": capture,
                    },
                )
                run["completed_capture_count"] += 1
                _write_json(root / "run.json", run)
            finally:
                if step["source"] == "ray":
                    response = ray_off_fn()
                    _append_jsonl(root / "commands.jsonl", {"event": "ray_off", "at": _utc_now(), "capture_id": step["capture_id"], "response": response})
    except BaseException as exc:
        failure = exc
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
    finally:
        cleanup = [step.to_jsonable() for step in cleanup_fn()]
        _write_json(root / "all-off-python.json", {"at": _utc_now(), "steps": cleanup})
        if run["status"] == "running":
            run["status"] = "complete" if all(item["ok"] for item in cleanup) else "failed"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    return root


def run_ray_hsi_manifold(
    plan: Mapping[str, Any], *, output_root: str | Path, run_name: str | None,
    camera_backend: camera_gphoto2.CameraBackend,
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
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
        recorded_exposure_purpose="P6",
    )
    return execute_ray_hsi_manifold_plan(
        plan,
        run_dir=run_dir,
        strip_off_fn=lambda: esphome.light(0, 0, 0, 0, 0),
        ray_set_hsi_fn=ray120c.set_hsi,
        ray_get_hsi_fn=ray120c.get_hsi,
        ray_set_rgb_fn=ray120c.set_rgb,
        ray_get_rgb_fn=ray120c.get_rgb,
        ray_off_fn=lambda: ray120c.set_cct(5600, intensity=0, gm=100),
        capture_step_fn=capture_step,
        sleep_fn=time.sleep,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(
            curve_path=None, camera_backend=camera_backend, backend_name="remote"
        ),
    )


def _prepare_source(
    step: Mapping[str, Any], *, strip_off_fn: StripOffFn,
    ray_set_hsi_fn: RayModeFn, ray_get_hsi_fn: RayModeFn,
    ray_set_rgb_fn: RayModeFn, ray_get_rgb_fn: RayModeFn,
    ray_off_fn: Callable[[], Mapping[str, Any]], sleep_fn: SleepFn, command_log: Path,
) -> None:
    strip_response = strip_off_fn()
    _append_jsonl(command_log, {"event": "strip_off", "at": _utc_now(), "capture_id": step["capture_id"], "response": strip_response})
    off_response = ray_off_fn()
    _append_jsonl(command_log, {"event": "ray_off", "at": _utc_now(), "capture_id": step["capture_id"], "response": off_response})
    sleep_fn(float(step["off_seconds_before"]))
    if step["source"] == "ambient":
        return
    mode = str(step["ray_mode"])
    state = dict(step["ray_state"])
    if mode == "hsi":
        set_response = ray_set_hsi_fn(int(state["hue"]), int(state["sat"]), intensity_percent=float(state["intensity_percent"]))
        readback = ray_get_hsi_fn()
        expected = {"hue": int(state["hue"]), "sat": int(state["sat"]), "intensity": ray120c.intensity_percent_to_raw(float(state["intensity_percent"]))}
    elif mode == "rgb":
        set_response = ray_set_rgb_fn(int(state["r"]), int(state["g"]), int(state["b"]), intensity_percent=float(state["intensity_percent"]))
        readback = ray_get_rgb_fn()
        expected = {"r": int(state["r"]), "g": int(state["g"]), "b": int(state["b"]), "intensity": ray120c.intensity_percent_to_raw(float(state["intensity_percent"]))}
    else:
        raise ValueError(f"unsupported Ray mode: {mode}")
    _verify_readback(readback, expected, mode=mode)
    _append_jsonl(command_log, {"event": "ray_on_readback_verified", "at": _utc_now(), "capture_id": step["capture_id"], "mode": mode, "expected": expected, "set_response": set_response, "readback": readback})
    sleep_fn(float(step["settle_seconds"]))


def _verify_readback(response: Mapping[str, Any], expected: Mapping[str, int], *, mode: str) -> None:
    if response.get("code") not in (None, 0):
        raise RuntimeError(f"Ray {mode} readback failed: {response}")
    data = response.get("data")
    if not isinstance(data, Mapping):
        raise RuntimeError(f"Ray {mode} readback has no data mapping")
    mismatches = {key: {"expected": value, "actual": data.get(key)} for key, value in expected.items() if data.get(key) != value}
    if mismatches:
        raise RuntimeError(f"Ray {mode} readback mismatch: {mismatches}")


def _validate_executable_plan(plan: Mapping[str, Any]) -> None:
    if plan.get("status") not in {"planned", "dry_run"}:
        raise ValueError("P6 plan status must be planned or dry_run")
    measurement = plan.get("measurement", {})
    if measurement.get("phase") != "P6" or measurement.get("capture_count") != EXPECTED_CAPTURE_COUNT:
        raise ValueError("P6 executable plan has an invalid phase or capture count")
    captures = plan.get("captures")
    if not isinstance(captures, list) or len(captures) != EXPECTED_CAPTURE_COUNT:
        raise ValueError(f"P6 requires exactly {EXPECTED_CAPTURE_COUNT} capture steps")
    if any(step.get("source") not in {"ambient", "ray"} or step.get("strip_command") is not None for step in captures):
        raise ValueError("P6 plan may only contain ambient and Ray captures")


def _file_reference(path: Path) -> dict[str, Any]:
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or execute the P6 Ray-only HSI manifold plan.")
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--target-max", type=int, default=19661)
    parser.add_argument("--min-shutter-speed", default="1/16000")
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--off-seconds", type=float, default=DEFAULT_OFF_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--random-seed", type=int, default=DEFAULT_SEED)
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
        "location_config_path": args.location_config,
        "observer_config_path": args.raw_observer_config,
        "target_max": args.target_max,
        "min_shutter_speed": args.min_shutter_speed,
        "max_shutter_speed": args.max_shutter_speed,
        "off_seconds": args.off_seconds,
        "settle_seconds": args.settle_seconds,
        "random_seed": args.random_seed,
        "camera_backend": args.camera_backend,
    }
    if args.dry_run:
        print(write_ray_hsi_manifold_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output:
        raise SystemExit("--execute requires --allow-high-output")
    if args.camera_backend != "remote":
        raise SystemExit("P6 real acquisition requires --camera-backend remote")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    plan = build_ray_hsi_manifold_plan(**kwargs)
    output = run_ray_hsi_manifold(plan, output_root=args.output_dir, run_name=args.run_name, camera_backend=backend)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
