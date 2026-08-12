import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.measurement import recorded_exposure
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation


F0A_TEMP_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/test-runtime"
)
FAKE_RAY_ENV = {
    "AMARAN_OPENAPI_SECRET": "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="
}


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
                target_max=19661,
                min_shutter_speed="1/16000",
                max_shutter_speed="25",
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
            self.assertEqual(data["measurement"]["camera_auto_exposure"]["target_max"], 19661)
            self.assertEqual(data["measurement"]["camera_auto_exposure"]["min_shutter_speed"], "1/16000")
            self.assertEqual(data["measurement"]["camera_auto_exposure"]["max_shutter_speed"], "25")
            self.assertEqual(data["captures"][0]["source"], "ambient")
            self.assertEqual(data["captures"][1]["source"], "ray")
            self.assertEqual(data["captures"][2]["source"], "strip")
            self.assertEqual(data["measurement"]["flat_field"], {"status": "planned", "capture_id": data["captures"][-1]["capture_id"]})
            paired = [item for item in data["captures"] if item["purpose"] == "paired_repeat"]
            linearity = [item for item in data["captures"] if item["purpose"] == "linearity_bracket"]
            self.assertEqual(len(paired), 4)
            self.assertEqual(len(linearity), 12)
            self.assertTrue(all(item["other_source_must_be_off"] for item in data["captures"]))
            self.assertIn("default_white_lut", data["inputs"])
            self.assertIn("white_endpoints", data["inputs"])
            self.assertIn("code_duty_curve", data["inputs"])

    def test_plan_records_missing_flat_field_material_explicitly(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)

            self.assertEqual(
                plan["measurement"]["flat_field"],
                {"status": "not_available", "reason": "no_repeatable_flat_field_material"},
            )

            no_curve_plan = measure_raw_observer_validation.build_raw_observer_validation_plan(
                baseline_lut_path=plan["inputs"]["baseline_lut"]["path"],
                location_config_path=plan["inputs"]["location_config"]["path"],
                observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
                curve_path=None,
            )
            self.assertEqual(no_curve_plan["inputs"]["code_duty_curve"], {"status": "disabled"})

    def test_preflight_plan_stops_after_two_longest_bracket_checks(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            base = self._plan(root)
            plan = measure_raw_observer_validation.build_raw_observer_validation_plan(
                baseline_lut_path=base["inputs"]["baseline_lut"]["path"],
                location_config_path=base["inputs"]["location_config"]["path"],
                observer_config_path=base["inputs"]["raw_observer_config"]["path"],
                target_max=19661,
                linearity_factors=(0.5, 1.0, 1.5),
                preflight_only=True,
            )

            self.assertTrue(plan["measurement"]["preflight_only"])
            self.assertEqual(len(plan["captures"]), 5)
            checks = [step for step in plan["captures"] if step["purpose"] == "linearity_preflight"]
            self.assertEqual([step["source"] for step in checks], ["ray", "strip"])
            self.assertTrue(all(step["exposure_factor"] == 1.5 for step in checks))
            self.assertFalse(any(step["purpose"] == "paired_repeat" for step in plan["captures"]))
            self.assertEqual(plan["devices"]["camera"]["backend"], "remote")
            self.assertEqual(plan["inputs"]["location_config"]["sha256"], measure_raw_observer_validation.hashlib.sha256(Path(plan["inputs"]["location_config"]["path"]).read_bytes()).hexdigest())
            self.assertEqual(plan["cleanup"]["python"], "required_on_normal_exit_exception_and_keyboard_interrupt")
            self.assertEqual(plan["cleanup"]["shell"], "required_via_wrapper_trap")

    def test_boundary_confirmation_plan_omits_paired_repeats(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            base = self._plan(root)
            plan = measure_raw_observer_validation.build_raw_observer_validation_plan(
                baseline_lut_path=base["inputs"]["baseline_lut"]["path"],
                location_config_path=base["inputs"]["location_config"]["path"],
                observer_config_path=base["inputs"]["raw_observer_config"]["path"],
                linearity_factors=(1.0, 1.25),
                linearity_repeats=3,
                boundary_confirmation_only=True,
            )

            self.assertTrue(plan["measurement"]["boundary_confirmation_only"])
            self.assertFalse(plan["measurement"]["preflight_only"])
            self.assertEqual(plan["measurement"]["paired_repeats"], 0)
            self.assertEqual(len(plan["captures"]), 15)
            self.assertFalse(any(step["purpose"] == "paired_repeat" for step in plan["captures"]))
            brackets = [step for step in plan["captures"] if step["purpose"] == "linearity_bracket"]
            self.assertEqual(len(brackets), 12)
            self.assertEqual({step["exposure_factor"] for step in brackets}, {1.0, 1.25})

    def test_plan_rejects_preflight_and_boundary_confirmation_together(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            base = self._plan(root)
            with self.assertRaisesRegex(ValueError, "mutually exclusive"):
                measure_raw_observer_validation.build_raw_observer_validation_plan(
                    baseline_lut_path=base["inputs"]["baseline_lut"]["path"],
                    location_config_path=base["inputs"]["location_config"]["path"],
                    observer_config_path=base["inputs"]["raw_observer_config"]["path"],
                    preflight_only=True,
                    boundary_confirmation_only=True,
                )

    def test_remote_dry_run_never_constructs_backend_or_calls_lights(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            base = self._plan(root)
            args = [
                "--baseline-lut", base["inputs"]["baseline_lut"]["path"],
                "--location-config", base["inputs"]["location_config"]["path"],
                "--raw-observer-config", base["inputs"]["raw_observer_config"]["path"],
                "--camera-backend", "remote",
                "--min-shutter-speed", "1/16000",
                "--preflight-only",
                "--dry-run",
                "--output-dir", str(root / "output"),
                "--run-name", "remote-dry",
            ]
            with mock.patch.object(measure_raw_observer_validation.camera_remote, "create_camera_backend") as factory, \
                 mock.patch.object(measure_raw_observer_validation.esphome, "light") as strip, \
                 mock.patch.object(measure_raw_observer_validation.ray120c, "set_cct") as ray:
                self.assertEqual(measure_raw_observer_validation.main(args), 0)
            factory.assert_not_called()
            strip.assert_not_called()
            ray.assert_not_called()
            plan = json.loads((root / "output" / "remote-dry" / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["devices"]["camera"]["backend"], "remote")
            self.assertEqual(plan["measurement"]["camera_auto_exposure"]["min_shutter_speed"], "1/16000")

    def test_frozen_location_hash_mismatch_stops_before_capture_or_lights(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            Path(plan["inputs"]["location_config"]["path"]).write_text('{"changed":true}', encoding="utf-8")
            calls = []
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                measure_raw_observer_validation.execute_raw_observer_validation_plan(
                    plan,
                    run_dir=root / "run",
                    strip_light_fn=lambda *_values: calls.append("strip") or {},
                    ray_set_cct_fn=lambda *_args, **_kwargs: calls.append("ray") or {},
                    capture_step_fn=lambda _step: calls.append("capture") or {},
                    sleep_fn=lambda _seconds: None,
                )
            self.assertEqual(calls, [])

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

    def test_execute_requires_explicit_high_output_consent_before_hardware_runner(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            args = [
                "--baseline-lut",
                plan["inputs"]["baseline_lut"]["path"],
                "--location-config",
                plan["inputs"]["location_config"]["path"],
                "--raw-observer-config",
                plan["inputs"]["raw_observer_config"]["path"],
                "--execute",
            ]

            with self.assertRaisesRegex(ValueError, "allow-high-output"), mock.patch.object(
                measure_raw_observer_validation,
                "run_native_raw_observer_validation",
            ) as runner:
                measure_raw_observer_validation.main(args)

            runner.assert_not_called()

    def test_execute_calls_hardware_runner_only_after_explicit_consent(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            args = [
                "--baseline-lut",
                plan["inputs"]["baseline_lut"]["path"],
                "--location-config",
                plan["inputs"]["location_config"]["path"],
                "--raw-observer-config",
                plan["inputs"]["raw_observer_config"]["path"],
                "--execute",
                "--allow-high-output",
                "--output-dir",
                str(root / "output"),
                "--run-name",
                "run",
            ]

            with mock.patch.object(
                measure_raw_observer_validation,
                "run_native_raw_observer_validation",
                return_value=root / "output" / "run",
            ) as runner:
                self.assertEqual(measure_raw_observer_validation.main(args), 0)

            runner.assert_called_once()
            self.assertEqual(runner.call_args.kwargs["run_name"], "run")

    def test_native_runner_passes_frozen_shutter_bounds_to_capture_adapter(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            plan["measurement"]["camera_auto_exposure"].update(
                {"min_shutter_speed": "1/16000", "max_shutter_speed": "25"}
            )
            capture_step = mock.Mock()

            with mock.patch.object(
                measure_raw_observer_validation,
                "build_native_raw_capture_step_fn",
                return_value=capture_step,
            ) as build_capture, mock.patch.object(
                measure_raw_observer_validation,
                "execute_raw_observer_validation_plan",
                return_value=root / "run",
            ):
                output = measure_raw_observer_validation.run_native_raw_observer_validation(
                    plan,
                    output_root=root,
                    run_name="run",
                )

            self.assertEqual(output, root / "run")
            self.assertEqual(build_capture.call_args.kwargs["min_shutter_speed"], "1/16000")
            self.assertEqual(build_capture.call_args.kwargs["max_shutter_speed"], "25")

    def test_execute_plan_keeps_sources_isolated_and_writes_a_complete_run(self):
        with mock.patch.dict(os.environ, FAKE_RAY_ENV, clear=False), tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            strip_calls: list[tuple[int, int, int, int, int]] = []
            ray_calls: list[tuple[int, float | None, float | None, int]] = []
            sleeps: list[float] = []
            captured: list[str] = []

            def strip(cw, ww, r, g, b):
                strip_calls.append((cw, ww, r, g, b))
                return {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}

            def ray(cct, *, intensity=None, intensity_percent=None, gm, **_kwargs):
                ray_calls.append((cct, intensity, intensity_percent, gm))
                return {"cct": cct, "intensity": intensity, "intensity_percent": intensity_percent, "gm": gm}

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
            self.assertIn((5600, None, 100.0, 100), ray_calls)
            self.assertEqual(ray_calls[-1], (5600, 0, None, 100))
            self.assertEqual(strip_calls[-1], (0, 0, 0, 0, 0))
            self.assertIn(1.0, sleeps)
            self.assertIn(60.0, sleeps)
            self.assertEqual(json.loads((run_dir / "run.json").read_text(encoding="utf-8"))["status"], "complete")
            self.assertEqual(len((run_dir / "captures.jsonl").read_text(encoding="utf-8").splitlines()), len(captured))
            self.assertIn("Status: `complete`", (run_dir / "EXPERIMENT_SUMMARY.md").read_text(encoding="utf-8"))
            cleanup = json.loads((run_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual([item["name"] for item in cleanup["steps"]], ["esphome", "ray120c"])
            self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_execute_plan_failure_still_attempts_both_final_shutdowns(self):
        with mock.patch.dict(os.environ, FAKE_RAY_ENV, clear=False), tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            strip_calls: list[tuple[int, int, int, int, int]] = []
            ray_calls: list[tuple[int, float | None, float | None, int]] = []

            def strip(cw, ww, r, g, b):
                strip_calls.append((cw, ww, r, g, b))
                return {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}

            def ray(cct, *, intensity=None, intensity_percent=None, gm, **_kwargs):
                ray_calls.append((cct, intensity, intensity_percent, gm))
                return {"cct": cct, "intensity": intensity, "intensity_percent": intensity_percent, "gm": gm}

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
            self.assertIn("Status: `failed`", (failed_dir / "EXPERIMENT_SUMMARY.md").read_text(encoding="utf-8"))
            self.assertEqual(strip_calls[-1], (0, 0, 0, 0, 0))
            self.assertEqual(ray_calls[-1], (5600, 0, None, 100))
            cleanup = json.loads((failed_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual([item["name"] for item in cleanup["steps"]], ["esphome", "ray120c"])

    def test_execute_plan_records_pre_capture_provenance_and_cleans_up_when_it_fails(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            calls = []

            result = measure_raw_observer_validation.execute_raw_observer_validation_plan(
                plan,
                run_dir=root / "provenance",
                strip_light_fn=lambda *values: calls.append(("strip", values)) or {},
                ray_set_cct_fn=lambda *args, **kwargs: calls.append(("ray", args, kwargs)) or {},
                capture_step_fn=lambda _step: {"raw": "ok.cr3"},
                sleep_fn=lambda _seconds: None,
                provenance_fn=lambda: {"git": {"commit": "abc", "dirty": False}},
            )
            run = json.loads((result / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run["run_id"], "provenance")
            self.assertEqual(run["provenance"]["git"]["commit"], "abc")

            with self.assertRaisesRegex(RuntimeError, "preflight failed"):
                measure_raw_observer_validation.execute_raw_observer_validation_plan(
                    plan,
                    run_dir=root / "provenance-failed",
                    strip_light_fn=lambda *values: calls.append(("strip", values)) or {},
                    ray_set_cct_fn=lambda *args, **kwargs: calls.append(("ray", args, kwargs)) or {},
                    capture_step_fn=lambda _step: {"raw": "unexpected.cr3"},
                    sleep_fn=lambda _seconds: None,
                    provenance_fn=lambda: (_ for _ in ()).throw(RuntimeError("preflight failed")),
                )
            failed = root / "provenance-failed"
            self.assertEqual(json.loads((failed / "run.json").read_text(encoding="utf-8"))["status"], "failed")
            self.assertFalse((failed / "captures.jsonl").exists())
            self.assertTrue((failed / "all-off-python.json").is_file())

    def test_camera_summary_redacts_serial_number_and_derives_anonymous_id(self):
        identity = measure_raw_observer_validation._redact_camera_summary(
            """Camera summary:
Manufacturer: Canon.Inc
Model: Canon EOS R6 Mark III
  Version: 3-1.0.2
  Serial Number: private-camera-serial
Current Lens: RF24-70mm F2.8 L IS USM
Focal Length: 50mm
"""
        )

        rendered = json.dumps(identity, sort_keys=True)
        self.assertNotIn("private-camera-serial", rendered)
        self.assertEqual(identity["manufacturer"], "Canon.Inc")
        self.assertEqual(identity["lens"], "RF24-70mm F2.8 L IS USM")
        self.assertEqual(identity["focal_length"], "50mm")
        self.assertEqual(len(identity["anonymous_device_id_sha256"]), 64)

    def test_execute_plan_accepts_empty_shell_created_directory_but_never_reuses_a_nonempty_one(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            empty_run = root / "empty-run"
            empty_run.mkdir()
            result = measure_raw_observer_validation.execute_raw_observer_validation_plan(
                plan,
                run_dir=empty_run,
                strip_light_fn=lambda *_values: {},
                ray_set_cct_fn=lambda *_args, **_kwargs: {},
                capture_step_fn=lambda _step: {"raw": "ok.cr3"},
                sleep_fn=lambda _seconds: None,
            )
            self.assertEqual(result, empty_run)

            reused_run = root / "reused-run"
            reused_run.mkdir()
            (reused_run / "previous.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "must be empty"):
                measure_raw_observer_validation.execute_raw_observer_validation_plan(
                    plan,
                    run_dir=reused_run,
                    strip_light_fn=lambda *_values: {},
                    ray_set_cct_fn=lambda *_args, **_kwargs: {},
                    capture_step_fn=lambda _step: {"raw": "ok.cr3"},
                    sleep_fn=lambda _seconds: None,
                )

    def test_execute_plan_marks_run_failed_when_cleanup_runner_raises(self):
        with mock.patch.dict(os.environ, FAKE_RAY_ENV, clear=False), tempfile.TemporaryDirectory() as tempdir:
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

            def exposure(path, shutter):
                nominal = recorded_exposure.parse_nominal_exposure(shutter)
                return recorded_exposure.RecordedExposure(
                    seconds=nominal * 0.9375,
                    source="Canon:ExposureTime",
                    nominal_seconds=nominal,
                    nominal_shutter_speed=shutter,
                    raw_file=Path(path),
                    status="recorded",
                    metadata_values={"Canon:ExposureTime": nominal * 0.9375},
                )

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
                recorded_exposure_fn=exposure,
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
            weak_reacquire = {
                **strip_bracket,
                "capture_id": "weak-signal-reacquire",
                "purpose": "weak_signal_reacquire",
                "exposure_factor": 1.25,
            }

            ambient_result = adapter(ambient)
            ray_result = adapter(ray_baseline)
            strip_result = adapter(strip_baseline)
            pair_result = adapter(ray_pair)
            bracket_result = adapter(strip_bracket)
            weak_result = adapter(weak_reacquire)

            self.assertEqual(ambient_result["mode"], "ambient_fixed")
            self.assertEqual(ray_result["mode"], "native_auto_exposure")
            self.assertEqual(strip_result["mode"], "native_auto_exposure")
            self.assertEqual(pair_result["mode"], "fixed_cached")
            self.assertEqual(bracket_result["mode"], "fixed_bracket")
            self.assertEqual(weak_result["mode"], "fixed_bracket")
            self.assertEqual([call["initial_shutter_speed"] for call in auto_calls], [None, None])
            self.assertTrue(all(call["decode_formats"] == () for call in auto_calls))
            self.assertTrue(all(call["min_shutter_speed"] == "1/8000" for call in auto_calls))
            self.assertEqual(fixed_calls[-2]["settings"].shutter_speed, "1/125")
            self.assertEqual(fixed_calls[-1]["settings"].shutter_speed, "1/60")
            self.assertEqual(len(list(measurements_dir.glob("*.patch-statistics.json"))), 6)
            weak_report = json.loads(
                (measurements_dir / "weak-signal-reacquire.patch-statistics.json").read_text(encoding="utf-8")
            )
            self.assertEqual(weak_report["analysis_context"]["exposure_factor"], 1.25)
            stored_report = json.loads(
                (measurements_dir / f"{strip_bracket['capture_id']}.patch-statistics.json").read_text(encoding="utf-8")
            )
            self.assertEqual(stored_report["analysis_context"]["source"], "strip")
            self.assertEqual(stored_report["analysis_context"]["exposure_factor"], 0.5)
            self.assertEqual(stored_report["exposure_metadata"]["source"], "Canon:ExposureTime")
            self.assertAlmostEqual(stored_report["analysis_context"]["exposure_seconds"], 0.0075)
            self.assertEqual(list(root.rglob("*.npy")), [])

            frozen_adapter = measure_raw_observer_validation.build_native_raw_capture_step_fn(
                camera_dir=root / "frozen-camera",
                measurements_dir=root / "frozen-measurements",
                scratch_dir=root / "frozen-scratch",
                location_config_path=root / "locations.json",
                observer_config_path=root / "observer.json",
                capture_fn=capture,
                raw_analyze_fn=lambda *_args, **_kwargs: {"quality": {"status": "pending_thresholds"}},
                raw_report_writer=write_report,
                recorded_exposure_fn=exposure,
                frozen_shutter_by_cache={"ray": "1/320"},
            )
            frozen_adapter({**ambient, "capture_id": "frozen-ambient"})
            frozen_result = frozen_adapter({**ray_pair, "capture_id": "frozen-ray"})
            self.assertEqual(frozen_result["mode"], "fixed_cached")
            self.assertEqual(fixed_calls[-1]["settings"].shutter_speed, "1/320")

    def test_native_capture_adapter_reuses_one_injected_backend_for_auto_and_fixed_captures(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            class FakeRemoteBackend:
                def __init__(self):
                    self.choice_reads = []

                def read_shutter_current_and_choices(self, connection):
                    self.choice_reads.append(connection.port)
                    return "1/100", ["1/200", "1/160", "1/125", "1/100", "1/80", "1/60"]

            backend = FakeRemoteBackend()
            fixed_backends = []
            auto_backends = []

            def result_for(settings, filename):
                path = root / filename.replace("%C", "cr3")
                path.write_bytes(b"raw")
                return measure_raw_observer_validation.camera_gphoto2.CaptureResult(
                    connection=measure_raw_observer_validation.camera_gphoto2.CameraConnection("remote", "http://bridge"),
                    settings=settings,
                    saved_file=path,
                    stdout="{}",
                )

            def backend_capture(injected, **kwargs):
                fixed_backends.append(injected)
                return result_for(kwargs["settings"], kwargs["filename_template"])

            def auto_expose(**kwargs):
                auto_backends.append(kwargs["camera_backend"])
                settings = measure_raw_observer_validation.camera_gphoto2.CaptureSettings(
                    iso="125", aperture="implicit auto", shutter_speed="1/100", image_format="RAW"
                )
                return measure_raw_observer_validation.camera_gphoto2.AutoExposureResult(
                    target_max=kwargs["target_max"],
                    final_capture=result_for(settings, kwargs["filename_template"]),
                    trials=(),
                )

            def exposure(path, shutter):
                seconds = recorded_exposure.parse_nominal_exposure(shutter)
                return recorded_exposure.RecordedExposure(
                    seconds=seconds,
                    source="Canon:ExposureTime",
                    nominal_seconds=seconds,
                    nominal_shutter_speed=shutter,
                    raw_file=Path(path),
                    status="recorded",
                    metadata_values={"Canon:ExposureTime": seconds},
                )

            adapter = measure_raw_observer_validation.build_native_raw_capture_step_fn(
                camera_dir=root / "camera",
                measurements_dir=root / "measurements",
                scratch_dir=root / "scratch",
                location_config_path=root / "locations.json",
                observer_config_path=root / "observer.json",
                camera_backend=backend,
                auto_expose_fn=auto_expose,
                raw_meter_fn=lambda *_args, **_kwargs: mock.Mock(
                    exposure_metric=10000, raw_visible_max=10000,
                    plane_max={"R": 0.1, "G1": 0.1, "G2": 0.1, "B": 0.1},
                ),
                raw_analyze_fn=lambda *_args, **_kwargs: {"quality": {"status": "pending_thresholds"}},
                raw_report_writer=lambda path, report: Path(path),
                recorded_exposure_fn=exposure,
            )
            with mock.patch.object(
                measure_raw_observer_validation.camera_remote,
                "capture_with_backend",
                side_effect=backend_capture,
            ), mock.patch.object(
                measure_raw_observer_validation.camera_gphoto2,
                "read_config_choices",
                side_effect=AssertionError("remote bracket must not use local gphoto2"),
            ):
                adapter(plan["captures"][0])
                adapter(plan["captures"][1])
                paired = next(step for step in plan["captures"] if step["purpose"] == "paired_repeat" and step["source"] == "ray")
                adapter(paired)
                bracket = next(
                    step
                    for step in plan["captures"]
                    if step["purpose"] == "linearity_bracket" and step["source"] == "ray"
                )
                adapter(bracket)

            self.assertEqual(auto_backends, [backend])
            self.assertEqual(fixed_backends, [backend, backend, backend])
            self.assertEqual(backend.choice_reads, ["http://bridge"])

    def test_remote_provenance_records_setting_choices_without_credentials(self):
        settings = measure_raw_observer_validation.camera_remote.RemoteCameraSettings(
            iso=measure_raw_observer_validation.camera_remote.RemoteCameraSetting("100", ("100", "125")),
            aperture=measure_raw_observer_validation.camera_remote.RemoteCameraSetting(
                "implicit auto", ("implicit auto",)
            ),
            shutter_speed=measure_raw_observer_validation.camera_remote.RemoteCameraSetting(
                "1/100", ("1/200", "1/100", "1/50")
            ),
            image_format="RAW",
        )
        backend = measure_raw_observer_validation.camera_remote.RemoteCameraBackend(
            config=measure_raw_observer_validation.camera_remote.RemoteCameraConfig(
                "http://bridge.local:8088", "do-not-record-this-token"
            )
        )
        connection = measure_raw_observer_validation.camera_gphoto2.CameraConnection(
            "Canon EOS R6 Mark III via r6-camera-bridge", "http://bridge.local:8088"
        )
        with mock.patch.object(backend, "connect", return_value=connection), mock.patch.object(
            backend, "_load_settings", return_value=settings
        ), mock.patch.object(
            measure_raw_observer_validation, "_git_provenance", return_value={"commit": "abc", "dirty": False}
        ), mock.patch.object(
            measure_raw_observer_validation, "_rawpy_provenance", return_value={"status": "ok"}
        ), mock.patch.object(
            measure_raw_observer_validation, "_command_version", return_value={"status": "ok"}
        ), mock.patch.object(
            measure_raw_observer_validation.ray120c, "get_node_config", return_value={}
        ), mock.patch.object(
            measure_raw_observer_validation,
            "_read_esphome_device_info",
            new=mock.AsyncMock(return_value={"name": "strip"}),
        ):
            provenance = measure_raw_observer_validation.collect_native_raw_observer_provenance(
                curve_path=None,
                camera_backend=backend,
                backend_name="remote",
            )

        self.assertEqual(
            provenance["camera"]["capture_setting_choices"]["shutter_speed"],
            ["1/200", "1/100", "1/50"],
        )
        self.assertNotIn("do-not-record-this-token", json.dumps(provenance, sort_keys=True))

    def test_native_raw_no_ambient_policy_is_restricted_to_exact_p7_formal_owners(self):
        F0A_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=F0A_TEMP_ROOT) as tempdir:
            root = Path(tempdir)
            analyze_calls = []
            observer_calls = []

            def capture(*, output_dir, filename_template, settings, **_kwargs):
                saved = Path(output_dir) / filename_template.replace("%C", "cr3")
                saved.parent.mkdir(parents=True, exist_ok=True)
                saved.write_bytes(b"raw")
                return measure_raw_observer_validation.camera_gphoto2.CaptureResult(
                    connection=measure_raw_observer_validation.camera_gphoto2.CameraConnection(
                        "fake", "offline"
                    ),
                    settings=settings,
                    saved_file=saved,
                    stdout="",
                )

            def exposure(path, shutter):
                seconds = recorded_exposure.parse_nominal_exposure(shutter)
                return recorded_exposure.RecordedExposure(
                    seconds=seconds,
                    source="Canon:ExposureTime",
                    nominal_seconds=seconds,
                    nominal_shutter_speed=shutter,
                    raw_file=Path(path),
                    status="recorded",
                    metadata_values={"Canon:ExposureTime": seconds},
                )

            def analyze(*args, **kwargs):
                analyze_calls.append((args, kwargs))
                return {"quality": {"status": "accepted"}}

            def write_report(path, report):
                target = Path(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(report), encoding="utf-8")
                return target

            step = {
                "capture_id": "td-b-formal",
                "source": "ray",
                "purpose": "p7_td_b_formal",
                "repeat_index": 0,
                "source_exposure_cache": "ray-h120-s100",
                "auto_exposure": False,
                "physical_capture_budget_remaining": 1,
            }
            adapter = measure_raw_observer_validation.build_native_raw_capture_step_fn(
                camera_dir=root / "camera",
                measurements_dir=root / "measurements",
                scratch_dir=root / "scratch",
                location_config_path=root / "locations.json",
                observer_config_path=root / "observer.json",
                capture_fn=capture,
                raw_analyze_fn=analyze,
                raw_report_writer=write_report,
                recorded_exposure_fn=exposure,
                frozen_shutter_by_cache={"ray-h120-s100": "1/5000"},
                ambient_policy=(
                    measure_raw_observer_validation
                    .AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
                ),
                ambient_policy_owner=(
                    measure_raw_observer_validation
                    .TD_B_FORMAL_AMBIENT_POLICY_OWNER
                ),
                physical_return_observer=lambda returned, raw_step, count: (
                    observer_calls.append((returned.saved_file, raw_step["capture_id"], count))
                    or {"physical_index": 1}
                ),
            )
            result = adapter(step)
            report = json.loads(Path(result["patch_statistics"]).read_text(encoding="utf-8"))
            self.assertEqual(
                result["native_raw_ambient_policy"],
                measure_raw_observer_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
            )
            self.assertEqual(result["physical_return_receipt"], {"physical_index": 1})
            self.assertEqual(observer_calls[0][1:], ("td-b-formal", 1))
            self.assertNotIn("ambient_raw_file", analyze_calls[0][1])
            self.assertFalse(report["analysis_context"]["ambient_subtraction_applied"])

            default_adapter = (
                measure_raw_observer_validation.build_native_raw_capture_step_fn(
                    camera_dir=root / "default-camera",
                    measurements_dir=root / "default-measurements",
                    scratch_dir=root / "default-scratch",
                    location_config_path=root / "locations.json",
                    observer_config_path=root / "observer.json",
                    capture_fn=capture,
                    raw_analyze_fn=analyze,
                    raw_report_writer=write_report,
                    recorded_exposure_fn=exposure,
                    frozen_shutter_by_cache={"ray-h120-s100": "1/5000"},
                )
            )
            with self.assertRaisesRegex(ValueError, "preceding ambient"):
                default_adapter({**step, "capture_id": "default-formal"})

            for owner in (None, {"experiment_id": "other"}):
                with self.subTest(owner=owner), self.assertRaisesRegex(
                    PermissionError, "exact P7 v2 formal"
                ):
                    measure_raw_observer_validation.build_native_raw_capture_step_fn(
                        camera_dir=root / "invalid-camera",
                        measurements_dir=root / "invalid-measurements",
                        scratch_dir=root / "invalid-scratch",
                        location_config_path=root / "locations.json",
                        observer_config_path=root / "observer.json",
                        ambient_policy=(
                            measure_raw_observer_validation
                            .AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
                        ),
                        ambient_policy_owner=owner,
                    )
            td_c_adapter = measure_raw_observer_validation.build_native_raw_capture_step_fn(
                camera_dir=root / "td-c-camera",
                measurements_dir=root / "td-c-measurements",
                scratch_dir=root / "td-c-scratch",
                location_config_path=root / "locations.json",
                observer_config_path=root / "observer.json",
                capture_fn=capture,
                raw_analyze_fn=analyze,
                raw_report_writer=write_report,
                recorded_exposure_fn=exposure,
                frozen_shutter_by_cache={"ray-h120-s100": "1/5000"},
                ambient_policy=(
                    measure_raw_observer_validation
                    .AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
                ),
                ambient_policy_owner=(
                    measure_raw_observer_validation
                    .TD_C_FORMAL_AMBIENT_POLICY_OWNER
                ),
                physical_return_observer=lambda _returned, _step, _count: {
                    "physical_index": 1
                },
            )
            td_c_result = td_c_adapter({**step, "capture_id": "td-c-formal"})
            td_c_report = json.loads(
                Path(td_c_result["patch_statistics"]).read_text(encoding="utf-8")
            )
            self.assertFalse(
                td_c_report["analysis_context"]["ambient_subtraction_applied"]
            )
            with self.assertRaisesRegex(ValueError, "forbids ambient"):
                adapter({
                    **step,
                    "capture_id": "invalid-ambient",
                    "source": "ambient",
                    "source_exposure_cache": None,
                })
            with self.assertRaisesRegex(ValueError, "overrides native_raw_ambient_policy"):
                adapter({
                    **step,
                    "capture_id": "invalid-policy-context",
                    "analysis_context": {
                        "native_raw_ambient_policy": (
                            measure_raw_observer_validation
                            .AMBIENT_POLICY_REQUIRE_PRECEDING
                        ),
                    },
                })

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
