import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from urllib import error
from unittest import mock

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote
from camera_based_rgbww_optimizer.control import camera_remote_v2


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


class FakeV2Response(FakeResponse):
    def __init__(self, body, *, content_type, headers=None, status=200):
        super().__init__([body])
        self.status = status
        self.headers = {"Content-Type": content_type, **(headers or {})}


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
    def _v2_response(self, *, payload=b"fake-cr3-v2", boundary="v2-boundary", metadata=None, headers=None):
        if metadata is None:
            metadata = {
                "schema": "remote_capture_result_v2", "capture_id": "capture-v2", "request_id": "request-v2",
                "timing_quality": "best_effort_gphoto2", "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
                "cr3": {"sha256": hashlib.sha256(payload).hexdigest(), "byte_count": len(payload), "content_type": "image/x-canon-cr3"},
                "gphoto2": {
                    "driver_event_type": None, "event_sequence": [],
                    "request_received_monotonic_ns": 1_000_000_000,
                    "capture_call_started_monotonic_ns": 1_100_000_000,
                    "capture_call_returned_monotonic_ns": 2_000_000_000,
                    "camera_event_observed_monotonic_ns": None, "file_added_observed_monotonic_ns": None,
                    "download_started_monotonic_ns": 2_100_000_000,
                    "download_completed_monotonic_ns": 3_000_000_000,
                    "cr3_saved_observed_monotonic_ns": 3_010_000_000,
                    "clock_domain": "bridge_monotonic",
                },
                "recorded_exposure": {"seconds": 0.25, "source": "Canon:ExposureTime", "status": "recorded"},
                "exposure_start_estimate": {
                    "timestamp_monotonic_ns": 1_750_000_000, "clock_domain": "bridge_monotonic",
                    "method": "gphoto_capture_return_minus_recorded_exposure", "status": "weak_estimate",
                    "uncertainty_ms": None, "uncertainty_basis": "unknown",
                },
                "network_observation": {"request_id": "request-v2", "response_or_event_round_trip_ms": None, "uncertainty_ms": None, "uncertainty_basis": "unknown"},
            }
        self._last_v2_metadata = json.loads(json.dumps(metadata))
        content = (
            f"--{boundary}\r\nContent-Type: application/json\r\nContent-ID: metadata\r\n\r\n".encode()
            + json.dumps(metadata, sort_keys=True).encode()
            + f"\r\n--{boundary}\r\nContent-Type: image/x-canon-cr3\r\nContent-ID: cr3\r\n\r\n".encode()
            + payload + f"\r\n--{boundary}--\r\n".encode()
        )
        return FakeV2Response(
            content,
            content_type=f'multipart/mixed; boundary="{boundary}"',
            headers={"X-Capture-ID": metadata["capture_id"], "X-Request-ID": metadata["request_id"], **(headers or {})},
        )

    def test_v2_multipart_saves_cr3_metadata_and_rebuilds_tier_b_timing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            response = self._v2_response()
            result = camera_remote.capture_remote_image_v2(
                output_dir=tmpdir, filename_template="capture.cr3",
                config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret-token"),
                opener=lambda *_args, **_kwargs: response,
                local_readback_done_monotonic_s=9.0,
                monotonic_fn=iter((10.0, 12.0)).__next__,
            )
            self.assertEqual(result.timing_evidence["tier"], "tier_b")
            self.assertAlmostEqual(result.timing_evidence["bridge_relative_delay_s"], 0.75)
            self.assertAlmostEqual(result.timing_evidence["best_effort_elapsed_s"], 1.75)
            self.assertEqual(result.saved_file.read_bytes(), b"fake-cr3-v2")
            metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(metadata["schema"], "remote_capture_result_v2")
            self.assertEqual(metadata["_local_receipt"]["parser_version"], camera_remote_v2.PARSER_VERSION)
            self.assertNotIn("secret-token", result.to_jsonable().__repr__())

    def test_v2_parser_rejects_schema_hash_ids_and_part_count_tampering(self):
        payload = b"payload"
        base = self._v2_response(payload=payload)
        for mutation in ("schema", "hash"):
            mutated = json.loads(json.dumps(self._last_v2_metadata))
            if mutation == "schema":
                mutated["schema"] = "wrong"
            else:
                mutated["cr3"]["sha256"] = "0" * 64
            response = self._v2_response(payload=payload, metadata=mutated)
            with self.subTest(mutation=mutation), self.assertRaises(camera_remote_v2.RemoteCaptureV2Error):
                camera_remote_v2.parse_v2_multipart(content_type=response.headers["Content-Type"], body=b"".join(response.chunks))
        with self.assertRaises(camera_remote_v2.RemoteCaptureV2Error):
            response = self._v2_response(payload=payload, headers={"X-Capture-ID": "wrong"})
            camera_remote.capture_remote_image_v2(
                output_dir=tempfile.mkdtemp(), filename_template="capture.cr3",
                config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                opener=lambda *_args, **_kwargs: response, local_readback_done_monotonic_s=9,
                monotonic_fn=iter((10.0, 12.0)).__next__,
            )
        base = self._v2_response(payload=payload)
        body = b"".join(base.chunks)
        extra = body.replace(b"\r\n--v2-boundary--", b"\r\n--v2-boundary\r\nContent-Type: text/plain\r\n\r\nextra\r\n--v2-boundary--")
        with self.assertRaises(camera_remote_v2.RemoteCaptureV2Error):
            camera_remote_v2.parse_v2_multipart(content_type=base.headers["Content-Type"], body=extra)

    def test_v2_metadata_replace_failure_removes_cr3_and_partial_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            response = self._v2_response()
            with mock.patch.object(camera_remote.os, "replace", side_effect=[None, OSError("metadata replace failed")]):
                with self.assertRaisesRegex(OSError, "metadata replace failed"):
                    camera_remote.capture_remote_image_v2(
                        output_dir=tmpdir, filename_template="capture.cr3",
                        config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "token"),
                        opener=lambda *_args, **_kwargs: response, local_readback_done_monotonic_s=9,
                        monotonic_fn=iter((10.0, 12.0)).__next__,
                    )
            self.assertEqual(list(Path(tmpdir).iterdir()), [])

    def test_v2_tier_a_and_tier_c_reconstruction_boundaries(self):
        payload = b"tier-a"
        response = self._v2_response(payload=payload)
        parsed = camera_remote_v2.parse_v2_multipart(content_type=response.headers["Content-Type"], body=b"".join(response.chunks))
        parsed.metadata["exposure_start_estimate"] = {
            "timestamp_monotonic_ns": 2_000_000_000, "clock_domain": "bridge_monotonic",
            "method": "gphoto_event_minus_recorded_exposure", "status": "estimated_not_absolute",
            "uncertainty_ms": None, "uncertainty_basis": "unknown",
        }
        parsed.metadata["gphoto2"]["file_added_observed_monotonic_ns"] = 2_250_000_000
        parsed.metadata["gphoto2"]["event_sequence"] = [{"monotonic_ns": 2_250_000_000, "clock_domain": "bridge_monotonic", "event_type": "file_added", "source": "fake", "payload_summary": {}}]
        camera_remote_v2.validate_capture_metadata(parsed.metadata, payload=payload)
        evidence = camera_remote_v2.reconstruct_best_effort_timing(parsed.metadata, local_request_started_monotonic_s=10, local_response_received_monotonic_s=12, local_readback_done_monotonic_s=9)
        self.assertEqual(evidence["tier"], "tier_a")

        tier_c = json.loads(json.dumps(parsed.metadata))
        tier_c["exposure_start_estimate"] = {
            "timestamp_monotonic_ns": None, "clock_domain": "bridge_monotonic",
            "method": None, "status": "unavailable", "uncertainty_ms": None, "uncertainty_basis": "unknown",
        }
        camera_remote_v2.validate_capture_metadata(tier_c, payload=payload)
        unavailable = camera_remote_v2.reconstruct_best_effort_timing(
            tier_c, local_request_started_monotonic_s=10, local_response_received_monotonic_s=12,
            local_readback_done_monotonic_s=9,
        )
        self.assertEqual(unavailable["tier"], "tier_c")
        self.assertEqual(unavailable["status"], "timing_evidence_unavailable")
        self.assertIsNone(unavailable["best_effort_elapsed_s"])
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
        self.assertEqual(result.http_attempts, 2)
        self.assertEqual(len(attempts), 2)
        self.assertEqual(sleeps, [0.25])

    def test_interrupted_download_removes_partial_and_never_installs_capture(self):
        class InterruptedResponse(FakeResponse):
            def read(self, size=None):
                if size is None:
                    return super().read(size)
                chunk = super().read(size)
                if chunk == b"second":
                    raise OSError("download interrupted")
                return chunk

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(OSError, "interrupted"):
                camera_remote.capture_remote_image(
                    output_dir=tmpdir,
                    filename_template="capture.cr3",
                    config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret"),
                    opener=lambda *_args, **_kwargs: InterruptedResponse([b"first", b"second"]),
                )
            files = list(Path(tmpdir).iterdir())

        self.assertEqual(files, [])

    def test_atomic_replace_failure_removes_partial_and_never_reports_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(camera_remote.os, "replace", side_effect=OSError("replace failed")):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    camera_remote.capture_remote_image(
                        output_dir=tmpdir,
                        filename_template="capture.cr3",
                        config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret"),
                        opener=lambda *_args, **_kwargs: FakeResponse([b"raw"]),
                    )
            files = list(Path(tmpdir).iterdir())

        self.assertEqual(files, [])


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

    def test_config_busy_retries_then_succeeds_and_persistent_busy_is_bounded(self):
        attempts = []

        def succeeds_after_busy(remote_request, *, timeout):
            attempts.append(remote_request.full_url)
            if len(attempts) == 1:
                raise error.HTTPError(
                    remote_request.full_url, 409, "Conflict", {}, io.BytesIO(b'{"error":"camera_busy"}')
                )
            return FakeResponse([json.dumps(self.CONFIG_PAYLOAD).encode("utf-8")])

        config = camera_remote.RemoteCameraConfig("http://camera.local:8088", "secret")
        settings = camera_remote.read_remote_camera_settings(
            config=config,
            opener=succeeds_after_busy,
            busy_retries=1,
            sleep_fn=lambda _seconds: None,
        )
        self.assertEqual(settings.aperture.current, "implicit auto")
        self.assertEqual(len(attempts), 2)

        def always_busy(remote_request, *, timeout):
            raise error.HTTPError(
                remote_request.full_url, 409, "Conflict", {}, io.BytesIO(b'{"error":"camera_busy"}')
            )

        with self.assertRaises(camera_remote.RemoteCameraHTTPError) as caught:
            camera_remote.read_remote_camera_settings(
                config=config,
                opener=always_busy,
                busy_retries=1,
                sleep_fn=lambda _seconds: None,
            )
        self.assertEqual(caught.exception.status, 409)


class RemoteCameraCliTests(unittest.TestCase):
    def test_health_is_unauthenticated_and_json_output_has_no_token(self):
        observed = {}

        def opener(remote_request, *, timeout):
            observed["url"] = remote_request.full_url
            observed["authorization"] = remote_request.get_header("Authorization")
            return FakeResponse([b'{"status":"ok"}'])

        payload = camera_remote.read_remote_health(
            base_url="http://camera.local:8088",
            opener=opener,
        )
        self.assertEqual(payload, {"status": "ok"})
        self.assertEqual(observed, {"url": "http://camera.local:8088/health", "authorization": None})

    def test_config_cli_outputs_summary_without_token_and_stable_http_exit_codes(self):
        backend = camera_remote.RemoteCameraBackend(
            config=camera_remote.RemoteCameraConfig("http://camera.local:8088", "super-secret"),
            opener=lambda *_args, **_kwargs: FakeResponse(
                [json.dumps(RemoteCameraExposureTests.CONFIG_PAYLOAD).encode("utf-8")]
            ),
        )
        stdout = io.StringIO()
        with mock.patch.object(camera_remote.RemoteCameraBackend, "from_environment", return_value=backend):
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(camera_remote.main(["config", "--json"]), 0)
        rendered = stdout.getvalue()
        self.assertIn('"aperture": "implicit auto"', rendered)
        self.assertNotIn("super-secret", rendered)

        with mock.patch.object(
            camera_remote,
            "read_remote_health",
            side_effect=camera_remote.RemoteCameraHTTPError(502),
        ), mock.patch.object(camera_remote, "load_remote_camera_base_url", return_value="http://camera.local:8088"):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(camera_remote.main(["health", "--json"]), 4)

    def test_config_cli_missing_token_is_nonzero_and_does_not_expose_secret_arguments(self):
        with tempfile.TemporaryDirectory() as tmpdir, contextlib.redirect_stderr(io.StringIO()) as stderr:
            code = camera_remote.main(["config", "--json", "--env-file", str(Path(tmpdir) / ".env")])
        self.assertEqual(code, 1)
        self.assertIn(camera_remote.TOKEN_ENV, stderr.getvalue())
        self.assertNotIn("Authorization", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
