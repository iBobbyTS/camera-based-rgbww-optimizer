# GUIDE5 strip history analyzer-v3 result

## Advisor decision

```text
decision = OPTION_3_CORRECT_THE_COMMON_CONTRAST
guide5_parent_branch = S-A
classification = common_warm_reentry_shift_with_session_block_heterogeneity
strip_fast_history_structure = conditionally_accepted
cross_session_warm_center = not_frozen
new_strip_acquisition = not_required_now
ray_fast_long_bridge = unlocked
combined_TD_B / TD_C / sentinel_and_later = locked
```

The immutable v2 artifact remains:

```text
/Volumes/4T/temp/rgbww-optimizer/guide5-strip-history-3x3-op120-reset600-20260810-2141/analysis-v2-strip-derived.json
SHA-256 = 7f1325fed769cbfe03623e7a76ffc155ea46ed03c60c8db36dbef8c1c3aea9d6
classification = underpowered_or_unclassified
```

The corrected offline artifact is:

```text
/Volumes/4T/temp/rgbww-optimizer/guide5-strip-history-3x3-op120-reset600-20260810-2141/analysis-v3-strip-common-and-session-derived.json
SHA-256 = 0e8ad4eabd5acbb8ef6a6cbcf7fa3fde2fee8d13ad6cdf3c58446325461ea58e
schema = guide5_strip_history_order_balanced_analysis_v3
status = accepted_advisor_corrected_classification
```

## Corrected result

The v2 `common_warm_reentry_effect` was the treatment-coded baseline-cell
intercept. Analyzer-v3 instead uses the balanced contrast:

```text
beta0 + (session2 + session3 + position2 + position3
         + predecessorB + predecessorC) / 3
variance scalar relative to one delta = 2/9
score = 13.5891110356185
guarded limit = 9.561891733668457
decision = detected
```

Position and predecessor contrasts remain compatible with zero. The additive
model is not rejected and nonlinear interaction is not demonstrated. The
session contrast `session3_minus_session2` is detected:

```text
score = 9.950862478050007
guarded limit = 9.561711294035568
```

This is an unknown session/block influence. It is not labeled thermal, camera,
code, geometry, or environment. A global cross-session strip warm center is not
frozen. Future combined comparison must use local warm anchors and explicitly
block by session.

No capture was repeated for analyzer-v3. The artifact reuses the accepted 21
captures with the frozen ordered 58 features, frozen per-capture covariance,
shared-A0 covariance, 0.9973 guarded coverage, and unchanged frame selection.
