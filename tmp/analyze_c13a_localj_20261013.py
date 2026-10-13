"""GUIDE13 C13-A local-Jacobian scale analysis (offline, frozen).

For each of the three priority Ray neighborhoods: primary-layer z of all
seven frames, center bracket (before/after) drift, the J = [dz/dH,
dz/dS] columns from central differences over the measured +-2deg/+-2pp
neighbors (S100 target: one-sided S98/S96 secant below the center -
documented as such), column non-orthogonality and conditioning, the
(H+1/S+1) holdout linear-approximation residual, and monotonicity
diagnostics. Per GUIDE13 C13-A: nothing here assumes orthogonal columns,
and the local linear approximation is adopted only if the neighborhood
is stable/linear enough; otherwise the target is reported
map_unqualified with what was estimated.

No device access. All inputs are the frozen run artifacts.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide13  # noqa: E402

ROOT = Path("D:/rgbww-optimizer/guide13-c13a/formal-c13a-localj")
OUT = Path("D:/rgbww-optimizer/guide13-c13a/derived/"
           "c13a-local-jacobian-20261013.json")
TARGETS = (
    {"target": "0/50", "h": 0, "s": 50,
     "h_minus": (358, 50), "h_plus": (2, 50),
     "s_minus": (0, 48), "s_plus": (0, 52),
     "holdout": (1, 51), "s_secant": "central"},
    {"target": "300/50", "h": 300, "s": 50,
     "h_minus": (298, 50), "h_plus": (302, 50),
     "s_minus": (300, 48), "s_plus": (300, 52),
     "holdout": (301, 51), "s_secant": "central"},
    {"target": "60/100", "h": 60, "s": 100,
     "h_minus": (58, 100), "h_plus": (62, 100),
     "s_minus": (60, 96), "s_plus": (60, 98),
     "holdout": (61, 99), "s_secant": "one_sided_below_center"},
)
H_STEP_DEG = 2.0
S_STEP_PP = 2.0


def z_of(capture_id: str) -> tuple[float, float] | None:
    stats = json.loads(
        (ROOT / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    layer = guide13.primary_layer_from_stats(stats)
    if layer["primary_quality"] != "accepted":
        return None
    return guide13.z_from_planes(layer["planes_nps"])


def main() -> int:
    rows = [
        json.loads(line)
        for line in (ROOT / "captures.jsonl").read_text(encoding="utf-8")
        .splitlines() if line.strip()
    ]
    by_key: dict[tuple[str, int, int], dict] = {}
    for row in rows:
        step = row["plan_step"]
        key = (step["c13a_target"], step["c13a_role"],
               (int(step["c12_hue"]), int(step["c12_sat"])))
        by_key[key] = {"capture_id": str(row["capture_id"]),
                       "z": z_of(str(row["capture_id"]))}
    targets_out = []
    for spec in TARGETS:
        t = spec["target"]
        before = by_key[(t, "center_before", (spec["h"], spec["s"]))]
        after = by_key[(t, "center_after", (spec["h"], spec["s"]))]
        hm = by_key[(t, "neighbor", spec["h_minus"])]
        hp = by_key[(t, "neighbor", spec["h_plus"])]
        sm = by_key[(t, "neighbor", spec["s_minus"])]
        sp = by_key[(t, "neighbor", spec["s_plus"])]
        hold = by_key[(t, "holdout", spec["holdout"])]
        frames = {"center_before": before, "center_after": after,
                  "h_minus": hm, "h_plus": hp, "s_minus": sm, "s_plus": sp,
                  "holdout": hold}
        missing = [k for k, v in frames.items() if v["z"] is None]
        center = (
            tuple(0.5 * (before["z"][i] + after["z"][i]) for i in (0, 1))
            if not missing else None)
        drift = (
            tuple(after["z"][i] - before["z"][i] for i in (0, 1))
            if not missing else None)
        j_col_h = j_col_s = None
        holdout_pred = holdout_resid = None
        if not missing:
            j_col_h = tuple(
                (hp["z"][i] - hm["z"][i]) / (2 * H_STEP_DEG) for i in (0, 1))
            if spec["s_secant"] == "central":
                j_col_s = tuple(
                    (sp["z"][i] - sm["z"][i]) / (2 * S_STEP_PP) for i in (0, 1))
            else:
                # one-sided secant on S98/S96 (both below the S100 center)
                j_col_s = tuple(
                    (sp["z"][i] - sm["z"][i]) / (sp["z"][i] * 0 + S_STEP_PP)
                    for i in (0, 1))
            dh = spec["holdout"][0] - spec["h"]
            ds = spec["holdout"][1] - spec["s"]
            holdout_pred = tuple(
                center[i] + j_col_h[i] * dh + j_col_s[i] * ds for i in (0, 1))
            holdout_resid = tuple(
                hold["z"][i] - holdout_pred[i] for i in (0, 1))
        # non-orthogonality and conditioning of the true J
        cos_angle = cond = None
        if j_col_h and j_col_s:
            dot = j_col_h[0] * j_col_s[0] + j_col_h[1] * j_col_s[1]
            nh = math.hypot(*j_col_h)
            ns = math.hypot(*j_col_s)
            cos_angle = dot / (nh * ns) if nh > 0 and ns > 0 else None
            det = j_col_h[0] * j_col_s[1] - j_col_h[1] * j_col_s[0]
            cond = (nh * ns) / abs(det) if det else None
        # S-direction monotonicity (three points on the S axis)
        s_monotone = None
        if not missing and spec["s_secant"] == "one_sided_below_center":
            s_monotone = all(
                (sm["z"][i] - sp["z"][i]) * (sp["z"][i] - center[i]) >= 0
                for i in (0, 1))
        targets_out.append({
            "target": t,
            "frames": {k: {"capture_id": v["capture_id"], "z": v["z"]}
                       for k, v in frames.items()},
            "center_mean": center,
            "center_drift_after_minus_before": drift,
            "J_columns": {
                "dz_per_deg_H": j_col_h,
                "dz_per_pp_S": j_col_s,
                "s_secant_kind": spec["s_secant"],
                "units": {"H": "degree", "S": "percentage_point"},
            },
            "column_non_orthogonality_cos": cos_angle,
            "condition_number_2x2": cond,
            "holdout_linear_check": {
                "request": spec["holdout"],
                "predicted_z": holdout_pred,
                "measured_z": hold["z"] if hold["z"] else None,
                "residual": holdout_resid,
            },
            "s_axis_monotone": s_monotone,
            "primary_invalid_frames": missing,
            "uncertainty_note": (
                "single observation per coordinate; frame-to-frame noise is "
                "not separable from the center drift bracket - the reported "
                "drift bounds the reference movement over the block, and "
                "column uncertainties are drift-limited estimates, not "
                "sampling variances"),
        })
    artifact = {
        "schema": "guide13_c13a_local_jacobian_v1",
        "run_root": str(ROOT),
        "targets": targets_out,
        "jacobian_rule": (
            "J = [dz/dH, dz/dS], columns from measured Ray central "
            "differences (S100: one-sided S98/S96 secant); non-orthogonal "
            "by construction; no 90-degree rotation anywhere"),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    for t in targets_out:
        j = t["J_columns"]
        print(f"== {t['target']} ==")
        if j["dz_per_deg_H"] is None:
            print("  primary-invalid frames:", t["primary_invalid_frames"])
            continue
        print(f"  center {['%.6f' % v for v in t['center_mean']]}")
        print(f"  drift  {['%.6f' % v for v in t['center_drift_after_minus_before']]}")
        print(f"  dH col {['%.6f' % v for v in j['dz_per_deg_H']]} /deg")
        print(f"  dS col {['%.6f' % v for v in j['dz_per_pp_S']]} /pp "
              f"({j['s_secant_kind']})")
        print(f"  cos(cols)={t['column_non_orthogonality_cos']:.4f} "
              f"cond={t['condition_number_2x2']:.2f}")
        h = t["holdout_linear_check"]
        print(f"  holdout resid {['%.6f' % v for v in h['residual']]}")
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
