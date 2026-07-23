# P7-R1 Advisor 决策请求

## 当前硬停止

```text
stage_status = blocked_waiting_for_advisor
candidate = retained
formal_capture_eligible = false
analysis_branch = uncertainty_unresolved
ray_branch = R-REFERENCE-UNSTABLE
sentinel_v2 = locked
remaining_9 / boundary / holdout / P8 = locked
new_device_run = not authorized
```

## 需要冻结的实验定义

1. 正式目标是 cold-start 后固定 60 秒的 transient output、连续点亮后的 steady-state，还是同时覆盖两个 operating envelope。
2. 下一轮定向实验采用哪种组合：
   - long-off 后的 cold-start repeatability；
   - 60/120/300/600 秒 settling curve；
   - 固定热状态后 command switch 对照；
   - ABBA 或短周期 Ray anchor/strip reference 交错。
3. 是否允许增加 time/thermal covariate；若允许，需明确它是条件 repeatability 还是额外 worst-case uncertainty，不能用它掩盖真实颜色漂移。
4. 当前 `reference_epoch_shift=false` 但 P6 compatibility 仍失败，应解释为热协议问题、新自然日重新锚定，还是需要拆分 cold-start 与 steady-state 的 analyzer 语义。

## Advisor 前不得做的事

- 不重跑 P7-R1；
- 不进入 sentinel-v2 或剩余 9 点；
- 不做 boundary、holdout 或 P8 INT；
- 不修改 trend `4.0`、single-frame dominance `0.5`、covariance、joint coverage、guard 或 58-feature；
- 不把 `uncertainty_unresolved` 写成 `physically unreachable`；
- 不启动新的高输出设备实验。

## 可继续的工作

只允许保留当前 run/candidate，进行离线 chronology、thermal hypothesis 和 analyzer regression，
以及更新计划。收到 Advisor 新 GUIDE 后，Planner 再重写 active PLAN，并另行确认精确的设备授权范围。
