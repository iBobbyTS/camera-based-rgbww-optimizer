# REF-G4-05-RAY-R6-STAGE-GATE：real delegate owner convergence

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_REAL_DELEGATE_CONVERGENCE`

**Executable after activation：** `true`

**Active task count after activation：** `1`

**Active task after activation：** `REF-G4-05-RAY-R6-STAGE-GATE`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_05_REAL_DELEGATE_CONVERGENCE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-RAY-R6-STAGE-GATE-OFFLINE-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_REAL_DELEGATE_CONVERGENCE","executable":true,"active_task_count":1,"active_task":"REF-G4-05-RAY-R6-STAGE-GATE","reference_task_id":"REF-G4-05-RAY-R6-STAGE-GATE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_REAL_DELEGATE_CONVERGENCE","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"724083157ae7fb17f68cdf915d32233e3a6d5740","expected_parent_tree":"5fca945fca7cba625d7844a0891910d8ec599dee","expected_subject":"docs(plan): activate ray r6 delegate convergence","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"activation_dirty_contract":{"clean_required":false,"exact_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"exact_initial_sha256":{".agent-work/EXECUTION_RESULT.md":"5958c1a627bbe5a201b72c3710be6fcb1888835b881d65270f0f898428c94d28","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py":"705b3523e3706df814f8d339b0cdb248fc90919458c5da0696bc3a800470effd","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py":"d5091c0b7c1141e033fadd58b065b13fde2bd69f7e93fd0bd087cb6f7395e885","tests/test_p7_td_b_r6_stage_gate.py":"dce9ec5b9535152ef6281d36995b4b23d0b718046a37faca5d409d1cc2941ed7"},"disposition":"CLASSIFIED_REJECTED_G4_05_CANDIDATE_RETAINED_IN_PLACE_FOR_OWNER_CONVERGENCE","other_dirty_allowed":false},"execution_authorized_before_activation":false,"single_current_action":"converge_non_authorizing_plan_schema_v2_template_materialization_and_real_delegate","allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"existing_dirty_candidate_paths":4,"new_modules":0,"new_test_modules":0,"giant_module_changes":"EXACT_RUNTIME_AUTHORITY_VALIDATION_AND_NARROW_KWARGS_DELEGATION_ONLY","sealed_runtime_template_authority_false":true,"authorized_runtime_plan_persisted":false,"post_capture_ledger_validator_calls":0,"controller_files":0,"corrective_suffixes":0,"new_task_ids":0,"branch":"main","execution_cwd":"/Users/ibobby/Projects/WLED-RGBWW","old_rejected_root":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a1db65d01cba-20260803T233631Z","old_rejected_root_access":0,"new_stage_gate_root":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-724083157ae7-20260804T000832Z","new_stage_gate_root_must_be_absent":true,"new_stage_gate_root_create_cap":1,"persist_cap":1,"internal_replay_cap":1,"public_replay_cap":1,"alternate_root":0,"retry":0,"repair_root":0,"artifact_names":["launch-descriptor.json","stage-gate.json","terminal-seal.json"],"root_mode":448,"artifact_mode":384,"formal_capture_budget":0,"release_root_access":0,"predevice_root_access":0,"readiness_root_access":0,"e2_root_access":0,"retained_r3_access":0,"legacy_or_deep_corrective_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_connect_calls":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"g4_05_accepted_before_planner_review":false,"g4_06_planning_unlocked_before_planner_review_and_focused_commit":false,"g4_06_execution_authorized":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_05_REAL_DELEGATE_CONVERGENCE_REVIEW","future_reference_task":"REF-G4-06-RAY-R6","future_reference_status":"LOCKED_UNTIL_G4_05_TERMINAL_ACCEPTANCE_AND_ORCHESTRATOR_FOCUSED_COMMIT"}`

## 0. Same-task convergence and no-new-archive rule

本PLAN是同一task、同一contract的唯一bounded owner-convergence package：

- task保持`REF-G4-05-RAY-R6-STAGE-GATE`；contract保持`G4-RAY-R6-STAGE-GATE-OFFLINE-V1`；
- 不创建corrective suffix、新reference task、新controller或新PLAN family；
- 上一reviewed PLAN/ER已分别归档为`.agent-work/archived/PLAN-20260803-1802.md`与
  `.agent-work/archived/EXECUTION_RESULT-20260803-1802.md`，terminal checkpoint已由Git `7240831...`冻结；本次Planner改写不得重复archive；
- 旧candidate的durable package/provenance/source guards/authority-false属于accepted subordinate evidence，但real delegate seam disposition仍是
  `REJECTED_G4_05_REAL_DELEGATE_SHAPE_INCOMPATIBLE`；不得把旧package改写成accepted。

本PLAN不执行。只有Orchestrator完成第1节exact activation后，Executer才可在本task内原地收敛现有candidate。

## 1. Activation topology and classified dirty worktree

Activation必须同时满足：

1. parent exact `724083157ae7fb17f68cdf915d32233e3a6d5740` / tree
   `5fca945fca7cba625d7844a0891910d8ec599dee` / branch `main`；
2. subject exact `docs(plan): activate ray r6 delegate convergence`；commit changed paths exact且仅为
   `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`；
3. child是parent direct child；PLAN/FULL repo-owned parser均active `1/1`，task/contract/canonical next exact同一G4-05；
4. activation前后worktree不要求clean，但必须且只能保留下列四项classified dirty candidate，并在activation完成、Executer首次编辑前保持exact SHA：

   - `.agent-work/EXECUTION_RESULT.md` /
     `5958c1a627bbe5a201b72c3710be6fcb1888835b881d65270f0f898428c94d28`；
   - `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py` /
     `705b3523e3706df814f8d339b0cdb248fc90919458c5da0696bc3a800470effd`；
   - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` /
     `d5091c0b7c1141e033fadd58b065b13fde2bd69f7e93fd0bd087cb6f7395e885`；
   - `tests/test_p7_td_b_r6_stage_gate.py` /
     `dce9ec5b9535152ef6281d36995b4b23d0b718046a37faca5d409d1cc2941ed7`。

5. GUIDE SHA仍为`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；canonical thermal owner与wrapper
   未变；retained R3仍`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption/formal/TD-C/G4-06 authority仍false。

任一项不满足：不得修改candidate、不得检查或创建new root，只更新ER后stop。禁止reset/clean/checkout/revert这四项；它们只能在allowed scope内原地修订。

## 2. Frozen scientific/runtime contract

### 2.1 Canonical scientific owner remains unchanged

Focused owner在G4-05 preflight必须继续调用而非复制：

- `thermal.build_td_b_r6_formal_plan()`；
- `thermal.validate_td_b_r6_formal_plan()`。

`thermal.validate_td_b_r6_capture_ledger()`是post-capture result owner，本task没有capture ledger，调用计数必须为0。Stage gate只能把它按callable identity和
required post-capture role冻结为未来G4-06/G4-07 canonical owner；tests验证planned 16 captures可导向其expected IDs/required result fields，但不得构造synthetic
capture results调用它来制造formal evidence。

Canonical GUIDE experiment仍是`P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`；Ray-only、strip zero throughout、ambient0、fixed exposure、
old/new pooling prohibited、launch1、retry0。Exact shutters：A `1/5000`、D `1/6400`、B `1/8000`、C `1/2500`。Exact states/commands：

- A：H120 / S100 / intensity100；
- D：H120 / S50 / intensity100；
- B：H0 / S0 / intensity100；
- C：H300 / S100 / intensity100。

Exact 16 capture IDs/order保持canonical owner输出：A0@600；D@60/120/300/600；A-after-D@600；B@60/120/300/600；A-after-B@600；
C@60/120/300/600；A-after-C@600。600秒仍是selected transient，不是steady/settled/TD-A pass/`t_formal`。

### 2.2 One non-authorizing PLAN_SCHEMA_V2 template/adapter owner

`p7_td_b_r6_stage_gate.py`必须在同一focused owner中产生并严格验证一个
`thermal.PLAN_SCHEMA_V2` shape的Ray R6 **runtime-plan template**。Template封存于durable package，status必须是waiting G4-06，authority与全部
execution/device/formal flags必须false；它永远不能被existing authorized execution validator直接接受。允许从repo-owned trusted base/resolved plan经一个
单一adapter构造；禁止读取G4-01/02/03/04、retained R3、legacy release或任何external payload。Tests必须用内部引用一致的synthetic trusted base，不得拿
历史artifact当fixture。

Runtime-plan template必须满足existing runner所需的结构shape及canonical R6 cross-check，但保持non-authorizing：

- top-level schema exact`thermal.PLAN_SCHEMA_V2`，timing contract、native RAW ambient policy、camera remote-v2 capability、frozen shutters、budgets、
  captures、stage均完整；template status exact waiting、execution authority false；不得把high-level scientific mapping冒充template，也不得把template伪装成
  authorized runtime plan；
- runner-facing`experiment_id`若为existing owner要求的`thermal.TD_B`，必须另以immutable `guide_experiment_id`/R6 contract reference绑定GUIDE exact ID；
  validator必须拒绝缺失、交换或把legacy TD-B plan伪装成R6的情况；
- captures exact 16，无ambient/setup；每步`capture_id`、sequence index、state、source ray、command、requested dwell、formal role/measurement、fixed shutter cache、
  observed-elapsed timing acceptance及isolation gates与canonical R6 exact一致；
- logical/physical budget均16，setup0、ambient0、launch1、retry0；不得允许17th return、second root、reacquire、auto exposure、mid-run shutter change或strip nonzero；
- template必须保留existing production owner需要的physical-return/sidecar/MakerNote/58-feature/clip/noise/finite/valid-pixel/timing/chronology/history/
  cleanup contracts；adapter不得复制capture loop、serializer、provenance ledger、device command或cleanup owner；
- focused `validate_runtime_plan_template`只调用canonical R6 plan validator和focused shape/authority-false cross-check；不调用post-capture ledger validator，也不要求
  template通过existing authorized validator。

Focused owner另提供pure `materialize_runtime_plan(template, future_activation)`：只在reference-consistent synthetic future G4-06 activation下，把同一template
一次性投影成authorized runtime plan。Activation必须绑定descriptor SHA、template SHA、expected materialized runtime SHA及source/root/budget bounds；materializer
先按不包含`expected_runtime_sha256`自引用字段的canonical runtime projection构造plan，再比较activation中的expected hash。Runtime plan自身不得包含自身hash，避免
self-reference。Materialized plan不持久化、不写stage-gate root。只有materialized plan才调用focused runtime validator与existing
`validate_authorized_execution_plan(runtime_plan, camera_backend=...)`。

Trusted base只提供existing owner通用字段；R6-specific IDs/states/dwell/commands/shutters/budgets只能由canonical R6 projection产生并cross-check。禁止第二个
parallel adapter、handwritten external controller或在G4-06临时补齐shape。

## 3. Exact PLAN-bound authority seam without weakening legacy

当前AGENTS已明确future bounded light/camera operation不需obsolete重复Human token。`measure_p7_thermal_diagnostics.py`只允许最小authority/validation seam：

1. 既有legacy plans继续走原`human_authorization_verified`验证，现有测试与拒绝行为不得削弱；
2. 仅由focused materializer从sealed template + exact future activation产生的R6 runtime plan可改走新的PLAN-bound authority schema；runtime plan内的authority
   projection必须绑定future task `REF-G4-06-RAY-R6`、active count1、descriptor SHA、template SHA、committed source HEAD/tree、launch cap1、retry0、formal root
   parent/basename constraint与`allow_device_control=true`；expected materialized runtime-plan SHA只由future activation绑定并由focused validator比较，不写回runtime
   plan自身；
3. authority mapping本身不能从stage-gate package推断；G4-05 package仍non-authorizing，G4-06必须另有active PLAN；
4. 缺字段、extra字段、bool/int混淆、descriptor/runtime hash drift、task/source/root/budget/bounds drift全部在camera backend connect或delegate前拒绝；
5. 不添加`human_authorization_verified=true`占位，不允许release、FULL或historical fixture替代future PLAN authority。

Narrow hook必须改为真实signature seam，至少显式接收：

- 已由focused materializer产生并验证的authorized `runtime_plan`；
- `output_dir`；
- `run_name`；
- `camera_backend`；
- stage gate、launch descriptor与future PLAN activation；
- injectable delegate（默认/声明owner必须是existing`run_authorized_plan`）。

调用顺序必须为：stage gate/template validation → descriptor/reference/semantic validation → future activation与descriptor/template/runtime hash validation → focused runtime
R6 validation → existing
`validate_authorized_execution_plan(runtime_plan, camera_backend=fake_or_real)` → delegate exactly once，且exact调用为：

`run_authorized_plan(runtime_plan, output_dir=output_dir, run_name=run_name, camera_backend=camera_backend)`。

不得丢弃或改名三个kwargs，不得把runtime plan降成`scientific_contract`，不得在hook中connect、创建root、import/call device owners或复制runner body。

## 4. Mandatory compatibility and failure probes

`tests/test_p7_td_b_r6_stage_gate.py`必须在原meaningful guards上补足真实owner compatibility。Fake callback once不再足够；至少证明：

1. `inspect.signature(run_authorized_plan)`存在plan positional及keyword-only `output_dir`、`run_name`、`camera_backend`；hook对真实delegate的调用shape exact；
2. Sealed template schema/shape/R6 semantics exact且authority false；existing authorized validator必须在connect前拒绝template，证明package不能自授权；
3. 对reference-consistent synthetic trusted base + future activation调用`materialize_runtime_plan`所得的authorized runtime plan，
   `validate_authorized_execution_plan(runtime_plan, camera_backend=fake_capable_backend)` PASS；fake backend只提供backend name、remote-v2 capability及required
   callable attributes，`connect`调用计数必须0；
4. patch真实`measure.run_authorized_plan` owner后调用narrow hook，断言materialized plan identity/semantic equality及三个kwargs exact once；不得只传
   `lambda(contract)`；
5. invalid/missing/extra future activation、descriptor/template/runtime hash、runtime schema、canonical IDs/order/state/dwell/command/shutter、budget15/17、
   ambient/setup、retry1、strip nonzero、
   bounds/root/hash/source drift均在delegate callback前0 calls；
6. legacy authorized-plan tests继续通过，证明新R6 branch没有扩大ordinary TD-A/TD-B/TD-C或旧release path；
7. descriptor reference drift仍优先于secret/historical semantic guard；secret/historical测试继续使用reference-consistent fixture；
8. template canonical JSON round-trip后仍通过focused template validator；synthetic materialized plan通过focused runtime与existing validators；tuple/list投影只能由
   repo-owned `json_native_value`处理；
9. mock `thermal.validate_td_b_r6_capture_ledger`并断言G4-05 build/evaluate/persist/replay/materialize全程0 calls，同时planned capture contract与canonical expected
   IDs/required post-capture fields exact；
10. no-device assertion覆盖camera connect、Ray/strip/control imports/calls、capture、formal root creation全部0。

测试可以import existing owner并mock它，但不得执行runner body、connect backend、创建formal root或访问network/device。

## 5. Rejected old root and one new durable candidate

旧root：

`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a1db65d01cba-20260803T233631Z`

保持immutable historical rejected；本PLAN对它read/list/replay/write/delete/move/access计数全部0。新root不是对旧rootretry，而是owner reassessment后新的same-task
candidate：

`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-724083157ae7-20260804T000832Z`

只有所有pre-package code/test/compatibility checks通过后，才对new exact path执行一次lexical absence gate；不得scan/list parent或换root。随后：

- root create exact1、mode0700；persist exact1；internal replay exact1；public replay exact1；retry/repair/alternate0；
- inventory exact仍为`launch-descriptor.json`、`stage-gate.json`、`terminal-seal.json`，files mode0600、canonical exclusive no-follow persistence；
- stage gate必须新增并绑定non-authorizing runtime-plan template及其canonical SHA；descriptor必须绑定template SHA并声明real owner和exact kwargs launch shape；
  terminal引用前两artifact且不self-reference；
- package authority仍全部false，status仍waiting Planner review；不得写future PLAN authority为true，不得创建formal root；
- persistence/internal/public replay只执行canonical plan validator、focused template/descriptor validators及authority-false检查；不得materialize authorized plan，不得调用
  existing authorized validator或post-capture ledger validator。Real-owner compatibility只在pre/post-package synthetic activation probes中证明；
- 任一persist/replay/identity失败保留new root及failure seal，立即stop；不得重试、修补root、读取旧root或另建root。

## 6. Continuous execution and validation order

本PLAN是一个最大安全连续工程包；implementation、tests、compatibility probes、evidence formatting和state text不得拆成新task/PLAN。

1. 验证activation topology及四项classified dirty initial SHA；记录old root access0，不检查其存在；
2. CodeGraph preflight现有candidate及`build_diagnostic_plan`/template/materializer/runtime validators/runner call path；实现单一template adapter、exact authority
   materialization branch与真实kwargs hook；
3. targeted：`.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate`；
4. real-owner offline probes：sealed template authority-false且existing validator reject/connect0；synthetic materialization后existing validator + fake capable backend
   PASS/connect0；patched real delegate materialized plan+kwargs exact once；invalid branches callback0；post-capture ledger validator calls0；
5. focused：
   `.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_p7_successor_e2`；
6. compile/static：`.venv/bin/python -m compileall -q src tests`、`zsh -n tmp/run-p7-thermal-diagnostics.zsh`；扫描diff不得出现parallel runner/serializer/
   capture loop/controller、obsolete Human token on new branch、secret/historical payload或旧task suffix；
7. 只有3–6全PASS，才按第5节创建new root并完成persist/internal/public replay；
8. package/source alignment后重跑targeted、real-owner probes与focused；只有final candidate运行一次
   `.venv/bin/python -m unittest discover -s tests`；不得继承上一candidate的931/931作为本candidate full result；
9. `codegraph sync`后query focused template adapter/materializer → thermal canonical plan validator → measure existing validator → narrow hook → existing runner，证明
   一个adapter/materializer owner、一个runner、无post-capture validator误用、无device/serializer duplication；
10. `git diff --check`；changed paths必须exact为四项classified candidate；PLAN/FULL/archives/GUIDE/RESEARCH/config/wrapper/thermal owner均不变；
11. repo-owned PLAN/FULL parser保持active `1/1`同task/contract/canonical next；ER记录所有identity/count/result后返回唯一Planner stop。

实现期可以按tests红绿完成同一设计，但一旦Executer宣布real-owner final compatibility candidate并运行第4节probe，任何production validator/signature/kwargs/
runtime-shape失败都立即terminal return，不允许第二adapter、第二authority schema、第二root或同边界retry。纯assertion输出格式错误也不得扩大semantic owner；需要
Planner判断时直接stop。禁止生成suffix/new task。

## 7. EXECUTION_RESULT handoff contract

Executer必须把live ER更新为本convergence handoff，并记录：

- activation child/parent/tree/subject/two-path topology；四项initial classified dirty SHA与final changed paths；
- template adapter/materializer owner/API、trusted base来源与no-external-payload证明；sealed template schema/bytes/SHA/authority-false及canonical JSON round-trip；
- cross-check matrix：16 IDs/order、state/dwell/commands/shutters、budget16/setup0/ambient0/launch1/retry0、Ray-only/strip-zero、quality/history/cleanup；
- post-capture owner identity/required future role及G4-05 capture-ledger validator calls0；
- synthetic materialized runtime plan SHA；new PLAN-bound authority exact descriptor/template/runtime hashes/source/root/bounds；legacy validation unchanged的tests；
- `inspect.signature`结果；fake-capable-backend attributes与connect count0；template existing-validator reject、materialized runtime existing-validator PASS；patched
  real delegate exact materialized plan与
  output_dir/run_name/camera_backend kwargs once；invalid probes callback0；
- targeted/focused/final-full/compile/static/CodeGraph/diff/machine命令、exit与exact test counts；
- old root access0；new root absence1/create1/persist1/internal replay1/public replay1及root/artifact device/inode/mode/bytes/SHA/inventory/terminal；
- retry/repair/alternate/formal root/device/network/camera connect/Ray/strip/capture/release consumption/TD-C均0；
- 结果只能称`G4_05_REAL_DELEGATE_CONVERGENCE_ACCEPTANCE_CANDIDATE`，等待Planner closed review；不得自称G4-05 accepted或G4-06 unlocked；
- Planner若接受，Orchestrator才可对code/test创建focused commit，并以其exact commit/tree作为未来G4-06 planning prerequisite。Executer不commit。

## 8. Safety and exact stop

- GUIDE/RESEARCH/FULL/PLAN/archives/thermal scientific owner/wrapper只读；不得修改或再次归档；
- 全程offline；device/network/app/process/listener/camera connect/Ray/strip/capture/nonzero light/release/formal/formal root/TD-C/firmware/deployment为0；
- 不访问任何external payload或旧root；只允许按第5节创建一个new offline stage-gate root；
- 不stage/commit/push/PR，不reset/clean/revert classified dirty candidate，不生成G4-06 PLAN；
- 本PLAN不授权G4-06、formal execution、设备或release consumption。

唯一stop为`RETURN_FOR_G4_05_REAL_DELEGATE_CONVERGENCE_REVIEW`。无论PASS/FAIL，Executer必须在此返回Planner；G4-06 planning/execution继续locked，
不得从stage-gate package、FULL或tests推断后续authority。
