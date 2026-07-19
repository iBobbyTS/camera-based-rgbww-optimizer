# P7-R0J production round-trip

- 状态：resolved（离线 producer/runner/analyzer round-trip 完成，等待 Planner 验收）
- 基线：`719d28a`
- 范围：正式 solver → runner persistence → public analyzer 的离线 round-trip；禁止设备、网络、`.env`、firmware 与 P7-R1。

## 已确认事实

1. `HsiStartBudget` logical exhaustion 只生成 start/phase/sub-budget，缺少 analyzer 要求的 pre-capture 与物理计数。
2. feedback callback 的 physical exhaustion 进入 top-level `budget_exhaustion`，但 nested `budget.exhaustion` 仍为 null。
3. R0I 手工 fixture 证明 analyzer 合同自洽，但没有证明 production producer 能生成同一合同。

## 根因假设

exhaustion evidence 的 owner 分裂在 start logical budget、target physical budget和 multiseed exception adapter；runner 没有一个 persistence boundary 将它们归一化为 analyzer 所需的 start-scoped 或 target-scoped结构。

## 结果

- runner finalization 是唯一 canonical enrichment owner；logical 使用 start counters，physical denial 使用 target counters。
- production feedback/backtrack exhaustion 已通过真实 solver、正式 runner persistence 和 public analyzer。
- physical sparse producer schema 已 canonicalize 为 target scope 双 ledger；adapter 事后超限改为 fatal `physical_budget_accounting_violation` 并保留 cleanup/evidence。
- exhaustibility matrix 明确 production-reachable、guarded-unreachable 和 fatal accounting 分支；删除 R0I 手工五类成功 fixture。
