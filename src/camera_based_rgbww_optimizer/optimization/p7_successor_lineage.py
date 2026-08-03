"""Guide 4 successor-lineage composition and non-authorizing state machine."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


__all__ = [
    "ARTIFACT_NAMES", "SuccessorLineageBundle", "SuccessorLineageError",
    "SuccessorLineageInputs", "build_successor_lineage_inputs",
    "compose_successor_lineage_bundle", "replay_successor_lineage_bundle",
    "strict_validate_successor_lineage_bundle", "validate_successor_lineage_release",
]

ARTIFACT_NAMES = (
    "frozen-inputs.json", "r6-formal-plan.json", "release-descriptor.json",
    "validation-summary.json", "terminal-seal.json",
)
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_FALSE_AUTHORITY = {
    "release_consumable": False,
    "release_consumption_authorized": False,
    "eligibility": False,
    "device_authorized": False,
    "formal_r6_authorized": False,
}
_PROHIBITED_CLAIMS = {
    "release_usable", "production_release_usable", "product_ready", "formal_pass",
    "final_validation_pass", "strict_validation_pass",
}
_SECRET_KEY_PARTS = ("secret", "password", "credential", "api_key", "token")
_FORBIDDEN_MARKERS = (
    "REF-P7-25-R2-", "retained-r3", "retained_r3_root",
    "setup-lineage-release", "external-controller", "external_controller",
    "planner-candidate",
)
_R6_PLAN_KEYS = {
    "schema", "status", "executable", "experiment_id", "source", "strip",
    "ambient", "formal_logical", "formal_physical_cap", "setup_in_formal_root",
    "launch", "retry", "capture_ids", "state_shutters", "c_policy_status",
    "old_new_frame_combination", "failure_contract",
}


class SuccessorLineageError(RuntimeError):
    def __init__(
        self, code: str, *, primary: BaseException | None = None,
        seal_failure: BaseException | None = None,
    ) -> None:
        self.code = code
        self.primary = primary
        self.seal_failure = seal_failure
        super().__init__(code)


@dataclass(frozen=True)
class SuccessorLineageInputs:
    frozen_inputs: Mapping[str, Any]
    r6_formal_plan: Mapping[str, Any]
    machine_status: Mapping[str, Any]


@dataclass(frozen=True)
class SuccessorLineageBundle:
    root: provenance.DirectoryIdentity
    artifacts: tuple[provenance.FileIdentity, ...]
    public_validation: Mapping[str, Any]
    final_replay: Mapping[str, Any]
    strict_validation: Mapping[str, Any]


def _freeze(value: Any) -> Any:
    native = provenance.json_native_value(value)
    if type(native) is dict:
        return MappingProxyType({key: _freeze(item) for key, item in native.items()})
    if type(native) is list:
        return tuple(_freeze(item) for item in native)
    return native


def _exact_keys(value: Any, expected: set[str], code: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise SuccessorLineageError(code)
    return value


def _sha256(value: object, code: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise SuccessorLineageError(code)
    return value


def _walk_guard(value: Any) -> None:
    if isinstance(value, Mapping):
        if _PROHIBITED_CLAIMS.intersection(value):
            raise SuccessorLineageError("prohibited_downstream_claim")
        for key, item in value.items():
            if type(key) is str and any(part in key.lower() for part in _SECRET_KEY_PARTS):
                raise SuccessorLineageError("secret_material_prohibited")
            _walk_guard(key)
            _walk_guard(item)
    elif type(value) in (tuple, list):
        for item in value:
            _walk_guard(item)
    elif type(value) is str and any(marker in value for marker in _FORBIDDEN_MARKERS):
        raise SuccessorLineageError("historical_input_prohibited")


def _authority(value: Mapping[str, Any], code: str) -> None:
    if any(value.get(key) is not expected for key, expected in _FALSE_AUTHORITY.items()):
        raise SuccessorLineageError(code)
    if value.get("retained_r3_status") != "RETAINED_UNVALIDATED_UNCONSUMED":
        raise SuccessorLineageError(code)


def _reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    if type(identity) is not provenance.FileIdentity:
        raise SuccessorLineageError("artifact_identity_invalid")
    return {
        "path": Path(identity.path).name,
        "bytes": identity.byte_count,
        "sha256": identity.sha256,
    }


def _source_mapping(identity: provenance.SourceIdentity) -> dict[str, Any]:
    if type(identity) is not provenance.SourceIdentity or not identity.clean:
        raise SuccessorLineageError("source_identity_not_clean")
    if identity.staged or identity.unstaged or identity.untracked or identity.head != identity.checkpoint:
        raise SuccessorLineageError("source_identity_not_clean")
    return {
        "repository": {
            "path": identity.repository.path,
            "device": identity.repository.device,
            "inode": identity.repository.inode,
            "mode": identity.repository.mode,
        },
        "head": identity.head,
        "checkpoint": identity.checkpoint,
        "tree": identity.tree,
        "staged": False,
        "unstaged": False,
        "untracked": False,
        "clean": True,
    }


def _check_r6_plan(plan: Mapping[str, Any]) -> None:
    _exact_keys(plan, _R6_PLAN_KEYS, "r6_plan_open_schema")
    failure_contract = _exact_keys(plan.get("failure_contract"), {
        "classification", "formal_pass", "strip_call_count", "retry",
    }, "r6_failure_contract_open_schema")
    capture_ids = tuple(str(value) for value in plan["capture_ids"])
    expected_prefixes = tuple(f"{index:03d}-" for index in range(16))
    if (
        plan["schema"] != "p7_td_b_ray_r6_formal_plan_v1"
        or plan["status"] != "selected_exposure_policy_non_executable"
        or plan["executable"] is not False
        or len(capture_ids) != 16
        or any(not value.startswith(prefix) for value, prefix in zip(capture_ids, expected_prefixes))
        or plan["state_shutters"] != {
            "A": "1/5000", "D": "1/6400", "B": "1/8000", "C": "1/2500",
        }
        or tuple(plan[key] for key in (
            "formal_logical", "formal_physical_cap", "setup_in_formal_root",
            "ambient", "launch", "retry",
        )) != (16, 16, 0, 0, 1, 0)
        or plan["old_new_frame_combination"] != "prohibited"
        or failure_contract != {
            "classification": "accepted_hard_failed_formal_attempt",
            "formal_pass": False,
            "strip_call_count": 0,
            "retry": 0,
        }
    ):
        raise SuccessorLineageError("r6_plan_drift")


def _check_source_mapping(value: Any, code: str) -> Mapping[str, Any]:
    source = _exact_keys(value, {
        "repository", "head", "checkpoint", "tree", "staged", "unstaged",
        "untracked", "clean",
    }, code)
    repository = _exact_keys(source["repository"], {
        "path", "device", "inode", "mode",
    }, code)
    if (
        type(repository["path"]) is not str or not repository["path"].startswith("/")
        or any(type(repository[key]) is not int for key in ("device", "inode", "mode"))
        or type(source["head"]) is not str or re.fullmatch(r"[0-9a-f]{40}", source["head"]) is None
        or source["checkpoint"] != source["head"]
        or type(source["tree"]) is not str or re.fullmatch(r"[0-9a-f]{40}", source["tree"]) is None
        or tuple(source[key] for key in ("staged", "unstaged", "untracked", "clean"))
        != (False, False, False, True)
    ):
        raise SuccessorLineageError(code)
    return source


def _check_policy_reference(value: Any, code: str) -> Mapping[str, Any]:
    policy = _exact_keys(value, {"path", "bytes", "sha256"}, code)
    if (
        type(policy["path"]) is not str or not policy["path"]
        or type(policy["bytes"]) is not int or policy["bytes"] <= 0
    ):
        raise SuccessorLineageError(code)
    _sha256(policy["sha256"], code)
    return policy


def build_successor_lineage_inputs(
    *,
    repo_root: str | Path,
    source_checkpoint: str,
    policy_path: str | Path,
    policy_sha256: str,
    eq_root: str | Path,
    eq_manifest_bytes: bytes,
    eq_manifest_sha256: str,
    source_identity_fn: Callable[..., provenance.SourceIdentity] = provenance.read_git_source_identity,
    read_exact_file_fn: Callable[..., provenance.FileIdentity] = provenance.read_exact_file,
    decode_policy_fn: Callable[[bytes], Any] = provenance.decode_strict_json_bytes,
    validate_policy_fn: Callable[[Mapping[str, Any]], None] = thermal.validate_td_b_exposure_policy_v2,
    audit_eq_fn: Callable[[str | Path], Mapping[str, Any]] = thermal.audit_td_b_eq_r6_qualification,
    build_r6_plan_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]] = thermal.build_td_b_r6_formal_plan,
    machine_status_fn: Callable[[], Mapping[str, Any]] = thermal.td_b_r6_machine_status,
) -> SuccessorLineageInputs:
    """Bind source, policy, EQ and non-executable R6 facts without release I/O."""

    source = source_identity_fn(repo_root, source_checkpoint)
    source_value = _source_mapping(source)
    expected_policy_sha = _sha256(policy_sha256, "policy_sha256_invalid")
    policy_identity = read_exact_file_fn(policy_path, expected_sha256=expected_policy_sha)
    if (
        type(policy_identity) is not provenance.FileIdentity
        or policy_identity.path != str(Path(policy_path))
        or policy_identity.sha256 != expected_policy_sha
    ):
        raise SuccessorLineageError("policy_identity_invalid")
    decoded_policy = decode_policy_fn(policy_identity.data)
    if not isinstance(decoded_policy, Mapping):
        raise SuccessorLineageError("policy_not_object")
    native_policy = provenance.json_native_value(decoded_policy)
    if type(native_policy) is not dict:
        raise SuccessorLineageError("policy_not_object")
    validate_policy_fn(native_policy)

    manifest_sha = _sha256(eq_manifest_sha256, "eq_manifest_sha256_invalid")
    if type(eq_manifest_bytes) is not bytes or hashlib.sha256(eq_manifest_bytes).hexdigest() != manifest_sha:
        raise SuccessorLineageError("eq_manifest_hash_drift")
    qualification = dict(audit_eq_fn(eq_root))
    manifest = qualification.get("manifest")
    if (
        qualification.get("status") != "qualified_1_2500"
        or qualification.get("selected_shutter") != "1/2500"
        or tuple(qualification.get(key) for key in (
            "candidate_launch_count", "candidate_2_call_count", "attempted_capture_calls",
            "physical_returned_cr3_count", "accepted_capture_count", "retry",
        )) != (1, 0, 4, 4, 4, 0)
        or not isinstance(manifest, Mapping)
        or manifest.get("payload_bytes") != len(eq_manifest_bytes)
        or manifest.get("sha256") != manifest_sha
    ):
        raise SuccessorLineageError("eq_qualification_drift")

    plan = dict(build_r6_plan_fn(native_policy))
    _check_r6_plan(plan)
    machine = dict(machine_status_fn())
    locks = machine.get("locks", {})
    if (
        locks.get("strip") != "blocked_until_ray_r6_pass"
        or locks.get("td_c") != "blocked_until_combined_td_b_pass"
        or locks.get("sentinel") is not True or locks.get("p8") is not True
        or machine.get("ray_r6", {}).get("formal_accepted") != 0
        or machine.get("ray_r6", {}).get("retry") != 0
    ):
        raise SuccessorLineageError("machine_lock_drift")
    frozen = {
        "schema": "g4_successor_lineage_frozen_inputs_v1",
        "source": source_value,
        "policy": {
            "path": policy_identity.path,
            "bytes": policy_identity.byte_count,
            "sha256": policy_identity.sha256,
        },
        "policy_contract": native_policy,
        "eq": {
            "root": str(eq_root), "manifest_bytes": len(eq_manifest_bytes),
            "manifest_sha256": manifest_sha, "qualification": qualification,
        },
        "old_new_frame_combination": "prohibited",
    }
    _walk_guard(frozen)
    return SuccessorLineageInputs(_freeze(frozen), _freeze(plan), _freeze(machine))


def _descriptor(inputs: SuccessorLineageInputs, first_two: Sequence[provenance.FileIdentity]) -> dict[str, Any]:
    return {
        "schema": "g4_successor_lineage_release_v1",
        "status": "candidate_non_authorizing",
        **_FALSE_AUTHORITY,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "source": provenance.json_native_value(inputs.frozen_inputs["source"]),
        "policy": provenance.json_native_value(inputs.frozen_inputs["policy"]),
        "eq": {
            key: inputs.frozen_inputs["eq"][key]
            for key in ("root", "manifest_bytes", "manifest_sha256")
        },
        "r6_plan": {
            key: provenance.json_native_value(inputs.r6_formal_plan[key])
            for key in (
                "schema", "status", "capture_ids", "state_shutters", "formal_logical",
                "formal_physical_cap", "setup_in_formal_root", "ambient", "retry",
                "old_new_frame_combination",
            )
        },
        "artifact_order": list(ARTIFACT_NAMES),
        "preterminal_references": [_reference(value) for value in first_two],
    }


def _check_descriptor(
    value: Mapping[str, Any], first_two: Sequence[provenance.FileIdentity]
) -> None:
    expected = {
        "schema", "status", *_FALSE_AUTHORITY, "retained_r3_status", "source",
        "policy", "eq", "r6_plan", "artifact_order", "preterminal_references",
    }
    _exact_keys(value, expected, "descriptor_open_schema")
    _authority(value, "descriptor_authority_drift")
    if value["schema"] != "g4_successor_lineage_release_v1" or value["status"] != "candidate_non_authorizing":
        raise SuccessorLineageError("descriptor_status_drift")
    if tuple(value["artifact_order"]) != ARTIFACT_NAMES:
        raise SuccessorLineageError("artifact_order_drift")
    if provenance.json_native_value(value["preterminal_references"]) != [
        _reference(identity) for identity in first_two
    ]:
        raise SuccessorLineageError("descriptor_reference_drift")
    _walk_guard(value)


def validate_successor_lineage_release(
    release: Mapping[str, Any], *, descriptor_identity: provenance.FileIdentity,
    expected_preterminal: Sequence[provenance.FileIdentity],
    call_counter: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Public-only validation of one persisted candidate descriptor."""

    if call_counter is not None:
        call_counter("public")
    if type(descriptor_identity) is not provenance.FileIdentity:
        raise SuccessorLineageError("descriptor_identity_invalid")
    _check_descriptor(release, expected_preterminal)
    if provenance.decode_canonical_json(descriptor_identity.data) != _freeze(release):
        raise SuccessorLineageError("descriptor_identity_content_drift")
    return {
        "schema": "g4_successor_lineage_validation_summary_v1",
        "status": "public_descriptor_semantic_pass",
        **_FALSE_AUTHORITY,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "descriptor": _reference(descriptor_identity),
    }


def _load_bundle(
    root_path: str | Path,
    expected: Sequence[provenance.FileIdentity],
    *,
    read_root_fn: Callable[..., provenance.DirectoryIdentity],
    read_file_fn: Callable[..., provenance.FileIdentity],
    inventory_fn: Callable[..., Sequence[str]],
) -> tuple[provenance.DirectoryIdentity, dict[str, Mapping[str, Any]]]:
    root = read_root_fn(root_path)
    if type(root) is not provenance.DirectoryIdentity or len(expected) != 5:
        raise SuccessorLineageError("bundle_identity_invalid")
    if tuple(inventory_fn(root)) != tuple(sorted(ARTIFACT_NAMES, key=lambda name: name.encode("utf-8"))):
        raise SuccessorLineageError("artifact_inventory_drift")
    values: dict[str, Mapping[str, Any]] = {}
    for name, identity in zip(ARTIFACT_NAMES, expected):
        if Path(identity.path).name != name:
            raise SuccessorLineageError("artifact_identity_order_drift")
        actual = read_file_fn(
            Path(root.path) / name, expected_mode=0o600,
            expected_size=identity.byte_count, expected_sha256=identity.sha256, root=root,
        )
        provenance.require_same_target(actual, identity)
        decoded = provenance.decode_canonical_json(actual.data)
        if not isinstance(decoded, Mapping):
            raise SuccessorLineageError("artifact_not_object")
        values[name] = decoded
    return root, values


def _check_complete_bundle(
    values: Mapping[str, Mapping[str, Any]], identities: Sequence[provenance.FileIdentity]
) -> None:
    frozen = _exact_keys(values[ARTIFACT_NAMES[0]], {
        "schema", "source", "policy", "policy_contract", "eq", "old_new_frame_combination",
    }, "frozen_inputs_open_schema")
    if frozen["schema"] != "g4_successor_lineage_frozen_inputs_v1" or frozen["old_new_frame_combination"] != "prohibited":
        raise SuccessorLineageError("frozen_inputs_drift")
    _check_source_mapping(frozen["source"], "source_contract_drift")
    _check_policy_reference(frozen["policy"], "policy_reference_contract_drift")
    _exact_keys(frozen["eq"], {
        "root", "manifest_bytes", "manifest_sha256", "qualification",
    }, "eq_open_schema")
    plan = values[ARTIFACT_NAMES[1]]
    _check_r6_plan(plan)
    descriptor = values[ARTIFACT_NAMES[2]]
    _check_descriptor(descriptor, identities[:2])
    _check_source_mapping(descriptor["source"], "descriptor_source_contract_drift")
    _check_policy_reference(descriptor["policy"], "descriptor_policy_contract_drift")
    _exact_keys(descriptor["eq"], {"root", "manifest_bytes", "manifest_sha256"}, "descriptor_eq_open_schema")
    _exact_keys(descriptor["r6_plan"], {
        "schema", "status", "capture_ids", "state_shutters", "formal_logical",
        "formal_physical_cap", "setup_in_formal_root", "ambient", "retry",
        "old_new_frame_combination",
    }, "descriptor_r6_open_schema")
    summary = _exact_keys(values[ARTIFACT_NAMES[3]], {
        "schema", "status", *_FALSE_AUTHORITY, "retained_r3_status", "descriptor",
    }, "summary_open_schema")
    _authority(summary, "summary_authority_drift")
    if (
        summary["schema"] != "g4_successor_lineage_validation_summary_v1"
        or summary["status"] != "public_descriptor_semantic_pass"
        or provenance.json_native_value(summary["descriptor"]) != _reference(identities[2])
    ):
        raise SuccessorLineageError("summary_reference_drift")
    terminal = _exact_keys(values[ARTIFACT_NAMES[4]], {
        "schema", "status", *_FALSE_AUTHORITY, "retained_r3_status", "references",
    }, "terminal_open_schema")
    _authority(terminal, "terminal_authority_drift")
    if (
        terminal["schema"] != "g4_successor_lineage_terminal_seal_v1"
        or terminal["status"] != "sealed_non_authorizing_pending_independent_replay"
        or provenance.json_native_value(terminal["references"]) != [
            _reference(identity) for identity in identities[:4]
        ]
        or any(ref["path"] == ARTIFACT_NAMES[4] for ref in terminal["references"])
    ):
        raise SuccessorLineageError("terminal_reference_drift")
    if (
        provenance.json_native_value(descriptor["source"]) != provenance.json_native_value(frozen["source"])
        or provenance.json_native_value(descriptor["policy"]) != provenance.json_native_value(frozen["policy"])
        or descriptor["eq"] != {key: frozen["eq"][key] for key in ("root", "manifest_bytes", "manifest_sha256")}
        or provenance.json_native_value(descriptor["r6_plan"]) != {
            key: provenance.json_native_value(plan[key])
            for key in (
                "schema", "status", "capture_ids", "state_shutters", "formal_logical",
                "formal_physical_cap", "setup_in_formal_root", "ambient", "retry",
                "old_new_frame_combination",
            )
        }
    ):
        raise SuccessorLineageError("cross_artifact_contract_drift")
    for guarded in (frozen, descriptor, summary, terminal):
        _walk_guard(guarded)


def replay_successor_lineage_bundle(
    root_path: str | Path, expected_artifacts: Sequence[provenance.FileIdentity], *,
    call_counter: Callable[[str], None] | None = None,
    read_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.read_existing_root,
    read_file_fn: Callable[..., provenance.FileIdentity] = provenance.read_exact_file,
    inventory_fn: Callable[..., Sequence[str]] = provenance.list_exact_regular_children,
) -> dict[str, Any]:
    if call_counter is not None:
        call_counter("final")
    _root, values = _load_bundle(
        root_path, expected_artifacts, read_root_fn=read_root_fn,
        read_file_fn=read_file_fn, inventory_fn=inventory_fn,
    )
    _check_complete_bundle(values, expected_artifacts)
    return _freeze({"schema": "g4_successor_lineage_final_replay_v1", "status": "pass", "artifact_count": 5})


def strict_validate_successor_lineage_bundle(
    root_path: str | Path, expected_artifacts: Sequence[provenance.FileIdentity], *,
    call_counter: Callable[[str], None] | None = None,
    read_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.read_existing_root,
    read_file_fn: Callable[..., provenance.FileIdentity] = provenance.read_exact_file,
    inventory_fn: Callable[..., Sequence[str]] = provenance.list_exact_regular_children,
) -> dict[str, Any]:
    if call_counter is not None:
        call_counter("strict")
    _root, values = _load_bundle(
        root_path, expected_artifacts, read_root_fn=read_root_fn,
        read_file_fn=read_file_fn, inventory_fn=inventory_fn,
    )
    _check_complete_bundle(values, expected_artifacts)
    return _freeze({"schema": "g4_successor_lineage_strict_validation_v1", "status": "pass", "artifact_count": 5})


def _failure_seal(primary: BaseException, artifacts: Sequence[provenance.FileIdentity]) -> dict[str, Any]:
    return {
        "schema": "g4_successor_lineage_failure_seal_v1",
        "status": "failed_before_terminal",
        **_FALSE_AUTHORITY,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "primary_failure": {
            "type": type(primary).__name__,
            "code": getattr(primary, "code", "untyped_failure"),
        },
        "references": [_reference(identity) for identity in artifacts],
    }


def compose_successor_lineage_bundle(
    inputs: SuccessorLineageInputs, *,
    safe_parent: provenance.DirectoryIdentity,
    child_name: str,
    call_counter: Callable[[str], None] | None = None,
    create_root_fn: Callable[..., provenance.DirectoryIdentity] = provenance.create_exclusive_direct_child,
    persist_fn: Callable[..., provenance.FileIdentity] = provenance.persist_canonical_json,
    public_validator_fn: Callable[..., Mapping[str, Any]] = validate_successor_lineage_release,
    replay_fn: Callable[..., Mapping[str, Any]] = replay_successor_lineage_bundle,
    strict_validator_fn: Callable[..., Mapping[str, Any]] = strict_validate_successor_lineage_bundle,
) -> SuccessorLineageBundle:
    """Write candidate→public summary→pending terminal, then replay twice."""

    if type(inputs) is not SuccessorLineageInputs:
        raise SuccessorLineageError("inputs_invalid")
    root = create_root_fn(safe_parent, child_name)
    if type(root) is not provenance.DirectoryIdentity:
        raise SuccessorLineageError("root_identity_invalid")
    artifacts: list[provenance.FileIdentity] = []
    terminal_written = False

    def persist(name: str, value: Mapping[str, Any]) -> provenance.FileIdentity:
        identity = persist_fn(root, name, value)
        if type(identity) is not provenance.FileIdentity or Path(identity.path).name != name:
            raise SuccessorLineageError("persist_identity_drift")
        artifacts.append(identity)
        return identity

    try:
        frozen = persist(ARTIFACT_NAMES[0], inputs.frozen_inputs)
        plan = persist(ARTIFACT_NAMES[1], inputs.r6_formal_plan)
        descriptor_value = _descriptor(inputs, (frozen, plan))
        descriptor = persist(ARTIFACT_NAMES[2], descriptor_value)
        public = dict(public_validator_fn(
            descriptor_value, descriptor_identity=descriptor,
            expected_preterminal=(frozen, plan), call_counter=call_counter,
        ))
        summary = persist(ARTIFACT_NAMES[3], public)
        terminal_value = {
            "schema": "g4_successor_lineage_terminal_seal_v1",
            "status": "sealed_non_authorizing_pending_independent_replay",
            **_FALSE_AUTHORITY,
            "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
            "references": [_reference(value) for value in (frozen, plan, descriptor, summary)],
        }
        persist(ARTIFACT_NAMES[4], terminal_value)
        terminal_written = True
    except BaseException as primary:
        if terminal_written:
            raise
        try:
            persist_fn(root, ARTIFACT_NAMES[4], _failure_seal(primary, artifacts))
        except BaseException as seal_failure:
            raise SuccessorLineageError(
                "preterminal_failure_and_seal_failure", primary=primary,
                seal_failure=seal_failure,
            ) from primary
        raise SuccessorLineageError("preterminal_failure_sealed", primary=primary) from primary

    final: Mapping[str, Any] | None = None
    strict: Mapping[str, Any] | None = None
    failures: list[BaseException] = []
    try:
        final = replay_fn(root.path, tuple(artifacts), call_counter=call_counter)
    except BaseException as exc:
        failures.append(exc)
    try:
        strict = strict_validator_fn(root.path, tuple(artifacts), call_counter=call_counter)
    except BaseException as exc:
        failures.append(exc)
    if failures:
        raise SuccessorLineageError(
            "independent_replay_failed_pending_seal_preserved",
            primary=failures[0], seal_failure=failures[1] if len(failures) > 1 else None,
        ) from failures[0]
    return SuccessorLineageBundle(
        root, tuple(artifacts), _freeze(public), _freeze(final), _freeze(strict)
    )
