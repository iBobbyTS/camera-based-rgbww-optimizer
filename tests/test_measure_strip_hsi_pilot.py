from __future__ import annotations

import json
import hashlib
import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from camera_based_rgbww_optimizer.control.all_off import ShutdownStep
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import analyze_strip_hsi_pilot
from camera_based_rgbww_optimizer.optimization import measure_strip_hsi_pilot as subject


class MeasureStripHsiPilotTests(unittest.TestCase):
    def test_dry_run_writes_validation_without_env_network_or_device_calls(self):
        with tempfile.TemporaryDirectory(dir=subject.PROJECT_TMP_DIR) as tempdir:
            with (
                mock.patch.object(subject.camera_remote, "create_camera_backend") as backend,
                mock.patch.object(subject.esphome, "light") as strip_light,
                mock.patch.object(subject.ray120c, "set_hsi") as ray_light,
                mock.patch.object(subject.all_off, "turn_everything_off") as shutdown,
            ):
                result = subject.main([
                    "--dry-run",
                    "--policy-version", "v1",
                    "--target-set", "sentinel",
                    "--camera-backend", "remote",
                    "--output-dir", tempdir,
                    "--run-name", "offline",
                ])

            root = Path(tempdir) / "offline"
            plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
            validation = json.loads((root / "uncertainty-validation.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["measurement"]["target_set"], "sentinel")
        self.assertEqual(validation["status"], "pass")
        self.assertFalse(validation["device_calls_performed"])
        backend.assert_not_called()
        strip_light.assert_not_called()
        ray_light.assert_not_called()
        shutdown.assert_not_called()

    def test_plan_freezes_gate5_basis_location_and_13_targets(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            uncertainty = _uncertainty_file(root)
            plan = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty, policy_version="v1",
            )
            parent = root / "sentinel-analysis.json"
            parent.write_text("{}", encoding="utf-8")
            remaining = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty,
                policy_version="v1",
                target_set="remaining",
                parent_analysis_path=parent,
            )

        self.assertEqual(plan["measurement"]["phase"], "P7-pilot")
        self.assertEqual(plan["measurement"]["branch"], "full_periodic_2d_HB")
        self.assertEqual(len(plan["targets"]), 4)
        self.assertEqual(plan["measurement"]["target_set"], "sentinel")
        self.assertEqual(len(plan["measurement"]["coordinate_feature_ids"]), 58)
        self.assertEqual(plan["inputs"]["location_config"]["sha256"], subject.LATEST_LOCATION_SHA256)
        self.assertEqual(plan["inputs"]["basis_analysis"]["sha256"], subject.FROZEN_BASIS_SHA256)
        self.assertEqual(plan["inputs"]["ray_hsi_manifold"]["sha256"], subject.FROZEN_MANIFOLD_SHA256)
        self.assertTrue(all(max(target["seed"]["best"]["command"].values()) == 4095 for target in plan["targets"]))
        combined = {(item["hue"], item["sat"]) for item in [*plan["targets"], *remaining["targets"]]}
        self.assertEqual(len(combined), 13)
        self.assertEqual(len(remaining["targets"]), 9)

    def test_boundary_plan_freezes_five_confirmations_and_scale_relaxed_max_codes(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            uncertainty = _uncertainty_file(root)
            parent = root / "combined-analysis.json"
            parent.write_text("{}", encoding="utf-8")
            targets = root / "boundary-targets.json"
            targets.write_text(json.dumps({"targets": [
                {"hue": 60, "sat": 75, "max_code": 4095},
                {"hue": 90, "sat": 70, "max_code": 3072},
                {"hue": 150, "sat": 65, "max_code": 2048},
            ]}), encoding="utf-8")

            plan = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty,
                policy_version="v1",
                target_set="boundary",
                parent_analysis_path=parent,
                target_file_path=targets,
            )

        self.assertEqual([item["max_code"] for item in plan["targets"]], [4095, 3072, 2048])
        self.assertEqual([item["confirmation_count"] for item in plan["targets"]], [5, 5, 5])
        self.assertTrue(all(max(item["seed"]["best"]["command"].values()) == item["max_code"] for item in plan["targets"]))

    def test_v1_formal_execution_is_hard_rejected_as_replay_only(self):
        with tempfile.TemporaryDirectory() as tempdir:
            uncertainty = _uncertainty_file(Path(tempdir))
            plan = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty, policy_version="v1",
            )
            with self.assertRaisesRegex(ValueError, "v1 is replay-only"):
                subject.execute_strip_hsi_pilot_plan(
                    plan, run_dir=Path(tempdir) / "run",
                    capture_step_fn=mock.Mock(), strip_light_fn=mock.Mock(),
                    ray_off_fn=mock.Mock(), sleep_fn=lambda _seconds: None,
                )

    def test_shell_wrapper_has_double_cleanup_and_fixed_project_cwd(self):
        wrapper = (Path(__file__).parents[1] / "tmp" / "run-strip-hsi-pilot.zsh").read_text(encoding="utf-8")

        self.assertIn('cd "$PROJECT_ROOT"', wrapper)
        self.assertIn("trap cleanup EXIT", wrapper)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off", wrapper)
        self.assertIn("--camera-backend remote", wrapper)

    def test_v2_waiting_policy_is_rejected_before_formal_plan(self):
        with self.assertRaisesRegex(ValueError, "waiting/candidate"):
            subject.build_strip_hsi_pilot_plan(policy_version="v2")

    def test_ordinary_budget_declares_exact_54_logical_and_67_physical_caps(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            uncertainty = _uncertainty_file(root)
            plan = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty, policy_version="v1",
            )
        self.assertTrue(all(item["solver_budget"]["max_logical_observations_per_target"] == 54 for item in plan["targets"]))
        self.assertTrue(all(item["solver_budget"]["max_physical_cr3_per_target"] == 67 for item in plan["targets"]))

    def test_n5_budget_declares_exact_62_logical_and_75_physical_caps(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            uncertainty = _uncertainty_file(root)
            combined_path = root / "combined.json"
            combined_path.write_text("{}", encoding="utf-8")
            target_file = root / "boundary-targets.json"
            target_file.write_text(json.dumps({"targets": [{"hue": 90, "sat": 75, "max_code": 4095}]}), encoding="utf-8")
            plan = subject.build_strip_hsi_pilot_plan(
                uncertainty_config_path=uncertainty, policy_version="v1",
                target_set="boundary", parent_analysis_path=combined_path,
                target_file_path=target_file,
            )
        self.assertEqual(plan["targets"][0]["solver_budget"]["max_logical_observations_per_target"], 62)
        self.assertEqual(plan["targets"][0]["solver_budget"]["max_physical_cr3_per_target"], 75)

    def test_v2_formal_runner_dispatches_evaluator_multiseed_status_and_repeat_blocks(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(
                policy_version="v2", policy_v2_config_path=policy,
            )
            run_root = root / "run"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            anchors = [json.loads(line) for line in (run_root / "reference-anchors.jsonl").read_text(encoding="utf-8").splitlines()]
            analysis = analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(
                run_root, policy_version="v2",
            )
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(anchors), 12)
        self.assertTrue(all(row["result_status"] == "faithful" for row in rows))
        self.assertTrue(all(row["feedback"]["kind"] == "hsi_bounded_multiseed_feedback_v2" for row in rows))
        self.assertTrue(all(row["feedback"]["budget_declaration"]["max_logical_observations_per_target"] == 54 for row in rows))
        self.assertTrue(all(row["physical_budget"]["physical_cr3_used"] <= 67 for row in rows))
        self.assertEqual(analysis["policy_version"], "v2")
        self.assertEqual(analysis["point_count"], 4)
        self.assertEqual(analysis["anchor_validation"]["anchor_count"], 12)
        self.assertEqual(analysis["target_evidence_validation"]["three_layer_result_audit"], "pass")
        self.assertEqual(analysis["target_evidence_validation"]["budget_audit"], "pass")

    def test_v2_analyzer_rejects_waiting_policy_hash_cleanup_and_confirmation_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(
                policy_version="v2", policy_v2_config_path=policy,
            )
            run_root = root / "run"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            (run_root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": False}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cleanup"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            _write_shell_cleanup(run_root)
            saved_plan = json.loads((run_root / "plan.json").read_text(encoding="utf-8"))
            waiting = subject.DEFAULT_POLICY_V2_CONFIG
            waiting_plan = json.loads(json.dumps(saved_plan))
            waiting_plan["inputs"]["policy_v2_artifact"] = {
                "path": str(waiting),
                "sha256": hashlib.sha256(waiting.read_bytes()).hexdigest(),
            }
            (run_root / "plan.json").write_text(json.dumps(waiting_plan), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen formal-eligible"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            drift_plan = json.loads(json.dumps(saved_plan))
            drift_plan["inputs"]["policy_v2_artifact"]["sha256"] = "0" * 64
            (run_root / "plan.json").write_text(json.dumps(drift_plan), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            (run_root / "plan.json").write_text(json.dumps(saved_plan), encoding="utf-8")
            saved_commands = (run_root / "commands.jsonl").read_text(encoding="utf-8")
            command_rows = [json.loads(line) for line in saved_commands.splitlines()]
            command_rows.pop(0)
            (run_root / "commands.jsonl").write_text("\n".join(json.dumps(item) for item in command_rows) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source isolation"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            (run_root / "commands.jsonl").write_text(saved_commands, encoding="utf-8")
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            confirmed = next(
                item for item in rows[0]["feedback"]["selected_result"]["confirmation_attempts"]
                if item["status"] == "confirmed"
            )
            confirmed["sample_indices"] = confirmed["sample_indices"][:-1]
            rows[0]["feedback"]["attempts"][
                rows[0]["feedback"]["selected_start_index"]
            ]["result"] = rows[0]["feedback"]["selected_result"]
            (run_root / "target-results.jsonl").write_text(
                "\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "confirmed group size"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_analyzer_reconstructs_counts_status_and_frozen_anchor_truth(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            run_root = root / "run"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            original = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]

            def write_rows(rows):
                (run_root / "target-results.jsonl").write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")

            rows = copy.deepcopy(original)
            selected = rows[0]["feedback"]["selected_result"]
            rows[0]["feedback"]["logical_observations_used"] = 0
            selected["budget"]["logical_observations_used"] = 0
            selected["budget"]["consumed"] = {key: 0 for key in selected["budget"]["consumed"]}
            rows[0]["feedback"]["attempts"][rows[0]["feedback"]["selected_start_index"]]["result"] = selected
            rows[0]["physical_budget"]["physical_cr3_used"] = 0
            write_rows(rows)
            with self.assertRaisesRegex(ValueError, "logical ledger|raw evidence|physical ledger"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            rows = copy.deepcopy(original)
            rows[0]["result_status"] = rows[0]["gamut_status"] = "unconfirmed"
            write_rows(rows)
            with self.assertRaisesRegex(ValueError, "result status"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            write_rows(original)

            commands = [json.loads(line) for line in (run_root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            anchor = next(item for item in commands if item["event"] == "ray_on_readback_verified")
            anchor["expected"]["hue"] = anchor["readback"]["data"]["hue"] = 1
            (run_root / "commands.jsonl").write_text("\n".join(json.dumps(item) for item in commands) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen plan"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_analyzer_rejects_start_limits_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            run_root = root / "limits"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            budget = rows[0]["feedback"]["selected_result"]["budget"]
            budget["limits"]["max_feedback_capture_attempts_per_start"] += 1
            rows[0]["feedback"]["attempts"][0]["result"] = rows[0]["feedback"]["selected_result"]
            (run_root / "target-results.jsonl").write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "budget limits differ from frozen solver budget"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_public_analyzer_rejects_asymmetric_exhaustion_ledgers(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            cases = ("nested-only", "top-only", "mismatch", "nested-empty", "confirmed-with-exhaustion", "status-without-ledgers")
            for case in cases:
                run_root = root / case
                _execute_fake_v2_plan(plan, run_root)
                _write_shell_cleanup(run_root)
                rows_path = run_root / "target-results.jsonl"
                rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
                feedback = rows[0]["feedback"]
                selected = feedback["selected_result"]
                ledger = {"status": "solver_budget_exhausted", "case": case}
                if case == "nested-only":
                    selected["budget"]["exhaustion"] = ledger
                elif case == "top-only":
                    selected["budget_exhaustion"] = ledger
                elif case == "mismatch":
                    selected["budget_exhaustion"] = ledger
                    selected["budget"]["exhaustion"] = {**ledger, "case": "different"}
                elif case == "nested-empty":
                    selected["budget"]["exhaustion"] = {}
                elif case == "confirmed-with-exhaustion":
                    selected["budget_exhaustion"] = ledger
                    selected["budget"]["exhaustion"] = ledger
                else:
                    selected["status"] = "solver_budget_exhausted"
                    selected["goal_confirmed"] = False
                feedback["attempts"][feedback["selected_start_index"]]["result"] = selected
                rows_path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
                with self.subTest(case=case), self.assertRaisesRegex(ValueError, "exhaustion"):
                    analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_public_analyzer_accepts_five_frozen_category_exhaustions(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            categories = {
                "initial": ["initial"],
                "initial_probes": [f"probe-{index}" for index in range(4)],
                "feedback_attempts": [f"feedback-{index}" for index in range(8)],
                "rebase_probes": [f"rebase-{index // 4}-probe-{index % 4}" for index in range(8)],
                "confirmation_captures": [f"confirm-{index // 3}-{index % 3}" for index in range(6)],
            }
            for category, phases in categories.items():
                run_root = root / category
                _execute_fake_v2_plan(plan, run_root)
                _write_shell_cleanup(run_root)
                _append_fake_exhausted_start(run_root, plan, category=category, phases=phases)
                analysis = analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
                self.assertEqual(analysis["status"], "ready_for_sentinel_branch")

    def test_v2_public_analyzer_rejects_category_under_over_and_phase_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            cases = {
                "one-under": [f"feedback-{index}" for index in range(7)],
                "one-over": [f"feedback-{index}" for index in range(9)],
                "wrong-phase": [f"feedback-{index}" for index in range(8)],
                "wrong-sub-budget": [f"feedback-{index}" for index in range(8)],
            }
            for case, phases in cases.items():
                run_root = root / case
                _execute_fake_v2_plan(plan, run_root)
                _write_shell_cleanup(run_root)
                _append_fake_exhausted_start(run_root, plan, category="feedback_attempts", phases=phases)
                if case.startswith("wrong-"):
                    rows_path = run_root / "target-results.jsonl"
                    rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
                    result = rows[0]["feedback"]["attempts"][1]["result"]
                    if case == "wrong-phase":
                        result["budget_exhaustion"]["phase"] = "probe-next"
                    else:
                        result["budget_exhaustion"]["sub_budget"] = "initial_probes"
                    result["budget"]["exhaustion"] = copy.deepcopy(result["budget_exhaustion"])
                    rows_path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
                with self.subTest(case=case), self.assertRaisesRegex(ValueError, "category|exhaustion"):
                    analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_analyzer_rejects_duplicate_capture_and_auto_audit_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            run_root = root / "duplicate"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            selected = rows[0]["feedback"]["selected_result"]
            selected["samples"][1]["observation"]["capture_id"] = selected["samples"][0]["observation"]["capture_id"]
            rows[0]["feedback"]["attempts"][rows[0]["feedback"]["selected_start_index"]]["result"] = selected
            (run_root / "target-results.jsonl").write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate|provenance"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            run_root = root / "auto"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            captures = [json.loads(line) for line in (run_root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            auto = next(item for item in captures if item.get("target_index") is not None and item.get("capture", {}).get("auto_exposure_audit"))
            auto["capture"]["auto_exposure_audit"]["capture_count"] = 2
            (run_root / "captures.jsonl").write_text("\n".join(json.dumps(item) for item in captures) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "audit structure"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_analyzer_replays_objective_and_requires_confirmed_group(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)

            run_root = root / "objective"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows_path = run_root / "target-results.jsonl"
            original = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
            tampered = copy.deepcopy(original)
            sample = tampered[0]["feedback"]["selected_result"]["samples"][0]
            sample["objective"]["observer_equivalent"] = not bool(sample["objective"]["observer_equivalent"])
            tampered[0]["feedback"]["attempts"][0]["result"] = tampered[0]["feedback"]["selected_result"]
            rows_path.write_text("\n".join(json.dumps(item) for item in tampered) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "objective differs from RAW replay"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            run_root = root / "no-confirmed-group"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            selected = rows[0]["feedback"]["selected_result"]
            for group in selected["confirmation_attempts"]:
                group["status"] = "failed"
                group["partial_group"] = False
            selected["goal_confirmed"] = True
            selected["status"] = "goal_confirmed"
            rows[0]["feedback"]["attempts"][rows[0]["feedback"]["selected_start_index"]]["result"] = selected
            rows_path = run_root / "target-results.jsonl"
            rows_path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "failed group lacks a failed sample|confirmation status differs from replayed samples"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            run_root = root / "row-cap"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows = [json.loads(line) for line in (run_root / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
            rows[0]["physical_budget"]["autoexposure_cap"] = 9999
            (run_root / "target-results.jsonl").write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "physical frozen sub-budget drift"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

    def test_v2_analyzer_rejects_empty_and_malformed_measurement_rejections(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)

            for label, evidence in (
                ("empty", {}),
                ("missing-capture-ids", {"source": "strip", "purpose": "candidate_feedback-0", "exposure_factors": [1.0], "rejected_features": [{"status": "weak"}]}),
                ("empty-capture-ids", {"source": "strip", "purpose": "candidate_feedback-0", "capture_ids": [], "exposure_factors": [1.0], "rejected_features": [{"status": "weak"}]}),
                ("fake-pre-capture", {"pre_capture_exhaustion": True, "status": "solver_budget_exhausted", "capture_ids": ["capture-0"]}),
            ):
                run_root = root / label
                _execute_fake_v2_plan(plan, run_root)
                _write_shell_cleanup(run_root)
                rows_path = run_root / "target-results.jsonl"
                rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
                selected = rows[0]["feedback"]["selected_result"]
                sample = selected["samples"][0]
                selected["measurement_rejections"].append({
                    "phase": "feedback-0", "command": sample["command"], "evidence": evidence,
                })
                selected["budget"]["consumed"]["feedback_attempts"] += 1
                selected["budget"]["logical_observations_used"] += 1
                rows[0]["feedback"]["logical_observations_used"] += 1
                rows[0]["feedback"]["attempts"][rows[0]["feedback"]["selected_start_index"]]["result"] = selected
                rows_path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
                with self.subTest(label=label), self.assertRaisesRegex(ValueError, "rejection|exhaustion"):
                    analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            valid_exhaustion = {
                "pre_capture_exhaustion": True,
                "status": "solver_budget_exhausted",
                "sub_budget": "logical_observations",
                "phase": "feedback-0",
                "requested_physical_cr3": 0,
                "physical_cr3_used": 12,
                "autoexposure_physical_cr3_used": 0,
                "weak_reacquire_physical_cr3_used": 0,
                "capture_attempted": False,
                "start_index": 0,
            }
            analyze_strip_hsi_pilot._validate_pre_capture_exhaustion(
                valid_exhaustion, target_key=(0, 0), expected_start_index=0,
                expected_counters={
                    "physical_cr3_used": 12,
                    "autoexposure_physical_cr3_used": 0,
                    "weak_reacquire_physical_cr3_used": 0,
                },
                expected_budget={
                    "exhaustion": valid_exhaustion,
                    "consumed": {"initial": 1, "initial_probes": 4, "feedback_attempts": 8, "rebase_probes": 8, "confirmation_captures": 6},
                    "limits": {
                        "rebase_probe_count": 4,
                        "max_rebases_per_start": 2,
                        "max_feedback_capture_attempts_per_start": 8,
                        "max_confirmation_groups_per_start": 2,
                        "confirmation_captures_per_group": 3,
                    },
                },
            )
            for field in ("phase", "physical_cr3_used", "autoexposure_physical_cr3_used", "weak_reacquire_physical_cr3_used"):
                tampered = copy.deepcopy(valid_exhaustion)
                tampered[field] = "tampered" if field == "phase" else int(tampered[field]) + 1
                with self.subTest(exhaustion_field=field), self.assertRaises(ValueError):
                    analyze_strip_hsi_pilot._validate_pre_capture_exhaustion(
                        tampered, target_key=(0, 0), expected_start_index=0,
                        expected_counters={
                            "physical_cr3_used": 12,
                            "autoexposure_physical_cr3_used": 0,
                            "weak_reacquire_physical_cr3_used": 0,
                        },
                        expected_budget={
                            "exhaustion": valid_exhaustion,
                            "consumed": {"initial": 1, "initial_probes": 4, "feedback_attempts": 8, "rebase_probes": 8, "confirmation_captures": 6},
                            "limits": {
                                "rebase_probe_count": 4,
                                "max_rebases_per_start": 2,
                                "max_feedback_capture_attempts_per_start": 8,
                                "max_confirmation_groups_per_start": 2,
                                "confirmation_captures_per_group": 3,
                            },
                        },
                    )
            with self.assertRaises(ValueError):
                analyze_strip_hsi_pilot._validate_pre_capture_exhaustion(
                    {**valid_exhaustion, "capture_ids": ["already-captured"]},
                    target_key=(0, 0), expected_start_index=0,
                    expected_counters={"physical_cr3_used": 12, "autoexposure_physical_cr3_used": 0, "weak_reacquire_physical_cr3_used": 0},
                    expected_budget={"exhaustion": valid_exhaustion, "consumed": {}, "limits": {}},
                )

            limits = {
                "rebase_probe_count": 4,
                "max_rebases_per_start": 2,
                "max_feedback_capture_attempts_per_start": 8,
                "max_confirmation_groups_per_start": 2,
                "confirmation_captures_per_group": 3,
            }
            categories = {
                "initial": ("initial", 1),
                "initial_probes": ("probe-4", 4),
                "feedback_attempts": ("feedback-8", 8),
                "rebase_probes": ("rebase-2-probe-4", 8),
                "confirmation_captures": ("confirm-1-2", 6),
            }
            for category, (phase, limit) in categories.items():
                consumed = {name: 0 for name in ("initial", "initial_probes", "feedback_attempts", "rebase_probes", "confirmation_captures")}
                consumed[category] = limit
                budget = {"consumed": consumed, "limits": limits}
                self.assertTrue(analyze_strip_hsi_pilot._phase_matches_sub_budget(phase, category, budget))
                consumed[category] = limit - 1
                self.assertFalse(analyze_strip_hsi_pilot._phase_matches_sub_budget(phase, category, budget))

    def test_v2_analyzer_rejects_unselected_cross_target_orphan_and_nonzero_off(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            policy = _frozen_policy_v2_file(root)
            plan = subject.build_strip_hsi_pilot_plan(policy_version="v2", policy_v2_config_path=policy)
            run_root = root / "run"
            _execute_fake_v2_plan(plan, run_root)
            _write_shell_cleanup(run_root)
            rows_path = run_root / "target-results.jsonl"
            captures_path = run_root / "captures.jsonl"
            commands_path = run_root / "commands.jsonl"
            original_rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
            original_captures = [json.loads(line) for line in captures_path.read_text(encoding="utf-8").splitlines()]
            original_commands = [json.loads(line) for line in commands_path.read_text(encoding="utf-8").splitlines()]

            def write(path, values):
                path.write_text("\n".join(json.dumps(item) for item in values) + "\n", encoding="utf-8")

            rows = copy.deepcopy(original_rows)
            malformed = copy.deepcopy(rows[0]["feedback"]["attempts"][0])
            malformed["start_index"] = 1
            malformed["result"]["goal_confirmed"] = False
            malformed["result"]["confirmation_attempts"][0]["candidate_command"]["r"] += 1
            rows[0]["feedback"]["attempts"].append(malformed)
            rows[0]["feedback"]["attempt_count"] = 2
            rows[0]["feedback"]["logical_observations_used"] += malformed["result"]["budget"]["logical_observations_used"]
            write(rows_path, rows)
            with self.assertRaisesRegex(ValueError, "confirmation command|duplicate"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")

            rows = copy.deepcopy(original_rows)
            other_capture = next(
                sample["observation"]["capture_id"]
                for sample in rows[1]["feedback"]["selected_result"]["samples"]
            )
            rows[0]["feedback"]["selected_result"]["samples"][0]["observation"]["capture_id"] = other_capture
            rows[0]["feedback"]["attempts"][0]["result"] = rows[0]["feedback"]["selected_result"]
            write(rows_path, rows)
            with self.assertRaisesRegex(ValueError, "provenance"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            write(rows_path, original_rows)

            commands = copy.deepcopy(original_commands)
            next(item for item in commands if item["event"] == "both_off")["strip_device_evidence"]["device_snapshot"]["red"] = 1
            write(commands_path, commands)
            with self.assertRaisesRegex(ValueError, "frozen command"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")
            write(commands_path, original_commands)

            rows = copy.deepcopy(original_rows)
            captures = copy.deepcopy(original_captures)
            commands = copy.deepcopy(original_commands)
            source_capture = next(item for item in captures if item.get("target_index") == 0 and not item["capture"].get("auto_exposure_audit"))
            orphan = copy.deepcopy(source_capture)
            orphan["capture_id"] += "-orphan"
            captures.append(orphan)
            for event in [item for item in commands if item["capture_id"] == source_capture["capture_id"]]:
                copied = copy.deepcopy(event)
                copied["capture_id"] = orphan["capture_id"]
                commands.append(copied)
            rows[0]["physical_budget"]["events"].append({
                "phase": orphan["purpose"], "physical_cr3": 1,
                "auto_exposure": False, "weak_reacquire": False,
            })
            rows[0]["physical_budget"]["physical_cr3_used"] += 1
            write(captures_path, captures)
            write(commands_path, commands)
            write(rows_path, rows)
            with self.assertRaisesRegex(ValueError, "orphan captures"):
                analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(run_root, policy_version="v2")


def _execute_fake_plan(plan, root: Path, *, mismatch_readback: bool = False, sleep_calls=None):
    manifold = RayHsiManifold.load()
    target_by_index = {target["index"]: target for target in plan["targets"]}
    ray_state = {}
    strip_generation = 0
    curve = json.loads(Path(plan["inputs"]["code_duty_curve"]["path"]).read_text(encoding="utf-8"))

    def capture_step(step):
        capture_id = step["capture_id"]
        raw = root / "camera" / f"{capture_id}.cr3"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"CR3")
        target_index_value = step["analysis_context"]["target_index"]
        if step["source"] == "ray":
            state = step["ray"]
            measured = manifold.target_at(state["hue"], state["sat"])
            values = {feature: measured.features[feature] for feature in manifold.coordinate_feature_ids}
        elif target_index_value is None or int(target_index_value) < 0:
            values = {feature: 0.01 for feature in manifold.coordinate_feature_ids}
        else:
            target = target_by_index[int(target_index_value)]
            measured = manifold.target_at(target["hue"], target["sat"])
            values = {feature: measured.features[feature] for feature in manifold.coordinate_feature_ids}
        report = root / "measurements" / f"{capture_id}.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(_report(values, raw)), encoding="utf-8")
        return {"capture": {"saved_file": str(raw), "byte_count": 3, "camera_backend": "remote"}, "patch_statistics": str(report)}

    def strip_light(cw, ww, r, g, b):
        nonlocal strip_generation
        payload = subject.esphome._build_payload(cw, ww, r, g, b, curve=curve)
        baseline = strip_generation
        strip_generation += 1
        return _strip_device_evidence(payload, baseline, strip_generation)

    def ray_set_hsi(hue, sat, *, intensity_percent):
        ray_state.update({"hue": hue, "sat": sat, "intensity": int(intensity_percent * 10)})
        return {"code": 0, "data": dict(ray_state)}

    def ray_get_hsi():
        state = dict(ray_state)
        if mismatch_readback:
            state["hue"] = (state["hue"] + 1) % 360
        return {"code": 0, "data": state}

    return subject.execute_strip_hsi_pilot_plan(
        plan,
        run_dir=root,
        capture_step_fn=capture_step,
        strip_light_fn=strip_light,
        ray_off_fn=lambda: {"code": 0, "data": {"intensity": 0}},
        ray_set_hsi_fn=ray_set_hsi,
        ray_get_hsi_fn=ray_get_hsi,
        sleep_fn=(sleep_calls.append if sleep_calls is not None else lambda _seconds: None),
        all_off_fn=lambda: [ShutdownStep("esphome", True), ShutdownStep("ray120c", True)],
    )


def _execute_fake_v2_plan(plan, root: Path):
    manifold = RayHsiManifold.load()
    target_by_index = {target["index"]: target for target in plan["targets"]}
    ray_state = {}
    capture_count = 0
    strip_generation = 0
    curve = json.loads(Path(plan["inputs"]["code_duty_curve"]["path"]).read_text(encoding="utf-8"))

    def capture_step(step):
        nonlocal capture_count
        capture_count += 1
        capture_id = step["capture_id"]
        raw = root / "camera" / f"{capture_id}.cr3"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"CR3")
        target_index = step["analysis_context"]["target_index"]
        if step["source"] == "ray":
            target = manifold.target_at(step["ray"]["hue"], step["ray"]["sat"])
        elif target_index is None or int(target_index) < 0:
            target = manifold.target_at(0, 0)
        else:
            row = target_by_index[int(target_index)]
            target = manifold.target_at(row["hue"], row["sat"])
        values = {feature: target.features[feature] for feature in manifold.coordinate_feature_ids}
        for plane in ("R", "G1", "G2", "B"):
            feature = next(item for item in manifold.coordinate_feature_ids if item.endswith(f"::{plane}"))
            values[feature] += (capture_count % 3 - 1) * 1e-7
        report = root / "measurements" / f"{capture_id}.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(_report(values, raw)), encoding="utf-8")
        return {
            "capture": {"saved_file": str(raw), "byte_count": 3, "camera_backend": "remote"},
            "patch_statistics": str(report), "physical_capture_count": 1,
            "auto_exposure_audit": ({
                "capture_count": 1, "trials": [], "final": {"status": "accepted"},
                "rejected_finals": [],
            } if step.get("auto_exposure") else None),
        }

    def strip_light(cw, ww, r, g, b):
        nonlocal strip_generation
        payload = subject.esphome._build_payload(cw, ww, r, g, b, curve=curve)
        baseline = strip_generation
        strip_generation += 1
        return _strip_device_evidence(payload, baseline, strip_generation)

    def ray_set_hsi(hue, sat, *, intensity_percent):
        ray_state.update({"hue": hue, "sat": sat, "intensity": int(intensity_percent * 10)})
        return {"code": 0, "data": dict(ray_state)}

    return subject.execute_strip_hsi_pilot_plan(
        plan, run_dir=root, capture_step_fn=capture_step,
        strip_light_fn=strip_light,
        ray_off_fn=lambda: {"code": 0, "data": {"intensity": 0}},
        ray_set_hsi_fn=ray_set_hsi,
        ray_get_hsi_fn=lambda: {"code": 0, "data": dict(ray_state)},
        sleep_fn=lambda _seconds: None,
        all_off_fn=lambda: [ShutdownStep("esphome", True), ShutdownStep("ray120c", True)],
    )


def _write_shell_cleanup(root: Path) -> None:
    cleanup = [{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]
    (root / "all-off-shell.json").write_text(json.dumps(cleanup), encoding="utf-8")


def _append_fake_exhausted_start(root: Path, plan, *, category: str, phases: list[str]) -> None:
    captures_path = root / "captures.jsonl"
    commands_path = root / "commands.jsonl"
    rows_path = root / "target-results.jsonl"
    captures = [json.loads(line) for line in captures_path.read_text(encoding="utf-8").splitlines()]
    commands = [json.loads(line) for line in commands_path.read_text(encoding="utf-8").splitlines()]
    rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines()]
    row = rows[0]
    feedback = row["feedback"]
    selected = feedback["selected_result"]
    command = dict(selected["selected_command"])
    base_sample = selected["samples"][-1]
    base_id = base_sample["observation"]["capture_id"]
    base_capture = next(item for item in captures if item["capture_id"] == base_id)
    base_commands = [item for item in commands if item["capture_id"] == base_id]
    rejections = []
    for index, phase in enumerate(phases):
        capture_id = f"r0i-{category}-{index}"
        capture = copy.deepcopy(base_capture)
        capture["capture_id"] = capture_id
        capture["purpose"] = f"candidate_{phase}"
        captures.append(capture)
        for event in base_commands:
            copied = copy.deepcopy(event)
            copied["capture_id"] = capture_id
            commands.append(copied)
        rejections.append({
            "phase": phase,
            "command": command,
            "evidence": {
                "source": "strip",
                "purpose": f"candidate_{phase}",
                "capture_ids": [capture_id],
                "exposure_factors": [1.0],
                "rejected_features": [{"status": "weak_signal", "feature": "fake"}],
            },
        })
        row["physical_budget"]["events"].append({
            "phase": f"candidate_{phase}", "physical_cr3": 1,
            "auto_exposure": False, "weak_reacquire": False,
        })
    row["physical_budget"]["physical_cr3_used"] += len(phases)
    limits = dict(plan["targets"][0]["solver_budget"])
    consumed = {name: 0 for name in ("initial", "initial_probes", "feedback_attempts", "rebase_probes", "confirmation_captures")}
    consumed[category] = len(phases)
    next_phase = {
        "initial": "initial",
        "initial_probes": "probe-next",
        "feedback_attempts": "feedback-8",
        "rebase_probes": "rebase-2-probe-0",
        "confirmation_captures": "confirm-2-0",
    }[category]
    ledger = {
        "pre_capture_exhaustion": True,
        "status": "solver_budget_exhausted",
        "sub_budget": category,
        "phase": next_phase,
        "requested_physical_cr3": 0,
        "physical_cr3_used": len(phases),
        "autoexposure_physical_cr3_used": 0,
        "weak_reacquire_physical_cr3_used": 0,
        "capture_attempted": False,
        "start_index": 1,
    }
    exhausted = {
        "kind": "hsi_bounded_local_feedback",
        "status": "solver_budget_exhausted",
        "active_channel": plan["targets"][0]["distinct_face_seeds"][1]["active_channel"],
        "initial_command": command,
        "selected_command": command,
        "goal_confirmed": False,
        "rounds_requested": 8,
        "rounds_completed": 0,
        "confirmation_attempts": [{
            "status": "partial", "sample_indices": [], "candidate_command": command,
            "captured_count": 0, "expected_capture_count": 3,
            "feasible_capture_count": 0, "partial_group": True,
        }],
        "thermal_rebases": [],
        "measurement_rejections": rejections,
        "step_records": [],
        "group_order": ["coordinate", "rendering"],
        "best": None,
        "samples": [],
        "budget": {
            "start_index": 1, "limits": limits, "consumed": consumed,
            "logical_observations_used": len(phases),
            "confirmation_groups_started": 1,
            "rebases_started": 2 if category == "rebase_probes" else 0,
            "exhaustion": ledger,
        },
        "budget_exhaustion": ledger,
    }
    feedback["attempts"].append({
        "start_index": 1,
        "seed": dict(plan["targets"][0]["distinct_face_seeds"][1]),
        "result": exhausted,
    })
    feedback["attempt_count"] = 2
    feedback["logical_observations_used"] += len(phases)
    captures_path.write_text("\n".join(json.dumps(item) for item in captures) + "\n", encoding="utf-8")
    commands_path.write_text("\n".join(json.dumps(item) for item in commands) + "\n", encoding="utf-8")
    rows_path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")


def _strip_device_evidence(payload, baseline_generation, generation):
    return {
        "schema_version": 1,
        "requested_payload": dict(payload),
        "baseline_snapshot": {"schema_version": 1, "generation": baseline_generation, **dict(payload)},
        "device_snapshot": {"schema_version": 1, "generation": generation, **dict(payload)},
        "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 7},
        "device_identity": {"name": "bedroom-rgbww-strip", "mac_address": "fake"},
    }


def _report(values, raw):
    grouped = {}
    for feature, value in values.items():
        patch, plane = feature.split("::")
        grouped.setdefault(patch, {})[plane] = value
    patches = []
    for patch, planes in sorted(grouped.items()):
        patches.append({
            "name": patch,
            "optimization_eligible": True,
            "planes": {
                plane: {
                    "quality": {"status": "accepted"},
                    "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                    "ambient_subtracted": {"trimmed_mean_per_second": float(planes.get(plane, 0.01))},
                }
                for plane in ("R", "G1", "G2", "B")
            },
        })
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": str(raw)},
        "exposure_metadata": {"status": "recorded"},
        "location_config": {"sha256": subject.LATEST_LOCATION_SHA256},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "observer_config": {"quality_thresholds": {"minimum_valid_pixels_per_plane": 29000, "maximum_nonfinite_fraction": 0.0, "maximum_clipped_fraction": 0.0, "maximum_near_noise_floor_fraction": 0.05}},
        "patches": patches,
    }


def _uncertainty_file(root: Path) -> Path:
    manifold = RayHsiManifold.load()
    path = root / "strip-hsi-uncertainty.json"
    regions = {}
    for kind, dimensions in {
        "sat0_exact_node": 2,
        "nonzero_exact_node": 3,
        "nonzero_regular_interpolation": 3,
        "nonzero_high_curvature_interpolation": 3,
    }.items():
        regions[kind] = {
            "component_scales": [1.0] * dimensions,
            "coverage_limit": 12.0,
            "guarded_acceptance_limit": 10.0,
            "diagonal_variance": [1e-4] * len(manifold.coordinate_feature_ids),
        }
    path.write_text(json.dumps({
        "schema_version": 1,
        "status": "offline_frozen_before_measurement",
        "feature_set": {
            "count": len(manifold.coordinate_feature_ids),
            "ids": list(manifold.coordinate_feature_ids),
            "sha256": subject.feature_ids_sha256(manifold.coordinate_feature_ids),
        },
        "joint_calibration": regions,
        "reference_calibration": regions,
        "confirmation_policies": {
            "repeat_spread": {
                family: {
                    str(count): {"component_scales": [1.0] * dimensions, "limit": 10.0}
                    for count in (3, 5)
                }
                for family, dimensions in (("sat0", 2), ("nonzero", 3))
            }
        },
    }), encoding="utf-8")
    return path


def _frozen_policy_v2_file(root: Path) -> Path:
    manifold = RayHsiManifold.load()
    waiting = json.loads(subject.DEFAULT_POLICY_V2_CONFIG.read_text(encoding="utf-8"))
    waiting["status"] = "offline_frozen_before_measurement"
    waiting["formal_capture_eligible"] = True
    waiting["reference_policy"]["status"] = "offline_frozen_before_measurement"
    waiting["repeatability_policy"]["status"] = "offline_frozen_before_measurement"
    variance = [1e-4] * len(manifold.coordinate_feature_ids)
    states = {}
    for hue, sat in ((0, 0), (120, 100), (300, 100)):
        target = manifold.target_at(hue, sat)
        unit = np.asarray([target.features[feature] for feature in manifold.coordinate_feature_ids], dtype=float)
        unit /= np.linalg.norm(unit)
        states[f"h{hue}-s{sat}"] = {
            "frozen_center": unit.tolist(), "frozen_diagonal_variance": variance,
            "frozen_count": 5,
            "center_compatibility_region": {"guarded_limit": 100.0, "unguarded_limit": 120.0},
            "repeatability_region": {"guarded_limit": 100.0, "unguarded_limit": 120.0},
        }
    waiting["reference_policy"]["states"] = states
    for class_policy in waiting["repeatability_policy"]["classes"].values():
        class_policy.update({
            "status": "offline_frozen_before_measurement",
            "targeted_variance": variance,
            "limits": {"3": 100.0, "5": 100.0},
        })
    coordinate_limits = {
        "sat0_exact_node:neutral_fullscale": {"component_scales": [1.0], "guarded_limit": 10.0, "unguarded_limit": 12.0},
        "nonzero_exact_node:mid_sat_fullscale": {"component_scales": [1.0, 1.0], "guarded_limit": 10.0, "unguarded_limit": 12.0},
        "nonzero_exact_node:sat100_fullscale": {"component_scales": [1.0, 1.0], "guarded_limit": 10.0, "unguarded_limit": 12.0},
    }
    waiting["coordinate_policy"]["formal_limits"] = coordinate_limits
    waiting["observer_policy"]["formal_limits"] = {
        key: {"guarded_limit": 1000.0, "unguarded_limit": 1200.0}
        for key in coordinate_limits
    }
    path = root / "strip-hsi-policy-v2.json"
    path.write_text(json.dumps(waiting), encoding="utf-8")
    return path


if __name__ == "__main__":
    unittest.main()
