# White LUT repeatability and strict anchor validation

## Scope

- Hardware work is explicitly authorized for the camera, Ray120c, and ESPHome strip.
- Measure full-brightness Ray and strip repeatability before choosing CCT/Duv goals.
- Tune and validate only `1800,3200,5600,20000K x GM 0,100,200` before relaunching the full 14x5 grid.
- Every hardware runner must keep Ray and strip mutually exclusive and have Python plus shell shutdown guards.

## Confirmed observations

- Manual 1800K captures made with the completed 14x5 LUT did not reproduce the calibration result.
- Manual strip-minus-Ray white-patch errors at GM 0/100/200 were respectively `+30.76K/+0.006394`, `+12.02K/+0.010868`, and `+29.67K/+0.007231 Duv`.
- Five non-black neutral patches agreed on the positive Duv direction, and the white patch was not clipped.
- The current defaults are `10K` CCT and `0.01` Duv. The Duv threshold is visibly too loose.
- Prior same-command samples inside one calibration run had P90 repeatability of `5.31K` and `5.22e-5 Duv`, excluding exposure-warning outliers.

## Current hypothesis

The optimizer accepts visibly different chromaticities because Duv is underweighted by an overly loose goal. End-to-end repeatability must be measured after independent source switching and exposure setup before selecting a tighter but achievable threshold and iteration budget.

## Next diagnostic

1. Confirm all three devices and both shutdown paths.
2. Repeatedly capture representative full-brightness Ray and strip outputs with fixed per-source exposures.
3. Derive robust within-source CCT/Duv spreads and use a multiple of that noise floor as the optimization goal.

## Measured repeatability

- Six representative targets, two sources, five power-cycled captures per source completed at `/Volumes/4T/temp/rgbww-optimizer/white-repeatability/20260712-005125`.
- Worst combined Ray/strip Duv sigma was `4.95e-5`; three sigma was `1.48e-4`.
- Worst combined CCT sigma was `40.28K` at the camera-observed high-CCT reference; three sigma was `120.84K`.
- The selected goal is `<0.0005 Duv` plus a dynamic CCT tolerance of at least `25K` or the Kelvin equivalent of `1 mired`.

## Implemented correction

- Feedback budget increased from 10 to 16 rounds.
- Added an optional previous-LUT seed and a white-patch linear camera-RGB cone seed.
- Previous measured starts are preferred when their strict normalized score is at most 4; otherwise the cone model starts first.
- Failed local attempts may restart with the endpoint-biased or model-selected full-scale channel active.
- Attempt indices are included in filenames to prevent gphoto2 overwrite prompts.

## Hardware verification

- Strict 12-point commands were assembled at `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/strict-anchor-seed-20260712.json`.
- Independent verification completed all 12 targets at `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/strict-anchor-verification-20260712-021543`.
- Nine targets passed on the first strip capture; three converged through feedback.
- The slowest target, `20000K/GM100`, passed after 10 feedback rounds within the 16-round budget.
- Full suite: 140 tests passed.

## Cross-day top-10 recheck

- Rechecked the ten highest previous `goal_score` nodes without optimization at `tmp/white-top10-recheck/20260712-232005`.
- All ten Ray controls read back the requested CCT, raw G/M, and full intensity. The test completed with 20 retained CR3 files, no retained NPY files, and successful shell-level shutdown of both lights.
- Five of ten nodes remained inside the strict goal. The five outside were `14000/130` (goal `2.150`), `3200/200` (`1.617`), `8000/130` (`1.182`), `2700/100` (`1.078`), and `20000/200` (`1.078`).
- Same-source cross-day weighted 24-patch RMSE remained small: Ray median `0.19%`, max `0.26%`; strip median `0.30%`, max `0.77%`. Current strip-to-Ray weighted 24-patch RMSE remained much larger at `14.28%..15.37%`.
- Cross-day differential strip-minus-Ray movement reached `107.97K` CCT and `0.0003223` Duv. Only two targets kept both individual sources inside the short-run repeatability limits, although common-mode movement canceled at several low-CCT targets.
- `2300/130` and `2300/200` still both pass with the same strip command. Ray readback reports the requested G/M values, while its measured outputs at these low-CCT settings remain nearly identical, consistent with a Ray low-CCT gamut limit rather than stale control state.
- The current full suite passes `141/141` after adding coverage for macOS `Could not detach kernel driver` PTP recovery.

## Revised root-cause hypothesis

- The optimizer marks a command complete after one in-goal capture; it does not recapture that command for confirmation.
- The strict run left twelve nodes at `goal_score >= 0.8`, including five initial commands accepted from a single strip capture. These commands had little safety margin against cross-day differential drift.
- Short-run repeatability underestimated the long-run/cross-day error surface. The new differential drift is large enough to push boundary samples outside the same threshold without a major hardware color change.
- Feedback optimizes and stops on white-patch CCT/Duv only. The weighted chart comparison is merely a secondary sample-sort key and is not an acceptance constraint, so matching the white chromaticity cannot guarantee Ray-like rendering of colored surfaces.

## Recommended next correction

1. Keep the public validation limits unchanged, but optimize to a smaller internal target such as `goal_score <= 0.5`.
2. Require two independently captured in-goal samples of the selected command before marking a node complete.
3. Define an explicit weighted color-chart acceptance or optimization term if the intended goal includes colored-surface rendering, not only white-point matching.
4. Add a final verification-only pass after the full grid so thermal/order effects are measured separately from optimization.

## Off/on refinement verification

- A 2-to-120-second stability run showed the same strip command moving from
  `9708.53K/-0.003502 Duv` at 2 seconds to `9867.37K/-0.002932 Duv` at 120
  seconds. The original confirmation path also changed non-zero strip commands
  without first recreating the saved-LUT off/on state.
- Confirmation now turns all five strip channels off for one second, reapplies
  the candidate for 60 seconds, and requires two captures inside the strict
  internal goal. A failed confirmation rebuilds the Jacobian from that settled
  state and drops older transient samples from the active secant window.
- The initial five failed nodes (`14000/130`, `3200/200`, `8000/130`,
  `2700/100`, and `20000/200`) all completed with two off/on confirmations.
- The first ten-point verification exposed four additional boundary nodes:
  `2300/200`, `2300/130`, `14000/0`, and `2300/70`.
- `2300/70` reproduced a cold/hot secant failure: predicted scores were
  `0.158..0.226`, while repeated measurements remained `2.145..2.365`.
  Feedback now treats two consecutive material secant prediction misses as a
  stale thermal base, rebuilds the local Jacobian, and records the rebase reason
  as `repeated_secant_prediction_miss`.
- The repaired `2300/70` run triggered that rebase, then confirmed at goal
  scores `0.542` and `0.545`. The other three boundary nodes also completed
  two off/on confirmations.
- The merged 70-point artifact is
  `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`.
- Final independent verification at
  `tmp/white-off-cycle-final-recheck-v2/20260713-024518/white-top10-recheck.json`
  passed all original ten high-risk nodes after independent Ray/strip switching
  and a 60-second strip settle. The other 60 grid nodes were not independently
  repeated in this focused pass.
