# P7-TD-B-PATH-R1+RETRY：规范化 prerequisite 身份并恢复连续 TD-B

**计划状态：** `offline_path_fix_then_single_fresh_setup_retry_authorized`

**Planner 日期：** `2026-07-22T06:28:34-0600`

**当前阶段：** `P7_TD_B_PREREQUISITE_IDENTITY_CORRECTION_AND_BOUNDED_EXECUTION`

**当前唯一动作：** Executor 在现有 P7 thermal owner 内完成 prerequisite canonical-path 离线纠偏、
对抗性回归和新代码 checkpoint；全部离线门通过后，使用全新目录重试一次 Ray H120/S50 setup。Setup
结构合法后不设普通 Planner 停点，继续完成 Ray TD-B、strip TD-B、两份 public analysis、paired finalizer
和独立双源 zero readback。

**唯一 Planner 停止点：** 完成上述整包并交回结果；或者任何离线门、preflight、setup、formal、证据、
预算、source isolation、cleanup 或 finalization hard failure 后，保留证据、确认双灯关闭并立即停止。禁止
进入 TD-C 或任何后续阶段。

## 1. 上轮验收和归档

已完成/已审部分全部归档，不得重新展开到 active PLAN：

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260722-0628-p7-td-b-e0x-setup-path-failure-review.md` | `f95d41a3a8bf9705b4ea51ae71164b7783da86b1b61b65665a5d3fbb5ecf87dc` |

Planner 决定：

```text
E0X production orchestration = accepted
implementation checkpoint = 87f1e3244fa0f2a597780a7b0bacb98632c76774
failed run = valid fail-closed before device preflight
root cause = relative/absolute path spelling compared as raw strings
scientific captures produced = 0
Advisor escalation = not required
one fresh setup retry after correction = authorized
```

旧失败目录必须永久保留且不得改写：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-073500
```

Shell cleanup 和独立 recovery 的全零 command 是安全动作，不计入 setup capture 或科学实验消费。本计划
明确批准一次新的 setup run；这不是 Executor 自行扩大自动重试规则。

## 2. 权限、科学语义和硬边界

### 2.1 设备权限

本项目 `AGENTS.md` 已冻结：在 active PLAN 边界内开关 Ray120c/RGBWW 灯带不需要另行人工批准。
此前 Human 对 exact named experiment 的放行在没有 camera request、CR3 或非零实验 command 前未被消费；
Executor 可直接执行本计划，不得再次询问同一开灯/相机包的授权。

唯一 named experiment：

```text
p7_td_b_command_switch_history_v1
```

允许：脚本内读取 `.env`、remote health/config/v2 capture、计划内 Ray/strip command、双层 `all_off`。
禁止人工读取/打印 `.env`，禁止 firmware compile/upload、remote deployment、依赖安装、破坏性硬件操作。

### 2.2 600 秒语义

600 秒仅是 Developer/Human 选择的 operational dwell，不是 Planner 推断的 steady-state：

```text
decision_owner = Developer/Human
thermal_extension_900_1200 = rejected
developer_selected_operational_dwell_s = 600
Ray TD-A = settling_not_demonstrated_by_600
strip TD-A = settling_not_demonstrated_by_600
t_settle_ray_s = null
t_settle_strip_s = null
t_formal_provisional_s = null
t_formal_s = null
```

不得输出 `settled_at_600`、`steady` 或自动写 `td_b_pass`。结构合法的科学状态只允许：

```text
td_b_operational_600_complete_waiting_for_planner
history_dependent_at_operational_dwell_600
```

可附 structured nonstationarity warning，但不得修改 trend、single-frame dominance、58-feature、covariance、
joint coverage、P6 topology、默认 LUT/runtime config、TD-A retained evidence 或 v1 envelope。

## 3. 必读输入和冻结身份

Executor 开始前必须阅读：

1. 本文件全文；
2. `.agent-work/PLANS/20260722-0628-p7-td-b-e0x-setup-path-failure-review.md` 的第 10 节；
3. `.agent-work/EXECUTION_RESULT.md` 的第 25 节；
4. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
5. `docs/README.md` 的 P7 thermal/timing/setup/cleanup 章节；
6. `config/hsi/p7-operating-envelope-v2.json`；
7. 当前 CodeGraph 和 `git status --short --branch`。

冻结输入：

| 输入 | SHA-256 |
| --- | --- |
| `config/hsi/p7-operating-envelope-v2.json` | `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16` |
| `config/location/locations-20260714-211759.json` | `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| `config/hsi/strip-hsi-policy-v2-waiting.json` | `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| `config/hsi/ray-hsi-manifold.json` | `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| `config/channel/code-duty-curve.json` | `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |
| E0X checkpoint | `87f1e3244fa0f2a597780a7b0bacb98632c76774` |
| E0X validation summary | `381387f6430cd811fef186662799079f6785dd67b14c31adf7b76f477dd679c2` |

受信 prerequisite 的唯一身份：

```text
project-relative = config/hsi/p7-operating-envelope-v2.json
canonical absolute = /Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-operating-envelope-v2.json
sha256 = 7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
type = regular file, not symlink
owner root = /Users/ibobby/Projects/WLED-RGBWW
```

除下一节允许的 code/tests/docs/skill 纠偏外，任何冻结实验输入漂移都必须在 backend 构造、output owner、
设备连接或 command 前停止。

## 4. PATH-R1 离线纠偏

### 4.1 单一 owner 和最小修复

在 `optimization.p7_thermal_diagnostics` 现有边界增加一个窄的 trusted-prerequisite resolver，并由 plan
producer、production setup validator 和 public analyzer/replay 共同使用。不得建立第二套 plan builder、
runner 或 analyzer。

Resolver 必须：

1. 将相对输入固定相对于仓库 `PROJECT_ROOT` 解析，不依赖调用进程的 cwd；
2. 允许项目相对 canonical spelling和上述 exact canonical absolute path；`./` 规范化后可接受；
3. 在读取 JSON 前拒绝 `..` path traversal、项目根外路径、缺失路径、目录和 symlink；
4. 解析结果必须与 frozen expected artifact 是同一个 exact canonical repository path；
5. 之后再校验 regular file 和冻结 SHA-256；
6. 计划内 `inputs.operating_envelope.path` 统一保存 canonical absolute path；
7. `inputs.operating_envelope.sha256` 保持冻结 hash；
8. 同内容 copy 即使 SHA-256 相同也必须因为 canonical owner/path不同而拒绝；
9. 所有拒绝发生在 backend construction、output directory creation、device/all_off/camera调用之前。

保持现有 `file_reference()` 的通用/历史行为不变；不要为了一个 CLI prerequisite 全局改写旧 artifact 的
path schema。若实现发现必须修改全局 `file_reference()` 才能完成，停止并交 Planner，不自行扩大范围。

不增加新 plan schema；只让现有 `p7_thermal_diagnostic_plan_v2` 的 operating-envelope reference 使用统一
canonical representation。Legacy v1、TD-A、R0/R0S/E0X retained replay不得变化。

### 4.2 必须覆盖的测试

至少新增并验证：

1. project-relative path 与 exact absolute path生成完全相同的 canonical operating-envelope reference；
2. 从非仓库 cwd 调用 producer时，相对 path仍以 `PROJECT_ROOT` 为 owner；
3. `./config/...` 合法；包含 `..`、项目根外路径、missing、directory均拒绝；
4. 指向受信文件的 symlink拒绝；同 hash copy拒绝；错误 hash/错误 config拒绝；
5. production setup fake CLI使用相对 path通过 frozen-input gate，并保留 0 device/network副作用；
6. production setup fake CLI使用 absolute path得到同一 plan/replay；
7. tampered plan path、hash或 owner在 backend construction和 output owner前拒绝；
8. public analyzer独立重放 canonical reference并拒绝 path/hash分裂；
9. TD-A v1/v2、TD-B R0/R0S/E0X、remote-v2 parser和wrapper分支保持兼容；
10. 失败测试不得产生真实 `.env`、network、camera、Ray、ESPHome、`all_off` 或 CR3。

不要只断言 helper 返回值；至少一组测试必须走：

```text
production CLI plan build
-> run_td_b_setup_provisional frozen-input gate
-> fake backend boundary
-> retained/public replay
```

### 4.3 离线验证、证据和 checkpoint

离线根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/<timestamp>/
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
for wrapper in tmp/*.zsh; do zsh -n "$wrapper"; done
git diff --check
codegraph sync
```

保存 focused/full logs、relative/absolute canonical plans、negative-case matrix、fake production round-trip、
`validation-summary.json` 和全部 SHA-256。通过后更新相关 docs/skill并创建 focused conventional commit。

提交后再次验证：

- `git rev-parse HEAD` 为新的 full 40-char code checkpoint；
- production `src/tests/docs/.agents/skills/tmp/run-p7-thermal-diagnostics.zsh` 相对 HEAD干净；
- 五个冻结 input hash不变；
- relative production fake round-trip在 checkpoint后仍通过；
- 未访问设备、网络、`.env` 或 `all_off`。

任一离线项失败：记录到 `EXECUTION_RESULT.md`，不得进入设备步骤，交 Planner。

## 5. 单次新 setup 和连续 TD-B

### 5.1 运行所有权与重试限制

离线门全通过后才能创建新 run。必须使用全新 timestamp/目录，绝不复用旧失败目录。Setup CLI应继续
传入项目相对 prerequisite path，以覆盖真实生产路径；artifact中必须出现 canonical absolute reference。

本计划只有一次新的 setup 权限。若新 setup任一点失败，即使仍为 0 capture，也不得自行做第二次 setup
重跑；完成 cleanup/recovery并交 Planner。

所有实机子 run只能通过已测试的 `tmp/run-p7-thermal-diagnostics.zsh` / production orchestrator启动。每个
run保存 PID/PPID/PGID/TTY、runner/wrapper log、start time、child/shell/signal/final exit和 owner路径。

### 5.2 顺序和总预算

严格串行：

```text
fresh preflight
-> Ray H120/S50 setup, 1..8 physical CR3
-> both off + verified zero + complete 1800 s cold proxy
-> canonical setup/release/resolved plan
-> Ray TD-B formal, exactly 16 CR3
-> Ray public analysis
-> strip TD-B formal, exactly 16 CR3
-> strip public analysis
-> paired finalizer/manifest
-> independent final both-off/readback
-> Planner stop
```

| Package | Formal | Setup | Ambient | Physical |
| --- | ---: | ---: | ---: | ---: |
| Ray | 16 | 1..8 | 0 | 17..24 |
| strip | 16 | 0 | 0 | 16 |
| combined | 32 | 1..8 | 0 | 33..40 |

第 9 张 setup capture必须在相机请求前拒绝。Setup图只属于 exposure ledger，不得进入 formal 58-feature、
repeatability、history aggregate或 covariance。

### 5.3 Fresh preflight

脚本自行加载 `.env`。在非零 command前验证：

- 无无法证明 ownership 的 camera/calibration/thermal process；
- 新 checkpoint、wrapper和冻结 input hash一致；
- `control.all_off`成功，Ray independent readback intensity 0；
- strip `bedroom-rgbww-strip` identity/MAC稳定、generation-bearing五通道全零；
- remote health、authenticated config、formal v2 capability、RAW、ISO 100、非空 aperture；
- Ray node config、HSI/CCT set/readback可用；
- location仍为 `locations-20260714-211759.json`；
- 新 run/log/wrapper-state路径不存在且不经 symlink。

Preflight失败：保留 evidence，执行 Python/shell cleanup和独立 zero，停止。

### 5.4 Setup exact contract

```text
Ray = H120/S50/INT100
strip = cw/ww/r/g/b all zero
historical shutter seed = 1/6400, seed_only
target_max = 19661
accepted_min ratio = existing auto-exposure 0.85
min shutter = 1/16000
max shutter = 25
max physical CR3 = 8
adapter = retained remote-v2 only
```

每张 trial/rejected-final/selected-final CR3和sidecar均保留；记录 ID、hash、byte count、recorded exposure、
shutter、timing tier/method；`.npy=0`。Setup结束立即双关灯、独立 zero readback，再完整等待 1800 秒。
只有 child、Python/shell cleanup、wrapper observed exit、final zero、canonical setup、resolved plan和release全部
可独立重放时才能进入 Ray formal。

### 5.5 Ray formal

```text
A = H120/S100/INT100, shutter 1/5000
D = H120/S50/INT100, shutter only from canonical setup
B = H0/S0/INT100, shutter 1/8000
C = H300/S100/INT100, shutter 1/2000
```

Chronology恰好 16 张：

```text
A0 at 600
D at 60/120/300/600
A return at 600
B at 60/120/300/600
A return at 600
C at 60/120/300/600
A return at 600
```

每个 group只发送一次 command并精确 readback，持续到该组最后 capture；transition先双关灯/读回再打开
新状态。只有 Ray亮，strip始终 verified zero。Formal不得 auto-expose。

Ray acquisition只要 capture/timing/owner/source-isolation/ledger/cleanup结构合法，就运行 public analyzer；即使
科学状态是 history-dependent/nonstationarity warning也继续 strip。Hard-invalid、measurement failure或
cleanup uncertainty则停止。

### 5.6 Strip formal

```text
A: cw=518,  ww=0,    r=0,    g=4095, b=0;    shutter=1/320
D: cw=4095, ww=0,    r=0,    g=3118, b=13;   shutter=1/400
B: cw=4095, ww=4095, r=0,    g=1887, b=1535; shutter=1/500
C: cw=406,  ww=0,    r=4095, g=0,    b=1541; shutter=1/125
```

Chronology与 Ray相同，恰好 16 张。只有 strip亮，Ray intensity始终独立读回 0；每次 transition记录
generation、identity、requested raw command和readback。Formal不得 auto-expose。

### 5.7 Timing、证据、观察和 cleanup

- nominal `60/120/300/600` 只用于调度/分组；
- 只接受 Tier A/B finite/nonnegative observed elapsed，不做 proximity gate；
- 保留 gphoto2 method，`absolute_exposure_start=false`；
- command group内 chronology严格递增；
- 每 run只解析一次 camera settings并注入全部 capture；
- 每张 CR3非空且 recorded exposure、sidecar、hash、byte count、capture/request ID可重放；
- 所有测试和正式 run均不得保留 `.npy`。

长 run启动后只做一次约 3 分钟健康检查；随后使用当前 task的稀疏一次性 heartbeat按 ETA恢复，不短间隔
轮询，不因结束回答终止进程。

每个 run都要求 Python `finally` 和 shell EXIT/INT/TERM/HUP trap独立关两灯并保存真实退出状态；完成后再
取得 strip generation-bearing zero与 Ray intensity 0。缺任一 cleanup证据立即执行独立 recovery并停止。

## 6. 分支和交接

允许继续：

```text
PATH-R1 offline all pass -> focused commit/post-checkpoint pass -> fresh setup
fresh setup canonical pass + full cold proxy -> Ray formal
Ray structurally valid -> public analysis -> strip formal
strip structurally valid -> public analysis -> paired finalizer -> final zero -> Planner stop
```

必须停止：

```text
offline correction/test/checkpoint failure -> zero device access -> Planner
preflight failure -> cleanup/recovery -> Planner
setup invalid/unreachable/over-budget/evidence or canonicalization failure -> preserve artifacts -> Planner
Ray hard-invalid or cleanup uncertainty -> no strip -> Planner
strip hard-invalid or cleanup uncertainty -> no paired scientific claim -> Planner
paired/final-zero failure -> preserve source analyses, no next-stage claim -> Planner
```

`paired finalizer` 只能汇总两个 public analysis、input/setup/physical ledger、wrapper/cleanup和 independent
final zero，原子生成：

```text
input-manifest.json
td-b-combined-analysis.json
EXPERIMENT_SUMMARY.md
independent-final-zero.json
```

不得重新拟合、改变单源状态、生成新 operating envelope或解锁后续阶段。

Executor 只把进度、checks、commit、artifact/hash、PID/exit、counts、analysis status、cleanup和实际分支写入
`.agent-work/EXECUTION_RESULT.md`；不得修改、追加、归档或重命名本文件。

## 7. 硬锁

本包不允许：

- 第二次 setup重试；
- 900/1200 秒扩展或把 600 秒称为 settled；
- TD-C core/expansion；
- sentinel、remaining 9、boundary、holdout、Gate-6、P8；
- P6 requalification或重拍；
- firmware、remote deployment、默认 LUT/runtime安装；
- 修改 uncertainty/covariance/feature/threshold以让结果通过；
- 把 setup/history failure升级为 physical gamut或 physically unreachable；
- 覆盖/删除失败 run或旧 evidence。

完成本计划不自动授权任何下一阶段。Planner复验时必须先归档本计划，再写唯一下一工作包。
