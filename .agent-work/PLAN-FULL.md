# REF-G4-06 materialized commit attestation large-change roadmap

**Document status:** `ACTIVE_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v17","document_status":"ACTIVE_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION","executable":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_section":"MATERIALIZED_COMMIT_ATTESTATION_NATURAL_EXIT_QUALIFICATION","current_section_status":"ACTIVE_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-NATURAL-EXIT-QUALIFICATION-V1","architecture_attempt":2,"architecture_attempt_increment":0,"prior_materialized_architecture_production_integration_failures":1,"production_failure_increment":0,"candidate_failure_increment":0,"controller_harness_invalid_event_count_since_v2":4,"continuation_class":"SAME_CANDIDATE_ZERO_WRITE_NATURAL_EXIT_QUALIFICATION","orchestration_branch":"codex/g4-r6-owner-alignment-large-change","production_source_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","test_source_sha256":"c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc","production_source_write_cap":0,"test_source_write_cap":0,"hard_changed_lines_cap":480,"focused_natural_exit_invocation_cap":1,"full_suite_authorized":true,"full_suite_invocation_cap":1,"full_retry":0,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_EXECUTE_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION"}`

## Current section

继承 targeted `4/4`，不得重跑。Candidate source/test identities 冻结且 write cap 为 `0/0`。当前 PLAN 先取得一次 `-v` focused natural exit 完整证据；若 green，连续完成 related、compile/static、CodeGraph、identity freeze 与唯一 full suite。接受后由 Orchestrator 创建 exact code checkpoint并执行 read-only post-commit attestation probe。

## Hard locks

- 不读取或复用任何 rejected implementation；不新增 parallel controller、candidate、task suffix 或第二 identity authority。
- 不访问 package/formal roots、external experiment payload、设备或网络。
- Full budget/retry 为 `1/0`；只允许 green 或 exact 既有 `2F+8E` governance baseline。
