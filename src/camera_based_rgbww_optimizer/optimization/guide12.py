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
