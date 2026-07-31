# REF-P7-25-R2-B2-P4 implementation / evidence review

**Planner 日期：** `2026-07-31`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-CONTROLLER-CONFORMANCE-COMPOSITION-OWNER-V1`

**Decision：**
`REJECTED_VALIDATION_EVIDENCE_GAP_CODE_SCOPE_ACCEPTED`

**Exact next branch：** `REF-P7-25-R2-B2-P4-V1`，只运行 final committed source 的
一次 exact full `755/755` validation；不改代码，不运行 external controller。

## 1. Frozen implementation identity

- Activation commit：`5f2483c319b395b2aef2a43f4827b4c150f3f3fd`，parent
  `102c625eb73cf49d7e14af12663f967397e28fa2`，subject exact
  `chore(plan): activate b2 controller conformance owner`，changed paths exact 为
  FULL、PLAN 和 `20260731-1106` review archive。
- Implementation commit：`83bb193259fcf1de5b3f78798001e83496c2daae`，direct parent
  `5f2483c319b395b2aef2a43f4827b4c150f3f3fd`，subject exact
  `feat(p7): add retained controller conformance owner`。
- Implementation changed paths exact：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py` 与
  `tests/test_p7_retained_r3_controller_conformance.py`；blob OID 分别为
  `52fcdc73c69e367cd1b046b52d83ffc555a6d496` 与
  `28a58c6051de378fbcc6485c316df9ff10d3a90c`。
- Final source/test SHA-256：
  `94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7` /
  `447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726`。
- Evidence commit：`de50071cd21a2459a9f68aca5e4357fe7d86abae`，direct parent
  `83bb193259fcf1de5b3f78798001e83496c2daae`，只修改
  `.agent-work/EXECUTION_RESULT.md`。

## 2. Evidence reviewed

- Dedicated test surface exact `14` methods；targeted `14/14` pass。
- Precommit focused `70/70` pass；compileall pass。
- CodeGraph sync invoked once and reported current；`git diff --check` pass。
- Postcommit focused against final committed source `70/70` pass。
- Full suite process只启动一次，但其terminal exit/count/output没有被保留；并且上述final source
  在该full process启动后又进行了public-method attribute allowance和root/file mode两处
  fail-closed调整。因此该process不能证明commit `83bb193`的final source，不能记为
  `755/755`。
- External controller、evidence root、retained R3、real B2、canonical validator、eligibility、
  release、network、device与scientific操作均为 `0`。Retained R3仍是
  `RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Findings

### REV-B2-P4-001 — final-source full evidence absent

Severity：acceptance blocker；code finding：否。

原PLAN明确要求final source的quiet full suite exact `755/755`。现有full process没有可恢复的
terminal证据，而且运行时source并非最终commit内容。Focused与targeted通过不能替代该验收项。
因此P4整体不能验收，但没有理由修改或回滚exact两文件implementation。

### REV-B2-P4-002 — lifecycle wording overbroad, implementation semantics accepted

Severity：plan-contract ambiguity；code finding：否。

原machine row的单一布尔字段 `failure_terminal_attempted_once=true` 若脱离详细正文，可能被误读为
conformance callback失败后也必须写terminal。实现与原PLAN的effect boundary实际表达两类不同失败：

1. `conformance` 是任何effect callback之前的pre-effect gate。它失败时直接重新抛出原异常，
   terminal、terminal seal和admission均为 `0`；这防止未通过conformance的controller产生证据副作用。
2. `activation`、`root`、`inputs`、`evaluate` 才是sealed primary phases。它们之一失败后，
   terminal恰好尝试一次；terminal成功后seal恰好尝试一次；seal成功后admission恰好尝试一次，
   最后保留原primary exception identity。

`execute_controller_lifecycle` lines 380–415 与 dedicated tests 11–13 实现并冻结了这一区分。
这与“conformance before effect callbacks”和正文“primary phase failure”一致，不构成代码缺陷。
Successor PLAN必须以结构化字段明确拆分，不再使用未限定的
`failure_terminal_attempted_once`。

## 4. Architecture / maintainability assessment

Second-pass架构收敛可接受。新增owner是pure in-memory边界，复用既有machine-contract、
preparation与provenance I/O types，不引入external I/O、validator、release或scientific authority。
Runtime AST与negative fixture解析域分离；root identity chain与lifecycle composition均由单一owner
负责。14个dedicated tests覆盖反复出现的owner-field、root-binding与terminal-order漂移。
没有发现需要exact两路径code correction的真实finding；当前最小动作仅是补足final-source full
validation。

## 5. Acceptance decision and residual locks

P4 implementation scope与ownership接受，但P4 package因 `REV-B2-P4-001`拒收。下一分支只能：

- 只读证明HEAD ancestry、exact implementation/evidence commits、exact two paths、final hashes与
  exact 14 methods；
- 对commit `83bb193`的final files运行一次冻结full command并要求exact `755/755`、exit `0`；
- append一次ER handoff并停止。

不得修改code/test，亦不得补跑targeted/focused/compileall/CodeGraph，除非Planner另行开包。
External controller、retained read、real B2、manifest、canonical validator、eligibility、release、
network、device、FORMAL与later stages继续hard locked。

## 6. Proposed FULL transition

- `REF-P7-25-R2-B2-P4` →
  `REJECTED_VALIDATION_EVIDENCE_GAP_CODE_SCOPE_ACCEPTED`。
- 新增并激活 `REF-P7-25-R2-B2-P4-V1` →
  `READY_FOR_ORCHESTRATOR_ACTIVATION`。
- `repair_v2_status` →
  `P4_IMPLEMENTATION_RETAINED_FINAL_SOURCE_FULL_VALIDATION_PENDING`。
- `retained_r3_status`保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- 所有external/release/device/scientific locks保持不变。
