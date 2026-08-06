# REF-G4-06 materialized commit attestation zero-write qualification

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ZERO_WRITE_QUALIFICATION`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ZERO-WRITE-QUALIFICATION-V1`

**Reviewed disposition：** `ACCEPTED_CONTROLLED_INVALID_TARGETED_CLASS_IDENTITY_INVOCATION_NO_TEST_EXECUTION_NO_CANDIDATE_FAILURE`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ZERO_WRITE_QUALIFICATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ZERO-WRITE-QUALIFICATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ZERO_WRITE_QUALIFICATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_ZERO_WRITE_QUALIFICATION","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","architecture_attempt":2,"architecture_attempt_increment":0,"prior_materialized_architecture_production_integration_failures":1,"production_failure_increment_from_invalid_invocation":0,"production_retry_count":0,"candidate_retry_count":0,"full_retry_count":0,"continuation_class":"SAME_CANDIDATE_ZERO_WRITE_QUALIFICATION_ONLY","reviewed_disposition":"ACCEPTED_CONTROLLED_INVALID_TARGETED_CLASS_IDENTITY_INVOCATION_NO_TEST_EXECUTION_NO_CANDIDATE_FAILURE","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ZERO-WRITE-QUALIFICATION-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_ATTESTATION_ZERO_WRITE_QUALIFICATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ZERO_WRITE_QUALIFICATION"},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0203.md","bytes":3244,"sha256":"49848ae2fe20f8ec800aeefb136c6212018e417a9c33bfb4d22b8c30728a26d7","source_bytes":10732,"source_sha256":"3f60d4bfde4a77e5d8ba843094fd2a0ab9af6cfd77c6d319a9ba93f7e5c7df87"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0203.md","bytes":2290,"sha256":"419f4f71b1491a1b7460b77055bce9b0071b9becff24825c4c7a15d90c8a4b79","source_bytes":6552,"source_sha256":"2808c5aa92cc7d3c83ddfddb5cb7363f6f91d759145687159f02326ed251b143"}},"frozen_candidate":{"source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","mode":420,"bytes":105150,"sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d"},"test":{"path":"tests/test_p7_td_b_r6_stage_gate.py","mode":420,"bytes":151231,"sha256":"c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc"},"changed_lines":438,"hard_cap":480},"single_current_action":"run_the_complete_zero_write_candidate_qualification_using_exact_current_source_test_identities","executor_repo_write_paths":[".agent-work/EXECUTION_RESULT.md"],"production_source_write_cap":0,"test_source_write_cap":0,"fixture_correction_remaining":0,"harness_correction_remaining":0,"production_correction_remaining":0,"new_task_suffix_allowed":false,"new_candidate_allowed":false,"alternate_candidate_or_root_allowed":false,"historical_candidate_input_allowed":false,"candidate_commit_by_executer":false,"exact_targeted_test_class":"P7TdBR6StageGateTests","exact_targeted_test_methods":["test_planned_subject_real_topology_binds_exact_two_committed_blobs","test_production_cli_seam_loads_materializes_and_delegates_exactly_once","test_measure_cli_routes_exact_stage_gate_chain_and_rejects_generic_bypass","test_committed_source_attestation_accepts_code_child_and_agent_work_descendants"],"targeted_invocation_cap":1,"stage_gate_focused_invocation_cap":1,"related_invocation_cap":1,"full_suite_invocation_cap":1,"full_suite_retry":0,"allowed_full_non_green_baseline":{"failures":2,"errors":8,"test_module":"tests.test_p7_thermal_diagnostics","classification":"CURRENT_AGENTS_GOVERNANCE_LINEAGE_IDENTITY_GROUP","exact_test_identities_required":true,"exact_first_failing_frames_required":true,"stage_gate_failure_allowed":false,"materialized_attestation_failure_allowed":false,"changed_owner_failure_allowed":false,"additional_failure_or_error_allowed":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ZERO_WRITE_QUALIFICATION_REVIEW"}`

## 1. Frozen intake and zero-write boundary

Orchestrator激活前同步PLAN/FULL/PLAN-FULL至本contract并reset live ER。Executer必须验证machine state `1/1/1`及下列candidate identity：

- source：105150 bytes、mode `0644`、SHA-256 `f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d`；
- test：151231 bytes、mode `0644`、SHA-256 `c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc`；
- diff：438 changed lines，hard cap 480。

本PLAN对production和test写入均为0；唯一repo写路径是 `.agent-work/EXECUTION_RESULT.md`。任何source/test byte、mode、diff或third path变化立即停止。Historical rejected implementation/diff/tree/blob/file禁止读取或复用。

错误类名invocation执行tests为0，只是无效证据；不增加architecture/candidate/production/harness/full retry计数。本PLAN不是新candidate、suffix、retry或corrective implementation。

## 2. Exact targeted identities

Targeted只允许一次，必须使用current test source已核实的exact class：

`tests.test_p7_td_b_r6_stage_gate.P7TdBR6StageGateTests`

及以下四个exact methods：

1. `test_planned_subject_real_topology_binds_exact_two_committed_blobs`
2. `test_production_cli_seam_loads_materializes_and_delegates_exactly_once`
3. `test_measure_cli_routes_exact_stage_gate_chain_and_rejects_generic_bypass`
4. `test_committed_source_attestation_accepts_code_child_and_agent_work_descendants`

命令seal前必须只读核对这四个qualified identities存在；不得从手写缩写推断类名。若identity不匹配，停止，不更正命令、不重跑。

## 3. Maximum-continuous qualification

按顺序执行，每项在ER记录exact argv、count、duration、exit和evidence bytes/SHA：

1. exact targeted group，要求4/4 green；
2. entire `tests.test_p7_td_b_r6_stage_gate` focused，要求全部green；
3. related thermal diagnostics与terminal focused；只允许逐项匹配current-AGENTS governance-lineage exact `2F+8E` group，无stage-gate/materialized/changed-owner或额外F/E；
4. compileall/static、`git diff --check`、scope/cap、forbidden historical/package/device scan；
5. `codegraph sync`及post-sync call-chain query；candidate source/test SHA必须仍匹配frozen values；
6. 记录final identity freeze；
7. 唯一full unittest discovery，invocation/retry `1/0`。接受仅为green，或exact `2F+8E`且test identities与first failing frames逐项匹配 `tests.test_p7_thermal_diagnostics` current-AGENTS group；任何其他F/E拒绝；
8. cleanup、scratch inventory、process/automation 0和ER handoff。

任一gate non-green立即停止；所有harness/production/test correction和rerun预算为0。不得拆包或把targeted/focused green代替full acceptance。

只可fresh创建一个 `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-zero-write-qualification-*` validation evidence root；不得读取existing package/formal/experiment roots。单命令预计超过10分钟时按visible Terminal、三次稀疏liveness与Orchestrator automation规则执行。

## 4. Acceptance and stop

接受要求：candidate全程byte-for-byte frozen；targeted和stage-gate focused green；related/full green或仅exact governance baseline；compile/static/CodeGraph/diff/scope通过；无historical/package/formal/release/device/network effects。

Executer不得commit。ER完成后停在：

`RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ZERO_WRITE_QUALIFICATION_REVIEW`

Planner接受后才由Orchestrator创建exact code checkpoint并执行一次read-only post-commit attestation probe；package preparation仍需后续独立PLAN。

## 5. Hard locks

- GUIDE/RESEARCH immutable；Human goal、GUIDE、scientific stage未完成；retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- Package prepare/describe/replay/probe/root、formal/replacement formal、release、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C全部false。
- Executer不得修改source/test/PLAN/FULL/PLAN-FULL/archive/debug/config/wrapper/GUIDE/RESEARCH，不得commit/push/PR。
