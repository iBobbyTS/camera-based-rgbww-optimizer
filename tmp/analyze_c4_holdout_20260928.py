"""GUIDE11 C4 experience-holdout analysis (frozen before completion review).

Per target: fresh Ray bracket consistency, strip model-command z distance to
the paired Ray mean, full-frame exposure guard, and equivalent (hue, SAT)
inversion against the C3 anchor map (white / S50 / S100 layers, ambiguity
flagged). Cross-target checks: monotone hue rotation across the six S75
sectors, SAT monotonicity on the low-SAT white-blend points. No pass/fail
invented beyond the preregistered product tolerances; steady_claim=False.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.frame_exposure import frame_exposure_profile

RUN = Path("D:/rgbww-optimizer/guide11-c4/formal-c4-20260928-r1")
ANCHORS = Path("D:/rgbww-optimizer/guide11-c1/derived/c3-anchor-self-check-20260925.json")
OUT = Path("D:/rgbww-optimizer/guide11-c4/derived/c4-holdout-analysis-20260928.json")

HUE_TOL_DEG = 2.0
SAT_TOL_PP = 2.0
S50_HUES = (0, 60, 120, 180, 240, 300)
S100_HUES = (0, 60, 180, 240)


def planes_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads((root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    return {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }


def z_of(root: Path, capture_id: str) -> dict[str, float]:
    p = planes_of(root, capture_id)
    g = 0.5 * (p["G1"] + p["G2"])
    return {"log_R_over_G": math.log(p["R"] / g), "log_B_over_G": math.log(p["B"] / g)}


def dist(a, b) -> float:
    return math.hypot(a["log_R_over_G"] - b["log_R_over_G"], a["log_B_over_G"] - b["log_B_over_G"])


def hue_interp(zs: dict[int, tuple], hue: float) -> tuple[float, float]:
    hues = sorted(zs)
    lo = max(h for h in hues if h <= hue + 1e-9) if hue >= hues[0] else hues[-1] - 360
    hi = min(h for h in hues if h >= hue - 1e-9) if hue <= hues[-1] else hues[0] + 360
    zlo, zhi = zs[lo % 360], zs[hi % 360]
    t = 0.0 if hi == lo else (hue - lo) / (hi - lo)
    return (zlo[0] + t * (zhi[0] - zlo[0]), zlo[1] + t * (zhi[1] - zlo[1]))


class AnchorMap:
    """Piecewise-linear (hue, SAT) -> Ray z map from the frozen anchors."""

    def __init__(self, grid: list[dict]) -> None:
        self.white = None
        self.s50: dict[int, tuple] = {}
        self.s100: dict[int, tuple] = {}
        for a in grid:
            z = (a["z_mean"]["log_R_over_G"], a["z_mean"]["log_B_over_G"])
            if a["sat"] == 0:
                self.white = z
            elif a["sat"] == 50:
                self.s50[a["hue"]] = z
            elif a["sat"] == 100:
                self.s100[a["hue"]] = z

    def z_at(self, hue: float, sat: float) -> tuple[float, float] | None:
        if self.white is None or not self.s50:
            return None
        if sat <= 0:
            return self.white
        z50 = hue_interp(self.s50, hue % 360)
        if sat <= 50:
            t = sat / 50.0
            return (self.white[0] + t * (z50[0] - self.white[0]), self.white[1] + t * (z50[1] - self.white[1]))
        if not self.s100:
            return None
        z100 = hue_interp(self.s100, hue % 360)
        t = (sat - 50) / 50.0
        return (z50[0] + t * (z100[0] - z50[0]), z50[1] + t * (z100[1] - z50[1]))

    def invert(self, z: dict[str, float]) -> dict:
        zx, zy = z["log_R_over_G"], z["log_B_over_G"]
        best = None
        for hue10 in range(0, 3600):
            hue = hue10 / 10.0
            for sat in range(0, 101):
                p = self.z_at(hue, float(sat))
                if p is None:
                    continue
                d = math.hypot(zx - p[0], zy - p[1])
                if best is None or d < best[2]:
                    best = (hue, float(sat), d)
        return {"equiv_hue": best[0], "equiv_sat": best[1], "residual_z": best[2]}


def main() -> None:
    spec = json.loads((RUN / "experiment-spec.json").read_text(encoding="utf-8"))
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    amap = AnchorMap(anchors["grid"])

    rows = {}
    for line in (RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        step = row.get("plan_step", {})
        rows.setdefault((int(step["c1_hue"]), int(step["c1_sat"])), {})[
            str(step["role"]).rsplit("_", 1)[-1]
        ] = row["capture_id"]

    targets = []
    saturated = 0
    for contract in spec["analysis_contract"]["targets"]:
        key = (int(contract["hue"]), int(contract["sat"]))
        have = rows.get(key, {})
        if not {"before", "after", "point"}.issubset(have):
            targets.append({**contract, "status": "pending", "have": sorted(have)})
            continue
        z_before, z_after = z_of(RUN, have["before"]), z_of(RUN, have["after"])
        ray_mean = {
            axis: (z_before[axis] + z_after[axis]) / 2 for axis in z_before
        }
        strip_row = next(
            r for r in (RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if json.loads(r)["capture_id"] == have["point"]
        )
        profile = frame_exposure_profile(str((json.loads(strip_row).get("capture") or {}).get("saved_file", "")))
        if profile["classification"] == "saturated":
            saturated += 1
        zs = z_of(RUN, have["point"])
        inv = amap.invert(zs)
        targets.append({
            **contract,
            "status": "complete",
            "ray_bracket_consistent": dist(z_before, z_after) < 0.02,
            "ray_bracket_z_distance": dist(z_before, z_after),
            "ray_z_mean": ray_mean,
            "strip_z": zs,
            "z_distance_to_paired_ray": dist(zs, ray_mean),
            "frame_classification": profile["classification"],
            "saturated_fraction": profile["saturated_fraction"],
            "equivalent": inv,
            "equiv_hue_error_deg": ((inv["equiv_hue"] - key[0] + 180) % 360) - 180,
            "equiv_sat_error_pp": inv["equiv_sat"] - key[1],
            "product_layer_valid": (
                abs(((inv["equiv_hue"] - key[0] + 180) % 360) - 180) <= HUE_TOL_DEG
                and abs(inv["equiv_sat"] - key[1]) <= SAT_TOL_PP
                and key[1] >= 25
            ),
        })

    done = [t for t in targets if t.get("status") == "complete"]
    sectors = sorted(
        (t for t in done if t["sat"] == 75 and t["hue"] not in (350,)),
        key=lambda t: t["hue"],
    )
    white = amap.white
    turns = []
    for a, b in zip(sectors, sectors[1:] + sectors[:1]):
        def v(t):
            return (t["strip_z"]["log_R_over_G"] - white[0], t["strip_z"]["log_B_over_G"] - white[1])
        va, vb = v(a), v(b)
        turns.append((b["hue"], va[0] * vb[1] - va[1] * vb[0]))
    hue_monotone = all(cross > 0 for _, cross in turns) or all(cross < 0 for _, cross in turns)

    sat_mono = {}
    for hue, lo, hi in ((90, 20, 75), (210, 10, 75)):
        t_lo = next((t for t in done if t["hue"] == hue and t["sat"] == lo), None)
        t_hi = next((t for t in done if t["hue"] == hue and t["sat"] == hi), None)
        if t_lo and t_hi:
            d_lo = math.hypot(t_lo["strip_z"]["log_R_over_G"] - white[0], t_lo["strip_z"]["log_B_over_G"] - white[1])
            d_hi = math.hypot(t_hi["strip_z"]["log_R_over_G"] - white[0], t_hi["strip_z"]["log_B_over_G"] - white[1])
            sat_mono[f"h{hue}"] = {"d_white_s{lo}": d_lo, "d_white_s{hi}": d_hi, "monotone": d_hi > d_lo}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "schema": "guide11_c4_holdout_analysis_v1",
        "run_root": str(RUN),
        "anchor_map": str(ANCHORS),
        "tolerances": {"hue_deg": HUE_TOL_DEG, "sat_pp": SAT_TOL_PP},
        "targets": targets,
        "hue_rotation_monotone_across_s75_sectors": hue_monotone,
        "sector_cross_products": turns,
        "low_sat_monotonicity": sat_mono,
        "saturated_frames": saturated,
        "inversion_caveat": (
            "equivalent hue/SAT from piecewise-linear anchor-map inversion; "
            "anchor-density ambiguity flagged in the P6 self-check applies"
        ),
        "steady_claim": False,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"targets complete: {len(done)}/{len(targets)} | saturated frames: {saturated} -> {OUT}")
    for t in done:
        print(
            f"H{t['hue']:>3}/S{t['sat']:>3}  zdist={t['z_distance_to_paired_ray']:.3f}  "
            f"bracket={'ok' if t['ray_bracket_consistent'] else 'FAIL'}  "
            f"equivHue={t['equiv_hue_error_deg']:+7.2f}deg equivSAT={t['equiv_sat_error_pp']:+6.2f}pp  "
            f"resid={t['equivalent']['residual_z']:.3f}  frame={t['frame_classification']}"
        )


if __name__ == "__main__":
    main()
