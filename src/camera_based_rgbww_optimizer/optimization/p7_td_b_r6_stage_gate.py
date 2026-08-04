"""Offline, non-authorizing stage gate for the future Ray TD-B formal R6 run.

This module owns only the G4-05 launch shape and its provenance package.  The
scientific plan remains owned by :mod:`p7_thermal_diagnostics`; device and
capture execution remain owned by :mod:`measure_p7_thermal_diagnostics`.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils.agent_work_machine_contract import (
    parse_full_plan_machine_state,
    parse_plan_machine_contract,
)
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


STAGE_GATE_SCHEMA = "p7_td_b_r6_stage_gate_v1"
LAUNCH_DESCRIPTOR_SCHEMA = "p7_td_b_r6_launch_descriptor_v1"
TERMINAL_SEAL_SCHEMA = "p7_td_b_r6_stage_gate_terminal_seal_v1"
INPUT_SCHEMA = "p7_td_b_r6_stage_gate_input_v1"
TASK_ID = "REF-G4-05-RAY-R6-STAGE-GATE"
CONTRACT_ID = "G4-RAY-R6-STAGE-GATE-OFFLINE-V1"
FUTURE_TASK_ID = "REF-G4-06-RAY-R6"
ENGINEERING_PACKAGE_A_CONTRACT_ID = (
    "G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V2"
)
FORMAL_PACKAGE_B_CONTRACT_ID = "G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1"
PASS_STATUS = "sealed_offline_ray_r6_stage_gate_pass_waiting_planner_review"
FAIL_STATUS = "sealed_offline_ray_r6_stage_gate_fail_waiting_planner_review"
RETAINED_R3_STATUS = "RETAINED_UNVALIDATED_UNCONSUMED"
EXPECTED_ARTIFACTS = (
    "launch-descriptor.json",
    "stage-gate.json",
    "terminal-seal.json",
)
PRE_TERMINAL_ARTIFACTS = ("launch-descriptor.json", "stage-gate.json")
EXPECTED_SOURCE_PATHS = (
    ".agent-work/FULL_PLAN_REFERENCE.md",
    ".agent-work/PLAN.md",
    "advisor/4/4.GUIDE.md",
    "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",
    "tests/test_p7_td_b_r6_stage_gate.py",
    "tests/test_p7_thermal_diagnostics.py",
    "tmp/run-p7-thermal-diagnostics.zsh",
)
FORMAL_ROOT_PARENT = "/Volumes/4T/temp/rgbww-optimizer"
FORMAL_ROOT_BASENAME_REGEX = (
    r"^p7-td-b-formal-r6-[0-9a-f]{12}-[0-9]{8}T[0-9]{6}Z$"
)
RUNTIME_TEMPLATE_STATUS = "waiting_g4_06_plan_non_authorizing"
TEMPLATE_AUTHORITY_SCHEMA = "p7_td_b_r6_runtime_template_authority_v1"
PLAN_BOUND_AUTHORITY_SCHEMA = "p7_td_b_r6_plan_bound_authority_v1"
FUTURE_ACTIVATION_SCHEMA = "p7_td_b_r6_future_plan_activation_v2"
COMMITTED_SOURCE_ATTESTATION_SCHEMA = "p7_td_b_r6_committed_source_attestation_v1"
PACKAGE_BINDING_SCHEMA = "p7_td_b_r6_stage_gate_package_binding_v1"
ALLOWED_CODE_CHILD_SUBJECT = "feat(stage-gate): bind ray r6 package identity"
ALLOWED_CODE_CHILD_PATHS = (
    "src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py",
    "tests/test_p7_td_b_r6_stage_gate.py",
)
ORCHESTRATION_PATH_PREFIX = ".agent-work/"
_SHA40 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SECRET_TERMS = ("secret", "token", "password", "credential", "private-key", ".env")
_HISTORICAL_PREFIXES = (".agent-work/archived/", ".agent-work/PLANS/", "audit/")
_HISTORICAL_TERMS = ("retained-r3", "legacy-r2", "deep-corrective")


class StageGateError(RuntimeError):
    """A fail-closed G4-05 boundary error with a stable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class SourceReference:
    path: str
    bytes: int
    sha256: str
    mode: int


@dataclass(frozen=True)
class StageGateInput:
    schema: str
    source_checkpoint: str
    source_tree: str
    output_root: str
    source_references: tuple[SourceReference, ...]
    prerequisite_projection: Mapping[str, Any]


@dataclass(frozen=True)
class CommittedSourceAttestation:
    """Canonical read-only proof of the A -> C -> L source topology."""

    schema: str
    verified_parent_checkpoint: str
    verified_parent_tree: str
    code_owner_checkpoint: str
    code_owner_tree: str
    live_activation_checkpoint: str
    live_activation_tree: str
    candidate_references_sha256: str
    post_child_changed_paths: tuple[str, ...]
    post_child_commits: tuple[Mapping[str, Any], ...]


def _native(value: Any) -> Any:
    return provenance.json_native_value(value)


def _source_reference_value(value: SourceReference) -> dict[str, Any]:
    if type(value) is not SourceReference:
        raise StageGateError("source_reference_type_invalid")
    return asdict(value)


def _validate_repo_path(value: object) -> str:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        raise StageGateError("source_path_invalid")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise StageGateError("source_path_invalid")
    lowered = value.lower()
    if any(term in lowered for term in _SECRET_TERMS):
        raise StageGateError("secret_material_prohibited")
    if value.startswith(_HISTORICAL_PREFIXES) or any(
        term in lowered for term in _HISTORICAL_TERMS
    ):
        raise StageGateError("historical_input_prohibited")
    return value


def _read_source(repo_root: Path, path: str) -> SourceReference:
    relative = _validate_repo_path(path)
    root = repo_root.resolve(strict=True)
    target = root / relative
    try:
        observed = os.lstat(target)
    except OSError as exc:
        raise StageGateError("source_missing") from exc
    if stat.S_ISLNK(observed.st_mode) or not stat.S_ISREG(observed.st_mode):
        raise StageGateError("source_not_regular")
    try:
        identity = provenance.read_exact_file(target)
    except provenance.ProvenanceIOError as exc:
        raise StageGateError(f"source_{exc.code}") from exc
    return SourceReference(
        path=relative,
        bytes=identity.byte_count,
        sha256=identity.sha256,
        mode=identity.mode,
    )


def _validate_source_references(
    references: object, *, repo_root: Path, require_expected_set: bool = True,
    allow_orchestration_drift: bool = False,
) -> tuple[SourceReference, ...]:
    if type(references) is not tuple or any(
        type(item) is not SourceReference for item in references
    ):
        raise StageGateError("source_references_type_invalid")
    paths = tuple(item.path for item in references)
    if len(set(paths)) != len(paths):
        raise StageGateError("source_reference_duplicate")
    if paths != tuple(sorted(paths, key=lambda item: item.encode("utf-8"))):
        raise StageGateError("source_references_not_sorted")
    if require_expected_set and paths != EXPECTED_SOURCE_PATHS:
        raise StageGateError("source_reference_set_drift")
    for item in references:
        _validate_repo_path(item.path)
        if (
            type(item.bytes) is not int
            or item.bytes <= 0
            or type(item.mode) is not int
            or item.mode < 0
            or _SHA256.fullmatch(item.sha256) is None
        ):
            raise StageGateError("source_reference_identity_invalid")
        if (
            not (allow_orchestration_drift and item.path.startswith(ORCHESTRATION_PATH_PREFIX))
            and _read_source(repo_root, item.path) != item
        ):
            raise StageGateError("source_reference_drift")
    return references


def _candidate_references(source_references: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_path = {
        str(item.get("path")): _native(item)
        for item in source_references
        if isinstance(item, Mapping)
    }
    try:
        candidates = [by_path[path] for path in ALLOWED_CODE_CHILD_PATHS]
    except KeyError as exc:
        raise StageGateError("candidate_reference_missing") from exc
    if any(set(item) != {"path", "bytes", "sha256", "mode"} for item in candidates):
        raise StageGateError("candidate_reference_shape_drift")
    return candidates


def _candidate_references_sha256(references: Sequence[Mapping[str, Any]]) -> str:
    return hashlib.sha256(provenance.canonical_json_bytes(_native(references))).hexdigest()


def _attestation_value(value: CommittedSourceAttestation) -> dict[str, Any]:
    if type(value) is not CommittedSourceAttestation:
        raise StageGateError("committed_source_attestation_type_invalid")
    return _native(asdict(value))


def _validate_post_child_ledger(attestation: Mapping[str, Any]) -> None:
    commits = attestation.get("post_child_commits")
    flattened = attestation.get("post_child_changed_paths")
    if type(commits) is not list or type(flattened) is not list:
        raise StageGateError("committed_source_post_child_ledger_shape_drift")
    expected_parent = attestation.get("code_owner_checkpoint")
    live = attestation.get("live_activation_checkpoint")
    visited = {expected_parent}
    observed_paths: list[str] = []
    for row in commits:
        if not isinstance(row, Mapping) or set(row) != {
            "parent_checkpoint", "child_checkpoint", "child_tree", "changed_paths",
        }:
            raise StageGateError("committed_source_post_child_ledger_shape_drift")
        parent = row.get("parent_checkpoint")
        child = row.get("child_checkpoint")
        child_tree = row.get("child_tree")
        paths = row.get("changed_paths")
        if (
            parent != expected_parent
            or _SHA40.fullmatch(str(child)) is None
            or _SHA40.fullmatch(str(child_tree)) is None
            or child in visited
            or type(paths) is not list
        ):
            raise StageGateError("committed_source_post_child_ledger_drift")
        for path in paths:
            if (
                type(path) is not str
                or not _canonical_git_path(path).startswith(ORCHESTRATION_PATH_PREFIX)
            ):
                raise StageGateError("committed_source_post_child_path_drift")
            observed_paths.append(path)
        visited.add(child)
        expected_parent = child
    if expected_parent != live or observed_paths != flattened:
        raise StageGateError("committed_source_post_child_ledger_drift")


def _projection(plan: Mapping[str, Any], full: Mapping[str, Any]) -> Mapping[str, Any]:
    if (
        plan.get("active_task_count") != 1
        or full.get("active_task_count") != 1
        or plan.get("active_task") != TASK_ID
        or full.get("active_task") != TASK_ID
        or plan.get("reference_task_id") != TASK_ID
        or plan.get("contract_id") != CONTRACT_ID
        or full.get("active_plan_contract_id") != CONTRACT_ID
        or full.get("canonical_next_reference_task") != TASK_ID
        or full.get("retained_r3_status") != RETAINED_R3_STATUS
        or full.get("release_consumption_authorized") is not False
        or full.get("formal_r6_authorized") is not False
        or full.get("td_c_authorized") is not False
    ):
        raise StageGateError("machine_contract_drift")
    frozen = full.get("frozen_guide_input")
    if not isinstance(frozen, Mapping) or dict(frozen) != {
        "stage": "EQ-R6_STATE_C",
        "selected_exposure": "1/2500",
        "status": "ACCEPTED_QUALIFIED_INPUT_NOT_A_CURRENT_TASK",
    }:
        raise StageGateError("scientific_prerequisite_drift")
    prerequisites: dict[str, Any] = {
        "eq_r6_state_c": dict(frozen),
        "g4_01": _native(full.get("g4_01_prerequisite")),
        "g4_02": _native(full.get("g4_02_prerequisite")),
        "g4_03": _native(full.get("g4_03_prerequisite")),
        "g4_04": _native(full.get("g4_04_prerequisite")),
        "retained_r3_status": RETAINED_R3_STATUS,
        "canonical_validator_success": full.get("canonical_validator_success"),
        "eligibility": full.get("eligibility"),
        "release_consumable": full.get("release_consumable"),
        "release_consumption_authorized": False,
        "device_authorized": False,
        "formal_r6_authorized": False,
        "td_c_authorized": False,
    }
    if (
        prerequisites["canonical_validator_success"] is not True
        or prerequisites["eligibility"] is not True
        or prerequisites["release_consumable"] is not True
        or any(not isinstance(prerequisites[key], Mapping) for key in ("g4_01", "g4_02", "g4_03", "g4_04"))
    ):
        raise StageGateError("prerequisite_projection_drift")
    return prerequisites


def build_stage_gate_input(
    *, repo_root: str | Path, source_checkpoint: str, source_tree: str,
    output_root: str | Path,
) -> StageGateInput:
    """Freeze current repo source identities without reading external artifacts."""

    root = Path(repo_root).resolve(strict=True)
    if _SHA40.fullmatch(source_checkpoint) is None or _SHA40.fullmatch(source_tree) is None:
        raise StageGateError("source_git_identity_invalid")
    output = Path(output_root)
    if not output.is_absolute() or str(output) != os.fspath(output_root):
        raise StageGateError("output_root_invalid")
    plan_source = (root / ".agent-work/PLAN.md").read_bytes()
    full_source = (root / ".agent-work/FULL_PLAN_REFERENCE.md").read_bytes()
    plan = parse_plan_machine_contract(plan_source).value
    full = parse_full_plan_machine_state(full_source).value
    expected_output_root = plan.get(
        "new_stage_gate_root", plan.get("stage_gate_root"),
    )
    if expected_output_root != str(output):
        raise StageGateError("output_root_drift")
    references = tuple(_read_source(root, path) for path in EXPECTED_SOURCE_PATHS)
    references = tuple(sorted(references, key=lambda item: item.path.encode("utf-8")))
    return StageGateInput(
        schema=INPUT_SCHEMA,
        source_checkpoint=source_checkpoint,
        source_tree=source_tree,
        output_root=str(output),
        source_references=references,
        prerequisite_projection=_projection(plan, full),
    )


def _state_for_capture(capture_id: str) -> str:
    if "-ray-a" in capture_id:
        return "A"
    if "-ray-d-" in capture_id:
        return "D"
    if "-ray-b-" in capture_id:
        return "B"
    if "-ray-c-" in capture_id:
        return "C"
    raise StageGateError("canonical_capture_state_invalid")


def _expanded_contract() -> dict[str, Any]:
    plan = thermal.build_td_b_r6_formal_plan()
    thermal.validate_td_b_r6_formal_plan(plan)
    captures = []
    for index, capture_id in enumerate(plan["capture_ids"]):
        state = _state_for_capture(capture_id)
        match = re.search(r"-t([0-9]+)\Z", capture_id)
        if match is None:
            raise StageGateError("canonical_capture_time_invalid")
        captures.append({
            "sequence_index": index,
            "capture_id": capture_id,
            "state_id": state,
            "elapsed_s": int(match.group(1)),
            "source": "ray",
            "strip": "zero_throughout",
            "nominal_shutter": plan["state_shutters"][state],
            "exposure_mode": "fixed",
            "weak_reacquire": False,
            "mid_run_shutter_change": False,
        })
    return {
        "canonical_plan": plan,
        "captures": captures,
        "operating_envelope": {
            "dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "steady_status": "not_demonstrated",
        },
        "capture_acceptance_requirements": [
            "current_run_unique_cr3_and_sidecar_path_bytes_sha256",
            "remote_capture_and_request_ids",
            "makernote_actual_exposure",
            "exact_state_and_readback",
            "strip_zero",
            "exact_58_required_features",
            "clipped_fraction_zero",
            "near_noise_finite_valid_pixels",
            "timing_and_chronology_provenance",
            "physical_budget_accounting",
        ],
        "history_gate": {
            "anchors": [
                "000-ray-a0-t600", "005-ray-a-after-d-t600",
                "010-ray-a-after-b-t600", "015-ray-a-after-c-t600",
            ],
            "all_compatible_required_for_strip_entry": True,
            "bypass_allowed": False,
        },
        "hard_failure": {
            "classification": "accepted_hard_failed_formal_attempt",
            "formal_pass": False,
            "strip_call_count": 0,
            "retry": 0,
            "terminal_seal_required": True,
            "alternate_root": 0,
        },
    }


def _template_authority() -> dict[str, Any]:
    return {
        "schema": TEMPLATE_AUTHORITY_SCHEMA,
        "execution_authorized": False,
        "allow_device_control": False,
        "remote_v2_capability": True,
    }


def _capture_role(index: int, state: str) -> str:
    if index == 0:
        return "initial_anchor"
    if state == "A":
        return {5: "return_after_D", 10: "return_after_B", 15: "return_after_C"}[index]
    return "switch_curve"


def build_runtime_plan_template() -> dict[str, Any]:
    """Build one deterministic PLAN_SCHEMA_V2 shape without execution authority."""

    canonical = thermal.build_td_b_r6_formal_plan()
    thermal.validate_td_b_r6_formal_plan(canonical)
    group_ends = {0, 4, 5, 9, 10, 14, 15}
    captures: list[dict[str, Any]] = []
    for index, capture_id in enumerate(canonical["capture_ids"]):
        state = _state_for_capture(capture_id)
        elapsed_match = re.search(r"-t([0-9]+)\Z", capture_id)
        if elapsed_match is None:
            raise StageGateError("canonical_capture_time_invalid")
        command = dict(thermal.RAY_STATES[state])
        captures.append({
            "capture_id": capture_id,
            "sequence_index": index,
            "source_id": "ray",
            "state_id": state,
            "command": command,
            "exact_command_hash": thermal.canonical_sha256(command),
            "requested_elapsed_s": int(elapsed_match.group(1)),
            "timing_acceptance": "observed_elapsed_record_only",
            "timing_status": "resolved",
            "formal_measurement": True,
            "capture_role": "formal",
            "role": _capture_role(index, state),
            "isolation_gate_after": (
                f"after_{_capture_role(index, state)}_{index:03d}"
                if index in group_ends else None
            ),
            "exposure_mode": "fixed",
            "weak_reacquire": False,
            "mid_run_shutter_change": False,
            "strip_state": "zero_throughout",
        })
    required_keys = thermal.required_shutter_cache_keys(captures)
    frozen_shutters: dict[str, str] = {}
    for step in captures:
        key = thermal.shutter_cache_key_for_step(step)
        if key is not None:
            frozen_shutters[key] = canonical["state_shutters"][step["state_id"]]
    if tuple(sorted(frozen_shutters)) != required_keys:
        raise StageGateError("runtime_shutter_owner_drift")
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": RUNTIME_TEMPLATE_STATUS,
        "runtime_plan_state": "sealed_non_authorizing_template",
        "experiment_id": thermal.TD_B,
        "guide_experiment_id": thermal.TD_B_R6_EXPERIMENT_ID,
        "guide_contract_schema": canonical["schema"],
        "variant": "core",
        "source": "ray",
        "stage": "TD-B",
        "timing_contract": thermal.timing_contract(2),
        "native_raw_ambient_policy": thermal.expected_native_raw_ambient_policy(
            thermal.TD_B, plan_schema=thermal.PLAN_SCHEMA_V2,
        ),
        "camera": {
            "backend": "remote",
            "auto_exposure_in_timed_cycle": False,
            "actual_exposure_start_provenance_required": False,
            "adapter_capability_available": True,
            "v2_capture_timing_capability_available": True,
        },
        "execution_authorization": _template_authority(),
        "formal_capture_eligible": False,
        "captures": captures,
        "budgets": {
            "formal_cap": 16,
            "logical_cap": 16,
            "ambient_cap": 0,
            "setup_physical_cr3_cap": 0,
            "physical_cr3_cap": 16,
            "launch_cap": 1,
            "retry": 0,
        },
        "frozen_shutters": frozen_shutters,
        "exposure_setup_required": [],
        "setup_physical_cr3_count": 0,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(required_keys),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen_shutters),
        },
        "capture_ledger_contract": {
            "formal_measurement": "boolean",
            "capture_role": ["formal", "ambient"],
            "ambient_counts_as_physical_cr3": True,
            "physical_return_ledger_schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_return_precedes_measurement_acceptance": True,
            "old_new_frame_combination": "prohibited",
            "accepted_capture_count": 16,
        },
        "post_capture_validator": {
            "module": "camera_based_rgbww_optimizer.optimization.p7_thermal_diagnostics",
            "callable": "validate_td_b_r6_capture_ledger",
            "call_stage": "post_capture_before_analysis",
            "g4_05_call_count": 0,
            "required_fields": [
                "current_run_cr3_sidecar_path_bytes_sha256",
                "remote_capture_request_ids",
                "makernote_actual_exposure",
                "exact_state_readback_strip_zero",
                "58_features_clip_noise_finite_valid_pixels",
                "timing_chronology_budget",
            ],
        },
        "quality_history_contract": {
            "quality_bypass_allowed": False,
            "history_bypass_allowed": False,
            "return_anchor_ids": [
                "000-ray-a0-t600", "005-ray-a-after-d-t600",
                "010-ray-a-after-b-t600", "015-ray-a-after-c-t600",
            ],
            "operating_claim": "selected_fixed_time_transient_not_proven_steady",
        },
        "continuous_command_between_timed_points": True,
        "source_isolation_contract": (
            "independent_both_off_readback_at_run_ambient_and_transition_gates"
        ),
        "cleanup": {
            "python_finally": "required",
            "shell_trap": "EXIT_INT_TERM_HUP_required",
            "independent_final_zero": "required",
            "terminal_seal": "required",
        },
        "hard_locks": {
            "strip_nonzero": True,
            "auto_exposure": True,
            "weak_reacquire": True,
            "mid_run_shutter_change": True,
            "second_root": True,
            "seventeenth_return": True,
            "td_c": True,
        },
    }


def runtime_plan_template_sha256(template: Mapping[str, Any]) -> str:
    return hashlib.sha256(provenance.canonical_json_bytes(template)).hexdigest()


def validate_runtime_plan_template(template: Mapping[str, Any]) -> None:
    """Validate the complete non-authorizing runner shape and canonical R6 projection."""

    if not isinstance(template, Mapping):
        raise StageGateError("runtime_template_invalid")
    native = _native(template)
    canonical = native.get("guide_contract_schema")
    if canonical != thermal.build_td_b_r6_formal_plan()["schema"]:
        raise StageGateError("runtime_template_guide_contract_drift")
    expected = build_runtime_plan_template()
    if native != expected:
        raise StageGateError("runtime_template_drift")
    if native["execution_authorization"] != _template_authority():
        raise StageGateError("runtime_template_authority_drift")


_ACTIVATION_KEYS = {
    "schema", "active_task", "active_task_count", "execution_authorized",
    "allow_device_control", "descriptor_sha256", "template_sha256",
    "expected_runtime_sha256", "code_owner_checkpoint", "code_owner_tree",
    "live_activation_checkpoint", "live_activation_tree",
    "committed_source_attestation",
    "formal_root_parent", "formal_root_basename", "formal_root_basename_regex",
    "launch_cap", "retry",
}


def _validate_activation_shape(
    activation: Mapping[str, Any], template: Mapping[str, Any],
    *, require_expected_runtime: bool,
) -> None:
    if not isinstance(activation, Mapping) or set(activation) != _ACTIVATION_KEYS:
        raise StageGateError("future_activation_shape_drift")
    template_sha = runtime_plan_template_sha256(template)
    basename = activation.get("formal_root_basename")
    expected_runtime = activation.get("expected_runtime_sha256")
    attestation = activation.get("committed_source_attestation")
    if (
        activation.get("schema") != FUTURE_ACTIVATION_SCHEMA
        or activation.get("active_task") != FUTURE_TASK_ID
        or type(activation.get("active_task_count")) is not int
        or activation.get("active_task_count") != 1
        or activation.get("execution_authorized") is not True
        or activation.get("allow_device_control") is not True
        or _SHA256.fullmatch(str(activation.get("descriptor_sha256"))) is None
        or activation.get("template_sha256") != template_sha
        or _SHA40.fullmatch(str(activation.get("code_owner_checkpoint"))) is None
        or _SHA40.fullmatch(str(activation.get("code_owner_tree"))) is None
        or _SHA40.fullmatch(str(activation.get("live_activation_checkpoint"))) is None
        or _SHA40.fullmatch(str(activation.get("live_activation_tree"))) is None
        or not isinstance(attestation, Mapping)
        or set(attestation) != {
            "schema", "verified_parent_checkpoint", "verified_parent_tree",
            "code_owner_checkpoint", "code_owner_tree",
            "live_activation_checkpoint", "live_activation_tree",
            "candidate_references_sha256", "post_child_changed_paths",
            "post_child_commits",
        }
        or attestation.get("schema") != COMMITTED_SOURCE_ATTESTATION_SCHEMA
        or attestation.get("code_owner_checkpoint") != activation.get("code_owner_checkpoint")
        or attestation.get("code_owner_tree") != activation.get("code_owner_tree")
        or attestation.get("live_activation_checkpoint") != activation.get("live_activation_checkpoint")
        or attestation.get("live_activation_tree") != activation.get("live_activation_tree")
        or _SHA40.fullmatch(str(attestation.get("verified_parent_checkpoint"))) is None
        or _SHA40.fullmatch(str(attestation.get("verified_parent_tree"))) is None
        or _SHA256.fullmatch(str(attestation.get("candidate_references_sha256"))) is None
        or type(attestation.get("post_child_changed_paths")) is not list
        or any(type(path) is not str for path in attestation.get("post_child_changed_paths", ()))
        or type(attestation.get("post_child_commits")) is not list
        or activation.get("formal_root_parent") != FORMAL_ROOT_PARENT
        or type(basename) is not str
        or re.fullmatch(FORMAL_ROOT_BASENAME_REGEX, basename) is None
        or activation.get("formal_root_basename_regex") != FORMAL_ROOT_BASENAME_REGEX
        or type(activation.get("launch_cap")) is not int
        or activation.get("launch_cap") != 1
        or type(activation.get("retry")) is not int
        or activation.get("retry") != 0
        or (
            require_expected_runtime
            and _SHA256.fullmatch(str(expected_runtime)) is None
        )
    ):
        raise StageGateError("future_activation_drift")
    _validate_post_child_ledger(attestation)
    if attestation.get("code_owner_checkpoint") == attestation.get(
        "verified_parent_checkpoint"
    ):
        raise StageGateError("future_activation_role_drift")
    for path in attestation["post_child_changed_paths"]:
        if not _canonical_git_path(path).startswith(ORCHESTRATION_PATH_PREFIX):
            raise StageGateError("future_activation_post_child_path_drift")


def _materialized_projection(
    template: Mapping[str, Any], activation: Mapping[str, Any],
) -> dict[str, Any]:
    plan = _native(template)
    plan["status"] = "execute_authorized"
    plan["runtime_plan_state"] = "materialized_plan_bound_authorized"
    plan["formal_capture_eligible"] = True
    plan["execution_authorization"] = {
        "schema": PLAN_BOUND_AUTHORITY_SCHEMA,
        "execution_authorized": True,
        "active_task": FUTURE_TASK_ID,
        "active_task_count": 1,
        "allow_device_control": True,
        "remote_v2_capability": True,
        "descriptor_sha256": activation["descriptor_sha256"],
        "template_sha256": activation["template_sha256"],
        "committed_source_attestation": _native(
            activation["committed_source_attestation"]
        ),
        "formal_root_parent": FORMAL_ROOT_PARENT,
        "formal_root_basename": activation["formal_root_basename"],
        "formal_root_basename_regex": FORMAL_ROOT_BASENAME_REGEX,
        "launch_cap": 1,
        "retry": 0,
    }
    return plan


def materialized_runtime_plan_sha256(
    template: Mapping[str, Any], activation: Mapping[str, Any], *,
    committed_source_attestation: CommittedSourceAttestation,
) -> str:
    validate_runtime_plan_template(template)
    if activation.get("committed_source_attestation") != _attestation_value(
        committed_source_attestation
    ):
        raise StageGateError("committed_source_attestation_binding_drift")
    _validate_activation_shape(activation, template, require_expected_runtime=False)
    return hashlib.sha256(
        provenance.canonical_json_bytes(_materialized_projection(template, activation))
    ).hexdigest()


def materialize_runtime_plan(
    template: Mapping[str, Any], future_activation: Mapping[str, Any], *,
    committed_source_attestation: CommittedSourceAttestation,
) -> dict[str, Any]:
    """Purely materialize one authorized plan; no package or runtime I/O occurs."""

    validate_runtime_plan_template(template)
    if future_activation.get("committed_source_attestation") != _attestation_value(
        committed_source_attestation
    ):
        raise StageGateError("committed_source_attestation_binding_drift")
    _validate_activation_shape(
        future_activation, template, require_expected_runtime=True,
    )
    plan = _materialized_projection(template, future_activation)
    digest = hashlib.sha256(provenance.canonical_json_bytes(plan)).hexdigest()
    if digest != future_activation.get("expected_runtime_sha256"):
        raise StageGateError("materialized_runtime_hash_drift")
    validate_materialized_runtime_plan(plan)
    return plan


def validate_materialized_runtime_plan(plan: Mapping[str, Any]) -> None:
    """Validate exact R6 semantics and the PLAN-bound authority projection."""

    if not isinstance(plan, Mapping):
        raise StageGateError("materialized_runtime_invalid")
    native = _native(plan)
    authority = native.get("execution_authorization")
    expected_authority_keys = {
        "schema", "execution_authorized", "active_task", "active_task_count",
        "allow_device_control", "remote_v2_capability", "descriptor_sha256",
        "template_sha256", "committed_source_attestation",
        "formal_root_parent", "formal_root_basename",
        "formal_root_basename_regex", "launch_cap", "retry",
    }
    if not isinstance(authority, Mapping) or set(authority) != expected_authority_keys:
        raise StageGateError("runtime_authority_shape_drift")
    if (
        authority.get("schema") != PLAN_BOUND_AUTHORITY_SCHEMA
        or authority.get("execution_authorized") is not True
        or authority.get("active_task") != FUTURE_TASK_ID
        or type(authority.get("active_task_count")) is not int
        or authority.get("active_task_count") != 1
        or authority.get("allow_device_control") is not True
        or authority.get("remote_v2_capability") is not True
        or _SHA256.fullmatch(str(authority.get("descriptor_sha256"))) is None
        or _SHA256.fullmatch(str(authority.get("template_sha256"))) is None
        or not isinstance(authority.get("committed_source_attestation"), Mapping)
        or set(authority.get("committed_source_attestation", {})) != {
            "schema", "verified_parent_checkpoint", "verified_parent_tree",
            "code_owner_checkpoint", "code_owner_tree",
            "live_activation_checkpoint", "live_activation_tree",
            "candidate_references_sha256", "post_child_changed_paths",
            "post_child_commits",
        }
        or authority["committed_source_attestation"].get("schema")
        != COMMITTED_SOURCE_ATTESTATION_SCHEMA
        or any(
            _SHA40.fullmatch(str(authority["committed_source_attestation"].get(key))) is None
            for key in (
                "verified_parent_checkpoint", "verified_parent_tree",
                "code_owner_checkpoint", "code_owner_tree",
                "live_activation_checkpoint", "live_activation_tree",
            )
        )
        or _SHA256.fullmatch(str(
            authority["committed_source_attestation"].get("candidate_references_sha256")
        )) is None
        or type(authority["committed_source_attestation"].get("post_child_changed_paths")) is not list
        or type(authority["committed_source_attestation"].get("post_child_commits")) is not list
        or authority.get("formal_root_parent") != FORMAL_ROOT_PARENT
        or re.fullmatch(
            FORMAL_ROOT_BASENAME_REGEX,
            str(authority.get("formal_root_basename")),
        ) is None
        or authority.get("formal_root_basename_regex") != FORMAL_ROOT_BASENAME_REGEX
        or type(authority.get("launch_cap")) is not int
        or authority.get("launch_cap") != 1
        or type(authority.get("retry")) is not int
        or authority.get("retry") != 0
    ):
        raise StageGateError("runtime_authority_drift")
    committed = authority["committed_source_attestation"]
    _validate_post_child_ledger(committed)
    if committed.get("code_owner_checkpoint") == committed.get(
        "verified_parent_checkpoint"
    ):
        raise StageGateError("runtime_authority_role_drift")
    for path in committed["post_child_changed_paths"]:
        if not _canonical_git_path(path).startswith(ORCHESTRATION_PATH_PREFIX):
            raise StageGateError("runtime_authority_post_child_path_drift")
    template = _native(native)
    template["status"] = RUNTIME_TEMPLATE_STATUS
    template["runtime_plan_state"] = "sealed_non_authorizing_template"
    template["formal_capture_eligible"] = False
    template["execution_authorization"] = _template_authority()
    validate_runtime_plan_template(template)
    if authority.get("template_sha256") != runtime_plan_template_sha256(template):
        raise StageGateError("runtime_template_hash_drift")


def _authority_false() -> dict[str, Any]:
    return {
        "execution_authorized": False,
        "device_authorized": False,
        "network_authorized": False,
        "camera_authorized": False,
        "ray_authorized": False,
        "strip_authorized": False,
        "capture_authorized": False,
        "formal_r6_authorized": False,
        "formal_root_creation_authorized": False,
        "release_consumption_authorized": False,
        "td_c_authorized": False,
        "g4_06_unlocked": False,
    }


def evaluate_stage_gate(value: StageGateInput, *, repo_root: str | Path) -> dict[str, Any]:
    """Build the canonical offline gate after validating references first."""

    if type(value) is not StageGateInput or value.schema != INPUT_SCHEMA:
        raise StageGateError("input_invalid")
    root = Path(repo_root).resolve(strict=True)
    _validate_source_references(value.source_references, repo_root=root)
    if _SHA40.fullmatch(value.source_checkpoint) is None or _SHA40.fullmatch(value.source_tree) is None:
        raise StageGateError("source_git_identity_invalid")
    contract = _expanded_contract()
    runtime_template = build_runtime_plan_template()
    validate_runtime_plan_template(runtime_template)
    gate = {
        "schema": STAGE_GATE_SCHEMA,
        "status": "offline_stage_gate_pass_waiting_planner_review",
        "reference_task": TASK_ID,
        "contract_id": CONTRACT_ID,
        "source_checkpoint": value.source_checkpoint,
        "source_tree": value.source_tree,
        "output_root": value.output_root,
        "source_references": [_source_reference_value(item) for item in value.source_references],
        "prerequisites": _native(value.prerequisite_projection),
        "scientific_contract": contract,
        "runtime_plan_template": runtime_template,
        "runtime_plan_template_sha256": runtime_plan_template_sha256(runtime_template),
        "cleanup_contract": {
            "python_cleanup": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell_cleanup": "required_via_existing_production_wrapper_trap",
            "independent_final_zero": "required",
            "terminal_seal": "required",
        },
        "authority": _authority_false(),
        "claims": {
            "hardware_ready": False,
            "formal_pass": False,
            "quality_pass": False,
            "history_pass": False,
            "release_consumed": False,
            "offline_engineering_evidence_only": True,
        },
        "retry": 0,
        "alternate_root": 0,
    }
    validate_stage_gate(gate, repo_root=root)
    return gate


def _references_from_payload(value: object) -> tuple[SourceReference, ...]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes))
    ):
        raise StageGateError("descriptor_reference_drift")
    try:
        if any(not isinstance(item, Mapping) for item in value):
            raise TypeError("source reference is not a mapping")
        return tuple(SourceReference(**dict(item)) for item in value)
    except (TypeError, ValueError) as exc:
        raise StageGateError("descriptor_reference_drift") from exc


def _scan_semantic_guards(value: Any, *, key: str = "") -> None:
    if isinstance(value, Mapping):
        for child_key, child in value.items():
            _scan_semantic_guards(child, key=str(child_key))
        return
    if isinstance(value, (list, tuple)):
        for child in value:
            _scan_semantic_guards(child, key=key)
        return
    if type(value) is str:
        lowered = value.lower()
        if any(term in lowered for term in _SECRET_TERMS):
            raise StageGateError("secret_material_prohibited")
        if value.startswith(_HISTORICAL_PREFIXES) or any(
            term in lowered for term in _HISTORICAL_TERMS
        ):
            raise StageGateError("historical_input_prohibited")


def validate_stage_gate(
    value: Mapping[str, Any], *, repo_root: str | Path,
    allow_orchestration_drift: bool = False,
) -> None:
    if not isinstance(value, Mapping):
        raise StageGateError("stage_gate_invalid")
    root = Path(repo_root).resolve(strict=True)
    refs = _references_from_payload(value.get("source_references"))
    _validate_source_references(
        refs, repo_root=root,
        allow_orchestration_drift=allow_orchestration_drift,
    )
    canonical_plan = value.get("scientific_contract", {}).get("canonical_plan")
    if not isinstance(canonical_plan, Mapping):
        raise StageGateError("canonical_plan_missing")
    try:
        thermal.validate_td_b_r6_formal_plan(_native(canonical_plan))
    except (TypeError, ValueError) as exc:
        raise StageGateError("canonical_plan_drift") from exc
    expected = _expanded_contract()
    if _native(value.get("scientific_contract")) != expected:
        raise StageGateError("expanded_contract_drift")
    template = value.get("runtime_plan_template")
    if not isinstance(template, Mapping):
        raise StageGateError("runtime_template_missing")
    validate_runtime_plan_template(template)
    if value.get("runtime_plan_template_sha256") != runtime_plan_template_sha256(template):
        raise StageGateError("runtime_template_reference_drift")
    authority = value.get("authority")
    if authority != _authority_false():
        raise StageGateError("authority_drift")
    if (
        value.get("schema") != STAGE_GATE_SCHEMA
        or value.get("status") != "offline_stage_gate_pass_waiting_planner_review"
        or value.get("reference_task") != TASK_ID
        or value.get("contract_id") != CONTRACT_ID
        or type(value.get("output_root")) is not str
        or not Path(str(value.get("output_root"))).is_absolute()
        or value.get("retry") != 0
        or value.get("alternate_root") != 0
        or value.get("claims") != {
            "hardware_ready": False,
            "formal_pass": False,
            "quality_pass": False,
            "history_pass": False,
            "release_consumed": False,
            "offline_engineering_evidence_only": True,
        }
    ):
        raise StageGateError("stage_gate_semantic_drift")


def build_launch_descriptor(stage_gate: Mapping[str, Any]) -> dict[str, Any]:
    """Derive a non-executable future launch descriptor from the validated gate."""

    scientific = _native(stage_gate["scientific_contract"])
    descriptor = {
        "schema": LAUNCH_DESCRIPTOR_SCHEMA,
        "status": "non_authorizing_waiting_g4_06_plan",
        "reference_task": FUTURE_TASK_ID,
        "source_references": _native(stage_gate["source_references"]),
        "committed_source_contract": {
            "schema": COMMITTED_SOURCE_ATTESTATION_SCHEMA,
            "verified_parent": {
                "checkpoint": stage_gate["source_checkpoint"],
                "tree": stage_gate["source_tree"],
                "role": "activation_parent_not_code_owner",
            },
            "allowed_code_owner_child": {
                "subject": ALLOWED_CODE_CHILD_SUBJECT,
                "direct_parent": stage_gate["source_checkpoint"],
                "merge_commit_allowed": False,
                "changed_paths": list(ALLOWED_CODE_CHILD_PATHS),
                "candidate_references": _candidate_references(
                    stage_gate["source_references"]
                ),
                "child_checkpoint_recorded": False,
                "child_tree_recorded": False,
            },
            "allowed_post_child_lineage": {
                "code_owner_must_be_live_ancestor": True,
                "changed_path_prefix": ORCHESTRATION_PATH_PREFIX,
                "non_orchestration_changes_allowed": False,
                "linear_direct_child_required": True,
                "merge_commit_allowed": False,
                "nonlinear_history_allowed": False,
                "per_commit_adjacent_paths_required": True,
                "live_checkpoint_recorded": False,
                "live_tree_recorded": False,
            },
        },
        "scientific_contract": scientific,
        "runtime_plan_template_sha256": stage_gate["runtime_plan_template_sha256"],
        "production_wrapper": {
            "path": "tmp/run-p7-thermal-diagnostics.zsh",
            "identity_owned_by_source_references": True,
            "visible_terminal_required": True,
        },
        "runner": {
            "module": "camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics",
            "callable": "run_validated_td_b_r6_runtime_contract",
            "delegate": "run_authorized_plan",
            "delegate_signature": (
                "run_authorized_plan(runtime_plan, *, output_dir, run_name, camera_backend)"
            ),
            "argv_shape": [
                "--experiment-id", thermal.TD_B,
                "--source", "ray", "--phase", "formal", "--execute",
                "--allow-device-control", "--code-checkpoint", "<G4_06_COMMITTED_HEAD>",
                "--output-dir", "<EXACT_FRESH_PARENT>", "--run-name", "<EXACT_FRESH_BASENAME>",
            ],
        },
        "formal_root": {
            "parent": FORMAL_ROOT_PARENT,
            "basename_regex": FORMAL_ROOT_BASENAME_REGEX,
            "direct_child": True,
            "canonical_lexical_path": True,
            "must_be_absent_before_launch": True,
            "single_root": True,
        },
        "budgets": {
            "logical": scientific["canonical_plan"]["formal_logical"],
            "physical_cap": scientific["canonical_plan"]["formal_physical_cap"],
            "setup_in_formal_root": scientific["canonical_plan"]["setup_in_formal_root"],
            "ambient": scientific["canonical_plan"]["ambient"],
            "launch_cap": scientific["canonical_plan"]["launch"],
            "retry": scientific["canonical_plan"]["retry"],
        },
        "cleanup": {
            "python": "existing_measure_owner_required",
            "shell": "existing_production_wrapper_trap_required",
            "independent_final_zero": "required",
            "terminal_seal": "required",
        },
        "bounds_expansion": {
            "firmware_flash": "human_stop",
            "remote_deployment": "human_stop",
            "destructive_hardware_change": "human_stop",
            "outside_plan": "human_stop",
            "target_intensity_range_duration_retry_recovery_expansion": "human_stop",
        },
        "authority": _authority_false(),
    }
    return descriptor


def validate_launch_descriptor(
    descriptor: Mapping[str, Any], stage_gate: Mapping[str, Any], *, repo_root: str | Path,
    allow_orchestration_drift: bool = False,
) -> None:
    """Validate references before applying semantic secret/historical guards."""

    if not isinstance(descriptor, Mapping) or not isinstance(stage_gate, Mapping):
        raise StageGateError("launch_descriptor_invalid")
    descriptor_refs = descriptor.get("source_references")
    if descriptor_refs != stage_gate.get("source_references"):
        raise StageGateError("descriptor_reference_drift")
    refs = _references_from_payload(descriptor_refs)
    _validate_source_references(
        refs, repo_root=Path(repo_root).resolve(strict=True),
        allow_orchestration_drift=allow_orchestration_drift,
    )
    _scan_semantic_guards({
        key: value for key, value in descriptor.items() if key != "source_references"
    })
    expected = build_launch_descriptor(stage_gate)
    if _native(descriptor) != expected:
        raise StageGateError("launch_descriptor_semantic_drift")


def _git(
    repo_root: Path, *arguments: str, text: bool = False,
) -> bytes | str:
    try:
        completed = subprocess.run(
            ["git", *arguments], cwd=repo_root, check=True,
            capture_output=True, text=text,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise StageGateError("committed_source_git_query_failed") from exc
    return completed.stdout


def _git_text(repo_root: Path, *arguments: str) -> str:
    value = _git(repo_root, *arguments, text=True)
    assert isinstance(value, str)
    return value.rstrip("\n")


def _canonical_attestation_root(repo_root: str | Path) -> Path:
    requested = Path(repo_root)
    if not requested.is_absolute() or requested.is_symlink():
        raise StageGateError("committed_source_repo_root_invalid")
    try:
        resolved = requested.resolve(strict=True)
    except OSError as exc:
        raise StageGateError("committed_source_repo_root_invalid") from exc
    if requested != resolved:
        raise StageGateError("committed_source_repo_root_invalid")
    top = _git_text(resolved, "rev-parse", "--show-toplevel")
    if Path(top) != resolved:
        raise StageGateError("committed_source_repo_root_invalid")
    return resolved


def _canonical_git_path(value: object) -> str:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        raise StageGateError("committed_source_path_invalid")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
        raise StageGateError("committed_source_path_invalid")
    if str(parsed) != value:
        raise StageGateError("committed_source_path_invalid")
    return value


def _worktree_status_paths(repo_root: Path) -> tuple[str, ...]:
    raw = _git(
        repo_root, "status", "--porcelain=v1", "-z", "--untracked-files=all",
    )
    assert isinstance(raw, bytes)
    records = raw.decode("utf-8", errors="strict").split("\0")
    paths: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2] != " ":
            raise StageGateError("committed_source_worktree_status_invalid")
        status = record[:2]
        paths.append(_canonical_git_path(record[3:]))
        if "R" in status or "C" in status:
            if index >= len(records) or not records[index]:
                raise StageGateError("committed_source_worktree_status_invalid")
            paths.append(_canonical_git_path(records[index]))
            index += 1
    return tuple(paths)


def _validate_descriptor_attestation_contract(
    descriptor: Mapping[str, Any],
) -> tuple[str, str, list[dict[str, Any]]]:
    contract = descriptor.get("committed_source_contract")
    if not isinstance(contract, Mapping) or set(contract) != {
        "schema", "verified_parent", "allowed_code_owner_child",
        "allowed_post_child_lineage",
    }:
        raise StageGateError("committed_source_descriptor_shape_drift")
    parent = contract.get("verified_parent")
    child = contract.get("allowed_code_owner_child")
    lineage = contract.get("allowed_post_child_lineage")
    source_refs = descriptor.get("source_references")
    if not isinstance(source_refs, Sequence) or isinstance(source_refs, (str, bytes)):
        raise StageGateError("committed_source_descriptor_shape_drift")
    candidates = _candidate_references(source_refs)
    if (
        contract.get("schema") != COMMITTED_SOURCE_ATTESTATION_SCHEMA
        or not isinstance(parent, Mapping)
        or set(parent) != {"checkpoint", "tree", "role"}
        or _SHA40.fullmatch(str(parent.get("checkpoint"))) is None
        or _SHA40.fullmatch(str(parent.get("tree"))) is None
        or parent.get("role") != "activation_parent_not_code_owner"
        or not isinstance(child, Mapping)
        or set(child) != {
            "subject", "direct_parent", "merge_commit_allowed", "changed_paths",
            "candidate_references", "child_checkpoint_recorded",
            "child_tree_recorded",
        }
        or child.get("subject") != ALLOWED_CODE_CHILD_SUBJECT
        or child.get("direct_parent") != parent.get("checkpoint")
        or child.get("merge_commit_allowed") is not False
        or child.get("changed_paths") != list(ALLOWED_CODE_CHILD_PATHS)
        or child.get("candidate_references") != candidates
        or child.get("child_checkpoint_recorded") is not False
        or child.get("child_tree_recorded") is not False
        or not isinstance(lineage, Mapping)
        or lineage != {
            "code_owner_must_be_live_ancestor": True,
            "changed_path_prefix": ORCHESTRATION_PATH_PREFIX,
            "non_orchestration_changes_allowed": False,
            "linear_direct_child_required": True,
            "merge_commit_allowed": False,
            "nonlinear_history_allowed": False,
            "per_commit_adjacent_paths_required": True,
            "live_checkpoint_recorded": False,
            "live_tree_recorded": False,
        }
    ):
        raise StageGateError("committed_source_descriptor_semantic_drift")
    return str(parent["checkpoint"]), str(parent["tree"]), candidates


def validate_committed_source_attestation(
    descriptor: Mapping[str, Any], future_activation: Mapping[str, Any], *,
    repo_root: str | Path,
) -> CommittedSourceAttestation:
    """Validate A/C/L topology and committed candidate bytes using read-only Git."""

    if not isinstance(descriptor, Mapping) or not isinstance(future_activation, Mapping):
        raise StageGateError("committed_source_input_invalid")
    root = _canonical_attestation_root(repo_root)
    parent_checkpoint, parent_tree, candidates = (
        _validate_descriptor_attestation_contract(descriptor)
    )
    code_checkpoint = future_activation.get("code_owner_checkpoint")
    code_tree = future_activation.get("code_owner_tree")
    live_checkpoint = future_activation.get("live_activation_checkpoint")
    live_tree = future_activation.get("live_activation_tree")
    if any(
        _SHA40.fullmatch(str(value)) is None
        for value in (code_checkpoint, code_tree, live_checkpoint, live_tree)
    ):
        raise StageGateError("committed_source_activation_identity_invalid")
    if (
        _git_text(root, "rev-parse", f"{parent_checkpoint}^{{commit}}") != parent_checkpoint
        or _git_text(root, "rev-parse", f"{parent_checkpoint}^{{tree}}") != parent_tree
        or _git_text(root, "rev-parse", f"{code_checkpoint}^{{tree}}") != code_tree
        or _git_text(root, "rev-parse", f"{live_checkpoint}^{{tree}}") != live_tree
    ):
        raise StageGateError("committed_source_tree_drift")
    head = _git_text(root, "rev-parse", "HEAD")
    head_tree = _git_text(root, "rev-parse", "HEAD^{tree}")
    if head != live_checkpoint or head_tree != live_tree:
        raise StageGateError("committed_source_live_head_drift")
    parent_row = _git_text(root, "rev-list", "--parents", "-n", "1", str(code_checkpoint)).split()
    if len(parent_row) != 2 or parent_row[1] != parent_checkpoint:
        raise StageGateError("committed_source_parent_drift")
    if _git_text(root, "show", "-s", "--format=%s", str(code_checkpoint)) != ALLOWED_CODE_CHILD_SUBJECT:
        raise StageGateError("committed_source_subject_drift")
    try:
        changed = tuple(thermal.changed_paths_between_checkpoints(
            parent_checkpoint, str(code_checkpoint), project_root=root,
        ))
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise StageGateError("committed_source_changed_paths_query_failed") from exc
    if changed != ALLOWED_CODE_CHILD_PATHS:
        raise StageGateError("committed_source_changed_paths_drift")
    for reference in candidates:
        path = _canonical_git_path(reference["path"])
        raw_entry = _git(root, "ls-tree", "-z", str(code_checkpoint), "--", path)
        assert isinstance(raw_entry, bytes)
        entries = [item for item in raw_entry.split(b"\0") if item]
        if len(entries) != 1:
            raise StageGateError("committed_source_candidate_blob_missing")
        try:
            metadata, encoded_path = entries[0].split(b"\t", 1)
            git_mode, git_type, _blob_oid = metadata.decode("ascii").split(" ", 2)
            tree_path = encoded_path.decode("utf-8")
        except (UnicodeError, ValueError) as exc:
            raise StageGateError("committed_source_candidate_blob_invalid") from exc
        blob = _git(root, "show", f"{code_checkpoint}:{path}")
        assert isinstance(blob, bytes)
        if (
            git_mode != "100644"
            or git_type != "blob"
            or tree_path != path
            or len(blob) != reference["bytes"]
            or hashlib.sha256(blob).hexdigest() != reference["sha256"]
            or reference["mode"] != 0o644
        ):
            raise StageGateError("committed_source_candidate_blob_drift")
        if _source_reference_value(_read_source(root, path)) != reference:
            raise StageGateError("committed_source_current_candidate_drift")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", str(code_checkpoint), str(live_checkpoint)],
        cwd=root, capture_output=True,
    )
    if ancestor.returncode != 0:
        raise StageGateError("committed_source_lineage_drift")
    reverse_commits: list[dict[str, Any]] = []
    visited = {str(live_checkpoint)}
    current = str(live_checkpoint)
    while current != str(code_checkpoint):
        row = _git_text(root, "rev-list", "--parents", "-n", "1", current).split()
        if len(row) != 2 or row[0] != current:
            raise StageGateError("committed_source_post_child_non_linear_history")
        parent = row[1]
        if parent in visited:
            raise StageGateError("committed_source_post_child_history_cycle")
        child_tree = _git_text(root, "rev-parse", f"{current}^{{tree}}")
        if _SHA40.fullmatch(child_tree) is None:
            raise StageGateError("committed_source_post_child_tree_invalid")
        try:
            adjacent_paths = tuple(thermal.changed_paths_between_checkpoints(
                parent, current, project_root=root,
            ))
        except (OSError, subprocess.CalledProcessError, ValueError) as exc:
            raise StageGateError("committed_source_post_child_query_failed") from exc
        for path in adjacent_paths:
            canonical = _canonical_git_path(path)
            if not canonical.startswith(ORCHESTRATION_PATH_PREFIX):
                raise StageGateError("committed_source_post_child_path_drift")
        reverse_commits.append({
            "parent_checkpoint": parent,
            "child_checkpoint": current,
            "child_tree": child_tree,
            "changed_paths": list(adjacent_paths),
        })
        visited.add(parent)
        current = parent
    post_child_commits = tuple(reversed(reverse_commits))
    post_child_paths = tuple(
        path
        for row in post_child_commits
        for path in row["changed_paths"]
    )
    refs = _references_from_payload(descriptor.get("source_references"))
    _validate_source_references(
        refs, repo_root=root, allow_orchestration_drift=True,
    )
    if any(
        not path.startswith(ORCHESTRATION_PATH_PREFIX)
        for path in _worktree_status_paths(root)
    ):
        raise StageGateError("committed_source_worktree_scope_drift")
    attestation = CommittedSourceAttestation(
        schema=COMMITTED_SOURCE_ATTESTATION_SCHEMA,
        verified_parent_checkpoint=parent_checkpoint,
        verified_parent_tree=parent_tree,
        code_owner_checkpoint=str(code_checkpoint),
        code_owner_tree=str(code_tree),
        live_activation_checkpoint=str(live_checkpoint),
        live_activation_tree=str(live_tree),
        candidate_references_sha256=_candidate_references_sha256(candidates),
        post_child_changed_paths=post_child_paths,
        post_child_commits=post_child_commits,
    )
    supplied = future_activation.get("committed_source_attestation")
    if supplied is not None and supplied != _attestation_value(attestation):
        raise StageGateError("committed_source_attestation_binding_drift")
    return attestation


def validate_future_activation(
    descriptor: Mapping[str, Any],
    template: Mapping[str, Any],
    runtime_plan: Mapping[str, Any],
    activation: Mapping[str, Any],
    *,
    repo_root: str | Path,
    output_dir: str | Path,
    run_name: str,
) -> None:
    """Bind descriptor, template, runtime hash, source, and exact root bounds."""

    validate_runtime_plan_template(template)
    attestation = validate_committed_source_attestation(
        descriptor, activation, repo_root=repo_root,
    )
    _validate_activation_shape(activation, template, require_expected_runtime=True)
    if (
        descriptor.get("authority") != _authority_false()
        or activation.get("descriptor_sha256")
        != hashlib.sha256(provenance.canonical_json_bytes(descriptor)).hexdigest()
        or descriptor.get("runtime_plan_template_sha256")
        != activation.get("template_sha256")
        or activation.get("committed_source_attestation")
        != _attestation_value(attestation)
        or runtime_plan_template_sha256(template) != activation.get("template_sha256")
        or activation.get("expected_runtime_sha256")
        != hashlib.sha256(provenance.canonical_json_bytes(runtime_plan)).hexdigest()
        or type(run_name) is not str
        or run_name != activation.get("formal_root_basename")
        or str(Path(output_dir)) != activation.get("formal_root_parent")
        or str(Path(output_dir) / run_name)
        != str(Path(FORMAL_ROOT_PARENT) / str(activation.get("formal_root_basename")))
    ):
        raise StageGateError("future_activation_binding_drift")
    validate_materialized_runtime_plan(runtime_plan)


def _artifact_reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    return {
        "path": Path(identity.path).name,
        "bytes": identity.byte_count,
        "sha256": identity.sha256,
        "device": identity.device,
        "inode": identity.inode,
        "mode": identity.mode,
    }


def _root_value(root: provenance.DirectoryIdentity) -> dict[str, Any]:
    return {"path": root.path, "device": root.device, "inode": root.inode, "mode": root.mode}


def _read_artifact(root: provenance.DirectoryIdentity, reference: Mapping[str, Any]) -> provenance.FileIdentity:
    try:
        identity = provenance.read_exact_file(
            Path(root.path) / str(reference["path"]),
            expected_mode=0o600,
            expected_size=int(reference["bytes"]),
            expected_sha256=str(reference["sha256"]),
            root=root,
        )
    except (KeyError, TypeError, ValueError, provenance.ProvenanceIOError) as exc:
        raise StageGateError("artifact_identity_drift") from exc
    if (
        identity.device != reference.get("device")
        or identity.inode != reference.get("inode")
        or identity.mode != reference.get("mode")
    ):
        raise StageGateError("artifact_identity_drift")
    return identity


def _load_stage_gate_package(
    output_root: str | Path, *, repo_root: str | Path,
    allow_orchestration_drift: bool,
) -> dict[str, Any]:
    try:
        root = provenance.read_existing_root(output_root)
        inventory = provenance.list_exact_regular_children(root)
    except provenance.ProvenanceIOError as exc:
        raise StageGateError(f"replay_{exc.code}") from exc
    if inventory != EXPECTED_ARTIFACTS:
        raise StageGateError("artifact_inventory_drift")
    try:
        terminal_identity = provenance.read_exact_file(
            Path(root.path) / "terminal-seal.json", expected_mode=0o600, root=root,
        )
        terminal = provenance.decode_canonical_json(terminal_identity.data)
    except provenance.ProvenanceIOError as exc:
        raise StageGateError(f"terminal_{exc.code}") from exc
    if (
        not isinstance(terminal, Mapping)
        or terminal.get("schema") != TERMINAL_SEAL_SCHEMA
        or terminal.get("status") != PASS_STATUS
        or terminal.get("root") != _root_value(root)
        or tuple(terminal.get("inventory_before_terminal", ())) != PRE_TERMINAL_ARTIFACTS
        or terminal.get("retry") != 0
        or terminal.get("alternate_root") != 0
        or "terminal-seal.json" in str(terminal.get("artifacts"))
    ):
        raise StageGateError("terminal_seal_drift")
    artifacts = terminal.get("artifacts")
    if not isinstance(artifacts, Mapping) or set(artifacts) != {
        "launch-descriptor.json", "stage-gate.json",
    }:
        raise StageGateError("terminal_reference_drift")
    stage_identity = _read_artifact(root, artifacts["stage-gate.json"])
    descriptor_identity = _read_artifact(root, artifacts["launch-descriptor.json"])
    try:
        stage_gate = provenance.decode_canonical_json(stage_identity.data)
        descriptor = provenance.decode_canonical_json(descriptor_identity.data)
    except provenance.ProvenanceIOError as exc:
        raise StageGateError(f"artifact_{exc.code}") from exc
    validate_stage_gate(
        stage_gate,
        repo_root=repo_root,
        allow_orchestration_drift=allow_orchestration_drift,
    )
    validate_launch_descriptor(
        descriptor,
        stage_gate,
        repo_root=repo_root,
        allow_orchestration_drift=allow_orchestration_drift,
    )
    return {
        "status": "pass",
        "root": _root_value(root),
        "inventory": list(inventory),
        "artifacts": {
            "stage-gate.json": _artifact_reference(stage_identity),
            "launch-descriptor.json": _artifact_reference(descriptor_identity),
            "terminal-seal.json": _artifact_reference(terminal_identity),
        },
        "stage_gate": _native(stage_gate),
        "launch_descriptor": _native(descriptor),
    }


def replay_stage_gate_package(
    output_root: str | Path, *, repo_root: str | Path,
) -> dict[str, Any]:
    """Public canonical replay with bound root and file identities."""

    return _load_stage_gate_package(
        output_root,
        repo_root=repo_root,
        allow_orchestration_drift=False,
    )


def load_and_validate_stage_gate_package(
    package_dir: str | Path, *, repo_root: str | Path,
) -> dict[str, Any]:
    """Load a sealed package while allowing only live orchestration-file drift."""

    return _load_stage_gate_package(
        package_dir,
        repo_root=repo_root,
        allow_orchestration_drift=True,
    )


def stage_gate_package_binding(package: Mapping[str, Any]) -> dict[str, Any]:
    """Project one successful canonical replay into the closed machine binding."""

    if (
        not isinstance(package, Mapping)
        or package.get("status") != "pass"
        or not isinstance(package.get("root"), Mapping)
        or tuple(package.get("inventory", ())) != EXPECTED_ARTIFACTS
        or not isinstance(package.get("artifacts"), Mapping)
        or set(package["artifacts"]) != set(EXPECTED_ARTIFACTS)
    ):
        raise StageGateError("package_binding_replay_shape_drift")
    root = _native(package["root"])
    artifacts = _native(package["artifacts"])
    if (
        set(root) != {"path", "device", "inode", "mode"}
        or type(root["path"]) is not str
        or not Path(root["path"]).is_absolute()
        or any(
            set(artifacts[name])
            != {"path", "bytes", "sha256", "device", "inode", "mode"}
            or artifacts[name]["path"] != name
            for name in EXPECTED_ARTIFACTS
        )
    ):
        raise StageGateError("package_binding_replay_identity_drift")
    return {
        "schema": PACKAGE_BINDING_SCHEMA,
        "package_root": root,
        "inventory": list(EXPECTED_ARTIFACTS),
        "artifacts": {
            name: artifacts[name]
            for name in EXPECTED_ARTIFACTS
        },
    }


def _formal_authority_contract(
    *, output_dir: str | Path, run_name: str,
    package_binding: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "experiment_id": thermal.TD_B,
        "source": "ray",
        "stage": "TD-B",
        "camera_backend": "remote",
        "formal_execution_authorized": True,
        "formal_root_creation_authorized": True,
        "device_control_authorized": True,
        "camera_authorized": True,
        "ray_authorized": True,
        "strip_authorized": False,
        "capture_authorized": True,
        "formal_root_parent": str(output_dir),
        "formal_root_basename": run_name,
        "formal_root_basename_regex": FORMAL_ROOT_BASENAME_REGEX,
        "logical_capture_cap": 16,
        "physical_cr3_cap": 16,
        "launch_cap": 1,
        "retry": 0,
        "release_consumption_authorized": False,
        "td_c_authorized": False,
        "stage_gate_package_binding": _native(package_binding),
    }


def _formal_full_mirror(authority: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "package": "B_FORMAL_ACQUISITION",
        "contract_id": FORMAL_PACKAGE_B_CONTRACT_ID,
        "authority_owner": "MATCHING_LIVE_PLAN_ONLY",
        "full_top_level_non_authorizing": True,
        "formal_authority_mirror": _native(authority),
        "g4_07_unlocked": False,
    }


def _validate_production_formal_machine_contract(
    repo_root: Path, *, output_dir: str | Path, run_name: str,
    package_binding: Mapping[str, Any],
) -> None:
    try:
        plan = parse_plan_machine_contract(
            (repo_root / ".agent-work/PLAN.md").read_bytes()
        ).value
        full = parse_full_plan_machine_state(
            (repo_root / ".agent-work/FULL_PLAN_REFERENCE.md").read_bytes()
        ).value
    except (OSError, ValueError) as exc:
        raise StageGateError("production_machine_contract_invalid") from exc
    authority = plan.get("formal_execution_authority")
    expected_authority = _formal_authority_contract(
        output_dir=output_dir, run_name=run_name,
        package_binding=package_binding,
    )
    if (
        plan.get("active_task_count") != 1
        or plan.get("active_task") != FUTURE_TASK_ID
        or plan.get("reference_task_id") != FUTURE_TASK_ID
        or plan.get("contract_id") != FORMAL_PACKAGE_B_CONTRACT_ID
        or plan.get("executable") is not True
        or not isinstance(authority, Mapping)
        or _native(authority) != expected_authority
        or full.get("active_task_count") != 1
        or full.get("active_task") != FUTURE_TASK_ID
        or full.get("current_plan_active_task_count") != 1
        or full.get("current_plan_active_task") != FUTURE_TASK_ID
        or full.get("active_plan_contract_id") != FORMAL_PACKAGE_B_CONTRACT_ID
        or full.get("canonical_next_reference_task") != FUTURE_TASK_ID
        or full.get("executable") is not False
        or full.get("full_is_non_executable_reference") is not True
        or full.get("release_consumption_authorized") is not False
        or full.get("device_authorized_by_this_file") is not False
        or full.get("camera_authorized_by_this_file") is not False
        or full.get("ray_authorized_by_this_file") is not False
        or full.get("strip_authorized_by_this_file") is not False
        or full.get("formal_r6_authorized") is not False
        or full.get("td_c_authorized") is not False
        or _native(full.get("g4_06_state")) != _formal_full_mirror(expected_authority)
    ):
        raise StageGateError("production_machine_contract_drift")


def _build_production_activation(
    descriptor: Mapping[str, Any], template: Mapping[str, Any], *,
    repo_root: Path, code_owner_checkpoint: str,
    output_dir: str | Path, run_name: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if _SHA40.fullmatch(code_owner_checkpoint) is None:
        raise StageGateError("production_code_checkpoint_invalid")
    live_checkpoint = _git_text(repo_root, "rev-parse", "HEAD")
    probe: dict[str, Any] = {
        "code_owner_checkpoint": code_owner_checkpoint,
        "code_owner_tree": _git_text(
            repo_root, "rev-parse", f"{code_owner_checkpoint}^{{tree}}",
        ),
        "live_activation_checkpoint": live_checkpoint,
        "live_activation_tree": _git_text(repo_root, "rev-parse", "HEAD^{tree}"),
    }
    attestation = validate_committed_source_attestation(
        descriptor, probe, repo_root=repo_root,
    )
    activation: dict[str, Any] = {
        "schema": FUTURE_ACTIVATION_SCHEMA,
        "active_task": FUTURE_TASK_ID,
        "active_task_count": 1,
        "execution_authorized": True,
        "allow_device_control": True,
        "descriptor_sha256": hashlib.sha256(
            provenance.canonical_json_bytes(descriptor)
        ).hexdigest(),
        "template_sha256": runtime_plan_template_sha256(template),
        "expected_runtime_sha256": "0" * 64,
        **probe,
        "committed_source_attestation": _attestation_value(attestation),
        "formal_root_parent": str(output_dir),
        "formal_root_basename": run_name,
        "formal_root_basename_regex": FORMAL_ROOT_BASENAME_REGEX,
        "launch_cap": 1,
        "retry": 0,
    }
    activation["expected_runtime_sha256"] = materialized_runtime_plan_sha256(
        template,
        activation,
        committed_source_attestation=attestation,
    )
    runtime = materialize_runtime_plan(
        template,
        activation,
        committed_source_attestation=attestation,
    )
    validate_future_activation(
        descriptor,
        template,
        runtime,
        activation,
        repo_root=repo_root,
        output_dir=output_dir,
        run_name=run_name,
    )
    return activation, runtime


def run_production_cli_launch(
    *, package_dir: str | Path, repo_root: str | Path,
    code_owner_checkpoint: str, output_dir: str | Path, run_name: str,
    camera_backend_name: str, camera_backend_kwargs: Mapping[str, Any],
    backend_factory: Callable[..., Any],
    delegated_run_fn: Callable[..., Any] | None = None,
    validated_run_fn: Callable[..., Any] | None = None,
) -> Any:
    """Require future Package-B authority before materializing the CLI launch."""

    root = _canonical_attestation_root(repo_root)
    if (
        camera_backend_name != "remote"
        or not isinstance(camera_backend_kwargs, Mapping)
        or set(camera_backend_kwargs) != {"env_file", "base_url", "timeout"}
        or not callable(backend_factory)
        or (delegated_run_fn is not None and not callable(delegated_run_fn))
        or (validated_run_fn is not None and not callable(validated_run_fn))
    ):
        raise StageGateError("production_cli_dispatch_shape_drift")
    package = load_and_validate_stage_gate_package(
        package_dir, repo_root=root,
    )
    package_binding = stage_gate_package_binding(package)
    _validate_production_formal_machine_contract(
        root, output_dir=output_dir, run_name=run_name,
        package_binding=package_binding,
    )
    stage_gate = package["stage_gate"]
    descriptor = package["launch_descriptor"]
    template = stage_gate.get("runtime_plan_template")
    if not isinstance(template, Mapping):
        raise StageGateError("runtime_template_missing")
    activation, runtime = _build_production_activation(
        descriptor,
        template,
        repo_root=root,
        code_owner_checkpoint=code_owner_checkpoint,
        output_dir=output_dir,
        run_name=run_name,
    )
    camera_backend = backend_factory(
        camera_backend_name, **dict(camera_backend_kwargs),
    )
    if validated_run_fn is None:
        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            run_validated_td_b_r6_runtime_contract,
        )

        validated_run_fn = run_validated_td_b_r6_runtime_contract
    kwargs: dict[str, Any] = {
        "repo_root": root,
        "output_dir": output_dir,
        "run_name": run_name,
        "camera_backend": camera_backend,
    }
    if delegated_run_fn is not None:
        kwargs["delegated_run_fn"] = delegated_run_fn
    return validated_run_fn(
        runtime,
        stage_gate,
        descriptor,
        activation,
        **kwargs,
    )


def persist_stage_gate_package(
    value: StageGateInput, *, repo_root: str | Path,
    evaluated_gate: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create one exclusive package and perform one internal canonical replay."""

    if type(value) is not StageGateInput:
        raise StageGateError("input_invalid")
    root: provenance.DirectoryIdentity | None = None
    phase = "root_create"
    try:
        root = provenance.create_exclusive_root(value.output_root)
        phase = "stage_gate"
        if evaluated_gate is None:
            gate = evaluate_stage_gate(value, repo_root=repo_root)
        else:
            gate = _native(evaluated_gate)
            validate_stage_gate(gate, repo_root=repo_root)
            if (
                gate.get("source_checkpoint") != value.source_checkpoint
                or gate.get("source_tree") != value.source_tree
                or gate.get("output_root") != value.output_root
                or gate.get("source_references")
                != [_source_reference_value(item) for item in value.source_references]
                or gate.get("prerequisites") != _native(value.prerequisite_projection)
            ):
                raise StageGateError("evaluated_gate_input_binding_drift")
        stage_identity = provenance.persist_canonical_json(root, "stage-gate.json", gate)
        phase = "launch_descriptor"
        descriptor = build_launch_descriptor(gate)
        validate_launch_descriptor(descriptor, gate, repo_root=repo_root)
        descriptor_identity = provenance.persist_canonical_json(
            root, "launch-descriptor.json", descriptor,
        )
        phase = "internal_replay"
        if provenance.list_exact_regular_children(root) != PRE_TERMINAL_ARTIFACTS:
            raise StageGateError("preterminal_inventory_drift")
        replayed_stage = provenance.decode_canonical_json(
            provenance.read_exact_file(
                Path(root.path) / "stage-gate.json", expected_mode=0o600, root=root,
            ).data
        )
        replayed_descriptor = provenance.decode_canonical_json(
            provenance.read_exact_file(
                Path(root.path) / "launch-descriptor.json", expected_mode=0o600, root=root,
            ).data
        )
        validate_stage_gate(replayed_stage, repo_root=repo_root)
        validate_launch_descriptor(replayed_descriptor, replayed_stage, repo_root=repo_root)
        phase = "terminal_seal"
        terminal = {
            "schema": TERMINAL_SEAL_SCHEMA,
            "status": PASS_STATUS,
            "root": _root_value(root),
            "inventory_before_terminal": list(PRE_TERMINAL_ARTIFACTS),
            "artifacts": {
                "stage-gate.json": _artifact_reference(stage_identity),
                "launch-descriptor.json": _artifact_reference(descriptor_identity),
            },
            "internal_replay": True,
            "retry": 0,
            "alternate_root": 0,
            "formal_capture_count": 0,
            "device_call_count": 0,
            "release_consumption_count": 0,
        }
        terminal_identity = provenance.persist_canonical_json(
            root, "terminal-seal.json", terminal,
        )
        return {
            "status": "pass",
            "root": _root_value(root),
            "artifacts": {
                "stage-gate.json": _artifact_reference(stage_identity),
                "launch-descriptor.json": _artifact_reference(descriptor_identity),
                "terminal-seal.json": _artifact_reference(terminal_identity),
            },
            "internal_replay": True,
        }
    except BaseException as exc:
        if root is not None:
            try:
                if "terminal-seal.json" not in provenance.list_exact_regular_children(root):
                    provenance.persist_canonical_json(root, "terminal-seal.json", {
                        "schema": TERMINAL_SEAL_SCHEMA,
                        "status": FAIL_STATUS,
                        "root": _root_value(root),
                        "failed_phase": phase,
                        "failure_code": getattr(exc, "code", type(exc).__name__),
                        "retry": 0,
                        "alternate_root": 0,
                        "formal_capture_count": 0,
                        "device_call_count": 0,
                        "release_consumption_count": 0,
                    })
            except BaseException:
                pass
        raise


def _canonical_cli_repo_root(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise StageGateError("cli_repo_root_not_absolute")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise StageGateError("cli_repo_root_invalid") from exc
    if resolved != path or not resolved.is_dir():
        raise StageGateError("cli_repo_root_not_canonical")
    return resolved


def _canonical_cli_package_root(value: str, *, must_exist: bool) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise StageGateError("cli_package_root_not_absolute")
    try:
        if must_exist:
            resolved = path.resolve(strict=True)
            if resolved != path or not resolved.is_dir():
                raise StageGateError("cli_package_root_not_canonical")
        else:
            parent = path.parent.resolve(strict=True)
            resolved = parent / path.name
            if resolved != path:
                raise StageGateError("cli_package_root_not_canonical")
            if path.exists() or path.is_symlink():
                raise StageGateError("cli_package_root_not_fresh")
    except OSError as exc:
        raise StageGateError("cli_package_root_invalid") from exc
    return resolved


def _validate_cli_source_parent(repo_root: Path, checkpoint: str, tree: str) -> None:
    if _SHA40.fullmatch(checkpoint) is None or _SHA40.fullmatch(tree) is None:
        raise StageGateError("cli_source_parent_identity_invalid")
    try:
        actual_checkpoint = _git_text(repo_root, "rev-parse", f"{checkpoint}^{{commit}}")
        actual_tree = _git_text(repo_root, "rev-parse", f"{checkpoint}^{{tree}}")
    except (StageGateError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise StageGateError("cli_source_parent_not_found") from exc
    if actual_checkpoint != checkpoint or actual_tree != tree:
        raise StageGateError("cli_source_parent_tree_drift")


def _canonical_binding_stdout(binding: Mapping[str, Any]) -> str:
    return json.dumps(
        _native(binding), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def _parse_cli(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare or describe a sealed synthetic Ray R6 stage-gate package.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare")
    prepare.add_argument("--repo-root", required=True)
    prepare.add_argument("--source-parent-checkpoint", required=True)
    prepare.add_argument("--source-parent-tree", required=True)
    prepare.add_argument("--package-root", required=True)
    describe = commands.add_parser("describe")
    describe.add_argument("--repo-root", required=True)
    describe.add_argument("--package-root", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = _parse_cli(argv)
        repo_root = _canonical_cli_repo_root(args.repo_root)
        if args.command == "prepare":
            package_root = _canonical_cli_package_root(
                args.package_root, must_exist=False,
            )
            _validate_cli_source_parent(
                repo_root,
                args.source_parent_checkpoint,
                args.source_parent_tree,
            )
            value = build_stage_gate_input(
                repo_root=repo_root,
                source_checkpoint=args.source_parent_checkpoint,
                source_tree=args.source_parent_tree,
                output_root=package_root,
            )
            gate = evaluate_stage_gate(value, repo_root=repo_root)
            persist_stage_gate_package(
                value, repo_root=repo_root, evaluated_gate=gate,
            )
            package = replay_stage_gate_package(package_root, repo_root=repo_root)
        else:
            package_root = _canonical_cli_package_root(
                args.package_root, must_exist=True,
            )
            package = replay_stage_gate_package(package_root, repo_root=repo_root)
        print(_canonical_binding_stdout(stage_gate_package_binding(package)))
        return 0
    except (StageGateError, provenance.ProvenanceIOError, OSError, ValueError) as exc:
        print(getattr(exc, "code", type(exc).__name__), file=sys.stderr)
        return 1


__all__ = [
    "ALLOWED_CODE_CHILD_PATHS", "ALLOWED_CODE_CHILD_SUBJECT",
    "COMMITTED_SOURCE_ATTESTATION_SCHEMA", "CommittedSourceAttestation",
    "CONTRACT_ID", "EXPECTED_ARTIFACTS", "EXPECTED_SOURCE_PATHS",
    "FORMAL_ROOT_BASENAME_REGEX", "FORMAL_ROOT_PARENT", "FUTURE_ACTIVATION_SCHEMA",
    "FUTURE_TASK_ID", "PACKAGE_BINDING_SCHEMA", "PASS_STATUS", "PLAN_BOUND_AUTHORITY_SCHEMA",
    "RUNTIME_TEMPLATE_STATUS", "SourceReference", "StageGateError",
    "StageGateInput", "TASK_ID", "build_launch_descriptor",
    "build_runtime_plan_template", "build_stage_gate_input",
    "evaluate_stage_gate", "main", "materialize_runtime_plan",
    "materialized_runtime_plan_sha256", "persist_stage_gate_package",
    "replay_stage_gate_package", "runtime_plan_template_sha256",
    "stage_gate_package_binding",
    "validate_future_activation", "validate_launch_descriptor",
    "validate_committed_source_attestation",
    "validate_materialized_runtime_plan", "validate_runtime_plan_template",
    "validate_stage_gate",
]


if __name__ == "__main__":
    raise SystemExit(main())
