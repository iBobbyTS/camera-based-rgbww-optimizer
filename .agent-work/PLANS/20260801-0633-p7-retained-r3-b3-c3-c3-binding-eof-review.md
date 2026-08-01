# P7 retained-R3 Option B：B3-C3-C3 artifact-role binding / ER EOF 审核归档

**审核日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C3`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-CORRECTED-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V1`

**Planner decision：**
`BINDING_FAILURE_ACCEPTED_AS_DURABLE_FACT_EXECUTION_REJECTED_AND_ER_NON_EOF_TERMINAL_HANDOFF_REQUIRES_SUPERSESSION`

## 1. 审核范围与方法

本次只读审核只使用 committed Git metadata、`PLAN.md` 与 Git object 中的
`.agent-work/EXECUTION_RESULT.md` parent/child bytes。未读取 fresh failed root、controller artifacts、external manifest、retained R3、
生产源码或测试源码；未运行 tests、controller、CodeGraph、canonical validator、audit、release、network、device、camera、Ray、strip、
cleanup、formal 或 public analyzer。

审核对象：

- activation：`38aa1ce69c0a8dd70374415c531b8d33d6ebd064`；
- evidence commit：`fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36`；
- evidence subject：`chore(evidence): record B3-C3-C3 verification stop`；
- evidence changed path：exact one `.agent-work/EXECUTION_RESULT.md`；
- parent ER blob：`161dadc31edf0769861e42ca0116758672826053`；
- child ER blob：`744720bf87aa9a7ce98823049fe15f2aeb248cc4`。

## 2. 可接受的 durable facts

Committed ER payload足以冻结以下失败事实，不把它误报为real manifest defect：

1. transport与activation machine gate被记录为PASS；outer controller exit为`1`；
2. controller按`real_manifest_reference.files`列表位置推断artifact语义角色；该冻结列表第一项实际为
   `execution-result-admission.json`，却被当成manifest解析，随后在typed-facts gate以
   `RuntimeError:manifest_typed_facts_mismatch` fail closed；
3. 正确后继必须按machine-row中明确的artifact basename做exact lookup/binding，禁止按位置、排序、generic selector或fallback推断角色；
4. corrected self-check失败后，focused、full、synthetic实际均为`0`/`NOT_RUN`；不得把本轮算作postcommit verification通过；
5. ER记录canonical validator未调用、eligibility未发出、release不可消费、B4未解锁，retained R3继续
   `RETAINED_UNVALIDATED_UNCONSUMED`；network/device/camera/Ray/strip/formal等锁均为0；
6. fresh failed root不得复用。其路径仅作为失败记录存在，本审核未读取其内容，也不验收其中artifact identity。

## 3. 独立 physical EOF 核算

Planner从Git objects重算parent/child ER bytes，而非采信payload中的`postappend_operations=0`：

- parent bytes：`1332706`；SHA-256：
  `0b5514770f001f329b84922789820f37c9c01f2763579653df253f0cf81602e1`；
- child bytes：`1337266`；SHA-256：
  `ec8a1f8385f90b49318a122d4142a6e1af831ddf5a8c1f99c77a31947166314b`；
- `child.startswith(parent)=false`；
- longest common prefix：`2583` bytes；
- preserved common suffix：`1330123` bytes；
- insertion delta：`4560` bytes；SHA-256：
  `c69f63b45d54d5faab7f52c3c9d37e5336c0c732bcb2b00171daad732571fda6`；
- insertion之后仍有parent原有`1330123` bytes，因此本轮handoff不是physical EOF append。

这不改变binding failure与zero-lock事实，但使B3-C3-C3 terminal handoff不满足PLAN的physical EOF要求，必须先单独supersede。

## 4. Validation quality 与拒绝理由

本轮没有focused/full/synthetic测试结果可接受；它们均在binding failure后正确保持0。Controller的self-check失败可作为诊断事实，
不能作为corrected verification closure。ER payload虽声称一次append和postappend operations 0，但Git object字节证明实际内容插入历史前部，
所以handoff也不能直接验收。

因此执行结论为拒绝：
`REJECTED_CONTROLLER_ARTIFACT_ROLE_POSITIONAL_MISBINDING_AND_NON_EOF_EXECUTION_RESULT_HANDOFF`。

## 5. Exact next branch

唯一后继先执行`REF-P7-25-R2-B3-C3-C3-S1` Git/ER-only terminal supersession：只在当前ER物理EOF追加一个canonical supersession
section，引用本归档、冻结上述binding failure与全部locks，并明确原B3-C3-C3 section是noncanonical-positioned historical evidence。
该包不得读取失败root或real inputs，不得运行verification，也不得修controller binding。

S1被Planner验收且Orchestrator更新reference后，另起bounded correction package：controller必须通过machine-row basename exact lookup绑定
manifest、manifest seal、terminal、terminal seal、admission，禁止任何position inference；只有该后续包才可重新执行remaining self-check、
focused `83`、full `800`与brand-new synthetic exact once。

## 6. Residual risks 与 stop point

- positional role binding缺陷仍未修复，verification route保持锁定；
- real retained audit与canonical eligibility validator均未执行；
- release consumption、B4、device/formal/TD-C/sentinel/P8继续锁定；
- 下一Planner stop：
  `B3_C3_C3_S1_GIT_ER_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW`。

维护性判断：先把证据排序缺陷与controller绑定缺陷拆成两个独立包，避免一次执行同时改写历史证据和重跑验证；后续采用basename exact
binding可保持artifact ownership显式且不引入generic selector。
