from __future__ import annotations

from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import FrozenHsiUncertaintyEvaluator
from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    HsiPolicyV2,
    WAITING_STATUS,
    conservative_class_variance,
    local_tangent_evaluate,
    plane_block_regularize,
)
from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import collect_patch_plane_features


GROUP_ORDER = ("hue", "sat", "shape")
V2_GROUP_ORDER = ("coordinate", "rendering")
CHANNELS = ("cw", "ww", "r", "g", "b")
P7_RESULT_STATUSES = frozenset({
    "faithful",
    "unconfirmed",
    "measurement_unreachable",
    "uncertainty_unresolved",
    "solver_budget_exhausted",
    "reference_drift",
    "boundary_bracketed_at_full_scale",
})


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
    uncertainty_evaluator: FrozenHsiUncertaintyEvaluator,
    max_code: int = 4095,
) -> dict[str, Any]:
    coordinate = manifold.coordinate(candidate_features, target_hue=target_hue, target_sat=target_sat)
    joint = uncertainty_evaluator.evaluate(
        manifold,
        candidate_features,
        target_hue=target_hue,
        target_sat=target_sat,
    )

    feature_ids = coordinate.feature_ids
    target = manifold.target_at(target_hue, target_sat)
    candidate = _unit([candidate_features[feature] for feature in feature_ids])
    target_values = _unit([target.features[feature] for feature in feature_ids])
    diagonal = np.maximum(np.asarray(joint["diagonal_variance"], dtype=float), 1e-12)
    shape_vector = (candidate - target_values) / np.sqrt(diagonal)
    scales = np.maximum(np.asarray(joint["component_scales"], dtype=float), 1e-12)
    guarded_limit = max(float(joint["guarded_acceptance_limit"]), 1e-12)
    if float(target_sat) == 0.0:
        hue_normalized = 0.0
        sat_normalized = coordinate.sat_error_percent / scales[0] / guarded_limit
        orthogonal_normalized = coordinate.orthogonal_residual / scales[1] / guarded_limit
        hue_scale = None
        sat_scale = float(scales[0])
        orthogonal_scale = float(scales[1])
    else:
        hue_normalized = coordinate.hue_error_degrees / scales[0] / guarded_limit
        sat_normalized = coordinate.sat_error_percent / scales[1] / guarded_limit
        orthogonal_normalized = coordinate.orthogonal_residual / scales[2] / guarded_limit
        hue_scale = float(scales[0])
        sat_scale = float(scales[1])
        orthogonal_scale = float(scales[2])
    continuity = _command_distance(command, previous_command, max_code=max_code)
    feasible = bool(joint["feasible"])
    objective = {
        "kind": "ray_hsi_joint_uncertainty_lexicographic",
        "feasible": feasible,
        "uncertainty_decision": joint["decision"],
        "uncertainty_artifact_sha256": joint["artifact_sha256"],
        "target_kind": joint["target_kind"],
        "joint_score": joint["joint_score"],
        "joint_output": list(joint["output"]),
        "coverage_limit": joint["coverage_limit"],
        "guarded_acceptance_limit": joint["guarded_acceptance_limit"],
        "hue_error_degrees": None if float(target_sat) == 0.0 else coordinate.hue_error_degrees,
        "hue_defined": float(target_sat) > 0.0,
        "hue_scale_degrees": hue_scale,
        "hue_normalized": hue_normalized,
        "sat_error_percent": coordinate.sat_error_percent,
        "sat_scale_percent": sat_scale,
        "sat_normalized": sat_normalized,
        "orthogonal_residual": coordinate.orthogonal_residual,
        "orthogonal_scale": orthogonal_scale,
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
            "shape": [orthogonal_normalized],
        },
        "objective": objective,
    }


def hsi_objective_sort_key(objective: Mapping[str, Any]) -> tuple[float, ...]:
    if objective.get("kind") == "ray_hsi_policy_v2_lexicographic":
        return _hsi_v2_objective_sort_key(objective)
    hue_excess = 0.0 if not bool(objective.get("hue_defined", True)) else max(
        abs(float(objective["hue_normalized"])) - 1.0, 0.0
    )
    sat_excess = max(abs(float(objective["sat_normalized"])) - 1.0, 0.0)
    return (
        0.0 if bool(objective["feasible"]) else 1.0,
        hue_excess,
        sat_excess,
        float(objective.get("joint_score", float("inf"))),
        float(objective["orthogonal_normalized"]),
        float(objective["shape_normalized_p90"]),
        float(objective["shape_normalized_maximum"]),
        float(objective.get("command_continuity_l1", 0.0)),
    )


def evaluate_hsi_observation_v2(
    manifold: RayHsiManifold,
    candidate_features: Mapping[str, float],
    *,
    target_hue: float,
    target_sat: float,
    repeatability_class: str,
    policy: HsiPolicyV2,
    command: Mapping[str, int] | None = None,
    previous_command: Mapping[str, int] | None = None,
    max_code: int = 4095,
) -> dict[str, Any]:
    artifact = policy.artifact
    feature_ids = tuple(artifact["feature_set"]["ids"])
    repeat_class = artifact["repeatability_policy"]["classes"][repeatability_class]
    strip_variance = conservative_class_variance(
        repeat_class["p1_floor_diagonal_variance"],
        repeat_class.get("targeted_variance"),
        feature_ids,
    )
    ray_variance = np.asarray(
        artifact["match_components"]["ray_repeatability_diagonal_variance"], dtype=float,
    )
    target = manifold.target_at(target_hue, target_sat)
    interpolation_name = "exact_node" if all(
        float(target.interpolation[key]) == 0.0
        for key in ("hue_fraction", "sat_fraction")
    ) else "high_curvature" if (
        float(target_sat) >= 80.0 and (float(target_hue) % 360.0 >= 330.0 or float(target_hue) % 360.0 <= 90.0)
    ) else "regular"
    interpolation = np.asarray(
        artifact["match_components"]["interpolation"][interpolation_name]["diagonal_variance"],
        dtype=float,
    )
    match_variance = plane_block_regularize(ray_variance + strip_variance + interpolation, feature_ids)
    local = local_tangent_evaluate(
        manifold, candidate_features,
        target_hue=target_hue, target_sat=target_sat,
        diagonal_variance=match_variance,
        condition_limit=float(artifact["coordinate_policy"]["condition_limit"]),
    )
    continuity = _command_distance(command, previous_command, max_code=max_code)
    if local["status"] != "evaluated":
        objective = {
            "kind": "ray_hsi_policy_v2_lexicographic",
            "feasible": False,
            "hsi_coordinate_equivalent": "uncertainty_unresolved",
            "observer_equivalent": "not_evaluated",
            "color_rendering_residual": None,
            "uncertainty_decision": "uncertainty_unresolved",
            "command_continuity_l1": continuity,
            "coordinate": local,
        }
        return {"residuals": {"coordinate": [float("inf")], "rendering": [float("inf")]}, "objective": objective}

    kind = _v2_target_kind(target_sat, interpolation_name)
    region_key = f"{kind}:{repeatability_class}"
    coordinate_limits = artifact["coordinate_policy"].get("formal_limits") or {}
    observer_limits = artifact["observer_policy"].get("formal_limits") or {}
    coordinate_region = coordinate_limits.get(region_key, coordinate_limits.get(kind))
    observer_region = observer_limits.get(region_key, observer_limits.get(kind))
    signed_coordinate = (
        [float(local["sat_error_percent"])] if float(target_sat) == 0.0 else
        [float(local["hue_error_degrees"]), float(local["sat_error_percent"])]
    )
    if coordinate_region is None:
        coordinate_score = None
        coordinate_decision = WAITING_STATUS
        coordinate_residual = signed_coordinate
    else:
        scales = np.asarray(coordinate_region["component_scales"], dtype=float)
        if scales.shape != (len(signed_coordinate),) or np.any(scales <= 0.0):
            raise ValueError("invalid frozen v2 coordinate scales")
        coordinate_residual = (np.asarray(signed_coordinate) / scales).tolist()
        coordinate_score = float(np.linalg.norm(coordinate_residual))
        coordinate_decision = (
            "pass" if coordinate_score <= float(coordinate_region["guarded_limit"])
            else "unresolved" if coordinate_score <= float(coordinate_region["unguarded_limit"])
            else "fail"
        )
    observer_score = float(local["observer_whitened_score"])
    if observer_region is None:
        observer_decision = WAITING_STATUS
    else:
        observer_decision = (
            "pass" if observer_score <= float(observer_region["guarded_limit"])
            else "unresolved" if observer_score <= float(observer_region["unguarded_limit"])
            else "fail"
        )
    rendering = local["color_rendering_residual"]
    rendering_vector = np.asarray(local["directional_orthogonal_residual"], dtype=float) / np.sqrt(match_variance)
    feasible = coordinate_decision == "pass"
    objective = {
        "kind": "ray_hsi_policy_v2_lexicographic",
        "feasible": feasible,
        "policy_artifact_sha256": policy.artifact_sha256,
        "policy_status": artifact["status"],
        "target_kind": kind,
        "target_region_key": region_key,
        "repeatability_class": repeatability_class,
        "coordinate_guarded_limit": None if coordinate_region is None else float(coordinate_region["guarded_limit"]),
        "coordinate_unguarded_limit": None if coordinate_region is None else float(coordinate_region["unguarded_limit"]),
        "hsi_coordinate_equivalent": coordinate_decision,
        "observer_equivalent": observer_decision,
        "color_rendering_residual": rendering,
        "coordinate_guarded_excess": None if coordinate_score is None else max(
            coordinate_score / float(coordinate_region["guarded_limit"]) - 1.0, 0.0,
        ),
        "coordinate_score": coordinate_score,
        "hue_defined": float(target_sat) > 0.0,
        "hue_error_degrees": local.get("hue_error_degrees"),
        "sat_error_percent": float(local["sat_error_percent"]),
        "observer_whitened_score": observer_score,
        "tangent_condition_number": float(local["condition_number"]),
        "command_continuity_l1": continuity,
        "coordinate": local,
    }
    return {
        "residuals": {"coordinate": coordinate_residual, "rendering": rendering_vector.tolist()},
        "objective": objective,
    }


def _hsi_v2_objective_sort_key(objective: Mapping[str, Any]) -> tuple[float, ...]:
    hue = 0.0 if not bool(objective.get("hue_defined")) else abs(float(objective.get("hue_error_degrees", float("inf"))))
    return (
        0.0 if bool(objective.get("feasible")) else 1.0,
        float(objective.get("coordinate_guarded_excess") if objective.get("coordinate_guarded_excess") is not None else float("inf")),
        hue,
        abs(float(objective.get("sat_error_percent", float("inf")))),
        float((objective.get("color_rendering_residual") or {}).get("whitened_score", float("inf"))),
        float(objective.get("command_continuity_l1", 0.0)),
    )


def _v2_target_kind(target_sat: float, interpolation_name: str) -> str:
    if float(target_sat) == 0.0:
        return "sat0_exact_node"
    return f"nonzero_{interpolation_name}"


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
