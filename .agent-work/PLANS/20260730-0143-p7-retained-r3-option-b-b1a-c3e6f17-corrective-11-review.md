# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-11：C11 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`（C11，SHA-256 `d1c548e57d2fb118c30a6b0ce15147db6cc2cad7ea6cadbf10daa1121f3ddbf9`）

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md` lines 16184-16242；review 时 SHA-256 `35aa718b1666f0c640b1db772132ea3e1f4fcb8273a0ab5c149de22cba774270`

**Reviewed FULL:** `.agent-work/FULL_PLAN_REFERENCE.md`（SHA-256 `d089f4b604a9d0307798c4a84f3b63610e13b2364f93e5aace163cafa2a287b6`）

**Decision:** `REJECTED_PLAN_SCANNER_FALSE_NEGATIVE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12`

## Reviewed scope, implementation method, and evidence

本轮 Planner 只读检查 AGENTS.md、项目 skill、当前 PLAN/FULL、C11 execution section 与 C10 archive，并以独立只读 Python bytes parser 复算 SHA、line endings、候选数量和 strict JSON。未访问网络、设备、`.env`、release、retained R3、candidate、controller、source 或外部 evidence root；未运行测试、qualification、public analyzer 或 Git mutation。

- Executer 通过单一 ASCII-base64 wrapper 启动 C11 qualification，命令退出码 `1`，向 `EXECUTION_RESULT.md` append `1` 次后停止，无 fallback/retry。
- Executer 正确观察 PLAN SHA `d1c548e57d2fb118c30a6b0ce15147db6cc2cad7ea6cadbf10daa1121f3ddbf9` 与 FULL SHA `d089f4b604a9d0307798c4a84f3b63610e13b2364f93e5aace163cafa2a287b6`，均与冻结值一致；FULL candidate count 报告 `1`。
- Executer 把 PLAN candidate count 报告为 `0`，因此 PLAN object unavailable，后续 12-key 与 19-key gates 均未建立。
- Planner 独立按 PLAN 冻结的 raw-byte 规则复算：PLAN 共有 `35` 个 raw lines，line 17 以 bytes `` `PLAN_MACHINE_CONTRACT= `` 开始、以 `` `\n `` 结束、无 CRLF、strict JSON object 可解析，唯一候选数为 `1`；FULL line 21 同样是唯一合法候选，候选数为 `1`。
- 独立解析的 PLAN object task/contract 均为 C11；FULL object 的 active task/contract 均为 C11，`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`，`candidate_contract_orchestrator_verified=true`。
- Executer 报告 device/network/camera/Ray/strip/release/retained-R3/test/Git mutation/old-root access 全为 `0`；未提供与此相冲突的 evidence。

## Planner findings and validation quality

1. C11 必须拒绝为 `REJECTED_PLAN_SCANNER_FALSE_NEGATIVE`。冻结输入及 owner 已正确分离，PLAN/FULL 也都真实存在唯一合法 machine row；失败来自 Executer 的 PLAN scanner 实现与冻结字节算法不一致。
2. 因 PLAN object 未解析，C11 的 required-subset 和 zero-budget semantic qualification 不成立；但失败发生在 path/artifact gate 前，未污染 retained R3、release 或设备状态。
3. C12 只纠正 scanner：使用 owner-specific `splitlines(keepends=True)`，marker bytes 必须包括起始 backtick，合法 suffix 必须是 exact backtick+LF，JSON slice 必须是 `raw[len(marker):-2]`。不得用 presentation text、line-number lookup、decode 后模糊匹配、alias 或另一 owner buffer补偿。
4. C12 必须先等待 Orchestrator 把 FULL 唯一激活为 C12，再由 Planner 刷新 exact FULL SHA；在这两个动作完成前不得 dispatch。

## Residual risks and exact next branch

唯一下一分支是 C12 byte-exact scanner qualification。它仍是纯离线、两输入、零 path/artifact package；不解锁 bootstrap、controller/source、测试、Git mutation、retained R3、release、network、device、camera、Ray、strip、formal 或 public analyzer。C12 PASS 也仅证明 qualification contract，不是 package execution 或 eligibility。

**维护性判断：** 本轮只收紧一次性 qualification scanner 的 byte ownership，不触碰生产代码或共享抽象；无需架构重构。
