# PLAN — GUIDE9 H120/S100 scale × source-age discrimination

## Active route

- GUIDE9 supersedes GUIDE7 execution branches; earlier roots remain historical evidence only.
- Execute `GUIDE9_H120_S100_SCALE_AGE_DISCRIMINATION_V1`: Ray before/after plus four independent strip cycles.
- Cycle order is 4095, 2048, 2048, 4095; each cycle is a verified 600 s all-zero reset, 120 s capture, then continuous 600 s capture.
- Shutters are Ray `1/5000` and strip `1/400`; no probes, solver, ambient, or FAST/LONG pooling.
- After one complete 10/10 acquisition, run the frozen GUIDE9 analyzer once and continue to H120/S50. No more H120/S100 face, scale, probe, solver, or centered continuation.
- 13-node grid, boundary, Gate-6, P8 and LUT remain locked.

## Accepted GUIDE9 H120/S100 result

- Acquisition completed 10/10 with quality, source isolation and cleanup pass.
- Ray bracket passed: `5.7825 < 9.5430`.
- Scale 2048 FAST/LONG repeatability passed; scale 4095 FAST passed and LONG failed (`12.7135 > 9.5616`).
- Classification: `H120_S100_operating_repeatability_unresolved_across_tested_scales`.
- Scale×age interaction score: `11.1009`; physical/thermal causation is not claimed.
- H120/S100 search is closed. Next action is `GUIDE9_H120_S50_FAST_DIRECT_BATCH1_V1`.
- Batch 1 freezes four offline-diverse commands: P2 best CW face, high-white G face, RGB-dominant R face, and the S100 continuity command. Each receives an independent reset600 and dwell120; Ray brackets the batch.

## Historical GUIDE7 record

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

## GUIDE9 H0/S0 accepted classification

- Root: `/Volumes/4T/temp/rgbww-optimizer/guide9-h0-s0-best-repeat-20260821/20260821-031503-high-white`
- Acquisition/quality/cleanup: 4/4 accepted, Ray bracket pass, strip repeatability pass, final zero and Git-clean checkpoint pass.
- Classification: `H0_S0_stable_nonfaithful`; repeatability score `3.4473695284 < 9.5630091172`; direct scores `1569.2116457297` and `1567.5080471826`.
- H0/S0 is scientifically classified. It is not a physical-gamut conclusion.

## Exact next experiment

- Execute `GUIDE9_H300_S100_FAST_DIRECT_BATCH1_V1` under FAST-DIRECT with Ray `1/2500`, strip `1/125`, reset600/D120/A120/tested120, two Ray references and four offline-selected strip candidates.
- Candidate 1 is the retained P2 H300/S100 command `CW406/WW0/R4095/G0/B1541`; the other three are bounded face-local discriminating commands.
- Cap 6 formal/6 physical, ambient 0, retry 0. Keep 13-node grid, boundary, Gate-6, P8 and LUT locked.

Keep 13-node grid, boundary, Gate-6, P8 and LUT installation locked.
