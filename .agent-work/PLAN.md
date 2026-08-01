# P7 retained-R3 Option B：M1-S1-C1 dedicated fixture correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-DEDICATED-FIXTURE-CORRECTION-V1`

**当前唯一动作：** Orchestrator先把M1-S1的targeted failure登记为test-only rejection并建立fresh exact activation；随后Executer只修改
`tests/test_p7_retained_r3_real_manifest_domain_template.py`中的test07 collision fixture与test13 authority-negative assertion，重跑完整冻结验证链，创建exact
one-path correction commit，向ER做single append，然后停止。

**唯一 Planner stop：**
`B2_M1_S1_C1_DEDICATED_FIXTURE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2337-p7-retained-r3-b2-m1-s1-targeted-failure-review.md`；bytes `24194`，SHA-256
`f0da8a83f4694aa04fb846495e26dcc895136cdc1851e027fbc5b83d15bdd38e`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_c1_dedicated_fixture_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-DEDICATED-FIXTURE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"5567837b1bbe3fdd368f0c8cbddd21c19a436e40","expected_subject":"chore(plan): activate real manifest fixture correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2337-p7-retained-r3-b2-m1-s1-targeted-failure-review.md"],"clean_porcelain_required_after_activation":true},"rejected_candidate":{"activation_commit":"84b3458765849f9c50515067788af365006cef68","candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_parent":"84b3458765849f9c50515067788af365006cef68","candidate_tree":"ff424f29e6a7a95349500ce356669a754d9ffa14","evidence_commit":"5567837b1bbe3fdd368f0c8cbddd21c19a436e40","evidence_parent":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_consumable":false,"exact_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_blob":"84fcd755225af39eb89459146de282392367b70b","source_bytes":23352,"source_sha256":"5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d","test_blob":"05db407f9fd6c67bf359f1874cff2f9baaf9564f","test_bytes":17413,"test_sha256":"cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af","targeted_ran":13,"targeted_passed":11,"targeted_failed":2},"correction_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): correct real manifest domain fixtures","expected_changed_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-DEDICATED-FIXTURE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_DEDICATED_FIXTURE_CORRECTION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_real_manifest_candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","m1_real_manifest_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_real_manifest_domain_template.py"],"correction_contract":{"test_methods_changed":["test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"],"production_writes":0,"test_method_additions":0,"test_method_removals":0,"collision_fixture":"copy_first_identity_and_replace_only_label_with_second_expected_label","collision_expected_code":"path_collision","authority_check":"ast_exact_import_and_callable_tokens","raw_source_substring_forbidden":true,"legal_package":"camera_based_rgbww_optimizer"},"test_contract":{"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query":1,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true,"query_before_test_read_or_edit":true},"execution_budgets":{"correction_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"retry":0,"fallback":0},"zero_budgets":{"production_writes":0,"second_test_path_writes":0,"source_candidate_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"external_controller_reads":0,"external_controller_writes":0,"external_controller_processes":0,"external_root_reads":0,"external_root_creates":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2337-p7-retained-r3-b2-m1-s1-targeted-failure-review.md","bytes":24194,"sha256":"f0da8a83f4694aa04fb846495e26dcc895136cdc1851e027fbc5b83d15bdd38e"},"planner_stop":"B2_M1_S1_C1_DEDICATED_FIXTURE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation 与 immutable topology gate

本包是对失败M1-S1的独立test-only successor，不得复用旧activation作为执行授权。Executer开始前必须证明当前activation是
`5567837b1bbe3fdd368f0c8cbddd21c19a436e40`的direct child，subject exact `chore(plan): activate real manifest fixture correction`，changed paths exact
FULL/PLAN/本failure-review archive三项；porcelain clean，PLAN/FULL machine rows均strict JSON且PLAN required FULL subset exact。

同时冻结下列immutable topology：旧activation `84b3458765849f9c50515067788af365006cef68`；candidate `cddd23e...`是其direct child、tree
`ff424f29e6a7a95349500ce356669a754d9ffa14`、changed paths exact machine row two paths；evidence `5567837...`是candidate direct child且只改ER。当前source/test
blob、bytes、SHA-256必须exact匹配machine row，archive bytes/hash exact。任一不符须在test read/edit、tests或CodeGraph前single ER handoff并停止。

Candidate保持`consumable=false`。本包通过后也只能产生waiting-review correction candidate；不得在Executer阶段自称M1-S1 owner已accepted。

## 2. Fresh CodeGraph 与 exact write boundary

Activation gate后、读取或编辑dedicated test前，exact一次`codegraph sync`再exact一次精确query，覆盖新module builder、test07/test13、P3/P4/P5 owner calls与
generated source authority surface。Query须确认production source仍为candidate frozen blob、两项失败均可由test source解释、无需production修改；若发现production finding，
write0并停Planner，不得扩大纠偏。

唯一write path是`tests/test_p7_retained_r3_real_manifest_domain_template.py`。只允许修改test07与test13；production module、P3/P4/P5/P7、其余test methods、imports
（除test13 AST断言确有必要的stdlib test import）与fake runtime行为均冻结。test methods仍exact13，不能新增helper/framework或第二authority owner。

Ordered validations之后、commit之前，再exact一次CodeGraph sync/query，覆盖同一builder、两项测试与P3/P4/P5 call graph，证明production/source blob不变、
test-only blast radius、无second analyzer/classifier/serializer/lifecycle/authority owner。两轮均须exit0且不得retry。

## 3. Exact two-fixture correction

### 3.1 test07 collision fixture

不得只替换第二identity的`path`。构造collision时，以第一条C1 identity为完整有效physical identity，并只把`label`替换为第二条expected label，例如语义exact为
`replace(first, label=second.label)`；这样第二条仍通过label、absolute path、direct-child、mode及device/root identity validation，随后两条path exact相同，断言必须得到
stable code `path_collision`。继续保留原cardinality、order、direct-child等其他断言。

### 3.2 test13 authority-negative assertion

删除对完整source的裸substring all/none判断。对generated source strict UTF-8 decode并`ast.parse`，分别收集：

- `ast.Import` / `ast.ImportFrom`的exact module qualified names与imported aliases；
- `ast.Call`的exact `Name.id`或`Attribute.attr` callable tokens。

Import modules须exact限定为generated controller既有的`sys`、P4 conformance module与P3 provenance-I/O module；禁止authority symbols
`canonical_validator`、`emit_eligibility`、`consume_release`、`device_authorized`、`camera`、`ray120c`及forbidden modules`socket`、`requests`须按exact token/qualified
name不相交。合法package token `camera_based_rgbww_optimizer`不得因包含字符序列`camera`而失败。不得删除negative coverage，也不得改production generated source来迎合测试。

## 4. Complete frozen validation chain 与 commit

Pre-edit gate/CodeGraph通过、exact one-path test edit完成后，严格按顺序每项exact一次；任一nonzero/count/shape mismatch立即停止，后项保持0：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template`，exact`13/13`、`OK`；
2. focused：machine row exact command，exact`83/83`、`OK`；
3. compileall：`.venv/bin/python -m compileall -q src tests`，exit0；
4. full discovery：machine row exact command，exact`800/800`、唯一`OK`；
5. post-edit CodeGraph sync/query exact`1/1`，随后验证test methods13、test07/test13 exact semantics、source candidate frozen blob/hash、unstaged diff exact one test path，
   `git diff --check` clean；
6. stage exact one test path，创建唯一commit，subject exact `fix(p7): correct real manifest domain fixtures`，parent exact current activation，冻结after blob/bytes/SHA与
   canonical patch SHA；
7. postcommit targeted exact`13/13`、`OK`，验证commit subject/parent/path与porcelain clean。

总tests `4`、compileall `1`、CodeGraph sync/query `2/2`、commit `1`、retry/fallback `0/0`。不得运行pytest、formatter、额外ad-hoc test或同包第二次纠偏。

## 5. ER handoff、failure branches 与 hard locks

无论通过或失败，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append。记录activation/candidate/evidence topology、archive identity、pre/post CodeGraph、exact
test diff、两项fixture结果、四次tests/compileall、source unchanged identity、correction commit identity、ER immutable prefix、first failure及全部zero budgets。
Executer不得修改PLAN/FULL/archive/debug/GUIDE/RESEARCH。

- Activation/topology/pre-CodeGraph失败：test writes0、tests0、commit0，single ER后停止；
- Edit或targeted/focused/compileall/full/post-CodeGraph/precommit失败：保留one-path diff，不修第二次、不commit、不继续后项，single ER后停止；
- Commit后posttarget/topology失败：保留commit为non-consumable evidence，不amend/rebase，single ER后停止；
- 全绿：只报告`M1-S1-C1 correction candidate waiting independent Planner review`，不得进入M1-I1或real B2。

本包pure-offline，不命中Human高危授权，也不需要Advisor。Real/retained evidence读取、external controller/root/process、synthetic integration、Git provenance replay、
physical subordinate manifest、canonical validator/callback/eligibility、retained audit、release、network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/
FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：纠偏只影响一个dedicated test中的两个既有方法；production owner边界和复杂度均不变，完整冻结验证与pre/post CodeGraph覆盖回归，不需要重构。
