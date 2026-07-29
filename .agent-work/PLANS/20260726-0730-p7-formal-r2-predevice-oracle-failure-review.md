# Planner 验收归档：REF-P7-04 FORMAL-R2 pre-device oracle failure

**审查日期：** 2026-07-26 07:30

## 证据与决定

- pre-device gate 在设备、Terminal、formal package 和 run-root ownership 之前 hard-stop。
- 首失败是外置 oracle 错写为 `normalized_per_second.trimmed_mean`；production/PLAN exact
  常量为 `statistics.normalized_per_second.trimmed_mean`，无 production drift。
- HEAD、release/public validator、resolved plan、Ray 16 formal/0 ambient schedule、caps/shutter
  ledger 已通过；后续 consumer/manifests/E2/strip/runtime deep replay 未完成，不能报 pre-device pass。
- Ray/strip/paired roots 均不存在；formal package attempts=`0`，retry=`0`，设备/network/formal/Git=`0`。
- failure audit SHA `493c239e7a4fe3068249f9a0c5898e85d8e0a94a7146435639e55386805f240a`。

接受 fail-closed 结果。发布唯一最小 pre-device oracle correction；只允许修正 exact statistic
oracle 并完成剩余离线深重放，禁止启动 Terminal、设备或 formal。通过后由 Planner 另发 FORMAL PLAN。

