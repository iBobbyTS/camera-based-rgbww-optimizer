# PLAN — fresh GUIDE6 H120/S100 direct target-local F1

## Accepted prerequisite

- Qualification root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-strip-exposure-qualification-20260818/20260818-003422-s-measurement`
- Classification: `strip_exposure_window_qualified`.
- Selected strip shutter: `1/400`.
- Guard shutter: `1/320`, evidence-only; no automatic fallback or reacquire.
- Physical/diagnostic/formal: `8 / 8 / 0`.
- Shape compatibility: pass; source isolation, cleanup and final zero: pass.
- Policy: `config/hsi/strip-h120-s100-exposure-policy-v1.json`.

## Next scientific action

- Experiment ID: `GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-V1`.
- Use a fresh root; do not copy, pool or import either contaminated historical
  GUIDE6 root.
- Ray Q_before/Q_after: fixed `1/5000`.
- Strip base/probes/candidates/confirmations: fixed selected `1/400` only.
- Before every strip capture, require capture-level Ray intensity zero evidence.
- Before every Ray capture, require capture-level five-channel strip-zero evidence.
- Preserve reset600, D120, A120, tested120, frozen 58 features, observer,
  thresholds, covariance, coverage and bounded LC-A/B/C/D/E routing.
- Guard `1/320` must not be used as an in-run fallback.

After completion, run the frozen GUIDE6 analyzer once and follow its predeclared
LC branch. Do not enter 13-node grid, boundary, Gate-6, P8 or LUT installation.
