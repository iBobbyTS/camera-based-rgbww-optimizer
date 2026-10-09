"""GUIDE12 W12-4: true-LONG order re-verification (frozen).

Per GUIDE 12.GUIDE.md W12-4, re-verify the FAST/LONG protocol difference at
the four GUIDE11 deviation points (1800/100, 3200/100, 5600/100, 20000/100)
with the order structure GUIDE11 W4 lacked: LONG executes before FAST for
the two largest-deviation points (3200, 20000), FAST before LONG for the
other two (balanced), and the campaign interleaves the points so protocol
is not confounded with time period. Source order (Ray-first vs strip-first)
is balanced four/four and flips between the two protocols of each point.

The runner applies one plan-level reset per plan, so one plan carries
exactly one protocol for exactly one point (two frames: one Ray reference
and one strip observation under the frozen LUT node command). The campaign
is eight small runs executed in W124_EXECUTION_ORDER.

Timing labels stay exact: FAST = reset600/D120, LONG = reset1800/D600
(matching the GUIDE11 W4 definitions this experiment re-verifies).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

W124_EXPERIMENT_ID = "GUIDE12_W12_4_LONG_ORDER_REVERIFICATION_V1"
CHANNELS = ("cw", "ww", "r", "g", "b")
W124_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 100), (3200, 100), (5600, 100), (20000, 100),
)
W124_PROTOCOLS = ("fast", "long")
W124_TIMING = {
    "fast": {"reset_s": 600, "dwell_s": 120,
             "resolution": "guide12_w124fast_reset600_D120"},
    "long": {"reset_s": 1800, "dwell_s": 600,
             "resolution": "guide12_w124long_reset1800_D600"},
}

# Measured-good shutters frozen from the executed W12-2 verification plans
# (quality-passed frames; 20000/100 strip is the W12-2 rail correction).
W124_FROZEN_SHUTTERS: dict[str, dict[str, str]] = {
    "1800/100": {"ray": "1/1600", "strip": "1/100"},
    "3200/100": {"ray": "1/2500", "strip": "1/100"},
    "5600/100": {"ray": "1/2500", "strip": "1/100"},
    "20000/100": {"ray": "1/2500", "strip": "1/125"},
}

# Campaign execution order (one run per entry): LONG precedes FAST for the
# two GUIDE11 largest-deviation points (3200, 20000), FAST precedes LONG for
# 1800/5600 (balanced), and points alternate so both protocols appear in
# each half of the campaign (protocol is not a time-period alias).
W124_EXECUTION_ORDER: tuple[tuple[str, str], ...] = (
    ("3200/100", "long"), ("1800/100", "fast"),
    ("20000/100", "long"), ("5600/100", "fast"),
    ("3200/100", "fast"), ("1800/100", "long"),
    ("20000/100", "fast"), ("5600/100", "long"),
)

# Source order per run: four Ray-first and four strip-first, opposite
# between the two protocols of the same point.
W124_RAY_FIRST: dict[tuple[str, str], bool] = {
    ("3200/100", "long"): True, ("1800/100", "fast"): True,
    ("20000/100", "long"): False, ("5600/100", "fast"): False,
    ("3200/100", "fast"): False, ("1800/100", "long"): False,
    ("20000/100", "fast"): True, ("5600/100", "long"): True,
}

CAMPAIGN_FRAME_CAP = 24
CAMPAIGN_CORE_FRAMES = 16


def execution_index(point: str, protocol: str) -> int:
    return W124_EXECUTION_ORDER.index((point, protocol))


def build_guide12_w124_point_plan(
    lut_nodes: list[Mapping[str, Any]],
    cct: int,
    gm: int,
    *,
    protocol: str,
    ray_first: bool | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One W12-4 run: one point under one protocol, two frames (Ray
    reference + strip on the frozen LUT node command). ``ray_first``
    defaults to the frozen campaign source-order table."""
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization import guide12
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    if protocol not in W124_PROTOCOLS:
        raise ValueError("W12-4 protocol must be 'fast' or 'long'")
    key = f"{cct}/{gm}"
    if (cct, gm) not in W124_POINTS:
        raise ValueError(f"W12-4 point {key} is not one of the four frozen points")
    lut_by_key = {(int(n["cct"]), int(n["gm"])): n for n in lut_nodes}
    if (cct, gm) not in lut_by_key:
        raise ValueError(f"W12-4 point {key} missing from the frozen LUT")
    strip_command = {ch: int(lut_by_key[(cct, gm)]["command"][ch]) for ch in CHANNELS}
    ray_command = {"cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct"}
    if ray_first is None:
        ray_first = W124_RAY_FIRST[(key, protocol)]
    timing = W124_TIMING[protocol]
    shutters = W124_FROZEN_SHUTTERS[key]
    sources = ("ray", "strip") if ray_first else ("strip", "ray")

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    for source_index, source in enumerate(sources, start=1):
        command = ray_command if source == "ray" else strip_command
        cache = f"w124-{protocol}-{source}-{cct}-{gm}"
        frozen[cache] = shutters[source]
        captures.append({
            "capture_id": (
                f"{len(captures):03d}-{source}-guide12-w124-{protocol}-cct{cct}-gm{gm}"
            ),
            "source_id": source,
            "state_id": f"W124_{protocol.upper()}_CCT{cct}_GM{gm}_{source.upper()}",
            "role": (
                "ray_reference" if source == "ray"
                else f"strip_w124_{protocol}"
            ),
            "command": dict(command),
            "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": timing["dwell_s"],
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True,
            "capture_role": "formal",
            "session_index": len(captures) + 1,
            "source_order": source_index,
            "nominal_shutter": shutters[source],
            "exposure_cache_key": cache,
            "strip_zero_required": source == "ray",
            "ray_zero_required": source == "strip",
            "w124_point": key,
            "w124_protocol": protocol,
            "w124_lut_command": dict(strip_command) if source == "strip" else None,
        })
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W124_EXPERIMENT_ID,
        "variant": f"p7_td_c_w12_4_{protocol}_v1",
        "stage": f"GUIDE12-W12-4-{protocol.upper()}",
        "phase": "formal",
        "source": "guide12_w12_4_long_order_reverification_20261008",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "frozen_lut": {"path": "D:/rgbww-optimizer/guide12-w122/derived/"
                          "w12-2-frozen-lut-20261005.json"},
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": timing["resolution"],
        "cold_proxy": timing["reset_s"],
        "cold_proxy_wait_s": timing["reset_s"],
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "rule": (
                "verbatim W12-2 executed verification shutters for the four "
                "points (quality-passed frames; 20000/100 strip is the "
                "W12-2 rail correction 1/125)"
            ),
        },
        "budgets": {
            "formal_cap": 2, "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": 2, "setup_physical_cr3_cap": 0,
            "retry": 0,
            "campaign_core_frames": CAMPAIGN_CORE_FRAMES,
            "campaign_frame_cap": CAMPAIGN_FRAME_CAP,
        },
        "execution_authorization": {
            "schema": f"direct_guide12_w124_{protocol}_v1",
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W124_EXPERIMENT_ID,
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
            "method": "guide12_w12_4_order_reverification_did",
            "point": {"cct": cct, "gm": gm},
            "protocol": protocol,
            "primary_quantity": "(strip-Ray)_LONG-(strip-Ray)_FAST",
            "components_reported_separately": ["Ray_LONG-FAST", "strip_LONG-FAST"],
            "campaign_execution_order": [
                f"{p}:{q}" for p, q in W124_EXECUTION_ORDER],
            "order_note": (
                "LONG precedes FAST for 3200/100 and 20000/100 (GUIDE11 "
                "largest deviations), FAST precedes LONG for 1800/100 and "
                "5600/100; source order four/four and flipped within each "
                "point; GUIDE11's all-FAST-first layout is only historical "
                "context, never merged as one ideal ABBA"
            ),
            "same_command_rule": (
                "strip uses the current frozen LUT command; if it differs "
                "from GUIDE11's adopted command the GUIDE11 comparison is "
                "historical background, not a same-command replicate"
            ),
            "independent_reset_s": timing["reset_s"],
            "dwell_s": timing["dwell_s"],
            "steady_claim": False,
            "thermal_causal_claim": False,
            "tolerances": dict(guide12.W12_TOLERANCES),
        },
    }
