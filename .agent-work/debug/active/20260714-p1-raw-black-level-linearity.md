# P1 RAW Black-Level Linearity

## Confirmed observations

- P1 run `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-011100-p1` completed 31/31 captures with both lights off at the end.
- Pair-repeat P95 coefficient of variation is low: Ray `0.0008251`, strip `0.0011404`.
- Exposure-normalized P1 linearity residuals are systematic and much larger: Ray P50/P95 `7.14%/31.12%`; strip P50/P95 `7.91%/32.54%`.
- CR3 EXIF confirms the requested shutter sequence: Ray `1/800,1/400,1/200`; strip `1/160,1/80,1/40`.
- Both sources show the same decreasing normalized signal with longer exposure. For `block_04::R`, Ray is `78.44,66.06,59.59` per second; strip is `17.42,14.95,13.67` per second.
- Ambient subtraction changes these examples by only about `0.001`, so it is not the cause.
- The reports contain `black_level_per_channel=[0,44,124,90]`, while the observed intercept from the three raw code values is about `0.03` normalized, approximately 500 raw DN at global white level 16383. The per-channel black metadata is therefore implausible for this CR3 data.

## Hypothesis

`rawpy`'s CR3 `black_level_per_channel` is not usable for this camera. The analyzer subtracts it without a plausibility check, leaving a fixed sensor offset that becomes large after per-second normalization at short exposures.

## Verification

- The full RAW image's top/left optical margins have a modal code of `512` for all four CFA indices in the P1 CR3. `load_raw_mosaic` now resolves black levels from these margins only when the reported level differs by more than 1% of the global white level.
- A saved Ray `1/800` CR3 resolves `[0,44,124,90]` to `[512,512,512,512]`, recording both reported and optical levels plus per-channel fallback sources.
- Offline reanalysis of all saved P1 CR3 with forced optical black `512` reduces linearity residual P95 to Ray `0.00847` and strip `0.00437`; the corresponding uncorrected values were `0.31120` and `0.32545`.
- Pair-repeat P95 CV remains below `0.0014`, so the regression is specific to the removed fixed intercept, not exposure drift.

## Next action

The first black-level retry at `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-020000-p1-black-level-retry` failed during Ray auto-exposure after the ambient frame. The failure was `ValueError: global RAW white level must be finite and exceed black level`; both Python and shell cleanup records confirm the two lights were off. The failed auto-exposure CR3 was deleted by the generic temporary-trial cleanup, so its metadata cannot be inspected.

`camera_gphoto2.auto_expose_capture` now has an opt-in `preserve_failed_trial_dir`, used only by P1 native RAW capture. It copies a failed raw trial plus its exception JSON before normal temporary cleanup. Full verification and a new P1 directory are required before considering this resolved. The original first P1 run remains a failed measurement-chain validation artifact because its reports used invalid black metadata and its flat-field record was only `not_requested`.
