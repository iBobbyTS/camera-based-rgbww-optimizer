# P7 retained-R3 Option B：M1-C1-C1-C1 wildcard fixture correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-C1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-C1-C1-WILDCARD-FIXTURE-CORRECTION-V1`

**当前唯一动作：** 在Orchestrator建立exact activation commit后，Executer只修改dedicated P4 conformance test中的test23
wildcard negative fixture，使wildcard import位于合法module scope而controller call仍位于function scope；随后完整执行冻结的53/70/compileall/787、
post-edit CodeGraph与postcommit53验证链，做single correction commit与single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_C1_C1_C1_WILDCARD_FIXTURE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2138-p7-retained-r3-b2-m1-c1-c1-wildcard-fixture-failure-review.md`；bytes `7470`，SHA-256
`2df0babdfed6cb1bc5cacffb9911c31eef1ec428ef9e698936c69c5a226437fb`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_c1_c1_c1_wildcard_fixture_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-C1-C1-WILDCARD-FIXTURE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f","expected_subject":"chore(plan): activate existing root wildcard fixture correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2138-p7-retained-r3-b2-m1-c1-c1-wildcard-fixture-failure-review.md"],"clean_porcelain_required_after_activation":true},"rejected_candidate":{"commit":"40d92acb77b32f370955d687c74c7ff7077f55e1","parent":"77c96d6eec4d1881a82a678c84165dff03d6fb6e","subject":"chore(p7): retain rejected existing root candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_provenance_io.py"],"tree":"f8ff6be0b0436947eb2eaae26914b55313ce442b","canonical_binary_patch_sha256":"00eb408bb3fe4440a5589dacd9799247577ccd0c6dbc891c6ff693c5e9e5f683","consumable":false,"immutable":true},"evidence_commit":{"commit":"ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f","parent":"40d92acb77b32f370955d687c74c7ff7077f55e1","subject":"chore(evidence): record existing root wildcard test failure","changed_paths":[".agent-work/EXECUTION_RESULT.md"],"er_before_blob":"fc9e97fb076dbe013640833e85dbbcb00edeb20b","er_after_blob":"22afac8a93932aed3241f38c0623452b12972bd8"},"candidate_blobs":{"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py":{"blob":"07f89d15c8288e0d45c495d6d5737bc37427b769","bytes":30424,"sha256":"008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee"},"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py":{"blob":"d6d6cc628861baf8a95a09f13fa9204989693b5b","bytes":19767,"sha256":"118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d"},"tests/test_p7_retained_r3_controller_conformance.py":{"blob":"429ab49802f50e1e3743dffd09c7f72345a2c271","bytes":25822,"sha256":"5091c9f98607f1d0a1122fca96356391dbe5b5bdff943a6c5ba8a0c678f0d3a9"},"tests/test_p7_retained_r3_provenance_io.py":{"blob":"e7bd034d46fda2d24b1fc431e1bfc75f3f570f83","bytes":34056,"sha256":"96c33cb4a0cd21706c9b14c8527a50f0b3bd355ccc4efad7d2e3a9a239c864a2"}},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct existing root wildcard fixture","expected_changed_paths":["tests/test_p7_retained_r3_controller_conformance.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-C1-C1-WILDCARD-FIXTURE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"BLOCKED_ON_EXISTING_ROOT_IDENTITY_OWNER","existing_root_identity_owner_status":"ACTIVE_WILDCARD_FIXTURE_CORRECTION","m1_existing_root_candidate_commit":"40d92acb77b32f370955d687c74c7ff7077f55e1","m1_existing_root_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_controller_conformance.py"],"fixture_contract":{"test_method":"test_23_existing_root_import_and_call_provenance_near_misses_rejected","only_case":"wildcard","module_scope_import":"from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import *","controller_call":"existing = read_existing_root(path)","source_utf8":true,"source_ast_parseable":true,"wildcard_import_ast_parent":"Module.body","controller_call_ast_parent":"FunctionDef.body","expected_error":"existing_root_owner_import_invalid","expected_error_unchanged":true,"all_other_cases_unchanged":true,"all_other_test_methods_unchanged":true,"production_classifier_unchanged":true,"new_helper_framework":false},"test_contract":{"p3_test_methods":28,"p4_test_methods":25,"p5_test_methods":6,"p7_test_methods":11,"new_test_methods":0,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance","targeted_expected":53,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template","focused_expected":70,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":787,"postcommit_targeted_expected":53},"codegraph_contract":{"prior_pre_edit_sync_query_inherited":true,"inherited_from_activation":"77c96d6eec4d1881a82a678c84165dff03d6fb6e","inherited_candidate_paths_unchanged_through_evidence":true,"fresh_pre_edit_sync":0,"fresh_pre_edit_query":0,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"retry":0,"fallback":0},"zero_budgets":{"production_source_writes":0,"p3_test_writes":0,"other_p4_test_method_writes":0,"method_additions":0,"generic_parser_fallback":0,"classifier_weakening":0,"m1_source_test_writes":0,"m1_implementation_commits":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2138-p7-retained-r3-b2-m1-c1-c1-wildcard-fixture-failure-review.md","bytes":7470,"sha256":"2df0babdfed6cb1bc5cacffb9911c31eef1ec428ef9e698936c69c5a226437fb"},"planner_stop":"B2_M1_C1_C1_C1_WILDCARD_FIXTURE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Review decision 与 activation gate

上一M1-C1-C1结果判定为
`REJECTED_TARGETED_WILDCARD_NEGATIVE_SOURCE_CONSTRUCTION_FAILURE_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`。Candidate
`40d92ac...`把P3/P4 owner与九项regressions提交为exact four paths，但唯一targeted `53` exit1；52 pass不构成whole-package验收。
Evidence `ec782ab...`仅追加ER，不改变candidate paths。本包只纠正test23 wildcard specimen的source construction，不重新实现或修改P3/P4 owner。

Executer开始前必须验证activation是parent `ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f`的direct child，subject exact
`chore(plan): activate existing root wildcard fixture correction`，changed paths exact FULL/PLAN/本archive三项，PLAN/FULL machine rows strict
JSON、required FULL subset exact、porcelain clean。还必须验证candidate/evidence topology、subjects、changed paths、tree/patch、four candidate blobs与ER
before/after blobs exact；任一不符须在source/test edit或validation前single ER handoff并停止。

Rejected candidate `40d92ac...`与evidence `ec782ab...`必须immutable、non-consumable；不得amend、rebase、cherry-pick重写、regenerate或把其actual
subject改称原PLAN implementation subject。本包是pure-offline test-fixture engineering correction，不命中AGENTS高危设备授权，不需Human或Advisor。

## 2. Exact one-path correction

唯一write path是`tests/test_p7_retained_r3_controller_conformance.py`。编辑前其blob/bytes/SHA必须exact
`429ab49802f50e1e3743dffd09c7f72345a2c271` / `25822` /
`5091c9f98607f1d0a1122fca96356391dbe5b5bdff943a6c5ba8a0c678f0d3a9`。其他candidate三路径在本包前后必须保持machine row冻结的
blob/bytes/SHA exact。

只允许修改existing method
`test_23_existing_root_import_and_call_provenance_near_misses_rejected`内wildcard case及其直接shape assertion：

- 构造UTF-8 bytes，其module body包含exact
  `from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import *`；该`ast.ImportFrom`必须是module-scope node，不能经过shared
  `runtime(body)`缩进进controller。
- 同一source仍须包含一个`def controller():`，其function body内是direct
  `existing = read_existing_root(path)`，确保P4能看到owner call而不是只看到孤立import。
- Source必须能被`ast.parse`成功解析；test内应以direct AST assertion证明wildcard import在`Module.body`、controller call在
  `FunctionDef.body`，然后调用现有`subject.analyze_controller_source(source)`。
- Expected stable code必须仍是exact `existing_root_owner_import_invalid`；不得改成`source_parse_failed`、宽泛`assertRaises`或接受多码。
- `missing/wrong_module/duplicate/alias/attribute/local_shadow/argument_shadow`的source与expected codes全部byte-semantically unchanged。Test23外的
24个methods、module imports、shared `OWNER_IMPORT`/`runtime`、所有assertions与method inventory `25`不变；不得新增method、helper framework、dynamic
import/exec/eval、regex或generic source fallback。

Production P3/P4 source、P3 test、P5/P7、M1及任何其他path写入均为`0`。尤其不得为通过fixture而修改
`_validate_existing_root_owner`、weakening classifier或给function-scope wildcard建立容错路径。

## 3. CodeGraph 与 maintainability boundary

上一包在任何candidate edit前已按序完成CodeGraph sync/query，且candidate/evidence提交固定其exact four paths；本包明确继承该pre-edit owner-map证据，fresh
pre-edit sync/query预算`0/0`，不得为了重复确认额外消耗。One-path edit完成且四组runtime checks通过后，执行exact一次`codegraph sync`，随后exact一次
query，覆盖test23、`runtime`、`analyze_controller_source`、`_validate_existing_root_owner`，证明：

- diff仅在dedicated test，P3/P4 owner definitions没有改变；
- wildcard specimen在module scope进入existing P4 classifier；
- 无second analyzer/classifier、generic parser/helper或production blast-radius change。

Sync/query必须`1/1`且exit0；不得降级warning或retry。维护性边界仍是P3唯一physical provenance-I/O owner、P4唯一AST/effect-provenance owner、test仅
构造合法negative specimen。本地one-off conditional/source bytes足够，不得抽象新shared helper。

## 4. Exact validation、commit 与 ER evidence

Activation/topology/blob gate与exact one-path edit后严格按下列顺序，每项exact一次；任一nonzero、count或shape mismatch立即停止，不得retry/fallback或继续后续项：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance`，exact
   `53/53`、`OK`；必须特别记录wildcard subtest现在返回exact `existing_root_owner_import_invalid`，而不是仅记录suite green；
2. focused：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template`，exact
   `70/70`、`OK`；
3. compileall：`.venv/bin/python -m compileall -q src tests`，exit0；
4. full discovery：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，exact `787/787`、唯一`OK`；
5. post-edit CodeGraph sync/query exact `1/1`，随后AST/diff/blob gate与`git diff --check`；unstaged diff必须exact one path，only test23 wildcard
   fixture/shape assertion，methods仍`25`，candidate另外三paths blob exact；
6. stage exact one path，创建唯一implementation commit；subject exact `fix(p7): correct existing root wildcard fixture`；parent必须是runtime
   activation HEAD，changed paths exact one；冻结before/after blob、bytes/SHA与canonical binary patch SHA；
7. postcommit targeted exact `53/53`、`OK`，验证commit topology/subject/path与porcelain clean。

总test invocations `4`、compileall `1`、fresh CodeGraph sync/query `1/1`、implementation commit `1`、retry/fallback `0/0`。不得运行额外ad-hoc
Python、pytest、discovery、formatter、test correction或第二commit。

无论通过/失败，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append。记录activation/candidate/evidence topology、candidate four blobs、ER immutable
prefix、one-path before/after identity/diff、AST module/function parents、actual wildcard code、test method inventories、四次test/compileall、CodeGraph、commit
topology、first failure与全部zero budgets。旧ER必须prefix exact；Executer不得改PLAN/FULL/archive/debug/GUIDE/RESEARCH。

## 5. Hard locks、failure branches 与 next unlock

本包不会运行M1或读取任何real inputs。Accepted C1/retained physical reads、external controller/root/process、Git provenance replay、real B2、manifest/seal
writes、canonical validator/callback、eligibility、retained audit/release、network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public
analyzer/TD-C/sentinel/P8/firmware/deployment全部`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

- Activation/topology/blob gate失败：test writes0、commit0、all validations0，single ER handoff后停Planner；
- Edit/targeted/focused/compileall/full/CodeGraph/precommit gate失败：保留exact one-path diff，不跨界修复、不commit、不retry，single ER handoff后停Planner；
- Commit后posttarget/topology失败：保留commit为non-consumable evidence，不amend/rebase，single ER handoff后停Planner；
- 全绿：只报告candidate `40d92ac...` + correction commit完成full validation，waiting independent Planner review；不得自行接受、消费或进入M1。

Planner只有在独立复核完整validation与exact one-path semantic diff后，才能接受composite existing-root owner candidate。接受后下一步才是fresh M1 successor；必须使用新
activation与accepted P3/P4 owner，不能复用被拒绝M1 activation或从本PLAN直接执行M1。

维护性判断：本包只修一个dedicated negative fixture的module/function source边界，保持生产owner、classifier、稳定错误码与test inventory不变；验证覆盖whole
four-path candidate，未引入helper/framework或新职责，接受后无需额外重构。
