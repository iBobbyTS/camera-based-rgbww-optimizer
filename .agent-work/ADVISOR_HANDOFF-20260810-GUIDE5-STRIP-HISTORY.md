# ADVISOR HANDOFF — GUIDE5 strip-only fast history

## Gate

`ADVISOR_GATE_REQUIRED`

The frozen analyzer returned `underpowered_or_unclassified`, which is not one of
the GUIDE5 S-A/S-B/S-C/S-D/S-E result branches. This is a scientific
classification gap, not an acquisition or evidence failure.

## Accepted acquisition

- Experiment: `GUIDE5-STRIP-HISTORY-ORDER-BALANCED-3X3-OP120-RESET600-V1`
- Root: `/Volumes/4T/temp/rgbww-optimizer/guide5-strip-history-3x3-op120-reset600-20260810-2141`
- Accepted sessions: `session-1` (DBC), `session-2` (CDB),
  `session-3-retry-4` (BCD)
- Captures: `7 + 7 + 7 = 21`
- Every session: run complete, quality pass, wrapper exit 0, shell cleanup exit 0,
  physical CR3/return `7/7`
- Session Git checkpoints: `606acb16073389731997ba08023dd5fc68b48fec`
  for sessions 1/2 and `ad2470366f5b519c9b345aaa516da8ded80da8fd`
  for session 3; all recorded `dirty=false`
- Ray R6 frames pooled: `false`
- Other experiment envelopes pooled: `false`

The analyzer used an external metadata analysis view at
`analysis-input-accepted-v2`. It contains copied small evidence and hard links to
the same accepted CR3 bytes; it does not duplicate or modify the source sessions.

## Frozen analysis

- Output: `/Volumes/4T/temp/rgbww-optimizer/guide5-strip-history-3x3-op120-reset600-20260810-2141/analysis-v2-strip-derived.json`
- SHA-256: `7f1325fed769cbfe03623e7a76ffc155ea46ed03c60c8db36dbef8c1c3aea9d6`
- Classification: `underpowered_or_unclassified`
- Legacy classification: `nonlinear/non-additive`
- Observation count / residual degrees of freedom: `9 / 2`
- Additive model rejected: `false`
- Common warm reentry detected: `false`
- Period main effect detected: `false`
- Predecessor main effect detected: `false`
- Nonlinear interaction demonstrated: `false`
- Raw return deltas compatible with zero: `false`
- R6 direction transfer: `not_applicable`

All named additive contrasts are individually compatible with zero. The common
warm-reentry score is `8.891427007641992` against guarded limit
`9.561767425446003`. The analyzer nevertheless cannot assign
`no_history_effect_detected` because the raw return deltas are not jointly
compatible with zero.

## Exact Advisor question

How should this valid 21-capture strip result map to the GUIDE5 scientific branch:

1. accept it as S-B / `no_history_effect_detected` because all modeled additive
   contrasts are compatible with zero and the additive model is not rejected;
2. classify it as S-D / unresolved because raw return compatibility failed; or
3. define another scientifically justified branch or minimal discriminating
   analysis/experiment?

Until Advisor answers, the paired Ray fast-vs-long bridge and all combined TD-B,
TD-C, sentinel, and later stages remain locked. No new acquisition is authorized
by this handoff.
