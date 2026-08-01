# P7 retained-R3 Option B：P1-C1 activation exact-bytes invocation failure Planner 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-IMMUTABLE-EXPECTATION-CORRECTION-V1`

## 1. 冻结输入与 evidence topology

- activation commit：`81019ea94c266e9f69a82a3d985f6397d45041a4`；parent `6a8ae8fcbecb311bfe53c3cc4d13773ef49956be`；subject exact `chore(plan): correct immutable parser expectations`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1204-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-targeted-review.md`。
- evidence commit：`aea9ce3769dea41348d739ee92b36fa2f47889a5`；parent exact activation；subject exact `chore(evidence): record immutable parser correction`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- canonical handoff schema：`p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_c1_immutable_expectation_correction_result_v1`；ER append是Executer最后副作用，Orchestrator已按exact subject/path提交。
- activation machine-row parse前，committed PLAN、FULL、review archive各读取一次，activation topology通过；required FULL subset、pre-edit status与dirty identity核验均未到达。

## 2. 执行事实与 preserved dirty identities

唯一失败发生在activation validation invocation：调用方把`git show`输出解码为text后传入当前exact-bytes parser，owner以`source_not_exact_bytes` fail closed。该失败发生在source/test写入、test correction与任何validation之前：source patch `0`、test patch `0`、targeted/focused/full/compileall/CodeGraph/diff/status/implementation commit/postcommit targeted均为`0`。

Planner独立核对当前worktree仅保留exact two modified paths，且身份与P1-C1 frozen precondition完全一致：

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`：bytes `9414`；SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`；Git blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`。
- `tests/test_agent_work_machine_contract.py`：bytes `13411`；SHA-256 `5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920`；Git blob `5efc93c11b37de900f67b3d1c4aa734048d035fc`。

因此本轮是纯pre-effect invocation error，不构成P1-C1 implementation、test correction、validation或commit尝试。现有P1 source/test contractual dirty implementation没有漂移，也不得由Planner重写、撤销或提交。

## 3. Planner findings 与决定

**Decision：** `REJECTED_P1_C1_EXECUTION_CREDIT_PRESERVE_EXACT_TWO_PATHS_FOR_EXACT_BYTES_SUCCESSOR`。

失败属于调用边界错误：repo-owned parser的exact-bytes合同正确执行，调用方却主动把bytes降格成`str`。不得为适配错误调用而放宽production parser接受text，也不得重新实现machine-row扫描。下一包只允许从Git或`Path.read_bytes()`取得exact bytes后调用当前`parse_plan_machine_contract`/`parse_full_plan_machine_state`；明确禁止`text=True`、`encoding=`、`.decode()`与`read_text()`进入machine-row调用链。

P1-C1原始纠偏范围保持不变：source write exact `0`，dedicated test一次test-only JSON semantic adapter patch，然后从targeted开始完成focused/full、compileall、CodeGraph、exact two-path commit与postcommit targeted。retry与fallback仍为`0`；若exact-bytes activation gate或后续任一步失败，立即封存真实失败，不得修补同一尝试。

这是repository validation invocation纠偏，不是色彩或测量科学问题，不需Advisor。设备、网络、real artifacts、self-check owner、canonical validator、eligibility与release均继续锁定，也不需Human设备授权。

## 4. Residual risks 与 exact next branch

- preserved source/test尚未经过P1-C1计划的test-only correction和全套验证，不能获得实现接受或caller compatibility credit。
- exact-bytes acquisition必须针对activation commit本身，不能读取working-tree PLAN/FULL替代committed activation evidence；archive也必须按committed bytes验证identity。
- machine-row parser本身不得再改；唯一production path仍保持dirty但本包source write为`0`。
- P1-C1-R1接受前，R2 real successor、real self-check、validator、eligibility与release消费继续硬锁。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1`，唯一exact-bytes activation invocation + preserved P1-C1 test-only correction与完整validation package。Planner stop为`B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_EXACT_BYTES_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW`。

维护性判断：本轮不放宽parser API，不增加helper或parallel owner；只纠正调用方bytes边界并沿用原test-only correction，因此single-owner和deep-immutability边界保持不变。
