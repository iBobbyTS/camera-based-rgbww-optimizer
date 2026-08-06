# REF-G4-06 atomic materialized runtime consumer migration

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION`

**Executable：** `true`

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

**Contract：** `G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1`

**Contract strategy：** `B_INTENTIONAL_PUBLIC_MATERIALIZED_RUNTIME_CONTRACT_MIGRATION`

**Planner stop：** `RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","reference_task_id":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_ATOMIC_CONSUMER_MIGRATION","contract_strategy":"B_INTENTIONAL_PUBLIC_MATERIALIZED_RUNTIME_CONTRACT_MIGRATION","historical_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","historical_disposition":"REJECTED_MATERIALIZED_ATTESTATION_OWNER_SEAM_THIRD_SUBSTANTIVE_FAILURE_TERMINAL_FAIL_CLOSED","historical_ref":"refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected","historical_commit":"4a39f9ab377d7568c37eeea8aaa78d82aaa14535","historical_candidate_input_allowed":false,"fourth_repair_allowed":false,"new_architecture_route":true,"new_architecture_attempt":1,"required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","active_plan_contract_id":"G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","canonical_next_reference_status":"ACTIVE_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION"},"large_change":{"branch":"codex/g4-r6-owner-alignment-large-change","plan_full_section":"ATOMIC_PUBLIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION","expected_changed_lines_min":300,"expected_changed_lines_max":700,"hard_changed_lines_cap":900,"atomic_section_split_allowed":false},"single_owner":{"module":"camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate","owns":["schema","serialization","materialization","validation","canonical_runtime_construction"],"parallel_authority_schema_allowed":false,"old_and_new_schema_both_authorizing_allowed":false},"production_scope":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py"],"test_scope":["tests/test_p7_td_b_r6_stage_gate.py","tests/test_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_terminal.py","tests/p7_td_b_r6_materialized_runtime_support.py"],"executor_repo_write_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py","tests/test_p7_td_b_r6_stage_gate.py","tests/test_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_terminal.py","tests/p7_td_b_r6_materialized_runtime_support.py",".agent-work/EXECUTION_RESULT.md"],"fixture_strategy":"ONE_CANONICAL_TEST_SUPPORT_PATH_SUPPLYING_VALUES_AND_DELEGATING_ALL_SCHEMA_CONSTRUCTION_TO_PRODUCTION_OWNER","accepted_rollback":{"stage_gate_source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","stage_gate_test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","all_six_existing_paths_bound_to_activation_head":true,"executer_rollback_authorized":false},"validation_order":["targeted","stage_gate_focused","terminal_focused","thermal_focused","related_integration","compile_static","codegraph_sync_query","diff_scope_identity","full_suite"],"targeted_invocation_cap":1,"stage_gate_invocation_cap":1,"terminal_invocation_cap":1,"thermal_invocation_cap":1,"related_invocation_cap":1,"full_suite_invocation_cap":1,"full_suite_retry":0,"same_candidate_correction_after_valid_failure_allowed":false,"test_rerun_after_valid_failure_allowed":false,"known_governance_baseline":{"module":"tests.test_p7_thermal_diagnostics","failures":2,"errors":8,"candidate_owned_error_allowed":false,"exact_identity_manifest_required":true,"exact_first_frame_required":true},"candidate_commit_by_executer":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW"}`

## 1. Activation、accepted-tree intake与maintainability preflight

Orchestrator必须先把FULL与PLAN-FULL同步到本PLAN的 `required_full_machine_state`，复位 `.agent-work/EXECUTION_RESULT.md`，创建仅含orchestration文档的activation checkpoint，再允许Executer开始。FULL/PF始终为non-executable reference；执行权只来自本PLAN。

Executer必须从当前accepted tree独立实现，不得读取、diff、show、checkout、merge、cherry-pick、rebase、复制或应用historical ref `refs/heads/codex/historical-g4-r6-materialized-attestation-third-failure-rejected` 或commit `4a39f9ab377d7568c37eeea8aaa78d82aaa14535` 的implementation。旧task保持terminal rejected；本任务不是其第四次repair、corrective suffix或同candidate重跑。

在任何写入前完成并写入ER的maintainability preflight：

1. 核验branch为 `codex/g4-r6-owner-alignment-large-change`、HEAD为Orchestrator activation checkpoint、worktree仅有PLAN明确允许的状态；PLAN/FULL/PF active task/contract精确一致。
2. 冻结现有六个consumer文件的path、mode、bytes、SHA-256及HEAD blob OID；stage-gate source/test blob必须分别为 `0015d7ce2f2a5dde9118478f98c929020a474a01`、`2a60a987dda02675c2eddc7d8260d61a8f68edc3`。六路径HEAD identities构成rollback ledger；Executer不得自行rollback，失败后由Orchestrator按ledger恢复。
3. 使用CodeGraph确认stage-gate builder/materializer/validator、measure execution consumer、terminal replay/finalizer consumer和三个fixture入口的完整调用链；记录未发现的额外consumer为0，若发现额外production consumer则停止返回Planner，不得静默扩大scope。
4. 预计改动超过300行，继续使用当前large-change branch和PLAN-FULL的单一 `ATOMIC_PUBLIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION` section。该迁移只有完整跨consumer状态才可验证，禁止拆成producer-only、fixture-only、zero-write、natural-exit、qualification或docs微section。
5. `p7_td_b_r6_stage_gate.py`是大型协调模块。只允许围绕现有materialized runtime boundary建立一个纯canonical construction seam；不得借机重构无关package、capture或thermal逻辑。最终changed-lines预计300–700，hard cap 900；超限立即停止。

## 2. Strategy B public contract delta与唯一owner

本包有意且原子地迁移公开PLAN-bound materialized runtime contract：

1. `camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate`继续唯一拥有：attestation dataclass/schema、JSON-native serialization、activation/materialized authority construction、runtime plan materialization及fail-closed validation。
2. 在该production owner中提供一个纯、无I/O、可复用的canonical runtime construction入口。它接收typed `CommittedSourceAttestation`及冻结的activation inputs，构造唯一future activation/PLAN-bound authority并调用现有materialization/validation owners；production activation和所有synthetic fixtures均委托它。
3. 新attestation公开形状必须包含能在commit存在后物化并验证的exact facts：verified parent identity、code-owner checkpoint/tree/direct parent/subject/changed paths/blob OIDs、current candidate identities、live activation identity、candidate-reference digest及post-child linear ledger。
4. 因activation与PLAN-bound authority形状发生公开变化，相关schema版本必须各自明确单向升级。旧attestation schema、旧future-activation schema、旧PLAN-bound authority schema及旧top-level code/live identity aliases必须fail closed；不得同时保留两套可独立授权schema、compatibility fallback或alias normalization。
5. Template authority继续non-authorizing；package、formal和device权限不得因schema迁移改变。Public contract delta必须在ER列出old→new schema、removed aliases、added nested fields、serialization order/shape和所有error codes。
6. Measure与terminal模块只是consumer：它们只能调用stage-gate公开construction/validation contract或读取经其验证的结果，不得复制字段集合、schema常量、serializer、digest或独立放行逻辑。

## 3. Complete consumer、path与fixture migration ledger

必须在同一candidate内检查并按需修改全部scope：

### Production consumers

- `p7_td_b_r6_stage_gate.py`：`CommittedSourceAttestation`、serialization、production activation、future activation、materialized projection/runtime materialization及validator全部由一个schema owner闭合。
- `measure_p7_thermal_diagnostics.py`：`validate_authorized_execution_plan → run_validated_td_b_r6_runtime_contract → run_authorized_plan → execute_plan`消费新contract，但保持frozen materialized plan不可变；resolved camera settings/runtime provenance继续通过独立runtime context传递并写入run evidence，不能重新写回frozen plan。
- `p7_td_b_r6_terminal.py`：`is_r6_materialized_plan`、replay/finalizer必须消费同一stage-gate validator；不得用旧字段列表或宽松识别绕过schema migration。

### Canonical fixture construction

- 新增唯一 `tests/p7_td_b_r6_materialized_runtime_support.py`，只拥有确定性sample values和无副作用调用编排；它不得定义schema常量、手写authority/attestation key set、独立serializer、validator或acceptance rule。
- `tests/test_p7_td_b_r6_stage_gate.py::SyntheticGitRepository.future_activation` 必须把真实synthetic Git attestation交给production canonical construction入口，不再手写公开authority schema。
- `tests/test_p7_thermal_diagnostics.py::_r6_materialized_plan_for_test` 与 `tests/test_p7_td_b_r6_terminal.py::materialized_plan` 必须复用上述shared test support，并由support委托production owner；两处不得保留等价nested dictionary。
- 对六个existing files及新support path建立final path/fixture ledger，证明handwritten authority/attestation fixture count为0、production schema owner count为1、independent authorizing schema count为1。

## 4. Negative regression与error precedence

必须增加或更新有行为意义的保护测试：

1. canonical construction对typed attestation产生唯一、deterministic、JSON-native的activation与materialized plan；三类fixture生成相同contract shape，并由public validator接受。
2. 旧schema、旧top-level aliases、missing/extra/unknown fields、wrong native types、descriptor/reference digest drift、parent/merge/path/blob/current-bytes/post-child lineage drift均fail closed；不得因迁移增加wide ignore或默认填充。
3. Error precedence保持：outer authority shape/schema及source/reference integrity在下游语义和backend factory前拒绝；具体underlying stable code不得被无差别包装丢失。测试必须分别让每个guard可达，不能用同一fixture同时违反多条规则却要求后置错误。
4. Measure full-chain regression不得mock `execute_plan`，证明materialized plan调用前后bytes/native value不变，runtime context独立，resolved settings仍进入run evidence，未知真实template drift仍在任何fake callback effect前拒绝。
5. Terminal regressions证明new contract经过识别、replay、failure seal与pass seal owners；stale contract不能因`is_r6_materialized_plan`宽松判断进入finalizer。
6. 所有backend/light/capture callbacks必须是fake并断言connect、device、camera、Ray、strip、capture调用为0；本包不产生科学、formal或设备证据。

## 5. Maximum safe continuous validation package

只允许一个fresh `/Volumes/4T/temp/rgbww-optimizer/g4-r6-atomic-materialized-runtime-consumer-migration-*` validation root。不得读取existing external roots、package/formal roots或historical implementation。Candidate开始资格验证后source/test/support写入cap为0；任一有效non-green立即停止，不修改candidate、不重跑、不换root。

按以下顺序各运行一次并封存exact argv、environment、start/end、natural exit、counts、bytes/SHA及完整traceback：

1. **Targeted**：canonical construction、三个fixture入口、old/new schema exclusivity、error precedence、frozen-plan/runtime-context及terminal recognition/validation negative probes；必须green。
2. **Stage-gate focused**：完整 `tests.test_p7_td_b_r6_stage_gate`；必须green。
3. **Terminal focused**：完整 `tests.test_p7_td_b_r6_terminal`；必须green。
4. **Thermal focused**：完整 `tests.test_p7_thermal_diagnostics`。接受仅为green或下述exact unrelated governance baseline；任何materialized/runtime/stage-gate/terminal/candidate-owned F/E立即拒绝。
5. **Related integration**：一次联合运行stage-gate、terminal、thermal三组，证明加载顺序和shared fixture不会产生order-dependent drift。接受标准同上；不得用baseline吸收candidate错误。
6. **Compile/static**：对三个production modules、三个test modules及support module运行compileall/import/AST静态检查；运行repo-owned PLAN/FULL parser、machine-state exact consistency、`git diff --check`。
7. **CodeGraph**：`codegraph sync`后查询canonical factory→materializer/validator→measure/terminal调用链；证明production schema owner=1、fixture delegation完整、无parallel authority owner。
8. **Diff/scope/identity**：changed paths只能是PLAN允许的7个implementation/test paths加ER；final diff不超过900；记录mode、bytes、SHA-256、blob/worktree identities及六路径rollback ledger；GUIDE/RESEARCH/config/wrapper/package artifacts必须零变化。
9. **Full suite**：仅当前八个gate全部满足后运行唯一一次 `.venv/bin/python -m unittest discover -s tests`；invocation/retry `1/0`。接受仅为全绿或exact unrelated governance baseline，无任何additional F/E。

Exact governance baseline只包含 `tests.test_p7_thermal_diagnostics` 的以下2F+8E，并要求每个identity与first underlying frame仍指向既有 `TD-B governance successor path identity differs: AGENTS.md` seam：

Failures：

- `test_recovery_head_fails_closed_and_historical_policy_remains_replayable`
- `test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift`

Errors：

- `test_agents_policy_lineage_rejects_wrong_bytes_owner_and_provenance`
- `test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`
- `test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`
- `test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`
- `test_lineage_release_rejects_candidate_and_resolved_plan_tampering`
- `test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`
- `test_public_default_successor_lineage_layers_historical_and_current_owners`
- `test_public_default_successor_manifest_fails_closed_on_exact_drift`

任一candidate-owned error、identity变化、不同first frame或额外F/E均不能归入baseline。Harness/collection/seal无效也立即返回Planner，不在本PLAN内更正命令或重跑。

若full预计超过10分钟，Executer必须在可见macOS Terminal启动，执行三次稀疏liveness检查；确认存活后由Orchestrator创建automation并按long-task规则blocked。Human恢复后只检查一次；不得后台轮询或重复launch。

## 6. Handoff、acceptance与stop

`.agent-work/EXECUTION_RESULT.md`必须记录：activation/rollback identities；contract delta；完整consumer/path/fixture ledger；changed paths/diff；所有validation logs及SHA；full invocation/retry；process/automation；scratch inventory；零external effects；candidate是否满足acceptance。

Planner acceptance要求：

- Strategy B的old→new迁移原子完成，old schema不再可授权；
- stage-gate为唯一schema/serialization/materialization/validation owner；
- measure、terminal及三个fixture入口全部消费canonical production contract；
- handwritten schema fixtures=0，parallel authorizing owners=0；
- frozen-plan/runtime-context seam和error precedence保持；
- 所有focused/integration/static/CodeGraph/diff gates合格；
- full为green或仅exact unrelated `2F+8E` baseline；
- source/test没有在有效non-green后修改或重跑；
- package/formal/release/device/scientific effects全为0。

Executer不得commit、push或创建PR。成功或失败均停在：

`RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`

若拒绝，本candidate只能由Orchestrator保存为historical-only并恢复rollback ledger；不得在同candidate上修复或重跑。若接受，仍只解锁Orchestrator创建focused engineering checkpoint与large-change clean review；package preparation必须由后续独立PLAN授权。

## 7. Hard locks

GUIDE/RESEARCH immutable；Human goal、GUIDE和科学阶段均未完成；retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。Package prepare/describe/root、replacement formal、release consumption、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C全部false。不得访问external experiment payload，不得从offline green推导hardware/formal readiness。
