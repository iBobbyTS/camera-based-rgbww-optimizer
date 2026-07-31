# REF-P7-25-R2-B2-P6-C1-C1-C1-V1：deterministic validation-only closure

**计划状态：** WAITING_ORCHESTRATOR_ACTIVATION

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1-C1-C1-V1

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-V1-DETERMINISTIC-VALIDATION-CLOSURE-V1

**Planner decision：** P6-C1-C1-C1 at evidence HEAD
`2fc509b02fd8be0fee05653e5875709f0d05a141` is
`REJECTED_POST_FULL_VALIDATION_HARNESS_STOPITERATION_CANDIDATE_REGRESSION_GREEN_NON_CONSUMABLE`。
The exact candidate `48b3979d6c0df5f488cd500597e26dc4c38877dd` passed fresh targeted `8/8`, focused `90/90`,
compileall, unique full `775/775`, and CodeGraph, but a temporary combined AST gate raised `StopIteration`; retry `0` and
no implementation commit were correct. Independent review verifies the candidate's exact one-path topology and that
deterministic selection of the real test08 followed by `ast.walk(selected_test08)` finds the unique literal
`generated_calls` assignment. No code/test correction is authorized.

**当前唯一动作：** Orchestrator审核、更新 FULL，并以 clean evidence HEAD
`2fc509b02fd8be0fee05653e5875709f0d05a141` 为 direct parent创建 exact activation commit。Activation后，Executer
只对已提交 candidate `48b3979d...` 执行 frozen deterministic static gate与一轮 fresh validation，writes exact
`.agent-work/EXECUTION_RESULT.md` EOF append one；code/test writes与implementation commit均为 `0`。

**唯一 Planner stop：**
B2_P6_C1_C1_C1_V1_DETERMINISTIC_VALIDATION_CLOSURE_WAITING_PLANNER_REVIEW。

**本轮新归档：**
`.agent-work/PLANS/20260731-1634-p7-retained-r3-b2-p6-c1-c1-c1-harness-failure-review.md`；bytes `6389`，
SHA-256 `db6545c82e4be051c4536d0cd2e47fcf8f0f6b4f3ff62c5117f59a4ffec3c6ad`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p6_c1_c1_c1_v1_deterministic_validation_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P6-C1-C1-C1-V1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-V1-DETERMINISTIC-VALIDATION-CLOSURE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"2fc509b02fd8be0fee05653e5875709f0d05a141","expected_subject":"chore(plan): activate p6 validation harness closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1634-p7-retained-r3-b2-p6-c1-c1-c1-harness-failure-review.md"],"clean_porcelain_required_after_activation":true},"candidate":{"commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","parent":"478d8c52e4a21d6628219e27b88b507d736f3aca","subject":"chore(p7): retain rejected p6 c1 c1 c1 guard candidate","changed_paths":["tests/test_p7_retained_r3_controller_domain_template.py"],"diff_numstat":{"insertions":2,"deletions":2},"canonical_binary_diff_sha256":"96a38decb6664fec7f5744f568ddad86b7c206d969452a458ddff854881da781","regression_green":true,"consumable_before_planner_acceptance":false},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P6-C1-C1-C1-V1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-V1-DETERMINISTIC-VALIDATION-CLOSURE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","candidate_consumable":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_code_test_write_paths":[],"exact_execution_write_paths":[".agent-work/EXECUTION_RESULT.md"],"identity_contract":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob":"a1e196664840bc340be789829b8cf0826c9ec7f4","source_bytes":13918,"source_sha256":"56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob":"eb943384817996b96e332c83f618ba82cf210d4a","test_bytes":12992,"test_sha256":"6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc"},"ast_gate_contract":{"class_name":"ControllerDomainTemplateTests","test_method_name":"test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner","assignment_name":"generated_calls","selection":"exact_name_then_ast_walk","assignment_count":1,"runtime_imports":["ControllerRuntimeRequest","compose_controller_source"],"test_method_count":8,"test_method_names":["test_01_identical_spec_builds_frozen_byte_exact_bundle","test_02_placeholder_replacement_is_unique_adjacent_and_canonical","test_03_runtime_request_inputs_are_exact_and_compose_without_effect","test_04_existing_analyzer_accepts_golden_eighteen_binding_report","test_05_single_physical_root_chain_and_seven_reads_have_exact_shape","test_06_git6_matrix16_exact9_and_lifecycle_inventory_is_frozen","test_07_invalid_specs_and_literal_values_fail_closed_with_stable_codes","test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner"],"generated_calls":["ByteSpan","DirectoryIdentity","FileIdentity","LifecycleCallbacks","LifecycleRequirements","RootIdentityChain","RuntimeError","SealTargetIdentity","create_exclusive_root","execute_controller_lifecycle","len","persist_canonical_json","read_exact_file","require_activation_contract","run_read_only_git","type","validate_root_identity_chain"]},"regression_contract":{"targeted_expected":8,"focused_expected":90,"full_expected":775},"execution_budgets":{"deterministic_static_gate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":0,"codegraph_queries":1,"implementation_commits":0,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"implementation_commits":0,"postcommit_targeted":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P6_C1_C1_C1_V1_DETERMINISTIC_VALIDATION_CLOSURE_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen candidate gate

Activation direct parent、subject与 exact three-path set必须匹配 machine row，之后 porcelain clean。FULL只允许本 V1
task active，retained R3必须保持 `RETAINED_UNVALIDATED_UNCONSUMED`，candidate `48b3979d...`必须保持
non-consumable，device authorization false。

在任何 Python validation前，用 allowlisted read-only Git核对：

- candidate exact full commit、direct parent、subject；
- candidate changed path exact one test path，numstat exact `2/2`；
- candidate binary diff SHA-256 exact machine row；
- source/test blob、bytes与working-tree SHA-256 exact machine row；
- activation后的 code/test porcelain clean。

任一不匹配立即 fail closed，只append ER。不得修改、amend、rebase、cherry-pick、重建或重新提交 candidate。

## 2. Deterministic static gate

运行 exact one inline/read-only Python AST gate。它必须：

1. strict UTF-8读取 exact dedicated test，parse AST；
2. exact-name选择 class `ControllerDomainTemplateTests`，且数量 exact one；
3. exact-name选择真实 test08 `test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner`，且数量 exact one；
4. 从该 selected test08使用 `ast.walk(selected_test08)` 查找 target含 Name `generated_calls` 的 `ast.Assign`，要求
   exact one；不得依赖 `method.body`位置、固定 statement index、substring method match或首个任意 assignment；
5. 对 value运行 `ast.literal_eval`，要求 exact `set[str]`且内容等于 machine row的 `generated_calls`；
6. 从 module top-level exact runtime-owner `ImportFrom`核对 imported names exact
   `ControllerRuntimeRequest`、`compose_controller_source`；
7. 核对 exact八个 test method names、source/test identities与 only-candidate-path topology；
8. 明确证明两个 added names为 exact `RuntimeError`和`type`，不接受 wildcard、prefix、regex、动态 inventory-derived
   allowlist或 generic builtin allowance。

Gate invocation exact `1`。失败不得修复或重跑；append ER并停。

## 3. Fresh ordered independent closure

Static gate通过后，按顺序执行一次；不得把前包通过计入本包：

1. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`：exact `8/8`、exit `0`、`OK`；
2. `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`：exact `90/90`、exit `0`、`OK`；
3. compileall exact domain-template source与 dedicated test：exit `0`；
4. unique full：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`：exact
   `775/775`、exit `0`、`OK`，记录唯一 unified session；
5. 不运行 `codegraph sync`：candidate working-tree bytes已经在上一包唯一 sync中得到 `Already up to date`，本包无
   code/test write；运行 exact one query，核对 domain template/test08到 runtime composition/conformance/lifecycle owner，
   无第二 effect/lifecycle/analyzer owner；
6. 再核对 worktree除允许的最终 ER append前无变化、source/test identities仍 exact；
7. 不 stage、不创建 implementation commit；仅向 `.agent-work/EXECUTION_RESULT.md` EOF append一次 validation-only
   handoff，停在 Planner review。

Retry/fallback exact `0/0`。任何一项失败都不得补脚本、修 code/test、重复命令、降低 counts或改变 candidate身份。

## 4. Acceptance, failure and hard locks

Acceptance要求 deterministic gate、fresh targeted8、focused90、compileall、unique full775、CodeGraph query、final identity/
porcelain gates全部通过；code/test writes `0`、implementation commit `0`、ER append exact one。结果只能报告
`validation_only_candidate_ready_waiting_for_planner_review`，candidate在 Planner接受前仍 non-consumable。

任一检查失败即报告 validation-only failure，保留 exact evidence，不修复、不retry、不fallback，停在唯一 Planner stop。

External controller/root/source、synthetic integration、old failed evidence、retained R3/candidate payload、Git provenance replay、
real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、
credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment
全部 hard locked `0`。本包绝不授权 retained consumption、synthetic integration或任何后续 scientific/device stage。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1634-p7-retained-r3-b2-p6-c1-c1-c1-harness-failure-review.md","bytes":6389,"sha256":"db6545c82e4be051c4536d0cd2e47fcf8f0f6b4f3ff62c5117f59a4ffec3c6ad"}`
