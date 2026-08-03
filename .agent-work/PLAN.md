# REF-G4-03-ZERO-READINESS：fresh real zero/readiness 单包

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_ZERO_READINESS`

**Executable：** `true`（仅在Orchestrator将FULL对齐为同一contract并创建exact activation commit后生效）

**Active task count：** `1`

**Active task：** `REF-G4-03-ZERO-READINESS`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_03_ZERO_READINESS_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-ZERO-READINESS-SINGLE-OWNER-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_BOUNDED_ZERO_READINESS","executable":true,"active_task_count":1,"active_task":"REF-G4-03-ZERO-READINESS","reference_task_id":"REF-G4-03-ZERO-READINESS","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_SINGLE_ZERO_READINESS_PACKAGE","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"5d05cc14286af0f96b9021401f44d3c72a348911","expected_parent_tree":"19ae4e14d90b12b5872ff841220284e27f297b00","expected_subject":"docs(plan): activate g4 zero readiness","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260803-1316.md",".agent-work/archived/PLAN-20260803-1316.md"],"child_sha_recorded_in_plan":false},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1316.md","bytes":8895,"sha256":"5eb3d0076f27fafcd69a8794511f29ac23798894abe92a5a0332f0f53966d88b"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1316.md","bytes":2439,"sha256":"b25a380efaf685057e0c90573eea30854ffafb7c5116d4af06bc92a27a4400fc"},"single_current_action":"implement_test_and_run_one_repo_owned_fresh_real_zero_readiness_composition_with_bounded_read_only_and_zero_only_device_calls","allowed_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py","tests/test_p7_successor_zero_readiness.py","tmp/run-g4-zero-readiness.zsh",".agent-work/EXECUTION_RESULT.md"],"thermal_giant_module_edits":0,"parallel_semantic_owner_creation":0,"fresh_root":"/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-5d05cc14286a-20260803T191648Z","fresh_root_mode":448,"artifact_mode":384,"expected_duration_seconds_max":480,"visible_terminal_required":false,"real_execution_invocation_cap":1,"root_acquisition_cap":1,"retry":0,"alternate_root":0,"offline_bounded_correction_cap":1,"camera_health_get_cap":1,"camera_config_get_cap":1,"camera_capture_calls":0,"strip_verified_zero_cap":3,"strip_shell_zero_cap":1,"strip_nonzero_calls":0,"ray_set_intensity_zero_cap":4,"ray_get_cct_cap":3,"ray_get_node_config_cap":1,"ray_nonzero_calls":0,"source_isolation_validation_cap":2,"python_finally_required":true,"shell_trap_required":true,"independent_final_zero_required":true,"terminal_seal_required":true,"release_consumption":0,"retained_r3_access":0,"legacy_release_access":0,"other_external_experiment_payload_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"config_write_calls":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"targeted_test_invocation_cap":2,"focused_test_invocation_cap":1,"full_suite_invocation_cap":1,"compile_static_invocation_cap":1,"codegraph_sync_cap":1,"release_consumption_authorized":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","device_authorized":true,"camera_authorized":true,"ray_authorized":true,"strip_authorized":true,"capture_authorized":false,"formal_r6_authorized":false,"td_c_authorized":false,"success_candidate_proposal_allowed":true,"planner_stop":"RETURN_FOR_G4_03_ZERO_READINESS_REVIEW","future_reference_task":"REF-G4-04-E2","future_stage_locked":true}`

## 1. Intake与activation gate

Executer开始前必须同时证明：

1. 当前HEAD是Orchestrator创建的activation commit，且是
   `5d05cc14286af0f96b9021401f44d3c72a348911`的direct child；subject与五个changed paths严格匹配machine row。
2. branch为`main`；除activation五路径外无dirty/untracked内容。
3. PLAN与FULL strict machine parser均通过；两者contract均为
   `G4-ZERO-READINESS-SINGLE-OWNER-V1`，active task/count为
   `REF-G4-03-ZERO-READINESS / 1`。
4. G4-02 prerequisite仍为accepted；只对exact G4-01 release的validator/eligibility/consumable为true，
   release consumption authorization为false；retained R3仍为
   `RETAINED_UNVALIDATED_UNCONSUMED`。
5. 两个1316 archive存在且metadata内的source body identity分别为7943 bytes /
   `6f53b21b90fb71bb07f10978a1584524be4153ba0235e587c15c5078e05eee36`
   与1489 bytes /
   `43b03d56345a3de0735468e33827161fb626bd216656393752c7e05790b0d06f`。
6. fresh root及其symlink均不存在；不得删除、移动、复用或改名任何旧external root。

任一项不满足：不编辑production/test/wrapper、不访问网络或设备，在ER精确记录drift并stop。禁止reset/clean/checkout。

## 2. Maintainability与owner contract

CodeGraph已确认现有底层source of truth：

- strip zero/identity/generation：`control.esphome.verified_light(0,0,0,0,0)`；
- Ray zero/readback/identity：`control.ray120c.set_cct`、`get_cct`、`get_node_config`；
- 双源零态语义：`optimization.hsi_source_evidence.validate_both_off`；
- camera health/config：`control.camera_remote.read_remote_health`与
  `RemoteCameraBackend.connect/_load_settings`；
- cleanup：`control.all_off.turn_everything_off`；
- shell safety模式：tracked `tmp/run-p7-thermal-diagnostics.zsh`、
  `tmp/run-strip-state-readback-preflight.zsh`。

现有EQ-R6 prelaunch owner会生成formal launch handoff并绑定旧实验授权语义，strip-state preflight会执行非零转换；
两者均不得直接调用。Executer只新增一个小型Guide4 stage composition owner
`p7_successor_zero_readiness.py`、一个对应行为测试文件和一个tracked wrapper。新owner只能编排上述底层owner、
canonical persistence、chronology和call ledger；不得复制ESPHome/Ray/camera协议、zero validator或serialization语义。
不得修改：

- `measure_p7_thermal_diagnostics.py`
- `p7_thermal_diagnostics.py`
- `analyze_p7_thermal_diagnostics.py`
- 任何既有control owner、config、GUIDE、RESEARCH、PLAN、FULL或archive。

## 3. Frozen lab identity、endpoint与budget

Exact target如下；secret只从既有环境/`.env`加载，禁止输出、序列化或写入CLI：

- strip：expected name `bedroom-rgbww-strip`，host
  `bedroom-rgbww-strip.local`，port `6053`，state entity
  `rgbww_commanded_state`，curve
  `config/channel/code-duty-curve.json`；
- camera bridge：base URL `http://ibobby-rpi-4.local:8088`，
  GET `/health`与authenticated GET `/v1/config`，backend `remote`，
  model `Canon EOS R6 Mark III via r6-camera-bridge`；
- camera capability：
  `remote_v2_capture_timing_v1`且`capture_with_timing` callable；只检查，
  不调用`/v1/capture`或`/v2/capture`；
- Ray：`ws://127.0.0.1:33782`，node `40165-560387`，client `1`，
  timeout `3.0s`，zero命令固定`cct=5600,intensity=0,gm=100`。

Camera health/config各最多1次，backend busy retry必须为0，每次timeout最多10秒；ESPHome单次state timeout最多5秒；
Ray单次timeout 3秒。成功路径总上限：verified strip zero 3次、shell strip zero 1次、Ray set intensity0 4次、
Ray get_cct 3次、Ray get_node_config 1次、source-isolation validation 2次。所有nonzero/capture/config write计数必须为0。
不得扩大endpoint、target、timeout、call count、retry、recovery path或root。

预计完成时间少于8分钟（含测试与唯一real run），因此使用普通前台执行；禁止后台进程、Terminal launch和automation。
若执行前预计会超过10分钟，停止回Orchestrator，不得自行改变launch方式。

## 4. 单一实现动作与测试

Executer按以下顺序完成一次动作：

1. 实现owner与wrapper，先以fake dependencies覆盖：
   fresh/absolute root、0700/0600、exclusive/canonical JSON、secret absence、exact inventory；
   camera identity/health/config/capability；strip generation严格增加且五通道为零；Ray node/readback intensity0；
   source isolation；call/time caps；capture/nonzero禁止；任一阶段失败仍执行Python finally、shell trap、independent final-zero并写terminal FAIL；
   signal/child failure/cleanup failure优先级及terminal non-self-reference。
2. 运行targeted tests；若首次失败，只允许在这三个新增文件内做一次bounded engineering correction并重跑targeted。
   第二次同一边界失败立即stop，不得设备调用。
3. 运行focused tests：
   新测试、camera_remote、ray120c、esphome、all_off、hsi source evidence及现有P7 wrapper/contract相关测试。
4. 运行full suite、compileall、`git diff --check`；随后`codegraph sync`并query新owner到所有底层owner的调用边。
5. 只有全部offline gate通过，才允许唯一一次real wrapper前台调用。

Executer不得commit；Orchestrator在Planner接受后处理focused commit。

## 5. 唯一real chronology与evidence schema

Wrapper必须将以下顺序固定且可测试：

1. exclusive acquisition exact fresh root，mode 0700；写
   `frozen-inputs.json`；
2. generation-bearing strip zero；Ray exact zero + CCT readback + node config；camera health/config/capability；
3. 写`strip-readiness.json`、`ray-readiness.json`、
   `camera-readiness.json`与`source-isolation.json`；
4. Python `finally`无条件执行verified strip zero与Ray exact intensity0，写
   `python-finally-zero.json`；
5. wrapper在EXIT/INT/TERM/HUP trap中无条件调用repo-owned all-off，写
   `all-off-shell.json`、`all-off-shell.stderr.log`、
   `all-off-shell.exit-status.txt`；
6. shell cleanup后调用owner的finalize-only入口，重新执行generation-bearing strip zero、Ray exact zero/readback和
   第二次`validate_both_off`，写`independent-final-zero.json`；
7. 写`runner.log`、`wrapper.log`、`wrapper-result.json`，最后写
   `terminal-seal.json`。Terminal seal引用此前每个artifact的path/bytes/SHA/mode，不自引用。

每个JSON必须canonical、单换行、mode 0600；text/log也为0600。Terminal PASS必须同时要求exact inventory、全部stage PASS、
device identity一致、strip三次verified generation逐次严格增加、全部五通道零、Ray intensity始终0、camera capture/config-write 0、
root fresh、无临时文件、child/wrapper/shell cleanup exit均0、所有call ledger exact。任何失败同样保留同一root中的FAIL seal；
不得重试、换root、修设备或转入G4-04。

## 6. Acceptance与handoff

ER必须记录：

- activation topology、PLAN/FULL parser与archive identity；
- 新owner/test/wrapper bytes/SHA与CodeGraph调用边；
- targeted/focused/full/compile/diff结果；
- root device/inode/mode与exact inventory；
- 每项artifact device/inode/mode/bytes/SHA；
- redacted endpoint/identity结果、chronology、call ledger、所有exit status；
- `capture=0`、`nonzero=0`、`release_consumption=0`、formal/TD-C=0；
- terminal PASS或精确失败分类、残留进程检查、最终zero状态。

PASS仅构成G4-03 candidate，不能自行授予G4-04、release consumption或formal权限。Executer写完ER即在
`RETURN_FOR_G4_03_ZERO_READINESS_REVIEW`停止；Planner随后独立只读验收并先归档PLAN/ER。
