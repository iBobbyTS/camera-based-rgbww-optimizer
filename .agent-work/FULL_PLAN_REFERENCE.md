# Advisor 4.GUIDE unfinished work reference

**文档状态：** `GUIDE4_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_ACTIVE_NON_EXECUTABLE_REFERENCE`

**快照日期：** `2026-08-05`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`（immutable scientific input）

**Supervisor decision：** `SUPERVISOR_ENGINEERING_RECOVERY_AND_SINGLE_REPLACEMENT_R6`

**Archived predecessor：** `.agent-work/archived/FULL_PLAN_REFERENCE-20260805-0235.md`

**当前可执行任务数：** `1`（执行权仅来自matching live PLAN；FULL本身不可执行）

**当前 active task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**唯一 canonical next reference：** `REF-G4-06-REPLACEMENT-PACKAGE`
（`ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_supervisor_replacement_r6_v50","snapshot_date":"2026-08-05","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","supervisor_decision":"SUPERVISOR_ENGINEERING_RECOVERY_AND_SINGLE_REPLACEMENT_R6","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_LOCKS_ONLY","completed_content_allowed":false,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-ACCEPTED-REVIEW-FINDING-REPAIR-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","accepted_engineering_checkpoint":"1fbe38d17ec9885dcd5b563edd90359761c51910","accepted_engineering_tree":"9535ac6bcd445898c48ff2227f659d2ea6955e60","large_change_workflow":{"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted_commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","section_1_accepted_tree":"656fee670f289b0a20fea1a8c015762afd44a5c0","section_1_clean_review_streak":2,"section_2_base_code_commit":"7d02562db0afcffaa8f2a341345235a6310b654c","section_2_clean_review_streak":0,"section_2_status":"ACTIVE_ACCEPTED_REVIEW_FINDING_REPAIR","accepted_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"],"review_reports":[{"path":".agent-work/reviews/20260805-g4-r6-section2-round1.md","sha256":"cdb6ea0246f0f0c0c32f18901262c55396e429c872f6db02cca9647c59a04657"},{"path":".agent-work/reviews/20260805-g4-r6-section2-round2.md","sha256":"8e3b945ba2f6d68479fefdb002e0f793ea8db46cbbade5952b100a2a7a9a5c58"}]},"replacement_package_task":{"task_id":"REF-G4-06-REPLACEMENT-PACKAGE","status":"ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","root_selected":false,"root_created":false,"prepare_count":0,"describe_count":0,"formal_authorized":false},"historical_formal_ledger":{"classification":"ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT","formal_launch_count":1,"formal_attempt_count":1,"formal_root_create_count":1,"production_loader_count":1,"logical_capture_count":0,"physical_capture_count":0,"retry":0,"alternate_root":0,"strip_zero_proven":true,"ray_zero_proven":false,"ray_zero_status":"UNPROVEN_CONNECTION_REFUSED","scientific_or_quality_credit":false},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"allowed_next_action":"REPAIR_ACCEPTED_SECTION_2_AUTHORITY_AND_PROVENANCE_FINDINGS"}`

## Current unfinished route

| Reference ID | 状态 | 当前边界 | Stop |
| --- | --- | --- | --- |
| `REF-G4-06-REPLACEMENT-PACKAGE` | `ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR` | 同一existing owner内关闭authority vocabulary与accepted-engineering cross-binding两个accepted findings | `RETURN_FOR_G4_06_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_REVIEW` |
| `REF-G4-06-REPLACEMENT-R6` | `LOCKED_PENDING_ACCEPTED_OWNER_ALIGNMENT_PACKAGE_AND_NONZERO_FREE_ZERO_GATE_PLAN` | 新fresh formal root、一次replacement launch；先证明Ray/strip zero且不得发nonzero命令 | Ray zero不能证明或任一既定hard stop时返回Supervisor |

## Accepted Section 1 checkpoint and Section 2 boundary

- Section 1已由Planner接受并提交为`5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74`，
  tree `656fee670f289b0a20fea1a8c015762afd44a5c0`；exact source/test两路径。
- Durable raised-`OSError`、returncode-2与nonancestor三类语义均由existing test owner覆盖；最终
  affected `2/2`、focused `51/51`，Section 1 full discovery为0。
- 两个独立xhigh review报告均为clean/mergeable，SHA-256记录在machine state；clean streak为2。
- Section 2实现由Planner判定semantically acceptable但未最终接受；无效`-t .`调用在收集前失败，保留为
  harness-contract历史且不消耗有效full collection。当前PLAN冻结候选字节，只补齐最终qualification。
- Package root/prepare/describe、device/formal/release仍锁定。
- Section 2 base code commit `7d02562`的两轮review均非clean；clean streak已重置为0。
  Orchestrator接受`REV-S2-AUTH-001`与`REV-S2-PROV-001`，只授权同一owner内的最小repair wave。

## Frozen history and authority locks

- Runtime-context accepted checkpoint仍为`1fbe38d17ec9885dcd5b563edd90359761c51910`。
- Historical Section 1 stash与rejected branch保持不可读取/复用；旧formal root/package保持immutable不可访问。
- 旧formal ledger保持launch/attempt/root/loader `1/1/1/1`、capture `0/0`、retry/alternate `0/0`，
  Strip zero proven、Ray zero unproven。
- FULL不授权execution；纠偏执行权仅来自matching live PLAN。GUIDE/RESEARCH保持不变。
