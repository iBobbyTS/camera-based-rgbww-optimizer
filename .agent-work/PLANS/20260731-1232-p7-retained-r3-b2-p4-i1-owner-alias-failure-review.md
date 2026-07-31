# REF-P7-25-R2-B2-P4-I1 owner-alias failure review

**Planner 日期：** `2026-07-31`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-REPO-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**Decision：**
`REJECTED_PRE_EFFECT_OWNER_ALIAS_ESCAPE_CORRECTIVE_INTEGRATION_REQUIRED`

**Exact next branch：** `REF-P7-25-R2-B2-P4-I1-C1`。它只允许创建一个新的、不可复用的
synthetic external controller source/root，以accepted repo owner先验收actual runtime source，并以
direct/nonlocal live names跨callback传递owner结果；mutable evidence state只可保存plain projections。
不得修改repo owner，不得读取失败source/root、retained R3或进入real B2。

## 1. Reviewed topology and immutable failure identity

- P4-I1 activation commit：`53ee10d6706ee39ab0767d7204ca904ff41a7b98`，direct parent
  `c89b2914af44eb3d10f4dc8b347340d86abc5756`，subject exact
  `chore(plan): activate p4 repo-owner integration qualification`，changed paths exact为FULL、PLAN与
  `.agent-work/PLANS/20260731-1137-p7-retained-r3-b2-p4-v1-final-source-validation-review.md`。
- P4-I1 evidence commit：`d822b2303072a7179ecd1f3ff245b2cacdece80a`，是activation的direct child，
  subject exact `chore(evidence): record p4 integration conformance failure`，仅修改
  `.agent-work/EXECUTION_RESULT.md`。
- Updated debug commit/current reviewed HEAD：
  `f1b64db91365baf1980f6150be9b03350565136f`，是evidence commit的direct child，subject exact
  `docs(debug): record p4 alias boundary result`，仅修改
  `.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md`。
- Failed source冻结在
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-controller-c89b291.py`：
  bytes `20586`，SHA-256
  `8c4cb131ed97bc38f5ff72947000d3b7932574759483b4172cd9fbfd992ea904`，mode `0600`，
  device `16777240`，inode `2224706`。该identity由committed ER、updated second-pass debug record及
  Orchestrator提供的独立事实共同冻结；Planner未重新读取该旧source。
- Fresh output root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-qualification-c89b291`
  从未创建且保持absent。Planner未读取该path或任何旧external root。

## 2. Execution evidence reviewed

唯一controller process count `1`、exit `1`。Source exclusive creation与accepted provenance owner的
single read已完成；同一in-memory source identity通过strict UTF-8、AST parse和builtin compile后，
repo-owned `analyze_controller_source`被exact调用一次。它以stable code `owner_alias_escape`拒绝actual
runtime AST。Lifecycle conformance attempt `1`；由于conformance是pre-effect gate，activation Git
`0/6`、root `0/1`、synthetic writes/reads `0/4`、matrix `0/16`、qualification `0/2`、terminal
`0/2`、admission `0/1`。因此不存在progressive、terminal、seal、admission或其它root artifact。

Retry、fallback、alternate/second source、second root/process、source rewrite/rerun及cleanup/delete均为
`0`。旧source/root/evidence、accepted C1、retained R3、Git provenance replay、real B2、subordinate
manifest、canonical validator、eligibility、retained audit、全部release、network、DNS、environment、
credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、
firmware、deployment、tests、compileall、CodeGraph sync、stage与commit预算均保持 `0`。

## 3. Findings

### REV-B2-P4-I1-001 — actual runtime source escaped a live owner result through mutable state

Severity：blocking integration composition defect；repo-owner finding：否。

Failed source把`create_exclusive_root`、`read_exact_file`、`run_read_only_git`等owner calls的live return
objects赋入generic mutable `state` container或由alias继续传递。Accepted owner要求每个owner call直接赋值
给唯一name，并拒绝任何把该name再次赋给其它target的AST。`owner_alias_escape`因此是正确、稳定且在任何
effect之前发生的拒绝；它不是owner false positive，也不是缺失terminal evidence。

Correction不得放宽或修改analyzer。Fresh source必须让每个owner call direct-bind到唯一name；若live
identity或opaque seal gate需跨lifecycle callback，使用analyzer接受的明确enclosing direct name加
`nonlocal`绑定，不得通过dict/list/object field、return alias或第二变量运输。Callback返回给lifecycle
的值也只能是plain projection。Mutable counters/evidence state只可保存str/int/bool/None及由owner
allowlisted fields立即构造的plain tuple/list/dict；不得保存任何live owner object、opaque gate或其alias。

### REV-B2-P4-I1-002 — P4 conformance owner fulfilled the required pre-effect safety boundary

Severity：closure record；code finding：否。

Conformance attempt exact `1`，其余effect和terminal attempts全零，与accepted lifecycle contract一致。
Root absent、Git零调用及artifact零写入共同证明failure没有跨越pre-effect boundary。P4 implementation
commit `83bb193259fcf1de5b3f78798001e83496c2daae`及其source/test identities、14-method dedicated
coverage和final full `755/755`继续accepted；本轮不授权任何repo code/test modification或新owner。

### REV-B2-P4-I1-003 — successor must certify its final dispatched source before effects

Severity：blocking acceptance requirement；code finding：否。

下一source不能仅凭模板或局部snippet宣称alias-safe。唯一process必须先用accepted provenance owner读取
最终物理source exact一次，在同一in-memory bytes上做strict UTF-8、AST parse、compile，并在lifecycle
conformance callback调用accepted `analyze_controller_source`。Positive report须明确证明actual source中
所有owner results各有唯一direct binding、root reads共享同一个direct live `DirectoryIdentity` name、
`returncode` usage为零、reflection/unknown attribute/opaque introspection为零。Analyzer通过之前Git、root、
inputs、matrix、terminal/seal/admission均必须为零。

由于mutable-container mutator并非accepted owner的schema职责，fresh source还须在同一pre-effect callback
对已经parse的actual AST执行一个bounded composition assertion：report列出的bound/opaque names不得作为
container constructor或mutator argument、subscript/attribute assignment value、callback return value或普通
call argument；唯一例外是allowlisted owner-field attribute projection、shared `root=` name、
`RootIdentityChain`的exact before/files/after immutable composition及opaque gate原name传给admission。该
assertion只验证本external source的transport形状，不复制或取代accepted owner。

Negative fixtures必须保持独立bytes/AST domain，只交给各自独立的analyzer调用；不能exec、拼接到actual
runtime source，或用whole-source文本计数影响actual positive。原16-case matrix继续适用：actual source
positive、Git field/unknown/reflection/alias/root-source negatives、root identity chain、primary failure与
terminal lifecycle均须exact `16/16`。

## 4. Decision and bounded corrective package

Decision：`REJECTED_PRE_EFFECT_OWNER_ALIAS_ESCAPE_CORRECTIVE_INTEGRATION_REQUIRED`。

新任务 `REF-P7-25-R2-B2-P4-I1-C1` 只允许：

1. 在新的exclusive path创建一次final controller source，并由accepted provenance owner exact读取一次；
2. 在唯一process内先验收actual bytes，再执行六个read-only activation Git calls；
3. 创建唯一fresh synthetic root，写/read exact四个synthetic inputs；
4. 用direct/nonlocal live bindings及plain projection state执行原exact 16-case matrix；
5. PASS时写qualification、terminal、seal与admission，并append一次ER；
6. 任一失败fail closed，retry/fallback/第二source/root/process均为零。

该包不得读取或修复旧P4-I1 source/root，不能读取retained、accepted C1或旧external evidence，不能运行
real B2、Git provenance replay、manifest、canonical validator、eligibility、release、network或device。
通过也只证明alias-safe synthetic integration，不自动解锁后续阶段。

## 5. Proposed FULL transition

- `REF-P7-25-R2-B2-P4-I1` →
  `REJECTED_PRE_EFFECT_OWNER_ALIAS_ESCAPE_CORRECTIVE_INTEGRATION_REQUIRED`。
- 新增 `REF-P7-25-R2-B2-P4-I1-C1` → `READY_FOR_ORCHESTRATOR_ACTIVATION`。
- `repair_v2_status` → `P4_OWNER_ACCEPTED_ALIAS_SAFE_SYNTHETIC_CORRECTION_PENDING`。
- `retained_r3_status`保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- real B2、retained reads、subordinate manifest、canonical validator、eligibility、release、network、device、
  FORMAL与later stages全部继续hard locked。

Planner只创建本archive并重写active PLAN；FULL、ER、debug、code、test、GUIDE与RESEARCH保持只读。
Orchestrator须独立审核、更新FULL并创建exact activation commit后，才可dispatch corrective Executer。

维护性判断：failure来自外置controller的live-object transport，不是repo owner架构缺陷。Correction复用
single conformance/provenance/lifecycle owners且不新增repo abstraction；direct live bindings与plain projection
state使ownership边界更明确，16-case matrix继续提供回归保护。
