from __future__ import annotations

import ast
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import tempfile
from types import MappingProxyType
import unittest

from camera_based_rgbww_optimizer.optimization import p7_successor_lineage as subject
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


SAFE_TEMP_BASE = Path("/Volumes/4T/temp/rgbww-optimizer")
CHECKPOINT = "a" * 40
TREE = "b" * 40
POLICY_BYTES = b'{\n  "schema": "fixture",\n  "states": {"C": "1/2500"}\n}\n'
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
MANIFEST_BYTES = b'[{"path":"fixture"}]'
MANIFEST_SHA = hashlib.sha256(MANIFEST_BYTES).hexdigest()
REPO_ROOT = Path(__file__).resolve().parents[1]
REAL_POLICY_PATH = REPO_ROOT / "config/hsi/p7-ray-td-b-exposure-policy-v2.json"
REAL_POLICY_SHA = "c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681"


def capture_ids() -> list[str]:
    states = ("a0", "d", "a-after-d", "b", "a-after-b", "c", "a-after-c")
    values: list[str] = []
    index = 0
    for state, count in zip(states, (1, 4, 1, 4, 1, 4, 1)):
        for slot in range(count):
            suffix = "t600" if count == 1 else f"t{(60, 120, 300, 600)[slot]}"
            values.append(f"{index:03d}-ray-{state}-{suffix}")
            index += 1
    return values


def plan_fixture() -> dict:
    return {
        "schema": "p7_td_b_ray_r6_formal_plan_v1",
        "status": "selected_exposure_policy_non_executable",
        "executable": False,
        "experiment_id": "P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6",
        "source": "ray",
        "strip": "zero_throughout",
        "ambient": 0,
        "formal_logical": 16,
        "formal_physical_cap": 16,
        "setup_in_formal_root": 0,
        "launch": 1,
        "retry": 0,
        "capture_ids": capture_ids(),
        "state_shutters": {
            "A": "1/5000", "D": "1/6400", "B": "1/8000", "C": "1/2500",
        },
        "c_policy_status": "qualified",
        "old_new_frame_combination": "prohibited",
        "failure_contract": {
            "classification": "accepted_hard_failed_formal_attempt",
            "formal_pass": False,
            "strip_call_count": 0,
            "retry": 0,
        },
    }


def status_fixture() -> dict:
    return {
        "ray_r6": {"formal_accepted": 0, "retry": 0},
        "locks": {
            "strip": "blocked_until_ray_r6_pass",
            "td_c": "blocked_until_combined_td_b_pass",
            "sentinel": True,
            "p8": True,
        },
    }


def qualification_fixture() -> dict:
    return {
        "status": "qualified_1_2500",
        "selected_shutter": "1/2500",
        "candidate_launch_count": 1,
        "candidate_2_call_count": 0,
        "attempted_capture_calls": 4,
        "physical_returned_cr3_count": 4,
        "accepted_capture_count": 4,
        "retry": 0,
        "manifest": {"payload_bytes": len(MANIFEST_BYTES), "sha256": MANIFEST_SHA},
    }


def source_identity(**changes) -> provenance.SourceIdentity:
    value = provenance.SourceIdentity(
        provenance.RepositoryIdentity("/repo", 1, 2, 0o755),
        CHECKPOINT, CHECKPOINT, TREE, False, False, False, True,
    )
    return replace(value, **changes)


def file_identity(path: str, data: bytes = POLICY_BYTES) -> provenance.FileIdentity:
    return provenance.FileIdentity(
        path, data, len(data), hashlib.sha256(data).hexdigest(), 1, 2, 0o600, None,
    )


def native(value):
    return provenance.json_native_value(value)


class SuccessorInputTests(unittest.TestCase):
    def build(self, **overrides):
        calls: list[str] = []
        policy_path = "/repo/config/policy.json"
        functions = {
            "source_identity_fn": lambda repo, sha: calls.append(f"git:{repo}:{sha}") or source_identity(),
            "read_exact_file_fn": lambda path, **kwargs: calls.append("read-policy") or file_identity(str(path)),
            "decode_policy_fn": lambda data: calls.append("decode-policy") or provenance.decode_strict_json_bytes(data),
            "validate_policy_fn": lambda value: calls.append("validate-policy") if value["schema"] == "fixture" else (_ for _ in ()).throw(ValueError("schema")),
            "audit_eq_fn": lambda root: calls.append(f"eq:{root}") or qualification_fixture(),
            "build_r6_plan_fn": lambda policy: calls.append("plan") or plan_fixture(),
            "machine_status_fn": lambda: calls.append("status") or status_fixture(),
        }
        arguments = {
            "repo_root": "/repo",
            "source_checkpoint": CHECKPOINT,
            "policy_path": policy_path,
            "policy_sha256": POLICY_SHA,
            "eq_root": "/evidence/eq-r6",
            "eq_manifest_bytes": MANIFEST_BYTES,
            "eq_manifest_sha256": MANIFEST_SHA,
            **functions,
        }
        arguments.update(overrides)
        return subject.build_successor_lineage_inputs(**arguments), calls

    def test_build_consumes_owner_identities_and_same_pretty_policy_bytes(self):
        inputs, calls = self.build()
        self.assertEqual(calls, [
            f"git:/repo:{CHECKPOINT}", "read-policy", "decode-policy", "validate-policy",
            "eq:/evidence/eq-r6", "plan", "status",
        ])
        self.assertEqual(inputs.frozen_inputs["source"]["tree"], TREE)
        self.assertEqual(inputs.frozen_inputs["policy"]["sha256"], POLICY_SHA)
        self.assertEqual(inputs.frozen_inputs["policy_contract"]["schema"], "fixture")
        with self.assertRaisesRegex(provenance.ProvenanceIOError, "json_not_canonical"):
            provenance.decode_canonical_json(POLICY_BYTES)

    def test_real_repository_policy_passes_production_default_consumers(self):
        self.assertTrue(REAL_POLICY_PATH.is_absolute())
        policy_bytes = REAL_POLICY_PATH.read_bytes()
        self.assertEqual(len(policy_bytes), 4065)
        self.assertEqual(hashlib.sha256(policy_bytes).hexdigest(), REAL_POLICY_SHA)

        inputs = subject.build_successor_lineage_inputs(
            repo_root="/repo",
            source_checkpoint=CHECKPOINT,
            policy_path=REAL_POLICY_PATH,
            policy_sha256=REAL_POLICY_SHA,
            eq_root="/evidence/eq-r6",
            eq_manifest_bytes=MANIFEST_BYTES,
            eq_manifest_sha256=MANIFEST_SHA,
            source_identity_fn=lambda *_args: source_identity(),
            audit_eq_fn=lambda _root: qualification_fixture(),
            machine_status_fn=status_fixture,
        )

        self.assertEqual(inputs.frozen_inputs["policy"]["path"], str(REAL_POLICY_PATH))
        self.assertEqual(inputs.frozen_inputs["policy"]["bytes"], 4065)
        self.assertEqual(inputs.frozen_inputs["policy"]["sha256"], REAL_POLICY_SHA)
        self.assertEqual(inputs.r6_formal_plan["state_shutters"]["C"], "1/2500")
        self.assertEqual(len(inputs.r6_formal_plan["capture_ids"]), 16)
        self.assertEqual(inputs.r6_formal_plan["formal_logical"], 16)
        self.assertEqual(inputs.r6_formal_plan["formal_physical_cap"], 16)
        self.assertFalse(inputs.r6_formal_plan["executable"])

    def test_policy_projection_is_single_same_object_and_preserves_immutability(self):
        decoded_policy = MappingProxyType({
            "schema": "fixture",
            "states": MappingProxyType({
                "C": MappingProxyType({"formal_shutter": "1/2500"}),
            }),
            "sequence": ("A", "D", "B", "C"),
        })
        before = provenance.json_native_value(decoded_policy)
        seen: list[dict] = []

        def validate_policy(value):
            self.assertIs(type(value), dict)
            self.assertIs(type(value["states"]), dict)
            self.assertIs(type(value["sequence"]), list)
            seen.append(value)

        def build_plan(value):
            seen.append(value)
            return plan_fixture()

        inputs, _calls = self.build(
            decode_policy_fn=lambda _data: decoded_policy,
            validate_policy_fn=validate_policy,
            build_r6_plan_fn=build_plan,
        )

        self.assertEqual(len(seen), 2)
        self.assertIs(seen[0], seen[1])
        self.assertEqual(seen[0], before)
        self.assertIs(type(decoded_policy), MappingProxyType)
        self.assertIs(type(decoded_policy["states"]), MappingProxyType)
        self.assertIs(type(decoded_policy["sequence"]), tuple)
        self.assertEqual(provenance.json_native_value(decoded_policy), before)
        frozen = inputs.frozen_inputs["policy_contract"]
        self.assertIs(type(frozen), MappingProxyType)
        self.assertIs(type(frozen["states"]), MappingProxyType)
        self.assertIs(type(frozen["sequence"]), tuple)
        self.assertEqual(provenance.json_native_value(frozen), before)
        with self.assertRaises(TypeError):
            frozen["schema"] = "changed"
        with self.assertRaises(TypeError):
            frozen["states"]["C"] = {}

        tree = ast.parse(Path(subject.__file__).read_text(encoding="utf-8"))
        build_node = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "build_successor_lineage_inputs"
        )
        projections = [
            node for node in ast.walk(build_node)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "provenance"
            and node.func.attr == "json_native_value"
        ]
        self.assertEqual(len(projections), 1)

    def test_source_policy_semantic_and_eq_drift_fail_closed(self):
        for dirty in (
            {"staged": True, "clean": False},
            {"unstaged": True, "clean": False},
            {"untracked": True, "clean": False},
            {"head": "c" * 40, "clean": False},
        ):
            with self.subTest(dirty=dirty), self.assertRaisesRegex(subject.SuccessorLineageError, "source_identity_not_clean"):
                self.build(source_identity_fn=lambda *_args, value=dirty: source_identity(**value))
        with self.assertRaisesRegex(subject.SuccessorLineageError, "policy_identity_invalid"):
            self.build(read_exact_file_fn=lambda *_args, **_kwargs: file_identity("/repo/config/policy.json", b"{}\n"))
        with self.assertRaises(ValueError):
            self.build(validate_policy_fn=lambda value: (_ for _ in ()).throw(ValueError("semantic mismatch")))
        with self.assertRaisesRegex(subject.SuccessorLineageError, "eq_manifest_hash_drift"):
            self.build(eq_manifest_bytes=b"drift")

    def test_old_routes_and_r6_drift_are_rejected(self):
        for marker in ("REF-P7-25-R2-old", "retained-r3", "setup-lineage-release", "external-controller"):
            with self.subTest(marker=marker), self.assertRaisesRegex(subject.SuccessorLineageError, "historical_input_prohibited"):
                self.build(eq_root=f"/evidence/{marker}")
        bad = plan_fixture()
        bad["state_shutters"]["C"] = "1/3200"
        with self.assertRaisesRegex(subject.SuccessorLineageError, "r6_plan_drift"):
            self.build(build_r6_plan_fn=lambda _policy: bad)


class SuccessorBundleTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SAFE_TEMP_BASE.is_dir())
        self.temporary = tempfile.TemporaryDirectory(prefix="g4-successor-test-", dir=SAFE_TEMP_BASE)
        self.parent = Path(self.temporary.name)
        self.parent.chmod(0o700)
        self.parent_identity = provenance.read_existing_root(self.parent)
        self.inputs = SuccessorInputTests().build()[0]

    def tearDown(self):
        self.temporary.cleanup()

    def compose(self, name="release", **kwargs):
        counts = {"public": 0, "final": 0, "strict": 0}

        def count(kind):
            counts[kind] += 1

        bundle = subject.compose_successor_lineage_bundle(
            self.inputs, safe_parent=self.parent_identity, child_name=name,
            call_counter=count, **kwargs,
        )
        return bundle, counts

    def load_values(self, bundle):
        return [native(provenance.decode_canonical_json(item.data)) for item in bundle.artifacts]

    def write_bundle(self, name, values):
        root = provenance.create_exclusive_direct_child(self.parent_identity, name)
        return root, tuple(
            provenance.persist_canonical_json(root, artifact_name, value)
            for artifact_name, value in zip(subject.ARTIFACT_NAMES, values)
        )

    def write_reference_consistent_bundle(self, name, values):
        root = provenance.create_exclusive_direct_child(self.parent_identity, name)
        frozen = provenance.persist_canonical_json(
            root, subject.ARTIFACT_NAMES[0], values[0]
        )
        plan = provenance.persist_canonical_json(
            root, subject.ARTIFACT_NAMES[1], values[1]
        )
        descriptor_value = json.loads(json.dumps(values[2]))
        descriptor_value["preterminal_references"] = [
            subject._reference(frozen), subject._reference(plan)
        ]
        descriptor = provenance.persist_canonical_json(
            root, subject.ARTIFACT_NAMES[2], descriptor_value
        )
        summary_value = json.loads(json.dumps(values[3]))
        summary_value["descriptor"] = subject._reference(descriptor)
        summary = provenance.persist_canonical_json(
            root, subject.ARTIFACT_NAMES[3], summary_value
        )
        terminal_value = json.loads(json.dumps(values[4]))
        terminal_value["references"] = [
            subject._reference(identity)
            for identity in (frozen, plan, descriptor, summary)
        ]
        terminal = provenance.persist_canonical_json(
            root, subject.ARTIFACT_NAMES[4], terminal_value
        )
        return root, (frozen, plan, descriptor, summary, terminal)

    def assert_both_reject(self, root, identities, code):
        for validator in (subject.replay_successor_lineage_bundle, subject.strict_validate_successor_lineage_bundle):
            with self.subTest(validator=validator.__name__), self.assertRaisesRegex(subject.SuccessorLineageError, code):
                validator(root.path, identities)

    def test_exact_state_machine_terminal_last_and_each_validator_once(self):
        order: list[str] = []

        def persist(root, name, value):
            order.append(name)
            return provenance.persist_canonical_json(root, name, value)

        reads = {"final": 0, "strict": 0}

        def final(root, identities, **kwargs):
            def read(*args, **read_kwargs):
                reads["final"] += 1
                return provenance.read_exact_file(*args, **read_kwargs)
            return subject.replay_successor_lineage_bundle(root, identities, read_file_fn=read, **kwargs)

        def strict(root, identities, **kwargs):
            def read(*args, **read_kwargs):
                reads["strict"] += 1
                return provenance.read_exact_file(*args, **read_kwargs)
            return subject.strict_validate_successor_lineage_bundle(root, identities, read_file_fn=read, **kwargs)

        bundle, counts = self.compose(persist_fn=persist, replay_fn=final, strict_validator_fn=strict)
        self.assertEqual(order, list(subject.ARTIFACT_NAMES))
        self.assertEqual(counts, {"public": 1, "final": 1, "strict": 1})
        self.assertEqual(reads, {"final": 5, "strict": 5})
        values = self.load_values(bundle)
        self.assertEqual(values[2]["status"], "candidate_non_authorizing")
        self.assertEqual(values[3]["status"], "public_descriptor_semantic_pass")
        self.assertEqual(values[4]["status"], "sealed_non_authorizing_pending_independent_replay")
        self.assertNotIn("final_validation_pass", json.dumps(values))
        self.assertNotIn("strict_validation_pass", json.dumps(values))
        self.assertEqual(bundle.final_replay["status"], "pass")
        self.assertEqual(bundle.strict_validation["status"], "pass")

    def test_closed_schema_rejects_extra_claim_in_each_artifact(self):
        bundle, _ = self.compose()
        originals = self.load_values(bundle)
        for index, artifact_name in enumerate(subject.ARTIFACT_NAMES):
            values = json.loads(json.dumps(originals))
            values[index]["product_ready"] = True
            root, identities = self.write_bundle(f"extra-{index}", values)
            self.assert_both_reject(root, identities, "open_schema|prohibited_downstream_claim")

    def test_cross_artifact_references_and_terminal_non_circularity_are_exact(self):
        bundle, _ = self.compose()
        originals = self.load_values(bundle)
        mutations = []
        values = json.loads(json.dumps(originals))
        values[2]["preterminal_references"][0]["sha256"] = "0" * 64
        mutations.append(values)
        values = json.loads(json.dumps(originals))
        values[3]["descriptor"]["bytes"] += 1
        mutations.append(values)
        values = json.loads(json.dumps(originals))
        values[4]["references"][2]["path"] = subject.ARTIFACT_NAMES[4]
        mutations.append(values)
        values = json.loads(json.dumps(originals))
        values[2]["artifact_order"] = list(reversed(subject.ARTIFACT_NAMES))
        mutations.append(values)
        for index, values in enumerate(mutations):
            root, identities = self.write_bundle(f"cross-{index}", values)
            self.assert_both_reject(root, identities, "reference_drift|artifact_order_drift|terminal_reference_drift")

    def test_unsynchronized_frozen_tamper_reports_exact_reference_drift(self):
        bundle, _ = self.compose()
        originals = self.load_values(bundle)
        validators = (
            subject.replay_successor_lineage_bundle,
            subject.strict_validate_successor_lineage_bundle,
        )
        for index, validator in enumerate(validators):
            values = json.loads(json.dumps(originals))
            values[0]["policy_contract"]["benign_test_marker"] = "changed"
            root, identities = self.write_bundle(f"integrity-{index}", values)
            with self.subTest(validator=validator.__name__), self.assertRaises(
                subject.SuccessorLineageError
            ) as raised:
                validator(root.path, identities)
            self.assertEqual(raised.exception.code, "descriptor_reference_drift")

    def test_reference_consistent_semantic_guards_are_exactly_reachable(self):
        bundle, _ = self.compose()
        originals = self.load_values(bundle)
        validators = (
            subject.replay_successor_lineage_bundle,
            subject.strict_validate_successor_lineage_bundle,
        )
        cases = (
            ({"api_token": "x"}, "secret_material_prohibited"),
            ({"route": "REF-P7-25-R2-old"}, "historical_input_prohibited"),
        )
        for case_index, (value, expected_code) in enumerate(cases):
            for validator_index, validator in enumerate(validators):
                values = json.loads(json.dumps(originals))
                values[0]["policy_contract"]["unexpected"] = value
                root, identities = self.write_reference_consistent_bundle(
                    f"semantic-{case_index}-{validator_index}", values
                )
                with self.subTest(
                    validator=validator.__name__, expected_code=expected_code
                ), self.assertRaises(subject.SuccessorLineageError) as raised:
                    validator(root.path, identities)
                self.assertEqual(raised.exception.code, expected_code)

    def test_preterminal_failure_writes_truthful_failure_seal(self):
        def fail_public(*_args, **_kwargs):
            raise ValueError("public failed")

        with self.assertRaises(subject.SuccessorLineageError) as raised:
            self.compose(public_validator_fn=fail_public)
        self.assertEqual(raised.exception.code, "preterminal_failure_sealed")
        root = provenance.read_existing_root(self.parent / "release")
        names = provenance.list_exact_regular_children(root)
        self.assertEqual(names, tuple(sorted(subject.ARTIFACT_NAMES[:3] + (subject.ARTIFACT_NAMES[4],))))
        seal = provenance.decode_canonical_json(
            provenance.read_exact_file(self.parent / "release" / subject.ARTIFACT_NAMES[4], root=root).data
        )
        self.assertEqual(seal["status"], "failed_before_terminal")
        self.assertEqual(len(seal["references"]), 3)
        self.assertEqual(seal["primary_failure"]["type"], "ValueError")
        self.assertFalse(seal["release_consumable"])

    def test_failure_seal_failure_reports_both_causes(self):
        terminal_calls = 0

        def persist(root, name, value):
            nonlocal terminal_calls
            if name == subject.ARTIFACT_NAMES[4]:
                terminal_calls += 1
                raise OSError("seal blocked")
            return provenance.persist_canonical_json(root, name, value)

        def fail_public(*_args, **_kwargs):
            raise ValueError("public failed")

        with self.assertRaises(subject.SuccessorLineageError) as raised:
            self.compose(persist_fn=persist, public_validator_fn=fail_public)
        self.assertEqual(raised.exception.code, "preterminal_failure_and_seal_failure")
        self.assertIsInstance(raised.exception.primary, ValueError)
        self.assertIsInstance(raised.exception.seal_failure, OSError)
        self.assertEqual(terminal_calls, 1)

    def test_postterminal_failure_preserves_pending_seal_and_runs_both(self):
        seen = {"final": 0, "strict": 0}

        def fail_final(*_args, **_kwargs):
            seen["final"] += 1
            raise ValueError("final failed")

        def pass_strict(root, identities, **kwargs):
            seen["strict"] += 1
            return subject.strict_validate_successor_lineage_bundle(root, identities, **kwargs)

        with self.assertRaises(subject.SuccessorLineageError) as raised:
            self.compose(replay_fn=fail_final, strict_validator_fn=pass_strict)
        self.assertEqual(raised.exception.code, "independent_replay_failed_pending_seal_preserved")
        self.assertEqual(seen, {"final": 1, "strict": 1})
        root = provenance.read_existing_root(self.parent / "release")
        seal = provenance.decode_canonical_json(
            provenance.read_exact_file(self.parent / "release" / subject.ARTIFACT_NAMES[4], root=root).data
        )
        self.assertEqual(seal["status"], "sealed_non_authorizing_pending_independent_replay")
        self.assertEqual(provenance.list_exact_regular_children(root), tuple(sorted(subject.ARTIFACT_NAMES)))

    def test_safe_parent_contract_rejects_escape_preexisting_and_symlink(self):
        for child in ("../escape", "a/b", "/absolute", "..", "."):
            with self.subTest(child=child), self.assertRaisesRegex(provenance.ProvenanceIOError, "unsafe_child"):
                subject.compose_successor_lineage_bundle(
                    self.inputs, safe_parent=self.parent_identity, child_name=child,
                )
        (self.parent / "existing").mkdir()
        with self.assertRaisesRegex(provenance.ProvenanceIOError, "root_exists"):
            subject.compose_successor_lineage_bundle(
                self.inputs, safe_parent=self.parent_identity, child_name="existing",
            )
        target = self.parent / "target"
        target.mkdir()
        (self.parent / "link").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(provenance.ProvenanceIOError, "root_exists"):
            subject.compose_successor_lineage_bundle(
                self.inputs, safe_parent=self.parent_identity, child_name="link",
            )

    def test_module_has_no_device_or_process_owner(self):
        source = Path(subject.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        }
        joined = "\n".join(sorted(imports))
        for token in ("subprocess", "socket", "requests", "ray120c", "esphome"):
            self.assertNotIn(token, joined)
        self.assertNotIn("json.loads", source)
        self.assertNotIn("create_exclusive_root", source)


if __name__ == "__main__":
    unittest.main()
