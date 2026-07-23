# P7-TD-A 900/1200 秒扩展决策请求

> **已被人工决定取代。** Human/Developer 已明确拒绝 900/1200 秒扩展，并选择 600 秒作为产品
> operational dwell。本文件只保留为决定前的历史问题清单，不再是当前待办；详见
> `03-human-decision-no-extension.md`。

## 1. 当前硬停止

```text
TD-A acquisition = accepted
TD-A scientific gate = not_settled_by_600
operating envelope = undefined
t_formal_provisional = null
Executor device work = locked
TD-B / TD-C / sentinel / remaining / boundary / holdout / Gate-6 / P8 = locked
```

第三轮 GUIDE 已明确该分支必须请求 Advisor 决定 900/1200 秒扩展。Planner 没有把结果解释为代码
失败，也没有自行延长实验。

## 2. 需要 Advisor 冻结的决定

### 2.1 是否扩展

请明确选择：

1. 批准一个新的 TD-A thermal extension；
2. 先做新的离线分析或修改 measurement model，再决定是否实拍；
3. 不再追求当前 `conditioned_steady_after_switch` envelope，并说明 P7 应如何收口。

### 2.2 若扩展，必须给出 exact experiment contract

旧 cycle 已在 600 秒后关闭，不能事后追加同一条时间序列。新 GUIDE 至少应冻结：

- Ray 与 strip 是否都重测，还是允许 source-specific 设计；
- 每个 source 的 independent cold cycle 数；
- 新 run 是否必须重拍 300/600 作为 overlap anchor；
- 正式采样点是否为 `[300,600,900,1200]`、`[600,900,1200]` 或其他预先冻结集合；
- 1200 秒是候选还是 validation-only；
- cold proxy、continuous-on 上限、ambient 位置、formal/physical CR3 cap；
- 新旧 TD-A 是否允许联合判断，若允许，怎样处理 session/epoch 与不同 cycle 的 covariance；
- 最早候选 `t`、joint coverage、trend、dominance 与持续单向 drift 的验收规则；
- 一个 source 通过、另一个仍未通过时的状态；
- 1200 秒仍未稳定时的停止状态和是否允许更长时间；
- 新实验之后何时才允许定义 `t_formal_provisional` 并进入 TD-B。

### 2.3 时间语义

现有 timing 只能继续声明：

```text
timing = best_effort_gphoto2_observed_elapsed_v2
absolute_exposure_start = false
nominal_slot = scheduler/grouping only
nominal_proximity_gate = none
```

若 Advisor 认为 900/1200 秒判定需要绝对 exposure-start，应明确提出新的远程能力要求；否则建议保持
当前 Developer/Human 决策，不因约 4 至 5 秒的稳定 bridge delay 否定 retained capture。

## 3. Planner 建议的保守边界

Planner 不预先决定采样点，但建议任何扩展都满足：

- 使用全新 named run 和新目录，不修改旧 TD-A evidence；
- 至少保留一个与旧范围重叠的 anchor，避免 600 与 900/1200 之间无连接；
- 保留三个 independent cycle，除非 Advisor 明确给出减少 cycle 的统计理由；
- Ray 与 strip 继续拆成独立、非并发 source run；
- 不在同一 run 内重估 uncertainty 或放宽门槛；
- 继续使用 Python finally、shell trap 和独立 final zero readback；
- 运行结束必须再次停在 Planner 门，不自动进入 TD-B。

## 4. Advisor 前禁止事项

- 不重跑原 TD-A；
- 不启动 900/1200 秒设备实验；
- 不把 600 秒写为 steady 或 provisional；
- 不修改 trend `4.0`、dominance `0.5`、joint coverage、covariance 或 58-feature；
- 不合并 cold 与 steady covariance；
- 不进入 TD-B、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6 或 P8；
- 不覆盖默认 LUT/runtime 或 operating-envelope settle fields。
