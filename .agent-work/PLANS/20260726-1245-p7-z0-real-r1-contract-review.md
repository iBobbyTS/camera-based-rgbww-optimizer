# Planner Review：P7-TD-B-Z0-REAL-R1 contract parser first failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-R1` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-r1/20260726T120000Z/`

仅执行离线核验；未运行 self-check、real wrapper、hostname、网络、设备、secret content、E2、formal 或 Git。

## 证据与结论

- compile-only 与 wrapper syntax 通过；driver 启动一次，在 freeze contract parser 立即 hard-fail。
- source 仍绑定旧 `P7-TD-B-Z0-REAL`，拒绝 active `P7-TD-B-Z0-REAL-R1`，错误 `ValueError: R4 contract differs`。
- `real-driver-ledger.json` SHA-256 `201d0f3b7faa71c50e9752deef33d8cc44b8ee4130fbf67317c767200b49e086`；wrapper/stages/verified/hostname/network/device/secret/nonzero/camera/Ray/E2/formal/Git/retry/rerun 均为 `0`。
- 旧 REAL/REAL-C1 roots 与 PLAN/FULL 未修改。

## Planner 决策

**拒绝 `P7-TD-B-Z0-REAL-R1`。** 本次没有产生 self-check 或真实可达性证据。

冻结 finding：

`REV-Z0-REAL-R1-CONTRACT-PARSER-024` — 阶段 contract parser/archive owner 未随 active R1 PLAN 更新，必须 exact 接受 R1 contract 并拒绝旧/未知/前缀相似/错 archive/hash contract。

## 精确下一分支

`P7-TD-B-Z0-REAL-R1-C1_OFFLINE_CONTRACT_PARSER_CORRECTION`

下一包只能是纯离线 parser/archive owner 修复与负例矩阵；不得运行 real self-check/wrapper、hostname、网络、设备、retry、E2、formal、相机/Ray、非零输出或 Git。

维护性判断：失败仅限阶段 contract owner 接线，未触及生产设备路径或科学合同；最小 exact parser 回归即可，无需架构重构。
