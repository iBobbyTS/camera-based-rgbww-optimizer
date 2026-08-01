# P7 retained-R3 Option B：B3-C3-C3-S1 Git/ER terminal supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C3-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-S1-GIT-ER-TERMINAL-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先按machine contract建立exact activation；Executer随后只从committed Git与当前ER完成一次physical EOF
canonical supersession append，冻结B3-C3-C3的artifact-role positional misbinding、测试全0及全部locks，不读取failed root或real inputs，
不修controller，不重跑verification。

**唯一 Planner stop：**
`B3_C3_C3_S1_GIT_ER_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0633-p7-retained-r3-b3-c3-c3-binding-eof-review.md`；bytes `5251`，SHA-256
`e83b0d7216ce88989ad97ecb4a5c7ad53a5106b161c47bc6cbbf26ce505ae2d9`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c3_s1_git_er_terminal_supersession_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C3-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-S1-GIT-ER-TERMINAL-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_execution":{"activation":"38aa1ce69c0a8dd70374415c531b8d33d6ebd064","evidence_commit":"fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36","decision":"REJECTED_CONTROLLER_ARTIFACT_ROLE_POSITIONAL_MISBINDING_AND_NON_EOF_EXECUTION_RESULT_HANDOFF","durable_binding_failure_accepted":true,"verification_accepted":false,"artifact_role_error":"REAL_MANIFEST_FILES_POSITION_ZERO_IS_ADMISSION_NOT_MANIFEST","focused_actual":0,"full_actual":0,"synthetic_actual":0,"failed_root_reuse_permitted":false},"physical_eof_facts":{"parent_er_bytes":1332706,"parent_er_sha256":"0b5514770f001f329b84922789820f37c9c01f2763579653df253f0cf81602e1","evidence_er_bytes":1337266,"evidence_er_sha256":"ec8a1f8385f90b49318a122d4142a6e1af831ddf5a8c1f99c77a31947166314b","parent_is_evidence_prefix":false,"lcp_bytes":2583,"common_suffix_bytes":1330123,"inserted_bytes":4560,"inserted_sha256":"c69f63b45d54d5faab7f52c3c9d37e5336c0c732bcb2b00171daad732571fda6","original_section_canonical_position":false},"activation_commit":{"expected_parent":"fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36","expected_subject":"chore(plan): activate B3-C3-C3 ER supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0633-p7-retained-r3-b3-c3-c3-binding-eof-review.md"],"clean_porcelain_required_after_activation":true},"repository_machine_row_contract":{"plan_delimiter":"PLAN_MACHINE_CONTRACT=","full_delimiter":"FULL_PLAN_MACHINE_STATE=","wrapper":"exact_single_backtick_wrapped_line","decode":"strict_utf8","parse":"json_object_duplicate_free_nonfinite_safe","compare":"typed_semantic_fields_only","canonical_reencode":false,"sorted_key_gate":false,"raw_vs_reencoded_byte_equality":false,"generic_scanner":false},"execution_result_precondition":{"path":".agent-work/EXECUTION_RESULT.md","bytes":1337266,"sha256":"ec8a1f8385f90b49318a122d4142a6e1af831ddf5a8c1f99c77a31947166314b","mode":420,"blob_oid":"744720bf87aa9a7ce98823049fe15f2aeb248cc4","whole_file_reads":1,"tail_reads":0},"canonical_supersession":{"heading":"## 2026-08-01 B3-C3-C3 non-EOF handoff canonical supersession","append_location":"PHYSICAL_EOF_ONLY","supersedes_commit":"fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36","supersedes_heading":"## 2026-08-01 B3-C3-C3 corrected byte-stable postcommit verification execution","superseded_section_status":"NONCANONICAL_POSITIONED_HISTORICAL_EVIDENCE","review_archive":[".agent-work/PLANS/20260801-0633-p7-retained-r3-b3-c3-c3-binding-eof-review.md",5251,"e83b0d7216ce88989ad97ecb4a5c7ad53a5106b161c47bc6cbbf26ce505ae2d9"],"binding_failure":"CONTROLLER_POSITIONALLY_BOUND_ADMISSION_AS_MANIFEST","required_future_binding":"EXACT_MACHINE_ROW_BASENAME_LOOKUP_NO_POSITION_INFERENCE","verification_status":"REJECTED_NOT_RUN_AFTER_SELF_CHECK_FAILURE","focused_actual":0,"full_actual":0,"synthetic_actual":0,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","canonical_validator_called":false,"eligibility_emitted":false,"release_consumable":false,"b4_unlocked":false,"binding_correction_authorized":false,"verification_rerun_authorized":false},"execution_budgets":{"repository_plan_reads":1,"repository_full_reads":1,"git_read_invocations_max":12,"execution_result_whole_file_reads":1,"execution_result_tail_reads":0,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"process_table_scans":0,"retry":0,"fallback":0},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): supersede B3-C3-C3 non-EOF handoff","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C3-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-S1-GIT-ER-TERMINAL-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c3_status":"REJECTED_CONTROLLER_ARTIFACT_ROLE_POSITIONAL_MISBINDING_AND_NON_EOF_EXECUTION_RESULT_HANDOFF","b3_c3_c3_s1_status":"ACTIVE_GIT_ER_TERMINAL_SUPERSESSION","executer_dispatched":true,"device_authorized_by_this_file":false},"zero_budgets":{"fresh_failed_root_reads":0,"external_manifest_reads":0,"real_manifest_reads":0,"real_source_reads":0,"c1_reads":0,"retained_reads":0,"repository_code_direct_reads":0,"repository_test_direct_reads":0,"repository_code_writes":0,"repository_test_writes":0,"tests":0,"controller_invocations":0,"controller_writes":0,"synthetic_runs":0,"codegraph_queries":0,"codegraph_sync":0,"canonical_validator_calls":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"advisor_request_git_document_reads":0,"guide_writes":0,"research_writes":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_TERMINAL_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"archive":{"path":".agent-work/PLANS/20260801-0633-p7-retained-r3-b3-c3-c3-binding-eof-review.md","bytes":5251,"sha256":"e83b0d7216ce88989ad97ecb4a5c7ad53a5106b161c47bc6cbbf26ce505ae2d9"},"planner_stop":"B3_C3_C3_S1_GIT_ER_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与只读输入边界

Activation必须是`fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36`的direct child，subject与exact three-path set按machine
row；activation后porcelain clean。Executer在任何ER操作前只读取committed/current PLAN与FULL各一次并要求byte-identical，以exact
delimiter、strict UTF-8、duplicate-free/non-finite-safe object parse和typed semantic compare核对active task/contract。禁止canonical
reencode、key-order/whitespace/raw-byte equality gate、regex、generic或fallback scanner。

本包唯一可读取的工作文件是`.agent-work/EXECUTION_RESULT.md` whole file exact once；必须先核对mode、bytes、SHA-256与committed
blob OID。任何不一致均停止且不得append。禁止tail补读、父目录list、glob、search、symlink follow或读取任何external/fresh/real/retained
路径。

## 2. Canonical physical EOF supersession

前置identity全部PASS后，Executer构造machine row规定的exact heading与一个strict JSON object。Payload必须逐项记录：被supersede commit与
heading、原section非canonical-positioned、Planner archive path/bytes/SHA、accepted binding failure、focused/full/synthetic全0、future
basename binding要求、当前verification rejected、failed root不可复用，以及retained/validator/eligibility/release/B4全部locks。

以exact one且唯一一次successful `apply_patch`把该section追加在当前文件physical EOF。Patch context必须来自本轮whole-file read观察到的
实际末尾唯一字节；禁止按同名历史heading、行号或first-match位置插入。不得修改、移动、删除或重写旧section。Append完成即停止，
`postappend_operations=0`；不得再read、hash、tail、status、diff、commit或尝试修复。本次append的物理prefix关系由Orchestrator commit与
后续Planner从Git objects独立验收。

若precondition或patch失败，保持ER不变并直接报告失败；failed `apply_patch`也计入预算，禁止第二次尝试、fallback或改用shell/Python写入。

## 3. 明确冻结的后续 correction

本包不修controller，也不重跑self-check/tests/synthetic。S1被验收后才可另包授权binding correction；后续controller必须按machine-row
basename exact lookup分别绑定manifest、manifest seal、terminal、terminal seal与admission，禁止列表位置、排序、generic selector、
guess或fallback。该未来要求只作为冻结事实，不是本PLAN的执行授权。

## 4. Locks 与授权

Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`；canonical lineage validator仍是唯一eligibility owner。Release、network、DNS、
environment、credentials、device、camera、Ray、strip、cleanup、capture、formal、public analyzer、TD-C、sentinel、firmware、deployment与
P8全部为0。本包纯离线Git/ER证据治理，不需要Advisor科学决策或Human设备授权。

维护性判断：把ER顺序修复与controller basename binding修复拆开，避免证据治理包夹带verification重跑；本轮仅追加一个canonical
supersession section，不引入生产抽象或并行owner。
