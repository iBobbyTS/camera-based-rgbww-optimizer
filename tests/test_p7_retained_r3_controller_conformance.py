from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, replace
import hashlib
import inspect
import unittest

from camera_based_rgbww_optimizer.utils import p7_retained_r3_controller_conformance as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
)


OWNER_IMPORT = (
    "from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io "
    "import read_existing_root\n"
)


def runtime(body: str) -> bytes:
    return ("def controller():\n" + "".join(f"    {line}\n" for line in body.splitlines())).encode()


def root() -> DirectoryIdentity:
    return DirectoryIdentity("/evidence", 7, 11, 0o700)


def file_identity(path: str = "/evidence/a.json", **changes: object) -> FileIdentity:
    values = {
        "path": path, "data": b"{}\n", "byte_count": 3,
        "sha256": hashlib.sha256(b"{}\n").hexdigest(), "device": 7,
        "inode": 12, "mode": 0o600, "root": root(),
    }
    values.update(changes)
    return FileIdentity(**values)


class ControllerConformanceTests(unittest.TestCase):
    def test_01_exact_owner_schemas_and_public_methods(self):
        report = subject.analyze_controller_source(runtime("span = ByteSpan(0, 1)\nvalue = span.end"))
        self.assertEqual(report.owner_fields, subject.ControllerConformanceRequirements().owner_fields)
        self.assertEqual(report.public_methods, (("MachineContractEvidence", ("to_mapping",)), ("SealTargetIdentity", ("as_mapping",))))
        self.assertEqual(len(report.owner_fields), 9)

    def test_02_git_exit_code_runtime_positive(self):
        report = subject.analyze_controller_source(runtime("ledger = run_read_only_git(repo, argv)\nassert ledger.exit_code == 0"))
        self.assertIn(("ledger", "exit_code"), report.attribute_uses)

    def test_03_returncode_negative_is_isolated_from_positive(self):
        positive = runtime("ledger = run_read_only_git(repo, argv)\nassert ledger.exit_code == 0")
        negative = runtime("ledger = run_read_only_git(repo, argv)\nassert ledger.returncode == 0")
        report = subject.analyze_controller_source(positive)
        with self.assertRaisesRegex(subject.ControllerConformanceError, "git_returncode_rejected"):
            subject.analyze_controller_source(negative)
        self.assertEqual(report.source_sha256, hashlib.sha256(positive).hexdigest())

    def test_04_unknown_attribute_and_unbound_owner_result_rejected(self):
        cases = (
            runtime("ledger = run_read_only_git(repo, argv)\nvalue = ledger.missing"),
            runtime("value = run_read_only_git(repo, argv).exit_code"),
        )
        for source in cases:
            with self.subTest(source=source), self.assertRaises(subject.ControllerConformanceError):
                subject.analyze_controller_source(source)

    def test_05_alias_and_reflection_rejected(self):
        cases = (
            "ledger = run_read_only_git(repo, argv)\nalias = ledger",
            "ledger = run_read_only_git(repo, argv)\nvalue = getattr(ledger, 'exit_code')",
            "ledger = run_read_only_git(repo, argv)\nvalue = vars(ledger)",
            "ledger = run_read_only_git(repo, argv)\nvalue = ledger.__dict__",
            "gate = validate_terminal_seal(data, target)\nvalue = gate.payload",
        )
        for body in cases:
            with self.subTest(body=body), self.assertRaises(subject.ControllerConformanceError):
                subject.analyze_controller_source(runtime(body))

    def test_06_root_bound_read_positive(self):
        report = subject.analyze_controller_source(runtime("root_id = create_exclusive_root(path)\nitem = read_exact_file(child, root=root_id)\nassert item.root == root_id"))
        self.assertEqual(report.root_reads, (("item", "root_id"),))

    def test_07_rootless_literal_and_different_root_rejected(self):
        cases = (
            "root_id = create_exclusive_root(path)\nitem = read_exact_file(child)",
            "root_id = create_exclusive_root(path)\nitem = read_exact_file(child, root='/tmp')",
            "root_id = create_exclusive_root(path)\nitem = read_exact_file(child, root=other)",
        )
        for body in cases:
            with self.subTest(body=body), self.assertRaises(subject.ControllerConformanceError):
                subject.analyze_controller_source(runtime(body))

    def test_08_identity_chain_positive(self):
        chain = subject.RootIdentityChain(root(), (file_identity(),), root())
        self.assertIs(subject.validate_root_identity_chain(chain), chain)

    def test_09_identity_chain_device_inode_mode_sibling_escape_negatives(self):
        negatives = (
            subject.RootIdentityChain(root(), (file_identity(device=8),), root()),
            subject.RootIdentityChain(root(), (file_identity(root=replace(root(), inode=99)),), root()),
            subject.RootIdentityChain(root(), (file_identity(root=replace(root(), mode=0o755)),), root()),
            subject.RootIdentityChain(root(), (file_identity(mode=0o644),), root()),
            subject.RootIdentityChain(root(), (file_identity("/sibling/a.json"),), root()),
            subject.RootIdentityChain(root(), (file_identity("/evidence/../a.json"),), root()),
        )
        for chain in negatives:
            with self.subTest(chain=chain), self.assertRaises(subject.ControllerConformanceError):
                subject.validate_root_identity_chain(chain)

    def test_10_success_lifecycle_exact_order_and_counts(self):
        calls: list[str] = []
        def callback(name: str):
            def invoke(*_args: object) -> str:
                calls.append(name)
                return name
            return invoke
        callbacks = subject.LifecycleCallbacks(*(callback(name) for name in subject.LifecycleRequirements().success_order))
        result = subject.execute_controller_lifecycle(callbacks)
        self.assertEqual(result.order, subject.LifecycleRequirements().success_order)
        self.assertEqual(tuple(calls), result.order)

    def test_11_primary_phase_failure_ordering(self):
        phases = ("conformance", "activation", "root", "inputs", "evaluate")
        for failed in phases:
            calls: list[str] = []
            primary = LookupError(failed)
            def callback(name: str):
                def invoke(*_args: object) -> str:
                    calls.append(name)
                    if name == failed:
                        raise primary
                    return name
                return invoke
            callbacks = subject.LifecycleCallbacks(*(callback(name) for name in subject.LifecycleRequirements().success_order))
            with self.subTest(failed=failed), self.assertRaises(BaseException) as raised:
                subject.execute_controller_lifecycle(callbacks)
            self.assertIs(raised.exception, primary)
            if failed == "conformance":
                self.assertEqual(calls, ["conformance"])
            else:
                self.assertEqual(calls[-3:], ["terminal", "terminal_seal", "admission"])

    def test_12_terminal_and_seal_failure_block_admission(self):
        for failed in ("terminal", "terminal_seal"):
            calls: list[str] = []
            def callback(name: str):
                def invoke(*_args: object) -> str:
                    calls.append(name)
                    if name == failed:
                        raise LookupError(name)
                    return name
                return invoke
            callbacks = subject.LifecycleCallbacks(*(callback(name) for name in subject.LifecycleRequirements().success_order))
            with self.subTest(failed=failed), self.assertRaises(subject.ControllerConformanceError):
                subject.execute_controller_lifecycle(callbacks)
            self.assertNotIn("admission", calls)

    def test_13_valid_fail_admission_preserves_primary_identity(self):
        primary = LookupError("primary")
        calls: list[str] = []
        def callback(name: str):
            def invoke(*_args: object) -> str:
                calls.append(name)
                if name == "evaluate":
                    raise primary
                return name
            return invoke
        callbacks = subject.LifecycleCallbacks(*(callback(name) for name in subject.LifecycleRequirements().success_order))
        with self.assertRaises(LookupError) as raised:
            subject.execute_controller_lifecycle(callbacks)
        self.assertIs(raised.exception, primary)
        self.assertEqual(calls[-3:], ["terminal", "terminal_seal", "admission"])

    def test_14_static_boundary_and_exact_exports(self):
        source = inspect.getsource(subject)
        tree = ast.parse(source)
        imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        self.assertFalse({"os", "pathlib", "subprocess", "socket", "requests"} & imported)
        self.assertFalse(any(isinstance(node, ast.Import) and any(alias.name in {"os", "pathlib", "subprocess", "socket", "requests"} for alias in node.names) for node in ast.walk(tree)))
        self.assertEqual(subject.__all__, [
            "ControllerConformanceError", "ControllerConformanceReport",
            "ControllerConformanceRequirements", "ControllerTransportReport",
            "LifecycleCallbacks",
            "LifecycleRequirements", "LifecycleResult", "RootIdentityChain",
            "analyze_controller_source", "execute_controller_lifecycle",
            "validate_root_identity_chain",
        ])
        self.assertEqual(len([name for name in dir(self) if name.startswith("test_")]), 25)

    def test_15_transport_report_classifies_effect_and_fixture_bindings(self):
        report = subject.analyze_controller_source(runtime(
            "live_root = create_exclusive_root(path)\n"
            "live_file = read_exact_file(child, root=live_root)\n"
            "fixture_root = DirectoryIdentity(path='/fixture', device=7, inode=9, mode=448)\n"
            "fixture_file = FileIdentity(path='/fixture/a', data=b'x', byte_count=1, "
            "sha256='0', device=7, inode=10, mode=384, root=fixture_root)\n"
            "assert live_file.root == live_root"
        ))
        self.assertEqual(report.transport.effect_bindings, (
            ("live_file", "FileIdentity", "read_exact_file"),
            ("live_root", "DirectoryIdentity", "create_exclusive_root"),
        ))
        self.assertEqual(report.transport.fixture_bindings, (
            ("fixture_file", "FileIdentity", "FileIdentity"),
            ("fixture_root", "DirectoryIdentity", "DirectoryIdentity"),
        ))
        self.assertEqual(
            report.transport.fixture_constructor_edges,
            (("fixture_file", "root", "fixture_root"),),
        )
        self.assertEqual(report.transport.effect_transport_uses, ())

    def test_16_fixture_file_root_composition_is_not_live_transport(self):
        report = subject.analyze_controller_source(runtime(
            "drift_root = DirectoryIdentity(path='/fixture', device=7, inode=9, mode=448)\n"
            "drift_file = FileIdentity(path='/fixture/a', data=b'x', byte_count=1, "
            "sha256='0', device=7, inode=10, mode=384, root=drift_root)"
        ))
        self.assertEqual(report.transport.effect_bindings, ())
        self.assertEqual(report.transport.fixture_bindings, (
            ("drift_file", "FileIdentity", "FileIdentity"),
            ("drift_root", "DirectoryIdentity", "DirectoryIdentity"),
        ))
        self.assertEqual(
            report.transport.fixture_constructor_edges,
            (("drift_file", "root", "drift_root"),),
        )
        self.assertEqual(report.transport.effect_transport_uses, ())

    def test_17_effect_identity_cannot_masquerade_as_fixture(self):
        source = runtime(
            "live_root = create_exclusive_root(path)\n"
            "forged = FileIdentity(path='/fixture/a', data=b'x', byte_count=1, "
            "sha256='0', device=7, inode=10, mode=384, root=live_root)"
        )
        with self.assertRaises(subject.ControllerConformanceError) as raised:
            subject.analyze_controller_source(source)
        self.assertEqual(raised.exception.code, "effect_fixture_constructor_transport")

    def test_18_effect_alias_container_and_generic_helper_transport_rejected(self):
        cases = {
            "alias": (
                "live = create_exclusive_root(path)\nalias = live",
                "effect_alias_transport",
            ),
            "container": (
                "live = create_exclusive_root(path)\nitems = [live]",
                "effect_container_transport",
            ),
            "generic_helper_argument": (
                "live = create_exclusive_root(path)\nconsume(live)",
                "effect_generic_helper_transport",
            ),
            "callback_return": (
                "live = create_exclusive_root(path)\nreturn live",
                "effect_callback_return",
            ),
            "closure_return": (
                "live = create_exclusive_root(path)\ndef inner():\n    return live\ninner()",
                "effect_closure_return",
            ),
        }
        for name, (body, code) in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(subject.ControllerConformanceError) as raised:
                    subject.analyze_controller_source(runtime(body))
                self.assertEqual(raised.exception.code, code)

    def test_19_exact_root_identity_chain_composition_only_exception(self):
        prefix = (
            "before = create_exclusive_root(path)\n"
            "item = read_exact_file(child, root=before)\n"
            "after = create_exclusive_root(path)\n"
        )
        report = subject.analyze_controller_source(runtime(
            prefix
            + "chain = RootIdentityChain(before=before, files=(item,), after=after)\n"
            + "validated = validate_root_identity_chain(chain)"
        ))
        self.assertEqual(
            report.transport.root_chain_compositions,
            (("chain", "before", ("item",), "after"),),
        )
        self.assertEqual(
            report.transport.root_chain_validations,
            (("chain", "validate_root_identity_chain"),),
        )
        self.assertEqual(report.transport.effect_transport_uses, ())

        near_misses = {
            "positional": (
                "chain = RootIdentityChain(before, (item,), after)\n"
                "validated = validate_root_identity_chain(chain)",
                "root_chain_shape_invalid",
            ),
            "list_files": (
                "chain = RootIdentityChain(before=before, files=[item], after=after)\n"
                "validated = validate_root_identity_chain(chain)",
                "root_chain_shape_invalid",
            ),
            "missing": (
                "chain = RootIdentityChain(before=before, files=(item,))\n"
                "validated = validate_root_identity_chain(chain)",
                "root_chain_shape_invalid",
            ),
            "extra": (
                "chain = RootIdentityChain(before=before, files=(item,), after=after, extra=1)\n"
                "validated = validate_root_identity_chain(chain)",
                "root_chain_shape_invalid",
            ),
            "wrong_validator": (
                "chain = RootIdentityChain(before=before, files=(item,), after=after)\n"
                "validated = validate_other(chain)",
                "root_chain_unvalidated",
            ),
            "alias": (
                "chain = RootIdentityChain(before=before, files=(item,), after=after)\n"
                "validated = validate_root_identity_chain(chain)\nalias = chain",
                "owner_alias_escape",
            ),
        }
        for name, (tail, code) in near_misses.items():
            with self.subTest(name=name):
                with self.assertRaises(subject.ControllerConformanceError) as raised:
                    subject.analyze_controller_source(runtime(prefix + tail))
                self.assertEqual(raised.exception.code, code)

    def test_20_transport_report_is_deterministic_and_exports_exact(self):
        source = runtime(
            "live = create_exclusive_root(path)\n"
            "value = live.path\n"
            "fixture = DirectoryIdentity(path='/fixture', device=7, inode=9, mode=448)"
        )
        first = subject.analyze_controller_source(source).transport
        second = subject.analyze_controller_source(source).transport
        self.assertEqual(first, second)
        self.assertTrue(all(isinstance(getattr(first, field.name), tuple) for field in fields(first)))
        with self.assertRaises(FrozenInstanceError):
            first.effect_bindings = ()
        self.assertIn("ControllerTransportReport", subject.__all__)
        module_tree = ast.parse(inspect.getsource(subject))
        analyzers = [
            node.name for node in ast.walk(module_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and "analyze" in node.name and "controller" in node.name
        ]
        self.assertEqual(analyzers, ["analyze_controller_source"])
        self.assertEqual(
            [name for name in subject.__all__ if "analyze" in name],
            ["analyze_controller_source"],
        )

    def test_21_existing_root_exact_import_direct_call_and_read_positive(self):
        source = runtime(
            OWNER_IMPORT
            + "existing = read_existing_root(source_root)\n"
            + "item = read_exact_file(source_path, root=existing)\n"
            + "assert item.root == existing"
        )
        report = subject.analyze_controller_source(source)
        self.assertEqual(
            report.bound_results,
            (("existing", "DirectoryIdentity"), ("item", "FileIdentity")),
        )
        self.assertEqual(report.root_reads, (("item", "existing"),))
        self.assertEqual(
            report.transport.effect_bindings,
            (
                ("existing", "DirectoryIdentity", "read_existing_root"),
                ("item", "FileIdentity", "read_exact_file"),
            ),
        )
        self.assertEqual(report.transport.effect_transport_uses, ())

    def test_22_multiple_existing_and_created_roots_are_reported_deterministically(self):
        source = runtime(
            OWNER_IMPORT
            + "alpha = read_existing_root(alpha_path)\n"
            + "alpha_file = read_exact_file(alpha_child, root=alpha)\n"
            + "beta = read_existing_root(beta_path)\n"
            + "beta_file = read_exact_file(beta_child, root=beta)\n"
            + "output = create_exclusive_root(output_path)\n"
            + "output_file = read_exact_file(output_child, root=output)"
        )
        first = subject.analyze_controller_source(source)
        second = subject.analyze_controller_source(source)
        self.assertEqual(first, second)
        self.assertEqual(
            first.root_reads,
            (
                ("alpha_file", "alpha"),
                ("beta_file", "beta"),
                ("output_file", "output"),
            ),
        )
        self.assertEqual(
            tuple(item for item in first.transport.effect_bindings if item[1] == "DirectoryIdentity"),
            (
                ("alpha", "DirectoryIdentity", "read_existing_root"),
                ("beta", "DirectoryIdentity", "read_existing_root"),
                ("output", "DirectoryIdentity", "create_exclusive_root"),
            ),
        )

    def test_23_existing_root_import_and_call_provenance_near_misses_rejected(self):
        cases = {
            "missing": (
                "existing = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
            "wrong_module": (
                "from elsewhere import read_existing_root\nexisting = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
            "duplicate": (
                OWNER_IMPORT + OWNER_IMPORT + "existing = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
            "alias": (
                OWNER_IMPORT.replace("read_existing_root", "read_existing_root as acquire")
                + "existing = acquire(path)",
                "existing_root_owner_import_invalid",
            ),
            "wildcard": (
                OWNER_IMPORT.replace("read_existing_root", "*")
                + "existing = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
            "attribute": (
                OWNER_IMPORT
                + "import camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io as provenance\n"
                + "existing = provenance.read_existing_root(path)",
                "existing_root_owner_call_invalid",
            ),
            "local_shadow": (
                OWNER_IMPORT
                + "def read_existing_root(value):\n"
                + "    return value\n"
                + "existing = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
            "argument_shadow": (
                OWNER_IMPORT
                + "def helper(read_existing_root):\n"
                + "    return read_existing_root\n"
                + "existing = read_existing_root(path)",
                "existing_root_owner_import_invalid",
            ),
        }
        for name, (body, code) in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(subject.ControllerConformanceError) as raised:
                    subject.analyze_controller_source(runtime(body))
                self.assertEqual(raised.exception.code, code)

    def test_24_existing_root_transport_and_read_shape_negatives_remain_closed(self):
        prefix = OWNER_IMPORT + "existing = read_existing_root(path)\n"
        cases = {
            "constructor": (
                "fixture = DirectoryIdentity(path='/x', device=1, inode=2, mode=448)\n"
                "item = read_exact_file(child, root=fixture)",
                "read_root_not_live_identity",
            ),
            "nested_owner": (
                OWNER_IMPORT + "item = read_exact_file(child, root=read_existing_root(path))",
                "existing_root_owner_call_invalid",
            ),
            "alias": (prefix + "alias = existing", "effect_alias_transport"),
            "rebind": (prefix + "existing = other", "owner_result_rebound"),
            "container": (prefix + "roots = [existing]", "effect_container_transport"),
            "reflection": (prefix + "value = getattr(existing, 'path')", "reflection_rejected"),
            "generic_helper": (prefix + "consume(existing)", "effect_generic_helper_transport"),
            "rootless": (prefix + "item = read_exact_file(child)", "read_root_not_live_name"),
            "positional": (
                prefix + "item = read_exact_file(child, existing)",
                "read_root_not_live_name",
            ),
            "non_name": (
                prefix + "item = read_exact_file(child, root=(existing,))",
                "read_root_not_live_name",
            ),
        }
        for name, (body, code) in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(subject.ControllerConformanceError) as raised:
                    subject.analyze_controller_source(runtime(body))
                self.assertEqual(raised.exception.code, code)

    def test_25_created_existing_chain_schema_and_effect_escape_regressions(self):
        positive = runtime(
            OWNER_IMPORT
            + "before = read_existing_root(source_root)\n"
            + "item = read_exact_file(source_child, root=before)\n"
            + "after = read_existing_root(source_root)\n"
            + "chain = RootIdentityChain(before=before, files=(item,), after=after)\n"
            + "validated = validate_root_identity_chain(chain)\n"
            + "output = create_exclusive_root(output_root)\n"
            + "output_item = read_exact_file(output_child, root=output)"
        )
        report = subject.analyze_controller_source(positive)
        self.assertEqual(len(report.owner_fields), 9)
        self.assertEqual(
            report.transport.root_chain_compositions,
            (("chain", "before", ("item",), "after"),),
        )
        self.assertEqual(
            report.transport.root_chain_validations,
            (("chain", "validate_root_identity_chain"),),
        )
        self.assertEqual(report.transport.effect_transport_uses, ())

        tree = ast.parse(positive.decode("utf-8"))
        imports = [
            (node.module, tuple((alias.name, alias.asname) for alias in node.names))
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and any(
                alias.name == "read_existing_root" for alias in node.names
            )
        ]
        self.assertEqual(
            imports,
            [(
                "camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io",
                (("read_existing_root", None),),
            )],
        )
        self.assertEqual(subject._CALL_OWNERS["read_existing_root"], "DirectoryIdentity")

        with self.assertRaises(subject.ControllerConformanceError) as raised:
            subject.analyze_controller_source(runtime(
                OWNER_IMPORT
                + "existing = read_existing_root(path)\n"
                + "leaked = helper(existing)"
            ))
        self.assertEqual(raised.exception.code, "effect_generic_helper_transport")


if __name__ == "__main__":
    unittest.main()
