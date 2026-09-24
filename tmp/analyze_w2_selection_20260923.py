"""One-shot GUIDE11 W2 selection analysis over the merged 98 observations."""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.optimization.analyze_guide11_n1 import (
    observation_from_capture_row,
)

PARENT = Path("D:/rgbww-optimizer/guide11-w2/formal-w2-20260922")
SUFFIX = Path("D:/rgbww-optimizer/guide11-w2/formal-w2-20260923-suffix")
TARGETS = Path("D:/rgbww-optimizer/guide11-n1/derived/w1-frozen-targets-20260922.json")
OUT = Path("D:/rgbww-optimizer/guide11-w2/derived/w2-selection-20260923.json")


def load_rows(root: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    import numpy as np

    from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

    targets = json.loads(TARGETS.read_text(encoding="utf-8"))
    target_by_key = {(n["cct"], n["gm"]): n for n in targets["nodes"]}

    observations = []
    matrix_cache: dict[str, object] = {}
    for root in (PARENT, SUFFIX):
        for row in load_rows(root):
            if row.get("source_id") != "strip":
                continue
            capture_id = str(row["capture_id"])
            measurement_path = root / "measurements" / f"{capture_id}.patch-statistics.json"
            stats = json.loads(measurement_path.read_text(encoding="utf-8"))
            patches = stats["patches"]
            block = next(p for p in patches if p.get("index") == 6)
            planes = {
                plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
                for plane in ("R", "G1", "G2", "B")
            }
            g_mean = 0.5 * (planes["G1"] + planes["G2"])
            camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
            raw_path = str((row.get("capture") or {}).get("saved_file", ""))
            if raw_path not in matrix_cache:
                matrix_cache[raw_path] = common._load_rawpy_rgb_xyz_matrix(Path(raw_path), np)
            estimate = common.estimate_white_point_from_camera_neutral(
                camera_neutral, matrix_cache[raw_path]
            )
            step = row.get("plan_step", {})
            key = (int(step["target_cct"]), int(step["target_gm"]))
            command = {k: int(v) for k, v in (step.get("command") or {}).items()}
            if not command:
                raise ValueError(f"W2 strip observation lacks its command: {capture_id}")
            observations.append({
                "capture_id": capture_id,
                "run_root": str(root),
                "key": key,
                "candidate_index": int(step.get("capture_id", "c0").split("candidate")[-1]),
                "command": command,
                "white_point": {
                    "cct_K": float(estimate["cct_K"]),
                    "duv": float(estimate["duv"]),
                    "mired": 1_000_000.0 / float(estimate["cct_K"]),
                },
            })

    by_node: dict[tuple[int, int], list[dict]] = {}
    for obs in observations:
        by_node.setdefault(obs["key"], []).append(obs)

    # W6-era status for the fallback comparison.
    w8 = json.loads(
        Path("D:/rgbww-optimizer/guide10-white70-w8-final/guide10-white70-final-artifact.json")
        .read_text(encoding="utf-8")
    )
    w6_by_key = {(int(r["cct"]), int(r["gm"])): r for r in w8["canonical_lut"]}

    rows = []
    improved = 0
    within = 0
    for key in sorted(by_node):
        node = target_by_key[key]
        target = node["ray_target"]
        tol = node["tolerances"]
        candidates = []
        for obs in by_node[key]:
            wp = obs["white_point"]
            gates = {
                "cct_K": abs(wp["cct_K"] - target["cct_K"]) / tol["cct_K"],
                "mired": abs(wp["mired"] - target["mired"]) / tol["mired"],
                "duv": abs(wp["duv"] - target["duv"]) / tol["duv"],
            }
            candidates.append({
                "capture_id": obs["capture_id"],
                "candidate_index": obs["candidate_index"],
                "command": obs["command"],
                "white_point": wp,
                "e_gates": gates,
                "E": max(gates.values()),
            })
        candidates.sort(key=lambda c: c["E"])
        best = candidates[0]
        w6 = w6_by_key[key]
        w6_status = w6.get("status")
        rows.append({
            "cct": key[0], "gm": key[1],
            "w6_status": w6_status,
            "selected": best,
            "all_candidates": candidates,
            "candidate_count": len(candidates),
            "selected_within_tolerance": best["E"] < 1.0,
            "certification": "selection_frame_only_independent_FAST_confirmation_required",
        })
        if best["E"] < 1.0:
            within += 1
        if w6_status != "pass" and best["E"] < 1.0:
            improved += 1

    artifact = {
        "schema": "guide11_w2_selection_v1",
        "observation_count": len(observations),
        "node_count": len(rows),
        "nodes_within_tolerance": within,
        "nodes_improved_from_w6_fail": improved,
        "objective": "E(u)=max(|e_K|/tau_K, |e_mired|/tau_mired, |e_Duv|/tau_Duv) vs W1 frozen targets",
        "sources": {
            "parent_prefix": str(PARENT),
            "suffix": str(SUFFIX),
            "frozen_targets": str(TARGETS),
        },
        "note": "Selection frames cannot certify; selected commands require independent FAST confirmation before adoption.",
        "nodes": rows,
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("observations:", len(observations), "| nodes:", len(rows))
    print("within tolerance (selection frame):", within, "/", len(rows))
    print("improved from W6-fail:", improved)
    print("->", OUT)


if __name__ == "__main__":
    main()
