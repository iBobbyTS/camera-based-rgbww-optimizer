from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote
from camera_based_rgbww_optimizer.interaction import location_picker_ui
from camera_based_rgbww_optimizer.interaction import raw_visual_preview
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR
from camera_based_rgbww_optimizer.utils import location_regions


DEFAULT_OUTPUT_DIR = PROJECT_TMP_DIR / "location-checker"
DEFAULT_TARGET_MAX = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX
DEFAULT_FILENAME_TEMPLATE = "%Y%m%d-%H%M%S-location-check.%C"
DCRAW_WHITE_BALANCE_CHOICES = raw_visual_preview.DCRAW_WHITE_BALANCE_CHOICES
VISUAL_PREVIEW_SOURCE_CHOICES = raw_visual_preview.VISUAL_PREVIEW_SOURCE_CHOICES


@dataclass(frozen=True)
class LocationCheckResult:
    location_config: Path
    raw_file: Path
    decoded_file: Path
    overlay_file: Path
    metadata_file: Path
    region_count: int
    image_shape: tuple[int, ...]
    shutter_speed: str
    capture_count: int


def load_required_location_regions(path: Path, *, expected_count: int = 24) -> list[dict[str, Any]]:
    regions = location_regions.load_location_regions(path, "all")
    if len(regions) != expected_count:
        raise RuntimeError(f"location checker requires exactly {expected_count} blocks, got {len(regions)} from {path}")
    return regions


def validate_regions_inside_image(image: Any, regions: Sequence[dict[str, Any]]) -> None:
    np = _import_numpy()
    for region in regions:
        try:
            location_regions.extract_region(np, image, region)
        except ValueError as exc:
            raise RuntimeError(f"{region.get('name', 'region')} does not fit the captured image: {exc}") from exc


def render_location_overlay(preview: Any, regions: Sequence[dict[str, Any]], output_path: Path) -> Path:
    np = _import_numpy()
    cv2 = _import_cv2()
    if preview.ndim != 3 or preview.shape[2] != 3:
        raise ValueError(f"expected HxWx3 preview image, got shape {preview.shape}")
    if preview.dtype != np.uint8:
        raise ValueError(f"expected uint8 preview image, got dtype {preview.dtype}")

    output = preview.copy()
    for region in regions:
        points = region.get("points")
        if not points:
            continue
        polygon = np.array([[(int(round(x)), int(round(y))) for x, y in points]], dtype=np.int32)
        color = _region_color(int(region.get("index", 0)))
        cv2.polylines(output, polygon, isClosed=True, color=color, thickness=5, lineType=cv2.LINE_AA)
        cv2.polylines(output, polygon, isClosed=True, color=(0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
        label = _region_color_label(region)
        if label is not None:
            _draw_region_label(cv2, np, output, region, label, color)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(location_picker_ui.rgb_to_png_data(output))
    return output_path


def capture_location_check(
    location_config: Path,
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    target_max: int = DEFAULT_TARGET_MAX,
    iso: str | None = None,
    aperture: str | None = None,
    image_format: str = camera_gphoto2.DEFAULT_IMAGE_FORMAT,
    min_shutter_speed: str = camera_gphoto2.DEFAULT_MIN_SHUTTER_SPEED,
    max_shutter_speed: str = camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED,
    max_exposure_trials: int = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_TRIALS,
    max_captures: int = camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_CAPTURES,
    expected_model: str = camera_gphoto2.DEFAULT_CAMERA_MODEL,
    camera_port: str | None = None,
    executable: str = "gphoto2",
    preview_source: str = "camera-jpeg",
    exiftool_executable: str = "exiftool",
    dcraw_executable: str = "dcraw_emu",
    dcraw_white_balance: str = "camera",
    timeout: float = 90.0,
    camera_backend: camera_gphoto2.CameraBackend | None = None,
) -> LocationCheckResult:
    regions = load_required_location_regions(location_config)
    run_dir = output_dir / datetime.now().strftime("%Y%m%d-%H%M%S")
    camera_dir = run_dir / "camera"
    decode_dir = run_dir / "decoded"

    exposure = camera_gphoto2.auto_expose_capture(
        output_dir=camera_dir,
        filename_template=DEFAULT_FILENAME_TEMPLATE,
        target_max=target_max,
        iso=iso,
        aperture=aperture,
        image_format=image_format,
        min_shutter_speed=min_shutter_speed,
        max_shutter_speed=max_shutter_speed,
        max_trials=max_exposure_trials,
        max_captures=max_captures,
        decode_output_dir=decode_dir,
        decode_formats=("npy",),
        metering_regions=None,
        port=camera_port,
        expected_model=expected_model,
        executable=executable,
        timeout=timeout,
        camera_backend=camera_backend,
    )
    capture = exposure.final_capture
    if capture.decoded is None:
        raise RuntimeError("auto exposure did not return decoded output")
    decoded = capture.decoded
    preview_decoded = _decode_visual_preview(
        capture.saved_file,
        output_dir=decode_dir,
        output_stem="location-check-preview",
        preview_source=preview_source,
        exiftool_executable=exiftool_executable,
        dcraw_executable=dcraw_executable,
        dcraw_white_balance=dcraw_white_balance,
        timeout=timeout,
    )
    preview_file = _find_visual_preview_file(preview_decoded.output_files, preview_source=preview_source)
    image = _read_visual_preview(preview_file, preview_source=preview_source)
    validate_regions_inside_image(image, regions)

    preview = _visual_decode_to_preview_uint8(image)
    overlay_file = run_dir / "location-check-overlay.png"
    render_location_overlay(preview, regions, overlay_file)

    metadata_file = run_dir / "location-check.json"
    metadata = {
        "location_config": str(location_config),
        "raw_file": str(capture.saved_file),
        "decoded_file": str(preview_file),
        "overlay_file": str(overlay_file),
        "region_count": len(regions),
        "target_max": target_max,
        "metering_mode": camera_gphoto2.METERING_MODE_FULL,
        "decode_mode": _visual_preview_decode_mode(preview_source),
        "decode_white_balance": dcraw_white_balance if preview_source == "dcraw" else None,
        "auto_exposure": exposure.to_jsonable(),
        "metering_decode": decoded.to_jsonable(),
        "decode": preview_decoded.to_jsonable(),
    }
    metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    return LocationCheckResult(
        location_config=location_config,
        raw_file=capture.saved_file,
        decoded_file=preview_file,
        overlay_file=overlay_file,
        metadata_file=metadata_file,
        region_count=len(regions),
        image_shape=tuple(int(value) for value in image.shape),
        shutter_speed=capture.settings.shutter_speed,
        capture_count=len(exposure.trials) + 1 + len(exposure.rejected_finals),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture one camera image and render a PNG overlay for a required location JSON."
    )
    parser.add_argument("location_config", type=Path, help="Required location picker JSON to check against the capture.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for checker outputs.")
    parser.add_argument("--target-max", type=int, default=DEFAULT_TARGET_MAX, help="White point used for preview scaling.")
    parser.add_argument("--iso", help="Fixed ISO. Defaults to 100 locally or the current remote value.")
    parser.add_argument("--aperture", help="Fixed aperture. Defaults to 4 locally or the current remote value.")
    parser.add_argument("--image-format", default=camera_gphoto2.DEFAULT_IMAGE_FORMAT)
    parser.add_argument("--min-shutter-speed", default=camera_gphoto2.DEFAULT_MIN_SHUTTER_SPEED)
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--max-exposure-trials", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_TRIALS)
    parser.add_argument("--max-captures", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_CAPTURES)
    parser.add_argument("--model", default=camera_gphoto2.DEFAULT_CAMERA_MODEL)
    parser.add_argument("--port", dest="camera_port", help="Camera USB port passed to gphoto2.")
    parser.add_argument("--camera-port", dest="camera_port", help="Camera USB port passed to gphoto2.")
    parser.add_argument("--gphoto2", default="gphoto2")
    parser.add_argument("--camera-backend", choices=("local", "remote"), default="local")
    parser.add_argument("--remote-env-file", type=Path, default=camera_remote.DEFAULT_ENV_FILE)
    parser.add_argument("--remote-base-url", help=f"Override {camera_remote.BASE_URL_ENV} for the remote backend.")
    parser.add_argument(
        "--preview-source",
        choices=VISUAL_PREVIEW_SOURCE_CHOICES,
        default="camera-jpeg",
        help="Visual preview source used for region fit checking and overlay rendering.",
    )
    parser.add_argument("--exiftool", default="exiftool", help="exiftool executable used to extract camera JPEG previews.")
    parser.add_argument("--dcraw", default="dcraw_emu", help="dcraw-compatible executable used for visual preview decode.")
    parser.add_argument(
        "--dcraw-white-balance",
        choices=DCRAW_WHITE_BALANCE_CHOICES,
        default="camera",
        help="White balance mode for dcraw visual preview decode.",
    )
    parser.add_argument("--timeout", type=float, default=90.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    camera_backend = (
        None
        if args.camera_backend == "local"
        else camera_remote.RemoteCameraBackend.from_environment(
            env_file=args.remote_env_file,
            base_url=args.remote_base_url,
            timeout=args.timeout,
        )
    )
    result = capture_location_check(
        args.location_config,
        output_dir=args.output_dir,
        target_max=args.target_max,
        iso=args.iso,
        aperture=args.aperture,
        image_format=args.image_format,
        min_shutter_speed=args.min_shutter_speed,
        max_shutter_speed=args.max_shutter_speed,
        max_exposure_trials=args.max_exposure_trials,
        max_captures=args.max_captures,
        expected_model=args.model,
        camera_port=args.camera_port,
        executable=args.gphoto2,
        preview_source=args.preview_source,
        exiftool_executable=args.exiftool,
        dcraw_executable=args.dcraw,
        dcraw_white_balance=args.dcraw_white_balance,
        timeout=args.timeout,
        camera_backend=camera_backend,
    )
    print(f"Location check overlay: {result.overlay_file}")
    print(f"Metadata: {result.metadata_file}")
    print(f"Captured RAW: {result.raw_file}")
    print(f"Decoded preview: {result.decoded_file}")
    print(
        f"Regions: {result.region_count}; image shape: {result.image_shape}; "
        f"shutter: {result.shutter_speed}; captures: {result.capture_count}"
    )
    return 0


def _find_output_with_suffix(paths: Sequence[Path], suffix: str) -> Path:
    return raw_visual_preview.find_output_with_suffix(paths, suffix)


def _decode_visual_preview(
    raw_file: str | Path,
    *,
    output_dir: str | Path,
    output_stem: str,
    preview_source: str,
    exiftool_executable: str = "exiftool",
    dcraw_executable: str = "dcraw_emu",
    dcraw_white_balance: str = "camera",
    timeout: float = 90.0,
) -> camera_gphoto2.DecodeResult:
    if preview_source == "camera-jpeg":
        return raw_visual_preview.decode_embedded_jpeg_preview(
            raw_file,
            output_dir=output_dir,
            output_stem=output_stem,
            executable=exiftool_executable,
            timeout=timeout,
        )
    if preview_source == "dcraw":
        return raw_visual_preview.decode_dcraw_preview(
            raw_file,
            output_dir=output_dir,
            output_stem=output_stem,
            executable=dcraw_executable,
            white_balance=dcraw_white_balance,
            timeout=timeout,
        )
    raise ValueError(f"unsupported preview source: {preview_source}")


def _find_visual_preview_file(paths: Sequence[Path], *, preview_source: str) -> Path:
    if preview_source == "camera-jpeg":
        return _find_output_with_suffix(paths, ".jpg")
    if preview_source == "dcraw":
        return _find_output_with_suffix(paths, ".tiff")
    raise ValueError(f"unsupported preview source: {preview_source}")


def _read_visual_preview(path: Path, *, preview_source: str) -> Any:
    if preview_source == "camera-jpeg":
        return raw_visual_preview.read_jpeg(path)
    if preview_source == "dcraw":
        return raw_visual_preview.read_tiff(path)
    raise ValueError(f"unsupported preview source: {preview_source}")


def _visual_preview_decode_mode(preview_source: str) -> str:
    if preview_source == "camera-jpeg":
        return "camera_embedded_jpeg_preview"
    if preview_source == "dcraw":
        return "dcraw_emu_visual_preview"
    raise ValueError(f"unsupported preview source: {preview_source}")


def _decode_dcraw_preview(
    raw_file: str | Path,
    *,
    output_dir: str | Path,
    output_stem: str = "location-check-preview",
    executable: str = "dcraw_emu",
    white_balance: str = "camera",
    timeout: float = 90.0,
) -> camera_gphoto2.DecodeResult:
    return raw_visual_preview.decode_dcraw_preview(
        raw_file,
        output_dir=output_dir,
        output_stem=output_stem,
        executable=executable,
        white_balance=white_balance,
        timeout=timeout,
    )


def _visual_decode_to_preview_uint8(image: Any) -> Any:
    return raw_visual_preview.visual_decode_to_preview_uint8(image)


def _draw_region_label(
    cv2: Any,
    np: Any,
    image: Any,
    region: dict[str, Any],
    label: str,
    color: tuple[int, int, int],
) -> None:
    points = region.get("points")
    if not points:
        return
    polygon = np.array(points, dtype=np.float32)
    x = int(round(float(polygon[:, 0].mean())))
    y = int(round(float(polygon[:, 1].mean())))
    font = cv2.FONT_HERSHEY_SIMPLEX
    min_x = float(polygon[:, 0].min())
    max_x = float(polygon[:, 0].max())
    min_y = float(polygon[:, 1].min())
    max_y = float(polygon[:, 1].max())
    max_width = max(1.0, (max_x - min_x) * 0.88)
    max_height = max(1.0, (max_y - min_y) * 0.38)
    scale = 1.0
    thickness = 2
    text_size, baseline = cv2.getTextSize(label, font, scale, thickness)
    if text_size[0] > 0 and text_size[1] > 0:
        scale = min(scale, max_width / float(text_size[0]), max_height / float(text_size[1]))
    scale = max(0.35, min(1.0, scale))
    text_size, baseline = cv2.getTextSize(label, font, scale, thickness)
    x = max(6, min(image.shape[1] - text_size[0] - 6, x - text_size[0] // 2))
    y = max(text_size[1] + 6, min(image.shape[0] - baseline - 6, y + text_size[1] // 2))
    cv2.putText(image, label, (x, y), font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(image, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)


def _region_color_label(region: dict[str, Any]) -> str | None:
    patch = region.get("patch")
    if not isinstance(patch, dict):
        return None
    name = patch.get("name")
    if not isinstance(name, str):
        return None
    return _PATCH_COLOR_LABELS.get(name, name.replace("_", " ").title())


_PATCH_COLOR_LABELS = {
    "black": "Black",
    "neutral_3_5": "Dark Gray",
    "neutral_5": "Gray",
    "neutral_6_5": "Mid Gray",
    "neutral_8": "Light Gray",
    "white": "White",
    "cyan": "Cyan",
    "magenta": "Magenta",
    "yellow": "Yellow",
    "red": "Red",
    "green": "Green",
    "blue": "Blue",
    "purple": "Purple",
    "orange": "Orange",
    "orange_yellow": "Orange Yellow",
    "yellow_green": "Yellow Green",
    "moderate_red": "Moderate Red",
    "purplish_blue": "Purplish Blue",
    "bluish_green": "Bluish Green",
    "blue_flower": "Blue Flower",
    "foliage": "Foliage",
    "blue_sky": "Blue Sky",
    "light_skin": "Light Skin",
    "dark_skin": "Dark Skin",
}


def _region_color(index: int) -> tuple[int, int, int]:
    palette = (
        (66, 217, 255),
        (255, 207, 64),
        (98, 220, 146),
        (255, 125, 125),
        (176, 132, 255),
        (255, 166, 80),
    )
    return palette[(index - 1) % len(palette)]


def _import_numpy() -> Any:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("numpy is required for the location checker") from exc
    return np


def _import_cv2() -> Any:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("opencv-contrib-python-headless is required for the location checker") from exc
    return cv2


if __name__ == "__main__":
    raise SystemExit(main())
