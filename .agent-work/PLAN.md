# REF-G4-06-RAY-R6 Package A production CLI launch seam

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_PACKAGE_A_ENGINEERING_ONLY`

**Executable：** `true_after_exact_orchestrator_activation`

**Active task count：** `1`

**Active reference task：** `REF-G4-06-RAY-R6`

**Contract：** `G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V1`

**Planner stop：** `RETURN_FOR_G4_06_PACKAGE_A_TWO_PHASE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_PACKAGE_A_ENGINEERING_ONLY","executable":true,"active_task_count":1,"active_task":"REF-G4-06-RAY-R6","reference_task_id":"REF-G4-06-RAY-R6","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_PACKAGE_A_ENGINEERING_ONLY_AFTER_EXACT_ORCHESTRATOR_ACTIVATION","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"ca0a4673bba0b0c646294f2199bfacdb55374702","expected_parent_tree":"5ca9644d3745b9eac033740a51b43161876ede98","expected_subject":"docs(plan): activate ray r6 production launch seam","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"activation_dirty_contract":{"exact_paths":[".agent-work/EXECUTION_RESULT.md"],"exact_initial_sha256":{".agent-work/EXECUTION_RESULT.md":"fb4c677af69df9ed9bfa70173ea285560159172baa904c475d76ebe18f07e6e4"},"other_dirty_allowed":false},"single_current_action":"route_existing_stage_gate_materializer_and_narrow_hook_through_production_cli_without_launching","package":"A_PRODUCTION_CLI_LAUNCH_SEAM_ENGINEERING_ONLY","candidate_code_child":{"expected_subject":"feat(stage-gate): route ray r6 formal launch owner","expected_parent_is_activation_child":true,"expected_changed_paths":["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"child_sha_recorded_in_plan":false},"allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"new_modules":0,"new_test_modules":0,"controller_files":0,"corrective_suffixes":0,"new_task_ids":0,"measure_maintainability_preflight_required":true,"semantic_owner":"p7_td_b_r6_stage_gate","measure_change_role":"NARROW_CLI_PARSE_AND_DISPATCH_ONLY","production_wrapper":"tmp/run-p7-thermal-diagnostics.zsh","production_wrapper_changes_allowed":false,"production_launch_chain":["p7_td_b_r6_stage_gate.load_and_validate_stage_gate_package","p7_td_b_r6_stage_gate.validate_committed_source_attestation","p7_td_b_r6_stage_gate.materialize_runtime_plan","measure_p7_thermal_diagnostics.run_validated_td_b_r6_runtime_contract","measure_p7_thermal_diagnostics.run_authorized_plan"],"handwritten_controller_allowed":false,"python_c_or_heredoc_launch_allowed":false,"monkeypatch_allowed":false,"environment_semantic_owner_allowed":false,"accepted_g4_05_code_checkpoint":"d813cba24f49ca8ae8b54004f7ec20592ee979ab","accepted_g4_05_code_tree":"e5a940cb068ab1aec0d462edf8ea9f3b907eb1fe","accepted_g4_05_package_access":0,"synthetic_package_fixtures_only":true,"targeted_required":true,"focused_required":true,"compile_static_required":true,"codegraph_sync_required":true,"fresh_full_suite_runs":1,"phase1_status":"READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD","phase2_reuses_same_plan":true,"phase2_full_rerun":false,"formal_root_access":0,"formal_root_create":0,"device_access":0,"network_access":0,"camera_connect_calls":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"retained_r3_access":0,"old_frame_access":0,"old_release_access":0,"old_corrective_access":0,"old_external_controller_access":0,"firmware_access":0,"deployment_access":0,"td_c_access":0,"g4_06_formal_execution_authorized":false,"g4_07_execution_authorized":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_06_PACKAGE_A_TWO_PHASE_REVIEW","future_package":"G4_06_PACKAGE_B_FORMAL_ACQUISITION_NOT_AUTHORIZED"}`

## 0. Package purpose 与 activation

当前production owner函数已存在，但`tmp/run-p7-thermal-diagnostics.zsh`所调用的CLI没有把accepted stage-gate package、live C/L attestation、future activation与runtime materializer路由到existing narrow hook。Package A只修复这个工程调用seam并建立immutable code checkpoint；它不访问accepted G4-05 root，不创建formal或evidence root，不连接设备，也不授权Package B。

本PLAN只有Orchestrator完成以下exact activation后才可执行：

1. parent=`ca0a4673bba0b0c646294f2199bfacdb55374702`，tree=`5ca9644d3745b9eac033740a51b43161876ede98`，branch=`main`；
2. subject exact=`docs(plan): activate ray r6 production launch seam`；changed paths exact且仅为FULL与PLAN；
3. activation前除待提交的FULL/PLAN外，dirty必须且只能为`.agent-work/EXECUTION_RESULT.md`，SHA-256
   `fb4c677af69df9ed9bfa70173ea285560159172baa904c475d76ebe18f07e6e4`；
4. activation后PLAN/FULL strict parser active `1/1`，task/contract/canonical next exact同一`REF-G4-06-RAY-R6`；
5. GUIDE SHA仍为`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；GUIDE/RESEARCH、wrapper、thermal scientific owner、accepted prerequisites与authority locks不变。

任一 mismatch：不编辑代码、不创建synthetic fixture，只写ER后回唯一Planner stop。

## 1. Maintainability preflight 与 owner boundary

`measure_p7_thermal_diagnostics.py`是巨型coordinator。Executer在编辑前必须先用CodeGraph确认：CLI parse/main → new narrow dispatch → existing
`run_validated_td_b_r6_runtime_contract()` → existing `run_authorized_plan()`的调用路径与blast radius，并把preflight结论写ER。

冻结的ownership：

- package inventory/load、artifact identity、terminal seal、PLAN/FULL active contract、C/L source attestation、future activation构造/验证、expected runtime SHA与materialization归existing focused
  `p7_td_b_r6_stage_gate.py`；
- `measure_p7_thermal_diagnostics.py`只允许增加最窄CLI参数解析与单一dispatch；不得复制package验证、Git traversal、serialization、runtime-plan构造、device/capture或cleanup语义；
- existing `run_validated_td_b_r6_runtime_contract()`及`run_authorized_plan()`仍分别是唯一narrow validation/delegate owner和唯一真实runner；
- wrapper已有generic pass-through args与shell cleanup trap，Package A不得修改；
- 不新增module、test module、controller、service、schema family或parallel semantic owner。

若direct measure修改需要把package/attestation/materialization状态塞入main，必须把该逻辑收敛到existing focused stage-gate owner，只保留measure的一次调用与kwargs转发；若仍无法避免扩大god object，停止并向Orchestrator请求最小enabling refactor，不得借本包做无关重构。

## 2. Exact implementation scope

允许修改且只能修改：

1. `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
2. `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
3. `tests/test_p7_td_b_r6_stage_gate.py`
4. `.agent-work/EXECUTION_RESULT.md`

Stage-gate owner必须提供单一production seam，完成：

- 从显式package directory读取exact inventory，仅接受`stage-gate.json`、`launch-descriptor.json`、`terminal-seal.json`；root必须regular directory、非symlink，artifact必须regular、非symlink、mode0600；
- fail closed验证artifact bytes/SHA、terminal seal对前两artifact的引用、stage gate与descriptor closed schema/semantic contract；不得接受extra/missing/stale/historical/secret artifact；
- 读取live PLAN/FULL machine rows，要求active count `1/1`、active task `REF-G4-06-RAY-R6`、active contract
  `G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V1`，且FULL canonical next相同；
- 以descriptor冻结的verified parent/code-owner合同和live HEAD/tree做repo-owned read-only per-commit attestation；C必须是live ancestor，C之后逐adjacent commit必须linear direct child且只含`.agent-work/`路径；
- 构造closed future activation，exact绑定descriptor SHA、template SHA、C/tree、L/tree、canonical attestation、explicit output parent/run name、launch1/retry0；
- 先计算expected runtime SHA，再用existing `materialize_runtime_plan()`得到唯一runtime；不得从CLI拼写或转录runtime JSON；
- 把runtime、stage gate、descriptor、activation、repo root、output dir、run name与camera backend exact一次交给existing narrow hook；hook再exact一次委派existing runner。

Measure CLI必须只接收显式、无secret的package path与现有formal args，要求exact Ray/TD-B/formal/remote-v2/execute/device-control shape；invalid/missing/extra组合必须在backend factory、connect、output root creation、Ray/strip/capture前拒绝。Legacy CLI所有既有分支与参数语义不变。

本包只实现并测试seam；不得调用production seam访问真实package或运行真实delegate。

## 3. Synthetic-only test contract

只允许test-owned synthetic temp package/Git fixtures；不得读取
`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-70fec61ef830-20260804T012240Z`或任何accepted/rejected/retained/formal/external root。Fixture不得包含真实device地址、camera credential、secret或historical payload。

Meaningful tests至少覆盖：

1. exact three-artifact inventory、root/artifact symlink、mode、bytes、SHA、terminal references；extra/missing/stale均fail closed；
2. descriptor、template与package artifact交叉引用一致；篡改引用优先报integrity drift；内部引用一致的secret/historical fixture命中各自semantic guard；
3. live PLAN/FULL active `1/1`、task/contract/canonical next exact；active0、task/contract不一致、duplicate/malformed machine row均pre-connect FAIL；
4. C/L：C==L、合法多级`.agent-work/`-only linear descendant PASS；wrong parent/tree/HEAD、non-ancestor、merge/nonlinear、mixed/non-agent-work adjacent path、dirty source/test FAIL；
5. future activation所有closed keys、descriptor/template/C/L/attestation/root/launch/retry绑定；missing/extra/伪造ledger与expected runtime SHA drift FAIL；
6. pure materializer只生成existing canonical 16-Ray runtime shape，A/D/B/C shutter、logical/physical16、setup0/ambient0、strip zero、launch1/retry0与hard locks不漂移；不执行device；
7. CLI valid synthetic path用fake backend与injected delegate证明package owner → materializer → narrow hook → delegate kwargs exact且each once；不得调用真实network/device；
8. 所有invalid package/source/machine/activation/runtime/CLI case均backend factory/connect=`0`、delegate=`0`、output/formal root create=`0`；
9. delegate exception不触发CLI retry、repair、alternate root或第二次调用；
10. legacy dry-run、setup、EQ-R6与setup-release CLI branch的关键保护测试保持不变；wrapper args pass-through与`zsh -n`继续PASS。

测试不得通过monkeypatch production semantic owner、handwritten controller、`python -c`、here-doc或环境变量注入来伪造生产路径。依赖注入只用于fake backend/delegate observation，不能跳过package/attestation/materializer/narrow-hook owner链。

## 4. Validation sequence 与 immutable checkpoint

Executer按顺序执行：

1. intake与CodeGraph maintainability preflight；
2. 添加/先跑focused regression，证明当前CLI seam缺失且pre-connect fail closed；
3. 最小实现focused owner与measure narrow dispatch；
4. targeted stage-gate/CLI tests；
5. relevant focused thermal/CLI/integration tests；
6. `compileall`、wrapper `zsh -n`与适用static checks；
7. `codegraph sync`，再query package load → PLAN/FULL contract → C/L attestation → activation/materializer → narrow hook → runner exactly once；
8. `git diff --check`；dirty exact只能为ER与三项candidate code/test；
9. final candidate只运行一次fresh `.venv/bin/python -m unittest discover -s tests`；不得继承G4-05的942/942，也不得在final full之后修补semantic code再复用结果。

Phase1 Planner只可在全部PASS后返回`READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`。Orchestrator随后创建一个controlled code child：

- parent exact为Package A activation child；
- subject exact=`feat(stage-gate): route ray r6 formal launch owner`；
- changed paths exact为measure、stage-gate、focused tests三项，不含ER；
- 不push、不创建PR。

同一PLAN进入phase2 read-only review：验证child direct-parent/subject/path set/tree、Git blobs与current bytes、ER-only dirty、source identities、CodeGraph与phase1 test evidence；code bytes未变时继承唯一fresh full，不重复full。只有phase2接受后才归档PLAN/ER并把Package A标为terminal accepted。Package B仍须由Orchestrator更新FULL后另行委派Planner，不能从本PLAN直接执行。

## 5. Hard locks 与 failure convergence

Package A全部计数必须保持：accepted G4-05 root access=0；formal root access/create=0；device/network/backend connect/camera/Ray/strip/capture/nonzero light=0；release/retained R3/old frame/old release/old corrective/external controller access=0；firmware/deployment/TD-C=0。

这是同一`REF-G4-06-RAY-R6`的Package A，不创建suffix/new task/new experiment root。第一次具体工程失败允许在final-candidate声明前一次bounded correction；同一owner/seam第二次失败必须重新评估ownership，只允许上述最小focused extraction与保护测试；同一具体边界第三次失败停止回Orchestrator。不得第四次retry或用新task/root掩盖状态不变。

以下立即停止，不做第二次修补：需要修改GUIDE/RESEARCH、thermal scientific contract、wrapper、超过三项candidate code/test、创建新module/controller、弱化source attestation或pre-connect failure、让generic CLI绕过narrow hook、或需要真实package/device/formal root才能证明正确性。

本包没有Human/Advisor gate：它是纯工程architecture/provenance/test工作。Firmware/deploy/destructive hardware与bounds expansion仍需Human，但本包全部为0。

## 6. Executer handoff 与唯一 Planner stop

Executer只写`.agent-work/EXECUTION_RESULT.md`，不得修改/归档PLAN、FULL、debug、archives、GUIDE/RESEARCH或wrapper，不得commit/push/PR。ER必须记录：intake；maintainability结论；exact source/test diff；synthetic fixture边界；targeted/focused/full commands、counts与freshness；compile/static/CodeGraph/diff结果；all access/call/root counters；candidate identities；以及phase1 disposition request。

唯一stop：`RETURN_FOR_G4_06_PACKAGE_A_TWO_PHASE_REVIEW`。

Package A acceptance只证明production CLI seam与immutable code checkpoint可供未来Package B规划；不表示hardware ready、formal launch/pass、quality/history pass、G4-07 unlocked、release consumed或任何设备授权。
