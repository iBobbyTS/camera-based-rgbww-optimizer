# Orchestration recovery gate：等待新 goal

**计划状态：** `NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL`

**Executable：** `false`

**Active task count：** `0`

**Canonical next reference placeholder：** `REF-P7-RECOVERY-NEXT-GOAL`

**当前动作：** 无。等待 Human 明确发起新 goal。

**Planner stop：** `NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL`

**Retired draft archive：** `.agent-work/PLANS/20260801-2152-p7-orchestration-recovery-draft-retirement.md`；bytes `4279`；SHA-256 `18384a4bd1d422d4413265ba90a8582e4a466bb77bc28434084d88935cb7e7b5`。

`PLAN_MACHINE_CONTRACT={"schema":"orchestration_recovery_no_active_plan_v1","plan_status":"NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL","executable":false,"active_task_count":0,"active_task":null,"canonical_next_reference_task":"REF-P7-RECOVERY-NEXT-GOAL","canonical_next_reference_status":"NEW_GOAL_INTAKE_PLACEHOLDER_NON_EXECUTABLE","retired_plan":{"archive_path":".agent-work/PLANS/20260801-2152-p7-orchestration-recovery-draft-retirement.md","archive_bytes":4279,"archive_sha256":"18384a4bd1d422d4413265ba90a8582e4a466bb77bc28434084d88935cb7e7b5","disposition":"RETIRED_HISTORICAL_SUPERSEDED_WAITING_DRAFT","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1-R1-C1-C1-C1-C1-C1","source_blob_oid":"416120e223c23badd470112462d0bf38b7103555","source_bytes":11093,"source_sha256":"0745069a0a97a0c6c5af84ac2ab72c33a3d99843da8dca6971b04a63feb2119f"},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","eligibility":false,"release_consumable":false,"release_consumption_authorized":false,"device_authorized_by_this_file":false,"camera_authorized_by_this_file":false,"ray_authorized_by_this_file":false,"strip_authorized_by_this_file":false,"formal_r6_authorized":false,"td_c_authorized":false,"old_corrective_task_ids_reactivatable":false,"automatic_experiment_package_generation":false,"allowed_next_action":"WAIT_FOR_HUMAN_NEW_GOAL","future_planner_requirement":"WRITE_NEW_PLAN_FROM_THEN_APPLICABLE_GUIDE_HUMAN_GOAL_AND_ORCHESTRATOR_REFERENCE","planner_stop":"NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL"}`

## Non-execution locks

- `REF-P7-RECOVERY-NEXT-GOAL` 只是稳定、平坦的新 goal intake placeholder，不是 active task，不提供 execution、device、retry、stage-entry、budget 或 commit 授权。
- 旧 `REF-P7-25-R2-...` 深层 corrective task ID 与其 predecessor 不得恢复、重试或继续追加 C1/R1/S1 后缀；其内容仅能按既有 archive、Git object 与 evidence 作为历史引用。
- Retained R3 仍为 `RETAINED_UNVALIDATED_UNCONSUMED`。本文件不宣布或授权 canonical validation、eligibility、release consumption、FORMAL-R6、TD-C、network、device、camera、Ray 或 strip 操作。
- 不得从 FULL 的 non-executable route、旧 PLAN、archive 或 EXECUTION_RESULT 自动生成或执行实验工作包。
- 下一步只能等待 Human 发起新 goal。届时未来 Planner 必须根据当时适用的 GUIDE、Human goal 与 Orchestrator canonical reference 新写 PLAN；不得把本 waiting gate 当作该新 PLAN。

维护性判断：当前文件只保留单一非执行状态与 JSON-native machine row，不承载历史 corrective 细节或平行执行语义。
