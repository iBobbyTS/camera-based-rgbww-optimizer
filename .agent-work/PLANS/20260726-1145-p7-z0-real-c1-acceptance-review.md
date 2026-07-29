# Planner Review：P7-TD-B-Z0-REAL-C1 offline event/seal correction

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-C1` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-c1/20260726T110000Z/`

仅执行离线证据/hash 核验；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与验收

- Event matrix 六 case + 五 negatives 全部通过：success 六事件；adapter-read-failure prefix 1；import-failure prefix 3；load-failure prefix 5 + failure；downstream-failure prefix 6 + failure；partial-persistence 合法 prefix；runtime owner exact，`secret_serialized=false`。
- Failure-seal matrix `7/7`：各 failure/duplicate/tamper/symlink/nonregular case SHA unchanged，`FileExistsError=false`。
- fresh root strict JSON `32`；terminal/post/validation/zero hash 从最终磁盘重算，mismatch/drift/residual 全部闭合。
- validation SHA-256 `9ce2b4b74dd4f2ca752042354881e77aaae01297cd5d0ed376b83ad95f64eca3`；event SHA `d8a0a858cccc268c6729da574d7c3bff4e1a9f13a40089a3982574f7772df1c4`；seal SHA `d2174520129869b2c27a222fc09bb498dbc9abbd386abc568d960451f72b996a`；terminal SHA `05fd0750dc5eae7e9cef8bc96ba825579856cd447784e514a9095b96acaf9144`。
- package/driver/event/seal=`1/1/1/1`；real wrapper/hostname/network/device/production/secret/camera/Ray/nonzero/E2/formal/Git/retry/rerun=`0`；残留进程=`0`。

## Planner 决策

**接受 REAL-C1，关闭 `REV-Z0-REAL-EVENT-OWNER-022` 与 `REV-Z0-REAL-FAILURE-SEAL-023`。** 这只证明 real-gate 的离线 self-check contract，不是实际设备可达性证据。

## 精确下一分支

`P7-TD-B-Z0-REAL-R1_BOUNDED_ZERO_ONLY_REACHABILITY`

下一 active PLAN 重新释放唯一 bounded real Z0：self-check 一次、wrapper 一次、五个 zero-only stages、exact hostname/identity/generation/all-zero；无 retry/IP fallback/standalone probe，失败后 cleanup 并停；E2/formal、相机/Ray、非零输出继续锁定。

维护性判断：REAL-C1 仅修复离线 event/seal owners，未增加生产路径；下一步为既有 bounded real gate 的重放，无需架构重构。
