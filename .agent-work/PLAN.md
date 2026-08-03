# REF-G4-01-SUCCESSOR-LINEAGE：建立 Guide 4 successor composition owner

**计划状态：** `EXECUTABLE_BOUNDED_PURE_OFFLINE_ENABLING_INTEGRATION`

**Executable：** `true`

**Active task count：** `1`

**Active task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Planner 日期：** `2026-08-02`

**适用 GUIDE：** `advisor/4/4.GUIDE.md`；SHA-256
`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-SUCCESSOR-LINEAGE-ENABLING-INTEGRATION-V1","plan_status":"EXECUTABLE_BOUNDED_PURE_OFFLINE_ENABLING_INTEGRATION","executable":true,"active_task_count":1,"active_task":"REF-G4-01-SUCCESSOR-LINEAGE","reference_task_id":"REF-G4-01-SUCCESSOR-LINEAGE","reference_goal":"REF-G4-COMPLETE","package_kind":"bounded_pure_offline_repo_owned_composition_seam_and_tests","verified_source_parent":"b91066015613c996187665d8ea9b7841ac321b84","verified_source_parent_tree":"4b1083e71d321e85daa64e47fe1dcd82eef79aef","activation_child_sha_recorded_in_plan":false,"activation_child_subject":"docs(plan): activate g4 successor lineage integration","activation_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260802-2246.md"],"rotated_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260802-2246.md","bytes":1619225,"sha256":"dea5bb1d4f183aee806d7bb8b83153d486190f19e64eb8cf59c8bdb3f7d6e5e4","source_body_bytes":1618285,"source_body_sha256":"803a023422bf20c096c218498e44f7196d6bc99aa8504ff4e8110592b9448abd","immutable_after_activation":true},"activation_protected_paths":["src","tests","config","advisor",".agent-work/FULL_PLAN_REFERENCE.md"],"guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","single_current_action":"implement_one_repo_owned_guide4_successor_lineage_composition_owner_and_behavior_tests_then_stop_for_planner_review_and_orchestrator_checkpoint","allowed_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py","tests/test_p7_successor_lineage.py",".agent-work/EXECUTION_RESULT.md"],"production_source_edits":1,"test_file_edits":1,"config_edits":0,"guide_edits":0,"research_edits":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"release_root_acquisition":0,"release_generation":0,"public_validator_invocations":0,"final_validator_invocations":0,"strict_validator_invocations":0,"release_consumption":0,"retained_r3_access":0,"legacy_release_access":0,"old_controller_access":0,"external_experiment_payload_access":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"commit_by_executer":0,"amend":0,"push":0,"ordinary_bounded_correction_cap":1,"corrective_task_id_creation":0,"planner_stop":"RETURN_FOR_ENABLING_INTEGRATION_REVIEW_AND_ORCHESTRATOR_CHECKPOINT","future_release_family":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage","future_release_exact_root":"MUST_BE_FROZEN_BY_THE_POST_CHECKPOINT_PLAN_NOT_THIS_PACKAGE","future_reference_task":"REF-G4-01-SUCCESSOR-LINEAGE","future_stage_locked":true}`

## 1. 当前唯一动作与停止点

本包只建立一个可维护的 repository-owned Guide 4 successor-lineage composition seam，及其行为保护测试。
Executer 完成实现与验证后，只写当前 `.agent-work/EXECUTION_RESULT.md` 并停回 Planner。Planner 验收后，
Orchestrator 才能建立包含本 owner 的 exact Git checkpoint；随后仍由同一个
`REF-G4-01-SUCCESSOR-LINEAGE` 的新 Planner pass 冻结 exact checkpoint/tree 与 exact fresh root，首次生成并验证
release。

本包不得取得 release root，不得生成 release，不得调用 public/final/strict validator，不得把未提交代码绑定为
lineage source，也不得新建 corrective task ID。后续 predevice/device/formal stage 全部 hard locked。

**唯一 Planner stop：**
`RETURN_FOR_ENABLING_INTEGRATION_REVIEW_AND_ORCHESTRATOR_CHECKPOINT`。

## 2. Frozen intake

### 2.1 非自引用 activation topology

```text
verified source parent = b91066015613c996187665d8ea9b7841ac321b84
verified source parent parent = 4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd
verified source parent tree = 4b1083e71d321e85daa64e47fe1dcd82eef79aef
verified source parent subject = docs(orchestration): activate guide 4 completion goal
branch = main

allowed direct child subject = docs(plan): activate g4 successor lineage integration
allowed direct child exact changed paths =
  .agent-work/EXECUTION_RESULT.md
  .agent-work/PLAN.md
  .agent-work/archived/EXECUTION_RESULT-20260802-2246.md

rotated archive = .agent-work/archived/EXECUTION_RESULT-20260802-2246.md
archive bytes = 1619225
archive SHA-256 = dea5bb1d4f183aee806d7bb8b83153d486190f19e64eb8cf59c8bdb3f7d6e5e4
source body bytes = 1618285
source body SHA-256 = 803a023422bf20c096c218498e44f7196d6bc99aa8504ff4e8110592b9448abd
```

本 PLAN 不记录、也不要求预知 future child SHA。Orchestrator必须先以 exact subject/path set建立上述唯一 activation
child；archive从该commit起immutable，不由Executer修改。Executer启动时必须只读证明：current HEAD是verified
source parent的direct child；subject与changed paths exact；worktree clean；PLAN/FULL对本task一致；且
`verified source parent..current HEAD` 对 `src/`、`tests/`、`config/`、`advisor/**/GUIDE.md`、
`advisor/**/RESEARCH.md` 与 `.agent-work/FULL_PLAN_REFERENCE.md` 完全无变化。任一不一致即停，不得reset、clean、
checkout、猜测child SHA或接受更深后继。

### 2.2 Accepted EQ family

以下只作为 immutable accepted scientific/provenance input；本包不得读取或修改 external payload：

```text
acceptance archive =
  .agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
archive bytes = 25296
archive SHA-256 = bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7

accepted EQ family root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
canonical manifest schema = planner_eq_family_manifest_v1
canonical manifest subject = all descendants of that exact root, root excluded
canonical manifest entries/files/directories/symlinks/other = 47/42/5/0/0
canonical manifest payload bytes = 7980
canonical manifest SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
accepted status = qualified_1_2500
```

四个 accepted artifact reference 只冻结 path/hash，不在本包打开：

```text
run/outer-result.json =
  20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
run/candidate-1-outer-terminal.json =
  6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
run/candidate-1/candidate-result.json =
  7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
run/candidate-1/terminal-seal.json =
  8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

### 2.3 Accepted post-EQ checkpoint and policy

```text
acceptance archive =
  .agent-work/PLANS/20260727-2052-p7-post-eq-policy-c1e1-acceptance-review.md
archive bytes = 17030
archive SHA-256 = 6dd605a8d5f142d8fb50cc9a40020e6a816cc116581cccb414459f6c91cc1762

checkpoint = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
parent = f37517af3ae25efb41f085904fd48f037980ed04
tree = 6a69b2c7c1569352047500c44e25b337e4ff82aa
subject = feat(p7): finalize eq-r6 state-c exposure policy
changed paths = exact three paths below
```

| Accepted path | Bytes at checkpoint | SHA-256 at checkpoint |
| --- | ---: | --- |
| `config/hsi/p7-ray-td-b-exposure-policy-v2.json` | 4065 | `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681` |
| `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | 171565 | `87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90` |
| `tests/test_p7_td_b_r6_contract.py` | 102435 | `10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23` |

当前 policy owner 必须保持：

```text
path = config/hsi/p7-ray-td-b-exposure-policy-v2.json
bytes = 4065
SHA-256 = c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
selected C = 1/2500
old_new_frame_combination = prohibited
```

### 2.4 当前 production delegates

下列 owner 在本包中全部只读；新 seam 只组合其 public API，不复制其 policy/plan/serialization 语义：

| Boundary | Current path | Bytes | Current SHA-256 |
| --- | --- | ---: | --- |
| policy、EQ audit、R6 plan builder/validator | `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | 203416 | `14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1` |
| legacy lineage writer，仅用于证明不适用 | `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py` | 188493 | `a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47` |
| downstream analysis consumer，当前不调用 | `src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py` | 97644 | `8e68400d51d01a20f4629aec7ad17c084835d7242e1cfba73a0335916209fa03` |
| filesystem/Git/canonical JSON | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | 21151 | `a27546b1b19aa979d5bfb1731b4bf5dab87a6eed6b5c18ff5b728095d73957c1` |

必须复用 `p7_thermal_diagnostics.load_td_b_exposure_policy_v2()`、
`audit_td_b_eq_r6_qualification()`、`build_td_b_r6_formal_plan()`、
`validate_td_b_r6_formal_plan()` 与 `td_b_r6_machine_status()`；canonical bytes、exclusive-root、exact-file、
read-only Git 与 durable persistence 必须委派给 `p7_retained_r3_provenance_io` 的现有 owner，不得写第二套
JSON projector、Git parser、temporary-replace writer或 filesystem identity模型。

## 3. Maintainability preflight 与 owner 决定

CodeGraph 已确认现有 `write_td_b_setup_lineage_release()` 硬绑定 legacy R2 setup release、旧 F0A Planner
candidate，并重建旧 formal plan；其 validator 同样要求这些 owner。它不能证明 current Guide 4 successor，且使用它会
违反 old release/retained route lock。

因此本包的最小 enabling change 是新增：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
tests/test_p7_successor_lineage.py
```

`measure_p7_thermal_diagnostics.py`、`p7_thermal_diagnostics.py` 与
`analyze_p7_thermal_diagnostics.py` 均不得修改。新模块是唯一 Guide 4 composition owner；它只组合上述 existing
delegates，不成为第二个 scientific-policy、R6-plan、Git、serialization或validator semantic owner。不得复用
retained controller source/template/runtime，不得生成 handwritten external controller。

若实现证明必须修改任一巨型 P7 module、第三个 production module、config、docs、skill或 wrapper，立即停回
Orchestrator；不得自行扩大 changed-path set。

## 4. Enabling integration contract

新模块必须提供以下稳定 public seam；类型名称可以使用 module-local frozen dataclass，但函数名与职责不可漂移：

```text
build_successor_lineage_inputs(...)
compose_successor_lineage_bundle(...)
validate_successor_lineage_release(...)
replay_successor_lineage_bundle(...)
strict_validate_successor_lineage_bundle(...)
```

行为合同：

1. 所有 runtime input 必须显式接收并精确绑定 `source_checkpoint`、`source_tree`、policy path/hash、EQ root及
   canonical EQ manifest bytes/hash；不得从 retained release、旧 candidate、archive摘要或环境变量猜测。
2. `build_successor_lineage_inputs()` 只通过现有 thermal owner验证 accepted policy、EQ qualification、exact R6
   non-executable formal plan与 machine locks；它不得声明 release/device/formal authority。
3. `compose_successor_lineage_bundle()` 只能在 caller 提供的 absent、non-symlink、safe-parent-contained exact root上
   acquisition一次；调用 provenance owner写 canonical artifacts。它不得调用 legacy lineage writer，也不得读取
   legacy R2、retained R3或旧 external-controller root。
4. Future bundle schema必须把 current route与 retained state分开，并至少固定：
   `status=fresh_successor_lineage_validated_unconsumed`、`release_consumable=false`、
   `release_consumption_authorized=false`、`device_authorized=false`、`formal_r6_authorized=false`、
   `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、exact source commit/tree、policy/EQ references、
   R6 exact plan reference及 `old_new_frame_combination=prohibited`。
5. Public validator是 release semantic owner；final replay验证完整 artifact inventory、每个 path/bytes/SHA、
   non-circular terminal references与 source immutability；strict validator拒绝 duplicate key、NaN/Infinity、symlink、
   extra/missing artifact、path escape、secret/authority drift与非canonical bytes。三者不得相互伪造结果或按摘要放行。
6. Future exact success bundle的 artifact name/order必须由 module constant冻结，并至少分离 frozen inputs、R6 formal
   plan、release descriptor、validation summary与terminal seal；terminal最后写且不自引用。失败可形成truthful
   non-success seal，但不得 repair、retry、alternate root或第二 bundle。
7. Public/final/strict call accounting必须可注入并被测试；future generation pass要求三者首次各一次。**本包只实现并
   测试 seam，真实 invocation count必须保持 `0/0/0`。**
8. Module import与unit tests必须 pure offline、无 filesystem mutation at import、无 external root读取、无
   subprocess/device/network side effect。

Future root contract仅冻结 family与生成规则，不授权取得：

```text
safe parent = /Volumes/4T/temp/rgbww-optimizer
family = /Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage
exact child = future Planner在Orchestrator checkpoint后冻结的
              successor-<checkpoint12>-<UTC YYYYMMDDTHHMMSSZ>
this package root acquisition/generation = 0/0
```

## 5. 保护测试

`tests/test_p7_successor_lineage.py` 必须以 hermetic injected fixtures 覆盖实际行为断言：

1. composition只调用现有 policy、EQ audit、R6 plan builder/validator与 provenance owner；不复制 delegate语义；
2. exact accepted policy/EQ/source commit/tree positive fixture可构造 non-authorizing bundle model；
3. policy bytes/hash、EQ manifest bytes/hash、checkpoint/tree任一 drift均 fail closed；dirty/staged source拒绝；
4. legacy setup release、旧 Planner candidate、retained R3 root、旧 deep task ID或旧 controller input一律拒绝；
5. bundle保持 retained R3 unvalidated/unconsumed，所有 eligibility/consumption/device/formal字段为 false；
6. exact R6 `000..015`、A/D/B fixed shutters、C=`1/2500`、16/16、retry0与old/new pooling prohibition来自
   existing thermal owner且不可被 caller覆盖；
7. public validator拒绝字段/hash/path/authority drift；final replay拒绝tamper、missing、extra、duplicate reference与
   terminal self-reference；strict validator拒绝noncanonical JSON、duplicate key、NaN/Infinity、symlink/path escape、
   secret material；
8. root acquisition恰好一次；preexisting/nonempty/symlink root拒绝；失败无repair/retry/alternate root；
9. validator call accounting exact；本测试只用 injected fixture，绝不读取 accepted external EQ payload或生成真实 release；
10. import、negative path与failure seal均保持 device/network/camera/Ray/strip/capture/formal/consumption call count为0。

不得用只检查 symbol存在、只运行代码或 mock掉被测语义的空断言代替上述测试。

## 6. 执行顺序与验证

1. 复核 §2 exact Git/archive/policy/current-owner identity；只读 CodeGraph确认 blast radius仍与本 PLAN一致。
2. 新增唯一 production module与唯一 test module；不编辑其他 source/config/test/docs/skill/wrapper。
3. 运行新测试文件；再运行现有 R6 contract、thermal lineage与 provenance focused tests。
4. 运行受影响测试集合；随后运行 full suite并报告 exact discovered/passed/skipped/failed count。
5. 运行 `python -m compileall`（至少覆盖新增 module及受影响 package）、适用 static/import check、
   `git diff --check`。
6. 在实现完成后运行 `codegraph sync`，再 query新 public seam与delegate call path；证明没有第二套 persistence/
   serialization/Git owner。
7. 生成 repo diff inventory，要求除 Executer-owned `.agent-work/EXECUTION_RESULT.md` 外 changed source set exact为
   §3两个文件；证明 GUIDE/RESEARCH/FULL/PLAN/config、三个巨型 P7 module、legacy archives与external roots未变。
8. Executer只把命令、exit、exact counts、diff inventory、CodeGraph结果、owner/seam结论与 acceptance request写入
   `.agent-work/EXECUTION_RESULT.md`，不得修改 PLAN或FULL，不得 stage/commit/amend/push。

预计本包本身不超过10分钟。若在启动任一授权 validation前根据现有 timing明确预计超过10分钟，Executer必须改用
可见 macOS Terminal启动，完成3次稀疏liveness检查后把session/命令/日志路径交回；不得用Codex background tool长期
占有。其后由Orchestrator决定automation与blocked状态，Executer不得自行持续轮询。

## 7. Failure convergence 与验收

- 首次普通实现/测试缺陷：本 PLAN只允许一次不扩大owner/path/API的 bounded correction。
- 同一边界第二次失败：停止并记录 exact seam/state evidence，回 Orchestrator重新评估；不得继续修、创建新root或
  task suffix。
- 同一边界第三次失败：明确 terminal stop；禁止第四次同类retry。
- accepted policy/EQ scientific provenance矛盾、必须改变 GUIDE contract或无法复用 frozen thermal owners时立即停；
  只有确属科学指导不足/矛盾才请求Advisor。普通module/test/Git问题归Orchestrator。

Planner接受条件：exact两个实现路径、真实保护测试通过、focused/affected/full/compile/static/diff/CodeGraph证据闭合，
没有 release/external/device/formal side effect，且 handoff明确请求：

```text
REF-G4-01-SUCCESSOR-LINEAGE remains unfinished
enabling composition owner = ready for Orchestrator checkpoint
next package = same REF-G4-01, freeze post-checkpoint exact root and generate/validate once
```

通过只允许 Orchestrator 建立 focused checkpoint并委派同一 reference的后续 Planner pass；不解锁任何后续 stage。

维护性判断：本包把缺失的 Guide 4 composition seam隔离为一个小型repo owner，三个巨型P7模块保持只读；policy、
R6 plan与canonical persistence继续由现有单一source of truth负责，测试覆盖authority、drift、replay与failure边界。
