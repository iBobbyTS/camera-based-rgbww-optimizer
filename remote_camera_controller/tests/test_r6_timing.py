from __future__ import annotations

import copy
import unittest

from r6_timing import (
    CaptureObservation,
    TimingMetadataError,
    append_event,
    build_capture_metadata,
    build_exposure_start_estimate,
    validate_capture_association,
    validate_observation,
)


class TimingMetadataTests(unittest.TestCase):
    def observation(self, **overrides: object) -> CaptureObservation:
        values = {
            "request_received_monotonic_ns": 1_000_000_000,
            "capture_call_started_monotonic_ns": 1_100_000_000,
            "capture_call_returned_monotonic_ns": None,
            "camera_event_observed_monotonic_ns": None,
            "camera_event_type": None,
            "file_added_observed_monotonic_ns": None,
            "download_started_monotonic_ns": 2_500_000_000,
            "download_completed_monotonic_ns": 3_000_000_000,
            "cr3_saved_observed_monotonic_ns": 3_010_000_000,
        }
        values.update(overrides)
        observation = CaptureObservation(**values)
        append_event(
            observation,
            monotonic_ns=1_100_000_000,
            event_type="capture_command_started",
            source="fake_gphoto2",
        )
        append_event(
            observation,
            monotonic_ns=3_000_000_000,
            event_type="capture_process_returned",
            source="fake_gphoto2",
        )
        return observation

    def test_file_added_event_builds_tier_a_estimate(self) -> None:
        observation = self.observation(file_added_observed_monotonic_ns=2_000_000_000)
        estimate = build_exposure_start_estimate(
            observation,
            {"seconds": 0.25, "source": "Canon:ExposureTime", "status": "recorded"},
        )
        self.assertEqual(estimate["timestamp_monotonic_ns"], 1_750_000_000)
        self.assertEqual(estimate["method"], "gphoto_event_minus_recorded_exposure")
        self.assertEqual(estimate["status"], "estimated_not_absolute")

    def test_capture_return_without_event_builds_tier_b_estimate(self) -> None:
        observation = self.observation(capture_call_returned_monotonic_ns=2_000_000_000)
        estimate = build_exposure_start_estimate(
            observation,
            {"seconds": 0.25, "source": "Canon:ExposureTime", "status": "recorded"},
        )
        self.assertEqual(estimate["timestamp_monotonic_ns"], 1_750_000_000)
        self.assertEqual(
            estimate["method"], "gphoto_capture_return_minus_recorded_exposure"
        )
        self.assertEqual(estimate["status"], "weak_estimate")

    def test_request_and_download_only_are_tier_c_unavailable(self) -> None:
        estimate = build_exposure_start_estimate(
            self.observation(),
            {"seconds": 0.25, "source": "Canon:ExposureTime", "status": "recorded"},
        )
        self.assertIsNone(estimate["timestamp_monotonic_ns"])
        self.assertIsNone(estimate["method"])
        self.assertEqual(estimate["status"], "unavailable")

    def test_missing_or_nominal_exposure_never_builds_estimate(self) -> None:
        observation = self.observation(
            capture_call_returned_monotonic_ns=2_000_000_000,
            file_added_observed_monotonic_ns=1_900_000_000,
        )
        for exposure in (
            {"seconds": None, "source": None, "status": "unavailable"},
            {"seconds": 0.25, "source": "requested_shutter", "status": "nominal_fallback"},
            {"seconds": 0.25, "source": "EXIF:ExposureTime", "status": "recorded"},
        ):
            with self.subTest(exposure=exposure):
                estimate = build_exposure_start_estimate(observation, exposure)
                self.assertEqual(estimate["status"], "unavailable")

    def test_invalid_units_negative_and_non_monotonic_values_are_rejected(self) -> None:
        invalid = (
            self.observation(request_received_monotonic_ns=-1),
            self.observation(capture_call_started_monotonic_ns=1.1),
            self.observation(capture_call_started_monotonic_ns=3_100_000_000),
            self.observation(capture_call_returned_monotonic_ns=3_100_000_000),
        )
        for observation in invalid:
            with self.subTest(observation=observation):
                with self.assertRaises(TimingMetadataError):
                    validate_observation(observation)

        reversed_events = self.observation()
        reversed_events.event_sequence[1]["monotonic_ns"] = 1_000_000_000
        with self.assertRaises(TimingMetadataError):
            validate_observation(reversed_events)

    def test_capture_association_fails_closed(self) -> None:
        payload = b"fake-cr3-payload"
        metadata = build_capture_metadata(
            capture_id="capture-1",
            request_id="request-1",
            payload=payload,
            observation=self.observation(capture_call_returned_monotonic_ns=2_000_000_000),
            recorded_exposure={
                "seconds": 0.25,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
            request_received_utc="2026-07-19T00:00:00+00:00",
        )
        mutations = []
        wrong_capture = copy.deepcopy(metadata)
        wrong_capture["capture_id"] = "capture-2"
        mutations.append(wrong_capture)
        wrong_request = copy.deepcopy(metadata)
        wrong_request["request_id"] = "request-2"
        mutations.append(wrong_request)
        wrong_hash = copy.deepcopy(metadata)
        wrong_hash["cr3"]["sha256"] = "0" * 64
        mutations.append(wrong_hash)
        for mutated in mutations:
            with self.subTest(mutated=mutated):
                with self.assertRaises(TimingMetadataError):
                    validate_capture_association(
                        mutated,
                        payload=payload,
                        expected_capture_id="capture-1",
                        expected_request_id="request-1",
                    )

    def test_network_observation_does_not_change_raw_event_or_estimate(self) -> None:
        metadata = build_capture_metadata(
            capture_id="capture-1",
            request_id="request-1",
            payload=b"payload",
            observation=self.observation(file_added_observed_monotonic_ns=2_000_000_000),
            recorded_exposure={
                "seconds": 0.25,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
            request_received_utc="2026-07-19T00:00:00+00:00",
        )
        original_estimate = copy.deepcopy(metadata["exposure_start_estimate"])
        original_event = metadata["gphoto2"]["file_added_observed_monotonic_ns"]
        metadata["network_observation"]["response_or_event_round_trip_ms"] = 12.5
        self.assertEqual(metadata["exposure_start_estimate"], original_estimate)
        self.assertEqual(
            metadata["gphoto2"]["file_added_observed_monotonic_ns"], original_event
        )

    def test_download_or_write_time_is_never_used_as_exposure_start(self) -> None:
        estimate = build_exposure_start_estimate(
            self.observation(
                download_started_monotonic_ns=1_500_000_000,
                download_completed_monotonic_ns=2_000_000_000,
                cr3_saved_observed_monotonic_ns=2_100_000_000,
            ),
            {"seconds": 0.1, "source": "Canon:ExposureTime", "status": "recorded"},
        )
        self.assertEqual(estimate["status"], "unavailable")
        self.assertIsNone(estimate["timestamp_monotonic_ns"])


if __name__ == "__main__":
    unittest.main()
