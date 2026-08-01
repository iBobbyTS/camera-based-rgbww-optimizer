# P7-I1 synthetic integration acceptance route transition

**归档日期：** `2026-07-31`

**Reviewed reference task：** `REF-P7-25-R2-B2-P7-I1-E1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-C1-AUDIT-DOMAIN-VALIDATION-SUPERSESSION-V1`

**Planner decision：**
`ACCEPTED_COMPLETE_FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。

## 1. Reviewed scope and method

本归档保存已完成的 Planner stop；它不授权重跑 P7-I1。Reviewed evidence 证明 activation/evidence commit
拓扑与 exact path，old ER prefix、single EOF append、strict two-field supersession、physical source/root、exact9 artifacts、
matrix16、terminal/admission 与 retry0 均匹配冻结合同。Data-owner map 保持：旧 ER 独占 process facts 与 success label，
physical source 独占 source identity，physical root 独占 root/canonical/sidecar/matrix/terminal/admission，Git 与 old prefix
独占 topology/EOF delta。

## 2. Evidence and validation quality

- activation commit：`47927fe9747afaa484f0be200af56031c8a011f7`；
- evidence commit：`b630d0be71cbbf8d56df4ac26a42ade6593207f0`，exact path only
  `.agent-work/EXECUTION_RESULT.md`；
- old prefix：`1140609` bytes，SHA-256
  `85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f`；
- accepted append：`10181` bytes / `6` lines / EOF-only，SHA-256
  `1ab6f655aa903907036f9ed47616e05f724f7a265701cbc9041ca8f14f6aaac2`；
- new total：`1150790` bytes，SHA-256
  `75e247657f27cd4edb6e7054c1d66f6f7bbef931f4d1cb337fe993df15ecd54d`；
- reviewed acceptance archive：
  `.agent-work/PLANS/20260731-2048-p7-retained-r3-b2-p7-i1-e1-c1-acceptance-review.md`，bytes `5575`，
  SHA-256 `782b3a9c2683a1d8bd023b0ec1d405a90ea747af9d0ea91d1091a84d972055fb`。

验证质量足以证明 fresh synthetic integration qualified，但该结果明确不验证、消费或授予 retained R3 eligibility；
canonical validator calls、eligibility emissions 与 release consumption 均为 `0`。

## 3. Decision, residual risk and exact next branch

Planner接受 P7-I1 为
`FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。Retained R3 保持
`RETAINED_UNVALIDATED_UNCONSUMED`。Residual engineering gap 是 current P7 template 固定 synthetic payload，而 repository
尚无 production public owner 构造 schema `p7_retained_r3_audit_provenance_manifest_v2` 的 real-manifest controller template。

Orchestrator 已登记唯一下一工程 branch `REF-P7-25-R2-B2-M1`：新增一个 repo-owned pure deterministic
real-manifest-v2 domain-template owner及 dedicated test。M1-I1、real B2、canonical validator、eligibility、release、network、
device与全部科学路线继续锁定，直到新的 active PLAN 分别解锁。

维护性判断：本归档只保存已验收 evidence 与 route transition，不引入生产抽象或并行 owner。
