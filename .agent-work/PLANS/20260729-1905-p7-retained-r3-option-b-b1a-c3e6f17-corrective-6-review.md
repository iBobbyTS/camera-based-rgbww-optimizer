# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6：C6 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，`F17 corrective-6 qualification` section

**Decision:** `REJECTED_C6_SCANNER_SEMANTICS_MISMATCH`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-7`

## Reviewed scope and frozen evidence

本轮仅离线审计；读取 AGENTS.md、camera-based-rgbww-optimizer skill、当前 PLAN/FULL、C6 execution section 与最近 C5 review archive。未读取代码、测试、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径；未访问网络、相机、Ray120c、strip 或任何设备；未进行 Git mutation。

- PLAN raw SHA-256（C6 execution report）：`b1acac5eb1a343d82d851575cff39f3048707d26789ee8fff6fabee414e68938`。
- FULL raw SHA-256（C6 execution report及当前 raw）：`61ba86f43525beb66f3a7dba8e0f7194445bc50e02b142b31f76262f5358a066`。
- C6 terminal=`FAIL`；candidate counts reported PLAN=`0`, FULL=`0`, lines empty；`required_subset_12=false`, `zero_budget_fields=false`, `wrapper_contract=false`；first failure=`candidate_count`。
- artifact/path=`0/0`；old-root/retry=`0/0`；forbidden calls=`0`；ER append once；HEAD read-only observation=`7fbf976945794926f3f8462a4c44af4f59c20841`。
- Exact raw line inspection: PLAN line 17 and FULL line 21 each contain one physical line beginning with a backtick, then the required prefix and a JSON object, and ending with one backtick followed by LF. Neither line has leading whitespace, CRLF, or trailing bytes.

## Planner findings

1. **拒绝 C6 candidate=0 结论。** C6 scanner 与 PLAN 的 `canonical_wrapper` 语义不一致：两个实际 machine rows 都满足物理行字节、`startswith(b"`")`、去 LF 后 `endswith(b"`")`、内层 prefix 和 JSON slice 条件。C6 的空候选结果不能证明 rows 缺失，反而证明 scanner 没有按冻结 wrapper 语义提取。
2. **拒绝 C6 gate 结果。** 由于候选未提取，required subset、zero-budget、wrapper 与 contract gate 均未获得有效输入；这些 FAIL 不能被解释为 PLAN/FULL 内容的真实不一致。
3. **保留副作用边界。** C6 的零 artifact/path、零 old-root/retry、零 forbidden calls 与一次 ER append 仍是有效的 fail-closed 证据，但不抵消 scanner qualification 失败。

## Exact corrective contract

C7 必须冻结一个可直接重放的 marker extraction algorithm，Executer 不得自行设计 scanner：逐行保留 raw bytes（含 LF），仅接受同时满足以下条件的唯一 rows：`line.startswith(b"`")`；去除且仅去除行尾一个 `b"\n"`（若有 `b"\r\n"` 则拒绝）；去 LF 的 line 以 `b"`"` 结尾；内层字节以精确 PLAN/FULL prefix 开始；去 prefix 后首尾正好是 `{`/`}`，对该 JSON slice 做 `json.loads`；要求结果为 object，且整行除首尾反引号与 LF 外无其他字符。逐路径记录 candidate line numbers/counts，并只对唯一 row 解析。required_subset_12 与 zero_budget_fields 继续逐键、逐值、逐类型比较唯一 JSON objects，不得自然语言推断；保留 direct one-shot、path-before-gate、PASS/FAIL 一次 ER append、全零锁。

`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变；C6 不授权 bootstrap、release、R3、正式实验或设备。

**维护性判断：** 仅修正 Planner machine-contract 的 scanner 交接语义和冻结输入；不触碰生产代码、设备 owner 或测试路径，不引入共享抽象。C7 通过后仍需独立 Planner 验收。
