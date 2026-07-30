# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2：helper-owned test correction

**计划状态：** `DISPATCHABLE_ONE_EXECUTER`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE`

**唯一当前动作：** 一个新的 Executer 先以 committed helper APIs 验证 activation lineage 与
PLAN/FULL owner；gate 全绿后，只修正 dedicated test 的静态 callee owner 判断，并在一个 fresh
external root 中运行一次 fail-fast validation chain。不得提交、stage、执行真实 controller，或读取
retained R3、candidate、release。

**C1 review archive：**
`.agent-work/PLANS/20260730-0330-p7-retained-r3-option-b-b1a-c3e6f19-corrective-1-review.md`；
SHA-256 `67eca7450faf11dfbf949279244357616b4fc964f93770ab602d33305d0e7026`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_2_activation_plan_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE","dispatch_state":"dispatchable_one_executer","single_current_action":"helper_gate_then_dedicated_test_only_correction_and_one_fail_fast_validation_chain","activation_commit":{"required_direct_parent":"5d6fa3d8e317a7f176c2849781bc47f3d97f3c25","exact_changed_paths":[".agent-work/PLAN.md"],"exact_subject":"chore(plan): activate f19 helper-owned correction","actual_child_owner":"runtime_git_rev_parse_HEAD_full_sha_after_orchestrator_commit","actual_child_requirements":{"full_40_char":true,"not_equal_parent":true,"clean_porcelain":true},"committed_plan_blob_owner":"runtime_git_rev_parse_HEAD_colon_plan_path","committed_plan_sha256_owner":"runtime_sha256_of_committed_plan_blob","self_referential_expected_child_or_plan_sha_forbidden":true},"frozen_full":{"path":".agent-work/FULL_PLAN_REFERENCE.md","sha256":"6932a0e9d6b0bf30e07afe3f4aadd8314ce26b43e167a2a3b20f849369147751","active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"execution_source_machine_marker_literal_count":0,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"656dbda9cf852e1a52affe5edd60148366f401bf","sha256":"579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647"}},"immutable_repo_evidence":{"execution_result":{"path":".agent-work/EXECUTION_RESULT.md","blob_oid":"90946b3053623069ba7100332605a21e0dc46ff7","sha256":"4eba2a8125361d2db9ef7a704880ac9ea1591bd128199a34403bf49a5eb6267f","allowed_change":"single_append_after_terminal_seal_only"},"c1_review_archive":{"path":".agent-work/PLANS/20260730-0330-p7-retained-r3-option-b-b1a-c3e6f19-corrective-1-review.md","blob_oid":"488d7af98d270aa2955c9500055d62ac05b84e75","sha256":"67eca7450faf11dfbf949279244357616b4fc964f93770ab602d33305d0e7026","preserve_byte_exact":true}},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py"],"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","fresh_evidence_root_absent_at_activation":true,"fresh_evidence_root_exclusive_create_mode":"0700","fresh_artifact_requirements":{"regular":true,"non_symlink":true,"exclusive_create":true,"mode":"0600","strict_json":true,"terminal_seal":true},"validation_chain":{"fail_fast":true,"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CORRECTIVE_2_TERMINAL_WAITING_PLANNER"}`

## 1. Activation lineage与helper gate

任何fresh-root、repo edit、旧证据读取或测试前，Executer必须完成全部gate；任一不符立即停止，
不得创建root、编辑、测试或append ER：

1. 工作区porcelain必须clean；actual HEAD必须是full 40-char child、不同于冻结parent，且其direct
   parent精确为`5d6fa3d8e317a7f176c2849781bc47f3d97f3c25`。
2. actual child的commit subject精确为`chore(plan): activate f19 helper-owned correction`，相对direct
   parent的changed-path set精确且仅为`.agent-work/PLAN.md`。
3. 从actual child读取committed PLAN blob；worktree PLAN bytes必须与该blob相等。actual child SHA、
   PLAN blob OID及committed PLAN SHA-256属于runtime evidence，不在PLAN中预填expected value，避免
   activation commit自引用。
4. FULL worktree bytes SHA-256必须精确为
   `6932a0e9d6b0bf30e07afe3f4aadd8314ce26b43e167a2a3b20f849369147751`，且等于actual child中的
   committed FULL blob；helper、controller和dedicated test必须匹配machine contract冻结的blob/SHA。
5. Execution source必须从committed
   `camera_based_rgbww_optimizer.utils.agent_work_machine_contract`直接import
   `parse_plan_machine_contract`与`parse_full_plan_machine_state`。PLAN committed bytes只传给前者一次，
   FULL committed bytes只传给后者一次。
6. 仅使用两个API各自返回的`value`和`evidence`验证candidate count/source SHA/owner，以及冻结的
   task、contract、retained状态和candidate-contract flag。API必须各调用恰好一次。
7. Execution source不得包含任何machine marker literal，不得实现独立line/split/regex/substring
   scanner、marker alias、fallback、inference或payload repair；也不得从一个owner借值给另一个owner。

本PLAN提交前验证到fresh root不存在；派发时必须再次确认仍不存在。存在即hard fail，不得复用、
覆盖、删除、修复或改走alternate root。

## 2. 唯一test-only修复

Gate全绿后，只允许编辑：

`tests/test_p7_retained_r3_exact_five_controller.py`

必须保持controller byte-exact，并以最小变更修复dedicated static regression的false positive：

1. AST检查分离`ast.Name` builtin/global callee与`ast.Attribute` method callee；继续禁止builtin
   `open`及attribute `read_text`、`read_bytes`、`write_text`、`write_bytes`、`unlink`、`mkdir`、
   `system`、`run`、`Popen`。
2. Bytecode检查分离global/name load与attribute/method load，不得把`LOAD_FAST run`误判为subprocess。
3. 显式证明允许的`Name("run")`定义和调用只属于
   `execute_prepared_exact_five_controller`的lexical nested local helper。
4. 保留forbidden-import、callback protocol与eligibility边界。禁止production rename、删除static
   regression、以generic string absence替代语义检查，或缩小direct-I/O边界。

实现完成后，worktree implementation diff path必须且仅为dedicated test；PLAN是已提交activation
path，不计入implementation diff。controller/helper/FULL/archive及所有其他repo path保持byte-exact。

## 3. Fresh evidence与一次fail-fast验证链

Gate全部通过后，才可exclusive-create machine contract所列fresh root，mode `0700`。所有artifact
必须regular/non-symlink、exclusive-create、mode `0600`；JSON必须strict parse且terminal seal不可变。

以下命令严格顺序、每项最多一次；任一nonzero立即seal，后续命令调用数保持`0`：

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

Terminal evidence必须记录activation actual child/parent/subject/path set、committed PLAN blob/SHA、
helper两次parse的独立evidence、FULL/task/contract/retained lock、before/after controller/test identity、
exact implementation diff path、fresh artifact manifest、每个command exit/count与所有zero budgets。

Seal后最多向`.agent-work/EXECUTION_RESULT.md` append一次；不得改写旧内容。PASS或FAIL都必须停在
Planner门，不得stage/commit或进入真实controller/B2。

## 4. Hard locks与停止点

- 禁止读取、stat或probe retained R3、candidate、release payload/path；禁止真实controller、canonical
  validator、eligibility、manifest consumer或release consumption。
- 禁止network、DNS、env/credential、device、camera、Ray、strip、cleanup、capture、FORMAL、public
  analyzer、TD-C、sentinel、P8、firmware或deployment。
- retry、fallback、reuse、rewrite、repair、alternate path均为`0`；旧F19 evidence和C1 archive保持不变。
- PASS仅证明test false positive已修复且一次validation链通过；不授权commit、R3读取、真实controller或B2。

**Planner stop：** `F19_CORRECTIVE_2_TERMINAL_WAITING_PLANNER`。

**维护性判断：** C2仅修改dedicated regression test，继续复用唯一committed machine-contract helper；
production controller、解析owner与科学合同均不新增分支。完整targeted/focused/full回归和CodeGraph用于
证明边界保持，验收前不建议额外重构。
