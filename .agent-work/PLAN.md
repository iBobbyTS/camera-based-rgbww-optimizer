# PLAN — GUIDE7 short order-balanced CW endpoint

## Accepted offline correction

- Both F2 roots are accepted long-block reference failures.
- Classification: `reproducible_cumulative_block_history_shift_with_locally_reproducible_probe_differentials`.
- Immutable preregistration:
  `.agent-work/analysis-v2-f2-locally-bracketed-probes-derived.json`.
- Both roots select candidate `CW4095/WW0/R0/G4095/B0`; no parent artifact was modified.

## Exact next experiment

- ID: `GUIDE7_H120_S100_F2_CW_SHORT_ORDER_BALANCED_ENDPOINT_V1`.
- Base: `CW4095/WW0/R0/G3839/B0`.
- Candidate: `CW4095/WW0/R0/G4095/B0`.
- Ray Q_before/Q_after: reset600, D120/A120/Q120, Ray `1/5000`.
- Strip sessions: reset-separated, base→candidate; candidate→base; candidate.
- Strip `1/400`; Ray zero before every strip capture; strip zero before Ray captures.
- 7 total captures, ambient 0, retry 0, no probes and no in-run solver.
- Gate: Ray bracket, base pair, candidate 3-way repeatability, order-balanced
  candidate-minus-base effect, and direct target-local candidate result.

Branches: faithful→H120/S50; stable nonfaithful/locally inadequate/repeatability
failure→3072 diagnostic. Keep 13-node grid, boundary, Gate-6, P8 and LUT locked.
