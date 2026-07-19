# P7-R0K executable exhaustibility contract

- 状态：blocked_for_planner
- 基线：`84577a4`
- 范围：仅 exhaustibility contract、confirmation_groups 与 physical denial production round-trip；禁止设备、网络、`.env`、firmware 与 P7-R1。

## 已确认事实

1. R0J canonical runner finalization、start/target scope 与 post-capture fatal accounting 应保留。
2. matrix 目前未被 producer/analyzer 执行，伪造 `initial` exhaustion 可通过。
3. production `confirmation_groups` 在第三次 reservation 可达，现有 matrix 分类错误。
4. physical denial 尚无正式 runner persistence → public analyzer 证明。

## 根因假设

可达性仍是文档元数据而非 schema validator；sub-budget 也不足以区分 physical pre-denial 与 post-capture fatal path。

## 已完成诊断

1. matrix 已重构为稳定 path contract；runner canonicalizer、formal analyzer 和 readiness 读取同一个对象。
2. 真实 solver 已稳定触发 `logical.confirmation_groups` / `confirm-2`，并完成正式 fake runner persistence 到 public analyzer 回环。
3. post-capture overrun 通过 fatal path ID 落入 failure evidence，保留非空 CR3 和 Python cleanup。
4. public analyzer 已拒绝伪造的 guarded `logical.initial`。

## 阻塞分支

冻结普通点上限满足 `67 = 54 + (10 - 1) + 4`。用实际预算对象填满两个 start 的 54 logical observations、10 张首个 auto-exposure CR3 和 4 张 weak reacquire 后，physical 恰为 67、remaining 为 0；下一次 `feedback-8` 首先被 start category/logical gate 拒绝，capture callback 不会执行。因此当前正式控制流无法产生 `physical.pre_capture_denial`，与 R0K 将其要求为 production-reachable 并要求完整 public round-trip 冲突。

禁止用 patched solver 第 55 次额外回调或手工 target row 冒充 production success。Planner 需选择：

- 将 `physical.pre_capture_denial` 改为 guarded-unreachable，并以 public rejection + fatal post-capture 路径作为门禁；或
- 明确授权一个新的 target-scoped capture producer trigger（这会改变 runner/solver target 架构，可能需要 Advisor）。
