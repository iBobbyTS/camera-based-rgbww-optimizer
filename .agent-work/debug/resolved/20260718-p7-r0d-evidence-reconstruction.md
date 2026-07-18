# P7-R0D formal evidence reconstruction

- 状态：resolved
- 范围：仅修复 `R0C-REV-001/002` 的离线证据审计；未执行设备、网络、`.env` 或灯光调用。
- 基线：`b4779036d9bc9610e967fa5d9514a39463034551`

## 根因

1. `analyze_strip_hsi_pilot._validate_v2_target_evidence` 只校验 target row 自报值未超 cap，未消费 `captures.jsonl`。
2. `analyze_hsi_reference_repeatability._audit_capture_contract` 只比较 command event 与 attempt readback，未与 `plan.captures` 对照，也未从 auto audit 结构重算 physical。
3. runner 的 final off 虽已调用，但未验证返回 payload，无法证明 source 确实关闭。

## 修复

- 新增共享 `hsi_source_evidence` validator，严格验证 frozen plan source state、五通道 strip payload、Ray readback 和 off/on/off grammar。
- Formal v2 从 samples/captures/commands/physical events 重建 start/target logical、physical、selection 和 status，并输出 reported/recomputed 对照。
- P7-R1 对照冻结 capture plan，重算 retained report features、auto structure、base/weak selection 和全部 run counters。
- Runner 首尾 off response mismatch 立即失败，仍由 Python finally 和 shell trap 负责 cleanup。

## 验证

- Focused P7：31/31。
- Full suite：402/402，99.519 s。
- `compileall`、四个 wrapper `zsh -n`、`git diff --check`、`codegraph sync` 通过。
- Retained evidence：`tmp/strip-hsi-pilot-offline/p7-r0d-v2-20260718-final-verified`。

## 边界

P7-R1 仍未授权，真实 reference/repeatability、新 sentinel-v2 与后续阶段未测；Goal 保持 Blocked 并交还 Planner。
