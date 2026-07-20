from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime
from email import policy
from email.parser import BytesParser
from email.message import Message
from typing import Any, Mapping


SCHEMA = "remote_capture_result_v2"
PARSER_VERSION = "camera_remote_v2_multipart_parser_v1"
TIMING_CONTRACT = "best_effort_gphoto2_v1"
TIMING_PROVENANCE = "best_effort_gphoto2_exposure_start_estimate"
MAX_METADATA_BYTES = 256 * 1024
MAX_MULTIPART_BYTES = 256 * 1024 * 1024
CR3_CONTENT_TYPES = frozenset(("image/x-canon-cr3",))
ALLOWED_RESPONSE_HEADERS = frozenset(
    ("content-type", "content-length", "cache-control", "x-capture-id", "x-request-id", "x-capture-metadata-schema")
)
ALLOWED_PART_HEADERS = frozenset(
    ("content-type", "content-id", "content-disposition", "content-transfer-encoding")
)
REQUIRED_RESPONSE_HEADERS = frozenset(
    ("content-type", "content-length", "x-capture-id", "x-request-id", "x-capture-metadata-schema")
)
REMOTE_METADATA_KEYS = frozenset(
    (
        "schema", "capture_id", "request_id", "timing_quality", "formal_p7_eligibility",
        "cr3", "gphoto2", "recorded_exposure", "exposure_start_estimate",
        "network_observation", "bridge_utc_observation",
    )
)
LOCAL_RECEIPT_KEYS = frozenset(
    (
        "parser_version", "response_headers", "multipart_body_byte_count",
        "multipart_body_sha256", "http_attempts", "successful_attempt_index",
        "local_request_started_monotonic_s", "local_response_received_monotonic_s",
        "received_monotonic_s", "timing_evidence",
    )
)


class RemoteCaptureV2Error(ValueError):
    """The v2 response or timing metadata is not auditable."""


@dataclass(frozen=True)
class ParsedV2Multipart:
    metadata: dict[str, Any]
    cr3_bytes: bytes
    response_headers: dict[str, str]
    parser_version: str = PARSER_VERSION


def _header_value(response: Any, name: str) -> str | None:
    headers = getattr(response, "headers", None)
    if headers is not None:
        value = headers.get(name)
        if value is not None:
            return str(value)
        for key, candidate in getattr(headers, "items", lambda: ())():
            if str(key).lower() == name.lower():
                return str(candidate)
    getter = getattr(response, "getheader", None)
    if getter is not None:
        value = getter(name)
        if value is not None:
            return str(value)
    return None


def response_header_summary(response: Any) -> dict[str, str]:
    summary: dict[str, str] = {}
    for name in ALLOWED_RESPONSE_HEADERS:
        value = _header_value(response, name)
        if value is not None:
            if len(value) > 4096:
                raise RemoteCaptureV2Error(f"response header is too large: {name}")
            summary[name] = value
    return summary


def _content_type_and_boundary(value: str | None) -> tuple[str, str]:
    if not value:
        raise RemoteCaptureV2Error("v2 response lacks Content-Type")
    try:
        header_bytes = f"Content-Type: {value}\r\n\r\n".encode("ascii", "strict")
    except UnicodeEncodeError as exc:
        raise RemoteCaptureV2Error("v2 Content-Type is not ASCII") from exc
    message = BytesParser(policy=policy.HTTP).parsebytes(header_bytes)
    if message.get_content_type() != "multipart/mixed":
        raise RemoteCaptureV2Error("v2 response must be multipart/mixed")
    boundary = message.get_boundary()
    if not boundary or len(boundary) > 200:
        raise RemoteCaptureV2Error("v2 multipart boundary is missing or invalid")
    return message.get_content_type(), boundary


def _part_headers_are_allowed(part: Message) -> None:
    for name, _value in part.raw_items():
        if name.lower() not in ALLOWED_PART_HEADERS:
            raise RemoteCaptureV2Error(f"unsupported multipart part header: {name}")


def _require_exact_keys(value: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    actual = set(value)
    if actual != expected:
        unknown = sorted(actual - expected)
        missing = sorted(expected - actual)
        raise RemoteCaptureV2Error(f"{name} fields differ from frozen schema; missing={missing}, unknown={unknown}")


def _validate_part_association(part: Message, *, content_id: str, disposition: str, name: str) -> None:
    if part.get("Content-ID") != f"<{content_id}>":
        raise RemoteCaptureV2Error(f"v2 {name} part Content-ID mismatch")
    if part.get_content_disposition() != disposition:
        raise RemoteCaptureV2Error(f"v2 {name} part Content-Disposition mismatch")
    if part.get_param("name", header="content-disposition") != name:
        raise RemoteCaptureV2Error(f"v2 {name} part disposition name mismatch")


def _json_metadata(payload: bytes) -> dict[str, Any]:
    if len(payload) > MAX_METADATA_BYTES:
        raise RemoteCaptureV2Error("v2 metadata exceeds the conservative size limit")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RemoteCaptureV2Error("v2 metadata is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise RemoteCaptureV2Error("v2 metadata must be a JSON object")
    return value


def parse_v2_multipart(*, content_type: str | None, body: bytes, response_headers: Mapping[str, str] | None = None) -> ParsedV2Multipart:
    if len(body) > MAX_MULTIPART_BYTES:
        raise RemoteCaptureV2Error("v2 multipart body exceeds the conservative size limit")
    if response_headers is None or not REQUIRED_RESPONSE_HEADERS.issubset(response_headers):
        missing = sorted(REQUIRED_RESPONSE_HEADERS - set(response_headers or {}))
        raise RemoteCaptureV2Error(f"v2 response lacks required association headers: {missing}")
    try:
        declared_length = int(response_headers["content-length"])
    except (TypeError, ValueError) as exc:
        raise RemoteCaptureV2Error("v2 Content-Length is invalid") from exc
    if declared_length < 0 or declared_length != len(body):
        raise RemoteCaptureV2Error("v2 Content-Length differs from received body")
    if response_headers["x-capture-metadata-schema"] != SCHEMA:
        raise RemoteCaptureV2Error("v2 metadata schema header mismatch")
    _content_type_and_boundary(content_type)
    envelope = (
        f"MIME-Version: 1.0\r\nContent-Type: {content_type}\r\n\r\n".encode("ascii", "strict")
        + body
    )
    message = BytesParser(policy=policy.HTTP).parsebytes(envelope)
    if message.defects:
        raise RemoteCaptureV2Error("v2 multipart parser reported malformed MIME defects")
    if not message.is_multipart() or message.get_content_type() != "multipart/mixed":
        raise RemoteCaptureV2Error("v2 response is not a multipart/mixed envelope")
    parts = list(message.iter_parts())
    if len(parts) != 2:
        raise RemoteCaptureV2Error("v2 response must contain exactly two parts")
    for part in parts:
        if part.is_multipart():
            raise RemoteCaptureV2Error("nested multipart parts are not allowed")
        _part_headers_are_allowed(part)
    if parts[0].get_content_type() != "application/json" or parts[1].get_content_type() not in CR3_CONTENT_TYPES:
        raise RemoteCaptureV2Error("v2 response must contain one JSON and one CR3 part")
    _validate_part_association(parts[0], content_id="metadata", disposition="inline", name="metadata")
    _validate_part_association(parts[1], content_id="cr3", disposition="attachment", name="cr3")
    metadata_payload = parts[0].get_payload(decode=True)
    cr3_payload = parts[1].get_payload(decode=True)
    if not isinstance(metadata_payload, bytes) or not isinstance(cr3_payload, bytes) or not cr3_payload:
        raise RemoteCaptureV2Error("v2 multipart contains an empty or undecodable part")
    metadata = _json_metadata(metadata_payload)
    validate_capture_metadata(
        metadata,
        payload=cr3_payload,
        expected_capture_id=response_headers["x-capture-id"],
        expected_request_id=response_headers["x-request-id"],
    )
    return ParsedV2Multipart(
        metadata=metadata,
        cr3_bytes=cr3_payload,
        response_headers=dict(response_headers or {}),
    )


def _finite_number(value: object, name: str, *, integer: bool = False) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RemoteCaptureV2Error(f"{name} must be numeric")
    if integer:
        if not isinstance(value, int) or value < 0:
            raise RemoteCaptureV2Error(f"{name} must be a non-negative integer")
        return value
    number = float(value)
    if not math.isfinite(number):
        raise RemoteCaptureV2Error(f"{name} must be finite")
    return number


def validate_capture_metadata(
    metadata: Mapping[str, Any], *, payload: bytes,
    expected_capture_id: str | None = None, expected_request_id: str | None = None,
) -> None:
    _require_exact_keys(metadata, REMOTE_METADATA_KEYS, "remote_capture_result_v2")
    if metadata.get("schema") != SCHEMA:
        raise RemoteCaptureV2Error("v2 metadata schema mismatch")
    capture_id = metadata.get("capture_id")
    request_id = metadata.get("request_id")
    if not isinstance(capture_id, str) or not capture_id or not isinstance(request_id, str) or not request_id:
        raise RemoteCaptureV2Error("v2 metadata IDs must be non-empty strings")
    if expected_capture_id is not None and capture_id != expected_capture_id:
        raise RemoteCaptureV2Error("v2 capture ID mismatch")
    if expected_request_id is not None and request_id != expected_request_id:
        raise RemoteCaptureV2Error("v2 request ID mismatch")
    if metadata.get("timing_quality") != "best_effort_gphoto2":
        raise RemoteCaptureV2Error("v2 timing quality is unsupported")
    if metadata.get("formal_p7_eligibility") != "unchanged_requires_later_planner_advisor_decision":
        raise RemoteCaptureV2Error("v2 formal P7 eligibility marker is unsupported")
    cr3 = metadata.get("cr3")
    if not isinstance(cr3, Mapping) or cr3.get("content_type") not in CR3_CONTENT_TYPES:
        raise RemoteCaptureV2Error("v2 CR3 metadata is missing or has an unsupported content type")
    _require_exact_keys(cr3, frozenset(("sha256", "byte_count", "content_type")), "cr3")
    digest = hashlib.sha256(payload).hexdigest()
    if cr3.get("sha256") != digest or cr3.get("byte_count") != len(payload):
        raise RemoteCaptureV2Error("v2 CR3 hash or byte count mismatch")
    gphoto = metadata.get("gphoto2")
    if not isinstance(gphoto, Mapping) or gphoto.get("clock_domain") != "bridge_monotonic":
        raise RemoteCaptureV2Error("v2 gphoto timing clock domain is missing")
    _require_exact_keys(gphoto, frozenset((
        "driver_event_type", "event_sequence", "request_received_monotonic_ns",
        "capture_call_started_monotonic_ns", "capture_call_returned_monotonic_ns",
        "camera_event_observed_monotonic_ns", "file_added_observed_monotonic_ns",
        "download_started_monotonic_ns", "download_completed_monotonic_ns",
        "cr3_saved_observed_monotonic_ns", "clock_domain",
    )), "gphoto2")
    required = ("request_received_monotonic_ns", "capture_call_started_monotonic_ns", "download_completed_monotonic_ns")
    timestamps: dict[str, int] = {}
    for name in required:
        timestamps[name] = int(_finite_number(gphoto.get(name), f"gphoto2.{name}", integer=True))
    if not timestamps["request_received_monotonic_ns"] <= timestamps["capture_call_started_monotonic_ns"] <= timestamps["download_completed_monotonic_ns"]:
        raise RemoteCaptureV2Error("v2 required bridge timestamps are out of order")
    optional_names = (
        "capture_call_returned_monotonic_ns", "camera_event_observed_monotonic_ns",
        "file_added_observed_monotonic_ns", "download_started_monotonic_ns", "cr3_saved_observed_monotonic_ns",
    )
    for name in optional_names:
        value = gphoto.get(name)
        if value is not None:
            parsed = int(_finite_number(value, f"gphoto2.{name}", integer=True))
            if parsed < timestamps["capture_call_started_monotonic_ns"] or (
                name != "cr3_saved_observed_monotonic_ns" and parsed > timestamps["download_completed_monotonic_ns"]
            ):
                raise RemoteCaptureV2Error(f"v2 gphoto timestamp out of order: {name}")
    events = gphoto.get("event_sequence")
    if not isinstance(events, list):
        raise RemoteCaptureV2Error("v2 event sequence is missing")
    previous = -1
    for event in events:
        if not isinstance(event, Mapping) or event.get("clock_domain") != "bridge_monotonic":
            raise RemoteCaptureV2Error("v2 event sequence entry is malformed")
        _require_exact_keys(event, frozenset(("monotonic_ns", "clock_domain", "event_type", "source", "payload_summary")), "event_sequence entry")
        if event.get("event_type") not in {
            "capture_command_started", "capture_result_path_observed", "download_started",
            "capture_process_returned", "cr3_saved_observed", "file_added", "capture_complete",
        } or event.get("source") not in {
            "bridge_subprocess", "bridge_filesystem_observation", "gphoto2_cli_stdout",
            "gphoto2_cli_stderr", "gphoto2_event",
        }:
            raise RemoteCaptureV2Error("v2 event sequence type/source is unsupported")
        payload_summary = event.get("payload_summary")
        if not isinstance(payload_summary, Mapping) or not set(payload_summary).issubset(
            {"operation", "success", "kind", "raw_payload_included", "path_included"}
        ):
            raise RemoteCaptureV2Error("v2 event payload summary differs from frozen safe schema")
        if "operation" in payload_summary and payload_summary["operation"] != "capture_image_and_download":
            raise RemoteCaptureV2Error("v2 event operation is unsupported")
        if "kind" in payload_summary and payload_summary["kind"] not in {
            "camera_file_reported", "local_download_reported", "single_cr3_present",
        }:
            raise RemoteCaptureV2Error("v2 event kind is unsupported")
        for boolean_key in ("success", "raw_payload_included", "path_included"):
            if boolean_key in payload_summary and not isinstance(payload_summary[boolean_key], bool):
                raise RemoteCaptureV2Error(f"v2 event {boolean_key} must be boolean")
        event_ns = int(_finite_number(event.get("monotonic_ns"), "event.monotonic_ns", integer=True))
        if event_ns < previous:
            raise RemoteCaptureV2Error("v2 event sequence is not monotonic")
        previous = event_ns
    estimate = metadata.get("exposure_start_estimate")
    if not isinstance(estimate, Mapping) or estimate.get("clock_domain") != "bridge_monotonic":
        raise RemoteCaptureV2Error("v2 exposure estimate is missing its clock domain")
    _require_exact_keys(estimate, frozenset((
        "timestamp_monotonic_ns", "clock_domain", "method", "status",
        "uncertainty_ms", "uncertainty_basis",
    )), "exposure_start_estimate")
    status = estimate.get("status")
    if status not in {"estimated_not_absolute", "weak_estimate", "unavailable"}:
        raise RemoteCaptureV2Error("v2 exposure estimate status is unsupported")
    estimate_ns = estimate.get("timestamp_monotonic_ns")
    if status == "unavailable":
        if estimate_ns is not None or estimate.get("method") is not None:
            raise RemoteCaptureV2Error("unavailable timing must not contain an estimate")
    else:
        if estimate_ns is None or estimate.get("method") not in {
            "gphoto_event_minus_recorded_exposure", "gphoto_capture_return_minus_recorded_exposure"
        }:
            raise RemoteCaptureV2Error("v2 available estimate lacks a recognized method")
        estimate_int = int(_finite_number(estimate_ns, "exposure_start_estimate.timestamp_monotonic_ns", integer=True))
        if estimate_int < timestamps["capture_call_started_monotonic_ns"]:
            raise RemoteCaptureV2Error("v2 exposure estimate precedes capture start")
    exposure = metadata.get("recorded_exposure")
    if not isinstance(exposure, Mapping):
        raise RemoteCaptureV2Error("v2 recorded exposure is missing")
    _require_exact_keys(exposure, frozenset(("seconds", "source", "status")), "recorded_exposure")
    seconds = exposure.get("seconds")
    try:
        exposure_value = float(seconds) if seconds is not None and not isinstance(seconds, bool) else float("nan")
    except (TypeError, ValueError):
        exposure_value = float("nan")
    exposure_usable = (
        exposure.get("status") == "recorded"
        and exposure.get("source") in {"Canon:ExposureTime", "EXIF:ExposureTime"}
        and math.isfinite(exposure_value)
        and exposure_value > 0
    )
    if exposure.get("status") == "recorded" and not exposure_usable:
        raise RemoteCaptureV2Error("v2 recorded exposure provenance is invalid")
    if status != "unavailable" and not exposure_usable:
        raise RemoteCaptureV2Error("available v2 timing requires recorded exposure provenance")
    if status != "unavailable":
        exposure_ns = round(exposure_value * 1_000_000_000)
        method = estimate.get("method")
        expected_event = gphoto.get("file_added_observed_monotonic_ns")
        if expected_event is None and gphoto.get("camera_event_observed_monotonic_ns") is not None and gphoto.get("driver_event_type") in {"file_added", "capture_complete"}:
            expected_event = gphoto.get("camera_event_observed_monotonic_ns")
        if method == "gphoto_event_minus_recorded_exposure":
            if expected_event is None or int(estimate["timestamp_monotonic_ns"]) != int(expected_event) - exposure_ns:
                raise RemoteCaptureV2Error("v2 event timing estimate does not match recorded exposure")
        elif method == "gphoto_capture_return_minus_recorded_exposure":
            returned = gphoto.get("capture_call_returned_monotonic_ns")
            if returned is None or int(estimate["timestamp_monotonic_ns"]) != int(returned) - exposure_ns:
                raise RemoteCaptureV2Error("v2 capture-return timing estimate does not match recorded exposure")
    network = metadata.get("network_observation")
    if not isinstance(network, Mapping):
        raise RemoteCaptureV2Error("v2 network observation is missing")
    _require_exact_keys(network, frozenset((
        "request_id", "response_or_event_round_trip_ms", "uncertainty_ms", "uncertainty_basis",
    )), "network_observation")
    if network.get("request_id") != request_id:
        raise RemoteCaptureV2Error("v2 network observation request ID mismatch")
    if network.get("uncertainty_basis") != "unknown":
        raise RemoteCaptureV2Error("v2 network uncertainty basis is unsupported")
    for name in ("response_or_event_round_trip_ms", "uncertainty_ms"):
        value = network.get(name)
        if value is not None and float(_finite_number(value, f"network_observation.{name}")) < 0:
            raise RemoteCaptureV2Error(f"network_observation.{name} must be non-negative")
    bridge_utc = metadata.get("bridge_utc_observation")
    if not isinstance(bridge_utc, Mapping):
        raise RemoteCaptureV2Error("v2 bridge UTC observation is missing")
    _require_exact_keys(bridge_utc, frozenset(("request_received", "source")), "bridge_utc_observation")
    if not isinstance(bridge_utc.get("request_received"), str) or bridge_utc.get("source") != "bridge_system_clock_utc":
        raise RemoteCaptureV2Error("v2 bridge UTC observation is invalid")
    try:
        datetime.fromisoformat(bridge_utc["request_received"])
    except ValueError as exc:
        raise RemoteCaptureV2Error("v2 bridge UTC timestamp is invalid") from exc


def split_and_validate_sidecar(
    sidecar: Mapping[str, Any], *, payload: bytes,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if set(sidecar) != REMOTE_METADATA_KEYS | {"_local_receipt"}:
        raise RemoteCaptureV2Error("v2 sidecar fields differ from frozen remote-plus-local schema")
    remote = {key: sidecar[key] for key in REMOTE_METADATA_KEYS}
    validate_capture_metadata(remote, payload=payload)
    receipt = sidecar.get("_local_receipt")
    if not isinstance(receipt, Mapping):
        raise RemoteCaptureV2Error("v2 sidecar lacks local receipt")
    _require_exact_keys(receipt, LOCAL_RECEIPT_KEYS, "local receipt")
    if receipt.get("parser_version") != PARSER_VERSION:
        raise RemoteCaptureV2Error("v2 sidecar parser version mismatch")
    headers = receipt.get("response_headers")
    if not isinstance(headers, Mapping) or not REQUIRED_RESPONSE_HEADERS.issubset(headers):
        raise RemoteCaptureV2Error("v2 sidecar lacks required response headers")
    if headers.get("x-capture-id") != remote["capture_id"] or headers.get("x-request-id") != remote["request_id"]:
        raise RemoteCaptureV2Error("v2 sidecar response IDs differ from metadata")
    if headers.get("x-capture-metadata-schema") != SCHEMA:
        raise RemoteCaptureV2Error("v2 sidecar schema header mismatch")
    body_count = _finite_number(receipt.get("multipart_body_byte_count"), "local receipt multipart byte count", integer=True)
    try:
        declared = int(headers["content-length"])
    except (TypeError, ValueError) as exc:
        raise RemoteCaptureV2Error("v2 sidecar Content-Length is invalid") from exc
    if declared != body_count:
        raise RemoteCaptureV2Error("v2 sidecar Content-Length differs from received byte count")
    body_digest = receipt.get("multipart_body_sha256")
    if not isinstance(body_digest, str) or len(body_digest) != 64:
        raise RemoteCaptureV2Error("v2 sidecar multipart digest is invalid")
    attempts = _finite_number(receipt.get("http_attempts"), "local receipt http attempts", integer=True)
    successful = _finite_number(receipt.get("successful_attempt_index"), "local receipt successful attempt", integer=True)
    if attempts < 1 or successful != attempts:
        raise RemoteCaptureV2Error("v2 sidecar successful attempt index is inconsistent")
    local_start = float(_finite_number(receipt.get("local_request_started_monotonic_s"), "local receipt request start"))
    local_response = float(_finite_number(receipt.get("local_response_received_monotonic_s"), "local receipt response time"))
    received = float(_finite_number(receipt.get("received_monotonic_s"), "local receipt received time"))
    if min(local_start, local_response, received) < 0 or local_start > local_response or received != local_response:
        raise RemoteCaptureV2Error("v2 sidecar successful-attempt local clocks are inconsistent")
    if not isinstance(receipt.get("timing_evidence"), Mapping):
        raise RemoteCaptureV2Error("v2 sidecar timing evidence is missing")
    return remote, dict(receipt)


def reconstruct_best_effort_timing(
    metadata: Mapping[str, Any], *, local_request_started_monotonic_s: float,
    local_response_received_monotonic_s: float, local_readback_done_monotonic_s: float,
) -> dict[str, Any]:
    # The caller validates the CR3 association first. Re-validate local ordering and
    # recompute the relative offset without accepting any caller-provided elapsed value.
    values = (local_request_started_monotonic_s, local_response_received_monotonic_s, local_readback_done_monotonic_s)
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) for value in values):
        raise RemoteCaptureV2Error("local timing values must be finite")
    if local_readback_done_monotonic_s > local_request_started_monotonic_s or local_request_started_monotonic_s > local_response_received_monotonic_s:
        raise RemoteCaptureV2Error("local timing values are out of order")
    gphoto = metadata.get("gphoto2") if isinstance(metadata, Mapping) else None
    estimate = metadata.get("exposure_start_estimate") if isinstance(metadata, Mapping) else None
    if not isinstance(gphoto, Mapping) or not isinstance(estimate, Mapping) or gphoto.get("clock_domain") != "bridge_monotonic" or estimate.get("clock_domain") != "bridge_monotonic":
        raise RemoteCaptureV2Error("timing metadata lacks bridge monotonic provenance")
    request_ns = _finite_number(gphoto.get("request_received_monotonic_ns"), "gphoto2.request_received_monotonic_ns", integer=True)
    bridge_delay = None
    elapsed = None
    status = estimate.get("status")
    if status not in {"estimated_not_absolute", "weak_estimate", "unavailable"}:
        raise RemoteCaptureV2Error("timing metadata has an unsupported estimate status")
    tier = {"estimated_not_absolute": "tier_a", "weak_estimate": "tier_b", "unavailable": "tier_c"}[status]
    if status != "unavailable":
        estimate_ns = _finite_number(estimate.get("timestamp_monotonic_ns"), "exposure_start_estimate.timestamp_monotonic_ns", integer=True)
        bridge_delay = (int(estimate_ns) - int(request_ns)) / 1_000_000_000.0
        if bridge_delay < 0 or not math.isfinite(bridge_delay):
            raise RemoteCaptureV2Error("bridge relative timing offset is negative or non-finite")
        estimated_local = float(local_request_started_monotonic_s) + bridge_delay
        elapsed = estimated_local - float(local_readback_done_monotonic_s)
    return {
        "provenance": TIMING_PROVENANCE,
        "timing_contract": TIMING_CONTRACT,
        "tier": tier,
        "status": "accepted_best_effort_anchor" if tier in {"tier_a", "tier_b"} else "timing_evidence_unavailable",
        "local_request_started_monotonic_s": float(local_request_started_monotonic_s),
        "local_response_received_monotonic_s": float(local_response_received_monotonic_s),
        "local_round_trip_s": float(local_response_received_monotonic_s - local_request_started_monotonic_s),
        "local_readback_done_monotonic_s": float(local_readback_done_monotonic_s),
        "bridge_relative_delay_s": bridge_delay,
        "best_effort_elapsed_s": elapsed,
        "network_assumption": "wired_lan_latency_negligible_developer_decision",
        "absolute_exposure_start": False,
    }
