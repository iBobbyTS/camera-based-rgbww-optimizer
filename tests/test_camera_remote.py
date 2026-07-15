import io
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from urllib import error

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote


class FakeResponse:
    def __init__(self, chunks):
        self.chunks = iter(chunks)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _traceback):
        return None

    def read(self, size=None):
        if size is None:
            return b"".join(self.chunks)
        if size != camera_remote.DOWNLOAD_CHUNK_SIZE:
            raise AssertionError(size)
        return next(self.chunks, b"")


class RemoteCameraConfigTests(unittest.TestCase):
    def test_environment_overrides_env_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text(
                f"{camera_remote.BASE_URL_ENV}=http://file-host:8088\n"
                f"{camera_remote.TOKEN_ENV}=file-token\n",
                encoding="utf-8",
            )
            config = camera_remote.load_remote_camera_config(
                env_file=env_file,
                environ={
                    camera_remote.BASE_URL_ENV: "https://process-host/bridge/",
                    camera_remote.TOKEN_ENV: "process-token",
                },
            )

        self.assertEqual(config.base_url, "https://process-host/bridge")
        self.assertEqual(config.token, "process-token")
        self.assertEqual(config.capture_url, "https://process-host/bridge/v1/capture")

    def test_missing_token_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(camera_remote.RemoteCameraError, camera_remote.TOKEN_ENV):
                camera_remote.load_remote_camera_config(env_file=Path(tmpdir) / ".env", environ={})

    def test_invalid_env_entry_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("not-an-assignment\n", encoding="utf-8")
            with self.assertRaisesRegex(camera_remote.RemoteCameraError, ":1"):
                camera_remote.load_remote_camera_config(env_file=env_file, environ={})


class RemoteCameraCaptureTests(unittest.TestCase):
    def test_capture_posts_bearer_token_and_atomically_saves_response(self):
        observed = {}

        def opener(capture_request, *, timeout):
            observed["url"] = capture_request.full_url
            observed["method"] = capture_request.get_method()
            observed["authorization"] = capture_request.get_header("Authorization")
            observed["timeout"] = timeout
            return FakeResponse([b"fake ", b"cr3"])

        with tempfile.TemporaryDirectory() as tmpdir:
            result = camera_remote.capture_remote_image(
                output_dir=tmpdir,
                filename_template="capture-%Y%m%d.%C",
                config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret-token"),
                timeout=45,
                opener=opener,
                now=datetime(2026, 7, 14, 12, 30, 0),
            )
            payload = result.saved_file.read_bytes()
            partials = list(Path(tmpdir).glob("*.part")) + list(Path(tmpdir).glob(".*.part"))

        self.assertEqual(observed["url"], "http://camera.local:8088/v1/capture")
        self.assertEqual(observed["method"], "POST")
        self.assertEqual(observed["authorization"], "Bearer secret-token")
        self.assertEqual(observed["timeout"], 45)
        self.assertEqual(result.saved_file.name, "capture-20260714.cr3")
        self.assertEqual(result.byte_count, 8)
        self.assertEqual(payload, b"fake cr3")
        self.assertEqual(partials, [])
        self.assertNotIn("secret-token", str(result.to_jsonable()))

    def test_empty_response_does_not_replace_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "capture.cr3"
            destination.write_bytes(b"existing")
            with self.assertRaisesRegex(camera_remote.RemoteCameraError, "empty"):
                camera_remote.capture_remote_image(
                    output_dir=tmpdir,
                    filename_template="capture.cr3",
                    config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                    opener=lambda *_args, **_kwargs: FakeResponse([]),
                )
            payload = destination.read_bytes()
            partials = list(Path(tmpdir).glob("*.part")) + list(Path(tmpdir).glob(".*.part"))

        self.assertEqual(payload, b"existing")
        self.assertEqual(partials, [])

    def test_http_error_does_not_include_token(self):
        def opener(*_args, **_kwargs):
            raise error.HTTPError("http://camera.local/v1/capture", 401, "Unauthorized", {}, None)

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(camera_remote.RemoteCameraError, "status 401") as caught:
                camera_remote.capture_remote_image(
                    output_dir=tmpdir,
                    config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret-token"),
                    opener=opener,
                )

        self.assertNotIn("secret-token", str(caught.exception))

    def test_filename_cannot_escape_output_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(camera_remote.RemoteCameraError, "inside output_dir"):
                camera_remote.capture_remote_image(
                    output_dir=tmpdir,
                    filename_template="../capture.cr3",
                    config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                    opener=lambda *_args, **_kwargs: FakeResponse([b"unused"]),
                )

    def test_capture_sends_requested_exposure_settings_as_json(self):
        observed = {}

        def opener(capture_request, *, timeout):
            observed["payload"] = json.loads(capture_request.data.decode("utf-8"))
            observed["content_type"] = capture_request.get_header("Content-type")
            return FakeResponse([b"raw"])

        with tempfile.TemporaryDirectory() as tmpdir:
            camera_remote.capture_remote_image(
                output_dir=tmpdir,
                filename_template="capture.cr3",
                config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                settings=camera_gphoto2.CaptureSettings(
                    iso="125",
                    aperture="implicit auto",
                    shutter_speed="1/250",
                    image_format="RAW",
                ),
                opener=opener,
            )

        self.assertEqual(
            observed["payload"],
            {"iso": "125", "aperture": "implicit auto", "shutter_speed": "1/250"},
        )
        self.assertEqual(observed["content_type"], "application/json")

    def test_camera_busy_retries_complete_request(self):
        attempts = []
        sleeps = []

        def opener(_capture_request, *, timeout):
            attempts.append(timeout)
            if len(attempts) == 1:
                raise error.HTTPError(
                    "http://camera.local/v1/capture",
                    409,
                    "Conflict",
                    {},
                    io.BytesIO(b'{"error":"camera_busy"}'),
                )
            return FakeResponse([b"raw"])

        with tempfile.TemporaryDirectory() as tmpdir:
            result = camera_remote.capture_remote_image(
                output_dir=tmpdir,
                filename_template="capture.cr3",
                config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                opener=opener,
                busy_retries=1,
                busy_retry_delay=0.25,
                sleep_fn=sleeps.append,
            )

        self.assertEqual(result.byte_count, 3)
        self.assertEqual(len(attempts), 2)
        self.assertEqual(sleeps, [0.25])


class RemoteCameraExposureTests(unittest.TestCase):
    CONFIG_PAYLOAD = {
        "iso": {"current": "125", "choices": ["100", "125", "200"]},
        "aperture": {"current": "implicit auto", "choices": ["implicit auto"]},
        "shutter_speed": {"current": "1/100", "choices": ["1/100", "1/50"]},
        "image_format": {"current": "RAW", "fixed": "RAW"},
    }

    def test_reads_remote_config_and_uses_current_values_when_unspecified(self):
        observed = {}

        def opener(config_request, *, timeout):
            observed["method"] = config_request.get_method()
            observed["authorization"] = config_request.get_header("Authorization")
            return FakeResponse([json.dumps(self.CONFIG_PAYLOAD).encode("utf-8")])

        config = camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret")
        settings = camera_remote.read_remote_camera_settings(config=config, opener=opener)
        backend = camera_remote.RemoteCameraBackend(config=config, opener=opener)
        resolved = backend.resolve_capture_settings(iso=None, aperture=None, image_format="RAW")

        self.assertEqual(observed, {"method": "GET", "authorization": "Bearer secret"})
        self.assertEqual(settings.shutter_speed.choices, ("1/100", "1/50"))
        self.assertEqual(resolved.iso, "125")
        self.assertEqual(resolved.aperture, "implicit auto")

    def test_shared_auto_exposure_runs_entire_search_through_remote_backend(self):
        capture_payloads = []

        def opener(remote_request, *, timeout):
            if remote_request.get_method() == "GET":
                return FakeResponse([json.dumps(self.CONFIG_PAYLOAD).encode("utf-8")])
            payload = json.loads(remote_request.data.decode("utf-8"))
            capture_payloads.append(payload)
            return FakeResponse([payload["shutter_speed"].encode("ascii")])

        def meter(raw_file):
            shutter = Path(raw_file).read_text(encoding="ascii")
            maximum = {"1/100": 10000, "1/50": 48000}[shutter]
            return camera_gphoto2.ExposureMeasurement(maximum=maximum, exposure_metric=float(maximum))

        backend = camera_remote.RemoteCameraBackend(
            config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret"),
            opener=opener,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            result = camera_gphoto2.auto_expose_capture(
                output_dir=Path(tmpdir) / "final",
                filename_template="final.cr3",
                target_max=49152,
                iso=None,
                aperture=None,
                min_shutter_speed="1/100",
                max_shutter_speed="1/50",
                camera_backend=backend,
                meter_fn=meter,
            )

        self.assertEqual(result.final_capture.settings.shutter_speed, "1/50")
        self.assertGreaterEqual(len(capture_payloads), 2)
        self.assertTrue(all(payload["iso"] == "125" for payload in capture_payloads))
        self.assertTrue(all(payload["aperture"] == "implicit auto" for payload in capture_payloads))
        self.assertEqual(capture_payloads[-1]["shutter_speed"], "1/50")


if __name__ == "__main__":
    unittest.main()
