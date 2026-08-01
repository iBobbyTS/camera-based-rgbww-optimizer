# P7 retained-R3 Option B：B3-C3-C4-C2 fixed-index machine-row successor

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-C2`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C2-FIXED-INDEX-MACHINE-ROW-SUCCESSOR-V1`

**当前唯一动作：** Orchestrator建立fresh activation后，Executer先用独立Phase1 process只读committed PLAN/FULL；machine row只能按固定首尾索引、
`inner = row[1:-1]`、inner prefix和strict JSON解析，禁止扫描内部backtick。Phase1 root touch/create0且fail-fast；仅通过后才启动独立Phase2，在全新root运行
exact-one canonical Git diff diagnostic并single ER EOF handoff。

**唯一 Planner stop：**
`B3_C3_C4_C2_FIXED_INDEX_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0757-p7-retained-r3-b3-c3-c4-c1-internal-backtick-gate-review.md`；bytes `3584`，SHA-256
`67e6597f24772203ef5e40ecb0e2996766c1d0bca928ef0426d95a30109f9cf1`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_c2_fixed_index_machine_row_successor_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-C2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C2-FIXED-INDEX-MACHINE-ROW-SUCCESSOR-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_c1":{"activation":"eb33eba3aa2a6942370850b80645fc5e146a425b","evidence_commit":"cdbb4b7f7a7461d9af490efb48f572e08b0cc862","decision":"REJECTED_NON_CONTRACTUAL_INTERNAL_BACKTICK_CARDINALITY_GATE_PHASE1_FAIL_FAST_EFFECTIVE","er_parent_blob":"cde8e55036f9368c2f17821d5559faa6b6171208","er_parent_bytes":1358875,"er_parent_sha256":"d5a8b60c676a6cd9f4d8eb39dd7f05a2bbdf28b2a4a38274d9d462677f6220fb","er_suffix_lines":6,"er_suffix_bytes":2877,"er_suffix_sha256":"96d3e909e357f87c832efe6f07782dca6678b340d158a9c080098d89ae464b0f","first_failure":"NON_CONTRACTUAL_WHOLE_ROW_BACKTICK_CARDINALITY_GATE","phase1_candidates":1,"phase1_exit":1,"phase1_root_touches":0,"phase1_root_creates":0,"phase2_invocations":0,"canonical_git_diff_invocations":0,"retry":0,"fallback":0,"provenance_drift_proven":false},"activation_commit":{"expected_parent":"cdbb4b7f7a7461d9af490efb48f572e08b0cc862","expected_subject":"chore(plan): correct C4-C1 internal backtick gate","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0757-p7-retained-r3-b3-c3-c4-c1-internal-backtick-gate-review.md"],"clean_porcelain_required_after_activation":true},"phase1_pre_root_gate":{"independent_process_invocations":1,"process":".venv/bin/python -","shell":false,"committed_plan_object":"<activation_commit>:.agent-work/PLAN.md","committed_full_object":"<activation_commit>:.agent-work/FULL_PLAN_REFERENCE.md","git_show_invocations":2,"working_tree_plan_reads":0,"working_tree_full_reads":0,"strict_utf8_decodes":2,"reject_cr":true,"split_algorithm":"text.split('\\n')","boundary_algorithm":["len(row) >= 2","row[0] == '`'","row[-1] == '`'","inner = row[1:-1]","inner.startswith(expected_prefix)","payload = inner[len(expected_prefix):]"],"plan_inner_prefix":"PLAN_MACHINE_CONTRACT=","full_inner_prefix":"FULL_PLAN_MACHINE_STATE=","row_count_each":1,"whole_row_backtick_count_calls":0,"inner_backtick_count_calls":0,"whole_row_backtick_find_calls":0,"inner_backtick_find_calls":0,"whole_row_backtick_membership_tests":0,"inner_backtick_membership_tests":0,"internal_backtick_scans":0,"payload_strip":false,"regex":false,"bare_prefix_alternative":false,"generic_scanner":false,"canonical_reencode":false,"repair":false,"fallback":false,"duplicate_keys_rejected":true,"nonfinite_rejected":true,"required_full_subset_exact":true,"stdout_envelopes":1,"stderr_bytes":0,"success_status":"PRE_ROOT_FIXED_INDEX_MACHINE_ROWS_VALID","external_root_lstat":0,"external_root_absence_checks":0,"external_root_mkdirs":0,"external_root_reads":0,"external_root_writes":0},"phase_boundary":{"phase2_invocations_if_phase1_nonzero":0,"phase2_invocations_if_phase1_success":1,"same_shell_or_process":false,"manual_continue_on_nonzero":false,"fail_fast_required":true},"canonical_git_diagnostic":{"cwd":"/Users/ibobby/Projects/WLED-RGBWW","argv":["git","diff","--binary","f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","--","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"invocations":1,"shell":false,"stdin_bytes":0,"expected_exit":0,"expected_stdout_bytes":5874,"expected_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","expected_stderr_bytes":0,"expected_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","alternate_argv_invocations":0,"working_tree_source_reads":0,"working_tree_test_reads":0},"phase2_fresh_package":{"independent_process_invocations":1,"process":".venv/bin/python -","shell":false,"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-m1-patch-diagnostic-c2-<activation_short12>","must_differ_from_all_failed_roots":true,"root_mode":448,"absence_checks":1,"mkdirs":1,"inline_controller_only":true,"controller_source_files":0,"controller_invocations":1,"diagnostic_name":"m1-patch-byte-diagnostic.json","diagnostic_mode":384,"diagnostic_writes":1,"preserve_after_terminal":true},"classification":{"exact_match":"M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT","same_exact_argv_output_mismatch":"CURRENT_GIT_COMMAND_RENDERING_MISMATCH_NO_COMMITTED_OBJECT_DRIFT","git_failure":"GIT_COMMAND_FAILURE_DRIFT_DETERMINATION_INDETERMINATE","actual_provenance_drift_claim_permitted":false},"execution_budgets":{"phase1_process_invocations":1,"phase1_git_show_invocations":2,"phase1_machine_row_parse_attempts":2,"phase2_process_invocations":1,"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_writes":0,"controller_invocations":1,"canonical_git_diff_invocations":1,"diagnostic_writes":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"success_contract":{"phase1_status":"PRE_ROOT_FIXED_INDEX_MACHINE_ROWS_VALID","phase1_root_creation":0,"diagnostic_argv_exact":true,"diagnostic_exit":0,"observed_stdout_bytes":5874,"observed_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","success_label":"M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-C2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-C2-FIXED-INDEX-MACHINE-ROW-SUCCESSOR-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_FIXED_INDEX_PATCH_DIAGNOSTIC","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3-C3-C4 fixed-index diagnostic","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"all_failed_root_reads":0,"all_failed_root_writes":0,"all_failed_root_deletes":0,"real_manifest_root_reads":0,"real_source_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"working_tree_plan_reads":0,"working_tree_full_reads":0,"working_tree_source_reads":0,"working_tree_test_reads":0,"remaining_manifest_self_checks":0,"focused_invocations":0,"full_invocations":0,"synthetic_runs":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_GIT_OBJECT_DIAGNOSTIC","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0757-p7-retained-r3-b3-c3-c4-c1-internal-backtick-gate-review.md","bytes":3584,"sha256":"67e6597f24772203ef5e40ecb0e2996766c1d0bca928ef0426d95a30109f9cf1"},"planner_stop":"B3_C3_C4_C2_FIXED_INDEX_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation与review facts

上一C1结果reject：Phase1找到了candidate1，却新增未授权的whole-row backtick count==2 gate；内部backtick导致在required fixed slice前失败。Fail-fast本身有效，
root touch/create、Phase2、Git diagnostic、diagnostic writes均0；未观察patch bytes或provenance drift。

Activation必须是`cdbb4b7f7a7461d9af490efb48f572e08b0cc862`的direct child，subject exact
`chore(plan): correct C4-C1 internal backtick gate`，changed paths exact FULL/PLAN/本archive；porcelain clean、ER prefix/suffix与C1 topology exact。失败则
Phase1/Phase2/root/Git0并single ER。

## 2. Phase1 exact fixed-index algorithm

Phase1是独立non-shell Python process，只以read-only `git show <activation>:PLAN`与`git show <activation>:FULL`各一次读取committed objects；working-tree
PLAN/FULL及所有external roots/source/test/evidence reads0。Root lstat/absence/mkdir/read/write exact0。

每个strict UTF-8、无CR text只执行`split('\n')`。对每一row按以下固定顺序：

1. 若`len(row) < 2`，不是candidate；
2. 只判断`row[0] == '`'`和`row[-1] == '`'`；
3. exact `inner = row[1:-1]`；
4. 只判断`inner.startswith(expected_prefix)`，PLAN prefix exact `PLAN_MACHINE_CONTRACT=`，FULL prefix exact
   `FULL_PLAN_MACHINE_STATE=`；
5. matching inner各exact1；payload exact `inner[len(expected_prefix):]`，不strip，strict JSON拒绝duplicate/nonfinite；
6. 验证reference/contract/activation与required FULL exact subset。

禁止在whole row或inner上对backtick做`count`、`find`、`index`、`rfind`、`rindex`、membership test、循环或任何内部扫描；内部backtick只作为JSON string普通
字符存在。禁止regex、bare-prefix alternative、generic scanner、canonical reencode、repair/fallback。

通过时stdout exact one strict envelope，status `PRE_ROOT_FIXED_INDEX_MACHINE_ROWS_VALID`、row counts1/1、subset true、stderr0、exit0。任何失败必须
Phase2 invocation0且root touch/create0，只做single ER append。

## 3. Phase2 exact-one Git diagnostic

仅在Executer独立观察Phase1 exit0与success envelope后，才启动另一个independent non-shell Python process；不得共享shell/pipeline/trap或预建root。
Phase2 fresh root使用machine row C2 path，与所有failed rootsbyte-different；no-follow absence check1，absent后mkdir1/mode0700。

同一inline process以argv vector、`shell=False`、cwd exact repo、stdin empty运行冻结`git diff --binary` argv exact一次。Raw stdout/stderr禁止
decode/normalize/strip，只计算bytes/SHA。Alternate argv/retry/fallback/working-tree source/test reads0。只写一个exclusive regular0600 diagnostic，绑定
Phase1 facts、expected/observed argv、stdout/stderr identity、exit与classification。

Exact argv+exit0+stdout5874/SHA `6b26e493...`才是
`M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT`；same argv output mismatch或Git failure按machine row分类，任何分支不得claim
actual provenance drift。

## 4. EOF与locks

Phase2后process scan1并排除scan自身；不得kill/cleanup。ER只tail-read1、apply_patch physical EOF append1，记录Phase1 root0、Phase2/root/diagnostic、actual
counts、failed roots no-read/no-reuse与locks；append后operations0、不commit。

Phase1 failure则Phase2/root/Git0；Phase2 failure保留new root且不retry；exact match也只停Planner，不恢复self-check/tests/synthetic。所有failed roots、real
manifest/source、C1/retained、working-tree files、remaining checks、focused/full/synthetic、validator/audit/eligibility/release、network/device/science/firmware/deployment
均0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：C2只冻结固定索引slice并移除内部delimiter扫描，继续复用two-process boundary；无production/test/framework变更。
