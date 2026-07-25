# Human / Orchestrator priority-selection等待门

**计划状态：** `explicit_planner_stop_waiting_for_human_priority_selection`

**Planner 日期：** `2026-07-25`

**Reference task ID：** `NONE_AWAITING_ORCHESTRATOR_SELECTION`

**PLAN contract ID：** `WORKFLOW-AWAIT-PRIORITY-R1`

**Package kind：** `planner_stop_no_execution`

**Current HEAD：** `3f8fb5c2f046ad5c75eab200005331acd5f2cc27`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"WORKFLOW-AWAIT-PRIORITY-R1","reference_task_id":"NONE_AWAITING_ORCHESTRATOR_SELECTION","package_kind":"planner_stop_no_execution","expected_head":"3f8fb5c2f046ad5c75eab200005331acd5f2cc27"}`

**当前唯一动作：** Orchestrator将`REF-WORKFLOW-01`更新为`COMPLETE`，保留P7/Z0相关reference的paused/blocked状态，并依据刷新后的
`FULL_PLAN_REFERENCE.md`向Human呈现仍未完成的优先级选项；等待Human明确选择下一reference。不得派发Executor或从本PLAN推断实验恢复。

**唯一 Planner 停止点：** 在Human给出新的明确优先级、或出现新的适用Advisor guidance前，保持本Planner stop。收到选择后，Planner必须
先归档本等待门，再基于届时HEAD、FULL与GUIDE另写一个single executable package；本PLAN本身不授权任何实现、Git或设备动作。

## 1. 已完成baseline

- `REF-WORKFLOW-01` implementation与commit finalization均已接受。
- final commit：`3f8fb5c2f046ad5c75eab200005331acd5f2cc27`；parent
  `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`。
- final review archive：`.agent-work/PLANS/20260725-1410-ref-workflow-01-commit-final-review.md`，SHA-256
  `be445be5277f350a1f7b9bc41c7b8fcfaa30e63b42f8f759b1cbfda9050b1880`。
- exact commit包含13个已验收paths；parent/message/path set/blob hashes/index与unrelated preservation均通过Planner独立核验。
- 实现baseline：focused `51/51`；skill `41300 -> 4678` bytes；old exact credential current count `0`；credential/API/help/static/
  link/CodeGraph checks通过；network/device/actual credential reads均`0`。
- full `557/559`中的两个TD-B lineage errors已分类为frozen committed HEAD baseline debt，不影响`REF-WORKFLOW-01`完成。

完成只表示移除Ray built-in credential default、建立shared local-lab context并完成相关文档/skill progressive disclosure；它降低possible
platform misclassification信号但不保证分类结果，也不改变平台policy。

## 2. 仍暂停且不得自动恢复

- P7 lineage baseline test debt仍属于P7 engineering路径；本等待门不授权修复。
- `REV-Z0-R2-EVIDENCE-TREE-005`与`REV-Z0-R2-WRAPPER-BYTE-COPY-006`仍open。
- Z0-R2-C1先前因Human最高优先级切换而superseded/paused，不是执行失败；其旧PLAN不能复用为authorization。
- real Z0、E2、Ray/strip/camera操作、capture、formal、TD-C、sentinel、remaining、boundary、holdout、Gate-6与P8全部保持
  paused/blocked/locked，直到Human选择且Orchestrator更新reference、Planner发布新PLAN。

Human若选择恢复P7，Planner必须基于new HEAD重新冻结inputs并处理lineage baseline/checkpoint影响；不得直接续跑旧root、旧PLAN或旧budget。
若选择需要新的科学方向且现有GUIDE不足或矛盾，由Orchestrator暂停对应route并请求Advisor；workflow closure本身不需要Advisor。

## 3. 本等待门的零预算

```text
executor_dispatch = 0
implementation_or_documentation_edits = 0
test_or_module_execution = 0
git_stage_or_commit = 0
git_push_or_pr = 0
network_calls = 0
device_calls = 0
credential_or_secret_reads = 0
camera_calls = 0
ray_calls = 0
strip_calls = 0
light_nonzero_output = 0
z0_runs = 0
e2_runs = 0
capture_or_formal = 0
firmware_or_deployment = 0
```

本PLAN是明确的non-executable Planner stop，不是Executor work package。FULL仍由Orchestrator独占维护，GUIDE/RESEARCH保持Advisor-owned；
任何reference status或优先级变化必须先由对应owner记录，再触发下一次Planner规划。
