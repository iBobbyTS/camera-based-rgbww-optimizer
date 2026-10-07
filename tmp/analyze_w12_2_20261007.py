"""GUIDE12 W12-2 frozen-LUT verification analysis (offline, frozen).

Reads every W12-2 verification run root (six batches plus the evidence-
backed retry runs), recomputes white points with the W12 estimator chain
(block_06 four-plane normalized-per-second trimmed means -> camera neutral
-> white point), and produces per-node verification:

- per repeat: strip minus reference signed errors and the full-tolerance E
  (reference = paired Ray frame; cold nodes use the mean of their Ray
  before/after sandwich);
- cold drift gate: |ray_after - ray_before| per component vs the W12
  tolerances (the W12 reference-compatibility rule; a tripped gate
  classifies the node reference_limited, never silently passes);
- per-node verdict against the W12-2 confirmation rules (changed nodes
  carry two independent pairs, unchanged one);
- retry precedence: a later retry pair supersedes the failed original for
  the same node/repeat (both stay in the record);
- S0 session table (A: C12-1 run, B: warm batch, C: pending W12-3).

Output: D:/rgbww-optimizer/guide12-w122/derived/w12-2-verification-analysis.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

ROOT = Path("D:/rgbww-optimizer/guide12-w122")
RUNS = [
    "formal-w122-warm",
    "formal-w122-warm-1800g0-retry2",
    "formal-w122-mid",
    "formal-w122-high",
    "formal-w122-high-5000g200-retry",
    "formal-w122-veryhigh",
    "formal-w122-veryhigh-rail-retry",
    "formal-w122-cold14k",
    "formal-w122-cold14k-rail-retry",
    "formal-w122-cold20k",
    "formal-w122-cold20k-rail-retry",
]
LUT = ROOT / "derived/w12-2-frozen-lut-20261005.json"
OUT = ROOT / "derived/w12-2-verification-analysis.json"
TOL = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")

_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    rows = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    raw_path = str(next(
        r for r in rows if str(r.get("capture_id")) == capture_id
    )["capture"]["saved_file"])
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(Path(raw_path), np)
    est = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path]
    )
    return {"cct_K": float(est["cct_K"]), "duv": float(est["duv"]),
            "mired": 1_000_000.0 / float(est["cct_K"])}


def main() -> int:
    lut = json.loads(LUT.read_text(encoding="utf-8"))
    changed = {
        f"{n['cct']}/{n['gm']}"
        for n in lut["nodes"] if n["verification_class"] == "needs_two_pairs"
    }
    pairs: dict[tuple[str, int], dict] = {}
    order: list[tuple[str, int]] = []
    s0_frames = []
    for run in RUNS:
        root = ROOT / run
        if not (root / "captures.jsonl").exists():
            print(f"跳过（无 captures）: {run}")
            continue
        rows = [
            json.loads(line)
            for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in rows:
            step = row["plan_step"]
            quality = (row.get("capture", {}).get("direct_quality") or {}).get("status")
            if step.get("role") == "s0_reference" and quality == "pass":
                s0_frames.append({
                    "run": run, "capture_id": str(row["capture_id"]),
                    "white_point": white_point_of(root, str(row["capture_id"])),
                })
                continue
            if "w122_node" not in step:
                continue
            key = (str(step["w122_node"]), int(step["w122_repeat"]))
            entry = pairs.setdefault(key, {"node": key[0], "repeat": key[1]})
            slot = str(step["w122_step"])
            entry[slot] = {
                "run": run,
                "capture_id": str(row["capture_id"]),
                "quality": quality,
                "white_point": (
                    white_point_of(root, str(row["capture_id"]))
                    if quality in ("pass", "near_noise_only") else None
                ),
            }
            if key not in order:
                order.append(key)

    node_results = []
    for key in order:
        entry = pairs[key]
        node, repeat = key
        steps = {k: v for k, v in entry.items() if k not in ("node", "repeat")}
        ray_keys = [k for k in steps if k in ("ray", "raybefore", "rayafter")]
        ray_refs = [
            steps[k] for k in ray_keys
            if steps[k]["quality"] == "pass" and steps[k]["white_point"]
        ]
        strip = steps.get("strip")
        drift = None
        if "raybefore" in steps and "rayafter" in steps:
            b, a = steps["raybefore"], steps["rayafter"]
            if b["white_point"] and a["white_point"]:
                drift = {
                    c: a["white_point"][c] - b["white_point"][c]
                    for c in COMPONENTS
                }
        drift_within = (
            all(abs(drift[c]) <= TOL[c] for c in COMPONENTS)
            if drift else None
        )
        result = {
            "node": node, "repeat": repeat,
            "verification_class": (
                "needs_two_pairs" if node in changed else "one_pair_plus_history"),
            "steps": steps,
            "cold_drift": drift,
            "cold_drift_within_tolerances": drift_within,
        }
        if strip and strip["white_point"] and ray_refs:
            reference = {
                c: float(np.mean([r["white_point"][c] for r in ray_refs]))
                for c in COMPONENTS
            }
            signed = {
                c: strip["white_point"][c] - reference[c] for c in COMPONENTS
            }
            e = max(abs(signed["cct_K"]) / TOL["cct_K"],
                    abs(signed["mired"]) / TOL["mired"],
                    abs(signed["duv"]) / TOL["duv"])
            result.update({
                "reference_white_point": reference,
                "signed_errors": signed,
                "E_normalized": e,
                "E_within_gate": e <= 1.0,
                "pair_valid": bool(drift_within is not False),
            })
        else:
            result.update({"pair_valid": False, "reason": "missing valid ray/strip"})
        node_results.append(result)

    by_node: dict[str, list[dict]] = {}
    for r in node_results:
        by_node.setdefault(r["node"], []).append(r)
    summary_rows = []
    for node in sorted(by_node, key=lambda k: tuple(int(x) for x in k.split("/"))):
        reps = by_node[node]
        valid_es = [r["E_normalized"] for r in reps if r.get("pair_valid")]
        need = 2 if node in changed else 1
        confirmed = len(valid_es) >= need
        if not valid_es:
            verdict = "unverified"
        elif max(valid_es) <= 1.0 and confirmed:
            verdict = "verified_qualified"
        elif max(valid_es) <= 1.0:
            verdict = "measured_ok_confirmation_short"
        else:
            verdict = "exceeds_tolerance"
        drift_trips = [
            r for r in reps if r.get("cold_drift_within_tolerances") is False
        ]
        if drift_trips:
            verdict = "reference_limited(drift_gate)"
        summary_rows.append({
            "node": node,
            "repeats": len(reps),
            "valid_pairs": len(valid_es),
            "E_values": [round(e, 4) for e in valid_es],
            "E_max": round(max(valid_es), 4) if valid_es else None,
            "verdict": verdict,
        })
    qualified = sum(1 for r in summary_rows if r["verdict"] == "verified_qualified")
    print(f"节点判定: verified_qualified {qualified}/70")
    for r in summary_rows:
        flag = "" if r["verdict"] == "verified_qualified" else "  <-- " + r["verdict"]
        print(f"  {r['node']:11s} E={r['E_values']} valid={r['valid_pairs']}{flag}")
    s0_summary = {
        "frames": s0_frames,
        "note": "session C rides the W12-3 campaign",
    }
    result = {
        "schema": "guide12_w12_2_verification_analysis_v1",
        "tolerances": TOL,
        "lut": str(LUT),
        "runs": RUNS,
        "node_pairs": node_results,
        "node_summary": summary_rows,
        "summary": {
            "verified_qualified": qualified,
            "total_nodes": len(summary_rows),
            "verdict_counts": {
                v: sum(1 for r in summary_rows if r["verdict"] == v)
                for v in {r["verdict"] for r in summary_rows}
            },
        },
        "s0_sessions": s0_summary,
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
