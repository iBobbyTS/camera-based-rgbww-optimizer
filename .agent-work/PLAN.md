# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1：correct-domain validation-only closure

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-CORRECT-DOMAIN-VALIDATION-CLOSURE-V1`

**Planner decision：** active P7-C1-C1-C1-C1 execution is
`REJECTED_PRE_GATE_EXECUTER_CR_DOMAIN_ASSERTION_CANDIDATE_NOT_YET_CONSUMABLE`。Committed candidate
`88c4c0370a5dc296c04e949823c952398c6a394d` contains the exact two-path semantic matrix/list-of-lists and dedicated-test corrections, but the unique pre-gate incorrectly required a CR constant in the generated-controller AST. Current source proves CR rejection belongs to outer builder `_plain`; no code/test defect was established. Because the package failed its frozen gate, later formal inventory/tests were `0` and the candidate remains non-consumable pending this fresh validation-only closure.

**当前唯一动作：** Orchestrator审核、更新FULL，并以clean evidence HEAD
`6d400efb156e3d072cecb5ea42dc5e923f8b0854`为direct parent创建exact activation commit。Activation后，Executer不得修改code/test；只消费current committed candidate identity，运行exact one corrected deterministic pre-gate：在outer builder source/behavior验证CR rejection，在generated AST不要求CR，并完成formal matrix/payload及frozen runnable inventory。随后fresh targeted11、focused93、compileall、unique full778 exact once；CodeGraph、implementation commit和postcommit test均为`0`。只向ER append once并停回Planner。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_V1_CORRECT_DOMAIN_VALIDATION_CLOSURE_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1746-p7-retained-r3-b2-p7-canonical-payload-pregate-domain-review.md`，bytes `6730`，SHA-256
`13b3dd9fa3799ede990f6e4b1c3efa834a62a009a5cbe420a0c51dbaea645ba3`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_v1_correct_domain_validation_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-CORRECT-DOMAIN-VALIDATION-CLOSURE-V1","execution_authorized_after_orchestrator_activation":true,"validation_only":true,"activation_commit":{"expected_parent":"6d400efb156e3d072cecb5ea42dc5e923f8b0854","expected_subject":"chore(plan): activate p7 payload validation closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1746-p7-retained-r3-b2-p7-canonical-payload-pregate-domain-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-CORRECT-DOMAIN-VALIDATION-CLOSURE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_GATE_EXECUTER_CR_DOMAIN_ASSERTION_CANDIDATE_NOT_YET_CONSUMABLE","p7_candidate_commit":"88c4c0370a5dc296c04e949823c952398c6a394d","p7_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"candidate":{"commit":"88c4c0370a5dc296c04e949823c952398c6a394d","parent":"be0e4dafd725207d14c7862777f2739f68f99e81","subject":"chore(p7): retain rejected p7 payload candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"89cf2b7f7452deb7c139fbb26f1dfb91fa49574610e1a341a48610fbd1929fb4","consumable_before_planner_review":false},"candidate_identity":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob_oid":"bbbcb3390a275043d72883729ddb6c8246de9e5a","source_bytes":19754,"source_sha256":"4601582595b59ff9a82721550a87e6d720bb390bb8e39e57324a711f599e36cb","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob_oid":"4074404187191b18286d201d456ea167294632c3","test_bytes":26844,"test_sha256":"13ec55eaac578f58583c7d6541733b3d2ab237168f1185796d9a9e9f3a449032"},"accepted_codegraph_preflight":{"source_contract":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","activation_commit":"13f79754daf549deeee5b470e2e620fa70e43545","sync_invocations":1,"sync_exit":0,"query_invocations":1,"query_exit":0,"successor_may_freeze":true},"exact_execution_write_paths":[".agent-work/EXECUTION_RESULT.md"],"code_test_writes":0,"corrected_gate_contract":{"invocations":1,"fail_fast":true,"candidate_identity_exact":true,"outer_plain_cr_source_check":true,"outer_plain_cr_behavior_check":true,"cr_bearing_specimen_expected_stable_error":true,"generated_ast_cr_constant_required":false,"generated_ast_parse_compile":true,"physical_nul_bytes":0,"generated_lf_tokens":3,"outer_template_nul_correction_locations":5,"generated_runtime_nul_constants":8,"generated_runtime_lf_constants":3,"test_methods":11,"test03_exact_boundary":true,"test08_exact_any_join_inventory":true,"semantic_matrix_container":"list","semantic_matrix_entry_container":"list","semantic_matrix_cases":16,"semantic_matrix_names_order_values_exact":true,"canonical_encode_strict_decode_reencode":true,"tuple_negative_error":"json_unsupported_value","git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"artifact_names":9,"explicit_root_bound_reads":7,"expected_bound_results":18,"controller_entrypoint_count":1,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778},"execution_budgets":{"corrected_pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"postcommit_targeted_invocations":0,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"candidate_edits":0,"second_gate":0,"implementation_commits":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_V1_CORRECT_DOMAIN_VALIDATION_CLOSURE_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen inputs

Activation必须匹配machine row的exact parent、subject与three-path set，之后porcelain clean。FULL只允许本V1 active；必须保持retained R3 unvalidated/unconsumed、P5/P6 accepted、candidate `88c4c03...` pending/non-consumable、implementation commits `0`、device authorization false。

Activation后只读核对candidate topology、canonical binary diff、exact source/test blob/bytes/SHA、evidence commit、PLAN/FULL rows和archive identity。Candidate source/test bytes不得改写、regenerate、checkout、touch或重新commit。Frozen P7-C1 CodeGraph evidence继续使用；本包CodeGraph sync/query exact `0/0`。

## 2. One corrected deterministic pre-gate

Executer运行exact one fail-fast Python gate并独立保存其logical exit。Gate只能读current committed candidate，不得生成临时代码副本或改动repo文件。

### 2.1 Correct CR ownership domain

Gate必须同时证明：

1. outer builder `_plain` source AST包含nonempty/plain-string rejection，且明确拒绝physical NUL、LF和CR；不得以generated controller常量代替该owner检查；
2. 以一个仅在合法plain-string spec field注入physical CR的bounded `ControllerDomainTemplateSpec` specimen调用existing builder，必须fail closed并返回该字段对应的stable `ControllerDomainTemplateError.code`；不得执行generated controller、root或其他effect；
3. exact valid spec仍能build；generated controller strict UTF-8、AST parse和compile通过；generated AST **不得被要求**包含CR constant。Gate可以确认generated constants没有意外physical CR，但不能把absence当错误。

不得修改builder来迎合gate，不得把CR规则移动进template，不得添加generic validation helper或second analyzer。

### 2.2 Complete previously unreached inventory

同一gate在CR domain通过后必须完成此前未执行的formal inventory：

- current changed paths相对activation exact two，candidate commit/parent/subject/path/diff和source/test identities exact；
- `git diff --check`、strict UTF-8、module/test/generated AST parse+compile；test methods exact `11`；
- physical NUL `0`、generated LF tokens `3`、outer-template NUL correction locations `5`、generated runtime NUL constants `8`、generated runtime LF constants `3`；
- test03使用current exact escaped-source boundary且保留NUL/LF negative specimens；test08只显式加入existing `any`/`join`并保持unknown-call/import/payload negatives；
- production `semantic_matrix` exact ordered `16` list-of-list entries；前13 names/order/boolean sources与末三true rows exact；`len == 16`、`all(...)`和persisted `{"matrix": semantic_matrix}` exact；tuple payload count `0`；
- existing canonical owner可encode该matrix，strict decode后shape/order/name/value不变并canonical re-encode identical；tuple specimen仍exact `ProvenanceIOError("json_unsupported_value")`；
- frozen runnable contract：replacement tuple only、Git ledgers6、root create1、synthetic inputs4、artifacts9、root-bound reads7、expected bindings18、eight lifecycle order、persist-before-read、qualification→terminal→seal→admission、single guarded entrypoint、single canonical stdout envelope、success stderr empty、retry/fallback0；
- serializer、runtime、conformance、lifecycle、provenance owners和public API/dataclasses未改；second owner/helper/analyzer/fallback/allowlist expansion为0。

任一断言失败必须停止；不得修gate、rerun或继续tests。

## 3. Fresh validation and evidence

Corrected pre-gate exit `0`后按顺序exact once：

1. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`，exact `11/11`、exit `0`、`OK`；
2. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`，exact `93/93`、exit `0`、`OK`；
3. `.venv/bin/python -m compileall -q src tests`，exit `0`；
4. unique `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，使用唯一unified session并保留terminal evidence，exact `778/778`、exit `0`、`OK`；
5. final只读核对candidate/source/test identities、archive、PLAN/FULL、worktree clean和CodeGraph调用0；不得stage/commit candidate，implementation commit exact `0`；
6. 只向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation/candidate/evidence topology、correct CR ownership proof、完整matrix/payload/runnable inventory、fresh test outputs、zero budgets和residual boundary，然后停在Planner review。

Retry/fallback `0/0`。任一失败不得重跑、repair、fallback、修改code/test、创建implementation commit或降低counts；保留真实证据并停止。

## 4. Acceptance boundary and hard locks

Success只报告
`repo_owned_runnable_domain_template_candidate_validation_pass_waiting_for_planner`。Executer不得自行把candidate标为accepted/consumable；只有后续independent Planner review可接受candidate `88c4c03...`。

本包不运行external controller/source/root/process或synthetic integration，不读取retained R3/candidate payload，不运行Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit或release。Network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked `0`。不需要Human授权。

维护性判断：本包是pure validation-only closure；candidate维持single deterministic template owner与dedicated test边界，不新增或修改任何production/test abstraction。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1746-p7-retained-r3-b2-p7-canonical-payload-pregate-domain-review.md","bytes":6730,"sha256":"13b3dd9fa3799ede990f6e4b1c3efa834a62a009a5cbe420a0c51dbaea645ba3"}`
