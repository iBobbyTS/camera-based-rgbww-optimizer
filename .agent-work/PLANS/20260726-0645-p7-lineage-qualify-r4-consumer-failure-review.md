# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-R4 post-seal consumer failure

**审查日期：** 2026-07-26 06:45

## 证据与决定

- qualification `1/1` exit `0`；57-path candidate `prohibited=[]`；唯一 v2 release：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-qualify-r4/qualify-a87b09f-20260726T060200Z/setup-lineage-release.json`，
  SHA `947b27c481931259ea2ee4eeeb3fb1eafa6d1c4bac169b934ec04d3b08f7ee44`。
- Production/public validator 均通过；release schema、checkpoint、production usability 合法。
- 唯一 fake consumer 因 Executor 合同外断言 `resolved.stage == "formal"` 失败；合法冻结值为
  `stage="TD-B"`，experiment id=`p7_td_b_command_switch_history_v1`。该失败不证明 release
  schema/production validator 缺陷，但按首次 consumer attempt 仍保持 release acceptance=false。
- failure audit SHA `3280561d5baf125fb7583034107ef6fe591e2b6e8e05ec6484d318e719e9bfac`；
  retry/rerun/formal/device/network/Git 均为 `0`。

接受 qualification 与 sealed release 作为 immutable evidence，但暂不接受 release 进入 formal。
发布唯一纯离线 fake-consumer oracle correction；禁止重跑 qualification、修改或重建 release。

