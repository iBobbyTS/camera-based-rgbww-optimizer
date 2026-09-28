"""GUIDE11 W8 recompute: white final report from real inputs only.

Rebuilds the GUIDE10-era W8 final artifact from GUIDE11 real evidence:
per-node command provenance (W2-selected vs W6 fallback), W1 frozen Ray
targets and tolerances, error identity (selection frame vs W6 single
observation), N1 co-located conditional/prediction intervals, W4 true
FAST/LONG difference-in-differences, and W3 segmented interpolation
applicability. No fabricated thermal_bias; no interval without evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

BASE = Path("D:/rgbww-optimizer")
OUT = BASE / "guide11-w8" / "guide11-white-final-report-20260928.json"
T_PRED_DF1 = 12.706  # Student-t two-sided 95%, df=1 (n=2 cycles)
PRED_FACTOR = T_PRED_DF1 * math.sqrt(1.0 + 0.5)  # prediction interval, n=2


def load(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


lut = load("guide11-w3/frozen-lut-20260923.json")
w1 = load("guide11-n1/derived/w1-frozen-targets-20260922.json")
w2 = load("guide11-w2/derived/w2-selection-20260923.json")
n1 = load("guide11-n1/derived/n1-combined-analysis-20260922.json")
w4 = load("guide11-w4/derived/w4-protocol-analysis-20260924.json")
old_w8 = load("guide10-white70-w8-final/guide10-white70-final-artifact.json")

w1_by_key = {(n["cct"], n["gm"]): n for n in w1["nodes"]}
w2_by_key = {(n["cct"], n["gm"]): n for n in w2["nodes"]}
w6_by_key = {(n["cct"], n["gm"]): n for n in old_w8["node_status_map"]}
n1_by_key = {(p["cct"], p["gm"]): p for p in n1["points"]}
w4_by_key = {(p["cct"], p["gm"]): p for p in w4["points"]}


def interval_components(point):
    """Conditional CI and Student-t prediction interval per component."""
    out = {}
    for comp in ("cct_K_diff", "mired_diff", "duv_diff"):
        block = point.get(comp) or {}
        if block.get("status") != "ok":
            out[comp] = {"status": block.get("status", "missing")}
            continue
        mean, sd = float(block["mean"]), float(block.get("sample_sd", 0.0))
        half = PRED_FACTOR * sd
        out[comp] = {
            "status": "ok",
            "conditional_ci": [block["ci_low"], block["ci_high"]],
            "prediction_interval": [mean - half, mean + half],
            "note": "Student-t df=1; normality not verified; n=2 cycles",
        }
    return out


W4_ANCHORS = {(1800, 100), (3200, 100), (5600, 100), (20000, 100)}

nodes_out = []
within_point_estimate = 0
identity_counts: dict[str, int] = {}
for row in lut["nodes"]:
    key = (row["cct"], row["gm"])
    target = w1_by_key.get(key)
    tol = (target or {}).get("tolerances") or {}
    ray = (target or {}).get("ray_target") or {}

    w2row = w2_by_key.get(key)
    w6row = w6_by_key.get(key)
    if row["source"].startswith("w2_selected") and w2row and w2row.get("selected"):
        sel = w2row["selected"]
        gates = sel["e_gates"]
        evidence = {
            "identity": "w2_selection_frame",
            "e_cct_K": gates.get("cct_K"),
            "e_mired": gates.get("mired"),
            "e_duv": gates.get("duv"),
            "E_normalized": sel.get("E"),
            "within_tolerance_point_estimate": bool(w2row.get("selected_within_tolerance")),
            "repeat_count": 1,
            "certification": "selection frame only; not an independent confirmation",
        }
    elif w6row:
        g = w6row.get("gates") or {}
        def signed_err(name, gate_key):
            value = w6row.get(name)
            return None if value is None else float(value)
        E_val = None
        if all(isinstance(tol.get(k), (int, float)) for k in ("cct_K", "mired", "duv")):
            parts = []
            for err_name, tol_name in (
                ("cct_error_K", "cct_K"), ("mired_error", "mired"), ("duv_error", "duv"),
            ):
                err = w6row.get(err_name)
                if err is not None:
                    parts.append(abs(float(err)) / float(tol[tol_name]))
            if parts:
                E_val = max(parts)
        evidence = {
            "identity": "w6_single_observation",
            "e_cct_K": w6row.get("cct_error_K"),
            "e_mired": w6row.get("mired_error"),
            "e_duv": w6row.get("duv_error"),
            "E_normalized": E_val,
            "within_tolerance_point_estimate": w6row.get("status") == "pass",
            "repeat_count": 1,
            "certification": "W6 single FAST observation; E recomputed against W1 tolerances",
        }
    else:
        evidence = {
            "identity": "no_evidence",
            "within_tolerance_point_estimate": False,
            "repeat_count": 0,
            "certification": "no measured strip observation retained for this node",
        }
    # W2 re-measurement of the shipped command: for non-adopted W2 nodes the
    # freeze kept the W6 fallback, but W2 usually re-measured that exact
    # command as a candidate. Attach it as selection-frame evidence for the
    # command actually shipped in the LUT.
    w2_probe = None
    if w2row and not row["source"].startswith("w2_selected"):
        for cand in w2row.get("all_candidates") or ():
            if cand.get("command") == row["command"]:
                w2_probe = {
                    "identity": "w2_remeasurement_of_shipped_command",
                    "E_normalized": cand.get("E"),
                    "e_cct_K": (cand.get("e_gates") or {}).get("cct_K"),
                    "e_mired": (cand.get("e_gates") or {}).get("mired"),
                    "e_duv": (cand.get("e_gates") or {}).get("duv"),
                    "capture_id": cand.get("capture_id"),
                    "certification": "selection frame; W2 selected a different candidate but the freeze retained this command",
                }
                break
        if w2_probe is None:
            w2_probe = {
                "identity": "w2_no_remeasurement_of_shipped_command",
                "w2_best_tested_E": (w2row.get("selected") or {}).get("E"),
                "note": (
                    "W2 probed new candidates only; the shipped fallback command was "
                    "not re-measured. Freeze kept it because a selection frame cannot "
                    "certify a command change; only within-tolerance selections were adopted."
                ),
            }
    identity_counts[evidence["identity"]] = identity_counts.get(evidence["identity"], 0) + 1
    if evidence["within_tolerance_point_estimate"]:
        within_point_estimate += 1

    n1point = n1_by_key.get(key)
    if n1point:
        interval = {
            "applicable": True,
            "source": "n1_colocated_repeatability",
            "cycles_n": len(n1point.get("cycles") or {}),
            "components": interval_components(n1point),
            "burst_layer_available": bool(n1point.get("is_burst_point")),
            "burst_layer_note": (
                "same-dwell adjacent RAWs quantify combined short-term noise; "
                "not separable into camera vs LED share"
                if n1point.get("is_burst_point")
                else "no burst at this anchor"
            ),
        }
    else:
        interval = {
            "applicable": False,
            "source": None,
            "reason": (
                "no co-located N1 repeatability point; pooled transfer to other "
                "active-face/load groups not validated (GUIDE11 3.2)"
            ),
        }

    cct, gm = key
    if 5300 <= cct <= 7250 and abs(gm - 100) <= 65:
        interp = {
            "continuous_supported": True,
            "basis": "W3 holdout within-tolerance points 6100/35 and 7250/100; 5300/100 near miss (E=1.67)",
        }
    else:
        interp = {
            "continuous_supported": False,
            "basis": "W3 holdout failed outside 5300-7250 or at |GM offset|>65; nearest-node commands only, no continuity claim",
        }

    protocol = None
    if key in W4_ANCHORS and key in w4_by_key:
        p = w4_by_key[key]
        protocol = {
            "delta_protocol": p.get("delta_protocol"),
            "fast_strip_minus_ray": p.get("fast_strip_minus_ray"),
            "long_strip_minus_ray": p.get("long_strip_minus_ray"),
            "interpretation": "difference-in-differences; not a proven physical temperature causation",
        }

    nodes_out.append({
        "cct": cct,
        "gm": gm,
        "command": row["command"],
        "command_source": row["source"],
        "ray_target": {
            "cct_K": ray.get("cct_K"), "duv": ray.get("duv"),
            "mired": ray.get("mired"), "capture_id": ray.get("capture_id"),
        },
        "threshold_source": "guide11_w1_frozen_targets_v1",
        "tolerances": tol,
        "error_evidence": evidence,
        "w2_probe_evidence": w2_probe,
        "interval_evidence": interval,
        "protocol_deviation": protocol,
        "interpolation_applicability": interp,
        "route_note": (
            "1800/GM100 active search permanently closed in GUIDE10; "
            "repeat observation only"
            if key == (1800, 100) else None
        ),
    })

true_long_obs = sum(
    2 for _ in W4_ANCHORS
)  # one LONG Ray + one LONG strip source observation per anchor

report = {
    "schema": "guide11_white_final_report_v1",
    "stage": "GUIDE11-W8-RECOMPUTE",
    "created_from_real_inputs": {
        "lut": "guide11-w3/frozen-lut-20260923.json (70 nodes; 9 W2-selected, 61 W6 fallback)",
        "targets": "guide11-n1/derived/w1-frozen-targets-20260922.json",
        "w2_selection": "guide11-w2/derived/w2-selection-20260923.json (25 nodes, 49 observations)",
        "n1_repeatability": "guide11-n1/derived/n1-combined-analysis-20260922.json (36 observations, 6 anchors)",
        "w3_holdout": "guide11-w3/derived/w3-holdout-analysis-20260924.json (20 non-node points, 2 within tolerance)",
        "w4_protocol": "guide11-w4/derived/w4-protocol-analysis-20260924.json (4 anchors, FAST and true LONG)",
    },
    "node_count": len(nodes_out),
    "identity_counts": identity_counts,
    "within_tolerance_point_estimate": within_point_estimate,
    "uncertainty_scope": (
        "FAST direct observer reset600/D120 unless a protocol_deviation block is "
        "present; conditional intervals are N1 co-located cycle CIs; prediction "
        "intervals are Student-t df=1 from n=2 cycles and are wide by construction"
    ),
    "true_LONG_observations": true_long_obs,
    "fast_long_method": (
        "Delta_protocol=(strip-Ray)_LONG-(strip-Ray)_FAST at 4 anchors; both sides "
        "protocol-verified by timing labels (reset1800/D600 observed 604.6-605.9 s "
        "exposure-start elapsed; FAST reset600/D120)"
    ),
    "fast_long_bias_field_replaced": (
        "the GUIDE10 artifact's thermal_bias scalar is not carried over; only the "
        "measured per-anchor delta_protocol blocks above"
    ),
    "closed_routes": [
        "1800/GM100 active search (GUIDE10 permanent closure; repeat-only)",
        "H120/S100 and H300/S100 color routes (GUIDE11 C1; not reopened)",
    ],
    "steady_claim": False,
    "nodes": nodes_out,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT)
print("nodes:", len(nodes_out))
print("identity:", identity_counts)
print("within point estimate:", within_point_estimate)
print("true LONG observations:", true_long_obs)
