"""Pure Guide-4 E2 preformal integration and non-authorizing evidence."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


__all__ = [
    "ArtifactReference",
    "E2ContractError",
    "E2Input",
    "E2Package",
    "PrerequisiteReference",
    "SourceReference",
    "evaluate_e2_preformal_gate",
    "frozen_e2_input",
    "persist_e2_package",
    "replay_e2_package",
]


INPUT_SCHEMA = "g4_e2_preformal_input_v1"
RESULT_SCHEMA = "g4_e2_preformal_gate_result_v1"
TERMINAL_SCHEMA = "g4_e2_preformal_terminal_v1"
REPLAY_SCHEMA = "g4_e2_preformal_replay_v1"
RESULT_NAME = "preformal-gate-result.json"
TERMINAL_NAME = "terminal-seal.json"
ARTIFACT_NAMES = (RESULT_NAME, TERMINAL_NAME)
PASS_STATUS = "offline_preformal_contract_pass_waiting_planner_review"
SUCCESS_TERMINAL_STATUS = "sealed_offline_preformal_contract_pass_waiting_planner_review"
OUTPUT_ROOT_PARENT = "/Volumes/4T/temp/rgbww-optimizer"
OUTPUT_ROOT_BASENAME = re.compile(
    r"g4-e2-preformal-([0-9a-f]{12})-([0-9]{8}T[0-9]{6}Z)\Z"
)
SOURCE_IDENTITY = re.compile(r"[0-9a-f]{40}\Z")
GUARD_KEYS = (
    "frozen_input_exact",
    "g4_01_release_accepted_unconsumed",
    "g4_02_predevice_accepted",
    "g4_03_effect_confirmed_transport_ambiguous",
    "ray_only_capture_order_exact",
    "state_shutters_exact",
    "formal_plan_non_executable",
    "formal_budget_exact",
    "failure_contract_exact",
    "operating_600_transient_not_steady",
    "downstream_locks_preserved",
    "retained_r3_unvalidated_unconsumed",
    "release_consumption_false",
    "device_formal_td_c_authority_false",
)
AUTHORITY_FALSE_KEYS = (
    "execution_authorized",
    "human_authorization",
    "formal_pass",
    "hardware_ready",
    "release_consumed",
    "g4_06_unlocked",
)
AUTHORITY_ZERO_KEYS = (
    "release_consumption",
    "device_access",
    "formal_r6_access",
    "td_c_access",
    "capture_count",
)


class E2ContractError(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        primary: BaseException | None = None,
        seal_failure: BaseException | None = None,
    ) -> None:
        self.code = code
        self.primary = primary
        self.seal_failure = seal_failure
        super().__init__(code)


@dataclass(frozen=True)
class ArtifactReference:
    name: str
    byte_count: int
    sha256: str


@dataclass(frozen=True)
class SourceReference:
    path: str
    byte_count: int
    sha256: str


@dataclass(frozen=True)
class PrerequisiteReference:
    root_path: str
    artifacts: tuple[ArtifactReference, ...]
    disposition: str


@dataclass(frozen=True)
class E2Input:
    schema: str
    source_checkpoint: str
    source_tree: str
    guide: SourceReference
    policy: SourceReference
    policy_status: str
    g4_01: PrerequisiteReference
    g4_01_source_head: str
    g4_01_source_tree: str
    g4_01_canonical_validator_success: bool
    g4_01_eligibility: bool
    g4_01_release_consumable: bool
    g4_01_release_consumption_authorized: bool
    g4_02: PrerequisiteReference
    g4_03: PrerequisiteReference
    g4_03_review_plan: SourceReference
    g4_03_review_result: SourceReference
    g4_03_owner: SourceReference
    g4_03_tests: SourceReference
    g4_03_wrapper: SourceReference
    g4_03_classification: str
    g4_03_request_transport_success: bool
    g4_03_request_transport_exit: int
    g4_03_request_error_code: int
    g4_03_final_residual: int
    protected_sources: tuple[SourceReference, ...]
    retained_r3_status: str
    release_consumption_authorized: bool
    device_authorized: bool
    formal_r6_authorized: bool
    td_c_authorized: bool
    output_root: str


@dataclass(frozen=True)
class E2Package:
    root: provenance.DirectoryIdentity
    result: provenance.FileIdentity
    terminal: provenance.FileIdentity
    replay: Mapping[str, Any]


def _artifact(name: str, byte_count: int, sha256: str) -> ArtifactReference:
    return ArtifactReference(name, byte_count, sha256)


def _source(path: str, byte_count: int, sha256: str) -> SourceReference:
    return SourceReference(path, byte_count, sha256)


def _validate_output_root(value: object) -> str:
    """Validate one canonical direct child without touching the filesystem."""

    if type(value) is not str or not value:
        raise E2ContractError("invalid_output_root")
    if "\\" in value or any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise E2ContractError("invalid_output_root")
    parent, separator, basename = value.rpartition("/")
    if separator != "/" or parent != OUTPUT_ROOT_PARENT or not basename:
        raise E2ContractError("invalid_output_root")
    path = Path(value)
    if not path.is_absolute() or str(path) != value:
        raise E2ContractError("invalid_output_root")
    match = OUTPUT_ROOT_BASENAME.fullmatch(basename)
    if match is None:
        raise E2ContractError("invalid_output_root")
    timestamp = match.group(2)
    try:
        parsed = datetime.strptime(timestamp, "%Y%m%dT%H%M%SZ")
    except ValueError as error:
        raise E2ContractError("invalid_output_root", primary=error) from error
    if parsed.strftime("%Y%m%dT%H%M%SZ") != timestamp:
        raise E2ContractError("invalid_output_root")
    return value


def _validate_source_identity(value: object, *, code: str) -> str:
    """Validate one explicit Git-shaped identity without consulting Git."""

    if type(value) is not str or SOURCE_IDENTITY.fullmatch(value) is None:
        raise E2ContractError(code)
    return value


def frozen_e2_input(
    *,
    output_root: str,
    source_checkpoint: str,
    source_tree: str,
) -> E2Input:
    """Return the exact machine-row references without reading their targets."""

    output_root = _validate_output_root(output_root)
    source_checkpoint = _validate_source_identity(
        source_checkpoint, code="invalid_source_checkpoint",
    )
    source_tree = _validate_source_identity(source_tree, code="invalid_source_tree")

    return E2Input(
        schema=INPUT_SCHEMA,
        source_checkpoint=source_checkpoint,
        source_tree=source_tree,
        guide=_source(
            "advisor/4/4.GUIDE.md", 22702,
            "659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35",
        ),
        policy=_source(
            "config/hsi/p7-ray-td-b-exposure-policy-v2.json", 4065,
            "c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681",
        ),
        policy_status="qualified_1_2500",
        g4_01=PrerequisiteReference(
            "/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release",
            (
                _artifact("frozen-inputs.json", 5047, "8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8"),
                _artifact("r6-formal-plan.json", 899, "dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b"),
                _artifact("release-descriptor.json", 2024, "6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452"),
                _artifact("validation-summary.json", 432, "07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07"),
                _artifact("terminal-seal.json", 808, "d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850"),
            ),
            "ACCEPTED_ELIGIBLE_CONSUMABLE_UNCONSUMED",
        ),
        g4_01_source_head="779c7d9572d991f82076c892ec8198a059bbe44e",
        g4_01_source_tree="1ead5268917612d1232543b1a7eca28788f3980c",
        g4_01_canonical_validator_success=True,
        g4_01_eligibility=True,
        g4_01_release_consumable=True,
        g4_01_release_consumption_authorized=False,
        g4_02=PrerequisiteReference(
            "/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z",
            (
                _artifact("predevice-oracle-result.json", 3186, "78fa982b7f318734afc158324b968ee71ff41b5ce7b91e27d6eabc0f60bc40d9"),
                _artifact("terminal-seal.json", 1114, "39456ca3379df45cae0ca5337bf6d24d2040e6581dcd074b8ebf12d39b87e68e"),
            ),
            "ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED",
        ),
        g4_03=PrerequisiteReference(
            "/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-d957a89a84d3-20260803T200550Z",
            (_artifact("terminal-seal.json", 2936, "c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d"),),
            "ACCEPTED_G4_03_ZERO_READINESS_WITH_REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN",
        ),
        g4_03_review_plan=_source(
            ".agent-work/archived/PLAN-20260803-1436.md", 11600,
            "bdb9666ccda837123c2461df8f2e3bedd725ab1d941fdc6439e4aa7c0e8c82e8",
        ),
        g4_03_review_result=_source(
            ".agent-work/archived/EXECUTION_RESULT-20260803-1436.md", 11039,
            "9c39787d61a36c403887f41b59f47f7016437226286339237c187ae147708b5f",
        ),
        g4_03_owner=_source(
            "src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py", 36066,
            "ba326702ad53aba06eeef2c12a86753c31bbeaa65bed78139dc777f2047d9193",
        ),
        g4_03_tests=_source(
            "tests/test_p7_successor_zero_readiness.py", 25654,
            "6bbee82e8e61a65aada750e7d5b74d30157d38b61c8edec4b7d20bd907d1a2dd",
        ),
        g4_03_wrapper=_source(
            "tmp/run-g4-zero-readiness.zsh", 2969,
            "13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a",
        ),
        g4_03_classification="REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN",
        g4_03_request_transport_success=False,
        g4_03_request_transport_exit=1,
        g4_03_request_error_code=-128,
        g4_03_final_residual=0,
        protected_sources=(
            _source("src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py", 203416, "14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1"),
            _source("src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py", 188493, "a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47"),
            _source("src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py", 97644, "8e68400d51d01a20f4629aec7ad17c084835d7242e1cfba73a0335916209fa03"),
            _source("src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py", 26438, "8485755619ee6cee11845ff0ca698a8fff0906ff42537b3039ce5b8358fc1555"),
            _source("src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py", 24232, "4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81"),
            _source("src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py", 27938, "38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608"),
            _source("tmp/run-p7-thermal-diagnostics.zsh", 4070, "2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5"),
        ),
        retained_r3_status="RETAINED_UNVALIDATED_UNCONSUMED",
        release_consumption_authorized=False,
        device_authorized=False,
        formal_r6_authorized=False,
        td_c_authorized=False,
        output_root=output_root,
    )


def _valid_sha(value: object) -> bool:
    return type(value) is str and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _validate_artifact(value: object) -> None:
    if (
        type(value) is not ArtifactReference
        or type(value.name) is not str
        or not value.name
        or "/" in value.name
        or "\\" in value.name
        or type(value.byte_count) is not int
        or value.byte_count <= 0
        or not _valid_sha(value.sha256)
    ):
        raise E2ContractError("invalid_artifact_reference")


def _validate_source(value: object) -> None:
    if (
        type(value) is not SourceReference
        or type(value.path) is not str
        or not value.path
        or Path(value.path).is_absolute()
        or "\\" in value.path
        or any(part in {"", ".", ".."} for part in value.path.split("/"))
        or type(value.byte_count) is not int
        or value.byte_count <= 0
        or not _valid_sha(value.sha256)
    ):
        raise E2ContractError("invalid_source_reference")


def _validate_prerequisite(value: object) -> None:
    if (
        type(value) is not PrerequisiteReference
        or type(value.root_path) is not str
        or not Path(value.root_path).is_absolute()
        or type(value.artifacts) is not tuple
        or type(value.disposition) is not str
        or not value.disposition
    ):
        raise E2ContractError("invalid_prerequisite_reference")
    for artifact in value.artifacts:
        _validate_artifact(artifact)
    names = tuple(artifact.name for artifact in value.artifacts)
    if len(set(names)) != len(names):
        raise E2ContractError("duplicate_prerequisite_artifact")


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _artifact_projection(value: ArtifactReference) -> dict[str, Any]:
    return {"name": value.name, "bytes": value.byte_count, "sha256": value.sha256}


def _source_projection(value: SourceReference) -> dict[str, Any]:
    return {"path": value.path, "bytes": value.byte_count, "sha256": value.sha256}


def _prerequisite_projection(value: PrerequisiteReference) -> dict[str, Any]:
    return {
        "root_path": value.root_path,
        "artifacts": [_artifact_projection(item) for item in value.artifacts],
        "disposition": value.disposition,
    }


def _reference_ledger(inputs: E2Input) -> dict[str, Any]:
    return {
        "output_root": inputs.output_root,
        "source_checkpoint": inputs.source_checkpoint,
        "source_tree": inputs.source_tree,
        "guide": _source_projection(inputs.guide),
        "policy": {**_source_projection(inputs.policy), "status": inputs.policy_status},
        "g4_01": _prerequisite_projection(inputs.g4_01),
        "g4_02": _prerequisite_projection(inputs.g4_02),
        "g4_03": {
            **_prerequisite_projection(inputs.g4_03),
            "classification": inputs.g4_03_classification,
            "request_transport_success": inputs.g4_03_request_transport_success,
            "request_transport_exit": inputs.g4_03_request_transport_exit,
            "request_error_code": inputs.g4_03_request_error_code,
            "final_residual": inputs.g4_03_final_residual,
        },
        "protected_sources": [_source_projection(item) for item in inputs.protected_sources],
    }


def _authority() -> dict[str, Any]:
    return {
        **{key: False for key in AUTHORITY_FALSE_KEYS},
        **{key: 0 for key in AUTHORITY_ZERO_KEYS},
    }


def _result_value(
    inputs: E2Input,
    formal_plan: Mapping[str, Any],
    machine_status: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": PASS_STATUS,
        "reference_ledger": _reference_ledger(inputs),
        "formal_plan": provenance.json_native_value(formal_plan),
        "machine_status": provenance.json_native_value(machine_status),
        "guards": {key: True for key in GUARD_KEYS},
        "authority": _authority(),
    }


def _require_exact_shape(actual: Any, expected: Any, *, code: str) -> None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping) or set(actual) != set(expected):
            raise E2ContractError(code)
        for key, expected_value in expected.items():
            _require_exact_shape(actual[key], expected_value, code=code)
        return
    if isinstance(expected, list):
        if type(actual) not in {list, tuple} or len(actual) != len(expected):
            raise E2ContractError(code)
        for actual_value, expected_value in zip(actual, expected, strict=True):
            _require_exact_shape(actual_value, expected_value, code=code)
        return
    if type(actual) is not type(expected) or actual != expected:
        raise E2ContractError(code)


def _existing_owner_value(
    owner: Callable[[], Mapping[str, Any]],
    *,
    code: str,
) -> Mapping[str, Any]:
    try:
        value = owner()
    except BaseException as error:
        raise E2ContractError(code, primary=error) from error
    if not isinstance(value, Mapping):
        raise E2ContractError(code)
    return value


def _validate_result_contract(
    result: Mapping[str, Any],
    inputs: E2Input,
    *,
    expected_plan: Mapping[str, Any] | None = None,
    expected_status: Mapping[str, Any] | None = None,
    build_plan_fn: Callable[[], Mapping[str, Any]] = thermal.build_td_b_r6_formal_plan,
    validate_plan_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_r6_formal_plan,
    machine_status_fn: Callable[[], Mapping[str, Any]] = thermal.td_b_r6_machine_status,
) -> Mapping[str, Any]:
    """Validate the one closed E2 result contract at every trust boundary."""

    _validate_exact_input(inputs)
    if not isinstance(result, Mapping):
        raise E2ContractError("result_contract_drift")
    try:
        native = provenance.json_native_value(result)
    except BaseException as error:
        raise E2ContractError("result_not_json_native", primary=error) from error
    if not isinstance(native, Mapping) or set(native) != {
        "schema", "status", "reference_ledger", "formal_plan",
        "machine_status", "guards", "authority",
    }:
        raise E2ContractError("result_contract_drift")
    plan = native.get("formal_plan")
    status = native.get("machine_status")
    if not isinstance(plan, Mapping) or not isinstance(status, Mapping):
        raise E2ContractError("result_contract_drift")
    try:
        validate_plan_fn(plan)
    except BaseException as error:
        raise E2ContractError("formal_plan_owner_rejected", primary=error) from error
    plan_owner_value = (
        expected_plan
        if expected_plan is not None
        else _existing_owner_value(build_plan_fn, code="formal_plan_owner_rejected")
    )
    status_owner_value = (
        expected_status
        if expected_status is not None
        else _existing_owner_value(machine_status_fn, code="machine_status_owner_rejected")
    )
    if not isinstance(plan_owner_value, Mapping) or not isinstance(status_owner_value, Mapping):
        raise E2ContractError("existing_owner_result_type_invalid")
    _require_exact_shape(plan, provenance.json_native_value(plan_owner_value), code="formal_plan_contract_drift")
    _require_exact_shape(status, provenance.json_native_value(status_owner_value), code="machine_status_contract_drift")
    expected = _result_value(inputs, plan_owner_value, status_owner_value)
    _require_exact_shape(native, expected, code="result_contract_drift")
    canonical = provenance.canonical_json_bytes(native)
    decoded = provenance.decode_canonical_json(canonical)
    _require_exact_shape(decoded, expected, code="result_canonical_projection_drift")
    return native


def _validate_exact_input(value: E2Input) -> None:
    if type(value) is not E2Input:
        raise E2ContractError("invalid_input_type")
    _validate_output_root(value.output_root)
    _validate_source_identity(
        value.source_checkpoint, code="invalid_source_checkpoint",
    )
    _validate_source_identity(value.source_tree, code="invalid_source_tree")
    for source in (
        value.guide, value.policy, value.g4_03_review_plan, value.g4_03_review_result,
        value.g4_03_owner, value.g4_03_tests, value.g4_03_wrapper,
    ):
        _validate_source(source)
    if type(value.protected_sources) is not tuple:
        raise E2ContractError("protected_sources_not_tuple")
    for source in value.protected_sources:
        _validate_source(source)
    for prerequisite in (value.g4_01, value.g4_02, value.g4_03):
        _validate_prerequisite(prerequisite)
    integer_fields = (
        value.g4_03_request_transport_exit, value.g4_03_request_error_code,
        value.g4_03_final_residual,
    )
    boolean_fields = (
        value.g4_01_canonical_validator_success, value.g4_01_eligibility,
        value.g4_01_release_consumable, value.g4_01_release_consumption_authorized,
        value.g4_03_request_transport_success, value.release_consumption_authorized,
        value.device_authorized, value.formal_r6_authorized, value.td_c_authorized,
    )
    if any(type(item) is not int for item in integer_fields):
        raise E2ContractError("input_integer_type_invalid")
    if any(type(item) is not bool for item in boolean_fields):
        raise E2ContractError("input_boolean_type_invalid")
    expected = frozen_e2_input(
        output_root=value.output_root,
        source_checkpoint=value.source_checkpoint,
        source_tree=value.source_tree,
    )
    if value != expected:
        raise E2ContractError("frozen_input_drift")


def evaluate_e2_preformal_gate(
    inputs: E2Input,
    *,
    build_plan_fn: Callable[[], Mapping[str, Any]] = thermal.build_td_b_r6_formal_plan,
    validate_plan_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_r6_formal_plan,
    machine_status_fn: Callable[[], Mapping[str, Any]] = thermal.td_b_r6_machine_status,
) -> Mapping[str, Any]:
    """Evaluate exact frozen references without reading any prerequisite root."""

    _validate_exact_input(inputs)
    plan = _existing_owner_value(build_plan_fn, code="formal_plan_owner_rejected")
    status = _existing_owner_value(machine_status_fn, code="machine_status_owner_rejected")
    result = _result_value(inputs, plan, status)
    _validate_result_contract(
        result,
        inputs,
        expected_plan=plan,
        expected_status=status,
        validate_plan_fn=validate_plan_fn,
    )
    return _freeze(result)


def _reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    return {
        "path": Path(identity.path).name,
        "device": identity.device,
        "inode": identity.inode,
        "mode": identity.mode,
        "bytes": identity.byte_count,
        "sha256": identity.sha256,
    }


def _fail_seal(code: str, result: provenance.FileIdentity | None) -> dict[str, Any]:
    return {
        "schema": TERMINAL_SCHEMA,
        "status": "offline_preformal_package_failed",
        "failure_code": code,
        "result": _reference(result) if result is not None else None,
        "terminal_self_reference": False,
        "retry": 0,
        "alternate_root": 0,
        "authority": {"execution_authorized": False, "formal_r6_access": 0, "capture_count": 0},
    }


def _success_terminal(result: provenance.FileIdentity) -> dict[str, Any]:
    return {
        "schema": TERMINAL_SCHEMA,
        "status": SUCCESS_TERMINAL_STATUS,
        "result": _reference(result),
        "artifact_count_before_terminal": 1,
        "terminal_self_reference": False,
        "retry": 0,
        "alternate_root": 0,
        "authority": {
            "execution_authorized": False,
            "formal_r6_access": 0,
            "capture_count": 0,
        },
    }


def _validate_success_terminal(
    terminal: Mapping[str, Any],
    result: provenance.FileIdentity,
) -> None:
    if not isinstance(terminal, Mapping):
        raise E2ContractError("replay_terminal_contract_drift")
    try:
        native = provenance.json_native_value(terminal)
    except BaseException as error:
        raise E2ContractError("replay_terminal_contract_drift", primary=error) from error
    _require_exact_shape(
        native,
        _success_terminal(result),
        code="replay_terminal_contract_drift",
    )


def persist_e2_package(
    inputs: E2Input,
    result: Mapping[str, Any],
    *,
    create_root_fn: Callable[[str], provenance.DirectoryIdentity] = provenance.create_exclusive_root,
    persist_fn: Callable[[provenance.DirectoryIdentity, str, Any], provenance.FileIdentity] = provenance.persist_canonical_json,
) -> E2Package:
    """Persist one exclusive two-artifact package and replay it once."""

    _validate_exact_input(inputs)
    _validate_result_contract(result, inputs)
    root = create_root_fn(inputs.output_root)
    if type(root) is not provenance.DirectoryIdentity or root.path != inputs.output_root:
        raise E2ContractError("created_root_identity_mismatch")
    result_identity: provenance.FileIdentity | None = None
    try:
        result_identity = persist_fn(root, RESULT_NAME, result)
    except BaseException as primary:
        try:
            persist_fn(root, TERMINAL_NAME, _fail_seal("result_persist_failed", None))
        except BaseException as seal_failure:
            raise E2ContractError(
                "result_persist_and_fail_seal_failed", primary=primary, seal_failure=seal_failure,
            ) from primary
        raise E2ContractError("result_persist_failed", primary=primary) from primary
    terminal_value = _success_terminal(result_identity)
    try:
        terminal_identity = persist_fn(root, TERMINAL_NAME, terminal_value)
    except BaseException as primary:
        try:
            terminal_identity = persist_fn(
                root, TERMINAL_NAME, _fail_seal("terminal_persist_failed", result_identity),
            )
        except BaseException as seal_failure:
            raise E2ContractError(
                "terminal_persist_and_fail_seal_failed", primary=primary, seal_failure=seal_failure,
            ) from primary
        raise E2ContractError("terminal_persist_failed", primary=primary) from primary
    replay = replay_e2_package(
        root.path,
        source_checkpoint=inputs.source_checkpoint,
        source_tree=inputs.source_tree,
    )
    return E2Package(root, result_identity, terminal_identity, replay)


def replay_e2_package(
    root_path: str | Path,
    *,
    source_checkpoint: str,
    source_tree: str,
) -> Mapping[str, Any]:
    """Independently replay one exact offline package through provenance I/O."""

    source_checkpoint = _validate_source_identity(
        source_checkpoint, code="invalid_source_checkpoint",
    )
    source_tree = _validate_source_identity(source_tree, code="invalid_source_tree")
    root = provenance.read_existing_root(str(Path(root_path)))
    inputs = frozen_e2_input(
        output_root=root.path,
        source_checkpoint=source_checkpoint,
        source_tree=source_tree,
    )
    if provenance.list_exact_regular_children(root) != ARTIFACT_NAMES:
        raise E2ContractError("package_inventory_drift")
    result_identity = provenance.read_exact_file(
        Path(root.path) / RESULT_NAME, expected_mode=0o600, root=root,
    )
    terminal_identity = provenance.read_exact_file(
        Path(root.path) / TERMINAL_NAME, expected_mode=0o600, root=root,
    )
    result = provenance.decode_canonical_json(result_identity.data)
    terminal = provenance.decode_canonical_json(terminal_identity.data)
    _validate_result_contract(result, inputs)
    _validate_success_terminal(terminal, result_identity)
    return _freeze({
        "schema": REPLAY_SCHEMA,
        "status": "pass",
        "root": {"path": root.path, "device": root.device, "inode": root.inode, "mode": root.mode},
        "result": _reference(result_identity),
        "terminal": _reference(terminal_identity),
        "execution_authorized": False,
    })
