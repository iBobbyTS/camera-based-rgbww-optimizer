# REF-G4-06 materialized attestation owner-seam refactor and qualification

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_OWNER_SEAM_REFACTOR`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-OWNER-SEAM-REFACTOR-QUALIFICATION-V1`

**Reviewed disposition：** `REJECTED_MATERIALIZED_ATTESTATION_FOCUSED_SECOND_SUBSTANTIVE_OWNER_SEAM_FAILURE_BOUNDED_ENABLING_REFACTOR_REQUIRED`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-OWNER-SEAM-REFACTOR-QUALIFICATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_OWNER_SEAM_REFACTOR","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_MATERIALIZED_OWNER_SEAM_REFACTOR","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_WITH_SHARED_ACCEPTED_ENGINEERING_PREREQUISITE_OWNER","architecture_attempt":2,"architecture_attempt_increment":0,"same_boundary_substantive_failure_count":2,"prior_materialized_architecture_production_integration_failures":1,"current_substantive_production_failure_increment":1,"production_failure_count_after_review":2,"candidate_failure_increment":1,"production_retry_count":0,"candidate_retry_count":0,"full_invocation_count_before_current_plan":0,"full_retry_count":0,"controller_harness_invalid_event_count_since_v2":4,"third_same_boundary_failure_terminal":true,"continuation_class":"SAME_STABLE_REFERENCE_SECOND_FAILURE_MINIMAL_ENABLING_OWNER_SEAM_REFACTOR","reviewed_disposition":"REJECTED_MATERIALIZED_ATTESTATION_FOCUSED_SECOND_SUBSTANTIVE_OWNER_SEAM_FAILURE_BOUNDED_ENABLING_REFACTOR_REQUIRED","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-OWNER-SEAM-REFACTOR-QUALIFICATION-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_QUALIFICATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_OWNER_SEAM_REFACTOR"},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0230.md","bytes":4657,"sha256":"52c7392c33b77e965c3650560b3ab8281999f91ee31fb112859d49e8106c1bac"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0230.md","bytes":2445,"sha256":"d7483d5ef54a05dce0207789079b5ffd5e2df353fcc2b86c655dc5f18177a8a9"}},"frozen_intake":{"source_sha256":"f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d","test_sha256":"c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc","changed_lines":438,"hard_cap_before_correction":480},"reviewed_focused":{"tests":53,"exit":1,"failures":4,"errors":10,"duration_s":185.648,"log_bytes":30744,"log_sha256":"16945a869e1eab3b96ab70a6e14d77bd77563a7bfaf664a6feae2487e91caa9c","candidate_owned_non_green_manifestations":3,"stale_test_or_mock_manifestations":11,"substantive_owner_seam_failures":1},"single_current_action":"perform_minimal_shared_prerequisite_owner_refactor_update_all_confirmed_stale_tests_and_complete_one_qualification","executor_repo_write_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py",".agent-work/EXECUTION_RESULT.md"],"maximum_additional_changed_lines":160,"final_hard_changed_lines_cap":600,"targeted_invocation_cap":1,"stage_gate_focused_invocation_cap":1,"related_invocation_cap":1,"full_suite_invocation_cap":1,"full_suite_retry":0,"correction_cap":1,"new_task_suffix_allowed":false,"new_candidate_allowed":false,"parallel_identity_owner_allowed":false,"historical_candidate_input_allowed":false,"candidate_commit_by_executer":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_REVIEW"}`

## 1. Frozen intake, ownership and maintainability preflight

Orchestrator激活前必须将PLAN/FULL/PLAN-FULL精确同步至本contract并复位ER。Executer只能从当前working candidate继续；不得读取、复制、merge、cherry-pick或比较任何historical rejected implementation。

Intake必须确认source/test SHA分别为 `f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d`、`c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc`，当前diff为438 changed lines。只允许修改：

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_p7_td_b_r6_stage_gate.py`
- `.agent-work/EXECUTION_RESULT.md`

先用CodeGraph复核 `build_stage_gate_input → _validate_preparation_source_attestation` 与 `materialize_committed_source_attestation → validate_committed_source_attestation` 调用链。此模块是large coordinator；不得新增module、parallel runner、第二identity authority或宽泛ignore。最小enabling refactor总新增changed-lines上限160，最终diff hard cap 600。若无法在该范围内建立清晰单一owner，立即停止。

## 2. One bounded owner-seam correction

在同一stable reference内一次完成以下共同根因，不得拆成error-code corrective包：

1. 抽取一个内部、单一source-of-truth的 accepted-engineering prerequisite Git validator；preparation owner和post-commit validator必须复用它。
2. Preparation必须在任何package/root effect前验证accepted engineering的exact tree、direct parent、subject、changed paths、blob OIDs及其到verified parent的ancestry；不能只比较descriptor与binding互相一致。
3. Materializer必须先验证descriptor contract和accepted-engineering prerequisite，再查询/构造candidate commit identity；不得让candidate topology查询抢先遮蔽prerequisite stable error。
4. `changed_paths_between_checkpoints` 在accepted-engineering和code-owner/post-child seam的 `OSError`、`CalledProcessError`、`ValueError` 必须各自归一为既有精确stable StageGateError；不得裸逸出，也不得以一个泛化错误吞掉underlying seam。
5. 保持materialized identity为唯一post-commit authority；不恢复static subject/blob constants，不把descriptor、worktree hash和commit identity变成并列放行owner。
6. 不放宽exact parent、non-merge、changed paths、committed blobs、current candidate bytes、linear orchestration-only descendants、worktree scope或fail-closed顺序。

## 3. Test contract convergence and protective coverage

同步修正全部11个stale test/mock/error-priority表现，但只改变不可达或已过时的测试合同：

- invalid topology测试必须在正确owner处断言：materializer可直接拒绝无法materialize的parent/merge/path/lineage；仅identity tamper测试才先取得valid identity再修改字段。
- `P7TdBR6StageGateTests.future_activation`补齐v2的五个attestation字段并移除旧top-level identity aliases；继续证明所有backend/device callback未调用。
- old-descriptor测试必须把被篡改descriptor直接交给descriptor owner，使descriptor semantic guard可达；另保留current-candidate drift的独立覆盖。
- 将activation descendant冒充code owner的断言更新为精确 `committed_source_parent_drift`；不得把更精确fail-closed错误改回泛化binding code。
- accepted-engineering subject/path和query exception必须继续证明在root/backend effect前由共享prerequisite owner拒绝。

不得通过删除negative cases、放宽regex、mock掉production owner、跳过materializer/validator或仅让测试绿来接受候选。

## 4. Maximum safe continuous validation package

实现完成后在一个fresh `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-owner-seam-qualification-*` root中依次执行并完整封存：

1. 一次targeted：覆盖本review全部14个表现对应的test identities及新增shared-prerequisite/error-normalization保护断言；必须green。
2. 一次stage-gate focused：`.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_stage_gate`；必须自然退出且green。
3. 一次related thermal diagnostics + terminal focused；只允许精确既有 `tests.test_p7_thermal_diagnostics` governance-lineage baseline `2F+8E`，需要完整identities和first frames；不得有stage-gate/materialized/changed-owner/additional F/E。
4. `compileall`、repo-owned PLAN/FULL/PF parser、`git diff --check`、scope/cap、forbidden historical/package/device scan。
5. `codegraph sync`及post-sync query，证明共享prerequisite owner只有一个，preparation/materializer/validator调用链无parallel authority。
6. 冻结source/test mode、bytes、SHA、diff和path set。
7. 唯一full discovery自然退出，invocation/retry `1/0`。接受仅为全绿，或精确上述unrelated governance baseline `2F+8E`；任何source/test/stage-gate/materialized/new F/E均立即拒绝。
8. 记录完整argv、环境、start/end、exit、duration、test counts、日志bytes/SHA、cleanup、process/automation 0及ER handoff。

本PLAN内只有一次correction budget。Harness封装错误可在运行测试前修正命令，但不得修改source/test；一旦任何有效test non-green，不得修改候选或重跑。若再次证明同一accepted-engineering/materialization owner seam substantive failure，即为第三次，必须terminal fail closed。

若full预计超过10分钟，使用visible macOS Terminal、三次稀疏liveness及automation规则；不得按progress字符提前终止。

## 5. Acceptance and stop

接受需要：共享prerequisite owner真实存在且两条调用链复用；14个review表现均有精确归因和保护；targeted/focused通过；related/full全绿或仅exact unrelated baseline；static/CodeGraph/diff/scope通过；无external effect。

Executer不得commit。完成或任一有效gate失败后停在：

`RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_REVIEW`

Planner接受后才允许Orchestrator建立focused code checkpoint及read-only post-commit attestation probe。Package preparation仍需后续独立PLAN。

## 6. Hard locks

GUIDE/RESEARCH immutable；Human goal/Guide/science未完成；retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。Package prepare/describe/root、formal、release、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C全部false。不得commit/push/PR，不得创建task suffix、new candidate、alternate root family或parallel semantic owner。
