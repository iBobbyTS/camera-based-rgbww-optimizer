# Planner Review：P7-TD-B-Z0-REAL-R1-C2 source-level event consistency

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-R1-C2` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-r1-c2/20260726T150000Z/`

仅执行离线 source/evidence 核验；未运行 real wrapper、hostname、网络、设备、secret 内容、E2、formal 或 Git。

## 证据与验收

- exact candidate controller SHA-256 `98849221977908e96a3ff042c69a8fce8e306013ceb4a33f543a14ce079c3509`；driver通过importlib直接import该path并调用`r4_event_binding_selfcheck`，不是语义摘要。
- source-level matrix `11/11`：prefix counts exact `6/1/3/5/6/3`，五负例fail closed；producer、fake override、validator consumer同一source owner，item_kind/outcome/runtime/secret serialization exact。
- source-matrix SHA `953682f9e4c0bef4571a86e64487a3d730bbef748b5ad3f1abe2a299322779d7`；validation SHA `28dd5ae2fdafd2251bb0c353d1db3392f6463004bfe483e3457d2c31beddf848`；terminal SHA `aa6901243ac73a35346e893d94f0bca1a4346b313f33e4f3050a9d77f3c0b78f`，mismatch=`[]`。
- package/driver/source-matrix=`1/1/1`；real wrapper/hostname/network/device/production/secret/E2/formal/camera/Ray/nonzero/Git/retry=`0`。

## Planner 决策

**接受 C2，关闭 `REV-Z0-REAL-R1-SOURCE-EVENT-CONSISTENCY-025`。** Candidate source必须在下一real gate中byte-exact冻结；任何source drift重新锁门。

## 精确下一分支

`P7-TD-B-Z0-REAL-R2_BOUNDED_ZERO_ONLY_REACHABILITY`

下一 active PLAN 释放唯一 bounded real R2，必须复制/使用 controller SHA `988492...c3509`，先self-check一次再wrapper一次，五zero stages；无retry/IP fallback/standalone probe，E2/formal、相机/Ray、非零输出继续锁定。

维护性判断：C2 将producer/override/validator收敛到同一candidate source owner；下一步byte-exact消费该source，不新增生产架构。
