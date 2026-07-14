import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation


def write_lut(path: Path) -> None:
    targets = []
    for cct in (3200, 5600):
        for gm in (0, 100):
            targets.append(
                {
                    "cct": cct,
                    "gm": gm,
                    "selected_command": {"cw": cct // 2, "ww": gm + 10, "r": 0, "g": 0, "b": 4095},
                }
            )
    path.write_text(json.dumps({"targets": targets}), encoding="utf-8")


class RawObserverValidationPlanTests(unittest.TestCase):
    def test_dry_run_writes_only_immutable_plan_without_device_calls(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            lut = root / "lut.json"
            location = root / "locations.json"
            observer = root / "observer.json"
            write_lut(lut)
            location.write_text("{}", encoding="utf-8")
            observer.write_text("{}", encoding="utf-8")

            output = measure_raw_observer_validation.write_raw_observer_validation_dry_run(
                output_root=root,
                run_name="dry",
                baseline_lut_path=lut,
                location_config_path=location,
                observer_config_path=observer,
                paired_repeats=2,
                linearity_factors=(0.5, 1.0, 2.0),
                linearity_repeats=2,
                off_seconds=1.0,
                settle_seconds=60.0,
                include_flat_field=True,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(output, root / "dry" / "plan.json")
            self.assertEqual(sorted(path.name for path in (root / "dry").iterdir()), ["plan.json"])
            self.assertEqual(data["status"], "dry_run")
            self.assertEqual(data["measurement"]["anchor"]["strip_command"]["cw"], 2800)
            self.assertEqual(data["captures"][0]["source"], "ambient")
            self.assertEqual(data["captures"][1]["source"], "ray")
            self.assertEqual(data["captures"][2]["source"], "strip")
            paired = [item for item in data["captures"] if item["purpose"] == "paired_repeat"]
            linearity = [item for item in data["captures"] if item["purpose"] == "linearity_bracket"]
            self.assertEqual(len(paired), 4)
            self.assertEqual(len(linearity), 12)
            self.assertTrue(all(item["other_source_must_be_off"] for item in data["captures"]))

    def test_plan_rejects_missing_baseline_factor_and_invalid_repeat_count(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            lut = root / "lut.json"
            location = root / "locations.json"
            observer = root / "observer.json"
            write_lut(lut)
            location.write_text("{}", encoding="utf-8")
            observer.write_text("{}", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "include 1.0"):
                measure_raw_observer_validation.build_raw_observer_validation_plan(
                    baseline_lut_path=lut,
                    location_config_path=location,
                    observer_config_path=observer,
                    linearity_factors=(0.5, 2.0),
                )
            with self.assertRaisesRegex(ValueError, "paired_repeats"):
                measure_raw_observer_validation.build_raw_observer_validation_plan(
                    baseline_lut_path=lut,
                    location_config_path=location,
                    observer_config_path=observer,
                    paired_repeats=0,
                )

    def test_cli_requires_dry_run_and_explicit_lut(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                measure_raw_observer_validation.parse_args([])
            with self.assertRaises(SystemExit):
                measure_raw_observer_validation.parse_args(["--baseline-lut", "lut.json"])


if __name__ == "__main__":
    unittest.main()
