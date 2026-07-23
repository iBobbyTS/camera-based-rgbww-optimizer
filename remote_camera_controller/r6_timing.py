from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Any, Mapping


SCHEMA = "remote_capture_result_v2"
CLOCK_DOMAIN = "bridge_monotonic"
TIMING_QUALITY = "best_effort_gphoto2"
FORMAL_P7_ELIGIBILITY = "unchanged_requires_later_planner_advisor_decision"
RECORDED_EXPOSURE_SOURCES = frozenset(("Canon:ExposureTime",))
TIER_A_EVENT_TYPES = frozenset(("file_added", "capture_complete"))


class TimingMetadataError(ValueError):
    """Timing metadata is internally inconsistent or cannot be associated."""


@dataclass
class CaptureObservation:
    request_received_monotonic_ns: int
    capture_call_started_monotonic_ns: int
    capture_call_returned_monotonic_ns: int | None = None
    camera_event_observed_monotonic_ns: int | None = None
    camera_event_type: str | None = None
    file_added_observed_monotonic_ns: int | None = None
    download_started_monotonic_ns: int | None = None
    download_completed_monotonic_ns: int | None = None
    cr3_saved_observed_monotonic_ns: int | None = None
    event_sequence: list[dict[str, Any]] = field(default_factory=list)


def append_event(
    observation: CaptureObservation,
    *,
    monotonic_ns: int,
    event_type: str,
    source: str,
    payload_summary: Mapping[str, Any] | None = None,
) -> None:
    observation.event_sequence.append(
        {
            "monotonic_ns": monotonic_ns,
            "clock_domain": CLOCK_DOMAIN,
            "event_type": event_type,
            "source": source,
            "payload_summary": dict(payload_summary or {}),
        }
    )


def _require_monotonic_ns(name: str, value: object, *, optional: bool) -> int | None:
    if value is None and optional:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TimingMetadataError(f"{name} must be a non-negative integer nanosecond value")
    return value


def validate_observation(observation: CaptureObservation) -> None:
    required_names = (
        "request_received_monotonic_ns",
        "capture_call_started_monotonic_ns",
        "download_completed_monotonic_ns",
    )
    optional_names = (
        "capture_call_returned_monotonic_ns",
        "camera_event_observed_monotonic_ns",
        "file_added_observed_monotonic_ns",
        "download_started_monotonic_ns",
        "cr3_saved_observed_monotonic_ns",
    )
    values: dict[str, int | None] = {}
    for name in required_names:
        values[name] = _require_monotonic_ns(name, getattr(observation, name), optional=False)
    for name in optional_names:
        values[name] = _require_monotonic_ns(name, getattr(observation, name), optional=True)

    request_received = values["request_received_monotonic_ns"]
    capture_started = values["capture_call_started_monotonic_ns"]
    download_completed = values["download_completed_monotonic_ns"]
    assert request_received is not None
    assert capture_started is not None
    assert download_completed is not None
    if request_received > capture_started or capture_started > download_completed:
        raise TimingMetadataError("required capture timestamps are out of order")

    capture_returned = values["capture_call_returned_monotonic_ns"]
    if capture_returned is not None and not capture_started <= capture_returned <= download_completed:
        raise TimingMetadataError("capture return timestamp is out of order")
    camera_event = values["camera_event_observed_monotonic_ns"]
    if camera_event is not None and not capture_started <= camera_event <= download_completed:
        raise TimingMetadataError("camera event timestamp is out of order")
    file_added = values["file_added_observed_monotonic_ns"]
    if file_added is not None and not capture_started <= file_added <= download_completed:
        raise TimingMetadataError("file-added timestamp is out of order")
    download_started = values["download_started_monotonic_ns"]
    if download_started is not None and not capture_started <= download_started <= download_completed:
        raise TimingMetadataError("download start timestamp is out of order")
    saved = values["cr3_saved_observed_monotonic_ns"]
    if saved is not None and saved < capture_started:
        raise TimingMetadataError("CR3 saved observation timestamp is out of order")

    if (camera_event is None) != (observation.camera_event_type is None):
        raise TimingMetadataError("camera event timestamp and type must be present together")

    previous = -1
    for event in observation.event_sequence:
        if not isinstance(event, dict):
            raise TimingMetadataError("event sequence entries must be objects")
        event_ns = _require_monotonic_ns(
            "event_sequence.monotonic_ns", event.get("monotonic_ns"), optional=False
        )
        assert event_ns is not None
        if event_ns < previous:
            raise TimingMetadataError("event sequence is not monotonic")
        if event.get("clock_domain") != CLOCK_DOMAIN:
            raise TimingMetadataError("event sequence has an unsupported clock domain")
        if not isinstance(event.get("event_type"), str) or not event["event_type"]:
            raise TimingMetadataError("event sequence has an invalid event type")
        if not isinstance(event.get("source"), str) or not event["source"]:
            raise TimingMetadataError("event sequence has an invalid source")
        if not isinstance(event.get("payload_summary"), dict):
            raise TimingMetadataError("event sequence payload summary must be an object")
        previous = event_ns


def _recorded_exposure_is_usable(recorded_exposure: Mapping[str, Any]) -> bool:
    seconds = recorded_exposure.get("seconds")
    return (
        recorded_exposure.get("status") == "recorded"
        and recorded_exposure.get("source") in RECORDED_EXPOSURE_SOURCES
        and isinstance(seconds, (int, float))
        and not isinstance(seconds, bool)
        and math.isfinite(float(seconds))
        and float(seconds) > 0
    )


def build_exposure_start_estimate(
    observation: CaptureObservation,
    recorded_exposure: Mapping[str, Any],
) -> dict[str, Any]:
    validate_observation(observation)
    unavailable = {
        "timestamp_monotonic_ns": None,
        "clock_domain": CLOCK_DOMAIN,
        "method": None,
        "status": "unavailable",
        "uncertainty_ms": None,
        "uncertainty_basis": "unknown",
    }
    if not _recorded_exposure_is_usable(recorded_exposure):
        return unavailable

    exposure_ns = round(float(recorded_exposure["seconds"]) * 1_000_000_000)
    event_ns: int | None = None
    if observation.file_added_observed_monotonic_ns is not None:
        event_ns = observation.file_added_observed_monotonic_ns
    elif (
        observation.camera_event_observed_monotonic_ns is not None
        and observation.camera_event_type in TIER_A_EVENT_TYPES
    ):
        event_ns = observation.camera_event_observed_monotonic_ns

    if event_ns is not None:
        estimate_ns = event_ns - exposure_ns
        if estimate_ns >= observation.capture_call_started_monotonic_ns:
            return {
                "timestamp_monotonic_ns": estimate_ns,
                "clock_domain": CLOCK_DOMAIN,
                "method": "gphoto_event_minus_recorded_exposure",
                "status": "estimated_not_absolute",
                "uncertainty_ms": None,
                "uncertainty_basis": "unknown",
            }

    if observation.capture_call_returned_monotonic_ns is not None:
        estimate_ns = observation.capture_call_returned_monotonic_ns - exposure_ns
        if estimate_ns >= observation.capture_call_started_monotonic_ns:
            return {
                "timestamp_monotonic_ns": estimate_ns,
                "clock_domain": CLOCK_DOMAIN,
                "method": "gphoto_capture_return_minus_recorded_exposure",
                "status": "weak_estimate",
                "uncertainty_ms": None,
                "uncertainty_basis": "unknown",
            }
    return unavailable


def build_capture_metadata(
    *,
    capture_id: str,
    request_id: str,
    payload: bytes,
    observation: CaptureObservation,
    recorded_exposure: Mapping[str, Any],
    request_received_utc: str,
) -> dict[str, Any]:
    if not capture_id or not request_id:
        raise TimingMetadataError("capture_id and request_id must be non-empty")
    validate_observation(observation)
    metadata = {
        "schema": SCHEMA,
        "capture_id": capture_id,
        "request_id": request_id,
        "timing_quality": TIMING_QUALITY,
        "formal_p7_eligibility": FORMAL_P7_ELIGIBILITY,
        "cr3": {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
            "content_type": "image/x-canon-cr3",
        },
        "gphoto2": {
            "driver_event_type": observation.camera_event_type,
            "event_sequence": observation.event_sequence,
            "request_received_monotonic_ns": observation.request_received_monotonic_ns,
            "capture_call_started_monotonic_ns": observation.capture_call_started_monotonic_ns,
            "capture_call_returned_monotonic_ns": observation.capture_call_returned_monotonic_ns,
            "camera_event_observed_monotonic_ns": observation.camera_event_observed_monotonic_ns,
            "file_added_observed_monotonic_ns": observation.file_added_observed_monotonic_ns,
            "download_started_monotonic_ns": observation.download_started_monotonic_ns,
            "download_completed_monotonic_ns": observation.download_completed_monotonic_ns,
            "cr3_saved_observed_monotonic_ns": observation.cr3_saved_observed_monotonic_ns,
            "clock_domain": CLOCK_DOMAIN,
        },
        "recorded_exposure": dict(recorded_exposure),
        "exposure_start_estimate": build_exposure_start_estimate(
            observation, recorded_exposure
        ),
        "network_observation": {
            "request_id": request_id,
            "response_or_event_round_trip_ms": None,
            "uncertainty_ms": None,
            "uncertainty_basis": "unknown",
        },
        "bridge_utc_observation": {
            "request_received": request_received_utc,
            "source": "bridge_system_clock_utc",
        },
    }
    validate_capture_association(
        metadata,
        payload=payload,
        expected_capture_id=capture_id,
        expected_request_id=request_id,
    )
    return metadata


def validate_capture_association(
    metadata: Mapping[str, Any],
    *,
    payload: bytes,
    expected_capture_id: str,
    expected_request_id: str,
) -> None:
    if metadata.get("schema") != SCHEMA:
        raise TimingMetadataError("capture metadata schema mismatch")
    if metadata.get("capture_id") != expected_capture_id:
        raise TimingMetadataError("capture ID mismatch")
    if metadata.get("request_id") != expected_request_id:
        raise TimingMetadataError("request ID mismatch")
    cr3 = metadata.get("cr3")
    if not isinstance(cr3, Mapping):
        raise TimingMetadataError("CR3 metadata is missing")
    if cr3.get("sha256") != hashlib.sha256(payload).hexdigest():
        raise TimingMetadataError("CR3 hash mismatch")
    if cr3.get("byte_count") != len(payload):
        raise TimingMetadataError("CR3 byte count mismatch")
