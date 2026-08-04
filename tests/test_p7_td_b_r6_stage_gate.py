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
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


ACTIVATION_HEAD = "860b27359ab54a1c8c4b4a4737331e169e53cb38"
ACTIVATION_TREE = "c4c9f0129beba2f13b663f9d392abab986e37484"
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

    def __init__(
        self,
        root: Path,
        *,
        code_child_subject: str = "feat(stage-gate): route ray r6 formal launch owner",
    ) -> None:
        root = root.resolve()
        super().__init__(root, root.parent / "offline-stage-gate")
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
        self.git("commit", "-q", "-m", code_child_subject)
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

    def persist_production_package(self) -> None:
        subject.persist_stage_gate_package(self.build_input(), repo_root=self.root)

    def activate_package_a_machine(self) -> None:
        plan = {
            "active_task_count": 1,
            "active_task": subject.FUTURE_TASK_ID,
            "reference_task_id": subject.FUTURE_TASK_ID,
            "contract_id": subject.ENGINEERING_PACKAGE_A_CONTRACT_ID,
        }
        full = {
            "active_task_count": 1,
            "active_task": subject.FUTURE_TASK_ID,
            "active_plan_contract_id": subject.ENGINEERING_PACKAGE_A_CONTRACT_ID,
            "canonical_next_reference_task": subject.FUTURE_TASK_ID,
            "executable": False,
            "full_is_non_executable_reference": True,
            "release_consumption_authorized": False,
            "device_authorized_by_this_file": False,
            "camera_authorized_by_this_file": False,
            "ray_authorized_by_this_file": False,
            "strip_authorized_by_this_file": False,
            "formal_r6_authorized": False,
            "td_c_authorized": False,
            "g4_06_state": {
                "package": "A_AUTHORITY_CONTRACT_REVISION_ENGINEERING_ONLY",
                "formal_execution_authorized": False,
            },
        }
        self.commit_machine(plan, full, "synthetic package A activation")

    def activate_package_b_machine(self) -> None:
        plan, full = self.package_b_machine_values()
        self.commit_machine(plan, full, "synthetic package B activation")

    def package_b_machine_values(self) -> tuple[dict, dict]:
        authority = {
            "experiment_id": thermal.TD_B,
            "source": "ray",
            "stage": "TD-B",
            "camera_backend": "remote",
            "formal_execution_authorized": True,
            "formal_root_creation_authorized": True,
            "device_control_authorized": True,
            "camera_authorized": True,
            "ray_authorized": True,
            "strip_authorized": False,
            "capture_authorized": True,
            "formal_root_parent": subject.FORMAL_ROOT_PARENT,
            "formal_root_basename": FUTURE_RUN_NAME,
            "formal_root_basename_regex": subject.FORMAL_ROOT_BASENAME_REGEX,
            "logical_capture_cap": 16,
            "physical_cr3_cap": 16,
            "launch_cap": 1,
            "retry": 0,
            "release_consumption_authorized": False,
            "td_c_authorized": False,
        }
        plan = {
            "active_task_count": 1,
            "active_task": subject.FUTURE_TASK_ID,
            "reference_task_id": subject.FUTURE_TASK_ID,
            "contract_id": subject.FORMAL_PACKAGE_B_CONTRACT_ID,
            "executable": True,
            "formal_execution_authority": authority,
        }
        full = {
            "active_task_count": 1,
            "active_task": subject.FUTURE_TASK_ID,
            "current_plan_active_task_count": 1,
            "current_plan_active_task": subject.FUTURE_TASK_ID,
            "active_plan_contract_id": subject.FORMAL_PACKAGE_B_CONTRACT_ID,
            "canonical_next_reference_task": subject.FUTURE_TASK_ID,
            "executable": False,
            "full_is_non_executable_reference": True,
            "release_consumption_authorized": False,
            "device_authorized_by_this_file": False,
            "camera_authorized_by_this_file": False,
            "ray_authorized_by_this_file": False,
            "strip_authorized_by_this_file": False,
            "formal_r6_authorized": False,
            "td_c_authorized": False,
            "g4_06_state": {
                "package": "B_FORMAL_ACQUISITION",
                "contract_id": subject.FORMAL_PACKAGE_B_CONTRACT_ID,
                "authority_owner": "MATCHING_LIVE_PLAN_ONLY",
                "full_top_level_non_authorizing": True,
                "formal_authority_mirror": authority,
                "g4_07_unlocked": False,
            },
        }
        return plan, full

    def commit_package_a_code_descendant(self) -> None:
        path = self.root / subject.ALLOWED_CODE_CHILD_PATHS[1]
        path.write_bytes(path.read_bytes() + b"synthetic-package-a-code-child\n")
        self.git("add", "--", subject.ALLOWED_CODE_CHILD_PATHS[1])
        self.git("commit", "-q", "-m", "feat(stage-gate): route ray r6 formal launch owner")
        self.live_checkpoint = self.git_text("rev-parse", "HEAD")
        self.live_tree = self.git_text("rev-parse", "HEAD^{tree}")

    def commit_machine(self, plan: dict, full: dict, commit_subject: str) -> None:
        (self.root / ".agent-work/PLAN.md").write_bytes(
            machine_row("PLAN_MACHINE_CONTRACT", plan)
        )
        (self.root / ".agent-work/FULL_PLAN_REFERENCE.md").write_bytes(
            machine_row("FULL_PLAN_MACHINE_STATE", full)
        )
        self.git("add", "--", ".agent-work/PLAN.md", ".agent-work/FULL_PLAN_REFERENCE.md")
        self.git("commit", "-q", "-m", commit_subject)
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

    def production_fixture(self, temporary: str, name: str = "production") -> SyntheticGitRepository:
        fixture = SyntheticGitRepository(Path(temporary) / name / "repo")
        fixture.persist_production_package()
        fixture.activate_package_b_machine()
        return fixture

    def package_a_fixture(self, temporary: str, name: str = "package-a") -> SyntheticGitRepository:
        fixture = SyntheticGitRepository(Path(temporary) / name / "repo")
        fixture.persist_production_package()
        fixture.activate_package_a_machine()
        return fixture

    def rewrite_package_json(
        self, fixture: SyntheticGitRepository, name: str, value: dict,
    ) -> None:
        path = fixture.output_root / name
        path.write_bytes(provenance.canonical_json_bytes(value))
        path.chmod(0o600)

    def refresh_terminal_reference(
        self, fixture: SyntheticGitRepository, name: str,
    ) -> None:
        terminal_path = fixture.output_root / "terminal-seal.json"
        terminal = json.loads(terminal_path.read_text(encoding="utf-8"))
        identity = provenance.read_exact_file(
            fixture.output_root / name, expected_mode=0o600,
        )
        terminal["artifacts"][name] = {
            "path": name,
            "bytes": identity.byte_count,
            "sha256": identity.sha256,
            "device": identity.device,
            "inode": identity.inode,
            "mode": identity.mode,
        }
        self.rewrite_package_json(fixture, "terminal-seal.json", terminal)

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

    def test_synthetic_input_binds_activation_and_all_candidate_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.fixture(temporary)
            value = fixture.build_input()
            self.assertEqual(value.source_checkpoint, ACTIVATION_HEAD)
            self.assertEqual(value.source_tree, ACTIVATION_TREE)
            self.assertEqual(
                tuple(item.path for item in value.source_references),
                subject.EXPECTED_SOURCE_PATHS,
            )
            self.assertTrue(all(item.bytes > 0 for item in value.source_references))
            self.assertTrue(all(len(item.sha256) == 64 for item in value.source_references))
            self.assertEqual(
                value.prerequisite_projection["retained_r3_status"],
                subject.RETAINED_R3_STATUS,
            )
            self.assertFalse(
                value.prerequisite_projection["release_consumption_authorized"]
            )

    def test_production_cli_seam_loads_materializes_and_delegates_exactly_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SyntheticGitRepository(Path(temporary) / "repo")
            fixture.persist_production_package()
            fixture.activate_package_b_machine()
            backend = FakeCapableBackend()
            backend_factory = mock.Mock(return_value=backend)
            delegated = mock.Mock(return_value=Path("synthetic-result"))

            result = subject.run_production_cli_launch(
                package_dir=fixture.output_root,
                repo_root=fixture.root,
                code_owner_checkpoint=fixture.code_checkpoint,
                output_dir=Path(subject.FORMAL_ROOT_PARENT),
                run_name=FUTURE_RUN_NAME,
                camera_backend_name="remote",
                camera_backend_kwargs={
                    "env_file": Path("synthetic.env"),
                    "base_url": None,
                    "timeout": 10.0,
                },
                backend_factory=backend_factory,
                delegated_run_fn=delegated,
            )

            self.assertEqual(result, Path("synthetic-result"))
            backend_factory.assert_called_once()
            delegated.assert_called_once()
            runtime = delegated.call_args.args[0]
            self.assertEqual(len(runtime["captures"]), 16)
            self.assertEqual(runtime["budgets"]["logical_cap"], 16)
            self.assertEqual(runtime["budgets"]["physical_cr3_cap"], 16)
            self.assertEqual(runtime["setup_physical_cr3_count"], 0)
            self.assertEqual(runtime["budgets"]["ambient_cap"], 0)
            self.assertEqual(
                [row["state_id"] for row in runtime["captures"]],
                ["A", *(["D"] * 4), "A", *(["B"] * 4), "A", *(["C"] * 4), "A"],
            )
            self.assertTrue(runtime["hard_locks"]["strip_nonzero"])
            backend.connect.assert_not_called()

    def test_planned_subject_real_topology_binds_exact_three_committed_blobs(self):
        planned_subject = "feat(stage-gate): route ray r6 formal launch owner"
        self.assertEqual(subject.ALLOWED_CODE_CHILD_SUBJECT, planned_subject)
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SyntheticGitRepository(Path(temporary) / "planned" / "repo")
            fixture.persist_production_package()
            fixture.activate_package_b_machine()
            attestation = subject.validate_committed_source_attestation(
                fixture.descriptor,
                fixture.activation_probe(),
                repo_root=fixture.root,
            )
            self.assertEqual(
                fixture.git_text("show", "-s", "--format=%s", fixture.code_checkpoint),
                planned_subject,
            )
            self.assertEqual(
                tuple(thermal.changed_paths_between_checkpoints(
                    fixture.source_checkpoint,
                    fixture.code_checkpoint,
                    project_root=fixture.root,
                )),
                subject.ALLOWED_CODE_CHILD_PATHS,
            )
            candidates = fixture.descriptor["committed_source_contract"][
                "allowed_code_owner_child"
            ]["candidate_references"]
            self.assertEqual(len(candidates), 3)
            for reference in candidates:
                blob = subprocess.run(
                    ["git", "show", f"{fixture.code_checkpoint}:{reference['path']}"],
                    cwd=fixture.root,
                    check=True,
                    capture_output=True,
                ).stdout
                self.assertEqual(len(blob), reference["bytes"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), reference["sha256"])
                self.assertEqual(reference["mode"], 0o644)
            self.assertEqual(attestation.code_owner_checkpoint, fixture.code_checkpoint)
            self.assertEqual(attestation.live_activation_checkpoint, fixture.live_checkpoint)
            self.assertEqual(len(attestation.post_child_commits), 1)
            self.assertEqual(
                tuple(attestation.post_child_commits[0]["changed_paths"]),
                (".agent-work/FULL_PLAN_REFERENCE.md", ".agent-work/PLAN.md"),
            )

    def test_legacy_subject_with_identical_code_tree_fails_before_backend(self):
        legacy_subject = "feat(stage-gate): accept ray r6 launch owner"
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SyntheticGitRepository(Path(temporary) / "legacy" / "repo")
            planned_checkpoint = fixture.code_checkpoint
            legacy_checkpoint = fixture.commit_tree(
                fixture.code_tree,
                (fixture.source_checkpoint,),
                legacy_subject,
            )
            self.assertEqual(
                fixture.git_text("rev-parse", f"{planned_checkpoint}^{{tree}}"),
                fixture.git_text("rev-parse", f"{legacy_checkpoint}^{{tree}}"),
            )
            fixture.set_head(legacy_checkpoint)
            fixture.code_checkpoint = legacy_checkpoint
            fixture.persist_production_package()
            fixture.activate_package_b_machine()
            factory = mock.Mock()
            delegated = mock.Mock()
            with self.assertRaisesRegex(
                subject.StageGateError, "committed_source_subject_drift",
            ):
                subject.run_production_cli_launch(
                    package_dir=fixture.output_root,
                    repo_root=fixture.root,
                    code_owner_checkpoint=fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=delegated,
                )
            factory.assert_not_called()
            delegated.assert_not_called()

    def test_package_a_engineering_machine_state_is_not_production_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.package_a_fixture(temporary)
            factory = mock.Mock()
            delegated = mock.Mock()
            with self.assertRaisesRegex(
                subject.StageGateError, "production_machine_contract_drift",
            ):
                subject.run_production_cli_launch(
                    package_dir=fixture.output_root,
                    repo_root=fixture.root,
                    code_owner_checkpoint=fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=delegated,
                )
            factory.assert_not_called()
            delegated.assert_not_called()

    def test_formal_machine_authority_matrix_is_closed_and_pre_backend(self):
        def plan_authority(name: str, value: object):
            return lambda plan, _full: plan["formal_execution_authority"].__setitem__(name, value)

        def mirrored_authority(name: str, value: object):
            def mutate(plan: dict, full: dict) -> None:
                plan["formal_execution_authority"][name] = value
                full["g4_06_state"]["formal_authority_mirror"][name] = value
            return mutate

        cases = {
            "plan_formal_false": plan_authority("formal_execution_authorized", False),
            "plan_device_false": plan_authority("device_control_authorized", False),
            "plan_camera_false": plan_authority("camera_authorized", False),
            "plan_ray_false": plan_authority("ray_authorized", False),
            "plan_capture_false": plan_authority("capture_authorized", False),
            "plan_source_drift": plan_authority("source", "strip"),
            "plan_backend_drift": plan_authority("camera_backend", "local"),
            "plan_not_executable": lambda plan, _full: plan.__setitem__(
                "executable", False,
            ),
            "authority_missing": lambda plan, _full: plan["formal_execution_authority"].pop("capture_authorized"),
            "authority_extra": lambda plan, _full: plan["formal_execution_authority"].__setitem__("extra", False),
            "mirror_authority_missing": lambda _plan, full: full["g4_06_state"]["formal_authority_mirror"].pop("capture_authorized"),
            "mirror_authority_extra": lambda _plan, full: full["g4_06_state"]["formal_authority_mirror"].__setitem__("extra", False),
            "package_a_contract_with_authority": lambda plan, full: (
                plan.__setitem__("contract_id", subject.ENGINEERING_PACKAGE_A_CONTRACT_ID),
                full.__setitem__("active_plan_contract_id", subject.ENGINEERING_PACKAGE_A_CONTRACT_ID),
                full["g4_06_state"].__setitem__("contract_id", subject.ENGINEERING_PACKAGE_A_CONTRACT_ID),
            ),
            "third_contract": lambda plan, full: (
                plan.__setitem__("contract_id", "G4-RAY-R6-THIRD-CONTRACT"),
                full.__setitem__("active_plan_contract_id", "G4-RAY-R6-THIRD-CONTRACT"),
                full["g4_06_state"].__setitem__("contract_id", "G4-RAY-R6-THIRD-CONTRACT"),
            ),
            "plan_full_contract_mismatch": lambda _plan, full: full.__setitem__(
                "active_plan_contract_id", subject.ENGINEERING_PACKAGE_A_CONTRACT_ID,
            ),
            "full_mirror_mismatch": lambda _plan, full: full["g4_06_state"].__setitem__(
                "package", "A_ENGINEERING",
            ),
            "full_claims_device_authority": lambda _plan, full: full.__setitem__(
                "device_authorized_by_this_file", True,
            ),
            "full_claims_formal_authority": lambda _plan, full: full.__setitem__(
                "formal_r6_authorized", True,
            ),
            "full_claims_executable": lambda _plan, full: full.__setitem__(
                "executable", True,
            ),
            "full_drops_non_authorizing_lock": lambda _plan, full: full.__setitem__(
                "full_is_non_executable_reference", False,
            ),
            "wrong_task": lambda plan, full: (
                plan.__setitem__("active_task", "REF-WRONG"),
                full.__setitem__("active_task", "REF-WRONG"),
            ),
            "wrong_count": lambda plan, full: (
                plan.__setitem__("active_task_count", 0),
                full.__setitem__("active_task_count", 0),
            ),
            "wrong_canonical_next": lambda _plan, full: full.__setitem__(
                "canonical_next_reference_task", "REF-WRONG",
            ),
            "wrong_current_plan_task": lambda _plan, full: full.__setitem__(
                "current_plan_active_task", "REF-WRONG",
            ),
            "wrong_current_plan_count": lambda _plan, full: full.__setitem__(
                "current_plan_active_task_count", 0,
            ),
            "retry_expansion": mirrored_authority("retry", 1),
            "launch_expansion": mirrored_authority("launch_cap", 2),
            "logical_expansion": mirrored_authority("logical_capture_cap", 17),
            "physical_expansion": mirrored_authority("physical_cr3_cap", 17),
            "root_expansion": mirrored_authority("formal_root_parent", "/synthetic/other"),
            "strip_expansion": mirrored_authority("strip_authorized", True),
            "release_expansion": mirrored_authority("release_consumption_authorized", True),
            "td_c_expansion": mirrored_authority("td_c_authorized", True),
        }
        with tempfile.TemporaryDirectory() as temporary:
            for index, (name, mutate) in enumerate(cases.items()):
                with self.subTest(name=name):
                    fixture = self.production_fixture(
                        temporary, f"matrix-{index:02d}",
                    )
                    plan, full = fixture.package_b_machine_values()
                    mutate(plan, full)
                    (fixture.root / ".agent-work/PLAN.md").write_bytes(
                        machine_row("PLAN_MACHINE_CONTRACT", plan)
                    )
                    (fixture.root / ".agent-work/FULL_PLAN_REFERENCE.md").write_bytes(
                        machine_row("FULL_PLAN_MACHINE_STATE", full)
                    )
                    factory = mock.Mock()
                    delegated = mock.Mock()
                    with self.assertRaisesRegex(
                        subject.StageGateError, "production_machine_contract_drift",
                    ):
                        subject.run_production_cli_launch(
                            package_dir=fixture.output_root,
                            repo_root=fixture.root,
                            code_owner_checkpoint=fixture.code_checkpoint,
                            output_dir=Path(subject.FORMAL_ROOT_PARENT),
                            run_name=FUTURE_RUN_NAME,
                            camera_backend_name="remote",
                            camera_backend_kwargs={
                                "env_file": Path("synthetic.env"),
                                "base_url": None,
                                "timeout": 10.0,
                            },
                            backend_factory=factory,
                            delegated_run_fn=delegated,
                        )
                    factory.assert_not_called()
                    delegated.assert_not_called()

    def test_old_descriptor_does_not_promote_later_package_a_code_child(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SyntheticGitRepository(Path(temporary) / "source-bound" / "repo")
            fixture.persist_production_package()
            fixture.commit_package_a_code_descendant()
            fixture.activate_package_b_machine()
            old_descriptor = deepcopy(fixture.descriptor)
            old_descriptor["committed_source_contract"]["allowed_code_owner_child"][
                "subject"
            ] = "feat(stage-gate): accept ray r6 launch owner"
            with self.assertRaisesRegex(
                subject.StageGateError,
                "committed_source_descriptor_semantic_drift",
            ):
                subject.validate_committed_source_attestation(
                    old_descriptor,
                    fixture.activation_probe(),
                    repo_root=fixture.root,
                )
            factory = mock.Mock()
            delegated = mock.Mock()
            with self.assertRaisesRegex(subject.StageGateError, "source_reference_drift"):
                subject.run_production_cli_launch(
                    package_dir=fixture.output_root,
                    repo_root=fixture.root,
                    code_owner_checkpoint=fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=delegated,
                )
            factory.assert_not_called()
            delegated.assert_not_called()

    def test_measure_cli_routes_exact_stage_gate_chain_and_rejects_generic_bypass(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.production_fixture(temporary)
            backend = FakeCapableBackend()
            backend_factory = mock.Mock(return_value=backend)
            delegated = mock.Mock(return_value=Path("synthetic-cli-result"))
            argv = [
                "--experiment-id", thermal.TD_B,
                "--source", "ray",
                "--phase", "formal",
                "--execute",
                "--allow-device-control",
                "--code-checkpoint", fixture.code_checkpoint,
                "--output-dir", subject.FORMAL_ROOT_PARENT,
                "--run-name", FUTURE_RUN_NAME,
                "--stage-gate-package", str(fixture.output_root),
            ]

            self.assertEqual(
                measure.main(
                    argv,
                    backend_factory=backend_factory,
                    run_fn=delegated,
                    repo_root=fixture.root,
                ),
                0,
            )
            backend_factory.assert_called_once()
            delegated.assert_called_once()
            backend.connect.assert_not_called()

            bypass_factory = mock.Mock()
            with self.assertRaisesRegex(
                PermissionError, "requires --stage-gate-package",
            ):
                measure.main(
                    [item for item in argv if item not in {
                        "--stage-gate-package", str(fixture.output_root),
                    }],
                    backend_factory=bypass_factory,
                    run_fn=mock.Mock(),
                    repo_root=fixture.root,
                )
            bypass_factory.assert_not_called()

    def test_production_package_integrity_precedes_semantics_and_backend_factory(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = self.production_fixture(temporary, "integrity")
            descriptor_path = fixture.output_root / "launch-descriptor.json"
            descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
            descriptor["secret_note"] = "credential"
            self.rewrite_package_json(
                fixture, "launch-descriptor.json", descriptor,
            )
            factory = mock.Mock()
            with self.assertRaisesRegex(subject.StageGateError, "artifact_identity_drift"):
                subject.run_production_cli_launch(
                    package_dir=fixture.output_root,
                    repo_root=fixture.root,
                    code_owner_checkpoint=fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=mock.Mock(),
                )
            factory.assert_not_called()

            historical = self.production_fixture(temporary, "historical")
            historical_descriptor = json.loads(
                (historical.output_root / "launch-descriptor.json").read_text(
                    encoding="utf-8"
                )
            )
            historical_descriptor["historical_payload"] = "retained-r3"
            self.rewrite_package_json(
                historical, "launch-descriptor.json", historical_descriptor,
            )
            self.refresh_terminal_reference(historical, "launch-descriptor.json")
            historical_factory = mock.Mock()
            with self.assertRaisesRegex(subject.StageGateError, "historical_input_prohibited"):
                subject.run_production_cli_launch(
                    package_dir=historical.output_root,
                    repo_root=historical.root,
                    code_owner_checkpoint=historical.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=historical_factory,
                    delegated_run_fn=mock.Mock(),
                )
            historical_factory.assert_not_called()

            self.refresh_terminal_reference(fixture, "launch-descriptor.json")
            with self.assertRaisesRegex(subject.StageGateError, "secret_material_prohibited"):
                subject.run_production_cli_launch(
                    package_dir=fixture.output_root,
                    repo_root=fixture.root,
                    code_owner_checkpoint=fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=mock.Mock(),
                )
            factory.assert_not_called()

    def test_production_inventory_machine_and_delegate_failures_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            extra = self.production_fixture(temporary, "extra")
            (extra.output_root / "unexpected.json").write_text("{}", encoding="utf-8")
            (extra.output_root / "unexpected.json").chmod(0o600)
            factory = mock.Mock()
            common = {
                "repo_root": extra.root,
                "code_owner_checkpoint": extra.code_checkpoint,
                "output_dir": Path(subject.FORMAL_ROOT_PARENT),
                "run_name": FUTURE_RUN_NAME,
                "camera_backend_name": "remote",
                "camera_backend_kwargs": {
                    "env_file": Path("synthetic.env"),
                    "base_url": None,
                    "timeout": 10.0,
                },
                "backend_factory": factory,
                "delegated_run_fn": mock.Mock(),
            }
            with self.assertRaisesRegex(subject.StageGateError, "artifact_inventory_drift"):
                subject.run_production_cli_launch(
                    package_dir=extra.output_root, **common,
                )
            factory.assert_not_called()

            machine = self.production_fixture(temporary, "machine")
            (machine.root / ".agent-work/PLAN.md").write_bytes(
                machine_row("PLAN_MACHINE_CONTRACT", {
                    "active_task_count": 0,
                    "active_task": None,
                    "reference_task_id": subject.FUTURE_TASK_ID,
                    "contract_id": subject.FORMAL_PACKAGE_B_CONTRACT_ID,
                    "formal_execution_authority": {},
                })
            )
            factory = mock.Mock()
            with self.assertRaisesRegex(subject.StageGateError, "production_machine_contract_drift"):
                subject.run_production_cli_launch(
                    package_dir=machine.output_root,
                    repo_root=machine.root,
                    code_owner_checkpoint=machine.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=mock.Mock(),
                )
            factory.assert_not_called()

            delegated_fixture = self.production_fixture(temporary, "delegate")
            backend = FakeCapableBackend()
            factory = mock.Mock(return_value=backend)
            delegated = mock.Mock(side_effect=RuntimeError("synthetic delegate failure"))
            with self.assertRaisesRegex(RuntimeError, "synthetic delegate failure"):
                subject.run_production_cli_launch(
                    package_dir=delegated_fixture.output_root,
                    repo_root=delegated_fixture.root,
                    code_owner_checkpoint=delegated_fixture.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=delegated,
                )
            factory.assert_called_once()
            delegated.assert_called_once()
            backend.connect.assert_not_called()

    def test_production_source_and_machine_parser_drift_precede_backend_factory(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = self.production_fixture(temporary, "source")
            factory = mock.Mock()
            with self.assertRaisesRegex(
                subject.StageGateError, "committed_source_parent_drift",
            ):
                subject.run_production_cli_launch(
                    package_dir=source.output_root,
                    repo_root=source.root,
                    code_owner_checkpoint=source.live_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=mock.Mock(),
                )
            factory.assert_not_called()

            duplicate = self.production_fixture(temporary, "duplicate")
            plan_path = duplicate.root / ".agent-work/PLAN.md"
            plan_path.write_bytes(plan_path.read_bytes() + plan_path.read_bytes())
            factory = mock.Mock()
            with self.assertRaisesRegex(
                subject.StageGateError, "production_machine_contract_invalid",
            ):
                subject.run_production_cli_launch(
                    package_dir=duplicate.output_root,
                    repo_root=duplicate.root,
                    code_owner_checkpoint=duplicate.code_checkpoint,
                    output_dir=Path(subject.FORMAL_ROOT_PARENT),
                    run_name=FUTURE_RUN_NAME,
                    camera_backend_name="remote",
                    camera_backend_kwargs={
                        "env_file": Path("synthetic.env"),
                        "base_url": None,
                        "timeout": 10.0,
                    },
                    backend_factory=factory,
                    delegated_run_fn=mock.Mock(),
                )
            factory.assert_not_called()

    def test_stage_gate_cli_rejects_extra_or_inexact_combinations_before_dispatch(self):
        absolute_package = Path("/synthetic/stage-gate-package")
        base = [
            "--experiment-id", thermal.TD_B,
            "--source", "ray",
            "--phase", "formal",
            "--execute",
            "--allow-device-control",
            "--code-checkpoint", "1" * 40,
            "--output-dir", subject.FORMAL_ROOT_PARENT,
            "--run-name", FUTURE_RUN_NAME,
            "--stage-gate-package", str(absolute_package),
        ]
        cases = {
            "relative_package": [
                *base[:-1], "relative-package",
            ],
            "human_gate_injection": [
                *base, "--human-authorization", thermal.TD_B,
            ],
            "parallel_release": [
                *base, "--setup-release", "/synthetic/release.json",
            ],
            "variant_expansion": [
                *base, "--variant", "expansion",
            ],
            "remote_override": [
                *base, "--remote-base-url", "http://127.0.0.1:1",
            ],
        }
        for name, argv in cases.items():
            with self.subTest(name=name):
                factory = mock.Mock()
                launch = mock.Mock()
                with self.assertRaisesRegex(
                    PermissionError, "exact stage-gate CLI contract",
                ):
                    measure.main(
                        argv,
                        backend_factory=factory,
                        g4_r6_launch_fn=launch,
                    )
                factory.assert_not_called()
                launch.assert_not_called()

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
