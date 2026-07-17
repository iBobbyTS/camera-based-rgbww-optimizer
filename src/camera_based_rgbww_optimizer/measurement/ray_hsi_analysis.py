from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import collect_patch_plane_features


EXPECTED_CAPTURE_COUNT = 106
PRIMARY_HUES = (0, 60, 120, 180, 240, 300)
RGB_TO_HUE = {"r": 0, "y": 60, "g": 120, "c": 180, "b": 240, "m": 300}
SATURATIONS = (5, 20, 50, 80, 95, 100)


def analyze_ray_hsi_run(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    run = _load_json(root / "run.json")
    if run.get("phase") != "P6" or run.get("status") != "complete":
        raise ValueError("P6 analysis requires a completed P6 run")
    if int(run.get("completed_capture_count", -1)) != EXPECTED_CAPTURE_COUNT:
        raise ValueError(f"P6 analysis requires {EXPECTED_CAPTURE_COUNT} completed captures")
    if (root / "failure.json").exists():
        raise ValueError("P6 run contains failure.json")
    python_cleanup = _load_json_value(root / "all-off-python.json")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if not _cleanup_ok(python_cleanup) or not _cleanup_ok(shell_cleanup):
        raise ValueError("P6 analysis requires successful Python and shell cleanup")
    npy_count = len(list(root.rglob("*.npy")))
    if npy_count:
        raise ValueError("P6 run must not retain .npy files")

    captures = _load_jsonl(root / "captures.jsonl")
    if len(captures) != EXPECTED_CAPTURE_COUNT:
        raise ValueError(f"P6 captures.jsonl must contain {EXPECTED_CAPTURE_COUNT} rows")
    samples: list[dict[str, Any]] = []
    raw_count = 0
    recorded_count = 0
    for record in captures:
        capture = record.get("capture", {})
        raw_path = Path(str(capture.get("capture", {}).get("saved_file", "")))
        if not raw_path.is_file() or raw_path.stat().st_size <= 0:
            raise ValueError(f"missing or empty CR3 for {record.get('capture_id')}")
        raw_count += 1
        report_path = Path(str(capture.get("patch_statistics", "")))
        report = _load_json(report_path)
        if report.get("exposure_metadata", {}).get("status") != "recorded":
            raise ValueError(f"capture {record.get('capture_id')} lacks recorded exposure")
        recorded_count += 1
        if record.get("source") == "ambient":
            continue
        samples.append(_sample_from_report(record, report))

    analysis = analyze_ray_hsi_samples(samples)
    return {
        "schema_version": 1,
        "analysis": "ray_hsi_manifold_gate5",
        "status": "ready_for_manual_gate5_decision",
        "run_dir": str(root),
        "run_json_sha256": _sha256(root / "run.json"),
        "capture_validation": {
            "capture_count": len(captures),
            "raw_count": raw_count,
            "recorded_exposure_count": recorded_count,
            "measurement_count": len(captures),
            "npy_count": npy_count,
        },
        "cleanup": {"python": python_cleanup, "shell": shell_cleanup},
        **analysis,
    }


def analyze_ray_hsi_samples(samples: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not samples:
        raise ValueError("at least one P6 Ray sample is required")
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    all_feature_ids: set[str] = set()
    accepted_counts: list[int] = []
    rejected_counts: list[int] = []
    for raw in samples:
        sample = dict(raw)
        values = {str(key): float(value) for key, value in dict(sample.get("features", {})).items() if math.isfinite(float(value))}
        if not values:
            raise ValueError(f"sample {sample.get('capture_id')} has no reliable features")
        sample["features"] = values
        key = _sample_key(sample)
        grouped[key].append(sample)
        all_feature_ids.update(values)
        accepted_counts.append(len(values))
        rejected_counts.append(int(sample.get("rejected_feature_count", 0)))

    repeatability = _repeatability(grouped)
    sat0 = _analyze_sat0(grouped, repeatability)
    endpoints = _analyze_mode_endpoints(grouped, repeatability)
    manifold = _analyze_manifold_candidates(grouped, repeatability)
    periodicity = _analyze_periodicity(grouped)
    missing = _required_state_gaps(grouped)
    invalid_for_model = bool(missing or sat0["status"] == "insufficient_reliable_features")
    return {
        "sample_count": len(samples),
        "quality_coverage": {
            "feature_universe_count": len(all_feature_ids),
            "accepted_feature_count": _distribution(accepted_counts),
            "rejected_feature_count": _distribution(rejected_counts),
            "required_state_gaps": missing,
        },
        "repeatability": repeatability,
        "sat0": sat0,
        "hsi_rgb_endpoints": endpoints,
        "affine_separability": manifold,
        "hue_periodicity": periodicity,
        "decision_hints": {
            "automatic_gate5_selection": False,
            "run_invalid_for_model_selection": invalid_for_model,
            "sat0_hue_effect_exceeds_3sigma": sat0.get("hue_effect_exceeds_3sigma"),
            "endpoint_modes_shape_compatible": endpoints.get("all_within_3sigma"),
            "ha_suggested_condition_met": any(
                candidate.get("ha_suggested_condition_met") is True
                for candidate in manifold["candidates"].values()
            ),
            "candidate_branches": ["separable_manifold_HA", "full_periodic_2d_HB", "targeted_resample_HC", "invalidate_and_repeat_HD", "stop_hsi_route"],
        },
        "notes": [
            "Only features accepted by the frozen RAW observer quality gate enter numerical comparisons.",
            "All shape residuals remove one global scale; this does not establish absolute brightness equality.",
            "The analyzer reports candidate evidence only and never selects Gate-5 automatically.",
        ],
    }


def _sample_from_report(record: Mapping[str, Any], report: Mapping[str, Any]) -> dict[str, Any]:
    collection = collect_patch_plane_features([report])
    features = {
        str(item["feature_id"]): float(item["value"])
        for item in collection["observations"]
        if item["status"] == "included" and item["quality_status"] == "accepted" and item["value"] is not None
    }
    rejected = len(collection["observations"]) - len(features)
    context = dict(record.get("analysis_context", {}))
    return {
        "capture_id": record["capture_id"],
        "mode": record.get("ray_mode"),
        "state": dict(record.get("ray_state") or {}),
        "family": context.get("family"),
        "endpoint": context.get("endpoint"),
        "repeat_index": record.get("repeat_index"),
        "features": features,
        "rejected_feature_count": rejected,
    }


def _sample_key(sample: Mapping[str, Any]) -> tuple[Any, ...]:
    mode = sample.get("mode")
    state = sample.get("state", {})
    if mode == "hsi":
        return ("hsi", int(state["hue"]), int(state["sat"]))
    if mode == "rgb":
        return ("rgb", str(sample.get("endpoint")))
    raise ValueError(f"unsupported sample mode: {mode}")


def _repeatability(grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    groups = []
    residuals = []
    for key, samples in grouped.items():
        if len(samples) < 2:
            continue
        pair_values = [_shape_residual(left["features"], right["features"]) for left, right in itertools.combinations(samples, 2)]
        usable = [item for item in pair_values if item["status"] == "ok"]
        residuals.extend(float(item["relative_residual"]) for item in usable)
        groups.append({"state": list(key), "repeat_count": len(samples), "pair_count": len(usable), "shape_residual": _distribution([item["relative_residual"] for item in usable])})
    return {"groups": groups, "group_count": len(groups), "shape_residual": _distribution(residuals), "three_sigma_proxy": 3.0 * _robust_sigma(residuals)}


def _analyze_sat0(grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]], repeatability: Mapping[str, Any]) -> dict[str, Any]:
    centers = {hue: _center(grouped.get(("hsi", hue, 0), [])) for hue in PRIMARY_HUES}
    if any(center is None for center in centers.values()):
        return {"status": "insufficient_reliable_features", "missing_hues": [hue for hue, center in centers.items() if center is None]}
    comparisons = []
    for left_hue, right_hue in itertools.combinations(PRIMARY_HUES, 2):
        item = _shape_residual(centers[left_hue], centers[right_hue])
        item.update({"left_hue": left_hue, "right_hue": right_hue})
        comparisons.append(item)
    residuals = [float(item["relative_residual"]) for item in comparisons if item["status"] == "ok"]
    threshold = float(repeatability.get("three_sigma_proxy") or 0.0)
    maximum = max(residuals, default=None)
    return {
        "status": "complete",
        "hue_count": len(centers),
        "comparisons": comparisons,
        "hue_effect_shape_residual": _distribution(residuals),
        "repeatability_three_sigma_proxy": threshold,
        "hue_effect_exceeds_3sigma": None if maximum is None else maximum > threshold,
    }


def _analyze_mode_endpoints(grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]], repeatability: Mapping[str, Any]) -> dict[str, Any]:
    rows = []
    threshold = float(repeatability.get("three_sigma_proxy") or 0.0)
    for endpoint, hue in RGB_TO_HUE.items():
        hsi = _center(grouped.get(("hsi", hue, 100), []))
        rgb = _center(grouped.get(("rgb", endpoint), []))
        if hsi is None or rgb is None:
            rows.append({"endpoint": endpoint, "hue": hue, "status": "missing_state"})
            continue
        row = _shape_residual(hsi, rgb)
        row.update({"endpoint": endpoint, "hue": hue, "within_3sigma": row.get("relative_residual", math.inf) <= threshold})
        rows.append(row)
    complete = [row for row in rows if row["status"] == "ok"]
    return {
        "comparisons": rows,
        "complete_count": len(complete),
        "shape_residual": _distribution([row["relative_residual"] for row in complete]),
        "repeatability_three_sigma_proxy": threshold,
        "all_within_3sigma": len(complete) == 6 and all(row["within_3sigma"] for row in complete),
    }


def _analyze_manifold_candidates(
    grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]],
    repeatability: Mapping[str, Any],
) -> dict[str, Any]:
    sat0_centers = {hue: _center(grouped.get(("hsi", hue, 0), [])) for hue in PRIMARY_HUES}
    available = [center for center in sat0_centers.values() if center is not None]
    pooled = _center([{"features": center} for center in available]) if available else None

    def pooled_zero(_hue: int) -> dict[str, float] | None:
        return pooled

    def periodic_zero(hue: int) -> dict[str, float] | None:
        return _periodic_sat0_center(sat0_centers, hue)

    candidates = {
        "pooled_sat0": _analyze_manifold(grouped, repeatability, zero_for_hue=pooled_zero),
        "hue_dependent_periodic_sat0": _analyze_manifold(grouped, repeatability, zero_for_hue=periodic_zero),
    }
    residuals = {
        name: candidate["orthogonal_relative_residual"]["p90"]
        for name, candidate in candidates.items()
        if candidate["orthogonal_relative_residual"]["p90"] is not None
    }
    preferred = min(residuals, key=residuals.get) if residuals else None
    return {
        "status": "candidate_comparison_only",
        "preferred_by_p90_residual": preferred,
        "candidates": candidates,
    }


def _analyze_manifold(
    grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]],
    repeatability: Mapping[str, Any],
    *,
    zero_for_hue: Any,
) -> dict[str, Any]:
    rows = []
    by_hue: dict[int, list[dict[str, Any]]] = defaultdict(list)
    repeat_floor = float(repeatability.get("shape_residual", {}).get("p90") or 0.0)
    threshold = 2.0 * repeat_floor
    for hue in range(0, 360, 30):
        zero = zero_for_hue(hue)
        endpoint = _center(grouped.get(("hsi", hue, 100), []))
        if zero is None or endpoint is None:
            continue
        for sat in SATURATIONS[:-1]:
            sample = _center(grouped.get(("hsi", hue, sat), []))
            if sample is None:
                continue
            row = _affine_projection(zero, endpoint, sample)
            row.update({"hue": hue, "sat": sat, "within_2x_repeatability": row.get("orthogonal_relative_residual", math.inf) <= threshold})
            rows.append(row)
            by_hue[hue].append(row)
    monotonic = []
    for hue, hue_rows in sorted(by_hue.items()):
        ordered = sorted(hue_rows, key=lambda item: item["sat"])
        rho = [item.get("rho") for item in ordered]
        monotonic.append({"hue": hue, "status": "complete" if all(value is not None for value in rho) else "incomplete", "monotonic_non_decreasing": all(float(a) <= float(b) + 1e-12 for a, b in zip(rho, rho[1:])) if all(value is not None for value in rho) else None, "rho": rho})
    complete = [row for row in rows if row["status"] == "ok"]
    within_fraction = sum(bool(row["within_2x_repeatability"]) for row in complete) / len(complete) if complete else 0.0
    return {
        "point_count": len(rows),
        "complete_point_count": len(complete),
        "orthogonal_relative_residual": _distribution([row["orthogonal_relative_residual"] for row in complete]),
        "repeatability_p90": repeat_floor,
        "suggested_2x_repeatability_threshold": threshold,
        "within_threshold_fraction": within_fraction,
        "rho_monotonicity": monotonic,
        "ha_suggested_condition_met": len(complete) == 60 and within_fraction >= 0.90 and all(item["monotonic_non_decreasing"] is True for item in monotonic),
        "points": rows,
    }


def _periodic_sat0_center(
    centers: Mapping[int, dict[str, float] | None], hue: int
) -> dict[str, float] | None:
    normalized = hue % 360
    lower = (normalized // 60) * 60
    upper = (lower + 60) % 360
    left = centers.get(lower)
    right = centers.get(upper)
    if left is None or right is None:
        return None
    if normalized == lower:
        return dict(left)
    fraction = (normalized - lower) / 60.0
    common = sorted(set(left).intersection(right))
    if not common:
        return None
    return {
        feature: (1.0 - fraction) * float(left[feature]) + fraction * float(right[feature])
        for feature in common
    }


def _analyze_periodicity(grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    centers = {hue: _center(grouped.get(("hsi", hue, 100), [])) for hue in range(0, 360, 30)}
    edges = []
    for hue in range(0, 360, 30):
        next_hue = (hue + 30) % 360
        if centers[hue] is None or centers[next_hue] is None:
            edges.append({"from_hue": hue, "to_hue": next_hue, "status": "missing_state"})
            continue
        row = _shape_residual(centers[hue], centers[next_hue])
        row.update({"from_hue": hue, "to_hue": next_hue, "is_periodic_closure": hue == 330})
        edges.append(row)
    complete = [row for row in edges if row["status"] == "ok"]
    closure = next((row for row in complete if row["is_periodic_closure"]), None)
    return {"edges": edges, "edge_shape_residual": _distribution([row["relative_residual"] for row in complete]), "closure_edge": closure}


def _required_state_gaps(grouped: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]]) -> list[list[Any]]:
    expected = {("hsi", hue, 0) for hue in PRIMARY_HUES}
    expected.update(("hsi", hue, sat) for hue in range(0, 360, 30) for sat in SATURATIONS)
    expected.update(("rgb", endpoint) for endpoint in RGB_TO_HUE)
    return [list(key) for key in sorted(expected - set(grouped), key=str)]


def _center(samples: Sequence[Mapping[str, Any]]) -> dict[str, float] | None:
    if not samples:
        return None
    common = set(samples[0]["features"])
    for sample in samples[1:]:
        common.intersection_update(sample["features"])
    if not common:
        return None
    return {feature: float(np.median([sample["features"][feature] for sample in samples])) for feature in sorted(common)}


def _shape_residual(left: Mapping[str, float], right: Mapping[str, float]) -> dict[str, Any]:
    common = sorted(set(left).intersection(right))
    if not common:
        return {"status": "no_common_reliable_features", "common_feature_count": 0}
    a = np.asarray([left[key] for key in common], dtype=float)
    b = np.asarray([right[key] for key in common], dtype=float)
    denominator = float(np.dot(a, a))
    reference_norm = float(np.linalg.norm(b))
    if denominator <= 0 or reference_norm <= 0:
        return {"status": "degenerate", "common_feature_count": len(common)}
    scale = float(np.dot(a, b) / denominator)
    return {"status": "ok", "common_feature_count": len(common), "global_scale_left_to_right": scale, "relative_residual": float(np.linalg.norm(scale * a - b) / reference_norm)}


def _affine_projection(zero: Mapping[str, float], endpoint: Mapping[str, float], sample: Mapping[str, float]) -> dict[str, Any]:
    common = sorted(set(zero).intersection(endpoint, sample))
    if not common:
        return {"status": "no_common_reliable_features", "common_feature_count": 0}
    matrix = np.column_stack(([zero[key] for key in common], [endpoint[key] for key in common])).astype(float)
    target = np.asarray([sample[key] for key in common], dtype=float)
    norm = float(np.linalg.norm(target))
    if norm <= 0:
        return {"status": "degenerate", "common_feature_count": len(common)}
    coefficients, _, _, _ = np.linalg.lstsq(matrix, target, rcond=None)
    fitted = matrix @ coefficients
    total = float(np.sum(coefficients))
    rho = None if abs(total) <= 1e-12 else float(coefficients[1] / total)
    return {"status": "ok", "common_feature_count": len(common), "zero_coefficient": float(coefficients[0]), "endpoint_coefficient": float(coefficients[1]), "rho": rho, "coefficients_nonnegative": bool(np.all(coefficients >= 0)), "orthogonal_relative_residual": float(np.linalg.norm(fitted - target) / norm)}


def _robust_sigma(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    array = np.asarray(values, dtype=float)
    median = float(np.median(array))
    return 1.4826 * float(np.median(np.abs(array - median)))


def _distribution(values: Sequence[float | int]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "minimum": None, "median": None, "p90": None, "maximum": None}
    array = np.asarray(values, dtype=float)
    return {"count": len(values), "minimum": float(np.min(array)), "median": float(np.median(array)), "p90": float(np.quantile(array, 0.9)), "maximum": float(np.max(array))}


def _cleanup_ok(value: Any) -> bool:
    steps = value.get("steps") if isinstance(value, Mapping) else value
    return isinstance(steps, list) and len(steps) == 2 and all(isinstance(step, Mapping) and step.get("ok") is True for step in steps)


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_json_value(path: Path) -> Any:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_ray_hsi_analysis(output_path: str | Path, analysis: Mapping[str, Any]) -> Path:
    path = Path(output_path)
    path.write_text(json.dumps(analysis, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a completed P6 Ray HSI manifold run.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = analyze_ray_hsi_run(args.run_dir)
    output = args.output or args.run_dir / "ray-hsi-analysis.json"
    print(write_ray_hsi_analysis(output, analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
