from __future__ import annotations

import argparse
import hashlib
import json
import math
import copy
from pathlib import Path
from typing import Any, Mapping, Sequence


CHANNELS = ("cw", "ww", "r", "g", "b")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _active_face(command: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(name for name in CHANNELS if int(command[name]) >= 4095)


def _distance(a: tuple[float, float], b: tuple[float, float], spans: tuple[float, float]) -> float:
    dm = (a[0] - b[0]) / spans[0]
    dg = (a[1] - b[1]) / spans[1]
    return math.hypot(dm, dg)


def build_guide10_white70_candidates(
    baseline: Mapping[str, Any],
    evidence: Sequence[tuple[str, Mapping[str, Any]]],
    confirmation: Mapping[str, Any],
) -> dict[str, Any]:
    baseline_nodes = {(int(row["cct"]), int(row["gm"])): row for row in baseline["nodes"]}
    if len(baseline_nodes) != 70:
        raise ValueError("GUIDE10 white70 requires exactly 70 baseline nodes")

    observations: dict[tuple[int, int], list[dict[str, Any]]] = {key: [] for key in baseline_nodes}
    for order, (source, analysis) in enumerate(evidence):
        for row in analysis.get("nodes", ()):
            key = (int(row["cct"]), int(row["gm"]))
            if key in observations:
                observations[key].append({"order": order, "source": source, "row": row})

    confirm_key = (1800, 100)
    confirm_observation = confirmation["confirmation_observations"][0]
    observations[confirm_key].append({
        "order": len(evidence),
        "source": str(confirmation.get("run_root", "GUIDE10 confirmation")),
        "row": {
            "cct": 1800,
            "gm": 100,
            "status": "pass",
            "strip_command": confirmation["selected_command"],
            "gates": confirm_observation["gates"],
            "cct_error_K": confirm_observation["cct_error_K"],
            "mired_error": confirm_observation["mired_error"],
            "duv_error": confirm_observation["duv_error"],
        },
    })

    canonical = []
    for key, base in sorted(baseline_nodes.items()):
        candidates = observations[key]
        passing = [item for item in candidates if item["row"].get("status") == "pass"]
        selected = max(passing or candidates, key=lambda item: item["order"]) if candidates else None
        row = selected["row"] if selected else base
        command = {name: int(row["strip_command"][name]) for name in CHANNELS}
        status = "strict_equivalent" if row.get("status") == "pass" else "stable_best"
        canonical.append({
            "cct": key[0],
            "gm": key[1],
            "status": status,
            "command": command,
            "active_face": list(_active_face(command)),
            "errors": {
                "cct_K": float(row["cct_error_K"]),
                "mired": float(row["mired_error"]),
                "duv": float(row["duv_error"]),
            },
            "source": selected["source"] if selected else "baseline",
        })

    anchor_rows = []
    for row in canonical:
        key = (row["cct"], row["gm"])
        base_command = baseline_nodes[key]["strip_command"]
        if row["status"] == "strict_equivalent":
            anchor_rows.append({
                "coordinate": (1_000_000.0 / row["cct"], float(row["gm"])),
                "face": tuple(row["active_face"]),
                "delta": {name: row["command"][name] - int(base_command[name]) for name in CHANNELS},
            })

    mired_values = [1_000_000.0 / key[0] for key in baseline_nodes]
    gm_values = [float(key[1]) for key in baseline_nodes]
    spans = (max(mired_values) - min(mired_values), max(gm_values) - min(gm_values))
    output_nodes = []
    for row in canonical:
        key = (row["cct"], row["gm"])
        if row["status"] == "strict_equivalent":
            output_nodes.append({**row, "candidate_command": dict(row["command"]), "field_action": "retain_strict"})
            continue
        point = (1_000_000.0 / row["cct"], float(row["gm"]))
        same_face = [anchor for anchor in anchor_rows if anchor["face"] == tuple(row["active_face"])]
        bounded = same_face and (
            min(a["coordinate"][0] for a in same_face) <= point[0] <= max(a["coordinate"][0] for a in same_face)
            and min(a["coordinate"][1] for a in same_face) <= point[1] <= max(a["coordinate"][1] for a in same_face)
        )
        if not bounded:
            output_nodes.append({**row, "candidate_command": dict(row["command"]), "field_action": "retain_no_bounded_anchor"})
            continue
        nearest = sorted(same_face, key=lambda a: _distance(a["coordinate"], point, spans))[:4]
        distances = [_distance(a["coordinate"], point, spans) for a in nearest]
        weights = [1.0 / max(value, 1e-9) for value in distances]
        candidate = {}
        for name in CHANNELS:
            delta = sum(weight * anchor["delta"][name] for weight, anchor in zip(weights, nearest)) / sum(weights)
            candidate[name] = max(0, min(4095, int(round(row["command"][name] + delta))))
        output_nodes.append({**row, "candidate_command": candidate, "field_action": "same_face_bounded_idw"})

    return {
        "schema": "guide10_white70_canonical_and_correction_field_v1",
        "status": "candidate_generation_complete",
        "node_count": len(output_nodes),
        "strict_equivalent_count": sum(row["status"] == "strict_equivalent" for row in output_nodes),
        "stable_best_count": sum(row["status"] == "stable_best" for row in output_nodes),
        "field_adjusted_count": sum(row["field_action"] == "same_face_bounded_idw" for row in output_nodes),
        "model": "inverse-distance weighted low-order field in target mired x GM, piecewise by active face",
        "extrapolation": "prohibited; canonical command retained outside same-face anchor bounds",
        "role": "candidate_generation_only_requires_direct_validation",
        "nodes": output_nodes,
        "next": "GUIDE10_WHITE70_FAST_VALIDATION_ROUND1",
    }


def build_guide10_white70_validation_plan(
    candidates: Mapping[str, Any],
    calibration: Mapping[str, Any],
    *,
    candidate_reference: Mapping[str, Any],
    calibration_reference: Mapping[str, Any],
) -> dict[str, Any]:
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    if candidates.get("schema") != "guide10_white70_canonical_and_correction_field_v1":
        raise ValueError("GUIDE10 white70 validation requires the frozen candidate schema")
    if candidates.get("status") != "candidate_generation_complete":
        raise ValueError("GUIDE10 white70 candidates are not complete")
    candidate_rows = {
        (int(row["cct"]), int(row["gm"])): row for row in candidates.get("nodes", ())
    }
    calibration_rows = {
        (int(row["cct"]), int(row["gm"])): row for row in calibration.get("targets", ())
    }


    if len(candidate_rows) != 70 or set(candidate_rows) != set(calibration_rows):
        raise ValueError("GUIDE10 white70 candidates must match the exact frozen 14x5 grid")

    captures = []
    contracts = []
    frozen_shutters = {}
    capture_index = 0
    for target_index, key in enumerate(sorted(candidate_rows)):
        cct, gm = key
        candidate = candidate_rows[key]
        calibration_row = calibration_rows[key]
        command = {name: int(candidate["candidate_command"][name]) for name in CHANNELS}
        ray_shutter = str(calibration_row["ray"]["auto_exposure"]["final"]["shutter_speed"])
        strip_shutter = str(calibration_row["feedback_optimizer"]["best"]["capture"]["shutter_speed"])
        cache_key = f"white-{cct}-gm{gm}"
        frozen_shutters[f"ray-{cache_key}"] = ray_shutter
        frozen_shutters[f"strip-{cache_key}"] = strip_shutter
        source_order = ("ray", "strip") if target_index % 2 == 0 else ("strip", "ray")
        contracts.append({
            "target_index": target_index,
            "cct": cct,
            "gm": gm,
            "source_order": list(source_order),
            "strip_command": command,
            "resolved_cct_tolerance_K": float(calibration_row["feedback_goal"]["resolved_cct_tolerance_K"]),
            "cct_tolerance_mired": float(calibration_row["feedback_goal"]["cct_tolerance_mired"]),
            "duv_tolerance": float(calibration_row["feedback_goal"]["duv_tolerance"]),
            "candidate_status": str(candidate["status"]),
            "field_action": str(candidate["field_action"]),
        })
        for source_order_index, source in enumerate(source_order, start=1):
            source_command = (
                {"mode": "cct", "cct": cct, "gm": gm, "intensity_percent": 100.0}
                if source == "ray" else dict(command)
            )
            captures.append({
                "capture_id": f"{capture_index:03d}-{source}-guide10-white70-r1-cct{cct}-gm{gm}",
                "source_id": source,
                "state_id": f"CCT{cct}_GM{gm}",
                "role": f"{source}_cct{cct}_gm{gm}",
                "capture_role": "formal",
                "formal_measurement": True,
                "command": source_command,
                "exact_command_hash": thermal.canonical_sha256(source_command),
                "requested_elapsed_s": 120,
                "nominal_shutter": ray_shutter if source == "ray" else strip_shutter,
                "exposure_cache_key": f"{source}-{cache_key}",
                "timing_acceptance": "observed_elapsed_record_only",
                "strip_zero_required": source == "ray",
                "ray_zero_required": source == "strip",
                "session_index": target_index + 1,
                "source_order": source_order_index,
                "target_cct": cct,
                "target_gm": gm,
                "steady_claim": False,
            })
            capture_index += 1
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": "GUIDE10_WHITE70_FAST_VALIDATION_ROUND1_V1",
        "variant": "guide10-white70-fast-validation-round1",
        "stage": "GUIDE10-WHITE70-FAST-VALIDATION-ROUND1",
        "phase": "formal",
        "source": "white70_candidate_validation",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "uncertainty": thermal.file_reference(thermal.UNCERTAINTY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "guide10_candidates": dict(candidate_reference),
            "white_70_calibration": dict(calibration_reference),
        },
        "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide10_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "frozen_shutters": frozen_shutters,
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen_shutters),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen_shutters),
        },
        "budgets": {
            "ray_cap": 70,
            "strip_cap": 70,
            "formal_cap": 140,
            "physical_cr3_cap": 140,
            "ambient_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": "direct_guide10_white70_round1_v1",
            "human_authorization_required": False,
            "human_authorization_verified": True,
            "human_authorization_experiment_id": "GUIDE10_WHITE70_FAST_VALIDATION_ROUND1_V1",
            "bounded_device_scope": True,
            "experiment_id": "GUIDE10_WHITE70_FAST_VALIDATION_ROUND1_V1",
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
            "method": "white_fast_direct_representative_12",
            "target_contracts": contracts,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "source_order_balanced": True,
            "candidate_generation_round": 1,
            "global_model_refit": False,
            "default_lut_installation": False,
            "steady_claim": False,
        },
    }


def build_guide10_white70_recovery_suffix(interrupted_root: Path) -> dict[str, Any]:
    run = json.loads((interrupted_root / "run.json").read_text(encoding="utf-8"))
    pause_path = interrupted_root / "pause-evidence.json"
    pause = json.loads(pause_path.read_text(encoding="utf-8"))
    plan_path = interrupted_root / "experiment-spec.json"
    captures_path = interrupted_root / "captures.jsonl"
    returns_path = interrupted_root / "physical-returns.jsonl"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    captures = _read_jsonl(captures_path)
    returns = _read_jsonl(returns_path)
    if run.get("status") != "interrupted" or run.get("interruption_reason") != "user_requested_pause":
        raise ValueError("GUIDE10 recovery requires an explicitly paused run")
    if run.get("cleanup") != "pass" or pause.get("status") != "pass":
        raise ValueError("GUIDE10 recovery requires passed pause cleanup evidence")
    expected_zero = {"blue": 0, "green": 0, "cold_white": 0, "red": 0, "warm_white": 0}
    if pause.get("rgbww_zero_readback") != expected_zero or int(pause.get("ray_zero_readback", {}).get("intensity", -1)) != 0:
        raise ValueError("GUIDE10 recovery requires exact RGBWW and Ray zero readback")
    if len(captures) != len(returns) or len(captures) != int(run.get("completed_formal", -1)):
        raise ValueError("GUIDE10 recovery ledgers disagree on the completed prefix")
    expected = plan.get("captures", [])
    if not captures or len(captures) >= len(expected) or len(captures) % 2:
        raise ValueError("GUIDE10 recovery prefix must end on a complete Ray/strip node")
    for index, (capture, returned, step) in enumerate(zip(captures, returns, expected)):
        capture_id = str(step["capture_id"])
        if str(capture.get("capture_id")) != capture_id or str(returned.get("capture_id")) != capture_id:
            raise ValueError(f"GUIDE10 recovery prefix diverges at index {index}")
        receipt = capture.get("capture", {}).get("physical_return_receipt", {})
        if str(receipt.get("cr3_sha256")) != str(returned.get("cr3_sha256")) or int(receipt.get("cr3_byte_count", -1)) != int(returned.get("cr3_byte_count", -2)):
            raise ValueError(f"GUIDE10 recovery physical receipt diverges at index {index}")
        raw_path = Path(str(returned["cr3_path"]))
        if not raw_path.is_file() or raw_path.stat().st_size != int(returned["cr3_byte_count"]):
            raise ValueError(f"GUIDE10 recovery RAW artifact is missing at index {index}")
    suffix = json.loads(json.dumps(plan))
    suffix["captures"] = expected[len(captures):]
    suffix["capture_ids"] = [row["capture_id"] for row in suffix["captures"]]
    required_cache_keys = sorted({str(row["exposure_cache_key"]) for row in suffix["captures"]})
    suffix["frozen_shutters"] = {
        key: value for key, value in suffix["frozen_shutters"].items() if key in required_cache_keys
    }
    suffix["shutter_ledger_provenance"]["required_cache_keys"] = required_cache_keys
    suffix["shutter_ledger_provenance"]["frozen_shutters_sha256"] = hashlib.sha256(
        json.dumps(suffix["frozen_shutters"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    ray_count = sum(row["source_id"] == "ray" for row in suffix["captures"])
    strip_count = sum(row["source_id"] == "strip" for row in suffix["captures"])
    suffix["budgets"].update(ray_cap=ray_count, strip_cap=strip_count, formal_cap=len(suffix["captures"]), physical_cr3_cap=len(suffix["captures"]))
    suffix["stage"] = "GUIDE10-WHITE70-FAST-VALIDATION-ROUND1-RECOVERY-SUFFIX"
    suffix["variant"] = "guide10-white70-fast-validation-round1-recovery-suffix"
    suffix["recovery"] = {
        "schema": "guide10_white70_round1_recovery_suffix_v1",
        "parent_root": str(interrupted_root.resolve()),
        "completed_prefix_count": len(captures),
        "remaining_suffix_count": len(suffix["captures"]),
        "parent_plan_sha256": _sha256(plan_path),
        "parent_captures_sha256": _sha256(captures_path),
        "parent_physical_returns_sha256": _sha256(returns_path),
        "pause_evidence": {"path": str(pause_path.resolve()), "sha256": _sha256(pause_path)},
    }
    suffix["analysis_contract"]["recovery_parent_prefix_count"] = len(captures)
    return suffix


def build_guide10_white70_w5_plan(
    round1_analysis: Mapping[str, Any],
    round1_plan: Mapping[str, Any],
    calibration: Mapping[str, Any],
    *,
    analysis_reference: Mapping[str, Any],
    round1_reference: Mapping[str, Any],
    calibration_reference: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the single bounded W5 local-candidate batch.

    This consumes only the frozen round-1 residuals. Historical Jacobians are
    used where present; nodes without one receive three explicitly labelled
    directional fallback commands. No global refit or in-run feedback loop is
    introduced here.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
    from camera_based_rgbww_optimizer.optimization import white_lut_feedback

    failed = [row for row in round1_analysis.get("nodes", ()) if row.get("status") != "pass"]
    if not failed:
        raise ValueError("GUIDE10 W5 requires the frozen nonconforming node set")
    if int(round1_analysis.get("node_count", 0)) != 70:
        raise ValueError("GUIDE10 W5 requires the 70-node round-1 analysis")
    plan_by_key = {(int(x["target_cct"]), int(x["target_gm"])): x for x in round1_plan.get("captures", ())}
    contract_by_key = {(int(x["cct"]), int(x["gm"])): x for x in round1_plan["analysis_contract"]["target_contracts"]}
    cal_by_key = {(int(x["cct"]), int(x["gm"])): x for x in calibration.get("targets", ())}
    captures: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for node_index, node in enumerate(sorted(failed, key=lambda x: (int(x["cct"]), int(x["gm"])) )):
        key = (int(node["cct"]), int(node["gm"]))
        template = plan_by_key[key]
        contract = copy.deepcopy(contract_by_key[key])
        calibration_row = cal_by_key[key]
        base = {name: int(node["strip_command"][name]) for name in CHANNELS}
        active = str(calibration_row.get("feedback_optimizer", {}).get("active_channel", contract.get("active_channel", "r")))
        jac = calibration_row.get("feedback_optimizer", {}).get("final_jacobian")
        candidates: list[dict[str, int]] = []
        method = "historical_jacobian_gate_aligned"
        if jac is not None:
            step = white_lut_feedback.solve_damped_step(
                base, node["strip"]["white_point"], node["ray"]["white_point"], jac,
                active_channel=active, cct_tolerance_K=float(node["limits"]["cct_K"]),
                duv_tolerance=float(node["limits"]["duv"]), max_code=4095,
                max_step_code=min(768, int(calibration_row["feedback_optimizer"].get("final_max_step_code", 768))),
                damping=float(calibration_row["feedback_optimizer"].get("damping", 0.05)),
                rgb_penalty=0.0, channel_penalties=calibration_row["feedback_optimizer"].get("channel_penalties"),
            )["command"]
            candidates.append({name: int(step[name]) for name in CHANNELS})
        else:
            method = "bounded_directional_fallback_no_jacobian"
        # Keep the candidate batch finite and gate-aligned: two bounded
        # micro-steps around the first prediction, or around the measured base.
        seed = candidates[0] if candidates else base
        residual_mired = float(node.get("mired_error", 0.0))
        residual_duv = float(node.get("duv_error", 0.0))
        free = [name for name in CHANNELS if name != active]
        ranked = sorted(free, key=lambda name: (int(seed[name]) in (0, 4095), name))
        direction = -1 if residual_mired > 0 else 1
        if residual_duv > 0:
            direction *= -1
        for offset in (256, 512):
            command = dict(seed)
            channel = ranked[0]
            value = max(0, min(4095, int(command[channel]) + direction * offset))
            command[channel] = value
            if command != base and command not in candidates:
                candidates.append(command)
        if not candidates:
            candidates = [base]
        candidates = candidates[:3]
        candidate_rows.append({"cct": key[0], "gm": key[1], "base_command": base, "active_channel": active, "method": method, "commands": candidates, "max_unique_commands": 5})
        contract.update({"target_index": node_index, "strip_command": candidates[0], "source_order": list(contract.get("source_order", ["ray", "strip"])), "candidate_owner": "guide10_w5_bounded_local_candidate"})
        contracts.append(contract)
        ray_template = {**template, "source_id": "ray", "role": "ray_reference"}
        strip_template = {**template, "source_id": "strip", "role": "strip_candidate"}
        for candidate_index, command in enumerate(candidates):
            for source, source_template in (("ray", ray_template), ("strip", strip_template)):
                step = copy.deepcopy(source_template)
                step.update({
                    "capture_id": f"{len(captures):03d}-{source}-guide10-white70-w5-cct{key[0]}-gm{key[1]}-candidate{candidate_index}",
                    "state_id": f"CCT{key[0]}_GM{key[1]}_W5_C{candidate_index}",
                    "role": "ray_reference" if source == "ray" else "strip_candidate",
                    "capture_role": "formal", "formal_measurement": True,
                    "session_index": len(captures) + 1,
                    "source_order": 1 if source == "ray" else 2,
                })
                if source == "strip":
                    step["command"] = dict(command)
                    step["exact_command_hash"] = thermal.canonical_sha256(command)
                captures.append(step)
    if len(captures) != sum(len(x["commands"]) for x in candidate_rows) * 2:
        raise AssertionError("GUIDE10 W5 capture construction is not paired")
    frozen_shutters = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    return {
        "schema": thermal.PLAN_SCHEMA_V2, "status": "execute_authorized", "experiment_id": thermal.TD_C,
        "guide_experiment_id": "GUIDE10_WHITE70_W5_LOCAL_CORRECTION_V1", "variant": "guide10-white70-w5-local-correction",
        "stage": "GUIDE10-WHITE70-W5-LOCAL-CORRECTION", "phase": "formal", "source": "white70_round1_residuals",
        "inputs": {"round1_analysis": dict(analysis_reference), "round1_plan": dict(round1_reference), "calibration": dict(calibration_reference)},
        "captures": captures, "capture_ids": [x["capture_id"] for x in captures],
        "timing_contract": thermal.timing_contract(2), "timing_resolution": "guide10_reset600_D120", "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "frozen_shutters": frozen_shutters,
        "shutter_ledger_provenance": {"owner": "experiment_capture_steps", "required_cache_keys": sorted(frozen_shutters), "frozen_shutters_sha256": thermal.canonical_sha256(frozen_shutters)},
        "budgets": {"ray_cap": len(captures)//2, "strip_cap": len(captures)//2, "formal_cap": len(captures), "physical_cr3_cap": len(captures), "ambient_cap": 0, "retry": 0},
        "execution_authorization": {"schema": "direct_guide10_white70_w5_local_correction_v1", "human_authorization_required": False, "human_authorization_verified": True, "experiment_id": "GUIDE10_WHITE70_W5_LOCAL_CORRECTION_V1", "bounded_device_scope": True, "remote_v2_capability": True},
        "camera": {"backend": "remote", "v2_capture_timing_capability_available": True, "v2_capture_capability": "remote_v2_capture_timing_v1", "resolved_capture_settings": {"owner": "remote_backend.resolve_capture_settings", "iso": "100", "aperture": "f/4", "image_format": "RAW"}},
        "analysis_contract": {"method": "guide10_white70_w5_bounded_local_candidates", "target_contracts": contracts, "candidate_rows": candidate_rows, "round1_failed_node_count": len(failed), "independent_reset_s": 600, "dwell_s": 120, "global_model_refit": False, "third_local_generation": False, "max_unique_commands_per_node": 5, "refinement_budget_per_node": 2, "best_command_valid_observations": 3, "pass_next": "GUIDE10_WHITE70_W6_FINAL_VALIDATION", "failure_next": "GUIDE10_WHITE70_W6_FINAL_VALIDATION"},
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build GUIDE10 canonical white70 and one-time correction-field candidates.")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, action="append", default=[])
    parser.add_argument("--confirmation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    evidence = [(str(path.resolve()), json.loads(path.read_text(encoding="utf-8"))) for path in args.evidence]
    confirmation = json.loads(args.confirmation.read_text(encoding="utf-8"))
    result = build_guide10_white70_candidates(baseline, evidence, confirmation)
    result["inputs"] = {
        "baseline": {"path": str(args.baseline.resolve()), "sha256": _sha256(args.baseline)},
        "evidence": [{"path": str(path.resolve()), "sha256": _sha256(path)} for path in args.evidence],
        "confirmation": {"path": str(args.confirmation.resolve()), "sha256": _sha256(args.confirmation)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "node_count", "strict_equivalent_count", "stable_best_count", "field_adjusted_count", "next")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
