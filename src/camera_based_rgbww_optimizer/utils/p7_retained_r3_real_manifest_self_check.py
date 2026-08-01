"""Typed, pure in-memory validation of subordinate real-manifest evidence."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import PurePosixPath
import re
from typing import Any, Callable, Mapping

from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
    ProvenanceIOError,
    canonical_json_bytes,
    decode_canonical_json,
    run_read_only_git,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_real_manifest_domain_template import (
    RealManifestBaselineIdentity,
    RealManifestCommitIdentity,
    RealManifestGitPathIdentity,
    RealManifestInputIdentity,
)

__all__ = [
    "RealManifestSelfCheckError",
    "RealManifestGitFileBytes",
    "RealManifestSelfCheckSpec",
    "RealManifestSelfCheckReport",
    "required_real_manifest_git_argv",
    "run_real_manifest_self_check",
]


_SHA40 = re.compile(r"[0-9a-f]{40}")
_SHA64 = re.compile(r"[0-9a-f]{64}")
_ROLE_NAMES = (
    ("manifest", "retained-r3-audit-provenance-manifest-v2.json"),
    ("manifest_seal", "retained-r3-audit-provenance-manifest-v2.sha256.json"),
    ("terminal", "terminal-evidence.json"),
    ("terminal_seal", "terminal-evidence.sha256.json"),
    ("admission", "execution-result-admission.json"),
)
_MANIFEST_SCHEMA = "p7_retained_r3_audit_provenance_manifest_v2"
_SUCCESS_STATUS = "sealed_subordinate_provenance_evidence"
_C1_LABELS = (
    "path_owner_index",
    "path_owner_index_seal",
    "terminal_evidence",
    "terminal_evidence_seal",
)
_RETAINED_LABELS = (
    "current_lineage_candidate",
    "resolved_formal_plan",
    "setup_lineage_release",
)


class RealManifestSelfCheckError(RuntimeError):
    """Fail-closed error with a stable machine-readable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class RealManifestGitFileBytes:
    commit: str
    repo_path: str
    data: bytes


@dataclass(frozen=True)
class RealManifestSelfCheckSpec:
    reference_task_id: str
    contract_id: str
    repo_root: str
    artifacts: tuple[FileIdentity, ...]
    activation: RealManifestCommitIdentity
    baseline: RealManifestBaselineIdentity
    c1_inputs: tuple[RealManifestInputIdentity, ...]
    retained_inputs: tuple[RealManifestInputIdentity, ...]
    git_file_bytes: tuple[RealManifestGitFileBytes, ...]


@dataclass(frozen=True)
class RealManifestSelfCheckReport:
    reference_task_id: str
    contract_id: str
    status: str
    artifact_facts: tuple[tuple[str, str, int, str], ...]
    git_ledger_facts: tuple[
        tuple[tuple[str, ...], str, int, str, str], ...
    ]
    ordered_git_argv: tuple[tuple[str, ...], ...]
    git_stdout_sha256: tuple[str, ...]
    git_file_facts: tuple[tuple[str, str, int, str, str], ...]
    eligibility: bool
    release_consumable: bool
    authority: str
    canonical_report_bytes: bytes
    canonical_report_sha256: str


def _fail(code: str) -> None:
    raise RealManifestSelfCheckError(code)


def _plain(value: Any) -> bool:
    return type(value) is str and bool(value) and not any(
        token in value for token in ("\x00", "\n", "\r")
    )


def _repo_path(value: Any) -> bool:
    if not _plain(value):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and str(path) == value
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _absolute(value: Any) -> bool:
    if not _plain(value):
        return False
    path = PurePosixPath(value)
    return (
        path.is_absolute()
        and str(path) == value
        and all(part not in {".", ".."} for part in path.parts)
    )


def _exact(left: Any, right: Any) -> bool:
    if isinstance(left, Mapping) or isinstance(right, Mapping):
        if not isinstance(left, Mapping) or not isinstance(right, Mapping):
            return False
        if set(left) != set(right):
            return False
        return all(_exact(left[key], right[key]) for key in left)
    if type(left) in (tuple, list) or type(right) in (tuple, list):
        if type(left) not in (tuple, list) or type(right) not in (tuple, list):
            return False
        return len(left) == len(right) and all(
            _exact(a, b) for a, b in zip(left, right, strict=True)
        )
    if type(left) is not type(right):
        return False
    return left == right


def _json_native(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _json_native(item) for key, item in value.items()}
    if type(value) in (tuple, list):
        return [_json_native(item) for item in value]
    if value is None or type(value) in (bool, int, str):
        return value
    _fail("report_json_invalid")


def _git_blob_oid(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def _input_row(identity: RealManifestInputIdentity) -> tuple[Any, ...]:
    if type(identity) is not RealManifestInputIdentity:
        _fail("typed_identity_invalid")
    if (
        not _plain(identity.label)
        or not _absolute(identity.path)
        or not _absolute(identity.root_path)
        or str(PurePosixPath(identity.path).parent) != identity.root_path
        or type(identity.byte_count) is not int
        or identity.byte_count <= 0
        or _SHA64.fullmatch(identity.sha256) is None
        or any(type(value) is not int or value <= 0 for value in (
            identity.device, identity.inode, identity.root_device, identity.root_inode,
        ))
        or identity.mode != 0o600
        or identity.root_mode != 0o700
        or identity.device != identity.root_device
    ):
        _fail("typed_identity_invalid")
    return (
        identity.label,
        identity.path,
        identity.root_path,
        identity.byte_count,
        identity.sha256,
        identity.device,
        identity.mode,
        identity.inode,
        identity.root_device,
        identity.root_inode,
        identity.root_mode,
    )


def _commit_row(identity: RealManifestCommitIdentity) -> tuple[Any, ...]:
    if type(identity) is not RealManifestCommitIdentity:
        _fail("typed_identity_invalid")
    if (
        _SHA40.fullmatch(identity.commit) is None
        or _SHA40.fullmatch(identity.parent) is None
        or not _plain(identity.subject)
        or type(identity.changed_paths) is not tuple
        or not identity.changed_paths
        or any(not _repo_path(path) for path in identity.changed_paths)
        or tuple(sorted(identity.changed_paths)) != identity.changed_paths
        or len(set(identity.changed_paths)) != len(identity.changed_paths)
        or _SHA64.fullmatch(identity.full_patch_sha256) is None
    ):
        _fail("typed_identity_invalid")
    return (
        identity.commit,
        identity.parent,
        identity.subject,
        identity.changed_paths,
        identity.full_patch_sha256,
    )


def _seam_row(identity: RealManifestGitPathIdentity) -> tuple[Any, ...]:
    if type(identity) is not RealManifestGitPathIdentity:
        _fail("typed_identity_invalid")
    if (
        not _repo_path(identity.repo_path)
        or _SHA40.fullmatch(identity.before_blob_oid) is None
        or _SHA40.fullmatch(identity.after_blob_oid) is None
        or any(_SHA64.fullmatch(value) is None for value in (
            identity.before_sha256,
            identity.after_sha256,
            identity.binary_patch_sha256,
        ))
    ):
        _fail("typed_identity_invalid")
    return (
        identity.repo_path,
        identity.before_blob_oid,
        identity.after_blob_oid,
        identity.before_sha256,
        identity.after_sha256,
        identity.binary_patch_sha256,
    )


def _baseline_row(identity: RealManifestBaselineIdentity) -> tuple[Any, ...]:
    if type(identity) is not RealManifestBaselineIdentity:
        _fail("typed_identity_invalid")
    if (
        any(_SHA40.fullmatch(value) is None for value in (
            identity.release_checkpoint,
            identity.helper_v1,
            identity.integration,
        ))
        or not _repo_path(identity.helper_path)
        or not _repo_path(identity.test_path)
        or type(identity.seam_chain) is not tuple
        or len(identity.seam_chain) != 2
        or tuple(item.repo_path for item in identity.seam_chain) != (
            identity.helper_path,
            identity.test_path,
        )
        or any(_SHA64.fullmatch(value) is None for value in (
            identity.governance_manifest_sha256,
            identity.guide_sha256,
            identity.lineage_owner_decision_evidence_sha256,
            identity.advisor_attachment_sha256,
        ))
        or not _plain(identity.human_governance_override)
        or not _plain(identity.helper_disposition)
    ):
        _fail("typed_identity_invalid")
    seams = tuple(_seam_row(item) for item in identity.seam_chain)
    return (
        identity.release_checkpoint,
        identity.helper_v1,
        identity.integration,
        identity.helper_path,
        identity.test_path,
        seams,
        identity.governance_manifest_sha256,
        identity.guide_sha256,
        identity.lineage_owner_decision_evidence_sha256,
        identity.advisor_attachment_sha256,
        identity.human_governance_override,
        identity.helper_disposition,
    )


def _validate_spec(spec: RealManifestSelfCheckSpec) -> tuple[
    tuple[Any, ...], tuple[Any, ...], tuple[tuple[Any, ...], ...], tuple[tuple[Any, ...], ...]
]:
    if type(spec) is not RealManifestSelfCheckSpec:
        _fail("invalid_spec")
    if not _plain(spec.reference_task_id):
        _fail("reference_task_invalid")
    if not _plain(spec.contract_id):
        _fail("contract_id_invalid")
    if not _absolute(spec.repo_root):
        _fail("repo_root_invalid")
    activation = _commit_row(spec.activation)
    baseline = _baseline_row(spec.baseline)
    if (
        spec.activation.commit == spec.activation.parent
        or len({
            spec.baseline.release_checkpoint,
            spec.baseline.helper_v1,
            spec.baseline.integration,
        }) != 3
        or spec.baseline.helper_path == spec.baseline.test_path
    ):
        _fail("typed_identity_invalid")
    if type(spec.c1_inputs) is not tuple or len(spec.c1_inputs) != 4:
        _fail("typed_identity_invalid")
    if type(spec.retained_inputs) is not tuple or len(spec.retained_inputs) != 3:
        _fail("typed_identity_invalid")
    c1 = tuple(_input_row(item) for item in spec.c1_inputs)
    retained = tuple(_input_row(item) for item in spec.retained_inputs)
    if tuple(item[0] for item in c1) != _C1_LABELS:
        _fail("typed_identity_invalid")
    if tuple(item[0] for item in retained) != _RETAINED_LABELS:
        _fail("typed_identity_invalid")
    if len({item[1] for item in c1 + retained}) != 7:
        _fail("typed_identity_invalid")
    return activation, baseline, c1, retained


def _artifact_values(
    artifacts: tuple[FileIdentity, ...],
    activation: tuple[Any, ...],
    baseline: tuple[Any, ...],
    c1: tuple[tuple[Any, ...], ...],
    retained: tuple[tuple[Any, ...], ...],
) -> tuple[tuple[str, str, int, str], ...]:
    if type(artifacts) is not tuple or len(artifacts) != len(_ROLE_NAMES):
        _fail("artifact_contract_invalid")
    if any(type(item) is not FileIdentity for item in artifacts):
        _fail("artifact_identity_invalid")
    roots = tuple(item.root for item in artifacts)
    if (
        type(roots[0]) is not DirectoryIdentity
        or any(root != roots[0] for root in roots)
    ):
        _fail("artifact_root_mismatch")
    root = roots[0]
    assert root is not None
    if (
        not _absolute(root.path)
        or type(root.device) is not int
        or root.device <= 0
        or type(root.inode) is not int
        or root.inode <= 0
        or root.mode != 0o700
    ):
        _fail("artifact_root_mismatch")
    if len({item.path for item in artifacts}) != len(artifacts):
        _fail("artifact_path_invalid")
    if len({(item.device, item.inode) for item in artifacts}) != len(artifacts):
        _fail("artifact_identity_invalid")

    decoded: list[Any] = []
    facts: list[tuple[str, str, int, str]] = []
    for (role, basename), item in zip(_ROLE_NAMES, artifacts, strict=True):
        root = item.root
        if (
            item.mode != 0o600
            or type(item.device) is not int
            or item.device <= 0
            or type(item.inode) is not int
            or item.inode <= 0
            or item.byte_count != len(item.data)
            or item.sha256 != hashlib.sha256(item.data).hexdigest()
            or root is None
            or item.device != root.device
        ):
            _fail("artifact_identity_invalid")
        path = PurePosixPath(item.path)
        if path.name != basename or str(path.parent) != root.path:
            _fail("artifact_path_invalid")
        try:
            value = decode_canonical_json(item.data)
        except ProvenanceIOError as exc:
            raise RealManifestSelfCheckError("artifact_json_invalid") from exc
        decoded.append(value)
        facts.append((role, basename, item.byte_count, item.sha256))

    manifest, manifest_seal, terminal, terminal_seal, admission = decoded
    expected_manifest = _json_native({
        "schema": _MANIFEST_SCHEMA,
        "status": _SUCCESS_STATUS,
        "activation": activation,
        "baseline": baseline,
        "c1": c1,
        "retained": retained,
    })
    if not _exact(manifest, expected_manifest):
        _fail("manifest_contract_mismatch")
    expected_manifest_seal = {
        "bytes": artifacts[0].byte_count,
        "sha256": artifacts[0].sha256,
        "target": _ROLE_NAMES[0][1],
    }
    if not _exact(manifest_seal, expected_manifest_seal):
        _fail("seal_contract_mismatch")
    if not _exact(terminal, {"status": _SUCCESS_STATUS}):
        _fail("terminal_contract_mismatch")
    expected_terminal_seal = {
        "bytes": artifacts[2].byte_count,
        "sha256": artifacts[2].sha256,
        "target": _ROLE_NAMES[2][1],
    }
    if not _exact(terminal_seal, expected_terminal_seal):
        _fail("seal_contract_mismatch")
    if not _exact(admission, {
        "admitted": True,
        "eligibility": False,
        "release_consumable": False,
    }):
        _fail("admission_contract_mismatch")
    return tuple(facts)


def _file_map(spec: RealManifestSelfCheckSpec) -> dict[tuple[str, str], bytes]:
    if type(spec.git_file_bytes) is not tuple or not spec.git_file_bytes:
        _fail("git_file_bytes_invalid")
    rows: list[tuple[str, str, bytes]] = []
    for item in spec.git_file_bytes:
        if (
            type(item) is not RealManifestGitFileBytes
            or _SHA40.fullmatch(item.commit) is None
            or not _repo_path(item.repo_path)
            or type(item.data) is not bytes
        ):
            _fail("git_file_bytes_invalid")
        rows.append((item.commit, item.repo_path, item.data))
    keys = tuple((commit, path) for commit, path, _data in rows)
    if keys != tuple(sorted(keys)) or len(set(keys)) != len(keys):
        _fail("git_file_bytes_invalid")
    activation = spec.activation
    baseline = spec.baseline
    expected_rows = (
        *((activation.parent, path) for path in activation.changed_paths),
        *((activation.commit, path) for path in activation.changed_paths),
        (baseline.helper_v1, baseline.helper_path),
        (baseline.helper_v1, baseline.test_path),
        (baseline.integration, baseline.helper_path),
        (baseline.integration, baseline.test_path),
    )
    if len(set(expected_rows)) != len(expected_rows):
        _fail("git_file_set_collision")
    expected = set(expected_rows)
    if set(keys) != expected:
        _fail("git_file_set_mismatch")
    result = {(commit, path): data for commit, path, data in rows}
    seam_pairs = (
        (baseline.seam_chain[0], baseline.helper_v1, baseline.integration),
        (baseline.seam_chain[1], baseline.helper_v1, baseline.integration),
    )
    for seam, before, after in seam_pairs:
        before_data = result[(before, seam.repo_path)]
        after_data = result[(after, seam.repo_path)]
        if (
            hashlib.sha256(before_data).hexdigest() != seam.before_sha256
            or hashlib.sha256(after_data).hexdigest() != seam.after_sha256
            or _git_blob_oid(before_data) != seam.before_blob_oid
            or _git_blob_oid(after_data) != seam.after_blob_oid
        ):
            _fail("seam_identity_mismatch")
    return result


def required_real_manifest_git_argv(
    spec: RealManifestSelfCheckSpec,
) -> tuple[tuple[str, ...], ...]:
    """Return the one deterministic, P3-allowlisted Git ledger order."""

    _validate_spec(spec)
    _file_map(spec)
    activation = spec.activation
    baseline = spec.baseline
    commands: list[tuple[str, ...]] = []
    for commit in (
        activation.commit,
        activation.parent,
        baseline.release_checkpoint,
        baseline.helper_v1,
        baseline.integration,
    ):
        commands.append(("git", "rev-parse", "--verify", commit + "^{commit}"))
    commands.extend((
        ("git", "show", "-s", "--format=%H%x00%P%x00%s", activation.commit),
        ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", activation.commit),
    ))
    for path in activation.changed_paths:
        commands.append(("git", "rev-parse", activation.parent + ":" + path))
        commands.append(("git", "rev-parse", activation.commit + ":" + path))
    commands.append((
        "git", "diff", "--binary", "--full-index", "--no-ext-diff",
        activation.parent, activation.commit, "--", *activation.changed_paths,
    ))
    for before, after, path in (
        (baseline.helper_v1, baseline.integration, baseline.helper_path),
        (baseline.helper_v1, baseline.integration, baseline.test_path),
    ):
        commands.append(("git", "rev-parse", before + ":" + path))
        commands.append(("git", "rev-parse", after + ":" + path))
        commands.append((
            "git", "diff", "--binary", "--full-index", "--no-ext-diff",
            before, after, "--", path,
        ))
    return tuple(commands)


def _runner(dependencies: Mapping[str, Callable[..., Any]] | None) -> Callable[..., Any]:
    if dependencies is None:
        return run_read_only_git
    if not isinstance(dependencies, Mapping) or set(dependencies) != {"run_git"}:
        _fail("git_dependency_invalid")
    runner = dependencies["run_git"]
    if not callable(runner):
        _fail("git_dependency_invalid")
    return runner


def _expected_stdout(
    argv: tuple[str, ...],
    spec: RealManifestSelfCheckSpec,
    files: Mapping[tuple[str, str], bytes],
) -> tuple[str, bytes | str]:
    activation = spec.activation
    baseline = spec.baseline
    if argv[:3] == ("git", "rev-parse", "--verify"):
        return "exact", argv[3][:-9].encode("ascii") + b"\n"
    if argv[:4] == ("git", "show", "-s", "--format=%H%x00%P%x00%s"):
        return "exact", (
            activation.commit.encode("ascii") + b"\x00"
            + activation.parent.encode("ascii") + b"\x00"
            + activation.subject.encode("utf-8") + b"\n"
        )
    if argv[:6] == ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z"):
        return "paths", b""
    if argv[:2] == ("git", "rev-parse"):
        commit, path = argv[2].split(":", 1)
        return "exact", _git_blob_oid(files[(commit, path)]).encode("ascii") + b"\n"
    if argv[:5] == ("git", "diff", "--binary", "--full-index", "--no-ext-diff"):
        parent, child = argv[5:7]
        if (parent, child) == (activation.parent, activation.commit):
            return "sha", activation.full_patch_sha256
        seam_key = (parent, child, argv[-1])
        if seam_key == (
            baseline.helper_v1, baseline.integration, baseline.helper_path
        ):
            return "sha", baseline.seam_chain[0].binary_patch_sha256
        if seam_key == (
            baseline.helper_v1, baseline.integration, baseline.test_path
        ):
            return "sha", baseline.seam_chain[1].binary_patch_sha256
        _fail("git_ledger_invalid")
    _fail("git_ledger_invalid")


def run_real_manifest_self_check(
    spec: RealManifestSelfCheckSpec,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> RealManifestSelfCheckReport:
    """Validate all in-memory facts and then execute one ordered Git ledger."""

    activation, baseline, c1, retained = _validate_spec(spec)
    artifact_facts = _artifact_values(
        spec.artifacts, activation, baseline, c1, retained
    )
    files = _file_map(spec)
    argv_rows = required_real_manifest_git_argv(spec)
    run_git = _runner(dependencies)
    ledgers: list[GitLedger] = []
    for argv in argv_rows:
        try:
            ledger = run_git(spec.repo_root, argv)
        except (ProvenanceIOError, OSError) as exc:
            raise RealManifestSelfCheckError("git_ledger_invalid") from exc
        if (
            type(ledger) is not GitLedger
            or ledger.argv != argv
            or ledger.cwd != spec.repo_root
            or type(ledger.exit_code) is not int
            or type(ledger.stdout) is not bytes
            or type(ledger.stderr) is not bytes
            or ledger.stdout_sha256 != hashlib.sha256(ledger.stdout).hexdigest()
            or ledger.stderr_sha256 != hashlib.sha256(ledger.stderr).hexdigest()
        ):
            _fail("git_ledger_invalid")
        if ledger.exit_code != 0 or ledger.stderr != b"":
            _fail("git_command_failed")
        kind, expected = _expected_stdout(argv, spec, files)
        if kind == "exact" and ledger.stdout != expected:
            _fail("git_stdout_mismatch")
        if kind == "sha" and ledger.stdout_sha256 != expected:
            _fail("git_stdout_mismatch")
        if kind == "paths":
            if not ledger.stdout.endswith(b"\x00"):
                _fail("git_stdout_mismatch")
            try:
                paths = tuple(
                    item.decode("utf-8", errors="strict")
                    for item in ledger.stdout[:-1].split(b"\x00")
                )
            except UnicodeDecodeError as exc:
                raise RealManifestSelfCheckError("git_stdout_mismatch") from exc
            if paths != spec.activation.changed_paths or len(set(paths)) != len(paths):
                _fail("git_stdout_mismatch")
        ledgers.append(ledger)

    git_file_facts = tuple(
        (
            commit,
            path,
            len(data),
            hashlib.sha256(data).hexdigest(),
            _git_blob_oid(data),
        )
        for (commit, path), data in sorted(files.items())
    )
    git_ledger_facts = tuple(
        (
            item.argv,
            item.cwd,
            item.exit_code,
            item.stdout_sha256,
            item.stderr_sha256,
        )
        for item in ledgers
    )
    payload = _json_native({
        "schema": "p7_retained_r3_real_manifest_self_check_report_v1",
        "status": "real_manifest_self_check_pass",
        "reference_task_id": spec.reference_task_id,
        "contract_id": spec.contract_id,
        "artifact_facts": artifact_facts,
        "manifest_facts": {
            "activation": activation,
            "baseline": baseline,
            "c1": c1,
            "retained": retained,
        },
        "git": {
            "ordered_argv": argv_rows,
            "stdout_sha256": tuple(item.stdout_sha256 for item in ledgers),
            "file_facts": git_file_facts,
            "ledger_facts": tuple(
                {
                    "argv": item.argv,
                    "cwd": item.cwd,
                    "exit_code": item.exit_code,
                    "stdout_sha256": item.stdout_sha256,
                    "stderr_sha256": item.stderr_sha256,
                }
                for item in ledgers
            ),
        },
        "eligibility": False,
        "release_consumable": False,
        "authority": "subordinate_self_check_only",
    })
    report_bytes = canonical_json_bytes(payload)
    try:
        decoded_report = decode_canonical_json(report_bytes)
    except ProvenanceIOError as exc:
        raise RealManifestSelfCheckError("report_json_invalid") from exc
    if not _exact(decoded_report, payload):
        _fail("report_json_invalid")
    if canonical_json_bytes(_json_native(decoded_report)) != report_bytes:
        _fail("report_json_invalid")
    return RealManifestSelfCheckReport(
        spec.reference_task_id,
        spec.contract_id,
        "real_manifest_self_check_pass",
        artifact_facts,
        git_ledger_facts,
        argv_rows,
        tuple(item.stdout_sha256 for item in ledgers),
        git_file_facts,
        False,
        False,
        "subordinate_self_check_only",
        report_bytes,
        hashlib.sha256(report_bytes).hexdigest(),
    )
