# P7-TD-B-E0X+EXEC：闭合生产回环并连续执行 Setup -> Ray -> Strip

**计划状态：** `offline_gate_then_bounded_execution_authorized`

**Planner 日期：** `2026-07-21T23:58:34-0600`

**当前阶段：** `P7_TD_B_PRODUCTION_ORCHESTRATION_AND_COMMAND_SWITCH_DIAGNOSTIC`

**当前唯一动作：** Executor 先离线修复 R0S 暴露的 production orchestration 缺口；仅当 E0X 的真实
CLI/wrapper/finalizer fake round-trip、负例、focused/full suite 和 checkpoint 全部通过时，在同一工作包
内依次执行一次 Ray H120/S50 setup、Ray TD-B、strip TD-B、双单源分析和成对交接。E0X 通过后不设置
普通 Planner 停点。

**唯一 Planner 停止点：** 两源 TD-B 均完成结构合法的 retained acquisition、public analysis、final
manifest 和独立双源 zero readback后停止；或者任一 hard-invalid/fail-closed 分支完成证据保留与双关灯
后立即停止。不得进入 TD-C 或任何后续阶段。

## 1. 上轮验收与归档

P7-TD-B-R0S 离线合同已接受并归档：

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260721-2358-p7-td-b-r0s-review.md` | `301579bb07082bd6e538a1ebeda483b938cb7dfe2d73634f9e968a709be964a5` |

验收决定：

```text
r0s_offline_contract = accepted
historical_p6_shutter = seed_only
fake_setup_resolution = accepted
real_td_b_execution_ready = false
blocking_scope = production_orchestration_only
next = E0X offline gate, then one continuous bounded TD-B diagnostic
```

R0S 的 schema、seed audit、1..8 physical ledger、analyzer replay 和 fail-closed validator 不得回滚。
真实 CLI 当前仍会在 backend connect 前拒绝 unresolved `ray-h120-s50`；这是本包 E0X 必须闭合的入口。

## 2. Human/Developer 决策和设备权限

本项目 `AGENTS.md` 已明确：在 active PLAN 边界内开关 Ray120c 或 RGBWW 灯带不需要另行 Human
授权。Executor 可直接消费本计划的有界灯光/相机诊断，不得重复询问开灯授权。

本计划授权的唯一 named experiment：

```text
p7_td_b_command_switch_history_v1
```

CLI 兼容参数仍可使用：

```text
--execute
--allow-device-control
--human-authorization p7_td_b_command_switch_history_v1
```

这里的旧参数名仅为现有代码 gate，不表示 Planner 擅自生成新的 Human 科学决定。禁止 firmware
compile/upload、remote deployment、破坏性硬件修改或任何本计划以外的设备动作。

## 3. 科学语义冻结

600 秒来自 Developer/Human 的时间上限决定，不是 steady-state 推导：

```text
decision_owner = Developer/Human
planner_inference = false
thermal_extension_900_1200 = rejected
developer_selected_operational_dwell_s = 600
operational_dwell_claim = selected_time_limit_not_proven_steady
```

以下字段必须继续保持：

```text
Ray TD-A = settling_not_demonstrated_by_600
strip TD-A = settling_not_demonstrated_by_600
t_settle_ray_s = null
t_settle_strip_s = null
t_formal_provisional_s = null
t_formal_s = null
```

TD-B 只诊断 600 秒 operational dwell 下的 command-switch/history 行为。即使结果通过结构门，也不得
输出 `settled_at_600`、`steady` 或自动写 `td_b_pass`；Developer override 分支的合法科学状态只允许：

```text
td_b_operational_600_complete_waiting_for_planner
history_dependent_at_operational_dwell_600
```

另可附带 structured nonstationarity warning。禁止修改 trend `4.0`、single-frame dominance `0.5`、
58-feature、covariance、joint coverage、P6 `full_periodic_2d_HB` topology、默认 LUT/runtime config、
TD-A retained evidence 或 v1 operating envelope。

## 4. 必读输入和冻结哈希

Executor 必须先阅读：

1. 本文件全文；
2. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
3. `docs/README.md` 的 P7 thermal/timing/setup/cleanup 章节；
4. `.agent-work/PLANS/20260721-2358-p7-td-b-r0s-review.md`；
5. `.agent-work/EXECUTION_RESULT.md` 第 24 节；
6. `config/hsi/p7-operating-envelope-v2.json`；
7. `advisor/3/1.GUIDE.md` 与 `advisor/3/1.RESEARCH.md`；
8. 当前 CodeGraph 和 `git status --short --branch`。

冻结输入：

| 输入 | SHA-256 |
| --- | --- |
| R0S checkpoint `2030b9f` | `2030b9fe79bd0b80d703cfd221a404df3807c033` |
| `config/hsi/p7-operating-envelope-v2.json` | `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16` |
| `config/location/locations-20260714-211759.json` | `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| `config/hsi/strip-hsi-policy-v2-waiting.json` | `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| `config/hsi/ray-hsi-manifold.json` | `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| `config/channel/code-duty-curve.json` | `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |
| production wrapper at review | `4f776135b18df57897011d6c37f7683768d772cd5a9ee7f73c07f2ffae0d7dfb` |
| R0S validation | `7ef454eed34c4de43f7cb065102b2e09dbc24c7567aad0349b33b824838edbfb` |

R0S evidence root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-setup-offline/20260721-231909
```

任何冻结 config/location/policy/manifold/curve hash 漂移都必须在设备连接前停止。E0X 允许修改并重新
冻结 production code、tests、docs、skill 和 wrapper；不得修改上述实验输入。

## 5. E0X：离线 production round-trip

### 5.1 必须闭合的五个 finding

实现并测试：

```text
R0S-PR-001 setup function not wired to CLI
R0S-PR-002 canonical setup needs post-wrapper finalization
R0S-PR-003 generic auto exposure deletes attempts and uses /v1
R0S-PR-004 source isolation not validated before first setup capture
R0S-PR-005 code/plan/wrapper/resume binding incomplete
```

### 5.2 单一生产状态机

保持现有 `p7_thermal_diagnostics` / `measure_p7_thermal_diagnostics` owner，不建立平行 runner。正式 Ray
TD-B 入口必须表达以下状态：

```text
preflight_validated
setup_running
setup_capture_complete_waiting_for_wrapper_finalize
setup_canonical_complete
formal_plan_resolved
formal_running
formal_complete
```

允许使用 provisional artifact，但它不能 formal-eligible。Wrapper 退出并产生真实 child/shell/signal/
cleanup evidence后，外层 orchestrator 必须再执行一次独立 post-wrapper `all_off`、generation-bearing
strip-zero snapshot 和 Ray intensity-zero readback，并保存为单独 artifact。只有这些实际文件全部存在且
通过时，窄 finalizer 才能原子生成 canonical setup artifact。Formal resume 必须重新读取 canonical
artifact，重放 hashes/owners/cleanup/cold wait，然后生成 resolved plan；禁止进程内仅凭内存对象继续，
也禁止 child 预报未来 shell/final-zero evidence。

正式 CLI 至少需要等价能力：

```text
--phase setup
--phase formal --setup-artifact <canonical setup.json>
```

也可用语义等价的显式子命令，但不得让默认 `--execute` 隐式猜测 phase。Dry-run 必须显示 phase、
setup requirement、budgets、device lock 和 output owner。

### 5.3 Retained remote-v2 auto exposure

复用 `camera_gphoto2` 现有 candidate ordering、metering、acceptance、bracketing 和 final-selection 逻辑；
不要复制或改写第二套搜索算法。增加最窄的 capture/deletion strategy 或 hook，使 TD-B setup 能：

- 每次 physical attempt 都走 `RemoteCameraBackend.capture_with_timing()` / `/v2/capture`；
- 保留 trial、rejected final 和 selected final 的非空 CR3 与 sidecar；
- 每次独立记录 capture/request ID、hash、byte count、recorded exposure、shutter、timing tier/method；
- 删除所有 decode `.npy`，不删除 setup CR3/sidecar；
- 最多 8 physical CR3，且第 9 次请求在 capture 前拒绝；
- adapter 在产生 CR3 后失败时仍把该张计入 physical ledger并保留路径/hash。

冻结 setup 曝光参数：

```text
state = Ray H120/S50/INT100
historical initial seed = 1/6400, seed_only
target_max = 19661
accepted_min = existing auto-exposure 0.85 ratio
min_shutter_speed = 1/16000
max_shutter_speed = 25
max_physical_cr3 = 8
ISO/aperture/RAW = resolve once from remote config
metering = existing frozen location/observer native RAW meter
```

不得用当前相机 shutter、普通 `/v1/capture` 或 formal cycle 当前状态替代 seed/adapter。

### 5.4 第一张 setup CR3 前的强制验证

在调用 retained-v2 exposure adapter 前，必须已经独立验证并落盘：

- exact named experiment、phase、code checkpoint、input hashes 和 budgets；
- remote `/health`、认证 config、v2 capability、ISO/aperture/RAW 和 shutter choices；
- Ray set response 与 independent HSI readback精确为 H120/S50/raw INT1000；
- strip generation-bearing state 为五通道全零、device identity/MAC 稳定；
- run start 双源 off/readback gate 先通过，再只打开 Ray；
- output directory 是全新 owner，没有 symlink/path escape。

若任一项失败，capture count 必须为 0，执行 Python/shell 双 cleanup 后停止。

### 5.5 Cold proxy 和 finalization

Setup capture phase结束后立即双源关灯并独立 zero readback，再开始 monotonic 1800 秒 off wait。该 wait
属于 setup artifact，必须完整执行；不能与 formal A0 的 600 秒合并。Shell cleanup 和 wrapper exit 在
child退出后落盘，canonical finalizer必须从 retained文件重建，不接受 caller 注入的假 shell evidence。

Canonical artifact和resolved plan必须绑定：

```text
E0X implementation commit (full 40-char HEAD)
unresolved plan hash
setup provisional hash
wrapper source hash
wrapper-result hash
all-off-python hash
all-off-shell hash
final-zero hash
canonical setup hash
resolved formal plan hash
```

真实 artifact 的 code checkpoint 必须等于执行时 HEAD；dirty code/config/wrapper 必须 fail closed。允许
工作区仅有 Planner-owned `.agent-work/PLAN.md`、archives、advisor 或其他已知文档改动；生产 src/tests/
config/docs/skill/wrapper 相对 checkpoint 必须干净。

### 5.6 Fake production round-trip 和负例

E0X 至少覆盖：

1. 正式 CLI setup phase fake backend：1..8 次各自通过；9 在 capture 前拒绝；
2. `/v2` attempt、CR3/sidecar、recorded exposure、ID/hash/byte-count/owner replay；
3. trial/rejected-final/final 均 retained，`.npy=0`；
4. pre-capture Ray/strip isolation 错误导致 0 capture；
5. child success + shell cleanup success -> canonical setup；
6. child failure、cleanup failure、INT/TERM/HUP 不产生 formal-eligible setup；
7. provisional、fake、wrong HEAD、wrong wrapper、wrong plan、stale setup、path escape 全部拒绝；
8. formal resume从 canonical disk artifact重建 resolved plan，不使用进程内 shortcut；
9. setup 8 + formal 16 = physical 24；formal runner 不再 auto-expose；
10. public analyzer独立重算 setup/formal/physical ledger并排除 setup statistics；
11. strip TD-B 不要求 setup artifact，保持 16 formal / 0 ambient；
12. TD-A v1/v2、R0/R0S replay、remote v2 parser和wrapper六分支保持兼容；
13. dry-run/fake validation 为 0 device/network/`.env`/`all_off` side effect。
14. TD-B paired finalizer fake round-trip、input manifest/hash/owner tamper拒绝、单源状态不被改写、final
    zero证据缺失时拒绝。

### 5.7 E0X 验证门和 checkpoint

所有证据写入新目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-production-offline/<timestamp>/
```

至少运行：

```zsh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest \
  tests.test_p7_thermal_diagnostics \
  tests.test_analyze_p7_thermal_diagnostics \
  tests.test_measure_raw_observer_validation \
  tests.test_camera_gphoto2 \
  tests.test_camera_remote -v

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q src tests
zsh -n tmp/run-p7-thermal-diagnostics.zsh
git diff --check
codegraph sync
```

生成 `validation-summary.json`、production fake artifacts、negative-case matrix、full/focused logs 和 SHA-256。
E0X 实现/测试/docs/skill/wrapper通过后创建一个 focused conventional commit，并把 full 40-char commit
写入 readiness。提交后再执行 post-checkpoint release gate：生产 `src/tests/docs/.agents/skills/tmp wrapper`
相对 HEAD 无 diff、input/wrapper hash一致、production fake CLI/wrapper/finalizer round-trip再次通过。若任何
检查失败，停在 Planner，不访问设备。

## 6. E0X 通过后的连续实机包

### 6.1 总顺序和预算

禁止并行，只允许：

```text
device preflight
-> Ray H120/S50 setup (1..8 physical)
-> both off + 1800 s cold proxy
-> Ray TD-B formal (16 physical)
-> Ray public analysis
-> strip TD-B formal (16 physical)
-> strip public analysis
-> paired handoff/final manifest
-> independent final both-off/readback
-> Planner stop
```

预算：

| Source/package | Formal | Setup | Ambient | Physical cap |
| --- | ---: | ---: | ---: | ---: |
| Ray | 16 | 1..8 | 0 | schema cap 24 |
| strip | 16 | 0 | 0 | schema cap 24 |
| combined | 32 | 1..8 | 0 | actual cap 40 |

真实允许范围只有 33..40 physical：Ray 必须等于 `setup_count + 16`，strip 必须恰好 16，combined 必须
等于 `setup_count + 32` 且不超过 40。既有 per-source schema 中的 24 只保留兼容性，不能相加为 48，
不能授权 strip extra capture，也不能隐藏 formal retry。任何不等式或超限都是 fatal accounting failure。

### 6.2 实机 preflight

由脚本读取 `.env`，不得由 Executor读取或打印 secret。依次验证：

- 没有无法证明 ownership 的 camera/calibration/thermal process；
- E0X checkpoint、wrapper 和冻结 inputs hash 一致；
- `control.all_off` 成功，Ray intensity 0；
- ESPHome `bedroom-rgbww-strip` identity/MAC/generation-bearing五通道全零；
- remote health、authenticated config、v2 capability、RAW/ISO 100/非空 aperture；
- Ray node config、HSI/CCT readback可用；
- camera location仍为 `locations-20260714-211759.json`；
- 新 run、log、wrapper-state path 均不存在。

Preflight失败：保留 artifact，执行 Python+shell关灯和独立 zero readback，停止，不 retry。

### 6.3 Ray setup 和 formal schedule

Setup exact command：

```text
Ray = H120/S50/INT100
strip = cw/ww/r/g/b all zero
```

Setup 成功 canonical finalize后，在新 formal run中使用：

```text
A = Ray H120/S100/INT100, shutter 1/5000
D = Ray H120/S50/INT100, shutter from canonical setup only
B = Ray H0/S0/INT100, shutter 1/8000
C = Ray H300/S100/INT100, shutter 1/2000
```

Capture chronology：

```text
A0 at 600
D at 60/120/300/600
A return at 600
B at 60/120/300/600
A return at 600
C at 60/120/300/600
A return at 600
```

每个 command group只发送一次命令并精确 readback；组内持续点亮至最后 capture。每次 group transition
必须先双关灯/读回，再打开新状态。只有 Ray亮，strip始终 generation-bearing verified zero。Formal cycle
`auto_exposure=false`，每个 step恰好一个 retained remote-v2 CR3。

### 6.4 Strip formal schedule

只有在 Ray acquisition 的 capture/timing/ownership/source-isolation/cleanup/wrapper 合同结构合法时才继续
strip。Ray analyzer若科学状态为 history-dependent 或 nonstationarity warning，仍继续 strip；这正是成对
诊断目的。Ray hard-invalid、measurement failure或 cleanup uncertainty则停止。

Strip exact commands/shutters：

```text
A: cw=518, ww=0, r=0, g=4095, b=0; shutter=1/320
D: cw=4095, ww=0, r=0, g=3118, b=13; shutter=1/400
B: cw=4095, ww=4095, r=0, g=1887, b=1535; shutter=1/500
C: cw=406, ww=0, r=4095, g=0, b=1541; shutter=1/125
```

Chronology与 Ray完全相同。只有 strip亮，Ray intensity始终独立读回 0；`verified_light` 必须逐 transition
记录 generation、identity、requested raw command和readback。Formal cycle不得 auto-expose。

### 6.5 Timing、曝光和 retained evidence

- nominal `60/120/300/600` 仅用于调度/分组；
- 只接受 Tier A/B finite/nonnegative observed elapsed；不使用 proximity gate；
- 保存 gphoto2 estimate method，`absolute_exposure_start=false`；
- chronology必须在同一 command group内严格递增；
- camera settings每个 run只从remote config解析一次并注入全部 capture；
- 每张 CR3非空、recorded exposure、v2 sidecar、hash、byte count、capture/request ID都可重放；
- 不保留 `.npy`；setup CR3是例外，它全部保留但不进入 formal analysis。

### 6.6 长任务所有权

Setup、Ray formal、strip formal 都必须通过 `tmp/run-p7-thermal-diagnostics.zsh` 或同一受测 production
wrapper运行。每个子 run保留独立 run dir、runner/wrapper log、wrapper state、PID/PPID/PGID/TTY、start
time、child/shell/signal/final exit evidence。

启动后做一次约 3 分钟健康检查。随后使用当前 task 的稀疏一次性 heartbeat按 ETA恢复；不得短间隔轮询，
不得因为结束回答而杀掉任务。仍运行时按 completed/target 和实际 elapsed重估，只创建下一次 one-shot。

### 6.7 Cleanup

每个 setup/formal run均必须：

- Python `finally` 无条件关 strip和Ray；
- shell EXIT/INT/TERM/HUP trap独立调用 `control.all_off`；
- 保存两层 exit和输出；
- run完成后独立取得 strip generation-bearing zero + Ray intensity 0。

缺任一 cleanup证据时立即执行 recovery `control.all_off` 并保存结果。任何 cleanup uncertainty都阻止下一
source；即使科学结果有效也不能继续。

## 7. 分支矩阵

### 7.1 可继续分支

```text
E0X all pass + focused/full/compile/wrapper/diff/CodeGraph pass
  -> commit exact checkpoint -> device preflight

preflight pass
  -> setup

setup canonical pass + both-off pass + full 1800 s wait
  -> Ray formal

Ray acquisition structurally valid + cleanup certain
  -> analyze Ray
  -> even if history-dependent/nonstationary, continue strip

strip acquisition structurally valid + cleanup certain
  -> analyze strip -> paired manifest -> independent final zero -> Planner stop
```

### 7.2 必须停止分支

```text
E0X test/round-trip/checkpoint failure
  -> no device calls; record and stop

preflight failure
  -> cleanup + independent zero; stop

setup 0-result/unreachable/invalid v2 evidence/9th request/budget drift
  -> preserve every produced CR3; cleanup; no Ray formal

post-setup cleanup/cold wait/canonical finalizer/resolved-plan failure
  -> cleanup; no Ray formal

Ray hard-invalid, missing CR3/sidecar, chronology/source/readback/ledger failure, cleanup uncertainty
  -> cleanup; no strip

strip hard-invalid or cleanup uncertainty
  -> cleanup; no paired scientific claim
```

唯一允许的自动启动修复：launcher 在任何 device command、camera request、CR3 或 run owner产生前失败，且
双源 zero已独立确认时，可修复 launcher并在**全新目录**重试一次。任何非零 command或capture开始后不得
自动重跑该 source/setup。

## 8. 最终分析和交接

对每个结构合法 run运行 public `analyze_p7_thermal_diagnostics`。需要新增或复用一个窄的 TD-B paired
finalizer，原子生成：

```text
input-manifest.json
td-b-combined-analysis.json
EXPERIMENT_SUMMARY.md
independent-final-zero.json
```

Finalizer只汇总两源各自 public analysis、input hashes、setup/physical counts、wrapper/cleanup和最终 zero；
不得重新拟合、不改变单源状态、不生成新的 operating envelope、不解锁 TD-C。

Executor 在 `.agent-work/EXECUTION_RESULT.md` 写入：

- E0X commit/hash、测试计数、logs和validation artifact hashes；
- preflight、setup、Ray、strip、paired目录和全部关键 hashes；
- PID/TTY/exit、capture/formal/setup/physical/NPY counters；
- 每源 analyzer status、history/nonstationarity指标；
- Python/shell/recovery/final zero结果；
- 实际分支和唯一 Planner决策请求。

不得修改、追加、归档或重命名本文件。

## 9. 硬锁

本工作包禁止：

- 900/1200 秒扩展或把 600 秒称为 settled；
- TD-C core/expansion；
- 四点 sentinel、remaining 9、boundary、holdout、Gate-6、P8；
- P6 7点 requalification、13点或106点重拍；
- firmware、remote deployment、默认 LUT/runtime config安装；
- 修改 uncertainty/covariance/feature/threshold来让本 run通过；
- 把 setup failure或 history failure写成 physical gamut/unreachable；
- 覆盖或删除失败 run、旧 evidence或默认配置。

完成本计划不自动授权任何下一阶段。Planner验收时必须先归档本计划，再根据 TD-B证据决定是否回
Advisor、设计补充诊断或继续下一阶段。

---

## 10. Planner Review Addendum (2026-07-22T06:28:34-0600)

### 10.1 Reviewed scope and implementation quality

This archive preserves the exact active plan reviewed at SHA-256:

```text
20e09f24611f2350982034cb9ee83bbb66074553512f0a4d60ecc005172c2d31
```

Reviewed implementation checkpoints:

```text
87f1e3244fa0f2a597780a7b0bacb98632c76774  feat(p7): close TD-B production orchestration
e025b38                                      docs(p7): record TD-B setup gate failure
```

E0X is accepted as code-complete. Its method keeps the existing thermal runner as the single production owner,
adds retained remote-v2 setup attempts, post-wrapper canonical finalization, resolved-plan resume, source
isolation, exact checkpoint binding, and a paired finalizer without creating a parallel acquisition framework.

Validation quality accepted by Planner:

```text
focused: 159/159 pass
full suite: 529/529 pass
post-checkpoint production round-trip: 4/4 pass
compileall: pass
all repository tmp/*.zsh syntax: pass
git diff --check: pass
CodeGraph sync: pass
frozen inputs: 5/5 exact hash match
```

Accepted E0X evidence root:

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-production-offline/20260722-090000
validation-summary.json = 381387f6430cd811fef186662799079f6785dd67b14c31adf7b76f477dd679c2
readiness.json          = 8b853f38a09d6a87c235d137e4106f8860e6c15d59b19b9969ccbf5cd3048655
```

### 10.2 Real setup failure review

The retained setup attempt is a valid fail-closed launcher/input-gate failure, not a scientific acquisition
failure and not evidence that the target state is unreachable:

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-073500
failure = TD-B setup frozen input references differ before device access
child_exit_code = 1
shell_cleanup_exit_code = 0
wrapper_exit_code = 1
nonzero source commands = 0
camera requests = 0
CR3 = 0
NPY = 0
formal acquisition = 0
```

Planner independently verified that the relative path
`config/hsi/p7-operating-envelope-v2.json` and the expected absolute path resolve to the same regular repository
file with SHA-256 `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16`.
The production gate compared raw path strings because `file_reference()` preserves the caller spelling. The
other frozen references matched. This is a producer/validator canonical-path ownership defect.

Safety evidence accepted:

```text
wrapper-result.json             aa5eff6ebe4b39857295a701fce2c35f7760de02f159eab09c7c278e8e57ddc0
wrapper-observed-exit.json       619f3474175013d83ad888cd36fc1908891d80603326ba16371da8af17cb610c
all-off-shell.json               388736d378cfa69da8846d8b48f75d476055f9af1a2b95fffd18fa8ac85e8de1
independent-recovery-zero.json   29b08bd449b80ad8392f280253a7098fa15b5a0ae9ff5689bec68f023965683e
```

The independent recovery confirms strip generation `2 -> 3`, all five strip channels zero, stable device/MAC,
and Ray intensity zero. No residual production process remained.

### 10.3 Planner decision

```text
E0X implementation = accepted
real setup run = valid fail-closed, no measurement evidence produced
root cause = local path canonicalization defect
Advisor escalation = not required
same-hash arbitrary-file substitution = prohibited
zero-output cleanup commands = safety actions, not setup capture consumption
previous failed run = immutable; never reused or overwritten
one fresh setup retry after offline correction = authorized
setup success = continue the already bounded Ray -> strip TD-B package without an ordinary Planner stop
```

The correction must canonicalize the requested prerequisite to the exact trusted repository artifact before
comparison, retain its SHA-256, and keep owner/root/type checks. It must not accept a different file merely because
its bytes have the same hash. Missing paths, directories, symlinks, path escape, same-content copies, wrong hashes,
and producer/analyzer disagreement remain fail closed before backend construction or any device side effect.

### 10.4 Residual risks and exact next branch

- A global change to `file_reference()` could alter historical schemas; the correction must be scoped or versioned
  and prove legacy replay compatibility.
- The first setup attempt never reached device preflight, so remote-v2, Ray H120/S50 setup, cold proxy, and both
  16-frame formal runs remain unverified on hardware.
- The 600-second dwell remains a Developer/Human time-limit decision and is not scientific settling evidence.
- TD-C, sentinel, boundary, holdout, Gate-6, P8, firmware, deployment, and default LUT installation stay locked.

Exact next branch:

```text
P7-TD-B-PATH-R1
  -> offline canonical-path correction and adversarial replay
  -> focused/full/checkpoint gate
  -> one fresh setup retry
  -> if valid, continuous Ray formal -> strip formal -> paired finalization -> Planner stop
  -> on any hard failure, cleanup/recovery evidence -> Planner stop
```
