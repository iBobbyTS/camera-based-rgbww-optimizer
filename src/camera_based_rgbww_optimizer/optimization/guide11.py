"""GUIDE11 shared white-control interpolation and N1 repeatability planning.

GUIDE11 corrections implemented here:

* One shared ``mired x GM`` piecewise-bilinear command interpolation that the
  runtime controller path and validation/holdout plans must both call. Nearest
  node copying is only a labelled diagnostic, never the runtime model.
* N1 (``11.GUIDE.md`` section 3.2): six fixed white states, two independent
  FAST paired cycles split across two operating sessions, balanced source
  order, and optional same-dwell burst captures that never add a reset.
"""

from __future__ import annotations

import copy
import math
from typing import Any, Mapping, Sequence


CHANNELS = ("cw", "ww", "r", "g", "b")

N1_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 100),
    (2300, 200),
    (3200, 0),
    (5600, 100),
    (14000, 0),
    (20000, 100),
)
N1_BURST_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 100),
    (5600, 100),
    (20000, 100),
)
N1_BURST_EXTRA_CAPTURES = 2
N1_BURST_STEP_S = 5.0

GUIDE11_N1_EXPERIMENT_ID = "GUIDE11_N1_WHITE_REPEATABLILITY_V1"
GUIDE11_N1_VARIANT = "guide11-n1-white-repeatability"
N1_AUTHORIZATION_SCHEMA = "direct_guide11_n1_repeatability_v1"


def _mired(cct: int) -> float:
    return 1_000_000.0 / float(cct)


def _lut_rows(lut: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in lut:
        command = {name: int(row["command"][name]) for name in CHANNELS}
        rows.append({
            "cct": int(row["cct"]),
            "gm": int(row["gm"]),
            "mired": _mired(int(row["cct"])),
            "command": command,
        })
    if not rows:
        raise ValueError("GUIDE11 interpolation requires a non-empty LUT")
    if len({(row["cct"], row["gm"]) for row in rows}) != len(rows):
        raise ValueError("GUIDE11 interpolation requires unique LUT nodes")
    return rows


def _channel_value(
    cct_rows: dict[float, list[dict[str, Any]]],
    gm_columns: Sequence[float],
    mired: float,
    gm: float,
    channel: str,
) -> float:
    mired_keys = sorted(cct_rows)
    if mired <= mired_keys[0]:
        m_lo = m_hi = mired_keys[0]
    elif mired >= mired_keys[-1]:
        m_lo = m_hi = mired_keys[-1]
    else:
        m_lo = max(key for key in mired_keys if key <= mired)
        m_hi = min(key for key in mired_keys if key >= mired)
    if gm <= gm_columns[0]:
        g_lo = g_hi = gm_columns[0]
    elif gm >= gm_columns[-1]:
        g_lo = g_hi = gm_columns[-1]
    else:
        g_lo = max(key for key in gm_columns if key <= gm)
        g_hi = min(key for key in gm_columns if key >= gm)

    def at(m_key: float, g_key: float) -> float:
        candidates = [
            row for row in cct_rows[m_key]
            if abs(row["gm"] - g_key) < 1e-9
        ]
        if not candidates:
            nearest = min(cct_rows[m_key], key=lambda row: abs(row["gm"] - g_key))
            raise ValueError(
                f"GUIDE11 interpolation grid lacks GM {g_key} at mired {m_key}; "
                f"nearest stored GM is {nearest['gm']}"
            )
        return float(candidates[0]["command"][channel])

    if m_lo == m_hi and g_lo == g_hi:
        return at(m_lo, g_lo)
    if m_lo == m_hi:
        frac_g = (gm - g_lo) / (g_hi - g_lo)
        return at(m_lo, g_lo) * (1.0 - frac_g) + at(m_lo, g_hi) * frac_g
    if g_lo == g_hi:
        frac_m = (mired - m_lo) / (m_hi - m_lo)
        return at(m_lo, g_lo) * (1.0 - frac_m) + at(m_hi, g_lo) * frac_m
    frac_m = (mired - m_lo) / (m_hi - m_lo)
    frac_g = (gm - g_lo) / (g_hi - g_lo)
    c00 = at(m_lo, g_lo)
    c01 = at(m_lo, g_hi)
    c10 = at(m_hi, g_lo)
    c11 = at(m_hi, g_hi)
    return (
        c00 * (1.0 - frac_m) * (1.0 - frac_g)
        + c01 * (1.0 - frac_m) * frac_g
        + c10 * frac_m * (1.0 - frac_g)
        + c11 * frac_m * frac_g
    )


def interpolate_white_command(
    lut: Sequence[Mapping[str, Any]], cct: int, gm: int,
) -> dict[str, Any]:
    """Shared runtime white command model: bilinear in mired x GM, clamped.

    This is the single interpolation owner for GUIDE11. The runtime
    controller, validation plans, and holdout plans must all route through
    this function so a request resolves to one identical command everywhere.
    Requests outside the LUT hull clamp to the hull edge; the response always
    reports whether the request was an exact stored node.
    """
    rows = _lut_rows(lut)
    gm_columns = sorted({float(row["gm"]) for row in rows})
    cct_rows: dict[float, list[dict[str, Any]]] = {}
    for row in rows:
        cct_rows.setdefault(row["mired"], []).append(row)
    mired = _mired(cct)
    gm_value = float(gm)
    hull_m = (min(cct_rows), max(cct_rows))
    hull_g = (gm_columns[0], gm_columns[-1])
    exact_node = any(
        row["cct"] == int(cct) and row["gm"] == int(gm) for row in rows
    )
    command = {}
    for channel in CHANNELS:
        value = _channel_value(cct_rows, gm_columns, mired, gm_value, channel)
        command[channel] = max(0, min(4095, int(round(value))))
    clamped = (
        not hull_m[0] - 1e-9 <= mired <= hull_m[1] + 1e-9
        or not hull_g[0] - 1e-9 <= gm_value <= hull_g[1] + 1e-9
    )
    return {
        "model": "guide11_mired_gm_bilinear_clamped_v1",
        "request": {"cct": int(cct), "gm": int(gm), "mired": mired},
        "command": command,
        "exact_node": exact_node,
        "clamped_to_hull": clamped,
        "nearest_node_command": None if exact_node else _nearest_node_command(rows, cct, gm),
    }


def _nearest_node_command(
    rows: Sequence[dict[str, Any]], cct: int, gm: int,
) -> dict[str, int]:
    mired = _mired(cct)
    nearest = min(
        rows,
        key=lambda row: abs(row["mired"] - mired) / max(mired, 1.0)
        + abs(row["gm"] - float(gm)) / 200.0,
    )
    return dict(nearest["command"])


def build_guide11_n1_session_plan(
    lut: Sequence[Mapping[str, Any]],
    frozen_shutters: Mapping[str, str],
    *,
    session_index: int,
    cycle_index: int,
) -> dict[str, Any]:
    """Build one N1 operating-session plan (one FAST paired cycle per point).

    Session 1 carries the bursts; session 2 is plain paired cycles so the six
    states span at least two operating periods with balanced Ray/strip order.
    """
    if session_index not in (1, 2) or cycle_index not in (1, 2):
        raise ValueError("GUIDE11 N1 defines exactly two sessions/cycles")
    import hashlib
    import json
    from datetime import datetime, timezone

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    rows = _lut_rows(lut)
    shutters = dict(frozen_shutters)

    def nearest_shutter(source: str, cct: int, gm: int) -> str:
        mired = _mired(cct)
        nearest = min(
            rows,
            key=lambda row: abs(row["mired"] - mired) / max(mired, 1.0)
            + abs(row["gm"] - float(gm)) / 200.0,
        )
        key = f"{source}-white-{nearest['cct']}-gm{nearest['gm']}"
        if key not in shutters:
            raise ValueError(f"GUIDE11 N1 lacks a qualified {source} shutter for {key}")
        return str(shutters[key])

    captures: list[dict[str, Any]] = []
    commands_audit: list[dict[str, Any]] = []
    session_plan_shutters: dict[str, str] = {}
    for point_index, (cct, gm) in enumerate(N1_POINTS):
        resolved = interpolate_white_command(lut, cct, gm)
        strip_command = resolved["command"]
        ray_command = {"mode": "cct", "cct": cct, "gm": gm, "intensity_percent": 100.0}
        commands_audit.append({
            "cct": cct,
            "gm": gm,
            "command_source": "w6_node_exact" if resolved["exact_node"] else "guide11_bilinear_interpolation",
            "exact_node": resolved["exact_node"],
            "clamped_to_hull": resolved["clamped_to_hull"],
            "strip_command": strip_command,
        })
        ray_first = (point_index + cycle_index) % 2 == 0
        order = ("ray", "strip") if ray_first else ("strip", "ray")
        burst_here = session_index == 1 and (cct, gm) in N1_BURST_POINTS
        for source_index, source in enumerate(order, start=1):
            command = ray_command if source == "ray" else dict(strip_command)
            shutter = nearest_shutter(source, cct, gm)
            cache_key = f"{source}-n1-cct{cct}-gm{gm}"
            session_plan_shutters[cache_key] = shutter
            base = {
                "capture_role": "formal",
                "formal_measurement": True,
                "command": command,
                "exact_command_hash": thermal.canonical_sha256(command),
                "requested_elapsed_s": 120,
                "nominal_shutter": shutter,
                "exposure_cache_key": cache_key,
                "timing_acceptance": "observed_elapsed_record_only",
                "strip_zero_required": source == "ray",
                "ray_zero_required": source == "strip",
                "session_index": point_index * 2 + source_index,
                "source_order": source_index,
                "target_cct": cct,
                "target_gm": gm,
                "steady_claim": False,
                "source_id": source,
                "state_id": f"N1_C{cycle_index}_CCT{cct}_GM{gm}_{source.upper()}",
                "role": f"{source}_n1_cct{cct}_gm{gm}_cycle{cycle_index}",
                "n1_cycle_index": cycle_index,
                "n1_session_index": session_index,
            }
            elapsed_list = [120]
            if burst_here:
                elapsed_list.extend(
                    120 + N1_BURST_STEP_S * (extra + 1)
                    for extra in range(N1_BURST_EXTRA_CAPTURES)
                )
            for elapsed_index, elapsed in enumerate(elapsed_list):
                step = dict(base)
                step["requested_elapsed_s"] = elapsed
                burst_role = (
                    "burst_main" if burst_here and elapsed_index == 0
                    else f"burst_extra_{elapsed_index}" if burst_here
                    else "paired_cycle_main"
                )
                step["n1_burst_role"] = burst_role
                step["capture_id"] = (
                    f"{len(captures):03d}-{source}-guide11-n1-s{session_index}"
                    f"-cct{cct}-gm{gm}-c{cycle_index}"
                    + (f"-b{elapsed_index}" if burst_here else "")
                )
                captures.append(step)
    budget_cr3 = len(captures)
    plan = {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": GUIDE11_N1_EXPERIMENT_ID,
        "variant": GUIDE11_N1_VARIANT,
        "stage": f"GUIDE11-N1-SESSION-{session_index}",
        "phase": "formal",
        "source": "guide11_n1_repeatability",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
        },
        "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_n1_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": session_plan_shutters,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(session_plan_shutters),
            "frozen_shutters_sha256": thermal.canonical_sha256(session_plan_shutters),
        },
        "budgets": {
            "ray_cap": sum(row["source_id"] == "ray" for row in captures),
            "strip_cap": sum(row["source_id"] == "strip" for row in captures),
            "formal_cap": budget_cr3,
            "physical_cr3_cap": budget_cr3,
            "ambient_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": N1_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": GUIDE11_N1_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100",
                "aperture": "f/4",
                "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_n1_white_repeatability",
            "points": [{"cct": cct, "gm": gm} for cct, gm in N1_POINTS],
            "burst_points": [{"cct": cct, "gm": gm} for cct, gm in N1_BURST_POINTS],
            "session_index": session_index,
            "cycle_index": cycle_index,
            "commands_audit": commands_audit,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "interpolation_model": "guide11_mired_gm_bilinear_clamped_v1",
            "steady_claim": False,
        },
    }
    return plan
