# Planner Review：P7-TD-B-Z0-R4-C1B offline binding/seal/evidence correction

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1B` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1b/20260726T050000Z/`

仅执行离线证据与磁盘哈希核验；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与验收

- C1A parser replay、C1B exact contract/reference/package/HEAD/archive owner 全部通过，C1A accepted hashes 无 mismatch。
- Event progressive matrix 六 case 全通过：success `6`、adapter-read-failure `1`、import-failure `3`、load-failure `5`、downstream-failure `6`、partial-persistence `3`；duplicate/out-of-order/tamper/symlink/runtime-mismatch 五负例均 fail closed，事件无 secret serialization、runtime owner exact。
- Failure-seal matrix `7/7`：self-check/post-check failure、already-sealed、tamper、symlink、nonregular、duplicate-finalizer 均首写后复用，SHA 不变，`FileExistsError=false`。
- Evidence-hash matrix `5/5`：valid/stale/tamper/missing/symlink 均按磁盘重算并正确 fail closed。
- 实际 fresh root 共 35 个 JSON，全部 strict parse；terminal canonical entries ordinary/non-symlink，mismatch=`[]`。
- validation-summary SHA-256 `57f8a4fd20cca2e850b921f69dff7ed854a682a4b13e39d96626bde701a6afd9`；terminal-seal SHA-256 `628a0d0ef665e6ffd8918dc343c656263ad4ad9c01c44400c5b1cac8e1ccfe54`；driver-result SHA-256 `794f755a95bb8a250e8fd9c33f3a0e51c80af15fa762240e1834acfecfaf0ca7`。
- package/driver/C1A self-check/event/seal/hash matrix=`1/1/1/1/1/1`；rerun/retry/real wrapper/hostname/network/device/.env/E2/formal/Git=`0`；无残留进程，旧 root 无漂移。

## Planner 决策

**接受 C1B，关闭 `REV-Z0-R4-EVENT-BINDING-016`、`REV-Z0-R4-FAILURE-SEAL-017`、`REV-Z0-R4-EVIDENCE-HASH-018`。** C1B 只证明离线 binding/seal/evidence contracts，尚未证明真实设备可达性或 zero stage 成功。

## 精确下一分支

`P7-TD-B-Z0-R4-C1C_OFFLINE_FULL_R4_ACCEPTANCE_GATE`

下一 active PLAN 必须回到 R4 完整离线验收：消费 C1A/C1B accepted evidence，重放 C5 322-entry seal/source/runtime，执行完整 R4 parser、actual-worker binding、failure/terminal/post audit 与 zero-budget self-check；仍不得运行 real wrapper、hostname、设备、网络、E2 或 formal。只有 C1C 全绿后，Planner 才能另行发布唯一 bounded real Z0 前置门。

维护性判断：C1B 完成三项离线 owner 纠偏，未触及生产 owner、设备控制或科学合同；下一步是既有 R4 合同的完整回归，不需要架构重构。
