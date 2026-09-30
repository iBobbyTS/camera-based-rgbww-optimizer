"""GUIDE12 W12-1 local-block analysis (3200/0 block 1 and successors).

Read-only analysis of one completed W12-1 block run root:
- per-frame block_06 white points (four-plane trimmed means, rawpy matrix,
  same estimator as the GUIDE11/W2 analyzer),
- Ray before/after reference compatibility gate (one product tolerance per
  component; target = per-component mean of before/after),
- signed strip-minus-reference errors and the full-tolerance E per candidate,
- block-local secant sensitivity fit with the u0 repeat as the frozen base
  (A = u - u0, B = r(u) - r(u0)) over tolerance-normalized outputs,
- the next face-constrained bounded step via guide12.solve_guide12_w12_face_step.

No device, camera or network work. CR3s are read only for rgb_xyz matrices.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

TOLERANCES = dict(guide12.W12_TOLERANCES)
COMPONENTS = ("cct_K", "mired", "duv")


def load_rows(root: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw_path = str((next(
        r for r in load_rows(root) if str(r.get("capture_id")) == capture_id
    ).get("capture") or {}).get("saved_file", ""))
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            Path(raw_path), np
        )
    estimate = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path]
    )
    return {
        "cct_K": float(estimate["cct_K"]),
        "duv": float(estimate["duv"]),
        "mired": 1_000_000.0 / float(estimate["cct_K"]),
    }


def signed_errors(strip_wp, reference_wp) -> dict:
    signed = guide12.signed_white_errors(strip_wp, reference_wp, TOLERANCES)
    return signed


def analyze_block(run_root: str, out_path: str | None = None) -> dict:
    root = Path(run_root)
    plan = json.loads((root / "experiment-spec.json").read_text(encoding="utf-8"))
    contract = plan["analysis_contract"]
    rows = load_rows(root)
    by_role: dict[str, dict] = {}
    frames = []
    for row in rows:
        step = row["plan_step"]
        capture_id = str(step["capture_id"])
        wp = white_point_of(root, capture_id)
        exposure = row["capture"]["recorded_exposure"]
        entry = {
            "capture_id": capture_id,
            "source_id": step["source_id"],
            "tag": (
                "ray_before" if step.get("ray_reference_position") == "raybefore"
                else "ray_after" if step.get("ray_reference_position") == "rayafter"
                else str(step.get("candidate_tag"))
            ),
            "command": step.get("command"),
            "white_point": wp,
            "recorded_shutter": exposure.get("nominal_shutter_speed"),
        }
        frames.append(entry)
        by_role[entry["tag"]] = entry

    ray_before = by_role["ray_before"]["white_point"]
    ray_after = by_role["ray_after"]["white_point"]
    compatibility = {
        name: {
            "before": ray_before[name], "after": ray_after[name],
            "delta": ray_after[name] - ray_before[name],
            "tolerance": TOLERANCES[name],
            "within": abs(ray_after[name] - ray_before[name]) <= TOLERANCES[name],
        }
        for name in COMPONENTS
    }
    compatible = all(item["within"] for item in compatibility.values())
    target = {
        name: 0.5 * (ray_before[name] + ray_after[name]) for name in COMPONENTS
    }

    candidates = []
    for frame in frames:
        if frame["source_id"] != "strip":
            continue
        signed = signed_errors(frame["white_point"], target)
        candidates.append({
            "tag": frame["tag"],
            "capture_id": frame["capture_id"],
            "command": frame["command"],
            "white_point": frame["white_point"],
            "signed_vs_block_reference": signed["components"],
            "E_normalized": signed["E_normalized"],
        })

    result: dict = {
        "schema": "guide12_w12_block_analysis_v1",
        "run_root": str(root),
        "node": {"cct": contract["node"]["cct"], "gm": contract["node"]["gm"]},
        "block_index": contract["node"]["block_index"],
        "frames": frames,
        "reference_compatibility": compatibility,
        "reference_compatible": compatible,
        "block_reference_target": target,
        "candidates": candidates,
        "tolerances": TOLERANCES,
        "sign_convention": "strip_minus_reference",
    }

    base = next((c for c in candidates if c["tag"] == "u0_repeat"), None)
    probes = [c for c in candidates if c["tag"] != "u0_repeat"]
    if compatible and base is not None and probes:
        base_error_normalized = {
            name: base["signed_vs_block_reference"][name]["error_signed"]
            / TOLERANCES[name]
            for name in COMPONENTS
        }
        observations = [
            {
                "command": {
                    "cold_white": c["command"]["cw"], "warm_white": c["command"]["ww"],
                    "red": c["command"]["r"], "green": c["command"]["g"],
                    "blue": c["command"]["b"],
                },
                "response": {
                    name: c["signed_vs_block_reference"][name]["error_signed"]
                    / TOLERANCES[name]
                    for name in COMPONENTS
                },
            }
            for c in probes
        ]
        base_observation = {
            "command": {
                "cold_white": base["command"]["cw"], "warm_white": base["command"]["ww"],
                "red": base["command"]["r"], "green": base["command"]["g"],
                "blue": base["command"]["b"],
            },
            "response": base_error_normalized,
        }
        fit = guide12.secant_sensitivity_fit(
            observations,
            channel_names=("cold_white", "warm_white", "red", "green", "blue"),
            base_observation=base_observation,
            output_names=COMPONENTS,
        )
        sensitivity_normalized = None
        if fit.get("status") == "fitted":
            sensitivity_normalized = {
                name: {
                    channel: float(fit["sensitivity"][channel_index][output_index])
                    for channel_index, channel in enumerate(
                        ("cold_white", "warm_white", "red", "green", "blue")
                    )
                }
                for output_index, name in enumerate(COMPONENTS)
            }
            long_names = {
                "cw": "cold_white", "ww": "warm_white", "r": "red",
                "g": "green", "b": "blue",
                "cold_white": "cold_white", "warm_white": "warm_white",
                "red": "red", "green": "green", "blue": "blue",
            }
            face = [long_names[k] for k in contract["face_channels"]]
            steps = {}
            for label, scale in (("step", 1.0), ("half_step", 0.5)):
                steps[label] = guide12.solve_guide12_w12_face_step(
                    base["command"], base_error_normalized, sensitivity_normalized,
                    face_channels=face, scale=scale,
                )
            result["next_steps"] = steps
        result["base_error_normalized"] = base_error_normalized
        result["secant_fit"] = {
            k: v for k, v in fit.items() if k != "sensitivity"
        }
        result["sensitivity_normalized"] = sensitivity_normalized

    best = min(candidates, key=lambda c: c["E_normalized"])
    result["best_candidate"] = {"tag": best["tag"], "E_normalized": best["E_normalized"]}
    result["gate_E_pass"] = best["E_normalized"] <= 1.0

    if out_path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"wrote {out}")
    return result


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: analyze_w12_block <run-root> [out.json]", file=sys.stderr)
        return 2
    result = analyze_block(argv[1], argv[2] if len(argv) > 2 else None)
    print(json.dumps({
        "node": result["node"], "block": result["block_index"],
        "reference_compatible": result["reference_compatible"],
        "best": result["best_candidate"], "gate_E_pass": result["gate_E_pass"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
