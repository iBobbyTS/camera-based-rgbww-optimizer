# P7 retained-R3 Option B：M1-S1-C1-C1 CodeGraph scope correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-CODEGRAPH-SCOPE-CORRECTION-V1`

**当前唯一动作：** Orchestrator先登记M1-S1-C1为pre-edit CodeGraph semantic-scope rejection并建立fresh exact activation；随后Executer先执行5个
逐文件逐symbol的pre-edit CodeGraph query并验证`5/5`、required coverage `24/24`，通过后只修改dedicated test中的原test07/test13 fixture/assertion，
执行完整冻结验证链与同样5组post-edit CodeGraph query，创建exact one-path correction commit，single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_S1_C1_C1_CODEGRAPH_SCOPE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2348-p7-retained-r3-b2-m1-s1-c1-codegraph-scope-failure-review.md`；bytes `7601`，SHA-256
`29bc017e9076257dd94ec9fdb8b61ce76246941dd93c1143069cd052864e1fe5`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_c1_c1_codegraph_scope_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-CODEGRAPH-SCOPE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"850537007233a1517962afbef26e8e40e4782ad2","expected_subject":"chore(plan): activate real manifest CodeGraph scope correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2348-p7-retained-r3-b2-m1-s1-c1-codegraph-scope-failure-review.md"],"clean_porcelain_required_after_activation":true},"rejected_execution":{"activation_commit":"0895921fc0a4d959b8d06ad218f70340e341197a","activation_parent":"5567837b1bbe3fdd368f0c8cbddd21c19a436e40","activation_subject":"chore(plan): activate real manifest fixture correction","evidence_commit":"850537007233a1517962afbef26e8e40e4782ad2","evidence_parent":"0895921fc0a4d959b8d06ad218f70340e341197a","first_failure":"pre_edit_codegraph_semantic_scope_mismatch","codegraph_sync_exit_zero":1,"codegraph_queries_exit_zero":1,"codegraph_query_groups_semantically_complete":0,"test_reads":0,"test_writes":0,"tests":0,"commits":0},"rejected_candidate":{"candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_parent":"84b3458765849f9c50515067788af365006cef68","candidate_tree":"ff424f29e6a7a95349500ce356669a754d9ffa14","candidate_consumable":false,"exact_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_blob":"84fcd755225af39eb89459146de282392367b70b","source_bytes":23352,"source_sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d","test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","test_bytes":17413,"test_sha256":"cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af"},"correction_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct real manifest domain fixtures","expected_changed_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-CODEGRAPH-SCOPE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_CODEGRAPH_SCOPE_CORRECTION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_real_manifest_candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","m1_real_manifest_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"correction_contract":{"test_methods_changed":["test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"],"production_writes":0,"test_method_additions":0,"test_method_removals":0,"collision_fixture":"copy_first_identity_and_replace_only_label_with_second_expected_label","collision_expected_code":"path_collision","authority_check":"ast_exact_import_and_callable_tokens","raw_source_substring_forbidden":true,"legal_package":"camera_based_rgbww_optimizer"},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query_groups":5,"pre_edit_required_coverage":24,"post_edit_sync":1,"post_edit_query_groups":5,"post_edit_required_coverage":24,"query_groups":[{"id":"m1_production","file":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","symbols":["RealManifestDomainTemplateSpec","RealManifestDomainTemplateBundle","build_real_manifest_domain_template"]},{"id":"m1_dedicated_test","file":"tests/test_p7_retained_r3_real_manifest_domain_template.py","symbols":["RealManifestDomainTemplateTests","test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"]},{"id":"p3_provenance_io","file":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","symbols":["read_existing_root","canonical_json_bytes","create_exclusive_root","persist_canonical_json","read_exact_file","run_read_only_git"]},{"id":"p4_conformance","file":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","symbols":["analyze_controller_source","_validate_existing_root_owner","validate_root_identity_chain","execute_controller_lifecycle"]},{"id":"p5_runtime","file":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py","symbols":["ControllerRuntimeRequest","compose_controller_source","execute_controller_runtime"]}],"sync_before_queries":true,"queries_before_test_read_or_edit":true,"wrong_route_retry":0,"fallback":0},"test_contract":{"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"execution_budgets":{"correction_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":10,"retry":0,"fallback":0},"zero_budgets":{"production_writes":0,"second_test_path_writes":0,"source_candidate_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"external_controller_reads":0,"external_controller_writes":0,"external_controller_processes":0,"external_root_reads":0,"external_root_creates":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2348-p7-retained-r3-b2-m1-s1-c1-codegraph-scope-failure-review.md","bytes":7601,"sha256":"29bc017e9076257dd94ec9fdb8b61ce76246941dd93c1143069cd052864e1fe5"},"planner_stop":"B2_M1_S1_C1_C1_CODEGRAPH_SCOPE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation and immutable gates

本包不得复用失败activation `0895921fc0a4d959b8d06ad218f70340e341197a`。Executer开始前必须证明当前activation是evidence HEAD
`850537007233a1517962afbef26e8e40e4782ad2`的direct child，subject exact
`chore(plan): activate real manifest CodeGraph scope correction`，changed paths exact为FULL、PLAN与本轮archive；porcelain clean，PLAN/FULL machine rows
均strict JSON且required FULL subset exact。

同时验证machine row中的failed activation/evidence topology、rejected candidate two-path topology与source/test blob/bytes/SHA-256、上一archive identity及本archive
identity。任一不符须在CodeGraph、test read/edit、tests或commit前single ER handoff并停止。

Candidate `cddd23e...`继续`consumable=false`。本包通过也只产生waiting-review correction candidate；Executer不得自称owner accepted或进入M1-I1。

## 2. Deterministic pre/post CodeGraph contract

Activation gate后、读取或编辑dedicated test source前，执行exact一次`codegraph sync`，随后按下列顺序各执行exact一次query：

1. `codegraph explore "File src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py. Return current line-numbered verbatim source and call paths for RealManifestDomainTemplateSpec, RealManifestDomainTemplateBundle, build_real_manifest_domain_template."`
2. `codegraph explore "File tests/test_p7_retained_r3_real_manifest_domain_template.py. Return current line-numbered verbatim source for RealManifestDomainTemplateTests.test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes and RealManifestDomainTemplateTests.test_13_generated_compile_fake_success_failure_and_negative_authority_surface."`
3. `codegraph explore "File src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py. Return current line-numbered verbatim source and call paths for read_existing_root, canonical_json_bytes, create_exclusive_root, persist_canonical_json, read_exact_file, run_read_only_git."`
4. `codegraph explore "File src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py. Return current line-numbered verbatim source and call paths for analyze_controller_source, _validate_existing_root_owner, validate_root_identity_chain, execute_controller_lifecycle."`
5. `codegraph explore "File src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py. Return current line-numbered verbatim source and call paths for ControllerRuntimeRequest, compose_controller_source, execute_controller_runtime."`

每个query必须exit0，并在自身stdout实际回显其exact repo-relative file path及每个required symbol。逐项coverage为5 file paths + 19 symbols = exact`24/24`；
query groups exact`5/5`。额外相关call-path source可存在，但旧synthetic test、同名相邻文件或summary不能替代required回显。任一missing/stale/wrong-route均立即以
`pre_edit_codegraph_semantic_scope_mismatch`停止；不得发第6个query、修改query后重试、fallback到grep/raw source，也不得读取/编辑test或运行tests。

Pre-edit `5/5`与`24/24`通过后，必须从回显source确认：production builder仍为frozen candidate；test07仅有collision fixture root mismatch；test13仅有
raw substring assertion；P3/P4/P5仍为唯一existing-root/I-O、static provenance/root-chain/lifecycle、runtime composition owners。若出现production finding，
write0并停Planner，不得扩大本包。

完成test edit与targeted/focused/compileall/full后，再exact一次`codegraph sync`并按同一顺序执行同5条命令，仍要求groups`5/5`、coverage`24/24`、
retry/fallback0。Post-edit回显必须证明production source/blob不变、test-only blast radius、P3/P4/P5单一owner、无second analyzer/classifier/serializer/lifecycle或
generic path authority。

## 3. Unchanged exact one-path semantic correction

唯一write path是`tests/test_p7_retained_r3_real_manifest_domain_template.py`。只允许修改以下两个既有test methods；production、新imports（除test13 AST断言
必要的stdlib test import）、其余11 methods、fake runtime和所有其他paths冻结，test methods保持exact13。

### 3.1 test07 collision fixture

构造collision时复制第一条C1完整identity，仅把`label`替换为第二条expected label，语义exact为
`replace(first, label=second.label)`。这样label/order、absolute/direct-child path、root/device/inode/mode与hash保持有效，两条path exact相同，断言stable code
`path_collision`。不得只替换第二identity的`path`，不得改production validation order。

### 3.2 test13 authority-negative assertion

删除对完整generated source的裸substring all/none判断。Strict UTF-8 decode后`ast.parse`，收集`ast.Import`/`ast.ImportFrom` exact qualified module和aliases，
以及`ast.Call`的exact `Name.id`/`Attribute.attr` tokens。Import modules只允许既有`sys`、P4 conformance module与P3 provenance-I/O module；
authority symbols `canonical_validator`、`emit_eligibility`、`consume_release`、`device_authorized`、`camera`、`ray120c`以及forbidden modules
`socket`、`requests`必须与exact tokens/qualified names不相交。合法package `camera_based_rgbww_optimizer`不能因包含字符序列`camera`而失败。不得删除negative
coverage或改generated production source迎合test。

## 4. Frozen validation and commit chain

严格顺序、每项exact一次；任一nonzero/count/shape mismatch立即停止，后项保持0：

1. targeted：machine row command，exact`13/13`、`OK`；
2. focused：machine row command，exact`83/83`、`OK`；
3. compileall：machine row command，exit0；
4. full discovery：machine row command，exact`800/800`、唯一`OK`；
5. post-edit CodeGraph sync一次 + 固定queries五次，exact`5/5`与coverage`24/24`；
6. 验证source candidate frozen blob/hash、test methods13、test07/test13 exact semantics、unstaged diff exact one test path、`git diff --check` clean；
7. stage exact one test path，创建唯一commit，subject exact `fix(p7): correct real manifest domain fixtures`，parent exact current activation；冻结after blob/bytes/SHA与
   canonical binary patch SHA；
8. postcommit targeted exact`13/13`、`OK`，验证commit subject/parent/path与porcelain clean。

总tests `4`、compileall `1`、CodeGraph sync `2`、queries `10`、commit `1`、retry/fallback `0/0`。不得运行pytest、formatter、ad-hoc test、
additional search/query、第二edit round、第二commit、amend或rebase。

## 5. ER handoff, failure branches, and hard locks

无论通过或失败，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append。记录activation/candidate/evidence/archive identities、每个CodeGraph query的command/exit/
required path-symbol coverage、exact test diff、两项fixture结果、四次tests/compileall、production source unchanged identity、correction commit、ER immutable prefix、
first failure及全部zero budgets。Executer不得修改PLAN/FULL/archive/debug/GUIDE/RESEARCH。

- Activation/topology/pre-CodeGraph失败：test read/edit0、tests0、commit0，single ER后停止；
- Pre-edit任一query不满足exit/path/symbol coverage：剩余query只按固定顺序执行到first failure即停，test read/edit0、tests0、commit0；不得补query；
- Edit或targeted/focused/compileall/full/post-CodeGraph/precommit失败：保留one-path diff，不修第二次、不commit、不继续后项；
- Commit后posttarget/topology失败：保留commit为non-consumable evidence，不amend/rebase；
- 全绿：只报告`M1-S1-C1-C1 correction candidate waiting independent Planner review`，不得进入M1-I1或real B2。

本包pure-offline，不命中Human高危授权，也不需要Advisor。Real C1/retained physical reads、external controller/root/process、synthetic integration、Git provenance
replay、real B2、subordinate manifest physical writes、canonical validator/callback/eligibility、retained audit/release、network/DNS/`.env`/credentials、device/camera/
Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：本包仅把模糊单query改成5个按owner/file分组的确定性证据门，并保持原one-path test纠偏完全不变；production职责、复杂度和test inventory不变，
无需架构重构。
