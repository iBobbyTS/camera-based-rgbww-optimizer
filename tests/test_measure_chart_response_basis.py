import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_chart_response_basis


ROOT = Path(__file__).resolve().parents[1]


class MeasureChartResponseBasisTests(unittest.TestCase):
    def _build(self, **overrides):
        kwargs = {
            "baseline_lut_path": "/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json",
            "location_config_path": ROOT / "config/location/locations-20260714-211759.json",
            "observer_config_path": ROOT / "config/camera/raw-observer.json",
            "curve_path": ROOT / "config/channel/code-duty-curve.json",
        }
        kwargs.update(overrides)
        return measure_chart_response_basis.build_chart_response_basis_plan(**kwargs)

    def test_plan_has_fixed_58_capture_coverage_and_four_plane_contract(self):
        plan = self._build()
        captures = plan["captures"]

        self.assertEqual(len(captures), 58)
        self.assertEqual(plan["measurement"]["feature_planes"], ["R", "G1", "G2", "B"])
        self.assertEqual(plan["measurement"]["raw_response_model"], "identity")
        self.assertEqual(plan["measurement"]["validated_exposure_envelope"]["maximum_factor"], 1.25)
        formal = [step for step in captures if step["purpose"] == "basis_formal"]
        self.assertEqual(len(formal), 45)
        states = {(step["analysis_context"]["channel"], step["analysis_context"]["target_code"]) for step in formal}
        self.assertEqual(len(states), 15)
        self.assertTrue(all(sum(step["strip_command"].values()) == step["analysis_context"]["target_code"] for step in formal))
        self.assertTrue(all(step["other_source_must_be_off"] for step in captures))
        self.assertEqual(sum(step["purpose"] == "anchor_check" for step in captures), 1)

    def test_plan_is_seed_deterministic_and_balanced(self):
        first = self._build(random_seed=123)
        second = self._build(random_seed=123)
        third = self._build(random_seed=124)
        first_states = [step["strip_command"] for step in first["captures"] if step["purpose"] == "basis_formal"]
        second_states = [step["strip_command"] for step in second["captures"] if step["purpose"] == "basis_formal"]
        third_states = [step["strip_command"] for step in third["captures"] if step["purpose"] == "basis_formal"]
        self.assertEqual(first_states, second_states)
        self.assertNotEqual(first_states, third_states)

    def test_dry_run_writes_only_plan_without_backend_creation(self):
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(
            measure_chart_response_basis.camera_remote,
            "create_camera_backend",
            side_effect=AssertionError("dry-run must not create backend"),
        ):
            output = measure_chart_response_basis.write_chart_response_basis_dry_run(
                output_root=tempdir,
                run_name="dry",
                baseline_lut_path="/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json",
                location_config_path=ROOT / "config/location/locations-20260714-211759.json",
                observer_config_path=ROOT / "config/camera/raw-observer.json",
                curve_path=ROOT / "config/channel/code-duty-curve.json",
            )
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(plan["status"], "dry_run")
            self.assertEqual(plan["devices"]["camera"]["backend"], "remote")

    def test_plan_rejects_non_remote_backend_and_unvalidated_observer(self):
        with self.assertRaisesRegex(ValueError, "camera_backend=remote"):
            self._build(camera_backend="local")
        with tempfile.TemporaryDirectory() as tempdir:
            observer = json.loads((ROOT / "config/camera/raw-observer.json").read_text(encoding="utf-8"))
            observer["statistics"]["combine_green"] = True
            path = Path(tempdir) / "observer.json"
            path.write_text(json.dumps(observer), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "four-plane"):
                self._build(observer_config_path=path)

    def test_run_reuses_p1_safety_runtime_with_p2_phase(self):
        plan = self._build()
        backend = object()
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(
            measure_chart_response_basis.raw_validation,
            "build_native_raw_capture_step_fn",
            return_value=lambda _step: {},
        ) as build_capture, mock.patch.object(
            measure_chart_response_basis.raw_validation,
            "execute_raw_observer_validation_plan",
            return_value=Path(tempdir) / "run",
        ) as execute:
            result = measure_chart_response_basis.run_chart_response_basis(
                plan,
                output_root=tempdir,
                run_name="run",
                curve_path=ROOT / "config/channel/code-duty-curve.json",
                camera_backend=backend,
            )
        self.assertEqual(result, Path(tempdir) / "run")
        self.assertEqual(build_capture.call_args.kwargs["recorded_exposure_purpose"], "P2")
        self.assertEqual(execute.call_args.kwargs["phase"], "P2")
        self.assertIs(execute.call_args.kwargs["capture_step_fn"], build_capture.return_value)

    def test_p2_plan_uses_shared_executor_cleanup_for_both_lights(self):
        plan = self._build(settle_seconds=0, off_seconds=0)
        strip_calls = []
        ray_calls = []

        def strip(*values):
            strip_calls.append(values)
            return {"values": values}

        def ray(*args, **kwargs):
            ray_calls.append((args, kwargs))
            return {}

        with tempfile.TemporaryDirectory() as tempdir:
            run = measure_chart_response_basis.raw_validation.execute_raw_observer_validation_plan(
                plan,
                run_dir=Path(tempdir) / "run",
                strip_light_fn=strip,
                ray_set_cct_fn=ray,
                capture_step_fn=lambda step: {"capture_id": step["capture_id"]},
                sleep_fn=lambda _seconds: None,
                phase="P2",
            )
            run_json = json.loads((run / "run.json").read_text(encoding="utf-8"))
            cleanup = json.loads((run / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(run_json["phase"], "P2")
        self.assertEqual(run_json["status"], "complete")
        self.assertEqual(strip_calls[-1], (0, 0, 0, 0, 0))
        self.assertEqual(ray_calls[-1][1]["intensity"], 0)
        self.assertEqual([step["name"] for step in cleanup["steps"]], ["esphome", "ray120c"])


if __name__ == "__main__":
    unittest.main()
