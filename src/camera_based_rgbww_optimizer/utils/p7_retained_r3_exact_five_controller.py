"""Pure callback orchestration for a fail-closed exact-five preparation.

This module owns ordering and call cardinality only.  Candidate facts, real I/O,
and the canonical eligibility decision remain owned by injected callbacks.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import Callable, Mapping

from camera_based_rgbww_optimizer.utils.agent_work_machine_contract import (
    ParsedMachineContract,
)


__all__ = [
    "ExactFiveControllerError",
    "ExactFiveCandidateEntry",
    "ExactFiveControllerRequest",
    "ExactFiveControllerCallbacks",
    "PreparedExactFiveController",
    "prepare_exact_five_controller",
    "execute_prepared_exact_five_controller",
]


_LOWER_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_LOWER_BLOB_OID = re.compile(r"[0-9a-f]{40}\Z")
_SAFE_PATH = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+@/-]*\Z")
_SAFE_SCHEMA = re.compile(r"[a-z0-9][a-z0-9._-]*\Z")


class ExactFiveControllerError(RuntimeError):
    """A stable fail-closed controller error."""

    def __init__(self, code: str, *, phase: str = "prepare") -> None:
        self.code = code
        self.phase = phase
        super().__init__(f"{phase}:{code}")


def _require_exact_string(value: object, code: str) -> str:
    if type(value) is not str or not value:
        raise ExactFiveControllerError(code)
    return value


def _require_sha256(value: object, code: str) -> str:
    text = _require_exact_string(value, code)
    if _LOWER_SHA256.fullmatch(text) is None:
        raise ExactFiveControllerError(code)
    return text


def _require_blob_oid(value: object, code: str) -> str:
    text = _require_exact_string(value, code)
    if _LOWER_BLOB_OID.fullmatch(text) is None:
        raise ExactFiveControllerError(code)
    return text


def _validate_argv(value: object, code: str) -> None:
    if type(value) is not tuple or not value:
        raise ExactFiveControllerError(code)
    if any(type(part) is not str or not part or "\x00" in part for part in value):
        raise ExactFiveControllerError(code)


@dataclass(frozen=True)
class ExactFiveCandidateEntry:
    """One frozen repo-relative candidate entry."""

    repo_path: str
    expected_sha256: str
    after_blob_oid: str

    def __post_init__(self) -> None:
        path = _require_exact_string(self.repo_path, "invalid_repo_path")
        if (
            path.startswith("/")
            or "\\" in path
            or _SAFE_PATH.fullmatch(path) is None
            or any(part in {"", ".", ".."} for part in path.split("/"))
        ):
            raise ExactFiveControllerError("invalid_repo_path")
        _require_sha256(self.expected_sha256, "invalid_expected_sha256")
        _require_blob_oid(self.after_blob_oid, "invalid_after_blob_oid")


@dataclass(frozen=True)
class ExactFiveControllerRequest:
    """All immutable bindings needed by the exact-five state owner."""

    reference_task_id: str
    contract_id: str
    entries: tuple[ExactFiveCandidateEntry, ...]
    expected_parent: str
    expected_subject: str
    candidate_identity_sha256: str
    bootstrap_record_sha256: str
    bootstrap_seal_sha256: str
    import_static_argv: tuple[str, ...]
    targeted_test_argv: tuple[str, ...]
    focused_test_argv: tuple[str, ...]
    full_test_argv: tuple[str, ...]
    subordinate_manifest_schema: str

    def __post_init__(self) -> None:
        _require_exact_string(self.reference_task_id, "invalid_reference_task_id")
        _require_exact_string(self.contract_id, "invalid_contract_id")
        if type(self.entries) is not tuple or len(self.entries) != 5:
            raise ExactFiveControllerError("entry_count_not_five")
        if any(type(entry) is not ExactFiveCandidateEntry for entry in self.entries):
            raise ExactFiveControllerError("invalid_entry_type")
        paths = tuple(entry.repo_path for entry in self.entries)
        if len(set(paths)) != 5:
            raise ExactFiveControllerError("duplicate_entry_path")
        if paths != tuple(sorted(paths, key=lambda item: item.encode("utf-8"))):
            raise ExactFiveControllerError("entries_not_utf8_sorted")
        _require_blob_oid(self.expected_parent, "invalid_expected_parent")
        _require_exact_string(self.expected_subject, "invalid_expected_subject")
        if "\x00" in self.expected_subject or "\n" in self.expected_subject:
            raise ExactFiveControllerError("invalid_expected_subject")
        _require_sha256(self.candidate_identity_sha256, "invalid_candidate_identity")
        _require_sha256(self.bootstrap_record_sha256, "invalid_bootstrap_record_identity")
        _require_sha256(self.bootstrap_seal_sha256, "invalid_bootstrap_seal_identity")
        _validate_argv(self.import_static_argv, "invalid_import_static_argv")
        _validate_argv(self.targeted_test_argv, "invalid_targeted_test_argv")
        _validate_argv(self.focused_test_argv, "invalid_focused_test_argv")
        _validate_argv(self.full_test_argv, "invalid_full_test_argv")
        schema = _require_exact_string(
            self.subordinate_manifest_schema,
            "invalid_subordinate_manifest_schema",
        )
        if _SAFE_SCHEMA.fullmatch(schema) is None:
            raise ExactFiveControllerError("invalid_subordinate_manifest_schema")


AcquireCallback = Callable[[ExactFiveControllerRequest], bool]
MaterializeCallback = Callable[[ExactFiveCandidateEntry], bool]
ArgvGateCallback = Callable[[tuple[str, ...]], bool]
RequestCallback = Callable[[ExactFiveControllerRequest], bool]
ManifestCallback = Callable[[str], bool]
TerminalCallback = Callable[[Mapping[str, object]], bool]


@dataclass(frozen=True)
class ExactFiveControllerCallbacks:
    """Narrow callbacks; deliberately no consumer or emitter surface."""

    acquire: AcquireCallback
    materialize_one_entry: MaterializeCallback
    import_static_gate: ArgvGateCallback
    targeted_gate: ArgvGateCallback
    focused_gate: ArgvGateCallback
    full_gate: ArgvGateCallback
    single_commit: RequestCallback
    subordinate_manifest_seal: ManifestCallback
    canonical_validator: RequestCallback
    terminal_seal: TerminalCallback


@dataclass(frozen=True)
class PreparedExactFiveController:
    """Immutable validated controller input with canonical owner bindings."""

    request: ExactFiveControllerRequest
    plan_source_sha256: str
    full_source_sha256: str


def _require_mapping_value(
    mapping: Mapping[str, object], key: str, expected: object, code: str
) -> None:
    if mapping.get(key) != expected or type(mapping.get(key)) is not type(expected):
        raise ExactFiveControllerError(code)


def prepare_exact_five_controller(
    request: ExactFiveControllerRequest,
    plan: ParsedMachineContract,
    full: ParsedMachineContract,
) -> PreparedExactFiveController:
    """Validate canonical bindings without invoking any callback."""

    if type(request) is not ExactFiveControllerRequest:
        raise ExactFiveControllerError("invalid_request")
    if type(plan) is not ParsedMachineContract or plan.evidence.owner != "PLAN":
        raise ExactFiveControllerError("invalid_plan_contract")
    if type(full) is not ParsedMachineContract or full.evidence.owner != "FULL":
        raise ExactFiveControllerError("invalid_full_contract")

    plan_value = plan.value
    full_value = full.value
    _require_mapping_value(
        plan_value, "reference_task_id", request.reference_task_id, "plan_task_drift"
    )
    _require_mapping_value(plan_value, "contract_id", request.contract_id, "plan_contract_drift")
    _require_mapping_value(
        plan_value.get("activation_commit", {}),
        "expected_parent",
        request.expected_parent,
        "plan_parent_drift",
    )
    _require_mapping_value(
        plan_value.get("activation_commit", {}),
        "expected_subject",
        request.expected_subject,
        "plan_subject_drift",
    )
    _require_mapping_value(
        plan_value.get("candidate_contract", {}),
        "identity_sha256",
        request.candidate_identity_sha256,
        "plan_candidate_identity_drift",
    )
    _require_mapping_value(
        plan_value.get("candidate_contract", {}), "exact_entry_count", 5, "plan_entry_count_drift"
    )
    _require_mapping_value(
        plan_value.get("accepted_bootstrap", {}),
        "record_sha256",
        request.bootstrap_record_sha256,
        "plan_bootstrap_record_drift",
    )
    _require_mapping_value(
        plan_value.get("accepted_bootstrap", {}),
        "seal_sha256",
        request.bootstrap_seal_sha256,
        "plan_bootstrap_seal_drift",
    )

    _require_mapping_value(full_value, "active_task_count", 1, "full_active_count_drift")
    _require_mapping_value(
        full_value, "active_task", request.reference_task_id, "full_task_drift"
    )
    _require_mapping_value(
        full_value,
        "active_plan_contract_id",
        request.contract_id,
        "full_contract_drift",
    )
    _require_mapping_value(
        full_value,
        "retained_r3_status",
        "RETAINED_UNVALIDATED_UNCONSUMED",
        "full_retained_status_drift",
    )
    _require_mapping_value(
        full_value,
        "candidate_machine_contract_sha256",
        request.candidate_identity_sha256,
        "full_candidate_identity_drift",
    )
    _require_mapping_value(
        full_value,
        "candidate_contract_orchestrator_verified",
        True,
        "full_candidate_verified_drift",
    )
    return PreparedExactFiveController(
        request=request,
        plan_source_sha256=plan.evidence.source_sha256,
        full_source_sha256=full.evidence.source_sha256,
    )


def _terminal_payload(
    *,
    status: str,
    failed_phase: str | None,
    results: Mapping[str, bool],
    counts: Mapping[str, int],
) -> Mapping[str, object]:
    return MappingProxyType(
        {
            "schema": "exact-five-controller-terminal-v1",
            "status": status,
            "failed_phase": failed_phase,
            "callback_results": MappingProxyType(dict(results)),
            "callback_counts": MappingProxyType(dict(counts)),
        }
    )


def execute_prepared_exact_five_controller(
    prepared: PreparedExactFiveController,
    callbacks: ExactFiveControllerCallbacks,
) -> Mapping[str, object]:
    """Execute the fixed sequence once, terminal-sealing success or failure."""

    if type(prepared) is not PreparedExactFiveController:
        raise ExactFiveControllerError("not_prepared", phase="execute")
    if type(callbacks) is not ExactFiveControllerCallbacks:
        raise ExactFiveControllerError("invalid_callbacks", phase="execute")

    names = (
        "acquire",
        "materialize_one_entry",
        "import_static_gate",
        "targeted_gate",
        "focused_gate",
        "full_gate",
        "single_commit",
        "subordinate_manifest_seal",
        "canonical_validator",
        "terminal_seal",
    )
    counts = {name: 0 for name in names}
    results: dict[str, bool] = {}

    def seal(status: str, failed_phase: str | None) -> Mapping[str, object]:
        payload = _terminal_payload(
            status=status,
            failed_phase=failed_phase,
            results=results,
            counts={**counts, "terminal_seal": 1},
        )
        counts["terminal_seal"] += 1
        callback = callbacks.terminal_seal
        if not callable(callback):
            raise ExactFiveControllerError("missing_callback", phase="terminal_seal")
        try:
            raw = callback(payload)
        except Exception as exc:
            raise ExactFiveControllerError("callback_exception", phase="terminal_seal") from exc
        if type(raw) is not bool or raw is not True:
            raise ExactFiveControllerError("callback_non_pass", phase="terminal_seal")
        results["terminal_seal"] = raw
        return payload

    def run(phase: str, callback: object, argument: object) -> bool:
        if not callable(callback):
            seal("FAIL", phase)
            raise ExactFiveControllerError("missing_callback", phase=phase)
        counts[phase] += 1
        try:
            raw = callback(argument)
        except Exception as exc:
            seal("FAIL", phase)
            raise ExactFiveControllerError("callback_exception", phase=phase) from exc
        if type(raw) is not bool:
            seal("FAIL", phase)
            raise ExactFiveControllerError("callback_result_not_exact_bool", phase=phase)
        results[phase] = raw
        if raw is not True:
            seal("FAIL", phase)
            raise ExactFiveControllerError("callback_non_pass", phase=phase)
        return raw

    request = prepared.request
    run("acquire", callbacks.acquire, request)
    for entry in request.entries:
        run("materialize_one_entry", callbacks.materialize_one_entry, entry)
    run("import_static_gate", callbacks.import_static_gate, request.import_static_argv)
    run("targeted_gate", callbacks.targeted_gate, request.targeted_test_argv)
    run("focused_gate", callbacks.focused_gate, request.focused_test_argv)
    run("full_gate", callbacks.full_gate, request.full_test_argv)
    run("single_commit", callbacks.single_commit, request)
    run(
        "subordinate_manifest_seal",
        callbacks.subordinate_manifest_seal,
        request.subordinate_manifest_schema,
    )
    run("canonical_validator", callbacks.canonical_validator, request)
    return seal("PASS", None)
