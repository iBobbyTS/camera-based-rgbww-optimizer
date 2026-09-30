"""GUIDE12 batch-1 analysis: native exposure qualification + all-off environment.

Reads the recovered formal-b1 root (13 frames) and answers, per class:
  - rail status per block_06 plane per stop (v3 near-rail metrics),
  - main-layer validity per stop (four planes accepted, no rail, p99 margin),
  - adjacent-stop exposure-normalized chroma consistency (|dz| <= 0.01),
  - fastest qualified stop (selected_member=faster),
and per all-off exposure class:
  - ambient+dark block_06 plane levels A (start vs end drift),
  - A/on ratios and z(on) - z(on-A) sensitivity bounds for the paired class.
No device access; no RAW decode beyond the retained patch statistics.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path("D:/rgbww-optimizer/guide12-batch1/formal-b1-20260929-r1")
OUT = Path("D:/rgbww-optimizer/guide12-batch1/derived/b1-exposure-qualification-20260930.json")
PLANES = ("R", "G1", "G2", "B")
Z_TOL = 0.01
P99_MARGIN_DN = 2.0


def load_rows(name: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def frame_of(capture_id: str) -> dict:
    stats = json.loads(
        (ROOT / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {}
    for plane, blk in block["planes"].items():
        raw = blk["statistics"]["raw_code"]
        nps = blk["statistics"]["normalized_per_second"]
        planes[plane] = {
            "quality": blk["quality"]["status"],
            "failures": list(blk["quality"]["failures"]),
            "near_white_rail_fraction": blk["metrics"].get("near_white_rail_fraction"),
            "white_rail_plateau": blk["metrics"].get("white_rail_plateau"),
            "near_noise_fraction": blk["metrics"].get("near_noise_floor_fraction"),
            "effective_white_level": float(blk["cfa"]["effective_white_level"]),
            "raw_code_min": raw["minimum"],
            "raw_code_max": raw["maximum"],
            "raw_code_p99": raw.get("percentile_99"),
            "normalized_per_second": nps["trimmed_mean"],
        }
    return {
        "capture_id": capture_id,
        "shutter": stats["exposure_metadata"].get("shutter") or stats.get("exposure_seconds"),
        "planes": planes,
    }


def z_of(planes: dict) -> dict[str, float]:
    g = 0.5 * (planes["G1"]["normalized_per_second"] + planes["G2"]["normalized_per_second"])
    return {
        "log_R_over_G": math.log(planes["R"]["normalized_per_second"] / g),
        "log_B_over_G": math.log(planes["B"]["normalized_per_second"] / g),
    }


def stop_status(frame: dict) -> dict:
    rail = any(
        p["white_rail_plateau"]
        or (p["near_white_rail_fraction"] or 0.0) > 0.05
        for p in frame["planes"].values()
    )
    p99_at_ceiling = any(
        (p["raw_code_p99"] or 0.0) >= p["effective_white_level"] - P99_MARGIN_DN
        for p in frame["planes"].values()
    )
    rejected = {
        plane: p["failures"]
        for plane, p in frame["planes"].items()
        if p["quality"] != "accepted"
    }
    if rail or p99_at_ceiling:
        status = "rail_or_ceiling"
    elif rejected:
        status = "plane_rejected_" + "_".join(sorted(rejected))[:60]
    else:
        status = "main_layer_valid"
    return {
        "status": status,
        "rejected_planes": rejected,
        "p99_values": {
            plane: {
                "p99": p["raw_code_p99"],
                "white_level": p["effective_white_level"],
                "margin_dn": None if p["raw_code_p99"] is None
                else p["effective_white_level"] - p["raw_code_p99"],
            }
            for plane, p in frame["planes"].items()
        },
    }


def main() -> None:
    captures = load_rows("captures.jsonl")
    by_id = {str(row["capture_id"]): row for row in captures}
    spec = json.loads((ROOT / "experiment-spec.json").read_text(encoding="utf-8"))

    classes = spec["analysis_contract"]["classes"]
    ladder_frames: dict[str, list[dict]] = {}
    for row in captures:
        step = row.get("plan_step", {})
        if step.get("ladder_class"):
            ladder_frames.setdefault(step["ladder_class"], []).append(frame_of(str(row["capture_id"])))

    classes_out = []
    for klass in classes:
        frames = ladder_frames[klass["label"]]
        stops = []
        for frame in frames:
            entry = {
                **frame,
                **stop_status(frame),
                "z": z_of(frame["planes"]),
            }
            stops.append(entry)
        pair_consistent: dict[int, bool] = {}
        for index, (faster, slower) in enumerate(zip(stops, stops[1:])):
            dz = {
                axis: slower["z"][axis] - faster["z"][axis]
                for axis in ("log_R_over_G", "log_B_over_G")
            }
            consistent = max(abs(v) for v in dz.values()) <= Z_TOL
            faster["consistency_with_next_stop"] = {"dz": dz, "consistent": consistent}
            slower["consistency_with_previous_stop"] = {"dz": dz, "consistent": consistent}
            pair_consistent[index] = consistent
        selected = None
        selection_reason = None
        for index, stop in enumerate(stops):
            if stop["status"] != "main_layer_valid":
                selection_reason = selection_reason or (
                    f"stop {stop['capture_id']} not main-layer valid: {stop['status']}"
                )
                continue
            neighbor_ok = (
                pair_consistent.get(index - 1, False)
                or pair_consistent.get(index, False)
            )
            if neighbor_ok:
                selected = stop["capture_id"]
                selection_reason = "fastest clean stop consistent with an adjacent stop"
                break
        if selected is None and selection_reason is None:
            selection_reason = "no qualified stop had a consistent adjacent pair"
        classes_out.append({
            "label": klass["label"],
            "state_id": klass["state_id"],
            "command": klass["command"],
            "stops": stops,
            "selected_capture_id": selected,
            "selection_reason": selection_reason,
            "verdict": "qualified" if selected else "measurement_window_unqualified",
        })

    ambient = {}
    for row in captures:
        step = row.get("plan_step", {})
        if step.get("capture_role") != "ambient":
            continue
        key = (step["ambient_position"], step["ambient_shutter_speed"])
        ambient[key] = frame_of(str(row["capture_id"]))
    all_off_out = []
    for shutter in spec["analysis_contract"]["all_off_shutters"]:
        start = ambient.get(("start", shutter))
        end = ambient.get(("end", shutter))
        entry = {"shutter": shutter}
        for position, frame in (("start", start), ("end", end)):
            if frame:
                entry[position] = {
                    "capture_id": frame["capture_id"],
                    "planes_nps": {
                        plane: p["normalized_per_second"]
                        for plane, p in frame["planes"].items()
                    },
                    "plane_status": {
                        plane: p["quality"] for plane, p in frame["planes"].items()
                    },
                }
        if start and end:
            entry["drift_ratio_end_over_start"] = {
                plane: (
                    end["planes"][plane]["normalized_per_second"]
                    / start["planes"][plane]["normalized_per_second"]
                    if start["planes"][plane]["normalized_per_second"] > 0 else None
                )
                for plane in PLANES
            }
        # Pair with the on-class sharing this shutter: 1/400 -> red/blue
        # classes' selected-or-middle stop, 1/8 -> white class.
        on_frames = [
            stop for klass in classes_out
            if (klass["label"] == "high_white_load") == (shutter == "1/8")
            for stop in klass["stops"]
            if (shutter == "1/8") or stop["shutter"] in (None, "1/400")
        ]
        if start and on_frames:
            on = on_frames[len(on_frames) // 2]
            ratios = {}
            z_on = z_of(on["planes"])
            z_corrected = {}
            g_corr = 0.5 * (
                on["planes"]["G1"]["normalized_per_second"]
                - start["planes"]["G1"]["normalized_per_second"]
            ) if all(
                on["planes"][p]["normalized_per_second"]
                > start["planes"][p]["normalized_per_second"]
                for p in PLANES
            ) else None
            for plane in PLANES:
                on_val = on["planes"][plane]["normalized_per_second"]
                a_val = start["planes"][plane]["normalized_per_second"]
                ratios[plane] = a_val / on_val if on_val > 0 else None
            if g_corr and g_corr > 0:
                z_corrected = {
                    "log_R_over_G": math.log(
                        (on["planes"]["R"]["normalized_per_second"]
                         - start["planes"]["R"]["normalized_per_second"]) / g_corr
                    ),
                    "log_B_over_G": math.log(
                        (on["planes"]["B"]["normalized_per_second"]
                         - start["planes"]["B"]["normalized_per_second"]) / g_corr
                    ),
                }
                entry["z_on_minus_z_on_minus_A"] = {
                    axis: z_on[axis] - z_corrected[axis] for axis in z_on
                }
            entry["paired_on_capture"] = on["capture_id"]
            entry["A_over_on_ratio"] = ratios
        all_off_out.append(entry)

    artifact = {
        "schema": "guide12_b1_exposure_qualification_v1",
        "run_root": str(ROOT),
        "recovery_note": "engineering failure recovered without recapture; see recovery-note-20260930.md",
        "z_tolerance_adjacent_stop": Z_TOL,
        "p99_margin_dn": P99_MARGIN_DN,
        "classes": classes_out,
        "all_off": all_off_out,
        "notes": (
            "Ladder frames are diagnostics and are not independent model "
            "acceptance frames. near-noise rejections on dark planes of "
            "single-channel commands are recorded as stop status; the main "
            "layer requires all four block_06 planes accepted."
        ),
        "steady_claim": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("== classes ==")
    for klass in classes_out:
        print(f"{klass['label']}: verdict={klass['verdict']}"
              + (f" selected={klass['selected_capture_id']}" if klass["selected_capture_id"]
                 else f" ({klass['selection_reason']})"))
        for stop in klass["stops"]:
            cons = stop.get("consistency_with_next_stop")
            print(f"  {stop['capture_id']}: {stop['status']}"
                  + (f" | dz={[round(v,4) for v in cons['dz'].values()]}"
                     f" consistent={cons['consistent']}" if cons else ""))
    print("== all-off ==")
    for entry in all_off_out:
        print(entry["shutter"], "start planes:", {
            k: round(v, 5) for k, v in (entry.get("start", {}).get("planes_nps") or {}).items()
        }, "| drift:", entry.get("drift_ratio_end_over_start"))
        if "z_on_minus_z_on_minus_A" in entry:
            print("   z(on)-z(on-A):", entry["z_on_minus_z_on_minus_A"],
                  "| A/on:", {k: (round(v, 5) if v is not None else None)
                              for k, v in entry.get("A_over_on_ratio", {}).items()})
    print("->", OUT)


if __name__ == "__main__":
    main()
