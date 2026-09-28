"""Fit the GUIDE11 C3 periodic hue x SAT command model from measured anchors.

S50 layer: 6 anchors (C1 finals at H0/60/180/240 + GUIDE9 closed-route
bests H120/H300, best-repeat confirmed). S100 layer: 4 anchors (C1 finals;
H120/H300 S100 routes stay closed). SAT0 white: GUIDE9 H0/S0 best-repeat.
The C1 commands are pending the running best-repeat confirmation batch;
refit after its analysis lands.
"""
from __future__ import annotations

import json
from pathlib import Path

from camera_based_rgbww_optimizer.optimization.guide11 import (
    fit_periodic_hue_sat_command_model,
    interpolate_hsi_command,
)

OUT = Path("D:/rgbww-optimizer/guide11-c1/derived/c3-command-model-20260928.json")

S50 = {
    0: {"r": 3835, "g": 903, "b": 903, "cw": 0, "ww": 0},        # C1 batch2 best
    60: {"r": 4095, "g": 4095, "b": 974, "cw": 9, "ww": 9},      # C1 batch2 best
    120: {"r": 0, "g": 4095, "b": 831, "cw": 2111, "ww": 1919},  # G9 best-repeat 20260821
    180: {"r": 1024, "g": 4095, "b": 4095, "cw": 0, "ww": 0},    # C1 batch1 fallback
    240: {"r": 1024, "g": 2048, "b": 4095, "cw": 0, "ww": 0},    # C1 batch1 fallback
    300: {"r": 2495, "g": 0, "b": 2559, "cw": 192, "ww": 4095},  # G9 best-repeat 20260823
}
S100 = {
    0: {"r": 2048, "g": 0, "b": 0, "cw": 0, "ww": 0},            # C1 batch1 fallback
    60: {"r": 4095, "g": 4095, "b": 1024, "cw": 0, "ww": 0},     # C1 batch1 fallback
    180: {"r": 1024, "g": 4095, "b": 4095, "cw": 0, "ww": 0},    # C1 batch1 fallback
    240: {"r": 1024, "g": 2048, "b": 4095, "cw": 0, "ww": 0},    # C1 batch1 fallback
}
WHITE_SAT0 = {"r": 0, "g": 1279, "b": 1663, "cw": 4095, "ww": 4095}  # G9 H0/S0 best-repeat


def main() -> None:
    anchors = []
    for hue, command in S50.items():
        anchors.append({"hue": hue, "sat": 50, "command": command, "source": "guide11_c1_final/guide9_best_repeat"})
    for hue, command in S100.items():
        anchors.append({"hue": hue, "sat": 100, "command": command, "source": "guide11_c1_final"})
    model = fit_periodic_hue_sat_command_model(anchors, white_layer=WHITE_SAT0)

    # Anchor residuals and a periodicity spot check.
    print("S50 order:", model["layers"]["50"]["harmonic_order"],
          "max residual:", {k: round(v, 2) for k, v in model["layers"]["50"]["max_anchor_residual"].items()})
    print("S100 order:", model["layers"]["100"]["harmonic_order"],
          "max residual:", {k: round(v, 2) for k, v in model["layers"]["100"]["max_anchor_residual"].items()})
    a = interpolate_hsi_command(model, 0.0, 70)
    b = interpolate_hsi_command(model, 360.0, 70)
    assert a["command"] == b["command"], "periodicity broken"
    sample = interpolate_hsi_command(model, 30.0, 75)
    print("sample H30/S75:", sample["command"], sample["sat_layer"])
    sample_low = interpolate_hsi_command(model, 210.0, 20)
    print("sample H210/S20:", sample_low["command"], sample_low["sat_layer"])

    artifact = dict(model)
    artifact.update({
        "provenance": {
            "s50_anchors": {str(h): {"command": c, "origin": "C1 final (pending confirm)" if h in (0, 60, 180, 240) else "G9 best-repeat closed route"} for h, c in S50.items()},
            "s100_anchors": {str(h): {"command": c, "origin": "C1 final (pending confirm)"} for h, c in S100.items()},
            "sat0_white": {"command": WHITE_SAT0, "origin": "G9 H0/S0 best-repeat 20260821"},
            "closed_routes_kept_closed": ["H120/S100", "H300/S100"],
        },
        "status": "provisional_until_c1_confirm_analysis",
        "sat0_hue": "not_applicable",
        "note": "commands at anchor hues exact; between anchors periodic interpolation; SAT<50 blends white->S50 hue-first; H120/H300 S100 absent by closed-route rule",
    })
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("->", OUT)


if __name__ == "__main__":
    main()
