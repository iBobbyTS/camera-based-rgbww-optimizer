# Planner 验收归档：REF-P7-04 FORMAL-R3 visible-Terminal pre-exec failure

**审查日期：** 2026-07-26 08:30

## 证据与决定

- 唯一 visible Terminal launch：window `258939`、TTY `/dev/ttys007`、shell PID `42206`。
  External wrapper SHA `a1a87564...cff5`，mode `0644`；shell `exec` 以 permission denied 失败。
- 三次 liveness 均为 dead，owned processes=`[]`；continuous log/state、Ray/strip/paired roots、
  capture/ledger/analyzer 均不存在。Formal wrapper/device/capture/analyzer attempts=`0`，automation=`0`。
- 唯一实际 `all_off` exit `1`：运行环境缺 `AMARAN_OPENAPI_SECRET`，Ray adapter 未构建；
  strip outcome 未序列化，fresh post-failure 双零未知。最后完整证明仍是 accepted prelaunch zero。
- failure audit SHA `389dfada76f684c587d121aa342733f62c53d4eac2c231c8f486be0cc567bb10`；
  未重试、未修改 mode 后重发。

接受 pre-exec fail-closed 事实，拒绝 formal/cleanup 验收。发布最小纯离线 executable-mode 与
cleanup-secret availability correction；不得启动 Terminal、formal 或设备。

