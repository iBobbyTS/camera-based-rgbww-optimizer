"""GUIDE12 N2 repeatability experiment: plans for the frozen §3.2 design.

Six fixed states (four white CCT/gm points plus two extreme fullscale color
commands), three separated sessions x two independent FAST paired cycles x
two sources (Ray, strip). Ray/strip order reverses between the two cycles of
a session and the starting order rotates across sessions. Session 1 carries
the adjacent bursts for three representative states (extra captures on the
same FAST state - no extra reset, dwell continues) and the all-off
environment diagnostics for the actual slowest strip class and the Ray class.

Design freeze: .agent-work/guide12/GUIDE12-N2-DESIGN-20261002.md (commands
frozen, matching bias allowed, no optimization inside N2).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide12 import (
    W12_FAST_DWELL_S,
    W12_PRECHECK_RAW_MAX_CEILING,
)
from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
    AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
)

N2_EXPERIMENT_ID = "GUIDE12_N2_REPEATABILITY_V1"
N2_AUTHORIZATION_SCHEMA = "direct_guide12_n2_repeatability_v1"
N2_VARIANT = "p7_td_c_n2_repeatability_v1"
N2_SESSIONS = 3
N2_CYCLES = 2
N2_BURST_EXTRA_CAPTURES = 2
N2_BURST_STEP_S = 20.0

# Ray CCT shutters: frozen W2 anchors (guide12.W12_RAY_SHUTTERS) with the
# documented same-CCT nearest-gm transfer for the two gm100 points that have
# no exact W2 anchor (1800/100 <- gm70, 5600/100 <- gm0; every 20000 anchor
# is 1/2500). gm is a second-order exposure effect; in-run FAST/rail gates
# remain the acceptance owner.
N2_RAY_CCT_SHUTTERS: dict[tuple[int, int], str] = {
    (1800, 100): "1/1600",
    (3200, 0): "1/2500",
    (5600, 100): "1/2500",
    (20000, 100): "1/2500",
}

# Strip shutters: batch-1 white line 1/100 default (20000/100 carries the
# heavy load -> 1/125 node override precedent), batch-1 measured stops for
# the two color extremes (fullscale_red 1/500, fullscale_blue 1/320).
N2_STRIP_SHUTTERS: dict[str, str] = {
    "white_1800_100": "1/100",
    "white_3200_0": "1/100",
    "white_5600_100": "1/100",
    "white_20000_100": "1/125",
    "color_red": "1/500",
    "color_blue": "1/320",
}

N2_STATES: tuple[dict[str, Any], ...] = (
    {
        "key": "white_1800_100", "kind": "white", "cct": 1800, "gm": 100,
        "strip_command": {"b": 0, "cw": 0, "g": 1197, "r": 4095, "ww": 0},
        "command_source": "guide11_w2_adopted",
        "ray_mode": "cct",
    },
    {
        "key": "white_3200_0", "kind": "white", "cct": 3200, "gm": 0,
        "strip_command": {"b": 839, "cw": 314, "g": 0, "r": 273, "ww": 4095},
        "command_source": "guide12_w12_adopted_E0.1675",
        "ray_mode": "cct",
    },
    {
        "key": "white_5600_100", "kind": "white", "cct": 5600, "gm": 100,
        "strip_command": {"b": 116, "cw": 4095, "g": 17, "r": 142, "ww": 428},
        "command_source": "guide11_w2_adopted",
        "ray_mode": "cct",
    },
    {
        "key": "white_20000_100", "kind": "white", "cct": 20000, "gm": 100,
        "strip_command": {"b": 3581, "cw": 0, "g": 4095, "r": 3214, "ww": 181},
        "command_source": "guide11_w2_adopted",
        "ray_mode": "cct",
    },
    {
        "key": "color_red", "kind": "color", "hue": 0,
        "strip_command": {"b": 0, "cw": 0, "g": 0, "r": 4095, "ww": 0},
        "command_source": "guide12_batch1_fullscale_red",
        "ray_mode": "hsi", "ray_hue": 0, "ray_sat": 100,
    },
    {
        "key": "color_blue", "kind": "color", "hue": 240,
        "strip_command": {"b": 4095, "cw": 0, "g": 0, "r": 0, "ww": 0},
        "command_source": "guide12_batch1_fullscale_blue",
        "ray_mode": "hsi", "ray_hue": 240, "ray_sat": 100,
    },
)

# Burst states (session 1 only): warm white, cool white, red extreme.
N2_BURST_STATE_KEYS = ("white_1800_100", "white_20000_100", "color_red")

# Ray HSI shutter ladder candidates (exposure-qualification budget, not
# science frames): bracketing the white-anchor order of magnitude.
N2_HSI_LADDER_STOPS = ("1/1000", "1/2000", "1/4000")


def _ray_command(state: Mapping[str, Any]) -> dict[str, Any]:
    if state["ray_mode"] == "hsi":
        return {
            "mode": "hsi", "hue": int(state["ray_hue"]),
            "sat": int(state["ray_sat"]), "intensity_percent": 100.0,
        }
    return {
        "mode": "cct", "cct": int(state["cct"]), "gm": int(state["gm"]),
        "intensity_percent": 100.0,
    }


def build_guide12_n2_session_plan(
    session_index: int,
    *,
    hsi_ray_shutters: Mapping[str, str] | None = None,
    strip_shutter_overrides: Mapping[str, str] | None = None,
    predicted_raw_max: Mapping[str, float] | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One N2 session: 6 states x 2 FAST paired cycles x 2 sources.

    Session 1 additionally carries the three-state adjacent bursts (extra
    captures on the same FAST state, dwell ladder, no extra reset) and the
    all-off environment pair for the slowest strip class and the Ray class.
    """
    if session_index not in (1, 2, 3):
        raise ValueError("GUIDE12 N2 defines exactly three sessions (1..3)")
    hsi = dict(hsi_ray_shutters or {})
    overrides = dict(strip_shutter_overrides or {})
    for state in N2_STATES:
        if state["ray_mode"] == "hsi":
            key = f"ray-hsi-h{state['ray_hue']}-s100"
            if key not in hsi:
                raise ValueError(
                    f"GUIDE12 N2 needs the ladder-frozen Ray HSI shutter {key}"
                )
    if predicted_raw_max is not None:
        for key, value in predicted_raw_max.items():
            if float(value) > W12_PRECHECK_RAW_MAX_CEILING:
                raise ValueError(
                    f"GUIDE12 N2 strip state {key} predicted raw max {value} DN "
                    f"exceeds the pre-check ceiling {W12_PRECHECK_RAW_MAX_CEILING}"
                )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    off_hash = thermal.canonical_sha256({"strip": "off", "ray": "off"})

    def add_ambient(position: str, shutter: str, slug: str) -> None:
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-ambient-alloff-{position}-{slug}"
                f"-s{session_index}"
            ),
            "source_id": "ambient", "state_id": "ambient",
            "command": None, "exact_command_hash": off_hash,
            "requested_elapsed_s": None, "timing_acceptance": None,
            "timing_status": "diagnostic_not_timed", "formal_measurement": False,
            "capture_role": "ambient", "ambient_position": position,
            "ambient_shutter_speed": shutter, "nominal_shutter": shutter,
            "isolation_gate_before": f"guide12_n2_alloff_{position}_{slug}_s{session_index}",
            "all_off_diagnostic": True,
        })

    if session_index == 1:
        add_ambient("start", "1/125", "1over125")
        add_ambient("start", "1/2500", "1over2500")

    for state in N2_STATES:
        strip_command = {k: int(v) for k, v in state["strip_command"].items()}
        ray = _ray_command(state)
        strip_shutter = str(overrides.get(state["key"]) or N2_STRIP_SHUTTERS[state["key"]])
        if state["ray_mode"] == "hsi":
            ray_shutter = hsi[f"ray-hsi-h{state['ray_hue']}-s100"]
            ray_cache = f"n2-ray-hsi-h{state['ray_hue']}-s100"
        else:
            ray_shutter = N2_RAY_CCT_SHUTTERS[(int(state["cct"]), int(state["gm"]))]
            ray_cache = f"n2-ray-white-{state['cct']}-gm{state['gm']}"
        strip_cache = f"n2-strip-{state['key']}"
        frozen[ray_cache] = ray_shutter
        frozen[strip_cache] = strip_shutter
        for cycle_index in (1, 2):
            burst_here = (
                session_index == 1 and cycle_index == 1
                and state["key"] in N2_BURST_STATE_KEYS
            )
            ray_first = (cycle_index + session_index) % 2 == 0
            order = ("ray", "strip") if ray_first else ("strip", "ray")
            for source_index, source in enumerate(order, start=1):
                command = ray if source == "ray" else strip_command
                shutter = ray_shutter if source == "ray" else strip_shutter
                cache_key = ray_cache if source == "ray" else strip_cache
                base = {
                    "capture_role": "formal", "formal_measurement": True,
                    "command": command,
                    "exact_command_hash": thermal.canonical_sha256(command),
                    "requested_elapsed_s": W12_FAST_DWELL_S,
                    "nominal_shutter": shutter,
                    "exposure_cache_key": cache_key,
                    "timing_acceptance": "observed_elapsed_record_only",
                    "strip_zero_required": source == "ray",
                    "ray_zero_required": source == "strip",
                    "session_index": len(captures) + 1,
                    "source_order": source_index,
                    "source_id": source,
                    "state_id": (
                        f"N2_S{session_index}_C{cycle_index}_{state['key']}"
                        f"_{source.upper()}"
                    ),
                    "role": f"n2_{state['key']}_s{session_index}_c{cycle_index}",
                    "n2_session_index": session_index,
                    "n2_cycle_index": cycle_index,
                    "n2_state_key": state["key"],
                }
                elapsed_list = [W12_FAST_DWELL_S]
                if burst_here:
                    elapsed_list.extend(
                        W12_FAST_DWELL_S + N2_BURST_STEP_S * (extra + 1)
                        for extra in range(N2_BURST_EXTRA_CAPTURES)
                    )
                for elapsed_index, elapsed in enumerate(elapsed_list):
                    step = dict(base)
                    step["requested_elapsed_s"] = elapsed
                    step["n2_burst_role"] = (
                        "burst_main" if burst_here and elapsed_index == 0
                        else f"burst_extra_{elapsed_index}" if burst_here
                        else "paired_cycle_main"
                    )
                    step["capture_id"] = (
                        f"{len(captures):03d}-{source}-guide12-n2"
                        f"-s{session_index}-{state['key']}-c{cycle_index}"
                        + (f"-b{elapsed_index}" if burst_here else "")
                    )
                    captures.append(step)

    if session_index == 1:
        add_ambient("end", "1/125", "1over125")
        add_ambient("end", "1/2500", "1over2500")

    main_frames = sum(
        1 for step in captures if step.get("capture_role") == "formal"
    )
    if session_index == 1:
        expected_main = 6 * 2 * 2 + len(N2_BURST_STATE_KEYS) * 2 * N2_BURST_EXTRA_CAPTURES
    else:
        expected_main = 6 * 2 * 2
    if main_frames != expected_main:
        raise ValueError(
            f"GUIDE12 N2 session {session_index} frame count {main_frames} "
            f"differs from the frozen design {expected_main}"
        )

    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": N2_EXPERIMENT_ID,
        "variant": N2_VARIANT,
        "stage": f"GUIDE12-N2-SESSION-{session_index}",
        "phase": "formal",
        "source": "guide12_n2_design_frozen_20261002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_n2_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": (
            AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC
            if session_index == 1 else AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        ),
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": main_frames,
            "diagnostic_cap": len(captures) - main_frames,
            "ambient_cap": len(captures) - main_frames,
            "physical_cr3_cap": len(captures),
            "setup_physical_cr3_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": N2_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": N2_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
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
            "method": "guide12_n2_repeatability_session",
            "session_index": session_index,
            "design": "guide12_n2_design_frozen_20261002",
            "states": [
                {
                    "key": state["key"], "kind": state["kind"],
                    "strip_command": dict(state["strip_command"]),
                    "command_source": state["command_source"],
                    "ray_command": _ray_command(state),
                }
                for state in N2_STATES
            ],
            "burst_states": list(N2_BURST_STATE_KEYS),
            "burst_extra_captures": N2_BURST_EXTRA_CAPTURES,
            "ray_shutter_provenance": {
                "white": "W2 frozen anchors; 1800/100<-gm70, 5600/100<-gm0, "
                         "20000/100<-all-gm 1/2500 (same-CCT nearest-gm transfer)",
                "hsi": "ladder-frozen per session (exposure-qualification budget)",
            },
            "predicted_raw_max": (
                {k: float(v) for k, v in (predicted_raw_max or {}).items()}
            ),
        },
    }


def build_guide12_n2_hsi_ladder_plan(
    *,
    hues: Sequence[int] = (0, 240),
    stops: Sequence[str] = N2_HSI_LADDER_STOPS,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Ray HSI shutter ladder for the two color states (qualification budget).

    Three stops per hue bracketing the white-anchor order of magnitude; the
    ladder frames are real FAST observations (formal timing identity); the
    selected stop is frozen into the session plan and the selection evidence
    is archived beside it. ``hues``/``stops`` narrow a retry to the states a
    prior ladder attempt could not cover (fail-closed observer gates stop
    the run at the first rejected frame).
    """
    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    for state in N2_STATES:
        if state["ray_mode"] != "hsi" or int(state["ray_hue"]) not in set(int(h) for h in hues):
            continue
        for stop in stops:
            cache_key = f"n2-ladder-ray-hsi-h{state['ray_hue']}-s100-{stop.replace('/', '')}"
            frozen[cache_key] = stop
            command = _ray_command(state)
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-ray-guide12-n2-ladder"
                    f"-h{state['ray_hue']}-s100-{stop.replace('/', '')}"
                ),
                "source_id": "ray",
                "state_id": f"N2_LADDER_H{state['ray_hue']}_{stop.replace('/', '')}",
                "role": "hsi_shutter_ladder",
                "command": command,
                "exact_command_hash": thermal.canonical_sha256(command),
                "requested_elapsed_s": W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": stop,
                "exposure_cache_key": cache_key,
                "strip_zero_required": True,
            })
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": N2_EXPERIMENT_ID,
        "variant": N2_VARIANT,
        "stage": "GUIDE12-N2-HSI-LADDER",
        "phase": "diagnostic",
        "source": "guide12_n2_design_frozen_20261002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_n2_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0,
            "ambient_cap": 0,
            "physical_cr3_cap": len(captures),
            "setup_physical_cr3_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": N2_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": N2_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
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
            "method": "guide12_n2_hsi_shutter_ladder",
            "design": "guide12_n2_design_frozen_20261002",
            "stops": [str(s) for s in stops],
            "hues": [int(h) for h in hues],
            "note": "diagnostics; selected stop frozen into the session plan",
        },
    }
