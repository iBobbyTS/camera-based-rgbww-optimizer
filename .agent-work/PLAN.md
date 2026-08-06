# REF-G4-06 materialized attestation natural-exit qualification

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_NATURAL_EXIT_QUALIFICATION`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-NATURAL-EXIT-QUALIFICATION-V1`

**Reviewed disposition：** `ACCEPTED_TARGETED_GREEN_REJECTED_FOCUSED_HANDOFF_AS_CONTROLLER_EARLY_TERMINATION_EVIDENCE_INCOMPLETE_NO_CANDIDATE_FAILURE`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-NATURAL-EXIT-QUALIFICATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_NATURAL_EXIT_QUALIFICATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_NATURAL_EXIT_QUALIFICATION","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","architecture_attempt":2,"architecture_attempt_increment":0,"prior_materialized_architecture_production_integration_failures":1,"production_failure_increment":0,"candidate_failure_increment":0,"production_retry_count":0,"candidate_retry_count":0,"full_retry_count":0,"controller_harness_invalid_event_count_current_handoff":2,"controller_harness_invalid_event_count_since_v2":4,"harness_correction_consumed":1,"harness_correction_remaining":0,"continuation_class":"SAME_CANDIDATE_ZERO_WRITE_NATURAL_EXIT_QUALIFICATION","reviewed_disposition":"ACCEPTED_TARGETED_GREEN_REJECTED_FOCUSED_HANDOFF_AS_CONTROLLER_EARLY_TERMINATION_EVIDENCE_INCOMPLETE_NO_CANDIDATE_FAILURE","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-NATURAL-EXIT-QUALIFICATION-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_NATURAL_EXIT_QUALIFICATION"},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0214.md","bytes":3434,"sha256":"5c1b4dd50301a82af319e84aac5f9240ec4ffbee6710f8af5b88375466baa1ab","source_bytes":9717,"source_sha256":"4b47db38cec33bc7f57b4f60a527eb0c2de4fe3faf310971ef0b3fa42cab78e4"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0214.md","bytes":2012,"sha256":"279ed3c269e37d3b8ef586d025ae64d5f2366630749fe698f44d9f4e12f7a166","source_bytes":5899,"source_sha256":"dc1c3e70a8fbeb4e09837373cfac0bb36086e41a2f1ff25ea543f201e1400754"}},"frozen_candidate":{"source_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","test_sha256":"c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc","changed_lines":438,"hard_cap":480,"source_write_cap":0,"test_write_cap":0},"inherited_targeted":{"tests":4,"exit":0,"duration_s":8.410,"log_bytes":123,"log_sha256":"f7d767b7b33d8e95477855ebbd1ab328dc617bd780a4d87b8df39b0290346f2a","rerun_allowed":false},"invalid_focused_evidence":{"process_invocation_count":1,"natural_exit_count":0,"log_bytes":23,"log_sha256":"8a2c1d1a2680ad47d97e22e8e10f9c24a4e379210bf603bb2e98e88f40c9b201","candidate_failure_credit":false},"single_current_action":"obtain_the_first_natural_verbose_fully_sealed_focused_result_then_complete_remaining_zero_write_qualification","executor_repo_write_paths":[".agent-work/EXECUTION_RESULT.md"],"production_source_write_cap":0,"test_source_write_cap":0,"all_correction_remaining":0,"targeted_rerun_allowed":false,"stage_gate_focused_natural_exit_invocation_cap":1,"stage_gate_focused_semantic_retry":0,"related_invocation_cap":1,"full_suite_invocation_cap":1,"full_suite_retry":0,"zsh_status_variable_allowed":false,"progress_character_termination_allowed":false,"natural_exit_required_for_failure_attribution":true,"full_traceback_required_for_failure_attribution":true,"allowed_full_non_green_baseline":{"failures":2,"errors":8,"test_module":"tests.test_p7_thermal_diagnostics","classification":"CURRENT_AGENTS_GOVERNANCE_LINEAGE_IDENTITY_GROUP","exact_test_identities_required":true,"exact_first_failing_frames_required":true,"stage_gate_failure_allowed":false,"materialized_attestation_failure_allowed":false,"changed_owner_failure_allowed":false,"additional_failure_or_error_allowed":false},"new_task_suffix_allowed":false,"new_candidate_allowed":false,"alternate_candidate_or_root_allowed":false,"historical_candidate_input_allowed":false,"candidate_commit_by_executer":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION_REVIEW"}`

## 1. Frozen zero-write intake

Orchestrator激活前同步PLAN/FULL/PLAN-FULL至本contract并reset ER。Executer必须验证source/test SHA分别为 `f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d`、`c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc`，diff `438/480`。

Production/test write cap均为0；唯一repo写路径是ER。任何candidate byte/mode/diff变化立即停止。不得读取historical rejected implementation或其他existing external root。

继承targeted 4/4、8.410s、`OK`；不得重跑。23-byte focused progress log被SIGTERM截断，不具有candidate failure credit。

## 2. Exact natural-exit focused command and seal

Stage-gate focused只允许一次first valid natural completion：

`.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_stage_gate`

Runner/seal必须满足：

1. 合并保存完整stdout/stderr；使用 `command_exit_code` 等普通变量，禁止读取或赋值zsh special readonly `status`；
2. 记录exact argv、environment、start/end UTC、PID/TTY（适用时）、natural exit code、duration、log bytes/SHA；
3. 不得根据 `. F E` progress characters、部分计数或elapsed time发送SIGTERM/INT/KILL；
4. 必须等待natural exit。若预计超过10分钟，使用visible Terminal、三次稀疏liveness与automation，但liveness不得改变进程；
5. 只有包含exact test identities、完整tracebacks、final `Ran N tests` summary与natural exit的log才可归因non-green；crash/signal/truncated log一律归为invalid harness evidence并停止，不计candidate failure。

若natural focused non-green，立即停止，无修正/重跑。若green，连续进入后续gate。

## 3. Remaining maximum-continuous qualification

1. Related thermal diagnostics+terminal focused，一次；仅允许逐项匹配current-AGENTS exact governance `2F+8E`，无stage-gate/materialized/changed-owner/additional F/E。
2. Compileall/static、`git diff --check`、scope/cap与forbidden historical/package/device scan。
3. `codegraph sync`及post-sync call-chain query；复核frozen candidate SHA。
4. Final identity freeze。
5. 唯一full discovery使用verbose natural-exit seal，invocation/retry `1/0`；不得因progress字符提前终止。接受仅为green或exact governance `2F+8E` with exact identities/first frames，无其他F/E。
6. 记录cleanup、scratch inventory、process/automation 0和ER handoff。

所有correction预算为0。任一有效gate non-green立即停止；无效/truncated evidence也停止，不更正命令或重跑。

只可fresh创建一个 `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-natural-exit-qualification-*` validation evidence root；不得读取本轮旧root或任何package/formal/experiment root。

## 4. Acceptance and stop

接受要求：candidate全程frozen；inherited targeted及natural focused有效；related/full green或仅exact governance baseline；static/CodeGraph/diff/scope通过；无external effect。

Executer不得commit，完成后停在：

`RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_NATURAL_EXIT_QUALIFICATION_REVIEW`

Planner接受后才由Orchestrator创建exact code checkpoint并做一次read-only post-commit attestation probe；package preparation仍需后续PLAN。

## 5. Locks

GUIDE/RESEARCH immutable；Human goal/Guide/science未完成；retained R3未消费。Package/formal/release/device/network/camera/Ray/strip/capture/light/analysis/G4-07/TD-C全部false。Executer不得修改source/test/PLAN/FULL/PF/archive/debug/config/wrapper或commit/push/PR。
