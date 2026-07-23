from __future__ import annotations

import atexit
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


RUNTIME_PARENT = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))
if not RUNTIME_PARENT.is_dir() or not os.access(RUNTIME_PARENT, os.W_OK):
    RUNTIME_PARENT = Path("/Volumes/4T/temp/rgbww-optimizer")
    RUNTIME_PARENT.mkdir(parents=True, exist_ok=True)
TEST_ROOT = Path(
    tempfile.mkdtemp(prefix="r6-camera-bridge-tests-", dir=RUNTIME_PARENT)
)
TOKEN_PATH = TEST_ROOT / "token"
TOKEN_PATH.write_text("offline-test-token\n", encoding="utf-8")
os.environ["CAMERA_TOKEN_FILE"] = str(TOKEN_PATH)
os.environ["CAPTURE_TEMP_DIR"] = str(TEST_ROOT / "captures")
atexit.register(shutil.rmtree, TEST_ROOT, True)

import r6_camera_bridge as bridge
from r6_timing import CaptureObservation, build_capture_metadata


class BridgeCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = bridge.app.test_client()
        self.authorization = {"Authorization": f"Bearer {bridge.API_TOKEN}"}
        self.payload = b"offline-fake-cr3"
        observation = CaptureObservation(
            request_received_monotonic_ns=1_000_000_000,
            capture_call_started_monotonic_ns=1_100_000_000,
            capture_call_returned_monotonic_ns=1_500_000_000,
            download_started_monotonic_ns=1_600_000_000,
            download_completed_monotonic_ns=1_800_000_000,
            cr3_saved_observed_monotonic_ns=1_810_000_000,
        )
        self.metadata = build_capture_metadata(
            capture_id="capture-fixed",
            request_id="request-fixed",
            payload=self.payload,
            observation=observation,
            recorded_exposure={
                "seconds": 0.1,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
            request_received_utc="2026-07-19T00:00:00+00:00",
        )

    def fake_capture(self, *args: object, **kwargs: object) -> tuple[bytes, str, dict[str, object]]:
        metadata = json.loads(json.dumps(self.metadata))
        metadata["capture_id"] = kwargs["capture_id"]
        metadata["request_id"] = kwargs["request_id"]
        metadata["network_observation"]["request_id"] = kwargs["request_id"]
        return self.payload, "r6-test.cr3", metadata

    def test_v1_binary_response_remains_compatible(self) -> None:
        with mock.patch.object(
            bridge, "_capture_payload_and_metadata", side_effect=self.fake_capture
        ):
            response = self.client.post("/v1/capture", headers=self.authorization, json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.payload)
        self.assertEqual(response.content_type, "application/octet-stream")
        self.assertNotIn(b"remote_capture_result_v2", response.data)

    def test_v2_returns_associated_multipart_metadata_and_cr3(self) -> None:
        with mock.patch.object(
            bridge, "_capture_payload_and_metadata", side_effect=self.fake_capture
        ):
            response = self.client.post("/v2/capture", headers=self.authorization, json={})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content_type.startswith("multipart/mixed; boundary="))
        self.assertIn(b"remote_capture_result_v2", response.data)
        self.assertIn(self.payload, response.data)
        self.assertIn(response.headers["X-Capture-ID"].encode(), response.data)
        self.assertIn(response.headers["X-Request-ID"].encode(), response.data)

    def test_api_response_excludes_secrets_serials_and_internal_paths(self) -> None:
        with mock.patch.object(
            bridge, "_capture_payload_and_metadata", side_effect=self.fake_capture
        ):
            response = self.client.post("/v2/capture", headers=self.authorization, json={})
        forbidden = (
            bridge.API_TOKEN.encode(),
            b".env",
            b"serial",
            b"/run/r6-camera-bridge",
            b"/home/ibobby",
        )
        for value in forbidden:
            with self.subTest(value=value):
                self.assertNotIn(value, response.data)

    def test_fake_gphoto2_output_records_observed_cli_events_only(self) -> None:
        script = (
            "print('New file is in location /store_00020001/DCIM/100CANON/IMG_0001.CR3')\n"
            "print('Saving file as capture.cr3')\n"
        )
        observation = bridge._run_timed_capture(
            [sys.executable, "-c", script], bridge.time.monotonic_ns()
        )
        self.assertIsNotNone(observation.capture_call_returned_monotonic_ns)
        self.assertIsNotNone(observation.download_started_monotonic_ns)
        self.assertIsNone(observation.camera_event_observed_monotonic_ns)
        self.assertIsNone(observation.file_added_observed_monotonic_ns)
        summaries = json.dumps(observation.event_sequence, sort_keys=True)
        self.assertNotIn("/store_", summaries)
        self.assertNotIn("capture.cr3", summaries)

    def test_recorded_exposure_uses_canon_makernote_authority(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="0.000153798956285995\n", stderr=""
        )
        with mock.patch.object(bridge.subprocess, "run", return_value=completed) as run:
            result = bridge._recorded_exposure(Path("capture.cr3"))

        self.assertEqual(
            result,
            {
                "seconds": 0.000153798956285995,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
        )
        command = run.call_args.args[0]
        self.assertIn("-Canon:ExposureTime", command)
        self.assertNotIn("-EXIF:ExposureTime", command)

    def test_recorded_exposure_fails_closed_without_valid_canon_value(self) -> None:
        cases = (
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout="not-a-number\n", stderr=""
            ),
            subprocess.CompletedProcess(
                args=[], returncode=1, stdout="0.00015625\n", stderr="failed"
            ),
        )
        for completed in cases:
            with self.subTest(completed=completed):
                with mock.patch.object(
                    bridge.subprocess, "run", return_value=completed
                ):
                    self.assertEqual(
                        bridge._recorded_exposure(Path("capture.cr3")),
                        {"seconds": None, "source": None, "status": "unavailable"},
                    )

    def test_recorded_exposure_fails_closed_when_exiftool_is_unavailable(self) -> None:
        with mock.patch.object(
            bridge.subprocess, "run", side_effect=FileNotFoundError
        ):
            self.assertEqual(
                bridge._recorded_exposure(Path("capture.cr3")),
                {"seconds": None, "source": None, "status": "unavailable"},
            )


if __name__ == "__main__":
    unittest.main()
