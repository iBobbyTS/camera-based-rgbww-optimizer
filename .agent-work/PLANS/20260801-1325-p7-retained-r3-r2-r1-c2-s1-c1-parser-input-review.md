# P7 retained-R3 Option B：R2-R1-C2-S1-C1 parser input review

**Planner review 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-COLLISION-FIXTURE-CORRECTION-AND-REAL-SELF-CHECK-V1`

**Activation：** `2c1a0564fef1eb01d06a7f54b392cfbc5aa1b3ef`；parent `5d34ce4154c95c462141cc78d15783980e4c8f82`；subject `chore(plan): correct real self-check collision fixture`；exact changed paths为FULL、PLAN与`.agent-work/PLANS/20260801-1314-p7-retained-r3-r2-r1-c2-s1-precedence-review.md`。

**Evidence commit：** `c52fd8753f84802da1829dd5c90e1061d71ee9cc`；parent `2c1a0564fef1eb01d06a7f54b392cfbc5aa1b3ef`；subject `chore(evidence): record collision-fixture corrected real self-check`；changed path exact `.agent-work/EXECUTION_RESULT.md`。

## 1. Reviewed scope 与 evidence quality

Planner完整读取AGENTS、project skill、committed PLAN、FULL machine state、本轮review archive与ER最后完整section，并独立核对HEAD topology和exact-two dirty identity。ER最后level-2 section为`R2-R1-C2-S1-C1 activation parser input-type failure physical EOF handoff`，canonical strict-JSON handoff位于physical EOF，文件以LF结束；suffix bytes `3059`、SHA-256 `193bd3ab7c5bb9d08f1404117a03cc54044c8973eeeed05caddcd52f869e8fc3`。

Activation topology、exact changed paths、archive bytes `5104`与SHA-256 `7a2eec4268f7cf394c95d0d3624fb69cee53911ec9a0e4b77315926d8aaf17a2`均匹配。Accepted repo-owned PLAN parser被调用一次，但调用点传入`UTF8_STR`；owner要求exact `bytes`，因此以`MachineContractValidationError(code="source_not_exact_bytes")`在PLAN parse阶段fail closed。FULL parser未调用，activation/archive/FULL subset尚未判定，pre-patch status与dirty identity gate也未开始。

当前worktree仍为exact two dirty，逐字等于上一包冻结身份：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py`：bytes `25094`，SHA-256 `a14c947322219b198e98c94f0063cbc8018fe6568bee8593253d6a1013bcab1a`，Git object `ccecfde60f96c9b54464df19fc18d1cb60de5973`。
- `tests/test_p7_retained_r3_real_manifest_self_check.py`：bytes `25823`，SHA-256 `21e9fd10fe9523b5d5555d4ef9cc52a0ec9ca3a691ba9a37edc76e329e76c7f1`，Git object `7afc8a37dae845f801b56d426ecdca3a91aa0fc7`。

## 2. Decision 与 failure classification

**Decision：** `REJECTED_PRE_EFFECT_CALL_SITE_DECODED_STR_NOT_EXACT_BYTES_PRESERVE_EXACT_TWO_DIRTY`。

这是Executer acquisition/call-site类型错误，不是accepted parser owner、FULL row、activation topology、production seam owner、fixture或test defect。Parser正确拒绝非exact-bytes输入。不得修改parser、公开typed API、FULL row、owner source、现有dirty bytes或证据；也不给fixture patch、targeted、focused、full、commit或real self-check任何信用。

## 3. Verified zero effects 与 locks

Fixture patch、source/test write、targeted/focused/full、compileall、CodeGraph、diff/status、implementation commit、postcommit targeted、fresh source/root、14 physical inputs、8 Git acquisitions、argv check、self-check owner、report与terminal均为`0`。Retry与fallback为`0`。

Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`；canonical validator、eligibility emission、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部`0`。

## 4. Exact next branch

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1`。Activation acquisition必须从Git stdout bytes或`Path.read_bytes()`取得committed PLAN/FULL/archive raw bytes，并把原始bytes直接传给accepted `parse_plan_machine_contract`、`parse_full_plan_machine_state`；禁止`decode`、text mode、`read_text`或任何手写Markdown parser。Typed value只通过`.value`读取；若需序列化parser evidence，只调用现有`.evidence.to_mapping()`，不得假设未公开字段。

完成typed activation gate后，仍须一次pre-patch status与两次dirty identity gate。随后只执行原冻结的一行fixture correction：`release_checkpoint=spec.activation.parent,`替换为`helper_v1=spec.activation.parent,`；owner source零读零写，assertion与precedence不变。之后从fresh targeted开始完成原targeted→focused→full→compileall→CodeGraph→diff/status→exact-two implementation commit→postcommit targeted→唯一fresh pure-offline real self-check合同。任一步失败立即physical-EOF handoff；不得retry、fallback或进入validator/release/device路线。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_RAW_BYTES_FIXTURE_CORRECTION_AND_REAL_SELF_CHECK_WAITING_PLANNER_REVIEW`。

维护性判断：successor只纠正外层controller的bytes acquisition，不改repo-owned parser或production owner；继续复用既有typed API、fixture与real self-check路径，无需新增抽象。
