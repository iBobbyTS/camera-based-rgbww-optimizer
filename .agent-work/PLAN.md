# P7 retained-R3 Option B：M1-R1-S1-C1-C1-C1 physical-EOF supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-C1-GIT-ER-ONLY-PHYSICAL-EOF-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录S1-C1-C1 rejection并创建activation；Executer随后只用committed Git objects与当前
worktree ER验证exact byte topology，并用一个以完整唯一current-final S1 block为上下文的`apply_patch`，在ER physical EOF exact one
append canonical supersession payload。已内嵌的错误自报PASS块必须原位保留、不得改写或给予completion credit。

**唯一 Planner stop：**
`B2_M1_R1_S1_C1_C1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0258-p7-retained-r3-b2-m1-r1-s1-c1-c1-non-eof-review.md`；bytes `5840`，SHA-256
`96d4ce9e41bd227ce58f1a81260bd4249a71bb2ce9cf9d6d264dd354ba4717d4`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_c1_c1_git_er_only_physical_eof_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-C1-GIT-ER-ONLY-PHYSICAL-EOF-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"7b747a0ad9d019ceb59af0089d8efa85f93ff51e","expected_subject":"chore(plan): activate physical EOF evidence correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0258-p7-retained-r3-b2-m1-r1-s1-c1-c1-non-eof-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation":"376ab503622a695926f6b091a3e0a899dc5e1590","evidence_commit":"7b747a0ad9d019ceb59af0089d8efa85f93ff51e","result":"REJECTED_NON_EOF_INSERTION_CONTRACT_VIOLATION","embedded_payload_result":"PASS","embedded_payload_credit":false,"embedded_payload_disposition":"REJECTED_NON_EOF_SELF_REPORTED_PASS_IMMUTABLE","old_er":{"blob":"4ebbaef274da8ed2f90ae071f55e92cc2e178000","bytes":1243874,"sha256":"64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd"},"new_er":{"blob":"cc5e8a24fb30dc235a245118af5ea7d8e39e3306","bytes":1248695,"sha256":"75808b704952f1d4be3ad8ff273577c3962769ae47399694ee09d474fd7001d2"},"common_prefix_bytes":2579,"inserted_bytes":4821,"inserted_sha256":"b3f18c72e09cdb647a0e597fd639c3d8d216bab5678d4f0bb34f6517f97be6a2","preserved_old_suffix_bytes":1241295,"old_suffix_preserved":true,"physical_eof_append":false},"physical_eof_policy":{"current_er_must_equal_activation_committed_blob":true,"current_er_must_end_with_exact_final_anchor":true,"final_anchor_occurrences":1,"final_anchor":"COMPLETE_FINAL_REF_P7_25_R2_B2_M1_R1_S1_BLOCK_THROUGH_CLOSING_FENCE_AND_EOF","short_or_generic_anchor_prohibited":true,"apply_patch_invocations":1,"execution_result_physical_eof_appends":1,"old_prefix_bytes_required":1248695,"old_prefix_sha256_required":"75808b704952f1d4be3ad8ff273577c3962769ae47399694ee09d474fd7001d2","append_is_last_side_effect":true,"postappend_operations":0,"independent_prefix_verification_owner":"PLANNER_AFTER_ORCHESTRATOR_EVIDENCE_COMMIT"},"terminal_payload":{"heading":"## REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1 physical EOF supersession handoff","schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_c1_c1_physical_eof_supersession_v1","strict_canonical_one_line_json":true,"records_rejected_embedded_block_identity":true,"records_byte_topology":true,"records_git_counts":true,"records_zero_locks":true,"embedded_pass_completion_credit":false,"eligibility":false,"release_consumable":false,"retry":0,"fallback":0},"failure_policy":{"validation_failure_before_append":"FREEZE_FAIL_PAYLOAD_AND_APPEND_ONLY_IF_EXACT_PHYSICAL_EOF_PRECONDITIONS_REMAIN_PROVEN","physical_eof_precondition_failure":"STOP_NO_WRITE_BECAUSE_SAFE_APPEND_CANNOT_BE_PROVEN","apply_patch_failure":"STOP_NO_RETRY_NO_FALLBACK_NO_SECOND_APPEND"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-C1-GIT-ER-ONLY-PHYSICAL-EOF-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","m1_real_input_manifest_status":"REJECTED_EXECUTION_ASSERTION_SELECTOR_NOT_CONTRACTUAL","m1_real_input_supersession_status":"ACTIVE_PHYSICAL_EOF_EVIDENCE_CORRECTION","executer_dispatched":true,"device_authorized_by_this_file":false},"execution_budgets":{"git_object_reads_maximum":24,"worktree_er_reads_maximum":3,"apply_patch_invocations":1,"execution_result_physical_eof_appends":1,"tests":0,"compileall":0,"codegraph_queries":0,"codegraph_sync":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"external_path_operations":0,"old_s1_external_reads":0,"c1_external_reads":0,"retained_external_reads":0,"fresh_path_probes":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"repository_code_writes":0,"repository_test_writes":0,"new_scanners":0,"new_harnesses":0,"new_helpers":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"source_creates":0,"output_root_creates":0,"output_artifact_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_ONLY_PHYSICAL_EOF_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"archive":{"path":".agent-work/PLANS/20260801-0258-p7-retained-r3-b2-m1-r1-s1-c1-c1-non-eof-review.md","bytes":5840,"sha256":"96d4ce9e41bd227ce58f1a81260bd4249a71bb2ce9cf9d6d264dd354ba4717d4"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_M1_R1_S1_C1_C1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 exact committed gate

Orchestrator须先把S1-C1-C1 rejection及唯一active S1-C1-C1-C1写入FULL并创建activation。Expected parent exact
`7b747a0ad9d019ceb59af0089d8efa85f93ff51e`，subject exact
`chore(plan): activate physical EOF evidence correction`，changed paths exact为FULL、PLAN与本轮new archive。Activation后porcelain必须clean。

Executer只用direct read-only Git plumbing及当前ER worktree bytes验证：activation topology；PLAN/FULL each exact one machine row与required FULL
subset；archive committed bytes/SHA；activation committed ER exact blob `cc5e8a2...` / bytes `1248695` / SHA-256 `75808b7...`；rejected
activation/evidence direct-child topology与ER old/new identities；common prefix `2579`、inserted `4821`、inserted SHA
`b3f18c72...`、preserved old suffix `1241295`且physical EOF append false。Git invocation maximum `24`，worktree ER read maximum `3`，均不是必须耗尽。

只允许读取repository committed objects、PLAN/FULL/new archive与当前worktree ER。不得访问任何external path。不得创建helper、scanner、parser、
harness、scratch file或临时evidence文件。

## 2. Immutable bad block 与 payload semantics

当前ER内已有heading
`## REF-P7-25-R2-B2-M1-R1-S1-C1-C1 selector-free Git/ER supersession handoff`及schema
`p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_c1_selector_free_supersession_v1`。它们须在current committed/worktree ER各exact once，其完整
`4821` bytes identity须匹配上述SHA，但不得被编辑、移动、删除、重生成或当作successful append。

新payload在gate成功时使用`result=PASS`，但必须将旧内嵌block明确分类为
`REJECTED_NON_EOF_SELF_REPORTED_PASS_IMMUTABLE`、`completion_credit=false`，并记录old/new ER identities、exact byte topology、原S1 corrected
classification、old records immutable、accepted C1 review、successor rule、Git attempted/succeeded与所有zero locks。它不得产生manifest、retained
audit、eligibility、release或device credit。

若一般validation gate失败，在内存中冻结`result=FAIL`、first failure stage/type/message、已完成facts与Git counts；只有当current ER exact identity、
完整final anchor unique且worktree ends-with anchor这些physical EOF preconditions仍全部证明时，才允许同样在EOF append该FAIL payload。若任何physical EOF
precondition本身失败，必须no-write stop，因为安全append位置无法证明。Apply-patch失败也立即stop；retry/fallback/second append均0。

## 3. 强制 physical EOF append 方法

在唯一write前，Executer须从current committed ER取得物理最后一个完整Markdown block：heading exact
`## REF-P7-25-R2-B2-M1-R1-S1 Executer handoff`、其空行、opening fence、完整one-line JSON payload及closing fence。必须证明：

1. 该完整block byte sequence在ER中exact once；
2. current worktree ER byte-for-byte等于activation committed ER；
3. worktree ER以该完整block closing fence加final LF结束；
4. 在内存中完成新heading与single fenced one-line strict canonical JSON payload，并预先记录
   `execution_result_physical_eof_appends=1`、`apply_patch_invocations=1`、postappend operations `0`。

随后执行exact one `apply_patch`。Patch hunk的context必须是上述**完整唯一final S1 block，从heading直到physical EOF closing fence**，并只在其后增加
一个空行、新heading `## REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1 physical EOF supersession handoff`、空行、` ```json `、one-line payload、
closing fence与final LF。禁止只用generic closing fence、短JSON尾、重复section heading或其他可能在文件前部命中的模糊context。禁止使用第二次
apply_patch修正位置。

该successful apply_patch是Executer最后一个side effect。之后Git、worktree read/stat/hash/diff/status、ER read、external/process及其他操作全部0。
物理prefix/append证明由Orchestrator commit后下一轮Planner独立完成，Executer不得自验并据此增加postappend操作。

## 4. Hard locks 与 stop

External path operations总数0：旧S1/C1/retained/fresh均no read/stat/list/glob/search/probe/reuse/modify/delete。Code/test/PLAN/FULL/archive/
debug/GUIDE/RESEARCH writes0；tests/compileall/CodeGraph/implementation commit0；builder/runtime/controller/source/output0。Validator/callback/
eligibility、retained audit、release generation/qualification/copy/consumption0；network/DNS/environment/credentials/device/camera/Ray/strip/cleanup/
capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment0。

本包是`PURE_OFFLINE_GIT_ER_ONLY_PHYSICAL_EOF_SUPERSESSION`，无需Human设备授权或Advisor科学决定。Sole physical EOF append或safe no-write stop后
立即停Planner门；不得进入fresh real-input successor、validator、release或任何设备阶段。

维护性判断：本包只在不可变ledger末尾追加纠偏行，使用既有Git/ER owner并将最终prefix验证交给独立review；不新增生产抽象、helper、scanner、
parser、harness或平行evidence owner，无需架构重构。
