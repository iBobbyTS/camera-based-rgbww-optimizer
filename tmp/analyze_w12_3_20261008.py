"""GUIDE12 W12-3 runtime interpolation holdout analysis (offline, frozen).

Reads the W12-3 holdout run root, recomputes white points with the shared W12
estimator chain (block_06 four-plane normalized-per-second trimmed means ->
camera neutral -> white point), and produces the per-request verdict:

- reference = paired Ray frame (cold requests use the mean of the
  raybefore/rayafter sandwich, with the W12 reference-compatibility drift
  gate; a tripped gate classifies the request reference_limited);
- signed errors e = strip - same-block Ray for cct_K / mired / duv and the
  frozen full-tolerance E = max(|e_K|/tau_K, |e_mired|/tau_mired,
  |e_Duv|/tau_Duv), gate E <= 1.0;
- per-request verdict qualified / exceeds_tolerance / reference_limited;
- node baseline (auxiliary, per GUIDE: only with a real signed baseline and
  a comparable estimator): nearest W12-2 verified_qualified node's signed
  errors, increment = request error - node error, with an explicit
  different-day caveat — never Ray-Ray=0;
- S0 session C z (HSI hue0/S0/INT100) joined against C12-1 sessions A/B.

Output: D:/rgbww-optimizer/guide12-w123/derived/w12-3-interpolation-analysis-20261008.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

ROOT = Path("D:/rgbww-optimizer/guide12-w123/formal-w123-holdout")
W122_ANALYSIS = Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-verification-analysis.json"
)
C12_MAPPING = Path(
    "D:/rgbww-optimizer/guide12-c12/derived/c12-1-mapping-20261005.json"
)
OUT = Path("D:/rgbww-optimizer/guide12-w123/derived/"
           "w12-3-interpolation-analysis-20261008.json")
TOL = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")

_MATRIX_CACHE: dict[str, object] = {}


def _planes_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    return {
        plane: float(
            block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"]
        )
        for plane in ("R", "G1", "G2", "B")
    }


def _matrix_for(root: Path, rows: list[dict], capture_id: str):
    raw_path = str(next(
        r for r in rows if str(r.get("capture_id")) == capture_id
    )["capture"]["saved_file"])
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(Path(raw_path), np)
    return _MATRIX_CACHE[raw_path]


def white_point_of(root: Path, rows: list[dict], capture_id: str) -> dict[str, float]:
    planes = _planes_of(root, capture_id)
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    est = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _matrix_for(root, rows, capture_id)
    )
    return {"cct_K": float(est["cct_K"]), "duv": float(est["duv"]),
            "mired": 1_000_000.0 / float(est["cct_K"])}


def z_of(root: Path, capture_id: str) -> tuple[float, float]:
    planes = _planes_of(root, capture_id)
    g = 0.5 * (planes["G1"] + planes["G2"])
    return (math.log(planes["R"] / g), math.log(planes["B"] / g))


def nearest_verified_node(request_cct: float, request_gm: float,
                          w122: dict) -> dict | None:
    """Nearest W12-2 verified_qualified node in (mired, gm)."""
    best = None
    for row in w122["node_summary"]:
        if row["verdict"] != "verified_qualified":
            continue
        cct, gm = (int(x) for x in row["node"].split("/"))
        d2 = ((1e6 / cct - 1e6 / request_cct) ** 2
              + (gm - request_gm) ** 2)
        if best is None or d2 < best[0]:
            best = (d2, row["node"])
    return {"node": best[1], "distance_sq_mired_gm": round(best[0], 2)} if best else None


def node_signed_mean(w122: dict, node: str) -> dict[str, float] | None:
    errs = [
        p["signed_errors"] for p in w122["node_pairs"]
        if p["node"] == node and p.get("pair_valid") and p.get("signed_errors")
    ]
    if not errs:
        return None
    return {c: float(np.mean([e[c] for e in errs])) for c in COMPONENTS}


def main() -> int:
    rows = [
        json.loads(line)
        for line in (ROOT / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    requests: dict[str, dict] = {}
    order: list[str] = []
    s0 = None
    for row in rows:
        step = row["plan_step"]
        quality = (row.get("capture", {}).get("direct_quality") or {}).get("status")
        if step.get("role") == "s0_reference":
            s0 = {
                "capture_id": str(row["capture_id"]),
                "quality": quality,
                "z": z_of(ROOT, str(row["capture_id"])),
            }
            continue
        key = str(step["w123_request"])
        entry = requests.setdefault(key, {})
        slot = str(step["w123_step"])
        entry[slot] = {
            "capture_id": str(row["capture_id"]),
            "quality": quality,
            "white_point": (
                white_point_of(ROOT, rows, str(row["capture_id"]))
                if quality in ("pass", "near_noise_only") else None
            ),
        }
        if step.get("w123_step") == "strip":
            entry["command"] = step.get("w123_interpolated_command")
        if key not in order:
            order.append(key)

    w122 = json.loads(W122_ANALYSIS.read_text(encoding="utf-8"))
    request_results = []
    for key in order:
        entry = requests[key]
        cct, gm = (int(x) for x in key.split("/"))
        steps = {k: v for k, v in entry.items() if k != "command"}
        ray_keys = [k for k in steps if k in ("ray", "raybefore", "rayafter")]
        ray_refs = [
            steps[k] for k in ray_keys
            if steps[k]["quality"] == "pass" and steps[k]["white_point"]
        ]
        strip = steps.get("strip")
        drift = None
        if "raybefore" in steps and "rayafter" in steps:
            b, a = steps["raybefore"], steps["rayafter"]
            if b["white_point"] and a["white_point"]:
                drift = {
                    c: a["white_point"][c] - b["white_point"][c]
                    for c in COMPONENTS
                }
        drift_within = (
            all(abs(drift[c]) <= TOL[c] for c in COMPONENTS) if drift else None
        )
        result = {
            "request": key,
            "command": entry.get("command"),
            "cold_sandwich": "raybefore" in steps,
            "cold_drift": drift,
            "cold_drift_within_tolerances": drift_within,
        }
        if strip and strip["white_point"] and ray_refs:
            reference = {
                c: float(np.mean([r["white_point"][c] for r in ray_refs]))
                for c in COMPONENTS
            }
            signed = {
                c: strip["white_point"][c] - reference[c] for c in COMPONENTS
            }
            e = max(abs(signed["cct_K"]) / TOL["cct_K"],
                    abs(signed["mired"]) / TOL["mired"],
                    abs(signed["duv"]) / TOL["duv"])
            if drift_within is False:
                verdict = "reference_limited(drift_gate)"
            elif e <= 1.0:
                verdict = "qualified"
            else:
                verdict = "exceeds_tolerance"
            result.update({
                "strip_white_point": strip["white_point"],
                "ray_white_point": reference,
                "signed_errors": {c: round(signed[c], 6) for c in COMPONENTS},
                "E_normalized": round(e, 4),
                "verdict": verdict,
            })
        else:
            result.update({"verdict": "unverified",
                           "reason": "missing valid ray/strip"})
        # auxiliary node baseline (real signed baseline, same estimator chain,
        # different day: comparability caveat per GUIDE W12-3)
        near = nearest_verified_node(cct, gm, w122)
        if near:
            base = node_signed_mean(w122, near["node"])
            if base and "signed_errors" in result:
                result["nearest_verified_node"] = near
                result["node_baseline_signed_errors"] = {
                    c: round(base[c], 6) for c in COMPONENTS}
                result["increment_over_node_baseline"] = {
                    c: round(result["signed_errors"][c] - base[c], 6)
                    for c in COMPONENTS}
                result["node_baseline_caveat"] = (
                    "different day/session, same frozen estimator chain; "
                    "increment is descriptive, not a separated pure "
                    "interpolation error")
        request_results.append(result)

    qualified = [r for r in request_results if r["verdict"] == "qualified"]
    print(f"W12-3 请求判定: qualified {len(qualified)}/{len(request_results)}")
    for r in request_results:
        cmd = r.get("command") or {}
        win = max(cmd, key=lambda k: cmd[k]) if cmd else "-"
        print(f"  {r['request']:11s} E={r.get('E_normalized')} "
              f"win={win} {r['verdict']}")
    e_all = [r["E_normalized"] for r in request_results if "E_normalized" in r]
    signed_all = {
        c: [r["signed_errors"][c] for r in request_results if "signed_errors" in r]
        for c in COMPONENTS
    }
    summary = {
        "qualified": len(qualified),
        "total_requests": len(request_results),
        "verdict_counts": {
            v: sum(1 for r in request_results if r["verdict"] == v)
            for v in {r["verdict"] for r in request_results}
        },
        "E_median": round(float(np.median(e_all)), 4) if e_all else None,
        "E_max": round(max(e_all), 4) if e_all else None,
        "signed_error_mean": {
            c: round(float(np.mean(v)), 6) for c, v in signed_all.items() if v},
        "signed_error_range": {
            c: [round(min(v), 6), round(max(v), 6)]
            for c, v in signed_all.items() if v},
    }
    print("summary:", json.dumps(summary, ensure_ascii=False))

    # S0 session C joined with C12-1 sessions A/B
    c12 = json.loads(C12_MAPPING.read_text(encoding="utf-8"))
    hue0_ab = c12["s0_hue_consistency"]["hue0"]
    s0_out = None
    if s0 and s0["quality"] == "pass":
        a, b, c = hue0_ab[0], hue0_ab[1], s0["z"]
        dz_ab = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        dz_ac = max(abs(a[0] - c[0]), abs(a[1] - c[1]))
        dz_bc = max(abs(b[0] - c[0]), abs(b[1] - c[1]))
        s0_out = {
            "session_c_z": [round(x, 6) for x in s0["z"]],
            "sessions_ab_z_hue0": hue0_ab,
            "dz_between_sessions": {
                "A-B": round(dz_ab, 6), "A-C": round(dz_ac, 6),
                "B-C": round(dz_bc, 6)},
            "capture_id": s0["capture_id"],
            "note": "HSI hue0/S0/INT100, same command as C12-1 sessions A/B",
        }
        print("S0 会话一致性 z:", json.dumps(s0_out, ensure_ascii=False))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema": "guide12_w12_3_interpolation_analysis_v1",
        "tolerances": TOL,
        "run_root": str(ROOT),
        "requests": request_results,
        "summary": summary,
        "s0_sessions": s0_out,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
