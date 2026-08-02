# P7 retained-R3 Option B：effect-order exact-bytes/source-type failure 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1-R1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FRESH-REAL-SELF-CHECK-EFFECT-ORDER-SEQUENCING-CORRECTIVE-V1`

**Activation：** `eb472629eab08a911ce4e1880bb1d0370219b92d`

**Evidence commit：** `aea1e412c0673ef232c2381afa3e9078c0ad7a73`

**Planner decision：** `ACCEPTED_FAIL_CLOSED_LIFECYCLE_REJECTED_REAL_EXECUTION_EXACT_BYTES_AND_SOURCE_TYPE_PRE_OWNER_VIOLATION`

## 1. Reviewed scope 与方法

本次只验收 activation `eb472629eab08a911ce4e1880bb1d0370219b92d` 授权的 fresh real self-check effect-order corrective。独立审计 activation topology、changed paths、Git-object ER prefix/suffix、fresh path types/modes、四个 terminal JSON、effect order、counters、zero locks与authority boundary。没有调用owner、canonical validator、release、network、device、camera、Ray、strip、cleanup、formal或public analyzer。

Activation是evidence parent `0e8543ee11d209f1a5d3d0ed619f25b3801fe0bc` 的direct child，subject为 `chore(plan): correct real self-check effect order`，changed paths exact为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1829-p7-retained-r3-parser-byte-binding-effect-order-failure-review.md`

## 2. Evidence identities 与验证质量

Evidence commit `aea1e412c0673ef232c2381afa3e9078c0ad7a73` 仅修改 `.agent-work/EXECUTION_RESULT.md`。Activation ER blob bytes `1605081`、SHA-256 `9087458842341ad3281030f270f5ef3efd3ebffefbd0c3b32d9f3aa90d177608`；evidence ER blob bytes `1609346`、SHA-256 `613ee77aa70a9fa604843b73eed8bf901be813d5d7103f7e8cd60e5253b64f3c`；evidence blob以activation blob为exact prefix。唯一physical-EOF suffix bytes `4265`，SHA-256 `cf2b80ef4d83f40f58b3e110b15e008b2912ee2ae5debdec7ed417e0025abe95`。

Fresh source identity为 `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-effect-order-sequencing-corrective-eb47262-20260802T003858Z-source`。独立 `stat` 证明它实际是空directory、mode `0755`、directory entry bytes `64`，不是PLAN冻结的regular controller file `0600`。Fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-effect-order-sequencing-corrective-eb47262-20260802T003858Z-run` 同样是directory mode `0755`、不是冻结的 `0700`。

Fresh root内四个JSON均strict parse，physical identities为：

| Artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `effect-order.json` | 1579 | `450593974c29229f9614a54f9fbade78140740374d02a425733f5973f0ffd780` |
| `failure.json` | 3316 | `770b9dda1836a97e83e17dedc48a9e430e141cc6a4dadf9c6fdfc3525e49adfe` |
| `terminal-summary.json` | 4473 | `df1507882699e43087c66e741ac35ce8c432d5cd2d894cb7bb5183e002d27b90` |
| `terminal-seal.json` | 203 | `1f69e3e00db8314c67dca7e9bc4b7bd4c32231d3743f2bd5672359da2c417f5c` |

Artifact payload记录的activation Git-object identities经独立 `git show` 重放为：PLAN bytes `14275`、SHA-256 `f8255acfc1365a7643ba59890e27cec403e65219fc6e7a566894d1482caa9d0e`；FULL bytes `475659`、SHA-256 `edb3ccf13b29fcd5a8c810607fbcfadaab9ded23593e7bc8d3c54a55ea1c9aab`；accepted parser module source bytes `9414`、SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`。这些artifact事实可信，但ER prose把三组identity误写为 `18153/85fca7...`、`40306/2215a7...`、`14306/a30bdc...`，因此ER叙述不能作为identity owner；本归档冻结Git-object与artifact独立一致的真实值。

## 3. Findings 与决定

Effect-order的前半段确实改正：activation metadata/clean scope先完成，fresh identities随后创建，PLAN/FULL Git-object raw reads再发生。Controller在accepted PLAN parser第一次调用时却传入decoded text，accepted parser以 `MachineContractValidationError/source_not_exact_bytes` fail closed；FULL parser、required FULL subset、contract/seal、14-input snapshots与owner均未进入。Retry/fallback为 `0/0`，故接受该terminal fail-closed lifecycle。

但real execution必须拒绝，且有两个不可拆分的pre-owner违约：

1. accepted PLAN parser收到decoded text而不是同一Git-object raw `bytes`对象；
2. 所谓fresh source被建立为directory `0755`，fresh root也是directory `0755`，没有建立regular exclusive-create source file `0600`与root directory `0700`的冻结身份。

Failure accounting：accepted PLAN/FULL parser attempts `1/0`；required subset `0`；contract/seal checks `0`；physical input pre/post snapshots `0/0`；owner attempted/returned `0/0`；owner ledger `[]`；retry/fallback `0/0`。Tests、CodeGraph、canonical validator、eligibility、release、network/device/camera/Ray/strip/cleanup/formal/public analyzer、production/test/docs/skill/GUIDE writes、PLAN/FULL/archive writes及Executer commit全部为零。

结论只允许为subordinate fail-closed evidence。`production_owner_conclusion=false`、`lineage_conclusion=false`、`eligibility=false`、`release_consumable=false`；retained R3继续是unvalidated、unconsumed。

## 4. Residual risks 与 exact next branch

下一唯一分支是atomic parser/source-type corrective，不能再把sequencing、path type与parser byte-binding拆开验证：先验证activation topology；由activation metadata推导两个fresh paths；以exclusive file create建立source regular file mode `0600`，以exclusive directory create建立root directory mode `0700`；在同一controller内立即验证type、non-symlink、mode和freshness；之后各读取activation PLAN/FULL raw Git-object bytes exact一次，并把原始同一 `bytes` 对象直接送入accepted parsers，禁止decode、read_text、normalize、Markdown extraction、拼接或重编码。原子pre-owner gate任一步失败即以14-input与owner全零seal并停止；全部成功后才可冻结原14 immutable inputs并调用现有owner exact一次。

旧三轮的六个source/root paths，即 `992b04d...`、`b37cebb...`与本轮`eb47262...` paths，全部immutable no-read/no-stat/no-list/no-search/no-reuse。Retry/fallback保持零。不得修复ER旧payload、旧artifact、manifest或retained inputs；不得进入canonical validation、release、device或formal路线。

Planner stop：`FRESH_REAL_SELF_CHECK_ATOMIC_SOURCE_TYPE_RAW_BYTES_CORRECTIVE_WAITING_PLANNER_REVIEW`。

维护性判断：下一包仍只修执行包装的原子pre-owner gate，复用单一accepted parsers与real self-check owner；没有新增production abstraction或平行owner。
