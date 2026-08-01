# P7 retained-R3 Option B：B3-C3-C2 pure durable top-level fact diagnostic

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C2`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C2-PURE-DURABLE-TOP-LEVEL-FACT-DIAGNOSTIC-V1`

**当前唯一动作：** Orchestrator按machine contract创建exact activation；Executer随后只创建一个全新外置package与一个
non-TTY controller。Controller只读取accepted real manifest exact一次，在任何pass/fail判断前durably序列化并seal committed
expected facts与observed top-level type/keys/value summary，完成exact known-fact comparison及terminal handoff后停止。

**唯一 Planner stop：**
`B3_C3_C2_PURE_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0605-p7-retained-r3-b3-c3-c1-selfcheck-mismatch-review.md`；bytes `6258`，SHA-256
`5ddb4e94dd62860540358adb9d3800b557637d06d97394b4b1861f7e833ab40e`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c2_pure_durable_top_level_fact_diagnostic_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C2-PURE-DURABLE-TOP-LEVEL-FACT-DIAGNOSTIC-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_failure":{"activation":"6589f5e593d15e3191fc1e492b069fd51ea88a85","evidence_commit":"b923f4efb89a45705ed9af35cf5f53bf65ef8526","decision":"REJECTED_UNATTRIBUTED_TOP_LEVEL_MISMATCH_REQUIRES_DURABLE_FACT_DIAGNOSTIC","first_failure":"ValueError: manifest top-level mismatch","manifest_defect_proven":false,"failed_root_reuse_permitted":false},"activation_commit":{"expected_parent":"b923f4efb89a45705ed9af35cf5f53bf65ef8526","expected_subject":"chore(plan): activate pure top-level fact diagnostic","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0605-p7-retained-r3-b3-c3-c1-selfcheck-mismatch-review.md"],"clean_porcelain_required_after_activation":true},"repository_machine_row_contract":{"plan_delimiter":"PLAN_MACHINE_CONTRACT=","full_delimiter":"FULL_PLAN_MACHINE_STATE=","wrapper":"exact_single_backtick_wrapped_line","decode":"strict_utf8","parse":"json_object_duplicate_free_nonfinite_safe","compare":"typed_semantic_fields_only","canonical_reencode":false,"sorted_key_gate":false,"whitespace_normalization":false,"raw_vs_reencoded_byte_equality":false,"json_dumps_for_acceptance":false},"accepted_real_manifest":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-output/retained-r3-audit-provenance-manifest-v2.json","root_mode":448,"file_mode":384,"bytes":4651,"sha256":"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf","accepted_b2_evidence_commit":"3b9e60441062714115d9688e636891d591f3a6ef"},"known_top_level_expected":{"json_type":"object","facts":{"schema":{"json_type":"string","value":"p7_retained_r3_audit_provenance_manifest_v2"},"status":{"json_type":"string","value":"sealed_subordinate_provenance_evidence"},"immutable":{"json_type":"boolean","value":true}},"complete_exact_key_set_frozen":false,"whole_object_subset_equality_permitted":false,"observed_keys_are_diagnostic_only":true,"schema_widening_permitted":false,"generic_selector_permitted":false},"diagnostic_artifacts":{"fact_file":{"name":"manifest-top-level-facts.json","mode":384,"schema":"p7_retained_r3_manifest_top_level_fact_diagnostic_v1","status":"observed_before_judgment","exact_top_level_keys":["schema","status","expected","observed"],"expected_source":"committed_plan_known_top_level_expected","observed":{"json_type":"parsed_json_type","keys":"exact_observed_top_level_keys_in_parsed_insertion_order","key_count":"exact_integer","values":"one_row_per_observed_key"},"value_row":{"exact_keys":["key","json_type","summary"],"scalar_summary":"exact_typed_scalar_value","array_or_object_summary":{"exact_keys":["entry_count","diagnostic_canonical_json_bytes","diagnostic_canonical_json_sha256"],"acceptance_use":false}}},"seal_file":{"name":"manifest-top-level-facts.sha256.json","mode":384,"exact_keys":["bytes","sha256","target"],"target":"manifest-top-level-facts.json"},"write_order":["fact_file_fsync_atomic_publish","seal_file_fsync_atomic_publish","directory_fsync","replay_read_both","known_fact_judgment"],"writes":2,"replay_reads":2,"must_be_verified_before_judgment":true,"preserve_after_terminal":true},"controller_transport":{"fresh_package_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c2-<activation_short12>","root_mode":448,"source_name":"controller.py","source_mode":384,"create":"apply_patch_exact_once_after_nonfollowing_root_absence_gate","invocation":[".venv/bin/python","<absolute_fresh_package_root>/controller.py"],"tty":false,"stdin_source_bytes":0,"argv_source_fragments":0,"shell_eval":false,"terminal_paste":false,"repl":false,"ipython":false,"python_dash":false,"python_c":false,"heredoc":false,"source_self_identity_reads":2,"source_pre_post_identity_equal":true,"preserve_package_after_terminal":true},"read_budgets":{"real_manifest_root_nonfollowing_checks":1,"real_manifest_file_reads":1,"parent_directory_lists":0,"globs":0,"searches":0,"symlink_follows":0,"other_real_manifest_artifact_reads":0,"real_source_reads":0,"c1_reads":0,"retained_r3_reads":0,"governance_input_reads":0,"failed_b3_c3_root_reads":0,"failed_b3_c3_c1_root_reads":0},"execution_budgets":{"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_apply_patch_writes":1,"controller_source_self_reads":2,"outer_controller_invocations":1,"repository_file_decodes":2,"repository_machine_row_extractions":2,"git_read_invocations_max":20,"diagnostic_fact_writes":1,"diagnostic_seal_writes":1,"diagnostic_replay_reads":2,"known_fact_comparisons":4,"process_table_scans":1,"execution_result_tail_reads":1,"apply_patch_invocations":2,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"terminal_outcomes":{"match":{"status":"DIAGNOSTIC_COMPLETE","known_fact_result":"MATCH","success_label":"B3_C3_C2_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC_COMPLETE_NOT_POSTCOMMIT_VERIFIED"},"mismatch":{"status":"FAIL_CLOSED","known_fact_result":"MISMATCH","success_label":null,"required_first_failure":"exact expected and observed typed fact plus diagnostic identities"},"artifact_failure":{"status":"FAIL_CLOSED","known_fact_result":"NOT_JUDGED","success_label":null},"all":{"postcommit_verification_complete":false,"b4_unlocked":false,"canonical_eligibility_validator_called":false,"eligibility_emitted":false,"release_consumable":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED"}},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C2-PURE-DURABLE-TOP-LEVEL-FACT-DIAGNOSTIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c1_status":"REJECTED_UNATTRIBUTED_TOP_LEVEL_MISMATCH_REQUIRES_DURABLE_FACT_DIAGNOSTIC","b3_c3_c2_status":"ACTIVE_PURE_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3-C3-C2 pure fact diagnostic","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"failed_b3_c3_root_writes":0,"failed_b3_c3_c1_root_writes":0,"old_b3_evidence_reads":0,"controller_stdin_source_bytes":0,"controller_argv_source_fragments":0,"interactive_terminal_dispatch":0,"repl_invocations":0,"repository_code_direct_reads":0,"repository_test_direct_reads":0,"repository_code_writes":0,"repository_test_writes":0,"focused_suites":0,"full_suites":0,"synthetic_runs":0,"synthetic_controller_processes":0,"synthetic_input_writes":0,"synthetic_output_writes":0,"synthetic_replay_reads":0,"manifest_remaining_self_checks":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"retained_schema_validation":0,"retained_scientific_validation":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"generic_schema_allowlists":0,"generic_selectors":0,"canonical_machine_row_reencode_checks":0,"canonical_machine_row_key_order_checks":0,"canonical_machine_row_byte_equality_checks":0,"inferred_terminal_passed_field_checks":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC_ONLY","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0605-p7-retained-r3-b3-c3-c1-selfcheck-mismatch-review.md","bytes":6258,"sha256":"5ddb4e94dd62860540358adb9d3800b557637d06d97394b4b1861f7e833ab40e"},"planner_stop":"B3_C3_C2_PURE_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 machine-row gate

Activation必须是`b923f4efb89a45705ed9af35cf5f53bf65ef8526`的direct child，subject及FULL、PLAN、本review
archive exact three-path set以machine row为准，activation后porcelain clean。Executer在任何external access前完整读取activation
committed/current PLAN与FULL各一次并要求byte-identical。Machine row只允许exact delimiter、strict UTF-8、duplicate-free/
non-finite-safe object parse与typed semantic compare；禁止regex/generic/fallback scanner、canonical reencode、sorted-key、
whitespace normalization、raw-vs-reencoded equality及`json.dumps` acceptance gate。

## 2. Fresh byte-stable controller

先对machine row指定fresh root做exact one non-following absence gate。Present、symlink或error均停止，不得换path。Absent时只创建
0700 root，并用exact one `apply_patch`新增0600 `controller.py`。Controller启动后与terminal前各读取自身exact path一次，冻结
mode/bytes/SHA、strict UTF-8、NUL/CR absence及pre/post equality。只允许non-TTY argv
`.venv/bin/python <absolute-controller-file>` exact once；禁止复用B3-C3/C1 root、stdin source、Terminal paste、REPL/IPython、
`python -`、`python -c`、heredoc、shell eval、argv source fragment、retry或fallback。

## 3. Pure durable diagnostic

Transport通过后，只对accepted real manifest root做exact one non-following mode/type check，并对manifest exact path做exact one
non-following read，核对0600、bytes、SHA后strict parse。其他real artifacts、B2 source、C1、retained R3、governance inputs、
repository source/tests与任何失败root全部不得读取。

对同一次read的in-memory snapshot，在任何known-fact判断前按machine row生成fact与seal两个0600 artifacts：先atomic publish并fsync
fact，再publish seal并fsync directory，随后各exact one replay read验证bytes/SHA/target。Expected只能是committed PLAN列出的object及
schema/status/immutable typed facts。Observed必须记录实际JSON type、parsed insertion-order keys、key count及每个key的value
summary；scalar记录typed exact value，array/object仅记录entry count与diagnostic-only canonical JSON bytes/SHA。

Observed keys和container digest仅供归因，不得成为complete schema、key-order gate、generic selector/allowlist或acceptance owner。
不得把whole object与三字段subset比较。两个diagnostic artifacts durable且replay通过后，才执行object/schema/status/immutable四项
exact typed comparison。Match只表示diagnostic完成，不表示remaining self-check、postcommit verification、retained audit或eligibility
通过。Mismatch必须记录exact expected/observed typed fact，不得宣称超出durable事实的新manifest defect，也不得repair/regenerate。

## 4. Terminal handoff 与 locks

无论match、mismatch或artifact failure，ER append前都执行exact one bounded owned-process scan并记录
`owned_residual_processes`；scan error或非空即fail closed，但不得cleanup、kill或retry。所有Git/external/process操作必须在append前
完成。Executer只可tail-read ER一次，再以第二次且最后一次`apply_patch`在physical EOF追加唯一heading与一个strict JSON payload；
append后operations为0并停止，不commit。Fresh package及partial artifacts全部保留。

Focused、full、synthetic、remaining manifest self-check、canonical validator、real retained audit、eligibility、release、network、DNS、
environment、credentials、device、camera、Ray、strip、cleanup、capture、formal、public analyzer、TD-C、sentinel、firmware、deployment
及P8全部为0。`RETAINED_UNVALIDATED_UNCONSUMED`保持不变；canonical lineage validator仍是唯一eligibility owner。本包不需要
Advisor科学决策或Human设备授权。

维护性判断：本包只增加fresh package内的一次性diagnostic evidence，不修改repository实现，也不新增schema、manifest或eligibility
owner；后续是否恢复postcommit verification由Planner基于durable facts另行制定。
