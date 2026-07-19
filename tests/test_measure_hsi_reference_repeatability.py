from __future__ import annotations

import json
import copy
import os
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.control import all_off, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.control.all_off import ShutdownStep
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import measure_hsi_reference_repeatability as subject
from camera_based_rgbww_optimizer.optimization import analyze_hsi_reference_repeatability as analyzer


class MeasureHsiReferenceRepeatabilityTests(unittest.TestCase):
    def test_dry_run_has_exact_30_ray_50_strip_and_never_touches_devices(self):
        with tempfile.TemporaryDirectory(dir=subject.PROJECT_TMP_DIR) as tempdir:
            with (
                mock.patch.object(camera_remote, "create_camera_backend") as camera,
                mock.patch.object(esphome, "light") as strip,
                mock.patch.object(ray120c, "set_hsi") as ray,
                mock.patch.object(all_off, "turn_everything_off") as shutdown,
            ):
                result = subject.main([
                    "--dry-run", "--output-dir", tempdir, "--run-name", "draft",
                ])
            plan = json.loads((Path(tempdir) / "draft" / "plan.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(plan["experiment"], subject.EXPERIMENT_NAME)
        self.assertEqual(plan["measurement"]["formal_ray_count"], 30)
        self.assertEqual(plan["measurement"]["formal_strip_count"], 50)
        self.assertEqual(plan["measurement"]["ambient_count"], 2)
        self.assertEqual(len(plan["captures"]), 82)
        self.assertFalse(plan["formal_capture_eligible"])
        self.assertEqual(plan["authorization"]["status"], "not_authorized_for_execution")
        self.assertEqual(plan["offline_contract"]["network_calls"], 0)
        physical = plan["measurement"]["physical_capture_audit"]
        self.assertEqual(physical["baseline_physical_range_without_weak_reacquire"], [82, 170])
        self.assertEqual(physical["permitted_physical_range_with_weak_reacquire"], [82, 250])
        self.assertEqual(physical["maximum_total_physical_cr3"], 250)
        self.assertEqual(physical["absolute_cap_status"], "planner_frozen")
        self.assertEqual(physical["maximum_60_second_settling_seconds"], 9600)
        camera.assert_not_called()
        strip.assert_not_called()
        ray.assert_not_called()
        shutdown.assert_not_called()

    def test_sequence_keeps_ray_blocks_apart_and_balances_repeats(self):
        plan = subject.build_targeted_reference_repeatability_plan()
        formal = [item for item in plan["captures"] if item["formal_measurement"]]
        sources_blocks = []
        for item in formal:
            pair = (item["source"], item["block"])
            if not sources_blocks or sources_blocks[-1] != pair:
                sources_blocks.append(pair)
        self.assertEqual(sources_blocks, [("ray", "A"), ("strip", "A"), ("strip", "B"), ("ray", "B")])
        for block in ("A", "B"):
            ray = [item for item in formal if item["source"] == "ray" and item["block"] == block]
            strip = [item for item in formal if item["source"] == "strip" and item["block"] == block]
            self.assertEqual({(item["state"]["hue"], item["state"]["sat"]): sum(
                other["state"] == item["state"] for other in ray
            ) for item in ray}, {(0, 0): 5, (120, 100): 5, (300, 100): 5})
            self.assertTrue(all(sum(other["command_key"] == key for other in strip) == 5 for key in subject.STRIP_KEYS))

    def test_commands_are_exactly_extracted_from_frozen_sentinel(self):
        plan = subject.build_targeted_reference_repeatability_plan()
        self.assertEqual(max(plan["commands"]["h0-s0-scale-relaxed-3072"].values()), 3072)
        for key in subject.STRIP_KEYS[:-1]:
            self.assertEqual(max(plan["commands"][key].values()), 4095)

    def test_fake_backend_executes_exact_82_and_python_cleanup(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            output = _execute_fake(plan, root)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            captures = (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(output, root)
        self.assertEqual(len(captures), 82)
        self.assertEqual(run["logical_captures_completed"], 82)
        self.assertEqual(run["formal_captures_completed"], 80)
        self.assertEqual(run["physical_cr3_count"], 82)
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_fake_backend_failure_preserves_evidence_and_python_cleanup(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "injected capture failure"):
                _execute_fake(plan, root, fail_at=5)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            failure = json.loads((root / "failure.json").read_text(encoding="utf-8"))
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(run["status"], "failed")
        self.assertEqual(failure["type"], "RuntimeError")
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_python_and_shell_cleanup_fail_closed(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "python"
            with self.assertRaisesRegex(RuntimeError, "successful Python cleanup"):
                _execute_fake(plan, root, cleanup_ok=False)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run["status"], "failed")

            root2 = Path(tempdir) / "shell"
            _execute_fake(plan, root2)
            (root2 / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": False},
            ]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Python and shell cleanup"):
                analyzer.analyze_reference_repeatability_run(root2, monte_carlo_samples=1000, bootstrap_replicates=100)

    def test_shell_wrapper_records_atomic_long_task_exit_evidence_and_cleanup_once(self):
        cases = [
            ("success", None, 0, 0, 0, "complete", None),
            ("failure", None, 7, 0, 7, "child_failed", None),
            ("cleanup_failure", None, 0, 9, 70, "cleanup_failed", None),
            ("sleep", signal.SIGINT, 130, 0, 130, "signaled", "INT"),
            ("sleep", signal.SIGTERM, 143, 0, 143, "signaled", "TERM"),
            ("sleep", signal.SIGHUP, 129, 0, 129, "signaled", "HUP"),
        ]
        for mode, sent_signal, child_code, cleanup_code, wrapper_code, status, signal_name in cases:
            with self.subTest(mode=mode, sent_signal=sent_signal), tempfile.TemporaryDirectory() as tempdir:
                root, wrapper, call_log = _make_fake_r1_wrapper_project(Path(tempdir))
                run_dir = root / "runs" / f"{mode}-{getattr(sent_signal, 'name', 'exit')}"
                state_path = run_dir.parent / f"{run_dir.name}.wrapper-state.json"
                env = os.environ.copy()
                env["FAKE_RUNNER_MODE"] = mode
                env["FAKE_CALL_LOG"] = str(call_log)
                ready_file = Path(tempdir) / "runner-ready"
                env["FAKE_READY_FILE"] = str(ready_file)
                process = subprocess.Popen(
                    ["zsh", str(wrapper), str(run_dir)], env=env,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
                try:
                    if sent_signal is not None:
                        deadline = time.monotonic() + 5
                        while (not ready_file.exists() or not state_path.exists()) and time.monotonic() < deadline:
                            time.sleep(0.02)
                        self.assertTrue(ready_file.exists())
                        running_state = _load_json(state_path)
                        self.assertEqual(running_state["status"], "running")
                        os.kill(process.pid, sent_signal)
                    process.wait(timeout=8)
                finally:
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=5)

                calls = call_log.read_text(encoding="utf-8").splitlines()
                cleanup_calls = [line for line in calls if "camera_based_rgbww_optimizer.control.all_off" in line]
                runner_calls = [line for line in calls if "measure_hsi_reference_repeatability" in line]
                self.assertEqual(len(cleanup_calls), 1)
                self.assertEqual(len(runner_calls), 1)
                self.assertIn("--named-experiment p7_targeted_reference_repeatability_v2", runner_calls[0])
                self.assertEqual(process.returncode, wrapper_code)
                self.assertEqual((run_dir / "child-exit-status.txt").read_text(encoding="utf-8").strip(), str(child_code))
                self.assertEqual((run_dir / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip(), str(cleanup_code))

                result = _load_json(run_dir / "wrapper-result.json")
                state = _load_json(state_path)
                self.assertEqual(result["experiment"], subject.EXPERIMENT_NAME)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["child_exit_code"], child_code)
                self.assertEqual(result["shell_cleanup_exit_code"], cleanup_code)
                self.assertEqual(result["wrapper_exit_code"], wrapper_code)
                self.assertEqual(result["signal"], signal_name)
                self.assertEqual(Path(result["artifacts"]["run_dir"]), run_dir.resolve())
                self.assertEqual(Path(result["artifacts"]["shell_cleanup"]), run_dir.resolve() / "all-off-shell.json")
                self.assertEqual(state["experiment"], subject.EXPERIMENT_NAME)
                self.assertEqual(state["status"], "finished")
                self.assertEqual(state["wrapper_pid"], process.pid)
                self.assertEqual(state["child_pid"], result["child_pid"])
                self.assertEqual(state["wrapper_exit_code"], wrapper_code)
                self.assertEqual(Path(state["run_dir"]), run_dir.resolve())
                self.assertEqual(Path(state["runner_log"]), run_dir.parent.resolve() / f"{run_dir.name}.runner.log")
                self.assertEqual(Path(state["wrapper_log"]), run_dir.parent.resolve() / f"{run_dir.name}.wrapper.log")
                self.assertFalse(list(run_dir.glob(".*.tmp.*")))
                self.assertFalse(list(run_dir.parent.glob(".*.tmp.*")))
                self.assertNotIn("secret", json.dumps([result, state]).lower())
                self.assertNotIn("token", json.dumps([result, state]).lower())

                cleanup_stdout = (run_dir / "all-off-shell.json").read_text(encoding="utf-8")
                self.assertIn('"name": "esphome"', cleanup_stdout)
                cleanup_stderr = (run_dir / "all-off-shell.stderr.log").read_text(encoding="utf-8")
                if mode == "cleanup_failure":
                    self.assertIn("fake cleanup failed", cleanup_stderr)
                else:
                    self.assertEqual(cleanup_stderr, "")

    def test_terminal_launcher_records_ownership_and_execs_only_the_formal_wrapper(self):
        launcher = (
            Path(__file__).parents[1]
            / "tmp"
            / "launch-hsi-reference-repeatability-terminal.zsh"
        ).read_text(encoding="utf-8")
        self.assertIn('print -r -- "$$" >"$PREFLIGHT_DIR/launcher.pid"', launcher)
        self.assertIn('print -r -- "$PPID" >"$PREFLIGHT_DIR/terminal-shell.pid"', launcher)
        self.assertIn("pid=,ppid=,pgid=,tty=", launcher)
        self.assertIn("trap cleanup_preflight_failure EXIT INT TERM HUP", launcher)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off --json", launcher)
        self.assertIn('exec /bin/zsh "$WRAPPER" "$RUN_DIR"', launcher)
        self.assertNotIn("measure_hsi_reference_repeatability", launcher)
        self.assertNotIn("--allow-high-output", launcher)
        self.assertNotIn("set-hsi", launcher)

    def test_analyzer_finalizer_writes_only_formal_ineligible_candidate(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            report_path, candidate_path = analyzer.finalize_reference_repeatability_run(
                root, monte_carlo_samples=1000, bootstrap_replicates=100, seed=11,
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "calibrated_waiting_for_planner")
        self.assertFalse(report["formal_capture_eligible"])
        self.assertFalse(candidate["formal_capture_eligible"])
        self.assertTrue(candidate["planner_freeze_required"])
        self.assertIn("empirical_coverage", next(iter(report["synthetic_joint_coverage"]["regions"].values())))

    def test_weak_reacquire_retains_both_attempts_and_recomputes_physical_evidence(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root, weak_at=1)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            report = analyzer.analyze_reference_repeatability_run(
                root, monte_carlo_samples=1000, bootstrap_replicates=100, seed=11,
            )
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            logical = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
        weak_attempts = [item for item in attempts if item["logical_capture_id"] == logical[1]["capture_id"]]
        self.assertEqual([item["attempt_kind"] for item in weak_attempts], ["base", "weak_signal_reacquire"])
        self.assertIsNotNone(weak_attempts[0]["quality_rejection"])
        self.assertFalse(weak_attempts[0]["selected_for_formal"])
        self.assertTrue(weak_attempts[1]["selected_for_formal"])
        self.assertEqual(report["capture_audit"]["physical_cr3_count"], 83)
        self.assertEqual(report["capture_audit"]["weak_signal_reacquire_count"], 1)
        self.assertTrue(report["capture_audit"]["commands_jsonl_audited"])

    def test_reacquire_readback_mismatch_fails_and_python_cleanup_runs(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaises(Exception):
                _execute_fake(plan, root, weak_at=1, mismatch_reacquire=True)
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_auto_exposure_one_over_is_prechecked_before_adapter_call(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        plan["measurement"]["physical_capture_audit"]["maximum_autoexposure_physical_cr3"] = 0
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "before base capture"):
                _execute_fake(plan, root)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["logical_captures_completed"], 1)
        self.assertEqual(run["physical_cr3_count"], 1)
        self.assertEqual(run["auto_exposure_cache_miss_count"], 0)

    def test_analyzer_rejects_counter_and_command_tampering(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "counter"
            _execute_fake(plan, root)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            run["physical_cr3_count"] += 1
            (root / "run.json").write_text(json.dumps(run), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "counter mismatch"):
                analyzer.analyze_reference_repeatability_run(root, monte_carlo_samples=1000, bootstrap_replicates=100)

            root2 = Path(tempdir) / "commands"
            _execute_fake(plan, root2)
            (root2 / "all-off-shell.json").write_text((root / "all-off-shell.json").read_text(encoding="utf-8"), encoding="utf-8")
            commands = [json.loads(line) for line in (root2 / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            commands.pop(1)
            (root2 / "commands.jsonl").write_text("\n".join(json.dumps(item) for item in commands) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "command evidence|readback mismatch"):
                analyzer.analyze_reference_repeatability_run(root2, monte_carlo_samples=1000, bootstrap_replicates=100)

    def test_analyzer_compares_retained_evidence_to_frozen_plan_and_all_counters(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root)
            captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            feature_ids = analyzer.HsiPolicyV2.load(plan["inputs"]["policy_v2_waiting"]["path"]).artifact["feature_set"]["ids"]

            tampered_captures = copy.deepcopy(captures)
            tampered_attempts = copy.deepcopy(attempts)
            tampered_commands = copy.deepcopy(commands)
            ray_record = next(item for item in tampered_captures if item["source"] == "ray" and item["plan_step"]["state"]["hue"] == 0)
            attempt_id = ray_record["selected_attempt_capture_id"]
            ray_record["readback"]["data"]["hue"] = 1
            ray_record["plan_step"]["state"]["hue"] = 1
            next(item for item in tampered_attempts if item["attempt_capture_id"] == attempt_id)["readback"]["data"]["hue"] = 1
            ray_on = next(item for item in tampered_commands if item["capture_id"] == attempt_id and "ray_on" in item["event"])
            ray_on["expected"]["hue"] = ray_on["readback"]["data"]["hue"] = 1
            with self.assertRaisesRegex(ValueError, "frozen plan"):
                analyzer._audit_capture_contract(
                    tampered_captures, tampered_attempts, tampered_commands, feature_ids,
                    run=run, physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )

            nonzero = copy.deepcopy(commands)
            next(item for item in nonzero if item["event"] == "both_off")["strip_device_evidence"]["device_snapshot"]["red"] = 1
            with self.assertRaisesRegex(ValueError, "frozen command"):
                analyzer._audit_capture_contract(
                    captures, attempts, nonzero, feature_ids, run=run,
                    physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )
            foreign = copy.deepcopy(commands)
            event = copy.deepcopy(next(item for item in foreign if item["event"] == "strip_on_readback_verified"))
            event["capture_id"] = next(item for item in attempts if item["source"] == "ray")["attempt_capture_id"]
            foreign.append(event)
            with self.assertRaisesRegex(ValueError, "grammar"):
                analyzer._audit_capture_contract(
                    captures, attempts, foreign, feature_ids, run=run,
                    physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )
            drift_run = dict(run)
            drift_run["base_physical_cr3_count"] += 1
            with self.assertRaisesRegex(ValueError, "counter mismatch"):
                analyzer._audit_capture_contract(
                    captures, attempts, commands, feature_ids, run=drift_run,
                    physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )

    def test_analyzer_rejects_missing_plan_step_replaced_by_duplicate_ambient(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            feature_ids = analyzer.HsiPolicyV2.load(plan["inputs"]["policy_v2_waiting"]["path"]).artifact["feature_set"]["ids"]
            tampered = copy.deepcopy(captures)
            tampered[-1] = copy.deepcopy(tampered[0])
            with self.assertRaisesRegex(ValueError, "complete frozen plan order"):
                analyzer._audit_capture_contract(
                    tampered, attempts, commands, feature_ids, run=run,
                    physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )

    def test_runner_nonzero_both_off_fails_and_python_cleanup_runs(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(ValueError, "intensity zero"):
                _execute_fake(plan, root, nonzero_off=True)
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_analyzer_rejects_strip_cotamper_orphan_events_all_counter_drift_and_auto_one_over(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root)
            captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            physical = plan["measurement"]["physical_capture_audit"]
            feature_ids = analyzer.HsiPolicyV2.load(plan["inputs"]["policy_v2_waiting"]["path"]).artifact["feature_set"]["ids"]

            strip_captures = copy.deepcopy(captures)
            strip_attempts = copy.deepcopy(attempts)
            strip_commands = copy.deepcopy(commands)
            record = next(item for item in strip_captures if item["source"] == "strip")
            attempt_id = record["selected_attempt_capture_id"]
            response = next(item for item in strip_commands if item["capture_id"] == attempt_id and item["event"] == "strip_on_readback_verified")["device_evidence"]
            response["device_snapshot"]["red"] = int(response["device_snapshot"].get("red", 0)) + 1
            next(item for item in strip_attempts if item["attempt_capture_id"] == attempt_id)["readback"] = copy.deepcopy(response)
            record["readback"] = copy.deepcopy(response)
            with self.assertRaisesRegex(ValueError, "frozen command"):
                analyzer._audit_capture_contract(
                    strip_captures, strip_attempts, strip_commands, feature_ids,
                    run=run, physical_contract=physical, plan=plan,
                )

            orphan_commands = copy.deepcopy(commands)
            orphan = copy.deepcopy(orphan_commands[0])
            orphan["capture_id"] = "unknown-attempt"
            orphan_commands.append(orphan)
            with self.assertRaisesRegex(ValueError, "orphan"):
                analyzer._audit_capture_contract(
                    captures, attempts, orphan_commands, feature_ids,
                    run=run, physical_contract=physical, plan=plan,
                )

            for counter in (
                "logical_captures_completed", "formal_captures_completed",
                "physical_cr3_count", "base_physical_cr3_count",
                "auto_exposure_physical_cr3_count", "auto_exposure_cache_miss_count",
                "weak_signal_reacquire_count", "weak_signal_reacquire_physical_cr3_count",
            ):
                with self.subTest(counter=counter):
                    drift = dict(run)
                    drift[counter] += 1
                    with self.assertRaisesRegex(ValueError, "counter mismatch"):
                        analyzer._audit_capture_contract(
                            captures, attempts, commands, feature_ids,
                            run=drift, physical_contract=physical, plan=plan,
                        )

            over_attempts = copy.deepcopy(attempts)
            auto = next(item for item in over_attempts if item["auto_exposure"])
            auto["auto_exposure_audit"]["trials"] = [{"index": index} for index in range(12)]
            auto["auto_exposure_audit"]["capture_count"] = 13
            auto["physical_capture_count"] = 13
            auto["capture"]["auto_exposure_audit"] = copy.deepcopy(auto["auto_exposure_audit"])
            auto["capture"]["physical_capture_count"] = 13
            over_captures = copy.deepcopy(captures)
            logical = next(item for item in over_captures if item["capture_id"] == auto["logical_capture_id"])
            logical["capture"] = copy.deepcopy(auto["capture"])
            over_run = dict(run)
            for counter in ("physical_cr3_count", "base_physical_cr3_count", "auto_exposure_physical_cr3_count"):
                over_run[counter] += 12
            with self.assertRaisesRegex(ValueError, "per-cache-miss cap"):
                analyzer._audit_capture_contract(
                    over_captures, over_attempts, commands, feature_ids,
                    run=over_run, physical_contract=physical, plan=plan,
                )

    def test_analyzer_rejects_selecting_weak_rejected_base(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root, weak_at=1)
            captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            feature_ids = analyzer.HsiPolicyV2.load(plan["inputs"]["policy_v2_waiting"]["path"]).artifact["feature_set"]["ids"]
            record = captures[1]
            logical_attempts = [item for item in attempts if item["logical_capture_id"] == record["capture_id"]]
            base, reacquire = logical_attempts
            base["selected_for_formal"] = True
            reacquire["selected_for_formal"] = False
            record["selected_attempt_capture_id"] = base["attempt_capture_id"]
            record["capture"] = copy.deepcopy(base["capture"])
            record["readback"] = copy.deepcopy(base["readback"])
            with self.assertRaisesRegex(ValueError, "feature provenance|weak reacquire|selected"):
                analyzer._audit_capture_contract(
                    captures, attempts, commands, feature_ids, run=run,
                    physical_contract=plan["measurement"]["physical_capture_audit"], plan=plan,
                )

    def test_finalizer_branch_matrix_is_deterministic_and_never_implies_formal_eligibility(self):
        cases = {
            "R-PASS": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-REFERENCE-EPOCH": ({"failure_branch": None, "reference_epoch_shift": True}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-REFERENCE-UNSTABLE": ({"failure_branch": "R-REFERENCE-UNSTABLE", "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-STRIP-CLASS-HIGH": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": ["sat100_fullscale"]}, {"failure_branch": None}),
            "uncertainty_unresolved": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": "uncertainty_unresolved", "classes_above_p1_floor": []}, {"failure_branch": None}),
        }
        for expected, (ray, strip, joint) in cases.items():
            branch = analyzer.select_reference_repeatability_branch(
                ray_analysis=ray, strip_analysis=strip, joint_report=joint,
            )
            self.assertEqual(branch, expected)

    def test_strip_ab_block_shift_is_reported_separately_from_within_block_noise(self):
        manifold = RayHsiManifold.load()
        policy = analyzer.HsiPolicyV2.load(subject.DEFAULT_POLICY)
        states = {
            "h0-s0-fullscale": (0, 0),
            "h120-s100-fullscale": (120, 100),
            "h120-s50-fullscale": (120, 50),
            "h300-s100-fullscale": (300, 100),
            "h0-s0-scale-relaxed-3072": (0, 0),
        }
        current = {}
        for key, state in states.items():
            center = dict(manifold.target_at(*state).features)
            current[key] = {"A": [dict(center) for _ in range(5)], "B": [dict(center) for _ in range(5)]}
        shifted_feature = manifold.coordinate_feature_ids[0]
        for row in current["h120-s50-fullscale"]["B"]:
            row[shifted_feature] *= 1.5
        report, _components = analyzer._analyze_strip(
            current, policy=policy, feature_ids=manifold.coordinate_feature_ids,
            seed=11, monte_carlo_samples=1000,
        )
        failure = next(item for item in report["failed_commands"] if item["command"] == "h120-s50-fullscale")
        self.assertEqual(failure["audit_status"], "pass")
        self.assertEqual(failure["block_center_shift"], "fail")


def _execute_fake(
    plan, root: Path, *, fail_at: int | None = None,
    weak_at: int | None = None, mismatch_reacquire: bool = False,
    cleanup_ok: bool = True, nonzero_off: bool = False,
):
    manifold = RayHsiManifold.load()
    ray_state = {}
    ray_set_calls = 0
    force_readback_mismatch = False
    strip_generation = 0
    curve = json.loads(Path(plan["inputs"]["code_duty_curve"]["path"]).read_text(encoding="utf-8"))

    def capture_step(step):
        if fail_at is not None and int(step["index"]) == fail_at:
            raise RuntimeError("injected capture failure")
        capture_id = step["capture_id"]
        raw = root / "camera" / f"{capture_id}.cr3"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"CR3")
        if step["source"] == "ray":
            target = manifold.target_at(step["ray"]["hue"], step["ray"]["sat"])
        elif step["source"] == "strip":
            key = next(key for key, command in plan["commands"].items() if command == step["strip_command"])
            state = {
                "h0-s0-fullscale": (0, 0), "h120-s100-fullscale": (120, 100),
                "h120-s50-fullscale": (120, 50), "h300-s100-fullscale": (300, 100),
                "h0-s0-scale-relaxed-3072": (0, 0),
            }[key]
            target = manifold.target_at(*state)
        else:
            target = manifold.target_at(0, 0)
        values = {feature: target.features[feature] for feature in manifold.coordinate_feature_ids}
        report = root / "measurements" / f"{capture_id}.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report_value = _report(values, raw)
        if weak_at is not None and int(step["index"]) == weak_at and step["capture_id"].endswith("-base"):
            plane = report_value["patches"][0]["planes"]["G1"]
            plane["quality"]["status"] = "rejected"
            plane["metrics"]["near_noise_floor_fraction"] = 0.1
        report.write_text(json.dumps(report_value), encoding="utf-8")
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
        nonlocal ray_set_calls, force_readback_mismatch
        ray_set_calls += 1
        force_readback_mismatch = mismatch_reacquire and ray_set_calls == 2
        ray_state.update({"hue": hue, "sat": sat, "intensity": int(intensity_percent * 10)})
        return {"code": 0, "data": dict(ray_state)}

    def ray_get_hsi():
        state = dict(ray_state)
        if force_readback_mismatch:
            state["hue"] = (int(state["hue"]) + 1) % 360
        return {"code": 0, "data": state}

    return subject.execute_targeted_reference_repeatability_plan(
        plan, run_dir=root, capture_step_fn=capture_step,
        strip_light_fn=strip_light,
        ray_off_fn=lambda: {"code": 0, "data": {"intensity": 1 if nonzero_off else 0}},
        ray_set_hsi_fn=ray_set_hsi,
        ray_get_hsi_fn=ray_get_hsi,
        sleep_fn=lambda _seconds: None,
        all_off_fn=lambda: [ShutdownStep("esphome", cleanup_ok), ShutdownStep("ray120c", True)],
    )


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
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": str(raw)},
        "exposure_metadata": {"status": "recorded"},
        "location_config": {"sha256": "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "observer_config": {"quality_thresholds": {"minimum_valid_pixels_per_plane": 29000, "maximum_nonfinite_fraction": 0.0, "maximum_clipped_fraction": 0.0, "maximum_near_noise_floor_fraction": 0.05}},
        "patches": [{
            "name": patch, "optimization_eligible": True,
            "planes": {
                plane: {
                    "quality": {"status": "accepted"},
                    "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                    "ambient_subtracted": {"trimmed_mean_per_second": float(planes.get(plane, 0.01))},
                } for plane in ("R", "G1", "G2", "B")
            },
        } for patch, planes in sorted(grouped.items())],
    }


def _make_fake_r1_wrapper_project(tempdir: Path):
    root = tempdir / "project"
    (root / "tmp").mkdir(parents=True)
    (root / ".venv/bin").mkdir(parents=True)
    (root / "config/location").mkdir(parents=True)
    source = Path(__file__).parents[1] / "tmp/run-hsi-reference-repeatability.zsh"
    wrapper = root / "tmp/run-hsi-reference-repeatability.zsh"
    shutil.copy2(source, wrapper)
    fake_python = root / ".venv/bin/python"
    fake_python.write_text("""#!/usr/bin/env python3
import json
import os
import signal
import sys
import time

with open(os.environ["FAKE_CALL_LOG"], "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\\n")
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])
if "camera_based_rgbww_optimizer.control.all_off" in sys.argv:
    print(json.dumps([{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]))
    if os.environ.get("FAKE_RUNNER_MODE") == "cleanup_failure":
        print("fake cleanup failed", file=sys.stderr)
        raise SystemExit(9)
    raise SystemExit(0)
mode = os.environ.get("FAKE_RUNNER_MODE", "success")
if mode in {"success", "cleanup_failure"}:
    raise SystemExit(0)
if mode == "failure":
    raise SystemExit(7)
for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(signum, lambda received, _frame: sys.exit(128 + received))
open(os.environ["FAKE_READY_FILE"], "w", encoding="utf-8").write("ready\\n")
time.sleep(30)
""", encoding="utf-8")
    fake_python.chmod(0o755)
    return root, wrapper, tempdir / "calls.log"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
