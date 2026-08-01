# P7 retained-R3 Option B：R2-R1-C1-S1 physical-EOF supersession 验收

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C1-S1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C1-S1-GIT-ER-PHYSICAL-EOF-SUPERSESSION-V1`

**Activation：** `8ffcb91b5396265aa7e138c3ec8d57b450a95d58`

**Evidence commit：** `96e8a61b9e041f3d0b9af4bde5ed5e470f9ecab2`

**Planner decision：** `ACCEPTED_PHYSICAL_EOF_SUPERSESSION`

## 1. Topology、machine row 与 reviewed scope

- Activation是`cdf3bbc47bc95075747d1cc4d4b3baa2ea5a9c59`的direct child，subject exact `chore(plan): activate typed-evidence EOF supersession`，changed paths exact为FULL、PLAN及`20260801-1246` review archive。
- Evidence是activation direct child，subject exact `chore(evidence): seal typed-evidence physical EOF supersession`，changed path exact仅`.agent-work/EXECUTION_RESULT.md`；Planner接手时worktree clean。
- Committed PLAN与FULL raw exact bytes分别由accepted `parse_plan_machine_contract`和`parse_full_plan_machine_state`解析成功。两者`MachineContractEvidence.to_mapping()`只包含owner公开的13字段：`schema`、`owner`、`marker_ascii`、`source_bytes`、`source_sha256`、`candidate_count`、`candidate_lines`、`line_number`、`raw_row_bytes`、`raw_row_sha256`、`payload_bytes`、`payload_sha256`、`line_ending`；PLAN required FULL subset exact match。
- Review archive bytes `4562`、SHA-256 `fc22dbf1a7590fe39491fd95518a10b3bd0e34d03764bcd7c1b7b6f726a12a26` exact；activation ER baseline bytes `1467231`、SHA-256 `beaf989c2ad59a31dd62a68fabfe2a851b3a51396dc967308d022382da72a18a`、blob `f5f30897330b72c24cadd73b075d7576245ad977` exact。

## 2. Physical EOF 与 canonical facts 判定

Evidence ER bytes `1470994`、SHA-256 `b11ba3063474d71e40b8001fab5722d778d9e914e8b3291ded98bd433b8e1c57`、blob `1abca706cede4c96a2557a08b8fa5683c3071684`。其前`1467231` bytes与activation baseline逐字节相同，之后仅有一个Markdown分隔空行及一个新terminal section；旧non-EOF record没有删除、移动、修复或改写。

新heading `2026-08-01 P7 retained-R3 Option B R2-R1-C1 typed-evidence failure canonical physical-EOF supersession`只出现一次，section是当前文件最后一节，以closing fence与LF终止。Strict JSON duplicate-free、nonfinite-safe解析通过，完整记录原`AttributeError`、不存在字段`whole_line_backtick_count`、一次未授权pre-gate status偏差、后续owner/test/runtime effect `0`及retained R3锁定状态。

因此S1只获得ER canonical physical-EOF supersession信用；它不获得owner correction、real self-check、canonical validation、eligibility或release consumption信用。

## 3. Residual risk 与 exact next branch

原R2-R1-C1失败来自调用层臆造`MachineContractEvidence`字段，不是parser owner或self-check owner缺陷。下一包恢复原exact two-path Git seam owner correction、完整验证与唯一fresh pure-offline real self-check，但activation typed evidence只能调用`MachineContractEvidence.to_mapping()`并核对上述真实公开字段集合；禁止属性猜测、手写Markdown扫描或并行parser。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2`。

Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。Canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer继续锁定。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_WAITING_ORCHESTRATOR_ACTIVATION`。

维护性判断：S1仅恢复ER canonical位置；下一包复用既有parser与self-check owner，不新增抽象或authority。
