# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_G4_03_OFFLINE_APP_LIFECYCLE_CONVERGENCE_ACCEPTED_CANDIDATE_EVIDENCE`
- archived_at: `2026-08-03T14:36:21-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-03-ZERO-READINESS / pure classifier and frozen 1415 observation`
- source_checkpoint: `109ba1bf483aebb6c7eea55e4c9f46e9fbdfb28c`
- original_body_bytes: `9689`
- original_body_sha256: `cd28ad1226e72b7b546b5d4f8c6622cd6af5593af7890e4ed4883f38091acba2`
- terminal_disposition: `PLANNER_ACCEPTED_G4_03_ZERO_READINESS_WITH_REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1436.md`
- prior_rejection_pointer: `.agent-work/archived/EXECUTION_RESULT-20260803-1415.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_G4_03_TERMINAL_DISPOSITION_AND_G4_04_PLANNING_UNLOCK_REVIEW`
- historical_non_executable: `true`

本archive保留Executer handoff与全部offline validation声明。Planner确认exit `1/-128`、
`request_transport_success=false`和原1415 rejection均未被改写；当前classifier只确认authoritative final effect clean。
本archive不授权G4-04 execution、device、release、formal、retry、external root consumption、commit或后继PLAN。
下方逐字节保留reviewed EXECUTION_RESULT body。

---

# REF-G4-03-ZERO-READINESS：pure offline app-lifecycle convergence handoff

**状态：** `G4_03_ACCEPTANCE_CANDIDATE_AFTER_OFFLINE_APP_LIFECYCLE_CONVERGENCE`

**PLAN contract：** `G4-ZERO-READINESS-APP-LIFECYCLE-CONVERGENCE-V1`

**Reference task：** `REF-G4-03-ZERO-READINESS`

**Planner stop：** `RETURN_FOR_G4_03_APP_LIFECYCLE_CONVERGENCE_REVIEW`

## 1. 结论

现有zero-readiness owner内新增一个frozen、exactly typed app-lifecycle observation record与一个pure classifier。Classifier把graceful request transport与authoritative final effect明确分离：request exit `0`且effect guards全满足时分类为
`REQUEST_CONFIRMED_EFFECT_CONFIRMED_CLEAN`；request exit非0但exact single request与全部effect guards满足时分类为
`REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN`，同时强制保留
`request_transport_success=false`及原exit/error；任一identity、request、variant、poll或residual guard失败均fail closed。

全部offline validation通过后，唯一一次post-test pure invocation对冻结1415 observation得到
`REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN`。该结果不改写原1415 Planner rejection中的事实：exit `1/-128`仍不是request success。Executer只提出
`G4_03_ACCEPTANCE_CANDIDATE_AFTER_OFFLINE_APP_LIFECYCLE_CONVERGENCE`，未自行把G4-03设为PASS、未解锁G4-04、未生成后继task或commit。

本包没有访问app、process、listener、device、network或external experiment root/payload，没有创建production/external root；没有capture、nonzero light、release consumption、formal R6、TD-C、firmware、deployment或config write。

## 2. Activation与intake

- HEAD：`109ba1bf483aebb6c7eea55e4c9f46e9fbdfb28c`
- direct parent：`c7838eece611c92d74dc49e4922af1b133141bac`
- branch：`main`
- activation subject：`docs(plan): activate offline app lifecycle convergence`
- activation changed paths exact：
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
- intake worktree：clean。
- repo-owned PLAN/FULL strict parser：PASS；contract均为
  `G4-ZERO-READINESS-APP-LIFECYCLE-CONVERGENCE-V1`；active task/count均为
  `REF-G4-03-ZERO-READINESS / 1`；canonical next仍为同一task；G4-04 locked。
- G4-01/G4-02未重开；未创建task suffix或corrective reference。

Immutable intake identity：

| owner | bytes | SHA-256 |
|---|---:|---|
| existing source | 28288 | `fea119e6a49825cf5858732c5a27dd0187020b70bc6fa5d6e8e2b3c428dacc8c` |
| existing tests | 16311 | `5e2efcbab079b46ca18e874ee5d684a73586517b58560d793d4bff6fc060a6b7` |
| read-only wrapper | 2969 | `13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a` |

只读的两个1415 archive identity：

| archive | file bytes/SHA-256 | preserved body bytes/SHA-256 |
|---|---|---|
| `.agent-work/archived/PLAN-20260803-1415.md` | `11371` / `8fdc95371fa21eb7a6a486cd9c145a76becae474aacd9159c66464a0689ad188` | `10251` / `8359238500b313c5f4b68ba6afe1b8e31132f9fae356a96cb0f58a36b35de472` |
| `.agent-work/archived/EXECUTION_RESULT-20260803-1415.md` | `10449` / `0f05a0b25394ddde5f499d2e906e51d5d4a546f54bfcd6b10cbe906101835602` | `9377` / `9df3bf1601ae8d13819841188a16f474367d1efdcb907f48f8d23dfd8c3fd287` |

distinct archive read set为exact上述2项；archives未修改。

## 3. 实现与ownership

仅修改现有：

- `src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py`
- `tests/test_p7_successor_zero_readiness.py`

新增public owner surface：

- `AppLifecycleObservation`：frozen dataclass；字段仅为str/int/bool/None及tuple；提供确定性的JSON-native projection。
- `classify_app_lifecycle_observation`：只消费caller冻结的record，不自行观察任何live state。

Classifier返回deep immutable顶层/guard `MappingProxyType`，JSON-native projection exact包含：

```text
schema
classification
request_transport_status
request_transport_success
final_effect_status
request_transport_exit
request_error_code
guards
```

不包含authority、`g4_03_pass`或`g4_04_unlocked`字段。

Guard set exact覆盖：schema、bundle/bundle-id/executable、positive owned PID、non-preexisting、single graceful request、exit/error consistency、force/alternate/service/endpoint variant、poll schedule/count、0秒presence、bounded disappearance、disappearance后持续absent，以及app/listener/owned/scratch四项final residual。

Fail-closed行为：

- exact type validation拒绝bool-as-int、非str、mutable list poll/presence、tuple内错误类型、unknown dict shape。
- request count `0/2`、force/alternate/service/endpoint variant非0、identity drift、pre-existing、poll drift、0秒缺失、deadline未消失、消失后复现、任一final residual非0均不产生clean classification。
- pre-existing app返回明确`NON_OWNED_NOT_APPLICABLE`，不取得owned cleanup credit。
- exit/error不一致返回`APP_LIFECYCLE_FAIL_CLOSED`与transport status `invalid`。

现有readiness执行、root schema、device cleanup、serialization、wrapper与CLI行为未改变。没有新module、controller、persistence owner、wrapper、CLI或I/O path；没有编辑巨型P7模块。

After identity与diff：

| path | bytes | SHA-256 | diff |
|---|---:|---|---:|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py` | 36066 | `ba326702ad53aba06eeef2c12a86753c31bbeaa65bed78139dc777f2047d9193` | `+159/-0` |
| `tests/test_p7_successor_zero_readiness.py` | 25654 | `6bbee82e8e61a65aada750e7d5b74d30157d38b61c8edec4b7d20bd907d1a2dd` | `+173/-1` |

read-only wrapper after identity仍为bytes `2969` / SHA-256
`13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a`。

## 4. Tests与checks

- targeted：`15/15` PASS，`0.048s`，一次调用；未使用bounded correction。
- focused：`125/125` PASS，`2.547s`，一次调用。覆盖zero-readiness、provenance、machine parser、camera/Ray/strip/all-off owner。
- full suite：`879/879` PASS，`155.919s`，一次调用。
- `.venv/bin/python -m compileall -q src tests`：PASS，一次调用。
- `git diff --check`：PASS。
- CodeGraph sync：PASS，modified `2` files / `123` nodes。
- CodeGraph query：classifier只调用本模块的结构validator与纯内建逻辑；没有新增I/O、process、network、device或provenance-writer边。
- wrapper、PLAN、FULL、archives、GUIDE、RESEARCH保持只读。

Full suite产生的仅是测试框架现有temporary fixtures；没有读取或创建任何external experiment root/payload，也没有production/device owner调用。

## 5. 唯一offline classifier invocation

输入record：

```text
schema=g4_app_lifecycle_observation_v1
app_bundle=/Applications/amaran Desktop.app
app_bundle_id=com.sidus.amaran-desktop
app_executable=/Applications/amaran Desktop.app/Contents/MacOS/amaran Desktop
owned_pid=79395
app_preexisting=false
graceful_request_count=1
request_transport_exit=1
request_error_code=-128
force_request_count=0
alternate_request_count=0
poll_elapsed_seconds=(0,1,2,4,8,15)
owned_pid_present=(true,false,false,false,false,false)
final_app_residual_count=0
final_listener_residual_count=0
final_owned_residual_count=0
final_scratch_residual_count=0
service_variant_count=0
endpoint_variant_count=0
```

完整JSON-native output：

```json
{"classification":"REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN","final_effect_status":"confirmed_clean","guards":{"alternate_request_zero":true,"app_bundle_exact":true,"app_bundle_id_exact":true,"app_executable_exact":true,"disappeared_within_bounded_grace":true,"endpoint_variant_zero":true,"final_app_residual_zero":true,"final_listener_residual_zero":true,"final_owned_residual_zero":true,"final_scratch_residual_zero":true,"force_request_zero":true,"graceful_request_exactly_once":true,"non_preexisting":true,"owned_pid_positive":true,"owned_present_at_zero":true,"poll_presence_count_exact":true,"poll_schedule_exact":true,"remained_absent_after_disappearance":true,"schema_exact":true,"service_variant_zero":true,"transport_exit_error_consistent":true},"request_error_code":-128,"request_transport_exit":1,"request_transport_status":"ambiguous_failure","request_transport_success":false,"schema":"g4_app_lifecycle_classification_v1"}
```

Classifier post-test invocation count：`1`。所有guards为true；final effect为confirmed clean；request transport明确为ambiguous failure且success为false。原exit/error未被改写。

## 6. Authority与访问账本

```text
external_experiment_payload_access=0
app_access=0
process_poll=0
listener_access=0
device_access=0
network_access=0
production_or_external_root_access=0
production_or_external_root_creation=0
release_consumption=0
capture_access=0
nonzero_light=0
formal_r6_access=0
td_c_access=0
firmware_access=0
deployment_access=0
config_write_calls=0
new_task_ids=0
corrective_suffixes=0
commit_by_executer=0
```

Prior rejection仍保持：
`REJECTED_G4_03_PASS_APP_GRACEFUL_QUIT_EXIT_MISMATCH_DESPITE_RESIDUAL_ZERO`。本次classifier提供新的工程语义分层，不重写当时request exit事实或Planner局部判定。

## 7. Planner decision request

请Planner先归档PLAN/ER并独立验收：

1. record/classifier exact closed contract、immutability与pure-call boundary；
2. truth-table和所有fail-closed guards；
3. 冻结1415 observation的唯一结果是否支持
   `G4_03_ACCEPTANCE_CANDIDATE_AFTER_OFFLINE_APP_LIFECYCLE_CONVERGENCE`；
4. prior rejection是否被完整保留，且没有把exit `1/-128`表达为request success。

只有Orchestrator可决定G4-03 terminal disposition。本handoff不自行PASS、不解锁G4-04、不生成后继PLAN或task。
