# Planner Review：P7-TD-B-Z0-R4-C1C1A typed path correction

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1C1A` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1c1a/20260726T080000Z/`

仅执行离线 evidence/hash 核验；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与验收

- C5 positive metadata replay `322/322`，完整 `bytes/device/inode/mode/path/sha256` 比较，mismatch=`[]`。
- metadata negative matrix `12/12`：missing、wrong device/inode/mode/path/bytes/SHA、symlink、FIFO、socket、directory、path traversal 全部 fail closed，并写入 immutable ordinary JSON。
- typed path matrix `20/20`：allowlist、空值、`..`、分隔符、absolute、duplicate/preexisting、symlink-parent、FIFO-parent 全部正确拒绝，无 `TypeError`、路径逃逸或覆盖。
- fresh root JSON `20/20` strict parse；validation/terminal/post/zero handoff hash 均从最终磁盘 bytes 重算，mismatch/drift=`[]`，residual=`0`。
- validation SHA-256 `f44aeeeaf74d9bcf45a7f99bdb43577ae8d69f1394688c388550458c38d82fed`；terminal SHA-256 `ba717ae82cb173553c0b600f90a592d8adaf4a21237a62b37241275805be3f3c`；driver SHA-256 `be908d40d9e165b4b5a332066b22c4851bc9a3705f0568325513f82d55e74021`。
- package/driver/positive/metadata-negative/path-negative=`1/1/322/1/1`；event/seal/real-wrapper/hostname/network/device/.env/E2/formal/Git/retry/rerun=`0`；旧 C1C1/C1C/C1B/C5 roots 无漂移。

## Planner 决策

**接受 C1C1A，关闭 `REV-Z0-R4-C1C1-PATH-CONSTRUCTION-021`。** C1C1A 完成 C5 metadata owner 与 negative path writer 纠偏，但完整 R4 C1C gate 尚未重新执行。

## 精确下一分支

`P7-TD-B-Z0-R4-C1C2_OFFLINE_FULL_R4_REPLAY_GATE`

下一 active PLAN 必须重新执行完整 C1C offline gate：消费 C1A/C1B/C1C1A accepted evidence，重放 C5 322 metadata、完整 parser/event/seal/hash/terminal/post/zero audit；继续禁止 real wrapper、hostname、设备、网络、E2、formal、retry、Git。只有 C1C2 全绿后才能讨论 bounded real Z0 前置门。

维护性判断：C1C1A 仅修正 typed path helper，未增加生产抽象；下一步是既有完整 R4 gate 的重放，无需架构重构。
