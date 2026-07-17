from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote, esphome, ray120c, white_lut as white_lut_control
from camera_based_rgbww_optimizer.measurement.chart_response_basis import CHANNELS, LEVEL_CODES
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "chart-response-basis"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_BASELINE_LUT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/"
    "14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json"
)
DEFAULT_SEED = 20260716
DEFAULT_REPEATS = 3
DEFAULT_SETTLE_SECONDS = 60.0
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_ANCHOR_CCT = 5600
DEFAULT_ANCHOR_GM = 100


def build_chart_response_basis_plan(
    *,
    baseline_lut_path: str | Path,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    curve_path: str | Path = esphome.DEFAULT_CURVE_PATH,
    repeats: int = DEFAULT_REPEATS,
    random_seed: int = DEFAULT_SEED,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    off_seconds: float = DEFAULT_OFF_SECONDS,
    settle_seconds: float = DEFAULT_SETTLE_SECONDS,
    camera_backend: str = "remote",
) -> dict[str, Any]:
    if repeats != 3:
        raise ValueError("P2 requires exactly three independent repeats per state")
    if camera_backend != "remote":
        raise ValueError("new P2 experiments require camera_backend=remote")
    if off_seconds < 0 or settle_seconds < 0:
        raise ValueError("off_seconds and settle_seconds must be non-negative")

    observer_path = Path(observer_config_path)
    observer = json.loads(observer_path.read_text(encoding="utf-8"))
    validation = observer.get("validation", {})
    envelope = validation.get("exposure_envelope", {})
    if validation.get("raw_response_model") != "identity":
        raise ValueError("P2 requires the Gate-1 identity RAW response decision")
    if envelope.get("minimum_factor") != 1.0 or envelope.get("maximum_factor") != 1.25:
        raise ValueError("P2 requires the validated 1.0x..1.25x exposure envelope")
    if observer.get("statistics", {}).get("combine_green") is not False:
        raise ValueError("P2 requires four-plane G-C observer configuration")

    lut_path = Path(baseline_lut_path)
    anchor = white_lut_control.interpolate_white_lut(
        white_lut_control.load_white_lut(lut_path),
        DEFAULT_ANCHOR_CCT,
        DEFAULT_ANCHOR_GM,
        clamp=False,
    )["command"]
    anchor_command = {channel: int(anchor[channel]) for channel in CHANNELS}
    captures: list[dict[str, Any]] = []
    previous_state: str | None = None

    def add_capture(
        *,
        purpose: str,
        command: Mapping[str, int] | None,
        cache: str | None = None,
        auto_exposure: bool = False,
        repeat_index: int | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        nonlocal previous_state
        index = len(captures)
        source = "ambient" if command is None else "strip"
        state = "ambient" if command is None else _command_state(command)
        analysis_context = dict(context or {})
        analysis_context.update({"previous_state": previous_state, "total_target_load": 0 if command is None else sum(command.values())})
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
                "ray": None,
                "strip_command": None if command is None else dict(command),
                "other_source_must_be_off": True,
                "analysis_context": analysis_context,
            }
        )
        previous_state = state

    add_capture(purpose="ambient", command=None)
    calibration_states = [(channel, role) for channel in CHANNELS for role in ("protection", "weak")]
    random.Random(random_seed ^ 0xA5A5).shuffle(calibration_states)
    for channel, role in calibration_states:
        code = 4095 if role == "protection" else 1024
        add_capture(
            purpose="basis_exposure_auto",
            command=_single_channel_command(channel, code),
            cache=f"{channel}:{role}",
            auto_exposure=True,
            context={"channel": channel, "target_code": code, "exposure_role": role},
        )
    add_capture(
        purpose="anchor_auto_exposure",
        command=anchor_command,
        cache="anchor",
        auto_exposure=True,
        context={"anchor_cct": DEFAULT_ANCHOR_CCT, "anchor_gm": DEFAULT_ANCHOR_GM},
    )

    states = [(channel, code) for channel in CHANNELS for code in LEVEL_CODES]
    random.Random(random_seed).shuffle(states)
    for state_index, (channel, code) in enumerate(states, start=1):
        role = "weak" if code == 1024 else "protection"
        for repeat_index in range(repeats):
            add_capture(
                purpose="basis_formal",
                command=_single_channel_command(channel, code),
                cache=f"{channel}:{role}",
                repeat_index=repeat_index,
                context={
                    "state_index": state_index,
                    "channel": channel,
                    "target_code": code,
                    "level_fraction": code / 4095.0,
                    "exposure_role": role,
                },
            )
        if state_index == 8:
            add_capture(
                purpose="anchor_check",
                command=anchor_command,
                cache="anchor",
                context={"after_state_index": state_index, "anchor_cct": DEFAULT_ANCHOR_CCT, "anchor_gm": DEFAULT_ANCHOR_GM},
            )

    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_chart_response_basis",
            "phase": "P2",
            "anchor": {
                "cct": DEFAULT_ANCHOR_CCT,
                "gm": DEFAULT_ANCHOR_GM,
                "strip_command": anchor_command,
            },
            "channels": list(CHANNELS),
            "level_codes": list(LEVEL_CODES),
            "repeats": repeats,
            "random_seed": random_seed,
            "feature_planes": ["R", "G1", "G2", "B"],
            "raw_response_model": "identity",
            "validated_exposure_envelope": copy.deepcopy(envelope),
            "camera_auto_exposure": {
                "target_max": int(target_max),
                "min_shutter_speed": str(min_shutter_speed),
                "max_shutter_speed": str(max_shutter_speed),
            },
            "source_isolation": "every capture requires Ray off before strip is enabled",
        },
        "inputs": {
            "baseline_lut": _file_reference(lut_path),
            "location_config": _file_reference(Path(location_config_path)),
            "raw_observer_config": _file_reference(observer_path),
            "code_duty_curve": _file_reference(Path(curve_path)),
        },
        "devices": {"camera": {"backend": camera_backend, "credentials": "loaded_by_script_not_recorded"}},
        "captures": captures,
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted_even_if_one_shutdown_fails",
        },
    }


def write_chart_response_basis_dry_run(
    *, output_root: str | Path, run_name: str | None, **plan_kwargs: Any
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_chart_response_basis_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = datetime.now(timezone.utc).isoformat()
    plan["run_dir"] = str(run_dir)
    output = run_dir / "plan.json"
    output.write_text(json.dumps(plan, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return output


def run_chart_response_basis(
    plan: Mapping[str, Any], *, output_root: str | Path, run_name: str | None,
    curve_path: str | Path, camera_backend: camera_gphoto2.CameraBackend,
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
        recorded_exposure_purpose="P2",
    )
    return raw_validation.execute_raw_observer_validation_plan(
        plan,
        run_dir=run_dir,
        strip_light_fn=lambda cw, ww, r, g, b: esphome.light(cw, ww, r, g, b, curve_path=curve_path),
        ray_set_cct_fn=ray120c.set_cct,
        capture_step_fn=capture_step,
        sleep_fn=time.sleep,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(
            curve_path=curve_path, camera_backend=camera_backend, backend_name="remote"
        ),
        phase="P2",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or run the P2 five-channel chart response basis plan.")
    parser.add_argument("--baseline-lut", type=Path, default=DEFAULT_BASELINE_LUT)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)
    parser.add_argument("--random-seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--target-max", type=int, default=19661)
    parser.add_argument("--min-shutter-speed", default="1/16000")
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--off-seconds", type=float, default=DEFAULT_OFF_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
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
        "baseline_lut_path": args.baseline_lut,
        "location_config_path": args.location_config,
        "observer_config_path": args.raw_observer_config,
        "curve_path": args.curve,
        "repeats": args.repeats,
        "random_seed": args.random_seed,
        "target_max": args.target_max,
        "min_shutter_speed": args.min_shutter_speed,
        "max_shutter_speed": args.max_shutter_speed,
        "off_seconds": args.off_seconds,
        "settle_seconds": args.settle_seconds,
        "camera_backend": args.camera_backend,
    }
    if args.dry_run:
        print(write_chart_response_basis_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    plan = build_chart_response_basis_plan(**kwargs)
    print(run_chart_response_basis(plan, output_root=args.output_dir, run_name=args.run_name, curve_path=args.curve, camera_backend=backend))
    return 0


def _single_channel_command(channel: str, code: int) -> dict[str, int]:
    if channel not in CHANNELS:
        raise ValueError(f"unsupported channel: {channel}")
    return {name: int(code) if name == channel else 0 for name in CHANNELS}


def _command_state(command: Mapping[str, int]) -> str:
    return ",".join(f"{channel}={int(command[channel])}" for channel in CHANNELS)


def _file_reference(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


if __name__ == "__main__":
    raise SystemExit(main())
