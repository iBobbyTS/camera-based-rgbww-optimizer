# Advisor 4.GUIDE unfinished work reference

**文档状态：** `MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_FAILURE_TERMINAL_CROSS_ARCHITECTURE_REASSESSMENT_REQUIRED`

**快照日期：** `2026-08-06`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（SHA-256 `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；immutable scientific input）

**当前可执行任务数：** `0`

**当前 active task：** `null`

**Canonical historical reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`（`MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_FAILURE_TERMINAL_CROSS_ARCHITECTURE_REASSESSMENT_REQUIRED`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_g4_06_materialized_third_failure_terminal","snapshot_date":"2026-08-06","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":0,"active_task":null,"active_plan_contract_id":null,"current_plan_active_task_count":0,"current_plan_active_task":null,"canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_FAILURE_TERMINAL_CROSS_ARCHITECTURE_REASSESSMENT_REQUIRED","executable":false,"full_is_non_executable_reference":true,"plan_status":"MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_FAILURE_TERMINAL_CROSS_ARCHITECTURE_REASSESSMENT_REQUIRED","reference_goal":"REF-G4-COMPLETE","terminal_task":{"task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","disposition":"REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED","architecture_attempt":2,"same_boundary_substantive_failure_count":3,"production_failure_count_after_review":3,"production_retry_count":0,"candidate_retry_count":0,"full_invocation_count":0,"full_retry_count":0,"fourth_repair_allowed":false,"corrective_suffix_allowed":false,"new_candidate_allowed":false,"new_architecture_execution_package_allowed":false,"historical_candidate_input_allowed":false},"historical_isolation":{"ref":"refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected","commit":"4a39f9ab377d7568c37eeea8aaa78d82aaa14535","in_live_ancestry":false,"production_input_allowed":false,"package_input_allowed":false,"formal_input_allowed":false,"release_input_allowed":false,"candidate_source_sha256":"c4d04e0c4045520ffd9d262190cc9d9edd3b445c32afe2434f741cc3df7dd316","candidate_test_sha256":"639999ab7615a8250eec1d3b6974e3516493941786009292f68257cb96dedb45"},"accepted_tree_restored":{"source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0257.md","sha256":"3e40687d30c0d5ae5ee87fc673ee551f00e26a8bf10697fa235fb6758089a43e"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0257.md","sha256":"75256ecbaf49cf3efe2f7b61234b3572344636901acb7675a5c901488bac1ddd"},"full_pre_rewrite":{"path":".agent-work/archived/FULL_PLAN_REFERENCE-20260806-0300.md","sha256":"0b7cf9ca9f6be174463d20373f580422409525767309c744bd3464984dc046fe"}},"validation":{"targeted":{"tests":14,"exit":0},"stage_gate_focused":{"tests":54,"exit":0},"related":{"tests":95,"exit":1,"failures":2,"errors":21,"allowed_baseline_failures":2,"allowed_baseline_errors":8,"additional_changed_owner_errors":13,"error_code":"runtime_authority_drift"},"full":{"invocations":0,"retries":0}},"frozen_scientific_prerequisite":{"eq_r6_state":"C","exposure_qualification":"qualified_1_2500","scientific_credit_from_terminal_task":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","human_goal_complete":false,"guide_complete":false,"scientific_result_created":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"process_active":false,"automation_active":false,"allowed_next_action":"CROSS_ARCHITECTURE_REASSESSMENT_ONLY_AFTER_NEW_ORCHESTRATOR_ROUTE_NOT_CURRENT_PLAN_EXECUTION"}`

## Terminal route state

| Reference ID | 状态 | 执行权 |
| --- | --- | --- |
| `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` | `REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED` | `false`；禁止第四次 repair、suffix、same candidate 或 historical input |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `LOCKED_NO_ACCEPTED_CODE_CHECKPOINT` | `false` |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_NO_ACCEPTED_PACKAGE_OR_SAFETY_GATE` | `false` |

## Evidence and safety boundary

- Rejected candidate 已完整冻结于 historical-only ref/commit，且不在 accepted orchestration ancestry；live source/test 已恢复 accepted blobs。
- Terminal related evidence为 `95 tests / 2F+21E`，较允许基线新增13个 `runtime_authority_drift` cross-owner integration errors；这不是科学、设备、formal 或 release 结果。
- Human goal、GUIDE 与 scientific stage 均未完成；retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- PLAN/FULL/PF 均无 active executable task。未来 cross-architecture reassessment 必须从 accepted tree 新建稳定路线；不得恢复本 materialized candidate 或读取 historical implementation作为输入。
- Package/formal/release/device/network/camera/Ray/strip/capture/analysis、G4-07、TD-C 权限全部 false。
