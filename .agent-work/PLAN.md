# REF-P7-25-R2-B2-P7：repo-owned runnable domain-template correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-REPO-OWNED-RUNNABLE-DOMAIN-TEMPLATE-CORRECTION-V1`

**Planner decision：** P6 validation-only closure at evidence HEAD
`74dddff36d02d908934a9b65db018169f9966b8e` is
`ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL`。
Candidate `48b3979d6c0df5f488cd500597e26dc4c38877dd` 可作为 frozen P6 builder owner消费；它尚未通过
fresh synthetic integration。Planner source review确认 generated source仍缺完整运行绑定、owner import、entrypoint、callback和
persist-before-read ordering，所以真正 external integration继续锁定。

**当前唯一动作：** Orchestrator审核、更新 FULL，并以 clean evidence HEAD
`74dddff36d02d908934a9b65db018169f9966b8e` 为 direct parent创建 exact activation commit。Activation后，Executer只修改
existing domain-template module与dedicated test exact two paths，把 accepted deterministic builder纠偏为可执行但仍由既有 owner
管理 effects/lifecycle 的 canonical source；运行 frozen regression并创建 exact one implementation commit。不得创建 external
controller/source/root/process，不得进入 P5-I1、retained、validator或设备阶段。

**唯一 Planner stop：**
`B2_P7_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1647-p7-retained-r3-b2-p6-validation-acceptance-review.md`；bytes `6337`，SHA-256
`14e77f490188c9def0cf332b2a5d1c5059edb4283a2d160f0c6688598f1dd971`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_repo_owned_runnable_domain_template_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-REPO-OWNED-RUNNABLE-DOMAIN-TEMPLATE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"74dddff36d02d908934a9b65db018169f9966b8e","expected_subject":"chore(plan): activate p7 runnable template correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1647-p7-retained-r3-b2-p6-validation-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-REPO-OWNED-RUNNABLE-DOMAIN-TEMPLATE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","executer_dispatched":true,"device_authorized_by_this_file":false},"baseline":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob":"a1e196664840bc340be789829b8cf0826c9ec7f4","source_bytes":13918,"source_sha256":"56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob":"eb943384817996b96e332c83f618ba82cf210d4a","test_bytes":12992,"test_sha256":"6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc"},"accepted_runtime_owner":{"commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","parent":"099d1ad833c3e73b7dc157f5786ad66bb6718f5e","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","test_blob":"a6aa7d7caf015e2eb858830dc89aaedaeb51aafa","test_sha256":"66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782","entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime.execute_controller_runtime"},"exact_code_test_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"exact_execution_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py",".agent-work/EXECUTION_RESULT.md"],"runnable_contract":{"public_exports_unchanged":true,"public_dataclass_fields_unchanged":true,"runtime_request_owner_unchanged":true,"controller_entrypoint":"guarded_exact_once","activation_contract_binding_source":"replacement_tuple_only","unresolved_runtime_names":0,"required_owner_imports":["canonical_json_bytes","create_exclusive_root","persist_canonical_json","read_exact_file","run_read_only_git"],"git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"semantic_matrix_cases":16,"artifact_names":9,"explicit_root_bound_reads":7,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0,"second_analyzer":false,"second_lifecycle":false},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT_FULL_SHA","expected_subject":"fix(p7): make retained controller template runnable","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"]},"execution_budgets":{"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"implementation_commits":1,"postcommit_targeted_invocations":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and immutable baseline

Activation必须匹配 machine row的 full parent、subject与 exact three-path set，之后 porcelain clean。FULL只允许本 P7 task
active；P6 candidate必须标为 accepted/consumable但 synthetic integration仍未 qualified；P5 runtime owner继续 accepted；retained
R3必须为 `RETAINED_UNVALIDATED_UNCONSUMED`，device authorization false。

任何 code/test写入前，核对 baseline source/test blob、bytes、SHA与 committed working-tree bytes exact；核对 P6 candidate和 P5
runtime owner full commit/parent/path/blob身份。任一不匹配只append ER并停。不得 amend/rebase/rebuild accepted commits。

## 2. Exact two-path correction

只允许修改 machine row exact two paths；不得新增 helper/module/framework。`build_controller_domain_template`必须继续 pure、deterministic、
effect-free，现有 public exports、dataclass fields、stable errors、exact 18/14/4/7 static ownership和
`ControllerRuntimeRequest` owner边界不变。

修正 `_CANONICAL_TEMPLATE` 与 dedicated tests，使 compose后的 source同时满足：

1. replacement tuple是 activation/runtime/path/budget运行绑定的唯一输入。Generated source从该 frozen tuple显式派生
   `REPO_ROOT`、`ACTIVATION_COMMIT`、`RUNTIME_COMMIT`、`RUNTIME_PARENT`、`RUNTIME_PATHS`、`OUTPUT_ROOT`；不得依赖
   caller globals、environment、reflection、dynamic import、fallback或 generic mapping escape。
2. Provenance import显式包含并只通过 existing owner调用 `canonical_json_bytes`、`create_exclusive_root`、
   `persist_canonical_json`、`read_exact_file`、`run_read_only_git`。所有 owner call使用真实签名：
   `persist_canonical_json(root_identity, child_name, payload)`，所有 explicit reads绑定同一 immutable
   `DirectoryIdentity`。
3. Generated module只有 exact one guarded process entrypoint调用 `controller()`；import/compile不产生 effect。Success只向 stdout
   写 exact one canonical JSON envelope，stderr empty；不得 print repr、traceback或第二 envelope。
4. Exact eight lifecycle callbacks在使用前定义并由 single `execute_controller_lifecycle` owner调用；callbacks承载 phase-owned
   state转换，不得增加第二 lifecycle、parallel orchestration或在 lifecycle外预先完成全部 effects。
5. Order必须可由 AST与 effect-free harness证明：activation Git6 validation；root create1；four inputs exclusive persist；four
   same-root reads及 `RootIdentityChain` validation；evaluate matrix16；qualification target/sidecar；terminal target/sidecar；admission。
   每个 target先 persist再 read，qualification在terminal前，terminal在seal前，seal在admission前。不得 read nonexistent target，
   不得把 output-root string误传给 root-identity参数。
6. Git ledgers只消费 `GitLedger.exit_code/stdout/stderr` public fields并验证 frozen full identity，不得 `.returncode`、raw
   process transport或 second analyzer。现有 exact artifact names9、Git6、matrix16、root-bound explicit reads7与 retry/fallback0
   不得漂移。
7. Failure保持 primary dominance；不得因 terminal/seal缺 target覆盖早期 failure。该 correction不执行外部 source/root/process，
   只在 dedicated tests的 in-memory fake owner harness证明 callback order、arguments、single canonical envelope与零真实 effect。

Dedicated test总数改为 exact `11`，保留原八个方法含义并增加 exact三类 regression：runtime name/entrypoint binding；
persist/read/root-signature ordering；in-memory owner harness success与pre-root failure dominance。Assertions必须验证真实参数、返回身份、
callback顺序和 output bytes，不得只 compile/execute code。

## 3. Ordered validation and commit

依次且各 exact once：

1. targeted domain-template module：`11/11`、exit `0`、`OK`；
2. focused domain-template/runtime/conformance/preparation/provenance/machine-contract六模块：`93/93`、exit `0`、`OK`；
3. compileall exact source/test：exit `0`；
4. unique unbuffered full suite：`778/778`、exit `0`、`OK`，记录唯一 unified session；
5. `codegraph sync` exact once，再 query exact once，证明 builder -> runtime composition -> conformance/provenance/lifecycle仍为
   单一 owners且无 device/validator/release blast radius；
6. `git diff --check`、exact two-path diff、test method count/name、no external effect gate通过；
7. 创建 direct child exact implementation commit，subject
   `fix(p7): make retained controller template runnable`，changed paths exact two；
8. postcommit targeted exact `11/11`、exit `0`、`OK`，porcelain除最终 ER append前 clean；
9. 向 `.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录 commits、path/blob/bytes/SHA、counts、CodeGraph、
   external zero budgets与 residual risk，然后停在 Planner review。

Retry/fallback `0/0`。任一失败不得补第二实现、第二 commit、重跑命令、降低 counts或扩大路径；保留真实证据并停。

## 4. Acceptance and hard locks

Acceptance要求 exact two-path topology、runnable contract全部 dedicated tests、targeted11、focused93、compileall、unique full778、
CodeGraph、single commit、postcommit targeted11与final porcelain通过。成功只可报告
`repo_owned_runnable_domain_template_candidate_waiting_for_planner_review`；不得声称 synthetic integration qualified。

External controller/source/root/process与 synthetic integration exact `0`。Old failed evidence、retained R3/candidate payload、Git provenance
replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、
credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部
hard locked `0`。本 PLAN不授权 P5-I1或任何 later stage。

维护性判断：变更局限现有 domain-template owner与其 dedicated tests；运行 effect仍归 accepted runtime/provenance/conformance/lifecycle
owners，不引入新的 shared abstraction或 parallel coordinator。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1647-p7-retained-r3-b2-p6-validation-acceptance-review.md","bytes":6337,"sha256":"14e77f490188c9def0cf332b2a5d1c5059edb4283a2d160f0c6688598f1dd971"}`
