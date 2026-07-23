# P7 归档：TD-A Ray 首帧 Timing Hard-Invalid

**归档日期：** `2026-07-21`

**原活动计划 SHA-256：**
`f3df0e06b45de7fa254cae7e3313f17e85afc30ae01dfae94e93f01291a42ff0`

**Planner 决定：** `valid_failure_accept_and_branch_to_offline_timing_v2`

## 0. Planner 验收补记

本归档完整保留已审查的 TD-A 实机执行合同、方法、安全边界和停止分支。Executor 严格消费了
Human 的一次 exact `p7_td_a_cold_settling_v1` 授权：首次成功非零 Ray command 已发生，随后首次
`t60` capture 因旧合同要求 best-effort exposure-start 与 nominal slot 的误差不超过 `+/-2 s` 而
fail closed。strip 未启动、Ray 未重跑、旧 run 未复用。

Planner 独立核验以下事实：

- run 为 `failed`，`0 formal / 1 ambient / run ledger 1 physical`；磁盘保留 ambient 与失败 t60
  两张非空 CR3，零 NPY；
- failed t60 为 Tier B `accepted_best_effort_anchor`，nominal `60.0 s`，best-effort observed elapsed
  `64.40580299403518 s`，offset `+4.40580299403518 s`；
- `plan.json`、`run.json`、`failure.json`、Python cleanup、shell cleanup、wrapper result 与 independent
  recovery 的 SHA-256 均与 Executor 交接一致；
- Python/shell cleanup 均成功；independent recovery 证明 strip generation `4 -> 5` 后五通道全零，
  Ray readback intensity 为 `0`；
- wrapper、child 和 heartbeat 均已退出，不存在残留 calibration process；
- 失败原因是旧 nominal-proximity acceptance contract，不是 CR3、remote-v2 sidecar、recorded
  exposure、source isolation、readback 或 cleanup 损坏。

Human/Developer 在本次 Planner 门明确作出新的 timing 决定：gphoto2 只能提供最佳估计，无法真正
控制或证明绝对 exposure-start；后续只记录并在计算中使用该 best-effort observed elapsed，不再以
类似 `+/-2 s` 的 nominal deviation 作为接受/拒绝条件。该决定属于 Human/Developer，不是 Planner
擅自放宽实验门槛，也不允许把 Tier C、缺失、非有限、负值、sidecar/replay 不一致或 chronology
错误作为有效 timing。

### 验收证据

| 证据 | 路径 / SHA-256 |
| --- | --- |
| Executor 交接 | `.agent-work/EXECUTION_RESULT.md` 第 16 节 |
| Ray run | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-150200` |
| plan | `plan.json` / `ebbe657c4b9b11b2dee0f93dd9d38d8fbeffc9d577e3dfc30675677153943c88` |
| run | `run.json` / `e15c7834c036f12df8c9a819f7d3ce33beda17323c88162f2928e4fe7f17a04f` |
| failure | `failure.json` / `a002378287807d353849048eabd40eace1a38ef25aba107d9838751358b81a91` |
| Python cleanup | `all-off-python.json` / `cf9c45b3cc3d7c4a89f61653b5c57876020c4e87aab90ecfe365d09f8c35a1f4` |
| shell cleanup | `all-off-shell.json` / `86ff1100dcb07dc5579079f6a7d22b81711e4655983e96b90d73df21c4a96427` |
| wrapper result | `wrapper-result.json` / `461e9f288859658da2d7571716673858c6bf6fb119ea76f3270a80344fe620a1` |
| failed t60 CR3 | `camera/001-ray-a-t60-*.cr3` / `2c44295d5d949ef6f0b652b596173d2c177bb115e64f87efa061dc383b2c303c` |
| failed t60 sidecar | `camera/001-ray-a-t60-*.cr3.metadata.json` / `168d7cf616d5f95d3ef4851c1288370fcb5beec3040b54663fb481592c488fef` |
| independent recovery | `recovery-all-off.json` / `7271ef39a4e245a58c280bb425fb0b96e50225662b5a17349aaa18ef2f1a8cb5` |

### 质量、残余风险与下一分支

- 采集和安全证据质量足以接受为正式 valid-failure；本 run 不可续跑、补写或升级为 complete。
- 旧 `best_effort_gphoto2_v1` artifacts 必须保持只读可审计，不得原地改写为新合同。
- best-effort observed elapsed 仍不是绝对曝光起点；新分析必须保留该限制，并报告 timing tier、
  method、offset 和分布。
- 只有 evidence integrity、Tier A/B、有限非负 elapsed、独立 sidecar replay 和 cycle chronology
  可以作为 timing hard gate；nominal proximity 不再是 hard gate。
- 下一唯一分支是纯离线 `P7-TD-A-T0` timing v2 纠偏。原 Human 授权已经消费；离线验收通过也
  不会自动授权新的实拍，后续必须由 Human 对新的 exact TD-A run 另行授权。

---

## 原活动计划全文

**计划状态：** `active`

**Planner 日期：** `2026-07-21`

**当前阶段：** `P7_TD_A_COLD_SETTLING_EXECUTION`

**当前状态：** `authorized_ready_for_single_execution_package`

**当前唯一动作：** 使用已验收的 production runner/wrapper，按 `ray_then_strip` 顺序完成一次 exact
TD-A 双源采集、单源分析和 paired finalization，然后停止交还 Planner。

**唯一 Planner 停止点：** 任一 hard-invalid/安全停止分支，或两个 source 均完成并生成 combined
analysis、summary、manifest 和最终双灯 zero evidence。

**禁止自动进入：** TD-B、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6、P8、默认
LUT/runtime 安装、firmware 或 remote deployment。

---

## 1. Planner 验收结论与归档

W0 已通过 Planner 验收。production wrapper 六条真实 zsh runtime 路径、paired input manifest、独立
replay、tamper/atomic contracts 和完整 workspace tests 均通过，没有未解决的 Must Fix 或 Should Fix。

本轮归档：

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260721-0009-p7-td-a-w0.md` | `fa2787098f864d60383b759e90321af45cef120f81d7265558881ae0ce6c84a6` |

历史归档保持不变。需要追溯时重点读取：

```text
.agent-work/PLANS/20260720-0046.md
.agent-work/PLANS/20260720-1300-p7-td-a-r0d.md
.agent-work/PLANS/20260720-2236-p7-td-a-e0-ray-wrapper-failure.md
.agent-work/PLANS/20260721-0009-p7-td-a-w0.md
```

## 2. Executor 所有权与必读顺序

Executor 开始前必须依次读取：

1. 本文件全文；
2. `AGENTS.md`；
3. `.agent-work/PLAN/00-CONTRACT.md`；
4. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
5. 第 1 节四份归档；
6. `.agent-work/EXECUTION_RESULT.md` 第 13 至 15 节；
7. `.agent-work/debug/resolved/20260720-p7-td-a-wrapper-runtime.md`；
8. `advisor/3/1.GUIDE.md` 的 TD-A 与 operating-envelope 决策；
9. `docs/README.md` 的 remote v2 timing、source isolation、recorded exposure、thermal diagnostics 和
   cleanup；
10. 使用 CodeGraph 定位 thermal plan/runner/analyzer、remote backend、verified strip readback、Ray
    readback、all-off 和 wrapper owner；
11. `git status --short --branch`，保留全部现有用户与 Planner 改动。

所有权：

- `.agent-work/PLAN.md` 由 Planner 独占，Executor 只读；
- 执行进展、证据、失败和 Planner 决策请求只写 `.agent-work/EXECUTION_RESULT.md`；
- 不得修改、追加、归档或重命名 PLAN；
- 不得修改第 1 节归档；
- 不得把 Planner/用户未提交文件混入执行证据 commit；
- 真实采集只能使用现有 `tmp/run-p7-thermal-diagnostics.zsh` 和现有 production module；不得创建
  平行 runner、wrapper、capture path 或 analyzer；
- `.env` 只允许正式 Python remote backend 自行加载，不得人工读取、source、打印或持久化 secret。

## 3. Human 授权恢复与消费边界

Human 于 `2026-07-20T16:04:40Z` 给出的 exact 一次性授权此前没有被消费。Planner 已冻结：

```text
acquisition_authorization_consumption_boundary
= first_successful_nonzero_source_command
```

旧失败 run 为 `0 command / 0 capture / 0 CR3`，因此 W0 验收后恢复原授权。Executor 可以直接消费，
不得再次询问同一范围。

授权范围：

```text
authorization_owner = Human
experiment_id = p7_td_a_cold_settling_v1
execution_package_count = one
sources = ray, strip as two independent runs
source_order = ray_then_strip
state = H120/S100/INT100 equivalent
cycles_per_source = 3
timed_points_s = 60,120,300,600
formal_cap = 12 per source / 24 total
ambient_cap = 3 per source / 6 total
physical_cap = 22 per source / 44 total
maximum_continuous_on = 600 s formal exposure-start target per cycle
maximum_commanded_on = 1800 s formal target per source
cold_proxy_off_s = 1800 before each cycle when uninstrumented
timing_contract = best_effort_gphoto2_v1
remote_timeout_s = 120
new_run_directories = required
```

允许的设备操作：

- remote `/health`、`/v1/config`、v2 capability/settings 和计划内 captures；
- Ray exact `H=120,S=100,INT=100`、off、readback 和 cleanup；
- strip exact参数顺序 `cw,ww,r,g,b` 的 `518,0,0,4095,0`、zero、generation-bearing readback 和
  cleanup；
- Python finally、shell trap、失败 recovery 和 combined 完成后的独立 final all-off/readback；
- 正式脚本内部读取 `.env`，但不得输出 secret。

不授权：

- 额外曝光试拍或 auto-exposure；
- 其他 Hue/SAT/INT、其他 strip command 或额外 source；
- 自动 experiment/source retry、第二套 TD-A 或复用旧目录；
- 扩大 timed points、cycle、亮度、capture cap 或 recovery 范围；
- TD-B/C、sentinel、boundary、holdout、P8、firmware、remote deployment 或默认配置安装。

授权在首次成功非零 source command 后视为已消费。之后即使 run hard-invalid，也不得自动再开第二个
Ray 或 strip run；必须停止交还 Planner/Human。

## 4. 冻结代码与输入

### 4.1 代码 checkpoint

任何设备或网络访问前必须证明以下 Git objects 存在且当前工作树中的相关 production files 与冻结
checkpoint 一致：

```text
R0D settings owner
3cbc72a9d9500a61e21a793e0f1787d4bdba340c

E0 completion owner
d5cc596521f938c4f353a7d7a498f6f7be6453f8

W0 implementation/code checkpoint
960484e1107cbcfb3304075a5ac54a0fbe6a382e

W0 evidence
1c592c93a681269ec9f7ce566903153a5db5cc6a
```

必须执行等价于：

```zsh
git cat-file -e 3cbc72a9d9500a61e21a793e0f1787d4bdba340c^{commit}
git cat-file -e d5cc596521f938c4f353a7d7a498f6f7be6453f8^{commit}
git cat-file -e 960484e1107cbcfb3304075a5ac54a0fbe6a382e^{commit}
git cat-file -e 1c592c93a681269ec9f7ce566903153a5db5cc6a^{commit}
```

Production wrapper 必须为：

```text
tmp/run-p7-thermal-diagnostics.zsh
sha256 = 4f776135b18df57897011d6c37f7683768d772cd5a9ee7f73c07f2ffae0d7dfb
```

Paired finalizer 的 `--code-checkpoint` 必须传：

```text
960484e1107cbcfb3304075a5ac54a0fbe6a382e
```

不得使用 HEAD、docs commit、任意短 hash 或 hand-written hash-like 字符串替代。

### 4.2 冻结实验输入

| 输入 | 路径 / SHA-256 |
| --- | --- |
| Advisor GUIDE | `advisor/3/1.GUIDE.md` / `92f766da523c40ff49c228c996dffd6d3839552f70bbd79aa7627485dd749be1` |
| Advisor RESEARCH | `advisor/3/1.RESEARCH.md` / `1fac3ed986b393aa3467722e3ee06ab240e6df1b64c4146741072bcae2f91a9c` |
| Location | `config/location/locations-20260714-211759.json` / `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| Ray manifold | `config/hsi/ray-hsi-manifold.json` / `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| Operating envelope | `config/hsi/p7-operating-envelope-v1.json` / `d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25` |
| P7 policy/feature file | `config/hsi/strip-hsi-policy-v2-waiting.json` / `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| P7 uncertainty | `config/hsi/strip-hsi-uncertainty.json` / `cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94` |
| RAW observer | `config/camera/raw-observer.json` / `b81d563eba1910286d879e560538dd497385e422c1bab762008c2b28a26fc4d9` |
| Code-duty curve | `config/channel/code-duty-curve.json` / `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |
| R1 commands | retained `commands.jsonl` / `2d0667d235bffff9119eea54e76d76ed1914f246fec64903f2dd1a9b675b4ca3` |
| R1 plan | retained `plan.json` / `55c25a4b51d4a247e1888f3d6a075dea313f3dadc3e5e8435e53c419131a1c2e` |

R1 retained root：

```text
/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/
  p7-r1-20260719-091000-terminal-retry1
```

W0 validation：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/
  p7-td-a-w0-20260721-054106/validation-summary.json
sha256 = 94ce883c689fed4dc43f1ce1db0396fe41f11846d167604fa9cc8a6c017647af
```

Operating-envelope 的以下字段必须仍为 null：

```text
t_settle_ray_s
t_settle_strip_s
t_formal_provisional_s
t_formal_s
```

继续冻结 identity RAW、`R/G1/G2/B`、58-feature、joint 99.73% coverage、trend `4.0`、
single-frame dominance `0.5`、P6 `full_periodic_2d_HB`、SAT0 Hue undefined、HSI/RGB endpoint 分离、
INT100 full-scale policy 和 `absolute_exposure_start=false`。

## 5. 实机前离线进入门

在任何设备、网络或 `.env` 调用前，创建新的 entry evidence directory，并完成：

1. 第 4 节全部 commit、path 和 SHA-256 验证；
2. 确认 production wrapper hash 精确匹配；
3. 确认 operating-envelope 四个 settle 字段仍为 null；
4. 确认旧失败目录
   `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-040137`
   只读保留，不复用、不改写；
5. 确认没有其他 calibration、gphoto2、camera、Ray、ESPHome 或 thermal wrapper process；无法证明
   ownership 时 fail closed；
6. 生成全新 Ray 和 strip dry plans；
7. 每个 plan 必须为 exact TD-A、3 cycles、`60/120/300/600`、12 formal、3 ambient、physical cap
   22、cold proxy 1800；
8. Ray shutter ledger 必须恰好为 `ray-h120-s100=1/5000`；
9. strip shutter ledger 必须恰好为 `strip-h120-s100-fullscale=1/320`；
10. 两者 `exposure_setup_required=[]`，timed cycle `auto_exposure=false`，不得出现
    `ray-h120-s50`；
11. 冻结两个全新且互不相同、当前不存在的实际 run paths 和一个 combined output path；
12. 运行 focused thermal tests、`zsh -n tmp/run-p7-thermal-diagnostics.zsh`、`git diff --check`；
13. 保存 entry summary、dry-plan paths/hashes、当前 PID audit、代码 checkpoint、source order 和计划
    SHA-256。

推荐根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-entry-<UTC timestamp>/
  p7-td-a-ray-<UTC timestamp>/
  p7-td-a-strip-<UTC timestamp>/
  p7-td-a-combined-<UTC timestamp>/
```

任一项失败：保持零设备，写 `TD-A-OFFLINE-ENTRY-FAIL`，停止交还 Planner。

## 6. 实机 Preflight

离线进入门通过后，按顺序：

1. 正式 remote Python path 自行加载 `.env`；
2. remote `/health` 和 `/v1/config` 通过，v2 capability 必须为冻结正式 capability；
3. 使用同一 `RemoteCameraBackend` 解析一次非空 ISO、aperture 和 `RAW`；不得 capture；
4. 检查 Ray node/config 与当前 readback；
5. 调用共享 `all_off`；
6. 独立确认 Ray intensity `0`；
7. 使用 generation-bearing ESPHome snapshot 确认 device identity 为 `bedroom-rgbww-strip`、五通道全
   零且 generation 前进；
8. 不发送非零 probe，不执行 auto-exposure，不拍摄 CR3；
9. 保存 preflight、Python cleanup、shell cleanup、independent zero readback、run paths、launcher paths
   和全部 input hashes。

Preflight 失败：执行 Python 和 shell recovery all-off，独立确认两灯关闭，保存失败证据，分支
`TD-A-PREFLIGHT-FAIL`，不得启动 Ray run。

## 7. Ray Source Run

### 7.1 启动

使用全新 Ray run directory，通过 OS-owned Terminal/background task 启动唯一 production wrapper：

```zsh
tmp/run-p7-thermal-diagnostics.zsh "$RAY_RUN_DIR" \
  --experiment-id p7_td_a_cold_settling_v1 \
  --source ray \
  --human-authorization p7_td_a_cold_settling_v1 \
  --camera-backend remote \
  --remote-timeout 120
```

保存：Terminal window/tab、TTY、wrapper PID/PPID/PGID、child PID、start time、runner log、wrapper log
和 wrapper-state path。启动后只做一次约 3 分钟健康检查，确认：

- process 脱离当前 agent command；
- wrapper-state 为 `running`；
- child/PID/TTY ownership 一致；
- 没有 failure、重复 process 或非计划设备调用；
- 当前仍处于 runner 预期阶段。

运行时间较长时，不使用短轮询、`wait/sleep`、launchd 或 app-server loop。创建当前 task 的一次性
heartbeat，时间按 cold proxy、captures 和已完成进度估算；heartbeat 提示必须包含 run path、PID、
logs、代码 checkpoint 和完成检查规则。每次 heartbeat 触发后先删除自身；若仍运行，重新估时并创建
新的单次 heartbeat。

### 7.2 固定采集顺序

Ray run：

1. Python finally 与 shell EXIT/INT/TERM/HUP cleanup 已安装；
2. 双源 all-off/readback；
3. 使用 retained shutter `1/5000`，不做曝光 trial；
4. emitter off `>=1800 s`，记录 `thermal_label=cold_proxy_uninstrumented`；
5. start ambient；
6. apply exact `H=120,S=100,INT=100`，拍 exposure-start target `60/120/300/600 s`；
7. final capture 返回后立即 off/readback；
8. 第二次 cold proxy `>=1800 s`；
9. cycle 2 同样执行，之后 mid ambient；
10. 第三次 cold proxy `>=1800 s`；
11. cycle 3 同样执行；
12. all-off/readback，end ambient；
13. Python cleanup，wrapper shell cleanup，wrapper 完整退出。

每个 formal capture 前 strip 必须 generation-bearing verified zero。command application 到 readback 完成后
开始 elapsed；request completion tail 必须记录，不得解释为额外 formal dwell、额外 capture 或下一实验
授权。

### 7.3 Ray 完成检查与分支

wrapper 完整退出后，检查第 9 节全部 artifact，再运行：

```zsh
.venv/bin/python -m \
  camera_based_rgbww_optimizer.optimization.analyze_p7_thermal_diagnostics \
  "$RAY_RUN_DIR" \
  --feature-ids config/hsi/strip-hsi-policy-v2-waiting.json
```

分支：

- capture/timing/isolation/readback/hash/cleanup/wrapper/artifact 任一 hard invalid：执行独立 recovery
  all-off，确认两灯关闭，写 `TD-A-RAY-HARD-INVALID`，不得启动 strip；
- 结构合法且 `status=settling_not_demonstrated_by_600`：这是合法 science result，继续 strip；
- 结构合法且 `status=td_a_pass`：继续 strip；
- 不自动创建第二个 Ray run。

## 8. Strip Source Run

Ray 结构合法后，不交还 Planner，使用全新 strip run directory 启动：

```zsh
tmp/run-p7-thermal-diagnostics.zsh "$STRIP_RUN_DIR" \
  --experiment-id p7_td_a_cold_settling_v1 \
  --source strip \
  --human-authorization p7_td_a_cold_settling_v1 \
  --camera-backend remote \
  --remote-timeout 120
```

执行与 Ray 相同的 OS-owned ownership、3 分钟健康检查和稀疏单次 heartbeat 合同。Strip 固定：

```text
argument order = cw,ww,r,g,b
command = 518,0,0,4095,0
retained shutter = 1/320
```

三个 cycle、cold proxy、ambient、timed points、off/readback、cleanup 顺序与第 7.2 节一致。每个 strip
formal capture 前 Ray intensity 必须 verified `0`。

wrapper 完整退出后检查 artifact，再运行同一单源 analyzer。任一 hard invalid：独立 recovery、确认
双灯关闭、写 `TD-A-STRIP-HARD-INVALID`，不得 retry 或 paired finalize。

## 9. Artifact Hard Gate

每个 source run 必须保留并可重放：

```text
plan.json
run.json
captures.jsonl
commands.jsonl
isolation-gates.jsonl
thermal-covariates.jsonl
remote-timing-metadata/*.json
commands-audit.json
analysis.json
all-off-python.json
all-off-shell.json
all-off-shell.stderr.log
all-off-shell.exit-status.txt
child-exit-status.txt
wrapper-result.json
camera/*.cr3
measurements/*.json
failure.json  # 仅失败时
```

Parent/entry evidence 必须保留：

```text
runner log
wrapper log
wrapper-state.json
launcher/PID/TTY/start-finish evidence
preflight and recovery artifacts
dry plans and hashes
```

Hard gates：

- 每源 12 formal、3 ambient、physical `<=22`；
- 全部 CR3 非空且 hash/recorded exposure/remote sidecar association 可重放；
- formal timing 只允许 Tier A/B；
- Ray/strip/ambient 三者每张恰好一个 source；
- exact command/readback；
- zero NPY；
- Python cleanup、shell cleanup、wrapper completion 全通过；
- source run status complete，失败 run 不伪装 complete；
- 旧失败 run 和本次新目录不交叉引用。

## 10. Paired Finalization

仅当 Ray 与 strip 两个 run 都结构合法时，确认冻结的 combined output path 仍不存在；由 production
finalizer 原子创建该目录并运行：

```zsh
.venv/bin/python -m \
  camera_based_rgbww_optimizer.optimization.analyze_p7_thermal_diagnostics \
  "$RAY_RUN_DIR" \
  --feature-ids config/hsi/strip-hsi-policy-v2-waiting.json \
  --paired-run "$STRIP_RUN_DIR" \
  --combined-output "$COMBINED_DIR" \
  --code-checkpoint 960484e1107cbcfb3304075a5ac54a0fbe6a382e
```

Combined directory 必须恰好保留：

```text
td-a-combined-analysis.json
EXPERIMENT_SUMMARY.md
input-manifest.json
```

必须确认：

- manifest schema 为 `p7_td_a_input_manifest_v1`；
- decision owner 为 `Planner`；
- code checkpoint 精确为 `960484e1107cbcfb3304075a5ac54a0fbe6a382e`；
- Ray/strip run path、plan/run hash、feature policy hash、frozen inputs、timing、analysis/summary hash 全部
  replay pass；
- formal total 24、ambient total 6、physical total `<=44`；
- 默认 operating-envelope 在 finalization 前后 byte-identical；
- 不生成或安装默认 config；
- existing combined directory 不覆盖。

两个 source 和 paired finalizer 后，再执行一次独立 final all-off，并用 Ray readback 与 generation-bearing
strip snapshot 确认最终双灯关闭。Python、shell 和 independent final zero 三类证据保存到 entry/final
safety evidence 路径，不得向 combined directory 添加第四个文件。

## 11. TD-A 判定

每个 source 独立：

1. 候选只允许 `60/120/300`；
2. 每 cycle 候选与同 cycle 所有更晚点通过 frozen compatibility；
3. 同一时点 3 cycles center 通过 frozen same-state joint coverage；
4. 所有合法 pair 使用 exact evaluator；
5. chronology trend `<=4.0`；
6. single-frame dominance `<=0.5`；
7. 无持续单向 feature drift；
8. timing Tier A/B、quality、isolation、readback、recorded exposure、cleanup 和 wrapper 全通过；
9. 返回最早合法候选，否则 null。

`600 s` 只验证更早候选，不能返回 `t_settle=600`。

Combined：

```text
both t_settle non-null:
  status = td_a_pass
  t_formal_provisional_s = max(t_settle_ray_s, t_settle_strip_s)

either t_settle null:
  status = settling_not_demonstrated_by_600
  t_formal_provisional_s = null

Tier C / timing hash or clock mismatch:
  hard invalid; no valid combined result
```

不得把趋势并入 covariance，不得调整 threshold，不得写 600 为 settle，不得扩展 900/1200，也不得
覆盖正式 operating-envelope。

## 12. 安全与停止分支

| 分支 | 条件 | 动作 |
| --- | --- | --- |
| `TD-A-OFFLINE-ENTRY-FAIL` | commit/hash/dry plan/path/test/process ownership 失败 | 零设备，停止交还 Planner |
| `TD-A-PREFLIGHT-FAIL` | remote/readback/off/settings 失败 | 双 cleanup 与独立 zero，零正式 capture，停止 |
| `TD-A-RAY-HARD-INVALID` | Ray 采集或证据合同无效 | 双 cleanup，不启动 strip，停止 |
| `TD-A-RAY-NONSETTLE` | Ray 合法但 600 内未证明稳定 | 继续 strip，最终 combined nonsettle |
| `TD-A-STRIP-HARD-INVALID` | strip 采集或证据合同无效 | 双 cleanup，不 retry、不 finalizer，停止 |
| `TD-A-NONSETTLE` | 两源合法，至少一源 settle=null | combined nonsettle，最终双关灯，停止交还 Planner/Advisor |
| `TD-A-PASS` | 两源合法且 settle 均非空 | 生成 provisional combined evidence，最终双关灯，停止交还 Planner |

统一安全合同：

- 每张照片只允许 Ray、strip 或 ambient 之一；
- Python finally 无条件尝试关闭两灯，单项失败不阻止另一项 cleanup；
- shell trap 独立 all-off，保存 stdout、stderr 和 exit code；
- 任一状态不确定立即 independent recovery all-off；
- cleanup evidence 缺失不能声称 complete；
- 不保存 NPY；
- 不进行短轮询，不因“观察 5 分钟”停止长任务；
- 不删除失败 CR3、sidecar、logs 或 cleanup evidence；
- 不自动 retry；
- 本计划结束后不进入下一阶段。

## 13. Executor 交接模板

```text
Result status:
Authorization consumed at:
PLAN modified: no

Offline entry:
- accepted commit existence:
- wrapper SHA-256:
- frozen input hashes:
- operating-envelope null fields/hash:
- Ray/strip dry plans and hashes:
- new entry/Ray/strip/combined paths:
- process ownership audit:
- focused/wrapper/diff:

Preflight:
- remote health/config/v2/settings:
- Ray off/readback:
- strip identity/generation/zero:
- preflight Python/shell cleanup:
- formal capture count before source command:

Ray:
- path/PID/PPID/PGID/TTY/log/start-finish:
- formal/ambient/physical:
- command/shutter/settings:
- CR3/recorded exposure/timing tiers/NPY:
- isolation/readback/cleanup/wrapper:
- analysis status/t_settle_ray_s:

Strip:
- path/PID/PPID/PGID/TTY/log/start-finish:
- formal/ambient/physical:
- command/shutter/settings:
- CR3/recorded exposure/timing tiers/NPY:
- isolation/readback/cleanup/wrapper:
- analysis status/t_settle_strip_s:

Combined:
- path:
- analysis/summary/manifest SHA-256:
- manifest replay:
- code checkpoint:
- total formal/ambient/physical:
- status/t_formal_provisional_s:
- default operating-envelope unchanged:

Final safety:
- Python cleanup:
- shell cleanup:
- independent Ray zero:
- independent strip generation-bearing zero:
- residual process:
- retry performed: no

Next = Planner review only; all later stages locked
```

## 14. 当前状态机

```text
current_phase = P7_TD_A_COLD_SETTLING_EXECUTION
stage_status = authorized_ready_for_single_execution_package
decision_owner = Human authorization + Planner execution gate
authorization = restored existing p7_td_a_cold_settling_v1 exact scope
authorization_consumed = false until first successful nonzero source command
source_order = ray_then_strip
code_checkpoint = 960484e1107cbcfb3304075a5ac54a0fbe6a382e
td_a = authorized_once
td_b = locked
td_c = locked
sentinel = locked
remaining_9 = locked
boundary = locked
holdout = locked
Gate_6 = locked
P8 = locked
default_install = locked
next_action = execute exact TD-A Ray then strip package, finalize, stop for Planner
```
