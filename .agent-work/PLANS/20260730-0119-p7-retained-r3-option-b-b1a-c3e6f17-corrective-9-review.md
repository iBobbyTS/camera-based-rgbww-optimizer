# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9：C9 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md` (C9)

**Reviewed execution handoff:** Orchestrator 提供的 C9 terminal evidence；`.agent-work/EXECUTION_RESULT.md` append 为 `0`

**Decision:** `REJECTED_JS_BASE64_ENCODER_UNAVAILABLE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-10`

## Reviewed scope and frozen evidence

本轮仅离线 Planner 审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C9 terminal evidence 与 C8 archive。未访问代码、测试、controller、source、release、retained R3、`.env`、外部路径、网络、相机、Ray120c、strip 或任何设备；未执行 Git mutation。

- C9 唯一 `functions.exec` 在 JS payload 生成层报 `TextEncoder is not defined`；`exec_command` 未被调用，Python 未启动。
- 因此 qualification=`0`、`.agent-work/EXECUTION_RESULT.md` append=`0`；artifact/path/old-root/retry=`0/0/0/0`，禁止后继调用=`0`。
- C9 没有运行 newline、marker、strict-JSON、required-subset-12、owner 或 zero-budget-19 gate，不能据此推断这些 gate 的 PASS 或 FAIL。
- C9 未改变 `RETAINED_UNVALIDATED_UNCONSUMED`，未授权 path probing、bootstrap、release、R3、正式实验或设备操作。
- C9 前置 C8 archive：`.agent-work/PLANS/20260730-0125-p7-retained-r3-option-b-b1a-c3e6f17-corrective-8-review.md`；SHA-256 `c10aa54dddadc8acddfbda64bbefe1d8f6bff1a231f3eda391d3b358af22d146`。
- C9 reviewed PLAN SHA-256：`ef5543df11a1e54b0bcd270ffb8c821d3e83823c1968bed9c6694c269eaa3632`；只读 FULL SHA-256：`b569f511a9d49881ae13b791d275f723bdb26e5062971fda50bbbcc939a7a7b8`。

## Planner findings

1. C9 是 JS host 缺少 `TextEncoder` 的 invocation-layer failure；明确拒绝为 `REJECTED_JS_BASE64_ENCODER_UNAVAILABLE`。
2. C10 只修复 base64 encoder：qualification Python source 必须纯 ASCII；JS 仅可使用当前环境可用的 `btoa(source)`，或手写纯 JS base64 encoder。禁止 `TextEncoder`、`Buffer`、Node API 与额外工具调用。
3. Python invocation 继续固定为简单 `python -c` base64 wrapper 加单一 payload；不得 heredoc、template literal、dispatcher、shell eval、子进程或把 qualification source 直接嵌入 shell 引号。
4. C9 的 exact terminal-newline policy、PLAN marker line 17、FULL marker line 21、required-subset-12、zero-budget-19、gate-before-path、PASS/FAIL 最多一次 ER append 以及全部后继锁原样保留。

**Residual risk and exact next branch:** C10 仍可能在 JS encoder 或 direct command invocation 层失败；任何失败均以一次 terminal handoff 或一次 ER append 停止，不得 fallback/retry。下一分支仅执行 C10 离线 contract qualification，不执行 package。

**维护性判断：** 只替换调用前的 base64 encoder 合同，既有 gate、ownership 与安全边界不变；不触碰生产模块、测试或外部执行包，不引入共享抽象。
