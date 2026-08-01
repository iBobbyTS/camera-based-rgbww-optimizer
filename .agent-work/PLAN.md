# P7 retained-R3 Option B：M1-R1-S1-C1 Git/ER-only terminal assertion supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-S1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-GIT-ER-ONLY-TERMINAL-ASSERTION-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录S1 rejection并创建activation；Executer随后只从committed Git objects与committed ER
append一条canonical supersession，纠正`c1_terminal_link`为non-contractual execution selector mismatch。不得读取或探测任何external path。

**唯一 Planner stop：**
`B2_M1_R1_S1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0236-p7-retained-r3-b2-m1-r1-s1-terminal-link-review.md`；bytes `5457`，SHA-256
`00f06209f889a2a80a700eb43f2146bcfbc199fea0103cd86d12a935322a0215`；archive不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_git_er_only_terminal_assertion_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-S1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-GIT-ER-ONLY-TERMINAL-ASSERTION-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"5d4e903b0d747be169d68032066b023d77f3a8f9","expected_subject":"chore(plan): supersede strict retained terminal assertion","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0236-p7-retained-r3-b2-m1-r1-s1-terminal-link-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation":"8e5eeb134a18fc8c90627304fcff40e608dd897c","evidence_commit":"5d4e903b0d747be169d68032066b023d77f3a8f9","evidence_parent":"8e5eeb134a18fc8c90627304fcff40e608dd897c","evidence_subject":"chore(evidence): record strict retained terminal link stop","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"evidence_er_blob":"4ebbaef274da8ed2f90ae071f55e92cc2e178000","evidence_er_bytes":1243874,"evidence_er_sha256":"64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd","result":"FAIL","first_failure_type":"RuntimeError","first_failure_message":"c1_terminal_link","classification":"NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH","c1_evidence_defect":false,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"output_artifacts":0},"accepted_partial_boundary":{"preacquisition_roots":2,"preacquisition_files":7,"c1_canonical_decodes":4,"retained_strict_decodes":3,"retained_canonical_reencode":0,"retained_schema_validation":0,"retained_scientific_validation":0,"identity_rows_complete":true,"identity_credit":"FAILURE_EVIDENCE_ONLY","eligibility":false,"release_consumable":false},"accepted_c1_review":{"archive":".agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md","decision":"ACCEPTED_EXACT_PATH_OWNER_INDEX_ONLY","terminal_linkage_previously_independently_accepted":true,"reopen":false},"supersession_contract":{"old_record_immutable":true,"old_fresh_namespace_disposition":"IMMUTABLE_NO_READ_NO_STAT_NO_LIST_NO_GLOB_NO_SEARCH_NO_REUSE_NO_MODIFY_NO_DELETE","corrected_failure_classification":"NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH","invented_or_reconstructed_identity_rows":false,"c1_repair_required":false,"production_repair_required":false,"test_repair_required":false,"runner_repair_required":false,"successor_rule":"USE_ACCEPTED_C1_REVIEW_AND_EXACT_IDENTITY_CANONICAL_DECODE_WITHOUT_UNVERSIONED_TERMINAL_FIELD_SELECTOR"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-S1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-GIT-ER-ONLY-TERMINAL-ASSERTION-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","m1_real_input_manifest_status":"REJECTED_EXECUTION_ASSERTION_SELECTOR_NOT_CONTRACTUAL","m1_real_input_supersession_status":"ACTIVE_GIT_ER_ONLY_TERMINAL_ASSERTION_SUPERSESSION","executer_dispatched":true,"device_authorized_by_this_file":false},"execution_budgets":{"git_object_reads":12,"execution_result_appends":1,"tests":0,"compileall":0,"codegraph_queries":0,"codegraph_sync":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"external_path_operations":0,"old_s1_external_reads":0,"c1_external_reads":0,"retained_external_reads":0,"fresh_path_probes":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"input_writes":0,"retained_artifact_writes":0,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"source_creates":0,"output_root_creates":0,"output_artifact_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_ONLY_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"archive":{"path":".agent-work/PLANS/20260801-0236-p7-retained-r3-b2-m1-r1-s1-terminal-link-review.md","bytes":5457,"sha256":"00f06209f889a2a80a700eb43f2146bcfbc199fea0103cd86d12a935322a0215"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_M1_R1_S1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 exact Git gate

Orchestrator须先把S1 rejection及唯一active S1-C1写入FULL，并创建activation。Expected parent exact
`5d4e903b0d747be169d68032066b023d77f3a8f9`，subject exact
`chore(plan): supersede strict retained terminal assertion`，changed paths exact为FULL、PLAN与本轮new archive。Activation后porcelain必须clean。

Executer只从Git object database验证activation topology、PLAN/FULL各exact one strict machine row、required FULL subset和new archive committed
identity；再验证rejected activation/evidence topology及ER frozen blob/bytes/SHA。允许exact十二次只读Git invocation，必须在ER append前全部完成。
不得调用generic machine-row parser、CodeGraph、测试或compileall。

## 2. One immutable supersession record

Executer从committed ER中的single S1 handoff读取并严格验证：schema/reference/contract、two root rows、ordered seven file rows、C1 canonical
`4`、retained strict `3`、first failure exact `RuntimeError/c1_terminal_link`、builder/runtime/controller/output均`0`、retry/fallback `0/0`、all
locks与Planner stop。禁止读取working ER来代替activation-prefix Git blob，也禁止恢复、补写或发明identity rows。

构造schema exact `p7_td_b_retained_r3_option_b_b2_m1_r1_s1_c1_supersession_v1`的single canonical payload，至少包括：

- activation与evidence commit/ER identities；
- original record immutable且credit仅为failure evidence；
- corrected classification exact `NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH`；
- `c1_evidence_defect=false`，production/test/runner repair required均false；
- accepted C1 review archive和`terminal_linkage_previously_independently_accepted=true`；
- old fresh namespace exact immutable no-read disposition；
- successor rule exact使用accepted C1 review + exact four identities/canonical decode，不再发明unversioned terminal field selector；
- eligibility/release consumable均false，全部zero locks，Planner stop exact。

不得改写原S1 block、声称S1成功、授予manifest/eligibility/release credit，或把Executor记录的external timing提升为新的independent observation。

## 3. Sole append lifecycle

全部Git reads完成后，在内存冻结final payload，令`execution_result_appends=1`，然后exact one `apply_patch`向ER EOF appendheading
`## REF-P7-25-R2-B2-M1-R1-S1-C1 Git/ER-only supersession handoff`与single fenced one-line strict canonical JSON block。
成功append是最后一个side effect；之后repository/Git/external/process操作均`0`，不得第二append。首次apply_patch若no-write rejected，立即停止，
retry/fallback保持`0/0`。

## 4. Hard locks 与 stop

External path operation总数`0`：旧S1、C1、retained、fresh targets均no read/stat/list/glob/search/probe。Code/test/PLAN/FULL/archive/debug/
GUIDE/RESEARCH writes0；builder/runtime/controller/source/output/tests/compileall/CodeGraph/implementation commit0。Validator/callback/eligibility、
retained audit、release generation/qualification/copy/consumption0；network/DNS/environment/credentials/device/camera/Ray/strip/cleanup/capture/
FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment0。

本包是`PURE_OFFLINE_GIT_ER_ONLY_SUPERSESSION`，无需Human设备授权或Advisor科学决定。Sole append后立即停Planner门；不得自行进入fresh S2。

维护性边界：移除一次性field-selector假设，不新增production helper、parser、test harness或parallel evidence owner；无需架构重构。
