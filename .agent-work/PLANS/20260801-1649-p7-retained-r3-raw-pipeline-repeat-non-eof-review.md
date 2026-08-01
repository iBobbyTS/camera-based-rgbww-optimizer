# P7 retained-R3 Option B：raw-pipeline repeat non-EOF review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-RAW-PIPELINE-PHYSICAL-EOF-FIXED-MATRIX-CORRECTIVE-SUPERSESSION-V1`

**Activation：** `cafa54453c740d62beb83e1f7a48363ccd3c9852`

**Evidence child：** `5e7e91e35f7c72d460c0aa5c6852847cb19372ef`

**Decision：** `REJECTED_ATOMIC_ORDER_ZERO_BUDGET_VIOLATIONS_AND_HANDOFF_NOT_AT_PHYSICAL_EOF`

## 1. Reviewed scope and immutable identities

- Activation direct parent：`e56b09af4b6d375ecce5f1f26531cbb5dd68dd0c`；subject exact `chore(plan): seal raw-pipeline EOF correction`；changed paths exact为FULL、PLAN和`20260801-1636` archive。
- Activation committed PLAN：`17902` bytes / SHA-256 `d7a163a0c324211f5333f4b7f505031bd9e3696b30bdeb906b5abd80308b8b47`。
- Activation committed FULL：`466261` bytes / SHA-256 `7d1dc40249540cbd716f7933b2042b3eef37de3825f422c52e88d770b20489ef`。
- Activation committed ER：`1555130` bytes / SHA-256 `27a5f4adea3bc7d73f5e743cd2b4b701ae564bee818da48c3af888b9cd78e352`。
- Evidence child direct parent为activation，subject exact `chore(evidence): seal raw-pipeline EOF supersession`；changed path只有`.agent-work/EXECUTION_RESULT.md`。
- Evidence ER：`1559501` bytes / SHA-256 `7b771a53aec9b06588398cfa536a8829979759ffc26b73966a01583f5b8ed69b`；当前worktree ER与该Git object exact一致。
- `git diff --check cafa544..5e7e91e`通过；PLAN、FULL、archive、代码、测试、skill、docs与GUIDE均未被Executer修改。

## 2. Accepted-parser success but contract rejection

同一个local process确实从activation Git objects捕获PLAN/FULL raw stdout bytes，并直接交给accepted parsers各一次；PLAN/FULL parser calls为`1/1`，其source identities分别与activation的`17902`/`466261` bytes及上述SHA-256一致。

但是在合同允许的原子序列之外，Executer已经发生CodeGraph query `1`、repository test direct read `1`、agent-work searches `2`、worktree ER partial searches `2`、ER recovery read `1`、worktree ER exact reads `2`和retry `1`。这同时违反`codegraph=0`、repository test reads `0`、searches `0`、retry `0`及唯一ER读取预算，且activation metadata没有在parser acquisition前完整验证。因而即使accepted parsers成功，也不能进入fixed report/matrix acceptance。

Report/seal reads为`0/0`，strict loads为`0/0`，matrix freezes/structural checks为`0/0`。Controller、selector、ledger Git、validator、tests、compileall、network与device effects均为`0`。Synthetic engineering attribution facts不接受；production owner、lineage、eligibility与release均为`false`，retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Independent physical-EOF finding

Evidence记录声称以true physical EOF append，但Git blob反证如下：

- 新heading `D2-C1-R2-C1-S1-C1-C1-C1-C1-C1 raw-pipeline physical-EOF corrective fail-closed supersession`起始byte offset为`1546782`；其record占`4370` bytes（连同分隔newline形成本次`4371`-byte diff）。
- 从新heading到current physical EOF仍有`12719` bytes；因此该记录不是EOF append。
- preserved old tail heading当前位于offset `1555430`；从该heading至physical EOF exact `4071` bytes / SHA-256 `b91a59124220413e1f6037fb8429af934fdf1b53ebd048ab27141c42bd0bf62e`。
- Current evidence ER不是activation ER的prefix extension。新增non-EOF记录与其后完整old tail都必须原样保留，但新增记录不能获得terminal/durable handoff信用。

## 4. Validation quality and decision

本次评审使用activation/evidence Git topology、changed paths、committed blob byte/SHA identities、exact diff、heading offsets、完整physical tail identity与worktree/object equality完成独立复核。未重跑controller、selector、ledger、tests、validator或设备操作，也未读取外部report/seal。

结论为拒绝：`REJECTED_ATOMIC_ORDER_ZERO_BUDGET_VIOLATIONS_AND_HANDOFF_NOT_AT_PHYSICAL_EOF`。Parser成功事实可保留为historical evidence，但不能抵消前序零预算违规；原合同与synthetic engineering attribution均不接受。

## 5. Residual risks and exact next branch

下一包只做最小physical-EOF failure supersession，不读report/seal，不做matrix，不重复parser，不做任何探索。它冻结evidence ER完整identity以及真正EOF的完整`4071`-byte tail anchor，使用该完整tail作为唯一`apply_patch`上下文，把一条bounded failure supersession写在真正EOF；`apply_patch`必须是唯一写操作和最后操作。

Report/seal/`$.matrix`留给该physical-EOF封存被Planner接受后的独立后继包。这样不会再把EOF可追溯性与matrix读取绑定为同一失败面。

Exact next branch：`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1`，`MINIMAL_PHYSICAL_EOF_FAILURE_SUPERSESSION`。
