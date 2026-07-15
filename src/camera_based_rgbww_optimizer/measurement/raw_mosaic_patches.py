from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.paths import PROJECT_ROOT
from camera_based_rgbww_optimizer.utils import location_regions


PLANE_ORDER = ("R", "G1", "G2", "B")
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config/camera/raw-observer.json"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config/location/locations-20260714-211759.json"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "tmp/raw-observer-validation"
BLACK_LEVEL_FALLBACK_MIN_SAMPLES = 128
BLACK_LEVEL_FALLBACK_MIN_MODAL_FRACTION = 0.01
BLACK_LEVEL_FALLBACK_TOLERANCE_FRACTION = 0.01


@dataclass(frozen=True)
class RawMosaicFrame:
    source_file: Path
    mosaic: np.ndarray
    raw_pattern: np.ndarray
    color_desc: str
    black_levels: tuple[float, ...]
    white_level: float
    camera_white_levels: tuple[float, ...] | None
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RawExposureMeterResult:
    """Native-Bayer exposure result expressed on the existing 16-bit meter scale."""

    exposure_metric: int
    raw_visible_max: int | None
    plane_max: dict[str, float | None]
    clipped_fraction: float | None
    low_signal_fraction: float | None
    quality_status: str

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "exposure_metric": self.exposure_metric,
            "raw_visible_max": self.raw_visible_max,
            "plane_max": self.plane_max,
            "clipped_fraction": self.clipped_fraction,
            "low_signal_fraction": self.low_signal_fraction,
            "quality_status": self.quality_status,
        }


def load_observer_config(path: str | Path = DEFAULT_OBSERVER_CONFIG) -> dict[str, Any]:
    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("raw observer config root must be an object")
    _validate_observer_config(data)
    return data


def load_raw_mosaic(path: str | Path) -> RawMosaicFrame:
    import rawpy

    source_file = Path(path)
    with rawpy.imread(str(source_file)) as raw:
        if raw.raw_pattern is None:
            raise ValueError(f"{source_file} does not expose a Bayer raw_pattern")
        mosaic = np.asarray(raw.raw_image_visible).copy()
        raw_pattern = np.asarray(raw.raw_pattern, dtype="int16").copy()
        color_desc = bytes(raw.color_desc).decode("ascii", errors="replace").rstrip("\x00 ")
        reported_black_levels = tuple(float(value) for value in raw.black_level_per_channel)
        camera_white = getattr(raw, "camera_white_level_per_channel", None)
        camera_white_levels = None if camera_white is None else tuple(float(value) for value in camera_white)
        sizes = raw.sizes
        black_levels, black_metadata = _resolve_black_levels(
            reported_black_levels=reported_black_levels,
            raw_image=np.asarray(raw.raw_image),
            raw_pattern=raw_pattern,
            top_margin=int(sizes.top_margin),
            left_margin=int(sizes.left_margin),
            white_level=float(raw.white_level),
        )
        metadata = {
            "rawpy_version": str(getattr(rawpy, "__version__", "unknown")),
            "libraw_version": [int(value) for value in getattr(rawpy, "libraw_version", ())],
            "visible_shape": [int(value) for value in mosaic.shape],
            "raw_pattern_indices": raw_pattern.tolist(),
            "color_desc": color_desc,
            **black_metadata,
            "white_level": float(raw.white_level),
            "camera_white_level_per_channel": (
                None if camera_white_levels is None else list(camera_white_levels)
            ),
            "raw_sizes": {
                "raw_height": int(sizes.raw_height),
                "raw_width": int(sizes.raw_width),
                "height": int(sizes.height),
                "width": int(sizes.width),
                "top_margin": int(sizes.top_margin),
                "left_margin": int(sizes.left_margin),
            },
        }
        return RawMosaicFrame(
            source_file=source_file,
            mosaic=mosaic,
            raw_pattern=raw_pattern,
            color_desc=color_desc,
            black_levels=black_levels,
            white_level=float(raw.white_level),
            camera_white_levels=camera_white_levels,
            metadata=metadata,
        )


def _resolve_black_levels(
    *,
    reported_black_levels: Sequence[float],
    raw_image: np.ndarray,
    raw_pattern: np.ndarray,
    top_margin: int,
    left_margin: int,
    white_level: float,
) -> tuple[tuple[float, ...], dict[str, Any]]:
    """Use optical black margins only when RAW metadata is materially implausible."""

    reported = tuple(float(value) for value in reported_black_levels)
    optical = _optical_black_levels(
        raw_image=raw_image,
        raw_pattern=raw_pattern,
        color_count=len(reported),
        top_margin=top_margin,
        left_margin=left_margin,
    )
    tolerance = max(16.0, float(white_level) * BLACK_LEVEL_FALLBACK_TOLERANCE_FRACTION)
    resolved: list[float] = []
    sources: list[str] = []
    for index, value in enumerate(reported):
        candidate = optical[index] if optical is not None else None
        if candidate is not None and candidate >= float(white_level) - tolerance:
            candidate = None
        if candidate is not None and abs(value - candidate) > tolerance:
            resolved.append(candidate)
            sources.append("optical_black_margin_fallback")
        else:
            resolved.append(value)
            sources.append("metadata")
    return tuple(resolved), {
        "black_level_per_channel_reported": list(reported),
        "black_level_per_channel": resolved,
        "black_level_source_per_channel": sources,
        "optical_black_level_per_channel": None if optical is None else list(optical),
        "black_level_metadata_tolerance_dn": tolerance,
    }


def _optical_black_levels(
    *,
    raw_image: np.ndarray,
    raw_pattern: np.ndarray,
    color_count: int,
    top_margin: int,
    left_margin: int,
) -> tuple[float | None, ...] | None:
    image = np.asarray(raw_image)
    pattern = np.asarray(raw_pattern)
    if image.ndim != 2 or pattern.shape != (2, 2):
        return None
    top_limit = min(max(0, int(top_margin)), image.shape[0])
    left_limit = min(max(0, int(left_margin)), image.shape[1])
    if top_limit == 0 and left_limit == 0:
        return None

    samples_by_index: list[list[np.ndarray]] = [[] for _ in range(color_count)]
    for row_offset in range(2):
        for column_offset in range(2):
            color_index = int(pattern[row_offset, column_offset])
            if color_index < 0 or color_index >= color_count:
                return None
            if top_limit:
                samples_by_index[color_index].append(image[row_offset:top_limit:2, column_offset::2])
            if left_limit:
                samples_by_index[color_index].append(image[row_offset::2, column_offset:left_limit:2])

    levels: list[float | None] = []
    for samples in samples_by_index:
        values = np.concatenate([np.asarray(sample).reshape(-1) for sample in samples]) if samples else np.empty(0)
        finite = values[np.isfinite(values)]
        if finite.size < BLACK_LEVEL_FALLBACK_MIN_SAMPLES:
            levels.append(None)
            continue
        codes, counts = np.unique(finite.astype("int64", copy=False), return_counts=True)
        modal_index = int(np.argmax(counts))
        if counts[modal_index] / finite.size < BLACK_LEVEL_FALLBACK_MIN_MODAL_FRACTION:
            levels.append(None)
            continue
        levels.append(float(codes[modal_index]))
    return tuple(levels)


def describe_cfa_planes(
    frame: RawMosaicFrame,
    *,
    minimum_camera_white_to_global_ratio: float,
) -> list[dict[str, Any]]:
    pattern = np.asarray(frame.raw_pattern)
    if pattern.shape != (2, 2):
        raise ValueError(f"only 2x2 Bayer CFA patterns are supported, got {pattern.shape}")
    if frame.mosaic.ndim != 2:
        raise ValueError("raw mosaic must be a two-dimensional array")
    if not 0.0 <= minimum_camera_white_to_global_ratio <= 1.0:
        raise ValueError("minimum_camera_white_to_global_ratio must be between 0 and 1")

    green_count = 0
    by_label: dict[str, dict[str, Any]] = {}
    pattern_labels: list[list[str]] = [[], []]
    for row_offset in range(2):
        for column_offset in range(2):
            color_index = int(pattern[row_offset, column_offset])
            if color_index < 0 or color_index >= len(frame.color_desc):
                raise ValueError(
                    f"CFA color index {color_index} is outside color_desc {frame.color_desc!r}"
                )
            color_code = frame.color_desc[color_index].upper()
            if color_code == "G":
                green_count += 1
                label = f"G{green_count}"
            elif color_code in {"R", "B"}:
                label = color_code
            else:
                raise ValueError(f"unsupported Bayer color code {color_code!r}")
            if label in by_label:
                raise ValueError(f"Bayer pattern contains duplicate {label} plane")
            if color_index >= len(frame.black_levels):
                raise ValueError(f"missing black level for CFA color index {color_index}")

            samples = np.asarray(frame.mosaic[row_offset::2, column_offset::2], dtype="float64")
            finite_samples = samples[np.isfinite(samples)]
            observed_max = float(finite_samples.max()) if finite_samples.size else None
            black_level = float(frame.black_levels[color_index])
            black_level_sources = frame.metadata.get("black_level_source_per_channel")
            black_level_source = (
                str(black_level_sources[color_index])
                if isinstance(black_level_sources, Sequence) and color_index < len(black_level_sources)
                else "frame_black_levels"
            )
            camera_white = _channel_value(frame.camera_white_levels, color_index)
            effective_white, white_source = _resolve_white_level(
                camera_white=camera_white,
                global_white=float(frame.white_level),
                black_level=black_level,
                observed_max=observed_max,
                minimum_camera_white_to_global_ratio=minimum_camera_white_to_global_ratio,
            )
            by_label[label] = {
                "label": label,
                "color_code": color_code,
                "color_index": color_index,
                "row_offset": row_offset,
                "column_offset": column_offset,
                "black_level": black_level,
                "black_level_source": black_level_source,
                "camera_white_level": camera_white,
                "global_white_level": float(frame.white_level),
                "effective_white_level": effective_white,
                "effective_white_level_source": white_source,
                "observed_max": observed_max,
            }
            pattern_labels[row_offset].append(label)

    if set(by_label) != set(PLANE_ORDER):
        raise ValueError(
            "CFA must contain exactly one red, two green, and one blue cell; "
            f"resolved {sorted(by_label)}"
        )
    descriptors = [by_label[label] for label in PLANE_ORDER]
    for descriptor in descriptors:
        descriptor["pattern_labels"] = pattern_labels
    return descriptors


def load_mapped_location_regions(
    path: str | Path,
    *,
    target_shape: tuple[int, int],
    block_indices: str | tuple[int, ...] = "all",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    location_path = Path(path)
    document = json.loads(location_path.read_text(encoding="utf-8"))
    source_image = document.get("image")
    if isinstance(source_image, Mapping):
        source_width = _positive_float(source_image.get("width"), "location image width")
        source_height = _positive_float(source_image.get("height"), "location image height")
    else:
        source_height, source_width = target_shape
    regions = location_regions.load_location_regions(location_path, block_indices)
    mapped = map_regions_to_mosaic(
        regions,
        source_size=(source_height, source_width),
        target_shape=target_shape,
    )
    return mapped, {
        "path": str(location_path),
        "sha256": _sha256(location_path),
        "source_image": {"width": source_width, "height": source_height},
        "target_mosaic": {"width": int(target_shape[1]), "height": int(target_shape[0])},
        "scale": {
            "x": float(target_shape[1]) / source_width,
            "y": float(target_shape[0]) / source_height,
        },
    }


def map_regions_to_mosaic(
    regions: Sequence[Mapping[str, Any]],
    *,
    source_size: tuple[float, float],
    target_shape: tuple[int, int],
) -> list[dict[str, Any]]:
    source_height = _positive_float(source_size[0], "source height")
    source_width = _positive_float(source_size[1], "source width")
    target_height = int(target_shape[0])
    target_width = int(target_shape[1])
    if target_height <= 0 or target_width <= 0:
        raise ValueError("target mosaic dimensions must be positive")
    x_scale = target_width / source_width
    y_scale = target_height / source_height
    mapped: list[dict[str, Any]] = []
    for region in regions:
        item = copy.deepcopy(dict(region))
        region_type = item.get("type")
        if region_type == "polygon":
            item["points"] = [
                (float(point[0]) * x_scale, float(point[1]) * y_scale)
                for point in item["points"]
            ]
        elif region_type == "roi":
            item["x"] = int(round(float(item["x"]) * x_scale))
            item["y"] = int(round(float(item["y"]) * y_scale))
            item["width"] = max(1, int(round(float(item["width"]) * x_scale)))
            item["height"] = max(1, int(round(float(item["height"]) * y_scale)))
        elif region_type != "full":
            raise ValueError(f"unsupported region type: {region_type}")
        mapped.append(item)
    return mapped


def analyze_mosaic_patches(
    frame: RawMosaicFrame,
    *,
    regions: Sequence[Mapping[str, Any]],
    exposure_seconds: float,
    observer_config: Mapping[str, Any],
    combine_green: bool | None = None,
) -> dict[str, Any]:
    _validate_observer_config(observer_config)
    exposure = _positive_float(exposure_seconds, "exposure_seconds")
    statistics_config = _mapping_section(observer_config, "statistics")
    quality_config = _mapping_section(observer_config, "quality_thresholds")
    raw_metadata_config = _mapping_section(observer_config, "raw_metadata")
    patch_policy = _mapping_section(observer_config, "patch_policy")
    combine_green_value = (
        bool(statistics_config["combine_green"]) if combine_green is None else bool(combine_green)
    )
    descriptors = describe_cfa_planes(
        frame,
        minimum_camera_white_to_global_ratio=float(
            raw_metadata_config["minimum_camera_white_to_global_ratio"]
        ),
    )
    diagnostic_roles = {str(role).lower() for role in patch_policy["diagnostic_only_roles"]}
    patches: list[dict[str, Any]] = []
    for region in regions:
        view, region_mask, row_start, column_start = _region_window(frame.mosaic, region)
        patch_metadata = region.get("patch")
        roles = {
            str(role).lower()
            for role in (patch_metadata.get("roles", []) if isinstance(patch_metadata, Mapping) else [])
        }
        diagnostic_only = bool(roles & diagnostic_roles)
        planes: dict[str, dict[str, Any]] = {}
        for descriptor in descriptors:
            values = _extract_plane_values(
                view,
                region_mask,
                row_start=row_start,
                column_start=column_start,
                row_offset=int(descriptor["row_offset"]),
                column_offset=int(descriptor["column_offset"]),
            )
            planes[str(descriptor["label"])] = summarize_plane(
                values,
                descriptor=descriptor,
                exposure_seconds=exposure,
                statistics_config=statistics_config,
                quality_config=quality_config,
            )
        patch = {
            "name": str(region["name"]),
            "type": str(region["type"]),
            "index": int(region["index"]) if "index" in region else None,
            "patch": copy.deepcopy(patch_metadata) if isinstance(patch_metadata, Mapping) else None,
            "optimization_eligible": not diagnostic_only,
            "planes": planes,
        }
        _refresh_patch_quality(patch)
        if combine_green_value:
            patch["combined_green"] = combine_green_planes(planes)
        patches.append(patch)

    report = {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "exposure_seconds": exposure,
        "observer_config": copy.deepcopy(dict(observer_config)),
        "mosaic": {
            "shape": [int(value) for value in frame.mosaic.shape],
            "dtype": str(frame.mosaic.dtype),
            "plane_order": list(PLANE_ORDER),
            "pattern_labels": descriptors[0]["pattern_labels"],
            "planes": [
                {key: value for key, value in descriptor.items() if key != "pattern_labels"}
                for descriptor in descriptors
            ],
        },
        "raw_metadata": copy.deepcopy(frame.metadata),
        "combined_green_enabled": combine_green_value,
        "patches": patches,
    }
    report["quality"] = summarize_report_quality(patches)
    return report


def meter_mosaic_exposure(
    frame: RawMosaicFrame,
    *,
    regions: Sequence[Mapping[str, Any]],
    observer_config: Mapping[str, Any],
    target_scale: int = 65535,
) -> RawExposureMeterResult:
    """Meter mapped native-Bayer regions without demosaic or persistent decodes."""

    if target_scale <= 0:
        raise ValueError("target_scale must be positive")
    report = analyze_mosaic_patches(
        frame,
        regions=regions,
        exposure_seconds=1.0,
        observer_config=observer_config,
        combine_green=False,
    )
    plane_max: dict[str, float | None] = {label: None for label in PLANE_ORDER}
    clipped_values: list[tuple[float, int]] = []
    low_signal_values: list[tuple[float, int]] = []
    for patch in report["patches"]:
        if not patch["optimization_eligible"]:
            continue
        for label, plane in patch["planes"].items():
            maximum = plane["statistics"]["black_corrected_normalized"]["maximum"]
            if maximum is not None:
                current = plane_max[label]
                plane_max[label] = float(maximum) if current is None else max(float(current), float(maximum))
            valid_count = int(plane["metrics"]["valid_pixel_count"])
            for values, metric_name in (
                (clipped_values, "clipped_fraction"),
                (low_signal_values, "near_noise_floor_fraction"),
            ):
                metric = plane["metrics"][metric_name]
                if metric is not None and valid_count > 0:
                    values.append((float(metric), valid_count))
    finite_maxima = [value for value in plane_max.values() if value is not None]
    normalized_max = min(1.0, max(0.0, max(finite_maxima, default=0.0)))
    return RawExposureMeterResult(
        exposure_metric=int(round(normalized_max * target_scale)),
        raw_visible_max=_raw_visible_max(frame.mosaic),
        plane_max=plane_max,
        clipped_fraction=_weighted_fraction(clipped_values),
        low_signal_fraction=_weighted_fraction(low_signal_values),
        quality_status=str(report["quality"]["status"]),
    )


def meter_raw_exposure(
    raw_file: str | Path,
    *,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    target_scale: int = 65535,
) -> RawExposureMeterResult:
    """Load a CR3 and meter its saved chart regions directly in the Bayer mosaic."""

    frame = load_raw_mosaic(raw_file)
    regions, _ = load_mapped_location_regions(
        location_config_path,
        target_shape=(int(frame.mosaic.shape[0]), int(frame.mosaic.shape[1])),
    )
    return meter_mosaic_exposure(
        frame,
        regions=regions,
        observer_config=load_observer_config(observer_config_path),
        target_scale=target_scale,
    )


def summarize_plane(
    values: np.ndarray,
    *,
    descriptor: Mapping[str, Any],
    exposure_seconds: float,
    statistics_config: Mapping[str, Any],
    quality_config: Mapping[str, Any],
) -> dict[str, Any]:
    selected = np.asarray(values, dtype="float64").reshape(-1)
    finite_mask = np.isfinite(selected)
    finite = selected[finite_mask]
    selected_count = int(selected.size)
    valid_count = int(finite.size)
    nonfinite_fraction = 0.0 if selected_count == 0 else 1.0 - valid_count / selected_count
    black_level = float(descriptor["black_level"])
    white_level = float(descriptor["effective_white_level"])
    sensor_range = white_level - black_level
    if sensor_range <= 0:
        raise ValueError(f"{descriptor['label']} white level must exceed its black level")

    trim_fraction = float(statistics_config["trim_fraction"])
    noise_margin = float(statistics_config["noise_floor_margin_normalized"]) * sensor_range
    clipping_margin = float(statistics_config["clipping_margin_normalized"]) * sensor_range
    if valid_count:
        normalized = (finite - black_level) / sensor_range
        raw_stats = _distribution_statistics(finite, trim_fraction)
        normalized_stats = _distribution_statistics(normalized, trim_fraction)
        normalized_per_second = _scale_statistics(normalized_stats, exposure_seconds)
        clipped_fraction = float(np.mean(finite >= white_level - clipping_margin))
        near_noise_fraction = float(np.mean(finite <= black_level + noise_margin))
        below_black_fraction = float(np.mean(finite < black_level))
    else:
        raw_stats = _empty_statistics()
        normalized_stats = _empty_statistics()
        normalized_per_second = _empty_statistics()
        clipped_fraction = None
        near_noise_fraction = None
        below_black_fraction = None

    metrics = {
        "selected_pixel_count": selected_count,
        "valid_pixel_count": valid_count,
        "nonfinite_fraction": nonfinite_fraction,
        "clipped_fraction": clipped_fraction,
        "near_noise_floor_fraction": near_noise_fraction,
        "below_black_fraction": below_black_fraction,
    }
    return {
        "label": str(descriptor["label"]),
        "cfa": {
            key: copy.deepcopy(descriptor[key])
            for key in (
                "color_code",
                "color_index",
                "row_offset",
                "column_offset",
                "black_level",
                "black_level_source",
                "camera_white_level",
                "global_white_level",
                "effective_white_level",
                "effective_white_level_source",
                "observed_max",
            )
        },
        "metrics": metrics,
        "statistics": {
            "raw_code": raw_stats,
            "black_corrected_normalized": normalized_stats,
            "normalized_per_second": normalized_per_second,
        },
        "quality": evaluate_plane_quality(metrics, quality_config),
    }


def evaluate_plane_quality(
    metrics: Mapping[str, Any],
    quality_config: Mapping[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    pending_thresholds: list[str] = []
    valid_count = int(metrics["valid_pixel_count"])
    if valid_count < int(quality_config["minimum_valid_pixels_per_plane"]):
        failures.append("insufficient_valid_pixels")

    checks = (
        ("maximum_nonfinite_fraction", "nonfinite_fraction", "nonfinite_fraction_exceeded"),
        ("maximum_clipped_fraction", "clipped_fraction", "clipped_fraction_exceeded"),
        (
            "maximum_near_noise_floor_fraction",
            "near_noise_floor_fraction",
            "near_noise_floor_fraction_exceeded",
        ),
    )
    for threshold_name, metric_name, failure_name in checks:
        threshold = quality_config[threshold_name]
        metric = metrics[metric_name]
        if threshold is None:
            pending_thresholds.append(threshold_name)
        elif metric is not None and float(metric) > float(threshold):
            failures.append(failure_name)

    if float(metrics["nonfinite_fraction"]) > 0:
        warnings.append("nonfinite_pixels_present")
    if metrics["clipped_fraction"] is not None and float(metrics["clipped_fraction"]) > 0:
        warnings.append("clipped_pixels_present")
    if (
        metrics["near_noise_floor_fraction"] is not None
        and float(metrics["near_noise_floor_fraction"]) > 0
    ):
        warnings.append("near_noise_floor_pixels_present")

    if failures:
        status = "rejected"
        accepted: bool | None = False
    elif pending_thresholds:
        status = "pending_thresholds"
        accepted = None
    else:
        status = "accepted"
        accepted = True
    return {
        "status": status,
        "accepted": accepted,
        "failures": failures,
        "warnings": warnings,
        "pending_thresholds": pending_thresholds,
        "thresholds": copy.deepcopy(dict(quality_config)),
    }


def combine_green_planes(planes: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    g1 = planes["G1"]
    g2 = planes["G2"]
    g1_stats = g1["statistics"]["normalized_per_second"]
    g2_stats = g2["statistics"]["normalized_per_second"]
    combined_stats = {
        key: _mean_optional(g1_stats[key], g2_stats[key])
        for key in ("mean", "median", "trimmed_mean", "mad")
    }
    g1_variance = g1_stats["variance"]
    g2_variance = g2_stats["variance"]
    combined_stats["variance"] = (
        None
        if g1_variance is None or g2_variance is None
        else (float(g1_variance) + float(g2_variance)) / 4.0
    )
    g1_center = g1_stats["trimmed_mean"]
    g2_center = g2_stats["trimmed_mean"]
    ratio = (
        None
        if g1_center is None or g2_center in (None, 0)
        else float(g1_center) / float(g2_center)
    )
    quality_statuses = {str(g1["quality"]["status"]), str(g2["quality"]["status"])}
    if "rejected" in quality_statuses:
        quality_status = "rejected"
    elif "pending_thresholds" in quality_statuses:
        quality_status = "pending_thresholds"
    else:
        quality_status = "accepted"
    result: dict[str, Any] = {
        "label": "G",
        "method": "arithmetic_mean_of_g1_g2_plane_statistics",
        "normalized_per_second": combined_stats,
        "g1_to_g2_trimmed_mean_ratio": ratio,
        "quality_status": quality_status,
    }
    if "ambient_subtracted" in g1 and "ambient_subtracted" in g2:
        result["ambient_subtracted"] = {
            key: _mean_optional(g1["ambient_subtracted"].get(key), g2["ambient_subtracted"].get(key))
            for key in ("mean_per_second", "median_per_second", "trimmed_mean_per_second")
        }
    return result


def apply_ambient_subtraction(
    signal_report: Mapping[str, Any],
    ambient_report: Mapping[str, Any],
) -> dict[str, Any]:
    result = copy.deepcopy(dict(signal_report))
    ambient_by_name = {str(patch["name"]): patch for patch in ambient_report["patches"]}
    for patch in result["patches"]:
        ambient_patch = ambient_by_name.get(str(patch["name"]))
        if ambient_patch is None:
            raise ValueError(f"ambient report is missing patch {patch['name']}")
        for label in PLANE_ORDER:
            signal_plane = patch["planes"][label]
            ambient_plane = ambient_patch["planes"][label]
            signal_stats = signal_plane["statistics"]["normalized_per_second"]
            ambient_stats = ambient_plane["statistics"]["normalized_per_second"]
            subtraction = {
                f"{key}_per_second": _subtract_optional(signal_stats[key], ambient_stats[key])
                for key in ("mean", "median", "trimmed_mean")
            }
            subtraction["combined_mad_per_second"] = _hypot_optional(
                signal_stats["mad"], ambient_stats["mad"]
            )
            subtraction["combined_variance_per_second_squared"] = _sum_optional(
                signal_stats["variance"], ambient_stats["variance"]
            )
            signal_plane["ambient_subtracted"] = subtraction
        if result["combined_green_enabled"]:
            patch["combined_green"] = combine_green_planes(patch["planes"])
    result["ambient_reference"] = copy.deepcopy(dict(ambient_report))
    return result


def summarize_report_quality(patches: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    optimization_planes = [
        plane
        for patch in patches
        if bool(patch["optimization_eligible"])
        for plane in patch["planes"].values()
    ]
    statuses = [str(plane["quality"]["status"]) for plane in optimization_planes]
    if not statuses:
        status = "no_optimization_patches"
        accepted: bool | None = False
    elif any(status == "rejected" for status in statuses):
        status = "rejected"
        accepted = False
    elif any(status == "pending_thresholds" for status in statuses):
        status = "pending_thresholds"
        accepted = None
    else:
        status = "accepted"
        accepted = True
    return {
        "status": status,
        "accepted_for_optimization": accepted,
        "optimization_patch_count": sum(bool(patch["optimization_eligible"]) for patch in patches),
        "diagnostic_patch_count": sum(not bool(patch["optimization_eligible"]) for patch in patches),
        "accepted_plane_count": statuses.count("accepted"),
        "pending_plane_count": statuses.count("pending_thresholds"),
        "rejected_plane_count": statuses.count("rejected"),
    }


def analyze_raw_file(
    raw_file: str | Path,
    *,
    exposure_seconds: float,
    location_config_path: str | Path = DEFAULT_LOCATION_CONFIG,
    observer_config_path: str | Path = DEFAULT_OBSERVER_CONFIG,
    ambient_raw_file: str | Path | None = None,
    ambient_exposure_seconds: float | None = None,
    combine_green: bool | None = None,
) -> dict[str, Any]:
    observer_path = Path(observer_config_path)
    observer_config = load_observer_config(observer_path)
    frame = load_raw_mosaic(raw_file)
    regions, location_metadata = load_mapped_location_regions(
        location_config_path,
        target_shape=(int(frame.mosaic.shape[0]), int(frame.mosaic.shape[1])),
    )
    report = analyze_mosaic_patches(
        frame,
        regions=regions,
        exposure_seconds=exposure_seconds,
        observer_config=observer_config,
        combine_green=combine_green,
    )
    report["created_at"] = datetime.now(timezone.utc).isoformat()
    report["source"] = {
        "path": str(frame.source_file),
        "sha256": _sha256(frame.source_file),
    }
    report["location_config"] = location_metadata
    report["observer_config_source"] = {
        "path": str(observer_path),
        "sha256": _sha256(observer_path),
    }

    if ambient_raw_file is not None:
        if ambient_exposure_seconds is None:
            raise ValueError("ambient_exposure_seconds is required with ambient_raw_file")
        ambient_frame = load_raw_mosaic(ambient_raw_file)
        ambient_regions, _ = load_mapped_location_regions(
            location_config_path,
            target_shape=(int(ambient_frame.mosaic.shape[0]), int(ambient_frame.mosaic.shape[1])),
        )
        ambient_report = analyze_mosaic_patches(
            ambient_frame,
            regions=ambient_regions,
            exposure_seconds=ambient_exposure_seconds,
            observer_config=observer_config,
            combine_green=combine_green,
        )
        ambient_report["source"] = {
            "path": str(ambient_frame.source_file),
            "sha256": _sha256(ambient_frame.source_file),
        }
        report = apply_ambient_subtraction(report, ambient_report)
    return report


def write_report(path: str | Path, report: Mapping[str, Any]) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_exposure_seconds(value: str) -> float:
    text = value.strip().lower()
    if text == "bulb":
        raise argparse.ArgumentTypeError("bulb exposure cannot be normalized")
    try:
        seconds = float(Fraction(text))
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError(f"invalid exposure value: {value}") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("exposure must be positive and finite")
    return seconds


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure native Bayer R/G1/G2/B patch statistics from an existing RAW file."
    )
    parser.add_argument("raw_file", type=Path)
    parser.add_argument("--exposure", required=True, type=parse_exposure_seconds, help="Seconds or fraction, e.g. 1/30.")
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--ambient-raw", type=Path)
    parser.add_argument("--ambient-exposure", type=parse_exposure_seconds)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--combined-green",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Override the config and include or omit G=(G1+G2)/2.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.ambient_raw is None and args.ambient_exposure is not None:
        raise ValueError("--ambient-exposure requires --ambient-raw")
    report = analyze_raw_file(
        args.raw_file,
        exposure_seconds=args.exposure,
        location_config_path=args.location_config,
        observer_config_path=args.observer_config,
        ambient_raw_file=args.ambient_raw,
        ambient_exposure_seconds=args.ambient_exposure,
        combine_green=args.combined_green,
    )
    output = args.output
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output = DEFAULT_OUTPUT_ROOT / timestamp / "patch-statistics.json"
    print(write_report(output, report))
    return 0


def _validate_observer_config(config: Mapping[str, Any]) -> None:
    statistics = _mapping_section(config, "statistics")
    quality = _mapping_section(config, "quality_thresholds")
    raw_metadata = _mapping_section(config, "raw_metadata")
    patch_policy = _mapping_section(config, "patch_policy")
    trim_fraction = float(statistics["trim_fraction"])
    if not 0.0 <= trim_fraction < 0.5:
        raise ValueError("statistics.trim_fraction must be in [0, 0.5)")
    for name in ("noise_floor_margin_normalized", "clipping_margin_normalized"):
        value = float(statistics[name])
        if not 0.0 <= value < 1.0:
            raise ValueError(f"statistics.{name} must be in [0, 1)")
    if not isinstance(statistics["combine_green"], bool):
        raise ValueError("statistics.combine_green must be boolean")
    if int(quality["minimum_valid_pixels_per_plane"]) < 1:
        raise ValueError("quality_thresholds.minimum_valid_pixels_per_plane must be positive")
    for name in (
        "maximum_nonfinite_fraction",
        "maximum_clipped_fraction",
        "maximum_near_noise_floor_fraction",
    ):
        value = quality[name]
        if value is not None and not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"quality_thresholds.{name} must be null or in [0, 1]")
    ratio = float(raw_metadata["minimum_camera_white_to_global_ratio"])
    if not 0.0 <= ratio <= 1.0:
        raise ValueError("raw_metadata.minimum_camera_white_to_global_ratio must be in [0, 1]")
    roles = patch_policy["diagnostic_only_roles"]
    if not isinstance(roles, list) or not all(isinstance(role, str) for role in roles):
        raise ValueError("patch_policy.diagnostic_only_roles must be an array of strings")


def _mapping_section(config: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = config.get(name)
    if not isinstance(value, Mapping):
        raise ValueError(f"raw observer config {name} must be an object")
    return value


def _resolve_white_level(
    *,
    camera_white: float | None,
    global_white: float,
    black_level: float,
    observed_max: float | None,
    minimum_camera_white_to_global_ratio: float,
) -> tuple[float, str]:
    if not math.isfinite(global_white) or global_white <= black_level:
        raise ValueError("global RAW white level must be finite and exceed black level")
    camera_valid = (
        camera_white is not None
        and math.isfinite(camera_white)
        and camera_white > black_level
        and camera_white >= global_white * minimum_camera_white_to_global_ratio
        and (observed_max is None or camera_white >= observed_max)
    )
    if camera_valid:
        return float(camera_white), "camera_white_level_per_channel"
    return global_white, "global_white_level_fallback"


def _region_window(
    mosaic: np.ndarray,
    region: Mapping[str, Any],
) -> tuple[np.ndarray, np.ndarray | None, int, int]:
    height, width = mosaic.shape
    region_type = region.get("type")
    if region_type == "full":
        return mosaic, None, 0, 0
    if region_type == "roi":
        x = int(region["x"])
        y = int(region["y"])
        roi_width = int(region["width"])
        roi_height = int(region["height"])
        if x < 0 or y < 0 or roi_width <= 0 or roi_height <= 0:
            raise ValueError(f"ROI {region['name']} has invalid bounds")
        if x + roi_width > width or y + roi_height > height:
            raise ValueError(f"ROI {region['name']} exceeds mosaic bounds")
        return mosaic[y : y + roi_height, x : x + roi_width], None, y, x
    if region_type != "polygon":
        raise ValueError(f"unsupported region type: {region_type}")

    points = [(float(point[0]), float(point[1])) for point in region["points"]]
    if len(points) < 3 or not all(math.isfinite(value) for point in points for value in point):
        raise ValueError(f"polygon {region['name']} must contain at least three finite points")
    if any(x < 0 or x > width or y < 0 or y > height for x, y in points):
        raise ValueError(f"polygon {region['name']} exceeds mosaic bounds")
    min_x = max(0, int(math.floor(min(x for x, _ in points))))
    max_x = min(width, int(math.ceil(max(x for x, _ in points))))
    min_y = max(0, int(math.floor(min(y for _, y in points))))
    max_y = min(height, int(math.ceil(max(y for _, y in points))))
    if max_x <= min_x or max_y <= min_y:
        raise ValueError(f"polygon {region['name']} selected no pixels")
    yy, xx = np.mgrid[min_y:max_y, min_x:max_x]
    px = xx.astype("float64") + 0.5
    py = yy.astype("float64") + 0.5
    inside = np.zeros(px.shape, dtype=bool)
    for index, (x1, y1) in enumerate(points):
        x2, y2 = points[(index + 1) % len(points)]
        crosses = ((y1 > py) != (y2 > py)) & (
            px < (x2 - x1) * (py - y1) / ((y2 - y1) or 1e-12) + x1
        )
        inside ^= crosses
    if not bool(inside.any()):
        raise ValueError(f"polygon {region['name']} selected no pixels")
    return mosaic[min_y:max_y, min_x:max_x], inside, min_y, min_x


def _extract_plane_values(
    view: np.ndarray,
    region_mask: np.ndarray | None,
    *,
    row_start: int,
    column_start: int,
    row_offset: int,
    column_offset: int,
) -> np.ndarray:
    rows = np.arange(row_start, row_start + view.shape[0])[:, None]
    columns = np.arange(column_start, column_start + view.shape[1])[None, :]
    mask = ((rows % 2) == row_offset) & ((columns % 2) == column_offset)
    if region_mask is not None:
        mask &= region_mask
    return view[mask]


def _distribution_statistics(values: np.ndarray, trim_fraction: float) -> dict[str, float | None]:
    if values.size == 0:
        return _empty_statistics()
    ordered = np.sort(np.asarray(values, dtype="float64"))
    trim_count = int(math.floor(ordered.size * trim_fraction))
    trimmed = ordered[trim_count : ordered.size - trim_count] if trim_count else ordered
    median = float(np.median(ordered))
    return {
        "minimum": float(np.min(ordered)),
        "maximum": float(np.max(ordered)),
        "mean": float(np.mean(ordered)),
        "median": median,
        "trimmed_mean": float(np.mean(trimmed)),
        "mad": float(np.median(np.abs(ordered - median))),
        "variance": float(np.var(ordered)),
    }


def _empty_statistics() -> dict[str, None]:
    return {key: None for key in ("minimum", "maximum", "mean", "median", "trimmed_mean", "mad", "variance")}


def _scale_statistics(statistics: Mapping[str, float | None], exposure_seconds: float) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for key, value in statistics.items():
        if value is None:
            result[key] = None
        elif key == "variance":
            result[key] = float(value) / (exposure_seconds * exposure_seconds)
        else:
            result[key] = float(value) / exposure_seconds
    return result


def _refresh_patch_quality(patch: dict[str, Any]) -> None:
    statuses = [str(plane["quality"]["status"]) for plane in patch["planes"].values()]
    if not patch["optimization_eligible"]:
        patch["quality_status"] = "diagnostic_only"
    elif "rejected" in statuses:
        patch["quality_status"] = "rejected"
    elif "pending_thresholds" in statuses:
        patch["quality_status"] = "pending_thresholds"
    else:
        patch["quality_status"] = "accepted"


def _weighted_fraction(values: Sequence[tuple[float, int]]) -> float | None:
    total = sum(weight for _, weight in values)
    return None if total == 0 else sum(value * weight for value, weight in values) / total


def _raw_visible_max(mosaic: np.ndarray) -> int | None:
    finite = np.asarray(mosaic, dtype="float64")[np.isfinite(mosaic)]
    return None if finite.size == 0 else int(np.max(finite))


def _channel_value(values: tuple[float, ...] | None, index: int) -> float | None:
    if values is None or index >= len(values):
        return None
    return float(values[index])


def _positive_float(value: Any, name: str) -> float:
    try:
        resolved = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be positive and finite") from exc
    if not math.isfinite(resolved) or resolved <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return resolved


def _mean_optional(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return (float(left) + float(right)) / 2.0


def _subtract_optional(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def _sum_optional(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) + float(right)


def _hypot_optional(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return math.hypot(float(left), float(right))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
