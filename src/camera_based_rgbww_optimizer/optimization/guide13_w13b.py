"""GUIDE13 W13-B: independent-confirmation backfill for corrected white nodes.

The W13-A campaign replaced 23 node commands (qualified in their correction
blocks) and re-qualified 4 originals via session shift; 15 W12-2 changed nodes
still carry only two pairs. GUIDE13 W13-B requires at least 3 independent
pairs per adopted command before a node may carry any confirmation claim.

Measurement contract: identical to the frozen W12-2 verification run (same
FAST sandwich per node - Ray/strip for warm, Ray-before/strip/Ray-after for
>=14000K - same shutters incl. the W12-2 node table overrides, same
isolation and quality semantics), reusing the W12-2 execution schema. The
GUIDE13 identity rides on guide_experiment_id; each strip step records the
exact frozen command and its pair ordinal so the offline analyzer can count
independent pairs without guessing from filenames.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from camera_based_rgbww_optimizer.optimization.guide12 import (
    W122_STRIP_SHUTTER_OVERRIDES,
    W12_FAST_DWELL_S,
    W12_RAY_SHUTTERS,
    W12_TOLERANCES,
)

W13B_EXPERIMENT_ID = "GUIDE13_W13_B_CONFIRMATION_BACKFILL_V1"
W13B_SCHEMA = "direct_guide12_w122_verification_v1"
W13B_COLD_CCT = 14000


def resolve_w13b_ray_shutter(cct: int, gm: int) -> str:
    """W12-2 anchor + same-CCT nearest-gm transfer (frozen rule)."""
    direct = W12_RAY_SHUTTERS.get(f"ray-white-{cct}-gm{gm}")
    if direct:
        return direct
    from camera_based_rgbww_optimizer.optimization.guide12_w123 import (
        resolve_w123_ray_shutter,
    )
    return resolve_w123_ray_shutter(cct, gm)


def build_guide13_w13b_session_plan(
    nodes: list[dict[str, Any]],
    *,
    session_index: int,
    pair_ordinals: tuple[int, ...] = (2, 3),
) -> dict[str, Any]:
    """One W13-B confirmation session: for every (node, ordinal) pair an
    independent FAST sandwich with the frozen adopted command."""
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
        AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
    )

    captures: list[dict[str, Any]] = []
    frozen: dict[str, str] = {}
    for node in nodes:
        cct, gm = int(node["cct"]), int(node["gm"])
        key = f"{cct}/{gm}"
        command = {c: int(v) for c, v in node["command"].items() if c in ("cw", "ww", "r", "g", "b")}
        cache = key.replace("/", "-")
        ray_shutter = resolve_w13b_ray_shutter(cct, gm)
        strip_shutter = W122_STRIP_SHUTTER_OVERRIDES.get((cct, gm)) or "1/100"
        frozen[f"w13b-ray-{cache}"] = ray_shutter
        frozen[f"w13b-strip-{cache}"] = strip_shutter
        ray_command = {"cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct"}
        cold = cct >= W13B_COLD_CCT

        def add(step, src, cmd, shutter, role):
            captures.append({
                "capture_id": (
                    f"{len(captures):03d}-{src}-guide13-w13b-cct{cct}-gm{gm}"
                    f"-p{ordinal}-{step}"
                ),
                "source_id": src,
                "state_id": f"CCT{cct}_GM{gm}_W13B_S{session_index}_P{ordinal}_{step.upper()}",
                "role": role, "command": dict(cmd),
                "exact_command_hash": thermal.canonical_sha256(cmd),
                "requested_elapsed_s": W12_FAST_DWELL_S,
                "timing_acceptance": "observed_elapsed_record_only",
                "formal_measurement": True, "capture_role": "formal",
                "session_index": len(captures) + 1,
                "nominal_shutter": shutter,
                "exposure_cache_key": f"w13b-{src}-{cache}",
                "strip_zero_required": src == "ray",
                "ray_zero_required": src == "strip",
                "w13b_node": key, "w13b_pair_ordinal": ordinal, "w13b_step": step,
                "w13b_frozen_command": dict(command),
            })

        for ordinal in pair_ordinals:
            if cold:
                add("raybefore", "ray", ray_command, ray_shutter, "ray_reference")
            else:
                add("ray", "ray", ray_command, ray_shutter, "ray_reference")
            add("strip", "strip", command, strip_shutter, "strip_confirmation")
            if cold:
                add("rayafter", "ray", ray_command, ray_shutter, "ray_reference")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W13B_EXPERIMENT_ID,
        "variant": "guide13_w13_b_confirmation_backfill_v1",
        "stage": "GUIDE13-W13-B-CONFIRMATION",
        "phase": "formal",
        "source": "guide13_w13b_session_20261016",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "corrected_lut": {"path": "D:/rgbww-optimizer/guide13-w13a/derived/"
                              "w13a-corrected-lut-v2-20261016.json"},
        },
        "captures": captures,
        "capture_ids": [str(step["capture_id"]) for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide13_w13b_reset600_D120",
        "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
            "ray_rule": "W12-2 anchors + same-CCT nearest-gm transfer",
            "strip_rule": "W12-2 node override table else 1/100 white-line anchor",
        },
        "budgets": {
            "formal_cap": len(captures),
            "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": len(captures), "setup_physical_cr3_cap": 0,
            "retry": 0,
            "pair_budget_note": "per-node cap 3 independent pairs total across W13-A block + W13-B sessions",
        },
        "execution_authorization": {
            "schema": W13B_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W13B_EXPERIMENT_ID,
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
            "method": "guide13_w13_b_confirmation_backfill",
            "nodes": [f"{n['cct']}/{n['gm']}" for n in nodes],
            "pair_ordinals": list(pair_ordinals),
            "tolerances": dict(W12_TOLERANCES),
            "gate": "E<=1 per pair; node confirmed at >=3 independent pairs (W13-A block photo counts as ordinal 1)",
            "steady_claim": False,
        },
        "cleanup": {
            "python_finally": "required",
            "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
    }
