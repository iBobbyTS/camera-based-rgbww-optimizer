# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1：outer `_plain` physical-NUL correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-OUTER-PLAIN-PHYSICAL-NUL-CORRECTION-V1`

**Planner decision：** V1 validation-only closure is
`REJECTED_PRE_GATE_OUTER_PLAIN_PHYSICAL_NUL_REJECTION_MISSING_CANDIDATE_NOT_CONSUMABLE`。Activation、candidate topology、identities、AST与exact 11 methods均通过；唯一gate随后source-backed证明outer `_plain`使用literal escape string `"\\x00"`，没有拒绝physical NUL。Tests及external effects均为`0`。Candidate `88c4c037...`保持non-consumable；这是真实的local owner-semantic defect，不是generated-controller CR domain、科学分支或Human授权问题。

**当前唯一动作：** Orchestrator审核并更新FULL后，以clean HEAD
`11eba96e2c971b2c6da1e0a7e3bdf9dd574d20d0`为direct parent创建exact activation commit。Executer只在existing deterministic template module及dedicated test内纠正outer `_plain` physical-NUL guard并加入public negative/positive behavior assertions；必须保持literal escape text可用、`_CANONICAL_TEMPLATE`及exact-spec replacement byte-identical，且不得改serializer、matrix、owners或API。之后运行fresh pre-gate、targeted11、focused93、compileall、unique full778、single implementation commit与postcommit targeted11；继承CodeGraph evidence且本包CodeGraph `0/0`。只向ER append once并停回Planner。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_V1_C1_OUTER_PLAIN_PHYSICAL_NUL_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1758-p7-retained-r3-b2-p7-v1-outer-plain-nul-failure-review.md`，bytes `5922`，SHA-256
`67e578ce4d3ce35ff136989dd4b2d511bf7022f557cff9bae4469581ffd39955`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_v1_c1_outer_plain_physical_nul_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-OUTER-PLAIN-PHYSICAL-NUL-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"11eba96e2c971b2c6da1e0a7e3bdf9dd574d20d0","expected_subject":"chore(plan): activate p7 outer plain nul correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1758-p7-retained-r3-b2-p7-v1-outer-plain-nul-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-OUTER-PLAIN-PHYSICAL-NUL-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_GATE_OUTER_PLAIN_PHYSICAL_NUL_REJECTION_MISSING_CANDIDATE_NOT_CONSUMABLE","p7_candidate_commit":"88c4c0370a5dc296c04e949823c952398c6a394d","p7_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_validation":{"activation_commit":"12a38ea64040e8ab3eedd91c6feee80e6fe64494","evidence_commit":"11eba96e2c971b2c6da1e0a7e3bdf9dd574d20d0","gate_invocations":1,"gate_exit":1,"stable_finding":"outer_plain_physical_nul_rejection_missing","targeted_invocations":0,"external_effects":0},"baseline":{"candidate_commit":"88c4c0370a5dc296c04e949823c952398c6a394d","candidate_parent":"be0e4dafd725207d14c7862777f2739f68f99e81","candidate_subject":"chore(p7): retain rejected p7 payload candidate","candidate_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"candidate_canonical_binary_diff_sha256":"89cf2b7f7452deb7c139fbb26f1dfb91fa49574610e1a341a48610fbd1929fb4","source_blob_oid":"bbbcb3390a275043d72883729ddb6c8246de9e5a","source_bytes":19754,"source_sha256":"4601582595b59ff9a82721550a87e6d720bb390bb8e39e57324a711f599e36cb","test_blob_oid":"4074404187191b18286d201d456ea167294632c3","test_bytes":26844,"test_sha256":"13ec55eaac578f58583c7d6541733b3d2ab237168f1185796d9a9e9f3a449032","template_bytes":11999,"template_sha256":"0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467","replacement_bytes":1907,"replacement_sha256":"502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d2530160807"},"exact_implementation_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT","expected_subject":"fix(p7): reject physical nul in controller template specs","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"count":1},"source_domain_contract":{"module_physical_nul_bytes":0,"outer_plain_ast_physical_nul_constants":1,"outer_plain_ast_physical_lf_constants":1,"outer_plain_ast_physical_cr_constants":1,"literal_backslash_x00_spec_text_accepted":true,"physical_nul_spec_text_rejected":true,"physical_nul_error_code_field_specific":true,"canonical_template_byte_identical":true,"canonical_template_physical_nul_bytes":0,"canonical_template_literal_backslash_x00_tokens":8,"canonical_template_literal_backslash_n_tokens":3,"exact_spec_replacement_byte_identical":true,"serializer_changes":0,"semantic_matrix_changes":0,"owner_api_dataclass_changes":0,"new_helpers":0,"fallbacks":0},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"implementation_commits":1,"postcommit_targeted_invocations":1,"codegraph_sync":0,"codegraph_queries":0,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"third_code_path":0,"template_edits":0,"replacement_edits":0,"serializer_edits":0,"matrix_edits":0,"owner_api_edits":0,"new_helper":0,"generic_allowlist":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_V1_C1_OUTER_PLAIN_PHYSICAL_NUL_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen inputs

Activation必须匹配machine row的exact parent、subject与three-path set，之后porcelain clean。FULL只允许本C1 active；必须保持retained R3 unvalidated/unconsumed、P5/P6 accepted、candidate `88c4c03...` rejected/non-consumable、implementation commits `0`、device authorization false。

Activation后只读核对candidate topology、canonical binary diff、baseline source/test blob/bytes/SHA、rejected V1 activation/evidence、PLAN/FULL rows与archive identity。Accepted P7-C1 CodeGraph preflight继续冻结使用；本包CodeGraph sync/query exact `0/0`。任一不符必须在edit前fail closed。

## 2. Exact two-path correction

只允许修改machine row中的existing module与dedicated test：

1. 在existing `_plain` condition内，将错误的literal-backslash-`x00` string test纠正为physical-NUL semantic test。不得向module写入physical NUL byte；module strict UTF-8且physical NUL bytes仍为`0`。
2. 保持existing nonempty、type、physical LF与physical CR rules及stable caller-provided error code不变。不得新增helper、validator、normalizer、fallback或generic allowlist。
3. 在existing dedicated test method内加入public builder behavior assertion：otherwise-valid spec field注入physical NUL必须以该field现有stable code fail closed；otherwise-valid spec field包含literal four-character escape text backslash-`x00`必须仍能build并在runtime request中保持exact text。不得直接以private `_plain`调用替代public behavior coverage。
4. `_CANONICAL_TEMPLATE`必须保持baseline exact bytes/SHA；其physical NUL bytes `0`、literal generated `\\x00` tokens `8`、literal generated `\\n` tokens `3`。Generated template AST中的runtime NUL/LF语义不得因outer-spec guard修正而改变。
5. Exact valid `spec()`的replacement statement必须保持baseline exact bytes/SHA。Exact16 semantic matrix list-of-lists、test03、test08、eleven methods、owners/API/dataclasses、runtime/lifecycle/provenance、paths/budgets/artifacts/entrypoint全部不得改变。

实现后`git diff --check`通过，working diff仅exact two paths。不得顺手重构或修改doc/skill/debug。

## 3. One pre-gate, fresh validation, commit and posttest

Executer运行exact one fail-fast Python pre-gate，独立保存logical exit。Gate必须证明：

- activation/baseline/working path exact，strict UTF-8，module/test AST parse+compile，methods exact `11`；
- module source physical NUL bytes `0`，`_plain` AST exact physical NUL/LF/CR constants各`1`，不再把literal backslash-`x00`当成拒绝常量；
- public physical-NUL negative与literal-escape positive behavior均通过且stable；
- template及exact-spec replacement bytes/SHA完全等于baseline，template physical NUL `0`、literal `\\x00`/`\\n` counts `8/3`；
- production diff只有outer guard的one semantic token correction，test diff只有bounded behavior assertions；serializer、matrix、owners/API与所有其他module bytes不漂移。

Pre-gate exit `0`后按顺序exact once：

1. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`，exact `11/11`、exit `0`、`OK`；
2. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`，exact `93/93`、exit `0`、`OK`；
3. `.venv/bin/python -m compileall -q src tests`，exit `0`；
4. unique `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，single unified session、exact `778/778`、exit `0`、`OK`；
5. 核对exact two paths及`git diff --check`后，创建exact one commit，direct parent为activation commit、subject与paths匹配machine row；不得amend、second commit或混入ER；
6. commit后再次核对topology、source/test identities、template/replacement invariant及clean porcelain；运行exact one postcommit targeted命令，exact `11/11`、exit `0`、`OK`；
7. 只向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation、baseline/final identities与diff、source-domain proof、所有fresh outputs、commit topology、zero budgets和residual boundary，然后停在Planner review。ER append由Orchestrator另行保留，不属于implementation commit。

Retry/fallback `0/0`。任一gate/test/commit/posttest失败不得重跑、repair、fallback、降低counts或进入后续stage；保留真实证据并停止。

## 4. Acceptance boundary and hard locks

Success只报告
`outer_plain_physical_nul_correction_pass_waiting_for_planner`。Executer不得自行接受candidate或解锁integration；只有后续independent Planner review可判断new correction commit是否使repo-owned runnable template consumable。

本包不运行external controller/source/root/process或synthetic integration，不读取retained R3/candidate payload，不运行Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit或release。Network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked `0`。不需要Human授权。

维护性判断：纠正保持在single deterministic template owner与dedicated test边界，只修source-domain semantic constant并增加public regression coverage；不新增抽象、复杂度或平行owner。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1758-p7-retained-r3-b2-p7-v1-outer-plain-nul-failure-review.md","bytes":5922,"sha256":"67e578ce4d3ce35ff136989dd4b2d511bf7022f557cff9bae4469581ffd39955"}`
