# Advisor 4.GUIDE unfinished work reference

**文档状态：** `ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION`

**快照日期：** `2026-08-06`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（SHA-256 `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；immutable scientific input）

**当前可执行任务数：** `1`

**当前 active task：** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

**Canonical next reference：** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`（`ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_g4_06_consumer_migration_v1","snapshot_date":"2026-08-06","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","active_plan_contract_id":"G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","canonical_next_reference_status":"ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","reference_goal":"REF-G4-COMPLETE","contract_strategy":"B_INTENTIONAL_PUBLIC_MATERIALIZED_RUNTIME_CONTRACT_MIGRATION","schema_owner":"camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate","serialization_owner":"camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate","validation_owner":"camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate.validate_materialized_runtime_plan","consumer_scope":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py","tests/test_p7_td_b_r6_stage_gate.py","tests/test_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_terminal.py","tests/p7_td_b_r6_materialized_runtime_support.py"],"fixture_strategy":"ONE_CANONICAL_TEST_CONSTRUCTION_PATH_DELEGATING_TO_PRODUCTION_OWNER","parallel_authority_schema_allowed":false,"historical_route":{"task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","disposition":"REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED","historical_ref":"refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected","historical_commit":"4a39f9ab377d7568c37eeea8aaa78d82aaa14535","in_live_ancestry":false,"fourth_repair_allowed":false,"historical_candidate_input_allowed":false},"accepted_tree":{"source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"reassessment_note":".agent-work/debug/unresolved/20260806-g4-r6-materialized-runtime-consumer-migration.md","frozen_scientific_prerequisite":{"eq_r6_state":"C","exposure_qualification":"qualified_1_2500"},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","human_goal_complete":false,"guide_complete":false,"scientific_result_created":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_RUN_ONE_ATOMIC_CONSUMER_MIGRATION_PLAN"}`

## Current unfinished route

| Reference ID | 状态 | Owner / scope | 执行权 |
| --- | --- | --- | --- |
| `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION` | `ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION` | Existing stage-gate materialization/serialization/validation owner plus every measure/terminal consumer and fixture builder | `true` only through matching Planner PLAN; FULL itself remains non-executable |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `LOCKED_NO_ACCEPTED_CODE_CHECKPOINT` | Later offline package stage | `false` |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_NO_ACCEPTED_PACKAGE_OR_SAFETY_GATE` | Later formal stage | `false` |

## Owner and migration contract

- Strategy B is selected: the public PLAN-bound materialized runtime contract will be migrated intentionally and atomically. This is not a fourth repair of the rejected candidate and does not create another attestation identity owner.
- `p7_td_b_r6_stage_gate` remains the sole production owner for schema, serialization, materialization and validation. Measure and terminal modules are consumers, not parallel schema owners.
- The atomic scope includes all three production modules and all three fixture-construction sites listed in machine state. A canonical test support path may hold deterministic samples but must delegate schema construction/validation to the production owner.
- The accepted frozen-plan/runtime-context split remains authoritative. Error precedence must remain fail closed, and unknown/stale fields must retain stable negative coverage.
- Planner must freeze rollback to the accepted blobs, complete consumer/path ledger, fixture ledger, validation order, exact related baseline, single full-suite budget and no-retry branch before execution.

## Frozen safety and history locks

- Historical materialized candidate remains terminal rejected, historical-only and forbidden as implementation, production, package, formal or release input.
- PLAN/FULL/PLAN-FULL active count is `1/1/1` for the exact matching reference and contract; FULL/PF remain non-executable references.
- Human goal and GUIDE remain unfinished; no scientific result is created. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.
- Package/formal/release/device/network/camera/Ray/strip/capture/analysis/G4-07/TD-C permissions remain false.
