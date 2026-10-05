"""GUIDE12 C12-1 offline tables (frozen, read-only).

The three tables GUIDE 12.GUIDE.md C12-1 requires before any new capture:
1. old-mapping self-inverse error on Ray itself: invert the measured Ray z
   of the ten GUIDE11-C4 holdout targets through the frozen C3 anchor map
   (piecewise-linear (hue,SAT)->z ruler) and compare recovered menu labels;
   multi-solution candidates counted as local minima of the misfit field;
2. same-command valid strip - local Ray direct z differences (components);
3. actual fullscale qualification of the commands used (any channel 4095).

Budget references: old GUIDE11 verdict tolerances hue 2.0 deg / sat 2.0 pp;
new GUIDE12 mapping budget hue 0.5 deg / sat 0.5 pp.

Inputs (retained artifacts, no device work):
- D:/rgbww-optimizer/guide11/guide11-c1/derived/c3-anchor-self-check-20260925.json
- D:/rgbww-optimizer/guide11/guide11-c4/derived/c4-holdout-analysis-20260928.json
Output: D:/rgbww-optimizer/guide12-c12/derived/c12-1-offline-tables-20261005.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ANCHORS = Path(
    "D:/rgbww-optimizer/guide11/guide11-c1/derived/c3-anchor-self-check-20260925.json"
)
C4 = Path(
    "D:/rgbww-optimizer/guide11/guide11-c4/derived/c4-holdout-analysis-20260928.json"
)
OUT = Path(
    "D:/rgbww-optimizer/guide12-c12/derived/c12-1-offline-tables-20261005.json"
)
OLD_TOL = {"hue_deg": 2.0, "sat_pp": 2.0}
NEW_BUDGET = {"hue_deg": 0.5, "sat_pp": 0.5}


def hue_interp(table: dict[int, tuple], hue: float) -> tuple[float, float]:
    hues = sorted(table)
    hue = hue % 360.0
    for lo, hi in zip(hues, hues[1:] + [hues[0] + 360]):
        if lo <= hue <= hi:
            t = 0.0 if hi == lo else (hue - lo) / (hi - lo)
            zlo, zhi = table[lo], table[hi % 360]
            return (
                zlo[0] + t * (zhi[0] - zlo[0]),
                zlo[1] + t * (zhi[1] - zlo[1]),
            )
    raise ValueError(hue)


class AnchorMap:
    """Piecewise-linear (hue, SAT) -> Ray z ruler from the frozen anchors."""

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

    def z_at(self, hue: float, sat: float) -> tuple[float, float]:
        if sat <= 0:
            return self.white
        z50 = hue_interp(self.s50, hue % 360)
        if sat <= 50:
            t = sat / 50.0
            return (
                self.white[0] + t * (z50[0] - self.white[0]),
                self.white[1] + t * (z50[1] - self.white[1]),
            )
        z100 = hue_interp(self.s100, hue % 360)
        t = (sat - 50) / 50.0
        return (
            z50[0] + t * (z100[0] - z50[0]),
            z50[1] + t * (z100[1] - z50[1]),
        )

    def misfit_field(self, zx: float, zy: float):
        """Dense misfit grid + count of local minima (multi-solution)."""
        hue_steps = [h / 2.0 for h in range(0, 720)]  # 0.5 deg
        sat_steps = [s / 2.0 for s in range(0, 202)]  # 0.5 pp
        grid = [
            [
                math.hypot(
                    zx - self.z_at(hue, sat)[0], zy - self.z_at(hue, sat)[1]
                )
                for sat in sat_steps
            ]
            for hue in hue_steps
        ]
        minima = []
        for i in range(len(hue_steps)):
            for j in range(len(sat_steps)):
                d = grid[i][j]
                neighbors = []
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ii, jj = i + di, j + dj
                    if 0 <= ii < len(hue_steps) and 0 <= jj < len(sat_steps):
                        neighbors.append(grid[ii][jj])
                if all(d <= n for n in neighbors):
                    minima.append((hue_steps[i], sat_steps[j], d))
        best = min(minima, key=lambda m: m[2])
        # merge minima closer than 3 deg hue / 3 pp sat
        merged = []
        for m in sorted(minima, key=lambda m: m[2]):
            if all(
                abs(((m[0] - k[0] + 180) % 360) - 180) > 3.0 or abs(m[1] - k[1]) > 3.0
                for k in merged
            ):
                merged.append(m)
        return best, merged

    def invert(self, zx: float, zy: float) -> dict:
        best, merged = self.misfit_field(zx, zy)
        return {
            "equiv_hue": best[0],
            "equiv_sat": best[1],
            "residual_z": best[2],
            "local_minima_count": len(merged),
            "multi_solution_candidates": [
                {"hue": h, "sat": s, "residual_z": d} for h, s, d in merged
            ],
        }


def circular_hue_error(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0)


def main() -> int:
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    amap = AnchorMap(anchors["grid"])
    c4 = json.loads(C4.read_text(encoding="utf-8"))

    table1, table2, table3 = [], [], []
    for t in c4["targets"]:
        zx = t["ray_z_mean"]["log_R_over_G"]
        zy = t["ray_z_mean"]["log_B_over_G"]
        inv = amap.invert(zx, zy)
        hue_err = circular_hue_error(inv["equiv_hue"], t["hue"])
        sat_err = inv["equiv_sat"] - t["sat"]
        table1.append({
            "menu_hue": t["hue"], "menu_sat": t["sat"],
            "recovered_hue": inv["equiv_hue"], "recovered_sat": inv["equiv_sat"],
            "hue_error_deg": hue_err, "sat_error_pp": sat_err,
            "residual_z": inv["residual_z"],
            "local_minima_count": inv["local_minima_count"],
            "within_old_2deg_2pp": hue_err <= OLD_TOL["hue_deg"] and abs(sat_err) <= OLD_TOL["sat_pp"],
            "within_new_05deg_05pp": hue_err <= NEW_BUDGET["hue_deg"] and abs(sat_err) <= NEW_BUDGET["sat_pp"],
        })
        dz_r = t["strip_z"]["log_R_over_G"] - zx
        dz_b = t["strip_z"]["log_B_over_G"] - zy
        table2.append({
            "menu_hue": t["hue"], "menu_sat": t["sat"],
            "dz_log_R_over_G": dz_r, "dz_log_B_over_G": dz_b,
            "z_distance": math.hypot(dz_r, dz_b),
            "recorded_z_distance_to_paired_ray": t.get("z_distance_to_paired_ray"),
        })
        cmd = t["model_command"]
        table3.append({
            "menu_hue": t["hue"], "menu_sat": t["sat"],
            "command": cmd,
            "max_channel": max(cmd.values()),
            "actual_fullscale": any(v == 4095 for v in cmd.values()),
            "clipped_channels": t.get("clipped_channels"),
            "saturated_fraction": t.get("saturated_fraction"),
            "frame_classification": t.get("frame_classification"),
        })

    hue_errs = [r["hue_error_deg"] for r in table1]
    sat_errs = [abs(r["sat_error_pp"]) for r in table1]
    result = {
        "schema": "guide12_c12_1_offline_tables_v1",
        "inputs": {
            "anchor_map": str(ANCHORS),
            "c4_holdout": str(C4),
            "note": (
                "old C3 ruler = piecewise-linear (hue,SAT)->z over the frozen "
                "11-anchor grid (SAT0 white + 6xS50 + 4xS100); Ray z = fresh "
                "GUIDE11-C4 per-target Ray observations"
            ),
        },
        "budgets": {"old_verdict_tol": OLD_TOL, "new_mapping_budget": NEW_BUDGET},
        "table1_old_mapping_self_inverse_on_ray": table1,
        "table1_summary": {
            "n": len(table1),
            "hue_error_deg_max": max(hue_errs),
            "hue_error_deg_median": sorted(hue_errs)[len(hue_errs) // 2],
            "sat_error_pp_absmax": max(sat_errs),
            "within_old_count": sum(r["within_old_2deg_2pp"] for r in table1),
            "within_new_count": sum(r["within_new_05deg_05pp"] for r in table1),
            "targets_with_multisolution": sum(
                r["local_minima_count"] >= 2 for r in table1),
        },
        "table2_same_command_strip_minus_ray_z": table2,
        "table3_actual_fullscale_qualification": table3,
        "conclusions": {},
    }
    t1 = result["table1_summary"]
    result["conclusions"] = {
        "old_ruler_self_inverse": (
            f"{t1['within_old_count']}/{t1['n']} targets within old 2deg/2pp; "
            f"{t1['within_new_count']}/{t1['n']} within new 0.5deg/0.5pp budget; "
            f"max hue error {t1['hue_error_deg_max']:.2f} deg, "
            f"max |sat| error {t1['sat_error_pp_absmax']:.1f} pp; "
            f"{t1['targets_with_multisolution']} targets multi-solution"
        ),
        "mapping_misfit_is_not_gamut_shortage": (
            "strip-ray z differences and ruler inverse errors are reported "
            "separately; neither is labelled gamut insufficiency"
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    print("表1（旧C3尺对Ray自身反解）:")
    for r in table1:
        print(
            f"  ({r['menu_hue']:3d},{r['menu_sat']:3d}) -> "
            f"({r['recovered_hue']:6.1f},{r['recovered_sat']:5.1f}) "
            f"Δhue={r['hue_error_deg']:5.2f}° Δsat={r['sat_error_pp']:+6.1f}pp "
            f"多解={r['local_minima_count']} 旧门={'✓' if r['within_old_2deg_2pp'] else '✗'} "
            f"新预算={'✓' if r['within_new_05deg_05pp'] else '✗'}"
        )
    print(result["conclusions"]["old_ruler_self_inverse"])
    print("表2 max |dz|:", max(r["z_distance"] for r in table2))
    print("表3 满幅:", sum(r["actual_fullscale"] for r in table3), "/", len(table3))
    return 0


if __name__ == "__main__":
    sys.exit(main())
