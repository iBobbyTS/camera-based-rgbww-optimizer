# P7 R2-D1 evidence-to-release decision review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `6bcd090f93c4be64b5514b0a4caf524c30bb13bf2a90bc862cb0301abd82f39c`

**Reference task：** `REF-P7-04`

**Decision：** `accepted_release_harness_preparation_required_before_invocation`

## 1. Independent verification

D1 root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-r2-release-decision-d1-offline/20260726T150000Z`。

Decision candidate regular JSON、status `eligible_waiting_for_planner`、SHA
`ac451f77929592222ad1de807381de444287dd2bee91d0310b42903123fbee42`；production usability、release
generation/validation/consumption、execution/device/live/formal authority全部false。Future template SHA
`ee5adcc87e195d8ccf9bf329978a8f7d7c5ac50b1ee36da5d89817eb6e024ce4`，status
`prepared_non_authorizing_waiting_for_later_plan`，output/later PLAN/authorized contract null，budget0/1、retry false，argv exact。

R2 contract/marker/audit/status/evidence 与H4 owners全部physical path/bytes/hash/mode/schema/status重验通过；17 个preparation
targets逐个actual regular/non-symlink bytes/hash exact。Evidence audit checkpoint52a是target1e3的direct parent，evidence SHA
unchanged。Setup checkpoint→target changed-path ledger独立git重算57条，与candidate ledger逐项相同；sorted/deduplicated、
classified57/57、prohibited/unclassified empty；ledger SHA
`8b09481f24cf14e43682a24c2550210e4b02f282a32101189af148bfba229ddb`。

Final fake consumer matrix `91/91`，SHA
`3ba609e65a00b5c0f3e6cb82b6417788b9face8e7905ddd59da368443e866f27`；positive仍non-authorizing，全部
required negative branches pass。Strict JSON17/17、authorization true0；validation SHA
`2d4238c21962882c2dde65d1c193aeb00b4ac3ca607d7a0acecd0196b3e403ee`。Production release writer
import/call/invocation0；immutability/residual/budgets exact。

首轮90/91因external validator把preparation实际0600错写0644而fail closed；failure record SHA
`f58647dca4b061d42d1aa4c15f1f7f0dd3a9081daa778de5cb951341e27c2f29` 与superseded matrix SHA
`2dfbb4c2782fc3fd6c9e93e72f58199b202146276551ecf0752728587976d273` preserved。仅修external fact并用fresh
fixtures-v2重跑，符合D1纠偏范围。

上次agent transport502发生在D1 root仍为空且production/project network/release invocation0的状态；恢复未重复任何production
动作。FULL initial `f6ea3bda...5841`→current `a9462f7e...a296` 是Human解除设备暂停后Orchestrator的授权治理更新，非Executor
drift；D1自身范围保持纯离线。EXECUTION_RESULT §119 SHA
`75ea57859e697b4e78fc5682db171d6aa3ec734c0c48d67e813ee7e71a135123`。

## 2. Acceptance and residual risk

D1 **接受**。它证明evidence→release eligibility和exact command语义，但不授权或生成release。

Residual risk：production release child将生成current-lineage-candidate、resolved-formal-plan与setup-lineage-release三份互相
绑定artifact；D1尚无独立child exit、terminal audit、三文件cardinality/schema/status/hash/public validation owner。直接执行
template会降低失败取证质量，因此先建立一个纯离线release-specific harness/gate。

Human已解除旧设备暂停，但release harness包仍是纯离线；后续device/live/formal必须由active PLAN按具体target/range/duration/
abort/cleanup边界另行授权。Release success也不自动授权这些动作。

## 3. Exact next branch

发布 bounded `R2-D2-OFFLINE-RELEASE-HARNESS-PREPARATION`：构建non-authorizing future release run-contract template、strict
later-PLAN gate、release-specific terminal/output validator和injected production-shaped three-artifact matrix。Production release
invocation0，future release budget保持0/1；完成后停Planner。

## 4. Suggested Orchestrator reference update

- D1 marked accepted/complete；
- REF-P7-04 current action → D2 offline release harness preparation；
- future release remains locked，budget0/1；
- Human device pause marked lifted，但无active PLAN的具体device/live/formal操作仍未授权。

维护性判断：D1决策边界清晰；D2应复用既有外置gate/accounting模式并新增release三artifact validator，不改production。
