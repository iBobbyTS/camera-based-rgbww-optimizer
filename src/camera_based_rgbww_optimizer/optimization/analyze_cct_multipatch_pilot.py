from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.optimization.multipatch_objective import (
    objective_from_residual_groups,
)


GROUPS = ("neutral", "white", "training", "holdout")
COLOR_METRICS = ("mean", "p90", "maximum")


def analyze_cct_multipatch_pilot(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    run = _load_json(root / "run.json")
    if run.get("phase") != "P4" or run.get("status") != "complete":
        raise ValueError("P4 analysis requires a completed P4 run")
    if int(run.get("completed_target_count", -1)) != 12:
        raise ValueError("P4 analysis requires exactly 12 completed targets")
    if (root / "failure.json").exists():
        raise ValueError("P4 run contains failure.json")
    python_cleanup = _load_json(root / "all-off-python.json")
    shell_cleanup = _load_json(root / "all-off-shell.json")
    if not _cleanup_ok(python_cleanup) or not _cleanup_ok(shell_cleanup):
        raise ValueError("P4 analysis requires successful Python and shell cleanup")

    captures = _load_jsonl(root / "captures.jsonl")
    targets = _load_jsonl(root / "target-results.jsonl")
    if len(targets) != 12:
        raise ValueError(f"P4 target-results must contain 12 rows, found {len(targets)}")
    capture_validation = _validate_captures(root, captures)
    point_results = [
        _analyze_unreachable_target(item)
        if item.get("status") == "measurement_unreachable"
        else _analyze_target(item)
        for item in targets
    ]
    if len({(item["cct_K"], item["gm_raw"]) for item in point_results}) != 12:
        raise ValueError("P4 target grid contains duplicates or missing points")
    evaluable_points = [item for item in point_results if item["status"] == "complete"]
    unreachable_points = [item for item in point_results if item["status"] == "measurement_unreachable"]

    aggregate_metrics: dict[str, Any] = {}
    aggregate_passes = []
    for group in ("training", "holdout"):
        aggregate_metrics[group] = {}
        for metric in COLOR_METRICS:
            if not evaluable_points:
                aggregate_metrics[group][metric] = {"status": "not_available"}
                aggregate_passes.append(False)
                continue
            baseline = np.asarray([item["baseline_center"][group][metric] for item in evaluable_points])
            candidate = np.asarray([item["candidate_center"][group][metric] for item in evaluable_points])
            noise = np.asarray([item["baseline_repeatability_3sigma"][group][metric] for item in evaluable_points])
            summary = {
                "baseline_grid_mean": float(np.mean(baseline)),
                "candidate_grid_mean": float(np.mean(candidate)),
                "grid_mean_improvement": float(np.mean(baseline) - np.mean(candidate)),
                "baseline_grid_p90": float(np.quantile(baseline, 0.9)),
                "candidate_grid_p90": float(np.quantile(candidate, 0.9)),
                "grid_p90_improvement": float(np.quantile(baseline, 0.9) - np.quantile(candidate, 0.9)),
                "baseline_grid_worst": float(np.max(baseline)),
                "candidate_grid_worst": float(np.max(candidate)),
                "grid_worst_improvement": float(np.max(baseline) - np.max(candidate)),
                "repeatability_3sigma_p90": float(np.quantile(noise, 0.9)),
            }
            summary["improvements_exceed_repeatability"] = all(
                summary[name] > summary["repeatability_3sigma_p90"]
                for name in ("grid_mean_improvement", "grid_p90_improvement", "grid_worst_improvement")
            )
            aggregate_passes.append(bool(summary["improvements_exceed_repeatability"]))
            aggregate_metrics[group][metric] = summary

    all_points_evaluable = len(evaluable_points) == 12
    all_settled = all_points_evaluable and all(item["settled_candidate_count"] == 2 for item in evaluable_points)
    all_hard_gates = all_points_evaluable and all(item["all_settled_hard_gates_pass"] for item in evaluable_points)
    all_white_nonworse = all_points_evaluable and all(item["white_point_nonworse"] for item in evaluable_points)
    all_feedback_confirmed = all_points_evaluable and all(item["feedback_goal_confirmed"] for item in evaluable_points)
    gate_a_evidence = bool(
        all_settled and all_hard_gates and all_white_nonworse
        and all(aggregate_passes) and _commands_have_full_scale(evaluable_points)
    )
    return {
        "schema_version": 2,
        "analysis": "cct_multipatch_pilot_gate3",
        "status": "ready_for_manual_gate3_decision",
        "run_dir": str(root),
        "run_json_sha256": _sha256(root / "run.json"),
        "capture_validation": capture_validation,
        "cleanup": {"python": python_cleanup, "shell": shell_cleanup},
        "point_count": len(point_results),
        "evaluable_point_count": len(evaluable_points),
        "measurement_unreachable_point_count": len(unreachable_points),
        "points": point_results,
        "aggregate": {
            "training_holdout": aggregate_metrics,
            "settled_candidate_count_is_two_for_all_points": all_settled,
            "all_settled_hard_gates_pass": all_hard_gates,
            "all_white_points_nonworse": all_white_nonworse,
            "all_feedback_goal_confirmed": all_feedback_confirmed,
            "command_continuity": _command_continuity(evaluable_points, all_points=point_results),
            "rgb_fraction": _distribution([item["rgb_fraction"] for item in evaluable_points]) if evaluable_points else {"status": "not_available"},
        },
        "decision_hints": {
            "c_a_evidence_complete": gate_a_evidence,
            "measurement_unreachable_points": [item["target_id"] for item in unreachable_points],
            "measurement_unreachable_extreme_cct_only": _unreachable_extreme_cct_only(point_results),
            "nonconverged_points": [item["target_id"] for item in evaluable_points if not item["feedback_goal_confirmed"]],
            "hard_gate_failed_points": [item["target_id"] for item in evaluable_points if not item["all_settled_hard_gates_pass"]],
            "white_worse_points": [item["target_id"] for item in evaluable_points if not item["white_point_nonworse"]],
            "automatic_gate3_selection": False,
        },
        "notes": [
            "C-A still requires an advanced-model Gate-3 decision; this analyzer never expands to 70 points.",
            "Improvement is baseline minus candidate. Positive values are better.",
            "The repeatability comparison uses three-sigma variation across the three same-run baseline captures.",
            "Candidate settled evidence is the confirmed pair, or the explicit final-verification pair when feedback did not converge.",
            "A measurement_unreachable point is excluded from numerical aggregates and makes C-A impossible; its frozen quality evidence remains in the point record.",
        ],
    }


def write_analysis(run_dir: str | Path, *, output: str | Path | None = None) -> Path:
    root = Path(run_dir)
    destination = Path(output) if output is not None else root / "gate3-analysis.json"
    analysis = analyze_cct_multipatch_pilot(root)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(json.dumps(analysis, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return destination


def _analyze_target(result: Mapping[str, Any]) -> dict[str, Any]:
    baseline = list(result["baseline"])
    if len(baseline) != 3:
        raise ValueError("each P4 target requires three baseline observations")
    settled = _settled_candidate_samples(result)
    if len(settled) != 2:
        raise ValueError("each P4 target requires two settled candidate observations")
    tolerance = float(result["neutral_chroma_tolerance"])
    baseline_center = _center_objective(baseline, tolerance)
    candidate_center = _center_objective(settled, tolerance)
    repeatability = {
        group: {
            metric: _three_sigma([float(item["objective"][group][metric]) for item in baseline])
            for metric in COLOR_METRICS
        }
        for group in ("training", "holdout")
    }
    baseline_white = [float(item["objective"]["white_point"]["goal_score"]) for item in baseline]
    white_allowance = _three_sigma(baseline_white)
    white_nonworse = (
        float(candidate_center["white_point"]["goal_score"])
        <= float(baseline_center["white_point"]["goal_score"]) + white_allowance
    )
    command = {name: int(result["feedback"]["selected_command"][name]) for name in ("cw", "ww", "r", "g", "b")}
    total = sum(command.values())
    target = result["target"]
    return {
        "status": "complete",
        "target_id": f"{int(target['cct_K'])}K-gm{int(target['gm_raw'])}",
        "cct_K": int(target["cct_K"]),
        "gm_raw": int(target["gm_raw"]),
        "baseline_command": dict(target["baseline_command"]),
        "candidate_command": command,
        "candidate_max_channel": max(command.values()),
        "rgb_fraction": 0.0 if total <= 0 else float((command["r"] + command["g"] + command["b"]) / total),
        "feedback_goal_confirmed": bool(result["feedback"]["goal_confirmed"]),
        "feedback_status": str(result["feedback"]["status"]),
        "settled_candidate_count": len(settled),
        "settled_candidate_objectives": [item["objective"] for item in settled],
        "all_settled_hard_gates_pass": all(bool(item["objective"]["feasible"]) for item in settled),
        "white_point_nonworse": bool(white_nonworse),
        "white_repeatability_3sigma": white_allowance,
        "baseline_center": baseline_center,
        "candidate_center": candidate_center,
        "baseline_repeatability_3sigma": repeatability,
    }


def _analyze_unreachable_target(result: Mapping[str, Any]) -> dict[str, Any]:
    target = result.get("target", {})
    if result.get("reason") != "weak_signal_after_max_validated_exposure":
        raise ValueError("unsupported P4 measurement_unreachable reason")
    envelope = [float(value) for value in result.get("validated_exposure_envelope", [])]
    if envelope != [1.0, 1.25]:
        raise ValueError("P4 measurement_unreachable must preserve the frozen 1.0x..1.25x envelope")
    evidence = result.get("evidence")
    if not isinstance(evidence, Mapping) or not evidence.get("rejected_features"):
        raise ValueError("P4 measurement_unreachable requires rejected-feature evidence")
    cct = int(target["cct_K"])
    gm = int(target["gm_raw"])
    return {
        "status": "measurement_unreachable",
        "target_id": f"{cct}K-gm{gm}",
        "cct_K": cct,
        "gm_raw": gm,
        "baseline_command": dict(target["baseline_command"]),
        "stage": str(result.get("stage")),
        "reason": str(result["reason"]),
        "validated_exposure_envelope": envelope,
        "evidence": dict(evidence),
    }


def _settled_candidate_samples(result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    feedback = result["feedback"]
    confirmed = [item for item in feedback["confirmation_attempts"] if item.get("status") == "confirmed"]
    if confirmed:
        by_index = {int(item["index"]): item for item in feedback["samples"]}
        return [by_index[int(index)] for index in confirmed[-1]["sample_indices"]]
    return list(result.get("final_verification", []))


def _center_objective(samples: Sequence[Mapping[str, Any]], tolerance: float) -> dict[str, Any]:
    residuals = {
        group: np.median(np.stack([np.asarray(item["residuals"][group], dtype="float64") for item in samples]), axis=0)
        for group in GROUPS
    }
    return objective_from_residual_groups(residuals, neutral_chroma_tolerance=tolerance)


def _validate_captures(root: Path, captures: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not captures:
        raise ValueError("P4 run has no captures")
    raw_files = []
    measurement_files = []
    recorded = 0
    for item in captures:
        capture = item["capture"]
        raw = Path(capture["capture"]["saved_file"])
        measurement = Path(capture["patch_statistics"])
        if not raw.is_file() or raw.stat().st_size <= 0:
            raise ValueError(f"missing or empty P4 RAW: {raw}")
        if not measurement.is_file():
            raise ValueError(f"missing P4 measurement: {measurement}")
        report = _load_json(measurement)
        if report.get("exposure_metadata", {}).get("status") != "recorded":
            raise ValueError(f"P4 capture lacks recorded exposure: {measurement}")
        recorded += 1
        raw_files.append(str(raw))
        measurement_files.append(str(measurement))
    npy = list(root.rglob("*.npy"))
    if npy:
        raise ValueError(f"P4 run retained {len(npy)} .npy files")
    return {
        "capture_count": len(captures),
        "raw_count": len(raw_files),
        "measurement_count": len(measurement_files),
        "recorded_exposure_count": recorded,
        "npy_count": 0,
    }


def _cleanup_ok(value: Any) -> bool:
    steps = value if isinstance(value, list) else value.get("steps", []) if isinstance(value, Mapping) else []
    return len(steps) == 2 and all(isinstance(step, Mapping) and bool(step.get("ok")) for step in steps)


def _commands_have_full_scale(points: Sequence[Mapping[str, Any]]) -> bool:
    return all(int(item["candidate_max_channel"]) == 4095 for item in points)


def _command_continuity(
    points: Sequence[Mapping[str, Any]], *, all_points: Sequence[Mapping[str, Any]] | None = None
) -> dict[str, Any]:
    by_target = {(int(item["cct_K"]), int(item["gm_raw"])): item for item in points}
    grid_points = points if all_points is None else all_points
    ccts = sorted({int(item["cct_K"]) for item in grid_points})
    gms = sorted({int(item["gm_raw"]) for item in grid_points})
    edges = []
    omitted_edges = []
    for gm in gms:
        for left, right in zip(ccts, ccts[1:]):
            if (left, gm) in by_target and (right, gm) in by_target:
                edges.append(_command_edge(by_target[(left, gm)], by_target[(right, gm)], "cct"))
            else:
                omitted_edges.append({"axis": "cct", "left": f"{left}K-gm{gm}", "right": f"{right}K-gm{gm}"})
    for cct in ccts:
        for left, right in zip(gms, gms[1:]):
            if (cct, left) in by_target and (cct, right) in by_target:
                edges.append(_command_edge(by_target[(cct, left)], by_target[(cct, right)], "gm"))
            else:
                omitted_edges.append({"axis": "gm", "left": f"{cct}K-gm{left}", "right": f"{cct}K-gm{right}"})
    return {
        "edge_count": len(edges),
        "possible_edge_count": len(edges) + len(omitted_edges),
        "omitted_edge_count": len(omitted_edges),
        "omitted_edges": omitted_edges,
        "normalized_l1": _distribution([edge["normalized_l1"] for edge in edges]) if edges else {"status": "not_available"},
        "worst_edges": sorted(edges, key=lambda edge: edge["normalized_l1"], reverse=True)[:5],
    }


def _unreachable_extreme_cct_only(points: Sequence[Mapping[str, Any]]) -> bool:
    unreachable = [item for item in points if item["status"] == "measurement_unreachable"]
    if not unreachable:
        return False
    ccts = [int(item["cct_K"]) for item in points]
    extremes = {min(ccts), max(ccts)}
    return all(int(item["cct_K"]) in extremes for item in unreachable)


def _command_edge(left: Mapping[str, Any], right: Mapping[str, Any], axis: str) -> dict[str, Any]:
    channels = ("cw", "ww", "r", "g", "b")
    distance = sum(abs(int(left["candidate_command"][name]) - int(right["candidate_command"][name])) for name in channels)
    return {
        "axis": axis,
        "left": left["target_id"],
        "right": right["target_id"],
        "normalized_l1": float(distance / (4095 * len(channels))),
    }


def _distribution(values: Sequence[float]) -> dict[str, float]:
    array = np.asarray(values, dtype="float64")
    return {
        "minimum": float(np.min(array)),
        "median": float(np.median(array)),
        "p90": float(np.quantile(array, 0.9)),
        "maximum": float(np.max(array)),
    }


def _three_sigma(values: Sequence[float]) -> float:
    return 0.0 if len(values) < 2 else float(3.0 * np.std(np.asarray(values), ddof=1))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a completed P4 CCT multipatch pilot")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    print(write_analysis(args.run_dir, output=args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
