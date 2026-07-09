import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.optimization import measure_white_endpoints, measure_white_lut


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


class WhiteLutCalibrationTests(unittest.TestCase):
    def test_lut_default_target_grid_uses_four_cct_points_and_three_gm_points(self):
        args = measure_white_lut.parse_args(["--dry-run"])

        self.assertEqual(args.target_ccts, (1800, 3200, 5600, 20000))
        self.assertEqual(args.target_gm_values, (0, 100, 200))

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

    def test_lut_run_uses_endpoint_range_for_inside_and_outside_rgb_penalty(self):
        light_calls = []
        ray_calls = []

        def fake_light(cw, ww, r, g, b):
            command = {"cw": int(cw), "ww": int(ww), "r": int(r), "g": int(g), "b": int(b)}
            light_calls.append(command)
            return command

        def fake_ray_set_cct(cct, **kwargs):
            ray_calls.append((cct, kwargs))
            return {"code": 0, "data": {"cct": cct, **kwargs}}

        def fake_auto_expose(*, output_dir, filename_template, decode_output_dir, scratch_dir, **kwargs):
            output_path = Path(output_dir)
            decode_path = Path(decode_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            decode_path.mkdir(parents=True, exist_ok=True)
            stem = filename_template.replace(".%C", "")
            raw_file = output_path / f"{stem}.cr3"
            raw_file.write_bytes(b"ray")
            npy_file = decode_path / f"{stem}.npy"
            if "20000K" in stem:
                image = np.full((2, 4, 3), [600, 900, 1400], dtype=np.uint16)
            else:
                image = np.full((2, 4, 3), [1000, 700, 400], dtype=np.uint16)
            decoded = fake_decode_result(raw_file, npy_file, image)
            capture = camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=camera_gphoto2.CaptureSettings(shutter_speed="1/30"),
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
                light_fn=fake_light,
                ray_set_cct_fn=fake_ray_set_cct,
                auto_expose_fn=fake_auto_expose,
                capture_fn=fake_capture,
                decoder_fn=fake_decoder,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "complete")
        self.assertEqual(len(data["targets"]), 2)
        self.assertTrue(data["targets"][0]["range_classification"]["inside"])
        self.assertEqual(data["targets"][0]["solver"]["rgb_penalty"], 0.45)
        self.assertFalse(data["targets"][1]["range_classification"]["inside"])
        self.assertEqual(data["targets"][1]["solver"]["rgb_penalty"], 0.02)
        self.assertEqual(max(data["targets"][0]["solver"]["command"].values()), 4095)
        self.assertEqual(light_calls[-1], {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0})
        self.assertEqual(ray_calls[-1], (20000, {"intensity": 0, "gm": 100}))


if __name__ == "__main__":
    unittest.main()
