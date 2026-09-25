"""One-shot GUIDE11 C1 batch-1 product-layer analysis."""
from __future__ import annotations

import json
import math
from pathlib import Path

RUN = Path("D:/rgbww-optimizer/guide11-c1/formal-c1-20260924-r8")
OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c1-batch1-analysis-20260925.json")


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
    return {
        "log_R_over_G": math.log(p["R"] / g),
        "log_B_over_G": math.log(p["B"] / g),
        "g1_minus_g2_over_mean_g": (p["G1"] - p["G2"]) / g,
    }


def dist(a: dict[str, float], b: dict[str, float]) -> float:
    return math.hypot(a["log_R_over_G"] - b["log_R_over_G"], a["log_B_over_G"] - b["log_B_over_G"])


def main() -> None:
    plan = json.loads((RUN / "experiment-spec.json").read_text(encoding="utf-8"))
    rows = [json.loads(l) for l in (RUN / "captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_target: dict[tuple[int, int], dict[str, list[str]]] = {}
    for row in rows:
        step = row.get("plan_step", {})
        key = (int(step["c1_hue"]), int(step["c1_sat"]))
        by_target.setdefault(key, {}).setdefault(str(row["source_id"]), []).append(
            (str(row["capture_id"]), str(step.get("role", "")).split("_")[-1])
        )
    results = []
    for target in plan["analysis_contract"]["targets"]:
        hue, sat = target["hue"], target["sat"]
        groups = by_target[(hue, sat)]
        ray_ids = groups.get("ray", [])
        strip_entries = groups.get("strip", [])
        ray_z_before = z_of(ray_ids[0][0]) if ray_ids else None
        ray_z_after = z_of(ray_ids[-1][0]) if len(ray_ids) > 1 else None
        bracket_consistent = (
            ray_z_before is not None and ray_z_after is not None
            and dist(ray_z_before, ray_z_after) < 0.02
        )
        ray_z_mean = (
            {
                axis: 0.5 * (ray_z_before[axis] + ray_z_after[axis])
                for axis in ray_z_before
            }
            if ray_z_before and ray_z_after else ray_z_before
        )
        candidates = []
        for capture_id, role in strip_entries:
            z = z_of(capture_id)
            candidates.append({
                "capture_id": capture_id,
                "role": role,
                "z": z,
                "z_distance_to_ray": dist(z, ray_z_mean) if ray_z_mean else None,
            })
        candidates.sort(key=lambda c: (c["z_distance_to_ray"] is None, c["z_distance_to_ray"] or 0.0))
        results.append({
            "hue": hue, "sat": sat,
            "ray_z_before": ray_z_before,
            "ray_z_after": ray_z_after,
            "ray_bracket_consistent": bracket_consistent,
            "ray_z_mean": ray_z_mean,
            "candidates_ranked": candidates,
            "best": candidates[0] if candidates else None,
            "batch2_justified": bool(candidates) and candidates[0]["z_distance_to_ray"] is not None and candidates[0]["z_distance_to_ray"] > 0.05,
            "certification": "batch1_selection_frame_only; Ray H/S to z calibration pending C3; no pass verdict this round",
        })
    artifact = {
        "schema": "guide11_c1_batch1_analysis_v1",
        "run_root": str(RUN),
        "target_count": len(results),
        "note": "Distances in z=[log(R/Gmean), log(B/Gmean)] units; ranking only, no product tolerance verdict before the C3 Ray-menu calibration",
        "results": results,
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'target':>10} {'bracket':>8} {'best role':>28} {'z-dist':>8} {'batch2?':>7}")
    for r in results:
        best = r["best"] or {}
        print(f"H{r['hue']:>3}/S{r['sat']:<3} {str(r['ray_bracket_consistent']):>8} {best.get('role','')[:28]:>28} {best.get('z_distance_to_ray', -1):>8.3f} {str(r['batch2_justified']):>7}")
    print("->", OUT)


if __name__ == "__main__":
    main()
