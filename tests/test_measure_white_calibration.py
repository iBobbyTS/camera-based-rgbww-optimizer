import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.optimization import measure_white_endpoints, measure_white_lut, white_lut_feedback


def project_temp_dir():
    measure_white_endpoints.PROJECT_TMP_DIR.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=measure_white_endpoints.PROJECT_TMP_DIR)


def write_location_config(path: Path) -> None:
    blocks = []
    for index in range(1, 3):
        x0 = (index - 1) * 2
        roles = ["neutral", "white"] if index == 1 else ["color"]
        blocks.append(
            {
                "index": index,
                "patch": {"name": f"patch_{index}", "roles": roles},
                "points": [
                    {"x": x0, "y": 0},
                    {"x": x0 + 1, "y": 0},
                    {"x": x0 + 1, "y": 1},
                    {"x": x0, "y": 1},
                ],
            }
        )
    path.write_text(json.dumps({"blocks": blocks}), encoding="utf-8")


def write_channel_response(path: Path) -> None:
    measurements = []
    vectors = {
        "cw": [1.0, 0.2, 0.1, 1.1, 0.25, 0.12],
        "ww": [1.0, 0.55, 0.3, 1.0, 0.58, 0.28],
        "r": [1.0, 0.1, 0.1, 1.0, 0.12, 0.1],
        "g": [0.1, 1.0, 0.1, 0.12, 1.0, 0.1],
        "b": [0.1, 0.1, 1.0, 0.11, 0.1, 1.0],
    }
    for channel, vector in vectors.items():
        regions = []
        for index in range(2):
            start = index * 3
            regions.append(
                {
                    "name": f"block_{index + 1:02d}",
                    "ambient_subtracted_channel_mean_per_second": vector[start : start + 3],
                }
            )
        measurements.append({"channel": channel, "code": 4095, "regions": regions, "source_file": "source.json"})
    path.write_text(json.dumps({"kind": "test_channel_response", "measurements": measurements}), encoding="utf-8")


def write_endpoint_calibration(path: Path, *, low=2700, high=6500) -> None:
    data = {
        "measurement": {"kind": "camera_based_rgbww_optimizer_white_endpoint_ray_match"},
        "created_at": "2026-06-07T00:00:00+00:00",
        "ray_endpoint_matches": {
            "ww": {"best": {"cct": low, "gm": 100, "relative_rmse": 0.01}, "ranked": []},
            "cw": {"best": {"cct": high, "gm": 100, "relative_rmse": 0.01}, "ranked": []},
        },
        "white_range": {
            "ww": {"cct": low, "gm": 100},
            "cw": {"cct": high, "gm": 100},
            "low_cct": low,
            "high_cct": high,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def fake_decode_result(raw_file: Path, npy_file: Path, image: np.ndarray) -> camera_gphoto2.DecodeResult:
    np.save(npy_file, image)
    return camera_gphoto2.DecodeResult(
        source_file=raw_file,
        output_files=(npy_file,),
        metadata_file=npy_file.with_suffix(".json"),
        image_shape=tuple(image.shape),
        image_dtype=str(image.dtype),
        stats={"image": {"max": int(image.max()), "channel_max": [int(image.max())] * 3}, "raw_visible": {"max": int(image.max())}},
    )


class WhiteEndpointMeasurementTests(unittest.TestCase):
    def test_endpoint_dry_run_writes_reusable_output_shape(self):
        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            write_location_config(location_path)

            output = measure_white_endpoints.run_white_endpoint_measurement(
                output_root=root,
                run_name="dry",
                location_config=location_path,
                endpoint_ray_ccts=(2700, 6500),
                endpoint_ray_gm_values=(0, 100, 200),
                neutral_roles=("neutral",),
                color_weight=0.2,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=False,
                dry_run=True,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "dry_run")
        self.assertEqual(data["measurement"]["kind"], "camera_based_rgbww_optimizer_white_endpoint_ray_match")
        self.assertEqual(len(data["endpoint_ray_plan"]), 6)
        self.assertEqual(data["camera"]["scratch_dir"], str(Path(tmpdir) / "dry" / "scratch"))

    def test_endpoint_run_matches_strip_channels_to_ray_grid_and_turns_off(self):
        light_calls = []
        ray_calls = []

        def fake_light(cw, ww, r, g, b):
            command = {"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)}
            light_calls.append(command)
            return command

        def fake_ray_set_cct(cct, **kwargs):
            ray_calls.append((cct, kwargs))
            return {"code": 0, "data": {"cct": cct, **kwargs}}

        def fake_white_point(capture, regions):
            if "strip-ww" in capture.saved_file.stem:
                return {"cct_K": 2700.0, "duv": 0.0, "xy": [0.45, 0.41], "uv1960": [0.26, 0.35]}
            if "strip-cw" in capture.saved_file.stem:
                return {"cct_K": 6500.0, "duv": 0.0, "xy": [0.31, 0.33], "uv1960": [0.20, 0.31]}
            return {"cct_K": 5000.0, "duv": 0.0, "xy": [0.34, 0.35], "uv1960": [0.22, 0.32]}

        class FakeAutoExpose:
            def __init__(self):
                self.index = 0
                self.scratch_dirs = []

            def __call__(self, *, output_dir, filename_template, decode_output_dir, scratch_dir, **kwargs):
                self.scratch_dirs.append(Path(scratch_dir))
                output_path = Path(output_dir)
                decode_path = Path(decode_output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                decode_path.mkdir(parents=True, exist_ok=True)
                stem = filename_template.replace(".%C", "")
                raw_file = output_path / f"{stem}.cr3"
                raw_file.write_bytes(b"raw")
                npy_file = decode_path / f"{stem}.npy"
                if "strip-ww" in stem or "2700K" in stem:
                    image = np.full((2, 4, 3), [1000, 600, 300], dtype=np.uint16)
                elif "strip-cw" in stem or "6500K" in stem:
                    image = np.full((2, 4, 3), [700, 900, 1100], dtype=np.uint16)
                else:
                    image = np.full((2, 4, 3), [500, 500, 500], dtype=np.uint16)
                decoded = fake_decode_result(raw_file, npy_file, image)
                capture = camera_gphoto2.CaptureResult(
                    connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                    settings=camera_gphoto2.CaptureSettings(shutter_speed="1/30"),
                    saved_file=raw_file,
                    stdout="",
                    decoded=decoded,
                )
                return camera_gphoto2.AutoExposureResult(target_max=49152, final_capture=capture, trials=())

        fake_auto = FakeAutoExpose()
        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            write_location_config(location_path)
            output = measure_white_endpoints.run_white_endpoint_measurement(
                output_root=root,
                run_name="run",
                location_config=location_path,
                endpoint_ray_ccts=(2700, 6500),
                endpoint_ray_gm_values=(100,),
                neutral_roles=("neutral",),
                color_weight=0.2,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=True,
                dry_run=False,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
                ray_search_mode="grid",
                light_fn=fake_light,
                ray_set_cct_fn=fake_ray_set_cct,
                auto_expose_fn=fake_auto,
                white_point_estimator_fn=fake_white_point,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "complete")
        self.assertEqual(data["ray_endpoint_matches"]["ww"]["best"]["cct"], 2700)
        self.assertEqual(data["ray_endpoint_matches"]["cw"]["best"]["cct"], 6500)
        self.assertEqual(data["white_range"]["low_cct"], 2700)
        self.assertEqual(data["white_range"]["high_cct"], 6500)
        self.assertEqual(light_calls[0], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1], (6500, {"intensity": 0, "gm": 100}))
        self.assertTrue(all(path == Path(tmpdir) / "run" / "scratch" for path in fake_auto.scratch_dirs))

    def test_endpoint_adaptive_search_uses_white_point_estimates_and_turns_off(self):
        light_calls = []
        ray_calls = []

        def fake_light(cw, ww, r, g, b):
            command = {"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)}
            light_calls.append(command)
            return command

        def fake_ray_set_cct(cct, **kwargs):
            ray_calls.append((int(cct), kwargs))
            return {"code": 0, "data": {"cct": int(cct), **kwargs}}

        def fake_auto_expose(*, output_dir, filename_template, decode_output_dir, scratch_dir, **kwargs):
            output_path = Path(output_dir)
            decode_path = Path(decode_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            decode_path.mkdir(parents=True, exist_ok=True)
            stem = filename_template.replace(".%C", "")
            raw_file = output_path / f"{stem}.cr3"
            raw_file.write_bytes(stem.encode("ascii"))
            npy_file = decode_path / f"{stem}.npy"
            decoded = fake_decode_result(raw_file, npy_file, np.full((2, 4, 3), 1000, dtype=np.uint16))
            capture = camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=camera_gphoto2.CaptureSettings(shutter_speed="1/30"),
                saved_file=raw_file,
                stdout="",
                decoded=decoded,
            )
            return camera_gphoto2.AutoExposureResult(target_max=49152, final_capture=capture, trials=())

        def fake_white_point(capture, regions):
            name = capture.saved_file.stem
            if "endpoint-strip-ww" in name:
                return {"cct_K": 3000.0, "duv": -0.002, "xy": [0.43, 0.40], "uv1960": [0.25, 0.35]}
            if "endpoint-strip-cw" in name:
                return {"cct_K": 6500.0, "duv": 0.003, "xy": [0.31, 0.33], "uv1960": [0.20, 0.31]}
            cct_text = name.rsplit("K-gm", 1)[0].rsplit("-", 1)[-1]
            gm_text = name.rsplit("gm", 1)[-1]
            return {
                "cct_K": float(int(cct_text)),
                "duv": (float(int(gm_text)) - 100.0) / 10000.0,
                "xy": [0.33, 0.34],
                "uv1960": [0.21, 0.32],
            }

        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            write_location_config(location_path)
            output = measure_white_endpoints.run_white_endpoint_measurement(
                output_root=root,
                run_name="adaptive",
                location_config=location_path,
                endpoint_ray_ccts=(2700, 6500),
                endpoint_ray_gm_values=(100,),
                neutral_roles=("neutral",),
                color_weight=0.2,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=True,
                dry_run=False,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
                ray_search_mode="adaptive",
                ray_cct_min=2000,
                ray_cct_max=7000,
                ray_gm_min=70,
                ray_gm_max=130,
                ray_search_cct_iterations=3,
                ray_search_gm_iterations=2,
                light_fn=fake_light,
                ray_set_cct_fn=fake_ray_set_cct,
                auto_expose_fn=fake_auto_expose,
                white_point_estimator_fn=fake_white_point,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "complete")
        self.assertEqual(data["measurement"]["ray_search_mode"], "adaptive")
        self.assertIn("ww", data["ray_searches"])
        self.assertIn("cw", data["ray_searches"])
        self.assertEqual(data["strip_endpoints"]["ww"]["white_point"]["cct_K"], 3000.0)
        self.assertEqual(data["strip_endpoints"]["cw"]["white_point"]["duv"], 0.003)
        self.assertLess(abs(data["ray_endpoint_matches"]["ww"]["best"]["cct"] - 3000), 1000)
        self.assertLess(abs(data["ray_endpoint_matches"]["cw"]["best"]["cct"] - 6500), 1000)
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1][1]["intensity"], 0)

    def test_endpoint_adaptive_search_starts_at_target_cct_and_corrects_observed_error(self):
        ray_calls = []

        def fake_light(cw, ww, r, g, b):
            return {"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)}

        def fake_ray_set_cct(cct, **kwargs):
            ray_calls.append((int(cct), kwargs))
            return {"code": 0, "data": {"cct": int(cct), **kwargs}}

        def fake_auto_expose(*, output_dir, filename_template, decode_output_dir, scratch_dir, **kwargs):
            output_path = Path(output_dir)
            decode_path = Path(decode_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            decode_path.mkdir(parents=True, exist_ok=True)
            stem = filename_template.replace(".%C", "")
            raw_file = output_path / f"{stem}.cr3"
            raw_file.write_bytes(stem.encode("ascii"))
            npy_file = decode_path / f"{stem}.npy"
            decoded = fake_decode_result(raw_file, npy_file, np.full((2, 4, 3), 1000, dtype=np.uint16))
            capture = camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=camera_gphoto2.CaptureSettings(shutter_speed="1/30"),
                saved_file=raw_file,
                stdout="",
                decoded=decoded,
            )
            return camera_gphoto2.AutoExposureResult(target_max=49152, final_capture=capture, trials=())

        def fake_white_point(capture, regions):
            name = capture.saved_file.stem
            if "endpoint-strip-ww" in name:
                return {"cct_K": 3000.0, "duv": -0.02, "xy": [0.43, 0.40], "uv1960": [0.25, 0.35]}
            if "endpoint-strip-cw" in name:
                return {"cct_K": 6500.0, "duv": -0.02, "xy": [0.31, 0.33], "uv1960": [0.20, 0.31]}
            cct_text = name.rsplit("K-gm", 1)[0].rsplit("-", 1)[-1]
            gm_text = name.rsplit("gm", 1)[-1]
            cct = int(cct_text)
            gm = int(gm_text)
            return {
                "cct_K": float(cct + 100 + (gm - 100) * 0.5),
                "duv": float(100 - gm) / 5000.0,
                "xy": [0.33, 0.34],
                "uv1960": [0.21, 0.32],
            }

        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            write_location_config(location_path)
            output = measure_white_endpoints.run_white_endpoint_measurement(
                output_root=root,
                run_name="adaptive-correction",
                location_config=location_path,
                endpoint_ray_ccts=(2700, 6500),
                endpoint_ray_gm_values=(100,),
                neutral_roles=("neutral",),
                color_weight=0.2,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=True,
                dry_run=False,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
                ray_search_mode="adaptive",
                ray_cct_min=2000,
                ray_cct_max=7000,
                ray_gm_min=70,
                ray_gm_max=130,
                ray_search_cct_iterations=6,
                ray_search_gm_iterations=3,
                light_fn=fake_light,
                ray_set_cct_fn=fake_ray_set_cct,
                auto_expose_fn=fake_auto_expose,
                white_point_estimator_fn=fake_white_point,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        ww_samples = data["ray_searches"]["ww"]["samples"]
        cw_samples = data["ray_searches"]["cw"]["samples"]
        self.assertEqual(ww_samples[0]["cct"], 3000)
        self.assertEqual(ww_samples[1]["cct"], 2900)
        self.assertEqual(cw_samples[0]["cct"], 6500)
        self.assertEqual(cw_samples[1]["cct"], 6400)
        self.assertTrue(any(sample["cct"] == 2885 and sample["gm"] == 130 for sample in ww_samples))
        self.assertTrue(any(sample["cct"] == 6385 and sample["gm"] == 130 for sample in cw_samples))
        self.assertEqual(data["ray_endpoint_matches"]["ww"]["best"]["absolute_cct_error_K"], 0.0)
        self.assertEqual(data["ray_endpoint_matches"]["cw"]["best"]["absolute_cct_error_K"], 0.0)


class WhiteEndpointDefaultTests(unittest.TestCase):
    def test_adaptive_search_default_iterations_are_long_scan(self):
        args = measure_white_endpoints.parse_args(["--dry-run"])

        self.assertEqual(args.ray_search_cct_iterations, 64)
        self.assertEqual(args.ray_search_gm_iterations, 16)

    def test_ray_start_argument_accepts_endpoint_cct_and_gm_seeds(self):
        args = measure_white_endpoints.parse_args([
            "--dry-run",
            "--ray-start",
            "ww=2961,160",
            "--ray-start",
            "cw=7895:100",
        ])

        self.assertEqual(dict(args.ray_start), {"ww": {"cct": 2961, "gm": 160}, "cw": {"cct": 7895, "gm": 100}})


class WhiteLutCalibrationTests(unittest.TestCase):
    def test_initial_lut_seed_replaces_model_command_and_preserves_full_scale_channel(self):
        solution = {
            "command": {"cw": 4095, "ww": 1000, "r": 0, "g": 0, "b": 0},
            "active_channel": "cw",
            "score": 1.0,
        }
        seeded = measure_white_lut.seed_solution_from_lut(
            solution,
            {
                "targets": [
                    {
                        "cct": 3200,
                        "gm": 100,
                        "selected_command": {"cw": 1000, "ww": 4095, "r": 10, "g": 20, "b": 30},
                    }
                ]
            },
            cct=3200,
            gm=100,
            max_code=4095,
        )

        self.assertEqual(seeded["command"], {"cw": 1000, "ww": 4095, "r": 10, "g": 20, "b": 30})
        self.assertEqual(seeded["active_channel"], "ww")
        self.assertEqual(seeded["model_command"], solution["command"])
        self.assertIsNone(seeded["initial_lut_seed"]["prior_white_point_comparison"])

    def test_feedback_restarts_try_endpoint_bias_with_original_active_channel_free(self):
        solution = {
            "command": {"cw": 256, "ww": 3711, "r": 4095, "g": 0, "b": 0},
            "active_channel": "r",
            "model_active_channel": "r",
            "endpoint_bias": "ww",
        }

        attempts = measure_white_lut.feedback_restart_solutions(solution, max_code=4095)

        self.assertEqual([attempt["active_channel"] for attempt in attempts], ["r", "ww"])
        self.assertEqual(attempts[1]["command"]["ww"], 4095)
        self.assertEqual(attempts[1]["command"]["r"], 4095)

    def test_feedback_restarts_keep_alternative_command_with_same_active_channel(self):
        solution = {
            "command": {"cw": 0, "ww": 0, "r": 4095, "g": 1100, "b": 0},
            "active_channel": "r",
            "alternative_initial_solutions": [
                {
                    "command": {"cw": 256, "ww": 3711, "r": 4095, "g": 0, "b": 0},
                    "active_channel": "r",
                    "source": "initial_lut",
                }
            ],
        }

        attempts = measure_white_lut.feedback_restart_solutions(solution, max_code=4095)

        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0]["feedback_restart"]["source"], "primary")
        self.assertEqual(attempts[1]["feedback_restart"]["source"], "initial_lut")
        self.assertNotEqual(attempts[0]["command"], attempts[1]["command"])

    def test_feedback_attempt_sort_prefers_confirmed_result(self):
        def attempt(*, confirmed, score):
            return {
                "goal_confirmed": confirmed,
                "best": {
                    "white_point_comparison": {
                        "goal_score": score,
                        "absolute_cct_error_K": score,
                    },
                    "comparison_to_ray_weighted": {"relative_rmse": score},
                },
            }

        unconfirmed = attempt(confirmed=False, score=0.01)
        confirmed = attempt(confirmed=True, score=0.9)

        self.assertIs(
            min([unconfirmed, confirmed], key=measure_white_lut.feedback_attempt_sort_key),
            confirmed,
        )

    def test_white_point_mix_finds_full_scale_linear_camera_rgb_solution(self):
        regions = [
            {"name": "block_01", "patch": {"name": "white", "roles": ["neutral", "white"]}},
        ]
        basis = {
            "cw": np.asarray([0.3, 0.6, 1.0]),
            "ww": np.asarray([1.0, 0.7, 0.2]),
            "r": np.asarray([1.0, 0.0, 0.0]),
            "g": np.asarray([0.0, 1.0, 0.0]),
            "b": np.asarray([0.0, 0.0, 1.0]),
        }
        target = {
            "camera_neutral_g1": [1.0, 1.0, 0.0],
            "rawpy_rgb_xyz_matrix_first3": np.eye(3).tolist(),
        }

        result = measure_white_lut.solve_white_point_mix(
            basis,
            target,
            regions=regions,
            max_code=4095,
        )

        self.assertEqual(max(result["best"]["command"].values()), 4095)
        self.assertLess(result["best"]["camera_rgb_direction_residual"], 1e-10)

    def test_lut_default_target_grid_uses_four_cct_points_and_three_gm_points(self):
        args = measure_white_lut.parse_args(["--dry-run"])

        self.assertEqual(args.target_ccts, (1800, 3200, 5600, 20000))
        self.assertEqual(args.target_gm_values, (0, 100, 200))
        self.assertEqual(args.feedback_rounds, 16)
        self.assertEqual(args.feedback_confirmations, 2)
        self.assertEqual(args.feedback_confirmation_settle_seconds, 60.0)
        self.assertEqual(args.feedback_confirmation_off_seconds, 1.0)
        self.assertEqual(args.feedback_thermal_rebases, 2)
        self.assertEqual(args.feedback_cct_tolerance_K, 25.0)
        self.assertEqual(args.feedback_cct_tolerance_mired, 1.0)
        self.assertEqual(args.feedback_duv_tolerance, 0.0005)
        self.assertEqual(measure_white_lut.DEFAULT_INITIAL_LUT_LOCAL_SCORE_LIMIT, 4.0)

    def test_lut_dry_run_requires_and_records_endpoint_calibration(self):
        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            response_path = root / "response.json"
            endpoint_path = root / "white-endpoints.json"
            write_location_config(location_path)
            write_channel_response(response_path)
            write_endpoint_calibration(endpoint_path)

            output = measure_white_lut.run_white_lut_calibration(
                output_root=root,
                run_name="dry",
                endpoint_calibration=endpoint_path,
                location_config=location_path,
                channel_response=response_path,
                target_ccts=(3200,),
                target_gm_values=(0, 100, 200),
                neutral_roles=("neutral",),
                color_weight=0.2,
                inside_rgb_penalty=0.45,
                outside_rgb_penalty=0.06,
                endpoint_rgb_penalty=0.02,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=False,
                dry_run=True,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "dry_run")
        self.assertEqual(data["measurement"]["endpoint_calibration"], str(endpoint_path))
        self.assertEqual(data["white_range"]["low_cct"], 2700)
        self.assertEqual(len(data["target_plan"]), 3)
        self.assertEqual(data["target_plan"][0]["rgb_policy"]["gm_compensation"]["direction"], "magenta")
        self.assertEqual(
            data["target_plan"][0]["rgb_policy"]["channel_penalties"],
            {"r": 0.02, "g": 0.45, "b": 0.02},
        )

    def test_lut_run_uses_endpoint_range_for_inside_and_outside_rgb_penalty(self):
        light_calls = []
        ray_calls = []
        events = []
        exposure_calls = []
        capture_states = []
        strip_state = {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}
        ray_is_on = False

        def fake_light(cw, ww, r, g, b):
            command = {"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)}
            strip_state.update(command)
            light_calls.append(command)
            events.append(("light", command))
            return command

        def fake_ray_set_cct(cct, **kwargs):
            nonlocal ray_is_on
            intensity = kwargs.get("intensity_percent", kwargs.get("intensity", 0))
            ray_is_on = float(intensity) > 0
            ray_calls.append((cct, kwargs))
            events.append(("ray", int(cct), kwargs))
            return {"code": 0, "data": {"cct": cct, **kwargs}}

        def fake_auto_expose(*, output_dir, filename_template, decode_output_dir, scratch_dir, **kwargs):
            output_path = Path(output_dir)
            decode_path = Path(decode_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            decode_path.mkdir(parents=True, exist_ok=True)
            stem = filename_template.replace(".%C", "")
            source = "ray" if stem.startswith("target-ray") else "strip"
            source_index = sum(1 for call in exposure_calls if call["source"] == source)
            final_shutter = (
                ("1/1000", "1/1250")[source_index]
                if source == "ray"
                else ("1/125", "1/160")[source_index]
            )
            exposure_calls.append({
                "source": source,
                "initial_shutter_speed": kwargs.get("initial_shutter_speed"),
                "final_shutter_speed": final_shutter,
            })
            capture_states.append({
                "source": source,
                "ray_on": ray_is_on,
                "strip_on": any(strip_state.values()),
            })
            raw_file = output_path / f"{stem}.cr3"
            raw_file.write_bytes(source.encode("ascii"))
            npy_file = decode_path / f"{stem}.npy"
            if "20000K" in stem:
                image = np.full((2, 4, 3), [600, 900, 1400], dtype=np.uint16)
            else:
                image = np.full((2, 4, 3), [1000, 700, 400], dtype=np.uint16)
            decoded = fake_decode_result(raw_file, npy_file, image)
            capture = camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=camera_gphoto2.CaptureSettings(shutter_speed=final_shutter),
                saved_file=raw_file,
                stdout="",
                decoded=decoded,
            )
            return camera_gphoto2.AutoExposureResult(target_max=49152, final_capture=capture, trials=())

        def fake_capture(*, output_dir, filename_template, settings, **kwargs):
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            raw_file = output_path / filename_template.replace(".%C", ".cr3")
            raw_file.write_bytes(b"rgbww")
            return camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=settings,
                saved_file=raw_file,
                stdout="",
            )

        def fake_decoder(raw_file, *, output_dir, formats, **kwargs):
            decode_path = Path(output_dir)
            decode_path.mkdir(parents=True, exist_ok=True)
            npy_file = decode_path / f"{Path(raw_file).stem}.npy"
            return fake_decode_result(Path(raw_file), npy_file, np.full((2, 4, 3), 900, dtype=np.uint16))

        def fake_white_point(capture, regions):
            cct = 20000.0 if "20000K" in capture.saved_file.stem else 3200.0
            return {"cct_K": cct, "duv": 0.0, "xy": [0.33, 0.33], "uv1960": [0.21, 0.31]}

        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            response_path = root / "response.json"
            endpoint_path = root / "white-endpoints.json"
            write_location_config(location_path)
            write_channel_response(response_path)
            write_endpoint_calibration(endpoint_path, low=2700, high=6500)

            output = measure_white_lut.run_white_lut_calibration(
                output_root=root,
                run_name="run",
                endpoint_calibration=endpoint_path,
                location_config=location_path,
                channel_response=response_path,
                target_ccts=(3200, 20000),
                target_gm_values=(100,),
                neutral_roles=("neutral",),
                color_weight=0.2,
                inside_rgb_penalty=0.45,
                outside_rgb_penalty=0.06,
                endpoint_rgb_penalty=0.02,
                max_code=4095,
                safe_code_limit=1024,
                allow_high_output=True,
                dry_run=False,
                settle_seconds=0.0,
                ray_intensity_percent=100,
                target_max=49152,
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                block_indices="all",
                auto_exposure_metering_mode=camera_gphoto2.METERING_MODE_FULL,
                auto_exposure_metering_location_config=None,
                feedback_confirmation_settle_seconds=0.0,
                feedback_confirmation_off_seconds=0.0,
                light_fn=fake_light,
                ray_set_cct_fn=fake_ray_set_cct,
                auto_expose_fn=fake_auto_expose,
                capture_fn=fake_capture,
                decoder_fn=fake_decoder,
                white_point_estimator_fn=fake_white_point,
            )
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(list((root / "run" / "decoded").glob("*.npy")), [])

        self.assertEqual(data["status"], "complete")
        self.assertEqual(len(data["targets"]), 2)
        self.assertTrue(data["targets"][0]["range_classification"]["inside"])
        self.assertEqual(data["targets"][0]["solver"]["rgb_penalty"], 0.45)
        self.assertFalse(data["targets"][1]["range_classification"]["inside"])
        self.assertEqual(data["targets"][1]["solver"]["rgb_penalty"], 0.02)
        self.assertEqual(max(data["targets"][0]["solver"]["command"].values()), 4095)
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1], (20000, {"intensity": 0, "gm": 100}))
        ray_on_indices = [
            index
            for index, event in enumerate(events)
            if event[0] == "ray" and "intensity_percent" in event[2]
        ]
        self.assertEqual(len(ray_on_indices), 2)
        for index in ray_on_indices:
            self.assertEqual(events[index - 1], ("light", {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}))
        self.assertEqual(
            exposure_calls,
            [
                {"source": "ray", "initial_shutter_speed": "1/30", "final_shutter_speed": "1/1000"},
                {"source": "strip", "initial_shutter_speed": "1/30", "final_shutter_speed": "1/125"},
                {"source": "ray", "initial_shutter_speed": "1/1000", "final_shutter_speed": "1/1250"},
                {"source": "strip", "initial_shutter_speed": "1/125", "final_shutter_speed": "1/160"},
            ],
        )
        self.assertEqual(
            capture_states,
            [
                {"source": "ray", "ray_on": True, "strip_on": False},
                {"source": "strip", "ray_on": False, "strip_on": True},
                {"source": "ray", "ray_on": True, "strip_on": False},
                {"source": "strip", "ray_on": False, "strip_on": True},
            ],
        )
        self.assertEqual(data["camera"]["exposure_cache"]["ray_final_shutter_speed"], "1/1250")
        self.assertEqual(data["camera"]["exposure_cache"]["strip_final_shutter_speed"], "1/160")
        self.assertEqual(data["measurement"]["decoded_npy_retention"], "delete_after_measurement")
        self.assertTrue(all(target["ray"]["removed_npy_files"] for target in data["targets"]))
        self.assertTrue(
            all(
                sample["removed_npy_files"]
                for target in data["targets"]
                for sample in target["feedback_optimizer"]["samples"]
            )
        )

    def test_feedback_optimizer_converges_with_synthetic_camera_observations(self):
        current_command = {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}
        desired_command = {"cw": 4095, "ww": 1500, "r": 400, "g": 1200, "b": 300}
        light_calls = []
        auto_exposure_calls = []

        def fake_light(cw, ww, r, g, b):
            current_command.update({"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)})
            light_calls.append(dict(current_command))
            return dict(current_command)

        def fake_capture(*, output_dir, filename_template, settings, **kwargs):
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            raw_file = output_path / filename_template.replace(".%C", ".cr3")
            raw_file.write_bytes(b"rgbww")
            return camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=settings,
                saved_file=raw_file,
                stdout="",
            )

        def fake_decoder(raw_file, *, output_dir, formats, **kwargs):
            decode_path = Path(output_dir)
            decode_path.mkdir(parents=True, exist_ok=True)
            npy_file = decode_path / f"{Path(raw_file).stem}.npy"
            return fake_decode_result(Path(raw_file), npy_file, np.full((2, 4, 3), 900, dtype=np.uint16))

        def fake_auto_expose(*, output_dir, filename_template, decode_output_dir, initial_shutter_speed, **kwargs):
            auto_exposure_calls.append(initial_shutter_speed)
            capture = fake_capture(
                output_dir=output_dir,
                filename_template=filename_template,
                settings=camera_gphoto2.CaptureSettings(shutter_speed=initial_shutter_speed),
            )
            decoded = fake_decoder(
                capture.saved_file,
                output_dir=decode_output_dir,
                formats=("npy",),
            )
            final_capture = camera_gphoto2.CaptureResult(
                connection=capture.connection,
                settings=capture.settings,
                saved_file=capture.saved_file,
                stdout=capture.stdout,
                decoded=decoded,
            )
            return camera_gphoto2.AutoExposureResult(
                target_max=49152,
                final_capture=final_capture,
                trials=(),
            )

        def fake_white_point(capture, regions):
            ww_error = current_command["ww"] - desired_command["ww"]
            g_error = current_command["g"] - desired_command["g"]
            return {
                "cct_K": 5000.0 + ww_error * 0.2 + g_error * 0.01,
                "duv": ww_error * 0.000001 + g_error * 0.00002,
                "xy": [0.33, 0.33],
                "uv1960": [0.21, 0.31],
            }

        with project_temp_dir() as tmpdir:
            root = Path(tmpdir)
            location_path = root / "locations.json"
            write_location_config(location_path)
            regions = measure_white_lut.common.load_weighted_location_regions(
                location_path,
                "all",
                neutral_roles=("neutral",),
                color_weight=0.2,
            )
            result = white_lut_feedback.run_feedback_optimization(
                target={"index": 0, "cct": 5000, "gm": 50},
                target_vector=np.full(6, 1000.0),
                target_white_point={"cct_K": 5000.0, "duv": 0.0},
                initial_solution={
                    "active_channel": "cw",
                    "command": {"cw": 4095, "ww": 500, "r": 400, "g": 400, "b": 300},
                },
                rgb_penalty=0.45,
                regions=regions,
                camera_dir=root / "camera",
                decode_dir=root / "decoded",
                scratch_dir=root / "scratch",
                initial_shutter_speed="1/30",
                iso="100",
                aperture="4",
                image_format="RAW",
                min_shutter_speed="1/8000",
                max_shutter_speed="30",
                max_trials=5,
                max_captures=10,
                decode_formats=("npy",),
                metering_regions=None,
                settle_seconds=0.0,
                target_max=49152,
                low_signal_ratio=0.1,
                high_signal_ratio=1.0,
                max_code=4095,
                feedback_rounds=3,
                feedback_probe_step=256,
                feedback_max_step=768,
                feedback_damping=0.05,
                feedback_confirmation_settle_seconds=0.0,
                feedback_confirmation_off_seconds=0.0,
                feedback_cct_tolerance_K=10.0,
                feedback_duv_tolerance=0.01,
                light_fn=fake_light,
                auto_expose_fn=fake_auto_expose,
                capture_fn=fake_capture,
                decoder_fn=fake_decoder,
                white_point_estimator_fn=fake_white_point,
            )
            self.assertEqual(list((root / "decoded").glob("*.npy")), [])

        self.assertEqual(result["status"], "goal_confirmed")
        self.assertTrue(result["goal_confirmed"])
        self.assertTrue(result["confirmation_attempts"])
        self.assertEqual(result["confirmation_attempts"][-1]["status"], "confirmed")
        self.assertTrue(result["best"]["white_point_comparison"]["within_goal"])
        self.assertLess(result["best"]["white_point_comparison"]["goal_score"], 1.0)
        self.assertEqual(max(result["selected_command"].values()), 4095)
        self.assertGreaterEqual(result["rounds_completed"], 1)
        self.assertEqual(result["initial_shutter_speed"], "1/30")
        self.assertEqual(result["final_shutter_speed"], "1/30")
        self.assertEqual(auto_exposure_calls, ["1/30"])
        self.assertTrue(any(sample["phase"].startswith("probe-") for sample in result["samples"]))
        self.assertTrue(any(sample["phase"].startswith("feedback-") for sample in result["samples"]))
        self.assertEqual(
            len([sample for sample in result["samples"] if sample["phase"].startswith("confirm-")]),
            2,
        )
        self.assertEqual(result["attempt"], 0)
        self.assertTrue(all(max(call.values()) == 4095 or max(call.values()) == 0 for call in light_calls))


if __name__ == "__main__":
    unittest.main()
