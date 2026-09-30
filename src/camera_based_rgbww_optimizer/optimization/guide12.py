"""GUIDE12 shared helpers: signed white errors, fullscale faces, secant fits.

GUIDE12 (2026-09-29) fixes three GUIDE11 accounting defects that these
helpers own going forward:

1. White-light errors are reported as SIGNED PHYSICAL-UNIT differences
   ``strip - reference`` with their tolerance and a separately-derived
   dimensionless absolute normalized error. A normalized gate value is never
   assigned into a physical-unit field again (the W8 defect).
2. Secant sensitivity uses A = u - u0 against B = r(u) - r(u0) with one
   frozen base observation, so an intercept in r(u) = a*u + b cannot leak
   into the recovered slope (the W2 defect).
3. Fullscale evidence is read from actual applied/read-back payloads; a
   nominal or planned max-4095 value never implies ``fullscale_actual``.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

WHITE_COMPONENTS = ("cct_K", "mired", "duv")


def signed_white_errors(
    strip_white_point: Mapping[str, float],
    reference_white_point: Mapping[str, float],
    tolerances: Mapping[str, float],
) -> dict[str, Any]:
    """Signed physical-unit white error of strip minus reference.

    Returns per-component ``error_signed`` (physical unit), ``tolerance`` and
    ``abs_normalized_error`` (|signed| / tolerance), plus ``E_normalized`` =
    max over components. The sign convention is recorded so downstream
    reports cannot silently flip strip-minus-Ray into Ray-minus-strip.
    """
    components: dict[str, dict[str, float]] = {}
    for name in WHITE_COMPONENTS:
        tolerance = float(tolerances[name])
        signed = float(strip_white_point[name]) - float(reference_white_point[name])
        components[name] = {
            "error_signed": signed,
            "tolerance": tolerance,
            "abs_normalized_error": abs(signed) / tolerance,
        }
    return {
        "components": components,
        "E_normalized": max(c["abs_normalized_error"] for c in components.values()),
        "sign_convention": "strip_minus_reference",
    }


CHANNEL_ALIASES = {
    "cold_white": "cold_white", "cw": "cold_white",
    "warm_white": "warm_white", "ww": "warm_white",
    "red": "red", "r": "red",
    "green": "green", "g": "green",
    "blue": "blue", "b": "blue",
}


def _five_channel_payload(
    payload: Mapping[str, int] | None,
) -> dict[str, int] | None:
    if payload is None:
        return None
    mapped = {
        CHANNEL_ALIASES[str(key).lower()]: int(value)
        for key, value in payload.items()
        if str(key).lower() in CHANNEL_ALIASES
    }
    return mapped or None


def fullscale_evidence(
    requested_payload: Mapping[str, int] | None,
    actual_payload: Mapping[str, int] | None,
) -> dict[str, Any]:
    """Fullscale accounting for one strip command application.

    ``actual_payload`` must come from the device snapshot after apply or from
    readback (long channel names or the plan-step short names); when it is
    missing the actual status is ``unknown`` and never defaults to
    fullscale. The user-defined fullscale contract is max(actual PWM) == 4095
    over the five physical channels.
    """
    channels = ("cold_white", "warm_white", "red", "green", "blue")
    requested = _five_channel_payload(requested_payload)
    actual = _five_channel_payload(actual_payload)
    actual_max = None if actual is None else max(actual.values())
    return {
        "requested_payload": requested,
        "actual_payload": actual,
        "requested_max": None if requested is None else max(requested.values()),
        "actual_max": actual_max,
        "requested_max_is_4095": bool(requested is not None and max(requested.values()) >= 4095),
        "fullscale_actual": None if actual_max is None else bool(actual_max >= 4095),
        "fullscale_actual_source": None if actual is None else "applied_or_readback_payload",
        "actual_channels_at_4095": [] if actual is None else [
            name for name in channels if actual[name] >= 4095
        ],
        "contract": "max_actual_pwm_equals_4095_user_defined_fullscale",
    }


def secant_sensitivity_fit(
    observations: Sequence[Mapping[str, Any]],
    *,
    channel_names: Sequence[str],
    base_observation: Mapping[str, Any],
    output_names: Sequence[str],
) -> dict[str, Any]:
    """Least-squares secant fit with the GUIDE12 differenced algebra.

    ``observations`` carry ``command`` (channel -> code) and ``response``
    (output name -> value); ``base_observation`` is the frozen base. Rows are
    A = u_i - u0, B = r(u_i) - r(u0); repeats of the base command are counted
    and excluded. Returns the sensitivity matrix, rank diagnostics, singular
    values, and the base response so callers can record them.
    """
    import numpy as np

    names = list(channel_names)
    base_cmd = np.array([float(base_observation["command"][n]) for n in names])
    base_response = np.array(
        [float(base_observation["response"][o]) for o in output_names]
    )
    a_rows: list[list[float]] = []
    b_rows: list[list[float]] = []
    base_repeats = 0
    for obs in observations:
        if obs is base_observation:
            continue
        cmd = np.array([float(obs["command"][n]) for n in names])
        if np.allclose(cmd, base_cmd):
            base_repeats += 1
            continue
        response = np.array([float(obs["response"][o]) for o in output_names])
        a_rows.append(cmd - base_cmd)
        b_rows.append(response - base_response)
    fit: dict[str, Any] = {
        "base_command": {n: int(base_cmd[i]) for i, n in enumerate(names)},
        "base_response": {o: float(base_response[i]) for i, o in enumerate(output_names)},
        "base_repeats_same_command": base_repeats,
        "row_count": len(a_rows),
    }
    if not a_rows:
        return {**fit, "status": "no_direction_rows"}
    a_matrix = np.asarray(a_rows)
    b_matrix = np.asarray(b_rows)
    sensitivity, *_ = np.linalg.lstsq(a_matrix, b_matrix, rcond=None)
    return {
        **fit,
        "status": "fitted",
        "sensitivity": sensitivity.tolist(),
        "command_delta_rank": int(np.linalg.matrix_rank(a_matrix)),
        "sensitivity_rank": int(np.linalg.matrix_rank(sensitivity)),
        "command_delta_singular_values": [
            float(v) for v in np.linalg.svd(a_matrix, compute_uv=False)
        ],
        "algebra": "A=u-u0, B=r(u)-r(u0), single frozen base observation",
    }

# ---------------------------------------------------------------------------
# GUIDE12 batch 1: native exposure qualification + all-off environment frames
# ---------------------------------------------------------------------------

BATCH1_AUTHORIZATION_SCHEMA = "direct_guide12_batch1_exposure_all_off_v1"
BATCH1_VARIANT = "guide12-batch1-exposure-all-off"
BATCH1_STATE_DWELL_S = 120

# Frozen qualification ladders: fastest stop first so the very first frame of
# each class is the safest predicted exposure, then adjacent stops. The white
# class uses the W2-adopted 2300/100 command (actual readback 0/4095/1965/312/0).
BATCH1_CLASSES: tuple[dict[str, Any], ...] = (
    {
        "state_id": "B1_R4095",
        "label": "fullscale_red",
        "command": {"cw": 0, "ww": 0, "r": 4095, "g": 0, "b": 0},
        "ladder": ("1/500", "1/400", "1/320"),
    },
    {
        "state_id": "B1_B4095",
        "label": "fullscale_blue",
        "command": {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 4095},
        "ladder": ("1/500", "1/400", "1/320"),
    },
    {
        "state_id": "B1_WHITE2300",
        "label": "high_white_load",
        "command": {"cw": 0, "ww": 4095, "r": 1965, "g": 312, "b": 0},
        "ladder": ("1/10", "1/8", "1/6"),
    },
)
BATCH1_ALL_OFF_SHUTTERS = ("1/400", "1/8")


def build_guide12_batch1_plan() -> dict[str, Any]:
    """Assemble the frozen GUIDE12 batch-1 execution plan.

    13 physical CR3 frames: 2 start all-off + 3 classes x 3-stop ladders +
    2 end all-off. Ladder frames are diagnostics at frozen shutters sharing
    one command application per class; all-off frames record the ambient+dark
    term per exposure class without any subtraction.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
    )

    captures: list[dict[str, Any]] = []
    off_hash = thermal.canonical_sha256({"strip": "off", "ray": "off"})

    def add_ambient(position: str, shutter: str) -> None:
        slug = shutter.replace("/", "over")
        captures.append({
            "capture_id": f"{len(captures):03d}-ambient-alloff-{position}-{slug}",
            "source_id": "ambient", "state_id": "ambient",
            "command": None, "exact_command_hash": off_hash,
            "requested_elapsed_s": None, "timing_acceptance": None,
            "timing_status": "diagnostic_not_timed", "formal_measurement": False,
            "capture_role": "ambient", "ambient_position": position,
            "ambient_shutter_speed": shutter, "nominal_shutter": shutter,
            "isolation_gate_before": f"guide12_batch1_alloff_{position}_{slug}",
            "all_off_diagnostic": True,
        })

    for shutter in BATCH1_ALL_OFF_SHUTTERS:
        add_ambient("start", shutter)
    for klass in BATCH1_CLASSES:
        command = dict(klass["command"])
        command_hash = thermal.canonical_sha256(command)
        for index, shutter in enumerate(klass["ladder"]):
            slug = shutter.replace("/", "over")
            captures.append({
                "capture_id": f"{len(captures):03d}-strip-{klass['label']}-{slug}",
                "source_id": "strip", "state_id": klass["state_id"],
                "command": command, "exact_command_hash": command_hash,
                "requested_elapsed_s": 120 + 15 * index,
                "timing_acceptance": "diagnostic_not_formal",
                "timing_status": "diagnostic_not_timed",
                "formal_measurement": False, "capture_role": "diagnostic",
                "nominal_shutter": shutter,
                "exposure_cache_key": f"guide12-b1-{klass['label']}-{slug}",
                "ray_zero_required": True,
                "ladder_class": klass["label"], "ladder_index": index,
            })
    for shutter in BATCH1_ALL_OFF_SHUTTERS:
        add_ambient("end", shutter)

    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in captures
        if step.get("exposure_cache_key") is not None
    }
    ambient_count = sum(1 for step in captures if step["capture_role"] == "ambient")
    ladder_count = len(captures) - ambient_count
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": thermal.GUIDE12_BATCH1_EXPERIMENT_ID,
        "variant": BATCH1_VARIANT,
        "stage": "GUIDE12-BATCH1-EXPOSURE-ALL-OFF",
        "phase": "diagnostic",
        "source": "guide12_batch1_frozen_ladder",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_batch1_apply_D120",
        "state_dwell_s": BATCH1_STATE_DWELL_S,
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": 0,
            "diagnostic_cap": ladder_count,
            "ambient_cap": ambient_count,
            "physical_cr3_cap": len(captures),
            "setup_physical_cr3_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": BATCH1_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": thermal.GUIDE12_BATCH1_EXPERIMENT_ID,
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
            "method": "guide12_native_exposure_qualification_with_all_off",
            "classes": [
                {"label": k["label"], "state_id": k["state_id"],
                 "command": dict(k["command"]), "ladder": list(k["ladder"])}
                for k in BATCH1_CLASSES
            ],
            "all_off_shutters": list(BATCH1_ALL_OFF_SHUTTERS),
            "rail_rule": (
                "plane disqualified by near_white_rail_fraction > 0.05 or "
                "white_rail_plateau at effective_white_level - 2 DN; "
                "qualification requires adjacent-stop exposure-normalized "
                "consistency of the main planes"
            ),
            "selected_member": "faster",
            "qualification_frames_not_model_acceptance": True,
            "no_ambient_subtraction": True,
            "steady_claim": False,
        },
        "cleanup": {
            "python_finally": "required",
            "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
    }


def build_guide12_batch1_white_followup_plan() -> dict[str, Any]:
    """One-stop reverse recheck for the railed white-load class.

    formal-b1 found the 2300/100 white command pins every block plane at
    16382 through 1/10..1/6 (about 2x the W2-era block signal at the same
    readback command). The frozen ladder rule allows one reverse-direction
    stop: 1/20 is predicted to land near 9600 DN. No ambient frames, so the
    plan runs under the legacy unsubtracted_no_ambient policy.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    klass = BATCH1_CLASSES[2]
    command = dict(klass["command"])
    shutter = "1/20"
    slug = shutter.replace("/", "over")
    captures = [{
        "capture_id": f"000-strip-{klass['label']}-reverse-{slug}",
        "source_id": "strip", "state_id": klass["state_id"],
        "command": command, "exact_command_hash": thermal.canonical_sha256(command),
        "requested_elapsed_s": 120,
        "timing_acceptance": "diagnostic_not_formal",
        "timing_status": "diagnostic_not_timed",
        "formal_measurement": False, "capture_role": "diagnostic",
        "nominal_shutter": shutter,
        "exposure_cache_key": f"guide12-b1-{klass['label']}-reverse-{slug}",
        "ray_zero_required": True,
        "ladder_class": klass["label"], "ladder_index": 3,
    }]
    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in captures
    }
    plan = build_guide12_batch1_plan()
    plan.update({
        "guide_experiment_id": None,
        "variant": f"{BATCH1_VARIANT}-white-reverse-recheck",
        "stage": "GUIDE12-BATCH1-WHITE-REVERSE-RECHECK",
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_resolution": "guide12_batch1_reverse_D120",
        "native_raw_ambient_policy": "unsubtracted_no_ambient",
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": 0, "diagnostic_cap": 1, "ambient_cap": 0,
            "physical_cr3_cap": 1, "setup_physical_cr3_cap": 0, "retry": 0,
        },
        "execution_authorization": {
            "schema": BATCH1_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": thermal.TD_C,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "analysis_contract": {
            **dict(plan["analysis_contract"]),
            "method": "guide12_white_reverse_recheck",
            "reverse_recheck_of": "formal-b1-20260929-r1 high_white_load",
            "predicted_code_dn": 9600,
        },
    })
    return plan


def build_guide12_batch1_white_corrected_arm_plan() -> dict[str, Any]:
    """Corrected white-load ladder arm at the W2-era white-line anchor.

    formal-b1 anchored the white class on the C1 color tier (1/8); the W2
    white line actually ran this command at 1/80 (recorded 0.0125 s, block
    max ~12042). The railed 1/10..1/20 stops were an anchor error, not a
    brightness change. Two stops at the correct anchor complete the class
    within its 6-frame cap (4 used + 2).
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    klass = BATCH1_CLASSES[2]
    command = dict(klass["command"])
    captures = []
    for index, shutter in enumerate(("1/100", "1/80")):
        slug = shutter.replace("/", "over")
        captures.append({
            "capture_id": f"{index:03d}-strip-{klass['label']}-corrected-{slug}",
            "source_id": "strip", "state_id": klass["state_id"],
            "command": command, "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": 120 + 15 * index,
            "timing_acceptance": "diagnostic_not_formal",
            "timing_status": "diagnostic_not_timed",
            "formal_measurement": False, "capture_role": "diagnostic",
            "nominal_shutter": shutter,
            "exposure_cache_key": f"guide12-b1-{klass['label']}-corrected-{slug}",
            "ray_zero_required": True,
            "ladder_class": klass["label"], "ladder_index": 4 + index,
        })
    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in captures
    }
    plan = build_guide12_batch1_plan()
    plan.update({
        "guide_experiment_id": None,
        "variant": f"{BATCH1_VARIANT}-white-corrected-arm",
        "stage": "GUIDE12-BATCH1-WHITE-CORRECTED-ARM",
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_resolution": "guide12_batch1_corrected_D120",
        "native_raw_ambient_policy": "unsubtracted_no_ambient",
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": 0, "diagnostic_cap": 2, "ambient_cap": 0,
            "physical_cr3_cap": 2, "setup_physical_cr3_cap": 0, "retry": 0,
        },
        "execution_authorization": {
            "schema": BATCH1_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": thermal.TD_C,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "analysis_contract": {
            **dict(plan["analysis_contract"]),
            "method": "guide12_white_corrected_arm",
            "corrects": "formal-b1 white anchor error (C1 color tier 1/8 vs white-line 1/80)",
            "w2_anchor_evidence": (
                "guide11-w2 formal-w2-20260922 capture 017: recorded 0.0125 s, "
                "block max 12042 at the same readback command"
            ),
        },
    })
    return plan


# ---------------------------------------------------------------------------
# GUIDE12 W12-1: fullscale-face bounded solving on a frozen open queue
# ---------------------------------------------------------------------------

W12_EXPERIMENT_ID = "GUIDE12_W12_FULLSCALE_BOUNDED_V1"
W12_AUTHORIZATION_SCHEMA = "direct_guide12_w12_fullscale_bounded_v1"
W12_VARIANT = "guide12-w12-fullscale-bounded"
W12_TOLERANCES = {"cct_K": 25.0, "mired": 1.0, "duv": 0.0005}
# Batch-1 white-line qualification: fullscale white commands run 1/100 with
# ~7257 DN p99 margin; 1/80 remains the secondary confirmation stop only.
W12_STRIP_SHUTTER = "1/100"
W12_STRIP_SHUTTER_SECONDARY = "1/80"
# Ray CCT reference shutters frozen from the GUIDE11 W2 experiment spec
# (formal-w2-20260922 frozen_shutters ray-white-* table); Ray targets are
# unchanged, so the measured W2 anchors carry over without re-derivation.
W12_RAY_SHUTTERS: dict[str, str] = {
    "ray-white-10000-gm70": "1/3200",
    "ray-white-14000-gm0": "1/2500",
    "ray-white-14000-gm130": "1/3200",
    "ray-white-14000-gm200": "1/3200",
    "ray-white-1800-gm70": "1/1600",
    "ray-white-2000-gm100": "1/2000",
    "ray-white-2000-gm200": "1/2000",
    "ray-white-2000-gm70": "1/2000",
    "ray-white-20000-gm0": "1/2500",
    "ray-white-20000-gm130": "1/2500",
    "ray-white-20000-gm200": "1/2500",
    "ray-white-20000-gm70": "1/2500",
    "ray-white-2300-gm100": "1/2500",
    "ray-white-2300-gm130": "1/2500",
    "ray-white-2300-gm200": "1/2500",
    "ray-white-2700-gm100": "1/2500",
    "ray-white-3200-gm0": "1/2500",
    "ray-white-3200-gm70": "1/2500",
    "ray-white-3800-gm0": "1/2500",
    "ray-white-4500-gm70": "1/3200",
    "ray-white-5600-gm0": "1/2500",
    "ray-white-6500-gm0": "1/2500",
    "ray-white-8000-gm0": "1/2500",
    "ray-white-8000-gm130": "1/3200",
    "ray-white-8000-gm70": "1/3200",
}
W12_PASS_E = 1.0
W12_MAX_NODE_COUNT = 30
W12_UNIQUE_COMMAND_CAP = 8
W12_UNIQUE_COMMAND_EXPANDED_CAP = 12
W12_MAX_STEP_CODES = 768.0
W12_CANDIDATES_PER_BLOCK = 4
W12_FAST_RESET_S = 600
W12_FAST_DWELL_S = 120
W12_CLOSED_POINTS = ((1800, 100),)
W12_PRIORITY_FIRST = (3200, 0)
W12_FLIPPED_NODES = ((1800, 70), (2000, 100))
W12_COLD_END_MAX_CCT = 2700
# Probe-channel rank on a white fullscale face: the white channel opposite
# the face carries the purest temperature response, blue the secondary cooling
# plus duv response, red the warming/duv axis; green is mostly luminance and
# is probed last. Ties break toward the smaller current code (more headroom).
W12_PROBE_CHANNEL_RANK = {
    "cold_white": 0, "warm_white": 0, "blue": 1, "red": 2, "green": 3,
}
# Pre-freeze the offline exposure pre-check ceiling for candidate commands at
# the frozen strip shutter; the in-run near-white-rail gate stays the owner.
W12_PRECHECK_RAW_MAX_CEILING = 15000.0

_LONG_CHANNELS = ("cold_white", "warm_white", "red", "green", "blue")
_SHORT_BY_LONG = {
    "cold_white": "cw", "warm_white": "ww", "red": "r", "green": "g", "blue": "b",
}


def _long_command(command: Mapping[str, int]) -> dict[str, int]:
    mapped = _five_channel_payload(command)
    if mapped is None:
        raise ValueError("GUIDE12 W12 command lacks five-channel PWM payload")
    missing = [c for c in _LONG_CHANNELS if c not in mapped]
    if missing:
        raise ValueError(f"GUIDE12 W12 command missing channels: {missing}")
    return {c: int(mapped[c]) for c in _LONG_CHANNELS}


def guide12_w12_face_channels(command: Mapping[str, int]) -> list[str]:
    """Channels pinned at the user-defined fullscale code on this command."""
    long_command = _long_command(command)
    return [c for c in _LONG_CHANNELS if long_command[c] >= 4095]


def build_guide12_w12_open_queue(fresh_pairing: Mapping[str, Any]) -> dict[str, Any]:
    """Frozen W12-1 open queue from the fresh same-candidate pairing audit.

    Open nodes are the audited grid nodes whose best paired observation still
    exceeds the full-tolerance gate E>1 versus its own same-run Ray reference.
    Unchanged qualified nodes stay out (W12-2 handles their independent
    confirmation); 1800/100 remains the closed point. Order: the named large
    residual 3200/0, the two flipped adopted nodes, remaining cold-end risk
    (cct<=2700), then everything else, both by descending E.
    """
    import copy as _copy

    open_rows: list[dict[str, Any]] = []
    pass_rows: list[dict[str, Any]] = []
    for node in fresh_pairing.get("nodes", ()):
        key = (int(node["cct"]), int(node["gm"]))
        if key in W12_CLOSED_POINTS:
            continue
        pairs = [p for p in node.get("pairs", ()) if p.get("E_vs_fresh_ray") is not None]
        if not pairs:
            continue
        best = min(pairs, key=lambda p: float(p["E_vs_fresh_ray"]))
        error_e = float(best["E_vs_fresh_ray"])
        row = {
            "cct": key[0], "gm": key[1],
            "E_vs_fresh_ray": error_e,
            "base_command": dict(best["command"]),
            "base_capture_id": best.get("strip_capture_id"),
            "fresh_ray_capture_id": best.get("ray_capture_id"),
            "fresh_ray_white_point": dict(best["fresh_ray_white_point"]),
            "signed_vs_fresh_ray": _copy.deepcopy(best["signed_vs_fresh_ray"]),
            "face_channels": guide12_w12_face_channels(best["command"]),
        }
        if error_e <= W12_PASS_E:
            pass_rows.append({k: row[k] for k in ("cct", "gm", "E_vs_fresh_ray")})
        else:
            open_rows.append(row)

    def order_key(row: Mapping[str, Any]) -> tuple[int, int, float]:
        key = (int(row["cct"]), int(row["gm"]))
        if key == W12_PRIORITY_FIRST:
            return (0, 0, -float(row["E_vs_fresh_ray"]))
        if key in W12_FLIPPED_NODES:
            return (1, W12_FLIPPED_NODES.index(key), -float(row["E_vs_fresh_ray"]))
        if int(row["cct"]) <= W12_COLD_END_MAX_CCT:
            return (2, 0, -float(row["E_vs_fresh_ray"]))
        return (3, 0, -float(row["E_vs_fresh_ray"]))

    open_rows.sort(key=order_key)
    if len(open_rows) > W12_MAX_NODE_COUNT:
        raise ValueError(
            f"GUIDE12 W12 open queue {len(open_rows)} nodes exceeds the frozen "
            f"stage budget {W12_MAX_NODE_COUNT}"
        )
    return {
        "schema": "guide12_w12_open_queue_v1",
        "source_schema": fresh_pairing.get("schema"),
        "pass_threshold_E": W12_PASS_E,
        "closed_points": [list(point) for point in W12_CLOSED_POINTS],
        "open_node_count": len(open_rows),
        "stage_node_budget": W12_MAX_NODE_COUNT,
        "unique_command_cap": W12_UNIQUE_COMMAND_CAP,
        "unique_command_expanded_cap": W12_UNIQUE_COMMAND_EXPANDED_CAP,
        "max_step_codes": W12_MAX_STEP_CODES,
        "candidates_per_block": W12_CANDIDATES_PER_BLOCK,
        "order_rule": (
            "3200/0 first, then flipped adopted nodes 1800/70 and 2000/100, "
            "then cold-end risk cct<=2700, then remaining; groups 2-3 by "
            "descending E_vs_fresh_ray"
        ),
        "unchanged_qualified_nodes": pass_rows,
        "nodes": open_rows,
    }


def guide12_w12_probe_channels(command: Mapping[str, int]) -> list[str]:
    """Three non-face probe channels, most chromatic leverage first."""
    long_command = _long_command(command)
    locked = set(guide12_w12_face_channels(long_command))
    ranked = [
        c for c in _LONG_CHANNELS
        if c not in locked and long_command[c] < 4095
    ]
    ranked.sort(key=lambda c: (W12_PROBE_CHANNEL_RANK[c], float(long_command[c])))
    if len(ranked) < 2:
        raise ValueError(
            "GUIDE12 W12 face leaves fewer than two probe directions: "
            f"{dict(long_command)}"
        )
    return ranked[:3]


def guide12_w12_probe_candidates(
    base_command: Mapping[str, int],
) -> list[dict[str, Any]]:
    """Frozen first-block candidate list: base repeat plus single-axis probes.

    The base repeat re-anchors the historical command inside the current block
    (it is not a new unique command); each probe steps one non-face channel by
    min(768, headroom) so the block-local secants give clean axis directions.
    """
    long_command = _long_command(base_command)
    candidates: list[dict[str, Any]] = [{
        "tag": "u0_repeat",
        "command": {_SHORT_BY_LONG[c]: long_command[c] for c in _LONG_CHANNELS},
        "role": "base_repeat",
        "new_unique_command": False,
    }]
    for channel in guide12_w12_probe_channels(long_command):
        step = min(W12_MAX_STEP_CODES, float(4095 - long_command[channel]))
        probed = dict(long_command)
        probed[channel] = int(long_command[channel] + step)
        candidates.append({
            "tag": f"probe_{_SHORT_BY_LONG[channel]}",
            "command": {_SHORT_BY_LONG[c]: probed[c] for c in _LONG_CHANNELS},
            "role": "single_axis_probe",
            "probe_channel": channel,
            "probe_step_codes": int(step),
            "new_unique_command": True,
        })
    if len(candidates) > W12_CANDIDATES_PER_BLOCK:
        raise ValueError("GUIDE12 W12 probe block exceeds the per-block candidate cap")
    return candidates


def solve_guide12_w12_face_step(
    base_command: Mapping[str, int],
    base_error_normalized: Mapping[str, float],
    sensitivity_normalized: Mapping[str, Mapping[str, float]],
    *,
    face_channels: Sequence[str],
    max_step_codes: float = W12_MAX_STEP_CODES,
    scale: float = 1.0,
) -> dict[str, Any]:
    """Box-constrained step on one fullscale face (global optimum, no clip).

    ``base_error_normalized`` is the signed strip-minus-reference error in
    tolerance units for cct_K/mired/duv; ``sensitivity_normalized`` maps each
    output to per-channel slopes in the same units. The surrogate solve runs
    in the (mired, duv) subspace because K/mired along one temperature
    direction are not independent ranks; cct_K stays in the recorded
    prediction and the measured full-tolerance gate. Face channels stay
    pinned (lower == upper == 0); every other channel respects [0, 4095] and
    the per-step cap. The step comes from the shared active-set-enumerating
    bounded least-squares owner, never an unconstrained solve with
    per-channel clipping afterwards.
    """
    import numpy as np

    from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
        solve_box_constrained_least_squares,
    )

    if not 0.0 < scale <= 1.0:
        raise ValueError("GUIDE12 W12 step scale must be in (0, 1]")
    long_base = _long_command(base_command)
    locked = {str(c) for c in face_channels}
    unknown = locked - set(_LONG_CHANNELS)
    if unknown:
        raise ValueError(f"GUIDE12 W12 face names unknown channels: {sorted(unknown)}")
    outputs = ("cct_K", "mired", "duv")
    sensitivity = np.array([
        [float(sensitivity_normalized[o][c]) for c in _LONG_CHANNELS]
        for o in outputs
    ])
    base_error = np.array([float(base_error_normalized[o]) for o in outputs])
    solve_rows = (1, 2)  # mired, duv subspace
    lower = np.array([
        max(-float(long_base[c]), -max_step_codes) if c not in locked else 0.0
        for c in _LONG_CHANNELS
    ])
    upper = np.array([
        min(float(4095 - long_base[c]), max_step_codes) if c not in locked else 0.0
        for c in _LONG_CHANNELS
    ])
    if np.any(lower > upper):
        raise ValueError("GUIDE12 W12 face leaves an infeasible step box")
    matrix = sensitivity[np.ix_(list(solve_rows), list(range(len(_LONG_CHANNELS))))]
    delta = np.asarray(
        solve_box_constrained_least_squares(
            matrix, -base_error[list(solve_rows)], lower, upper,
        ),
        dtype=float,
    ) * scale
    # Integer codes: round to nearest, then clamp back into the box (all box
    # edges are integer-valued, so clamping only binds where it must).
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
    predicted_error = {
        name: float(predicted[index]) for index, name in enumerate(outputs)
    }
    at_bound = [
        _SHORT_BY_LONG[_LONG_CHANNELS[i]]
        for i in range(len(_LONG_CHANNELS))
        if _LONG_CHANNELS[i] not in locked and (
            abs(delta[i] - lower[i]) <= 1e-9 or abs(delta[i] - upper[i]) <= 1e-9
        )
    ]
    return {
        "command": codes,
        "delta": final_delta,
        "scale": scale,
        "active_bound_channels": at_bound,
        "predicted_error_normalized": predicted_error,
        "predicted_E": max(abs(v) for v in predicted_error.values()),
        "solved_subspace": ["mired", "duv"],
        "k_mired_note": (
            "cct_K and mired along one temperature direction are not "
            "independent ranks; the surrogate solve uses mired only"
        ),
        "method": "box_constrained_least_squares_active_set_enumeration",
        "surrogate": True,
        "final_selection_requires_measured_gate": True,
        "face_channels": sorted(_SHORT_BY_LONG[c] for c in locked),
    }


def build_guide12_w12_block_plan(
    node: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    *,
    block_index: int,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
    predicted_raw_max: Mapping[str, float] | None = None,
    command_budget: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """One W12-1 local block: Ray before, strip candidates, Ray after.

    Every observation is its own FAST state (unique state_id -> independent
    off600 reset, exact command, 120 s dwell). Strip candidates use the
    batch-1 white-line anchor 1/100; Ray references reuse the frozen W2
    per-(cct, gm) shutter table.
    """
    import copy

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    cct, gm = int(node["cct"]), int(node["gm"])
    if not 1 <= len(candidates) <= W12_CANDIDATES_PER_BLOCK:
        raise ValueError(
            "GUIDE12 W12 block needs 1..4 strip candidates, got "
            f"{len(candidates)}"
        )
    ray_key = f"ray-white-{cct}-gm{gm}"
    if ray_key not in W12_RAY_SHUTTERS:
        raise ValueError(f"GUIDE12 W12 lacks a frozen Ray shutter for {ray_key}")
    ray_command = {
        "cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct",
    }
    strip_cache_key = f"guide12-w12-strip-white-{cct}-gm{gm}"
    tags = [str(c["tag"]) for c in candidates]
    if len(set(tags)) != len(tags):
        raise ValueError("GUIDE12 W12 block candidate tags must be unique")

    captures: list[dict[str, Any]] = []

    def add_ray(position: str) -> None:
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-ray-guide12-w12-cct{cct}-gm{gm}"
                f"-block{block_index}-{position}"
            ),
            "source_id": "ray",
            "state_id": f"CCT{cct}_GM{gm}_W12_B{block_index}_{position.upper()}",
            "role": "ray_reference",
            "command": dict(ray_command),
            "exact_command_hash": thermal.canonical_sha256(ray_command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": len(captures) + 1,
            "nominal_shutter": W12_RAY_SHUTTERS[ray_key],
            "exposure_cache_key": ray_key,
            "strip_zero_required": True,
            "ray_reference_position": position,
        })

    add_ray("raybefore")
    for candidate in candidates:
        command = {k: int(v) for k, v in candidate["command"].items()}
        if len(command) != 5 or sorted(command) != ["b", "cw", "g", "r", "ww"]:
            raise ValueError(
                f"GUIDE12 W12 strip candidate needs all five channels: {command}"
            )
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-strip-guide12-w12-cct{cct}-gm{gm}"
                f"-block{block_index}-{candidate['tag']}"
            ),
            "source_id": "strip",
            "state_id": (
                f"CCT{cct}_GM{gm}_W12_B{block_index}_C{len(captures)}_{candidate['tag']}"
            ),
            "role": "strip_candidate",
            "command": command,
            "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": len(captures) + 1,
            "nominal_shutter": W12_STRIP_SHUTTER,
            "exposure_cache_key": strip_cache_key,
            "ray_zero_required": True,
            "candidate_tag": str(candidate["tag"]),
            "candidate_role": str(candidate.get("role", "candidate")),
        })
    add_ray("rayafter")

    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in captures
    }
    new_unique = sum(1 for c in candidates if c.get("new_unique_command", True))
    ceiling_check = {}
    if predicted_raw_max is not None:
        for candidate in candidates:
            tag = str(candidate["tag"])
            if tag in predicted_raw_max:
                value = float(predicted_raw_max[tag])
                if value > W12_PRECHECK_RAW_MAX_CEILING:
                    raise ValueError(
                        f"GUIDE12 W12 candidate {tag} predicted raw max {value} DN "
                        f"exceeds the pre-check ceiling {W12_PRECHECK_RAW_MAX_CEILING}"
                    )
                ceiling_check[tag] = value
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W12_EXPERIMENT_ID,
        "variant": W12_VARIANT,
        "stage": "GUIDE12-W12-FULLSCALE-BOUNDED",
        "phase": "formal",
        "source": "guide12_w12_open_queue_frozen",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
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
        "timing_resolution": "guide12_w12_reset600_D120",
        "cold_proxy": W12_FAST_RESET_S,
        "cold_proxy_wait_s": W12_FAST_RESET_S,
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
            "schema": W12_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W12_EXPERIMENT_ID,
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
            "method": "guide12_w12_fullscale_face_bounded_local_block",
            "node": {"cct": cct, "gm": gm, "block_index": block_index},
            "base_command": dict(node.get("base_command", {})),
            "base_E_vs_fresh_ray": node.get("E_vs_fresh_ray"),
            "face_channels": list(node.get("face_channels", [])),
            "tolerances": dict(W12_TOLERANCES),
            "strip_candidates": [
                {
                    "tag": str(c["tag"]),
                    "command": {k: int(v) for k, v in c["command"].items()},
                    "role": str(c.get("role", "candidate")),
                    "new_unique_command": bool(c.get("new_unique_command", True)),
                }
                for c in candidates
            ],
            "new_unique_commands_in_block": new_unique,
            "command_budget": dict(command_budget or {}),
            "predicted_raw_max_at_strip_shutter": ceiling_check,
            "strip_shutter": W12_STRIP_SHUTTER,
            "strip_shutter_secondary": W12_STRIP_SHUTTER_SECONDARY,
            "ray_shutter_key": ray_key,
            "reference_rule": (
                "target reference is the per-component mean of the block's "
                "Ray before/after white points; the block is certifiable only "
                "if before/after agree within one product tolerance per "
                "component (25 K, 1.0 mired, 0.0005 Duv)"
            ),
            "objective": (
                "E=max(|e_K|/25, |e_mired|/1.0, |e_Duv|/0.0005), e=strip-block"
                "-Ray(mean of before/after); K/mired are one temperature "
                "direction, never independent ranks"
            ),
            "fast_protocol": "off600 -> exact command -> 120 s -> capture",
            "independent_reset_s": W12_FAST_RESET_S,
            "stop_names": [
                "qualified",
                "tested_neighborhood_practical_convergence",
                "bounded_search_exhausted",
            ],
            "steady_claim": False,
        },
        "cleanup": {
            "python_finally": "required",
            "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
    }
