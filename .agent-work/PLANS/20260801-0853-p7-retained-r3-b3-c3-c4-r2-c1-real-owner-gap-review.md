# P7 retained-R3 Option B：R2-C1 real owner gap review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R2-C1`

**Decision：** `REJECTED_PRE_EFFECT_REAL_SELF_CHECK_OWNER_AND_DURABLE_OUTPUT_CONTRACT_INCOMPLETE`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R3`；先实现单一 repo-owned typed real self-check owner 及 dedicated tests。Owner只返回 canonical in-memory report；real inputs、focused/full与 durable launcher output 均留给后续独立执行包。

## 1. Topology与physical EOF

- Activation `3e26adc176b25c81810039751ab4061e768fc873`是parent `c0e878653a72966c3890f5371d2e271e4d0009db`的direct child，tree `51a552da099919e02dfb85b215f70dfdb7802ddc`，subject exact `chore(plan): split B3 real verification remainder`；changed paths exact FULL、PLAN与`20260801-0844` review archive。
- Evidence `329e501645bdeb58aae43087d09fb094ebbd2be2`是activation direct child，tree `7bd3e6f3db0563b83333454dc32be3d0c76bee1f`，subject exact `chore(evidence): record B3 real verification remainder`，changed path only ER。
- ER prefix blob/bytes/SHA为`c367b7337a7795af693f0b126c5954b9568e98d6` / `1380184` / `0d82ed9483d1b3f173145b23cefdff9e3d56573df99ff09ecafb7790c9c0d9bd`；physical EOF suffix为6 lines、5092 bytes、SHA `200932701d31d041b109c087f7142cb287410d388c6b3ffd1072bfda6e45cd0c`；after blob/bytes/SHA为`fc0494465142104b64158db4746e59f63aaae80c` / `1385276` / `1424c20efce1eb9b082dbe17b92d22e0b876faf578941803c7b69d55c342ff61`。

## 2. Contract review与first failure

R2-C1正确在`PRE_ROOT_PRE_CONTROLLER_PRE_INPUT`停下，first failure为`FROZEN_REAL_CONTRACT_LACKS_EXACT_RECOMPUTE_OWNER_AND_DURABLE_OUTPUT_BINDINGS`。四类缺口均成立：

1. manifest每个required fact没有唯一JSON owner path与expected type；
2. seam没有唯一commit/path/argv/expected binding；
3. Git只有最大调用数，没有ordered argv/result ledger；
4. full suite没有唯一durable path/basename/mode/write/seal/terminal identity。

不得再引用、扩写或从`23ab2d8` one-off sections推导这些缺失绑定。聊天常量、generic selector、failed root、repository code/test recovery均未被使用，故不属于input defect。

## 3. Effect、lock与credit

Manifest self-check、focused83、full810、synthetic均`NOT_RUN/LOCKED_ZERO`。Fresh root/controller、real/C1/retained reads与writes、tests、CodeGraph、validator/audit/eligibility/release、network/device/science、retry/fallback均0。Process scan1、owned0；单次ER physical EOF append后operations0。

因此R2-C1不获得B3 credit，retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`，synthetic与B4保持锁定。

## 4. Successor maintainability boundary

CodeGraph确认现有P3 `p7_retained_r3_provenance_io`已拥有`FileIdentity`、`GitLedger`、strict canonical JSON与allowlisted read-only Git；P5 runtime及P6/P7 domain/runnable owners也已存在；M1 real-manifest domain/template已拥有activation、baseline、input与seam identity dataclasses。但没有一个完整typed B3 real self-check entrypoint，且新owner/test路径均不存在。

R3只新增一个typed owner与一个dedicated test。Owner集中拥有exact five artifact roles、JSON fact paths/types、seam bindings、ordered Git-ledger validation及canonical report；复用P3与M1类型，不新增filesystem/process/persistence/validator/eligibility authority。Durable full log由后续launcher捕获，不能混入owner。Implementation/tests只用synthetic typed values，不读retained real artifacts。

维护性判断：停止给one-off controller追加字段，改为单一typed owner；职责从执行与持久化中分离，exact two-path实现可独立回归，未增加平行validator或eligibility owner。
