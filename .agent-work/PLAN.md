# P7 retained-R3 Option B：R3-C1 typed owner bounded correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-TYPED-REAL-SELF-CHECK-CORRECTION-V1`

**当前唯一动作：** 在已保留的exact-two untracked candidate中修复fixture JSON container及八项frozen production findings，然后执行一次fresh validation sequence并提交实现。

**唯一 Planner stop：** `B3_C3_C4_R3_C1_TYPED_REAL_SELF_CHECK_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0909-p7-retained-r3-b3-c3-c4-r3-targeted-static-review.md`；bytes `4144`，SHA-256 `81df9abdffdfcae0be0c5af308641efbe203742c88ef927e02c557ee3044716d`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r3_c1_typed_real_self_check_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R3-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-TYPED-REAL-SELF-CHECK-CORRECTION-V1","reviewed_r3":{"activation":"b955866b0418bf325c9dd3c0b90bfe5f2008a73e","evidence":"2a9ebca4fcddd0bfccfe051e45227c03891fecdf","decision":"REJECTED_TARGETED_FIXTURE_AND_PRODUCTION_JSON_IDENTITY_CONTRACT_DEFECTS","targeted_tests":12,"targeted_errors":12,"subject_invocations":0,"git_calls":0,"later_stages":0,"retry":0,"fallback":0},"activation_commit":{"expected_parent":"2a9ebca4fcddd0bfccfe051e45227c03891fecdf","expected_subject":"chore(plan): correct typed real self-check owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0909-p7-retained-r3-b3-c3-c4-r3-targeted-static-review.md"],"expected_untracked_after_activation":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"candidate_before":{"source":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","bytes":21578,"sha256":"e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885"},"test":{"path":"tests/test_p7_retained_r3_real_manifest_self_check.py","bytes":17922,"sha256":"d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb"}},"exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"],"preserved_public_api":["RealManifestSelfCheckError","RealManifestGitFileBytes","RealManifestSelfCheckSpec","RealManifestSelfCheckReport","required_real_manifest_git_argv","run_real_manifest_self_check"],"frozen_findings":["FIXTURE_JSON_CONTAINER","DECODED_MAPPING_IDENTITY","REPORT_JSON_CONTAINER","PHYSICAL_ROOT_IDENTITY","TYPED_POSITION_LABELS","SEAM_KEY_COLLISION","DIFF_TREE_ORDER","REPORT_LEDGER_FACTS"],"codegraph":{"accepted_pre_edit_credit":{"task":"REF-P7-25-R2-B3-C3-C4-R3","queries":1},"new_pre_edit_queries":0,"sync":1,"post_queries":1},"test_contract":{"targeted":{"module":"tests.test_p7_retained_r3_real_manifest_self_check","expected_tests":12,"invocations":1},"focused":{"modules":["tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_real_manifest_domain_template","tests.test_p7_retained_r3_real_manifest_self_check"],"expected_tests":53,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":822,"invocations":1},"postcommit_targeted":{"expected_tests":12,"invocations":1}},"implementation_commit":{"expected_parent_activation":true,"expected_subject":"fix(p7): correct real manifest self-check owner","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"execution_budgets":{"source_apply_patch_writes":1,"test_apply_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"implementation_commits":1,"postcommit_targeted_suites":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"new_pre_edit_codegraph_queries":0,"other_source_writes":0,"other_test_writes":0,"old_one_off_contract_reads":0,"real_artifact_reads":0,"retained_artifact_reads":0,"c1_artifact_reads":0,"external_root_reads":0,"external_root_writes":0,"durable_log_writes":0,"filesystem_owner_additions":0,"process_runner_additions":0,"validator_additions":0,"validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R3-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-TYPED-REAL-SELF-CHECK-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"ACTIVE_BOUNDED_CORRECTION","real_execution_status":"BLOCKED_ON_R3_C1_ACCEPTANCE","synthetic_remainder_status":"BLOCKED","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record real self-check correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_BOUNDED_CORRECTION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0909-p7-retained-r3-b3-c3-c4-r3-targeted-static-review.md","bytes":4144,"sha256":"81df9abdffdfcae0be0c5af308641efbe203742c88ef927e02c557ee3044716d"},"planner_stop":"B3_C3_C4_R3_C1_TYPED_REAL_SELF_CHECK_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与scope gate

Activation必须是`2a9ebca...`direct child、subject/path set exact；commit后porcelain只能是machine row冻结的两个untracked candidate，且bytes/SHA仍exact。任一额外path或candidate drift立即停。

只允许各一次`apply_patch`修改原source/test。不得修改P3/P5/P6/P7/M1、validator、runner、docs、skill、PLAN/FULL/archive。保留R3已完成的pre-edit CodeGraph query credit，C1不重复pre-query；这不授权跳过post-sync/query。

## 2. Exact correction contract

保持six exports、frozen dataclasses、stable error codes、P3 `FileIdentity/GitLedger/canonical_json_bytes/decode_canonical_json/run_read_only_git`与M1 typed identities复用，不新增filesystem、persistence、subprocess、validator或eligibility authority。

一次局部修复必须同时关闭：

1. Fixture在P3 encode前把activation/baseline/C1/retained及nested seam rows显式构造成JSON lists；不得放宽P3 encoder。
2. `_exact`对双方Mapping按exact key set递归比较，不要求`mappingproxy`与`dict` concrete type相同；非Mapping scalar仍要求type exact，sequence仍保持expected tuple position/type语义。
3. Report显式构造JSON-native dict/list/scalar payload；P3 canonical encode后必须strict decode/re-encode exact，不能用`default=`或通用宽松serializer。
4. 五artifact shared root须absolute lexical path、mode0700、positive device/inode；file须mode0600、positive device/inode、device绑定root、exact direct-child basename、distinct path及distinct `(device,inode)`，bytes/hash exact。
5. C1 labels/orderexact `path_owner_index,path_owner_index_seal,terminal_evidence,terminal_evidence_seal`；retained labels/orderexact `current_lineage_candidate,resolved_formal_plan,setup_lineage_release`。
6. Activation commit/parent、baseline release/helper/integration及helper/test paths须满足exact chain distinctness；构造expected Git file keys前证明cardinality未因collision折叠，seam before/after bytes SHA-256与Git blob OID exact。
7. Diff-tree decoded stdout path tuple必须与sorted unique activation paths exact同序；swapped、duplicate、missing、extra、invalid UTF-8均fail closed。
8. Canonical report与`RealManifestSelfCheckReport`须逐条保存validated ledger的exact argv、cwd、exit code、stdout SHA-256、stderr SHA-256；继续明确`eligibility=false`、`release_consumable=false`、`authority=subordinate_self_check_only`。

不得从fixture failure推断production通过；不得减少既有five artifact、typed manifest、Git verify/metadata/blob/full patch/two seam patch覆盖。

## 3. Exact12 regression与fresh sequence

维持exact12 methods，不增减count；在现有测试中补齐八finding正负例。Golden success须真正进入subject并完成18条fake Git ledger、canonical report roundtrip与determinism。Negative cases须断言stable first code及pre-Git/first-mismatch call count；特别覆盖shared-invalid-root、inode alias、wrong labels/order、mappingproxy-vs-dict、JSON list report、key collision、swapped diff-tree与完整ledger facts。

严格fresh顺序：targeted12 → focused53 → full822 → compileall exact source → CodeGraph sync/post-query → `git diff --check`与exact-two status → commit → postcommit targeted12。任一步失败立即停，后续0，retry/fallback0。提交只能含exact two paths，parent为activation，subject exact machine row。

## 4. Handoff与locks

Terminal前process scan1且不kill/cleanup。ER只在physical EOF一次`apply_patch`追加activation/candidate before-after identity、八finding closure、18 Git facts、test/compile/CodeGraph/commit topology、all zero budgets；append后operations0。Executer不得提交ER或修改plan files。

C1接受前real execution、real artifacts、validator、eligibility、release、synthetic、网络与设备全部锁0。C1成功仅使Planner可规划后续独立real execution package，不授予B3或retained eligibility credit。

维护性判断：修复限定同一owner/test，不改变six-export或权限边界；严格JSON与physical/Git identity由单一owner负责，完整负例覆盖避免再次依赖one-off执行合同。
