"""GUIDE11 C1 batch2 improvement analysis with full-frame exposure guards."""
from __future__ import annotations

import json
import math
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.frame_exposure import frame_exposure_profile

RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1b2-20260926-r6")
B1_RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1-20260924-r8")
B1_ANALYSIS = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-batch1-analysis-20260925.json")
OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-batch2-analysis-20260927.json")


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


def raw_path_of(row: dict) -> str:
    return str((row.get("capture") or {}).get("saved_file", ""))


def main() -> None:
    rows = [json.loads(l) for l in RUN.joinpath("captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    b1_rows = [json.loads(l) for l in B1_RUN.joinpath("captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_target: dict[tuple[int, int], dict[str, list[dict]]] = {}
    for row in rows:
        step = row.get("plan_step", {})
        key = (int(step["c1_hue"]), int(step["c1_sat"]))
        by_target.setdefault(key, {}).setdefault(str(row["source_id"]), []).append(row)

    b1 = json.loads(B1_ANALYSIS.read_text(encoding="utf-8"))
    b1_fallback = {
        (int(t["hue"]), int(t["sat"])): t for t in b1["results"]
    }

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

        fallback = b1_fallback.get(key) or {}
        fb_id = (fallback.get("best") or {}).get("capture_id")
        fallback_z = z_of(B1_RUN, fb_id) if fb_id else None
        fallback_dist = dist(fallback_z, ray_mean) if (fallback_z and ray_mean) else None

        candidates = []
        for row in groups.get("strip", []):
            profile = frame_exposure_profile(raw_path_of(row))
            frames_guarded += 1
            if profile["classification"] == "saturated":
                saturated += 1
            z = z_of(RUN, row["capture_id"])
            candidates.append({
                "capture_id": row["capture_id"],
                "command": row.get("plan_step", {}).get("command"),
                "z": z,
                "z_distance_to_ray": dist(z, ray_mean) if ray_mean else None,
                "frame_classification": profile["classification"],
                "saturated_fraction": profile["saturated_fraction"],
            })
        candidates.sort(key=lambda c: (c["z_distance_to_ray"] is None, c["z_distance_to_ray"] or 9))
        best = candidates[0] if candidates else None
        improved = bool(
            best and best["z_distance_to_ray"] is not None
            and fallback_dist is not None
            and best["z_distance_to_ray"] < fallback_dist
        )
        results.append({
            "hue": key[0], "sat": key[1],
            "ray_bracket_consistent": ray_consistent,
            "ray_z_mean": ray_mean,
            "batch1_fallback": {
                "capture_id": fb_id,
                "z_distance_to_ray": fallback_dist,
            },
            "batch2_candidates": candidates,
            "best": best,
            "improved_vs_batch1": improved,
            "improvement": (
                fallback_dist - best["z_distance_to_ray"]
                if improved else None
            ),
        })

    artifact = {
        "schema": "guide11_c1_batch2_analysis_v1",
        "run_root": str(RUN),
        "capture_count": len(rows),
        "frames_profiled": frames_guarded,
        "saturated_frames": saturated,
        "targets": results,
        "improved_target_count": sum(1 for r in results if r["improved_vs_batch1"]),
        "note": "z distances to paired Ray means; full-frame exposure profile guards every strip frame",
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'target':>10} {'bracket':>8} {'fb dist':>8} {'b2 best':>8} {'improved':>8} {'frame':>8}")
    for r in results:
        fb = r['batch1_fallback']['z_distance_to_ray']
        bb = r['best']['z_distance_to_ray'] if r['best'] else None
        print(f"H{r['hue']:>3}/S{r['sat']:<3} {str(r['ray_bracket_consistent']):>8} {fb if fb is not None else -1:>8.3f} {bb if bb is not None else -1:>8.3f} {str(r['improved_vs_batch1']):>8} {r['best']['frame_classification'] if r['best'] else '-':>8}")
    print('improved:', artifact['improved_target_count'], '/', len(results), '| saturated frames:', saturated)
    print('->', OUT)


if __name__ == "__main__":
    main()
