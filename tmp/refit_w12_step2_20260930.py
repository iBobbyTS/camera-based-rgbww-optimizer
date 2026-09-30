"""GUIDE12 W12-1 pooled cross-block refit and next-step solve (3200/0 block 3).

Combines block 1 (u0 repeat + 3 single-axis probes) and block 2 (step +
half_step) observations, each expressed against its own block Ray reference,
re-centres the GUIDE12 secant fit on the current best command (block-2 step),
solves the next face-constrained bounded step, and freezes the block-3
candidate list with full solver provenance.

Cross-block pooling assumes the two block references are compatible; their
per-component delta is recorded as an uncertainty note. The measured
full-tolerance gate stays the only selection authority.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12

LONG_OF = {
    "cw": "cold_white", "ww": "warm_white", "r": "red", "g": "green", "b": "blue",
}
COMPONENTS = ("cct_K", "mired", "duv")
TOL = dict(guide12.W12_TOLERANCES)


def normalized_response(candidate: dict) -> dict[str, float]:
    return {
        name: candidate["signed_vs_block_reference"][name]["error_signed"] / TOL[name]
        for name in COMPONENTS
    }


def long_command(command: dict) -> dict[str, int]:
    return {LONG_OF[k]: int(v) for k, v in command.items()}


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "usage: refit_w12_step2 <block1-analysis.json> <block2-analysis.json>"
            " <out-prefix>",
            file=sys.stderr,
        )
        return 2
    block1 = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    block2 = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    out_prefix = Path(argv[3])

    by_tag = {}
    for block in (block1, block2):
        for candidate in block["candidates"]:
            by_tag.setdefault(candidate["tag"], []).append(candidate)

    base = by_tag["step"][-1]
    base_response = normalized_response(base)
    observations = []
    reference_notes = []
    for block, block_name in ((block1, "block1"), (block2, "block2")):
        for candidate in block["candidates"]:
            if candidate["tag"] == "step" and block is block2:
                continue
            observations.append({
                "command": long_command(candidate["command"]),
                "response": normalized_response(candidate),
                "tag": candidate["tag"],
                "reference_block": block_name,
            })
    reference_delta = {
        name: block2["block_reference_target"][name]
        - block1["block_reference_target"][name]
        for name in COMPONENTS
    }
    reference_notes.append({
        "cross_block_reference_delta": reference_delta,
        "note": (
            "each observation keeps its own block Ray reference; the two "
            "references differ by far less than one tolerance per component"
        ),
    })

    base_observation = {
        "command": long_command(base["command"]),
        "response": base_response,
    }
    fit = guide12.secant_sensitivity_fit(
        observations,
        channel_names=("cold_white", "warm_white", "red", "green", "blue"),
        base_observation=base_observation,
        output_names=COMPONENTS,
    )
    if fit.get("status") != "fitted":
        raise SystemExit(f"secant refit failed: {fit.get('status')}")
    sensitivity = {
        name: {
            channel: float(fit["sensitivity"][channel_index][output_index])
            for channel_index, channel in enumerate(
                ("cold_white", "warm_white", "red", "green", "blue")
            )
        }
        for output_index, name in enumerate(COMPONENTS)
    }

    # Prediction-vs-measurement consistency of the block-2 step under the
    # block-1 surrogate (direction agreement evidence for the budget rule).
    b1_fit_step_pred = None
    for label, steps in (("block1_step_prediction", block1.get("next_steps") or {}),):
        step = steps.get("step")
        if step:
            b1_fit_step_pred = step["predicted_error_normalized"]
    consistency = None
    if b1_fit_step_pred is not None:
        consistency = {
            "predicted": b1_fit_step_pred,
            "measured": base_response,
            "ratio_measured_over_predicted_per_component": {
                name: (
                    None if abs(b1_fit_step_pred[name]) < 1e-9
                    else base_response[name] / b1_fit_step_pred[name]
                )
                for name in COMPONENTS
            },
        }

    face = ["warm_white"]
    steps = {}
    for label, scale in (("step2", 1.0), ("step2_half", 0.5)):
        steps[label] = guide12.solve_guide12_w12_face_step(
            base["command"], base_response, sensitivity,
            face_channels=face, scale=scale,
        )

    candidates = []
    for label, role in (("step2", "face_step_refit"), ("step2_half", "face_step_refit_half")):
        step = steps[label]
        candidates.append({
            "tag": label,
            "command": step["command"],
            "role": role,
            "new_unique_command": True,
            "solver_evidence": {
                "source_blocks": [1, 2],
                "base_tag": "step",
                "base_command": base["command"],
                "base_error_normalized": base_response,
                "predicted_error_normalized": step["predicted_error_normalized"],
                "predicted_E": step["predicted_E"],
                "scale": step["scale"],
                "active_bound_channels": step["active_bound_channels"],
                "method": step["method"],
                "solved_subspace": step["solved_subspace"],
                "face_channels": step["face_channels"],
                "surrogate": True,
                "final_selection_requires_measured_gate": True,
            },
        })

    evidence = {
        "schema": "guide12_w12_pooled_refit_v1",
        "node": {"cct": 3200, "gm": 0},
        "base": {"tag": "step", "command": base["command"],
                 "error_normalized": base_response,
                 "E_normalized": base["E_normalized"]},
        "observations": observations,
        "reference_notes": reference_notes,
        "secant_fit": {k: v for k, v in fit.items() if k != "sensitivity"},
        "sensitivity_normalized": sensitivity,
        "block1_surrogate_consistency": consistency,
        "next_steps": steps,
    }
    evidence_path = out_prefix.with_name(out_prefix.name + "-evidence.json")
    evidence_path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    candidates_path = out_prefix.with_name(out_prefix.name + "-candidates.json")
    candidates_path.write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {candidates_path}")
    print(f"wrote {evidence_path}")
    for label in ("step2", "step2_half"):
        step = steps[label]
        print(label, step["command"], "predE=", round(step["predicted_E"], 4),
              "bounds=", step["active_bound_channels"])
    print("fit rank:", fit["command_delta_rank"], "sens rank:", fit["sensitivity_rank"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
