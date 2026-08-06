# REF-G4-06 materialized commit attestation bounded second engineering package

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V2`

**Planner disposition on reviewed candidate：** `REJECTED_MATERIALIZED_COMMIT_ATTESTATION_V1_PRODUCTION_ACTIVATION_SEAM_NOT_PROPAGATED`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V2","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_PRESERVES_REJECTED_V1_RESTORES_ACCEPTED_TREE_AND_ALIGNS_MACHINE_STATE","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","architecture_attempt":2,"prior_materialized_architecture_production_integration_failures":1,"cross_architecture_third_failure":false,"reviewed_disposition":"REJECTED_MATERIALIZED_COMMIT_ATTESTATION_V1_PRODUCTION_ACTIVATION_SEAM_NOT_PROPAGATED","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V2","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2"},"accepted_restart":{"checkpoint":"7a7a3a9800af610a00d47c7cc635a066a7126555","accepted_owner_checkpoint":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","rejected_v1_input_allowed":false},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260806-0135.md","bytes":3557,"sha256":"7a1352a1ce0db10ae7adce0afedd39df0f0bd8fca27ba6a2535e31ba26695159","source_bytes":13814,"source_sha256":"dfaa93c29203bfcffd41a5a7f77bfe2fa65fdabb3ae64edd56e92d40316c3af2","supersedes":{"path":".agent-work/archived/PLAN-20260806-0131.md","bytes":4547,"sha256":"e0b682c88e1a9272c57770656a0483865b50e2c08a075839be6d8d3a9581284c","reason":"LF_EOF_ARCHIVE_FORMAT_CORRECTION_ONLY","historical_immutable":true}},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260806-0131.md","bytes":3839,"sha256":"4c5c1a708290feeb877d88a672737559c9006f53f9577212d73615d58e512414","source_bytes":7181,"source_sha256":"f45a680a0d4d53c4341789bbb0b17966b42ae6644717ebe5eac0288e67fd3572"}},"single_current_action":"independently_implement_the_complete_materialized_identity_owner_and_propagate_it_through_all_production_activation_and_cli_callers_then_run_final_qualification","executor_repo_write_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py",".agent-work/EXECUTION_RESULT.md"],"third_production_or_test_path_allowed":false,"new_module_allowed":false,"new_controller_allowed":false,"parallel_identity_authority_allowed":false,"rejected_candidate_input_allowed":false,"historical_candidate_input_allowed":false,"candidate_commit_by_executer":false,"unborn_commit_proof_required":false,"production_activation_materialized_identity_required":true,"production_cli_and_measure_cli_regression_required":true,"future_package_binding_in_current_plan":false,"expected_changed_lines_min":260,"expected_changed_lines_max":440,"hard_changed_lines_cap":480,"large_change_branch":"codex/g4-r6-owner-alignment-large-change","large_change_plan_full_section":"MATERIALIZED_COMMIT_ATTESTATION_OWNER","bounded_harness_correction_cap":1,"production_correction_after_substantive_validation_failure_cap":0,"full_suite_invocation_cap":1,"full_suite_retry":0,"allowed_full_non_green_baseline":{"failures":2,"errors":8,"test_module":"tests.test_p7_thermal_diagnostics","classification":"CURRENT_AGENTS_GOVERNANCE_LINEAGE_IDENTITY_GROUP","exact_test_identities_required":true,"exact_first_failing_frames_required":true,"stage_gate_failure_allowed":false,"materialized_attestation_failure_allowed":false,"changed_owner_failure_allowed":false,"additional_failure_or_error_allowed":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2_REVIEW"}`

## 1. Activation prerequisites and independent restart

Orchestrator必须先把rejected v1 candidate及review evidence保存为historical-only ref/commit，再非破坏性恢复accepted source/test blobs，并以focused orchestration activation commit同步PLAN/FULL/PLAN-FULL。Executer intake必须验证：

- branch为 `codex/g4-r6-owner-alignment-large-change`，HEAD为Orchestrator的新activation commit；
- machine active state为本task/contract `1/1/1`；
- source/test blobs精确为 `0015d7ce2f2a5dde9118478f98c929020a474a01` / `2a60a987dda02675c2eddc7d8260d61a8f68edc3`；
- rejected v1、Q1、Section2、source-attestation-v2 refs不在live ancestry，且其diff/tree/blob/file/patch/implementation读取与复用计数为0。

这不是Q2、新task suffix或旧candidate修补。必须从accepted tree与本合同独立实现。

## 2. Scope and maintainability preflight

唯一production/test写路径：

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_p7_td_b_r6_stage_gate.py`

另可写 `.agent-work/EXECUTION_RESULT.md`。若需要第三production/test/config/wrapper路径、新module/controller或第二identity authority，停止交Orchestrator。

编辑前用CodeGraph从accepted tree核对 `validate_committed_source_attestation`、descriptor/binding、`_build_production_activation`、`run_production_cli_launch`、measure CLI链及persist/replay/loader callers。证明改动替换旧静态self/unborn identity合同并保持一个canonical owner，不复制Git/path/blob/serialization/error owner。预计changed lines `260..440`，hard cap `480`；超过cap或扩大god-object并行语义时停止。

## 3. Complete owner and production propagation contract

同一个最大安全工程包必须全部完成：

1. Candidate阶段不以静态self subject/blob或未来commit SHA/tree为放行权威；descriptor只携带当前可证明的closed candidate paths/references及future materialized schema。
2. Materialized identity在一个真实commit已存在后才生成，closed fields包含exact checkpoint/tree/direct parent/subject/ordered paths/blob OIDs/current identities及linear post-commit ledger。
3. 单一 `validate_committed_source_attestation` owner用read-only real Git和current bytes校验所有field、non-merge parent、tree、subject、ordered changed paths、mode/blob OID、ancestry、worktree scope；unknown/missing/duplicate/reordered/drift均fail closed。
4. `_build_production_activation`及所有production activation/CLI/measure CLI caller必须显式构造或接收同一materialized identity，并在第一次validation call前传入；不得用空probe、全局constant、environment、monkey patch或另一个controller替代。
5. Production inventory/machine/source/parser drift、backend factory与delegate precedence必须保持原合同；materialized identity错误不得错误遮蔽更早的source/machine gate，也不得让backend/device callback提前发生。
6. Public persist/replay/production loader继续绑定canonical owners；本包不得读取、prepare、describe、persist、replay或创建真实package/root。
7. Descriptor/source-reference integrity优先；内部引用一致的secret/historical fixtures必须分别达到semantic guards，不得用双重非法fixture要求较晚错误。

## 4. Regression contract

新tests必须由各自fresh real-Git fixture动态创建parent/candidate/post-commit lineage并从Git读取identity。至少覆盖：

- positive direct child、current bytes、legal `.agent-work/` descendants、JSON-native/deterministic materialization；
- shape/schema/unknown/missing/duplicate/order/SHA/tree/parent/merge/subject/path/blob/mode/current-bytes/ancestry/worktree negative matrix；
- `_build_production_activation` exact materialized propagation；
- production CLI load → materialize → validate → delegate exactly once；
- measure CLI exact route；generic bypass拒绝；
- source/machine/parser/materialized drift都在backend factory/device callback前fail closed；
- delegate failure、inventory failure与binding precedence不被materialized shape错误遮蔽；
- persist/replay/loader只引用canonical owner且无package/device side effect。

不得只改expected error code、mock `validate_committed_source_attestation`、宽泛ignore/allowlist或降低validator约束。

## 5. Validation and freeze

按顺序执行且在ER记录命令、count、duration、exit、evidence path/bytes/SHA：

1. materialized owner + production activation/CLI targeted，全部green；
2. entire `tests.test_p7_td_b_r6_stage_gate` focused，全部green；若仍出现materialized production integration failure，立即停止，不在本candidate修补；
3. related `tests.test_p7_thermal_diagnostics` 与terminal focused；仅允许可追溯exact current-AGENTS governance-lineage `2F+8E` group，无新owner failure；
4. final compileall/static、`git diff --check`、exact scope/cap、forbidden historical/package/device scan；
5. `codegraph sync`及post-sync query，证明single owner与所有production callers完成传播；
6. 冻结source/test path/mode/bytes/SHA/diff stats，之后禁止写入；
7. 对冻结candidate运行唯一full unittest discovery，budget/retry `1/0`。接受仅为完全green，或exact `2 failures + 8 errors` 且全部test identities与first failing frames逐项匹配 `tests.test_p7_thermal_diagnostics` current-AGENTS governance-lineage group；不得有stage-gate/materialized/changed-owner/额外F/E。

本包可有一次仅fixture/validation harness bounded correction，必须完整记账；substantive production failure后 correction cap为0。不得拆出单-call、单test、单validation或ER微PLAN。单命令预计超过10分钟时遵守visible Terminal、三次稀疏liveness与automation规则。

Scratch只可fresh创建于 `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-v2-*`，不得读取existing package/formal/experiment roots；结束时process/automation为0。

## 6. Acceptance and handoff

接受必须同时满足：exact scope/cap；targeted和stage-gate focused green；related/full仅有允许的exact governance baseline或green；compile/static/CodeGraph/diff/scope通过；source/test freeze后无mutation；历史输入和全部外部effect为0。

Executer不得commit。ER返回candidate identities、完整validation/effect ledger，并停在：

`RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_V2_REVIEW`

Planner若接受，Orchestrator才建立exact code checkpoint并运行一次read-only post-commit attestation probe；package preparation仍由后续独立PLAN决定。若拒绝，不修补、不重跑、不创建suffix/Q2/alternate candidate/root。

## 7. Hard locks

- GUIDE/RESEARCH immutable；Human goal、GUIDE、scientific stage未完成；retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- Package prepare/describe/replay/probe/root、formal/replacement formal、release、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C权限全部false。
- Executer不得修改PLAN/FULL/PLAN-FULL/archive/debug/config/wrapper/GUIDE/RESEARCH，不得commit/push/PR。
