from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import collect_patch_plane_features


GROUP_ORDER = ("hue", "sat", "shape")
CHANNELS = ("cw", "ww", "r", "g", "b")


class HsiRejectedFeaturesError(ValueError):
    def __init__(self, rejected: Sequence[Mapping[str, Any]], *, weak_signal_only: bool):
        super().__init__(f"{len(rejected)} required HSI observer features were rejected")
        self.rejected = [dict(item) for item in rejected]
        self.weak_signal_only = bool(weak_signal_only)


def required_hsi_features_from_report(
    report: Mapping[str, Any], required_feature_ids: Sequence[str]
) -> dict[str, float]:
    required = tuple(str(value) for value in required_feature_ids)
    if not required or len(set(required)) != len(required):
        raise ValueError("required HSI feature IDs must be unique and non-empty")
    collection = collect_patch_plane_features([report])
    by_id = {str(item["feature_id"]): item for item in collection["observations"]}
    missing = [feature for feature in required if feature not in by_id]
    if missing:
        raise ValueError(f"RAW report is missing required HSI features: {missing}")
    rejected = [
        by_id[feature]
        for feature in required
        if by_id[feature]["status"] != "included"
        or by_id[feature]["quality_status"] != "accepted"
        or by_id[feature]["value"] is None
    ]
    if rejected:
        raise HsiRejectedFeaturesError(
            rejected,
            weak_signal_only=_weak_signal_only(report, rejected),
        )
    return {feature: float(by_id[feature]["value"]) for feature in required}


def evaluate_hsi_observation(
    manifold: RayHsiManifold,
    candidate_features: Mapping[str, float],
    *,
    target_hue: float,
    target_sat: float,
    command: Mapping[str, int] | None = None,
    previous_command: Mapping[str, int] | None = None,
    strip_hue_three_sigma_degrees: float = 0.0,
    strip_sat_three_sigma_percent: float = 0.0,
    strip_shape_three_sigma: float = 0.0,
    max_code: int = 4095,
) -> dict[str, Any]:
    coordinate = manifold.coordinate(candidate_features, target_hue=target_hue, target_sat=target_sat)
    hue_tolerance = math.hypot(coordinate.hue_three_sigma_degrees, float(strip_hue_three_sigma_degrees))
    sat_tolerance = math.hypot(coordinate.sat_three_sigma_percent, float(strip_sat_three_sigma_percent))
    shape_tolerance = math.hypot(manifold.repeatability_three_sigma, float(strip_shape_three_sigma))
    if min(hue_tolerance, sat_tolerance, shape_tolerance) <= 0:
        raise ValueError("HSI observer tolerances must be positive")

    feature_ids = coordinate.feature_ids
    target = manifold.target_at(target_hue, target_sat)
    candidate = _unit([candidate_features[feature] for feature in feature_ids])
    target_values = _unit([target.features[feature] for feature in feature_ids])
    shape_vector = (candidate - target_values) / shape_tolerance
    hue_normalized = 0.0 if float(target_sat) == 0.0 else coordinate.hue_error_degrees / hue_tolerance
    sat_normalized = coordinate.sat_error_percent / sat_tolerance
    orthogonal_normalized = coordinate.orthogonal_residual / shape_tolerance
    continuity = _command_distance(command, previous_command, max_code=max_code)
    feasible = bool(
        abs(hue_normalized) <= 1.0
        and abs(sat_normalized) <= 1.0
        and orthogonal_normalized <= 1.0
    )
    objective = {
        "kind": "ray_hsi_lexicographic",
        "feasible": feasible,
        "hue_error_degrees": None if float(target_sat) == 0.0 else coordinate.hue_error_degrees,
        "hue_defined": float(target_sat) > 0.0,
        "hue_tolerance_degrees": hue_tolerance,
        "hue_normalized": hue_normalized,
        "sat_error_percent": coordinate.sat_error_percent,
        "sat_tolerance_percent": sat_tolerance,
        "sat_normalized": sat_normalized,
        "orthogonal_residual": coordinate.orthogonal_residual,
        "orthogonal_tolerance": shape_tolerance,
        "orthogonal_normalized": orthogonal_normalized,
        "shape_residual": coordinate.shape_residual,
        "shape_normalized_rms": float(np.sqrt(np.mean(shape_vector * shape_vector))),
        "shape_normalized_p90": float(np.quantile(np.abs(shape_vector), 0.9)),
        "shape_normalized_maximum": float(np.max(np.abs(shape_vector))),
        "command_continuity_l1": continuity,
        "coordinate": coordinate.to_jsonable(),
    }
    return {
        "residuals": {
            "hue": [hue_normalized],
            "sat": [sat_normalized],
            "shape": shape_vector.tolist(),
        },
        "objective": objective,
    }


def hsi_objective_sort_key(objective: Mapping[str, Any]) -> tuple[float, ...]:
    hue_excess = max(abs(float(objective["hue_normalized"])) - 1.0, 0.0)
    sat_excess = max(abs(float(objective["sat_normalized"])) - 1.0, 0.0)
    return (
        0.0 if bool(objective["feasible"]) else 1.0,
        hue_excess,
        sat_excess,
        float(objective["orthogonal_normalized"]),
        float(objective["shape_normalized_p90"]),
        float(objective["shape_normalized_maximum"]),
        float(objective.get("command_continuity_l1", 0.0)),
    )


def _command_distance(
    command: Mapping[str, int] | None,
    previous: Mapping[str, int] | None,
    *,
    max_code: int,
    channels: Sequence[str] = CHANNELS,
) -> float:
    if command is None or previous is None:
        return 0.0
    return sum(abs(int(command[channel]) - int(previous[channel])) for channel in channels) / (len(channels) * max_code)


def _unit(values: Sequence[float]) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    norm = float(np.linalg.norm(array))
    if norm <= 0 or not np.isfinite(norm):
        raise ValueError("HSI candidate vector must have positive finite norm")
    return array / norm


def _weak_signal_only(report: Mapping[str, Any], rejected: Sequence[Mapping[str, Any]]) -> bool:
    thresholds = report.get("observer_config", {}).get("quality_thresholds", {})
    try:
        minimum_pixels = int(thresholds["minimum_valid_pixels_per_plane"])
        maximum_nonfinite = float(thresholds["maximum_nonfinite_fraction"])
        maximum_clipped = float(thresholds["maximum_clipped_fraction"])
        maximum_near_noise = float(thresholds["maximum_near_noise_floor_fraction"])
    except (KeyError, TypeError, ValueError):
        return False
    for item in rejected:
        metrics = item["metrics"]
        if item["status"] != "included":
            return False
        if int(metrics["valid_pixel_count"]) < minimum_pixels:
            return False
        if float(metrics["nonfinite_fraction"]) > maximum_nonfinite:
            return False
        if float(metrics["clipped_fraction"]) > maximum_clipped:
            return False
        if float(metrics["near_noise_floor_fraction"]) <= maximum_near_noise:
            return False
    return True
