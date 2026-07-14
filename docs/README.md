# Camera-Based RGBWW Optimizer

## Purpose

This project calibrates and optimizes a five-channel RGBWW light source using a
camera as the measurement device, an Aputure Amaran Ray120c as the high-color
reference, and a 24-patch color chart for camera-observed matching.

Core goals:

- Measure per-channel RGBWW brightness response in linear camera RAW space.
- Build code-duty correction curves for linear brightness control.
- Capture and annotate color-chart locations for repeatable patch statistics.
- Match white mode against Ray120c CCT/G-M references.
- Build model-first RGB/HSI matching workflows with sparse residual correction
  only where measurements justify it.

## Python Layout

Implementation lives in the installable package:

```text
src/camera_based_rgbww_optimizer/
  control/        # Canon/gphoto2, Ray120c, ESPHome RGBWW strip control
  optimization/   # Measurement and calibration workflows
  utils/          # Shared geometry/statistics and post-processing tools
  interaction/    # Local Web UI tools
  paths.py        # Project-root and tmp-path helpers
```

Install the project in editable mode before running package modules:

```bash
.venv/bin/python -m pip install -e .
```

This installs the package's Python runtime dependencies, including ESPHome
Native API control, Ray120c token generation, RAW decoding, NumPy processing,
TIFF export, and OpenCV color-chart detection. The `gphoto2` command-line tool
`exiftool`, and `dcraw_emu` are system dependencies and must still be installed
separately.

All commands below use `python -m ...`; root-level legacy script entry points are
not part of the current project interface.

## Device Facts

- Camera: Canon EOS R6 Mark III over USB PTP with `gphoto2`.
- Reference light: Aputure Amaran Ray120c controlled through Amaran Desktop
  OpenAPI v2 at `ws://127.0.0.1:33782`.
- RGBWW fixture: ESPHome Native API action `set_rgbww_12bit` with channel values
  `0..4095`.
- Default ESPHome device host: `bedroom-rgbww-strip.local`.
- Default ESPHome expected name: `bedroom-rgbww-strip`.
- The ESPHome host and expected name can be overridden with
  `CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_HOST` and
  `CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_EXPECTED_NAME`.
- ESPHome firmware files live under `firmware/esphome/` and use the same
  `bedroom-rgbww-strip` device name.

## Temporary Data

All project temporary data, captures, decoded images, probe outputs, and scratch
artifacts must live under the repository `tmp/` directory. Do not write project
temporary data to the system `/tmp`.

Scripts that can leave the RGBWW fixture on must turn it off before exiting,
except explicit light-on/control tools.

Use the shared cleanup command after manual runs or shell-interrupted
calibration jobs. It calls ESPHome `all_off` and sets Ray120c intensity to `0`:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --ray-timeout 5
```

## RGBWW Control

Use the ESPHome control module:

```python
from camera_based_rgbww_optimizer.control.esphome import light

light(cw, ww, r, g, b)
```

Command-line use:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.esphome 0 0 2048 0 0
.venv/bin/python -m camera_based_rgbww_optimizer.control.esphome 0 0 0 0 0
.venv/bin/python -m camera_based_rgbww_optimizer.control.esphome 2048 0 0 0 0 --no-curve
```

If `config/channel/code-duty-curve.json` exists, input values are treated as
desired linear brightness codes and mapped through the measured code-duty curve
before sending PWM codes. Use `--no-curve` or `curve_path=None` for raw PWM
tests. If the curve file does not exist, values pass through directly. All-zero
output calls the ESPHome `all_off` action.

## Camera Control

Validated local setup on 2026-06-05:

- Host tool: Homebrew `gphoto2 2.5.32`
- Camera library: `libgphoto2 2.5.34`
- Detected camera: `Canon EOS R6 Mark III`
- Camera firmware/device version reported by gphoto2: `3-1.0.2`

Detect and capture:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 detect
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 capture \
  --output-dir tmp/captures/camera \
  --iso 100 \
  --aperture 4 \
  --shutter-speed 1/30 \
  --image-format RAW
```

Decode a CR3 into linear 16-bit camera RGB:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 decode tmp/captures/camera/example.cr3 \
  --output-dir tmp/captures/decoded \
  --format npy \
  --format tiff
```

By default the decode path uses `rawpy`/LibRaw with raw color output, no
camera/auto white balance, no auto-brightening, linear gamma, and 16-bit output.
LibRaw handles RAW black/white level correction before demosaicing; do not apply
a second manual black-level subtraction to the decoded output. This fixed rawpy
path is the measurement basis, not the visual preview path.

Auto-exposure target:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 auto-expose \
  --output-dir tmp/captures/camera \
  --decode-output-dir tmp/captures/decoded \
  --target-max 49152 \
  --iso 100 \
  --aperture 4 \
  --min-shutter-speed 1/8000 \
  --max-shutter-speed 30 \
  --max-trials 5 \
  --max-captures 10
```

The auto-exposure routine keeps ISO and aperture fixed, starts from the current
bounded shutter speed, meters decoded linear RGB, caps total shutter releases,
deletes trial files, and saves only the accepted final capture. Use
`--scratch-dir /Volumes/4T/temp/rgbww-optimizer/scratch` when temporary
auto-exposure trial captures should be kept off the repository disk.

On macOS, Apple Image Capture may start `ptpcamerad`/`icdd` and briefly claim
the PTP USB interface. The camera wrapper retries once after a
`Could not claim the USB device` gphoto2 failure by killing those per-user Image
Capture processes so gphoto2 can claim the interface first. Set
`CAMERA_BASED_RGBWW_OPTIMIZER_DISABLE_MACOS_PTP_RECOVERY=1` to disable this
automatic recovery when diagnosing host-side camera issues.

## Native RAW Observer Validation

`camera_based_rgbww_optimizer.measurement.raw_mosaic_patches` measures a saved
CR3 directly in the visible Bayer mosaic. It keeps `R/G1/G2/B` planes separate,
uses the saved color-chart regions, supports exposure normalization and an
explicit ambient RAW, and writes JSON only. It does not demosaic and does not
create `.npy` files. The companion offline analysis module derives repeatability,
exposure-linearity, and G1/G2 evidence from those reports; it does not set
empirical quality thresholds automatically.

The P1 capture runner requires the external best 70-point LUT explicitly,
rather than reading the default 4x3 LUT, and plans ambient, independent
Ray/strip exposure caches, alternating paired repeats, exposure brackets,
optional flat field, and two cleanup layers. `--dry-run` performs no device
I/O and writes only `plan.json`:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --dry-run
```

Real acquisition requires both `--execute` and `--allow-high-output`; it uses
the native Bayer exposure meter, emits JSON-only patch reports, and keeps Ray
and strip shutter caches independent. It must be launched through a temporary
shell wrapper with `EXIT`, `INT`, `TERM`, and `HUP` traps that run
`control.all_off --json` into the same run directory. Python `finally` uses
the same public cleanup entry point, including on capture errors. The runner
accepts an existing run directory only when it is empty, so the shell trap can
create the directory without allowing any old experiment to be reused.

## Location Picker

Use the local Web UI to capture a preview and mark color-chart patches:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.interaction.location_picker_ui \
  --blocks 24 \
  --rows 4 \
  --cols 6
```

The UI serves on `127.0.0.1:8765` by default. It auto-exposes, decodes a preview,
runs automatic block detection, then lets the user edit quadrilaterals. Confirmed
locations are saved under `config/location/`.

The picker keeps the linear `.npy` RAW decode for auto-exposure metering, then
extracts the camera-rendered `JpgFromRaw` preview with `exiftool` for the visible
Web UI image and automatic block detection. This makes the picker match the
camera/Finder preview instead of `dcraw_emu` full RAW color reconstruction. Pass
`--preview-source dcraw` to use the fallback `dcraw_emu` path; its default white
balance uses `dcraw_emu -w`, while `--dcraw-white-balance auto` uses
`dcraw_emu -a` whole-image auto white balance. Automatic detection results with
any point outside the decoded preview are rejected instead of displayed.

The Python packages used by this path are installed by `pip install -e .`;
`exiftool` and `dcraw_emu` are separate system dependencies.

## Native Bayer Patch Statistics

Analyze an existing CR3 directly in the native Bayer mosaic without demosaic,
white balance, gamma, or device access:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.measurement.raw_mosaic_patches \
  tmp/location-ui/20260709-012027/camera/20260709-012032-location.cr3 \
  --exposure 1/20 \
  --location-config config/location/locations-20260709-012045.json \
  --output tmp/raw-observer-validation/offline/patch-statistics.json
```

Pass `--ambient-raw` and `--ambient-exposure` to normalize both captures by
exposure time before subtracting the ambient/dark observation. The report keeps
`R/G1/G2/B` separate, optionally derives `G=(G1+G2)/2`, records per-plane black
and effective white levels, and includes median, trimmed mean, MAD, variance,
pixel counts, clipping, and noise-floor diagnostics. Color-chart coordinates
are scaled from the saved location image dimensions to `raw_image_visible`,
which accounts for the one-pixel size difference in the current Canon files.

Acceptance thresholds live in `config/camera/raw-observer.json`. The clipping
and near-noise thresholds intentionally remain `null` until the paired
repeatability and three-exposure linearity experiment establishes defensible
values. Reports therefore remain `pending_thresholds` and are not optimization
acceptance evidence yet. This native-mosaic path runs alongside the existing
demosaiced white-patch CCT/Duv path; it does not replace that diagnostic path.

Check a saved location file against a fresh single camera capture:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.interaction.location_checker \
  config/location/locations-20260605-225800.json
```

The checker requires a location JSON argument, uses full-frame auto-exposure,
keeps the accepted final RAW capture, then extracts the camera-rendered
`JpgFromRaw` preview with `exiftool` for visual inspection. Pass
`--preview-source dcraw` to use the fallback `dcraw_emu` path. The
checker verifies the 24 saved polygons fit the decoded preview and writes a PNG
overlay plus metadata under `tmp/location-checker/`. The overlay labels saved
ColorChecker patches by color name, not block number. It does not fill the
inside of each patch box; older location files without patch metadata still get
colored outlines but no numeric fallback labels.

## Channel Response Measurement

Measure per-channel code/duty response:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_channel_response \
  --channels cw,ww,r,g,b \
  --dry-run
```

Run a real high-output sweep only after confirming the strip and camera setup:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_channel_response \
  --channels cw,ww,r,g,b \
  --location-config config/location/locations-20260605-225800.json \
  --block-indices all \
  --allow-high-output
```

The measurement script turns the light off before and after the run, captures a
fixed all-off ambient frame at `ISO 100` / `30s`, measures codes from high to low
down to `8`, normalizes by shutter seconds, subtracts ambient, and writes an
incremental JSON report under `tmp/channel-response/`.

## Response Merge And Curve Generation

Merge compact measurement data:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.utils.merge_channel_response
```

Generate the compact code-duty correction curve:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.utils.generate_channel_curve \
  --input tmp/channel-response/merged/channel-code-duty-response-merged.json \
  --output config/channel/code-duty-curve.json
```

The full merged response JSON is the measurement archive for later color
modeling. The code-duty correction path only needs the small curve file.

## Ray120c Control

Use Amaran Desktop OpenAPI v2 for Ray120c reference control:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c set-cct 1800 --intensity-percent 1 --gm 200
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-cct
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c set-hsl 60 50 --intensity-percent 1
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-hsl
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c set-rgb 12 34 56 --intensity-percent 1
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-rgb
```

Confirmed Ray120c ranges:

- CCT: `1800K..20000K`
- Intensity raw: `0..1000`, where `10` is `1%`
- G/M raw: `0..200`, where `100` is neutral
- HSI/HSL hue: `0..360`
- HSI/HSL saturation: `0..100`
- RGB: `0..255` per channel

## Calibration Direction

White mode should match Ray120c 100% brightness across:

- CCT: `1800K..20000K`
- G/M offset: `-1.0..+1.0`

Initial CCT/G-M LUT grid:

- CCT points: `1800, 2000, 2300, 2700, 3200, 3800, 4500, 5000, 5600, 6500, 8000, 10000, 14000, 20000`
- G/M raw points: `0, 70, 100, 130, 200`
- Total initial grid: `14 x 5 = 70` Ray120c target points

Before optimizing a white LUT, measure the strip's WW and CW endpoints as a
separate reusable calibration artifact. By default, the endpoint script first
photographs the strip endpoints, estimates the white patch CCT/Duv from linear
RAW, then controls the Ray120c through target-driven CCT/G-M correction to find
the nearest reference for each endpoint. The adaptive search starts from the
strip-estimated CCT, corrects the next Ray setting from the observed CCT error,
then alternates CCT and G/M correction for three rounds. Defaults are a total
budget of up to 64 CCT samples and 16 G/M samples per endpoint:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_white_endpoints \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/white-endpoints \
  --location-config config/location/locations-20260605-225800.json \
  --allow-high-output
```

When previous measurements have already found a useful Ray starting point, seed
the adaptive run per endpoint:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_white_endpoints \
  --output-dir tmp/white-endpoints \
  --location-config config/location/locations-20260605-225800.json \
  --allow-high-output \
  --ray-start ww=2961,160 \
  --ray-start cw=7895,100
```

Use `--ray-search-mode grid` to run the legacy fixed `14 x 5` Ray reference
grid and rank references by camera-observed similarity instead of CCT/Duv search.
For shell-launched endpoint runs, wrap the command with
`camera_based_rgbww_optimizer.control.all_off` as an `EXIT` cleanup trap so the
strip and Ray120c are explicitly turned off after success, failure, or
interruption.

The selected best-environment endpoint result is stored as
`config/white/white-endpoints.json`. It contains the canonical
`ray_endpoint_matches` and `white_range` used by the formal white LUT run:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_white_lut \
  --output-dir tmp/white-lut-calibration \
  --endpoint-calibration config/white/white-endpoints.json \
  --location-config config/location/locations-20260709-012045.json \
  --allow-high-output
```

The white LUT runner's default target grid is `1800, 3200, 5600, 20000K` x G/M
raw values `0, 100, 200`, covering the complete Ray120c G/M range from maximum
magenta through neutral to maximum green. It uses neutral patches as the primary
model objective and color patches as lower-weight auxiliary checks. Every RGBWW
candidate is brightness-maximized by keeping one selected active channel at
`4095`.

RGB regularization is directional instead of using a single inside/outside CCT
switch. The optimizer linearly interpolates a native G/M prior between the
measured WW endpoint (`2931K`, raw G/M `176`) and CW endpoint (`7702K`, raw G/M
`160`), clamping outside that CCT span. It then combines:

- CCT extension need: release red below the WW endpoint and blue above the CW
  endpoint.
- G/M compensation need: release red plus blue toward magenta, or green toward
  green.
- Native-white preservation: keep unrelated RGB channels strongly penalized.

The default penalties are `0.45` at the native white-only point, a `0.06` cap
for the primary that extends CCT just outside the white-channel span, and `0.02`
at full CCT/G-M compensation. The transition follows the normalized distance to
the supported CCT or directional G/M limit. The same per-channel penalties are
used by both the model solver and the feedback loop. Each target's complete
policy is written into `target_plan[].rgb_policy`, including during `--dry-run`.

The per-target model solution is only the starting command. The runner captures
that command, estimates its white-patch CCT/Duv, then probes each of the four
free channels to estimate a local Jacobian. When measured samples bracket the
target CCT and the interpolated Duv remains within tolerance, the next command
uses sample-pair secant interpolation. Otherwise it applies a damped, bounded
Jacobian update and uses Broyden secant updates for up to sixteen feedback rounds.
The Jacobian step is solved as a box-constrained regularized least-squares
problem: current channel headroom, the `0..4095` code range, and the per-round
maximum step are constraints in the solve itself. Do not solve an unconstrained
step and clip it afterward; clipping can remove compensating boundary terms and
reverse the predicted CCT direction.
An initial, probe, or feedback sample inside the goal is not sufficient to
complete a target. The runner reapplies the exact command and requires two
additional independent captures to remain inside the goal. A failed
confirmation is retained as a normal measurement and feedback continues from
the newly observed state. This prevents an early probe captured under a
different strip thermal state from becoming the final LUT command. Configure
the count with `--feedback-confirmations`; the default is `2`. Each confirmation
holds the selected command for `60` seconds before capture by default so the
accepted LUT represents continuous-use output rather than a transient channel
temperature. Configure that interval with
`--feedback-confirmation-settle-seconds`.
Each confirmation first sends an all-zero strip command for one second before
reapplying the candidate, matching how a saved LUT starts from the off state;
configure that interval with `--feedback-confirmation-off-seconds`.
If a thermally settled confirmation fails, the runner treats it as the new
local base, probes the four free channels again, and discards older transient
samples from subsequent secant prediction while preserving them in the result
JSON. At most two such thermal Jacobian rebuilds are allowed per start by
default; configure this with `--feedback-thermal-rebases`.
The same rebuild is triggered when two consecutive bracketed-CCT secant
predictions materially understate the measured goal score. This prevents an
early cold-state sample from repeatedly bracketing later warm-state samples
after the strip response has moved.
The default measured stop target is `<0.0005` absolute Duv error. CCT uses a
dynamic tolerance: at least `25K`, raised at high CCT to the Kelvin equivalent
of `1 mired` around the camera-observed Ray reference. This matches measured
end-to-end repeatability without making the numerically unstable high-CCT
Kelvin estimate control the solve.
All samples, Jacobians, predicted steps, measured errors, and the selected best
command are persisted in `white-lut-calibration.json`. Use each target's
`selected_command` for the final LUT; `solver.command` is only the model's
initial candidate. Pass
`--feedback-rounds 0` only for a model-only one-shot diagnostic.
For a stricter repeat pass over an already measured grid, pass
`--initial-lut <previous-white-lut-calibration.json>` to seed each target from
its previous selected command before camera feedback.
The runner also solves a full-scale white-patch camera-RGB cone model after the
Ray reference capture. A previous measured command whose strict normalized
score is at most `4` remains the primary local start; otherwise the white-patch
model starts first. The unused start is retained as a fallback. If a local
attempt exhausts its budget, the runner may restart with the endpoint-biased or
model-selected full-scale channel active so that the previously saturated
channel becomes adjustable. Attempt numbers are included in capture filenames.

Before every Ray reference capture, the strip is explicitly turned off. After
the Ray capture finishes, Ray is set to intensity `0` before any RGBWW capture
is allowed to start. Ray and strip automatic exposure use independent shutter
caches initialized from the fixed `1/30` default: later Ray targets start from
the previous Ray result, while each target's initial strip candidate starts
from the previous strip result. Probe and feedback captures keep that target's
resolved strip shutter fixed. Linear `.npy` decodes are temporary measurement
inputs: after region statistics, white-point estimation, and exposure checks
finish, every Ray, initial strip, probe, and feedback `.npy` is deleted. RAW
captures, decode metadata JSON, and calibration results remain. The existing
final cleanup still turns off both the strip and Ray120c on normal exit or
exceptions.

Apply the calibrated white LUT to the strip with bilinear interpolation across
the neighboring CCT and raw G/M grid points. The CCT-axis ratio is calculated
directly in Kelvin while raw G/M remains linear:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.white_lut 4500 75 \
  --intensity-percent 100
```

The default LUT is `config/white/white-lut.json`. Values outside its measured
CCT/G-M range are rejected unless `--clamp` is passed. Use `--dry-run` to print
the interpolated linear RGBWW command without controlling ESPHome. This is an
explicit light-on control command and intentionally leaves the strip at the
requested output; use `camera_based_rgbww_optimizer.control.all_off` or set
`--intensity-percent 0` to turn it off.

Use model-first matching in camera-observed color space, then add sparse
LUT/residual correction only where real captures show systematic error. If CCT
calibration measurements point to a better color calibration method, update the
strategy to follow the measured evidence.

## Validation

Run:

```bash
.venv/bin/python -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

## References

- [SAGE LED color-mixing reference (PDF; DOI: 10.1177/14771535211058096)](https://journals.sagepub.com/doi/pdf/10.1177/14771535211058096)
- [NIST: Practical Use and Calculation of CCT and Duv](https://www.nist.gov/publications/practical-use-and-calculation-cct-and-duv)
