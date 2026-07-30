# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12：C12 qualification review

**Review date:** `2026-07-30`

**Reviewed plan:** `.agent-work/PLAN.md`（C12，SHA-256 `6cd894ef408a2c0af4b17b4224f02288126be93186463b9096a2ab06086a0b37`）

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md` 的单行 `C12_QUALIFICATION_RESULT` append；review 时 SHA-256 `c4128ff6e9503a1f386c70acc965f1742001a2b917d0bfce60dfb1b71417670c`

**Reviewed FULL:** `.agent-work/FULL_PLAN_REFERENCE.md`（SHA-256 `4149897d26685c65b2dca8ea262c753126c18f0811bc93964fbbebfea91c266c`）

**Decision:** `REJECTED_REPEATED_SCANNER_FALSE_NEGATIVE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13`

## Reviewed scope, implementation method, and evidence

本轮 Planner 只读检查 AGENTS.md、项目 skill、当前 PLAN/FULL、C12 execution append 与 C11 review archive，并以独立 raw-bytes parser 复算 SHA、候选数量、strict JSON 与 owner fields。未访问 retained R3、candidate、release、旧 evidence root、网络、`.env`、设备、相机、Ray、strip 或 public analyzer；未执行 qualification/test/controller/source/Git mutation。

- Executer 记录 C12 terminal `FAIL`、append count `1`、PLAN SHA `6cd894ef408a2c0af4b17b4224f02288126be93186463b9096a2ab06086a0b37` 与 FULL SHA `4149897d26685c65b2dca8ea262c753126c18f0811bc93964fbbebfea91c266c`；两份文件 SHA 均准确。
- Executer 报告 PLAN/FULL candidate count 均为 `0`，required subset 为 `0/0`、zero budgets 为 `0/19`，并以 exit `1` 停止。
- Planner 按冻结 predicate 独立复算：PLAN line 17 是唯一合法候选，raw-row SHA-256 `00834c875225bd339efe6e7e9ec6cd6e069e663f745780af82f1343c8c74da7c`；FULL line 21 是唯一合法候选，raw-row SHA-256 `9b30824d7244ac5aa2be02cc4e2baf246b1a5f0bbd7c74c7b74d01cc4be97608`。两行均以约定 marker bytes 开始，以 hex `600a` 结束、无 CRLF，JSON slice 严格解析为 object。
- 独立 owner 校验通过：PLAN zero-budget fields 为 `19/19` 个 JSON integer zero；PLAN task/contract 与 FULL active task/contract 一致；FULL 保持 `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED` 且 `candidate_contract_orchestrator_verified=true`。
- Executer append 没有记录实际 scanner source/hash、所用 marker bytes、候选 raw-row hash/hex 或逐 owner ledger，因此无法由其 evidence 重放 `0/0` 的具体实现；其 `candidate_counts` 是与冻结输入矛盾的转录/实现结果，而不是输入事实。

## Planner findings and validation quality

1. C12 必须拒绝为 `REJECTED_REPEATED_SCANNER_FALSE_NEGATIVE`。输入、SHA、machine rows 和 owner fields 均有效，失败来自 Executer 临时 scanner；C11 与 C12 已连续出现相同类别 false negative。
2. C12 没有证明 required subset 12/12 或 zero budgets 19/19。失败记录也缺少 scanner executable provenance，不能把手工转录的 `0/0` 当作可审计事实。
3. 不得签发 C13 为另一轮手工 scanner 转录。下一工程分支应建立一个仓库内、可复用、可测试、exact-byte 的单一 owner，并由专用测试覆盖：合法 LF row、CRLF、EOF 无 LF、重复 candidate、错误 prefix/suffix、非-object JSON、PLAN/FULL owner 分离与字段类型。
4. helper 的 exact repository paths、public surface、测试路径、changed-path set、验证命令与 Git scope 属于 Orchestrator 工程所有权。Planner 只建议最小两路径（一个 helper module + 一个 dedicated test），不得自行激活或假定路径。

## Residual risks and exact next branch

唯一下一分支是 C13 engineering activation gate。Orchestrator 必须先确认最小 helper/test 工程范围并把 FULL 唯一激活为 C13；随后 Planner 才能冻结 executable source/hash、changed paths、测试与 evidence contract。当前 PLAN 不授权 Executer dispatch、source/test/Git mutation，也不解锁 bootstrap、retained R3、candidate、release、eligibility、network、device、camera、Ray、strip、formal 或 public analyzer。

**维护性判断：** 连续两次临时 scanner 漂移已满足共享 owner 的引入条件；最小 helper + dedicated test 可消除重复转录，不应扩展到生产实验控制或 provenance eligibility owner。
