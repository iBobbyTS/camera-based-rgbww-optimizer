# Planner Review：P7-TD-B-Z0-R4-C1A contract parser 离线纠偏

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1A` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1a/20260726T041500Z/`

仅执行离线证据重放与哈希核验；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与验收

- exact-valid C1A contract、reference、package kind、expected HEAD、PLAN bytes/SHA、rejection archive bytes/SHA 全部 exact 通过。
- parser matrix `10/10`：exact-valid 接受；old R4、unknown、prefix-similar、wrong package、wrong HEAD、wrong archive/hash、missing、duplicate、non-string 全部 fail closed。
- `contract-selfcheck.json` SHA-256 `57d62c66539c3085bf18c4a284192eca07d8a780301e1d171f5e8c68223925f2`。
- `validation-summary.json` SHA-256 `5fd62b5ab01f4f66c021b72a34055792124fd60d5d67aaef25d867ac50ccdc92`，status=`offline_pass_waiting_for_planner`。
- `terminal-seal.json` SHA-256 `8a318f13c5e380e8c21716f54c42273e0ed73c6eaf63c65f15664aff53cc7fa3`；13 JSON strict parse，canonical entries ordinary/non-symlink，mismatch=`[]`。
- package build/driver=`1/1`，rerun/retry=`0/0`；event/seal/wrapper/hostname/network/device/secret/E2/formal/Git 全为 `0`，无残留进程；C1/R4 旧 root 未漂移。

## Planner 决策

**接受 C1A，关闭 `REV-Z0-R4-C1-CONTRACT-PARSER-019`。** C1A 只证明 exact contract parser/self-check，未证明 binding、failure seal 或 evidence-hash 三项原始纠偏。

## 精确下一分支

`P7-TD-B-Z0-R4-C1B_OFFLINE_BINDING_FAILURE_SEAL_EVIDENCE_CORRECTION`

下一 active PLAN 必须是新的纯离线 C1B：复用 C1A accepted parser/source/runtime，修复并验证 `EXPECTED_SECRETS` 单一 owner、progressive event-binding matrix、failure-seal 幂等性和最终磁盘 hash 原子 handoff。仍禁止 hostname、网络、设备、real wrapper、E2、formal、retry、lineage release 和 Git。

维护性判断：C1A 仅增加精确 contract owner 与负例矩阵，未引入生产路径；下一 C1B 仍可保持 binding/seal/evidence 单一离线 owner，无需架构重构。
