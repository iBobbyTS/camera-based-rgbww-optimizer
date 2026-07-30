# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2：helper-owned activation gate

**计划状态：** `NOT_DISPATCHABLE_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_PLANNER_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE`

**唯一当前动作：** Orchestrator先将FULL唯一active task/contract对齐至本C2；随后一个独立
Planner activation pass冻结aligned FULL raw SHA、activation parent/subject/path set，并将本包改为
dispatchable。当前不得dispatch Executer、创建root、编辑test、运行测试或append ER。

**C1 review archive：**
`.agent-work/PLANS/20260730-0330-p7-retained-r3-option-b-b1a-c3e6f19-corrective-1-review.md`；
SHA-256 `67eca7450faf11dfbf949279244357616b4fc964f93770ab602d33305d0e7026`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_2_pre_activation_plan_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE","dispatch_state":"not_dispatchable_waiting_orchestrator_full_alignment_and_planner_activation","single_current_action":"orchestrator_align_full_then_planner_freeze_exact_activation_lineage_and_full_sha","required_full_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true},"full_raw_sha256_owner":"next_planner_activation_after_orchestrator_alignment","activation_lineage_owner":"next_planner_activation_after_orchestrator_alignment","machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_marker_owner":"PLAN_MACHINE_MARKER","full_marker_owner":"FULL_PLAN_MACHINE_MARKER","direct_api_calls_required":true,"handwritten_marker_or_scanner_forbidden":true,"alias_inference_fallback_or_payload_repair_forbidden":true},"review_archive":{"path":".agent-work/PLANS/20260730-0330-p7-retained-r3-option-b-b1a-c3e6f19-corrective-1-review.md","sha256":"67eca7450faf11dfbf949279244357616b4fc964f93770ab602d33305d0e7026"},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726"},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"656dbda9cf852e1a52affe5edd60148366f401bf","sha256":"579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647"}},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py"],"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-1-offline","fresh_evidence_root_required_absent_at_dispatch":true,"validation_chain":{"fail_fast":true,"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"test_file_edits":1,"controller_calls":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CORRECTIVE_2_TERMINAL_WAITING_PLANNER"}`

## 1. Orchestrator alignment与下一Planner activation（当前唯一可执行步骤）

1. Orchestrator只更新其拥有的FULL，使唯一active task为本C2、contract ID精确匹配，并保持
   `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、
   `candidate_contract_orchestrator_verified=true`和B2 locked。
2. Orchestrator提交FULL整理后，必须交一个新的Planner activation pass；该pass只允许更新PLAN，冻结：
   aligned FULL raw SHA、activation direct parent、exact subject、exact changed-path set、committed PLAN
   blob/runtime owner与clean porcelain SHA。
3. 在上述activation完成并提交前，本PLAN是non-dispatchable；Executer调用预算为`0`。

## 2. 冻结的helper-owned activation gate

下一activation版本必须规定：在任何fresh-root、repo edit、archive/旧证据检查或测试前，Executer：

1. 从committed source直接import：
   `parse_plan_machine_contract`与`parse_full_plan_machine_state`；
2. 将PLAN原始`bytes`只传给前者，将FULL原始`bytes`只传给后者；
3. 使用两个API返回的`value`和`evidence`验证candidate count、owner、source SHA、task、contract、
   retained状态与candidate contract；
4. 不得在execution source中手写`PLAN_MACHINE_CONTRACT`、`PLAN_MACHINE_STATE`或
   `FULL_PLAN_MACHINE_STATE` marker，不得使用独立`splitlines`/regex/substring scanner、marker alias、
   fallback、inference或payload repair；
5. helper import、blob/SHA、API返回值或activation lineage任一不符时，在path operation前停止；不得
   创建root、编辑、运行测试或append ER。

该规则修复C1的唯一根因：Executer错误查找不存在的`PLAN_MACHINE_STATE`。Canonical owners始终为
PLAN=`PLAN_MACHINE_CONTRACT`、FULL=`FULL_PLAN_MACHINE_STATE`，但execution不得再次人工转录它们。

## 3. activation成功后唯一实现动作

唯一允许编辑：

`tests/test_p7_retained_r3_exact_five_controller.py`

保持controller byte-exact。Dedicated static regression必须：

1. 分离`ast.Name`与`ast.Attribute` callee；继续禁止builtin `open`及attribute `read_text`、
   `read_bytes`、`write_text`、`write_bytes`、`unlink`、`mkdir`、`system`、`run`、`Popen`；
2. 分离bytecode global/name load与attribute/method load，不把`LOAD_FAST run`当作subprocess；
3. 显式证明允许的`Name("run")`定义/调用只属于
   `execute_prepared_exact_five_controller` lexical nested local helper；
4. 保留forbidden-import、callback protocol与eligibility边界；禁止production rename、删除static
   regression、generic string-absence替代或缩小direct-I/O边界。

exact worktree implementation diff path必须且仅为该test。

## 4. Fresh evidence与一次fail-fast验证链

activation gate全部通过后，才可exclusive-create一次machine contract所列fresh root，mode `0700`；
artifact必须regular/non-symlink、exclusive-create、mode `0600`。不得复用、覆盖或修复旧证据。

以下命令严格顺序、每项最多一次；任一nonzero立即seal并保持后续调用为0：

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

Terminal seal记录activation/helper parse evidence、before/after controller/test identity、exact diff path、
fresh artifact manifest、全部command exit/count与zero locks。Executer最多append ER一次，不得stage/commit。

## 5. Hard locks与停止点

- 禁止读取、stat或probe retained R3、candidate、release payload/path；禁止controller、canonical
  validator、eligibility、manifest consumer或release consumption。
- 禁止network、DNS、env/credential、device、camera、Ray、strip、cleanup、capture、FORMAL、public
  analyzer、TD-C、sentinel、P8、firmware或deployment。
- retry、fallback、alternate path均为`0`；旧F19 evidence immutable，不得reuse/repair/rewrite。
- PASS只证明test false positive修复和一次验证链通过；不授权commit、真实controller或B2。

**当前Planner stop：**
`F19_CORRECTIVE_2_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_PLANNER_ACTIVATION`。

**维护性判断：** C2不新增生产抽象；它强制复用已经提交并有11项回归覆盖的唯一machine-contract
helper，移除activation gate中的平行marker scanner。后续代码改动仍严格限制在dedicated test。
