# PLAN — S02 Direct local-controllability protocol

Source: `.agent-work/PLAN-FULL.md`. PLAN-FULL remains the feature roadmap; this file
contains only S02.

## Goal

Implement and validate `GUIDE6_H120_S100_DIRECT_LOCAL_CONTROLLABILITY_V1` through
the existing plan, measurement and analyzer owners: exact base, four +256 probes,
two drift anchors, direct-whitened Jacobian, at most four bounded feedback candidates,
one no-new-probe Broyden/model rebase, and three confirmations after a passing candidate.

## Safety and budgets

- Ray 2; strip <=14; total <=16; ambient 0; hidden in-root retry 0.
- Always reserve three confirmation slots before feedback.
- Reset600 and D120/A120/tested-command120 remain frozen.
- Source isolation, finally cleanup, zero readback and clean Git checkpoint remain mandatory.

## Scope

Only existing `p7_thermal_diagnostics.py`, `measure_p7_thermal_diagnostics.py`,
`analyze_p7_thermal_diagnostics.py`, named bounded solver seams if necessary,
`tests/test_p7_direct_r6.py`, and an existing wrapper argument if needed.

No generic runtime, release/lineage/stage-gate, B pre/post, synthesis, 13-node grid,
boundary, Gate-6 or P8.

## Acceptance

Exact protocol/budget/cleanup behavior; direct-whitened Jacobian and candidate evidence;
truthful LC-A/B/C/D/E predicates; first G-active block cannot claim terminal unresolved
or gamut unreachable. After implementation and dual bounded review, execute one clean
live block and follow its predefined branch.
