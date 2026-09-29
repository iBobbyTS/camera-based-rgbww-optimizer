"""GUIDE11 C6 final coverage map - aggregates all closed analysis artifacts.

Per GUIDE11 C6: per-hue valid intervals, best-tested, bounded upper requests,
chromaticity error with available intervals, legacy 58-feature status,
inversion ambiguity, current-map eligibility, INT applicability, and stop
reasons. Untested hues are marked untested; no hardware-limit claims.
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path("D:/rgbww-optimizer")
REPO_TMP = Path("C:/Users/iBobb/Projects/WLED-RGBWW/tmp")

C1C = json.loads((BASE / "guide11-c1/derived/c1-confirm-analysis-20260928.json").read_text(encoding="utf-8"))
C2A = json.loads((BASE / "guide11-c1/derived/c2-reachability-assessment-20260928.json").read_text(encoding="utf-8"))
C2S = json.loads((BASE / "guide11-c2/derived/c2-s25-analysis-20260928.json").read_text(encoding="utf-8"))
C4 = json.loads((BASE / "guide11-c4/derived/c4-holdout-analysis-20260928.json").read_text(encoding="utf-8"))
C5 = json.loads((BASE / "guide11-c5/derived/c5-int-analysis-20260928.json").read_text(encoding="utf-8"))
W8 = json.loads((BASE / "guide11-w8/guide11-white-final-report-20260928.json").read_text(encoding="utf-8"))

MAIN_HUES = (0, 60, 180, 240)


def main_hue_entry(hue: int) -> dict:
    tiers = {}
    for sat in (25, 50, 100):
        node = next(
            (t for t in C2A["per_node"] if t["hue"] == hue and t["sat"] == sat), None
        )
        s25 = next(
            (t for t in C2S["targets"] if t["hue"] == hue and t["sat"] == 25), None
        )
        if sat == 25 and s25 and s25.get("status") == "complete":
            tiers["25"] = {
                "z_distance": s25["z_distance_to_paired_ray"],
                "equiv_sat_error_pp": s25["equiv_sat_error_pp"],
                "n_observations": 1,
                "source": "c2_s25",
            }
        elif node:
            tiers[str(sat)] = {
                "z_distance": (
                    0.887 if (hue == 0 and sat == 100)
                    else next(
                        (t["confirm_z_distance_mean"] for t in C1C["targets"]
                         if t["hue"] == hue and t["sat"] == sat),
                        None,
                    )
                ),
                "equiv_sat_error_pp": node["equiv_sat_error_pp"],
                "equiv_hue_error_deg_upper_bound": node["equiv_hue_error_deg"],
                "n_observations": 3 if sat != 100 or hue != 0 else 2,
                "source": "c1c_confirm",
            }
    confirm = next(
        (t for t in C1C["targets"] if t["hue"] == hue and t["sat"] == 100), None
    )
    boundary = C2S["per_hue_boundary"][f"h{hue}"]
    int_levels = {100}
    for point in C5["color_points"]:
        if point["hue"] == hue and point["separable_int_levels"]:
            int_levels.update(point["separable_int_levels"])
    return {
        "hue": hue,
        "tested_sat_tiers": [25, 50, 100],
        "product_layer_valid": False,
        "bounded_best_by_tier": tiers,
        "best_tested_command_at_s100": confirm["selected_command"] if confirm else None,
        "reachability_boundary_bracket": boundary["reachability_boundary_bracket"],
        "s_best_tested_product_layer": 0,
        "covered_intervals": [],
        "search_upper_request": {
            "sat": 100,
            "status": "tested_bounded_best_outside_product_tolerance",
        },
        "repeatability_within_session": "three_observation_spread<=0.008_z (7/8 nodes; h0/s100 two valid confirms 0.0008)",
        "session_or_selection_caveats": (
            "h0/s100 B1 selection frame exposure-invalid (patch clipped at 1/8); "
            "confirm values from two healthy 1/25 FAST observations"
            if hue == 0 else "selection process flagged per GUIDE11 C1"
        ),
        "int_applicable_levels": sorted(int_levels),
        "int_note": (
            "INT100 baseline only" if sorted(int_levels) == [100]
            else f"separable down to {min(int_levels)} at tested color point"
        ),
        "inversion_ambiguous": True,
        "legacy_58feature": "preserved side-by-side in C1 batch artifacts; not a product pass criterion",
        "stop_reason": "product_tolerance_unmet_all_tested_tiers; downward search stopped at S25 per GUIDE11 C2",
    }


def non_main_entries() -> list[dict]:
    out = []
    for t in C4["targets"]:
        if t.get("status") != "complete":
            continue
        out.append({
            "hue": t["hue"],
            "sat": t["sat"],
            "model_interpolated_command": t["model_command"],
            "z_distance": t["z_distance_to_paired_ray"],
            "equiv_sat_error_pp": t["equiv_sat_error_pp"],
            "equiv_hue_error_deg_caveat": (
                "near-white inversion weakly determined" if t["sat"] <= 20 else "sparse S100 anchors"
            ),
            "product_layer_valid": bool(t.get("product_layer_valid")),
            "bracket_consistent": t["ray_bracket_consistent"],
            "stop_reason": "holdout evidence only; bounded best, no per-point search budget spent",
        })
    return out


coverage = {
    "schema": "guide11_final_coverage_v1",
    "date": "2026-09-29",
    "scope_statement": (
        "stable best approximations and empirically bounded reachable sets under "
        "the tested protocol, scales, neighborhoods and budgets; no hardware-limit claims"
    ),
    "steady_claim": False,
    "white_line": {
        "nodes_within_tolerance": W8.get("within_tolerance_point_estimate"),
        "node_count": W8.get("node_count"),
        "basis": "guide11-white-final-report-20260928.json (recomputed from real inputs)",
        "continuous_interpolation_supported_band": "5300-7250K |GM|<=65 with holdout support",
        "closed_permanently": ["1800/GM100 (GUIDE10)"],
        "true_long_observations": 8,
    },
    "main_hues": [main_hue_entry(h) for h in MAIN_HUES],
    "non_main_hue_holdouts": non_main_entries(),
    "int_separability": {
        "verdict": "not_separable_below_int100_except_h90_s50_to_int50",
        "per_point_lowest_separable": {
            f"h{p['hue']}_s{p['sat']}": p["lowest_separable_int"] for p in C5["color_points"]
        },
        "note": "Ray itself drifts with INT (0.007-0.077 z); offsets are paired differences; INT100 trivially meets its own baseline",
    },
    "sat0_white_command": "single white command; hue not_applicable (P6 self-check)",
    "untested": {
        "hues_without_dedicated_evidence": [20, 40, 80, 100, 110, 130, 140, 160, 170, 190, 200, 220, 230, 250, 260, 290, 310, 320, 340]
        + [],
        "statement": "untested hues remain untested; not 0%",
    },
    "interval_status": (
        "conditional/prediction intervals exist only at the six N1 co-located white "
        "anchors; color points report n and spread instead; pooled transfer unverified"
    ),
}

out_repo = REPO_TMP / "guide11-final-coverage-20260929.json"
out_repo.write_text(json.dumps(coverage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
(BASE / "guide11-c1/derived").mkdir(parents=True, exist_ok=True)
(BASE / "guide11-c1/derived/guide11-final-coverage-20260929.json").write_text(
    json.dumps(coverage, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(f"-> {out_repo}")
for h in coverage["main_hues"]:
    print(
        f"H{h['hue']:>3}: boundary={h['reachability_boundary_bracket']} "
        f"int={h['int_applicable_levels']} s100_z={h['bounded_best_by_tier'].get('100', {}).get('z_distance')}"
    )
