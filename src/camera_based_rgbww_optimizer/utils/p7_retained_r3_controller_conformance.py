"""Pure in-memory conformance and composition for retained-R3 controllers."""

from __future__ import annotations

import ast
from dataclasses import dataclass, fields
import hashlib
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.utils.agent_work_machine_contract import (
    MachineContractEvidence,
    ParsedMachineContract,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation import (
    ByteSpan,
    OwnedStatementPair,
    PreparedControllerSource,
    SealTargetIdentity,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
)

__all__ = [
    "ControllerConformanceError",
    "ControllerConformanceReport",
    "ControllerConformanceRequirements",
    "ControllerTransportReport",
    "LifecycleCallbacks",
    "LifecycleRequirements",
    "LifecycleResult",
    "RootIdentityChain",
    "analyze_controller_source",
    "execute_controller_lifecycle",
    "validate_root_identity_chain",
]


class ControllerConformanceError(RuntimeError):
    """Fail-closed error carrying one stable machine-readable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


_OWNER_TYPES = (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
    MachineContractEvidence,
    ParsedMachineContract,
    ByteSpan,
    OwnedStatementPair,
    PreparedControllerSource,
    SealTargetIdentity,
)
_OWNER_FIELDS = (
    ("DirectoryIdentity", ("path", "device", "inode", "mode")),
    (
        "FileIdentity",
        ("path", "data", "byte_count", "sha256", "device", "inode", "mode", "root"),
    ),
    (
        "GitLedger",
        ("argv", "cwd", "exit_code", "stdout", "stderr", "stdout_sha256", "stderr_sha256"),
    ),
    (
        "MachineContractEvidence",
        (
            "schema", "owner", "marker_ascii", "source_bytes", "source_sha256",
            "candidate_count", "candidate_lines", "line_number", "raw_row_bytes",
            "raw_row_sha256", "payload_bytes", "payload_sha256", "line_ending",
        ),
    ),
    ("ParsedMachineContract", ("value", "evidence")),
    ("ByteSpan", ("start", "end")),
    ("OwnedStatementPair", ("assignment_span", "validation_span", "function_name")),
    ("PreparedControllerSource", ("source", "source_sha256", "pair")),
    ("SealTargetIdentity", ("path", "byte_count", "sha256", "device", "inode")),
)
_PUBLIC_METHODS = (
    ("MachineContractEvidence", ("to_mapping",)),
    ("SealTargetIdentity", ("as_mapping",)),
)
_CALL_OWNERS = MappingProxyType(
    {
        "create_exclusive_root": "DirectoryIdentity",
        "read_existing_root": "DirectoryIdentity",
        "read_exact_file": "FileIdentity",
        "run_read_only_git": "GitLedger",
        "parse_plan_machine_contract": "ParsedMachineContract",
        "parse_full_plan_machine_state": "ParsedMachineContract",
        "locate_owned_statement_pair": "OwnedStatementPair",
        "prepare_controller_source": "PreparedControllerSource",
        "DirectoryIdentity": "DirectoryIdentity",
        "FileIdentity": "FileIdentity",
        "GitLedger": "GitLedger",
        "MachineContractEvidence": "MachineContractEvidence",
        "ParsedMachineContract": "ParsedMachineContract",
        "ByteSpan": "ByteSpan",
        "OwnedStatementPair": "OwnedStatementPair",
        "PreparedControllerSource": "PreparedControllerSource",
        "SealTargetIdentity": "SealTargetIdentity",
    }
)
_OWNER_CONSTRUCTORS = frozenset(owner.__name__ for owner in _OWNER_TYPES)
_OPAQUE_CALLS = frozenset(("validate_terminal_seal",))
_REFLECTION_CALLS = frozenset(
    ("getattr", "setattr", "delattr", "vars", "dir", "globals", "locals", "eval", "exec")
)
_EXISTING_ROOT_OWNER_MODULE = (
    "camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io"
)


@dataclass(frozen=True)
class ControllerConformanceRequirements:
    owner_fields: tuple[tuple[str, tuple[str, ...]], ...] = _OWNER_FIELDS
    public_methods: tuple[tuple[str, tuple[str, ...]], ...] = _PUBLIC_METHODS
    git_success_field: str = "exit_code"


@dataclass(frozen=True)
class ControllerTransportReport:
    effect_bindings: tuple[tuple[str, str, str], ...]
    fixture_bindings: tuple[tuple[str, str, str], ...]
    fixture_constructor_edges: tuple[tuple[str, str, str], ...]
    root_chain_compositions: tuple[tuple[str, str, tuple[str, ...], str], ...]
    root_chain_validations: tuple[tuple[str, str], ...]
    effect_transport_uses: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ControllerConformanceReport:
    source_sha256: str
    owner_fields: tuple[tuple[str, tuple[str, ...]], ...]
    public_methods: tuple[tuple[str, tuple[str, ...]], ...]
    bound_results: tuple[tuple[str, str], ...]
    attribute_uses: tuple[tuple[str, str], ...]
    root_reads: tuple[tuple[str, str], ...]
    transport: ControllerTransportReport


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _direct_assignment(call: ast.Call, parents: Mapping[ast.AST, ast.AST]) -> str | None:
    parent = parents.get(call)
    if isinstance(parent, ast.Assign) and parent.value is call and len(parent.targets) == 1:
        target = parent.targets[0]
        return target.id if isinstance(target, ast.Name) else None
    if isinstance(parent, ast.AnnAssign) and parent.value is call:
        return parent.target.id if isinstance(parent.target, ast.Name) else None
    return None


def _nearest_function(
    node: ast.AST, parents: Mapping[ast.AST, ast.AST]
) -> ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | None:
    current = parents.get(node)
    while current is not None:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            return current
        current = parents.get(current)
    return None


def _keyword_map(call: ast.Call) -> dict[str, ast.expr] | None:
    if any(keyword.arg is None for keyword in call.keywords):
        return None
    return {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg is not None}


def _name_tuple(node: ast.AST) -> tuple[str, ...] | None:
    if not isinstance(node, ast.Tuple):
        return None
    names: list[str] = []
    for element in node.elts:
        if not isinstance(element, ast.Name):
            return None
        names.append(element.id)
    return tuple(names)


def _current_owner_surface() -> tuple[
    tuple[tuple[str, tuple[str, ...]], ...], tuple[tuple[str, tuple[str, ...]], ...]
]:
    owner_fields = tuple((owner.__name__, tuple(field.name for field in fields(owner))) for owner in _OWNER_TYPES)
    public_methods = tuple(
        (
            owner.__name__,
            tuple(
                name
                for name, value in vars(owner).items()
                if not name.startswith("_") and callable(value)
            ),
        )
        for owner in _OWNER_TYPES
        if any(owner.__name__ == name for name, _methods in _PUBLIC_METHODS)
    )
    return owner_fields, public_methods


def _validate_existing_root_owner(tree: ast.Module) -> None:
    owner_imports = 0
    invalid_import = False
    owner_calls: list[ast.Call] = []
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                mentions_owner = alias.name == "read_existing_root" or (
                    node.module == _EXISTING_ROOT_OWNER_MODULE and alias.name == "*"
                )
                if not mentions_owner:
                    continue
                if (
                    node.level != 0
                    or node.module != _EXISTING_ROOT_OWNER_MODULE
                    or alias.name != "read_existing_root"
                    or alias.asname is not None
                ):
                    invalid_import = True
                else:
                    owner_imports += 1
        if isinstance(node, ast.Call) and _call_name(node) == "read_existing_root":
            owner_calls.append(node)

    if not owner_calls and not invalid_import and owner_imports == 0:
        return
    if invalid_import or owner_imports != 1:
        raise ControllerConformanceError("existing_root_owner_import_invalid")

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                bound_name = alias.asname or alias.name.split(".", 1)[0]
                if (
                    bound_name == "read_existing_root"
                    and not (
                        isinstance(node, ast.ImportFrom)
                        and node.level == 0
                        and node.module == _EXISTING_ROOT_OWNER_MODULE
                        and alias.name == "read_existing_root"
                        and alias.asname is None
                    )
                ):
                    raise ControllerConformanceError("existing_root_owner_import_invalid")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == "read_existing_root":
                raise ControllerConformanceError("existing_root_owner_import_invalid")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                arguments = (
                    *node.args.posonlyargs,
                    *node.args.args,
                    *node.args.kwonlyargs,
                )
                if any(argument.arg == "read_existing_root" for argument in arguments):
                    raise ControllerConformanceError("existing_root_owner_import_invalid")
                if (
                    node.args.vararg is not None
                    and node.args.vararg.arg == "read_existing_root"
                ) or (
                    node.args.kwarg is not None
                    and node.args.kwarg.arg == "read_existing_root"
                ):
                    raise ControllerConformanceError("existing_root_owner_import_invalid")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if node.id == "read_existing_root":
                raise ControllerConformanceError("existing_root_owner_import_invalid")
        if isinstance(node, ast.ExceptHandler) and node.name == "read_existing_root":
            raise ControllerConformanceError("existing_root_owner_import_invalid")
        if isinstance(node, (ast.Global, ast.Nonlocal)) and "read_existing_root" in node.names:
            raise ControllerConformanceError("existing_root_owner_import_invalid")

    for call in owner_calls:
        if (
            not isinstance(call.func, ast.Name)
            or call.func.id != "read_existing_root"
            or _direct_assignment(call, parents) is None
        ):
            raise ControllerConformanceError("existing_root_owner_call_invalid")


def analyze_controller_source(
    source: bytes,
    requirements: ControllerConformanceRequirements = ControllerConformanceRequirements(),
) -> ControllerConformanceReport:
    """Parse, compile and certify one runtime source domain independently."""

    if type(source) is not bytes:
        raise ControllerConformanceError("source_not_bytes")
    if type(requirements) is not ControllerConformanceRequirements:
        raise ControllerConformanceError("invalid_requirements")
    if (
        requirements.owner_fields != _OWNER_FIELDS
        or requirements.public_methods != _PUBLIC_METHODS
        or requirements.git_success_field != "exit_code"
    ):
        raise ControllerConformanceError("requirements_drift")
    current_fields, current_methods = _current_owner_surface()
    if current_fields != requirements.owner_fields:
        raise ControllerConformanceError("owner_schema_drift")
    if current_methods != requirements.public_methods:
        raise ControllerConformanceError("owner_method_drift")
    try:
        text = source.decode("utf-8", errors="strict")
        tree = ast.parse(text)
        compile(tree, "<retained-r3-controller>", "exec")
    except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
        raise ControllerConformanceError("source_parse_failed") from exc

    _validate_existing_root_owner(tree)

    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    bindings: dict[str, str] = {}
    effect_bindings: dict[str, tuple[str, str]] = {}
    fixture_bindings: dict[str, tuple[str, str]] = {}
    binding_functions: dict[str, ast.AST | None] = {}
    opaque: set[str] = set()
    root_names: set[str] = set()
    root_reads: list[tuple[str, str]] = []
    existing_root_bindings: set[str] = set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name in _REFLECTION_CALLS:
            raise ControllerConformanceError("reflection_rejected")
        owner = _CALL_OWNERS.get(name or "")
        if owner is not None:
            assigned = _direct_assignment(node, parents)
            if assigned is None:
                code = (
                    "existing_root_owner_call_invalid"
                    if name == "read_existing_root"
                    else "owner_result_unbound"
                )
                raise ControllerConformanceError(code)
            if assigned in bindings or assigned in opaque:
                raise ControllerConformanceError("owner_result_rebound")
            bindings[assigned] = owner
            binding_functions[assigned] = _nearest_function(node, parents)
            provenance = (owner, name or "")
            if name in _OWNER_CONSTRUCTORS:
                fixture_bindings[assigned] = provenance
            else:
                effect_bindings[assigned] = provenance
            if owner == "DirectoryIdentity" and assigned in effect_bindings:
                root_names.add(assigned)
                if name == "read_existing_root":
                    existing_root_bindings.add(assigned)
        elif name in _OPAQUE_CALLS:
            assigned = _direct_assignment(node, parents)
            if assigned is None:
                raise ControllerConformanceError("opaque_result_unbound")
            opaque.add(assigned)

        if name == "read_exact_file":
            roots = [keyword.value for keyword in node.keywords if keyword.arg == "root"]
            if len(roots) != 1 or not isinstance(roots[0], ast.Name):
                raise ControllerConformanceError("read_root_not_live_name")
            root_name = roots[0].id
            if root_name not in root_names or bindings.get(root_name) != "DirectoryIdentity":
                raise ControllerConformanceError("read_root_not_live_identity")
            assigned = _direct_assignment(node, parents)
            if assigned is None:
                raise ControllerConformanceError("owner_result_unbound")
            root_reads.append((assigned, root_name))

    for bound in existing_root_bindings:
        stores = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Store)
            and node.id == bound
        ]
        if len(stores) != 1:
            raise ControllerConformanceError("owner_result_rebound")

    fixture_constructor_edges: list[tuple[str, str, str]] = []
    root_chain_compositions: dict[str, tuple[str, tuple[str, ...], str]] = {}
    root_chain_validations: list[tuple[str, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        assigned = _direct_assignment(node, parents)
        if name in _OWNER_CONSTRUCTORS and assigned is not None:
            keywords = _keyword_map(node)
            for argument in (*node.args, *(node.keywords)):
                value = argument.value if isinstance(argument, ast.keyword) else argument
                if isinstance(value, ast.Name) and value.id in effect_bindings:
                    raise ControllerConformanceError("effect_fixture_constructor_transport")
            if keywords is None:
                if any(
                    isinstance(argument, ast.Name) and argument.id in fixture_bindings
                    for argument in node.args
                ):
                    raise ControllerConformanceError("fixture_constructor_edge_not_named")
                continue
            allowed_fields = set(dict(requirements.owner_fields)[name or ""])
            for field_name, value in keywords.items():
                if isinstance(value, ast.Name) and value.id in fixture_bindings:
                    if field_name not in allowed_fields:
                        raise ControllerConformanceError("fixture_constructor_edge_unknown_field")
                    fixture_constructor_edges.append((assigned, field_name, value.id))

        if name == "RootIdentityChain":
            if assigned is None or node.args:
                raise ControllerConformanceError("root_chain_shape_invalid")
            keywords = _keyword_map(node)
            if keywords is None or set(keywords) != {"before", "files", "after"}:
                raise ControllerConformanceError("root_chain_shape_invalid")
            before = keywords["before"]
            files = _name_tuple(keywords["files"])
            after = keywords["after"]
            if not isinstance(before, ast.Name) or not isinstance(after, ast.Name) or files is None:
                raise ControllerConformanceError("root_chain_shape_invalid")
            if (
                effect_bindings.get(before.id, (None,))[0] != "DirectoryIdentity"
                or effect_bindings.get(after.id, (None,))[0] != "DirectoryIdentity"
                or any(effect_bindings.get(item, (None,))[0] != "FileIdentity" for item in files)
            ):
                raise ControllerConformanceError("root_chain_effect_identity_required")
            if assigned in bindings or assigned in opaque or assigned in root_chain_compositions:
                raise ControllerConformanceError("owner_result_rebound")
            root_chain_compositions[assigned] = (before.id, files, after.id)

        if name == "validate_root_identity_chain":
            if (
                len(node.args) != 1
                or node.keywords
                or not isinstance(node.args[0], ast.Name)
                or node.args[0].id not in root_chain_compositions
            ):
                raise ControllerConformanceError("root_chain_validation_invalid")
            chain_name = node.args[0].id
            if any(existing == chain_name for existing, _validator in root_chain_validations):
                raise ControllerConformanceError("root_chain_validation_duplicate")
            root_chain_validations.append((chain_name, "validate_root_identity_chain"))

    for chain_name in root_chain_compositions:
        if not any(existing == chain_name for existing, _validator in root_chain_validations):
            raise ControllerConformanceError("root_chain_unvalidated")

    field_map = dict(requirements.owner_fields)
    method_map = dict(requirements.public_methods)
    attribute_uses: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if node.attr == "returncode":
            raise ControllerConformanceError("git_returncode_rejected")
        if node.attr == "__dict__":
            raise ControllerConformanceError("reflection_rejected")
        if not isinstance(node.value, ast.Name):
            if isinstance(node.value, ast.Call) and _call_name(node.value) in _CALL_OWNERS:
                raise ControllerConformanceError("owner_result_unbound")
            continue
        owner = bindings.get(node.value.id)
        if owner is not None:
            if node.attr not in field_map[owner] and node.attr not in method_map.get(owner, ()):
                raise ControllerConformanceError("unknown_owner_attribute")
            attribute_uses.append((node.value.id, node.attr))
        elif node.value.id in opaque:
            raise ControllerConformanceError("opaque_gate_introspection")

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if isinstance(value, ast.Name) and value.id in effect_bindings:
            raise ControllerConformanceError("effect_alias_transport")
        if isinstance(value, ast.Name) and (
            value.id in fixture_bindings or value.id in opaque or value.id in root_chain_compositions
        ):
            raise ControllerConformanceError("owner_alias_escape")

    exact_root_chain_nodes: set[ast.AST] = set()
    exact_validator_nodes: set[ast.AST] = set()
    exact_read_root_nodes: set[ast.AST] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name == "RootIdentityChain" and _direct_assignment(node, parents) in root_chain_compositions:
            exact_root_chain_nodes.add(node)
        elif name == "validate_root_identity_chain":
            exact_validator_nodes.add(node)
        elif name == "read_exact_file":
            exact_read_root_nodes.add(node)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Name) or node.id not in effect_bindings or not isinstance(node.ctx, ast.Load):
            continue
        parent = parents.get(node)
        if isinstance(parent, ast.Attribute) and parent.value is node:
            continue
        if isinstance(parent, ast.Compare):
            continue
        if isinstance(parent, ast.Call):
            if parent in exact_validator_nodes:
                continue
            if parent in exact_read_root_nodes and any(
                keyword.arg == "root" and keyword.value is node for keyword in parent.keywords
            ):
                continue
            if parent in exact_root_chain_nodes:
                continue
            raise ControllerConformanceError("effect_generic_helper_transport")
        if isinstance(parent, ast.keyword):
            call = parents.get(parent)
            if isinstance(call, ast.Call) and call in exact_root_chain_nodes:
                continue
            if isinstance(call, ast.Call) and call in exact_read_root_nodes and parent.arg == "root":
                continue
            if isinstance(call, ast.Call) and _call_name(call) in _OWNER_CONSTRUCTORS:
                continue
            raise ControllerConformanceError("effect_generic_helper_transport")
        if isinstance(parent, (ast.Tuple, ast.List, ast.Set, ast.Dict)):
            ancestor = parents.get(parent)
            if isinstance(parent, ast.Tuple) and isinstance(ancestor, ast.keyword):
                call = parents.get(ancestor)
                if isinstance(call, ast.Call) and call in exact_root_chain_nodes and ancestor.arg == "files":
                    continue
            raise ControllerConformanceError("effect_container_transport")
        if isinstance(parent, ast.Return):
            return_function = _nearest_function(parent, parents)
            code = (
                "effect_callback_return"
                if return_function is binding_functions.get(node.id)
                else "effect_closure_return"
            )
            raise ControllerConformanceError(code)
        if isinstance(parent, (ast.Assign, ast.AnnAssign)):
            continue
        raise ControllerConformanceError("effect_indirect_transport")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Name) or node.id not in root_chain_compositions or not isinstance(node.ctx, ast.Load):
            continue
        parent = parents.get(node)
        if isinstance(parent, ast.Call) and parent in exact_validator_nodes:
            continue
        raise ControllerConformanceError("root_chain_transport_invalid")

    transport = ControllerTransportReport(
        effect_bindings=tuple(
            sorted((bound, owner, call) for bound, (owner, call) in effect_bindings.items())
        ),
        fixture_bindings=tuple(
            sorted((bound, owner, call) for bound, (owner, call) in fixture_bindings.items())
        ),
        fixture_constructor_edges=tuple(sorted(fixture_constructor_edges)),
        root_chain_compositions=tuple(
            sorted(
                (chain, before, files, after)
                for chain, (before, files, after) in root_chain_compositions.items()
            )
        ),
        root_chain_validations=tuple(sorted(root_chain_validations)),
        effect_transport_uses=(),
    )

    return ControllerConformanceReport(
        source_sha256=hashlib.sha256(source).hexdigest(),
        owner_fields=current_fields,
        public_methods=current_methods,
        bound_results=tuple(sorted(bindings.items())),
        attribute_uses=tuple(sorted(attribute_uses)),
        root_reads=tuple(sorted(root_reads)),
        transport=transport,
    )


@dataclass(frozen=True)
class RootIdentityChain:
    before: DirectoryIdentity
    files: tuple[FileIdentity, ...]
    after: DirectoryIdentity


def _is_direct_child(path: str, root: str) -> bool:
    if type(path) is not str or type(root) is not str or not path.startswith("/") or not root.startswith("/"):
        return False
    if "\\" in path or "\\" in root or root == "/":
        return False
    parent, separator, child = path.rpartition("/")
    return bool(
        separator and parent == root and child not in {"", ".", ".."}
        and "/" not in child and all(part not in {"", ".", ".."} for part in path.split("/")[1:])
    )


def validate_root_identity_chain(chain: RootIdentityChain) -> RootIdentityChain:
    """Validate already-read identities without touching the filesystem."""

    if type(chain) is not RootIdentityChain:
        raise ControllerConformanceError("invalid_root_chain")
    if type(chain.before) is not DirectoryIdentity or type(chain.after) is not DirectoryIdentity:
        raise ControllerConformanceError("invalid_root_identity")
    if chain.before != chain.after:
        raise ControllerConformanceError("root_identity_drift")
    if chain.before.mode != 0o700:
        raise ControllerConformanceError("root_mode_mismatch")
    if type(chain.files) is not tuple:
        raise ControllerConformanceError("invalid_file_identities")
    for identity in chain.files:
        if type(identity) is not FileIdentity:
            raise ControllerConformanceError("invalid_file_identity")
        if identity.root != chain.before:
            raise ControllerConformanceError("file_root_mismatch")
        if not _is_direct_child(identity.path, chain.before.path):
            raise ControllerConformanceError("file_not_direct_child")
        if identity.device != chain.before.device:
            raise ControllerConformanceError("file_device_mismatch")
        if identity.mode != 0o600:
            raise ControllerConformanceError("file_mode_mismatch")
    return chain


@dataclass(frozen=True)
class LifecycleRequirements:
    success_order: tuple[str, ...] = (
        "conformance", "activation", "root", "inputs", "evaluate",
        "terminal", "terminal_seal", "admission",
    )
    retry: int = 0
    fallback: int = 0


LifecycleCallback = Callable[..., object]


@dataclass(frozen=True)
class LifecycleCallbacks:
    conformance: LifecycleCallback
    activation: LifecycleCallback
    root: LifecycleCallback
    inputs: LifecycleCallback
    evaluate: LifecycleCallback
    terminal: LifecycleCallback
    terminal_seal: LifecycleCallback
    admission: LifecycleCallback


@dataclass(frozen=True)
class LifecycleResult:
    order: tuple[str, ...]
    values: tuple[tuple[str, object], ...]


def _callback(callbacks: LifecycleCallbacks, phase: str) -> LifecycleCallback:
    callback = getattr(callbacks, phase)
    if not callable(callback):
        raise ControllerConformanceError(f"missing_callback:{phase}")
    return callback


def execute_controller_lifecycle(
    callbacks: LifecycleCallbacks,
    requirements: LifecycleRequirements = LifecycleRequirements(),
) -> LifecycleResult:
    """Compose injected callbacks with a sealed, retry-free terminal lifecycle."""

    if type(callbacks) is not LifecycleCallbacks or type(requirements) is not LifecycleRequirements:
        raise ControllerConformanceError("invalid_lifecycle")
    if requirements.retry != 0 or requirements.fallback != 0 or requirements.success_order != LifecycleRequirements().success_order:
        raise ControllerConformanceError("invalid_lifecycle_requirements")
    order: list[str] = []
    values: list[tuple[str, object]] = []
    primary: BaseException | None = None

    try:
        order.append("conformance")
        values.append(("conformance", _callback(callbacks, "conformance")()))
    except BaseException:
        raise

    for phase in ("activation", "root", "inputs", "evaluate"):
        try:
            order.append(phase)
            values.append((phase, _callback(callbacks, phase)()))
        except BaseException as exc:
            primary = exc
            break

    try:
        order.append("terminal")
        terminal = _callback(callbacks, "terminal")(primary, tuple(values))
        values.append(("terminal", terminal))
    except BaseException as exc:
        raise ControllerConformanceError("terminal_failed") from exc
    try:
        order.append("terminal_seal")
        seal = _callback(callbacks, "terminal_seal")(terminal)
        values.append(("terminal_seal", seal))
    except BaseException as exc:
        raise ControllerConformanceError("terminal_seal_failed") from exc
    try:
        order.append("admission")
        admission = _callback(callbacks, "admission")(seal)
        values.append(("admission", admission))
    except BaseException as exc:
        if primary is not None:
            raise primary from exc
        raise
    if primary is not None:
        raise primary
    return LifecycleResult(tuple(order), tuple(values))
