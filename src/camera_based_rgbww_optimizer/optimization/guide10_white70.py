from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


CHANNELS = ("cw", "ww", "r", "g", "b")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
