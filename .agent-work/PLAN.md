# PLAN — GUIDE6 S-MEASUREMENT strip exposure qualification

## Current disposition

- `device_health = normal`
- `historical_183_8_strip_baseline = invalid_cross_source_contamination`
- The two retained GUIDE6 roots are `historical_only_not_scientific_input`.
- `current_F1 = strip_reference_unobservable_under_unqualified_historical_shutter`
- `human_physical_gate = resolved`
- `science_delta = none`
- `next_branch = GUIDE6_S_MEASUREMENT_strip_exposure_qualification`

## Next bounded experiment

- Experiment ID: `GUIDE6_S_MEASUREMENT_STRIP_EXPOSURE_QUALIFICATION_V1`.
- Source: strip only; verify Ray readback intensity `0` before every capture.
- Exact tested command: `CW518 / WW0 / R0 / G4095 / B0`.
- History: `reset600 -> D120 -> A120 -> tested120`; keep tested output on
  through the shutter ladder.
- Formal/ambient/solver/probe: `0 / 0 / prohibited / prohibited`.
- Ladder: `1/1600, 1/1250, 1/1000, 1/800, 1/640, 1/500, 1/400,
  1/320, 1/250`.
- Continue only after `near_noise_only`. Stop on clipping, nonfinite,
  source-isolation failure, or any other quality/evidence failure.
- Qualify the first adjacent pair that is 58/58 valid, unclipped, and compatible
  under the frozen exposure-normalized shape evaluator. Select the faster member;
  the slower member is guard-only.
- Do not subtract ambient or change observer, features, thresholds, covariance,
  coverage, or frame selection.
- If no legal pair exists through `1/250`, classify
  `no_legal_strip_exposure_window` and enter `ADVISOR_GATE_REQUIRED`.

This PLAN prepares the executable direct spec and tests only. Device work is not
part of the current correction task.
