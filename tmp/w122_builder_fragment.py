

# ---------------------------------------------------------------------------
# GUIDE12 W12-2: frozen 70-node LUT independent verification
# ---------------------------------------------------------------------------

W122_EXPERIMENT_ID = "GUIDE12_W12_2_VERIFICATION_V1"
W122_AUTHORIZATION_SCHEMA = "direct_guide12_w122_verification_v1"
W122_STRIP_SHUTTER_OVERRIDES: dict[tuple[int, int], str] = {
    # W12 node-level pre-check ceilings plus the N2-measured bright 20000K
    # strip family; the white point is a same-shutter ratio quantity
    (2700, 100): "1/125", (5600, 0): "1/125", (8000, 0): "1/125",
    (14000, 0): "1/125", (20000, 0): "1/125", (20000, 70): "1/125",
    (20000, 100): "1/125", (20000, 130): "1/125", (20000, 200): "1/125",
}
W122_BATCHES: dict[str, tuple[tuple[int, int], ...]] = {
    "warm": tuple((cct, gm) for cct in (1800, 2000, 2300) for gm in (0, 70, 100, 130, 200)),
    "mid": tuple((cct, gm) for cct in (2700, 3200, 3800) for gm in (0, 70, 100, 130, 200)),
    "high": tuple((cct, gm) for cct in (4500, 5000, 5600) for gm in (0, 70, 100, 130, 200)),
    "veryhigh": tuple((cct, gm) for cct in (6500, 8000, 10000) for gm in (0, 70, 100, 130, 200)),
    "cold14k": tuple((14000, gm) for gm in (0, 70, 100, 130, 200)),
    "cold20k": tuple((20000, gm) for gm in (0, 70, 100, 130, 200)),
}
W122_COLD_CCT = 14000  # >= this: Ray before/after sandwich (drift gate)
W122_S0_SHUTTER = "1/6400"


def build_guide12_w122_verification_plan(
    lut_nodes: Sequence[Mapping[str, Any]],
    batch_name: str,
    *,
    include_s0_reference: bool = False,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One W12-2 verification batch over frozen-LUT nodes.

    Per node: independent FAST source pairs (Ray reference at the node's
    cct/gm, then the strip's frozen adopted command); ``needs_two_pairs``
    nodes (commands changed since W2) get a second independent pair. Cold
    nodes (>= 14000K) sandwich every strip observation between Ray
    before/after references so the known 20000K Ray drift stays a gated,
    measurable effect. Commands come verbatim from the frozen LUT - this
    builder never modifies them (verification, not optimization).
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    batch = W122_BATCHES.get(batch_name)
    if batch is None:
        raise ValueError(f"unknown W12-2 batch: {batch_name}")
    selected = [
        n for n in lut_nodes
        if (int(n["cct"]), int(n["gm"])) in set(batch)
    ]
    if len(selected) != len(batch):
        missing = set(batch) - {(int(n["cct"]), int(n["gm"])) for n in selected}
        raise ValueError(f"W12-2 batch {batch_name} lacks LUT nodes: {sorted(missing)}")
    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    if include_s0_reference:
        s0_command = {"mode": "hsi", "hue": 0, "sat": 0, "intensity_percent": 100.0}
        frozen["w122-s0-reference-session"] = W122_S0_SHUTTER
        captures.append({
            "capture_id": "000-ray-guide12-w122-s0-reference-session",
            "source_id": "ray",
            "state_id": "W122_S0_REFERENCE_SESSION",
            "role": "s0_reference",
            "command": s0_command,
            "exact_command_hash": thermal.canonical_sha256(s0_command),
            "requested_elapsed_s": W12_FAST_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "formal_measurement": True, "capture_role": "formal",
            "session_index": 1,
            "nominal_shutter": W122_S0_SHUTTER,
            "exposure_cache_key": "w122-s0-reference-session",
            "strip_zero_required": True,
        })
    for node in selected:
        cct, gm = int(node["cct"]), int(node["gm"])
        command = {k: int(node["command"][k]) for k in ("cw", "ww", "r", "g", "b")}
        repeats = 2 if node["verification_class"] == "needs_two_pairs" else 1
        cold = cct >= W122_COLD_CCT
        ray_key = f"ray-white-{cct}-gm{gm}"
        if ray_key not in W12_RAY_SHUTTERS:
            raise ValueError(f"W12-2 lacks a frozen Ray shutter for {ray_key}")
        strip_shutter = W122_STRIP_SHUTTER_OVERRIDES.get((cct, gm), W12_STRIP_SHUTTER)
        frozen[f"w122-{ray_key}"] = W12_RAY_SHUTTERS[ray_key]
        frozen[f"w122-strip-white-{cct}-gm{gm}"] = strip_shutter
        ray_command = {"cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct"}
        for repeat in range(1, repeats + 1):
            def add(step, src, cmd, shutter, key, role, _cct=cct, _gm=gm, _repeat=repeat):
                captures.append({
                    "capture_id": (
                        f"{len(captures):03d}-{src}-guide12-w122-cct{_cct}-gm{_gm}"
                        f"-r{_repeat}-{step}"
                    ),
                    "source_id": src,
                    "state_id": f"CCT{_cct}_GM{_gm}_W122_R{_repeat}_{step.upper()}",
                    "role": role,
                    "command": dict(cmd),
                    "exact_command_hash": thermal.canonical_sha256(cmd),
                    "requested_elapsed_s": W12_FAST_DWELL_S,
                    "timing_acceptance": "observed_elapsed_record_only",
                    "formal_measurement": True, "capture_role": "formal",
                    "session_index": len(captures) + 1,
                    "nominal_shutter": shutter,
                    "exposure_cache_key": key,
                    "strip_zero_required": src == "ray",
                    "ray_zero_required": src == "strip",
                    "w122_node": f"{_cct}/{_gm}",
                    "w122_repeat": _repeat,
                    "w122_step": step,
                })
            if cold:
                add("raybefore", "ray", ray_command, W12_RAY_SHUTTERS[ray_key],
                    f"w122-{ray_key}", "ray_reference")
            add("strip", "strip", command, strip_shutter,
                f"w122-strip-white-{cct}-gm{gm}", "strip_lut_command")
            if cold:
                add("rayafter", "ray", ray_command, W12_RAY_SHUTTERS[ray_key],
                    f"w122-{ray_key}", "ray_reference")
    frame_budget = 2 * 70 + 4 * 16
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W122_EXPERIMENT_ID,
        "variant": "p7_td_c_w12_2_verification_v1",
        "stage": f"GUIDE12-W12-2-{batch_name.upper()}",
        "phase": "formal",
        "source": "guide12_w12_2_frozen_lut_20261005",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "observer": thermal.file_reference(thermal.OBSERVER_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "frozen_lut": {"path": "D:/rgbww-optimizer/guide12-w122/derived/"
                          "w12-2-frozen-lut-20261005.json"},
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide12_w122_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "strip_rule": (
                "batch-1 white-line 1/100 default; 1/125 node-level for the "
                "W12 pre-check ceilings and the N2-measured bright 20000K "
                "strip family"
            ),
            "ray_rule": "W2 frozen per-(cct,gm) table (W12_RAY_SHUTTERS)",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0,
            "ambient_cap": 0,
            "physical_cr3_cap": len(captures),
            "setup_physical_cr3_cap": 0,
            "retry": 0,
            "campaign_frame_budget": frame_budget,
            "campaign_frames_scheduled": 185 + 1,
        },
        "execution_authorization": {
            "schema": W122_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W122_EXPERIMENT_ID,
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
            "method": "guide12_w12_2_verification_batch",
            "lut": "w12-2-frozen-lut-20261005.json (commands frozen pre-verification)",
            "per_node": "independent FAST source pairs; needs_two_pairs nodes x2",
            "cold_gate": (
                "cct>=14000K sandwich Ray before/after per strip observation; "
                "reference incompatibility classifies, never silently passes"
            ),
            "s0_reference": "session B frame rides the warm batch",
            "tolerances": dict(W12_TOLERANCES),
        },
    }
