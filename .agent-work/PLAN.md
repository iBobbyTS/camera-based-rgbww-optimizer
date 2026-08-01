# P7 retained-R3 Option B：M1-S1-C1-C1-C1-C1-C1 CodeGraph-free exact-diff correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-CODEGRAPH-FREE-EXACT-DIFF-CORRECTION-V1`

**当前唯一动作：** Orchestrator先把M1-S1-C1-C1-C1-C1登记为CodeGraph wrong-route rejection并建立fresh activation；Executer随后仅依赖冻结Git object identities读取既有test07/test13，完成exact one-path fixture correction，按顺序运行既有tests，并在测试全绿后仅运行一次无query、非语义门的`codegraph sync`，形成单一候选提交和ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_S1_C1_C1_C1_C1_C1_CODEGRAPH_FREE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0026-p7-retained-r3-b2-m1-s1-c1-c1-c1-c1-codegraph-routing-review.md`；bytes `9878`，SHA-256
`06447d6c7847e5f8ffabba19212be96ac06cd3723ab4c644b2d274fc8ed100f2`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_c1_c1_c1_c1_c1_codegraph_free_exact_diff_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-CODEGRAPH-FREE-EXACT-DIFF-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"540568c84d266c115f2a4fcdf9078fccc4956279","expected_subject":"chore(plan): activate real manifest CodeGraph-free correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0026-p7-retained-r3-b2-m1-s1-c1-c1-c1-c1-codegraph-routing-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation_commit":"3c46c3531766576d9f6d7172d12add911f934537","activation_parent":"aae2e5c8d1c87f0f12955d049b7c3c581774680c","activation_subject":"chore(plan): activate real manifest exact diff correction","evidence_commit":"540568c84d266c115f2a4fcdf9078fccc4956279","evidence_parent":"3c46c3531766576d9f6d7172d12add911f934537","evidence_subject":"chore(evidence): record production CodeGraph routing stop","evidence_er_blob":"ea2e26ac24649e284c6e76bc01ebc64a3cc29b57","evidence_er_bytes":1195508,"evidence_er_sha256":"da00b05efcf259f717efdd5a5f9dcdf0df23a0250349da92c9a0ae77940e7966","first_failure":"pre_edit_codegraph_production_ownership_mismatch","pre_edit_codegraph_sync":1,"pre_edit_codegraph_queries":1,"authoritative_production_file_coverage":"2/4","post_edit_codegraph_sync":0,"post_edit_codegraph_queries":0,"test_writes":0,"tests":0,"commits":0,"retry":0},"rejected_candidate":{"candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_parent":"84b3458765849f9c50515067788af365006cef68","candidate_tree":"ff424f29e6a7a95349500ce356669a754d9ffa14","candidate_consumable":false,"exact_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_blob":"84fcd755225af39eb89459146de282392367b70b","source_bytes":23352,"source_sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d","test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","test_bytes":17413,"test_sha256":"cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af"},"correction_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct real manifest domain fixtures","expected_changed_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-CODEGRAPH-FREE-EXACT-DIFF-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_CODEGRAPH_FREE_EXACT_DIFF_CORRECTION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_real_manifest_candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","m1_real_manifest_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"correction_contract":{"test_methods_changed":["test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"],"production_writes":0,"test_method_additions":0,"test_method_removals":0,"collision_fixture":"copy_first_identity_and_replace_only_label_with_second_expected_label","collision_expected_code":"path_collision","authority_check":"existing_test_runtime_ast_exact_import_alias_and_callable_tokens","raw_source_substring_forbidden":true,"legal_package":"camera_based_rgbww_optimizer"},"production_identity_contract":{"m1":{"blob":"84fcd755225af39eb89459146de282392367b70b","bytes":23352,"sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d"},"p3":{"blob":"d6d6cc628861baf8a95a09f13fa9204989693b5b","bytes":19767,"sha256":"118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d"},"p4":{"blob":"07f89d15c8288e0d45c495d6d5737bc37427b769","bytes":30424,"sha256":"008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee"},"p5":{"blob":"075face6fd7453236affa303640b91eb16a42a9b","bytes":12320,"sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2"}},"evidence_owner_contract":{"before_identities_owner":"frozen_git_blob_bytes_sha256_only","after_test_semantics_owners":["exact_diff_limited_to_test07_test13","existing_dedicated_runtime_assertions","targeted_focused_full_tests","postcommit_blob_and_canonical_patch_sha256","planner_independent_committed_diff_review"],"codegraph_role":"post_test_sync_only_nonsemantic","post_test_sync":1,"ad_hoc_ast_static_gates":0,"evidence_helpers":0,"generic_scanner":0,"current_test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","one_path_diff_required":true,"wrong_route_retry":0,"fallback":0},"test_contract":{"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"execution_budgets":{"correction_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"ad_hoc_ast_static_gates":0,"evidence_helpers":0,"retry":0,"fallback":0},"zero_budgets":{"production_writes":0,"second_test_path_writes":0,"source_candidate_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"ad_hoc_ast_static_gates":0,"evidence_helpers":0,"generic_scanner":0,"external_controller_reads":0,"external_controller_writes":0,"external_controller_processes":0,"external_root_reads":0,"external_root_creates":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0026-p7-retained-r3-b2-m1-s1-c1-c1-c1-c1-codegraph-routing-review.md","bytes":9878,"sha256":"06447d6c7847e5f8ffabba19212be96ac06cd3723ab4c644b2d274fc8ed100f2"},"planner_stop":"B2_M1_S1_C1_C1_C1_C1_C1_CODEGRAPH_FREE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation and immutable Git gates

本包不得复用activation `3c46c3531766576d9f6d7172d12add911f934537`。Executer开始前必须证明当前activation是evidence HEAD
`540568c84d266c115f2a4fcdf9078fccc4956279`的direct child，subject exact
`chore(plan): activate real manifest CodeGraph-free correction`，changed paths exact为FULL、PLAN与本轮archive；porcelain clean，PLAN/FULL machine rows strict JSON且required FULL subset exact。

同时验证reviewed activation/evidence direct-child topology、ER authoritative blob/bytes/SHA-256、rejected candidate topology、本archive identity及所有earlier archives不变。Candidate `cddd23e...`继续`consumable=false`。本包通过也只产生waiting-review one-path correction candidate；Executer不得自称owner accepted或进入M1-I1。

在任何source read或edit前，仅用Git object命令验证以下identity exact：

| Owner | Path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| M1 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| P3 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `d6d6cc628861baf8a95a09f13fa9204989693b5b` | `19767` | `118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d` |
| P4 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py` | `07f89d15c8288e0d45c495d6d5737bc37427b769` | `30424` | `008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee` |
| P5 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py` | `075face6fd7453236affa303640b91eb16a42a9b` | `12320` | `07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2` |
| dedicated test | `tests/test_p7_retained_r3_real_manifest_domain_template.py` | `05db407f9fd6c67bf359f1874cff2f9baaf9564f` | `17413` | `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af` |

这些冻结Git blob/bytes/SHA-256是全部pre-edit identity owner。禁止CodeGraph explore/query、coverage assertion、inline AST/static gate、helper、scanner、source-shape程序或generic search fallback。Identity mismatch必须write0/tests0停止。

## 2. Direct exact one-path semantic correction

Identity gate通过后，Executer可直接读取以下两个既有methods并实施correction；无需先用额外程序重新证明旧syntax。唯一write path是
`tests/test_p7_retained_r3_real_manifest_domain_template.py`。只允许修改：

- `test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes`
- `test_13_generated_compile_fake_success_failure_and_negative_authority_surface`

Production、imports（现有`ast`足够）、其余11 methods、fake runtime和所有其他paths冻结；不得新增或删除test method、helper、scanner或production abstraction。

### 2.1 test07 collision fixture

构造collision时复制第一条C1完整identity，仅把`label`替换为第二条expected label，语义exact为：

`replace(spec().c1_inputs[0], label=spec().c1_inputs[1].label)`

这样第二expected label、absolute/direct-child path、root/device/inode/mode与hash均有效，而两条path exact相同；继续断言stable code `path_collision`。不得仅替换第二identity的`path`，不得改production validation order。

### 2.2 test13 authority-negative assertion

在test13既有runtime assertion中strict UTF-8 decode generated source并`ast.parse`；从generated tree收集：

- `ast.Import`与`ast.ImportFrom`的exact qualified modules及alias names；
- `ast.Call`中exact `ast.Name.id`与`ast.Attribute.attr` callable tokens。

Import modules/aliases只允许generated source既有的`sys`、P4 conformance module与P3 provenance-I/O module及其既有imported symbols。Authority symbols `canonical_validator`、`emit_eligibility`、`consume_release`、`device_authorized`、`camera`、`ray120c`与forbidden modules `socket`、`requests`必须同exact qualified names/aliases/call tokens不相交。合法package `camera_based_rgbww_optimizer`不能因包含字符序列`camera`而失败。删除完整generated source的`lowered` substring all/none判断，不得删除negative coverage或改generated production source迎合test。

这里的AST仅是existing dedicated test的runtime assertion，不是额外static invocation、evidence helper或pre-edit gate。

## 3. Exact diff, ordered tests, and maintenance sync

Edit后先以Git原生diff保留并人工检查完整diff：worktree diff exact one dedicated-test path，only changed methods为test07/test13，production identities与before exact相同，`git diff --check` clean。不得通过新脚本/helper/AST gate/scanner判定diff；若可读Git diff出现第三method、import、helper或其他path，立即停止，tests保持0。

通过后严格顺序、每项exact一次；任一nonzero/count/shape mismatch立即停止，后项保持0：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template`，exact `13/13`、`OK`；
2. focused：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template`，exact `83/83`、`OK`；
3. compileall：`.venv/bin/python -m compileall -q src tests`，exit `0`；
4. full discovery：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，exact `800/800`、唯一`OK`；
5. 仅在上述一path edit与ordered validation全通过后运行`codegraph sync` exact一次，要求exit `0`；禁止`codegraph explore`或任何query。该sync仅满足changed-project maintenance rule，不证明语义、call graph、文件覆盖或owner boundary；nonzero仍须precommit stop，retry `0`；
6. 再检查完整Git diff exact one test path/only test07+test13、production identities frozen及`git diff --check`；不得运行替代AST/helper/scanner；
7. stage exact one test path，检查staged diff与unstaged empty；创建single commit，subject exact `fix(p7): correct real manifest domain fixtures`；
8. commit必须direct child of current activation，changed path exact one test path，porcelain clean；记录tree、test after blob/bytes/SHA-256，以及由`git diff --binary <activation> <commit> -- tests/test_p7_retained_r3_real_manifest_domain_template.py` exact bytes计算的canonical patch SHA-256；
9. postcommit targeted exact一次，exact `13/13`、`OK`；
10. append `.agent-work/EXECUTION_RESULT.md` exact一次并停止；该append不得并入implementation commit。

总预算：tests `4`、compileall `1`、CodeGraph maintenance sync `1`、ad-hoc AST/static gates `0`、evidence helpers/scanners `0`、correction commit `1`、ER append `1`、retry/fallback `0/0`。本包不存在CodeGraph explore/query阶段或coverage assertion。

## 4. ER handoff and hard locks

ER必须记录activation/evidence/candidate topology、before/after Git identities、exact unstaged/staged/committed diff scope、完整validation ledger、唯一post-test CodeGraph sync exit、implementation commit topology、canonical binary patch SHA-256、ER immutable-prefix identity、所有zero budgets、first failure或success stop。不得声称CodeGraph证明任何production semantic或owner boundary；不得记录任何CodeGraph query/coverage assertion。test13的AST只作为dedicated runtime test结果报告。

持续硬锁：production与second test path writes；source/P3/P4/P5/P7 edits；所有CodeGraph explore/query/semantic assertions；dedicated-test/finer/additional CodeGraph query；ad-hoc AST/static gate；evidence helper/scanner；generic search fallback；external controller/root/process；synthetic integration；accepted-C1/retained physical reads；Git provenance replay；real B2；subordinate manifest physical writes；canonical validator/callback/eligibility；retained audit；release generation/qualification/copy/consumption；network/DNS/environment/credentials；device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment；PLAN/FULL/archive/debug/GUIDE/RESEARCH writes by Executer。所有预算exact `0`。

这是一项纯离线、单test-path纠偏，不需要Human或Advisor授权，预计少于10分钟，不使用visible Terminal。Executer成功或失败均停在唯一Planner stop，不得进入M1-I1或任何later stage。

维护性边界：P3仍唯一拥有physical provenance I/O，P4仍唯一拥有static/effect provenance与lifecycle validation，P5仍唯一拥有runtime composition，M1仍是immutable domain-template composition；本包不新增证据框架，只修正两个既有test fixtures。CodeGraph仅保留项目索引同步职责，不参与此test-only correction的语义裁决。
