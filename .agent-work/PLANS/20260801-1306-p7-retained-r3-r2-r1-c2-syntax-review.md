# P7 retained-R3 Option B：R2-R1-C2 syntax failure review

**Planner review 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-PUBLIC-TYPED-EVIDENCE-CORRECTED-GIT-SEAM-REAL-SELF-CHECK-V1`

**Activation：** `a658e6fb572b12203752fc7f6a977fcdb05df6e5`；parent `96e8a61b9e041f3d0b9af4bde5ed5e470f9ecab2`；subject `chore(plan): resume real self-check with public typed evidence`；exact changed paths为FULL、PLAN及前一review archive。

**Evidence commit：** `7dd4277436272ce2e209ac9295d3a4eba2096190`；parent `a658e6fb572b12203752fc7f6a977fcdb05df6e5`；subject `chore(evidence): record public-typed corrected real self-check`；changed path exact `.agent-work/EXECUTION_RESULT.md`。

## 1. Reviewed scope 与 evidence quality

Planner完整读取active PLAN、FULL machine row、accepted archive、evidence commit及ER physical EOF。ER最后一个完整level-2 section为`R2-R1-C2 public typed gate implementation failure`，文件以LF结束；canonical handoff位于physical EOF。

Typed activation gate accepted：PLAN/FULL各以raw exact bytes调用accepted public parser一次，`ParsedMachineContract.value`访问各一次，`MachineContractEvidence.to_mapping()`各一次；13-key evidence set、FULL required subset、archive identity均通过。没有hand-written parser、text decode或direct private evidence field access。

Owner/test before identity通过后，Executer对既有owner与dedicated test各完成一次patch。当前worktree exact two dirty：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py`：bytes `25094`，SHA-256 `a14c947322219b198e98c94f0063cbc8018fe6568bee8593253d6a1013bcab1a`，Git object identity `ccecfde60f96c9b54464df19fc18d1cb60de5973`。
- `tests/test_p7_retained_r3_real_manifest_self_check.py`：bytes `25849`，SHA-256 `4ce7c7b87c85e9b641bb6a5cb4d4cb3960a1d8627b89b78767408370e5b7fca6`，Git object identity `c7328e4d104ffcc0ad9d7e703e86ede7a1dc3a0e`。

`git diff --check`无whitespace错误，diff path set exact two。该check只描述当前文本形态，不替代Python parse/test。

## 2. Planner findings 与 decision

Targeted首次且唯一调用在导入dedicated test时以`SyntaxError: Generator expression must be parenthesized`失败，首报path为`tests/test_p7_retained_r3_real_manifest_self_check.py`、line `408`，completed tests `0`。根因是`rollback_owner`与紧邻的`swapped_paths`两处同型表达式都把conditional expression括号在`for`之前闭合，却继续向`sorted`传入`key=`；这是test patch的局部Python语法错误，不是owner contract、typed gate或科学合同缺陷。

**Decision：** `REJECTED_TARGETED_TEST_GENERATOR_SYNTAX_ERROR_PRESERVE_EXACT_TWO_DIRTY`。

不授予targeted、focused、full、compileall、CodeGraph、implementation commit或real self-check信用。保留当前source/test dirty内容逐字不变进入successor；不得重做owner source patch或typed gate，不得丢弃、重置或重建这两条diff。

## 3. Verified zero effects 与 residual risk

失败后additional patch、targeted retry、focused/full、compileall、CodeGraph、diff/status postcheck、implementation commit与postcommit targeted均为`0`。Fresh source/root、14 physical input reads、8 Git acquisitions、argv owner check、self-check owner、report与terminal均为`0`。Canonical validator、eligibility、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer均为`0`。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

Residual risk仅为：最小语法修复后功能断言尚未执行，owner/test语义仍需原targeted→focused→full链证明；fresh real self-check也尚未开始。

## 4. Exact next branch

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1`：在冻结exact-two dirty identity通过后，只对dedicated test执行一次最小generator parenthesization patch，同时修复`rollback_owner`与`swapped_paths`两处同型语法；owner source writes `0`。随后从原targeted开始，继续focused/full/compileall/CodeGraph/diff/status、exact-two implementation commit、postcommit targeted与唯一fresh pure-offline real self-check。

如dirty identity不符、test patch不能exact match、patch后path set不再exact two，立即fail closed，不运行tests或real self-check。任何测试/commit/runtime失败同样按原顺序停止。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_SYNTAX_CORRECTION_AND_REAL_SELF_CHECK_WAITING_PLANNER_REVIEW`。

维护性判断：本review只隔离dedicated test局部语法错误，保留既有single owner、typed parser及authority边界；无需重构。
