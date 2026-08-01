# P7 retained-R3 Option B：R2-R1 typed contract activation failure 验收

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-REPO-PARSED-CORRECTED-GIT-SEAM-REAL-SELF-CHECK-V1`

**Evidence commit：** `1475952415757f45daa53c4b14f6c3c53eac2d63`

**Planner decision：** `REJECTED_PRE_EFFECT_TYPED_PARSER_RESULT_CONSUMPTION_ERROR`

## 1. Topology 与 reviewed scope

- activation `61c33604a55c06345095515be9b0d5ea226031a2` 是已接受parser evidence `e4f10665752651d612ae90d4be114d45b7ed38d0`的direct child，subject exact `chore(plan): resume corrected real self-check with parser owner`，changed paths exact FULL、PLAN、`20260801-1231` acceptance archive。
- evidence `1475952415757f45daa53c4b14f6c3c53eac2d63` 是activation direct child，subject exact `chore(evidence): record repo-parsed corrected real self-check`，changed path exact `.agent-work/EXECUTION_RESULT.md`。
- worktree在Planner接手时clean；没有owner source/test、runtime artifact、PLAN、FULL或archive的未提交改动。

## 2. Failure 判定

Accepted helper `parse_plan_machine_contract`与`parse_full_plan_machine_state`返回冻结dataclass `ParsedMachineContract`；JSON mapping位于`.value`，可重放evidence位于`.evidence`。Executer正确使用raw exact bytes并各调用helper一次，但把返回对象直接当mapping下标访问，触发`TypeError: 'ParsedMachineContract' object is not subscriptable`。这是调用层typed-interface误用，不是repo-owned parser defect，也不是科学问题。

失败发生在required FULL subset与owner identity之前：owner source/test context reads、patch、tests、compileall、CodeGraph sync、commit、fresh source/root、physical reads、self-check owner与全部real execution effects均为`0`。因此本包不能获得实现或real self-check完成信用，必须以最小typed-interface successor继续；accepted parser owner不得修改或复制。

## 3. Counter deviation 与 handoff

PLAN规定activation gate任一失败后后续status/context/patch/test/real execution全部`0`。ER记录parser TypeError后仍执行`pre_edit_status_checks=1`及topology diagnostics，故执行合同存在额外只读counter偏差。它不改变pre-effect和clean结论，但下一包必须把required subset、archive identity与typed interface全部通过后才执行唯一pre-edit status；若typed gate失败，status必须保持`0`。

ER evidence commit记录heading index `1`、complete-last-section-heading-to-physical-EOF extraction `1`、唯一append `1`、postappend operations `0`。最终R2-R1 heading、strict JSON block与closing fence确实位于文件physical EOF且以LF结束；handoff有效，无需supersession。

## 4. Locks、residual risk 与 next branch

retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。canonical validator、eligibility、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer均为`0`且继续锁定。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C1`。只纠正activation调用层：分别使用两个`ParsedMachineContract.value`做contract/subset比较，`.evidence`仅做typed evidence核对；不得修改accepted parser owner。通过typed activation gate后，原R2-R1 exact two-path Git seam owner correction、validation、commit及fresh pure-offline real self-check合同原样继续。

维护性判断：失败来自单一调用点误用明确typed API；最小successor无需新增抽象或修改parser owner，保持owner边界最清晰。
