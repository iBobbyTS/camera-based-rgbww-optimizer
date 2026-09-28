"""GUIDE11 C2 per-hue SAT reachability assessment (offline, C1C evidence only).

Per main hue (H0/H60/H180/H240) and tested SAT tier (S50/S100):
decompose the confirmed strip-vs-Ray z offset into the hue's own S50->S100
radial direction (SAT-equivalent error) and the tangential direction
(hue-equivalent error, using adjacent-hue anchors at the same SAT for the
local degrees-per-z scale). First-order local geometry; tangential component
conservatively includes chromaticity-shape mismatch. Used to decide whether
the GUIDE C2 S25 descent tier is necessary (no product-layer valid node at
S50) and to report s_best_tested / covered_intervals / search_upper_request.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

C1C = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-confirm-analysis-20260928.json")
ANCHORS = Path("D:/rgbww-optimizer/guide11-c1/derived/c3-anchor-self-check-20260925.json")
OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c2-reachability-assessment-20260928.json")

HUE_TOL_DEG = 2.0
SAT_TOL_PP = 2.0


def key(h, s):
    return f"h{h}_s{s}"


def main() -> None:
    c1c = json.loads(C1C.read_text(encoding="utf-8"))
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    anchor_z = {
        (a["hue"], a["sat"]): (a["z_mean"]["log_R_over_G"], a["z_mean"]["log_B_over_G"])
        for a in anchors["grid"]
    }
    targets = {f"h{t['hue']}_s{t['sat']}": t for t in c1c["targets"]}

    out = {
        "schema": "guide11_c2_reachability_assessment_v1",
        "inputs": {
            "c1c_confirm_analysis": str(C1C),
            "anchor_self_check": str(ANCHORS),
        },
        "tolerances": {"hue_deg": HUE_TOL_DEG, "sat_pp": SAT_TOL_PP},
        "per_node": [],
        "per_hue": {},
        "s25_descent_necessary": None,
        "steady_claim": False,
    }

    for hue in (0, 60, 180, 240):
        r50 = targets[key(hue, 50)]["ray_z_mean"]
        r100 = targets[key(hue, 100)]["ray_z_mean"]
        seg = (r100["log_R_over_G"] - r50["log_R_over_G"], r100["log_B_over_G"] - r50["log_B_over_G"])
        seg_len = math.hypot(*seg)
        # degrees-per-z tangential scale at this hue/SAT from adjacent-hue anchors
        deg_scale = {}
        for sat in (50, 100):
            dists = []
            for other in (hue - 60, hue + 60):
                z = anchor_z.get((other % 360, sat))
                rz = anchor_z.get((hue, sat)) or (r50 if sat == 50 else r100)
                if z is None or rz is None:
                    continue
                dists.append(math.hypot(z[0] - rz[0], z[1] - rz[1]) / 60.0)
            if dists:
                deg_scale[sat] = sum(dists) / len(dists)

        for sat in (50, 100):
            t = targets[key(hue, sat)]
            zs = [c["z"] for c in t["confirms"] if c["frame_classification"] != "saturated"]
            if t["hue"] == 0 and t["sat"] == 100:
                zs = [c["z"] for c in t["confirms"]]  # patch-validated saturated-tagged frames
            sx = sum(z["log_R_over_G"] for z in zs) / len(zs)
            sy = sum(z["log_B_over_G"] for z in zs) / len(zs)
            rx = r50["log_R_over_G"] + (seg[0] if sat == 100 else 0.0)
            ry = r50["log_B_over_G"] + (seg[1] if sat == 100 else 0.0)
            dx, dy = sx - rx, sy - ry
            a = (dx * seg[0] + dy * seg[1]) / seg_len  # radial component
            tcomp = (dx * -seg[1] + dy * seg[0]) / seg_len  # tangential component
            d_sat = a / seg_len * 50.0
            d_hue = (tcomp / deg_scale[sat]) if sat in deg_scale else None
            valid = (
                d_hue is not None and abs(d_hue) <= HUE_TOL_DEG and abs(d_sat) <= SAT_TOL_PP
            )
            out["per_node"].append(
                {
                    "hue": hue,
                    "sat": sat,
                    "n_valid_observations": len(zs),
                    "z_offset": {"log_R_over_G": dx, "log_B_over_G": dy},
                    "radial_z": a,
                    "tangential_z": tcomp,
                    "equiv_sat_error_pp": d_sat,
                    "equiv_hue_error_deg": d_hue,
                    "deg_scale_z_per_deg": deg_scale.get(sat),
                    "product_layer_valid": valid,
                    "note": "H0/S100 uses the two patch-validated 1/25 confirms; B1 selection frame exposure-invalid"
                    if (hue == 0 and sat == 100)
                    else "",
                }
            )

        nodes = [n for n in out["per_node"] if n["hue"] == hue]
        valid_sats = [n["sat"] for n in nodes if n["product_layer_valid"]]
        out["per_hue"][f"h{hue}"] = {
            "s_best_tested": max(valid_sats) if valid_sats else 0,
            "covered_intervals": (
                [{"from": 50, "to": 100, "basis": "two tested tiers both valid; interior untested"}]
                if len(valid_sats) == 2
                else []
            ),
            "search_upper_request": {
                "sat": 100,
                "status": "tested_bounded_best_outside_product_tolerance",
                "z_distance_confirm_mean": targets[key(hue, 100)]["confirm_z_distance_mean"],
            },
            "valid_tiers": valid_sats,
        }

    # S25 descent is necessary iff every hue lacks a product-layer valid node at S50
    need_s25 = all(hv["s_best_tested"] == 0 for hv in out["per_hue"].values())
    out["s25_descent_necessary"] = need_s25
    out["s25_targets_if_needed"] = (
        [
            {"hue": h, "sat": 25, "basis": "S50 invalid at product layer; GUIDE C2 last descent tier"}
            for h in (0, 60, 180, 240)
        ]
        if need_s25
        else []
    )
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"nodes: {len(out['per_node'])} | s25 necessary: {need_s25} -> {OUT}")
    for n in out["per_node"]:
        dh = n["equiv_hue_error_deg"]
        print(
            f"H{n['hue']:>3}/S{n['sat']:>3}  dSAT={n['equiv_sat_error_pp']:+7.2f}pp  "
            f"dHue={f'{dh:+7.2f}deg' if dh is not None else '  n/a   '}  "
            f"radial_z={n['radial_z']:+.3f} tang_z={n['tangential_z']:+.3f}  valid={n['product_layer_valid']}"
        )


if __name__ == "__main__":
    main()
