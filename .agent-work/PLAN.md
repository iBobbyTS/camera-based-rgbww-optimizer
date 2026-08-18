# PLAN — ADVISOR_GATE_REQUIRED after GUIDE6 LC-B continuation

## Gate

`ADVISOR_GATE_REQUIRED`: the qualified, isolated H120/S100 direct route produced
two valid LC-B blocks. The single permitted generation-1 centered continuation
is exhausted. A second continuation is prohibited.

## Frozen facts

- Strip exposure policy: selected `1/400`, guard-only `1/320`.
- F1 base `CW518/WW0/R0/G4095/B0`: valid LC-B; four candidates; no pass.
- Centered continuation base `CW0/WW0/R377/G4095/B107`: valid LC-B; four
  candidates; no pass.
- Continuation analyzer base score/guard: `1459.4726873465686 /
  9.507745630047346`.
- Best continuation candidate score/guard: `1457.9065349594123 /
  9.506925685282807`.
- Ray bracket, strip base anchors, 58-feature quality, source isolation,
  cleanup and final zero all pass in both blocks.
- This does not establish gamut or physical unreachability.

## Advisor question

Given two measurement-valid LC-B blocks with bounded local improvement but
scores still far outside the frozen guard, define the next scientifically valid
branch and exact experiment, if any. State whether to use an alternate active-set
screen, revise only the solver navigation experiment while preserving the final
estimand, or terminate H120/S100 under a more precise non-gamut classification.

Keep 13-node grid, boundary, Gate-6, P8 and LUT installation locked pending the
decision. Do not start another device experiment or continuation.
