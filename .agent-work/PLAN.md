# P7 retained-R3 Option B：R3-C1-R1 fresh typed owner correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-FRESH-TYPED-OWNER-CORRECTION-V1`

**当前唯一动作：** 不做新的pre-edit发现，直接在same exact-two candidate中关闭已冻结八findings，执行fresh targeted12/focused53/full822/compileall/CodeGraph post validation并提交实现。

**唯一 Planner stop：** `B3_C3_C4_R3_C1_R1_FRESH_TYPED_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0926-p7-retained-r3-b3-c3-c4-r3-c1-s1-acceptance.md`；bytes `2871`，SHA-256 `3701930e115ef23f0e5f0de966fd4709bde934e2b4cf73e7a9d3ee63d1c83e8b`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r3_c1_r1_fresh_typed_owner_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R3-C1-R1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-FRESH-TYPED-OWNER-CORRECTION-V1","accepted_s1":{"activation":"0ef6198038160ac19cfeaa780a289c9a9f0cd360","evidence":"3bc46c5a866d5f3f8d303224fcb582a4de630e8d","decision":"ACCEPTED_COMPLETE_PHYSICAL_EOF_SUPERSESSION","supersession_append_bytes":4133,"supersession_append_sha256":"0df6b914dca2988607d2adf403bbd6467beb410f93906d9c1443ed5cdd93591b","candidate_identity_exact":true,"production_credit":false},"activation_commit":{"expected_parent":"3bc46c5a866d5f3f8d303224fcb582a4de630e8d","expected_subject":"chore(plan): resume real self-check correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0926-p7-retained-r3-b3-c3-c4-r3-c1-s1-acceptance.md"],"expected_untracked_after_activation":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"candidate_before":{"source":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","bytes":21578,"sha256":"e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885"},"test":{"path":"tests/test_p7_retained_r3_real_manifest_self_check.py","bytes":17922,"sha256":"d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb"}},"exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"],"preserved_public_api":["RealManifestSelfCheckError","RealManifestGitFileBytes","RealManifestSelfCheckSpec","RealManifestSelfCheckReport","required_real_manifest_git_argv","run_real_manifest_self_check"],"frozen_findings":["FIXTURE_JSON_CONTAINER","DECODED_MAPPING_IDENTITY","REPORT_JSON_CONTAINER","PHYSICAL_ROOT_IDENTITY","TYPED_POSITION_LABELS","SEAM_KEY_COLLISION","DIFF_TREE_ORDER","REPORT_LEDGER_FACTS"],"orchestrator_provided_contract":true,"pre_edit_discovery":{"codegraph_queries":0,"codegraph_sync":0,"other_discovery_queries":0},"test_contract":{"targeted":{"module":"tests.test_p7_retained_r3_real_manifest_self_check","expected_tests":12,"invocations":1},"focused":{"modules":["tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_real_manifest_domain_template","tests.test_p7_retained_r3_real_manifest_self_check"],"expected_tests":53,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":822,"invocations":1},"postcommit_targeted":{"expected_tests":12,"invocations":1}},"implementation_commit":{"expected_parent_activation":true,"expected_subject":"fix(p7): correct real manifest self-check owner","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"execution_budgets":{"candidate_identity_reads":2,"source_apply_patch_writes":1,"test_apply_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"pre_edit_codegraph_queries":0,"pre_edit_codegraph_sync":0,"pre_edit_discovery_queries":0,"other_source_writes":0,"other_test_writes":0,"old_one_off_contract_reads":0,"real_artifact_reads":0,"retained_artifact_reads":0,"c1_artifact_reads":0,"external_root_reads":0,"external_root_writes":0,"durable_log_writes":0,"filesystem_owner_additions":0,"process_runner_additions":0,"validator_additions":0,"validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R3-C1-R1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-FRESH-TYPED-OWNER-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"ACTIVE_FRESH_BOUNDED_CORRECTION","real_execution_status":"BLOCKED_ON_R3_C1_R1_ACCEPTANCE","synthetic_remainder_status":"BLOCKED","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record fresh real self-check correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_FRESH_BOUNDED_CORRECTION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0926-p7-retained-r3-b3-c3-c4-r3-c1-s1-acceptance.md","bytes":2871,"sha256":"3701930e115ef23f0e5f0de966fd4709bde934e2b4cf73e7a9d3ee63d1c83e8b"},"planner_stop":"B3_C3_C4_R3_C1_R1_FRESH_TYPED_OWNER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、identity与no-discovery gate

Activation必须是`3bc46c5...`direct child、subject/path set exact；commit后porcelain只能是machine row exact-two untracked candidate。读取两文件只为核对冻结bytes/SHA并执行指定patch，不得重新做架构/semantic discovery。

Orchestrator已经提供完整八findings及下述修复合同。Pre-edit阶段禁止调用CodeGraph explore/sync、grep式发现、测试或其他诊断；相关counts必须全0。若合同与candidate出现无法局部解决的矛盾，立即停并handoff，不得用新query自行扩展范围。

## 2. One source patch + one test patch

保持six exports、frozen dataclasses、stable error codes及P3/M1 imports；只各一次`apply_patch`：

1. Fixture所有manifest nested rows在P3 encode前显式转为JSON lists；不放宽P3 encoder。
2. `_exact`先处理双方Mapping：exact key set、递归value/type；非Mapping scalar继续concrete type exact，decoded JSON arrays与expected typed tuple positions exact。
3. Success report显式创建JSON-native dict/list/scalar；P3 canonical encode并strict decode/re-encode exact。禁止`default=`、pickle或宽松serializer。
4. Shared artifact root验证absolute lexical path、mode0700、positive device/inode；files验证mode0600、positive device/inode、device绑定root、exact direct-child basenames、distinct paths及distinct `(device,inode)`、bytes/hash exact。
5. C1 exact ordered labels为`path_owner_index,path_owner_index_seal,terminal_evidence,terminal_evidence_seal`；retained exact ordered labels为`current_lineage_candidate,resolved_formal_plan,setup_lineage_release`。
6. Activation child/parent、baseline release/helper/integration及helper/test paths证明exact chain distinct；expected Git file keys先证明cardinality未collision，再作set equality；seam bytes SHA-256/Git blob OID exact。
7. Diff-tree stdout decode tuple必须与activation changed_paths exact同序；swapped/duplicate/missing/extra/invalid UTF-8 fail closed。
8. `RealManifestSelfCheckReport`与canonical payload逐条记录validated ledger的argv、cwd、exit code、stdout SHA-256、stderr SHA-256；仍固定`eligibility=false`、`release_consumable=false`、`authority=subordinate_self_check_only`。

不得删减five artifact canonical/type/root/path/hash、typed manifest positions、18 ordered Git commands、activation full patch、two seam patches、blob bytes/OID/SHA验证，不得新增filesystem/persistence/subprocess/validator/eligibility authority。

## 3. Fresh exact validation sequence

Tests保持exact12 methods，在既有methods内覆盖八finding。Golden success必须真实进入subject、执行18条fake Git ledger并验证canonical report roundtrip/determinism/full ledger facts。Negative cases断言stable first code与pre-Git/first-mismatch call count，至少包括mappingproxy/dict、shared invalid root、inode alias、wrong labels/order、key collision、swapped diff-tree及tuple-free report。

严格顺序且各一次：

1. targeted exact12；
2. focused exact53（P3 28 + M1 13 + owner 12）；
3. full discovery exact822；
4. compileall exact source/test；
5. `codegraph sync`一次，然后单次post-query确认six exports/call paths/no new authority；
6. `git diff --check`及status exact-two；
7. commit exact subject/path/parent；
8. postcommit targeted exact12。

任一步失败立即停，后续0，retry/fallback0。CodeGraph只允许步骤5，任何提前query均hard failure。

## 4. Handoff与locks

Terminal前process scan1、owned0，不kill/cleanup。ER tail read一次，以当前最后S1 supersession完整block为full-tail anchor，一次`apply_patch`追加physical EOF handoff；append后operations0。记录activation、candidate before/after、八finding closure、tests/compile/CodeGraph/diff/commit topology与所有locks。Executer不得commit ER或修改plan files。

R1成功只提交repo-owned subordinate self-check owner，不执行real artifacts、validator、eligibility、release、synthetic、网络或设备，也不授予B3 credit。Planner接受后才规划独立real execution package。

维护性判断：R1在现有exact-two owner/test内关闭已知语义缺陷；无新发现阶段、无新owner、权限与I/O边界保持不变。
