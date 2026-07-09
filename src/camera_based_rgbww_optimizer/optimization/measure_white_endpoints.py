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
DEFAULT_RAY_SEARCH_CCT_ITERATIONS = 8
DEFAULT_RAY_SEARCH_GM_ITERATIONS = 6

LightFn = Callable[..., dict[str, int]]
RaySetCctFn = Callable[..., dict[str, Any]]
AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
WhitePointEstimatorFn = Callable[[camera_gphoto2.CaptureResult, Sequence[dict[str, Any]]], dict[str, Any]]


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
                "Endpoint CCT/G-M is assigned by estimating the strip endpoint white patch CCT/Duv, then controlling Ray120c through an adaptive CCT/G-M binary search.",
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

    gm = min(max(int(initial_gm), int(ray_gm_min)), int(ray_gm_max))
    cct_low = int(ray_cct_min)
    cct_high = int(ray_cct_max)
    cct_history = []
    for iteration in range(cct_iterations):
        midpoint = int(round((cct_low + cct_high) / 2))
        left = sample(cct_low, gm, "cct", iteration)
        middle = sample(midpoint, gm, "cct", iteration)
        right = sample(cct_high, gm, "cct", iteration)
        candidates = [left, middle, right]
        best = min(candidates, key=lambda item: item["white_point_comparison"]["normalized_score"])
        cct_history.append(
            {
                "iteration": iteration,
                "low": cct_low,
                "mid": midpoint,
                "high": cct_high,
                "best": _compact_reference_match(best),
            }
        )
        if int(best["cct"]) <= midpoint:
            cct_high = midpoint
        else:
            cct_low = midpoint
        if cct_high - cct_low <= 1:
            break

    best_cct_sample = min(samples, key=lambda item: item["white_point_comparison"]["normalized_score"])
    cct = int(best_cct_sample["cct"])
    gm_low = int(ray_gm_min)
    gm_high = int(ray_gm_max)
    gm_history = []
    for iteration in range(gm_iterations):
        midpoint = int(round((gm_low + gm_high) / 2))
        left = sample(cct, gm_low, "gm", iteration)
        middle = sample(cct, midpoint, "gm", iteration)
        right = sample(cct, gm_high, "gm", iteration)
        candidates = [left, middle, right]
        best = min(candidates, key=lambda item: item["white_point_comparison"]["normalized_score"])
        gm_history.append(
            {
                "iteration": iteration,
                "low": gm_low,
                "mid": midpoint,
                "high": gm_high,
                "best": _compact_reference_match(best),
            }
        )
        if int(best["gm"]) <= midpoint:
            gm_high = midpoint
        else:
            gm_low = midpoint
        if gm_high - gm_low <= 1:
            break

    best = min(samples, key=lambda item: item["white_point_comparison"]["normalized_score"])
    ranked = [_compact_reference_match(item) for item in sorted(samples, key=lambda item: item["white_point_comparison"]["normalized_score"])]
    return {
        "target_white_point": target_white_point,
        "strategy": {
            "kind": "coordinate_binary_search",
            "initial_gm": int(initial_gm),
            "cct_iterations": int(cct_iterations),
            "gm_iterations": int(gm_iterations),
            "cct_bounds": [int(ray_cct_min), int(ray_cct_max)],
            "gm_bounds": [int(ray_gm_min), int(ray_gm_max)],
        },
        "cct_history": cct_history,
        "gm_history": gm_history,
        "samples": [common.jsonable_without_vector(item) for item in samples],
        "match": {
            "best": _compact_reference_match(best),
            "ranked": ranked,
        },
    }


def _compact_reference_match(reference: dict[str, Any]) -> dict[str, Any]:
    comparison = reference.get("white_point_comparison", {})
    white_point = reference.get("white_point", {})
    return {
        "cct": int(reference["cct"]),
        "gm": int(reference["gm"]),
        "score": float(comparison.get("normalized_score", 0.0)),
        "cct_error_K": float(comparison.get("cct_error_K", 0.0)),
        "duv_error": float(comparison.get("duv_error", 0.0)),
        "absolute_cct_error_K": float(comparison.get("absolute_cct_error_K", 0.0)),
        "absolute_duv_error": float(comparison.get("absolute_duv_error", 0.0)),
        "ray_white_point": {
            "cct_K": float(white_point.get("cct_K", 0.0)),
            "duv": float(white_point.get("duv", 0.0)),
            "xy": white_point.get("xy"),
            "uv1960": white_point.get("uv1960"),
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())
