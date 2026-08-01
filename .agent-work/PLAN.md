# P7 retained-R3 Option B：B3-C3-C4 M1 patch-byte pure Git diagnostic

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-M1-PATCH-BYTE-PURE-GIT-DIAGNOSTIC-V1`

**当前唯一动作：** Orchestrator先建立exact activation；Executer随后在一个全新外置root内运行exact canonical
`git diff --binary` argv一次，只持久化expected/observed argv、stdout bytes与SHA-256以及terminal classification，然后在ER物理EOF
追加一次handoff。不得读取或复用V3 failed root，不得恢复remaining self-check、focused/full tests或synthetic。

**唯一 Planner stop：**
`B3_C3_C4_M1_PATCH_BYTE_PURE_GIT_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0737-p7-retained-r3-b3-c3-c4-v3-m1-patch-byte-review.md`；bytes `5725`，SHA-256
`b53d451c88c999d8bb1e6a1becc17c18c40e253a4730f23acf83954d9badf6af`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_m1_patch_byte_pure_git_diagnostic_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-M1-PATCH-BYTE-PURE-GIT-DIAGNOSTIC-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_v3":{"activation":"d2c9794d566259660506925c49672b6cb55fdb14","evidence_commit":"7d2e9ac93f388f5d9204ed3243f4cf8b16dfc83f","decision":"REJECTED_INSUFFICIENT_DURABLE_M1_PATCH_BYTE_DIAGNOSTIC_PURE_GIT_DIAGNOSTIC_REQUIRED","er_parent_bytes":1350396,"er_parent_sha256":"1fa058cf4d9b468676925d4d7d2d3b8b6a2bb24d86ebcb90609d6f9672fecdf4","er_suffix_bytes":4125,"er_suffix_sha256":"6a8df353e1ceebb12b2ad446fbbbd87bc12b75eef35e5c37e71d20ba5a86baaa","first_failure":"M1 patch bytes","source_file_identity_match":true,"source_parent_reads":0,"focused_actual":0,"full_actual":0,"synthetic_actual":0,"failed_root_reuse_permitted":false,"provenance_drift_proven":false},"activation_commit":{"expected_parent":"7d2e9ac93f388f5d9204ed3243f4cf8b16dfc83f","expected_subject":"chore(plan): diagnose B3-C3-C4 M1 patch bytes","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0737-p7-retained-r3-b3-c3-c4-v3-m1-patch-byte-review.md"],"clean_porcelain_required_after_activation":true},"canonical_git_diagnostic":{"cwd":"/Users/ibobby/Projects/WLED-RGBWW","argv":["git","diff","--binary","f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","--","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"invocations":1,"shell":false,"stdin_bytes":0,"expected_exit":0,"expected_stdout_bytes":5874,"expected_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","expected_stderr_bytes":0,"expected_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","persist_fields":["expected_argv","observed_argv","argv_exact_match","expected_stdout_bytes","observed_stdout_bytes","expected_stdout_sha256","observed_stdout_sha256","exit_code","stderr_bytes","stderr_sha256","classification"],"alternate_argv_invocations":0,"working_tree_source_reads":0,"working_tree_test_reads":0},"fresh_package":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-m1-patch-diagnostic-<activation_short12>","root_mode":448,"absence_checks":1,"mkdirs":1,"source_name":"controller.py","source_mode":384,"controller_create_apply_patch_writes":1,"controller_invocations":1,"controller_retry":0,"controller_fallback":0,"diagnostic_name":"m1-patch-byte-diagnostic.json","diagnostic_mode":384,"diagnostic_writes":1,"preserve_after_terminal":true},"classification":{"exact_match":"V3_CONTROLLER_COMMAND_RENDERING_OR_COMPARISON_MISMATCH_NO_PROVENANCE_DRIFT","same_exact_argv_output_mismatch":"CURRENT_GIT_COMMAND_RENDERING_MISMATCH_NO_COMMITTED_OBJECT_DRIFT","git_failure":"GIT_COMMAND_FAILURE_DRIFT_DETERMINATION_INDETERMINATE","actual_provenance_drift_claim_permitted":false},"execution_budgets":{"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_apply_patch_writes":1,"controller_invocations":1,"canonical_git_diff_invocations":1,"diagnostic_writes":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"success_contract":{"diagnostic_argv_exact":true,"diagnostic_exit":0,"observed_stdout_bytes":5874,"observed_stdout_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","success_label":"M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-M1-PATCH-BYTE-PURE-GIT-DIAGNOSTIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_M1_PATCH_BYTE_PURE_GIT_DIAGNOSTIC","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3-C3-C4 M1 patch diagnostic","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"failed_v3_root_reads":0,"failed_v2_root_reads":0,"earlier_failed_external_root_reads":0,"real_manifest_root_reads":0,"real_source_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"working_tree_source_reads":0,"working_tree_test_reads":0,"remaining_manifest_self_checks":0,"focused_invocations":0,"full_invocations":0,"synthetic_runs":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_GIT_OBJECT_DIAGNOSTIC","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0737-p7-retained-r3-b3-c3-c4-v3-m1-patch-byte-review.md","bytes":5725,"sha256":"b53d451c88c999d8bb1e6a1becc17c18c40e253a4730f23acf83954d9badf6af"},"planner_stop":"B3_C3_C4_M1_PATCH_BYTE_PURE_GIT_DIAGNOSTIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation与唯一exact Git command

Activation必须是`7d2e9ac93f388f5d9204ed3243f4cf8b16dfc83f`的direct child，subject和exact three-path set必须匹配
machine row，activation后porcelain clean。Executer在任何执行前读取committed/current PLAN与FULL各一次并要求byte-identical；只允许strict
UTF-8与duplicate-free/non-finite-safe JSON解析machine row，不得canonical reencode、key-order/raw-byte gate、generic scanner或fallback。

使用activation short12派生的fresh root做一次non-following absence gate；present、symlink或error均停。Absent后创建`0700` root并以第一次
且唯一一次successful `apply_patch`写入`0600 controller.py`。Controller只能以`subprocess` argv vector、`shell=false`、cwd exact repository、
stdin空运行machine row冻结的canonical Git argv一次。不得增加、删除、重排或替换flag/path，不得运行alternate command、retry或fallback，
不得读取working-tree source/test或任何external/failed/retained root。

## 2. 最小durable diagnostic

Controller以实际传给subprocess的argv作为`observed_argv`，与machine row的`expected_argv`逐项typed equality。捕获raw stdout和stderr，直接
在内存计算bytes与SHA-256；不得decode、normalize、strip或canonicalize stdout。只写一个`0600 m1-patch-byte-diagnostic.json`，字段仅需覆盖
machine row的`persist_fields`。Expected值必须原样来自PLAN；observed值必须来自唯一实际invocation。

若exit0、argv exact且stdout bytes/SHA exact匹配，classification为
`V3_CONTROLLER_COMMAND_RENDERING_OR_COMPARISON_MISMATCH_NO_PROVENANCE_DRIFT`。若同一exact argv exit0但stdout identity不匹配，classification为
`CURRENT_GIT_COMMAND_RENDERING_MISMATCH_NO_COMMITTED_OBJECT_DRIFT`。若Git命令失败，则为
`GIT_COMMAND_FAILURE_DRIFT_DETERMINATION_INDETERMINATE`并fail closed。本包不得声称actual provenance drift；它只区分V3 controller mismatch、
当前Git renderer mismatch或命令失败。

## 3. Physical EOF handoff与locks

写完diagnostic后做一次owned-process scan；error或非空即fail closed，不kill/cleanup。Executer只tail-read ER一次，以第二次且最后一次
successful `apply_patch`在physical EOF追加一个heading和一个strict JSON payload。Payload必须绑定activation、fresh root、diagnostic
path/bytes/SHA、expected/observed argv与stdout bytes/SHA、exit、classification、actual counts、failed-root no-read/no-reuse、later-stage0和全部
locks。Append后operations0，停止且不commit。

Remaining self-check、focused `83`、full `800`、synthetic、真实retained audit、canonical validator、eligibility、release、B4、network、DNS、
environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware和deployment全部
保持0。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。本包不需要Advisor科学决策或Human设备授权。

维护性判断：本包只创建一个一次性pure-Git evidence artifact，不改生产代码、测试、manifest schema、validator或eligibility owner；无需重构。
