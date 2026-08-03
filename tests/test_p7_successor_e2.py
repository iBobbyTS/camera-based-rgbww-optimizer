import ast
import copy
import inspect
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_successor_e2 as subject
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


TEMP_PARENT = "/Volumes/4T/temp/rgbww-optimizer"
SOURCE_CHECKPOINT = "1" * 40
SOURCE_TREE = "2" * 40
ALTERNATE_SOURCE_CHECKPOINT = "a" * 40
ALTERNATE_SOURCE_TREE = "b" * 40
REJECTED_HISTORICAL_ROOT = (
    "/Volumes/4T/temp/rgbww-optimizer/"
    "g4-e2-preformal-4995f7d65141-20260803T204648Z"
)
_ROOT_SEQUENCE = 0


def _fresh_root_path():
    global _ROOT_SEQUENCE
    _ROOT_SEQUENCE += 1
    nonce = f"{os.getpid():06x}{_ROOT_SEQUENCE:06x}"[-12:]
    return f"{TEMP_PARENT}/g4-e2-preformal-{nonce}-20990101T000000Z"


class OwnedE2Roots:
    """Own at most two exact E2 roots and remove only identity-bound files."""

    _KNOWN_FILES = frozenset((*subject.ARTIFACT_NAMES, "extra.json"))

    def __init__(self, count=1):
        if type(count) is not int or not 1 <= count <= 2:
            raise AssertionError("test root count must be one or two")
        self.paths = tuple(_fresh_root_path() for _ in range(count))
        self.identities = {}

    def __enter__(self):
        for path in self.paths:
            if path == REJECTED_HISTORICAL_ROOT or os.path.lexists(path):
                raise AssertionError(f"test root is not fresh: {path}")
        return self

    def create(self, path):
        if path not in self.paths or path in self.identities:
            raise AssertionError("test attempted unowned or repeated root creation")
        identity = provenance.create_exclusive_root(path)
        if type(identity) is not provenance.DirectoryIdentity or identity.path != path:
            raise AssertionError("provenance owner returned the wrong root identity")
        self.identities[path] = identity
        return identity

    def __exit__(self, exc_type, exc, traceback):
        cleanup_error = None
        for path in reversed(self.paths):
            identity = self.identities.get(path)
            if identity is None:
                if os.path.lexists(path) and cleanup_error is None:
                    cleanup_error = AssertionError(f"unowned test root appeared: {path}")
                continue
            try:
                if path == REJECTED_HISTORICAL_ROOT:
                    raise AssertionError("refusing historical-root cleanup")
                parent, separator, _basename = path.rpartition("/")
                if separator != "/" or parent != TEMP_PARENT:
                    raise AssertionError("test root is not an exact direct child")
                current = provenance.read_existing_root(path)
                if current != identity:
                    raise AssertionError("test root identity drifted")
                inventory = provenance.list_exact_regular_children(current)
                if not set(inventory).issubset(self._KNOWN_FILES):
                    raise AssertionError(f"unknown test artifact inventory: {inventory!r}")
                for name in inventory:
                    child = provenance.read_exact_file(
                        Path(path) / name,
                        expected_mode=0o600,
                        root=current,
                    )
                    os.unlink(child.path)
                os.rmdir(path)
                if os.path.lexists(path):
                    raise AssertionError(f"test root residual: {path}")
            except BaseException as error:
                cleanup_error = cleanup_error or error
        if cleanup_error is not None:
            raise cleanup_error
        return False


class E2TestCase(unittest.TestCase):
    def setUp(self):
        self.output_root = _fresh_root_path()
        self.inputs = subject.frozen_e2_input(
            output_root=self.output_root,
            source_checkpoint=SOURCE_CHECKPOINT,
            source_tree=SOURCE_TREE,
        )

    def evaluate(self, *, inputs=None, plan=None, status=None):
        calls = {"build": 0, "validate": 0, "status": 0}
        chosen_plan = thermal.build_td_b_r6_formal_plan() if plan is None else plan
        chosen_status = thermal.td_b_r6_machine_status() if status is None else status

        def build():
            calls["build"] += 1
            return copy.deepcopy(chosen_plan)

        def validate(value):
            calls["validate"] += 1
            thermal.validate_td_b_r6_formal_plan(value)

        def machine_status():
            calls["status"] += 1
            return copy.deepcopy(chosen_status)

        result = subject.evaluate_e2_preformal_gate(
            self.inputs if inputs is None else inputs,
            build_plan_fn=build,
            validate_plan_fn=validate,
            machine_status_fn=machine_status,
        )
        self.assertEqual(calls, {"build": 1, "validate": 1, "status": 1})
        return result

    def native_result(self):
        return provenance.json_native_value(self.evaluate())

    def assert_result_rejected(self, value, *, inputs=None):
        with self.assertRaises(subject.E2ContractError):
            subject._validate_result_contract(
                value,
                self.inputs if inputs is None else inputs,
            )


class FrozenInputTests(E2TestCase):
    def test_frozen_input_requires_three_exact_keyword_only_bindings(self):
        signature = inspect.signature(subject.frozen_e2_input)
        self.assertEqual(
            tuple(signature.parameters),
            ("output_root", "source_checkpoint", "source_tree"),
        )
        for name in signature.parameters:
            parameter = signature.parameters[name]
            self.assertEqual(parameter.kind, inspect.Parameter.KEYWORD_ONLY)
            self.assertIs(parameter.default, inspect.Parameter.empty)
            self.assertEqual(parameter.annotation, "str")
        with self.assertRaises(TypeError):
            subject.frozen_e2_input()
        with self.assertRaises(TypeError):
            subject.frozen_e2_input(self.output_root)
        for missing in ("output_root", "source_checkpoint", "source_tree"):
            values = {
                "output_root": self.output_root,
                "source_checkpoint": SOURCE_CHECKPOINT,
                "source_tree": SOURCE_TREE,
            }
            del values[missing]
            with self.subTest(missing=missing), self.assertRaises(TypeError):
                subject.frozen_e2_input(**values)
        with self.assertRaises(TypeError):
            subject.frozen_e2_input(
                output_root=self.output_root,
                source_checkpoint=SOURCE_CHECKPOINT,
                source_tree=SOURCE_TREE,
                unexpected=True,
            )
        self.assertEqual(
            subject.frozen_e2_input(
                output_root=self.output_root,
                source_checkpoint=SOURCE_CHECKPOINT,
                source_tree=SOURCE_TREE,
            ).output_root,
            self.output_root,
        )

    def test_output_root_validation_is_strict_lexical_and_has_no_filesystem_io(self):
        with mock.patch.object(provenance, "create_exclusive_root") as create, \
             mock.patch.object(provenance, "read_existing_root") as read, \
             mock.patch.object(provenance, "list_exact_regular_children") as inventory:
            value = subject.frozen_e2_input(
                output_root=self.output_root,
                source_checkpoint=SOURCE_CHECKPOINT,
                source_tree=SOURCE_TREE,
            )
        self.assertEqual(value.output_root, self.output_root)
        create.assert_not_called()
        read.assert_not_called()
        inventory.assert_not_called()

        class StringSubclass(str):
            pass

        invalid = (
            None,
            b"bytes",
            Path(self.output_root),
            StringSubclass(self.output_root),
            "",
            "relative/root",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101T000000Z/child",
            f"{TEMP_PARENT}//g4-e2-preformal-abcdef123456-20990101T000000Z",
            f"{TEMP_PARENT}/./g4-e2-preformal-abcdef123456-20990101T000000Z",
            f"{TEMP_PARENT}/../g4-e2-preformal-abcdef123456-20990101T000000Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101T000000Z/",
            f"{TEMP_PARENT}/g4-e2-preformal-ABCDEF123456-20990101T000000Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcde123456-20990101T000000Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990229T000000Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101T240000Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101T000060Z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101t000000z",
            f"{TEMP_PARENT}/g4-e2-preformal-abcdef123456-20990101T000000Z\n",
            f"{TEMP_PARENT}\\g4-e2-preformal-abcdef123456-20990101T000000Z",
        )
        with mock.patch.object(provenance, "create_exclusive_root") as create, \
             mock.patch.object(provenance, "persist_canonical_json") as persist, \
             mock.patch.object(provenance, "read_existing_root") as read:
            for value in invalid:
                with self.subTest(value=value), self.assertRaises(subject.E2ContractError):
                    subject.frozen_e2_input(
                        output_root=value,
                        source_checkpoint=SOURCE_CHECKPOINT,
                        source_tree=SOURCE_TREE,
                    )
        create.assert_not_called()
        persist.assert_not_called()
        read.assert_not_called()

    def test_exact_input_allows_only_the_validated_root_to_change(self):
        other_root = _fresh_root_path()
        other = subject.frozen_e2_input(
            output_root=other_root,
            source_checkpoint=ALTERNATE_SOURCE_CHECKPOINT,
            source_tree=ALTERNATE_SOURCE_TREE,
        )
        subject._validate_exact_input(other)
        self.assertEqual(other.output_root, other_root)
        self.assertEqual(other.source_checkpoint, ALTERNATE_SOURCE_CHECKPOINT)
        self.assertEqual(other.source_tree, ALTERNATE_SOURCE_TREE)
        with self.assertRaisesRegex(subject.E2ContractError, "frozen_input_drift"):
            subject._validate_exact_input(replace(other, policy_status="pending"))

    def test_source_pair_validation_is_strict_pure_and_run_specific(self):
        class StringSubclass(str):
            pass

        invalid = (
            None,
            b"1" * 40,
            Path("1" * 40),
            StringSubclass("1" * 40),
            "",
            "1" * 39,
            "1" * 41,
            "A" * 40,
            "g" * 40,
            "1" * 39 + "-",
        )
        with mock.patch.object(provenance, "create_exclusive_root") as create, \
             mock.patch.object(provenance, "persist_canonical_json") as persist, \
             mock.patch.object(provenance, "read_existing_root") as read, \
             mock.patch.object(Path, "read_text") as read_text, \
             mock.patch.object(Path, "read_bytes") as read_bytes, \
             mock.patch.object(os, "getenv") as getenv, \
             mock.patch("subprocess.run") as run:
            for field in ("source_checkpoint", "source_tree"):
                for value in invalid:
                    kwargs = {
                        "output_root": self.output_root,
                        "source_checkpoint": SOURCE_CHECKPOINT,
                        "source_tree": SOURCE_TREE,
                    }
                    kwargs[field] = value
                    with self.subTest(field=field, value=value), self.assertRaises(subject.E2ContractError):
                        subject.frozen_e2_input(**kwargs)
            accepted = subject.frozen_e2_input(
                output_root=self.output_root,
                source_checkpoint=ALTERNATE_SOURCE_CHECKPOINT,
                source_tree=ALTERNATE_SOURCE_TREE,
            )
        self.assertEqual(accepted.source_checkpoint, ALTERNATE_SOURCE_CHECKPOINT)
        self.assertEqual(accepted.source_tree, ALTERNATE_SOURCE_TREE)
        for call in (create, persist, read, read_text, read_bytes, getenv, run):
            call.assert_not_called()

    def test_output_root_validator_ast_is_lexical_only(self):
        tree = ast.parse(Path(subject.__file__).read_text(encoding="utf-8"))
        functions = {
            node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
        }
        for name in ("_validate_output_root", "_validate_source_identity"):
            calls = {
                node.func.attr
                for node in ast.walk(functions[name])
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            }
            self.assertTrue(calls.isdisjoint({
                "exists", "getenv", "is_dir", "is_file", "iterdir", "lstat", "open",
                "read_bytes", "read_text", "resolve", "run", "stat", "touch", "mkdir",
                "glob", "rglob",
            }))
        source = Path(subject.__file__).read_text(encoding="utf-8")
        self.assertNotIn("4995f7d65141ce8a4086d74f9add21c5b44d593d", source)
        self.assertNotIn("da458ce4a81344397354a8535e8a38cef5d59375", source)

    def test_exact_frozen_input_and_existing_owners_pass_once(self):
        result = self.evaluate()
        self.assertEqual(result["schema"], subject.RESULT_SCHEMA)
        self.assertEqual(result["status"], subject.PASS_STATUS)
        self.assertTrue(all(result["guards"].values()))
        self.assertEqual(
            result["authority"],
            {
                "execution_authorized": False,
                "human_authorization": False,
                "formal_pass": False,
                "hardware_ready": False,
                "release_consumed": False,
                "g4_06_unlocked": False,
                "release_consumption": 0,
                "device_access": 0,
                "formal_r6_access": 0,
                "td_c_access": 0,
                "capture_count": 0,
            },
        )
        self.assertIsInstance(result, MappingProxyType)
        self.assertIsInstance(result["reference_ledger"], MappingProxyType)
        self.assertIsInstance(result["formal_plan"]["capture_ids"], tuple)
        with self.assertRaises(TypeError):
            result["status"] = "forged"

    def test_reference_artifact_drift_is_rejected(self):
        for field in ("g4_01", "g4_02", "g4_03"):
            original = getattr(self.inputs, field)
            first = original.artifacts[0]
            mutations = (
                replace(first, name=first.name + ".forged"),
                replace(first, byte_count=first.byte_count + 1),
                replace(first, sha256="0" * 64),
            )
            for changed in mutations:
                artifacts = (changed,) + original.artifacts[1:]
                with self.subTest(field=field, changed=changed), self.assertRaises(subject.E2ContractError):
                    self.evaluate(inputs=replace(self.inputs, **{field: replace(original, artifacts=artifacts)}))
            if len(original.artifacts) > 1:
                with self.subTest(field=field, case="order"), self.assertRaises(subject.E2ContractError):
                    self.evaluate(inputs=replace(self.inputs, **{field: replace(original, artifacts=tuple(reversed(original.artifacts)))}))
                with self.subTest(field=field, case="count"), self.assertRaises(subject.E2ContractError):
                    self.evaluate(inputs=replace(self.inputs, **{field: replace(original, artifacts=original.artifacts[:-1])}))
                with self.subTest(field=field, case="duplicate"), self.assertRaises(subject.E2ContractError):
                    self.evaluate(inputs=replace(self.inputs, **{field: replace(original, artifacts=original.artifacts + (first,))}))

    def test_source_and_checkpoint_drift_is_rejected(self):
        cases = {
            "guide": replace(self.inputs.guide, byte_count=self.inputs.guide.byte_count + 1),
            "policy": replace(self.inputs.policy, sha256="0" * 64),
            "policy_status": "pending",
            "g4_01_source_head": "0" * 40,
            "g4_01_source_tree": "0" * 40,
            "g4_03_review_plan": replace(self.inputs.g4_03_review_plan, path="forged.md"),
            "protected_sources": tuple(reversed(self.inputs.protected_sources)),
            "retained_r3_status": "VALIDATED",
        }
        for field, value in cases.items():
            with self.subTest(field=field), self.assertRaises(subject.E2ContractError):
                self.evaluate(inputs=replace(self.inputs, **{field: value}))

    def test_transport_and_authority_drift_is_rejected(self):
        cases = {
            "g4_03_classification": "SUCCESS",
            "g4_03_request_transport_success": True,
            "g4_03_request_transport_exit": 0,
            "g4_03_request_error_code": 0,
            "g4_03_final_residual": 1,
            "g4_01_canonical_validator_success": False,
            "g4_01_eligibility": False,
            "g4_01_release_consumable": False,
            "g4_01_release_consumption_authorized": True,
            "release_consumption_authorized": True,
            "device_authorized": True,
            "formal_r6_authorized": True,
            "td_c_authorized": True,
        }
        for field, value in cases.items():
            with self.subTest(field=field), self.assertRaises(subject.E2ContractError):
                self.evaluate(inputs=replace(self.inputs, **{field: value}))

    def test_strict_types_and_closed_shapes_are_rejected(self):
        cases = (
            replace(self.inputs, g4_03_request_transport_exit=False),
            replace(self.inputs, device_authorized=0),
            replace(self.inputs, protected_sources=list(self.inputs.protected_sources)),
            replace(self.inputs, output_root="relative/root"),
            replace(self.inputs, guide=replace(self.inputs.guide, path="../GUIDE.md")),
            replace(self.inputs, g4_01=replace(self.inputs.g4_01, artifacts=list(self.inputs.g4_01.artifacts))),
        )
        for value in cases:
            with self.subTest(value=value), self.assertRaises(subject.E2ContractError):
                self.evaluate(inputs=value)


class OwnerContractTests(E2TestCase):
    def test_formal_plan_exact_fields_are_closed(self):
        base = thermal.build_td_b_r6_formal_plan()
        mutations = []
        for key, value in {
            "status": "ready",
            "executable": True,
            "experiment_id": "forged",
            "source": "strip",
            "strip": "nonzero",
            "ambient": 1,
            "formal_logical": 15,
            "formal_physical_cap": 17,
            "setup_in_formal_root": 1,
            "launch": 2,
            "retry": 1,
            "c_policy_status": "pending",
            "old_new_frame_combination": "allowed",
        }.items():
            changed = copy.deepcopy(base)
            changed[key] = value
            mutations.append((key, changed))
        for label, mutator in (
            ("capture_order", lambda value: value["capture_ids"].reverse()),
            ("capture_id", lambda value: value["capture_ids"].__setitem__(0, "forged")),
            ("shutter", lambda value: value["state_shutters"].__setitem__("C", "1/2000")),
            ("failure", lambda value: value["failure_contract"].__setitem__("retry", 1)),
        ):
            changed = copy.deepcopy(base)
            mutator(changed)
            mutations.append((label, changed))
        open_plan = copy.deepcopy(base)
        open_plan["extra"] = True
        mutations.append(("open", open_plan))
        for label, value in mutations:
            with self.subTest(label=label), self.assertRaises((subject.E2ContractError, ValueError, TypeError)):
                self.evaluate(plan=value)

    def test_machine_status_envelope_and_locks_are_closed(self):
        base = self.native_result()
        mutations = []
        paths = (
            ("operating_envelope", "dwell_s", 601),
            ("operating_envelope", "claim", "steady"),
            ("operating_envelope", "steady_status", "demonstrated"),
            ("locks", "strip", "unlocked"),
            ("locks", "td_c", "unlocked"),
            ("locks", "sentinel", False),
            ("locks", "p8", False),
            ("ray_r6", "formal_planned", 15),
            ("ray_r6", "formal_accepted", 1),
            ("ray_r6", "retry", 1),
            ("ray_r6", "return_anchor_history", "pass"),
        )
        for section, key, value in paths:
            changed = copy.deepcopy(base)
            changed["machine_status"][section][key] = value
            mutations.append((f"{section}.{key}", changed))
        changed = copy.deepcopy(base)
        changed["machine_status"]["extra"] = {}
        mutations.append(("open", changed))
        for label, value in mutations:
            with self.subTest(label=label):
                self.assert_result_rejected(value)

    def test_e2_has_no_local_full_formal_or_machine_literal_contract(self):
        source = Path(subject.__file__).read_text(encoding="utf-8")
        self.assertNotIn("P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6", source)
        self.assertNotIn("000-ray-a0-t600", source)
        self.assertNotIn("selected_fixed_time_transient_not_proven_steady", source)
        self.assertNotIn("def _validate_formal_plan", source)
        self.assertNotIn("def _validate_machine_status", source)
        self.assertIn("thermal.build_td_b_r6_formal_plan", source)
        self.assertIn("thermal.validate_td_b_r6_formal_plan", source)
        self.assertIn("thermal.td_b_r6_machine_status", source)

    def test_non_executable_plan_is_rejected_before_backend_or_output(self):
        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def __init__(self):
                self.connect_calls = 0

            def connect(self):
                self.connect_calls += 1
                raise AssertionError("must not connect")

            def resolve_capture_settings(self, **_kwargs):
                raise AssertionError("must not resolve")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("must not capture")

        backend = FakeBackend()
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as tempdir:
            output = Path(tempdir) / "must-not-exist"
            with self.assertRaises((PermissionError, ValueError, KeyError)):
                measure.run_authorized_plan(
                    thermal.build_td_b_r6_formal_plan(),
                    output_dir=output,
                    run_name="run",
                    camera_backend=backend,
                )
            self.assertFalse(output.exists())
        self.assertEqual(backend.connect_calls, 0)


class PackageTests(E2TestCase):
    def _package_values(self, owned, index=0):
        root = owned.paths[index]
        inputs = subject.frozen_e2_input(
            output_root=root,
            source_checkpoint=SOURCE_CHECKPOINT,
            source_tree=SOURCE_TREE,
        )
        result = subject.evaluate_e2_preformal_gate(inputs)
        return root, inputs, result

    def test_exact_two_artifact_package_modes_canonicality_and_replay(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            with mock.patch.object(
                subject, "replay_e2_package", wraps=subject.replay_e2_package,
            ) as canonical_replay:
                package = subject.persist_e2_package(
                    inputs, result, create_root_fn=owned.create,
                )
            canonical_replay.assert_called_once_with(
                root,
                source_checkpoint=SOURCE_CHECKPOINT,
                source_tree=SOURCE_TREE,
            )
            self.assertEqual(package.root.path, root)
            self.assertEqual(package.root.mode, 0o700)
            self.assertEqual(provenance.list_exact_regular_children(package.root), subject.ARTIFACT_NAMES)
            self.assertEqual(package.result.mode, 0o600)
            self.assertEqual(package.terminal.mode, 0o600)
            self.assertEqual(
                package.result.data,
                provenance.canonical_json_bytes(provenance.decode_canonical_json(package.result.data)),
            )
            terminal = provenance.decode_canonical_json(package.terminal.data)
            self.assertFalse(terminal["terminal_self_reference"])
            self.assertEqual(terminal["artifact_count_before_terminal"], 1)
            self.assertEqual(package.replay["status"], "pass")
            self.assertFalse(package.replay["execution_authorized"])

    def test_result_persist_failure_writes_fail_seal_once(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            calls = 0

            def persist(bound_root, name, value):
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("injected result failure")
                return provenance.persist_canonical_json(bound_root, name, value)

            with self.assertRaisesRegex(subject.E2ContractError, "result_persist_failed"):
                subject.persist_e2_package(
                    inputs, result, create_root_fn=owned.create, persist_fn=persist,
                )
            self.assertEqual(calls, 2)
            bound = provenance.read_existing_root(root)
            self.assertEqual(provenance.list_exact_regular_children(bound), (subject.TERMINAL_NAME,))
            seal = provenance.decode_canonical_json(
                provenance.read_exact_file(Path(root) / subject.TERMINAL_NAME, root=bound).data
            )
            self.assertEqual(seal["failure_code"], "result_persist_failed")

    def test_terminal_persist_failure_writes_fail_seal_once(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            calls = 0

            def persist(bound_root, name, value):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected terminal failure")
                return provenance.persist_canonical_json(bound_root, name, value)

            with self.assertRaisesRegex(subject.E2ContractError, "terminal_persist_failed"):
                subject.persist_e2_package(
                    inputs, result, create_root_fn=owned.create, persist_fn=persist,
                )
            self.assertEqual(calls, 3)
            bound = provenance.read_existing_root(root)
            self.assertEqual(provenance.list_exact_regular_children(bound), subject.ARTIFACT_NAMES)
            seal = provenance.decode_canonical_json(
                provenance.read_exact_file(Path(root) / subject.TERMINAL_NAME, root=bound).data
            )
            self.assertEqual(seal["failure_code"], "terminal_persist_failed")

    def test_replay_rejects_inventory_drift(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            package = subject.persist_e2_package(
                inputs, result, create_root_fn=owned.create,
            )
            extra = provenance.persist_canonical_json(package.root, "extra.json", {"extra": True})
            self.assertEqual(extra.mode, 0o600)
            with self.assertRaisesRegex(subject.E2ContractError, "package_inventory_drift"):
                subject.replay_e2_package(
                    root,
                    source_checkpoint=SOURCE_CHECKPOINT,
                    source_tree=SOURCE_TREE,
                )

    def _persist_handcrafted_package(self, owned, result, terminal_mutator=None, index=0):
        root_path = owned.paths[index]
        root = owned.create(root_path)
        result_identity = provenance.persist_canonical_json(root, subject.RESULT_NAME, result)
        terminal = subject._success_terminal(result_identity)
        if terminal_mutator is not None:
            terminal_mutator(terminal)
        provenance.persist_canonical_json(root, subject.TERMINAL_NAME, terminal)
        return root_path

    def test_shared_closed_result_semantics_cover_evaluate_persist_and_replay(self):
        result = self.native_result()
        result["extra"] = True
        self.assert_result_rejected(result)

        create_calls = 0

        def create(_path):
            nonlocal create_calls
            create_calls += 1
            raise AssertionError("root creation must not be reached")

        with self.assertRaises(subject.E2ContractError):
            subject.persist_e2_package(self.inputs, result, create_root_fn=create)
        self.assertEqual(create_calls, 0)

        with OwnedE2Roots() as owned:
            root, inputs, _result = self._package_values(owned)
            result = provenance.json_native_value(
                subject.evaluate_e2_preformal_gate(inputs)
            )
            result["extra"] = True
            root = self._persist_handcrafted_package(owned, result)
            with self.assertRaises(subject.E2ContractError):
                subject.replay_e2_package(
                    root,
                    source_checkpoint=SOURCE_CHECKPOINT,
                    source_tree=SOURCE_TREE,
                )

    def test_result_root_mismatch_is_rejected_before_io(self):
        other_inputs = subject.frozen_e2_input(
            output_root=_fresh_root_path(),
            source_checkpoint=SOURCE_CHECKPOINT,
            source_tree=SOURCE_TREE,
        )
        other_result = subject.evaluate_e2_preformal_gate(other_inputs)
        calls = {"create": 0, "persist": 0}

        def create(_path):
            calls["create"] += 1
            raise AssertionError("create must not run")

        def persist(_root, _name, _value):
            calls["persist"] += 1
            raise AssertionError("persist must not run")

        with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
            subject.persist_e2_package(
                self.inputs,
                other_result,
                create_root_fn=create,
                persist_fn=persist,
            )
        self.assertEqual(calls, {"create": 0, "persist": 0})

    def test_result_source_pair_mismatch_is_rejected_before_io(self):
        other_inputs = subject.frozen_e2_input(
            output_root=self.output_root,
            source_checkpoint=ALTERNATE_SOURCE_CHECKPOINT,
            source_tree=ALTERNATE_SOURCE_TREE,
        )
        other_result = subject.evaluate_e2_preformal_gate(other_inputs)
        calls = {"create": 0, "persist": 0}

        def create(_path):
            calls["create"] += 1
            raise AssertionError("create must not run")

        def persist(_root, _name, _value):
            calls["persist"] += 1
            raise AssertionError("persist must not run")

        with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
            subject.persist_e2_package(
                self.inputs,
                other_result,
                create_root_fn=create,
                persist_fn=persist,
            )
        self.assertEqual(calls, {"create": 0, "persist": 0})

    def test_create_seam_wrong_root_is_rejected_before_result_persist(self):
        with OwnedE2Roots(2) as owned:
            _expected_root, inputs, result = self._package_values(owned, 0)
            persist_calls = 0

            def create_wrong(_path):
                return owned.create(owned.paths[1])

            def persist(_root, _name, _value):
                nonlocal persist_calls
                persist_calls += 1
                raise AssertionError("persist must not run")

            with self.assertRaisesRegex(subject.E2ContractError, "created_root_identity_mismatch"):
                subject.persist_e2_package(
                    inputs,
                    result,
                    create_root_fn=create_wrong,
                    persist_fn=persist,
                )
            self.assertEqual(persist_calls, 0)

    def test_cross_root_transplant_is_rejected(self):
        with OwnedE2Roots(2) as owned:
            root_a, inputs_a, result_a = self._package_values(owned, 0)
            package_a = subject.persist_e2_package(
                inputs_a, result_a, create_root_fn=owned.create,
            )
            root_b = owned.create(owned.paths[1])
            copied_result = provenance.persist_canonical_json(
                root_b,
                subject.RESULT_NAME,
                provenance.decode_canonical_json(package_a.result.data),
            )
            provenance.persist_canonical_json(
                root_b,
                subject.TERMINAL_NAME,
                subject._success_terminal(copied_result),
            )
            self.assertEqual(root_a, package_a.root.path)
            with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
                subject.replay_e2_package(
                    root_b.path,
                    source_checkpoint=SOURCE_CHECKPOINT,
                    source_tree=SOURCE_TREE,
                )

    def test_replay_uses_trusted_source_pair_not_artifact_self_report(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            root = self._persist_handcrafted_package(
                owned,
                provenance.json_native_value(result),
            )
            with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
                subject.replay_e2_package(
                    root,
                    source_checkpoint=ALTERNATE_SOURCE_CHECKPOINT,
                    source_tree=ALTERNATE_SOURCE_TREE,
                )
            replay = subject.replay_e2_package(
                root,
                source_checkpoint=inputs.source_checkpoint,
                source_tree=inputs.source_tree,
            )
            self.assertEqual(replay["status"], "pass")

    def test_result_top_level_guards_and_authority_are_closed_and_strict(self):
        base = self.native_result()
        cases = []
        for key in tuple(base):
            changed = copy.deepcopy(base)
            del changed[key]
            cases.append((f"top_missing_{key}", changed))
        changed = copy.deepcopy(base)
        changed["extra"] = False
        cases.append(("top_extra", changed))

        changed = copy.deepcopy(base)
        changed["guards"] = {}
        cases.append(("guards_empty", changed))
        first_guard = next(iter(base["guards"]))
        for label, mutate in (
            ("guards_missing", lambda value: value["guards"].pop(first_guard)),
            ("guards_extra", lambda value: value["guards"].__setitem__("extra", True)),
            ("guards_false", lambda value: value["guards"].__setitem__(first_guard, False)),
            ("guards_truthy_int", lambda value: value["guards"].__setitem__(first_guard, 1)),
        ):
            changed = copy.deepcopy(base)
            mutate(changed)
            cases.append((label, changed))

        for key, expected in base["authority"].items():
            changed = copy.deepcopy(base)
            del changed["authority"][key]
            cases.append((f"authority_missing_{key}", changed))
            changed = copy.deepcopy(base)
            changed["authority"][key] = 0 if expected is False else False
            cases.append((f"authority_type_{key}", changed))
            changed = copy.deepcopy(base)
            changed["authority"][key] = True if expected is False else 1
            cases.append((f"authority_value_{key}", changed))
        changed = copy.deepcopy(base)
        changed["authority"]["extra"] = 0
        cases.append(("authority_extra", changed))

        for label, value in cases:
            with self.subTest(label=label):
                self.assert_result_rejected(value)

    def test_reference_ledger_tampering_is_closed(self):
        base = self.native_result()
        cases = []
        for section in ("output_root", "source_checkpoint", "source_tree", "guide", "policy", "g4_01", "g4_02", "g4_03", "protected_sources"):
            changed = copy.deepcopy(base)
            if isinstance(changed["reference_ledger"][section], str):
                changed["reference_ledger"][section] = "0" * 40
            elif isinstance(changed["reference_ledger"][section], list):
                changed["reference_ledger"][section].reverse()
            else:
                changed["reference_ledger"][section]["extra"] = True
            cases.append((section, changed))
        for section in ("g4_01", "g4_02", "g4_03"):
            for mutation in ("name", "bytes", "sha256", "order", "count"):
                changed = copy.deepcopy(base)
                artifacts = changed["reference_ledger"][section]["artifacts"]
                if mutation == "order" and len(artifacts) < 2:
                    continue
                if mutation == "name":
                    artifacts[0]["name"] += ".forged"
                elif mutation == "bytes":
                    artifacts[0]["bytes"] += 1
                elif mutation == "sha256":
                    artifacts[0]["sha256"] = "0" * 64
                elif mutation == "order":
                    artifacts.reverse()
                else:
                    artifacts.pop()
                cases.append((f"{section}_{mutation}", changed))
        for key, value in {
            "classification": "SUCCESS",
            "request_transport_success": True,
            "request_transport_exit": 0,
            "request_error_code": 0,
            "final_residual": 1,
        }.items():
            changed = copy.deepcopy(base)
            changed["reference_ledger"]["g4_03"][key] = value
            cases.append((f"g4_03_{key}", changed))
        for label, value in cases:
            with self.subTest(label=label):
                self.assert_result_rejected(value)

        for key in ("output_root", "source_checkpoint", "source_tree"):
            missing = copy.deepcopy(base)
            del missing["reference_ledger"][key]
            with self.subTest(missing=key):
                self.assert_result_rejected(missing)
        extra = copy.deepcopy(base)
        extra["reference_ledger"]["extra_root"] = self.output_root
        self.assert_result_rejected(extra)

    def test_formal_and_machine_result_tampering_use_existing_owners(self):
        base = self.native_result()
        formal_cases = []
        for label, mutate in (
            ("missing", lambda value: value["formal_plan"].pop("schema")),
            ("extra", lambda value: value["formal_plan"].__setitem__("extra", True)),
            ("field", lambda value: value["formal_plan"].__setitem__("source", "strip")),
            ("order", lambda value: value["formal_plan"]["capture_ids"].reverse()),
            ("shutter", lambda value: value["formal_plan"]["state_shutters"].__setitem__("C", "1/2000")),
            ("budget", lambda value: value["formal_plan"].__setitem__("formal_logical", 17)),
            ("failure", lambda value: value["formal_plan"]["failure_contract"].__setitem__("retry", 1)),
        ):
            changed = copy.deepcopy(base)
            mutate(changed)
            formal_cases.append((f"formal_{label}", changed))
        for section, key, value in (
            ("operating_envelope", "dwell_s", 601),
            ("locks", "strip", "unlocked"),
            ("ray_r6", "formal_accepted", 1),
        ):
            changed = copy.deepcopy(base)
            changed["machine_status"][section][key] = value
            formal_cases.append((f"machine_{section}_{key}", changed))
        changed = copy.deepcopy(base)
        changed["machine_status"]["extra"] = True
        formal_cases.append(("machine_extra", changed))
        for label, value in formal_cases:
            with self.subTest(label=label):
                self.assert_result_rejected(value)

    def test_terminal_shape_authority_and_result_identity_are_closed(self):
        mutators = []
        terminal_keys = (
            "schema", "status", "result", "artifact_count_before_terminal",
            "terminal_self_reference", "retry", "alternate_root", "authority",
        )
        for key in terminal_keys:
            mutators.append((f"missing_{key}", lambda value, key=key: value.pop(key)))
        mutators.append(("extra", lambda value: value.__setitem__("extra", True)))
        for key in ("execution_authorized", "formal_r6_access", "capture_count"):
            mutators.append((f"authority_missing_{key}", lambda value, key=key: value["authority"].pop(key)))
            mutators.append((f"authority_value_{key}", lambda value, key=key: value["authority"].__setitem__(key, 1)))
        mutators.append(("authority_extra", lambda value: value["authority"].__setitem__("extra", 0)))
        for key, forged in (
            ("path", "forged.json"), ("device", 0), ("inode", 0),
            ("mode", 0), ("bytes", 1), ("sha256", "0" * 64),
        ):
            mutators.append((f"identity_{key}", lambda value, key=key, forged=forged: value["result"].__setitem__(key, forged)))
        for label, mutator in mutators:
            with self.subTest(label=label):
                with OwnedE2Roots() as owned:
                    _root, inputs, _result = self._package_values(owned)
                    base = provenance.json_native_value(
                        subject.evaluate_e2_preformal_gate(inputs)
                    )
                    root = self._persist_handcrafted_package(owned, base, mutator)
                    with self.assertRaisesRegex(subject.E2ContractError, "replay_terminal_contract_drift"):
                        subject.replay_e2_package(
                            root,
                            source_checkpoint=SOURCE_CHECKPOINT,
                            source_tree=SOURCE_TREE,
                        )

    def test_synchronized_result_and_terminal_forgery_still_fails_closed(self):
        with OwnedE2Roots() as owned:
            _root, inputs, _result = self._package_values(owned)
            result = provenance.json_native_value(
                subject.evaluate_e2_preformal_gate(inputs)
            )
            result["guards"]["forged_guard"] = True
            root = self._persist_handcrafted_package(owned, result)
            with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
                subject.replay_e2_package(
                    root,
                    source_checkpoint=SOURCE_CHECKPOINT,
                    source_tree=SOURCE_TREE,
                )

    def test_ephemeral_packages_leave_no_test_root_residual(self):
        with OwnedE2Roots() as owned:
            root, inputs, result = self._package_values(owned)
            package = subject.persist_e2_package(
                inputs, result, create_root_fn=owned.create,
            )
            self.assertEqual(package.replay["status"], "pass")
            self.assertIsInstance(package.replay, MappingProxyType)
            self.assertTrue(Path(root).exists())
        self.assertFalse(Path(root).exists())


class CanonicalOwnerBindingTests(E2TestCase):
    def test_public_signatures_and_ast_bind_canonical_owners(self):
        persist = inspect.signature(subject.persist_e2_package)
        replay = inspect.signature(subject.replay_e2_package)
        self.assertEqual(
            tuple(persist.parameters),
            ("inputs", "result", "create_root_fn", "persist_fn"),
        )
        self.assertEqual(persist.parameters["inputs"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(persist.parameters["result"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(persist.parameters["create_root_fn"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(persist.parameters["persist_fn"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(
            tuple(replay.parameters),
            ("root_path", "source_checkpoint", "source_tree"),
        )
        self.assertEqual(replay.parameters["root_path"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for name in ("source_checkpoint", "source_tree"):
            self.assertEqual(replay.parameters[name].kind, inspect.Parameter.KEYWORD_ONLY)
            self.assertIs(replay.parameters[name].default, inspect.Parameter.empty)
            self.assertEqual(replay.parameters[name].annotation, "str")

        tree = ast.parse(Path(subject.__file__).read_text(encoding="utf-8"))
        functions = {
            node.name: node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        persist_node = functions["persist_e2_package"]
        replay_node = functions["replay_e2_package"]
        self.assertIsNone(persist_node.args.kwarg)
        self.assertIsNone(replay_node.args.kwarg)
        persist_calls = [node for node in ast.walk(persist_node) if isinstance(node, ast.Call)]
        replay_calls = [node for node in ast.walk(replay_node) if isinstance(node, ast.Call)]
        direct_replay = [
            node for node in persist_calls
            if isinstance(node.func, ast.Name) and node.func.id == "replay_e2_package"
        ]
        self.assertEqual(len(direct_replay), 1)
        self.assertEqual(len(direct_replay[0].args), 1)
        self.assertEqual(
            tuple(keyword.arg for keyword in direct_replay[0].keywords),
            ("source_checkpoint", "source_tree"),
        )
        self.assertEqual(
            tuple(
                (keyword.value.value.id, keyword.value.attr)
                for keyword in direct_replay[0].keywords
                if isinstance(keyword.value, ast.Attribute)
                and isinstance(keyword.value.value, ast.Name)
            ),
            (("inputs", "source_checkpoint"), ("inputs", "source_tree")),
        )
        for node in persist_calls + replay_calls:
            self.assertTrue({keyword.arg for keyword in node.keywords}.isdisjoint({
                "build_plan_fn", "validate_plan_fn", "machine_status_fn", "replay_fn", "inputs",
            }))
        names = {node.id for node in ast.walk(persist_node) if isinstance(node, ast.Name)}
        self.assertNotIn("replay_fn", names)

    def test_persist_rejects_removed_semantic_keywords_before_io(self):
        result = self.native_result()
        for forbidden in (
            "build_plan_fn", "validate_plan_fn", "machine_status_fn", "replay_fn",
        ):
            calls = {"create": 0, "persist": 0}

            def create(_path):
                calls["create"] += 1
                raise AssertionError("create must not run")

            def persist(_root, _name, _value):
                calls["persist"] += 1
                raise AssertionError("persist must not run")

            kwargs = {
                "create_root_fn": create,
                "persist_fn": persist,
                forbidden: lambda *_args, **_kwargs: None,
            }
            with self.subTest(forbidden=forbidden), self.assertRaises(TypeError):
                subject.persist_e2_package(self.inputs, result, **kwargs)
            self.assertEqual(calls, {"create": 0, "persist": 0})

    def test_replay_rejects_removed_keywords_before_root_read(self):
        for forbidden in (
            "inputs", "build_plan_fn", "validate_plan_fn", "machine_status_fn", "replay_fn",
        ):
            with self.subTest(forbidden=forbidden), mock.patch.object(
                provenance, "read_existing_root",
            ) as read_root, self.assertRaises(TypeError):
                subject.replay_e2_package(
                    "must-not-be-read",
                    source_checkpoint=SOURCE_CHECKPOINT,
                    source_tree=SOURCE_TREE,
                    **{forbidden: lambda *_args, **_kwargs: None},
                )
            read_root.assert_not_called()

    def test_replay_requires_explicit_source_pair_before_root_read(self):
        cases = (
            {},
            {"source_checkpoint": SOURCE_CHECKPOINT},
            {"source_tree": SOURCE_TREE},
        )
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), mock.patch.object(
                provenance, "read_existing_root",
            ) as read_root, self.assertRaises(TypeError):
                subject.replay_e2_package("must-not-be-read", **kwargs)
            read_root.assert_not_called()

    def test_replay_rejects_invalid_trusted_source_pair_before_root_read(self):
        cases = (
            {"source_checkpoint": "A" * 40, "source_tree": SOURCE_TREE},
            {"source_checkpoint": SOURCE_CHECKPOINT, "source_tree": "2" * 39},
            {"source_checkpoint": b"1" * 40, "source_tree": SOURCE_TREE},
        )
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), mock.patch.object(
                provenance, "read_existing_root",
            ) as read_root, self.assertRaises(subject.E2ContractError):
                subject.replay_e2_package("must-not-be-read", **kwargs)
            read_root.assert_not_called()

    def test_self_consistent_forged_owner_result_cannot_reach_io(self):
        forged_plan = thermal.build_td_b_r6_formal_plan()
        forged_plan["experiment_id"] = "forged-owner-experiment"
        forged_status = thermal.td_b_r6_machine_status()
        forged_status["operating_envelope"]["dwell_s"] = 601
        calls = {"build": 0, "validate": 0, "status": 0, "create": 0, "persist": 0}

        def build():
            calls["build"] += 1
            return copy.deepcopy(forged_plan)

        def validate(_value):
            calls["validate"] += 1

        def status():
            calls["status"] += 1
            return copy.deepcopy(forged_status)

        result = subject.evaluate_e2_preformal_gate(
            self.inputs,
            build_plan_fn=build,
            validate_plan_fn=validate,
            machine_status_fn=status,
        )
        self.assertEqual(calls, {"build": 1, "validate": 1, "status": 1, "create": 0, "persist": 0})

        def create(_path):
            calls["create"] += 1
            raise AssertionError("create must not run")

        def persist(_root, _name, _value):
            calls["persist"] += 1
            raise AssertionError("persist must not run")

        with self.assertRaises(subject.E2ContractError):
            subject.persist_e2_package(
                self.inputs,
                result,
                create_root_fn=create,
                persist_fn=persist,
            )
        self.assertEqual(calls["create"], 0)
        self.assertEqual(calls["persist"], 0)


class StaticBoundaryTests(unittest.TestCase):
    def test_e2_fixture_has_only_exact_identity_owned_cleanup(self):
        source = inspect.getsource(OwnedE2Roots)
        self.assertNotIn("TemporaryDirectory", inspect.getsource(PackageTests))
        self.assertNotIn("EXPECTED_OUTPUT_ROOT", Path(subject.__file__).read_text(encoding="utf-8"))
        self.assertNotIn("EXPECTED_OUTPUT_ROOT", inspect.getsource(PackageTests))
        self.assertNotIn("glob", source)
        self.assertNotIn("rmtree", source)
        self.assertNotIn("scandir", source)
        self.assertIn("provenance.read_existing_root", source)
        self.assertIn("provenance.list_exact_regular_children", source)
        self.assertIn("provenance.read_exact_file", source)
        self.assertIn("os.unlink", source)
        self.assertIn("os.rmdir", source)

    def test_owner_has_no_process_network_device_or_environment_boundary(self):
        path = Path(subject.__file__)
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = set()
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.add(node.func.attr)
        self.assertTrue(imports.isdisjoint({"os", "socket", "subprocess", "urllib", "requests"}))
        self.assertTrue(calls.isdisjoint({"system", "popen", "run", "urlopen", "connect", "capture"}))
        source = path.read_text(encoding="utf-8")
        self.assertNotIn("environ", source)
        self.assertNotIn("esphome", source)
        self.assertNotIn("ray120c", source)


if __name__ == "__main__":
    unittest.main()
