from __future__ import annotations

import hmac
import json
import math
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

from flask import Flask, Response, jsonify, request, send_file

from r6_timing import (
    SCHEMA,
    CaptureObservation,
    TimingMetadataError,
    append_event,
    build_capture_metadata,
)


CAMERA_MODEL = "Canon EOS R6 Mark III"
CAMERA_PORT = os.environ.get("CAMERA_PORT")
GPHOTO2_BINARY = os.environ.get("GPHOTO2_BINARY", "/usr/local/bin/gphoto2")
GPHOTO2_LIBRARY_PATH = os.environ.get("GPHOTO2_LD_LIBRARY_PATH", "/usr/local/lib")
CAPTURE_TEMP_DIR = Path(os.environ.get("CAPTURE_TEMP_DIR", "/run/r6-camera-bridge"))
CAPTURE_TIMEOUT_SECONDS = int(os.environ.get("CAPTURE_TIMEOUT_SECONDS", "120"))
TOKEN_FILE = Path(os.environ.get("CAMERA_TOKEN_FILE", "/home/ibobby/.config/r6-camera-bridge.token"))
API_DOCUMENTATION_PATH = Path(
    os.environ.get("API_DOCUMENTATION_PATH", "/home/ibobby/r6-camera-bridge/API.md")
)
CONFIG_TIMEOUT_SECONDS = int(os.environ.get("CONFIG_TIMEOUT_SECONDS", "30"))
EXIFTOOL_BINARY = os.environ.get(
    "EXIFTOOL_BINARY",
    "/home/ibobby/r6-camera-bridge/vendor/exiftool/exiftool",
)

RAW_FORMAT = "RAW"
CONFIG_FIELDS = {
    "iso": "/main/imgsettings/iso",
    "aperture": "/main/capturesettings/aperture",
    "shutter_speed": "/main/capturesettings/shutterspeed",
    "image_format": "/main/imgsettings/imageformat",
}
SETTABLE_FIELDS = frozenset(("iso", "aperture", "shutter_speed"))


class CameraCommandError(RuntimeError):
    """A gphoto2 command could not complete successfully."""


class CaptureProcessError(CameraCommandError):
    """The capture process failed after timing observation began."""


def _load_api_token() -> str:
    try:
        return TOKEN_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        token = secrets.token_urlsafe(32)
        descriptor = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as token_file:
            token_file.write(f"{token}\n")
        return token


API_TOKEN = _load_api_token()
if not API_TOKEN:
    raise RuntimeError("camera API token must not be empty")

app = Flask(__name__)
capture_lock = threading.Lock()


def _is_authorized() -> bool:
    authorization = request.headers.get("Authorization", "")
    scheme, _, supplied_token = authorization.partition(" ")
    return scheme == "Bearer" and hmac.compare_digest(supplied_token, API_TOKEN)


def _release_desktop_camera_claim() -> None:
    for process_name in ("gvfsd-gphoto2", "gvfs-gphoto2-vo"):
        subprocess.run(
            ["pkill", "-TERM", "-x", process_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def _camera_environment() -> dict[str, str]:
    environment = os.environ.copy()
    previous = environment.get("LD_LIBRARY_PATH")
    environment["LD_LIBRARY_PATH"] = (
        f"{GPHOTO2_LIBRARY_PATH}:{previous}" if previous else GPHOTO2_LIBRARY_PATH
    )
    environment["LC_ALL"] = "C"
    return environment


def _camera_command() -> list[str]:
    command = [GPHOTO2_BINARY, "--camera", CAMERA_MODEL]
    if CAMERA_PORT:
        command.extend(["--port", CAMERA_PORT])
    return command


def _run_camera_command(*arguments: str, timeout: int = CONFIG_TIMEOUT_SECONDS) -> str:
    completed = subprocess.run(
        [*_camera_command(), *arguments],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=_camera_environment(),
        check=False,
    )
    if completed.returncode != 0:
        raise CameraCommandError("gphoto2 command failed")
    return completed.stdout


def _parse_camera_config(output: str) -> dict[str, object]:
    current: str | None = None
    choices: list[str] = []
    for line in output.splitlines():
        current_match = re.match(r"^Current:\s?(.*)$", line)
        if current_match:
            current = current_match.group(1)
            continue
        choice_match = re.match(r"^Choice:\s*\d+\s+(.*)$", line)
        if choice_match:
            choices.append(choice_match.group(1))

    if current is None:
        raise CameraCommandError("gphoto2 config output was malformed")
    return {"current": current, "choices": choices}


def _read_camera_config() -> dict[str, dict[str, object]]:
    return {
        field: _parse_camera_config(_run_camera_command("--get-config", path))
        for field, path in CONFIG_FIELDS.items()
    }


def _is_bulb(value: object) -> bool:
    return isinstance(value, str) and value.strip().casefold() == "bulb"


def _set_camera_config(values: dict[str, str]) -> None:
    arguments: list[str] = []
    for field, value in values.items():
        arguments.extend(("--set-config", f"{CONFIG_FIELDS[field]}={value}"))
    _run_camera_command(*arguments)


def _camera_config_response(config: dict[str, dict[str, object]]) -> Response:
    response = jsonify(
        iso=config["iso"],
        aperture=config["aperture"],
        shutter_speed=config["shutter_speed"],
        image_format={
            "current": config["image_format"]["current"],
            "fixed": RAW_FORMAT,
        },
    )
    response.headers["Cache-Control"] = "no-store"
    return response


def _validate_settings(
    supplied: object, config: dict[str, dict[str, object]]
) -> dict[str, str] | tuple[Response, int]:
    if supplied is None:
        supplied = {}
    if not isinstance(supplied, dict):
        return _error(400, "settings_required")

    supplied_fields = set(supplied)
    if not supplied_fields.issubset(SETTABLE_FIELDS):
        return _error(400, "unknown_setting")

    requested: dict[str, str] = {}
    for field in SETTABLE_FIELDS:
        if field not in supplied:
            continue
        value = supplied[field]
        if not isinstance(value, str) or not value:
            return _error(400, f"invalid_{field}")
        if field == "shutter_speed" and _is_bulb(value):
            return _error(400, "bulb_not_allowed")
        choices = config[field]["choices"]
        if value not in choices:
            return _error(400, f"invalid_{field}")
        requested[field] = value

    current_shutter = config["shutter_speed"]["current"]
    if "shutter_speed" not in requested and _is_bulb(current_shutter):
        return _error(409, "camera_in_bulb_mode")
    return requested


def _force_raw_and_verify(
    config: dict[str, dict[str, object]], requested: dict[str, str]
) -> dict[str, dict[str, object]]:
    if RAW_FORMAT not in config["image_format"]["choices"]:
        raise CameraCommandError("camera does not expose RAW format")

    _set_camera_config({**requested, "image_format": RAW_FORMAT})
    updated = _read_camera_config()
    if updated["image_format"]["current"] != RAW_FORMAT:
        raise CameraCommandError("camera did not retain RAW format")
    for field, value in requested.items():
        if updated[field]["current"] != value:
            raise CameraCommandError("camera did not retain requested setting")
    return updated


def _classify_capture_output(line: str) -> tuple[str, dict[str, object]] | None:
    normalized = line.strip()
    if normalized.startswith("New file is in location"):
        return (
            "capture_result_path_observed",
            {"kind": "camera_file_reported", "raw_payload_included": False},
        )
    if normalized.startswith("Saving file as"):
        return (
            "download_started",
            {"kind": "local_download_reported", "raw_payload_included": False},
        )
    return None


def _observe_capture_stream(
    stream: TextIO,
    *,
    source: str,
    observation: CaptureObservation,
    observation_lock: threading.Lock,
) -> None:
    for line in stream:
        classified = _classify_capture_output(line)
        if classified is None:
            continue
        event_type, payload_summary = classified
        with observation_lock:
            observed_ns = time.monotonic_ns()
            if (
                event_type == "capture_result_path_observed"
                and observation.capture_call_returned_monotonic_ns is None
            ):
                observation.capture_call_returned_monotonic_ns = observed_ns
            elif (
                event_type == "download_started"
                and observation.download_started_monotonic_ns is None
            ):
                observation.download_started_monotonic_ns = observed_ns
            append_event(
                observation,
                monotonic_ns=observed_ns,
                event_type=event_type,
                source=source,
                payload_summary=payload_summary,
            )


def _run_timed_capture(command: list[str], request_received_ns: int) -> CaptureObservation:
    capture_started_ns = time.monotonic_ns()
    observation = CaptureObservation(
        request_received_monotonic_ns=request_received_ns,
        capture_call_started_monotonic_ns=capture_started_ns,
    )
    append_event(
        observation,
        monotonic_ns=capture_started_ns,
        event_type="capture_command_started",
        source="bridge_subprocess",
        payload_summary={"operation": "capture_image_and_download"},
    )
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=_camera_environment(),
    )
    if process.stdout is None or process.stderr is None:
        process.kill()
        raise CaptureProcessError("gphoto2 capture pipes were unavailable")

    observation_lock = threading.Lock()
    readers = [
        threading.Thread(
            target=_observe_capture_stream,
            kwargs={
                "stream": process.stdout,
                "source": "gphoto2_cli_stdout",
                "observation": observation,
                "observation_lock": observation_lock,
            },
            daemon=True,
        ),
        threading.Thread(
            target=_observe_capture_stream,
            kwargs={
                "stream": process.stderr,
                "source": "gphoto2_cli_stderr",
                "observation": observation,
                "observation_lock": observation_lock,
            },
            daemon=True,
        ),
    ]
    for reader in readers:
        reader.start()
    try:
        returncode = process.wait(timeout=CAPTURE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        raise
    finally:
        for reader in readers:
            reader.join(timeout=2)
        process.stdout.close()
        process.stderr.close()

    with observation_lock:
        completed_ns = time.monotonic_ns()
        observation.download_completed_monotonic_ns = completed_ns
        append_event(
            observation,
            monotonic_ns=completed_ns,
            event_type="capture_process_returned",
            source="bridge_subprocess",
            payload_summary={"success": returncode == 0},
        )
    if returncode != 0:
        raise CaptureProcessError("gphoto2 capture command failed")
    return observation


def _parse_exposure_seconds(value: str) -> float | None:
    normalized = value.strip()
    if not normalized:
        return None
    fraction_match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)/([0-9]+(?:\.[0-9]+)?)", normalized)
    try:
        if fraction_match:
            numerator = float(fraction_match.group(1))
            denominator = float(fraction_match.group(2))
            seconds = numerator / denominator
        else:
            seconds = float(normalized)
    except (ValueError, ZeroDivisionError):
        return None
    if not math.isfinite(seconds) or seconds <= 0:
        return None
    return seconds


def _recorded_exposure(raw_file: Path) -> dict[str, object]:
    try:
        completed = subprocess.run(
            [
                EXIFTOOL_BINARY,
                "-s3",
                "-n",
                "-Canon:ExposureTime",
                str(raw_file),
            ],
            capture_output=True,
            text=True,
            timeout=CONFIG_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"seconds": None, "source": None, "status": "unavailable"}
    if completed.returncode != 0:
        return {"seconds": None, "source": None, "status": "unavailable"}
    seconds = _parse_exposure_seconds(completed.stdout)
    if seconds is None:
        return {"seconds": None, "source": None, "status": "unavailable"}
    return {
        "seconds": seconds,
        "source": "Canon:ExposureTime",
        "status": "recorded",
    }


def _capture_payload_and_metadata(
    supplied_settings: object,
    *,
    request_received_ns: int,
    request_received_utc: str,
    request_id: str,
    capture_id: str,
) -> tuple[bytes, str, dict[str, object]] | tuple[Response, int]:
    capture_dir: Path | None = None
    try:
        CAPTURE_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        capture_dir = Path(tempfile.mkdtemp(prefix="capture-", dir=CAPTURE_TEMP_DIR))
        filename_template = str(capture_dir / "capture.%C")
        _release_desktop_camera_claim()

        config = _read_camera_config()
        requested = _validate_settings(supplied_settings, config)
        if isinstance(requested, tuple):
            return requested
        updated = _force_raw_and_verify(config, requested)
        if _is_bulb(updated["shutter_speed"]["current"]):
            return _error(409, "camera_in_bulb_mode")

        command = _camera_command()
        command.extend(["--capture-image-and-download", "--filename", filename_template])
        observation = _run_timed_capture(command, request_received_ns)
        files = sorted(path for path in capture_dir.iterdir() if path.is_file())
        if len(files) != 1 or files[0].suffix.lower() != ".cr3":
            return _error(502, "camera_capture_failed")

        raw_file = files[0]
        observation.cr3_saved_observed_monotonic_ns = time.monotonic_ns()
        append_event(
            observation,
            monotonic_ns=observation.cr3_saved_observed_monotonic_ns,
            event_type="cr3_saved_observed",
            source="bridge_filesystem_observation",
            payload_summary={"kind": "single_cr3_present", "path_included": False},
        )
        recorded_exposure = _recorded_exposure(raw_file)
        payload = raw_file.read_bytes()
        public_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        public_filename = f"r6-{public_timestamp}.cr3"
        metadata = build_capture_metadata(
            capture_id=capture_id,
            request_id=request_id,
            payload=payload,
            observation=observation,
            recorded_exposure=recorded_exposure,
            request_received_utc=request_received_utc,
        )
        shutil.rmtree(capture_dir, ignore_errors=True)
        capture_dir = None
        return payload, public_filename, metadata
    finally:
        if capture_dir is not None:
            shutil.rmtree(capture_dir, ignore_errors=True)


def _binary_capture_response(
    payload: bytes,
    *,
    filename: str,
    capture_id: str,
    request_id: str,
) -> Response:
    response = Response(payload, mimetype="application/octet-stream")
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.headers["X-Capture-ID"] = capture_id
    response.headers["X-Request-ID"] = request_id
    response.content_length = len(payload)
    return response


def _multipart_capture_response(
    payload: bytes,
    *,
    filename: str,
    metadata: dict[str, object],
    capture_id: str,
    request_id: str,
) -> Response:
    boundary = f"r6-camera-bridge-{secrets.token_hex(16)}"
    metadata_payload = json.dumps(
        metadata, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    prefix = (
        f"--{boundary}\r\n"
        "Content-Type: application/json\r\n"
        'Content-Disposition: inline; name="metadata"\r\n'
        "Content-ID: <metadata>\r\n\r\n"
    ).encode("ascii")
    middle = (
        f"\r\n--{boundary}\r\n"
        "Content-Type: image/x-canon-cr3\r\n"
        f'Content-Disposition: attachment; name="cr3"; filename="{filename}"\r\n'
        "Content-ID: <cr3>\r\n\r\n"
    ).encode("ascii")
    suffix = f"\r\n--{boundary}--\r\n".encode("ascii")
    chunks = (prefix, metadata_payload, middle, payload, suffix)
    response = Response(chunks, content_type=f"multipart/mixed; boundary={boundary}")
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Capture-ID"] = capture_id
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Capture-Metadata-Schema"] = SCHEMA
    response.content_length = sum(len(chunk) for chunk in chunks)
    return response


def _error(status: int, code: str) -> tuple[Response, int]:
    return jsonify(error=code), status


@app.get("/health")
def health() -> tuple[Response, int]:
    return jsonify(status="ok"), 200


@app.get("/v1/API.md")
def api_documentation() -> Response | tuple[Response, int]:
    try:
        response = send_file(
            API_DOCUMENTATION_PATH,
            mimetype="text/markdown; charset=utf-8",
            conditional=False,
        )
    except FileNotFoundError:
        return _error(404, "api_documentation_not_found")
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/v1/config")
def get_config() -> Response | tuple[Response, int]:
    if not _is_authorized():
        response, status = _error(401, "unauthorized")
        response.headers["WWW-Authenticate"] = "Bearer"
        return response, status
    if not capture_lock.acquire(blocking=False):
        return _error(409, "camera_busy")

    try:
        _release_desktop_camera_claim()
        return _camera_config_response(_read_camera_config())
    except subprocess.TimeoutExpired:
        return _error(504, "camera_config_timeout")
    except (CameraCommandError, OSError):
        return _error(502, "camera_config_failed")
    finally:
        capture_lock.release()


@app.post("/v1/capture")
def capture() -> Response | tuple[Response, int]:
    return _capture_response(version=1)


@app.post("/v2/capture")
def capture_v2() -> Response | tuple[Response, int]:
    return _capture_response(version=2)


def _capture_response(*, version: int) -> Response | tuple[Response, int]:
    request_received_ns = time.monotonic_ns()
    request_received_utc = datetime.now(timezone.utc).isoformat()
    request_id = str(uuid.uuid4())
    capture_id = str(uuid.uuid4())
    if not _is_authorized():
        response, status = _error(401, "unauthorized")
        response.headers["WWW-Authenticate"] = "Bearer"
        return response, status

    if not capture_lock.acquire(blocking=False):
        return _error(409, "camera_busy")

    try:
        result = _capture_payload_and_metadata(
            request.get_json(silent=True),
            request_received_ns=request_received_ns,
            request_received_utc=request_received_utc,
            request_id=request_id,
            capture_id=capture_id,
        )
        if len(result) == 2:
            return result
        payload, filename, metadata = result
        if version == 1:
            return _binary_capture_response(
                payload,
                filename=filename,
                capture_id=capture_id,
                request_id=request_id,
            )
        return _multipart_capture_response(
            payload,
            filename=filename,
            metadata=metadata,
            capture_id=capture_id,
            request_id=request_id,
        )
    except subprocess.TimeoutExpired:
        return _error(504, "camera_capture_timeout")
    except TimingMetadataError:
        return _error(500, "capture_metadata_invalid")
    except (CameraCommandError, OSError):
        return _error(500, "camera_capture_internal_error")
    finally:
        capture_lock.release()
