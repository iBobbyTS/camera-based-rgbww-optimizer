# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1：dedicated static-test owner correction

**计划状态：** `READY_FOR_EXACT_ACTIVATION_COMMIT_THEN_CLEAN_EXECUTER_DISPATCH`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST`

**唯一动作：** 仅修正 dedicated static regression 对局部 `run` callback helper
的误判，然后在唯一 fresh evidence root 中按 fail-fast 顺序执行一次冻结验证链并停止。

**Dispatch verdict：** `READY_AFTER_EXACT_ACTIVATION_COMMIT_AND_CLEAN_PORCELAIN`。
Orchestrator必须先以当前HEAD为直接parent，使用下述exact subject提交且只提交本PLAN；
actual child SHA、PLAN blob OID、PLAN raw SHA及clean porcelain由dispatch runtime读取并冻结，
不写回本PLAN，从而避免自引用。提交合同不完全匹配时，Executer不得创建root、编辑、运行测试
或append ER；由Orchestrator纠正activation lineage后重新dispatch。

**F19 failure review archive：**
`.agent-work/PLANS/20260730-0315-p7-retained-r3-option-b-b1a-c3e6f19-failure-review.md`；
SHA-256 `b10e05fdf141c5864edf2eadcfa5022a7e92293bd573c51faf2c609bcad522de`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_1_active_plan_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST","dispatch_state":"ready_after_exact_activation_commit_and_clean_porcelain","single_current_action":"test_only_static_callee_owner_correction_then_one_fail_fast_validation_chain_and_planner_stop","full_contract":{"raw_sha256":"1125e0a0474f3e34f073c9b7c3639217a5ebe797a1be25e9c8b2efc192abae96","active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true},"activation_commit_contract":{"parent_sha":"784b0de8722d60af2a08a7346015de127540ffe2","exact_subject":"chore(plan): activate f19 static-test corrective","exact_changed_paths":[".agent-work/PLAN.md"],"actual_child_sha_owner":"dispatch_runtime_git_rev_parse_HEAD","actual_child_parent_owner":"dispatch_runtime_git_rev_parse_HEAD_parent","actual_plan_blob_oid_owner":"dispatch_runtime_git_ls_tree_HEAD","actual_plan_sha256_owner":"dispatch_runtime_raw_bytes","expected_clean_porcelain_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","self_reference_forbidden":true},"review_archive":{"path":".agent-work/PLANS/20260730-0315-p7-retained-r3-option-b-b1a-c3e6f19-failure-review.md","sha256":"b10e05fdf141c5864edf2eadcfa5022a7e92293bd573c51faf2c609bcad522de"},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726"},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"656dbda9cf852e1a52affe5edd60148366f401bf","sha256":"579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647"}},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py"],"old_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-preparation-offline","immutable":true,"artifacts":{"00-dispatch-and-bootstrap-replay.json":"b4f6557fbc7a3a8dc1718c472900ea4d24045a9da6373a62b984889d2a32ffaa","01-controller-source-identity.json":"3feba60353c1307a5809c86f1b2a1607574e27345109580632e120176b00cc00","02-targeted.log":"ea1c8715a6cf27c66e6ad038803b9af85331561fbd90e254ced492bd3ff82ba7","06-validation-summary.json":"8c1d2090611e3c08c8028384a2d766d96a373752798d695f31175fcb0979bcfe","07-terminal-summary.json":"7ec1b83244b5b6ee6119baaeb0feb1bff12bbfff38e9af68411017bd28560e46"}},"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-1-offline","fresh_evidence_root_required_absent_at_dispatch":true,"test_correction_contract":{"separate_ast_name_and_attribute_callees":true,"builtin_open_name_still_prohibited":true,"filesystem_and_subprocess_attributes_still_prohibited":["read_text","read_bytes","write_text","write_bytes","unlink","mkdir","system","run","Popen"],"bytecode_global_and_attribute_opcodes_classified_separately":true,"load_fast_run_not_subprocess":true,"nested_local_run_owner_explicitly_asserted":true,"generic_string_absence_check_forbidden":true,"production_rename_forbidden":true},"validation_chain":{"fail_fast":true,"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"test_file_edits":1,"controller_calls":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CORRECTIVE_1_TERMINAL_WAITING_PLANNER"}`

## 1. Activation gate（任何repo path operation之前）

Executer在任何fresh-root创建、repo编辑或测试命令前，必须只读验证：

1. 当前HEAD的直接parent为
   `784b0de8722d60af2a08a7346015de127540ffe2`；subject精确为
   `chore(plan): activate f19 static-test corrective`；该commit changed-path set精确且仅为
   `.agent-work/PLAN.md`。
2. runtime读取实际child SHA、PLAN blob OID和PLAN raw SHA；HEAD blob与worktree PLAN bytes一致，
   porcelain为空且其SHA-256为
   `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。
3. FULL raw SHA为
   `1125e0a0474f3e34f073c9b7c3639217a5ebe797a1be25e9c8b2efc192abae96`；其machine state严格为
   active count `1`、本task、本contract、
   `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、
   `candidate_contract_orchestrator_verified=true`。
4. committed controller blob/SHA分别为
   `45097745bcc48aa1312b06fc07c6c910a4529325` /
   `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`；
   committed test baseline blob/SHA分别为
   `656dbda9cf852e1a52affe5edd60148366f401bf` /
   `579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647`。
5. review archive及旧F19 root五项artifact的path、regular/non-symlink、bytes、mode `0600`
   与machine contract所列SHA均匹配；旧root mode为`0700`。
6. fresh corrective root仍不存在。

任一gate失败：不得创建fresh root、不得编辑test、不得执行任何验证命令，也不得append ER；
停止并向Planner/Orchestrator报告activation lineage contradiction。retry、fallback、alternate path均为0。

## 2. 唯一代码改动

唯一允许编辑：

`tests/test_p7_retained_r3_exact_five_controller.py`

必须保持controller source byte-exact不变。Dedicated test必须：

1. 分离`ast.Name` direct builtin/global call与`ast.Attribute` method call；继续禁止builtin `open`；
2. 继续禁止attribute `read_text`、`read_bytes`、`write_text`、`write_bytes`、`unlink`、
   `mkdir`、`system`、`run`、`Popen`；
3. bytecode按global/name load与attribute/method load分别分类，不把`LOAD_FAST run`视为subprocess；
4. 显式断言被接受的`Name("run")`定义及调用均位于
   `execute_prepared_exact_five_controller`的lexically nested local helper边界；
5. 原forbidden-import、callback protocol及eligibility边界断言保持；不得改production命名、删除static
   regression、改成generic string absence或缩小direct-I/O边界。

编辑后exact worktree diff path必须且仅为上述test；否则fail并进入terminal seal。

## 3. Fresh evidence与验证链

只允许exclusive-create一次：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-1-offline`

root必须mode `0700`；每个artifact必须exclusive-create、regular/non-symlink、mode `0600`、不可覆盖。
必须progressive持久化dispatch/identity、targeted、focused、full、CodeGraph、diff-check、validation summary
与terminal summary；每项绑定path、bytes、SHA-256、exit code、测试计数（若适用）及实际调用计数。

严格按以下顺序，每项最多一次，前一项nonzero立即停止且后续调用计数为0：

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

Terminal seal必须记录before/after controller/test bytes、SHA、blob身份、exact diff path、activation
lineage、PLAN/FULL/archive/旧证据身份、fresh artifact manifest、全部command exit/count与zero locks。
Executer只可向`.agent-work/EXECUTION_RESULT.md` append一次truthful terminal record，不得stage或commit。

## 4. Hard locks与终止分支

- old F19 evidence只读immutable；不得reuse、repair、rewrite、append或delete。
- 禁止读取、stat或probe retained R3、candidate及release payload/path。
- 禁止真实controller、manifest、canonical validator、eligibility、consumer或release。
- 禁止network、DNS、env/credential、device、camera、Ray、strip、cleanup、capture、FORMAL、
  public analyzer、TD-C、sentinel、P8、firmware或deployment。
- PASS仅表示static-test false positive已纠正且一次验证链通过；不授权commit、不进入真实F19 controller或B2。
- FAIL保留fresh evidence并停止；retry、fallback、alternate path均为0。

**Planner stop：** `F19_CORRECTIVE_1_TERMINAL_WAITING_PLANNER`。

**维护性判断：** 纠偏仅调整dedicated static test的callee-owner分类；controller状态机、callback API、
eligibility与provenance owner均不变。单一test owner和完整回归链足够，无需新增抽象或production重构。
