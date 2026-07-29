# Planner Review：P7-TD-B-Z0-REAL pre-device self-check hard failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real/20260726T100000Z/`

仅执行离线 evidence 核验；未解析 hostname、连接网络/设备、运行 wrapper、读取 secret 内容、执行 E2/formal 或 Git。

## 证据与结论

- 唯一 driver 在 pre-device self-check hard-fail；self-check=`1`，wrapper/real attempts/hostname/network/device/production=`0`。
- wrapper-binding self-check pass，但 event-binding fail：success 只有 4 个事件；load-failure 被错误标记为 success 且无 load 事件；downstream-failure/partial-persistence 的 prefix/result 与期望不一致。
- `event-binding-selfcheck.json` SHA-256 `0f0317d5bd1395b33d8144f2abfa04ada1e3e5844fc6508a4ab6e497d54e464b`。
- failure path 再次写入已存在的 `zero-budget-audit.json`/`terminal-seal.json`，driver 尾部触发 `FileExistsError`；`driver-failure.json` SHA-256 `18aa89b6c5a9b2c0d095b12262b22b27a74d7f8ef38dc2134410e7d6710ece55`。
- `pre-device-failure.json` SHA-256 `b0a140e7a53d2b984b70c65e2420ac2bb96f1359ef5019d956b14993d90db850`；旧 C1C2/离线 roots 未修改。

## Planner 决策

**拒绝 `P7-TD-B-Z0-REAL`，不得进入 real wrapper、E2 或 formal。** 本次没有真实可达性证据。

冻结 findings：

1. `REV-Z0-REAL-EVENT-OWNER-022` — real-gate fake event self-check 未消费 C1B/C1C2 accepted prefix/result owner；success/load/downstream/partial cases 的 event count、outcome 与合法 prefix 不一致。
2. `REV-Z0-REAL-FAILURE-SEAL-023` — pre-device failure 分支与 driver-finalizer 重复创建 zero-budget/terminal artifacts，触发 `FileExistsError`；必须幂等复用并校验既有 seal。

## 精确下一分支

`P7-TD-B-Z0-REAL-C1_OFFLINE_EVENT_SEAL_CORRECTION`

下一包只能是纯离线纠偏：修复 real-gate self-check 对 accepted event prefix/result owner 的绑定，并修复 failure-seal single-owner/idempotent orchestration；不得运行 real wrapper、hostname、网络、设备、retry、E2、formal、相机/Ray、非零输出或 Git。

维护性判断：失败集中在 real-gate 复用的 fake event self-check 与 failure seal 控制流，未触及生产 owner、设备路径或科学合同；最小离线矩阵与幂等 seal 回归即可，无需架构重构。
