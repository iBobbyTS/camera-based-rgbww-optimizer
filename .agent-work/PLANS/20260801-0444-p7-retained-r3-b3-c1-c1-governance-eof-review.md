# P7 retained-R3 Option B：B3-C1-C1 governance / EOF 审核归档

**审核日期：** `2026-08-01`

**Reviewed task：** `REF-P7-25-R2-B3-C1-C1`

**Activation：** `a9de513b94b2e6871914960c238333a979de4ecf`

**Evidence commit：** `4877fd30ea2821e71fc7497321e24a886302d93c`

**Planner decision：**
`REJECTED_NON_EOF_HANDOFF_UNAUTHORIZED_CODEGRAPH_AND_GOVERNANCE_IDENTITY_MISBINDING`

## 1. 已审核范围与方法

Planner只读审核activation、evidence commit、committed/current
`EXECUTION_RESULT.md`、Advisor request文件的Git历史、B2 sealed subordinate manifest、
repository governance manifest、GUIDE、Advisor Option-B attachment与原始lineage-owner decision
evidence。未修改Advisor文件、B2 manifest、retained R3或任何外置artifact；未调用canonical
validator、retained audit、tests、controller、network或device。

独立Git审计确认evidence commit parent为`a9de513...`、subject为
`chore(evidence): record B3-C1-C1 governance stop`，changed path exact one：
`.agent-work/EXECUTION_RESULT.md`。

## 2. Execution结果中可保留的事实

以下读操作结果与冻结identity一致，但不能因此credit本轮handoff：

- activation PLAN/FULL strict machine-row decode与typed subset compare通过；canonical reencode、key-order、raw-byte-equality均为`0`；
- B2 source、real manifest five、C1 four及retained three的path/mode/bytes/SHA identity读取成功；
- canonical validator、retained audit、eligibility emission、release consumption、network、device与FORMAL均为`0`；
- first failure发生在focused/full/synthetic之前，因此三者actual均为`0`。

## 3. 三项独立finding

### 3.1 Governance identity不是current-file drift

PLAN冻结的`842cfad0...`并不是
`advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md`的SHA。该Git文件自
`3e2ebed...`加入后到current内容一致，实际bytes `6754`、SHA-256
`5b23cbdfe97ac71e7438f1d30461455938828029c0ba32e931a9570e0ea88a34`。

`842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`
属于exact external decision evidence：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json`

该文件bytes `7066`，自身声明`status=advisor_decision_required`且`accepted=false`。它是
Advisor请求前的canonical lineage-owner decision evidence，而不是Advisor最终决策文本。

实际Advisor Option-B决策由attachment承载：

`/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt`

其bytes `11146`、SHA-256
`91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`，与B2
manifest baseline下一位置一致。Governance manifest `69bbbb...`及GUIDE `659152...`
也与current/Git identity一致。

因此B2 immutable manifest的正确positional provenance语义应为：governance manifest、GUIDE、
lineage-owner decision evidence、Advisor Option-B attachment、Human governance override、helper
disposition。现有production dataclass字段名`advisor_decision_sha256`与后续PLAN路径映射把第三项误称为
Advisor decision，形成治理身份misbinding；不能以current Advisor request file drift解释。

### 3.2 Handoff不是physical EOF append

Activation parent ER为bytes `1293091`、SHA-256
`f0bf45501ae31d700eb3d0095d01d881b2a35ae1c17717936b36ec0a95240413`。
Evidence ER为bytes `1301614`、SHA-256
`6c2ccf6170aca4e1b51b1192b1be93ab0a43457063ac3675be5afb052c64128c`。

新块在byte offset `2579`插入，insert bytes `8523`、SHA-256
`3bf15b37db7711bfeb343fbd0a89b394a9db8fc82aab06fab4dbd464d64d9412`；
其后完整保留旧suffix bytes `1290512`、SHA-256
`926777941aa912f6bc08a2a32e13b65e34fc8d05fc6d675757259c7239a25d1d`。
所以payload内`physical_eof=true`、`append_last=true`是错误声明，违反active PLAN的exact
physical-EOF evidence lifecycle。

### 3.3 未授权CodeGraph probes

Payload记录`codegraph_queries_before_controller=3`。Active PLAN未授予CodeGraph query预算，且
Orchestrator明确不需要额外probe。它们虽然没有改变scientific/retained结果，仍是执行范围与计数合同偏差。

## 4. 决定、残余风险与exact next branch

本handoff不得credit为B3-C1-C1通过，也不得credit为合规的terminal failure handoff。
`RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator sole eligibility owner、release/device/FORMAL锁保持不变。

Exact next branch为`REF-P7-25-R2-B3-C1-C1-S1` Git/ER-only supersession：只使用committed Git
objects复核上述三项并在ER真实physical EOF追加exact one canonical terminal supersession block；不得读取
external governance/real/retained artifacts，不得运行CodeGraph、tests、controller、validator或audit。

该supersession被Planner接受后，Orchestrator应进入一个独立governance identity correction package：

1. 保持sealed B2 manifest five及old/new payload bytes immutable，不repair/regenerate；
2. 把baseline第三SHA的owner明确为exact lineage-owner decision evidence path `842cfad...`，第四SHA保持Advisor Option-B attachment `91a88...`；
3. 修正production spec/dataclass与dedicated test中误导的`advisor_decision_sha256`命名/绑定，并让未来self-check核对正确exact path；
4. focused/full/synthetic通过前不得进入retained real audit；最终eligibility仍只能由existing canonical validator产生。

维护性判断：问题位于一次性evidence lifecycle与M1 baseline治理字段边界；先做Git/ER supersession，再以原owner和dedicated test完成窄治理身份修正，可避免修改immutable payload或新增平行provenance owner。
