# Planner 终态审查 — Ray R6 package precondition mismatch

- **审查时间：** 2026-08-06（本次唯一 Planner review）
- **审查对象：** `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`
- **审查输入：** 当前 `.agent-work/PLAN.md`（审查前 SHA-256
  `1ce9f2ec0b38f3915e515c2e8b14d9c42b31d1446ad3b743caf7af8b6fe860d4`）、
  当前 `.agent-work/EXECUTION_RESULT.md`（SHA-256
  `880acca1dac3f645ef7b3321c4c9a267b39aa8583e5e51344c693fb2a9c62e84`）、
  `.agent-work/PLAN-FULL.md`（SHA-256
  `eb2b7fb849bbf957d4d939a4d69a084347bd544813a6b03f7a06883de3fb10f1`）及冻结
  successor release 目录只读证据。

## 证据与 exact mismatch

冻结 successor release 根为：
`/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release`。
下列五个文件均存在且 hash 精确匹配 PLAN：

| 文件 | SHA-256 |
| --- | --- |
| `frozen-inputs.json` | `8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8` |
| `r6-formal-plan.json` | `dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b` |
| `release-descriptor.json` | `6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452` |
| `validation-summary.json` | `07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07` |
| `terminal-seal.json` | `d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850` |

目录的实际 regular-file inventory **恰为上述五项**。现有 production
`load_and_validate_stage_gate_package()` / `stage_gate_package_binding()` 要求的
`launch-descriptor.json` 与 `stage-gate.json` 在该根中均 **MISSING**；它们不是
可从 successor lineage 的五文件别名推导的文件。当前 PLAN 也未声明或提供
独立 `new_stage_gate_root`，而仓库 stage-gate owner 的 input/projection 仍绑定
replacement-package task/contract，不能把该五文件根伪装为 stage-gate package。

## Planner decision

`REJECTED_TERMINAL_ENGINEERING_PRECONDITION_MISMATCH`。

这是 engineering/package contract blocker，不是 scientific failure；没有任何
capture、quality、chronology、history 或 cleanup 科学结果。Executer 的
fail-closed 行为正确：未消费 release、未创建 formal root、未启动 Terminal、相机、
Ray 或设备，未运行 analyzer，retry/launch/capture 均为 `0`。

本边界**不允许 corrective package**：修复需要重建/补写冻结 release，或改变
stage-gate owner/task/authority route，均超出最小工程解除范围并会引入第二 owner。
因此不伪造 `acquisition_fail`、`stop_history_model_required` 或任何科学负结果，
不重试、不创建 second root、不修改 frozen release、GUIDE 或 RESEARCH。

## 下一状态与锁

- 当前 PLAN 已终态降级为 non-executable、`active_task_count=0`。
- `science_delta=none`，`scientific_result_created=false`。
- release/formal/device/network/camera/Ray/strip/capture/analysis/TD-C 全部关闭。
- 下一步仅为 Orchestrator/`sol_max` 对 package-owner 与 successor-release 路线做
  新的语义重评；本归档不授权下一包、设备或 release 消费。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6","plan_status":"PLANNER_STOP_TERMINAL_ENGINEERING_PRECONDITION_MISMATCH","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6","planner_decision":"REJECTED_TERMINAL_ENGINEERING_PRECONDITION_MISMATCH","classification":"engineering_package_contract_blocker","corrective_package_allowed":false,"science_delta":"none","scientific_result_created":false,"release_consumption_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"td_c_authorized":false,"retry":0,"alternate_root":0,"planner_stop":"RETURN_TO_ORCHESTRATOR_FOR_PACKAGE_OWNER_AND_RELEASE_ROUTE_REASSESSMENT"}`
