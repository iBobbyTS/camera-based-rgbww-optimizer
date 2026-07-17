from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Any, Mapping, Sequence

import numpy as np


MODEL_NAME = "cubic_origin_monotonic"
SCHEMA_VERSION = 1


def fit_response_candidate(
    reports: Sequence[Mapping[str, Any]],
    *,
    minimum_derivative: float = 0.05,
) -> dict[str, Any]:
    """Fit a candidate-only monotonic RAW response correction.

    The model is g(y)=y*(1+a*y+b*y^2). It is fitted only against
    global-scale-removed exposure shape residuals and is never applied to the
    retained RAW reports or observer configuration.
    """

    if minimum_derivative <= 0:
        raise ValueError("minimum_derivative must be positive")
    _validate_training_reports(reports)

    best = (0.0, 0.0)
    best_key = _candidate_key(reports, *best, minimum_derivative=minimum_derivative)
    center_a = center_b = 0.0
    half_width = 4.0
    for _ in range(6):
        for a in np.linspace(center_a - half_width, center_a + half_width, 17):
            for b in np.linspace(center_b - half_width, center_b + half_width, 17):
                key = _candidate_key(
                    reports,
                    float(a),
                    float(b),
                    minimum_derivative=minimum_derivative,
                )
                if key is not None and (best_key is None or key < best_key):
                    best = (float(a), float(b))
                    best_key = key
        center_a, center_b = best
        half_width /= 4.0

    if best_key is None:
        raise ValueError("no monotonic response candidate could be fitted")
    a, b = best
    identity = evaluate_response_model(reports, a=0.0, b=0.0)
    corrected = evaluate_response_model(reports, a=a, b=b)
    lower_envelope = evaluate_response_model(reports, a=0.0, b=0.0, maximum_factor=1.0)
    derivative_minimum = response_derivative_minimum(a=a, b=b)
    signal_values = _training_signal_values(reports)

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "candidate_only_waiting_for_cross_day_holdout",
        "analysis": "raw_response_candidate",
        "input_sha256": _reports_sha256(reports),
        "model": {
            "name": MODEL_NAME,
            "formula": "g(y)=y*(1+a*y+b*y^2)",
            "coefficients": {"a": a, "b": b},
            "constraints": {
                "g_at_zero": 0.0,
                "minimum_derivative_required": float(minimum_derivative),
                "minimum_derivative_observed_on_0_to_1": derivative_minimum,
            },
            "training_range": {
                "minimum_black_corrected_normalized_trimmed_mean": min(signal_values),
                "maximum_black_corrected_normalized_trimmed_mean": max(signal_values),
            },
            "application_range": {
                "minimum_black_corrected_normalized_trimmed_mean": 0.0,
                "maximum_black_corrected_normalized_trimmed_mean": max(signal_values),
            },
            "out_of_range_policy": "reject_outside_training_range",
        },
        "comparisons": {
            "identity_full_envelope": identity,
            "candidate_full_envelope": corrected,
            "identity_lower_envelope_factor_lte_1": lower_envelope,
        },
        "notes": [
            "This artifact does not modify native RAW values or raw-observer.json.",
            "A complete P1 run from another natural day is required as holdout before proposing installation.",
            "The lower-envelope comparison changes the accepted exposure range and is not a substitute for holdout.",
        ],
    }


def evaluate_holdout(
    reports: Sequence[Mapping[str, Any]],
    candidate: Mapping[str, Any],
    *,
    repeatability_reports: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate frozen coefficients on independent reports without refitting."""

    _validate_training_reports(reports)
    if repeatability_reports is not None:
        _validate_training_reports(repeatability_reports)
        if _location_sha256(repeatability_reports) != _location_sha256(reports):
            raise ValueError("holdout and repeatability reports use different location_config.sha256 values")
    model = candidate.get("model")
    coefficients = model.get("coefficients") if isinstance(model, Mapping) else None
    application_range = model.get("application_range") if isinstance(model, Mapping) else None
    if not isinstance(coefficients, Mapping) or not isinstance(application_range, Mapping):
        raise ValueError("candidate has no supported model coefficients or application range")
    if model.get("name") != MODEL_NAME:
        raise ValueError(f"unsupported response model: {model.get('name')}")
    a = float(coefficients["a"])
    b = float(coefficients["b"])
    holdout_sha256 = _reports_sha256(reports)
    if holdout_sha256 == candidate.get("input_sha256"):
        raise ValueError("holdout reports are identical to the candidate training input")

    signal_values = _training_signal_values(reports)
    minimum = float(application_range["minimum_black_corrected_normalized_trimmed_mean"])
    maximum = float(application_range["maximum_black_corrected_normalized_trimmed_mean"])
    outside = [value for value in signal_values if value < minimum or value > maximum]
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "analysis": "raw_response_candidate_holdout",
        "candidate_input_sha256": candidate.get("input_sha256"),
        "holdout_input_sha256": holdout_sha256,
        "repeatability_input_sha256": _reports_sha256(repeatability_reports or reports),
        "model": dict(model),
        "holdout_signal_range": {
            "minimum_black_corrected_normalized_trimmed_mean": min(signal_values),
            "maximum_black_corrected_normalized_trimmed_mean": max(signal_values),
            "outside_application_range_count": len(outside),
        },
        "identity_full_envelope": evaluate_response_model(
            reports,
            a=0.0,
            b=0.0,
            repeatability_reports=repeatability_reports,
        ),
    }
    if outside:
        result["status"] = "rejected_outside_candidate_application_range"
        result["candidate_full_envelope"] = None
    else:
        result["status"] = "holdout_ready_for_manual_branch_review"
        result["candidate_full_envelope"] = evaluate_response_model(
            reports,
            a=a,
            b=b,
            repeatability_reports=repeatability_reports,
        )
    return result


def evaluate_response_model(
    reports: Sequence[Mapping[str, Any]],
    *,
    a: float,
    b: float,
    maximum_factor: float | None = None,
    repeatability_reports: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    _validate_training_reports(reports)
    centers, repeatability = _collect_centers(reports, a=a, b=b)
    if repeatability_reports is not None:
        _unused_centers, repeatability = _collect_centers(repeatability_reports, a=a, b=b)
    residuals: list[float] = []
    sigma_values: list[float] = []
    by_source: dict[str, dict[str, Any]] = {}

    for source, source_centers in centers.items():
        factors = sorted(source_centers)
        if maximum_factor is not None:
            factors = [factor for factor in factors if factor <= maximum_factor]
        reference_factor = min(factors, key=lambda factor: abs(factor - 1.0))
        if abs(reference_factor - 1.0) > 1e-9:
            raise ValueError(f"source {source} has no 1.0 reference exposure factor")
        source_residuals: list[float] = []
        source_sigmas: list[float] = []
        residuals_by_plane: dict[str, list[float]] = defaultdict(list)
        sigmas_by_plane: dict[str, list[float]] = defaultdict(list)
        residuals_by_factor: dict[str, list[float]] = defaultdict(list)
        sigmas_by_factor: dict[str, list[float]] = defaultdict(list)
        feature_diagnostics: list[dict[str, Any]] = []
        reference = source_centers[reference_factor]
        for factor in factors:
            if factor == reference_factor:
                continue
            ratios = {
                feature_id: value / reference[feature_id]
                for feature_id, value in source_centers[factor].items()
                if feature_id in reference and value > 0 and reference[feature_id] > 0
            }
            if not ratios:
                continue
            global_scale = float(np.median(list(ratios.values())))
            for feature_id, ratio in ratios.items():
                patch_name, plane = feature_id.rsplit("::", 1)
                shape = ratio / global_scale - 1.0
                absolute_shape = abs(shape)
                residuals.append(absolute_shape)
                source_residuals.append(absolute_shape)
                residuals_by_plane[plane].append(absolute_shape)
                residuals_by_factor[str(factor)].append(absolute_shape)
                cv = repeatability.get(source, {}).get(feature_id)
                sigma = None
                if cv is not None and cv > 0:
                    sigma = absolute_shape / cv
                    sigma_values.append(sigma)
                    source_sigmas.append(sigma)
                    sigmas_by_plane[plane].append(sigma)
                    sigmas_by_factor[str(factor)].append(sigma)
                feature_diagnostics.append(
                    {
                        "feature_id": feature_id,
                        "patch_name": patch_name,
                        "plane": plane,
                        "factor": factor,
                        "absolute_shape_relative_residual": absolute_shape,
                        "shape_residual_repeatability_sigma": sigma,
                    }
                )
        by_source[source] = {
            "absolute_shape_relative_residual_non_reference": _distribution(source_residuals),
            "shape_residual_repeatability_sigma_non_reference": _distribution(source_sigmas),
            "by_plane": {
                plane: {
                    "absolute_shape_relative_residual_non_reference": _distribution(values),
                    "shape_residual_repeatability_sigma_non_reference": _distribution(
                        sigmas_by_plane.get(plane, [])
                    ),
                }
                for plane, values in sorted(residuals_by_plane.items())
            },
            "by_factor": {
                factor: {
                    "absolute_shape_relative_residual_non_reference": _distribution(values),
                    "shape_residual_repeatability_sigma_non_reference": _distribution(
                        sigmas_by_factor.get(factor, [])
                    ),
                }
                for factor, values in sorted(residuals_by_factor.items(), key=lambda item: float(item[0]))
            },
            "worst_features_by_repeatability_sigma": sorted(
                feature_diagnostics,
                key=lambda item: (
                    -1.0
                    if item["shape_residual_repeatability_sigma"] is None
                    else float(item["shape_residual_repeatability_sigma"])
                ),
                reverse=True,
            )[:20],
        }

    if not residuals:
        raise ValueError("reports do not contain comparable non-reference exposure factors")
    return {
        "maximum_factor": maximum_factor,
        "sources": by_source,
        "summary": {
            "absolute_shape_relative_residual_non_reference": _distribution(residuals),
            "shape_residual_repeatability_sigma_non_reference": _distribution(sigma_values),
        },
    }


def apply_response_model(value: float, *, a: float, b: float) -> float:
    y = float(value)
    return y * (1.0 + a * y + b * y * y)


def response_derivative_minimum(*, a: float, b: float) -> float:
    points = [0.0, 1.0]
    if b != 0:
        vertex = -a / (3.0 * b)
        if 0.0 < vertex < 1.0:
            points.append(vertex)
    return min(1.0 + 2.0 * a * y + 3.0 * b * y * y for y in points)


def _candidate_key(
    reports: Sequence[Mapping[str, Any]],
    a: float,
    b: float,
    *,
    minimum_derivative: float,
) -> tuple[float, float, float, float] | None:
    if response_derivative_minimum(a=a, b=b) < minimum_derivative:
        return None
    evaluation = evaluate_response_model(reports, a=a, b=b)
    distribution = evaluation["summary"]["absolute_shape_relative_residual_non_reference"]
    p95 = float(distribution["p95"])
    maximum = float(distribution["max"])
    return (p95 + 0.1 * maximum, p95, maximum, abs(a) + abs(b))


def _collect_centers(
    reports: Sequence[Mapping[str, Any]],
    *,
    a: float,
    b: float,
) -> tuple[dict[str, dict[float, dict[str, float]]], dict[str, dict[str, float]]]:
    linearity: dict[tuple[str, float, str], list[float]] = defaultdict(list)
    repeats: dict[tuple[str, str], list[float]] = defaultdict(list)
    for report in reports:
        context = report.get("analysis_context")
        if not isinstance(context, Mapping):
            continue
        source = str(context.get("source"))
        purpose = str(context.get("purpose"))
        if purpose not in {"linearity_bracket", "paired_repeat"}:
            continue
        exposure = _positive_float(context.get("exposure_seconds"), "exposure_seconds")
        ambient_exposure = _ambient_exposure_seconds(report)
        ambient_by_feature = _ambient_values(report)
        for patch in report.get("patches", []):
            if not isinstance(patch, Mapping) or not bool(patch.get("optimization_eligible")):
                continue
            patch_name = str(patch.get("name"))
            planes = patch.get("planes")
            if not isinstance(planes, Mapping):
                continue
            for plane_name, plane in planes.items():
                if not isinstance(plane, Mapping) or not _plane_is_usable(plane):
                    continue
                feature_id = f"{patch_name}::{plane_name}"
                signal = _trimmed_signal(plane)
                ambient = ambient_by_feature.get(feature_id)
                if signal is None or ambient is None:
                    continue
                rate = apply_response_model(signal, a=a, b=b) / exposure
                rate -= apply_response_model(ambient, a=a, b=b) / ambient_exposure
                if not np.isfinite(rate) or rate <= 0:
                    continue
                if purpose == "linearity_bracket":
                    factor = _positive_float(context.get("exposure_factor"), "exposure_factor")
                    linearity[(source, factor, feature_id)].append(rate)
                elif purpose == "paired_repeat":
                    repeats[(source, feature_id)].append(rate)

    centers: dict[str, dict[float, dict[str, float]]] = defaultdict(lambda: defaultdict(dict))
    for (source, factor, feature_id), values in linearity.items():
        centers[source][factor][feature_id] = float(np.median(values))
    repeatability: dict[str, dict[str, float]] = defaultdict(dict)
    for (source, feature_id), values in repeats.items():
        if len(values) < 2:
            continue
        mean = float(np.mean(values))
        if mean > 0:
            repeatability[source][feature_id] = float(np.std(values, ddof=1) / mean)
    return {source: dict(groups) for source, groups in centers.items()}, dict(repeatability)


def _ambient_values(report: Mapping[str, Any]) -> dict[str, float]:
    ambient = report.get("ambient_reference")
    if not isinstance(ambient, Mapping):
        raise ValueError("report has no ambient_reference")
    values: dict[str, float] = {}
    for patch in ambient.get("patches", []):
        if not isinstance(patch, Mapping):
            continue
        patch_name = str(patch.get("name"))
        planes = patch.get("planes")
        if not isinstance(planes, Mapping):
            continue
        for plane_name, plane in planes.items():
            if isinstance(plane, Mapping):
                value = _trimmed_signal(plane)
                if value is not None:
                    values[f"{patch_name}::{plane_name}"] = value
    return values


def _ambient_exposure_seconds(report: Mapping[str, Any]) -> float:
    metadata = report.get("ambient_exposure_metadata")
    if isinstance(metadata, Mapping) and metadata.get("seconds") is not None:
        return _positive_float(metadata["seconds"], "ambient exposure seconds")
    ambient = report.get("ambient_reference")
    if isinstance(ambient, Mapping):
        return _positive_float(ambient.get("exposure_seconds"), "ambient exposure seconds")
    raise ValueError("report has no ambient exposure provenance")


def _trimmed_signal(plane: Mapping[str, Any]) -> float | None:
    statistics = plane.get("statistics")
    normalized = statistics.get("black_corrected_normalized") if isinstance(statistics, Mapping) else None
    value = normalized.get("trimmed_mean") if isinstance(normalized, Mapping) else None
    if not isinstance(value, (int, float)) or not np.isfinite(value):
        return None
    return float(value)


def _plane_is_usable(plane: Mapping[str, Any]) -> bool:
    metrics = plane.get("metrics")
    if not isinstance(metrics, Mapping):
        return False
    clipped = metrics.get("clipped_fraction")
    return isinstance(clipped, (int, float)) and float(clipped) == 0.0


def _training_signal_values(reports: Sequence[Mapping[str, Any]]) -> list[float]:
    values: list[float] = []
    for report in reports:
        context = report.get("analysis_context")
        if not isinstance(context, Mapping) or context.get("purpose") != "linearity_bracket":
            continue
        for patch in report.get("patches", []):
            if not isinstance(patch, Mapping) or not bool(patch.get("optimization_eligible")):
                continue
            planes = patch.get("planes")
            if not isinstance(planes, Mapping):
                continue
            for plane in planes.values():
                if isinstance(plane, Mapping) and _plane_is_usable(plane):
                    value = _trimmed_signal(plane)
                    if value is not None:
                        values.append(value)
    if not values:
        raise ValueError("reports contain no usable linearity signal values")
    return values


def _validate_training_reports(reports: Sequence[Mapping[str, Any]]) -> None:
    if not reports:
        raise ValueError("at least one report is required")
    _location_sha256(reports)
    statuses = {
        report.get("analysis_context", {}).get("exposure_status")
        for report in reports
        if isinstance(report.get("analysis_context"), Mapping)
        and report.get("analysis_context", {}).get("source") != "ambient"
    }
    if statuses != {"recorded"}:
        raise ValueError("all signal reports require recorded exposure provenance")


def _location_sha256(reports: Sequence[Mapping[str, Any]]) -> str:
    locations = {
        report.get("location_config", {}).get("sha256")
        for report in reports
        if isinstance(report.get("location_config"), Mapping)
    }
    if len(locations) != 1 or None in locations:
        raise ValueError("reports must share one explicit location_config.sha256")
    return str(next(iter(locations)))


def _reports_sha256(reports: Sequence[Mapping[str, Any]]) -> str:
    evidence = []
    for report in reports:
        source = report.get("source")
        context = report.get("analysis_context")
        evidence.append(
            {
                "source_sha256": source.get("sha256") if isinstance(source, Mapping) else None,
                "capture_id": context.get("capture_id") if isinstance(context, Mapping) else None,
                "exposure_seconds": context.get("exposure_seconds") if isinstance(context, Mapping) else None,
            }
        )
    payload = json.dumps(evidence, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _positive_float(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or not np.isfinite(value) or float(value) <= 0:
        raise ValueError(f"{label} must be a positive finite number")
    return float(value)


def _distribution(values: Sequence[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "p50": None, "p90": None, "p95": None, "max": None}
    array = np.asarray(values, dtype=np.float64)
    return {
        "count": int(array.size),
        "p50": float(np.percentile(array, 50)),
        "p90": float(np.percentile(array, 90)),
        "p95": float(np.percentile(array, 95)),
        "max": float(np.max(array)),
    }
