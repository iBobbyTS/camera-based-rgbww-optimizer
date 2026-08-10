from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
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
from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
    parse_nominal_exposure,
    validate_recorded_exposure_setting,
)
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.control import esphome
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.analyze_hsi_reference_repeatability import (
    write_reference_epoch_v2_derived,
)


POST_FIX_REVALIDATION_SCHEMA = "p7_direct_ray_r6_post_fix_revalidation_v1"
LEGACY_EXPOSURE_FAILURE_MESSAGE = (
    "direct Ray R6 recorded exposure differs from frozen shutter"
)
POST_FIX_REVALIDATION_FILE = "post-fix-revalidation.json"
R6_VECTOR_REANALYSIS_SCHEMA = "p7_ray_r6_vector_reanalysis_v1"
POST_FIX_ORIGINAL_FILES = (
    "experiment-spec.json", "input-checkpoint.json", "run.json",
    "failure.json", "wrapper-result.json", "all-off-python.json",
    "all-off-shell.json", "all-off-shell.exit-status.txt",
)


def analyze_thermal_run(
    run_dir: str | Path,
    *, feature_ids: Sequence[str],
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
    post_fix_revalidation: bool = False,
) -> dict[str, Any]:
    root = Path(run_dir).resolve()
    plan = _load_json(root / "experiment-spec.json")
    run = _load_json(root / "run.json")
    revalidation = (
        _validate_post_fix_revalidation(root, run)
        if post_fix_revalidation
        else None
    )
    if (
        plan.get("experiment_id") not in thermal.EXPERIMENT_IDS
        or run.get("experiment_id") != plan.get("experiment_id")
        or (run.get("status") != "complete" and revalidation is None)
        or run.get("cleanup") != "pass"
        or (
            revalidation is None
            and run.get("capture_settings_provenance")
            != plan.get("camera", {}).get("resolved_capture_settings")
        )
    ):
        raise ValueError("thermal analyzer requires a completed exact experiment")
    if plan.get("execution_authorization", {}).get("schema") == "direct_ray_r6_authority_v1":
        expected = thermal.build_ray_r6_spec()
        if plan != expected:
            raise ValueError("direct Ray R6 spec drifted")
        _validate_required_execution_artifacts(root)
        _validate_reproducibility_checkpoint(root, plan, run)
        captures = _load_jsonl(root / "captures.jsonl")
        physical = _load_jsonl(root / "physical-returns.jsonl")
        if len(captures) != 16 or len(physical) != 16:
            raise ValueError("direct Ray R6 requires exactly 16 accepted and physical rows")
        if [row.get("capture_id") for row in captures] != expected["capture_ids"]:
            raise ValueError("direct Ray R6 capture order drifted")
        if [row.get("capture_id") for row in physical] != expected["capture_ids"]:
            raise ValueError("direct Ray R6 physical order drifted")
        _validate_run_counts(run, plan, captures, physical)
        capture_settings = _validate_capture_settings_provenance(
            plan, run, captures,
            allow_implicit_aperture_reconciliation=revalidation is not None,
        )
        physical_by_id = _validate_physical_rows(root, captures, physical)
        expected_steps = {str(row["capture_id"]): row for row in expected["captures"]}
        for row in captures:
            capture_id = str(row["capture_id"])
            step = row.get("plan_step")
            capture = row.get("capture")
            if not isinstance(step, Mapping) or not isinstance(capture, Mapping):
                raise ValueError("direct Ray R6 capture artifact lacks its owners")
            expected_step = expected_steps.get(capture_id)
            if expected_step is None or dict(step) != dict(expected_step):
                raise ValueError("direct Ray R6 capture step differs from canonical spec")
            if any(row.get(key) != expected_step.get(key) for key in (
                "capture_id", "source_id", "state_id", "capture_role", "formal_measurement",
            )):
                raise ValueError("direct Ray R6 capture ledger differs from canonical spec")
            values = capture.get("feature_values")
            if (
                not isinstance(values, Mapping)
                or tuple(values) != tuple(feature_ids)
                or any(
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    for value in values.values()
                )
            ):
                raise ValueError("direct Ray R6 capture feature owner differs from frozen policy")
            direct_quality = capture.get("direct_quality")
            if (
                not isinstance(direct_quality, Mapping)
                or direct_quality.get("status") != "pass"
                or direct_quality.get("feature_count") != len(feature_ids)
            ):
                raise ValueError("direct Ray R6 RAW feature quality did not pass")
            _validate_recorded_exposure(capture, str(expected_step["nominal_shutter"]))
            strip_zero = capture.get("strip_zero_before_capture")
            requested_zero = strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
            observed_zero = strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
            if (
                not isinstance(requested_zero, Mapping)
                or any(int(value) != 0 for value in requested_zero.values())
                or not isinstance(observed_zero, Mapping)
                or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError("direct Ray R6 capture lacks verified strip-zero evidence")
            if capture_id not in physical_by_id:
                raise ValueError("direct Ray R6 capture lacks a physical return")
        quality = _load_json(root / "quality.json")
        expected_quality_rows = [
            {"capture_id": capture_id, "status": "pass", "feature_count": len(feature_ids)}
            for capture_id in expected["capture_ids"]
        ]
        if (
            quality.get("schema") != "p7_direct_ray_r6_quality_v1"
            or quality.get("status") != "pass"
            or quality.get("experiment_id") != thermal.TD_B
            or quality.get("capture_count") != 16
            or quality.get("rows") != expected_quality_rows
        ):
            raise ValueError("direct Ray R6 quality artifact did not pass")
        _validate_commands_and_gates(plan, root)
        _validate_cleanup_and_wrapper(
            root, post_fix_revalidation=post_fix_revalidation,
        )
        formal = []
        for row in captures:
            capture = row.get("capture")
            if not isinstance(capture, Mapping):
                raise ValueError("direct Ray R6 capture owner is missing")
            enriched = dict(row)
            enriched["feature_values"] = capture.get("feature_values")
            enriched["origin"] = "ray_r6"
            enriched["run_root"] = str(root)
            enriched["engineering_quality_status"] = "pass"
            formal.append(enriched)
        result = analyze_td_b(
            formal, feature_ids=feature_ids, r6_operational_contract=True,
        )
        report = {
            "schema": thermal.ANALYSIS_SCHEMA_V2,
            "status": "pass",
            "experiment_id": thermal.TD_B,
            "capture_count": 16,
            "direct_artifact_validation": "pass",
            **result,
        }
        if revalidation is not None:
            report["engineering_revalidation"] = {
                "schema": revalidation["schema"],
                "status": revalidation["status"],
                "artifact": POST_FIX_REVALIDATION_FILE,
                "sha256": _sha256(root / POST_FIX_REVALIDATION_FILE),
            }
            report["capture_settings_reconciliation"] = capture_settings
        return report
    if post_fix_revalidation:
        raise ValueError("post-fix revalidation only supports direct Ray R6")
    if str(plan.get("execution_authorization", {}).get("schema", "")).startswith("direct_"):
        prerequisite = plan.get("scientific_prerequisite")
        if (
            not isinstance(prerequisite, Mapping)
            or not isinstance(prerequisite.get("path"), str)
            or not isinstance(prerequisite.get("sha256"), str)
        ):
            raise ValueError("direct downstream run lacks its scientific prerequisite")
        prerequisite_path = Path(prerequisite["path"]).resolve()
        if (
            prerequisite_path.is_symlink()
            or not prerequisite_path.is_file()
            or hashlib.sha256(prerequisite_path.read_bytes()).hexdigest()
            != prerequisite["sha256"]
        ):
            raise ValueError("direct downstream prerequisite content hash drifted")
        prerequisite_value = _load_json(prerequisite_path)
        if plan.get("experiment_id") == thermal.TD_C:
            if not str(prerequisite_value.get("status", "")).endswith("_pass"):
                raise ValueError("TD-C direct run lacks a passing combined analysis")
        elif prerequisite_value.get("formal_pass") is not True:
            raise ValueError("strip TD-B direct run lacks a passing Ray analysis")
        expected = thermal.build_direct_plan(
            str(plan["experiment_id"]),
            source=plan.get("source"),
            variant=str(plan.get("variant", "core")),
        )
        if _stable_spec(plan) != _stable_spec(expected):
            raise ValueError("direct run spec differs from the canonical protocol")
        _validate_required_execution_artifacts(root)
        _validate_reproducibility_checkpoint(root, plan, run)
        captures = _load_jsonl(root / "captures.jsonl")
        physical = _load_jsonl(root / "physical-returns.jsonl")
        expected_ids = [str(step["capture_id"]) for step in expected["captures"]]
        if [str(row.get("capture_id")) for row in captures] != expected_ids:
            raise ValueError("direct capture order differs from its spec")
        if [str(row.get("capture_id")) for row in physical] != expected_ids:
            raise ValueError("direct physical order differs from its spec")
        formal = [row for row in captures if row.get("formal_measurement")]
        ambients = [row for row in captures if not row.get("formal_measurement")]
        _validate_run_counts(run, plan, captures, physical)
        physical_by_id = _validate_physical_rows(root, captures, physical)
        expected_steps = {str(step["capture_id"]): step for step in expected["captures"]}
        for row in captures:
            capture = row.get("capture")
            step = row.get("plan_step")
            capture_id = str(row.get("capture_id"))
            expected_step = expected_steps.get(capture_id)
            if (
                not isinstance(capture, Mapping)
                or not isinstance(step, Mapping)
                or expected_step is None
                or dict(step) != dict(expected_step)
                or any(row.get(key) != expected_step.get(key) for key in (
                    "capture_id", "source_id", "state_id", "capture_role", "formal_measurement",
                ))
            ):
                raise ValueError("direct capture differs from the canonical protocol")
            values = capture.get("feature_values")
            if row.get("formal_measurement") and (
                not isinstance(values, Mapping)
                or tuple(values) != tuple(feature_ids)
                or any(
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(float(value))
                    for value in values.values()
                )
            ):
                raise ValueError("direct capture lacks exact frozen feature values")
            if row.get("formal_measurement"):
                direct_quality = capture.get("direct_quality")
                if (
                    not isinstance(direct_quality, Mapping)
                    or direct_quality.get("status") != "pass"
                    or direct_quality.get("feature_count") != len(feature_ids)
                ):
                    raise ValueError("direct capture RAW feature quality did not pass")
                cache_key = thermal.shutter_cache_key_for_step(expected_step)
                nominal_shutter = plan.get("frozen_shutters", {}).get(cache_key)
                if not isinstance(nominal_shutter, str):
                    raise ValueError("direct capture lacks its frozen shutter")
                _validate_recorded_exposure(capture, nominal_shutter)
            if row.get("source_id") == "ray":
                zero = capture.get("strip_zero_before_capture")
                requested = zero.get("requested_payload") if isinstance(zero, Mapping) else None
                observed = zero.get("device_snapshot") if isinstance(zero, Mapping) else None
                if (
                    not isinstance(requested, Mapping)
                    or any(int(value) != 0 for value in requested.values())
                    or not isinstance(observed, Mapping)
                    or any(int(observed.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
                ):
                    raise ValueError("direct Ray capture lacks verified strip-zero evidence")
            if capture_id not in physical_by_id:
                raise ValueError("direct capture lacks physical return")
        quality = _load_json(root / "quality.json")
        expected_quality_rows = [
            {"capture_id": str(row["capture_id"]), "status": "pass"}
            for row in expected["captures"] if row.get("formal_measurement")
        ]
        if (
            quality.get("schema") != "p7_direct_protocol_quality_v1"
            or quality.get("status") != "pass"
            or quality.get("experiment_id") != plan["experiment_id"]
            or quality.get("capture_count") != len(formal)
            or quality.get("rows") != expected_quality_rows
        ):
            raise ValueError("direct quality artifact did not pass")
        _validate_commands_and_gates(plan, root)
        _validate_cleanup_and_wrapper(root)
        formal_rows = []
        for row in formal:
            enriched = dict(row)
            enriched["feature_values"] = row["capture"]["feature_values"]
            enriched["engineering_quality_status"] = "pass"
            enriched["run_root"] = str(root)
            formal_rows.append(enriched)
        if plan.get("experiment_id") == thermal.TD_B:
            result = analyze_td_b(formal_rows, feature_ids=feature_ids)
        else:
            result = analyze_td_c(
                formal_rows, ambients=ambients, feature_ids=feature_ids,
                compatibility_fn=compatibility_fn,
            )
        return {
            "schema": thermal.ANALYSIS_SCHEMA_V2,
            "status": "pass",
            "experiment_id": plan["experiment_id"],
            "capture_count": len(formal_rows),
            "direct_artifact_validation": "pass",
            **result,
        }
    raise ValueError("thermal analyzer supports direct protocol runs only")


def _stable_spec(value: Mapping[str, Any]) -> dict[str, Any]:
    stable = dict(value)
    stable.pop("created_at", None)
    stable.pop("scientific_prerequisite", None)
    return stable


def _validate_required_execution_artifacts(root: Path) -> None:
    required = (
        "captures.jsonl", "physical-returns.jsonl", "quality.json",
        "commands.jsonl", "commands-audit.json", "isolation-gates.jsonl",
        "all-off-python.json", "all-off-shell.json",
        "all-off-shell.exit-status.txt", "wrapper-result.json",
        "input-checkpoint.json",
    )
    if any(
        not (root / name).is_file() or (root / name).is_symlink()
        for name in required
    ):
        raise ValueError("direct run lacks a required execution artifact")


def _validate_reproducibility_checkpoint(
    root: Path, plan: Mapping[str, Any], run: Mapping[str, Any],
) -> None:
    checkpoint = _load_json(root / "input-checkpoint.json")
    git = checkpoint.get("git")
    if (
        checkpoint.get("schema") != "p7_direct_reproducibility_checkpoint_v1"
        or not isinstance(git, Mapping)
        or not isinstance(git.get("commit"), str)
        or not git["commit"]
        or git.get("dirty") is not False
        or run.get("git") != dict(git)
        or run.get("reproducibility_checkpoint") != "input-checkpoint.json"
    ):
        raise ValueError("direct run Git checkpoint is missing or dirty")
    plan_inputs = plan.get("inputs")
    checkpoint_inputs = checkpoint.get("inputs")
    if not isinstance(plan_inputs, Mapping) or not isinstance(checkpoint_inputs, Mapping):
        raise ValueError("direct run reproducibility inputs are missing")
    for name in ("location", "code_duty_curve"):
        reference = plan_inputs.get(name)
        item = checkpoint_inputs.get(name)
        if (
            not isinstance(reference, Mapping)
            or not isinstance(item, Mapping)
            or item.get("sha256") != reference.get("sha256")
            or not isinstance(item.get("run_path"), str)
        ):
            raise ValueError(f"direct run {name} checkpoint differs from its spec")
        path = (root / item["run_path"]).resolve()
        if (
            path.is_symlink()
            or not path.is_file()
            or not path.is_relative_to(root)
            or item.get("byte_count") != path.stat().st_size
            or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]
        ):
            raise ValueError(f"direct run {name} checkpoint payload drifted")


def _validate_run_counts(
    run: Mapping[str, Any],
    plan: Mapping[str, Any],
    captures: Sequence[Mapping[str, Any]],
    physical: Sequence[Mapping[str, Any]],
) -> None:
    formal = sum(bool(row.get("formal_measurement")) for row in captures)
    ambient = len(captures) - formal
    if (
        len(captures) != len(plan.get("captures", ()))
        or len(physical) != len(captures)
        or run.get("completed_formal") != formal
        or run.get("accepted_formal_count") != formal
        or run.get("ambient_capture_count") != ambient
        or run.get("accepted_ambient_count") != ambient
        or run.get("physical_returned_cr3_count") != len(physical)
        or run.get("physical_cr3_count")
        != int(plan.get("setup_physical_cr3_count", 0)) + len(physical)
    ):
        raise ValueError("direct run counters differ from retained artifacts")


def _validate_capture_settings_provenance(
    plan: Mapping[str, Any],
    run: Mapping[str, Any],
    captures: Sequence[Mapping[str, Any]],
    *,
    allow_implicit_aperture_reconciliation: bool,
) -> dict[str, Any]:
    planned = plan.get("camera", {}).get("resolved_capture_settings")
    runtime = run.get("capture_settings_provenance")
    if not isinstance(planned, Mapping) or not isinstance(runtime, Mapping):
        raise ValueError("direct capture settings provenance is missing")
    if planned == runtime:
        return {"status": "exact", "runtime": dict(runtime)}
    if not allow_implicit_aperture_reconciliation or any(
        runtime.get(key) != planned.get(key)
        for key in ("owner", "iso", "image_format")
    ) or planned.get("aperture") != "f/4" or runtime.get("aperture") != "implicit auto":
        raise ValueError("direct capture settings differ from the frozen spec")
    actual_rows = []
    for row in captures:
        capture = row.get("capture")
        device_capture = capture.get("capture") if isinstance(capture, Mapping) else None
        if (
            not isinstance(device_capture, Mapping)
            or device_capture.get("iso") != runtime["iso"]
            or device_capture.get("image_format") != runtime["image_format"]
            or device_capture.get("aperture") != runtime["aperture"]
        ):
            raise ValueError("direct capture settings are not uniform across retained frames")
        actual_rows.append(str(row.get("capture_id")))
    return {
        "status": "accepted_uniform_implicit_aperture",
        "planned_aperture_projection": planned["aperture"],
        "runtime_aperture": runtime["aperture"],
        "iso": runtime["iso"],
        "image_format": runtime["image_format"],
        "capture_count": len(actual_rows),
        "scientific_interpretation": "aperture_setting_unchanged_value_not_reported",
    }


def _validate_physical_rows(
    root: Path,
    captures: Sequence[Mapping[str, Any]],
    physical: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    expected_ids = [str(row.get("capture_id")) for row in captures]
    if [str(row.get("capture_id")) for row in physical] != expected_ids:
        raise ValueError("direct physical-return order differs from captures")
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(physical, start=1):
        capture_id = str(row.get("capture_id"))
        if capture_id in by_id or row.get("physical_index") != index:
            raise ValueError("direct physical-return identity is duplicated or reordered")
        for prefix in ("cr3", "sidecar"):
            path = Path(str(row.get(f"{prefix}_path"))).resolve()
            if path.is_symlink() or not path.is_file() or not path.is_relative_to(root):
                raise ValueError("direct physical artifact escaped the run root")
            payload = path.read_bytes()
            if (
                not payload
                or row.get(f"{prefix}_byte_count") != len(payload)
                or row.get(f"{prefix}_sha256") != hashlib.sha256(payload).hexdigest()
            ):
                raise ValueError("direct physical artifact content differs from its ledger")
        if row.get("sidecar_validation_status") != "pass":
            raise ValueError("direct physical return was not accepted")
        by_id[capture_id] = row
    return by_id


def _validate_recorded_exposure(
    capture: Mapping[str, Any], nominal_shutter: str,
) -> None:
    recorded = capture.get("recorded_exposure")
    if not isinstance(recorded, Mapping):
        raise ValueError("direct recorded exposure metadata is missing")
    validate_recorded_exposure_setting(recorded, nominal_shutter)


def _execution_groups(
    experiment_id: str, captures: Sequence[Mapping[str, Any]],
) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if step.get("capture_role") == "ambient":
            groups.append([step])
            continue
        key = thermal.timing_sequence_identity(experiment_id, step)
        previous = (
            groups[-1][0]
            if groups and groups[-1][0].get("capture_role") == "formal"
            else None
        )
        previous_key = (
            None
            if previous is None
            else thermal.timing_sequence_identity(experiment_id, previous)
        )
        if (
            groups
            and previous is not None
            and key == previous_key
            and float(step["requested_elapsed_s"])
            > float(groups[-1][-1]["requested_elapsed_s"])
        ):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def _validate_commands_and_gates(
    plan: Mapping[str, Any], root: Path, *, require_audit: bool = True,
) -> None:
    groups = _execution_groups(str(plan["experiment_id"]), plan["captures"])
    command_steps = [group[0] for group in groups if group[0]["capture_role"] != "ambient"]
    commands = _load_jsonl(root / "commands.jsonl")
    if len(commands) != len(command_steps):
        raise ValueError("direct command ledger count differs from protocol transitions")
    for row, step in zip(commands, command_steps, strict=True):
        if (
            row.get("event") != "command_readback_verified"
            or row.get("source_id") != step.get("source_id")
            or row.get("state_id") != step.get("state_id")
            or row.get("exact_command_hash") != step.get("exact_command_hash")
            or not isinstance(row.get("at"), str)
            or not isinstance(row.get("applied"), Mapping)
            or not row["applied"]
            or not isinstance(row.get("readback"), Mapping)
            or not row["readback"]
        ):
            raise ValueError("direct command ledger content differs from protocol transitions")

    direct_continuous_source = plan.get("execution_authorization", {}).get("schema") in {
        "direct_ray_r6_authority_v1", "direct_ray_history_session_v1",
        "direct_strip_history_session_v1",
    }
    expected_gates: list[tuple[str, str]] = [("run_start", "both_off")]
    for group in groups:
        first = group[0]
        if first["capture_role"] == "ambient":
            expected_gates.append((str(first["isolation_gate_before"]), "both_off"))
        else:
            gate_after = group[-1].get("isolation_gate_after")
            if gate_after:
                expected_gates.append((
                    str(gate_after),
                    "strip_zero_only" if direct_continuous_source else "both_off",
                ))
    gates = _load_jsonl(root / "isolation-gates.jsonl")
    if [(str(row.get("gate_id")), str(row.get("gate_kind"))) for row in gates] != expected_gates:
        raise ValueError("direct isolation gate sequence differs from protocol")
    for row in gates:
        evidence = row.get("evidence")
        if (
            not isinstance(row.get("at"), str)
            or not isinstance(evidence, Mapping)
            or evidence.get("status") != "pass"
            or not (
                evidence.get("strip_verified_off") is True
                or evidence.get("source_verified_zero") is True
            )
        ):
            raise ValueError("direct isolation gate did not prove strip zero")
        if row.get("gate_kind") == "both_off":
            if evidence.get("ray_verified_off") is not True or not isinstance(evidence.get("ray_off_command"), Mapping):
                raise ValueError("direct both-off gate did not prove Ray off")
        elif plan.get("execution_authorization", {}).get("schema") == "direct_strip_history_session_v1":
            if evidence.get("source_verified") != "ray" or evidence.get("ray_verified_off") is not True:
                raise ValueError("direct strip history gate did not prove Ray zero")
        elif evidence.get("ray_off_command") is not None or evidence.get("ray_verified_off") is True:
            raise ValueError("direct Ray history gate contains a Ray-off command")

    if require_audit:
        audit = _load_json(root / "commands-audit.json")
        if (
            audit.get("status") != "pass"
            or audit.get("formal_capture_count") != int(plan["budgets"]["formal_cap"])
            or audit.get("ambient_capture_count") != int(plan["budgets"]["ambient_cap"])
        ):
            raise ValueError("direct command audit differs from protocol budgets")
        if audit.get("derived_after_original_child_failure") is True:
            sources = audit.get("source_artifacts")
            expected_sources = ("commands.jsonl", "isolation-gates.jsonl", "captures.jsonl")
            if (
                not isinstance(sources, Mapping)
                or set(sources) != set(expected_sources)
                or any(sources[name] != _sha256(root / name) for name in expected_sources)
            ):
                raise ValueError("derived direct command audit source hashes drifted")


def _validate_cleanup(root: Path) -> None:
    python_cleanup = _load_json(root / "all-off-python.json")
    python_steps = python_cleanup.get("steps")
    if (
        python_cleanup.get("status") != "pass"
        or not isinstance(python_steps, list)
        or not python_steps
        or not all(isinstance(step, Mapping) and step.get("ok") is True for step in python_steps)
    ):
        raise ValueError("direct Python cleanup artifact did not pass")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if (
        not isinstance(shell_cleanup, list)
        or not shell_cleanup
        or not all(
            isinstance(step, Mapping) and step.get("ok") is True
            for step in shell_cleanup
        )
        or (root / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip()
        != "0"
    ):
        raise ValueError("direct shell cleanup artifact did not pass")


def _validate_cleanup_and_wrapper(
    root: Path, *, post_fix_revalidation: bool = False,
) -> None:
    _validate_cleanup(root)
    wrapper = _load_json(root / "wrapper-result.json")
    if post_fix_revalidation:
        _validate_post_fix_revalidation(root, _load_json(root / "run.json"))
        return
    if (
        wrapper.get("status") != "complete"
        or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("direct wrapper artifact did not prove a clean exit")


def revalidate_direct_ray_r6_exposure_failure(
    run_dir: str | Path,
    *,
    feature_ids: Sequence[str],
    validator_commit: str,
) -> dict[str, Any]:
    """Revalidate one retained 16/16 run stopped by the superseded exposure gate."""

    root = Path(run_dir).resolve()
    if not _is_commit_id(validator_commit):
        raise ValueError("post-fix validator commit must be a 40-character hexadecimal ID")
    revalidation_path = root / POST_FIX_REVALIDATION_FILE
    commands_audit_path = root / "commands-audit.json"
    if revalidation_path.exists() or commands_audit_path.exists():
        raise FileExistsError("post-fix revalidation is one-shot and requires absent derived artifacts")

    plan = _load_json(root / "experiment-spec.json")
    run = _load_json(root / "run.json")
    failure = _load_json(root / "failure.json")
    wrapper = _load_json(root / "wrapper-result.json")
    _validate_legacy_exposure_failure(run, failure, wrapper)
    expected = thermal.build_ray_r6_spec()
    if plan != expected:
        raise ValueError("post-fix revalidation requires the exact direct Ray R6 spec")
    frozen_feature_ids = tuple(
        _feature_ids_from_artifact(thermal.POLICY_PATH)
    )
    if tuple(feature_ids) != frozen_feature_ids:
        raise ValueError("post-fix revalidation requires the frozen feature identity")

    original_hashes = {name: _sha256(root / name) for name in POST_FIX_ORIGINAL_FILES}
    _validate_reproducibility_checkpoint(root, plan, run)
    captures = _load_jsonl(root / "captures.jsonl")
    physical = _load_jsonl(root / "physical-returns.jsonl")
    _validate_run_counts(run, plan, captures, physical)
    _validate_physical_rows(root, captures, physical)
    _validate_commands_and_gates(plan, root, require_audit=False)
    _validate_cleanup(root)

    from camera_based_rgbww_optimizer.optimization import (
        measure_p7_thermal_diagnostics as measure,
    )

    quality_path = root / "quality.json"
    if not quality_path.is_file() or quality_path.is_symlink():
        raise ValueError("post-fix revalidation requires the retained quality artifact")
    quality_hash = _sha256(quality_path)
    quality = measure.validate_direct_ray_r6_post_capture(root, plan, None)
    if _sha256(quality_path) != quality_hash:
        raise ValueError("post-fix revalidation must not rewrite retained quality evidence")
    if quality.get("capture_count") != 16:
        raise ValueError("post-fix revalidation quality count differs from the frozen run")

    commands_audit = {
        "status": "pass",
        "formal_capture_count": int(plan["budgets"]["formal_cap"]),
        "ambient_capture_count": int(plan["budgets"]["ambient_cap"]),
        "derived_after_original_child_failure": True,
        "source_artifacts": {
            name: _sha256(root / name)
            for name in ("commands.jsonl", "isolation-gates.jsonl", "captures.jsonl")
        },
    }
    _write_text_atomic(
        commands_audit_path,
        json.dumps(commands_audit, indent=2, sort_keys=True, allow_nan=False) + "\n",
    )
    try:
        _validate_commands_and_gates(plan, root)
        if any(_sha256(root / name) != digest for name, digest in original_hashes.items()):
            raise ValueError("post-fix revalidation changed original execution evidence")
        evidence = {
            "schema": POST_FIX_REVALIDATION_SCHEMA,
            "status": "pass",
            "reason": "legacy_exact_float_exposure_setting_gate_superseded",
            "run_root": str(root),
            "validator_commit": validator_commit,
            "acquisition_git": dict(run["git"]),
            "original_failure_preserved": True,
            "original_child_exit": int(wrapper["child_exit_code"]),
            "original_artifacts": original_hashes,
            "derived_artifacts": {
                "quality.json": quality_hash,
                "commands-audit.json": _sha256(commands_audit_path),
            },
            "validated": [
                "exact_failure_identity", "reproducibility_checkpoint",
                "capture_and_physical_integrity", "command_and_isolation_sequence",
                "recorded_exposure_setting", "quality", "python_and_shell_cleanup",
            ],
        }
        _write_text_atomic(
            revalidation_path,
            json.dumps(evidence, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        _validate_post_fix_revalidation(root, run)
        return evidence
    except BaseException:
        revalidation_path.unlink(missing_ok=True)
        commands_audit_path.unlink(missing_ok=True)
        raise


def _validate_post_fix_revalidation(
    root: Path, run: Mapping[str, Any],
) -> dict[str, Any]:
    evidence = _load_json(root / POST_FIX_REVALIDATION_FILE)
    failure = _load_json(root / "failure.json")
    wrapper = _load_json(root / "wrapper-result.json")
    _validate_legacy_exposure_failure(run, failure, wrapper)
    if (
        evidence.get("schema") != POST_FIX_REVALIDATION_SCHEMA
        or evidence.get("status") != "pass"
        or evidence.get("reason") != "legacy_exact_float_exposure_setting_gate_superseded"
        or evidence.get("run_root") != str(root)
        or evidence.get("original_failure_preserved") is not True
        or evidence.get("original_child_exit") != 1
        or not _is_commit_id(evidence.get("validator_commit"))
        or evidence.get("acquisition_git") != run.get("git")
    ):
        raise ValueError("post-fix revalidation evidence is invalid")
    originals = evidence.get("original_artifacts")
    derived = evidence.get("derived_artifacts")
    if (
        not isinstance(originals, Mapping)
        or set(originals) != set(POST_FIX_ORIGINAL_FILES)
        or not isinstance(derived, Mapping)
        or set(derived) != {"quality.json", "commands-audit.json"}
    ):
        raise ValueError("post-fix revalidation hashes are missing")
    for name in POST_FIX_ORIGINAL_FILES:
        if originals[name] != _sha256(root / name):
            raise ValueError("post-fix original artifact hash drifted")
    for name in ("quality.json", "commands-audit.json"):
        if derived.get(name) != _sha256(root / name):
            raise ValueError("post-fix derived artifact hash drifted")
    return evidence


def _validate_legacy_exposure_failure(
    run: Mapping[str, Any], failure: Mapping[str, Any], wrapper: Mapping[str, Any],
) -> None:
    if (
        run.get("status") != "failed"
        or run.get("cleanup") != "pass"
        or failure.get("type") != "ValueError"
        or failure.get("message") != LEGACY_EXPOSURE_FAILURE_MESSAGE
        or not isinstance(failure.get("at"), str)
        or wrapper.get("status") != "child_failed"
        or wrapper.get("child_exit_code") != 1
        or wrapper.get("wrapper_exit_code") != 1
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("retained run is not the exact legacy exposure-only failure")


def _sha256(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or unsafe artifact: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_commit_id(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def _replay_timing_evidence(
    capture: Mapping[str, Any], payload: Mapping[str, Any], raw_path: Path, run_root: Path,
) -> tuple[dict[str, Any], str | None]:
    """Replay the retained remote-v2 timing receipt for offline compatibility tools."""
    del capture
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
    anchor_labels = {
        "initial_anchor": "A0",
        "return_after_D": "A_after_D",
        "return_after_B": "A_after_B",
        "return_after_C": "A_after_C",
    }
    anchors: list[tuple[str, np.ndarray]] = []
    for row in captures:
        step = row["plan_step"]
        feature = _features(row, feature_ids)
        if step.get("role") in anchor_labels:
            anchors.append((anchor_labels[str(step["role"])], _unit(feature, feature_ids)))
        else:
            state_points[str(step["state_id"])][int(step["requested_elapsed_s"])].append(feature)
    anchor_pair_diagnostics = []
    for left_index in range(len(anchors)):
        for right_index in range(left_index + 1, len(anchors)):
            left_label, left = anchors[left_index]
            right_label, right = anchors[right_index]
            if compatibility_fn is None:
                diagnostic = frozen_same_state_compatibility_diagnostic(
                    left, right, source=source, state="A", feature_ids=feature_ids,
                )
            else:
                passed = bool(anchor_compatibility(left, right))
                diagnostic = {
                    "statistic": "injected_same_state_compatibility",
                    "decision": "pass" if passed else "fail",
                }
            anchor_pair_diagnostics.append({
                "left": left_label,
                "right": right_label,
                **diagnostic,
            })
    history_pass = (
        [label for label, _ in anchors]
        == ["A0", "A_after_D", "A_after_B", "A_after_C"]
        and len(anchor_pair_diagnostics) == 6
        and all(item["decision"] == "pass" for item in anchor_pair_diagnostics)
    )
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
        chronology = {
            state: _r6_state_chronology_diagnostic(
                points, feature_ids, source=source, state=state,
            )
            for state, points in sorted(state_points.items())
        }
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
            "return_anchor_history_compatibility": {
                "status": "pass" if history_pass else "fail",
                "anchor_order": [label for label, _ in anchors],
                "pair_count": len(anchor_pair_diagnostics),
                "pairwise": anchor_pair_diagnostics,
            },
            "chronology_by_state": chronology,
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
    status = "td_b_pass"
    if not history_pass:
        status = "history_dependent_at_current_protocol"
    elif any(result["t_settle_s"] is None for result in state_results.values()):
        status = "stop_thermal_extension_required"
    return {
        "status": status, "return_anchor_history_effect": "pass" if history_pass else "fail",
        "state_specific_settle_time": {state: result["t_settle_s"] for state, result in state_results.items()},
    }


def analyze_r6_anchor_vectors(
    evidence_dir: str | Path,
    *,
    feature_ids: Sequence[str],
    source_bundle_sha256: str | None = None,
    source_bundle_member: str | None = None,
    analyzer_commit: str | None = None,
) -> dict[str, Any]:
    """Diagnose retained R6 anchor geometry without reclassifying the failed run."""
    root = Path(evidence_dir).resolve()
    analysis = _load_json(root / "analysis.json")
    quality = _load_json(root / "quality.json")
    revalidation = _load_json(root / POST_FIX_REVALIDATION_FILE)
    captures = _load_jsonl(root / "captures.jsonl")
    covariates = _load_jsonl(root / "thermal-covariates.jsonl")
    if (
        analysis.get("status") != "history_dependent_at_operational_dwell_600"
        or analysis.get("formal_pass") is not False
        or analysis.get("return_anchor_history") != "fail"
        or analysis.get("operational_endpoint_600_valid") is not False
    ):
        raise ValueError("R6 vector reanalysis requires the retained history-negative analysis")
    if (
        quality.get("status") != "pass"
        or quality.get("capture_count") != 16
        or revalidation.get("status") != "pass"
        or revalidation.get("original_child_exit") != 1
        or revalidation.get("original_failure_preserved") is not True
    ):
        raise ValueError("R6 vector reanalysis requires accepted quality and preserved revalidation")
    if (
        len(captures) != 16
        or len(covariates) != 16
        or tuple(str(row.get("capture_id")) for row in captures)
        != thermal.TD_B_R6_CAPTURE_IDS
    ):
        raise ValueError("R6 vector reanalysis requires the exact retained 16-frame order")
    anchor_labels = {
        "initial_anchor": "A0",
        "return_after_D": "A_after_D",
        "return_after_B": "A_after_B",
        "return_after_C": "A_after_C",
    }
    anchors: list[dict[str, Any]] = []
    covariate_reconciliations: list[dict[str, Any]] = []
    for index, (row, covariate) in enumerate(zip(captures, covariates)):
        capture = row.get("capture")
        step = row.get("plan_step")
        if not isinstance(capture, Mapping) or not isinstance(step, Mapping):
            raise ValueError("R6 vector reanalysis capture lacks its retained owners")
        embedded_covariate = dict(capture.get("thermal_covariates") or {})
        if set(embedded_covariate) != set(covariate):
            raise ValueError("R6 vector reanalysis covariate key identity drifted")
        differing_covariates = {
            key for key in covariate
            if embedded_covariate.get(key) != covariate.get(key)
        }
        if differing_covariates - {"previous_state_dwell_s"}:
            raise ValueError("R6 vector reanalysis covariate ledger differs outside the corrected dwell field")
        if differing_covariates:
            covariate_reconciliations.append({
                "sequence_index": index,
                "field": "previous_state_dwell_s",
                "embedded_value": embedded_covariate.get("previous_state_dwell_s"),
                "canonical_ledger_value": covariate.get("previous_state_dwell_s"),
            })
        if int(covariate.get("sequence_index", -1)) != index:
            raise ValueError("R6 vector reanalysis covariate chronology drifted")
        role = str(step.get("role"))
        if role not in anchor_labels:
            continue
        values = capture.get("feature_values")
        if not isinstance(values, Mapping) or tuple(values) != tuple(feature_ids):
            raise ValueError("R6 vector reanalysis anchor differs from the frozen feature identity")
        anchors.append({
            "label": anchor_labels[role],
            "capture_id": str(row["capture_id"]),
            "unit_shape": ordered_unit_shape(values, feature_ids),
            "session_elapsed_s": float(covariate["session_elapsed_s"]),
            "source_on_elapsed_s": float(covariate["source_on_elapsed_s"]),
            "previous_state_id": covariate.get("previous_state_id"),
        })
    expected_labels = ["A0", "A_after_D", "A_after_B", "A_after_C"]
    if [str(anchor["label"]) for anchor in anchors] != expected_labels:
        raise ValueError("R6 vector reanalysis requires the exact four retained A anchors")

    pair_variance = _same_state_pair_variance(source="ray", state="A")
    if pair_variance.shape != (len(feature_ids),):
        raise ValueError("R6 common whitening covariance differs from feature identity")
    whitening_scale = np.sqrt(pair_variance)
    whitened = np.vstack([
        np.asarray(anchor["unit_shape"], dtype=float) / whitening_scale
        for anchor in anchors
    ])
    relative_whitened = whitened - whitened[0]
    centered = relative_whitened - np.mean(relative_whitened, axis=0)
    _u, singular_values, vh = np.linalg.svd(centered, full_matrices=False)
    variance_components = singular_values * singular_values
    total_variance = float(np.sum(variance_components))
    if total_variance <= 0.0:
        raise ValueError("R6 anchors do not identify a drift direction")
    explained = variance_components / total_variance
    direction = np.asarray(vh[0], dtype=float)
    if float((whitened[-1] - whitened[0]) @ direction) < 0.0:
        direction = -direction
    anchor_projections = centered @ direction

    step_vectors = np.diff(whitened, axis=0)
    step_pairs = (
        ("A0_to_A_after_D", 0),
        ("A_after_D_to_A_after_B", 1),
        ("A_after_B_to_A_after_C", 2),
    )
    step_diagnostics = [
        {
            "name": name,
            "norm": float(np.linalg.norm(step_vectors[index])),
            "projection_on_r6_drift_direction": float(step_vectors[index] @ direction),
            "orthogonal_residual_norm": float(np.linalg.norm(
                step_vectors[index] - (step_vectors[index] @ direction) * direction
            )),
        }
        for name, index in step_pairs
    ]
    step_cosines = []
    for left in range(len(step_vectors)):
        for right in range(left + 1, len(step_vectors)):
            step_cosines.append({
                "left": step_pairs[left][0],
                "right": step_pairs[right][0],
                "cosine": _vector_cosine(step_vectors[left], step_vectors[right]),
            })

    deltas = whitened - whitened[0]
    anchor_diagnostics = []
    for index, anchor in enumerate(anchors):
        projection = float(deltas[index] @ direction)
        residual = deltas[index] - projection * direction
        anchor_diagnostics.append({
            "label": anchor["label"],
            "capture_id": anchor["capture_id"],
            "previous_state_id": anchor["previous_state_id"],
            "session_elapsed_s": anchor["session_elapsed_s"],
            "source_on_elapsed_s": anchor["source_on_elapsed_s"],
            "projection_on_r6_drift_direction": projection,
            "orthogonal_residual_norm": float(np.linalg.norm(residual)),
        })

    mds = _classical_mds(whitened)
    chronology_relations = {}
    chronology = analysis.get("chronology_by_state")
    if not isinstance(chronology, Mapping) or set(chronology) != {"B", "C", "D"}:
        raise ValueError("R6 vector reanalysis requires complete D/B/C chronology evidence")
    for state in ("D", "B", "C"):
        state_value = chronology[state]
        slope_values = (
            state_value.get("direction", {}).get("slope_by_feature")
            if isinstance(state_value, Mapping) else None
        )
        if not isinstance(slope_values, Mapping) or tuple(slope_values) != tuple(feature_ids):
            raise ValueError("R6 chronology direction differs from frozen feature identity")
        common_whitened_slope = np.asarray(
            [float(slope_values[feature_id]) for feature_id in feature_ids], dtype=float,
        ) / whitening_scale
        chronology_relations[state] = {
            "cosine_with_r6_drift_direction": _vector_cosine(
                direction, common_whitened_slope,
            ),
            "projection_on_r6_drift_direction": float(common_whitened_slope @ direction),
            "orthogonal_residual_norm": float(np.linalg.norm(
                common_whitened_slope
                - (common_whitened_slope @ direction) * direction
            )),
        }

    elapsed = np.asarray([float(anchor["session_elapsed_s"]) for anchor in anchors])
    source_on = np.asarray([float(anchor["source_on_elapsed_s"]) for anchor in anchors])
    monotonic_projection = bool(np.all(np.diff(anchor_projections) > 0.0))
    pc1_dominates_remainder = bool(float(explained[0]) > float(np.sum(explained[1:])))
    support = pc1_dominates_remainder and monotonic_projection
    return {
        "schema": R6_VECTOR_REANALYSIS_SCHEMA,
        "status": (
            "rank1_drift_hypothesis_supported"
            if support else "rank1_drift_hypothesis_unsupported"
        ),
        "scientific_interpretation": {
            "history_dependence_observed": True,
            "history_origin": "not_identifiable_between_cumulative_period_effect_and_predecessor_carryover",
            "preferred_working_hypothesis": "approximately_rank1_cumulative_source_age_or_session_time_drift",
            "c_specific_carryover": "unproven",
            "causal_confounding_resolved": False,
            "r6_formal_pass": False,
            "r6_reclassification_allowed": False,
            "r6_use_for_new_experiment": "hypothesis_generation_and_frozen_drift_direction_only",
            "strip_combined_td_c": "locked",
        },
        "input_identity": {
            "evidence_dir": str(root),
            "evidence_dir_is_authority": source_bundle_sha256 is None,
            "source_bundle_sha256": source_bundle_sha256,
            "source_bundle_member": source_bundle_member,
            "analyzer_commit": analyzer_commit,
            "feature_ids_sha256": hashlib.sha256(
                ("\n".join(feature_ids) + "\n").encode("utf-8")
            ).hexdigest(),
            "artifacts": {
                name: _sha256(root / name)
                for name in (
                    "analysis.json", "captures.jsonl", "thermal-covariates.jsonl",
                    "quality.json", POST_FIX_REVALIDATION_FILE,
                )
            },
        },
        "covariate_reconciliation": {
            "canonical_owner": "thermal-covariates.jsonl",
            "allowed_differing_field": "previous_state_dwell_s",
            "difference_count": len(covariate_reconciliations),
            "differences": covariate_reconciliations,
            "all_other_fields_exact": True,
        },
        "common_whitening": {
            "space": "ordered_58_feature_unit_shape",
            "covariance": "two_times_frozen_ray_within_state_diagonal_variance",
            "feature_ids": list(feature_ids),
            "diagonal_variance": pair_variance.tolist(),
        },
        "difference_vector_cosines": step_cosines,
        "step_vectors": step_diagnostics,
        "pca": {
            "rank": int(np.linalg.matrix_rank(centered)),
            "singular_values": singular_values.tolist(),
            "explained_variance_ratio": explained.tolist(),
            "pc1_dominates_remainder": pc1_dominates_remainder,
        },
        "classical_mds": mds,
        "r6_drift_direction": {
            "orientation": "A0_toward_A_after_C_positive",
            "values_by_feature": {
                feature_id: float(direction[index])
                for index, feature_id in enumerate(feature_ids)
            },
            "sha256": hashlib.sha256(
                np.asarray(direction, dtype="<f8").tobytes()
            ).hexdigest(),
            "source": "R6_hypothesis_generation_only_frozen_before_new_experiment",
        },
        "anchor_projections": anchor_diagnostics,
        "time_relations": {
            "session_elapsed_s": _linear_relation(elapsed, anchor_projections),
            "source_on_elapsed_s": _linear_relation(source_on, anchor_projections),
            "sample_count": 4,
            "causal_claim_allowed": False,
        },
        "chronology_direction_relations": chronology_relations,
        "support_rule": {
            "kind": "diagnostic_non_gating_structural_rule",
            "pc1_dominates_sum_of_remaining_components": pc1_dominates_remainder,
            "anchor_projection_strictly_monotonic_in_observed_order": monotonic_projection,
            "measurement_threshold_changed": False,
        },
    }


def _vector_cosine(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = np.asarray(left, dtype=float)
    right_values = np.asarray(right, dtype=float)
    denominator = float(np.linalg.norm(left_values) * np.linalg.norm(right_values))
    if denominator <= 0.0:
        raise ValueError("R6 vector cosine requires nonzero vectors")
    return float((left_values @ right_values) / denominator)


def _linear_relation(x: Sequence[float], y: Sequence[float]) -> dict[str, float]:
    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    design = np.column_stack((np.ones(len(x_values)), x_values))
    coefficients, *_ = np.linalg.lstsq(design, y_values, rcond=None)
    fitted = design @ coefficients
    residual = y_values - fitted
    total = float(np.sum((y_values - np.mean(y_values)) ** 2))
    return {
        "intercept": float(coefficients[0]),
        "slope_per_second": float(coefficients[1]),
        "pearson_correlation": float(np.corrcoef(x_values, y_values)[0, 1]),
        "r_squared": 1.0 if total <= 0.0 else float(1.0 - np.sum(residual * residual) / total),
    }


def _classical_mds(values: np.ndarray) -> dict[str, Any]:
    count = len(values)
    squared_distances = np.sum(
        (values[:, None, :] - values[None, :, :]) ** 2, axis=2,
    )
    centering = np.eye(count) - np.ones((count, count)) / count
    gram = -0.5 * centering @ squared_distances @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    tolerance = max(float(eigenvalues[0]), 1.0) * np.finfo(float).eps * count
    positive = eigenvalues > tolerance
    positive_values = eigenvalues[positive]
    coordinates = eigenvectors[:, positive] * np.sqrt(positive_values)
    if coordinates.size and coordinates[-1, 0] < coordinates[0, 0]:
        coordinates[:, 0] *= -1.0
    return {
        "rank": int(np.sum(positive)),
        "eigenvalues": eigenvalues.tolist(),
        "positive_explained_variance_ratio": (
            [] if not len(positive_values)
            else (positive_values / np.sum(positive_values)).tolist()
        ),
        "coordinates": coordinates.tolist(),
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


def _same_state_variance(*, source: str, state: str) -> np.ndarray:
    policy = _load_json(thermal.POLICY_PATH)
    if source == "ray":
        variance = np.asarray(
            policy["reference_policy"]["ray_within_state_diagonal_variance"],
            dtype=float,
        )
    else:
        class_name = {
            "A": "sat100_fullscale", "D": "mid_sat_fullscale",
            "B": "neutral_fullscale", "C": "sat100_fullscale",
        }[state]
        variance = np.asarray(
            policy["repeatability_policy"]["classes"][class_name]["p1_floor_diagonal_variance"],
            dtype=float,
        )
    return variance


def _same_state_pair_variance(*, source: str, state: str) -> np.ndarray:
    return 2.0 * _same_state_variance(source=source, state=state)


def frozen_same_state_compatibility_diagnostic(
    left: Sequence[float], right: Sequence[float], *,
    source: str, state: str, feature_ids: Sequence[str],
) -> dict[str, Any]:
    pair_variance = _same_state_pair_variance(source=source, state=state)
    if pair_variance.shape != (len(feature_ids),):
        raise ValueError("frozen same-state covariance differs from feature contract")
    left_values = np.asarray(left, dtype=float)
    right_values = np.asarray(right, dtype=float)
    limits = calibrate_direct_limits(left_values, pair_variance, samples=1000)
    score = direct_whitened_norm(right_values - left_values, pair_variance)
    passed = score <= float(limits["guarded_limit"])
    return {
        "statistic": str(limits["statistic"]),
        "score": score,
        "guarded_limit": float(limits["guarded_limit"]),
        "unguarded_limit": float(limits["unguarded_limit"]),
        "decision": "pass" if passed else "fail",
    }


def _r6_state_chronology_diagnostic(
    points: Mapping[int, Sequence[Mapping[str, float]]],
    feature_ids: Sequence[str],
    *, source: str, state: str,
) -> dict[str, Any]:
    expected_points = tuple(thermal.TIMED_POINTS)
    if tuple(sorted(points)) != expected_points or any(len(points[point]) != 1 for point in expected_points):
        raise ValueError("Ray R6 chronology requires one 60/120/300/600 capture per switched state")
    ordered_features = [points[point][0] for point in expected_points]
    normalized = np.vstack([_unit(features, feature_ids) for features in ordered_features])
    chronology_axis = np.linspace(-0.5, 0.5, len(normalized))
    centered = normalized - np.mean(normalized, axis=0)
    slope = (chronology_axis @ centered) / float(chronology_axis @ chronology_axis)
    dominant_index = int(np.argmax(np.abs(slope)))
    variance = _same_state_variance(source=source, state=state)
    if variance.shape != (len(feature_ids),):
        raise ValueError("frozen chronology covariance differs from feature contract")
    trend_score = direct_whitened_norm(slope, variance)
    energy = np.sum(centered * centered / variance, axis=1)
    total_energy = float(np.sum(energy))
    dominance = (
        0.0 if total_energy <= 0.0
        else float(np.max(energy) / total_energy)
    )
    trend_limit = float(thermal.AUDIT_THRESHOLDS["trend_whitened_limit"])
    dominance_limit = float(
        thermal.AUDIT_THRESHOLDS["maximum_single_frame_variance_fraction"]
    )
    return {
        "elapsed_s": list(expected_points),
        "normalized_feature_values": [
            {feature_id: float(row[index]) for index, feature_id in enumerate(feature_ids)}
            for row in normalized
        ],
        "trend": {
            "score": trend_score,
            "limit": trend_limit,
            "decision": "pass" if trend_score <= trend_limit else "fail",
            "hard_gate_for_operational_600": False,
        },
        "dominance": {
            "maximum_single_frame_variance_fraction": dominance,
            "limit": dominance_limit,
            "decision": "pass" if dominance <= dominance_limit else "fail",
            "hard_gate_for_operational_600": False,
        },
        "direction": {
            "semantics": "least_squares_slope_over_ordered_60_120_300_600_unit_shapes",
            "slope_by_feature": {
                feature_id: float(slope[index])
                for index, feature_id in enumerate(feature_ids)
            },
            "dominant_feature_id": str(feature_ids[dominant_index]),
            "dominant_signed_slope": float(slope[dominant_index]),
            "l2": float(np.linalg.norm(slope)),
        },
        "audit_status": (
            "pass"
            if trend_score <= trend_limit and dominance <= dominance_limit
            else "scientific_chronology_signal_present"
        ),
        "covariance": "frozen_same_state_per_capture_diagonal_variance",
    }


def frozen_same_state_compatibility(
    *, source: str, feature_ids: Sequence[str], state: str = "A",
) -> Callable[[Sequence[float], Sequence[float]], bool]:
    def compatible(left: Sequence[float], right: Sequence[float]) -> bool:
        diagnostic = frozen_same_state_compatibility_diagnostic(
            left, right, source=source, state=state, feature_ids=feature_ids,
        )
        return diagnostic["decision"] == "pass"

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


def _feature_ids_from_artifact(path: Path) -> list[str]:
    artifact = _load_json(path)
    ids = artifact.get("feature_set", {}).get("ids") or artifact.get("ids")
    if not isinstance(ids, list) or not ids or any(not isinstance(item, str) or not item for item in ids):
        raise ValueError("thermal feature file lacks a non-empty string ID list")
    return ids


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


def _guarded_zero_diagnostic(
    value: np.ndarray, variance: np.ndarray, *, center: np.ndarray,
) -> dict[str, Any]:
    if value.shape != variance.shape or np.any(variance <= 0.0):
        raise ValueError("Ray history contrast covariance differs from the feature contract")
    limits = calibrate_direct_limits(center, variance, samples=1000)
    score = direct_whitened_norm(value, variance)
    limit = float(limits["guarded_limit"])
    return {
        "score": score, "guarded_limit": limit,
        "decision": "detected" if score > limit else "compatible_with_zero",
    }


def analyze_ray_history_experiment(
    experiment_root: str | Path,
    *,
    feature_ids: Sequence[str],
    r6_vector_artifact: str | Path | None,
    source: str = "ray",
) -> dict[str, Any]:
    """Classify one frozen 3x3 history experiment without pooling R6 frames."""
    root = Path(experiment_root).resolve()
    ids = tuple(feature_ids)
    frozen_ids = tuple(_feature_ids_from_artifact(thermal.POLICY_PATH))
    if ids != frozen_ids:
        raise ValueError("history analysis requires the frozen 58-feature identity")
    if source not in {"ray", "strip"}:
        raise ValueError("history analysis source must be ray or strip")
    drift_path: Path | None = None
    drift_artifact: Mapping[str, Any] = {}
    if source == "ray":
        if r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires the frozen R6 direction artifact")
        drift_path = Path(r6_vector_artifact).resolve()
        drift_artifact = _load_json(drift_path)
        direction_map = drift_artifact.get("r6_drift_direction", {}).get("values_by_feature")
        whitening = drift_artifact.get("common_whitening", {})
        if (
            drift_artifact.get("scientific_interpretation", {}).get("r6_formal_pass") is not False
            or drift_artifact.get("scientific_interpretation", {}).get("r6_reclassification_allowed") is not False
            or not isinstance(direction_map, Mapping)
            or tuple(direction_map) != ids
            or tuple(whitening.get("feature_ids", ())) != ids
        ):
            raise ValueError("Ray history analysis requires the frozen negative-R6 direction artifact")
        direction = np.asarray([direction_map[name] for name in ids], dtype=float)
        if not np.all(np.isfinite(direction)) or not math.isclose(
            float(np.linalg.norm(direction)), 1.0, rel_tol=1e-8, abs_tol=1e-8,
        ):
            raise ValueError("frozen R6 drift direction is not a finite unit vector")
        pair_variance = np.asarray(whitening.get("diagonal_variance"), dtype=float)
    else:
        direction = np.zeros(len(ids), dtype=float)
        pair_variance = _same_state_pair_variance(source="strip", state="A")
    expected_pair_variance = _same_state_pair_variance(source=source, state="A")
    if pair_variance.shape != (len(ids),) or not np.allclose(
        pair_variance, expected_pair_variance, rtol=0.0, atol=0.0,
    ):
        raise ValueError("history common whitening differs from the frozen source covariance")

    observations: list[dict[str, Any]] = []
    baseline_centers: list[np.ndarray] = []
    session_artifacts: list[dict[str, Any]] = []
    for session_index in (1, 2, 3):
        session_root = root / f"session-{session_index}"
        plan = _load_json(session_root / "experiment-spec.json")
        run = _load_json(session_root / "run.json")
        builder = (
            thermal.build_ray_history_session_spec
            if source == "ray" else thermal.build_strip_history_session_spec
        )
        expected = builder(
            session_index, device_control_enabled=True,
            session_start_condition=plan.get("session_start_condition"),
        )
        if plan != expected:
            raise ValueError("Ray history session differs from its exact cyclic design")
        _validate_required_execution_artifacts(session_root)
        _validate_reproducibility_checkpoint(session_root, plan, run)
        captures = _load_jsonl(session_root / "captures.jsonl")
        physical = _load_jsonl(session_root / "physical-returns.jsonl")
        _validate_run_counts(run, plan, captures, physical)
        _validate_physical_rows(session_root, captures, physical)
        _validate_commands_and_gates(plan, session_root)
        _validate_cleanup_and_wrapper(session_root)
        quality = _load_json(session_root / "quality.json")
        if (
            quality.get("schema") not in {
                "guide4_ray_history_session_quality_v1",
                "guide5_strip_history_session_quality_v1",
            }
            or quality.get("status") != "pass"
            or quality.get("session_index") != session_index
            or quality.get("capture_count") != 7
        ):
            raise ValueError("Ray history session quality artifact did not pass")
        by_role: dict[str, Mapping[str, Any]] = {}
        for row, expected_step in zip(captures, expected["captures"], strict=True):
            capture = row.get("capture")
            step = row.get("plan_step")
            if (
                not isinstance(capture, Mapping)
                or not isinstance(step, Mapping)
                or dict(step) != dict(expected_step)
                or str(row.get("capture_id")) != expected_step["capture_id"]
            ):
                raise ValueError("Ray history capture differs from its exact session spec")
            values = capture.get("feature_values")
            if (
                not isinstance(values, Mapping)
                or tuple(values) != ids
                or any(
                    isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(float(value)) for value in values.values()
                )
            ):
                raise ValueError("Ray history capture lacks the frozen feature vector")
            direct_quality = capture.get("direct_quality")
            if (
                not isinstance(direct_quality, Mapping)
                or direct_quality.get("status") != "pass"
                or direct_quality.get("feature_count") != len(ids)
            ):
                raise ValueError("Ray history capture quality did not pass")
            _validate_recorded_exposure(capture, str(expected_step["nominal_shutter"]))
            if source == "ray":
                strip_zero = capture.get("strip_zero_before_capture")
                requested_zero = (
                    strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
                )
                observed_zero = (
                    strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
                )
                if (
                    not isinstance(requested_zero, Mapping)
                    or any(int(value) != 0 for value in requested_zero.values())
                    or not isinstance(observed_zero, Mapping)
                    or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
                ):
                    raise ValueError("Ray history capture lacks verified strip-zero evidence")
            else:
                ray_zero = capture.get("ray_zero_before_capture")
                if not isinstance(ray_zero, Mapping):
                    raise ValueError("strip history capture lacks verified Ray-zero evidence")
            if expected_step["role"] in {"initial_anchor", "return_anchor"}:
                by_role[str(expected_step["anchor_label"])] = values
        baseline = _unit(by_role["A0"], ids)
        baseline_centers.append(baseline)
        for position, predecessor in enumerate(expected["session_order"], start=1):
            label = f"A_after_{predecessor}"
            delta = _unit(by_role[label], ids) - baseline
            whitened_delta = delta / np.sqrt(pair_variance)
            projection = float(whitened_delta @ direction)
            orthogonal = whitened_delta - projection * direction
            observations.append({
                "session": session_index, "position": position,
                "predecessor": predecessor, "delta": delta,
                "whitened_delta": whitened_delta,
                "projection": projection,
                "orthogonal_norm": float(np.linalg.norm(orthogonal)),
            })
        session_artifacts.append({
            "session": session_index, "root": str(session_root),
            "order": expected["session_order"], "quality_sha256": _sha256(session_root / "quality.json"),
        })

    # Treatment coding: intercept, session 2/3, position 2/3, predecessor B/C.
    design = np.asarray([
        [
            1.0,
            float(row["session"] == 2), float(row["session"] == 3),
            float(row["position"] == 2), float(row["position"] == 3),
            float(row["predecessor"] == "B"), float(row["predecessor"] == "C"),
        ]
        for row in observations
    ])
    response = np.vstack([row["delta"] for row in observations])
    calibration_center = np.mean(np.vstack(baseline_centers), axis=0)
    response_covariance = np.eye(9)
    for left in range(9):
        for right in range(9):
            if left != right and observations[left]["session"] == observations[right]["session"]:
                response_covariance[left, right] = 0.5
    covariance_inverse = np.linalg.inv(response_covariance)
    information = design.T @ covariance_inverse @ design
    coefficient_covariance = np.linalg.inv(information)
    coefficients = coefficient_covariance @ design.T @ covariance_inverse @ response
    fitted = design @ coefficients
    residuals = response - fitted

    def contrast(name: str, vector: Sequence[float]) -> dict[str, Any]:
        row = np.asarray(vector, dtype=float)
        effect = row @ coefficients
        variance_scalar = float(row @ coefficient_covariance @ row)
        diagnostic = _guarded_zero_diagnostic(
            effect, variance_scalar * pair_variance, center=calibration_center,
        )
        return {
            "name": name,
            "projection_on_r6_direction": float(
                (effect / np.sqrt(pair_variance)) @ direction
            ),
            "variance_scalar_relative_to_one_delta": variance_scalar,
            **diagnostic,
        }

    contrasts = {
        "common_warm_reentry_effect": contrast(
            "common_warm_reentry_effect", (1, 0, 0, 0, 0, 0, 0),
        ),
        "position_2_minus_1": contrast("position_2_minus_1", (0, 0, 0, 1, 0, 0, 0)),
        "position_3_minus_2": contrast("position_3_minus_2", (0, 0, 0, -1, 1, 0, 0)),
        "C_minus_D": contrast("C_minus_D", (0, 0, 0, 0, 0, 0, 1)),
        "C_minus_B": contrast("C_minus_B", (0, 0, 0, 0, 0, -1, 1)),
        "B_minus_D": contrast("B_minus_D", (0, 0, 0, 0, 0, 1, 0)),
    }
    position_projections = [
        0.0,
        float((coefficients[3] / np.sqrt(pair_variance)) @ direction),
        float((coefficients[4] / np.sqrt(pair_variance)) @ direction),
    ]
    period_detected = (
        position_projections[0] < position_projections[1] < position_projections[2]
        and all(
            contrasts[name]["decision"] == "detected"
            for name in ("position_2_minus_1", "position_3_minus_2")
        )
    )
    c_detected = all(
        contrasts[name]["decision"] == "detected"
        for name in ("C_minus_D", "C_minus_B")
    )
    other_state_effect = contrasts["B_minus_D"]["decision"] == "detected"
    orthogonal_large = any(
        _guarded_zero_diagnostic(
            (row["whitened_delta"] - row["projection"] * direction)
            * np.sqrt(pair_variance),
            pair_variance,
            center=calibration_center,
        )["decision"] == "detected"
        for row in observations
    )
    residual_large = False
    residual_rows = []
    residual_maker = np.eye(9) - design @ coefficient_covariance @ design.T @ covariance_inverse
    residual_covariance = residual_maker @ response_covariance @ residual_maker.T
    for index, residual in enumerate(residuals):
        variance_scalar = max(float(residual_covariance[index, index]), 1e-15)
        diagnostic = _guarded_zero_diagnostic(
            residual, variance_scalar * pair_variance, center=calibration_center,
        )
        residual_large |= diagnostic["decision"] == "detected"
        residual_rows.append({
            "session": observations[index]["session"],
            "position": observations[index]["position"],
            "predecessor": observations[index]["predecessor"],
            **diagnostic,
        })
    return_compatible = all(
        _guarded_zero_diagnostic(
            row["delta"], pair_variance, center=calibration_center,
        )["decision"]
        == "compatible_with_zero"
        for row in observations
    )
    nonlinear = residual_large or orthogonal_large or other_state_effect
    if nonlinear:
        classification = "nonlinear/non-additive"
    elif period_detected and c_detected:
        classification = "mixed"
    elif period_detected:
        classification = "period-only"
    elif c_detected:
        classification = "C-carryover-only"
    elif return_compatible:
        classification = "R6-not-reproduced"
    else:
        classification = "nonlinear/non-additive"
    return {
        "schema": "guide4_ray_history_order_balanced_analysis_v1",
        "status": "classified_waiting_advisor_review",
        "experiment_id": (
            thermal.RAY_HISTORY_3X3_EXPERIMENT_ID
            if source == "ray" else thermal.STRIP_HISTORY_3X3_EXPERIMENT_ID
        ),
        "classification": classification,
        "r6_formal_result_preserved": "valid_scientific_negative",
        "r6_frames_pooled": False,
        "frozen_r6_direction": (
            {
                "artifact": str(drift_path), "sha256": _sha256(drift_path),
                "direction_sha256": drift_artifact["r6_drift_direction"]["sha256"],
            }
            if source == "ray" else None
        ),
        "measurement_contract": {
            "feature_count": len(ids), "observer": "frozen",
            "operational_dwell_s": thermal.RAY_HISTORY_OPERATIONAL_DWELL_S,
            "thermal_error": "human_accepted_to_reduce_time_and_power",
            "steady_or_settled_claim": False,
            "covariance": "frozen_ray_within_state_diagonal_with_shared_A0_block_covariance",
            "guarded_coverage": "frozen_direct_limits",
        },
        "sessions": session_artifacts,
        "model": {
            "formula": "return_anchor_delta = session + sequence_position + immediate_predecessor_state + residual",
            "observation_count": 9, "parameter_count": 7, "residual_degrees_of_freedom": 2,
            "position_projections_on_r6_direction": position_projections,
            "contrasts": contrasts, "residuals": residual_rows,
        },
        "diagnostics": {
            "period_detected": period_detected, "C_carryover_detected": c_detected,
            "other_state_effect_detected": other_state_effect,
            "large_orthogonal_residual": orthogonal_large,
            "orthogonal_to_frozen_r6_direction_detected": orthogonal_large,
            "additive_model_rejected": residual_large,
            "all_return_deltas_compatible_with_zero": return_compatible,
        },
        "locks": {
            "strip": True, "combined_td_b": True, "td_c": True,
            "sentinel_and_later": True, "until": "classification_review_complete",
        },
    }


def analyze_ray_history_experiment_v2(
    experiment_root: str | Path,
    *, feature_ids: Sequence[str], r6_vector_artifact: str | Path | None,
    source: str = "ray",
) -> dict[str, Any]:
    """Derive the Advisor-5 common-reentry classification without changing v1 evidence."""
    legacy = analyze_ray_history_experiment(
        experiment_root, feature_ids=feature_ids,
        r6_vector_artifact=r6_vector_artifact,
        source=source,
    )
    diagnostics = legacy["diagnostics"]
    contrasts = legacy["model"]["contrasts"]
    additive_residual = bool(diagnostics["additive_model_rejected"])
    period = bool(diagnostics["period_detected"])
    predecessor = bool(
        diagnostics["C_carryover_detected"]
        or diagnostics["other_state_effect_detected"]
    )
    common = contrasts["common_warm_reentry_effect"]["decision"] == "detected"
    raw_compatible = bool(diagnostics["all_return_deltas_compatible_with_zero"])
    if additive_residual:
        classification = "interaction_or_nonadditive_unresolved"
    elif common and not period and not predecessor:
        classification = "common_warm_reentry_shift"
    elif period or predecessor:
        classification = "additive_period_or_carryover_effect"
    elif raw_compatible:
        classification = "no_history_effect_detected"
    else:
        classification = "underpowered_or_unclassified"
    original = Path(experiment_root).resolve() / "analysis.json"
    return {
        "schema": "guide4_ray_history_order_balanced_analysis_v2",
        "status": "classified_waiting_advisor_review",
        "experiment_id": legacy["experiment_id"],
        "legacy_classification": legacy["classification"],
        "classification": classification,
        "r6_rank1_direction_transfer": "rejected" if source == "ray" else "not_applicable",
        "r6_frames_pooled": False,
        "original_analysis_sha256": _sha256(original) if original.is_file() else None,
        "frozen_r6_direction": legacy["frozen_r6_direction"],
        "measurement_contract": legacy["measurement_contract"],
        "sessions": legacy["sessions"],
        "model": legacy["model"],
        "diagnostics": {
            "common_warm_reentry_detected": common,
            "period_main_effect_detected": period,
            "predecessor_main_effect_detected": predecessor,
            "additive_model_rejected": additive_residual,
            "nonlinear_interaction_demonstrated": additive_residual,
            "raw_return_deltas_compatible_with_zero": raw_compatible,
            "orthogonal_to_frozen_r6_direction_detected": bool(
                diagnostics["orthogonal_to_frozen_r6_direction_detected"]
            ),
        },
        "locks": {
            "strip_history_only": classification != "common_warm_reentry_shift",
            "combined_td_b": True, "td_c": True,
            "sentinel_and_later": True,
            "until": "advisor_review_complete",
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze P7 thermal diagnostics or derive P7-R1 epoch-v2 evidence.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--feature-ids", type=Path)
    parser.add_argument("--derive-r1-output", type=Path)
    parser.add_argument("--revalidate-exposure-failure", action="store_true")
    parser.add_argument("--validator-commit")
    parser.add_argument("--r6-vector-reanalysis-output", type=Path)
    parser.add_argument("--source-bundle-sha256")
    parser.add_argument("--source-bundle-member")
    parser.add_argument("--analyzer-commit")
    parser.add_argument("--ray-history-analysis", action="store_true")
    parser.add_argument("--ray-history-analysis-v2", action="store_true")
    parser.add_argument("--ray-history-analysis-output", type=Path)
    parser.add_argument("--history-source", choices=("ray", "strip"), default="ray")
    parser.add_argument("--r6-vector-artifact", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.derive_r1_output is not None:
        paths = write_reference_epoch_v2_derived(args.run_dir, args.derive_r1_output)
        print("\n".join(str(path) for path in paths))
        return 0
    if args.feature_ids is None:
        raise ValueError("--feature-ids is required for thermal run analysis")
    feature_ids = _feature_ids_from_artifact(args.feature_ids)
    if args.ray_history_analysis_v2:
        if args.history_source == "ray" and args.r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires --r6-vector-artifact")
        if args.ray_history_analysis:
            raise ValueError("v1 and v2 Ray history analysis are mutually exclusive")
        output = args.ray_history_analysis_output
        if output is None:
            raise ValueError("v2 Ray history analysis requires --ray-history-analysis-output")
        report = analyze_ray_history_experiment_v2(
            args.run_dir, feature_ids=feature_ids,
            r6_vector_artifact=args.r6_vector_artifact,
            source=args.history_source,
        )
        _write_text_atomic(
            output.resolve(), json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output.resolve())
        return 0
    if args.ray_history_analysis:
        if args.r6_vector_artifact is None:
            raise ValueError("Ray history analysis requires --r6-vector-artifact")
        report = analyze_ray_history_experiment(
            args.run_dir, feature_ids=feature_ids,
            r6_vector_artifact=args.r6_vector_artifact,
        )
        output = args.run_dir.resolve() / "analysis.json"
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if args.r6_vector_artifact is not None:
        raise ValueError("--r6-vector-artifact requires --ray-history-analysis")
    if args.r6_vector_reanalysis_output is not None:
        if args.revalidate_exposure_failure or args.validator_commit is not None:
            raise ValueError("R6 vector reanalysis does not rerun exposure revalidation")
        if (
            args.analyzer_commit is None
            or len(args.analyzer_commit) != 40
            or any(character not in "0123456789abcdef" for character in args.analyzer_commit)
        ):
            raise ValueError("R6 vector reanalysis requires an exact analyzer commit")
        report = analyze_r6_anchor_vectors(
            args.run_dir,
            feature_ids=feature_ids,
            source_bundle_sha256=args.source_bundle_sha256,
            source_bundle_member=args.source_bundle_member,
            analyzer_commit=args.analyzer_commit,
        )
        output = args.r6_vector_reanalysis_output.resolve()
        _write_text_atomic(
            output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        )
        print(output)
        return 0
    if (
        args.source_bundle_sha256 is not None
        or args.source_bundle_member is not None
        or args.analyzer_commit is not None
    ):
        raise ValueError("source bundle identity requires --r6-vector-reanalysis-output")
    if args.revalidate_exposure_failure:
        if args.validator_commit is None:
            raise ValueError("--validator-commit is required for post-fix revalidation")
        revalidation_path = args.run_dir.resolve() / POST_FIX_REVALIDATION_FILE
        if revalidation_path.exists():
            retained = _validate_post_fix_revalidation(
                args.run_dir.resolve(), _load_json(args.run_dir.resolve() / "run.json"),
            )
            if retained.get("validator_commit") != args.validator_commit:
                raise ValueError("retained revalidation belongs to a different validator commit")
        else:
            revalidate_direct_ray_r6_exposure_failure(
                args.run_dir,
                feature_ids=feature_ids,
                validator_commit=args.validator_commit,
            )
    elif args.validator_commit is not None:
        raise ValueError("--validator-commit requires --revalidate-exposure-failure")
    report = analyze_thermal_run(
        args.run_dir,
        feature_ids=feature_ids,
        post_fix_revalidation=args.revalidate_exposure_failure,
    )
    output = args.run_dir / "analysis.json"
    _write_text_atomic(output, json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
