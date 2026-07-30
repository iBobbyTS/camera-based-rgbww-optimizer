# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5：C5 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，`F17 corrective-5 qualification` section

**Decision:** `REJECTED_C5_CONTRACT_QUALIFICATION`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6`

## Reviewed scope and frozen evidence

本轮仅离线审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C5 execution section 与最近 Planner archives。未读取代码、测试、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径；未访问网络、相机、Ray120c、strip 或任何设备；未进行 Git mutation。

- PLAN raw SHA-256（C5 执行报告）：`0a0620853ad6003027bcbe66ded8765a36c3898b900b4584ecdbed93697040f7`。
- FULL raw SHA-256（C5 执行报告及当前 raw）：`95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6`。
- candidate 计数首失败：PLAN `2`（lines `15,27`），FULL `3`（lines `701,737,2378`）；首失败阶段为 `candidate_counts`。
- `required_subset_12` parsed count=`0`，未形成可逐键重放的冻结对象。
- `zero_budget_fields` count=`19`，但 `all_zero=false`；字段集合与值未构成 Executer 可重放的唯一全零对象。
- wrapper/strict/no_forbidden=`false/false/false`；artifact/path/old-root/retry=`0/0/0/0`；ER append 恰好一次；未触碰设备/网络/Git。

## Planner findings

1. **拒绝 candidate marker 计数。** C5 将正文叙述中的 `candidate` 词（包括历史架构说明和 review 文字）与 machine row 混为候选，导致 PLAN/FULL 计数分别为 `2/3`，在真正 wrapper/JSON gate 前失败。候选必须只由“物理行首 + 单行反引号包裹 + exact JSON object”这一 canonical row 谓词产生；正文的 JSON/schema/示例或 marker 字符串不得进入计数。
2. **required subset 未冻结为可重放输入。** C5 的 `required_subset_12` 为空，无法证明 12 个键、每个期望值、键集合唯一性及 PLAN/FULL 绑定；Executer 不能从自然语言、嵌套说明或别名推断这些值。
3. **zero-budget 未冻结为可重放输入。** 虽解析到 19 个字段，但 `all_zero=false`，且字段集合和值不是一个唯一 JSON object；因此不能证明全零锁，也不能把报告中的计数解释成实际预算。

零 artifact/path、零禁止调用与一次 ER append 只证明 fail-closed 的副作用边界，不能抵消 machine contract qualification 失败。`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变；C5 不授权 bootstrap、release、R3、正式实验或设备。

## Evidence limits and stop

C5 是不可接受的 pre-path contract rejection；不得重试、复用或触碰旧 root。下一包只能修正 scanner 与两个冻结 JSON owners，保留 direct one-shot、path-before-gate、PASS/FAIL 一次 ER append、全零锁及 Planner stop。

**维护性判断：** 纠偏仅限 PLAN 的离线 machine-contract 边界；不触碰生产代码、设备 owner 或测试路径，不引入新共享抽象。C6 通过后仍需独立 Planner 验收，不能据此解锁后续阶段。
