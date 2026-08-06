# REF-G4-06 atomic materialized runtime consumer migration roadmap

**Document status:** `ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION`

**Executable authority:** `false`

**Stable reference:** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v20_consumer_migration","document_status":"ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","executable":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","active_plan_contract_id":"G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1","reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","current_section":"ATOMIC_PUBLIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","current_section_status":"ACTIVE","contract_strategy":"B_INTENTIONAL_PUBLIC_MATERIALIZED_RUNTIME_CONTRACT_MIGRATION","schema_owner":"camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate","complete_consumer_scope":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py","tests/test_p7_td_b_r6_stage_gate.py","tests/test_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_terminal.py","tests/p7_td_b_r6_materialized_runtime_support.py"],"fixture_strategy":"ONE_CANONICAL_TEST_CONSTRUCTION_PATH_DELEGATING_TO_PRODUCTION_OWNER","parallel_authority_schema_allowed":false,"historical_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","historical_disposition":"REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED","historical_ref":"refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected","historical_commit":"4a39f9ab377d7568c37eeea8aaa78d82aaa14535","historical_candidate_input_allowed":false,"fourth_repair_allowed":false,"accepted_source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","accepted_test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","full_suite_budget":1,"full_retry":0,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_RUN_ONE_ATOMIC_CONSUMER_MIGRATION_PLAN"}`

## Atomic section boundary

The Planner must release one complete engineering package, not a sequence of preflight, fixture, natural-exit or qualification micro-plans. The package must state:

1. Strategy B intentionally migrates the public materialized runtime authority contract. Old and new authority schemas may not independently authorize execution.
2. `p7_td_b_r6_stage_gate` remains the single schema/serialization/materialization/validation owner.
3. Every production consumer and every fixture builder in the six-path ledger is in scope; repeated authority dictionaries must converge on one canonical construction path that delegates to the production owner.
4. The frozen-plan/runtime-context separation remains unchanged. Stable error precedence and negative fail-closed regressions are required.
5. Rollback is the exact accepted source/test blobs recorded above. Rejected historical implementations are not inputs.
6. Validation order is targeted, stage-gate, terminal, thermal, exact related integration, compile/static, CodeGraph sync/query and diff/scope, followed by one full suite only after every focused consumer group passes.
7. The exact related governance baseline may not absorb candidate-owned errors. The candidate has no full retry and cannot be modified after qualification failure.
8. Package, formal, release, device, network, camera, Ray, strip, capture, analysis, G4-07 and TD-C remain locked throughout this engineering section.

This roadmap is non-executable. Only the Planner-owned matching `.agent-work/PLAN.md`, after Orchestrator review and synchronized machine activation, may authorize implementation.
