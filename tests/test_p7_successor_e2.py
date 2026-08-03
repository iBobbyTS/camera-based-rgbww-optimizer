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


class E2TestCase(unittest.TestCase):
    def setUp(self):
        self.inputs = subject.frozen_e2_input()

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
            "source_checkpoint": "0" * 40,
            "source_tree": "0" * 40,
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
    def _temporary_package(self):
        tempdir = tempfile.TemporaryDirectory(dir=TEMP_PARENT)
        root = str(Path(tempdir.name) / "package")
        patcher = mock.patch.object(subject, "EXPECTED_OUTPUT_ROOT", root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(tempdir.cleanup)
        inputs = subject.frozen_e2_input()
        result = subject.evaluate_e2_preformal_gate(inputs)
        return root, inputs, result

    def test_exact_two_artifact_package_modes_canonicality_and_replay(self):
        root, inputs, result = self._temporary_package()
        with mock.patch.object(
            subject, "replay_e2_package", wraps=subject.replay_e2_package,
        ) as canonical_replay:
            package = subject.persist_e2_package(inputs, result)
        canonical_replay.assert_called_once_with(root)
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
        root, inputs, result = self._temporary_package()
        calls = 0

        def persist(bound_root, name, value):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("injected result failure")
            return provenance.persist_canonical_json(bound_root, name, value)

        with self.assertRaisesRegex(subject.E2ContractError, "result_persist_failed"):
            subject.persist_e2_package(inputs, result, persist_fn=persist)
        self.assertEqual(calls, 2)
        bound = provenance.read_existing_root(root)
        self.assertEqual(provenance.list_exact_regular_children(bound), (subject.TERMINAL_NAME,))
        seal = provenance.decode_canonical_json(
            provenance.read_exact_file(Path(root) / subject.TERMINAL_NAME, root=bound).data
        )
        self.assertEqual(seal["failure_code"], "result_persist_failed")

    def test_terminal_persist_failure_writes_fail_seal_once(self):
        root, inputs, result = self._temporary_package()
        calls = 0

        def persist(bound_root, name, value):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected terminal failure")
            return provenance.persist_canonical_json(bound_root, name, value)

        with self.assertRaisesRegex(subject.E2ContractError, "terminal_persist_failed"):
            subject.persist_e2_package(inputs, result, persist_fn=persist)
        self.assertEqual(calls, 3)
        bound = provenance.read_existing_root(root)
        self.assertEqual(provenance.list_exact_regular_children(bound), subject.ARTIFACT_NAMES)
        seal = provenance.decode_canonical_json(
            provenance.read_exact_file(Path(root) / subject.TERMINAL_NAME, root=bound).data
        )
        self.assertEqual(seal["failure_code"], "terminal_persist_failed")

    def test_replay_rejects_inventory_drift(self):
        root, inputs, result = self._temporary_package()
        package = subject.persist_e2_package(inputs, result)
        extra = provenance.persist_canonical_json(package.root, "extra.json", {"extra": True})
        self.assertEqual(extra.mode, 0o600)
        with self.assertRaisesRegex(subject.E2ContractError, "package_inventory_drift"):
            subject.replay_e2_package(root)

    def _persist_handcrafted_package(self, result, terminal_mutator=None):
        tempdir = tempfile.TemporaryDirectory(dir=TEMP_PARENT)
        self.addCleanup(tempdir.cleanup)
        root_path = str(Path(tempdir.name) / "package")
        root = provenance.create_exclusive_root(root_path)
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

        root = self._persist_handcrafted_package(result)
        with self.assertRaises(subject.E2ContractError):
            subject.replay_e2_package(root)

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
        for section in ("source_checkpoint", "source_tree", "guide", "policy", "g4_01", "g4_02", "g4_03", "protected_sources"):
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
        base = self.native_result()
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
                root = self._persist_handcrafted_package(base, mutator)
                with self.assertRaisesRegex(subject.E2ContractError, "replay_terminal_contract_drift"):
                    subject.replay_e2_package(root)

    def test_synchronized_result_and_terminal_forgery_still_fails_closed(self):
        result = self.native_result()
        result["guards"]["forged_guard"] = True
        root = self._persist_handcrafted_package(result)
        with self.assertRaisesRegex(subject.E2ContractError, "result_contract_drift"):
            subject.replay_e2_package(root)

    def test_ephemeral_packages_leave_no_test_root_residual(self):
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as parent:
            root = str(Path(parent) / "package")
            with mock.patch.object(subject, "EXPECTED_OUTPUT_ROOT", root):
                inputs = subject.frozen_e2_input()
                result = subject.evaluate_e2_preformal_gate(inputs)
                package = subject.persist_e2_package(inputs, result)
                self.assertEqual(package.replay["status"], "pass")
                self.assertIsInstance(package.replay, MappingProxyType)
                self.assertTrue(Path(root).exists())
        self.assertFalse(Path(parent).exists())


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
        self.assertEqual(tuple(replay.parameters), ("root_path",))
        self.assertEqual(replay.parameters["root_path"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)

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
        self.assertEqual(direct_replay[0].keywords, [])
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
                    **{forbidden: lambda *_args, **_kwargs: None},
                )
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
