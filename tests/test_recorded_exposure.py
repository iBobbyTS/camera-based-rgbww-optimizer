import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.measurement import recorded_exposure
from camera_based_rgbww_optimizer.optimization import white_calibration_common


def result(payload, *, returncode=0, stderr=""):
    return subprocess.CompletedProcess(
        args=["exiftool"],
        returncode=returncode,
        stdout=json.dumps(payload) if not isinstance(payload, str) else payload,
        stderr=stderr,
    )


class RecordedExposureTests(unittest.TestCase):
    def test_prefers_canon_makernote_over_standard_exif(self):
        exposure = recorded_exposure.resolve_recorded_exposure(
            Path("capture.cr3"),
            "1/60",
            runner=lambda _command: result(
                [{"Canon:ExposureTime": 0.015625, "ExifIFD:ExposureTime": 1 / 60}]
            ),
        )

        self.assertEqual(exposure.source, "Canon:ExposureTime")
        self.assertEqual(exposure.status, "recorded")
        self.assertAlmostEqual(exposure.seconds, 1 / 64)
        self.assertAlmostEqual(exposure.to_jsonable()["recorded_to_nominal_ratio"], 0.9375)

    def test_uses_standard_exif_when_canon_value_is_absent(self):
        exposure = recorded_exposure.resolve_recorded_exposure(
            "capture.cr3",
            "1/125",
            runner=lambda _command: result([{"ExifIFD:ExposureTime": 0.0081}]),
        )

        self.assertEqual(exposure.source, "ExifIFD:ExposureTime")
        self.assertAlmostEqual(exposure.seconds, 0.0081)

    def test_exiftool_failure_falls_back_with_diagnostic_provenance(self):
        exposure = recorded_exposure.resolve_recorded_exposure(
            "capture.cr3",
            "30",
            runner=lambda _command: result([], returncode=1, stderr="missing file"),
        )

        self.assertEqual(exposure.status, "fallback_nominal")
        self.assertEqual(exposure.source, "nominal_shutter_speed")
        self.assertEqual(exposure.seconds, 30.0)
        self.assertIn("missing file", exposure.diagnostic)

    def test_invalid_metadata_never_silently_becomes_recorded(self):
        exposure = recorded_exposure.resolve_recorded_exposure(
            "capture.cr3",
            "1/100",
            runner=lambda _command: result([{"Canon:ExposureTime": 0, "ExifIFD:ExposureTime": "bad"}]),
        )

        self.assertEqual(exposure.status, "fallback_nominal")
        self.assertIn("no positive", exposure.diagnostic)

    def test_bulb_nominal_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "bulb"):
            recorded_exposure.resolve_recorded_exposure("capture.cr3", "bulb", runner=lambda _command: result([]))

    def test_formal_measurement_rejects_nominal_fallback(self):
        fallback = recorded_exposure.RecordedExposure(
            seconds=0.01,
            source="nominal_shutter_speed",
            nominal_seconds=0.01,
            nominal_shutter_speed="1/100",
            raw_file=Path("capture.cr3"),
            status="fallback_nominal",
            metadata_values={},
            diagnostic="exiftool unavailable",
        )

        with self.assertRaisesRegex(RuntimeError, "required for P1"):
            recorded_exposure.require_recorded(fallback, purpose="P1")

    def test_setting_gate_accepts_small_canon_tv_difference(self):
        recorded_exposure.validate_recorded_exposure_setting(
            {
                "status": "recorded",
                "source": "Canon:ExposureTime",
                "seconds": 0.000193774542476587,
            },
            "1/5000",
        )

    def test_setting_gate_rejects_an_adjacent_shutter_setting(self):
        with self.assertRaisesRegex(ValueError, "different shutter setting"):
            recorded_exposure.validate_recorded_exposure_setting(
                {
                    "status": "recorded",
                    "source": "Canon:ExposureTime",
                    "seconds": 1 / 6400,
                },
                "1/5000",
            )

    def test_setting_gate_rejects_invalid_or_unrecorded_metadata(self):
        for payload in (
            {"status": "fallback_nominal", "source": "nominal_shutter_speed", "seconds": 1 / 5000},
            {"status": "recorded", "source": "Canon:ExposureTime", "seconds": float("nan")},
            {"status": "recorded", "source": "ExifIFD:ExposureTime", "seconds": 1 / 5000},
        ):
            with self.subTest(payload=payload):
                with self.assertRaisesRegex(ValueError, "missing or invalid"):
                    recorded_exposure.validate_recorded_exposure_setting(payload, "1/5000")

    def test_white_calibration_region_measurement_uses_recorded_duration(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            raw_file = root / "capture.cr3"
            npy_file = root / "capture.npy"
            raw_file.write_bytes(b"fake")
            np.save(npy_file, np.full((2, 2, 3), 100, dtype=np.uint16))
            capture = camera_gphoto2.CaptureResult(
                connection=camera_gphoto2.CameraConnection("test", "usb:test"),
                settings=camera_gphoto2.CaptureSettings(shutter_speed="1/2"),
                saved_file=raw_file,
                stdout="",
                decoded=camera_gphoto2.DecodeResult(
                    source_file=raw_file,
                    output_files=(npy_file,),
                    metadata_file=root / "capture.json",
                    image_shape=(2, 2, 3),
                    image_dtype="uint16",
                    stats={},
                ),
            )
            exposure = recorded_exposure.RecordedExposure(
                seconds=0.25,
                source="Canon:ExposureTime",
                nominal_seconds=0.5,
                nominal_shutter_speed="1/2",
                raw_file=raw_file,
                status="recorded",
                metadata_values={"Canon:ExposureTime": 0.25},
            )

            with mock.patch.object(
                white_calibration_common.recorded_exposure,
                "resolve_recorded_exposure",
                return_value=exposure,
            ):
                seconds, _vector, measurements = white_calibration_common.measure_capture_regions(
                    capture,
                    [{"type": "full", "name": "full"}],
                )

            self.assertEqual(seconds, 0.25)
            self.assertEqual(measurements[0]["normalized"]["channel_mean_per_second"], [400.0] * 3)


if __name__ == "__main__":
    unittest.main()
