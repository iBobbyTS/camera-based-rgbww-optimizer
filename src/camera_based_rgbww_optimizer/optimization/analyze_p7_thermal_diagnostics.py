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

    direct_r6 = plan.get("execution_authorization", {}).get("schema") == "direct_ray_r6_authority_v1"
    expected_gates: list[tuple[str, str]] = [("run_start", "both_off")]
    for group in groups:
        first = group[0]
        if first["capture_role"] == "ambient":
            expected_gates.append((str(first["isolation_gate_before"]), "both_off"))
        else:
            gate_after = group[-1].get("isolation_gate_after")
            if gate_after:
                expected_gates.append((str(gate_after), "strip_zero_only" if direct_r6 else "both_off"))
    gates = _load_jsonl(root / "isolation-gates.jsonl")
    if [(str(row.get("gate_id")), str(row.get("gate_kind"))) for row in gates] != expected_gates:
        raise ValueError("direct isolation gate sequence differs from protocol")
    for row in gates:
        evidence = row.get("evidence")
        if (
            not isinstance(row.get("at"), str)
            or not isinstance(evidence, Mapping)
            or evidence.get("status") != "pass"
            or evidence.get("strip_verified_off") is not True
        ):
            raise ValueError("direct isolation gate did not prove strip zero")
        if row.get("gate_kind") == "both_off":
            if evidence.get("ray_verified_off") is not True or not isinstance(evidence.get("ray_off_command"), Mapping):
                raise ValueError("direct both-off gate did not prove Ray off")
        elif (
            evidence.get("ray_off_command") is not None
            or evidence.get("ray_verified_off") is True
        ):
            raise ValueError("direct strip-only gate contains a Ray-off command")

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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze P7 thermal diagnostics or derive P7-R1 epoch-v2 evidence.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--feature-ids", type=Path)
    parser.add_argument("--derive-r1-output", type=Path)
    parser.add_argument("--revalidate-exposure-failure", action="store_true")
    parser.add_argument("--validator-commit")
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
