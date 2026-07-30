# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-8：C8 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md` (C8)

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，C8 handoff

**Decision:** `REJECTED_COMMAND_QUOTING_FAILURE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9`

## Reviewed scope and frozen evidence

本轮仅离线 Planner 审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C8 evidence 与 C7 archive。未访问代码、测试、controller、source、release、retained R3、`.env`、外部路径、网络、相机、Ray120c、strip 或任何设备；未执行 Git mutation。

- C8 的首个 direct `exec_command` 在 zsh 层报 `unmatched \"`；Python 未启动。
- 因此 qualification=0、EXECUTION_RESULT append=0；artifact/path/old-root/retry=`0/0/0/0`，禁止调用计数为 `0`，无后继调用。
- C8 未产生可接受的 qualification 结论，也未改变 `RETAINED_UNVALIDATED_UNCONSUMED` 或任何授权边界。
- C8 前置 C7 archive：`.agent-work/PLANS/20260730-0110-p7-retained-r3-option-b-b1a-c3e6f17-corrective-7-review.md`；SHA-256 `3ca7244319c2823bc96519645a83fd434bec14ba334e15fa1fd4341d9336ff78`。
- C8 reviewed PLAN SHA-256：`b8057a0b22331633313552a14f6aee30424467545add2134a7ae8223cb690cc0`；只读 FULL SHA-256：`5e8679526db21743d78776e0b334077239ec89e3acaf0f46beb5fec6f655af4d`。

## Planner findings

1. C8 是 command-quoting invocation-layer failure，不是 newline、marker、JSON、owner 或 budget gate 的证据；拒绝 C8。
2. 零副作用与未启动 Python 的事实保留，但不授权 retry、path reuse、bootstrap、release、R3、正式实验或设备操作。
3. C9 只修复命令传递方式；必须使用无 shell 引号风险的 single direct command（推荐以 Python 内计算 base64 后作为单一参数传给 `python3 -c`，或直接调用已存在的只读标准库 entrypoint），禁止 heredoc、嵌套引号、反引号、shell eval、二级 dispatcher 与额外命令。

**维护性判断：** 仅替换 Executer 调用层合同并保留既有离线 gate；不触碰生产代码、设备 owner、测试或外部执行包，不引入共享抽象。
