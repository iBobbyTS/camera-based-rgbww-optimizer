import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.interaction import location_checker


def make_location_config(count=24, *, include_patch=False):
    blocks = []
    for index in range(1, count + 1):
        x = float((index - 1) % 6) * 2.0
        y = float((index - 1) // 6) * 2.0
        block = {
            "index": index,
            "points": [
                {"x": x, "y": y},
                {"x": x + 1.0, "y": y},
                {"x": x + 1.0, "y": y + 1.0},
                {"x": x, "y": y + 1.0},
            ],
        }
        if include_patch:
            block["patch"] = {"name": "red", "label": "R", "standard_index": 15}
        blocks.append(block)
    return {"blocks": blocks}


class LocationCheckerArgsTests(unittest.TestCase):
    def test_parse_args_requires_location_json(self):
        with self.assertRaises(SystemExit):
            location_checker.parse_args([])

        args = location_checker.parse_args(["config/location/example.json", "--max-exposure-trials", "3"])

        self.assertEqual(args.location_config, Path("config/location/example.json"))
        self.assertEqual(args.max_exposure_trials, 3)


class LocationCheckerRenderTests(unittest.TestCase):
    def test_load_required_location_regions_requires_24_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "locations.json"
            path.write_text(json.dumps(make_location_config(23)), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "exactly 24"):
                location_checker.load_required_location_regions(path)

    def test_load_required_location_regions_preserves_patch_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "locations.json"
            path.write_text(json.dumps(make_location_config(include_patch=True)), encoding="utf-8")

            regions = location_checker.load_required_location_regions(path)

        self.assertEqual(regions[0]["patch"]["name"], "red")

    def test_validate_regions_inside_image_reports_bad_region(self):
        image = np.zeros((5, 5, 3), dtype=np.uint16)
        region = {
            "type": "roi",
            "name": "bad",
            "x": 4,
            "y": 4,
            "width": 10,
            "height": 1,
        }

        with self.assertRaisesRegex(RuntimeError, "bad"):
            location_checker.validate_regions_inside_image(image, [region])

    def test_render_location_overlay_writes_png_and_changes_pixels(self):
        image = np.full((30, 30, 3), 64, dtype=np.uint8)
        regions = [
            {
                "type": "polygon",
                "name": "block_01",
                "index": 1,
                "points": [(5.0, 5.0), (20.0, 5.0), (20.0, 20.0), (5.0, 20.0)],
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "overlay.png"
            location_checker.render_location_overlay(image, regions, output)
            data = output.read_bytes()

        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertNotEqual(image.tobytes(), data)

    def test_render_location_overlay_labels_patch_color_not_index(self):
        class FakeCv2:
            LINE_AA = object()
            FONT_HERSHEY_SIMPLEX = object()

            def __init__(self):
                self.labels = []

            def fillPoly(self, *_args, **_kwargs):
                raise AssertionError("location checker overlay should not fill polygons")

            def addWeighted(self, _fill_layer, _fill_alpha, output, _output_alpha, _gamma):
                raise AssertionError("location checker overlay should not blend polygon fills")

            def polylines(self, *_args, **_kwargs):
                return None

            def getTextSize(self, label, *_args, **_kwargs):
                return (len(label) * 8, 12), 2

            def putText(self, _image, label, *_args, **_kwargs):
                self.labels.append(label)
                return None

        image = np.full((30, 30, 3), 64, dtype=np.uint8)
        regions = [
            {
                "type": "polygon",
                "name": "block_15",
                "index": 15,
                "patch": {"name": "red"},
                "points": [(5.0, 5.0), (20.0, 5.0), (20.0, 20.0), (5.0, 20.0)],
            },
            {
                "type": "polygon",
                "name": "block_16",
                "index": 16,
                "points": [(22.0, 5.0), (28.0, 5.0), (28.0, 20.0), (22.0, 20.0)],
            },
        ]
        fake_cv2 = FakeCv2()

        with tempfile.TemporaryDirectory() as tmpdir, mock.patch.object(
            location_checker,
            "_import_cv2",
            return_value=fake_cv2,
        ), mock.patch.object(location_checker.location_picker_ui, "rgb_to_png_data", return_value=b"png"):
            location_checker.render_location_overlay(image, regions, Path(tmpdir) / "overlay.png")

        self.assertEqual(fake_cv2.labels, ["Red", "Red"])
        self.assertNotIn("15", fake_cv2.labels)
        self.assertNotIn("16", fake_cv2.labels)

    def test_decode_dcraw_preview_uses_auto_white_balance_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            raw_file = Path(tmpdir) / "input.cr3"
            raw_file.write_bytes(b"raw")

            def fake_run(command, **_kwargs):
                output_file = Path(command[command.index("-Z") + 1])
                output_file.write_bytes(b"tiff")
                return mock.Mock(returncode=0, stdout="", stderr="")

            with mock.patch.object(location_checker.subprocess, "run", side_effect=fake_run) as run, mock.patch.object(
                location_checker,
                "_import_tifffile",
                return_value=mock.Mock(imread=lambda _path: np.full((2, 3, 3), 200, dtype=np.uint8)),
            ):
                result = location_checker._decode_dcraw_preview(raw_file, output_dir=Path(tmpdir) / "decoded")

        command = run.call_args.args[0]
        self.assertEqual(command[:2], ["dcraw_emu", "-T"])
        self.assertIn("-a", command)
        self.assertEqual(command[command.index("-o") + 1], "1")
        self.assertEqual(command[command.index("-q") + 1], "3")
        self.assertEqual(result.output_files[0].suffix, ".tiff")
        self.assertEqual(result.stats["postprocess_params"]["decoder"], "dcraw_emu")
        self.assertEqual(result.stats["postprocess_params"]["white_balance"], "auto")

    def test_decode_dcraw_preview_can_use_camera_white_balance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            raw_file = Path(tmpdir) / "input.cr3"
            raw_file.write_bytes(b"raw")

            def fake_run(command, **_kwargs):
                Path(command[command.index("-Z") + 1]).write_bytes(b"tiff")
                return mock.Mock(returncode=0, stdout="", stderr="")

            with mock.patch.object(location_checker.subprocess, "run", side_effect=fake_run) as run, mock.patch.object(
                location_checker,
                "_import_tifffile",
                return_value=mock.Mock(imread=lambda _path: np.full((2, 3, 3), 200, dtype=np.uint8)),
            ):
                result = location_checker._decode_dcraw_preview(
                    raw_file,
                    output_dir=Path(tmpdir) / "decoded",
                    executable="dcraw_emu",
                    white_balance="camera",
                )

        command = run.call_args.args[0]
        self.assertIn("-w", command)
        self.assertNotIn("-a", command)
        self.assertEqual(result.stats["postprocess_params"]["white_balance"], "camera")

    def test_visual_decode_to_preview_uint8_preserves_uint8(self):
        image = np.array([[[1, 2, 3]]], dtype=np.uint8)

        preview = location_checker._visual_decode_to_preview_uint8(image)

        self.assertIs(preview, image)

    def test_visual_decode_to_preview_uint8_scales_uint16(self):
        image = np.array([[[0, 257, 65535]]], dtype=np.uint16)

        preview = location_checker._visual_decode_to_preview_uint8(image)

        self.assertEqual(preview.tolist(), [[[0, 1, 255]]])

    def test_capture_location_check_uses_full_frame_auto_exposure_and_renders_overlay(self):
        auto_exposure_calls = []

        with tempfile.TemporaryDirectory() as tmpdir:
            location_path = Path(tmpdir) / "locations.json"
            location_path.write_text(json.dumps(make_location_config()), encoding="utf-8")

            def fake_auto_expose_capture(**kwargs):
                auto_exposure_calls.append(kwargs)
                self.assertIsNone(kwargs["metering_regions"])
                self.assertEqual(kwargs["decode_formats"], ("npy",))
                self.assertNotIn("decoder", kwargs)
                raw_file = Path(kwargs["output_dir"]) / "check.cr3"
                raw_file.parent.mkdir(parents=True, exist_ok=True)
                raw_file.write_bytes(b"raw")
                output_dir = Path(kwargs["decode_output_dir"])
                output_dir.mkdir(parents=True, exist_ok=True)
                npy = output_dir / "decoded.npy"
                metadata = output_dir / "decoded.json"
                np.save(npy, np.full((12, 14, 3), 1000, dtype=np.uint16))
                metadata.write_text("{}", encoding="utf-8")
                decoded = camera_gphoto2.DecodeResult(
                    source_file=Path(raw_file),
                    output_files=(npy, metadata),
                    metadata_file=metadata,
                    image_shape=(12, 14, 3),
                    image_dtype="uint16",
                    stats={
                        "image": {"max": 1000, "channel_max": [1000, 1000, 1000]},
                        "exposure": {"channel_contrast_max": 1000.0},
                    },
                )
                capture = camera_gphoto2.CaptureResult(
                    connection=camera_gphoto2.CameraConnection("Canon EOS R6 Mark III", "usb:001,010"),
                    settings=camera_gphoto2.CaptureSettings(shutter_speed="1/80"),
                    saved_file=raw_file,
                    stdout="Saving file as check.cr3",
                    decoded=decoded,
                )
                return camera_gphoto2.AutoExposureResult(
                    target_max=kwargs["target_max"],
                    final_capture=capture,
                    trials=(),
                )

            def write_preview(raw_file, **kwargs):
                output_dir = Path(kwargs["output_dir"])
                output_dir.mkdir(parents=True, exist_ok=True)
                tiff = output_dir / "preview.tiff"
                metadata = output_dir / "preview.json"
                tiff.write_bytes(b"tiff")
                metadata.write_text("{}", encoding="utf-8")
                return camera_gphoto2.DecodeResult(
                    source_file=Path(raw_file),
                    output_files=(tiff, metadata),
                    metadata_file=metadata,
                    image_shape=(12, 14, 3),
                    image_dtype="uint8",
                    stats={
                        "image": {"max": 200, "channel_max": [200, 200, 200]},
                        "exposure": {"channel_contrast_max": 100.0},
                    },
                )

            with mock.patch.object(
                location_checker.camera_gphoto2,
                "auto_expose_capture",
                side_effect=fake_auto_expose_capture,
            ), mock.patch.object(
                location_checker,
                "_decode_dcraw_preview",
                side_effect=write_preview,
            ) as preview_decode, mock.patch.object(
                location_checker,
                "_import_tifffile",
                return_value=mock.Mock(imread=lambda _path: np.full((12, 14, 3), 200, dtype=np.uint8)),
            ):
                result = location_checker.capture_location_check(location_path, output_dir=Path(tmpdir) / "out")

            self.assertEqual(len(auto_exposure_calls), 1)
            self.assertEqual(preview_decode.call_count, 1)
            self.assertEqual(preview_decode.call_args.kwargs["white_balance"], "auto")
            self.assertEqual(result.region_count, 24)
            self.assertEqual(result.shutter_speed, "1/80")
            self.assertEqual(result.capture_count, 1)
            self.assertTrue(result.overlay_file.exists())
            self.assertTrue(result.metadata_file.exists())


if __name__ == "__main__":
    unittest.main()
