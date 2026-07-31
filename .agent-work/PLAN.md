# REF-P7-25-R2-B2-P6-C1-C1-C1：exact generated guard-call allowlist correction

**计划状态：** WAITING_ORCHESTRATOR_ACTIVATION

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1-C1-C1

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-EXACT-GENERATED-GUARD-CALL-ALLOWLIST-CORRECTION-V1

**Planner decision：** P6-C1-C1 candidate `66532b5adef27de3c7839c5a7c783ebd7a053d38` at evidence HEAD
`0b704f535f3653429f527abec99f54c4c48d798a` is `REJECTED_TARGETED_GENERATED_RUNTIME_ERROR_AND_TYPE_CALL_ALLOWLIST_GAP`。
Activation与 exact one-path import correction均匹配，但 fresh targeted8只有 `7` pass/`1` failure。Planner独立确认 test08遗漏的 exact
`RuntimeError` 与 `type` 都来自 canonical generated source 的同一 pre-effect activation-contract gate；只允许补这两个 exact expected names。

**当前唯一动作：** Orchestrator审核、更新 FULL，并以 evidence HEAD
`0b704f535f3653429f527abec99f54c4c48d798a` 为 direct parent创建 exact activation commit。Activation后，Executer只在 dedicated test08
的 `generated_calls` expected set中加入 exact `RuntimeError` 与 `type`，保留 import correction和其余源码；然后运行冻结验证序列。

**唯一 Planner stop：**
B2_P6_C1_C1_C1_GENERATED_CALL_ALLOWLIST_CORRECTION_WAITING_PLANNER_REVIEW。

**本轮新归档：**
`.agent-work/PLANS/20260731-1622-p7-retained-r3-b2-p6-c1-c1-generated-call-review.md`；bytes `5477`，SHA-256
`5e84944d40520e659bcd3db6ccbcc7163917f7d9de526dccb1c060080b804e01`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p6_c1_c1_c1_exact_generated_guard_call_allowlist_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P6-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-EXACT-GENERATED-GUARD-CALL-ALLOWLIST-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"0b704f535f3653429f527abec99f54c4c48d798a","expected_subject":"chore(plan): activate p6 c1 c1 c1 generated call correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1622-p7-retained-r3-b2-p6-c1-c1-generated-call-review.md"],"clean_porcelain_required_after_activation":true},"rejected_candidate":{"commit":"66532b5adef27de3c7839c5a7c783ebd7a053d38","consumable":false,"evidence_commit":"0b704f535f3653429f527abec99f54c4c48d798a","targeted_tests":8,"targeted_exit":1,"failures":1,"errors":0,"passed":7,"unexpected_generated_calls":["RuntimeError","type"]},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): admit exact retained controller guard calls in tests","expected_changed_paths":["tests/test_p7_retained_r3_controller_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P6-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-EXACT-GENERATED-GUARD-CALL-ALLOWLIST-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","rejected_candidate_commit":"66532b5adef27de3c7839c5a7c783ebd7a053d38","rejected_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_controller_domain_template.py"],"correction_contract":{"test_method":"test_static_owner_and_forbidden_domain_guards","set_name":"generated_calls","exact_added_names":["RuntimeError","type"],"before_imported_names":["ControllerRuntimeRequest","compose_controller_source"],"after_imported_names":["ControllerRuntimeRequest","compose_controller_source"],"generic_allowlist_permitted":false,"dynamic_inventory_derived_allowlist_permitted":false,"other_test_body_edits":0,"production_source_edits":0,"third_path_edits":0,"source_blob_immutable":"a1e196664840bc340be789829b8cf0826c9ec7f4","source_sha256_immutable":"56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032","test_parent_blob":"ea737487e549758bb5f37c46a444cdf880b32d0f","test_parent_sha256":"0fdad3f746d8f1e206897c1951c805fb6d4aa1f25e1d0a54cd6cb305f8403f0e","preserve_exact_eight_test_names":true,"preserve_p6_source_and_runtime_shape":true},"regression_contract":{"targeted_expected":8,"focused_expected":90,"full_expected":775,"postcommit_targeted_expected":8},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"targeted_invocations":2,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"retry":0,"fallback":0},"zero_budgets":{"second_code_test_path_writes":0,"production_source_writes":0,"other_test_body_writes":0,"generic_allowlist_changes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P6_C1_C1_C1_GENERATED_CALL_ALLOWLIST_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 exact one-path scope

Activation direct parent、subject与 exact three-path set必须匹配 machine row，之后 porcelain clean。FULL只允许 P6-C1-C1-C1 active，明确
`66532b5adef27de3c7839c5a7c783ebd7a053d38` rejected/non-consumable；retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`，device authorization false。

Executer唯一可写 code/test path：

`tests/test_p7_retained_r3_controller_domain_template.py`

不得修改 domain-template production source、runtime、preparation、conformance、provenance-I/O、lifecycle、validator、retained helper或第二
code/test path。若 activation drift、worktree非 clean或 correction需要扩大路径，立即 fail closed append ER。

## 2. Exact generated-call correction

唯一允许的语义修改位于 `test_static_owner_and_forbidden_domain_guards` 内既有 `generated_calls` set literal：加入 exact string names
`RuntimeError` 与 `type`。它们分别对应 canonical generated `require_activation_contract` 中的 stable fail-closed异常和 exact tuple-type gate。

必须保留：

- runtime import exact names `ControllerRuntimeRequest` 与 `compose_controller_source`；
- `generated_calls` 中全部既有 names；
- 其他 import/call/payload inventory、negative assertions、fixture、expected counts和另外七个 test bodies；
- exact 八个 test method names；
- production source blob `a1e196664840bc340be789829b8cf0826c9ec7f4`、bytes `13918`、SHA-256
  `56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`。

禁止从 observed inventory动态构造 allowlist，禁止 wildcard/prefix/regex/generic builtin allowance，禁止删除 negative assertion或修改 production
source。Diff gate必须证明相对 parent test blob `ea737487e549758bb5f37c46a444cdf880b32d0f` 只有上述 two-element set addition。

## 3. Fresh ordered validation 与 commit

不得把前包的七项通过计入本包。Activation后按顺序执行，retry/fallback exact `0/0`：

1. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`：exact `8/8`、exit `0`、`OK`；
2. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`：exact `90/90`、exit `0`、`OK`；
3. compileall exact domain-template source与 dedicated test，exit `0`；
4. unique full：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`：exact `775/775`、exit `0`、`OK`，记录唯一 unified session；
5. `codegraph sync` exact once；query test08 generated inventory到 canonical `require_activation_contract`/runtime composition path，确认 two exact names有源码依据且无第二 effect/lifecycle/analyzer owner；
6. `git diff --check`、exact one-path gate、exact eight-method gate、production source identity gate、import preservation gate、AST/diff exact two-name addition gate；
7. 创建唯一 implementation commit，subject exact `fix(p7): admit exact retained controller guard calls in tests`，changed path exact one test文件；
8. postcommit targeted fresh exact `8/8`、exit `0`、`OK`；
9. 仅向 `EXECUTION_RESULT.md` EOF append一次完整 handoff，停在 Planner review。

## 4. Acceptance、failure 与 hard locks

Acceptance要求：唯一 diff是 test08既有 `generated_calls` set加入 exact `RuntimeError` 与 `type`；import correction、production source、其余 test
body与全部 negative boundary不变；fresh targeted8、focused90、compileall、unique full775、CodeGraph、diff/AST/path/identity gates、single test-only
commit与 postcommit targeted8全部通过。

任一检查失败即 fail closed：不 retry、不 fallback、不作第二修复、不放宽 counts或 allowlist、不运行 generated source/external controller/root；保留
code/evidence，append ER并停在唯一 Planner stop。

Old failed controllers/roots/evidence、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、
eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
TD-C、sentinel、P8、firmware、deployment全部 hard locked 0。本包通过只证明 corrected P6 composite candidate ready for Planner review，不自动
授权 synthetic integration。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1622-p7-retained-r3-b2-p6-c1-c1-generated-call-review.md","bytes":5477,"sha256":"5e84944d40520e659bcd3db6ccbcc7163917f7d9de526dccb1c060080b804e01"}`
