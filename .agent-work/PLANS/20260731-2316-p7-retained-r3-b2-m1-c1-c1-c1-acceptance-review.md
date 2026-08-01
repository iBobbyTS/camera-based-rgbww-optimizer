# P7 retained-R3 Option B：M1-C1-C1-C1 wildcard fixture correction acceptance review

**Planner review date：** `2026-07-31`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-C1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-C1-C1-WILDCARD-FIXTURE-CORRECTION-V1`

**Decision：**
`ACCEPTED_COMPLETE_COMPOSITE_EXISTING_ROOT_IDENTITY_OWNER_VALIDATED`

**Exact next branch：** `REF-P7-25-R2-B2-M1-S1`；以本轮已接受的 P3/P4 existing-root owner 为前提，建立 fresh
real-manifest-v2 domain-template successor activation，不复用旧 M1 activation，也不进入 M1-I1、real input、validator、release 或设备路线。

## 1. Reviewed topology 与 immutable evidence

- Activation `51af8645e47fa87400a6a7456122ab097fb7ae67`是parent
  `ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f`的direct child，subject exact
  `chore(plan): activate existing root wildcard fixture correction`，tree
  `5d67e48e54dd856d6591c4025edecd41c95e0dc1`；changed paths exact FULL/PLAN/上一failure-review archive三项。
- Rejected predecessor candidate `40d92acb77b32f370955d687c74c7ff7077f55e1`保持immutable，parent
  `77c96d6eec4d1881a82a678c84165dff03d6fb6e`，subject exact
  `chore(p7): retain rejected existing root candidate`，tree
  `f8ff6be0b0436947eb2eaae26914b55313ce442b`，changed paths exact P3/P4 source及其dedicated tests四项；canonical binary patch
  SHA-256 exact `00eb408bb3fe4440a5589dacd9799247577ccd0c6dbc891c6ff693c5e9e5f683`。
- Predecessor evidence `ec782ab...`是candidate direct child且仅改ER；它没有改变四条candidate paths。其ER after blob
  `22afac8a93932aed3241f38c0623452b12972bd8`同时是本轮single append前的exact prefix。
- Correction implementation `ffd1d9bb234c90a28ab497b10a35b08e4478eb1c`是activation direct child，tree
  `398a3fb1b2c3a090b41f675c4eb6750cf5987ee5`，subject exact
  `fix(p7): correct existing root wildcard fixture`，changed path exact仅
  `tests/test_p7_retained_r3_controller_conformance.py`；canonical binary patch SHA-256 exact
  `9f1b6e97aa05f9a10b001254206de7fe8356a8ef138e55bfd55f1d15ade99dfb`。
- Evidence `4609d56709dbc8ac2c3046ada797e0faa16bf2ff`是implementation direct child，subject exact
  `chore(evidence): record existing root wildcard fixture correction`，只对ER做17行EOF append。Prefix blob/bytes/SHA-256为
  `22afac8a93932aed3241f38c0623452b12972bd8` / `1163313` /
  `24c93dca54ab0235f7c1b85fb89a084a59ccfcc03b2ed237b9ae7e697c3e7189`；after blob/bytes/SHA-256为
  `5bd42105c6778122af6006632052f136c951f7b0` / `1170070` /
  `642d147bb02c90d8b2b70ca6215f9e3fed7cf6355f94e0a90dcaace690af7fda`。旧ER内容没有被改写。

## 2. Exact one-path semantic review

独立diff review确认唯一语义变化局限于existing method
`test_23_existing_root_import_and_call_provenance_near_misses_rejected`的`wildcard` specimen及其直接shape assertions：

- before test blob/bytes/SHA-256为`429ab49802f50e1e3743dffd09c7f72345a2c271` / `25822` /
  `5091c9f98607f1d0a1122fca96356391dbe5b5bdff943a6c5ba8a0c678f0d3a9`；after为
  `edb4777738b849ed0b288642b2e2ac39f0f4aee4` / `27053` /
  `be3837f147aea7cdcb3b2abd0f4746dfd0819527fdbec613c355337fa1527ab4`。
- Wildcard source现在是explicit UTF-8 bytes：module body第一项为exact
  `from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import *`，第二项为`def controller():`，其function body direct
  assignment/call为`existing = read_existing_root(path)`。
- Direct AST assertions验证`ast.ImportFrom`的module/name、`FunctionDef`名、function-body `Assign`、`Call`及callee
  `read_existing_root`；source先经`ast.parse`成功后才进入existing `analyze_controller_source`。
- Expected stable code保持exact `existing_root_owner_import_invalid`。其他七个near-miss case、shared `OWNER_IMPORT`/`runtime`、test23外methods、P3
  test及全部production source均未改变；method inventory保持P3/P4/P5/P7=`28/25/6/11`。
- P4 source blob `07f89d15c8288e0d45c495d6d5737bc37427b769`、P3 source blob
  `d6d6cc628861baf8a95a09f13fa9204989693b5b`与P3 test blob
  `e7bd034d46fda2d24b1fc431e1bfc75f3f570f83`在candidate、activation与implementation间完全不变；其SHA-256分别为
  `008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee`、
  `118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d`、
  `96c33cb4a0cd21706c9b14c8527a50f0b3bd355ccc4efad7d2e3a9a239c864a2`。

该diff达到最小纠偏目标：把此前Python语法域内不合法的function-scope wildcard import变为合法module-scope negative specimen，既未把expected
code弱化为`source_parse_failed`，也未修改生产classifier以容忍非法fixture。

## 3. Validation quality 与 CodeGraph evidence limitation

Executer记录的冻结ledger为：targeted `53/53` exit0、focused `70/70` exit0、compileall exit0、full discovery
`787/787` exit0、postcommit targeted `53/53` exit0；test invocations exact4、compileall exact1、retry/fallback exact`0/0`。Targeted与
posttarget均覆盖test23，且其stable assertion只能在actual code为`existing_root_owner_import_invalid`时通过。Full suite覆盖整个composite P3/P4
candidate而不是只覆盖fixture。

Post-edit CodeGraph sync/query exact`1/1`且按序exit0。Query命名了test23、`runtime`、`analyze_controller_source`与
`_validate_existing_root_owner`，并打印production single analyzer/classifier owner，但没有单独打印test file。这是一个明确的展示范围限制，不能单独证明test
shape；不过它不构成验收缺口，原因是：

1. Git exact one-path semantic diff本身逐行给出module/function source construction和direct AST assertions；
2. 同一after blob被四个ordered test invocations中的相关suite执行，test23 stable-code assertion全绿；
3. 三条production/P3-test路径identity冻结，commit tree/path与binary patch证明没有second analyzer/classifier/parser/helper blast radius；
4. CodeGraph返回的production source仍证明P4唯一classifier path未变。

因此无需重跑已冻结CodeGraph或测试，也不应因为query未回显已由Git blob直接证明的test source而拒绝whole package。

## 4. Planner findings、decision 与 accepted owner boundary

Planner接受`40d92ac... + ffd1d9b...`为一个composite existing-root identity owner实现：

- P3 public `read_existing_root`是唯一existing physical-root acquisition owner，执行absolute/canonical/no-follow lstat、directory/0700与typed identity
  freeze；不create/open/enumerate/repair。
- P4只认可canonical unaliased import与direct-bound `read_existing_root(...)` result为effect-owned live root；constructor、alias、wildcard、attribute、shadow、
  nested/container/reflection/rebind仍fail closed，同时允许多个独立acquired roots与existing created-output-root owner并存。
- P3 physical I/O、P4 AST/effect provenance、P5 runtime职责仍分离；本轮fixture correction没有新增owner或framework。

旧candidate/evidence commits继续作为immutable historical evidence，但`m1_existing_root_candidate_commit`应由Orchestrator提案标记为
`ACCEPTED_COMPOSITE_40D92AC_PLUS_FFD1D9B`且`consumable=true`，只在后续fresh M1 successor的pure-offline implementation scope内消费；这不使retained
R3 eligible，也不授权M1-I1、real input、validator、release、network或device。

## 5. Residual risks、hard locks 与 exact next branch

Existing-root owner已具备实现M1 template所需的安全effect-provenance primitive，但real-manifest-v2 domain owner本身仍不存在，旧M1 activation
`535e5e1...`已因owner gap终止，绝不可恢复或复用。Next package必须是fresh successor `REF-P7-25-R2-B2-M1-S1`：

- exact new module+dedicated test两路径，pure/deterministic/effect-free builder；
- generated controller每个既有input root通过accepted P3 `read_existing_root` direct acquisition并被P4 exact识别，new output root仍只由
  `create_exclusive_root`创建一次；
- fresh pre/post CodeGraph、targeted13、focused83、compileall、full800、exact two-path commit与posttarget13；
- real C1/retained physical reads、external controller/root/process、M1-I1、real B2、manifest actual writes、validator/callback、eligibility、release、network/DNS/
  environment/credentials/device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部`0`。

Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。下一工程包不需要Advisor或Human授权；它不包含科学分支或高危设备操作。

维护性判断：验收后的能力仍由P3 physical-I/O与P4 static provenance两个existing owners承担，fixture correction只修合法source domain；fresh M1应只新增一个
typed pure composition owner并复用P3/P4/P5，不应增加第二writer、analyzer、classifier、serializer或lifecycle。
