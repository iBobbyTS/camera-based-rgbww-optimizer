from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import collect_patch_plane_features
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


DEFAULT_CONFIG = PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json"
HUE_NODES = tuple(range(0, 360, 30))
SAT_NODES = (0, 5, 20, 50, 80, 95, 100)
SAT0_HUES = (0, 60, 120, 180, 240, 300)


@dataclass(frozen=True)
class ManifoldTarget:
    hue: float
    sat: float
    features: dict[str, float]
    interpolation: dict[str, Any]


@dataclass(frozen=True)
class ManifoldCoordinate:
    target_hue: float
    target_sat: float
    hue_error_degrees: float
    sat_error_percent: float
    orthogonal_residual: float
    shape_residual: float
    global_scale_candidate_to_target: float
    common_feature_count: int
    tangent_condition_number: float
    hue_three_sigma_degrees: float
    sat_three_sigma_percent: float
    feature_ids: tuple[str, ...]

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "target_hue": self.target_hue,
            "target_sat": self.target_sat,
            "hue_error_degrees": self.hue_error_degrees,
            "sat_error_percent": self.sat_error_percent,
            "orthogonal_residual": self.orthogonal_residual,
            "shape_residual": self.shape_residual,
            "global_scale_candidate_to_target": self.global_scale_candidate_to_target,
            "common_feature_count": self.common_feature_count,
            "tangent_condition_number": self.tangent_condition_number,
            "hue_three_sigma_degrees": self.hue_three_sigma_degrees,
            "sat_three_sigma_percent": self.sat_three_sigma_percent,
            "feature_ids": list(self.feature_ids),
        }


class RayHsiManifold:
    def __init__(
        self,
        *,
        config: Mapping[str, Any],
        nodes: Mapping[tuple[int, int], Mapping[str, float]],
        zero_direction: Mapping[str, float],
        zero_scales: Mapping[int, float],
        repeatability_three_sigma: float,
    ) -> None:
        self.config = dict(config)
        self.nodes = {
            (int(hue), int(sat)): {str(key): float(value) for key, value in features.items()}
            for (hue, sat), features in nodes.items()
        }
        self.zero_direction = {str(key): float(value) for key, value in zero_direction.items()}
        self.zero_scales = {int(key): float(value) for key, value in zero_scales.items()}
        self.repeatability_three_sigma = float(repeatability_three_sigma)
        missing = [(hue, sat) for hue in HUE_NODES for sat in SAT_NODES[1:] if (hue, sat) not in self.nodes]
        if missing:
            raise ValueError(f"Ray HSI manifold is missing measured nodes: {missing}")
        if set(self.zero_scales) != set(SAT0_HUES):
            raise ValueError("Ray HSI manifold requires six SAT0 scale anchors")
        if self.repeatability_three_sigma <= 0:
            raise ValueError("Ray HSI repeatability must be positive")
        self.coordinate_feature_ids = tuple(sorted(
            set.intersection(*(set(features) for features in self.nodes.values()), set(self.zero_direction))
        ))
        if len(self.coordinate_feature_ids) < 4:
            raise ValueError("Ray HSI manifold has fewer than four globally reliable coordinate features")

    @classmethod
    def load(cls, config_path: str | Path = DEFAULT_CONFIG) -> "RayHsiManifold":
        path = Path(config_path)
        config = _load_json(path)
        if config.get("status") != "measured_gate5_frozen":
            raise ValueError("Ray HSI manifold config is not Gate-5 frozen")
        if config.get("gate5", {}).get("decision") != "full_periodic_2d_HB":
            raise ValueError("Ray HSI manifold config does not select full_periodic_2d_HB")
        run_ref = config["inputs"]["run"]
        analysis_ref = config["inputs"]["analysis"]
        run_dir = Path(run_ref["path"])
        _require_sha256(run_dir / "run.json", run_ref["run_json_sha256"])
        _require_sha256(run_dir / "plan.json", run_ref["plan_json_sha256"])
        analysis_path = Path(analysis_ref["path"])
        _require_sha256(analysis_path, analysis_ref["sha256"])
        analysis = _load_json(analysis_path)
        if analysis.get("status") != "ready_for_manual_gate5_decision":
            raise ValueError("frozen Ray HSI analysis is not complete")

        captures = _load_jsonl(run_dir / "captures.jsonl")
        groups: dict[tuple[int, int], list[dict[str, float]]] = {}
        for record in captures:
            if record.get("source") != "ray" or record.get("ray_mode") != "hsi":
                continue
            state = record.get("ray_state") or {}
            key = (int(state["hue"]), int(state["sat"]))
            report = _load_json(Path(record["capture"]["patch_statistics"]))
            groups.setdefault(key, []).append(_accepted_features(report))

        centers = {key: _feature_center(values) for key, values in groups.items()}
        sat0_centers = {hue: centers[(hue, 0)] for hue in SAT0_HUES}
        zero_direction, zero_scales = _pooled_zero_direction(sat0_centers)
        nodes = {
            (hue, sat): centers[(hue, sat)]
            for hue in HUE_NODES
            for sat in SAT_NODES[1:]
        }
        return cls(
            config=config,
            nodes=nodes,
            zero_direction=zero_direction,
            zero_scales=zero_scales,
            repeatability_three_sigma=float(analysis["repeatability"]["three_sigma_proxy"]),
        )

    def target_at(self, hue: float, sat: float) -> ManifoldTarget:
        normalized_hue = float(hue) % 360.0
        bounded_sat = min(max(float(sat), 0.0), 100.0)
        lower_hue = int(math.floor(normalized_hue / 30.0) * 30) % 360
        upper_hue = (lower_hue + 30) % 360
        hue_fraction = (normalized_hue - lower_hue) / 30.0
        if upper_hue == 0 and normalized_hue >= 330:
            hue_fraction = (normalized_hue - 330.0) / 30.0
        lower_sat, upper_sat = _bracket(SAT_NODES, bounded_sat)
        sat_fraction = 0.0 if upper_sat == lower_sat else (bounded_sat - lower_sat) / (upper_sat - lower_sat)

        corners = {
            (lower_hue, lower_sat): self._node(lower_hue, lower_sat),
            (upper_hue, lower_sat): self._node(upper_hue, lower_sat),
            (lower_hue, upper_sat): self._node(lower_hue, upper_sat),
            (upper_hue, upper_sat): self._node(upper_hue, upper_sat),
        }
        common = set.intersection(*(set(values) for values in corners.values()))
        if not common:
            raise ValueError(f"Ray HSI target {hue}/{sat} has no common reliable features")
        features = {}
        for feature in sorted(common):
            low = _lerp(corners[(lower_hue, lower_sat)][feature], corners[(upper_hue, lower_sat)][feature], hue_fraction)
            high = _lerp(corners[(lower_hue, upper_sat)][feature], corners[(upper_hue, upper_sat)][feature], hue_fraction)
            features[feature] = _lerp(low, high, sat_fraction)
        return ManifoldTarget(
            hue=normalized_hue,
            sat=bounded_sat,
            features=features,
            interpolation={
                "hue_nodes": [lower_hue, upper_hue],
                "hue_fraction": hue_fraction,
                "sat_nodes": [lower_sat, upper_sat],
                "sat_fraction": sat_fraction,
                "common_feature_count": len(features),
            },
        )

    def coordinate(self, candidate_features: Mapping[str, float], *, target_hue: float, target_sat: float) -> ManifoldCoordinate:
        target = self.target_at(target_hue, target_sat)
        missing = [feature for feature in self.coordinate_feature_ids if feature not in candidate_features]
        if missing:
            raise ValueError(f"candidate is missing {len(missing)} frozen Ray HSI coordinate features")
        common = list(self.coordinate_feature_ids)
        candidate = np.asarray([float(candidate_features[key]) for key in common], dtype=float)
        target_values = np.asarray([target.features[key] for key in common], dtype=float)
        target_unit = _unit(target_values)
        candidate_unit = _unit(candidate)
        shape = float(np.linalg.norm(candidate_unit - target_unit))
        if float(target.sat) == 0.0:
            return self._sat0_coordinate(
                candidate,
                candidate_unit,
                target,
                target_values,
                common,
                shape,
            )
        estimated_hue = float(target.hue)
        estimated_sat = float(target.sat)
        matrix = np.empty((len(common), 2), dtype=float)
        for _index in range(8):
            current = self.target_at(estimated_hue, estimated_sat)
            matrix = self._coordinate_tangents(estimated_hue, estimated_sat, common)
            residual = candidate_unit - _unit([current.features[key] for key in common])
            delta, _, _, _ = np.linalg.lstsq(matrix, residual, rcond=None)
            hue_step = min(max(float(delta[0]), -15.0), 15.0)
            sat_step = min(max(float(delta[1]), -15.0), 15.0)
            estimated_hue = (estimated_hue + hue_step) % 360.0
            estimated_sat = min(max(estimated_sat + sat_step, 0.0), 100.0)
            if abs(hue_step) < 1e-5 and abs(sat_step) < 1e-5:
                break
        fitted_target = self.target_at(estimated_hue, estimated_sat)
        orthogonal = float(np.linalg.norm(candidate_unit - _unit([fitted_target.features[key] for key in common])))
        matrix = self._coordinate_tangents(float(target.hue), float(target.sat), common)
        condition = float(np.linalg.cond(matrix))
        denominator = float(candidate @ candidate)
        scale = 0.0 if denominator <= 0 else float(candidate @ target_values / denominator)
        pseudo = np.linalg.pinv(matrix)
        coordinate_noise = self.repeatability_three_sigma * np.linalg.norm(pseudo, axis=1)
        return ManifoldCoordinate(
            target_hue=float(target.hue),
            target_sat=float(target.sat),
            hue_error_degrees=_signed_hue_delta(estimated_hue, target.hue),
            sat_error_percent=float(estimated_sat - target.sat),
            orthogonal_residual=orthogonal,
            shape_residual=shape,
            global_scale_candidate_to_target=scale,
            common_feature_count=len(common),
            tangent_condition_number=condition,
            hue_three_sigma_degrees=float(coordinate_noise[0]),
            sat_three_sigma_percent=float(coordinate_noise[1]),
            feature_ids=tuple(common),
        )

    def _sat0_coordinate(
        self,
        candidate: np.ndarray,
        candidate_unit: np.ndarray,
        target: ManifoldTarget,
        target_values: np.ndarray,
        features: Sequence[str],
        shape: float,
    ) -> ManifoldCoordinate:
        estimated_sat = 0.0
        sat_tangent = np.empty(len(features), dtype=float)
        for _index in range(8):
            current = self.target_at(target.hue, estimated_sat)
            upper = min(estimated_sat + 1.0, 100.0)
            current_unit = _unit([current.features[key] for key in features])
            upper_target = self.target_at(target.hue, upper)
            sat_tangent = (
                _unit([upper_target.features[key] for key in features]) - current_unit
            ) / (upper - estimated_sat)
            denominator = float(sat_tangent @ sat_tangent)
            if denominator <= 1e-18:
                break
            step = float(sat_tangent @ (candidate_unit - current_unit) / denominator)
            step = min(max(step, -15.0), 15.0)
            estimated_sat = min(max(estimated_sat + step, 0.0), 100.0)
            if abs(step) < 1e-5:
                break
        fitted = self.target_at(target.hue, estimated_sat)
        orthogonal = float(np.linalg.norm(candidate_unit - _unit([fitted.features[key] for key in features])))
        denominator = float(candidate @ candidate)
        scale = 0.0 if denominator <= 0 else float(candidate @ target_values / denominator)
        tangent_norm = float(np.linalg.norm(sat_tangent))
        sat_noise = 100.0 if tangent_norm <= 1e-12 else self.repeatability_three_sigma / tangent_norm
        return ManifoldCoordinate(
            target_hue=float(target.hue),
            target_sat=0.0,
            hue_error_degrees=0.0,
            sat_error_percent=float(estimated_sat),
            orthogonal_residual=orthogonal,
            shape_residual=shape,
            global_scale_candidate_to_target=scale,
            common_feature_count=len(features),
            tangent_condition_number=1.0,
            hue_three_sigma_degrees=180.0,
            sat_three_sigma_percent=float(sat_noise),
            feature_ids=tuple(features),
        )

    def _coordinate_tangents(self, hue: float, sat: float, features: Sequence[str]) -> np.ndarray:
        hue_before = self.target_at(hue - 1.0, sat)
        hue_after = self.target_at(hue + 1.0, sat)
        sat_low = max(0.0, float(sat) - 1.0)
        sat_high = min(100.0, float(sat) + 1.0)
        sat_before = self.target_at(hue, sat_low)
        sat_after = self.target_at(hue, sat_high)
        hue_tangent = (
            _unit([hue_after.features[key] for key in features])
            - _unit([hue_before.features[key] for key in features])
        ) / 2.0
        sat_tangent = (
            _unit([sat_after.features[key] for key in features])
            - _unit([sat_before.features[key] for key in features])
        ) / (sat_high - sat_low)
        return np.column_stack((hue_tangent, sat_tangent))

    def _node(self, hue: int, sat: int) -> dict[str, float]:
        if sat == 0:
            scale = _periodic_scalar(self.zero_scales, hue)
            return {feature: value * scale for feature, value in self.zero_direction.items()}
        return self.nodes[(hue, sat)]


def _accepted_features(report: Mapping[str, Any]) -> dict[str, float]:
    collection = collect_patch_plane_features([report])
    return {
        str(item["feature_id"]): float(item["value"])
        for item in collection["observations"]
        if item["status"] == "included"
        and item["quality_status"] == "accepted"
        and item["value"] is not None
    }


def _feature_center(samples: Sequence[Mapping[str, float]]) -> dict[str, float]:
    if not samples:
        raise ValueError("cannot center an empty Ray HSI sample group")
    common = set(samples[0])
    for sample in samples[1:]:
        common.intersection_update(sample)
    if not common:
        raise ValueError("Ray HSI repeated samples have no common reliable features")
    return {
        feature: float(np.median([sample[feature] for sample in samples]))
        for feature in sorted(common)
    }


def _pooled_zero_direction(centers: Mapping[int, Mapping[str, float]]) -> tuple[dict[str, float], dict[int, float]]:
    common = set.intersection(*(set(center) for center in centers.values()))
    if not common:
        raise ValueError("SAT0 centers have no common reliable features")
    feature_order = sorted(common)
    normalized = []
    vectors = {}
    for hue, center in centers.items():
        vector = np.asarray([center[feature] for feature in feature_order], dtype=float)
        vectors[hue] = vector
        normalized.append(_unit(vector))
    direction = _unit(np.median(np.vstack(normalized), axis=0))
    scales = {hue: float(vector @ direction) for hue, vector in vectors.items()}
    return ({feature: float(direction[index]) for index, feature in enumerate(feature_order)}, scales)


def _periodic_scalar(values: Mapping[int, float], hue: float) -> float:
    normalized = float(hue) % 360.0
    lower = int(math.floor(normalized / 60.0) * 60) % 360
    upper = (lower + 60) % 360
    fraction = (normalized - lower) / 60.0
    if upper == 0 and normalized >= 300:
        fraction = (normalized - 300.0) / 60.0
    return _lerp(float(values[lower]), float(values[upper]), fraction)


def _bracket(nodes: Sequence[int], value: float) -> tuple[int, int]:
    for node in nodes:
        if value == node:
            return node, node
    for left, right in zip(nodes, nodes[1:]):
        if left < value < right:
            return left, right
    return nodes[-1], nodes[-1]


def _unit(values: Sequence[float] | np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    norm = float(np.linalg.norm(array))
    if norm <= 0 or not np.isfinite(norm):
        raise ValueError("Ray HSI feature vector must have positive finite norm")
    return array / norm


def _lerp(left: float, right: float, fraction: float) -> float:
    return (1.0 - float(fraction)) * float(left) + float(fraction) * float(right)


def _signed_hue_delta(value: float, reference: float) -> float:
    return (float(value) - float(reference) + 180.0) % 360.0 - 180.0


def _require_sha256(path: Path, expected: str) -> None:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != str(expected):
        raise ValueError(f"frozen input hash mismatch for {path}: expected {expected}, got {actual}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
