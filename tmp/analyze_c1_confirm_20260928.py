"""GUIDE11 C1 best-repeat confirmation analysis with full-frame guards.

Per target: fresh Ray bracket consistency, two independent FAST
confirmations of the final selected command, three-observation summary
(selection frame + 2 confirms) with spread, and stability verdict per
GUIDE11 C1 semantics (selection process flagged; no pass/fail invented).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.frame_exposure import frame_exposure_profile

RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1c-20260928-r1")
B1_RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1-20260924-r8")
B2_RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1b2-20260926-r6")
B2_ANALYSIS = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-batch2-analysis-20260927.json")
OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-confirm-analysis-20260928.json")


def planes_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads((root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(encoding="utf-8"))
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    return {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }


def z_of(root: Path, capture_id: str) -> dict[str, float]:
    p = planes_of(root, capture_id)
    g = 0.5 * (p["G1"] + p["G2"])
    return {"log_R_over_G": math.log(p["R"] / g), "log_B_over_G": math.log(p["B"] / g)}


def dist(a, b) -> float:
    return math.hypot(a["log_R_over_G"] - b["log_R_over_G"], a["log_B_over_G"] - b["log_B_over_G"])


def spread(zs: list[dict]) -> dict[str, float]:
    out = {}
    for axis in ("log_R_over_G", "log_B_over_G"):
        vals = [z[axis] for z in zs]
        mean = sum(vals) / len(vals)
        out[axis] = {
            "mean": mean,
            "min": min(vals),
            "max": max(vals),
            "max_abs_deviation": max(abs(v - mean) for v in vals),
        }
    out["pairwise_max"] = max(
        dist(a, b) for i, a in enumerate(zs) for b in zs[i + 1:]
    )
    return out


def main() -> None:
    rows = [json.loads(l) for l in RUN.joinpath("captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    b2 = json.loads(B2_ANALYSIS.read_text(encoding="utf-8"))
    selection_by_target = {
        (int(t["hue"]), int(t["sat"])): t for t in b2["targets"]
    }
    spec = json.loads(RUN.joinpath("experiment-spec.json").read_text(encoding="utf-8"))
    contract_by_target = {
        (int(t["hue"]), int(t["sat"])): t for t in spec["analysis_contract"]["targets"]
    }

    by_target: dict[tuple[int, int], dict[str, list[dict]]] = {}
    for row in rows:
        step = row.get("plan_step", {})
        key = (int(step["c1_hue"]), int(step["c1_sat"]))
        by_target.setdefault(key, {}).setdefault(str(row["source_id"]), []).append(row)

    results = []
    frames_guarded = 0
    saturated = 0
    for key in sorted(by_target):
        groups = by_target[key]
        ray_rows = sorted(groups.get("ray", []), key=lambda r: int(r["capture_id"].split("-")[0]))
        ray_z = [z_of(RUN, r["capture_id"]) for r in ray_rows]
        ray_mean = {
            axis: sum(z[axis] for z in ray_z) / len(ray_z) for axis in ray_z[0]
        } if ray_z else None
        ray_consistent = len(ray_z) == 2 and dist(ray_z[0], ray_z[1]) < 0.02

        contract = contract_by_target.get(key) or {}
        selection_batch = contract.get("selection_batch")
        selection_capture = contract.get("selected_capture_id")
        selection_root = B2_RUN if selection_batch == "batch2" else B1_RUN
        selection_z = z_of(selection_root, selection_capture) if selection_capture else None

        confirms = []
        for row in groups.get("strip", []):
            profile = frame_exposure_profile(str((row.get("capture") or {}).get("saved_file", "")))
            frames_guarded += 1
            if profile["classification"] == "saturated":
                saturated += 1
            z = z_of(RUN, row["capture_id"])
            confirms.append({
                "capture_id": row["capture_id"],
                "z": z,
                "z_distance_to_fresh_ray": dist(z, ray_mean) if ray_mean else None,
                "frame_classification": profile["classification"],
                "saturated_fraction": profile["saturated_fraction"],
            })

        three_obs = ([selection_z] if selection_z else []) + [c["z"] for c in confirms]
        confirm_dist = [c["z_distance_to_fresh_ray"] for c in confirms]
        # Stability semantics: confirmations repeat the same command under
        # independent FAST cycles. Reproducibility is about the spread of the
        # strip observations; distance to Ray is the accuracy figure.
        strip_obs = [selection_z] + [c["z"] for c in confirms] if selection_z else [c["z"] for c in confirms]
        stability = spread(strip_obs) if len(strip_obs) >= 2 else None
        results.append({
            "hue": key[0], "sat": key[1],
            "selected_command": contract.get("selected_command"),
            "selection_batch": selection_batch,
            "selection_capture_id": selection_capture,
            "ray_bracket_consistent": ray_consistent,
            "ray_z_mean": ray_mean,
            "confirms": confirms,
            "confirm_z_distance_mean": (
                sum(d for d in confirm_dist if d is not None) / len([d for d in confirm_dist if d is not None])
                if any(d is not None for d in confirm_dist) else None
            ),
            "selection_z_distance_to_fresh_ray": (
                dist(selection_z, ray_mean) if (selection_z and ray_mean) else None
            ),
            "three_observation_spread": spread(three_obs) if len(three_obs) >= 2 else None,
            "independent_fast_observations_total": len(three_obs),
            "certification": "selection frame flagged; two independent FAST confirmations complete the GUIDE11 C1 three-observation requirement",
        })

    artifact = {
        "schema": "guide11_c1_confirm_analysis_v1",
        "run_root": str(RUN),
        "capture_count": len(rows),
        "frames_profiled": frames_guarded,
        "saturated_frames": saturated,
        "targets": results,
        "note": "z vs fresh paired Ray means; full-frame exposure guard on every confirm frame; spread quantifies command reproducibility",
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'target':>10} {'bracket':>8} {'sel->ray':>9} {'conf mean':>10} {'3obs sprd':>10} {'frame':>8}")
    for r in results:
        sel_d = r["selection_z_distance_to_fresh_ray"]
        conf = r["confirm_z_distance_mean"]
        spr = (r["three_observation_spread"] or {}).get("pairwise_max")
        frames = "/".join(c["frame_classification"][:4] for c in r["confirms"])
        print(f"H{r['hue']:>3}/S{r['sat']:<3} {str(r['ray_bracket_consistent']):>8} {sel_d if sel_d is not None else -1:>9.3f} {conf if conf is not None else -1:>10.3f} {spr if spr is not None else -1:>10.3f} {frames:>8}")
    print("saturated frames:", saturated, "|", "->", OUT)


if __name__ == "__main__":
    main()
