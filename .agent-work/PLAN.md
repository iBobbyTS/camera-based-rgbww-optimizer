# REF-G4-04-E2：final canonical owner-binding refactor

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FINAL_CANONICAL_OWNER_BINDING`

**Executable after activation：** `true`

**Active task count after activation：** `1`

**Active task after activation：** `REF-G4-04-E2`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_FINAL_CANONICAL_OWNER_BINDING_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-E2-FINAL-CANONICAL-OWNER-BINDING-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FINAL_CANONICAL_OWNER_BINDING","executable":true,"active_task_count":1,"active_task":"REF-G4-04-E2","reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_FINAL_CANONICAL_OWNER_BINDING","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"a05b2703de49f29d0fc93030a37a39fed24c2fdb","expected_parent_tree":"825145cbae27087939d380b3c42e2148abee11e9","expected_subject":"docs(plan): activate final e2 owner binding","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"execution_authorized_before_activation":false,"single_current_action":"remove_public_semantic_and_replay_owner_injection_from_existing_e2_persist_replay_boundaries_and_lock_canonical_owner_signatures","allowed_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","tests/test_p7_successor_e2.py"],"existing_production_files_edited":1,"existing_test_files_edited":1,"new_production_modules":0,"new_test_files":0,"giant_p7_module_edits":0,"config_edits":0,"wrapper_edits":0,"full_edits_by_executer":0,"plan_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"corrective_suffixes":0,"new_task_ids":0,"source_checkpoint":"a05b2703de49f29d0fc93030a37a39fed24c2fdb","source_tree":"825145cbae27087939d380b3c42e2148abee11e9","guide":{"path":"advisor/4/4.GUIDE.md","sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35"},"candidate_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":26151,"sha256":"ffbe04250a43e3c1329bc8cfce6ec60d7eb814070603e1f350f58e7b669e904a"},"candidate_tests":{"path":"tests/test_p7_successor_e2.py","bytes":26715,"sha256":"15f6fdcd94165d1ab570d8ae75a1e5e53dda83e17ffe8e0262afb35e255c97f7"},"prior_reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1549.md","bytes":16255,"sha256":"221f4f0425b754489671802ec2786dd7760f7ca9221d1257cc39f74009ad78ad"},"prior_reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1549.md","bytes":9554,"sha256":"c816a196362cd41ded2402bd858caab6082bb2b500cc553cbd20038d78588b83"},"same_boundary_failure_count_before_attempt":2,"attempt_ordinal":3,"final_same_reference_attempt":true,"fourth_attempt_allowed":false,"offline_bounded_correction_cap":0,"targeted_test_invocation_cap":1,"focused_test_invocation_cap":1,"full_suite_invocation_cap":1,"compile_static_invocation_cap":1,"source_scan_invocation_cap":1,"codegraph_sync_cap":1,"persist_public_parameters":["inputs","result","create_root_fn","persist_fn"],"replay_public_parameters":["root_path"],"evaluate_semantic_injection_allowed":true,"persist_semantic_injection_allowed":false,"persist_replay_injection_allowed":false,"replay_semantic_injection_allowed":false,"canonical_thermal_owner_required":true,"canonical_replay_owner_required":true,"existing_rejected_e2_root_access_allowed":false,"new_durable_e2_root_allowed":false,"production_evaluation_cap":0,"production_persist_cap":0,"production_replay_cap":0,"unit_test_ephemeral_tempdir_only":true,"external_payload_access":0,"release_root_access":0,"predevice_root_access":0,"readiness_root_access":0,"retained_r3_access":0,"legacy_r2_access":0,"deep_corrective_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"g4_05_planning_unlocked":false,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_04_E2_FINAL_CANONICAL_OWNER_BINDING_REVIEW","future_reference_task":"REF-G4-05-RAY-R6-STAGE-GATE","future_stage_locked":true}`

## 0. Activation gate

本文件是等待Orchestrator activation的draft；activation前不得执行。Orchestrator必须验证并形成：

1. direct parent exact为`a05b2703de49f29d0fc93030a37a39fed24c2fdb`，parent tree exact为
   `825145cbae27087939d380b3c42e2148abee11e9`，branch为`main`；
2. subject exact为`docs(plan): activate final e2 owner binding`；changed paths exact且仅为PLAN、ER、FULL；
3. activation child中PLAN/FULL strict machine parser为active count`1/1`、task均为`REF-G4-04-E2`、canonical next singleton同task；
4. source/test、GUIDE与prior reviewed archives identity exact匹配machine row；
5. retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption、device、formal R6、TD-C与G4-05/06 authority均false/0。

任一项失败立即只写ER并stop，不编辑source/test。本attempt不允许activation drift correction。

## 1. Final-attempt与maintainability boundary

这是同一canonical-owner boundary的第三次且最后一次attempt；不创建task ID、corrective suffix、controller、module或root。Executer没有
bounded correction/retry预算：targeted、signature invariant、canonical-owner probe或任一其他要求首次失败即停止回Orchestrator；不得修后
重跑，第四轮明确禁止。

Maintainability preflight结论：只需缩小现有E2 public trust boundary。既有`p7_thermal_diagnostics.py`继续唯一拥有formal plan builder、
validator与machine status；既有provenance owner继续拥有I/O/serialization；现有E2 owner继续组合它们。不得修改三个巨型P7模块、
provenance owner或其他文件，不做无关重构。

## 2. Exact public API owner binding

在`p7_successor_e2.py`做最小签名和调用链收敛：

### `persist_e2_package`

Public参数集必须由`inspect.signature`锁定为exact：

1. `inputs`
2. `result`
3. keyword-only `create_root_fn`
4. keyword-only `persist_fn`

不得公开、接受或从`**kwargs`吞入`build_plan_fn`、`validate_plan_fn`、`machine_status_fn`或`replay_fn`。`create_root_fn`和
`persist_fn`只保留为I/O failure test seam；不能影响semantic truth。Persist必须在任何create/persist callback前，用不可由public caller替换的
canonical bindings重新验证result：

- `thermal.build_td_b_r6_formal_plan`
- `thermal.validate_td_b_r6_formal_plan`
- `thermal.td_b_r6_machine_status`

成功写入两artifact后必须直接调用repo-owned `replay_e2_package(root.path)`，不得经过可注入callback、alias选择或caller-provided replay。

### `replay_e2_package`

Public参数集必须由`inspect.signature`锁定为exact单参数`root_path`；不得公开、接受或吞入`inputs`、`build_plan_fn`、
`validate_plan_fn`、`machine_status_fn`、I/O owner或任意callback。Replay必须使用`frozen_e2_input()`及不可由public caller替换的canonical
thermal builder/validator/status，对decoded result重跑现有shared closed result contract，再验证closed terminal与result identity。

### `evaluate_e2_preformal_gate`与private seam

Evaluate可保留当前窄的`build_plan_fn`、`validate_plan_fn`、`machine_status_fn`测试依赖注入，以验证evaluator组合逻辑；但其产物不得因此
携带owner authority。任何result在persist/replay public trust boundary都必须独立经过上面的canonical revalidation。

Private `_validate_result_contract`内部可保留evaluate专用expected/seam参数，但persist/replay不得把public callback转交给它；production
trust-boundary call sites必须静态指向canonical module owners。不得复制formal/machine literal或建立第二个validator。

## 3. Preserve accepted partial contracts

必须保留前一candidate已证明的行为：

- shared closed result validator仍由evaluate、persist、replay三入口复用；
- result top/nested exact shape、strict bool/int、exact guards、authority与frozen reference ledger；
- formal plan经existing builder+validator且与builder JSON-native exact相等；machine status与existing owner exact相等；
- terminal closed schema/authority/result regular-file identity；同步改写open result及匹配terminal仍fail closed；
- persist semantic validation发生在create/persist之前；fail seal仍single root、retry0、alternate root0；
- accepted test-only ephemeral package仍可canonical round-trip，测试清理后root residual为0；
- E2 source无device/network/process/env/controller owner，无formal/machine完整字面副本。

## 4. Required tests and no-I/O exploit closure

只修改现有`tests/test_p7_successor_e2.py`。除保留全部实质断言外，新增：

1. `inspect.signature`逐项断言persist exact参数集/keyword-only属性与replay exact单参数；AST断言两public函数没有`**kwargs`，persist直接调用
   canonical replay owner，persist/replay call sites没有semantic callback参数；
2. 对persist分别传入`build_plan_fn`、`validate_plan_fn`、`machine_status_fn`、`replay_fn`，必须在函数body/I/O前以`TypeError`拒绝；
   `create_root_fn`计数必须为0，persist_fn计数0；
3. 重现Planner probe的self-consistent forged formal/machine result，但不提供semantic injection时必须由canonical owner拒绝，create/persist均0；
4. 对replay分别传入`inputs`、三个semantic owner和replay callback，必须因unexpected keyword以`TypeError`拒绝，且mocked
   `read_existing_root`调用0，证明没有读取root/payload；
5. Evaluate窄DI仍各调用一次并可产生测试结果；将该结果交persist时只能由canonical owners裁定，不能继承注入owner authority；
6. accepted ephemeral roundtrip仍证明persist调用canonical replay、canonical bytes、0700/0600、exact inventory、closed terminal、deep immutable
   replay及cleanup residual0；已有result/terminal/open/synchronized forgery tests继续通过。

所有injection closure probe必须无I/O；不得为了测试访问已拒E2 root。只有既有fresh、自动清理的
`/Volumes/4T/temp/rgbww-optimizer` test `TemporaryDirectory`可用于accepted roundtrip；它不是durable/experiment root。

## 5. Validation sequence：zero retry

严格按顺序，每项只运行一次：

1. Targeted：`.venv/bin/python -m unittest tests.test_p7_successor_e2`。任何fail/error立即stop，不修改后重跑；
2. Focused：successor lineage、predevice、zero-readiness、E2、R6 contract、thermal runner与provenance相关unittest集合；
3. Full：`.venv/bin/python -m unittest discover -s tests`；
4. `.venv/bin/python -m compileall -q src tests`与`zsh -n tmp/run-p7-thermal-diagnostics.zsh`；
5. 对activation HEAD→worktree的exact source/test调用repo-owned baseline-aware source scanner；要求exact two paths、0 findings、无private/
   env/network/symlink/unsafe path；
6. `git diff --check`，证明dirty paths仅source/test/ER，GUIDE/RESEARCH、FULL/PLAN、archives、config、wrappers、三大P7模块未变；
7. `codegraph sync`后query：persist/replay public paths只能绑定canonical thermal/provenance/replay owners，无semantic/replay callback边；
8. repo-owned PLAN/FULL strict parser要求active count`1/1`、task同为`REF-G4-04-E2`、canonical next singleton不变。

任一canonical-owner static/dynamic probe、targeted、focused、full、compile、scan、diff、CodeGraph或machine check失败均是本final attempt失败；
不得使用corrective budget，不得重跑同一gate。

## 6. Safety and authority locks

- 全程offline code/test-only；production evaluate/persist/replay为0，不创建durable E2/formal/experiment root；
- 已拒E2 root、G4-01/02/03 roots、retained R3、legacy/deep-corrective及其他external payload访问均0；
- device、network、app、process、listener、camera、Ray、strip、capture、nonzero light、release consumption、formal R6、TD-C、firmware、
  deployment调用均0；
- 不生成G4-05/06 PLAN，不把offline tests写成hardware ready/formal pass/release consumed/G4-06 unlocked；
- 普通工程问题不升级Human/Advisor；GUIDE/RESEARCH immutable。

## 7. Handoff and sole stop

ER必须记录activation topology、source/test before/after identity、public signatures、AST/CodeGraph owner bindings、每个无I/O injection/probe的
exception与I/O计数、canonical forged-result rejection、accepted roundtrip、exact validation counts、zero retry事实、test-root cleanup及全部prohibited
access为0。

成功只能提出`G4_04_E2_FINAL_CANONICAL_OWNER_BINDING_ACCEPTANCE_CANDIDATE`；失败记录exact first failing gate并立即停止。Executer停于
`RETURN_FOR_G4_04_E2_FINAL_CANONICAL_OWNER_BINDING_REVIEW`。Planner review后只有Orchestrator可决定G4-04 disposition；G4-05至多成为
planning candidate，不自动执行或生成PLAN，G4-06保持locked。
