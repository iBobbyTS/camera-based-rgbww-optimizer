# REF-G4-04-E2 Package A terminal checkpoint

**计划状态：** `TERMINAL_ACCEPTED_WAITING_ORCHESTRATOR_SOURCE_CHECKPOINT`

**Executable：** `false`

**Active task count：** `0`

**Reviewed reference task：** `REF-G4-04-E2`

**Terminal disposition：** `ACCEPTED_G4_04_E2_FRESH_ROOT_SOURCE_BINDING_ENGINEERING_UNIT_ONLY`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":"G4-E2-FRESH-ROOT-BINDING-ENABLING-V1","plan_status":"TERMINAL_ACCEPTED_WAITING_ORCHESTRATOR_SOURCE_CHECKPOINT","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","terminal_disposition":"ACCEPTED_G4_04_E2_FRESH_ROOT_SOURCE_BINDING_ENGINEERING_UNIT_ONLY","planner_review_complete":true,"source_checkpoint_pending_commit":true,"accepted_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":27874,"sha256":"717db782214c60681c6876d94213637f0a75ed4f380e8e5e2971b58cbb436747"},"accepted_tests":{"path":"tests/test_p7_successor_e2.py","bytes":53423,"sha256":"24b2f8a89dc79ac15ed1537aad34380ebe5ffc9259733927f46cc0eceadec4f3"},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1705.md","bytes":19743,"sha256":"83f0b46e09f77a2a98e52c06f10ba8a2b795c66fe7ee7e7c3643edea8b3b9010"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1705.md","bytes":11360,"sha256":"880bc3338cf52bf953ddfcab4c57c82cde1e6c41e657c83d1e87644136ecd530"},"planner_independent_targeted":{"tests":38,"passed":38},"executer_final_validation":{"focused_tests":237,"focused_passed":237,"full_tests":917,"full_passed":917},"human_rule_exception":"STALE_HARNESS_EXPECTATION_AFTER_INTENTIONAL_RUN_SPECIFIC_SOURCE_BINDING","ordinary_production_failure":false,"fresh_root_source_binding_accepted":true,"guide_fresh_e2_satisfied":false,"fresh_durable_e2_generated":false,"fresh_durable_e2_accepted":false,"g4_04_stage_complete":false,"g4_05_planning_unlocked":false,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"release_consumption_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"formal_r6_authorized":false,"td_c_authorized":false,"next_owner":"Orchestrator","next_action":"CREATE_ONE_FOCUSED_PACKAGE_A_SOURCE_CHECKPOINT_COMMIT_THEN_REQUEST_SEPARATE_PACKAGE_B_FRESH_E2_EVIDENCE_PLAN","future_reference_task":"REF-G4-04-E2","future_reference_status":"WAITING_CLEAN_COMMITTED_PACKAGE_A_SOURCE_CHECKPOINT","planner_stop":"ORCHESTRATOR_REVIEW_AND_COMMIT_PACKAGE_A_SOURCE_CHECKPOINT"}`

## Accepted scope

Planner接受且只接受同一`REF-G4-04-E2`内的Package A工程单元：

- repo-owned factory显式绑定fresh `output_root`与未来accepted `source_checkpoint/source_tree`；
- root/source validators为pure lexical，source truth不能由artifact ledger自证；
- persist把已验证source pair直接交给canonical replay，public replay显式接收trusted pair；
- cross-root transplant、forged source self-report与created-root identity drift均fail closed；
- test roots由exact provenance identity持有并以allowlisted regular-file inventory安全清理。

Human-rule exact两行stale-harness例外分类为
`STALE_HARNESS_EXPECTATION_AFTER_INTENTIONAL_RUN_SPECIFIC_SOURCE_BINDING`；它不是production owner failure，也没有打开新的bounded correction。

## Review evidence

- Planner独立targeted：`38/38 PASS`。
- Planner high-risk static probe：public signatures、pure validators、persist→canonical replay exact args、PLAN/FULL intake一致性均PASS。
- Executer fresh terminal evidence：focused `237/237 PASS`、full `917/917 PASS`、compile/static/source scan/CodeGraph与diff-check PASS。
- Reviewed PLAN archive：
  `.agent-work/archived/PLAN-20260803-1705.md`，19743 bytes，
  SHA-256 `83f0b46e09f77a2a98e52c06f10ba8a2b795c66fe7ee7e7c3643edea8b3b9010`。
- Reviewed ER archive：
  `.agent-work/archived/EXECUTION_RESULT-20260803-1705.md`，11360 bytes，
  SHA-256 `880bc3338cf52bf953ddfcab4c57c82cde1e6c41e657c83d1e87644136ecd530`。

## Exact stop

本文件不授权任何执行。fresh durable E2仍未生成或接受，G4-04 stage未完成，G4-05 planning/execution与G4-06仍锁定。

下一步只能由Orchestrator审查并为accepted Package A source/test与本checkpoint创建一个focused clean source checkpoint。只有该commit/tree
成立后，Planner才可在Orchestrator另行委派时为同一`REF-G4-04-E2`起草独立Package B fresh E2 evidence PLAN，并显式冻结该accepted HEAD/tree。
本轮不得起草或执行Package B，不得访问device、release、formal或external experiment payload。
