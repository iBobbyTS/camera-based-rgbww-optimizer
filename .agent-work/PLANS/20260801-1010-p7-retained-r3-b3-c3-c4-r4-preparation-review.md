# P7 retained-R3 Option B：R4 immutable preparation 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R4`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R4-REAL-SELF-CHECK-PREPARATION-V1`

**Planner 决定：** `ACCEPTED_COMPLETE_IMMUTABLE_PREPARATION_NOT_EXECUTED_NOT_ELIGIBLE`

## 1. 提交与physical EOF

- activation `9907aab3d3d165b17759fd656db27c6d07c30461`，parent exact `36ea02ad1993c34e119c6bb80e5a841c2e77b205`，subject `chore(plan): prepare real manifest self-check`，changed paths exact FULL、PLAN及前轮acceptance archive。
- evidence `bddf374606ff34a7cd32ad9ba15089df70d0bb05`是activation direct child，subject `chore(evidence): record real self-check preparation`，changed path exact `.agent-work/EXECUTION_RESULT.md`。
- parent ER bytes/SHA-256 `1404105` / `169716925b35283bb13e65cc59f8ca4ec5cd4c3d6a8e359adeceed70eb0d7142`；child `1408527` / `43488ee147e21835e6ab81cb7b588f74236428b33f3a4924a858aceb74624ac0`。
- child以parent为exact prefix；唯一physical EOF suffix bytes/SHA-256 `4422` / `76ba71272b8186780dc16c042ee78ed74eaec49b6388fa4c46d65442bef84b93`，heading只出现一次，payload strict duplicate-free JSON。

## 2. Fresh source与sealed output

- source `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-prep-9907aab3d3d1-source.py`：mode `0600`，device/inode `16777240/2273245`，bytes `6060`，SHA-256 `207e55df7edc62ab1b50f3e08824dd81f4e7c473b19c72ba946ca62bf8daeedd`，pre/post identity exact。
- root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-prep-9907aab3d3d1`：absolute，mode `0700`，device/inode `16777240/2273247`，inventory exact two。
- `real-self-check-preparation.json`：mode `0600`，inode `2273248`，bytes `3278`，SHA-256 `06e395e7796f5654748e49c28734938021786353a564a278869b988269513532`。
- `real-self-check-preparation.sha256.json`：mode `0600`，inode `2273249`，bytes `135`，SHA-256 `278a7186eadf330d008339c00df5e94a98cf720db5c64f800193a8dc8e1a6b04`。
- 两artifact均strict decode并exact canonical re-encode；seal exact绑定主文件target/bytes/SHA。
- payload exact `prepared_not_executed`，`execution_authorized=false`、`eligibility=false`、`release_consumable=false`、`canonical_validator_sole_eligibility_owner=true`；三组5+4+3 frozen identities与active PLAN exact相等。

## 3. Budget与偏差审查

committed PLAN/FULL/archive reads、source write/compile/invocation、root creation、两次canonical writes/reloads、identity/inventory/process/ER append budgets均exact；retry/fallback/postappend operations为0。

real manifest/C1/retained root/file reads、self-check owner、Git acquisition、canonical validator、eligibility、release consumption、repository code/test、network/device/camera/Ray/strip/cleanup/formal/public analyzer均0。

执行中active PLAN未在machine row逐字列出P3 callable名称。Orchestrator通过CodeGraph确认并补充现有唯一owners：

- `create_exclusive_root(path, *, dependencies=None) -> DirectoryIdentity`；
- `persist_canonical_json(root, child_name, value, *, dependencies=None) -> FileIdentity`。

Planner独立源码复核确认PLAN prose已明确要求“P3 exclusive-root owner”和“P3 canonical exclusive writer”；上述函数正是该模块内唯一匹配实现，分别强制absolute/0700/exclusive root与direct-child/no-follow/0600/exclusive/fsync/reload。source只导入`sys`、`__future__`及该P3模块，只调用上述owners与`canonical_json_bytes`，没有open/stat/subprocess/network/validator/release/device surface，也没有parallel writer。因此这是既有owner名称解析，不是授权扩张或执行方向变更，接受该偏差。

## 4. 决定、残余风险与下一分支

接受R4完成。它只证明一个immutable preparation contract已经sealed，不证明真实manifest facts、retained R3、canonical eligibility或release consumability。

下一唯一分支为`REF-P7-25-R2-B3-C3-C4-R5`：一次pure-offline real self-check。它必须验证R4 preparation，使用P3 no-follow readers读取冻结manifest 5、C1 4、retained 3 files，构造独立typed spec；只用exact frozen Git bytes acquisition，然后调用`run_real_manifest_self_check`一次并验证其18条ordered Git ledger。成功或失败都生成sealed terminal evidence。

R5仍不得调用canonical validator、发eligibility、消费release或访问network/device/camera/Ray/strip/formal/public analyzer。用户当前设备禁令不影响此纯离线只读包。

失败分支：任一root/file identity、canonical/seal、typed fact、Git acquisition、18-ledger、owner report或terminal seal失败即hard fail，保留fresh source/root/progressive evidence，retry/fallback为0，停止在Planner门；不得repair/reuse root或进入validator。

维护性判断：R4复用唯一P3 persistence owner且无生产改动；R5继续复用已验收typed owner与P3 readers，不引入新共享抽象或eligibility authority。
