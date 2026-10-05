"""GUIDE12 N2 repeatability analysis (frozen, section 3.3).

Read-only analysis over the three certified N2 session roots:
- per-frame block_06 white points for the four white states (same estimator
  chain as the W12 analyzer: four-plane normalized-per-second trimmed means
  -> camera neutral -> white-point estimate),
- raw z vectors and full grouping saved verbatim,
- paired per-cycle differences d = strip - ray as the operational quantity,
- session-unit t intervals for the mean (design independent unit = session),
  iid-cycle t interval as secondary, PI for the next independent FAST paired
  operation, chi-square std conditional intervals, measured min/max,
- order effect (ray-first vs strip-first cycles) and per-session systematic
  offsets reported as independent effects, never merged into the variance,
- joint 95% region for the mean difference = pre-declared Bonferroni box over
  the three tolerance components (98.33% session-level t per component),
- burst-vs-anchor deltas (session 1 dwell bursts),
- color states: accepted-plane repeatability only, no white-point claims,
- 3200/0 cycles double as W12-2 independent-confirmation shares (E values).

No device, camera or network work. CR3s are read only for rgb_xyz matrices.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

TOLERANCES = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")
WHITE_STATES = ("white_1800_100", "white_3200_0", "white_5600_100", "white_20000_100")
COLOR_STATES = ("color_red", "color_blue")
MAIN_ROLES = ("paired_cycle_main", "burst_main")
EXTRA_ROLES = ("burst_extra_1", "burst_extra_2")
SESSION_ROOTS = {
    1: "D:/rgbww-optimizer/guide12-n2/formal-n2-session1-r5",
    2: "D:/rgbww-optimizer/guide12-n2/formal-n2-session2-r2",
    3: "D:/rgbww-optimizer/guide12-n2/formal-n2-session3",
}
BONF_T = {  # session-level t quantiles, two-sided
    0.9833: {2: 9.925},  # df=2 Bonferroni per-component 98.33%
    0.95: {2: 4.303, 5: 2.571},  # df=2 session / df=5 cycle
}
CHI2_975_DF = {2: 7.378, 5: 12.833}
CHI2_025_DF = {2: 0.0506, 5: 0.831}

_MATRIX_CACHE: dict[str, object] = {}


def load_rows(root: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def white_point_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw_path = str((next(
        r for r in load_rows(root) if str(r.get("capture_id")) == capture_id
    ).get("capture") or {}).get("saved_file", ""))
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            Path(raw_path), np
        )
    estimate = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path]
    )
    return {
        "cct_K": float(estimate["cct_K"]),
        "duv": float(estimate["duv"]),
        "mired": 1_000_000.0 / float(estimate["cct_K"]),
    }


def plane_levels(root: Path, capture_id: str) -> dict[str, dict]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    out = {}
    for plane, pv in block["planes"].items():
        quality = pv.get("quality", {})
        if quality.get("status") == "accepted":
            out[plane] = {
                "trimmed_mean": float(
                    pv["statistics"]["normalized_per_second"]["trimmed_mean"]
                )
            }
    return out


def t_quantile_two_sided(p: float, df: int) -> float:
    table = BONF_T.get(p) or {}
    if df in table:
        return table[df]
    raise KeyError(f"no frozen t quantile for p={p} df={df}")


def mean_interval(values: list[float], p: float, df_source: str) -> dict:
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    df = n - 1
    t = t_quantile_two_sided(p, df if df_source == "values" else 2)
    half = t * float(arr.std(ddof=1)) / math.sqrt(n)
    return {
        "mean": float(arr.mean()),
        "half_width": float(half),
        "low": float(arr.mean() - half),
        "high": float(arr.mean() + half),
        "n": n,
        "df": df if df_source == "values" else 2,
        "t": t,
    }


def std_conditional_interval(values: list[float]) -> dict:
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    df = n - 1
    s = float(arr.std(ddof=1))
    low = math.sqrt(df / CHI2_975_DF[df]) * s
    high = math.sqrt(df / CHI2_025_DF[df]) * s
    return {"s": s, "low": low, "high": high, "df": df}


def main() -> int:
    frames = []
    order_map: dict[tuple, str] = {}
    for session_index, root_s in sorted(SESSION_ROOTS.items()):
        root = Path(root_s)
        rows = load_rows(root)
        plan_order = [str(r["capture_id"]) for r in rows]
        for row in rows:
            step = row["plan_step"]
            state_key = str(step["n2_state_key"])
            cycle = int(step["n2_cycle_index"])
            source = str(step["source_id"])
            burst_role = step.get("n2_burst_role")
            capture_id = str(row["capture_id"])
            entry = {
                "session": session_index,
                "cycle": cycle,
                "state": state_key,
                "source": source,
                "burst_role": burst_role,
                "is_burst_extra": burst_role in EXTRA_ROLES,
                "capture_id": capture_id,
                "run_root": str(root),
                "recorded_shutter": (row["capture"].get("recorded_exposure") or {}).get(
                    "nominal_shutter_speed"
                ),
            }
            if state_key in WHITE_STATES:
                entry["white_point"] = white_point_of(root, capture_id)
            else:
                entry["planes"] = plane_levels(root, capture_id)
            frames.append(entry)
            if burst_role in MAIN_ROLES:
                group = (state_key, session_index, cycle)
                order_map.setdefault(
                    group, []
                ).append(plan_order.index(capture_id))
    # per (state, session, cycle): which source came first
    cycle_order = {}
    for (state_key, session_index, cycle), positions in order_map.items():
        rows_sorted = sorted(positions)
        first_source = None
        root = Path(SESSION_ROOTS[session_index])
        rows = load_rows(root)
        plan_ids = [str(r["capture_id"]) for r in rows]
        first_id = plan_ids[rows_sorted[0]]
        for row in rows:
            if str(row["capture_id"]) == first_id:
                first_source = str(row["plan_step"]["source_id"])
                break
        cycle_order[(state_key, session_index, cycle)] = first_source

    analysis: dict = {
        "schema": "guide12_n2_repeatability_analysis_v1",
        "created_for": "GUIDE12_N2_REPEATABILITY_V1, GUIDE 12.GUIDE.md section 3.3",
        "population_labels": {
            "commands": "frozen N2 six-state command table (design 2026-10-02)",
            "sources": "strip (bedroom-rgbww-strip PWM) vs ray (Ray120c reference)",
            "protocol": "FAST off600 -> command 120 -> capture, frozen shutters sha 9d1793...",
            "session_population": (
                "3 fully power-off separated sessions 2026-10-02..05, "
                ">=12h separation, generation-reset verified"
            ),
            "estimator": (
                "block_06 four-plane normalized_per_second trimmed mean -> "
                "camera neutral -> white-point estimate (W12 chain)"
            ),
            "tolerances": TOLERANCES,
            "joint_region_declaration": (
                "joint 95% mean region = pre-declared Bonferroni box, "
                "98.33% session-level (df=2) t interval per component; "
                "PI intervals are marginal 95%, not joint"
            ),
        },
        "frames": frames,
        "white_states": {},
        "color_states": {},
    }

    for state_key in WHITE_STATES:
        mains = [
            f for f in frames
            if f["state"] == state_key and not f["is_burst_extra"]
        ]
        z_table: dict[str, dict[str, dict[str, float]]] = {}
        for f in mains:
            z_table.setdefault(f["source"], {}).setdefault(
                f"session{f['session']}_cycle{f['cycle']}", {}
            )["z"] = f["white_point"]
        d_rows = []
        for session_index in (1, 2, 3):
            for cycle in (1, 2):
                ray = next(
                    (f for f in mains if f["session"] == session_index
                     and f["cycle"] == cycle and f["source"] == "ray"), None)
                strip = next(
                    (f for f in mains if f["session"] == session_index
                     and f["cycle"] == cycle and f["source"] == "strip"), None)
                if ray is None or strip is None:
                    continue
                d = {
                    c: strip["white_point"][c] - ray["white_point"][c]
                    for c in COMPONENTS
                }
                d_rows.append({
                    "session": session_index,
                    "cycle": cycle,
                    "first_source": cycle_order.get(
                        (state_key, session_index, cycle)),
                    "d": d,
                    "z_ray": ray["white_point"],
                    "z_strip": strip["white_point"],
                })
        comp_stats = {}
        for c in COMPONENTS:
            vals = [r["d"][c] for r in d_rows]
            session_means = [
                float(np.mean([r["d"][c] for r in d_rows if r["session"] == s]))
                for s in (1, 2, 3)
            ]
            ray_first = [r["d"][c] for r in d_rows if r["first_source"] == "ray"]
            strip_first = [r["d"][c] for r in d_rows if r["first_source"] == "strip"]
            comp_stats[c] = {
                "values": vals,
                "mean": float(np.mean(vals)),
                "min": float(np.min(vals)),
                "max": float(np.max(vals)),
                "session_means": session_means,
                "between_session_range": float(np.max(session_means) - np.min(session_means)),
                "within_session_cycle_spread": [
                    abs(r1 - r2) for r1, r2 in zip(
                        [r["d"][c] for r in d_rows if r["cycle"] == 1],
                        [r["d"][c] for r in d_rows if r["cycle"] == 2],
                    )
                ],
                "ci_mean_session_unit": mean_interval(session_means, 0.95, "session"),
                "ci_mean_iid_cycle": mean_interval(vals, 0.95, "values"),
                "pi_next_fast_operation_marginal95": {
                    **mean_interval(vals, 0.95, "values"),
                    "note": "mean +/- t*s*sqrt(1+1/n) is NOT applied; see pi_half_width",
                    "pi_half_width": float(
                        t_quantile_two_sided(0.95, 5)
                        * float(np.std(vals, ddof=1))
                        * math.sqrt(1 + 1 / len(vals))
                    ),
                },
                "std_conditional": std_conditional_interval(vals),
                "order_effect": {
                    "ray_first_mean": float(np.mean(ray_first)),
                    "strip_first_mean": float(np.mean(strip_first)),
                    "difference": float(np.mean(strip_first) - np.mean(ray_first)),
                    "note": "independent systematic effect, not merged into variance",
                },
                "bonferroni_component_interval_9833_session": mean_interval(
                    session_means, 0.9833, "session"),
            }
        joint = {
            c: comp_stats[c]["bonferroni_component_interval_9833_session"]
            for c in COMPONENTS
        }
        joint_within = all(
            joint[c]["low"] >= -TOLERANCES[c] and joint[c]["high"] <= TOLERANCES[c]
            for c in COMPONENTS
        )
        pi_within = all(
            comp_stats[c]["mean"]
            + comp_stats[c]["pi_next_fast_operation_marginal95"]["pi_half_width"]
            <= TOLERANCES[c]
            and comp_stats[c]["mean"]
            - comp_stats[c]["pi_next_fast_operation_marginal95"]["pi_half_width"]
            >= -TOLERANCES[c]
            for c in COMPONENTS
        )
        e_w12 = []
        for r in d_rows:
            e_w12.append(max(
                abs(r["d"]["cct_K"]) / TOLERANCES["cct_K"],
                abs(r["d"]["mired"]) / TOLERANCES["mired"],
                abs(r["d"]["duv"]) / TOLERANCES["duv"],
            ))
        analysis["white_states"][state_key] = {
            "z_by_source_session_cycle": z_table,
            "paired_differences": d_rows,
            "component_statistics": comp_stats,
            "joint95_mean_region_bonferroni": {
                "components": joint,
                "within_tolerances": joint_within,
            },
            "marginal95_pi_within_tolerances": pi_within,
            "w12_E_per_cycle": e_w12,
        }

    for state_key in COLOR_STATES:
        mains = [
            f for f in frames
            if f["state"] == state_key and not f["is_burst_extra"]
        ]
        plane_sets: dict[str, dict] = {}
        for f in mains:
            key = f"{f['source']}_s{f['session']}c{f['cycle']}"
            plane_sets[key] = f.get("planes", {})
        analysis["color_states"][state_key] = {
            "note": (
                "accepted-plane normalized_per_second trimmed means only; "
                "near-noise planes recorded, no white-point claims"
            ),
            "block06_planes_by_observation": plane_sets,
        }

    bursts = [f for f in frames if f["is_burst_extra"]]
    burst_report = []
    for f in bursts:
        anchor = next(
            (g for g in frames
             if g["state"] == f["state"] and g["source"] == f["source"]
             and g["session"] == f["session"] and g["cycle"] == f["cycle"]
             and not g["is_burst_extra"]), None)
        if anchor is None:
            continue
        if "white_point" in f and "white_point" in anchor:
            burst_report.append({
                "state": f["state"], "source": f["source"],
                "burst_role": f["burst_role"],
                "delta_vs_anchor": {
                    c: f["white_point"][c] - anchor["white_point"][c]
                    for c in COMPONENTS
                },
            })
    analysis["burst_deltas_vs_anchor"] = burst_report

    out = Path(
        "D:/rgbww-optimizer/guide12-n2/derived/n2-repeatability-analysis-20261005.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(analysis, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {out}")
    for state_key in WHITE_STATES:
        block = analysis["white_states"][state_key]
        line = [f"{state_key}:"]
        for c in COMPONENTS:
            s = block["component_statistics"][c]
            line.append(
                f"{c} d̄={s['mean']:+.4g} "
                f"CI(sess)[{s['ci_mean_session_unit']['low']:+.4g},"
                f"{s['ci_mean_session_unit']['high']:+.4g}] "
                f"PI(marg)[±{s['pi_next_fast_operation_marginal95']['pi_half_width']:.4g}]"
            )
        print(" | ".join(line))
        print(
            f"  joint95(Bonf) within tol: "
            f"{block['joint95_mean_region_bonferroni']['within_tolerances']} | "
            f"marginal-PI within tol: {block['marginal95_pi_within_tolerances']} | "
            f"W12-E per cycle: {[round(e,3) for e in block['w12_E_per_cycle']]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
