"""GUIDE13 C13-A: true local 2D Ray Jacobian neighborhoods (frozen).

Per GUIDE13 C13-A, the local measurement scale around an adopted (H, S)
target is J = [dz/dH, dz/dS] with BOTH columns measured on the Ray along
the menu H and S directions - never a 90-degree rotation of the radial
direction. The census of every Ray HSI coordinate ever measured
(2026-10-13, offline) found only exact-center observations for the three
priority targets (14/6/14 frames) and zero true local neighbors, so each
priority target gets one neighborhood block:

  center_before, (H-2,S), (H+2,S), (H,S-2), (H,S+2), holdout(H+1,S+1),
  center_after

with the S100 target using S98/S96 (SAT cannot exceed 100) and holdout
(H+1, S99), exactly as GUIDE13 specifies. All frames are Ray-only HSI at
INT=100% with verified strip-zero isolation; the two centers bracket the
neighborhood for drift. Strip commands are NOT part of this measurement:
the J scale feeds the C13-B bounded re-search analysis offline.

Budget: 3 targets x 7 frames = 21 frames (within the <=91-frame C13-A
local-scale budget; further targets only after these three are judged).

Execution reuses the frozen C12-1 Ray-grid execution schema (same
measurement contract: Ray HSI, strip-zero isolation, near-noise
classification semantics); the GUIDE13 scientific identity is carried by
guide_experiment_id, and each step keeps the c12_hue/c12_sat fields the
runner's post-capture validator reads plus c13a_* role fields.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

C13A_EXPERIMENT_ID = "GUIDE13_C13_A_LOCAL_JACOBIAN_SCALE_V1"
C13A_AUTHORIZATION_SCHEMA = "direct_guide12_c12_ray_grid_v1"

# Priority targets (experiment_targets.initial_local_Jacobian_targets)
# with their measured center shutter (actual shutter_speed of every
# prior Ray observation at that coordinate) and neighbor layout.
C13A_TARGETS: tuple[dict[str, Any], ...] = (
    {
        "hue": 0, "sat": 50, "shutter": "1/2000",
        "neighbors": ((358, 50), (2, 50), (0, 48), (0, 52)),
        "holdout": (1, 51),
    },
    {
        "hue": 300, "sat": 50, "shutter": "1/3200",
        "neighbors": ((298, 50), (302, 50), (300, 48), (300, 52)),
        "holdout": (301, 51),
    },
    {
        "hue": 60, "sat": 100, "shutter": "1/3200",
        # S100: SAT cannot exceed 100, so the S column uses S98/S96
        "neighbors": ((58, 100), (62, 100), (60, 98), (60, 96)),
        "holdout": (61, 99),
    },
)
C13A_NEVER_MEASURED_CHECK = (
    "2026-10-13 census over guide12-c12/c122/c124/w123 Ray HSI captures: "
    "no coordinate in any neighborhood other than the three centers was "
    "ever measured (fresh by construction)")


def build_guide13_c13a_plan() -> dict[str, Any]:
    """Three priority local-J neighborhoods, 7 Ray frames each."""
    from camera_based_rgbww_optimizer.optimization import guide12
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    layout = {}
    for target in C13A_TARGETS:
        h, s = target["hue"], target["sat"]
        key = f"{h}/{s}"
        block = [("center_before", (h, s))]
        block += [("neighbor", coord) for coord in target["neighbors"]]
        block += [("holdout", target["holdout"])]
        block += [("center_after", (h, s))]
        layout[key] = {
            "order": [role for role, _ in block],
            "shutter": target["shutter"],
        }
        for role, (nh, ns) in block:
            command = {"mode": "hsi", "hue": nh, "sat": ns,
                       "intensity_percent": 100.0}
            cache = f"c13a-{key.replace('/', '-')}-{nh}-{ns}"
            frozen[cache] = target["shutter"]
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-ray-guide13-c13a-h{h}-s{s}"
                    f"-{role}-{nh}-{ns}"),
                "source_id": "ray",
                "state_id": f"C13A_H{h}_S{s}_{role.upper()}_{nh}_{ns}",
                "role": "ray_local_jacobian",
                "command": command,
                "exact_command_hash": thermal.canonical_sha256(command),
                "requested_elapsed_s": guide12.W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": target["shutter"],
                "exposure_cache_key": cache,
                "strip_zero_required": True,
                "ray_zero_required": False,
                "c12_hue": nh, "c12_sat": ns,
                "c13a_target": key, "c13a_role": role,
            })
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C13A_EXPERIMENT_ID,
        "variant": "guide13_c13_a_local_jacobian_v1",
        "stage": "GUIDE13-C13-A-LOCAL-J",
        "phase": "formal",
        "source": "guide13_c13a_priority_neighborhoods_20261013",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "neighbor_census": C13A_NEVER_MEASURED_CHECK,
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide13_c13a_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "ray_rule": (
                "each neighborhood transfers the actual center shutter of "
                "every prior Ray observation at that coordinate "
                "(1/2000, 1/3200, 1/3200); +-2deg/+-2pp is the same "
                "brightness class"),
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0, "extra_budget_cap": 0,
            "c13a_total_local_budget": 91,
        },
        "execution_authorization": {
            "schema": C13A_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C13A_EXPERIMENT_ID,
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
            "method": "guide13_c13_a_local_jacobian_scale",
            "neighborhood_layout": layout,
            "jacobian_rule": (
                "J = [dz/dH, dz/dS] with each column from the measured Ray "
                "responses along that menu direction; central differences "
                "over +-2deg/+-2pp; the two columns are NOT assumed "
                "orthogonal; propagate J parameter uncertainty, reference "
                "drift (center brackets), and observation covariance"
            ),
            "holdout_rule": (
                "the (H+1,S+1) point is a one-point linear-approximation "
                "check, never a training point for J itself"),
            "s0_rule": "S0 Hue is undefined; no S0 neighborhood is measured",
        },
    }
