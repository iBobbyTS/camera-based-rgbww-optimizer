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

Remote capture is the required backend for new formal experiments; local
gphoto2 remains available for compatibility and offline tests. Copy
`.env.example` to `.env`, set the bridge token, then use the script-owned
read-only checks (neither command captures an image or changes settings):

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote health --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote config --json
```

Direct remote capture remains available with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote capture \
  --output-dir tmp/captures/remote-camera \
  --filename-template '%Y%m%d-%H%M%S.%C'
```

`camera_remote` reads
`CAMERA_BASED_RGBWW_OPTIMIZER_REMOTE_CAMERA_BASE_URL` and
`CAMERA_BASED_RGBWW_OPTIMIZER_REMOTE_CAMERA_TOKEN` from the process environment
first and the project `.env` second. Do not source, print, or pass the token on
the command line; only the Python process reads it at actual runtime. It reads
the exact values exposed by
`GET /v1/config`, sends ISO/aperture/shutter settings in an authenticated
`POST /v1/capture`, streams the response to a temporary file, and atomically
installs the completed CR3. Omit `--iso`, `--aperture`, or `--shutter-speed` to
keep the corresponding current remote value. A `camera_busy` response is retried
as a bounded complete request. Neither local nor remote capture keeps a second
copy on the camera.

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
empirical quality thresholds automatically. The completed P1 decision uses the
identity RAW response only inside `1.0x..1.25x` of each source's auto-exposure
baseline. It keeps `R/G1/G2/B` separate because the two green planes have small
but repeatable patch/source dependence.

Measurement normalization must use the exposure duration recorded in the CR3,
not only the shutter label requested through gphoto2. Canon MakerNote
`Canon:ExposureTime` is authoritative, standard EXIF is the fallback, and the
requested shutter is a degraded fallback with explicit provenance. In retained
R6 Mark III samples, displayed `1/60` and `30` settings recorded approximately
`1/64` and `32` seconds. The shared resolver is
`camera_based_rgbww_optimizer.measurement.recorded_exposure`.

The P1 capture runner requires the external best 70-point LUT explicitly,
rather than reading the default 4x3 LUT, and plans ambient, independent
Ray/strip exposure caches, alternating paired repeats, exposure brackets,
optional flat field, and two cleanup layers. `--dry-run` performs no device
I/O and writes only `plan.json`:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
  --target-max 19661 \
  --min-shutter-speed 1/16000 \
  --linearity-factors 0.5,1,1.5 \
  --preflight-only \
  --dry-run
```

The plan freezes the camera backend, auto-exposure shutter bounds, plus the
location path and SHA-256. Use `--min-shutter-speed 1/16000` when the 100% Ray
baseline remains above the requested target at `1/8000`; the selected value
must be supported by the remote camera config. Dry-run
does not load `.env`, access the network, or call either light. Real acquisition
requires both `--execute` and `--allow-high-output`; it uses
the native Bayer exposure meter, emits JSON-only patch reports, and keeps Ray
and strip shutter caches independent. P1 fails immediately and enters cleanup
if a CR3 cannot provide recorded exposure metadata; it never continues a formal
batch on requested-shutter fallback. It must be launched through a temporary
shell wrapper with `EXIT`, `INT`, `TERM`, and `HUP` traps that run
`control.all_off --json` into the same run directory. Python `finally` uses
the same public cleanup entry point, including on capture errors. The runner
accepts an existing run directory only when it is empty, so the shell trap can
create the directory without allowing any old experiment to be reused.
Before the first capture, a native run also freezes the baseline/default LUT,
endpoints, location, code-duty curve, and observer-config hashes together with
Git state, rawpy/LibRaw, gphoto2, a redacted camera summary plus anonymous
device ID, Ray node configuration, and ESPHome device identity in `run.json`. A failed pre-capture probe is recorded
as a failed run and still executes Python cleanup.

After a completed P1 run, analyze the immutable run directory offline:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation \
  /Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/<run-id>
```

Legacy P1 runs whose patch reports were normalized by requested shutter labels
can be recomputed from their retained CR3 files without overwriting the old
`analysis.json`:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation \
  /path/to/p1-run \
  --recompute-recorded-exposure
```

This writes `analysis-recorded-exposure-v1.json`, verifies the frozen location
and observer-config hashes, and records the exposure source for every CR3. The
linearity result separates per-shutter global exposure scale from residual
patch/CFA shape because later matching permits a global brightness scale but
cannot ignore color-dependent response.

The analyzer rejects a non-complete run by default, restores each capture's
source/purpose/repeat/factor/shutter provenance from `captures.jsonl`, and
produces separate Ray/strip repeatability and exposure-linearity evidence plus
cross-context G1/G2 statistics. It deliberately does not mark P1 pass/fail or
write empirical observer thresholds; those decisions follow the branches in
`.agent-work/PLAN.md`.

When P1 reaches its broad exposure-response branch, use the separate
`measure_raw_shutter_response` runner rather than changing P1's off/on thermal
protocol. It photographs Ray and strip at the same explicit shutter sequence
while each source remains on continuously after a warm-up. The dry run is safe
and device-free; real runs require `--execute --allow-device-control` and the
dedicated `tmp/run-raw-shutter-response.zsh` shell wrapper:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_raw_shutter_response \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --dry-run
```

After a complete run, call
`camera_based_rgbww_optimizer.optimization.measure_raw_shutter_response.analyze_raw_shutter_response_run`
from Python. It reports per-source, per-shutter ratios against `1/80`, capture
duration distributions from the monotonic timestamps, and the recorded source-on
commands. It does not update observer thresholds or decide which device caused a
response difference.

Do not run P1-D merely because legacy shutter-normalized analysis failed. First
recompute retained CR3 files with recorded exposure metadata. P1-D remains a
diagnostic branch only when corrected evidence cannot distinguish camera response
from source response. Its conservative default Ray intensity is `1%`; every real
run still requires a clipping-safe preflight and the shell cleanup wrapper.

If P1-D shows the same shutter-dependent shape residual for Ray and strip, fit a
candidate-only monotonic response model from the completed full P1 run:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_raw_response_candidate \
  /Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/<training-run>
```

The output `raw-response-candidate.json` compares the identity model, the fitted
`g(y)=y*(1+a*y+b*y^2)` candidate, and an uncorrected lower exposure envelope.
It requires recorded exposure provenance, guarantees `g(0)=0` and a positive
derivative on `0..1`, records the observed training range, and rejects use outside
that range. This artifact never changes retained RAW reports or
`config/camera/raw-observer.json`. A complete P1 run from another natural day,
with the same remote backend and frozen inputs, is mandatory holdout evidence
before any correction schema may be proposed.

Evaluate the frozen coefficients on that independent run; do not omit
`--candidate`, because the default mode fits a new training candidate:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_raw_response_candidate \
  /Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/<holdout-run> \
  --candidate /Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/<training-run>/raw-response-candidate.json \
  --candidate-sha256 <frozen-sha256>
```

This verifies the frozen candidate file hash, rejects the original training input
by evidence hash, and refuses to apply
the model when holdout linearity signals exceed its frozen application range.
For a PLAN 7.5-B boundary-only confirmation run, add
`--repeatability-run /path/to/completed-full-p1`; only paired-repeat noise is
borrowed from that full run, while all boundary linearity centers remain from the
new run. The location hashes must match.

Generate a bounded 15-capture confirmation plan with two factors and three
repeats per source using `measure_raw_observer_validation
--boundary-confirmation-only --linearity-factors 1,1.25
--linearity-repeats 3`. This mode still captures ambient and independent Ray/strip
auto-exposure baselines, retains the normal off/on isolation protocol, records
`paired_repeats=0`, and requires the same real-run wrapper and cleanup safeguards.
The 2026-07-16 boundary run passed with identity RAW: the strip maximum was
`2.903` repeatability sigma. The frozen polynomial candidate was rejected for
installation because it raised that maximum to `3.182` sigma despite improving
the aggregate P95. `config/camera/raw-observer.json` therefore records identity,
the bounded envelope, a `0.05` near-noise cutoff, and `combine_green=false`.

## Five-Channel Chart Response Basis

After Gate-1, build the P2 plan without device access:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_chart_response_basis \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
  --dry-run
```

The immutable plan contains 58 captures: one ambient, ten channel-specific
protection/weak auto-exposure baselines, one 5600K/GM100 anchor baseline, 45
formal off/on captures for five channels at target codes 1024/2048/4095, and
one anchor check after state 8. It rejects non-remote execution, a non-identity
RAW observer, combined green, or an observer config without the validated
`1.0x..1.25x` envelope. Real acquisition must use
`tmp/run-chart-response-basis.zsh`, which adds an independent shell trap to the
shared Python cleanup.

After a completed run, fit the three empirical bases offline:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_chart_response_basis \
  /Volumes/4T/temp/rgbww-optimizer/chart-response-basis/<run-id>
```

The analysis uses only accepted `R/G1/G2/B` observations, robustly centers the
three repeats, divides each column by its target code fraction, and reports SVD,
rank, condition number, channel-column angles, bootstrap intervals, feature
weights, rejected observations, cross-level shape differences, repeatability,
and anchor shape drift. A rejected low-signal cell may borrow the nearest
accepted level from the same channel at weight `0.25` for matrix diagnostics;
features with no accepted level are censored zero at weight `0`. Neither enters
the direct cross-level comparison.

The completed P2 run at
`/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935`
has 58/58 recorded-exposure captures and three rank-5 bases with condition
numbers `121.68..125.30`. All five channels have repeatable level-dependent
shape, so Stage 2 selected B-B with piecewise-linear normalized columns at
codes 1024/2048/4095.

Build the P3 held-out mixture plan without device access:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_chart_basis_mixtures \
  --basis-analysis /Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
  --dry-run
```

The P3 plan freezes 24 unique commands across dominant-channel, white+RGB,
high-load, LUT-nearby, and low/mid Latin-hypercube categories. Each command has
two independent off/on captures; protection/weak exposure baselines and anchor
checks bring the complete plan to 55 captures. Real acquisition must use
`tmp/run-chart-basis-mixtures.zsh` for the independent shell cleanup trap.

Analyze a completed P3 run only against the frozen P2 artifact and hash:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_chart_basis_validation \
  /Volumes/4T/temp/rgbww-optimizer/chart-basis-mixtures/<run-id> \
  --basis-analysis /Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json \
  --basis-sha256 <frozen-sha256>
```

The report separates absolute response from global-scale-removed shape error,
combines P2 basis-center and P3 repeat-center uncertainty, and summarizes
residuals by category, active-set size, load, order, neutral/chromatic patches,
and CFA plane. It leaves the M-A..M-E decision to Gate-2.

The completed P3 run selected M-E. No held-out mixture had at least 80% of
features within two combined sigmas; sample shape P95 had a 6.43% median and
62.77% maximum, while the final anchor shape drift was only 0.281% P95. The
error was broad and not load-correlated, so no global load or interaction model
is installed. The empirical basis is seed-only for the P4 C-F local camera
feedback path; the existing white LUT and white-point feedback remain valid.

P4 freezes its 4x3 pilot contract in
`config/camera/cct-multipatch-pilot.json`. Build the offline plan with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_cct_multipatch_pilot \
  --dry-run \
  --run-name p4-offline-preflight
```

The dry-run verifies the frozen P2 basis hash, latest location hash, identity
RAW observer, best external 70-point LUT, 12 targets, and the fixed 92-feature
neutral/training/holdout split. It records the seven formal A/B captures per
target and both cleanup requirements without loading remote credentials or
creating a camera backend. Real P4 acquisition requires
`--execute --allow-high-output --camera-backend remote` and must run through
`tmp/run-cct-multipatch-pilot.zsh`; the runner rechecks frozen input hashes,
records remote provenance and failures, and has Python cleanup in addition to
the wrapper's shell trap. The multipatch objective is lexicographic: neutral chroma and the
existing CCT/Duv limits are hard gates before training color, holdout color,
and regularization can affect candidate ranking. A candidate must also rank
strictly better than the same-run baseline center before it is confirmed. If
feedback cannot improve a point, the runner still captures two 60-second
settled final-verification samples for the Gate-3 failure branch.

After the wrapper has exited and both cleanup files exist, analyze the complete
pilot with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_cct_multipatch_pilot \
  /Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/<run-id>
```

The analyzer refuses incomplete runs, `failure.json`, missing/empty RAW files,
non-recorded exposure, retained `.npy`, or either failed cleanup layer. It uses
the confirmed settled pair, or the explicit final-verification pair for a
non-converged point, and reports baseline-to-candidate training/holdout
mean/P90/worst improvement against same-run three-sigma repeatability. It also
reports white-point non-degradation, hard-gate failures, command continuity and
RGB use. It produces Gate-3 evidence but never selects C-A..C-F or expands the
grid automatically.

The completed P4 retry9 produced 12 target rows: seven evaluable and five
`measurement_unreachable`. On the evaluable subset, all training and holdout
mean/P90/maximum improvements exceeded same-run three-sigma repeatability and
white points were non-worse. However, an interior `5600K/GM100` target was not
observable under the frozen RAW envelope, and three GM0 targets failed the
settled neutral hard gate. Gate 3 therefore stopped before P5: keep the current
external white-only 70-point candidate, use multipatch as diagnostics only,
do not overwrite the default LUT, and proceed to Ray-only HSI
characterization.

If a P4 RAW has only near-noise quality failures while valid-pixel,
nonfinite, and clipping gates all pass, the runner reacquires that exact
source/command once at `1.25x` exposure, inside the P1-validated envelope.
The native values remain exposure-normalized. It does not widen observer
thresholds, censor the feature, or retry pixel-count/clipping/nonfinite and
mixed-quality failures; those still fail the run and enter both cleanup
layers. If a Ray reference remains a pure weak-signal rejection after the
single `1.25x` reacquisition, or the strip cannot establish the three-sample
baseline under the same bound, the runner records that target as
`measurement_unreachable` with both capture IDs and the rejected features,
then continues the frozen 12-target acquisition. Such a point is excluded from
numerical aggregates, makes C-A impossible, and is reported as C-D evidence;
it is not treated as a successful optimization or used to widen the validated
exposure envelope.
During local feedback, a pure weak-signal rejection after the bounded
reacquisition invalidates that candidate only. The feedback loop records the
rejection and tries `0.5` and `0.25` trust-region backtracks from the current
valid command; rejected observations never enter samples or update the
Jacobian. If all backtracks fail, the point keeps its best valid command and
uses the existing settled final-verification path. A rejected confirmation is
handled as a failed confirmation and may trigger thermal rebase. Setup/probe
or final-verification observations that remain unmeasurable make the target
`measurement_unreachable`, while mixed quality failures still fail the run.

## Ray HSI Manifold

Stage 5 first characterizes Ray120c itself; it does not control or fit the
RGBWW strip. Build the immutable P6 plan offline with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold \
  --dry-run \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json
```

The plan contains 73 unique base states and 106 recorded captures: the 12x6
HSI Hue/SAT grid at INT100, SAT=0 repeats at six primary hues with five total
Hue-0 anchors, repeated primary HSI SAT100 endpoints, RGB R/Y/G/C/B/M pairs,
and one ambient frame. Every unique Ray state auto-exposes independently;
repeat captures reuse only that exact state's shutter cache. Every HSI or RGB
command is followed by exact mode readback before the 60-second settled
capture. The strip is explicitly turned off before every frame, and both
devices are still shut down by Python cleanup plus the shell trap.

Real acquisition must use a fresh run directory and the wrapper:

```bash
tmp/run-ray-hsi-manifold.zsh \
  /Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/<run-id>
```

After a completed run with both cleanup files, analyze it offline with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.measurement.ray_hsi_analysis \
  /Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/<run-id>
```

Only features accepted by the frozen native-Bayer observer quality gate enter
the numerical comparison. The analyzer reports SAT=0 Hue dependence,
scale-removed HSI/RGB endpoint differences, both pooled-zero and periodic
Hue-dependent-zero affine manifold candidates, radial monotonicity, and the
330-to-0 periodic edge. It does not select Gate 5 or implement strip HSI.

P6 retry1 completed all 106 captures with recorded exposure, zero retained
`.npy`, exact readback for all 105 Ray states, and successful Python/shell
cleanup. Gate 5 selected `full_periodic_2d_HB`. SAT=0 has no repeatable
scale-removed Hue-dependent shape, so it uses one pooled color direction while
preserving the measured Hue-dependent brightness scale. HSI and RGB endpoints
are not direction-equivalent and remain separate. The affine SAT model failed
broadly rather than at isolated points, while radial progress stayed monotonic
for all 12 hues; the frozen Stage-6 target is therefore the measured periodic
2D Hue/SAT surface in `config/hsi/ray-hsi-manifold.json`, initially using
piecewise-linear interpolation without overshoot.

Stage 6 P7 is deliberately staged. Before any new device call, generate
`config/hsi/strip-hsi-uncertainty.json` from the frozen P6 Ray repeats, the two
natural-day P1 strip repeat groups, and P6 interpolation cross-validation. The
model keeps the exact ordered 58-feature native-Bayer vector, normalizes each
observation to unit shape, and uses a positive CFA-plane block-isotropic
diagonal covariance. Match covariance is Ray repeatability plus the strip
repeatability floor plus the target's interpolation component; no additional
camera-noise term is added. Fixed-seed Monte Carlo propagates this covariance
through the actual Ray manifold inverse, calibrates one joint 99.73% score, and
freezes a bootstrap-derived guarded acceptance limit before measurement.
SAT=0 uses only SAT and orthogonal outputs and never invents a Hue gate.

The formal uncertainty calculation is a long, offline-only task:

```bash
tmp/run-hsi-uncertainty.zsh tmp/hsi-uncertainty-formal/<run-id> --workers 12
```

Phase A does not load `.env`, construct a camera backend, or call Ray/ESPHome.
Its Python and shell safety records therefore prove that no source was touched;
real P7 acquisition continues to use `tmp/run-strip-hsi-pilot.zsh` and its two
actual all-off layers. After the frozen artifact exists, build only the four
sentinel targets first:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_strip_hsi_pilot \
  --dry-run \
  --policy-version v1 \
  --target-set sentinel \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json
```

The sentinel set is `H0/S0`, `H120/S100`, `H120/S50`, and `H300/S100`.
Only the frozen automatic release conditions may unlock the remaining nine
points. Each real session photographs three pre Ray anchors and one post anchor
with exact readback. Ordinary points require three independent 60-second
off/on confirmations; boundary, scale-relaxed, and holdout points require five.
Full-scale candidates keep one active channel at `4095`. A non-faithful point
receives `3072`, then if needed `2048`, diagnostics without changing Ray
INT100; this can establish only a full-scale policy effect, never physical
gamut. The scoped boundary name is `s_exact_max_int100_fullscale`.

The first four-point sentinel completed mechanically but is now diagnostic-only:
its v1 nonlinear coordinate gate amplified repeatability and its SAT100 reference
region collapsed to a zero scale that had been hidden by a `1e-12` floor. P7-R0
therefore keeps `config/hsi/strip-hsi-uncertainty.json` immutable for legacy
replay and introduces `config/hsi/strip-hsi-policy-v2-waiting.json`. The v2
artifact is deliberately `waiting_for_targeted_measurement` and
`formal_capture_eligible=false`; it cannot authorize a capture.

Policy v2 separates three outputs. `hsi_coordinate_equivalent` uses a signed,
unclipped target-local tangent (SAT100 is one-sided from the measured SAT95
node; SAT0 has no Hue dimension). `observer_equivalent` independently evaluates
the direct ordered 58-feature residual. `color_rendering_residual` retains the
directional tangent-orthogonal vector plus per-plane/per-patch summaries; it is
reported and used as a solver tie-break without being folded back into the HSI
coordinate hard gate. Reference center compatibility, reference pre/post
repeatability, and confirmation spread all operate directly in unit-shape
58-feature space with CFA-plane block-isotropic diagonal covariance.

P7-R0C keeps the legacy config/hash intact and uses
`config/hsi/strip-hsi-pilot-v2.json` for the new runner contract. The v2
formal path requires explicit policy dispatch, rejects waiting/candidate
artifacts, calls the signed v2 evaluator and two-distinct-face solver, and
audits logical observations separately from physical CR3 files. Planner caps
are `54/67` for ordinary targets and `62/75` for n=5 targets. Primary and both
backtracks each consume a feedback attempt, rebases reserve all four probes,
and budget exhaustion returns structured evidence with the best valid sample.
Once a confirmation group starts, every measurable n=3/n=5 capture is retained
before the group decision. If no candidate was confirmed, the solver uses an
unspent one of the two declared confirmation groups to verify the best-valid
command; it may never add a third or hidden group. Across distinct-face starts,
any confirmed result is selected before an unconfirmed lower-error sample.

The formal analyzer requires explicit policy dispatch. V1 remains
legacy-replay-only; v2 validates the frozen/formal-eligible policy hash,
multiseed selection, per-start and target budgets, 12 three-frame reference
anchors, confirmation spread, and the separate coordinate/observer/rendering
layers. Combined sentinel/remaining analysis rejects mixed policy versions or
hashes.

Offline P7-R0E commands are:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.measurement.hsi_policy_v2
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_strip_hsi_pilot \
  <legacy-sentinel-run> --policy-version v1
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_hsi_policy_v2_replay \
  <legacy-sentinel-run> --policy-v2 config/hsi/strip-hsi-policy-v2-waiting.json
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_hsi_reference_repeatability \
  --dry-run --policy-v2 config/hsi/strip-hsi-policy-v2-waiting.json
```

The last command only emits the draft named-experiment schema
`p7_targeted_reference_repeatability_v2`: 30 formal Ray measurements, 50
formal strip measurements, and two ambient frames in the fixed order ambient,
Ray A, strip A, strip B, Ray B, ambient. Dry-run does not load `.env`, create a
camera backend, or call a light. P7-R0E implements—but does not run—the remote
execution surface, analyzer, formal-ineligible `calibrated_waiting_for_planner`
finalizer, and `tmp/run-hsi-reference-repeatability.zsh` dual-cleanup wrapper.
Every P7-R1 logical row retains append-only base and optional weak-reacquire
attempt evidence, including command/readback, settling contract, CR3/report,
adapter physical count, rejected-quality provenance, and selected-attempt ID.
The analyzer reads `commands.jsonl` and `capture-attempts.jsonl`, independently
recomputes physical/auto-exposure/reacquire counters, and compares them with
`run.json`. The absolute 250-CR3 bound is Planner-frozen; the dry plan reports
`baseline_physical_range_without_weak_reacquire=82..170` and
`permitted_physical_range_with_weak_reacquire=82..250`, plus a maximum 9600
seconds of 60-second settling events for Planner review. Formal v2 and P7-R1
share one narrow validator for both off responses and the single exact source-on
readback. Formal target logical/physical counts and result status are rebuilt
from captures, samples, attempts and auto-exposure structure instead of trusting
target-row self-reports.
P7-R0E additionally requires a RAW-to-58-feature/objective replay, unique
capture ownership, exact target/attempt plan order, and frozen sub-budget caps.
Measurement rejections are not free logical observations: quality rejections
must carry non-empty capture IDs plus source/purpose/exposure/quality evidence;
only an explicit pre-capture solver-budget exhaustion record may omit capture
IDs, and it must prove no capture was attempted and retain the physical counters.
Top-level and nested exhaustion ledgers must either both be absent or be identical
non-empty mappings; any exhaustion also requires an exhausted frozen category,
`solver_budget_exhausted` start status, and no confirmed group.
The formal runner canonicalizes sparse producer exhaustion once it owns both the
start capture ledger and target physical budget: logical exhaustion uses start
counters, while physical denial uses target counters. A CR3 produced before an
adapter reports an overrun is a fatal `physical_budget_accounting_violation`, not
pre-capture exhaustion.
`EXHAUSTIBILITY_MATRIX` is keyed by stable path ID so producer finalization,
formal analysis, readiness output and tests share the same origin/scope/status/
phase-family contract. `logical.feedback_attempts` and
`logical.confirmation_groups` are production-reachable; guarded logical paths
are rejected by the public analyzer, and post-capture physical overruns are fatal
paths. Planner froze `physical.pre_capture_denial` as guarded-unreachable: the
54/67 and 62/75 equations reach the physical cap only when both start logical
caps are already full, and the solver checks the logical gate before the capture
callback. The remaining precheck stays as defense-in-depth, but runner
finalization and formal analysis reject it from completed-target evidence. No
fixture may manufacture a production success round-trip for that path.
ESPHome command acknowledgement is explicitly not device readback. The formal
entrypoints now require an independent generation-bearing `rgbww_commanded_state`
snapshot; the offline fake verifies stale generation, channel mismatch, missing
entity, and timeout failures. The firmware config is not flashed by this phase.
Before any P7-R1 execution, run the separately authorized low-output device gate
only through `tmp/run-strip-state-readback-preflight.zsh RUN_DIR`. Its frozen raw
PWM sequence is zero, `(cw,ww,r,g,b)=(8,16,24,32,48)` twice, zero, then a final
verified zero after Python all-off; every call bypasses the code-duty curve and
must advance the device generation with an exact, stable name/MAC snapshot.
The wrapper adds an independent EXIT/INT/TERM/HUP all-off trap. A missing state
entity, identity/readback drift, or unverified cleanup stops at P7-D0 and does
not authorize firmware upload, camera access, or P7-R1.
Before a rerun, the wrapper also atomically records the child exit, shell
cleanup exit, final wrapper exit, and received signal. Signal exits take
priority as `128+n`, followed by the original child failure; a cleanup-only
failure maps to `70`. Cleanup stdout and stderr remain separate, and cleanup is
run exactly once.
The execution CLI is fail-closed unless both `--allow-high-output` and the exact
`--named-experiment p7_targeted_reference_repeatability_v2` are supplied. The
long-task wrapper records adjacent running/finished state with wrapper and child
PIDs plus runner/wrapper logs, then atomically retains child, shell-cleanup,
signal, and final wrapper exit evidence. Signal `128+n` outranks child failure,
child failure outranks cleanup-only exit `70`, and cleanup runs exactly once.
The PLAN section 4.4 continuous package authorizes one exact R1 only after the
same-session D0 gate passes; this does not authorize a second R1. New sentinel,
remaining nine, boundary, holdout, and P8 remain locked.

The completed 2026-07-19 R1 run retained 82 logical captures (30 Ray, 50 strip,
two ambient) and consumed 105 physical CR3 with zero weak reacquire. Source,
readback, ownership, recorded-exposure, physical-budget, no-NPY, and Python plus
shell cleanup audits pass. The calibrated candidate remains formal-ineligible:
all three Ray states fail A/B center compatibility and measured trend gates,
and all five strip commands have unresolved within-command trend (four also
fail block-center stability). Synthetic joint coverage passes, but it cannot
override the measured `R-REFERENCE-UNSTABLE` / `uncertainty_unresolved` branch.
Do not rerun R1, relax thresholds, or enter sentinel-v2 before Planner review.

## Location Picker

Use the local Web UI to capture a preview and mark color-chart patches:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.interaction.location_picker_ui \
  --blocks 24 \
  --rows 4 \
  --cols 6
```

Use the same complete auto-exposure and location workflow through the remote
camera bridge with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.interaction.location_picker_ui \
  --camera-backend remote \
  --blocks 24 \
  --rows 4 \
  --cols 6
```

The default backend remains `local`. In remote mode, omitted ISO and aperture
values resolve to the current values reported by `/v1/config`; explicit values
must exactly match the remote choices. The RAW is still decoded and analyzed on
this machine after download.

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
  path/to/existing-history.cr3 \
  --exposure 1/20 \
  --location-config config/location/locations-20260714-211759.json \
  --output tmp/raw-observer-validation/offline/patch-statistics.json
```

Pass `--ambient-raw` and `--ambient-exposure` to normalize both captures by
exposure time before subtracting the ambient/dark observation. The report keeps
`R/G1/G2/B` separate, optionally derives `G=(G1+G2)/2`, records per-plane black
and effective white levels, and includes median, trimmed mean, MAD, variance,
pixel counts, clipping, and noise-floor diagnostics. Color-chart coordinates
are scaled from the saved location image dimensions to `raw_image_visible`,
which accounts for the one-pixel size difference in the current Canon files.

Acceptance thresholds live in `config/camera/raw-observer.json`. P1 validated
zero clipping/nonfinite tolerance, at least 29000 valid pixels per plane, and a
`0.05` near-noise fraction inside the `1.0x..1.25x` exposure envelope. Features
outside those limits must be omitted at that exposure and reacquired with the
weak-signal exposure strategy; thresholds must not be widened to retain them.
This native-mosaic path runs alongside the existing demosaiced white-patch
CCT/Duv path; it does not replace that diagnostic path.

Check a saved location file against a fresh single camera capture:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.interaction.location_checker \
  config/location/locations-20260714-211759.json \
  --camera-backend remote
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
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
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
modeling. The code-duty correction path only needs the small curve file. The
current June 6 archive was normalized from requested shutter labels and its
referenced CR3/run directories are no longer retained, so it cannot be repaired
from recorded exposure metadata. Keep the current curve for compatibility with
the already calibrated white LUT, but do not use it as absolute P2 basis or
intensity evidence. A future channel-response acquisition will record
`exposure_metadata` per capture and must replace that evidence before P2.

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
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
  --allow-high-output
```

When previous measurements have already found a useful Ray starting point, seed
the adaptive run per endpoint:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_white_endpoints \
  --output-dir tmp/white-endpoints \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
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
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
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
