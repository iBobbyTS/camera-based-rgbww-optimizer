from __future__ import annotations

import argparse
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2, esphome, ray120c
from camera_based_rgbww_optimizer.optimization import measure_channel_response
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR
from camera_based_rgbww_optimizer.utils import location_regions


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "white-lut-calibration"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260605-225800.json"
DEFAULT_CHANNEL_RESPONSE = PROJECT_TMP_DIR / "channel-response" / "merged" / "channel-code-duty-response-merged.json"
DEFAULT_ENDPOINT_CALIBRATION = PROJECT_ROOT / "config" / "white" / "white-endpoints.json"
DEFAULT_TARGET_CCTS = (1800, 3200, 5600, 20000)
DEFAULT_TARGET_GM_VALUES = (0, 100, 200)
DEFAULT_INSIDE_RGB_PENALTY = 0.45
DEFAULT_OUTSIDE_RGB_PENALTY = 0.06
DEFAULT_ENDPOINT_RGB_PENALTY = 0.02
DEFAULT_MAX_CODE = 4095
DEFAULT_SAFE_CODE_LIMIT = 1024
DEFAULT_SETTLE_SECONDS = 1.0
DEFAULT_COARSE_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
DEFAULT_REFINEMENT_STEPS = (0.125, 0.0625, 0.03125, 0.015625)
DEFAULT_LOW_SIGNAL_RATIO = 0.1
DEFAULT_HIGH_SIGNAL_RATIO = 1.0
DEFAULT_RAY_INTENSITY_PERCENT = 100.0

LightFn = Callable[..., dict[str, int]]
RaySetCctFn = Callable[..., dict[str, Any]]
AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
CaptureFn = Callable[..., camera_gphoto2.CaptureResult]
DecoderFn = Callable[..., camera_gphoto2.DecodeResult]


def load_endpoint_calibration(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("measurement", {}).get("kind") != "camera_based_rgbww_optimizer_white_endpoint_ray_match":
        raise ValueError(f"unsupported endpoint calibration kind in {path}")
    matches = data.get("ray_endpoint_matches", {})
    if "cw" not in matches or "ww" not in matches:
        raise ValueError(f"endpoint calibration must contain cw and ww matches: {path}")
    white_range = data.get("white_range")
    if not isinstance(white_range, dict):
        raise ValueError(f"endpoint calibration must contain white_range: {path}")
    return data


def solve_high_output_mix(
    basis_vectors: dict[str, Any],
    target_vector: Any,
    *,
    regions: Sequence[dict[str, Any]],
    rgb_penalty: float,
    endpoint_bias: str | None,
    channels: Sequence[str] = common.DEFAULT_CHANNELS,
    max_code: int = DEFAULT_MAX_CODE,
    coarse_levels: Sequence[float] = DEFAULT_COARSE_LEVELS,
    refinement_steps: Sequence[float] = DEFAULT_REFINEMENT_STEPS,
) -> dict[str, Any]:
    np = common.import_numpy()
    matrix = np.column_stack([common.weighted_vector(basis_vectors[channel], regions) for channel in channels])
    target = common.weighted_vector(target_vector, regions)
    if target.size != matrix.shape[0]:
        raise ValueError(f"target vector length {target.size} does not match basis length {matrix.shape[0]}")
    if common.vector_norm(target) <= 0:
        raise ValueError("target vector has no measurable signal")

    best_weights: Any | None = None
    best_score: float | None = None
    best_comparison: dict[str, float] | None = None
    for active_index in _active_channel_indices(channels, endpoint_bias):
        for weights in _coarse_weight_vectors(len(channels), active_index, coarse_levels):
            refined = _refine_weights(
                matrix,
                target,
                weights,
                active_index,
                channels=channels,
                rgb_penalty=rgb_penalty,
                refinement_steps=refinement_steps,
            )
            comparison = common.compare_vectors(matrix @ refined, target)
            score = comparison["relative_rmse"] + rgb_penalty * _rgb_fraction(refined, channels)
            if best_score is None or score < best_score:
                best_weights = refined
                best_score = score
                best_comparison = comparison

    if best_weights is None or best_comparison is None or best_score is None:
        raise RuntimeError("could not solve high-output RGBWW mix")

    command = {
        channel: int(round(float(weight) * max_code))
        for channel, weight in zip(channels, best_weights)
    }
    active_channel = max(command, key=command.get)
    command[active_channel] = int(max_code)
    rgb_fraction = _rgb_fraction(best_weights, channels)
    weights = {channel: float(best_weights[index]) for index, channel in enumerate(channels)}
    return {
        "command": command,
        "weights": weights,
        "active_channel": active_channel,
        "comparison": best_comparison,
        "score": float(best_score),
        "rgb_fraction": rgb_fraction,
        "rgb_penalty": float(rgb_penalty),
        "endpoint_bias": endpoint_bias,
        "predicted_vector_norm": common.vector_norm(matrix @ best_weights),
        "target_vector_norm": common.vector_norm(target),
    }


def run_white_lut_calibration(
    *,
    output_root: Path,
    run_name: str | None,
    endpoint_calibration: Path,
    location_config: Path,
    channel_response: Path,
    target_ccts: Sequence[int],
    target_gm_values: Sequence[int],
    neutral_roles: Sequence[str],
    color_weight: float,
    inside_rgb_penalty: float,
    outside_rgb_penalty: float,
    endpoint_rgb_penalty: float,
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
    output_json: Path | None = None,
    low_signal_ratio: float = DEFAULT_LOW_SIGNAL_RATIO,
    high_signal_ratio: float = DEFAULT_HIGH_SIGNAL_RATIO,
    leave_ray_on: bool = False,
    light_fn: LightFn = esphome.light,
    ray_set_cct_fn: RaySetCctFn = ray120c.set_cct,
    auto_expose_fn: AutoExposeFn = camera_gphoto2.auto_expose_capture,
    capture_fn: CaptureFn = camera_gphoto2.capture_image,
    decoder_fn: DecoderFn = camera_gphoto2.decode_raw_image,
) -> Path:
    common.validate_high_output_plan(
        max_code=max_code,
        safe_code_limit=safe_code_limit,
        allow_high_output=allow_high_output,
        dry_run=dry_run,
        operation="white LUT calibration",
    )
    endpoint_data = load_endpoint_calibration(endpoint_calibration)
    endpoint_matches = endpoint_data["ray_endpoint_matches"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / (run_name or timestamp)
    if output_json is None:
        output_json = run_dir / "white-lut-calibration.json"
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
    basis = common.load_channel_basis(channel_response, regions, max_code=max_code)
    target_plan = common.build_target_grid(target_ccts, target_gm_values)
    result: dict[str, Any] = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "status": "planned" if dry_run else "running",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_white_lut_from_endpoint_calibration",
            "target_ccts": [int(value) for value in target_ccts],
            "target_gm_values": [int(value) for value in target_gm_values],
            "endpoint_calibration": str(endpoint_calibration),
            "endpoint_calibration_created_at": endpoint_data.get("created_at"),
            "white_range": endpoint_data["white_range"],
            "ray_intensity_percent": float(ray_intensity_percent),
            "max_code": int(max_code),
            "high_output_constraint": "max(cw, ww, r, g, b) == max_code for every RGBWW candidate",
            "allow_high_output": bool(allow_high_output),
            "settle_seconds": float(settle_seconds),
            "location_config": str(location_config),
            "regions": location_regions.jsonable_regions(regions),
            "neutral_roles": list(neutral_roles),
            "color_weight": float(color_weight),
            "inside_rgb_penalty": float(inside_rgb_penalty),
            "outside_rgb_penalty": float(outside_rgb_penalty),
            "endpoint_rgb_penalty": float(endpoint_rgb_penalty),
            "channel_response": str(channel_response),
            "channel_response_kind": basis["kind"],
            "channel_response_sources": basis["source_measurements"],
            "notes": [
                "CW/WW endpoint CCT/G-M range is read from an independent white endpoint measurement JSON.",
                "Neutral patches are primary; color patches are auxiliary with lower weight.",
                "Targets inside the Ray-matched CW/WW CCT span get stronger RGB penalty; outside targets allow RGB exploration.",
                "The code-duty curve is applied by the ESPHome control layer; stored commands are desired linear channel codes.",
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
        "target_plan": target_plan,
        "ray_endpoint_matches": endpoint_matches,
        "white_range": endpoint_data["white_range"],
        "targets": [],
    }
    common.write_json(output_json, result)
    if dry_run:
        result["status"] = "dry_run"
        common.write_json(output_json, result)
        return output_json

    last_ray_target: dict[str, int] | None = None
    try:
        light_fn(0, 0, 0, 0, 0)
        for target in target_plan:
            print(f"target {target['index'] + 1}/{len(target_plan)}: Ray {target['cct']}K gm={target['gm']} at {ray_intensity_percent:g}%")
            last_ray_target = {"cct": int(target["cct"]), "gm": int(target["gm"])}
            ray_response = ray_set_cct_fn(
                target["cct"],
                intensity_percent=ray_intensity_percent,
                gm=target["gm"],
            )
            time.sleep(max(0.0, settle_seconds))
            ray_capture = common.capture_auto_exposed(
                auto_expose_fn=auto_expose_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                scratch_dir=scratch_dir,
                filename_template=f"target-ray-{target['index']:02d}-{target['cct']}K-gm{target['gm']}.%C",
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
            ray_seconds, target_vector, ray_regions = common.measure_auto_exposure_regions(ray_capture, regions)
            range_class = common.classify_target_range(
                target["cct"],
                cw_match=endpoint_matches["cw"],
                ww_match=endpoint_matches["ww"],
            )
            endpoint_bias = _endpoint_bias_for_range(range_class, matches=endpoint_matches)
            rgb_penalty = inside_rgb_penalty if range_class["inside"] else outside_rgb_penalty
            if endpoint_bias is not None and not range_class["inside"]:
                rgb_penalty = min(rgb_penalty, endpoint_rgb_penalty)
            solution = solve_high_output_mix(
                basis["vectors"],
                target_vector,
                regions=regions,
                rgb_penalty=rgb_penalty,
                endpoint_bias=endpoint_bias,
                max_code=max_code,
            )
            command = solution["command"]
            print(
                f"  {range_class['mode']} rgb_penalty={rgb_penalty:g} "
                f"command: cw={command['cw']} ww={command['ww']} r={command['r']} g={command['g']} b={command['b']}"
            )
            payload = light_fn(command["cw"], command["ww"], command["r"], command["g"], command["b"])
            time.sleep(max(0.0, settle_seconds))
            rgbww_capture = common.capture_fixed(
                capture_fn=capture_fn,
                decoder_fn=decoder_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                filename_template=f"target-rgbww-{target['index']:02d}-{target['cct']}K-gm{target['gm']}.%C",
                iso=iso,
                aperture=aperture,
                image_format=image_format,
                shutter_speed=ray_capture.final_capture.settings.shutter_speed,
                decode_formats=decode_formats,
                metering_regions=metering_regions,
            )
            rgbww_seconds, rgbww_vector, rgbww_regions = common.measure_capture_regions(rgbww_capture, regions)
            measured_comparison = common.compare_vectors(
                common.weighted_vector(rgbww_vector, regions),
                common.weighted_vector(target_vector, regions),
            )
            exposure_warning = common.exposure_warning(
                rgbww_capture,
                target_max=target_max,
                low_signal_ratio=low_signal_ratio,
                high_signal_ratio=high_signal_ratio,
            )
            target_result = {
                **target,
                "range_classification": range_class,
                "ray": {
                    "set_response": ray_response,
                    "auto_exposure": ray_capture.to_jsonable(),
                    "shutter_seconds": ray_seconds,
                    "vector_norm": common.vector_norm(target_vector),
                    "regions": ray_regions,
                },
                "solver": {
                    **solution,
                    "max_channel_value": max(command.values()),
                },
                "rgbww": {
                    "payload": payload,
                    "capture": rgbww_capture.to_jsonable(),
                    "shutter_seconds": rgbww_seconds,
                    "vector_norm": common.vector_norm(rgbww_vector),
                    "comparison_to_ray_weighted": measured_comparison,
                    "exposure_warning": exposure_warning,
                    "regions": rgbww_regions,
                },
            }
            result["targets"].append(target_result)
            common.write_json(output_json, result)
            if exposure_warning:
                print(f"  exposure warning: {exposure_warning['kind']}")

        result["status"] = "complete"
        common.write_json(output_json, result)
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
        description="Measure a small CCT/G-M white calibration LUT using a prior WW/CW endpoint calibration JSON."
    )
    parser.add_argument("--endpoint-calibration", type=Path, default=DEFAULT_ENDPOINT_CALIBRATION)
    parser.add_argument("--target-ccts", "--ccts", type=common.parse_int_values, default=DEFAULT_TARGET_CCTS)
    parser.add_argument("--target-gm-values", "--gm-values", type=common.parse_int_values, default=DEFAULT_TARGET_GM_VALUES)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--channel-response", type=Path, default=DEFAULT_CHANNEL_RESPONSE)
    parser.add_argument("--block-indices", type=measure_channel_response.parse_block_indices, default="all")
    parser.add_argument("--neutral-roles", type=common.parse_roles, default=common.DEFAULT_NEUTRAL_ROLES)
    parser.add_argument("--color-weight", type=float, default=common.DEFAULT_COLOR_WEIGHT)
    parser.add_argument("--inside-rgb-penalty", type=float, default=DEFAULT_INSIDE_RGB_PENALTY)
    parser.add_argument("--outside-rgb-penalty", type=float, default=DEFAULT_OUTSIDE_RGB_PENALTY)
    parser.add_argument("--endpoint-rgb-penalty", type=float, default=DEFAULT_ENDPOINT_RGB_PENALTY)
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
    parser.add_argument("--low-signal-ratio", type=float, default=DEFAULT_LOW_SIGNAL_RATIO)
    parser.add_argument("--high-signal-ratio", type=float, default=DEFAULT_HIGH_SIGNAL_RATIO)
    parser.add_argument("--leave-ray-on", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_json = run_white_lut_calibration(
        output_root=args.output_dir,
        run_name=args.run_name,
        endpoint_calibration=args.endpoint_calibration,
        location_config=args.location_config,
        channel_response=args.channel_response,
        target_ccts=args.target_ccts,
        target_gm_values=args.target_gm_values,
        neutral_roles=args.neutral_roles,
        color_weight=args.color_weight,
        inside_rgb_penalty=args.inside_rgb_penalty,
        outside_rgb_penalty=args.outside_rgb_penalty,
        endpoint_rgb_penalty=args.endpoint_rgb_penalty,
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
        output_json=args.output_json,
        low_signal_ratio=args.low_signal_ratio,
        high_signal_ratio=args.high_signal_ratio,
        leave_ray_on=args.leave_ray_on,
    )
    print(output_json)
    return 0


def _active_channel_indices(channels: Sequence[str], endpoint_bias: str | None) -> list[int]:
    if endpoint_bias in channels:
        return [channels.index(endpoint_bias)]
    return list(range(len(channels)))


def _coarse_weight_vectors(channel_count: int, active_index: int, levels: Sequence[float]) -> list[Any]:
    np = common.import_numpy()
    vectors = []
    for values in itertools.product(levels, repeat=channel_count - 1):
        weights = np.zeros(channel_count, dtype="float64")
        weights[active_index] = 1.0
        value_iter = iter(values)
        for index in range(channel_count):
            if index == active_index:
                continue
            weights[index] = min(max(float(next(value_iter)), 0.0), 1.0)
        vectors.append(weights)
    return vectors


def _refine_weights(
    matrix: Any,
    target: Any,
    weights: Any,
    active_index: int,
    *,
    channels: Sequence[str],
    rgb_penalty: float,
    refinement_steps: Sequence[float],
) -> Any:
    np = common.import_numpy()
    current = np.array(weights, dtype="float64")
    best_score = _solver_score(matrix, target, current, channels=channels, rgb_penalty=rgb_penalty)
    for step in refinement_steps:
        improved = True
        while improved:
            improved = False
            for index in range(current.size):
                if index == active_index:
                    continue
                for delta in (-float(step), float(step)):
                    candidate = np.array(current, dtype="float64")
                    candidate[index] = min(max(candidate[index] + delta, 0.0), 1.0)
                    score = _solver_score(matrix, target, candidate, channels=channels, rgb_penalty=rgb_penalty)
                    if score + 1e-12 < best_score:
                        current = candidate
                        best_score = score
                        improved = True
    current[active_index] = 1.0
    return current


def _solver_score(matrix: Any, target: Any, weights: Any, *, channels: Sequence[str], rgb_penalty: float) -> float:
    comparison = common.compare_vectors(matrix @ weights, target)
    return float(comparison["relative_rmse"]) + float(rgb_penalty) * _rgb_fraction(weights, channels)


def _rgb_fraction(weights: Any, channels: Sequence[str]) -> float:
    total = sum(float(value) for value in weights)
    if total <= 0:
        return 0.0
    rgb = sum(float(weights[index]) for index, channel in enumerate(channels) if channel in {"r", "g", "b"})
    return float(rgb / total)


def _endpoint_bias_for_range(range_class: dict[str, Any], *, matches: dict[str, dict[str, Any]]) -> str | None:
    if range_class["inside"]:
        return None
    cct = range_class["low_cct"] if range_class["mode"].startswith("below") else range_class["high_cct"]
    distances = {
        channel: abs(int(match["best"]["cct"]) - int(cct))
        for channel, match in matches.items()
    }
    return min(distances, key=distances.get)


if __name__ == "__main__":
    raise SystemExit(main())
