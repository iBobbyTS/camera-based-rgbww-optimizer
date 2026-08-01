"""Pure-offline machine-row and canonical patch diagnostic owner.

This module validates the PLAN/FULL contract before invoking the existing
read-only Git boundary.  It does not persist evidence or decide eligibility.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Callable, Mapping

from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    GitLedger,
    ProvenanceIOError,
    canonical_json_bytes,
    run_read_only_git,
)

__all__ = [
    "OfflinePatchPreflightError",
    "MachineRowPreflightResult",
    "CanonicalPatchDiagnosticSpec",
    "OfflinePatchPreflightResult",
    "run_offline_patch_preflight",
]


_SHA40 = re.compile(r"[0-9a-f]{40}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_PLAN_PREFIX = "PLAN_MACHINE_CONTRACT="
_FULL_PREFIX = "FULL_PLAN_MACHINE_STATE="


class OfflinePatchPreflightError(RuntimeError):
    """Fail-closed boundary error with a stable machine-readable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class MachineRowPreflightResult:
    plan_contract: Mapping[str, Any]
    full_state: Mapping[str, Any]
    required_full_state: Mapping[str, Any]


@dataclass(frozen=True)
class CanonicalPatchDiagnosticSpec:
    repo: str
    parent_sha: str
    child_sha: str
    paths: tuple[str, ...]
    expected_exit_code: int
    expected_stdout_bytes: int
    expected_stdout_sha256: str
    expected_stderr_bytes: int
    expected_stderr_sha256: str


@dataclass(frozen=True)
class OfflinePatchPreflightResult:
    machine_rows: MachineRowPreflightResult
    diagnostic_spec: CanonicalPatchDiagnosticSpec
    observed_argv: tuple[str, ...]
    observed_exit_code: int
    observed_stdout_bytes: int
    observed_stdout_sha256: str
    observed_stderr_bytes: int
    observed_stderr_sha256: str
    classification: str
    report_bytes: bytes


def _reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise OfflinePatchPreflightError("machine_row_duplicate_key")
        value[key] = item
    return value


def _reject_nonfinite(_value: str) -> None:
    raise OfflinePatchPreflightError("machine_row_nonfinite")


def _decode_rows(data: bytes, *, kind: str, prefix: str) -> dict[str, Any]:
    invalid_code = f"invalid_{kind}_bytes"
    if type(data) is not bytes:
        raise OfflinePatchPreflightError(invalid_code)
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise OfflinePatchPreflightError("machine_row_utf8_invalid") from exc
    if "\r" in text:
        raise OfflinePatchPreflightError("machine_row_cr_invalid")

    rows: list[str] = []
    for row in text.split("\n"):
        if len(row) < 2 or row[0] != "`" or row[-1] != "`":
            continue
        inner = row[1:-1]
        if inner.startswith(prefix):
            rows.append(inner[len(prefix):])
    if len(rows) != 1:
        raise OfflinePatchPreflightError(f"{kind}_row_count_invalid")
    try:
        value = json.loads(
            rows[0],
            object_pairs_hook=_reject_duplicate,
            parse_constant=_reject_nonfinite,
        )
    except OfflinePatchPreflightError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError) as exc:
        raise OfflinePatchPreflightError("machine_row_json_invalid") from exc
    if type(value) is not dict:
        raise OfflinePatchPreflightError("machine_row_json_invalid")
    return value


def _freeze(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _exact_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(
            _exact_equal(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            _exact_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _machine_rows(plan_bytes: bytes, full_bytes: bytes) -> tuple[MachineRowPreflightResult, dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = _decode_rows(plan_bytes, kind="plan", prefix=_PLAN_PREFIX)
    full = _decode_rows(full_bytes, kind="full", prefix=_FULL_PREFIX)
    required = plan.get("required_full_machine_state")
    if type(required) is not dict or any(type(key) is not str for key in required):
        raise OfflinePatchPreflightError("required_full_state_invalid")
    for key, expected in required.items():
        if key not in full or not _exact_equal(full[key], expected):
            raise OfflinePatchPreflightError("required_full_subset_mismatch")
    result = MachineRowPreflightResult(
        _freeze(plan), _freeze(full), _freeze(required)
    )
    return result, plan, full, required


def _repo_path(value: str) -> bool:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        return False
    if value.startswith("/") or "//" in value:
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _diagnostic_argv(spec: CanonicalPatchDiagnosticSpec) -> tuple[str, ...]:
    if type(spec) is not CanonicalPatchDiagnosticSpec:
        raise OfflinePatchPreflightError("diagnostic_spec_invalid")
    if type(spec.repo) is not str or not Path(spec.repo).is_absolute():
        raise OfflinePatchPreflightError("diagnostic_spec_invalid")
    if not _SHA40.fullmatch(spec.parent_sha) or not _SHA40.fullmatch(spec.child_sha):
        raise OfflinePatchPreflightError("patch_argv_invalid")
    if (
        type(spec.paths) is not tuple
        or not spec.paths
        or any(not _repo_path(path) for path in spec.paths)
        or tuple(sorted(spec.paths)) != spec.paths
        or len(set(spec.paths)) != len(spec.paths)
    ):
        raise OfflinePatchPreflightError("patch_argv_invalid")
    if (
        type(spec.expected_exit_code) is not int
        or spec.expected_exit_code != 0
        or type(spec.expected_stdout_bytes) is not int
        or spec.expected_stdout_bytes < 0
        or _SHA256.fullmatch(spec.expected_stdout_sha256) is None
        or type(spec.expected_stderr_bytes) is not int
        or spec.expected_stderr_bytes < 0
        or _SHA256.fullmatch(spec.expected_stderr_sha256) is None
    ):
        raise OfflinePatchPreflightError("patch_expectation_invalid")
    return (
        "git", "diff", "--binary", "--full-index", "--no-ext-diff",
        spec.parent_sha, spec.child_sha, "--", *spec.paths,
    )


def _runner(dependencies: Mapping[str, Callable[..., Any]] | None) -> Callable[..., Any]:
    if dependencies is None:
        return run_read_only_git
    if not isinstance(dependencies, Mapping) or set(dependencies) != {"run_git"}:
        raise OfflinePatchPreflightError("diagnostic_spec_invalid")
    run_git = dependencies["run_git"]
    if not callable(run_git):
        raise OfflinePatchPreflightError("diagnostic_spec_invalid")
    return run_git


def run_offline_patch_preflight(
    plan_bytes: bytes,
    full_bytes: bytes,
    diagnostic_spec: CanonicalPatchDiagnosticSpec,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> OfflinePatchPreflightResult:
    """Validate both machine rows, then execute one canonical read-only diff."""

    machine_rows, plan, full, required = _machine_rows(plan_bytes, full_bytes)
    argv = _diagnostic_argv(diagnostic_spec)
    run_git = _runner(dependencies)
    try:
        ledger = run_git(diagnostic_spec.repo, argv)
    except (ProvenanceIOError, OSError) as exc:
        raise OfflinePatchPreflightError("git_result_invalid") from exc
    if (
        type(ledger) is not GitLedger
        or ledger.argv != argv
        or ledger.cwd != diagnostic_spec.repo
        or type(ledger.exit_code) is not int
        or type(ledger.stdout) is not bytes
        or type(ledger.stderr) is not bytes
        or ledger.stdout_sha256 != hashlib.sha256(ledger.stdout).hexdigest()
        or ledger.stderr_sha256 != hashlib.sha256(ledger.stderr).hexdigest()
    ):
        raise OfflinePatchPreflightError("git_result_invalid")

    if ledger.exit_code != 0:
        classification = "CANONICAL_PATCH_GIT_FAILURE"
    elif (
        ledger.exit_code == diagnostic_spec.expected_exit_code
        and len(ledger.stdout) == diagnostic_spec.expected_stdout_bytes
        and ledger.stdout_sha256 == diagnostic_spec.expected_stdout_sha256
        and len(ledger.stderr) == diagnostic_spec.expected_stderr_bytes
        and ledger.stderr_sha256 == diagnostic_spec.expected_stderr_sha256
    ):
        classification = "CANONICAL_PATCH_EXACT_MATCH"
    else:
        classification = "CANONICAL_PATCH_OUTPUT_MISMATCH"

    report = {
        "schema": "p7_retained_r3_offline_patch_preflight_report_v1",
        "machine_rows": {
            "plan_schema": plan.get("schema"),
            "full_schema": full.get("schema"),
            "required_full_state": required,
        },
        "diagnostic": {
            "expected_argv": list(argv),
            "observed_argv": list(ledger.argv),
            "expected_exit_code": diagnostic_spec.expected_exit_code,
            "observed_exit_code": ledger.exit_code,
            "expected_stdout_bytes": diagnostic_spec.expected_stdout_bytes,
            "observed_stdout_bytes": len(ledger.stdout),
            "expected_stdout_sha256": diagnostic_spec.expected_stdout_sha256,
            "observed_stdout_sha256": ledger.stdout_sha256,
            "expected_stderr_bytes": diagnostic_spec.expected_stderr_bytes,
            "observed_stderr_bytes": len(ledger.stderr),
            "expected_stderr_sha256": diagnostic_spec.expected_stderr_sha256,
            "observed_stderr_sha256": ledger.stderr_sha256,
            "classification": classification,
        },
    }
    report_bytes = canonical_json_bytes(report)
    return OfflinePatchPreflightResult(
        machine_rows,
        diagnostic_spec,
        ledger.argv,
        ledger.exit_code,
        len(ledger.stdout),
        ledger.stdout_sha256,
        len(ledger.stderr),
        ledger.stderr_sha256,
        classification,
        report_bytes,
    )
