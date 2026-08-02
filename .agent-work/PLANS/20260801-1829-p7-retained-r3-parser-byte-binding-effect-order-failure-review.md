# P7 retained-R3 Option B：parser byte-binding effect-order failure 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1-R1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FRESH-REAL-SELF-CHECK-PARSER-BYTE-BINDING-CORRECTIVE-V1`

**Activation：** `b37cebb0aa8a2c2566dfda636598aab87f751f33`

**Evidence commit：** `0e8543ee11d209f1a5d3d0ed619f25b3801fe0bc`

**Planner decision：** `ACCEPTED_FAILURE_LIFECYCLE_REJECTED_REAL_SELF_CHECK_EXECUTION_PRE_OWNER_EFFECT_ORDER_VIOLATION`

## 1. Reviewed scope 与方法

本次只验收 activation `b37cebb0aa8a2c2566dfda636598aab87f751f33` 所授权的 fresh real self-check parser byte-binding corrective。独立审计 activation topology、changed paths、Git-object ER prefix/suffix、fresh source/root identities、四个 terminal artifacts、seal、effect order、counters、zero locks 与 authority boundary。没有调用 owner、canonical validator、release、network、device、camera、Ray、strip、cleanup、formal 或 public analyzer。

Activation 是 evidence parent `a61cd46958e1b97d70015064dcbdcfe121672e4d` 的 direct child，subject 为 `chore(plan): correct real self-check parser byte binding`，changed paths exact 为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1817-p7-retained-r3-real-self-check-pre-owner-bytes-failure-review.md`

## 2. Evidence identities 与验证质量

Evidence commit `0e8543ee11d209f1a5d3d0ed619f25b3801fe0bc` 仅修改 `.agent-work/EXECUTION_RESULT.md`。Activation ER blob bytes `1600280`；evidence ER blob bytes `1605081`；evidence blob以activation blob为exact prefix。唯一physical-EOF suffix bytes `4801`，SHA-256 `6f59996e03dd4474092aa7a4455d79a5b182a9f998316de71f54a6fd2a986429`。

Fresh source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-real-self-check-parser-bytes-corrective-b37cebb0aa8a.py`，bytes `262`，SHA-256 `06c4085c2acbfe4807397b8704086f1c00c2c61badf0f7a9a6653cbe5e7e3ee6`，mode `0600`，invocations `0`。

Fresh root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-real-self-check-parser-bytes-corrective-b37cebb0aa8a-output`，mode `0700`。独立读取确认四件套：

| Artifact | bytes | SHA-256 | mode |
| --- | ---: | --- | --- |
| `00-execution-contract.json` | 4671 | `202660e0ec6d6a673545a0db45ba6a9c719fe65dfe748b04f909fdb06cb8876e` | `0600` |
| `00-execution-contract.sha256.json` | 144 | `5c85d96e83502afd00fca6f12682b3cf1f8f5d743951c5940ab96164bb702d11` | `0600` |
| `01-terminal-summary.json` | 5090 | `cd8ffc0645e0c1736792cc0c92a25c4201d41896f6d53cebe23a3eeb1e72d9fb` | `0600` |
| `01-terminal-summary.sha256.json` | 142 | `deaf4678f592e9a43ecb3960b34b7a4bc7775805e58fde47cfb29f513e1b7106` | `0600` |

两份payload均为sorted、indent-2、UTF-8、newline-terminated canonical JSON；两个seal的artifact、bytes、SHA-256与实际payload exact一致。Failure为 code `PRE_OWNER_EFFECT_ORDER_VIOLATION`、stage `pre_owner_gate`、type `FrozenEffectOrderViolation`、row `null`、message `activation Git-object raw reads occurred before exclusive fresh source/root creation`。

## 3. Findings 与决定

Parser identity proof本身可信：activation PLAN/FULL Git-object raw bytes各读取exact一次，分别为 bytes `12969` / SHA-256 `145ba4660364ae73b44ce5ed9d76a120f6c1c404754a820baa2e9c1dcb0e6d15` 与 bytes `474432` / SHA-256 `606182c2c6bf43931336d8bc9c35902de146ffe406822d25532cee1ba31b371d`；同一个raw bytes对象直接进入对应accepted parser，decode/read_text/controller-owned parser均为false，FULL required subset match为true。

但observed effect order为：

1. read activation PLAN/FULL raw Git objects；
2. pass same raw bytes to accepted parsers；
3. validate required FULL subset；
4. derive and exclusively create fresh source/root。

Active PLAN冻结顺序要求fresh source/root独占创建必须先于raw Git-object read/parser。因此这是pre-owner effect-order硬失败，不能给予real self-check execution credit。

Failure lifecycle验收通过：physical retained-R3 input reads `0/14`；input before/after `[]/[]`；owner attempted/returned `0/0`；owner ledger `[]`；success report `0`；retry/fallback `0/0`；fresh source/root `1/1`；local controller process `1`；owned processes empty `true`；ER append `1`；Executer commit `0`。Repository code/test writes、tests、CodeGraph、canonical validator、production-owner conclusion、lineage、eligibility、release、network/device/camera/Ray/strip/cleanup/formal/public analyzer及PLAN/FULL/archive writes全部为零。

结论仅是subordinate failure evidence。`production_owner_conclusion=false`、`lineage_conclusion=false`、`eligibility=false`、`release_consumable=false`；retained R3继续是unvalidated、unconsumed。

## 4. Residual risks 与 exact next branch

剩余问题只在controller effect sequencing，不是accepted parser、14个immutable inputs或owner科学结果。禁止把本failure解释成owner disposition，也禁止消费旧source/root、修复payload、重建manifest或进入canonical validation/release/device/formal路线。

下一唯一分支是bounded sequencing corrective：activation metadata/topology确认后，先据activation short SHA推导并以exclusive create建立新的source/root，再在同一controller内各读取activation PLAN/FULL raw bytes exact一次并直接传入accepted parsers；required FULL subset成功后才写contract/seal、冻结原14 inputs并调用当前repo-owned real self-check owner exact一次。旧`992b04d...`与`b37cebb...`的source/root全部immutable no-read/no-stat/no-list/no-search/no-reuse。Retry与fallback保持零。

Planner stop：`FRESH_REAL_SELF_CHECK_EFFECT_ORDER_SEQUENCING_CORRECTIVE_WAITING_PLANNER_REVIEW`。

维护性判断：拒绝范围精确落在执行包装的effect sequencing；下一包复用accepted parser与单一real self-check owner，不引入production抽象或并行owner。
