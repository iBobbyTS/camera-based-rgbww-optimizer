# REF-P7-25-R2-B2-P4-I1-C1 transport failure review

**Planner 日期：** `2026-07-31`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-ALIAS-SAFE-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**Decision：**
`REJECTED_PRE_EFFECT_LIVE_OWNER_CONTAINER_WRITE_FIELD_ONLY_CORRECTION_REQUIRED`

**Exact next branch：** `REF-P7-25-R2-B2-P4-I1-C1-C1`。下一包只允许一个fresh、不可复用的
field-only synthetic integration source/root：先通过accepted repo analyzer与bounded transport gate，再执行原
Git/root/inputs/16-case/lifecycle合同。不得读取或修复本轮失败source/root，不得读取retained R3或进入real B2。

## 1. Reviewed topology and immutable failure identity

- Activation commit：`30e913d96d7485de64548dfbeff0f2e47619e903`，direct parent
  `f1b64db91365baf1980f6150be9b03350565136f`，subject exact
  `chore(plan): activate p4 alias-safe integration qualification`。
- Evidence commit：`0fd144ab2749ce731e36926e140b6723f7a44122`，是activation direct child，subject exact
  `chore(evidence): record p4 transport gate failure`，仅修改 `.agent-work/EXECUTION_RESULT.md`。
- Updated debug commit/current reviewed HEAD：
  `972f82465fa5d9671dba12a0570103bd1b9fb6af`，是evidence direct child，subject exact
  `docs(debug): refine p4 field projection boundary`，仅修改
  `.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md`。
- Failed source冻结在
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-controller-f1b64db.py`：
  bytes `33510`，SHA-256
  `de2038f4d520febb0984e6b8ff6a73c293a46503ee1d6f07118036343aff2f29`，mode `0600`，device
  `16777240`，inode `2225015`。Planner只接受committed ER、updated debug与Orchestrator冻结事实，未重读该source。
- Frozen failed output root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-qualification-f1b64db`
  未创建且保持absent；Planner未读取该path或任何external root。

## 2. Evidence and validation quality

唯一controller process count `1`、exit `1`。Source exclusive创建一次并由accepted provenance owner读取一次；
同一in-memory bytes完成strict UTF-8、AST parse、builtin compile。Accepted
`analyze_controller_source`调用一次并PASS，报告 `18` 个bound results；随后同一already-parsed actual AST进入
bounded transport assertion，exact一次以stable code `live_owner_container_write` hard-fail。

Transport gate记录 `16` 个live-object container/call occurrences：六个Git ledgers被临时tuple/list分组，四个
written/input identities被分组，九个artifact identities被list收集，root/qualification/terminal/seal/admission
identities在field projection前进入generic dict/helper call。该结果证明repo analyzer已正确接受direct/nonlocal
binding，但外置source仍把live owners运输到container或generic projection helper。

Failure发生在所有effects之前：activation Git calls/ledgers `0/6`、root `0/1`、inputs `0/4`、matrix `0/16`、
qualification `0/2`、terminal/seal `0/2`、admission `0/1`；fresh root absent。Retry、fallback、source rewrite、
alternate/second source、second root/process、rerun、delete与cleanup全部 `0`。旧source/root/evidence、accepted C1、
retained、Git provenance replay、real B2、manifest、canonical validator、eligibility、release、network/device及所有
later stages均为 `0`。证据质量足以拒绝本package并冻结mechanical correction；它不证明任何semantic matrix结果。

## 3. Findings

### REV-B2-P4-I1-C1-001 — temporary live-owner collections violate the transport boundary

Severity：blocking external composition defect；repo-owner finding：否。

六个Git ledger检查、input identities与artifact identities仍经tuple/list聚合。即使随后只读取字段，live object先
进入container已扩大alias surface并违反本package的direct-name ownership合同。下一source须把六个Git calls及其
`exit_code`/stderr检查逐项展开，每个ledger direct binding后立即以字段字面量构造plain dict；四个input和每个
artifact同样逐一验证、逐一inline projection。不得建立任何live artifact list/tuple/set/dict或遍历live owner集合。

### REV-B2-P4-I1-C1-002 — generic projection helpers still transport live identities

Severity：blocking external composition defect；repo-owner finding：否。

`projection(identity)`形式把live owner作为普通call argument，再在helper内部提取字段；这不满足“direct binding
后立即field-only projection”。Fresh source不得定义或调用任何接收live owner的generic projection/helper，
也不得通过comprehension、map、closure return、callback return或第二name间接投影。Plain dict必须在拥有该
direct name的同一callback中用explicit accepted fields立即构造；其后mutable state和callback returns只能携带
plain str/int/bool/None/bytes摘要及递归plain tuple/list/dict，绝不能携带live owner或opaque gate。

### REV-B2-P4-I1-C1-003 — transport gate must preserve the repo-required immutable root chain

Severity：blocking acceptance clarification；repo-owner finding：否。

不是所有identity组合都可删除。`validate_root_identity_chain`的repo contract要求immutable
`RootIdentityChain(before, files, after)`；因此bounded gate必须精确允许且只允许这一constructor的named
`before/files/after` immutable composition及随后的direct validator call。该例外不可扩展成generic path/call
allowlist。相同地，terminal seal owner要求的exact target identity direct call及opaque gate原name传给唯一
admission callback必须保留；gate仍禁止opaque introspection、alias、serialization或container write。

### REV-B2-P4-I1-C1-004 — accepted analyzer and pre-effect boundary remain valid

Severity：closure record；code finding：否。

Accepted analyzer已对最终dispatched bytes给出PASS和18 bindings；additional gate随后在任何effect前正确拒绝
composition drift。Implementation `83bb193259fcf1de5b3f78798001e83496c2daae`、source/test identities、14个
dedicated methods与final full `755/755`保持accepted。本轮不授权修改repo owner/code/test，也不新增第三owner。

## 4. Decision and bounded corrective package

Decision：`REJECTED_PRE_EFFECT_LIVE_OWNER_CONTAINER_WRITE_FIELD_ONLY_CORRECTION_REQUIRED`。

新任务 `REF-P7-25-R2-B2-P4-I1-C1-C1` 只允许：

1. 在全新exclusive path创建唯一final controller source，并由accepted provenance owner exact读取一次；
2. 在effects前先对same bytes运行accepted analyzer，再运行纠正后的bounded transport gate；
3. 逐项展开六个Git ledger检查/field projection，不调用generic projection helper；
4. 每个input/artifact identity direct binding后立即构造plain dict，不建立live artifact collection；
5. transport gate只为repo-required immutable `RootIdentityChain(before, files, after)`和现有seal owner-required
   direct calls保留exact shape exception；
6. 两个gate都通过后才执行Git6、one root、four synthetic inputs、原16 cases、exact9 artifacts、terminal seal、
   admission与一次ER append；任一失败fail closed，retry/fallback/第二source/root/process为零。

本package通过也只证明field-only synthetic external integration。失败source/root、retained R3、real B2、Git
provenance replay、subordinate manifest、actual canonical validator、eligibility、release、network、device、
FORMAL及later stages继续hard locked。

## 5. Proposed FULL transition

- `REF-P7-25-R2-B2-P4-I1-C1` →
  `REJECTED_PRE_EFFECT_LIVE_OWNER_CONTAINER_WRITE_FIELD_ONLY_CORRECTION_REQUIRED`。
- 新增 `REF-P7-25-R2-B2-P4-I1-C1-C1` → `READY_FOR_ORCHESTRATOR_ACTIVATION`。
- `repair_v2_status` → `P4_OWNER_ACCEPTED_FIELD_ONLY_SYNTHETIC_CORRECTION_PENDING`。
- `retained_r3_status`保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- old source/root、retained reads、real B2、manifest、validator、eligibility、release、network/device与scientific
  stages全部继续hard locked。

Planner只创建本archive并重写active PLAN；FULL、ER、debug、code、test、GUIDE与RESEARCH保持只读且不提交。
Orchestrator须独立审核、更新FULL并创建exact activation commit后，才可dispatch corrective Executer。

维护性判断：缺陷位于一次性external controller的机械transport，不在repo owner。逐项field projection移除
temporary ownership graph，同时保留唯一必要的immutable root-chain和seal direct-call语义；无需架构重构。
