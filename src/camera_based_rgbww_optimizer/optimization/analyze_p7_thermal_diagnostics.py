from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
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


TD_A_COMBINED_ANALYSIS_SCHEMA_V1 = "p7_td_a_combined_analysis_v1"
TD_A_COMBINED_ANALYSIS_SCHEMA_V2 = "p7_td_a_combined_analysis_v2"
TD_A_INPUT_MANIFEST_SCHEMA_V1 = "p7_td_a_input_manifest_v1"
TD_A_INPUT_MANIFEST_SCHEMA_V2 = "p7_td_a_input_manifest_v2"
# Public aliases retain the current production v2 names.
TD_A_COMBINED_ANALYSIS_SCHEMA = TD_A_COMBINED_ANALYSIS_SCHEMA_V2
TD_A_INPUT_MANIFEST_SCHEMA = TD_A_INPUT_MANIFEST_SCHEMA_V2
TD_A_DECISION_OWNER = "Planner"
TD_A_ANALYZER_MODULE = (
    "camera_based_rgbww_optimizer.optimization.analyze_p7_thermal_diagnostics"
)
TD_A_COMMAND_CONTRACT = {
    "module_entry": f"python -m {TD_A_ANALYZER_MODULE}",
    "ray_positional_owner": "run_dir",
    "strip_paired_owner": "--paired-run",
    "feature_file_owner": "--feature-ids",
    "combined_output_owner": "--combined-output",
    "code_checkpoint_owner": "--code-checkpoint",
}
_GIT_CHECKPOINT_RE = re.compile(r"[0-9a-f]{7,64}")


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
    envelope_path = Path(plan["inputs"]["operating_envelope"]["path"])
    envelope = _load_json(envelope_path)
    envelope_mode = thermal.validate_operating_envelope(
        envelope, artifact_path=envelope_path,
        require_v2=(plan.get("experiment_id") == thermal.TD_B and envelope.get("schema") == thermal.OPERATING_ENVELOPE_V2_SCHEMA),
    )
    if plan.get("experiment_id") == thermal.TD_B and envelope_mode["mode"] == "developer_human_override":
        thermal.validate_td_b_operational_dwell_plan(plan, envelope)
    schema = plan.get("schema")
    if schema == thermal.PLAN_SCHEMA_V1:
        timing_version = 1
        expected_contract = thermal.timing_contract(1)
    elif schema == thermal.PLAN_SCHEMA_V2:
        timing_version = 2
        expected_contract = thermal.timing_contract(2)
    else:
        raise ValueError("thermal analyzer requires an explicit supported plan schema")
    if plan.get("timing_contract") != expected_contract:
        raise ValueError("thermal timing contract differs from frozen best-effort contract")
    if timing_version == 2:
        for step in plan.get("captures", []):
            if "timing_tolerance_s" in step or "actual_elapsed_s" in step:
                raise ValueError("thermal v2 plan contains legacy timing fields")
            if step.get("formal_measurement") and step.get("timing_acceptance") != "observed_elapsed_record_only":
                raise ValueError("thermal v2 plan lacks observed-elapsed acceptance semantics")
    capture_settings = _validate_capture_settings_provenance(plan, run)
    captures = _load_jsonl(root / "captures.jsonl")
    covariates = _load_jsonl(root / "thermal-covariates.jsonl")
    commands = _load_jsonl(root / "commands.jsonl")
    isolation = _load_jsonl(root / "isolation-gates.jsonl")
    if len(captures) != len(plan["captures"]) or len(covariates) != len(captures):
        raise ValueError("thermal capture/covariate count differs from frozen plan")
    if [row.get("capture_id") for row in captures] != [row.get("capture_id") for row in plan["captures"]]:
        raise ValueError("thermal capture evidence is missing, duplicated, or reordered")
    if timing_version == 1 and any(not row.get("timing_valid") for row in captures):
        raise ValueError("thermal run contains a missed-timing capture")
    if timing_version == 2 and any(
        any(key in row for key in ("actual_elapsed_s", "timing_error_s", "timing_valid"))
        for row in captures
    ):
        raise ValueError("thermal v2 capture ledger contains legacy timing fields")
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
    expected_commands = [
        group[0] for group in _formal_groups(str(plan["experiment_id"]), plan["captures"])
    ]
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
    completion_audit = _validate_completion_evidence(root, run)
    thermal.audit_chronology(covariates)
    recomputed_formal = 0
    recomputed_ambient = 0
    recomputed_physical = 0
    formal_captures = []
    ambient_captures = []
    timing_tiers: dict[str, int] = defaultdict(int)
    timing_unknown = 0
    owned_raw_paths: set[Path] = set()
    observed_by_cycle: dict[tuple[Any, ...], float] = {}
    slot_observed: dict[int, list[tuple[float, str]]] = defaultdict(list)
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
            if timing_version == 1:
                actual = float(capture["actual_elapsed_s"])
                error = float(capture["timing_error_s"])
                if abs((actual - requested) - error) > 1e-9 or abs(error) > float(step["timing_tolerance_s"]):
                    raise ValueError("thermal capture timing evidence is inconsistent")
            recomputed_formal += 1
            formal_captures.append(capture)
            expected_command = step["command"]
        else:
            legacy_present = capture.get("actual_elapsed_s") is not None or capture.get("timing_error_s") is not None
            observed_present = capture.get("best_effort_exposure_start_elapsed_s") is not None or capture.get("timing_offset_s") is not None
            if legacy_present or observed_present:
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
        raw_candidate = Path(str(raw_path)) if raw_path else None
        resolved_raw = raw_candidate.resolve() if raw_candidate is not None else None
        if (
            resolved_raw is None
            or not resolved_raw.is_relative_to(root.resolve())
            or raw_candidate is None
            or raw_candidate.is_symlink()
            or not resolved_raw.is_file()
            or resolved_raw.stat().st_size <= 0
            or resolved_raw in owned_raw_paths
        ):
            raise ValueError("thermal capture lacks retained nonempty CR3 provenance")
        owned_raw_paths.add(resolved_raw)
        timing, estimate_method = _replay_timing_evidence(capture, payload, resolved_raw, root)
        timing_tiers[str(timing["tier"])] += 1
        if timing["tier"] == "tier_c":
            timing_unknown += 1
        stored_timing = capture.get("timing_evidence")
        if not isinstance(stored_timing, Mapping) or dict(stored_timing) != timing:
            raise ValueError("thermal timing evidence differs from independent replay")
        capture_actual = timing.get("best_effort_elapsed_s")
        if step["formal_measurement"] and capture_actual is not None:
            expected_error = None if step.get("requested_elapsed_s") is None else float(capture_actual) - float(step["requested_elapsed_s"])
            if timing_version == 1:
                if capture.get("actual_elapsed_s") != capture_actual or capture.get("timing_error_s") != expected_error:
                    raise ValueError("thermal timing elapsed or error was self-reported inconsistently")
            else:
                if (
                    timing.get("tier") not in thermal.ACCEPTED_TIMING_TIERS
                    or timing.get("status") != "accepted_best_effort_anchor"
                    or capture.get("nominal_slot_s") != step.get("requested_elapsed_s")
                    or capture.get("best_effort_exposure_start_elapsed_s") != capture_actual
                    or capture.get("timing_offset_s") != expected_error
                    or capture.get("timing_evidence_status") != "accepted"
                    or capture.get("timing_estimate_method") != estimate_method
                ):
                    raise ValueError("thermal v2 observed timing was self-reported inconsistently")
                observed = float(capture_actual)
                if not np.isfinite(observed) or observed < 0:
                    raise ValueError("thermal v2 observed elapsed is invalid")
                group = thermal.timing_sequence_identity(str(plan["experiment_id"]), step)
                previous_observed = observed_by_cycle.get(group)
                if previous_observed is not None and observed <= previous_observed:
                    raise ValueError("thermal v2 observed chronology is not strictly increasing")
                observed_by_cycle[group] = observed
                slot_observed[int(step["requested_elapsed_s"])].append((observed, str(estimate_method)))
        exposure = payload.get("recorded_exposure") or payload.get("exposure_metadata") or {}
        if exposure.get("status") != "recorded":
            raise ValueError("thermal capture lacks recorded exposure provenance")
        physical_value = payload.get("physical_capture_count")
        if type(physical_value) is not int or physical_value != 1:
            raise ValueError("thermal fixed capture physical count must equal one")
        recomputed_physical += physical_value
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
        result = analyze_td_a(
            formal_captures, feature_ids=feature_ids,
            compatibility_fn=compatibility, timing_version=timing_version,
        )
    elif experiment == thermal.TD_B:
        result = analyze_td_b(
            formal_captures, feature_ids=feature_ids, compatibility_fn=compatibility_fn,
            operational_override=(envelope_mode["mode"] == "developer_human_override"),
            operational_dwell_s=(
                thermal.DEVELOPER_OPERATIONAL_DWELL_S
                if envelope_mode["mode"] == "developer_human_override" else None
            ),
        )
    else:
        result = analyze_td_c(
            formal_captures, ambients=ambient_captures, feature_ids=feature_ids,
            p6_compare_fn=lambda rows: compare_current_ray_center_to_p6(rows, feature_ids),
        )
    timing_slot_summary = {
        str(slot): {
            "sample_count": len(values),
            "observed_elapsed_s": [value for value, _method in values],
            "offset_s": [value - float(slot) for value, _method in values],
            "estimate_method": [method for _value, method in values],
            "method_distribution": dict(Counter(
                method for _value, method in values
            )),
            "min_observed_elapsed_s": min(value for value, _method in values),
            "median_observed_elapsed_s": float(np.median([value for value, _method in values])),
            "max_observed_elapsed_s": max(value for value, _method in values),
        }
        for slot, values in sorted(slot_observed.items())
    }
    report = {
        "schema": thermal.ANALYSIS_SCHEMA_V2 if timing_version == 2 else "p7_thermal_diagnostic_analysis_v1",
        "experiment_id": experiment,
        "source_id": str(plan.get("source")),
        "capture_contract": "pass", "timing_contract": "pass",
        "covariate_contract": "pass", "source_isolation_contract": "pass",
        "cleanup_contract": completion_audit["cleanup_contract"],
        "wrapper_contract": completion_audit["wrapper_contract"],
        "formal_capture_count": recomputed_formal, "ambient_capture_count": recomputed_ambient,
        "physical_cr3_count": recomputed_physical, "retained_npy_count": 0,
        "timing_absolute_truth": False,
        "timing_source": "best_effort_gphoto2_observed_elapsed" if timing_version == 2 else "best_effort_gphoto2",
        "timing_contract_evidence": dict(expected_contract),
        "tier_distribution": dict(timing_tiers),
        "unknown_uncertainty_count": timing_unknown,
    }
    if timing_version == 2:
        report["timing_slot_summary"] = timing_slot_summary
    report.update(result)
    return report


def _validate_completion_evidence(root: Path, run: Mapping[str, Any]) -> dict[str, str]:
    if run.get("cleanup") != "pass":
        raise ValueError("thermal run.json cleanup did not pass")

    python_cleanup = _load_json(root / "all-off-python.json")
    if set(python_cleanup) != {"status", "steps"} or python_cleanup.get("status") != "pass":
        raise ValueError("thermal Python cleanup artifact has an unsupported or failed schema")
    _validate_shutdown_steps(python_cleanup.get("steps"), artifact="Python")

    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    _validate_shutdown_steps(shell_cleanup, artifact="shell")

    wrapper = _load_json(root / "wrapper-result.json")
    expected_wrapper_keys = {
        "schema_version", "experiment", "status", "run_dir", "wrapper_pid", "child_pid",
        "child_exit_code", "shell_cleanup_exit_code", "wrapper_exit_code", "signal", "started_at",
    }
    if set(wrapper) != expected_wrapper_keys:
        raise ValueError("thermal wrapper result schema drift")
    if (
        wrapper.get("schema_version") != 1
        or wrapper.get("experiment") != "p7_thermal_diagnostics_v1"
        or wrapper.get("status") != "complete"
        or Path(str(wrapper.get("run_dir"))).resolve() != root.resolve()
        or type(wrapper.get("wrapper_pid")) is not int
        or int(wrapper["wrapper_pid"]) <= 0
        or type(wrapper.get("child_pid")) is not int
        or int(wrapper["child_pid"]) <= 0
        or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None
        or not isinstance(wrapper.get("started_at"), str)
        or not str(wrapper["started_at"]).strip()
    ):
        raise ValueError("thermal wrapper did not complete cleanly")
    _validate_zero_exit_file(root / "child-exit-status.txt", artifact="child")
    _validate_zero_exit_file(root / "all-off-shell.exit-status.txt", artifact="shell cleanup")
    return {"cleanup_contract": "pass", "wrapper_contract": "pass"}


def _validate_shutdown_steps(value: Any, *, artifact: str) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"thermal {artifact} cleanup must contain exactly two shutdown steps")
    for expected_name, item in zip(("esphome", "ray120c"), value, strict=True):
        if not isinstance(item, Mapping) or set(item) != {"name", "ok", "detail", "error"}:
            raise ValueError(f"thermal {artifact} cleanup step schema drift")
        if (
            item.get("name") != expected_name
            or item.get("ok") is not True
            or item.get("error") is not None
            or not isinstance(item.get("detail"), Mapping)
        ):
            raise ValueError(f"thermal {artifact} cleanup did not prove both lights off")


def _validate_zero_exit_file(path: Path, *, artifact: str) -> None:
    try:
        value = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"thermal {artifact} exit artifact is missing or unreadable") from exc
    if value.strip() != "0":
        raise ValueError(f"thermal {artifact} exit status is not zero")


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
) -> tuple[dict[str, Any], str | None]:
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
    estimate = remote_metadata.get("exposure_start_estimate")
    method = estimate.get("method") if isinstance(estimate, Mapping) else None
    if replayed.get("tier") in thermal.ACCEPTED_TIMING_TIERS and method not in {
        "gphoto_event_minus_recorded_exposure",
        "gphoto_capture_return_minus_recorded_exposure",
    }:
        raise ValueError("thermal available timing estimate lacks a recognized method")
    return replayed, method


def analyze_td_a(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    timing_version: int = 2,
) -> dict[str, Any]:
    cycles: dict[str, dict[int, list[Mapping[str, float]]]] = defaultdict(lambda: defaultdict(list))
    for row in captures:
        step = row["plan_step"]
        features = _features(row, feature_ids)
        cycles[str(step["cycle_index"])][int(step["requested_elapsed_s"])].append(features)
    settling = thermal.settle_from_cycles(cycles, feature_ids, compatibility_fn=compatibility_fn)
    observed_by_slot: dict[int, list[float]] = defaultdict(list)
    for row in captures:
        observed = row.get("best_effort_exposure_start_elapsed_s")
        if observed is not None:
            observed_by_slot[int(row["plan_step"]["requested_elapsed_s"])].append(float(observed))
    groups = {
        f"cycle-{cycle}": [features for point in sorted(points) for features in points[point]]
        for cycle, points in cycles.items()
    }
    audit = thermal.summarize_group_audit(groups, feature_ids)
    if audit["trend_failed"] or audit["dominance_failed"]:
        settling = {"status": "settling_not_demonstrated_by_600", "t_settle_s": None, "six_hundred_is_validation_only": True}
    result = {
        "status": "td_a_pass" if settling["t_settle_s"] is not None else settling["status"],
        "within_cycle_settling": settling,
        "between_cycle_repeatability": audit,
        "state_specific_settle_time": {"A": settling["t_settle_s"]},
        "source_specific_settle_time": settling["t_settle_s"],
        "temperature_not_sufficient_proxy": False,
    }
    if timing_version == 1:
        return result
    if timing_version != 2:
        raise ValueError("unsupported TD-A timing analysis version")
    selected = settling["t_settle_s"]
    if selected is not None and not observed_by_slot.get(int(selected)):
        raise ValueError("TD-A v2 settled result lacks observed timing evidence")
    result.update({
        "source_specific_settle_observed_max_s": (
            None if selected is None else max(observed_by_slot[int(selected)])
        ),
    })
    return result


def analyze_td_b(
    captures: Sequence[Mapping[str, Any]], *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    operational_override: bool = False,
    operational_dwell_s: int | None = None,
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
    history_pass = len(anchors) == 4 and thermal._all_pairs(anchors, anchor_compatibility)
    state_results = {
        state: thermal.settle_from_cycles(
            {"switch": points}, feature_ids,
            compatibility_fn=(compatibility_fn or frozen_same_state_compatibility(
                source=source, state=state, feature_ids=feature_ids,
            )),
        )
        for state, points in state_points.items()
    }
    if operational_override:
        if operational_dwell_s != thermal.DEVELOPER_OPERATIONAL_DWELL_S:
            raise ValueError("TD-B operational override requires the frozen 600 second dwell")
        nonstationary_states = sorted(
            state for state, result in state_results.items() if result.get("t_settle_s") is None
        )
        return {
            "status": (
                "td_b_operational_600_complete_waiting_for_planner"
                if history_pass else "history_dependent_at_operational_dwell_600"
            ),
            "return_anchor_history_effect": "pass" if history_pass else "fail",
            "operational_dwell_s": operational_dwell_s,
            "dwell_source": "developer_human_override",
            "dwell_is_scientifically_settled": False,
            "operational_nonstationarity_observed": bool(nonstationary_states),
            "nonstationary_states": nonstationary_states,
            "state_specific_settle_time": {
                state: result["t_settle_s"] for state, result in state_results.items()
            },
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


def analyze_td_a_pair(
    ray_run: str | Path,
    strip_run: str | Path,
    output_dir: str | Path,
    *,
    feature_ids: Sequence[str],
    feature_ids_path: str | Path,
    code_checkpoint: str,
) -> dict[str, Any]:
    checkpoint = _validate_code_checkpoint(code_checkpoint)
    ray_root = Path(ray_run).resolve()
    strip_root = Path(strip_run).resolve()
    feature_path = Path(feature_ids_path).resolve()
    if ray_root == strip_root:
        raise ValueError("TD-A paired finalizer requires distinct Ray and strip runs")
    if _feature_ids_from_artifact(feature_path) != list(feature_ids):
        raise ValueError("TD-A paired finalizer feature IDs differ from the retained feature file")
    ray_plan = _load_json(ray_root / "plan.json")
    strip_plan = _load_json(strip_root / "plan.json")
    plan_schemas = {ray_plan.get("schema"), strip_plan.get("schema")}
    if len(plan_schemas) != 1 or next(iter(plan_schemas)) not in {
        thermal.PLAN_SCHEMA_V1, thermal.PLAN_SCHEMA_V2,
    }:
        raise ValueError("TD-A paired finalizer rejects mixed timing plan versions")
    timing_version = 1 if ray_plan.get("schema") == thermal.PLAN_SCHEMA_V1 else 2
    combined_schema = (
        TD_A_COMBINED_ANALYSIS_SCHEMA_V1 if timing_version == 1
        else TD_A_COMBINED_ANALYSIS_SCHEMA_V2
    )
    manifest_schema = (
        TD_A_INPUT_MANIFEST_SCHEMA_V1 if timing_version == 1
        else TD_A_INPUT_MANIFEST_SCHEMA_V2
    )
    ray_report = analyze_thermal_run(ray_root, feature_ids=feature_ids)
    strip_report = analyze_thermal_run(strip_root, feature_ids=feature_ids)

    if ray_plan.get("experiment_id") != thermal.TD_A or strip_plan.get("experiment_id") != thermal.TD_A:
        raise ValueError("TD-A paired finalizer requires two exact TD-A runs")
    if ray_plan.get("source") != "ray" or strip_plan.get("source") != "strip":
        raise ValueError("TD-A paired finalizer requires Ray first and strip second")
    if ray_report.get("source_id") != "ray" or strip_report.get("source_id") != "strip":
        raise ValueError("TD-A paired finalizer source owner mismatch")
    if ray_plan.get("inputs") != strip_plan.get("inputs"):
        raise ValueError("TD-A paired finalizer frozen input path/hash mismatch")
    if ray_plan.get("timing_contract") != strip_plan.get("timing_contract"):
        raise ValueError("TD-A paired finalizer timing contract mismatch")
    policy_reference = ray_plan.get("inputs", {}).get("policy")
    if (
        not isinstance(policy_reference, Mapping)
        or Path(str(policy_reference.get("path"))).resolve() != feature_path
        or policy_reference.get("sha256") != _sha256_file(feature_path)
    ):
        raise ValueError("TD-A paired finalizer feature file differs from frozen policy input")

    reports = (ray_report, strip_report)
    for source, report in zip(("ray", "strip"), reports, strict=True):
        if (
            report.get("experiment_id") != thermal.TD_A
            or report.get("source_id") != source
            or report.get("capture_contract") != "pass"
            or report.get("timing_contract") != "pass"
            or report.get("covariate_contract") != "pass"
            or report.get("source_isolation_contract") != "pass"
            or report.get("cleanup_contract") != "pass"
            or report.get("wrapper_contract") != "pass"
            or report.get("formal_capture_count") != 12
            or report.get("ambient_capture_count") != 3
            or not isinstance(report.get("physical_cr3_count"), int)
            or int(report["physical_cr3_count"]) > 22
            or report.get("retained_npy_count") != 0
            or report.get("unknown_uncertainty_count") != 0
        ):
            raise ValueError(f"TD-A paired finalizer {source} contract did not pass")
        tiers = report.get("tier_distribution")
        if (
            not isinstance(tiers, Mapping)
            or set(tiers) - {"tier_a", "tier_b"}
            or sum(int(count) for count in tiers.values()) != int(report["physical_cr3_count"])
        ):
            raise ValueError(f"TD-A paired finalizer {source} timing tier ledger is invalid")

    formal_total = sum(int(report["formal_capture_count"]) for report in reports)
    ambient_total = sum(int(report["ambient_capture_count"]) for report in reports)
    physical_total = sum(int(report["physical_cr3_count"]) for report in reports)
    if formal_total != 24 or ambient_total != 6 or physical_total > 44:
        raise ValueError("TD-A paired finalizer combined capture budget mismatch")

    ray_settle = _validated_td_a_settle(ray_report, source="ray")
    strip_settle = _validated_td_a_settle(strip_report, source="strip")
    both_settled = ray_settle is not None and strip_settle is not None
    provisional = max(ray_settle, strip_settle) if both_settled else None
    status = "td_a_pass" if both_settled else "settling_not_demonstrated_by_600"
    combined = {
        "schema": combined_schema,
        "experiment_id": thermal.TD_A,
        "status": status,
        "ray_run": str(ray_root.resolve()),
        "strip_run": str(strip_root.resolve()),
        "input_contract": "pass",
        "timing_contract": "pass",
        "capture_contract": "pass",
        "cleanup_contract": "pass",
        "wrapper_contract": "pass",
        "formal_capture_count": formal_total,
        "ambient_capture_count": ambient_total,
        "physical_cr3_count": physical_total,
        "physical_cr3_cap": 44,
        "t_settle_ray_s": ray_settle,
        "t_settle_strip_s": strip_settle,
        "t_formal_provisional_s": provisional,
        "t_formal_s": None,
        "six_hundred_is_validation_only": True,
        "default_operating_envelope_modified": False,
        "source_results": {"ray": ray_report, "strip": strip_report},
    }
    if timing_version == 2:
        ray_observed = ray_report.get("source_specific_settle_observed_max_s") if both_settled else None
        strip_observed = strip_report.get("source_specific_settle_observed_max_s") if both_settled else None
        observed_provisional = (
            max(ray_observed, strip_observed)
            if ray_observed is not None and strip_observed is not None else None
        )
        combined.update({
            "t_settle_ray_observed_max_s": ray_observed,
            "t_settle_strip_observed_max_s": strip_observed,
            "t_formal_provisional_observed_max_s": observed_provisional,
            "source_observed_timing_summary": {
                "ray": ray_report.get("timing_slot_summary", {}),
                "strip": strip_report.get("timing_slot_summary", {}),
            },
        })

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=False)
    analysis_path = output / "td-a-combined-analysis.json"
    summary_path = output / "EXPERIMENT_SUMMARY.md"
    manifest_path = output / "input-manifest.json"
    try:
        _write_text_atomic(
            analysis_path,
            json.dumps(combined, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        )
        _write_text_atomic(summary_path, _render_td_a_summary(combined))
        manifest = _build_td_a_input_manifest(
            ray_root=ray_root,
            strip_root=strip_root,
            feature_path=feature_path,
            analysis_path=analysis_path,
            summary_path=summary_path,
            frozen_inputs=ray_plan["inputs"],
            timing_contract=ray_plan["timing_contract"],
            code_checkpoint=checkpoint,
            manifest_schema=manifest_schema,
            analysis_schema=combined_schema,
        )
        _write_text_atomic(
            manifest_path,
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        )
        validate_td_a_input_manifest(manifest_path)
    except BaseException:
        for path in (manifest_path, summary_path, analysis_path):
            path.unlink(missing_ok=True)
        try:
            output.rmdir()
        except OSError:
            pass
        raise
    return combined


def _build_td_a_input_manifest(
    *,
    ray_root: Path,
    strip_root: Path,
    feature_path: Path,
    analysis_path: Path,
    summary_path: Path,
    frozen_inputs: Mapping[str, Any],
    timing_contract: Mapping[str, Any],
    code_checkpoint: str,
    manifest_schema: str,
    analysis_schema: str,
) -> dict[str, Any]:
    def source_entry(root: Path) -> dict[str, str]:
        plan_path = (root / "plan.json").resolve()
        run_path = (root / "run.json").resolve()
        return {
            "run_dir": str(root.resolve()),
            "plan_path": str(plan_path),
            "plan_sha256": _sha256_file(plan_path),
            "run_path": str(run_path),
            "run_sha256": _sha256_file(run_path),
        }

    return {
        "schema": manifest_schema,
        "experiment_id": thermal.TD_A,
        "decision_owner": TD_A_DECISION_OWNER,
        "generated_by": {
            "module": TD_A_ANALYZER_MODULE,
            "analysis_schema": analysis_schema,
            "code_checkpoint": code_checkpoint,
            "command_contract": dict(TD_A_COMMAND_CONTRACT),
        },
        "sources": {
            "ray": source_entry(ray_root),
            "strip": source_entry(strip_root),
        },
        "feature_ids": {
            "path": str(feature_path.resolve()),
            "sha256": _sha256_file(feature_path),
        },
        "frozen_inputs": dict(frozen_inputs),
        "timing_contract": dict(timing_contract),
        "outputs": {
            analysis_path.name: {
                "path": str(analysis_path.resolve()),
                "sha256": _sha256_file(analysis_path),
            },
            summary_path.name: {
                "path": str(summary_path.resolve()),
                "sha256": _sha256_file(summary_path),
            },
        },
    }


def validate_td_a_input_manifest(manifest_path: str | Path) -> dict[str, Any]:
    path = Path(manifest_path).resolve()
    manifest = _load_json(path)
    if set(manifest) != {
        "schema", "experiment_id", "decision_owner", "generated_by", "sources",
        "feature_ids", "frozen_inputs", "timing_contract", "outputs",
    }:
        raise ValueError("TD-A input manifest top-level schema drift")
    manifest_schema = manifest.get("schema")
    if manifest_schema == TD_A_INPUT_MANIFEST_SCHEMA_V1:
        expected_plan_schema = thermal.PLAN_SCHEMA_V1
        expected_analysis_schema = TD_A_COMBINED_ANALYSIS_SCHEMA_V1
    elif manifest_schema == TD_A_INPUT_MANIFEST_SCHEMA_V2:
        expected_plan_schema = thermal.PLAN_SCHEMA_V2
        expected_analysis_schema = TD_A_COMBINED_ANALYSIS_SCHEMA_V2
    else:
        raise ValueError("TD-A input manifest owner or schema mismatch")
    if (
        manifest.get("experiment_id") != thermal.TD_A
        or manifest.get("decision_owner") != TD_A_DECISION_OWNER
    ):
        raise ValueError("TD-A input manifest owner or schema mismatch")

    generated = manifest.get("generated_by")
    if not isinstance(generated, Mapping) or set(generated) != {
        "module", "analysis_schema", "code_checkpoint", "command_contract",
    }:
        raise ValueError("TD-A input manifest generated_by schema drift")
    if (
        generated.get("module") != TD_A_ANALYZER_MODULE
        or generated.get("analysis_schema") != expected_analysis_schema
        or generated.get("command_contract") != TD_A_COMMAND_CONTRACT
    ):
        raise ValueError("TD-A input manifest generator contract mismatch")
    _validate_code_checkpoint(generated.get("code_checkpoint"))

    sources = manifest.get("sources")
    if not isinstance(sources, Mapping) or set(sources) != {"ray", "strip"}:
        raise ValueError("TD-A input manifest source schema drift")
    source_plans: dict[str, dict[str, Any]] = {}
    source_roots: dict[str, Path] = {}
    for source in ("ray", "strip"):
        entry = sources.get(source)
        if not isinstance(entry, Mapping) or set(entry) != {
            "run_dir", "plan_path", "plan_sha256", "run_path", "run_sha256",
        }:
            raise ValueError(f"TD-A input manifest {source} source schema drift")
        root = _absolute_path(entry.get("run_dir"), label=f"{source} run_dir")
        plan_path = _absolute_path(entry.get("plan_path"), label=f"{source} plan_path")
        run_path = _absolute_path(entry.get("run_path"), label=f"{source} run_path")
        if plan_path != root / "plan.json" or run_path != root / "run.json":
            raise ValueError(f"TD-A input manifest {source} retained path owner mismatch")
        if _sha256_file(plan_path) != entry.get("plan_sha256"):
            raise ValueError(f"TD-A input manifest {source} plan hash mismatch")
        if _sha256_file(run_path) != entry.get("run_sha256"):
            raise ValueError(f"TD-A input manifest {source} run hash mismatch")
        plan = _load_json(plan_path)
        run = _load_json(run_path)
        if (
            plan.get("experiment_id") != thermal.TD_A
            or plan.get("schema") != expected_plan_schema
            or plan.get("source") != source
            or run.get("experiment_id") != thermal.TD_A
            or run.get("status") != "complete"
        ):
            raise ValueError(f"TD-A input manifest {source} plan/run owner mismatch")
        _verify_frozen_inputs(plan.get("inputs", {}))
        source_plans[source] = plan
        source_roots[source] = root
    if source_roots["ray"] == source_roots["strip"]:
        raise ValueError("TD-A input manifest Ray and strip run paths must differ")

    feature = manifest.get("feature_ids")
    if not isinstance(feature, Mapping) or set(feature) != {"path", "sha256"}:
        raise ValueError("TD-A input manifest feature file schema drift")
    feature_path = _absolute_path(feature.get("path"), label="feature_ids path")
    if _sha256_file(feature_path) != feature.get("sha256"):
        raise ValueError("TD-A input manifest feature file hash mismatch")
    _feature_ids_from_artifact(feature_path)

    frozen_inputs = manifest.get("frozen_inputs")
    timing_contract = manifest.get("timing_contract")
    if not isinstance(frozen_inputs, Mapping) or not isinstance(timing_contract, Mapping):
        raise ValueError("TD-A input manifest frozen input or timing schema drift")
    policy_reference = frozen_inputs.get("policy")
    if (
        not isinstance(policy_reference, Mapping)
        or Path(str(policy_reference.get("path"))).resolve() != feature_path
        or policy_reference.get("sha256") != feature.get("sha256")
    ):
        raise ValueError("TD-A input manifest feature file is not the frozen policy input")

    if (
        source_plans["ray"].get("inputs") != source_plans["strip"].get("inputs")
        or frozen_inputs != source_plans["ray"].get("inputs")
    ):
        raise ValueError("TD-A input manifest frozen input replay mismatch")
    if (
        source_plans["ray"].get("timing_contract")
        != source_plans["strip"].get("timing_contract")
        or timing_contract != source_plans["ray"].get("timing_contract")
        or timing_contract != thermal.timing_contract(
            1 if expected_plan_schema == thermal.PLAN_SCHEMA_V1 else 2
        )
    ):
        raise ValueError("TD-A input manifest timing contract replay mismatch")

    outputs = manifest.get("outputs")
    expected_output_names = {"td-a-combined-analysis.json", "EXPERIMENT_SUMMARY.md"}
    if not isinstance(outputs, Mapping) or set(outputs) != expected_output_names:
        raise ValueError("TD-A input manifest output schema drift")
    output_paths: dict[str, Path] = {}
    for name in expected_output_names:
        entry = outputs.get(name)
        if not isinstance(entry, Mapping) or set(entry) != {"path", "sha256"}:
            raise ValueError(f"TD-A input manifest output schema drift: {name}")
        output_path = _absolute_path(entry.get("path"), label=f"output {name}")
        if output_path != path.parent / name:
            raise ValueError(f"TD-A input manifest output path owner mismatch: {name}")
        if _sha256_file(output_path) != entry.get("sha256"):
            raise ValueError(f"TD-A input manifest output hash mismatch: {name}")
        output_paths[name] = output_path
    analysis = _load_json(output_paths["td-a-combined-analysis.json"])
    if (
        analysis.get("schema") != expected_analysis_schema
        or analysis.get("experiment_id") != thermal.TD_A
        or Path(str(analysis.get("ray_run"))).resolve() != Path(sources["ray"]["run_dir"])
        or Path(str(analysis.get("strip_run"))).resolve() != Path(sources["strip"]["run_dir"])
    ):
        raise ValueError("TD-A input manifest combined analysis owner mismatch")
    return manifest


def _validate_code_checkpoint(value: Any) -> str:
    if not isinstance(value, str) or _GIT_CHECKPOINT_RE.fullmatch(value.strip()) is None:
        raise ValueError("TD-A paired finalizer requires an auditable Git code checkpoint")
    return value.strip()


def _absolute_path(value: Any, *, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"TD-A input manifest {label} is missing")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"TD-A input manifest {label} must be absolute")
    return path.resolve()


def _sha256_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise ValueError(f"missing or unreadable retained artifact: {path}") from exc


def _feature_ids_from_artifact(path: Path) -> list[str]:
    artifact = _load_json(path)
    ids = artifact.get("feature_set", {}).get("ids") or artifact.get("ids")
    if not isinstance(ids, list) or not ids or any(not isinstance(item, str) or not item for item in ids):
        raise ValueError("thermal feature file lacks a non-empty string ID list")
    return ids


def _validated_td_a_settle(report: Mapping[str, Any], *, source: str) -> int | None:
    value = report.get("source_specific_settle_time")
    if value is None:
        if report.get("status") != "settling_not_demonstrated_by_600":
            raise ValueError(f"TD-A paired finalizer {source} has an invalid non-settle status")
        return None
    if type(value) is not int or value not in thermal.TIMED_POINTS[:-1]:
        raise ValueError(f"TD-A paired finalizer {source} has an invalid settle time")
    if report.get("status") != "td_a_pass":
        raise ValueError(f"TD-A paired finalizer {source} settle/status mismatch")
    return value


def _render_td_a_summary(combined: Mapping[str, Any]) -> str:
    lines = (
        "# P7 TD-A Combined Analysis\n\n"
        f"- status: `{combined['status']}`\n"
        f"- Ray settle: `{combined['t_settle_ray_s']}` s\n"
        f"- strip settle: `{combined['t_settle_strip_s']}` s\n"
        f"- provisional formal settle: `{combined['t_formal_provisional_s']}` s\n"
    )
    if combined.get("schema") == TD_A_COMBINED_ANALYSIS_SCHEMA_V2:
        lines += (
            f"- Ray observed settle max: `{combined.get('t_settle_ray_observed_max_s')}` s\n"
            f"- strip observed settle max: `{combined.get('t_settle_strip_observed_max_s')}` s\n"
            f"- provisional observed settle max: `{combined.get('t_formal_provisional_observed_max_s')}` s\n"
        )
    return lines + (
        f"- captures: `{combined['formal_capture_count']}` formal + "
        f"`{combined['ambient_capture_count']}` ambient / `{combined['physical_cr3_count']}` physical CR3\n"
        "- default operating envelope modified: `false`\n"
    )


def _write_text_atomic(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(value, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_json_value(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"missing or unreadable JSON artifact: {path}") from exc
    if not text.strip():
        raise ValueError(f"empty JSON artifact: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON artifact: {path}") from exc


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _formal_groups(
    experiment_id: str, captures: Sequence[Mapping[str, Any]],
) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if not step.get("formal_measurement"):
            continue
        key = thermal.timing_sequence_identity(experiment_id, step)
        if groups:
            previous = groups[-1][0]
            previous_key = thermal.timing_sequence_identity(experiment_id, previous)
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
    parser.add_argument("--paired-run", type=Path, help="Strip TD-A run paired with positional Ray TD-A run.")
    parser.add_argument("--combined-output", type=Path, help="New output directory for paired TD-A finalization.")
    parser.add_argument("--code-checkpoint", help="Explicit Git checkpoint owning paired TD-A finalization.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.derive_r1_output is not None and (
        args.paired_run is not None or args.combined_output is not None or args.code_checkpoint is not None
    ):
        raise ValueError("R1 derivation cannot be combined with TD-A paired finalization")
    if args.derive_r1_output is not None:
        paths = write_reference_epoch_v2_derived(args.run_dir, args.derive_r1_output)
        print("\n".join(str(path) for path in paths))
        return 0
    if args.feature_ids is None:
        raise ValueError("--feature-ids is required for thermal run analysis")
    feature_ids = _feature_ids_from_artifact(args.feature_ids)
    if args.paired_run is not None:
        if args.combined_output is None:
            raise ValueError("--combined-output is required with --paired-run")
        if args.code_checkpoint is None:
            raise ValueError("--code-checkpoint is required with --paired-run")
        analyze_td_a_pair(
            args.run_dir, args.paired_run, args.combined_output,
            feature_ids=feature_ids, feature_ids_path=args.feature_ids,
            code_checkpoint=args.code_checkpoint,
        )
        print(args.combined_output / "td-a-combined-analysis.json")
        print(args.combined_output / "EXPERIMENT_SUMMARY.md")
        print(args.combined_output / "input-manifest.json")
        return 0
    if args.combined_output is not None or args.code_checkpoint is not None:
        raise ValueError("--combined-output/--code-checkpoint require --paired-run")
    report = analyze_thermal_run(args.run_dir, feature_ids=feature_ids)
    output = args.run_dir / "analysis.json"
    _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
