# P7 retained-R3 Option B：R2-R1-C2-S1 collision precedence review

**Planner review 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-TEST-GENERATOR-SYNTAX-CORRECTION-AND-REAL-SELF-CHECK-V1`

**Activation：** `6ef2e9a07af85ab105177d2c64db6d70da4c9d34`；parent `7dd4277436272ce2e209ac9295d3a4eba2096190`；subject `chore(plan): repair real self-check test syntax`；exact changed paths为FULL、PLAN与`.agent-work/PLANS/20260801-1306-p7-retained-r3-r2-r1-c2-syntax-review.md`。

**Evidence commit：** `5d34ce4154c95c462141cc78d15783980e4c8f82`；parent `6ef2e9a07af85ab105177d2c64db6d70da4c9d34`；subject `chore(evidence): record syntax-corrected real self-check`；changed path exact `.agent-work/EXECUTION_RESULT.md`。

## 1. Reviewed scope 与 evidence quality

Planner完整读取AGENTS、project skill、active PLAN、FULL reference、前一review archive与ER physical EOF，并独立核对HEAD topology及exact-two dirty diff。ER最后完整level-2 section为`R2-R1-C2-S1 targeted semantic failure physical EOF handoff`，canonical strict-JSON handoff位于physical EOF且文件以LF结束。

Activation、archive与preserved dirty identity均匹配合同。Syntax correction只改dedicated test中`rollback_owner`和`swapped_paths`两处generator parenthesization；owner source保持不变。当前worktree仍为exact two dirty：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py`：bytes `25094`，SHA-256 `a14c947322219b198e98c94f0063cbc8018fe6568bee8593253d6a1013bcab1a`，Git object `ccecfde60f96c9b54464df19fc18d1cb60de5973`。
- `tests/test_p7_retained_r3_real_manifest_self_check.py`：bytes `25823`，SHA-256 `21e9fd10fe9523b5d5555d4ef9cc52a0ec9ca3a691ba9a37edc76e329e76c7f1`，Git object `7afc8a37dae845f801b56d426ecdca3a91aa0fc7`。

Targeted唯一调用完成`12`项中的`11`项并仅有一项失败：`test_09_blob_bytes_sha_oid_and_seam_mismatch_are_pre_git`期待`git_file_set_collision`，owner实际返回`git_file_set_mismatch`。后续focused/full/compileall/CodeGraph/diff/status/commit/postcommit/real self-check均为`0`，符合fail-fast。

## 2. Precedence finding 与 decision

Owner的fail-closed precedence正确。`_file_map`先验证typed rows及sorted/unique输入，再构造expected `(commit,path)` rows；只有expected rows本身重复时才返回`git_file_set_collision`，否则实际key set不同返回`git_file_set_mismatch`，最后才验证seam bytes/hash/blob。

当前negative fixture把`release_checkpoint`改成activation parent，同时把`helper_path`和first seam path改成activation path。但修复后的seam owner是`helper_v1 -> integration`，`release_checkpoint`不再拥有任何file row；因此expected rows并未重复，而fixture仍携带原seam-path rows，正确分类就是`git_file_set_mismatch`。这不是production owner defect，也不应通过改变precedence把set mismatch误报为collision。

**Decision：** `REJECTED_TARGETED_FIXTURE_STALE_COLLISION_OWNER_BINDING_PRESERVE_EXACT_TWO_DIRTY`。

不授予focused/full/compileall/CodeGraph/commit或real self-check信用。保留syntax-corrected exact-two dirty bytes，不重做source patch、syntax patch或typed gate。

## 3. Verified zero effects 与 residual risk

Targeted retry、additional patch、implementation commit、fresh source/root、14 physical inputs、8 Git acquisition processes、argv check、owner call、report与terminal均为`0`。Canonical validator、eligibility emission、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer均为`0`。Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。

Residual risk仅为dedicated collision fixture未构造真实expected-row collision；更正后仍须原targeted→focused→full链与fresh pure-offline real self-check证明owner实现。

## 4. Exact next branch

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1`。冻结当前exact-two dirty identity后，只在dedicated test现有collision fixture内把`release_checkpoint=spec.activation.parent`替换为`helper_v1=spec.activation.parent`。这会让activation parent/path与baseline helper_v1/helper_path形成真实expected-row duplicate，并在任何actual set/seam lookup前稳定返回`git_file_set_collision`。不得修改owner source、assertion、其他fixture或precedence。

随后从fresh targeted一次开始，按focused/full/compileall/CodeGraph/diff/status、exact-two implementation commit、postcommit targeted与唯一fresh pure-offline real self-check继续。任一步失败立即停止；不得重试、fallback或进入validator/release/device路线。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_FIXTURE_CORRECTION_AND_REAL_SELF_CHECK_WAITING_PLANNER_REVIEW`。

维护性判断：本review保留single production owner，只纠正dedicated negative fixture对seam commit owner的陈旧绑定；不引入新抽象或authority。
