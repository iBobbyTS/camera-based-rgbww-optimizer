# Planner release-provenance 验收：REF-P7-04 sealed lineage release

**审查日期：** 2026-07-26 07:00

## 证据与决定

- corrected fake consumer `1/1 pass`，documented oracle 为 stage=`TD-B`、exact experiment/
  source/schema/checkpoint/status/usability；independent audit `1/1 pass`，所有 mismatch arrays 为空。
- validation SHA `39c2f5ec5cc824eed58990a5dd001d7ba5b60834cee164a016aa82961b9e034f`；
  audit SHA `cb9e4283d36bb7b6614ca360c26ac8caf22b4e617805291a0af0e5577b2598f9`。
- sealed release SHA `947b27c481931259ea2ee4eeeb3fb1eafa6d1c4bac169b934ec04d3b08f7ee44`、
  resolved plan SHA `7948e61a0d336c56584c53b16b7d964eaf33a62555dedc182008f5142eb8836f`、
  首失败 audit SHA `3280561d5baf125fb7583034107ef6fe591e2b6e8e05ec6484d318e719e9bfac`
  前后不变。
- qualification/replay/candidate/release write/device/network/formal/Git 均为 `0`。

接受 sealed v2 release 的 provenance，允许 production formal runner 在 exact clean checkpoint
消费它。此 release acceptance 只证明 provenance/consumer usability，本身不授权 formal、设备
访问或灯光输出；formal 授权仅来自下面另行发布的 active PLAN 及其 exact bounds。

