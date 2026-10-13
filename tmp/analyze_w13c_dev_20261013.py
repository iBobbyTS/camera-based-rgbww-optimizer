"""GUIDE13 W13-C dev-regression analysis (offline, frozen).

Recomputes, for each of the six corrected-interpolation requests, the
strip white point minus the local Ray white point (raybefore/rayafter
mean for the cold 17500/30 sandwich, the single ray frame otherwise),
with the same white-point chain the W12-2/W12-3 analyzers used: block_06
four native planes -> camera neutral -> estimate_white_point_from_
camera_neutral with the frame's rawpy rgb_xyz_matrix. Signed (K, mired,
Duv), tolerances E = max(|eK|/25, |emired|/1, |eDuv|/0.0005).

Development-regression semantics only: these six coordinates were the
old W12-3 requests, evaluated here against the corrected runtime
function; the 20 new holdouts are a separate later arm.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide12  # noqa: E402
from camera_based_rgbww_optimizer.optimization import (  # noqa: E402
    white_calibration_common as common,
)

ROOT = Path("D:/rgbww-optimizer/guide13-w13c/formal-w13c-dev")
OUT = Path("D:/rgbww-optimizer/guide13-w13c/derived/"
           "w13c-dev-regression-20261013.json")
TOL = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")
COLD_REQUEST = "17500/30"

_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (ROOT / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]
                     ["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    physical = {
        str(json.loads(line)["capture_id"]): json.loads(line)
        for line in (ROOT / "physical-returns.jsonl")
        .read_text(encoding="utf-8").splitlines() if line.strip()
    }
    raw_path = str(physical[capture_id]["cr3_path"])
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            Path(raw_path), np)
    est = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path])
    return {"cct_K": float(est["cct_K"]), "duv": float(est["duv"]),
            "mired": 1_000_000.0 / float(est["cct_K"])}


def main() -> int:
    rows = [
        json.loads(line)
        for line in (ROOT / "captures.jsonl").read_text(encoding="utf-8")
        .splitlines() if line.strip()
    ]
    by_request: dict[str, dict[str, dict]] = {}
    quality: dict[str, str | None] = {}
    for row in rows:
        step = row["plan_step"]
        request = step["w13c_request"]
        role = "ray" if step["w13c_step"] in ("ray", "raybefore", "rayafter") \
            else "strip"
        slot = step["w13c_step"] if role == "strip" else "ref"
        by_request.setdefault(request, {}).setdefault(slot, []).append({
            "capture_id": str(row["capture_id"]),
            "step": step["w13c_step"],
            "quality": ((row.get("capture") or {}).get("direct_quality")
                        or {}).get("status"),
            "white_point": white_point_of(str(row["capture_id"])),
        })
    # Node-bias baseline: the corrected-weight blend of the bracketing
    # nodes' own W12-2 signed errors predicts what the dev arm should
    # observe if the interpolation merely inherits node bias (GUIDE13:
    # look at node baselines before declaring the bilinear method dead).
    node_err: dict[str, dict[str, float]] = {}
    verification = json.loads(Path(
        "D:/rgbww-optimizer/guide12-w122/derived/"
        "w12-2-verification-analysis.json").read_text(encoding="utf-8"))
    for pair in verification["node_pairs"]:
        if pair.get("E_normalized") is not None:
            node_err[pair["node"]] = pair["signed_errors"]
    lut_nodes = json.loads(Path(
        "D:/rgbww-optimizer/guide12-w122/derived/"
        "w12-2-frozen-lut-20261005.json").read_text(encoding="utf-8")
    )["nodes"]

    def node_bias_prediction(cct: int, gm: int) -> dict[str, float | None]:
        weights = {}
        try:
            from camera_based_rgbww_optimizer.optimization.guide13_w13c \
                import _corrected_weights
            weights = _corrected_weights(lut_nodes, cct, gm)
        except ValueError:
            return {c: None for c in COMPONENTS}
        out: dict[str, float | None] = {c: 0.0 for c in COMPONENTS}
        for (ncct, ngm), w in weights.items():
            err = node_err.get(f"{ncct}/{ngm}")
            if err is None:
                return {c: None for c in COMPONENTS}
            for c in COMPONENTS:
                out[c] += w * float(err[c])
        return out

    requests_out = []
    for request, slots in by_request.items():
        strip = slots["strip"][0]
        refs = slots.get("ref", [])
        if request == COLD_REQUEST:
            reference = {
                c: float(np.mean([r["white_point"][c] for r in refs]))
                for c in COMPONENTS
            }
            ref_note = "mean(raybefore, rayafter)"
            ray_drift = {
                c: refs[1]["white_point"][c] - refs[0]["white_point"][c]
                for c in COMPONENTS
            } if len(refs) == 2 else None
        else:
            reference = refs[0]["white_point"]
            ref_note = "single ray frame"
            ray_drift = None
        signed = {
            c: strip["white_point"][c] - reference[c] for c in COMPONENTS}
        e = max(abs(signed["cct_K"]) / TOL["cct_K"],
                abs(signed["mired"]) / TOL["mired"],
                abs(signed["duv"]) / TOL["duv"])
        cct, gm = (int(x) for x in request.split("/"))
        prediction = node_bias_prediction(cct, gm)
        unexplained = (
            {c: signed[c] - prediction[c] for c in COMPONENTS}
            if prediction["cct_K"] is not None else None)
        requests_out.append({
            "request": request,
            "strip_capture_id": strip["capture_id"],
            "reference_capture_ids": [r["capture_id"] for r in refs],
            "reference_note": ref_note,
            "ray_reference_drift": ray_drift,
            "strip_white_point": strip["white_point"],
            "reference_white_point": reference,
            "signed_errors": signed,
            "node_bias_prediction": prediction,
            "unexplained_error": unexplained,
            "E_normalized": e,
            "E_within_gate": e <= 1.0,
            "qualities": {
                "strip": strip["quality"],
                "refs": [r["quality"] for r in refs],
            },
            "corrected_command": next(
                r["plan_step"] for r in rows
                if r["plan_step"].get("w13c_request") == request
                and r["plan_step"]["w13c_step"] == "strip"
            )["w13c_corrected_command"],
        })
    artifact = {
        "schema": "guide13_w13c_dev_regression_v1",
        "tolerances": TOL,
        "run_root": str(ROOT),
        "role": "development regression of the corrected interpolation; "
                "not independent holdouts",
        "requests": requests_out,
        "summary": {
            "requests": len(requests_out),
            "E_within_gate": sum(1 for r in requests_out
                                 if r["E_within_gate"]),
            "E_values": {r["request"]: round(r["E_normalized"], 4)
                         for r in requests_out},
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"{'request':>9s} {'E':>8s} gate  {'eK':>10s} {'emired':>9s} "
          f"{'eDuv':>12s} | {'predK':>9s} {'unexpK':>9s} {'unexpMir':>9s}")
    for r in requests_out:
        s = r["signed_errors"]
        p = r["node_bias_prediction"]
        u = r["unexplained_error"] or {}
        print(f"{r['request']:>9s} {r['E_normalized']:8.3f} "
              f"{'PASS' if r['E_within_gate'] else 'FAIL':>4s} "
              f"{s['cct_K']:10.3f} {s['mired']:9.4f} {s['duv']:12.3e} | "
              f"{(p['cct_K'] if p['cct_K'] is not None else float('nan')):9.2f} "
              f"{u.get('cct_K', float('nan')):9.2f} "
              f"{u.get('mired', float('nan')):9.4f}")
    cold = next(r for r in requests_out if r["request"] == COLD_REQUEST)
    print("17500/30 ray drift (after-before):", cold["ray_reference_drift"])
    print("within gate:", artifact["summary"]["E_within_gate"], "/",
          len(requests_out))
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
