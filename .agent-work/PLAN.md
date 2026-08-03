# REF-G4-01-SUCCESSOR-LINEAGE：provenance/state seam 第二次 owner reassessment

**计划状态：** `EXECUTABLE_BOUNDED_PURE_OFFLINE_SECOND_SEAM_REASSESSMENT`

**Executable：** `true`

**Active task count：** `1`

**Active task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Planner review disposition：** `REJECTED_HIGH_RISK_PROVENANCE_STATE_SEAM_SECOND_PASS_REQUIRED`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-SUCCESSOR-LINEAGE-PROVENANCE-SEAM-REASSESSMENT-V2","plan_status":"EXECUTABLE_BOUNDED_PURE_OFFLINE_SECOND_SEAM_REASSESSMENT","executable":true,"active_task_count":1,"active_task":"REF-G4-01-SUCCESSOR-LINEAGE","reference_task_id":"REF-G4-01-SUCCESSOR-LINEAGE","reference_goal":"REF-G4-COMPLETE","package_kind":"bounded_pure_offline_existing_owner_extension_and_composition_repair","same_boundary_failure_ordinal":2,"review_source_head":"c0e47c482ba0dfb9c004c0e67383e012ab56073e","review_source_tree":"ff51ee655d5dfe1f1337f5a756e9daac9c883ade","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260802-2320.md","bytes":19849,"sha256":"e40698084b84f1e7e3b4e5176d44c215345015e9b40cc405763ee8f88086fad7"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260802-2320.md","bytes":11889,"sha256":"52feabe4be3510368e7429733afeb97d4923a1d7f6d153ec9ad0ddec8844c13d"},"policy_bytes_decoder":"PROVENANCE_STRICT_JSON_BYTES_NONCANONICAL_INPUT_V1","bundle_state_machine":"CANDIDATE_DESCRIPTOR_THEN_PUBLIC_SUMMARY_THEN_TERMINAL_LAST_PENDING_INDEPENDENT_REPLAY","independent_replay_results_persisted_in_bundle":false,"single_current_action":"repair_the_five_frozen_and_three_additional_same_root_provenance_findings_by_minimally_extending_the_existing_provenance_owner_and_reducing_successor_to_composition_only","allowed_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_successor_lineage.py","tests/test_p7_retained_r3_provenance_io.py",".agent-work/EXECUTION_RESULT.md"],"production_source_edits":2,"test_file_edits":2,"giant_p7_module_edits":0,"config_edits":0,"guide_edits":0,"research_edits":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"release_root_acquisition":0,"release_generation":0,"public_validator_invocations":0,"final_validator_invocations":0,"strict_validator_invocations":0,"release_consumption":0,"retained_r3_access":0,"legacy_release_access":0,"external_experiment_payload_access":0,"full_suite_invocations":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"ordinary_bounded_correction_cap":0,"corrective_task_id_creation":0,"third_same_boundary_failure_action":"STOP_RETURN_ORCHESTRATOR_NO_FURTHER_REPAIR","planner_stop":"RETURN_FOR_SECOND_SEAM_REASSESSMENT_REVIEW_OR_THIRD_FAILURE_STOP","future_reference_task":"REF-G4-01-SUCCESSOR-LINEAGE","future_stage_locked":true}`

## 1. Review decision 与唯一 stop

首包 **reject**。Targeted `9/9`、focused `44/44` 及 Orchestrator独立 `836/836` 证明普通回归面为绿，不能关闭
下列纯合成可复现的 high-risk provenance/state findings。当前task保持同一 flat
`REF-G4-01-SUCCESSOR-LINEAGE`；不得创建suffix、corrective task、release root或新semantic owner。

本包是同一 seam 的第二次 owner reassessment，只允许一次实现。任一 Must Fix仍可复现、任何新同根high-risk缺口、
或验证失败，即计为第三次同边界失败并执行
`STOP_RETURN_ORCHESTRATOR_NO_FURTHER_REPAIR`；不得在本包内再修。

**唯一 Planner stop：**
`RETURN_FOR_SECOND_SEAM_REASSESSMENT_REVIEW_OR_THIRD_FAILURE_STOP`。

## 2. Reviewed evidence与输入冻结

```text
review source HEAD = c0e47c482ba0dfb9c004c0e67383e012ab56073e
review source tree = ff51ee655d5dfe1f1337f5a756e9daac9c883ade
reviewed PLAN archive = .agent-work/archived/PLAN-20260802-2320.md
  bytes/SHA-256 = 19849 / e40698084b84f1e7e3b4e5176d44c215345015e9b40cc405763ee8f88086fad7
reviewed ER archive = .agent-work/archived/EXECUTION_RESULT-20260802-2320.md
  bytes/SHA-256 = 11889 / 52feabe4be3510368e7429733afeb97d4923a1d7f6d153ec9ad0ddec8844c13d
candidate module = src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
  bytes/SHA-256 = 23185 / 4fdd7fe880650c98fc9ffad0520a2e8bd15c371c206484905e72f8cb298a1240
candidate tests = tests/test_p7_successor_lineage.py
  bytes/SHA-256 = 16284 / b269dcf99b20c731d75dda622fcb5bc9597f572819c2c85d9aae8e34ad3ed46e
GUIDE SHA-256 = 659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
post-EQ checkpoint = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
policy path/SHA-256 = config/hsi/p7-ray-td-b-exposure-policy-v2.json /
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
accepted EQ manifest bytes/SHA-256 = 7980 /
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

Orchestrator激活本 PLAN后，Executer只接受上述两个candidate file为继承的未提交实现；archive immutable。
其他dirty/staged/untracked内容即停。不得要求 PLAN自嵌future commit SHA；dispatch必须提供current HEAD、parent、subject、
exact activation paths，Executer只读证明activation未修改candidate/provenance/test/config/GUIDE/FULL内容。

## 3. Must Fix ledger

### `REV-G4-01-001 SOURCE_ATTESTATION_FALSE`

`source_checkpoint`、tree、HEAD、index/worktree状态必须由真实Git事实产生，禁止caller自报。最小扩展
`p7_retained_r3_provenance_io.py`，提供一个typed source identity owner；其内部只通过扩展后的
`run_read_only_git` exact allowlist读取 `HEAD^{commit}`、exact checkpoint tree及porcelain staged/unstaged/untracked状态。
返回值必须同时绑定repo physical path、HEAD、checkpoint、tree、index/worktree clean，并由successor module消费。
successor module不得直接调用subprocess或自己解析Git输出。

### `REV-G4-01-002 POLICY_IDENTITY_SEMANTIC_SPLIT`

现有policy是合法pretty JSON（4065 bytes），不是repo canonical compact JSON；不得调用
`provenance.decode_canonical_json()`。最小扩展provenance owner新增
`decode_strict_json_bytes()`（或职责完全等价的具名API）：严格UTF-8、拒绝BOM、duplicate key、NaN/Infinity及
unsupported JSON value，但**不要求re-encode后与原bytes canonical相等**。Successor必须只将同一次
`read_exact_file()` 返回的 `FileIdentity.data` 交该decoder，再交existing thermal in-memory policy validator；禁止随后
按path二次读取、禁止successor自行调用`json.loads`或复制strict JSON owner。Policy reference、semantic contract与SHA
必须来自同一FileIdentity。测试必须使用当前pretty JSON形状positive fixture，并证明duplicate/nonfinite/invalid UTF-8、
identity bytes与semantic contract不一致、fixture schema伪装均拒绝。

### `REV-G4-01-003 SAFE_PARENT_SYMLINK_ESCAPE`

最小扩展provenance owner以取得 canonical、no-follow parent directory identity，并以该identity创建一个exact direct
child；create前后都必须重验parent dev/inode/mode/path。Successor只传parent identity与一个direct-child name，不做词法
`Path.parent`安全判断。symlink parent、parent swap、escape、preexisting child全部fail closed。

### `REV-G4-01-004 CROSS_ARTIFACT_REPLAY_GAP`

共享internal schema checker逐项绑定：descriptor的两个preterminal refs、public validation summary中的descriptor
bytes/SHA与全部authority、terminal前四refs，必须分别与实际 `FileIdentity` exact相等。Final replay和strict validator
都必须在terminal写完后各自读取真实五artifact，验证closed schema、cross-reference、artifact order、terminal
non-circularity及pending-replay seal语义；不能只看status/path，也不能把public semantic pass冒充final/strict pass。

### `REV-G4-01-005 OPEN_AUTHORITY_SCHEMA`

五个artifact全部使用exact key set。任何额外authority/downstream claim，包括但不限于
`release_usable`、`production_release_usable`、`product_ready`、`formal_pass` 均拒绝；retained、eligibility、consumption、
device、formal字段只允许合同中的exact false/status。Public/final/strict三条入口全部执行同一closed-schema helper。

### 同根新增finding

- `REV-G4-01-006 FAILURE_SEAL_ABSENT`：实现必须使用无循环state machine。Descriptor只能是candidate且
  non-authorizing；public summary只能声明descriptor semantic pass，不能声明final/strict。Terminal必须是第五件且最后
  persist，success状态只能为 `sealed_non_authorizing_pending_independent_replay`（或冻结的完全等价literal），authority
  全false，不声明final/strict pass。Terminal写前任何失败且terminal target仍可exclusive-create时，写truthful fail seal：
  primary failure、已存在artifact exact refs、authority false；seal失败保留原primary并向caller报告双失败。Terminal写后
  final/strict失败时不得覆盖、repair或retry pending seal，只在返回值/exception/ER记录primary failure。
- `REV-G4-01-007 VALIDATOR_ACCOUNTING_UNDERCOUNT`：final/strict内部再次调用public函数却不计数。提取一个无counter的
  shared closed-schema helper；public/final/strict各自入口恰好计数一次，彼此不得调用另一个public入口。
- `REV-G4-01-008 PREVALIDATION_STATUS_LIE`：descriptor在验证前即写
  `fresh_successor_lineage_validated_unconsumed`。Descriptor改为candidate/non-authorizing；public summary只记录public
  semantic pass；terminal-last只记录sealed/pending independent replay。Final/strict各运行一次并真实读取五件，其pass结果
  只存在compose返回值与ER；future consumer必须重放，绝不能把pending seal本身当validation proof。失败root任何artifact
  都不得声称validated/final/strict pass。

## 4. Owner/state seam与exact scope

唯一允许修改：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`：只新增通用Git source identity、canonical
   parent/direct-child primitive及strict-noncanonical-input JSON bytes decoder；保持filesystem/Git/JSON单一source of truth。
2. `tests/test_p7_retained_r3_provenance_io.py`：上述primitive的真实behavior、race/symlink/dirty/staged/untracked测试。
3. `src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py`：删除caller自报、path safety、二次policy读取与
   open-schema逻辑；只组合provenance与thermal owners并负责Guide4 artifact state machine。
4. `tests/test_p7_successor_lineage.py`：五项frozen finding和三项新增finding的合成回归。
5. `.agent-work/EXECUTION_RESULT.md`：handoff only。

三个巨型P7模块、config、docs、skill、GUIDE/RESEARCH、PLAN/FULL、archive均不得改。不得新增adapter/controller/module。
若需要第六个path或更改scientific contract，立即第三次stop。

## 5. 验证合同

先做CodeGraph owner query；实现后运行 `codegraph sync`并query provenance→successor delegate path。验证至少包含：

1. provenance targeted tests及successor targeted tests；每个 REV finding有先失败后受保护的行为断言；pretty policy
   positive fixture必须通过strict-noncanonical-input decoder，canonical-only decoder继续对该fixture fail closed；
2. focused集合：上述两test modules，加现有controller conformance/runtime/integration中直接依赖provenance primitive的
   synthetic tests；不得打开accepted external EQ payload；
3. compile/static/import、artifact state-machine replay、`git diff --check`、exact changed-path inventory；必须断言
   descriptor/public-summary/pending-terminal三个状态不越权，terminal-last且无rewrite，final/strict结果只在返回值/ER；
4. 证明release root acquisition/generation与real public/final/strict invocation均为0；所有device/formal side effect为0；
5. 证明三个巨型模块、config、GUIDE/RESEARCH/FULL/PLAN/archive相对activation未变。

本包 **禁止 full suite**。先前full suite确实只读accepted external EQ fixture，因此
`external_experiment_payload_access=0` 与 full suite不可同时成立。本包选择focused/affected且payload-free路径，
`full_suite_invocations=0`；不得把 `836/836`冒充本次repair后的full结果。后续若Orchestrator要求full suite，必须另行
显式授权该read-only fixture access并如实计数。

本包预计不超过10分钟；若预计超时，按visible Terminal/3次liveness规则回交，不得后台长占有。

## 6. 第三次失败 stop与handoff

无in-place correction budget。任一测试/静态复现失败、scope扩大、CodeGraph无法证明单一owner、或REV finding未闭合：

```text
REF-G4-01-SUCCESSOR-LINEAGE remains unfinished
same provenance/state boundary failure ordinal = 3
stop = RETURN_ORCHESTRATOR_NO_FURTHER_REPAIR
release/device/formal = locked
```

全部通过也只回Planner review并请求Orchestrator建立代码checkpoint；release acquisition/generation仍为0，后续仍由同一
reference的新PLAN冻结exact source/tree/root。Executer禁止stage/commit/amend/push，禁止修改PLAN/FULL。

维护性判断：该包把Git、directory identity与canonical persistence收回既有provenance owner，并压缩successor module
为composition/state machine；这是第二次也是最后一次允许的enabling seam修复，不做无关重构。
