# Planner 离线 policy-source review：AGENTS.md Human decision

**审查日期：** 2026-07-26 21:45

## 结论

Human 已明确要求将项目授权边界改为：只有远程 firmware 等危险操作需要人类授权；
offline release 与 Ray/RGBWW 开关灯不需要另行授权。该决定已落入冻结的
`AGENTS.md`，当前 blob SHA-256 为
`a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5`，相对旧
`fa6c95d` 的 AGENTS hash `f4a4a9edffb563c0ea7709382b53eed919c4a5528c69ffa9878a4c32348ee99b`。

该 Human decision 足以覆盖 changed-path lineage allowlist 对这一个 workflow/authorization
policy 文件的分类：它不是科学模型、相机/remote parsing、setup semantics、frozen input、
budget、command、shutter 或 cleanup 的变更。无需 Advisor 提供科学语义；仍需一个纯离线
policy/allowlist freeze 来固定 scope、hash、provenance 与 rollback，不可直接重跑 qualification。

