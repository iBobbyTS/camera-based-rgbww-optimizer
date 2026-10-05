"""GUIDE12 C12-1 Ray HSI true mapping: frozen targets and plan builders.

Scientific owner: advisor/12/12.GUIDE.md section 5 C12-1 (immutable).
The old GUIDE11 C3 ruler is deprecated as the product SAT/Hue meter
(offline evidence: 0/10 self-inverse within the old 2deg/2pp gate,
all targets multi-solution - c12-1-offline-tables-20261005.json).

This module freezes:
- the C12-1 Ray-only capture grid: 12 holdouts at previously untested
  coordinates (six sectors, 0/360 sides, S10/S20/S75 curvature), the
  H120/S100 and H300/S100 qualification references (2 each), one S0
  control per special target, one session-A S0 reference and one S0
  hue-consistency diagnostic (hue 240);
- per-target initial shutters transferred from the P6 node-brightness
  table (D:/rgbww-optimizer/guide12-c12/derived/p6-node-brightness.json)
  scaled by the N2 H0/S100 anchor factor 0.59, targeting ~9000 DN block
  max, snapped to the next faster camera stop (evidence:
  c12-1-frozen-targets-20261005.json).

Total frozen frames: 20 of the <=31 Ray-only budget; the remaining 11
cover bounded shutter retries / diagnostics.

All frames are real FAST observations (off600 -> command 120 -> capture,
strip verified zero) exactly like the N2 ladder, so measurement identity
matches the existing evidence chain.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import (
    p7_thermal_diagnostics as thermal,
)
from camera_based_rgbww_optimizer.optimization.guide12_n2 import W12_FAST_DWELL_S
from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
    AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
)

C12_EXPERIMENT_ID = "GUIDE12_C12_RAY_MAPPING_V1"
C12_VARIANT = "c12_1_ray_grid_v1"
C12_SCHEMA = "direct_guide12_c12_ray_grid_v1"

# (hue, sat, role, shutter) - frozen 2026-10-05; provenance in the module
# docstring and c12-1-frozen-targets-20261005.json.
C12_1_TARGETS: tuple[dict[str, Any], ...] = (
    {"hue": 5, "sat": 50, "role": "holdout", "shutter": "1/4000"},
    {"hue": 355, "sat": 50, "role": "holdout", "shutter": "1/2500"},
    {"hue": 65, "sat": 20, "role": "holdout", "shutter": "1/6400"},
    {"hue": 125, "sat": 10, "role": "holdout", "shutter": "1/6400"},
    {"hue": 175, "sat": 75, "role": "holdout", "shutter": "1/4000"},
    {"hue": 235, "sat": 20, "role": "holdout", "shutter": "1/5000"},
    {"hue": 245, "sat": 75, "role": "holdout", "shutter": "1/4000"},
    {"hue": 295, "sat": 10, "role": "holdout", "shutter": "1/5000"},
    {"hue": 305, "sat": 75, "role": "holdout", "shutter": "1/2500"},
    {"hue": 55, "sat": 75, "role": "holdout", "shutter": "1/5000"},
    {"hue": 115, "sat": 50, "role": "holdout", "shutter": "1/5000"},
    {"hue": 335, "sat": 20, "role": "holdout", "shutter": "1/4000"},
    {"hue": 120, "sat": 100, "role": "special_qualification_ref", "shutter": "1/3200"},
    {"hue": 120, "sat": 100, "role": "special_qualification_ref", "shutter": "1/3200"},
    {"hue": 300, "sat": 100, "role": "special_qualification_ref", "shutter": "1/1600"},
    {"hue": 300, "sat": 100, "role": "special_qualification_ref", "shutter": "1/1600"},
    {"hue": 0, "sat": 0, "role": "s0_control", "shutter": "1/6400"},
    {"hue": 0, "sat": 0, "role": "s0_control", "shutter": "1/6400"},
    {"hue": 0, "sat": 0, "role": "s0_reference_sessionA", "shutter": "1/6400"},
    {"hue": 240, "sat": 0, "role": "s0_hue_consistency_diag", "shutter": "1/6400"},
)

# Coordinates already measured before this freeze (training pool; holdouts
# above were chosen to avoid them).
C12_1_EXISTING_COORDINATES: tuple[tuple[int, int], ...] = (
    (0, 50), (0, 100), (60, 50), (60, 100), (120, 50), (180, 50), (180, 100),
    (240, 50), (240, 100), (300, 50),
    (30, 75), (90, 75), (150, 75), (210, 75), (270, 75), (330, 75), (350, 75),
    (280, 50), (90, 20), (210, 10),
)


def c12_target_command(target: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "mode": "hsi",
        "hue": int(target["hue"]),
        "sat": int(target["sat"]),
        "intensity_percent": 100.0,
    }


def build_guide12_c12_ray_grid_plan(
    *,
    roles: Sequence[str] | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Ray-only HSI grid for the C12-1 true mapping.

    ``roles`` narrows a retry to the target classes a first attempt could
    not cover (fail-closed observer gates stop the run at the first
    rejected frame); the default covers every frozen target once.
    """
    selected = [
        t for t in C12_1_TARGETS if roles is None or t["role"] in set(roles)
    ]
    if not selected:
        raise ValueError("C12-1 role filter selected no targets")
    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    counters: dict[str, int] = {}
    for target in selected:
        role = str(target["role"])
        counters[role] = counters.get(role, 0) + 1
        key = f"c12-{role}-h{target['hue']}-s{target['sat']}-{counters[role]}"
        shutter = str(target["shutter"])
        frozen[key] = shutter
        command = c12_target_command(target)
        captures.append({
            "capture_id": f"{len(captures):03d}-ray-guide12-c12-{key}",
            "source_id": "ray",
            "state_id": f"C12_1_{key.upper().replace('-', '_')}",
            "role": "c12_ray_grid",
            "command": command,
            "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True,
            "capture_role": "formal",
            "session_index": len(captures) + 1,
            "nominal_shutter": shutter,
            "exposure_cache_key": key,
            "c12_role": role,
            "c12_hue": int(target["hue"]),
            "c12_sat": int(target["sat"]),
            "strip_zero_required": True,
        })
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C12_EXPERIMENT_ID,
        "variant": C12_VARIANT,
        "stage": "GUIDE12-C12-1-RAY-GRID",
        "phase": "formal",
        "source": "guide12_c12_1_design_frozen_20261005",
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
        "timing_resolution": "guide12_c12_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "transfer_rule": (
                "P6 node brightness (foundations/ray-hsi-manifold) scaled by "
                "N2 H0/S100 anchor factor 0.59, target 9000 DN, next faster "
                "camera stop; anchors: H0->1/1600 (N2 1/1000), H240->1/3200 "
                "(N2 1/2000)"
            ),
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0,
            "ambient_cap": 0,
            "physical_cr3_cap": len(captures),
            "setup_physical_cr3_cap": 0,
            "retry": 0,
            "ray_only_total_cap": 31,
            "frozen_frames": len(C12_1_TARGETS),
            "remaining_diagnostics_cap": 31 - len(C12_1_TARGETS),
        },
        "execution_authorization": {
            "schema": C12_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C12_EXPERIMENT_ID,
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
            "method": "guide12_c12_ray_grid",
            "design": "guide12_c12_1_design_frozen_20261005",
            "z_estimator": (
                "block_06 four planes -> z=(log R/Gmean, log B/Gmean)"
            ),
            "budgets": {"hue_deg": 0.5, "sat_pp": 0.5},
            "holdout_count": sum(
                1 for t in C12_1_TARGETS if t["role"] == "holdout"
            ),
            "special_qualification": ["120,100", "300,100"],
            "s0_frames": [
                "sessionA reference (hue 0)",
                "hue consistency diag (hue 240)",
                "one S0 control per special target",
            ],
        },
    }
