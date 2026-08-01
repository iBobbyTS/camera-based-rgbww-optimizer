# P7 retained-R3 Option B：M1-S1 canonical JSON payload correction acceptance review

**Planner review date：** `2026-08-01`

**Reviewed reference task：**
`REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-C1-CANONICAL-JSON-PAYLOAD-CORRECTION-V1`

**Decision：**
`ACCEPTED_COMPLETE_REAL_MANIFEST_DOMAIN_OWNER_CANONICAL_JSON_VALIDATED`

**Exact next branch：** `REF-P7-25-R2-B2-M1-I1`；建立一次 fresh pure-offline synthetic integration，
只组合已接受的 M1 builder 与 P5 runtime，创建 synthetic fixture/source/output evidence 并停在 Planner 验收门。
不得读取真实 C1/retained、调用 canonical validator、生成 eligibility/release 或进入设备路线。

## 1. Reviewed topology 与 activation carry-forward

- Activation `db4703a2e13f8314cfe529551078e60567678bf7` 是 evidence parent
  `1b6715a2326d5a8d62d503e34e4cd8da76dfdf67` 的 direct child，subject exact
  `chore(plan): activate real manifest canonical payload correction`，tree
  `2b6b5c733a2b91f0c6f3da3f00f6765663840c75`。Changed paths exact 为 FULL、PLAN、
  `20260801-0043` failure-review archive 与 M1 dedicated test 四项。
- 第四项不是 activation-time implementation acceptance，而是正确分类的
  `UNVALIDATED_CARRY_FORWARD`。其 committed blob/bytes/SHA-256 exact
  `1df5786db37e7bb9cd4d5ffe26e4310d53f700aa` / `18553` /
  `9d6deea37ab7d33748b95fa1dabc1380a3ae9677b4008684387699bc40bd1dd6`；相对 rejected
  activation `89b9b54...` 的 binary diff bytes/SHA-256 exact `3404` /
  `b01f78668e05e709d33d415020dcb388fefe34980f381f823b14e8103e1cf777`。
- Implementation `c480c4065081eab06388a12e95fd79b37b0230e2` 是 activation direct child，tree
  `df6ce2d1b8adcf0f5b9d30b4f9936312a37b1529`，subject exact
  `fix(p7): project real manifest into canonical JSON`，changed paths exact 为 M1 module 与其
  dedicated test 两项。
- Evidence `216946495c455c91d433c4e70b32c14b940428fa` 是 implementation direct child，subject
  exact `chore(evidence): record real manifest canonical payload validation`，changed path exact
  `.agent-work/EXECUTION_RESULT.md`。Git diff 证明它只做 17 行 EOF append，无删除或 earlier-prefix rewrite。
- ER prefix at implementation exact blob/bytes/SHA-256 为
  `7a084f14c6e941ca3d899fa4b4932d0080106645` / `1202556` /
  `171d14a5e6e276be044130c5dbec40490d55aeb9af57d9410c7ba88006b4be65`；evidence after
  exact blob/bytes/SHA-256 为 `5a5019e7032d6e2501ec86d64261307ca8a6140d` / `1208558` /
  `ac56758bcb9a832749fe73ca695c2a3dade8c6198b1756b56b0b0ac8483ffdbb`。

## 2. Exact two-path implementation review

Canonical binary patch bytes/SHA-256 exact `4827` /
`c536bf657b1ccb5021c823a12c586c45e014f713b7a367f62a7964a243967f01`；numstat exact M1
`+9/-2`、test `+33/-0`。`git show --check` 对 activation、implementation、evidence 均无 whitespace error。

M1 production diff只改变 `_CANONICAL_TEMPLATE` 的 `phase_evaluate` persistence boundary 与对应
template golden：

- internal `activation`、`baseline`、two-row seam、C1 four rows、retained three rows继续由
  `build_real_manifest_domain_template` 构造 immutable tuples；typed frozen dataclass 与字段顺序未改；
- persisted `activation` 是 exact five-item list，changed paths 是 ordered list；
- persisted `baseline` 是 exact twelve-item list，seam 是 ordered two-row list且每行 exact six items；
- persisted C1/retained 分别是 ordered four/three rows，每行 exact eleven items；
- schema/status、所有字段值与顺序保持不变，没有 normalize、stringify、infer 或 drop；
- 没有 generic converter/helper、serializer widening、tuple allowlist、fallback、second payload owner 或 fake
  persist bypass。

`_CANONICAL_TEMPLATE_SHA256` 从
`16f7ff136de41fb9e220d48f3d6c4e5de08b95f58b38754fc7faaf9b7e40d147` 更新为
`4819a57be714bf0cd8760d3bc9f59b7d92d889b0fc1ee802e2b9a092ea14ce32`；
`_GOLDEN_REPLACEMENT_SHA256` 保持 exact
`55c43ad338a83c11a2b2c8d2c5714a9efaf75ec4215dd30e103d540b0c6502ec`。

Final M1 blob/bytes/SHA-256 exact：
`4bf50cf69f259f212e34d9be5eacd7721ed91c41` / `23725` /
`8016df1265a82a49b90c7bbe33ccf7621c61ac9568538f159aea4f84fca3543f`。

Final dedicated-test blob/bytes/SHA-256 exact：
`4036e05ed0ad92d4afc52df69b9a7cf7356c8fef` / `20374` /
`d8bff33770aba2b002b25652e086e5f45f5ef646cc0ade97d1a7be8ea7a99fc4`。

## 3. Dedicated tests 与 frozen owner audit

Independent committed-diff review确认：

- carried test07继续以 `replace(spec().c1_inputs[0], label=spec().c1_inputs[1].label)`构造
  direct-child/root-valid collision，并期待 exact `path_collision`；
- carried test13继续 strict decode + `ast.parse`，只从 exact import modules/aliases/call tokens排除 authority
  surface；合法 package `camera_based_rgbww_optimizer` 不再被 raw substring `camera` 误判；
- test13 fake success path的 `persist()`仍调用 P3 `canonical_json_bytes`；它逐字段构造 expected
  schema/status/activation/baseline/C1/retained JSON-native shape，并比较 stored first manifest exact canonical
  bytes；primary failure identity assertion保持不变；
- dedicated method inventory仍 exact `13`，没有新 helper、fixture converter、scanner、second fake runtime 或
  test path。

P3 source在 activation/implementation间保持 exact blob/bytes/SHA-256
`d6d6cc628861baf8a95a09f13fa9204989693b5b` / `19767` /
`118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d`；P3 test blob保持
`e7bd034d46fda2d24b1fc431e1bfc75f3f570f83`，其中 frozen negative assertion仍以 tuple matrix期待
`json_unsupported_value`。因此 P3 仍是唯一 canonical JSON eligibility/persistence value-domain owner，M1没有
放宽 serializer。

P4 conformance source保持 blob/SHA-256
`07f89d15c8288e0d45c495d6d5737bc37427b769` /
`008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee`；P5 runtime source保持
`075face6fd7453236affa303640b91eb16a42a9b` /
`07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2`；P7 runnable template source
保持 `5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5` /
`10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2`。没有跨 owner blast radius。

## 4. Validation quality 与 acceptance

Executer冻结的 ordered ledger为：targeted `13/13 OK`、focused `83/83 OK`、compileall exit `0`、full
discovery `800/800 OK`、postcommit targeted `13/13 OK`。Test invocations exact `4`、compileall exact `1`、
retry/fallback `0/0`。只有全部precommit validation通过后才运行 maintenance-only `codegraph sync` exact `1`，
exit `0`并报告 `Already up to date`；CodeGraph explore/query exact `0`，没有语义结论依赖该sync。

Git topology、exact two-path diff、stored exact-shape assertions、P3 tuple rejection owner、final objects与ER EOF
append相互一致，没有 acceptance finding。Planner因此接受 composite M1 owner，即 rejected historical candidate
`cddd23e...` 的实现内容经 activation carry-forward、test07/test13纠偏和 `c480c40...` canonical JSON修复形成的
current accepted tree。`cddd23e...` 本身继续 historical/non-consumable；新 consumable owner是 exact
`c480c4065081eab06388a12e95fd79b37b0230e2`，只可供 fresh pure-offline M1-I1 synthetic integration消费。

该接受不证明真实 retained R3、canonical validator、eligibility或release，也不授权 M1-R1、network/device 或任何
scientific stage。Retained R3继续 `RETAINED_UNVALIDATED_UNCONSUMED`。

## 5. Exact next branch 与 hard locks

下一唯一package为 `REF-P7-25-R2-B2-M1-I1`：

- fresh activation-derived source、seven synthetic direct-child fixture roots/files与exclusive output root；旧
  P7-I1、旧failed roots、真实 C1 path-owner、真实 retained artifacts全部不得读取或复用；
- M1 `build_real_manifest_domain_template` exact `1`，P5 `execute_controller_runtime` exact `1`，controller
  process exact `1`；无override、retry、fallback或第二source/root/process；
- 验证 source regular0600/hash、Git56成功、synthetic C1 four + retained three reads、output exact five canonical
  artifacts、manifest/seal/terminal/admission、stdout/stderr/exit、root/input immutability与无残留owned process；
- 不改production/test，不跑 tests/compileall/CodeGraph，不读真实 C1/retained，不调用canonical validator/callback，
  不emit eligibility，不做retained audit或任何release/network/device/science操作；
- success/failure都只append ER一次并停 Planner review。通过标签只能是
  `FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。

该工程包不需要 Advisor scientific decision 或 Human危险设备授权。

维护性判断：M1继续只拥有 typed domain composition 与自己的 persistence projection；P3/P4/P5分别保持
physical/canonical I/O、static provenance/lifecycle与outer runtime单一owner。后继只组合既有owner，不新增生产抽象或
第二evidence framework。
