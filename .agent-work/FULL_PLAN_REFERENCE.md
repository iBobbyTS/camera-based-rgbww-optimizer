# Advisor 4.GUIDE unfinished work reference

**文档状态：** `GUIDE4_SECTION_1_DURABLE_OSERROR_REGRESSION_ACTIVE_NON_EXECUTABLE_REFERENCE`

**快照日期：** `2026-08-05`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（immutable scientific input）

**Supervisor decision：** `SUPERVISOR_ENGINEERING_RECOVERY_AND_SINGLE_REPLACEMENT_R6`

**Archived predecessor：** `.agent-work/archived/FULL_PLAN_REFERENCE-20260805-0235.md`

**当前可执行任务数：** `1`（执行权仅来自matching live PLAN；FULL本身不可执行）

**当前 active task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**唯一 canonical next reference：** `REF-G4-06-REPLACEMENT-PACKAGE`
（`ACTIVE_SECTION_1_DURABLE_OSERROR_REGRESSION_CORRECTION`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_supervisor_replacement_r6_v46","snapshot_date":"2026-08-05","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","supervisor_decision":"SUPERVISOR_ENGINEERING_RECOVERY_AND_SINGLE_REPLACEMENT_R6","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"archived_predecessor":{"path":".agent-work/archived/FULL_PLAN_REFERENCE-20260805-0235.md","bytes":8271,"sha256":"9117793dcaf8a2c11484cd54f32cdeb3b0d5af1a7cc2544af693d95d82b7f556","status":"PACKAGE_OWNER_ALIGNMENT_ACTIVE_PRE_REJECTION_SNAPSHOT_HISTORICAL_NON_EXECUTABLE"},"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-1-DURABLE-OSERROR-REGRESSION-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_1_DURABLE_OSERROR_REGRESSION_CORRECTION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_1_DURABLE_OSERROR_REGRESSION","accepted_engineering_checkpoint":"1fbe38d17ec9885dcd5b563edd90359761c51910","accepted_engineering_tree":"9535ac6bcd445898c48ff2227f659d2ea6955e60","large_change_workflow":{"current_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","section_1_sizing_failure_count":1,"section_1_semantic_failure_count":0,"section_1_validation_qualification_failure_count":1,"section_1_accepted_commit":null,"section_1_clean_review_streak":0,"section_2_status":"LOCKED"},"candidate_source_sha256":"2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11","candidate_test_sha256":"2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17","candidate_state":{"accepted":false,"committed":false,"preserved_in_place":true,"production_source_write_authorized":false,"test_write_cap":1,"only_allowed_change":"DURABLE_ANCESTRY_SUBPROCESS_OSERROR_REGRESSION","focused_after_final_change_required":true,"final_changed_line_hard_cap":330},"replacement_package_task":{"task_id":"REF-G4-06-REPLACEMENT-PACKAGE","status":"ACTIVE_SECTION_1_DURABLE_OSERROR_REGRESSION_CORRECTION","root_selected":false,"root_created":false,"prepare_count":0,"describe_count":0,"formal_authorized":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"formal_root_create_count":1,"production_loader_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"strip_zero_proven":true,"ray_zero_proven":false,"ray_zero_status":"UNPROVEN_CONNECTION_REFUSED","scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"allowed_next_action":"ADD_ONE_DURABLE_OSERROR_TEST_AND_REQUALIFY_FINAL_SECTION_1_CANDIDATE"}`

## Current unfinished route

| Reference ID | 状态 | 当前边界 | Stop |
| --- | --- | --- | --- |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `ACTIVE_SECTION_1_DURABLE_OSERROR_REGRESSION_CORRECTION` | Production冻结；仅在existing test owner持久覆盖ancestry subprocess OSError，再对最终candidate跑exact+focused+compile/CodeGraph | `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_DURABLE_REGRESSION_REVIEW` |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_PENDING_ACCEPTED_OWNER_ALIGNMENT_PACKAGE_AND_NONZERO_FREE_ZERO_GATE_PLAN` | 新fresh formal root、一次replacement launch；先证明Ray/strip zero且不得发nonzero命令 | Ray zero不能证明或任一既定hard stop时返回Supervisor |

## Candidate qualification state

- Section 1 ownership/closed shape/descriptor/Git identity/error precedence/zero-effect语义已通过Planner
  独立审查，semantic failure count保持0。
- 当前295-line candidate仍unaccepted/uncommitted。唯一缺口是focused后新增的ancestry
  `subprocess.run` OSError映射缺少repo-owned durable regression；一次性probe不替代持久测试。
- 本包冻结production source与其它test semantics，只允许加入该一条持久回归，并在最终candidate上运行
  affected exact tests和fresh stage-gate focused一次。Large-change workflow已满足，最终hard cap为330。
- Section 2、package root/prepare/describe、device/formal/release继续锁定。

## Frozen history and authority locks

- Runtime-context accepted checkpoint仍为`1fbe38d17ec9885dcd5b563edd90359761c51910`。
- Historical Section 1 stash与rejected branch保持不可读取/复用；旧formal root/package保持immutable不可访问。
- 旧formal ledger保持launch/attempt/root/loader `1/1/1/1`、capture `0/0`、retry/alternate `0/0`，
  Strip zero proven、Ray zero unproven。
- FULL不授权execution；纠偏执行权仅来自matching live PLAN。GUIDE/RESEARCH保持不变。
