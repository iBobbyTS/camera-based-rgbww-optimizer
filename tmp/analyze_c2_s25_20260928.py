"""GUIDE11 C2 S25 descent-tier analysis (frozen before completion review).

Two roots (interrupted r1 + recovery r2-suffix); per target the bracket must
come intact from a single root (latest complete root wins, orphan rows from
the interrupted root recorded). Per target: Ray bracket consistency, strip
model-command z distance, full-frame exposure guard, equivalent (hue, SAT)
anchor-map inversion, product-layer validity. Per hue: the SAT reachability
boundary bracket after the S25 tier — S25 valid closes at (25,50); S25
invalid closes at (0,25) and stops the downward search per GUIDE11 C2.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.frame_exposure import frame_exposure_profile

ROOTS = [
    Path("D:/rgbww-optimizer/guide11-c2/formal-c2s25-20260928-r1"),
    Path("D:/rgbww-optimizer/guide11-c2/formal-c2s25-20260928-r2-suffix"),
]
ANCHORS = Path("D:/rgbww-optimizer/guide11-c1/derived/c3-anchor-self-check-20260925.json")
OUT = Path("D:/rgbww-optimizer/guide11-c2/derived/c2-s25-analysis-20260928.json")

HUE_TOL_DEG = 2.0
SAT_TOL_PP = 2.0
TARGETS = [(0, 25), (60, 25), (180, 25), (240, 25)]


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
    lo = max((h for h in hues if h <= hue + 1e-9), default=hues[-1] - 360)
    hi = min((h for h in hues if h >= hue - 1e-9), default=hues[0] + 360)
    zlo, zhi = zs[lo % 360], zs[hi % 360]
    t = 0.0 if hi == lo else (hue - lo) / (hi - lo)
    return (zlo[0] + t * (zhi[0] - zlo[0]), zlo[1] + t * (zhi[1] - zlo[1]))


class AnchorMap:
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
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    amap = AnchorMap(anchors["grid"])

    rows_by_root = []
    for root in ROOTS:
        rows = {}
        ledger = root / "captures.jsonl"
        if not ledger.is_file():
            continue
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            step = row.get("plan_step", {})
            rows.setdefault((int(step["c1_hue"]), int(step["c1_sat"])), {})[
                str(step["role"]).rsplit("_", 1)[-1]
            ] = row["capture_id"]
        rows_by_root.append((root, rows))

    targets = []
    saturated = 0
    for hue, sat in TARGETS:
        chosen = None
        for root, rows in reversed(rows_by_root):
            have = rows.get((hue, sat), {})
            if {"before", "after", "point"}.issubset(have):
                chosen = (root, have)
                break
        orphans = []
        for root, rows in rows_by_root:
            if chosen and root == chosen[0]:
                continue
            partial = rows.get((hue, sat), {})
            orphans.extend(f"{root.name}:{cid}" for cid in partial.values())
        if chosen is None:
            targets.append({"hue": hue, "sat": sat, "status": "missing", "orphan_rows": orphans})
            continue
        root, have = chosen
        z_before, z_after = z_of(root, have["before"]), z_of(root, have["after"])
        ray_mean = {axis: (z_before[axis] + z_after[axis]) / 2 for axis in z_before}
        strip_row = next(
            json.loads(line)
            for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if json.loads(line)["capture_id"] == have["point"]
        )
        profile = frame_exposure_profile(str((strip_row.get("capture") or {}).get("saved_file", "")))
        if profile["classification"] == "saturated":
            saturated += 1
        zs = z_of(root, have["point"])
        inv = amap.invert(zs)
        equiv_hue_err = ((inv["equiv_hue"] - hue + 180) % 360) - 180
        equiv_sat_err = inv["equiv_sat"] - sat
        valid = (
            abs(equiv_hue_err) <= HUE_TOL_DEG
            and abs(equiv_sat_err) <= SAT_TOL_PP
            and sat >= 25
        )
        targets.append({
            "hue": hue,
            "sat": sat,
            "status": "complete",
            "bracket_root": root.name,
            "orphan_rows": orphans,
            "ray_bracket_consistent": dist(z_before, z_after) < 0.02,
            "ray_bracket_z_distance": dist(z_before, z_after),
            "ray_z_mean": ray_mean,
            "strip_z": zs,
            "z_distance_to_paired_ray": dist(zs, ray_mean),
            "frame_classification": profile["classification"],
            "saturated_fraction": profile["saturated_fraction"],
            "equivalent": inv,
            "equiv_hue_error_deg": equiv_hue_err,
            "equiv_sat_error_pp": equiv_sat_err,
            "product_layer_valid": valid,
        })

    per_hue = {}
    for hue, _sat in TARGETS:
        node = next(t for t in targets if t["hue"] == hue)
        if node.get("product_layer_valid"):
            per_hue[f"h{hue}"] = {
                "s25_valid": True,
                "reachability_boundary_bracket": [25, 50],
                "boundary_status": "valid_at_25_invalid_at_50",
            }
        else:
            per_hue[f"h{hue}"] = {
                "s25_valid": False,
                "reachability_boundary_bracket": [0, 25],
                "boundary_status": "invalid_at_25_white_only_valid",
                "downward_search_stopped": True,
            }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "schema": "guide11_c2_s25_analysis_v1",
        "run_roots": [str(r) for r in ROOTS],
        "anchor_map": str(ANCHORS),
        "tolerances": {"hue_deg": HUE_TOL_DEG, "sat_pp": SAT_TOL_PP},
        "targets": targets,
        "per_hue_boundary": per_hue,
        "saturated_frames": saturated,
        "inversion_caveat": (
            "equivalent hue/SAT from piecewise-linear anchor-map inversion; "
            "near-white hue is weakly determined (P6 ambiguity note)"
        ),
        "steady_claim": False,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"targets complete: {sum(1 for t in targets if t.get('status')=='complete')}/4 | saturated: {saturated} -> {OUT}")
    for t in targets:
        if t.get("status") == "complete":
            print(
                f"H{t['hue']:>3}/S25  zdist={t['z_distance_to_paired_ray']:.3f}  "
                f"bracket={'ok' if t['ray_bracket_consistent'] else 'FAIL'}  root={t['bracket_root']}  "
                f"equivHue={t['equiv_hue_error_deg']:+7.2f}deg equivSAT={t['equiv_sat_error_pp']:+6.2f}pp  "
                f"valid={t['product_layer_valid']}"
            )
        else:
            print(f"H{t['hue']:>3}/S25  status={t['status']}")


if __name__ == "__main__":
    main()
