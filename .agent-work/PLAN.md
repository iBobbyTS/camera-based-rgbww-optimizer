# REF-G4-01-SUCCESSOR-LINEAGE：JSON-native representation seam correction

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_CODE_TEST_CORRECTION`

**Executable：** `true`（仅在Orchestrator按§2对齐FULL并提交activation后生效）

**Active task count：** `1`

**Active task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_01_JSON_NATIVE_PROJECTION_CORRECTION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-SUCCESSOR-LINEAGE-JSON-NATIVE-PROJECTION-CORRECTION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_CODE_TEST_CORRECTION","executable":true,"active_task_count":1,"active_task":"REF-G4-01-SUCCESSOR-LINEAGE","reference_task_id":"REF-G4-01-SUCCESSOR-LINEAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_BOUNDED_JSON_NATIVE_PROJECTION_CORRECTION","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","verified_source_parent":"b2ec3b0807841bb2e42ca928ce65615d4a704f9f","activation_child_sha_recorded_in_plan":false,"activation_child_subject":"docs(plan): activate g4 json-native seam correction","activation_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260803-1057.md",".agent-work/archived/PLAN-20260803-1057.md"],"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1057.md","bytes":20233,"sha256":"f8daec91b1c41b6a4686511869c18be3b1feea06291e6b88a118e61701d16f7d","source_body_bytes":19179,"source_body_sha256":"8ee8f364b3f551df024295b631ad3768efbb6b2dfd66593a196dfb8e062f9f10"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1057.md","bytes":8260,"sha256":"9f446dbfdef2040147db504a61c85f92ca95f718be52e1fb1cc377c74a8aab8e","source_body_bytes":7208,"source_body_sha256":"90b791591cabba8423489ea46a420552df226e9389e5c0650f06f3ba9536028e"},"rejected_execution_disposition":"REJECTED_ZERO_ROOT_JSON_NATIVE_REPRESENTATION_SEAM","same_boundary_failure_ordinal":1,"single_current_action":"project_the_strictly_decoded_immutable_policy_exactly_once_through_the_existing_provenance_json_native_owner_then_use_that_same_native_value_for_default_validation_default_r6_plan_build_and_frozen_policy_contract_with_real_policy_regression","allowed_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py","tests/test_p7_successor_lineage.py",".agent-work/EXECUTION_RESULT.md"],"production_source_edits":1,"test_file_edits":1,"provenance_owner_edits":0,"thermal_giant_module_edits":0,"config_edits":0,"guide_edits":0,"research_edits":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"archive_edits_by_executer":0,"execution_pass_cap":1,"ordinary_bounded_correction_cap":1,"corrective_task_id_creation":0,"release_root_acquisition":0,"release_generation":0,"public_validator_invocations":0,"final_validator_invocations":0,"strict_validator_invocations":0,"release_consumption":0,"retained_r3_access":0,"legacy_release_access":0,"external_experiment_payload_access":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"targeted_test_invocation_cap":1,"focused_test_invocation_cap":1,"compile_static_invocation_cap":1,"full_suite_invocation_cap":1,"codegraph_sync_cap":1,"commit_by_executer":0,"planner_stop":"RETURN_FOR_G4_01_JSON_NATIVE_PROJECTION_CORRECTION_REVIEW","future_reference_task":"REF-G4-01-SUCCESSOR-LINEAGE","future_stage_locked":true}`

## 1. Planner review decision

Planner独立拒绝上一fresh release execution result：

```text
decision = REJECTED_ZERO_ROOT_JSON_NATIVE_REPRESENTATION_SEAM
specific boundary failure ordinal = 1
source/policy file identity preflight = pass
strict decoded types = mappingproxy / nested tuple
production validator = ValueError: in-memory TD-B exposure policy differs from the repository owner
UTC/root/build/compose/public/final/strict = 0/0/0/0/0/0/0
retry/fallback/repair/alternate root = 0/0/0/0
```

Planner用exact repo policy独立复现：`provenance.decode_strict_json_bytes`返回immutable JSON representation；当前
successor owner将其直接交给thermal validator/build owner，而thermal owner的repository policy是ordinary
`dict/list`。调用既有`provenance.json_native_value`后，同一production validator与
`build_td_b_r6_formal_plan`均通过，原immutable input仍未改变。

因此这是首次真实production-default invocation暴露的普通representation integration seam，不是policy bytes、EQ、
measurement、science、device或GUIDE hard stop，不需要Human/Advisor。Accepted successor/provenance owner整体保留；本包
只允许一次bounded correction，继续同一flat `REF-G4-01-SUCCESSOR-LINEAGE`，不创建suffix、新task或release root。

## 2. Activation与review archives

Orchestrator activation必须是下列parent的direct child：

```text
parent = b2ec3b0807841bb2e42ca928ce65615d4a704f9f
subject = docs(plan): activate g4 json-native seam correction
changed paths exact =
  .agent-work/EXECUTION_RESULT.md
  .agent-work/FULL_PLAN_REFERENCE.md
  .agent-work/PLAN.md
  .agent-work/archived/EXECUTION_RESULT-20260803-1057.md
  .agent-work/archived/PLAN-20260803-1057.md
```

Child SHA不自嵌PLAN。执行前repo-owned parser必须证明PLAN/FULL contract ID一致、active count `1/1`、task exact；
worktree clean。Reviewed archives必须exact：

| archive | bytes | SHA-256 | body bytes | body SHA-256 |
|---|---:|---|---:|---|
| `.agent-work/archived/PLAN-20260803-1057.md` | 20233 | `f8daec91b1c41b6a4686511869c18be3b1feea06291e6b88a118e61701d16f7d` | 19179 | `8ee8f364b3f551df024295b631ad3768efbb6b2dfd66593a196dfb8e062f9f10` |
| `.agent-work/archived/EXECUTION_RESULT-20260803-1057.md` | 8260 | `9f446dbfdef2040147db504a61c85f92ca95f718be52e1fb1cc377c74a8aab8e` | 7208 | `90b791591cabba8423489ea46a420552df226e9389e5c0650f06f3ba9536028e` |

Archive replay任一不符即stop。上一failure evidence immutable；不得改写为release attempt或科学失败。

## 3. Maintainability preflight与唯一实现

CodeGraph preflight已经定位单一ownership seam：

```text
decode owner = provenance.decode_strict_json_bytes -> mappingproxy/tuple
native projection owner = provenance.json_native_value -> dict/list
consumer owners = thermal.validate_td_b_exposure_policy_v2 + thermal.build_td_b_r6_formal_plan
composition owner = successor.build_successor_lineage_inputs
```

`p7_thermal_diagnostics.py`是巨型P7模块且不是缺陷owner，禁止修改。`p7_retained_r3_provenance_io.py`已有正确的
single source of truth，禁止修改或复制其serialization逻辑。不得新增adapter/controller/helper文件。

只在`build_successor_lineage_inputs`内做最小修改：

1. strict decoder结果保留为独立immutable decoded value；top-level非`Mapping`继续使用现有
   `policy_not_object` precedence。
2. 紧接decode/type gate后，显式且exactly once调用
   `native_policy = provenance.json_native_value(decoded_policy)`。
3. `native_policy`必须是ordinary top-level `dict`，nested mappings/lists也必须是ordinary JSON-native值；任何
   unsupported/cyclic/nonfinite representation继续由provenance owner fail closed，不新增compatibility coercion。
4. 把同一个`native_policy`对象依次交给现有production `validate_policy_fn`与`build_r6_plan_fn`；不得各自重新投影、
   shallow `dict()`、JSON round-trip或复制thermal validation。
5. `frozen["policy_contract"]`使用同一个`native_policy`作为值；移除该位置原有第二次显式
   `provenance.json_native_value(policy)`。最终`SuccessorLineageInputs`仍由现有`_freeze`形成immutable
   mappingproxy/tuple output，不降低immutability。

只允许修改：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
tests/test_p7_successor_lineage.py
.agent-work/EXECUTION_RESULT.md
```

其他source/test、provenance owner、thermal giant module、config、PLAN/FULL/archive、GUIDE/RESEARCH均只读。

## 4. Required behavior tests

在`tests/test_p7_successor_lineage.py`补充有行为断言的回归，不得只检查source text：

1. **真实production-default seam：** 读取exact absolute repo
   `config/hsi/p7-ray-td-b-exposure-policy-v2.json`的真实bytes/path/SHA；保留default
   `read_exact_file_fn`、`decode_policy_fn`、`validate_policy_fn`与`build_r6_plan_fn`，仅用bounded clean-source、EQ audit与
   machine-status fakes隔离Git/EQ/device。`build_successor_lineage_inputs`必须通过，并断言C=`1/2500`、16 capture、
   non-executable plan及policy identity exact。不得用fixture validator或fixture plan掩盖这条seam。
2. **single projection/same object：** 自定义immutable nested mappingproxy/tuple input，callback捕获identity；断言
   validator与plan builder收到exact同一个ordinary `dict`对象、nested sequence为`list`，且只发生一次显式native
   projection。测试不得mock掉`provenance.json_native_value`的真实递归语义。
3. **input/output immutability：** build后原decoded mappingproxy/tuple内容与type不变；returned
   `frozen_inputs["policy_contract"]`仍为mappingproxy/nested tuple，mutation被拒绝；其JSON-native投影与原语义相等。
4. 保留并继续通过现有source/policy/EQ drift、old-route、R6 drift、integrity/reference、error-precedence与failure seal
   tests；不得为了新pass放宽closed schema、authority、terminal-last或historical guard。

测试不得读取external EQ root、retained R3、legacy release或设备。真实policy是repo tracked config，不是external
experiment payload。

## 5. One execution pass与validation

Executer只运行一个实现/验证pass，不得在失败后现场第二轮修改。顺序：

1. 复核activation topology、clean worktree、archive replay、PLAN/FULL parser与allowed paths。
2. 按§3修改exact one production file与§4 exact one test file。
3. targeted exactly once：successor + provenance owner suites。
4. relevant focused exactly once：successor、provenance与`test_p7_td_b_r6_contract`，证明production thermal consumer合同未退化。
5. compile/static exactly once：compile changed source/test；AST/static证明`build_successor_lineage_inputs`只有一个显式
   `provenance.json_native_value` projection，且thermal/provenance模块未改。
6. full unittest discovery exactly once，记录exact count。
7. `codegraph sync` exactly once，然后query确认decode -> native projection -> validate/build -> frozen contract call path，
   没有parallel owner。
8. `git diff --check`、changed-path exact、secret/path/forbidden-import检查；证明config、GUIDE/RESEARCH、PLAN/FULL、
   provenance owner、thermal giant module与其他tests未变。

测试/compile/full任一步失败立即写ER并stop，不得同包修第二次、retry test或建立corrective suffix。预计小于10分钟；
禁止background/Terminal/automation。

## 6. Absolute zero boundary与handoff

```text
release family/root generation = 0
public/final/strict validator real invocation = 0/0/0
release consumption / retained R3 / legacy release = 0/0/0
external experiment root access = 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
commit/amend/stage/push by Executer = 0
corrective task ID / new root = 0/0
```

Executer只写live ER，至少记录：activation/parser/archive evidence；CodeGraph preflight；exact diff；real-policy default
regression与nested representation assertions；targeted/focused/compile/static/full exact counts；CodeGraph sync/query；
changed-path/zero-authority ledger；decision request。成功请求：

```text
RETURN_FOR_G4_01_JSON_NATIVE_PROJECTION_CORRECTION_REVIEW
```

本包成功只表示owner seam candidate可供Planner验收；不生成release、不解锁G4-02，也不自动commit。随后stop。

## 7. 维护性判断

修复位于composition owner的单一adapter seam，仅复用既有provenance native projection；不修改巨型thermal owner，不复制
serialization/validation，不新增module/controller。真实default integration与nested immutability回归覆盖该高风险边界。
