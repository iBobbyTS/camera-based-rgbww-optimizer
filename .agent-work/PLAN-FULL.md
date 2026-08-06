# REF-G4-06 materialized commit attestation large-change roadmap

**Document status:** `ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Architecture:** `MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v13","document_status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","executable":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_section":"MATERIALIZED_COMMIT_ATTESTATION_OWNER","current_section_status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","orchestration_branch":"codex/g4-r6-owner-alignment-large-change","intake_checkpoint":"7a7a3a9800af610a00d47c7cc635a066a7126555","accepted_owner_checkpoint":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","accepted_source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","accepted_test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","historical_q1_input_allowed":false,"historical_v2_input_allowed":false,"maintainability_preflight_required":true,"parallel_attestation_owner_allowed":false,"static_self_subject_authority_allowed":false,"static_self_blob_authority_allowed":false,"candidate_qualification_must_not_require_unborn_commit":true,"post_accept_materialized_commit_identity_required":true,"package_preparation_in_current_section":false,"expected_changed_lines_min":220,"expected_changed_lines_max":380,"hard_changed_lines_cap":420,"candidate_implementation_authorized":true,"candidate_commit_authorized":false,"full_suite_authorized":true,"full_suite_invocation_cap":1,"full_retry":0,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_EXECUTE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING"}`

## Current section

Active PLAN将maintainability preflight、single-owner replacement、dynamic real-Git positive/negative tests、targeted/focused/compile/static/CodeGraph/scope、唯一full与ER handoff合并为一个package。候选接受后由Orchestrator创建exact code checkpoint并执行read-only post-commit probe；package preparation仍是后续独立边界。

## Hard locks

- 不读取或复用historical rejected implementation；不新增parallel controller或第二identity authority。
- 不访问package/formal roots、external experiment payload、设备或网络。
- Full budget/retry为 `1/0`；候选full允许green或exact既有2 failures + 8 errors governance-lineage baseline，任何新增或changed-owner非绿均拒绝。
