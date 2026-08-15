# Feature State

## Feature

- Feature ID / slug: `guide6-h120-s100-local-controllability-v1`
- Goal: execute the first real bounded direct local-controllability block.
- Execution mode: `EXECUTE_WITH_COMMITS`
- Skill invocation source: `CUSTOM_INSTRUCTIONS_AUTO`
- Invocation timing: `FEATURE_START`
- Trigger evidence / matched conditions: adaptive device execution crosses plan, runner, analyzer and tests at a high-risk hardware boundary.
- Audit mode: `LIVE`
- Audit activation source / explicit opt-out: `default-on skill policy`
- Audit trace path: `.agent-work/audit/guide6-h120-s100-local-controllability-v1/TRACE.jsonl`
- Feature base: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Current feature head: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Active artifact isolation: `archived-before-base`
- Workflow adoption note: `new`
- Integration repair waves used: `0/5`
- Integration automatic recovery used: `no`
- PLAN-FULL review status: `approved`
- Reviewed plan SHA-256: initial `ccdc2e45801b8d303b21caa9148323b59e584ac66ef243a96f03fb0296dabc24`; corrected pre-ledger `b908e8b58e5e0260119a22f3f4279c30c41ed1b72da184c73e284754b267d570`
- PLAN_DELTA recheck: `not-required`
- Open owner/plan decisions: `none`

## Current section

- ID/title: `S01 / Seed-negative immutable reclassification`
- Review intensity: `BOUNDED`
- Review assurance requested/resolved: `AUTO / ONE`
- Assurance reasons/override: offline additive artifact with exact values; no device behavior.
- Original section lineage: `S01`
- Section base: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Current head: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Status: `IMPLEMENTING`
- Allowed-to-edit owners/files/symbols/routes: analyzer reclassification helper, direct tests, current feature artifacts.
- Inspect-only dependency paths/direct impact cone: retained roots, legacy analyses, frozen policy.
- Explicitly excluded owners/mechanisms: device runner, solver, legacy mutation, generalized framework.
- Allowed structural changes: one local derived-artifact function/output.

## Review state

- Initial bounded review: `not-run`
- Open finding IDs: `none`
- Cumulative repair waves used: `0/5`
- Exact product/test head covered by current evidence: `none`
- Clean A closure: `no`
- Final bounded review: `not-required`
- Required assurance evidence satisfied: `no`
- Clean B final, if required: `not-required`
- Reset reason, if any: `none`

## Validation

- Targeted checks: `pending`
- Section/package checks: `pending`
- Integration checks: `pending`
- Evidence gaps/residual risk: S01 implementation and exact immutable behavior tests pending.

## Recovery

- Generation: `0`
- Backup ref: `none`
- Automatic hard-cap recovery used for original lineage: `no`
- Recovery classification: `none`
- Authorized named recovery wave or replacement boundary: `none`
- Preserved code/evidence: retained two roots and legacy analyses.

## Decisions and next action

- Owner decisions required: `none`
- Rejected/non-blocking scope proposals: no generalized runtime, release, lineage, stage-gate or broad solver framework.
- Next action: implement S01 immutable seed-negative correction.

## Section summary

| Section | Original lineage | Base | Head | Status | Waves | Recovery used | Clean A | Clean B | Notes |
|---|---|---|---|---|---:|---|---|---|---|
| S01 | S01 | 3e81a32 | pending | PLAN_REVIEW | 0 | no | no | n/a | immutable correction |
| S02 | S02 | S01 | pending | PLANNED | 0 | no | no | no | adaptive device protocol |
