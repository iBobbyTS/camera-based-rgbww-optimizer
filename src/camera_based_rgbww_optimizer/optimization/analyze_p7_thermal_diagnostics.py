from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    calibrate_direct_limits,
    direct_whitened_norm,
    ordered_unit_shape,
)
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import (
    DEFAULT_P6_RUN,
    load_ray_repeat_groups,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.optimization.analyze_hsi_reference_repeatability import (
    write_reference_epoch_v2_derived,
)


def analyze_thermal_run(
    run_dir: str | Path,
    *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
) -> dict[str, Any]:
    root = Path(run_dir)
    plan = _load_json(root / "plan.json")
    run = _load_json(root / "run.json")
    if plan.get("experiment_id") not in thermal.EXPERIMENT_IDS or run.get("status") != "complete":
        raise ValueError("thermal analyzer requires a completed exact experiment")
    _verify_frozen_inputs(plan["inputs"])
    if plan.get("timing_contract") != {
        "name": "best_effort_gphoto2_v1",
        "decision_owner": "Developer/Human",
        "network_assumption": "wired_lan_latency_negligible_developer_decision",
        "accepted_tiers": ["tier_a", "tier_b"],
        "absolute_exposure_start_required": False,
        "absolute_exposure_start": False,
        "provenance": "best_effort_gphoto2_exposure_start_estimate",
    }:
        raise ValueError("thermal timing contract differs from frozen best-effort contract")
    capture_settings = _validate_capture_settings_provenance(plan, run)
    captures = _load_jsonl(root / "captures.jsonl")
    covariates = _load_jsonl(root / "thermal-covariates.jsonl")
    commands = _load_jsonl(root / "commands.jsonl")
    isolation = _load_jsonl(root / "isolation-gates.jsonl")
    if len(captures) != len(plan["captures"]) or len(covariates) != len(captures):
        raise ValueError("thermal capture/covariate count differs from frozen plan")
    if [row.get("capture_id") for row in captures] != [row.get("capture_id") for row in plan["captures"]]:
        raise ValueError("thermal capture evidence is missing, duplicated, or reordered")
    if any(not row.get("timing_valid") for row in captures):
        raise ValueError("thermal run contains a missed-timing capture")
    expected_gate_ids = ["run_start"] + [
        str(gate_id) for step in plan["captures"]
        for gate_id in (step.get("isolation_gate_before"), step.get("isolation_gate_after"))
        if gate_id
    ]
    if [row.get("gate_id") for row in isolation] != expected_gate_ids:
        raise ValueError("thermal source-isolation gate ledger differs from frozen plan")
    curve = _load_json(Path(plan["inputs"]["code_duty_curve"]["path"]))
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
    for row in isolation:
        evidence = row.get("evidence") or {}
        if evidence.get("status") != "pass" or evidence.get("strip_verified_off") is not True or evidence.get("ray_verified_off") is not True:
            raise ValueError("thermal source-isolation gate did not pass")
        validate_both_off(
            evidence.get("strip_device_evidence", {}), evidence.get("ray_readback", {}), curve,
        )
    expected_commands = [group[0] for group in _formal_groups(plan["captures"])]
    if len(commands) != len(expected_commands):
        raise ValueError("thermal command/readback ledger count differs from frozen plan")
    for expected, item in zip(expected_commands, commands, strict=True):
        if (
            item.get("event") != "command_readback_verified"
            or item.get("source_id") != expected.get("source_id")
            or item.get("state_id") != expected.get("state_id")
            or item.get("exact_command_hash") != expected.get("exact_command_hash")
            or not isinstance(item.get("applied"), Mapping)
            or not isinstance(item.get("readback"), Mapping)
        ):
            raise ValueError("thermal command/readback evidence differs from frozen plan")
    if not (root / "commands-audit.json").is_file() or _load_json(root / "commands-audit.json").get("status") != "pass":
        raise ValueError("thermal command audit artifact is missing")
    if not (root / "all-off-python.json").is_file() or not (root / "all-off-shell.json").is_file():
        raise ValueError("thermal analyzer requires Python and shell cleanup artifacts")
    thermal.audit_chronology(covariates)
    recomputed_formal = 0
    recomputed_ambient = 0
    recomputed_physical = 0
    formal_captures = []
    ambient_captures = []
    timing_tiers: dict[str, int] = defaultdict(int)
    timing_unknown = 0
    for step, capture, covariate in zip(plan["captures"], captures, covariates, strict=True):
        if capture.get("plan_step") != step or capture.get("source_id") != step.get("source_id"):
            raise ValueError("thermal capture owner or frozen step mismatch")
        if capture.get("capture_role") != step.get("capture_role") or bool(capture.get("formal_measurement")) != bool(step.get("formal_measurement")):
            raise ValueError("thermal capture formal/ambient role mismatch")
        payload = capture.get("capture") or {}
        camera_capture = payload.get("capture")
        if not isinstance(camera_capture, Mapping) or any(
            camera_capture.get(key) != capture_settings[key]
            for key in ("iso", "aperture", "image_format")
        ):
            raise ValueError("thermal capture settings differ from resolved remote provenance")
        if step["formal_measurement"]:
            requested = float(step["requested_elapsed_s"])
            actual = float(capture["actual_elapsed_s"])
            error = float(capture["timing_error_s"])
            if abs((actual - requested) - error) > 1e-9 or abs(error) > float(step["timing_tolerance_s"]):
                raise ValueError("thermal capture timing evidence is inconsistent")
            recomputed_formal += 1
            formal_captures.append(capture)
            expected_command = step["command"]
        else:
            if capture.get("actual_elapsed_s") is not None or capture.get("timing_error_s") is not None:
                raise ValueError("ambient capture cannot masquerade as a timed formal capture")
            if not isinstance(payload.get("ambient_diagnostic"), Mapping):
                raise ValueError("ambient capture lacks ambient_diagnostic payload")
            if payload.get("feature_values") is not None or capture.get("feature_values") is not None:
                raise ValueError("ambient capture cannot enter the formal 58-feature ledger")
            recomputed_ambient += 1
            ambient_captures.append(capture)
            expected_command = {"strip": "off", "ray": "off"}
        thermal.validate_covariate_record(covariate, expected_command=expected_command)
        if covariate["source_id"] != step["source_id"] or covariate["state_id"] != step["state_id"]:
            raise ValueError("thermal covariate source/state owner mismatch")
        raw_path = payload.get("saved_file") or (payload.get("capture") or {}).get("saved_file")
        if not raw_path or not Path(raw_path).is_file() or Path(raw_path).stat().st_size <= 0:
            raise ValueError("thermal capture lacks retained nonempty CR3 provenance")
        timing = _replay_timing_evidence(capture, payload, Path(raw_path), root)
        timing_tiers[str(timing["tier"])] += 1
        if timing["tier"] == "tier_c":
            timing_unknown += 1
        stored_timing = capture.get("timing_evidence")
        if not isinstance(stored_timing, Mapping) or dict(stored_timing) != timing:
            raise ValueError("thermal timing evidence differs from independent replay")
        capture_actual = timing.get("best_effort_elapsed_s")
        if step["formal_measurement"] and capture_actual is not None:
            expected_error = None if step.get("requested_elapsed_s") is None else float(capture_actual) - float(step["requested_elapsed_s"])
            if capture.get("actual_elapsed_s") != capture_actual or capture.get("timing_error_s") != expected_error:
                raise ValueError("thermal timing elapsed or error was self-reported inconsistently")
        exposure = payload.get("recorded_exposure") or payload.get("exposure_metadata") or {}
        if exposure.get("status") != "recorded":
            raise ValueError("thermal capture lacks recorded exposure provenance")
        physical = int(payload.get("physical_capture_count", 1))
        if physical != 1:
            raise ValueError("thermal fixed capture physical count must equal one")
        recomputed_physical += physical
    if recomputed_formal != int(plan["budgets"]["formal_cap"]) or int(run.get("completed_formal", -1)) != recomputed_formal:
        raise ValueError("thermal formal ledger count mismatch")
    if recomputed_ambient != int(plan["budgets"]["ambient_cap"]) or int(run.get("ambient_capture_count", -1)) != recomputed_ambient:
        raise ValueError("thermal ambient ledger count mismatch")
    if recomputed_physical != int(run.get("physical_cr3_count", -1)) or recomputed_physical > int(plan["budgets"]["physical_cr3_cap"]):
        raise ValueError("thermal physical CR3 ledger mismatch")
    if list(root.rglob("*.npy")):
        raise ValueError("thermal diagnostics retain zero NPY files")

    experiment = str(plan["experiment_id"])
    compatibility = compatibility_fn or frozen_same_state_compatibility(
        source=str(plan.get("source") or "ray"), feature_ids=feature_ids,
    )
    if experiment == thermal.TD_A:
        result = analyze_td_a(formal_captures, feature_ids=feature_ids, compatibility_fn=compatibility)
    elif experiment == thermal.TD_B:
        result = analyze_td_b(formal_captures, feature_ids=feature_ids, compatibility_fn=compatibility_fn)
    else:
        result = analyze_td_c(
            formal_captures, ambients=ambient_captures, feature_ids=feature_ids,
            p6_compare_fn=lambda rows: compare_current_ray_center_to_p6(rows, feature_ids),
        )
    return {
        "schema": "p7_thermal_diagnostic_analysis_v1", "experiment_id": experiment,
        "capture_contract": "pass", "timing_contract": "pass",
        "covariate_contract": "pass", "source_isolation_contract": "pass",
        "formal_capture_count": recomputed_formal, "ambient_capture_count": recomputed_ambient,
        "physical_cr3_count": recomputed_physical, "retained_npy_count": 0,
        "timing_absolute_truth": False,
        "timing_source": "best_effort_gphoto2",
        "tier_distribution": dict(timing_tiers),
        "unknown_uncertainty_count": timing_unknown,
        **result,
    }


def _validate_capture_settings_provenance(
    plan: Mapping[str, Any], run: Mapping[str, Any],
) -> dict[str, str]:
    camera = plan.get("camera")
    settings = camera.get("resolved_capture_settings") if isinstance(camera, Mapping) else None
    if not isinstance(settings, Mapping):
        raise ValueError("thermal plan lacks resolved remote capture settings provenance")
    expected = {
        "owner": "remote_backend.resolve_capture_settings",
        "iso": settings.get("iso"),
        "aperture": settings.get("aperture"),
        "image_format": settings.get("image_format"),
    }
    if (
        dict(settings) != expected
        or any(not isinstance(expected[key], str) or not expected[key].strip() for key in ("iso", "aperture"))
        or expected["image_format"] != "RAW"
        or run.get("capture_settings_provenance") != expected
    ):
        raise ValueError("thermal run capture settings provenance is inconsistent")
    return expected


def _replay_timing_evidence(
    capture: Mapping[str, Any], payload: Mapping[str, Any], raw_path: Path, run_root: Path,
) -> dict[str, Any]:
    metadata_path = payload.get("remote_metadata_path")
    if not isinstance(metadata_path, str):
        raise ValueError("thermal capture lacks retained remote v2 metadata path")
    root = run_root.resolve()
    resolved_raw = raw_path.resolve()
    resolved_metadata = Path(metadata_path).resolve()
    if not resolved_raw.is_relative_to(root) or not resolved_metadata.is_relative_to(root):
        raise ValueError("thermal v2 CR3/sidecar owner is outside the current run")
    expected_metadata = resolved_raw.with_suffix(resolved_raw.suffix + ".metadata.json")
    if resolved_metadata != expected_metadata:
        raise ValueError("thermal v2 sidecar path does not belong to the retained CR3")
    sidecar = _load_json(resolved_metadata)
    remote_metadata, receipt = camera_remote_v2.split_and_validate_sidecar(
        sidecar, payload=resolved_raw.read_bytes(),
    )
    duplicate_metadata = payload.get("timing_metadata")
    if not isinstance(duplicate_metadata, Mapping) or dict(duplicate_metadata) != sidecar:
        raise ValueError("thermal duplicate timing metadata differs from retained sidecar")
    timing = receipt.get("timing_evidence")
    if not isinstance(timing, Mapping):
        raise ValueError("thermal v2 metadata lacks local timing evidence")
    if receipt.get("received_monotonic_s") != receipt.get("local_response_received_monotonic_s"):
        raise ValueError("thermal v2 successful-attempt response timing is inconsistent")
    replayed = camera_remote_v2.reconstruct_best_effort_timing(
        remote_metadata,
        local_request_started_monotonic_s=float(receipt["local_request_started_monotonic_s"]),
        local_response_received_monotonic_s=float(receipt["local_response_received_monotonic_s"]),
        local_readback_done_monotonic_s=float(timing["local_readback_done_monotonic_s"]),
    )
    if dict(timing) != replayed:
        raise ValueError("thermal local timing receipt was tampered")
    return replayed


def analyze_td_a(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
) -> dict[str, Any]:
    cycles: dict[str, dict[int, list[Mapping[str, float]]]] = defaultdict(lambda: defaultdict(list))
    for row in captures:
        step = row["plan_step"]
        features = _features(row, feature_ids)
        cycles[str(step["cycle_index"])][int(step["requested_elapsed_s"])].append(features)
    settling = thermal.settle_from_cycles(cycles, feature_ids, compatibility_fn=compatibility_fn)
    groups = {
        f"cycle-{cycle}": [features for point in sorted(points) for features in points[point]]
        for cycle, points in cycles.items()
    }
    audit = thermal.summarize_group_audit(groups, feature_ids)
    if audit["trend_failed"] or audit["dominance_failed"]:
        settling = {"status": "settling_not_demonstrated_by_600", "t_settle_s": None, "six_hundred_is_validation_only": True}
    return {
        "status": "td_a_pass" if settling["t_settle_s"] is not None else settling["status"],
        "within_cycle_settling": settling,
        "between_cycle_repeatability": audit,
        "state_specific_settle_time": {"A": settling["t_settle_s"]},
        "source_specific_settle_time": settling["t_settle_s"],
        "temperature_not_sufficient_proxy": False,
    }


def analyze_td_b(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
) -> dict[str, Any]:
    source = str(captures[0]["plan_step"].get("source_id", "ray")) if captures else "ray"
    anchor_compatibility = compatibility_fn or frozen_same_state_compatibility(
        source=source, state="A", feature_ids=feature_ids,
    )
    state_points: dict[str, dict[int, list[Mapping[str, float]]]] = defaultdict(lambda: defaultdict(list))
    anchors: list[np.ndarray] = []
    for row in captures:
        step = row["plan_step"]
        feature = _features(row, feature_ids)
        if step.get("role") in {"initial_anchor", "return_after_D", "return_after_B", "return_after_C"}:
            anchors.append(_unit(feature, feature_ids))
        else:
            state_points[str(step["state_id"])][int(step["requested_elapsed_s"])].append(feature)
    history_pass = thermal._all_pairs(anchors, anchor_compatibility)
    state_results = {
        state: thermal.settle_from_cycles(
            {"switch": points}, feature_ids,
            compatibility_fn=(compatibility_fn or frozen_same_state_compatibility(
                source=source, state=state, feature_ids=feature_ids,
            )),
        )
        for state, points in state_points.items()
    }
    status = "td_b_pass"
    if not history_pass:
        status = "history_dependent_at_current_protocol"
    elif any(result["t_settle_s"] is None for result in state_results.values()):
        status = "stop_thermal_extension_required"
    return {
        "status": status, "return_anchor_history_effect": "pass" if history_pass else "fail",
        "state_specific_settle_time": {state: result["t_settle_s"] for state, result in state_results.items()},
    }


def analyze_td_c(
    captures: Sequence[Mapping[str, Any]], *, ambients: Sequence[Mapping[str, Any]],
    feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    p6_compare_fn: Callable[[Sequence[Mapping[str, Any]]], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    compatibility = compatibility_fn or frozen_same_state_compatibility(source="ray", feature_ids=feature_ids)
    sessions: dict[tuple[str, int], dict[str, Any]] = defaultdict(dict)
    for row in captures:
        step = row["plan_step"]
        session = sessions[(str(step["state_id"]), int(step["session_index"]))]
        session[str(step["source_id"])] = _unit(_features(row, feature_ids), feature_ids)
        if int(step["source_order"]) == 1:
            session["order"] = f"{step['source_id']}_first"
    difference_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
    ray_centers: dict[str, list[np.ndarray]] = defaultdict(list)
    strip_centers: dict[str, list[np.ndarray]] = defaultdict(list)
    order_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
    for (state, _session), sources in sorted(sessions.items()):
        if set(sources) != {"ray", "strip", "order"}:
            raise ValueError("TD-C session lacks exactly one Ray and one strip capture")
        difference = sources["strip"] - sources["ray"]
        difference_vectors[state].append(difference)
        ray_centers[state].append(sources["ray"])
        strip_centers[state].append(sources["strip"])
        order_vectors[str(sources["order"])].append(difference)
    compatibility_pass = all(thermal._all_pairs(values, compatibility) for values in difference_vectors.values())
    stable_center_pass = all(
        thermal._all_pairs(ray_centers[state], compatibility) and thermal._all_pairs(strip_centers[state], compatibility)
        for state in difference_vectors
    )
    ray_first = order_vectors.get("ray_first", [])
    strip_first = order_vectors.get("strip_first", [])
    order_pass = bool(ray_first and strip_first) and compatibility(
        np.mean(np.vstack(ray_first), axis=0), np.mean(np.vstack(strip_first), axis=0),
    )
    p6 = dict(p6_compare_fn(captures)) if p6_compare_fn is not None else {"status": "not_evaluated"}
    ambient = analyze_ambient_trend(ambients)
    gates = {
        "compatibility": "pass" if compatibility_pass else "fail",
        "order_effect": "pass" if order_pass else "fail",
        "stable_center": "pass" if stable_center_pass else "fail",
        "p6_interpretability": "pass" if p6.get("status") == "pass" else "fail",
        "ambient_trend": ambient["status"],
    }
    failures = [name for name, decision in gates.items() if decision != "pass"]
    return {
        "status": "td_c_core_pass_waiting_for_planner" if not failures else "td_c_gate_failed",
        "failure_branches": failures, "gates": gates,
        "within_session_compatibility": {"status": gates["compatibility"]},
        "balanced_order_effect": {"status": gates["order_effect"], "design": "ray_first_vs_strip_first"},
        "stable_center": {"status": gates["stable_center"]},
        "current_stable_center_vs_p6": p6,
        "ambient_trend": ambient,
        "comparison_design": "order_balanced_paired_comparison_not_classic_abba",
    }


def analyze_ambient_trend(ambients: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not ambients:
        return {"status": "fail", "reason": "missing_ambient_evidence"}
    payloads = [(row.get("capture") or {}).get("ambient_diagnostic") or row.get("ambient_diagnostic") for row in ambients]
    if any(not isinstance(value, Mapping) for value in payloads):
        return {"status": "fail", "reason": "invalid_ambient_diagnostic"}
    geometry = {str(value.get("geometry_hash")) for value in payloads}
    black = np.asarray([value.get("black_levels") for value in payloads], dtype=float)
    if black.ndim != 2 or np.any(~np.isfinite(black)):
        return {"status": "fail", "reason": "invalid_black_level_provenance"}
    tolerance = min(float(value.get("black_level_tolerance_dn", 0.0)) for value in payloads)
    span = float(np.max(np.ptp(black, axis=0)))
    passed = len(geometry) == 1 and span <= tolerance
    return {
        "status": "pass" if passed else "fail", "geometry_hash_count": len(geometry),
        "black_level_max_span_dn": span, "black_level_tolerance_dn": tolerance,
    }


def _features(row: Mapping[str, Any], feature_ids: Sequence[str]) -> Mapping[str, float]:
    values = row.get("feature_values") or (row.get("capture") or {}).get("feature_values")
    if not isinstance(values, Mapping) or set(values) != set(feature_ids):
        raise ValueError("thermal capture lacks exact frozen feature provenance")
    return {key: float(values[key]) for key in feature_ids}


def _unit(row: Mapping[str, float], feature_ids: Sequence[str]) -> np.ndarray:
    return ordered_unit_shape(row, feature_ids)


def frozen_same_state_compatibility(
    *, source: str, feature_ids: Sequence[str], state: str = "A",
) -> Callable[[Sequence[float], Sequence[float]], bool]:
    policy = _load_json(thermal.POLICY_PATH)
    if source == "ray":
        variance = np.asarray(policy["reference_policy"]["ray_within_state_diagonal_variance"], dtype=float)
    else:
        class_name = {
            "A": "sat100_fullscale", "D": "mid_sat_fullscale",
            "B": "neutral_fullscale", "C": "sat100_fullscale",
        }[state]
        variance = np.asarray(policy["repeatability_policy"]["classes"][class_name]["p1_floor_diagonal_variance"], dtype=float)
    pair_variance = 2.0 * variance

    def compatible(left: Sequence[float], right: Sequence[float]) -> bool:
        left_values = np.asarray(left, dtype=float)
        limits = calibrate_direct_limits(left_values, pair_variance, samples=1000)
        score = direct_whitened_norm(np.asarray(right, dtype=float) - left_values, pair_variance)
        return score <= float(limits["guarded_limit"])

    return compatible


def compare_current_ray_center_to_p6(
    captures: Sequence[Mapping[str, Any]], feature_ids: Sequence[str],
) -> dict[str, Any]:
    manifold = RayHsiManifold.load(thermal.MANIFOLD_PATH)
    p6 = load_ray_repeat_groups(manifold, DEFAULT_P6_RUN)
    output = {}
    compatibility = frozen_same_state_compatibility(source="ray", feature_ids=feature_ids)
    state_coordinates = {"A": (120, 100), "B": (0, 0), "C": (300, 100), "D": (120, 50)}
    for state in sorted({str(row["plan_step"]["state_id"]) for row in captures}):
        current = np.mean(np.vstack([
            _unit(_features(row, feature_ids), feature_ids)
            for row in captures if row["source_id"] == "ray" and row["plan_step"]["state_id"] == state
        ]), axis=0)
        hue, sat = state_coordinates[state]
        frozen_rows = p6[f"p6:h{hue}:s{sat}"]
        frozen = np.mean(np.asarray(frozen_rows, dtype=float), axis=0)
        output[state] = {"decision": "pass" if compatibility(frozen, current) else "fail"}
    return {"status": "pass" if all(item["decision"] == "pass" for item in output.values()) else "fail", "states": output}


def _verify_frozen_inputs(inputs: Mapping[str, Any]) -> None:
    for name, reference in inputs.items():
        path = Path(reference["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
            raise ValueError(f"thermal frozen input hash drift: {name}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _formal_groups(captures: Sequence[Mapping[str, Any]]) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if not step.get("formal_measurement"):
            continue
        key = (step.get("source_id"), step.get("state_id"), step.get("cycle_index"), step.get("role"))
        if groups:
            previous = groups[-1][0]
            previous_key = (
                previous.get("source_id"), previous.get("state_id"),
                previous.get("cycle_index"), previous.get("role"),
            )
        else:
            previous_key = None
        if groups and key == previous_key and float(step["requested_elapsed_s"]) > float(groups[-1][-1]["requested_elapsed_s"]):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze P7 thermal diagnostics or derive P7-R1 epoch-v2 evidence.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--feature-ids", type=Path)
    parser.add_argument("--derive-r1-output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.derive_r1_output is not None:
        paths = write_reference_epoch_v2_derived(args.run_dir, args.derive_r1_output)
        print("\n".join(str(path) for path in paths))
        return 0
    if args.feature_ids is None:
        raise ValueError("--feature-ids is required for thermal run analysis")
    artifact = _load_json(args.feature_ids)
    feature_ids = artifact.get("feature_set", {}).get("ids") or artifact.get("ids")
    report = analyze_thermal_run(args.run_dir, feature_ids=feature_ids)
    output = args.run_dir / "analysis.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
