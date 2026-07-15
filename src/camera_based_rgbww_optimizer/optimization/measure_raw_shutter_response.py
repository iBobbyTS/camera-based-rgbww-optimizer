from __future__ import annotations

import argparse
import collections
import copy
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, esphome, ray120c, white_lut as white_lut_control
from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches, recorded_exposure
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "raw-shutter-response"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260709-012045.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_ANCHOR_CCT = 5600
DEFAULT_ANCHOR_GM = 100
DEFAULT_RAY_INTENSITY_PERCENT = 1.0
DEFAULT_STRIP_INTENSITY_PERCENT = 20.0
DEFAULT_SHUTTER_ORDER = ("1/80", "1/60", "1/100", "1/50", "1/50", "1/100", "1/60", "1/80")
DEFAULT_CYCLES = 3
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_WARMUP_SECONDS = 60.0

StripLightFn = Callable[[int, int, int, int, int], Mapping[str, Any]]
RaySetCctFn = Callable[..., Mapping[str, Any]]
CaptureStepFn = Callable[[Mapping[str, Any]], Mapping[str, Any]]
SleepFn = Callable[[float], None]
ProvenanceFn = Callable[[], Mapping[str, Any]]
MonotonicFn = Callable[[], float]


def build_raw_shutter_response_plan(
    *,
    baseline_lut_path: str | Path,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    curve_path: str | Path | None = esphome.DEFAULT_CURVE_PATH,
    anchor_cct: int = DEFAULT_ANCHOR_CCT,
    anchor_gm: int = DEFAULT_ANCHOR_GM,
    ray_intensity_percent: float = DEFAULT_RAY_INTENSITY_PERCENT,
    strip_intensity_percent: float = DEFAULT_STRIP_INTENSITY_PERCENT,
    shutter_order: Sequence[str] = DEFAULT_SHUTTER_ORDER,
    cycles: int = DEFAULT_CYCLES,
    off_seconds: float = DEFAULT_OFF_SECONDS,
    warmup_seconds: float = DEFAULT_WARMUP_SECONDS,
) -> dict[str, Any]:
    """Build a same-shutter, continuous-on diagnostic plan without device I/O."""

    shutters = _validate_shutter_order(shutter_order)
    if cycles < 1:
        raise ValueError("cycles must be at least 1")
    if off_seconds < 0 or warmup_seconds < 0:
        raise ValueError("off_seconds and warmup_seconds must be non-negative")
    if not 0.0 < ray_intensity_percent <= 100.0:
        raise ValueError("ray_intensity_percent must be in (0, 100]")
    if not 0.0 < strip_intensity_percent <= 100.0:
        raise ValueError("strip_intensity_percent must be in (0, 100]")

    lut_path = Path(baseline_lut_path)
    interpolation = white_lut_control.interpolate_white_lut(
        white_lut_control.load_white_lut(lut_path), anchor_cct, anchor_gm, clamp=False
    )
    base_command = {channel: int(value) for channel, value in interpolation["command"].items()}
    strip_command = _scale_command(base_command, strip_intensity_percent)
    captures: list[dict[str, Any]] = [
        {
            "capture_id": "0000-ambient",
            "index": 0,
            "source": "ambient",
            "purpose": "ambient",
            "shutter_speed": "30",
            "cycle": None,
            "order_index": None,
            "other_source_must_be_off": True,
        }
    ]
    for source in ("ray", "strip"):
        for cycle in range(cycles):
            for order_index, shutter_speed in enumerate(shutters):
                index = len(captures)
                captures.append(
                    {
                        "capture_id": f"{index:04d}-{source}-shutter-response",
                        "index": index,
                        "source": source,
                        "purpose": "shutter_response",
                        "shutter_speed": shutter_speed,
                        "cycle": cycle,
                        "order_index": order_index,
                        "other_source_must_be_off": True,
                    }
                )

    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_raw_shutter_response",
            "anchor": {
                "cct": int(anchor_cct),
                "gm": int(anchor_gm),
                "ray_intensity_percent": float(ray_intensity_percent),
                "strip_intensity_percent": float(strip_intensity_percent),
                "base_strip_command": base_command,
                "strip_command": strip_command,
            },
            "shutter_order": list(shutters),
            "cycles": int(cycles),
            "frames_per_shutter_per_source": int(cycles * shutters.count(shutters[0])),
            "source_protocol": "source_on_once_then_continuous_captures",
            "source_isolation": "the other source must be off before each source group",
            "off_seconds_before_source": float(off_seconds),
            "warmup_seconds": float(warmup_seconds),
        },
        "inputs": {
            "baseline_lut": raw_validation._file_reference(lut_path),
            "location_config": raw_validation._file_reference(Path(location_config_path)),
            "raw_observer_config": raw_validation._file_reference(Path(observer_config_path)),
            "code_duty_curve": raw_validation._file_reference_or_disabled(curve_path),
        },
        "captures": captures,
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted_even_if_one_shutdown_fails",
        },
    }


def write_raw_shutter_response_dry_run(*, output_root: str | Path, run_name: str | None, **plan_kwargs: Any) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_raw_shutter_response_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = _utc_now()
    plan["run_dir"] = str(run_dir)
    _write_json(run_dir / "plan.json", plan)
    return run_dir / "plan.json"


def execute_raw_shutter_response_plan(
    plan: Mapping[str, Any],
    *,
    run_dir: str | Path,
    strip_light_fn: StripLightFn,
    ray_set_cct_fn: RaySetCctFn,
    capture_step_fn: CaptureStepFn,
    sleep_fn: SleepFn,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    provenance_fn: ProvenanceFn | None = None,
    monotonic_fn: MonotonicFn = time.monotonic,
) -> Path:
    """Execute continuous source groups while preserving source isolation and final cleanup."""

    plan_data = copy.deepcopy(dict(plan))
    _validate_plan(plan_data)
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 1,
        "run_id": root.name,
        "phase": "P1-D",
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "inputs": copy.deepcopy(plan_data["inputs"]),
        "measurement": copy.deepcopy(plan_data["measurement"]),
        "safety": {"source_isolation": plan_data["measurement"]["source_isolation"]},
        "provenance": {"status": "pending" if provenance_fn is not None else "not_collected"},
    }
    _write_json(root / "run.json", run)
    failure: BaseException | None = None
    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("shutter-response provenance collector must return a mapping")
            run["provenance"] = copy.deepcopy(dict(provenance))
            _write_json(root / "run.json", run)

        ambient = plan_data["captures"][0]
        _set_both_off(plan_data, strip_light_fn, ray_set_cct_fn, root / "commands.jsonl", capture_id=ambient["capture_id"])
        capture_started_monotonic_seconds = monotonic_fn()
        capture = dict(capture_step_fn(copy.deepcopy(ambient)))
        _append_capture(
            root,
            ambient,
            capture,
            capture_started_monotonic_seconds=capture_started_monotonic_seconds,
            capture_finished_monotonic_seconds=monotonic_fn(),
        )

        for source in ("ray", "strip"):
            group = [step for step in plan_data["captures"] if step["source"] == source]
            _activate_source_group(
                source,
                plan=plan_data,
                strip_light_fn=strip_light_fn,
                ray_set_cct_fn=ray_set_cct_fn,
                sleep_fn=sleep_fn,
                command_log=root / "commands.jsonl",
                capture_id=str(group[0]["capture_id"]),
            )
            for step in group:
                _append_jsonl(
                    root / "commands.jsonl",
                    {"event": "capture_requested", "at": _utc_now(), "capture_id": step["capture_id"], "source": source},
                )
                capture_started_monotonic_seconds = monotonic_fn()
                capture = dict(capture_step_fn(copy.deepcopy(step)))
                _append_capture(
                    root,
                    step,
                    capture,
                    capture_started_monotonic_seconds=capture_started_monotonic_seconds,
                    capture_finished_monotonic_seconds=monotonic_fn(),
                )
            _deactivate_source(source, plan_data, strip_light_fn, ray_set_cct_fn, root / "commands.jsonl", str(group[-1]["capture_id"]))
    except BaseException as exc:
        failure = exc
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
    finally:
        cleanup = _cleanup(plan_data, strip_light_fn, ray_set_cct_fn, all_off_fn)
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if _cleanup_ok(cleanup) else "failed"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    return root


def build_native_shutter_response_capture_step_fn(
    *,
    camera_dir: str | Path,
    measurements_dir: str | Path,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    iso: str = camera_gphoto2.DEFAULT_ISO,
    aperture: str = camera_gphoto2.DEFAULT_APERTURE,
    image_format: str = camera_gphoto2.DEFAULT_IMAGE_FORMAT,
    capture_fn: Callable[..., camera_gphoto2.CaptureResult] = camera_gphoto2.capture_image,
    raw_analyze_fn: Callable[..., Mapping[str, Any]] = raw_mosaic_patches.analyze_raw_file,
    raw_report_writer: Callable[[str | Path, Mapping[str, Any]], Path] = raw_mosaic_patches.write_report,
    recorded_exposure_fn: raw_validation.RecordedExposureFn = recorded_exposure.resolve_recorded_exposure,
) -> CaptureStepFn:
    camera_output = Path(camera_dir)
    measurements_output = Path(measurements_dir)
    ambient_capture: camera_gphoto2.CaptureResult | None = None
    exposures_by_path: dict[Path, recorded_exposure.RecordedExposure] = {}

    def capture_exposure(capture: camera_gphoto2.CaptureResult) -> recorded_exposure.RecordedExposure:
        path = Path(capture.saved_file)
        if path not in exposures_by_path:
            exposures_by_path[path] = recorded_exposure_fn(path, capture.settings.shutter_speed)
        return recorded_exposure.require_recorded(exposures_by_path[path], purpose="P1-D")

    def capture_step(step: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal ambient_capture
        shutter_speed = str(step["shutter_speed"])
        capture = capture_fn(
            output_dir=camera_output,
            filename_template=_capture_filename(step),
            settings=camera_gphoto2.CaptureSettings(
                iso=iso, aperture=aperture, shutter_speed=shutter_speed, image_format=image_format
            ),
            timeout=120.0,
        )
        exposure = capture_exposure(capture)
        if step["source"] == "ambient":
            ambient_capture = capture
            return {
                "mode": "ambient_fixed",
                "capture": capture.to_jsonable(),
                "exposure_metadata": exposure.to_jsonable(),
            }
        if ambient_capture is None:
            raise ValueError("signal shutter-response capture requires the preceding ambient capture")
        report = raw_validation._write_native_capture_report(
            capture,
            step=step,
            ambient_capture=ambient_capture,
            capture_exposure=exposure,
            ambient_exposure=capture_exposure(ambient_capture),
            location_config_path=location_config_path,
            observer_config_path=observer_config_path,
            measurements_dir=measurements_output,
            raw_analyze_fn=raw_analyze_fn,
            raw_report_writer=raw_report_writer,
        )
        return {
            "mode": "fixed_shutter_response",
            "capture": capture.to_jsonable(),
            "exposure_metadata": exposure.to_jsonable(),
            "patch_statistics": str(report[0]),
            "quality": report[1],
        }

    return capture_step


def run_native_raw_shutter_response(
    plan: Mapping[str, Any], *, output_root: str | Path, run_name: str | None, curve_path: str | Path | None
) -> Path:
    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    capture_step_fn = build_native_shutter_response_capture_step_fn(
        camera_dir=run_dir / "camera",
        measurements_dir=run_dir / "measurements",
        location_config_path=plan["inputs"]["location_config"]["path"],
        observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
    )
    return execute_raw_shutter_response_plan(
        plan,
        run_dir=run_dir,
        strip_light_fn=lambda cw, ww, r, g, b: esphome.light(cw, ww, r, g, b, curve_path=curve_path),
        ray_set_cct_fn=ray120c.set_cct,
        capture_step_fn=capture_step_fn,
        sleep_fn=time.sleep,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(curve_path=curve_path),
    )


def analyze_raw_shutter_response_run(run_dir: str | Path, *, reference_shutter: str = "1/80") -> Path:
    root = Path(run_dir)
    run = json.loads((root / "run.json").read_text(encoding="utf-8"))
    if run.get("status") != "complete":
        raise ValueError(f"shutter-response run is not complete: {run.get('status')}")
    plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
    captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
    steps_by_id = {str(step["capture_id"]): step for step in plan["captures"]}
    source_values: dict[str, dict[str, dict[str, list[float]]]] = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(list))
    )
    capture_durations: dict[str, dict[str, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    missing_timing: dict[str, int] = collections.defaultdict(int)
    exposure_sources: dict[str, int] = collections.defaultdict(int)
    exposure_statuses: dict[str, int] = collections.defaultdict(int)
    missing_exposure_metadata = 0
    quality_counts: dict[str, int] = collections.defaultdict(int)
    for entry in captures:
        step = steps_by_id.get(str(entry["capture_id"]))
        if step is None:
            raise ValueError(f"capture {entry['capture_id']} is not present in plan.json")
        if step["source"] == "ambient":
            continue
        started = entry.get("capture_started_monotonic_seconds")
        finished = entry.get("capture_finished_monotonic_seconds")
        if isinstance(started, (int, float)) and isinstance(finished, (int, float)) and float(finished) >= float(started):
            capture_durations[str(step["source"])][str(step["shutter_speed"])].append(float(finished) - float(started))
        else:
            missing_timing[str(step["source"])] += 1
        report_path = entry["capture"].get("patch_statistics")
        if not isinstance(report_path, str):
            raise ValueError(f"capture {entry['capture_id']} has no patch-statistics report")
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
        exposure_metadata = report.get("exposure_metadata")
        if isinstance(exposure_metadata, Mapping):
            exposure_sources[str(exposure_metadata.get("source", "unknown"))] += 1
            exposure_statuses[str(exposure_metadata.get("status", "unknown"))] += 1
        else:
            missing_exposure_metadata += 1
        for patch in report["patches"]:
            if not patch["optimization_eligible"]:
                continue
            for plane_name, plane in patch["planes"].items():
                metrics = plane.get("metrics")
                if isinstance(metrics, Mapping):
                    clipped = metrics.get("clipped_fraction")
                    if isinstance(clipped, (int, float)) and float(clipped) > 0:
                        quality_counts["excluded_clipped"] += 1
                        continue
                    quality_counts["included_with_metrics"] += 1
                else:
                    quality_counts["included_missing_metrics"] += 1
                value = plane["ambient_subtracted"]["trimmed_mean_per_second"]
                source_values[step["source"]][step["shutter_speed"]][f"{patch['name']}::{plane_name}"].append(float(value))

    summary: dict[str, Any] = {}
    for source, shutter_values in source_values.items():
        if reference_shutter not in shutter_values:
            raise ValueError(f"reference shutter {reference_shutter} missing for {source}")
        reference = {feature: _median(values) for feature, values in shutter_values[reference_shutter].items()}
        source_summary: dict[str, Any] = {}
        for shutter, features in shutter_values.items():
            ratios: list[float] = []
            ratios_by_plane: dict[str, list[float]] = collections.defaultdict(list)
            for feature, values in features.items():
                if feature not in reference or reference[feature] == 0:
                    continue
                ratio = _median(values) / reference[feature] - 1.0
                ratios.append(ratio)
                ratios_by_plane[feature.rsplit("::", 1)[1]].append(ratio)
            global_scale = None if not ratios else 1.0 + _median(ratios)
            shape_residuals = (
                [] if global_scale is None else [((1.0 + ratio) / global_scale) - 1.0 for ratio in ratios]
            )
            shape_by_plane = {
                plane: (
                    []
                    if global_scale is None
                    else [((1.0 + ratio) / global_scale) - 1.0 for ratio in values]
                )
                for plane, values in ratios_by_plane.items()
            }
            source_summary[shutter] = {
                "feature_count": len(ratios),
                "relative_to_reference": _distribution(ratios),
                "relative_to_reference_by_plane": {
                    plane: _distribution(values) for plane, values in sorted(ratios_by_plane.items())
                },
                "global_scale_to_reference": global_scale,
                "shape_relative_to_global_scale": _distribution(shape_residuals),
                "shape_relative_to_global_scale_by_plane": {
                    plane: _distribution(values) for plane, values in sorted(shape_by_plane.items())
                },
            }
        summary[source] = source_summary
    timing_summary = {
        source: {
            "valid_capture_count": sum(len(values) for values in shutters.values()),
            "missing_capture_count": missing_timing[source],
            "capture_duration_seconds": _distribution([value for values in shutters.values() for value in values]),
            "capture_duration_seconds_by_shutter": {
                shutter: _distribution(values) for shutter, values in sorted(shutters.items())
            },
        }
        for source, shutters in sorted(capture_durations.items())
    }
    for source, count in missing_timing.items():
        timing_summary.setdefault(
            source,
            {
                "valid_capture_count": 0,
                "missing_capture_count": count,
                "capture_duration_seconds": None,
                "capture_duration_seconds_by_shutter": {},
            },
        )
    output = {
        "schema_version": 1,
        "analysis": "raw_shutter_response",
        "run_dir": str(root),
        "reference_shutter": reference_shutter,
        "status": "ready_for_manual_branch_review",
        "sources": summary,
        "capture_timing": {
            "clock": "monotonic_seconds",
            "sources": timing_summary,
        },
        "source_commands": _collect_source_commands(root / "commands.jsonl"),
        "exposure_provenance": {
            "source_counts": dict(sorted(exposure_sources.items())),
            "status_counts": dict(sorted(exposure_statuses.items())),
            "missing_metadata_report_count": missing_exposure_metadata,
            "recorded_metadata_required_for_acceptance": True,
        },
        "quality_observations": dict(sorted(quality_counts.items())),
        "notes": [
            "No shutter-response pass/fail conclusion or observer-threshold update is inferred automatically.",
            "Global per-shutter scale and residual patch/CFA shape are reported separately.",
            "Nominal or missing exposure metadata blocks acceptance even when diagnostic ratios are present.",
        ],
    }
    output_path = root / "analysis.json"
    _write_json(output_path, output)
    return output_path


def _collect_source_commands(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "not_recorded", "sources": {}}
    sources: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        name = event.get("event")
        if name not in {"ray_on", "strip_on"} or not isinstance(event.get("requested_command"), Mapping):
            continue
        source = str(name).removesuffix("_on")
        sources[source].append(
            {
                "capture_id": event.get("capture_id"),
                "requested_command": dict(event["requested_command"]),
            }
        )
    return {"status": "recorded", "sources": dict(sorted(sources.items()))}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure same-shutter continuous-on RAW response for P1-D diagnosis.")
    parser.add_argument("--baseline-lut", required=True, type=Path)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--anchor-cct", type=int, default=DEFAULT_ANCHOR_CCT)
    parser.add_argument("--anchor-gm", type=int, default=DEFAULT_ANCHOR_GM)
    parser.add_argument("--ray-intensity-percent", type=float, default=DEFAULT_RAY_INTENSITY_PERCENT)
    parser.add_argument("--strip-intensity-percent", type=float, default=DEFAULT_STRIP_INTENSITY_PERCENT)
    parser.add_argument("--shutter-order", default=",".join(DEFAULT_SHUTTER_ORDER))
    parser.add_argument("--cycles", type=int, default=DEFAULT_CYCLES)
    parser.add_argument("--off-seconds", type=float, default=DEFAULT_OFF_SECONDS)
    parser.add_argument("--warmup-seconds", type=float, default=DEFAULT_WARMUP_SECONDS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--no-curve", action="store_true")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    plan_kwargs = {
        "baseline_lut_path": args.baseline_lut,
        "location_config_path": args.location_config,
        "observer_config_path": args.raw_observer_config,
        "curve_path": None if args.no_curve else args.curve,
        "anchor_cct": args.anchor_cct,
        "anchor_gm": args.anchor_gm,
        "ray_intensity_percent": args.ray_intensity_percent,
        "strip_intensity_percent": args.strip_intensity_percent,
        "shutter_order": tuple(item.strip() for item in args.shutter_order.split(",") if item.strip()),
        "cycles": args.cycles,
        "off_seconds": args.off_seconds,
        "warmup_seconds": args.warmup_seconds,
    }
    if args.dry_run:
        print(write_raw_shutter_response_dry_run(output_root=args.output_dir, run_name=args.run_name, **plan_kwargs))
        return 0
    if not args.allow_device_control:
        raise ValueError("--execute requires --allow-device-control")
    print(run_native_raw_shutter_response(build_raw_shutter_response_plan(**plan_kwargs), output_root=args.output_dir, run_name=args.run_name, curve_path=plan_kwargs["curve_path"]))
    return 0


def _validate_shutter_order(values: Sequence[str]) -> tuple[str, ...]:
    shutters = tuple(value.strip() for value in values if value.strip())
    if len(shutters) < 4 or len(set(shutters)) < 4:
        raise ValueError("shutter_order must contain at least four distinct shutter speeds")
    counts = collections.Counter(shutters)
    if len(set(counts.values())) != 1 or next(iter(counts.values())) < 2:
        raise ValueError("shutter_order must repeat every shutter an equal number of times")
    for shutter in shutters:
        camera_gphoto2._parse_shutter_seconds(shutter)
    return shutters


def _scale_command(command: Mapping[str, int], intensity_percent: float) -> dict[str, int]:
    return {channel: int(round(int(value) * intensity_percent / 100.0)) for channel, value in command.items()}


def _validate_plan(plan: Mapping[str, Any]) -> None:
    captures = plan.get("captures")
    if not isinstance(captures, list) or not captures or captures[0].get("source") != "ambient":
        raise ValueError("plan must begin with an ambient capture")
    if any(not bool(step.get("other_source_must_be_off")) for step in captures):
        raise ValueError("every shutter-response capture must require source isolation")


def _set_both_off(plan: Mapping[str, Any], strip_light_fn: StripLightFn, ray_set_cct_fn: RaySetCctFn, command_log: Path, *, capture_id: str) -> None:
    anchor = plan["measurement"]["anchor"]
    strip_light_fn(0, 0, 0, 0, 0)
    ray_set_cct_fn(int(anchor["cct"]), intensity=0, gm=int(anchor["gm"]))
    _append_jsonl(command_log, {"event": "both_off", "at": _utc_now(), "capture_id": capture_id})


def _activate_source_group(source: str, *, plan: Mapping[str, Any], strip_light_fn: StripLightFn, ray_set_cct_fn: RaySetCctFn, sleep_fn: SleepFn, command_log: Path, capture_id: str) -> None:
    measurement = plan["measurement"]
    anchor = measurement["anchor"]
    _set_both_off(plan, strip_light_fn, ray_set_cct_fn, command_log, capture_id=capture_id)
    sleep_fn(float(measurement["off_seconds_before_source"]))
    if source == "ray":
        command = {
            "cct": int(anchor["cct"]),
            "gm": int(anchor["gm"]),
            "intensity_percent": float(anchor["ray_intensity_percent"]),
        }
        response = ray_set_cct_fn(
            command["cct"],
            intensity_percent=command["intensity_percent"],
            gm=command["gm"],
        )
    else:
        command = anchor["strip_command"]
        response = strip_light_fn(*(int(command[channel]) for channel in ("cw", "ww", "r", "g", "b")))
    _append_jsonl(
        command_log,
        {
            "event": f"{source}_on",
            "at": _utc_now(),
            "capture_id": capture_id,
            "requested_command": dict(command),
            "response": dict(response),
        },
    )
    sleep_fn(float(measurement["warmup_seconds"]))
    _append_jsonl(command_log, {"event": "source_warmed", "at": _utc_now(), "capture_id": capture_id, "seconds": measurement["warmup_seconds"]})


def _deactivate_source(source: str, plan: Mapping[str, Any], strip_light_fn: StripLightFn, ray_set_cct_fn: RaySetCctFn, command_log: Path, capture_id: str) -> None:
    anchor = plan["measurement"]["anchor"]
    if source == "ray":
        ray_set_cct_fn(int(anchor["cct"]), intensity=0, gm=int(anchor["gm"]))
    else:
        strip_light_fn(0, 0, 0, 0, 0)
    _append_jsonl(command_log, {"event": f"{source}_off", "at": _utc_now(), "capture_id": capture_id})


def _append_capture(
    root: Path,
    step: Mapping[str, Any],
    capture: Mapping[str, Any],
    *,
    capture_started_monotonic_seconds: float,
    capture_finished_monotonic_seconds: float,
) -> None:
    _append_jsonl(
        root / "captures.jsonl",
        {
            "capture_id": step["capture_id"],
            "source": step["source"],
            "purpose": step["purpose"],
            "shutter_speed": step["shutter_speed"],
            "cycle": step.get("cycle"),
            "order_index": step.get("order_index"),
            "capture_started_monotonic_seconds": float(capture_started_monotonic_seconds),
            "capture_finished_monotonic_seconds": float(capture_finished_monotonic_seconds),
            "capture": dict(capture),
        },
    )


def _cleanup(plan: Mapping[str, Any], strip_light_fn: StripLightFn, ray_set_cct_fn: RaySetCctFn, all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]]) -> dict[str, Any]:
    anchor = plan["measurement"]["anchor"]
    try:
        steps = all_off_fn(strip_off_fn=lambda: dict(strip_light_fn(0, 0, 0, 0, 0)), ray_set_cct_fn=ray_set_cct_fn, ray_cct=int(anchor["cct"]), ray_gm=int(anchor["gm"]))
        return {"at": _utc_now(), "steps": [step.to_jsonable() if isinstance(step, all_off.ShutdownStep) else dict(step) for step in steps]}
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


def _capture_filename(step: Mapping[str, Any]) -> str:
    cycle = "none" if step.get("cycle") is None else str(step["cycle"])
    return f"{step['capture_id']}-source-{step['source']}-shutter-{step['shutter_speed'].replace('/', '_')}-cycle-{cycle}.%C"


def _distribution(values: Sequence[float]) -> dict[str, float | int] | None:
    if not values:
        return None
    ordered = sorted(values)
    return {"count": len(ordered), "p10": ordered[round(0.10 * (len(ordered) - 1))], "p50": _median(ordered), "p90": ordered[round(0.90 * (len(ordered) - 1))], "min": ordered[0], "max": ordered[-1]}


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2.0


def _write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, data: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
