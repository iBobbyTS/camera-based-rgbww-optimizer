# P7 retained-R3 Option B：B3-C3-C4-C1 two-phase patch diagnostic gate correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C1-TWO-PHASE-PATCH-DIAGNOSTIC-GATE-CORRECTION-V1`

**当前唯一动作：** Orchestrator建立exact activation后，Executer先运行一个独立pre-root verifier process，只读activation commit中的PLAN/FULL并按
exact Markdown backtick delimiter机械切片；该process的任何失败都必须在root touch/create exact0时fail-fast。只有phase1 exit0并产生唯一strict
success envelope后，才启动第二个独立Python process，创建一个不同于旧failed root的fresh root并运行exact一次canonical Git diff diagnostic，随后single
ER EOF handoff并停止。

**唯一 Planner stop：**
`B3_C3_C4_C1_TWO_PHASE_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0748-p7-retained-r3-b3-c3-c4-patch-diagnostic-preflight-failure-review.md`；bytes `6782`，SHA-256
`3edc5e2e6cfcf002458a6034e88aa37c6e5cca89ef2fcd196c4cb37c110b26d8`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_c1_two_phase_patch_diagnostic_gate_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C1-TWO-PHASE-PATCH-DIAGNOSTIC-GATE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_failed_diagnostic":{"activation":"a859217aefe6cbcb421cce5aa1a178f688c899ad","evidence_commit":"e0b0e34116ddb3c09a7072f1c3782786ee6ad9d0","decision":"REJECTED_PRE_INVOCATION_MARKDOWN_MACHINE_ROW_PARSE_AND_NON_FAIL_FAST_ROOT_CREATION","er_parent_blob":"bce93488e3c1d815767ced3f62b1cae1f189b241","er_parent_bytes":1354521,"er_parent_sha256":"50fd97882b243d926ab7f4fd7b083c82068917aa7293f06a6d659b2449cb7ee9","er_suffix_lines":6,"er_suffix_bytes":4354,"er_suffix_sha256":"6947626b0531160e25fbab7cd6f6a157a702e32db8b625a22af73ec675cb7637","first_failure":"PLAN_MACHINE_ROW_MARKDOWN_DELIMITER_PARSE_FAILURE","reported_bare_prefix_count":0,"canonical_git_diagnostic_invocations":0,"secondary_failed_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-m1-patch-diagnostic-a859217aefe6","secondary_failed_root_mkdirs":1,"failed_root_reuse_permitted":false,"provenance_drift_proven":false},"activation_commit":{"expected_parent":"e0b0e34116ddb3c09a7072f1c3782786ee6ad9d0","expected_subject":"chore(plan): correct patch diagnostic pre-root gate","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0748-p7-retained-r3-b3-c3-c4-patch-diagnostic-preflight-failure-review.md"],"clean_porcelain_required_after_activation":true},"phase1_pre_root_gate":{"independent_process_invocations":1,"process":".venv/bin/python -","shell":false,"committed_plan_object":"<activation_commit>:.agent-work/PLAN.md","committed_full_object":"<activation_commit>:.agent-work/FULL_PLAN_REFERENCE.md","git_show_invocations":2,"working_tree_plan_reads":0,"working_tree_full_reads":0,"strict_utf8_decodes":2,"reject_cr":true,"split_algorithm":"text.split('\\n')","plan_opening_delimiter":"`PLAN_MACHINE_CONTRACT=","full_opening_delimiter":"`FULL_PLAN_MACHINE_STATE=","closing_delimiter":"`","row_selection":"line.startswith(opening_delimiter) and line.endswith(closing_delimiter)","row_count_each":1,"payload_slice":"line[len(opening_delimiter):-len(closing_delimiter)]","payload_strip":false,"regex":false,"bare_prefix_alternative":false,"generic_scanner":false,"canonical_reencode":false,"repair":false,"fallback":false,"duplicate_keys_rejected":true,"nonfinite_rejected":true,"required_full_subset_exact":true,"stdout_envelopes":1,"stderr_bytes":0,"success_status":"PRE_ROOT_COMMITTED_MACHINE_ROWS_VALID","external_root_lstat":0,"external_root_absence_checks":0,"external_root_mkdirs":0,"external_root_reads":0,"external_root_writes":0},"phase_boundary":{"phase2_invocations_if_phase1_nonzero":0,"phase2_invocations_if_phase1_success":1,"same_shell_or_process":false,"manual_continue_on_nonzero":false,"fail_fast_required":true},"canonical_git_diagnostic":{"cwd":"/Users/ibobby/Projects/WLED-RGBWW","argv":["git","diff","--binary","f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","--","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"invocations":1,"shell":false,"stdin_bytes":0,"expected_exit":0,"expected_stdout_bytes":5874,"expected_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","expected_stderr_bytes":0,"expected_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","persist_fields":["phase1_status","phase1_plan_row_count","phase1_full_row_count","expected_argv","observed_argv","argv_exact_match","expected_stdout_bytes","observed_stdout_bytes","expected_stdout_sha256","observed_stdout_sha256","exit_code","stderr_bytes","stderr_sha256","classification"],"alternate_argv_invocations":0,"working_tree_source_reads":0,"working_tree_test_reads":0},"phase2_fresh_package":{"independent_process_invocations":1,"process":".venv/bin/python -","shell":false,"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-m1-patch-diagnostic-c1-<activation_short12>","must_differ_from_failed_root":true,"root_mode":448,"absence_checks":1,"mkdirs":1,"inline_controller_only":true,"controller_source_files":0,"controller_invocations":1,"controller_retry":0,"controller_fallback":0,"diagnostic_name":"m1-patch-byte-diagnostic.json","diagnostic_mode":384,"diagnostic_writes":1,"preserve_after_terminal":true},"classification":{"exact_match":"M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT","same_exact_argv_output_mismatch":"CURRENT_GIT_COMMAND_RENDERING_MISMATCH_NO_COMMITTED_OBJECT_DRIFT","git_failure":"GIT_COMMAND_FAILURE_DRIFT_DETERMINATION_INDETERMINATE","actual_provenance_drift_claim_permitted":false},"execution_budgets":{"phase1_process_invocations":1,"phase1_git_show_invocations":2,"phase1_machine_row_parse_attempts":2,"phase2_process_invocations":1,"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_writes":0,"controller_invocations":1,"canonical_git_diff_invocations":1,"diagnostic_writes":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"success_contract":{"phase1_status":"PRE_ROOT_COMMITTED_MACHINE_ROWS_VALID","phase1_root_creation":0,"diagnostic_argv_exact":true,"diagnostic_exit":0,"observed_stdout_bytes":5874,"observed_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","success_label":"M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C1-TWO-PHASE-PATCH-DIAGNOSTIC-GATE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_TWO_PHASE_PATCH_DIAGNOSTIC_GATE_CORRECTION","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3-C3-C4 two-phase patch diagnostic","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"failed_current_root_reads":0,"failed_current_root_writes":0,"failed_current_root_deletes":0,"failed_v3_root_reads":0,"failed_v2_root_reads":0,"earlier_failed_external_root_reads":0,"real_manifest_root_reads":0,"real_source_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"working_tree_plan_reads":0,"working_tree_full_reads":0,"working_tree_source_reads":0,"working_tree_test_reads":0,"remaining_manifest_self_checks":0,"focused_invocations":0,"full_invocations":0,"synthetic_runs":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_GIT_OBJECT_DIAGNOSTIC","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0748-p7-retained-r3-b3-c3-c4-patch-diagnostic-preflight-failure-review.md","bytes":6782,"sha256":"3edc5e2e6cfcf002458a6034e88aa37c6e5cca89ef2fcd196c4cb37c110b26d8"},"planner_stop":"B3_C3_C4_C1_TWO_PHASE_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW"}`

## 1. Review decision 与 activation gate

上一执行判定为`REJECTED_PRE_INVOCATION_MARKDOWN_MACHINE_ROW_PARSE_AND_NON_FAIL_FAST_ROOT_CREATION`。首错是bare-prefix parser count0，次生effect是
同shell在nonzero后仍mkdir1；canonical Git invocation0，未观察M1 patch bytes，也未证明provenance drift。Failed root
`...-a859217aefe6`保持immutable/non-consumable，本PLAN不授权读取或复用。

Executer开始前只用Git metadata验证activation是parent `e0b0e34116ddb3c09a7072f1c3782786ee6ad9d0`的direct child，subject exact
`chore(plan): correct patch diagnostic pre-root gate`，changed paths exact FULL/PLAN/本archive三项、porcelain clean；同时验证evidence commit topology与ER
prefix/suffix identities exact。不得读取failed root或运行diagnostic。Activation gate失败则phase1/phase2/root/diagnostic0，single ER后停。

## 2. Phase 1：独立 committed-machine-row pre-root gate

Phase1必须是一个独立、non-shell Python process；它与Phase2不得位于同一shell text、session pipeline、command substitution、trap或continuation。它只运行两次
read-only Git object command：

1. `git show <activation_commit>:.agent-work/PLAN.md`；
2. `git show <activation_commit>:.agent-work/FULL_PLAN_REFERENCE.md`。

不得读取working-tree PLAN/FULL，也不得触碰external root、failed roots、source/test、ER payload或retained evidence。Phase1的root lstat、absence check、mkdir、read、
write budget全部exact0。

对两个Git stdout bytes分别strict UTF-8 decode，任何decode error或physical CR立即nonzero。机械slice算法逐字冻结：

1. 仅执行`text.split('\n')`，不`strip`/`lstrip`/`rstrip`；
2. PLAN opening delimiter exact `` `PLAN_MACHINE_CONTRACT= ``，FULL opening delimiter exact
   `` `FULL_PLAN_MACHINE_STATE= ``，共同closing delimiter exact单个`` ` ``；
3. row selection只能是`line.startswith(opening_delimiter) and line.endswith(closing_delimiter)`；每文件exact one row；
4. JSON bytes/string只能用`line[len(opening_delimiter):-len(closing_delimiter)]`取得；不得搜索bare prefix、regex、alternative、generic scanner或修复；
5. strict JSON必须拒绝duplicate keys与NaN/Infinity，验证reference/contract/activation及PLAN `required_full_machine_state`是FULL machine object的exact subset；不得
   canonical reencode或raw key-order gate。

全部通过只向stdout发一个strict single-line JSON envelope，status exact `PRE_ROOT_COMMITTED_MACHINE_ROWS_VALID`、PLAN/FULL row counts各1、required subset
true，stderr0并exit0。任何failure必须nonzero且Phase2 invocation0、root touch/create0；Executer随后只做single ER failure append。禁止为parse failure运行fallback或继续。

## 3. Hard phase boundary 与 Phase 2 diagnostic

只有Executer独立观察Phase1 process exit0、stderr0、exact one success envelope且全部fields匹配后，才可另行发起一个新的independent Phase2 Python process。
不得把两个phase拼在一个shell、用缺少`set -e`的wrapper继续、或在Phase1启动前预建目录。Phase2 invocation本身就是唯一inline controller，不持久化
`controller.py`。

Phase2 root exact
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-m1-patch-diagnostic-c1-<activation_short12>`，必须与旧failed root
byte-different。仅Phase2开始后做一次no-follow absence gate；present/symlink/error即fail closed且mkdir0。Absent后mkdir exact1、mode0700。

在同一Phase2 Python process内，以`subprocess` argv vector、`shell=False`、cwd exact repository、stdin empty运行machine row canonical Git argv exact一次。
不得增加/删除/重排flag/path，不得alternate command、retry、fallback或working-tree source/test read。Observed argv必须是实际传给subprocess的tuple/list；raw
stdout/stderr只计算bytes与SHA，禁止decode/normalize/strip/canonicalize。

只写一个exclusive regular0600 `m1-patch-byte-diagnostic.json`，字段exact覆盖machine row persist fields并绑定Phase1 success facts。若argv exact、exit0且
stdout bytes/SHA exact，classification为`M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT`；若same exact argv exit0但stdout
identity不符，为`CURRENT_GIT_COMMAND_RENDERING_MISMATCH_NO_COMMITTED_OBJECT_DRIFT`；Git failure为
`GIT_COMMAND_FAILURE_DRIFT_DETERMINATION_INDETERMINATE`。任何分支都不得claim actual provenance drift。

## 4. Terminal handoff、failure branches 与 locks

Phase2结束后做一次owned-process scan，必须按PID/argv排除scan process自身；error或真实owned match即fail closed，不kill/cleanup/retry。Executer只tail-read ER
一次，以一次successful `apply_patch`在physical EOF追加heading + strict JSON payload，绑定activation、phase1 committed-object reads/row counts/root0、phase2
invocation/new root/diagnostic identity、expected/observed argv/stdout/exit/classification、process scan、actual counts、旧root no-read/no-reuse及全部locks。Append后
operations0、停止、不commit。

- Phase1 failure：Phase2/controller/Git/diagnostic/root touch/create exact0，single ER后停；
- Phase2 absence/mkdir/Git/diagnostic failure：保留new root，不repair/delete/reuse，不retry，single ER后停；
- Exact match：只报告canonical Git diagnostic match/no provenance drift，停Planner；不得恢复remaining self-check、tests或synthetic。

Failed current/V3/V2/earlier roots、real manifest/source、C1/retained artifacts、working-tree PLAN/FULL/source/test reads、remaining manifest self-check、focused/full、
synthetic、real B2/manifest repair/regeneration、CodeGraph、canonical validator/callback、retained audit、eligibility、release、network/DNS/environment/credentials、
device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部0。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

本包是pure-offline Git-object diagnostic，不需要Advisor科学判断或Human设备授权。

维护性判断：纠偏只把一次性diagnostic拆成pre-root immutable-object parser和post-gate inline diagnostic两个独立process；不新增持久化parser/controller framework，
不改production/tests/manifest/validator owner，当前无需重构。
