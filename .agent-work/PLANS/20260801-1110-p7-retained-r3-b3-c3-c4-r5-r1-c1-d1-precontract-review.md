# P7 retained-R3 Option B：R5-R1-C1-D1 precontract parser failure 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-D1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-D1-GIT-OBJECT-DIAGNOSTIC-V1`

**Planner 决定：** `REJECTED_PRECONTRACT_FIXED_BOUNDARY_PARSER_REQUIRED`

## 1. Review boundary 与 topology

- review depth：`Medium`；范围仅为activation `f0949e274db65fb2f3da0c22ef185b39b55e39e5`、evidence commit `21cd061b39bcaeb7676ffe9152bab84517580efd`、被执行PLAN、fresh source/root与physical EOF handoff。未读取任何旧source/root、R4 preparation、manifest、C1或retained artifacts，也未把Executer自报结果当作Git attribution或eligibility结论。
- activation是`bbb71f173b3d97c02c9838b111091e052588f447` direct child，subject exact `chore(plan): diagnose real manifest Git object`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1059-p7-retained-r3-b3-c3-c4-r5-r1-c1-git-acquisition-review.md`。该archive当前bytes/SHA-256为`5430` / `89939c8ddcdf913743c9989d4c16e987265f64d3431957015d2d0524bdfd6654`。
- evidence是activation direct child，subject exact `chore(evidence): record real manifest Git object diagnostic`，changed path exact`.agent-work/EXECUTION_RESULT.md`；handoff位于physical EOF。

## 2. Independent evidence review

- fresh source为`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-git-object-diagnostic-r5-r1-c1-d1-f0949e274db6-source.py`，bytes/SHA-256/mode为`3468` / `3a18e3e47ea45b889fb12e485c403c62b4285bdfefe1a75885e62ba14b4002fc` / `0600`。
- fresh root为`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-git-object-diagnostic-r5-r1-c1-d1-f0949e274db6`，mode `0700`；inventory exact terminal pair。`99-terminal-summary.json` bytes/SHA-256为`613` / `b03b7729b05eeb6143dab48569dfd1ecce0e0dff5369f556bb695c1f269c2be7`，seal bytes/SHA-256为`203` / `21c66287c1262b1dd377e619ceb2ec8d6b654a5f7c8ddf54ae337a64f531b6ac`，seal内target bytes/hash与summary完全一致；两文件均strict JSON。
- terminal status/classification为`FAIL` / `PRECONTRACT_CONTROLLER_FAILURE`。single permitted committed FULL read搜索bare `FULL_PLAN_MACHINE_STATE=` prefix；canonical machine row实际由Markdown backticks包围，因而candidate为None，随后`.get`触发controller failure。FULL read budget已耗尽，controller fail closed。
- 10个冻结Git diagnostic argv全部actual `0`；没有commit/path/blob/content attribution。contract/report writes为0，terminal writes2；retry/fallback0；process scan1、owned0。
- old/real artifact reads、required argv owner、self-check owner、canonical validator、eligibility、release、repository code/test writes、network及全部device surfaces均0。retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Planner finding

`REV-R5-R1-C1-D1-001`（Must Fix / Agent-Fixable）：D1 activation preflight违反了已在R5-R1-C1实际验收通过的fixed-boundary machine-row parser合同，使用bare marker search，导致Git diagnostic在precontract阶段完全未运行。该失败不能否定冻结的10个Git argv，也不能提供任何Git object事实；必须拒绝D1且不得复用失败source/root。

唯一允许的修复不是扩大parser，而是逐字恢复已验收算法：单次FULL read；定位唯一整行，该行精确以一个opening backtick加`FULL_PLAN_MACHINE_STATE=`开始并以唯一closing backtick结束；验证整行backtick count等于2且closing是最后字符；mechanically slice固定prefix/opening与最后1字符；仅把inner JSON传给`json.loads`。禁止bare marker search、regex、split-after-marker、跨行、二读与fallback。

## 4. 决定与唯一下一分支

D1拒绝，状态为`REJECTED_PRECONTRACT_FIXED_BOUNDARY_PARSER_REQUIRED`。唯一下一分支为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-D1-R1`：使用全新activation-derived source/root恢复上述fixed-boundary preflight，然后原样执行D1冻结的10个exact argv，并逐次持久化exact argv、exit code、stdout/stderr bytes与SHA-256。

D1-R1不得读取或复用任何旧source/root，不得读取real artifacts，不得调用self-check owner、required argv owner、canonical validator、eligibility或release；network/device/camera/Ray/strip/cleanup/formal/public analyzer全部0。它只产生Git provenance diagnostic，不授予real self-check、manifest事实、canonical eligibility或release consumability信用。无需Advisor科学决策或Human设备授权。

维护性判断：失败局限于一次性offline controller的machine-row preflight；successor恢复已验收的单一parser合同，不新增production owner、path fallback或eligibility authority。
