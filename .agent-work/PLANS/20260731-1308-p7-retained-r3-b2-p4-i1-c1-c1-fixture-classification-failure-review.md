# REF-P7-25-R2-B2-P4-I1-C1-C1 fixture-classification failure review

**Planner 日期：** `2026-07-31`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-C1-FIELD-ONLY-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**Decision：**
`REJECTED_DUPLICATED_EXTERNAL_TRANSPORT_CLASSIFIER_FALSE_POSITIVE_REPO_OWNER_CORRECTION_REQUIRED`

**Exact next branch：** `REF-P7-25-R2-B2-P4-C1`。下一包不是又一次 external source retry，而是
exact现有两个repo paths内的bounded owner correction：让accepted conformance owner在同一次runtime-source分析中
输出exact transport-domain report，区分effect-owned live results、唯一required immutable
`RootIdentityChain` composition与pure in-memory negative-fixture identities。后续external source只能消费该报告，
不得实现第二AST classifier。

## 1. Reviewed topology and frozen failure identity

- Activation commit：`53df8ca0611b05819e500c9376c6f150b48511cd`，direct parent
  `972f82465fa5d9671dba12a0570103bd1b9fb6af`，subject exact
  `chore(plan): activate p4 field-only integration qualification`；exact changed paths为FULL、PLAN与前次review archive。
- Evidence commit：`697f9f1800a91442695f23d551a8d1a5f5cb9624`，是activation direct child，subject exact
  `chore(evidence): record p4 fixture classification failure`，只修改 `.agent-work/EXECUTION_RESULT.md`。
- Updated debug/current reviewed HEAD：`781e410c43774c20da9f00e8c9e0f5bfd27b1f66`，是evidence direct
  child，subject exact `docs(debug): reassess p4 transport classifier ownership`，只修改
  `.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md`。
- Immutable failed source：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-c1-controller-972f824.py`，
  bytes `32216`，SHA-256
  `a9d982f88bc75ef09e029ce4311a46f3e9f59264fed86c98e1bb5fc284122010`。本review只采用committed ER、
  updated debug与Orchestrator冻结事实，不读取source或任何external root。
- Frozen output root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-c1-qualification-972f824`
  保持absent；本review不访问该path。

## 2. Evidence quality and exact result

唯一controller process为 `1`、exit `1`。Source exclusive创建一次、accepted provenance owner exact读取一次，
同一in-memory bytes完成strict UTF-8 decode、AST parse、builtin compile与dispatch。Accepted
`analyze_controller_source`调用一次并PASS，exact `18` bound results；这继续证明现有owner surface、direct binding、
known attributes与shared-root read检查没有漂移。

随后一次性external bounded gate在所有effects前以stable exception
`live_owner_transport:drift_root:Call` hard-fail。被拒绝的语句是PLAN-required pure in-memory case 11：
`FileIdentity(root=drift_root)`。`drift_root`来自pure in-memory `DirectoryIdentity` fixture，不是I/O/effect owner返回的
live identity，也没有跨callback或container运输。该结果是一次性gate把所有owner-typed names混成单一live-name
集合造成的false positive；不是accepted analyzer failure、repo owner drift、I/O结果或科学结论。

Effects exact全零：Git ledgers `0/6`、root `0/1`、synthetic writes/reads `0/4`、matrix `0/16`、qualification
`0/2`、terminal/seal `0/2`、admission `0/1`、final artifacts `0/9`。Retry、fallback、second source/root/process、
rewrite/rerun/delete/cleanup均为 `0`。失败/旧source/root/evidence、accepted C1、retained R3、real B2、manifest、
canonical validator、eligibility、release、network/device与later stages均未访问。证据足以拒绝当前package并重定向
owner边界；它不证明16-case semantics，也不授权重跑。

## 3. Findings

### REV-B2-P4-I1-C1-C1-001 — external transport gate confuses fixture construction with live transport

Severity：blocking false positive；ownership：repo conformance owner缺少transport-domain report。

一次性gate只按绑定名是否具有owner类型分类，无法区分 operational/effect owner call result 与直接dataclass
constructor产生的pure in-memory fixture。于是合法的fixture-to-fixture constructor edge
`FileIdentity(root=drift_root)`被当作跨边界live transport。后续不得通过变量名、callee/path allowlist或再生成一套
external AST walker修补；分类必须由repo owner基于call provenance与exact AST shape一次完成并写入immutable report。

### REV-B2-P4-I1-C1-C1-002 — transport ownership is duplicated outside the accepted analyzer

Severity：blocking architecture/maintainability finding。

Repo analyzer已拥有owner schemas、constructor/call bindings、attributes、root reads与alias规则，但external source另建
transport classifier，导致同一AST节点由两个不同规则集解释。I1-C1报告过live container/call occurrences，本轮又误拒
pure fixture，证明继续one-off source retry只会扩大平行ownership。最小纠偏是在现有module扩展现有analysis pass，
由同一binding registry输出transport report；external consumer只检查report exact值，不再遍历AST做transport判定。

### REV-B2-P4-I1-C1-C1-003 — exact domain semantics must remain fail closed

Severity：blocking acceptance contract。

Repo owner必须以调用来源和结构而非名字推断domain：operational owner calls返回effect-owned live result；直接
`DirectoryIdentity`/`FileIdentity` constructors可形成isolated pure in-memory fixture graph。Fixture identity仅可进入
另一个exact owner-dataclass constructor或pure in-memory negative chain，不得把effect result伪装为fixture。
Effect-owned live result的alias、普通container、generic helper/call argument、callback return与closure transport仍须
stable reject。唯一effect identity grouping exception是named-field exact
`RootIdentityChain(before=..., files=(...), after=...)`，且只能direct传给
`validate_root_identity_chain`；禁止generic path/call allowlist。

### REV-B2-P4-I1-C1-C1-004 — existing owner baseline remains accepted but incomplete for integration

Severity：scope/closure record。

Implementation `83bb193259fcf1de5b3f78798001e83496c2daae`的existing source/test topology、14 dedicated methods、
focused `70/70`与final-source full `755/755`仍是可信baseline；本finding不推翻这些测试结果，但证明它们没有覆盖
transport-domain ownership。新package必须从actual baseline `755`增加exact meaningful methods，并以新final source的
targeted/focused/full/compileall/CodeGraph/双路径commit/postcommit证据重新建立acceptance。

## 4. Decision and bounded repo-owned P4 successor

Decision：
`REJECTED_DUPLICATED_EXTERNAL_TRANSPORT_CLASSIFIER_FALSE_POSITIVE_REPO_OWNER_CORRECTION_REQUIRED`。

新任务 `REF-P7-25-R2-B2-P4-C1` 只允许修改：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`；
2. `tests/test_p7_retained_r3_controller_conformance.py`。

Implementation必须扩展现有single owner，而不是新建module/service或第二classifier：

- 同一次 `analyze_controller_source` parse/binding pass产出immutable exact transport-domain report；
- report列明effect-owned bindings、pure-fixture bindings、fixture composition edges、exact root-chain compositions与
  effect transport occurrences；PASS report的prohibited occurrences必须为空；
- call provenance区分operational owner result与direct dataclass constructor fixture，case-11 shape合法；
- effect identity alias/container/generic helper/callback/closure运输继续stable reject；
- 只允许exact immutable `RootIdentityChain` named composition及direct validator use，不得generic allowlist；
- 加exact六个meaningful dedicated regression methods，覆盖positive report、case-11 fixture、effect-to-fixture masquerade、
  alias/container/helper negatives、exact root-chain exception和deterministic exports/report；
- targeted必须由14变为`20/20`，原focused baseline 70变为`76/76`，actual full baseline 755变为`761/761`；
  compileall、CodeGraph sync、exact双路径diff/commit与postcommit targeted均须通过。

本包不创建/读取external source/root，不运行synthetic integration或retained/real-B2流程。Repo owner correction通过后，
Planner才可决定一个后续consumer integration包；该包必须只消费repo transport report，禁止实现任何第二AST transport
classifier。

## 5. Proposed FULL transition and locks

- `REF-P7-25-R2-B2-P4-I1-C1-C1` →
  `REJECTED_DUPLICATED_EXTERNAL_TRANSPORT_CLASSIFIER_FALSE_POSITIVE_REPO_OWNER_CORRECTION_REQUIRED`。
- 新增 `REF-P7-25-R2-B2-P4-C1` → `READY_FOR_ORCHESTRATOR_ACTIVATION`。
- `REF-P7-25-R2-B2-P4` existing baseline记为
  `ACCEPTED_BASE_REOPENED_FOR_TRANSPORT_DOMAIN_SUCCESSOR`，不把旧755结果误称为新correction证据。
- `repair_v2_status` → `P4_TRANSPORT_DOMAIN_OWNER_CORRECTION_PENDING`。
- `retained_r3_status`保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- external sources/roots、failed source/root、accepted C1、retained reads、Git provenance replay、real B2、manifest、
  validator、eligibility、release、network、device、FORMAL与所有later stages继续hard locked `0`。

Planner只创建本archive并重写active PLAN；FULL、ER、debug、GUIDE、RESEARCH与production/test files保持只读且不提交。
Orchestrator须独立审核、更新FULL并创建exact activation commit后，才可dispatch corrective Executer。

维护性判断：当前缺口跨越AST ownership和shared provenance边界；继续one-off gate会形成重复owner。Exact双路径修复把
transport classification并回已有pure-in-memory conformance module，仍与I/O、validator、release和科学owner隔离；
六个新增回归方法与761 full baseline保护新边界，完成后无需额外抽象或架构重构。
