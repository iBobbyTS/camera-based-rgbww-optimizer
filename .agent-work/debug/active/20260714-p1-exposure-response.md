# P1 Recorded Exposure And Residual RAW Response

## Confirmed Root Cause

- P1 v6: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6`.
- P1 v7: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-035100-p1-exposure-diagnostic-v7`.
- Both legacy runs normalized native RAW values with the requested/display shutter string. Canon R6 Mark III CR3 MakerNote `Canon:ExposureTime` differs materially at several settings. Examples:
  - display `1/60` -> recorded `0.015625s` (`1/64`);
  - display `30` -> recorded `32s`.
- The earlier cross-source response ratios followed the same camera exposure-time signature. This invalidates the previous conclusion that a strip-specific PWM/power effect was the primary cause.
- v6 and v7 both planned `ray_intensity_percent=100` but sent raw OpenAPI `intensity=100`, approximately true `10%`. The old note incorrectly described v7 as raw `10`; retained `plan.json` and `commands.jsonl` show raw `100` in both runs. This does not invalidate within-run exposure ratios, but neither run is a valid Ray 100% brightness baseline.

## Implemented Offline Fix

- Shared resolver: `src/camera_based_rgbww_optimizer/measurement/recorded_exposure.py`.
- Priority: `Canon:ExposureTime`, standard EXIF, then explicit `fallback_nominal` with a diagnostic.
- P1/P1-D acquisition reports now store signal and ambient exposure provenance and normalize from recorded duration.
- Legacy P1 can be recomputed from retained CR3 with:

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation RUN_DIR \
  --recompute-recorded-exposure
```

- The command verifies frozen location/observer-config hashes and writes `analysis-recorded-exposure-v1.json`; it never overwrites `analysis.json`.
- Linearity analysis now separates total per-exposure response, global scale, and residual patch/CFA shape. Reference-factor zero residuals also have an explicit non-reference-only summary.

## Recomputed Evidence

Both runs were recomputed from every retained CR3. All `31/31` v6 and `27/27` v7 reports used `Canon:ExposureTime`; no fallback occurred.

### v6

- Output: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6/analysis-recorded-exposure-v1.json`.
- Non-reference P95 total residual: Ray `0.7734%`, strip `0.3776%`.
- Non-reference P95 shape residual after removing global exposure scale: Ray `0.3999%`, strip `0.3755%`.
- Non-reference P95 shape residual in repeatability sigma: Ray `16.62`, strip `7.19`.

### v7

- Output: `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-035100-p1-exposure-diagnostic-v7/analysis-recorded-exposure-v1.json`.
- Non-reference P95 total residual: Ray `0.5635%`, strip `0.2735%`.
- Non-reference P95 shape residual after removing global exposure scale: Ray `0.1787%`, strip `0.1961%`.
- Non-reference P95 shape residual in repeatability sigma: Ray `11.19`, strip `3.75`.

The large old scalar error is fixed, but P1 still does not pass the existing `3 sigma_repeat` policy.

## Residual Shape Diagnosis

- The largest residuals occur in high-signal green samples, especially blocks `06`, `09`, `14`, and `19` on `G1/G2`.
- Short exposures are positive and long exposures negative after removing global scale. Ray and strip show the same direction.
- Maximum ambient-subtracted normalized patch signal was approximately:
  - v6 Ray: `0.237 / 0.472 / 0.742` at `0.5x / 1x / 1.5x`;
  - v6 strip: `0.277 / 0.552 / 0.870`;
  - v7 Ray: `0.374 / 0.472 / 0.591` at `0.8x / 1x / 1.25x`;
  - v7 strip: `0.438 / 0.552 / 0.693`.
- This is consistent with mild high-signal RAW compression. It is not evidence for a strip-only fault.
- A temporary monotonic correction candidate `g(y)=y*(1+a*y+b*y^2)` was fit offline with global per-exposure scale removed. Training on v6 reduced v7 P95 shape from `0.1894%` to `0.1068%`; training on v7 reduced v6 from `0.3941%` to `0.1858%`. The correction direction cross-validates, but evidence is same-day and still above strict repeatability. Do not install a response correction yet.

## Code-Duty Impact

- `tmp/channel-response/merged/channel-code-duty-response-merged.json` contains 95 normalized measurements across 26 requested shutter settings.
- Its two referenced source run directories and CR3 files are absent locally and under `/Volumes/4T/temp/rgbww-optimizer`.
- Therefore the current `config/channel/code-duty-curve.json` cannot be repaired exactly from CR3 metadata.
- Keep it only for compatibility with the already closed-loop-calibrated white LUT. Do not use it as absolute P2 basis/intensity evidence. Future channel-response acquisition now records actual exposure metadata.

## Current Decision

- P1 remains `fail`; do not set observer quality thresholds and do not enter P2.
- Do not run the old P1-D same-shutter protocol next. The principal shutter discrepancy has already been identified from retained metadata.
- The next device run is a new full P1 at lower RAW signal, using recorded exposure normalization and an explicit `--target-max 19661` candidate (30% of the 16-bit meter scale). Keep `0.5x,1x,1.5x` brackets so the longest bracket is expected below the prior compression region.
- `19661` is a data-derived starting candidate, not an accepted threshold. Before the full run, one Ray and one strip longest-bracket preflight must confirm no clipping and maximum reliable patch/CFA signal below `0.45`; otherwise lower `target_max` and create a new dry-run plan.
- Only if the lower-signal full P1 still shows cross-source shape above the decision policy should P1-D or a formally versioned camera-response correction be reconsidered.
