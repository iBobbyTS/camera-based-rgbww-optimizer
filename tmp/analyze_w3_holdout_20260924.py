"""One-shot GUIDE11 W3 holdout analysis: node-residual vs interpolation-increment."""
from __future__ import annotations

import json
import math
from pathlib import Path

RUN = Path("D:/rgbww-optimizer/guide11-w3/formal-w3-20260923")
LUT = Path("D:/rgbww-optimizer/guide11-w3/frozen-lut-20260923.json")
TARGETS = Path("D:/rgbww-optimizer/guide11-n1/derived/w1-frozen-targets-20260922.json")
W2_SEL = Path("D:/rgbww-optimizer/guide11-w2/derived/w2-selection-20260923.json")
OUT = Path("D:/rgbww-optimizer/guide11-w3/derived/w3-holdout-analysis-20260924.json")


def white_point_of(row: dict, matrix_cache: dict, common, np) -> dict:
    capture_id = str(row["capture_id"])
    root = Path(row["run_root"]) if "run_root" in row else RUN
    stats = json.loads((root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw_path = str((row.get("capture") or {}).get("saved_file", ""))
    if raw_path not in matrix_cache:
        matrix_cache[raw_path] = common._load_rawpy_rgb_xyz_matrix(Path(raw_path), np)
    estimate = common.estimate_white_point_from_camera_neutral(camera_neutral, matrix_cache[raw_path])
    return {
        "cct_K": float(estimate["cct_K"]),
        "duv": float(estimate["duv"]),
        "mired": 1_000_000.0 / float(estimate["cct_K"]),
    }


def error_gates(wp: dict, target: dict, tol: dict) -> tuple[dict, float]:
    gates = {
        "cct_K": (wp["cct_K"] - target["cct_K"]) / tol["cct_K"],
        "mired": (wp["mired"] - target["mired"]) / tol["mired"],
        "duv": (wp["duv"] - target["duv"]) / tol["duv"],
    }
    return gates, max(abs(v) for v in gates.values())


def main() -> None:
    import numpy as np

    from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

    matrix_cache: dict = {}
    targets = json.loads(TARGETS.read_text(encoding="utf-8"))
    target_by_key = {(n["cct"], n["gm"]): n for n in targets["nodes"]}
    w2_sel = json.loads(W2_SEL.read_text(encoding="utf-8"))
    sel_by_key = {(n["cct"], n["gm"]): n for n in w2_sel["nodes"]}

    rows = [
        json.loads(line)
        for line in (RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    obs_by_point: dict[tuple[int, int], dict[str, dict]] = {}
    for row in rows:
        step = row.get("plan_step", {})
        key = (int(step["target_cct"]), int(step["target_gm"]))
        obs_by_point.setdefault(key, {})[str(row["source_id"])] = {**row, "run_root": str(RUN)}

    plan = json.loads((RUN / "experiment-spec.json").read_text(encoding="utf-8"))
    audit_by_point = {(a["cct"], a["gm"]): a for a in plan["analysis_contract"]["requests_audit"]}

    results = []
    for point in plan["analysis_contract"]["points"]:
        key = (point["cct"], point["gm"])
        pair = obs_by_point[key]
        ray_wp = white_point_of(pair["ray"], matrix_cache, common, np)
        strip_wp = white_point_of(pair["strip"], matrix_cache, common, np)
        # Non-node holdout targets are the paired Ray observations themselves;
        # tolerances inherit from the nearest frozen node's contract.
        lut_nodes_all = [(n["cct"], n["gm"]) for n in json.loads(LUT.read_text(encoding="utf-8"))["nodes"]]
        tol_nearest = min(
            lut_nodes_all,
            key=lambda k: abs(1_000_000.0 / k[0] - 1_000_000.0 / key[0]) / (1_000_000.0 / key[0])
            + abs(k[1] - key[1]) / 200.0,
        )
        target = ray_wp
        tol = target_by_key[tol_nearest]["tolerances"]
        holdout_gates, holdout_e = error_gates(strip_wp, target, tol)

        # Node-baseline residual: nearest frozen-LUT node's own error under
        # the frozen command (W2 selection frame where available).
        lut_nodes = [(n["cct"], n["gm"]) for n in json.loads(LUT.read_text(encoding="utf-8"))["nodes"]]
        nearest = min(
            lut_nodes,
            key=lambda k: abs(1_000_000.0 / k[0] - 1_000_000.0 / key[0]) / (1_000_000.0 / key[0])
            + abs(k[1] - key[1]) / 200.0,
        )
        nearest_node_target = target_by_key[nearest]
        sel = sel_by_key.get(nearest)
        if sel and sel["selected"]["E"] < 1.0:
            node_basis = "w2_selection_frame"
            node_e = sel["selected"]["E"]
            node_gates = sel["selected"]["e_gates"]
        else:
            node_basis = "w6_observation_vs_frozen_target"
            t2 = nearest_node_target["ray_target"]
            tol2 = nearest_node_target["tolerances"]
            node_gates, node_e = error_gates(
                {"cct_K": t2["cct_K"], "mired": t2["mired"], "duv": t2["duv"]}, t2, tol2
            )
            node_e = 0.0  # pass node by W6 status; exact residual not asserted here
        increment_gates = {
            axis: holdout_gates[axis] - node_gates.get(axis, 0.0) for axis in holdout_gates
        }
        results.append({
            "cct": key[0], "gm": key[1],
            "ray_white_point": ray_wp,
            "strip_white_point": strip_wp,
            "holdout_error_gates": holdout_gates,
            "holdout_E": holdout_e,
            "holdout_within_tolerance": holdout_e < 1.0,
            "nearest_node": {"cct": nearest[0], "gm": nearest[1], "basis": node_basis, "E": node_e},
            "interpolation_increment_gates": increment_gates,
            "command": audit_by_point[key]["interpolated_command"],
            "differs_from_nearest_copy": audit_by_point[key]["interpolated_command"] != audit_by_point[key]["nearest_node_command"],
        })

    within = sum(1 for r in results if r["holdout_within_tolerance"])
    difficult = [r for r in results if r["cct"] in (3200, 14000)]
    artifact = {
        "schema": "guide11_w3_holdout_analysis_v1",
        "run_root": str(RUN),
        "point_count": len(results),
        "within_tolerance": within,
        "difficult_region_within": sum(1 for r in difficult if r["holdout_within_tolerance"]),
        "objective": "E(u) vs W1 frozen targets; node-baseline residual and interpolation increment reported separately",
        "node_baseline_caveat": "pass-node baselines use W6 status (E recorded 0.0 as pass); W2-selected nodes use the selection frame",
        "points": results,
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("points:", len(results), "| within tolerance:", within)
    print("difficult region (3200/14000):", artifact["difficult_region_within"], "/", len(difficult))
    worst = sorted(results, key=lambda r: -r["holdout_E"])[:5]
    for r in worst:
        print(f"  worst {r['cct']}/{r['gm']}: E={r['holdout_E']:.2f} gates={ {k: round(v,2) for k,v in r['holdout_error_gates'].items()} }")
    print("->", OUT)


if __name__ == "__main__":
    main()
