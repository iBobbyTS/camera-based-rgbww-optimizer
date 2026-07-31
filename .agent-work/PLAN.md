# REF-P7-25-R2-B2-P7-C1-C1：generated-source NUL escape correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-GENERATED-NUL-ESCAPE-CORRECTION-V1`

**Planner decision：** P7-C1 candidate
`96b15f4d7e000cb2f2276f069ad92832226b1afd` is
`REJECTED_TARGETED_CANONICAL_TEMPLATE_PHYSICAL_NUL` and is not consumable.
Its activation、exact-two-path scope、CodeGraph preflight order与zero budgets均通过；唯一缺陷是outer bytes
template提前把generated-source `\x00` separator解释成physical NUL，导致targeted `11`中`1` pass、`10` errors。

**当前唯一动作：** Orchestrator审核、更新 FULL，并以clean evidence HEAD
`158ea8c2385dede47cc090093f126a0a167acfb6` 为direct parent创建exact activation commit。Activation后，Executer只修改existing
domain-template module与dedicated test exact two paths：仅修generated-source NUL separator的escape layer，并增加或保持meaningful
byte-level assertion。之后运行fresh targeted11、focused93、compileall、unique full778、single implementation commit与postcommit
targeted11。P7-C1已经合规完成的pre-edit CodeGraph sync/query作为本direct successor的冻结ownership evidence；本包不得再调用
CodeGraph。不得运行external controller/source/root/process、synthetic integration、retained、validator、release、network或device work。

**唯一 Planner stop：**
`B2_P7_C1_C1_NUL_ESCAPE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1711-p7-retained-r3-b2-p7-c1-nul-failure-review.md`，identity在activation前由Orchestrator填写至本文final row与
FULL；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_generated_nul_escape_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-GENERATED-NUL-ESCAPE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"158ea8c2385dede47cc090093f126a0a167acfb6","expected_subject":"chore(plan): activate p7 c1 c1 nul escape correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1711-p7-retained-r3-b2-p7-c1-nul-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-GENERATED-NUL-ESCAPE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_TARGETED_CANONICAL_TEMPLATE_PHYSICAL_NUL","p7_rejected_candidate_commit":"96b15f4d7e000cb2f2276f069ad92832226b1afd","p7_rejected_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_candidate":{"commit":"96b15f4d7e000cb2f2276f069ad92832226b1afd","parent":"13f79754daf549deeee5b470e2e620fa70e43545","subject":"chore(p7): retain rejected p7 c1 runnable candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"1c31652a43350f50076a1d3e13da4dfd6ab5fc372341d3df3ad2e70cddc981ea","consumable":false},"baseline":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_bytes":19747,"source_sha256":"3a6a7c3b93d996369dfc7b0813cae098032d1c6c93136d82321ceb93886dcb59","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_bytes":20936,"test_sha256":"029233a25caa63b8f76b03557353ef748005d0e7f143425e36f5747cc688a841"},"accepted_codegraph_preflight":{"source_contract":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","activation_commit":"13f79754daf549deeee5b470e2e620fa70e43545","sync_invocations":1,"sync_exit":0,"query_invocations":1,"query_exit":0,"query_immediately_after_sync":true,"source_or_test_content_read_before_sync":0,"post_edit_sync_invocations":0,"post_edit_query_invocations":0,"successor_may_freeze":true},"exact_code_test_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"exact_execution_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py",".agent-work/EXECUTION_RESULT.md"],"correction_contract":{"outer_template_only_escape_layer":true,"physical_nul_bytes_in_owner_generated_source":0,"generated_runtime_nul_separator_semantics_preserved":true,"broad_replacement":false,"raw_template_conversion":false,"generic_escape_helper":false,"unrelated_backslash_changes":0,"public_exports_unchanged":true,"public_dataclass_fields_unchanged":true,"runtime_request_owner_unchanged":true,"lifecycle_owner_unchanged":true,"provenance_owner_unchanged":true,"controller_entrypoint_count":1,"test_method_count":11,"meaningful_byte_level_assertion_required":true},"runnable_contract":{"replacement_tuple_only":true,"git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"semantic_matrix_cases":16,"artifact_names":9,"explicit_root_bound_reads":7,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0,"second_analyzer":false,"second_lifecycle":false},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT_FULL_SHA","expected_subject":"fix(p7): preserve generated nul separator syntax","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"]},"execution_budgets":{"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":1,"postcommit_targeted_invocations":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_NUL_ESCAPE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen identities

Activation必须匹配machine row的full parent、subject与exact three-path set，之后porcelain clean。FULL只允许P7-C1-C1 active；必须明确
P7-C1 rejected、candidate `96b15f4d...` non-consumable、P6与P5 owners仍accepted、retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`且device authorization false。

Activation后先核对candidate/evidence topology、exact two-path baseline bytes/SHA、PLAN/FULL machine rows与archive identity。P7-C1已接受的
CodeGraph preflight必须按machine row冻结：它发生在candidate source理解/编辑之前，exact sync后immediate exact query，且post-edit调用0。
本successor不得再运行CodeGraph sync/query；不得以新query替换、补充或重解释冻结证据。

## 2. Exact two-path minimal correction

只允许修改machine row exact two paths，且两个路径都必须出现在implementation commit。不得新增helper/module/framework，不得改runtime、
provenance、conformance、lifecycle owners。

唯一production变更：在existing outer bytes `_CANONICAL_TEMPLATE` 内，仅对用于generated Python source的NUL separator syntax修正escape
layer，使builder/compose返回的source bytes不含physical byte `0x00`，同时generated module执行时Git metadata/path comparison与value
validation仍使用真实NUL separator语义。不得做全文件或generic `.replace()`、raw-template conversion、通用escape helper、fallback，亦不得改
unrelated backslashes、line endings、bindings、artifact names、phase order或error codes。

Dedicated test保持exact `11` methods，并添加或强化meaningful byte-level regression，至少证明：

1. owner template经builder/compose产生的source中physical `0x00` count exact `0`；
2. generated source bytes在冻结的activation/runtime Git-output comparisons及value guard位置保留escaped NUL source syntax；
3. generated source可AST parse/compile，运行时fake ledgers的真实NUL-delimited bytes仍匹配；
4. 断言使用exact byte/token boundary，不得用宽泛substring replace、regex/prefix allowlist或只执行不验证。

其余runnable contract完全冻结：replacement tuple是唯一activation/runtime/path/budget binding；required provenance owner/signatures、Git6、root1、
inputs4、matrix16、artifacts9、root reads7、eight lifecycle order、persist-before-read、single guarded entrypoint、single canonical stdout envelope、
stderr empty、primary-failure dominance及retry/fallback0不漂移。

## 3. Fresh validation, commit and evidence

在exact two-path edit完成后依次exact once：

1. `git diff --check`、exact path set、physical-NUL/token byte-level gate、test method count/name与frozen runnable AST/effect-free gate；
2. targeted domain-template：exact `11/11`、exit `0`、`OK`；
3. focused domain-template/runtime/conformance/preparation/provenance/machine-contract六模块：exact `93/93`、exit `0`、`OK`；
4. compileall exact source/test：exit `0`；
5. unique unbuffered full suite：exact `778/778`、exit `0`、`OK`，保留唯一unified session/terminal evidence；
6. 再次核对diff、no physical NUL、exact two paths、identities与frozen CodeGraph evidence；不得运行CodeGraph；
7. 创建direct child exact implementation commit，subject `fix(p7): preserve generated nul separator syntax`，changed paths exact two；
8. postcommit targeted exact `11/11`、exit `0`、`OK`；final porcelain除ER append前clean；
9. 向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation/candidate/implementation topology、before/after blob/bytes/SHA、
   byte-level gate、全部validation、frozen CodeGraph evidence、zero budgets与residual risk，然后停在Planner review。

Retry/fallback `0/0`。任一失败不得补第二实现、第二commit、重跑命令、降低counts、扩大路径或修改测试来追随错误实现；保留真实证据并停。

## 4. Acceptance and hard locks

Acceptance要求escape-layer correction narrow、exact two-path topology、physical NUL exact0、escaped-source/runtime separator语义保持、test11、
targeted11、focused93、compileall、unique full778、single implementation commit、postcommit targeted11与final porcelain通过。Success只报告
`repo_owned_runnable_domain_template_candidate_waiting_for_planner_review`；不得声称synthetic integration qualified。

External controller/source/root/process与synthetic integration exact0。Old failed evidence、retained R3/candidate payload、Git provenance replay、real
B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、
Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked0。本PLAN不授权P5-I1或later
stage。

维护性判断：本纠偏只修deterministic template owner的单一转义层，并由dedicated byte-level regression保护；不新增owner、helper、状态机或
parallel coordinator，维护复杂度不增加。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1711-p7-retained-r3-b2-p7-c1-nul-failure-review.md","bytes":5755,"sha256":"1e1c7e0866f3186eb25c2c8b40f19c40a6b549eaf02f5c8c4e157512e777625b"}`
