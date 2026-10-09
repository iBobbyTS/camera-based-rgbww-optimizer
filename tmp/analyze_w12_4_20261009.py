"""GUIDE12 W12-4 LONG order re-verification analysis (offline, frozen).

Reads the eight W12-4 point/protocol run roots, recomputes white points
with the shared W12 estimator chain (block_06 four-plane normalized-per-
second trimmed means -> camera neutral -> white point), and produces per
point:

- (strip - Ray) under LONG and under FAST (same frozen LUT command in
  both protocols);
- the primary quantity Delta_protocol = (strip-Ray)_LONG - (strip-Ray)_FAST
  per component against the W12 tolerances;
- per-source LONG-FAST differences (Ray and strip separately), which the
  GUIDE requires reported alongside the difference-in-differences;
- execution-position context so protocol-vs-period aliasing is visible:
  LONG occupied positions 1,3,6,8 and FAST 2,4,5,7 across the night.

Single DiD per point is one observation, not a repeated-interval estimate;
order effects are not separated from protocol effects by design here, and
LONG is never claimed as steady state.

Output: D:/rgbww-optimizer/guide12-w124/derived/w12-4-order-reverification-analysis-20261009.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

ROOT = Path("D:/rgbww-optimizer/guide12-w124")
RUNS = [
    ("3200/100", "long", "formal-w124-01-p3200100-long", 1),
    ("1800/100", "fast", "formal-w124-02-p1800100-fast", 2),
    ("20000/100", "long", "formal-w124-03-p20000100-long", 3),
    ("5600/100", "fast", "formal-w124-04-p5600100-fast", 4),
    ("3200/100", "fast", "formal-w124-05-p3200100-fast", 5),
    ("1800/100", "long", "formal-w124-06-p1800100-long", 6),
    ("20000/100", "fast", "formal-w124-07-p20000100-fast", 7),
    ("5600/100", "long", "formal-w124-08-p5600100-long", 8),
]
OUT = ROOT / "derived/w12-4-order-reverification-analysis-20261009.json"
TOL = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")

_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(run_root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (run_root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(
            block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"]
        )
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    rows = [
        json.loads(line)
        for line in (run_root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
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
    obs: dict[tuple[str, str], dict] = {}
    for point, protocol, run_name, position in RUNS:
        run_root = ROOT / run_name
        rows = [
            json.loads(line)
            for line in (run_root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in rows:
            step = row["plan_step"]
            quality = (row.get("capture", {}).get("direct_quality") or {}).get("status")
            entry = obs.setdefault((point, protocol), {
                "point": point, "protocol": protocol,
                "execution_position": position, "run": run_name,
                "source_order": [], "white_points": {},
            })
            source = str(step["source_id"])
            entry["source_order"].append(source)
            entry["white_points"][source] = {
                "capture_id": str(row["capture_id"]),
                "quality": quality,
                "value": white_point_of(run_root, str(row["capture_id"])),
            }
    results = []
    for point in ("1800/100", "3200/100", "5600/100", "20000/100"):
        fast = obs[(point, "fast")]
        long_ = obs[(point, "long")]
        sr = {}
        for tag, e in (("FAST", fast), ("LONG", long_)):
            s = e["white_points"]["strip"]["value"]
            r = e["white_points"]["ray"]["value"]
            sr[tag] = {c: s[c] - r[c] for c in COMPONENTS}
        did = {c: sr["LONG"][c] - sr["FAST"][c] for c in COMPONENTS}
        src_diff = {
            "ray_LONG_minus_FAST": {
                c: long_["white_points"]["ray"]["value"][c]
                - fast["white_points"]["ray"]["value"][c] for c in COMPONENTS},
            "strip_LONG_minus_FAST": {
                c: long_["white_points"]["strip"]["value"][c]
                - fast["white_points"]["strip"]["value"][c] for c in COMPONENTS},
        }
        results.append({
            "point": point,
            "white_points": {
                tag: {src: e["white_points"][src]["value"]
                      for src in ("ray", "strip")}
                for tag, e in (("FAST", fast), ("LONG", long_))
            },
            "source_orders": {"FAST": fast["source_order"], "LONG": long_["source_order"]},
            "execution_positions": {"LONG": long_["execution_position"],
                                    "FAST": fast["execution_position"]},
            "signed_errors": sr,
            "Delta_protocol": did,
            "Delta_normalized": {
                c: round(abs(did[c]) / TOL[c], 4) for c in COMPONENTS},
            "per_source": src_diff,
        })
        print(f"{point:10s} DiD: dK={did['cct_K']:+8.1f}  dmired={did['mired']:+6.2f}  "
              f"dduv={did['duv']:+.5f}  | Ray(L-F): {src_diff['ray_LONG_minus_FAST']['cct_K']:+8.1f}K  "
              f"| strip(L-F): {src_diff['strip_LONG_minus_FAST']['cct_K']:+8.1f}K")
    norm_max = {
        c: max(abs(r["Delta_protocol"][c]) / TOL[c] for r in results)
        for c in COMPONENTS}
    print("per-component max |DiD|/tol:", {k: round(v, 3) for k, v in norm_max.items()})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema": "guide12_w12_4_order_reverification_analysis_v1",
        "tolerances": TOL,
        "runs": [r[2] for r in RUNS],
        "execution_order": [
            {"position": pos, "point": p, "protocol": q, "run": run}
            for p, q, run, pos in RUNS],
        "points": results,
        "interpretation_caveats": [
            "single DiD per point is one observation, not a repeated interval",
            "order and period effects are not separated by this design; "
            "LONG occupied positions 1,3,6,8 and FAST 2,4,5,7",
            "LONG is not claimed as steady state; no FAST fit feedback",
            "20000/100 carries the documented Ray drift characteristic; "
            "its Ray LONG-FAST difference includes that device behavior",
        ],
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
