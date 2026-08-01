# P7 retained-R3 Option B：M1-R1-S1-C1-C1 selector-free Git/ER supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-S1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-GIT-ER-ONLY-SELECTOR-FREE-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录S1-C1 rejection并创建activation；Executer随后只从committed Git objects与committed ER
验证exact事实，并无论validation成功或失败都exact one EOF append canonical terminal payload。不得把任何旧ER或旧narrative中的
`planner_stop`字符串作为gate，不得访问任何external path。

**唯一 Planner stop：**
`B2_M1_R1_S1_C1_C1_GIT_ER_ONLY_SELECTOR_FREE_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0244-p7-retained-r3-b2-m1-r1-s1-c1-selector-stop-review.md`；bytes `4161`，SHA-256
`d9a668d1ae77ba2c6a5833160cc3e778caed35186336f628fa5367948371afe7`；archive不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_c1_git_er_only_selector_free_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-S1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-GIT-ER-ONLY-SELECTOR-FREE-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"7dceb396ebafe1ee38ca14411851fc7bc27a34c6","expected_subject":"chore(plan): activate selector-free retained supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0244-p7-retained-r3-b2-m1-r1-s1-c1-selector-stop-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation":"7dceb396ebafe1ee38ca14411851fc7bc27a34c6","activation_parent":"5d4e903b0d747be169d68032066b023d77f3a8f9","activation_subject":"chore(plan): supersede strict retained terminal assertion","result":"PRE_APPEND_NO_WRITE_STOP","classification":"NON_CONTRACTUAL_OLD_PLANNER_STOP_SELECTOR_MISMATCH","reported_git_object_reads":12,"execution_result_appends":0,"retry":0,"fallback":0,"evidence_commit":null,"independently_verified_er_unchanged":true,"independently_verified_worktree_clean":true},"authoritative_er":{"commit":"7dceb396ebafe1ee38ca14411851fc7bc27a34c6","blob":"4ebbaef274da8ed2f90ae071f55e92cc2e178000","bytes":1243874,"sha256":"64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd"},"original_s1":{"activation":"8e5eeb134a18fc8c90627304fcff40e608dd897c","evidence_commit":"5d4e903b0d747be169d68032066b023d77f3a8f9","result":"FAIL","first_failure_type":"RuntimeError","first_failure_message":"c1_terminal_link","classification":"NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH","identity_rows_complete":true,"preacquisition_roots":2,"preacquisition_files":7,"c1_canonical_decodes":4,"retained_strict_decodes":3,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"output_artifacts":0,"eligibility":false,"release_consumable":false},"selector_policy":{"old_er_planner_stop_assertions":0,"old_archive_planner_stop_assertions":0,"old_narrative_planner_stop_assertions":0,"active_machine_contract_planner_stop_assertions_maximum":1,"old_planner_stop_values_are_data_only":true},"terminal_payload_policy":{"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_c1_selector_free_supersession_v1","append_on_validation_success":true,"append_on_validation_failure":true,"execution_result_appends":1,"failure_payload_preserves_first_failure_and_git_counts":true,"success_payload_records_supersession":true,"append_is_last_side_effect":true,"retry":0,"fallback":0},"supersession_contract":{"old_records_immutable":true,"old_fresh_namespace_disposition":"IMMUTABLE_NO_READ_NO_STAT_NO_LIST_NO_GLOB_NO_SEARCH_NO_REUSE_NO_MODIFY_NO_DELETE","corrected_failure_classification":"NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH","c1_evidence_defect":false,"production_repair_required":false,"test_repair_required":false,"runner_repair_required":false,"successor_rule":"USE_ACCEPTED_C1_REVIEW_AND_EXACT_IDENTITY_CANONICAL_DECODE_WITHOUT_UNVERSIONED_TERMINAL_FIELD_SELECTOR","eligibility":false,"release_consumable":false},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-S1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-GIT-ER-ONLY-SELECTOR-FREE-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","m1_real_input_manifest_status":"REJECTED_EXECUTION_ASSERTION_SELECTOR_NOT_CONTRACTUAL","m1_real_input_supersession_status":"ACTIVE_SELECTOR_FREE_GIT_ER_ONLY_SUPERSESSION","executer_dispatched":true,"device_authorized_by_this_file":false},"execution_budgets":{"git_object_reads_maximum":24,"execution_result_appends":1,"tests":0,"compileall":0,"codegraph_queries":0,"codegraph_sync":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"external_path_operations":0,"old_s1_external_reads":0,"c1_external_reads":0,"retained_external_reads":0,"fresh_path_probes":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"repository_code_writes":0,"repository_test_writes":0,"new_scanners":0,"new_harnesses":0,"new_helpers":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"source_creates":0,"output_root_creates":0,"output_artifact_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_ONLY_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"archive":{"path":".agent-work/PLANS/20260801-0244-p7-retained-r3-b2-m1-r1-s1-c1-selector-stop-review.md","bytes":4161,"sha256":"d9a668d1ae77ba2c6a5833160cc3e778caed35186336f628fa5367948371afe7"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_M1_R1_S1_C1_C1_GIT_ER_ONLY_SELECTOR_FREE_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 bounded Git gate

Orchestrator须先把S1-C1 rejection及唯一active S1-C1-C1写入FULL，并创建activation。Expected parent exact
`7dceb396ebafe1ee38ca14411851fc7bc27a34c6`，subject exact
`chore(plan): activate selector-free retained supersession`，changed paths exact为FULL、PLAN与本轮new archive。Activation后porcelain必须clean。

Executer只用direct read-only Git plumbing与内存中的strict JSON decode验证：activation topology；PLAN/FULL各exact one machine row及required FULL
subset；new archive committed bytes/SHA；activation ER blob/bytes/SHA；original S1 activation/evidence topology；committed ER中single S1 block的
schema/reference/contract、two roots、ordered seven files、C1 canonical `4`、retained strict `3`、first failure、zero execution/eligibility/release facts。
Git invocation是maximum `24`而非必须耗尽的exact count；可在单次invocation返回多个相关facts。

禁止对任何old ER、archive或narrative中的`planner_stop`值做exact/string/existence assertion。唯一允许的stop gate是active PLAN machine contract自己的
current `planner_stop`，最多一次。不得创建或修改repository helper、scanner、harness、parser或临时evidence文件。

## 2. Terminal payload must persist

所有validation均在一个有明确exception boundary的执行生命周期内完成。Executer从开始即累计Git attempted/succeeded、已验证facts与first failure。

- 若全部gate通过，payload `result=PASS`，记录原S1 failure的corrected classification、immutable input/evidence disposition、accepted C1 review、
  successor rule、zero credit/locks与exact committed identities。
- 若任一gate失败，立即冻结`result=FAIL` payload，记录first failure stage/type/message、Git attempted/succeeded、已完成facts；不得记录supersession
  success或任何新增credit。

两条路径都必须在内存中先令`execution_result_appends=1`，随后exact one `apply_patch`向ER EOF appendheading
`## REF-P7-25-R2-B2-M1-R1-S1-C1-C1 selector-free Git/ER supersession handoff`与single fenced one-line strict canonical JSON block。
该append是最后一个side effect；之后Git/repository/external/process操作均`0`。Append自身若失败则stop，retry/fallback仍`0/0`；不得second append。

## 3. Hard locks 与 stop

External path operations总数`0`：旧S1、C1、retained、fresh targets均no read/stat/list/glob/search/probe/reuse/modify/delete。Code/test/PLAN/FULL/
archive/debug/GUIDE/RESEARCH writes0；tests/compileall/CodeGraph/implementation commit0；builder/runtime/controller/source/output0。Validator/callback/
eligibility、retained audit、release generation/qualification/copy/consumption0；network/DNS/environment/credentials/device/camera/Ray/strip/cleanup/
capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment0。

本包是`PURE_OFFLINE_GIT_ER_ONLY_SUPERSESSION`，无需Human设备授权或Advisor科学决定。Sole append后立即停Planner门；不得进入fresh S2。

维护性边界：删除一次性old-stop selector，不新增production/test/helper/scanner/harness/parser或parallel evidence owner；无需架构重构。
