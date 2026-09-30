"""GUIDE12 W12-1 efficiency-corrected step-3 solve (3200/0 block 3).

The pooled cross-block secant refit is degenerate along the green direction
(smallest command-delta singular value 13.3 codes; only ~10-code local
excitation between u0/step/half_step), so it is rejected as a derivative
owner. Instead the block-1 surrogate stays the span owner (three orthogonal
768-code probe axes, rank 3), and the u0 -> step transfer is calibrated by
per-component measured/predicted efficiency ratios before the next solve.
The measured full-tolerance gate stays the only selection authority.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12

COMPONENTS = ("cct_K", "mired", "duv")
TOL = dict(guide12.W12_TOLERANCES)
LONG_OF = {
    "cw": "cold_white", "ww": "warm_white", "r": "red", "g": "green", "b": "blue",
}
SHORT_OF = {v: k for k, v in LONG_OF.items()}


def normalized_response(candidate: dict) -> dict[str, float]:
    return {
        name: candidate["signed_vs_block_reference"][name]["error_signed"] / TOL[name]
        for name in COMPONENTS
    }


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "usage: solve_w12_step3 <block1-analysis.json> <block2-analysis.json>"
            " <out-prefix>",
            file=sys.stderr,
        )
        return 2
    block1 = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    block2 = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    candidates1 = {c["tag"]: c for c in block1["candidates"]}
    candidates2 = {c["tag"]: c for c in block2["candidates"]}
    sensitivity = block1["sensitivity_normalized"]

    base = candidates2["step"]
    base_response = normalized_response(base)
    u0_response = normalized_response(candidates1["u0_repeat"])

    # Measured u0 -> step transfer, predicted by the block-1 surrogate.
    u0_cmd = candidates1["u0_repeat"]["command"]
    step_cmd = base["command"]
    predicted_transfer = {}
    for name in COMPONENTS:
        predicted_transfer[name] = sum(
            sensitivity[name][LONG_OF[ch]] * (step_cmd[ch] - u0_cmd[ch])
            for ch in u0_cmd
        )
    measured_transfer = {
        name: base_response[name] - u0_response[name] for name in COMPONENTS
    }
    efficiency = {}
    for name in COMPONENTS:
        if abs(predicted_transfer[name]) < 0.5:
            efficiency[name] = None  # transfer too small to calibrate
        else:
            efficiency[name] = measured_transfer[name] / predicted_transfer[name]
    # A component without a calibratable transfer keeps efficiency 1.0 but is
    # flagged; sign flips would reject the surrogate outright.
    for name, value in list(efficiency.items()):
        if value is None or value <= 0:
            raise SystemExit(
                f"u0->step transfer for {name} is not a calibratable direction "
                f"(predicted {predicted_transfer[name]:.4f}, efficiency {value}); "
                "refuse to extrapolate"
            )

    scaled_sensitivity = {
        name: {
            channel: value * efficiency[name]
            for channel, value in slopes.items()
        }
        for name, slopes in sensitivity.items()
    }

    steps = {}
    for label, scale in (("step3", 1.0), ("step3_half", 0.5)):
        steps[label] = guide12.solve_guide12_w12_face_step(
            base["command"], base_response, scaled_sensitivity,
            face_channels=["warm_white"], scale=scale,
        )

    candidates = []
    for label, role in (
        ("step3", "face_step_efficiency_corrected"),
        ("step3_half", "face_step_efficiency_corrected_half"),
    ):
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
                "measured_over_predicted_efficiency": efficiency,
                "predicted_transfer_u0_to_step": predicted_transfer,
                "measured_transfer_u0_to_step": measured_transfer,
                "predicted_error_normalized": step["predicted_error_normalized"],
                "predicted_E": step["predicted_E"],
                "scale": step["scale"],
                "active_bound_channels": step["active_bound_channels"],
                "method": step["method"],
                "method_note": (
                    "block-1 orthogonal-probe surrogate with per-component "
                    "measured u0->step efficiency calibration; pooled refit "
                    "rejected as degenerate along green"
                ),
                "solved_subspace": step["solved_subspace"],
                "face_channels": step["face_channels"],
                "surrogate": True,
                "final_selection_requires_measured_gate": True,
            },
        })

    evidence = {
        "schema": "guide12_w12_efficiency_corrected_step_v1",
        "node": {"cct": 3200, "gm": 0},
        "rejected_pooled_refit_reason": (
            "smallest command-delta singular value 13.3 codes (green ~10-code "
            "local excitation); fitted green slope -0.42 mired/code is not a "
            "credible local derivative"
        ),
        "base": {
            "tag": "step", "command": base["command"],
            "error_normalized": base_response,
            "E_normalized": base["E_normalized"],
        },
        "transfer": {
            "predicted": predicted_transfer,
            "measured": measured_transfer,
            "efficiency": efficiency,
        },
        "cross_block_reference_delta": {
            name: block2["block_reference_target"][name]
            - block1["block_reference_target"][name]
            for name in COMPONENTS
        },
        "next_steps": steps,
    }
    out_prefix = Path(argv[3])
    evidence_path = out_prefix.with_name(out_prefix.name + "-evidence.json")
    evidence_path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    candidates_path = out_prefix.with_name(out_prefix.name + "-candidates.json")
    candidates_path.write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("efficiency:", {k: round(v, 4) for k, v in efficiency.items()})
    print("cross-block reference delta:",
          {k: round(v, 5) for k, v in evidence["cross_block_reference_delta"].items()})
    for label in ("step3", "step3_half"):
        step = steps[label]
        print(label, step["command"], "predE=", round(step["predicted_E"], 4),
              "pred_err=", {k: round(v, 3)
                            for k, v in step["predicted_error_normalized"].items()},
              "bounds=", step["active_bound_channels"])
    print(f"wrote {candidates_path}")
    print(f"wrote {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
