# REF-G4-04-E2：fresh output-root binding enabling unit

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FRESH_ROOT_BINDING_ENABLING_ONLY`

**Executable after activation：** `true`

**Active task count after activation：** `1`

**Active task after activation：** `REF-G4-04-E2`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-E2-FRESH-ROOT-BINDING-ENABLING-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FRESH_ROOT_BINDING_ENABLING_ONLY","executable":true,"active_task_count":1,"active_task":"REF-G4-04-E2","reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_FRESH_ROOT_BINDING_ENGINEERING_ONLY","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"ce4eaab9e06bdb1c6092b2ab104b7f2931a7fb44","expected_parent_tree":"e1682006013ec148435a16515cb3688823bfd3f8","expected_subject":"docs(plan): activate e2 fresh root binding","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"execution_authorized_before_activation":false,"single_current_action":"replace_rejected_fixed_e2_output_root_default_with_explicit_validated_fresh_root_binding_and_cross_root_replay_protection","allowed_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","tests/test_p7_successor_e2.py"],"existing_production_files_edited":1,"existing_test_files_edited":1,"new_production_modules":0,"new_test_files":0,"giant_p7_module_edits":0,"config_edits":0,"wrapper_edits":0,"full_edits_by_executer":0,"plan_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"corrective_suffixes":0,"new_task_ids":0,"source_checkpoint":"ce4eaab9e06bdb1c6092b2ab104b7f2931a7fb44","source_tree":"e1682006013ec148435a16515cb3688823bfd3f8","guide":{"path":"advisor/4/4.GUIDE.md","sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35"},"source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":25075,"sha256":"c986255dc341b9ffdc54efff5e1cbb1d2c05b9fdd141fb0e660ad20c8c771bbf"},"tests":{"path":"tests/test_p7_successor_e2.py","bytes":32097,"sha256":"5b3f250dbbfab1914b3faaebabd32ac1b0c74dc3ea5c399cdaa4a553aabdcb32"},"current_fixed_rejected_root":"/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-4995f7d65141-20260803T204648Z","current_fixed_rejected_root_is_default":true,"current_fixed_rejected_root_access_allowed":false,"root_parent":"/Volumes/4T/temp/rgbww-optimizer","root_basename_regex":"^g4-e2-preformal-[0-9a-f]{12}-[0-9]{8}T[0-9]{6}Z$","root_direct_child_required":true,"root_canonical_lexical_required":true,"root_utc_timestamp_roundtrip_required":true,"frozen_e2_input_public_parameters":["output_root"],"frozen_e2_input_output_root_keyword_only":true,"frozen_e2_input_output_root_default_allowed":false,"result_reference_ledger_output_root_required":true,"replay_actual_root_expected_input_binding_required":true,"cross_root_transplant_rejection_required":true,"runtime_global_mutation_allowed":false,"root_selection_mock_patch_allowed":false,"handwritten_controller_allowed":false,"persist_semantic_injection_allowed":false,"persist_replay_injection_allowed":false,"replay_semantic_injection_allowed":false,"durable_e2_package_generation_allowed":false,"production_evaluation_cap":0,"production_persist_cap":0,"production_replay_cap":0,"new_durable_e2_root_allowed":false,"unit_test_exact_direct_child_root_fixture_allowed":true,"unit_test_fixture_root_concurrent_cap":2,"unit_test_fixture_root_per_case_cap":2,"unit_test_fixture_root_must_be_absent":true,"unit_test_fixture_nonce_from_legal_hex_timestamp":true,"unit_test_fixture_context_owned_identity_required":true,"unit_test_fixture_exact_cleanup_required":true,"unit_test_fixture_cleanup_wide_glob_allowed":false,"unit_test_fixture_cleanup_rmtree_allowed":false,"unit_test_fixture_final_residual":0,"targeted_test_invocation_cap":2,"offline_bounded_correction_cap":1,"focused_test_invocation_cap":1,"full_suite_invocation_cap":1,"compile_static_invocation_cap":1,"source_scan_invocation_cap":1,"codegraph_sync_cap":1,"external_payload_access":0,"release_root_access":0,"predevice_root_access":0,"readiness_root_access":0,"retained_r3_access":0,"legacy_r2_access":0,"deep_corrective_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"g4_04_stage_complete":false,"guide_fresh_e2_satisfied":false,"g4_05_planning_unlocked":false,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW","future_reference_task":"REF-G4-04-E2","future_reference_status":"WAITING_SEPARATE_FRESH_OFFLINE_E2_PACKAGE_PLAN_AFTER_CLEAN_COMMITTED_ROOT_BINDING","future_stage_locked":true}`

## 0. Activation gate

本文件当前只是draft。Executer只能在Orchestrator形成以下exact activation后开始：

1. parent `ce4eaab9e06bdb1c6092b2ab104b7f2931a7fb44`、tree `e1682006013ec148435a16515cb3688823bfd3f8`、branch
   `main`；
2. subject `docs(plan): activate e2 fresh root binding`；changed paths exact且仅为PLAN/ER/FULL；
3. activation child中PLAN/FULL strict parser为active`1/1`、同一`REF-G4-04-E2`、canonical next singleton；
4. GUIDE/source/test identity exact；retained R3仍unvalidated/unconsumed，release/device/formal/TD-C/G4-05/06 authority均false/0；
5. 已拒root不读取、不遍历、不stat；worktree在activation commit后clean。

任一项失败只写ER并stop，不编辑code/test。

## 1. Preflight与scope

Planner已独立确认current `frozen_e2_input()`无参数，并把`output_root`固定为已拒root
`/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-4995f7d65141-20260803T204648Z`；因此不能从clean committed owner直接生成
GUIDE §6所需fresh E2。本包只修复该enabling ownership seam，不生成package。

只修改existing E2 source/test；不新增module/helper service/controller/wrapper，不修改巨型P7模块或provenance owner。Root lexical validation、
input construction、result ledger与replay expected-input binding由同一E2 owner维护，禁止平行adapter、runtime global mutation、patch constant或
handwritten external controller。

## 2. Explicit fresh root owner

将repo-owned `frozen_e2_input` public contract改为：

`frozen_e2_input(*, output_root: str) -> E2Input`

- `output_root`必须显式keyword-only且无default；无参数调用必须`TypeError`，旧fixed root不得被隐式复用；
- type必须exact `str`，不接受`Path`、subclass、bytes或其他path-like；
- 使用一个E2内部pure lexical validator作为唯一root shape owner；不得读取、resolve、stat、创建或遍历路径；
- exact parent为`/Volumes/4T/temp/rgbww-optimizer`，路径必须是其exact direct child；
- `str(Path(value)) == value`且parts exact，拒绝重复slash、trailing slash、`.`、`..`、relative path、extra child、空segment；
- basename必须fullmatch `^g4-e2-preformal-[0-9a-f]{12}-[0-9]{8}T[0-9]{6}Z$`；拒绝uppercase hex、wrong prefix/suffix、
  slash、backslash及control字符；
- timestamp必须按UTC `YYYYMMDDTHHMMSSZ`严格calendar/time parse并round-trip exact，拒绝无效date/hour/leap值；不要求读取current clock；
- current fixed rejected root只能作为历史拒绝fixture，不能是default或production selection。Executer不得访问其filesystem identity。

`_validate_exact_input(value)`必须先验证`value.output_root`，然后以
`frozen_e2_input(output_root=value.output_root)`构造expected并对其余全部frozen fields做原有exact equality；不得放宽source、GUIDE、policy、
prerequisite、transport、authority或protected-source合同。

## 3. Root-bound result与replay

`_reference_ledger(inputs)`新增closed exact `output_root`字段，值必须等于validated `inputs.output_root`。因此evaluate result、persist revalidation
与replay revalidation都绑定同一root；top-level/nested closed-shape、canonical JSON、formal/machine owners、guards与authority不退化。

`replay_e2_package(root_path)`在repo-owned provenance owner绑定并读取actual root后，必须以actual bound `root.path`调用
`frozen_e2_input(output_root=root.path)`构建expected input，再执行canonical shared result validation。禁止仍调用无参factory、读取global
expected root或接受caller input。把root A的result/terminal复制到另一个同样合法的root B，即便更新terminal result file identity，也必须因
`reference_ledger.output_root=A`与actual B不符而fail closed。

`persist_e2_package`保持已接受public signature与owner binding：semantic validation必须在create/persist前；只保留create/persist I/O seams；
semantic/replay callback injection关闭；成功路径直接调用canonical replay。Create返回的bound root identity path必须exact等于validated
`inputs.output_root`，否则在写result前拒绝，避免I/O seam改变semantic root。

## 4. Tests

只修改existing E2 tests并保留全部owner-binding、closed result/terminal与tamper断言。至少新增：

1. `inspect.signature(frozen_e2_input)`证明exact一个kw-only、无default的`output_root`；无参调用TypeError，source中旧constant不再作为factory
   default；root选择不通过runtime global patch；
2. accepted lexical roots覆盖lowercase 12-hex与有效UTC timestamp，且construction不做filesystem call；
3. invalid exact类型：`Path`、bytes、str subclass；invalid parent、relative/extra-child、double/trailing slash、`.`、`..`、backslash、uppercase、
   wrong hex length、wrong prefix/suffix、invalid calendar/date/time全部拒绝；create/persist/read均0；
4. `_validate_exact_input`允许仅output_root按valid fresh value变化，但其他每个frozen字段仍exact；result ledger新增root且missing/extra/tamper拒绝；
5. persist在I/O前拒绝input/result root ledger mismatch；create/persist均0；create seam返回不同root identity时result persist=0；
6. cross-root transplant：用test-owned fixture生成两个exact合法且预先不存在的direct-child roots，并在A生成package，复制canonical artifacts到B并使terminal identity与B
   result一致，replay B仍因ledger A拒绝；不得读取任何历史/external root；
7. accepted ephemeral roundtrip显式传入fresh output_root，无patch `EXPECTED_OUTPUT_ROOT`或其他global，canonical replay/bytes/modes/inventory/
   terminal/deep immutable及cleanup residual0继续通过；
8. persist/replay signature、canonical thermal/replay owner、unexpected semantic keyword I/O=0及self-consistent forged evaluator rejection全部不退化；
9. AST/CodeGraph证明root validator pure、无filesystem/device/network/process/env/controller owner，只有provenance owner执行I/O。

测试fixture允许在`/Volumes/4T/temp/rgbww-optimizer`下为每个case选择最多两个exact合法、预先不存在的direct-child roots；basename nonce必须来自合法12位lowercase hex与严格UTC timestamp。不得使用嵌套`TemporaryDirectory`、patch runtime root constant或外部controller选择target。

Fixture必须由test-owned context/finalizer持有repo provenance owner返回的DirectoryIdentity。`finally`清理前重新验证path仍是expected direct child、identity未漂移、不是历史rejected root，inventory只能是exact known artifact names且均为regular files；随后只对记录的exact child逐项unlink并对exact root执行`rmdir`。禁止glob、recursive delete、rmtree、parent cleanup或按prefix扫描。若identity/inventory漂移则fail closed并报告residual，不得扩大删除范围。每case及并发root cap均为2，正常结束residual必须0。现有mock只可用于无I/O调用计数/owner isolation，不得改变production root或semantic truth。

## 5. Validation与failure convergence

顺序：

1. targeted E2 tests；首次失败允许仅在existing source/test内一次bounded correction并重跑；同边界第二次失败立即stop；
2. focused lineage/predevice/zero-readiness/E2/R6/thermal/provenance tests一次；
3. full suite一次；`compileall -q src tests`；wrapper syntax；
4. repo-owned baseline-aware source scan对activation→worktree exact source/test，要求0 findings；
5. `git diff --check`与dirty-path invariant；GUIDE/RESEARCH、PLAN/FULL、archives、config、wrappers、巨型P7 owners未变；
6. `codegraph sync`后query fresh-root validator/result-ledger/replay binding及canonical owner无退化；
7. PLAN/FULL repo-owned parser为active`1/1` same task，canonical next不变。

ER必须记录每个gate invocation/count、是否使用唯一correction、source/test before/after identity与所有negative cases。测试通过后不得执行
production evaluator/persist/replay，不得创建durable package/root；成功只提出engineering acceptance candidate。

## 6. Safety与stop

- 旧fixed/rejected E2 root及所有external payload访问0；durable root/package generation0；production evaluate/persist/replay0；
- device/network/app/process/listener/camera/Ray/strip/capture/light/release/formal/TD-C/firmware/deployment均0；
- 不生成或执行fresh package PLAN，不生成G4-05/06 PLAN，不解锁G4-05 planning/execution；
- 不创建task ID/suffix，不把offline tests表述为fresh E2、hardware readiness或formal pass。

Executer唯一stop是`RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW`。若accepted，Planner只接受root-binding engineering unit，
随后同一task active0返回Orchestrator；只有从clean committed checkpoint起草的下一独立PLAN才能选择一个exact fresh root并生成one package。
