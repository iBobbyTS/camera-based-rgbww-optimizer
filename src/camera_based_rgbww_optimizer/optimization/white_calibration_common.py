from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.measurement import recorded_exposure
from camera_based_rgbww_optimizer.optimization import measure_channel_response
from camera_based_rgbww_optimizer.utils import location_regions


DEFAULT_CHANNELS = ("cw", "ww", "r", "g", "b")
DEFAULT_NEUTRAL_ROLES = ("neutral",)
DEFAULT_COLOR_WEIGHT = 0.2
DEFAULT_MAX_CODE = 4095
DEFAULT_CCT_ERROR_SCALE = 500.0
DEFAULT_DUV_ERROR_SCALE = 0.005

AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
CaptureFn = Callable[..., camera_gphoto2.CaptureResult]
DecoderFn = Callable[..., camera_gphoto2.DecodeResult]


def parse_int_values(value: str) -> tuple[int, ...]:
    tokens = [token.strip() for token in value.replace(",", " ").split() if token.strip()]
    if not tokens:
        raise argparse.ArgumentTypeError("at least one integer value is required")
    values: list[int] = []
    for token in tokens:
        try:
            values.append(int(token))
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"invalid integer value: {token}") from exc
    return tuple(values)


def parse_roles(value: str) -> tuple[str, ...]:
    roles = tuple(token.strip().lower() for token in value.replace(",", " ").split() if token.strip())
    if not roles:
        raise argparse.ArgumentTypeError("at least one role is required")
    return roles


def build_target_grid(ccts: Sequence[int], gm_values: Sequence[int]) -> list[dict[str, int]]:
    return [
        {"index": index, "cct": int(cct), "gm": int(gm)}
        for index, (cct, gm) in enumerate(itertools.product(ccts, gm_values))
    ]


def validate_high_output_plan(
    *,
    max_code: int,
    safe_code_limit: int,
    allow_high_output: bool,
    dry_run: bool,
    operation: str,
) -> None:
    if max_code <= 0:
        raise ValueError("max-code must be positive")
    if max_code > safe_code_limit and not allow_high_output and not dry_run:
        raise ValueError(
            f"{operation} requires at least one channel at max-code {max_code}; "
            f"pass --allow-high-output after confirming the fixture is safe above {safe_code_limit}"
        )


def select_weighted_regions(
    regions: Sequence[dict[str, Any]],
    *,
    neutral_roles: Sequence[str],
    color_weight: float,
) -> list[dict[str, Any]]:
    neutral = {role.lower() for role in neutral_roles}
    weighted: list[dict[str, Any]] = []
    for region in regions:
        patch_roles = {
            str(role).lower()
            for role in region.get("patch", {}).get("roles", [])
        }
        is_neutral = bool(neutral & patch_roles)
        weight = 1.0 if is_neutral else float(color_weight)
        item = dict(region)
        item["calibration_weight"] = weight
        item["calibration_primary"] = bool(is_neutral)
        weighted.append(item)
    if not any(region["calibration_primary"] for region in weighted):
        raise ValueError(f"no primary white/gray regions matched roles: {', '.join(neutral_roles)}")
    return weighted


def load_weighted_location_regions(
    location_config: Path,
    block_indices: str | tuple[int, ...],
    *,
    neutral_roles: Sequence[str],
    color_weight: float,
) -> list[dict[str, Any]]:
    return select_weighted_regions(
        location_regions.load_location_regions(location_config, block_indices),
        neutral_roles=neutral_roles,
        color_weight=color_weight,
    )


def resolve_metering_regions(
    *,
    auto_exposure_metering_mode: str,
    location_config: Path,
    auto_exposure_metering_location_config: Path | None,
) -> tuple[Path | None, list[dict[str, Any]] | None]:
    if auto_exposure_metering_mode != camera_gphoto2.METERING_MODE_LOCATION:
        return None, None
    metering_config = auto_exposure_metering_location_config or location_config
    return metering_config, camera_gphoto2.load_metering_regions(metering_config)


def load_channel_basis(
    response_path: Path,
    regions: Sequence[dict[str, Any]],
    *,
    channels: Sequence[str] = DEFAULT_CHANNELS,
    max_code: int = DEFAULT_MAX_CODE,
) -> dict[str, Any]:
    np = import_numpy()
    data = json.loads(Path(response_path).read_text(encoding="utf-8"))
    selected_names = [str(region["name"]) for region in regions]
    measurements = data.get("measurements", [])
    vectors: dict[str, Any] = {}
    source_measurements: dict[str, dict[str, Any]] = {}
    for channel in channels:
        channel_measurements = [
            item
            for item in measurements
            if item.get("channel") == channel and int(item.get("code", 0)) > 0
        ]
        if not channel_measurements:
            raise ValueError(f"channel response has no positive measurements for channel {channel}")
        measurement = max(channel_measurements, key=lambda item: int(item.get("code", 0)))
        code = int(measurement["code"])
        region_map = {region["name"]: region for region in measurement.get("regions", [])}
        values: list[float] = []
        for name in selected_names:
            if name not in region_map:
                raise ValueError(f"channel response missing region {name!r} for channel {channel}")
            values.extend(region_channel_mean_per_second(region_map[name], prefer_ambient_subtracted=True))
        scale = float(max_code) / float(code)
        vectors[channel] = np.asarray(values, dtype="float64") * scale
        source_measurements[channel] = {
            "source_file": measurement.get("source_file"),
            "source_index": measurement.get("source_index"),
            "code": code,
            "original_channel": measurement.get("original_channel"),
        }
    return {
        "kind": data.get("kind"),
        "path": str(response_path),
        "channels": list(channels),
        "max_code": int(max_code),
        "regions": list(selected_names),
        "vectors": vectors,
        "source_measurements": source_measurements,
    }


def region_measurement_vector(measurements: Sequence[dict[str, Any]]) -> Any:
    np = import_numpy()
    values: list[float] = []
    for measurement in measurements:
        values.extend(region_channel_mean_per_second(measurement, prefer_ambient_subtracted=False))
    return np.asarray(values, dtype="float64")


def weighted_vector(vector: Any, regions: Sequence[dict[str, Any]]) -> Any:
    np = import_numpy()
    weights: list[float] = []
    for region in regions:
        weights.extend([math.sqrt(float(region.get("calibration_weight", 1.0)))] * 3)
    return np.asarray(vector, dtype="float64") * np.asarray(weights, dtype="float64")


def compare_vectors(candidate_vector: Any, target_vector: Any) -> dict[str, float]:
    np = import_numpy()
    candidate = np.asarray(candidate_vector, dtype="float64")
    target = np.asarray(target_vector, dtype="float64")
    candidate_norm = vector_norm(candidate)
    target_norm = vector_norm(target)
    if candidate_norm <= 0 or target_norm <= 0:
        return {
            "relative_rmse": float("inf"),
            "cosine_distance": float("inf"),
            "scale_to_reference": 0.0,
            "brightness_ratio": 0.0,
        }
    scale = float(np.dot(target, candidate) / np.dot(candidate, candidate))
    residual = target - candidate * scale
    relative_rmse = float(np.sqrt(np.mean(residual * residual)) / (target_norm / (target.size ** 0.5)))
    cosine = float(np.dot(candidate, target) / (candidate_norm * target_norm))
    return {
        "relative_rmse": relative_rmse,
        "cosine_distance": float(1.0 - max(min(cosine, 1.0), -1.0)),
        "scale_to_reference": scale,
        "brightness_ratio": float(candidate_norm / target_norm),
    }


def compare_white_points(
    candidate: dict[str, Any],
    target: dict[str, Any],
    *,
    cct_error_scale: float = DEFAULT_CCT_ERROR_SCALE,
    duv_error_scale: float = DEFAULT_DUV_ERROR_SCALE,
) -> dict[str, float]:
    cct_error = float(candidate["cct_K"]) - float(target["cct_K"])
    duv_error = float(candidate["duv"]) - float(target["duv"])
    cct_scale = float(cct_error_scale)
    duv_scale = float(duv_error_scale)
    if cct_scale <= 0:
        raise ValueError("cct_error_scale must be positive")
    if duv_scale <= 0:
        raise ValueError("duv_error_scale must be positive")
    normalized_cct = cct_error / cct_scale
    normalized_duv = duv_error / duv_scale
    score = math.sqrt(normalized_cct * normalized_cct + normalized_duv * normalized_duv)
    return {
        "cct_error_K": cct_error,
        "duv_error": duv_error,
        "absolute_cct_error_K": abs(cct_error),
        "absolute_duv_error": abs(duv_error),
        "normalized_score": score,
    }


def best_ray_match(
    strip_vector: Any,
    ray_measurements: Sequence[dict[str, Any]],
    *,
    regions: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    strip_weighted = weighted_vector(strip_vector, regions)
    comparisons = []
    for measurement in ray_measurements:
        comparison = compare_vectors(weighted_vector(measurement["vector"], regions), strip_weighted)
        comparisons.append({
            "cct": int(measurement["cct"]),
            "gm": int(measurement["gm"]),
            **comparison,
        })
    comparisons.sort(key=lambda item: (item["relative_rmse"], item["cosine_distance"]))
    return {
        "best": comparisons[0],
        "ranked": comparisons,
    }


def select_white_point_region(regions: Sequence[dict[str, Any]]) -> dict[str, Any]:
    if not regions:
        raise ValueError("at least one region is required to estimate white point")
    for region in regions:
        patch = region.get("patch", {})
        roles = {str(role).lower() for role in patch.get("roles", [])}
        if "white" in roles or str(patch.get("name", "")).lower() == "white":
            return region
    for region in regions:
        patch = region.get("patch", {})
        roles = {str(role).lower() for role in patch.get("roles", [])}
        if "neutral" in roles and "black" not in roles:
            return region
    return regions[0]


def estimate_capture_white_point(
    capture: camera_gphoto2.CaptureResult,
    regions: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    np = import_numpy()
    image = load_npy(find_npy_output(capture))
    region = select_white_point_region(regions)
    pixels = location_regions.extract_region(np, image, region)
    summary = measure_channel_response.summarize_region(pixels)
    channel_mean = np.asarray(summary["channel_mean"], dtype="float64")
    if channel_mean.size < 3:
        raise ValueError("white point estimation requires at least three decoded channels")
    if float(channel_mean[1]) <= 0:
        raise ValueError("green channel mean must be positive for white point estimation")
    camera_neutral = channel_mean[:3] / float(channel_mean[1])
    wb_gains = float(channel_mean[1]) / channel_mean[:3]
    matrix = _load_rawpy_rgb_xyz_matrix(capture.saved_file, np)
    estimate = estimate_white_point_from_camera_neutral(camera_neutral, matrix, np_module=np)
    return {
        **estimate,
        "method": "white_patch_rawpy_matrix_inverse_planckian_locus",
        "region": {
            "name": region["name"],
            "patch": region.get("patch"),
            "pixel_count": int(summary["pixel_count"]),
            "channel_mean": float_list(summary["channel_mean"]),
            "channel_median": float_list(summary["channel_median"]),
            "channel_p10": float_list(summary["channel_p10"]),
            "channel_p90": float_list(summary["channel_p90"]),
        },
        "camera_neutral_g1": float_list(camera_neutral),
        "white_balance_gains_g1": float_list(wb_gains),
        "rawpy_rgb_xyz_matrix_first3": matrix.tolist(),
    }


def estimate_white_point_from_camera_neutral(
    camera_neutral: Sequence[Any],
    rgb_xyz_matrix: Any,
    *,
    np_module: Any | None = None,
) -> dict[str, Any]:
    np = np_module or import_numpy()
    neutral = np.asarray(camera_neutral, dtype="float64")
    if neutral.size < 3:
        raise ValueError("camera_neutral must contain at least three channels")
    matrix = np.asarray(rgb_xyz_matrix, dtype="float64")
    if matrix.shape != (3, 3):
        raise ValueError("rgb_xyz_matrix must be 3x3")
    # Empirically for this LibRaw/rawpy path, inverse(matrix) maps camera-neutral
    # observations into plausible XYZ white points for Canon CR3 files.
    xyz = np.linalg.inv(matrix) @ neutral[:3]
    x, y = xyz_to_xy(xyz)
    cct, duv, u, v = cct_duv_from_xy(x, y, np_module=np)
    return {
        "cct_K": float(cct),
        "duv": float(duv),
        "xy": [float(x), float(y)],
        "uv1960": [float(u), float(v)],
        "approx_XYZ": float_list(xyz),
    }


def xyz_to_xy(xyz: Sequence[Any]) -> tuple[float, float]:
    values = import_numpy().asarray(xyz, dtype="float64")
    total = float(values.sum())
    if total == 0:
        raise ValueError("XYZ sum must be non-zero")
    return float(values[0] / total), float(values[1] / total)


def xy_to_uv1960(x: float, y: float) -> tuple[float, float]:
    denominator = -2.0 * float(x) + 12.0 * float(y) + 3.0
    if denominator == 0:
        raise ValueError("xy point cannot be converted to CIE 1960 UCS")
    return 4.0 * float(x) / denominator, 6.0 * float(y) / denominator


def cct_duv_from_xy(
    x: float,
    y: float,
    *,
    np_module: Any | None = None,
) -> tuple[float, float, float, float]:
    np = np_module or import_numpy()
    target = np.asarray(xy_to_uv1960(x, y), dtype="float64")
    low = 1000.0
    high = 25000.0
    best_temperature = 0.0
    best_distance = float("inf")
    best_uv = None
    for _ in range(6):
        temperatures = np.geomspace(low, high, 300)
        uvs = np.asarray([xy_to_uv1960(*_planck_xy(float(value), np)) for value in temperatures], dtype="float64")
        distances = np.linalg.norm(uvs - target, axis=1)
        index = int(distances.argmin())
        best_temperature = float(temperatures[index])
        best_distance = float(distances[index])
        best_uv = uvs[index]
        low = float(temperatures[max(0, index - 3)])
        high = float(temperatures[min(len(temperatures) - 1, index + 3)])
    assert best_uv is not None
    epsilon = max(1.0, best_temperature * 0.001)
    lower_uv = np.asarray(xy_to_uv1960(*_planck_xy(max(1000.0, best_temperature - epsilon), np)), dtype="float64")
    upper_uv = np.asarray(xy_to_uv1960(*_planck_xy(best_temperature + epsilon, np)), dtype="float64")
    tangent = upper_uv - lower_uv
    cross = tangent[0] * (target[1] - best_uv[1]) - tangent[1] * (target[0] - best_uv[0])
    duv = best_distance if cross >= 0 else -best_distance
    return best_temperature, duv, float(target[0]), float(target[1])


def classify_target_range(
    cct: int,
    *,
    cw_match: dict[str, Any],
    ww_match: dict[str, Any],
) -> dict[str, Any]:
    cw_cct = int(cw_match["best"]["cct"])
    ww_cct = int(ww_match["best"]["cct"])
    low = min(cw_cct, ww_cct)
    high = max(cw_cct, ww_cct)
    if low <= int(cct) <= high:
        mode = "inside_cw_ww_ray_matched_range"
        distance = 0
    elif int(cct) < low:
        mode = "below_cw_ww_ray_matched_range"
        distance = low - int(cct)
    else:
        mode = "above_cw_ww_ray_matched_range"
        distance = int(cct) - high
    return {
        "mode": mode,
        "low_cct": low,
        "high_cct": high,
        "distance_kelvin": distance,
        "inside": mode == "inside_cw_ww_ray_matched_range",
    }


def capture_auto_exposed(
    *,
    auto_expose_fn: AutoExposeFn,
    camera_dir: Path,
    decode_dir: Path,
    scratch_dir: Path,
    filename_template: str,
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
    initial_shutter_speed: str | None = None,
) -> camera_gphoto2.AutoExposureResult:
    return auto_expose_fn(
        output_dir=camera_dir,
        filename_template=filename_template,
        target_max=target_max,
        iso=iso,
        aperture=aperture,
        image_format=image_format,
        min_shutter_speed=min_shutter_speed,
        max_shutter_speed=max_shutter_speed,
        max_trials=max_trials,
        max_captures=max_captures,
        decode_output_dir=decode_dir,
        decode_formats=decode_formats,
        scratch_dir=scratch_dir,
        metering_regions=metering_regions,
        initial_shutter_speed=initial_shutter_speed,
    )


def capture_fixed(
    *,
    capture_fn: CaptureFn,
    decoder_fn: DecoderFn,
    camera_dir: Path,
    decode_dir: Path,
    filename_template: str,
    iso: str,
    aperture: str,
    image_format: str,
    shutter_speed: str,
    decode_formats: Sequence[str],
    metering_regions: Sequence[dict[str, Any]] | None,
) -> camera_gphoto2.CaptureResult:
    capture = capture_fn(
        output_dir=camera_dir,
        filename_template=filename_template,
        settings=camera_gphoto2.CaptureSettings(
            iso=iso,
            aperture=aperture,
            shutter_speed=shutter_speed,
            image_format=image_format,
        ),
        timeout=120.0,
    )
    decoded = decoder_fn(
        capture.saved_file,
        output_dir=decode_dir,
        formats=decode_formats,
        metering_regions=metering_regions,
    )
    return camera_gphoto2.CaptureResult(
        connection=capture.connection,
        settings=capture.settings,
        saved_file=capture.saved_file,
        stdout=capture.stdout,
        decoded=decoded,
        backend=capture.backend,
        endpoint=capture.endpoint,
        http_attempts=capture.http_attempts,
    )


def measure_capture_regions(
    capture: camera_gphoto2.CaptureResult,
    regions: Sequence[dict[str, Any]],
) -> tuple[float, Any, list[dict[str, Any]]]:
    seconds = recorded_exposure.resolve_recorded_exposure(
        capture.saved_file,
        capture.settings.shutter_speed,
    ).seconds
    image = load_npy(find_npy_output(capture))
    measurements = measure_channel_response.measure_image_regions(
        image,
        regions,
        shutter_seconds_value=seconds,
    )
    return seconds, region_measurement_vector(measurements), measurements


def measure_auto_exposure_regions(
    capture: camera_gphoto2.AutoExposureResult,
    regions: Sequence[dict[str, Any]],
) -> tuple[float, Any, list[dict[str, Any]]]:
    return measure_capture_regions(capture.final_capture, regions)


def find_npy_output(capture: camera_gphoto2.CaptureResult) -> Path:
    return measure_channel_response.find_npy_output(capture)


def remove_capture_npy_outputs(capture: camera_gphoto2.CaptureResult) -> tuple[Path, ...]:
    if capture.decoded is None:
        return ()
    removed: list[Path] = []
    for output_file in capture.decoded.output_files:
        path = Path(output_file)
        if path.suffix.lower() != ".npy":
            continue
        path.unlink(missing_ok=True)
        removed.append(path)
    return tuple(removed)


def load_npy(path: Path) -> Any:
    np = import_numpy()
    return np.load(path)


def load_rawpy_rgb_xyz_matrix(raw_file: Path, np_module: Any | None = None) -> Any:
    np = np_module or import_numpy()
    try:
        import rawpy
    except ImportError as exc:
        raise RuntimeError("rawpy is required to estimate CCT/Duv from RAW captures") from exc
    with rawpy.imread(str(raw_file)) as raw:
        return np.asarray(raw.rgb_xyz_matrix[:3], dtype="float64")


_load_rawpy_rgb_xyz_matrix = load_rawpy_rgb_xyz_matrix


def _planck_xy(temperature: float, np: Any) -> tuple[float, float]:
    wavelengths_nm = np.arange(380.0, 781.0, 5.0)
    wavelengths_m = wavelengths_nm * 1e-9
    c2 = 1.438776877e-2
    spectrum = 1.0 / (np.power(wavelengths_m, 5) * np.expm1(c2 / (wavelengths_m * float(temperature))))
    cmf = np.column_stack(
        [
            _cie1931_xbar_approx(wavelengths_nm, np),
            _cie1931_ybar_approx(wavelengths_nm, np),
            _cie1931_zbar_approx(wavelengths_nm, np),
        ]
    )
    xyz = np.trapezoid(spectrum[:, None] * cmf, wavelengths_nm, axis=0)
    return xyz_to_xy(xyz)


def _cie1931_xbar_approx(wavelengths_nm: Any, np: Any) -> Any:
    t1 = (wavelengths_nm - 442.0) * np.where(wavelengths_nm < 442.0, 0.0624, 0.0374)
    t2 = (wavelengths_nm - 599.8) * np.where(wavelengths_nm < 599.8, 0.0264, 0.0323)
    t3 = (wavelengths_nm - 501.1) * np.where(wavelengths_nm < 501.1, 0.0490, 0.0382)
    return 0.362 * np.exp(-0.5 * t1 * t1) + 1.056 * np.exp(-0.5 * t2 * t2) - 0.065 * np.exp(-0.5 * t3 * t3)


def _cie1931_ybar_approx(wavelengths_nm: Any, np: Any) -> Any:
    t1 = (wavelengths_nm - 568.8) * np.where(wavelengths_nm < 568.8, 0.0213, 0.0247)
    t2 = (wavelengths_nm - 530.9) * np.where(wavelengths_nm < 530.9, 0.0613, 0.0322)
    return 0.821 * np.exp(-0.5 * t1 * t1) + 0.286 * np.exp(-0.5 * t2 * t2)


def _cie1931_zbar_approx(wavelengths_nm: Any, np: Any) -> Any:
    t1 = (wavelengths_nm - 437.0) * np.where(wavelengths_nm < 437.0, 0.0845, 0.0278)
    t2 = (wavelengths_nm - 459.0) * np.where(wavelengths_nm < 459.0, 0.0385, 0.0725)
    return 1.217 * np.exp(-0.5 * t1 * t1) + 0.681 * np.exp(-0.5 * t2 * t2)


def region_channel_mean_per_second(region: dict[str, Any], *, prefer_ambient_subtracted: bool) -> list[float]:
    if prefer_ambient_subtracted:
        if "ambient_subtracted_channel_mean_per_second" in region:
            return float_list(region["ambient_subtracted_channel_mean_per_second"])
        ambient_subtracted = region.get("ambient_subtracted")
        if isinstance(ambient_subtracted, dict) and "channel_mean_per_second" in ambient_subtracted:
            return float_list(ambient_subtracted["channel_mean_per_second"])
    if "channel_mean_per_second" in region:
        return float_list(region["channel_mean_per_second"])
    normalized = region.get("normalized")
    if isinstance(normalized, dict) and "channel_mean_per_second" in normalized:
        return float_list(normalized["channel_mean_per_second"])
    raise ValueError(f"region {region.get('name')} has no channel mean per second values")


def jsonable_without_vector(item: dict[str, Any]) -> dict[str, Any]:
    output = dict(item)
    output.pop("vector", None)
    return output


def exposure_warning(
    capture: camera_gphoto2.CaptureResult,
    *,
    target_max: int,
    low_signal_ratio: float,
    high_signal_ratio: float,
) -> dict[str, Any] | None:
    if capture.decoded is None:
        return None
    decoded_max = capture.decoded.stats.get("image", {}).get("max")
    if decoded_max is None:
        return None
    decoded_max = float(decoded_max)
    if decoded_max > float(target_max) * high_signal_ratio:
        return {
            "kind": "rgbww_above_reference_exposure_target",
            "decoded_max": decoded_max,
            "target_max": int(target_max),
            "suggestion": "Repeat this target with a shorter fixed shutter if clipped values are visible.",
        }
    if decoded_max < float(target_max) * low_signal_ratio:
        return {
            "kind": "rgbww_low_signal_at_reference_exposure",
            "decoded_max": decoded_max,
            "target_max": int(target_max),
            "suggestion": "Inspect noise; if needed, repeat this target with a longer exposure that still keeps Ray120c below clipping.",
        }
    return None


def vector_norm(vector: Any) -> float:
    np = import_numpy()
    return float(np.linalg.norm(vector))


def float_list(values: Sequence[Any]) -> list[float]:
    return [float(value) for value in values]


def import_numpy() -> Any:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for white calibration") from exc
    return np


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
