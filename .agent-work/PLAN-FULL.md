# PLAN-FULL — GUIDE8 Ray H120/S100 measurement recovery

## Scientific state

- Accepted root classification:
  `local_controllability_not_observable_under_frozen_exposure`.
- Failure subclassification:
  `Ray_reference_emission_or_optical_path_not_established`.
- Scientific color observation: absent.
- Solver attempt count: 0.
- Formal exposure expansion: prohibited until the diagnostic qualifies a window.
- Frozen observer/features/thresholds/covariance/coverage remain unchanged.

## Current section S01 — direct Ray emission/exposure diagnostic

Authority: `advisor/8/8.GUIDE.md` and `advisor/8/8.RESEARCH.md`.

Goal: implement, validate and execute
`GUIDE8_RAY_H120_S100_EMISSION_EXPOSURE_DIAG_V1` through the existing plan,
measurement and analyzer owners.

Acceptance:

- exact control, dark, 14-shutter ladder, early-stop and 16-physical cap;
- H120 remains continuously on during the ladder;
- only near-noise-only continues; clipping/nonfinite/other quality, shape,
  isolation or evidence failures stop;
- a legal pair must be adjacent in the frozen ladder, have nominal exposure ratio
  `<=1.25`, and pass existing
  `raw_response_candidate.evaluate_response_model` on the two retained
  patch-statistics reports with frozen P1 repeatability reports, identity response
  (`a=b=0`), and all required 58 features at `<=3.0` repeatability sigma. This is
  the frozen P1 Gate-1 rule; no new direct norm, threshold or covariance is allowed.
  Ladder neighbors above `1.25` cannot qualify. The first legal pair selects the
  faster shutter, with formal selected shutter no slower than `1/320` and `1/250`
  diagnostic-only;
- exposure-policy-v2 is immutable, contains required hashes/provenance including
  the exact P1 evaluator source hash and frozen repeatability evidence identity,
  and does not change the frozen measurement semantics;
- fake behavior evidence covers E-A..E-G-relevant execution and cleanup paths;
- one clean checkpoint precedes hardware execution.

Review assurance: `AUTO -> ONE`. This is one protocol-specific path in existing
owners with bounded irreversible side effects and exact cleanup; one independent
bounded review plus direct behavior tests is proportionate.

## Predefined result branches

- E-A control invalid: Human physical/path inspection; no ladder.
- E-B dark contamination: unresolved environment/optical leak; no subtraction.
- E-C `1/5000 + 1/4000` qualified: retain historical shutter and start a fresh
  GUIDE7 F1 local-controllability root automatically.
- E-D another adjacent pair qualified: create v2 policy, do not pool old/new
  centers, and start a fresh GUIDE7 F1 root automatically.
- E-E no single-exposure window: Advisor gate before HDR.
- E-F near-noise through `1/250`: emission not established; Human physical gate.
- E-G shape invariance failure: Advisor gate.

## Locked remainder

Until E-C/E-D and the subsequent H120/S100 scientific classification:
strip probes outside that fresh F1 root, 13-node INT100 grid, per-Hue boundary,
Gate-6, P8 and runtime/default LUT installation remain locked.

PLAN/PLAN-FULL are versioned collaboration records only; production and tests do
not consume them as runtime or authorization state.
