from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement import raw_observer_analysis


SCHEMA_VERSION = 1
CHANNELS = ("cw", "ww", "r", "g", "b")
LEVEL_CODES = (1024, 2048, 4095)


def analyze_chart_response_basis(
    reports: Sequence[Mapping[str, Any]],
    *,
    channels: Sequence[str] = CHANNELS,
    level_codes: Sequence[int] = LEVEL_CODES,
    minimum_repeats: int = 3,
    bootstrap_samples: int = 1000,
    random_seed: int = 20260716,
) -> dict[str, Any]:
    """Fit level-specific five-channel bases from native Bayer patch reports."""

    if minimum_repeats < 2:
        raise ValueError("minimum_repeats must be at least 2")
    if bootstrap_samples < 100:
        raise ValueError("bootstrap_samples must be at least 100")
    channel_order = _validate_channels(channels)
    levels = _validate_levels(level_codes)
    formal = [report for report in reports if _context(report, "purpose") == "basis_formal"]
    if not formal:
        raise ValueError("no basis_formal reports were supplied")

    collection = raw_observer_analysis.collect_patch_plane_features(formal)
    grouped: dict[tuple[str, int, str], list[float]] = defaultdict(list)
    rejected: list[dict[str, Any]] = []
    for observation in collection["observations"]:
        report = formal[int(observation["report_index"])]
        channel = str(_context(report, "channel"))
        target_code = int(_context(report, "target_code"))
        if channel not in channel_order or target_code not in levels:
            raise ValueError(f"unexpected basis state: channel={channel}, target_code={target_code}")
        reason = _observation_rejection_reason(observation)
        if reason is not None:
            rejected.append(
                {
                    "report_id": observation["report_id"],
                    "feature_id": observation["feature_id"],
                    "channel": channel,
                    "target_code": target_code,
                    "reason": reason,
                }
            )
            continue
        grouped[(channel, target_code, str(observation["feature_id"]))].append(
            float(observation["value"])
        )

    expected_states = {(channel, level) for channel in channel_order for level in levels}
    actual_states = {(channel, level) for channel, level, _feature in grouped}
    missing_states = sorted(expected_states - actual_states)
    if missing_states:
        raise ValueError(f"basis reports are missing channel/level states: {missing_states}")

    all_features = sorted({str(item["feature_id"]) for item in collection["observations"]})
    if not all_features:
        raise ValueError("basis reports contain no patch-plane features")

    rng = np.random.default_rng(random_seed)
    statistics: dict[str, dict[str, dict[str, Any]]] = {}
    bases: dict[str, Any] = {}
    normalized_by_level: dict[int, np.ndarray] = {}
    direct_mask_by_level: dict[int, np.ndarray] = {}
    feature_noise: dict[str, list[float]] = defaultdict(list)
    direct: dict[tuple[str, int, str], dict[str, Any]] = {}
    for channel, level in expected_states:
        fraction = level / 4095.0
        for feature in all_features:
            values = np.asarray(grouped[(channel, level, feature)], dtype=float)
            if values.size < minimum_repeats:
                continue
            center = float(np.median(values))
            standard_deviation = float(np.std(values, ddof=1))
            bootstrap = np.median(
                rng.choice(values, size=(bootstrap_samples, values.size), replace=True),
                axis=1,
            ) / fraction
            ci_low, ci_high = np.percentile(bootstrap, (2.5, 97.5))
            direct[(channel, level, feature)] = {
                "mode": "direct",
                "repeat_count": int(values.size),
                "center": center,
                "standard_deviation": standard_deviation,
                "normalized_center": center / fraction,
                "normalized_center_ci95": [float(ci_low), float(ci_high)],
            }
            feature_noise[feature].append(standard_deviation / max(abs(center), 1e-12))

    imputed_cells: list[dict[str, Any]] = []
    censored_cells: list[dict[str, Any]] = []
    for level in levels:
        matrix = np.empty((len(all_features), len(channel_order)), dtype=float)
        cell_weights = np.empty_like(matrix)
        direct_mask = np.zeros_like(matrix, dtype=bool)
        level_stats: dict[str, dict[str, Any]] = {}
        for channel_index, channel in enumerate(channel_order):
            channel_stats: dict[str, Any] = {}
            for feature_index, feature in enumerate(all_features):
                cell = direct.get((channel, level, feature))
                if cell is not None:
                    resolved = dict(cell)
                    direct_mask[feature_index, channel_index] = True
                    cell_weights[feature_index, channel_index] = 1.0
                else:
                    donors = [
                        (donor_level, direct[(channel, donor_level, feature)])
                        for donor_level in levels
                        if (channel, donor_level, feature) in direct
                    ]
                    if donors:
                        donor_level, donor = min(
                            donors,
                            key=lambda item: abs(math.log(float(item[0]) / float(level))),
                        )
                        resolved = {
                            "mode": "imputed_from_level",
                            "repeat_count": 0,
                            "center": None,
                            "standard_deviation": None,
                            "normalized_center": donor["normalized_center"],
                            "normalized_center_ci95": donor["normalized_center_ci95"],
                            "imputed_from_level": donor_level,
                        }
                        cell_weights[feature_index, channel_index] = 0.25
                        imputed_cells.append(
                            {"channel": channel, "target_code": level, "feature_id": feature, "from_level": donor_level}
                        )
                    else:
                        resolved = {
                            "mode": "censored_zero",
                            "repeat_count": 0,
                            "center": None,
                            "standard_deviation": None,
                            "normalized_center": 0.0,
                            "normalized_center_ci95": None,
                        }
                        cell_weights[feature_index, channel_index] = 0.0
                        censored_cells.append(
                            {"channel": channel, "target_code": level, "feature_id": feature}
                        )
                matrix[feature_index, channel_index] = float(resolved["normalized_center"])
                channel_stats[feature] = resolved
            level_stats[channel] = channel_stats
        normalized_by_level[level] = matrix
        direct_mask_by_level[level] = direct_mask
        statistics[str(level)] = level_stats
        bases[str(level)] = {
            "matrix": matrix.tolist(),
            "cell_weights": cell_weights.tolist(),
            "diagnostics": _matrix_diagnostics(matrix, channel_order),
        }

    raw_weights = {
        feature: 1.0 / max(float(np.median(values)) ** 2, 1e-12)
        for feature, values in feature_noise.items()
    }
    missing_weight = float(np.median(list(raw_weights.values()))) if raw_weights else 1.0
    for feature in all_features:
        raw_weights.setdefault(feature, missing_weight)
    median_weight = float(np.median(list(raw_weights.values())))
    feature_weights = {feature: value / median_weight for feature, value in raw_weights.items()}

    anchor_reports = [
        report
        for report in reports
        if _context(report, "purpose") in {"anchor_auto_exposure", "anchor_check"}
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "chart_response_basis",
        "status": "ready_for_manual_branch_review",
        "location_config_sha256": collection["location_config_sha256"],
        "channels": list(channel_order),
        "level_codes": list(levels),
        "feature_order": all_features,
        "feature_count": len(all_features),
        "plane_order": list(collection["plane_order"]),
        "basis_by_level": bases,
        "feature_statistics": statistics,
        "feature_weights": feature_weights,
        "repeatability_summary": _repeatability_summary(statistics, channel_order, levels),
        "level_shape_comparison": _compare_levels(
            normalized_by_level,
            direct_mask_by_level,
            statistics,
            channel_order,
        ),
        "anchor_drift": _analyze_anchor_drift(anchor_reports),
        "rejections": {
            "observation_count": len(rejected),
            "observations": rejected,
            "imputed_cell_count": len(imputed_cells),
            "imputed_cells": imputed_cells,
            "censored_zero_cell_count": len(censored_cells),
            "censored_zero_cells": censored_cells,
        },
        "bootstrap": {"samples": bootstrap_samples, "random_seed": random_seed},
        "notes": [
            "Each basis column is divided by target_code/4095 before level comparison.",
            "Rejected or near-noise observations never enter a direct basis center.",
            "A missing cell borrows the nearest same-channel accepted normalized level only for matrix conditioning; imputed cells never enter level-shape comparisons.",
            "A channel-feature with no accepted level is represented as censored zero with cell weight 0.",
            "No B-A/B-B/B-C/B-D branch is selected automatically.",
        ],
    }


def _matrix_diagnostics(matrix: np.ndarray, channels: Sequence[str]) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    tolerance = float(max(matrix.shape) * np.finfo(float).eps * singular_values[0])
    rank = int(np.sum(singular_values > tolerance))
    condition = math.inf if rank < len(channels) else float(singular_values[0] / singular_values[-1])
    angles: list[dict[str, Any]] = []
    for left in range(len(channels)):
        for right in range(left + 1, len(channels)):
            a = matrix[:, left]
            b = matrix[:, right]
            cosine = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
            cosine = min(1.0, max(-1.0, cosine))
            angles.append(
                {
                    "left": channels[left],
                    "right": channels[right],
                    "cosine": cosine,
                    "angle_degrees": float(np.degrees(np.arccos(cosine))),
                }
            )
    return {
        "rank": rank,
        "condition_number": None if not math.isfinite(condition) else condition,
        "singular_values": singular_values.tolist(),
        "rank_tolerance": tolerance,
        "column_angles": angles,
    }


def _compare_levels(
    matrices: Mapping[int, np.ndarray],
    direct_masks: Mapping[int, np.ndarray],
    statistics: Mapping[str, Mapping[str, Mapping[str, Any]]],
    channels: Sequence[str],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    levels = sorted(matrices)
    for channel_index, channel in enumerate(channels):
        for left_index, left_level in enumerate(levels):
            for right_level in levels[left_index + 1 :]:
                mask = direct_masks[left_level][:, channel_index] & direct_masks[right_level][:, channel_index]
                left = matrices[left_level][mask, channel_index]
                right = matrices[right_level][mask, channel_index]
                if left.size < 2 or np.linalg.norm(left) == 0 or np.linalg.norm(right) == 0:
                    output.append(
                        {
                            "channel": channel,
                            "left_level": left_level,
                            "right_level": right_level,
                            "direct_feature_count": int(left.size),
                            "relative_l2_shape_difference": None,
                            "cosine": None,
                        }
                    )
                    continue
                left_unit = left / np.linalg.norm(left)
                right_unit = right / np.linalg.norm(right)
                cosine = float(np.dot(left_unit, right_unit))
                scale = float(np.median(right / left))
                shape_residual = right / (left * scale) - 1.0
                sigma_multiples: list[float] = []
                direct_features = [
                    feature
                    for feature, included in zip(statistics[str(left_level)][channel], mask)
                    if included
                ]
                for feature, residual in zip(direct_features, shape_residual):
                    left_stat = statistics[str(left_level)][channel][feature]
                    right_stat = statistics[str(right_level)][channel][feature]
                    left_cv = float(left_stat["standard_deviation"]) / max(abs(float(left_stat["center"])), 1e-12)
                    right_cv = float(right_stat["standard_deviation"]) / max(abs(float(right_stat["center"])), 1e-12)
                    sigma = math.sqrt(left_cv * left_cv + right_cv * right_cv)
                    sigma_multiples.append(math.inf if sigma == 0 and residual != 0 else (0.0 if sigma == 0 else abs(float(residual)) / sigma))
                output.append(
                    {
                        "channel": channel,
                        "left_level": left_level,
                        "right_level": right_level,
                        "direct_feature_count": int(left.size),
                        "relative_l2_shape_difference": float(np.linalg.norm(left_unit - right_unit)),
                        "cosine": min(1.0, max(-1.0, cosine)),
                        "global_scale_right_to_left": scale,
                        "absolute_shape_relative_residual": _distribution_summary(np.abs(shape_residual)),
                        "shape_residual_repeatability_sigma": _distribution_summary(sigma_multiples),
                        "feature_count_over_3_sigma": sum(value > 3.0 for value in sigma_multiples),
                    }
                )
    return output


def _repeatability_summary(
    statistics: Mapping[str, Mapping[str, Mapping[str, Any]]],
    channels: Sequence[str],
    levels: Sequence[int],
) -> dict[str, Any]:
    by_level: dict[str, Any] = {}
    for level in levels:
        by_level[str(level)] = {}
        for channel in channels:
            cvs = [
                float(item["standard_deviation"]) / max(abs(float(item["center"])), 1e-12)
                for item in statistics[str(level)][channel].values()
                if item["mode"] == "direct"
            ]
            by_level[str(level)][channel] = _distribution_summary(cvs)
    return {"coefficient_of_variation_by_level_channel": by_level}


def _analyze_anchor_drift(reports: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if len(reports) != 2:
        return {"status": "unavailable", "report_count": len(reports)}
    collection = raw_observer_analysis.collect_patch_plane_features(reports)
    by_report: dict[str, dict[str, float]] = defaultdict(dict)
    planes: dict[str, str] = {}
    for observation in collection["observations"]:
        if _observation_rejection_reason(observation) is not None:
            continue
        feature = str(observation["feature_id"])
        by_report[str(observation["report_id"])][feature] = float(observation["value"])
        planes[feature] = str(observation["plane"])
    report_ids = [str(_context(report, "capture_id")) for report in reports]
    common = sorted(set(by_report[report_ids[0]]) & set(by_report[report_ids[1]]))
    ratios = np.asarray(
        [by_report[report_ids[1]][feature] / by_report[report_ids[0]][feature] for feature in common],
        dtype=float,
    )
    global_scale = float(np.median(ratios)) if ratios.size else None
    shape = ratios / global_scale - 1.0 if global_scale not in (None, 0.0) else np.asarray([], dtype=float)
    return {
        "status": "complete" if common else "no_common_accepted_features",
        "report_ids": report_ids,
        "common_feature_count": len(common),
        "global_scale_right_to_left": global_scale,
        "absolute_relative_drift": _distribution_summary(np.abs(ratios - 1.0)),
        "absolute_shape_drift": _distribution_summary(np.abs(shape)),
        "absolute_shape_drift_by_plane": {
            plane: _distribution_summary(
                abs(float(value))
                for feature, value in zip(common, shape)
                if planes[feature] == plane
            )
            for plane in ("R", "G1", "G2", "B")
        },
    }


def _distribution_summary(values: Sequence[float] | np.ndarray) -> dict[str, Any]:
    finite = np.asarray([float(value) for value in values if math.isfinite(float(value))], dtype=float)
    if finite.size == 0:
        return {"count": 0, "p50": None, "p90": None, "p95": None, "max": None}
    return {
        "count": int(finite.size),
        "p50": float(np.percentile(finite, 50)),
        "p90": float(np.percentile(finite, 90)),
        "p95": float(np.percentile(finite, 95)),
        "max": float(np.max(finite)),
    }


def _observation_rejection_reason(observation: Mapping[str, Any]) -> str | None:
    if observation.get("status") != "included":
        return str(observation.get("status"))
    quality_status = str(observation.get("quality_status"))
    if quality_status != "accepted":
        return f"quality_{quality_status}"
    return None


def _context(report: Mapping[str, Any], key: str) -> Any:
    context = report.get("analysis_context")
    if not isinstance(context, Mapping) or key not in context:
        raise ValueError(f"basis report is missing analysis_context.{key}")
    return context[key]


def _validate_channels(channels: Sequence[str]) -> tuple[str, ...]:
    values = tuple(str(value) for value in channels)
    if values != CHANNELS:
        raise ValueError(f"channels must be exactly {CHANNELS}")
    return values


def _validate_levels(level_codes: Sequence[int]) -> tuple[int, ...]:
    values = tuple(int(value) for value in level_codes)
    if values != LEVEL_CODES:
        raise ValueError(f"level_codes must be exactly {LEVEL_CODES}")
    return values
