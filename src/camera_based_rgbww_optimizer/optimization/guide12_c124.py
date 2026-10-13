"""GUIDE12 C12-4: frozen runtime periodic color model + holdout plan.

Per GUIDE 12.GUIDE.md section 5 C12-4: the runtime output function this
module freezes maps a requested (hue, sat) to a strip command by periodic
hue interpolation over the C12-2/C12-3 adopted (validated) commands, with
SAT entering monotonically between the validated SAT anchors. Whatever
function ships at runtime is the one measured: ten new non-node holdout
requests (six sectors, two periodic neighbors across 0/360, two fixed
low-SAT points), each with its own Ray before/after bracket around one
strip observation (30 frames), test total error, local hue direction,
SAT monotonicity, and bounded prediction intervals. The legacy
"within_c1_anchor_envelope" comparison is reported as one comparison,
never as the product gate.

Model (GUIDE13-corrected semantics, 2026-10-13):
- anchors: per hue in {0,60,120,180,240,300}, the S25 and S50 adopted
  commands, plus every adopted high-SAT command (H60/S100 today); SAT 0
  is served by the single validated white S0 command and does not
  change with hue.
- SAT ladder: a SAT layer participates for a request hue only when the
  layer is actually measured there (an anchor at exactly that hue, or
  two bracketing anchor hues for interpolation). Requests between two
  available layers are linearly blended (hue first, then SAT - frozen
  order) and reported as interpolated; requests beyond the top available
  layer are served at that top layer and reported as gamut_compressed
  with requested/realized SAT. Nothing is silently clamped and nothing
  is labelled as-requested unless it truly is.
- winner projection: the final command is projected to true fullscale
  (max channel 4095) with round-half-up integerization - the same
  frozen order as W12-3.

GUIDE12-era behavior that this module no longer produces: S<=25 served
by the colored S25 layer (so S0 was never white), S>=50 served by the
S50 layer even where an adopted S100 command existed, and interior SAT
values labelled with a blanket "as-requested" note. The GUIDE12 C12-4
holdout (2/10) remains an evaluation of that old function only.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Mapping

C124_EXPERIMENT_ID = "GUIDE12_C12_4_RUNTIME_MODEL_HOLDOUT_V1"
C124_SCHEMA = "direct_guide12_c124_model_holdout_v1"
CHANNELS = ("cw", "ww", "r", "g", "b")
FULLSCALE = 4095
C124_HUE_ANCHORS = (0, 60, 120, 180, 240, 300)
C124_SAT_ANCHORS = (25, 50)

# Adopted (validated) commands from C12-2/C12-3, keyed "hue/sat". The
# S0 white command ("0/0") is part of the anchor set: GUIDE13 requires
# the runtime to emit the validated fullscale S0 command for SAT 0
# instead of the old colored S25 clamp.
C124_ADOPTED: dict[str, dict[str, int]] = {
    "0/0": {"cw": 4095, "ww": 2240, "r": 658, "g": 1681, "b": 1425},
    "0/25": {"cw": 1575, "ww": 2343, "r": 4095, "g": 1024, "b": 1024},
    "0/50": {"cw": 282, "ww": 1818, "r": 4095, "g": 180, "b": 480},
    "60/25": {"cw": 1575, "ww": 1575, "r": 4095, "g": 4095, "b": 1792},
    "60/50": {"cw": 1050, "ww": 1818, "r": 4095, "g": 4095, "b": 1024},
    "60/100": {"cw": 0, "ww": 0, "r": 4095, "g": 3390, "b": 80},
    "120/25": {"cw": 3343, "ww": 1018, "r": 1759, "g": 4095, "b": 1300},
    "120/50": {"cw": 282, "ww": 1818, "r": 368, "g": 4095, "b": 1024},
    "180/25": {"cw": 1575, "ww": 2193, "r": 1507, "g": 4095, "b": 2657},
    "180/50": {"cw": 1050, "ww": 1050, "r": 920, "g": 4095, "b": 2388},
    "240/25": {"cw": 3111, "ww": 2343, "r": 542, "g": 2048, "b": 4095},
    "240/50": {"cw": 796, "ww": 547, "r": 1031, "g": 2048, "b": 4095},
    "300/25": {"cw": 3111, "ww": 4095, "r": 4095, "g": 1804, "b": 4095},
    "300/50": {"cw": 1818, "ww": 2586, "r": 4095, "g": 528, "b": 4095},
}

# Ten frozen non-node holdout requests: six mid-sector, two periodic
# neighbors straddling 0/360, two fixed low-SAT interior points.
C124_HOLDOUTS: tuple[tuple[int, int], ...] = (
    (30, 50), (90, 50), (150, 50), (210, 50), (270, 50), (330, 50),
    (2, 25), (358, 25),
    (75, 35), (255, 40),
)


def _layer_hues(sat_anchor: int) -> list[int]:
    """Hues that actually have an adopted command at this SAT layer."""
    if sat_anchor == 0:
        return list(C124_HUE_ANCHORS)  # S0 white anchor is hue-independent
    return [h for h in C124_HUE_ANCHORS if f"{h}/{sat_anchor}" in C124_ADOPTED]


def _layer_available_for_hue(sat_anchor: int, hue_n: int) -> bool:
    """A SAT layer can serve a hue only where it is measured: an anchor
    at exactly that hue, or two bracketing anchor hues on the ring. The
    S0 white layer is measured for every hue by definition."""
    if sat_anchor == 0:
        return True
    hues = _layer_hues(sat_anchor)
    if not hues:
        return False
    if hue_n in hues:
        return True
    if len(hues) < 2:
        return False
    ring = sorted(hues)
    spans = list(zip(ring, ring[1:])) + [(ring[-1], ring[0] + 360)]
    target = hue_n if hue_n >= ring[0] else hue_n + 360
    return any(lo < target < hi for lo, hi in spans)


def _sat_layers(sat: int, hue_n: int) -> tuple[int, int | None, float]:
    """(lo, hi, w): the bracketing available SAT layers for this hue
    and the blend weight; hi is None when serving at the single layer
    lo (either exactly the request or an explicit compression)."""
    ladder = [0] + [
        s for s in sorted({int(k.split("/")[1]) for k in C124_ADOPTED
                           if int(k.split("/")[1]) > 0})
        if _layer_available_for_hue(s, hue_n)
    ]
    if sat <= ladder[0]:
        return ladder[0], None, 0.0
    if sat >= ladder[-1]:
        return ladder[-1], None, 0.0
    for lo, hi in zip(ladder, ladder[1:]):
        if lo <= sat <= hi:
            if sat == lo:
                return lo, None, 0.0
            if sat == hi:
                return hi, None, 0.0
            return lo, hi, (sat - lo) / (hi - lo)
    raise ValueError(f"C12-4 SAT ladder failed for sat={sat} hue={hue_n}")


def _hue_blend(hue: int, sat_anchor: int) -> dict[str, float]:
    """Periodic linear blend of anchor commands at one SAT layer,
    shortest arc on the 0/360 ring; only hues with an adopted command
    at this SAT layer participate. Layer 0 is the hue-independent white
    S0 command."""
    if sat_anchor == 0:
        base = C124_ADOPTED["0/0"]
        return {ch: float(base[ch]) for ch in CHANNELS}
    layer = {
        h: C124_ADOPTED[f"{h}/{sat_anchor}"]
        for h in C124_HUE_ANCHORS
        if f"{h}/{sat_anchor}" in C124_ADOPTED
    }
    hues = sorted(layer)
    if not hues:
        raise ValueError(f"C12-4 model has no anchors at SAT {sat_anchor}")
    if len(hues) == 1:
        if hue % 360 != hues[0]:
            raise ValueError(
                f"C12-4 SAT {sat_anchor} layer only measured at hue "
                f"{hues[0]}; cannot serve hue {hue}")
        return {ch: float(layer[hues[0]][ch]) for ch in CHANNELS}
    ring = hues + [hues[0] + 360]
    target = hue if hue >= hues[0] else hue + 360
    for k in range(len(hues)):
        if ring[k] <= target <= ring[k + 1]:
            h0, h1 = hues[k], ring[k + 1] % 360
            span = ring[k + 1] - ring[k]
            w = 0.0 if span == 0 else (target - ring[k]) / span
            return {
                ch: (1 - w) * float(layer[h0][ch]) + w * float(layer[h1][ch])
                for ch in CHANNELS
            }
    raise ValueError(f"C12-4 hue blend failed for {hue}")


def c124_model_command(hue: int, sat: int) -> dict[str, Any]:
    """Frozen runtime output function (GUIDE13-corrected semantics):
    periodic hue interpolation first, then SAT-ladder blend, then
    true-fullscale projection with round-half-up integerization. The
    returned record states the requested and realized SAT and whether
    the request was gamut-compressed; only exact serves are
    as-requested."""
    hue_n = hue % 360
    lo, hi, w = _sat_layers(sat, hue_n)
    base = _hue_blend(hue_n, lo)
    if hi is not None and w > 0.0:
        top = _hue_blend(hue_n, hi)
        raw = {ch: (1 - w) * base[ch] + w * top[ch] for ch in CHANNELS}
    else:
        raw = base
    peak = max(raw.values())
    if peak <= 0:
        raise ValueError("C12-4 model produced a zero command")
    projected = {
        ch: max(0, min(FULLSCALE, int(math.floor(v * FULLSCALE / peak + 0.5))))
        for ch, v in raw.items()
    }
    winner = max(projected, key=lambda ch: projected[ch])
    if projected[winner] != FULLSCALE:
        projected[winner] = FULLSCALE
    if hi is None and sat == lo:
        realized, status, compressed = lo, "as-requested", False
    elif hi is None:
        realized, status, compressed = lo, "gamut_compressed", True
    else:
        realized, status, compressed = sat, "interpolated", False
    return {
        "request": {"hue": hue, "sat": sat},
        "command": projected,
        "winning_channel": winner,
        "realized_sat": realized,
        "sat_status": status,
        "gamut_compressed": compressed,
        "served_layers": [lo, hi] if hi is not None else [lo],
    }

# Ray HSI shutters for the holdout targets: exact P6 (hue, sat) anchors
# exist for the mid-sector hues at S50/S25; (75,35)/(255,40)/(2,25)/
# (358,25) transfer from the nearest P6 row with the C12-1 rule.
C124_RAY_SHUTTERS: dict[str, str] = {
    "30/50": "1/6400", "90/50": "1/5000", "150/50": "1/4000",
    "210/50": "1/4000", "270/50": "1/3200", "330/50": "1/2500",
    "2/25": "1/4000", "358/25": "1/4000",
    "75/35": "1/3200", "255/40": "1/4000",
}


def build_guide12_c124_holdout_plan(
    requests: tuple[tuple[int, int], ...] = C124_HOLDOUTS,
    *,
    ray_shutter_overrides: Mapping[str, str] | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Ten holdout requests, each an independent Ray-bracketed FAST
    sandwich (ray before, strip model output, ray after) - 30 frames."""
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.guide12_n2 import W12_FAST_DWELL_S
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    models = {}
    for cct_key_index, (hue, sat) in enumerate(requests):
        key = f"{hue}/{sat}"
        model = c124_model_command(hue, sat)
        models[key] = model["command"]
        ray_shutter = str(
            (ray_shutter_overrides or {}).get(key) or C124_RAY_SHUTTERS[key])
        ray_command = {"mode": "hsi", "hue": hue, "sat": sat,
                       "intensity_percent": 100.0}
        cache = key.replace("/", "-")
        frozen[f"c124-ray-{cache}"] = ray_shutter
        frozen[f"c124-strip-{cache}"] = "1/400"

        def add(src: str, role: str, cmd: dict[str, Any], shutter: str,
                cache_key: str, position: str) -> None:
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-{src}-guide12-c124-h{hue}-s{sat}"
                    f"-{position}"
                ),
                "source_id": src,
                "state_id": f"C124_H{hue}_S{sat}_{position.upper()}",
                "role": role,
                "command": dict(cmd),
                "exact_command_hash": thermal.canonical_sha256(cmd),
                "requested_elapsed_s": W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": shutter,
                "exposure_cache_key": cache_key,
                "strip_zero_required": src == "ray",
                "ray_zero_required": src == "strip",
                "c124_request": key, "c124_position": position,
                "c124_model_command": dict(model["command"]) if src == "strip" else None,
            })

        add("ray", "ray_reference", ray_command, ray_shutter,
            f"c124-ray-{cache}", "raybefore")
        add("strip", "strip_model_output", model["command"], "1/400",
            f"c124-strip-{cache}", "strip")
        add("ray", "ray_reference", ray_command, ray_shutter,
            f"c124-ray-{cache}", "rayafter")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C124_EXPERIMENT_ID,
        "variant": "c12_4_runtime_model_holdout_v1",
        "stage": "GUIDE12-C12-4-HOLDOUT",
        "phase": "formal",
        "source": "guide12_c12_4_runtime_model_20261012",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "adopted_commands": {
                "path": "D:/rgbww-optimizer/guide12-c122/derived/"
                        "c124-adopted-20261012.json"},
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_c124_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "ray_rule": (
                "exact P6 anchors where present; nearest-row transfer for "
                "interior coordinates (C12-1 rule)"
            ),
            "strip_rule": "uniform 1/400 (model outputs are S25-S50 class)",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0, "holdout_requests": len(requests),
            "repair_rounds_cap": 1, "repair_holdouts_cap": 6,
            "repair_frames_cap": 18,
        },
        "execution_authorization": {
            "schema": C124_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C124_EXPERIMENT_ID,
            "bounded_device_scope": True, "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide12_c12_4_model_holdout",
            "requests": [f"{h}/{s}" for h, s in requests],
            "model_commands": models,
            "checks": [
                "total 2D error per request (radial SAT / tangential Hue)",
                "local hue direction consistency",
                "SAT monotonicity across the model outputs",
                "bounded prediction intervals",
            ],
            "c1_envelope_note": (
                "within_c1_anchor_envelope is one comparison, never the "
                "product gate"
            ),
            "steady_claim": False,
        },
    }
