# REF-P7-25-R2-B2-P7：pre-edit CodeGraph ordering failure review

**Planner 日期：** 2026-07-31

**Reviewed reference：** `REF-P7-25-R2-B2-P7`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-REPO-OWNED-RUNNABLE-DOMAIN-TEMPLATE-CORRECTION-V1`

**Planner decision：**
`REJECTED_PRE_EDIT_CODEGRAPH_QUERY_BEFORE_REQUIRED_SYNC`。

本拒绝只针对 active PLAN 的 CodeGraph 顺序冲突。Executer遵守 repository-level
CodeGraph-before-read规则，在任何 source理解或编辑前运行了 exact one `codegraph explore`，但 active PLAN同时冻结
`codegraph sync` 后再运行唯一 query。已经发生的 query不能被追认成 sync之后的 query，也不能通过第二次 query补救；因此
retry/fallback `0/0`下正确 fail closed。没有 runnable-template实现候选，也没有 external或retained effect。

## 1. Frozen inputs and topology

- Review evidence HEAD：`778576e1bc1df797e0293d52fa58dfe4fc385744`，direct parent
  `d0825454d7ed073287fe2f4ac1942f3537597dc0`，subject
  `chore(evidence): record p7 codegraph ordering stop`，changed path exact
  `.agent-work/EXECUTION_RESULT.md`；review开始时 worktree clean。
- Activation：`d0825454d7ed073287fe2f4ac1942f3537597dc0`，direct parent
  `74dddff36d02d908934a9b65db018169f9966b8e`，subject
  `chore(plan): activate p7 runnable template correction`，changed paths exact FULL、PLAN和
  `.agent-work/PLANS/20260731-1647-p7-retained-r3-b2-p6-validation-acceptance-review.md`。
- Reviewed active PLAN SHA-256：
  `563625bc1451f9b0f645632cab5aa53539921ef2d7e60b847a5159499cee6640`。
- Prior archive：bytes `6337`，SHA-256
  `14e77f490188c9def0cf332b2a5d1c5059edb4283a2d160f0c6688598f1dd971`。
- Accepted P6 candidate：`48b3979d6c0df5f488cd500597e26dc4c38877dd`，direct parent
  `478d8c52e4a21d6628219e27b88b507d736f3aca`，subject
  `chore(p7): retain rejected p6 c1 c1 c1 guard candidate`，changed path exact dedicated test。
- Accepted P5 runtime owner：`37f7d0021c7a81a9d6680815bc51c305cf807a7b`，direct parent
  `099d1ad833c3e73b7dc157f5786ad66bb6718f5e`，changed paths exact runtime module与dedicated test。
- Frozen current source blob/bytes/SHA-256：
  `a1e196664840bc340be789829b8cf0826c9ec7f4` / `13918` /
  `56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`。
- Frozen current test blob/bytes/SHA-256：
  `eb943384817996b96e332c83f618ba82cf210d4a` / `12992` /
  `6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc`。

## 2. Validation quality and decision

Executer handoff与committed evidence证明：

- activation、active machine contracts、source/test baseline、P6 candidate和P5 runtime owner身份全部通过；
- 任何 source理解或编辑前，pre-edit CodeGraph query exact `1`、exit `0`；
- active PLAN要求的先 sync 后 unique query已不可满足，因为 sync `0/1`而query `1/1`；
- code/test writes、targeted、focused、compileall、full、CodeGraph sync、second query、diff/static gates、commit、
  postcommit targeted全部 `0`；
- external controller/source/root/process、synthetic integration、old evidence、retained/candidate payload、validator、eligibility、
  release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、FORMAL及later stages全部 `0`；
- retry/fallback `0/0`，ER仅追加一次，未改 PLAN/FULL/archive/debug/GUIDE/RESEARCH。

这是一项可独立确认的流程合同缺陷，不是 production/template实现失败，也不改变 P5/P6 accepted status。
`RETAINED_UNVALIDATED_UNCONSUMED`继续成立；P7未产生可消费候选。

## 3. Exact corrective branch

- Reference：`REF-P7-25-R2-B2-P7-C1`
- Contract：
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1`
- Implementation scope与P7保持不变：exact domain-template module及dedicated test two paths，runnable合同不降级。
- 唯一流程修正：activation/baseline身份核对后，在任何 source/test content理解、grep/find或编辑之前运行 exact one
  `codegraph sync`，紧接 exact one `codegraph explore`；该query同时作为本包唯一和最终CodeGraph ownership证据。
- 编辑及所有validation后 CodeGraph sync/query均为 `0`。本包不跨project边界，不要求第二次图更新，也不得以“final query”为由
  重复调用；product behavior由fresh targeted `11/11`、focused `93/93`、compileall、unique full `778/778`、exact diff/static
  gates和postcommit targeted `11/11`验证。
- Exact implementation subject仍为 `fix(p7): make retained controller template runnable`；retry/fallback `0/0`。
- Stop：`B2_P7_C1_CODEGRAPH_PREFLIGHT_ORDER_CORRECTION_WAITING_PLANNER_REVIEW`。

## 4. Residual risks and locks

Pre-edit CodeGraph只能证明编辑前的owner routing与blast-radius边界，不能单独证明post-edit bytes；因此success acceptance必须同时
依赖本包冻结的fresh tests、AST/effect-free harness、exact two-path diff及commit topology。External controller/source/root/process、
synthetic integration、retained R3、canonical validator、eligibility、release、network和device routes继续hard locked `0`。

维护性判断：纠偏只消除执行顺序自相矛盾；template/runtime/provenance/conformance/lifecycle owner边界、代码范围与验证深度均不变，
无需新增helper、framework或后续架构清理。
