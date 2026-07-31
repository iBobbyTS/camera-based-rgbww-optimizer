# REF-P7-25-R2-B2-P4-C1-C1 activation provenance disposition review

**归档时间：** `2026-07-31T13:32:33-0600`

**归档类型：** Planner stop 已由 Orchestrator disposition 解锁；归档后进入 validation-only successor。

**Reviewed reference task：** `REF-P7-25-R2-B2-P4-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-ACTIVATION-PROVENANCE-DISPOSITION-STOP-V1`

**Reviewed PLAN identity：** bytes `4400`，SHA-256
`3cda6f5f7a90f0f088ae2e5004a9d8f5458c6ba518bd38eae49e69a4c5fc08f2`。

## Reviewed scope

上一 active PLAN 是无 Executer dispatch 的 Planner stop。它冻结了两项 finding：

1. activation commit `48adfd669dc8d49fe11c983a4ca36e928bef6c22` 的真实 subject 是
   `chore(plan): activate p4 transport domain correction`，而原 P4-C1 PLAN 预期的是多出 `owner` 的 subject；
2. evidence commit `bd9d205cf7a4385d202666f87d225739e57c970c` 中新追加的 Executer handoff 把真实
   activation subject 误写成预期 subject，并因此错误声称 activation gate passed。

该 stop 禁止 code/test/ER 写入、外部 controller/source/root、synthetic integration、retained R3、real B2、
canonical validator、eligibility、release、网络、设备与科学阶段，等待 Orchestrator 决定是否允许不改历史的 bounded
provenance disposition。

## Evidence reviewed

- P4-C1 review archive：
  `.agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md`，
  bytes `21675`，blob `ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd`，SHA-256
  `d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd`。
- Rejected activation：`48adfd669dc8d49fe11c983a4ca36e928bef6c22`，parent
  `781e410c43774c20da9f00e8c9e0f5bfd27b1f66`，真实 subject
  `chore(plan): activate p4 transport domain correction`。
- Retained implementation：`0ec12f2de91b84f4379d64437170fa53c3ae4a28`，parent 为上述 activation，subject
  `fix(p7): own retained controller transport domains`，exact two changed paths。
- Misstated evidence prerequisite：`bd9d205cf7a4385d202666f87d225739e57c970c`，parent 为上述 implementation，subject
  `chore(evidence): record p4 transport domain correction`，changed path 仅
  `.agent-work/EXECUTION_RESULT.md`。
- Planner rejection：`dfc2ed4d646e7c1a284c075810ae1424a3272504`；Orchestrator disposition：
  `1e63d808af45424f51ff0784955c95eccf4c3230`。
- Final source blob/SHA-256：`1868ad4b4446defcc6d8187ea21d18ccf128fa31` /
  `6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745`。
- Final dedicated-test blob/SHA-256：`25eafb91d7794d4510c9d7da34f1d8666ab1ff55` /
  `e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72`。

## Planner decision

`ACCEPTED_ORCHESTRATOR_NON_REWRITING_VALIDATION_ONLY_DISPOSITION`。

Orchestrator 已在 `1e63d808af45424f51ff0784955c95eccf4c3230` 冻结唯一非改写路线：保留全部历史提交，
把 `bd9d205...` 作为含错误 activation-subject 陈述且必须被 successor 明确 supersede 的 evidence prerequisite；
只读重放真实 Git/file identities，随后只允许向 ER 追加一次 truthful supersession record 并创建一个单文件 focused evidence
commit。该路线不把原 P4-C1 合同重解释为通过，也不重新运行或扩大 implementation validation。

## Residual risks and exact next branch

- 新记录必须只 supersede `bd9d205...` 中的 activation subject / activation-gate assertion 以及由它派生的 P4-C1 PASS
  disposition；不得声称旧 ER 全部无效，也不得改写其测试事实。
- Implementation 的既有 validation facts 可如实引用，但不等于原 P4-C1 contract accepted，不产生 retained、validator、
  eligibility 或 release authority。
- 任一 commit/parent/subject/path/blob/SHA/archive identity 不匹配都必须在任何 ER 写入前 hard fail。
- Exact next branch：`REF-P7-25-R2-B2-P4-C1-C1` validation-only provenance closure；失败时仅允许新的 bounded
  offline evidence correction，不返回代码实现或外部 integration。

维护性判断：该 disposition 只修复证据真相，不新增 analyzer、transport owner、manifest owner 或执行框架。
