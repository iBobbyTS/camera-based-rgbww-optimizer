# GUIDE7 F2 repeat — repeated strip block drift

- Repeat root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f2-reference-repeat-20260819/20260819-004620-cw-active-reference-repeat`
- Captures: 12/12 accepted; Ray 2, strip 10; candidates 0; base repeats 3.
- Exact CW face, G probe, shutters and source-isolation contract passed.
- Ray bracket: `3.5065 / 9.5433`, pass.
- Strip anchor 1: `2.2890 / 9.5614`, pass.
- Strip anchor 2: `12.4327 / 9.5614`, fail.
- Repeat1-vs-repeat2 stability: `14.7520 / 9.5614`, fail.
- Classification: `target_block_reference_invalid` (`LC-E`, F2-E).
- Measurement-valid color/solver conclusion: none.
- Cleanup and independent final zero: pass; Git clean.
- `science_delta`: repeatable evidence that the CW-active block is unstable under
  the current fast F2 history/timing contract; not a gamut result.
- Next: `ADVISOR_GATE_REQUIRED`; no third F2 block.

The analyzer was run exactly once on this root. No threshold, feature, covariance,
coverage, exposure or frame selection changed.
