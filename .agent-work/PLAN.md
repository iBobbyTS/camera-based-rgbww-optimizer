# REF-G4-04-E2：fresh offline preformal integration gate

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_OFFLINE_E2_PREFORMAL_GATE`

**Executable：** `true`（仅在Orchestrator把FULL对齐为同一contract并创建exact activation commit后生效）

**Active task count：** `1`

**Active task：** `REF-G4-04-E2`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_PREFORMAL_GATE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-E2-PREFORMAL-OFFLINE-INTEGRATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_OFFLINE_E2_PREFORMAL_GATE","executable":true,"active_task_count":1,"active_task":"REF-G4-04-E2","reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_OFFLINE_PREFORMAL_ONLY","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"4995f7d65141ce8a4086d74f9add21c5b44d593d","expected_parent_tree":"da458ce4a81344397354a8535e8a38cef5d59375","expected_subject":"docs(plan): activate g4 e2 preformal gate","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"single_current_action":"implement_one_repo_owned_pure_e2_integration_and_evidence_owner_validate_exact_accepted_prerequisite_references_and_non_executable_r6_contract_then_persist_one_fresh_non_authorizing_offline_package","allowed_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","tests/test_p7_successor_e2.py",".agent-work/EXECUTION_RESULT.md"],"new_production_modules":1,"new_test_files":1,"existing_production_edits":0,"giant_p7_module_edits":0,"config_edits":0,"wrapper_edits":0,"full_edits_by_executer":0,"plan_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"corrective_suffixes":0,"new_task_ids":0,"source_checkpoint":"4995f7d65141ce8a4086d74f9add21c5b44d593d","source_tree":"da458ce4a81344397354a8535e8a38cef5d59375","guide":{"path":"advisor/4/4.GUIDE.md","sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35"},"g4_01_release":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release","source_head":"779c7d9572d991f82076c892ec8198a059bbe44e","source_tree":"1ead5268917612d1232543b1a7eca28788f3980c","mode":448,"artifacts":[["frozen-inputs.json",5047,"8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8"],["r6-formal-plan.json",899,"dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b"],["release-descriptor.json",2024,"6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452"],["validation-summary.json",432,"07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07"],["terminal-seal.json",808,"d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850"]],"canonical_validator_success":true,"eligibility":true,"release_consumable":true,"release_consumption_authorized":false},"g4_02_predevice":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z","mode":448,"artifacts":[["predevice-oracle-result.json",3186,"78fa982b7f318734afc158324b968ee71ff41b5ce7b91e27d6eabc0f60bc40d9"],["terminal-seal.json",1114,"39456ca3379df45cae0ca5337bf6d24d2040e6581dcd074b8ebf12d39b87e68e"]],"disposition":"ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED"},"g4_03_readiness":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-d957a89a84d3-20260803T200550Z","terminal_sha256":"c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d","reviewed_plan_archive":[".agent-work/archived/PLAN-20260803-1436.md",11600,"bdb9666ccda837123c2461df8f2e3bedd725ab1d941fdc6439e4aa7c0e8c82e8"],"reviewed_er_archive":[".agent-work/archived/EXECUTION_RESULT-20260803-1436.md",11039,"9c39787d61a36c403887f41b59f47f7016437226286339237c187ae147708b5f"],"owner":["src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py",36066,"ba326702ad53aba06eeef2c12a86753c31bbeaa65bed78139dc777f2047d9193"],"tests":["tests/test_p7_successor_zero_readiness.py",25654,"6bbee82e8e61a65aada750e7d5b74d30157d38b61c8edec4b7d20bd907d1a2dd"],"wrapper":["tmp/run-g4-zero-readiness.zsh",2969,"13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a"],"classification":"REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN","request_transport_success":false,"request_transport_exit":1,"request_error_code":-128,"final_residual":0,"disposition":"ACCEPTED_G4_03_ZERO_READINESS_WITH_REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN"},"policy":{"path":"config/hsi/p7-ray-td-b-exposure-policy-v2.json","bytes":4065,"sha256":"c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681","status":"qualified_1_2500"},"protected_owners":[["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",203416,"14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1"],["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",188493,"a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47"],["src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py",97644,"8e68400d51d01a20f4629aec7ad17c084835d7242e1cfba73a0335916209fa03"],["src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py",26438,"8485755619ee6cee11845ff0ca698a8fff0906ff42537b3039ce5b8358fc1555"],["src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py",24232,"4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81"],["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py",27938,"38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608"],["tmp/run-p7-thermal-diagnostics.zsh",4070,"2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5"]],"e2_output_root":"/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-4995f7d65141-20260803T204648Z","e2_output_root_preflight":"ABSENT_AT_PLANNER_REVIEW","e2_output_root_mode":448,"e2_artifacts":["preformal-gate-result.json","terminal-seal.json"],"e2_root_creation_cap":1,"e2_evaluation_cap":1,"e2_replay_cap":1,"release_root_access":0,"release_consumption":0,"predevice_root_access":0,"readiness_root_access":0,"retained_r3_access":0,"legacy_r2_access":0,"deep_corrective_access":0,"other_external_payload_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"config_write_calls":0,"formal_capture_count":0,"physical_capture_count":0,"fake_adapter_only":true,"targeted_test_invocation_cap":2,"focused_test_invocation_cap":1,"full_suite_invocation_cap":1,"compile_static_invocation_cap":1,"wrapper_syntax_invocation_cap":1,"codegraph_sync_cap":1,"offline_bounded_correction_cap":1,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_04_E2_PREFORMAL_GATE_REVIEW","future_reference_task":"REF-G4-05-RAY-R6-STAGE-GATE","future_stage_locked":true}`

## 1. Activation与intake

Executer开始前必须证明：

1. branch为`main`；HEAD是machine row中expected parent的direct child；activation subject与exact three paths一致。
2. PLAN/FULL strict parser通过；contract均为`G4-E2-PREFORMAL-OFFLINE-INTEGRATION-V1`；active task/count均为
   `REF-G4-04-E2 / 1`。
3. 除activation three paths外worktree clean；GUIDE、policy、protected owners、G4-03 owner/test/wrapper与review archives
   的bytes/SHA exact。
4. exact E2 output root不存在；G4-01/02/03 external roots只作为冻结reference，不读取、不遍历、不消费。
5. G4-05/06、formal capture、device、camera、Ray、strip、network、release consumption与TD-C保持locked。

任一项失败：不得创建E2 root或编辑code/test，只写ER并stop。禁止reset、clean、checkout或从旧archive生成新语义。

## 2. Maintainability与ownership

Preflight结论：三大巨型P7模块已拥有exposure policy、R6 plan/ledger、runner/cleanup与analyzer语义，本包不得修改它们。
G4-01 lineage、G4-02 predevice、G4-03 readiness及provenance owner也保持单一source of truth。

只新增`p7_successor_e2.py`作为窄的stage integration/evidence owner。它只能组合现有owner的公开contract，不得复制
formal plan、serialization、filesystem、release validator、readiness classifier或device control语义；不得成为formal runner。
所有I/O只通过既有provenance owner注入的root/create/persist/read/replay接口。不得新增CLI、wrapper或controller。

## 3. Pure E2 input与result contract

新增frozen、exactly typed input/reference records及一个pure evaluator。Input必须逐项保留machine row冻结的：

- source checkpoint/tree、GUIDE与policy identity；
- G4-01 exact five release artifact names/bytes/SHA及accepted-but-unconsumed状态；
- G4-02 exact two durable evidence artifact identities；
- G4-03 terminal seal、review archive、owner/test/wrapper identities及historical transport/effect分类；
- protected formal plan/runner/analyzer/lineage/predevice/provenance/wrapper source identities。

Evaluator必须通过依赖注入各调用一次现有`build_td_b_r6_formal_plan`、`validate_td_b_r6_formal_plan`与
`td_b_r6_machine_status`，并fail closed验证：

- exact Ray-only 000..015顺序；A/D/B/C shutter分别`1/5000`、`1/6400`、`1/8000`、`1/2500`；
- plan仍是`selected_exposure_policy_non_executable`、`executable=false`；formal logical/physical均16、ambient/setup均0、
  launch1、retry0、old/new pooling prohibited；
- failure contract仍为accepted hard-failed formal attempt、formal false、strip call count0、retry0；
- operational 600仍是selected transient而非steady；strip/TD-C/sentinel/P8 locks不变；
- G4-03 request transport仍false、exit1/error-128，只允许effect-confirmed-clean分类；
- retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption及全部device/formal authority均false。

Output必须deep immutable且可投影为canonical JSON；只允许状态
`offline_preformal_contract_pass_waiting_planner_review`或fail-closed exception。不得含execution authorization、Human
authorization、formal pass、hardware readiness、release consumed或G4-06 unlock claim。

## 4. Fake-adapter与fail-closed tests

仅新增`tests/test_p7_successor_e2.py`，至少覆盖：

1. exact frozen input通过，三项existing owner各调用一次，result字段/guards/authority exact；
2. release五项、predevice两项与G4-03 identities任一name/bytes/SHA/order/count漂移均拒绝；
3. source checkpoint/tree、GUIDE/policy/protected source identity、qualification/shutter任一漂移均拒绝；
4. G4-03 transport被伪写success、exit/error改变、effect classification/final residual改变均拒绝；
5. formal ID/order/source/shutter/budget/ambient/setup/launch/retry/pooling/failure contract任一漂移均拒绝；
6. operating/steady与strip/TD-C/sentinel/P8 lock任一漂移均拒绝；
7. invalid type、bool-as-int、mutable/open shape、duplicate artifact或non-absolute root fail closed；
8. evaluator纯函数、输入不变、结果deep immutable与canonical JSON projection exact；
9. non-executable formal plan交给现有execution validator时在fake backend的connect/config/capture调用前被拒绝，调用均0；
10. durable E2 package仅含exact two artifacts，root/file mode为0700/0600、canonical bytes、terminal非自引用、独立replay一次；
11. result persist或terminal persist失败时保留单一fail seal；不得alternate root/retry；
12. AST/CodeGraph证明integration evaluator无device/network/process/subprocess/env owner，persistence只调用既有provenance owner。

Tests只使用in-memory/fake adapters及位于`/Volumes/4T/temp/rgbww-optimizer`下的fresh test temporary roots；不得读取
G4-01/02/03或任何旧external payload。

## 5. Validation与唯一fresh E2 package

顺序：

1. targeted新测试；首次失败只允许在新owner/test内一次bounded correction并重跑targeted。同一边界第二次失败stop。
2. focused：successor lineage、predevice、zero-readiness、R6 contract、thermal runner与provenance owner tests。
3. full suite；`compileall -q src tests`；`zsh -n tmp/run-p7-thermal-diagnostics.zsh`；`git diff --check`。
4. 使用现有source scanner对exact changed source/test相对activation HEAD做baseline-aware secret/path扫描；private value、env read、
   network target、unsafe absolute path、symlink或changed-path越界均fail。
5. `codegraph sync`后query新owner只组合现有pure/formal/provenance owner，没有device/network/process/controller边。
6. 全部通过后，用repo-owned owner对machine row exact frozen record evaluate一次，再在exact E2 output root持久化一次并replay一次。
   Package只能是`preformal-gate-result.json`与`terminal-seal.json`；terminal hash由ER外部记录，不得自引用。

E2 package是offline engineering evidence，不是formal root，不得读取release/readiness payload，不得访问任何device。即使PASS，
Executer也只能提出`G4_04_E2_ACCEPTANCE_CANDIDATE_OFFLINE_PREFORMAL_CONTRACT_PASS`。

## 6. Failure convergence与hard locks

- ordinary owner/test工程失败：一次bounded correction；同边界第二次失败停止回Orchestrator，不创建corrective task/suffix。
- frozen policy/source/prerequisite identity不一致、无法维持Ray-only/strip-zero/fixed-shutter/no-retry合同，立即fail closed；不得猜测。
- 不得进入G4-05/06，不得构造execute-authorized plan，不得请求或消费Human formal authorization。
- 不得访问retained R3、legacy R2、deep corrective、formal root、camera、Ray、strip、network或external payload。

## 7. Handoff

ER必须记录activation topology、source/test before/after identity、exact prerequisite reference账本、existing owner调用计数、
truth-table/negative cases、test/check exact counts、CodeGraph边、source scan、E2 root/artifact identities与terminal external SHA、
replay结果，以及全部prohibited access/count为0。

Executer停止于`RETURN_FOR_G4_04_E2_PREFORMAL_GATE_REVIEW`。Planner必须先归档PLAN/ER并独立验收；只有Orchestrator可
终结G4-04并将`REF-G4-05-RAY-R6-STAGE-GATE`解锁为planning-only。本PLAN不授权或生成G4-05/06 PLAN。
