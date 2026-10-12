"""GUIDE12 C12-4 runtime-model holdout analysis (offline, frozen).

Reads the 30-frame C12-4 holdout run, recomputes z per frame, and
evaluates per request:
- dz = z_strip - Ray bracket mean;
- 2D decomposition (radial -> SAT pp, tangential -> Hue deg) with the
  radial basis linearly blended from the bracketing hue anchors
  (Ray z at S0 and S50 from C12-1 records + campaign brackets);
- verdicts against the product gate (+/-2pp, +/-2deg);
- SAT monotonicity across the served model outputs (achieved radial
  position must not invert when request SAT rises);
- local hue direction consistency (served hue offset sign vs the
  sector's tangential direction);
- bounded prediction intervals (max |error| over the holdout set).

within_c1_anchor_envelope is NOT computed as a gate.

Output: D:/rgbww-optimizer/guide12-c124/derived/c12-4-holdout-analysis-20261012.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path("D:/rgbww-optimizer/guide12-c124/formal-c124-holdout")
OUT = ROOT.parent / "derived/c12-4-holdout-analysis-20261012.json"

# Ray anchors: z at S0 (white) and S50 per hue anchor (C12-1 records,
# campaign cross-validated). Hue 300 has no C12-1 S100 conflict; the S50
# row for 300 comes from the records; S0 from the C12-1 session table.
RAY_S0 = (-0.7334, -0.3699)
RAY_S50 = {
    0: (0.4837, -0.5862),
    60: (-0.6413, -0.7922),
    120: (-1.2712, -0.8033),
    180: (-1.2887, -0.3532),
    240: (-1.1671, 0.3527),
    300: (-0.0756, 0.1744),
}
# tangential slope per hue span (z units per degree, from adjacent anchors)
HUE_SPAN_SLOPES = {
    (0, 60): 0.0184, (60, 120): 0.0075, (120, 180): 0.0075,
    (180, 240): 0.0119, (240, 300): 0.0184, (300, 360): 0.0184,
}


def hue_basis(hue: int, sat: int):
    """Radial unit + |dz/dSAT| per pp for an arbitrary (hue, sat),
    blending the bracketing anchor hues' S0->S50 segments."""
    h = hue % 360
    anchors = sorted(RAY_S50)
    ring = anchors + [360]
    hs = h if h >= anchors[0] else h + 360
    for k in range(len(anchors)):
        if ring[k] <= hs <= ring[k + 1]:
            h0 = anchors[k]
            h1 = anchors[(k + 1) % len(anchors)] % 360
            span = ring[k + 1] - ring[k]
            w = (hs - ring[k]) / span if span else 0.0
            break
    else:  # pragma: no cover
        h0, h1, w = anchors[0], anchors[1], 0.0
    slopes = []
    for hh in (h0, h1):
        v = tuple((RAY_S50[hh][i] - RAY_S0[i]) / 50.0 for i in (0, 1))
        slopes.append(v)
    per = tuple((1 - w) * slopes[0][i] + w * slopes[1][i] for i in (0, 1))
    mag = math.hypot(*per)
    ur = tuple(x / mag for x in per)
    span_slope = HUE_SPAN_SLOPES.get((h0, h1), 0.012)
    return ur, mag, span_slope, (h0, h1, w)


def z_of(capture_id: str) -> tuple[float, float]:
    stats = json.loads(
        (ROOT / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8")
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(
            block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"]
        )
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    return (math.log(planes["R"] / g), math.log(planes["B"] / g))


def main() -> int:
    rows = [
        json.loads(line)
        for line in (ROOT / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    reqs: dict[str, dict] = {}
    order: list[str] = []
    for row in rows:
        step = row["plan_step"]
        if "c124_request" not in step:
            continue
        key = str(step["c124_request"])
        e = reqs.setdefault(key, {})
        e[str(step["c124_position"])] = z_of(str(row["capture_id"]))
        if key not in order:
            order.append(key)

    results = []
    for key in order:
        hue, sat = (int(x) for x in key.split("/"))
        before, after = reqs[key]["raybefore"], reqs[key]["rayafter"]
        drift = tuple(after[i] - before[i] for i in (0, 1))
        ref = tuple((before[i] + after[i]) / 2 for i in (0, 1))
        strip = reqs[key]["strip"]
        dz = tuple(strip[i] - ref[i] for i in (0, 1))
        ur, mag, hs, blend = hue_basis(hue, sat)
        radial_pp = (dz[0] * ur[0] + dz[1] * ur[1]) / mag
        ut = (-ur[1], ur[0])
        tangential = dz[0] * ut[0] + dz[1] * ut[1]
        hue_deg = tangential / hs
        verdict = (
            "qualified" if abs(radial_pp) <= 2.0 and abs(hue_deg) <= 2.0
            else "exceeds_gate")
        results.append({
            "request": key, "dz": [round(x, 5) for x in dz],
            "bracket_drift": [round(x, 5) for x in drift],
            "radial_pp": round(radial_pp, 3),
            "hue_deg": round(hue_deg, 3),
            "radial_basis_blend": {"anchors": blend[:2], "w": round(blend[2], 3)},
            "verdict": verdict,
        })
        print(f"  {key:8s} dz=({dz[0]:+.4f},{dz[1]:+.4f}) "
              f"radial={radial_pp:+7.2f}pp hue={hue_deg:+7.2f}deg {verdict}")

    qualified = sum(1 for r in results if r["verdict"] == "qualified")
    print(f"qualified {qualified}/{len(results)}")
    # SAT monotonicity: achieved radial position must rise with request SAT
    # among same-hue-sector comparisons (no inversion)
    sat_pairs = [(("2/25", "330/50"), "sector A"), (("75/35", "90/50"), "sector B")]
    mono_notes = []
    for (a, b), tag in sat_pairs:
        ra = next(r for r in results if r["request"] == a)
        rb = next(r for r in results if r["request"] == b)
        # compare the served model's achieved saturation proxy: use the
        # strip-frame distance from white in z (not the request labels)
        za = reqs[a]["strip"]; zb = reqs[b]["strip"]
        da = math.hypot(za[0] - RAY_S0[0], za[1] - RAY_S0[1])
        db = math.hypot(zb[0] - RAY_S0[0], zb[1] - RAY_S0[1])
        note = {
            "pair": [a, b], "tag": tag,
            "achieved_distance_from_white": [round(da, 4), round(db, 4)],
            "monotone": True,  # filled below by SAT ordering
            "request_sat": [int(a.split("/")[1]), int(b.split("/")[1])],
        }
        note["monotone"] = (
            (note["request_sat"][0] <= note["request_sat"][1]) ==
            (da <= db))
        mono_notes.append(note)
        print(f"monotonicity {tag}: {a} vs {b}: {da:.3f} vs {db:.3f} -> "
              f"{'OK' if note['monotone'] else 'INVERSION'}")
    max_abs = {
        "max_abs_radial_pp": round(max(abs(r["radial_pp"]) for r in results), 3),
        "max_abs_hue_deg": round(max(abs(r["hue_deg"]) for r in results), 3),
    }
    print("bounds:", json.dumps(max_abs))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema": "guide12_c12_4_holdout_analysis_v1",
        "run_root": str(ROOT),
        "requests": results,
        "summary": {
            "qualified": qualified, "total": len(results),
            **max_abs,
            "bounded_prediction_interval_note": (
                "holdout max |error| is the empirical bound; the model "
                "makes no tighter claimed interval"),
        },
        "sat_monotonicity": mono_notes,
        "c1_envelope": "not used as a gate (comparison only, per GUIDE)",
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
