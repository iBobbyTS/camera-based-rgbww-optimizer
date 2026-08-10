# Advisor handoff — Ray history COLD600 classification

## Decision requested

Please review the completed cyclic order-balanced Ray-only identification result and
decide the next GUIDE route. The frozen analyzer classified the result as
`nonlinear/non-additive`. Until review completes, strip, combined TD-B, TD-C,
sentinel, and all later stages remain locked.

## Scientific authority and constraints

- Authority: `advisor/4/R6_REVISION.md`.
- R6 remains a valid scientific negative and hypothesis-generation evidence only.
- R6 frames were not pooled into this experiment's fit, covariance, coverage, or
  pass/fail result.
- Human changed operational dwell to 120 s and between-session cold proxy to 600 s
  to save time and power, explicitly accepting additional thermal error.
- No settled or steady-state claim is made.
- Frozen observer, ordered 58 features, uncertainty, covariance, guarded coverage,
  exposure settings, and frame selection were unchanged.

## Completed acquisition

```text
experiment = GUIDE4-RAY-HISTORY-ORDER-BALANCED-3X3-OP120-COLD600-V3
root = /Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-cold600-v3-20260810-081551
orders = DBC / CDB / BCD
sessions = 3/3
captures = 21/21
captures per session = 7/7, 7/7, 7/7
operational dwell = 120 s
cold proxy = 600 s per session
quality = pass / pass / pass
cleanup = Python pass + shell exit 0 for all sessions
wrapper exit = 0 / 0 / 0
acquisition git = afa43188b8efb2454a9267495a8effbe9c1152b4
acquisition dirty = false
```

Session quality artifact SHA-256:

```text
session 1 = 3615cae8a4e79230ced28be4a36258960d497baf7bcd9df484dcb82cf283385b
session 2 = bbe77f48d2305a94b79059e532263c0549992b3e7fa10448f6617c4781138f1e
session 3 = 3aae4e608269f9a3c125a904843828363b871119276627709ee2e972e0a2c3c1
```

Independent post-run all-off confirmed strip five-channel zero and Ray intensity 0.
No firmware, deployment, strip output, retry acquisition, second COLD600 root, or
later-stage experiment occurred.

## Frozen analysis result

Analyzer was invoked exactly once on the COLD600 V3 root.

```text
analysis = /Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-cold600-v3-20260810-081551/analysis.json
analysis sha256 = 0628736473668cceee9657f3a6770663e53728a3bb4ce10a871770bbf6c9136b
schema = guide4_ray_history_order_balanced_analysis_v1
status = classified_waiting_advisor_review
classification = nonlinear/non-additive
r6_frames_pooled = false
```

Diagnostics:

```text
period_detected = false
C_carryover_detected = false
other_state_effect_detected = false
large_orthogonal_residual = true
additive_model_rejected = false
all_return_deltas_compatible_with_zero = false
```

All frozen additive-model period and predecessor contrasts were compatible with zero.
The `nonlinear/non-additive` branch was selected because the frozen orthogonal-residual
diagnostic was large. This result does not establish C-specific carryover and does not
reclassify or pass R6.

Frozen R6 projection artifact:

```text
.agent-work/evidence/R6_VECTOR_REANALYSIS-20260809.json
sha256 = 68df8420dbdeabe19eb314d212e63404c0a1f67a141863c6357756b0aa301918
direction sha256 = bb707f600272968af656ba890535ebb161e0f45209249adde1aa72cdf3dfba57
```

## Current gate

```text
ADVISOR_GATE_REQUIRED
```

This is a scientific interpretation and branch-selection gate. It is not an engineering
failure, retry-budget stop, or Human device-authorization gate. No further scientific
stage should start before Advisor review.
