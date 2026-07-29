# REF-P7-23-C0 / EQ-R6 live owner pre-execution correction

**计划状态：** `executable_pure_offline_correction`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C0`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-LIVE-RUNNER-PREEXEC-CORRECTION`

**Package kind：** `bounded_offline_implementation_and_validation`

**Expected parent HEAD：** `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-LIVE-RUNNER-PREEXEC-CORRECTION","reference_task_id":"REF-P7-23-C0","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_offline_implementation_and_validation","expected_parent_head":"98de1a91c264d4b72c4a97fc499ae7d39a67dacc","single_current_action":"implement_and_offline_validate_exact_eq_r6_live_owner","human_eq_r6_confirmation_preserved":true,"device_access":"forbidden","network_access":"forbidden","env_access":"forbidden","camera_access":"forbidden","ray_access":"forbidden","strip_access":"forbidden","light_access":"forbidden","real_all_off_access":"forbidden","real_capture_cap":0,"release_generation_authorized":false,"release_consumption_authorized":false,"eq_r6_launch_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"focused_commit_authorized":true,"planner_stop_required":true}`

**当前唯一动作：** 在不访问任何设备、网络或 `.env` 的前提下，复用现有 thermal plan、remote camera、
physical-return ledger 与 production wrapper lifecycle，补齐 exact EQ-R6 的真实执行 owner，并只用 injected
fake/adversarial adapters 验证其之后能够安全承载 Human 已确认的两档条件流程。

**唯一 Planner 停止点：** 完成代码、离线测试、evidence package与一个 focused commit 后立即停止，写
`.agent-work/EXECUTION_RESULT.md` 交 Planner 验收。不得在本 package 中启动 visible Terminal、创建真实
EQ root、访问设备、运行真实 cleanup、生成release或顺带进入 `REF-P7-23`。

## 1. Planner decision 与 archive

Human 已明确确认：

> 我确认进入 EQ-R6：先运行 1/2500，仅在 clipping-only 失败时运行 1/3200；最多 8 张 CR3、retry 0、每档 A600+C600，并执行双 cleanup、final-zero 和 terminal seal。

该确认已接受并归档：

- `.agent-work/PLANS/20260727-1324-p7-eq-r6-human-checkpoint-live-owner-review.md`
- SHA-256：
  `9a8f959d9a471a9226a26ac829272665df88f8c6a0ffe70a690fb9cef88138a6`
- reviewed checkpoint PLAN SHA-256：
  `0c6530260eb60e052a4cd08fc65bab1e50dcac51846f543c6d238fd0c25a896f`

Planner静态核对确认当前实现不能直接运行 EQ-R6：

- `build_td_b_eq_r6_plan()` 明确是 `offline_contract_only` 且 `executable=False`；
- 唯一 EQ scheduler 为 `run_td_b_eq_r6_fake()`；
- production CLI没有 EQ-R6 execute/orchestrate mode；
- 通用 wrapper没有“candidate 1 完整 cleanup/final-zero/seal之后，才由 clipping-only分类解锁独立
  candidate 2 wrapper sequence”的 outer owner。

因此本包只修复执行入口和生命周期，不执行实验。若本包被 Planner接受且 scientific bounds未变化，
后续 exact `REF-P7-23` 可直接消费已记录的 Human确认，不得再次要求同一批准。

## 2. Frozen inputs

| Input | Frozen value |
|---|---|
| applicable GUIDE | `advisor/4/4.GUIDE.md` |
| GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| Orchestrator FULL active-C0 SHA-256 | `b7b06e1a7160fff5a324428a5a6cc149b515f113ba18776525508fd32d31e109` |
| terminal EXECUTION_RESULT input SHA-256 | `aa08b4ba9a2b5301880fa4097d3d557d22817b5bc63f54e4a88e4533907a2807` |
| project skill SHA-256 | `c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607` |
| exposure policy SHA-256 | `9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2` |
| thermal contract source SHA-256 | `8ff49485abfd03d31d16addaaed33026f6a7aa3b334b7f768f3e17e1e4fdc719` |
| measurement runner source SHA-256 | `accc38aed15d25f3aec7b9764005bbd32e19d7df93b656a335cbd16b788e264e` |
| existing EQ test SHA-256 | `365391e90012bf8f90dc0e3c587152e3b64ea120e3707e10fa8eecb3fc5b6eb7` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |

本次 FULL hash 更新仅记录 Orchestrator 将 reference 转为 stable active C0 contract state；不扩展设备、
EQ、权限、预算、root、capture、release或后续stage边界。

在首次改动前必须 fail closed 核对：

1. `HEAD` 与 expected parent HEAD相等；
2. 上表 source/policy/GUIDE hashes相等；
3. staged paths为空；
4. 允许保留当前 worktree 中 Human/其他owner已有的 PLAN/FULL/EXECUTION_RESULT/advisor/archive改动，
   但不得编辑、恢复、重排、stage或commit它们；
5. 以下 correction evidence root不存在，且其任何父级不是symlink：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c0-offline/eq-r6-c0-98de1a9-20260727T1324
```

任一冻结项不符：不改代码，记录 exact mismatch并停回 Planner。

## 3. Scientific contract 不得改变

实现必须原样消费现有 EQ contract，不得借 correction修改：

```text
candidate 1 shutter = 1/2500
candidate 1 IDs =
  000-ray-c2500-t60
  001-ray-c2500-t120
  002-ray-c2500-t300
  003-ray-c2500-t600
candidate 2 shutter = 1/3200
candidate 2 IDs =
  004-ray-c3200-t60
  005-ray-c3200-t120
  006-ray-c3200-t300
  007-ray-c3200-t600
slots = 60/120/300/600 seconds
per-candidate sequence = strip zero -> A600 no capture -> C captures -> off/cleanup/final-zero/seal
candidate 2 unlock = candidate 1 first failure is exactly clipping-only
physical CR3 cap = 8 total, 4 per candidate
formal = 0
ambient = 0
retry/relaunch/same-root replay = 0
```

58-feature order、clipping threshold 0、near-noise/finite/valid-pixel、recorded exposure ratio、
no-ambient statistic、source isolation、physical-return-before-processing、A/D/B shutters、600秒
transient语义均保持现有 owner。不得添加 `1/4000`、更快shutter、自动曝光、fallback或 tolerance widening。

## 4. Implementation ownership 与 maintainability preflight

这是 high-risk device/lifecycle boundary。实现前先固定 ownership：

```text
p7_thermal_diagnostics.py
  owns exact EQ contract, activation validation and classification

measure_p7_thermal_diagnostics.py
  owns candidate execution adapters, outer conditional orchestration,
  progressive evidence and final classification

tmp/run-p7-thermal-diagnostics.zsh
  remains the single production child/wrapper cleanup owner

camera_remote + existing physical-return helpers
  remain the only CR3/sidecar/remote-ID return owners
```

不得创建第二套 generic thermal runner、第二套 physical ledger、第二个 camera backend、第二个
all-off implementation或新的 root-level CLI wrapper。若 direct change会把通用 `main()` 变成不清晰的
branch god-object，先做最小的 EQ argument validator/dispatcher extraction并用测试保护；不要重构无关 formal/setup
路径。

允许修改的 production/test/docs paths上限：

```text
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
tmp/run-p7-thermal-diagnostics.zsh
docs/README.md
.agents/skills/camera-based-rgbww-optimizer/SKILL.md
```

只有实际需要记录新 module command/lifecycle时才改 docs/skill；不得编辑其他 production、test、wrapper或
project policy文件。若必须超出此 path set，先停回 Planner。

## 5. Required live-owner structure

实现必须建立以下可测试边界；具体私有helper命名可遵循现有风格，但 owner不得合并或省略。

### 5.1 Explicit activation

- offline `build_td_b_eq_r6_plan()` 继续是 non-executable contract；
- 新的 activation/validator必须只从 exact offline plan、current checkpoint、frozen exposure policy与
  unique output owner构建 live-bound plan；
- live validator必须拒绝 contract/policy/checkpoint/root/candidate/order/budget任一漂移；
- generic formal/setup `--execute`不得误接收 offline EQ plan；
- CLI必须有显式 EQ-R6 orchestrate mode和只供 outer owner调用的 single-candidate mode，二者不能与
  dry-run、formal、setup、release modes混用。

### 5.2 One candidate per wrapper lifecycle

- 每个 wrapper child只能运行一个 candidate；
- candidate child在任何正常/异常路径均先执行 Python cleanup并落盘 progressive evidence；
- enclosing existing production wrapper无条件执行 shell cleanup并记录 child/signal/cleanup exit；
- outer owner观察 wrapper退出后执行 independent final-zero并写 terminal seal；
- 只有 candidate 1 terminal seal完整通过且其 first failed returned capture分类严格等于
  `{"clipping"}`，outer owner才允许创建/启动 candidate 2独立subroot；
- candidate 1 `4/4 pass`、任一non-clipping failure、cleanup/readback/evidence failure均必须令
  candidate 2 attempted launch count保持0。

### 5.3 Physical and progressive evidence

每个 camera request/return必须复用既有 remote-v2/physical-return验证，做到：

- attempted call在调用前落盘；
- returned CR3在任何decode/feature/quality处理前写 path、bytes、SHA-256、sidecar path/bytes/hash、
  remote capture/request IDs；
- rejected return也保留同样的已验证 evidence；
- attempt、physical return、accepted/rejected、candidate与total cap分开计数；
- artifacts采用 atomic JSON或append+flush JSONL，strict JSON、`allow_nan=False`；
- root/subroot必须fresh、regular、non-symlink，所有artifact必须留在correction所验证的run owner内；
- terminal seal绑定 plan/source hashes、wrapper source hash、candidate classification、cleanup、
  final-zero、attempt/return counts与所有canonical artifact hashes；
- exception/signal/adapter drift/partial JSON不得被写为success，也不得解锁下一candidate。

### 5.4 Later visible-Terminal compatibility

本包不启动Terminal，但实现必须让后续 `REF-P7-23` 能：

- 由 Human-visible macOS Terminal进行单一 outer launch；
- 在首次device call前写 immutable launch ledger，绑定outer PID、child wrapper PID、root、HEAD、
  PLAN/policy/source hashes与exact argv（secret/private override不得出现）；
- 允许Executer只做三次稀疏liveness检查后把 PID/root/ledger/ETA交Orchestrator；
- outer process覆盖一至两个合法 candidate，但每个candidate仍各有独立wrapper exit、cleanup、
  final-zero与terminal seal；
- 不需要Codex background process，不依赖现场手工编辑artifact，也不要求在candidate之间重新授权。

## 6. Offline-only adversarial validation

所有测试必须使用 injected fakes、临时fixture与无副作用 subprocess stub。必须显式断言：

1. candidate 1 `4/4 pass`：选择 `1/2500`，candidate 2 launch/attempt/capture为0；
2. candidate 1首张、第二张及后续任一 capture clipping-only：当场停，不补该candidate剩余slot；
   candidate 1完整 cleanup/final-zero/seal后只启动一次 candidate 2；
3. candidate 1 low-signal、nonfinite、invalid-pixel、metadata、ratio、source/readback任一failure：
   hard stop，candidate 2为0；
4. candidate 2 `4/4 pass`选择 `1/3200`；candidate 2任一failure为
   `exposure_window_unresolved`；
5. Python cleanup、shell cleanup、wrapper exit、independent final-zero或terminal seal任一failure：
   final status失败，后续candidate为0；
6. exception、SIGINT/SIGTERM/HUP、child nonzero、missing/malformed/tampered progressive artifact均
   fail closed；
7. physical evidence先于decode/feature callback；sidecar缺失、越界、symlink、hash drift、
   remote ID drift均保留可证明的returned CR3 evidence后失败；
8. candidate cap 4、total cap 8、formal/ambient 0、retry/relaunch 0不可绕过；
9. duplicate/nonfresh/symlink root、wrong HEAD/policy/plan/wrapper hash、wrong IDs/order/shutter/slot、
   public/private parameter leakage均在device adapter调用前拒绝；
10. existing setup/formal/release CLI与wrapper regression保持原行为，EQ mode不能意外进入它们；
11. fake orchestration证明每个candidate有独立 wrapper lifecycle和terminal seal，第二candidate的
    launch timestamp严格晚于candidate 1 seal；
12. launch ledger immutable，second write/tamper/rebinding拒绝；argv/artifacts/log不含secret、
    token、private credential或 `.env` 内容。

测试证据至少包括：

```text
focused EQ-R6 contract/lifecycle suite
all tests covering measure_p7_thermal_diagnostics and production wrapper
full pytest suite
python compileall for touched Python modules
zsh -n tmp/run-p7-thermal-diagnostics.zsh
strict JSON parse of every generated JSON artifact
git diff --check
CodeGraph sync + changed-symbol/blast-radius check
```

若 full suite存在与parent HEAD相同的已知baseline failure，必须以同命令在unmodified parent worktree或
可证明的baseline evidence对照；不得把新failure归为baseline。任何新相关failure都拒绝本包。

## 7. Frozen zero-side-effect budget

```text
network calls = 0
.env reads = 0
real remote backend construction/calls = 0
real camera/gphoto2 calls = 0
real Ray calls = 0
real ESPHome/strip calls = 0
real all_off calls = 0
nonzero light output = 0
CR3/NPY/TIFF capture = 0
EQ-R6 real root/visible Terminal launch = 0
release generation/qualification/consumption = 0
formal R6/strip/TD-C/public analyzer = 0
firmware/deployment/destructive hardware = 0
retry = 0
```

测试必须通过 injected counters/forbidden fakes证明以上为0；不能仅以“未观察到”代替。

## 8. Evidence package

只允许创建一次 frozen correction root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c0-offline/eq-r6-c0-98de1a9-20260727T1324
```

至少包含：

```text
frozen-inputs.json
implementation-manifest.json
eq-r6-adversarial-matrix.json
wrapper-lifecycle-matrix.json
cli-isolation-matrix.json
side-effect-accounting.json
test-results.json
strict-json-audit.json
codegraph-audit.json
validation-summary.json
terminal-summary.json
```

`validation-summary.json` 必须列出每个canonical artifact的absolute path、bytes、SHA-256，记录
parent/new HEAD、commit、actual changed/committed paths、test totals、all mismatch arrays与明确
`real_eq_r6_invocations=0`。写入后不得修补原artifact；若summary自身计数错误，停回Planner报告，禁止
same-root重建。

## 9. Focused commit contract

离线验证通过后，创建一个 focused commit：

```text
fix(p7): add bounded eq-r6 live owner
```

要求：

- parent必须是 expected parent HEAD；
- 只stage第4节允许集合中实际修改的paths；
- `.agent-work/PLAN.md`、`FULL_PLAN_REFERENCE.md`、`EXECUTION_RESULT.md`、所有PLANS archives、
  advisor files与既有unrelated dirty/untracked paths不得stage；
- commit前记录 staged path set与blob hashes；commit后验证commit path set/message/parent；
- commit后重跑focused EQ/lifecycle tests、`zsh -n`、`git diff --check`与CodeGraph sync；
- 不push、不建PR、不生成release。

若实现或验证失败，不得创建“部分成功”commit；保留evidence并停回Planner。

## 10. Executer handoff

Executer只向 `.agent-work/EXECUTION_RESULT.md` 追加：

- frozen-input preflight；
- ownership/maintainability判断；
- exact changed paths与关键合同；
- adversarial matrix及全部test/check结果；
- correction root、canonical artifact hashes与terminal summary；
- side-effect counters；
- commit SHA/parent/message/path set；
- residual risks和 Planner decision request。

不得修改本 PLAN、FULL、GUIDE/RESEARCH或archive。handoff必须明确：

```text
this package did not execute EQ-R6
Human confirmation is preserved but device execution remains Planner-locked
next decision belongs to Planner
```

维护性判断：本包影响 thermal contract、runner/CLI与wrapper lifecycle三个边界。实现必须复用既有
camera/physical-return/cleanup owners，把新增复杂度限制在显式 EQ dispatcher、single-candidate owner和
outer lifecycle orchestrator；adversarial tests覆盖分支、evidence与失败关闭。若需复制通用runner或新增
平行wrapper，应拒绝并回Planner重划边界。

---

## Planner review：REF-P7-23-C0 rejected

**Review 时间：** 2026-07-27 14:01（America/Edmonton）

**Reviewed PLAN SHA-256：**
`8779e9312a471da87eeb4324d29aea37f03e8eacb83ed85ae8e79d68d0b5a043`

**Reviewed EXECUTION_RESULT：**
`.agent-work/EXECUTION_RESULT.md` §136，SHA-256
`d9113e4216a34cb69827f2b6846e6ebcbc6378c51d2d5fe1fdd2d81976c93900`

**Orchestrator review FULL SHA-256：**
`a438ffc0f2e0170ee3e291357b4bdf303816be96951b76ff04103bbdc9189ee5`

### Reviewed implementation and evidence

- C0 commit：
  `57985fa74301e26d097c96e69e52661714fea7b3`，parent
  `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`。
- commit message：
  `fix(p7): add bounded eq-r6 live owner`。
- exact committed paths：
  - `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
  - `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
  - `tests/test_p7_td_b_r6_contract.py`
- validation summary：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c0-offline/eq-r6-c0-98de1a9-20260727T1324/validation-summary.json`，
  SHA-256 `aca05551c26f512799cb2de0eea2342d30ace04360a71ac29b29fe0e56d541a2`。
- terminal summary：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c0-offline/eq-r6-c0-98de1a9-20260727T1324/terminal-summary.json`，
  SHA-256 `a33aa0ec87a37ae98cde1d5762acd65e0513a57fd04babea84735728ae5f9a6b`。
- reported tests：focused/post-commit `124/124`，full `618/618`。
- reported side effects：real EQ、device、network、`.env`、camera、Ray、strip、all_off、
  capture与release均为0。

C0确实建立了 explicit live activation、single-candidate runner、outer conditional owner、physical-return
evidence、CLI isolation与基本 wrapper seal。commit、reported test totals及offline zero-side-effect结论
不因下述拒绝而撤销；但这些结果不足以满足 C0 PLAN 的 adversarial acceptance。

### Acceptance-blocking finding 1

**ID：** `REV-EQ-R6-C0-001`

**Finding：** launch ledger 的 runtime identity/argv 可以在落盘后被合法形状的值重新绑定。

`_validate_td_b_eq_r6_launch_ledger()` 对 `outer_pid` 与 `wrapper_pid` 只要求正整数；对 `argv`
只要求非空且不含private词。它没有接收/核对 expected outer PID、expected wrapper PID或 exact expected
argv/binding digest。`_seal_eq_candidate()` 再次调用同一弱validator，也没有把 `wrapper-result.json`
中的 wrapper/child ownership反向绑定 launch ledger。

Planner fresh injected diagnostic在独立temp root中分别将已写ledger改为：

```text
outer_pid = 999999
wrapper_pid = 888888
argv append "--safe-flag"
```

三种情况均返回 `ACCEPTED_TAMPER`。现有
`test_launch_ledger_tamper_rejects_before_any_adapter` 只篡改
`measurement_runner.sha256`，未覆盖 PID/argv rebinding。C0
`eq-r6-adversarial-matrix.json` 却将“second write/tamper/private argv rejected”写为pass，因此matrix
truth与真实覆盖不一致。

**Impact：** immutable launch ledger不能证明被审计的outer/wrapper process与exact argv就是之后访问设备、
写candidate evidence并被terminal seal接受的process/command；违反C0 PLAN §5.3、§5.4、§6.9、§6.12。

### Acceptance-blocking finding 2

**ID：** `REV-EQ-R6-C0-002`

**Finding：** outer owner在 wrapper evidence缺失等早期失败路径不会尝试 independent final-zero。

`orchestrate_td_b_eq_r6()` 在 `run_fn()` 返回后先检查 `wrapper-result.json`，缺失时立即raise；只有该文件
存在才调用 `final_zero_fn()`。Planner fresh injected diagnostic令subprocess返回0但不生成wrapper-result，
结果为：

```text
RuntimeError: EQ-R6 wrapper exited without wrapper-result evidence
final_zero_calls = []
outer-failure.json = present
```

同类漏洞还覆盖 subprocess exception、malformed/tampered wrapper-result、seal前解析/验证错误以及
`KeyboardInterrupt`/`SystemExit`。现有测试只证明部分shell/final-zero失败会阻止candidate 2，没有证明
所有BaseException路径都best-effort执行并持久化 independent final-zero。

**Impact：** runner在真实设备可能已被child触达后，无法保证outer-level final-zero attempt/evidence；
违反C0 PLAN §5.2、§6.5、§6.6与唯一安全停止合同。

### Planner decision

`REF-P7-23-C0 = REJECTED_ACCEPTANCE_BLOCKING`。

拒绝原因是普通 code/evidence correction，不需要 Advisor科学决定，也不改变Human已确认的candidate、
shutter、强度、时长、预算或branch。不得撤销、重写或rebase C0 commit；下一包必须以
`57985fa74301e26d097c96e69e52661714fea7b3` 为parent完成最小C1修复。

### Residual locks

- Human exact EQ-R6确认继续有效，C1通过且scientific bounds不变时无需重问；
- 设备、网络、`.env`、camera、Ray、strip、真实all_off、capture、EQ root/launch、release、formal R6、
  strip stage与TD-C仍为0；
- C0 evidence保持只读，不得修改或用同root重建matrix；
- candidate 2必须在candidate 1 terminal seal完整通过且clipping-only后才可能解锁；
- C1不得借机修改observer、58 features、quality thresholds、shutters、A600+C600、physical cap8或retry0。

### Exact next branch

```text
REF-P7-23-C1
P7-TD-B-EQ-R6-RUNTIME-BINDING-AND-FINAL-ZERO-CORRECTION
pure offline
parent = 57985fa74301e26d097c96e69e52661714fea7b3
```

C1只修复 runtime PID/argv binding、terminal ownership关联与所有outer failure路径的best-effort
independent final-zero/terminal failure evidence，补fresh adversarial tests与真实matrix。通过focused/full/
static/zero-side-effect验证后才允许focused commit，然后必须停回Planner；同包不得启动EQ-R6。
