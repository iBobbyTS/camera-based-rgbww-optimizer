# REF-G4-06-REPLACEMENT-PACKAGE Planner failure stop

**计划状态：** `NON_EXECUTABLE_WAITING_ORCHESTRATOR_LARGE_CHANGE_WORKFLOW`

**Executable：** `false`

**Active task count：** `0`

**Reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Reviewed contract：** `G4-R6-REPLACEMENT-PACKAGE-OWNER-ALIGNMENT-V1`

**唯一 Planner stop：** `RETURN_FOR_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-REPLACEMENT-PACKAGE-OWNER-ALIGNMENT-FAILURE-REVIEW-V1","plan_status":"NON_EXECUTABLE_WAITING_ORCHESTRATOR_LARGE_CHANGE_WORKFLOW","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"WAITING_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL","single_current_action":"orchestrator_preserve_rejected_dirty_candidate_and_activate_required_repo_large_change_workflow","planner_stop":"RETURN_FOR_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL","review_disposition":"REJECTED_SOURCE_TEST_CHANGED_LINE_HARD_CAP_BREACHED_CANDIDATE_INCOMPLETE_UNVALIDATED","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260805-0226.md","bytes":18343,"sha256":"650cb336d3cb195d86321a2d56e94d97527048a614f6f983b5d8e608d5f3b317"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0226.md","bytes":7390,"sha256":"2a5aec2db4120cb6a3fd91d5cf9c6c0f72226884a582011d3b048cbb17a0ba24"},"observed_candidate_numstat":{"historical_source_added":131,"historical_source_deleted":68,"historical_test_added":70,"historical_test_deleted":36,"historical_total":305,"live_source_added":126,"live_source_deleted":68,"live_test_added":70,"live_test_deleted":36,"live_total":300,"hard_cap":300,"breach_not_revoked_by_later_compaction":true},"validation":{"targeted_run":false,"focused_run":false,"full_discovery_invocation_count":0,"candidate_complete":false,"candidate_validated":false,"candidate_committed":false},"authority_counts":{"package_root_selection":0,"package_root_check":0,"package_root_create":0,"public_prepare":0,"public_describe":0,"old_package_access":0,"old_formal_root_access":0,"device":0,"network":0,"camera":0,"ray":0,"strip":0,"capture":0,"cleanup":0,"formal":0,"release":0},"dirty_candidate_disposition":{"preserve_as_rejected_branch_snapshot":true,"accepted_input":false,"production_truth":false,"commit_to_main":false,"reuse_as_read_only_design_input_only":true,"destructive_reset_clean_checkout_allowed":false,"archive_branch":"codex/g4-r6-owner-alignment-rejected-305","large_change_branch":"codex/g4-r6-owner-alignment-large-change","stable_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","corrective_suffix_allowed":false},"large_change_workflow":{"applicable_top_level_agents_over_300_rule_found":true,"required":true,"git_branch_required":true,"plan_full_required":true,"section_subagent_commit_clean_review_loop_required":true,"ordinary_bounded_candidate_rerelease_allowed":false,"smaller_complete_design_proven":false,"reason":"nontrivial_candidate_observed_305_and_effective_top_level_agents_rule_requires_large_change_workflow_at_300_or_more"},"descriptor_guard_contract":{"descriptor_reference_drift_precedence_retained":true,"reference_drift_test_expected_code":"descriptor_reference_drift","reference_consistent_secret_fixture_required":true,"reference_consistent_historical_fixture_required":true},"package_prepare_authorized":false,"package_describe_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Planner review disposition

当前 candidate 被拒绝，精确处置为：

`REJECTED_SOURCE_TEST_CHANGED_LINE_HARD_CAP_BREACHED_CANDIDATE_INCOMPLETE_UNVALIDATED`

理由是同一次 candidate 曾观测到 production/test 合计 `305` changed lines，超过 PLAN 冻结的 `300` hard cap。已经发出的机械压缩把 live numstat 降到 `300`，但不能撤销已经命中的 hard stop。Candidate 在停止时仍不完整、未验证、未提交；targeted、focused、compile、post-change CodeGraph 和 full discovery 均未运行。因此不得验收、不得继续 Executer 修补、不得把 live `300` 解释为重新获得授权。

这是工程变更规模与执行合同失败，不是 scientific、formal、quality、release、device 或 Human/Advisor 阻塞。所有 package-root、public prepare/describe、historical-root、device、network、camera、Ray、strip、capture、formal 和 release 调用均为 `0`。

## 2. Test-contract finding retained for the next engineering design

完整性优先的 `descriptor_reference_drift` 行为必须保留。一个同时修改 `frozen-inputs.json` 内容却仍引用旧 bytes/SHA 的 fixture，首先违反跨文件引用完整性；它应明确期待 `descriptor_reference_drift`。

专属内容 guard 必须使用内部引用一致的独立 fixture 才可达：

- reference-consistent secret fixture → `secret_material_prohibited`；
- reference-consistent historical fixture → `historical_input_prohibited`。

这四个入口/内容组合是同一错误优先级合同，不是四个安全缺陷。该事实不撤销本次 305-line hard stop，也不授权在当前 candidate 上继续修改。

## 3. Required dirty-candidate disposition

Orchestrator 必须以可恢复、非破坏方式处理当前 dirty source/test draft：

1. 在当前 `main` activation HEAD 上创建本地历史分支 `codex/g4-r6-owner-alignment-rejected-305`。
2. 只 stage 并 commit 两个 source/test dirty paths，作为明确 rejected、incomplete、unvalidated 的 draft snapshot；不得提交到 `main`，不得宣称 accepted，也不得消费其输出。
3. Planner review docs、archives、debug disposition 保持 unstaged，然后使用 `git switch main`。因为 main ref 未移动，source/test 会随分支切换回到 accepted activation tree，Planner docs 可作为未提交工作继续携带；不得使用 destructive reset、clean、checkout 或 restore。
4. Orchestrator 在 `main` 独立审查并提交 Planner review docs，更新 FULL 后，从该 clean review commit 创建 `codex/g4-r6-owner-alignment-large-change`。
5. Rejected branch 只允许作为 historical/read-only design input；禁止直接 cherry-pick 其 source/test candidate 为 production truth。

## 4. Required next orchestration state

Orchestrator 应在 FULL 中把同一稳定 task `REF-G4-06-REPLACEMENT-PACKAGE` 设为等待 required repo large-change workflow，不创建 corrective suffix 或新实验 root。需要的状态至少包括：

- status: `WAITING_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL`；
- current PLAN active task count: `0`；
- current PLAN executable: `false`；
- canonical next: `REF-G4-06-REPLACEMENT-PACKAGE`；
- rejected candidate disposition及其本地历史分支/commit identity；
- 当前有效顶层AGENTS明确要求非平凡修改可能达到或超过300行时使用Git branch、PLAN-FULL及section/subagent/commit/clean-review loop；historical305已触发该强制流程；
- large-change branch identity；
- `PLAN-FULL` required，按section/subagent/commit/clean-review loop收敛；
- package root、prepare/describe、formal、device、network、camera、Ray、strip、capture、release全部未授权；
- retained R3和历史 formal ledger不变。

当前没有足够证据证明一个完整、可验证且不规避阈值的更小设计可以重新按普通 `<=300` candidate 释放。后续仍在同一个reference task内解决，但必须由Orchestrator建立branch + PLAN-FULL + section/subagent/commit/clean-review workflow；不需要Human或Advisor。

## 5. Frozen locks

本 PLAN 不授权 Executer、代码修改、测试运行、package root、public prepare/describe、旧 package/formal root、device/network/camera/Ray/strip/capture/cleanup/formal、release consumption、analysis、G4-07、TD-C 或 Git commit。

唯一 stop 为：

`RETURN_FOR_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL`
