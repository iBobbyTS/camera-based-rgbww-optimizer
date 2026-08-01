# P7 retained-R3 Option B：R2-R1-C1 typed-evidence failure 与 non-EOF handoff 验收

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C1-TYPED-PARSER-CORRECTED-GIT-SEAM-REAL-SELF-CHECK-V1`

**Activation：** `e2cf73d282d57b35894dfb5a239d711a81f90523`

**Evidence commit：** `cdf3bbc47bc95075747d1cc4d4b3baa2ea5a9c59`

**Planner decision：** `REJECTED_PRE_EFFECT_TYPED_EVIDENCE_FIELD_ASSUMPTION_AND_NON_PHYSICAL_EOF_HANDOFF`

## 1. Reviewed scope 与拓扑

本轮只读审核 committed Git、active PLAN/FULL、上一review archive与ER；未读取real inputs、retained R3 artifacts、old/fresh roots、owner source/test或GUIDE，未运行tests、CodeGraph、self-check、validator、release、network或device工具。

- Activation是`1475952415757f45daa53c4b14f6c3c53eac2d63`的direct child，subject exact `chore(plan): correct typed parser consumption`，changed paths exact为FULL、PLAN及`.agent-work/PLANS/20260801-1239-p7-retained-r3-r2-r1-typed-contract-review.md`。
- Evidence是activation direct child，subject exact `chore(evidence): record typed-parser corrected real self-check`，changed path exact仅`.agent-work/EXECUTION_RESULT.md`。
- Activation ER identity为bytes `1464275`、SHA-256 `0594478104bfbec7ea5ef77cde71ae731e253c11a56d62ed9afef52fc5ee812f`、blob `8ba53e60b93bfbe84ae92ba3de969b72b9d62baa`。
- Evidence ER identity为bytes `1467231`、SHA-256 `beaf989c2ad59a31dd62a68fabfe2a851b3a51396dc967308d022382da72a18a`、blob `f5f30897330b72c24cadd73b075d7576245ad977`；Planner接手时worktree clean。

## 2. Typed-evidence failure 判定

Executer按合同使用raw exact bytes、两个accepted helper、`.value`与`.evidence`，但在typed evidence核对中读取并不存在于accepted `MachineContractEvidence` interface的`whole_line_backtick_count`，触发`AttributeError`。这是调用层臆造typed字段，不是repo-owned parser owner或self-check owner缺陷。

失败发生在activation typed gate内：owner source/test context、patch、tests、compileall、CodeGraph、implementation commit、fresh source/root、14 physical inputs、8 Git acquisitions、18-ledger与self-check owner调用全部为`0`。因此R2-R1-C1不能获得owner correction、validation或real self-check完成信用；本轮也不得直接重试该owner/self-check路线。

## 3. Counter deviation 与 handoff 判定

PLAN只允许complete typed gate之后执行唯一pre-edit status，typed gate失败时该计数必须为`0`。ER却记录`pre_gate_status_checks=1`，所以存在一次额外只读status观察。该偏差不改变pre-effect与clean结论，但必须作为canonical failure facts保存；不能把它重标为合同允许的pre-edit status。

Evidence payload声称heading index、complete-last-section-to-EOF extraction、唯一append及postappend `0`，但Git diff实际把六行section插入旧文档第38行之后，当前heading位于约line `41`。Evidence ER的physical EOF仍是更早的`R2-R1 activation typed-contract failure` section，并以closing fence和LF终止。因此R2-R1-C1 handoff不是physical EOF，`append_is_final_operation`与`strategy`自述不能替代物理位置证据。

Typed failure事实可从committed evidence重放，但其位置不canonical。下一步必须先做Git/ER-only physical EOF supersession；不得删除、移动、修复或再解释旧non-EOF section。

## 4. Locks、residual risk 与 exact next branch

Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。Owner correction、fresh real self-check、real inputs、canonical validator、eligibility、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部继续锁定。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C1-S1`，仅对`cdf3bbc`中位置错误但可重放的typed failure facts做physical-EOF canonical supersession，并明确旧section为`NONCANONICAL_POSITIONED_HISTORICAL_EVIDENCE`。只有该supersession经Planner接受后，Orchestrator才可另行决定新的typed-interface owner/self-check successor；本包不得把不存在字段换成另一组猜测后重试。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C1_S1_PHYSICAL_EOF_SUPERSESSION_WAITING_ORCHESTRATOR_ACTIVATION`。

维护性判断：拒绝点限于调用层typed字段假设与ER位置治理；最小后继只修证据位置，不改production/test/owner，也不新增抽象。
