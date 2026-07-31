"""Deterministic outer runtime for one retained-R3 controller source.

Preparation, source conformance, and physical readback remain owned by their
dedicated modules.  This adapter only sequences those owners around one
exclusive source write and, after verification, one process launch.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
import errno
import hashlib
import os
from pathlib import Path
import stat
import subprocess
from typing import Any, Callable, Mapping

from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import (
    ControllerConformanceReport,
    analyze_controller_source,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation import (
    PreparedControllerSource,
    prepare_controller_source,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    FileIdentity,
    read_exact_file,
)

__all__ = [
    "ControllerCompositionReport",
    "ControllerProcessReport",
    "ControllerRuntimeDependencies",
    "ControllerRuntimeError",
    "ControllerRuntimeReport",
    "ControllerRuntimeRequest",
    "compose_controller_source",
    "execute_controller_runtime",
]


class ControllerRuntimeError(RuntimeError):
    """Fail-closed outer-runtime error with a stable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ControllerRuntimeRequest:
    template_source: bytes
    assignment_name: str
    validation_function: str
    replacement_statement: bytes
    source_path: str
    process_argv: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.template_source) is not bytes or type(self.replacement_statement) is not bytes:
            raise ControllerRuntimeError("source_not_bytes")
        if (
            type(self.assignment_name) is not str
            or not self.assignment_name.isidentifier()
            or type(self.validation_function) is not str
            or not self.validation_function.isidentifier()
        ):
            raise ControllerRuntimeError("invalid_preparation_request")
        _absolute_source_path(self.source_path)
        if (
            type(self.process_argv) is not tuple
            or not self.process_argv
            or any(type(item) is not str or not item or "\x00" in item for item in self.process_argv)
        ):
            raise ControllerRuntimeError("invalid_process_argv")


@dataclass(frozen=True)
class ControllerCompositionReport:
    source: bytes
    source_sha256: str
    byte_count: int
    function_name: str
    source_path: str
    process_argv: tuple[str, ...]


@dataclass(frozen=True)
class ControllerProcessReport:
    argv: tuple[str, ...]
    exit_code: int
    stdout: bytes
    stderr: bytes
    stdout_sha256: str
    stderr_sha256: str


@dataclass(frozen=True)
class ControllerRuntimeReport:
    composition: ControllerCompositionReport
    conformance: ControllerConformanceReport
    source_identity: FileIdentity
    process: ControllerProcessReport


@dataclass(frozen=True)
class ControllerRuntimeDependencies:
    analyze_source: Callable[[bytes], ControllerConformanceReport] = analyze_controller_source
    open_fd: Callable[[Any, int, int], int] = os.open
    write_fd: Callable[[int, bytes | memoryview], int] = os.write
    fsync_fd: Callable[[int], None] = os.fsync
    close_fd: Callable[[int], None] = os.close
    fstat: Callable[[int], os.stat_result] = os.fstat
    lstat: Callable[[Any], os.stat_result] = os.lstat
    read_source: Callable[..., FileIdentity] = read_exact_file
    run_process: Callable[..., Any] = subprocess.run


def _dependencies(
    overrides: Mapping[str, Callable[..., Any]] | None,
) -> ControllerRuntimeDependencies:
    defaults = ControllerRuntimeDependencies()
    values = {field.name: getattr(defaults, field.name) for field in fields(defaults)}
    try:
        supplied = dict(overrides or {})
    except (TypeError, ValueError) as exc:
        raise ControllerRuntimeError("invalid_dependencies") from exc
    if set(supplied) - set(values):
        raise ControllerRuntimeError("unknown_dependency")
    if any(not callable(value) for value in supplied.values()):
        raise ControllerRuntimeError("noncallable_dependency")
    values.update(supplied)
    return ControllerRuntimeDependencies(**values)


def _absolute_source_path(value: object) -> Path:
    if type(value) is not str or not value or "\x00" in value:
        raise ControllerRuntimeError("invalid_source_path")
    path = Path(value)
    if not path.is_absolute() or str(path) != value or path.name in {"", ".", ".."}:
        raise ControllerRuntimeError("source_path_not_absolute")
    return path


def _required_flag(name: str) -> int:
    value = getattr(os, name, None)
    if type(value) is not int or value == 0:
        raise ControllerRuntimeError(f"required_open_flag_unavailable:{name}")
    return value


def compose_controller_source(request: ControllerRuntimeRequest) -> ControllerCompositionReport:
    """Compose one deterministic byte source without filesystem or process effects."""

    if type(request) is not ControllerRuntimeRequest:
        raise ControllerRuntimeError("invalid_request")
    prepared: PreparedControllerSource = prepare_controller_source(
        request.template_source,
        assignment_name=request.assignment_name,
        validation_function=request.validation_function,
        replacement_statement=request.replacement_statement,
    )
    return ControllerCompositionReport(
        source=prepared.source,
        source_sha256=prepared.source_sha256,
        byte_count=len(prepared.source),
        function_name=prepared.pair.function_name,
        source_path=request.source_path,
        process_argv=request.process_argv,
    )


def _stat_tuple(value: os.stat_result) -> tuple[int, int, int]:
    if stat.S_ISLNK(value.st_mode) or not stat.S_ISREG(value.st_mode):
        raise ControllerRuntimeError("source_not_regular")
    mode = stat.S_IMODE(value.st_mode)
    if mode != 0o600:
        raise ControllerRuntimeError("source_mode_mismatch")
    return value.st_dev, value.st_ino, mode


def _directory_tuple(value: os.stat_result) -> tuple[int, int, int]:
    if stat.S_ISLNK(value.st_mode) or not stat.S_ISDIR(value.st_mode):
        raise ControllerRuntimeError("parent_not_directory")
    return value.st_dev, value.st_ino, stat.S_IMODE(value.st_mode)


def _close(deps: ControllerRuntimeDependencies, fd: int, primary: BaseException | None) -> None:
    try:
        deps.close_fd(fd)
    except OSError as exc:
        failure = ControllerRuntimeError("close_failed")
        if primary is not None:
            raise primary from failure
        raise failure from exc


def _write_all(deps: ControllerRuntimeDependencies, fd: int, data: bytes) -> None:
    remaining = memoryview(data)
    while remaining:
        try:
            written = deps.write_fd(fd, remaining)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            raise ControllerRuntimeError("source_write_failed") from exc
        if type(written) is not int or written <= 0 or written > len(remaining):
            raise ControllerRuntimeError("source_write_no_progress")
        remaining = remaining[written:]


def _persist_source(
    composition: ControllerCompositionReport,
    deps: ControllerRuntimeDependencies,
) -> FileIdentity:
    path = _absolute_source_path(composition.source_path)
    parent = path.parent
    try:
        parent_before = _directory_tuple(deps.lstat(parent))
    except ControllerRuntimeError:
        raise
    except OSError as exc:
        raise ControllerRuntimeError("parent_lstat_failed") from exc

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _required_flag("O_NOFOLLOW")
    try:
        fd = deps.open_fd(path, flags, 0o600)
    except OSError as exc:
        raise ControllerRuntimeError("source_open_failed") from exc
    primary: BaseException | None = None
    written_identity: tuple[int, int, int] | None = None
    try:
        _write_all(deps, fd, composition.source)
        written_identity = _stat_tuple(deps.fstat(fd))
        deps.fsync_fd(fd)
    except BaseException as exc:
        primary = exc
        if isinstance(exc, ControllerRuntimeError):
            raise
        raise ControllerRuntimeError("source_file_fsync_failed") from exc
    finally:
        _close(deps, fd, primary)

    directory_flags = os.O_RDONLY | _required_flag("O_DIRECTORY") | _required_flag("O_NOFOLLOW")
    try:
        parent_fd = deps.open_fd(parent, directory_flags, 0)
    except OSError as exc:
        raise ControllerRuntimeError("parent_open_failed") from exc
    primary = None
    try:
        if _directory_tuple(deps.fstat(parent_fd)) != parent_before:
            raise ControllerRuntimeError("parent_identity_drift")
        deps.fsync_fd(parent_fd)
    except BaseException as exc:
        primary = exc
        if isinstance(exc, ControllerRuntimeError):
            raise
        raise ControllerRuntimeError("parent_fsync_failed") from exc
    finally:
        _close(deps, parent_fd, primary)

    try:
        if _directory_tuple(deps.lstat(parent)) != parent_before:
            raise ControllerRuntimeError("parent_identity_drift")
        identity = deps.read_source(
            path,
            expected_mode=0o600,
            expected_size=composition.byte_count,
            expected_sha256=composition.source_sha256,
        )
    except ControllerRuntimeError:
        raise
    except BaseException as exc:
        raise ControllerRuntimeError("source_readback_failed") from exc
    if type(identity) is not FileIdentity:
        raise ControllerRuntimeError("source_readback_invalid")
    if (
        written_identity is None
        or (identity.device, identity.inode, identity.mode) != written_identity
        or identity.path != str(path)
        or identity.data != composition.source
        or identity.byte_count != composition.byte_count
        or identity.sha256 != composition.source_sha256
    ):
        raise ControllerRuntimeError("source_identity_drift")
    return identity


def _launch(
    request: ControllerRuntimeRequest,
    source_identity: FileIdentity,
    deps: ControllerRuntimeDependencies,
) -> ControllerProcessReport:
    try:
        completed = deps.run_process(
            request.process_argv,
            input=source_identity.data,
            shell=False,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ControllerRuntimeError("controller_launch_failed") from exc
    exit_code = getattr(completed, "returncode", None)
    stdout = getattr(completed, "stdout", None)
    stderr = getattr(completed, "stderr", None)
    if type(exit_code) is not int or type(stdout) is not bytes or type(stderr) is not bytes:
        raise ControllerRuntimeError("controller_result_invalid")
    return ControllerProcessReport(
        argv=request.process_argv,
        exit_code=exit_code,
        stdout=bytes(stdout),
        stderr=bytes(stderr),
        stdout_sha256=hashlib.sha256(stdout).hexdigest(),
        stderr_sha256=hashlib.sha256(stderr).hexdigest(),
    )


def execute_controller_runtime(
    request: ControllerRuntimeRequest,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> ControllerRuntimeReport:
    """Analyze once, persist once, verify once, then launch exactly once."""

    if type(request) is not ControllerRuntimeRequest:
        raise ControllerRuntimeError("invalid_request")
    deps = _dependencies(dependencies)
    composition = compose_controller_source(request)
    try:
        conformance = deps.analyze_source(composition.source)
    except BaseException as exc:
        raise ControllerRuntimeError("source_conformance_failed") from exc
    if type(conformance) is not ControllerConformanceReport:
        raise ControllerRuntimeError("source_conformance_invalid")
    source_identity = _persist_source(composition, deps)
    process = _launch(request, source_identity, deps)
    return ControllerRuntimeReport(composition, conformance, source_identity, process)
