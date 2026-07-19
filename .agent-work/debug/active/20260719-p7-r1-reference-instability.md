# P7-R1 reference and strip repeatability instability

## Completed evidence

- Formal run: `/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/p7-r1-20260719-091000-terminal-retry1`.
- Acquisition completed `82 logical / 80 formal / 105 physical CR3`, with `30 Ray / 50 strip / 2 ambient`, eight exposure caches consuming 31 auto-exposure CR3, and zero weak reacquire.
- All 82 retained CR3 are non-empty; selected attempt ownership is unique; source/readback audit passes; retained NPY count is zero.
- Python cleanup, shell cleanup, child exit, shell-cleanup exit, and wrapper exit all pass with code zero.
- `analysis.json` SHA-256: `ac5630e26180dc9f288eacb1ff0f8352e9acc6f9f0ea4a2e857ff3552eaf243f`.
- Candidate SHA-256: `755bbe775cf7cfe4ef6d01751aca2ea2e7b3a2d61fbc05f19bca087f47609a01`; status remains `calibrated_waiting_for_planner`, `formal_capture_eligible=false`.

## Analyzer result

- Top-level branch: `uncertainty_unresolved`; Ray failure branch: `R-REFERENCE-UNSTABLE`; `reference_epoch_shift=false`.
- Ray A/B compatibility fails for all three states: H0/S0 score `51.97 > 9.51`, H120/S100 `29.25 > 9.48`, H300/S100 `17.81 > 9.63`.
- Within-block Ray trend exceeds the frozen limit 4.0 in both blocks for H0/S0 and H120/S100, and in block B for H300/S100. H120/S100 and H300/S100 also exceed the single-frame variance dominance limit.
- All five strip commands have `uncertainty_unresolved` within-command audits. Four fail block-center stability; the 3072 relaxed neutral passes block-center stability but still has block-B trend `7.71 > 4.0`.
- Synthetic joint coverage itself passes all regions with no failed region. This does not override the measured reference/repeatability failure.

## Frozen branch

Do not adjust trend thresholds, covariance, guards, 58-feature space, or the candidate; do not rerun R1 or start sentinel-v2. Planner must review whether the chronology reflects thermal/reference drift, camera/exposure behavior, or another epoch/source effect. Advisor escalation follows PLAN only if Planner determines the existing architecture or measurement model must change.
