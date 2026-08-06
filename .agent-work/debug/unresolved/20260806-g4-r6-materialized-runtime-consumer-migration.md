# G4 R6 materialized runtime consumer migration reassessment

**Status:** `UNRESOLVED_READ_ONLY_REASSESSMENT_COMPLETE_PLANNER_PACKAGE_PENDING`

**Date:** `2026-08-06`

**Live branch:** `codex/g4-r6-owner-alignment-large-change`

**Accepted-tree intake HEAD:** `976de440043aca02086837d86ead413f1c7d2cbf`

**Accepted blobs:** stage-gate source `0015d7ce2f2a5dde9118478f98c929020a474a01`; stage-gate test `2a60a987dda02675c2eddc7d8260d61a8f68edc3`

## Frozen historical boundary

- `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` remains `REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED`.
- The rejected candidate remains isolated at `refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected`, commit `4a39f9ab377d7568c37eeea8aaa78d82aaa14535`, outside live ancestry.
- Its implementation was not read or reused in this reassessment. Only accepted-tree source plus immutable Planner/Executer evidence were inspected.
- No production/test file, test process, package/formal root, network endpoint, camera, Ray, strip, or GUIDE/RESEARCH file was touched.

## Confirmed facts

1. `p7_td_b_r6_stage_gate.py` owns the public materialized-plan builder, exact authority serialization, future-activation validation, and `validate_materialized_runtime_plan`.
2. The PLAN-bound authority is a public cross-module runtime contract. `measure_p7_thermal_diagnostics.py` validates it before execution and `p7_td_b_r6_terminal.py` validates it during terminal replay/finalization.
3. The accepted runtime owner already keeps resolved camera settings outside the frozen plan and passes them as explicit runtime context; this ownership split must remain intact.
4. The third rejected candidate changed the stage-gate authority contract without migrating every terminal/thermal fixture consumer. Its extra 13 `runtime_authority_drift` errors therefore prove incomplete consumer migration, not impossibility of materialized identity.
5. Three accepted test locations construct equivalent authority/attestation payloads: the stage-gate `SyntheticGitRepository` path, terminal `materialized_plan`, and thermal `_r6_materialized_plan_for_test`. Rule-of-three is met; handwritten dictionaries are no longer an acceptable independent schema owner.

## Failure-candidate ledger

| candidate | owner/state boundary changed | first candidate-owned error |
| --- | --- | --- |
| materialized commit attestation v1 | Replaced static future identity with post-commit materialized identity in the stage-gate schema, but did not propagate production activation | production/measure activation produced `committed_source_materialized_shape_drift` |
| materialized commit attestation v2 focused | Propagated the activation seam, then exposed incomplete preparation/accepted-engineering subject/path handling | accepted-engineering subject/path preparation drift, followed by an unwrapped path-query `OSError` |
| materialized owner-seam third candidate | Changed the stage-gate materialized authority shape while leaving terminal and thermal consumers on the accepted public fixture contract | first additional related-group error was `runtime_authority_drift`; 13 additional errors occurred beyond the exact 2F+8E governance baseline |

Historical dispositions and counts above are descriptive evidence only. They do not authorize a fourth repair of any rejected candidate.

## Complete accepted-tree consumer map

| role | accepted owner/path | contract use |
| --- | --- | --- |
| template/builder owner | `p7_td_b_r6_stage_gate.build_runtime_plan_template`, `_materialized_projection`, `materialize_runtime_plan` | Builds the only production PLAN-bound materialized runtime projection |
| validator/serializer owner | `p7_td_b_r6_stage_gate.validate_materialized_runtime_plan`, `CommittedSourceAttestation`, `_attestation_value` | Owns exact schema, serialization and fail-closed validation |
| activation owner | `p7_td_b_r6_stage_gate._build_production_activation`, `validate_committed_source_attestation`, `validate_future_activation` | Resolves committed Git identity and binds it to activation/runtime bytes |
| thermal execution consumer | `measure_p7_thermal_diagnostics.validate_authorized_execution_plan`, `run_validated_td_b_r6_runtime_contract`, `run_authorized_plan`, `execute_plan` | Revalidates the public authority before the existing execution owner; runtime camera context stays separate |
| terminal consumer | `p7_td_b_r6_terminal.is_r6_materialized_plan` plus terminal replay/finalizer call to `validate_materialized_runtime_plan` | Recognizes the R6 plan and performs exact final evidence validation |
| stage-gate fixture consumer | `tests/test_p7_td_b_r6_stage_gate.py::SyntheticGitRepository.future_activation` and related fixture paths | Uses production materialization, but also assembles activation/attestation inputs |
| terminal fixture consumer | `tests/test_p7_td_b_r6_terminal.py::materialized_plan` | Handwrites the accepted nested attestation and calls private projection plus public validator |
| thermal fixture consumer | `tests/test_p7_thermal_diagnostics.py::_r6_materialized_plan_for_test` | Handwrites the same nested attestation and calls private projection plus public validator |
| full-chain thermal regression | stage-gate `SyntheticGitRepository` reused by thermal full-chain tests | Exercises the real production contract across stage-gate and thermal execution |

CodeGraph and exhaustive accepted-tree symbol search found no additional direct production callers of `validate_materialized_runtime_plan` outside the three production modules above. Indirect callers remain covered through the listed stage-gate, thermal and terminal entry points.

## Single root-cause hypothesis

The rejected route treated committed materialized identity as an internal stage-gate attestation refactor even though the nested attestation is part of the public PLAN-bound runtime authority consumed by thermal execution, terminal finalization, and their fixtures. Producer/validator evolution without one atomic consumer migration left handwritten fixture schemas stale and made consumer errors look like architecture failures.

## Selected contract strategy

`B — INTENTIONAL_PUBLIC_MATERIALIZED_RUNTIME_CONTRACT_MIGRATION`

- Keep `p7_td_b_r6_stage_gate` as the single production schema/serialization/materialization/validation owner.
- Migrate every production consumer and every fixture builder in one atomic package; do not retain old and new authority schemas as independently authorizing variants.
- Replace repeated handwritten test dictionaries with one canonical fixture construction path that delegates to the production-owned pure materialization contract. A test-support helper may own deterministic sample values, but it must not define a competing schema or validator.
- Preserve error precedence: structural/binding/reference integrity rejects before downstream semantic claims; negative regressions must prove unknown or stale authority fields still fail closed with stable underlying codes.
- Preserve the accepted frozen-plan/runtime-context split and do not broaden stage-gate, package, formal, device or scientific authority.

## Next minimum diagnostic and package boundary

The next Planner pass must freeze one atomic migration package covering:

1. the exact public contract delta and rollback to the current accepted blobs;
2. stage-gate builder/validator/activation paths;
3. thermal and terminal production consumers;
4. all three fixture construction sites and meaningful negative regressions;
5. targeted, stage-gate, terminal, thermal and related groups before one candidate full suite;
6. CodeGraph sync/query, compile/static, diff/scope, immutable artifact identity and one Planner stop.

No focused group may absorb candidate-owned errors into the governance-lineage baseline. The same candidate may not be repaired or rerun after a qualification failure.
