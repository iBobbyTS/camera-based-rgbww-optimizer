"""GUIDE13 W13-B session-2 combined analysis (offline, frozen).

Merges the three session-2 roots (partial s2 7 frames + s2r-a 2 frames +
s2r-b 46 frames = 55 frames) and evaluates every confirmation pair with the
frozen white-point chain, the cold-family drift gate, and per-node
3-pair confirmation status (ordinal 1 = the W13-A qualifying block).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide12  # noqa: E402
from camera_based_rgbww_optimizer.optimization import (  # noqa: E402
    white_calibration_common as common,
)

ROOTS = [
    Path("D:/rgbww-optimizer/guide13-w13b/formal-w13b-s2"),      # partial 7
    Path("D:/rgbww-optimizer/guide13-w13b/formal-w13b-s2r-a"),   # 2
    Path("D:/rgbww-optimizer/guide13-w13b/formal-w13b-s2r-b"),   # 46
]
OUT = Path("D:/rgbww-optimizer/guide13-w13b/derived/"
           "w13b-s2-combined-confirmation-analysis.json")
TOL = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")
COLD_CCT = 14000
_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]
                     ["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    physical = {
        str(json.loads(line)["capture_id"]): json.loads(line)
        for line in (root / "physical-returns.jsonl")
        .read_text(encoding="utf-8").splitlines() if line.strip()
    }
    raw_path = str(physical[capture_id]["cr3_path"])
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            Path(raw_path), np)
    est = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path])
    return {"cct_K": float(est["cct_K"]), "duv": float(est["duv"]),
            "mired": 1_000_000.0 / float(est["cct_K"])}


def main() -> int:
    by_pair: dict[tuple[str, int], dict[str, list]] = {}
    total = 0
    for root in ROOTS:
        rows = [
            json.loads(line)
            for line in (root / "captures.jsonl").read_text(encoding="utf-8")
            .splitlines() if line.strip()
        ]
        total += len(rows)
        for row in rows:
            step = row["plan_step"]
            key = (step["w13b_node"], int(step["w13b_pair_ordinal"]))
            slot = "ref" if step["w13b_step"] in ("ray", "raybefore", "rayafter") \
                else "strip"
            by_pair.setdefault(key, {}).setdefault(slot, []).append({
                "capture_id": str(row["capture_id"]),
                "step": step["w13b_step"],
                "run": root.name,
                "white_point": white_point_of(root, str(row["capture_id"])),
            })
    results = []
    for (node, ordinal), slots in sorted(by_pair.items()):
        strip = slots["strip"][0]
        refs = slots.get("ref", [])
        cold = int(node.split("/")[0]) >= COLD_CCT
        if cold and len(refs) == 2:
            reference = {
                c: float(np.mean([r["white_point"][c] for r in refs]))
                for c in COMPONENTS}
            drift = {c: refs[1]["white_point"][c] - refs[0]["white_point"][c]
                     for c in COMPONENTS}
            drift_ok = all(abs(drift[c]) <= TOL[c] for c in COMPONENTS)
        elif refs:
            reference = refs[0]["white_point"]
            drift = drift_ok = None
        else:
            continue
        signed = {c: strip["white_point"][c] - reference[c] for c in COMPONENTS}
        e = max(abs(signed["cct_K"]) / TOL["cct_K"],
                abs(signed["mired"]) / TOL["mired"],
                abs(signed["duv"]) / TOL["duv"])
        results.append({
            "node": node, "pair_ordinal": ordinal,
            "strip_capture_id": strip["capture_id"],
            "reference_capture_ids": [r["capture_id"] for r in refs],
            "signed_errors": signed,
            "E_normalized": e,
            "E_within_gate": e <= 1.0,
            "ray_drift": drift,
            "ray_drift_within_gate": drift_ok,
        })
    by_node: dict[str, list[dict]] = {}
    for r in results:
        by_node.setdefault(r["node"], []).append(r)
    node_summary = []
    for node, pairs in sorted(by_node.items(),
                              key=lambda kv: tuple(int(x) for x in kv[0].split("/"))):
        valid = [p for p in pairs if p["ray_drift_within_gate"] is not False]
        es = [p["E_normalized"] for p in valid]
        node_summary.append({
            "node": node,
            "session_pairs": len(pairs),
            "valid_pairs": len(valid),
            "E_values": [round(x, 4) for x in es],
            "E_max": round(max(es), 4) if es else None,
            "all_within_gate": all(x <= 1.0 for x in es) if es else None,
            "confirmed_3_pairs": bool(
                valid and all(x <= 1.0 for x in es)),
        })
    artifact = {
        "schema": "guide13_w13b_s2_combined_analysis_v1",
        "tolerances": TOL,
        "roots": [str(r) for r in ROOTS],
        "frames_total": total,
        "pairs": results,
        "node_summary": node_summary,
        "summary": {
            "pairs": len(results),
            "pairs_within_gate": sum(1 for r in results if r["E_within_gate"]),
            "drift_gate_trips": sum(
                1 for r in results if r["ray_drift_within_gate"] is False),
            "nodes": len(by_node),
            "nodes_confirmed_3_pairs": sum(
                1 for n in node_summary if n["confirmed_3_pairs"]),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"{'node':>9s} {'ord':>3s} {'E':>7s} gate  {'eK':>9s} {'emir':>8s} {'eduv':>10s}")
    for r in results:
        s = r["signed_errors"]
        print(f"{r['node']:>9s} {r['pair_ordinal']:>3d} {r['E_normalized']:7.3f} "
              f"{'PASS' if r['E_within_gate'] else 'FAIL':>4s} "
              f"{s['cct_K']:9.2f} {s['mired']:8.4f} {s['duv']:10.3e}"
              + ("  DRIFT!" if r["ray_drift_within_gate"] is False else ""))
    print("pairs in gate:", artifact["summary"]["pairs_within_gate"], "/",
          len(results), "| drift trips:", artifact["summary"]["drift_gate_trips"],
          "| nodes confirmed:", artifact["summary"]["nodes_confirmed_3_pairs"],
          "/", len(by_node))
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
