"""Deterministic, effect-free construction of the retained-R3 controller domain."""

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
    "ControllerDomainTemplateError",
    "ControllerDomainTemplateSpec",
    "ControllerDomainTemplateBundle",
    "build_controller_domain_template",
]

_SHA40 = re.compile(r"[0-9a-f]{40}")
_SHA64 = re.compile(r"[0-9a-f]{64}")
_REFERENCE_TASK = "REF-P7-25-R2-B2-P6"
_CONTRACT = "P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1"
_ACTIVATION_SUBJECT = "chore(plan): activate p6 domain template owner"
_ACTIVATION_PATHS = (
    ".agent-work/FULL_PLAN_REFERENCE.md",
    ".agent-work/PLAN.md",
    ".agent-work/PLANS/20260731-1549-p7-retained-r3-b2-p5-i1-domain-template-gap-review.md",
)
_RUNTIME_PATHS = (
    "src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py",
    "tests/test_p7_retained_r3_controller_runtime.py",
)
_ARTIFACT_NAMES = (
    "synthetic-plan.json", "synthetic-full.json", "synthetic-lineage.json",
    "synthetic-seal.json", "integration-qualification.json",
    "integration-qualification.sha256.json", "terminal-evidence.json",
    "terminal-evidence.sha256.json", "execution-result-admission.json",
)
_LIFECYCLE_ORDER = (
    "conformance", "activation", "root", "inputs", "evaluate",
    "terminal", "terminal_seal", "admission",
)


class ControllerDomainTemplateError(ValueError):
    """Fail-closed builder failure carrying one stable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ControllerDomainTemplateSpec:
    reference_task_id: str
    contract_id: str
    activation_commit: str
    activation_parent: str
    activation_subject: str
    activation_paths: tuple[str, ...]
    runtime_commit: str
    runtime_parent: str
    runtime_source_blob_oid: str
    runtime_source_sha256: str
    runtime_test_blob_oid: str
    runtime_test_sha256: str
    source_path: str
    output_root: str
    repo_root: str
    process_argv: tuple[str, ...]


@dataclass(frozen=True)
class ControllerDomainTemplateBundle:
    template_source: bytes
    template_sha256: str
    replacement_statement: bytes
    replacement_sha256: str
    runtime_request: ControllerRuntimeRequest
    expected_bound_results: int
    expected_artifact_names: tuple[str, ...]
    expected_lifecycle_order: tuple[str, ...]


_CANONICAL_TEMPLATE = b'''from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import LifecycleCallbacks, LifecycleRequirements, RootIdentityChain, execute_controller_lifecycle, validate_root_identity_chain
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation import ByteSpan, OwnedStatementPair, PreparedControllerSource, SealTargetIdentity
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import DirectoryIdentity, FileIdentity, create_exclusive_root, read_exact_file, run_read_only_git

def require_activation_contract(value):
    if type(value) is not tuple or not value:
        raise RuntimeError("activation_contract_invalid")
    return value

def controller():
    ACTIVATION_CONTRACT = (("placeholder", True),)
    require_activation_contract(ACTIVATION_CONTRACT)
    activation_commit_ledger = run_read_only_git(REPO_ROOT, ("git", "rev-parse", "--verify", ACTIVATION_COMMIT + "^{commit}"))
    activation_metadata_ledger = run_read_only_git(REPO_ROOT, ("git", "show", "-s", "--format=%H%x00%P%x00%s", ACTIVATION_COMMIT))
    activation_paths_ledger = run_read_only_git(REPO_ROOT, ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", ACTIVATION_COMMIT))
    runtime_metadata_ledger = run_read_only_git(REPO_ROOT, ("git", "show", "-s", "--format=%H%x00%P%x00%s", RUNTIME_COMMIT))
    runtime_paths_ledger = run_read_only_git(REPO_ROOT, ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", RUNTIME_COMMIT))
    runtime_patch_ledger = run_read_only_git(REPO_ROOT, ("git", "diff", "--binary", "--full-index", "--no-ext-diff", RUNTIME_PARENT, RUNTIME_COMMIT, "--", RUNTIME_PATHS[0], RUNTIME_PATHS[1]))
    root_identity = create_exclusive_root(OUTPUT_ROOT)
    synthetic_plan_identity = read_exact_file(OUTPUT_ROOT + "/synthetic-plan.json", root=root_identity)
    synthetic_full_identity = read_exact_file(OUTPUT_ROOT + "/synthetic-full.json", root=root_identity)
    synthetic_lineage_identity = read_exact_file(OUTPUT_ROOT + "/synthetic-lineage.json", root=root_identity)
    synthetic_seal_identity = read_exact_file(OUTPUT_ROOT + "/synthetic-seal.json", root=root_identity)
    integration_qualification_identity = read_exact_file(OUTPUT_ROOT + "/integration-qualification.json", root=root_identity)
    terminal_evidence_identity = read_exact_file(OUTPUT_ROOT + "/terminal-evidence.json", root=root_identity)
    execution_result_admission_identity = read_exact_file(OUTPUT_ROOT + "/execution-result-admission.json", root=root_identity)
    fixture_root = DirectoryIdentity(path="/fixture", device=7, inode=9, mode=448)
    fixture_file = FileIdentity(path="/fixture/value", data=b"x", byte_count=1, sha256="2d711642b726b04401627ca9fbac32f5da7e5c8530fb1903cc4db02258717921", device=7, inode=10, mode=384, root=fixture_root)
    fixture_span = ByteSpan(start=0, end=1)
    fixture_target = SealTargetIdentity(path="/fixture/value", byte_count=1, sha256="2d711642b726b04401627ca9fbac32f5da7e5c8530fb1903cc4db02258717921", device=7, inode=10)
    root_chain = RootIdentityChain(before=root_identity, files=(synthetic_plan_identity, synthetic_full_identity, synthetic_lineage_identity, synthetic_seal_identity), after=root_identity)
    validate_root_identity_chain(root_chain)
    semantic_matrix = (
        ("activation_commit", activation_commit_ledger.exit_code == 0),
        ("activation_metadata", activation_metadata_ledger.exit_code == 0),
        ("activation_paths", activation_paths_ledger.exit_code == 0),
        ("runtime_metadata", runtime_metadata_ledger.exit_code == 0),
        ("runtime_paths", runtime_paths_ledger.exit_code == 0),
        ("runtime_patch", runtime_patch_ledger.exit_code == 0),
        ("plan_same_root", synthetic_plan_identity.root == root_identity),
        ("full_same_root", synthetic_full_identity.root == root_identity),
        ("lineage_same_root", synthetic_lineage_identity.root == root_identity),
        ("seal_same_root", synthetic_seal_identity.root == root_identity),
        ("qualification_nonempty", integration_qualification_identity.byte_count > 0),
        ("terminal_nonempty", terminal_evidence_identity.byte_count > 0),
        ("admission_nonempty", execution_result_admission_identity.byte_count > 0),
        ("fixture_root_mode", fixture_root.mode == 448),
        ("fixture_file_hash", fixture_file.sha256 == fixture_target.sha256),
        ("fixture_span_exact", fixture_span.end > fixture_span.start),
    )
    artifact_names = ("synthetic-plan.json", "synthetic-full.json", "synthetic-lineage.json", "synthetic-seal.json", "integration-qualification.json", "integration-qualification.sha256.json", "terminal-evidence.json", "terminal-evidence.sha256.json", "execution-result-admission.json")
    persist_canonical_json(OUTPUT_ROOT, artifact_names[0], {"kind": "input"})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[1], {"kind": "input"})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[2], {"kind": "input"})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[3], {"kind": "input"})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[4], {"matrix": semantic_matrix})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[5], {"target": artifact_names[4]})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[6], {"status": "synthetic_controller_qualified"})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[7], {"target": artifact_names[6]})
    persist_canonical_json(OUTPUT_ROOT, artifact_names[8], {"admitted": True})
    callbacks = LifecycleCallbacks(conformance=phase_conformance, activation=phase_activation, root=phase_root, inputs=phase_inputs, evaluate=phase_evaluate, terminal=phase_terminal, terminal_seal=phase_terminal_seal, admission=phase_admission)
    lifecycle_result = execute_controller_lifecycle(callbacks, LifecycleRequirements(success_order=("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission"), retry=0, fallback=0))
    return lifecycle_result.order == ("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission") and len(artifact_names) == 9 and len(semantic_matrix) == 16
'''


def _plain(value: object, code: str) -> str:
    if type(value) is not str or not value or "\x00" in value or "\n" in value or "\r" in value:
        raise ControllerDomainTemplateError(code)
    return value


def _absolute(value: object, code: str) -> str:
    text = _plain(value, code)
    path = PurePosixPath(text)
    if not path.is_absolute() or str(path) != text or any(part in {".", ".."} for part in path.parts):
        raise ControllerDomainTemplateError(code)
    return text


def _sha(value: object, pattern: re.Pattern[str], code: str) -> str:
    if type(value) is not str or pattern.fullmatch(value) is None:
        raise ControllerDomainTemplateError(code)
    return value


def _literal(value: object) -> str:
    if type(value) in (str, bool, int):
        if type(value) is str:
            _plain(value, "literal_string_invalid")
        return repr(value)
    if type(value) is tuple:
        body = ", ".join(_literal(item) for item in value)
        return "(" + body + ("," if len(value) == 1 else "") + ")"
    raise ControllerDomainTemplateError("literal_type_invalid")


def build_controller_domain_template(spec: ControllerDomainTemplateSpec) -> ControllerDomainTemplateBundle:
    """Return one immutable byte-exact controller request without effects."""

    if type(spec) is not ControllerDomainTemplateSpec:
        raise ControllerDomainTemplateError("invalid_spec")
    if spec.reference_task_id != _REFERENCE_TASK:
        raise ControllerDomainTemplateError("reference_task_mismatch")
    if spec.contract_id != _CONTRACT:
        raise ControllerDomainTemplateError("contract_mismatch")
    activation_commit = _sha(spec.activation_commit, _SHA40, "activation_commit_invalid")
    activation_parent = _sha(spec.activation_parent, _SHA40, "activation_parent_invalid")
    if spec.activation_subject != _ACTIVATION_SUBJECT:
        raise ControllerDomainTemplateError("activation_subject_mismatch")
    if spec.activation_paths != _ACTIVATION_PATHS:
        raise ControllerDomainTemplateError("activation_paths_mismatch")
    runtime_commit = _sha(spec.runtime_commit, _SHA40, "runtime_commit_invalid")
    runtime_parent = _sha(spec.runtime_parent, _SHA40, "runtime_parent_invalid")
    source_blob = _sha(spec.runtime_source_blob_oid, _SHA40, "runtime_source_blob_invalid")
    source_sha = _sha(spec.runtime_source_sha256, _SHA64, "runtime_source_sha_invalid")
    test_blob = _sha(spec.runtime_test_blob_oid, _SHA40, "runtime_test_blob_invalid")
    test_sha = _sha(spec.runtime_test_sha256, _SHA64, "runtime_test_sha_invalid")
    source_path = _absolute(spec.source_path, "source_path_invalid")
    output_root = _absolute(spec.output_root, "output_root_invalid")
    repo_root = _absolute(spec.repo_root, "repo_root_invalid")
    expected_argv = (repo_root + "/.venv/bin/python", "-")
    if spec.process_argv != expected_argv:
        raise ControllerDomainTemplateError("process_argv_mismatch")
    facts = tuple(sorted((
        ("activation_commit", activation_commit), ("activation_parent", activation_parent),
        ("activation_paths", spec.activation_paths), ("activation_subject", spec.activation_subject),
        ("artifact_names", _ARTIFACT_NAMES), ("contract_id", spec.contract_id),
        ("effect_bindings", 14), ("expected_bound_results", 18),
        ("fixture_bindings", 4), ("lifecycle_order", _LIFECYCLE_ORDER),
        ("matrix_cases", 16), ("output_root", output_root), ("reference_task_id", spec.reference_task_id),
        ("repo_root", repo_root), ("retry", 0), ("fallback", 0),
        ("root_reads", 7), ("runtime_commit", runtime_commit), ("runtime_parent", runtime_parent),
        ("runtime_paths", _RUNTIME_PATHS), ("runtime_source_blob_oid", source_blob),
        ("runtime_source_sha256", source_sha), ("runtime_test_blob_oid", test_blob),
        ("runtime_test_sha256", test_sha), ("source_path", source_path),
    ), key=lambda item: item[0].encode("utf-8")))
    replacement = ("    ACTIVATION_CONTRACT = " + _literal(facts) + "\n").encode("utf-8")
    try:
        text = _CANONICAL_TEMPLATE.decode("utf-8", errors="strict")
        compile(ast.parse(text), "<controller-domain-template>", "exec")
    except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
        raise ControllerDomainTemplateError("canonical_template_invalid") from exc
    request = ControllerRuntimeRequest(
        template_source=_CANONICAL_TEMPLATE,
        assignment_name="ACTIVATION_CONTRACT",
        validation_function="require_activation_contract",
        replacement_statement=replacement,
        source_path=source_path,
        process_argv=expected_argv,
    )
    return ControllerDomainTemplateBundle(
        template_source=_CANONICAL_TEMPLATE,
        template_sha256=hashlib.sha256(_CANONICAL_TEMPLATE).hexdigest(),
        replacement_statement=replacement,
        replacement_sha256=hashlib.sha256(replacement).hexdigest(),
        runtime_request=request,
        expected_bound_results=18,
        expected_artifact_names=_ARTIFACT_NAMES,
        expected_lifecycle_order=_LIFECYCLE_ORDER,
    )
