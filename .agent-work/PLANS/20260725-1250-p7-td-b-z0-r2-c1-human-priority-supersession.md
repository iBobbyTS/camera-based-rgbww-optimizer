# P7-TD-B Z0-R2-C1 Human-priority supersession归档

**归档时间：** `2026-07-25T12:50:00-0600`

**归档角色：** Planner

**被归档 active PLAN SHA-256：**
`d4cba3c75cb45a45b67805e74126a76efb8746c8f75eb3d41c9d7f8498d691c8`

**Planner 决定：** `human_priority_superseded_and_paused_without_execution`

**精确下一分支：** `REF-WORKFLOW-01_PLATFORM_FALSE_POSITIVE_RISK_REDUCTION`

## 原计划范围

原计划`P7-TD-B-F0B-R1-C3-E2-R1-Z0-R2-C1`只授权一个external offline package，用于修复
`REV-Z0-R2-EVIDENCE-TREE-005`与`REV-Z0-R2-WRAPPER-BYTE-COPY-006`，明确immutable evidence-tree、executable source和
binary wrapper-copy owners，并在不得访问device/network/secrets的边界内运行no-device regression。

## Supersession事实

Human将“降低平台possible cybersecurity risk误判”设为最高优先级，要求立即暂停尚未执行的Z0-R2-C1。归档时没有该contract
对应的fresh root、source、matrix、validation或`EXECUTION_RESULT.md`执行段；所有package/matrix/real/device budgets均未消费。

因此本归档是priority supersession/pause，**不是执行失败、Planner拒绝或finding恶化**。两个Z0-R2 findings保持open，未来恢复时
必须由Human/Orchestrator重新选择reference、由Planner基于当时HEAD与evidence另写active PLAN；不得直接重用被归档计划作为授权。

## 新优先级与边界

下一active package只处理本地仓库的workflow/platform context信号：移除Ray production-looking credential默认值，统一三个control
CLI/module的user-owned local-lab calibration语境，给AGENTS加入简短正向scope，集中记录本地连接边界，并把project skill中的P7历史
细节迁到普通engineering docs后缩成progressive入口。

该包严格offline：不得读取`.env`或任何实际credential内容，不得访问hostname/network/device，不得控制灯光或相机，不得运行Z0、
E2、capture、formal、firmware或deployment。GUIDE与FULL_PLAN_REFERENCE保持只读。

## Evidence与残余风险

- 原active PLAN：`.agent-work/PLAN.md` at supersession，bytes `12845`，SHA-256
  `d4cba3c75cb45a45b67805e74126a76efb8746c8f75eb3d41c9d7f8498d691c8`。
- current HEAD：`8cd04d847d42ff5c7bcf7501f46be97cbbef429d`。
- 未产生Z0-R2-C1 execution evidence；既有Z0-R2 failure evidence和review archive保持不变。
- 残余风险：两个pre-device engineering findings仍open；real Z0、E2和所有后续科学任务继续paused/locked，直到Human优先任务完成并由
  Orchestrator重新排程。
