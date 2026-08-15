# PLAN — S01 Seed-negative immutable reclassification

Source: `.agent-work/PLAN-FULL.md`. PLAN-FULL remains the feature roadmap; this file
contains only the current section.

## Goal

Create an immutable derived artifact for the two accepted roots that records
`repeatable_target_local_seed_mismatch`, exact command hash, scores and zero solver
attempts while keeping both legacy `analysis.json` files byte-identical.

## Allowed scope

- `src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py`
- `tests/test_p7_direct_r6.py`
- current `.agent-work` feature records

No device execution, solver implementation, feature/covariance/threshold change or
legacy artifact mutation.

## Acceptance

Exact two-root regression, immutable output/no overwrite, legacy bytes unchanged,
and corrected status consumable by S02.
