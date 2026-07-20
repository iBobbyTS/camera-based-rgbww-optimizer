from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_remote, camera_remote_v2
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


DEFAULT_OUTPUT = Path("/Volumes/4T/temp/rgbww-optimizer/p7-local-v2-timing-offline")


class _FakeResponse:
    def __init__(self, body: bytes, headers: Mapping[str, str]) -> None:
        self._body = body
        self._read = False
        self.status = 200
        self.headers = dict(headers)

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, _exc_type: object, _exc: object, _traceback: object) -> None:
        return None

    def read(self, _size: int | None = None) -> bytes:
        if self._read:
            return b""
        self._read = True
        return self._body


def _metadata(payload: bytes) -> dict[str, Any]:
    return {
        "schema": camera_remote_v2.SCHEMA,
        "capture_id": "offline-r0c-capture",
        "request_id": "offline-r0c-request",
        "timing_quality": "best_effort_gphoto2",
        "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
        "cr3": {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
            "content_type": "image/x-canon-cr3",
        },
        "gphoto2": {
            "driver_event_type": None,
            "event_sequence": [],
            "request_received_monotonic_ns": 1_000_000_000,
            "capture_call_started_monotonic_ns": 1_100_000_000,
            "capture_call_returned_monotonic_ns": 2_000_000_000,
            "camera_event_observed_monotonic_ns": None,
            "file_added_observed_monotonic_ns": None,
            "download_started_monotonic_ns": 2_100_000_000,
            "download_completed_monotonic_ns": 3_000_000_000,
            "cr3_saved_observed_monotonic_ns": 3_010_000_000,
            "clock_domain": "bridge_monotonic",
        },
        "recorded_exposure": {
            "seconds": 0.25,
            "source": "Canon:ExposureTime",
            "status": "recorded",
        },
        "exposure_start_estimate": {
            "timestamp_monotonic_ns": 1_750_000_000,
            "clock_domain": "bridge_monotonic",
            "method": "gphoto_capture_return_minus_recorded_exposure",
            "status": "weak_estimate",
            "uncertainty_ms": None,
            "uncertainty_basis": "unknown",
        },
        "network_observation": {
            "request_id": "offline-r0c-request",
            "response_or_event_round_trip_ms": None,
            "uncertainty_ms": None,
            "uncertainty_basis": "unknown",
        },
        "bridge_utc_observation": {
            "request_received": "2026-07-20T00:00:00+00:00",
            "source": "bridge_system_clock_utc",
        },
    }


def _multipart(metadata: Mapping[str, Any], payload: bytes, boundary: str = "p7-lv2-r0c") -> tuple[bytes, dict[str, str]]:
    body = (
        f"--{boundary}\r\nContent-Type: application/json\r\n"
        'Content-Disposition: inline; name="metadata"\r\nContent-ID: <metadata>\r\n\r\n'.encode("ascii")
        + json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8")
        + f"\r\n--{boundary}\r\nContent-Type: image/x-canon-cr3\r\n"
        'Content-Disposition: attachment; name="cr3"; filename="offline.CR3"\r\n'
        "Content-ID: <cr3>\r\n\r\n".encode("ascii")
        + payload
        + f"\r\n--{boundary}--\r\n".encode("ascii")
    )
    headers = {
        "Content-Type": f"multipart/mixed; boundary={boundary}",
        "Content-Length": str(len(body)),
        "X-Capture-ID": str(metadata["capture_id"]),
        "X-Request-ID": str(metadata["request_id"]),
        "X-Capture-Metadata-Schema": camera_remote_v2.SCHEMA,
    }
    return body, headers


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expect_rejection(name: str, operation: Callable[[], object]) -> dict[str, Any]:
    try:
        operation()
    except Exception as exc:
        return {
            "name": name,
            "expected": "reject",
            "actual": "reject",
            "exception": type(exc).__name__,
            "message": str(exc),
        }
    return {"name": name, "expected": "reject", "actual": "accepted_unexpectedly"}


def generate_validation_artifacts(output_dir: str | Path, run_name: str) -> Path:
    root = Path(output_dir) / run_name
    root.mkdir(parents=True, exist_ok=False)
    valid_dir = root / "valid-v2-response-fixture"
    malformed_dir = root / "malformed-response-fixtures"
    valid_dir.mkdir()
    malformed_dir.mkdir()
    payload = b"offline-fake-cr3-bytes-r0c"
    metadata = _metadata(payload)
    body, headers = _multipart(metadata, payload)
    _write_json(root / "plan.json", {
        "schema": "p7_local_v2_timing_offline_validation_v1",
        "status": "offline_only",
        "timing_contract": camera_remote_v2.TIMING_CONTRACT,
        "device_calls": 0,
        "network_calls": 0,
        "env_calls": 0,
        "all_off_calls": 0,
    })
    (valid_dir / "response-body.bin").write_bytes(body)
    _write_json(valid_dir / "response-headers.json", headers)
    _write_json(valid_dir / "remote-metadata.json", metadata)
    (valid_dir / "fake-input.CR3").write_bytes(payload)

    result = camera_remote.capture_remote_image_v2(
        output_dir=valid_dir,
        filename_template="production-roundtrip.CR3",
        config=camera_remote.RemoteCameraConfig("http://offline.invalid", "offline-token"),
        opener=lambda *_args, **_kwargs: _FakeResponse(body, headers),
        local_readback_done_monotonic_s=9.0,
        monotonic_fn=iter((10.0, 12.0)).__next__,
    )
    replayed = analyze_p7_thermal_diagnostics._replay_timing_evidence(
        {},
        {
            "remote_metadata_path": str(result.metadata_path),
            "timing_metadata": dict(result.metadata),
        },
        result.saved_file,
        valid_dir,
    )
    _write_json(root / "timing-reconstruction.json", replayed)
    _write_json(root / "production-roundtrip-analysis.json", {
        "status": "pass",
        "client": "capture_remote_image_v2",
        "analyzer": "analyze_p7_thermal_diagnostics._replay_timing_evidence",
        "tier": replayed["tier"],
        "timing_absolute_truth": False,
        "cr3_sha256": _sha256(result.saved_file),
        "sidecar_sha256": _sha256(result.metadata_path),
    })

    normalized_headers = {key.lower(): value for key, value in headers.items()}
    response_cases: list[tuple[str, Callable[[], object]]] = []
    for header in ("content-length", "x-capture-id", "x-request-id", "x-capture-metadata-schema"):
        altered = dict(normalized_headers)
        altered.pop(header)
        response_cases.append((f"missing_{header}", lambda altered=altered: camera_remote_v2.parse_v2_multipart(
            content_type=altered.get("content-type"), body=body, response_headers=altered,
        )))
    bad_network = deepcopy(metadata)
    bad_network["network_observation"]["request_id"] = "forged"
    bad_network_body, bad_network_headers = _multipart(bad_network, payload)
    response_cases.append(("network_request_id_mismatch", lambda: camera_remote_v2.parse_v2_multipart(
        content_type=bad_network_headers["Content-Type"], body=bad_network_body,
        response_headers={key.lower(): value for key, value in bad_network_headers.items()},
    )))
    unknown = deepcopy(metadata)
    unknown["remote_camera_serial"] = "must-not-persist"
    unknown_body, unknown_headers = _multipart(unknown, payload)
    response_cases.append(("unknown_sensitive_metadata", lambda: camera_remote_v2.parse_v2_multipart(
        content_type=unknown_headers["Content-Type"], body=unknown_body,
        response_headers={key.lower(): value for key, value in unknown_headers.items()},
    )))
    wrong_part = body.replace(b"Content-ID: <metadata>", b"Content-ID: <cr3>", 1)
    wrong_part_headers = dict(normalized_headers)
    wrong_part_headers["content-length"] = str(len(wrong_part))
    response_cases.append(("part_content_id_mismatch", lambda: camera_remote_v2.parse_v2_multipart(
        content_type=wrong_part_headers["content-type"], body=wrong_part, response_headers=wrong_part_headers,
    )))

    results = []
    for name, operation in response_cases:
        item = _expect_rejection(name, operation)
        results.append(item)
        _write_json(malformed_dir / f"{name}.json", item)

    sidecar = json.loads(result.metadata_path.read_text(encoding="utf-8"))
    sidecar_cases = {
        "parser_version": lambda value: value["_local_receipt"].__setitem__("parser_version", "forged"),
        "header_capture_id": lambda value: value["_local_receipt"]["response_headers"].__setitem__("x-capture-id", "forged"),
        "schema_header": lambda value: value["_local_receipt"]["response_headers"].__setitem__("x-capture-metadata-schema", "forged"),
        "successful_attempt_index": lambda value: value["_local_receipt"].__setitem__("successful_attempt_index", 2),
        "successful_attempt_start": lambda value: value["_local_receipt"].__setitem__("local_request_started_monotonic_s", -1.0),
    }
    for name, mutation in sidecar_cases.items():
        altered = deepcopy(sidecar)
        mutation(altered)
        item = _expect_rejection(name, lambda altered=altered: camera_remote_v2.split_and_validate_sidecar(
            altered, payload=result.saved_file.read_bytes(),
        ))
        results.append(item)
        _write_json(malformed_dir / f"{name}.json", item)

    revision = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=PROJECT_ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    input_paths = (
        PROJECT_ROOT / "src/camera_based_rgbww_optimizer/control/camera_remote.py",
        PROJECT_ROOT / "src/camera_based_rgbww_optimizer/control/camera_remote_v2.py",
        PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
        PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py",
    )
    artifacts = {
        str(path.relative_to(root)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != "validation-summary.json"
    }
    _write_json(root / "validation-summary.json", {
        "schema": "p7_local_v2_timing_validation_summary_v1",
        "status": "pass" if all(item["actual"] == "reject" for item in results) else "fail",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_git_head_before_r0c_commit": revision,
        "input_sha256": {str(path.relative_to(PROJECT_ROOT)): _sha256(path) for path in input_paths},
        "negative_fixtures": results,
        "test_commands": [
            "python -m unittest tests.test_camera_remote tests.test_measure_raw_observer_validation tests.test_p7_thermal_diagnostics tests.test_analyze_p7_thermal_diagnostics -v",
            "python -m unittest discover -s tests -v",
        ],
        "counters": {"device": 0, "network": 0, "env": 0, "all_off": 0},
        "artifact_sha256": artifacts,
    })
    return root


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate fake-only P7 local v2 timing validation evidence.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    print(generate_validation_artifacts(args.output_dir, args.run_name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
