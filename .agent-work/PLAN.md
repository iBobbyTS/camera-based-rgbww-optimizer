# P7 retained-R3 Option B：B3-C3-C4-R2-C1 real verification remainder

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R2-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-C1-REAL-SELF-CHECK-TEST-REMAINDER-V1`

**当前唯一动作：** 只完成B3的real manifest/Git/input self-check → focused83 → durable full810。Fresh synthetic/replay拆到下一独立包，C1未被
Planner接受前保持锁定；不得从聊天或failed roots补执行常量。

**唯一 Planner stop：**
`B3_C3_C4_R2_C1_REAL_SELF_CHECK_TEST_REMAINDER_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0844-p7-retained-r3-b3-c3-c4-r2-incomplete-contract-review.md`；bytes `3464`，SHA-256
`c6660c8a18d930cabba63568fb16c2b6de21a71835efd9ccfc0dff31c8c6ade1`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r2_c1_real_self_check_test_remainder_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R2-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-C1-REAL-SELF-CHECK-TEST-REMAINDER-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_r2":{"activation":"e8ca8829f9209284dd74fa37d46a60e0388dcb11","evidence":"c0e878653a72966c3890f5371d2e271e4d0009db","decision":"REJECTED_PRE_EFFECT_INCORPORATED_CONTROLLER_EXECUTION_CONSTANTS_INCOMPLETE","predecessor_identity_match":true,"root_controller_input_effects":0,"manifest_self_check":0,"focused":0,"full":0,"synthetic":0,"retry":0,"fallback":0},"activation_commit":{"expected_parent":"c0e878653a72966c3890f5371d2e271e4d0009db","expected_subject":"chore(plan): split B3 real verification remainder","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0844-p7-retained-r3-b3-c3-c4-r2-incomplete-contract-review.md"],"clean_porcelain_required_after_activation":true},"accepted_stable_diagnostic":{"evidence":"6b2df9a376e30b971d3b021d868cc0cc4022b3bc","classification":"CANONICAL_PATCH_EXACT_MATCH","stdout_bytes":6006,"stdout_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","rerun":0},"frozen_real_contract":{"commit":"23ab2d8","path":".agent-work/PLAN.md","bytes":20343,"sha256":"31fa85881e885f2b4c878f48e7cf4f70a206d48360a3f8bcf695234d92dfa5b7","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-BASENAME-BOUND-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V2","incorporated_sections":["accepted_implementation","real_manifest_reference","artifact_role_binding","manifest_top_level_contract","exact_artifact_contract","source_identity","manifest_git_recompute","governance_identities","input_roots","controller_transport","focused","zero_budgets"],"excluded_sections":["activation_commit","repository_machine_row_contract","fresh_synthetic","full","success_contract","execution_budgets","archive","required_full_machine_state","orchestrator_commit_after_handoff"],"all_incorporated_values_byte_semantically_unchanged":true,"chat_supplied_constants":0,"failed_root_recovery":0},"verification_order":["manifest_self_check","focused_83","full_810"],"focused":{"modules":["tests.test_p7_retained_release_audit","tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_controller_conformance","tests.test_p7_retained_r3_controller_preparation","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_r3_controller_domain_template","tests.test_p7_retained_r3_controller_runtime","tests.test_p7_retained_r3_controller_integration","tests.test_p7_retained_r3_real_manifest_domain_template"],"expected_tests":83,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":810,"invocations":1,"durable_output_required":true},"fresh_package":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c4-r2-c1-<activation_short12>","root_mode":448,"absence_checks":1,"mkdirs":1,"controller_name":"controller.py","controller_mode":384,"controller_apply_patch_writes":1,"controller_invocations":1,"non_tty":true,"stdin_source":false,"preserve_after_terminal":true},"success_contract":{"manifest_self_check":"PASS_DERIVED_FROM_INCORPORATED_FROZEN_CHECKS","focused_exit":0,"focused_tests":83,"full_exit":0,"full_tests":810,"success_label":"B3_REAL_SELF_CHECK_AND_TEST_REMAINDER_PASS_SYNTHETIC_STILL_REQUIRED","synthetic_completed":false,"b4_unlocked":false},"execution_budgets":{"predecessor_contract_reads":1,"fresh_package_absence_checks":1,"fresh_package_mkdirs":1,"controller_source_apply_patch_writes":1,"outer_controller_invocations":1,"manifest_remaining_self_checks":1,"focused_suites":1,"full_suites":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R2-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R2-C1-REAL-SELF-CHECK-TEST-REMAINDER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_REAL_SELF_CHECK_TEST_REMAINDER","offline_patch_preflight_owner_status":"ACCEPTED_COMPLETE","stable_patch_diagnostic_status":"ACCEPTED_COMPLETE_EXACT_MATCH","synthetic_remainder_status":"BLOCKED_ON_R2_C1_ACCEPTANCE","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3 real verification remainder","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"stable_patch_diagnostic_reruns":0,"synthetic_runs":0,"synthetic_controller_processes":0,"synthetic_input_writes":0,"synthetic_output_writes":0,"synthetic_replay_reads":0,"repository_code_direct_reads":0,"repository_test_direct_reads":0,"repository_code_writes":0,"repository_test_writes":0,"implementation_commits":0,"failed_root_reads":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"generic_schema_allowlists":0,"artifact_position_inferences":0,"inferred_terminal_passed_field_checks":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"guide_writes":0,"research_writes":0},"authorization":{"classification":"PURE_OFFLINE_REAL_SELF_CHECK_TEST_REMAINDER","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0844-p7-retained-r3-b3-c3-c4-r2-incomplete-contract-review.md","bytes":3464,"sha256":"c6660c8a18d930cabba63568fb16c2b6de21a71835efd9ccfc0dff31c8c6ade1"},"planner_stop":"B3_C3_C4_R2_C1_REAL_SELF_CHECK_TEST_REMAINDER_WAITING_PLANNER_REVIEW"}`

## 1. Activation与complete real contract

Activation必须是`c0e8786...`direct child，subject/path set与PLAN/FULL required subset exact、porcelain clean。Effect前只读取得
`23ab2d8:.agent-work/PLAN.md`并验证bytes/SHA；只消费machine row列出的real incorporated sections。Synthetic及excluded history不授权执行。

Controller只能使用incorporated exact basename map、artifact/source/C1/retained/governance/Git constants；不得从聊天、code/test direct reads、failed roots或猜测补值。
Fresh root/controller transport按incorporated contract，source pre/post identity一致。

## 2. Ordered real remainder

严格顺序：

1. Real five exact basename binding；manifest object/schema/status、seal/terminal/admission exact contracts；source、C1 four、retained three、governance positions及Git
   child/parent/tree/path/blob/file/legacy patch/seam facts独立重算；全部real inputs只读。Mismatch立即停。
2. Focused九模块exact83一次。
3. Durable full discovery exact810一次。

每阶段仅上一阶段PASS后进入；failure后续0，retry/fallback0。C1不创建synthetic root、不调用builder/runtime/synthetic controller。

## 3. EOF、locks与next dependency

Terminal前process scan1；不kill/cleanup。ER tail-read1、second apply_patch physical EOF append1，记录contract identity、real pre/post facts、Git ledgers、83/810、
counts/locks；append后operations0、不commit。

C1 success仍不关闭B3，也不解锁B4；只解锁下一fresh synthetic/replay package。下一Planner必须引用accepted P7-I1 committed integration contract冻结完整7 inputs、callable/args、
controller argv/input与5-output lifecycle/replay，不能从本PLAN推导。

Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`，validator/audit/eligibility/release/network/device全部锁0。

维护性判断：拆包只消费完整committed real contract，降低state complexity；synthetic由accepted integration contract另包拥有，不增加production抽象。
