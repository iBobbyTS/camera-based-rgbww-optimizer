# P7 retained-R3 Option B：B3-C2 governance identity correction 验收归档

**审核日期：** `2026-08-01`

**Reviewed task：** `REF-P7-25-R2-B3-C2`

**Activation：** `8e5d4ea520fd5aa5edb41af7b574188b47596bc3`

**Evidence / implementation commit：** `e84f5b6adc7c004b388074f5e81a4d109a6541f2`

**Planner decision：**
`REJECTED_EXECUTION_BUDGET_ACCEPTED_COMMITTED_IMPLEMENTATION_PENDING_TERMINAL_SUPERSESSION`

## 1. 审核范围与方法

Planner独立只读检查active PLAN、activation/evidence commit metadata、exact changed paths、two-path
patch、committed `EXECUTION_RESULT.md` parent/child bytes、physical EOF suffix及末尾strict JSON payload；独立重跑
dedicated targeted与focused suites。未读取retained R3、old B2 manifest、external governance evidence、Advisor
attachment或old external evidence；未调用CodeGraph、controller、canonical validator、retained audit、release、network或
device，也未运行full suite或public analyzer。

Activation commit以`751a04d14c263853d56836049ce1bb3038a5e990`为parent、subject为
`chore(plan): activate B3 governance identity correction`，changed paths exact为FULL、PLAN与上一review archive。
Evidence commit以activation为parent、subject为`fix(p7): correct manifest governance identity`，changed paths exact为：

1. `.agent-work/EXECUTION_RESULT.md`；
2. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`；
3. `tests/test_p7_retained_r3_real_manifest_domain_template.py`。

`git diff --check`通过，review前后worktree clean。

## 2. Implementation identity 与验证

Two-path diff只做existing owner的语义命名纠偏：

- `RealManifestBaselineIdentity.advisor_decision_sha256`改为
  `lineage_owner_decision_evidence_sha256`；
- builder唯一字段访问同步改名；
- dedicated test的dataclass字段顺序及baseline position 8访问同步改名，并新增length、legacy identifier、canonical
  template/golden replacement冻结断言；
- 没有新增manifest字段、serializer、path allowlist、controller、validator或parallel owner。

独立identity重算：

- source post SHA-256：`da8b24b9530d387befde8eda3f0ee0dcfca373e28f27a6bda3433c4f4bf5f410`；
- test post SHA-256：`193464af34c10809b91987f984a4b7ce40f924df66a472511acbd6fb5142b378`；
- exact two-path binary diff SHA-256：
  `2685d00525d90f725ed3c73ca7adeebcf9bb5ade14c39dc4172d725fa9d741c0`；
- Executor evidence：targeted `13/13`、focused `83/83`、compileall pass、full `800/800`、CodeGraph pre-query
  `1` / sync `1`、diff check pass；
- Planner独立复跑：targeted `13/13`、focused `83/83`。

Serialized baseline仍为12 positions，position 8 value仍是原lineage-owner decision evidence SHA，position 9仍是
Advisor attachment SHA；canonical template SHA `a83804d2...`与golden replacement SHA `55c43ad3...`未变。
因此实现候选及其focused行为可接受，无需回退、改写或再次编辑code/test。

## 3. Execution contract finding 与决定

Active PLAN明确冻结`repository_code_reads_max=1`及`repository_test_reads_max=1`。Executor在pre-edit读取后又各做
一次post-edit direct scan，实际均为`2`。虽然第二次读取是只读identifier/hash核对，发生在code edit与全部测试之后，
没有扩大write scope、改变artifact或触碰locked inputs，但它仍是不可追溯消除的exact budget violation。

因此本轮不能取得PLAN允许的success outcome
`B3_C2_GOVERNANCE_IDENTITY_CORRECTION_VALIDATED`，也不能整体标为accepted。Planner同时确认该偏差不污染已提交
two-path implementation：拒绝的是execution conformance，不是code candidate。保留commit `e84f5b6...`，禁止重新编辑、
重跑本实现包或伪造历史actual为预算内。

ER lifecycle独立重算通过：

- parent ER bytes `1309616`，SHA-256
  `f0474fcc4b6f835d91c9483f4923b9ca50f54ce3b0fa7816ca2be32caeee7546`；
- evidence ER bytes `1314849`，SHA-256
  `ff23fe99b2819bae2c90542f7ea1ddd42445553363960ac1a5e35a182ae8f33f`；
- parent是evidence的完整prefix，physical EOF suffix bytes `5233`，SHA-256
  `66ec9bb4cccbc33e93ef461cf311c895e1ca9dec4afd9eb879b9ecd570470be9`；
- EOF payload为strict canonical JSON，准确记录`actual=2/2`、first failure、zero locks与
  `FAIL_EXECUTION_READ_BUDGET_EXCEEDED_IMPLEMENTATION_VALIDATED`，没有虚报成功。

## 4. Locks、残余风险与exact next branch

`RETAINED_UNVALIDATED_UNCONSUMED`保持不变；canonical lineage validator仍是唯一eligibility owner；B4、release、
device、FORMAL-R6、strip、TD-C、sentinel与P8继续锁定。本轮不生成eligibility，不credit real retained audit。

唯一残余问题是repository ledger尚未以一个独立terminal block明确区分“B3-C2 execution rejected”与“committed
implementation accepted for future verification”。下一唯一包为`REF-P7-25-R2-B3-C2-S1` Git/ER-only budget
supersession：只使用committed Git objects和本archive，复核e84f5b6 parent/subject/path/blob/diff及ER EOF identity，
然后在ER physical EOF追加一个canonical terminal block。不得再读或改code/test，不得重跑测试、CodeGraph、controller、
validator、audit、release或设备路径，不得修改旧payload。

S1被Planner接受后，Orchestrator才可规划fresh postcommit self-check/test/synthetic verification；它仍不得直接进入real
retained audit、eligibility或release。

维护性判断：implementation仍位于单一frozen dataclass/builder owner及dedicated test；后继只封存execution-budget
偏差与accepted candidate identity，不增加production abstraction或平行provenance owner。
