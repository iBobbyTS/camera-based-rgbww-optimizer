# PLAN — one centered GUIDE6 LC-B continuation

## Accepted F1 result

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-f1-20260818/20260818-005758-strip-1over400-fresh`
- Acquisition/analyzer: 13/13 accepted; `LC-B`;
  `H120_S100_local_controllable_but_not_yet_faithful`.
- Ray bracket and strip base anchors: pass.
- Base score: `1471.8684202769587`; best observed candidate score:
  `1468.2674910054316`.
- Best command selected as continuation center:
  `CW0 / WW0 / R377 / G4095 / B107`.
- Cleanup, final zero, source isolation and Git identity: pass.

## Exact continuation

- Experiment ID: `GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-CONTINUATION-V1`.
- Variant: `guide6-direct-target-local-h120-s100-continuation`.
- This is generation 1 and the only centered continuation permitted.
- Use the same scientific contract, strip `1/400`, Ray `1/5000`, reset600,
  D120/A120/tested120, four local probes, two base anchors, at most four solver
  candidates, and three confirmations only after a passing candidate.
- Preserve capture-level source-zero evidence, frozen 58 features, observer,
  thresholds, covariance, coverage and cleanup.
- Do not reuse either contaminated historical root and do not use `1/320` guard
  as fallback.
- If this continuation returns LC-B again, stop at
  `ADVISOR_GATE_REQUIRED_after_centered_continuation`; no second continuation.

Keep 13-node grid, boundary, Gate-6, P8 and LUT installation locked.
