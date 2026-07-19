# P7-R0K executable exhaustibility contract

- 状态：resolved_offline_waiting_for_planner_acceptance
- 基线：`16f47c1`
- 范围：仅 exhaustion path contract、n=3/n=5 不可达性和 readiness；未访问设备、网络、`.env`、firmware 或 P7-R1 execution。

## 根因与 Planner 决定

`physical.pre_capture_denial` 曾被误标为 production-reachable。冻结预算满足普通点 `67 = 54 + (10 - 1) + 4`、n=5 点 `75 = 62 + (10 - 1) + 4`；两个 start 的 logical categories 用满时 physical cap 也恰好用满。solver 在调用 capture callback 前先消费 start logical budget，所以没有第 55/63 个正式 target observation 能抵达 physical remaining precheck。

Planner 在 8.7.44 冻结该 path 为 `guarded_unreachable / not_emitted`，拒绝新增 target-scoped producer；remaining precheck 仅作为 defense-in-depth 保留。

## 修复与证据

1. runner canonicalizer 与 public analyzer 都从共享 stable path contract 拒绝 guarded exhaustion；内部自洽双 ledger 也不能成为 completed-target evidence。
2. n=3 与 n=5 production-state-machine tests 分别用满两个 starts、首轮 10 张 auto-exposure 和 4 张 weak reacquire allowance，证明 `54/67`、`62/75` 后下一 solver 请求在 callback 前被 logical gate 拒绝。
3. `logical.feedback_attempts` 与 `logical.confirmation_groups` 保留真实 solver -> runner persistence -> public analyzer 回环。
4. physical、auto-exposure、weak-reacquire 的 post-capture overrun 均形成 run-level `physical_budget_accounting_violation`，保留非空 CR3 和 Python cleanup。
5. readiness 对每个 stable path 记录最终 classification 和 evidence type；physical pre-capture 明确只有 producer-unreachability + runner/analyzer rejection，production success round-trip 为 false。

## 早期失败与修正

首次 guarded-path public test 暴露 phase-family regex 与 `fullmatch` 不一致：`probe-ww`、`prediction-rebase-2-ww` 等被仅允许一个尾随连字符的 pattern 错拒。修复为完整前缀族后，全部 guarded path 均由 classification fail closed。
