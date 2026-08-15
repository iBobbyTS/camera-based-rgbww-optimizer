# PLAN — GUIDE8 Ray H120/S100 emission/exposure diagnostic

## Outcome

Implement and execute the single Ray-only diagnostic
`GUIDE8_RAY_H120_S100_EMISSION_EXPOSURE_DIAG_V1`, then follow only its frozen
E-A..E-G branch. This is a diagnostic run with `formal=0`, not a solver or color
observation.

## Frozen scientific contract

- Preserve the failed GUIDE7 first-frame measurement root as
  `reference_observation_missing_at_historical_shutter`; solver attempts remain 0.
- Control: reset600, D=H120/S50 120 s, A=H120/S100 120 s,
  C=H300/S100 120 s, capture C at `1/2500`; invalid control stops as E-A.
- Dark: second reset600 while both sources remain off, capture one diagnostic dark
  at `1/250`; a valid/bright observation stops as E-B.
- H120 ladder: D120, A120, Q=H120/S100 120 s, keep Q continuously on, capture
  `1/5000, 1/4000, 1/3200, 1/2500, 1/2000, 1/1600, 1/1250,
  1/1000, 1/800, 1/640, 1/500, 1/400, 1/320, 1/250`.
- Stop on the first adjacent quality-valid, MakerNote-valid pair whose nominal
  exposure ratio is `<=1.25` and whose shape passes the existing P1 evaluator:
  `raw_response_candidate.evaluate_response_model` over the two retained
  patch-statistics reports with the frozen P1 repeatability reports, identity
  response (`a=b=0`), and every required 58 feature at `<=3.0` repeatability sigma.
  Ladder neighbors whose ratio is `>1.25` cannot form a legal pair. Do not add a
  direct norm, new threshold or covariance. Select the faster shutter. Only
  near-noise-only permits continuing to a slower shutter. Other
  quality/evidence/isolation failures stop immediately.
- Physical cap 16; formal 0; dark 1; ambient subtraction 0; retry 0; strip zero
  throughout; final all-off/zero required.
- No observer, feature, threshold, statistic, covariance, coverage or frame-selection
  changes. No strip probe, Jacobian, solver, grid, boundary, Gate-6, P8 or LUT work.

## Implementation boundary

Reuse only the existing owners:

- `p7_thermal_diagnostics.py`: exact diagnostic spec and policy schema.
- `measure_p7_thermal_diagnostics.py`: direct Ray diagnostic execution and early stop.
- `analyze_p7_thermal_diagnostics.py`: immutable derived classification/policy output,
  recording the P1 evaluator source hash and frozen repeatability evidence identity.
- `tests/test_p7_direct_r6.py`: real behavior tests for control stop, dark stop,
  near-noise continuation, valid-pair stop, non-near-noise stop, caps and cleanup.

No new service, runtime, registry, release, lineage, stage gate or readiness layer.

## Validation and execution

1. Run focused GUIDE8 behavior tests and the existing direct-path module suite once.
2. Run compile/static text checks and one bounded code review.
3. Commit a clean checkpoint including GUIDE8 docs and tracked plan/evidence.
4. Execute the Ray-only diagnostic without another Human authorization request,
   because root `AGENTS.md` directly covers bounded light/camera operations.
5. For a >10 minute live run, perform three 60-second liveness checks, create one
   appropriately timed automation, then end only after the automation exists.
6. On completion, delete the automation, analyze exactly once and continue E-C/E-D
   automatically; stop only at the explicit Human/Advisor gates defined by GUIDE8.
