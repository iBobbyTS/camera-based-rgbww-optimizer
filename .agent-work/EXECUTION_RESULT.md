# GUIDE9 H300 reference emission/path diagnostic readiness

- Advisor correction accepted: prior evidence is one incomplete run after a valid
  H300 Q-before plus one near-dark H300 observation without complete pre-capture
  state establishment, not two established first-reference failures.
- Current classification:
  `intermittent_H300_reference_emission_or_optical_path_dropout_unresolved`.
- Implemented `GUIDE9_RAY_H300_S100_REFERENCE_EMISSION_PATH_DIAG_V1` as a
  Ray-only, 0-formal/4-physical, order-balanced H0/S0 and H300/S100 diagnostic.
- Frozen shutters remain H0/S0 `1/16000` and H300/S100 `1/2500`; exposure,
  observer, 58 features, thresholds, covariance and coverage are unchanged.
- Capture-bound Ray set/immediate-readback/post-readback and strip-zero evidence
  is written before feature extraction, including rejected captures.
- Focused direct suite: 68 tests passed. Full discovery: 532 tests passed.
- `git diff --check` and `codegraph sync`: passed.
- Clean checkpoint: `9ad9be3`.
- First device attempt root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-ray-h300-reference-diagnostic-20260823/20260823-order-balanced-v1`.
- Classification: `ENGINEERING_OR_HARNESS_FAILURE`; the camera bridge health
  endpoint passed, but both the attempt and a bounded follow-up config check
  returned HTTP 502 `camera_config_failed` before any light or capture action.
- Captures: 0/4; `science_delta=none`; shell cleanup and independent Ray/strip
  zero readback passed; Git remained clean at the checkpoint.
- `HUMAN_GATE_REQUIRED`: physically wake/confirm the Canon camera and its USB
  connection. After `/v1/config` succeeds, start a fresh diagnostic root.
- Root 1 strip observations remain prohibited from pooling with this diagnostic
  or any fresh H300 batch.

## Completed diagnostic result

- Successful root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-ray-h300-reference-diagnostic-20260823/20260823-order-balanced-isolation-wired`.
- Acquisition completed 4/4 physical, 0 formal; wrapper, Python cleanup, shell
  cleanup, final Ray/strip zero and Git-clean checkpoint all passed.
- All four capture-bound state records show the exact HSI command, immediate
  readback and post-capture readback at intensity 1000, with strip five-channel
  zero evidence. Recorded shutters were H0 `0.00006103515625 s` and H300
  `0.000387549084953174 s`.
- Both H0 controls and both H300 observations rejected all 92 optimization
  planes as near-noise. Classification: `R-D /
  system_level_Ray_camera_or_optical_path_unresolved`.
- Immutable derived analysis:
  `analysis-guide9-h300-reference-derived.json` in the successful root.
- `HUMAN_GATE_REQUIRED`: inspect visible Ray emission for H0/S0 and H300/S100,
  Ray orientation/obstruction, camera framing/chart position and the physical
  camera/Ray optical path. H300/S50 and all later HSI work remain locked.
