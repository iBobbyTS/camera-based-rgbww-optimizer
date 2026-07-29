# Planner Review：P7-TD-B-Z0-R4-C1 contract parser first failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1` 与唯一 fresh corrective root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1/20260726T034500Z/`

本审查只读、离线完成；未访问设备、hostname、网络、`.env` 内容、real wrapper、E2、formal 或 Git。

## 证据与结论

- driver runs=`1`，retry/rerun=`0`；仅生成 `c1-driver-ledger.json`，SHA-256 `36ea15fa5120d7cf6877025311321f8552cd444052af58d4e07093bb7a78a564`。
- compile-only 与 wrapper syntax 在 driver 前通过；source copies 未进入后续 freeze/self-check。
- 首失败为 `ValueError: R4 contract differs`：C1 active contract `P7-TD-B-Z0-R4-C1` 未被仍只接受 `P7-TD-B-Z0-R4` 的旧 parser 接受。
- self-check、event matrix、wrapper、seal、设备/网络/hostname/secret/production/E2/formal/Git 均为 `0`；旧 R4 root 未修改。

## Planner 决策

**拒绝 `P7-TD-B-Z0-R4-C1`。** 本次没有验证其三项纠偏（binding、failure seal、evidence hash），也没有产生 real Z0 证据。

冻结新 finding：

`REV-Z0-R4-C1-CONTRACT-PARSER-019` — C1 corrective contract/archive owner 未接入 parser，导致在 freeze 前首失败。必须让 parser、自描述 contract、rejection archive 和 active PLAN 使用同一明确 owner；不允许放宽为任意 R4 前缀或跳过 contract identity 验证。

## 精确下一分支

`P7-TD-B-Z0-R4-C1A_OFFLINE_CONTRACT_PARSER_CORRECTION`

下一包只能修改/验证离线 contract parser 与 contract self-check：接受 exact C1 contract ID、package kind、reference ID、expected HEAD，并拒绝旧/未知/前缀相似/错 archive/hash 的 contract。不得运行 event matrix、failure seal matrix、real wrapper、hostname、设备、网络、E2、formal 或 retry；C1 原 corrective root 与 R4 root 均只读。

维护性判断：失败局限于 corrective harness 的 contract owner 接线，未触及生产 owner、设备控制或科学合同；最小 parser/self-check 回归即可修复，无需架构重构。
