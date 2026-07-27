from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from copy import deepcopy
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
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.optimization.analyze_hsi_reference_repeatability import (
    write_reference_epoch_v2_derived,
)
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    TD_B_FORMAL_FEATURE_STATISTIC,
    required_hsi_features_from_report,
)


TD_A_COMBINED_ANALYSIS_SCHEMA_V1 = "p7_td_a_combined_analysis_v1"
TD_A_COMBINED_ANALYSIS_SCHEMA_V2 = "p7_td_a_combined_analysis_v2"
TD_A_INPUT_MANIFEST_SCHEMA_V1 = "p7_td_a_input_manifest_v1"
TD_A_INPUT_MANIFEST_SCHEMA_V2 = "p7_td_a_input_manifest_v2"
TD_B_COMBINED_ANALYSIS_SCHEMA = "p7_td_b_combined_analysis_v1"
TD_B_INPUT_MANIFEST_SCHEMA = "p7_td_b_input_manifest_v1"
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
TD_B_RETAINED_FAILED_RAY_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/"
    "p7-td-b-canon-r2-ray-20260723-045514"
)
TD_B_RETAINED_FIRST_CAPTURE_PATH = (
    TD_B_RETAINED_FAILED_RAY_RUN
    / "camera"
    / (
        "000-ray-a-t600-source-ray-purpose-p7_thermal_td-b_ray_A-repeat-0-"
        "exposure-auto-attempt-0.cr3"
    )
)
TD_B_RETAINED_FIRST_SIDECAR_PATH = TD_B_RETAINED_FIRST_CAPTURE_PATH.with_suffix(
    TD_B_RETAINED_FIRST_CAPTURE_PATH.suffix + ".metadata.json"
)
TD_B_RETAINED_FIRST_CAPTURE_SHA256 = (
    "2cf5d680d694eb9c0d2e36bf8144dcf2f1fe02cd902bc4c202cf92ce1a699608"
)
TD_B_RETAINED_FIRST_SIDECAR_SHA256 = (
    "9952bf79094d7d93b21a9864e841359d0195c423c3dc8464e0250231bc1721ee"
)
TD_B_RETAINED_FIRST_CAPTURE_ID = "bfc876fa-9a69-445d-bfc2-298f42baf3af"
TD_B_RETAINED_FIRST_REQUEST_ID = "36d2a813-8d35-4f9a-b860-c58cc1ba12e9"
TD_B_R5_FORMAL_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/"
    "formal-r5-1e3b107-20260726T220000Z"
)
TD_B_R5_ARTIFACT_HASHES = {
    "ray-formal/plan.json": "94da09f240e2d0ca84ce545c52748522dfbaa9a674bf96ffcef5c8e74473ba9f",
    "ray-formal/failure.json": "2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65",
    "ray-formal/measurements/011-ray-c-t60.patch-statistics.json":
        "98b792f0ef2d89718102c054fa4c4ad43206cf3cce82855d9c67900b6223a8be",
    "ray-formal/run.json": "dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079",
    "ray-formal/physical-returns.jsonl":
        "d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02",
    "terminal-audit.json": "4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79",
    "returned-summary.json": "5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955",
    "ray-formal/all-off-python.json":
        "982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc",
    "ray-formal/all-off-shell.json":
        "3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381",
}


def td_b_feature_map_from_report(
    report: Mapping[str, Any], feature_ids: Sequence[str],
) -> dict[str, float]:
    context = report.get("analysis_context")
    if (
        not isinstance(context, Mapping)
        or context.get("native_raw_ambient_policy")
        != raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        or context.get("ambient_subtraction_applied") is not False
        or context.get("phase") != "TD-B"
        or context.get("formal_measurement") is not True
    ):
        raise ValueError("retained TD-B report lacks the frozen no-ambient owner")
    return required_hsi_features_from_report(
        report,
        feature_ids,
        statistic=TD_B_FORMAL_FEATURE_STATISTIC,
    )


def r5_formal_tree_manifest(root: str | Path = TD_B_R5_FORMAL_ROOT) -> list[dict[str, Any]]:
    """Return a deterministic, no-follow manifest for immutable R5 evidence."""
    target = Path(root)
    if target.resolve(strict=True) != TD_B_R5_FORMAL_ROOT.resolve(strict=True):
        raise ValueError("R5 diagnostic requires the exact retained formal root")
    rows: list[dict[str, Any]] = []
    for path in sorted(target.rglob("*")):
        relative = path.relative_to(target).as_posix()
        if path.is_symlink():
            rows.append({"path": relative, "type": "symlink"})
        elif path.is_file():
            rows.append({
                "path": relative,
                "type": "file",
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        elif path.is_dir():
            rows.append({"path": relative, "type": "directory"})
        else:
            rows.append({"path": relative, "type": "other"})
    return rows


def build_r5_partial_diagnostic(
    root: str | Path = TD_B_R5_FORMAL_ROOT,
) -> dict[str, Any]:
    """Describe the retained R5 prefix without running formal inference."""
    target = Path(root)
    if target.resolve(strict=True) != TD_B_R5_FORMAL_ROOT.resolve(strict=True):
        raise ValueError("R5 diagnostic requires the exact retained formal root")
    for relative, expected in TD_B_R5_ARTIFACT_HASHES.items():
        artifact = target / relative
        if artifact.is_symlink() or not artifact.is_file():
            raise ValueError(f"R5 retained artifact is missing or unsafe: {relative}")
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
            raise ValueError(f"R5 retained artifact hash drifted: {relative}")
    run = _load_json(target / "ray-formal/run.json")
    failure = _load_json(target / "ray-formal/failure.json")
    if run.get("formal_pass") is True:
        raise ValueError("R5 retained run cannot authorize formal pass")
    return {
        "schema": "r5_partial_diagnostic_analysis_v1",
        "formal_authorizing": False,
        "incomplete_sequence": True,
        "missing_slots": ["011", "012", "013", "014", "015"],
        "formal_pass": False,
        "r5_capture_011_quality": "invalid",
        "r5_run": "retained_accepted_hard_failed_formal_attempt",
        "retained_11_use": "diagnostic_only",
        "retained_11_formal_inference": "prohibited",
        "old_new_pooling_allowed": False,
        "failure_class": thermal.TD_B_R5_FAILURE_CLASS,
        "retained_root": str(target),
        "retained_artifact_hashes": dict(TD_B_R5_ARTIFACT_HASHES),
        "formal_analysis_fields": {
            "feature_vector": "not_evaluated",
            "inverse": "not_evaluated",
            "center": "not_evaluated",
            "covariance": "not_evaluated",
            "history": "not_evaluated",
            "reference": "not_evaluated",
        },
        "source_status": {
            "run_status": run.get("status"),
            "failure_classification": failure.get("classification"),
        },
    }


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
    if (
        plan.get("experiment_id") == thermal.TD_B
        and plan.get("source") == "ray"
        and int(plan.get("setup_physical_cr3_count", 0)) > 0
        and plan.get("setup_lineage_release_required") is True
    ):
        lineage_reference = plan.get("setup_lineage_release")
        if (
            not isinstance(lineage_reference, Mapping)
            or set(lineage_reference) != {"path", "sha256"}
        ):
            raise ValueError("Ray TD-B analysis lacks lineage release provenance")
        lineage_path = Path(str(lineage_reference.get("path"))).resolve()
        if (
            not lineage_path.is_file()
            or lineage_path.is_symlink()
            or hashlib.sha256(lineage_path.read_bytes()).hexdigest()
            != lineage_reference.get("sha256")
        ):
            raise ValueError("Ray TD-B lineage release owner or hash differs")
        lineage = _load_json(lineage_path)
        validated_lineage = thermal.validate_td_b_setup_lineage_release(
            lineage,
            release_path=lineage_path,
        )
        expected_plan = deepcopy(dict(validated_lineage["resolved_plan"]))
        observed_plan = deepcopy(dict(plan))
        observed_plan.pop("setup_lineage_release", None)
        expected_plan.pop("created_at", None)
        observed_plan.pop("created_at", None)
        expected_camera = deepcopy(dict(expected_plan.get("camera", {})))
        observed_camera = deepcopy(dict(observed_plan.get("camera", {})))
        observed_camera.pop("resolved_capture_settings", None)
        expected_plan["camera"] = expected_camera
        observed_plan["camera"] = observed_camera
        if observed_plan != expected_plan:
            raise ValueError("Ray TD-B run plan differs from lineage-qualified release")
    _verify_frozen_inputs(plan["inputs"])
    envelope_resolution = thermal.validate_trusted_operating_envelope_reference(
        plan["inputs"]["operating_envelope"],
    )
    envelope = envelope_resolution["envelope"]
    envelope_mode = envelope_resolution["mode"]
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
    expected_ambient_policy = thermal.expected_native_raw_ambient_policy(
        str(plan.get("experiment_id")),
        plan_schema=str(plan.get("schema")),
    )
    stored_ambient_policy = plan.get(
        "native_raw_ambient_policy",
        raw_validation.AMBIENT_POLICY_REQUIRE_PRECEDING if timing_version == 1 else None,
    )
    if stored_ambient_policy != expected_ambient_policy:
        raise ValueError("thermal native RAW ambient policy differs from frozen plan")
    if expected_ambient_policy == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT:
        if (
            any(
                step.get("capture_role") == "ambient"
                or step.get("source_id") == "ambient"
                for step in plan.get("captures", [])
            )
            or plan.get("budgets", {}).get("ambient_cap") != 0
        ):
            raise ValueError("TD-B unsubtracted_no_ambient plan contains ambient evidence")
    if timing_version == 2:
        for step in plan.get("captures", []):
            if "timing_tolerance_s" in step or "actual_elapsed_s" in step:
                raise ValueError("thermal v2 plan contains legacy timing fields")
            if step.get("formal_measurement") and step.get("timing_acceptance") != "observed_elapsed_record_only":
                raise ValueError("thermal v2 plan lacks observed-elapsed acceptance semantics")
    capture_settings = _validate_capture_settings_provenance(plan, run)
    captures = _load_jsonl(root / "captures.jsonl")
    covariates = _load_jsonl(root / "thermal-covariates.jsonl")
    physical_ledger_required = timing_version == 2
    physical_returns = (
        _load_jsonl(root / "physical-returns.jsonl")
        if physical_ledger_required and (root / "physical-returns.jsonl").is_file()
        else []
    )
    if physical_ledger_required and not (root / "physical-returns.jsonl").is_file():
        raise ValueError("thermal v2 physical return ledger is missing")
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
    setup_physical = 0
    setup_ref = plan.get("exposure_setup_artifact")
    if setup_ref is not None:
        if plan.get("experiment_id") != thermal.TD_B or plan.get("source") != "ray" or not isinstance(setup_ref, Mapping):
            raise ValueError("thermal setup artifact has an invalid experiment owner")
        setup_path = Path(str(setup_ref.get("path"))).resolve()
        if not setup_path.is_file() or _sha256_file(setup_path) != setup_ref.get("sha256"):
            raise ValueError("thermal setup artifact hash differs from plan")
        setup_artifact = _load_json(setup_path)
        validated_setup = thermal.validate_td_b_exposure_setup(setup_artifact, artifact_path=setup_path)
        if setup_artifact.get("fake_only") is True:
            raise ValueError("public thermal analyzer rejects fake setup evidence")
        setup_physical = int(validated_setup["physical_count"])
        if int(plan.get("setup_physical_cr3_count", -1)) != setup_physical:
            raise ValueError("thermal setup physical count differs from resolved plan")
    elif plan.get("experiment_id") == thermal.TD_B and plan.get("source") == "ray":
        raise ValueError("Ray TD-B analysis requires retained setup artifact")
    thermal.audit_chronology(covariates)
    recomputed_formal = 0
    recomputed_ambient = 0
    physical_by_capture: dict[str, Mapping[str, Any]] = {}
    owned_physical_paths: set[Path] = set()
    for index, row in enumerate(physical_returns, start=1):
        if (
            row.get("schema") != thermal.PHYSICAL_RETURN_LEDGER_SCHEMA
            or row.get("physical_index") != index
            or row.get("accepted_measurement") is not False
        ):
            raise ValueError("thermal physical return ledger schema or order differs")
        capture_id = row.get("capture_id")
        if not isinstance(capture_id, str) or capture_id in physical_by_capture:
            raise ValueError("thermal physical return ledger owner is missing or duplicated")
        raw_candidate = Path(str(row.get("cr3_path")))
        raw_path = raw_candidate.resolve()
        if (
            raw_candidate.is_symlink()
            or not raw_path.is_relative_to(root.resolve())
            or not raw_path.is_file()
            or raw_path.stat().st_size <= 0
            or raw_path in owned_physical_paths
            or row.get("cr3_byte_count") != raw_path.stat().st_size
            or row.get("cr3_sha256") != _sha256_file(raw_path)
        ):
            raise ValueError("thermal physical return ledger CR3 evidence differs")
        physical_by_capture[capture_id] = row
        owned_physical_paths.add(raw_path)
    if physical_ledger_required and len(physical_returns) != len(captures):
        raise ValueError("thermal physical return and accepted capture ledgers differ")
    recomputed_physical = setup_physical + len(physical_returns)
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
        payload_ambient_policy = payload.get(
            "native_raw_ambient_policy",
            raw_validation.AMBIENT_POLICY_REQUIRE_PRECEDING
            if timing_version == 1 else None,
        )
        if payload_ambient_policy != expected_ambient_policy:
            raise ValueError("thermal accepted capture ambient policy drifted")
        if timing_version == 2:
            report_value = payload.get("patch_statistics")
            report_path = Path(str(report_value)).resolve() if report_value else None
            if (
                report_path is None
                or not report_path.is_relative_to(root.resolve())
                or not report_path.is_file()
            ):
                raise ValueError("thermal accepted capture native RAW report is missing")
            report = _load_json(report_path)
            report_context = report.get("analysis_context")
            if (
                not isinstance(report_context, Mapping)
                or report_context.get("native_raw_ambient_policy") != expected_ambient_policy
                or bool(report_context.get("ambient_subtraction_applied"))
                != (
                    expected_ambient_policy
                    == raw_validation.AMBIENT_POLICY_REQUIRE_PRECEDING
                    and step.get("source_id") != "ambient"
                )
            ):
                raise ValueError("thermal native RAW report ambient policy replay failed")
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
        if physical_ledger_required:
            physical_row = physical_by_capture.get(str(step["capture_id"]))
            if (
                not isinstance(physical_row, Mapping)
                or Path(str(physical_row.get("cr3_path"))).resolve() != resolved_raw
            ):
                raise ValueError("thermal accepted capture differs from physical return owner")
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
        if not physical_ledger_required:
            recomputed_physical += physical_value
    if recomputed_formal != int(plan["budgets"]["formal_cap"]) or int(run.get("completed_formal", -1)) != recomputed_formal:
        raise ValueError("thermal formal ledger count mismatch")
    if recomputed_ambient != int(plan["budgets"]["ambient_cap"]) or int(run.get("ambient_capture_count", -1)) != recomputed_ambient:
        raise ValueError("thermal ambient ledger count mismatch")
    if int(run.get("setup_physical_cr3_count", 0)) != setup_physical:
        raise ValueError("thermal run setup physical ledger mismatch")
    if (
        physical_ledger_required
        and int(run.get("physical_returned_cr3_count", -1)) != len(physical_returns)
    ):
        raise ValueError("thermal run physical-return counter mismatch")
    if physical_ledger_required and (
        int(run.get("accepted_formal_count", -1)) != recomputed_formal
        or int(run.get("accepted_ambient_count", -1)) != recomputed_ambient
    ):
        raise ValueError("thermal run accepted measurement counters mismatch")
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
        "physical_cr3_count": recomputed_physical, "setup_physical_cr3_count": setup_physical,
        "native_raw_ambient_policy": expected_ambient_policy,
        "retained_npy_count": 0,
        "timing_absolute_truth": False,
        "timing_source": "best_effort_gphoto2_observed_elapsed" if timing_version == 2 else "best_effort_gphoto2",
        "timing_contract_evidence": dict(expected_contract),
        "tier_distribution": dict(timing_tiers),
        "unknown_uncertainty_count": timing_unknown,
    }
    if timing_version == 2:
        report["timing_slot_summary"] = timing_slot_summary
        report.update({
            "physical_returned_cr3_count": len(physical_returns),
            "accepted_formal_count": recomputed_formal,
            "accepted_ambient_count": recomputed_ambient,
        })
    report.update(result)
    return report


def replay_retained_td_b_first_capture(
    output_dir: str | Path,
    *,
    raw_analyze_fn: Callable[..., Mapping[str, Any]] | None = None,
    raw_report_writer: Callable[[str | Path, Mapping[str, Any]], Path] | None = None,
) -> dict[str, Any]:
    """Replay the fixed failed-run CR3 as forensic-only, never formal evidence."""
    return _replay_td_b_first_capture(
        cr3_path=TD_B_RETAINED_FIRST_CAPTURE_PATH,
        sidecar_path=TD_B_RETAINED_FIRST_SIDECAR_PATH,
        failed_run_path=TD_B_RETAINED_FAILED_RAY_RUN,
        expected_cr3_sha256=TD_B_RETAINED_FIRST_CAPTURE_SHA256,
        expected_sidecar_sha256=TD_B_RETAINED_FIRST_SIDECAR_SHA256,
        expected_capture_id=TD_B_RETAINED_FIRST_CAPTURE_ID,
        expected_request_id=TD_B_RETAINED_FIRST_REQUEST_ID,
        output_dir=output_dir,
        raw_analyze_fn=raw_analyze_fn,
        raw_report_writer=raw_report_writer,
    )


def _replay_td_b_first_capture(
    *,
    cr3_path: str | Path,
    sidecar_path: str | Path,
    failed_run_path: str | Path,
    expected_cr3_sha256: str,
    expected_sidecar_sha256: str,
    expected_capture_id: str,
    expected_request_id: str,
    output_dir: str | Path,
    raw_analyze_fn: Callable[..., Mapping[str, Any]] | None = None,
    raw_report_writer: Callable[[str | Path, Mapping[str, Any]], Path] | None = None,
) -> dict[str, Any]:
    from camera_based_rgbww_optimizer.control import camera_gphoto2
    from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches
    from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
        RecordedExposure,
        parse_nominal_exposure,
    )

    root = Path(failed_run_path).resolve()
    raw_candidate = Path(cr3_path)
    sidecar_candidate = Path(sidecar_path)
    raw = raw_candidate.resolve()
    sidecar = sidecar_candidate.resolve()
    if (
        raw_candidate.is_symlink()
        or sidecar_candidate.is_symlink()
        or not raw.is_relative_to(root)
        or not sidecar.is_relative_to(root)
        or not raw.is_file()
        or raw.stat().st_size <= 0
        or not sidecar.is_file()
        or sidecar.stat().st_size <= 0
    ):
        raise ValueError("retained TD-B first-capture owner is missing or outside failed run")
    payload = raw.read_bytes()
    if (
        hashlib.sha256(payload).hexdigest() != expected_cr3_sha256
        or hashlib.sha256(sidecar.read_bytes()).hexdigest()
        != expected_sidecar_sha256
    ):
        raise ValueError("retained TD-B first-capture CR3 or sidecar hash differs")

    plan = _load_json(root / "plan.json")
    commands = _load_jsonl(root / "commands.jsonl")
    expected_step = {
        "capture_id": "000-ray-a-t600",
        "capture_role": "formal",
        "command": {"hue": 120, "intensity_percent": 100.0, "sat": 100},
        "exact_command_hash": (
            "88de37b2161c25b401d616a34c105199243afe21c15545fe5a27691adbdbc96c"
        ),
        "formal_measurement": True,
        "isolation_gate_after": "after_initial_anchor",
        "requested_elapsed_s": 600,
        "role": "initial_anchor",
        "source_id": "ray",
        "state_id": "A",
        "timing_acceptance": "observed_elapsed_record_only",
        "timing_status": "resolved",
    }
    if (
        plan.get("experiment_id") != thermal.TD_B
        or plan.get("schema") != thermal.PLAN_SCHEMA_V2
        or plan.get("source") != "ray"
        or plan.get("frozen_shutters", {}).get("ray-h120-s100") != "1/5000"
        or not isinstance(plan.get("captures"), list)
        or not plan["captures"]
        or plan["captures"][0] != expected_step
    ):
        raise ValueError("retained TD-B first-capture frozen plan identity differs")
    first_command = commands[0] if commands else {}
    if (
        first_command.get("event") != "command_readback_verified"
        or first_command.get("source_id") != "ray"
        or first_command.get("state_id") != "A"
        or first_command.get("exact_command_hash")
        != expected_step["exact_command_hash"]
        or (first_command.get("readback") or {}).get("data")
        != {"hue": 120, "sat": 100, "intensity": 1000}
    ):
        raise ValueError("retained TD-B first-capture command/readback owner differs")

    try:
        metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        remote, receipt = camera_remote_v2.split_and_validate_sidecar(
            metadata,
            payload=payload,
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        camera_remote_v2.RemoteCaptureV2Error,
    ) as exc:
        raise ValueError("retained TD-B first-capture sidecar replay failed") from exc
    recorded = remote.get("recorded_exposure") or {}
    timing = receipt.get("timing_evidence") or {}
    if (
        remote.get("capture_id") != expected_capture_id
        or remote.get("request_id") != expected_request_id
        or recorded.get("status") != "recorded"
        or recorded.get("source") != "Canon:ExposureTime"
        or not isinstance(recorded.get("seconds"), (int, float))
        or float(recorded["seconds"]) <= 0
        or timing.get("tier") != "tier_b"
        or timing.get("status") != "accepted_best_effort_anchor"
    ):
        raise ValueError("retained TD-B first-capture ID/exposure/timing association differs")

    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    measurements = output / "measurements"
    measurements.mkdir()
    shutter = "1/5000"
    nominal_seconds = parse_nominal_exposure(shutter)
    exposure = RecordedExposure(
        seconds=float(recorded["seconds"]),
        source="Canon:ExposureTime",
        nominal_seconds=nominal_seconds,
        nominal_shutter_speed=shutter,
        raw_file=raw,
        status="recorded",
        metadata_values={"Canon:ExposureTime": float(recorded["seconds"])},
    )
    capture = camera_gphoto2.CaptureResult(
        connection=camera_gphoto2.CameraConnection(
            model="Canon EOS R6 Mark III via retained remote-v2 evidence",
            port="forensic-only",
        ),
        settings=camera_gphoto2.CaptureSettings(
            iso="100",
            aperture="implicit auto",
            shutter_speed=shutter,
            image_format="RAW",
        ),
        saved_file=raw,
        stdout="",
        backend="remote",
        endpoint="/v2/capture",
        http_attempts=int(receipt["http_attempts"]),
        remote_metadata_path=sidecar,
        timing_metadata=metadata,
        timing_evidence=timing,
    )
    analyze_fn = raw_analyze_fn or raw_mosaic_patches.analyze_raw_file
    writer = raw_report_writer or raw_mosaic_patches.write_report
    report_path, quality = raw_validation._write_native_capture_report(
        capture,
        step={
            "capture_id": expected_step["capture_id"],
            "source": "ray",
            "purpose": "p7_td_b_retained_first_capture_forensic",
            "repeat_index": 0,
            "analysis_context": {
                "forensic_only": True,
                "accepted_formal": False,
                "reusable_capture": False,
                "phase": "TD-B",
                "formal_measurement": True,
            },
        },
        ambient_capture=None,
        capture_exposure=exposure,
        location_config_path=thermal.LOCATION_PATH,
        observer_config_path=thermal.OBSERVER_PATH,
        measurements_dir=measurements,
        raw_analyze_fn=analyze_fn,
        raw_report_writer=writer,
        ambient_policy=raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        ambient_policy_owner=raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER,
    )
    report = _load_json(report_path)
    feature_ids = _load_json(thermal.POLICY_PATH)["feature_set"]["ids"]
    features = td_b_feature_map_from_report(report, feature_ids)
    if len(features) != 58 or set(features) != set(feature_ids):
        raise ValueError("retained TD-B first-capture replay lacks frozen 58 features")
    feature_payload = json.dumps(
        features,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    artifact = {
        "schema": "p7_td_b_retained_first_capture_forensic_replay_v1",
        "status": "pass",
        "forensic_only": True,
        "accepted_formal": False,
        "reusable_capture": False,
        "failed_run": str(root),
        "plan_reference": {
            "path": str((root / "plan.json").resolve()),
            "sha256": _sha256_file(root / "plan.json"),
        },
        "command_reference": {
            "path": str((root / "commands.jsonl").resolve()),
            "sha256": _sha256_file(root / "commands.jsonl"),
        },
        "cr3": {
            "path": str(raw),
            "sha256": expected_cr3_sha256,
            "byte_count": raw.stat().st_size,
        },
        "sidecar": {
            "path": str(sidecar),
            "sha256": expected_sidecar_sha256,
        },
        "capture_id": expected_capture_id,
        "request_id": expected_request_id,
        "recorded_exposure": exposure.to_jsonable(),
        "timing_evidence": dict(timing),
        "native_raw_ambient_policy": (
            raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        ),
        "ambient_policy_owner": dict(
            raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER
        ),
        "ambient_subtraction_applied": False,
        "report_reference": {
            "path": str(Path(report_path).resolve()),
            "sha256": _sha256_file(Path(report_path)),
        },
        "quality": dict(quality),
        "feature_count": len(features),
        "feature_ids": list(feature_ids),
        "feature_statistic": TD_B_FORMAL_FEATURE_STATISTIC,
        "features_sha256": hashlib.sha256(feature_payload).hexdigest(),
    }
    artifact_path = output / "retained-first-capture-replay.json"
    _write_text_atomic(
        artifact_path,
        json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n",
    )
    return artifact


def analyze_td_b_setup_resolution(
    plan: Mapping[str, Any], *, setup_artifact_path: str | Path,
) -> dict[str, Any]:
    """Public offline analyzer for the setup-to-resolved-plan boundary."""
    return thermal.replay_td_b_setup_resolution(
        plan, setup_artifact_path=setup_artifact_path,
    )


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
    r6_operational_contract: bool = False,
) -> dict[str, Any]:
    if r6_operational_contract:
        if len(captures) != 16:
            raise ValueError("Ray R6 analyzer requires complete 16/16 engineering/quality input")
        if tuple(str(row.get("capture_id")) for row in captures) != thermal.TD_B_R6_CAPTURE_IDS:
            raise ValueError("Ray R6 analyzer requires exact 000..015 order")
        if any(
            row.get("engineering_quality_status") != "pass"
            or row.get("origin") != "ray_r6"
            for row in captures
        ):
            raise ValueError("Ray R6 analyzer requires 16/16 accepted R6-only inputs")
        roots = {str(row.get("run_root")) for row in captures}
        if len(roots) != 1 or "" in roots:
            raise ValueError("Ray R6 analyzer prohibits old/new or cross-root pooling")
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
    if r6_operational_contract:
        nonstationary_states = sorted(
            state for state, result in state_results.items()
            if result.get("t_settle_s") is None
        )
        return {
            "status": (
                "td_b_operational_600_complete_waiting_for_planner"
                if history_pass else "history_dependent_at_operational_dwell_600"
            ),
            "formal_pass": bool(history_pass),
            "return_anchor_history": "pass" if history_pass else "fail",
            "return_anchor_history_effect": "pass" if history_pass else "fail",
            "steady_status": "not_demonstrated",
            "time_dependent_within_600": bool(nonstationary_states),
            "operational_endpoint_600_valid": bool(history_pass),
            "operational_dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "nonstationary_states": nonstationary_states,
            "state_specific_settle_time": {
                state: result["t_settle_s"] for state, result in state_results.items()
            },
            "strip_unlock_condition": "planner_accepts_complete_ray_r6_history_pass",
            "td_c_unlock_condition": "combined_td_b_pass",
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
        if name == "operating_envelope":
            thermal.validate_trusted_operating_envelope_reference(reference)
            continue
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


def analyze_td_b_pair(
    ray_run: str | Path, strip_run: str | Path, output_dir: str | Path,
    *, feature_ids: Sequence[str], feature_ids_path: str | Path,
    code_checkpoint: str, final_zero_path: str | Path,
) -> dict[str, Any]:
    checkpoint = _validate_code_checkpoint(code_checkpoint)
    ray_root = Path(ray_run).resolve()
    strip_root = Path(strip_run).resolve()
    output = Path(output_dir).resolve()
    zero_path = Path(final_zero_path).resolve()
    if ray_root == strip_root or output.exists():
        raise ValueError("TD-B paired finalizer requires distinct runs and a new output directory")
    ray_plan = _load_json(ray_root / "plan.json")
    strip_plan = _load_json(strip_root / "plan.json")
    if (
        ray_plan.get("experiment_id") != thermal.TD_B
        or strip_plan.get("experiment_id") != thermal.TD_B
        or ray_plan.get("source") != "ray" or strip_plan.get("source") != "strip"
        or ray_plan.get("schema") != thermal.PLAN_SCHEMA_V2
        or strip_plan.get("schema") != thermal.PLAN_SCHEMA_V2
        or ray_plan.get("inputs") != strip_plan.get("inputs")
    ):
        raise ValueError("TD-B paired finalizer source, schema, or frozen input owner differs")
    feature_path = Path(feature_ids_path).resolve()
    if _feature_ids_from_artifact(feature_path) != list(feature_ids):
        raise ValueError("TD-B paired finalizer feature IDs differ")
    ray_report = analyze_thermal_run(ray_root, feature_ids=feature_ids)
    strip_report = analyze_thermal_run(strip_root, feature_ids=feature_ids)
    allowed_statuses = {
        "td_b_operational_600_complete_waiting_for_planner",
        "history_dependent_at_operational_dwell_600",
    }
    for source, report in (("ray", ray_report), ("strip", strip_report)):
        if (
            report.get("experiment_id") != thermal.TD_B or report.get("source_id") != source
            or report.get("status") not in allowed_statuses
            or report.get("formal_capture_count") != 16 or report.get("ambient_capture_count") != 0
            or report.get("capture_contract") != "pass" or report.get("timing_contract") != "pass"
            or report.get("source_isolation_contract") != "pass" or report.get("cleanup_contract") != "pass"
            or report.get("wrapper_contract") != "pass" or report.get("retained_npy_count") != 0
            or report.get("dwell_is_scientifically_settled") is not False
        ):
            raise ValueError(f"TD-B paired finalizer {source} contract did not pass")
    setup_count = int(ray_report.get("setup_physical_cr3_count", -1))
    ray_physical = int(ray_report.get("physical_cr3_count", -1))
    strip_physical = int(strip_report.get("physical_cr3_count", -1))
    if not 1 <= setup_count <= 8 or ray_physical != setup_count + 16 or strip_physical != 16:
        raise ValueError("TD-B paired finalizer source physical accounting differs")
    total = ray_physical + strip_physical
    if total != setup_count + 32 or not 33 <= total <= 40:
        raise ValueError("TD-B paired finalizer combined physical accounting differs")
    final_zero = _load_json(zero_path)
    if set(final_zero) != {"strip_device_evidence", "ray_readback"}:
        raise ValueError("TD-B paired finalizer independent final zero schema differs")
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
    validate_both_off(
        final_zero["strip_device_evidence"], final_zero["ray_readback"],
        _load_json(thermal.CURVE_PATH),
    )
    combined = {
        "schema": TD_B_COMBINED_ANALYSIS_SCHEMA,
        "experiment_id": thermal.TD_B,
        "status": "td_b_paired_complete_waiting_for_planner",
        "scientifically_settled": False,
        "developer_selected_operational_dwell_s": 600,
        "ray_run": str(ray_root), "strip_run": str(strip_root),
        "source_results": {"ray": ray_report, "strip": strip_report},
        "formal_capture_count": 32, "setup_physical_cr3_count": setup_count,
        "physical_cr3_count": total, "physical_cr3_cap": 40,
        "independent_final_zero": {"path": str(zero_path), "sha256": _sha256_file(zero_path)},
        "default_operating_envelope_modified": False,
    }
    output.mkdir(parents=True, exist_ok=False)
    analysis_path = output / "td-b-combined-analysis.json"
    summary_path = output / "EXPERIMENT_SUMMARY.md"
    manifest_path = output / "input-manifest.json"
    try:
        _write_text_atomic(analysis_path, json.dumps(combined, indent=2, sort_keys=True, allow_nan=False) + "\n")
        _write_text_atomic(summary_path, (
            "# P7 TD-B Combined Analysis\n\n"
            f"- status: `{combined['status']}`\n"
            "- scientifically settled: `false`\n"
            f"- captures: `32` formal + `{setup_count}` setup = `{total}` physical CR3\n"
        ))
        manifest = {
            "schema": TD_B_INPUT_MANIFEST_SCHEMA,
            "decision_owner": "Planner",
            "generated_by": {"module": TD_A_ANALYZER_MODULE, "code_checkpoint": checkpoint},
            "sources": {
                "ray": {"run_dir": str(ray_root), "plan": thermal.file_reference(ray_root / "plan.json"),
                    "analysis": thermal.file_reference(ray_root / "analysis.json")},
                "strip": {"run_dir": str(strip_root), "plan": thermal.file_reference(strip_root / "plan.json"),
                    "analysis": thermal.file_reference(strip_root / "analysis.json")},
            },
            "final_zero": thermal.file_reference(zero_path),
            "outputs": {
                "td-b-combined-analysis.json": thermal.file_reference(analysis_path),
                "EXPERIMENT_SUMMARY.md": thermal.file_reference(summary_path),
            },
        }
        _write_text_atomic(manifest_path, json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n")
        validate_td_b_input_manifest(manifest_path)
    except BaseException:
        for path in (analysis_path, summary_path, manifest_path):
            path.unlink(missing_ok=True)
        try:
            output.rmdir()
        except OSError:
            pass
        raise
    return combined


def validate_td_b_input_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path).resolve()
    manifest = _load_json(manifest_path)
    if set(manifest) != {"schema", "decision_owner", "generated_by", "sources", "final_zero", "outputs"}:
        raise ValueError("TD-B input manifest schema keys differ")
    if manifest.get("schema") != TD_B_INPUT_MANIFEST_SCHEMA or manifest.get("decision_owner") != "Planner":
        raise ValueError("TD-B input manifest identity differs")
    generated = manifest.get("generated_by")
    if not isinstance(generated, Mapping) or set(generated) != {"module", "code_checkpoint"} or generated.get("module") != TD_A_ANALYZER_MODULE:
        raise ValueError("TD-B input manifest generator differs")
    _validate_code_checkpoint(generated.get("code_checkpoint"))
    sources = manifest.get("sources")
    if not isinstance(sources, Mapping) or set(sources) != {"ray", "strip"}:
        raise ValueError("TD-B input manifest source owners differ")
    for source in ("ray", "strip"):
        entry = sources[source]
        if not isinstance(entry, Mapping) or set(entry) != {"run_dir", "plan", "analysis"}:
            raise ValueError("TD-B input manifest source schema differs")
        root = Path(str(entry["run_dir"])).resolve()
        for name in ("plan", "analysis"):
            if entry[name] != thermal.file_reference(root / f"{name}.json"):
                raise ValueError("TD-B input manifest retained source hash differs")
    for name in ("final_zero",):
        reference = manifest.get(name)
        if not isinstance(reference, Mapping) or reference != thermal.file_reference(reference.get("path", "")):
            raise ValueError("TD-B input manifest final zero hash differs")
    outputs = manifest.get("outputs")
    if not isinstance(outputs, Mapping) or set(outputs) != {"td-b-combined-analysis.json", "EXPERIMENT_SUMMARY.md"}:
        raise ValueError("TD-B input manifest output schema differs")
    for name, reference in outputs.items():
        if not isinstance(reference, Mapping) or Path(str(reference.get("path"))).resolve() != manifest_path.parent / name or reference != thermal.file_reference(reference["path"]):
            raise ValueError("TD-B input manifest output owner or hash differs")
    return manifest


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
    parser.add_argument("--final-zero", type=Path, help="Independent final both-off evidence for paired TD-B.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.derive_r1_output is not None and (
        args.paired_run is not None or args.combined_output is not None
        or args.code_checkpoint is not None or args.final_zero is not None
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
        plan = _load_json(args.run_dir / "plan.json")
        if plan.get("experiment_id") == thermal.TD_B:
            if args.final_zero is None:
                raise ValueError("--final-zero is required for paired TD-B finalization")
            analyze_td_b_pair(
                args.run_dir, args.paired_run, args.combined_output,
                feature_ids=feature_ids, feature_ids_path=args.feature_ids,
                code_checkpoint=args.code_checkpoint, final_zero_path=args.final_zero,
            )
            print(args.combined_output / "td-b-combined-analysis.json")
        else:
            if args.final_zero is not None:
                raise ValueError("--final-zero is only valid for paired TD-B finalization")
            analyze_td_a_pair(
                args.run_dir, args.paired_run, args.combined_output,
                feature_ids=feature_ids, feature_ids_path=args.feature_ids,
                code_checkpoint=args.code_checkpoint,
            )
            print(args.combined_output / "td-a-combined-analysis.json")
        print(args.combined_output / "EXPERIMENT_SUMMARY.md")
        print(args.combined_output / "input-manifest.json")
        return 0
    if args.combined_output is not None or args.code_checkpoint is not None or args.final_zero is not None:
        raise ValueError("--combined-output/--code-checkpoint require --paired-run")
    report = analyze_thermal_run(args.run_dir, feature_ids=feature_ids)
    output = args.run_dir / "analysis.json"
    _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
