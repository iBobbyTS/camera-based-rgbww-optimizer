# REF-P7-25-R2-B2-P7-C1：CodeGraph preflight ordering correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1`

**Planner decision：** P7 at evidence HEAD
`778576e1bc1df797e0293d52fa58dfe4fc385744` is
`REJECTED_PRE_EDIT_CODEGRAPH_QUERY_BEFORE_REQUIRED_SYNC`。P7没有进入实现；P5 runtime owner、P6 deterministic
domain-template owner、frozen source/test baseline与所有external/retained/device locks保持不变。

**当前唯一动作：** Orchestrator审核、更新 FULL，并以 clean evidence HEAD
`778576e1bc1df797e0293d52fa58dfe4fc385744` 为 direct parent创建 exact activation commit。Activation后，Executer先运行
exact one CodeGraph sync及紧随的exact one query，再理解或编辑source/test；之后只修改existing domain-template module与
dedicated test exact two paths，完成原P7 runnable合同、fresh regression与exact one implementation commit。不得执行post-edit
CodeGraph、external controller/source/root/process、retained、validator或device work。

**唯一 Planner stop：**
`B2_P7_C1_CODEGRAPH_PREFLIGHT_ORDER_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1656-p7-retained-r3-b2-p7-codegraph-ordering-failure-review.md`；bytes `5389`，SHA-256
`f81f9a4c5e7cd153b99431799aa59a21520b436d397201e904cb3f6b0d631fbc`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_codegraph_preflight_order_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"778576e1bc1df797e0293d52fa58dfe4fc385744","expected_subject":"chore(plan): activate p7 c1 codegraph preflight correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1656-p7-retained-r3-b2-p7-codegraph-ordering-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_EDIT_CODEGRAPH_QUERY_BEFORE_REQUIRED_SYNC","p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"baseline":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob":"a1e196664840bc340be789829b8cf0826c9ec7f4","source_bytes":13918,"source_sha256":"56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob":"eb943384817996b96e332c83f618ba82cf210d4a","test_bytes":12992,"test_sha256":"6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc"},"accepted_runtime_owner":{"commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","parent":"099d1ad833c3e73b7dc157f5786ad66bb6718f5e","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","test_blob":"a6aa7d7caf015e2eb858830dc89aaedaeb51aafa","test_sha256":"66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782","entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime.execute_controller_runtime"},"exact_code_test_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"exact_execution_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py",".agent-work/EXECUTION_RESULT.md"],"codegraph_order":{"activation_and_identity_checks_only_before_preflight":true,"source_or_test_content_read_before_sync":0,"source_or_test_understanding_before_query":0,"sync_invocations":1,"query_invocations":1,"query_immediately_after_sync":true,"preflight_query_is_final_codegraph_evidence":true,"post_edit_sync_invocations":0,"post_edit_query_invocations":0},"runnable_contract":{"public_exports_unchanged":true,"public_dataclass_fields_unchanged":true,"runtime_request_owner_unchanged":true,"controller_entrypoint":"guarded_exact_once","activation_contract_binding_source":"replacement_tuple_only","unresolved_runtime_names":0,"required_owner_imports":["canonical_json_bytes","create_exclusive_root","persist_canonical_json","read_exact_file","run_read_only_git"],"git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"semantic_matrix_cases":16,"artifact_names":9,"explicit_root_bound_reads":7,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0,"second_analyzer":false,"second_lifecycle":false},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT_FULL_SHA","expected_subject":"fix(p7): make retained controller template runnable","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"]},"execution_budgets":{"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync_preflight":1,"codegraph_queries_preflight":1,"codegraph_sync_postedit":0,"codegraph_queries_postedit":0,"implementation_commits":1,"postcommit_targeted_invocations":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_CODEGRAPH_PREFLIGHT_ORDER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation, identity-only baseline and CodeGraph preflight

Activation必须匹配machine row的full parent、subject与exact three-path set，之后porcelain clean。FULL只允许本P7-C1 task
active；P7必须标为被CodeGraph顺序拒绝且implementation commits `0`；P6 candidate继续accepted/consumable但synthetic
integration未qualified；P5 runtime owner继续accepted；retained R3必须为`RETAINED_UNVALIDATED_UNCONSUMED`，device authorization
false。

在CodeGraph preflight之前，只允许读取PLAN/FULL/activation topology并核对committed blob、bytes、SHA等identity metadata；不得读取
source/test content，不得grep/find，不得对实现作语义推断或编辑。随后依次且各exact once：

1. 在repo root运行`codegraph sync`，exit `0`；
2. 紧接运行exact one `codegraph explore`，读取domain-template builder、runtime composition及
   conformance/provenance/lifecycle owner call paths，exit `0`。

该query既是pre-edit source理解入口，也是本包唯一和最终CodeGraph ownership/blast-radius evidence。之后CodeGraph sync/query
预算均为`0`；不得在validation或commit后重复。Sync/query任一失败即append ER并停，不得读/改source/test。

## 2. Exact two-path runnable correction

只允许修改machine row exact two paths；不得新增helper/module/framework。`build_controller_domain_template`继续pure、deterministic、
effect-free，现有public exports、dataclass fields、stable errors、exact 18/14/4/7 static ownership和
`ControllerRuntimeRequest` owner边界不变。

修正`_CANONICAL_TEMPLATE`与dedicated tests，使compose后的source同时满足：

1. Replacement tuple是activation/runtime/path/budget运行绑定的唯一输入；generated source显式派生`REPO_ROOT`、
   `ACTIVATION_COMMIT`、`RUNTIME_COMMIT`、`RUNTIME_PARENT`、`RUNTIME_PATHS`、`OUTPUT_ROOT`，无caller globals、environment、
   reflection、dynamic import、fallback或generic mapping escape。
2. Provenance import显式包含并只通过existing owner调用`canonical_json_bytes`、`create_exclusive_root`、
   `persist_canonical_json`、`read_exact_file`、`run_read_only_git`。`persist_canonical_json(root_identity, child_name, payload)`
   使用真实签名；所有explicit reads绑定同一immutable`DirectoryIdentity`。
3. Generated module只有exact one guarded process entrypoint调用`controller()`；import/compile无effect。Success stdout exact one
   canonical JSON envelope、stderr empty；无repr、traceback或第二envelope。
4. Exact eight lifecycle callbacks在使用前定义，由single`execute_controller_lifecycle`调用；callbacks承载phase-owned state
   转换，无第二lifecycle、parallel orchestration或lifecycle外预做全部effects。
5. AST与effect-free harness证明顺序：activation Git6；root create1；four inputs exclusive persist；four same-root reads及
   `RootIdentityChain` validation；evaluate matrix16；qualification target/sidecar；terminal target/sidecar；admission。每个target
   先persist再read，qualification在terminal前、terminal在seal前、seal在admission前；不得read nonexistent target或把root path
   string传给root-identity参数。
6. Git ledgers只消费`GitLedger.exit_code/stdout/stderr`并验证frozen full identity；不得`.returncode`、raw process transport或
   second analyzer。Exact artifact names9、Git6、matrix16、root-bound reads7及retry/fallback0不漂移。
7. Failure保持primary dominance；terminal/seal缺target不得覆盖早期failure。本包不执行external source/root/process，只在dedicated
   tests的in-memory fake-owner harness证明callback order、arguments、single canonical envelope与零真实effect。

Dedicated test总数exact `11`：保留原八个方法含义，增加runtime name/entrypoint binding、persist/read/root-signature ordering、
in-memory owner harness success与pre-root failure dominance三类regression；assertions验证真实参数、返回identity、callback顺序和
output bytes，不得只compile/execute。

## 3. Post-edit validation and commit

CodeGraph preflight通过后，依次且各exact once：

1. targeted domain-template：`11/11`、exit `0`、`OK`；
2. focused domain-template/runtime/conformance/preparation/provenance/machine-contract六模块：`93/93`、exit `0`、`OK`；
3. compileall exact source/test：exit `0`；
4. unique unbuffered full suite：`778/778`、exit `0`、`OK`，记录唯一unified session；
5. 不运行CodeGraph；将已冻结的preflight query作为唯一CodeGraph证据，并明确它证明owner routing而非post-edit bytes；
6. `git diff --check`、exact two-path diff、test method count/name、runnable AST/effect-free/no-external-effect gate通过；
7. 创建direct child exact implementation commit，subject
   `fix(p7): make retained controller template runnable`，changed paths exact two；
8. postcommit targeted exact `11/11`、exit `0`、`OK`，porcelain除最终ER append前clean；
9. 向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation/implementation、path/blob/bytes/SHA、validation、
   preflight CodeGraph、zero budgets与residual risk，然后停在Planner review。

Retry/fallback`0/0`。任一失败不得补第二实现、第二commit、重跑命令、降低counts或扩大路径；保留真实证据并停。

## 4. Acceptance and hard locks

Acceptance要求exact two-path topology、runnable合同全部dedicated tests、targeted11、focused93、compileall、unique full778、
preflight CodeGraph sync/query、single commit、postcommit targeted11与final porcelain通过。Success只报告
`repo_owned_runnable_domain_template_candidate_waiting_for_planner_review`；不得声称synthetic integration qualified。

External controller/source/root/process与synthetic integration exact`0`。Old failed evidence、retained R3/candidate payload、Git
provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、
environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、
deployment全部hard locked`0`。本PLAN不授权P5-I1或任何later stage。

维护性判断：本纠偏仅调整CodeGraph ownership检查的时间点；实现仍局限现有template owner及dedicated tests，runtime/provenance/
conformance/lifecycle保持单一owner，不新增parallel coordinator或维护性债务。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1656-p7-retained-r3-b2-p7-codegraph-ordering-failure-review.md","bytes":5389,"sha256":"f81f9a4c5e7cd153b99431799aa59a21520b436d397201e904cb3f6b0d631fbc"}`
