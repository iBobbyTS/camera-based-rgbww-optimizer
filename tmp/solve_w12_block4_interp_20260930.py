"""GUIDE12 W12-1 measured-bracket interpolation (3200/0 block 4).

Block 3 measured a clean bracket along the step->step3_half direction:
mired error +4.27 at step and -1.25 at step3_half (duv essentially solved).
Block 4 interpolates between the two MEASURED points - no model
extrapolation - with a primary candidate at the measured zero crossing and
a warm-side safety candidate. Budget after block 4: 9 of 12 unique commands
(expansion justified by measured improvement plus direction consistency in
blocks 2 and 3).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOL = {"cct_K": 25.0, "mired": 1.0, "duv": 0.0005}


def signed_of(candidate: dict) -> dict[str, float]:
    return {
        name: candidate["signed_vs_block_reference"][name]["error_signed"]
        for name in TOL
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: solve_w12_block4_interp <block2-analysis.json> <block3-analysis.json>",
              file=sys.stderr)
        return 2
    block2 = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    block3 = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    step = next(c for c in block2["candidates"] if c["tag"] == "step")
    half = next(c for c in block3["candidates"] if c["tag"] == "step3_half")

    step_signed = signed_of(step)
    half_signed = signed_of(half)

    def crossing_fraction(component: str) -> float:
        a, b = step_signed[component], half_signed[component]
        if a * b > 0:
            raise SystemExit(f"no sign change along the bracket for {component}")
        return a / (a - b)

    f_mired = crossing_fraction("mired")
    primary_f = f_mired
    safety_f = 0.6 * f_mired

    def interp(command_a: dict, command_b: dict, f: float) -> dict[str, int]:
        return {
            key: int(round(command_a[key] + f * (command_b[key] - command_a[key])))
            for key in command_a
        }

    def predicted_at(f: float) -> dict[str, float]:
        return {
            name: step_signed[name] + f * (half_signed[name] - step_signed[name])
            for name in TOL
        }

    candidates = []
    for label, f, role in (
        ("interp", primary_f, "measured_bracket_interpolation"),
        ("interp_warm", safety_f, "measured_bracket_interpolation_safety"),
    ):
        command = interp(step["command"], half["command"], f)
        predicted = predicted_at(f)
        predicted_normalized = {
            name: predicted[name] / TOL[name] for name in TOL
        }
        candidates.append({
            "tag": label,
            "command": command,
            "role": role,
            "new_unique_command": True,
            "solver_evidence": {
                "source_blocks": [2, 3],
                "bracket": {
                    "step": {"command": step["command"], "signed": step_signed},
                    "step3_half": {"command": half["command"], "signed": half_signed},
                },
                "interpolation_fraction": f,
                "mired_zero_crossing_fraction": f_mired,
                "predicted_signed": predicted,
                "predicted_error_normalized": predicted_normalized,
                "predicted_E": max(abs(v) for v in predicted_normalized.values()),
                "method": "linear_interpolation_between_measured_points",
                "extrapolation": False,
                "face_channels": ["warm_white"],
                "final_selection_requires_measured_gate": True,
            },
        })

    out_dir = Path("D:/rgbww-optimizer/guide12-w12/derived")
    candidates_path = out_dir / "w12-3200-gm0-block4-candidates-20260930.json"
    candidates_path.write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    evidence = {
        "schema": "guide12_w12_measured_bracket_interpolation_v1",
        "node": {"cct": 3200, "gm": 0},
        "bracket_signed": {"step": step_signed, "step3_half": half_signed},
        "crossing_fractions": {
            name: crossing_fraction(name)
            for name in TOL if step_signed[name] * half_signed[name] <= 0
        },
        "unique_command_budget": {
            "used_after_block4": 9, "cap": 12,
            "expansion_justification": (
                "measured improvement in every block (10.00 -> 4.27 -> 1.25 best) "
                "with direction-consistent predictions"
            ),
        },
        "candidates": candidates,
    }
    evidence_path = out_dir / "w12-3200-gm0-block4-evidence-20260930.json"
    evidence_path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    for candidate in candidates:
        print(candidate["tag"], candidate["command"],
              "predE=", round(candidate["solver_evidence"]["predicted_E"], 4),
              "pred_signed=", {k: round(v, 5)
                               for k, v in candidate["solver_evidence"]["predicted_signed"].items()})
    print(f"wrote {candidates_path}")
    print(f"wrote {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
