from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import (
    PLANES,
    MAD_NORMALIZER,
    QUANTILE_METHOD,
    feature_ids_sha256,
    regularize_groups,
    unit_shape,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import (
    HUE_NODES,
    SAT_NODES,
    RayHsiManifold,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


POLICY_VERSION = "v2"
SCHEMA_VERSION = 2
WAITING_STATUS = "waiting_for_targeted_measurement"
CANDIDATE_STATUS = "calibrated_waiting_for_planner"
FROZEN_STATUS = "offline_frozen_before_measurement"
REPEATABILITY_CLASSES = (
    "neutral_fullscale",
    "mid_sat_fullscale",
    "sat100_fullscale",
    "neutral_scale_relaxed",
)
SCALE_ESTIMATOR = "q0.6827_abs"
MINIMUM_IDENTIFIABLE_SCALE = 1e-9
DEFAULT_CONDITION_LIMIT = 1e8
DEFAULT_MC_SEED = 27072026
DEFAULT_MC_SAMPLES = 20000
DEFAULT_BOOTSTRAP_REPLICATES = 400
AUDIT_THRESHOLDS = {
    "minimum_effective_samples": 10,
    "trend_whitened_limit": 4.0,
    "bimodal_gap_sigma_limit": 4.0,
    "maximum_single_frame_variance_fraction": 0.5,
    "maximum_bootstrap_relative_span": 0.25,
}
DEFAULT_V1_ARTIFACT = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-uncertainty.json"
DEFAULT_MANIFOLD = PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json"
DEFAULT_WAITING_OUTPUT = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-policy-v2-waiting.json"


def ordered_unit_shape(
    features: Mapping[str, float], feature_ids: Sequence[str]
) -> np.ndarray:
    missing = [feature for feature in feature_ids if feature not in features]
    if missing:
        raise ValueError(f"missing {len(missing)} ordered HSI v2 features")
    return unit_shape([float(features[feature]) for feature in feature_ids])


def plane_block_regularize(
    diagonal_variance: Sequence[float], feature_ids: Sequence[str]
) -> np.ndarray:
    diagonal = np.asarray(diagonal_variance, dtype=float)
    if diagonal.shape != (len(feature_ids),):
        raise ValueError("v2 diagonal covariance does not match feature order")
    if np.any(~np.isfinite(diagonal)) or np.any(diagonal < 0.0):
        raise ValueError("v2 diagonal covariance must be finite and non-negative")
    output = np.empty_like(diagonal)
    for plane in PLANES:
        indices = [
            index for index, feature in enumerate(feature_ids)
            if feature.rsplit("::", 1)[-1] == plane
        ]
        if not indices:
            raise ValueError(f"v2 feature order has no {plane} plane")
        value = float(np.mean(diagonal[indices]))
        if value <= 0.0:
            raise ValueError(f"v2 {plane} variance is not numerically identifiable")
        output[indices] = value
    return output


def conservative_class_variance(
    p1_floor: Sequence[float],
    targeted: Sequence[float] | None,
    feature_ids: Sequence[str],
) -> np.ndarray:
    floor = plane_block_regularize(p1_floor, feature_ids)
    if targeted is None:
        return floor
    measured = plane_block_regularize(targeted, feature_ids)
    return np.maximum(floor, measured)


def mean_difference_covariance(
    left: Sequence[float], left_count: int,
    right: Sequence[float], right_count: int,
    feature_ids: Sequence[str],
) -> np.ndarray:
    if left_count < 1 or right_count < 1:
        raise ValueError("block mean covariance requires positive sample counts")
    left_diagonal = plane_block_regularize(left, feature_ids)
    right_diagonal = plane_block_regularize(right, feature_ids)
    return left_diagonal / left_count + right_diagonal / right_count


def summarize_within_block(
    samples: Sequence[Mapping[str, float]], feature_ids: Sequence[str]
) -> dict[str, Any]:
    if len(samples) < 2:
        raise ValueError("v2 within-block covariance requires at least two repeats")
    matrix = np.vstack([ordered_unit_shape(sample, feature_ids) for sample in samples])
    center = np.mean(matrix, axis=0)
    centered = matrix - center
    regularized = np.empty(len(feature_ids), dtype=float)
    plane_statistics = {}
    for plane in PLANES:
        indices = [index for index, feature in enumerate(feature_ids) if feature.endswith(f"::{plane}")]
        scalars = centered[:, indices].reshape(-1)
        dof = (len(samples) - 1) * len(indices)
        mad_scale = float(np.median(np.abs(scalars)) / MAD_NORMALIZER)
        rms_scale = float(np.sqrt(np.sum(scalars * scalars) / dof))
        variance = max(mad_scale * mad_scale, rms_scale * rms_scale, 1e-12)
        regularized[indices] = variance
        plane_statistics[plane] = {
            "mad_scale": mad_scale, "rms_scale": rms_scale,
            "degrees_of_freedom": dof, "final_variance": variance,
        }
    return {
        "count": len(samples),
        "center": center.tolist(),
        "diagonal_variance": regularized.tolist(),
        "plane_statistics": plane_statistics,
        "regularization": "within_group_centered_cfa_plane_mad_rms",
        "centered_within_block": True,
        "cross_session_shift_absorbed": False,
    }


def summarize_within_groups(
    groups: Mapping[str, Sequence[Mapping[str, float]]],
    feature_ids: Sequence[str],
    *, audit_thresholds: Mapping[str, float] = AUDIT_THRESHOLDS,
) -> dict[str, Any]:
    vectors = {
        str(group_id): [ordered_unit_shape(sample, feature_ids).tolist() for sample in samples]
        for group_id, samples in groups.items()
    }
    regularized = regularize_groups(vectors, feature_ids, center_within_group=True)
    audit = audit_repeatability_groups(vectors, feature_ids, thresholds=audit_thresholds)
    centers = {
        group_id: np.mean(np.asarray(rows, dtype=float), axis=0).tolist()
        for group_id, rows in vectors.items()
    }
    return {
        "group_count": len(vectors),
        "sample_count": sum(len(rows) for rows in vectors.values()),
        "group_centers": centers,
        "diagonal_variance": regularized["diagonal_variance"],
        "regularization": regularized,
        "audit": audit,
        "status": "pass" if audit["status"] == "pass" else "uncertainty_unresolved",
        "centered_within_group": True,
        "cross_session_shift_absorbed": False,
    }


def audit_repeatability_groups(
    groups: Mapping[str, Sequence[Sequence[float]]],
    feature_ids: Sequence[str],
    *, thresholds: Mapping[str, float] = AUDIT_THRESHOLDS,
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    ordered_groups: list[tuple[str, np.ndarray]] = []
    minimum = int(thresholds["minimum_effective_samples"])
    for group_id, values in sorted(groups.items()):
        matrix = np.asarray(values, dtype=float)
        if matrix.ndim != 2 or matrix.shape[1] != len(feature_ids):
            failures.append({"branch": "nonfinite_or_incomplete_feature", "group_id": group_id})
            continue
        if not np.all(np.isfinite(matrix)):
            failures.append({"branch": "nonfinite_feature", "group_id": group_id})
            continue
        ordered_groups.append((group_id, matrix))
    sample_count = sum(len(matrix) for _, matrix in ordered_groups)
    if sample_count < minimum:
        failures.append({"branch": "effective_sample_shortage", "observed": sample_count, "minimum": minimum})
    metrics: dict[str, Any] = {}
    if sample_count >= 2 and not any(item["branch"].startswith("nonfinite") for item in failures):
        centered_groups = [
            (group_id, matrix - np.mean(matrix, axis=0))
            for group_id, matrix in ordered_groups
        ]
        centered = np.vstack([matrix for _, matrix in centered_groups])
        groups_for_regularization = {
            group_id: values.tolist() for group_id, values in ordered_groups
        }
        covariance = np.asarray(
            regularize_groups(groups_for_regularization, feature_ids, center_within_group=True)["diagonal_variance"],
            dtype=float,
        )
        trend_by_group = []
        for group_id, residuals in centered_groups:
            if len(residuals) < 2:
                continue
            chronology = np.linspace(-0.5, 0.5, len(residuals))
            slope = (chronology @ residuals) / float(chronology @ chronology)
            score = direct_whitened_norm(slope, covariance)
            trend_by_group.append({"group_id": group_id, "score": score})
            if score > float(thresholds["trend_whitened_limit"]):
                failures.append({"branch": "trend", "group_id": group_id, "score": score})
        metrics["trend_by_group"] = trend_by_group
        metrics["trend_whitened_score"] = max((item["score"] for item in trend_by_group), default=0.0)
        _, singular, vh = np.linalg.svd(centered, full_matrices=False)
        projection = np.sort(centered @ vh[0]) if singular.size else np.zeros(len(matrix))
        gaps = np.diff(projection)
        robust_sigma = float(np.median(np.abs(projection - np.median(projection))) / 0.6744897501960817)
        bimodal_score = 0.0 if not len(gaps) or robust_sigma <= MINIMUM_IDENTIFIABLE_SCALE else float(np.max(gaps) / robust_sigma)
        metrics["bimodal_gap_sigma"] = bimodal_score
        if bimodal_score > float(thresholds["bimodal_gap_sigma_limit"]):
            failures.append({"branch": "bimodal", "score": bimodal_score, "provenance": "pooled_within_group_residuals"})
        energy = np.sum(centered * centered / covariance, axis=1)
        total = float(np.sum(energy))
        dominance = 0.0 if total <= 0.0 else float(np.max(energy) / total)
        metrics["maximum_single_frame_variance_fraction"] = dominance
        if dominance > float(thresholds["maximum_single_frame_variance_fraction"]):
            failures.append({"branch": "single_outlier_dominates_variance", "fraction": dominance, "provenance": "pooled_within_group_residuals"})
    return {
        "status": "pass" if not failures else "uncertainty_unresolved",
        "thresholds": {str(key): float(value) for key, value in thresholds.items()},
        "metrics": metrics,
        "failure_branches": failures,
        "residual_semantics": "chronological_within_state_command_block_centered",
    }


def direct_whitened_norm(delta: Sequence[float], diagonal_variance: Sequence[float]) -> float:
    values = np.asarray(delta, dtype=float)
    diagonal = np.asarray(diagonal_variance, dtype=float)
    if values.shape != diagonal.shape or np.any(~np.isfinite(values)):
        raise ValueError("direct-feature delta/covariance shape mismatch")
    if np.any(~np.isfinite(diagonal)) or np.any(diagonal <= 0.0):
        raise ValueError("direct-feature covariance must be positive and finite")
    return float(np.sqrt(np.sum(values * values / diagonal)))


def classify_region(score: float, *, guarded_limit: float, unguarded_limit: float) -> str:
    if not (0.0 < guarded_limit <= unguarded_limit):
        raise ValueError("v2 guarded limit must be positive and at most unguarded limit")
    if score <= guarded_limit:
        return "pass"
    if score <= unguarded_limit:
        return "unresolved"
    return "fail"


def evaluate_reference_difference(
    left_mean: Sequence[float], right_mean: Sequence[float],
    *, left_variance: Sequence[float], left_count: int,
    right_variance: Sequence[float], right_count: int,
    feature_ids: Sequence[str], guarded_limit: float, unguarded_limit: float,
    statistic: str,
) -> dict[str, Any]:
    covariance = mean_difference_covariance(
        left_variance, left_count, right_variance, right_count, feature_ids,
    )
    delta = np.asarray(right_mean, dtype=float) - np.asarray(left_mean, dtype=float)
    score = direct_whitened_norm(delta, covariance)
    decision = classify_region(score, guarded_limit=guarded_limit, unguarded_limit=unguarded_limit)
    return {
        "statistic": statistic,
        "space": "ordered_58_feature_unit_shape",
        "score": score,
        "guarded_limit": float(guarded_limit),
        "unguarded_limit": float(unguarded_limit),
        "decision": decision,
        "reference_drift": decision == "fail",
        "delta_l2": float(np.linalg.norm(delta)),
        "mean_difference_diagonal_variance": covariance.tolist(),
        "left_count": int(left_count),
        "right_count": int(right_count),
        "strip_covariance_included": False,
    }


def calibrate_direct_limits(
    center: Sequence[float], diagonal_variance: Sequence[float],
    *, seed: int = DEFAULT_MC_SEED, samples: int = 20000,
    guard_bootstrap_limits: Sequence[float] | None = None,
) -> dict[str, Any]:
    if samples < 1000:
        raise ValueError("v2 Monte Carlo requires at least 1000 samples")
    normalized_center = unit_shape(center)
    diagonal = np.asarray(diagonal_variance, dtype=float)
    if diagonal.shape != normalized_center.shape or np.any(diagonal <= 0.0):
        raise ValueError("invalid v2 Monte Carlo covariance")
    rng = np.random.default_rng(seed)
    noisy = normalized_center + rng.normal(0.0, np.sqrt(diagonal), size=(samples, len(center)))
    noisy /= np.linalg.norm(noisy, axis=1)[:, None]
    delta = noisy - normalized_center
    scores = np.sqrt(np.sum(delta * delta / diagonal, axis=1))
    unguarded = float(np.quantile(scores, 0.9973, method=QUANTILE_METHOD))
    guards = [float(value) for value in (guard_bootstrap_limits or ()) if np.isfinite(value)]
    guarded = min([unguarded, *guards]) if guards else unguarded
    return {
        "statistic": "direct_58_feature_regularized_whitened_norm",
        "normalization": "unit_shape_inside_monte_carlo",
        "seed": int(seed),
        "sample_count": int(samples),
        "quantile": 0.9973,
        "guarded_limit": guarded,
        "unguarded_limit": unguarded,
        "empirical_coverage_guarded": float(np.mean(scores <= guarded)),
        "empirical_coverage_unguarded": float(np.mean(scores <= unguarded)),
    }


def calibrate_joint_regions(
    manifold: RayHsiManifold,
    *, target_hue: float, target_sat: float,
    diagonal_variance: Sequence[float],
    seed: int = DEFAULT_MC_SEED,
    samples: int = DEFAULT_MC_SAMPLES,
    bootstrap_replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    audit_thresholds: Mapping[str, float] = AUDIT_THRESHOLDS,
) -> dict[str, Any]:
    if samples < 1000 or bootstrap_replicates < 100:
        raise ValueError("v2 joint calibration requires at least 1000 MC samples and 100 bootstraps")
    feature_ids = manifold.coordinate_feature_ids
    target = manifold.target_at(target_hue, target_sat)
    center = ordered_unit_shape(target.features, feature_ids)
    covariance = plane_block_regularize(diagonal_variance, feature_ids)
    tangents, coordinate_names, tangent_provenance = _local_tangents(
        manifold,
        target_hue=target_hue,
        target_sat=target_sat,
        feature_ids=feature_ids,
    )
    weighted = 1.0 / covariance
    normal = tangents.T @ (weighted[:, None] * tangents)
    condition = float(np.linalg.cond(normal))
    if not np.isfinite(condition) or condition > DEFAULT_CONDITION_LIMIT:
        return {
            "status": "uncertainty_unresolved",
            "failure_branch": "local_tangent_condition_limit",
            "condition_number": condition,
            "condition_limit": DEFAULT_CONDITION_LIMIT,
        }
    projector = np.linalg.solve(normal, tangents.T * weighted)
    rng = np.random.default_rng(seed)
    noisy = center + rng.normal(0.0, np.sqrt(covariance), size=(samples, len(center)))
    norms = np.linalg.norm(noisy, axis=1)
    if np.any(~np.isfinite(norms)) or np.any(norms <= 0.0):
        raise ValueError("v2 joint Monte Carlo produced non-identifiable unit shapes")
    noisy /= norms[:, None]
    residual = noisy - center
    coordinates = residual @ projector.T
    scales = np.asarray(calibrate_component_scales(coordinates), dtype=float)
    coordinate_scores = np.linalg.norm(coordinates / scales, axis=1)
    observer_scores = np.sqrt(np.sum(residual * residual / covariance, axis=1))
    orthogonal = residual - coordinates @ tangents.T
    rendering_scores = np.sqrt(np.sum(orthogonal * orthogonal / covariance, axis=1))
    coordinate_region = _bootstrap_guarded_region(
        coordinate_scores,
        rng=rng,
        replicates=bootstrap_replicates,
        maximum_relative_span=float(audit_thresholds["maximum_bootstrap_relative_span"]),
    )
    observer_region = _bootstrap_guarded_region(
        observer_scores,
        rng=rng,
        replicates=bootstrap_replicates,
        maximum_relative_span=float(audit_thresholds["maximum_bootstrap_relative_span"]),
    )
    failures = [
        name for name, region in (("coordinate", coordinate_region), ("observer", observer_region))
        if region["status"] != "pass"
    ]
    return {
        "status": "pass" if not failures else "uncertainty_unresolved",
        "failure_branch": None if not failures else "bootstrap_instability",
        "unstable_regions": failures,
        "space": "signed_local_coordinate_and_direct_58_feature_unit_shape",
        "seed": int(seed),
        "sample_count": int(samples),
        "bootstrap_replicates": int(bootstrap_replicates),
        "quantile": 0.9973,
        "target": {"hue": float(target_hue), "sat": float(target_sat)},
        "coordinate_names": list(coordinate_names),
        "component_scales": scales.tolist(),
        "coordinate_region": coordinate_region,
        "observer_region": observer_region,
        "empirical_coverage": {
            "coordinate_unguarded": float(np.mean(coordinate_scores <= coordinate_region["unguarded_limit"])),
            "coordinate_guarded": float(np.mean(coordinate_scores <= coordinate_region["guarded_limit"])),
            "observer_unguarded": float(np.mean(observer_scores <= observer_region["unguarded_limit"])),
            "observer_guarded": float(np.mean(observer_scores <= observer_region["guarded_limit"])),
        },
        "rendering_diagnostic": {
            "p9973_whitened_score": float(np.quantile(rendering_scores, 0.9973, method=QUANTILE_METHOD)),
            "hard_gate": False,
        },
        "condition_number": condition,
        "tangent_provenance": tangent_provenance,
        "noise_components_counted_once": True,
    }


def _bootstrap_guarded_region(
    scores: np.ndarray, *, rng: np.random.Generator, replicates: int,
    maximum_relative_span: float,
) -> dict[str, Any]:
    unguarded = float(np.quantile(scores, 0.9973, method=QUANTILE_METHOD))
    limits = np.empty(replicates, dtype=float)
    for index in range(replicates):
        resampled = rng.choice(scores, size=len(scores), replace=True)
        limits[index] = np.quantile(resampled, 0.9973, method=QUANTILE_METHOD)
    lower, median, upper = (
        float(np.quantile(limits, q, method=QUANTILE_METHOD)) for q in (0.05, 0.5, 0.95)
    )
    relative_span = float((upper - lower) / median) if median > 0.0 else float("inf")
    stable = np.isfinite(relative_span) and relative_span <= maximum_relative_span
    return {
        "status": "pass" if stable else "uncertainty_unresolved",
        "guarded_limit": min(unguarded, lower),
        "unguarded_limit": unguarded,
        "guard_calculation": "min(full_mc_q0.9973, bootstrap_q0.05_of_q0.9973)",
        "bootstrap_q05": lower,
        "bootstrap_median": median,
        "bootstrap_q95": upper,
        "bootstrap_relative_span": relative_span,
        "maximum_bootstrap_relative_span": maximum_relative_span,
    }


def calibrate_component_scales(outputs: Sequence[Sequence[float]]) -> list[float]:
    values = np.asarray(outputs, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2 or np.any(~np.isfinite(values)):
        raise ValueError("v2 component scale calibration requires finite 2-D samples")
    scales = np.quantile(np.abs(values), 0.6827, axis=0, method=QUANTILE_METHOD)
    if np.any(~np.isfinite(scales)) or np.any(scales < MINIMUM_IDENTIFIABLE_SCALE):
        raise ValueError("required v2 component scale is numerically unidentifiable")
    return [float(value) for value in scales]


def local_tangent_evaluate(
    manifold: RayHsiManifold,
    candidate_features: Mapping[str, float],
    *, target_hue: float, target_sat: float,
    diagonal_variance: Sequence[float],
    condition_limit: float = DEFAULT_CONDITION_LIMIT,
) -> dict[str, Any]:
    feature_ids = manifold.coordinate_feature_ids
    candidate = ordered_unit_shape(candidate_features, feature_ids)
    target = manifold.target_at(target_hue, target_sat)
    target_vector = ordered_unit_shape(target.features, feature_ids)
    residual = candidate - target_vector
    covariance = plane_block_regularize(diagonal_variance, feature_ids)
    tangents, coordinate_names, tangent_provenance = _local_tangents(
        manifold, target_hue=target_hue, target_sat=target_sat,
        feature_ids=feature_ids,
    )
    weighted = 1.0 / covariance
    normal = tangents.T @ (weighted[:, None] * tangents)
    rhs = tangents.T @ (weighted * residual)
    condition = float(np.linalg.cond(normal))
    if not np.isfinite(condition) or condition > condition_limit:
        return {
            "status": "uncertainty_unresolved",
            "reason": "local_tangent_condition_limit",
            "condition_number": condition,
            "condition_limit": float(condition_limit),
            "hue_defined": float(target_sat) > 0.0,
            "tangent_provenance": tangent_provenance,
        }
    delta = np.linalg.solve(normal, rhs)
    orthogonal = residual - tangents @ delta
    coordinate = dict(zip(coordinate_names, map(float, delta), strict=True))
    hue_error = coordinate.get("hue_error_degrees")
    if hue_error is not None:
        coordinate["hue_error_degrees"] = (hue_error + 180.0) % 360.0 - 180.0
    return {
        "status": "evaluated",
        "evaluator": "signed_target_local_tangent_v2",
        "hue_defined": float(target_sat) > 0.0,
        **({"hue_error_degrees": coordinate["hue_error_degrees"]} if hue_error is not None else {}),
        "sat_error_percent": coordinate["sat_error_percent"],
        "condition_number": condition,
        "condition_limit": float(condition_limit),
        "signed_unclipped": True,
        "direct_residual": residual.tolist(),
        "directional_orthogonal_residual": orthogonal.tolist(),
        "observer_whitened_score": direct_whitened_norm(residual, covariance),
        "color_rendering_residual": _residual_summary(orthogonal, feature_ids, covariance),
        "tangent_provenance": tangent_provenance,
    }


def evaluate_confirmation_spread(
    samples: Sequence[Mapping[str, float]], *, feature_ids: Sequence[str],
    class_name: str, class_variance: Sequence[float], limit: float | None,
) -> dict[str, Any]:
    if class_name not in REPEATABILITY_CLASSES:
        raise ValueError(f"unsupported v2 repeatability class: {class_name}")
    if len(samples) not in {3, 5}:
        raise ValueError("v2 confirmation spread requires exactly n=3 or n=5")
    vectors = [ordered_unit_shape(sample, feature_ids) for sample in samples]
    pair_variance = 2.0 * plane_block_regularize(class_variance, feature_ids)
    pair_scores = [
        direct_whitened_norm(vectors[left] - vectors[right], pair_variance)
        for left in range(len(vectors)) for right in range(left + 1, len(vectors))
    ]
    maximum = max(pair_scores)
    return {
        "space": "ordered_58_feature_unit_shape",
        "class": class_name,
        "confirmation_count": len(samples),
        "pair_scores": pair_scores,
        "group_maximum_score": maximum,
        "limit": None if limit is None else float(limit),
        "decision": WAITING_STATUS if limit is None else ("pass" if maximum <= limit else "fail"),
    }


def calibrate_confirmation_group_limit(
    center: Sequence[float], class_variance: Sequence[float],
    *, count: int, seed: int = DEFAULT_MC_SEED, samples: int = 20000,
) -> float:
    if count not in {3, 5} or samples < 1000:
        raise ValueError("v2 repeat calibration requires n=3/n=5 and at least 1000 samples")
    center_unit = unit_shape(center)
    variance = np.asarray(class_variance, dtype=float)
    if variance.shape != center_unit.shape or np.any(variance <= 0.0):
        raise ValueError("invalid v2 repeat calibration covariance")
    rng = np.random.default_rng(seed)
    maxima = np.empty(samples, dtype=float)
    pair_variance = 2.0 * variance
    for sample_index in range(samples):
        group = center_unit + rng.normal(0.0, np.sqrt(variance), size=(count, len(center_unit)))
        group /= np.linalg.norm(group, axis=1)[:, None]
        maxima[sample_index] = max(
            direct_whitened_norm(group[left] - group[right], pair_variance)
            for left in range(count) for right in range(left + 1, count)
        )
    return float(np.quantile(maxima, 0.9973, method=QUANTILE_METHOD))


def build_waiting_artifact(
    *, feature_ids: Sequence[str], v1_artifact: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    if v1_artifact.get("schema_version") != 1:
        raise ValueError("P7-R0 v2 bootstrap requires the frozen v1 artifact")
    p1_floor = v1_artifact["components"]["strip_repeatability_floor"]["diagonal_variance"]
    ray = v1_artifact["components"]["ray_repeatability"]["diagonal_variance"]
    return {
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "status": WAITING_STATUS,
        "formal_capture_eligible": False,
        "feature_set": {
            "count": len(feature_ids), "ids": list(feature_ids),
            "sha256": feature_ids_sha256(feature_ids),
            "transform": "exposure-normalized then unit shape",
        },
        "inputs": dict(inputs),
        "reference_policy": {
            "status": WAITING_STATUS,
            "statistics": ["reference_center_compatibility", "reference_repeatability"],
            "space": "ordered_58_feature_unit_shape",
            "strip_covariance_included": False,
            "ray_within_state_diagonal_variance": list(ray),
            "limits": None,
        },
        "repeatability_policy": {
            "status": WAITING_STATUS,
            "classes": {
                name: {"status": WAITING_STATUS, "p1_floor_diagonal_variance": list(p1_floor), "targeted_variance": None, "limits": {"3": None, "5": None}}
                for name in REPEATABILITY_CLASSES
            },
            "pair_covariance": "2 * max_per_plane(Sigma_P1_floor, Sigma_targeted_class)",
        },
        "coordinate_policy": {
            "evaluator": "signed_target_local_tangent_v2",
            "sat100": "one_sided_from_nearest_lower_measured_node",
            "sat0_hue_gate": False,
            "condition_limit": DEFAULT_CONDITION_LIMIT,
            "scale_estimator": SCALE_ESTIMATOR,
            "minimum_identifiable_scale": MINIMUM_IDENTIFIABLE_SCALE,
            "monte_carlo_seed": DEFAULT_MC_SEED,
            "formal_limits": None,
        },
        "match_components": {
            "ray_repeatability_diagonal_variance": list(ray),
            "interpolation": v1_artifact["components"]["interpolation"],
            "recipe": "Sigma_ray + Sigma_strip_class + Sigma_interpolation",
            "camera_noise_extra_component": False,
        },
        "observer_policy": {"formal_limits": None},
        "output_layers": ["hsi_coordinate_equivalent", "observer_equivalent", "color_rendering_residual"],
        "prohibitions": [
            "no_fit_from_sentinel_confirmations", "no_clipped_endpoint_coordinate",
            "no_1e-12_scale_escape", "no_gate6_until_new_named_experiment",
        ],
    }


class HsiPolicyV2:
    def __init__(self, artifact: Mapping[str, Any], *, artifact_sha256: str | None = None) -> None:
        if artifact.get("schema_version") != SCHEMA_VERSION or artifact.get("policy_version") != POLICY_VERSION:
            raise ValueError("not an HSI policy v2 artifact")
        if artifact.get("status") not in {WAITING_STATUS, CANDIDATE_STATUS, FROZEN_STATUS}:
            raise ValueError("unsupported HSI policy v2 status")
        if artifact.get("status") != FROZEN_STATUS and artifact.get("formal_capture_eligible") is not False:
            raise ValueError("waiting/candidate HSI policy v2 must be formal_capture_eligible=false")
        self.artifact = dict(artifact)
        self.artifact_sha256 = artifact_sha256

    @classmethod
    def load(cls, path: str | Path) -> "HsiPolicyV2":
        artifact_path = Path(path)
        value = json.loads(artifact_path.read_text(encoding="utf-8"))
        return cls(value, artifact_sha256=hashlib.sha256(artifact_path.read_bytes()).hexdigest())

    @property
    def formal_capture_eligible(self) -> bool:
        return self.artifact.get("status") == FROZEN_STATUS and self.artifact.get("formal_capture_eligible") is True


def write_policy_v2(path: str | Path, artifact: Mapping[str, Any]) -> Path:
    HsiPolicyV2(artifact)
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, output)
    return output


def build_waiting_artifact_from_files(
    *, v1_path: str | Path = DEFAULT_V1_ARTIFACT,
    manifold_path: str | Path = DEFAULT_MANIFOLD,
) -> dict[str, Any]:
    v1_file = Path(v1_path)
    manifold_file = Path(manifold_path)
    manifold = RayHsiManifold.load(manifold_file)
    v1 = json.loads(v1_file.read_text(encoding="utf-8"))
    return build_waiting_artifact(
        feature_ids=manifold.coordinate_feature_ids,
        v1_artifact=v1,
        inputs={
            "v1_uncertainty_artifact": _file_reference(v1_file),
            "ray_hsi_manifold": _file_reference(manifold_file),
        },
    )


def _local_tangents(
    manifold: RayHsiManifold, *, target_hue: float, target_sat: float,
    feature_ids: Sequence[str],
) -> tuple[np.ndarray, tuple[str, ...], dict[str, Any]]:
    hue = float(target_hue) % 360.0
    sat = float(target_sat)
    if sat < 0.0 or sat > 100.0:
        raise ValueError("v2 acceptance tangent requires SAT within 0..100")
    if sat == 0.0:
        current = ordered_unit_shape(manifold.target_at(hue, 0).features, feature_ids)
        upper = ordered_unit_shape(manifold.target_at(hue, SAT_NODES[1]).features, feature_ids)
        sat_tangent = (upper - current) / SAT_NODES[1]
        return sat_tangent[:, None], ("sat_error_percent",), {
            "hue": None, "sat": {"nodes": [0, SAT_NODES[1]], "kind": "one_sided_neutral"},
        }
    hue_step = 30.0
    before = ordered_unit_shape(manifold.target_at(hue - hue_step, sat).features, feature_ids)
    after = ordered_unit_shape(manifold.target_at(hue + hue_step, sat).features, feature_ids)
    hue_tangent = (after - before) / (2.0 * hue_step)
    if sat == 100.0:
        lower_sat = SAT_NODES[-2]
        lower = ordered_unit_shape(manifold.target_at(hue, lower_sat).features, feature_ids)
        current = ordered_unit_shape(manifold.target_at(hue, 100).features, feature_ids)
        sat_tangent = (current - lower) / (100.0 - lower_sat)
        sat_kind = "one_sided_endpoint_signed_unclipped"
        sat_nodes = [lower_sat, 100]
    else:
        if sat in SAT_NODES:
            sat_index = SAT_NODES.index(int(sat))
            lower_sat, upper_sat = SAT_NODES[sat_index - 1], SAT_NODES[sat_index + 1]
        else:
            lower_sat = max(node for node in SAT_NODES if node < sat)
            upper_sat = min(node for node in SAT_NODES if node > sat)
        lower = ordered_unit_shape(manifold.target_at(hue, lower_sat).features, feature_ids)
        upper = ordered_unit_shape(manifold.target_at(hue, upper_sat).features, feature_ids)
        sat_tangent = (upper - lower) / (upper_sat - lower_sat)
        sat_kind = "central_measured_nodes"
        sat_nodes = [lower_sat, upper_sat]
    return np.column_stack((hue_tangent, sat_tangent)), (
        "hue_error_degrees", "sat_error_percent",
    ), {
        "hue": {"nodes": [int((hue - hue_step) % 360), int((hue + hue_step) % 360)], "kind": "periodic_central"},
        "sat": {"nodes": sat_nodes, "kind": sat_kind},
    }


def _residual_summary(
    residual: np.ndarray, feature_ids: Sequence[str], diagonal_variance: np.ndarray
) -> dict[str, Any]:
    per_plane = {}
    per_patch: dict[str, list[float]] = {}
    for plane in PLANES:
        indices = [index for index, feature in enumerate(feature_ids) if feature.endswith(f"::{plane}")]
        values = residual[indices]
        per_plane[plane] = {
            "l2": float(np.linalg.norm(values)),
            "whitened_l2": direct_whitened_norm(values, diagonal_variance[indices]),
        }
    for index, feature in enumerate(feature_ids):
        patch = feature.split("::", 1)[0]
        per_patch.setdefault(patch, []).append(float(residual[index]))
    return {
        "raw_l2": float(np.linalg.norm(residual)),
        "whitened_score": direct_whitened_norm(residual, diagonal_variance),
        "directional_vector": residual.tolist(),
        "per_plane": per_plane,
        "per_patch_l2": {patch: float(np.linalg.norm(values)) for patch, values in sorted(per_patch.items())},
    }


def _file_reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the offline-only P7 HSI policy v2 waiting artifact.")
    parser.add_argument("--v1-artifact", type=Path, default=DEFAULT_V1_ARTIFACT)
    parser.add_argument("--manifold", type=Path, default=DEFAULT_MANIFOLD)
    parser.add_argument("--output", type=Path, default=DEFAULT_WAITING_OUTPUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    artifact = build_waiting_artifact_from_files(
        v1_path=args.v1_artifact, manifold_path=args.manifold,
    )
    print(write_policy_v2(args.output, artifact))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
