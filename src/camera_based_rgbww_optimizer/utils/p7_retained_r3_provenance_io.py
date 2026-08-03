"""Fail-closed local provenance file and read-only Git I/O primitives.

The module deliberately owns only physical I/O facts.  It does not interpret
retained artifacts, decide eligibility, or own a terminal lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
import errno
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
from types import MappingProxyType
from typing import Any, Callable, Mapping

__all__ = [
    "DirectoryIdentity",
    "FileIdentity",
    "GitLedger",
    "ProvenanceDependencies",
    "ProvenanceIOError",
    "RepositoryIdentity",
    "SourceIdentity",
    "canonical_json_bytes",
    "create_exclusive_direct_child",
    "create_exclusive_root",
    "decode_canonical_json",
    "decode_strict_json_bytes",
    "json_native_value",
    "list_exact_regular_children",
    "persist_canonical_json",
    "read_exact_file",
    "read_existing_root",
    "read_git_source_identity",
    "require_same_target",
    "run_read_only_git",
]


_SHA40 = re.compile(r"[0-9a-f]{40}")


class ProvenanceIOError(RuntimeError):
    """Boundary failure with a stable machine-readable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class DirectoryIdentity:
    path: str
    device: int
    inode: int
    mode: int


@dataclass(frozen=True)
class FileIdentity:
    path: str
    data: bytes
    byte_count: int
    sha256: str
    device: int
    inode: int
    mode: int
    root: DirectoryIdentity | None = None


@dataclass(frozen=True)
class GitLedger:
    argv: tuple[str, ...]
    cwd: str
    exit_code: int
    stdout: bytes
    stderr: bytes
    stdout_sha256: str
    stderr_sha256: str


@dataclass(frozen=True)
class RepositoryIdentity:
    path: str
    device: int
    inode: int
    mode: int


@dataclass(frozen=True)
class SourceIdentity:
    repository: RepositoryIdentity
    head: str
    checkpoint: str
    tree: str
    staged: bool
    unstaged: bool
    untracked: bool
    clean: bool


@dataclass(frozen=True)
class ProvenanceDependencies:
    lstat: Callable[[Any], os.stat_result] = os.lstat
    mkdir: Callable[[Any, int], None] = os.mkdir
    open_fd: Callable[[Any, int, int], int] = os.open
    fstat: Callable[[int], os.stat_result] = os.fstat
    read_fd: Callable[[int, int], bytes] = os.read
    write_fd: Callable[[int, bytes | memoryview], int] = os.write
    fsync_fd: Callable[[int], None] = os.fsync
    close_fd: Callable[[int], None] = os.close
    scandir: Callable[[Any], Any] = os.scandir
    run_process: Callable[..., Any] = subprocess.run


def _dependencies(
    overrides: Mapping[str, Callable[..., Any]] | None,
) -> ProvenanceDependencies:
    values = {field.name: getattr(ProvenanceDependencies(), field.name) for field in fields(ProvenanceDependencies)}
    try:
        supplied = dict(overrides or {})
    except (TypeError, ValueError) as exc:
        raise ProvenanceIOError("invalid_dependencies") from exc
    if set(supplied) - set(values):
        raise ProvenanceIOError("unknown_dependency")
    if any(not callable(value) for value in supplied.values()):
        raise ProvenanceIOError("noncallable_dependency")
    values.update(supplied)
    return ProvenanceDependencies(**values)


def _path(value: os.PathLike[str] | str) -> Path:
    if not isinstance(value, (str, os.PathLike)):
        raise ProvenanceIOError("invalid_path")
    try:
        path = Path(value)
    except (TypeError, ValueError, OSError) as exc:
        raise ProvenanceIOError("invalid_path") from exc
    if "\x00" in os.fspath(path):
        raise ProvenanceIOError("invalid_path")
    return path


def _required_open_flag(name: str) -> int:
    value = getattr(os, name, None)
    if type(value) is not int or value == 0:
        raise ProvenanceIOError(f"required_open_flag_unavailable:{name}")
    return value


def _require_direct_child(
    value: os.PathLike[str] | str, root: DirectoryIdentity
) -> Path:
    """Prove one lexical, absolute, exact direct-child relationship."""

    try:
        text = os.fspath(value)
    except (TypeError, ValueError, OSError) as exc:
        raise ProvenanceIOError("invalid_path") from exc
    if type(text) is not str or not text.startswith("/"):
        raise ProvenanceIOError("target_not_absolute")
    if "\\" in text:
        raise ProvenanceIOError("target_not_direct_child")
    parts = text.split("/")
    if len(parts) < 2 or parts[0] != "" or any(
        part in {"", ".", ".."} for part in parts[1:]
    ):
        raise ProvenanceIOError("target_not_direct_child")
    parent, _separator, child = text.rpartition("/")
    if not parent:
        parent = "/"
    if parent != root.path or not child:
        raise ProvenanceIOError("target_not_direct_child")
    target = _path(value)
    if str(target) != text:
        raise ProvenanceIOError("target_not_direct_child")
    return target


def _directory_from_stat(path: Path, value: os.stat_result) -> DirectoryIdentity:
    if stat.S_ISLNK(value.st_mode) or not stat.S_ISDIR(value.st_mode):
        raise ProvenanceIOError("root_not_directory")
    mode = stat.S_IMODE(value.st_mode)
    if mode != 0o700:
        raise ProvenanceIOError("root_mode_mismatch")
    return DirectoryIdentity(str(path), value.st_dev, value.st_ino, mode)


def _directory_identity(
    path: Path, dependencies: ProvenanceDependencies
) -> DirectoryIdentity:
    try:
        return _directory_from_stat(path, dependencies.lstat(path))
    except ProvenanceIOError:
        raise
    except OSError as exc:
        raise ProvenanceIOError("root_lstat_failed") from exc


def _require_root(
    root: DirectoryIdentity, dependencies: ProvenanceDependencies
) -> Path:
    if type(root) is not DirectoryIdentity:
        raise ProvenanceIOError("invalid_root_identity")
    path = _path(root.path)
    if _directory_identity(path, dependencies) != root:
        raise ProvenanceIOError("root_identity_drift")
    return path


def create_exclusive_root(
    path: os.PathLike[str] | str,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> DirectoryIdentity:
    """Create one exact 0700 directory; parents are never created or repaired."""

    deps = _dependencies(dependencies)
    target = _path(path)
    if not target.is_absolute():
        raise ProvenanceIOError("root_not_absolute")
    try:
        deps.mkdir(target, 0o700)
    except FileExistsError as exc:
        raise ProvenanceIOError("root_exists") from exc
    except OSError as exc:
        raise ProvenanceIOError("root_mkdir_failed") from exc
    return _directory_identity(target, deps)


def create_exclusive_direct_child(
    parent: DirectoryIdentity,
    child_name: str,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> DirectoryIdentity:
    """Create one exact child while binding the canonical parent identity."""

    deps = _dependencies(dependencies)
    parent_path = _require_root(parent, deps)
    child = parent_path / _direct_child(child_name)
    try:
        deps.mkdir(child, 0o700)
    except FileExistsError as exc:
        raise ProvenanceIOError("root_exists") from exc
    except OSError as exc:
        raise ProvenanceIOError("root_mkdir_failed") from exc
    if _directory_identity(parent_path, deps) != parent:
        raise ProvenanceIOError("parent_identity_drift")
    return _directory_identity(child, deps)


def read_existing_root(
    path: os.PathLike[str] | str,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> DirectoryIdentity:
    """Acquire one no-follow identity for an existing canonical 0700 root."""

    deps = _dependencies(dependencies)
    target = _path(path)
    try:
        text = os.fspath(path)
    except (TypeError, ValueError, OSError) as exc:
        raise ProvenanceIOError("invalid_path") from exc
    if type(text) is not str:
        raise ProvenanceIOError("invalid_path")
    if not text.startswith("/"):
        raise ProvenanceIOError("root_not_absolute")
    parts = text.split("/")
    if (
        "\\" in text
        or (text != "/" and any(part in {"", ".", ".."} for part in parts[1:]))
        or str(target) != text
    ):
        raise ProvenanceIOError("root_not_canonical")
    return _directory_identity(target, deps)


def _file_stat_identity(
    path: Path, value: os.stat_result, *, expected_mode: int | None
) -> tuple[int, int, int, int]:
    if stat.S_ISLNK(value.st_mode) or not stat.S_ISREG(value.st_mode):
        raise ProvenanceIOError("file_not_regular")
    mode = stat.S_IMODE(value.st_mode)
    if expected_mode is not None and mode != expected_mode:
        raise ProvenanceIOError("file_mode_mismatch")
    return value.st_dev, value.st_ino, mode, value.st_size


def _close(deps: ProvenanceDependencies, fd: int, primary: BaseException | None) -> None:
    try:
        deps.close_fd(fd)
    except OSError as exc:
        if primary is None:
            raise ProvenanceIOError("close_failed") from exc
        raise ProvenanceIOError("close_failed") from primary


def _read(deps: ProvenanceDependencies, fd: int, count: int) -> bytes:
    while True:
        try:
            value = deps.read_fd(fd, count)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            raise ProvenanceIOError("read_failed") from exc
        if type(value) is not bytes:
            raise ProvenanceIOError("invalid_read_result")
        return value


def read_exact_file(
    path: os.PathLike[str] | str,
    *,
    expected_mode: int | None = None,
    expected_size: int | None = None,
    expected_sha256: str | None = None,
    root: DirectoryIdentity | None = None,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> FileIdentity:
    """Read a frozen regular file through a no-follow descriptor."""

    deps = _dependencies(dependencies)
    target = _path(path)
    if root is not None:
        _require_root(root, deps)
        target = _require_direct_child(path, root)
    try:
        before_path = deps.lstat(target)
        path_tuple = _file_stat_identity(target, before_path, expected_mode=expected_mode)
    except ProvenanceIOError:
        raise
    except OSError as exc:
        raise ProvenanceIOError("file_lstat_failed") from exc
    flags = os.O_RDONLY | _required_open_flag("O_NOFOLLOW")
    try:
        fd = deps.open_fd(target, flags, 0)
    except OSError as exc:
        raise ProvenanceIOError("file_open_failed") from exc
    primary: BaseException | None = None
    try:
        before_fd = deps.fstat(fd)
        fd_tuple = _file_stat_identity(target, before_fd, expected_mode=expected_mode)
        if fd_tuple != path_tuple:
            raise ProvenanceIOError("file_identity_drift")
        size = path_tuple[3]
        chunks: list[bytes] = []
        remaining = size
        while remaining:
            chunk = _read(deps, fd, remaining)
            if not chunk:
                raise ProvenanceIOError("file_truncated")
            if len(chunk) > remaining:
                raise ProvenanceIOError("invalid_read_result")
            chunks.append(chunk)
            remaining -= len(chunk)
        extra = _read(deps, fd, 1)
        if extra:
            raise ProvenanceIOError("file_grew")
        after_fd = deps.fstat(fd)
        if _file_stat_identity(target, after_fd, expected_mode=expected_mode) != fd_tuple:
            raise ProvenanceIOError("file_identity_drift")
        data = b"".join(chunks)
        digest = hashlib.sha256(data).hexdigest()
        if expected_size is not None and (type(expected_size) is not int or len(data) != expected_size):
            raise ProvenanceIOError("file_size_mismatch")
        if expected_sha256 is not None and digest != expected_sha256:
            raise ProvenanceIOError("file_hash_mismatch")
        return FileIdentity(
            str(target), data, len(data), digest,
            fd_tuple[0], fd_tuple[1], fd_tuple[2], root,
        )
    except BaseException as exc:
        primary = exc
        raise
    finally:
        _close(deps, fd, primary)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProvenanceIOError("json_duplicate_key")
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    raise ProvenanceIOError("json_nonfinite")


def _freeze_json(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _freeze_json(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_freeze_json(item) for item in value)
    if type(value) is float and not math.isfinite(value):
        raise ProvenanceIOError("json_nonfinite")
    if type(value) in (str, int, float, bool) or value is None:
        return value
    raise ProvenanceIOError("json_unsupported_value")


def _json_native_value(value: Any, active: set[int]) -> Any:
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise ProvenanceIOError("json_unsupported_value")
        active.add(identity)
        try:
            result: dict[str, Any] = {}
            for key, item in value.items():
                if type(key) is not str:
                    raise ProvenanceIOError("json_unsupported_value")
                result[key] = _json_native_value(item, active)
            return result
        finally:
            active.remove(identity)
    if type(value) in (tuple, list):
        identity = id(value)
        if identity in active:
            raise ProvenanceIOError("json_unsupported_value")
        active.add(identity)
        try:
            return [_json_native_value(item, active) for item in value]
        finally:
            active.remove(identity)
    if type(value) is float and not math.isfinite(value):
        raise ProvenanceIOError("json_nonfinite")
    if type(value) in (str, int, float, bool) or value is None:
        return value
    raise ProvenanceIOError("json_unsupported_value")


def json_native_value(value: Any) -> Any:
    """Project immutable Mapping/tuple JSON values into plain dict/list values."""

    return _json_native_value(value, set())


def canonical_json_bytes(value: Any) -> bytes:
    """Encode strict JSON as compact sorted UTF-8 plus exactly one LF."""

    native = json_native_value(value)
    try:
        text = json.dumps(
            native, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError, OverflowError) as exc:
        raise ProvenanceIOError("json_encode_failed") from exc
    return text.encode("utf-8") + b"\n"


def decode_canonical_json(data: bytes) -> Any:
    """Strictly decode and exact-reencode canonical JSON bytes."""

    if type(data) is not bytes or data.startswith(b"\xef\xbb\xbf"):
        raise ProvenanceIOError("json_bytes_invalid")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise ProvenanceIOError("json_terminal_lf_invalid")
    try:
        text = data.decode("utf-8")
        value = json.loads(
            text, object_pairs_hook=_strict_object, parse_constant=_reject_constant,
        )
        frozen = _freeze_json(value)
    except ProvenanceIOError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ProvenanceIOError("json_decode_failed") from exc
    if canonical_json_bytes(value) != data:
        raise ProvenanceIOError("json_not_canonical")
    return frozen


def decode_strict_json_bytes(data: bytes) -> Any:
    """Strictly decode JSON bytes without requiring canonical source layout."""

    if type(data) is not bytes or data.startswith(b"\xef\xbb\xbf"):
        raise ProvenanceIOError("json_bytes_invalid")
    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
        return _freeze_json(value)
    except ProvenanceIOError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ProvenanceIOError("json_decode_failed") from exc


def _direct_child(value: str) -> str:
    if type(value) is not str or not value or "\x00" in value or value in {".", ".."}:
        raise ProvenanceIOError("unsafe_child")
    if PurePosixPath(value).is_absolute() or "/" in value or "\\" in value:
        raise ProvenanceIOError("unsafe_child")
    return value


def persist_canonical_json(
    root: DirectoryIdentity,
    child_name: str,
    value: Any,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> FileIdentity:
    """Exclusively persist, fsync, and reload one canonical JSON target."""

    deps = _dependencies(dependencies)
    root_path = _require_root(root, deps)
    target = root_path / _direct_child(child_name)
    payload = canonical_json_bytes(value)
    nofollow = _required_open_flag("O_NOFOLLOW")
    directory = _required_open_flag("O_DIRECTORY")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow
    root_flags = os.O_RDONLY | directory | nofollow
    try:
        fd = deps.open_fd(target, flags, 0o600)
    except FileExistsError as exc:
        raise ProvenanceIOError("target_exists") from exc
    except OSError as exc:
        raise ProvenanceIOError("target_open_failed") from exc
    primary: BaseException | None = None
    try:
        opened = deps.fstat(fd)
        opened_tuple = _file_stat_identity(target, opened, expected_mode=0o600)
        view = memoryview(payload)
        written = 0
        while written < len(payload):
            try:
                count = deps.write_fd(fd, view[written:])
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    continue
                raise ProvenanceIOError("write_failed") from exc
            if type(count) is not int or count <= 0 or count > len(payload) - written:
                raise ProvenanceIOError("write_no_progress")
            written += count
        try:
            deps.fsync_fd(fd)
        except OSError as exc:
            raise ProvenanceIOError("file_fsync_failed") from exc
        after = deps.fstat(fd)
        after_tuple = _file_stat_identity(target, after, expected_mode=0o600)
        if after_tuple[:3] != opened_tuple[:3] or after_tuple[3] != len(payload):
            raise ProvenanceIOError("target_identity_drift")
    except BaseException as exc:
        primary = exc
        raise
    finally:
        _close(deps, fd, primary)

    try:
        root_fd = deps.open_fd(root_path, root_flags, 0)
    except OSError as exc:
        raise ProvenanceIOError("root_open_failed") from exc
    root_primary: BaseException | None = None
    try:
        observed_root = _directory_from_stat(root_path, deps.fstat(root_fd))
        if observed_root != root or _directory_identity(root_path, deps) != root:
            raise ProvenanceIOError("root_identity_drift")
        try:
            deps.fsync_fd(root_fd)
        except OSError as exc:
            raise ProvenanceIOError("root_fsync_failed") from exc
    except BaseException as exc:
        root_primary = exc
        raise
    finally:
        _close(deps, root_fd, root_primary)

    identity = read_exact_file(
        target, expected_mode=0o600, expected_size=len(payload),
        expected_sha256=hashlib.sha256(payload).hexdigest(), root=root,
        dependencies=dependencies,
    )
    decode_canonical_json(identity.data)
    return identity


def require_same_target(actual: FileIdentity, expected: FileIdentity) -> FileIdentity:
    """Return the physical target only when every frozen field is exact."""

    if type(actual) is not FileIdentity or type(expected) is not FileIdentity:
        raise ProvenanceIOError("invalid_target_identity")
    if actual != expected:
        raise ProvenanceIOError("target_identity_mismatch")
    return actual


def list_exact_regular_children(
    root: DirectoryIdentity,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> tuple[str, ...]:
    """List exact direct regular-file children under one bound root identity."""

    deps = _dependencies(dependencies)
    root_path = _require_root(root, deps)
    names: list[str] = []
    try:
        with deps.scandir(root_path) as entries:
            for entry in entries:
                name = _direct_child(entry.name)
                observed = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(observed.st_mode) or not stat.S_ISREG(observed.st_mode):
                    raise ProvenanceIOError("child_not_regular")
                names.append(name)
    except ProvenanceIOError:
        raise
    except OSError as exc:
        raise ProvenanceIOError("root_inventory_failed") from exc
    if _directory_identity(root_path, deps) != root:
        raise ProvenanceIOError("root_identity_drift")
    return tuple(sorted(names, key=lambda value: value.encode("utf-8")))


def _sha(value: str) -> bool:
    return type(value) is str and _SHA40.fullmatch(value) is not None


def _repo_path(value: str) -> bool:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        return False
    if value.startswith("/") or "//" in value:
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _validate_git_argv(argv: tuple[str, ...]) -> None:
    if type(argv) is not tuple or any(type(item) is not str for item in argv):
        raise ProvenanceIOError("git_argv_invalid")
    valid = False
    if len(argv) == 4 and argv[:3] == ("git", "rev-parse", "--verify"):
        valid = argv[3] == "HEAD^{commit}" or (
            argv[3].endswith("^{commit}") and _sha(argv[3][:-9])
        )
    elif len(argv) == 5 and argv[:4] == ("git", "show", "-s", "--format=%H%x00%P%x00%s"):
        valid = _sha(argv[4])
    elif len(argv) == 5 and argv[:4] == ("git", "show", "-s", "--format=%H%x00%T"):
        valid = _sha(argv[4])
    elif argv == ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"):
        valid = True
    elif len(argv) == 7 and argv[:6] == ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z"):
        valid = _sha(argv[6])
    elif len(argv) == 3 and argv[:2] == ("git", "rev-parse") and ":" in argv[2]:
        sha, path = argv[2].split(":", 1)
        valid = _sha(sha) and _repo_path(path)
    if len(argv) >= 9 and argv[:5] == ("git", "diff", "--binary", "--full-index", "--no-ext-diff"):
        parent, child = argv[5:7]
        paths = argv[8:]
        valid = (
            argv[7] == "--" and _sha(parent) and _sha(child) and bool(paths)
            and all(_repo_path(path) for path in paths)
            and tuple(sorted(paths)) == paths and len(set(paths)) == len(paths)
        )
    if not valid:
        raise ProvenanceIOError("git_command_denied")


def run_read_only_git(
    repo: os.PathLike[str] | str,
    argv: tuple[str, ...],
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> GitLedger:
    """Run one exact allowlisted read-only Git argv and preserve its outcome."""

    deps = _dependencies(dependencies)
    repo_path = _path(repo)
    if not repo_path.is_absolute():
        raise ProvenanceIOError("repo_not_absolute")
    _validate_git_argv(argv)
    try:
        completed = deps.run_process(
            argv, cwd=str(repo_path), shell=False, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProvenanceIOError("git_launch_failed") from exc
    if (
        type(getattr(completed, "returncode", None)) is not int
        or type(getattr(completed, "stdout", None)) is not bytes
        or type(getattr(completed, "stderr", None)) is not bytes
    ):
        raise ProvenanceIOError("git_result_invalid")
    stdout = bytes(completed.stdout)
    stderr = bytes(completed.stderr)
    return GitLedger(
        tuple(argv), str(repo_path), completed.returncode, stdout, stderr,
        hashlib.sha256(stdout).hexdigest(), hashlib.sha256(stderr).hexdigest(),
    )


def _repository_identity(
    path: Path, dependencies: ProvenanceDependencies
) -> RepositoryIdentity:
    try:
        observed = dependencies.lstat(path)
    except OSError as exc:
        raise ProvenanceIOError("repo_lstat_failed") from exc
    if stat.S_ISLNK(observed.st_mode) or not stat.S_ISDIR(observed.st_mode):
        raise ProvenanceIOError("repo_not_directory")
    return RepositoryIdentity(
        str(path), observed.st_dev, observed.st_ino, stat.S_IMODE(observed.st_mode)
    )


def _require_clean_ledger(ledger: GitLedger, code: str) -> bytes:
    if ledger.exit_code != 0 or ledger.stderr:
        raise ProvenanceIOError(code)
    return ledger.stdout


def read_git_source_identity(
    repo: os.PathLike[str] | str,
    checkpoint: str,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> SourceIdentity:
    """Read one clean HEAD/checkpoint/tree identity through allowlisted Git."""

    if not _sha(checkpoint):
        raise ProvenanceIOError("source_checkpoint_invalid")
    deps = _dependencies(dependencies)
    repo_path = _path(repo)
    if not repo_path.is_absolute() or str(repo_path) != os.fspath(repo):
        raise ProvenanceIOError("repo_not_absolute")
    before = _repository_identity(repo_path, deps)
    head_bytes = _require_clean_ledger(
        run_read_only_git(
            repo_path, ("git", "rev-parse", "--verify", "HEAD^{commit}"),
            dependencies=dependencies,
        ),
        "source_head_unverified",
    )
    if not head_bytes.endswith(b"\n") or head_bytes.count(b"\n") != 1:
        raise ProvenanceIOError("source_head_invalid")
    try:
        head = head_bytes[:-1].decode("ascii")
    except UnicodeDecodeError as exc:
        raise ProvenanceIOError("source_head_invalid") from exc
    if not _sha(head) or head != checkpoint:
        raise ProvenanceIOError("source_head_mismatch")
    show = _require_clean_ledger(
        run_read_only_git(
            repo_path,
            ("git", "show", "-s", "--format=%H%x00%T", checkpoint),
            dependencies=dependencies,
        ),
        "source_tree_unverified",
    )
    try:
        commit_bytes, tree_bytes = show.removesuffix(b"\n").split(b"\x00", 1)
        observed_commit = commit_bytes.decode("ascii")
        tree = tree_bytes.decode("ascii")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ProvenanceIOError("source_tree_invalid") from exc
    if observed_commit != checkpoint or not _sha(tree):
        raise ProvenanceIOError("source_tree_invalid")
    status = _require_clean_ledger(
        run_read_only_git(
            repo_path,
            ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"),
            dependencies=dependencies,
        ),
        "source_status_unverified",
    )
    records = tuple(record for record in status.split(b"\x00") if record)
    if any(len(record) < 3 for record in records):
        raise ProvenanceIOError("source_status_invalid")
    untracked = any(record.startswith(b"?? ") for record in records)
    staged = any(record[:1] not in {b" ", b"?"} for record in records)
    unstaged = any(record[1:2] not in {b" ", b"?"} for record in records)
    after = _repository_identity(repo_path, deps)
    if after != before:
        raise ProvenanceIOError("repo_identity_drift")
    return SourceIdentity(
        before, head, checkpoint, tree, staged, unstaged, untracked,
        not (staged or unstaged or untracked),
    )
