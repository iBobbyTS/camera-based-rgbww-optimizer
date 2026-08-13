# ADVISOR_GATE_REQUIRED — GUIDE5 TD-C FAST endpoint decomposition

## 1. Required Advisor decision

Please review the immutable offline decomposition and answer exactly:

1. Does the decomposition support the proposed `GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1`
   experiment, or should the route remain locked?
2. How should the B/C residual decomposition be interpreted scientifically? In
   particular, does it justify testing an anchor-direction substitution for B?
3. Are the stated shared-observation covariance terms and the residual-minus-anchor
   contrasts sufficient, or is a different pre-registered contrast required?

This is an `ADVISOR_GATE_REQUIRED`, not a Human authorization gate. No device
acquisition is authorized by this handoff. C validation, solver sentinel and all
later stages remain locked.

## 2. Why repository-local work cannot decide this

The requested calculations are complete and deterministic, but their scientific
meaning and the choice of the next branch are not code questions. The current
data reject only the absolute composition

`core A_after_D absolute offset + post-state local coordinate (Q-A_after_Q)`

for predicting a new D→A→Q endpoint. They do not demonstrate a B/C state-specific
bias because the B-minus-C residual contrast had not previously been tested and B
fails more strongly than C. Advisor must decide whether the new decomposition
warrants the bounded B-only anchor-direction experiment.

## 3. Accepted endpoint evidence

- Endpoint root: `/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328`
- Protocol: `GUIDE5_TD_C_FAST_ENDPOINT_HOLDOUT_B_C_V1`
- Acquisition: 8 formal / 8 physical / 0 ambient / retry 0
- Wrapper and child exit: 0
- Python and shell cleanup: pass / 0
- Ray strip-zero and strip Ray-intensity-zero: all eight pass
- Paired offsets: B pass, score `7.4311219131`, guard `9.5196397714`; C pass,
  score `4.7820236614`, guard `9.5294838618`
- Original endpoint synthesis: B fail, score `20.5356966388`, guard `9.5289317274`;
  C fail, score `12.2078852606`, guard `9.5300736632`

The eight observations remain valid scientific evidence. They are not discarded
or reclassified as an engineering failure.

## 4. Offline decomposition requested by Advisor and completed

Derived artifact:

`/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328/analysis-v2-residual-decomposition-derived-v2.json`

SHA-256:
`570ef2631fae91035fb4a7d60c0b57494e349ab9252ba0f7df74750f87a9a52f`

It contains full 58-feature vectors and whitened scores for:

- `synthesis_residual_B` and `synthesis_residual_C`
- `B_minus_C_synthesis_residual`
- `A_after_B_minus_A_after_D`
- `A_after_C_minus_A_after_D`
- `residual_minus_anchor_substitution_B`
- `residual_minus_anchor_substitution_C`
- endpoint mean vectors for B and C

Summary scores:

| Contrast | Score |
|---|---:|
| synthesis residual B | 20.5356966388 |
| synthesis residual C | 12.2078852606 |
| B-minus-C synthesis residual | 18.3538445579 |
| A-after-B minus A-after-D | recorded in artifact |
| A-after-C minus A-after-D | recorded in artifact |
| residual-minus-anchor B | 15.8858229361 |
| residual-minus-anchor C | 12.5016914509 |

The artifact records that endpoint data were not used to refit the core or
combined parent analyses. Shared core-A terms are retained in the B-minus-C
covariance rather than treated as independent.

## 5. Conditionally permitted, non-executable next plan

`GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1`

- Session 1: B Ray→strip
- Session 2: B strip→Ray
- Each source: `reset600 → D120 → A_pre120 → B120 → A_post120`
- 12 formal / 12 physical / 0 ambient / retry 0
- Gates: A_pre paired consistency, B paired consistency, A_post paired
  consistency, A_post-minus-A_pre anchor direction, independent transfer of the
  pre-registered D→A→B pre-anchor local coordinate
- C validation, solver sentinel, and all later stages remain locked

The plan is recorded as `offline_conditionally_permitted` and
`formal_capture_eligible=false`; it has not been started.

## 6. Included files and excluded payloads

The adjacent ZIP contains only derived/calculated data, small execution
evidence, exact source/test files, PLAN/PLAN-FULL context, this handoff and a
manifest. It excludes CR3/RAW/DNG/NPY/NPZ/TIFF/JPEG/PNG, decoded camera arrays,
firmware, builds, caches, credentials and generated archives.

Excluded raw root retained for audit:

`/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328/camera`

The exclusion is intentional; the run identity is preserved by the included
derived artifacts, hashes and small ledgers.
