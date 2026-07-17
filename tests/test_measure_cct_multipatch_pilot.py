import json
import copy
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.control import all_off

from camera_based_rgbww_optimizer.optimization import measure_cct_multipatch_pilot
from camera_based_rgbww_optimizer.optimization.multipatch_objective import (
    RejectedOptimizationFeaturesError,
)


ROOT = Path(__file__).resolve().parents[1]


class MeasureCctMultipatchPilotTests(unittest.TestCase):
    def _fake_executor_inputs(self, root, plan, *, fail=False):
        light_calls = []
        ray_calls = []

        def light(cw, ww, r, g, b):
            command = {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}
            light_calls.append(command)
            return command

        def ray(cct, **kwargs):
            ray_calls.append((cct, kwargs))
            return {"data": {"cct": cct, **kwargs}}

        capture_count = 0

        def capture(step):
            nonlocal capture_count
            capture_count += 1
            if fail and capture_count == 2:
                raise RuntimeError("synthetic capture failure")
            raw = Path(root) / f"capture-{capture_count}.cr3"
            raw.write_bytes(b"raw")
            report = Path(root) / f"capture-{capture_count}.json"
            report.write_text(json.dumps({"step": step}), encoding="utf-8")
            return {
                "patch_statistics": str(report),
                "capture": {"saved_file": str(raw), "shutter_speed": "1/100"},
                "quality": {"status": "accepted"},
            }

        def observation(report, *, raw_file):
            index = int(report["step"]["analysis_context"]["target_index"])
            target = plan["targets"][index]
            values = {
                feature: float(feature_index + 1)
                for feature_index, feature in enumerate(
                    [
                        *plan["measurement"]["feature_split"]["neutral"],
                        *plan["measurement"]["feature_split"]["training"],
                        *plan["measurement"]["feature_split"]["holdout"],
                    ]
                )
            }
            return {
                "feature_values": values,
                "white_point": {"cct_K": float(target["cct_K"]), "duv": 0.0},
                "location_config_sha256": plan["inputs"]["location_config"]["sha256"],
                "plane_order": ["R", "G1", "G2", "B"],
            }

        def shutdown(**kwargs):
            kwargs["strip_off_fn"]()
            kwargs["ray_set_cct_fn"](kwargs["ray_cct"], intensity=0, gm=kwargs["ray_gm"])
            return [all_off.ShutdownStep("esphome", True), all_off.ShutdownStep("ray120c", True)]

        return capture, light, ray, observation, shutdown, light_calls, ray_calls

    def test_plan_freezes_grid_split_remote_and_double_cleanup(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        self.assertEqual(plan["measurement"]["target_count"], 12)
        self.assertEqual(plan["measurement"]["feature_count"], 92)
        self.assertEqual(len(plan["formal_capture_protocol"]), 84)
        self.assertEqual(plan["devices"]["camera"]["backend"], "remote")
        self.assertTrue(all(item["other_source_must_be_off"] for item in plan["formal_capture_protocol"]))
        self.assertIn("python", plan["cleanup"])
        self.assertIn("shell", plan["cleanup"])
        self.assertTrue(all(max(target["baseline_command"].values()) == 4095 for target in plan["targets"]))

    def test_dry_run_is_offline_and_atomic(self):
        with tempfile.TemporaryDirectory() as tempdir:
            output = measure_cct_multipatch_pilot.write_cct_multipatch_pilot_dry_run(
                output_root=tempdir, run_name="dry"
            )
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(output.with_suffix(".json.tmp").exists())
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["measurement"]["execution_status"], "hardware_runner_code_complete_waiting_for_dry_run_safety_review")

    def test_shell_wrapper_has_independent_trap_cleanup(self):
        wrapper = (ROOT / "tmp/run-cct-multipatch-pilot.zsh").read_text(encoding="utf-8")
        self.assertIn("trap cleanup EXIT", wrapper)
        self.assertIn("control.all_off --json", wrapper)
        self.assertIn("--execute --allow-high-output --camera-backend remote", wrapper)
        self.assertIn(".wrapper.pid", wrapper)
        self.assertIn(".started-at.txt", wrapper)
        self.assertIn("unsetopt BG_NICE", wrapper)

    def test_rejects_local_backend_and_changed_location(self):
        with self.assertRaisesRegex(ValueError, "camera_backend=remote"):
            measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan(camera_backend="local")
        with tempfile.TemporaryDirectory() as tempdir:
            changed = Path(tempdir) / "location.json"
            changed.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen hash"):
                measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan(location_config_path=changed)

    def test_executor_completes_all_targets_with_source_isolation_and_cleanup(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            run_dir = root / "run"
            inputs = self._fake_executor_inputs(root, plan)
            capture, light, ray, observation, shutdown, light_calls, ray_calls = inputs
            result = measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                plan, run_dir=run_dir, capture_step_fn=capture,
                strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                all_off_fn=shutdown, observation_fn=observation,
            )
            run = json.loads((result / "run.json").read_text(encoding="utf-8"))
            captures = (result / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            targets = (result / "target-results.jsonl").read_text(encoding="utf-8").splitlines()
            cleanup = json.loads((result / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(run["status"], "complete")
        self.assertEqual(run["completed_target_count"], 12)
        self.assertGreaterEqual(len(captures), 85)
        self.assertEqual(len(targets), 12)
        self.assertTrue(all(step["ok"] for step in cleanup["steps"]))
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1][1]["intensity"], 0)

    def test_executor_failure_preserves_evidence_and_runs_python_cleanup(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            run_dir = root / "run"
            capture, light, ray, observation, shutdown, light_calls, ray_calls = self._fake_executor_inputs(root, plan, fail=True)
            with self.assertRaisesRegex(RuntimeError, "synthetic capture failure"):
                measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                    plan, run_dir=run_dir, capture_step_fn=capture,
                    strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                    all_off_fn=shutdown, observation_fn=observation,
                )
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertTrue((run_dir / "failure.json").is_file())
            self.assertTrue((run_dir / "all-off-python.json").is_file())
        self.assertEqual(run["status"], "failed")
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1][1]["intensity"], 0)

    def test_executor_rejects_input_hash_drift_before_device_calls(self):
        plan = copy.deepcopy(measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan())
        plan["inputs"]["pilot_config"]["sha256"] = "changed"
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(ValueError, "hash changed"):
            measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                plan,
                run_dir=Path(tempdir) / "run",
                capture_step_fn=lambda _step: {},
                strip_light_fn=lambda *_args: (_ for _ in ()).throw(AssertionError("device call")),
                ray_set_cct_fn=lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("device call")),
            )

    def test_executor_reacquires_only_weak_signal_rejection_at_1_25x(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            capture, light, ray, base_observation, shutdown, _light_calls, _ray_calls = self._fake_executor_inputs(root, plan)
            rejected_once = False

            def observation(report, *, raw_file):
                nonlocal rejected_once
                step = report["step"]
                if step["source"] == "strip" and step["exposure_factor"] is None and not rejected_once:
                    rejected_once = True
                    raise RejectedOptimizationFeaturesError(
                        [{"feature_id": "block_24::B"}], weak_signal_only=True
                    )
                return base_observation(report, raw_file=raw_file)

            run_dir = root / "run"
            measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                plan, run_dir=run_dir, capture_step_fn=capture,
                strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                all_off_fn=shutdown, observation_fn=observation,
            )
            captures = [json.loads(line) for line in (run_dir / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            commands = [json.loads(line) for line in (run_dir / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
        weak = [item for item in captures if item["purpose"].endswith("weak-signal-reacquire")]
        self.assertEqual(len(weak), 1)
        self.assertEqual(sum(item["event"] == "weak_signal_reacquire" for item in commands), 1)

    def test_executor_records_unreachable_ray_reference_after_validated_reacquire(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            capture, light, ray, base_observation, shutdown, _light_calls, _ray_calls = self._fake_executor_inputs(root, plan)

            def observation(report, *, raw_file):
                step = report["step"]
                if step["source"] == "ray" and step["analysis_context"]["target_index"] == 0:
                    raise RejectedOptimizationFeaturesError(
                        [{"feature_id": "block_02::B", "metrics": {"near_noise_floor_fraction": 0.2}}],
                        weak_signal_only=True,
                    )
                return base_observation(report, raw_file=raw_file)

            run_dir = root / "run"
            measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                plan, run_dir=run_dir, capture_step_fn=capture,
                strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                all_off_fn=shutdown, observation_fn=observation,
            )
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            rows = [json.loads(line) for line in (run_dir / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(run["status"], "complete")
        self.assertEqual(run["completed_target_count"], 12)
        self.assertEqual(rows[0]["status"], "measurement_unreachable")
        self.assertEqual(rows[0]["validated_exposure_envelope"], [1.0, 1.25])
        self.assertEqual(len(rows[0]["evidence"]["capture_ids"]), 2)
        self.assertTrue(all(row.get("status") == "complete" for row in rows[1:]))

    def test_executor_records_unreachable_strip_baseline_after_validated_reacquire(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            capture, light, ray, base_observation, shutdown, _light_calls, _ray_calls = self._fake_executor_inputs(root, plan)

            def observation(report, *, raw_file):
                step = report["step"]
                if (
                    step["source"] == "strip"
                    and step["analysis_context"]["target_index"] == 0
                    and step["purpose"].startswith("baseline_observation")
                ):
                    raise RejectedOptimizationFeaturesError(
                        [{"feature_id": "block_24::B", "metrics": {"near_noise_floor_fraction": 0.2}}],
                        weak_signal_only=True,
                    )
                return base_observation(report, raw_file=raw_file)

            run_dir = root / "run"
            measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                plan, run_dir=run_dir, capture_step_fn=capture,
                strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                all_off_fn=shutdown, observation_fn=observation,
            )
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            rows = [json.loads(line) for line in (run_dir / "target-results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(run["status"], "complete")
        self.assertEqual(rows[0]["status"], "measurement_unreachable")
        self.assertEqual(rows[0]["stage"], "strip_baseline")
        self.assertEqual(rows[0]["evidence"]["source"], "strip")
        self.assertTrue(all(row.get("status") == "complete" for row in rows[1:]))

    def test_executor_does_not_downgrade_mixed_reacquire_failure(self):
        plan = measure_cct_multipatch_pilot.build_cct_multipatch_pilot_plan()
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            capture, light, ray, _base_observation, shutdown, _light_calls, _ray_calls = self._fake_executor_inputs(root, plan)

            def observation(report, *, raw_file):
                step = report["step"]
                raise RejectedOptimizationFeaturesError(
                    [{"feature_id": "block_02::B"}],
                    weak_signal_only=step["exposure_factor"] is None,
                )

            run_dir = root / "run"
            with self.assertRaises(RejectedOptimizationFeaturesError):
                measure_cct_multipatch_pilot.execute_cct_multipatch_pilot_plan(
                    plan, run_dir=run_dir, capture_step_fn=capture,
                    strip_light_fn=light, ray_set_cct_fn=ray, sleep_fn=lambda _seconds: None,
                    all_off_fn=shutdown, observation_fn=observation,
                )
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertTrue((run_dir / "failure.json").is_file())
        self.assertEqual(run["status"], "failed")

if __name__ == "__main__":
    unittest.main()
