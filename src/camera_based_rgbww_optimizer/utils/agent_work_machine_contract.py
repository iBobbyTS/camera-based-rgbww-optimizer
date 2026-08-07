"""Validation-only parser for canonical agent-work machine contract rows."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Mapping, NoReturn


PLAN_MACHINE_MARKER = b"`PLAN_MACHINE_CONTRACT="
FULL_PLAN_MACHINE_MARKER = b"`FULL_PLAN_MACHINE_STATE="
PLAN_FULL_MACHINE_MARKER = b"`PLAN_FULL_MACHINE_CONTRACT="
_EVIDENCE_SCHEMA = "agent_work_machine_contract_scan_evidence_v1"

__all__ = [
    "PLAN_MACHINE_MARKER",
    "FULL_PLAN_MACHINE_MARKER",
    "PLAN_FULL_MACHINE_MARKER",
    "MachineContractValidationError",
    "MachineContractEvidence",
    "ParsedMachineContract",
    "parse_machine_row",
    "parse_plan_machine_contract",
    "parse_full_plan_machine_state",
    "parse_plan_full_machine_contract",
]


class MachineContractValidationError(ValueError):
    """A fail-closed machine-row validation error with replayable evidence."""

    def __init__(self, code: str, evidence: dict[str, object]) -> None:
        self.code = code
        self.evidence = evidence
        super().__init__(code)


@dataclass(frozen=True)
class MachineContractEvidence:
    schema: str
    owner: str
    marker_ascii: str
    source_bytes: int
    source_sha256: str
    candidate_count: int
    candidate_lines: tuple[int, ...]
    line_number: int
    raw_row_bytes: int
    raw_row_sha256: str
    payload_bytes: int
    payload_sha256: str
    line_ending: str

    def to_mapping(self) -> dict[str, object]:
        """Return a deterministic, JSON-serializable representation."""
        return {
            "schema": self.schema,
            "owner": self.owner,
            "marker_ascii": self.marker_ascii,
            "source_bytes": self.source_bytes,
            "source_sha256": self.source_sha256,
            "candidate_count": self.candidate_count,
            "candidate_lines": list(self.candidate_lines),
            "line_number": self.line_number,
            "raw_row_bytes": self.raw_row_bytes,
            "raw_row_sha256": self.raw_row_sha256,
            "payload_bytes": self.payload_bytes,
            "payload_sha256": self.payload_sha256,
            "line_ending": self.line_ending,
        }


@dataclass(frozen=True)
class ParsedMachineContract:
    value: Mapping[str, object]
    evidence: MachineContractEvidence


class _DuplicateKeyError(ValueError):
    pass


class _NonFiniteConstantError(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _reject_nonfinite_constant(value: str) -> NoReturn:
    raise _NonFiniteConstantError(value)


def _deep_freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


def _marker_ascii(marker: bytes) -> str:
    return marker.decode("ascii", errors="backslashreplace")


def _error(
    code: str,
    *,
    owner: str,
    marker: bytes,
    source: bytes | None,
    candidate_lines: tuple[int, ...] = (),
    line_number: int | None = None,
    raw_row: bytes | None = None,
    payload: bytes | None = None,
) -> NoReturn:
    evidence: dict[str, object] = {
        "schema": _EVIDENCE_SCHEMA,
        "owner": owner,
        "marker_ascii": _marker_ascii(marker),
        "source_bytes": len(source) if source is not None else None,
        "source_sha256": hashlib.sha256(source).hexdigest() if source is not None else None,
        "candidate_count": len(candidate_lines),
        "candidate_lines": list(candidate_lines),
        "line_number": line_number,
        "raw_row_bytes": len(raw_row) if raw_row is not None else None,
        "raw_row_sha256": hashlib.sha256(raw_row).hexdigest() if raw_row is not None else None,
        "payload_bytes": len(payload) if payload is not None else None,
        "payload_sha256": hashlib.sha256(payload).hexdigest() if payload is not None else None,
        "line_ending": "LF" if raw_row is not None and raw_row.endswith(b"`\n") else None,
    }
    raise MachineContractValidationError(code, evidence)


def _parse_machine_row(
    complete_text: bytes,
    *,
    owner: str,
    literal_marker: bytes,
) -> ParsedMachineContract:
    marker = b"`" + literal_marker
    if type(complete_text) is not bytes:
        _error("source_not_exact_bytes", owner=owner, marker=marker, source=None)

    lines = complete_text.splitlines(keepends=True)
    candidates = tuple(
        (line_number, line)
        for line_number, line in enumerate(lines, start=1)
        if line.startswith(marker)
    )
    candidate_lines = tuple(line_number for line_number, _line in candidates)
    if len(candidates) != 1:
        _error(
            "candidate_count_not_one",
            owner=owner,
            marker=marker,
            source=complete_text,
            candidate_lines=candidate_lines,
        )

    line_number, raw_row = candidates[0]
    if not raw_row.endswith(b"`\n") or raw_row.endswith(b"\r\n"):
        _error(
            "invalid_line_ending_or_suffix",
            owner=owner,
            marker=marker,
            source=complete_text,
            candidate_lines=candidate_lines,
            line_number=line_number,
            raw_row=raw_row,
        )
    if raw_row.count(b"`") != 2:
        _error(
            "invalid_backtick_count",
            owner=owner,
            marker=marker,
            source=complete_text,
            candidate_lines=candidate_lines,
            line_number=line_number,
            raw_row=raw_row,
        )

    payload = raw_row[len(marker):-2]
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        _error(
            "invalid_utf8",
            owner=owner,
            marker=marker,
            source=complete_text,
            candidate_lines=candidate_lines,
            line_number=line_number,
            raw_row=raw_row,
            payload=payload,
        )

    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite_constant,
        )
    except _DuplicateKeyError:
        code = "duplicate_json_key"
    except _NonFiniteConstantError:
        code = "nonfinite_json_constant"
    except json.JSONDecodeError:
        code = "malformed_json"
    else:
        if not isinstance(value, dict):
            _error(
                "top_level_not_object",
                owner=owner,
                marker=marker,
                source=complete_text,
                candidate_lines=candidate_lines,
                line_number=line_number,
                raw_row=raw_row,
                payload=payload,
            )
        evidence = MachineContractEvidence(
            schema=_EVIDENCE_SCHEMA,
            owner=owner,
            marker_ascii=_marker_ascii(marker),
            source_bytes=len(complete_text),
            source_sha256=hashlib.sha256(complete_text).hexdigest(),
            candidate_count=1,
            candidate_lines=candidate_lines,
            line_number=line_number,
            raw_row_bytes=len(raw_row),
            raw_row_sha256=hashlib.sha256(raw_row).hexdigest(),
            payload_bytes=len(payload),
            payload_sha256=hashlib.sha256(payload).hexdigest(),
            line_ending="LF",
        )
        frozen_value = _deep_freeze(value)
        assert isinstance(frozen_value, Mapping)
        return ParsedMachineContract(value=frozen_value, evidence=evidence)

    _error(
        code,
        owner=owner,
        marker=marker,
        source=complete_text,
        candidate_lines=candidate_lines,
        line_number=line_number,
        raw_row=raw_row,
        payload=payload,
    )


def parse_machine_row(
    complete_text: bytes,
    literal_marker: bytes,
) -> ParsedMachineContract:
    """Parse one exact Markdown-wrapped strict-JSON machine row."""
    if type(literal_marker) is not bytes:
        _error("marker_not_exact_bytes", owner="GENERIC", marker=b"<invalid>", source=None)
    if (
        not literal_marker
        or b"`" in literal_marker
        or b"\r" in literal_marker
        or b"\n" in literal_marker
    ):
        _error(
            "invalid_literal_marker",
            owner="GENERIC",
            marker=literal_marker,
            source=complete_text if type(complete_text) is bytes else None,
        )
    try:
        owner = literal_marker.decode("ascii").removesuffix("=")
    except UnicodeDecodeError:
        _error(
            "invalid_literal_marker",
            owner="GENERIC",
            marker=literal_marker,
            source=complete_text if type(complete_text) is bytes else None,
        )
    return _parse_machine_row(
        complete_text,
        owner=owner,
        literal_marker=literal_marker,
    )


def parse_plan_machine_contract(source: bytes) -> ParsedMachineContract:
    return _parse_machine_row(
        source,
        owner="PLAN",
        literal_marker=PLAN_MACHINE_MARKER[1:],
    )


def parse_full_plan_machine_state(source: bytes) -> ParsedMachineContract:
    return _parse_machine_row(
        source,
        owner="FULL",
        literal_marker=FULL_PLAN_MACHINE_MARKER[1:],
    )


def parse_plan_full_machine_contract(source: bytes) -> ParsedMachineContract:
    return _parse_machine_row(
        source,
        owner="PLAN_FULL",
        literal_marker=PLAN_FULL_MACHINE_MARKER[1:],
    )
