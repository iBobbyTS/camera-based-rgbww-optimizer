# P7-TD-A：cold settling 设备授权前 dry-run 门

**计划状态：** `waiting_for_td_a_dry_run_and_human_authorization`

**Planner 日期：** `2026-07-21`

**当前阶段：** `P7_TD_A_COLD_SETTLING_V1`

**当前唯一动作：** Executor 只生成并验收 Ray 与 strip 两份 TD-A v2 离线 dry-run plan，确认
source-scoped shutter、计数、时序和输入哈希正确，然后停止交 Planner。当前计划不包含任何设备、网络、
`.env`、remote API、相机、Ray、ESPHome、`all_off` 或真实 CR3 操作。

**唯一 Planner 停止点：** 两份 dry-run plan 均满足本文件第 3 节合同并有完整离线证据；若任一合同失败，
只记录证据并停止，不得自行修复实验语义或启动实机。

**重要授权状态：** 旧 TD-A 一次性 Human authorization 已在此前 Ray 非零 command 成功时消费。
本文件没有新的 Human authorization。dry-run 通过不会恢复或扩大旧授权；只有 Planner 在获得新的、精确
覆盖本文件第 5 节操作范围的 Human 明确批准后，才能另写授权版 `PLAN.md` 交 Executor 执行。

## 1. R1 验收与归档

R1 离线纠偏已接受为 `R1-PASS`。五个 T0 finding 均闭合，且不代表 Ray 已稳定：

- focused P7 suite：`58/58`；独立完整套件：`502/502`，`113.494 s`；
- `compileall`、所有 `tmp/*.zsh` 语法检查、`git diff --check`、CodeGraph 均有通过证据；
- validation summary SHA-256：
  `3c38698ded093a734c708b27f0cbf13080ae3439382a5505055c1c2ef9918048`；
- 旧失败 run 的 `plan.json`、`run.json`、`failure.json`、`recovery-all-off.json` 前后哈希不变；
- default operating envelope 前后哈希均为
  `d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25`；
- 本轮没有设备、网络、`.env`、相机、Ray、ESPHome、真实 `all_off` 或新真实 CR3 副作用。

完整审查归档（未覆盖旧归档）：

| 文件 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260721-1427-p7-td-a-t0-r1-review.md` | `53194e42ea71c2a74c86d6b0c195415eeb27eaad8beeb0e8ba40f1f32da768dd` |

实现 checkpoint：`4901f819a8c43b6ffea89427f3960d9dc5e41159`。

## 2. Executor 读取顺序与写入边界

开始前依次读取：

1. 本文件全文；
2. `AGENTS.md`、`.agent-work/PLAN/00-CONTRACT.md`；
3. `.agent-work/PLANS/20260721-1427-p7-td-a-t0-r1-review.md`；
4. `.agent-work/EXECUTION_RESULT.md` 的 R1 交接；
5. `advisor/3/1.GUIDE.md`、`docs/README.md`、项目 camera skill；
6. 使用 CodeGraph确认当前 `p7_thermal_diagnostics` plan builder、dry-run runner、analyzer 和
   remote-v2 owner；
7. `git status --short --branch`，保留所有现有 Human/Planner 工作树内容。

只允许写入：

- `/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/` 下的新离线证据；
- `.agent-work/EXECUTION_RESULT.md` 的本轮交接追加；
- 必要的测试日志和不含凭据的摘要。

不得修改或写入：

- `.agent-work/PLAN.md`、`.agent-work/PLANS/`；
- `advisor/3/`、`AGENTS.md`、remote host、`remote_camera_controller/`；
- `.env` 或任何 token；
- 设备、网络、默认 LUT、默认 operating-envelope 数值或既有实拍 artifact。

## 3. 离线 dry-run 唯一动作

### 3.1 生成两份 source-scoped plan

使用全新的时间戳目录，例如：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-<timestamp>/
```

分别运行以下两个 dry-run；不要使用 `--execute`、`--allow-device-control`，也不要提供 Human
authorization 参数：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --experiment-id p7_td_a_cold_settling_v1 \
  --source ray \
  --dry-run \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-<timestamp> \
  --run-name ray

.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --experiment-id p7_td_a_cold_settling_v1 \
  --source strip \
  --dry-run \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-<timestamp> \
  --run-name strip
```

命令只能产生 `plan.json`，不得建立 production run、连接 backend 或读取 `.env`。若 CLI 或输入
artifact 缺失，记录明确失败原因并停止。

### 3.2 Dry-run 必须验证的硬条件

对 Ray 和 strip 两份 plan 均独立验证：

- `schema = p7_thermal_diagnostic_plan_v2`，`experiment_id = p7_td_a_cold_settling_v1`，
  `stage = TD-A`，`status = dry_run_complete_device_locked`；
- `formal_cap = 12`、`ambient_cap = 3`、`physical_cr3_cap = 22`；两份合计 formal `24`，
  source-run physical cap 合计 `44`；
- 三个 `cycle_index` 各有严格的 nominal slots `60, 120, 300, 600`，且每个 cycle 的 command
  连续不变；600 秒标记为 validation-only，不能被自动选为 settle time；
- plan 只包含自身 source 的 shutter keys：Ray 只能使用 retained P7-R1 的 `ray-h120-s100`，
  strip 只能使用 retained P7-R1 的 `strip-h120-s100-fullscale`；不得出现未来 TD-B 的
  `ray-h120-s50` setup 或任何跨 experiment key；
- timed capture 禁止 auto-exposure trial，shutter 在 cycle 前冻结；`exposure_setup_required=[]`；
- timing contract 为 v2：Tier A/B、有限非负 observed elapsed、method/sidecar 可重放；
  `absolute_exposure_start=false`，nominal slot 只用于分组，`nominal_offset_gate=none`；
- Ray command 为 `H120/S100/INT100`，strip command 为 retained P7-R1 的 H120/S100 full-scale
  command；不得调用 solver 生成新 strip command；
- plan 保留 remote backend/v2 capability、latest location 输入及所有 frozen input hash，但不
  读取或打印凭据；Python finally 与 shell `EXIT/INT/TERM/HUP` cleanup contract 必须存在；
- `formal_capture_eligible=false`，sentinel、TD-B/C、remaining、boundary、holdout、Gate-6 和
  P8 locks 全部为 true；
- 两份 plan 的 `offline_contract` 设备、网络、`.env`、相机和 `all_off` 计数均为零，输出目录无
  `.npy`、无 CR3、无后台进程。

### 3.3 Dry-run 证据

Executor 必须保留：

- `ray/plan.json`、`strip/plan.json` 及其 SHA-256；
- 解析后的 capture/ledger 摘要，列出 formal、ambient、physical、shutter keys、cycle/slot；
- dry-run stdout/stderr、进程退出码、side-effect audit；
- focused dry-run tests（如新增或复用）及 `git diff --check`；
- `.agent-work/EXECUTION_RESULT.md` 中的确切路径、哈希和结论。

完成后立即停止，不能因为 dry-run 绿灯而执行 preflight、`all_off` probe、remote health/config、
相机 capture、Ray/strip command 或 TD-A 实拍。

## 4. TD-A 离线分析合同（仅为后续授权准备）

真实 run 获得新授权后，analyzer 必须对每个 source 从 `[60, 120, 300]` 中选择最早满足以下全部
条件的时间：

1. 该时间及所有更晚点的同状态差异通过冻结 joint coverage；
2. 三个 cold cycle 对应中心兼容；
3. chronology trend `<= 4.0`、single-frame dominance `<= 0.5`；
4. 无持续单向 feature drift，且 quality、source isolation、readback、recorded exposure、timing
   provenance、physical ownership 和双 cleanup 全部通过。

`600 s` 只用于验证。如果 `300 -> 600` 仍有合法系统性变化，输出
`not_settled_by_600`，停止并请求 `900/1200 s` 扩展；不得把 600 自动改称 steady，也不得进入
TD-B。两 source 都通过时才生成 `t_formal_provisional_s = max(ray, strip)`，交 Planner 复核；
不得自动启动 TD-B、TD-C 或 sentinel。

## 5. 新 Human 授权的精确候选范围（当前不是授权）

只有 Human 明确批准下列**完整 named experiment**后，Planner 才能在新的 active PLAN 中记录授权，
Executor 才可执行：

```text
experiment_id = p7_td_a_cold_settling_v1
sources = Ray120c, bedroom-rgbww-strip
source order = two independent non-concurrent runs, Ray then strip
state = H120/S100/INT100 equivalent at full-scale operating policy
cycles per source = 3 independent cold cycles
timed points per cycle = 60, 120, 300, 600 s
formal captures = 12 per source, 24 total
ambient captures = start/mid/end, 3 per source
physical cap = 22 per source, 44 total diagnostic allocation
continuous source-on schedule = 3 x 600 s per source
cold-proxy wait = 3 x 1800 s per source before each cycle
timed-cycle auto-exposure = forbidden
camera = authenticated remote v2 backend; best-effort gphoto2 timing only
cleanup = Python finally plus shell EXIT/INT/TERM/HUP trap, with independent recovery
```

按当前 schedule，每个 source 的最小计划时间为 `3 x (1800 + 600) = 7200 s`，不含相机请求、
曝光和 cleanup overhead；两 source 不并发，Human authorization 必须覆盖约四小时的总实验窗口、
高输出状态、最大 44 个 physical CR3 和中止后的双层关灯恢复路径。任何更高输出、更长 dwell、额外
source/state、900/1200 扩展或 TD-B/C 均不包含在此候选授权内。

实际执行时仍必须：

- 每次仅一个 source 亮起；run start、ambient、transition 和结束均做独立双源 off/readback gate；
- 使用 `tmp/run-p7-thermal-diagnostics.zsh`，保持 Python cleanup 与 shell trap 两层证据；
- 用 remote backend 的一次性 resolved ISO/aperture/RAW settings，timed cycle 不重新 auto-expose；
- 记录 observed elapsed 和 estimate method，但不声称 absolute exposure-start，不使用 nominal
  `+/-2 s` proximity gate；
- 任一 readback、source isolation、timing integrity、CR3 ownership、remote metadata 或 cleanup
  失败立即停止并保留证据，不自动 retry 或进入下一阶段。

## 6. 未授权与后续锁定

在新的精确 Human authorization 被 Planner 写入新的 active PLAN 前：

- Executor 的唯一动作只有第 3 节离线 dry-run；
- TD-A 实拍、TD-B、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6、P8、firmware、
  remote deployment、默认 LUT/runtime 安装全部禁止；
- 不得重新拍 P7-R1、删除 Ray B 首帧、修改 trend/dominance、扩大 covariance/joint coverage、
  改 58-feature 或把 `uncertainty_unresolved` 改写成 gamut failure；
- 若 TD-A 在 600 秒内未证明稳定，必须回到 Planner/Advisor 决定是否扩展，不得自行延长或改变门槛。

---

## 7. Planner dry-run 验收记录（2026-07-21）

### 7.1 执行证据

Planner 在不访问网络、`.env`、remote API、设备或 `all_off` 的条件下实际生成两份 source-scoped
dry-run：

| source | plan | SHA-256 |
| --- | --- | --- |
| Ray | `/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-20260721-1432/ray/plan.json` | `3ff0b763cf224a8ae232482ec542f6120382565510770c18ab951795efe8a653` |
| strip | `/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-20260721-1432/strip/plan.json` | `a4d8eb34911058cfc6f8adbc5707a5d8062f711ce6ccb3565805b4c6d11c2420` |

两条命令退出码均为 `0`，输出目录只含两份 `plan.json`，无 `.npy`、CR3、run artifact 或后台进程。

### 7.2 合同核对

两份 plan 均满足：

- v2 schema、exact TD-A experiment ID、`dry_run_complete_device_locked`；
- 每 source `12 formal + 3 ambient`，`physical_cr3_cap=22`；
- cycle `1..3`，每 cycle slots 为 `60/120/300/600`，600 validation-only；
- Ray shutter ledger 只含 `ray-h120-s100`，strip 只含
  `strip-h120-s100-fullscale`，两者 `exposure_setup_required=[]`；
- v2 timing 为 Tier A/B best-effort observed elapsed，`absolute_exposure_start=false`，
  `nominal_offset_gate=none_developer_decision`；
- latest location SHA-256 为
  `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`；
- `formal_capture_eligible=false`，后续 hard locks 保持 true，offline side-effect contract 全零。

额外验证：`compileall`、全部 `tmp/*.zsh` 语法、`git diff --check`、CodeGraph、Markdown fence
结构均通过。

### 7.3 决定与下一分支

```text
decision = TD-A-DRYRUN-PASS
next = wait_for_new_exact_human_authorization
```

本次 dry-run 不构成设备授权。当前唯一下一分支是由 Human 明确批准本归档第 5 节的完整
`p7_td_a_cold_settling_v1` 范围；未批准前 Executor 没有任何可执行动作。批准后 Planner 必须把
authorization 原文、source order、每 source physical cap `22`、连续高输出时长、约四小时实验窗口和
双 cleanup/recovery 写入新的 active PLAN，才可运行 preflight 和实机。
