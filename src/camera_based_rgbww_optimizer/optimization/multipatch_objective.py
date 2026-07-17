from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.measurement import raw_observer_analysis
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common
from camera_based_rgbww_optimizer.optimization.white_lut_feedback import white_point_metrics


PLANE_ORDER = ("R", "G1", "G2", "B")


class RejectedOptimizationFeaturesError(ValueError):
    def __init__(self, rejected: Sequence[Mapping[str, Any]], *, weak_signal_only: bool):
        super().__init__(f"RAW report contains rejected optimization features: {len(rejected)}")
        self.rejected = [dict(item) for item in rejected]
        self.weak_signal_only = bool(weak_signal_only)


def feature_group(feature_id: str) -> tuple[int, str]:
    try:
        block_name, plane = str(feature_id).split("::", 1)
        block_index = int(block_name.removeprefix("block_"))
    except (TypeError, ValueError) as error:
        raise ValueError(f"invalid multipatch feature id: {feature_id!r}") from error
    if plane not in PLANE_ORDER:
        raise ValueError(f"unsupported CFA plane in feature id: {feature_id!r}")
    return block_index, plane


def validate_feature_split(
    feature_order: Sequence[str],
    *,
    neutral_blocks: Sequence[int],
    training_blocks: Sequence[int],
    holdout_blocks: Sequence[int],
) -> dict[str, list[str]]:
    groups = {
        "neutral": {int(value) for value in neutral_blocks},
        "training": {int(value) for value in training_blocks},
        "holdout": {int(value) for value in holdout_blocks},
    }
    if any(not values for values in groups.values()):
        raise ValueError("neutral, training, and holdout block sets must all be non-empty")
    if any(groups[left] & groups[right] for left, right in (("neutral", "training"), ("neutral", "holdout"), ("training", "holdout"))):
        raise ValueError("multipatch block sets must be disjoint")

    split = {name: [] for name in groups}
    seen: dict[int, set[str]] = {}
    for feature in feature_order:
        block, plane = feature_group(feature)
        seen.setdefault(block, set()).add(plane)
        for name, blocks in groups.items():
            if block in blocks:
                split[name].append(str(feature))
                break
    for name, blocks in groups.items():
        missing = sorted(block for block in blocks if seen.get(block) != set(PLANE_ORDER))
        if missing:
            raise ValueError(f"{name} blocks are missing complete R/G1/G2/B features: {missing}")
    return split


def fit_nonnegative_scale(candidate: Any, target: Any, weights: Any | None = None) -> float:
    candidate_array = np.asarray(candidate, dtype="float64")
    target_array = np.asarray(target, dtype="float64")
    if candidate_array.shape != target_array.shape or candidate_array.ndim != 1:
        raise ValueError("candidate and target must be same-length one-dimensional vectors")
    resolved_weights = np.ones_like(candidate_array) if weights is None else np.asarray(weights, dtype="float64")
    if resolved_weights.shape != candidate_array.shape or np.any(resolved_weights < 0):
        raise ValueError("weights must match the vectors and be non-negative")
    denominator = float(np.sum(resolved_weights * candidate_array * candidate_array))
    if denominator <= 0:
        return 0.0
    return max(0.0, float(np.sum(resolved_weights * candidate_array * target_array)) / denominator)


def robust_relative_error(candidate: Any, target: Any, *, scale: float) -> dict[str, float]:
    candidate_array = np.asarray(candidate, dtype="float64")
    target_array = np.asarray(target, dtype="float64")
    if candidate_array.shape != target_array.shape or candidate_array.ndim != 1 or candidate_array.size == 0:
        raise ValueError("candidate and target must be non-empty same-length vectors")
    floor = max(float(np.median(np.abs(target_array))) * 1e-6, 1e-12)
    residual = np.abs(float(scale) * candidate_array - target_array) / np.maximum(np.abs(target_array), floor)
    return {
        "mean": float(np.mean(residual)),
        "p90": float(np.quantile(residual, 0.9)),
        "maximum": float(np.max(residual)),
    }


def neutral_chroma_error(
    candidate_by_feature: Mapping[str, float],
    target_by_feature: Mapping[str, float],
    *,
    neutral_blocks: Sequence[int],
) -> dict[str, Any]:
    errors: list[float] = []
    by_block: dict[str, dict[str, float]] = {}
    for block in neutral_blocks:
        prefix = f"block_{int(block):02d}"
        candidate = np.asarray([candidate_by_feature[f"{prefix}::{plane}"] for plane in PLANE_ORDER], dtype="float64")
        target = np.asarray([target_by_feature[f"{prefix}::{plane}"] for plane in PLANE_ORDER], dtype="float64")
        candidate_green = float(np.mean(candidate[1:3]))
        target_green = float(np.mean(target[1:3]))
        if candidate_green <= 0 or target_green <= 0:
            raise ValueError(f"neutral block {block} has non-positive green response")
        block_errors = np.abs(candidate / candidate_green - target / target_green)
        errors.extend(float(value) for value in block_errors)
        by_block[prefix] = {
            plane: float(block_errors[index]) for index, plane in enumerate(PLANE_ORDER)
        }
    values = np.asarray(errors, dtype="float64")
    return {
        "mean": float(np.mean(values)),
        "p95": float(np.quantile(values, 0.95)),
        "maximum": float(np.max(values)),
        "by_block": by_block,
    }


def evaluate_multipatch_objective(
    candidate_by_feature: Mapping[str, float],
    target_by_feature: Mapping[str, float],
    *,
    feature_split: Mapping[str, Sequence[str]],
    neutral_blocks: Sequence[int],
    neutral_chroma_tolerance: float,
    white_point_comparison: Mapping[str, Any],
    regularization: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    if neutral_chroma_tolerance <= 0:
        raise ValueError("neutral_chroma_tolerance must be positive")
    required = [feature for group in feature_split.values() for feature in group]
    missing = [feature for feature in required if feature not in candidate_by_feature or feature not in target_by_feature]
    if missing:
        raise ValueError(f"missing multipatch features: {missing[:5]}")

    color_features = [*feature_split["training"], *feature_split["holdout"]]
    candidate_color = np.asarray([candidate_by_feature[feature] for feature in color_features], dtype="float64")
    target_color = np.asarray([target_by_feature[feature] for feature in color_features], dtype="float64")
    scale = fit_nonnegative_scale(candidate_color, target_color)
    group_errors = {}
    for name in ("training", "holdout"):
        features = feature_split[name]
        group_errors[name] = robust_relative_error(
            [candidate_by_feature[feature] for feature in features],
            [target_by_feature[feature] for feature in features],
            scale=scale,
        )

    neutral = neutral_chroma_error(
        candidate_by_feature,
        target_by_feature,
        neutral_blocks=neutral_blocks,
    )
    neutral["tolerance"] = float(neutral_chroma_tolerance)
    neutral["within_gate"] = neutral["maximum"] <= float(neutral_chroma_tolerance)
    neutral_violation = max(0.0, neutral["maximum"] / float(neutral_chroma_tolerance) - 1.0)
    white_score = float(white_point_comparison["goal_score"])
    white_within = bool(white_point_comparison["within_goal"])
    white_violation = max(0.0, white_score - 1.0)
    resolved_regularization = {
        "continuity": 0.0,
        "rgb_prior": 0.0,
        "headroom": 0.0,
        "sensitivity": 0.0,
        **{key: float(value) for key, value in (regularization or {}).items()},
    }
    regularization_score = math.fsum(resolved_regularization.values())
    rank_key = (
        0.0 if neutral["within_gate"] else 1.0,
        neutral_violation,
        0.0 if white_within else 1.0,
        white_violation,
        group_errors["training"]["p90"],
        group_errors["training"]["mean"],
        group_errors["training"]["maximum"],
        group_errors["holdout"]["p90"],
        group_errors["holdout"]["mean"],
        group_errors["holdout"]["maximum"],
        regularization_score,
    )
    return {
        "kind": "lexicographic_neutral_white_training_holdout",
        "global_brightness_scale": scale,
        "neutral": neutral,
        "white_point": dict(white_point_comparison),
        "training": group_errors["training"],
        "holdout": group_errors["holdout"],
        "regularization": {**resolved_regularization, "total": regularization_score},
        "rank_key": list(rank_key),
        "feasible": bool(neutral["within_gate"] and white_within),
    }


def objective_sort_key(objective: Mapping[str, Any]) -> tuple[float, ...]:
    return tuple(float(value) for value in objective["rank_key"])


def objective_from_residual_groups(
    residuals: Mapping[str, Any],
    *,
    neutral_chroma_tolerance: float,
    regularization_score: float = 0.0,
) -> dict[str, Any]:
    if neutral_chroma_tolerance <= 0:
        raise ValueError("neutral_chroma_tolerance must be positive")
    values = {name: np.asarray(residuals[name], dtype="float64") for name in ("neutral", "white", "training", "holdout")}
    if any(array.ndim != 1 or array.size == 0 for array in values.values()):
        raise ValueError("all residual groups must be non-empty one-dimensional vectors")
    neutral_max = float(np.max(np.abs(values["neutral"])))
    white_score = float(np.max(np.abs(values["white"])))

    def summary(name: str) -> dict[str, float]:
        absolute = np.abs(values[name])
        return {
            "mean": float(np.mean(absolute)),
            "p90": float(np.quantile(absolute, 0.9)),
            "maximum": float(np.max(absolute)),
        }

    neutral_within = neutral_max <= neutral_chroma_tolerance
    white_within = white_score < 1.0
    training = summary("training")
    holdout = summary("holdout")
    rank = (
        0.0 if neutral_within else 1.0,
        max(0.0, neutral_max / neutral_chroma_tolerance - 1.0),
        0.0 if white_within else 1.0,
        max(0.0, white_score - 1.0),
        training["p90"], training["mean"], training["maximum"],
        holdout["p90"], holdout["mean"], holdout["maximum"],
        float(regularization_score),
    )
    return {
        "kind": "lexicographic_predicted_residuals",
        "neutral": {"maximum": neutral_max, "tolerance": neutral_chroma_tolerance, "within_gate": neutral_within},
        "white_point": {"goal_score": white_score, "within_goal": white_within},
        "training": training,
        "holdout": holdout,
        "regularization": {"total": float(regularization_score)},
        "rank_key": list(rank),
        "feasible": bool(neutral_within and white_within),
    }


def observation_from_raw_report(
    report: Mapping[str, Any],
    *,
    raw_file: str | Any,
    white_block: int = 6,
    matrix_loader: Any = common.load_rawpy_rgb_xyz_matrix,
) -> dict[str, Any]:
    collection = raw_observer_analysis.collect_patch_plane_features([report])
    rejected = [
        item for item in collection["observations"]
        if item["status"] != "included" or item["quality_status"] != "accepted"
    ]
    if rejected:
        raise RejectedOptimizationFeaturesError(
            rejected,
            weak_signal_only=_weak_signal_only_rejections(report, rejected),
        )
    values = {
        str(item["feature_id"]): float(item["value"])
        for item in collection["observations"]
    }
    prefix = f"block_{int(white_block):02d}"
    white_values = np.asarray(
        [values[f"{prefix}::R"], values[f"{prefix}::G1"], values[f"{prefix}::G2"], values[f"{prefix}::B"]],
        dtype="float64",
    )
    green = float(np.mean(white_values[1:3]))
    if green <= 0:
        raise ValueError("white patch green response must be positive")
    camera_neutral = np.asarray([white_values[0], green, white_values[3]], dtype="float64") / green
    matrix = np.asarray(matrix_loader(raw_file), dtype="float64")
    white_point = common.estimate_white_point_from_camera_neutral(camera_neutral, matrix, np_module=np)
    return {
        "feature_values": values,
        "white_point": {
            **white_point,
            "method": "native_bayer_white_patch_rawpy_matrix_inverse_planckian_locus",
            "block": int(white_block),
            "camera_neutral_g1": camera_neutral.tolist(),
            "rawpy_rgb_xyz_matrix_first3": matrix.tolist(),
        },
        "location_config_sha256": collection["location_config_sha256"],
        "plane_order": collection["plane_order"],
    }


def _weak_signal_only_rejections(
    report: Mapping[str, Any], rejected: Sequence[Mapping[str, Any]]
) -> bool:
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


def build_residual_groups(
    candidate: Mapping[str, Any],
    target: Mapping[str, Any],
    *,
    feature_split: Mapping[str, Sequence[str]],
    neutral_blocks: Sequence[int],
    cct_tolerance_K: float,
    duv_tolerance: float,
) -> dict[str, np.ndarray]:
    candidate_values = candidate["feature_values"]
    target_values = target["feature_values"]
    neutral_residuals: list[float] = []
    for block in neutral_blocks:
        prefix = f"block_{int(block):02d}"
        candidate_block = np.asarray([candidate_values[f"{prefix}::{plane}"] for plane in PLANE_ORDER], dtype="float64")
        target_block = np.asarray([target_values[f"{prefix}::{plane}"] for plane in PLANE_ORDER], dtype="float64")
        candidate_green = float(np.mean(candidate_block[1:3]))
        target_green = float(np.mean(target_block[1:3]))
        if candidate_green <= 0 or target_green <= 0:
            raise ValueError(f"neutral block {block} has non-positive green response")
        neutral_residuals.extend((candidate_block / candidate_green - target_block / target_green).tolist())

    color_features = [*feature_split["training"], *feature_split["holdout"]]
    scale = fit_nonnegative_scale(
        [candidate_values[feature] for feature in color_features],
        [target_values[feature] for feature in color_features],
    )
    floor = max(
        float(np.median(np.abs([target_values[feature] for feature in color_features]))) * 1e-6,
        1e-12,
    )

    def color_residual(group: str) -> np.ndarray:
        return np.asarray([
            (scale * float(candidate_values[feature]) - float(target_values[feature]))
            / max(abs(float(target_values[feature])), floor)
            for feature in feature_split[group]
        ], dtype="float64")

    white = white_point_metrics(
        candidate["white_point"],
        target["white_point"],
        cct_tolerance_K=cct_tolerance_K,
        duv_tolerance=duv_tolerance,
    )
    return {
        "neutral": np.asarray(neutral_residuals, dtype="float64"),
        "white": np.asarray(white["normalized_error"], dtype="float64"),
        "training": color_residual("training"),
        "holdout": color_residual("holdout"),
    }


def repeatability_neutral_tolerance(
    observations: Sequence[Mapping[str, Any]],
    *,
    neutral_blocks: Sequence[int],
    absolute_floor: float,
    sigma_multiplier: float = 3.0,
) -> float:
    if len(observations) < 2:
        raise ValueError("at least two observations are required for repeatability")
    if absolute_floor <= 0 or sigma_multiplier <= 0:
        raise ValueError("repeatability floor and sigma multiplier must be positive")
    normalized: list[list[float]] = []
    for observation in observations:
        values = observation["feature_values"]
        vector: list[float] = []
        for block in neutral_blocks:
            prefix = f"block_{int(block):02d}"
            block_values = np.asarray([values[f"{prefix}::{plane}"] for plane in PLANE_ORDER], dtype="float64")
            green = float(np.mean(block_values[1:3]))
            if green <= 0:
                raise ValueError(f"neutral block {block} has non-positive green response")
            vector.extend((block_values / green).tolist())
        normalized.append(vector)
    sigma = np.std(np.asarray(normalized, dtype="float64"), axis=0, ddof=1)
    return max(float(absolute_floor), float(sigma_multiplier) * float(np.max(sigma)))
