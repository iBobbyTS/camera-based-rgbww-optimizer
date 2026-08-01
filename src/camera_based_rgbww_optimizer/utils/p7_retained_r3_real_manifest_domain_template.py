"""Pure, deterministic composition of one subordinate retained-R3 manifest owner."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import PurePosixPath
import re

from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime import (
    ControllerRuntimeRequest,
)

__all__ = [
    "RealManifestDomainTemplateError",
    "RealManifestGitPathIdentity",
    "RealManifestCommitIdentity",
    "RealManifestInputIdentity",
    "RealManifestBaselineIdentity",
    "RealManifestDomainTemplateSpec",
    "RealManifestDomainTemplateBundle",
    "build_real_manifest_domain_template",
]

_SHA40 = re.compile(r"[0-9a-f]{40}")
_SHA64 = re.compile(r"[0-9a-f]{64}")
_MODE_FILE = 0o600
_MODE_ROOT = 0o700
_REFERENCE_TASK = "REF-P7-25-R2-B2-M1-S1"
_CONTRACT = "P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1"
_C1_LABELS = (
    "path_owner_index", "path_owner_index_seal",
    "terminal_evidence", "terminal_evidence_seal",
)
_RETAINED_LABELS = (
    "current_lineage_candidate", "resolved_formal_plan", "setup_lineage_release",
)
_ARTIFACT_NAMES = (
    "retained-r3-audit-provenance-manifest-v2.json",
    "retained-r3-audit-provenance-manifest-v2.sha256.json",
    "terminal-evidence.json",
    "terminal-evidence.sha256.json",
    "execution-result-admission.json",
)
_LIFECYCLE_ORDER = (
    "conformance", "activation", "root", "inputs", "evaluate",
    "terminal", "terminal_seal", "admission",
)


class RealManifestDomainTemplateError(ValueError):
    """Fail-closed domain validation error with one stable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class RealManifestGitPathIdentity:
    repo_path: str
    before_blob_oid: str
    after_blob_oid: str
    before_sha256: str
    after_sha256: str
    binary_patch_sha256: str


@dataclass(frozen=True)
class RealManifestCommitIdentity:
    commit: str
    parent: str
    subject: str
    changed_paths: tuple[str, ...]
    full_patch_sha256: str


@dataclass(frozen=True)
class RealManifestInputIdentity:
    label: str
    path: str
    byte_count: int
    sha256: str
    device: int
    inode: int
    mode: int
    root_path: str
    root_device: int
    root_inode: int
    root_mode: int


@dataclass(frozen=True)
class RealManifestBaselineIdentity:
    release_checkpoint: str
    helper_v1: str
    integration: str
    helper_path: str
    test_path: str
    seam_chain: tuple[RealManifestGitPathIdentity, ...]
    governance_manifest_sha256: str
    guide_sha256: str
    lineage_owner_decision_evidence_sha256: str
    advisor_attachment_sha256: str
    human_governance_override: str
    helper_disposition: str


@dataclass(frozen=True)
class RealManifestDomainTemplateSpec:
    reference_task_id: str
    contract_id: str
    activation: RealManifestCommitIdentity
    baseline: RealManifestBaselineIdentity
    c1_inputs: tuple[RealManifestInputIdentity, ...]
    retained_inputs: tuple[RealManifestInputIdentity, ...]
    source_path: str
    output_root: str
    repo_root: str
    process_argv: tuple[str, ...]


@dataclass(frozen=True)
class RealManifestDomainTemplateBundle:
    template_source: bytes
    template_sha256: str
    replacement_statement: bytes
    replacement_sha256: str
    runtime_request: ControllerRuntimeRequest
    expected_bound_results: int
    expected_artifact_names: tuple[str, ...]
    expected_lifecycle_order: tuple[str, ...]


_GIT_LINES = "\n".join(
    f'        git_{index:02d} = run_read_only_git(REPO_ROOT, ("git", "show", "-s", "--format=%H%x00%P%x00%s", GIT_TARGETS[{index % 7}]))\n'
    f'        phase_state["git_{index:02d}"] = git_{index:02d}.exit_code == 0 and git_{index:02d}.stderr == b""'
    for index in range(56)
)

_TEMPLATE_PREFIX = '''import sys

from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import LifecycleCallbacks, LifecycleRequirements, RootIdentityChain, execute_controller_lifecycle, validate_root_identity_chain
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import DirectoryIdentity as PersistRootIdentity, canonical_json_bytes, create_exclusive_root, persist_canonical_json, read_exact_file, read_existing_root, run_read_only_git

def require_real_manifest_contract(value):
    if type(value) is not tuple or not value or any(type(item) is not tuple or len(item) != 2 or type(item[0]) is not str for item in value):
        raise RuntimeError("real_manifest_contract_invalid")
    return value

def controller():
    REAL_MANIFEST_CONTRACT = (("placeholder", True),)
    require_real_manifest_contract(REAL_MANIFEST_CONTRACT)
    def contract_value(name):
        matches = tuple(value for key, value in REAL_MANIFEST_CONTRACT if key == name)
        if len(matches) != 1:
            raise RuntimeError("real_manifest_binding_missing")
        return matches[0]

    REPO_ROOT = contract_value("repo_root")
    OUTPUT_ROOT = contract_value("output_root")
    C1_INPUTS = contract_value("c1_inputs")
    RETAINED_INPUTS = contract_value("retained_inputs")
    ACTIVATION = contract_value("activation")
    BASELINE = contract_value("baseline")
    GIT_TARGETS = contract_value("git_targets")
    RETRY = contract_value("retry")
    FALLBACK = contract_value("fallback")
    artifact_names = ("retained-r3-audit-provenance-manifest-v2.json", "retained-r3-audit-provenance-manifest-v2.sha256.json", "terminal-evidence.json", "terminal-evidence.sha256.json", "execution-result-admission.json")
    phase_state = {}
    output_root_identity = None
    persist_root_identity = None
    manifest_identity = None
    manifest_seal_identity = None
    terminal_identity = None
    terminal_seal_identity = None
    admission_identity = None
    primary_failure = None

    def phase_conformance():
        if RETRY != 0 or FALLBACK != 0 or len(artifact_names) != 5:
            raise RuntimeError("controller_contract_drift")
        return "conformant"

    def phase_activation():
'''

_TEMPLATE_SUFFIX = '''
        if not all(phase_state[name] for name in tuple("git_%02d" % index for index in range(56))):
            raise RuntimeError("git_identity_mismatch")
        return "activation_verified"

    def phase_root():
        nonlocal output_root_identity, persist_root_identity
        output_root_identity = create_exclusive_root(OUTPUT_ROOT)
        persist_root_identity = PersistRootIdentity(path=output_root_identity.path, device=output_root_identity.device, inode=output_root_identity.inode, mode=output_root_identity.mode)
        if persist_root_identity != output_root_identity:
            raise RuntimeError("output_root_identity_mismatch")
        return "root_created"

    def phase_inputs():
        c1_root_0 = read_existing_root(C1_INPUTS[0][2])
        c1_file_0 = read_exact_file(C1_INPUTS[0][1], expected_mode=C1_INPUTS[0][6], expected_size=C1_INPUTS[0][3], expected_sha256=C1_INPUTS[0][4], root=c1_root_0)
        c1_root_1 = read_existing_root(C1_INPUTS[1][2])
        c1_file_1 = read_exact_file(C1_INPUTS[1][1], expected_mode=C1_INPUTS[1][6], expected_size=C1_INPUTS[1][3], expected_sha256=C1_INPUTS[1][4], root=c1_root_1)
        c1_root_2 = read_existing_root(C1_INPUTS[2][2])
        c1_file_2 = read_exact_file(C1_INPUTS[2][1], expected_mode=C1_INPUTS[2][6], expected_size=C1_INPUTS[2][3], expected_sha256=C1_INPUTS[2][4], root=c1_root_2)
        c1_root_3 = read_existing_root(C1_INPUTS[3][2])
        c1_file_3 = read_exact_file(C1_INPUTS[3][1], expected_mode=C1_INPUTS[3][6], expected_size=C1_INPUTS[3][3], expected_sha256=C1_INPUTS[3][4], root=c1_root_3)
        retained_root_0 = read_existing_root(RETAINED_INPUTS[0][2])
        retained_file_0 = read_exact_file(RETAINED_INPUTS[0][1], expected_mode=RETAINED_INPUTS[0][6], expected_size=RETAINED_INPUTS[0][3], expected_sha256=RETAINED_INPUTS[0][4], root=retained_root_0)
        retained_root_1 = read_existing_root(RETAINED_INPUTS[1][2])
        retained_file_1 = read_exact_file(RETAINED_INPUTS[1][1], expected_mode=RETAINED_INPUTS[1][6], expected_size=RETAINED_INPUTS[1][3], expected_sha256=RETAINED_INPUTS[1][4], root=retained_root_1)
        retained_root_2 = read_existing_root(RETAINED_INPUTS[2][2])
        retained_file_2 = read_exact_file(RETAINED_INPUTS[2][1], expected_mode=RETAINED_INPUTS[2][6], expected_size=RETAINED_INPUTS[2][3], expected_sha256=RETAINED_INPUTS[2][4], root=retained_root_2)
        if not (c1_file_0.root == c1_root_0 and c1_file_1.root == c1_root_1 and c1_file_2.root == c1_root_2 and c1_file_3.root == c1_root_3 and retained_file_0.root == retained_root_0 and retained_file_1.root == retained_root_1 and retained_file_2.root == retained_root_2):
            raise RuntimeError("input_root_identity_mismatch")
        return "inputs_bound"

    def phase_evaluate():
        nonlocal manifest_identity, manifest_seal_identity
        manifest_payload = {
            "schema": "p7_retained_r3_audit_provenance_manifest_v2",
            "status": "sealed_subordinate_provenance_evidence",
            "activation": [ACTIVATION[0], ACTIVATION[1], ACTIVATION[2], list(ACTIVATION[3]), ACTIVATION[4]],
            "baseline": [BASELINE[0], BASELINE[1], BASELINE[2], BASELINE[3], BASELINE[4], [list(row) for row in BASELINE[5]], BASELINE[6], BASELINE[7], BASELINE[8], BASELINE[9], BASELINE[10], BASELINE[11]],
            "c1": [list(row) for row in C1_INPUTS],
            "retained": [list(row) for row in RETAINED_INPUTS],
        }
        manifest_written = persist_canonical_json(persist_root_identity, artifact_names[0], manifest_payload)
        manifest_identity = read_exact_file(OUTPUT_ROOT + "/" + artifact_names[0], expected_mode=384, expected_size=manifest_written.byte_count, expected_sha256=manifest_written.sha256, root=output_root_identity)
        if manifest_written != manifest_identity:
            raise RuntimeError("manifest_identity_mismatch")
        manifest_seal_written = persist_canonical_json(persist_root_identity, artifact_names[1], {"bytes": manifest_identity.byte_count, "sha256": manifest_identity.sha256, "target": artifact_names[0]})
        manifest_seal_identity = read_exact_file(OUTPUT_ROOT + "/" + artifact_names[1], expected_mode=384, expected_size=manifest_seal_written.byte_count, expected_sha256=manifest_seal_written.sha256, root=output_root_identity)
        if manifest_seal_written != manifest_seal_identity:
            raise RuntimeError("manifest_seal_identity_mismatch")
        return "manifest_sealed"

    def phase_terminal(primary, _values):
        nonlocal terminal_identity, terminal_seal_identity, primary_failure
        primary_failure = primary
        if primary is not None:
            return {"status": "failed"}
        terminal_written = persist_canonical_json(persist_root_identity, artifact_names[2], {"status": "sealed_subordinate_provenance_evidence"})
        terminal_identity = read_exact_file(OUTPUT_ROOT + "/" + artifact_names[2], expected_mode=384, expected_size=terminal_written.byte_count, expected_sha256=terminal_written.sha256, root=output_root_identity)
        if terminal_written != terminal_identity:
            raise RuntimeError("terminal_identity_mismatch")
        terminal_seal_written = persist_canonical_json(persist_root_identity, artifact_names[3], {"bytes": terminal_identity.byte_count, "sha256": terminal_identity.sha256, "target": artifact_names[2]})
        terminal_seal_identity = read_exact_file(OUTPUT_ROOT + "/" + artifact_names[3], expected_mode=384, expected_size=terminal_seal_written.byte_count, expected_sha256=terminal_seal_written.sha256, root=output_root_identity)
        if terminal_seal_written != terminal_seal_identity:
            raise RuntimeError("terminal_seal_identity_mismatch")
        return {"status": "terminal"}

    def phase_terminal_seal(terminal):
        if primary_failure is not None:
            return terminal
        if terminal_seal_identity.byte_count <= 0:
            raise RuntimeError("terminal_seal_missing")
        return {"status": "sealed"}

    def phase_admission(seal):
        nonlocal admission_identity
        if primary_failure is not None:
            return seal
        admission_written = persist_canonical_json(persist_root_identity, artifact_names[4], {"admitted": True, "eligibility": False, "release_consumable": False})
        admission_identity = read_exact_file(OUTPUT_ROOT + "/" + artifact_names[4], expected_mode=384, expected_size=admission_written.byte_count, expected_sha256=admission_written.sha256, root=output_root_identity)
        if admission_written != admission_identity:
            raise RuntimeError("admission_identity_mismatch")
        root_chain = RootIdentityChain(before=output_root_identity, files=(manifest_identity, manifest_seal_identity, terminal_identity, terminal_seal_identity, admission_identity), after=output_root_identity)
        root_chain_validated = validate_root_identity_chain(root_chain)
        if root_chain_validated.before != output_root_identity:
            raise RuntimeError("root_chain_mismatch")
        return {"status": "admitted"}

    callbacks = LifecycleCallbacks(conformance=phase_conformance, activation=phase_activation, root=phase_root, inputs=phase_inputs, evaluate=phase_evaluate, terminal=phase_terminal, terminal_seal=phase_terminal_seal, admission=phase_admission)
    result = execute_controller_lifecycle(callbacks, LifecycleRequirements(success_order=("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission"), retry=RETRY, fallback=FALLBACK))
    if result.order != ("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission"):
        raise RuntimeError("lifecycle_order_mismatch")
    return {"artifact_count": len(artifact_names), "status": "sealed_subordinate_provenance_evidence"}

def _main():
    sys.stdout.buffer.write(canonical_json_bytes(controller()))

if __name__ == "__main__":
    _main()
'''

_CANONICAL_TEMPLATE = (_TEMPLATE_PREFIX + _GIT_LINES + _TEMPLATE_SUFFIX).encode("utf-8")
_CANONICAL_TEMPLATE_SHA256 = "a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6"
_GOLDEN_REPLACEMENT_SHA256 = "55c43ad338a83c11a2b2c8d2c5714a9efaf75ec4215dd30e103d540b0c6502ec"


def _plain(value: object, code: str) -> str:
    if type(value) is not str or not value or any(token in value for token in ("\x00", "\n", "\r")):
        raise RealManifestDomainTemplateError(code)
    return value


def _sha(value: object, pattern: re.Pattern[str], code: str) -> str:
    if type(value) is not str or pattern.fullmatch(value) is None:
        raise RealManifestDomainTemplateError(code)
    return value


def _absolute(value: object, code: str) -> str:
    text = _plain(value, code)
    path = PurePosixPath(text)
    if not path.is_absolute() or str(path) != text or any(part in {".", ".."} for part in path.parts):
        raise RealManifestDomainTemplateError(code)
    return text


def _repo_path(value: object) -> str:
    text = _plain(value, "git_path_identity_invalid")
    path = PurePosixPath(text)
    if path.is_absolute() or str(path) != text or any(part in {"", ".", ".."} for part in path.parts):
        raise RealManifestDomainTemplateError("git_path_identity_invalid")
    return text


def _positive(value: object, code: str) -> int:
    if type(value) is not int or value <= 0:
        raise RealManifestDomainTemplateError(code)
    return value


def _literal(value: object) -> str:
    if type(value) in (str, bool, int):
        if type(value) is str:
            _plain(value, "literal_type_invalid")
        return repr(value)
    if type(value) is tuple:
        body = ", ".join(_literal(item) for item in value)
        return "(" + body + ("," if len(value) == 1 else "") + ")"
    raise RealManifestDomainTemplateError("literal_type_invalid")


def _git_path(identity: object) -> tuple[object, ...]:
    if type(identity) is not RealManifestGitPathIdentity:
        raise RealManifestDomainTemplateError("git_path_identity_invalid")
    return (
        _repo_path(identity.repo_path),
        _sha(identity.before_blob_oid, _SHA40, "blob_oid_invalid"),
        _sha(identity.after_blob_oid, _SHA40, "blob_oid_invalid"),
        _sha(identity.before_sha256, _SHA64, "sha256_invalid"),
        _sha(identity.after_sha256, _SHA64, "sha256_invalid"),
        _sha(identity.binary_patch_sha256, _SHA64, "sha256_invalid"),
    )


def _commit(identity: object) -> tuple[object, ...]:
    if type(identity) is not RealManifestCommitIdentity:
        raise RealManifestDomainTemplateError("commit_identity_invalid")
    if type(identity.changed_paths) is not tuple or not identity.changed_paths:
        raise RealManifestDomainTemplateError("commit_identity_invalid")
    paths = tuple(_repo_path(path) for path in identity.changed_paths)
    if len(paths) != len(set(paths)) or tuple(sorted(paths)) != paths:
        raise RealManifestDomainTemplateError("commit_identity_invalid")
    return (
        _sha(identity.commit, _SHA40, "commit_identity_invalid"),
        _sha(identity.parent, _SHA40, "commit_identity_invalid"),
        _plain(identity.subject, "commit_identity_invalid"),
        paths,
        _sha(identity.full_patch_sha256, _SHA64, "sha256_invalid"),
    )


def _input(identity: object, label: str) -> tuple[object, ...]:
    if type(identity) is not RealManifestInputIdentity:
        raise RealManifestDomainTemplateError("input_identity_invalid")
    if identity.label != label:
        raise RealManifestDomainTemplateError("input_identity_invalid")
    path = _absolute(identity.path, "path_not_absolute")
    root = _absolute(identity.root_path, "path_not_absolute")
    if str(PurePosixPath(path).parent) != root:
        raise RealManifestDomainTemplateError("path_not_direct_child")
    if identity.mode != _MODE_FILE or identity.root_mode != _MODE_ROOT:
        raise RealManifestDomainTemplateError("mode_invalid")
    if identity.device != identity.root_device:
        raise RealManifestDomainTemplateError("input_identity_invalid")
    return (
        label, path, root, _positive(identity.byte_count, "byte_count_invalid"),
        _sha(identity.sha256, _SHA64, "sha256_invalid"),
        _positive(identity.device, "input_identity_invalid"), identity.mode,
        _positive(identity.inode, "input_identity_invalid"),
        _positive(identity.root_device, "input_identity_invalid"),
        _positive(identity.root_inode, "input_identity_invalid"), identity.root_mode,
    )


def build_real_manifest_domain_template(
    spec: RealManifestDomainTemplateSpec,
) -> RealManifestDomainTemplateBundle:
    """Build byte-exact controller input without filesystem, process, or Git effects."""

    if type(spec) is not RealManifestDomainTemplateSpec:
        raise RealManifestDomainTemplateError("invalid_spec")
    if spec.reference_task_id != _REFERENCE_TASK:
        raise RealManifestDomainTemplateError("reference_task_mismatch")
    if spec.contract_id != _CONTRACT:
        raise RealManifestDomainTemplateError("contract_mismatch")
    activation = _commit(spec.activation)
    if type(spec.baseline) is not RealManifestBaselineIdentity:
        raise RealManifestDomainTemplateError("baseline_identity_invalid")
    baseline = spec.baseline
    seam = tuple(_git_path(item) for item in baseline.seam_chain) if type(baseline.seam_chain) is tuple else ()
    if len(seam) != 2 or tuple(item[0] for item in seam) != (baseline.helper_path, baseline.test_path):
        raise RealManifestDomainTemplateError("baseline_identity_invalid")
    baseline_value = (
        _sha(baseline.release_checkpoint, _SHA40, "baseline_identity_invalid"),
        _sha(baseline.helper_v1, _SHA40, "baseline_identity_invalid"),
        _sha(baseline.integration, _SHA40, "baseline_identity_invalid"),
        _repo_path(baseline.helper_path), _repo_path(baseline.test_path), seam,
        _sha(baseline.governance_manifest_sha256, _SHA64, "sha256_invalid"),
        _sha(baseline.guide_sha256, _SHA64, "sha256_invalid"),
        _sha(baseline.lineage_owner_decision_evidence_sha256, _SHA64, "sha256_invalid"),
        _sha(baseline.advisor_attachment_sha256, _SHA64, "sha256_invalid"),
        _plain(baseline.human_governance_override, "baseline_identity_invalid"),
        _plain(baseline.helper_disposition, "baseline_identity_invalid"),
    )
    if type(spec.c1_inputs) is not tuple or len(spec.c1_inputs) != 4:
        raise RealManifestDomainTemplateError("c1_cardinality_mismatch")
    if tuple(item.label if type(item) is RealManifestInputIdentity else None for item in spec.c1_inputs) != _C1_LABELS:
        raise RealManifestDomainTemplateError("c1_label_mismatch")
    if type(spec.retained_inputs) is not tuple or len(spec.retained_inputs) != 3:
        raise RealManifestDomainTemplateError("retained_cardinality_mismatch")
    if tuple(item.label if type(item) is RealManifestInputIdentity else None for item in spec.retained_inputs) != _RETAINED_LABELS:
        raise RealManifestDomainTemplateError("retained_label_mismatch")
    c1_inputs = tuple(_input(item, label) for item, label in zip(spec.c1_inputs, _C1_LABELS, strict=True))
    retained_inputs = tuple(_input(item, label) for item, label in zip(spec.retained_inputs, _RETAINED_LABELS, strict=True))
    source_path = _absolute(spec.source_path, "source_path_invalid")
    output_root = _absolute(spec.output_root, "output_root_invalid")
    repo_root = _absolute(spec.repo_root, "repo_root_invalid")
    paths = tuple(item[1] for item in c1_inputs + retained_inputs) + (source_path, output_root)
    if len(paths) != len(set(paths)):
        raise RealManifestDomainTemplateError("path_collision")
    expected_argv = (repo_root + "/.venv/bin/python", "-")
    if spec.process_argv != expected_argv:
        raise RealManifestDomainTemplateError("process_argv_mismatch")
    facts = tuple(sorted((
        ("activation", activation), ("artifact_names", _ARTIFACT_NAMES),
        ("baseline", baseline_value), ("c1_inputs", c1_inputs),
        ("contract_id", spec.contract_id),
        ("git_targets", (activation[0], activation[1], baseline_value[0], baseline_value[1], baseline_value[2], seam[0][1], seam[1][1])),
        ("lifecycle_order", _LIFECYCLE_ORDER), ("output_root", output_root),
        ("reference_task_id", spec.reference_task_id), ("repo_root", repo_root),
        ("retained_inputs", retained_inputs), ("retry", 0), ("fallback", 0),
        ("source_path", source_path),
    ), key=lambda item: item[0].encode("utf-8")))
    replacement = ("REAL_MANIFEST_CONTRACT = " + _literal(facts) + "\n").encode("utf-8")
    try:
        text = _CANONICAL_TEMPLATE.decode("utf-8", errors="strict")
        compile(ast.parse(text), "<real-manifest-domain-template>", "exec")
    except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
        raise RealManifestDomainTemplateError("canonical_template_invalid") from exc
    request = ControllerRuntimeRequest(
        template_source=_CANONICAL_TEMPLATE,
        assignment_name="REAL_MANIFEST_CONTRACT",
        validation_function="require_real_manifest_contract",
        replacement_statement=replacement,
        source_path=source_path,
        process_argv=expected_argv,
    )
    return RealManifestDomainTemplateBundle(
        template_source=_CANONICAL_TEMPLATE,
        template_sha256=hashlib.sha256(_CANONICAL_TEMPLATE).hexdigest(),
        replacement_statement=replacement,
        replacement_sha256=hashlib.sha256(replacement).hexdigest(),
        runtime_request=request,
        expected_bound_results=76,
        expected_artifact_names=_ARTIFACT_NAMES,
        expected_lifecycle_order=_LIFECYCLE_ORDER,
    )
