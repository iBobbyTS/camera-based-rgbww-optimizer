# P7-TD-B Z0-R2-C1R4 terminal-seal owner identity 验收归档

**归档时间：** 2026-07-25 16:47 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R4

**Reviewed PLAN SHA-256：** 6d3e1d7da522d56967cc9c7f28583eecec5d89cdcf7ac3d01c37897c0a356d5e

**Planner decision：** `accepted_cases_bootstrap; rejected_conflicting_whole_seal_ast_contract; c1r5_normalized_owner_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R5；保持 terminal-seal logic slice exact，只对冻结列出的 bookkeeping literal位置做精确 normalization，不保留错误旧contract labels且不泛化 parser/AST放宽。

## Reviewed scope 与执行方法

C1R4 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r4-offline/20260725T224236Z/`

Executor exact冻结 C1R3 artifacts，生成C1R4 source，完成compile/syntax与唯一授权的cases parent bootstrap。driver-start source/AST gate发现 `seal_r2` whole-function AST不一致后立即停止；driver、matrix与seal均未运行。

## Evidence 与 accepted validation

- `cases-bootstrap.json`：bytes `1004`，SHA-256 `f169f0510d21b0d5d8975b80ba3ac1e51c12e3bafe0e02b6c7c1b7bdda27db02`。
- `pre-driver-failure.json`：bytes `2479`，SHA-256 `b0f7ba7e59405b2a87e40f293e5e3a2b0aaa4cb55fd1619101f8d36256bbbb5a`。
- `validation-summary.json`：bytes `504`，SHA-256 `7d96f07fa87924f12713a17fff14d9e4c14f6922e5ed04be9ac7234d38233bff`。
- C1R4 `source/harness.py`：bytes `82103`，SHA-256 `0244b0d61ff85441d24a171ea5be1cf235133ccaed17e39cf497a21d2589904f`。
- canonical wrapper、real adapter与launcher均与C1R3 byte-exact；lifecycle AST SHA-256 `768a79fe9c09b9fb885463a2a44db061590bbb13a40b09a7defb6156dc87a1b2` exact。

cases bootstrap全部接受：before missing；single `os.mkdir` requested `0755`；无parents/exist-ok/recursive/fallback；after为empty、directory、non-symlink、mode `0755`；driver-start precheck identity相同；created count `1`。

## Finding、decision 与 residual risk

C1R3 `seal_r2` AST SHA为 `9173fdd3a96c84ca3c70f3ca891555aca61030f1cd5bb4bf0b314d3175ab01da`，C1R4 raw AST SHA为 `228b9142e1c1c220844ef4a856c1c067a6f5abb70a4b7b87291fbf3c639a9919`。差异只来自PLAN另行允许且必须更新的bookkeeping：terminal schema、old-root replay list、validation contract/schema与cases-parent budget。它们位于函数体内，故“更新bookkeeping”与“whole-function AST exact”不能同时成立。

Planner选择保持正确C1R4/C1R5 labels，不回退C1R3 labels；下一包以精确 AST location/type/value allowlist审计raw delta，并仅对这些节点做sentinel normalization。normalized AST/logic slice必须exact；其他constant、call、branch、operator、key、counter、seal顺序或failure behavior任何变化均拒绝。

package JSON `3/3` strict；driver/matrix/seal、old-root driver/launcher、secrets/.env/credential、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、Git均为0。production/scientific owner与workspace保持。
