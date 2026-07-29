# Planner 重新验收：FORMAL-LAUNCHER-C1 / FORMAL-R4 secret contradiction

**审查日期：** 2026-07-26 07:45

## 撤销与冻结事实

- 撤销此前对 C1 cleanup-secret availability 的接受，并拒绝 FORMAL-R4。此前归档保留为
  superseded history，不得再作为 `present/parseable=true` 证据。
- C1/R4 redacted artifact SHA 均为
  `b75762e39f223729331c5a7b75cee7e5dfbb02e661caf08d98467a4933f9d3be`，磁盘实际为
  `present=false`、`parseable=false`。C1 summary SHA `2617b925...d8b0e` 的 true 声明错误。
- Executor prelaunch driver 未消费 nonzero exit code，把空 stdout 当成功并错误越过 no-launch gate。
- R4 唯一 Terminal：window `259082`、TTY `/dev/ttys007`、PID `63847`；candidate 正确在
  pre-import secret gate exit `78`。PID dead，log/state/Ray/strip/paired/capture absent，device/network=`0`。
- Post-failure zero owner attempt=`1`，同样 secret gate exit `78`；actual all_off=`0`，fresh zero unknown；
  retry/automation/residual=`0`。Failure audit SHA
  `0d78504dc682072055777569f70d8b37e971825428ff801ff7de858cb1b11985`。

Candidate 的 bytes/mode/fail-closed behavior 仍可保留；secret availability 与 formal authorization
全部撤销。下一包只修正离线/visible-child evidence accounting，不运行 formal 或设备。

