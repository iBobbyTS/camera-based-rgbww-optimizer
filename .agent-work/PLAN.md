# REF-P7-25-R2-B2-P7-C1-C1-C1-C1：canonical semantic payload correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-CANONICAL-SEMANTIC-PAYLOAD-CORRECTION-V1`

**Planner decision：** P7-C1-C1-C1 candidate
`d60dd878055f3a8d73eebc4c367b07791e0339d3` is
`REJECTED_TARGETED_STALE_TEST_EXPECTATIONS_AND_CANONICAL_JSON_TUPLE_PAYLOAD` and is not consumable。Activation与fresh pre-gate通过，exact三个LF correction及既有五个NUL correction成立；fresh targeted exact11以`2 failures + 1 error`停止。两项failure分别是test03旧NUL文本层级期望与test08漏列既有`any`/`join`；唯一production error是tuple-valued `semantic_matrix`被existing canonical JSON owner按合同拒绝。Retry/fallback、后续validation及所有external/retained/device effects为`0`。

**当前唯一动作：** Orchestrator审核、更新FULL，并以clean evidence HEAD
`f6a22638ff19ae63c661a7d1fdc81ae0124166f3`为direct parent创建exact activation commit。Activation后，Executer只修改existing domain-template module与dedicated test exact two paths：保留已成立的LF/NUL escape correction，精确更新两项stale test expectations，并把`semantic_matrix`改为canonical JSON-compatible、ordered exact16-entry owner payload；不得修改serializer、扩大allowlist、增加generic conversion/helper或新增owner。随后exact once运行fresh pre-gate、targeted11、focused93、compileall、unique full778、single implementation commit与postcommit targeted11。P7-C1 accepted CodeGraph evidence继续冻结，本包不得调用CodeGraph。不得运行external controller/root/process、synthetic integration、retained、validator、release、network或device work。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_CANONICAL_SEMANTIC_PAYLOAD_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1730-p7-retained-r3-b2-p7-c1-c1-c1-targeted-residual-review.md`，bytes `6582`，SHA-256
`fc3b19d8f6f49b09a236a1490471c862d1c070d77ce5de54f44480d5cf3a54e1`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_canonical_semantic_payload_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-CANONICAL-SEMANTIC-PAYLOAD-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"f6a22638ff19ae63c661a7d1fdc81ae0124166f3","expected_subject":"chore(plan): activate p7 canonical semantic payload correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1730-p7-retained-r3-b2-p7-c1-c1-c1-targeted-residual-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-CANONICAL-SEMANTIC-PAYLOAD-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_TARGETED_STALE_TEST_EXPECTATIONS_AND_CANONICAL_JSON_TUPLE_PAYLOAD","p7_rejected_candidate_commit":"d60dd878055f3a8d73eebc4c367b07791e0339d3","p7_rejected_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_candidate":{"commit":"d60dd878055f3a8d73eebc4c367b07791e0339d3","parent":"e20179f0bd8cbde03f81e7d9c2062f4b8c6700d1","subject":"chore(p7): retain rejected p7 newline candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"291325ec6cbc5659858aa639d523cc12265f4d87b15089d6ecc36f91f5876a9b","consumable":false},"baseline":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob_oid":"c500cae6f561438c170d29356db0b7f85666f651","source_bytes":19759,"source_sha256":"02a89ff41bba6cd164585478955263d90b76fc7c1ad4066fe8d7634651dfb6a4","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob_oid":"60618440fc57c568b0f6e07921520ff99817cc06","test_bytes":24613,"test_sha256":"f454f4574fd01235463df0c651e878d7cba2d8d547034d2cdf9719af2ebc42ef"},"accepted_codegraph_preflight":{"source_contract":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","activation_commit":"13f79754daf549deeee5b470e2e620fa70e43545","sync_invocations":1,"sync_exit":0,"query_invocations":1,"query_exit":0,"query_immediately_after_sync":true,"source_or_test_content_read_before_sync":0,"post_edit_sync_invocations":0,"post_edit_query_invocations":0,"successor_may_freeze":true},"exact_code_test_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"exact_execution_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py",".agent-work/EXECUTION_RESULT.md"],"correction_contract":{"preserve_generated_lf_token_count":3,"preserve_generated_nul_token_count":5,"physical_nul_bytes_in_owner_generated_source":0,"stale_test_expectation_updates":2,"test03_exact_escaped_source_boundary":true,"test03_ast_runtime_constants_preserved":true,"test08_existing_calls_added":["any","join"],"test08_generic_allowlist_expansion":false,"semantic_matrix_owner_payload_json_compatible":true,"semantic_matrix_payload_container":"list","semantic_matrix_entry_container":"list","semantic_matrix_cases":16,"semantic_matrix_names_order_values_unchanged":true,"semantic_matrix_tuple_payloads":0,"canonical_serializer_changes":0,"generic_conversion_helpers":0,"new_owners":0,"science_semantics_unchanged":true,"artifact_names":9,"public_exports_unchanged":true,"public_dataclass_fields_unchanged":true,"runtime_request_owner_unchanged":true,"lifecycle_owner_unchanged":true,"provenance_owner_unchanged":true,"controller_entrypoint_count":1,"test_method_count":11,"positive_and_negative_owner_payload_assertions":true},"runnable_contract":{"replacement_tuple_only":true,"git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"semantic_matrix_cases":16,"artifact_names":9,"explicit_root_bound_reads":7,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0,"second_analyzer":false,"second_lifecycle":false},"regression_contract":{"pregate_expected":1,"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT_FULL_SHA","expected_subject":"fix(p7): encode canonical semantic matrix payload","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"]},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":1,"postcommit_targeted_invocations":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_CANONICAL_SEMANTIC_PAYLOAD_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen identities

Activation必须匹配machine row的full parent、subject与exact three-path set，之后porcelain clean。FULL只允许P7-C1-C1-C1-C1 active；必须明确P7-C1-C1-C1 rejected、candidate `d60dd87...` non-consumable、P6与P5 owners仍accepted、retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`且device authorization false。

Activation后先核对candidate/evidence topology、exact two-path baseline blob/bytes/SHA、PLAN/FULL machine rows与archive identity。P7-C1 accepted CodeGraph preflight必须按machine row冻结；本successor不得运行CodeGraph sync/query，也不得以任何新query替换、补充或重解释冻结证据。

## 2. Exact two-path bounded correction

只允许修改machine row exact two paths，且两个路径都必须出现在implementation commit。不得新增helper/module/framework，不得修改runtime、provenance、conformance、lifecycle或canonical serializer owners。

Production只允许在existing outer bytes `_CANONICAL_TEMPLATE`的`phase_evaluate`内把tuple-valued `semantic_matrix`改为existing canonical owner可接受的JSON-compatible ordered payload：

1. outer container exact `list`，每项exact two-element `list`；不得使用tuple、set、自定义mapping/object或generic coercion；
2. exact `16`项，entry name、原顺序与boolean value不变；前13项仍读取同一`phase_state` keys，末三项仍为`qualification_nonempty`、`terminal_nonempty`、`admission_nonempty`且value `True`；
3. existing `len == 16`与`all(value for _name, value in semantic_matrix)`判定保持；persisted artifact仍为`{"matrix": semantic_matrix}`，artifact name、phase ordering与owner不变；
4. 不得修改`canonical_json_bytes`/`persist_canonical_json`或其支持域，不得新增serializer allowlist、fallback、conversion helper、owner、dataclass、public API或另一个matrix。

Production中candidate已成立的exact三个generated LF token和既有五个generated NUL token必须byte-for-byte保持；CR、其他backslash、Git/root/input bindings、paths、budgets、artifacts、lifecycle与guarded entrypoint均不得漂移。若实现需要第二production位置或serializer owner改动，必须fail closed并停回Planner。

Dedicated test保持exact `11` methods，只允许两项stale expectation correction及matrix payload正负回归：

1. test03把旧NUL generated-text期望更新为当前exact escaped-source stable boundary；同时继续证明template/composed physical NUL `0`、five NUL + three LF tokens exact、generated AST常量在runtime分别具有真实NUL/LF/CR语义，negative specimens仍失败；不得弱化为宽泛substring或动态从实现构造expected；
2. test08 exact generated-call inventory仅显式加入已存在的`any`与`join`，并以AST count/source boundary证明二者来自冻结matrix/path表达式；未知call/import与forbidden payload负例保持。不得改为prefix、module、reflection或generic allowlist；
3. existing in-memory harness必须证明exact16 list-of-list payload可由existing `canonical_json_bytes`编码、strict decode后shape/order/name/value不变且canonical re-encode相同；另以tuple specimen证明existing owner继续抛`ProvenanceIOError("json_unsupported_value")`。不得修改fake owner替生产接受tuple，也不得只执行不验证。

其余runnable contract完全冻结：replacement tuple是唯一activation/runtime/path/budget binding；Git6、root1、inputs4、matrix16、artifacts9、root reads7、eight lifecycle order、persist-before-read、single guarded entrypoint、single canonical stdout envelope、stderr empty、primary-failure dominance及retry/fallback0不漂移。

## 3. Fresh validation, commit and evidence

在exact two-path edit完成后依次exact once：

1. 一个fail-fast Python pre-gate，独立保留logical exit；核对activation/baseline、exact path set、`git diff --check`、test methods11、production delta仅matrix payload plus two dedicated expectation surfaces、three LF/five NUL identities、physical NUL0、module/generated AST+compile、exact matrix list-of-list16、owner positive/tuple-negative与frozen runnable AST/effect-free contract；
2. targeted domain-template exact `11/11`、exit `0`、`OK`；
3. focused domain-template/runtime/conformance/preparation/provenance/machine-contract六模块 exact `93/93`、exit `0`、`OK`；
4. compileall exact source/test，exit `0`；
5. unique unbuffered full suite exact `778/778`、exit `0`、`OK`，保留唯一unified session/terminal evidence；
6. 再次核对diff、exact two paths、payload/LF/NUL identities与frozen CodeGraph evidence；不得运行CodeGraph；
7. 创建direct child exact implementation commit，subject `fix(p7): encode canonical semantic matrix payload`，changed paths exact two；
8. postcommit targeted exact `11/11`、exit `0`、`OK`；final porcelain除ER append前clean；
9. 向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation/candidate/implementation topology、before/after blob/bytes/SHA、两项stale expectation与canonical payload正负证据、全部validation、frozen CodeGraph evidence、zero budgets与residual risk，然后停在Planner review。

Retry/fallback `0/0`。任一失败不得补第二实现、第二commit、重跑命令、降低counts、扩大路径或修改serializer/tests追随错误实现；保留真实证据并停。

## 4. Acceptance and hard locks

Acceptance要求三处LF与五处NUL correction不漂移、test03/test08精确更新、canonical JSON-compatible ordered matrix exact16、tuple仍fail closed、exact two-path topology、physical NUL0、generated AST/compile、test11、targeted11、focused93、compileall、unique full778、single implementation commit、postcommit targeted11与final porcelain通过。Success只报告
`repo_owned_runnable_domain_template_candidate_waiting_for_planner_review`；不得声称synthetic integration qualified。

External controller/source/root/process与synthetic integration exact0。Old failed evidence、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked0。本PLAN不授权P5-I1或later stage。

维护性判断：本纠偏维持single deterministic template owner与existing canonical provenance owner的清晰边界，仅将一个错误tuple payload收敛到已支持的JSON value domain并修正两项精确测试库存；没有新增owner、serializer、helper、状态机或并行执行路径。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1730-p7-retained-r3-b2-p7-c1-c1-c1-targeted-residual-review.md","bytes":6582,"sha256":"fc3b19d8f6f49b09a236a1490471c862d1c070d77ce5de54f44480d5cf3a54e1"}`
