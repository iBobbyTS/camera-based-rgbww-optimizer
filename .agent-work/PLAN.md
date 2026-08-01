# P7 retained-R3 Option B：M1-S1-C1-C1-C1 evidence-owner correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-EVIDENCE-OWNER-CORRECTION-V1`

**当前唯一动作：** Orchestrator先把M1-S1-C1-C1登记为dedicated-test CodeGraph wrong-route rejection并建立fresh exact activation；Executer随后仅用一条production-only CodeGraph query验证P3/P4/P5/M1 call graph与ownership，用Git blob、exact one-path diff、Python AST/static gates及targeted/focused/full证明dedicated test；只修改原test07/test13，创建exact one-path correction commit并single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_S1_C1_C1_C1_EVIDENCE_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0000-p7-retained-r3-b2-m1-s1-c1-c1-codegraph-routing-review.md`；bytes `8412`，SHA-256
`3b4ecd888ca81a38acede732e9396e7c1744828513c05e39522f39bb190bd047`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_c1_c1_c1_evidence_owner_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-EVIDENCE-OWNER-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"af29d6f0e29fc0b5bdc8e8ff084ae9706d28aafa","expected_subject":"chore(plan): activate real manifest evidence owner correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0000-p7-retained-r3-b2-m1-s1-c1-c1-codegraph-routing-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation_commit":"becc092a028d6607c1dedb7c544a9d032dcf97a3","activation_parent":"850537007233a1517962afbef26e8e40e4782ad2","activation_subject":"chore(plan): activate real manifest CodeGraph scope correction","evidence_commit":"af29d6f0e29fc0b5bdc8e8ff084ae9706d28aafa","evidence_parent":"becc092a028d6607c1dedb7c544a9d032dcf97a3","evidence_er_blob":"643e91e13ebd71cdeec91aba368f580c68de2568","evidence_er_bytes":1185329,"evidence_er_sha256":"60fbfb97f8c859d5c6d6c1c30cebf3d0fb1e0482edbfb0069b9a01d207725b84","first_failure":"pre_edit_codegraph_semantic_scope_mismatch","codegraph_sync":1,"codegraph_queries":2,"production_group_coverage":"4/4","dedicated_test_group_coverage":"0/4","later_query_groups":0,"test_reads_outside_codegraph":0,"test_writes":0,"tests":0,"commits":0},"rejected_candidate":{"candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_parent":"84b3458765849f9c50515067788af365006cef68","candidate_tree":"ff424f29e6a7a95349500ce356669a754d9ffa14","candidate_consumable":false,"exact_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_blob":"84fcd755225af39eb89459146de282392367b70b","source_bytes":23352,"source_sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d","test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","test_bytes":17413,"test_sha256":"cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af"},"correction_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct real manifest domain fixtures","expected_changed_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-EVIDENCE-OWNER-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_EVIDENCE_OWNER_CORRECTION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_real_manifest_candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","m1_real_manifest_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"correction_contract":{"test_methods_changed":["test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"],"production_writes":0,"test_method_additions":0,"test_method_removals":0,"collision_fixture":"copy_first_identity_and_replace_only_label_with_second_expected_label","collision_expected_code":"path_collision","authority_check":"ast_exact_import_and_callable_tokens","raw_source_substring_forbidden":true,"legal_package":"camera_based_rgbww_optimizer"},"production_identity_contract":{"m1":{"blob":"84fcd755225af39eb89459146de282392367b70b","bytes":23352,"sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d"},"p3":{"blob":"d6d6cc628861baf8a95a09f13fa9204989693b5b","bytes":19767,"sha256":"118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d"},"p4":{"blob":"07f89d15c8288e0d45c495d6d5737bc37427b769","bytes":30424,"sha256":"008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee"},"p5":{"blob":"075face6fd7453236affa303640b91eb16a42a9b","bytes":12320,"sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2"}},"evidence_owner_contract":{"codegraph_scope":"production_p3_p4_p5_m1_call_graph_and_ownership_only","pre_edit_sync":1,"pre_edit_queries":1,"post_edit_sync":1,"post_edit_queries":1,"production_files_required":4,"production_ownership_boundaries_required":4,"dedicated_test_codegraph_queries":0,"finer_codegraph_queries":0,"generic_scanner":0,"git_ast_static_gates":2,"current_test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","current_test_methods":13,"one_path_diff_required":true,"wrong_route_retry":0,"fallback":0},"test_contract":{"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"execution_budgets":{"correction_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"git_ast_static_gates":2,"retry":0,"fallback":0},"zero_budgets":{"production_writes":0,"second_test_path_writes":0,"source_candidate_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"dedicated_test_codegraph_queries":0,"finer_codegraph_queries":0,"generic_scanner":0,"external_controller_reads":0,"external_controller_writes":0,"external_controller_processes":0,"external_root_reads":0,"external_root_creates":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0000-p7-retained-r3-b2-m1-s1-c1-c1-codegraph-routing-review.md","bytes":8412,"sha256":"3b4ecd888ca81a38acede732e9396e7c1744828513c05e39522f39bb190bd047"},"planner_stop":"B2_M1_S1_C1_C1_C1_EVIDENCE_OWNER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation and immutable gates

本包不得复用activation `becc092a028d6607c1dedb7c544a9d032dcf97a3`。Executer开始前必须证明当前activation是evidence HEAD
`af29d6f0e29fc0b5bdc8e8ff084ae9706d28aafa`的direct child，subject exact
`chore(plan): activate real manifest evidence owner correction`，changed paths exact为FULL、PLAN与本轮archive；porcelain clean，PLAN/FULL machine rows strict JSON且required FULL subset exact。

同时验证rejected activation/evidence direct-child topology、ER authoritative blob/bytes/SHA-256、rejected candidate two-path topology、本archive identity及所有earlier archive不变。Handoff中被截断的ER SHA不得被当作authoritative identity；以commit `af29d6f...`中的exact bytes `1185329`与SHA-256 `60fb...25b84`为准。

Candidate `cddd23e...`继续`consumable=false`。本包通过也只产生waiting-review one-path correction candidate；Executer不得自称owner accepted或进入M1-I1。

## 2. Reallocated evidence ownership

连续两个package已证明CodeGraph不能可靠返回dedicated-test source。本包禁止再查询dedicated test，禁止增加更细或更多query，禁止generic scanner、grep fallback或query修改重试。

### 2.1 Git/blob and pre-edit Python AST gate

Activation gate后，先验证machine row冻结的M1/P3/P4/P5 production blob/bytes/SHA-256和dedicated test current blob/bytes/SHA-256 exact。随后用一次read-only Python AST/static gate读取current Git worktree中的dedicated test，并至少证明：

1. UTF-8 strict decode与`ast.parse`成功；`RealManifestDomainTemplateTests`中`test_*` methods exact `13`，method names无增删；
2. test07现有collision assignment把第二identity作为`replace`第一参数、仅替换`path`为第一identity path，且随后期待`path_collision`；这正是待修正的known fixture shape；
3. test13现有negative assertion把exact forbidden tuple与`lowered = source.decode().lower()`、`all(name not in lowered ...)`绑定；这正是待移除的raw-substring shape；
4. 除test07/test13外其余11 methods的AST dump/hash记录为冻结before identity。

该gate只拥有test source identity/shape，不推断production correctness。Mismatch必须在edit/tests前停止；不得修改gate、重试或fallback。

### 2.2 One production-only CodeGraph query

Pre-edit static gate通过后，执行exact一次`codegraph sync`，再执行exact一次production-only query：

`codegraph explore "Trace the production-only call graph and ownership from build_real_manifest_domain_template through compose_controller_source and analyze_controller_source to read_existing_root, create_exclusive_root, read_exact_file, run_read_only_git, persist_canonical_json, validate_root_identity_chain, and execute_controller_lifecycle. Cover only the current production files p7_retained_r3_real_manifest_domain_template.py, p7_retained_r3_controller_runtime.py, p7_retained_r3_controller_conformance.py, and p7_retained_r3_provenance_io.py; explain the single P3 physical provenance-I/O, P4 static/effect provenance and lifecycle validation, P5 runtime composition, and M1 immutable template composition boundaries. Do not inspect tests."`

Query必须exit0，并实际覆盖四个production files与四个ownership boundaries。额外production call-path source可存在；test source不要求也不计数。任一production file/boundary缺失、wrong-route或stale立即以`pre_edit_codegraph_production_ownership_mismatch`停止；不得发第二条query、修改query、追加symbol query或使用generic scanner。

CodeGraph与Git/AST各自只在其owner范围内出结论：CodeGraph不得否决仅因未回显test；Git/AST不得取代production call-graph evidence。若production-only query发现真实production defect，write0并停Planner，不得扩大本包。

## 3. Exact one-path semantic correction

唯一write path是`tests/test_p7_retained_r3_real_manifest_domain_template.py`。只允许修改以下两个既有methods；production、imports（现有`ast`已足够）、其余11 methods、fake runtime和所有其他paths冻结，methods保持exact13。

### 3.1 test07 collision fixture

构造collision时复制第一条C1完整identity，仅把`label`替换为第二条expected label，语义exact为
`replace(spec().c1_inputs[0], label=spec().c1_inputs[1].label)`。这样第二expected label、absolute/direct-child path、root/device/inode/mode与hash均有效，而两条path exact相同；继续断言stable code `path_collision`。不得仅替换第二identity的`path`，不得改production validation order。

### 3.2 test13 authority-negative assertion

Strict UTF-8 decode generated source并`ast.parse`；从generated tree收集：

- `ast.Import`与`ast.ImportFrom`的exact qualified modules及alias names；
- `ast.Call`中exact `ast.Name.id`与`ast.Attribute.attr` callable tokens。

Import modules/aliases只允许generated source既有的`sys`、P4 conformance module与P3 provenance-I/O module及其既有imported symbols。Authority symbols `canonical_validator`、`emit_eligibility`、`consume_release`、`device_authorized`、`camera`、`ray120c`与forbidden modules `socket`、`requests`必须同exact qualified names/aliases/call tokens不相交。合法package `camera_based_rgbww_optimizer`不能因包含字符序列`camera`而失败。删除完整generated source的`lowered` substring all/none判断，不得删除negative coverage或改generated production source迎合test。

## 4. Post-edit static gate and frozen validation chain

Edit后立即执行一次read-only Python AST/static gate，并同时验证exact one-path unstaged diff：

1. production four identities与before exact相同；dedicated test methods仍exact13，其他11 methods AST dump/hash与before exact相同；
2. test07 exact使用first identity + only second label，保持`path_collision` assertion；
3. test13 exact使用generated AST qualified import/alias/call tokens，不存在`lowered` raw-source negative或`all(name not in lowered...)`；
4. worktree diff exact one test path，修改只落在test07/test13；`git diff --check` clean。

任一不符立即停止，tests/commit保持0。通过后严格顺序、每项exact一次；任一nonzero/count/shape mismatch立即停止，后项保持0：

1. targeted：machine row command，exact`13/13`、`OK`；
2. focused：machine row command，exact`83/83`、`OK`；
3. compileall：machine row command，exit0；
4. full discovery：machine row command，exact`800/800`、唯一`OK`；
5. post-edit `codegraph sync` exact一次，随后重发第2.2节同一production-only query exact一次；仍须四个production files与四个ownership boundaries完整，test source不要求；
6. 再验证production identities frozen、test-only blast radius、one-path diff、two-method AST semantics与`git diff --check`；
7. stage exact one test path；staged diff exact；创建single commit，subject exact `fix(p7): correct real manifest domain fixtures`；
8. commit必须direct child of current activation，changed path exact one test path，porcelain clean；记录tree、test after blob/bytes/SHA-256与canonical binary patch SHA-256；
9. postcommit targeted exact一次，exact`13/13`、`OK`；
10. append `.agent-work/EXECUTION_RESULT.md` exact一次并停止；该append不得并入implementation commit。

总预算：tests `4`、compileall `1`、CodeGraph sync/query `2/2`、Git/AST static gates `2`、correction commit `1`、ER append `1`、retry/fallback `0/0`。

## 5. ER handoff and hard locks

ER必须记录activation/evidence/candidate topology、before/after identities、pre/post AST findings、production-only CodeGraph四文件/四boundary coverage、完整validation ledger、implementation commit topology、ER immutable-prefix identity、所有zero budgets、first failure或success stop。若CodeGraph输出包含unrequested test内容，只能视作额外噪声，不得作为dedicated-test evidence。

持续硬锁：production与second test path writes；source/P3/P4/P5/P7 edits；dedicated-test CodeGraph query；finer/additional CodeGraph query；generic scanner；external controller/root/process；synthetic integration；accepted-C1/retained physical reads；Git provenance replay；real B2；subordinate manifest physical writes；canonical validator/callback/eligibility；retained audit；release generation/qualification/copy/consumption；network/DNS/environment/credentials；device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment；PLAN/FULL/archive/debug/GUIDE/RESEARCH writes by Executer。所有预算exact0。

这是一项纯离线、单test-path纠偏，不需要Human或Advisor授权，预计少于10分钟，不使用visible Terminal。Executer成功或失败均停在唯一Planner stop，不得进入M1-I1或任何later stage。

维护性边界：P3仍唯一拥有physical provenance I/O，P4仍唯一拥有static/effect provenance与lifecycle validation，P5仍唯一拥有runtime composition，M1仍是immutable domain-template composition；本包只重分配验证证据owner并修正两个既有test fixtures，不引入新helper、scanner或生产抽象。
