"""GUIDE12 W12-3: true fullscale runtime interpolation (frozen).

The actual runtime output function for non-node white requests, per GUIDE
12.GUIDE.md W12-3: interpolate in (mired, raw-GM) over the frozen 70-node
W12-2 LUT, then project to actual fullscale (scale so the maximum channel
reaches 4095), then integerize - in that declared order. The last actual
PWM always has at least one channel at 4095. Face switching is whatever
channel wins the projection; callers can inspect the winning channel to
cover face-switch requests.

Interpolation: bilinear in (mired, gm) over the 14-CCT x 5-gm grid.
Requests outside the convex grid raise (no extrapolation).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

W123_EXPERIMENT_ID = "GUIDE12_W12_3_INTERPOLATION_V1"
W123_AUTHORIZATION_SCHEMA = "direct_guide12_w123_interpolation_v1"
CHANNELS = ("cw", "ww", "r", "g", "b")
FULLSCALE = 4095


def _grid(lut_nodes: list[Mapping[str, Any]]):
    by_cct: dict[int, dict[int, Mapping[str, Any]]] = {}
    for node in lut_nodes:
        by_cct.setdefault(int(node["cct"]), {})[int(node["gm"])] = node
    ccts = sorted(by_cct)
    gms = sorted({gm for row in by_cct.values() for gm in row})
    if len(gms) != 5:
        raise ValueError("W12-3 expects the 5-gm frozen LUT grid")
    for cct in ccts:
        if sorted(by_cct[cct]) != gms:
            raise ValueError(f"W12-3 LUT row incomplete at {cct}K")
    mireds = [1_000_000.0 / cct for cct in ccts]
    return ccts, gms, mireds, by_cct


def interpolate_fullscale_command(
    lut_nodes: list[Mapping[str, Any]], cct: int, gm: int,
) -> dict[str, Any]:
    """Actual runtime command for a non-node (cct, gm) request.

    Order of operations (frozen): bilinear channel interpolation in
    (mired, gm) over the node grid -> fullscale projection (scale the
    maximum channel to 4095) -> round-half-up integerization -> clip to
    [0, 4095] (the winning channel stays exactly 4095).
    """
    ccts, gms, mireds, by_cct = _grid(lut_nodes)
    if not ccts[0] <= cct <= ccts[-1]:
        raise ValueError(f"W12-3 request {cct}K outside the node grid")
    if not gms[0] <= gm <= gms[-1]:
        raise ValueError(f"W12-3 request gm{gm} outside the node grid")
    # locate the bracketing mired interval (mired is decreasing in cct)
    target = 1_000_000.0 / cct
    i = max(
        (k for k in range(len(mireds) - 1)
         if mireds[k] >= target >= mireds[k + 1]),
        default=None,
    )
    if i is None:
        raise ValueError(f"W12-3 request {cct}K outside the node grid")
    j_raw = [k for k in range(len(gms) - 1) if gms[k] <= gm <= gms[k + 1]]
    j = j_raw[0] if j_raw else (0 if gm <= gms[0] else len(gms) - 2)
    ty = (gm - gms[j]) / (gms[j + 1] - gms[j]) if gms[j + 1] != gms[j] else 0.0
    cct_lo, cct_hi = ccts[i + 1], ccts[i]  # mired-increasing bracket
    tx = (target - mireds[i + 1]) / (mireds[i] - mireds[i + 1]) \
        if mireds[i] != mireds[i + 1] else 0.0
    corners = (
        (i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1),
    )
    weights = {
        (i, j): (1 - tx) * (1 - ty),
        (i, j + 1): (1 - tx) * ty,
        (i + 1, j): tx * (1 - ty),
        (i + 1, j + 1): tx * ty,
    }
    raw = {ch: 0.0 for ch in CHANNELS}
    used_nodes = []
    for (ci, gj), w in weights.items():
        node = by_cct[ccts[ci]][gms[gj]]
        used_nodes.append(f"{node['cct']}/{node['gm']}")
        for ch in CHANNELS:
            raw[ch] += w * float(node["command"][ch])
    peak = max(raw.values())
    if peak <= 0:
        raise ValueError("W12-3 interpolation produced a zero command")
    projected = {ch: raw[ch] * (FULLSCALE / peak) for ch in CHANNELS}
    command = {}
    for ch in CHANNELS:
        v = int(round(projected[ch]))
        command[ch] = max(0, min(FULLSCALE, v))
    winner = max(command, key=lambda ch: command[ch])
    if command[winner] != FULLSCALE:
        command[winner] = FULLSCALE
    return {
        "request": {"cct": int(cct), "gm": int(gm)},
        "command": command,
        "winning_channel": winner,
        "interpolated_raw": {ch: round(raw[ch], 2) for ch in CHANNELS},
        "bracketing_nodes": used_nodes,
        "projection_note": (
            "bilinear(mired,gm) -> scale max to 4095 -> round -> clip; "
            "winning channel forced to 4095"
        ),
    }


# 20 frozen non-node requests (GUIDE W12-3): warm/cold span, both GM sides,
# face switches, and the historical failure structures covered by nearby
# fresh coordinates (5350/105 ~ 5300/100, 6050/160 ~ 6100/165 - the exact
# old held-out points are not reused).
W123_REQUESTS: tuple[tuple[int, int], ...] = (
    (1850, 50), (2100, 170), (2400, 50), (2600, 120), (2900, 40), (3000, 180),
    (3400, 30), (3600, 150), (4100, 60), (4800, 140), (5350, 105), (5450, 90),
    (6050, 160), (7000, 80), (7500, 160), (9300, 40), (10500, 120),
    (11500, 60), (16000, 90), (17500, 30),
)
W123_COLD_CCT = 14000
W123_S0_SHUTTER = "1/6400"


def resolve_w123_ray_shutter(cct: int, gm: int, table: Mapping[str, str] = {}) -> str:
    """Frozen Ray shutter: W2 anchor table with the documented same-CCT
    nearest-gm (then joint nearest-cct/gm) transfer, exactly like W12-2."""
    from camera_based_rgbww_optimizer.optimization.guide12 import W12_RAY_SHUTTERS
    direct = table.get(f"{cct}/{gm}") or W12_RAY_SHUTTERS.get(f"ray-white-{cct}-gm{gm}")
    if direct:
        return direct

    def anchor(key: str):
        mcct, mgm = key.removeprefix("ray-white-").split("-gm")
        return abs(cct - int(mcct)) / 500.0 + abs(gm - int(mgm)) / 100.0, key

    same = [anchor(k) for k in W12_RAY_SHUTTERS if k.startswith(f"ray-white-{cct}-gm")]
    pool = same or [anchor(k) for k in W12_RAY_SHUTTERS]
    return W12_RAY_SHUTTERS[min(pool)[1]]


def build_guide12_w123_request_plan(
    lut_nodes: list[Mapping[str, Any]],
    *,
    strip_shutters: Mapping[str, str],
    ray_shutter_overrides: Mapping[str, str] | None = None,
    include_s0_reference: bool = False,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One W12-3 interpolation-holdout run: per frozen non-node request,
    an independent FAST pair (Ray at the requested cct/gm, then the strip
    running the frozen interpolated fullscale command); cold requests
    (>=14000K) sandwich the strip between Ray references. Commands are
    computed by the frozen runtime function and never adjusted in-run."""
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization import guide12
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    commands = {}
    if include_s0_reference:
        s0 = {"mode": "hsi", "hue": 0, "sat": 0, "intensity_percent": 100.0}
        frozen["w123-s0-reference-session"] = W123_S0_SHUTTER
        captures.append({
            "capture_id": "000-ray-guide12-w123-s0-reference-session",
            "source_id": "ray", "state_id": "W123_S0_REFERENCE_SESSION",
            "role": "s0_reference", "command": s0,
            "exact_command_hash": thermal.canonical_sha256(s0),
            "requested_elapsed_s": guide12.W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": 1, "nominal_shutter": W123_S0_SHUTTER,
            "exposure_cache_key": "w123-s0-reference-session",
            "strip_zero_required": True,
        })
    for cct, gm in W123_REQUESTS:
        key = f"{cct}/{gm}"
        interp = interpolate_fullscale_command(lut_nodes, cct, gm)
        commands[key] = interp
        cache_key = key.replace("/", "-")
        ray_shutter = resolve_w123_ray_shutter(
            cct, gm, ray_shutter_overrides or {})
        shutter_entry = strip_shutters[key]
        strip_shutter = str(
            shutter_entry["shutter"] if isinstance(shutter_entry, Mapping)
            else shutter_entry
        )
        frozen[f"w123-ray-{cache_key}"] = ray_shutter
        frozen[f"w123-strip-{cache_key}"] = strip_shutter
        ray_command = {"cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct"}
        cold = cct >= W123_COLD_CCT

        def add(step, src, cmd, shutter, cache, role):
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-{src}-guide12-w123-cct{cct}-gm{gm}-{step}"
                ),
                "source_id": src,
                "state_id": f"CCT{cct}_GM{gm}_W123_{step.upper()}",
                "role": role, "command": dict(cmd),
                "exact_command_hash": thermal.canonical_sha256(cmd),
                "requested_elapsed_s": guide12.W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": shutter, "exposure_cache_key": cache,
                "strip_zero_required": src == "ray",
                "ray_zero_required": src == "strip",
                "w123_request": key, "w123_step": step,
                "w123_interpolated_command": dict(interp["command"]),
            })

        if cold:
            add("raybefore", "ray", ray_command, ray_shutter,
                f"w123-ray-{cache_key}", "ray_reference")
        else:
            add("ray", "ray", ray_command, ray_shutter,
                f"w123-ray-{cache_key}", "ray_reference")
        add("strip", "strip", interp["command"], strip_shutter,
            f"w123-strip-{cache_key}", "strip_interpolated")
        if cold:
            add("rayafter", "ray", ray_command, ray_shutter,
                f"w123-ray-{cache_key}", "ray_reference")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W123_EXPERIMENT_ID,
        "variant": "p7_td_c_w12_3_interpolation_v1",
        "stage": "GUIDE12-W12-3-HOLDOUT",
        "phase": "formal",
        "source": "guide12_w12_3_frozen_requests_20261008",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "frozen_lut": {"path": "D:/rgbww-optimizer/guide12-w122/derived/"
                          "w12-2-frozen-lut-20261005.json"},
            "strip_shutters": {"path": "D:/rgbww-optimizer/guide12-w122/derived/"
                              "w123-strip-shutters-20261008.json"},
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_w123_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "strip_rule": (
                "slowest stop keeping the bilinear-predicted node-brightness "
                "ceiling <= 14000 DN (W12-2 measured node brightness table)"
            ),
            "ray_rule": "W2 anchors + same-CCT nearest-gm transfer (W12-2 rule)",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0, "extra_budget_cap": 24,
        },
        "execution_authorization": {
            "schema": W123_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W123_EXPERIMENT_ID,
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
            "method": "guide12_w12_3_interpolation_holdout",
            "requests": [f"{c}/{g}" for c, g in W123_REQUESTS],
            "interpolated_commands": {k: v["command"] for k, v in commands.items()},
            "covering": (
                "warm/cold span, both GM sides, face switches, and the "
                "historical 5300/100 and 6100/165 failure structures via "
                "fresh nearby coordinates"
            ),
            "tolerances": dict(guide12.W12_TOLERANCES),
        },
    }
