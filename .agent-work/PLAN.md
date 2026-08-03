# REF-G4-04-E2：Planner rejection checkpoint

**计划状态：** `TERMINAL_REJECTED_WAITING_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_REPLAY_CLOSURE`

**Executable：** `false`

**Active task count：** `0`

**Active task：** `null`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_OFFLINE_RESULT_REPLAY_CLOSURE`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":null,"plan_status":"TERMINAL_REJECTED_WAITING_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_REPLAY_CLOSURE","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"REJECTED_CURRENT_CANDIDATE_WAITING_BOUNDED_SAME_REFERENCE_OFFLINE_CORRECTION","terminal_disposition":"REJECTED_G4_04_E2_ACCEPTANCE_OPEN_RESULT_PERSISTENCE_AND_REPLAY_CONTRACT","review_source_head":"cda4f63b3428dc7c1e77510cebd7cb68a4a10a47","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1514.md","bytes":15973,"sha256":"68e806c7f6610a26f7d156ff5258ea279f95210e4bd5751f2005c26ed8ecff6b","source_body_bytes":14719,"source_body_sha256":"9fd6a8638c7137aa059267603d4a2eb6484b1251e04711bd8f3d1223d91c6817"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1514.md","bytes":8688,"sha256":"243a00e4c890ff232c9068f549c45b66a748954ceec7dc13ee56916167db496d","source_body_bytes":7488,"source_body_sha256":"0d5638d6c97e5f6cd3a7bfa6b807148ab477d757ec3070edf1cc55db1d43d6fc"},"rejected_candidate_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":24222,"sha256":"20bd2ca3fe1bbf2931b7f2605c307ed00fe8c0848734e68edbe35600ba8c4fed"},"rejected_candidate_tests":{"path":"tests/test_p7_successor_e2.py","bytes":16170,"sha256":"354f61e34ba714895f0fcd2b0ac50ef654ed8f685174f6ef76a1719d08c3ec1d"},"accepted_validation_evidence":{"targeted":"13_of_13_pass","focused":"245_of_245_pass","full":"892_of_892_pass","compileall":"pass","wrapper_syntax":"pass","source_scan":"pass_zero_findings","codegraph_sync":"pass","git_diff_check":"pass"},"primary_finding":"PERSIST_AND_REPLAY_ACCEPT_OPEN_OR_FORGED_RESULT_WITHOUT_CLOSED_SEMANTIC_REVALIDATION","ownership_finding":"LOCAL_FORMAL_PLAN_LITERAL_DUPLICATES_EXISTING_THERMAL_OWNER_AFTER_EXISTING_VALIDATOR_CALL","same_reference_bounded_correction_allowed":true,"same_reference":"REF-G4-04-E2","new_task_ids_allowed":false,"corrective_suffixes_allowed":false,"new_root_allowed":false,"existing_e2_root_access_allowed":false,"existing_e2_package_status":"REJECTED_UNTRUSTED_HISTORICAL_IDENTITY_ONLY","device_access_allowed":false,"network_access_allowed":false,"release_consumption_allowed":false,"formal_r6_allowed":false,"g4_05_planning_unlocked":false,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"future_reference_task":"REF-G4-04-E2","future_reference_status":"WAITING_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_OFFLINE_CORRECTION_NOT_EXECUTABLE","human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_OFFLINE_RESULT_REPLAY_CLOSURE"}`

## Planner decision

当前G4-04 E2 candidate被拒绝。`persist_e2_package`只要求任意Mapping的`status`等于PASS；它不要求result来自
`evaluate_e2_preformal_gate`，也不执行closed result contract。`replay_e2_package`只检查schema/status、
`all(result.get("guards", {}).values())`、一个authority位和`formal_plan.executable`；空guards会通过，open/missing字段、
authority其余位、冻结reference ledger、完整formal plan及machine status均没有重验。攻击者可持久化伪造result，owner随后会为它
生成一致terminal；该同步two-artifact package仍可replay PASS。

Tests只覆盖inventory drift及真实evaluator result的happy path，没有覆盖forged/open result、empty/missing/extra/false guard、
authority、reference ledger、formal plan、machine status或同步terminal tampering。因此`13/245/892`及compile/wrapper/source-scan/
CodeGraph绿证据不能关闭此provenance边界。

此外，owner在调用既有`thermal.validate_td_b_r6_formal_plan`之后，又在`_validate_formal_plan`复制完整formal plan字面合同。
这违反本PLAN的现有owner复用约束。Persistence I/O本身仍正确委托repo-owned provenance owner；没有发现device/network/process或
旧controller调用。

## 唯一允许的后续工程边界

Orchestrator可在同一`REF-G4-04-E2`下请求一次bounded offline correction，但当前checkpoint不授权执行。最小修订必须：

1. 建立一个closed result validator，并由evaluate、persist、replay共同复用；严格验证top-level/nested exact keys、exact guard set且
   每项`is True`、完整authority false/0、reference ledger等于exact frozen input projection。
2. Replay对decoded formal plan调用现有thermal validator，并与现有builder结果一致；machine status与现有owner结果一致。删除本地
   formal-plan字面语义副本，不得建立第二个formal owner。
3. Terminal schema/authority/result identity同样closed；同步伪造result+terminal必须fail closed。
4. 补充上述result/replay tamper测试。Correction只能编辑现有candidate source/test与ER，不得新建module、task ID、suffix、root，
   不得访问或修补已生成E2 root，不得访问device/network/release/formal。

已生成E2 package只保留为ER记录的rejected historical identity，不取得acceptance或后续stage credit。

## Stop

停止于`RETURN_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_OFFLINE_RESULT_REPLAY_CLOSURE`。G4-05/06保持locked；本文件不是
corrective executable PLAN，也不授权任何root或实验动作。
