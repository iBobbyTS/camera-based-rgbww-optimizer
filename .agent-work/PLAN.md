# PLAN — GUIDE7 F2 alternate-face controllability

## Resolved scientific disposition

- Both prior LC-B roots are accepted valid scientific evidence.
- Current G-active route classification:
  `H120_S100_G_active_fullscale_face_stable_nonfaithful_locally_exhausted`.
- No further centered continuation is allowed.
- Direct 58-feature estimand, covariance, 0.9973 coverage, observer, thresholds
  and whitened navigation coordinate remain frozen.
- Advisor gate is resolved; no new GUIDE is required.

## Offline selection

- Artifact: `config/hsi/guide7-h120-s100-f2-face-selection-v1.json`.
- Ranked legal non-G faces by P2 seed-only predicted residual:
  CW `0.3892623`, B `0.6820106`, WW `0.7009996`, R `0.9464259`.
- Selected face: CW.
- Selected seed: `CW4095/WW0/R0/G3839/B0`.
- `P2_seed_only=true`; prediction is not scientific acceptance.

## Exact experiment

- ID: `GUIDE7_H120_S100_F2_ALTERNATE_FACE_CONTROLLABILITY_V1`.
- New root; Ray `1/5000`, strip `1/400`; no guard fallback.
- Ray before/after, strip reset600, D120/A120/tested120.
- CW fixed at 4095; free channels WW/R/G/B; four one-sided 256 probes,
  including G 3839→4095.
- Two base anchors; at most four candidates; maximum absolute step 768;
  backtracks 1.0/0.5/0.25; one Broyden rebase; no re-probe.
- Faithful candidate: require 3 confirmations.
- Nonfaithful result: require 3 repeats of best-valid exact command.
- Cap: Ray 2, strip ≤14, total ≤16, ambient 0, retry 0.

F2 stable nonfaithful proceeds automatically to the 3072 closed-loop diagnostic.
Keep the 13-node grid, full boundary mapping, Gate-6, P8 and LUT installation locked.
