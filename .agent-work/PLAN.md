# REF-G4-06 materialized commit attestation qualification continuation

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-QUALIFICATION-CONTINUATION-V1`

**Reviewed disposition：** `REJECTED_TARGETED_AS_QUALIFICATION_RESULT_ACCEPTED_HARNESS_ACCOUNTING_CONTINUATION_NO_PRODUCTION_FAILURE`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_QUALIFICATION_CONTINUATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-QUALIFICATION-CONTINUATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_QUALIFICATION_CONTINUATION","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","architecture_attempt":2,"architecture_attempt_increment":0,"prior_materialized_architecture_production_integration_failures":1,"production_failure_increment_from_reviewed_targeted":0,"production_retry_count":0,"reviewed_disposition":"REJECTED_TARGETED_AS_QUALIFICATION_RESULT_ACCEPTED_HARNESS_ACCOUNTING_CONTINUATION_NO_PRODUCTION_FAILURE","continuation_class":"SAME_CANDIDATE_HARNESS_ACCOUNTING_CONTINUATION_NOT_NEW_ARCHITECTURE_ATTEMPT","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-QUALIFICATION-CONTINUATION-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_ATTESTATION_QUALIFICATION_CONTINUATION"},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0152.md","bytes":3638,"sha256":"f31c1661894e1f9a072e4e727962e021b65b227a5c8d8bc53551dfbdad166712","source_bytes":12909,"source_sha256":"23f69b8f34b99f94ef152e2a1fcd5b49d4328de67bebc97d95e32c932d66b52c"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0152.md","bytes":2880,"sha256":"1af558a51dccd8cd64c4e83af2324e674bc8b853534b5e9dfc9add5bcbc33977","source_bytes":6405,"source_sha256":"5775632ef2df1ff955e1519aef421d734b24403d2a97c5a54c6481d0ae14a1ba"}},"candidate_identity_at_review":{"source_path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","source_bytes":105150,"source_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","source_mode":420,"test_path":"tests/test_p7_td_b_r6_stage_gate.py","test_bytes":151167,"test_sha256":"372a70f9a33b7494181aab1bb0c29db49e6c6dcbe4ba06fd308d16f9ef62abe3","test_mode":420,"changed_lines":434,"hard_cap":480},"single_current_action":"correct_the_exact_stale_test_fixture_call_shape_then_run_the_complete_remaining_candidate_qualification_without_production_mutation","executor_repo_write_paths":["tests/test_p7_td_b_r6_stage_gate.py",".agent-work/EXECUTION_RESULT.md"],"production_source_frozen_path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","production_source_frozen_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","production_source_write_cap":0,"test_fixture_contract_correction_cap":1,"test_fixture_exact_change":"pass_the_materialized_attestation_identity_not_the_complete_activation_mapping_to_validate_committed_source_attestation","harness_correction_consumed":1,"harness_correction_remaining":0,"production_correction_after_activation_cap":0,"new_module_or_controller_allowed":false,"third_production_or_test_path_allowed":false,"new_task_suffix_allowed":false,"new_candidate_allowed":false,"alternate_candidate_or_root_allowed":false,"historical_candidate_input_allowed":false,"candidate_commit_by_executer":false,"hard_changed_lines_cap":480,"targeted_required":true,"stage_gate_focused_required":true,"related_required":true,"compile_static_required":true,"codegraph_sync_query_required":true,"identity_freeze_required":true,"full_suite_invocation_cap":1,"full_suite_retry":0,"allowed_full_non_green_baseline":{"failures":2,"errors":8,"test_module":"tests.test_p7_thermal_diagnostics","classification":"CURRENT_AGENTS_GOVERNANCE_LINEAGE_IDENTITY_GROUP","exact_test_identities_required":true,"exact_first_failing_frames_required":true,"stage_gate_failure_allowed":false,"materialized_attestation_failure_allowed":false,"changed_owner_failure_allowed":false,"additional_failure_or_error_allowed":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_QUALIFICATION_CONTINUATION_REVIEW"}`

## 1. Intake and frozen candidate

Orchestrator激活前必须同步PLAN/FULL/PLAN-FULL到本contract并reset live ER。Executer intake验证branch、activation HEAD、machine state `1/1/1`及当前candidate identities。

Production source已通过production CLI和measure CLI targeted传播验证，冻结为：

- path `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- mode `0644`
- bytes `105150`
- SHA-256 `f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d`

本PLAN中production source write cap为0。任何source变化、production语义修复需求或第三路径需求都立即停止。

当前test身份为151167 bytes、SHA-256 `372a70f9a33b7494181aab1bb0c29db49e6c6dcbe4ba06fd308d16f9ef62abe3`；唯一授权实现写入是把旧positive fixture调用从完整activation mapping改为其中的materialized attestation identity。不得改变production expected code、validator、其他fixture语义或放宽断言。

Historical Q1/Section2/v1/v2 rejected implementation及diff/tree/blob/file仍禁止读取、复制或复用。

## 2. Accounting and scope

这是same candidate的harness-accounting continuation：architecture attempt保持2，production substantive failure总数保持1，production retry为0；不创建task suffix、Q3、新candidate、alternate identity/root或新owner。

先前zsh readonly `status` wrapper错误已消耗harness correction `1/1`。本PLAN只授权上述一个明确test fixture contract correction；之后harness、test、production correction剩余均为0。Candidate changed-lines hard cap保持480。

唯一repo写路径：

- `tests/test_p7_td_b_r6_stage_gate.py`
- `.agent-work/EXECUTION_RESULT.md`

## 3. Maximum-continuous qualification package

完成fixture correction后不得再拆包，按顺序执行：

1. 重跑包含materialized topology、production CLI、measure CLI及positive descendant的完整targeted group，要求全部green。
2. 运行整个 `tests.test_p7_td_b_r6_stage_gate` focused，要求全部green。
3. 运行相关thermal diagnostics与terminal focused；仅允许逐项匹配既有current-AGENTS governance-lineage `2 failures + 8 errors` group，不得有stage-gate/materialized/changed-owner或额外F/E。
4. 运行final compileall/static、`git diff --check`、exact scope/changed-line cap、forbidden historical/package/device scan。
5. 运行 `codegraph sync` 与post-sync query，证明materialized owner、production activation、production CLI和measure CLI仍为单一完整调用链；source SHA必须仍等于冻结值。
6. 冻结最终source/test path、mode、bytes、SHA-256和diff stats；冻结后禁止任何写入。
7. 对冻结candidate运行唯一full unittest discovery，budget/retry `1/0`。接受仅为完全green，或exact `2F+8E` 且全部test identities与first failing frames匹配 `tests.test_p7_thermal_diagnostics` current-AGENTS group；不得有任何stage-gate/materialized/changed-owner/additional F/E。
8. 记录cleanup、scratch inventory/identity、process/automation 0及完整ER handoff。

任何gate non-green立即停止；不得修正、重跑、换root或把targeted green当作acceptance。单命令预计超过10分钟时使用visible Terminal、三次稀疏liveness与Orchestrator automation规则。

Validation scratch只可fresh创建一个 `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-qualification-*` evidence root；它不是candidate/package/formal root，不得读取已有external roots。

## 4. Acceptance and stop

Planner接受要求：fixture correction exact；production source frozen unchanged；scope/cap通过；targeted和stage-gate focused green；related/full green或仅exact governance baseline；compile/static/CodeGraph/diff通过；无historical/package/formal/release/device/network effects。

Executer不得commit。ER必须报告每项命令/count/duration/exit/evidence bytes/SHA、final source/test identity、full invocation/retry及zero-effect ledger，然后停在：

`RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_QUALIFICATION_CONTINUATION_REVIEW`

Planner接受后才由Orchestrator创建exact code checkpoint并运行一次read-only post-commit attestation probe；package preparation仍锁定并需后续独立PLAN。

## 5. Hard locks

- GUIDE/RESEARCH immutable；Human goal、GUIDE、scientific stage未完成；retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- Package prepare/describe/replay/probe/root、formal/replacement formal、release、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C权限全部false。
- Executer不得修改source/PLAN/FULL/PLAN-FULL/archive/debug/config/wrapper/GUIDE/RESEARCH，不得commit/push/PR。
