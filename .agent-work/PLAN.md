# PLAN — ADVISOR_GATE_REQUIRED after repeated GUIDE7 F2 block drift

## Gate

`ADVISOR_GATE_REQUIRED`: both complete CW-active F2 blocks have valid Ray
references, capture quality, source isolation and cleanup, but both fail the
second strip base anchor and do not establish stable best/base repeats. The one
permitted fresh reference/block-drift repeat is exhausted. A third F2 block is
prohibited.

## Frozen facts

- Experiment: `GUIDE7_H120_S100_F2_ALTERNATE_FACE_CONTROLLABILITY_V1`.
- Face/seed: CW active; `CW4095/WW0/R0/G3839/B0`.
- Ray shutter `1/5000`; strip shutter `1/400`; no guard fallback.
- Both blocks: 12/12 accepted captures, Ray bracket pass, anchor 1 pass,
  anchor 2 fail, candidates 0, base repeats 3, cleanup/final zero pass.
- First anchor-2 score/guard: `15.6161 / 9.5614`.
- Repeat anchor-2 score/guard: `12.4327 / 9.5614`.
- This is reference/block instability, not stable nonfaithfulness, solver failure,
  or gamut/physical unreachability.

## Advisor question

Define the next exact scientific disposition for repeated CW-active strip block
drift. Decide whether the F2 history/dwell/anchor design requires a bounded
measurement-science correction, whether this face should be classified as
unstable under the current fast envelope, or whether another predeclared route
should be used. Preserve the frozen direct 58-feature estimand, covariance,
coverage, observer and thresholds unless the Advisor explicitly changes them.

Keep 3072, the 13-node grid, full boundary mapping, Gate-6, P8 and LUT installation
locked. Do not run a third F2 block before Advisor response.
