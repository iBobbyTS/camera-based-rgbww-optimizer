# Planner Review：P7-TD-B-Z0-REAL-R1 source-level event self-check failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-R1` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-r1/20260726T140000Z/`

仅执行离线 evidence/source 核验；未运行 real wrapper、解析 hostname、访问网络/设备、读取 secret 内容、执行 E2/formal 或 Git。

## 证据与结论

- 唯一 driver 在 pre-device event-binding self-check hard-fail；self-check=`1`，wrapper/stages/verified/hostname/network/device/production=`0`。
- success 六事件通过，adapter-read/import failure通过；load-failure 实际合法五事件但 validator仍期待六；partial实际三事件仍被判false；downstream fake override未调用secret loader，仅四事件。
- 这证明 REAL-C1 的离线语义摘要未被 real-gate source/consumer一致消费，不能以摘要通过替代将进入真实 gate 的 source-level 验证。
- event self-check SHA-256 `15dc534ca8d3f41c691bef4dab17d4b1141b2cf1796a7b0fea6918783c870121`；pre-device failure SHA `38d8fcc6fec9c64cdf03a9a85571fd5580e6965df02342b1233c5391f21ad583`；terminal SHA `c8976a87d062f5ecf5b387ed11efff8ce4b5194ffb7ad2fb38e2ed5774b8272f`；zero SHA `9337b6b470ed378d3d8e5554d7e906e6c736813fe37a00a925796f62bca7c4b8`。

## Planner 决策

**拒绝 REAL-R1，不得重试或进入 real wrapper/E2/formal。**

冻结 finding：

`REV-Z0-REAL-R1-SOURCE-EVENT-CONSISTENCY-025` — 将进入 real gate 的 controller source 中，event producer、fake override 与 validator consumer 对 prefix/outcome 的定义不一致；必须直接对该 source 做离线调用与回归，不能只消费独立语义摘要。

## 精确下一分支

`P7-TD-B-Z0-REAL-R1-C2_OFFLINE_SOURCE_EVENT_CONSISTENCY`

下一包只能修改/验证将进入 real gate 的 source-level event owner/consumer：load=5 failure、downstream需实际调用fake secret loader并产生6 failure、partial=合法3 prefix；成功与其他case保持。禁止 real wrapper、hostname、网络、设备、retry、E2、formal、相机/Ray、非零输出、Git。

维护性判断：失败集中在 real-gate source 内 producer/consumer 接口一致性；应以同一 source-level owner和direct-call矩阵消除摘要漂移，无需生产架构重构。
