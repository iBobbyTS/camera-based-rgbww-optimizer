# REF-G4-06-RAY-R6 Route A visible-Terminal validation continuation

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION`

**Executable：** `true`

**Active task count：** `1`

**Reference task：** `REF-G4-06-RAY-R6`

**Total contract route：** `G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1`

**Current phase：** `FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_REMAINING_VALIDATION`

**Planner decision：** `CONTINUE_LONG_TASK_PACKAGING_NO_CANDIDATE_ACCEPTANCE_OR_REJECTION`

**Planner stop：** `RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_VISIBLE_TERMINAL_VALIDATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-RAY-R6","reference_task_id":"REF-G4-06-RAY-R6","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_ROUTE_A_FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_VALIDATION_AFTER_EXACT_ACTIVATION","route":"FINAL_CODE_FIRST_FINAL_PACKAGE_REMINT_CONVERGENCE","current_phase":"FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_REMAINING_VALIDATION","planner_decision":"CONTINUE_LONG_TASK_PACKAGING_NO_CANDIDATE_ACCEPTANCE_OR_REJECTION","candidate_disposition":"PRESERVED_UNACCEPTED_UNREJECTED_PENDING_REMAINING_VALIDATION","production_failure_count_increment":0,"activation_state":"WAITING_ORCHESTRATOR_FULL_ALIGNMENT_COMMIT","activation_commit":{"expected_parent":"7214ff5eb797d2716d7b9d4bdb34324f5febe350","expected_parent_tree":"d9dc5dcf0e2177a11f2b6651fe707fdca8b8ef6e","expected_subject":"docs(plan): continue Route A validation in Terminal","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260804-1848.md",".agent-work/archived/PLAN-20260804-1848.md"],"excluded_candidate_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"direct_non_merge_child":true,"child_sha_recorded_in_plan":false},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-RAY-R6","active_plan_contract_id":"G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-RAY-R6","canonical_next_reference_task":"REF-G4-06-RAY-R6","canonical_next_reference_status":"ACTIVE_ROUTE_A_FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_VALIDATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"ACTIVE_ROUTE_A_FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_VALIDATION","g4_06_state":{"route":"FINAL_CODE_FIRST_FINAL_PACKAGE_REMINT_CONVERGENCE","total_contract_route":"G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1","status":"ACTIVE_ROUTE_A_FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_VALIDATION","task_id":"REF-G4-06-RAY-R6","authority_owner":"MATCHING_LIVE_PLAN_ONLY","full_top_level_non_authorizing":true,"final_code_immutable_checkpoint":null,"final_code_tree":null,"final_package_binding":null,"production_source_frozen_no_further_code_change_before_formal":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"g4_07_unlocked":false}},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260804-1848.md","bytes":17893,"sha256":"db8230483b4d0435636e32c5fe23a3c55fc81e5d75f0bbfd0783f6e9bf08df74"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260804-1848.md","bytes":9852,"sha256":"3b634c16cd6dcd9efce2945236d2d68fcfe85f0fcb747a22532810acc6fd1ed2"},"partial_execution_result":{"source_bytes":8363,"source_sha256":"53b944f43552d9454f05a67683406a966ca34d3141f7f4c1b5ae82e572d65acf","status":"STOPPED_FOR_ORCHESTRATOR_VISIBLE_TERMINAL_REPACKAGING_NOT_A_CANDIDATE_REJECTION","tooling_correction_count":1,"tooling_correction_zero_modification":true},"candidate_identity":{"source_path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","source_bytes":94324,"source_sha256":"c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83","test_path":"tests/test_p7_td_b_r6_stage_gate.py","test_bytes":133201,"test_sha256":"479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e","overall_insertions":102,"overall_deletions":9,"production_insertions":35,"production_deletions":8,"candidate_writes_authorized":0},"inherited_validation":{"targeted":{"command":".venv/bin/python -m unittest -v tests.test_p7_td_b_r6_stage_gate","passed":47,"total":47,"duration_seconds":182.148,"exit_code":0,"rerun_authorized":false},"compile":{"command":".venv/bin/python -m py_compile src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py tests/test_p7_td_b_r6_stage_gate.py","exit_code":0,"rerun_authorized":false},"identity_condition":"EXACT_CANDIDATE_BYTES_SHA_AND_TWO_PATH_DIFF_MUST_REMAIN_UNCHANGED"},"validation_scratch":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-route-a-terminal-validation-7214ff5eb797-20260804T184848Z","classification":"FRESH_VALIDATION_STDIO_LOG_ROOT_NOT_EXPERIMENT_NOT_PACKAGE_NOT_FORMAL","must_not_preexist":true,"inventory":["command-seal.json","validation.stdout.log","validation.stderr.log","validation.exit"],"other_files_allowed":false,"alternate_root_count":0},"single_terminal_launch":true,"terminal_launch_count":1,"terminal_retry_count":0,"terminal_resume_count":0,"terminal_alternate_count":0,"visible_macos_terminal_required":true,"three_sparse_liveness_checks_required":true,"automation_owned_by_orchestrator":true,"expected_duration_over_10_minutes":true,"focused_required_once":true,"post_change_identity_required":true,"compile_rerun_required":false,"codegraph_sync_required_once":true,"codegraph_query_required_once":true,"diff_scope_machine_required":true,"full_suite_required_once":true,"full_suite_retry_count":0,"previous_interrupted_full_reusable":false,"allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"same_reference":true,"new_task_ids":0,"corrective_suffixes":0,"external_existing_root_access":0,"formal_root_access":0,"new_experiment_package_formal_roots":0,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"formal_execution_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"td_c_authorized":false,"planner_stop":"RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW"}`

## 1. Review disposition

Planner对partial ER与current exact candidate的处置是：

`CONTINUE_LONG_TASK_PACKAGING_NO_CANDIDATE_ACCEPTANCE_OR_REJECTION`

这不是candidate acceptance、rejection、production-seam failure、科学/formal/device failure、
GUIDE hard stop或权限请求；production failure count不增加。Candidate保持exact two-file dirty state，
不得修改、修补、重写、stage或commit。一次`apply_patch` hunk格式错误未修改文件，归类为tooling
correction，不计production failure。

已通过且可继承：

- targeted：exact `47/47`、`182.148s`、exit `0`；
- compile：exit `0`；
- candidate exact source/test bytes与SHA如machine row；
- external/device/formal访问和effect均为0。

Focused、post-change CodeGraph、fresh full均未启动；不能推断其结果。更早中断full仍为
`INTERRUPTED_UNPROVEN_NOT_REUSABLE`，不得恢复、补接或复用。

## 2. Activation gate

Orchestrator必须先创建exact activation commit：

- direct non-merge parent：
  `7214ff5eb797d2716d7b9d4bdb34324f5febe350`；
- subject：
  `docs(plan): continue Route A validation in Terminal`；
- changed paths精确为machine row列出的五个orchestration files；
- source/test candidate必须继续dirty且绝不进入activation commit；
- FULL只同步到`required_full_machine_state`。FULL始终
  `executable=false`、`full_is_non_executable_reference=true`；matching live PLAN是唯一
  execution authority。

Executer开始前用repo-owned parser及Git只读检查证明activation topology/path set、PLAN/FULL active
`1/1`、same task/contract、required FULL subset exact，并重算candidate bytes/SHA/numstat。
任一identity不符立即停回Orchestrator；不得适配、恢复或改candidate。

## 3. Frozen candidate and inherited checks

Exact candidate：

- source：`94324` bytes /
  `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83`；
- test：`133201` bytes /
  `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e`；
- relative HEAD：exact two paths，overall `+102/-9`，production `+35/-8`；
- candidate source/test writes authorized：`0`。

Targeted与compile仅在上述identity逐项保持exact时继承，且禁止重跑。Pre-Terminal identity gate还须
证明现有single attestation owner、无new schema/successor/controller/adapter与production soft cap
仍满足已归档PLAN，但不得运行CodeGraph；post-change CodeGraph属于Terminal sequence。

## 4. Fresh validation scratch/log root

唯一允许创建的新root：

`/Volumes/4T/temp/rgbww-optimizer/g4-route-a-terminal-validation-7214ff5eb797-20260804T184848Z`

它严格分类为`FRESH_VALIDATION_STDIO_LOG_ROOT_NOT_EXPERIMENT_NOT_PACKAGE_NOT_FORMAL`，只保存：

- `command-seal.json`
- `validation.stdout.log`
- `validation.stderr.log`
- `validation.exit`

Executer只可对exact path做non-following存在性检查；它必须不存在。只能在Human可见macOS Terminal
的单次launch内以exclusive fresh create建立；禁止alternate、retry、resume、覆盖或增加第五个文件。
`command-seal.json`须在执行前冻结cwd、activation HEAD、candidate hashes、全部exact argv、顺序、
single-launch/retry/resume/alternate counters与stdout/stderr/exit paths。Logs只记录命令stdout/stderr；
`validation.exit`记录整个fail-closed sequence的最终exit。

禁止读取、stat、list、describe、修改、删除或消费任何其他existing external experiment/package/
formal root。该validation root不提供实验、release、formal或hardware readiness credit。

## 5. One continuous visible-Terminal sequence

在同一次visible Terminal owner中按顺序执行，不得拆包：

1. 重新证明candidate exact bytes/SHA/two-path numstat；不写source/test。
2. Focused integration，exact一次：

```text
.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics
```

3. 不重跑已通过compile；改做post-focused static identity：重新核对两文件bytes/SHA、exact diff与
   `git diff --check`。任一变化视为candidate drift并停止。
4. `codegraph sync` exact一次，然后query exact一次，证明existing stage-gate attestation owner仍唯一、
   loader/launch无parallel validator、successor seam、controller或adapter。
5. Repo-owned PLAN/FULL parser、required subset、activation topology、exact changed scope与
   all-authority-false检查。
6. 只有1–5全部exit 0，才运行唯一fresh full：

```text
.venv/bin/python -m unittest discover -s tests
```

7. 写入final stdout/stderr/exit evidence并退出；不得运行第二次full或任何修复命令。

Focused或任一pre-full gate失败时，full必须保持not started；记录真实失败并退出。Full失败时记录
真实result并退出，retry为0。任何失败均不得修改candidate、创建suffix/route/root或现场纠偏。

## 6. Long-task ownership

Executer必须把sequence启动在Human可见macOS Terminal，记录Terminal window/tab、PID、exact command
seal与start time。启动后进行三次稀疏read-only liveness checks，证明同一PID/command仍存活且log
单调增长；不得启动第二owner或密集轮询。

第三次liveness确认后，Executer把evidence写入live ER并返回Orchestrator。Automation只由
Orchestrator创建；Planner/Executer不得创建。Orchestrator按预计完成窗口创建一次wake automation，
将goal标为blocked并停止轮询。

Human恢复goal后只检查一次：

- 未完成：保留同一Terminal owner与automation，再次blocked，不轮询；
- 已完成：Orchestrator删除automation，Executer只读取本PLAN exact validation root的四个文件，
  核对seal并finalize ER；不得重启、resume或补跑命令。

如果sequence在第三次liveness前已经terminal，也直接取得同一owner的terminal evidence并finalize
ER；不得为满足形式启动新进程。

## 7. Exact scope and authority

Continuation只可修改：

- `.agent-work/EXECUTION_RESULT.md`

Candidate source/test为read-only preserved inputs。PLAN、FULL、GUIDE、RESEARCH、其他source/test/config
只读。除exact fresh validation log root四文件外，不得写外部路径。

本PLAN不授权package remint、final-code checkpoint commit、existing package consumption、formal root、
device、network、camera、Ray、strip、capture、release、analysis、formal R6或TD-C。Backend/root/device
effect必须为0。

## 8. Final EXECUTION_RESULT and stop

Final ER必须记录：

- activation topology及PLAN/FULL exact machine evidence；
- inherited targeted/compile command、count、duration、exit及candidate identity条件；
- Terminal window/tab/PID、single launch、三次liveness与automation handoff evidence；
- exact validation root identity、four-file inventory、command-seal/hash、stdout/stderr/exit identities；
- focused、post-change identity、CodeGraph sync/query、scope/machine、fresh full的exact argv、顺序、
  start/end、exit与test counts；
- focused/pre-full/full terminal branch，明确full是否started；
- candidate final bytes/SHA/numstat保持exact及candidate writes `0`；
- tooling/production correction counts分别为`1/0`；
- external existing roots与device/network/camera/Ray/strip/capture/release/formal/backend effects全为0；
- 不猜测未来code checkpoint/tree。

Terminal sequence无论pass/fail都回到同一Planner stop。成功status request：

`READY_FOR_PLANNER_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`

失败status request：

`READY_FOR_PLANNER_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_VALIDATION_FAILURE_REVIEW`

唯一stop：

`RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`
