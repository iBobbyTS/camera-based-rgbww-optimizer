# REF-G4-04-E2：bounded offline result/replay contract closure

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_OFFLINE_RESULT_REPLAY_CLOSURE`

**Executable after activation：** `true`

**Active task count after activation：** `1`

**Active task after activation：** `REF-G4-04-E2`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-E2-BOUNDED-RESULT-REPLAY-CLOSURE-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_OFFLINE_RESULT_REPLAY_CLOSURE","executable":true,"active_task_count":1,"active_task":"REF-G4-04-E2","reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_BOUNDED_OFFLINE_RESULT_REPLAY_CLOSURE","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"f385288e2a465350d9d66801578b7bdc5e211122","expected_parent_tree":"ebcf5a67b563e6684e7f40b7cb23da625768613d","expected_subject":"docs(plan): activate bounded e2 replay closure","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"execution_authorized_before_activation":false,"single_current_action":"close_existing_e2_result_persist_replay_and_terminal_contract_with_one_shared_validator_and_existing_thermal_owners","allowed_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","tests/test_p7_successor_e2.py"],"existing_production_files_edited":1,"existing_test_files_edited":1,"new_production_modules":0,"new_test_files":0,"giant_p7_module_edits":0,"config_edits":0,"wrapper_edits":0,"full_edits_by_executer":0,"plan_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"corrective_suffixes":0,"new_task_ids":0,"source_checkpoint":"f385288e2a465350d9d66801578b7bdc5e211122","source_tree":"ebcf5a67b563e6684e7f40b7cb23da625768613d","guide":{"path":"advisor/4/4.GUIDE.md","sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35"},"rejected_candidate_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":24222,"sha256":"20bd2ca3fe1bbf2931b7f2605c307ed00fe8c0848734e68edbe35600ba8c4fed"},"rejected_candidate_tests":{"path":"tests/test_p7_successor_e2.py","bytes":16170,"sha256":"354f61e34ba714895f0fcd2b0ac50ef654ed8f685174f6ef76a1719d08c3ec1d"},"thermal_owner":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","bytes":203416,"sha256":"14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1"},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1514.md","bytes":15973,"sha256":"68e806c7f6610a26f7d156ff5258ea279f95210e4bd5751f2005c26ed8ecff6b"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1514.md","bytes":8688,"sha256":"243a00e4c890ff232c9068f549c45b66a748954ceec7dc13ee56916167db496d"},"existing_e2_package_status":"REJECTED_UNTRUSTED_HISTORICAL_IDENTITY_ONLY_NO_ACCESS","existing_e2_root_access_allowed":false,"new_e2_evidence_root_allowed":false,"production_evaluation_cap":0,"production_persist_cap":0,"production_replay_cap":0,"unit_test_ephemeral_tempdir_only":true,"external_payload_access":0,"release_root_access":0,"predevice_root_access":0,"readiness_root_access":0,"retained_r3_access":0,"legacy_r2_access":0,"deep_corrective_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"targeted_test_invocation_cap":2,"focused_test_invocation_cap":1,"full_suite_invocation_cap":1,"compile_static_invocation_cap":1,"source_scan_invocation_cap":1,"codegraph_sync_cap":1,"offline_bounded_correction_cap":1,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_REVIEW","future_reference_task":"REF-G4-05-RAY-R6-STAGE-GATE","future_stage_locked":true}`

## 0. Activation gate

本文件当前只是等待 Orchestrator activation 的 draft；在 Orchestrator 将 FULL 与本 machine row 对齐并创建 exact activation
commit 前，Executer不得执行任何步骤。Activation必须满足：

1. parent exact为`f385288e2a465350d9d66801578b7bdc5e211122`，parent tree为
   `ebcf5a67b563e6684e7f40b7cb23da625768613d`，branch为`main`，pre-activation worktree除Planner draft外无漂移；
2. subject exact为`docs(plan): activate bounded e2 replay closure`；changed paths exact且仅为
   `.agent-work/PLAN.md`、`.agent-work/EXECUTION_RESULT.md`、`.agent-work/FULL_PLAN_REFERENCE.md`；
3. activation child中PLAN/FULL active task count为`1/1`，task均为`REF-G4-04-E2`，canonical next singleton不变；
4. GUIDE、thermal owner、candidate source/test与review archives identity分别匹配machine row；
5. retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`，release consumption、device、formal R6、TD-C及G4-05/06 authority仍为false/0。

任一项失败：不得编辑source/test；只在ER记录exact drift并stop。不得reset、clean、checkout或从archive复制语义。

## 1. Maintainability与owner preflight

这是persistence/provenance高风险边界。现有`p7_successor_e2.py`是唯一E2 integration/evidence owner，现有
`p7_retained_r3_provenance_io.py`是filesystem/canonical serialization owner，现有`p7_thermal_diagnostics.py`是formal plan及
machine status owner。直接在E2 owner内收敛shared validation不会扩大三个巨型P7模块，也不需要新module。

Executer必须保持以下ownership：

- 新增或收敛一个E2内部closed result validator，由evaluate、persist、replay三条入口共同调用；不得为三条入口复制规则；
- 删除E2本地完整formal plan字面合同；formal plan只通过既有`build_td_b_r6_formal_plan`与
  `validate_td_b_r6_formal_plan`取得和验证；decoded plan还必须与builder结果exact相等；
- 删除/收敛E2本地machine status字面合同；decoded status必须与既有`td_b_r6_machine_status`结果exact相等；
- persistence、canonical JSON、file identity、root inventory仍只委托现有provenance owner；不得复制serialization/filesystem；
- 不得新增module、CLI、wrapper、adapter、controller、parallel semantic owner或无关重构；不修改三大巨型P7模块。

若无法在这两个existing source/test文件内维持上述owner边界，写ER并stop回Orchestrator。

## 2. Shared closed result contract

在现有E2 owner内建立一个shared closed validator，并使以下路径全部复用：

1. `evaluate_e2_preformal_gate`构造result后、return前验证；
2. `persist_e2_package`在任何create/persist调用前验证传入result；
3. `replay_e2_package`decode result后、接受terminal或返回PASS前验证。

Validator必须fail closed验证：

- top-level exact keys为schema、status、reference ledger、formal plan、machine status、guards、authority；禁止missing/extra；
- schema/status exact；所有nested mappings/lists拥有closed exact keys、order/shape和strict type，bool不得当int；
- guards key set exact等于evaluator固定guard set，且每一项必须`is True`；empty、missing、extra、truthy非bool及任一false均拒绝；
- authority key set exact，boolean位必须逐项`is False`，计数位必须type exact int且等于0；禁止extra/missing；
- reference ledger exact等于传入/frozen `E2Input`的唯一projection，包括source checkpoint/tree、GUIDE/policy、G4-01/02/03、
  protected sources、G4-03 historical transport/effect字段及顺序；不得只核对部分identity；
- formal plan先交由既有thermal validator，再与既有builder的JSON-native exact输出相等；不得保留第二套field literal；
- machine status与既有owner的JSON-native exact输出相等；不得保留第二套envelope/lock literal；
- canonical JSON projection稳定，deep immutable evaluator output仍成立。

Shared validator可以通过依赖注入复用evaluator已取得的existing-owner结果，避免无意义重复调用；但persist/replay必须独立取得
existing owner expected值，不能信任result自述。任何existing owner exception原样fail closed为E2 rejection；不得降级为PASS。

## 3. Closed terminal与synchronized forgery

成功terminal必须有closed validator：top-level exact keys、schema/status、result identity、artifact count、self-reference、retry、alternate
root及完整authority nested keys/type/value均exact；禁止missing/extra/truthy兼容。Terminal result reference必须等于replay刚读取的result
regular-file identity（name/device/inode/mode/bytes/SHA）；terminal自身不得自引用。

Replay接受顺序必须确保：inventory与regular-file约束通过后，result closed contract、terminal closed contract、terminal→result identity
绑定全部通过，才返回deep-immutable PASS。即便攻击者同步重写result bytes/SHA并重建匹配terminal reference，伪造/open result也必须在
shared semantic validator处失败。Fail seal行为仍保持single root/no retry/no alternate root，不能被当作PASS terminal。

## 4. Tests

只修改现有`tests/test_p7_successor_e2.py`，保留全部已有behavior assertions并新增至少：

1. evaluate、persist、replay三入口都证明调用同一closed validator语义；persist在root/create/persist前拒绝forged/open result；
2. result top-level missing/extra；guards empty/missing/extra/false/truthy非bool；authority每一bool/zero、missing/extra/type drift；
3. reference ledger各section、artifact identity/order/count、G4-03 transport/effect、protected sources的tamper；
4. formal plan missing/extra/field/order/shutter/budget/failure-contract tamper经existing thermal owner拒绝，且测试证明E2不再拥有完整plan literal；
5. machine status missing/extra/envelope/locks/R6 field tamper相对existing owner拒绝；
6. terminal top-level与authority missing/extra/type/value、result identity name/device/inode/mode/bytes/SHA drift全部拒绝；
7. 同步伪造result与terminal：重写result并更新terminal reference后仍fail closed，且不产生PASS replay；
8. accepted evaluator result仍可由测试专用ephemeral package round-trip，canonical bytes/modes/inventory/deep immutability不退化；
9. AST/CodeGraph继续证明无device/network/process/env/controller边，formal/machine语义只指向existing thermal owner。

测试仅可使用in-memory/fake adapter，以及测试框架既有、fresh、自动清理的
`/Volumes/4T/temp/rgbww-optimizer`下`TemporaryDirectory`。它不是新的durable E2 evidence/experiment root；不得使用machine row中的已拒E2
root，不得读取任何external payload。Owner不得执行production evaluation、persist或replay，也不得留下test root/residual。

## 5. Validation顺序与预算

1. Targeted：`.venv/bin/python -m unittest tests.test_p7_successor_e2`。首次失败只允许在exact source/test内一次bounded correction并重跑；
   第二次同边界失败立即stop回Orchestrator，不创建suffix或task。
2. Focused一次：运行successor lineage、predevice、zero-readiness、E2、R6 contract、thermal runner与provenance owner相关unittest集合；
   全部通过，记录invocation与exact test count。
3. Full suite一次：`.venv/bin/python -m unittest discover -s tests`；随后
   `.venv/bin/python -m compileall -q src tests`和`zsh -n tmp/run-p7-thermal-diagnostics.zsh`。
4. 对activation HEAD到worktree的exact changed source/test调用repo-owned
   `p7_thermal_diagnostics.scan_td_b_r6_offline_sources`做baseline-aware source scan；要求scanned paths exact、findings 0、private/env/
   network target/unsafe absolute path/symlink/changed-path越界均0。
5. `git diff --check`；证明diff paths仅为本PLAN允许的source/test/ER，且GUIDE/RESEARCH、FULL/PLAN、config、wrappers、三大P7模块、
   archives相对activation HEAD未变。
6. `codegraph sync`一次，再query E2 owner：result validation为单一shared owner；formal/machine指向thermal owners；I/O指向provenance
   owner；无device/network/process/controller边。
7. 用repo-owned `parse_plan_machine_contract`与`parse_full_plan_machine_state`读取complete bytes；要求PLAN/FULL strict parse通过、active
   task为`REF-G4-04-E2`且count为`1/1`，canonical next singleton不变。

本包不生成新的durable package或evidence root；之前`13/245/892`只能作为rejected candidate历史证据，本次必须记录实际fresh targeted、
focused、full结果，不能继承为acceptance。

## 6. Safety、authority与failure convergence

- 全程offline code/test-only；不得访问已拒E2 root或任何G4-01/02/03/retained/legacy/deep-corrective external payload；不得创建新的
  durable E2、formal或experiment root。
- release consumption、device/network/app/process/listener/camera/Ray/strip/capture/nonzero light/formal R6/TD-C/firmware/deployment调用均为0。
- 不得生成execute-authorized formal plan，不得进入或生成G4-05/06 PLAN，不得把offline tests表达为hardware readiness、formal pass、
  release consumed或G4-06 unlock。
- 本轮是同一`REF-G4-04-E2`的一次bounded engineering contract closure，不创建corrective suffix/new task/new root。
- 若碰到frozen source/scientific contract矛盾、GUIDE hard stop或无法安全选择科学分支，立即fail closed记录并stop；普通工程问题不升级
  Human/Advisor。

## 7. EXECUTION_RESULT handoff与唯一stop

ER必须记录：activation HEAD/tree/subject/path topology；source/test before/after bytes/SHA；shared validator三入口；existing thermal/provenance
owner调用与无local literal证据；所有result/terminal/synchronized-forgery negative cases；targeted/focused/full/compile/static/source scan/
diff/CodeGraph/machine parser结果；test temp cleanup；全部prohibited access/call/root counts为0。

成功只能提出`G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_ACCEPTANCE_CANDIDATE`；失败记录exact boundary与是否已使用唯一bounded correction。
Executer停止于`RETURN_FOR_G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_REVIEW`。Planner必须独立review并先归档PLAN/ER；只有Orchestrator可给
G4-04 terminal disposition并把G4-05变为planning-only。本PLAN不授权G4-05/06 execution。
