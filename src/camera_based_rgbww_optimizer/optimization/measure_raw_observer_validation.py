from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, esphome, ray120c, white_lut as white_lut_control
from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "raw-observer-validation"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260709-012045.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_WHITE_LUT = PROJECT_ROOT / "config" / "white" / "white-lut.json"
DEFAULT_WHITE_ENDPOINTS = PROJECT_ROOT / "config" / "white" / "white-endpoints.json"
DEFAULT_ANCHOR_CCT = 5600
DEFAULT_ANCHOR_GM = 100
DEFAULT_RAY_INTENSITY_PERCENT = 100.0
DEFAULT_PAIRED_REPEATS = 5
DEFAULT_LINEARITY_FACTORS = (0.5, 1.0, 2.0)
DEFAULT_LINEARITY_REPEATS = 3
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_SETTLE_SECONDS = 60.0

StripLightFn = Callable[[int, int, int, int, int], Mapping[str, Any]]
RaySetCctFn = Callable[..., Mapping[str, Any]]
CaptureStepFn = Callable[[Mapping[str, Any]], Mapping[str, Any]]
SleepFn = Callable[[float], None]
RawMeterFn = Callable[..., raw_mosaic_patches.RawExposureMeterResult]
RawAnalyzeFn = Callable[..., Mapping[str, Any]]
RawReportWriter = Callable[[str | Path, Mapping[str, Any]], Path]
ShutterChoicesFn = Callable[[str], Sequence[str]]
ProvenanceFn = Callable[[], Mapping[str, Any]]


def build_raw_observer_validation_plan(
    *,
    baseline_lut_path: str | Path,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    curve_path: str | Path | None = esphome.DEFAULT_CURVE_PATH,
    anchor_cct: int = DEFAULT_ANCHOR_CCT,
    anchor_gm: int = DEFAULT_ANCHOR_GM,
    ray_intensity_percent: float = DEFAULT_RAY_INTENSITY_PERCENT,
    paired_repeats: int = DEFAULT_PAIRED_REPEATS,
    linearity_factors: Sequence[float] = DEFAULT_LINEARITY_FACTORS,
    linearity_repeats: int = DEFAULT_LINEARITY_REPEATS,
    off_seconds: float = DEFAULT_OFF_SECONDS,
    settle_seconds: float = DEFAULT_SETTLE_SECONDS,
    include_flat_field: bool = False,
) -> dict[str, Any]:
    """Build the P1 capture order without connecting to camera or lights."""

    if paired_repeats < 1:
        raise ValueError("paired_repeats must be at least 1")
    if linearity_repeats < 1:
        raise ValueError("linearity_repeats must be at least 1")
    factors = _validate_linearity_factors(linearity_factors)
    if off_seconds < 0 or settle_seconds < 0:
        raise ValueError("off_seconds and settle_seconds must be non-negative")
    if not 0.0 <= float(ray_intensity_percent) <= 100.0:
        raise ValueError("ray_intensity_percent must be between 0 and 100")

    lut_path = Path(baseline_lut_path)
    interpolation = white_lut_control.interpolate_white_lut(
        white_lut_control.load_white_lut(lut_path),
        anchor_cct,
        anchor_gm,
        clamp=False,
    )
    strip_command = {channel: int(value) for channel, value in interpolation["command"].items()}
    captures: list[dict[str, Any]] = []

    def add_capture(
        *,
        source: str,
        purpose: str,
        repeat_index: int | None = None,
        exposure_factor: float | None = None,
        source_cache: str | None = None,
    ) -> None:
        index = len(captures)
        captures.append(
            {
                "capture_id": f"{index:04d}-{source}-{purpose}",
                "index": index,
                "source": source,
                "purpose": purpose,
                "repeat_index": repeat_index,
                "exposure_factor": exposure_factor,
                "source_exposure_cache": source_cache,
                "off_seconds_before": float(off_seconds),
                "settle_seconds": float(settle_seconds),
                "ray": (
                    None
                    if source not in {"ray", "flat_field_ray"}
                    else {"cct": int(anchor_cct), "gm": int(anchor_gm), "intensity_percent": float(ray_intensity_percent)}
                ),
                "strip_command": strip_command if source == "strip" else None,
                "other_source_must_be_off": True,
            }
        )

    add_capture(source="ambient", purpose="ambient")
    add_capture(source="ray", purpose="baseline_auto_exposure", source_cache="ray")
    add_capture(source="strip", purpose="baseline_auto_exposure", source_cache="strip")

    for repeat_index in range(paired_repeats):
        source_order = ("ray", "strip") if repeat_index % 2 == 0 else ("strip", "ray")
        for source in source_order:
            add_capture(
                source=source,
                purpose="paired_repeat",
                repeat_index=repeat_index,
                source_cache=source,
            )

    for repeat_index in range(linearity_repeats):
        ordered_factors = factors if repeat_index % 2 == 0 else tuple(reversed(factors))
        for factor_index, factor in enumerate(ordered_factors):
            source_order = ("ray", "strip") if (repeat_index + factor_index) % 2 == 0 else ("strip", "ray")
            for source in source_order:
                add_capture(
                    source=source,
                    purpose="linearity_bracket",
                    repeat_index=repeat_index,
                    exposure_factor=factor,
                    source_cache=source,
                )

    # A color-chart white patch cannot stand in for a spatial flat field.
    # Preserve that limitation explicitly when no repeatable diffuser is supplied.
    flat_field = {"status": "not_available", "reason": "no_repeatable_flat_field_material"}
    if include_flat_field:
        add_capture(source="flat_field_ray", purpose="flat_field", source_cache="ray")
        flat_field = {"status": "planned", "capture_id": captures[-1]["capture_id"]}

    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_raw_observer_validation",
            "anchor": {
                "cct": int(anchor_cct),
                "gm": int(anchor_gm),
                "ray_intensity_percent": float(ray_intensity_percent),
                "strip_command": strip_command,
            },
            "paired_repeats": int(paired_repeats),
            "linearity_factors": list(factors),
            "linearity_repeats": int(linearity_repeats),
            "flat_field": flat_field,
            "source_isolation": "every capture requires the other source to be off",
        },
        "inputs": {
            "baseline_lut": _file_reference(lut_path),
            "default_white_lut": _file_reference(DEFAULT_WHITE_LUT),
            "white_endpoints": _file_reference(DEFAULT_WHITE_ENDPOINTS),
            "location_config": _file_reference(Path(location_config_path)),
            "code_duty_curve": _file_reference_or_disabled(curve_path),
            "raw_observer_config": _file_reference(Path(observer_config_path)),
        },
        "captures": captures,
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted_even_if_one_shutdown_fails",
        },
    }


def write_raw_observer_validation_dry_run(
    *,
    output_root: str | Path,
    run_name: str | None,
    **plan_kwargs: Any,
) -> Path:
    """Write exactly the immutable dry-run plan and perform no device I/O."""

    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_raw_observer_validation_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = datetime.now(timezone.utc).isoformat()
    plan["run_dir"] = str(run_dir)
    output = run_dir / "plan.json"
    _write_json(output, plan)
    return output


def execute_raw_observer_validation_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    strip_light_fn: StripLightFn,
    ray_set_cct_fn: RaySetCctFn,
    capture_step_fn: CaptureStepFn,
    sleep_fn: SleepFn,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    provenance_fn: ProvenanceFn | None = None,
) -> Path:
    """Execute a prebuilt P1 plan with injected device operations and final shutdown.

    The public CLI deliberately does not invoke this function yet. Keeping the
    device operations injected makes the source-isolation and cleanup contract
    independently testable before a hardware runner is exposed.
    """

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
        "phase": "P1",
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "inputs": copy.deepcopy(plan_data["inputs"]),
        "measurement": copy.deepcopy(plan_data["measurement"]),
        "safety": {"source_isolation": plan_data["measurement"]["source_isolation"]},
        "provenance": {"status": "pending" if provenance_fn is not None else "not_collected"},
    }
    _write_json(root / "run.json", run)
    _write_experiment_summary(root, run=run, plan=plan_data)
    failure: BaseException | None = None
    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("P1 provenance collector must return a mapping")
            run["provenance"] = copy.deepcopy(dict(provenance))
            _write_json(root / "run.json", run)
        for step in plan_data["captures"]:
            _prepare_capture_source(
                step,
                strip_light_fn=strip_light_fn,
                ray_set_cct_fn=ray_set_cct_fn,
                sleep_fn=sleep_fn,
                command_log=root / "commands.jsonl",
            )
            _append_jsonl(
                root / "commands.jsonl",
                {
                    "event": "capture_requested",
                    "at": _utc_now(),
                    "capture_id": step["capture_id"],
                    "source": step["source"],
                    "purpose": step["purpose"],
                },
            )
            capture = dict(capture_step_fn(copy.deepcopy(step)))
            _append_jsonl(
                root / "captures.jsonl",
                {
                    "capture_id": step["capture_id"],
                    "source": step["source"],
                    "purpose": step["purpose"],
                    "repeat_index": step["repeat_index"],
                    "exposure_factor": step["exposure_factor"],
                    "capture": capture,
                },
            )
            _deactivate_capture_source(
                step,
                strip_light_fn=strip_light_fn,
                ray_set_cct_fn=ray_set_cct_fn,
                command_log=root / "commands.jsonl",
            )
    except BaseException as exc:
        failure = exc
        _write_json(
            root / "failure.json",
            {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)},
        )
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
    finally:
        cleanup = _run_python_cleanup(
            plan_data,
            strip_light_fn=strip_light_fn,
            ray_set_cct_fn=ray_set_cct_fn,
            all_off_fn=all_off_fn,
        )
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if _cleanup_succeeded(cleanup) else "failed"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
        _write_experiment_summary(root, run=run, plan=plan_data, cleanup=cleanup)
    if failure is not None:
        raise failure
    return root


def build_native_raw_capture_step_fn(
    *,
    camera_dir: str | Path,
    measurements_dir: str | Path,
    scratch_dir: str | Path,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    ambient_shutter_speed: str = "30",
    iso: str = camera_gphoto2.DEFAULT_ISO,
    aperture: str = camera_gphoto2.DEFAULT_APERTURE,
    image_format: str = camera_gphoto2.DEFAULT_IMAGE_FORMAT,
    target_max: int = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX,
    min_shutter_speed: str = camera_gphoto2.DEFAULT_MIN_SHUTTER_SPEED,
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    max_trials: int = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_TRIALS,
    max_captures: int = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_CAPTURES,
    auto_expose_fn: Callable[..., camera_gphoto2.AutoExposureResult] = camera_gphoto2.auto_expose_capture,
    capture_fn: Callable[..., camera_gphoto2.CaptureResult] = camera_gphoto2.capture_image,
    raw_meter_fn: RawMeterFn = raw_mosaic_patches.meter_raw_exposure,
    raw_analyze_fn: RawAnalyzeFn = raw_mosaic_patches.analyze_raw_file,
    raw_report_writer: RawReportWriter = raw_mosaic_patches.write_report,
    shutter_choices_fn: ShutterChoicesFn | None = None,
) -> CaptureStepFn:
    """Build the production camera side of P1 while leaving device control injected.

    The returned callback is intentionally not bound to the CLI. It keeps
    source-specific auto-exposure caches, records native Bayer reports without
    `.npy` output, and resolves bracket shutters against camera-supported
    choices. The outer executor remains responsible for Ray/strip isolation.
    """

    camera_output = Path(camera_dir)
    measurements_output = Path(measurements_dir)
    scratch_output = Path(scratch_dir)
    source_captures: dict[str, camera_gphoto2.CaptureResult] = {}
    ambient_capture: camera_gphoto2.CaptureResult | None = None
    shutter_choices_by_port: dict[str, tuple[str, ...]] = {}

    def meter(raw_file: Path) -> camera_gphoto2.ExposureMeasurement:
        result = raw_meter_fn(
            raw_file,
            location_config_path=location_config_path,
            observer_config_path=observer_config_path,
        )
        channel_max = tuple(
            int(round(max(0.0, min(1.0, float(result.plane_max.get(label) or 0.0))) * 65535.0))
            for label in raw_mosaic_patches.PLANE_ORDER
        )
        return camera_gphoto2.ExposureMeasurement(
            maximum=int(result.exposure_metric),
            raw_visible_max=result.raw_visible_max,
            channel_max=channel_max,
            exposure_metric=float(result.exposure_metric),
            details=result.to_jsonable(),
        )

    def capture_step(step: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal ambient_capture
        source = str(step["source"])
        filename = _capture_filename(step)
        if source == "ambient":
            capture = capture_fn(
                output_dir=camera_output,
                filename_template=filename,
                settings=camera_gphoto2.CaptureSettings(
                    iso=iso,
                    aperture=aperture,
                    shutter_speed=ambient_shutter_speed,
                    image_format=image_format,
                ),
                timeout=120.0,
            )
            ambient_capture = capture
            mode = "ambient_fixed"
        elif str(step["purpose"]) == "baseline_auto_exposure":
            cache_key = _source_cache_key(step)
            auto = auto_expose_fn(
                output_dir=camera_output,
                filename_template=filename,
                target_max=target_max,
                iso=iso,
                aperture=aperture,
                image_format=image_format,
                min_shutter_speed=min_shutter_speed,
                max_shutter_speed=max_shutter_speed,
                max_trials=max_trials,
                max_captures=max_captures,
                decode_formats=(),
                scratch_dir=scratch_output,
                initial_shutter_speed=(source_captures.get(cache_key).settings.shutter_speed if cache_key in source_captures else None),
                meter_fn=meter,
                preserve_failed_trial_dir=camera_output / "failed-auto-exposure-trials",
            )
            capture = auto.final_capture
            source_captures[cache_key] = capture
            mode = "native_auto_exposure"
        else:
            cache_key = _source_cache_key(step)
            base_capture = source_captures.get(cache_key)
            if base_capture is None:
                raise ValueError(f"capture {step['capture_id']} has no {cache_key} exposure baseline")
            shutter_speed = base_capture.settings.shutter_speed
            if str(step["purpose"]) == "linearity_bracket":
                shutter_speed = _resolve_bracket_shutter_speed(
                    base_capture,
                    factor=float(step["exposure_factor"]),
                    min_shutter_speed=min_shutter_speed,
                    max_shutter_speed=max_shutter_speed,
                    shutter_choices_fn=shutter_choices_fn,
                    choices_cache=shutter_choices_by_port,
                )
            capture = capture_fn(
                output_dir=camera_output,
                filename_template=filename,
                settings=camera_gphoto2.CaptureSettings(
                    iso=iso,
                    aperture=aperture,
                    shutter_speed=shutter_speed,
                    image_format=image_format,
                ),
                port=base_capture.connection.port,
                expected_model=base_capture.connection.model,
                timeout=120.0,
            )
            mode = "fixed_bracket" if str(step["purpose"]) == "linearity_bracket" else "fixed_cached"

        report = _write_native_capture_report(
            capture,
            step=step,
            ambient_capture=ambient_capture,
            location_config_path=location_config_path,
            observer_config_path=observer_config_path,
            measurements_dir=measurements_output,
            raw_analyze_fn=raw_analyze_fn,
            raw_report_writer=raw_report_writer,
        )
        return {
            "mode": mode,
            "capture": capture.to_jsonable(),
            "patch_statistics": str(report[0]),
            "quality": report[1],
        }

    return capture_step


def run_native_raw_observer_validation(
    plan: Mapping[str, Any],
    *,
    output_root: str | Path,
    run_name: str | None,
    curve_path: str | Path | None = esphome.DEFAULT_CURVE_PATH,
) -> Path:
    """Run P1 acquisition after the CLI has required explicit high-output consent."""

    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    capture_step_fn = build_native_raw_capture_step_fn(
        camera_dir=run_dir / "camera",
        measurements_dir=run_dir / "measurements",
        scratch_dir=run_dir / "scratch",
        location_config_path=plan["inputs"]["location_config"]["path"],
        observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
    )

    def strip_light(cw: int, ww: int, r: int, g: int, b: int) -> Mapping[str, Any]:
        return esphome.light(cw, ww, r, g, b, curve_path=curve_path)

    return execute_raw_observer_validation_plan(
        plan,
        run_dir=run_dir,
        strip_light_fn=strip_light,
        ray_set_cct_fn=ray120c.set_cct,
        capture_step_fn=capture_step_fn,
        sleep_fn=time.sleep,
        provenance_fn=lambda: collect_native_raw_observer_provenance(curve_path=curve_path),
    )


def collect_native_raw_observer_provenance(*, curve_path: str | Path | None) -> dict[str, Any]:
    """Collect immutable, read-only P1 environment evidence before the first capture."""

    camera = camera_gphoto2.auto_detect_camera()
    return {
        "git": _git_provenance(),
        "software": {
            "rawpy": _rawpy_provenance(),
            "gphoto2": _command_version(("gphoto2", "--version")),
        },
        "camera": {
            "model": camera.model,
            "port": camera.port,
            "identity": _camera_identity(camera.port),
            "capture_settings": {
                "iso": camera_gphoto2.DEFAULT_ISO,
                "aperture": camera_gphoto2.DEFAULT_APERTURE,
                "image_format": camera_gphoto2.DEFAULT_IMAGE_FORMAT,
            },
        },
        "ray120c": dict(ray120c.get_node_config()),
        "esphome": asyncio.run(_read_esphome_device_info()),
        "code_duty_curve": _file_reference_or_disabled(curve_path),
    }


def _git_provenance() -> dict[str, Any]:
    commit = _command_text(("git", "rev-parse", "HEAD"))
    dirty = _command_text(("git", "status", "--porcelain"))
    return {"commit": commit, "dirty": bool(dirty), "dirty_entries": dirty.splitlines()}


def _rawpy_provenance() -> dict[str, Any]:
    try:
        import rawpy
    except ImportError as exc:
        return {"status": "unavailable", "error": f"{type(exc).__name__}: {exc}"}
    return {
        "version": getattr(rawpy, "__version__", None),
        "libraw_version": getattr(rawpy, "libraw_version", None),
    }


def _command_version(command: Sequence[str]) -> dict[str, Any]:
    try:
        return {"status": "ok", "output": _command_text(command)}
    except OSError as exc:
        return {"status": "unavailable", "error": f"{type(exc).__name__}: {exc}"}
    except subprocess.CalledProcessError as exc:
        return {"status": "failed", "returncode": exc.returncode, "output": exc.stdout, "error": exc.stderr}


def _command_text(command: Sequence[str]) -> str:
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    return completed.stdout.strip()


def _camera_identity(port: str) -> dict[str, Any]:
    try:
        summary = _command_text(("gphoto2", "--port", port, "--summary"))
    except OSError as exc:
        return {"status": "unavailable", "error": f"{type(exc).__name__}: {exc}"}
    except subprocess.CalledProcessError as exc:
        return {"status": "failed", "returncode": exc.returncode, "output": exc.stdout, "error": exc.stderr}
    return _redact_camera_summary(summary)


def _redact_camera_summary(summary: str) -> dict[str, Any]:
    """Keep only P1 camera identity fields; never persist the raw summary or serial number."""

    def value_for(label: str) -> str | None:
        for line in summary.splitlines():
            stripped = line.strip()
            if stripped.startswith(label):
                return stripped.split(":", 1)[1].strip()
        return None

    def value_for_any(labels: Sequence[str]) -> str | None:
        for label in labels:
            value = value_for(label)
            if value is not None:
                return value
        return None

    serial = value_for("Serial Number:")
    model = value_for("Model:")
    anonymous_seed = serial or model or "unknown-camera"
    return {
        "status": "ok",
        "manufacturer": value_for("Manufacturer:"),
        "model": model,
        "firmware_version": value_for("Version:"),
        "anonymous_device_id_sha256": hashlib.sha256(anonymous_seed.encode("utf-8")).hexdigest(),
        "lens": value_for_any(("Current Lens:", "Lens Name:")),
        "focal_length": value_for_any(("Focal Length:",)),
    }


async def _read_esphome_device_info() -> dict[str, Any]:
    import aioesphomeapi

    api_key = esphome._load_api_encryption_key(esphome.DEFAULT_SECRETS_PATH)
    client = aioesphomeapi.APIClient(
        esphome.DEFAULT_HOST,
        esphome.DEFAULT_PORT,
        None,
        noise_psk=api_key,
        expected_name=esphome.DEFAULT_EXPECTED_NAME,
    )
    await client.connect(login=True)
    try:
        info, entities, services = await client.device_info_and_list_entities()
        return {
            "name": getattr(info, "name", None),
            "model": getattr(info, "model", None),
            "esphome_version": getattr(info, "esphome_version", None),
            "compilation_time": getattr(info, "compilation_time", None),
            "project_name": getattr(info, "project_name", None),
            "project_version": getattr(info, "project_version", None),
            "entity_count": len(entities),
            "services": sorted(str(service.name) for service in services),
        }
    finally:
        await client.disconnect()


def parse_linearity_factors(value: str) -> tuple[float, ...]:
    return _validate_linearity_factors(tuple(float(item.strip()) for item in value.split(",") if item.strip()))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the immutable dry-run plan for native Bayer raw observer validation."
    )
    parser.add_argument("--baseline-lut", required=True, type=Path)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--anchor-cct", type=int, default=DEFAULT_ANCHOR_CCT)
    parser.add_argument("--anchor-gm", type=int, default=DEFAULT_ANCHOR_GM)
    parser.add_argument("--ray-intensity-percent", type=float, default=DEFAULT_RAY_INTENSITY_PERCENT)
    parser.add_argument("--paired-repeats", type=int, default=DEFAULT_PAIRED_REPEATS)
    parser.add_argument("--linearity-factors", type=parse_linearity_factors, default=DEFAULT_LINEARITY_FACTORS)
    parser.add_argument("--linearity-repeats", type=int, default=DEFAULT_LINEARITY_REPEATS)
    parser.add_argument("--off-seconds", type=float, default=DEFAULT_OFF_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--include-flat-field", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Write only the immutable capture plan.")
    mode.add_argument("--execute", action="store_true", help="Run the P1 capture plan; requires --allow-high-output.")
    parser.add_argument(
        "--allow-high-output",
        action="store_true",
        help="Required with --execute because the explicit external LUT may use full-scale channels.",
    )
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--no-curve", action="store_true", help="Disable code-duty curve correction for the strip.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    plan_kwargs = {
        "baseline_lut_path": args.baseline_lut,
        "location_config_path": args.location_config,
        "observer_config_path": args.raw_observer_config,
        "anchor_cct": args.anchor_cct,
        "anchor_gm": args.anchor_gm,
        "ray_intensity_percent": args.ray_intensity_percent,
        "paired_repeats": args.paired_repeats,
        "linearity_factors": args.linearity_factors,
        "linearity_repeats": args.linearity_repeats,
        "off_seconds": args.off_seconds,
        "settle_seconds": args.settle_seconds,
        "include_flat_field": args.include_flat_field,
        "curve_path": None if args.no_curve else args.curve,
    }
    if args.dry_run:
        output = write_raw_observer_validation_dry_run(
            output_root=args.output_dir,
            run_name=args.run_name,
            **plan_kwargs,
        )
        print(output)
        return 0
    if not args.allow_high_output:
        raise ValueError("--execute requires --allow-high-output")
    output = run_native_raw_observer_validation(
        build_raw_observer_validation_plan(**plan_kwargs),
        output_root=args.output_dir,
        run_name=args.run_name,
        curve_path=None if args.no_curve else args.curve,
    )
    print(output)
    return 0


def _validate_linearity_factors(values: Sequence[float]) -> tuple[float, ...]:
    factors = tuple(float(value) for value in values)
    if len(factors) < 2 or any(value <= 0 for value in factors) or len(set(factors)) != len(factors):
        raise ValueError("linearity_factors must contain at least two unique positive values")
    if 1.0 not in factors:
        raise ValueError("linearity_factors must include 1.0")
    return factors


def _source_cache_key(step: Mapping[str, Any]) -> str:
    cache_key = step.get("source_exposure_cache")
    if cache_key not in {"ray", "strip"}:
        raise ValueError(f"capture {step.get('capture_id')} has no valid source exposure cache")
    return str(cache_key)


def _capture_filename(step: Mapping[str, Any]) -> str:
    repeat = "none" if step.get("repeat_index") is None else str(int(step["repeat_index"]))
    factor = "auto" if step.get("exposure_factor") is None else f"{float(step['exposure_factor']):g}x"
    return (
        f"{step['capture_id']}-source-{step['source']}-purpose-{step['purpose']}"
        f"-repeat-{repeat}-exposure-{factor}-attempt-0.%C"
    )


def _resolve_bracket_shutter_speed(
    base_capture: camera_gphoto2.CaptureResult,
    *,
    factor: float,
    min_shutter_speed: str,
    max_shutter_speed: str,
    shutter_choices_fn: ShutterChoicesFn | None,
    choices_cache: dict[str, tuple[str, ...]],
) -> str:
    if factor <= 0:
        raise ValueError("linearity bracket exposure factor must be positive")
    port = base_capture.connection.port
    choices = choices_cache.get(port)
    if choices is None:
        choices = tuple(
            shutter_choices_fn(port)
            if shutter_choices_fn is not None
            else camera_gphoto2.read_config_choices(port, camera_gphoto2.CONFIG_SHUTTER_SPEED)
        )
        choices_cache[port] = choices
    target_seconds = Fraction(base_capture.settings.shutter_speed) * Fraction(str(factor))
    return camera_gphoto2.select_supported_shutter_speed(
        choices,
        target_seconds=target_seconds,
        min_shutter_speed=min_shutter_speed,
        max_shutter_speed=max_shutter_speed,
    )


def _write_native_capture_report(
    capture: camera_gphoto2.CaptureResult,
    *,
    step: Mapping[str, Any],
    ambient_capture: camera_gphoto2.CaptureResult | None,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    measurements_dir: Path,
    raw_analyze_fn: RawAnalyzeFn,
    raw_report_writer: RawReportWriter,
) -> tuple[Path, Mapping[str, Any]]:
    kwargs: dict[str, Any] = {
        "exposure_seconds": float(Fraction(capture.settings.shutter_speed)),
        "location_config_path": location_config_path,
        "observer_config_path": observer_config_path,
    }
    if str(step["source"]) != "ambient":
        if ambient_capture is None:
            raise ValueError("non-ambient capture requires the preceding ambient capture")
        kwargs["ambient_raw_file"] = ambient_capture.saved_file
        kwargs["ambient_exposure_seconds"] = float(Fraction(ambient_capture.settings.shutter_speed))
    report = raw_analyze_fn(capture.saved_file, **kwargs)
    report = dict(report)
    report["analysis_context"] = {
        "capture_id": str(step["capture_id"]),
        "source": str(step["source"]),
        "purpose": str(step["purpose"]),
        "repeat_index": step.get("repeat_index"),
        "exposure_factor": step.get("exposure_factor"),
        "shutter_speed": capture.settings.shutter_speed,
        "capture_path": str(capture.saved_file),
    }
    path = measurements_dir / f"{step['capture_id']}.patch-statistics.json"
    raw_report_writer(path, report)
    quality = report.get("quality") if isinstance(report, Mapping) else None
    return path, quality if isinstance(quality, Mapping) else {"status": "missing"}


def _validate_executable_plan(plan: Mapping[str, Any]) -> None:
    captures = plan.get("captures")
    measurement = plan.get("measurement")
    if not isinstance(captures, list) or not captures:
        raise ValueError("plan captures must be a non-empty array")
    if not isinstance(measurement, Mapping) or not isinstance(measurement.get("anchor"), Mapping):
        raise ValueError("plan measurement.anchor must be an object")
    for step in captures:
        if not isinstance(step, Mapping):
            raise ValueError("plan capture must be an object")
        if step.get("source") not in {"ambient", "ray", "strip", "flat_field_ray"}:
            raise ValueError(f"unsupported capture source: {step.get('source')}")
        if not bool(step.get("other_source_must_be_off")):
            raise ValueError("every executable capture must require source isolation")


def _prepare_capture_source(
    step: Mapping[str, Any],
    *,
    strip_light_fn: StripLightFn,
    ray_set_cct_fn: RaySetCctFn,
    sleep_fn: SleepFn,
    command_log: Path,
) -> None:
    source = str(step["source"])
    if source == "ambient":
        _set_strip_off(strip_light_fn, command_log, step, reason="ambient")
        _set_ray_off(ray_set_cct_fn, step, command_log, reason="ambient")
    elif source in {"ray", "flat_field_ray"}:
        _set_strip_off(strip_light_fn, command_log, step, reason="before_ray")
        _sleep_before_light(step, sleep_fn, command_log)
        ray = step["ray"]
        if not isinstance(ray, Mapping):
            raise ValueError(f"{source} capture requires ray settings")
        response = ray_set_cct_fn(int(ray["cct"]), intensity=float(ray["intensity_percent"]), gm=int(ray["gm"]))
        _append_jsonl(
            command_log,
            {"event": "ray_on", "at": _utc_now(), "capture_id": step["capture_id"], "response": dict(response)},
        )
    elif source == "strip":
        _set_ray_off(ray_set_cct_fn, step, command_log, reason="before_strip")
        _sleep_before_light(step, sleep_fn, command_log)
        command = step["strip_command"]
        if not isinstance(command, Mapping):
            raise ValueError("strip capture requires strip_command")
        response = strip_light_fn(*(int(command[channel]) for channel in ("cw", "ww", "r", "g", "b")))
        _append_jsonl(
            command_log,
            {"event": "strip_on", "at": _utc_now(), "capture_id": step["capture_id"], "response": dict(response)},
        )
    else:
        raise ValueError(f"unsupported capture source: {source}")
    settle_seconds = float(step["settle_seconds"])
    sleep_fn(settle_seconds)
    _append_jsonl(
        command_log,
        {"event": "settled", "at": _utc_now(), "capture_id": step["capture_id"], "seconds": settle_seconds},
    )


def _deactivate_capture_source(
    step: Mapping[str, Any],
    *,
    strip_light_fn: StripLightFn,
    ray_set_cct_fn: RaySetCctFn,
    command_log: Path,
) -> None:
    source = str(step["source"])
    if source in {"ray", "flat_field_ray"}:
        _set_ray_off(ray_set_cct_fn, step, command_log, reason="after_capture")
    elif source == "strip":
        _set_strip_off(strip_light_fn, command_log, step, reason="after_capture")


def _sleep_before_light(step: Mapping[str, Any], sleep_fn: SleepFn, command_log: Path) -> None:
    seconds = float(step["off_seconds_before"])
    sleep_fn(seconds)
    _append_jsonl(
        command_log,
        {"event": "off_wait", "at": _utc_now(), "capture_id": step["capture_id"], "seconds": seconds},
    )


def _set_strip_off(
    strip_light_fn: StripLightFn,
    command_log: Path,
    step: Mapping[str, Any],
    *,
    reason: str,
) -> Mapping[str, Any]:
    response = strip_light_fn(0, 0, 0, 0, 0)
    _append_jsonl(
        command_log,
        {"event": "strip_off", "at": _utc_now(), "capture_id": step["capture_id"], "reason": reason, "response": dict(response)},
    )
    return response


def _set_ray_off(
    ray_set_cct_fn: RaySetCctFn,
    step: Mapping[str, Any],
    command_log: Path,
    *,
    reason: str,
) -> Mapping[str, Any]:
    ray = step.get("ray")
    cct = int(ray["cct"]) if isinstance(ray, Mapping) else DEFAULT_ANCHOR_CCT
    gm = int(ray["gm"]) if isinstance(ray, Mapping) else DEFAULT_ANCHOR_GM
    response = ray_set_cct_fn(cct, intensity=0, gm=gm)
    _append_jsonl(
        command_log,
        {"event": "ray_off", "at": _utc_now(), "capture_id": step["capture_id"], "reason": reason, "response": dict(response)},
    )
    return response


def _run_python_cleanup(
    plan: Mapping[str, Any],
    *,
    strip_light_fn: StripLightFn,
    ray_set_cct_fn: RaySetCctFn,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]],
) -> dict[str, Any]:
    anchor = plan["measurement"]["anchor"]
    try:
        steps = all_off_fn(
            strip_off_fn=lambda: dict(strip_light_fn(0, 0, 0, 0, 0)),
            ray_set_cct_fn=ray_set_cct_fn,
            ray_cct=int(anchor["cct"]),
            ray_gm=int(anchor["gm"]),
        )
        return {"at": _utc_now(), "steps": [_shutdown_step_json(step) for step in steps]}
    except BaseException as exc:
        return {
            "at": _utc_now(),
            "steps": [],
            "cleanup_exception": {"type": type(exc).__name__, "message": str(exc)},
        }


def _shutdown_step_json(step: all_off.ShutdownStep | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(step, all_off.ShutdownStep):
        return step.to_jsonable()
    return dict(step)


def _cleanup_succeeded(cleanup: Mapping[str, Any]) -> bool:
    steps = cleanup.get("steps")
    return (
        "cleanup_exception" not in cleanup
        and isinstance(steps, list)
        and len(steps) == 2
        and all(isinstance(item, Mapping) and bool(item.get("ok")) for item in steps)
    )


def _write_experiment_summary(
    root: Path,
    *,
    run: Mapping[str, Any],
    plan: Mapping[str, Any],
    cleanup: Mapping[str, Any] | None = None,
) -> None:
    measurement = plan["measurement"]
    anchor = measurement["anchor"]
    lines = [
        "# P1 Raw Observer Validation",
        "",
        f"- Status: `{run['status']}`",
        f"- Run directory: `{root}`",
        f"- Planned captures: `{len(plan['captures'])}`",
        f"- Anchor: Ray `{anchor['cct']}K / GM{anchor['gm']} / {anchor['ray_intensity_percent']}%`",
        f"- Source isolation: {measurement['source_isolation']}",
        "- Analysis: run `camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation` after completion.",
    ]
    if cleanup is not None:
        lines.append(f"- Python cleanup: `{'ok' if _cleanup_succeeded(cleanup) else 'failed'}`")
    (root / "EXPERIMENT_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _file_reference(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise ValueError(f"required input file does not exist: {path}")
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _file_reference_or_disabled(path: str | Path | None) -> dict[str, str]:
    if path is None:
        return {"status": "disabled"}
    return _file_reference(Path(path))


def _write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, data: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
