# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3：调用层语法失败验收

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** Executer handoff；本轮未追加 `.agent-work/EXECUTION_RESULT.md`

**Decision:** `REJECTED_INVOCATION_LAYER_SYNTAX_FAILURE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4`

## Reviewed scope and frozen evidence

本次仅做离线 Planner 验收。唯一 direct `exec_command` 在调用层 JavaScript 封装阶段抛出
`SyntaxError`；Python 未启动，Terminal 未启动，Executer 未进入 PLAN 的 marker/strict-JSON gate。

- terminal 结果：`FAIL`；首次且唯一 invocation 为调用层语法失败。
- `.agent-work/EXECUTION_RESULT.md`：本轮未 append（`append=0`），因此无独立 ER 原文或 ER hash。
- artifact/path：`0/0`；无 root、artifact、fallback 或 path identity 可供复核。
- old-root-touch/retry：`0/0`；无后继调用、禁止操作或重试。
- controller/source/test/Git/release/network/`.env`/device/camera/Ray/strip：均未启动或访问。

证据限制：上述计数来自 Executer handoff 而非成功写入的 ER；本轮不能证明 C3 的 marker、strict-JSON、owner、path-before-gate 或单次 append 合同已执行，只能确认证据链在调用层即终止。

## Planner findings and validation quality

1. 失败发生在 Python 进程创建前，根因是 direct `exec_command` 调用的 JavaScript 封装语法错误；这不是 C3 业务 gate 的 pass/fail 结果。
2. 未观察到任何 path operation 或副作用，但因 ER 未 append，`0/0` 属于 handoff 声明，不能升级为 conforming C3 evidence。
3. C3 被拒绝；不得重试该 invocation、复用其任何 candidate/root、补写或推断缺失的 ER，也不得进入 bootstrap、controller、R3、release、network 或 device。

## Residual risk and stop

在调用层封装能稳定启动单个 Python 标准库脚本前，无法审计 C3 的唯一 marker/owner 或 path-before-gate 合同。`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变，FULL 不在本归档中修改。

## Exact next branch

下一 active PLAN 仅允许一次 CORRECTIVE-4：修正 direct `exec_command` 的调用层封装，避免 JavaScript 内嵌复杂 heredoc/转义；仍必须由 direct `exec_command` 启动单个 Python 标准库脚本，不得增加二级 dispatcher。脚本只执行 C3 规定的唯一-marker owner audit，保留相同 unique-marker、owner-binding、path-before-gate、zero-budget、PASS/FAIL 单次 ER append 后 stop 合同。不得执行 package、修改代码/测试/GUIDE/FULL、访问旧 root 或任何设备/网络资源。

