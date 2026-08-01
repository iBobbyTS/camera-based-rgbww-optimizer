# P7 retained-R3 Option B：R3-C1-R1-C1 P3 frozen-sequence correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1-C1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-C1-P3-FROZEN-SEQUENCE-CORRECTION-V1`

**当前唯一动作：** 在preserved exact-two candidate中局部修复P3 frozen tuple/JSON list comparison、decoded report re-native及三个误绑定targeted assertions，然后执行fresh完整验证并提交。

**唯一 Planner stop：** `B3_C3_C4_R3_C1_R1_C1_P3_FROZEN_SEQUENCE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0938-p7-retained-r3-b3-c3-c4-r3-c1-r1-targeted-sequence-review.md`；bytes `4190`，SHA-256 `27fdee8093b132ac10681f27183e65c3179e468dabf94cebdafff6d8b3e5acb4`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r3_c1_r1_c1_p3_frozen_sequence_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R3-C1-R1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-C1-P3-FROZEN-SEQUENCE-CORRECTION-V1","reviewed_r1":{"activation":"fb97fe449bec04eda78c85e91a9185fde6139a98","evidence":"27424dd1feedb620d8b527c7aea4e8d27010dbed","decision":"REJECTED_TARGETED_P3_FROZEN_SEQUENCE_REPRESENTATION_MISMATCH","targeted":{"tests_run":12,"failures":8,"errors":3,"exit_code":1,"primary":"manifest_contract_mismatch"},"later_stages":0,"retry":0,"fallback":0,"physical_eof_handoff":true},"activation_commit":{"expected_parent":"27424dd1feedb620d8b527c7aea4e8d27010dbed","expected_subject":"chore(plan): correct P3 typed sequence boundary","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0938-p7-retained-r3-b3-c3-c4-r3-c1-r1-targeted-sequence-review.md"],"expected_untracked_after_activation":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"candidate_before":{"source":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","bytes":24679,"sha256":"ddb20f987ab728489f9898ffd2ebcb23cf2100bb332c56d93653529453f7796c"},"test":{"path":"tests/test_p7_retained_r3_real_manifest_self_check.py","bytes":21583,"sha256":"5caef9716070f3a78a1ee1c73754dc3f0eb6a0c9259c3da4399a7ff3c2d11859"}},"exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"],"preserved_public_api":["RealManifestSelfCheckError","RealManifestGitFileBytes","RealManifestSelfCheckSpec","RealManifestSelfCheckReport","required_real_manifest_git_argv","run_real_manifest_self_check"],"carried_findings":["FIXTURE_JSON_CONTAINER","DECODED_MAPPING_IDENTITY","REPORT_JSON_CONTAINER","PHYSICAL_ROOT_IDENTITY","TYPED_POSITION_LABELS","SEAM_KEY_COLLISION","DIFF_TREE_ORDER","REPORT_LEDGER_FACTS"],"bounded_corrections":["JSON_SEQUENCE_TUPLE_LIST_SEMANTIC_EQUIVALENCE","DECODED_REPORT_RENATIVE_BEFORE_REENCODE","SEAM_BYTES_NEGATIVE_PRESERVES_TUPLE","SEAM_OID_NEGATIVE_REACHES_REQUIRED_ARGV_OWNER","KEY_COLLISION_NEGATIVE_REACHES_REQUIRED_ARGV_OWNER"],"orchestrator_provided_contract":true,"pre_edit_discovery":{"codegraph_queries":0,"codegraph_sync":0,"other_discovery_queries":0},"test_contract":{"targeted":{"module":"tests.test_p7_retained_r3_real_manifest_self_check","expected_tests":12,"invocations":1},"focused":{"modules":["tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_real_manifest_domain_template","tests.test_p7_retained_r3_real_manifest_self_check"],"expected_tests":53,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":822,"invocations":1},"postcommit_targeted":{"expected_tests":12,"invocations":1}},"implementation_commit":{"expected_parent_activation":true,"expected_subject":"fix(p7): align real manifest decoded sequences","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"execution_budgets":{"candidate_identity_reads":2,"source_apply_patch_writes":1,"test_apply_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"pre_edit_codegraph_queries":0,"pre_edit_codegraph_sync":0,"pre_edit_discovery_queries":0,"other_source_writes":0,"other_test_writes":0,"real_artifact_reads":0,"retained_artifact_reads":0,"c1_artifact_reads":0,"external_root_reads":0,"external_root_writes":0,"durable_log_writes":0,"filesystem_owner_additions":0,"process_runner_additions":0,"validator_additions":0,"validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R3-C1-R1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-C1-P3-FROZEN-SEQUENCE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"ACTIVE_SEQUENCE_BOUNDARY_CORRECTION","real_execution_status":"BLOCKED_ON_C1_ACCEPTANCE","synthetic_remainder_status":"BLOCKED","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record P3 sequence correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_TYPED_SEQUENCE_CORRECTION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0938-p7-retained-r3-b3-c3-c4-r3-c1-r1-targeted-sequence-review.md","bytes":4190,"sha256":"27fdee8093b132ac10681f27183e65c3179e468dabf94cebdafff6d8b3e5acb4"},"planner_stop":"B3_C3_C4_R3_C1_R1_C1_P3_FROZEN_SEQUENCE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与no-discovery gate

Activation必须是`27424dd...`direct child、subject/path set exact；commit后porcelain只能是machine row two untracked files，且before bytes/SHA exact。Orchestrator已提供line-level根因与本PLAN correction；pre-edit CodeGraph、sync、grep式发现、测试诊断均0。若局部patch无法满足合同，立即handoff，不得扩张范围。

## 2. One source patch

只一次`apply_patch`修改source，保持six exports/dataclass fields/P3-M1 imports与全部既有validation：

1. `_exact`在任一侧为JSON sequence时，要求双方container均属于exact `(tuple,list)`、length/order exact并递归；允许P3 frozen tuple与JSON-native list语义等价。Mapping仍exact key set；scalar仍concrete type exact，因此`1`不得等价`true`。
2. Manifest expected facts可保持JSON-native lists；decoded P3 tuples必须通过上述JSON sequence comparator与typed positions逐项匹配。不得让typed spec接受list替代冻结tuple字段。
3. Report先`canonical_json_bytes(payload)`，再P3 strict decode；comparison用同一JSON comparator。Exact re-encode必须调用`canonical_json_bytes(_json_native(decoded_report))`，不得把mappingproxy/tuple直接交给P3 encoder。
4. 保留五artifact/root/path/hash、C1/retained labels、commit/path collision、18 ordered Git ledger、blob OID/SHA/seam、diff-tree exact order、full ledger report与no-authority逻辑不变。

不得修改P3 encoder/decoder、添加generic serializer、filesystem/process/persistence/validator/eligibility surface。

## 3. One test patch

只一次`apply_patch`修改dedicated test，methods仍exact12：

- Golden/manifest测试必须用真实P3 canonical encode/decode形成frozen tuple，并断言其与JSON-native list通过subject comparator，同时继续验证scalar type strict。
- Test 09 data drift把修改后的`git_file_bytes`重新转为tuple，使执行到`seam_identity_mismatch`。
- Seam OID mismatch与Git key collision不得通过`run_real_manifest_self_check`被旧manifest前置拦截；改为直接调用public `required_real_manifest_git_argv`并断言各自stable `seam_identity_mismatch` / `git_file_set_collision`，且不创建runner/Git call。
- 其余targeted assertions保持原语义；不得把合法golden的expected code改成failure以掩盖production defect。

## 4. Fresh validation、commit与handoff

严格各一次顺序：targeted12 → focused53 → full822 → compileall exact source/test → CodeGraph sync1 + post-query1 → `git diff --check` + status exact-two → commit → postcommit targeted12。CodeGraph只能在full/compileall通过后运行。任一步失败立即停，后续0，retry/fallback0。

Commit parent必须是activation，subject `fix(p7): align real manifest decoded sequences`，paths exact two。Terminal前process scan1、owned0；ER tail read一次，以当前R1 handoff完整block为full-tail anchor，一次`apply_patch`追加physical EOF strict JSON，append后operations0。Executer不得commit ER或改plan files。

成功只证明subordinate typed owner implementation/test通过，不执行或授权real artifacts、validator、eligibility、release、synthetic、network/device，也不直接授予B3 credit；等待Planner验收。

维护性判断：correction仅调整JSON wire representation adapter与对应测试前置条件，复用单一comparator和既有owners，不增加抽象或权限。
