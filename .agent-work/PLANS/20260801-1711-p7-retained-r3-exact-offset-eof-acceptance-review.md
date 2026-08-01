# P7 retained-R3 Option B：exact-offset physical-EOF supersession acceptance review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-MINIMAL-PHYSICAL-EOF-FAILURE-EXACT-OFFSET-SLICE-CORRECTION-V1`

**Decision：** `ACCEPTED_EXACT_OFFSET_TRUE_PHYSICAL_EOF_FAILURE_SUPERSESSION_ONLY`。

## 1. Reviewed scope、topology 与 immutable identities

Planner 独立读取 project skill、activation committed PLAN、activation/evidence Git metadata 及当前 ER physical EOF；未读取或修改 report/seal、terminal、source、其他 fresh/old roots、代码、测试、GUIDE 或设备状态。

Activation `3b53eb9227c2c114ecb0dd85ca99c583c6892e7d` 是 `fa51dd0e9bc92671b78c3d964eb4371594015791` 的 direct child，subject exact `chore(plan): correct EOF seal offset slice`，changed paths exact 且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1658-p7-retained-r3-minimal-eof-global-index-failure-review.md`

Activation committed identities：PLAN `11212` bytes / SHA-256 `dad0c4229db8d919810a33f064d6aab5dadb5b3015ebbfaa91891039df33b9db`；FULL `468192` bytes / SHA-256 `e45058ac3c0acdd389e6ffbaa5903216c7a575565ec2642a744f9a15a7d2df2f`；ER `1559501` bytes / SHA-256 `7b771a53aec9b06588398cfa536a8829979759ffc26b73966a01583f5b8ed69b`。

Evidence `94f161f56c96f4fdff7df8ae3a25072b62cc691c` 是 activation direct child，subject exact `chore(evidence): seal EOF index failure by exact offset`，changed path exact `.agent-work/EXECUTION_RESULT.md`。Review 开始时 HEAD exact evidence，worktree clean。

## 2. Independent exact-offset and EOF verification

Current ER exact `1561559` bytes / SHA-256 `6468ae28195ad5ae37bdb7cc4e821905b78467d2bca34b5bd0d8d9d061166b44`。其前 `1559501` bytes 与 activation ER 逐 byte 相同；新增 complete EOF suffix 含前导分隔 LF 为 exact `2058` bytes / SHA-256 `183f899049e3294f5f95bf98b8699a7ae04d25c3ff04ad9e537caff7dfdf3b05`，以 exact single LF 结束。

Planner 不做全文 heading search，直接复算 activation/current ER `[1546782:1546878]`：两份 exact `96`-byte slice 均与冻结 literal constant-time 相同，SHA-256 `d3e26074ad09fecf7d08b1acc6003f004fcb6198a37f36e8c61193442c4436a3`。再复算 `[1555430:1559501]`：两份完整 `4071`-byte tail constant-time 相同，SHA-256 `b91a59124220413e1f6037fb8429af934fdf1b53ebd048ab27141c42bd0bf62e`，结束位置 exact 等于 activation ER length 且以 single LF 结束。

Evidence suffix 位于此前 physical EOF 后，明确记录 activation topology/ER identity PASS、global `String#index` 命中更早重复 heading 的 predecessor failure、prior tail/suffix/patch/write 全 `0`、fixed-offset gates PASS、完整 pre-append ER preserved、one true-EOF append、retry/fallback/post-append operations `0`。Report/seal/matrix/controller/selector/ledger/validator/code/device 路线均未进入。

## 3. Decision、credit boundary 与 residual risk

本轮接受范围只覆盖 exact-offset failure seal 的 durable physical-EOF provenance；它修复了 predecessor 非唯一 heading 寻址及非 EOF handoff，不接受 synthetic engineering attribution facts，也不验证 fixed report 的完整 matrix。

Production owner、lineage、manifest truth、eligibility 与 release 继续无信用；Retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`。Original D2-C1-R2-C1 execution contract 继续 rejected。

唯一 successor 是同 reference chain 的下一 `C1` fixed-matrix read-only supersession：复用已接受的 activation Git-object raw bytes到 accepted PLAN/FULL parsers 的 same-process boundary；固定 report/seal 各读且 strict-load 一次；只从 top-level `$.matrix` 冻结完整 ordered 18 rows，并独立验证 `$.ledger_binding_proof.frozen_path == "$.ledger_rows"`；最后使用当前完整 `2058`-byte EOF tail 作为唯一 patch context，在 true physical EOF append 内嵌完整 matrix 的 supersession。禁止 controller、selector、Git ledger、artifact write、device 或更高层结论。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R2_C1_S1_C1_C1_C1_C1_C1_C1_C1_C1_FIXED_MATRIX_READ_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW`。

维护性判断：本轮只审计和编排 evidence；完整 tail anchor 与单一 report collection path 保持 provenance owner 清晰，不新增 repository abstraction 或代码债务。
