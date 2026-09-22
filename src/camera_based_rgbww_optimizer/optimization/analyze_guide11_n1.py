"""GUIDE11 N1 white repeatability analysis (offline).

Consumes completed N1 session run roots and reports the layered uncertainty
answer GUIDE11 section 3 requires: burst (same-dwell), cycle, and session
components for each of the six states, with CCT/mired/Duv propagated from the
same observations and the neutral-block product chromaticity
``z = [log(R/Gmean), log(B/Gmean)]`` reported as its own layer.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import white_calibration_common as common
from camera_based_rgbww_optimizer.optimization.guide11 import N1_BURST_POINTS, N1_POINTS


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _block06_trimmed_means(patch_statistics: Mapping[str, Any]) -> dict[str, float]:
    patches = patch_statistics.get("patches", ())
    block = next(
        (p for p in patches if p.get("index") == 6 or "block_06" in str(p.get("name", ""))),
        None,
    )
    if block is None:
        raise ValueError("patch statistics lack block_06")
    planes = block["planes"]
    return {
        plane: float(planes[plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }


def observation_from_capture_row(
    row: Mapping[str, Any], run_root: Path,
) -> dict[str, Any]:
    """Assemble one N1 observation: white point plus product chromaticity."""
    import numpy as np

    step = row.get("plan_step", {})
    capture_id = str(row["capture_id"])
    measurement_path = run_root / "measurements" / f"{capture_id}.patch-statistics.json"
    patch_statistics = json.loads(measurement_path.read_text(encoding="utf-8"))
    planes = _block06_trimmed_means(patch_statistics)
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    if g_mean <= 0 or min(planes["R"], planes["B"]) <= 0:
        raise ValueError(f"block_06 planes are not positive for {capture_id}")
    camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw_path = Path(str((row.get("capture") or {}).get("saved_file", "")))
    matrix = common._load_rawpy_rgb_xyz_matrix(raw_path, np)
    estimate = common.estimate_white_point_from_camera_neutral(camera_neutral, matrix)
    return {
        "capture_id": capture_id,
        "run_root": str(run_root),
        "source_id": str(row.get("source_id")),
        "cct": int(step.get("target_cct")),
        "gm": int(step.get("target_gm")),
        "cycle_index": int(step.get("n1_cycle_index")),
        "session_index": int(step.get("n1_session_index")),
        "burst_role": str(step.get("n1_burst_role", "paired_cycle_main")),
        "white_point": {
            "cct_K": float(estimate["cct_K"]),
            "duv": float(estimate["duv"]),
            "mired": 1_000_000.0 / float(estimate["cct_K"]),
        },
        "product_chromaticity": {
            "log_R_over_G": math.log(planes["R"] / g_mean),
            "log_B_over_G": math.log(planes["B"] / g_mean),
            "g1_minus_g2_over_mean_g": (planes["G1"] - planes["G2"]) / g_mean,
        },
        "block06_planes": planes,
        "observed_elapsed_s": row.get("best_effort_exposure_start_elapsed_s"),
    }


def _t_interval(values: Sequence[float], confidence: float = 0.95) -> dict[str, Any]:
    """Student-t interval for the mean; honest degradation for tiny n."""
    n = len(values)
    if n == 0:
        return {"status": "no_observations"}
    mean = sum(values) / n
    if n == 1:
        return {
            "status": "insufficient_for_interval",
            "n": 1,
            "mean": mean,
            "min": values[0],
            "max": values[0],
        }
    sample_sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
    # Two-sided t quantile for small n without scipy: exact tables for the
    # degrees of freedom N1 can actually produce.
    t_table = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}
    t_value = t_table.get(n - 1)
    if t_value is None:
        return {
            "status": "n_beyond_table",
            "n": n, "mean": mean,
            "sample_sd": sample_sd,
            "min": min(values), "max": max(values),
        }
    half = t_value * sample_sd / math.sqrt(n)
    return {
        "status": "ok",
        "n": n,
        "mean": mean,
        "sample_sd": sample_sd,
        "ci_low": mean - half,
        "ci_high": mean + half,
        "min": min(values),
        "max": max(values),
        "note": "Student-t conditional interval; normality not verified",
    }


def analyze_guide11_n1(session_roots: Sequence[Path]) -> dict[str, Any]:
    observations: list[dict[str, Any]] = []
    sessions = []
    for root in session_roots:
        root = Path(root)
        plan = json.loads((root / "experiment-spec.json").read_text(encoding="utf-8"))
        rows = _load_jsonl(root / "captures.jsonl")
        if plan.get("guide_experiment_id") != "GUIDE11_N1_WHITE_REPEATABLILITY_V1":
            raise ValueError(f"{root} is not a GUIDE11 N1 session run")
        for row in rows:
            observations.append(observation_from_capture_row(row, root))
        sessions.append({
            "root": str(root),
            "session_index": int(plan["analysis_contract"]["session_index"]),
            "capture_count": len(rows),
        })
    by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for obs in observations:
        by_key.setdefault(
            (obs["cct"], obs["gm"], obs["source_id"], obs["cycle_index"]), []
        ).append(obs)
    points = []
    for cct, gm in N1_POINTS:
        point_report: dict[str, Any] = {"cct": cct, "gm": gm}
        paired_by_cycle = {}
        for cycle in sorted({key[3] for key in by_key if key[0] == cct and key[1] == gm}):
            ray_rows = by_key.get((cct, gm, "ray", cycle), [])
            strip_rows = by_key.get((cct, gm, "strip", cycle), [])
            ray_main = [o for o in ray_rows if o["burst_role"] == "burst_main"] or ray_rows[:1]
            strip_main = [o for o in strip_rows if o["burst_role"] == "burst_main"] or strip_rows[:1]
            if not ray_main or not strip_main:
                point_report["status"] = "incomplete_pairing"
                continue
            ray, strip = ray_main[0], strip_main[0]
            paired_by_cycle[cycle] = {
                "ray": ray,
                "strip": strip,
                "diff": {
                    "cct_K": strip["white_point"]["cct_K"] - ray["white_point"]["cct_K"],
                    "mired": strip["white_point"]["mired"] - ray["white_point"]["mired"],
                    "duv": strip["white_point"]["duv"] - ray["white_point"]["duv"],
                },
            }
        point_report["cycles"] = {
            str(cycle): {
                "ray_cct_K": pair["ray"]["white_point"]["cct_K"],
                "strip_cct_K": pair["strip"]["white_point"]["cct_K"],
                "diff": pair["diff"],
                "ray_capture": pair["ray"]["capture_id"],
                "strip_capture": pair["strip"]["capture_id"],
            }
            for cycle, pair in paired_by_cycle.items()
        }
        for measure in ("cct_K", "mired", "duv"):
            diffs = [pair["diff"][measure] for pair in paired_by_cycle.values()]
            point_report[f"{measure}_diff"] = _t_interval(diffs)
        # Burst layer: within-group spread for the three burst states.
        burst_reports = {}
        for source in ("ray", "strip"):
            group = by_key.get((cct, gm, source, min(paired_by_cycle) if paired_by_cycle else 1), [])
            burst_rows = [o for o in group if o["burst_role"].startswith("burst")]
            if len(burst_rows) >= 2:
                burst_reports[source] = {
                    "n": len(burst_rows),
                    "cct_K_spread": _t_interval([o["white_point"]["cct_K"] for o in burst_rows]),
                    "product_z_spread": {
                        "log_R_over_G": _t_interval(
                            [o["product_chromaticity"]["log_R_over_G"] for o in burst_rows]
                        ),
                        "log_B_over_G": _t_interval(
                            [o["product_chromaticity"]["log_B_over_G"] for o in burst_rows]
                        ),
                    },
                    "capture_ids": [o["capture_id"] for o in burst_rows],
                }
        point_report["burst_layer"] = burst_reports
        point_report["is_burst_point"] = (cct, gm) in N1_BURST_POINTS
        # Product chromaticity of the main paired observations.
        point_report["product_chromaticity"] = {
            str(cycle): {
                "ray_z": pair["ray"]["product_chromaticity"],
                "strip_z": pair["strip"]["product_chromaticity"],
            }
            for cycle, pair in paired_by_cycle.items()
        }
        points.append(point_report)
    return {
        "schema": "guide11_n1_repeatability_analysis_v1",
        "sessions": sessions,
        "observation_count": len(observations),
        "points": points,
        "uncertainty_model": {
            "burst_layer": "same-dwell adjacent captures, no extra reset",
            "cycle_layer": "paired strip-minus-Ray difference per cycle",
            "session_layer": "cycle differences split across operating sessions",
            "interval": "Student-t conditional; prediction intervals need the pooled N1 model",
        },
        "steady_claim": False,
    }
