# P7 retained-R3 Option B：B3-C3-C4-S1-C1 physical-EOF supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-S1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-S1-C1-GIT-ER-PHYSICAL-EOF-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先建立exact activation；fresh Executer随后只核对committed Git/PLAN/FULL/ER，将
`ef1f9d0`中位置错误但内容canonical的C4 zero-effect record原样语义在ER physical EOF重录，并标记旧record仅为
noncanonical-positioned historical evidence。

**唯一 Planner stop：**
`B3_C3_C4_S1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0659-p7-retained-r3-b3-c3-c4-s1-non-eof-review.md`；bytes `4095`，SHA-256
`adbd3163a260adbf27bb187654a4ec8581b84fcb61898234fd95d4bbe2017df1`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_s1_c1_git_er_physical_eof_supersession_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-S1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-S1-C1-GIT-ER-PHYSICAL-EOF-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_execution":{"activation":"7e3e74f4b7766f6a8832dea99dccef2e5ca6bb8b","evidence_commit":"ef1f9d02515ae627bcf679f6a77238097255208a","decision":"REJECTED_NON_PHYSICAL_EOF_HANDOFF_CANONICAL_CONTENT_PRESERVED","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"parent_er_bytes":1340617,"parent_er_sha256":"e2cc3c5fc8a28bcb17262a25e23a2472b9f6a66db5fd326530733f477513e3ac","evidence_er_bytes":1343116,"evidence_er_sha256":"257ce792fec070ac63a0bdf43376aa11a698620ad6c6ce7d33620ac63768af82","canonical_record_content_accepted":true,"record_physical_eof":false,"record_inserted_after_old_line":38,"old_er_no_write_before_c4_s1":true},"repository_machine_row_contract":{"plan_delimiter":"PLAN_MACHINE_CONTRACT=","full_delimiter":"FULL_PLAN_MACHINE_STATE=","plan_physical_prefix":"`PLAN_MACHINE_CONTRACT=","full_physical_prefix":"`FULL_PLAN_MACHINE_STATE=","physical_suffix":"`","json_payload_slice":"AFTER_DELIMITER_BEFORE_FINAL_BACKTICK","forbidden_interpretation":"DELIMITER_THEN_OPENING_BACKTICK","exact_row_count_each":1,"decode":"strict_utf8","parse":"json_object_duplicate_free_nonfinite_safe","compare":"typed_semantic_fields_only","canonical_reencode":false,"generic_scanner":false},"review_archive":{"path":".agent-work/PLANS/20260801-0659-p7-retained-r3-b3-c3-c4-s1-non-eof-review.md","bytes":4095,"sha256":"adbd3163a260adbf27bb187654a4ec8581b84fcb61898234fd95d4bbe2017df1"},"execution_result_baseline":{"path":".agent-work/EXECUTION_RESULT.md","bytes":1343116,"sha256":"257ce792fec070ac63a0bdf43376aa11a698620ad6c6ce7d33620ac63768af82","blob_oid":"74819299d459b0138215184b00cbe2503d6eaf9f","must_be_unchanged_by_activation":true},"activation_commit":{"expected_parent":"ef1f9d02515ae627bcf679f6a77238097255208a","expected_subject":"chore(plan): activate B3-C3-C4-S1-C1 EOF supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0659-p7-retained-r3-b3-c3-c4-s1-non-eof-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task":"REF-P7-25-R2-B3-C3-C4-S1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-S1-C1-GIT-ER-PHYSICAL-EOF-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","b3_c3_c4_s1_status":"REJECTED_NON_PHYSICAL_EOF_HANDOFF_CANONICAL_CONTENT_PRESERVED","b3_c3_c4_s1_c1_status":"ACTIVE_GIT_ER_PHYSICAL_EOF_SUPERSESSION","executer_dispatched":true},"physical_eof_append_algorithm":{"step_1":"READ_COMMITTED_CURRENT_ER_ONCE_AND_REQUIRE_EXACT_BASELINE_IDENTITY","step_2":"TAIL_READ_ONCE_AND_IDENTIFY_UNIQUE_FINAL_SECTION_BEGINNING_WITH_EXACT_HEADING_B3_C3_C3_NON_EOF_HANDOFF_CANONICAL_SUPERSESSION","step_3":"REQUIRE_FINAL_SECTION_BYTES_ARE_THE_LITERAL_FILE_SUFFIX_ENDING_WITH_NEWLINE_FENCE_NEWLINE","step_4":"BUILD_ONE_APPLY_PATCH_HUNK_WHOSE_OLD_CONTEXT_IS_THAT_EXACT_FINAL_SECTION_SUFFIX_AND_WHOSE_REPLACEMENT_IS_IDENTICAL_SUFFIX_PLUS_EXACT_NEW_TERMINAL_RECORD","step_5":"DO_NOT_MATCH_A_BARE_FENCE_OR_NONFINAL_REPEATED_CONTEXT_AND_DO_NOT_INSERT_AFTER_ANY_EARLIER_SECTION","step_6":"ONE_SUCCESSFUL_UNDERLYING_APPLY_PATCH_ONLY_THEN_ZERO_POSTAPPEND_OPERATIONS","required_final_anchor_heading":"## 2026-08-01 B3-C3-C3 non-EOF handoff canonical supersession","required_old_file_terminal_bytes":"NEWLINE_TRIPLE_BACKTICK_NEWLINE","parent_prefix_acceptance_owner":"ORCHESTRATOR_AND_PLANNER_POSTCOMMIT_GIT_REVIEW"},"terminal_record":{"heading":"P7 retained-R3 Option B B3-C3-C4-S1 non-EOF record canonical physical-EOF supersession","status":"B3_C3_C4_S1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW","append":"PHYSICAL_EOF_ONLY","payload":"STRICT_JSON_OBJECT","supersedes_commit":"ef1f9d02515ae627bcf679f6a77238097255208a","supersedes_heading":"P7 retained-R3 Option B B3-C3-C4 no-handoff zero-effect terminal record","superseded_section_status":"NONCANONICAL_POSITIONED_HISTORICAL_EVIDENCE","required_canonical_facts":{"activation_gate":"PASS","machine_row_failure":"PLAN_ROW_COUNT_0_FROM_DELIMITER_THEN_BACKTICK_MISINTERPRETATION","typed_semantic_comparison_performed":false,"fresh_package_creates":0,"controller_invocations":0,"self_checks":0,"focused_invocations":0,"full_invocations":0,"synthetic_invocations":0,"external_root_reads":0,"fresh_root_reads":0,"er_apply_patch_wrapper_attempts":1,"er_apply_patch_underlying_calls":0,"prior_er_appends":0,"worktree_clean_after_stop":true,"verification_passed":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","eligibility_emitted":false,"release_consumable":false}},"execution_budgets":{"repository_file_decodes":2,"repository_machine_row_extractions":2,"git_read_invocations_max":12,"archive_identity_reads":1,"execution_result_identity_reads_before_append":1,"execution_result_tail_reads":1,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"forbidden_actions":["fresh_or_external_root_read_or_write","controller_create_or_invoke","self_check","focused_or_full_tests","synthetic","production_or_test_source_read_or_write","codegraph","canonical_validator","retained_audit","eligibility","release","network_or_device_adjacent_work","delete_move_or_repair_old_non_eof_record","plan_full_archive_write_by_executer","commit_by_executer"],"orchestrator_commit_after_handoff":{"expected_subject":"chore(evidence): seal B3-C3-C4-S1 EOF supersession","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_ONLY_PHYSICAL_EOF_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"planner_stop":"B3_C3_C4_S1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与只读 precondition

Activation必须是`ef1f9d02515ae627bcf679f6a77238097255208a`的direct child，subject及exact three-path set按machine row，且
不得改变ER baseline；activation后porcelain clean。Executer只读取committed/current PLAN和FULL各一次，按整行single-backtick物理边界提取
各自唯一machine row；JSON payload从delimiter之后切到final backtick之前，禁止解释成delimiter之后才出现opening backtick。只作
duplicate-free/non-finite-safe typed field比较，不做canonical reencode或generic scan。

Executer只读核对review archive identity、activation identity与current ER exact baseline。不得读取任何external/fresh root、
production/test source、retained artifact或旧failed package。

## 2. 唯一 physical-EOF supersession write

严格按`physical_eof_append_algorithm`执行：ER current committed内容只做一次identity read及一次tail read。Tail必须证明以exact
`required_final_anchor_heading`开始的final section就是literal file suffix，且文件终止字节为newline + closing fence + newline。唯一一次
successful underlying `apply_patch`必须以该完整final-section suffix作为old context，在保持suffix逐byte不变后追加新section；禁止只用bare
fence、短重复context或任何前部heading定位。若unique/final条件任一不满足，fail closed且write 0；patch失败时retry 0，不得换用shell、
Python或其他writer。

新record须以machine row指定heading开头，payload逐项保留`required_canonical_facts`，并明确`ef1f9d0`旧前部record只是
`NONCANONICAL_POSITIONED_HISTORICAL_EVIDENCE`。不得删除、移动、修复或改写旧record。Append后operations 0并停止、不commit；physical
prefix与EOF位置由Orchestrator及下轮Planner从committed Git独立验收。

成功只表示ER physical-EOF supersession等待验收，不恢复basename verification，不解锁B4。Retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`；validator、eligibility、release、network、device、camera、Ray、strip、formal、TD-C、sentinel与P8均锁定。
无需Advisor科学决策或Human设备授权。

维护性判断：本包只修ER物理位置并保存旧记录；不改production/test/controller/provenance owner，也不新增抽象。
