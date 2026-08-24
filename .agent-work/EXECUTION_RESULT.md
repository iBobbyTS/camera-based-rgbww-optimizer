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
- Device work has not started at this checkpoint. Root 1 strip observations are
  prohibited from pooling with this diagnostic or any fresh H300 batch.
