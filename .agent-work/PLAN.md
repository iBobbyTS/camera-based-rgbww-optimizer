# REF-P7-25-R2-B2-P6-C1：domain-template targeted correction

**计划状态：** WAITING_ORCHESTRATOR_ACTIVATION

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-DOMAIN-TEMPLATE-TARGETED-CORRECTION-V1

**Planner decision：** P6 candidate `3ca70bcee00a89535210d5b9ff9c33850bd58fb7` at evidence HEAD
`957538e491fd94f04e13c20f3020f476e79e384b` is `REJECTED_TARGETED_REPLACEMENT_INDENT_AND_STATIC_ASSERTION_CONTRACT`。Exact two-path scope正确，
但 targeted `8` tests exit `1`（failures `1`、errors `4`）。Replacement bytes 自带四空格，而 preparation owner 只替换 assignment
span，造成双重缩进；test 08 则把 mandatory metadata 中的 `retained` 误判为 retained-consumption。两项均为局部工程缺陷，
不需要 Advisor 或 Human 决策。

**当前唯一动作：** Orchestrator 审核、更新 FULL，并以 evidence HEAD
`957538e491fd94f04e13c20f3020f476e79e384b` 为 direct parent 创建 activation commit。Activation 后，Executer 仅修改已有 exact source/test 两路径：去除 replacement
statement 自带的 leading indentation，并把 test 08 改成 imports/calls/payload/generated-runtime semantic boundary 检查；随后按全新有序序列
运行 targeted8、focused90、compileall、unique full775、CodeGraph、exact two-path correction commit 与 postcommit targeted8。

**唯一 Planner stop：**
B2_P6_C1_DOMAIN_TEMPLATE_TARGETED_CORRECTION_WAITING_PLANNER_REVIEW。

**本轮新归档：**
.agent-work/PLANS/20260731-1604-p7-retained-r3-b2-p6-targeted-failure-review.md；bytes `19822`，SHA-256
`af7867b671295a0e0c222139a7866edc2cbeb28d32383d023e90f457b1704986`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p6_c1_domain_template_targeted_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P6-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-DOMAIN-TEMPLATE-TARGETED-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"957538e491fd94f04e13c20f3020f476e79e384b","expected_subject":"chore(plan): activate p6 c1 domain template correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1604-p7-retained-r3-b2-p6-targeted-failure-review.md"],"clean_porcelain_required_after_activation":true},"rejected_candidate":{"commit":"3ca70bcee00a89535210d5b9ff9c33850bd58fb7","consumable":false,"evidence_commit":"957538e491fd94f04e13c20f3020f476e79e384b","targeted_tests":8,"targeted_exit":1,"failures":1,"errors":4},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct retained controller domain template","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P6-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-DOMAIN-TEMPLATE-TARGETED-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","rejected_candidate_commit":"3ca70bcee00a89535210d5b9ff9c33850bd58fb7","rejected_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"correction_contract":{"replacement_leading_indent_bytes":0,"replacement_trailing_lf":1,"preparation_owner_replaces_assignment_span_only":true,"static_boundary_checks":["module_imports","module_calls","public_payload_fields","generated_runtime_imports","generated_runtime_calls","generated_runtime_semantics"],"mandatory_metadata_may_contain_retained":true,"global_retained_substring_ban":false,"preserve_builder_api":true,"preserve_exact_eight_test_names":true,"preserve_p6_scientific_and_runtime_shape":true},"regression_contract":{"targeted_expected":8,"focused_expected":90,"full_expected":775,"postcommit_targeted_expected":8},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"targeted_invocations":2,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P6_C1_DOMAIN_TEMPLATE_TARGETED_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 exact scope

Activation direct parent 必须 exact 为 `957538e491fd94f04e13c20f3020f476e79e384b`，subject 与 three-path set 必须匹配 machine row，之后 porcelain clean。FULL 只允许
P6-C1 active，并明确 `3ca70bcee00a89535210d5b9ff9c33850bd58fb7` 是 rejected/non-consumable；retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`，device authorization false。

Executer 只可修改已存在的：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
2. `tests/test_p7_retained_r3_controller_domain_template.py`

不得修改 runtime、preparation、conformance、provenance-I/O、lifecycle、validator、retained helper 或第三 code/test path。若 activation drift、
worktree 非 clean、correction 要求第三路径，立即 fail closed append ER。

## 2. Source correction contract

保持 P6 的 frozen public API、immutable dataclasses、builder ownership、canonical template、18/14/4/7 binding、Git6、single physical root、
matrix16、exact9 与 lifecycle inventory 不变。只修复 replacement statement 的定位语义：

- replacement bytes 必须从 `ACTIVATION_CONTRACT` 的 `A` 开始，leading indentation bytes exact `0`；
- replacement 仍是单一 canonical assignment并以 exact 一个 LF 结束；
- 不得更改 `prepare_controller_source`。它继续只替换 assignment AST byte span并保留 template source 的 line prefix；
- compose 后 strict UTF-8、AST parse、builtin compile必须通过，replacement uniqueness、adjacent validator和bytes/hash deterministic继续成立；
- 不得通过改成整行替换、strip/lstrip heuristic、第二 preparation owner或放宽 invalid-source failure来规避问题。

## 3. Test 08 semantic boundary correction

保留 exact 八个既有 test method 名称和其余七个测试语义。Test 08 不得全局禁止字符串 `retained`，因为 module docstring、reference/contract ID、
runtime owner module path与archive path属于 mandatory provenance metadata。它必须以 AST/value inventory直接证明：

- builder module没有 retained artifact reader、candidate reader、validator、eligibility、release、filesystem、process、network或device import/call；
- public spec/bundle/runtime request payload fields不接受 retained/candidate/eligibility/release/device generic payload；
- generated runtime source的 imports/calls只来自冻结的 runtime-adjacent owners，且没有 retained artifact consumption、canonical validator、
  eligibility emission、release consumption、第二 analyzer/classifier、generic parser、handwritten physical identity或额外 lifecycle；
- mandatory metadata 中出现 `retained` 不构成行为性失败；真正越过边界的 import/call/payload/generated-runtime fixture必须有 meaningful negative assertion。

禁止以新的全局 substring blacklist、空断言、只计数不验 AST/value或把 mandatory metadata 删除/脱敏来让测试通过。

## 4. Fresh ordered validation 与 commit

本包不得把 rejected P6 的失败 targeted invocation计入成功证据；activation 后必须按顺序 fresh 运行，retry/fallback exact 0：

1. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`：exact `8/8`、exit `0`、`OK`；
2. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`：exact `90/90`、exit `0`、`OK`；
3. compileall exact source/test two paths，exit `0`；
4. unique full：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`：exact `775/775`、exit `0`、`OK`，记录唯一 unified session；
5. `codegraph sync` exact once；query builder→runtime request/preparation/analyzer test path，确认无第二 effect/lifecycle/analyzer owner；
6. `git diff --check`、exact two-path gate、exact eight-method gate；
7. 创建唯一 correction commit，subject exact `fix(p7): correct retained controller domain template`，changed paths exact two；
8. postcommit targeted fresh exact `8/8`、exit `0`、`OK`；
9. 仅向 `EXECUTION_RESULT.md` EOF append一次完整 handoff，停在 Planner review。

## 5. Acceptance、failure 与 hard locks

Acceptance 要求：两个局部缺陷均按本合同修复；P6 其余 API/source/golden/inventory合同无漂移；fresh targeted8、focused90、compileall、
unique full775、CodeGraph、diff/path/method gates、single correction commit、postcommit targeted8全部通过。Handoff记录 activation、rejected candidate、
correction commit/parent/subject/path set、两文件 blob/bytes/SHA、replacement indent/LF、test08 AST/value boundary、所有 invocation/session/exit/count及zero budgets。

任一检查失败即 fail closed：不 retry、不 fallback、不放宽 counts、不修改第三路径、不运行 generated source/external controller/root，不读取 retained
或旧 evidence；保留 code/evidence，append ER并停在唯一 Planner stop。

旧 failed controllers/roots/evidence、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、
eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
TD-C、sentinel、P8、firmware、deployment全部 hard locked 0。P6-C1 通过只证明 corrected domain-template owner ready，不自动授权 synthetic integration。
