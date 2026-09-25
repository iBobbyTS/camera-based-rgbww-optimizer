"""GUIDE11 C3 pre-check: Ray H/S -> z anchor grid, periodicity, inversion.

Assembles every retained Ray reference observation (GUIDE11 C1 brackets,
GUIDE9 HSI batches, N1 white observations as the SAT~0 anchors), builds the
hue x saturation anchor grid in z=[log(R/G), log(B/G)], checks hue-sector
ordering and saturation direction, and reports nearest-anchor inversion with
ambiguity flags. Read-only; outputs the anchor table for Batch2 targeting.
"""
from __future__ import annotations

import glob
import json
import math
from pathlib import Path

OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c3-anchor-self-check-20260925.json")


def z_from_measurements(measurements_dir: Path, capture_id: str) -> dict[str, float] | None:
    path = measurements_dir / f"{capture_id}.patch-statistics.json"
    if not path.is_file():
        return None
    stats = json.loads(path.read_text(encoding="utf-8"))
    block = next((p for p in stats["patches"] if p.get("index") == 6), None)
    if block is None:
        return None
    p = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (p["G1"] + p["G2"])
    if min(p.values()) <= 0 or g <= 0:
        return None
    return {
        "log_R_over_G": math.log(p["R"] / g),
        "log_B_over_G": math.log(p["B"] / g),
    }


def ray_rows(run_root: Path) -> list[tuple[str, dict]]:
    captures_path = run_root / "captures.jsonl"
    if not captures_path.is_file():
        return []
    out = []
    for line in captures_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("source_id") == "ray":
            out.append((str(row["capture_id"]), row.get("plan_step") or row))
    return out


def main() -> None:
    anchors: list[dict] = []

    # GUIDE11 C1 brackets: hue/sat from the plan step.
    c1 = Path("D:/rgbww-optimizer/guide11-c1/formal-c1-20260924-r8")
    for capture_id, step in ray_rows(c1):
        z = z_from_measurements(c1 / "measurements", capture_id)
        if z:
            anchors.append({
                "hue": int(step.get("c1_hue", -1)), "sat": int(step.get("c1_sat", -1)),
                "z": z, "origin": f"C1:{capture_id}",
            })

    # GUIDE9 HSI Ray references: hue/sat parsed from the capture id/role.
    guide9_roots = {
        ("h120-s50", 120, 50): "guide9-h120-s50-batch1-20260820/20260820-170318-fast-direct",
        ("h120-s25", 120, 25): "guide9-h120-s25-batch1-20260821/20260821-204804-fast-direct",
        ("h0-s0", 0, 0): "guide9-h0-s0-batch1-20260821/20260821-004205-fast-direct",
        ("h300-s50", 300, 50): "guide9-h300-s50-batch1-20260823/20260823-220027-fast-direct",
        ("h300-s100", 300, 100): "guide9-h300-s100-batch1-20260823/20260823-h300-retry2",
    }
    base = Path("D:/rgbww-optimizer")
    for (label, hue, sat), rel in guide9_roots.items():
        root = base / rel
        for capture_id, step in ray_rows(root):
            z = z_from_measurements(root / "measurements", capture_id)
            if z:
                anchors.append({
                    "hue": hue, "sat": sat, "z": z, "origin": f"G9:{capture_id}",
                })

    # N1 white Ray observations: the SAT~0 anchors spread over CCT.
    n1_roots = [
        Path("D:/rgbww-optimizer/guide11-n1/formal-n1-s1-20260922-r2"),
        Path("D:/rgbww-optimizer/guide11-n1/formal-n1-s2-20260922"),
    ]
    for root in n1_roots:
        for capture_id, step in ray_rows(root):
            z = z_from_measurements(root / "measurements", capture_id)
            if z and step.get("target_cct") is not None:
                anchors.append({
                    "hue": None, "sat": 0,
                    "cct": int(step["target_cct"]), "gm": int(step.get("target_gm", 100)),
                    "z": z, "origin": f"N1:{capture_id}",
                })

    # Aggregate per (hue, sat): mean z and spread across repeats.
    def key_of(a):
        return (a["hue"], a["sat"])

    groups: dict[tuple, list[dict]] = {}
    for a in anchors:
        groups.setdefault(key_of(a), []).append(a)
    grid = []
    for key in sorted(groups, key=lambda k: (k[1] if k[0] is None else 1, k[0] if k[0] is not None else -1)):
        rows = groups[key]
        zx = [r["z"]["log_R_over_G"] for r in rows]
        zy = [r["z"]["log_B_over_G"] for r in rows]
        entry = {
            "hue": key[0], "sat": key[1],
            "n": len(rows),
            "z_mean": {"log_R_over_G": sum(zx) / len(zx), "log_B_over_G": sum(zy) / len(zy)},
            "z_spread": max(max(zx) - min(zx), max(zy) - min(zy)),
            "origins": [r["origin"] for r in rows][:6],
        }
        if key[0] is None:
            entry["cct_range"] = sorted({r.get("cct") for r in rows})
        grid.append(entry)

    # Saturation direction and sector ordering checks at S50.
    def zmean(hue, sat):
        for e in grid:
            if e["hue"] == hue and e["sat"] == sat:
                return e["z_mean"]
        return None

    checks = []
    for hue in (0, 60, 120, 180, 240, 300):
        s50, s100 = zmean(hue, 50), zmean(hue, 100)
        if s50 and s100:
            checks.append({
                "hue": hue,
                "s50_to_s100_vector": {
                    "log_R_over_G": s100["log_R_over_G"] - s50["log_R_over_G"],
                    "log_B_over_G": s100["log_B_over_G"] - s50["log_B_over_G"],
                },
            })
    # Nearest-anchor inversion over HSI anchors only (white anchors excluded).
    hsi = [e for e in grid if e["hue"] is not None]
    inversions = []
    for e in hsi:
        dists = sorted(
            (
                math.hypot(
                    e["z_mean"]["log_R_over_G"] - o["z_mean"]["log_R_over_G"],
                    e["z_mean"]["log_B_over_G"] - o["z_mean"]["log_B_over_G"],
                ),
                o["hue"], o["sat"],
            )
            for o in hsi if o is not e
        )
        nearest, second = dists[0], dists[1]
        inversions.append({
            "hue": e["hue"], "sat": e["sat"],
            "nearest": {"hue": nearest[1], "sat": nearest[2], "dist": nearest[0]},
            "second": {"hue": second[1], "sat": second[2], "dist": second[0]},
            "ambiguous": second[0] < 2 * nearest[0],
        })

    artifact = {
        "schema": "guide11_c3_anchor_self_check_v1",
        "anchor_count": len(anchors),
        "grid": grid,
        "saturation_direction_s50_to_s100": checks,
        "nearest_anchor_inversion": inversions,
        "inversion_ambiguous_count": sum(1 for i in inversions if i["ambiguous"]),
        "note": "z=log(R/Gmean),log(B/Gmean) from block_06; white N1 anchors approximate SAT0; calibration precedes any tolerance verdict",
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("anchors:", len(anchors), "| grid cells:", len(grid))
    for e in grid:
        label = f"H{e['hue']}/S{e['sat']}" if e["hue"] is not None else f"white/cct{e.get('cct_range')}"
        print(f"  {label:>24} n={e['n']} z=({e['z_mean']['log_R_over_G']:+.3f},{e['z_mean']['log_B_over_G']:+.3f}) spread={e['z_spread']:.3f}")
    print("ambiguous inversions:", artifact["inversion_ambiguous_count"])
    print("->", OUT)


if __name__ == "__main__":
    main()
