# Advisor 4.GUIDE unfinished work reference

**文档状态：** `ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING`

**快照日期：** `2026-08-06`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（SHA-256 `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；immutable scientific input）

**当前可执行任务数：** `1`（执行权仅来自 matching live PLAN）

**当前 active task：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**唯一 canonical next reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`（`ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_g4_06_materialized_commit_attestation_v1","snapshot_date":"2026-08-06","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","human_continuation":"ORCHESTRATOR_RESUME_EXISTING_HUMAN_GOAL_AUTONOMOUSLY","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","reference_goal":"REF-G4-COMPLETE","accepted_baseline":{"checkpoint":"7a7a3a9800af610a00d47c7cc635a066a7126555","accepted_owner_checkpoint":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"current_task":{"task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","contract":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1","owner_boundary":"EXISTING_P7_TD_B_R6_STAGE_GATE_SINGLE_OWNER","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","production_test_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"hard_changed_lines_cap":420,"full_suite_invocation_cap":1,"full_suite_retry":0,"historical_candidate_input_allowed":false,"package_or_formal_effect_allowed":false,"device_or_network_effect_allowed":false,"planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_REVIEW"},"historical_rejections":{"q1_input_allowed":false,"source_attestation_v2_ref":"refs/heads/codex/historical-g4-r6-source-attestation-v2-rejected","source_attestation_v2_commit":"ca6895a7172a38a1095358bfdc89d846d1d79c7a","source_attestation_v2_input_allowed":false},"frozen_scientific_prerequisite":{"eq_r6_state":"C","exposure_qualification":"qualified_1_2500","scientific_credit_from_current_task":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"formal_root_create_count":1,"production_loader_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"strip_zero_proven":true,"ray_zero_proven":false,"scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","human_goal_complete":false,"guide_complete":false,"scientific_result_created":false,"candidate_implementation_authorized":true,"candidate_commit_authorized":false,"full_suite_authorized":true,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"process_active":false,"automation_active":false,"allowed_next_action":"EXECUTER_EXECUTE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING"}`

## Current unfinished route

| Reference ID | 状态 | 下一真实 gate | Planner stop |
| --- | --- | --- | --- |
| `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` | `ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING` | 单一owner实现、dynamic real-Git regressions、focused及唯一full | `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_REVIEW` |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `LOCKED_PENDING_ACCEPTED_CODE_CHECKPOINT` | 新owner Planner接受、Orchestrator提交并通过post-commit probe后才可另行规划 | package/root/formal/device全锁 |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_PENDING_SEPARATE_FUTURE_PLAN` | accepted package及安全gate之后才可讨论formal | formal/device/capture全锁 |

## Engineering and safety boundary

- 当前包用materialized accepted-commit identity替换static self subject/blob与unborn-child自证；不是v2 repair、Q2或corrective suffix。
- Historical Q1、Section 2与v2 implementation均禁止读取或复用。
- GUIDE/RESEARCH immutable；Retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`；Human goal、GUIDE及scientific stage未完成。
- Package prepare/describe/root、formal、release、device/network/camera/Ray/strip/capture/analysis、G4-07、TD-C全部false。
