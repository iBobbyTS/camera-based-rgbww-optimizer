from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_td_b_r6_stage_gate as subject
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


ACTIVATION_HEAD = "860b27359ab54a1c8c4b4a4737331e169e53cb38"
ACTIVATION_TREE = "c4c9f0129beba2f13b663f9d392abab986e37484"
LIVE_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/"
    "g4-ray-r6-stage-gate-70fec61ef830-20260804T012240Z"
)
FUTURE_RUN_NAME = "p7-td-b-formal-r6-111111111111-20260804T010000Z"


class FakeCapableBackend:
    backend_name = "remote"
    v2_capture_capability = measure.REMOTE_V2_CAPABILITY

    def __init__(self) -> None:
        self.connect = mock.Mock(name="connect")
        self.resolve_capture_settings = mock.Mock(name="resolve_capture_settings")
        self.capture_with_timing = mock.Mock(name="capture_with_timing")


def machine_row(name: str, value: dict[str, object]) -> bytes:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return f"`{name}={payload}`\n".encode()


class SyntheticRepository:
    def __init__(self, root: Path, output_root: Path) -> None:
        self.root = root
        self.output_root = output_root
        self.source_checkpoint = ACTIVATION_HEAD
        self.source_tree = ACTIVATION_TREE
        for path in subject.EXPECTED_SOURCE_PATHS:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f"fixture:{path}\n".encode())
        plan = {
            "active_task_count": 1,
            "active_task": subject.TASK_ID,
            "reference_task_id": subject.TASK_ID,
            "contract_id": subject.CONTRACT_ID,
            "stage_gate_root": str(output_root),
        }
        prerequisite = {
            "disposition": "ACCEPTED_SYNTHETIC_PREREQUISITE",
            "release_consumed": False,
            "device_or_formal_credit": False,
        }
        full = {
            "active_task_count": 1,
            "active_task": subject.TASK_ID,
            "active_plan_contract_id": subject.CONTRACT_ID,
            "canonical_next_reference_task": subject.TASK_ID,
            "retained_r3_status": subject.RETAINED_R3_STATUS,
            "release_consumption_authorized": False,
            "formal_r6_authorized": False,
            "td_c_authorized": False,
            "frozen_guide_input": {
                "stage": "EQ-R6_STATE_C",
                "selected_exposure": "1/2500",
                "status": "ACCEPTED_QUALIFIED_INPUT_NOT_A_CURRENT_TASK",
            },
            "g4_01_prerequisite": prerequisite,
            "g4_02_prerequisite": prerequisite,
            "g4_03_prerequisite": prerequisite,
            "g4_04_prerequisite": prerequisite,
            "canonical_validator_success": True,
            "eligibility": True,
            "release_consumable": True,
        }
        (root / ".agent-work/PLAN.md").write_bytes(
            machine_row("PLAN_MACHINE_CONTRACT", plan)
        )
        (root / ".agent-work/FULL_PLAN_REFERENCE.md").write_bytes(
            machine_row("FULL_PLAN_MACHINE_STATE", full)
        )

    def build_input(self) -> subject.StageGateInput:
        return subject.build_stage_gate_input(
            repo_root=self.root,
            source_checkpoint=self.source_checkpoint,
            source_tree=self.source_tree,
            output_root=self.output_root,
        )


class SyntheticGitRepository(SyntheticRepository):
    """A real local A -> C -> L Git topology with no network or external payload."""

    def __init__(self, root: Path) -> None:
        super().__init__(root, root / "offline-stage-gate")
        self.git("init", "-q")
        self.git("config", "user.name", "G4 Synthetic")
        self.git("config", "user.email", "g4-synthetic@example.invalid")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "synthetic activation parent")
        self.source_checkpoint = self.git_text("rev-parse", "HEAD")
        self.source_tree = self.git_text("rev-parse", "HEAD^{tree}")
        for path in subject.ALLOWED_CODE_CHILD_PATHS:
            (self.root / path).write_bytes(f"candidate:{path}\n".encode())
        value = self.build_input()
        self.stage_gate = subject.evaluate_stage_gate(value, repo_root=self.root)
        self.descriptor = subject.build_launch_descriptor(self.stage_gate)
        subject.validate_launch_descriptor(
            self.descriptor, self.stage_gate, repo_root=self.root,
        )
        self.git("add", "--", *subject.ALLOWED_CODE_CHILD_PATHS)
        self.git("commit", "-q", "-m", subject.ALLOWED_CODE_CHILD_SUBJECT)
        self.code_checkpoint = self.git_text("rev-parse", "HEAD")
        self.code_tree = self.git_text("rev-parse", "HEAD^{tree}")
        self.live_checkpoint = self.code_checkpoint
        self.live_tree = self.code_tree

    def git(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments], cwd=self.root, check=check,
            capture_output=True, text=True,
        )

    def git_text(self, *arguments: str) -> str:
        return self.git(*arguments).stdout.strip()

    def commit_tree(self, tree: str, parents: tuple[str, ...], subject: str) -> str:
        arguments = ["commit-tree", tree]
        for parent in parents:
            arguments.extend(("-p", parent))
        arguments.extend(("-m", subject))
        return self.git_text(*arguments)

    def set_head(self, checkpoint: str) -> None:
        self.git("update-ref", "HEAD", checkpoint)
        self.live_checkpoint = checkpoint
        self.live_tree = self.git_text("rev-parse", f"{checkpoint}^{{tree}}")

    def commit_orchestration_descendant(self, name: str = "state.md") -> None:
        path = self.root / ".agent-work" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"orchestration:{name}\n", encoding="utf-8")
        self.git("add", "--", f".agent-work/{name}")
        self.git("commit", "-q", "-m", f"synthetic orchestration {name}")
        self.live_checkpoint = self.git_text("rev-parse", "HEAD")
        self.live_tree = self.git_text("rev-parse", "HEAD^{tree}")

    def activation_probe(self) -> dict[str, object]:
        return {
            "code_owner_checkpoint": self.code_checkpoint,
            "code_owner_tree": self.code_tree,
            "live_activation_checkpoint": self.live_checkpoint,
            "live_activation_tree": self.live_tree,
        }

    def future_activation(self) -> tuple[dict, dict, subject.CommittedSourceAttestation]:
        template = self.stage_gate["runtime_plan_template"]
        probe = self.activation_probe()
        attestation = subject.validate_committed_source_attestation(
            self.descriptor, probe, repo_root=self.root,
        )
        activation = {
            "schema": subject.FUTURE_ACTIVATION_SCHEMA,
            "active_task": subject.FUTURE_TASK_ID,
            "active_task_count": 1,
            "execution_authorized": True,
            "allow_device_control": True,
            "descriptor_sha256": hashlib.sha256(
                provenance.canonical_json_bytes(self.descriptor)
            ).hexdigest(),
            "template_sha256": subject.runtime_plan_template_sha256(template),
            "expected_runtime_sha256": "0" * 64,
            **probe,
            "committed_source_attestation": provenance.json_native_value(
                asdict(attestation)
            ),
            "formal_root_parent": subject.FORMAL_ROOT_PARENT,
            "formal_root_basename": FUTURE_RUN_NAME,
            "formal_root_basename_regex": subject.FORMAL_ROOT_BASENAME_REGEX,
            "launch_cap": 1,
            "retry": 0,
        }
        activation["expected_runtime_sha256"] = (
            subject.materialized_runtime_plan_sha256(
                template, activation,
                committed_source_attestation=attestation,
            )
        )
        runtime = subject.materialize_runtime_plan(
            template, activation,
            committed_source_attestation=attestation,
        )
        return activation, runtime, attestation


class P7TdBR6StageGateTests(unittest.TestCase):
    def fixture(self, temporary: str) -> SyntheticRepository:
        base = Path(temporary)
        return SyntheticRepository(base / "repo", base / "durable-root")

    def gate(self, fixture: SyntheticRepository) -> tuple[subject.StageGateInput, dict, dict]:
        value = fixture.build_input()
        gate = subject.evaluate_stage_gate(value, repo_root=fixture.root)
        descriptor = subject.build_launch_descriptor(gate)
        subject.validate_launch_descriptor(descriptor, gate, repo_root=fixture.root)
        return value, gate, descriptor

    def future_activation(self, gate: dict, descriptor: dict) -> tuple[dict, dict]:
        template = gate["runtime_plan_template"]
        candidates = descriptor["committed_source_contract"][
            "allowed_code_owner_child"
        ]["candidate_references"]
        attestation = subject.CommittedSourceAttestation(
            schema=subject.COMMITTED_SOURCE_ATTESTATION_SCHEMA,
            verified_parent_checkpoint=ACTIVATION_HEAD,
            verified_parent_tree=ACTIVATION_TREE,
            code_owner_checkpoint="1" * 40,
            code_owner_tree="2" * 40,
            live_activation_checkpoint="1" * 40,
            live_activation_tree="2" * 40,
            candidate_references_sha256=hashlib.sha256(
                provenance.canonical_json_bytes(candidates)
            ).hexdigest(),
            post_child_changed_paths=(),
            post_child_commits=(),
        )
        attestation_value = provenance.json_native_value(asdict(attestation))
        activation = {
            "schema": subject.FUTURE_ACTIVATION_SCHEMA,
            "active_task": subject.FUTURE_TASK_ID,
            "active_task_count": 1,
            "execution_authorized": True,
            "allow_device_control": True,
            "descriptor_sha256": hashlib.sha256(
                provenance.canonical_json_bytes(descriptor)
            ).hexdigest(),
            "template_sha256": subject.runtime_plan_template_sha256(template),
            "expected_runtime_sha256": "0" * 64,
            "code_owner_checkpoint": attestation.code_owner_checkpoint,
            "code_owner_tree": attestation.code_owner_tree,
            "live_activation_checkpoint": attestation.live_activation_checkpoint,
            "live_activation_tree": attestation.live_activation_tree,
            "committed_source_attestation": attestation_value,
            "formal_root_parent": subject.FORMAL_ROOT_PARENT,
            "formal_root_basename": FUTURE_RUN_NAME,
            "formal_root_basename_regex": subject.FORMAL_ROOT_BASENAME_REGEX,
            "launch_cap": 1,
            "retry": 0,
        }
        activation["expected_runtime_sha256"] = (
            subject.materialized_runtime_plan_sha256(
                template, activation,
                committed_source_attestation=attestation,
            )
        )
        runtime = subject.materialize_runtime_plan(
            template, activation,
            committed_source_attestation=attestation,
        )
        return activation, runtime

    def test_live_input_binds_activation_and_all_candidate_sources(self):
        value = subject.build_stage_gate_input(
            repo_root=PROJECT_ROOT,
            source_checkpoint=ACTIVATION_HEAD,
            source_tree=ACTIVATION_TREE,
            output_root=LIVE_ROOT,
        )
        self.assertEqual(value.source_checkpoint, ACTIVATION_HEAD)
        self.assertEqual(value.source_tree, ACTIVATION_TREE)
        self.assertEqual(
            tuple(item.path for item in value.source_references),
            subject.EXPECTED_SOURCE_PATHS,
        )
        self.assertTrue(all(item.bytes > 0 for item in value.source_references))
        self.assertTrue(all(len(item.sha256) == 64 for item in value.source_references))
        self.assertEqual(value.prerequisite_projection["retained_r3_status"], subject.RETAINED_R3_STATUS)
        self.assertFalse(value.prerequisite_projection["release_consumption_authorized"])

    def test_canonical_factory_reuses_thermal_owner_and_freezes_exact_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            with mock.patch.object(
                thermal, "build_td_b_r6_formal_plan",
                wraps=thermal.build_td_b_r6_formal_plan,
            ) as build, mock.patch.object(
                thermal, "validate_td_b_r6_formal_plan",
                wraps=thermal.validate_td_b_r6_formal_plan,
            ) as validate:
                gate = subject.evaluate_stage_gate(value, repo_root=fixture.root)
            self.assertGreaterEqual(build.call_count, 1)
            self.assertGreaterEqual(validate.call_count, 1)
            contract = gate["scientific_contract"]
            canonical = contract["canonical_plan"]
            self.assertEqual(canonical["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
            self.assertEqual(
                canonical["state_shutters"],
                {"A": "1/5000", "D": "1/6400", "B": "1/8000", "C": "1/2500"},
            )
            self.assertEqual(
                [item["capture_id"] for item in contract["captures"]],
                list(thermal.TD_B_R6_CAPTURE_IDS),
            )
            self.assertTrue(all(item["exposure_mode"] == "fixed" for item in contract["captures"]))
            self.assertTrue(all(item["strip"] == "zero_throughout" for item in contract["captures"]))
            self.assertEqual(canonical["formal_logical"], 16)
            self.assertEqual(canonical["formal_physical_cap"], 16)
            self.assertEqual(canonical["retry"], 0)
            self.assertEqual(contract["operating_envelope"]["steady_status"], "not_demonstrated")
            self.assertFalse(gate["authority"]["execution_authorized"])
            self.assertFalse(gate["claims"]["hardware_ready"])

    def test_source_reference_path_identity_and_set_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            first = value.source_references[0]
            cases = (
                replace(first, path="/absolute/path"),
                replace(first, bytes=first.bytes + 1),
                replace(first, sha256="0" * 64),
                replace(first, mode=first.mode ^ 0o100),
            )
            for altered in cases:
                references = (altered,) + value.source_references[1:]
                with self.subTest(altered=altered), self.assertRaises(subject.StageGateError):
                    subject.evaluate_stage_gate(replace(value, source_references=references), repo_root=fixture.root)
            with self.assertRaisesRegex(subject.StageGateError, "source_reference_duplicate"):
                subject.evaluate_stage_gate(
                    replace(value, source_references=value.source_references[:-1] + (first,)),
                    repo_root=fixture.root,
                )
            with self.assertRaisesRegex(subject.StageGateError, "source_reference_set_drift"):
                subject.evaluate_stage_gate(
                    replace(value, source_references=value.source_references[:-1]),
                    repo_root=fixture.root,
                )

    def test_symlink_source_and_output_root_drift_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            target = fixture.root / subject.EXPECTED_SOURCE_PATHS[-1]
            original = target.read_bytes()
            target.unlink()
            target.symlink_to(fixture.root / subject.EXPECTED_SOURCE_PATHS[-2])
            with self.assertRaisesRegex(subject.StageGateError, "source_not_regular"):
                fixture.build_input()
            target.unlink()
            target.write_bytes(original)
            source = (fixture.root / ".agent-work/PLAN.md").read_bytes()
            source = source.replace(str(fixture.output_root).encode(), b"/different/root")
            (fixture.root / ".agent-work/PLAN.md").write_bytes(source)
            with self.assertRaisesRegex(subject.StageGateError, "output_root_drift"):
                fixture.build_input()

    def test_descriptor_reference_drift_precedes_semantic_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, descriptor = self.gate(fixture)
            descriptor["runner"]["argv_shape"].append("--token")
            descriptor["source_references"][0]["sha256"] = "0" * 64
            with self.assertRaisesRegex(subject.StageGateError, "descriptor_reference_drift"):
                subject.validate_launch_descriptor(descriptor, gate, repo_root=fixture.root)

    def test_reference_consistent_secret_and_historical_semantics_hit_specialized_guards(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, descriptor = self.gate(fixture)
            secret = deepcopy(descriptor)
            secret["runner"]["argv_shape"].append("--secret-token")
            with self.assertRaisesRegex(subject.StageGateError, "secret_material_prohibited"):
                subject.validate_launch_descriptor(secret, gate, repo_root=fixture.root)
            historical = deepcopy(descriptor)
            historical["runner"]["argv_shape"].append("audit/1/historical.json")
            with self.assertRaisesRegex(subject.StageGateError, "historical_input_prohibited"):
                subject.validate_launch_descriptor(historical, gate, repo_root=fixture.root)

    def test_canonical_plan_and_expanded_contract_drift_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, _ = self.gate(fixture)
            mutations = []
            reordered = deepcopy(gate)
            reordered["scientific_contract"]["canonical_plan"]["capture_ids"][0:2] = reversed(
                reordered["scientific_contract"]["canonical_plan"]["capture_ids"][0:2]
            )
            mutations.append(reordered)
            duplicate = deepcopy(gate)
            duplicate["scientific_contract"]["captures"][1]["capture_id"] = duplicate["scientific_contract"]["captures"][0]["capture_id"]
            mutations.append(duplicate)
            wrong_shutter = deepcopy(gate)
            wrong_shutter["scientific_contract"]["captures"][0]["nominal_shutter"] = "1/4000"
            mutations.append(wrong_shutter)
            auto = deepcopy(gate)
            auto["scientific_contract"]["captures"][0]["exposure_mode"] = "auto"
            mutations.append(auto)
            budget = deepcopy(gate)
            budget["scientific_contract"]["canonical_plan"]["formal_physical_cap"] = 15
            mutations.append(budget)
            retry = deepcopy(gate)
            retry["scientific_contract"]["hard_failure"]["retry"] = 1
            mutations.append(retry)
            strip = deepcopy(gate)
            strip["scientific_contract"]["captures"][0]["strip"] = "nonzero"
            mutations.append(strip)
            steady = deepcopy(gate)
            steady["scientific_contract"]["operating_envelope"]["steady_status"] = "demonstrated"
            mutations.append(steady)
            bypass = deepcopy(gate)
            bypass["scientific_contract"]["history_gate"]["bypass_allowed"] = True
            mutations.append(bypass)
            for altered in mutations:
                with self.subTest(), self.assertRaises(subject.StageGateError):
                    subject.validate_stage_gate(altered, repo_root=fixture.root)

    def test_launch_descriptor_is_non_authorizing_and_preserves_future_bounds(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, descriptor = self.gate(fixture)
            self.assertEqual(descriptor["status"], "non_authorizing_waiting_g4_06_plan")
            self.assertFalse(descriptor["authority"]["execution_authorized"])
            self.assertEqual(descriptor["budgets"]["launch_cap"], 1)
            self.assertEqual(descriptor["budgets"]["retry"], 0)
            self.assertTrue(descriptor["formal_root"]["single_root"])
            self.assertTrue(descriptor["production_wrapper"]["visible_terminal_required"])
            self.assertEqual(descriptor["cleanup"]["python"], "existing_measure_owner_required")
            self.assertEqual(descriptor["cleanup"]["shell"], "existing_production_wrapper_trap_required")
            self.assertNotIn("human_authorization_verified", json.dumps(descriptor))
            self.assertFalse(gate["authority"]["formal_root_creation_authorized"])
            source_contract = descriptor["committed_source_contract"]
            self.assertEqual(
                source_contract["verified_parent"],
                {
                    "checkpoint": fixture.source_checkpoint,
                    "tree": fixture.source_tree,
                    "role": "activation_parent_not_code_owner",
                },
            )
            child = source_contract["allowed_code_owner_child"]
            self.assertEqual(child["subject"], subject.ALLOWED_CODE_CHILD_SUBJECT)
            self.assertEqual(
                child["changed_paths"], list(subject.ALLOWED_CODE_CHILD_PATHS),
            )
            self.assertFalse(child["child_checkpoint_recorded"])
            self.assertFalse(child["child_tree_recorded"])
            self.assertNotIn("source_checkpoint", descriptor)
            self.assertNotIn("source_tree", descriptor)
            template = gate["runtime_plan_template"]
            self.assertEqual(template["schema"], thermal.PLAN_SCHEMA_V2)
            self.assertEqual(template["status"], subject.RUNTIME_TEMPLATE_STATUS)
            self.assertFalse(template["execution_authorization"]["execution_authorized"])
            self.assertFalse(template["formal_capture_eligible"])
            self.assertEqual(
                descriptor["runtime_plan_template_sha256"],
                subject.runtime_plan_template_sha256(template),
            )

    def test_runtime_template_exact_shape_round_trip_and_existing_validator_rejects_before_connect(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, _ = self.gate(fixture)
            template = gate["runtime_plan_template"]
            subject.validate_runtime_plan_template(template)
            round_trip = provenance.decode_canonical_json(
                provenance.canonical_json_bytes(template)
            )
            subject.validate_runtime_plan_template(round_trip)
            self.assertLessEqual(
                {
                    "schema", "status", "experiment_id", "stage", "source",
                    "timing_contract", "native_raw_ambient_policy", "camera",
                    "execution_authorization", "captures", "budgets",
                    "frozen_shutters", "cleanup", "quality_history_contract",
                },
                set(template),
            )
            self.assertEqual(
                [row["capture_id"] for row in template["captures"]],
                list(thermal.TD_B_R6_CAPTURE_IDS),
            )
            self.assertEqual(
                [row["requested_elapsed_s"] for row in template["captures"]],
                [600, 60, 120, 300, 600, 600, 60, 120, 300, 600, 600, 60, 120, 300, 600, 600],
            )
            self.assertEqual(template["budgets"]["formal_cap"], 16)
            self.assertEqual(template["budgets"]["physical_cr3_cap"], 16)
            self.assertEqual(template["budgets"]["ambient_cap"], 0)
            self.assertEqual(template["budgets"]["setup_physical_cr3_cap"], 0)
            self.assertEqual(template["budgets"]["retry"], 0)
            backend = FakeCapableBackend()
            with self.assertRaises(PermissionError):
                measure.validate_authorized_execution_plan(
                    template, camera_backend=backend,
                )
            backend.connect.assert_not_called()

    def test_synthetic_materialization_passes_focused_and_existing_validators_without_connect(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            _, gate, descriptor = self.gate(fixture)
            activation, runtime = self.future_activation(gate, descriptor)
            subject.validate_materialized_runtime_plan(runtime)
            self.assertEqual(
                hashlib.sha256(provenance.canonical_json_bytes(runtime)).hexdigest(),
                activation["expected_runtime_sha256"],
            )
            self.assertNotIn(
                "expected_runtime_sha256", runtime["execution_authorization"],
            )
            self.assertNotIn("source_checkpoint", runtime["execution_authorization"])
            self.assertNotIn("source_tree", runtime["execution_authorization"])
            attestation = runtime["execution_authorization"][
                "committed_source_attestation"
            ]
            self.assertEqual(attestation["verified_parent_checkpoint"], ACTIVATION_HEAD)
            self.assertEqual(attestation["code_owner_checkpoint"], "1" * 40)
            self.assertEqual(attestation["live_activation_checkpoint"], "1" * 40)
            backend = FakeCapableBackend()
            measure.validate_authorized_execution_plan(runtime, camera_backend=backend)
            backend.connect.assert_not_called()

    def test_persist_internal_replay_public_replay_modes_inventory_and_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            persisted = subject.persist_stage_gate_package(value, repo_root=fixture.root)
            self.assertEqual(persisted["status"], "pass")
            self.assertTrue(persisted["internal_replay"])
            self.assertEqual(oct(os.stat(fixture.output_root).st_mode & 0o777), "0o700")
            self.assertEqual(
                tuple(sorted(path.name for path in fixture.output_root.iterdir())),
                subject.EXPECTED_ARTIFACTS,
            )
            self.assertTrue(all((os.stat(path).st_mode & 0o777) == 0o600 for path in fixture.output_root.iterdir()))
            replay = subject.replay_stage_gate_package(fixture.output_root, repo_root=fixture.root)
            self.assertEqual(replay["status"], "pass")
            self.assertEqual(tuple(replay["inventory"]), subject.EXPECTED_ARTIFACTS)
            terminal = provenance.decode_canonical_json((fixture.output_root / "terminal-seal.json").read_bytes())
            self.assertEqual(terminal["status"], subject.PASS_STATUS)
            self.assertNotIn("terminal-seal.json", terminal["artifacts"])
            self.assertEqual(terminal["formal_capture_count"], 0)
            self.assertEqual(terminal["device_call_count"], 0)

    def test_public_replay_rejects_post_persist_tamper_and_extra_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            subject.persist_stage_gate_package(fixture.build_input(), repo_root=fixture.root)
            stage = fixture.output_root / "stage-gate.json"
            stage.write_bytes(stage.read_bytes() + b" ")
            with self.assertRaises(subject.StageGateError):
                subject.replay_stage_gate_package(fixture.output_root, repo_root=fixture.root)
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            subject.persist_stage_gate_package(fixture.build_input(), repo_root=fixture.root)
            extra = fixture.output_root / "extra.json"
            extra.write_text("{}\n", encoding="utf-8")
            os.chmod(extra, 0o600)
            with self.assertRaisesRegex(subject.StageGateError, "artifact_inventory_drift"):
                subject.replay_stage_gate_package(fixture.output_root, repo_root=fixture.root)

    def test_first_persist_failure_is_terminal_sealed_without_retry_or_alternate_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            with mock.patch.object(
                subject, "evaluate_stage_gate", side_effect=subject.StageGateError("synthetic_first_failure"),
            ), self.assertRaisesRegex(subject.StageGateError, "synthetic_first_failure"):
                subject.persist_stage_gate_package(value, repo_root=fixture.root)
            self.assertEqual(
                tuple(path.name for path in fixture.output_root.iterdir()),
                ("terminal-seal.json",),
            )
            terminal = provenance.decode_canonical_json((fixture.output_root / "terminal-seal.json").read_bytes())
            self.assertEqual(terminal["status"], subject.FAIL_STATUS)
            self.assertEqual(terminal["failure_code"], "synthetic_first_failure")
            self.assertEqual(terminal["retry"], 0)
            self.assertEqual(terminal["alternate_root"], 0)

    def test_runner_signature_and_narrow_hook_delegate_real_shape_exactly_once(self):
        with tempfile.TemporaryDirectory(dir=subject.FORMAL_ROOT_PARENT) as temporary:
            fixture = SyntheticGitRepository(Path(temporary))
            gate = fixture.stage_gate
            descriptor = fixture.descriptor
            activation, runtime, _ = fixture.future_activation()
            signature = inspect.signature(measure.run_authorized_plan)
            self.assertEqual(tuple(signature.parameters)[:4], (
                "plan", "output_dir", "run_name", "camera_backend",
            ))
            self.assertEqual(signature.parameters["plan"].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            for name in ("output_dir", "run_name", "camera_backend"):
                self.assertEqual(signature.parameters[name].kind, inspect.Parameter.KEYWORD_ONLY)
            backend = FakeCapableBackend()
            with mock.patch.object(
                measure, "run_authorized_plan", return_value=Path("/synthetic/result"),
            ) as real_owner:
                result = measure.run_validated_td_b_r6_runtime_contract(
                    runtime, gate, descriptor, activation,
                    repo_root=fixture.root,
                    output_dir=subject.FORMAL_ROOT_PARENT,
                    run_name=FUTURE_RUN_NAME,
                    camera_backend=backend,
                    delegated_run_fn=real_owner,
                )
            self.assertEqual(result, Path("/synthetic/result"))
            real_owner.assert_called_once_with(
                runtime,
                output_dir=subject.FORMAL_ROOT_PARENT,
                run_name=FUTURE_RUN_NAME,
                camera_backend=backend,
            )
            backend.connect.assert_not_called()

    def test_invalid_activation_and_runtime_probes_stop_before_delegate(self):
        with tempfile.TemporaryDirectory(dir=subject.FORMAL_ROOT_PARENT) as temporary:
            fixture = SyntheticGitRepository(Path(temporary))
            gate = fixture.stage_gate
            descriptor = fixture.descriptor
            activation, runtime, _ = fixture.future_activation()
            cases = []
            missing = dict(activation)
            missing.pop("code_owner_tree")
            cases.append((runtime, descriptor, missing, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            missing_attestation = dict(activation)
            missing_attestation.pop("committed_source_attestation")
            cases.append((runtime, descriptor, missing_attestation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            extra = dict(activation, unexpected=False)
            cases.append((runtime, descriptor, extra, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            descriptor_drift = deepcopy(descriptor)
            descriptor_drift["runner"]["delegate"] = "other"
            cases.append((runtime, descriptor_drift, activation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            for field, value in (
                ("template_sha256", "0" * 64),
                ("expected_runtime_sha256", "0" * 64),
                ("code_owner_checkpoint", "0" * 40),
                ("active_task_count", True),
                ("formal_root_parent", "/different"),
                ("launch_cap", 2),
                ("launch_cap", True),
                ("retry", 1),
            ):
                cases.append((runtime, descriptor, dict(activation, **{field: value}), subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            parent_as_code = dict(activation)
            parent_as_code["code_owner_checkpoint"] = fixture.source_checkpoint
            parent_as_code["code_owner_tree"] = fixture.source_tree
            cases.append((runtime, descriptor, parent_as_code, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            extra_attestation = deepcopy(activation)
            extra_attestation["committed_source_attestation"]["unexpected"] = False
            cases.append((runtime, descriptor, extra_attestation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            missing_ledger = deepcopy(activation)
            missing_ledger["committed_source_attestation"].pop("post_child_commits")
            cases.append((runtime, descriptor, missing_ledger, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            forged_ledger = deepcopy(activation)
            forged_ledger["committed_source_attestation"]["post_child_commits"] = [{
                "parent_checkpoint": fixture.code_checkpoint,
                "child_checkpoint": fixture.code_checkpoint,
                "child_tree": fixture.code_tree,
                "changed_paths": [],
            }]
            cases.append((runtime, descriptor, forged_ledger, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            runtime_mutations = []
            for mutation in (
                lambda value: value.__setitem__("schema", "wrong"),
                lambda value: value["captures"].reverse(),
                lambda value: value["captures"][0].__setitem__("state_id", "B"),
                lambda value: value["captures"][0].__setitem__("requested_elapsed_s", 60),
                lambda value: value["captures"][0]["command"].__setitem__("hue", 0),
                lambda value: value["frozen_shutters"].__setitem__(next(iter(value["frozen_shutters"])), "1/30"),
                lambda value: value["budgets"].__setitem__("physical_cr3_cap", 15),
                lambda value: value["budgets"].__setitem__("formal_cap", 17),
                lambda value: value["budgets"].__setitem__("ambient_cap", 1),
                lambda value: value["budgets"].__setitem__("setup_physical_cr3_cap", 1),
                lambda value: value["budgets"].__setitem__("retry", 1),
                lambda value: value["captures"][0].__setitem__("strip_state", "nonzero"),
            ):
                altered = deepcopy(runtime)
                mutation(altered)
                runtime_mutations.append(altered)
            cases.extend(
                (altered, descriptor, activation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME)
                for altered in runtime_mutations
            )
            cases.append((runtime, descriptor, activation, "/different", FUTURE_RUN_NAME))
            cases.append((runtime, descriptor, activation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME + "x"))
            forged_runtime = deepcopy(runtime)
            forged_runtime["execution_authorization"][
                "committed_source_attestation"
            ]["post_child_commits"] = [{
                "parent_checkpoint": fixture.code_checkpoint,
                "child_checkpoint": fixture.code_checkpoint,
                "child_tree": fixture.code_tree,
                "changed_paths": [],
            }]
            cases.append((forged_runtime, descriptor, activation, subject.FORMAL_ROOT_PARENT, FUTURE_RUN_NAME))
            backend = FakeCapableBackend()
            for index, (candidate, descriptor_value, activation_value, output_dir, run_name) in enumerate(cases):
                callback = mock.Mock()
                with self.subTest(index=index), self.assertRaises((subject.StageGateError, PermissionError)):
                    measure.run_validated_td_b_r6_runtime_contract(
                        candidate, gate, descriptor_value, activation_value,
                        repo_root=fixture.root,
                        output_dir=output_dir,
                        run_name=run_name,
                        camera_backend=backend,
                        delegated_run_fn=callback,
                    )
                callback.assert_not_called()
            backend.connect.assert_not_called()

    def test_current_g4_05_authority_never_calls_real_or_fake_runner(self):
        with tempfile.TemporaryDirectory(dir=subject.FORMAL_ROOT_PARENT) as temporary:
            fixture = SyntheticGitRepository(Path(temporary))
            gate = fixture.stage_gate
            descriptor = fixture.descriptor
            activation, runtime, _ = fixture.future_activation()
            current = dict(
                activation,
                active_task=subject.TASK_ID,
                execution_authorized=False,
                allow_device_control=False,
            )
            callback = mock.Mock()
            backend = FakeCapableBackend()
            with self.assertRaises(subject.StageGateError):
                measure.run_validated_td_b_r6_runtime_contract(
                    runtime, gate, descriptor, current,
                    repo_root=fixture.root,
                    output_dir=subject.FORMAL_ROOT_PARENT,
                    run_name=FUTURE_RUN_NAME,
                    camera_backend=backend,
                    delegated_run_fn=callback,
                )
            callback.assert_not_called()
            backend.connect.assert_not_called()

    def test_committed_source_attestation_accepts_code_child_and_agent_work_descendants(self):
        with tempfile.TemporaryDirectory(dir=subject.FORMAL_ROOT_PARENT) as temporary:
            fixture = SyntheticGitRepository(Path(temporary))
            activation, runtime, attestation = fixture.future_activation()
            self.assertEqual(attestation.verified_parent_checkpoint, fixture.source_checkpoint)
            self.assertEqual(attestation.code_owner_checkpoint, fixture.code_checkpoint)
            self.assertEqual(attestation.live_activation_checkpoint, fixture.code_checkpoint)
            self.assertEqual(attestation.post_child_changed_paths, ())
            self.assertEqual(attestation.post_child_commits, ())
            subject.validate_future_activation(
                fixture.descriptor,
                fixture.stage_gate["runtime_plan_template"],
                runtime,
                activation,
                repo_root=fixture.root,
                output_dir=subject.FORMAL_ROOT_PARENT,
                run_name=FUTURE_RUN_NAME,
            )
            parent = fixture.code_checkpoint
            fixture.commit_orchestration_descendant("state-one.md")
            first = fixture.live_checkpoint
            first_tree = fixture.live_tree
            fixture.commit_orchestration_descendant("state-two.md")
            second = fixture.live_checkpoint
            second_tree = fixture.live_tree
            activation, runtime, attestation = fixture.future_activation()
            self.assertEqual(attestation.code_owner_checkpoint, fixture.code_checkpoint)
            self.assertEqual(attestation.live_activation_checkpoint, fixture.live_checkpoint)
            self.assertEqual(
                attestation.post_child_changed_paths,
                (".agent-work/state-one.md", ".agent-work/state-two.md"),
            )
            self.assertEqual(
                attestation.post_child_commits,
                (
                    {
                        "parent_checkpoint": parent,
                        "child_checkpoint": first,
                        "child_tree": first_tree,
                        "changed_paths": [".agent-work/state-one.md"],
                    },
                    {
                        "parent_checkpoint": first,
                        "child_checkpoint": second,
                        "child_tree": second_tree,
                        "changed_paths": [".agent-work/state-two.md"],
                    },
                ),
            )
            (fixture.root / ".agent-work/EXECUTION_RESULT.md").write_text(
                "phase2 dirty handoff\n", encoding="utf-8",
            )
            observed = subject.validate_committed_source_attestation(
                fixture.descriptor, activation, repo_root=fixture.root,
            )
            self.assertEqual(observed, attestation)

    def test_per_commit_history_rejects_1913_add_delete_and_restored_non_orchestration_matrix(self):
        paths = (
            "src/transient-post-child.py",
            "tests/transient-post-child.py",
            "config/transient-post-child.toml",
            "advisor/4/4.GUIDE.md",
            "tmp/run-p7-thermal-diagnostics.zsh",
            ".agent-work-evil/transient.md",
        )
        for path in paths:
            with self.subTest(path=path), tempfile.TemporaryDirectory(
                dir=subject.FORMAL_ROOT_PARENT,
            ) as temporary:
                fixture = SyntheticGitRepository(Path(temporary))
                target = fixture.root / path
                original = target.read_bytes() if target.exists() else None
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((original or b"") + b"transient post-child drift\n")
                fixture.git("add", "--", path)
                fixture.git("commit", "-q", "-m", f"add transient {path}")
                if original is None:
                    target.unlink()
                else:
                    target.write_bytes(original)
                fixture.git("add", "-A", "--", path)
                fixture.git("commit", "-q", "-m", f"restore transient {path}")
                fixture.live_checkpoint = fixture.git_text("rev-parse", "HEAD")
                fixture.live_tree = fixture.git_text("rev-parse", "HEAD^{tree}")
                self.assertEqual(fixture.live_tree, fixture.code_tree)
                with self.assertRaisesRegex(
                    subject.StageGateError,
                    "committed_source_post_child_path_drift",
                ):
                    subject.validate_committed_source_attestation(
                        fixture.descriptor,
                        fixture.activation_probe(),
                        repo_root=fixture.root,
                    )

    def test_per_commit_history_rejects_merge_even_with_restored_tree(self):
        for branch_has_source_drift in (False, True):
            with self.subTest(
                branch_has_source_drift=branch_has_source_drift,
            ), tempfile.TemporaryDirectory(
                dir=subject.FORMAL_ROOT_PARENT,
            ) as temporary:
                fixture = SyntheticGitRepository(Path(temporary))
                branch_tree = fixture.code_tree
                if branch_has_source_drift:
                    path = "src/branch-transient.py"
                    target = fixture.root / path
                    target.write_text("branch drift\n", encoding="utf-8")
                    fixture.git("add", "--", path)
                    branch_tree = fixture.git_text("write-tree")
                    target.unlink()
                    fixture.git("add", "-A", "--", path)
                branch = fixture.commit_tree(
                    branch_tree, (fixture.code_checkpoint,), "synthetic side branch",
                )
                merge = fixture.commit_tree(
                    fixture.code_tree,
                    (fixture.code_checkpoint, branch),
                    "synthetic merge with restored first-parent tree",
                )
                fixture.set_head(merge)
                self.assertEqual(fixture.live_tree, fixture.code_tree)
                with self.assertRaisesRegex(
                    subject.StageGateError,
                    "committed_source_post_child_non_linear_history",
                ):
                    subject.validate_committed_source_attestation(
                        fixture.descriptor,
                        fixture.activation_probe(),
                        repo_root=fixture.root,
                    )

    def test_per_commit_history_rejects_mixed_adjacent_paths(self):
        with tempfile.TemporaryDirectory(dir=subject.FORMAL_ROOT_PARENT) as temporary:
            fixture = SyntheticGitRepository(Path(temporary))
            paths = (".agent-work/state.md", "src/mixed-transient.py")
            for path in paths:
                target = fixture.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"mixed:{path}\n", encoding="utf-8")
            fixture.git("add", "--", *paths)
            fixture.git("commit", "-q", "-m", "mixed orchestration and source")
            fixture.live_checkpoint = fixture.git_text("rev-parse", "HEAD")
            fixture.live_tree = fixture.git_text("rev-parse", "HEAD^{tree}")
            with self.assertRaisesRegex(
                subject.StageGateError,
                "committed_source_post_child_path_drift",
            ):
                subject.validate_committed_source_attestation(
                    fixture.descriptor,
                    fixture.activation_probe(),
                    repo_root=fixture.root,
                )

    def test_committed_source_attestation_rejects_parent_subject_merge_and_path_drift(self):
        cases = (
            "subject", "parent", "missing_parent", "merge", "extra_path",
            "missing_descriptor", "extra_descriptor", "reordered_descriptor",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory(
                dir=subject.FORMAL_ROOT_PARENT,
            ) as temporary:
                fixture = SyntheticGitRepository(Path(temporary))
                descriptor = deepcopy(fixture.descriptor)
                expected_code = {
                    "subject": "committed_source_subject_drift",
                    "parent": "committed_source_parent_drift",
                    "missing_parent": "committed_source_parent_drift",
                    "merge": "committed_source_parent_drift",
                    "extra_path": "committed_source_changed_paths_drift",
                    "missing_descriptor": "committed_source_descriptor_semantic_drift",
                    "extra_descriptor": "committed_source_descriptor_semantic_drift",
                    "reordered_descriptor": "committed_source_descriptor_semantic_drift",
                }[case]
                if case == "subject":
                    bad = fixture.commit_tree(
                        fixture.code_tree, (fixture.source_checkpoint,), "wrong subject",
                    )
                    fixture.code_checkpoint = bad
                    fixture.set_head(bad)
                elif case == "parent":
                    side = fixture.commit_tree(
                        fixture.source_tree, (fixture.source_checkpoint,), "side parent",
                    )
                    bad = fixture.commit_tree(
                        fixture.code_tree, (side,), subject.ALLOWED_CODE_CHILD_SUBJECT,
                    )
                    fixture.code_checkpoint = bad
                    fixture.set_head(bad)
                elif case == "missing_parent":
                    bad = fixture.commit_tree(
                        fixture.code_tree, (), subject.ALLOWED_CODE_CHILD_SUBJECT,
                    )
                    fixture.code_checkpoint = bad
                    fixture.set_head(bad)
                elif case == "merge":
                    side = fixture.commit_tree(
                        fixture.source_tree, (fixture.source_checkpoint,), "side parent",
                    )
                    bad = fixture.commit_tree(
                        fixture.code_tree,
                        (fixture.source_checkpoint, side),
                        subject.ALLOWED_CODE_CHILD_SUBJECT,
                    )
                    fixture.code_checkpoint = bad
                    fixture.set_head(bad)
                elif case == "extra_path":
                    extra = fixture.root / "extra.py"
                    extra.write_text("extra\n", encoding="utf-8")
                    fixture.git("add", "--", "extra.py")
                    tree = fixture.git_text("write-tree")
                    bad = fixture.commit_tree(
                        tree, (fixture.source_checkpoint,),
                        subject.ALLOWED_CODE_CHILD_SUBJECT,
                    )
                    fixture.code_checkpoint = bad
                    fixture.code_tree = tree
                    fixture.set_head(bad)
                elif case == "missing_descriptor":
                    descriptor["committed_source_contract"][
                        "allowed_code_owner_child"
                    ]["changed_paths"].pop()
                elif case == "extra_descriptor":
                    descriptor["committed_source_contract"][
                        "allowed_code_owner_child"
                    ]["changed_paths"].append("extra.py")
                else:
                    descriptor["committed_source_contract"][
                        "allowed_code_owner_child"
                    ]["changed_paths"].reverse()
                with self.assertRaisesRegex(subject.StageGateError, expected_code):
                    subject.validate_committed_source_attestation(
                        descriptor, fixture.activation_probe(), repo_root=fixture.root,
                    )

    def test_committed_source_attestation_rejects_tree_blob_lineage_and_descriptor_prefill(self):
        cases = (
            "code_tree", "live_tree", "blob", "non_descendant",
            "post_child_src", "post_child_prefix", "prefilled_child",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory(
                dir=subject.FORMAL_ROOT_PARENT,
            ) as temporary:
                fixture = SyntheticGitRepository(Path(temporary))
                descriptor = deepcopy(fixture.descriptor)
                probe = fixture.activation_probe()
                expected_code = {
                    "code_tree": "committed_source_tree_drift",
                    "live_tree": "committed_source_tree_drift",
                    "blob": "committed_source_candidate_blob_drift",
                    "non_descendant": "committed_source_lineage_drift",
                    "post_child_src": "committed_source_post_child_path_drift",
                    "post_child_prefix": "committed_source_post_child_path_drift",
                    "prefilled_child": "committed_source_descriptor_semantic_drift",
                }[case]
                if case == "code_tree":
                    probe["code_owner_tree"] = "0" * 40
                elif case == "live_tree":
                    probe["live_activation_tree"] = "0" * 40
                elif case == "blob":
                    target = subject.ALLOWED_CODE_CHILD_PATHS[0]
                    for collection in (
                        descriptor["source_references"],
                        descriptor["committed_source_contract"][
                            "allowed_code_owner_child"
                        ]["candidate_references"],
                    ):
                        next(item for item in collection if item["path"] == target)[
                            "sha256"
                        ] = "0" * 64
                elif case == "non_descendant":
                    divergent = fixture.commit_tree(
                        fixture.code_tree, (fixture.source_checkpoint,), "divergent live",
                    )
                    fixture.set_head(divergent)
                    probe = fixture.activation_probe()
                elif case in {"post_child_src", "post_child_prefix"}:
                    path = (
                        "src/post-child.py"
                        if case == "post_child_src"
                        else ".agent-work-evil/state.md"
                    )
                    target = fixture.root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("drift\n", encoding="utf-8")
                    fixture.git("add", "--", path)
                    fixture.git("commit", "-q", "-m", "post-child drift")
                    fixture.live_checkpoint = fixture.git_text("rev-parse", "HEAD")
                    fixture.live_tree = fixture.git_text("rev-parse", "HEAD^{tree}")
                    probe = fixture.activation_probe()
                else:
                    descriptor["committed_source_contract"][
                        "allowed_code_owner_child"
                    ]["child_checkpoint"] = "0" * 40
                with self.assertRaisesRegex(subject.StageGateError, expected_code):
                    subject.validate_committed_source_attestation(
                        descriptor, probe, repo_root=fixture.root,
                    )

    def test_committed_source_attestation_worktree_scope_covers_tracked_staged_and_untracked(self):
        cases = ("tracked_candidate", "staged_candidate", "outside_untracked")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory(
                dir=subject.FORMAL_ROOT_PARENT,
            ) as temporary:
                fixture = SyntheticGitRepository(Path(temporary))
                if case in {"tracked_candidate", "staged_candidate"}:
                    path = fixture.root / subject.ALLOWED_CODE_CHILD_PATHS[0]
                    path.write_bytes(path.read_bytes() + b"drift\n")
                    if case == "staged_candidate":
                        fixture.git("add", "--", subject.ALLOWED_CODE_CHILD_PATHS[0])
                    expected = "committed_source_current_candidate_drift"
                else:
                    (fixture.root / "untracked.txt").write_text(
                        "outside\n", encoding="utf-8",
                    )
                    expected = "committed_source_worktree_scope_drift"
                with self.assertRaisesRegex(subject.StageGateError, expected):
                    subject.validate_committed_source_attestation(
                        fixture.descriptor, fixture.activation_probe(), repo_root=fixture.root,
                    )

    def test_post_capture_ledger_validator_is_never_called_by_g4_05_owners(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            with mock.patch.object(
                thermal, "validate_td_b_r6_capture_ledger",
            ) as ledger_validator:
                value, gate, descriptor = self.gate(fixture)
                activation, runtime = self.future_activation(gate, descriptor)
                subject.validate_runtime_plan_template(gate["runtime_plan_template"])
                subject.validate_materialized_runtime_plan(runtime)
                subject.persist_stage_gate_package(value, repo_root=fixture.root)
                subject.replay_stage_gate_package(
                    fixture.output_root, repo_root=fixture.root,
                )
            ledger_validator.assert_not_called()
            self.assertEqual(
                gate["runtime_plan_template"]["post_capture_validator"]["callable"],
                "validate_td_b_r6_capture_ledger",
            )
            self.assertEqual(
                gate["runtime_plan_template"]["post_capture_validator"]["g4_05_call_count"],
                0,
            )

    def test_root_must_be_fresh_and_second_persist_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            subject.persist_stage_gate_package(value, repo_root=fixture.root)
            with self.assertRaisesRegex(provenance.ProvenanceIOError, "root_exists"):
                subject.persist_stage_gate_package(value, repo_root=fixture.root)


if __name__ == "__main__":
    unittest.main()
