from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2, esphome, ray120c
from camera_based_rgbww_optimizer.optimization import measure_channel_response
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR
from camera_based_rgbww_optimizer.utils import location_regions


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "white-endpoints"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260605-225800.json"
DEFAULT_ENDPOINT_RAY_CCTS = (1800, 2000, 2300, 2700, 3200, 3800, 4500, 5000, 5600, 6500, 8000, 10000, 14000, 20000)
DEFAULT_ENDPOINT_RAY_GM_VALUES = (0, 70, 100, 130, 200)
DEFAULT_MAX_CODE = 4095
DEFAULT_SAFE_CODE_LIMIT = 1024
DEFAULT_SETTLE_SECONDS = 1.0
DEFAULT_RAY_INTENSITY_PERCENT = 100.0
DEFAULT_RAY_SEARCH_MODE = "adaptive"
DEFAULT_RAY_CCT_MIN = ray120c.CCT_MIN
DEFAULT_RAY_CCT_MAX = ray120c.CCT_MAX
DEFAULT_RAY_GM_MIN = ray120c.GM_MIN
DEFAULT_RAY_GM_MAX = ray120c.GM_MAX
DEFAULT_RAY_SEARCH_INITIAL_GM = 100
DEFAULT_RAY_SEARCH_CCT_ITERATIONS = 64
DEFAULT_RAY_SEARCH_GM_ITERATIONS = 16
DEFAULT_RAY_SEARCH_COORDINATE_ROUNDS = 3
DEFAULT_RAY_CCT_TOLERANCE_K = 10.0
DEFAULT_RAY_DUV_TOLERANCE = 0.01

LightFn = Callable[..., dict[str, int]]
RaySetCctFn = Callable[..., dict[str, Any]]
AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
WhitePointEstimatorFn = Callable[[camera_gphoto2.CaptureResult, Sequence[dict[str, Any]]], dict[str, Any]]


def parse_ray_start(value: str) -> tuple[str, dict[str, int]]:
    channel_text, separator, rest = value.strip().partition("=")
    if not separator:
        raise argparse.ArgumentTypeError("ray start must look like ww=CCT,GM or cw=CCT,GM")
    channel = channel_text.strip().lower()
    if channel not in {"ww", "cw"}:
        raise argparse.ArgumentTypeError("ray start channel must be ww or cw")
    parts = [part.strip() for part in rest.replace(":", ",").split(",") if part.strip()]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("ray start must include exactly CCT and GM, for example ww=2961,160")
    try:
        cct = int(parts[0])
        gm = int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ray start CCT and GM must be integers") from exc
    return channel, {"cct": cct, "gm": gm}


def _normalize_ray_start_map(ray_start: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    normalized: dict[str, dict[str, int]] = {}
    for channel, start in ray_start.items():
        channel_key = str(channel).strip().lower()
        if channel_key not in {"ww", "cw"}:
            raise ValueError("ray_start keys must be ww or cw")
        cct = int(start["cct"])
        gm = int(start["gm"])
        if not ray120c.CCT_MIN <= cct <= ray120c.CCT_MAX:
            raise ValueError(f"ray_start {channel_key} cct must be in [{ray120c.CCT_MIN}, {ray120c.CCT_MAX}]")
        if not ray120c.GM_MIN <= gm <= ray120c.GM_MAX:
            raise ValueError(f"ray_start {channel_key} gm must be in [{ray120c.GM_MIN}, {ray120c.GM_MAX}]")
        normalized[channel_key] = {"cct": cct, "gm": gm}
    return normalized


def run_white_endpoint_measurement(
    *,
    output_root: Path,
    run_name: str | None,
    location_config: Path,
    endpoint_ray_ccts: Sequence[int],
    endpoint_ray_gm_values: Sequence[int],
    neutral_roles: Sequence[str],
    color_weight: float,
    max_code: int,
    safe_code_limit: int,
    allow_high_output: bool,
    dry_run: bool,
    settle_seconds: float,
    ray_intensity_percent: float,
    target_max: int,
    iso: str,
    aperture: str,
    image_format: str,
    min_shutter_speed: str,
    max_shutter_speed: str,
    max_trials: int,
    max_captures: int,
    decode_formats: Sequence[str],
    block_indices: str | tuple[int, ...],
    auto_exposure_metering_mode: str,
    auto_exposure_metering_location_config: Path | None,
    ray_search_mode: str = DEFAULT_RAY_SEARCH_MODE,
    ray_cct_min: int = DEFAULT_RAY_CCT_MIN,
    ray_cct_max: int = DEFAULT_RAY_CCT_MAX,
    ray_gm_min: int = DEFAULT_RAY_GM_MIN,
    ray_gm_max: int = DEFAULT_RAY_GM_MAX,
    ray_search_initial_gm: int = DEFAULT_RAY_SEARCH_INITIAL_GM,
    ray_search_cct_iterations: int = DEFAULT_RAY_SEARCH_CCT_ITERATIONS,
    ray_search_gm_iterations: int = DEFAULT_RAY_SEARCH_GM_ITERATIONS,
    ray_start: dict[str, dict[str, int]] | None = None,
    output_json: Path | None = None,
    leave_ray_on: bool = False,
    light_fn: LightFn = esphome.light,
    ray_set_cct_fn: RaySetCctFn = ray120c.set_cct,
    auto_expose_fn: AutoExposeFn = camera_gphoto2.auto_expose_capture,
    white_point_estimator_fn: WhitePointEstimatorFn = common.estimate_capture_white_point,
) -> Path:
    common.validate_high_output_plan(
        max_code=max_code,
        safe_code_limit=safe_code_limit,
        allow_high_output=allow_high_output,
        dry_run=dry_run,
        operation="white endpoint measurement",
    )
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / (run_name or timestamp)
    if output_json is None:
        output_json = run_dir / "white-endpoints.json"
    else:
        output_json = Path(output_json)
        run_dir = output_json.parent
    camera_dir = run_dir / "camera"
    decode_dir = run_dir / "decoded"
    scratch_dir = run_dir / "scratch"
    run_dir.mkdir(parents=True, exist_ok=True)

    regions = common.load_weighted_location_regions(
        location_config,
        block_indices,
        neutral_roles=neutral_roles,
        color_weight=color_weight,
    )
    metering_config, metering_regions = common.resolve_metering_regions(
        auto_exposure_metering_mode=auto_exposure_metering_mode,
        location_config=location_config,
        auto_exposure_metering_location_config=auto_exposure_metering_location_config,
    )
    endpoint_ray_plan = common.build_target_grid(endpoint_ray_ccts, endpoint_ray_gm_values)
    ray_start = _normalize_ray_start_map(ray_start or {})
    result: dict[str, Any] = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "status": "planned" if dry_run else "running",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_white_endpoint_ray_match",
            "endpoint_ray_ccts": [int(value) for value in endpoint_ray_ccts],
            "endpoint_ray_gm_values": [int(value) for value in endpoint_ray_gm_values],
            "ray_search_mode": ray_search_mode,
            "adaptive_ray_search": {
                "cct_min": int(ray_cct_min),
                "cct_max": int(ray_cct_max),
                "gm_min": int(ray_gm_min),
                "gm_max": int(ray_gm_max),
                "initial_gm": int(ray_search_initial_gm),
                "cct_iterations": int(ray_search_cct_iterations),
                "gm_iterations": int(ray_search_gm_iterations),
                "coordinate_rounds": DEFAULT_RAY_SEARCH_COORDINATE_ROUNDS,
                "cct_tolerance_K": DEFAULT_RAY_CCT_TOLERANCE_K,
                "duv_tolerance": DEFAULT_RAY_DUV_TOLERANCE,
                "ray_start": ray_start,
                "cct_error_scale": common.DEFAULT_CCT_ERROR_SCALE,
                "duv_error_scale": common.DEFAULT_DUV_ERROR_SCALE,
            },
            "ray_intensity_percent": float(ray_intensity_percent),
            "max_code": int(max_code),
            "allow_high_output": bool(allow_high_output),
            "settle_seconds": float(settle_seconds),
            "location_config": str(location_config),
            "regions": location_regions.jsonable_regions(regions),
            "neutral_roles": list(neutral_roles),
            "color_weight": float(color_weight),
            "notes": [
                "Endpoint CCT/G-M is assigned by estimating the strip endpoint white patch CCT/Duv, then controlling Ray120c through target-driven alternating CCT/G-M correction.",
                "The legacy fixed Ray120c grid search is still available with --ray-search-mode grid.",
                "WW and CW strip endpoints are measured at full scale independently.",
                "Neutral patches are primary; color patches are auxiliary with lower weight.",
            ],
        },
        "camera": {
            "target_max": int(target_max),
            "iso": str(iso),
            "aperture": str(aperture),
            "image_format": str(image_format),
            "min_shutter_speed": str(min_shutter_speed),
            "max_shutter_speed": str(max_shutter_speed),
            "max_trials": int(max_trials),
            "max_captures": int(max_captures),
            "decode_formats": list(decode_formats),
            "scratch_dir": str(scratch_dir),
            "auto_exposure_metering": {
                "mode": auto_exposure_metering_mode,
                "location_config": str(metering_config) if metering_config is not None else None,
                "regions": location_regions.jsonable_regions(metering_regions) if metering_regions is not None else None,
            },
        },
        "endpoint_ray_plan": endpoint_ray_plan,
        "strip_endpoints": {},
        "ray_references": [],
        "ray_searches": {},
        "ray_endpoint_matches": {},
        "white_range": None,
    }
    common.write_json(output_json, result)
    if dry_run:
        result["status"] = "dry_run"
        common.write_json(output_json, result)
        return output_json

    last_ray_target: dict[str, int] | None = None
    try:
        light_fn(0, 0, 0, 0, 0)
        strip_vectors: dict[str, Any] = {}
        strip_white_points: dict[str, Any] = {}
        for channel in ("ww", "cw"):
            print(f"strip endpoint: {channel}=4095")
            command = {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}
            command[channel] = int(max_code)
            payload = light_fn(command["cw"], command["ww"], command["r"], command["g"], command["b"])
            time.sleep(max(0.0, settle_seconds))
            capture = common.capture_auto_exposed(
                auto_expose_fn=auto_expose_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                scratch_dir=scratch_dir,
                filename_template=f"endpoint-strip-{channel}.%C",
                target_max=target_max,
                iso=iso,
                aperture=aperture,
                image_format=image_format,
                min_shutter_speed=min_shutter_speed,
                max_shutter_speed=max_shutter_speed,
                max_trials=max_trials,
                max_captures=max_captures,
                decode_formats=decode_formats,
                metering_regions=metering_regions,
            )
            seconds, vector, measurements = common.measure_auto_exposure_regions(capture, regions)
            white_point = white_point_estimator_fn(capture.final_capture, regions)
            strip_vectors[channel] = vector
            strip_white_points[channel] = white_point
            result["strip_endpoints"][channel] = {
                "channel": channel,
                "command": command,
                "payload": payload,
                "auto_exposure": capture.to_jsonable(),
                "shutter_seconds": seconds,
                "vector_norm": common.vector_norm(vector),
                "white_point": white_point,
                "regions": measurements,
            }
            common.write_json(output_json, result)

        light_fn(0, 0, 0, 0, 0)
        if ray_search_mode == "grid":
            ray_references: list[dict[str, Any]] = []
            for target in endpoint_ray_plan:
                print(f"Ray reference {target['index'] + 1}/{len(endpoint_ray_plan)}: {target['cct']}K gm={target['gm']}")
                last_ray_target = {"cct": int(target["cct"]), "gm": int(target["gm"])}
                reference = _capture_ray_reference(
                    target_channel=None,
                    target=target,
                    ray_set_cct_fn=ray_set_cct_fn,
                    auto_expose_fn=auto_expose_fn,
                    white_point_estimator_fn=white_point_estimator_fn,
                    camera_dir=camera_dir,
                    decode_dir=decode_dir,
                    scratch_dir=scratch_dir,
                    target_max=target_max,
                    iso=iso,
                    aperture=aperture,
                    image_format=image_format,
                    min_shutter_speed=min_shutter_speed,
                    max_shutter_speed=max_shutter_speed,
                    max_trials=max_trials,
                    max_captures=max_captures,
                    decode_formats=decode_formats,
                    metering_regions=metering_regions,
                    regions=regions,
                    ray_intensity_percent=ray_intensity_percent,
                    settle_seconds=settle_seconds,
                    filename_template=f"ray-reference-{target['index']:02d}-{target['cct']}K-gm{target['gm']}.%C",
                )
                ray_references.append(reference)
                result["ray_references"].append(common.jsonable_without_vector(reference))
                common.write_json(output_json, result)
            matches = {
                "cw": common.best_ray_match(strip_vectors["cw"], ray_references, regions=regions),
                "ww": common.best_ray_match(strip_vectors["ww"], ray_references, regions=regions),
            }
        elif ray_search_mode == "adaptive":
            matches = {}
            for channel in ("ww", "cw"):
                search = _run_adaptive_ray_search(
                    target_channel=channel,
                    target_white_point=strip_white_points[channel],
                    ray_set_cct_fn=ray_set_cct_fn,
                    auto_expose_fn=auto_expose_fn,
                    white_point_estimator_fn=white_point_estimator_fn,
                    camera_dir=camera_dir,
                    decode_dir=decode_dir,
                    scratch_dir=scratch_dir,
                    target_max=target_max,
                    iso=iso,
                    aperture=aperture,
                    image_format=image_format,
                    min_shutter_speed=min_shutter_speed,
                    max_shutter_speed=max_shutter_speed,
                    max_trials=max_trials,
                    max_captures=max_captures,
                    decode_formats=decode_formats,
                    metering_regions=metering_regions,
                    regions=regions,
                    ray_intensity_percent=ray_intensity_percent,
                    settle_seconds=settle_seconds,
                    ray_cct_min=ray_cct_min,
                    ray_cct_max=ray_cct_max,
                    ray_gm_min=ray_gm_min,
                    ray_gm_max=ray_gm_max,
                    initial_gm=ray_search_initial_gm,
                    start_cct=ray_start.get(channel, {}).get("cct"),
                    start_gm=ray_start.get(channel, {}).get("gm"),
                    cct_iterations=ray_search_cct_iterations,
                    gm_iterations=ray_search_gm_iterations,
                    result=result,
                    output_json=output_json,
                )
                last_best = search["match"]["best"]
                last_ray_target = {"cct": int(last_best["cct"]), "gm": int(last_best["gm"])}
                result["ray_searches"][channel] = search
                matches[channel] = search["match"]
                common.write_json(output_json, result)
        else:
            raise ValueError("ray_search_mode must be one of: adaptive, grid")
        result["ray_endpoint_matches"] = matches
        result["white_range"] = {
            "cw": matches["cw"]["best"],
            "ww": matches["ww"]["best"],
            "low_cct": min(int(matches["cw"]["best"]["cct"]), int(matches["ww"]["best"]["cct"])),
            "high_cct": max(int(matches["cw"]["best"]["cct"]), int(matches["ww"]["best"]["cct"])),
        }
        result["status"] = "complete"
        common.write_json(output_json, result)
        print(
            "Ray-matched endpoint range: "
            f"{result['white_range']['low_cct']}K..{result['white_range']['high_cct']}K "
            f"(ww best {matches['ww']['best']['cct']}K gm={matches['ww']['best']['gm']}; "
            f"cw best {matches['cw']['best']['cct']}K gm={matches['cw']['best']['gm']})"
        )
        return output_json
    except Exception as exc:
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        common.write_json(output_json, result)
        raise
    finally:
        try:
            light_fn(0, 0, 0, 0, 0)
        except Exception:
            pass
        if not leave_ray_on and last_ray_target is not None:
            try:
                ray_set_cct_fn(last_ray_target["cct"], intensity=0, gm=last_ray_target["gm"])
            except Exception:
                pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure WW/CW strip endpoints by matching them to photographed Ray120c CCT/G-M references."
    )
    parser.add_argument("--endpoint-ray-ccts", type=common.parse_int_values, default=DEFAULT_ENDPOINT_RAY_CCTS)
    parser.add_argument("--endpoint-ray-gm-values", type=common.parse_int_values, default=DEFAULT_ENDPOINT_RAY_GM_VALUES)
    parser.add_argument("--ray-search-mode", choices=("adaptive", "grid"), default=DEFAULT_RAY_SEARCH_MODE)
    parser.add_argument("--ray-cct-min", type=int, default=DEFAULT_RAY_CCT_MIN)
    parser.add_argument("--ray-cct-max", type=int, default=DEFAULT_RAY_CCT_MAX)
    parser.add_argument("--ray-gm-min", type=int, default=DEFAULT_RAY_GM_MIN)
    parser.add_argument("--ray-gm-max", type=int, default=DEFAULT_RAY_GM_MAX)
    parser.add_argument("--ray-search-initial-gm", type=int, default=DEFAULT_RAY_SEARCH_INITIAL_GM)
    parser.add_argument("--ray-search-cct-iterations", type=int, default=DEFAULT_RAY_SEARCH_CCT_ITERATIONS)
    parser.add_argument("--ray-search-gm-iterations", type=int, default=DEFAULT_RAY_SEARCH_GM_ITERATIONS)
    parser.add_argument(
        "--ray-start",
        action="append",
        type=parse_ray_start,
        default=[],
        help="Seed adaptive search for one endpoint as ww=CCT,GM or cw=CCT,GM.",
    )
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--block-indices", type=measure_channel_response.parse_block_indices, default="all")
    parser.add_argument("--neutral-roles", type=common.parse_roles, default=common.DEFAULT_NEUTRAL_ROLES)
    parser.add_argument("--color-weight", type=float, default=common.DEFAULT_COLOR_WEIGHT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--max-code", type=int, default=DEFAULT_MAX_CODE)
    parser.add_argument("--safe-code-limit", type=int, default=DEFAULT_SAFE_CODE_LIMIT)
    parser.add_argument("--allow-high-output", action="store_true")
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--ray-intensity-percent", type=float, default=DEFAULT_RAY_INTENSITY_PERCENT)
    parser.add_argument("--target-max", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX)
    parser.add_argument("--iso", default=camera_gphoto2.DEFAULT_ISO)
    parser.add_argument("--aperture", default=camera_gphoto2.DEFAULT_APERTURE)
    parser.add_argument("--image-format", default=camera_gphoto2.DEFAULT_IMAGE_FORMAT)
    parser.add_argument("--min-shutter-speed", default=camera_gphoto2.DEFAULT_MIN_SHUTTER_SPEED)
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--max-trials", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_TRIALS)
    parser.add_argument("--max-captures", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_CAPTURES)
    parser.add_argument("--decode-format", dest="decode_formats", action="append")
    parser.add_argument(
        "--auto-exposure-metering-mode",
        choices=(camera_gphoto2.METERING_MODE_FULL, camera_gphoto2.METERING_MODE_LOCATION),
        default=camera_gphoto2.METERING_MODE_LOCATION,
    )
    parser.add_argument("--auto-exposure-metering-location-config", type=Path)
    parser.add_argument("--leave-ray-on", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_json = run_white_endpoint_measurement(
        output_root=args.output_dir,
        run_name=args.run_name,
        location_config=args.location_config,
        endpoint_ray_ccts=args.endpoint_ray_ccts,
        endpoint_ray_gm_values=args.endpoint_ray_gm_values,
        neutral_roles=args.neutral_roles,
        color_weight=args.color_weight,
        max_code=args.max_code,
        safe_code_limit=args.safe_code_limit,
        allow_high_output=args.allow_high_output,
        dry_run=args.dry_run,
        settle_seconds=args.settle_seconds,
        ray_intensity_percent=args.ray_intensity_percent,
        target_max=args.target_max,
        iso=args.iso,
        aperture=args.aperture,
        image_format=args.image_format,
        min_shutter_speed=args.min_shutter_speed,
        max_shutter_speed=args.max_shutter_speed,
        max_trials=args.max_trials,
        max_captures=args.max_captures,
        decode_formats=tuple(args.decode_formats or measure_channel_response.DEFAULT_DECODE_FORMATS),
        block_indices=args.block_indices,
        auto_exposure_metering_mode=args.auto_exposure_metering_mode,
        auto_exposure_metering_location_config=args.auto_exposure_metering_location_config,
        ray_search_mode=args.ray_search_mode,
        ray_cct_min=args.ray_cct_min,
        ray_cct_max=args.ray_cct_max,
        ray_gm_min=args.ray_gm_min,
        ray_gm_max=args.ray_gm_max,
        ray_search_initial_gm=args.ray_search_initial_gm,
        ray_search_cct_iterations=args.ray_search_cct_iterations,
        ray_search_gm_iterations=args.ray_search_gm_iterations,
        ray_start=dict(args.ray_start),
        output_json=args.output_json,
        leave_ray_on=args.leave_ray_on,
    )
    print(output_json)
    return 0


def _capture_ray_reference(
    *,
    target_channel: str | None,
    target: dict[str, int],
    ray_set_cct_fn: RaySetCctFn,
    auto_expose_fn: AutoExposeFn,
    white_point_estimator_fn: WhitePointEstimatorFn,
    camera_dir: Path,
    decode_dir: Path,
    scratch_dir: Path,
    target_max: int,
    iso: str,
    aperture: str,
    image_format: str,
    min_shutter_speed: str,
    max_shutter_speed: str,
    max_trials: int,
    max_captures: int,
    decode_formats: Sequence[str],
    metering_regions: Sequence[dict[str, Any]] | None,
    regions: Sequence[dict[str, Any]],
    ray_intensity_percent: float,
    settle_seconds: float,
    filename_template: str,
) -> dict[str, Any]:
    ray_response = ray_set_cct_fn(
        int(target["cct"]),
        intensity_percent=ray_intensity_percent,
        gm=int(target["gm"]),
    )
    time.sleep(max(0.0, settle_seconds))
    capture = common.capture_auto_exposed(
        auto_expose_fn=auto_expose_fn,
        camera_dir=camera_dir,
        decode_dir=decode_dir,
        scratch_dir=scratch_dir,
        filename_template=filename_template,
        target_max=target_max,
        iso=iso,
        aperture=aperture,
        image_format=image_format,
        min_shutter_speed=min_shutter_speed,
        max_shutter_speed=max_shutter_speed,
        max_trials=max_trials,
        max_captures=max_captures,
        decode_formats=decode_formats,
        metering_regions=metering_regions,
    )
    seconds, vector, measurements = common.measure_auto_exposure_regions(capture, regions)
    white_point = white_point_estimator_fn(capture.final_capture, regions)
    reference = {
        **target,
        "target_channel": target_channel,
        "set_response": ray_response,
        "auto_exposure": capture.to_jsonable(),
        "shutter_seconds": seconds,
        "vector": vector,
        "vector_norm": common.vector_norm(vector),
        "white_point": white_point,
        "regions": measurements,
    }
    return reference


def _run_adaptive_ray_search(
    *,
    target_channel: str,
    target_white_point: dict[str, Any],
    ray_set_cct_fn: RaySetCctFn,
    auto_expose_fn: AutoExposeFn,
    white_point_estimator_fn: WhitePointEstimatorFn,
    camera_dir: Path,
    decode_dir: Path,
    scratch_dir: Path,
    target_max: int,
    iso: str,
    aperture: str,
    image_format: str,
    min_shutter_speed: str,
    max_shutter_speed: str,
    max_trials: int,
    max_captures: int,
    decode_formats: Sequence[str],
    metering_regions: Sequence[dict[str, Any]] | None,
    regions: Sequence[dict[str, Any]],
    ray_intensity_percent: float,
    settle_seconds: float,
    ray_cct_min: int,
    ray_cct_max: int,
    ray_gm_min: int,
    ray_gm_max: int,
    initial_gm: int,
    start_cct: int | None,
    start_gm: int | None,
    cct_iterations: int,
    gm_iterations: int,
    result: dict[str, Any],
    output_json: Path,
) -> dict[str, Any]:
    if ray_cct_min >= ray_cct_max:
        raise ValueError("ray_cct_min must be less than ray_cct_max")
    if ray_gm_min >= ray_gm_max:
        raise ValueError("ray_gm_min must be less than ray_gm_max")
    if cct_iterations <= 0:
        raise ValueError("ray_search_cct_iterations must be positive")
    if gm_iterations <= 0:
        raise ValueError("ray_search_gm_iterations must be positive")

    samples: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()

    def sample(cct: int, gm: int, phase: str, iteration: int) -> dict[str, Any]:
        cct = min(max(int(round(cct)), int(ray_cct_min)), int(ray_cct_max))
        gm = min(max(int(round(gm)), int(ray_gm_min)), int(ray_gm_max))
        key = (cct, gm)
        for existing in samples:
            if (int(existing["cct"]), int(existing["gm"])) == key:
                return existing
        index = len(samples)
        print(f"Ray {target_channel} search {phase} {iteration}: {cct}K gm={gm}")
        reference = _capture_ray_reference(
            target_channel=target_channel,
            target={"index": index, "cct": cct, "gm": gm},
            ray_set_cct_fn=ray_set_cct_fn,
            auto_expose_fn=auto_expose_fn,
            white_point_estimator_fn=white_point_estimator_fn,
            camera_dir=camera_dir,
            decode_dir=decode_dir,
            scratch_dir=scratch_dir,
            target_max=target_max,
            iso=iso,
            aperture=aperture,
            image_format=image_format,
            min_shutter_speed=min_shutter_speed,
            max_shutter_speed=max_shutter_speed,
            max_trials=max_trials,
            max_captures=max_captures,
            decode_formats=decode_formats,
            metering_regions=metering_regions,
            regions=regions,
            ray_intensity_percent=ray_intensity_percent,
            settle_seconds=settle_seconds,
            filename_template=f"ray-search-{target_channel}-{index:02d}-{phase}-{cct}K-gm{gm}.%C",
        )
        comparison = common.compare_white_points(reference["white_point"], target_white_point)
        reference["white_point_comparison"] = comparison
        samples.append(reference)
        seen.add(key)
        result.setdefault("ray_searches", {}).setdefault(target_channel, {})["samples"] = [
            common.jsonable_without_vector(item) for item in samples
        ]
        result["ray_searches"][target_channel]["target_white_point"] = target_white_point
        common.write_json(output_json, result)
        return reference

    search_start_cct = _clamp_int(
        float(target_white_point["cct_K"]) if start_cct is None else int(start_cct),
        ray_cct_min,
        ray_cct_max,
    )
    search_start_gm = min(max(int(initial_gm if start_gm is None else start_gm), int(ray_gm_min)), int(ray_gm_max))
    current_cct = search_start_cct
    current_gm = search_start_gm
    cct_history: list[dict[str, Any]] = []
    gm_history: list[dict[str, Any]] = []
    round_history: list[dict[str, Any]] = []
    cct_budget_remaining = int(cct_iterations)
    gm_budget_remaining = int(gm_iterations)
    for round_index in range(DEFAULT_RAY_SEARCH_COORDINATE_ROUNDS):
        rounds_left = DEFAULT_RAY_SEARCH_COORDINATE_ROUNDS - round_index
        cct_budget = _split_remaining_budget(cct_budget_remaining, rounds_left)
        gm_budget = _split_remaining_budget(gm_budget_remaining, rounds_left)
        cct_result = _run_cct_correction_phase(
            sample_fn=sample,
            samples=samples,
            target_white_point=target_white_point,
            start_cct=current_cct,
            gm=current_gm,
            ray_cct_min=ray_cct_min,
            ray_cct_max=ray_cct_max,
            max_new_samples=cct_budget,
            round_index=round_index,
        )
        cct_budget_remaining -= cct_result["new_samples"]
        current_cct = int(cct_result["best_cct_match"]["cct"])
        cct_history.append(cct_result)
        gm_result = _run_gm_correction_phase(
            sample_fn=sample,
            samples=samples,
            target_white_point=target_white_point,
            cct=current_cct,
            start_gm=current_gm,
            ray_gm_min=ray_gm_min,
            ray_gm_max=ray_gm_max,
            max_new_samples=gm_budget,
            round_index=round_index,
        )
        gm_budget_remaining -= gm_result["new_samples"]
        current_cct = int(gm_result["best_duv_match"]["cct"])
        current_gm = int(gm_result["best_duv_match"]["gm"])
        gm_history.append(gm_result)
        best_after_round = _best_goal_match(samples)
        round_history.append(
            {
                "round": round_index,
                "cct_phase": cct_result["summary"],
                "gm_phase": gm_result["summary"],
                "best": _compact_reference_match(best_after_round),
            }
        )
        if cct_budget_remaining <= 0 and gm_budget_remaining <= 0:
            break

    best = _best_goal_match(samples)
    ranked = [_compact_reference_match(item) for item in sorted(samples, key=_goal_match_key)]
    return {
        "target_white_point": target_white_point,
        "strategy": {
            "kind": "target_driven_alternating_cct_gm_correction",
            "initial_gm": int(initial_gm),
            "start_cct": int(search_start_cct),
            "start_gm": int(search_start_gm),
            "cct_sample_budget": int(cct_iterations),
            "gm_sample_budget": int(gm_iterations),
            "coordinate_rounds": DEFAULT_RAY_SEARCH_COORDINATE_ROUNDS,
            "cct_tolerance_K": DEFAULT_RAY_CCT_TOLERANCE_K,
            "duv_tolerance": DEFAULT_RAY_DUV_TOLERANCE,
            "cct_bounds": [int(ray_cct_min), int(ray_cct_max)],
            "gm_bounds": [int(ray_gm_min), int(ray_gm_max)],
        },
        "round_history": round_history,
        "cct_history": cct_history,
        "gm_history": gm_history,
        "samples": [common.jsonable_without_vector(item) for item in samples],
        "match": {
            "best": _compact_reference_match(best),
            "ranked": ranked,
        },
    }


def _run_cct_correction_phase(
    *,
    sample_fn: Callable[[int, int, str, int], dict[str, Any]],
    samples: list[dict[str, Any]],
    target_white_point: dict[str, Any],
    start_cct: int,
    gm: int,
    ray_cct_min: int,
    ray_cct_max: int,
    max_new_samples: int,
    round_index: int,
) -> dict[str, Any]:
    start_count = len(samples)
    phase_samples: list[dict[str, Any]] = []
    steps: list[dict[str, Any]] = []
    target_cct = float(target_white_point["cct_K"])

    def add_sample(cct: int, reason: str) -> dict[str, Any]:
        reference = sample_fn(cct, gm, f"round{round_index}-cct", len(steps))
        if reference not in phase_samples:
            phase_samples.append(reference)
        steps.append({"reason": reason, "sample": _compact_reference_match(reference)})
        return reference

    if max_new_samples > 0:
        add_sample(_clamp_int(start_cct, ray_cct_min, ray_cct_max), "start_at_target_or_previous_best")
    while len(samples) - start_count < max_new_samples:
        best = _best_cct_match(phase_samples)
        if best["white_point_comparison"]["absolute_cct_error_K"] <= DEFAULT_RAY_CCT_TOLERANCE_K:
            break
        proposed = _predict_setting_from_observations(
            phase_samples,
            setting_key="cct",
            observed_key="cct_K",
            target_observed=target_cct,
        )
        if proposed is None:
            proposed = int(best["cct"]) - best["white_point_comparison"]["cct_error_K"]
        next_cct = _next_unseen_setting(
            proposed,
            bounds=(int(ray_cct_min), int(ray_cct_max)),
            seen={int(item["cct"]) for item in samples if int(item["gm"]) == int(gm)},
        )
        if next_cct is None:
            break
        add_sample(next_cct, "cct_error_correction")

    best = _best_cct_match(phase_samples or samples)
    return {
        "round": int(round_index),
        "kind": "cct_error_correction",
        "gm": int(gm),
        "new_samples": len(samples) - start_count,
        "steps": steps,
        "best_cct_match": _compact_reference_match(best),
        "summary": {
            "gm": int(gm),
            "best_cct": int(best["cct"]),
            "absolute_cct_error_K": float(best["white_point_comparison"]["absolute_cct_error_K"]),
            "absolute_duv_error": float(best["white_point_comparison"]["absolute_duv_error"]),
        },
    }


def _run_gm_correction_phase(
    *,
    sample_fn: Callable[[int, int, str, int], dict[str, Any]],
    samples: list[dict[str, Any]],
    target_white_point: dict[str, Any],
    cct: int,
    start_gm: int,
    ray_gm_min: int,
    ray_gm_max: int,
    max_new_samples: int,
    round_index: int,
) -> dict[str, Any]:
    start_count = len(samples)
    phase_samples: list[dict[str, Any]] = []
    steps: list[dict[str, Any]] = []
    target_duv = float(target_white_point["duv"])

    def add_sample(gm: int, reason: str) -> dict[str, Any]:
        reference = sample_fn(cct, gm, f"round{round_index}-gm", len(steps))
        if reference not in phase_samples:
            phase_samples.append(reference)
        steps.append({"reason": reason, "sample": _compact_reference_match(reference)})
        return reference

    if max_new_samples > 0:
        add_sample(_clamp_int(start_gm, ray_gm_min, ray_gm_max), "start_at_previous_best")
    while len(samples) - start_count < max_new_samples:
        best = _best_duv_match(phase_samples)
        if best["white_point_comparison"]["absolute_duv_error"] <= DEFAULT_RAY_DUV_TOLERANCE:
            break
        proposed = _predict_setting_from_observations(
            phase_samples,
            setting_key="gm",
            observed_key="duv",
            target_observed=target_duv,
        )
        if proposed is None:
            duv_error = float(best["white_point_comparison"]["duv_error"])
            step = max(1, min(60, int(round(abs(duv_error) / DEFAULT_RAY_DUV_TOLERANCE * 50.0))))
            proposed = int(best["gm"]) + (step if duv_error > 0 else -step)
        next_gm = _next_unseen_setting(
            proposed,
            bounds=(int(ray_gm_min), int(ray_gm_max)),
            anchor=int(best["gm"]),
            max_jump=20,
            seen={int(item["gm"]) for item in samples if int(item["cct"]) == int(cct)},
        )
        if next_gm is None:
            break
        add_sample(next_gm, "duv_error_correction")

    best = _best_duv_match(phase_samples or samples)
    return {
        "round": int(round_index),
        "kind": "duv_error_correction",
        "cct": int(cct),
        "new_samples": len(samples) - start_count,
        "steps": steps,
        "best_duv_match": _compact_reference_match(best),
        "summary": {
            "cct": int(cct),
            "best_gm": int(best["gm"]),
            "absolute_cct_error_K": float(best["white_point_comparison"]["absolute_cct_error_K"]),
            "absolute_duv_error": float(best["white_point_comparison"]["absolute_duv_error"]),
        },
    }


def _split_remaining_budget(remaining: int, rounds_left: int) -> int:
    if remaining <= 0:
        return 0
    return max(1, (int(remaining) + int(rounds_left) - 1) // int(rounds_left))


def _predict_setting_from_observations(
    references: Sequence[dict[str, Any]],
    *,
    setting_key: str,
    observed_key: str,
    target_observed: float,
) -> float | None:
    points: list[tuple[float, float]] = []
    seen: set[tuple[float, float]] = set()
    for reference in references:
        setting = float(reference[setting_key])
        observed = float(reference["white_point"][observed_key])
        key = (setting, observed)
        if key not in seen:
            points.append(key)
            seen.add(key)
    if len(points) < 2:
        return None

    bracket: tuple[tuple[float, float], tuple[float, float]] | None = None
    by_observed = sorted(points, key=lambda item: item[1])
    for left, right in zip(by_observed, by_observed[1:]):
        left_delta = left[1] - target_observed
        right_delta = right[1] - target_observed
        if left_delta == 0:
            return left[0]
        if right_delta == 0:
            return right[0]
        if left_delta * right_delta < 0:
            if bracket is None or abs(right[1] - left[1]) < abs(bracket[1][1] - bracket[0][1]):
                bracket = (left, right)
    if bracket is None:
        closest = sorted(points, key=lambda item: abs(item[1] - target_observed))[:2]
        left, right = closest[0], closest[1]
    else:
        left, right = bracket
    setting_delta = right[0] - left[0]
    observed_delta = right[1] - left[1]
    if setting_delta == 0 or abs(observed_delta) < 1e-12:
        return None
    slope = observed_delta / setting_delta
    if abs(slope) < 1e-12:
        return None
    return left[0] + (target_observed - left[1]) / slope


def _next_unseen_setting(
    proposed: float,
    *,
    bounds: tuple[int, int],
    seen: set[int],
    anchor: int | None = None,
    max_jump: int | None = None,
) -> int | None:
    low, high = bounds
    if anchor is not None and max_jump is not None:
        low = max(int(low), int(anchor) - int(max_jump))
        high = min(int(high), int(anchor) + int(max_jump))
    base = _clamp_int(proposed, low, high)
    offsets = (0, -1, 1, -2, 2, -5, 5, -10, 10, -20, 20, -50, 50, -100, 100, -250, 250, -500, 500)
    for offset in offsets:
        candidate = _clamp_int(base + offset, low, high)
        if candidate not in seen:
            return candidate
    for candidate in range(low, high + 1):
        if candidate not in seen:
            return candidate
    return None


def _clamp_int(value: float, low: int, high: int) -> int:
    return min(max(int(round(value)), int(low)), int(high))


def _best_cct_match(references: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return min(
        references,
        key=lambda item: (
            float(item["white_point_comparison"]["absolute_cct_error_K"]),
            float(item["white_point_comparison"]["absolute_duv_error"]),
            float(item["white_point_comparison"]["normalized_score"]),
        ),
    )


def _best_duv_match(references: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return min(
        references,
        key=lambda item: (
            float(item["white_point_comparison"]["absolute_duv_error"]),
            float(item["white_point_comparison"]["absolute_cct_error_K"]),
            float(item["white_point_comparison"]["normalized_score"]),
        ),
    )


def _best_goal_match(references: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return min(references, key=_goal_match_key)


def _goal_match_key(reference: dict[str, Any]) -> tuple[float, float, float, float]:
    comparison = reference["white_point_comparison"]
    absolute_cct_error = float(comparison["absolute_cct_error_K"])
    absolute_duv_error = float(comparison["absolute_duv_error"])
    return (
        max(absolute_cct_error / DEFAULT_RAY_CCT_TOLERANCE_K, absolute_duv_error / DEFAULT_RAY_DUV_TOLERANCE),
        absolute_cct_error,
        absolute_duv_error,
        float(comparison["normalized_score"]),
    )


def _compact_reference_match(reference: dict[str, Any]) -> dict[str, Any]:
    comparison = reference.get("white_point_comparison", {})
    white_point = reference.get("white_point", {})
    absolute_cct_error = float(comparison.get("absolute_cct_error_K", 0.0))
    absolute_duv_error = float(comparison.get("absolute_duv_error", 0.0))
    return {
        "cct": int(reference["cct"]),
        "gm": int(reference["gm"]),
        "score": float(comparison.get("normalized_score", 0.0)),
        "goal_score": max(
            absolute_cct_error / DEFAULT_RAY_CCT_TOLERANCE_K,
            absolute_duv_error / DEFAULT_RAY_DUV_TOLERANCE,
        ),
        "within_goal": absolute_cct_error < DEFAULT_RAY_CCT_TOLERANCE_K
        and absolute_duv_error < DEFAULT_RAY_DUV_TOLERANCE,
        "cct_error_K": float(comparison.get("cct_error_K", 0.0)),
        "duv_error": float(comparison.get("duv_error", 0.0)),
        "absolute_cct_error_K": absolute_cct_error,
        "absolute_duv_error": absolute_duv_error,
        "ray_white_point": {
            "cct_K": float(white_point.get("cct_K", 0.0)),
            "duv": float(white_point.get("duv", 0.0)),
            "xy": white_point.get("xy"),
            "uv1960": white_point.get("uv1960"),
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())
