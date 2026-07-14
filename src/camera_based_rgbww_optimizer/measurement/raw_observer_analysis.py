from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


DEFAULT_STATISTIC = "ambient_subtracted.trimmed_mean_per_second"
SCHEMA_VERSION = 1


def collect_patch_plane_features(
    reports: Sequence[Mapping[str, Any]],
    *,
    statistic: str = DEFAULT_STATISTIC,
    include_diagnostic: bool = False,
) -> dict[str, Any]:
    """Collect one explicitly selected statistic per native-Bayer patch and plane.

    The default deliberately requires ambient-subtracted values. A missing value is
    preserved as an observation issue rather than falling back to an uncorrected
    statistic, because that fallback would mix different measurement conditions.
    """

    if not reports:
        raise ValueError("at least one raw observer report is required")
    statistic_path = _parse_statistic_path(statistic)
    expected_location_hash: str | None = None
    expected_plane_order: tuple[str, ...] | None = None
    expected_patch_signature: tuple[tuple[str, bool], ...] | None = None
    observations: list[dict[str, Any]] = []

    for report_index, report in enumerate(reports):
        _validate_report_schema(report, report_index)
        report_id = _report_id(report, report_index)
        location_hash = _location_hash(report, report_index)
        plane_order = _plane_order(report, report_index)
        patch_signature = _patch_signature(report, report_index)
        if expected_location_hash is None:
            expected_location_hash = location_hash
            expected_plane_order = plane_order
            expected_patch_signature = patch_signature
        else:
            if location_hash != expected_location_hash:
                raise ValueError("raw observer reports use different location_config.sha256 values")
            if plane_order != expected_plane_order:
                raise ValueError("raw observer reports use different mosaic plane_order values")
            if patch_signature != expected_patch_signature:
                raise ValueError("raw observer reports use different patch names or optimization eligibility")

        for patch in report["patches"]:
            if not include_diagnostic and not bool(patch["optimization_eligible"]):
                continue
            patch_name = str(patch["name"])
            planes = patch["planes"]
            if set(planes) != set(plane_order):
                raise ValueError(f"report {report_id} patch {patch_name} does not contain the expected CFA planes")
            for plane in plane_order:
                plane_report = planes[plane]
                value = _nested_value(plane_report, statistic_path)
                status = "included"
                numeric_value: float | None = None
                if value is None:
                    status = "missing_statistic"
                else:
                    numeric_value = _finite_float(value)
                    if numeric_value is None:
                        status = "nonfinite_statistic"
                observations.append(
                    {
                        "feature_id": _feature_id(patch_name, plane),
                        "report_id": report_id,
                        "report_index": report_index,
                        "patch_name": patch_name,
                        "plane": plane,
                        "value": numeric_value,
                        "status": status,
                        "quality_status": str(plane_report["quality"]["status"]),
                        "metrics": _plane_metrics(plane_report),
                        "analysis_context": _analysis_context(report),
                    }
                )

    return {
        "schema_version": SCHEMA_VERSION,
        "statistic": statistic,
        "report_count": len(reports),
        "location_config_sha256": expected_location_hash,
        "plane_order": list(expected_plane_order or ()),
        "patch_signature": [
            {"name": name, "optimization_eligible": optimization_eligible}
            for name, optimization_eligible in (expected_patch_signature or ())
        ],
        "observations": observations,
        "included_observation_count": sum(item["status"] == "included" for item in observations),
        "missing_statistic_count": sum(item["status"] == "missing_statistic" for item in observations),
        "nonfinite_statistic_count": sum(item["status"] == "nonfinite_statistic" for item in observations),
    }


def analyze_repeatability(
    reports: Sequence[Mapping[str, Any]],
    *,
    statistic: str = DEFAULT_STATISTIC,
    include_diagnostic: bool = False,
) -> dict[str, Any]:
    """Describe per-patch, per-plane repeatability without deciding a pass threshold."""

    collection = collect_patch_plane_features(
        reports,
        statistic=statistic,
        include_diagnostic=include_diagnostic,
    )
    features: dict[str, dict[str, Any]] = {}
    for feature_id, observations in _observations_by_feature(collection["observations"]).items():
        values = [float(item["value"]) for item in observations if item["status"] == "included"]
        first = observations[0]
        features[feature_id] = {
            "patch_name": first["patch_name"],
            "plane": first["plane"],
            "report_ids": [item["report_id"] for item in observations if item["status"] == "included"],
            **_distribution_summary(values),
            "missing_observation_count": sum(item["status"] != "included" for item in observations),
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "raw_observer_repeatability",
        "collection": collection,
        "features": features,
        "summary": {
            "feature_count": len(features),
            "complete_feature_count": sum(item["count"] >= 2 for item in features.values()),
            "standard_deviation": _percentile_summary(
                item["standard_deviation"] for item in features.values()
            ),
            "coefficient_of_variation": _percentile_summary(
                item["coefficient_of_variation"] for item in features.values()
            ),
            "p95_range": _percentile_summary(item["p95_range"] for item in features.values()),
        },
    }


def analyze_exposure_linearity(
    exposure_groups: Mapping[float | str, Sequence[Mapping[str, Any]]],
    repeatability: Mapping[str, Any] | None = None,
    *,
    statistic: str = DEFAULT_STATISTIC,
    include_diagnostic: bool = False,
) -> dict[str, Any]:
    """Compare exposure-normalized feature centers across explicit exposure factors.

    The returned sigma multiples are derived only from the supplied repeatability
    analysis. This function intentionally does not embed a project pass/fail
    multiplier; the P1 evidence determines that policy.
    """

    if len(exposure_groups) < 2:
        raise ValueError("at least two exposure groups are required")
    collections: dict[float, dict[str, Any]] = {}
    for raw_factor, reports in exposure_groups.items():
        factor = _positive_factor(raw_factor)
        if factor in collections:
            raise ValueError(f"duplicate exposure factor: {factor}")
        collections[factor] = collect_patch_plane_features(
            reports,
            statistic=statistic,
            include_diagnostic=include_diagnostic,
        )
    _validate_group_collections(collections)

    factors = sorted(collections)
    by_factor = {
        factor: _observations_by_feature(collections[factor]["observations"])
        for factor in factors
    }
    feature_ids = sorted({feature_id for groups in by_factor.values() for feature_id in groups})
    features: dict[str, dict[str, Any]] = {}
    for feature_id in feature_ids:
        sample = next(
            observations[feature_id][0]
            for observations in by_factor.values()
            if feature_id in observations
        )
        centers: list[dict[str, Any]] = []
        for factor in factors:
            observations = by_factor[factor].get(feature_id, [])
            values = [float(item["value"]) for item in observations if item["status"] == "included"]
            centers.append(
                {
                    "factor": factor,
                    "count": len(values),
                    "center": _median_or_none(values),
                    "report_ids": [item["report_id"] for item in observations if item["status"] == "included"],
                }
            )
        available = [item for item in centers if item["center"] is not None]
        reference = min(available, key=lambda item: abs(math.log(float(item["factor"])))) if available else None
        reference_value = None if reference is None else float(reference["center"])
        noise_sigma = _repeatability_sigma(repeatability, feature_id)
        for item in centers:
            center = item["center"]
            if center is None or reference_value is None:
                item["relative_residual"] = None
                item["residual_repeatability_sigma"] = None
            else:
                difference = float(center) - reference_value
                item["relative_residual"] = None if reference_value == 0 else difference / abs(reference_value)
                item["residual_repeatability_sigma"] = _sigma_multiple(difference, noise_sigma)
        normalized_centers = [float(item["center"]) / reference_value for item in available] if reference_value else []
        slope = (
            float(np.polyfit(np.log([item["factor"] for item in available]), normalized_centers, 1)[0])
            if len(available) >= 2 and reference_value not in (None, 0.0)
            else None
        )
        features[feature_id] = {
            "patch_name": sample["patch_name"],
            "plane": sample["plane"],
            "status": "complete" if len(available) == len(factors) else "incomplete",
            "reference_factor": None if reference is None else reference["factor"],
            "reference_center": reference_value,
            "repeatability_sigma": noise_sigma,
            "centers": centers,
            "slope_per_log_exposure_factor": slope,
            "monotonic_drift": _monotonic_drift(available, noise_sigma),
        }

    residuals = [
        abs(float(center["relative_residual"]))
        for feature in features.values()
        for center in feature["centers"]
        if center["relative_residual"] is not None
    ]
    sigma_multiples = [
        float(center["residual_repeatability_sigma"])
        for feature in features.values()
        for center in feature["centers"]
        if center["residual_repeatability_sigma"] is not None
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "raw_observer_exposure_linearity",
        "statistic": statistic,
        "factors": factors,
        "collections": {str(factor): collection for factor, collection in collections.items()},
        "features": features,
        "summary": {
            "feature_count": len(features),
            "complete_feature_count": sum(item["status"] == "complete" for item in features.values()),
            "absolute_relative_residual": _percentile_summary(residuals),
            "residual_repeatability_sigma": _percentile_summary(sigma_multiples),
        },
    }


def analyze_green_consistency(
    reports: Sequence[Mapping[str, Any]],
    *,
    statistic: str = DEFAULT_STATISTIC,
    include_diagnostic: bool = False,
) -> dict[str, Any]:
    """Report G1/G2 ratios and differences while preserving capture provenance."""

    collection = collect_patch_plane_features(
        reports,
        statistic=statistic,
        include_diagnostic=include_diagnostic,
    )
    by_report_patch: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for observation in collection["observations"]:
        by_report_patch[(observation["report_id"], observation["patch_name"])][observation["plane"]] = observation

    observations: list[dict[str, Any]] = []
    for (report_id, patch_name), planes in sorted(by_report_patch.items()):
        g1 = planes.get("G1")
        g2 = planes.get("G2")
        if g1 is None or g2 is None or g1["status"] != "included" or g2["status"] != "included":
            observations.append(
                {
                    "report_id": report_id,
                    "patch_name": patch_name,
                    "status": "missing_green_statistic",
                    "g1": None if g1 is None else g1["value"],
                    "g2": None if g2 is None else g2["value"],
                }
            )
            continue
        g1_value = float(g1["value"])
        g2_value = float(g2["value"])
        mean_absolute = (abs(g1_value) + abs(g2_value)) / 2.0
        observations.append(
            {
                "report_id": report_id,
                "patch_name": patch_name,
                "status": "included",
                "g1": g1_value,
                "g2": g2_value,
                "g1_to_g2_ratio": None if g2_value == 0 else g1_value / g2_value,
                "relative_difference": None if mean_absolute == 0 else (g1_value - g2_value) / mean_absolute,
                "analysis_context": g1["analysis_context"],
            }
        )

    patches: dict[str, dict[str, Any]] = {}
    for patch_name in sorted({item["patch_name"] for item in observations}):
        patch_observations = [item for item in observations if item["patch_name"] == patch_name]
        ratios = [item["g1_to_g2_ratio"] for item in patch_observations if item["status"] == "included"]
        differences = [item["relative_difference"] for item in patch_observations if item["status"] == "included"]
        patches[patch_name] = {
            "ratio": _distribution_summary([float(value) for value in ratios if value is not None]),
            "relative_difference": _distribution_summary(
                [float(value) for value in differences if value is not None]
            ),
            "missing_observation_count": sum(item["status"] != "included" for item in patch_observations),
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "raw_observer_green_consistency",
        "collection": collection,
        "observations": observations,
        "patches": patches,
        "summary": {
            "patch_count": len(patches),
            "absolute_relative_difference": _percentile_summary(
                abs(float(item["relative_difference"]))
                for item in observations
                if item["status"] == "included" and item["relative_difference"] is not None
            ),
        },
    }


def recommend_quality_thresholds(
    reports: Sequence[Mapping[str, Any]],
    *,
    accepted_report_ids: Sequence[str] | None = None,
    statistic: str = DEFAULT_STATISTIC,
) -> dict[str, Any]:
    """Produce a review-only candidate threshold set from explicitly approved data.

    The caller must supply report IDs already justified by repeatability and
    linearity evidence. This function never treats `pending_thresholds` reports
    as independently accepted and never writes the observer configuration.
    """

    collection = collect_patch_plane_features(reports, statistic=statistic)
    known_ids = {str(item["report_id"]) for item in collection["observations"]}
    if accepted_report_ids is None:
        return {
            "schema_version": SCHEMA_VERSION,
            "analysis": "raw_observer_quality_threshold_recommendation",
            "status": "requires_explicit_accepted_report_ids",
            "collection": collection,
            "candidate_quality_thresholds": None,
            "reason": "No threshold is inferred until the caller explicitly selects measurement runs supported by repeatability and linearity evidence.",
        }
    selected_ids = {str(value) for value in accepted_report_ids}
    unknown_ids = sorted(selected_ids - known_ids)
    if unknown_ids:
        raise ValueError(f"accepted_report_ids are not present in the supplied reports: {unknown_ids}")
    selected = [
        item
        for item in collection["observations"]
        if item["report_id"] in selected_ids
        and item["status"] == "included"
        and item["quality_status"] != "rejected"
    ]
    if not selected:
        return {
            "schema_version": SCHEMA_VERSION,
            "analysis": "raw_observer_quality_threshold_recommendation",
            "status": "insufficient_usable_observations",
            "collection": collection,
            "selected_report_ids": sorted(selected_ids),
            "candidate_quality_thresholds": None,
        }
    metric_values = {
        metric: [float(item["metrics"][metric]) for item in selected if item["metrics"][metric] is not None]
        for metric in ("nonfinite_fraction", "clipped_fraction", "near_noise_floor_fraction")
    }
    valid_pixels = [int(item["metrics"]["valid_pixel_count"]) for item in selected]
    if any(not values for values in metric_values.values()) or not valid_pixels:
        raise ValueError("selected reports are missing quality metrics required for a threshold recommendation")
    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": "raw_observer_quality_threshold_recommendation",
        "status": "candidate_only",
        "collection": collection,
        "selected_report_ids": sorted(selected_ids),
        "candidate_quality_thresholds": {
            "minimum_valid_pixels_per_plane": min(valid_pixels),
            "maximum_nonfinite_fraction": max(metric_values["nonfinite_fraction"]),
            "maximum_clipped_fraction": max(metric_values["clipped_fraction"]),
            "maximum_near_noise_floor_fraction": max(metric_values["near_noise_floor_fraction"]),
        },
        "evidence": {
            "selected_observation_count": len(selected),
            "observed_metric_ranges": {
                metric: {"min": min(values), "max": max(values)} for metric, values in metric_values.items()
            },
            "valid_pixel_count": {"min": min(valid_pixels), "max": max(valid_pixels)},
            "review_required": "Merge this candidate manually only after documenting which repeatability and linearity decision selected these report IDs.",
        },
    }


def write_analysis_json(path: str | Path, analysis: Mapping[str, Any]) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def _validate_report_schema(report: Mapping[str, Any], report_index: int) -> None:
    if not isinstance(report, Mapping):
        raise ValueError(f"report {report_index} must be an object")
    if int(report.get("schema_version", -1)) != 1:
        raise ValueError(f"report {report_index} must use raw observer schema_version 1")
    if report.get("measurement") != "native_bayer_patch_statistics":
        raise ValueError(f"report {report_index} is not a native Bayer patch statistics report")
    if not isinstance(report.get("patches"), Sequence) or isinstance(report.get("patches"), (str, bytes)):
        raise ValueError(f"report {report_index} patches must be an array")


def _location_hash(report: Mapping[str, Any], report_index: int) -> str:
    location = report.get("location_config")
    if not isinstance(location, Mapping) or not isinstance(location.get("sha256"), str) or not location["sha256"]:
        raise ValueError(f"report {report_index} is missing location_config.sha256")
    return str(location["sha256"])


def _plane_order(report: Mapping[str, Any], report_index: int) -> tuple[str, ...]:
    mosaic = report.get("mosaic")
    values = mosaic.get("plane_order") if isinstance(mosaic, Mapping) else None
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"report {report_index} is missing mosaic.plane_order")
    plane_order = tuple(str(value) for value in values)
    if not plane_order or len(set(plane_order)) != len(plane_order):
        raise ValueError(f"report {report_index} mosaic.plane_order must contain unique labels")
    return plane_order


def _patch_signature(report: Mapping[str, Any], report_index: int) -> tuple[tuple[str, bool], ...]:
    signature: list[tuple[str, bool]] = []
    for patch in report["patches"]:
        if not isinstance(patch, Mapping) or not isinstance(patch.get("name"), str):
            raise ValueError(f"report {report_index} contains an invalid patch")
        if not isinstance(patch.get("planes"), Mapping):
            raise ValueError(f"report {report_index} patch {patch['name']} is missing planes")
        signature.append((str(patch["name"]), bool(patch.get("optimization_eligible"))))
    if len({name for name, _ in signature}) != len(signature):
        raise ValueError(f"report {report_index} contains duplicate patch names")
    return tuple(signature)


def _parse_statistic_path(statistic: str) -> tuple[str, ...]:
    parts = tuple(part.strip() for part in statistic.split(".") if part.strip())
    if not parts:
        raise ValueError("statistic must be a dotted path")
    return parts


def _nested_value(value: Mapping[str, Any], path: Sequence[str]) -> Any:
    current: Any = value
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return None
        current = current[key]
    return current


def _report_id(report: Mapping[str, Any], report_index: int) -> str:
    for container in (report, report.get("analysis_context"), report.get("source")):
        if isinstance(container, Mapping):
            for key in ("report_id", "capture_id", "sha256", "path"):
                value = container.get(key)
                if isinstance(value, str) and value:
                    return value
    return f"report-{report_index:04d}"


def _analysis_context(report: Mapping[str, Any]) -> dict[str, Any]:
    context = report.get("analysis_context")
    return dict(context) if isinstance(context, Mapping) else {}


def _plane_metrics(plane_report: Mapping[str, Any]) -> dict[str, Any]:
    metrics = plane_report.get("metrics")
    quality = plane_report.get("quality")
    if not isinstance(metrics, Mapping) or not isinstance(quality, Mapping) or "status" not in quality:
        raise ValueError("raw observer plane is missing metrics or quality.status")
    required = (
        "valid_pixel_count",
        "nonfinite_fraction",
        "clipped_fraction",
        "near_noise_floor_fraction",
    )
    if any(name not in metrics for name in required):
        raise ValueError("raw observer plane metrics are incomplete")
    return {name: metrics[name] for name in required}


def _feature_id(patch_name: str, plane: str) -> str:
    return f"{patch_name}::{plane}"


def _finite_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _observations_by_feature(observations: Sequence[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for observation in observations:
        grouped[str(observation["feature_id"])].append(dict(observation))
    return dict(grouped)


def _distribution_summary(values: Sequence[float]) -> dict[str, Any]:
    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "mad": None,
            "standard_deviation": None,
            "coefficient_of_variation": None,
            "p95_range": None,
        }
    array = np.asarray(values, dtype="float64")
    median = float(np.median(array))
    mad = float(np.median(np.abs(array - median)))
    standard_deviation = float(np.std(array, ddof=1)) if array.size >= 2 else None
    mean = float(np.mean(array))
    p05, p95 = np.percentile(array, [5, 95])
    return {
        "count": int(array.size),
        "mean": mean,
        "median": median,
        "mad": mad,
        "standard_deviation": standard_deviation,
        "coefficient_of_variation": (
            None if standard_deviation is None or mean == 0 else standard_deviation / abs(mean)
        ),
        "p95_range": float(p95 - p05),
    }


def _percentile_summary(values: Sequence[float | None] | Any) -> dict[str, Any]:
    finite = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    if not finite:
        return {"count": 0, "p50": None, "p90": None, "p95": None, "max": None}
    array = np.asarray(finite, dtype="float64")
    p50, p90, p95 = np.percentile(array, [50, 90, 95])
    return {
        "count": int(array.size),
        "p50": float(p50),
        "p90": float(p90),
        "p95": float(p95),
        "max": float(np.max(array)),
    }


def _median_or_none(values: Sequence[float]) -> float | None:
    return None if not values else float(np.median(np.asarray(values, dtype="float64")))


def _positive_factor(value: float | str) -> float:
    try:
        factor = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid exposure factor: {value}") from exc
    if not math.isfinite(factor) or factor <= 0:
        raise ValueError("exposure factors must be positive finite values")
    return factor


def _validate_group_collections(collections: Mapping[float, Mapping[str, Any]]) -> None:
    reference = next(iter(collections.values()))
    for collection in collections.values():
        for key in ("location_config_sha256", "plane_order", "patch_signature"):
            if collection[key] != reference[key]:
                raise ValueError(f"exposure groups use different {key} values")


def _repeatability_sigma(repeatability: Mapping[str, Any] | None, feature_id: str) -> float | None:
    if not isinstance(repeatability, Mapping):
        return None
    features = repeatability.get("features")
    feature = features.get(feature_id) if isinstance(features, Mapping) else None
    if not isinstance(feature, Mapping):
        return None
    standard_deviation = _finite_float(feature.get("standard_deviation"))
    if standard_deviation is not None and standard_deviation > 0:
        return standard_deviation
    mad = _finite_float(feature.get("mad"))
    return None if mad is None or mad <= 0 else mad * 1.4826


def _sigma_multiple(difference: float, sigma: float | None) -> float | None:
    if sigma is None or sigma <= 0:
        return 0.0 if difference == 0 else None
    return abs(difference) / sigma


def _monotonic_drift(centers: Sequence[Mapping[str, Any]], noise_sigma: float | None) -> str:
    if len(centers) < 2:
        return "indeterminate"
    values = [float(item["center"]) for item in centers]
    differences = np.diff(np.asarray(values, dtype="float64"))
    tolerance = 0.0 if noise_sigma is None else float(noise_sigma)
    signs = [0 if abs(value) <= tolerance else (1 if value > 0 else -1) for value in differences]
    if all(sign >= 0 for sign in signs) and any(sign > 0 for sign in signs):
        return "increasing"
    if all(sign <= 0 for sign in signs) and any(sign < 0 for sign in signs):
        return "decreasing"
    return "none"
