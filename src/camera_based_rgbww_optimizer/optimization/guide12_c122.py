"""GUIDE12 C12-2: fullscale main-node color solving (frozen scaffolding).

Per GUIDE 12.GUIDE.md section 5 C12-2: thirteen requests - six main hues
(0/60/120/180/240/300) at S50/S100 plus S0 - each solved against a
same-target same-block Ray HSI direct reference with the W12-1 machinery
discipline: true fullscale faces, per-command independent FAST resets,
box-constrained trust-region steps in the product z space
(ln(R/G), ln(B/G)), and >=3 independent confirmations of any adopted
command. Solver inputs from near-rail plateau frames are void (C1
lesson): every slope comes from frames the quality system accepted.

Budgets (per request): <=8 new unique commands (12 only with measured
improvement), at most 2 distinct fullscale faces, confirmations do not
count as new unique commands. The block runner executes one frozen block
(Ray bracket + <=4 strip candidates) per run; the offline block analyzer
between runs computes dz, local Jacobian secants, the next face step and
the budget ledger - no in-run adaptation.

Ray shutters are frozen from the exact P6 node-brightness anchors
(every request is a P6 grid node) with the C12-1 rule: brightness x 0.59
N2 anchor factor, 9000 DN target, next faster camera stop; H120/S100 and
H300/S100 reproduce the C12-1 frozen values, S0 reproduces the W12-3
session-C shutter.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

C122_EXPERIMENT_ID = "GUIDE12_C12_2_COLOR_FULLSCALE_SOLVING_V1"
C122_SCHEMA = "direct_guide12_c122_color_solving_v1"
CHANNELS = ("cw", "ww", "r", "g", "b")
FULLSCALE = 4095

C122_HUES = (0, 60, 120, 180, 240, 300)
C122_REQUESTS: tuple[tuple[int, int], ...] = tuple(
    (hue, sat) for hue in C122_HUES for sat in (50, 100)
) + ((0, 0),)

# Frozen 2026-10-09 from the exact P6 anchors (p6-node-brightness.json),
# C12-1 rule; anchor self-checks recorded in the module docstring.
C122_RAY_SHUTTERS: dict[str, str] = {
    "0/50": "1/2000", "0/100": "1/1600",
    "60/50": "1/6400", "60/100": "1/3200",
    "120/50": "1/5000", "120/100": "1/3200",
    "180/50": "1/5000", "180/100": "1/2500",
    "240/50": "1/4000", "240/100": "1/3200",
    "300/50": "1/3200", "300/100": "1/1600",
    "0/0": "1/6400",
}

# Initial strip shutter tiers (frozen anchors, structural dominance rule):
# white-dominant commands (cw+ww > r+g+b) take the W12-2 white-node tier
# 1/100 (predicted ~10900 DN for the S0 seed vs the 3200/100 anchor
# 13214 DN); RGB-dominant fullscale commands keep the GUIDE9/C1 tier
# 1/400. Later blocks carry explicit per-candidate shutters predicted
# from the measured base frame (offline exposure pre-check), never
# widened in-run.
C122_STRIP_SHUTTER_RGB = "1/400"
C122_STRIP_SHUTTER_WHITE = "1/100"


def c122_initial_strip_shutter(command: Mapping[str, int]) -> str:
    if int(command["cw"]) + int(command["ww"]) > int(command["r"]) + int(command["g"]) + int(command["b"]):
        return C122_STRIP_SHUTTER_WHITE
    return C122_STRIP_SHUTTER_RGB

# Solver weighting only (engineering allocation, NOT the product gate):
# S0 gates at |dz| <= 0.01 per log ratio; S50/S100 steps are weighted at
# 0.02 per z component. The product gate stays Hue +/-2deg, SAT +/-2pp
# evaluated by the offline analyzer against the Ray reference.
C122_Z_SCALE = {0: 0.01, 50: 0.02, 100: 0.02}

C122_UNIQUE_COMMAND_CAP = 8
C122_UNIQUE_COMMAND_CAP_EXPANDED = 12
C122_FACE_CAP = 2
C122_CONFIRMATIONS_REQUIRED = 3
C122_CANDIDATES_PER_BLOCK = 4
C122_MAX_STEP_CODES = 768.0

# Sector structure follows the frozen GUIDE9/C1 candidate families
# (dominant channels rotated by hue sector; SAT enters through the
# white-channel floor, S50 keeps the 1050 white base).
_SECTOR: dict[int, tuple[tuple[str, ...], dict[str, int]]] = {
    0: (("r",), {"g": 1024, "b": 1024}),
    60: (("r", "g"), {"b": 1024}),
    120: (("g",), {"r": 1024, "b": 1024}),
    180: (("g", "b"), {"r": 1024}),
    240: (("b",), {"r": 1024, "g": 2048}),
    300: (("r", "b"), {"g": 1024}),
}


def c122_initial_command(hue: int, sat: int) -> dict[str, int]:
    """Initial fullscale command for a request (sector-dominant family).

    Dominant channels sit at 4095 (true fullscale face), sector secondary
    channels at the C1 tiers, and S50 adds the 1050 white floor on both
    white channels. S0 starts from the neutral fullscale mix.
    """
    if (hue, sat) == (0, 0):
        # neutral seed: white channels dominant, small RGB balance
        return {"cw": 2600, "ww": 2600, "r": 700, "g": 700, "b": 700}
    if hue not in _SECTOR or sat not in (50, 100):
        raise ValueError(f"C12-2 request {hue}/{sat} is not one of the 13 frozen requests")
    dominant, secondary = _SECTOR[hue]
    command = {ch: 0 for ch in CHANNELS}
    for ch in dominant:
        command[ch] = FULLSCALE
    for ch, value in secondary.items():
        command[ch] = max(command[ch], value)
    if sat == 50:
        command["cw"] = 1050
        command["ww"] = 1050
    return command


def c122_probe_candidates(
    base_command: Mapping[str, int],
) -> list[dict[str, Any]]:
    """Frozen first-block candidate list: base repeat plus single-axis
    probes on the free channels with headroom (W12-1 probe discipline)."""
    from camera_based_rgbww_optimizer.optimization.guide12 import _long_command, _SHORT_BY_LONG, _LONG_CHANNELS

    long_command = _long_command(base_command)
    command = {_SHORT_BY_LONG[c]: int(long_command[c]) for c in _LONG_CHANNELS}
    face = sorted(ch for ch in CHANNELS if command[ch] == 0)
    candidates: list[dict[str, Any]] = [{
        "tag": "u0_repeat",
        "command": dict(command),
        "role": "base_repeat",
        "new_unique_command": False,
        "face_channels": face,
        "strip_shutter": c122_initial_strip_shutter(command),
    }]
    for ch in CHANNELS:
        if command[ch] <= 0:
            continue
        step = min(C122_MAX_STEP_CODES, float(FULLSCALE - command[ch]))
        if step <= 0:
            continue
        probed = dict(command)
        probed[ch] = int(command[ch] + step)
        candidates.append({
            "tag": f"probe_{ch}",
            "command": probed,
            "role": "single_axis_probe",
            "probe_channel": ch,
            "probe_step_codes": int(step),
            "new_unique_command": True,
            "face_channels": face,
            "strip_shutter": c122_initial_strip_shutter(command),
        })
    if len(candidates) > C122_CANDIDATES_PER_BLOCK:
        candidates = candidates[:C122_CANDIDATES_PER_BLOCK]
    return candidates


def solve_guide12_c122_face_step(
    base_command: Mapping[str, int],
    base_error_z: Mapping[str, float],
    sensitivity_z: Mapping[str, Mapping[str, float]],
    *,
    face_channels: Sequence[str],
    sat: int,
    scale: float = 1.0,
) -> dict[str, Any]:
    """Box-constrained step on one fullscale face in the z subspace.

    Mirrors the W12-1 face step with the color output space: signed
    strip-minus-reference errors and per-channel slopes for
    (z_r, z_b) = (ln(R/G), ln(B/G)), weighted by the frozen per-request
    solver scale. Face channels stay pinned at 0; every other channel
    respects [0, 4095] and the per-step cap. The caller projects the
    returned command to true fullscale before it becomes a candidate;
    final adoption always requires the measured product gate.
    """
    import numpy as np

    from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
        solve_box_constrained_least_squares,
    )
    from camera_based_rgbww_optimizer.optimization.guide12 import _long_command, _SHORT_BY_LONG, _LONG_CHANNELS

    if not 0.0 < scale <= 1.0:
        raise ValueError("C12-2 step scale must be in (0, 1]")
    z_scale = C122_Z_SCALE.get(sat)
    if z_scale is None:
        raise ValueError(f"C12-2 request sat {sat} has no frozen z scale")
    long_base = _long_command(base_command)
    locked = {str(c) for c in face_channels}
    outputs = ("z_r", "z_b")
    sensitivity = np.array([
        [float(sensitivity_z[o][c]) / z_scale for c in _LONG_CHANNELS]
        for o in outputs
    ])
    base_error = np.array([
        float(base_error_z[o]) / z_scale for o in outputs
    ])
    lower = np.array([
        max(-float(long_base[c]), -C122_MAX_STEP_CODES) if c not in locked else 0.0
        for c in _LONG_CHANNELS
    ])
    upper = np.array([
        min(float(FULLSCALE - long_base[c]), C122_MAX_STEP_CODES) if c not in locked else 0.0
        for c in _LONG_CHANNELS
    ])
    if np.any(lower > upper):
        raise ValueError("C12-2 face leaves an infeasible step box")
    unmodeled = [
        i for i in range(len(_LONG_CHANNELS))
        if _LONG_CHANNELS[i] not in locked
        and float(np.linalg.norm(sensitivity[:, i])) <= 1e-12
    ]
    for i in unmodeled:
        lower[i] = 0.0
        upper[i] = 0.0
    if all(
        float(np.linalg.norm(sensitivity[:, i])) <= 1e-12
        for i in range(len(_LONG_CHANNELS)) if i not in locked
    ):
        raise ValueError("C12-2 step lacks any modeled free direction")
    delta = np.asarray(
        solve_box_constrained_least_squares(sensitivity, -base_error, lower, upper),
        dtype=float,
    ) * scale
    codes: dict[str, int] = {}
    final_delta: dict[str, float] = {}
    for i, channel in enumerate(_LONG_CHANNELS):
        box_low = int(float(long_base[channel]) + lower[i])
        box_high = int(float(long_base[channel]) + upper[i])
        code = min(box_high, max(box_low, int(round(float(long_base[channel]) + delta[i]))))
        codes[_SHORT_BY_LONG[channel]] = int(code)
        final_delta[_SHORT_BY_LONG[channel]] = float(code - long_base[channel])
    predicted = base_error + sensitivity @ (
        np.array([final_delta[_SHORT_BY_LONG[c]] for c in _LONG_CHANNELS])
    )
    return {
        "command": codes,
        "delta": final_delta,
        "scale": scale,
        "face_channels": sorted(locked),
        "predicted_error_normalized": {
            name: float(predicted[index]) for index, name in enumerate(outputs)
        },
        "predicted_E": max(abs(float(v)) for v in predicted),
        "unmodeled_locked_channels": [
            _SHORT_BY_LONG[_LONG_CHANNELS[i]] for i in unmodeled
        ],
        "method": "box_constrained_least_squares_active_set_enumeration",
        "surrogate": True,
        "final_selection_requires_measured_gate": True,
    }


def build_guide12_c122_block_plan(
    hue: int,
    sat: int,
    candidates: Sequence[Mapping[str, Any]],
    *,
    block_index: int,
    ray_shutter: str | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One C12-2 solving block: Ray HSI bracket around <=4 strip candidates.

    Every observation is its own FAST state (unique state_id -> independent
    off600 reset, exact command hash, 120 s dwell). The Ray reference is the
    same-target HSI command at INT100 with its frozen shutter; strip
    candidates carry explicit per-candidate shutters (initial tier 1/400,
    later blocks predicted offline from the measured base frame).
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.guide12_n2 import W12_FAST_DWELL_S
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    if (hue, sat) not in C122_REQUESTS:
        raise ValueError(f"C12-2 request {hue}/{sat} is not one of the 13 frozen requests")
    if not 1 <= len(candidates) <= C122_CANDIDATES_PER_BLOCK:
        raise ValueError(
            f"C12-2 block needs 1..4 strip candidates, got {len(candidates)}"
        )
    request = f"{hue}/{sat}"
    resolved_ray_shutter = str(ray_shutter or C122_RAY_SHUTTERS[request])
    ray_command = {"mode": "hsi", "hue": hue, "sat": sat, "intensity_percent": 100.0}
    ray_cache = f"c122-ray-h{hue}-s{sat}"
    tags = [str(c["tag"]) for c in candidates]
    if len(set(tags)) != len(tags):
        raise ValueError("C12-2 block candidate tags must be unique")

    captures: list[dict[str, Any]] = []

    def add_ray(position: str) -> None:
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-ray-guide12-c122-h{hue}-s{sat}"
                f"-block{block_index}-{position}"
            ),
            "source_id": "ray",
            "state_id": f"C122_H{hue}_S{sat}_B{block_index}_{position.upper()}",
            "role": "ray_reference",
            "command": dict(ray_command),
            "exact_command_hash": thermal.canonical_sha256(ray_command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": len(captures) + 1,
            "nominal_shutter": resolved_ray_shutter,
            "exposure_cache_key": ray_cache,
            "strip_zero_required": True,
            "ray_reference_position": position,
            "c122_request": request, "c122_block": block_index,
        })

    add_ray("raybefore")
    for candidate in candidates:
        command = {k: int(v) for k, v in candidate["command"].items()}
        if len(command) != 5 or sorted(command) != ["b", "cw", "g", "r", "ww"]:
            raise ValueError(f"C12-2 strip candidate needs all five channels: {command}")
        if max(command.values()) > FULLSCALE or min(command.values()) < 0:
            raise ValueError(f"C12-2 strip candidate out of code range: {command}")
        shutter = str(
            candidate.get("strip_shutter")
            or c122_initial_strip_shutter(command)
        )
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-strip-guide12-c122-h{hue}-s{sat}"
                f"-block{block_index}-{candidate['tag']}"
            ),
            "source_id": "strip",
            "state_id": (
                f"C122_H{hue}_S{sat}_B{block_index}_C{len(captures)}_{candidate['tag']}"
            ),
            "role": "strip_candidate",
            "command": command,
            "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": len(captures) + 1,
            "nominal_shutter": shutter,
            "exposure_cache_key": f"{ray_cache}-{candidate['tag']}",
            "ray_zero_required": True,
            "candidate_tag": str(candidate["tag"]),
            "candidate_role": str(candidate.get("role", "candidate")),
            "c122_request": request, "c122_block": block_index,
            "c122_tag": str(candidate["tag"]),
            "c122_new_unique": bool(candidate.get("new_unique_command", True)),
            "c122_face_channels": sorted(
                str(c) for c in (candidate.get("face_channels") or
                                 (ch for ch in CHANNELS if command[ch] == 0))
            ),
        })
    add_ray("rayafter")

    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in captures
    }
    new_unique = sum(
        1 for c in candidates if c.get("new_unique_command", True)
    )
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C122_EXPERIMENT_ID,
        "variant": f"c12_2_color_solving_h{hue}_s{sat}_v1",
        "stage": f"GUIDE12-C12-2-H{hue}-S{sat}",
        "phase": "formal",
        "source": "guide12_c12_2_color_fullscale_solving_20261009",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "p6_node_brightness": {"path": "D:/rgbww-optimizer/guide12-c12/"
                                 "derived/p6-node-brightness.json"},
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_c122_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "ray_rule": (
                "exact P6 node-brightness anchors x 0.59 N2 factor, 9000 DN "
                "target, next faster stop (C12-1 rule; H120/S100->1/3200, "
                "H300/S100->1/1600, S0->1/6400 reproduce the frozen values)"
            ),
            "strip_rule": (
                "white-dominant tier 1/100 (W12-2 white-node anchor), "
                "RGB-dominant tier 1/400 (C1 fullscale anchor); later "
                "blocks predicted offline from the measured base frame, "
                "never widened in-run"
            ),
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0,
            "block_new_unique_commands": new_unique,
            "request_unique_command_cap": C122_UNIQUE_COMMAND_CAP,
            "request_unique_command_cap_expanded": C122_UNIQUE_COMMAND_CAP_EXPANDED,
            "request_face_cap": C122_FACE_CAP,
            "request_confirmations_required": C122_CONFIRMATIONS_REQUIRED,
        },
        "execution_authorization": {
            "schema": C122_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C122_EXPERIMENT_ID,
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
            "method": "guide12_c12_2_block_z_difference",
            "request": {"hue": hue, "sat": sat},
            "block_index": block_index,
            "primary_space": "z=(ln(R/G), ln(B/G)) block_06 four planes",
            "reference": "same-target Ray HSI bracket mean (before/after)",
            "product_gate": (
                "SAT>=25: Hue +/-2deg, SAT +/-2pp via offline inverse; "
                "S0: |dz| <= 0.01 per log ratio; plateau/void frames never "
                "feed slopes"
            ),
            "solver_scale_note": (
                "z scales 0.01 (S0) / 0.02 (S50/S100) weight the surrogate "
                "step only; they are an engineering allocation, not the "
                "product tolerance"
            ),
            "steady_claim": False,
        },
    }
