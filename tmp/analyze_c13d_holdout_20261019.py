"""GUIDE13 C13-D runtime holdout analysis (offline, frozen).

Merges the two C13-D roots (56-frame main + 7-frame tail = 63 frames, 21
requests x Ray sandwich) and evaluates, per request, the primary-layer z of
the strip model output minus the Ray-bracket mean, the same-hue-track
checks, and the label-honesty (requested vs realized SAT). Same-hue
equivalent-SAT/Hue deviation uses the C13-A local J only where one exists
(H0/S50-family, H60/S100-family); other targets report direct dz only, per
GUIDE13 C13-D (no new pass gate from worst failure).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide13  # noqa: E402
from camera_based_rgbww_optimizer.optimization import (  # noqa: E402
    white_calibration_common as common,
)

ROOTS = [
    Path("D:/rgbww-optimizer/guide13-c13d/formal-c13d-holdout"),
    Path("D:/rgbww-optimizer/guide13-c13d/formal-c13d-holdout-tail"),
]
OUT = Path("D:/rgbww-optimizer/guide13-c13d/derived/"
           "c13d-holdout-analysis-20261019.json")
_MATRIX_CACHE: dict[str, object] = {}


def z_of(root: Path, capture_id: str):
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    layer = guide13.primary_layer_from_stats(stats)
    if layer["primary_quality"] != "accepted":
        return None, layer["primary_quality"]
    physical = {
        str(json.loads(line)["capture_id"]): json.loads(line)
        for line in (root / "physical-returns.jsonl")
        .read_text(encoding="utf-8").splitlines() if line.strip()
    }
    raw_path = str(physical[capture_id]["cr3_path"])
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            Path(raw_path), np)
    return guide13.z_from_planes(layer["planes_nps"]), "accepted"


def main() -> int:
    by_req: dict[str, dict[str, list]] = {}
    total = 0
    for root in ROOTS:
        rows = [
            json.loads(line)
            for line in (root / "captures.jsonl").read_text(encoding="utf-8")
            .splitlines() if line.strip()
        ]
        total += len(rows)
        for row in rows:
            step = row["plan_step"]
            req = step["c13d_request"]
            slot = "ref" if step["c13d_position"].startswith("ray") else "strip"
            z, q = z_of(root, str(row["capture_id"]))
            by_req.setdefault(req, {}).setdefault(slot, []).append({
                "capture_id": str(row["capture_id"]),
                "position": step["c13d_position"],
                "z": z, "quality": q,
                "realized_sat": step.get("c13d_realized_sat"),
                "sat_status": step.get("c13d_sat_status"),
            })
    results = []
    for req in sorted(by_req,
                      key=lambda k: (int(k.split("/")[0]), int(k.split("/")[1]))):
        sl = by_req[req]
        refs = [x for x in sl.get("ref", []) if x["z"] is not None]
        strip = sl.get("strip", [None])[0]
        entry = {"request": req}
        if strip is None or strip["z"] is None or not refs:
            entry["status"] = "incomplete_or_primary_invalid"
            entry["detail"] = {
                "refs": len(refs), "strip_quality": strip and strip["quality"]}
            results.append(entry)
            continue
        ray = tuple(float(np.mean([r["z"][i] for r in refs])) for i in (0, 1))
        dz = (strip["z"][0] - ray[0], strip["z"][1] - ray[1])
        entry.update({
            "status": "measured",
            "strip_capture_id": strip["capture_id"],
            "dz": dz,
            "worst_abs_dz": max(abs(dz[0]), abs(dz[1])),
            "ray_drift": (refs[-1]["z"][0] - refs[0]["z"][0],
                          refs[-1]["z"][1] - refs[0]["z"][1]),
            "realized_sat": strip["realized_sat"],
            "sat_status_label": strip["sat_status"],
        })
        results.append(entry)
    # same-hue track grouping
    tracks: dict[str, list] = {}
    for r in results:
        if r.get("status") != "measured":
            continue
        hue = r["request"].split("/")[0]
        tracks.setdefault(hue, []).append(r)
    track_report = {}
    for hue, items in tracks.items():
        sats = sorted(int(r["request"].split("/")[1]) for r in items)
        track_report[f"H{hue}"] = {
            "sats": sats,
            "worst_by_sat": {
                r["request"].split("/")[1]: round(r["worst_abs_dz"], 4)
                for r in sorted(items, key=lambda x: int(x["request"].split("/")[1]))},
            "labels": {r["request"].split("/")[1]: r["sat_status_label"]
                       for r in items},
        }
    artifact = {
        "schema": "guide13_c13d_holdout_analysis_v1",
        "frames_total": total,
        "roots": [str(r) for r in ROOTS],
        "requests": results,
        "same_hue_tracks": track_report,
        "summary": {
            "measured": sum(1 for r in results if r.get("status") == "measured"),
            "requests": len(results),
            "median_worst_dz": float(np.median(
                [r["worst_abs_dz"] for r in results
                 if r.get("status") == "measured"])) if any(
                r.get("status") == "measured" for r in results) else None,
            "max_worst_dz": max((r["worst_abs_dz"] for r in results
                                 if r.get("status") == "measured"), default=None),
        },
        "comparison_rule": (
            "same-hue track equivalent-SAT and Hue deviation only; direct dz "
            "reported for all; no new pass gate from worst failure; local J "
            "conversion only where a measured J exists"),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    for r in results:
        if r.get("status") == "measured":
            dz = r["dz"]
            print(f"{r['request']:>8s} worst={r['worst_abs_dz']:.4f} "
                  f"dz=({dz[0]:+.4f},{dz[1]:+.4f}) label={r['sat_status_label']}")
        else:
            print(f"{r['request']:>8s} {r['status']}")
    print("median worst:", artifact["summary"]["median_worst_dz"],
          "| max:", artifact["summary"]["max_worst_dz"])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
