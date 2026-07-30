# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1：dedicated static-test owner correction

**计划状态：** `PLANNER_CORRECTIVE_DRAFT_WAITING_ORCHESTRATOR_FULL_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST`

**唯一动作：** 仅修正 dedicated static regression 对局部 `run` callback helper
的误判，然后在 fresh evidence root 中按 fail-fast 顺序完成一次冻结验证链并停止。

**Dispatch lock：** `LOCKED_PENDING_ORCHESTRATOR_FULL_UPDATE_AND_FRESH_PLANNER_ACTIVATION`。
本草案不授权 Executer；Orchestrator 必须先审查 F19 rejection、更新
`FULL_PLAN_REFERENCE.md`、整理并提交当前 reviewed state，再由新的 Planner
activation pass 将实际 FULL SHA、dispatch HEAD/parent/changed paths 与 clean
porcelain 冻结进可执行 PLAN。未完成该 activation 时，任何 edit、test、evidence
root 创建或 ER append 均为 `0`。

**F19 failure review archive：**
`.agent-work/PLANS/20260730-0315-p7-retained-r3-option-b-b1a-c3e6f19-failure-review.md`；
SHA-256 `b10e05fdf141c5864edf2eadcfa5022a7e92293bd573c51faf2c609bcad522de`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_1_planner_draft_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST","dispatch_lock":"locked_pending_orchestrator_full_update_and_fresh_planner_activation","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F19","single_current_action":"test_only_static_callee_owner_correction_then_one_fail_fast_validation_chain_and_planner_stop","review_archive":{"path":".agent-work/PLANS/20260730-0315-p7-retained-r3-option-b-b1a-c3e6f19-failure-review.md","sha256":"b10e05fdf141c5864edf2eadcfa5022a7e92293bd573c51faf2c609bcad522de"},"frozen_failed_inputs":{"dispatch_head":"1b38baa28e80c164656215500657031608c9692c","dispatch_parent":"2457844a5f0f1c9c279348dd4d5b5e2c5b4f393b","reviewed_plan_sha256":"a641fce40be077fb50bb47d69e1ba8dc17e8d6077a000bb1f47f3f60f68fb45b","reviewed_full_sha256":"05d9d3458d71a176ffd197aeb46fdf812a7b34e226ee62fc3aa5094d67f6adc6","controller_source_sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","dedicated_test_before_sha256":"579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647","failed_terminal_sha256":"7ec1b83244b5b6ee6119baaeb0feb1bff12bbfff38e9af68411017bd28560e46"},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py"],"old_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-preparation-offline","old_evidence_immutable":true,"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-1-offline","fresh_evidence_root_required_absent_at_activation":true,"test_correction_contract":{"separate_ast_name_and_attribute_callees":true,"builtin_open_name_still_prohibited":true,"filesystem_and_subprocess_attributes_still_prohibited":["read_text","read_bytes","write_text","write_bytes","unlink","mkdir","system","run","Popen"],"bytecode_global_and_attribute_opcodes_classified_separately":true,"load_fast_run_not_subprocess":true,"nested_local_run_owner_explicitly_asserted":true,"generic_string_absence_check_forbidden":true,"production_rename_forbidden":true},"test_budgets_after_activation":{"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"controller_calls":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"execution_result_append_cap_after_activation":1,"planner_stop":"F19_CORRECTIVE_1_TERMINAL_WAITING_PLANNER"}`

## 1. Correction owner and exact scope

F19 controller source保持byte-exact不变：

`src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py`

冻结SHA-256：
`746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`。

唯一允许编辑：

`tests/test_p7_retained_r3_exact_five_controller.py`

其失败baseline SHA-256为：
`579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647`。

不允许修改任何 production source、helper、其他test、doc、skill、wrapper、
PLAN、FULL、archive或GUIDE。不得通过production rename迁就误报，也不得删除
static regression、缩小其direct-I/O边界或仅断言字符串不存在。

Dedicated test必须将以下owner分开：

1. `ast.Name` direct builtin/global calls：继续禁止builtin `open`；
2. `ast.Attribute` method calls：继续禁止 `read_text`、`read_bytes`、
   `write_text`、`write_bytes`、`unlink`、`mkdir`、`system`、`run`、`Popen`；
3. bytecode只把global/name load与attribute/method load按相应owner判定，
   不得把`LOAD_FAST run`当作subprocess；
4. 明确验证被接受的`Name("run")`定义和调用均位于
   `execute_prepared_exact_five_controller`的lexically nested local helper边界；
5. forbidden import集合与callback protocol/eligibility边界断言必须原样保留。

## 2. Activation and preservation gates

Fresh Planner activation必须在dispatch前重新冻结：

- Orchestrator-updated FULL raw SHA、active task/contract、active count `1`、
  `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`及candidate verified flag；
- 实际dispatch HEAD、direct parent、subject、exact changed-path set；
- HEAD blob PLAN与worktree PLAN bytes一致及clean porcelain；
- controller source与failed-test baseline identities；
- old F19 evidence root五个artifact path/bytes/SHA均未改变；
- fresh corrective root仍absent。

任一gate失败：不得创建fresh root、不得编辑test、不得运行command，仅append一次
truthful pre-root FAIL（若activation PLAN明确授权）并Planner stop；retry/fallback为0。

## 3. Fresh validation chain

Activation后，Executer只可建立一次fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-1-offline`

root必须exclusive-create、mode `0700`；artifact必须regular/non-symlink、mode
`0600`、不可覆盖。建议使用与F19相同的progressive布局：dispatch/identity、
targeted、focused、full、CodeGraph、validation summary与terminal summary。

验证命令均最多一次，前一项nonzero立即停止，后续为0：

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

Terminal必须绑定before/after source/test bytes与SHA、exact diff path、activation
lineage、PLAN/FULL/archive/old-evidence identities、所有command exit/test counts、
fresh artifact identity及全部zero locks。Executer只可向
`.agent-work/EXECUTION_RESULT.md` append一次，不得stage或commit。

## 4. Hard locks and branch

- old F19 evidence只读且immutable；不得reuse、repair、rewrite或delete。
- 禁止读取或stat retained R3、candidate、release payload/path。
- 禁止真实controller、manifest、canonical validator、eligibility、consumer或release。
- 禁止network、DNS、env/credential、device、camera、Ray、strip、cleanup、capture、
  FORMAL、public analyzer、TD-C、sentinel、P8、firmware或deployment。
- PASS只说明test false positive已纠正且controller preparation validation chain通过；
  不自动commit、不进入真实F19 controller execution或B2。
- FAIL保留fresh evidence并停止；retry、fallback、alternate path均为0。

**Planner stop：** `F19_CORRECTIVE_1_DRAFT_WAITING_ORCHESTRATOR_FULL_ACTIVATION`。

**维护性判断：** 纠偏仅修复dedicated static test的callee-owner分类，不改变
controller状态机、callback API或eligibility边界；保持一source一test的清晰owner，
无需新增抽象或production重构。
