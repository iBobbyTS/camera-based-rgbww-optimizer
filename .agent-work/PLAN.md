# P7 retained-R3 Option B：B3-C3-C4-R2 postcommit verification remainder

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R2`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-POSTCOMMIT-VERIFICATION-REMAINDER-V1`

**当前唯一动作：** 使用accepted basename-bound C4 contracts完成此前始终未执行的B3 remainder：real manifest/Git/input self-check → focused83 →
durable full810 → brand-new synthetic terminal/replay。Stable patch diagnostic已经接受，本包不重跑diagnostic、不进入B4。

**唯一 Planner stop：**
`B3_C3_C4_R2_POSTCOMMIT_VERIFICATION_REMAINDER_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0834-p7-retained-r3-b3-c3-c4-r1-i1-diagnostic-acceptance-review.md`；bytes `3394`，
SHA-256 `694c116325f1d8aec60789820628b66286cb7af4ae0cfe94b451237024aa59be`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r2_postcommit_verification_remainder_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-POSTCOMMIT-VERIFICATION-REMAINDER-V1","execution_authorized_after_orchestrator_activation":true,"accepted_stable_diagnostic":{"activation":"5bcc8d36488da366d717e5abd5b600a18e38fbf5","evidence":"6b2df9a376e30b971d3b021d868cc0cc4022b3bc","classification":"CANONICAL_PATCH_EXACT_MATCH","argv":["git","diff","--binary","--full-index","--no-ext-diff","f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","--","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"stdout_bytes":6006,"stdout_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","stderr_bytes":0,"provenance_drift":false,"rerun_in_this_package":0},"activation_commit":{"expected_parent":"6b2df9a376e30b971d3b021d868cc0cc4022b3bc","expected_subject":"chore(plan): resume B3 postcommit verification remainder","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0834-p7-retained-r3-b3-c3-c4-r1-i1-diagnostic-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"frozen_predecessor_contract":{"commit":"23ab2d8","path":".agent-work/PLAN.md","bytes":20343,"sha256":"31fa85881e885f2b4c878f48e7cf4f70a206d48360a3f8bcf695234d92dfa5b7","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-BASENAME-BOUND-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V2","incorporated_sections":["artifact_role_binding","manifest_top_level_contract","exact_artifact_contract","source_identity","manifest_git_recompute","governance_identities","input_roots","controller_transport","focused","fresh_synthetic","zero_budgets"],"excluded_sections":["activation_commit","repository_machine_row_contract","full","archive","required_full_machine_state","orchestrator_commit_after_handoff"],"semantic_changes_allowed":["fresh activation and root namespace","stable patch diagnostic accepted and not rerun","full expected count 800 to 810","current archive and FULL state","new Planner stop"],"all_other_incorporated_values_byte_semantically_unchanged":true},"verification_order":["manifest_self_check","focused_83","full_810","synthetic_1"],"focused":{"modules":["tests.test_p7_retained_release_audit","tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_controller_conformance","tests.test_p7_retained_r3_controller_preparation","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_r3_controller_domain_template","tests.test_p7_retained_r3_controller_runtime","tests.test_p7_retained_r3_controller_integration","tests.test_p7_retained_r3_real_manifest_domain_template"],"expected_tests":83,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":810,"invocations":1,"durable_output_required":true},"fresh_package":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-r2-<activation_short12>","root_mode":448,"absence_checks":1,"mkdirs":1,"controller_name":"controller.py","controller_mode":384,"controller_apply_patch_writes":1,"controller_invocations":1,"non_tty":true,"stdin_source":false,"preserve_after_terminal":true},"fresh_synthetic":{"root":"<fresh_package_root>/synthetic","root_mode":448,"file_mode":384,"absence_checks":1,"input_files":7,"output_artifacts":5,"builder_entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_real_manifest_domain_template.build_real_manifest_domain_template","builder_calls":1,"runtime_calls":1,"controller_processes":1,"replay_reads":5,"retry":0,"fallback":0,"consumable":false},"success_contract":{"manifest_self_check":"PASS_DERIVED_FROM_INCORPORATED_FROZEN_CHECKS","focused_exit":0,"focused_tests":83,"full_exit":0,"full_tests":810,"synthetic_exit":0,"synthetic_lifecycle_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","synthetic_replay_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","success_label":"B3_POSTCOMMIT_VERIFICATION_COMPLETE_NOT_RETAINED_ELIGIBLE","b4_unlocked_only_after_planner_acceptance":true},"execution_budgets":{"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_apply_patch_writes":1,"outer_controller_invocations":1,"manifest_remaining_self_checks":1,"focused_suites":1,"full_suites":1,"synthetic_runs":1,"synthetic_controller_processes":1,"synthetic_input_writes":7,"synthetic_output_writes":5,"synthetic_replay_reads":5,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-POSTCOMMIT-VERIFICATION-REMAINDER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_POSTCOMMIT_VERIFICATION_REMAINDER","offline_patch_preflight_owner_status":"ACCEPTED_COMPLETE","stable_patch_diagnostic_status":"ACCEPTED_COMPLETE_EXACT_MATCH","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3 postcommit verification remainder","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"stable_patch_diagnostic_reruns":0,"one_off_machine_row_parsers":0,"repository_code_writes":0,"repository_test_writes":0,"implementation_commits":0,"failed_root_reads":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"generic_schema_allowlists":0,"artifact_position_inferences":0,"inferred_terminal_passed_field_checks":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"guide_writes":0,"research_writes":0},"authorization":{"classification":"PURE_OFFLINE_POSTCOMMIT_VERIFICATION_REMAINDER","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0834-p7-retained-r3-b3-c3-c4-r1-i1-diagnostic-acceptance-review.md","bytes":3394,"sha256":"694c116325f1d8aec60789820628b66286cb7af4ae0cfe94b451237024aa59be"},"planner_stop":"B3_C3_C4_R2_POSTCOMMIT_VERIFICATION_REMAINDER_WAITING_PLANNER_REVIEW"}`

## 1. Activation与incorporated frozen contract

Activation必须是`6b2df9a...`direct child，subject/path set与PLAN/FULL required subset exact、porcelain clean。Executer必须只读取得commit
`23ab2d8:.agent-work/PLAN.md`，验证bytes/SHA exact后，仅消费machine row列出的incorporated sections；excluded history不授权执行。Stable diagnostic
`6b2df9a...`已接受，本包不得重跑或重新实现其parser/diagnostic。

Incorporated C4 contract继续冻结：real five按exact basename unique map绑定；manifest只核对object/schema/status，immutability和PASS不是artifact字段；seal/terminal/
terminal-seal/admission按exact keys/value；source、C1 four、retained three、governance position8/9与Git child/parent/tree/path/blob/file/legacy patch/seam facts独立
重算。所有real inputs只读，任何mismatch立即停且后续阶段0。

## 2. Fresh controller与ordered remainder

只创建activation-derived fresh0700 root和0600 non-TTY controller一次；controller source pre/post identity必须一致，failed roots不可读/复用。Controller不得实现machine-row
parser；配置只能来自本PLAN machine contract与verified predecessor incorporated fields。

严格顺序：

1. corrected basename-bound real manifest/Git/input self-check exact1；
2. focused九模块 exact83一次；
3. durable full discovery exact810一次；
4. brand-new synthetic root，7 inputs、builder/runtime/controller各1、5 outputs basename binding及replay5。

每阶段只有上一阶段PASS才进入；failure立即停，后续实际0，retry/fallback0。Full按现有约4分钟证据仍under10，不需visible Terminal。

## 3. EOF、locks与B4 boundary

终端前process scan1，owned非空/error即fail closed且不kill。ER只tail-read1并以第二次apply_patch physical EOF append1；记录incorporated contract identity、所有
pre/post physical facts、Git ledgers、83/810/synthetic结果、counts/locks；append后operations0、不commit。

Success只表示B3 engineering closure，不运行canonical validator、retained audit、eligibility或release。只有独立Planner接受本包后才可提出B4；Executer不得自行进入。
全部zero budgets按machine row及incorporated C4 locks执行，Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：R2复用既有basename/controller合同与accepted stable diagnostic，只更新full count并完成缺失验证链；无production或parallel owner新增。
