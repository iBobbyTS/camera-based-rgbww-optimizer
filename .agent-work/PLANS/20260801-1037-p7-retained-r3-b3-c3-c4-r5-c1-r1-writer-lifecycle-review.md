# P7 retained-R3 Option B：R5-C1-R1 writer lifecycle 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-C1-R1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-R1-SYNTHETIC-WRITER-FAILURE-LIFECYCLE-V1`

**Planner 决定：** `ACCEPTED_COMPLETE_JSON_NATIVE_AND_P3_WRITER_FAILURE_LIFECYCLE`

## 1. Topology与physical evidence

- activation `9ef39998a31940ef153da11898407766b460f122`是`bf5b237f4d45c3dac4bebe5626e59ef39f6a39c1`direct child，subject `chore(plan): test writer failure lifecycle`。
- evidence `bf5e971765f1533e3ac3e991386d60e4b2f97a1f`是activation direct child，subject `chore(evidence): record writer failure lifecycle`，changed path exact ER。
- parent ER bytes/SHA-256 `1414382` / `f67a2fda8dd94a974dbf34f70ed94d0f5ecae23767cbf0e345c23c2608ba7d85`；child `1417401` / `85b49f87bf7c58514e7056f0fb1a5b0465a7053b0345d89b37a5fdf597c916a8`；unique EOF suffix bytes/SHA `3019` / `e82b169e57cbcafe817272a64c94ea87c162260b1bb1b86c2faf6dffeda07bac`。
- source mode `0600`，device/inode `16777240/2273287`，bytes `3382`，SHA-256 `4b54cc680b7edf495c855c3edec2dd096969cc632390c3f1de94d54165030573`，pre/post exact。
- golden root mode `0700`，inode `2273289`，exact4 canonical 0600 artifacts：contract `151/b3d688bc0fab8a6fd82e08f1547b053b1687cf0802ee2093aa564f738031ab9f`，seal `128/fab3fb497f0943dfccb7bb2c87fb9552c6d2389d11e9815677d5e7e1b590859d`，terminal `169/137f75b1ab4708b314273e24db98ff2ee5b610f23c1dbb9fedf8b511fb970043`，seal `126/be0ce7a6b0293b4f71468d27281fe0755f0e17a9a535482647707f47bf8f5274`。
- writer-failure root mode `0700`，inode `2273294`，exact2 canonical 0600 artifacts：terminal `252/eb52baa37170672610224ce4027246c4ea9fefdc8a57a381662a4a4266621969`，seal `126/d0a4de0d55791ef9036f3e8839e83e22f85bba35af770466a9535efd8bacccd4`；contract target与seal均absent。
- canonical reload `6`、seal checks `3`全部独立通过；ER handoff unique physical EOF。

## 2. Lifecycle finding closure

- local JSON-native adapter保持C1已验证语义：Mapping→plain dict、tuple/list→plain list、concrete scalar allowlist，无fallback。
- writer-failure fixture可成功native conversion。
- 同一broad primary `try`内实际顺序存在conversion、P3 contract persist和contract seal语句。
- contract persist使用exact `dependencies={"open_fd":deny_contract_open}`；injected callable调用exact1并在target创建前抛OSError，P3转换为`ProvenanceIOError/target_open_failed`。
- primary被broad catch捕获；contract writer invocations1、contract writes0；contract target/seal absent。
- failure terminal使用default uninjected P3 writer，exact terminal+seal成功，status `synthetic_writer_failure_sealed`，reported type/code/counters exact。
- golden case同时证明正常writer链路仍成功。旧roots/真实inputs、Git、owner、validator、release、network/device均0；retry/fallback0。

## 3. Planner决定与下一分支

接受C1-R1完成；C1 adapter语义与writer failure lifecycle合并视为可消费的一次性controller contract。此前R5 source/empty root及全部C1 synthetic roots只保留为evidence，永远不得复用。

下一唯一分支`REF-P7-25-R2-B3-C3-C4-R5-R1`：一次fresh pure-offline real manifest self-check successor。它必须：

- 新建source/root，继承accepted JSON-native adapter和primary lifecycle；contract conversion/persist/seal全部在broad catch内，失败用default uninjected terminal writer封存。
- 验证R4 preparation；P3 no-follow读取manifest5、C1四、retained三。
- exact 8 Git bytes acquisition；required argv check一次；self-check owner一次、18 ordered ledgers。
- 成功sealed contract/report/terminal；失败sealed contract（若已写）与terminal；retry/fallback0。

canonical validator、eligibility emission、release consumption、network/device/camera/Ray/strip/formal/public analyzer继续为0。R5-R1成功也只产生subordinate evidence，等待Planner验收。

维护性判断：C1-R1以P3既有dependency injection完成真实writer error-path覆盖，没有修改production代码或新增抽象；可安全回到fresh real successor。
