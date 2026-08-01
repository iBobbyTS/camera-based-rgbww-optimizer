# P7 retained-R3 Option B：B3-C3-C4-R1-I1 stable offline patch diagnostic

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R1-I1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-I1-STABLE-OFFLINE-PATCH-DIAGNOSTIC-V1`

**当前唯一动作：** Orchestrator建立activation后，Executer以一个最小non-shell launcher读取activation commit中的PLAN/FULL bytes，构造冻结spec并调用
accepted `run_offline_patch_preflight` exact一次；不实现parser/controller、不建root。Single canonical report + ER EOF handoff后停Planner。

**唯一 Planner stop：**
`B3_C3_C4_R1_I1_STABLE_OFFLINE_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0824-p7-retained-r3-b3-c3-c4-r1-owner-acceptance-review.md`；bytes `4872`，SHA-256
`89d9d139715c7eabe8d5cce5042a0fce2e0b8ca1c3bddca6e6f54321927bd4b1`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r1_i1_stable_offline_patch_diagnostic_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R1-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-I1-STABLE-OFFLINE-PATCH-DIAGNOSTIC-V1","execution_authorized_after_orchestrator_activation":true,"accepted_owner":{"activation":"a91b1ca059ab0265678e2bd64c1447c90f67e59a","implementation":"b929582521aa9e35a3bc1dcf163f1c22f1b7e2ae","evidence":"22712bf901da2ad1002514363796cf38ba941507","module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_offline_patch_preflight","entrypoint":"run_offline_patch_preflight","source_blob":"f310d108872724ab07870696528706878e42e5dc","source_sha256":"ba5b9c178238ea70a07013aecfcf38888b207812a8972d7bfaaa1aef170a92f4","test_blob":"b4b43edfbcd17bc3c870d4735e768207120f26c3","test_sha256":"a0320587dd38ec15bf6e09477111760c095e03be7d80c75f15cc330d500d9529","status":"ACCEPTED_COMPLETE_REPO_OWNED_OFFLINE_PATCH_PREFLIGHT_OWNER"},"activation_commit":{"expected_parent":"22712bf901da2ad1002514363796cf38ba941507","expected_subject":"chore(plan): activate stable offline patch diagnostic","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0824-p7-retained-r3-b3-c3-c4-r1-owner-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"committed_inputs":{"plan_object":"<activation_commit>:.agent-work/PLAN.md","full_object":"<activation_commit>:.agent-work/FULL_PLAN_REFERENCE.md","git_show_invocations":2,"working_tree_plan_reads":0,"working_tree_full_reads":0},"diagnostic_spec":{"repo":"/Users/ibobby/Projects/WLED-RGBWW","parent_sha":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","child_sha":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"expected_exit_code":0,"expected_stdout_bytes":6006,"expected_stdout_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","expected_stderr_bytes":0,"expected_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","argv":["git","diff","--binary","--full-index","--no-ext-diff","f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","--","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"authoritative_identity_owner":"Planner read-only Git object audit at 22712bf","worktree_independent":true},"execution_budgets":{"launcher_process_invocations":1,"committed_object_git_show_invocations":2,"stable_owner_invocations":1,"canonical_patch_git_invocations":1,"canonical_report_stdout_envelopes":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"success_contract":{"owner_classification":"CANONICAL_PATCH_EXACT_MATCH","owner_report_canonical":true,"observed_argv_exact":true,"observed_exit_code":0,"observed_stdout_bytes":6006,"observed_stdout_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","observed_stderr_bytes":0,"observed_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","success_label":"STABLE_OWNER_CANONICAL_PATCH_EXACT_MATCH"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R1-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-I1-STABLE-OFFLINE-PATCH-DIAGNOSTIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_STABLE_OWNER_PATCH_DIAGNOSTIC","offline_patch_preflight_owner_status":"ACCEPTED_COMPLETE","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record stable offline patch diagnostic","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"code_writes":0,"test_writes":0,"implementation_commits":0,"one_off_parser_implementations":0,"one_off_controller_files":0,"external_root_operations":0,"failed_root_reads":0,"working_tree_plan_reads":0,"working_tree_full_reads":0,"working_tree_source_reads":0,"working_tree_test_reads":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"real_manifest_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"remaining_manifest_self_checks":0,"synthetic_runs":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"guide_writes":0,"research_writes":0},"authorization":{"classification":"PURE_OFFLINE_REPO_GIT_OBJECT_DIAGNOSTIC","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0824-p7-retained-r3-b3-c3-c4-r1-owner-acceptance-review.md","bytes":4872,"sha256":"89d9d139715c7eabe8d5cce5042a0fce2e0b8ca1c3bddca6e6f54321927bd4b1"},"planner_stop":"B3_C3_C4_R1_I1_STABLE_OFFLINE_PATCH_DIAGNOSTIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation与stable-owner gate

Activation必须是`22712bf...`direct child，subject/path set与PLAN/FULL strict machine subset exact、porcelain clean；accepted owner source/test
blob/SHA与commit topology必须匹配machine row。任一失败则committed reads/owner/Git0，single ER后停。

## 2. 唯一stable invocation

Executer只启动一个minimal non-shell Python launcher。Launcher不得实现machine-row parsing、subset comparison、Git classification、canonical serializer或persist；它只：

1. 以`git show <activation>:PLAN`与`git show <activation>:FULL`各exact一次取得raw committed bytes，exit/stderr异常即停；
2. 构造machine row exact `CanonicalPatchDiagnosticSpec`；
3. 调用accepted `run_offline_patch_preflight(plan_bytes, full_bytes, spec)` exact一次，使用default P3 Git helper；
4. 将returned canonical `report_bytes`原样写stdout一次；classification非exact match时launcher nonzero，但仍保留report供ER记录。

不得生成source/controller文件、root或diagnostic artifact。Owner内部必须先验证PLAN+FULL+required subset，随后以helper-compatible argv运行Git exact一次。Expected
identity来自Planner在HEAD `22712bf...`对相同immutable commit/path argv的single read-only Git object audit：stdout6006/SHA `4044c624...`，stderr empty。

## 3. EOF stop与locks

Launcher terminal后owned-process scan1并排除scan自身；不kill/cleanup。Executer tail-read ER1，以single apply_patch在physical EOF追加heading+strict JSON，包含
activation/owner identities、committed object reads、owner canonical report完整facts、argv/expected/observed/classification、counts与locks；append后operations0、不commit。

Mismatch/Git failure/preflight error均不retry、不fallback、不改owner，single ER后停；exact match也只停Planner，不恢复remaining checks。

代码/测试/one-off parser/controller/root/worktree reads、real manifest/C1/retained、tests/CodeGraph/synthetic、validator/audit/eligibility/release、network/device/
science/firmware/deployment全部0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：本包只有薄launcher调用accepted typed owner；解析、subset、Git与canonical report职责不再散落，且无新增持久化框架。
