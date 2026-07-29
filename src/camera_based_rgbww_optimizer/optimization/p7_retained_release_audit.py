"""Fail-closed retained P7 release evidence auditing.

This module deliberately owns filesystem acquisition, canonical persistence,
structural auditing, and terminal sealing.  Scientific lineage meaning remains
owned by the callbacks supplied by the existing P7 lineage implementation.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping


SOURCE_NAMES = (
    "current-lineage-candidate.json",
    "resolved-formal-plan.json",
    "setup-lineage-release.json",
)
PROGRESSIVE_NAMES = (
    "00-owner-root-identity.json",
    "01-dependency-audit.json",
    "02-source-before-manifest.json",
    "03-schema-audit.json",
    "04-semantic-callback-results.json",
    "05-source-after-manifest.json",
    "06-immutability-result.json",
    "07-strict-preterminal-audit.json",
    "08-validation-summary.json",
)
TERMINAL_NAME = "09-terminal-summary.json"
_CANDIDATE_SCHEMA = "p7_td_b_current_lineage_candidate_v1"
_RESOLVED_SCHEMA = "p7_td_b_resolved_formal_plan_v1"
_RELEASE_SCHEMA = "p7_td_b_setup_lineage_release_v1"


class RetainedReleaseAuditError(RuntimeError):
    """A retained-release audit failed after preserving available evidence."""

    def __init__(
        self,
        message: str,
        *,
        root: Path | None = None,
        primary: BaseException | None = None,
        seal_failure: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.root = root
        self.primary = primary
        self.seal_failure = seal_failure


@dataclass(frozen=True)
class _DirectoryIdentity:
    device: int
    inode: int
    mode: int

    def jsonable(self) -> dict[str, int]:
        return {"device": self.device, "inode": self.inode, "mode": self.mode}


@dataclass(frozen=True)
class _FileIdentity:
    device: int
    inode: int
    mode: int
    bytes: int
    sha256: str

    def jsonable(self, *, path: str) -> dict[str, Any]:
        return {
            "path": path,
            "device": self.device,
            "inode": self.inode,
            "mode": self.mode,
            "bytes": self.bytes,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class _Dependencies:
    path: Callable[[Any], Path]
    lstat: Callable[[Any], os.stat_result]
    mkdir: Callable[[Any, int], None]
    open_fd: Callable[[Any, int, int], int]
    write_fd: Callable[[int, bytes | memoryview], int]
    fsync_fd: Callable[[int], None]
    close_fd: Callable[[int], None]
    sha256: Callable[[bytes], Any]
    json_dumps: Callable[..., str]
    json_loads: Callable[..., Any]
    is_dir: Callable[[int], bool]
    is_regular: Callable[[int], bool]
    phase_hook: Callable[[str, Mapping[str, Any]], None]


def _noop_hook(_phase: str, _context: Mapping[str, Any]) -> None:
    return None


def _default_dependencies() -> _Dependencies:
    return _Dependencies(
        path=Path,
        lstat=os.lstat,
        mkdir=lambda path, mode: os.mkdir(path, mode),
        open_fd=os.open,
        write_fd=os.write,
        fsync_fd=os.fsync,
        close_fd=os.close,
        sha256=hashlib.sha256,
        json_dumps=json.dumps,
        json_loads=json.loads,
        is_dir=stat.S_ISDIR,
        is_regular=stat.S_ISREG,
        phase_hook=_noop_hook,
    )


def _build_dependencies(overrides: Mapping[str, Any] | None) -> tuple[_Dependencies, dict[str, Any]]:
    values = vars(_default_dependencies()).copy()
    unknown = set(overrides or ()) - set(values)
    if unknown:
        raise RetainedReleaseAuditError(f"unknown dependency overrides: {sorted(unknown)}")
    values.update(dict(overrides or {}))
    missing = sorted(name for name, value in values.items() if not callable(value))
    if missing:
        raise RetainedReleaseAuditError(
            f"required semantic dependencies are not callable: {missing}"
        )
    dependencies = _Dependencies(**values)

    # Exercise only capabilities that cannot mutate filesystem state.  This
    # validates behavior rather than implementation provenance metadata.
    probe = dependencies.path("semantic-probe")
    if not isinstance(probe, Path) or probe.name != "semantic-probe":
        raise RetainedReleaseAuditError("path coercion/relative-child capability differs")
    if not dependencies.is_dir(stat.S_IFDIR | 0o700):
        raise RetainedReleaseAuditError("directory-mode predicate capability differs")
    if not dependencies.is_regular(stat.S_IFREG | 0o600):
        raise RetainedReleaseAuditError("regular-file predicate capability differs")
    digest = dependencies.sha256(b"semantic-probe")
    if not callable(getattr(digest, "hexdigest", None)):
        raise RetainedReleaseAuditError("SHA-256 capability differs")
    encoded = dependencies.json_dumps(
        {"b": 2, "a": 1},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    if encoded != '{"a":1,"b":2}':
        raise RetainedReleaseAuditError("canonical JSON encode capability differs")
    decoded = dependencies.json_loads(encoded)
    if decoded != {"a": 1, "b": 2}:
        raise RetainedReleaseAuditError("strict JSON decode capability differs")
    return dependencies, {
        "status": "pass",
        "required_capability_count": len(values),
        "missing_capabilities": [],
        "metadata_provenance_gates": 0,
    }


def _canonical_json_bytes(value: Any, dependencies: _Dependencies) -> bytes:
    encoded = dependencies.json_dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    if not isinstance(encoded, str):
        raise TypeError("canonical JSON encoder must return str")
    return encoded.encode("utf-8") + b"\n"


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _strict_json_load(data: bytes, dependencies: _Dependencies) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
        value = dependencies.json_loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"strict JSON decode failed: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("strict JSON root must be an object")
    return value


def _direct_child_name(value: str, *, label: str) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."}:
        raise RetainedReleaseAuditError(f"{label} must be a non-empty direct-child name")
    if (
        PurePosixPath(value).is_absolute()
        or "/" in value
        or "\\" in value
        or os.sep in value
        or (os.altsep is not None and os.altsep in value)
    ):
        raise RetainedReleaseAuditError(f"{label} must be a direct-child name")
    return value


def _directory_identity(
    path: Path,
    dependencies: _Dependencies,
    *,
    expected_mode: int | None = None,
) -> _DirectoryIdentity:
    try:
        observed = dependencies.lstat(path)
    except FileNotFoundError as exc:
        raise RetainedReleaseAuditError(f"required directory is absent: {path}") from exc
    if not dependencies.is_dir(observed.st_mode) or stat.S_ISLNK(observed.st_mode):
        raise RetainedReleaseAuditError(f"directory owner is not a no-follow directory: {path}")
    mode = stat.S_IMODE(observed.st_mode)
    if expected_mode is not None and mode != expected_mode:
        raise RetainedReleaseAuditError(
            f"directory mode differs for {path}: {mode:o} != {expected_mode:o}"
        )
    return _DirectoryIdentity(observed.st_dev, observed.st_ino, mode)


def _assert_directory_identity(
    path: Path,
    frozen: _DirectoryIdentity,
    dependencies: _Dependencies,
) -> None:
    current = _directory_identity(path, dependencies, expected_mode=frozen.mode)
    if current != frozen:
        raise RetainedReleaseAuditError(f"directory identity drifted: {path}")


def _require_absent(path: Path, dependencies: _Dependencies) -> None:
    try:
        dependencies.lstat(path)
    except FileNotFoundError:
        return
    raise RetainedReleaseAuditError(f"acquisition target already exists: {path}")


def _acquire_directories(
    trusted_base: Path,
    family_name: str,
    run_name: str,
    dependencies: _Dependencies,
) -> tuple[Path, Path, _DirectoryIdentity, _DirectoryIdentity, _DirectoryIdentity]:
    if not trusted_base.is_absolute():
        raise RetainedReleaseAuditError("trusted base must be absolute")
    base_identity = _directory_identity(trusted_base, dependencies)
    parent = trusted_base / family_name
    root = parent / run_name
    _require_absent(parent, dependencies)
    dependencies.mkdir(parent, 0o700)
    parent_identity = _directory_identity(parent, dependencies, expected_mode=0o700)
    _assert_directory_identity(trusted_base, base_identity, dependencies)
    _require_absent(root, dependencies)
    dependencies.mkdir(root, 0o700)
    root_identity = _directory_identity(root, dependencies, expected_mode=0o700)
    _assert_directory_identity(trusted_base, base_identity, dependencies)
    _assert_directory_identity(parent, parent_identity, dependencies)
    return root, parent, base_identity, parent_identity, root_identity


def _assert_owner_directories(
    *,
    base: Path,
    parent: Path,
    root: Path,
    identities: tuple[_DirectoryIdentity, _DirectoryIdentity, _DirectoryIdentity],
    dependencies: _Dependencies,
) -> None:
    for path, identity in zip((base, parent, root), identities, strict=True):
        _assert_directory_identity(path, identity, dependencies)


def _file_identity(
    path: Path,
    dependencies: _Dependencies,
    *,
    expected_mode: int | None = None,
    expected_bytes: bytes | None = None,
) -> tuple[_FileIdentity, bytes]:
    observed = dependencies.lstat(path)
    if not dependencies.is_regular(observed.st_mode) or stat.S_ISLNK(observed.st_mode):
        raise RetainedReleaseAuditError(f"file owner is not a no-follow regular file: {path}")
    mode = stat.S_IMODE(observed.st_mode)
    if expected_mode is not None and mode != expected_mode:
        raise RetainedReleaseAuditError(f"file mode differs for {path}: {mode:o}")
    data = path.read_bytes()
    if expected_bytes is not None and data != expected_bytes:
        raise RetainedReleaseAuditError(f"persisted bytes differ: {path}")
    identity = _FileIdentity(
        observed.st_dev,
        observed.st_ino,
        mode,
        len(data),
        dependencies.sha256(data).hexdigest(),
    )
    return identity, data


def _snapshot_sources(
    source_dir: Path,
    dependencies: _Dependencies,
) -> tuple[dict[str, _FileIdentity], dict[str, dict[str, Any]], dict[str, bytes]]:
    if not source_dir.is_absolute():
        raise RetainedReleaseAuditError("source directory must be absolute")
    _directory_identity(source_dir, dependencies)
    identities: dict[str, _FileIdentity] = {}
    manifest: dict[str, dict[str, Any]] = {}
    payload_bytes: dict[str, bytes] = {}
    for name in SOURCE_NAMES:
        path = source_dir / name
        identity, data = _file_identity(path, dependencies)
        identities[name] = identity
        manifest[name] = identity.jsonable(path=name)
        payload_bytes[name] = data
    return identities, manifest, payload_bytes


def _assert_sources_unchanged(
    source_dir: Path,
    before: Mapping[str, _FileIdentity],
    dependencies: _Dependencies,
) -> dict[str, dict[str, Any]]:
    after: dict[str, dict[str, Any]] = {}
    for name in SOURCE_NAMES:
        current, _ = _file_identity(source_dir / name, dependencies)
        after[name] = current.jsonable(path=name)
        if current != before[name]:
            raise RetainedReleaseAuditError(f"source identity drifted: {name}")
    return after


def _validate_repo_path(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("changed path must be a non-empty string")
    if value.startswith("/") or "\\" in value:
        raise ValueError("changed path must be repository-relative POSIX")
    components = value.split("/")
    if any(component in {"", ".", ".."} for component in components):
        raise ValueError("changed path contains empty/traversal component")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or str(parsed) != value:
        raise ValueError("changed path is not normalized repository-relative POSIX")
    return value


def _validate_reference(
    value: Any,
    *,
    expected_path: str,
    expected_sha256: str,
) -> None:
    if (
        not isinstance(value, dict)
        or set(value) != {"path", "sha256"}
        or value.get("path") != expected_path
        or value.get("sha256") != expected_sha256
    ):
        raise ValueError(f"artifact reference differs for {expected_path}")


def _validate_absolute_reference_shape(
    value: Any,
    *,
    expected_name: str,
    expected_sha256: str | None = None,
) -> None:
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise ValueError(f"artifact reference shape differs for {expected_name}")
    path = value.get("path")
    digest = value.get("sha256")
    if (
        not isinstance(path, str)
        or not Path(path).is_absolute()
        or Path(path).name != expected_name
        or not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        or (expected_sha256 is not None and digest != expected_sha256)
    ):
        raise ValueError(f"artifact reference differs for {expected_name}")


def _audit_schema(
    payloads: Mapping[str, dict[str, Any]],
    payload_bytes: Mapping[str, bytes],
) -> dict[str, Any]:
    candidate = payloads[SOURCE_NAMES[0]]
    resolved = payloads[SOURCE_NAMES[1]]
    release = payloads[SOURCE_NAMES[2]]
    synthetic_candidate_keys = {
        "schema",
        "status",
        "code_checkpoint",
        "changed_paths",
        "prohibited_paths",
        "resolved_formal_plan",
        "setup_lineage_release",
    }
    synthetic_resolved_keys = {"schema", "status", "code_checkpoint"}
    synthetic_release_keys = {
        "schema",
        "status",
        "code_checkpoint",
        "resolved_formal_plan",
    }
    production_candidate_keys = {
        "schema",
        "status",
        "old_checkpoint",
        "new_checkpoint",
        "release_reference",
        "canonical_setup_reference",
        "resolved_formal_plan_reference",
        "changed_paths",
        "prohibited_paths",
        "canonical_setup_replay",
        "production_release_usable",
        "planner_acceptance_required",
    }
    production_resolved_keys = {
        "analysis_contract",
        "budgets",
        "camera",
        "capture_ledger_contract",
        "captures",
        "cleanup",
        "cold_proxy",
        "continuous_command_between_timed_points",
        "created_at",
        "execute_lock",
        "execution_authorization",
        "experiment_id",
        "exposure_setup_artifact",
        "exposure_setup_required",
        "formal_capture_eligible",
        "frozen_shutters",
        "hard_locks",
        "inputs",
        "native_raw_ambient_policy",
        "offline_contract",
        "operational_dwell",
        "schema",
        "setup_lineage_release_required",
        "setup_physical_cr3_count",
        "shutter_ledger_provenance",
        "source",
        "source_isolation_contract",
        "stage",
        "status",
        "timing_contract",
        "timing_resolution",
        "variant",
    }
    production_release_keys = {
        "schema",
        "status",
        "production_release_usable",
        "old_checkpoint",
        "code_checkpoint",
        "legacy_release",
        "planner_lineage_candidate",
        "current_lineage_candidate",
        "canonical_setup",
        "resolved_formal_plan",
    }
    synthetic_variant = (
        set(candidate) == synthetic_candidate_keys
        and candidate.get("schema") == _CANDIDATE_SCHEMA
        and candidate.get("status") == "eligible"
        and set(resolved) == synthetic_resolved_keys
        and resolved.get("schema") == _RESOLVED_SCHEMA
        and resolved.get("status") == "formal_plan_resolved"
        and set(release) == synthetic_release_keys
        and release.get("schema") == _RELEASE_SCHEMA
        and release.get("status") == "formal_plan_resolved"
    )
    production_variant = (
        set(candidate) == production_candidate_keys
        and candidate.get("schema")
        == "p7_td_b_setup_release_lineage_candidate_v1"
        and candidate.get("status") == "eligible_waiting_for_planner"
        and candidate.get("canonical_setup_replay") == "pass"
        and candidate.get("production_release_usable") is False
        and candidate.get("planner_acceptance_required") is True
        and set(resolved) == production_resolved_keys
        and resolved.get("schema") == "p7_thermal_diagnostic_plan_v2"
        and resolved.get("status") == "execute_authorized"
        and set(release) == production_release_keys
        and release.get("schema") == "p7_td_b_setup_lineage_release_v2"
        and release.get("status") == "formal_plan_lineage_qualified"
        and release.get("production_release_usable") is True
    )
    if not synthetic_variant and not production_variant:
        raise ValueError("artifact schema or status differs")
    checkpoint = (
        candidate.get("code_checkpoint")
        if synthetic_variant
        else candidate.get("new_checkpoint")
    )
    if (
        not isinstance(checkpoint, str)
        or len(checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in checkpoint)
        or (
            synthetic_variant
            and (
                resolved.get("code_checkpoint") != checkpoint
                or release.get("code_checkpoint") != checkpoint
            )
        )
        or (
            production_variant
            and (
                release.get("code_checkpoint") != checkpoint
                or candidate.get("old_checkpoint") != release.get("old_checkpoint")
                or not isinstance(candidate.get("old_checkpoint"), str)
                or len(candidate["old_checkpoint"]) != 40
                or any(
                    character not in "0123456789abcdef"
                    for character in candidate["old_checkpoint"]
                )
                or candidate["old_checkpoint"] == checkpoint
            )
        )
    ):
        raise ValueError("artifact checkpoint links differ")
    rows = candidate.get("changed_paths")
    if not isinstance(rows, list) or len(rows) != 59:
        raise ValueError("changed_paths must contain exactly 59 rows")
    paths: list[str] = []
    for row in rows:
        if (
            not isinstance(row, dict)
            or set(row) != {"path", "classification"}
            or not isinstance(row.get("classification"), str)
            or not row["classification"]
        ):
            raise ValueError("changed_paths row schema differs")
        paths.append(_validate_repo_path(row.get("path")))
    if paths != sorted(paths):
        raise ValueError("changed_paths must be ordered by exact path string")
    if len(paths) != len(set(paths)):
        raise ValueError("changed_paths must contain unique paths")
    if candidate.get("prohibited_paths") != []:
        raise ValueError("prohibited_paths must be empty")
    candidate_sha = hashlib.sha256(payload_bytes[SOURCE_NAMES[0]]).hexdigest()
    resolved_sha = hashlib.sha256(payload_bytes[SOURCE_NAMES[1]]).hexdigest()
    if synthetic_variant:
        release_sha = hashlib.sha256(payload_bytes[SOURCE_NAMES[2]]).hexdigest()
        _validate_reference(
            candidate.get("resolved_formal_plan"),
            expected_path=SOURCE_NAMES[1],
            expected_sha256=resolved_sha,
        )
        _validate_reference(
            candidate.get("setup_lineage_release"),
            expected_path=SOURCE_NAMES[2],
            expected_sha256=release_sha,
        )
        _validate_reference(
            release.get("resolved_formal_plan"),
            expected_path=SOURCE_NAMES[1],
            expected_sha256=resolved_sha,
        )
    else:
        for field, expected_name in (
            ("release_reference", "setup-release.json"),
            ("canonical_setup_reference", "setup.json"),
            ("resolved_formal_plan_reference", SOURCE_NAMES[1]),
        ):
            _validate_absolute_reference_shape(
                candidate.get(field),
                expected_name=expected_name,
            )
        for field, expected_name in (
            ("legacy_release", "setup-release.json"),
            ("planner_lineage_candidate", "setup-release-lineage-candidate.json"),
            ("canonical_setup", "setup.json"),
        ):
            _validate_absolute_reference_shape(
                release.get(field),
                expected_name=expected_name,
            )
        _validate_absolute_reference_shape(
            release.get("current_lineage_candidate"),
            expected_name=SOURCE_NAMES[0],
            expected_sha256=candidate_sha,
        )
        _validate_absolute_reference_shape(
            release.get("resolved_formal_plan"),
            expected_name=SOURCE_NAMES[1],
            expected_sha256=resolved_sha,
        )
    return {
        "status": "pass",
        "artifact_count": 3,
        "changed_path_row_count": 59,
        "changed_path_rows_are_mappings": True,
        "prohibited_paths": [],
        "checkpoint": checkpoint,
        "reference_mismatches": [],
    }


def _callback_result(
    *,
    name: str,
    callback: Callable[..., Any],
    payloads: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    result = callback(
        copy.deepcopy(payloads[SOURCE_NAMES[0]]),
        copy.deepcopy(payloads[SOURCE_NAMES[1]]),
        copy.deepcopy(payloads[SOURCE_NAMES[2]]),
    )
    if not isinstance(result, Mapping) or result.get("status") != "pass":
        raise RetainedReleaseAuditError(f"{name} returned a non-pass result")
    normalized = copy.deepcopy(dict(result))
    return {
        "name": name,
        "call_count": 1,
        "status": "pass",
        "result": normalized,
        "result_sha256": hashlib.sha256(
            json.dumps(
                normalized,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest(),
    }


def _exclusive_write(
    path: Path,
    value: Any,
    dependencies: _Dependencies,
) -> _FileIdentity:
    data = _canonical_json_bytes(value, dependencies)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd: int | None = None
    primary: BaseException | None = None
    try:
        fd = dependencies.open_fd(path, flags, 0o600)
        offset = 0
        while offset < len(data):
            written = dependencies.write_fd(fd, memoryview(data)[offset:])
            if not isinstance(written, int) or written <= 0 or written > len(data) - offset:
                raise OSError("canonical writer made invalid/zero progress")
            offset += written
        dependencies.fsync_fd(fd)
    except BaseException as exc:
        primary = exc
        raise
    finally:
        if fd is not None:
            try:
                dependencies.close_fd(fd)
            except BaseException:
                if primary is None:
                    raise
    identity, _ = _file_identity(
        path,
        dependencies,
        expected_mode=0o600,
        expected_bytes=data,
    )
    return identity


def _artifact_reference(path: Path, dependencies: _Dependencies) -> dict[str, Any]:
    identity, _ = _file_identity(path, dependencies, expected_mode=0o600)
    return {"path": path.name, "bytes": identity.bytes, "sha256": identity.sha256}


def _persist(
    *,
    root: Path,
    name: str,
    value: Any,
    owner_context: Mapping[str, Any],
    dependencies: _Dependencies,
) -> dict[str, Any]:
    dependencies.phase_hook(f"before_write:{name}", owner_context)
    _assert_owner_directories(**owner_context, dependencies=dependencies)
    identity = _exclusive_write(root / name, value, dependencies)
    _assert_owner_directories(**owner_context, dependencies=dependencies)
    return {"path": name, "bytes": identity.bytes, "sha256": identity.sha256}


def _collect_existing_references(
    root: Path,
    dependencies: _Dependencies,
) -> tuple[list[dict[str, Any]], list[str]]:
    references: list[dict[str, Any]] = []
    invalid: list[str] = []
    for name in PROGRESSIVE_NAMES:
        path = root / name
        try:
            dependencies.lstat(path)
        except FileNotFoundError:
            continue
        try:
            references.append(_artifact_reference(path, dependencies))
        except BaseException as exc:
            invalid.append(f"{name}:{type(exc).__name__}")
    return references, invalid


def _load_canonical_artifact(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise ValueError(f"artifact is not single-LF canonical: {path.name}")
    value = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=_strict_object,
        parse_constant=_reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"artifact root is not object: {path.name}")
    if (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
        != data
    ):
        raise ValueError(f"artifact bytes are not canonical: {path.name}")
    return value


def _replay_terminal_bundle(root: Path) -> dict[str, Any]:
    """Read-only independent replay used by tests and package evidence."""
    mismatches: list[str] = []
    try:
        terminal = _load_canonical_artifact(root / TERMINAL_NAME)
    except BaseException as exc:
        return {"status": "fail", "mismatches": [f"terminal:{type(exc).__name__}"]}
    refs = terminal.get("artifact_references")
    if not isinstance(refs, list):
        return {"status": "fail", "mismatches": ["terminal_references_not_list"]}
    if terminal.get("artifact_reference_count") != len(refs):
        mismatches.append("artifact_reference_count")
    observed_names: list[str] = []
    for reference in refs:
        if not isinstance(reference, dict) or set(reference) != {"path", "bytes", "sha256"}:
            mismatches.append("reference_schema")
            continue
        name = reference["path"]
        observed_names.append(name)
        if name == TERMINAL_NAME:
            mismatches.append("terminal_self_reference")
            continue
        if name not in PROGRESSIVE_NAMES:
            mismatches.append(f"unexpected_reference:{name}")
            continue
        path = root / name
        try:
            data = path.read_bytes()
            _load_canonical_artifact(path)
        except BaseException as exc:
            mismatches.append(f"artifact:{name}:{type(exc).__name__}")
            continue
        if len(data) != reference["bytes"]:
            mismatches.append(f"bytes:{name}")
        if hashlib.sha256(data).hexdigest() != reference["sha256"]:
            mismatches.append(f"sha256:{name}")
    if observed_names != [name for name in PROGRESSIVE_NAMES if name in observed_names]:
        mismatches.append("reference_order")
    if len(observed_names) != len(set(observed_names)):
        mismatches.append("duplicate_reference")
    if terminal.get("status") == "pass":
        if observed_names != list(PROGRESSIVE_NAMES):
            mismatches.append("missing_progressive_artifact")
        if terminal.get("mismatch_arrays") != {
            "artifact": [],
            "callback": [],
            "identity": [],
            "schema": [],
            "side_effect": [],
        }:
            mismatches.append("terminal_mismatch_arrays")
        if terminal.get("semantic_callback_counts") != {
            "consumer": 1,
            "validator": 1,
        }:
            mismatches.append("callback_counts")
    return {"status": "pass" if not mismatches else "fail", "mismatches": mismatches}


def run_retained_release_audit(
    *,
    trusted_base: str | Path,
    family_name: str,
    run_name: str,
    source_dir: str | Path,
    semantic_validator: Callable[..., Mapping[str, Any]],
    semantic_consumer: Callable[..., Mapping[str, Any]],
    execution_accounting: Mapping[str, Any] | None = None,
    dependency_overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit one synthetic/retained release and seal one immutable evidence root.

    Dependency and callback callability are validated before any filesystem
    mutation.  Once the child root exists, every non-success path attempts a
    truthful terminal failure seal and never repairs or retries.
    """

    dependencies, dependency_audit = _build_dependencies(dependency_overrides)
    if not callable(semantic_validator) or not callable(semantic_consumer):
        raise RetainedReleaseAuditError(
            "semantic validator and consumer callbacks must be callable"
        )
    family = _direct_child_name(family_name, label="family_name")
    run = _direct_child_name(run_name, label="run_name")
    base = dependencies.path(trusted_base)
    sources = dependencies.path(source_dir)
    root: Path | None = None
    owner_context: dict[str, Any] | None = None
    primary: BaseException | None = None
    seal_failure: BaseException | None = None
    written: list[dict[str, Any]] = []
    callback_counts = {"validator": 0, "consumer": 0}
    try:
        root, parent, base_identity, parent_identity, root_identity = _acquire_directories(
            base, family, run, dependencies
        )
        identities = (base_identity, parent_identity, root_identity)
        owner_context = {
            "base": base,
            "parent": parent,
            "root": root,
            "identities": identities,
        }
        dependencies.phase_hook("after_root_acquisition", owner_context)
        owner_identity = {
            "schema": "p7_retained_release_owner_identity_v1",
            "status": "pass",
            "base": {"path": str(base), **base_identity.jsonable()},
            "parent": {"path": str(parent), **parent_identity.jsonable()},
            "root": {"path": str(root), **root_identity.jsonable()},
            "acquisition_counts": {"parent": 1, "root": 1},
        }
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[0],
                value=owner_identity,
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[1],
                value={
                    "schema": "p7_retained_release_dependency_audit_v1",
                    **dependency_audit,
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        before_identities, before_manifest, payload_bytes = _snapshot_sources(
            sources, dependencies
        )
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[2],
                value={
                    "schema": "p7_retained_release_source_manifest_v1",
                    "status": "pass",
                    "source_count": 3,
                    "sources": before_manifest,
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        payloads = {
            name: _strict_json_load(payload_bytes[name], dependencies)
            for name in SOURCE_NAMES
        }
        schema_audit = _audit_schema(payloads, payload_bytes)
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[3],
                value={
                    "schema": "p7_retained_release_schema_audit_v1",
                    **schema_audit,
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        dependencies.phase_hook("before_semantic_validator", owner_context)
        validator_result = _callback_result(
            name="validator", callback=semantic_validator, payloads=payloads
        )
        callback_counts["validator"] = 1
        dependencies.phase_hook("before_semantic_consumer", owner_context)
        consumer_result = _callback_result(
            name="consumer", callback=semantic_consumer, payloads=payloads
        )
        callback_counts["consumer"] = 1
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[4],
                value={
                    "schema": "p7_retained_release_semantic_callbacks_v1",
                    "status": "pass",
                    "callback_counts": callback_counts,
                    "results": [validator_result, consumer_result],
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        dependencies.phase_hook("before_source_after_snapshot", owner_context)
        after_manifest = _assert_sources_unchanged(
            sources, before_identities, dependencies
        )
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[5],
                value={
                    "schema": "p7_retained_release_source_manifest_v1",
                    "status": "pass",
                    "source_count": 3,
                    "sources": after_manifest,
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        identity_mismatches = [
            name for name in SOURCE_NAMES if before_manifest[name] != after_manifest[name]
        ]
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[6],
                value={
                    "schema": "p7_retained_release_immutability_v1",
                    "status": "pass" if not identity_mismatches else "fail",
                    "identity_mismatches": identity_mismatches,
                },
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        if identity_mismatches:
            raise RetainedReleaseAuditError("source identity mismatch")
        preterminal_references = [
            _artifact_reference(root / name, dependencies)
            for name in PROGRESSIVE_NAMES[:7]
        ]
        preterminal = {
            "schema": "p7_retained_release_preterminal_audit_v1",
            "status": "pass",
            "artifact_references": preterminal_references,
            "expected_progressive_count_before_self": 7,
            "mismatch_arrays": {
                "artifact": [],
                "callback": [],
                "identity": [],
                "schema": [],
                "side_effect": [],
            },
        }
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[7],
                value=preterminal,
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        validation = {
            "schema": "p7_retained_release_validation_summary_v1",
            "status": "pass",
            "artifact_count_before_terminal": 9,
            "source_count": 3,
            "changed_path_row_count": 59,
            "semantic_callback_counts": callback_counts,
            "execution_accounting": copy.deepcopy(dict(execution_accounting or {})),
            "mismatch_arrays": copy.deepcopy(preterminal["mismatch_arrays"]),
            "prohibited_side_effect_counts": {
                "device": 0,
                "network": 0,
                "production_qualification": 0,
                "release_consumption": 0,
            },
        }
        written.append(
            _persist(
                root=root,
                name=PROGRESSIVE_NAMES[8],
                value=validation,
                owner_context=owner_context,
                dependencies=dependencies,
            )
        )
        _assert_sources_unchanged(sources, before_identities, dependencies)
        _assert_owner_directories(**owner_context, dependencies=dependencies)
        terminal_references = [
            _artifact_reference(root / name, dependencies) for name in PROGRESSIVE_NAMES
        ]
        terminal = {
            "schema": "p7_retained_release_terminal_summary_v1",
            "status": "pass",
            "primary_failure": None,
            "seal_failure": None,
            "artifact_references": terminal_references,
            "artifact_reference_count": len(terminal_references),
            "semantic_callback_counts": callback_counts,
            "mismatch_arrays": copy.deepcopy(preterminal["mismatch_arrays"]),
        }
        _persist(
            root=root,
            name=TERMINAL_NAME,
            value=terminal,
            owner_context=owner_context,
            dependencies=dependencies,
        )
        replay = _replay_terminal_bundle(root)
        if replay != {"status": "pass", "mismatches": []}:
            raise RetainedReleaseAuditError(f"terminal replay failed: {replay}")
        return {
            "status": "pass",
            "root": str(root),
            "terminal": terminal,
            "replay": replay,
            "callback_counts": callback_counts,
        }
    except BaseException as exc:
        primary = exc
        if root is not None and owner_context is not None:
            try:
                dependencies.phase_hook("before_failure_seal", owner_context)
                _assert_owner_directories(**owner_context, dependencies=dependencies)
                existing, invalid = _collect_existing_references(root, dependencies)
                validation_path = root / PROGRESSIVE_NAMES[8]
                try:
                    dependencies.lstat(validation_path)
                except FileNotFoundError:
                    _persist(
                        root=root,
                        name=PROGRESSIVE_NAMES[8],
                        value={
                            "schema": "p7_retained_release_validation_summary_v1",
                            "status": "fail",
                            "primary_failure": {
                                "type": type(primary).__name__,
                                "message": str(primary),
                            },
                            "semantic_callback_counts": callback_counts,
                            "execution_accounting": copy.deepcopy(
                                dict(execution_accounting or {})
                            ),
                            "mismatch_arrays": {
                                "artifact": invalid,
                                "callback": [],
                                "identity": [],
                                "schema": [],
                                "side_effect": [],
                            },
                        },
                        owner_context=owner_context,
                        dependencies=dependencies,
                    )
                existing, invalid = _collect_existing_references(root, dependencies)
                _persist(
                    root=root,
                    name=TERMINAL_NAME,
                    value={
                        "schema": "p7_retained_release_terminal_summary_v1",
                        "status": "fail",
                        "primary_failure": {
                            "type": type(primary).__name__,
                            "message": str(primary),
                        },
                        "seal_failure": None,
                        "artifact_references": existing,
                        "artifact_reference_count": len(existing),
                        "semantic_callback_counts": callback_counts,
                        "mismatch_arrays": {
                            "artifact": invalid,
                            "callback": [],
                            "identity": [],
                            "schema": [],
                            "side_effect": [],
                        },
                    },
                    owner_context=owner_context,
                    dependencies=dependencies,
                )
            except BaseException as terminal_exc:
                seal_failure = terminal_exc
        if isinstance(primary, (KeyboardInterrupt, SystemExit)):
            setattr(primary, "retained_release_root", root)
            setattr(primary, "retained_release_seal_failure", seal_failure)
            raise
        raise RetainedReleaseAuditError(
            f"retained release audit failed: {primary}",
            root=root,
            primary=primary,
            seal_failure=seal_failure,
        ) from primary


__all__ = ["RetainedReleaseAuditError", "run_retained_release_audit"]
