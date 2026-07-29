# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-R1 changed-path policy hard failure

**审查日期：** 2026-07-26 21:15

## 证据

- exact CLI 已通过后，唯一 offline qualification 在 changed-path policy 阶段抛出
  `PermissionError: TD-B current lineage contains prohibited changes`。
- legacy release、planner candidate、current HEAD 读取均在离线 owner 内完成，但未生成
  usable release 或 output release artifact。
- device/network/hostname/.env-content/setup/formal/public analyzer/camera/Ray/strip/capture/
  CR3/NPY/retry/IP fallback/Git 均为 `0`；旧 `fa6c95d` 文件未改写。

## 决定

拒绝把该失败解释为 release 可用，也不直接放宽 allowlist。现有测试明确将
`AGENTS.md` 分类为 `prohibited_or_unreviewed`，而当前 checkpoint 包含该文件的 workflow/
authorization 文档改动；GUIDE 允许离线 candidate/qualification，但没有明确授权把此类
安全/执行政策文件从 prohibited 改为 lineage-eligible。放宽它会改变 release provenance
与安全语义，不能由 Planner 的机械 ledger correction 推断。

因此本分支升级为 `Advisor decision`：Advisor 需明确选择保持 `AGENTS.md` prohibited 并
排除当前 checkpoint，还是为该类 workflow-only policy change 定义可审计的 allowlist、hash
语义和回滚边界。决策前不重试 qualification、不生成 candidate/release、不访问设备或 formal。

