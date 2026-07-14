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

    def test_execute_plan_keeps_sources_isolated_and_writes_a_complete_run(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            strip_calls: list[tuple[int, int, int, int, int]] = []
            ray_calls: list[tuple[int, float, int]] = []
            sleeps: list[float] = []
            captured: list[str] = []

            def strip(cw, ww, r, g, b):
                strip_calls.append((cw, ww, r, g, b))
                return {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}

            def ray(cct, *, intensity, gm, **_kwargs):
                ray_calls.append((cct, intensity, gm))
                return {"cct": cct, "intensity": intensity, "gm": gm}

            def capture(step):
                captured.append(str(step["capture_id"]))
                return {"raw": f"{step['capture_id']}.cr3"}

            run_dir = measure_raw_observer_validation.execute_raw_observer_validation_plan(
                plan,
                run_dir=root / "run",
                strip_light_fn=strip,
                ray_set_cct_fn=ray,
                capture_step_fn=capture,
                sleep_fn=sleeps.append,
            )

            self.assertEqual(run_dir, root / "run")
            self.assertEqual(len(captured), len(plan["captures"]))
            self.assertIn((0, 0, 0, 0, 0), strip_calls)
            self.assertIn((5600, 100.0, 100), ray_calls)
            self.assertEqual(ray_calls[-1], (5600, 0, 100))
            self.assertEqual(strip_calls[-1], (0, 0, 0, 0, 0))
            self.assertIn(1.0, sleeps)
            self.assertIn(60.0, sleeps)
            self.assertEqual(json.loads((run_dir / "run.json").read_text(encoding="utf-8"))["status"], "complete")
            self.assertEqual(len((run_dir / "captures.jsonl").read_text(encoding="utf-8").splitlines()), len(captured))
            cleanup = json.loads((run_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual([item["name"] for item in cleanup["steps"]], ["esphome", "ray120c"])
            self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_execute_plan_failure_still_attempts_both_final_shutdowns(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            strip_calls: list[tuple[int, int, int, int, int]] = []
            ray_calls: list[tuple[int, float, int]] = []

            def strip(cw, ww, r, g, b):
                strip_calls.append((cw, ww, r, g, b))
                return {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}

            def ray(cct, *, intensity, gm, **_kwargs):
                ray_calls.append((cct, intensity, gm))
                return {"cct": cct, "intensity": intensity, "gm": gm}

            with self.assertRaisesRegex(RuntimeError, "camera failed"):
                measure_raw_observer_validation.execute_raw_observer_validation_plan(
                    plan,
                    run_dir=root / "failed",
                    strip_light_fn=strip,
                    ray_set_cct_fn=ray,
                    capture_step_fn=lambda _step: (_ for _ in ()).throw(RuntimeError("camera failed")),
                    sleep_fn=lambda _seconds: None,
                )

            failed_dir = root / "failed"
            self.assertTrue((failed_dir / "failure.json").is_file())
            self.assertEqual(json.loads((failed_dir / "run.json").read_text(encoding="utf-8"))["status"], "failed")
            self.assertEqual(strip_calls[-1], (0, 0, 0, 0, 0))
            self.assertEqual(ray_calls[-1], (5600, 0, 100))
            cleanup = json.loads((failed_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual([item["name"] for item in cleanup["steps"]], ["esphome", "ray120c"])

    def test_execute_plan_marks_run_failed_when_cleanup_runner_raises(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)

            run_dir = measure_raw_observer_validation.execute_raw_observer_validation_plan(
                plan,
                run_dir=root / "cleanup-failed",
                strip_light_fn=lambda *_values: {},
                ray_set_cct_fn=lambda *_args, **_kwargs: {},
                capture_step_fn=lambda _step: {"raw": "ok.cr3"},
                sleep_fn=lambda _seconds: None,
                all_off_fn=lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("cleanup failed")),
            )

            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            cleanup = json.loads((run_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual(run["status"], "failed")
            self.assertEqual(cleanup["cleanup_exception"]["type"], "RuntimeError")

    def test_native_capture_adapter_keeps_source_caches_and_uses_raw_reports(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            camera_dir = root / "camera"
            measurements_dir = root / "measurements"
            auto_calls = []
            fixed_calls = []

            class MeterResult:
                exposure_metric = 42000
                raw_visible_max = 15000
                plane_max = {"R": 0.60, "G1": 0.62, "G2": 0.61, "B": 0.58}

                def to_jsonable(self):
                    return {"quality_status": "pending_thresholds"}

            def capture(**kwargs):
                fixed_calls.append(kwargs)
                output = Path(kwargs["output_dir"])
                output.mkdir(parents=True, exist_ok=True)
                saved = output / kwargs["filename_template"].replace("%C", "cr3")
                saved.write_bytes(b"fake cr3")
                return measure_raw_observer_validation.camera_gphoto2.CaptureResult(
                    connection=measure_raw_observer_validation.camera_gphoto2.CameraConnection("test camera", "usb:test"),
                    settings=kwargs["settings"],
                    saved_file=saved,
                    stdout="",
                )

            def auto_expose(**kwargs):
                auto_calls.append(kwargs)
                kwargs["meter_fn"](root / "meter.cr3")
                shutter = "1/125" if "source-ray" in kwargs["filename_template"] else "1/60"
                return measure_raw_observer_validation.camera_gphoto2.AutoExposureResult(
                    target_max=kwargs["target_max"],
                    final_capture=capture(
                        output_dir=kwargs["output_dir"],
                        filename_template=kwargs["filename_template"],
                        settings=measure_raw_observer_validation.camera_gphoto2.CaptureSettings(
                            iso=kwargs["iso"],
                            aperture=kwargs["aperture"],
                            shutter_speed=shutter,
                            image_format=kwargs["image_format"],
                        ),
                    ),
                    trials=(),
                )

            def write_report(path, report):
                output = Path(path)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(report), encoding="utf-8")
                return output

            adapter = measure_raw_observer_validation.build_native_raw_capture_step_fn(
                camera_dir=camera_dir,
                measurements_dir=measurements_dir,
                scratch_dir=root / "scratch",
                location_config_path=root / "locations.json",
                observer_config_path=root / "observer.json",
                auto_expose_fn=auto_expose,
                capture_fn=capture,
                raw_meter_fn=lambda *_args, **_kwargs: MeterResult(),
                raw_analyze_fn=lambda *_args, **_kwargs: {"quality": {"status": "pending_thresholds"}},
                raw_report_writer=write_report,
                shutter_choices_fn=lambda _port: ("1/250", "1/125", "1/60"),
            )
            ambient = plan["captures"][0]
            ray_baseline = plan["captures"][1]
            strip_baseline = plan["captures"][2]
            ray_pair = next(step for step in plan["captures"] if step["purpose"] == "paired_repeat" and step["source"] == "ray")
            strip_bracket = next(
                step
                for step in plan["captures"]
                if step["purpose"] == "linearity_bracket" and step["source"] == "strip" and step["exposure_factor"] == 0.5
            )

            ambient_result = adapter(ambient)
            ray_result = adapter(ray_baseline)
            strip_result = adapter(strip_baseline)
            pair_result = adapter(ray_pair)
            bracket_result = adapter(strip_bracket)

            self.assertEqual(ambient_result["mode"], "ambient_fixed")
            self.assertEqual(ray_result["mode"], "native_auto_exposure")
            self.assertEqual(strip_result["mode"], "native_auto_exposure")
            self.assertEqual(pair_result["mode"], "fixed_cached")
            self.assertEqual(bracket_result["mode"], "fixed_bracket")
            self.assertEqual([call["initial_shutter_speed"] for call in auto_calls], [None, None])
            self.assertTrue(all(call["decode_formats"] == () for call in auto_calls))
            self.assertEqual(fixed_calls[-1]["settings"].shutter_speed, "1/125")
            self.assertEqual(len(list(measurements_dir.glob("*.patch-statistics.json"))), 5)
            self.assertEqual(list(root.rglob("*.npy")), [])

    def _plan(self, root: Path):
        lut = root / "lut.json"
        location = root / "locations.json"
        observer = root / "observer.json"
        write_lut(lut)
        location.write_text("{}", encoding="utf-8")
        observer.write_text("{}", encoding="utf-8")
        return measure_raw_observer_validation.build_raw_observer_validation_plan(
            baseline_lut_path=lut,
            location_config_path=location,
            observer_config_path=observer,
            paired_repeats=1,
            linearity_factors=(0.5, 1.0),
            linearity_repeats=1,
        )


if __name__ == "__main__":
    unittest.main()
