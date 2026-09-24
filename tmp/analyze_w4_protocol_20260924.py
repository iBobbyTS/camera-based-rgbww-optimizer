"""One-shot GUIDE11 W4 protocol difference-in-differences analysis."""
from __future__ import annotations

import json
from pathlib import Path

FAST = Path("D:/rgbww-optimizer/guide11-w4/formal-w4-fast-20260924-r2")
LONG = Path("D:/rgbww-optimizer/guide11-w4/formal-w4-long-20260924")
OUT = Path("D:/rgbww-optimizer/guide11-w4/derived/w4-protocol-analysis-20260924.json")


def white_point_of(root: Path, row: dict, cache: dict, common, np) -> dict:
    capture_id = str(row["capture_id"])
    stats = json.loads((root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw = str((row.get("capture") or {}).get("saved_file", ""))
    if raw not in cache:
        cache[raw] = common._load_rawpy_rgb_xyz_matrix(Path(raw), np)
    est = common.estimate_white_point_from_camera_neutral(neutral, cache[raw])
    return {
        "cct_K": float(est["cct_K"]),
        "duv": float(est["duv"]),
        "mired": 1_000_000.0 / float(est["cct_K"]),
    }


def collect(root: Path, cache, common, np) -> dict:
    pair_by_point: dict[tuple[int, int], dict[str, dict]] = {}
    for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        step = row.get("plan_step", {})
        key = (int(step["target_cct"]), int(step["target_gm"]))
        pair_by_point.setdefault(key, {})[str(row["source_id"])] = white_point_of(root, row, cache, common, np)
    return pair_by_point


def main() -> None:
    import numpy as np

    from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

    cache: dict = {}
    fast = collect(FAST, cache, common, np)
    long = collect(LONG, cache, common, np)
    results = []
    for key in sorted(fast):
        f, l = fast[key], long[key]
        def diff(a, b, axis):
            return {axis: a[axis] - b[axis] for axis in ("cct_K", "mired", "duv")}
        fast_pair = {axis: f["strip"][axis] - f["ray"][axis] for axis in ("cct_K", "mired", "duv")}
        long_pair = {axis: l["strip"][axis] - l["ray"][axis] for axis in ("cct_K", "mired", "duv")}
        results.append({
            "cct": key[0], "gm": key[1],
            "fast_white_points": f,
            "long_white_points": l,
            "fast_strip_minus_ray": fast_pair,
            "long_strip_minus_ray": long_pair,
            "delta_protocol": {axis: long_pair[axis] - fast_pair[axis] for axis in fast_pair},
            "ray_long_minus_fast": {axis: l["ray"][axis] - f["ray"][axis] for axis in fast_pair},
            "strip_long_minus_fast": {axis: l["strip"][axis] - f["strip"][axis] for axis in fast_pair},
        })
    artifact = {
        "schema": "guide11_w4_protocol_analysis_v1",
        "runs": {"fast": str(FAST), "long": str(LONG)},
        "protocol_evidence": {
            "fast": "reset600/D120 label guide11_w4fast_reset600_D120",
            "long": "reset1800/D600 label guide11_w4long_reset1800_D600; observed exposure-start elapsed 604.6-605.9 s",
        },
        "points": results,
        "interpretation_limits": [
            "single pair per point: conditional values only, no causal temperature claim",
            "FAST run preceded LONG run; reversed-order append (<=2 points, <=8 frames) only if adoption conclusions would change",
        ],
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'point':>12} {'dCCT':>8} {'dmired':>8} {'dDuv':>9} | {'ray dCCT':>9} {'strip dCCT':>10}")
    for r in results:
        d = r["delta_protocol"]
        print(f"{r['cct']:>6}/{r['gm']:<4} {d['cct_K']:>8.1f} {d['mired']:>8.2f} {d['duv']:>9.4f} | {r['ray_long_minus_fast']['cct_K']:>9.1f} {r['strip_long_minus_fast']['cct_K']:>10.1f}")
    print("->", OUT)


if __name__ == "__main__":
    main()
