# Planner Review：P7-TD-B-Z0-R4-C1C metadata replay first failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1C` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1c/20260726T060000Z/`

本审查只读离线完成；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与结论

- C1A/C1B replay、event replay、failure-seal replay、hash replay 均在其既定范围内完成；event、seal、hash 状态均 pass，设备/网络/real wrapper 为零。
- C5 entry count=`322`，但 `c5-322-replay.json` 因 helper 只重算 bytes/SHA，未比较 C5 合同要求的 `device/inode/mode/path` 合法 metadata，误报 322 项 metadata schema mismatch；这是 replay helper owner 缺陷，不是旧 C5 root 漂移。
- `c5-322-replay.json` SHA-256 `bbcc25652f51401eadf6749f8fb118336ff39a12c9b7ac82243dc580385106cd`。
- `driver-result.json` SHA-256 `1814b9a9507b29351647e6d62bcf157b9009cb9fb8ccbf388d32c400a322e415`，status=`hard_failure_waiting_for_planner`。
- `terminal-seal.json` SHA-256 `ff053dcc3b57345bd8fa0e8841af4302b256c26917726b0e38d7df077446503f`；`zero-budget.json` SHA-256 `acc06c092fe2ed06d4d415719d626604d0a1613cff80d74fd4abb56ca70b8712`；旧 C1A/C1B/C5 roots 未修改。

## Planner 决策

**拒绝 `P7-TD-B-Z0-R4-C1C`，不进入 real Z0。** 本次未完成 C5 322-entry replay，后续 full R4 gate 不可验收。

冻结 finding：

`REV-Z0-R4-C1C-METADATA-OWNER-020` — C5 replay helper 的 metadata owner 不完整，必须复用/对齐既有完整 ordinary metadata 合同，逐项比较合法 `device/inode/mode/path/bytes/SHA`；不得通过忽略字段或特殊豁免消除 mismatch。

## 精确下一分支

`P7-TD-B-Z0-R4-C1C1_OFFLINE_METADATA_REPLAY_CORRECTION`

下一包只能修复并验证 C5 replay metadata owner；不得运行 event/seal/real wrapper/hostname/设备/网络/E2/formal/retry，C1C root与所有旧 evidence只读。metadata correction 通过后再由 Planner 发布新的完整 C1C gate。

维护性判断：失败局限于 C1C 离线 replay helper 的 metadata schema 对齐，未触及生产路径或科学合同；应复用既有 metadata owner，避免平行字段定义，无需架构重构。
