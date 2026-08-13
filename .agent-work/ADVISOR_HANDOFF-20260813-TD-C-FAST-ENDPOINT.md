# Advisor Handoff — GUIDE5 TD-C FAST B/C Endpoint Holdout

## Gate

`ADVISOR_GATE_REQUIRED`

本轮采集协议完整执行并安全结束，但 endpoint 的科学 synthesis agreement
未通过。需要 Advisor 判断这是否是 GUIDE5 预期的 state-dependent endpoint
偏差，还是说明 core A absolute offset 与 combined local-state coordinate
不能预测新的 B/C endpoint。

## Run identity

- Root: `/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328`
- Protocol: `GUIDE5_TD_C_FAST_ENDPOINT_HOLDOUT_B_C_V1`
- Git branch: `codex/guide4-science-path-v3`
- Acquisition implementation commit before run: `6119917`
- Formal / physical / ambient: `8 / 8 / 0`
- Retry: `0`
- Wrapper exit: `0`
- Child exit: `0`
- Python cleanup: pass
- Shell cleanup: exit `0`
- `science_delta`: valid new 8-observation endpoint holdout; synthesis disagreement observed

## Frozen protocol actually executed

Sessions were exactly:

1. B: Ray → strip
2. C: strip → Ray
3. B: strip → Ray
4. C: Ray → strip

Each source used `reset600 → D120 → A120 → Q120 → capture Q`, with no ambient
capture. Frozen shutters were Ray B `1/8000`, Ray C `1/2500`, strip B `1/500`,
strip C `1/125`. Legacy 1800-second TD-C expansion, solver, sentinel and later
stages were not run.

## Validation and safety evidence

- `quality.json`: pass, eight pass rows.
- `wrapper-state.json`: finished, child/wrapper exit `0`, shell cleanup `0`.
- `run.json`: complete, `completed_formal=8`, `accepted_formal_count=8`.
- Eight capture rows and eight physical-return rows exist.
- Ray rows contain verified five-channel strip-zero snapshots.
- Strip rows contain verified Ray CCT readback with intensity `0`.
- No raw CR3, camera arrays, firmware or build output is included in the Advisor ZIP.

## Corrected analysis result

Artifact: `analysis.json`

| State | Paired-offset score | Guard | Repeatability | Synthesis score | Guard | Synthesis |
|---|---:|---:|---|---:|---:|---|
| B | 7.4311219131 | 9.5196397714 | pass | 20.5356966388 | 9.5289317274 | fail |
| C | 4.7820236614 | 9.5294838618 | pass | 12.2078852606 | 9.5300736632 | fail |

The synthesis residual covariance is the sum of:

`new endpoint mean + core A absolute mean + combined local-state mean`.

The balanced Latin-square GLS state estimand is equivalent to the mean of the
three state cells for this accepted design. The analyzer records this identity,
keeps the pre-solver strip-Ray offset out of the zero gate, and uses frozen
source-specific covariance and source-level unit-observation Monte Carlo.

## Scientific question for Advisor

Please decide:

1. Should the result be classified as a valid scientific endpoint mismatch for
   B and C, while retaining the fast protocol and leaving solver/later stages
   locked?
2. Does the B/C synthesis failure indicate a state-specific mismatch that can be
   handled by the next GUIDE5 branch, or does it invalidate the proposed
   core-A-plus-local-coordinate synthesis model?
3. Is another bounded characterization experiment required, and if so what
   exact contrast/protocol should be used? No new acquisition is authorized by
   this handoff itself.

## Included evidence

This handoff is accompanied by a ZIP containing only derived/small evidence,
source/test files, plans, GUIDE/RESEARCH context, logs and hashes. Raw capture
payloads are excluded and remain at the retained run root above.
