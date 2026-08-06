# Advisor 4.GUIDE unfinished work reference

**文档状态：** `ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION`

**快照日期：** `2026-08-06`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（SHA-256 `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；immutable scientific input）

**当前可执行任务数：** `1`（执行权仅来自 matching live PLAN）

**当前 active task：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**唯一 canonical next reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`（`ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_g4_06_materialized_attestation_qualification_continuation","snapshot_date":"2026-08-06","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","human_continuation":"ORCHESTRATOR_RESUME_EXISTING_HUMAN_GOAL_AUTONOMOUSLY","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-QUALIFICATION-CONTINUATION-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION","reference_goal":"REF-G4-COMPLETE","accepted_restart":{"checkpoint":"7a7a3a9800af610a00d47c7cc635a066a7126555","activation_parent":"f39539ff6c948d9adfa90a5b4eeb6b1337d7763a","accepted_owner_checkpoint":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"current_task":{"task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","status":"ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION","contract":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-QUALIFICATION-CONTINUATION-V1","architecture_attempt":2,"architecture_attempt_increment":0,"prior_materialized_architecture_production_integration_failures":1,"production_failure_increment_from_reviewed_targeted":0,"continuation_class":"SAME_CANDIDATE_HARNESS_ACCOUNTING_CONTINUATION_NOT_NEW_ARCHITECTURE_ATTEMPT","owner_boundary":"EXISTING_P7_TD_B_R6_STAGE_GATE_SINGLE_OWNER","production_source_frozen_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","production_source_write_cap":0,"test_fixture_contract_correction_cap":1,"hard_changed_lines_cap":480,"full_suite_invocation_cap":1,"full_suite_retry":0,"rejected_candidate_input_allowed":false,"package_or_formal_effect_allowed":false,"device_or_network_effect_allowed":false,"planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_QUALIFICATION_CONTINUATION_REVIEW"},"reviewed_disposition":"REJECTED_TARGETED_AS_QUALIFICATION_RESULT_ACCEPTED_HARNESS_ACCOUNTING_CONTINUATION_NO_PRODUCTION_FAILURE","reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0152.md","sha256":"f31c1661894e1f9a072e4e727962e021b65b227a5c8d8bc53551dfbdad166712"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0152.md","sha256":"1af558a51dccd8cd64c4e83af2324e674bc8b853534b5e9dfc9add5bcbc33977"}},"frozen_scientific_prerequisite":{"eq_r6_state":"C","exposure_qualification":"qualified_1_2500","scientific_credit_from_current_task":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"formal_root_create_count":1,"production_loader_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"strip_zero_proven":true,"ray_zero_proven":false,"scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","human_goal_complete":false,"guide_complete":false,"scientific_result_created":false,"candidate_implementation_authorized":true,"candidate_commit_authorized":false,"full_suite_authorized":true,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_EXECUTE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION"}`

## Current unfinished route

| Reference ID | 状态 | 下一真实 gate | Planner stop |
| --- | --- | --- | --- |
| `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` | `ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION` | 精确修正一个 stale positive fixture；production source 零写入；完成 focused/related/compile/CodeGraph/唯一 full qualification | `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_QUALIFICATION_CONTINUATION_REVIEW` |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `LOCKED_PENDING_ACCEPTED_CODE_CHECKPOINT` | 当前 owner 接受、提交及 post-commit probe 后才可另行规划 | package/root/formal/device 全锁 |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_PENDING_SEPARATE_FUTURE_PLAN` | accepted package 及安全 gate 后才可讨论 formal | formal/device/capture 全锁 |

## Engineering and safety boundary

- V2 production CLI 与 measure CLI targeted propagation 已通过；唯一 non-green 是 stale positive test fixture call shape。该结果不增加 architecture attempt 或 production failure 计数。
- 当前 continuation 复用同一未提交候选，只允许一个精确 test fixture 修正；production source SHA-256 必须保持冻结值，之后连续完成剩余 qualification。
- V1、Q1、Section 2、source-attestation-v2 及所有 rejected implementation 均禁止读取或复用。
- GUIDE/RESEARCH immutable；Retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`；Human goal、GUIDE 及 scientific stage 未完成。
- Package prepare/describe/root、formal、release、device/network/camera/Ray/strip/capture/analysis、G4-07、TD-C 全部 false。
