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
