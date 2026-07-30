# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-10：C10 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md` (C10)

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，C10 section lines 16160-16181

**Decision:** `REJECTED_INPUT_OWNER_BINDING`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-11`

## Reviewed scope, implementation method, and frozen evidence

本轮仅离线 Planner 审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C10 execution section 与 C9 archive。未访问设备、网络、`.env`、release、retained R3、代码、测试、controller、source 或外部路径；未执行 Git mutation，也未执行 C10/C11 qualification。

- C10 使用 manual ASCII base64 wrapper 成功生成 payload，固定 Python wrapper 已启动并完成，且仅向 `.agent-work/EXECUTION_RESULT.md` append 一次。
- reviewed PLAN SHA-256：`cc344ac8fc0a7a26df9abd342a9cddca17d6031133483554d16829a281dd393d`；只读 FULL SHA-256：`679320e07bb9e28f025a82a662772467d343253cef22b164fc6f333c2eeeda96`。
- C10 review 时 `.agent-work/EXECUTION_RESULT.md` SHA-256：`ecfa6fccd51153465d1adffbc910a6518e0be6b4c6018877c471193ac6215ae4`；C10 evidence 位于 lines 16160-16181。
- C10 的 PLAN/FULL raw SHA、`required_subset_12=12/12`、task lock、contract lock、FULL SHA lock、retained lock 均报告 PASS；artifact/path/old-root/retry=`0/0/0/0`，禁止调用为 `0`。
- 唯一 terminal failure 是 `zero_budget_fields19=0/19`；terminal=`FAIL`，append 后立即 stop，无 fallback 或 retry。
- `line21_hex` 解码为 C10 PLAN 第 21 行以“Executer 只能构造一份纯 ASCII qualification Python source”开头的 action prose，而非绝对路径 `.agent-work/FULL_PLAN_REFERENCE.md` 的第 21 行 `FULL_PLAN_MACHINE_STATE` row。这证明第二输入及 line owner 被错误绑定到 PLAN bytes。
- C9 review archive：`.agent-work/PLANS/20260730-0119-p7-retained-r3-option-b-b1a-c3e6f17-corrective-9-review.md`；SHA-256 `142c0b20aabed9731cccbc66b76f3121a1fc36c37bdd09a00569e5d292fb1092`。

## Planner findings and validation quality

1. C10 明确拒绝为 `REJECTED_INPUT_OWNER_BINDING`。失败根因是 PLAN/FULL raw bytes 与 line arrays 未保持独立 owner，不是 ASCII base64 transport、Python wrapper、marker 合同或冻结的 19 项 zero-budget object 本身失效。
2. C10 对 raw SHA、PLAN candidate 与 PLAN-derived gates 提供了可用证据；但因 FULL line 实际来自 PLAN buffer，所有声称依赖 FULL candidate 的语义结果都不构成独立 FULL owner 证明。`required_subset_12=12/12` 不能覆盖这一 provenance 缺陷。
3. C11 只修复输入 owner：必须从两个冻结绝对路径分别读取两个独立 raw byte buffers；`plan_lines` 只能由 PLAN bytes 派生，`full_lines` 只能由 FULL bytes 派生，禁止变量复用、赋值替换或从另一 owner 的 lines 取候选。
4. FULL candidate 与 FULL-owned state fields 必须只从 `full_lines` 中唯一 `FULL_PLAN_MACHINE_STATE` object 解析；PLAN `zero_budget_fields` 必须只从 `plan_lines` 中唯一 `PLAN_MACHINE_CONTRACT` object 解析，然后按 machine contract 冻结关系逐键、逐值、逐类型验证。
5. ASCII base64 wrapper、exact LF/marker、12/19、path-before-gate、PASS/FAIL 至多一次 ER append、artifact/path/old-root/retry 全零与全部设备/release/R3 后继锁原样保留。

## Residual risks and exact next branch

C11 仍可能因 Orchestrator-owned FULL 尚未激活 C11 或冻结 SHA 未同步而在 dispatch gate 前被阻断；这只能由 Orchestrator 更新 FULL、再由 Planner 同步冻结 C11 PLAN 的 exact FULL SHA，不能由 Executer解释或绕过。除此之外，唯一允许的下一分支是 C11 离线 input-owner qualification；不得 bootstrap、访问 release/R3、运行代码或测试、访问设备/网络/`.env`，也不得 fallback/retry。

**维护性判断：** 纠偏仅收紧 qualification 输入 owner 与 provenance 边界，不触碰生产模块、测试或外部执行包，不引入共享抽象。
