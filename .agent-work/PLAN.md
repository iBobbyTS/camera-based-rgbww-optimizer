# PLAN — GUIDE7 2048 stability-first diagnostic

## Accepted offline correction

- Both F2 roots are accepted long-block reference failures.
- Classification: `reproducible_cumulative_block_history_shift_with_locally_reproducible_probe_differentials`.
- Immutable preregistration:
  `.agent-work/analysis-v2-f2-locally-bracketed-probes-derived.json`.
- Both roots select candidate `CW4095/WW0/R0/G4095/B0`; no parent artifact was modified.

## Accepted short endpoint result

- `GUIDE7_H120_S100_F2_CW_SHORT_ORDER_BALANCED_ENDPOINT_V1` completed 7/7.
- Ray bracket passed, but full-scale base repeatability failed.
- Classification: `S-D / H120_S100_CW_active_fullscale_fast_repeatability_unresolved`.
- This is not gamut or physical unreachability; it unlocks scale 3072 only.

## Accepted 3072 scientific result

- `GUIDE7_H120_S100_F2_CW_SCALE3072_STABILITY_V1` completed 5/5.
- Ray bracket passed: `3.2949 < 9.5431`.
- Strip repeat 1 differed from repeats 2/3: `29.5633` and `25.9046`
  against guard `9.5614`; repeats 2/3 were compatible at `4.7387`.
- Classification: `R-UNSTABLE / scale3072_short_repeatability_unresolved`.
- This is a valid scale-relaxed scientific negative, not gamut inference.

## Exact next experiment

- ID: `GUIDE7_H120_S100_F2_CW_SCALE2048_STABILITY_V1`.
- Ray Q_before/Q_after: reset600, D120/A120/Q120, shutter `1/5000`.
- Strip command: `CW2048/WW0/R0/G2048/B0`, shutter `1/400`.
- Three reset-separated strip observations, each `reset600 -> D120 -> A120 -> tested120`.
- Budget: 2 Ray + 3 strip = 5 formal/physical, ambient 0, retry 0.
- Source isolation and final cleanup/zero are mandatory.
- Stability-first: no probe or solver candidate may run in this experiment.
- If compatible and faithful, proceed to H120/S50.
- A stable-nonfaithful or unstable 2048 outcome returns to Advisor because the
  predefined 3072/2048 scale-relaxed discrimination is then exhausted.

Keep 13-node grid, boundary, Gate-6, P8 and LUT installation locked.
