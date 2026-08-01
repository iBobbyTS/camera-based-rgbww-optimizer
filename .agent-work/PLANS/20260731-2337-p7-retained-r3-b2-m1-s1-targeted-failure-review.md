# P7 retained-R3 Option B：M1-S1 targeted failure review archive

**归档状态：** `REJECTED_TARGETED_TEST_FIXTURE_ASSERTION_FAILURE`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1`

**当前唯一动作：** Orchestrator先接受并登记composite P3/P4 existing-root owner，再建立fresh exact activation commit；随后Executer只新增一个
pure/deterministic/effect-free real-manifest-v2 controller template owner及其dedicated test，复用accepted P3/P4/P5 owners，完成冻结验证、exact
two-path implementation commit与single ER handoff，然后停止。

**唯一 Planner stop：**
`B2_M1_S1_REAL_MANIFEST_DOMAIN_TEMPLATE_SUCCESSOR_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2316-p7-retained-r3-b2-m1-c1-c1-c1-acceptance-review.md`；bytes `8890`，SHA-256
`160f00af69407ee6e70e161d0c79dea6efddbba8518aec349b3ce9d0ea5f4f78`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_real_manifest_domain_template_successor_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"4609d56709dbc8ac2c3046ada797e0faa16bf2ff","expected_subject":"chore(plan): activate real manifest domain successor","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2316-p7-retained-r3-b2-m1-c1-c1-c1-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_existing_root_owner":{"candidate_commit":"40d92acb77b32f370955d687c74c7ff7077f55e1","candidate_parent":"77c96d6eec4d1881a82a678c84165dff03d6fb6e","candidate_patch_sha256":"00eb408bb3fe4440a5589dacd9799247577ccd0c6dbc891c6ff693c5e9e5f683","correction_commit":"ffd1d9bb234c90a28ab497b10a35b08e4478eb1c","correction_parent":"51af8645e47fa87400a6a7456122ab097fb7ae67","correction_patch_sha256":"9f1b6e97aa05f9a10b001254206de7fe8356a8ef138e55bfd55f1d15ade99dfb","evidence_commit":"4609d56709dbc8ac2c3046ada797e0faa16bf2ff","consumable_for_this_package":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"feat(p7): own real manifest domain template","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_FRESH_SUCCESSOR_IMPLEMENTATION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_existing_root_candidate_commit":"40d92acb77b32f370955d687c74c7ff7077f55e1","m1_existing_root_correction_commit":"ffd1d9bb234c90a28ab497b10a35b08e4478eb1c","m1_existing_root_candidate_consumable":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"builder_contract":{"module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_real_manifest_domain_template","entrypoint":"build_real_manifest_domain_template","exports":["RealManifestDomainTemplateError","RealManifestGitPathIdentity","RealManifestCommitIdentity","RealManifestInputIdentity","RealManifestBaselineIdentity","RealManifestDomainTemplateSpec","RealManifestDomainTemplateBundle","build_real_manifest_domain_template"],"input_type":"RealManifestDomainTemplateSpec","output_type":"RealManifestDomainTemplateBundle","output_fields":["template_source","template_sha256","replacement_statement","replacement_sha256","runtime_request","expected_bound_results","expected_artifact_names","expected_lifecycle_order"],"frozen_dataclasses":true,"pure_in_memory":true,"assignment_name":"REAL_MANIFEST_CONTRACT","validation_function":"require_real_manifest_contract","runtime_request_type":"ControllerRuntimeRequest","generic_path_allowlist":false,"parallel_owner":false},"canonical_source_contract":{"strict_utf8":true,"ast_parse":true,"builtin_compile":true,"golden_template_and_replacement_sha256_literals_required":true,"schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","exact_artifact_names":["retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":5,"existing_root_acquisition_owner":"read_existing_root","existing_root_acquisition_calls":7,"single_output_root":true,"output_root_create_calls":1,"live_root_identities":8,"c1_input_labels":["path_owner_index","path_owner_index_seal","terminal_evidence","terminal_evidence_seal"],"retained_input_labels":["current_lineage_candidate","resolved_formal_plan","setup_lineage_release"],"c1_reads":4,"retained_reads":3,"input_reads_total":7,"controller_read_only_git_invocations":56,"git_success_field":"exit_code","runtime_returncode_uses":0,"persist_canonical_json_calls":5,"output_reload_reads":5,"read_exact_file_calls":12,"root_chain_file_count":5,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"retry":0,"fallback":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0},"validation_codes":["invalid_spec","reference_task_mismatch","contract_mismatch","commit_identity_invalid","git_path_identity_invalid","baseline_identity_invalid","input_identity_invalid","activation_identity_mismatch","c1_cardinality_mismatch","c1_label_mismatch","retained_cardinality_mismatch","retained_label_mismatch","path_collision","path_not_absolute","path_not_direct_child","byte_count_invalid","sha256_invalid","blob_oid_invalid","mode_invalid","source_path_invalid","output_root_invalid","repo_root_invalid","process_argv_mismatch","literal_type_invalid"],"test_contract":{"new_test_methods":13,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_baseline":787,"full_expected":800,"postcommit_targeted_expected":13},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query":1,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true,"query_before_source_test_read_or_edit":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"second_writer":0,"second_analyzer":0,"second_classifier":0,"second_serializer":0,"second_lifecycle":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2316-p7-retained-r3-b2-m1-c1-c1-c1-acceptance-review.md","bytes":8890,"sha256":"160f00af69407ee6e70e161d0c79dea6efddbba8518aec349b3ce9d0ea5f4f78"},"planner_stop":"B2_M1_S1_REAL_MANIFEST_DOMAIN_TEMPLATE_SUCCESSOR_WAITING_PLANNER_REVIEW"}`

## 1. Acceptance transition 与 fresh activation gate

上一包判定为`ACCEPTED_COMPLETE_COMPOSITE_EXISTING_ROOT_IDENTITY_OWNER_VALIDATED`。Candidate `40d92ac...`提供P3/P4
owner及regressions，correction `ffd1d9b...`只修合法wildcard negative source；evidence `4609d56...`只追加ER。本PLAN不会复用旧M1 activation
`535e5e1...`或旧gap evidence `195afbe...`，而要求Orchestrator先更新FULL为accepted owner + active fresh successor，再创建新activation。

Executer开始前必须验证activation是parent `4609d56709dbc8ac2c3046ada797e0faa16bf2ff`的direct child，subject exact
`chore(plan): activate real manifest domain successor`，changed paths exact FULL/PLAN/本acceptance archive三项，PLAN/FULL machine rows strict JSON、
required FULL subset exact、porcelain clean。还须验证accepted candidate/correction/evidence topology、subjects、patch SHA与当前P3/P4/P3-test/P4-test blob
identities匹配archive；任一不符须在source/test read/edit或CodeGraph前single ER handoff并停止。

本包只允许新增：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`；
2. `tests/test_p7_retained_r3_real_manifest_domain_template.py`。

两路径在activation必须absent。不得编辑existing P3/P4/P5/P7或任何其他path。Implementation须是activation direct child、exact two paths、single
commit、subject `feat(p7): own real manifest domain template`。Executer不得修改PLAN/FULL/archive。

## 2. Fresh CodeGraph 与 maintainability boundary

旧M1 pre-edit query发生在`read_existing_root` owner产生前，不能复用。本successor activation gate后、读取或编辑任何source/test前，必须exact一次
`codegraph sync`再exact一次精确query，覆盖：

- P3 `read_existing_root/canonical_json_bytes/create_exclusive_root/persist_canonical_json/read_exact_file/run_read_only_git`；
- P4 `analyze_controller_source/_validate_existing_root_owner/validate_root_identity_chain/execute_controller_lifecycle`；
- P5 `ControllerRuntimeRequest`与P7 builder pattern；
- 新module/test在pre-edit确实absent。

Query必须确认P3 direct no-follow existing-root acquisition与P4 exact direct-call provenance已经存在，并确认7个separate existing roots + one created output root可由
single P4 owner graph表达；若仍发现owner contract矛盾，source/test writes0并停Planner，不在M1内复制或放宽owner。

编辑及ordered tests完成后再exact一次sync/query，覆盖新builder、generated owner calls与P3/P4/P5 call graph，证明无second writer/analyzer/classifier/
serializer/lifecycle、无generic path owner、无production blast-radius。两组CodeGraph均必须exit0，不得warning/retry。

职责冻结：新module只拥有typed immutable spec、canonical controller template/replacement与runtime request composition；P3独占physical I/O/canonical
serialization，P4独占AST/effect provenance/root-chain/lifecycle，P5独占source persistence/process execution。不得复制这些实现或新增external one-off controller。

## 3. Public API、typed identities 与 fail-closed validation

`__all__`必须逐字节等于machine row八项exports。所有dataclass必须`frozen=True`，nested collections只能用tuple，builder不得mutate input。

- `RealManifestGitPathIdentity`字段exact：`repo_path,before_blob_oid,after_blob_oid,before_sha256,after_sha256,binary_patch_sha256`；
- `RealManifestCommitIdentity`字段exact：`commit,parent,subject,changed_paths,full_patch_sha256`；
- `RealManifestInputIdentity`字段exact：`label,path,byte_count,sha256,device,inode,mode,root_path,root_device,root_inode,root_mode`；
- `RealManifestBaselineIdentity`字段exact：`release_checkpoint,helper_v1,integration,helper_path,test_path,seam_chain,governance_manifest_sha256,guide_sha256,advisor_decision_sha256,advisor_attachment_sha256,human_governance_override,helper_disposition`；
- `RealManifestDomainTemplateSpec`字段exact：`reference_task_id,contract_id,activation,baseline,c1_inputs,retained_inputs,source_path,output_root,repo_root,process_argv`；
- `RealManifestDomainTemplateBundle`字段exact为machine row八项`output_fields`。

Spec必须要求fresh task/contract exact；activation/baseline/paths/hashes/blob OIDs/bytes/device/inode/modes/type exact并使用machine row稳定错误码。C1 tuple
exact4且labels/order exact；retained tuple exact3且labels/order exact。每组path必须absolute lexical-canonical direct child of its frozen root；七条input path、source与
output互不碰撞；file mode0600、root mode0700、bytes正数。Repo paths必须canonical relative并由typed identity逐项绑定，不接受generic allowlist。
`process_argv` exact `(repo_root + "/.venv/bin/python", "-")`。

## 4. Generated real-manifest controller contract

Builder只返回immutable bytes/hash/replacement/`ControllerRuntimeRequest`；builder本身filesystem/process/Git/external effects exact0。Template assignment
exact `REAL_MANIFEST_CONTRACT`且只出现一次，紧邻唯一`require_real_manifest_contract`调用；replacement为canonical Python literal，无physical NUL/CR/LF
escape drift。Dedicated test必须用literal golden SHA-256冻结template与replacement exact bytes，并strict UTF-8、AST parse、`compile()`及
`compose_controller_source()`重验。

Generated controller只能import/call accepted P3/P4 owner surface和Python builtins；不得import/call canonical validator、exact-five validator callback、
eligibility、release、network/device/science或P7 synthetic owner。每个七条input identity必须经direct canonical import/call
`read_existing_root(path)`各exact一次并direct bind，随后作为同一input的`read_exact_file(..., root=...)` live identity；不得constructor/alias/container/nested
transport。Output root仅由`create_exclusive_root`exact一次创建。P4应识别live root identities exact8、effect transport空。

Static AST inventory必须冻结：read-only Git owner calls56且只读`exit_code`，不得读`returncode`；input reads7（C1=4、retained=3）；output reload
reads5；`read_exact_file` total12；`persist_canonical_json`5；root-chain exact一次且包含5个output identities；lifecycle exact一次、order exact8、
retry/fallback0。Git56必须从typed baseline与activation identity构造exact command/expected-output checks，绑定full child/parent/subject/path set、before/after
blobs、canonical/full/per-path patches、helper-v1 disposition、release checkpoint与accepted seam chain；不得以generic path allowlist替代逐项identity。

Manifest payload冻结schema/status、baseline chain、C1 four、retained three与before/after physical identities。Real values只能来自future spec；本包不得读取real
C1或retained。Output root future runtime exact five direct regular0600 canonical compact sorted UTF-8 JSON+LF artifacts：manifest、manifest seal、terminal、
terminal seal、admission。每次persist后strict root-bound reload、duplicate/non-finite rejection与byte/hash equality；root before/after identity chain一致。
Manifest/seal一旦persist不可rewrite/repair/replace/relocate。Payload不得claim eligibility、release consumability、validator pass或device authorization。

任何conformance/activation/root/inputs/evaluate primary failure保持原exception identity dominant；只有existing P4 lifecycle可生成failure terminal/seal/admission，
terminal或seal failure阻止admission。不得fallback/retry/second root/process。

## 5. Dedicated regression contract

Dedicated file必须exact13个meaningful `unittest` methods，并冻结method names/inventory，至少逐项覆盖：

1. exact exports、dataclass fields/frozen/deep tuple；
2. deterministic build、exact template/replacement bytes与literal golden SHA；
3. runtime request、source/output/process binding及builder no-effect；
4. invalid spec/task/contract/type stable codes；
5. invalid commit/blob/SHA/path/bytes/mode/root identity stable codes；
6. activation/baseline chain exact typed binding、no generic allowlist；
7. C1 exact4 labels/order/direct-child/uniqueness/hash cardinality；
8. retained exact3 labels/order/direct-child/uniqueness/frozen hashes；
9. schema/status/exact5 artifact names及canonical payload/seal/terminal/admission；
10. accepted P3 existing-root direct acquisition exact7、created output exact1、Git56/`exit_code`/no`returncode` AST inventory；
11. P4 bound-result/live-root8/root-read/root-chain/effect-transport canonical inventory；
12. lifecycle exact order、primary-failure dominance、terminal/seal admission blocking、retry0；
13. no-I/O/no-authority negative surface，以及generated strict compile与fully fake success/failure runnable lifecycle。

Fake runnable tests只能inject in-memory/fake owners，不得create external root/process或读取real evidence。Assertions必须验证actual payload、calls、identity/hash与
exception dominance，不能只执行代码。

## 6. Exact validation、commit 与 ER evidence

Activation/topology/absence gate与fresh pre-edit CodeGraph通过后实现exact two paths，随后严格按下列顺序，每项exact一次；任一nonzero/count/shape mismatch立即停，
不得retry/fallback或继续后项：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template`，exact`13/13`、`OK`；
2. focused：machine row exact command，exact`83/83`、`OK`；
3. compileall：`.venv/bin/python -m compileall -q src tests`，exit0；
4. full discovery：machine row exact command，baseline787 + new13 = exact`800/800`、唯一`OK`；
5. post-edit CodeGraph sync/query exact`1/1`，随后API/AST/golden/diff/blob gate与`git diff --check`；unstaged diff exact two new paths；
6. stage exact two paths，创建唯一implementation commit，subject exact `feat(p7): own real manifest domain template`；冻结after blob/bytes/SHA及canonical
   binary patch SHA；
7. postcommit targeted exact`13/13`、`OK`，验证commit direct parent/subject/path与porcelain clean。

总test invocations4、compileall1、fresh CodeGraph sync/query`2/2`、implementation commit1、retry/fallback`0/0`。不得运行extra ad-hoc Python、pytest、
formatter、第二commit或测试纠偏。

无论通过/失败，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append。记录activation及accepted owner topology、pre/post CodeGraph、new-path
before-absent/after identity、public API/dataclass/golden/source AST/call inventory、四次test/compileall、commit topology、ER immutable prefix、first failure与全部
zero budgets。Executer不得修改PLAN/FULL/archive/debug/GUIDE/RESEARCH，不得自行接受或进入M1-I1。

## 7. Hard locks、failure branches 与授权

本包是pure-offline engineering implementation，不命中AGENTS高危授权，不需要Advisor或Human；但不授权任何设备或灯光操作。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`，canonical validator保持sole eligibility owner。

Real C1/retained physical reads、external controller/root/process、M1-I1 synthetic integration、Git provenance replay、real B2、physical subordinate manifest/seal
writes、canonical validator/callback、eligibility、retained audit、release generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device/camera/
Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。

- Activation/topology/absence/CodeGraph pre-gate失败：source/test writes0、tests0、commit0，single ER handoff后停Planner；
- Implementation或targeted/focused/compileall/full/post-CodeGraph/precommit失败：保留exact two-path diff，不跨界修复、不commit、不retry，single ER handoff后停；
- Commit后posttarget/topology失败：保留commit为non-consumable evidence，不amend/rebase，single ER handoff后停；
- 全绿：只报告M1-S1 candidate waiting independent Planner review；不得称retained eligible或解锁M1-I1。

维护性判断：本包只新增一个typed pure domain-composition owner和dedicated tests；P3/P4/P5仍分别独占I/O、static provenance/lifecycle与runtime。复杂度集中于
immutable spec/template合同，13项回归与pre/post CodeGraph覆盖边界，当前无需另行架构重构。

## 8. Planner 独立审核结论（2026-07-31）

### 审核范围与方法

Planner只读审核active PLAN、`.agent-work/EXECUTION_RESULT.md`、activation `84b3458765849f9c50515067788af365006cef68`、候选
`cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf`及evidence HEAD `5567837b1bbe3fdd368f0c8cbddd21c19a436e40`。候选是activation的direct
child，tree `ff424f29e6a7a95349500ce356669a754d9ffa14`，changed paths exact为新module与dedicated test，canonical binary patch SHA-256
`2d4a1d3b...`按Orchestrator冻结事实保留；evidence是候选的direct child且只修改ER。Planner未重跑测试或CodeGraph，也未读取real/retained evidence。

### Validation quality 与 findings

唯一targeted invocation返回`Ran 13 tests`、`11 pass / 2 fail`，随后所有later gates均按PLAN保持0。两项失败均只建立test finding：

1. `test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes`只把第二条identity的`path`换成第一条path，却保留第二条`root_path`，因此production
   builder按合同先返回`path_not_direct_child`；这不能证明`path_collision`分支错误。纠偏须让第二条fixture同时复用第一条`path`和对应root identity，先保持
   lexical direct-child与identity自洽，再expect exact `path_collision`。
2. `test_13_generated_compile_fake_success_failure_and_negative_authority_surface`对完整generated source做substring扫描；禁止词`camera`必然命中合法包名
   `camera_based_rgbww_optimizer`。纠偏须解析AST并对import module、imported symbol与callable的exact token/qualified name做authority检查，或使用不会命中合法包名
   的exact token边界；不得删掉禁止面，也不得放宽production owner。

候选module的生产职责边界仍与P3/P4/P5 owner合同一致，但targeted gate未通过，故没有资格声称实现合格、没有资格运行focused/full/post-edit CodeGraph，也不能
作为M1-I1、real retained-R3或canonical validator输入。

### Decision、residual risks 与 exact next branch

Decision：`REJECTED_TEST_FIXTURE_ASSERTION_ONLY_NO_PRODUCTION_FINDING_ESTABLISHED`。候选`cddd23e...`及evidence `5567837...`保持immutable provenance，
候选`consumable=false`。Residual risk是修正后的两项测试仍可能暴露真实production defect；因此下一包必须从fresh Orchestrator activation开始，只允许修改
dedicated test path，先重跑targeted，随后严格执行原冻结focused/compileall/full/post-edit CodeGraph/commit/postcommit targeted链；任一失败立即停止，不得在同包
追加第二次纠偏。

Exact next branch：`REF-P7-25-R2-B2-M1-S1-C1`，contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-DEDICATED-FIXTURE-CORRECTION-V1`。M1-I1、real/retained、validator、release、network与device routes继续hard locked。
