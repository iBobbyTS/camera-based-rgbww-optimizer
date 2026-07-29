# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-R1 CLI 首失败

**审查日期：** 2026-07-26 20:30

**审查范围：** 第 84 节离线 lineage qualification 首次运行。

## 证据与决定

- CLI 在 argparse 阶段以 exit code `2` 失败：错误 `experiment-id=td-b`，exact 允许值为
  `p7_td_b_command_switch_history_v1`。
- 未执行 legacy replay、candidate validation、release generation；未创建 output/release artifact。
- device/network/hostname/.env/setup/formal/public analyzer/camera/Ray/strip/capture/CR3/NPY/retry/IP fallback/Git 均为 `0`。
- 按首失败规则接受 hard-stop；不得修改历史 `fa6c95d` 文件或重试原包。

GUIDE 与代码中的 experiment-id 定义一致，问题是局部命令参数绑定，不需要 Advisor 决策。
发布唯一最小离线纠偏包：只修正 CLI 参数为 exact
`p7_td_b_command_switch_history_v1`，其他输入、phase、checkpoint、run root 和禁止项全部冻结。
纠偏包通过后仍须回到 lineage replay/candidate/release 的独立 Planner 验收门，不解锁设备或 formal。

