# P7-TD-B Z0-R2-C1R2 PLAN marker 首门失败验收归档

**归档时间：** 2026-07-25 16:30 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R2

**Reviewed PLAN SHA-256：** 890dc1496c8878960c6b2b9291fd69aa9520502e1ed625da93262df7a8f6ec74

**Planner decision：** `accepted_c1r2_authorized_repairs; rejected_completion_due_planner_marker_format; c1r3_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R3；Planner恢复四个 human marker value 的 backticks，Executor不得放宽 frozen parser，并从全新离线 root 重放唯一 package。

## Reviewed scope 与方法

唯一 C1R2 root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r2-offline/20260725T222554Z/`

Executor从 C1R1 frozen source生成三份新 source，仅实施授权的 secrets identity owner与launcher变量纠偏；完成 source delta、compile/syntax、live secrets gate与launcher exit propagation后，启动 driver一次。driver在任何 matrix 前由 frozen PLAN identity parser fail closed，未重跑。

## Evidence 与 validation quality

- `pre-device-failure.json`：bytes `2290`，SHA-256 `3910683745d1994733f1f3e8e2c4190de92d119ff057f0b2793b24f9075b1f10`。
- `validation-summary.json`：bytes `599`，SHA-256 `f40a920f2ab0fc23e4b1ec59d15692eead0e879eafe3a0d3ce4170627421617f`。
- `source/harness.py`：bytes `80980`，SHA-256 `4ca936042b94bc7abc2966d8f6c1298ebf6e390167782fba43a593d3d6ab0341`。
- `source/run_wrapper.zsh`：bytes `1671`，SHA-256 `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`。
- `source/real_adapter.py`：bytes `4240`，SHA-256 `c2bc28683a1e789f1945164471f6693f48c79dd3c6dcdb1b7e36d1f0e37fc186`。
- `launcher.zsh`：bytes `289`，SHA-256 `75c589929e08e00043591b683c128e86d30cc60f566caec4a2d5ec5472068dbc`。
- package现有 `11/11` JSON strict parse通过；HEAD/index与old-root manifests冻结。

已验证接受：live secrets exact path、regular non-symlink、mode `0644`、size `296`，空 Git index entry被允许，既有 manifest identity只作constant；contents open/read/hash/copy=`0/0/0/0`。launcher仅赋值普通 `driver_rc`，注入 exit `37` exact传播，实际 driver exit `1` exact传播；readonly/special assignments为0。

## Finding、decision 与 residual risk

driver first failure：`ValueError: human-readable marker count differs: contract_id`。frozen parser要求 Reference task ID、PLAN contract ID、Package kind、Expected HEAD四个 human marker value均由 Markdown backticks包围；reviewed PLAN没有 backticks，但 machine contract存在且唯一。该差异由 Planner-owned PLAN引入，Executor正确地未编辑 PLAN、未放宽 parser。

所有科学/production/external owners保持；matrix runs=`0`、terminal seal未启动，两个既有 review finding仍未关闭。C1R3只恢复 Planner marker格式并机械同步新contract evidence bookkeeping，不改变已验证 C1R2 secrets、launcher、wrapper、adapter或parser语义。

secrets/.env/credentials、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、Git操作均为0；repository与无关工作保持。
