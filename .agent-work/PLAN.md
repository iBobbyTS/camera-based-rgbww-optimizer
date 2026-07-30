# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4：exact field-owner gate correction

**计划状态：** `WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_PLANNER_ACTIVATION`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER`

**唯一当前动作：** Orchestrator审查C3 rejection，把FULL唯一active task/contract/status对齐本C4并提交；之后
Planner重新读取committed PLAN/FULL/HEAD，冻结activation lineage、FULL SHA与每个gate字段的owner/path/type，
再把本包改为最多派发一个新Executer。当前版本不是execution authorization，不得dispatch。

**C3 review archive：**
`.agent-work/PLANS/20260729-2203-p7-retained-r3-option-b-b1a-c3e6f19-corrective-3-review.md`；
SHA-256 `95fbaf7c109d4a58214b0f8860f4f8b7ed367dbc20d8fdb15d2e67fcf2026b9c`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_4_field_owner_draft_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER","dispatch_state":"waiting_orchestrator_full_alignment_and_planner_activation","single_current_action":"orchestrator_align_full_then_planner_freeze_activation_and_exact_field_owners","review_archive":{"path":".agent-work/PLANS/20260729-2203-p7-retained-r3-option-b-b1a-c3e6f19-corrective-3-review.md","sha256":"95fbaf7c109d4a58214b0f8860f4f8b7ed367dbc20d8fdb15d2e67fcf2026b9c"},"expected_full_alignment":{"active_task_count":{"owner":"FULL.value","path":["active_task_count"],"type":"int","value":1},"active_task":{"owner":"FULL.value","path":["active_task"],"type":"str","value":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4"},"active_plan_contract_id":{"owner":"FULL.value","path":["active_plan_contract_id"],"type":"str","value":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER"},"retained_r3_status":{"owner":"FULL.value","path":["retained_r3_status"],"type":"str","value":"RETAINED_UNVALIDATED_UNCONSUMED"},"candidate_machine_contract_sha256":{"owner":"FULL.value","path":["candidate_machine_contract_sha256"],"type":"str","value":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225"},"candidate_contract_orchestrator_verified":{"owner":"FULL.value","path":["candidate_contract_orchestrator_verified"],"type":"bool","value":true}},"forbidden_field_assumptions":["FULL.value.candidate_contract","PLAN.value.frozen_full.candidate_contract","PLAN.value.frozen_full.candidate_machine_contract_sha256","nested_candidate_object","alias","fallback","inference","payload_repair","cross_owner_borrow"],"activation_requirements":{"orchestrator_full_alignment_commit_required":true,"planner_activation_pass_required":true,"dispatch_before_both":false,"actual_child_parent_subject_changed_paths_plan_blob_plan_sha_full_blob_full_sha_to_be_frozen_by_activation_planner":true},"preserved_goal":{"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"controller_preserve_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","exact_local_run_owner_pairs":[["execute_prepared_exact_five_controller","STORE_FAST"],["execute_prepared_exact_five_controller","LOAD_FAST"]],"full_fresh_validation_chain":true,"retry":0,"fallback":0},"operation_budgets":{"helper_edits":0,"controller_source_edits":0,"test_file_edits":1,"controller_calls":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CORRECTIVE_4_WAITING_ORCHESTRATOR_FULL_ALIGNMENT"}`

## 1. C3 rejection与C4边界

C3在helper parse API各调用一次后，错误读取不存在的`FULL.value["candidate_contract"]`而pre-edit停止。
Planner已独立确认committed helper只返回`ParsedMachineContract(value=dict, evidence=MachineContractEvidence)`；helper
不会创建candidate nested object，也不会解释domain field。C4只纠正execution gate的field owner绑定，不修改helper、
controller、candidate、R3或科学合同。

C3的fail-closed结果接受：ER append `1`；fresh C3 root、artifact、C2 access、repo edit、test、controller、
validator、release、network和device operation均为`0`。C3本身不接受为test correction完成。

## 2. Orchestrator FULL alignment gate

Orchestrator必须先把FULL machine state与正文唯一active task对齐C4，并明确记录C3 rejection。FULL machine row必须
保持唯一，至少包含以下精确顶层字段：

| Owner | JSON path | Exact type | Required value |
| --- | --- | --- | --- |
| `FULL.value` | `active_task_count` | `int`（不得是`bool`） | `1` |
| `FULL.value` | `active_task` | `str` | `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4` |
| `FULL.value` | `active_plan_contract_id` | `str` | `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER` |
| `FULL.value` | `retained_r3_status` | `str` | `RETAINED_UNVALIDATED_UNCONSUMED` |
| `FULL.value` | `candidate_machine_contract_sha256` | `str` | `3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225` |
| `FULL.value` | `candidate_contract_orchestrator_verified` | `bool` | `true` |

`candidate_contract`不是FULL或PLAN已定义字段，禁止创建它来适配失败执行源。candidate identity digest只从
`FULL.value["candidate_machine_contract_sha256"]`读取；verified flag只从相邻顶层bool读取。不得读取candidate
payload来重算、证明或修复该digest。

FULL对齐后必须由Planner另行activation review；当前PLAN不得直接dispatch。

## 3. Planner activation必须冻结的逐字段owner合同

activation Planner必须从committed helper直接import两API；对committed PLAN bytes与committed FULL bytes各调用
一次且只调用一次。随后把下列每项写入activation machine contract，Executer只能逐项消费：

### PLAN parse owner

- `PLAN.value["reference_task_id"]: str`
- `PLAN.value["contract_id"]: str`
- `PLAN.value["machine_contract_helper"]: dict`
- `PLAN.value["operation_budgets"]: dict`
- `PLAN.value["execution_result_append_cap"]: int`（不得是`bool`）
- activation版新增的`PLAN.value["frozen_full"]: dict`，其中只能拥有FULL path/SHA以及需比较的exact field
  ledger；它是expected-value owner，不是actual FULL owner。

### FULL parse owner

- 上表六个顶层field逐项以exact path/name/type/value验证。
- helper evidence只从`FULL.evidence`读取：`owner == "FULL"`、candidate count `1`、source SHA等于冻结FULL
  raw SHA；不得把domain fields误读为evidence fields。

### 禁止语义

- 不得读取任何未在ledger列出的candidate key；
- 不得假设nested object、别名、默认值、optional fallback、跨PLAN/FULL借值或根据字段名推断路径；
- 不得用`.get()`把missing/type mismatch降级；每项应先验证exact key set membership与`type(value) is ...`，再比较值；
- 禁止独立marker scanner、regex、substring、payload repair或直接JSON重解析。

任一field missing、extra assumption、type/value mismatch必须在external path operation之前向ER最多append一次FAIL并停。

## 4. 激活后唯一test-only correction

只有全部activation/field-owner/C2 identity gate通过后，才允许从committed dedicated test
`3cff60484e70db003409268f3365d7275dd53ab5` / SHA-256
`e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6`作一次最小编辑：

- 所有bytecode `argval == "run"`的owner/opcode集合必须精确等于
  `{("execute_prepared_exact_five_controller", "STORE_FAST"),
  ("execute_prepared_exact_five_controller", "LOAD_FAST")}`；
- `LOAD_GLOBAL`、`LOAD_NAME`、`LOAD_ATTR`、`LOAD_METHOD run`继续分别拒绝；
- AST继续证明唯一`def run`直接嵌套于`execute_prepared_exact_five_controller`，全部`Name("run")` call的
  lexical owner就是该execute函数；
- forbidden imports、builtin/global/attribute/method callee、direct I/O、callback protocol、eligibility边界不得缩小；
- 禁止generic allowlist、字符串缺失替代、production rename、删除regression或修改controller/helper。

controller保持blob `45097745bcc48aa1312b06fc07c6c910a4529325`、SHA-256
`746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`。

## 5. Fresh C4 evidence与完整validation chain

activation Planner必须冻结一个与C2/C3不同、且activation时absent的C4 root。C2是唯一允许只读的旧external
evidence；C3 root不得创建、复用、读取或probe。C4 root exclusive-create mode `0700`，stage artifact
exclusive-create、regular/non-symlink/mode `0600`，JSON strict，terminal seal immutable。

实现后按顺序各一次、fail-fast、retry/fallback `0`：

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q \
  src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py \
  tests/test_p7_retained_r3_exact_five_controller.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v \
  tests.test_p7_retained_r3_exact_five_controller

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v \
  tests.test_agent_work_machine_contract \
  tests.test_p7_retained_r3_exact_five_controller \
  tests.test_p7_retained_release_audit

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v

codegraph sync

git diff --check
```

PASS/FAIL均terminal seal并向ER最多append一次，然后停在Planner门；不得stage/commit或进入真实controller/B2。

## 6. Hard locks与当前停止点

- candidate、retained R3、release path/payload禁止stat/probe/read；C2 evidence以外旧external root禁止访问。
- 禁止真实controller、canonical validator、eligibility、manifest generation/consumption、release qualification/
  generation/copy/consumption。
- 禁止network、DNS、env/credential、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
  TD-C、sentinel、P8、firmware及deployment。
- 以上全是engineering/provenance field-owner纠偏，不需要Advisor；当前无高危设备操作，不需要Human授权。

**Planner stop：** `F19_CORRECTIVE_4_WAITING_ORCHESTRATOR_FULL_ALIGNMENT`。

**维护性判断：** C4只冻结既有helper API的field owner/path/type，不新增scanner、parser或production owner；
test-only目标与完整回归链保留，未提高controller或eligibility复杂度。
