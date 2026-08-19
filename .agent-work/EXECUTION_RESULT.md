# GUIDE7 F2 — target block invalid from strip drift

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f2-alternate-face-20260819/20260819-225543-cw-active-base-repeat-fix`
- Captures: 12/12 accepted; Ray 2, strip 10; candidates 0; base repeats 3.
- CW-active seed and G probe executed exactly; all strip frames used `1/400`,
  Ray frames used `1/5000`; guard and contaminated roots were not used.
- Ray bracket passed.
- Strip base drift failed on anchor 2; repeat stability also failed narrowly.
- Classification: `target_block_reference_invalid` (`LC-E`, F2-E).
- `measurement_valid=false`; `science_delta`: a valid negative on this block's
  stability, not an H120/S100 color/gamut result.
- Cleanup and independent final zero: pass; Git clean.
- Next: one fresh F2 reference/block-drift repeat under the same contract.

The first analyzer invocation did not write output because it assumed F1 probe
roles. It was corrected to derive the exact four probe roles from the retained
protocol evidence; focused tests passed and the root was analyzed once without
reacquisition.
