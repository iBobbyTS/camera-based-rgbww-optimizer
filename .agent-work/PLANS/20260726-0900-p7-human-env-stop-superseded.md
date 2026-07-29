# Planner 归档：Human environment stop 被新 Human 决定替代

**归档日期：** 2026-07-26 09:00

**Reference task ID：** `REF-P7-04`

## 被审查状态

此前 `P7-TD-B-FORMAL-HUMAN-ENV-STOP` 要求 Human 将 `AMARAN_OPENAPI_SECRET` 注入 exact
visible Terminal child。该 stop 源于已接受的 ENV-ACCOUNTING-C1 negative evidence：exit matrix
`11/11`，exact child exit `78`，redacted `present=false` / `parseable=false`，formal/device/network
均为 `0`。该证据保持有效，不重写为执行失败或 readiness pass。

## 新 Human 决定与 Planner 决定

Human 现明确决定恢复 Ray120c 的硬编码公开默认 key，并把“这是公开默认协议 key、不是用户
私密凭据”作为持久项目事实；`AMARAN_OPENAPI_SECRET` 改为 optional override。该较新 Human
决定使 environment stop 不再是当前路线前置条件，因此本归档将其标记为 `superseded_by_human_decision`，
而非 accepted execution、failed execution 或 formal authorization。

仓库历史 parent 中冻结的默认值为
`9veqiL0G0EUOviwzL1prPc0iGIGUJtbzSaPYQfgfyxM=`。本事实来源仅为 Human classification 与仓库
历史；没有仓库证据证明外部厂商文档已验证该分类，后续文档不得作此声称。

## 下一分支

发布一个纯离线 implementation package，恢复公开默认、保留 optional override 的严格校验与
repr exclusion，更新 tests/docs/project skill 并创建 focused commit。Commit 将改变 clean HEAD，
因此现有 `a87b09f...` lineage release 不能自动用于 formal；完成后必须回 Planner 重新处理 lineage，
不得从本 Human 决定或代码提交直接进入设备/formal。

