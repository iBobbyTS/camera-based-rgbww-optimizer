"""GUIDE11 C5 INT separability analysis (frozen at completion).

Per color point (h0/s0 white, h90/s50, h0/s100, h180/s100) and INT tier
(100/50/20/5): paired Ray bracket consistency, strip z, the strip-Ray
chromaticity offset vector, and that offset's drift from its INT100 value.
Ray's own drift with INT is reported too (low PWM is not presumed
color-stable for either source). Preregistered separability rule: a tier is
separable iff both offset-drift log ratios stay within 0.01 of the INT100
baseline AND the strip frame is observable (not dark/saturated flagged).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.frame_exposure import frame_exposure_profile

RUN = Path("D:/rgbww-optimizer/guide11-c5/formal-c5-20260928-r1")
OUT = Path("D:/rgbww-optimizer/guide11-c5/derived/c5-int-analysis-20260928.json")

DRIFT_TOL = 0.01
COLOR_POINTS = [(0, 0), (90, 50), (0, 100), (180, 100)]
INT_LEVELS = (100, 50, 20, 5)


def planes_of(capture_id: str) -> dict[str, float]:
    stats = json.loads((RUN / "measurements" / f"{capture_id}.patch-statistics.json").read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    return {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }


def z_of(capture_id: str) -> dict[str, float]:
    p = planes_of(capture_id)
    g = 0.5 * (p["G1"] + p["G2"])
    return {"log_R_over_G": math.log(p["R"] / g), "log_B_over_G": math.log(p["B"] / g)}


def dist(a, b) -> float:
    return math.hypot(a["log_R_over_G"] - b["log_R_over_G"], a["log_B_over_G"] - b["log_B_over_G"])


def main() -> None:
    rows = {}
    strip_rows = {}
    for line in (RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        step = row.get("plan_step", {})
        key = (int(step["c1_hue"]), int(step["c1_sat"]), int(step["c5_intensity_percent"]))
        rows.setdefault(key, {})[str(step["role"]).rsplit("_", 1)[-1]] = row["capture_id"]
        if step["source_id"] == "strip":
            strip_rows[key] = row

    points = []
    for hue, sat in COLOR_POINTS:
        tiers = []
        baseline = None
        for level in INT_LEVELS:
            key = (hue, sat, level)
            have = rows.get(key, {})
            if not {"before", "after", "point"}.issubset(have):
                tiers.append({"int_percent": level, "status": "missing"})
                continue
            z_before, z_after = z_of(have["before"]), z_of(have["after"])
            ray_mean = {axis: (z_before[axis] + z_after[axis]) / 2 for axis in z_before}
            strip_row = strip_rows[key]
            profile = frame_exposure_profile(str((strip_row.get("capture") or {}).get("saved_file", "")))
            zs = z_of(have["point"])
            offset = {
                "log_R_over_G": zs["log_R_over_G"] - ray_mean["log_R_over_G"],
                "log_B_over_G": zs["log_B_over_G"] - ray_mean["log_B_over_G"],
            }
            observable = profile["classification"] == "normal"
            tier = {
                "int_percent": level,
                "status": "complete",
                "ray_bracket_consistent": dist(z_before, z_after) < 0.02,
                "ray_z_mean": ray_mean,
                "strip_z": zs,
                "offset_strip_minus_ray": offset,
                "z_distance_to_paired_ray": dist(zs, ray_mean),
                "frame_classification": profile["classification"],
                "observable": observable,
            }
            if baseline is None and level == 100:
                baseline = offset
            if baseline is not None:
                drift = {
                    axis: offset[axis] - baseline[axis] for axis in offset
                }
                tier["offset_drift_from_int100"] = drift
                tier["separable"] = (
                    observable
                    and abs(drift["log_R_over_G"]) <= DRIFT_TOL
                    and abs(drift["log_B_over_G"]) <= DRIFT_TOL
                )
            tiers.append(tier)
        # Ray's own drift with INT (reported, not presumed zero).
        ray_zs = {t["int_percent"]: t.get("ray_z_mean") for t in tiers if t.get("status") == "complete"}
        for t in tiers:
            if t.get("status") == "complete" and ray_zs.get(100) and t["int_percent"] != 100:
                t["ray_own_drift_from_int100"] = dist(t["ray_z_mean"], ray_zs[100])
        separable_tiers = [t["int_percent"] for t in tiers if t.get("separable")]
        points.append({
            "hue": hue,
            "sat": sat,
            "tiers": tiers,
            "lowest_separable_int": min(separable_tiers) if separable_tiers else None,
            "separable_int_levels": separable_tiers,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    all_lowest = [p["lowest_separable_int"] for p in points if p["lowest_separable_int"] is not None]
    out = {
        "schema": "guide11_c5_int_separability_v1",
        "run_root": str(RUN),
        "drift_tolerance": DRIFT_TOL,
        "rule": (
            "tier separable iff strip-Ray offset drift from the INT100 baseline "
            "stays within 0.01 on both log ratios and the strip frame is observable"
        ),
        "color_points": points,
        "overall_lowest_separable_int": min(all_lowest) if all_lowest else None,
        "int_separable": len(all_lowest) == len(points),
        "steady_claim": False,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"-> {OUT}")
    for p in points:
        print(f"H{p['hue']:>3}/S{p['sat']:>3}: separable tiers={p['separable_int_levels']} lowest={p['lowest_separable_int']}")
        for t in p["tiers"]:
            if t.get("status") != "complete":
                print(f"   i{t['int_percent']:>3}: {t['status']}")
                continue
            d = t.get("offset_drift_from_int100")
            dd = f"{d['log_R_over_G']:+.4f}/{d['log_B_over_G']:+.4f}" if d else "baseline"
            print(
                f"   i{t['int_percent']:>3}: zdist={t['z_distance_to_paired_ray']:.3f} drift={dd} "
                f"rayDrift={t.get('ray_own_drift_from_int100', 0):.3f} frame={t['frame_classification']} sep={t.get('separable')}"
            )


if __name__ == "__main__":
    main()
