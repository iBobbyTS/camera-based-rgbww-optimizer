# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2：marker-count qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** Executer handoff（本轮未追加 `.agent-work/EXECUTION_RESULT.md`）

**Decision:** `REJECTED_MARKER_COUNT_GATE`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3`

## Reviewed scope and frozen evidence

本次仅进行离线 Planner 验收；未访问 controller、source、candidate、fixture、canonical content、tests、release、retained R3、`.env`、相机、Ray120c、ESPHome、strip、网络或任何设备，也未进行 Git mutation。

- 当前 PLAN raw SHA-256：`eb4607f0d38929b97f5478c6a5b09fa7354eff9ba5bbd87cc6dc5ff7a8bfb864`。
- 当前 FULL raw SHA-256：`a676268f625091fbc2c2a3b7f388dd9b113a4ae247a376354a1e43ff1df82e99`；两者与 frozen handoff 匹配。
- 严格 extraction 发现 PLAN 有 2 条 marker 前缀物理行：canonical line 17，以及 C2 正文中的空 payload line 23；FULL 有 3 条状态 marker 前缀物理行：canonical line 21，以及 C1/C2 section 的空 payload lines 2302/2331。
- 按“恰好一条” gate，首次失败阶段为 `marker-count`；artifact/path counters 为 `0/0`，old-root touch/retry 为 `0/0`，禁止调用为 `0`，未 bootstrap、release 或 device。
- Executer 因 gate failure 未 append ER；因此本审计证据来自 handoff，缺少 ER 原文及其独立 hash，属于 evidence limitation，不能将 `0/0` 解读为整体 pass。

## Planner findings and validation quality

本轮 qualification 在 path-before-gate 规则下于 marker-count 阶段终止。重复 marker 来自正文示例/空 payload，而非可消费的 canonical row；仍不能证明唯一 machine contract 可解析或允许进入任何后续路径。零 artifact/path 仅证明 gate 失败前未产生副作用，不能升级为 package pass、bootstrap evidence 或 release eligibility。`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变。

## Residual risk and stop

在正文不再制造匹配前缀、且 canonical machine row 唯一性重新验证前，loader 仍可能误采集示例行或空 payload。旧 F17 root 与所有相关路径不得检查、创建、复用、修复、重试或通过任何 path operation 证明未触碰。

## Exact next branch

下一 active PLAN 仅允许一次离线 canonical machine-row 唯一性审计及文档 owner 语义修正：正文不得包含可被 loader 匹配的 marker 示例或空 payload；只保留一个完整 canonical row，并重新冻结 PLAN/FULL raw hashes。仍须 path-before-gate，artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；无论 gate pass 或 fail，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次，随后立即 stop，不得读取或触碰旧 root。
