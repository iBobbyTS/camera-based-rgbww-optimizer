# P7-TD-A：等待新的精确 Human 授权

**计划状态：** `waiting_for_new_exact_human_authorization`

**Planner 日期：** `2026-07-21`

**当前阶段：** `P7_TD_A_COLD_SETTLING_V1_AUTHORIZATION_GATE`

**当前唯一动作：** 等待 Human 明确批准一次完整、命名为
`p7_td_a_cold_settling_v1` 的 TD-A cold-settling 设备实验。当前没有 Executor 可执行的设备动作。

**唯一 Planner 停止点：**

- 未获得精确授权：保持停止，不运行任何 preflight、网络请求、相机 capture、灯光 command 或
  `all_off` probe；
- 获得精确授权：Planner 先把授权原文、范围、预算和恢复路径写入新的 active PLAN，再交 Executor；
- 授权被拒绝或范围改变：保持本计划并等待新的 Planner 决定，不自行扩大或替换实验。

## 1. 已完成并归档

### R1 离线合同纠偏

R1 已验收为 `R1-PASS`。五个 T0 finding 已闭合，独立验证为 focused `58/58`、full `502/502`
（`113.494 s`）；旧失败 run 与 default operating envelope 哈希均保持不变，未发生设备、网络、
`.env`、相机、Ray、ESPHome、真实 `all_off` 或新 CR3 副作用。

归档：

| 文件 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260721-1427-p7-td-a-t0-r1-review.md` | `53194e42ea71c2a74c86d6b0c195415eeb27eaad8beeb0e8ba40f1f32da768dd` |

实现 checkpoint：`4901f819a8c43b6ffea89427f3960d9dc5e41159`。

### TD-A v2 source-scoped dry-run

Planner 已实际生成并检查两份离线 plan，均退出码 `0`，输出目录只含 `plan.json`，无 CR3、NPY、
run、后台进程或设备副作用：

| source | plan | SHA-256 |
| --- | --- | --- |
| Ray | `/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-20260721-1432/ray/plan.json` | `3ff0b763cf224a8ae232482ec542f6120382565510770c18ab951795efe8a653` |
| strip | `/Volumes/4T/temp/rgbww-optimizer/p7-td-a-dryrun/td-a-dryrun-20260721-1432/strip/plan.json` | `a4d8eb34911058cfc6f8adbc5707a5d8062f711ce6ccb3565805b4c6d11c2420` |

dry-run 验收归档：

| 文件 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260721-1435-p7-td-a-dryrun-review.md` | `0851b10bdd429057c586d83e38a07885ba1ef954122cb0d5d6bc17d3fae1dbb5` |

两份 plan 均冻结：

- `p7_thermal_diagnostic_plan_v2` / `p7_td_a_cold_settling_v1` / `TD-A`；
- 每个 source `12 formal + 3 ambient`，`physical_cr3_cap=22`；
- 三个独立 cycle，每个为 `60/120/300/600 s`，600 仅 validation-only；
- Ray 只使用 `ray-h120-s100` shutter，strip 只使用
  `strip-h120-s100-fullscale` shutter，`exposure_setup_required=[]`；
- Tier A/B best-effort observed elapsed，`absolute_exposure_start=false`，无 nominal proximity gate；
- 最新 location 为 `config/location/locations-20260714-211759.json`，SHA-256
  `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`；
- `formal_capture_eligible=false`，sentinel、TD-B/C、remaining、boundary、holdout、Gate-6、P8
  locks 保持开启。

## 2. 当前授权事实

- 旧 TD-A 一次性授权已消费，不可用于重试或解释为本轮授权；
- R1-PASS 和 dry-run-PASS 都不是设备授权；
- 当前 active PLAN 不允许 Executor 读取 `.env`、连接 remote、访问设备或调用 cleanup API；
- Developer/Human 的既定 timing 决定保持有效：记录 gphoto2 最佳 observed elapsed，不能宣称绝对
  exposure-start，也不能使用 `+/-2 s` 或等价 nominal offset gate。

## 3. 待 Human 批准的 exact named experiment

Human 若批准，必须明确覆盖以下完整范围；只批准其中一部分不解锁执行：

```text
experiment_id = p7_td_a_cold_settling_v1
sources = Ray120c and bedroom-rgbww-strip
source order = two independent non-concurrent runs, Ray then strip
state = H120/S100/INT100 equivalent at full-scale operating policy
cycles per source = 3 independent cold cycles
timed points = 60, 120, 300, 600 seconds per cycle
formal captures = 12 per source, 24 total
ambient captures = start/mid/end, 3 per source
physical cap = 22 per source, 44 total diagnostic allocation
cold proxy wait = 1800 seconds before each cycle
continuous source-on schedule = 3 x 600 seconds per source
timed-cycle auto-exposure = forbidden
camera = authenticated remote v2 backend
timing = best-effort gphoto2 observed elapsed, non-absolute
cleanup = Python finally + shell EXIT/INT/TERM/HUP trap + independent recovery
```

每个 source 的计划最短时间为 `3 x (1800 + 600) = 7200 s`，不含请求、曝光和 cleanup overhead；
两 source 不并发，Human 必须理解约四小时总实验窗口、高输出状态、最多 44 个 physical CR3，以及
中断后的双层关灯恢复路径。900/1200 s 扩展、额外 state/source、TD-B、TD-C 和 sentinel 不在授权范围内。

## 4. 获得授权后的 Planner/Executor 边界

授权到达后，Planner 必须先更新本文件或建立新的 active PLAN，至少写入：

1. Human authorization 原文、时间、experiment ID 和批准范围；
2. Ray/strip source order、每 source `formal=12`、`ambient=3`、`physical cap=22`；
3. 远程 v2 backend、最新 location/hash、source-specific shutter ledger；
4. 预计连续点亮时长、总时间上限、abort 条件和 Python/shell 双 cleanup；
5. 明确 Executor 可消费该授权一次，且不得进入 TD-B/C。

Executor 执行时必须使用 `tmp/run-p7-thermal-diagnostics.zsh`，每次仅一个 source 亮起，在 run start、
ambient、transition、结束和异常路径保留独立 off/readback 与 cleanup 证据。任何 command/readback、
source isolation、remote metadata、CR3 ownership、observed timing integrity 或 cleanup 失败都要
停止、保留证据并交 Planner，不能自动 retry。

## 5. TD-A 结果分支（实拍后才适用）

- 每个 source 从 `60/120/300` 选择最早满足 frozen joint coverage、三 cycle center compatibility、
  trend `<=4.0`、single-frame dominance `<=0.5`、无单向 drift、quality/readback/exposure/cleanup
  gates 的候选；
- `600 s` 只作 validation。若 `300 -> 600` 仍有系统性变化，输出 `not_settled_by_600`，停止并
  请求 Planner/Advisor 决定 `900/1200 s`，不得自动称为 steady 或进入 TD-B；
- 两 source 都通过才生成 `t_formal_provisional_s=max(ray, strip)`，交 Planner 复核；不自动进入
  TD-B、TD-C、sentinel 或任何 HSI 正式优化；
- 任一失败只能归类为 timing/measurement/reference/operating-envelope 未解决或 cleanup failure，
  不得写成 physical gamut boundary、`hue_unreachable` 或 P8 许可。

## 6. 硬锁

在 TD-A 通过并经 Planner 明确验收前，TD-B、TD-C、四点 sentinel、remaining 9、boundary、holdout、
Gate-6、P8、firmware、remote deployment、默认 LUT/runtime 安装全部锁定。不得重拍 P7-R1、删除
Ray B 首帧、修改 trend/dominance、扩大 covariance/joint coverage、改变 58-feature、合并 cold/steady
covariance 或使用同一 run 拟合并通过 thermal correction。

---

## 7. Planner 决策记录：Human 放行 Executor（2026-07-21）

Human 在当前 thread 明确要求：

```text
修改AGENTS.md，开灯不需要人工授权。
本次的PLAN也改掉，放行executer。
```

Planner 将该决定解释为：Executor 可直接消费本实验既定范围内的 Ray120c/RGBWW 开关灯及 TD-A
采集操作，不再等待或重复询问独立的 light-on authorization。它不扩大实验范围，也不授权 TD-B、
TD-C、sentinel、firmware、remote deployment 或任何超出本计划的操作。

本归档时的 active PLAN SHA-256：
`a4a3cf364675d21dee923807c21385e7cbe63b24958c98b221dbba82461d043b`。

下一分支：Planner 必须把该决定和 exact TD-A bounds 写入新的 active PLAN；Executor 之后可按新计划
启动，不得再以“等待 Human 授权”为理由停下，也不得自行扩大 bounds。
