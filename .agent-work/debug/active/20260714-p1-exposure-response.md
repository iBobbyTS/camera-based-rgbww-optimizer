# P1 Exposure Response And Strip Shutter Interaction

## Evidence

- Formal provenance-bearing P1 run: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6`.
  - Completed `31/31` CR3 captures and reports; no `.npy`, no failure, Python and shell cleanup both succeeded.
  - The `0.5x, 1x, 1.5x` brackets resolved to Ray `1/800, 1/400, 1/250` and strip `1/160, 1/80, 1/50`.
  - No bracket plane clipped at `1.5x`, but the P95 absolute relative residual was Ray `1.458%` and strip `1.133%`, versus P95 paired-repeat CV of `0.0626%` and `0.1432%`.
  - All three occurrences of each shutter were internally stable, so the discrepancy is systematic rather than an isolated capture or heat drift.
- Exposure diagnostic: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-035100-p1-exposure-diagnostic-v7`.
  - Completed `27/27` CR3 captures and reports; no `.npy`, no failure, Python and shell cleanup both succeeded.
  - The `0.8x, 1x, 1.25x` brackets resolved to Ray `1/500, 1/400, 1/320` and strip `1/100, 1/80, 1/60`.
  - Relative to the strip `1/80` median, all three strip `1/60` captures were about `-4.64%`; Ray at `1/500` was about `-1.00%`, and Ray at `1/320` about `+0.39%`.
- Historical intensity correction: the v6 P1 runner and v7 diagnostic runner labeled their Ray commands as percentages but passed those values through the raw OpenAPI `intensity` argument. Their planned `100%` and `10%` Ray values therefore commanded raw `100` and `10` (about `10%` and `1%`), respectively. This invalidates their intended absolute Ray-output baseline, but not the within-source shutter-ratio evidence; their Ray command remained constant within each run. White LUT and endpoint runners already used `intensity_percent` and are unaffected.
- The active firmware configuration specifies five ESP32 LEDC outputs at `19531Hz`. The anchor strip command owns `cw=4095`, so the large `1/60` strip effect is not adequately explained by ordinary low-frequency PWM phase sampling of the dominant channel.
- Recomputing both runs from saved patch reports shows ambient subtraction changes the median signal by at most `0.000063%`; it cannot explain the observed `0.4%..4.6%` shutter effects. The shared `1/400` Ray and `1/80` strip medians agree between v6 and v7, so ordinary session/thermal drift is also not the primary explanation.
- The effect is nearly a uniform scalar over patches and CFA planes. In v7, strip `1/60` relative to `1/80` is about `-5.59%` for every plane, with only about `0.23` percentage points between the 10th and 90th feature percentiles. The `0.8x` condition is about `-1%` for both Ray and strip. This rules out a color-specific ROI issue but does not by itself separate camera shutter timing from strip output at `1/60`.

## Decision

P1 takes PLAN.md section 7.5 branch D:

- Do not set observer thresholds.
- Do not enter P2.
- Do not treat v6 as a P1 pass even though its source isolation, metadata, cleanup, and G1/G2 evidence are complete.
- Do not use v6/v7 as a valid reference-intensity P1 baseline; rerun any future P1 or branch-D hardware acquisition only after the percentage-call fix.

## Next Offline Work

1. Compare the saved v6/v7 raw per-plane distributions before and after ambient subtraction to separate camera shutter response from source/power response.
2. Verify whether the per-second deviation correlates with the actual shutter choice rather than the requested bracket factor, source, or capture order.
3. Design a bounded future hardware diagnostic only after the offline result identifies a discriminating change. Candidate changes are a fixed-shutter temporal repeat, a camera mode/shutter-timing cross-check, or a controlled strip electrical/power test. Do not start this diagnostic after 05:00 local time.

## Future Hardware Diagnostic Contract

Run only during a new pre-05:00 window and only after the current raw reports are retained unchanged.

1. Use a lower Ray intensity and a lower strip command so both sources can be captured at the same four shutters `1/100`, `1/80`, `1/60`, and `1/50` without clipping at ISO 100 / f4. Capture six frames per shutter with the source continuously on after a documented warm-up; the symmetric eight-step order contains each shutter twice and the default three cycles therefore produces six observations. Do not use the P1 off/on cadence for this shutter-timing diagnosis.
2. Execute the exact shutter order `1/80, 1/60, 1/100, 1/50, 1/50, 1/100, 1/60, 1/80` for each source. Record actual configured shutter, source command, capture monotonic time, optical black levels, and per-plane raw plus ambient-subtracted statistics.
3. Branch on the result:
   - Both sources reproduce the same shutter signature: investigate camera timing, anti-flicker/shutter mode, and camera-side exposure metadata before changing strip firmware.
   - Only strip reproduces it: capture the same strip command at a second reduced power level and inspect DC supply/driver ripple or load dependence; do not attribute it to the configured 19531Hz LEDC clock without evidence.
   - Neither reproduces it with continuous-on capture: the P1 off/on/settle protocol is interacting with source thermal state; redesign the P1 timing and repeat the complete formal run.
   - Only individual CFA planes or patches reproduce it: retain the diagnostics, classify clipping/noise/ROI causes, and follow PLAN.md 7.5-C rather than broadening a global threshold.
