"""GUIDE12 C12-1 true-mapping fit and inverse validation (frozen).

Stages:
1. assemble current-era Ray z observations (z = log R/Gmean, log B/Gmean,
   block_06 four planes, normalized-per-second trimmed means):
   C1 anchors, C4 targets, N2 H0/H240 repeats, C12-1 training roles;
   holdouts (C12-1 role=holdout) stay untouched until the final verdict;
2. compute P6 node z the same way and run the required historical->current
   transfer test at shared coordinates (accept within combined noise);
3. fit periodic-hue x nonlinear-SAT models (harmonic order, SAT degree),
   weighted least squares, complexity chosen by leave-one-out on training
   (never on holdouts);
4. invert each holdout z: local minima (multi-solution), local Jacobian,
   singular values, label errors, joint (H,S) regions from propagated
   measurement+model uncertainty; verdict vs the 0.5deg/0.5pp budget with
   confidence upper bounds (95% empirical quantile of holdout errors);
5. S0 hue-consistency check (hue 0 vs hue 240 at S0).

Output: D:/rgbww-optimizer/guide12-c12/derived/c12-1-mapping-20261005.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

OUT = Path("D:/rgbww-optimizer/guide12-c12/derived/c12-1-mapping-20261005.json")
C12_RUN = Path("D:/rgbww-optimizer/guide12-c12/formal-c12-1-ray-grid")
N2_ANALYSIS = Path(
    "D:/rgbww-optimizer/guide12-n2/derived/n2-repeatability-analysis-20261005.json"
)
C1_ANCHORS = Path(
    "D:/rgbww-optimizer/guide11/guide11-c1/derived/c3-anchor-self-check-20260925.json"
)
C4_ANALYSIS = Path(
    "D:/rgbww-optimizer/guide11/guide11-c4/derived/c4-holdout-analysis-20260928.json"
)
P6_RUN = Path(
    "D:/rgbww-optimizer/foundations/ray-hsi-manifold/p6-ray-hsi-remote-20260717-0403-retry1"
)
BUDGET = {"hue_deg": 0.5, "sat_pp": 0.5}


def z_from_patch_file(path: Path) -> tuple[float, float] | None:
    d = json.loads(path.read_text(encoding="utf-8"))
    block = next((p for p in d["patches"] if p.get("index") == 6), None)
    if block is None:
        return None
    planes = {}
    for plane in ("R", "G1", "G2", "B"):
        pv = block["planes"].get(plane)
        if pv is None or pv.get("quality", {}).get("status") != "accepted":
            return None
        planes[plane] = float(
            pv["statistics"]["normalized_per_second"]["trimmed_mean"]
        )
    g = 0.5 * (planes["G1"] + planes["G2"])
    if min(planes.values()) <= 0 or g <= 0:
        return None
    return math.log(planes["R"] / g), math.log(planes["B"] / g)


def assemble() -> dict:
    records = []
    # C1 anchors (training; z_mean given directly)
    anchors = json.loads(C1_ANCHORS.read_text(encoding="utf-8"))
    for a in anchors["grid"]:
        # the C1 "SAT0" row is a CCT-average white approximation, which
        # GUIDE C12-1 explicitly prohibits as an SAT0 stand-in; the true
        # HSI S0 comes from the C12-1 S0 frames (hue 0 and hue 240 agree
        # to |dz|~0.001)
        if a.get("sat") == 0:
            continue
        else:
            records.append({
                "hue": float(a["hue"]), "sat": float(a["sat"]),
                "z": [a["z_mean"]["log_R_over_G"], a["z_mean"]["log_B_over_G"]],
                "n": a.get("n", 2), "tag": f"c1_h{a['hue']}s{a['sat']}",
                "role": "train",
            })
    # C4 targets (training: fresh Ray observations of the old menu grid)
    c4 = json.loads(C4_ANALYSIS.read_text(encoding="utf-8"))
    for t in c4["targets"]:
        records.append({
            "hue": float(t["hue"]), "sat": float(t["sat"]),
            "z": [t["ray_z_mean"]["log_R_over_G"], t["ray_z_mean"]["log_B_over_G"]],
            "n": 1, "tag": f"c4_h{t['hue']}s{t['sat']}", "role": "train",
        })
    # N2 H0/H240 repeats (training, 6 sessions-cycles each)
    n2 = json.loads(N2_ANALYSIS.read_text(encoding="utf-8"))
    for state_key in ("color_red", "color_blue"):
        planes_by_obs = n2["color_states"][state_key]["block06_planes_by_observation"]
        for obs_key, planes in planes_by_obs.items():
            # only Ray observations enter the Ray mapping (strip frames of
            # color_blue carry all four accepted planes but a very
            # different z and would contaminate the fit)
            if not obs_key.startswith("ray_"):
                continue
            if not all(p in planes for p in ("R", "G1", "G2", "B")):
                continue
            g = 0.5 * (planes["G1"]["trimmed_mean"] + planes["G2"]["trimmed_mean"])
            hue = 0.0 if state_key == "color_red" else 240.0
            records.append({
                "hue": hue, "sat": 100.0,
                "z": [math.log(planes["R"]["trimmed_mean"] / g),
                      math.log(planes["B"]["trimmed_mean"] / g)],
                "n": 1, "tag": f"n2_{state_key}_{obs_key}", "role": "train",
            })
    # C12-1 grid: holdouts vs training roles
    rows = [
        json.loads(line)
        for line in (C12_RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for row in rows:
        step = row["plan_step"]
        z = z_from_patch_file(
            C12_RUN / "measurements" / f"{row['capture_id']}.patch-statistics.json"
        )
        if z is None:
            continue
        records.append({
            "hue": float(step["c12_hue"]), "sat": float(step["c12_sat"]),
            "z": list(z), "n": 1,
            "tag": f"c12_{step['c12_role']}_h{step['c12_hue']}s{step['c12_sat']}",
            "role": "holdout" if step["c12_role"] == "holdout" else "train",
        })
    return {"records": records}


def p6_nodes() -> list[dict]:
    plan = json.loads((P6_RUN / "plan.json").read_text(encoding="utf-8"))
    out = []
    for c in plan["captures"]:
        if c.get("ray_mode") != "hsi":
            continue
        ac = c["analysis_context"]
        if ac.get("sat", 0) == 0:
            continue
        z = z_from_patch_file(
            P6_RUN / "measurements" / f"{c['capture_id']}.patch-statistics.json"
        )
        if z is None:
            continue
        out.append({"hue": float(ac["hue"]), "sat": float(ac["sat"]),
                    "z": list(z), "tag": f"p6_h{ac['hue']}s{ac['sat']}"})
    return out


def circular_dist(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0)


def fit_model(records: list[dict], *, harmonics: int, sat_degree: int,
              use_p6: list[dict] | None = None, hold_out_tag: str | None = None):
    """Weighted LS for z(h,s); returns (params, predict, info)."""
    data = [r for r in records if r["role"] == "train" and r["tag"] != hold_out_tag]
    pool = data + (use_p6 or [])

    def basis(h: float, s: float) -> list[float]:
        cols = [1.0]  # white/SAT0 anchor term
        for k in range(1, harmonics + 1):
            for trig in (math.cos, math.sin):
                for d in range(1, sat_degree + 1):
                    cols.append(trig(k * math.radians(h)) * (s / 100.0) ** d)
        return cols

    X = np.array([basis(r["hue"], r["sat"]) for r in pool])
    w = np.sqrt([max(r.get("n", 1), 1) for r in pool])
    params = {}
    for comp in (0, 1):
        y = np.array([r["z"][comp] for r in pool])
        A = X * w[:, None]
        b = y * w
        beta, *_ = np.linalg.lstsq(A, b, rcond=None)
        params[comp] = beta

    def predict(h: float, s: float) -> tuple[float, float]:
        b = np.array(basis(h, s))
        return float(b @ params[0]), float(b @ params[1])

    resid = [
        math.hypot(*(np.array(predict(r["hue"], r["sat"])) - np.array(r["z"])))
        for r in data
    ]
    info = {
        "harmonics": harmonics, "sat_degree": sat_degree,
        "n_train_current": len(data), "n_p6": len(use_p6 or []),
        "train_rms_resid": float(np.sqrt(np.mean(np.square(resid)))),
        "train_max_resid": float(np.max(resid)),
        "param_count": len(params[0]),
    }
    return params, predict, info, basis


def loo_cv(records: list[dict], *, harmonics: int, sat_degree: int,
           use_p6: list[dict] | None) -> float:
    errs = []
    for r in [x for x in records if x["role"] == "train"]:
        _, predict, _, _ = fit_model(
            records, harmonics=harmonics, sat_degree=sat_degree,
            use_p6=use_p6, hold_out_tag=r["tag"],
        )
        errs.append(math.hypot(
            *(np.array(predict(r["hue"], r["sat"])) - np.array(r["z"]))))
    return float(np.sqrt(np.mean(np.square(errs))))


def fit_idw(records: list[dict], *, k: int, hold_out_tag: str | None = None):
    """Piecewise local model: k-nearest-node IDW in the scaled circular
    (hue, SAT) metric (GUIDE C12-1 permits piecewise models; selection is
    by independent label error, not fit residual)."""
    pts = [
        r for r in records
        if r["role"] == "train" and r["tag"] != hold_out_tag
    ]
    hues = np.array([r["hue"] for r in pts])
    sats = np.array([r["sat"] for r in pts])
    zs = np.array([r["z"] for r in pts])

    def dist(h, s):
        dh = np.abs(((h - hues + 180.0) % 360.0) - 180.0) / 30.0
        return np.sqrt(dh ** 2 + ((s - sats) / 25.0) ** 2)

    def predict(h: float, s: float) -> tuple[float, float]:
        d = dist(h, s)
        idx = np.argsort(d)[:k]
        w = 1.0 / np.maximum(d[idx], 1e-6) ** 2
        z = (w[:, None] * zs[idx]).sum(axis=0) / w.sum()
        return float(z[0]), float(z[1])

    def loo_err(r: dict) -> float:
        p2, _, _ = fit_idw(records, k=k, hold_out_tag=r["tag"])
        return math.hypot(*(np.array(p2(r["hue"], r["sat"])) - np.array(r["z"])))

    return predict, {"method": "idw", "k": k, "n_nodes": len(pts)}, loo_err


def invert(predict, z: tuple[float, float]) -> dict:
    zx, zy = z
    hue_steps = [i * 0.5 for i in range(720)]
    sat_steps = [j * 0.5 for j in range(201)]
    grid = [
        [math.hypot(predict(h, s)[0] - zx, predict(h, s)[1] - zy)
         for s in sat_steps]
        for h in hue_steps
    ]
    minima = []
    for i in range(len(hue_steps)):
        for j in range(len(sat_steps)):
            d = grid[i][j]
            neigh = []
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < len(hue_steps) and 0 <= jj < len(sat_steps):
                    neigh.append(grid[ii][jj])
            if neigh and all(d <= v for v in neigh):
                minima.append((hue_steps[i], sat_steps[j], d))
    minima.sort(key=lambda m: m[2])
    merged = []
    for m in minima:
        if all(circular_dist(m[0], k[0]) > 3.0 or abs(m[1] - k[1]) > 3.0
               for k in merged):
            merged.append(m)
    best = merged[0] if merged else (0.0, 0.0, float("inf"))
    h, s = best[0], best[1]
    eps_h, eps_s = 0.25, 0.25
    zph = predict(h + eps_h, s)
    zmh = predict(h - eps_h, s)
    zpp = predict(h, s + eps_s)
    zpm = predict(h, s - eps_s)
    jac = np.array([
        [(zph[0] - zmh[0]) / (2 * eps_h), (zpp[0] - zpm[0]) / (2 * eps_s)],
        [(zph[1] - zmh[1]) / (2 * eps_h), (zpp[1] - zpm[1]) / (2 * eps_s)],
    ])
    sv = np.linalg.svd(jac, compute_uv=False)
    return {
        "recovered_hue": h, "recovered_sat": s, "residual_z": best[2],
        "local_minima_count": len(merged),
        "multi_solutions": [{"hue": a, "sat": b, "residual_z": c} for a, b, c in merged[:8]],
        "jacobian": jac.tolist(),
        "singular_values": [float(v) for v in sv],
        "min_singular": float(sv.min()),
    }


def main() -> int:
    data = assemble()
    records = data["records"]
    holdouts = [r for r in records if r["role"] == "holdout"]
    training = [r for r in records if r["role"] == "train"]

    # --- P6 transfer test ---
    p6 = p6_nodes()
    transfer = []
    for node in p6:
        near = min(
            training,
            key=lambda r: circular_dist(r["hue"], node["hue"]) + abs(r["sat"] - node["sat"]),
        )
        dist = circular_dist(near["hue"], node["hue"]) + abs(near["sat"] - node["sat"])
        if dist <= 5.01:
            dz = math.hypot(
                near["z"][0] - node["z"][0], near["z"][1] - node["z"][1])
            transfer.append({
                "p6": node["tag"], "current": near["tag"],
                "coord_dist": dist, "dz": dz,
            })
    dzs = [t["dz"] for t in transfer]
    current_spread = []
    for hue in (0.0, 240.0):
        pts = [r for r in training if r["sat"] == 100 and r["hue"] == hue]
        if len(pts) >= 4:
            arr = np.array([p["z"] for p in pts])
            current_spread.append(float(np.mean(np.linalg.norm(
                arr - arr.mean(axis=0), axis=1))))
    noise_scale = max(current_spread) if current_spread else 0.01
    transfer_p95 = float(np.percentile(dzs, 95)) if dzs else None
    transfer_pass = transfer_p95 is not None and transfer_p95 <= 3.0 * noise_scale + 0.02
    print(f"P6 转移检验: n={len(dzs)} p95(dz)={transfer_p95} "
          f"当前噪声尺度={noise_scale:.4f} → {'通过' if transfer_pass else '拒绝'}")
    use_p6 = p6 if transfer_pass else None

    # --- model selection by LOO on training ---
    candidates = []
    for harmonics in (1, 2):
        for sat_degree in (1, 2):
            loo = loo_cv(records, harmonics=harmonics, sat_degree=sat_degree,
                         use_p6=use_p6)
            candidates.append({
                "family": "harmonic", "harmonics": harmonics,
                "sat_degree": sat_degree, "loo_rms": loo,
            })
            print(f"模型 h{harmonics}/d{sat_degree}: LOO RMS={loo:.4f}")
    train_recs = [r for r in records if r["role"] == "train"]
    for k in (3, 4, 6, 8):
        errs = []
        for r in train_recs:
            _, _, loo_err = fit_idw(records, k=k, hold_out_tag=r["tag"])
            errs.append(loo_err(r))
        rms = float(np.sqrt(np.mean(np.square(errs))))
        candidates.append({"family": "idw", "k": k, "loo_rms": rms})
        print(f"模型 idw/k{k}: LOO RMS={rms:.4f}")
    best = min(candidates, key=lambda c: c["loo_rms"])
    if best["family"] == "idw":
        predict, info, _ = fit_idw(records, k=best["k"])
    else:
        params, predict, info, basis = fit_model(
            records, harmonics=best["harmonics"], sat_degree=best["sat_degree"],
            use_p6=use_p6,
        )
    print("选定模型:", best, "| 训练:", info)

    # --- holdout inverse validation ---
    inversions = []
    for r in holdouts:
        inv = invert(predict, tuple(r["z"]))
        hue_err = circular_dist(inv["recovered_hue"], r["hue"])
        sat_err = inv["recovered_sat"] - r["sat"]
        inversions.append({
            "true_hue": r["hue"], "true_sat": r["sat"], **inv,
            "hue_error_deg": hue_err, "sat_error_pp": sat_err,
        })
    hue_errs = [i["hue_error_deg"] for i in inversions]
    sat_errs = [abs(i["sat_error_pp"]) for i in inversions]
    hue_ub95 = float(np.percentile(hue_errs, 95))
    sat_ub95 = float(np.percentile(sat_errs, 95))
    verdict = hue_ub95 <= BUDGET["hue_deg"] and sat_ub95 <= BUDGET["sat_pp"]

    # --- S0 hue consistency ---
    s0_rows = [r for r in records if r["sat"] == 0]
    s0_check = {
        "hue0": [r["z"] for r in s0_rows if r["hue"] == 0.0],
        "hue240": [r["z"] for r in s0_rows if r["hue"] == 240.0],
    }
    if s0_check["hue0"] and s0_check["hue240"]:
        a = np.mean([z for z in s0_check["hue0"]], axis=0)
        b = np.mean([z for z in s0_check["hue240"]], axis=0)
        s0_check["dz_between_hues"] = float(np.linalg.norm(a - b))

    result = {
        "schema": "guide12_c12_1_mapping_v1",
        "budget": BUDGET,
        "records": records,
        "p6_transfer": {
            "n_pairs": len(dzs), "p95_dz": transfer_p95,
            "noise_scale": noise_scale, "pass": transfer_pass,
            "pairs": transfer,
        },
        "model_selection": {"candidates": candidates, "selected": best,
                            "fit_info": info, "p6_used_as_training": use_p6 is not None},
        "holdout_inversions": inversions,
        "holdout_summary": {
            "n": len(inversions),
            "hue_error_max": max(hue_errs),
            "hue_error_median": float(np.median(hue_errs)),
            "hue_ub95": hue_ub95,
            "sat_error_absmax": max(sat_errs),
            "sat_ub95": sat_ub95,
            "multisolution_count": sum(i["local_minima_count"] >= 2 for i in inversions),
            "within_budget_05_05": sum(
                i["hue_error_deg"] <= 0.5 and abs(i["sat_error_pp"]) <= 0.5
                for i in inversions),
            "verdict_confidence_upper_bounds": (
                "PASS" if verdict else "FAIL"),
        },
        "s0_hue_consistency": s0_check,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    for i in inversions:
        print(f"  ({i['true_hue']:5.1f},{i['true_sat']:5.1f}) -> "
              f"({i['recovered_hue']:6.2f},{i['recovered_sat']:6.2f}) "
              f"Δh={i['hue_error_deg']:5.2f}° Δs={i['sat_error_pp']:+6.2f}pp "
              f"多解={i['local_minima_count']} σmin={i['min_singular']:.2e}")
    print(f"预算判定（95% 上界）: hue {hue_ub95:.2f}° / SAT {sat_ub95:.2f}pp "
          f"→ {'通过' if verdict else '未通过'}")
    if s0_check.get("dz_between_hues") is not None:
        print(f"S0 hue 一致性 |Δz| = {s0_check['dz_between_hues']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
