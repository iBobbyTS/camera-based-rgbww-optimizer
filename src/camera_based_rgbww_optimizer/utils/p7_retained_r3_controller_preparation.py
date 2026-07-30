"""Pure preparation primitives for retained-R3 controller source and seals.

This module deliberately owns no filesystem, process, validator, release, or
device operation.  Callers supply and consume bytes in memory.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
import re
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

__all__ = [
    "ByteSpan",
    "ControllerPreparationError",
    "ParentEdge",
    "PreparedControllerSource",
    "SealTargetIdentity",
    "SourceReplacement",
    "canonical_terminal_bytes",
    "locate_owned_statement_pair",
    "prepare_controller_source",
    "replace_byte_spans",
    "validate_and_emit_execution_result",
    "validate_terminal_seal",
]


_SHA256 = re.compile(r"[0-9a-f]{64}")
_GATE_TOKEN = object()


class ControllerPreparationError(ValueError):
    """Fail-closed preparation error with a stable machine-readable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ParentEdge:
    """One explicit AST parent edge, including list-field membership."""

    parent: ast.AST
    field: str
    index: int | None


@dataclass(frozen=True, order=True)
class ByteSpan:
    start: int
    end: int


@dataclass(frozen=True)
class SourceReplacement:
    span: ByteSpan
    replacement: bytes

    def __post_init__(self) -> None:
        if type(self.span) is not ByteSpan or type(self.replacement) is not bytes:
            raise ControllerPreparationError("invalid_replacement")


@dataclass(frozen=True)
class OwnedStatementPair:
    assignment_span: ByteSpan
    validation_span: ByteSpan
    function_name: str


@dataclass(frozen=True)
class PreparedControllerSource:
    source: bytes
    source_sha256: str
    pair: OwnedStatementPair


@dataclass(frozen=True)
class SealTargetIdentity:
    path: str
    byte_count: int
    sha256: str
    device: int
    inode: int

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path or "\x00" in self.path:
            raise ControllerPreparationError("invalid_target_path")
        for value, code in (
            (self.byte_count, "invalid_target_bytes"),
            (self.device, "invalid_target_device"),
            (self.inode, "invalid_target_inode"),
        ):
            if type(value) is not int or value < 0:
                raise ControllerPreparationError(code)
        if type(self.sha256) is not str or _SHA256.fullmatch(self.sha256) is None:
            raise ControllerPreparationError("invalid_target_sha256")

    def as_mapping(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "bytes": self.byte_count,
                "device": self.device,
                "inode": self.inode,
                "path": self.path,
                "sha256": self.sha256,
            }
        )


@dataclass(frozen=True, init=False)
class _ValidatedSealGate:
    payload: Mapping[str, object]
    target: SealTargetIdentity

    def __init__(
        self,
        token: object,
        payload: Mapping[str, object],
        target: SealTargetIdentity,
    ) -> None:
        if token is not _GATE_TOKEN:
            raise ControllerPreparationError("seal_gate_is_internal")
        object.__setattr__(self, "payload", _freeze_json(payload))
        object.__setattr__(self, "target", target)


def _freeze_json(value: object) -> object:
    """Return an immutable, detached snapshot of a strict-JSON value."""

    if type(value) is dict:
        return MappingProxyType(
            {key: _freeze_json(item) for key, item in value.items()}
        )
    if type(value) is list:
        return tuple(_freeze_json(item) for item in value)
    if type(value) in (str, int, float, bool) or value is None:
        return value
    raise ControllerPreparationError("terminal_not_json")


def _parent_edges(tree: ast.AST) -> dict[ast.AST, ParentEdge]:
    edges: dict[ast.AST, ParentEdge] = {}
    for parent in ast.walk(tree):
        for field, value in ast.iter_fields(parent):
            if isinstance(value, list):
                for index, child in enumerate(value):
                    if isinstance(child, ast.AST):
                        edges[child] = ParentEdge(parent, field, index)
            elif isinstance(value, ast.AST):
                edges[value] = ParentEdge(parent, field, None)
    return edges


def _regular_function_owner(
    node: ast.AST, edges: Mapping[ast.AST, ParentEdge]
) -> ast.FunctionDef:
    owners: list[ast.FunctionDef] = []
    current = node
    while current in edges:
        current = edges[current].parent
        if isinstance(current, ast.FunctionDef):
            owners.append(current)
        elif isinstance(current, (ast.AsyncFunctionDef, ast.Lambda)):
            raise ControllerPreparationError("alternate_function_owner")
    if not owners:
        raise ControllerPreparationError("function_owner_not_found")
    if len(owners) != 1:
        raise ControllerPreparationError("function_owner_ambiguous")
    return owners[0]


def _assigned_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        target = node.targets[0]
        return target.id if isinstance(target, ast.Name) else None
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def _is_validation_statement(node: ast.AST, function_name: str) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == function_name
    )


def _line_starts(source: bytes) -> tuple[int, ...]:
    starts = [0]
    starts.extend(index + 1 for index, value in enumerate(source) if value == 10)
    return tuple(starts)


def _node_span(node: ast.AST, source: bytes, starts: Sequence[int]) -> ByteSpan:
    values = (
        getattr(node, "lineno", None),
        getattr(node, "col_offset", None),
        getattr(node, "end_lineno", None),
        getattr(node, "end_col_offset", None),
    )
    if any(type(value) is not int for value in values):
        raise ControllerPreparationError("missing_source_span")
    lineno, col, end_lineno, end_col = values
    if not (1 <= lineno <= len(starts) and 1 <= end_lineno <= len(starts)):
        raise ControllerPreparationError("source_span_out_of_range")
    span = ByteSpan(starts[lineno - 1] + col, starts[end_lineno - 1] + end_col)
    if span.start < 0 or span.end <= span.start or span.end > len(source):
        raise ControllerPreparationError("invalid_source_span")
    return span


def locate_owned_statement_pair(
    source: bytes,
    *,
    assignment_name: str,
    validation_function: str,
) -> OwnedStatementPair:
    """Locate one same-list adjacent assignment/validation pair by AST edges."""

    if type(source) is not bytes:
        raise ControllerPreparationError("source_not_bytes")
    if type(assignment_name) is not str or not assignment_name.isidentifier():
        raise ControllerPreparationError("invalid_assignment_name")
    if type(validation_function) is not str or not validation_function.isidentifier():
        raise ControllerPreparationError("invalid_validation_function")
    try:
        text = source.decode("utf-8", errors="strict")
        tree = ast.parse(text)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise ControllerPreparationError("source_parse_failed") from exc

    edges = _parent_edges(tree)
    assignments = [node for node in ast.walk(tree) if _assigned_name(node) == assignment_name]
    if not assignments:
        raise ControllerPreparationError("assignment_not_found")
    if len(assignments) != 1:
        raise ControllerPreparationError("assignment_ambiguous")
    assignment = assignments[0]
    owner = _regular_function_owner(assignment, edges)
    edge = edges.get(assignment)
    if edge is None or edge.index is None:
        raise ControllerPreparationError("assignment_not_list_member")
    siblings = getattr(edge.parent, edge.field, None)
    if type(siblings) is not list or edge.index + 1 >= len(siblings):
        raise ControllerPreparationError("adjacent_validation_not_found")
    validation = siblings[edge.index + 1]
    if not _is_validation_statement(validation, validation_function):
        raise ControllerPreparationError("adjacent_validation_not_found")
    if _regular_function_owner(validation, edges) is not owner:
        raise ControllerPreparationError("cross_function_pair")

    starts = _line_starts(source)
    return OwnedStatementPair(
        assignment_span=_node_span(assignment, source, starts),
        validation_span=_node_span(validation, source, starts),
        function_name=owner.name,
    )


def replace_byte_spans(
    source: bytes, replacements: Sequence[SourceReplacement]
) -> bytes:
    """Apply non-overlapping UTF-8 byte-span replacements deterministically."""

    if type(source) is not bytes:
        raise ControllerPreparationError("source_not_bytes")
    try:
        replacement_items = tuple(replacements)
    except TypeError as exc:
        raise ControllerPreparationError("invalid_replacement") from exc
    if not replacement_items:
        raise ControllerPreparationError("replacement_set_empty")
    if any(type(item) is not SourceReplacement for item in replacement_items):
        raise ControllerPreparationError("invalid_replacement")
    ordered = sorted(replacement_items, key=lambda item: item.span.start)
    cursor = 0
    pieces: list[bytes] = []
    for item in ordered:
        start, end = item.span.start, item.span.end
        if type(start) is not int or type(end) is not int or start < 0 or end <= start:
            raise ControllerPreparationError("invalid_replacement_span")
        if end > len(source):
            raise ControllerPreparationError("replacement_span_out_of_range")
        if start < cursor:
            raise ControllerPreparationError("replacement_spans_overlap")
        pieces.extend((source[cursor:start], item.replacement))
        cursor = end
    pieces.append(source[cursor:])
    result = b"".join(pieces)
    try:
        text = result.decode("utf-8", errors="strict")
        tree = ast.parse(text)
        compile(tree, "<prepared-controller>", "exec")
    except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
        raise ControllerPreparationError("prepared_source_invalid") from exc
    return result


def prepare_controller_source(
    source: bytes,
    *,
    assignment_name: str,
    validation_function: str,
    replacement_statement: bytes,
) -> PreparedControllerSource:
    pair = locate_owned_statement_pair(
        source,
        assignment_name=assignment_name,
        validation_function=validation_function,
    )
    prepared = replace_byte_spans(
        source,
        (SourceReplacement(pair.assignment_span, replacement_statement),),
    )
    return PreparedControllerSource(
        source=prepared,
        source_sha256=hashlib.sha256(prepared).hexdigest(),
        pair=pair,
    )


def _reject_constant(value: str) -> object:
    raise ControllerPreparationError("terminal_non_finite")


def _strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ControllerPreparationError("terminal_duplicate_key")
        result[key] = value
    return result


def canonical_terminal_bytes(payload: Mapping[str, object]) -> bytes:
    """Serialize a terminal payload as canonical UTF-8 JSON plus exactly one LF."""

    if not isinstance(payload, Mapping):
        raise ControllerPreparationError("terminal_payload_not_mapping")
    try:
        body = json.dumps(
            dict(payload),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise ControllerPreparationError("terminal_not_json") from exc
    if b"\\n" in body:
        raise ControllerPreparationError("terminal_literal_backslash_n")
    result = body + b"\n"
    _strict_terminal_payload(result)
    return result


def _strict_terminal_payload(data: bytes) -> Mapping[str, object]:
    if type(data) is not bytes:
        raise ControllerPreparationError("terminal_not_bytes")
    if b"\\n" in data:
        raise ControllerPreparationError("terminal_literal_backslash_n")
    if b"\r" in data:
        raise ControllerPreparationError("terminal_crlf")
    if not data.endswith(b"\n"):
        raise ControllerPreparationError("terminal_missing_lf")
    if data.endswith(b"\n\n"):
        raise ControllerPreparationError("terminal_extra_lf")
    body = data[:-1]
    if b"\n" in body:
        raise ControllerPreparationError("terminal_embedded_lf")
    try:
        text = body.decode("utf-8", errors="strict")
        payload = json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_constant,
        )
    except ControllerPreparationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControllerPreparationError("terminal_parse_failed") from exc
    if type(payload) is not dict:
        raise ControllerPreparationError("terminal_payload_not_mapping")
    if canonical_terminal_bytes_without_validation(payload) != data:
        raise ControllerPreparationError("terminal_noncanonical")
    return payload


def canonical_terminal_bytes_without_validation(payload: Mapping[str, object]) -> bytes:
    try:
        body = json.dumps(
            dict(payload),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise ControllerPreparationError("terminal_not_json") from exc
    if b"\\n" in body:
        raise ControllerPreparationError("terminal_literal_backslash_n")
    return body + b"\n"


def validate_terminal_seal(
    data: bytes, expected_target: SealTargetIdentity
) -> _ValidatedSealGate:
    if type(expected_target) is not SealTargetIdentity:
        raise ControllerPreparationError("invalid_expected_target")
    payload = _strict_terminal_payload(data)
    target = payload.get("target")
    expected_mapping = dict(expected_target.as_mapping())
    if (
        type(target) is not dict
        or set(target) != set(expected_mapping)
        or any(
            type(target[key]) is not type(expected_value)
            or target[key] != expected_value
            for key, expected_value in expected_mapping.items()
        )
    ):
        raise ControllerPreparationError("terminal_target_mismatch")
    return _ValidatedSealGate(_GATE_TOKEN, payload, expected_target)


ExecutionResultCallback = Callable[[_ValidatedSealGate], object]


def validate_and_emit_execution_result(
    data: bytes,
    expected_target: SealTargetIdentity,
    callback: ExecutionResultCallback,
    *,
    primary_error: BaseException | None = None,
) -> object:
    """Invoke an injected ER callback only after exact seal validation."""

    gate = validate_terminal_seal(data, expected_target)
    if not callable(callback):
        raise ControllerPreparationError("execution_result_callback_missing")
    try:
        result = callback(gate)
    except BaseException as callback_error:
        if primary_error is not None:
            raise primary_error from callback_error
        raise
    if primary_error is not None:
        raise primary_error
    return result
