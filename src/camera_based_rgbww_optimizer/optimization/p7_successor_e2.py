"""Pure Guide-4 E2 preformal integration and non-authorizing evidence."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
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
EXPECTED_OUTPUT_ROOT = "/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-4995f7d65141-20260803T204648Z"
EXPECTED_CAPTURE_IDS = (
    "000-ray-a0-t600", "001-ray-d-t60", "002-ray-d-t120", "003-ray-d-t300",
    "004-ray-d-t600", "005-ray-a-after-d-t600", "006-ray-b-t60",
    "007-ray-b-t120", "008-ray-b-t300", "009-ray-b-t600",
    "010-ray-a-after-b-t600", "011-ray-c-t60", "012-ray-c-t120",
    "013-ray-c-t300", "014-ray-c-t600", "015-ray-a-after-c-t600",
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


def frozen_e2_input() -> E2Input:
    """Return the exact machine-row references without reading their targets."""

    return E2Input(
        schema=INPUT_SCHEMA,
        source_checkpoint="4995f7d65141ce8a4086d74f9add21c5b44d593d",
        source_tree="da458ce4a81344397354a8535e8a38cef5d59375",
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
        output_root=EXPECTED_OUTPUT_ROOT,
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


def _validate_exact_input(value: E2Input) -> None:
    if type(value) is not E2Input:
        raise E2ContractError("invalid_input_type")
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
    expected = frozen_e2_input()
    if value != expected:
        raise E2ContractError("frozen_input_drift")
    if not Path(value.output_root).is_absolute():
        raise E2ContractError("output_root_not_absolute")


def _validate_formal_plan(plan: Mapping[str, Any]) -> None:
    expected_keys = {
        "schema", "status", "executable", "experiment_id", "source", "strip",
        "ambient", "formal_logical", "formal_physical_cap", "setup_in_formal_root",
        "launch", "retry", "capture_ids", "state_shutters", "c_policy_status",
        "old_new_frame_combination", "failure_contract",
    }
    if set(plan) != expected_keys:
        raise E2ContractError("formal_plan_open_or_missing_schema")
    exact = {
        "schema": "p7_td_b_ray_r6_formal_plan_v1",
        "status": "selected_exposure_policy_non_executable",
        "executable": False,
        "experiment_id": "P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6",
        "source": "ray",
        "strip": "zero_throughout",
        "ambient": 0,
        "formal_logical": 16,
        "formal_physical_cap": 16,
        "setup_in_formal_root": 0,
        "launch": 1,
        "retry": 0,
        "capture_ids": list(EXPECTED_CAPTURE_IDS),
        "state_shutters": {"A": "1/5000", "D": "1/6400", "B": "1/8000", "C": "1/2500"},
        "c_policy_status": "qualified",
        "old_new_frame_combination": "prohibited",
        "failure_contract": {
            "classification": "accepted_hard_failed_formal_attempt",
            "formal_pass": False,
            "strip_call_count": 0,
            "retry": 0,
        },
    }
    if dict(plan) != exact:
        raise E2ContractError("formal_plan_contract_drift")


def _validate_machine_status(status: Mapping[str, Any]) -> None:
    try:
        envelope = status["operating_envelope"]
        locks = status["locks"]
        ray = status["ray_r6"]
    except (KeyError, TypeError) as error:
        raise E2ContractError("machine_status_missing") from error
    if (
        set(status) != {"r5", "exposure_qualification", "ray_r6", "operating_envelope", "locks"}
        or dict(envelope) != {
            "dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "steady_status": "not_demonstrated",
        }
        or dict(locks) != {
            "strip": "blocked_until_ray_r6_pass",
            "td_c": "blocked_until_combined_td_b_pass",
            "sentinel": True,
            "p8": True,
        }
        or dict(ray) != {
            "formal_planned": 16,
            "formal_accepted": 0,
            "retry": 0,
            "return_anchor_history": "not_evaluated",
        }
    ):
        raise E2ContractError("machine_status_contract_drift")


def evaluate_e2_preformal_gate(
    inputs: E2Input,
    *,
    build_plan_fn: Callable[[], Mapping[str, Any]] = thermal.build_td_b_r6_formal_plan,
    validate_plan_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_r6_formal_plan,
    machine_status_fn: Callable[[], Mapping[str, Any]] = thermal.td_b_r6_machine_status,
) -> Mapping[str, Any]:
    """Evaluate exact frozen references without reading any prerequisite root."""

    _validate_exact_input(inputs)
    plan = build_plan_fn()
    validate_plan_fn(plan)
    status = machine_status_fn()
    if not isinstance(plan, Mapping) or not isinstance(status, Mapping):
        raise E2ContractError("existing_owner_result_type_invalid")
    _validate_formal_plan(plan)
    _validate_machine_status(status)
    guards = {
        "frozen_input_exact": True,
        "g4_01_release_accepted_unconsumed": True,
        "g4_02_predevice_accepted": True,
        "g4_03_effect_confirmed_transport_ambiguous": True,
        "ray_only_capture_order_exact": True,
        "state_shutters_exact": True,
        "formal_plan_non_executable": True,
        "formal_budget_exact": True,
        "failure_contract_exact": True,
        "operating_600_transient_not_steady": True,
        "downstream_locks_preserved": True,
        "retained_r3_unvalidated_unconsumed": True,
        "release_consumption_false": True,
        "device_formal_td_c_authority_false": True,
    }
    result = {
        "schema": RESULT_SCHEMA,
        "status": PASS_STATUS,
        "reference_ledger": {
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
        },
        "formal_plan": provenance.json_native_value(plan),
        "machine_status": provenance.json_native_value(status),
        "guards": guards,
        "authority": {
            "execution_authorized": False,
            "human_authorization": False,
            "formal_pass": False,
            "hardware_ready": False,
            "release_consumed": False,
            "g4_06_unlocked": False,
            "release_consumption": 0,
            "device_access": 0,
            "formal_r6_access": 0,
            "td_c_access": 0,
            "capture_count": 0,
        },
    }
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


def persist_e2_package(
    inputs: E2Input,
    result: Mapping[str, Any],
    *,
    create_root_fn: Callable[[str], provenance.DirectoryIdentity] = provenance.create_exclusive_root,
    persist_fn: Callable[[provenance.DirectoryIdentity, str, Any], provenance.FileIdentity] = provenance.persist_canonical_json,
    replay_fn: Callable[[str | Path], Mapping[str, Any]] | None = None,
) -> E2Package:
    """Persist one exclusive two-artifact package and replay it once."""

    _validate_exact_input(inputs)
    if not isinstance(result, Mapping) or provenance.json_native_value(result).get("status") != PASS_STATUS:
        raise E2ContractError("result_not_accepted_for_persistence")
    root = create_root_fn(inputs.output_root)
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
    terminal_value = {
        "schema": TERMINAL_SCHEMA,
        "status": "sealed_offline_preformal_contract_pass_waiting_planner_review",
        "result": _reference(result_identity),
        "artifact_count_before_terminal": 1,
        "terminal_self_reference": False,
        "retry": 0,
        "alternate_root": 0,
        "authority": {"execution_authorized": False, "formal_r6_access": 0, "capture_count": 0},
    }
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
    replay_owner = replay_fn or replay_e2_package
    replay = replay_owner(root.path)
    return E2Package(root, result_identity, terminal_identity, replay)


def replay_e2_package(root_path: str | Path) -> Mapping[str, Any]:
    """Independently replay one exact offline package through provenance I/O."""

    root = provenance.read_existing_root(str(Path(root_path)))
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
    if (
        result.get("schema") != RESULT_SCHEMA
        or result.get("status") != PASS_STATUS
        or not all(result.get("guards", {}).values())
        or result.get("authority", {}).get("execution_authorized") is not False
        or result.get("formal_plan", {}).get("executable") is not False
    ):
        raise E2ContractError("replay_result_contract_drift")
    if (
        terminal.get("schema") != TERMINAL_SCHEMA
        or terminal.get("status") != "sealed_offline_preformal_contract_pass_waiting_planner_review"
        or terminal.get("result") != _reference(result_identity)
        or terminal.get("artifact_count_before_terminal") != 1
        or terminal.get("terminal_self_reference") is not False
        or terminal.get("retry") != 0
        or terminal.get("alternate_root") != 0
    ):
        raise E2ContractError("replay_terminal_contract_drift")
    return _freeze({
        "schema": REPLAY_SCHEMA,
        "status": "pass",
        "root": {"path": root.path, "device": root.device, "inode": root.inode, "mode": root.mode},
        "result": _reference(result_identity),
        "terminal": _reference(terminal_identity),
        "execution_authorized": False,
    })
