# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-7：C7 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，`F17 corrective-7 marker qualification` section

**Decision:** `REJECTED_C7_EXECUTOR_NEWLINE_MISJUDGMENT`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-8`

## Reviewed scope and frozen evidence

本轮仅离线 Planner 审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C7 execution section 与 C6 review archive。未访问代码、测试、controller、source、release、retained R3、`.env`、外部路径、网络、相机、Ray120c、strip 或任何设备；未执行 Git mutation。

- C7 ER 报告 terminal=`FAIL`，唯一 reason=`ValueError:missing-LF line 17`；artifact/path=`0/0`，old-root/retry=`0/0`，device/network/release/Git=`0`，且仅 append 一次。
- 直接读取当前 PLAN 原始 bytes（ER append 不改变 PLAN）：物理 line 17 长度 `2258` bytes，首字节为反引号，末四字节为 `}`、反引号、`0a`、EOF-of-line；`endswith(b"\\n")=true`，`endswith(b"\\r\\n")=false`。该行含精确 `PLAN_MACHINE_CONTRACT=` 前缀及 JSON object。
- 当前 PLAN raw SHA-256：`bbb0cbd6c71b4b25a5bfc224187a7918f54610818d24b838b0efa05a9d4fea52`。
- 当前 FULL raw SHA-256：`8c1ccf2c0b5e361980e1c49f27f87425157d34a0869a9e80f44c1172fb898431`；HEAD 只读观察：`274ed9e2bf9fcfd040dc7f5205c5d31ea08eaba5`。

## Planner findings

1. **拒绝 C7 的 missing-LF 结论。** 原始 bytes 明确证明 PLAN line 17 具备单个 LF，且不是 CRLF；Executor 的 terminal failure 与实际冻结输入矛盾，因此 C7 不能作为 marker parser 语义证据。
2. C7 的零副作用、一次 ER append 与停止边界仍有效；它们不授权 retry、path reuse、bootstrap、release、R3、正式实验或设备操作。
3. C8 必须由 Planner 明确冻结最终物理行 newline policy：marker row 必须以单个 `0x0a` 结束；EOF terminal line（无 LF）必须拒绝，CRLF 必须拒绝。Executer 不得自行改变该语义或自创 parser。

## Exact corrective contract

C8 仅执行一次离线 byte-exact qualification：逐行保留 raw bytes，要求唯一 PLAN line 17 与 FULL line 21 均满足首反引号、单 LF 终止（无 LF/CRLF 均 terminal FAIL）、去除该 LF 后末反引号、精确 prefix、JSON slice 首尾 `{}` 且 `json.loads` 结果为 object。required_subset_12 与 zero_budget_fields 仍只接受 machine row 中的唯一 JSON objects，逐键逐值逐类型比较；gate 前 path counter 必须为 0。保留 one-shot、一次 ER append、全零锁与 Planner stop。

`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变；C7 不授权任何 bootstrap、release、R3、正式实验或设备。

**维护性判断：** 仅纠正 Planner/Executer 的字节级交接合同并冻结 newline policy；不触碰生产代码、设备 owner、测试或执行 package 外部路径，不引入共享抽象。
