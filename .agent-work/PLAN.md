# P7 retained-R3 Option B：R3-C1-S1 physical-EOF supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-S1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-S1-PHYSICAL-EOF-SUPERSESSION-V1`

**当前唯一动作：** 只用Git、ER与candidate identity核对R3-C1的只读预算超限及non-EOF placement，并在ER physical EOF追加一次canonical supersession。

**唯一 Planner stop：** `B3_C3_C4_R3_C1_S1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0918-p7-retained-r3-b3-c3-c4-r3-c1-non-eof-review.md`；bytes `3229`，SHA-256 `1f862ef75dafed278b16d061e1f860db0948ed96d5e83ff1ec0ab0c6f2d819c5`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r3_c1_s1_physical_eof_supersession_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R3-C1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-S1-PHYSICAL-EOF-SUPERSESSION-V1","reviewed_r3_c1":{"activation":"ff372c136516fd785ec94adfeeb50063c3873c83","evidence":"b83ba49031d48c1545011fc7ca64910d636f575e","decision":"REJECTED_READ_ONLY_QUERY_BUDGET_EXCEEDED_AND_HANDOFF_NOT_AT_PHYSICAL_EOF","new_pre_edit_codegraph_queries":1,"budget":0,"patch_writes":0,"tests":0,"implementation_commits":0},"activation_commit":{"expected_parent":"b83ba49031d48c1545011fc7ca64910d636f575e","expected_subject":"chore(plan): supersede non-eof correction handoff","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0918-p7-retained-r3-b3-c3-c4-r3-c1-non-eof-review.md"],"expected_untracked_after_activation":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"candidate_identity":{"source":{"bytes":21578,"sha256":"e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885"},"test":{"bytes":17922,"sha256":"d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb"}},"er_identity":{"before":{"blob":"a91062d7a47b4e20e5bed0e2ad1badd8932b3ee7","bytes":1389034,"sha256":"4a3bfe71e531b98d2ed76adf70eb9b9fde390c9ed3a673191f5f16474f6aee23"},"after":{"blob":"ecd97ade34e5aa7402afbe945d7194307e9284b4","bytes":1392359,"sha256":"e1407040bf5d1c454706cf1e4242d034f243539118db1f4aebab391ceabcca2b"},"logical_prefix":{"lines":40,"bytes":2580,"sha256":"6c18f5e876c3eb59b63fa9f6ddf8d42a7513bc5254dc1231c6c84d20feeb6f14"},"inserted_block":{"starts_at_line":41,"lines":6,"bytes":3325,"sha256":"7ad28a388ec2f94e01ac128ed90b2ce854d97ad80c3aaf049ab6c37edb387c5d"},"preserved_suffix":{"starts_at_old_line":41,"starts_at_new_line":47,"lines":17705,"bytes":1386454,"sha256":"e69917f5a7017510bb9c0b5c79c77440d18bd5816300dd3ce856fb1d72229e58"},"final_256_sha256":"039f56395f2649fbce1ada716feb34f58394d11dd714f29d253de070bcdb5ed4"},"frozen_findings_after_s1":["FIXTURE_JSON_CONTAINER","DECODED_MAPPING_IDENTITY","REPORT_JSON_CONTAINER","PHYSICAL_ROOT_IDENTITY","TYPED_POSITION_LABELS","SEAM_KEY_COLLISION","DIFF_TREE_ORDER","REPORT_LEDGER_FACTS"],"success_contract":{"candidate_identity_exact":true,"activation_evidence_topology_exact":true,"extra_query_classification":"READ_ONLY_BUDGET_EXCESS_NO_CREDIT","non_eof_block_preserved":true,"preserved_suffix_exact":true,"canonical_supersession_at_physical_eof":true,"production_credit":false,"next_branch":"REF-P7-25-R2-B3-C3-C4-R3-C1-R1"},"execution_budgets":{"git_topology_queries":2,"candidate_identity_reads":2,"er_identity_reads":2,"er_line_comparisons":1,"er_placement_searches":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"codegraph_queries":0,"codegraph_sync":0,"source_edits":0,"test_edits":0,"tests":0,"compileall":0,"implementation_commits":0,"old_block_edits":0,"er_rewrites":0,"real_artifact_reads":0,"retained_artifact_reads":0,"c1_artifact_reads":0,"external_root_reads":0,"external_root_writes":0,"validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R3-C1-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-S1-PHYSICAL-EOF-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"BLOCKED_ON_HANDOFF_SUPERSESSION","real_execution_status":"BLOCKED","synthetic_remainder_status":"BLOCKED","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): supersede non-eof correction handoff","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0918-p7-retained-r3-b3-c3-c4-r3-c1-non-eof-review.md","bytes":3229,"sha256":"1f862ef75dafed278b16d061e1f860db0948ed96d5e83ff1ec0ab0c6f2d819c5"},"planner_stop":"B3_C3_C4_R3_C1_S1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与read-only gates

Activation必须是`b83ba49...`direct child、subject/path set exact；commit后porcelain只能是machine row的exact-two untracked candidate。先用bytes/SHA核对candidate未变；不得阅读或解释production语义。

只读核对`ff372c1`、`b83ba49` topology与ER before/after identity。确认新增CodeGraph query exact1、预算0、source/test patch0、tests0；将其分类为`READ_ONLY_BUDGET_EXCESS_NO_CREDIT`，不得升级为科学/设备问题，也不得把它计作恢复包的CodeGraph evidence。

## 2. Non-EOF proof

用line-aware exact comparison复现machine row：前40行prefix exact；line41的6-line/3325-byte block exact；old line41 onward与new line47 onward的17705-line preserved suffix byte exact；final256 hash unchanged。任一bytes/hash/line boundary mismatch立即停且ER append0。

现有non-EOF block必须保持byte-for-byte不变；不得删除、移动、改写或重新提交candidate。

## 3. Single physical-EOF supersession

所有gate通过后，读取ER当前physical tail一次，并以包含当前最后完整handoff block的exact full-tail anchor调用一次`apply_patch`在真正EOF追加：heading + 单行strict canonical JSON + fence。不得使用早期重复heading、短锚点或line-number insertion。

Supersession JSON必须记录本PLAN reference/contract、activation/evidence、candidate two hashes、extra query actual/budget/classification、ER before/after blob/bytes/SHA、prefix/insert/suffix/final256 facts，并明确：

- `supersedes_non_eof_block_status=B3_C3_C4_R3_C1_PRE_EDIT_QUERY_BUDGET_FAILED_WAITING_PLANNER_REVIEW`；
- old block preserved、authority降级为historical non-terminal；
- R3-C1仍rejected，patch/tests/production credit为0；
- 八findings保持未修复；next branch exact `REF-P7-25-R2-B3-C3-C4-R3-C1-R1`；
- real/validator/eligibility/release/network/device全部locked；
- stop exact machine row Planner stop。

Append前process scan1、owned0；不kill/cleanup。Apply patch完成后operations0，不读回、不commit。Executer不得修改PLAN/FULL/archive。

## 4. Acceptance与next branch

Planner只在提交后的独立审计证明supersession位于physical EOF、旧block与preserved suffix未变、candidate hashes未变时接受S1。S1不给production或B3 credit。

S1接受后规划fresh `R3-C1-R1`：same exact-two correction、同八findings、new pre-edit CodeGraph query冻结0，直接进入patch→target12→focused53→full822→compileall→post-sync/query→commit→posttarget；本S1不授权该执行。

维护性判断：单一EOF supersession保存不可变审计历史并恢复terminal authority；不触碰production owner或扩张验证框架。
