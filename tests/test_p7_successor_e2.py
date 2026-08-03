import ast
import copy
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
        base = thermal.td_b_r6_machine_status()
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
            changed[section][key] = value
            mutations.append((f"{section}.{key}", changed))
        changed = copy.deepcopy(base)
        changed["extra"] = {}
        mutations.append(("open", changed))
        for label, value in mutations:
            with self.subTest(label=label), self.assertRaises(subject.E2ContractError):
                self.evaluate(status=value)

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
        replay_calls = 0

        def replay(value):
            nonlocal replay_calls
            replay_calls += 1
            return subject.replay_e2_package(value)

        package = subject.persist_e2_package(inputs, result, replay_fn=replay)
        self.assertEqual(replay_calls, 1)
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
