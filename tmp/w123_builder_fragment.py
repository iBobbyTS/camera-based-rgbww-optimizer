

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
        strip_shutter = str(strip_shutters[key])
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
