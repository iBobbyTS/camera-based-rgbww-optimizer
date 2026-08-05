# Advisor 4.GUIDE unfinished work reference

**文档状态：** `ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING`

**快照日期：** `2026-08-05`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（SHA-256 `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；immutable scientific input）

**Human continuation：** `ORCHESTRATOR_RESUME_EXISTING_HUMAN_GOAL_AUTONOMOUSLY`

**当前可执行任务数：** `1`（执行权仅来自 matching live PLAN；FULL 本身不授权执行）

**当前 active task：** `REF-G4-06-SOURCE-ATTESTATION-V2`

**唯一 canonical next reference：** `REF-G4-06-SOURCE-ATTESTATION-V2`（`ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_g4_06_attestation_v2_v1","snapshot_date":"2026-08-05","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","human_continuation":"ORCHESTRATOR_RESUME_EXISTING_HUMAN_GOAL_AUTONOMOUSLY","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":1,"active_task":"REF-G4-06-SOURCE-ATTESTATION-V2","active_plan_contract_id":"G4-R6-SOURCE-ATTESTATION-V2-ENGINEERING-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-SOURCE-ATTESTATION-V2","canonical_next_reference_task":"REF-G4-06-SOURCE-ATTESTATION-V2","canonical_next_reference_status":"ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SOURCE_ATTESTATION_V2_ENGINEERING","reference_goal":"REF-G4-COMPLETE","live_intake":{"branch":"codex/g4-r6-owner-alignment-large-change","checkpoint":"641482706e5efebc81f1f55dba284cffd58b8355","tree":"d1db4d447ec8554683f1e60368f8dcee1d746d69","accepted_source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","accepted_test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"source_attestation_v2_task":{"task_id":"REF-G4-06-SOURCE-ATTESTATION-V2","status":"ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING","owner_boundary":"SINGLE_REPO_OWNED_SOURCE_ATTESTATION_SEAM","architecture":"VALIDATE_FROZEN_CANDIDATE_BYTES_THEN_ATTEST_EXACT_COMMIT_BLOBS_BEFORE_SEPARATE_PACKAGE_PREPARATION","reason":"DECOUPLE_ENGINEERING_CANDIDATE_QUALIFICATION_FROM_FUTURE_PACKAGE_DESCRIPTOR_IDENTITY","allowed_scope":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py","optional_minimal_owner_extraction_if_maintainability_preflight_requires","agent_work_execution_evidence"],"historical_q1_input_allowed":false,"package_or_formal_effect_allowed":false,"device_or_network_effect_allowed":false,"planner_stop":"RETURN_FOR_G4_06_SOURCE_ATTESTATION_V2_ENGINEERING_REVIEW"},"historical_q1":{"disposition":"REJECTED_IMMUTABLE_Q_TOPOLOGY_VALIDATION_COMMITTED_SOURCE_CANDIDATE_BLOB_DRIFT","ref":"refs/heads/codex/historical-g4-r6-immutable-qualification-q1-rejected","commit":"b5839d38ffa0c27bd5a6232a890cca3af0b8e7d9","implementation_read_or_reuse_allowed":false,"merge_cherry_pick_rebase_copy_allowed":false,"production_package_formal_release_input_allowed":false,"planner_archive":".agent-work/archived/PLAN-20260805-2300.md","execution_archive":".agent-work/archived/EXECUTION_RESULT-20260805-2300.md","full_archive":".agent-work/archived/FULL_PLAN_REFERENCE-20260805-2303.md"},"frozen_scientific_prerequisite":{"eq_r6_state":"C","exposure_qualification":"qualified_1_2500","scientific_credit_from_current_task":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"formal_root_create_count":1,"production_loader_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"strip_zero_proven":true,"ray_zero_proven":false,"scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","human_goal_complete":false,"guide_complete":false,"scientific_result_created":false,"candidate_implementation_authorized":true,"candidate_commit_authorized":false,"full_suite_authorized":true,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"allowed_next_action":"EXECUTER_EXECUTE_SOURCE_ATTESTATION_V2_ENGINEERING_PACKAGE"}`

## Current unfinished route

| Reference ID | 状态 | 目标边界 | Planner stop |
| --- | --- | --- | --- |
| `REF-G4-06-SOURCE-ATTESTATION-V2` | `ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING` | 在 accepted tree 上独立建立单一 source-attestation v2 seam；候选验证与未来 package descriptor identity 分离 | `RETURN_FOR_G4_06_SOURCE_ATTESTATION_V2_ENGINEERING_REVIEW` |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `LOCKED_PENDING_ACCEPTED_V2_CODE_CHECKPOINT` | 仅在 v2 工程 owner terminal accepted 且 exact commit/blob attestation 后，由新 PLAN 决定 offline package preparation | package/root/formal/device全锁 |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_PENDING_SEPARATE_FUTURE_PLAN` | 仅在 replacement package 与 zero safety gate 分别接受后，才可讨论 formal launch | formal/device/capture全锁 |

## Engineering boundary

- 新路线不是 Q1 rename、repair 或 retry，不读取、不复制、不合并 historical Q1 implementation。
- 资格验证首先冻结当前 candidate source/test bytes 和 exact scope；targeted/focused/full只验证这组冻结bytes。代码接受后由 Orchestrator 创建 focused commit，并以 read-only Git probe证明 commit blobs与已测bytes exact一致。
- Downstream package descriptor只能在该 code checkpoint terminal accepted 后由后续独立 PLAN 构造；当前工程包不得 prepare、describe、probe、选择或创建 package root。
- `p7_td_b_r6_stage_gate.py` 是大型 owner。Planner必须先做 maintainability preflight；若直接修改会增加 god-object、并行 semantic owner或重复 serialization/validation，允许一个最小 canonical extraction并配套 regression，但不得无关重构。
- 普通 harness/fixture问题可在同一 package 内做一次 bounded correction；只有真实 source-attestation owner缺陷重复成立才累计 same-boundary failure。

## Current locks

- GUIDE/RESEARCH immutable；不需要 Advisor。
- Package prepare/describe/root、replacement formal、release consumption、device/network/camera/Ray/strip/capture/analysis、G4-07、TD-C全部为false。
- Retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`；旧formal ledger保持不变。
- Human goal、GUIDE、scientific stage均未完成。
