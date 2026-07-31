# REF-P7-25-R2-B2-P6-C1-C1：dedicated test runtime-request import correction

**计划状态：** WAITING_ORCHESTRATOR_ACTIVATION

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1-C1

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-TEST-RUNTIME-REQUEST-IMPORT-CORRECTION-V1

**Planner decision：** P6-C1 candidate `73e2f2cc3b9b1465a47381b55360cf941ac0cbc4` at evidence HEAD
`e6520062bb1a60a0686066ccec39c4fb190905c0` is `REJECTED_TARGETED_TEST_RUNTIME_REQUEST_IMPORT_OMISSION`。
Activation、exact two-path scope 与 zero budgets均匹配；fresh targeted `8` tests中七项通过，唯一 error 是 dedicated test 08 引用了
`ControllerRuntimeRequest` 但未显式导入。该缺陷只属于 test import boundary，不需要 Advisor、Human、production source或第三路径。

**当前唯一动作：** Orchestrator 审核、更新 FULL，并以 evidence HEAD
`e6520062bb1a60a0686066ccec39c4fb190905c0` 为 direct parent 创建 exact activation commit。Activation 后，Executer只在 dedicated
test 的既有 runtime-owner import中加入 `ControllerRuntimeRequest`，不得改任何 test body或 production source；然后按 fresh ordered sequence
运行 targeted8、focused90、compileall、unique full775、CodeGraph、single test-only commit与 postcommit targeted8。

**唯一 Planner stop：**
B2_P6_C1_C1_TEST_IMPORT_CORRECTION_WAITING_PLANNER_REVIEW。

**本轮新归档：**
`.agent-work/PLANS/20260731-1614-p7-retained-r3-b2-p6-c1-import-failure-review.md`；bytes `6568`，SHA-256
`07c4199a024e1f45d21b6f69ce62e478f5e575b1dd30464626fc2e978a12a01a`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p6_c1_c1_test_runtime_request_import_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P6-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-TEST-RUNTIME-REQUEST-IMPORT-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"e6520062bb1a60a0686066ccec39c4fb190905c0","expected_subject":"chore(plan): activate p6 c1 c1 test import correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1614-p7-retained-r3-b2-p6-c1-import-failure-review.md"],"clean_porcelain_required_after_activation":true},"rejected_candidate":{"commit":"73e2f2cc3b9b1465a47381b55360cf941ac0cbc4","consumable":false,"evidence_commit":"e6520062bb1a60a0686066ccec39c4fb190905c0","targeted_tests":8,"targeted_exit":1,"failures":0,"errors":1,"passed":7},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): import retained controller runtime request in tests","expected_changed_paths":["tests/test_p7_retained_r3_controller_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P6-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-TEST-RUNTIME-REQUEST-IMPORT-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","rejected_candidate_commit":"73e2f2cc3b9b1465a47381b55360cf941ac0cbc4","rejected_candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["tests/test_p7_retained_r3_controller_domain_template.py"],"correction_contract":{"runtime_owner_module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime","before_imported_names":["compose_controller_source"],"after_imported_names":["ControllerRuntimeRequest","compose_controller_source"],"explicit_import_required":true,"test_body_edits":0,"production_source_edits":0,"third_path_edits":0,"source_blob_immutable":"a1e196664840bc340be789829b8cf0826c9ec7f4","source_sha256_immutable":"56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032","preserve_exact_eight_test_names":true,"preserve_test08_semantic_body":true,"preserve_p6_source_and_runtime_shape":true},"regression_contract":{"targeted_expected":8,"focused_expected":90,"full_expected":775,"postcommit_targeted_expected":8},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"targeted_invocations":2,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"retry":0,"fallback":0},"zero_budgets":{"second_code_test_path_writes":0,"production_source_writes":0,"test_body_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P6_C1_C1_TEST_IMPORT_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 exact one-path scope

Activation direct parent、subject 与 exact three-path set必须匹配 machine row，之后 porcelain clean。FULL只允许 P6-C1-C1 active，明确
`73e2f2cc3b9b1465a47381b55360cf941ac0cbc4` 仍 rejected/non-consumable；retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`，device authorization false。

Executer唯一可写 code/test path：

`tests/test_p7_retained_r3_controller_domain_template.py`

不得修改 `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`、runtime、preparation、conformance、
provenance-I/O、lifecycle、validator、retained helper或任何第二 code/test path。若 activation drift、worktree非 clean或 correction需要扩大路径，
立即 fail closed append ER。

## 2. Exact import-only correction

当前 dedicated test 已从
`camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime` 导入 `compose_controller_source`。唯一允许的语义修改是在该既有 import
中同时显式导入 `ControllerRuntimeRequest`。最终 imported-name set exact 为
`ControllerRuntimeRequest` 与 `compose_controller_source`；不得使用 module wildcard、动态 import、alias、test-local import、fallback、try/except、
reflection或重复类型定义。

禁止修改任何 test method body、fixture、expected tuple/count、negative assertion、method name或 production source。Source必须保持 blob
`a1e196664840bc340be789829b8cf0826c9ec7f4`、bytes `13918`、SHA-256
`56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`。Import correction前 test identity为 blob
`d716f13cb31b26ac151d5b013c8ee989cbbae716`、bytes `12929`、SHA-256
`17a011c8234c0acbad9b3bc3a3f1a26ad13ec9de41d284f4a458a616347fd44c`。

## 3. Fresh ordered validation 与 commit

不得把 P6-C1 的失败 invocation或其中七项通过计入本包成功证据。Activation 后按顺序执行，retry/fallback exact `0/0`：

1. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`：exact `8/8`、exit `0`、`OK`；
2. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`：exact `90/90`、exit `0`、`OK`；
3. compileall exact domain-template source与 dedicated test，exit `0`；
4. unique full：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`：exact `775/775`、exit `0`、`OK`，记录唯一 unified session；
5. `codegraph sync` exact once；query test import→`ControllerRuntimeRequest` payload inventory与 builder→runtime request/preparation/analyzer test path，确认无第二 effect/lifecycle/analyzer owner；
6. `git diff --check`、exact one-path gate、exact eight-method gate、test-body unchanged gate、source identity unchanged gate与 exact imported-name gate；
7. 创建唯一 implementation commit，subject exact `fix(p7): import retained controller runtime request in tests`，changed path exact one test文件；
8. postcommit targeted fresh exact `8/8`、exit `0`、`OK`；
9. 仅向 `EXECUTION_RESULT.md` EOF append一次完整 handoff，停在 Planner review。

## 4. Acceptance、failure 与 hard locks

Acceptance要求：唯一 diff是既有 runtime-owner import加入 `ControllerRuntimeRequest`；production source identity、test bodies、八个方法与 P6
合同不变；fresh targeted8、focused90、compileall、unique full775、CodeGraph、diff/path/body/source/import gates、single test-only commit与
postcommit targeted8全部通过。Handoff必须记录 activation、rejected candidate、implementation commit/parent/subject/path、test final
blob/bytes/SHA、source immutable identity、所有 invocation/session/exit/count与 zero budgets。

任一检查失败即 fail closed：不 retry、不 fallback、不改 test body、不修改 production source或第二路径、不放宽 counts，不运行 generated
source/external controller/root，不读取 retained或旧 evidence；保留 code/evidence，append ER并停在唯一 Planner stop。

旧 failed controllers/roots/evidence、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、
eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
TD-C、sentinel、P8、firmware、deployment全部 hard locked 0。本包通过只证明 composite domain-template owner ready for Planner review，
不自动授权 synthetic integration。
