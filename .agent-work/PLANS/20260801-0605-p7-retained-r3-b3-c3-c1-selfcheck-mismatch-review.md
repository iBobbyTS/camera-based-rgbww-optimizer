# P7 retained-R3 Option B：B3-C3-C1 self-check mismatch review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C1-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V1`

**Planner decision：**
`REJECTED_UNATTRIBUTED_TOP_LEVEL_MISMATCH_REQUIRES_DURABLE_FACT_DIAGNOSTIC`

## 1. Reviewed scope and method

Planner只读审核了committed active PLAN、activation/evidence Git topology及evidence commit中
`.agent-work/EXECUTION_RESULT.md`的physical EOF append。没有读取B3-C3-C1失败fresh package/root、real manifest、retained R3、
C1 external inputs、工作树production/test源码或失败controller source；没有运行test、controller、CodeGraph、validator、audit、
release、network或device操作。

Reviewed topology：

- activation `6589f5e593d15e3191fc1e492b069fd51ea88a85`是
  `b22cdafc8ab0b6e2e5a25b695edf325e7d782a6c`的direct child；subject为
  `chore(plan): activate byte-stable postcommit verification`；changed paths恰为FULL、PLAN及上一轮review archive三项；
- evidence `b923f4efb89a45705ed9af35cf5f53bf65ef8526`是activation的direct child；subject为
  `chore(evidence): record B3-C3-C1 byte-stable verification`；changed path恰为
  `.agent-work/EXECUTION_RESULT.md`；
- ER parent bytes `1323360`、SHA-256
  `64c1c937bfa986d3b1738c75c38ae86781188e2929b3f675c84e985c792a9ec2`；evidence bytes
  `1327409`、SHA-256 `594615188d35bc6c31833d0064c2fbeb32626cbee15226483f21cb936e69e50d`；
  physical EOF append bytes `4049`、SHA-256
  `919b598821849c6a29d0074a64e29580817818a42ce5cd611e6c7d0bb651494e`，且文件以LF结束；
- `git diff --check 6589f5e..b923f4e`通过；Planner检查时porcelain clean。

## 2. Accepted execution facts

Non-TTY controller transport成立：fresh root absence/mkdir各1，root mode0700，source mode0600，source通过exact path argv启动，
TTY false、stdin source bytes 0，source pre/post identity相等；outer controller exact1并以exit1 terminal。Machine-row读取/解析计数
为repository file decodes `2`、row extractions `2`，Git reads `7/36 max`。ER仅在controller terminal后以第二次
`apply_patch`追加一次，append后operations `0`。

执行在`real_manifest_top_level_frozen_fact_check`以
`ValueError: manifest top-level mismatch`进入`BR-SELF-CHECK`。Focused/full/synthetic均0，retry/fallback均0；canonical
validator、eligibility、release、network、device及全部later-stage zero locks均报告0。Retained状态仍为
`RETAINED_UNVALIDATED_UNCONSUMED`，canonical lineage validator仍是唯一eligibility owner。

## 3. Findings

### REV-B3-C3-C1-001 — mismatch不可归因

Failure payload没有序列化controller实际采用的exact expected top-level facts，也没有序列化observed manifest top-level JSON
type、keys和value summary。因此现有字符串只证明某个内部比较失败，不能区分：controller把已知subset错误地与整个object比较、
controller冻结了PLAN并未授权的额外key/value、或真实manifest的已知合同字段确实不匹配。它不能证明manifest defect，也不能授权
manifest repair、schema放宽、generic selector、real-input重写或B4。

Committed PLAN与accepted manifest contract目前只足以冻结以下top-level acceptance facts：JSON type必须为object；
`schema == "p7_retained_r3_audit_provenance_manifest_v2"`；
`status == "sealed_subordinate_provenance_evidence"`；`immutable is true`。PLAN没有冻结完整top-level exact key set，
所以successor不得把观测到的完整keys误升格为新的schema allowlist，也不得要求whole-object等于这三个字段组成的subset。

### REV-B3-C3-C1-002 — terminal residual-process proof不完整

Payload报告`process_table_scans=0`，且没有序列化`owned_residual_processes`集合。同步outer process已terminal并不等同于对owned child
残留做了计划要求的独立terminal proof。Successor必须在每个terminal branch的ER append前执行exact one bounded owned-process
scan并记录空集合或具体残留；不得cleanup、kill或retry。

## 4. Decision and residual risks

B3-C3-C1 execution按合同正确fail closed，但不通过工程postcommit verification。既不接受新manifest defect，也不接受对manifest、
schema或selector的任何修复。下一包必须使用全新root和全新non-TTY controller，在对同一次read得到的manifest做pass/fail判断前，
先durably写出并seal一个observed top-level fact diagnostic。Diagnostic只用于归因；acceptance仍只能由committed PLAN明确列出的三项
top-level facts及既有全部冻结self-check决定。

同一fresh package可以继续后续阶段，但仅限以下清晰分支：

1. 若diagnostic artifact成功落盘/seal，且known type/schema/status/immutable四项全部匹配，则在同一controller、同一内存snapshot中
   继续其余self-check；self-check全部通过才依序运行focused exact1、full exact1、synthetic exact1。
2. 若任一known fact mismatch，或diagnostic写入/seal失败，则立即停止，后续阶段全0；payload必须引用durable expected/observed事实和
   exact mismatch，不得宣称未被这些事实直接证明的manifest defect。
3. 无论分支，terminal前做exact one owned-process scan；任何失败保留fresh package，不复用B3-C3/C1失败root，不retry、不fallback。

Residual risk是完整top-level key set并非accepted contract；因此observed key list和各key value summary必须是diagnostic-only，不能被
当作generic schema、path allowlist或新eligibility owner。B4、real retained audit、validator、eligibility、release及全部设备阶段保持锁定。

## 5. Exact next branch

Next reference task：`REF-P7-25-R2-B3-C3-C2`。

Next contract：
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C2-DURABLE-TOP-LEVEL-FACT-DIAGNOSTIC-V1`。

Planner stop：
`B3_C3_C2_DURABLE_TOP_LEVEL_FACT_DIAGNOSTIC_WAITING_PLANNER_REVIEW`。

维护性判断：下一包仍为一次性外置controller，不新增production owner；durable diagnostic把比较依据从异常字符串提升为可审计事实，
并且保持accepted manifest contract与canonical eligibility owner边界不变。
