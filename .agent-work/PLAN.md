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

- Advisor corrected the prior handoff: one root had a valid H300 Q-before plus four valid strip captures and only lacked Q-after; one later root had a near-dark H300 observation without complete pre-capture Ray state evidence. This is not two established measurement failures.
- Current classification: `intermittent_H300_reference_emission_or_optical_path_dropout_unresolved`.
- Execute only `GUIDE9_RAY_H300_S100_REFERENCE_EMISSION_PATH_DIAG_V1`: two order-balanced Ray-only sessions, each with off600 and two dwell120 captures. Session 1 is H0/S0 then H300/S100; session 2 reverses the order.
- Use qualified shutters H0/S0 `1/16000` and H300/S100 `1/2500`; cap 0 formal/4 physical, ambient 0, retry 0, strip commands 0.
- Persist set response, immediate readback, post-capture readback, exact command hash, intensity and strip-zero evidence before feature extraction, including rejected captures.
- R-A permits one complete fresh H300 Batch 1. R-B/R-C close S100 and continue H300/S50. R-D stops HSI at a system-level Human physical gate.
- Never pool the incomplete root's strip frames with new Ray frames. Keep 13-node grid, boundary, Gate-6, P8 and LUT locked.
- The first completed 4/4 diagnostic occurred while the Ray was physically
  unplugged. It is retained as historical invalid-condition evidence and is not
  pooled or used for scientific classification.
- After Human restored Ray power, a fresh 4/4 diagnostic completed with full
  capture-bound state evidence, quality, cleanup and zero-state pass. Both H0
  controls and both H300 observations were individually valid; H300 failed
  repeatability at `20.6931 > 9.6326`.
- Current branch: `R-C / H300_S100_reference_repeatability_unresolved`.
  H300/S100 is closed. Execute `GUIDE9_H300_S50_FAST_DIRECT_BATCH1_V1` with
  Ray `1/4000`, strip `1/400`, four frozen P2 active-face candidates, six total
  captures, independent reset600/dwell120, no solver and no ambient.
- H300/S50 Batch 1 completed 6/6 with quality, source isolation, cleanup and
  Ray bracket pass (`3.7789 < 9.5994`). The lowest direct-score candidate is
  `CW192/WW4095/R2495/G0/B2559` at `1659.5267`. Execute two independent FAST
  repeats of that exact command to classify stable faithful, stable nonfaithful,
  or operating-repeatability unresolved.
- H300/S50 best-repeat completed 4/4. Ray bracket passed
  (`2.1517 < 9.5994`) and strip repeatability passed
  (`2.1463 < 9.6270`), while direct scores remained `1659.86/1659.25`.
  Classification: `H300_S50_stable_nonfaithful`; H300 route complete.
- Four-point sentinel is scientifically complete, but the 13-node grid remains
  locked because no chromatic Hue has a faithful endpoint. This does not trigger
  the GUIDE9 mandatory Advisor gate because H120/S25 and H300/S50 are both
  measurable and repeatable. Continue with the independent GUIDE9 white route,
  starting with the 12-point FAST-DIRECT representative validation.
- White12 engineering boundary is ready: `GUIDE9_WHITE_FAST_DIRECT_REPRESENTATIVE_12_V1`
  freezes 12 nodes from the retained 14x5 candidate, 24 Ray/strip captures,
  alternating within-node source order, per-capture reset600/dwell120, historical
  source-specific shutters, exact source isolation, and no global refit or LUT install.
- White12 completed 24/24 with quality, cleanup, source isolation and final zero.
  Only `5600K/GM200` passed; 11 nodes require direct paired local correction.
  Preserve the immutable analysis, keep the 70/70 gate locked, and generate one
  preregistered local candidate per failed node from that node's own retained
  feedback trace plus its current paired CCT/mired/Duv residual. Reacquire only
  Ray+candidate pairs; no global model refit or default LUT mutation.
- First local-Jacobian correction completed 10/10. `3200/GM100`, `5600/GM100`
  and `20000/GM100` passed. `3200/GM200` and `20000/GM200` improved to strict
  gate boundaries but remained just outside. Execute one second preregistered
  paired step for those two nodes, then move all remaining failures to bounded
  per-node probes.
- Second confirmation completed 4/4; both `3200/GM200` and `20000/GM200`
  passed all strict paired gates. Five historical-Jacobian nodes are now locally
  corrected. For the six remaining failed nodes without a retained Jacobian,
  run one bounded current-session local-probe block per node: one Ray reference,
  one base and four independent free-channel probes. Use the resulting local
  Jacobian only to preregister the next paired candidate.
- Local-probe path is ready for `1800/GM0,100,200`, `3200/GM0`, `5600/GM0`
  and `20000/GM0`: each node has one current Ray reference, one base and four
  independent free-channel probes (`±256`), 36 captures total. Analysis only
  preregisters one candidate per node; it does not capture candidates, refit the
  global model or modify the default LUT.

## GUIDE9 full white FAST-DIRECT result

- The first full-grid attempt was interrupted after four captures by a user
  `KeyboardInterrupt`; those four captures were preserved.
- Recovery suffixes completed the remaining 136 observations without repeating
  the accepted prefix. The combined evidence contains exactly 140 unique
  Ray/strip captures, with quality and source-isolation checks passing and
  final Ray/strip zero confirmed.
- Frozen white-grid analysis classified `11/70` nodes as passing and `59/70`
  as requiring local correction. This is a valid scientific local-correction
  result, not a reason to refit the global model or install the default LUT.
- The next route is `GUIDE9_WHITE70_LOCAL_NODE_CORRECTION`: generate and test
  node-local corrections only, retaining the 70-node candidate identity and
  all accepted 140 observations. Do not repeat successful nodes or enter the
  interpolation holdout until the failed nodes are corrected and reconfirmed.

## Interrupted local-probe recovery gate

- Root `/Volumes/4T/temp/rgbww-optimizer/guide9-white-local-probes-20260824/20260824-092424-no-model6`
  completed 24/36 accepted observations: the complete `1800/GM0,100,200` and
  `3200/GM0` six-observation blocks are retained and must not be repeated.
- Physical return 25, the `5600/GM0` Ray reference, was a near-dark frame and
  failed all 58 required features. Two bounded recovery diagnostics at
  `5600K/GM0` and `5600K/GM100`, both at 100% and `1/2500`, reproduced the same
  dark RAW distribution (`median=512`, `p99=521`, `max=534`). API command
  success therefore does not establish current physical Ray emission.
- Current classification: `HUMAN_GATE_REQUIRED / Ray emission or optical path
  absent`. Human must restore/confirm Ray power and visible output toward the
  chart. No automation is appropriate while waiting for physical intervention.
- After visible Ray output is restored, validate one bounded Ray reference,
  then recover only the remaining `5600/GM0` and `20000/GM0` blocks in a new
  root. Combine them offline with the immutable four-node prefix; do not pool
  the rejected dark Ray frame and do not reacquire the first 24 observations.

Keep 13-node grid, boundary, Gate-6, P8 and LUT installation locked.
