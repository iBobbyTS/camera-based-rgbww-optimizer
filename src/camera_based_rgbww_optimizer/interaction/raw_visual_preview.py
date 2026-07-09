from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2


DCRAW_WHITE_BALANCE_CHOICES = ("auto", "camera", "default")
VISUAL_PREVIEW_SOURCE_CHOICES = ("camera-jpeg", "dcraw")


def decode_embedded_jpeg_preview(
    raw_file: str | Path,
    *,
    output_dir: str | Path,
    output_stem: str = "visual-preview",
    executable: str = "exiftool",
    timeout: float = 90.0,
) -> camera_gphoto2.DecodeResult:
    source_path = Path(raw_file)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_file = target_dir / f"{output_stem}.jpg"
    metadata_file = target_dir / f"{output_stem}.json"

    last_error = ""
    for tag in ("JpgFromRaw", "PreviewImage"):
        command = [executable, "-b", f"-{tag}", str(source_path)]
        completed = subprocess.run(
            command,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode == 0 and completed.stdout:
            output_file.write_bytes(completed.stdout)
            image = read_jpeg(output_file)
            np = _import_numpy()
            stats = {
                "source_file": str(source_path),
                "image": _array_stats(np, image),
                "postprocess_params": {
                    "decoder": executable,
                    "preview_source": "camera-jpeg",
                    "embedded_tag": tag,
                    "output_format": "jpeg",
                },
                "command": command,
                "stdout_bytes": len(completed.stdout),
                "stderr": _decode_process_text(completed.stderr),
            }
            metadata_file.write_text(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            return camera_gphoto2.DecodeResult(
                source_file=source_path,
                output_files=(output_file, metadata_file),
                metadata_file=metadata_file,
                image_shape=tuple(int(value) for value in image.shape),
                image_dtype=str(image.dtype),
                stats=stats,
            )
        last_error = _decode_process_text(completed.stderr) or _decode_process_text(completed.stdout)

    raise RuntimeError(f"{executable} did not extract an embedded camera JPEG preview: {last_error}".strip())


def decode_dcraw_preview(
    raw_file: str | Path,
    *,
    output_dir: str | Path,
    output_stem: str = "visual-preview",
    executable: str = "dcraw_emu",
    white_balance: str = "camera",
    timeout: float = 90.0,
) -> camera_gphoto2.DecodeResult:
    if white_balance not in DCRAW_WHITE_BALANCE_CHOICES:
        raise ValueError(f"unsupported dcraw white balance mode: {white_balance}")

    source_path = Path(raw_file)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_file = target_dir / f"{output_stem}.tiff"
    metadata_file = target_dir / f"{output_stem}.json"

    wb_args = {
        "auto": ["-a"],
        "camera": ["-w"],
        "default": [],
    }[white_balance]
    command = [
        executable,
        "-T",
        *wb_args,
        "-o",
        "1",
        "-q",
        "3",
        "-Z",
        str(output_file),
        str(source_path),
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"{' '.join(command)} failed: {details}")
    if not output_file.exists():
        raise RuntimeError(f"dcraw did not write expected preview TIFF: {output_file}")

    np = _import_numpy()
    image = read_tiff(output_file)
    stats = {
        "source_file": str(source_path),
        "image": _array_stats(np, image),
        "postprocess_params": {
            "decoder": executable,
            "white_balance": white_balance,
            "output_color": "sRGB",
            "interpolation_quality": 3,
            "output_format": "tiff",
        },
        "command": command,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    metadata_file.write_text(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return camera_gphoto2.DecodeResult(
        source_file=source_path,
        output_files=(output_file, metadata_file),
        metadata_file=metadata_file,
        image_shape=tuple(int(value) for value in image.shape),
        image_dtype=str(image.dtype),
        stats=stats,
    )


def find_output_with_suffix(paths: Sequence[Path], suffix: str) -> Path:
    for path in paths:
        if path.suffix == suffix:
            return path
    raise RuntimeError(f"decoded output did not produce a {suffix} file")


def read_tiff(path: Path) -> Any:
    return _import_tifffile().imread(path)


def read_jpeg(path: Path) -> Any:
    cv2 = _import_cv2()
    np = _import_numpy()
    data = np.frombuffer(path.read_bytes(), dtype=np.uint8)
    bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if bgr is None:
        raise RuntimeError(f"could not decode embedded JPEG preview: {path}")
    return np.ascontiguousarray(bgr[..., ::-1])


def visual_decode_to_preview_uint8(image: Any) -> Any:
    np = _import_numpy()
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"expected HxWx3 visual image, got shape {image.shape}")
    if image.dtype == np.uint8:
        return image
    if image.dtype == np.uint16:
        return (np.clip(image, 0, 65535) / 257.0 + 0.5).astype(np.uint8)
    return np.clip(image, 0, 255).astype(np.uint8)


def _array_stats(np: Any, array: Any) -> dict[str, Any]:
    return {
        "shape": [int(value) for value in array.shape],
        "dtype": str(array.dtype),
        "pixel_count": _array_pixel_count(array),
        "min": int(array.min()),
        "max": int(array.max()),
        "channel_min": _channel_stat(array, "min"),
        "channel_max": _channel_stat(array, "max"),
        "channel_mean": _channel_stat(array, "mean"),
    }


def _array_pixel_count(array: Any) -> int:
    if len(array.shape) >= 3:
        return int(array.shape[0] * array.shape[1])
    return int(array.size)


def _channel_stat(array: Any, stat: str) -> list[int | float] | None:
    if len(array.shape) != 3:
        return None
    values: list[int | float] = []
    for channel in range(array.shape[2]):
        channel_array = array[..., channel]
        if stat == "min":
            values.append(int(channel_array.min()))
        elif stat == "max":
            values.append(int(channel_array.max()))
        elif stat == "mean":
            values.append(float(channel_array.mean()))
        else:
            raise AssertionError(stat)
    return values


def _import_numpy() -> Any:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for visual RAW preview decoding") from exc
    return np


def _import_tifffile() -> Any:
    try:
        import tifffile
    except ImportError as exc:
        raise RuntimeError("tifffile is required for visual RAW preview decoding") from exc
    return tifffile


def _import_cv2() -> Any:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("opencv-python-headless is required for embedded JPEG preview decoding") from exc
    return cv2


def _decode_process_text(value: bytes | str) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
