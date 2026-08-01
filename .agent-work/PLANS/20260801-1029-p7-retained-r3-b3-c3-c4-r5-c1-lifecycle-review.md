# P7 retained-R3 Option B：R5-C1 synthetic lifecycle 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-C1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-SYNTHETIC-CONTRACT-LIFECYCLE-V1`

**Planner 决定：** `REJECTED_PARTIAL_LIFECYCLE_COVERAGE_CONTRACT_WRITER_NOT_IN_INJECTED_PRIMARY_PATH`

## 1. Topology与可信物理证据

- activation `fc97ac1f4cd057768530222b614524719594c2ee`是`766408d6ad3bac646a19078fdb0ad04aab8b85b7`direct child，subject `chore(plan): test self-check lifecycle`。
- evidence `bf5b237f4d45c3dac4bebe5626e59ef39f6a39c1`是activation direct child，subject `chore(evidence): record self-check lifecycle test`，changed path exact ER。
- parent ER bytes/SHA `1411661` / `a44ed995502c1955c54f44a5e8c8d65c7f01889eda229e7f2cb435940b6eb125`；child `1414382` / `f67a2fda8dd94a974dbf34f70ed94d0f5ecae23767cbf0e345c23c2608ba7d85`；unique physical EOF suffix bytes/SHA `2721` / `a8bcab0dc4cecd9ae99dfaf25774139ee69d06d21c00e5e5c78fa3f28a17aae2`。
- source mode `0600`，bytes `4536`，SHA-256 `93f44dcc20ba24212b955200b255201a4628b7680ffb94a5aaeeb9059f431062`，pre/post identity exact。
- golden root mode `0700` exact4：contract `212/100a762f5ac001f788aab8255d250917bee4611ad8b1efa1f9a8e088fec57a01`，seal `128/b953ee3d9daa02ed840a67b5f8f11ed73ab73c8fc4f8edf3f46cb75df6a80cc0`，terminal `252/42c14a8cd6e263829f406f62b661ea3994bc961d6f6125516382e623a09ffa68`，seal `126/4c91df8f368d6d5f78eebfa2891b9b7fc00858c065a2f0228e0ddcc39788526d`。
- failure root mode `0700` exact2：terminal `278/37d863f46968edfd4a9953f96b14976ac117044f4c7fbb0fb0b41a7193c69090`，seal `126/5c8d4cca2df70e0ea36f9ea449cd8f6d5735e1667bc5771d81ed9c8925e440fe`；contract files absent。
- 六文件mode `0600`、strict canonical re-encode与三seal均通过；golden/failure statuses和reported counters与evidence一致。

## 2. 已通过的部分

- `_json_native`正确把Mapping转plain dict、tuple/list转plain list，concrete scalar仅`None/bool/int/str`，unsupported object以stable `SyntheticLifecycleError/json_native_unsupported`拒绝。
- golden case在一个try中完成conversion、contract persist/seal、success terminal/seal，证明frozen wire containers经adapter后可被P3 writer接受。
- injected deep object在contract前被拒绝，failure terminal pair成功sealed，contract writes0。
- old R5/R4/real inputs、Git、owner、validator、eligibility、release、network/device全部0；retry/fallback0。

## 3. 阻断finding

active PLAN明确要求injected case的primary `try`覆盖`conversion → contract persist → seal`，以证明contract writer/serialization failure也进入同一failure lifecycle。

实际source在failure case中只执行`_json_native(injected)`，若意外成功则立即抛`injected_failure_missing`；不存在contract persist/seal语句，并且except只捕获`SyntheticLifecycleError`。因此：

- 它证明conversion failure可写terminal；
- 它没有证明P3 contract persist或seal抛`ProvenanceIOError`时可写terminal；
- real successor若只复制这一catch结构，仍可能重现上一R5的无terminal缺口。

另有`sys` import未包含于PLAN的exact import allowlist；它仅用于stdout且没有新增authority，属于次要scope偏差，但后继应显式冻结或移除。

## 4. Planner决定与下一分支

拒绝C1完整验收，不解锁real R5。保留source及两synthetic roots，不得复用、修改或删除。

下一唯一分支`REF-P7-25-R2-B3-C3-C4-R5-C1-R1`是更小的pure-offline synthetic writer-failure lifecycle gate：一个fresh source、一个golden root和一个injected-writer-failure root。复用已验证local adapter语义，但failure case必须让native conversion成功，然后通过P3 `persist_canonical_json(..., dependencies=...)`的精确注入依赖使contract writer在写入前抛stable `ProvenanceIOError`，由包围conversion/persist/seal的broad primary catch捕获并写exact failure terminal pair。contract writes0、root inventory exact2。

R1不得读取旧source/roots、R4或真实输入，不得运行Git/self-check/validator。R1被接受后才可新建fresh R5 real successor。

维护性判断：问题仍限于一次性controller的异常边界测试；用writer dependency injection覆盖真实P3 failure surface即可，无需修改P3或生产代码。
