"""GUIDE13 C13-D: runtime experience holdout plan (frozen).

Per GUIDE13 C13-D: after the offline anchor-identity / 0-360 / SAT-boundary
/ fullscale / label regressions pass (they have - tests/test_guide12_c124 and
the offline enumeration), run the 10 general holdouts (three same-hue
low-SAT pairs included) and the fixed same-Hue SAT tracks (H60/H120/H300 at
S0/S10/S20/S37). Each request is an independent Ray-bracketed FAST sandwich
(ray before, strip model output, ray after) - the same frozen measurement
contract as the C12-4 holdout, reusing the c124 holdout execution schema
with GUIDE13 identity. Comparison is same-hue-track equivalent SAT and Hue
deviation only; the runtime function is the corrected c124_model_command
(S0 white anchor, honest requested/realized/compressed labels).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from camera_based_rgbww_optimizer.optimization.guide12_c124 import (
    C124_RAY_SHUTTERS,
    c124_model_command,
)

C13D_EXPERIMENT_ID = "GUIDE13_C13_D_RUNTIME_HOLDOUT_V1"
C13D_SCHEMA = "direct_guide12_c124_model_holdout_v1"
GENERAL = ((1, 37), (359, 37), (135, 50), (255, 50), (75, 10), (75, 20),
           (195, 10), (195, 20), (315, 10), (315, 20))
TRACKS = ((60, 10), (60, 20), (60, 37),
          (120, 0), (120, 10), (120, 20), (120, 37),
          (300, 0), (300, 10), (300, 20), (300, 37))


def _ray_shutter(hue: int, sat: int) -> str:
    key = f"{hue}/{sat}"
    if key in C124_RAY_SHUTTERS:
        return C124_RAY_SHUTTERS[key]
    # nearest-row transfer (C12-1 rule): nearest P6 row by hue then sat
    best = min(
        C124_RAY_SHUTTERS,
        key=lambda k: (abs(int(k.split("/")[0]) - hue) % 360,
                       abs(int(k.split("/")[1]) - sat)))
    return C124_RAY_SHUTTERS[best]


def build_guide13_c13d_plan() -> dict[str, Any]:
    from camera_based_rgbww_optimizer.optimization import guide12
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )
    from camera_based_rgbww_optimizer.optimization.guide12_n2 import W12_FAST_DWELL_S

    requests = GENERAL + TRACKS
    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    models: dict[str, dict[str, int]] = {}
    for hue, sat in requests:
        key = f"{hue}/{sat}"
        model = c124_model_command(hue, sat)
        models[key] = model["command"]
        ray_command = {"mode": "hsi", "hue": hue, "sat": sat,
                       "intensity_percent": 100.0}
        cache = key.replace("/", "-")
        ray_shutter = _ray_shutter(hue, sat)
        frozen[f"c13d-ray-{cache}"] = ray_shutter
        frozen[f"c13d-strip-{cache}"] = "1/400"

        def add(src, role, cmd, shutter, pos):
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-{src}-guide13-c13d-h{hue}-s{sat}"
                    f"-{pos}"),
                "source_id": src,
                "state_id": f"C13D_H{hue}_S{sat}_{pos.upper()}",
                "role": role, "command": dict(cmd),
                "exact_command_hash": thermal.canonical_sha256(cmd),
                "requested_elapsed_s": W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": shutter,
                "exposure_cache_key": f"c13d-{src}-{cache}",
                "strip_zero_required": src == "ray",
                "ray_zero_required": src == "strip",
                "c13d_request": key, "c13d_position": pos,
                "c13d_model_command": dict(model["command"]) if src == "strip" else None,
                "c13d_realized_sat": model["realized_sat"] if src == "strip" else None,
                "c13d_sat_status": model["sat_status"] if src == "strip" else None,
            })

        add("ray", "ray_reference", ray_command, ray_shutter, "raybefore")
        add("strip", "strip_model_output", model["command"], "1/400", "strip")
        add("ray", "ray_reference", ray_command, ray_shutter, "rayafter")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C13D_EXPERIMENT_ID,
        "variant": "guide13_c13_d_runtime_holdout_v1",
        "stage": "GUIDE13-C13-D-HOLDOUT",
        "phase": "formal",
        "source": "guide13_c13d_holdouts_20261018",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
        },
        "captures": captures,
        "capture_ids": [str(s["capture_id"]) for s in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide13_c13d_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "ray_rule": "exact P6 anchor else nearest-row transfer (C12-1 rule)",
            "strip_rule": "uniform 1/400 (model outputs are S0-S50 class)",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0, "general_holdouts": len(GENERAL),
            "track_frames": len(TRACKS) * 3,
        },
        "execution_authorization": {
            "schema": C13D_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C13D_EXPERIMENT_ID,
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
            "method": "guide13_c13_d_runtime_holdout",
            "requests": [f"{h}/{s}" for h, s in requests],
            "model_commands": models,
            "checks": [
                "same-hue track equivalent-SAT and Hue deviation only",
                "low-SAT non-silent-clamp label honesty (requested vs realized)",
                "no new pass gate from worst failure",
            ],
            "steady_claim": False,
        },
        "cleanup": {"python_finally": "required",
                    "shell_trap": "EXIT_INT_TERM_HUP_required"},
    }
