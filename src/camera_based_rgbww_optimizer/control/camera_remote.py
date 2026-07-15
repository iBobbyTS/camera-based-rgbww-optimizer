from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Callable, Mapping, Sequence
from urllib import error, parse, request

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


DEFAULT_BASE_URL = "http://ibobby-rpi-4.local:8088"
DEFAULT_CAPTURE_PATH = "/v1/capture"
DEFAULT_CONFIG_PATH = "/v1/config"
DEFAULT_HEALTH_PATH = "/health"
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_FILENAME_TEMPLATE = "%Y%m%d-%H%M%S.%C"
DEFAULT_TIMEOUT = 120.0
BASE_URL_ENV = "CAMERA_BASED_RGBWW_OPTIMIZER_REMOTE_CAMERA_BASE_URL"
TOKEN_ENV = "CAMERA_BASED_RGBWW_OPTIMIZER_REMOTE_CAMERA_TOKEN"
REMOTE_CAMERA_MODEL = "Canon EOS R6 Mark III via r6-camera-bridge"
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
DEFAULT_BUSY_RETRIES = 3
DEFAULT_BUSY_RETRY_DELAY = 0.5


class RemoteCameraError(RuntimeError):
    pass


class RemoteCameraHTTPError(RemoteCameraError):
    def __init__(self, status: int, error_code: str | None = None):
        self.status = int(status)
        self.error_code = error_code
        suffix = f" ({error_code})" if error_code else ""
        super().__init__(f"remote camera HTTP request failed with status {status}{suffix}")


@dataclass(frozen=True)
class RemoteCameraConfig:
    base_url: str
    token: str

    @property
    def capture_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{DEFAULT_CAPTURE_PATH}"

    @property
    def camera_config_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{DEFAULT_CONFIG_PATH}"

    @property
    def health_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{DEFAULT_HEALTH_PATH}"


@dataclass(frozen=True)
class RemoteCameraSetting:
    current: str
    choices: tuple[str, ...]


@dataclass(frozen=True)
class RemoteCameraSettings:
    iso: RemoteCameraSetting
    aperture: RemoteCameraSetting
    shutter_speed: RemoteCameraSetting
    image_format: str


@dataclass(frozen=True)
class RemoteCaptureResult:
    saved_file: Path
    byte_count: int
    endpoint: str
    http_attempts: int

    def to_jsonable(self) -> dict[str, object]:
        return {
            "backend": "remote",
            "model": REMOTE_CAMERA_MODEL,
            "endpoint": self.endpoint,
            "saved_file": str(self.saved_file),
            "byte_count": self.byte_count,
            "http_attempts": self.http_attempts,
        }


UrlOpen = Callable[..., BinaryIO]
SleepFn = Callable[[float], None]


def create_camera_backend(
    name: str,
    *,
    env_file: str | Path = DEFAULT_ENV_FILE,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> camera_gphoto2.CameraBackend:
    if name == "local":
        return camera_gphoto2.LocalCameraBackend(timeout=timeout)
    if name == "remote":
        return RemoteCameraBackend.from_environment(env_file=env_file, base_url=base_url, timeout=timeout)
    raise ValueError(f"unsupported camera backend: {name}")


def capture_with_backend(
    backend: camera_gphoto2.CameraBackend,
    *,
    output_dir: str | Path,
    filename_template: str,
    settings: camera_gphoto2.CaptureSettings,
) -> camera_gphoto2.CaptureResult:
    connection = backend.connect()
    resolved = backend.resolve_capture_settings(
        iso=settings.iso or None,
        aperture=settings.aperture or None,
        image_format=settings.image_format,
    )
    return backend.capture(
        output_dir=output_dir,
        filename_template=filename_template,
        settings=camera_gphoto2.CaptureSettings(
            iso=resolved.iso,
            aperture=resolved.aperture,
            shutter_speed=settings.shutter_speed,
            image_format=resolved.image_format,
        ),
        connection=connection,
        allow_bulb=False,
    )


def add_camera_backend_arguments(parser: argparse.ArgumentParser, *, default: str = "remote") -> None:
    parser.add_argument("--camera-backend", choices=("local", "remote"), default=default)
    parser.add_argument("--remote-env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--remote-base-url")
    parser.add_argument("--remote-timeout", type=float, default=DEFAULT_TIMEOUT)


def load_remote_camera_config(
    *,
    env_file: str | Path = DEFAULT_ENV_FILE,
    environ: Mapping[str, str] | None = None,
    base_url: str | None = None,
    token: str | None = None,
) -> RemoteCameraConfig:
    file_values = _read_env_file(Path(env_file))
    process_values = os.environ if environ is None else environ
    resolved_base_url = base_url or process_values.get(BASE_URL_ENV) or file_values.get(BASE_URL_ENV) or DEFAULT_BASE_URL
    resolved_token = token or process_values.get(TOKEN_ENV) or file_values.get(TOKEN_ENV)

    if not resolved_token or not resolved_token.strip():
        raise RemoteCameraError(
            f"remote camera token is missing; set {TOKEN_ENV} in the process environment or {env_file}"
        )
    normalized_base_url = _validate_base_url(resolved_base_url)
    return RemoteCameraConfig(base_url=normalized_base_url, token=resolved_token.strip())


def load_remote_camera_base_url(
    *,
    env_file: str | Path = DEFAULT_ENV_FILE,
    environ: Mapping[str, str] | None = None,
    base_url: str | None = None,
) -> str:
    """Resolve only the bridge URL for the unauthenticated health request."""

    file_values = _read_env_file(Path(env_file))
    process_values = os.environ if environ is None else environ
    return _validate_base_url(base_url or process_values.get(BASE_URL_ENV) or file_values.get(BASE_URL_ENV) or DEFAULT_BASE_URL)


def read_remote_health(
    *,
    base_url: str,
    timeout: float = DEFAULT_TIMEOUT,
    opener: UrlOpen = request.urlopen,
) -> Mapping[str, object]:
    if timeout <= 0:
        raise RemoteCameraError("timeout must be positive")
    health_url = f"{base_url.rstrip('/')}{DEFAULT_HEALTH_PATH}"
    health_request = request.Request(health_url, method="GET", headers={"Accept": "application/json"})
    try:
        with opener(health_request, timeout=timeout) as response:
            raw_payload = response.read()
    except error.HTTPError as exc:
        raise RemoteCameraHTTPError(exc.code, _read_error_code(exc)) from exc
    except error.URLError as exc:
        raise RemoteCameraError("remote camera request failed") from exc
    except TimeoutError as exc:
        raise RemoteCameraError("remote camera request timed out") from exc
    try:
        payload = json.loads(raw_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RemoteCameraError("remote camera health returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RemoteCameraError("remote camera health must be a JSON object")
    return payload


def capture_remote_image(
    *,
    output_dir: str | Path,
    filename_template: str = DEFAULT_FILENAME_TEMPLATE,
    config: RemoteCameraConfig | None = None,
    env_file: str | Path = DEFAULT_ENV_FILE,
    base_url: str | None = None,
    token: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    opener: UrlOpen = request.urlopen,
    settings: camera_gphoto2.CaptureSettings | None = None,
    busy_retries: int = DEFAULT_BUSY_RETRIES,
    busy_retry_delay: float = DEFAULT_BUSY_RETRY_DELAY,
    sleep_fn: SleepFn = time.sleep,
    now: datetime | None = None,
) -> RemoteCaptureResult:
    if timeout <= 0:
        raise RemoteCameraError("timeout must be positive")
    resolved_config = config or load_remote_camera_config(
        env_file=env_file,
        base_url=base_url,
        token=token,
    )
    destination = _resolve_destination(output_dir, filename_template, now=now)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = _capture_payload(settings)
    capture_request = request.Request(
        resolved_config.capture_url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {resolved_config.token}",
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
        },
    )

    temporary_path: Path | None = None
    byte_count = 0
    http_attempts = 0

    def counted_opener(*args: object, **kwargs: object) -> BinaryIO:
        nonlocal http_attempts
        http_attempts += 1
        return opener(*args, **kwargs)

    try:
        with _open_authenticated_request(
            capture_request,
            opener=counted_opener,
            timeout=timeout,
            busy_retries=busy_retries,
            busy_retry_delay=busy_retry_delay,
            sleep_fn=sleep_fn,
        ) as response:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=f".{destination.name}.",
                suffix=".part",
                dir=destination.parent,
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                while True:
                    chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                    if not chunk:
                        break
                    temporary.write(chunk)
                    byte_count += len(chunk)
                temporary.flush()
                os.fsync(temporary.fileno())
        if byte_count == 0:
            raise RemoteCameraError("remote camera returned an empty capture")
        os.replace(temporary_path, destination)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return RemoteCaptureResult(
        saved_file=destination,
        byte_count=byte_count,
        endpoint=resolved_config.capture_url,
        http_attempts=http_attempts,
    )


def read_remote_camera_settings(
    *,
    config: RemoteCameraConfig | None = None,
    env_file: str | Path = DEFAULT_ENV_FILE,
    base_url: str | None = None,
    token: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    opener: UrlOpen = request.urlopen,
    busy_retries: int = DEFAULT_BUSY_RETRIES,
    busy_retry_delay: float = DEFAULT_BUSY_RETRY_DELAY,
    sleep_fn: SleepFn = time.sleep,
) -> RemoteCameraSettings:
    if timeout <= 0:
        raise RemoteCameraError("timeout must be positive")
    resolved_config = config or load_remote_camera_config(
        env_file=env_file,
        base_url=base_url,
        token=token,
    )
    config_request = request.Request(
        resolved_config.camera_config_url,
        method="GET",
        headers={
            "Authorization": f"Bearer {resolved_config.token}",
            "Accept": "application/json",
        },
    )
    with _open_authenticated_request(
        config_request,
        opener=opener,
        timeout=timeout,
        busy_retries=busy_retries,
        busy_retry_delay=busy_retry_delay,
        sleep_fn=sleep_fn,
    ) as response:
        raw_payload = response.read()
    try:
        payload = json.loads(raw_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RemoteCameraError("remote camera config returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RemoteCameraError("remote camera config must be a JSON object")
    return RemoteCameraSettings(
        iso=_parse_setting(payload, "iso"),
        aperture=_parse_setting(payload, "aperture"),
        shutter_speed=_parse_setting(payload, "shutter_speed"),
        image_format=_parse_image_format(payload),
    )


@dataclass
class RemoteCameraBackend:
    config: RemoteCameraConfig
    timeout: float = DEFAULT_TIMEOUT
    opener: UrlOpen = request.urlopen
    busy_retries: int = DEFAULT_BUSY_RETRIES
    busy_retry_delay: float = DEFAULT_BUSY_RETRY_DELAY
    sleep_fn: SleepFn = time.sleep
    _camera_settings: RemoteCameraSettings | None = None

    @classmethod
    def from_environment(
        cls,
        *,
        env_file: str | Path = DEFAULT_ENV_FILE,
        base_url: str | None = None,
        token: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> "RemoteCameraBackend":
        return cls(
            config=load_remote_camera_config(env_file=env_file, base_url=base_url, token=token),
            timeout=timeout,
        )

    def connect(self) -> camera_gphoto2.CameraConnection:
        self._load_settings(refresh=True)
        return camera_gphoto2.CameraConnection(model=REMOTE_CAMERA_MODEL, port=self.config.base_url)

    def resolve_capture_settings(
        self,
        *,
        iso: str | None,
        aperture: str | None,
        image_format: str,
    ) -> camera_gphoto2.CaptureSettings:
        remote = self._load_settings()
        if image_format.upper() != "RAW" or remote.image_format.upper() != "RAW":
            raise RemoteCameraError("remote camera backend requires RAW image format")
        return camera_gphoto2.CaptureSettings(
            iso=_resolve_setting("iso", iso, remote.iso),
            aperture=_resolve_setting("aperture", aperture, remote.aperture),
            shutter_speed=remote.shutter_speed.current,
            image_format="RAW",
        )

    def read_shutter_current_and_choices(
        self,
        _connection: camera_gphoto2.CameraConnection,
    ) -> tuple[str, list[str]]:
        setting = self._load_settings().shutter_speed
        return setting.current, list(setting.choices)

    def read_current_shutter(self, _connection: camera_gphoto2.CameraConnection) -> str:
        return self._load_settings().shutter_speed.current

    def capture(
        self,
        *,
        output_dir: str | Path,
        filename_template: str,
        settings: camera_gphoto2.CaptureSettings,
        connection: camera_gphoto2.CameraConnection,
        allow_bulb: bool,
    ) -> camera_gphoto2.CaptureResult:
        if allow_bulb or settings.shutter_speed.strip().lower() == "bulb":
            raise RemoteCameraError("remote camera backend does not allow bulb capture")
        remote_result = capture_remote_image(
            output_dir=output_dir,
            filename_template=filename_template,
            config=self.config,
            timeout=self.timeout,
            opener=self.opener,
            settings=settings,
            busy_retries=self.busy_retries,
            busy_retry_delay=self.busy_retry_delay,
            sleep_fn=self.sleep_fn,
        )
        return camera_gphoto2.CaptureResult(
            connection=connection,
            settings=settings,
            saved_file=remote_result.saved_file,
            stdout=json.dumps(remote_result.to_jsonable(), sort_keys=True),
            backend="remote",
            endpoint=DEFAULT_CAPTURE_PATH,
            http_attempts=remote_result.http_attempts,
        )

    def _load_settings(self, *, refresh: bool = False) -> RemoteCameraSettings:
        if self._camera_settings is None or refresh:
            self._camera_settings = read_remote_camera_settings(
                config=self.config,
                timeout=self.timeout,
                opener=self.opener,
                busy_retries=self.busy_retries,
                busy_retry_delay=self.busy_retry_delay,
                sleep_fn=self.sleep_fn,
            )
        return self._camera_settings


def _capture_payload(settings: camera_gphoto2.CaptureSettings | None) -> dict[str, str]:
    if settings is None:
        return {}
    if settings.image_format.upper() != "RAW":
        raise RemoteCameraError("remote camera capture only supports RAW image format")
    if settings.shutter_speed.strip().lower() == "bulb":
        raise RemoteCameraError("remote camera capture does not allow bulb shutter speed")
    return {
        "iso": settings.iso,
        "aperture": settings.aperture,
        "shutter_speed": settings.shutter_speed,
    }


def _open_authenticated_request(
    authenticated_request: request.Request,
    *,
    opener: UrlOpen,
    timeout: float,
    busy_retries: int,
    busy_retry_delay: float,
    sleep_fn: SleepFn,
) -> BinaryIO:
    if busy_retries < 0:
        raise RemoteCameraError("busy_retries must be non-negative")
    if busy_retry_delay < 0:
        raise RemoteCameraError("busy_retry_delay must be non-negative")
    for attempt in range(busy_retries + 1):
        try:
            return opener(authenticated_request, timeout=timeout)
        except error.HTTPError as exc:
            error_code = _read_error_code(exc)
            if exc.code == 409 and error_code == "camera_busy" and attempt < busy_retries:
                sleep_fn(busy_retry_delay)
                continue
            raise RemoteCameraHTTPError(exc.code, error_code) from exc
        except error.URLError as exc:
            raise RemoteCameraError("remote camera request failed") from exc
        except TimeoutError as exc:
            raise RemoteCameraError("remote camera request timed out") from exc
    raise AssertionError("remote request retry loop exited unexpectedly")


def _read_error_code(exc: error.HTTPError) -> str | None:
    try:
        payload = json.loads(exc.read().decode("utf-8"))
    except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("error"), str):
        return None
    return payload["error"]


def _parse_setting(payload: dict[str, object], name: str) -> RemoteCameraSetting:
    raw_setting = payload.get(name)
    if not isinstance(raw_setting, dict):
        raise RemoteCameraError(f"remote camera config is missing {name}")
    current = raw_setting.get("current")
    choices = raw_setting.get("choices")
    if not isinstance(current, str) or not isinstance(choices, list) or not choices:
        raise RemoteCameraError(f"remote camera config has invalid {name}")
    if not all(isinstance(choice, str) for choice in choices):
        raise RemoteCameraError(f"remote camera config has invalid {name} choices")
    return RemoteCameraSetting(current=current, choices=tuple(choices))


def _parse_image_format(payload: dict[str, object]) -> str:
    raw_format = payload.get("image_format")
    if not isinstance(raw_format, dict):
        raise RemoteCameraError("remote camera config is missing image_format")
    value = raw_format.get("current") or raw_format.get("fixed")
    if not isinstance(value, str):
        raise RemoteCameraError("remote camera config has invalid image_format")
    return value


def _resolve_setting(name: str, requested: str | None, setting: RemoteCameraSetting) -> str:
    value = setting.current if requested is None else requested
    if value not in setting.choices:
        choices = ", ".join(setting.choices)
        raise RemoteCameraError(f"remote camera {name} {value!r} is unavailable; choices: {choices}")
    return value


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[7:].lstrip()
        key, separator, value = stripped.partition("=")
        if not separator or not key.strip():
            raise RemoteCameraError(f"invalid environment entry at {path}:{line_number}")
        normalized_value = value.strip()
        if len(normalized_value) >= 2 and normalized_value[0] == normalized_value[-1] and normalized_value[0] in "\"'":
            normalized_value = normalized_value[1:-1]
        values[key.strip()] = normalized_value
    return values


def _validate_base_url(value: str) -> str:
    normalized = value.strip().rstrip("/")
    parsed = parse.urlsplit(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RemoteCameraError(f"remote camera base URL must be an absolute HTTP(S) URL: {value}")
    if parsed.query or parsed.fragment:
        raise RemoteCameraError("remote camera base URL must not contain a query or fragment")
    return normalized


def _resolve_destination(output_dir: str | Path, filename_template: str, *, now: datetime | None) -> Path:
    expanded = (now or datetime.now()).strftime(filename_template.replace("%C", "cr3"))
    relative = Path(expanded)
    if relative.is_absolute() or ".." in relative.parts:
        raise RemoteCameraError("filename template must resolve inside output_dir")
    if not relative.name:
        raise RemoteCameraError("filename template must resolve to a filename")
    return Path(output_dir) / relative


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect or capture through r6-camera-bridge.")
    parser.add_argument("command", nargs="?", choices=("capture", "health", "config"), default="capture")
    parser.add_argument("--output-dir", default="captures/camera")
    parser.add_argument("--filename-template", default=DEFAULT_FILENAME_TEMPLATE)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--base-url", help=f"Override {BASE_URL_ENV}.")
    parser.add_argument("--iso", help="Exact ISO value from GET /v1/config; defaults to the current remote value.")
    parser.add_argument("--aperture", help="Exact aperture value from GET /v1/config; defaults to the current remote value.")
    parser.add_argument("--shutter-speed", help="Exact shutter value from GET /v1/config; defaults to the current remote value.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    backend: RemoteCameraBackend | None = None
    try:
        if args.command == "health":
            base_url = load_remote_camera_base_url(env_file=args.env_file, base_url=args.base_url)
            payload = read_remote_health(base_url=base_url, timeout=args.timeout)
            result = {"backend": "remote", "base_url": base_url, "service": dict(payload)}
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) if args.json else result)
            return 0
        backend = RemoteCameraBackend.from_environment(
            env_file=args.env_file,
            base_url=args.base_url,
            timeout=args.timeout,
        )
        connection = backend.connect()
        if args.command == "config":
            settings = backend._load_settings()
            result = {
                "backend": "remote",
                "base_url": backend.config.base_url,
                "model": connection.model,
                "iso": settings.iso.current,
                "aperture": settings.aperture.current,
                "shutter_speed": settings.shutter_speed.current,
                "image_format": settings.image_format,
                "choice_counts": {
                    "iso": len(settings.iso.choices),
                    "aperture": len(settings.aperture.choices),
                    "shutter_speed": len(settings.shutter_speed.choices),
                },
            }
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) if args.json else result)
            return 0
        base_settings = backend.resolve_capture_settings(
            iso=args.iso,
            aperture=args.aperture,
            image_format="RAW",
        )
        current_shutter, shutter_choices = backend.read_shutter_current_and_choices(connection)
        shutter_speed = args.shutter_speed or current_shutter
        if shutter_speed not in shutter_choices:
            raise RemoteCameraError(
                f"remote camera shutter_speed {shutter_speed!r} is unavailable; choices: {', '.join(shutter_choices)}"
            )
        result = backend.capture(
            output_dir=args.output_dir,
            filename_template=args.filename_template,
            settings=camera_gphoto2.CaptureSettings(
                iso=base_settings.iso,
                aperture=base_settings.aperture,
                shutter_speed=shutter_speed,
                image_format="RAW",
            ),
            connection=connection,
            allow_bulb=False,
        )
        print(json.dumps(result.to_jsonable(), ensure_ascii=False, indent=2, sort_keys=True))
    except Exception as exc:
        message = str(exc)
        if backend is not None and backend.config.token:
            message = message.replace(backend.config.token, "[REDACTED]")
        print(f"camera_remote: {message}", file=sys.stderr)
        return _error_exit_code(exc)
    return 0


def _error_exit_code(exc: BaseException) -> int:
    if isinstance(exc, RemoteCameraHTTPError):
        return {401: 2, 409: 3, 502: 4, 504: 5}.get(exc.status, 1)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
