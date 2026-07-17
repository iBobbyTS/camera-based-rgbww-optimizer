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

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote, esphome, ray120c, white_lut
from camera_based_rgbww_optimizer.measurement.chart_response_basis import CHANNELS, LEVEL_CODES
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "chart-basis-mixtures"
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
DEFAULT_SEED = 20260716
DEFAULT_REPEATS = 2
DEFAULT_SETTLE_SECONDS = 60.0
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_ANCHOR_CCT = 5600
DEFAULT_ANCHOR_GM = 100


def build_chart_basis_mixtures_plan(
    *,
    basis_analysis_path: str | Path = DEFAULT_BASIS_ANALYSIS,
    baseline_lut_path: str | Path = DEFAULT_BASELINE_LUT,
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
    if repeats != 2:
        raise ValueError("P3 requires exactly two independent repeats per mixture")
    if camera_backend != "remote":
        raise ValueError("new P3 experiments require camera_backend=remote")
    if off_seconds < 0 or settle_seconds < 0:
        raise ValueError("off_seconds and settle_seconds must be non-negative")

    observer_path = Path(observer_config_path)
    observer = json.loads(observer_path.read_text(encoding="utf-8"))
    validation = observer.get("validation", {})
    envelope = validation.get("exposure_envelope", {})
    if validation.get("raw_response_model") != "identity":
        raise ValueError("P3 requires the Gate-1 identity RAW response decision")
    if envelope.get("minimum_factor") != 1.0 or envelope.get("maximum_factor") != 1.25:
        raise ValueError("P3 requires the validated 1.0x..1.25x exposure envelope")
    if observer.get("statistics", {}).get("combine_green") is not False:
        raise ValueError("P3 requires four-plane G-C observer configuration")

    basis_path = Path(basis_analysis_path)
    basis = json.loads(basis_path.read_text(encoding="utf-8"))
    _validate_basis_analysis(basis)
    location_reference = _file_reference(Path(location_config_path))
    if basis["location_config_sha256"] != location_reference["sha256"]:
        raise ValueError("P2 basis and P3 location hashes do not match")

    lut_path = Path(baseline_lut_path)
    lut = white_lut.load_white_lut(lut_path)
    anchor_command = _lut_command(lut, DEFAULT_ANCHOR_CCT, DEFAULT_ANCHOR_GM)
    mixtures = _build_fixed_mixtures(lut)
    random.Random(random_seed).shuffle(mixtures)

    totals = [sum(item["command"].values()) for item in mixtures]
    split_load = sorted(totals)[len(totals) // 2]
    weak_command = min(mixtures, key=lambda item: sum(item["command"].values()))["command"]
    protection_command = max(mixtures, key=lambda item: sum(item["command"].values()))["command"]
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
        analysis_context.update(
            {
                "previous_state": previous_state,
                "total_target_load": 0 if command is None else sum(command.values()),
                "active_set": [] if command is None else [name for name in CHANNELS if command[name] > 0],
            }
        )
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
    add_capture(
        purpose="mixture_exposure_auto",
        command=protection_command,
        cache="mixture:protection",
        auto_exposure=True,
        context={"exposure_role": "protection"},
    )
    add_capture(
        purpose="mixture_exposure_auto",
        command=weak_command,
        cache="mixture:weak",
        auto_exposure=True,
        context={"exposure_role": "weak"},
    )
    add_capture(
        purpose="anchor_auto_exposure",
        command=anchor_command,
        cache="anchor",
        auto_exposure=True,
        context={"anchor_cct": DEFAULT_ANCHOR_CCT, "anchor_gm": DEFAULT_ANCHOR_GM},
    )
    for state_index, mixture in enumerate(mixtures, start=1):
        command = mixture["command"]
        role = "weak" if sum(command.values()) <= split_load else "protection"
        for repeat_index in range(repeats):
            add_capture(
                purpose="mixture_formal",
                command=command,
                cache=f"mixture:{role}",
                repeat_index=repeat_index,
                context={
                    "state_index": state_index,
                    "sample_id": mixture["sample_id"],
                    "category": mixture["category"],
                    "command": dict(command),
                    "exposure_role": role,
                },
            )
        if state_index in {8, 16, 24}:
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
            "kind": "camera_based_rgbww_optimizer_chart_basis_mixtures",
            "phase": "P3",
            "model_branch": "B-B",
            "level_dependent_channels": list(CHANNELS),
            "basis_interpolation": "piecewise_linear_normalized_columns_at_1024_2048_4095",
            "anchor": {"cct": DEFAULT_ANCHOR_CCT, "gm": DEFAULT_ANCHOR_GM, "strip_command": anchor_command},
            "mixture_count": len(mixtures),
            "repeats": repeats,
            "formal_capture_count": len(mixtures) * repeats,
            "random_seed": random_seed,
            "fixed_mixtures": mixtures,
            "feature_planes": ["R", "G1", "G2", "B"],
            "raw_response_model": "identity",
            "validated_exposure_envelope": copy.deepcopy(envelope),
            "camera_auto_exposure": {
                "target_max": int(target_max),
                "min_shutter_speed": str(min_shutter_speed),
                "max_shutter_speed": str(max_shutter_speed),
                "load_split": split_load,
            },
            "source_isolation": "every capture requires Ray off before strip is enabled",
        },
        "inputs": {
            "basis_analysis": _file_reference(basis_path),
            "baseline_lut": _file_reference(lut_path),
            "location_config": location_reference,
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


def write_chart_basis_mixtures_dry_run(
    *, output_root: str | Path, run_name: str | None, **plan_kwargs: Any
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_chart_basis_mixtures_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = datetime.now(timezone.utc).isoformat()
    plan["run_dir"] = str(run_dir)
    output = run_dir / "plan.json"
    output.write_text(json.dumps(plan, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return output


def run_chart_basis_mixtures(
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
        recorded_exposure_purpose="P3",
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
        phase="P3",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or run the P3 chart-basis mixture plan.")
    parser.add_argument("--basis-analysis", type=Path, default=DEFAULT_BASIS_ANALYSIS)
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
        "basis_analysis_path": args.basis_analysis,
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
        print(write_chart_basis_mixtures_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    plan = build_chart_basis_mixtures_plan(**kwargs)
    print(run_chart_basis_mixtures(plan, output_root=args.output_dir, run_name=args.run_name, curve_path=args.curve, camera_backend=backend))
    return 0


def _build_fixed_mixtures(lut: Mapping[str, Any]) -> list[dict[str, Any]]:
    groups: list[tuple[str, list[dict[str, int]]]] = [
        ("dominant_with_weak", [
            _command(cw=3072, ww=384), _command(ww=3072, r=384), _command(r=3072, g=384),
            _command(g=3072, b=384), _command(b=3072, cw=384),
        ]),
        ("white_rgb", [
            _command(cw=2048, ww=2048, r=768), _command(cw=2048, ww=2048, g=768),
            _command(cw=2048, ww=2048, b=768), _command(cw=1024, ww=3072, r=512, b=512),
            _command(cw=3072, ww=1024, g=512, b=512),
        ]),
        ("high_load", [
            _command(cw=4095, ww=4095, r=3072, g=3072, b=3072),
            _command(cw=4095, ww=3072, r=4095, g=2048, b=2048),
            _command(cw=3072, ww=4095, r=2048, g=4095, b=2048),
            _command(cw=3072, ww=3072, r=2048, g=2048, b=4095),
            _command(cw=4095, ww=4095, r=1024, g=4095, b=1024),
        ]),
        ("lut_nearby", [
            _lut_command(lut, 1800, 0), _lut_command(lut, 3200, 200), _lut_command(lut, 5600, 100),
            _lut_command(lut, 10000, 0), _lut_command(lut, 20000, 200),
        ]),
        ("latin_hypercube", [
            _command(cw=256, ww=1536, r=512, g=1024, b=768),
            _command(cw=1280, ww=256, r=1024, g=512, b=1536),
            _command(cw=768, ww=1024, r=1536, g=256, b=512),
            _command(cw=1536, ww=768, r=256, g=1280, b=1024),
        ]),
    ]
    mixtures: list[dict[str, Any]] = []
    for category, commands in groups:
        for index, command in enumerate(commands, start=1):
            mixtures.append({"sample_id": f"{category}-{index:02d}", "category": category, "command": command})
    if len(mixtures) != 24 or len({_command_state(item["command"]) for item in mixtures}) != 24:
        raise ValueError("P3 fixed mixture design must contain 24 unique commands")
    return mixtures


def _validate_basis_analysis(basis: Mapping[str, Any]) -> None:
    if basis.get("analysis") != "chart_response_basis" or basis.get("status") != "ready_for_manual_branch_review":
        raise ValueError("P3 requires a completed P2 basis analysis")
    if basis.get("channels") != list(CHANNELS) or basis.get("level_codes") != list(LEVEL_CODES):
        raise ValueError("P3 requires the five-channel 1024/2048/4095 P2 basis")
    if basis.get("plane_order") != ["R", "G1", "G2", "B"]:
        raise ValueError("P3 requires the frozen four-plane P2 basis")
    if any(basis["basis_by_level"][str(level)]["diagnostics"]["rank"] != 5 for level in LEVEL_CODES):
        raise ValueError("P3 B-B path requires rank-5 P2 bases at all levels")


def _lut_command(lut: Mapping[str, Any], cct: int, gm: int) -> dict[str, int]:
    resolved = white_lut.interpolate_white_lut(lut, cct, gm, clamp=False)["command"]
    return {channel: int(resolved[channel]) for channel in CHANNELS}


def _command(**values: int) -> dict[str, int]:
    command = {channel: int(values.get(channel, 0)) for channel in CHANNELS}
    if any(value < 0 or value > 4095 for value in command.values()):
        raise ValueError("channel commands must be within 0..4095")
    return command


def _command_state(command: Mapping[str, int]) -> str:
    return ",".join(f"{channel}={int(command[channel])}" for channel in CHANNELS)


def _file_reference(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


if __name__ == "__main__":
    raise SystemExit(main())
