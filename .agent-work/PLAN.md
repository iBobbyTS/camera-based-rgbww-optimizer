# P7 retained-R3 Option B：M1-I1-C1 Git grammar correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-I1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-C1-GIT-GRAMMAR-CORRECTION-V1`

**当前唯一动作：** 在M1 single generated-command owner中把全部56条read-only Git argv改为P3现有canonical
show grammar，并在M1 dedicated test中证明全部56条shape、target cycling及P3 eligibility；完成离线验证、single exact
two-path commit与single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_I1_C1_GIT_GRAMMAR_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0118-p7-retained-r3-b2-m1-i1-git-gate-failure-review.md`；bytes
`4927`，SHA-256 `48cf15c84bad5037c7ecb9baba977e233116c2ca2cbefedee466d9626609afbf`；不得覆盖 earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_i1_c1_git_grammar_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-I1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-C1-GIT-GRAMMAR-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"99bc4ec1710395fc54772343fc650daf7d29e7d4","expected_subject":"chore(plan): activate real manifest Git grammar correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0118-p7-retained-r3-b2-m1-i1-git-gate-failure-review.md"],"clean_porcelain_required_after_activation":true},"reviewed_failure":{"activation_commit":"2f2899ac769d0ac30662b495dfbdfd06fe508282","evidence_commit":"99bc4ec1710395fc54772343fc650daf7d29e7d4","stable_code":"git_command_denied","phase":"activation","controller_process_exit":1,"controller_git_attempts":1,"controller_git_successes":0,"source_created":1,"input_roots_created":7,"input_files_created":7,"output_root_created":0,"output_files_created":0,"retry":0,"fallback":0,"failure_evidence_disposition":"IMMUTABLE_NO_READ_NO_REUSE_NO_MODIFY_NO_DELETE_NO_RETRY"},"accepted_baseline":{"m1_commit":"c480c4065081eab06388a12e95fd79b37b0230e2","m1_source_blob":"4bf50cf69f259f212e34d9be5eacd7721ed91c41","m1_source_sha256":"8016df1265a82a49b90c7bbe33ccf7621c61ac9568538f159aea4f84fca3543f","m1_test_blob":"4036e05ed0ad92d4afc52df69b9a7cf7356c8fef","m1_test_sha256":"d8bff33770aba2b002b25652e086e5f45f5ef646cc0ade97d1a7be8ea7a99fc4","p3_source_blob":"d6d6cc628861baf8a95a09f13fa9204989693b5b","p3_source_sha256":"118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d","p3_git_owner":"_validate_git_argv"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-I1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-C1-GIT-GRAMMAR-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_GIT_GRAMMAR_CORRECTION","m1_real_manifest_candidate_commit":"c480c4065081eab06388a12e95fd79b37b0230e2","m1_real_manifest_candidate_consumable":false,"m1_synthetic_integration_status":"REJECTED_GIT_COMMAND_DENIED_CORRECTION_ACTIVE","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"correction_contract":{"generated_git_invocations":56,"target_count":7,"cycles":8,"old_argv_prefix":["git","show","-s","--format=%H"],"new_argv_prefix":["git","show","-s","--format=%H%x00%P%x00%s"],"target_expression":"GIT_TARGETS[index % 7]","p3_grammar_changed":false,"generic_allowlist":false,"second_git_runner":false,"retry":0,"fallback":0},"test_contract":{"dedicated_test_methods":13,"all_generated_argv_shapes_asserted":56,"p3_owner_acceptance_asserted":56,"target_cycle_exact":[0,1,2,3,4,5,6,0],"target_cycles":8,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): align real manifest Git ledgers","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"codegraph_queries":0,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"generic_allowlist":0,"second_git_runner":0,"failed_fresh_evidence_reads":0,"failed_fresh_evidence_writes":0,"failed_fresh_evidence_deletes":0,"synthetic_integration_runs":0,"controller_processes":0,"external_root_reads":0,"external_root_writes":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0118-p7-retained-r3-b2-m1-i1-git-gate-failure-review.md","bytes":4927,"sha256":"48cf15c84bad5037c7ecb9baba977e233116c2ca2cbefedee466d9626609afbf"},"planner_stop":"B2_M1_I1_C1_GIT_GRAMMAR_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 frozen gates

Orchestrator必须先把review decision与唯一active task写入FULL，再创建activation。Activation parent exact
`99bc4ec1710395fc54772343fc650daf7d29e7d4`，subject exact
`chore(plan): activate real manifest Git grammar correction`，changed paths exact：

1. `.agent-work/FULL_PLAN_REFERENCE.md`；
2. `.agent-work/PLAN.md`；
3. `.agent-work/PLANS/20260801-0118-p7-retained-r3-b2-m1-i1-git-gate-failure-review.md`。

Activation后porcelain必须clean。Executer验证activation topology、PLAN/FULL machine subset、archive final bytes/SHA、accepted
M1/P3 blob identities。任一不符时code/test edit、test、CodeGraph与implementation commit全部0，只append ER一次并停止。

Fresh failure evidence source、seven roots/files与absent output由ER冻结。Executer不得读取、stat、list、glob、search、复用、
修改、删除、cleanup或retry这些external paths；不得运行controller或构建新的source/root。只允许读取repository Git objects、
active PLAN/FULL与代码/测试。

## 2. Exact single-owner correction

只修改M1 `_GIT_LINES`生成表达式，把每条：

`("git", "show", "-s", "--format=%H", GIT_TARGETS[index % 7])`

改为P3现有exact accepted shape：

`("git", "show", "-s", "--format=%H%x00%P%x00%s", GIT_TARGETS[index % 7])`

全部56条由同一generator产生，target顺序0..6循环8次。继续检查每个ledger `exit_code == 0`且`stderr == b""`。
不得编辑P3 `_validate_git_argv`或其test，不得增加generic/regex/path allowlist、alternate Git command、第二runner、fallback、
command normalization或异常吞噬。更新M1 canonical template golden SHA literal；replacement contract不因该command token变化而
重构。

## 3. Dedicated regression coverage

只在M1现有dedicated test内增强既有test10/test13，不增加test method：

- 从composed generated source验证`run_read_only_git` exact56、`.exit_code` exact56、`.returncode` exact0；
- 验证每一条56 argv均为exact五项P3 show grammar，target expression按0..6循环8次，不能只断言首条或family count；
- fake success执行时记录全部56 actual argv；每项必须通过真实P3 `run_read_only_git`的现有validator，process dependency使用
  in-memory fake completed result，不启动Git subprocess；逐项ledger exit0/stderr empty，recorded actual targets顺序exact；
- 保留existing manifest payload、lifecycle、primary-failure identity、negative authority及method inventory assertions。

不得在test中复制P3 grammar实现、直接调用private validator、创建generic scanner/harness/second fake controller或通过
monkeypatch绕过P3 eligibility。

## 4. Ordered validation 与 commit

Semantic diff完成后依次且各一次：

1. targeted exact command，`13/13 OK`；
2. focused exact command，`83/83 OK`；
3. compileall exact command，exit0；
4. full exact command，`800/800 OK`。

只有四项全绿后才运行exact一次`codegraph sync`，只作maintenance，不运行query、不从sync得出semantic结论；nonzero立即停止。
随后`git diff --check`，验证diff changed paths exact two且只有command token、golden及dedicated coverage相关变化。创建single commit：

`fix(p7): align real manifest Git ledgers`

Commit direct parent必须是runtime activation HEAD，changed paths exact source/test，porcelain clean。然后postcommit targeted exact
一次，`13/13 OK`。Tests总invocations exact4、compileall1、sync1、query0、retry/fallback0。

## 5. Evidence、locks 与 stop

无论success/failure，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append，冻结activation/frozen gates、exact diff、56-shape
coverage、ordered validation、sync、commit topology/final blob/bytes/SHA、ER prefix和全部zero budgets，然后停唯一Planner门。

M1-I1本身retry exact0。Correction全绿也不得读取旧fresh evidence、重新运行synthetic integration或进入M1-R1；只有Planner
接受correction后，Orchestrator可再让Planner规划一个新activation-derived fresh M1-I1 package。

真实C1/retained、canonical validator/callback、eligibility、retained audit、release、network/DNS/env/credentials、device/camera/
Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。本pure-offline engineering
correction不需要Advisor或Human授权。

维护性边界：M1继续单独拥有generated command，P3继续单独拥有read-only Git eligibility；不新增owner、runner、allowlist、
compatibility layer或future cleanup debt。
