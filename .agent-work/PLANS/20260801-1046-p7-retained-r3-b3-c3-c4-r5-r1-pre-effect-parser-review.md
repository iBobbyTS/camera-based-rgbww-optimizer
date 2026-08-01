# P7 retained-R3 Option B：R5-R1 pre-effect parser failure 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-FRESH-REAL-MANIFEST-SELF-CHECK-V1`

**Planner 决定：** `REJECTED_PRE_EFFECT_FIXED_BOUNDARY_PARSER_REQUIRED`

## 1. Topology 与 evidence

- activation `f95b7e6d1888291bca79dae6312ddc69cfad2189` 是 `bf5e971765f1533e3ac3e991386d60e4b2f97a1f` direct child，subject exact `chore(plan): retry real manifest self-check`，changed paths exact FULL、PLAN 与 `.agent-work/PLANS/20260801-1037-p7-retained-r3-b3-c3-c4-r5-c1-r1-writer-lifecycle-review.md`。
- evidence `131cf843dfdab42eb4fca5ace619dcee4d2d335a` 是 activation direct child，subject exact `chore(evidence): record fresh real manifest self-check`，changed path exact `.agent-work/EXECUTION_RESULT.md`。
- parent ER bytes/SHA-256 `1417401` / `85b49f87bf7c58514e7056f0fb1a5b0465a7053b0345d89b37a5fdf597c916a8`；child `1421295` / `176dc3633e561758e3421a5eba74d2bd4751d140f18b20125413a6db6597bc0d`；evidence commit只增加6行，handoff位于physical EOF。
- committed PLAN/FULL/accepted archive各读取exact1；activation Git topology acquisition已完成。

## 2. Planner finding

`REV-R5-R1-001`（Must Fix / Agent-Fixable）：FULL machine-state parser没有冻结Markdown code-span的固定边界。它在唯一一次FULL读取后，以`FULL_PLAN_MACHINE_STATE=`分割整个余下文本，并把JSON后面的closing backtick及trailing Markdown一起传给`json.loads`，因此抛出`JSONDecodeError: Extra data`（line 1 column 8404 char 8403）。

违反的不变量是：只允许从唯一整行`FULL_PLAN_MACHINE_STATE=`读取payload；该整行必须由单个outer backtick包裹；parser只能机械移除prefix、opening backtick与唯一closing backtick；`json.loads`只能接收inner JSON。不得使用跨行或贪婪regex，不得消费第二次FULL读取。

## 3. 副作用与安全审计

- 失败发生在source/root absence gate之前：source/root absence check、write/create、compile/invoke均0，artifacts为空。
- R4 preparation、manifest、C1、retained真实文件读取均0；Git bytes acquisition、required argv check、self-check owner及18 ledgers均0。
- report/contract/terminal write均0；retry/fallback0；旧失败或synthetic roots读取0。
- canonical validator、eligibility、release consumption/copy/generation/qualification、network/device/camera/Ray/strip/cleanup/formal/public analyzer全部0。
- process scan1、owned process0；retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 4. 决定与唯一下一分支

R5-R1拒绝，不能取得real self-check、manifest事实、eligibility或release credit。下一唯一分支为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1`：fresh fixed-boundary parser successor。

successor继承R5-R1其余real self-check输入、P3 lifecycle、8次Git acquisition、owner1/18 ledgers及sealed output合同，但必须：

1. 使用全新activation-derived source/root，不得stat/read/list/write/reuse任何旧source/root；
2. 从唯一FULL读取中寻找唯一整行`FULL_PLAN_MACHINE_STATE=`，验证该行以exact一个opening backtick与exact一个closing backtick包裹且closing backtick后无字符；
3. 机械切除prefix/opening和唯一closing backtick后，仅把inner JSON交给`json.loads`；禁止regex贪婪、跨行payload或第二次读取；
4. 任一边界、唯一性或JSON错误都在任何source/root/input/Git/owner effect前hard fail，retry/fallback0；
5. canonical validator、eligibility、release、network/device等全部继续为0。

维护性判断：问题局限于一次性controller的Markdown边界解析；successor只冻结确定性parser，不新增production owner或authority。
