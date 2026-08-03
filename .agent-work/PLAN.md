# REF-G4-04-E2：Package B fresh E2 evidence

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FRESH_E2_EVIDENCE_ONLY`

**Executable after activation：** `true`

**Active task count after activation：** `1`

**Active task after activation：** `REF-G4-04-E2`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_04_FRESH_E2_EVIDENCE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-E2-FRESH-EVIDENCE-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_FRESH_E2_EVIDENCE_ONLY","executable":true,"active_task_count":1,"active_task":"REF-G4-04-E2","reference_task_id":"REF-G4-04-E2","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_FRESH_E2_EVIDENCE_ONLY","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0","expected_parent_tree":"0b2d9a58db1d84a7ca8997f354df5be726ddf225","expected_subject":"docs(plan): activate fresh e2 evidence","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md"],"child_sha_recorded_in_plan":false},"execution_authorized_before_activation":false,"single_current_action":"generate_and_independently_replay_one_fresh_e2_evidence_package","allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"source_or_test_edits":0,"full_edits_by_executer":0,"plan_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"new_modules":0,"controller_files":0,"corrective_suffixes":0,"new_task_ids":0,"branch":"main","execution_cwd":"/Users/ibobby/Projects/WLED-RGBWW","package_a_checkpoint":"50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0","package_a_tree":"0b2d9a58db1d84a7ca8997f354df5be726ddf225","package_a_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py","bytes":27874,"sha256":"717db782214c60681c6876d94213637f0a75ed4f380e8e5e2971b58cbb436747"},"package_a_tests":{"path":"tests/test_p7_successor_e2.py","bytes":53423,"sha256":"24b2f8a89dc79ac15ed1537aad34380ebe5ffc9259733927f46cc0eceadec4f3"},"package_a_reviewed_plan":{"path":".agent-work/archived/PLAN-20260803-1705.md","bytes":19743,"sha256":"83f0b46e09f77a2a98e52c06f10ba8a2b795c66fe7ee7e7c3643edea8b3b9010"},"package_a_reviewed_execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1705.md","bytes":11360,"sha256":"880bc3338cf52bf953ddfcab4c57c82cde1e6c41e657c83d1e87644136ecd530"},"fresh_root":"/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z","fresh_root_must_be_absent":true,"alternate_root_allowed":false,"retry":0,"repair":0,"production_factory_cap":1,"production_evaluate_cap":1,"production_persist_cap":1,"canonical_internal_replay_cap":1,"independent_public_replay_cap":1,"root_create_cap":1,"root_mode":448,"artifact_names":["preformal-gate-result.json","terminal-seal.json"],"artifact_mode":384,"inline_python_packaging_allowed":true,"inline_packaging_is_semantic_owner":false,"semantic_dict_or_bytes_construction_allowed":false,"semantic_callback_injection_allowed":false,"builder_validator_machine_replay_injection_allowed":false,"create_persist_seam_injection_allowed":false,"git_env_external_payload_reads_in_packaging":0,"test_invocations":0,"focused_test_invocations":0,"full_test_invocations":0,"compile_invocations":0,"codegraph_invocations":0,"package_a_full_validation_inherited":{"tests":917,"passed":917,"source_tree_unchanged_required":true},"release_root_access":0,"predevice_root_access":0,"readiness_root_access":0,"retained_r3_access":0,"rejected_e2_root_access":0,"legacy_or_deep_corrective_access":0,"device_access":0,"network_access":0,"app_access":0,"process_access":0,"listener_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"nonzero_light":0,"release_consumption":0,"formal_r6_access":0,"formal_root_creation":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"fresh_e2_accepted_before_planner_review":false,"g4_04_stage_complete_before_planner_review":false,"g4_05_plan_generation_allowed":false,"g4_05_execution_authorized":false,"g4_06_unlocked":false,"human_governance_gate":false,"advisor_scientific_gate":false,"planner_stop":"RETURN_FOR_G4_04_FRESH_E2_EVIDENCE_REVIEW","future_reference_task":"REF-G4-05-RAY-R6-STAGE-GATE","future_reference_status":"LOCKED_UNTIL_PLANNER_ACCEPTS_FRESH_E2_AND_ORCHESTRATOR_ADVANCES_FULL"}`

## 0. Activation gate

本PLAN当前是draft；不得检查fresh root、不得调用E2 owner。Executer只能在Orchestrator形成以下exact activation后执行：

1. cwd exact `/Users/ibobby/Projects/WLED-RGBWW`；parent `50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0`、tree
   `0b2d9a58db1d84a7ca8997f354df5be726ddf225`、branch `main`；
2. activation subject exact `docs(plan): activate fresh e2 evidence`，changed paths exact且仅为
   `.agent-work/EXECUTION_RESULT.md`、`.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`；
3. activation child后worktree clean；PLAN/FULL repo-owned strict parser为active `1/1`、同一
   `REF-G4-04-E2`、canonical next singleton；
4. Package A source/test与两个review archives的bytes/SHA仍与machine row exact；
5. retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`，release consumption、device、formal、TD-C及G4-05/06 authority仍false/0。

任一activation项失败：owner factory/evaluate/persist/replay/root access全部`0`，只写ER并stop。

## 1. Frozen inputs and single root

Package B只允许：

- source checkpoint：`50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0`；
- source tree：`0b2d9a58db1d84a7ca8997f354df5be726ddf225`；
- output root：
  `/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z`。

Executer在所有owner调用前只对该exact root执行一次冻结的absence gate：

```zsh
[[ ! -e "/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z" && ! -L "/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z" ]]
```

不得列举parent、glob、scan或访问任何其他root。若exact root已存在或symlink存在，factory/evaluate/persist/replay均`0`并stop。不得删除、
移动、修补、复用或另选root。

Package A已在同一source tree上fresh通过917/917；本包禁止修改代码/测试，也禁止重复targeted/focused/full/compile/CodeGraph。

## 2. Exact production packaging

Root absence gate通过后，只运行下面冻结的一条薄packaging命令一次。命令只import repo-owned E2 owner，传入三个literal，依序调用factory、
evaluate一次、persist一次；persist内部只能调用canonical replay一次。不得修改命令语义、拆出controller文件、构造semantic dict/bytes、
注入builder/validator/machine/replay/create/persist seam、读取Git/env/external payload或加入alternate/retry：

```zsh
.venv/bin/python -c 'from camera_based_rgbww_optimizer.optimization import p7_successor_e2 as e; i=e.frozen_e2_input(output_root="/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z",source_checkpoint="50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0",source_tree="0b2d9a58db1d84a7ca8997f354df5be726ddf225"); r=e.evaluate_e2_preformal_gate(i); p=e.persist_e2_package(i,r); t=e.provenance.decode_canonical_json(p.terminal.data); print("ROOT",p.root.path,p.root.device,p.root.inode,p.root.mode); print("RESULT",p.result.path,p.result.byte_count,p.result.sha256,p.result.device,p.result.inode,p.result.mode); print("TERMINAL",p.terminal.path,p.terminal.byte_count,p.terminal.sha256,p.terminal.device,p.terminal.inode,p.terminal.mode); print("TERMINAL_VALUE",t); print("INTERNAL_REPLAY",p.replay)'
```

Inline命令只是execution packaging，不是production semantic owner；所有semantic values、canonical bytes、validation与I/O都由repo-owned E2/provenance/
thermal owner产生。不得把stdout写入fresh root，也不得在root中新增第三个artifact。

## 3. Independent public replay and evidence

仅当第2节命令exit 0，运行下面独立只读packaging一次。它必须先调用public replay一次，再由repo provenance owner只读绑定同一个exact root/
inventory/files并输出identity summary；不得改变artifact：

```zsh
.venv/bin/python -c 'from camera_based_rgbww_optimizer.optimization import p7_successor_e2 as e; q=e.replay_e2_package("/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z",source_checkpoint="50bb3346b3f3f99b27a9c53e25fc7fa61802f5d0",source_tree="0b2d9a58db1d84a7ca8997f354df5be726ddf225"); d=e.provenance.read_existing_root("/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-50bb3346b3f3-20260803T231121Z"); n=e.provenance.list_exact_regular_children(d); r=e.provenance.read_exact_file(d.path+"/"+e.RESULT_NAME,expected_mode=0o600,root=d); t=e.provenance.read_exact_file(d.path+"/"+e.TERMINAL_NAME,expected_mode=0o600,root=d); v=e.provenance.decode_canonical_json(t.data); print("INDEPENDENT_REPLAY",q); print("ROOT",d.path,d.device,d.inode,d.mode); print("INVENTORY",n); print("RESULT",r.path,r.byte_count,r.sha256,r.device,r.inode,r.mode,r.root); print("TERMINAL",t.path,t.byte_count,t.sha256,t.device,t.inode,t.mode,t.root); print("TERMINAL_VALUE",v)'
```

Executer必须在ER记录：

- 两条命令exact invocation/exit与owner call counts；
- root exact path/device/inode/mode=`0700`；
- inventory exact且有序为`preformal-gate-result.json`、`terminal-seal.json`；
- result/terminal exact path、bytes、SHA-256、device、inode、mode=`0600`，且file root identity与root一致；
- terminal schema/status exact，`artifact_count_before_terminal=1`、`terminal_self_reference=false`、`retry=0`、
  `alternate_root=0`、authority exact `execution_authorized=false/formal_r6_access=0/capture_count=0`；
- internal与independent replay均schema/status pass、same root identity/result/terminal identity、`execution_authorized=false`；
- Package A HEAD/tree、source/test/archive identity、PLAN/FULL parser、`git diff --check`及final repo status。

成功只形成fresh E2 acceptance candidate；必须等待Planner独立review，不能自称fresh E2 accepted或G4-04 complete。

## 4. Failure branches

- absence/activation/source/parser失败：owner/root create `0`，stop；
- factory/evaluate失败：root create `0`，保留异常并stop；
- persist失败：不重试、不修复、不清理、不换root；保留repo owner形成的single failure/partial seal与traceback，立即stop；
- canonical internal replay失败：保留exact root/result/terminal证据，立即stop；
- independent replay、inventory、mode、identity、terminal或authority任一失败：保留exact root，立即Planner review；
- 所有失败分支retry=`0`、repair=`0`、alternate root=`0`。不得生成corrective suffix或新实验root。

## 5. Safety, repository and stop

- 仅允许新建上面唯一fresh offline E2 root及其exact两个artifact；不得访问旧rejected E2、G4-01 release、G4-02 predevice、G4-03 readiness、
  retained R3、legacy/deep-corrective或其他external payload；
- device/network/app/process/listener/camera/Ray/strip/capture/nonzero light/release consumption/formal R6/formal root/TD-C/firmware/deployment均0；
- repo内仅允许Executer更新`.agent-work/EXECUTION_RESULT.md`；PLAN/FULL/archive/source/test/GUIDE/RESEARCH/config/wrapper均只读；
- 不运行测试/compile/CodeGraph，不stage/commit/push/PR，不生成controller、wrapper、log或第三artifact；
- `git diff --check`与final status只验证repo state；不得为了clean而修改、reset或清理用户内容。

Executer唯一stop为`RETURN_FOR_G4_04_FRESH_E2_EVIDENCE_REVIEW`。本PLAN是G4-04最后一个执行包，但不生成或执行G4-05 PLAN；
只有Planner接受fresh E2且Orchestrator更新FULL后，G4-05 planning才可能解锁。
