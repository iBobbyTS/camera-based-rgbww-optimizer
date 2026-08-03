from __future__ import annotations

import ast
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from camera_based_rgbww_optimizer.optimization import p7_successor_lineage as successor
from camera_based_rgbww_optimizer.optimization import p7_successor_predevice as subject
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


SAFE_TEMP_BASE = Path("/Volumes/4T/temp/rgbww-optimizer")
REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO_ROOT / "config/hsi/p7-ray-td-b-exposure-policy-v2.json"
SOURCE_HEAD = "a" * 40
SOURCE_TREE = "b" * 40
EQ_BYTES = 7980
EQ_MANIFEST_BYTES = b"x" * EQ_BYTES
EQ_SHA256 = hashlib.sha256(EQ_MANIFEST_BYTES).hexdigest()


def _source_identity() -> provenance.SourceIdentity:
    return provenance.SourceIdentity(
        provenance.RepositoryIdentity("/synthetic/repository", 1, 2, 0o755),
        SOURCE_HEAD,
        SOURCE_HEAD,
        SOURCE_TREE,
        False,
        False,
        False,
        True,
    )


def _qualification() -> dict:
    return {
        "status": "qualified_1_2500",
        "selected_shutter": "1/2500",
        "candidate_launch_count": 1,
        "candidate_2_call_count": 0,
        "attempted_capture_calls": 4,
        "physical_returned_cr3_count": 4,
        "accepted_capture_count": 4,
        "retry": 0,
        "manifest": {"payload_bytes": EQ_BYTES, "sha256": EQ_SHA256},
    }


def _native(value):
    return provenance.json_native_value(value)


class SuccessorPredeviceTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SAFE_TEMP_BASE.is_dir())
        self.temporary = tempfile.TemporaryDirectory(
            prefix="g4-predevice-test-", dir=SAFE_TEMP_BASE
        )
        self.parent = Path(self.temporary.name)
        self.parent.chmod(0o700)
        self.parent_identity = provenance.read_existing_root(self.parent)
        policy_bytes = POLICY_PATH.read_bytes()
        self.policy_sha256 = hashlib.sha256(policy_bytes).hexdigest()
        inputs = successor.build_successor_lineage_inputs(
            repo_root="/synthetic/repository",
            source_checkpoint=SOURCE_HEAD,
            policy_path=POLICY_PATH,
            policy_sha256=self.policy_sha256,
            eq_root="/synthetic/eq-r6",
            eq_manifest_bytes=EQ_MANIFEST_BYTES,
            eq_manifest_sha256=EQ_SHA256,
            source_identity_fn=lambda *_args: _source_identity(),
            audit_eq_fn=lambda _root: _qualification(),
        )
        self.bundle = successor.compose_successor_lineage_bundle(
            inputs, safe_parent=self.parent_identity, child_name="release"
        )
        self.expectation = self._expectation(self.bundle)

    def tearDown(self):
        self.temporary.cleanup()

    def _expectation(self, bundle) -> subject.PredeviceExpectation:
        return subject.PredeviceExpectation(
            bundle_path=bundle.root.path,
            bundle_device=bundle.root.device,
            bundle_inode=bundle.root.inode,
            bundle_mode=bundle.root.mode,
            artifacts=tuple(
                subject.ArtifactExpectation(
                    Path(identity.path).name,
                    identity.byte_count,
                    identity.sha256,
                )
                for identity in bundle.artifacts
            ),
            source_repository_path="/synthetic/repository",
            source_head=SOURCE_HEAD,
            source_tree=SOURCE_TREE,
            policy_path=str(POLICY_PATH),
            policy_byte_count=POLICY_PATH.stat().st_size,
            policy_sha256=self.policy_sha256,
            eq_root="/synthetic/eq-r6",
            eq_manifest_bytes=EQ_BYTES,
            eq_manifest_sha256=EQ_SHA256,
        )

    def _values(self, bundle=None):
        selected = bundle or self.bundle
        return [
            _native(provenance.decode_canonical_json(identity.data))
            for identity in selected.artifacts
        ]

    def _reference_consistent_bundle(self, name, mutate):
        values = json.loads(json.dumps(self._values()))
        mutate(values)
        root = provenance.create_exclusive_direct_child(self.parent_identity, name)
        frozen = provenance.persist_canonical_json(root, successor.ARTIFACT_NAMES[0], values[0])
        plan = provenance.persist_canonical_json(root, successor.ARTIFACT_NAMES[1], values[1])
        descriptor_value = values[2]
        descriptor_value["source"] = values[0]["source"]
        descriptor_value["policy"] = values[0]["policy"]
        descriptor_value["eq"] = {
            key: values[0]["eq"][key]
            for key in ("root", "manifest_bytes", "manifest_sha256")
        }
        descriptor_value["r6_plan"] = values[1]
        descriptor_value["preterminal_references"] = [
            successor._reference(frozen), successor._reference(plan)
        ]
        descriptor = provenance.persist_canonical_json(
            root, successor.ARTIFACT_NAMES[2], descriptor_value
        )
        summary_value = values[3]
        summary_value["descriptor"] = successor._reference(descriptor)
        summary = provenance.persist_canonical_json(
            root, successor.ARTIFACT_NAMES[3], summary_value
        )
        terminal_value = values[4]
        terminal_value["references"] = [
            successor._reference(identity)
            for identity in (frozen, plan, descriptor, summary)
        ]
        terminal = provenance.persist_canonical_json(
            root, successor.ARTIFACT_NAMES[4], terminal_value
        )
        artifacts = (frozen, plan, descriptor, summary, terminal)
        bundle = successor.SuccessorLineageBundle(root, artifacts, {}, {}, {})
        return bundle, self._expectation(bundle)

    def _assert_rejected_mutation(self, name, mutate):
        _bundle, expectation = self._reference_consistent_bundle(name, mutate)
        with self.assertRaises((subject.SuccessorPredeviceError, successor.SuccessorLineageError, ValueError)):
            subject.evaluate_successor_predevice(expectation)

    def test_positive_delegates_each_validator_once_and_keeps_authority_false(self):
        calls = {"public": 0, "final": 0, "strict": 0, "policy": 0, "plan": 0, "machine": 0}

        def public(*args, **kwargs):
            calls["public"] += 1
            return successor.validate_successor_lineage_release(*args, **kwargs)

        def final(*args, **kwargs):
            calls["final"] += 1
            return successor.replay_successor_lineage_bundle(*args, **kwargs)

        def strict(*args, **kwargs):
            calls["strict"] += 1
            return successor.strict_validate_successor_lineage_bundle(*args, **kwargs)

        def policy(value):
            calls["policy"] += 1
            thermal.validate_td_b_exposure_policy_v2(value)

        def plan(value):
            calls["plan"] += 1
            thermal.validate_td_b_r6_formal_plan(value)

        def machine():
            calls["machine"] += 1
            return thermal.td_b_r6_machine_status()

        result = subject.evaluate_successor_predevice(
            self.expectation,
            public_validator_fn=public,
            replay_fn=final,
            strict_validator_fn=strict,
            validate_policy_fn=policy,
            validate_r6_plan_fn=plan,
            machine_status_fn=machine,
        )

        self.assertEqual(calls, {key: 1 for key in calls})
        self.assertEqual(result["schema"], "g4_successor_predevice_oracle_v1")
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["validations"], {
            "public": "public_descriptor_semantic_pass",
            "final_replay": "pass",
            "strict": "pass",
            "lineage": "pass",
            "call_counts": {"public": 1, "final": 1, "strict": 1},
        })
        self.assertEqual(result["release"]["artifact_count"], 5)
        self.assertEqual(result["r6"]["formal_logical"], 16)
        self.assertEqual(result["r6"]["formal_physical_cap"], 16)
        self.assertEqual(result["operational"], {
            "dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "steady_status": "not_demonstrated",
        })
        self.assertEqual(result["proposed_current_route_state"], {
            "canonical_validator_success": True,
            "eligibility": True,
            "release_consumable": True,
            "release_consumption_authorized": False,
            "scope": "exact_g4_01_release_only_waiting_planner_and_orchestrator",
        })
        effective = result["effective_authority"]
        self.assertEqual(effective["retained_r3_status"], "RETAINED_UNVALIDATED_UNCONSUMED")
        self.assertTrue(all(value is False for key, value in effective.items() if key != "retained_r3_status"))

    def test_module_is_a_small_owner_composition_without_parallel_io_or_validator(self):
        source = Path(subject.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            node.module or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        } | {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        self.assertFalse({"json", "hashlib", "os", "subprocess", "socket"}.intersection(imports))
        for owner_call in (
            "provenance.create_exclusive_root",
            "provenance.persist_canonical_json",
            "provenance.read_existing_root",
            "provenance.list_exact_regular_children",
            "provenance.read_exact_file",
            "provenance.decode_canonical_json",
            "provenance.require_same_target",
            "successor.validate_successor_lineage_release",
            "successor.replay_successor_lineage_bundle",
            "successor.strict_validate_successor_lineage_bundle",
            "thermal.validate_td_b_exposure_policy_v2",
            "thermal.validate_td_b_r6_formal_plan",
            "thermal.td_b_r6_machine_status",
        ):
            self.assertIn(owner_call, source)
        for forbidden in (".write_bytes(", ".write_text(", ".mkdir(", "open(", "__main__"):
            self.assertNotIn(forbidden, source)
        replay_node = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "replay_successor_predevice_evidence"
        )
        replay_names = {
            node.id for node in ast.walk(replay_node) if isinstance(node, ast.Name)
        }
        self.assertNotIn("evaluate_successor_predevice", replay_names)

    def test_durable_success_persists_exact_two_and_replays_once(self):
        calls = {"evaluate": 0, "root": 0, "result": 0, "terminal": 0, "replay": 0}
        output = self.parent / "oracle-success"

        def evaluate(value):
            calls["evaluate"] += 1
            return subject.evaluate_successor_predevice(value)

        def create(path):
            calls["root"] += 1
            return provenance.create_exclusive_root(path)

        def persist(root, name, value):
            calls["result" if name == subject.EVIDENCE_ARTIFACT_NAMES[0] else "terminal"] += 1
            return provenance.persist_canonical_json(root, name, value)

        package = subject.persist_successor_predevice_evidence(
            self.expectation,
            output_root=output,
            evaluate_fn=evaluate,
            create_root_fn=create,
            persist_fn=persist,
        )

        def read_root(path):
            calls["replay"] += 1
            return provenance.read_existing_root(path)

        replay = subject.replay_successor_predevice_evidence(package, read_root_fn=read_root)
        self.assertEqual(calls, {
            "evaluate": 1, "root": 1, "result": 1, "terminal": 1, "replay": 1,
        })
        self.assertEqual(package.root.mode, 0o700)
        self.assertEqual(tuple(item.mode for item in (package.result, package.terminal)), (0o600, 0o600))
        self.assertEqual(
            provenance.list_exact_regular_children(package.root),
            tuple(sorted(subject.EVIDENCE_ARTIFACT_NAMES)),
        )
        result = _native(provenance.decode_canonical_json(package.result.data))
        seal = _native(provenance.decode_canonical_json(package.terminal.data))
        self.assertEqual(result["proposed_current_route_state"]["eligibility"], True)
        self.assertTrue(all(
            value is False
            for key, value in result["effective_authority"].items()
            if key != "retained_r3_status"
        ))
        self.assertEqual(seal["schema"], "g4_successor_predevice_terminal_seal_v1")
        self.assertEqual(seal["status"], "sealed_pass_non_authorizing_waiting_planner_review")
        self.assertEqual(seal["result"]["path"], subject.EVIDENCE_ARTIFACT_NAMES[0])
        self.assertNotEqual(seal["result"]["path"], subject.EVIDENCE_ARTIFACT_NAMES[1])
        self.assertEqual(replay["schema"], "g4_successor_predevice_evidence_replay_v1")
        self.assertEqual(replay["status"], "pass")
        self.assertEqual(replay["artifact_count"], 2)
        self.assertEqual(replay["independent_replay_calls"], 1)
        self.assertEqual(replay["release_consumption"], 0)

    def test_evaluator_failure_is_before_root_and_preexisting_root_is_not_repaired(self):
        output = self.parent / "oracle-zero"
        calls = {"evaluate": 0, "root": 0}

        def fail(_value):
            calls["evaluate"] += 1
            raise RuntimeError("evaluate-failed")

        def create(path):
            calls["root"] += 1
            return provenance.create_exclusive_root(path)

        with self.assertRaisesRegex(RuntimeError, "evaluate-failed"):
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=output,
                evaluate_fn=fail, create_root_fn=create,
            )
        self.assertEqual(calls, {"evaluate": 1, "root": 0})
        self.assertFalse(os.path.lexists(output))

        existing = self.parent / "oracle-existing"
        existing.mkdir(mode=0o700)
        with self.assertRaisesRegex(provenance.ProvenanceIOError, "root_exists"):
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=existing,
            )
        self.assertEqual(tuple(existing.iterdir()), ())

    def test_post_root_result_failure_attempts_one_failure_seal_and_preserves_root(self):
        output = self.parent / "oracle-result-failure"
        calls = 0

        def persist(root, name, value):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise RuntimeError("result-persist-failed")
            return provenance.persist_canonical_json(root, name, value)

        with self.assertRaises(subject.SuccessorPredeviceError) as raised:
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=output, persist_fn=persist,
            )
        self.assertEqual(raised.exception.code, "durable_package_failed")
        self.assertIsInstance(raised.exception.primary, RuntimeError)
        self.assertEqual(calls, 2)
        root = provenance.read_existing_root(output)
        self.assertEqual(provenance.list_exact_regular_children(root), ("terminal-seal.json",))
        terminal = provenance.read_exact_file(output / "terminal-seal.json", expected_mode=0o600, root=root)
        seal = _native(provenance.decode_canonical_json(terminal.data))
        self.assertEqual(seal["status"], "sealed_fail_non_authorizing")
        self.assertEqual(seal["failed_phase"], "persist_result")
        self.assertEqual(seal["primary_code"], "RuntimeError")
        self.assertIsNone(seal["result"])

    def test_terminal_failure_seal_preserves_result_and_double_failure_is_visible(self):
        output = self.parent / "oracle-terminal-failure"
        calls = 0

        def persist(root, name, value):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("terminal-persist-failed")
            return provenance.persist_canonical_json(root, name, value)

        with self.assertRaises(subject.SuccessorPredeviceError) as raised:
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=output, persist_fn=persist,
            )
        self.assertEqual(raised.exception.code, "durable_package_failed")
        self.assertEqual(calls, 3)
        root = provenance.read_existing_root(output)
        self.assertEqual(provenance.list_exact_regular_children(root), tuple(sorted(subject.EVIDENCE_ARTIFACT_NAMES)))
        terminal = provenance.read_exact_file(output / "terminal-seal.json", expected_mode=0o600, root=root)
        seal = _native(provenance.decode_canonical_json(terminal.data))
        self.assertEqual(seal["status"], "sealed_fail_non_authorizing")
        self.assertEqual(seal["failed_phase"], "persist_terminal")
        self.assertEqual(seal["result"]["path"], subject.EVIDENCE_ARTIFACT_NAMES[0])

        double = self.parent / "oracle-double-failure"
        double_calls = 0

        def fail_both(_root, _name, _value):
            nonlocal double_calls
            double_calls += 1
            raise RuntimeError(f"persist-{double_calls}")

        with self.assertRaises(subject.SuccessorPredeviceError) as double_raised:
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=double, persist_fn=fail_both,
            )
        self.assertEqual(double_raised.exception.code, "durable_package_and_failure_seal_failed")
        self.assertEqual(double_calls, 2)
        self.assertIsInstance(double_raised.exception.primary, RuntimeError)
        self.assertIsInstance(double_raised.exception.seal_failure, RuntimeError)
        self.assertEqual(provenance.list_exact_regular_children(provenance.read_existing_root(double)), ())

    def test_root_identity_drift_fail_closed_after_creation(self):
        output = self.parent / "oracle-root-drift"

        def drift_root(path):
            root = provenance.create_exclusive_root(path)
            return replace(root, inode=root.inode + 1)

        with self.assertRaises(subject.SuccessorPredeviceError) as raised:
            subject.persist_successor_predevice_evidence(
                self.expectation, output_root=output, create_root_fn=drift_root,
            )
        self.assertEqual(raised.exception.code, "durable_package_and_failure_seal_failed")
        self.assertTrue(os.path.isdir(output))

    def test_replay_inventory_hash_canonical_root_and_target_drift_fail_closed(self):
        for index, case in enumerate(("inventory", "hash", "canonical", "root", "target")):
            output = self.parent / f"oracle-replay-{index}"
            package = subject.persist_successor_predevice_evidence(
                self.expectation, output_root=output,
            )
            kwargs = {}
            replay_package = package
            if case == "inventory":
                provenance.persist_canonical_json(package.root, "extra.json", {"extra": True})
            elif case == "hash":
                Path(package.result.path).write_bytes(b"{}\n")
            elif case == "canonical":
                path = Path(package.result.path)
                path.write_bytes(b'{ "schema": "not-canonical" }\n')
                current = provenance.read_exact_file(path, expected_mode=0o600, root=package.root)
                replay_package = replace(package, result=current)
            elif case == "root":
                kwargs["read_root_fn"] = lambda path: replace(
                    provenance.read_existing_root(path), inode=package.root.inode + 1
                )
            else:
                def read(path, **read_kwargs):
                    identity = provenance.read_exact_file(path, **read_kwargs)
                    if Path(path).name == subject.EVIDENCE_ARTIFACT_NAMES[0]:
                        return replace(identity, inode=identity.inode + 1)
                    return identity
                kwargs["read_file_fn"] = read
            with self.subTest(case=case), self.assertRaises(
                (subject.SuccessorPredeviceError, provenance.ProvenanceIOError)
            ):
                subject.replay_successor_predevice_evidence(replay_package, **kwargs)

    def test_historical_markers_are_rejected(self):
        markers = ("REF-P7-25-R2-old", "retained-r3", "retained_r3_root")
        for index, marker in enumerate(markers):
            with self.subTest(marker=marker):
                self._assert_rejected_mutation(
                    f"marker-{index}",
                    lambda values, value=marker: values[0]["policy_contract"].update({"marker": value}),
                )

    def test_source_head_checkpoint_and_tree_drift_are_rejected(self):
        for index, key in enumerate(("head", "checkpoint", "tree")):
            with self.subTest(key=key):
                self._assert_rejected_mutation(
                    f"source-{index}",
                    lambda values, field=key: values[0]["source"].__setitem__(field, "d" * 40),
                )

    def test_policy_and_eq_reference_drift_are_rejected(self):
        changes = (
            replace(self.expectation, policy_path="/synthetic/wrong-policy.json"),
            replace(self.expectation, policy_byte_count=self.expectation.policy_byte_count + 1),
            replace(self.expectation, policy_sha256="d" * 64),
            replace(self.expectation, eq_root="/synthetic/wrong-eq"),
            replace(self.expectation, eq_manifest_bytes=EQ_BYTES + 1),
            replace(self.expectation, eq_manifest_sha256="d" * 64),
        )
        for value in changes:
            with self.subTest(value=value), self.assertRaises(subject.SuccessorPredeviceError):
                subject.evaluate_successor_predevice(value)

    def test_auto_exposure_and_weak_reacquire_are_rejected(self):
        for index, field in enumerate(("auto_exposure", "weak_reacquire")):
            with self.subTest(field=field):
                self._assert_rejected_mutation(
                    f"automatic-{index}",
                    lambda values, key=field: values[1].__setitem__(key, True),
                )

    def test_capture_id_swap_missing_duplicate_and_resume_are_rejected(self):
        def swap(values):
            values[1]["capture_ids"][0], values[1]["capture_ids"][1] = (
                values[1]["capture_ids"][1], values[1]["capture_ids"][0]
            )

        mutations = (
            swap,
            lambda values: values[1]["capture_ids"].pop(),
            lambda values: values[1]["capture_ids"].__setitem__(1, values[1]["capture_ids"][0]),
            lambda values: values[1]["capture_ids"].__setitem__(0, "001-ray-d-t60-resume"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self._assert_rejected_mutation(f"capture-{index}", mutation)

    def test_pooling_origin_old_frame_and_cross_root_semantics_are_rejected(self):
        mutations = (
            lambda values: values[1].__setitem__("old_new_frame_combination", "allowed"),
            lambda values: values[1]["failure_contract"].__setitem__("origin", "old_frame"),
            lambda values: values[1]["failure_contract"].__setitem__("run_root", "cross-root"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self._assert_rejected_mutation(f"pool-{index}", mutation)

    def test_operational_and_lock_drift_are_rejected(self):
        cases = (
            ("dwell", lambda value: value["operating_envelope"].__setitem__("dwell_s", 601)),
            ("claim", lambda value: value["operating_envelope"].__setitem__("claim", "steady")),
            ("steady", lambda value: value["operating_envelope"].__setitem__("steady_status", "proven")),
            ("strip", lambda value: value["locks"].__setitem__("strip", "unlocked")),
            ("td_c", lambda value: value["locks"].__setitem__("td_c", "unlocked")),
            ("sentinel", lambda value: value["locks"].__setitem__("sentinel", False)),
        )
        for name, mutate in cases:
            machine = thermal.td_b_r6_machine_status()
            mutate(machine)
            with self.subTest(name=name), self.assertRaises(subject.SuccessorPredeviceError):
                subject.evaluate_successor_predevice(
                    self.expectation, machine_status_fn=lambda value=machine: value
                )

    def test_existing_io_owners_reject_inventory_and_artifact_drift(self):
        cases = ("extra", "missing", "symlink", "mode", "size", "hash", "canonical")
        for index, case in enumerate(cases):
            bundle = successor.compose_successor_lineage_bundle(
                successor.build_successor_lineage_inputs(
                    repo_root="/synthetic/repository",
                    source_checkpoint=SOURCE_HEAD,
                    policy_path=POLICY_PATH,
                    policy_sha256=self.policy_sha256,
                    eq_root="/synthetic/eq-r6",
                    eq_manifest_bytes=EQ_MANIFEST_BYTES,
                    eq_manifest_sha256=EQ_SHA256,
                    source_identity_fn=lambda *_args: _source_identity(),
                    audit_eq_fn=lambda _root: _qualification(),
                ),
                safe_parent=self.parent_identity,
                child_name=f"io-{index}",
            )
            expectation = self._expectation(bundle)
            first = Path(bundle.artifacts[0].path)
            if case == "extra":
                extra = first.parent / "extra.json"
                extra.write_bytes(b"{}\n")
                extra.chmod(0o600)
            elif case == "missing":
                first.unlink()
            elif case == "symlink":
                target = first.parent / "target.json"
                first.rename(target)
                first.symlink_to(target)
            elif case == "mode":
                first.chmod(0o644)
            elif case == "size":
                expectation = replace(
                    expectation,
                    artifacts=(replace(expectation.artifacts[0], byte_count=expectation.artifacts[0].byte_count + 1),)
                    + expectation.artifacts[1:],
                )
            elif case == "hash":
                expectation = replace(
                    expectation,
                    artifacts=(replace(expectation.artifacts[0], sha256="d" * 64),)
                    + expectation.artifacts[1:],
                )
            else:
                first.write_bytes(b'{ "not": "canonical" }\n')
                expectation = replace(
                    expectation,
                    artifacts=(subject.ArtifactExpectation(
                        expectation.artifacts[0].name,
                        first.stat().st_size,
                        hashlib.sha256(first.read_bytes()).hexdigest(),
                    ),) + expectation.artifacts[1:],
                )
            with self.subTest(case=case), self.assertRaises((subject.SuccessorPredeviceError, provenance.ProvenanceIOError)):
                subject.evaluate_successor_predevice(expectation)

    def test_same_target_identity_drift_is_rejected_by_provenance_owner(self):
        calls = 0

        def read(path, **kwargs):
            nonlocal calls
            calls += 1
            identity = provenance.read_exact_file(path, **kwargs)
            if calls == 2:
                return replace(identity, inode=identity.inode + 1)
            return identity

        with self.assertRaises(provenance.ProvenanceIOError):
            subject.evaluate_successor_predevice(self.expectation, read_file_fn=read)

    def test_validator_failure_is_immediate_without_fallback_or_second_call(self):
        for failed in ("public", "final", "strict"):
            calls = {"public": 0, "final": 0, "strict": 0}

            def invoke(kind, owner, *args, **kwargs):
                calls[kind] += 1
                if kind == failed:
                    raise RuntimeError(f"{kind}-failed")
                return owner(*args, **kwargs)

            with self.subTest(failed=failed), self.assertRaisesRegex(RuntimeError, f"{failed}-failed"):
                subject.evaluate_successor_predevice(
                    self.expectation,
                    public_validator_fn=lambda *args, **kwargs: invoke(
                        "public", successor.validate_successor_lineage_release, *args, **kwargs
                    ),
                    replay_fn=lambda *args, **kwargs: invoke(
                        "final", successor.replay_successor_lineage_bundle, *args, **kwargs
                    ),
                    strict_validator_fn=lambda *args, **kwargs: invoke(
                        "strict", successor.strict_validate_successor_lineage_bundle, *args, **kwargs
                    ),
                )
            self.assertEqual(calls[failed], 1)
            if failed == "public":
                self.assertEqual(calls, {"public": 1, "final": 0, "strict": 0})
            elif failed == "final":
                self.assertEqual(calls, {"public": 1, "final": 1, "strict": 0})
            else:
                self.assertEqual(calls, {"public": 1, "final": 1, "strict": 1})


if __name__ == "__main__":
    unittest.main()
