# P7 retained-R3 Option B：M1 repo-owned real-manifest-v2 domain-template owner

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-REAL-MANIFEST-DOMAIN-TEMPLATE-V1`

**当前唯一动作：** 在 Orchestrator 建立 exact activation commit 后，Executer 仅新增一个 pure/deterministic/effect-free
real-manifest-v2 controller template owner及其 dedicated test，完成冻结验证、exact two-path implementation commit与一次 ER
handoff，然后停止在 Planner 验收门。

**唯一 Planner stop：**
`B2_M1_REAL_MANIFEST_DOMAIN_TEMPLATE_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2057-p7-retained-r3-b2-p7-i1-acceptance-route-transition.md`；bytes `2871`，SHA-256
`3d5b8934cd03ce94fb164c9693fb361da251a64ccc3ed06ae573f461e953e0cc`；不得覆盖 earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_real_manifest_domain_template_v1","reference_task_id":"REF-P7-25-R2-B2-M1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-REAL-MANIFEST-DOMAIN-TEMPLATE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"9b23dbd17d5b29ddeb68b55334ade2f1815fa141","expected_subject":"chore(plan): activate real manifest domain owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2057-p7-retained-r3-b2-p7-i1-acceptance-route-transition.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"feat(p7): own real manifest domain template","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-REAL-MANIFEST-DOMAIN-TEMPLATE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_IMPLEMENTATION","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"builder_contract":{"module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_real_manifest_domain_template","entrypoint":"build_real_manifest_domain_template","exports":["RealManifestDomainTemplateError","RealManifestGitPathIdentity","RealManifestCommitIdentity","RealManifestInputIdentity","RealManifestBaselineIdentity","RealManifestDomainTemplateSpec","RealManifestDomainTemplateBundle","build_real_manifest_domain_template"],"input_type":"RealManifestDomainTemplateSpec","output_type":"RealManifestDomainTemplateBundle","output_fields":["template_source","template_sha256","replacement_statement","replacement_sha256","runtime_request","expected_bound_results","expected_artifact_names","expected_lifecycle_order"],"frozen_dataclasses":true,"pure_in_memory":true,"assignment_name":"REAL_MANIFEST_CONTRACT","validation_function":"require_real_manifest_contract","runtime_request_type":"ControllerRuntimeRequest","generic_path_allowlist":false,"parallel_owner":false},"canonical_source_contract":{"strict_utf8":true,"ast_parse":true,"builtin_compile":true,"golden_template_and_replacement_sha256_literals_required":true,"schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","exact_artifact_names":["retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":5,"single_output_root":true,"output_root_create_calls":1,"c1_input_labels":["path_owner_index","path_owner_index_seal","terminal_evidence","terminal_evidence_seal"],"retained_input_labels":["current_lineage_candidate","resolved_formal_plan","setup_lineage_release"],"c1_reads":4,"retained_reads":3,"input_reads_total":7,"controller_read_only_git_invocations":56,"git_success_field":"exit_code","runtime_returncode_uses":0,"persist_canonical_json_calls":5,"output_reload_reads":5,"read_exact_file_calls":12,"root_chain_file_count":5,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"retry":0,"fallback":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0},"validation_codes":["invalid_spec","reference_task_mismatch","contract_mismatch","commit_identity_invalid","git_path_identity_invalid","baseline_identity_invalid","input_identity_invalid","activation_identity_mismatch","c1_cardinality_mismatch","c1_label_mismatch","retained_cardinality_mismatch","retained_label_mismatch","path_collision","path_not_absolute","path_not_direct_child","byte_count_invalid","sha256_invalid","blob_oid_invalid","mode_invalid","source_path_invalid","output_root_invalid","repo_root_invalid","process_argv_mismatch","literal_type_invalid"],"test_contract":{"new_test_methods":13,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":74,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_baseline":778,"full_expected":791,"postcommit_targeted_expected":13},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query":1,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true,"query_before_source_edit":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"second_writer":0,"second_analyzer":0,"second_classifier":0,"second_serializer":0,"second_lifecycle":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2057-p7-retained-r3-b2-p7-i1-acceptance-route-transition.md","bytes":2871,"sha256":"3d5b8934cd03ce94fb164c9693fb361da251a64ccc3ed06ae573f461e953e0cc"},"planner_stop":"B2_M1_REAL_MANIFEST_DOMAIN_TEMPLATE_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 exact scope

Executer 开始时必须验证 activation 是 parent
`9b23dbd17d5b29ddeb68b55334ade2f1815fa141` 的 direct child、subject exact、changed paths exact three、
PLAN/FULL machine rows strict JSON且 required FULL subset exact，随后 porcelain clean。任一不符必须在 source/test read或edit前停止。

本包只允许新增：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`；
2. `tests/test_p7_retained_r3_real_manifest_domain_template.py`。

不得编辑 existing P3 provenance I/O、P4 conformance/lifecycle、P5 runtime、P7 synthetic template或其他路径。M1 implementation
commit须为activation direct child、exact two paths、subject `feat(p7): own real manifest domain template`。Executer不得修改PLAN/FULL/archive。

## 2. CodeGraph 与 maintainability preflight

因repo存在`.codegraph/`，activation gate后、读取或编辑source/test前，必须先运行一次`codegraph sync`，再运行一次精确query，覆盖
P3 `canonical_json_bytes/create_exclusive_root/persist_canonical_json/read_exact_file/run_read_only_git`、P4
`analyze_controller_source/validate_root_identity_chain/execute_controller_lifecycle`、P5 `ControllerRuntimeRequest`及P7 builder pattern；query还须确认
新module/test此前absent。不得先grep/read再补sync。

编辑完成后再执行一次`codegraph sync`和一次针对新owner/import/call graph的精确query，证明没有新增第二writer/analyzer/classifier/
serializer/lifecycle且只依赖既有owners。两次sync均须成功；不得把CodeGraph failure降级为warning。

维护性边界冻结为：新module只拥有typed immutable spec、canonical controller template/replacement与runtime request composition；P3独占physical
I/O/canonical serialization，P4独占AST conformance/root-chain/lifecycle，P5独占source persistence/process execution。不得复制这些实现，亦不得新增
generic dict payload、generic path allowlist或external one-off controller。

## 3. Public API、typed identities 与 fail-closed validation

`__all__`必须逐字节等于machine row的8项exports。所有dataclass都必须`frozen=True`，nested collections只能是tuple，builder不得mutate input。

- `RealManifestGitPathIdentity`字段 exact：`repo_path,before_blob_oid,after_blob_oid,before_sha256,after_sha256,binary_patch_sha256`；
- `RealManifestCommitIdentity`字段 exact：`commit,parent,subject,changed_paths,full_patch_sha256`；
- `RealManifestInputIdentity`字段 exact：`label,path,byte_count,sha256,device,inode,mode,root_path,root_device,root_inode,root_mode`；
- `RealManifestBaselineIdentity`字段 exact：`release_checkpoint,helper_v1,integration,helper_path,test_path,seam_chain,governance_manifest_sha256,guide_sha256,advisor_decision_sha256,advisor_attachment_sha256,human_governance_override,helper_disposition`；
- `RealManifestDomainTemplateSpec`字段 exact：`reference_task_id,contract_id,activation,baseline,c1_inputs,retained_inputs,source_path,output_root,repo_root,process_argv`；
- `RealManifestDomainTemplateBundle`字段 exact：machine row `output_fields`的8项。

Spec必须要求task/contract exact；activation/baseline/paths/hashes/blob OIDs/bytes/device/inode/modes/type exact并使用machine row稳定错误码。
C1 tuple必须exact4且labels/order exact；retained tuple必须exact3且labels/order exact。每组path必须absolute canonical direct child of its frozen root，七条输入
path与source/output不得碰撞；file mode exact0600、root mode exact0700、bytes正数。Repo paths必须canonical relative且由typed identity逐项绑定，绝不接受
generic allowlist。`process_argv` exact `(repo_root + "/.venv/bin/python", "-")`。

## 4. Generated real-manifest controller contract

Builder只能返回immutable bytes/hash/replacement/`ControllerRuntimeRequest`；调用builder本身的filesystem、process、Git、external artifact与network effects
必须为0。Template assignment exact `REAL_MANIFEST_CONTRACT`且只出现一次，紧邻唯一`require_real_manifest_contract`调用；replacement为canonical
Python literal、无physical NUL/CR/LF escape drift。Dedicated test必须用literal golden SHA-256冻结template与replacement exact bytes，并strict UTF-8、AST parse、
`compile()`以及`compose_controller_source()`重验。

Generated controller只可imports/calls P3/P4 owner surface和Python builtins；不得import/call canonical validator、exact-five validator callback、eligibility、
release、network/device/science或P7 synthetic owner。Static AST inventory必须exact冻结：Git owner calls56且只读`exit_code`；input reads7（C1=4、retained=3）；
output reload reads5；`read_exact_file` total12；`persist_canonical_json`5；output root create1；root-chain exact one并包含5个output identities；lifecycle exact one、
order exact8、retry/fallback0。Generated source不得读`returncode`，不得transport/alias/containerize effect-owned identities；P4 report
`effect_transport_uses=()`。

Git56必须从typed baseline与activation identity构造exact command/expected-output checks，绑定full child/parent/subject/path set、before/after blobs、
canonical/full/per-path patches、helper v1 disposition、release checkpoint与accepted seam chain；不得以generic path allowlist替代逐项identity。Manifest payload必须
冻结schema/status、baseline chain、C1 four、retained three及before/after physical identities。Real input values只能来自future spec；M1本包不得读取real C1或retained。

Output root exact five direct regular0600 canonical compact sorted UTF-8 JSON+LF artifacts：manifest、manifest seal、terminal、terminal seal、admission。
每次persist后须strict root-bound reload、duplicate/non-finite rejection与byte/hash equality；root before/after identity chain必须一致。Manifest/seal一旦persist不可
rewrite/repair/replace/relocate。Schema/status exact machine row values；payload不得含eligibility、release consumability、validator pass或device authorization claim。

任何conformance/activation/root/inputs/evaluate primary failure必须保持原exception identity为dominant；只有既有P4 lifecycle可生成failure terminal/seal/admission，
terminal或seal failure阻止admission。不得fallback/retry/second root/second process。

## 5. Dedicated regression contract

Dedicated file必须exact13个meaningful `unittest` methods，并冻结method names/inventory，至少逐项覆盖：

1. exact exports、dataclass fields/frozen/deep tuple contract；
2. deterministic build、exact template/replacement bytes与literal SHA；
3. exact runtime request、source/output/process binding且builder no-effect；
4. invalid spec/task/contract/type stable codes；
5. invalid commit/blob/SHA/path/bytes/mode/root identity stable codes；
6. activation与baseline chain exact typed binding、no generic allowlist；
7. C1 exact4 labels/order/direct-child/uniqueness与hash cardinality；
8. retained exact3 names/order/direct-child/uniqueness与frozen hashes；
9. schema/status/exact5 artifact names与canonical manifest/seal/terminal/admission；
10. owner imports/calls与Git56/`exit_code`/no`returncode` AST inventory；
11. P4 bound-result/root-read/root-chain/effect-transport canonical inventory；
12. lifecycle exact order、primary-failure dominance、terminal/seal admission blocking、retry0；
13. no-I/O/no-authority negative surface，以及generated strict compile和fully fake success/failure runnable lifecycle。

Fake runnable test只能inject in-memory/fake owners，不得创建external root/process或读取任何real C1/retained evidence。Assertions必须验证实际payload、call counts、
identity/hash与exception dominance，不能只执行代码。

## 6. Exact validation、commit 与 evidence

按此顺序各运行一次，任一nonzero立即停且不得以较窄green覆盖：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template`，exact `13/13`；
2. focused：machine row command，exact `74/74`；
3. compileall：machine row command，exit0；
4. full discovery：machine row command，基线`778`加13，exact `791/791`且唯一`OK`；
5. post-edit CodeGraph sync/query与`git diff --check`；
6. stage exact two paths并创建唯一implementation commit；
7. postcommit targeted exact `13/13`，并证明commit direct parent、subject、exact paths、worktree clean。

不得运行第五次test、第二次compileall、第三次CodeGraph sync/query或retry。通过或失败均只向
`.agent-work/EXECUTION_RESULT.md`做一次EOF append，记录activation/implementation topology、before absent/after bytes/SHA/blob、golden template/replacement identity、
API/AST/call inventory、四组test exit/count、CodeGraph/diff、zero budgets与first failure。Executer不得自行接受M1或进入M1-I1。

## 7. Hard locks、failure branches 与授权

本包是纯离线工程实现，不命中AGENTS高危设备授权，也不需要Advisor科学决策或Human批准；但它不授权任何device/light操作。

Real C1/retained physical reads、external controller/root/process、M1-I1 synthetic integration、real B2、manifest actual seal、canonical validator/callback、eligibility、
retained audit、release、network/DNS/`.env`/credentials、camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部0。
Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`，canonical validator仍是唯一eligibility owner。

- activation/CodeGraph gate失败：code/test edits0，single ER handoff后停Planner；
- implementation或precommit validation失败：保留exact two-path diff，不跨界修复、不commit、不retry，single ER handoff后停Planner；
- commit后postcommit targeted或topology失败：保留该commit为non-consumable evidence，不amend/rebase，single ER handoff后停Planner；
- 全绿：只报告candidate waiting Planner review；不得称retained eligible或解锁M1-I1。

维护性判断：M1新增一个typed pure domain owner与dedicated tests，依赖现有P3/P4/P5边界而不复制I/O或lifecycle；复杂度集中在immutable
spec/template合同，13项回归和CodeGraph inventory覆盖边界，当前不建议另行重构。
