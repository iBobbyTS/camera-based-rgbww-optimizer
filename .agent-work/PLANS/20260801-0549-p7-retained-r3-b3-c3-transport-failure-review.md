# P7 retained-R3 Option B：B3-C3 controller transport failure 验收归档

**审核时间：** `2026-08-01T05:49:49-0600`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-FRESH-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1`

**Activation：** `24ed7947f361908e46f1c8564e9f35fbd1589013`

**Evidence commit：** `b22cdafc8ab0b6e2e5a25b695edf325e7d782a6c`

**Planner decision：**
`REJECTED_CONTROLLER_SOURCE_TRANSPORT_CORRUPTION_NOT_MANIFEST_DEFECT`

## 1. 审核范围与方法

Planner独立只读核对active PLAN、activation/evidence Git topology、exact changed paths、committed
`EXECUTION_RESULT.md` parent/child identity、physical EOF suffix与末尾strict JSON payload。未运行test、CodeGraph或
controller；未读取external real manifest/source、C1、retained R3、lineage-owner evidence或Advisor attachment；未调用
canonical validator、retained audit、release、network、DNS、environment、credentials或device路径。

Activation是`1f121b16502d869ed31d6b6cccc0a79d3dbdd737`的direct child，subject为
`chore(plan): activate fresh postcommit verification`，changed paths exact为FULL、PLAN和本轮route-selection archive。
Evidence commit是activation的direct child，subject为`chore(evidence): record B3-C3 postcommit verification`，changed
path exact仅`.agent-work/EXECUTION_RESULT.md`。Evidence commit后worktree clean，activation→evidence diff check通过。

## 2. ER physical EOF 与执行actual

独立重算结果：

- parent ER bytes `1320095`，SHA-256
  `9917cfd4c8710f704f55a1d5df176de5dcee84327c50bbc822ae27080475ec63`；
- evidence ER bytes `1323360`，SHA-256
  `64c1c937bfa986d3b1738c75c38ae86781188e2929b3f675c84e985c792a9ec2`；
- parent是evidence完整prefix；physical EOF suffix bytes `3265`，SHA-256
  `c57f887e3d6fb1ddda238b688c3ba899a5db1dd22ef8adbd6c28bf47b067a34e`；
- suffix只含唯一heading及一个strict JSON fenced payload，payload位于physical EOF；
- activation machine gate `PASS`，outer controller `1`、self-check `1`、Git reads `7/36`、ER tail read `1`、ER append
  `1`、process scan `1`、retry `0`、fallback `0`、postappend operations `0`、owned residual `[]`；
- focused `0`、full `0`、synthetic run/controller/input/output/replay均`0`，符合first-failure stop；
- repository code/test reads/writes、CodeGraph、real-input writes、retained schema/science validation、canonical
  validator/callback、audit、eligibility、release、network/device/formal/public-analyzer及全部later-stage locks均为`0`。

## 3. Finding 与拒绝理由

唯一first failure发生在`BR-SELF-CHECK`，消息精确为：

```text
'retaine  m3-audit-provenance-manifest-v2.json'
```

冻结manifest文件名应为`retained-r3-audit-provenance-manifest-v2.json`。失败文本中的字面量已在`d-r3`位置被替换为
两个空格，说明controller实际执行的source token没有保持原始bytes。结合本轮使用过的interactive/REPL source transport
history，这是一项controller source transport corruption；它发生在任何manifest事实完成核验之前。没有证据表明sealed
manifest、production helper、dedicated test、canonical validator或retained R3本身存在defect，因此不得把本轮归因于
manifest mismatch，也不得由此修复、重建或重新生成manifest。

本轮未取得success label，不能接受为B3-C3完成。其fail-closed顺序、zero locks、物理EOF handoff和无残留进程可接受；
拒绝的仅是未完成的postcommit verification execution。失败root与本次controller transport不得retry、复用或在原位置修补。

## 4. Exact successor

唯一后继为`REF-P7-25-R2-B3-C3-C1`：创建全新activation-derived namespace，通过一次性、非交互式、non-TTY
外置source file承载controller。Source file必须以`apply_patch`一次创建在`/Volumes/4T/temp/rgbww-optimizer`下的fresh
0700 package root，文件0600；controller进入任何stage前做strict UTF-8、NUL/CR absence、bytes/SHA记录，并禁止source内硬编码任何real
manifest artifact basename。所有artifact basename只能从committed PLAN machine row strict解析取得。Controller只允许以
`.venv/bin/python <absolute-controller-file>`一次non-TTY argv调用，禁止Terminal paste、REPL、IPython、`python -`、
`python -c`、heredoc、shell-eval或stdin source execution。

后继必须从fresh absence gate重新开始，顺序仍为self-check→focused exact1→durable full exact1→brand-new synthetic
exact1→physical EOF handoff；不得retry、reuse失败root、读取old B3 evidence或跨过失败阶段。任何失败立即冻结actual并停止。
Canonical validator、real retained audit、eligibility、release、network/device及later stages继续locked。

## 5. 状态与维护性

`RETAINED_UNVALIDATED_UNCONSUMED`保持不变；canonical lineage validator仍是唯一eligibility owner；B4尚未解锁。本纠偏
属于纯离线execution transport治理，不需要Advisor科学决策或Human设备授权。

维护性判断：后继不新增production owner；它仅把一次性controller从易损的interactive transport迁移到可哈希、non-TTY、
生命周期明确的外置source file，并继续复用既有manifest/domain/runtime/test owner。
