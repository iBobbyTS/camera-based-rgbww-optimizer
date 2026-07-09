---
name: camera-based-rgbww-optimizer
description: Use when working on camera-based RGBWW calibration, RGBWW channel control, Canon camera capture, Ray120c reference matching, or color-chart workflows.
---

# Camera-Based RGBWW Optimizer Skill

## Project Facts

- Planned optimizer language: Python.
- Implementation package: `src/camera_based_rgbww_optimizer/`.
- Source layout: `control/` for device control, `optimization/` for measurement/calibration workflows, `utils/` for shared helpers and post-processing, and `interaction/` for local UI tools.
- Root-level compatibility scripts are intentionally not part of the current interface.
- ESPHome device name and default host: `bedroom-rgbww-strip` / `bedroom-rgbww-strip.local`.
- ESPHome firmware configs live under `firmware/esphome/bedroom-rgbww-strip*.yaml`.
- `.venv/bin/python -m pip install -e .` installs the package's Python dependencies; `gphoto2`, `exiftool`, and `dcraw_emu` remain system dependencies.
- Reference light: Aputure Amaran Ray120c at 100% brightness.
- Camera path: Canon EOS R6 Mark III over USB PTP using `gphoto2`.
- On macOS, `camera_gphoto2` retries once after a gphoto2 USB-claim failure by killing per-user `ptpcamerad`/`icdd` Image Capture processes; set `CAMERA_BASED_RGBWW_OPTIMIZER_DISABLE_MACOS_PTP_RECOVERY=1` to disable that recovery during host diagnostics.
- Measurement basis: fixed linear camera RAW RGB pipeline by default. Visual fit-check tools default to the camera-rendered `JpgFromRaw` preview and may explicitly use `dcraw_emu` preview decoding as a fallback.
- Calibration scene: black card, white card, 18% gray card, 24-color chart, RGBWW output, and Ray120c output.

## Workflow

1. Check `docs/README.md` before changing calibration or device-control behavior.
2. Use package module commands, for example `.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 ...`.
3. Keep all temporary project outputs under repository `tmp/`.
4. For channel tests, use low initial values and test one physical channel at a time.
5. For Canon R6 Mark III sessions, use `camera_based_rgbww_optimizer.control.camera_gphoto2`.
6. For Ray120c CCT/G-M, HSI, and RGB reference control, use `camera_based_rgbww_optimizer.control.ray120c`.
7. For RGBWW code/duty response measurement, use `camera_based_rgbww_optimizer.optimization.measure_channel_response`.
8. For color-block location annotation, use `camera_based_rgbww_optimizer.interaction.location_picker_ui`; it keeps linear `.npy` RAW only for auto-exposure metering, then uses the camera-rendered `JpgFromRaw` preview for the Web UI image and automatic block detection. Out-of-bounds automatic detections are rejected instead of shown.
9. For checking a saved location JSON against a fresh camera capture, use `camera_based_rgbww_optimizer.interaction.location_checker <locations.json>`; it uses full-frame auto-exposure, extracts the camera-rendered `JpgFromRaw` preview from the final RAW, and only uses the location JSON for outline + color-name label fit checking.
10. For WW/CW endpoint CCT/G-M detection, use `camera_based_rgbww_optimizer.optimization.measure_white_endpoints`; this is a separate reusable calibration step and should usually run before formal white LUT optimization. Its default mode photographs strip WW/CW endpoints, estimates white-patch CCT/Duv from linear RAW, then controls Ray120c through adaptive CCT/G-M binary search. Use `--ray-search-mode grid` only when the fixed Ray reference grid is needed for cross-checking.
11. For formal CCT/G-M white LUT calibration, use `camera_based_rgbww_optimizer.optimization.measure_white_lut --endpoint-calibration <white-endpoints.json>`.

## Calibration Direction

- White mode should match Ray120c 100% brightness across `1800K..20000K` CCT and `-1.0..+1.0` G/M offset.
- Use the first-pass CCT/G-M LUT grid from `docs/README.md`.
- Endpoint detection now uses white-patch CCT/Duv from linear RAW as the search target, then verifies by photographing Ray120c candidates during adaptive CCT/G-M search. Treat the estimated CCT/Duv as a search heuristic, not a Lightroom-equivalent absolute color temperature.
- White LUT optimization should read the endpoint JSON. Targets inside the Ray-matched WW/CW span should strongly penalize RGB use; targets outside the span may allow RGB as exploratory gamut extension.
- Neutral patches are the primary objective for white calibration; color patches are auxiliary lower-weight checks.
- Every RGBWW candidate in high-brightness white calibration should keep at least one channel at `4095`.
- All optimizer logic should operate on gamma-calibrated channel values, not raw PWM values.
- Color mode should use model-first matching in camera-observed color space plus sparse residual correction where measurements justify it.
- If CCT/G-M calibration measurements reveal a better color-mode model or solver structure, update the strategy to follow the measured evidence.

## Safety

- Do not run broad high-output sweeps without an explicit bounded range.
- Confirm channel order, brightness scaling, and thermal behavior before increasing PWM levels.
- All scripts that can leave the RGBWW fixture on must explicitly turn it off before exiting, except dedicated light-on/control tools.
