# P7-TD-A 900/1200 秒扩展门归档：由人工决定不扩展

**Planner 归档时间：** `2026-07-21T21:13:15-0600`

**被归档 active PLAN SHA-256：**
`f88fc960f78972fe895b85cc6a4f95b912e6d303afffb2d49d8db055415b1746`

## 1. 被归档计划

被归档计划状态为 `waiting_for_advisor_900_1200_extension_decision`。它依据 Advisor 第三轮 GUIDE
保留 TD-A 的有效负结果，并等待 Advisor 冻结 900/1200 秒扩展。该计划没有授权 Executor 执行代码、
网络、设备或实拍操作。

## 2. Human/Developer 决定

Human/Developer 在当前 thread 明确决定：

```text
不要继续扩展。使用目前的600秒。
记录下来这是人工的决定，不是planner的擅自决定，开发者不希望在这一点上拖长时间。
```

Planner 记录为：

```text
decision_owner = Developer/Human
decision_kind = product_operational_time_limit
thermal_extension_900_1200 = rejected
developer_selected_operational_dwell_s = 600
decision_reason = developer_does_not_want_to_extend_schedule_at_this_point
planner_inference = false
```

该决定取代 Advisor extension request，但不篡改 TD-A 的测量结论。以下历史事实继续有效：

```text
Ray = settling_not_demonstrated_by_600
strip = settling_not_demonstrated_by_600
t_settle_ray_s = null
t_settle_strip_s = null
t_formal_provisional_s = null
```

600 秒只能称为 Developer/Human 选择的 operational dwell，不得在报告、schema 或 analyzer 中改称
`settled`、`steady`、`td_a_pass` 或基于测量得到的 `t_formal_provisional`。

## 3. Planner 复核与代码现实

当前代码不能直接执行该决定：

- `SELECTABLE_SETTLE_POINTS` 仅允许 `60/120/300`；
- TD-B execute 要求 operating envelope `status=td_a_pass`；
- TD-B execute 要求 `t_formal_provisional_s` 属于 `60/120/300`；
- 当前 `config/hsi/p7-operating-envelope-v1.json` 保持 `offline_schema_only` 且 settle fields 全为 null；
- 直接覆盖 v1 会破坏 retained TD-A plan 的 frozen-input replay，因此禁止修改 v1。

所以 Planner 不把 600 填入旧字段，而是打开一个 bounded offline package：新增独立 v2 operating
envelope 和显式 Developer override 语义，使 TD-B 可以按 600 秒运行，同时继续报告未证明稳定。

## 4. 决策后的边界

- 不执行 900/1200 秒扩展；
- 不重跑 TD-A；
- 不修改历史 TD-A artifacts 或 analyzer 结果；
- 不放宽 trend、dominance、coverage、covariance 或 58-feature；
- 不把 600 秒的操作选择写成科学稳定性通过；
- 下一步只允许离线实现、测试和 TD-B dry-run；
- TD-B 实拍仍需新的 active PLAN，不从本归档自动启动；
- TD-C、sentinel、remaining、boundary、holdout、Gate-6 和 P8 继续锁定。

## 5. 唯一下一分支

`P7_TD_B_DEVELOPER_DWELL_OVERRIDE_R0`：Executor 离线实现 600 秒 operational dwell override，保留
科学结论与产品决策的语义分离，生成 Ray/strip TD-B dry-run 后停在 Planner 门。
