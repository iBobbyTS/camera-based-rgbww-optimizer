# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-CLI-C1

**审查日期：** 2026-07-26 20:45

## 证据

- CLI-C1 仅执行一次离线 argparse parse gate 并通过。
- exact experiment-id 为 `p7_td_b_command_switch_history_v1`；source、legacy release、
  checkpoint、phase、output-dir、run-name 均与原包一致。
- parse status `pass`，phase `formal`，mode `qualify_lineage_release`；replay/candidate/
  qualification/release flags 均为 `false`。
- strict JSON `2/2`；parse-result SHA `7351b7b7affc52f31290500976498d19b9ad7e5aea43e5ead4b14f39b5f8212a`；
  validation SHA `85507b32e651a6132a4cabc267712e146ccb61e8d88b39f1ee6209139f844372`。
- setup/replay/candidate/release/device/network/hostname/.env-content/camera/Ray/strip/formal/
  public analyzer/capture/CR3/NPY/retry/IP fallback/Git 全为 `0`。

## 决定

接受 CLI-C1，关闭纠偏分支，恢复原 `P7-TD-B-LINEAGE-QUALIFY-R1` 完整离线 qualification
包。该包仍只允许 immutable legacy replay、candidate/qualification provenance；parse 通过
不等于 release 验收，不进入设备或 formal。

