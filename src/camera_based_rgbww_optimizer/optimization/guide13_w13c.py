"""GUIDE13 W13-C: corrected-interpolation development regression plan.

The six frozen development-regression requests from GUIDE13 W13-C /
experiment_targets.json, photographed with the CORRECTED runtime
interpolation (guide12_w123.interpolate_fullscale_command, mired weight
fixed). These are development regressions of old W12-3 request
coordinates, not new independent holdouts; the 20 new holdouts run only
after this dev arm passes.

Strip shutter selection re-derives the W12-3 rule ("slowest stop
keeping the bilinear-predicted brightness ceiling <= 14000 DN") from the
W12-2 node brightness table with the CORRECTED bilinear weights - the
frozen 2026-10-08 table predicted brightness with the inverted-weight
commands, so its predictions no longer describe the corrected commands.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from camera_based_rgbww_optimizer.optimization.guide12_w123 import (
    interpolate_fullscale_command,
    resolve_w123_ray_shutter,
)

W13C_EXPERIMENT_ID = "GUIDE13_W13_C_INTERPOLATION_DEV_REGRESSION_V1"
# W13-C executes the exact W12-3 measurement contract (white FAST pairs,
# Ray reference + fullscale strip, per-frame source isolation); the
# frozen W12-3 execution schema is reused verbatim so the runner's
# authorization, isolation, near-noise classification and post-capture
# validation semantics are the ones the W12-3 holdout itself ran under.
# The GUIDE13 scientific identity is carried by guide_experiment_id.
W13C_AUTHORIZATION_SCHEMA = "direct_guide12_w123_interpolation_v1"
W13C_REQUESTS: tuple[tuple[int, int], ...] = (
    (1850, 50), (2400, 50), (5350, 105), (6050, 160),
    (10500, 120), (17500, 30),
)
W13C_COLD_CCT = 14000
W13C_BRIGHTNESS_CEILING_DN = 14000.0
# standard one-third-stop shutter denominators used by the frozen tables
W13C_SHUTTER_LADDER: tuple[int, ...] = (
    50, 60, 80, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800,
    1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6400,
)


def _corrected_weights(
    lut_nodes: list[Mapping[str, Any]], cct: int, gm: int,
) -> dict[tuple[int, int], float]:
    """Corner weights (cct, gm) -> w for the corrected bilinear blend
    (identical math to the corrected interpolate_fullscale_command,
    exposed here so brightness prediction uses the same weights)."""
    by_cct: dict[int, dict[int, Mapping[str, Any]]] = {}
    for node in lut_nodes:
        by_cct.setdefault(int(node["cct"]), {})[int(node["gm"])] = node
    ccts = sorted(by_cct)
    gms = sorted({g for row in by_cct.values() for g in row})
    mireds = [1_000_000.0 / c for c in ccts]
    target = 1_000_000.0 / cct
    i = max(
        (k for k in range(len(mireds) - 1)
         if mireds[k] >= target >= mireds[k + 1]), default=None)
    if i is None:
        raise ValueError(f"W13-C request {cct}K outside the node grid")
    j_raw = [k for k in range(len(gms) - 1) if gms[k] <= gm <= gms[k + 1]]
    j = j_raw[0] if j_raw else (0 if gm <= gms[0] else len(gms) - 2)
    ty = (gm - gms[j]) / (gms[j + 1] - gms[j]) if gms[j + 1] != gms[j] else 0.0
    tx = ((target - mireds[i + 1]) / (mireds[i] - mireds[i + 1])
          if mireds[i] != mireds[i + 1] else 0.0)
    # corrected: the LOWER cct (higher mired, T0) carries weight tx
    return {
        (ccts[i], gms[j]): tx * (1 - ty),
        (ccts[i], gms[j + 1]): tx * ty,
        (ccts[i + 1], gms[j]): (1 - tx) * (1 - ty),
        (ccts[i + 1], gms[j + 1]): (1 - tx) * ty,
    }


def predict_strip_max_dn(
    lut_nodes: list[Mapping[str, Any]],
    brightness: Mapping[str, Mapping[str, float]],
    cct: int, gm: int,
) -> float:
    """Predicted main-block ceiling (DN) at 1 s equivalent for the
    corrected interpolated command: the node dn_per_1over values blended
    with the same corrected weights."""
    weights = _corrected_weights(lut_nodes, cct, gm)
    total = 0.0
    for (node_cct, node_gm), w in weights.items():
        key = f"{node_cct}/{node_gm}"
        if key not in brightness:
            raise ValueError(f"W13-C brightness table missing node {key}")
        total += w * float(brightness[key]["dn_per_1over"])
    return total


def select_strip_shutter(
    lut_nodes: list[Mapping[str, Any]],
    brightness: Mapping[str, Mapping[str, float]],
    cct: int, gm: int,
) -> dict[str, Any]:
    """Slowest one-third stop keeping the corrected predicted ceiling
    <= 14000 DN (the frozen W12-3 selection rule)."""
    dn_per_1over = predict_strip_max_dn(lut_nodes, brightness, cct, gm)
    for denom in W13C_SHUTTER_LADDER:
        if dn_per_1over / denom <= W13C_BRIGHTNESS_CEILING_DN:
            return {
                "shutter": f"1/{denom}",
                "pred_max": dn_per_1over / denom,
                "dn_per_1over": dn_per_1over,
                "rule": "corrected-weight bilinear node brightness, "
                        "ceiling <= 14000 DN",
            }
    raise ValueError(
        f"W13-C no shutter keeps {cct}/{gm} under the ceiling "
        f"(dn_per_1over={dn_per_1over})")


def build_guide13_w13c_dev_plan(
    lut_nodes: list[Mapping[str, Any]],
    *,
    brightness: Mapping[str, Mapping[str, float]],
) -> dict[str, Any]:
    """One W13-C dev-regression run: per request, Ray at the requested
    cct/gm then the strip at the corrected interpolated command (cold
    requests sandwich the strip between Ray references). Commands come
    from the corrected runtime function and are never adjusted
    in-run."""
    from camera_based_rgbww_optimizer.optimization import guide12
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    commands: dict[str, dict[str, int]] = {}
    for cct, gm in W13C_REQUESTS:
        key = f"{cct}/{gm}"
        interp = interpolate_fullscale_command(lut_nodes, cct, gm)
        commands[key] = interp["command"]
        cache = key.replace("/", "-")
        ray_shutter = resolve_w123_ray_shutter(cct, gm)
        strip = select_strip_shutter(lut_nodes, brightness, cct, gm)
        frozen[f"w13c-ray-{cache}"] = ray_shutter
        frozen[f"w13c-strip-{cache}"] = strip["shutter"]
        ray_command = {"cct": cct, "gm": gm, "intensity_percent": 100.0,
                       "mode": "cct"}
        cold = cct >= W13C_COLD_CCT

        def add(step, src, cmd, shutter, role):
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-{src}-guide13-w13c-cct{cct}"
                    f"-gm{gm}-{step}"),
                "source_id": src,
                "state_id": f"CCT{cct}_GM{gm}_W13C_{step.upper()}",
                "role": role, "command": dict(cmd),
                "exact_command_hash": thermal.canonical_sha256(cmd),
                "requested_elapsed_s": guide12.W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": shutter,
                "exposure_cache_key": f"w13c-{src}-{cache}",
                "strip_zero_required": src == "ray",
                "ray_zero_required": src == "strip",
                "w13c_request": key, "w13c_step": step,
                "w13c_corrected_command": dict(interp["command"]),
                "w13c_command_source": "corrected_interpolate_fullscale",
            })

        if cold:
            add("raybefore", "ray", ray_command, ray_shutter, "ray_reference")
        else:
            add("ray", "ray", ray_command, ray_shutter, "ray_reference")
        add("strip", "strip", interp["command"], strip["shutter"],
            "strip_interpolated")
        if cold:
            add("rayafter", "ray", ray_command, ray_shutter, "ray_reference")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W13C_EXPERIMENT_ID,
        "variant": "guide13_w13_c_dev_regression_v1",
        "stage": "GUIDE13-W13-C-DEV-REGRESSION",
        "phase": "formal",
        "source": "guide13_w13c_corrected_requests_20261013",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "frozen_lut": {"path": "D:/rgbww-optimizer/guide12-w122/"
                          "derived/w12-2-frozen-lut-20261005.json"},
            "node_brightness": {"path": "D:/rgbww-optimizer/guide12-w122/"
                              "derived/w122-node-strip-brightness.json"},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide13_w13c_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "strip_rule": (
                "slowest 1/3 stop keeping the CORRECTED-weight bilinear "
                "node-brightness ceiling <= 14000 DN (W12-2 table)"
            ),
            "ray_rule": "W2 anchors + same-CCT nearest-gm transfer (W12-2 rule)",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0, "extra_budget_cap": 0,
        },
        "execution_authorization": {
            "schema": W13C_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W13C_EXPERIMENT_ID,
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
            "method": "guide13_w13_c_interpolation_dev_regression",
            "requests": [f"{c}/{g}" for c, g in W13C_REQUESTS],
            "corrected_commands": commands,
            "role": (
                "development regression of the corrected runtime function "
                "at old W12-3 request coordinates; NOT independent holdouts; "
                "the 20 new holdouts run only after this arm"),
            "tolerances": dict(guide12.W12_TOLERANCES),
        },
    }
