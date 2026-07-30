# REF-P7-25-R2-B2-C4-P2-C4：accepted integration qualification / Orchestrator route gate

**计划状态：** `PLANNER_ACCEPTED_EXECUTION_NOT_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reviewed reference task：** `REF-P7-25-R2-B2-C4-P2-C4`

**Reviewed contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C4-OBSERVABLE-FULL-VALIDATION-V1`

**Planner decision：**
`ACCEPTED_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_ORCHESTRATOR_PROVENANCE_ROUTE`

**当前唯一动作：** Orchestrator 独立审核本 decision，更新其独占的
`.agent-work/FULL_PLAN_REFERENCE.md`，并选择、冻结一个新的 provenance-bound C4 或
real-B2 engineering reference task；然后才可交 Planner 另写一个独立 executable package。

**唯一 Planner stop：**
`B2_C4_P2_C4_ACCEPTED_WAITING_ORCHESTRATOR_NEXT_PROVENANCE_ROUTE`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1346-p7-retained-r3-option-b-b2-c4-p2-c4-integration-qualification-review.md`，
bytes `6920`，SHA-256
`73fb12fd71589d478c5379c182af7fdb976ac05ddec6b4482d83a87a14adfb9d`。

**Earlier archive preserved：**
`.agent-work/PLANS/20260730-1329-p7-retained-r3-option-b-b2-c4-p2-c3-full-output-review.md`，
bytes `6985`，SHA-256
`a76dc1be89ba2e2bed3ca6baef8a11ac3b2e9583be5aef23687407017cd9e4be`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_c4_planner_acceptance_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2-C4","reviewed_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C4-OBSERVABLE-FULL-VALIDATION-V1","execution_authorized":false,"planner_decision":"ACCEPTED_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_ORCHESTRATOR_PROVENANCE_ROUTE","single_current_action":"orchestrator_select_and_freeze_next_provenance_bound_c4_or_real_b2_engineering_route","accepted_implementation_commit":"4e82a7d089ff8bc4baef653a4a19f85d23d0b882","accepted_full_suite":{"command":".venv/bin/python -m unittest discover -s tests -p 'test_*.py' -q","invocations":1,"same_session_terminal_exit":0,"tests":717,"terminal":"OK"},"accepted_postcommit_targeted":"5/5","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"next_package":"not_selected_or_authorized","planner_stop":"B2_C4_P2_C4_ACCEPTED_WAITING_ORCHESTRATOR_NEXT_PROVENANCE_ROUTE"}`

## 1. Accepted result

Planner 接受 P2-C4。当前 exact implementation commit 为
`4e82a7d089ff8bc4baef653a4a19f85d23d0b882`，parent 为
`1dd88a07d00f9b2e94638e4c3ed67f8c03525515`，subject 为
`test(p7): qualify retained r3 controller composition`，tree change 是 exact singleton：

```text
tests/test_p7_retained_r3_controller_integration.py
```

该文件 bytes `13148`，SHA-256
`740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366`，blob OID
`56c9ab686820af193c3e53e776e849905b243b4a`；canonical binary patch bytes `13752`，
SHA-256 `e3e7a6d9a555ec22c41e61cfd7f3fc8275e4236e2dbc0588c6298a068aac5a09`。

接受的 validation evidence 包括：

- preserved corrected targeted `5/5`、owner `32/32`、focused `58/58`，本 continuation
  rerun `0`；
- 唯一 quiet full invocation 的 same-session structured exit `0`、唯一
  `Ran 717 tests in 160.789s` 与 `OK`；
- compileall exit `0`；CodeGraph sync exit `0` / `Already up to date`；
- exact singleton scope/stage/blob/file/patch identities；
- unique postcommit targeted `5/5` / `OK`；
- retry、fallback、second full、second commit、amend 与 implementation edit 全为 `0`；
- historical/retained reads、actual validator、eligibility、release、network/device 与
  external-root operations 全为 `0`。

完整验收方法、证据和 residual risks 只保存在本次 review archive，active PLAN 不再保留
已完成执行细节。

## 2. Current gate and hard locks

本 PLAN 不授权 Executer，也不授权任何 source/test edit、test/compile/CodeGraph invocation、
Git commit、external evidence root、retained-R3 access、real B2/controller dispatch、canonical
validator、eligibility、lineage/release/consumer、network、设备、相机、Ray、strip、cleanup、
capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware 或 deployment。

`RETAINED_UNVALIDATED_UNCONSUMED` 必须保持不变。Synthetic integration qualification 不是
real retained-R3 audit、validator eligibility 或 release authorization。

下一步是 Orchestrator-owned engineering/provenance selection，不是 unresolved color science，
无需 Advisor；也不是高风险设备操作，无需 Human authorization。Orchestrator 选择新 route
并更新 FULL reference 后，Planner 必须重新写一个只含该 route 的 executable PLAN，任何
后续执行才可开始。

## 维护性判断

已接受的 singleton integration test 组合现有 preparation 与 lifecycle owner，没有新增
production owner、parallel validator 或执行框架。当前只保留一个不可执行选路门，避免在
active PLAN 中积累历史或提前展开未来设计。
