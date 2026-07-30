# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4：exact field-owner gate correction

**计划状态：** `DISPATCHABLE_ONE_EXECUTER_AFTER_ORCHESTRATOR_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER`

**唯一当前动作：** Orchestrator 以本 PLAN 冻结的 exact subject 提交唯一 PLAN path 后，派发一个新的
Executer。Executer必须先从 committed helper 直接调用 PLAN/FULL parse API 各一次，逐项验证本 PLAN
机器合同冻结的 exact owner/path/type/value；全部通过后仅修改 dedicated test 的 lexical-local `run`
`STORE_FAST`/`LOAD_FAST` 精确断言，再于唯一 fresh C4 root 运行一次完整 fail-fast validation chain。
不得执行真实 controller、读取 candidate/retained R3/release，或进入 B2。

**C3 review archive：**
`.agent-work/PLANS/20260729-2203-p7-retained-r3-option-b-b1a-c3e6f19-corrective-3-review.md`；
SHA-256 `95fbaf7c109d4a58214b0f8860f4f8b7ed367dbc20d8fdb15d2e67fcf2026b9c`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_4_field_owner_activation_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER","dispatch_state":"dispatchable_one_executer_after_orchestrator_commit","single_current_action":"exact_owner_gate_then_test_only_local_run_correction_then_one_fail_fast_validation_chain","activation_commit":{"required_direct_parent":"a647256cd49e477c73cf878101d5d6733d851dde","exact_changed_paths":[".agent-work/PLAN.md"],"exact_subject":"chore(plan): activate f19 exact field-owner correction","actual_child_owner":"runtime_git_rev_parse_HEAD_full_sha_after_orchestrator_commit","actual_child_requirements":{"full_40_char":true,"not_equal_parent":true,"clean_porcelain":true},"committed_plan":{"path":".agent-work/PLAN.md","blob_owner":"runtime_git_rev_parse_HEAD_colon_exact_plan_path","sha256_owner":"runtime_sha256_of_committed_plan_blob","worktree_must_equal_committed_blob":true},"self_referential_expected_child_blob_or_plan_sha_forbidden":true},"frozen_full":{"path":".agent-work/FULL_PLAN_REFERENCE.md","sha256":"e40337b5d9dc0af8b9c1f0bb03fcb100a4af9c3ef396d57f623a387a224715ae"},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"execution_source_machine_marker_literal_count":0,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0},"field_gate_ledger":[{"owner":"PLAN.value","path":["reference_task_id"],"type":"str","value":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4"},{"owner":"PLAN.value","path":["contract_id"],"type":"str","value":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER"},{"owner":"PLAN.value","path":["machine_contract_helper"],"type":"dict","value":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"execution_source_machine_marker_literal_count":0,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0}},{"owner":"PLAN.value","path":["operation_budgets"],"type":"dict","value":{"helper_edits":0,"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0}},{"owner":"PLAN.value","path":["execution_result_append_cap"],"type":"int","value":1},{"owner":"PLAN.value","path":["frozen_full"],"type":"dict","value":{"path":".agent-work/FULL_PLAN_REFERENCE.md","sha256":"e40337b5d9dc0af8b9c1f0bb03fcb100a4af9c3ef396d57f623a387a224715ae"}},{"owner":"FULL.value","path":["active_task_count"],"type":"int","value":1},{"owner":"FULL.value","path":["active_task"],"type":"str","value":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4"},{"owner":"FULL.value","path":["active_plan_contract_id"],"type":"str","value":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER"},{"owner":"FULL.value","path":["retained_r3_status"],"type":"str","value":"RETAINED_UNVALIDATED_UNCONSUMED"},{"owner":"FULL.value","path":["candidate_machine_contract_sha256"],"type":"str","value":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225"},{"owner":"FULL.value","path":["candidate_contract_orchestrator_verified"],"type":"bool","value":true}],"field_gate_rules":{"exact_key_membership_before_index":true,"exact_builtin_type_identity":true,"exact_value_compare_after_type":true,"full_fields_actual_owner":"FULL.value_top_level_only","plan_expected_owner":"PLAN.value.field_gate_ledger_only","helper_evidence_actual_owner":"PLAN.evidence_or_FULL.evidence_only","unlisted_nested_alias_get_default_fallback_inference_cross_owner_forbidden":true,"candidate_payload_recompute_or_read_forbidden":true},"helper_evidence_gate":{"plan":{"owner":"PLAN.evidence","expected_owner":"PLAN","candidate_count":1,"source_sha256_owner":"runtime_committed_PLAN_raw_sha256"},"full":{"owner":"FULL.evidence","expected_owner":"FULL","candidate_count":1,"source_sha256":"e40337b5d9dc0af8b9c1f0bb03fcb100a4af9c3ef396d57f623a387a224715ae"}},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"3cff60484e70db003409268f3365d7275dd53ab5","sha256":"e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6"}},"immutable_repo_evidence":{"execution_result":{"path":".agent-work/EXECUTION_RESULT.md","blob_oid":"4305982cd405904aa18edf4867d56916fe7e65f9","sha256":"9ad496d0e3a2c83cc9acd22afa6e7e3feab0a1615675161e657cae14144143e7","allowed_change":"single_append_after_terminal_seal_only"},"c3_review_archive":{"path":".agent-work/PLANS/20260729-2203-p7-retained-r3-option-b-b1a-c3e6f19-corrective-3-review.md","blob_oid":"2df795b0b5f0835f2fe540bf7d32c6ff4159a5d2","sha256":"95fbaf7c109d4a58214b0f8860f4f8b7ed367dbc20d8fdb15d2e67fcf2026b9c","preserve_byte_exact":true}},"immutable_c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","root_mode":"0700","artifacts":{"activation-gate.json":"cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c","pre-validation.json":"16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2","compileall.log":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","targeted_unittest.log":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48","terminal-evidence.json":"41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6"},"artifact_count":5,"artifact_mode":"0600","preserve_before_after_byte_exact":true,"repair_rewrite_delete_count":0},"forbidden_c3_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-3-offline","absence_owner":"accepted_C3_review_archive_at_review_time","current_probe_count":0,"create_reuse_read_probe_count":0},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py"],"exact_test_correction":{"lexical_owner":"execute_prepared_exact_five_controller","name_argval":"run","allowed_owner_opcodes":[["execute_prepared_exact_five_controller","STORE_FAST"],["execute_prepared_exact_five_controller","LOAD_FAST"]],"forbidden_opcodes":["LOAD_GLOBAL","LOAD_NAME","LOAD_ATTR","LOAD_METHOD"],"other_owner_or_opcode_allowed":false,"preserve_ast_lexical_owner_proof":true,"preserve_forbidden_import_direct_io_attribute_method_and_eligibility_boundaries":true,"generic_allowlist_string_absence_production_rename_or_regression_removal_forbidden":true},"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-4-offline","fresh_evidence_root_absent_at_activation":true,"fresh_evidence_root_exclusive_create_mode":"0700","fresh_artifacts":["activation-gate.json","pre-validation.json","compileall.log","targeted_unittest.log","focused_unittest.log","full_unittest.log","codegraph-sync.log","git-diff-check.log","terminal-evidence.json"],"fresh_artifact_requirements":{"regular":true,"non_symlink":true,"exclusive_create":true,"mode":"0600","json_strict_when_json":true,"terminal_seal_immutable":true},"validation_chain":{"fail_fast":true,"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0,"fallback":0},"operation_budgets":{"helper_edits":0,"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"terminal_required_on_pass_or_fail":true,"planner_stop":"F19_CORRECTIVE_4_TERMINAL_WAITING_PLANNER"}`

## 1. Activation lineage 与 committed-helper gate

Orchestrator提交本PLAN前不得dispatch。提交后的一个新Executer必须在任何external path operation、repo edit或
validation command之前完成以下全部gate；任一不符立即向ER最多append一次精确FAIL并停，path operation、
edit与command调用保持`0`：

1. `git status --porcelain=v1`为空；runtime HEAD为40-char child、不同于冻结parent，且direct parent精确为
   `a647256cd49e477c73cf878101d5d6733d851dde`。
2. actual child commit subject精确为`chore(plan): activate f19 exact field-owner correction`；相对parent的
   changed-path set精确且仅为`.agent-work/PLAN.md`。
3. 从actual child读取exact path `.agent-work/PLAN.md` committed blob；worktree PLAN bytes必须完全相同。
   actual child、PLAN blob OID与committed PLAN SHA-256是runtime child evidence，不在PLAN中预填，禁止自引用。
4. FULL worktree bytes及actual child committed FULL blob必须相等，raw SHA-256精确为
   `e40337b5d9dc0af8b9c1f0bb03fcb100a4af9c3ef396d57f623a387a224715ae`。helper、controller、test、
   C3 archive与ER committed identity必须匹配machine contract。
5. Execution source必须从committed
   `camera_based_rgbww_optimizer.utils.agent_work_machine_contract`直接import
   `parse_plan_machine_contract`与`parse_full_plan_machine_state`，各API恰好调用一次，且分别只接收committed
   PLAN bytes与committed FULL bytes；禁止execution source重现marker、scanner或JSON parser。
6. 对每个`field_gate_ledger` entry，必须先验证exact key membership，随后以`type(actual) is expected_type`
   验证exact builtin type，最后比较exact value。禁止`.get()`、未列键、nested candidate object、alias、default、
   fallback、inference、payload repair或PLAN/FULL cross-owner借值。
7. FULL candidate identity只能读取顶层
   `FULL.value["candidate_machine_contract_sha256"]: str`，verified只能读取相邻顶层
   `FULL.value["candidate_contract_orchestrator_verified"]: bool`。禁止读取不存在的`candidate_contract`，也禁止
   candidate payload read/recompute。
8. Helper evidence只能分别读取`PLAN.evidence`与`FULL.evidence`；owner须为`PLAN`/`FULL`，candidate count须各
   为`1`，source SHA须分别等于runtime committed PLAN raw SHA和冻结FULL SHA。domain value与evidence不得
   cross-owner。

Helper/field gate通过后，只读验证C2 root及五个artifact的regular/non-symlink/mode/bytes/SHA；C2是唯一可读
旧external evidence。C3 root不得create/reuse/read/stat/probe。fresh C4 root必须仍absent；不符即hard fail，
不得复用、覆盖、删除、修复、重写或换alternate root。

## 2. 唯一 test-only correction

全部gate通过后，只允许编辑：

`tests/test_p7_retained_r3_exact_five_controller.py`

从冻结test blob/SHA开始作最小语义修正：

1. 对所有bytecode `argval == "run"`，允许集合必须精确等于
   `{("execute_prepared_exact_five_controller", "STORE_FAST"),
   ("execute_prepared_exact_five_controller", "LOAD_FAST")}`；任何其他lexical owner或opcode均拒绝。
2. `LOAD_GLOBAL run`、`LOAD_NAME run`、`LOAD_ATTR run`、`LOAD_METHOD run`继续分别拒绝；不得使用generic
   name/path/callee allowlist或字符串缺失替代owner/opcode语义检查。
3. AST必须继续证明唯一`def run`直接嵌套于`execute_prepared_exact_five_controller`，全部
   `Name("run")` call的lexical owner就是该execute函数。
4. C2既有forbidden imports、builtin/global callee、attribute/method callee、direct I/O、callback protocol与
   eligibility边界不得缩小；不得rename production、删除static regression或修改controller/helper。

实现后implementation diff path精确且仅为dedicated test。controller/helper/FULL/PLAN/archive及其他repo path
保持committed bytes；PLAN activation commit不属于implementation diff。

## 3. Fresh C4 evidence 与唯一 fail-fast validation chain

实现完成后才可exclusive-create frozen fresh C4 root，mode `0700`。machine contract所列artifact按阶段
exclusive-create；均须regular/non-symlink/mode `0600`，JSON strict parse，terminal seal形成后不可改变。

以下命令严格按顺序、每项最多一次；任一nonzero立即记录并seal，后续调用数保持`0`：

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

Terminal evidence必须记录actual child/parent/subject/path set、committed PLAN blob/SHA、helper direct parse
counts/evidence、逐字段owner/path/type/value结果、FULL/task/contract/retained/candidate digest/verified locks、
controller/test before/after blob与SHA、exact implementation diff、C2 before/after identity、C3 zero access、
fresh artifact manifest、各command exit/count、retry/fallback、ER append count及全部zero budgets。
PASS/FAIL均terminal seal；seal后最多向`.agent-work/EXECUTION_RESULT.md` append一次，只能append旧内容。
不得stage/commit；停在Planner门，不得进入真实controller或B2。

## 4. Hard locks 与停止点

- 禁止读取、stat或probe candidate、retained R3、release path/payload；C2 evidence是唯一允许读取的旧external
  evidence，C3 root禁止任何访问。
- 禁止真实controller、canonical validator、eligibility emission、manifest writer/consumer、release
  qualification/generation/copy/consumption。
- 禁止network、DNS、`.env`/credential、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
  TD-C、sentinel、P8、firmware及deployment。
- retry、fallback、reuse、rewrite、repair与alternate path均为`0`。PASS只证明field-owner gate、dedicated
  static-test修正与完整离线validation chain通过，不授权commit、R3、release、controller或B2。
- 本包纯engineering/provenance/test纠偏，不需要Advisor；无高危设备操作，不需要Human授权。

**Planner stop：** `F19_CORRECTIVE_4_TERMINAL_WAITING_PLANNER`。

**维护性判断：** 本包只把既有committed helper返回值的field owner/path/type/value逐项机器化，并修正
dedicated regression的Python local-binding字节码语义；不新增parser、scanner、production owner或execution
framework。controller与eligibility边界不变，完整targeted/focused/full/CodeGraph验证保持。
