# REF-P7-25-R2-B2-P7-C1-C1-C1 Planner review：targeted stale expectations and canonical payload failure

**Review date：** 2026-07-31

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-GENERATED-NEWLINE-ESCAPE-CORRECTION-V1`

**Planner decision：** `REJECTED_TARGETED_STALE_TEST_EXPECTATIONS_AND_CANONICAL_JSON_TUPLE_PAYLOAD`

**Consumable：** `false`

## 1. Reviewed scope and immutable topology

Activation commit `e20179f0bd8cbde03f81e7d9c2062f4b8c6700d1` is a direct child of
`4af21403d047139a9261e010ac1d9ccc92b77f8a`, has subject
`chore(plan): activate p7 c1 c1 c1 newline escape correction`, and changed exactly FULL、PLAN与前序review archive三条路径。执行开始时worktree clean；active PLAN/FULL只放行P7-C1-C1-C1，retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`，P5/P6 owners保持accepted，device authorization false。

Orchestrator保留失败现场为candidate commit
`d60dd878055f3a8d73eebc4c367b07791e0339d3`，direct parent为activation，subject
`chore(p7): retain rejected p7 newline candidate`，changed paths exact：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
2. `tests/test_p7_retained_r3_controller_domain_template.py`

Candidate canonical binary diff SHA-256为
`291325ec6cbc5659858aa639d523cc12265f4d87b15089d6ecc36f91f5876a9b`。Final source blob/bytes/SHA-256为
`c500cae6f561438c170d29356db0b7f85666f651` / `19759` /
`02a89ff41bba6cd164585478955263d90b76fc7c1ad4066fe8d7634651dfb6a4`；final test blob/bytes/SHA-256为
`60618440fc57c568b0f6e07921520ff99817cc06` / `24613` /
`f454f4574fd01235463df0c651e878d7cba2d8d547034d2cdf9719af2ebc42ef`。

Evidence commit `f6a22638ff19ae63c661a7d1fdc81ae0124166f3`是candidate direct child，仅向
`.agent-work/EXECUTION_RESULT.md`追加真实handoff；本review以该clean HEAD为冻结parent。Candidate因targeted非零而永久non-consumable。

## 2. Execution method and evidence quality

Activation与baseline gate通过。Executer只修改exact two paths；outer `_CANONICAL_TEMPLATE`中activation commit stdout、activation metadata stdout、runtime metadata subject/stdout三个冻结LF token各增加exact一层escape，test03增加完整expression byte boundary、AST constant/compile与三个negative specimen。既有五个NUL separator、CR、其他backslash、public exports/dataclasses、runtime/lifecycle/provenance owners、replacement tuple、bindings、paths、budgets、phases、artifacts和guarded entrypoint均未漂移。

唯一fresh pre-gate exit `0`，证明exact paths `2`、test methods `11`、LF tokens `3`、template/composed physical NUL `0`、strict UTF-8、module/generated AST parse+compile、三个negative specimens、Git calls `6`、root create `1`、artifacts/persist `9`、root-bound reads `7`、lifecycle owner call `1`、bound results `18`、matrix/lifecycle identities与byte hashes全部通过。该证据足以确认三处LF production correction本身已成立。

唯一fresh targeted运行exact `11` methods，exit `1`，结果`8 pass / 2 failures / 1 error`；retry/fallback `0/0`，没有重跑或继续后续验证：

1. test03仍断言NUL correction前的generated-source文本层级；这是stale expectation。它必须改为当前escaped-source byte boundary，并继续由AST常量证明runtime NUL/LF/CR语义，不能把production退回旧形式来迎合测试。
2. test08的generated-call inventory漏列模板中既有且已由pre-gate证明的`any`与`join`；这是stale exact inventory。只能显式加入这两个现有call并保留未知call负例，不能泛化allowlist。
3. test10进入in-memory lifecycle后，`phase_evaluate`把tuple-valued `semantic_matrix`交给canonical provenance owner；`canonical_json_bytes`按既有合同以`ProvenanceIOError("json_unsupported_value")`拒绝tuple。这是production payload合同缺陷，不是测试预期问题。

Focused93、compileall、unique full778、implementation commit、postcommit targeted11均为exact `0`。已接受P7-C1 CodeGraph preflight保持冻结，本包CodeGraph调用`0/0`。证据对拒绝和后继范围均充分，但不支持接受、消费或synthetic integration资格。

## 3. Safety and zero-effect audit

External controller/source/root/process、synthetic integration、old failed evidence、retained artifact/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部exact `0`。Executer未修改PLAN、FULL、archive、debug、GUIDE或RESEARCH。

Candidate `d60dd878055f3a8d73eebc4c367b07791e0339d3`永久non-consumable；retained R3仍未验证、未消费；没有later stage解锁。

## 4. Residual risks and exact next branch

下一包必须保留已经成立的三处LF correction和五处NUL correction，仅在same exact two paths内做三项bounded correction：

1. test03的一个stale generated-source NUL文本期望改为当前exact escaped-source boundary，并同时断言AST runtime常量；
2. test08 exact generated-call inventory显式加入已有`any`与`join`，未知call/import/payload负例保持；
3. production `semantic_matrix`改为canonical JSON-compatible、ordered、exact 16-entry owner payload；entry names、顺序、boolean values、`all`判定与artifact `matrix`字段科学/工程语义不变。不得修改canonical serializer，不得允许tuple，不得新增generic conversion/helper/owner，也不得改变matrix cardinality或phase owner。

Dedicated test必须增加正负合同：canonical JSON-compatible matrix payload可由existing owner编码并strict decode/重编码稳定；tuple specimen仍由existing owner fail closed。不得把negative test变为serializer allowlist扩大。

Exact next branch为`REF-P7-25-R2-B2-P7-C1-C1-C1-C1`，contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-CANONICAL-SEMANTIC-PAYLOAD-CORRECTION-V1`。保持exact same two paths，fresh pre-gate、targeted `11/11`、focused `93/93`、compileall、unique full `778/778`、single implementation commit、postcommit targeted `11/11`，retry/fallback `0/0`。External、retained、release、network与device全锁`0`。

维护性判断：后继只把现有matrix投影收敛到canonical owner已支持的JSON value domain，并修正两项精确测试库存；不新增serializer、allowlist、owner、helper或状态机，所有ownership边界保持不变。
