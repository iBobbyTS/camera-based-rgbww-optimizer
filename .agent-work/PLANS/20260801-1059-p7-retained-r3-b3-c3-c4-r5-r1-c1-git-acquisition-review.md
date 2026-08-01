# P7 retained-R3 Option B：R5-R1-C1 Git acquisition failure 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-FIXED-BOUNDARY-REAL-MANIFEST-SELF-CHECK-V1`

**Planner 决定：** `REJECTED_GIT_OBJECT_DIAGNOSTIC_REQUIRED`

## 1. Review boundary 与 topology

- review depth：`Medium`；范围仅为activation `485a86382a80e37b3186cfec847f7ab85614234e`、evidence commit `bbb71f173b3d97c02c9838b111091e052588f447`、被执行PLAN以及physical EOF handoff。未把Executer自报结果当成canonical eligibility结论。
- activation是`131cf843dfdab42eb4fca5ace619dcee4d2d335a` direct child，subject exact `chore(plan): fix real manifest machine parser`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1046-p7-retained-r3-b3-c3-c4-r5-r1-pre-effect-parser-review.md`。
- evidence是activation direct child，subject exact `chore(evidence): record fixed-boundary real self-check`，changed path exact`.agent-work/EXECUTION_RESULT.md`。
- activation PLAN bytes/SHA-256 `17799` / `dc546aeedf3308226a58de3e42c221582ee347378f2316ef4360c40e8a578b11`；FULL `438811` / `e7e168bffbedb87cc88709e592c55397d929beade63cea9200b9acb2812a6272`；accepted archive `3813` / `2024a58ae4de7d0456a916845c3fba98eac2266a16b4000cc2b7cc037681cb8f`。
- parent ER bytes/SHA-256 `1421295` / `176dc3633e561758e3421a5eba74d2bd4751d140f18b20125413a6db6597bc0d`；child `1426440` / `ce8966b93f358deddddb43122d4d9e40c69df10fd119bcd8bd114a89dcf22234`。evidence commit只追加本轮handoff并位于physical EOF。

## 2. Accepted observations

- fixed-boundary FULL parser contract已实际通过：FULL读取1、candidate row1、outer backticks2、closing backtick为final character、inner JSON only、parse1、required subset exact；regex/multiline/fallback均0。
- fresh execution contract已经sealed；R4 preparation 2 files、manifest 5 files、C1 4 files及retained 3 files的冻结physical identities均通过，输入writes0。
- Git acquisition前两项成功；第三项exact object `32b9e670ff3bbea0cd1505528c2ca87c2935446c:src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py` 返回nonzero或nonempty stderr并立即hard fail。owner、required argv、18 ordered ledgers、success report、validator、eligibility与release均未进入。
- failure inventory exact contract pair+terminal pair，共4 files；canonical reload4、seal checks2；source pre/post identity相等；process scan1、owned0；retry/fallback0。
- network/device/camera/Ray/strip/cleanup/formal/public analyzer及repository code/test writes全部0。retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

这些是本次failure lifecycle与物理读取的有效观察，但不构成real self-check、manifest事实、canonical eligibility或release consumability信用。

## 3. Planner finding

`REV-R5-R1-C1-001`（Must Fix / Agent-Fixable）：第三个冻结Git acquisition对象尚未被证明是正确的commit/path组合，而且失败调用的exit code、stdout、stderr bytes及其SHA-256没有持久化。当前证据只能证明“第三个literal git show非成功”，不能区分：

1. commit object不存在或类型错误；
2. commit存在但exact path不存在；
3. exact path存在但指向错误blob；
4. typed baseline把rollback checkpoint、repair parent或repair child的commit/path位置绑定错误。

因此不能直接修改acquisition合同，也不能重跑真实self-check。最小下一步是一个不读取任何旧failure root、不读取真实artifacts、不调用owner的pure-offline Git object diagnostic；它必须冻结每个argv并为每次调用持久化exit/stdout/stderr的bytes与SHA-256。

## 4. 决定与唯一下一分支

R5-R1-C1拒绝，状态为`REJECTED_GIT_OBJECT_DIAGNOSTIC_REQUIRED`。下一唯一分支为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-D1`，仅诊断rollback checkpoint `32b9e670ff3bbea0cd1505528c2ca87c2935446c`、repair parent `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`、repair child `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`与冻结source/test blob OID/path关系。

D1必须：

1. 使用全新activation-derived standalone source/root；旧R5/R5-R1/R5-R1-C1及synthetic source/root的stat/read/list/search/reuse/write/delete均0；
2. 仅执行PLAN冻结的exact argv，cwd exact repository、shell false、stdin DEVNULL、无environment override；每次调用无论成功失败均保存argv、exit code以及stdout/stderr bytes与SHA-256；
3. 通过commit existence/type、三个exact commit tree inventories及四个冻结blob existence/content identity，判定third object是`COMMIT_MISSING`、`EXACT_PATH_MISSING`、`PATH_BLOB_MISMATCH`、`ROLLBACK_CHECKPOINT_NOT_FILE_OWNER`或`CONTRACT_CONSISTENT_UNEXPLAINED_FAILURE`之一；禁止generic path allowlist、自动替换路径或修改合同；
4. 只生成diagnostic report、terminal与seal；retry/fallback0；不读取R4/manifest/C1/retained artifacts，不运行真实self-check owner、required argv owner、validator或release；
5. 停在Planner门，由Planner根据持久化事实另行决定corrected acquisition合同；D1本身不授予任何real self-check或eligibility信用。

维护性判断：失败位于一次性执行包装器的Git provenance输入；下一包只收集冻结Git对象事实，不新增production owner、fallback或authority。
