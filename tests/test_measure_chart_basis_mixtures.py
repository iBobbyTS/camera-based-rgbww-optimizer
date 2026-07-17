import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_chart_basis_mixtures


ROOT = Path(__file__).resolve().parents[1]


class MeasureChartBasisMixturesTests(unittest.TestCase):
    def _build(self, **overrides):
        kwargs = {
            "basis_analysis_path": "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json",
            "baseline_lut_path": "/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json",
            "location_config_path": ROOT / "config/location/locations-20260714-211759.json",
            "observer_config_path": ROOT / "config/camera/raw-observer.json",
            "curve_path": ROOT / "config/channel/code-duty-curve.json",
        }
        kwargs.update(overrides)
        return measure_chart_basis_mixtures.build_chart_basis_mixtures_plan(**kwargs)

    def test_plan_has_fixed_24_mixtures_48_formal_captures_and_anchors(self):
        plan = self._build()
        formal = [step for step in plan["captures"] if step["purpose"] == "mixture_formal"]
        self.assertEqual(len(plan["measurement"]["fixed_mixtures"]), 24)
        self.assertEqual(len(formal), 48)
        self.assertEqual(len(plan["captures"]), 55)
        self.assertEqual(Counter(item["category"] for item in plan["measurement"]["fixed_mixtures"]), {
            "dominant_with_weak": 5, "white_rgb": 5, "high_load": 5, "lut_nearby": 5, "latin_hypercube": 4,
        })
        self.assertEqual(sum(step["purpose"] == "anchor_check" for step in plan["captures"]), 3)
        self.assertEqual({step["repeat_index"] for step in formal}, {0, 1})
        self.assertTrue(all(step["other_source_must_be_off"] for step in plan["captures"]))
        self.assertEqual(plan["measurement"]["level_dependent_channels"], ["cw", "ww", "r", "g", "b"])

    def test_plan_is_deterministic_but_seed_changes_acquisition_order_only(self):
        first = self._build(random_seed=10)
        second = self._build(random_seed=10)
        third = self._build(random_seed=11)
        self.assertEqual(first["measurement"]["fixed_mixtures"], second["measurement"]["fixed_mixtures"])
        self.assertNotEqual(first["measurement"]["fixed_mixtures"], third["measurement"]["fixed_mixtures"])
        first_commands = {tuple(item["command"].items()) for item in first["measurement"]["fixed_mixtures"]}
        third_commands = {tuple(item["command"].items()) for item in third["measurement"]["fixed_mixtures"]}
        self.assertEqual(first_commands, third_commands)

    def test_dry_run_does_not_create_remote_backend(self):
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(
            measure_chart_basis_mixtures.camera_remote,
            "create_camera_backend",
            side_effect=AssertionError("dry-run must not create backend"),
        ):
            output = measure_chart_basis_mixtures.write_chart_basis_mixtures_dry_run(
                output_root=tempdir, run_name="dry", **{
                    "basis_analysis_path": "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json",
                    "baseline_lut_path": "/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json",
                    "location_config_path": ROOT / "config/location/locations-20260714-211759.json",
                    "observer_config_path": ROOT / "config/camera/raw-observer.json",
                    "curve_path": ROOT / "config/channel/code-duty-curve.json",
                }
            )
            plan = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["devices"]["camera"]["backend"], "remote")

    def test_rejects_local_backend_and_basis_location_mismatch(self):
        with self.assertRaisesRegex(ValueError, "camera_backend=remote"):
            self._build(camera_backend="local")
        basis_path = Path("/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json")
        basis = json.loads(basis_path.read_text(encoding="utf-8"))
        basis["location_config_sha256"] = "different"
        with tempfile.TemporaryDirectory() as tempdir:
            changed = Path(tempdir) / "basis.json"
            changed.write_text(json.dumps(basis), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "location hashes"):
                self._build(basis_analysis_path=changed)

    def test_run_reuses_shared_remote_capture_and_cleanup_executor(self):
        plan = self._build()
        backend = object()
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(
            measure_chart_basis_mixtures.raw_validation, "build_native_raw_capture_step_fn", return_value=lambda _step: {}
        ) as build_capture, mock.patch.object(
            measure_chart_basis_mixtures.raw_validation, "execute_raw_observer_validation_plan", return_value=Path(tempdir) / "run"
        ) as execute:
            result = measure_chart_basis_mixtures.run_chart_basis_mixtures(
                plan, output_root=tempdir, run_name="run",
                curve_path=ROOT / "config/channel/code-duty-curve.json", camera_backend=backend,
            )
        self.assertEqual(result, Path(tempdir) / "run")
        self.assertEqual(build_capture.call_args.kwargs["recorded_exposure_purpose"], "P3")
        self.assertEqual(execute.call_args.kwargs["phase"], "P3")


if __name__ == "__main__":
    unittest.main()
