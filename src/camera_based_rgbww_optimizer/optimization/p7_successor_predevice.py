"""Pure-offline predevice oracle for one frozen Guide 4 successor bundle."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_successor_lineage as successor
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


__all__ = [
    "ArtifactExpectation",
    "EVIDENCE_ARTIFACT_NAMES",
    "PredeviceEvidencePackage",
    "PredeviceExpectation",
    "SuccessorPredeviceError",
    "evaluate_successor_predevice",
    "persist_successor_predevice_evidence",
    "replay_successor_predevice_evidence",
]

_SHA40 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
EVIDENCE_ARTIFACT_NAMES = ("predevice-oracle-result.json", "terminal-seal.json")
_FALSE_EFFECTIVE_AUTHORITY = {
    "canonical_validator_success": False,
    "eligibility": False,
    "release_consumable": False,
    "release_consumption_authorized": False,
    "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
    "device_authorized": False,
    "camera_authorized": False,
    "ray_authorized": False,
    "strip_authorized": False,
    "capture_authorized": False,
    "formal_r6_authorized": False,
    "td_c_authorized": False,
}


class SuccessorPredeviceError(RuntimeError):
    """A fail-closed error at the predevice composition boundary."""

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
class ArtifactExpectation:
    name: str
    byte_count: int
    sha256: str


@dataclass(frozen=True)
class PredeviceExpectation:
    bundle_path: str
    bundle_device: int
    bundle_inode: int
    bundle_mode: int
    artifacts: tuple[ArtifactExpectation, ...]
    source_repository_path: str
    source_head: str
    source_tree: str
    policy_path: str
    policy_byte_count: int
    policy_sha256: str
    eq_root: str
    eq_manifest_bytes: int
    eq_manifest_sha256: str


@dataclass(frozen=True)
class PredeviceEvidencePackage:
    root: provenance.DirectoryIdentity
    result: provenance.FileIdentity
    terminal: provenance.FileIdentity


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise SuccessorPredeviceError(code)


def _validate_expectation(value: PredeviceExpectation) -> None:
    _require(type(value) is PredeviceExpectation, "expectation_invalid")
    _require(
        Path(value.bundle_path).is_absolute()
        and value.bundle_mode == 0o700
        and type(value.bundle_device) is int
        and type(value.bundle_inode) is int,
        "bundle_expectation_invalid",
    )
    _require(
        tuple(item.name for item in value.artifacts) == successor.ARTIFACT_NAMES
        and all(
            type(item) is ArtifactExpectation
            and type(item.byte_count) is int
            and item.byte_count > 0
            and _SHA256.fullmatch(item.sha256) is not None
            for item in value.artifacts
        ),
        "artifact_expectation_invalid",
    )
    _require(
        Path(value.source_repository_path).is_absolute()
        and _SHA40.fullmatch(value.source_head) is not None
        and _SHA40.fullmatch(value.source_tree) is not None,
        "source_expectation_invalid",
    )
    _require(
        Path(value.policy_path).is_absolute()
        and type(value.policy_byte_count) is int
        and value.policy_byte_count > 0
        and _SHA256.fullmatch(value.policy_sha256) is not None,
        "policy_expectation_invalid",
    )
    _require(
        Path(value.eq_root).is_absolute()
        and type(value.eq_manifest_bytes) is int
        and value.eq_manifest_bytes > 0
        and _SHA256.fullmatch(value.eq_manifest_sha256) is not None,
        "eq_expectation_invalid",
    )


def _reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    return {
        "path": Path(identity.path).name,
        "bytes": identity.byte_count,
        "sha256": identity.sha256,
    }


def _identity_reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    _require(type(identity) is provenance.FileIdentity, "evidence_identity_invalid")
    return {
        **_reference(identity),
        "device": identity.device,
        "inode": identity.inode,
        "mode": identity.mode,
    }


def _root_reference(root: provenance.DirectoryIdentity) -> dict[str, Any]:
    _require(type(root) is provenance.DirectoryIdentity, "evidence_root_invalid")
    return {
        "path": root.path,
        "device": root.device,
        "inode": root.inode,
        "mode": root.mode,
    }


def _exact_keys(value: Any, expected: set[str], code: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping) and set(value) == expected, code)
    return value


def _validate_result(value: Mapping[str, Any]) -> dict[str, Any]:
    result = provenance.json_native_value(value)
    _exact_keys(result, {
        "schema", "status", "validations", "release", "artifacts", "source",
        "policy", "eq", "r6", "operational", "locks",
        "proposed_current_route_state", "effective_authority",
    }, "evidence_result_open_schema")
    validations = _exact_keys(result["validations"], {
        "public", "final_replay", "strict", "lineage", "call_counts",
    }, "evidence_validations_open_schema")
    _require(
        result["schema"] == "g4_successor_predevice_oracle_v1"
        and result["status"] == "pass"
        and validations == {
            "public": "public_descriptor_semantic_pass",
            "final_replay": "pass",
            "strict": "pass",
            "lineage": "pass",
            "call_counts": {"public": 1, "final": 1, "strict": 1},
        },
        "evidence_validation_drift",
    )
    nested_keys = {
        "release": {"path", "device", "inode", "mode", "artifact_count"},
        "source": {
            "repository", "head", "checkpoint", "tree", "staged", "unstaged",
            "untracked", "clean",
        },
        "policy": {"path", "bytes", "sha256"},
        "eq": {"root", "manifest_bytes", "manifest_sha256"},
        "r6": {
            "status", "executable", "capture_ids", "state_shutters", "formal_logical",
            "formal_physical_cap", "setup_in_formal_root", "ambient", "launch", "retry",
            "old_new_frame_combination",
        },
        "operational": {"dwell_s", "claim", "steady_status"},
        "locks": {"strip", "td_c", "sentinel", "p8"},
    }
    for name, keys in nested_keys.items():
        _exact_keys(result[name], keys, f"evidence_{name}_open_schema")
    _exact_keys(result["source"]["repository"], {
        "path", "device", "inode", "mode",
    }, "evidence_repository_open_schema")
    artifacts = result["artifacts"]
    _require(type(artifacts) is list and len(artifacts) == 5, "evidence_artifacts_drift")
    for expected_name, artifact in zip(successor.ARTIFACT_NAMES, artifacts):
        row = _exact_keys(artifact, {"path", "bytes", "sha256"}, "evidence_artifact_open_schema")
        _require(
            row["path"] == expected_name
            and type(row["bytes"]) is int
            and row["bytes"] > 0
            and type(row["sha256"]) is str
            and _SHA256.fullmatch(row["sha256"]) is not None,
            "evidence_artifact_drift",
        )
    _require(result["proposed_current_route_state"] == {
        "canonical_validator_success": True,
        "eligibility": True,
        "release_consumable": True,
        "release_consumption_authorized": False,
        "scope": "exact_g4_01_release_only_waiting_planner_and_orchestrator",
    }, "evidence_proposal_drift")
    _require(result["effective_authority"] == _FALSE_EFFECTIVE_AUTHORITY, "evidence_authority_drift")
    return result


def evaluate_successor_predevice(
    expectation: PredeviceExpectation,
    *,
    read_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.read_existing_root,
    inventory_fn: Callable[..., Sequence[str]] = provenance.list_exact_regular_children,
    read_file_fn: Callable[..., provenance.FileIdentity] = provenance.read_exact_file,
    same_target_fn: Callable[..., provenance.FileIdentity] = provenance.require_same_target,
    decode_fn: Callable[[bytes], Any] = provenance.decode_canonical_json,
    public_validator_fn: Callable[..., Mapping[str, Any]] = successor.validate_successor_lineage_release,
    replay_fn: Callable[..., Mapping[str, Any]] = successor.replay_successor_lineage_bundle,
    strict_validator_fn: Callable[..., Mapping[str, Any]] = successor.strict_validate_successor_lineage_bundle,
    validate_policy_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_exposure_policy_v2,
    validate_r6_plan_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_r6_formal_plan,
    machine_status_fn: Callable[[], Mapping[str, Any]] = thermal.td_b_r6_machine_status,
) -> dict[str, Any]:
    """Replay one exact successor bundle without consuming it or writing evidence."""

    _validate_expectation(expectation)
    root = read_root_fn(expectation.bundle_path)
    _require(
        type(root) is provenance.DirectoryIdentity
        and (
            root.path,
            root.device,
            root.inode,
            root.mode,
        )
        == (
            expectation.bundle_path,
            expectation.bundle_device,
            expectation.bundle_inode,
            expectation.bundle_mode,
        ),
        "bundle_identity_drift",
    )
    _require(
        tuple(inventory_fn(root))
        == tuple(sorted(successor.ARTIFACT_NAMES, key=lambda name: name.encode("utf-8"))),
        "artifact_inventory_drift",
    )

    identities: list[provenance.FileIdentity] = []
    decoded: dict[str, Mapping[str, Any]] = {}
    for item in expectation.artifacts:
        path = Path(root.path) / item.name
        identity = read_file_fn(
            path,
            expected_mode=0o600,
            expected_size=item.byte_count,
            expected_sha256=item.sha256,
            root=root,
        )
        actual = read_file_fn(
            path,
            expected_mode=0o600,
            expected_size=item.byte_count,
            expected_sha256=item.sha256,
            root=root,
        )
        same_target_fn(actual, identity)
        value = decode_fn(identity.data)
        _require(isinstance(value, Mapping), "artifact_not_object")
        identities.append(identity)
        decoded[item.name] = value

    counts = {"public": 0, "final": 0, "strict": 0}

    def count(kind: str) -> None:
        _require(kind in counts and counts[kind] == 0, "validator_call_count_drift")
        counts[kind] += 1

    public = public_validator_fn(
        decoded[successor.ARTIFACT_NAMES[2]],
        descriptor_identity=identities[2],
        expected_preterminal=tuple(identities[:2]),
        call_counter=count,
    )
    final = replay_fn(root.path, tuple(identities), call_counter=count)
    strict = strict_validator_fn(root.path, tuple(identities), call_counter=count)
    _require(counts == {"public": 1, "final": 1, "strict": 1}, "validator_call_count_drift")

    public_native = provenance.json_native_value(public)
    final_native = provenance.json_native_value(final)
    strict_native = provenance.json_native_value(strict)
    summary_native = provenance.json_native_value(decoded[successor.ARTIFACT_NAMES[3]])
    _require(public_native == summary_native, "public_summary_drift")
    _require(
        public_native.get("status") == "public_descriptor_semantic_pass"
        and final_native == {
            "schema": "g4_successor_lineage_final_replay_v1",
            "status": "pass",
            "artifact_count": 5,
        }
        and strict_native == {
            "schema": "g4_successor_lineage_strict_validation_v1",
            "status": "pass",
            "artifact_count": 5,
        },
        "lineage_validation_failed",
    )

    frozen = provenance.json_native_value(decoded[successor.ARTIFACT_NAMES[0]])
    r6_plan = provenance.json_native_value(decoded[successor.ARTIFACT_NAMES[1]])
    descriptor = provenance.json_native_value(decoded[successor.ARTIFACT_NAMES[2]])
    source = frozen.get("source", {})
    policy = frozen.get("policy", {})
    eq = frozen.get("eq", {})
    _require(
        source.get("repository", {}).get("path") == expectation.source_repository_path
        and source.get("head") == expectation.source_head
        and source.get("checkpoint") == expectation.source_head
        and source.get("tree") == expectation.source_tree
        and tuple(source.get(key) for key in ("staged", "unstaged", "untracked", "clean"))
        == (False, False, False, True),
        "source_contract_drift",
    )
    expected_policy = {
        "path": expectation.policy_path,
        "bytes": expectation.policy_byte_count,
        "sha256": expectation.policy_sha256,
    }
    _require(policy == expected_policy and descriptor.get("policy") == expected_policy, "policy_contract_drift")
    expected_eq = {
        "root": expectation.eq_root,
        "manifest_bytes": expectation.eq_manifest_bytes,
        "manifest_sha256": expectation.eq_manifest_sha256,
    }
    _require(
        {key: eq.get(key) for key in expected_eq} == expected_eq
        and descriptor.get("eq") == expected_eq
        and eq.get("qualification", {}).get("status") == "qualified_1_2500"
        and eq.get("qualification", {}).get("selected_shutter") == "1/2500",
        "eq_contract_drift",
    )

    policy_contract = provenance.json_native_value(frozen.get("policy_contract"))
    validate_policy_fn(policy_contract)
    validate_r6_plan_fn(r6_plan)
    machine = provenance.json_native_value(machine_status_fn())
    operational = machine.get("operating_envelope", {})
    locks = machine.get("locks", {})
    _require(
        operational == {
            "dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "steady_status": "not_demonstrated",
        },
        "operational_contract_drift",
    )
    _require(
        locks == {
            "strip": "blocked_until_ray_r6_pass",
            "td_c": "blocked_until_combined_td_b_pass",
            "sentinel": True,
            "p8": True,
        }
        and machine.get("ray_r6", {}).get("formal_accepted") == 0
        and machine.get("ray_r6", {}).get("retry") == 0,
        "machine_lock_drift",
    )

    return {
        "schema": "g4_successor_predevice_oracle_v1",
        "status": "pass",
        "validations": {
            "public": public_native["status"],
            "final_replay": final_native["status"],
            "strict": strict_native["status"],
            "lineage": "pass",
            "call_counts": counts,
        },
        "release": {
            "path": root.path,
            "device": root.device,
            "inode": root.inode,
            "mode": root.mode,
            "artifact_count": len(identities),
        },
        "artifacts": [_reference(identity) for identity in identities],
        "source": source,
        "policy": expected_policy,
        "eq": expected_eq,
        "r6": {
            key: provenance.json_native_value(r6_plan[key])
            for key in (
                "status",
                "executable",
                "capture_ids",
                "state_shutters",
                "formal_logical",
                "formal_physical_cap",
                "setup_in_formal_root",
                "ambient",
                "launch",
                "retry",
                "old_new_frame_combination",
            )
        },
        "operational": operational,
        "locks": locks,
        "proposed_current_route_state": {
            "canonical_validator_success": True,
            "eligibility": True,
            "release_consumable": True,
            "release_consumption_authorized": False,
            "scope": "exact_g4_01_release_only_waiting_planner_and_orchestrator",
        },
        "effective_authority": {
            "canonical_validator_success": False,
            "eligibility": False,
            "release_consumable": False,
            "release_consumption_authorized": False,
            "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
            "device_authorized": False,
            "camera_authorized": False,
            "ray_authorized": False,
            "strip_authorized": False,
            "capture_authorized": False,
            "formal_r6_authorized": False,
            "td_c_authorized": False,
        },
    }


def _failure_code(error: BaseException) -> str:
    code = getattr(error, "code", None)
    return code if type(code) is str and code else type(error).__name__


def _success_seal(
    root: provenance.DirectoryIdentity,
    result: provenance.FileIdentity,
) -> dict[str, Any]:
    return {
        "schema": "g4_successor_predevice_terminal_seal_v1",
        "status": "sealed_pass_non_authorizing_waiting_planner_review",
        "root": _root_reference(root),
        "result": _identity_reference(result),
        "accounting": {
            "evaluate_successor_predevice_calls": 1,
            "result_persist_calls_before_seal": 1,
            "terminal_persist_call_for_this_seal": 1,
            "independent_replay_calls_at_seal": 0,
            "independent_replay_required": 1,
        },
        "retry": 0,
        "release_consumption": 0,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "effective_authority": dict(_FALSE_EFFECTIVE_AUTHORITY),
    }


def _failure_seal(
    root: provenance.DirectoryIdentity,
    *,
    phase: str,
    primary: BaseException,
    result: provenance.FileIdentity | None,
) -> dict[str, Any]:
    return {
        "schema": "g4_successor_predevice_terminal_seal_v1",
        "status": "sealed_fail_non_authorizing",
        "failed_phase": phase,
        "primary_code": _failure_code(primary),
        "root": _root_reference(root),
        "result": _identity_reference(result) if result is not None else None,
        "accounting": {
            "evaluate_successor_predevice_calls": 1,
            "failure_seal_persist_attempts": 1,
            "independent_replay_calls_at_seal": 0,
        },
        "retry": 0,
        "release_consumption": 0,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "effective_authority": dict(_FALSE_EFFECTIVE_AUTHORITY),
    }


def persist_successor_predevice_evidence(
    expectation: PredeviceExpectation,
    *,
    output_root: str | Path,
    evaluate_fn: Callable[[PredeviceExpectation], Mapping[str, Any]] = evaluate_successor_predevice,
    create_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.create_exclusive_root,
    persist_fn: Callable[..., provenance.FileIdentity] = provenance.persist_canonical_json,
) -> PredeviceEvidencePackage:
    """Persist one non-authorizing oracle package under one fresh exact root."""

    result_value = _validate_result(evaluate_fn(expectation))
    root = create_root_fn(output_root)
    result_identity: provenance.FileIdentity | None = None
    phase = "validate_root_identity"
    try:
        _require(
            type(root) is provenance.DirectoryIdentity
            and root.path == str(Path(output_root))
            and root.mode == 0o700,
            "evidence_root_identity_drift",
        )
        phase = "persist_result"
        result_identity = persist_fn(root, EVIDENCE_ARTIFACT_NAMES[0], result_value)
        _require(
            type(result_identity) is provenance.FileIdentity
            and Path(result_identity.path).name == EVIDENCE_ARTIFACT_NAMES[0]
            and result_identity.mode == 0o600
            and result_identity.root == root,
            "evidence_result_identity_drift",
        )
        phase = "persist_terminal"
        terminal_identity = persist_fn(
            root,
            EVIDENCE_ARTIFACT_NAMES[1],
            _success_seal(root, result_identity),
        )
        _require(
            type(terminal_identity) is provenance.FileIdentity
            and Path(terminal_identity.path).name == EVIDENCE_ARTIFACT_NAMES[1]
            and terminal_identity.mode == 0o600
            and terminal_identity.root == root,
            "evidence_terminal_identity_drift",
        )
    except BaseException as primary:
        try:
            persist_fn(
                root,
                EVIDENCE_ARTIFACT_NAMES[1],
                _failure_seal(
                    root, phase=phase, primary=primary, result=result_identity,
                ),
            )
        except BaseException as seal_failure:
            raise SuccessorPredeviceError(
                "durable_package_and_failure_seal_failed",
                primary=primary,
                seal_failure=seal_failure,
            ) from primary
        raise SuccessorPredeviceError(
            "durable_package_failed", primary=primary,
        ) from primary
    return PredeviceEvidencePackage(root, result_identity, terminal_identity)


def _validate_success_seal(
    value: Mapping[str, Any],
    *,
    root: provenance.DirectoryIdentity,
    result: provenance.FileIdentity,
) -> dict[str, Any]:
    seal = provenance.json_native_value(value)
    _require(seal == _success_seal(root, result), "evidence_terminal_drift")
    return seal


def replay_successor_predevice_evidence(
    package: PredeviceEvidencePackage,
    *,
    read_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.read_existing_root,
    inventory_fn: Callable[..., Sequence[str]] = provenance.list_exact_regular_children,
    read_file_fn: Callable[..., provenance.FileIdentity] = provenance.read_exact_file,
    same_target_fn: Callable[..., provenance.FileIdentity] = provenance.require_same_target,
    decode_fn: Callable[[bytes], Any] = provenance.decode_canonical_json,
) -> dict[str, Any]:
    """Independently replay one exact durable package without its source release."""

    _require(type(package) is PredeviceEvidencePackage, "evidence_package_invalid")
    expected = (package.result, package.terminal)
    _require(
        tuple(Path(identity.path).name for identity in expected) == EVIDENCE_ARTIFACT_NAMES
        and all(
            type(identity) is provenance.FileIdentity
            and identity.mode == 0o600
            and identity.root == package.root
            for identity in expected
        ),
        "evidence_identity_drift",
    )
    root = read_root_fn(package.root.path)
    _require(root == package.root, "evidence_root_identity_drift")
    _require(
        tuple(inventory_fn(root))
        == tuple(sorted(EVIDENCE_ARTIFACT_NAMES, key=lambda name: name.encode("utf-8"))),
        "evidence_inventory_drift",
    )
    actual: list[provenance.FileIdentity] = []
    decoded: list[Mapping[str, Any]] = []
    for name, identity in zip(EVIDENCE_ARTIFACT_NAMES, expected):
        observed = read_file_fn(
            Path(root.path) / name,
            expected_mode=0o600,
            expected_size=identity.byte_count,
            expected_sha256=identity.sha256,
            root=root,
        )
        same_target_fn(observed, identity)
        value = decode_fn(observed.data)
        _require(isinstance(value, Mapping), "evidence_artifact_not_object")
        actual.append(observed)
        decoded.append(value)
    result = _validate_result(decoded[0])
    _validate_success_seal(decoded[1], root=root, result=actual[0])
    return {
        "schema": "g4_successor_predevice_evidence_replay_v1",
        "status": "pass",
        "artifact_count": 2,
        "root": _root_reference(root),
        "artifacts": [_identity_reference(identity) for identity in actual],
        "result_status": result["status"],
        "independent_replay_calls": 1,
        "retry": 0,
        "release_consumption": 0,
        "effective_authority": dict(_FALSE_EFFECTIVE_AUTHORITY),
    }
