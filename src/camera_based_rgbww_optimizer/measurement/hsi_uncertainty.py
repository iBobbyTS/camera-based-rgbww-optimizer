from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import signal
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import (
    HUE_NODES,
    SAT_NODES,
    RayHsiManifold,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


DEFAULT_OUTPUT = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-uncertainty.json"
DEFAULT_P6_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/"
    "p6-ray-hsi-remote-20260717-0403-retry1"
)
DEFAULT_P1_RUNS = (
    Path(
        "/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/"
        "p1-d1-remote-full-1-16000-20260714-235121"
    ),
    Path(
        "/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/"
        "p1-d2-cross-day-holdout-20260715-2300-retry2"
    ),
)
DEFAULT_BASIS_ANALYSIS = Path(
    "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/"
    "p2-five-channel-basis-20260716-005935/basis-analysis.json"
)
DEFAULT_LOCATION = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
PLANES = ("R", "G1", "G2", "B")
REGULARIZATION = "cfa_plane_block_isotropic_diagonal"
MAD_NORMALIZER = 0.6744897501960817
QUANTILE_METHOD = "linear"


def _interrupt_on_signal(signum: int, _frame: Any) -> None:
    """Route launchd/shell termination through the normal evidence finally path."""
    raise KeyboardInterrupt(f"received {signal.Signals(signum).name}")


def unit_shape(values: Sequence[float]) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    norm = float(np.linalg.norm(vector))
    if vector.ndim != 1 or norm <= 0.0 or not np.isfinite(norm):
        raise ValueError("HSI uncertainty vectors must have positive finite norm")
    return vector / norm


def feature_ids_sha256(feature_ids: Sequence[str]) -> str:
    payload = json.dumps(list(feature_ids), separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def target_kind(manifold: RayHsiManifold, hue: float, sat: float) -> str:
    bounded_sat = min(max(float(sat), 0.0), 100.0)
    normalized_hue = float(hue) % 360.0
    exact_hue = any(math.isclose(normalized_hue, node, abs_tol=1e-12) for node in HUE_NODES)
    exact_sat = any(math.isclose(bounded_sat, node, abs_tol=1e-12) for node in SAT_NODES)
    if bounded_sat == 0.0 and exact_hue:
        return "sat0_exact_node"
    if exact_hue and exact_sat:
        return "nonzero_exact_node"
    if _is_high_curvature(normalized_hue, bounded_sat):
        return "nonzero_high_curvature_interpolation"
    return "nonzero_regular_interpolation"


def regularize_groups(
    groups: Mapping[str, Sequence[Sequence[float]]],
    feature_ids: Sequence[str],
    *,
    center_within_group: bool = True,
) -> dict[str, Any]:
    feature_ids = tuple(feature_ids)
    if len(groups) < 2:
        raise ValueError("uncertainty component requires at least two independent groups")
    residuals: list[np.ndarray] = []
    group_audit: list[dict[str, Any]] = []
    for group_id, rows in sorted(groups.items()):
        matrix = np.asarray(rows, dtype=float)
        if matrix.ndim != 2 or matrix.shape[1] != len(feature_ids) or matrix.shape[0] < 2:
            raise ValueError(f"uncertainty group {group_id} must contain at least two complete vectors")
        if not np.all(np.isfinite(matrix)):
            raise ValueError(f"uncertainty group {group_id} contains nonfinite values")
        centered = matrix - np.mean(matrix, axis=0) if center_within_group else matrix
        residuals.append(centered)
        group_audit.append({"group_id": group_id, "sample_count": int(matrix.shape[0])})
    pooled = np.vstack(residuals)
    raw_variance = np.var(pooled, axis=0, ddof=1)
    diagonal = np.empty(len(feature_ids), dtype=float)
    plane_audit: dict[str, Any] = {}
    for plane in PLANES:
        indices = [index for index, feature in enumerate(feature_ids) if _feature_plane(feature) == plane]
        if not indices:
            raise ValueError(f"uncertainty feature set has no {plane} values")
        scalars = np.concatenate([matrix[:, indices].reshape(-1) for matrix in residuals])
        dof = sum((matrix.shape[0] - 1) * len(indices) for matrix in residuals)
        if dof <= 0:
            raise ValueError(f"uncertainty plane {plane} has no positive degrees of freedom")
        s_mad = float(np.median(np.abs(scalars)) / MAD_NORMALIZER)
        s_rms = float(np.sqrt(np.sum(scalars * scalars) / dof))
        variance = max(s_mad * s_mad, s_rms * s_rms, 1e-12)
        diagonal[indices] = variance
        plane_audit[plane] = {
            "feature_count": len(indices),
            "degrees_of_freedom": int(dof),
            "mad_scale": s_mad,
            "rms_scale": s_rms,
            "final_variance": variance,
        }
    if not np.all(np.isfinite(diagonal)) or np.any(diagonal <= 0.0):
        raise ValueError("regularized uncertainty covariance is not finite positive definite")
    return {
        "regularization": REGULARIZATION,
        "group_count": len(groups),
        "groups": group_audit,
        "raw_sample_variance_by_feature": {
            feature: float(raw_variance[index]) for index, feature in enumerate(feature_ids)
        },
        "plane_statistics": plane_audit,
        "diagonal_variance": diagonal.tolist(),
        "minimum_eigenvalue": float(np.min(diagonal)),
        "positive_definite": True,
    }


def load_ray_repeat_groups(
    manifold: RayHsiManifold,
    run_dir: str | Path = DEFAULT_P6_RUN,
) -> dict[str, list[list[float]]]:
    root = Path(run_dir)
    grouped: dict[tuple[int, int], list[Mapping[str, Any]]] = defaultdict(list)
    for record in _load_jsonl(root / "captures.jsonl"):
        state = record.get("ray_state") or {}
        if record.get("source") == "ray" and record.get("ray_mode") == "hsi":
            grouped[(int(state["hue"]), int(state["sat"]))].append(record)
    output: dict[str, list[list[float]]] = {}
    for state, records in sorted(grouped.items()):
        if len(records) < 2:
            continue
        rows = []
        for record in records:
            report = _load_json(Path(record["capture"]["patch_statistics"]))
            values = _accepted_feature_values(report, manifold.coordinate_feature_ids)
            rows.append(unit_shape(values).tolist())
        output[f"p6:h{state[0]}:s{state[1]}"] = rows
    if len(output) < 2:
        raise ValueError("P6 does not contain two complete independent Ray repeat groups")
    return output


def load_strip_repeat_groups(
    feature_ids: Sequence[str],
    run_dirs: Sequence[str | Path] = DEFAULT_P1_RUNS,
) -> dict[str, list[list[float]]]:
    output: dict[str, list[list[float]]] = {}
    for run_dir in run_dirs:
        root = Path(run_dir)
        analysis = _load_json(root / "analysis.json")
        observations = analysis["repeatability"]["strip"]["collection"]["observations"]
        by_report: dict[str, dict[str, float]] = defaultdict(dict)
        for item in observations:
            if item.get("status") == "included" and item.get("value") is not None:
                by_report[str(item["report_id"])][str(item["feature_id"])] = float(item["value"])
        rows = []
        for report_id, values in sorted(by_report.items()):
            missing = [feature for feature in feature_ids if feature not in values]
            if missing:
                raise ValueError(f"P1 strip repeat {report_id} is missing frozen HSI features")
            rows.append(unit_shape([values[feature] for feature in feature_ids]).tolist())
        if len(rows) < 2:
            raise ValueError(f"P1 run {root} has fewer than two strip paired repeats")
        output[f"p1:{root.name}"] = rows
    if len(output) < 2:
        raise ValueError("strip repeatability floor requires two natural-day run groups")
    return output


def build_interpolation_groups(manifold: RayHsiManifold) -> dict[str, dict[str, list[list[float]]]]:
    feature_ids = manifold.coordinate_feature_ids
    result: dict[str, dict[str, list[list[float]]]] = {
        "regular": defaultdict(list),
        "high_curvature": defaultdict(list),
    }
    hues = tuple(HUE_NODES)
    for fold in (0, 1):
        group_by_region: dict[str, list[list[float]]] = defaultdict(list)
        for hue_index, hue in enumerate(hues):
            if hue_index % 2 != fold:
                continue
            lower_hue = hues[(hue_index - 1) % len(hues)]
            upper_hue = hues[(hue_index + 1) % len(hues)]
            for sat in SAT_NODES[1:]:
                actual = unit_shape([manifold.nodes[(hue, sat)][feature] for feature in feature_ids])
                predicted = unit_shape([
                    0.5 * (
                        manifold.nodes[(lower_hue, sat)][feature]
                        + manifold.nodes[(upper_hue, sat)][feature]
                    )
                    for feature in feature_ids
                ])
                region = "high_curvature" if _is_high_curvature(hue, sat) else "regular"
                group_by_region[region].append((actual - predicted).tolist())
        for region, rows in group_by_region.items():
            result[region][f"hue_cv_fold_{fold}"] = rows
    internal_sats = SAT_NODES[1:-1]
    for fold in (0, 1):
        group_by_region = defaultdict(list)
        for sat_index, sat in enumerate(internal_sats):
            if sat_index % 2 != fold:
                continue
            full_index = SAT_NODES.index(sat)
            lower_sat = SAT_NODES[full_index - 1]
            upper_sat = SAT_NODES[full_index + 1]
            fraction = (sat - lower_sat) / (upper_sat - lower_sat)
            for hue in hues:
                actual = unit_shape([manifold.nodes[(hue, sat)][feature] for feature in feature_ids])
                lower = manifold._node(hue, lower_sat)
                upper = manifold._node(hue, upper_sat)
                predicted = unit_shape([
                    (1.0 - fraction) * lower[feature] + fraction * upper[feature]
                    for feature in feature_ids
                ])
                region = "high_curvature" if _is_high_curvature(hue, sat) else "regular"
                group_by_region[region].append((actual - predicted).tolist())
        for region, rows in group_by_region.items():
            result[region][f"sat_cv_fold_{fold}"] = rows
    return {region: dict(groups) for region, groups in result.items()}


def evaluate_joint(
    manifold: RayHsiManifold,
    candidate_features: Mapping[str, float],
    *,
    target_hue: float,
    target_sat: float,
    scales: Sequence[float],
) -> dict[str, Any]:
    coordinate = manifold.coordinate(candidate_features, target_hue=target_hue, target_sat=target_sat)
    values = _coordinate_output(coordinate, target_sat)
    scale_array = np.maximum(np.asarray(scales, dtype=float), 1e-12)
    if scale_array.shape != values.shape:
        raise ValueError("joint uncertainty scale dimension does not match evaluator output")
    joint_score = float(np.max(values / scale_array))
    return {
        "output": values.tolist(),
        "joint_score": joint_score,
        "coordinate": coordinate.to_jsonable(),
    }


class FrozenHsiUncertaintyEvaluator:
    def __init__(self, artifact: Mapping[str, Any], *, artifact_sha256: str | None = None) -> None:
        if artifact.get("status") != "offline_frozen_before_measurement":
            raise ValueError("HSI uncertainty artifact is not frozen before measurement")
        self.artifact = dict(artifact)
        self.artifact_sha256 = artifact_sha256

    @classmethod
    def load(cls, path: str | Path = DEFAULT_OUTPUT) -> "FrozenHsiUncertaintyEvaluator":
        artifact_path = Path(path)
        return cls(_load_json(artifact_path), artifact_sha256=_sha256(artifact_path))

    def evaluate(
        self,
        manifold: RayHsiManifold,
        candidate_features: Mapping[str, float],
        *,
        target_hue: float,
        target_sat: float,
    ) -> dict[str, Any]:
        kind = target_kind(manifold, target_hue, target_sat)
        calibration = self.artifact["joint_calibration"][kind]
        result = evaluate_joint(
            manifold,
            candidate_features,
            target_hue=target_hue,
            target_sat=target_sat,
            scales=calibration["component_scales"],
        )
        score = float(result["joint_score"])
        guarded = float(calibration["guarded_acceptance_limit"])
        coverage = float(calibration["coverage_limit"])
        result.update({
            "artifact_sha256": self.artifact_sha256,
            "target_kind": kind,
            "coverage_limit": coverage,
            "guarded_acceptance_limit": guarded,
            "component_scales": list(calibration["component_scales"]),
            "diagonal_variance": list(calibration["diagonal_variance"]),
            "feasible": score <= guarded,
            "decision": "faithful" if score <= guarded else (
                "uncertainty_unresolved" if score <= coverage else "outside_coverage"
            ),
        })
        return result

    def evaluate_reference(
        self,
        manifold: RayHsiManifold,
        candidate_features: Mapping[str, float],
        *,
        target_hue: float,
        target_sat: float,
    ) -> dict[str, Any]:
        kind = target_kind(manifold, target_hue, target_sat)
        if kind not in {"sat0_exact_node", "nonzero_exact_node"}:
            raise ValueError("P7 reference anchors must be exact frozen P6 nodes")
        calibration = self.artifact["reference_calibration"][kind]
        result = evaluate_joint(
            manifold,
            candidate_features,
            target_hue=target_hue,
            target_sat=target_sat,
            scales=calibration["component_scales"],
        )
        coverage = float(calibration["coverage_limit"])
        result.update({
            "artifact_sha256": self.artifact_sha256,
            "target_kind": kind,
            "coverage_limit": coverage,
            "within_reference_coverage": float(result["joint_score"]) <= coverage,
            "strip_component_included": False,
        })
        return result

    def confirmation_spread(
        self,
        objectives: Sequence[Mapping[str, Any]],
        *,
        target_sat: float,
    ) -> dict[str, Any]:
        count = len(objectives)
        family = "sat0" if float(target_sat) == 0.0 else "nonzero"
        calibration = self.artifact["confirmation_policies"]["repeat_spread"][family][str(count)]
        outputs = np.asarray([item["joint_output"] for item in objectives], dtype=float)
        scales = np.maximum(np.asarray(calibration["component_scales"], dtype=float), 1e-12)
        pairwise = np.vstack([
            np.abs(outputs[i] - outputs[j])
            for i in range(count)
            for j in range(i + 1, count)
        ])
        maximum_score = float(np.max(pairwise / scales))
        limit = float(calibration["limit"])
        return {
            "confirmation_count": count,
            "family": family,
            "maximum_pairwise_score": maximum_score,
            "repeat_spread_limit": limit,
            "pass": maximum_score <= limit,
        }


def validate_uncertainty_artifact(
    artifact: Mapping[str, Any],
    *,
    expected_feature_ids: Sequence[str],
) -> dict[str, Any]:
    """Audit the frozen Phase-A artifact without recalibrating any threshold."""
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, evidence: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "evidence": evidence})

    feature_set = artifact.get("feature_set", {})
    expected_hash = feature_ids_sha256(expected_feature_ids)
    record(
        "ordered_58_feature_contract",
        feature_set.get("count") == 58
        and feature_set.get("ids") == list(expected_feature_ids)
        and feature_set.get("sha256") == expected_hash,
        {"count": feature_set.get("count"), "sha256": feature_set.get("sha256")},
    )
    record(
        "frozen_before_measurement",
        artifact.get("status") == "offline_frozen_before_measurement"
        and artifact.get("no_post_measurement_threshold_update") is True,
        {
            "status": artifact.get("status"),
            "no_post_measurement_threshold_update": artifact.get("no_post_measurement_threshold_update"),
        },
    )
    recipes = artifact.get("covariance_recipes", {})
    record(
        "covariance_recipes",
        recipes.get("match") == "Sigma_ray + Sigma_strip_floor + Sigma_interpolation"
        and recipes.get("reference") == "2 * Sigma_ray + Sigma_interpolation"
        and recipes.get("camera_noise_extra_component") is False,
        recipes,
    )

    component_evidence: dict[str, Any] = {}
    components = artifact.get("components", {})
    component_pass = True
    for name in ("ray_repeatability", "strip_repeatability_floor"):
        component = components.get(name, {})
        diagonal = np.asarray(component.get("diagonal_variance", []), dtype=float)
        valid = (
            component.get("regularization") == REGULARIZATION
            and int(component.get("group_count", 0)) >= 2
            and component.get("positive_definite") is True
            and diagonal.shape == (58,)
            and bool(np.all(np.isfinite(diagonal)))
            and bool(np.all(diagonal > 0.0))
        )
        component_pass &= valid
        component_evidence[name] = {
            "group_count": component.get("group_count"),
            "minimum_eigenvalue": component.get("minimum_eigenvalue"),
            "valid": valid,
        }
    interpolation = components.get("interpolation", {})
    exact = np.asarray(interpolation.get("exact_node", {}).get("diagonal_variance", []), dtype=float)
    interpolation_valid = exact.shape == (58,) and bool(np.all(exact == 0.0))
    for region in ("regular", "high_curvature"):
        component = interpolation.get(region, {})
        diagonal = np.asarray(component.get("diagonal_variance", []), dtype=float)
        region_valid = (
            int(component.get("group_count", 0)) >= 2
            and component.get("positive_definite") is True
            and diagonal.shape == (58,)
            and bool(np.all(np.isfinite(diagonal)))
            and bool(np.all(diagonal > 0.0))
        )
        interpolation_valid &= region_valid
        component_evidence[f"interpolation_{region}"] = {
            "group_count": component.get("group_count"),
            "minimum_eigenvalue": component.get("minimum_eigenvalue"),
            "valid": region_valid,
        }
    component_evidence["interpolation_exact_node_zero"] = bool(
        exact.shape == (58,) and np.all(exact == 0.0)
    )
    record("positive_deterministic_components", component_pass and interpolation_valid, component_evidence)

    expected_kinds = {
        "sat0_exact_node": 2,
        "nonzero_exact_node": 3,
        "nonzero_regular_interpolation": 3,
        "nonzero_high_curvature_interpolation": 3,
    }
    calibration_evidence: dict[str, Any] = {}
    calibrations = artifact.get("joint_calibration", {})
    calibration_pass = set(calibrations) == set(expected_kinds)
    for kind, dimension in expected_kinds.items():
        calibration = calibrations.get(kind, {})
        monte_carlo = calibration.get("monte_carlo", {})
        bootstrap = calibration.get("bootstrap", {})
        coverage = float(calibration.get("coverage_limit", math.nan))
        guarded = float(calibration.get("guarded_acceptance_limit", math.nan))
        empirical = float(calibration.get("empirical_coverage", math.nan))
        sample_count = int(monte_carlo.get("sample_count", 0))
        valid = (
            len(calibration.get("component_scales", [])) == dimension
            and all(math.isfinite(float(value)) and float(value) > 0.0 for value in calibration.get("component_scales", []))
            and math.isfinite(coverage)
            and math.isfinite(guarded)
            and 0.0 < guarded <= coverage
            and abs(empirical - float(artifact.get("coverage_probability", math.nan))) <= max(1.0 / max(sample_count, 1), 1e-12)
            and monte_carlo.get("batch_size") == 50_000
            and monte_carlo.get("minimum_samples") == 200_000
            and monte_carlo.get("maximum_samples") == 1_000_000
            and 200_000 <= sample_count <= 1_000_000
            and int(monte_carlo.get("consecutive_stable_batches", 0)) >= 3
            and int(bootstrap.get("replicate_count_requested", 0)) == 200
            and int(bootstrap.get("replicate_count_valid", 0)) >= 180
        )
        calibration_pass &= valid
        calibration_evidence[kind] = {
            "dimension": len(calibration.get("component_scales", [])),
            "coverage_limit": coverage,
            "guarded_acceptance_limit": guarded,
            "empirical_coverage": empirical,
            "sample_count": sample_count,
            "stable_batches": monte_carlo.get("consecutive_stable_batches"),
            "bootstrap_valid": bootstrap.get("replicate_count_valid"),
            "valid": valid,
        }
    record("joint_monte_carlo_and_guard_band", calibration_pass, calibration_evidence)

    reference = artifact.get("reference_drift_region", {})
    reference_calibrations = artifact.get("reference_calibration", {})
    reference_pass = (
        reference.get("strip_component_included") is False
        and set(reference_calibrations) == {"sat0_exact_node", "nonzero_exact_node"}
    )
    record("reference_region_excludes_strip", reference_pass, reference)

    policies = artifact.get("confirmation_policies", {})
    spread = policies.get("repeat_spread", {})
    confirmation_pass = policies.get("ordinary") == 3 and policies.get("boundary_scale_relaxed_holdout") == 5
    for family, dimension in (("sat0", 2), ("nonzero", 3)):
        for count in (3, 5):
            calibration = spread.get(family, {}).get(str(count), {})
            confirmation_pass &= (
                calibration.get("confirmation_count") == count
                and calibration.get("sample_count") >= 200_000
                and len(calibration.get("component_scales", [])) == dimension
                and math.isfinite(float(calibration.get("limit", math.nan)))
                and float(calibration.get("limit", math.nan)) > 0.0
            )
    record("confirmation_3_and_5_frozen_spread", confirmation_pass, {
        "ordinary": policies.get("ordinary"),
        "boundary_scale_relaxed_holdout": policies.get("boundary_scale_relaxed_holdout"),
    })
    return {
        "schema_version": 1,
        "status": "pass" if all(item["passed"] for item in checks) else "fail",
        "artifact_status": artifact.get("status"),
        "coverage_probability": artifact.get("coverage_probability"),
        "checks": checks,
    }


def generate_uncertainty_artifact(
    *,
    manifold_path: str | Path,
    p6_run: str | Path = DEFAULT_P6_RUN,
    p1_runs: Sequence[str | Path] = DEFAULT_P1_RUNS,
    seed: int = 20260717,
    batch_size: int = 50_000,
    minimum_samples: int = 200_000,
    maximum_samples: int = 1_000_000,
    convergence_relative: float = 0.01,
    bootstrap_replicates: int = 200,
    bootstrap_samples: int = 20_000,
    workers: int = 1,
) -> dict[str, Any]:
    manifold_path = Path(manifold_path)
    manifold = RayHsiManifold.load(manifold_path)
    feature_ids = manifold.coordinate_feature_ids
    ray_groups = load_ray_repeat_groups(manifold, p6_run)
    strip_groups = load_strip_repeat_groups(feature_ids, p1_runs)
    interpolation_groups = build_interpolation_groups(manifold)
    ray_component = regularize_groups(ray_groups, feature_ids)
    strip_component = regularize_groups(strip_groups, feature_ids)
    interpolation_components = {
        region: regularize_groups(groups, feature_ids, center_within_group=False)
        for region, groups in interpolation_groups.items()
    }
    zero = np.zeros(len(feature_ids), dtype=float)
    ray_variance = np.asarray(ray_component["diagonal_variance"], dtype=float)
    strip_variance = np.asarray(strip_component["diagonal_variance"], dtype=float)
    interpolation_variances = {
        "exact": zero,
        "regular": np.asarray(interpolation_components["regular"]["diagonal_variance"], dtype=float),
        "high_curvature": np.asarray(interpolation_components["high_curvature"]["diagonal_variance"], dtype=float),
    }
    region_specs = {
        "sat0_exact_node": (0.0, 0.0, "exact"),
        "nonzero_exact_node": (120.0, 50.0, "exact"),
        "nonzero_regular_interpolation": (150.0, 35.0, "regular"),
        "nonzero_high_curvature_interpolation": (345.0, 50.0, "high_curvature"),
    }
    calibrations: dict[str, Any] = {}
    for offset, (kind, (hue, sat, interpolation_region)) in enumerate(region_specs.items()):
        match_variance = ray_variance + strip_variance + interpolation_variances[interpolation_region]
        calibration = calibrate_joint_region(
            manifold,
            target_hue=hue,
            target_sat=sat,
            diagonal_variance=match_variance,
            seed=seed + offset * 100_000,
            batch_size=batch_size,
            minimum_samples=minimum_samples,
            maximum_samples=maximum_samples,
            convergence_relative=convergence_relative,
            workers=workers,
        )
        bootstrap_limits = bootstrap_coverage_limits(
            manifold,
            target_hue=hue,
            target_sat=sat,
            ray_groups=ray_groups,
            strip_groups=strip_groups,
            interpolation_groups=None if interpolation_region == "exact" else interpolation_groups[interpolation_region],
            feature_ids=feature_ids,
            seed=seed + offset * 100_000 + 50_000,
            replicates=bootstrap_replicates,
            samples=bootstrap_samples,
            workers=workers,
        )
        if len(bootstrap_limits) < math.ceil(bootstrap_replicates * 0.9):
            raise ValueError("fewer than 180/200 valid uncertainty bootstrap replicates")
        calibration.update({
            "target_kind": kind,
            "representative_target": {"hue": hue, "sat": sat},
            "interpolation_component": interpolation_region,
            "bootstrap": {
                "method": "stratified_group_resampling_with_replacement",
                "seed": seed + offset * 100_000 + 50_000,
                "replicate_count_requested": bootstrap_replicates,
                "replicate_count_valid": len(bootstrap_limits),
                "samples_per_replicate": bootstrap_samples,
                "one_sided_confidence": 0.95,
                "coverage_limits": bootstrap_limits,
            },
            "guarded_acceptance_limit": float(np.quantile(bootstrap_limits, 0.05, method=QUANTILE_METHOD)),
            "diagonal_variance": match_variance.tolist(),
        })
        calibrations[kind] = calibration
    reference_calibrations: dict[str, Any] = {}
    for offset, (kind, (hue, sat)) in enumerate({
        "sat0_exact_node": (0.0, 0.0),
        "nonzero_exact_node": (120.0, 100.0),
    }.items()):
        reference_variance = 2.0 * ray_variance
        calibration = calibrate_joint_region(
            manifold,
            target_hue=hue,
            target_sat=sat,
            diagonal_variance=reference_variance,
            seed=seed + 600_000 + offset * 100_000,
            batch_size=batch_size,
            minimum_samples=minimum_samples,
            maximum_samples=maximum_samples,
            convergence_relative=convergence_relative,
            workers=workers,
        )
        bootstrap_limits = bootstrap_coverage_limits(
            manifold,
            target_hue=hue,
            target_sat=sat,
            ray_groups=ray_groups,
            strip_groups=None,
            interpolation_groups=None,
            feature_ids=feature_ids,
            seed=seed + 650_000 + offset * 100_000,
            replicates=bootstrap_replicates,
            samples=bootstrap_samples,
            workers=workers,
        )
        if len(bootstrap_limits) < math.ceil(bootstrap_replicates * 0.9):
            raise ValueError("fewer than 180/200 valid reference bootstrap replicates")
        calibration.update({
            "target_kind": kind,
            "representative_target": {"hue": hue, "sat": sat},
            "strip_component_included": False,
            "diagonal_variance": reference_variance.tolist(),
            "bootstrap": {
                "seed": seed + 650_000 + offset * 100_000,
                "replicate_count_requested": bootstrap_replicates,
                "replicate_count_valid": len(bootstrap_limits),
                "samples_per_replicate": bootstrap_samples,
                "coverage_limits": bootstrap_limits,
            },
            "guarded_acceptance_limit": float(np.quantile(bootstrap_limits, 0.05, method=QUANTILE_METHOD)),
        })
        reference_calibrations[kind] = calibration
    repeat_spread = {
        family: {
            str(count): calibrate_repeat_spread(
                manifold,
                target_hue=hue,
                target_sat=sat,
                strip_variance=strip_variance,
                count=count,
                seed=seed + 900_000 + family_offset * 10_000 + count,
                samples=minimum_samples,
                workers=workers,
            )
            for count in (3, 5)
        }
        for family_offset, (family, (hue, sat)) in enumerate({
            "sat0": (0.0, 0.0),
            "nonzero": (120.0, 50.0),
        }.items())
    }
    return {
        "schema_version": 1,
        "status": "offline_frozen_before_measurement",
        "observer_scope": {
            "camera": "Canon EOS R6 Mark III native Bayer",
            "raw_response": "identity",
            "exposure_envelope": "per-source 1.0x..1.25x",
            "planes": list(PLANES),
            "absolute_brightness_matched": False,
        },
        "feature_set": {
            "count": len(feature_ids),
            "ids": list(feature_ids),
            "sha256": feature_ids_sha256(feature_ids),
            "transform": "exposure-normalized then unit shape",
        },
        "inputs": {
            "manifold": _file_reference(manifold_path),
            "p6_run": _p6_run_reference(Path(p6_run)),
            "p1_runs": [_run_reference(Path(path)) for path in p1_runs],
            "basis_analysis": _file_reference(DEFAULT_BASIS_ANALYSIS),
            "location_config": _file_reference(DEFAULT_LOCATION),
            "raw_observer_config": _file_reference(DEFAULT_OBSERVER),
        },
        "regularization": {
            "type": REGULARIZATION,
            "mad_normalizer": MAD_NORMALIZER,
            "variance_floor": 1e-12,
            "off_diagonal": 0.0,
        },
        "components": {
            "ray_repeatability": ray_component,
            "strip_repeatability_floor": strip_component,
            "interpolation": {
                "exact_node": {"diagonal_variance": zero.tolist(), "by_contract": True},
                "regular": interpolation_components["regular"],
                "high_curvature": interpolation_components["high_curvature"],
            },
        },
        "covariance_recipes": {
            "match": "Sigma_ray + Sigma_strip_floor + Sigma_interpolation",
            "reference": "2 * Sigma_ray + Sigma_interpolation",
            "confirmation_pairwise": "2 * Sigma_strip_floor",
            "camera_noise_extra_component": False,
        },
        "joint_score_definition": "max_j(abs_output_j / q0.6827_null_j)",
        "coverage_probability": 0.9973,
        "joint_calibration": calibrations,
        "reference_calibration": reference_calibrations,
        "confirmation_policies": {
            "ordinary": 3,
            "boundary_scale_relaxed_holdout": 5,
            "repeat_spread": repeat_spread,
        },
        "reference_drift_region": {
            "strip_component_included": False,
            "recipe": "2 * Sigma_ray + Sigma_interpolation",
            "calibration": "reference_calibration",
        },
        "no_post_measurement_threshold_update": True,
        "parallel_workers": workers,
    }


def calibrate_joint_region(
    manifold: RayHsiManifold,
    *,
    target_hue: float,
    target_sat: float,
    diagonal_variance: Sequence[float],
    seed: int,
    batch_size: int,
    minimum_samples: int,
    maximum_samples: int,
    convergence_relative: float,
    workers: int = 1,
) -> dict[str, Any]:
    if not (0 < batch_size <= minimum_samples <= maximum_samples):
        raise ValueError("invalid Monte Carlo batch/sample bounds")
    rng = np.random.default_rng(seed)
    outputs: list[np.ndarray] = []
    limits: list[float] = []
    stable_batches = 0
    while sum(len(batch) for batch in outputs) < maximum_samples:
        outputs.append(_null_outputs_parallel(
            manifold,
            target_hue=target_hue,
            target_sat=target_sat,
            diagonal_variance=diagonal_variance,
            sample_count=min(batch_size, maximum_samples - sum(len(batch) for batch in outputs)),
            rng=rng,
            workers=workers,
        ))
        values = np.vstack(outputs)
        scales = np.maximum(np.quantile(values, 0.6827, axis=0, method=QUANTILE_METHOD), 1e-12)
        scores = np.max(values / scales, axis=1)
        limit = float(np.quantile(scores, 0.9973, method=QUANTILE_METHOD))
        limits.append(limit)
        if len(values) >= minimum_samples and len(limits) >= 2:
            relative = abs(limit - limits[-2]) / max(abs(limits[-2]), 1e-12)
            stable_batches = stable_batches + 1 if relative < convergence_relative else 0
            if stable_batches >= 3:
                break
    values = np.vstack(outputs)
    scales = np.maximum(np.quantile(values, 0.6827, axis=0, method=QUANTILE_METHOD), 1e-12)
    scores = np.max(values / scales, axis=1)
    coverage_limit = float(np.quantile(scores, 0.9973, method=QUANTILE_METHOD))
    if stable_batches < 3:
        raise ValueError("joint coverage limit did not converge in the frozen sample budget")
    empirical_coverage = float(np.mean(scores <= coverage_limit))
    coverage_tolerance = max(2.0 / len(scores), 1e-5)
    if abs(empirical_coverage - 0.9973) > coverage_tolerance:
        raise ValueError("joint null empirical coverage misses the predeclared numerical tolerance")
    return {
        "output_dimensions": ["abs_sat_error_percent", "orthogonal_residual"] if target_sat == 0 else [
            "abs_hue_error_degrees", "abs_sat_error_percent", "orthogonal_residual"
        ],
        "component_scales": scales.tolist(),
        "coverage_limit": coverage_limit,
        "empirical_coverage": empirical_coverage,
        "empirical_coverage_tolerance": coverage_tolerance,
        "empirical_coverage_check": "pass",
        "monte_carlo": {
            "seed": seed,
            "batch_size": batch_size,
            "minimum_samples": minimum_samples,
            "maximum_samples": maximum_samples,
            "sample_count": int(len(values)),
            "coverage_limit_history": limits,
            "consecutive_stable_batches": stable_batches,
            "relative_convergence_threshold": convergence_relative,
            "quantile_method": QUANTILE_METHOD,
        },
    }


def bootstrap_coverage_limits(
    manifold: RayHsiManifold,
    *,
    target_hue: float,
    target_sat: float,
    ray_groups: Mapping[str, Sequence[Sequence[float]]],
    strip_groups: Mapping[str, Sequence[Sequence[float]]] | None,
    interpolation_groups: Mapping[str, Sequence[Sequence[float]]] | None,
    feature_ids: Sequence[str],
    seed: int,
    replicates: int,
    samples: int,
    workers: int = 1,
) -> list[float]:
    tasks = [(
        manifold, target_hue, target_sat, ray_groups, strip_groups,
        interpolation_groups, tuple(feature_ids), seed + index, samples,
    ) for index in range(replicates)]
    if workers <= 1:
        results = [_bootstrap_replicate_task(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(_bootstrap_replicate_task, tasks))
    return [float(value) for value in results if value is not None]


def calibrate_repeat_spread(
    manifold: RayHsiManifold,
    *,
    target_hue: float,
    target_sat: float,
    strip_variance: Sequence[float],
    count: int,
    seed: int,
    samples: int,
    workers: int = 1,
) -> dict[str, Any]:
    if count < 2:
        raise ValueError("repeat spread requires at least two confirmations")
    chunk_count = max(1, min(workers, samples))
    base, remainder = divmod(samples, chunk_count)
    tasks = [(
        manifold, target_hue, target_sat, tuple(strip_variance), count,
        seed + index, base + (1 if index < remainder else 0),
    ) for index in range(chunk_count)]
    if workers <= 1:
        chunks = [_repeat_spread_chunk(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            chunks = list(executor.map(_repeat_spread_chunk, tasks))
    pairwise_all = np.concatenate(chunks, axis=0)
    pooled = pairwise_all.reshape(-1, pairwise_all.shape[-1])
    scales = np.maximum(np.quantile(pooled, 0.6827, axis=0, method=QUANTILE_METHOD), 1e-12)
    maxima = np.max(pairwise_all / scales, axis=(1, 2))
    return {
        "confirmation_count": count,
        "seed": seed,
        "sample_count": samples,
        "component_scales": scales.tolist(),
        "limit": float(np.quantile(maxima, 0.9973, method=QUANTILE_METHOD)),
        "recipe": "maximum pairwise joint score under 2 * Sigma_strip_floor",
    }


def write_uncertainty_artifact(path: str | Path, artifact: Mapping[str, Any]) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, output)
    return output


def _null_outputs(
    manifold: RayHsiManifold,
    *,
    target_hue: float,
    target_sat: float,
    diagonal_variance: Sequence[float],
    sample_count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    feature_ids = manifold.coordinate_feature_ids
    target = manifold.target_at(target_hue, target_sat)
    center = unit_shape([target.features[feature] for feature in feature_ids])
    sigma = np.sqrt(np.asarray(diagonal_variance, dtype=float))
    if sigma.shape != center.shape or np.any(~np.isfinite(sigma)) or np.any(sigma < 0.0):
        raise ValueError("invalid diagonal uncertainty covariance")
    output = []
    for noise in rng.normal(0.0, sigma, size=(sample_count, len(feature_ids))):
        candidate = unit_shape(center + noise)
        coordinate = manifold.coordinate(
            dict(zip(feature_ids, candidate, strict=True)),
            target_hue=target_hue,
            target_sat=target_sat,
        )
        output.append(_coordinate_output(coordinate, target_sat))
    return np.vstack(output)


def _null_outputs_parallel(
    manifold: RayHsiManifold,
    *,
    target_hue: float,
    target_sat: float,
    diagonal_variance: Sequence[float],
    sample_count: int,
    rng: np.random.Generator,
    workers: int,
) -> np.ndarray:
    if workers <= 1 or sample_count < workers:
        return _null_outputs(
            manifold, target_hue=target_hue, target_sat=target_sat,
            diagonal_variance=diagonal_variance, sample_count=sample_count, rng=rng,
        )
    base, remainder = divmod(sample_count, workers)
    tasks = [(
        manifold, target_hue, target_sat, tuple(diagonal_variance),
        base + (1 if index < remainder else 0),
        int(rng.integers(0, np.iinfo(np.int64).max)),
    ) for index in range(workers)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        chunks = list(executor.map(_null_outputs_task, tasks))
    return np.vstack(chunks)


def _null_outputs_task(task: tuple[Any, ...]) -> np.ndarray:
    manifold, target_hue, target_sat, diagonal_variance, sample_count, seed = task
    return _null_outputs(
        manifold, target_hue=target_hue, target_sat=target_sat,
        diagonal_variance=diagonal_variance, sample_count=sample_count,
        rng=np.random.default_rng(seed),
    )


def _bootstrap_replicate_task(task: tuple[Any, ...]) -> float | None:
    (
        manifold, target_hue, target_sat, ray_groups, strip_groups,
        interpolation_groups, feature_ids, seed, samples,
    ) = task
    rng = np.random.default_rng(seed)
    try:
        ray = regularize_groups(_bootstrap_groups(ray_groups, rng), feature_ids)
        variance = np.asarray(ray["diagonal_variance"])
        if strip_groups is not None:
            strip = regularize_groups(_bootstrap_groups(strip_groups, rng), feature_ids)
            variance = variance + np.asarray(strip["diagonal_variance"])
        if interpolation_groups is not None:
            interpolation = regularize_groups(
                _bootstrap_groups(interpolation_groups, rng), feature_ids,
                center_within_group=False,
            )
            variance = variance + np.asarray(interpolation["diagonal_variance"])
        values = _null_outputs(
            manifold, target_hue=target_hue, target_sat=target_sat,
            diagonal_variance=variance, sample_count=samples, rng=rng,
        )
        scales = np.maximum(np.quantile(values, 0.6827, axis=0, method=QUANTILE_METHOD), 1e-12)
        return float(np.quantile(np.max(values / scales, axis=1), 0.9973, method=QUANTILE_METHOD))
    except ValueError:
        return None


def _repeat_spread_chunk(task: tuple[Any, ...]) -> np.ndarray:
    manifold, target_hue, target_sat, strip_variance, count, seed, samples = task
    rng = np.random.default_rng(seed)
    target = manifold.target_at(target_hue, target_sat)
    feature_ids = manifold.coordinate_feature_ids
    center = unit_shape([target.features[feature] for feature in feature_ids])
    sigma = np.sqrt(np.asarray(strip_variance, dtype=float))
    pair_count = count * (count - 1) // 2
    dimensions = 2 if target_sat == 0 else 3
    result = np.empty((samples, pair_count, dimensions), dtype=float)
    for sample_index in range(samples):
        outputs = []
        for _repeat in range(count):
            candidate = unit_shape(center + rng.normal(0.0, sigma))
            coordinate = manifold.coordinate(
                dict(zip(feature_ids, candidate, strict=True)),
                target_hue=target_hue, target_sat=target_sat,
            )
            outputs.append(_coordinate_output(coordinate, target_sat))
        matrix = np.vstack(outputs)
        result[sample_index] = np.vstack([
            np.abs(matrix[i] - matrix[j])
            for i in range(count) for j in range(i + 1, count)
        ])
    return result


def _coordinate_output(coordinate: Any, target_sat: float) -> np.ndarray:
    if float(target_sat) == 0.0:
        return np.asarray([abs(coordinate.sat_error_percent), coordinate.orthogonal_residual], dtype=float)
    return np.asarray([
        abs(coordinate.hue_error_degrees),
        abs(coordinate.sat_error_percent),
        coordinate.orthogonal_residual,
    ], dtype=float)


def _bootstrap_groups(
    groups: Mapping[str, Sequence[Sequence[float]]], rng: np.random.Generator
) -> dict[str, list[list[float]]]:
    group_ids = sorted(groups)
    selected = rng.choice(group_ids, size=len(group_ids), replace=True)
    output = {}
    for index, group_id in enumerate(selected):
        rows = np.asarray(groups[str(group_id)], dtype=float)
        sample_indices = rng.integers(0, len(rows), size=len(rows))
        output[f"bootstrap-{index}:{group_id}"] = rows[sample_indices].tolist()
    return output


def _accepted_feature_values(report: Mapping[str, Any], feature_ids: Sequence[str]) -> list[float]:
    values: dict[str, float] = {}
    for patch in report.get("patches", []):
        patch_name = str(patch["name"])
        for plane, item in patch.get("planes", {}).items():
            feature = f"{patch_name}::{plane}"
            if feature not in feature_ids:
                continue
            if item.get("quality", {}).get("status") != "accepted":
                raise ValueError(f"P6 repeat feature {feature} is not accepted")
            values[feature] = float(item["ambient_subtracted"]["trimmed_mean_per_second"])
    missing = [feature for feature in feature_ids if feature not in values]
    if missing:
        raise ValueError(f"P6 repeat report is missing {len(missing)} frozen HSI features")
    return [values[feature] for feature in feature_ids]


def _is_high_curvature(hue: float, sat: float) -> bool:
    normalized_hue = float(hue) % 360.0
    bounded_sat = float(sat)
    wrap = (normalized_hue >= 330.0 or normalized_hue <= 90.0) and bounded_sat in (20.0, 50.0, 80.0, 95.0)
    cool = 240.0 <= normalized_hue <= 330.0 and bounded_sat in (20.0, 50.0, 80.0)
    return wrap or cool


def _feature_plane(feature_id: str) -> str:
    try:
        plane = feature_id.rsplit("::", 1)[1]
    except IndexError as exc:
        raise ValueError(f"invalid HSI feature id: {feature_id}") from exc
    if plane not in PLANES:
        raise ValueError(f"unsupported HSI feature plane: {plane}")
    return plane


def _run_reference(run_dir: Path) -> dict[str, Any]:
    return {
        "path": str(run_dir),
        "run_json_sha256": _sha256(run_dir / "run.json"),
        "plan_json_sha256": _sha256(run_dir / "plan.json"),
        "analysis_sha256": _sha256(run_dir / "analysis.json") if (run_dir / "analysis.json").is_file() else None,
    }


def _p6_run_reference(run_dir: Path) -> dict[str, Any]:
    return {
        "path": str(run_dir),
        "run_json_sha256": _sha256(run_dir / "run.json"),
        "plan_json_sha256": _sha256(run_dir / "plan.json"),
        "analysis_path": str(run_dir / "ray-hsi-analysis.json"),
        "analysis_sha256": _sha256(run_dir / "ray-hsi-analysis.json"),
    }


def _file_reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": _sha256(path)}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze P7 HSI joint uncertainty before device measurement.")
    parser.add_argument("--manifold-config", type=Path, default=PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json")
    parser.add_argument("--p6-run", type=Path, default=DEFAULT_P6_RUN)
    parser.add_argument("--p1-run", type=Path, action="append", dest="p1_runs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260717)
    parser.add_argument("--batch-size", type=int, default=50_000)
    parser.add_argument("--minimum-samples", type=int, default=200_000)
    parser.add_argument("--maximum-samples", type=int, default=1_000_000)
    parser.add_argument("--convergence-relative", type=float, default=0.01)
    parser.add_argument("--bootstrap-replicates", type=int, default=200)
    parser.add_argument("--bootstrap-samples", type=int, default=20_000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--evidence-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    evidence_dir = args.evidence_dir
    run_record = {
        "schema_version": 1,
        "phase": "P7-phase-A-uncertainty",
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "pid": os.getpid(),
        "offline_only": True,
        "device_calls_allowed": False,
        "output": str(args.output),
    }
    if evidence_dir is not None:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        _write_runtime_json(evidence_dir / "run.json", run_record)
    previous_signal_handlers = {
        signum: signal.signal(signum, _interrupt_on_signal)
        for signum in (signal.SIGHUP, signal.SIGTERM)
    }
    try:
        print("phase=A uncertainty generation started", flush=True)
        artifact = generate_uncertainty_artifact(
            manifold_path=args.manifold_config,
            p6_run=args.p6_run,
            p1_runs=args.p1_runs or DEFAULT_P1_RUNS,
            seed=args.seed,
            batch_size=args.batch_size,
            minimum_samples=args.minimum_samples,
            maximum_samples=args.maximum_samples,
            convergence_relative=args.convergence_relative,
            bootstrap_replicates=args.bootstrap_replicates,
            bootstrap_samples=args.bootstrap_samples,
            workers=args.workers,
        )
        output = write_uncertainty_artifact(args.output, artifact)
        print(output, flush=True)
        run_record["status"] = "complete"
        run_record["output_sha256"] = _sha256(output)
    except BaseException as exc:
        run_record["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        if evidence_dir is not None:
            _write_runtime_json(evidence_dir / "failure.json", {
                "at": _utc_now(), "type": type(exc).__name__, "message": str(exc),
            })
        raise
    finally:
        run_record["finished_at"] = _utc_now()
        if evidence_dir is not None:
            _write_runtime_json(evidence_dir / "all-off-python.json", {
                "at": _utc_now(),
                "offline_only": True,
                "sources_touched": False,
                "device_calls_performed": False,
                "status": "safe_by_device_isolation",
                "reason": "Phase A prohibits camera, Ray, ESPHome, and real all-off calls",
            })
            _write_runtime_json(evidence_dir / "run.json", run_record)
        for signum, previous_handler in previous_signal_handlers.items():
            signal.signal(signum, previous_handler)
    return 0


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_runtime_json(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


if __name__ == "__main__":
    raise SystemExit(main())
