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
- On macOS, `camera_gphoto2` retries once after a gphoto2 USB-claim or kernel-driver-detach failure by killing per-user `ptpcamerad`/`icdd` Image Capture processes; set `CAMERA_BASED_RGBWW_OPTIMIZER_DISABLE_MACOS_PTP_RECOVERY=1` to disable that recovery during host diagnostics.
- Measurement basis: fixed linear camera RAW RGB pipeline by default. Visual fit-check tools default to the camera-rendered `JpgFromRaw` preview and may explicitly use `dcraw_emu` preview decoding as a fallback.
- Calibration scene: black card, white card, 18% gray card, 24-color chart, RGBWW output, and Ray120c output.

## Workflow

1. Check `docs/README.md` before changing calibration or device-control behavior.
2. Use package module commands, for example `.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 ...`.
3. Keep all temporary project outputs under repository `tmp/`.
4. For channel tests, use low initial values and test one physical channel at a time.
5. For Canon R6 Mark III sessions, use `camera_based_rgbww_optimizer.control.camera_gphoto2`.
6. For Ray120c CCT/G-M, HSI, and RGB reference control, use `camera_based_rgbww_optimizer.control.ray120c`.
7. For explicit cleanup after manual or interrupted runs, use `camera_based_rgbww_optimizer.control.all_off`; it calls ESPHome `all_off` and sets Ray120c intensity to `0`.
8. For RGBWW code/duty response measurement, use `camera_based_rgbww_optimizer.optimization.measure_channel_response`.
9. For color-block location annotation, use `camera_based_rgbww_optimizer.interaction.location_picker_ui`; it keeps linear `.npy` RAW only for auto-exposure metering, then uses the camera-rendered `JpgFromRaw` preview for the Web UI image and automatic block detection. Out-of-bounds automatic detections are rejected instead of shown.
10. For checking a saved location JSON against a fresh camera capture, use `camera_based_rgbww_optimizer.interaction.location_checker <locations.json>`; it uses full-frame auto-exposure, extracts the camera-rendered `JpgFromRaw` preview from the final RAW, and only uses the location JSON for outline + color-name label fit checking.
11. For WW/CW endpoint CCT/G-M detection, use `camera_based_rgbww_optimizer.optimization.measure_white_endpoints`; this is a separate reusable calibration step and should usually run before formal white LUT optimization. Its default mode photographs strip WW/CW endpoints, estimates white-patch CCT/Duv from linear RAW, then controls Ray120c through target-driven alternating CCT/G-M correction: start from the strip-estimated CCT, correct the next CCT setting from observed error, solve G/M from observed Duv error, and repeat for three rounds. Defaults are total budgets of up to 64 CCT samples and 16 G/M samples per endpoint. Use `--ray-start ww=CCT,GM --ray-start cw=CCT,GM` to seed from a previous run. Use `--ray-search-mode grid` only when the fixed Ray reference grid is needed for cross-checking.
12. For formal CCT/G-M white LUT calibration, use `camera_based_rgbww_optimizer.optimization.measure_white_lut`. The canonical endpoint input is `config/white/white-endpoints.json`, the default Ray grid is `1800, 3200, 5600, 20000K` x raw G/M `0, 100, 200`, and the current location config is `config/location/locations-20260709-012045.json`. Every capture must have exactly one source on: turn the strip off before enabling Ray, then set Ray intensity to `0` immediately after its reference capture and before enabling the strip. Maintain independent Ray and strip automatic-exposure shutter caches; each target's initial strip candidate auto-exposes from the previous strip result, while its probes and feedback keep that resolved strip shutter fixed. Treat every linear `.npy` decode as temporary: delete it after region statistics, white-point estimation, and exposure checks for Ray, initial strip, probe, feedback, and confirmation captures; retain RAW files, decode metadata JSON, and calibration results. The channel-basis solver supplies an initial high-output command; `--initial-lut` may replace it with a previous measured command for strict repeat passes. Outside the native CCT span, low-penalty compensation RGB channels may own the required `4095` high-output constraint so the endpoint white channel can move away from saturation. Camera-observed CCT/Duv feedback then probes the four free channels and estimates a local Jacobian. The measured default goal is Duv below `0.0005` plus a dynamic CCT tolerance of at least `25K`, raised at high CCT to the Kelvin equivalent of `1 mired`. When measured samples bracket the target CCT and interpolated Duv remains within tolerance, use sample-pair secant interpolation for the next command; otherwise run up to sixteen constrained Broyden correction rounds. Solve each damped Jacobian step with channel headroom, the `0..4095` range, and the round step limit included as box constraints; never solve unconstrained and clip afterward because clipping can discard compensating terms at saturated channels. A candidate only completes after two independent off/on reapplications of the same command also meet the goal; each confirmation holds the strip off for one second, then holds the command for 60 seconds before capture. A failed settled confirmation becomes a new thermal base, the local Jacobian is rebuilt, and older transient samples no longer drive secant prediction. Two consecutive materially inaccurate bracketed-CCT predictions trigger the same rebase so an early cold sample cannot trap later warm-state secant steps. RGB penalties are computed per R/G/B channel from both CCT extension and distance from the endpoint-interpolated native G/M: red is released for warmer extension, blue for cooler extension, red plus blue toward magenta, and green toward green.
   For strict reruns, compare the previous measured command's score against the white-patch camera-RGB cone seed: keep the previous command first when its strict score is at most `4`, otherwise start from the cone model, and retain the other as fallback. Exhausted attempts may restart with the endpoint-biased or model-selected full-scale channel active; attempt indices must remain part of capture filenames.
13. To apply a completed white LUT, use `camera_based_rgbww_optimizer.control.white_lut CCT GM`. It reads `config/white/white-lut.json` by default, performs bilinear interpolation over neighboring targets using Kelvin on the CCT axis and linear raw G/M on the tint axis, applies optional linear `--intensity-percent` scaling, and delegates the final command to the shared ESPHome controller. It is an explicit light-on tool and intentionally leaves the strip on.

## Calibration Direction

- White mode should match Ray120c 100% brightness across `1800K..20000K` CCT and `-1.0..+1.0` G/M offset.
- Use the first-pass CCT/G-M LUT grid from `docs/README.md`.
- Endpoint detection now uses white-patch CCT/Duv from linear RAW as the search target, then verifies by photographing Ray120c candidates during adaptive CCT/G-M correction. Treat the estimated CCT/Duv as a search heuristic, not a Lightroom-equivalent absolute color temperature.
- White LUT optimization should read the endpoint JSON and interpolate the native white-only G/M between WW and CW. Preserve strong RGB penalties near that native locus, then directionally relax only the channels needed for CCT extension or G/M compensation.
- Neutral patches are the primary objective for white calibration; color patches are auxiliary lower-weight checks.
- Every RGBWW candidate in high-brightness white calibration should keep at least one channel at `4095`.
- All optimizer logic should operate on gamma-calibrated channel values, not raw PWM values.
- Color mode should use model-first matching in camera-observed color space plus sparse residual correction where measurements justify it.
- If CCT/G-M calibration measurements reveal a better color-mode model or solver structure, update the strategy to follow the measured evidence.

## Safety

- Do not run broad high-output sweeps without an explicit bounded range.
- Confirm channel order, brightness scaling, and thermal behavior before increasing PWM levels.
- All scripts that can leave the RGBWW fixture on must explicitly turn it off before exiting, except dedicated light-on/control tools.
