from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement import raw_observer_analysis
from camera_based_rgbww_optimizer.measurement.chart_response_basis import (
    CHANNELS,
    LEVEL_CODES,
    _observation_rejection_reason,
)


SCHEMA_VERSION = 1


def analyze_chart_basis_validation(
    reports: Sequence[Mapping[str, Any]], basis: Mapping[str, Any], *, minimum_repeats: int = 2
) -> dict[str, Any]:
    """Evaluate held-out RGBWW mixtures against the frozen piecewise P2 basis."""
    _validate_basis(basis)
    if minimum_repeats != 2:
        raise ValueError("P3 analysis requires exactly two repeats")
    formal = [report for report in reports if _context(report, "purpose") == "mixture_formal"]
    if not formal:
        raise ValueError("no mixture_formal reports were supplied")
    collection = raw_observer_analysis.collect_patch_plane_features(formal)
    if collection["location_config_sha256"] != basis["location_config_sha256"]:
        raise ValueError("P2 basis and P3 reports use different location hashes")
    if list(collection["plane_order"]) != basis["plane_order"]:
        raise ValueError("P2 basis and P3 reports use different CFA planes")

    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    sample_context: dict[str, dict[str, Any]] = {}
    previous_states_by_capture: dict[str, dict[str, Any]] = defaultdict(dict)
    rejected: list[dict[str, Any]] = []
    for observation in collection["observations"]:
        report = formal[int(observation["report_index"])]
        sample_id = str(_context(report, "sample_id"))
        if not sample_id:
            raise ValueError("mixture report is missing sample_id")
        context = dict(report.get("analysis_context", {}))
        command = context.get("command")
        if not isinstance(command, Mapping):
            raise ValueError(f"mixture {sample_id} is missing its command")
        normalized_command = {channel: int(command[channel]) for channel in CHANNELS}
        current = {
            "sample_id": sample_id,
            "category": str(context.get("category")),
            "state_index": int(context.get("state_index")),
            "command": normalized_command,
            "total_target_load": int(context.get("total_target_load", sum(normalized_command.values()))),
            "active_set": list(context.get("active_set", [channel for channel in CHANNELS if normalized_command[channel] > 0])),
        }
        if sample_id in sample_context and sample_context[sample_id] != current:
            raise ValueError(f"mixture {sample_id} repeats have inconsistent context")
        sample_context[sample_id] = current
        capture_id = str(context.get("capture_id"))
        previous_states_by_capture[sample_id].setdefault(capture_id, context.get("previous_state"))
        reason = _observation_rejection_reason(observation)
        if reason is not None:
            rejected.append(
                {"sample_id": sample_id, "report_id": observation["report_id"], "feature_id": observation["feature_id"], "reason": reason}
            )
            continue
        grouped[(sample_id, str(observation["feature_id"]))].append(float(observation["value"]))

    if len(sample_context) != 24:
        raise ValueError(f"P3 requires 24 mixture samples, found {len(sample_context)}")
    for sample_id, context in sample_context.items():
        context["previous_states"] = list(previous_states_by_capture[sample_id].values())
    sample_results: list[dict[str, Any]] = []
    for sample_id, context in sorted(sample_context.items(), key=lambda item: item[1]["state_index"]):
        prediction = predict_piecewise_basis(basis, context["command"])
        measured: list[float] = []
        predicted: list[float] = []
        weights: list[float] = []
        sigma: list[float] = []
        feature_ids: list[str] = []
        repeat_sigma: list[float] = []
        basis_sigma: list[float] = []
        for feature_index, feature in enumerate(basis["feature_order"]):
            values = np.asarray(grouped[(sample_id, feature)], dtype=float)
            if values.size < minimum_repeats:
                continue
            center = float(np.median(values))
            observed_sigma = float(np.std(values, ddof=1) / math.sqrt(values.size))
            model_sigma = float(prediction["basis_center_sigma"][feature_index])
            combined_sigma = math.sqrt(observed_sigma * observed_sigma + model_sigma * model_sigma)
            confidence = float(prediction["confidence"][feature_index])
            feature_weight = float(basis["feature_weights"][feature]) * confidence
            if feature_weight <= 0 or prediction["values"][feature_index] <= 0:
                continue
            feature_ids.append(feature)
            measured.append(center)
            predicted.append(float(prediction["values"][feature_index]))
            weights.append(feature_weight)
            sigma.append(combined_sigma)
            repeat_sigma.append(observed_sigma)
            basis_sigma.append(model_sigma)
        if len(feature_ids) < 5:
            raise ValueError(f"mixture {sample_id} has too few accepted predictable features")
        sample_results.append(
            _sample_result(
                context,
                feature_ids=feature_ids,
                measured=np.asarray(measured),
                predicted=np.asarray(predicted),
                weights=np.asarray(weights),
                sigma=np.asarray(sigma),
                repeat_sigma=np.asarray(repeat_sigma),
                basis_sigma=np.asarray(basis_sigma),
            )
        )

    shape_p95 = [item["absolute_shape_relative_residual"]["p95"] for item in sample_results]
    sigma_p95 = [item["shape_residual_sigma_multiple"]["p95"] for item in sample_results]
    within_2 = [item["feature_fraction_at_or_below_2_sigma"] for item in sample_results]
    loads = [float(item["total_target_load"]) for item in sample_results]
    indices = [float(item["state_index"]) for item in sample_results]
    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "chart_basis_validation",
        "status": "ready_for_manual_branch_review",
        "model": {
            "branch": "B-B",
            "basis_interpolation": "piecewise_linear_normalized_columns_at_1024_2048_4095",
            "level_dependent_channels": list(CHANNELS),
        },
        "location_config_sha256": collection["location_config_sha256"],
        "sample_count": len(sample_results),
        "samples": sample_results,
        "aggregate": {
            "sample_shape_p95": _distribution_summary(shape_p95),
            "sample_shape_sigma_p95": _distribution_summary(sigma_p95),
            "sample_fraction_at_or_below_2_sigma": _distribution_summary(within_2),
            "shape_p95_correlation_with_total_load": _pearson(loads, shape_p95),
            "shape_p95_correlation_with_state_index": _pearson(indices, shape_p95),
            "by_category": _group_summary(sample_results, "category"),
            "by_active_set_size": _group_summary(sample_results, "active_set_size"),
        },
        "anchor_drift": _analyze_anchor_series(reports),
        "rejections": {"observation_count": len(rejected), "observations": rejected},
        "decision_hints": {
            "sample_fraction_with_at_least_80_percent_features_within_2_sigma": sum(value >= 0.8 for value in within_2) / len(within_2),
            "all_sample_sigma_p95_at_or_below_3": all(value <= 3.0 for value in sigma_p95),
            "automatic_branch_selection": False,
        },
        "notes": [
            "Predictions interpolate each normalized P2 channel column linearly between target codes 1024, 2048, and 4095.",
            "Imputed P2 cells contribute at reduced confidence and censored-zero cells contribute no residual weight.",
            "Sigma combines P3 repeat-center uncertainty with P2 basis-center uncertainty.",
            "Global-scale-removed shape residuals are reported separately from absolute response residuals.",
            "No M-A/M-B/M-C/M-D/M-E branch is selected automatically.",
        ],
    }


def predict_piecewise_basis(basis: Mapping[str, Any], command: Mapping[str, int]) -> dict[str, list[float]]:
    _validate_basis(basis)
    feature_count = len(basis["feature_order"])
    values = np.zeros(feature_count, dtype=float)
    variance = np.zeros(feature_count, dtype=float)
    confidence_numerator = np.zeros(feature_count, dtype=float)
    contribution_magnitude = np.zeros(feature_count, dtype=float)
    for channel_index, channel in enumerate(CHANNELS):
        code = int(command[channel])
        if code < 0 or code > 4095:
            raise ValueError(f"{channel} command is outside 0..4095")
        if code == 0:
            continue
        column, cell_weight, normalized_sigma = _interpolated_column(basis, channel, channel_index, code)
        fraction = code / 4095.0
        contribution = column * fraction
        values += contribution
        variance += np.square(normalized_sigma * fraction / math.sqrt(3.0))
        magnitude = np.abs(contribution)
        confidence_numerator += magnitude * cell_weight
        contribution_magnitude += magnitude
    confidence = np.divide(
        confidence_numerator,
        contribution_magnitude,
        out=np.zeros_like(confidence_numerator),
        where=contribution_magnitude > 0,
    )
    return {
        "values": values.tolist(),
        "confidence": confidence.tolist(),
        "basis_center_sigma": np.sqrt(variance).tolist(),
    }


def _interpolated_column(
    basis: Mapping[str, Any], channel: str, channel_index: int, code: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if code <= LEVEL_CODES[0]:
        left = right = LEVEL_CODES[0]
        t = 0.0
    elif code >= LEVEL_CODES[-1]:
        left = right = LEVEL_CODES[-1]
        t = 0.0
    else:
        left, right = next((a, b) for a, b in zip(LEVEL_CODES, LEVEL_CODES[1:]) if a <= code <= b)
        t = (code - left) / (right - left)
    left_basis = basis["basis_by_level"][str(left)]
    right_basis = basis["basis_by_level"][str(right)]
    left_column = np.asarray(left_basis["matrix"], dtype=float)[:, channel_index]
    right_column = np.asarray(right_basis["matrix"], dtype=float)[:, channel_index]
    left_weight = np.asarray(left_basis["cell_weights"], dtype=float)[:, channel_index]
    right_weight = np.asarray(right_basis["cell_weights"], dtype=float)[:, channel_index]
    column = left_column * (1.0 - t) + right_column * t
    weight = left_weight * (1.0 - t) + right_weight * t
    left_sigma = _normalized_sigma_column(basis, channel, left)
    right_sigma = _normalized_sigma_column(basis, channel, right)
    sigma = np.sqrt(np.square(left_sigma * (1.0 - t)) + np.square(right_sigma * t))
    return column, weight, sigma


def _normalized_sigma_column(basis: Mapping[str, Any], channel: str, level: int) -> np.ndarray:
    output: list[float] = []
    for feature in basis["feature_order"]:
        stat = basis["feature_statistics"][str(level)][channel][feature]
        if stat["mode"] == "direct":
            output.append(float(stat["standard_deviation"]) / (level / 4095.0))
            continue
        donors = [
            (candidate, basis["feature_statistics"][str(candidate)][channel][feature])
            for candidate in LEVEL_CODES
            if basis["feature_statistics"][str(candidate)][channel][feature]["mode"] == "direct"
        ]
        if donors:
            donor_level, donor = min(
                donors,
                key=lambda item: abs(
                    float(item[1]["normalized_center"]) - float(stat["normalized_center"])
                ),
            )
            output.append(float(donor["standard_deviation"]) / (donor_level / 4095.0))
        else:
            output.append(0.0)
    return np.asarray(output)


def _sample_result(
    context: Mapping[str, Any], *, feature_ids: Sequence[str], measured: np.ndarray,
    predicted: np.ndarray, weights: np.ndarray, sigma: np.ndarray,
    repeat_sigma: np.ndarray, basis_sigma: np.ndarray,
) -> dict[str, Any]:
    normalized_weights = weights / np.sum(weights)
    absolute_residual = measured - predicted
    relative_residual = absolute_residual / np.maximum(np.abs(predicted), 1e-12)
    scale = float(np.sum(weights * predicted * measured) / np.sum(weights * predicted * predicted))
    shape_residual = measured / np.maximum(scale * predicted, 1e-12) - 1.0
    sigma_multiple = np.divide(
        np.abs(measured - scale * predicted), sigma,
        out=np.full_like(sigma, np.nan), where=sigma > 0,
    )
    finite_sigma = sigma_multiple[np.isfinite(sigma_multiple)]
    plane_signed: dict[str, list[float]] = defaultdict(list)
    neutral: list[float] = []
    chromatic: list[float] = []
    for feature, residual in zip(feature_ids, shape_residual):
        patch, plane = feature.split("::", 1)
        plane_signed[plane].append(float(residual))
        (neutral if _is_neutral_patch(patch) else chromatic).append(abs(float(residual)))
    return {
        **dict(context),
        "active_set_size": len(context["active_set"]),
        "accepted_feature_count": len(feature_ids),
        "global_scale_measured_to_prediction": scale,
        "weighted_relative_rmse": float(math.sqrt(np.sum(normalized_weights * np.square(relative_residual)))),
        "weighted_shape_rmse": float(math.sqrt(np.sum(normalized_weights * np.square(shape_residual)))),
        "absolute_relative_residual": _distribution_summary(np.abs(relative_residual)),
        "absolute_shape_relative_residual": _distribution_summary(np.abs(shape_residual)),
        "shape_residual_sigma_multiple": _distribution_summary(finite_sigma),
        "feature_fraction_at_or_below_2_sigma": float(np.mean(finite_sigma <= 2.0)) if finite_sigma.size else 0.0,
        "feature_fraction_at_or_below_3_sigma": float(np.mean(finite_sigma <= 3.0)) if finite_sigma.size else 0.0,
        "repeat_center_sigma": _distribution_summary(repeat_sigma),
        "basis_center_sigma": _distribution_summary(basis_sigma),
        "neutral_patch_absolute_shape_residual": _distribution_summary(neutral),
        "chromatic_patch_absolute_shape_residual": _distribution_summary(chromatic),
        "signed_shape_residual_by_plane": {plane: _signed_summary(values) for plane, values in sorted(plane_signed.items())},
    }


def _validate_basis(basis: Mapping[str, Any]) -> None:
    if basis.get("analysis") != "chart_response_basis" or basis.get("status") != "ready_for_manual_branch_review":
        raise ValueError("invalid or incomplete P2 basis analysis")
    if basis.get("channels") != list(CHANNELS) or basis.get("level_codes") != list(LEVEL_CODES):
        raise ValueError("P2 basis channel or level contract mismatch")
    if not basis.get("feature_order") or not basis.get("feature_weights"):
        raise ValueError("P2 basis is missing features or feature weights")


def _analyze_anchor_series(reports: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    anchor_reports = [
        report
        for report in reports
        if _context(report, "purpose") in {"anchor_auto_exposure", "anchor_check"}
    ]
    if len(anchor_reports) < 2:
        return {"status": "unavailable", "report_count": len(anchor_reports)}
    collection = raw_observer_analysis.collect_patch_plane_features(anchor_reports)
    by_report: dict[str, dict[str, float]] = defaultdict(dict)
    for observation in collection["observations"]:
        if _observation_rejection_reason(observation) is None:
            by_report[str(observation["report_id"])][str(observation["feature_id"])] = float(
                observation["value"]
            )
    report_ids = [str(_context(report, "capture_id")) for report in anchor_reports]
    baseline_id = report_ids[0]
    baseline = by_report[baseline_id]
    comparisons: list[dict[str, Any]] = []
    for report_id in report_ids[1:]:
        common = sorted(set(baseline) & set(by_report[report_id]))
        if len(common) < 2:
            comparisons.append(
                {"report_id": report_id, "common_feature_count": len(common), "status": "insufficient_features"}
            )
            continue
        left = np.asarray([baseline[feature] for feature in common], dtype=float)
        right = np.asarray([by_report[report_id][feature] for feature in common], dtype=float)
        scale = float(np.median(right / left))
        shape = np.abs(right / (left * scale) - 1.0)
        comparisons.append(
            {
                "report_id": report_id,
                "common_feature_count": len(common),
                "status": "complete",
                "global_scale_to_baseline": scale,
                "absolute_shape_drift": _distribution_summary(shape),
            }
        )
    return {
        "status": "complete",
        "baseline_report_id": baseline_id,
        "report_ids": report_ids,
        "comparisons_to_baseline": comparisons,
    }


def _context(report: Mapping[str, Any], key: str) -> Any:
    context = report.get("analysis_context")
    return context.get(key) if isinstance(context, Mapping) else None


def _is_neutral_patch(patch: str) -> bool:
    try:
        return int(patch.rsplit("_", 1)[1]) >= 19
    except (IndexError, ValueError):
        return False


def _distribution_summary(values: Sequence[float] | np.ndarray) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    array = array[np.isfinite(array)]
    if not array.size:
        return {"count": 0, "p50": None, "p90": None, "p95": None, "max": None}
    p50, p90, p95 = np.percentile(array, (50, 90, 95))
    return {"count": int(array.size), "p50": float(p50), "p90": float(p90), "p95": float(p95), "max": float(np.max(array))}


def _signed_summary(values: Sequence[float]) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    return {"count": int(array.size), "mean": float(np.mean(array)), "median": float(np.median(array))}


def _pearson(left: Sequence[float], right: Sequence[float]) -> float | None:
    a = np.asarray(left, dtype=float)
    b = np.asarray(right, dtype=float)
    if a.size < 3 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def _group_summary(samples: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for sample in samples:
        grouped[str(sample[key])].append(float(sample["absolute_shape_relative_residual"]["p95"]))
    return {name: _distribution_summary(values) for name, values in sorted(grouped.items())}
