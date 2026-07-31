# REF-P7-25-R2-B2-P4：repo-owned controller conformance/composition owner

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-CONTROLLER-CONFORMANCE-COMPOSITION-OWNER-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact
activation commit；activation后，Executer只在exact两个repo paths实现并验证一个
pure-in-memory controller conformance/composition owner，然后创建一个focused repair
commit。不得生成或运行external controller，不得创建qualification/evidence root。

**唯一 Planner stop：**
`B2_P4_CONTROLLER_CONFORMANCE_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1106-p7-retained-r3-b2-owner-api-controller-architecture-review.md`。
bytes `6686`，SHA-256
`feb896f822efc57f796730ca330f37b1109c51b4dcc2533e757d19e6d1f3d3c9`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_controller_conformance_composition_owner_v1","reference_task_id":"REF-P7-25-R2-B2-P4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-CONTROLLER-CONFORMANCE-COMPOSITION-OWNER-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"102c625eb73cf49d7e14af12663f967397e28fa2","expected_subject":"chore(plan): activate b2 controller conformance owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1106-p7-retained-r3-b2-owner-api-controller-architecture-review.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","activation_head_must_match_frozen_activation_tuple":true,"expected_subject":"feat(p7): add retained controller conformance owner","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_controller_conformance.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-CONTROLLER-CONFORMANCE-COMPOSITION-OWNER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_controller_conformance.py"],"accepted_owner_types":{"DirectoryIdentity":["path","device","inode","mode"],"FileIdentity":["path","data","byte_count","sha256","device","inode","mode","root"],"GitLedger":["argv","cwd","exit_code","stdout","stderr","stdout_sha256","stderr_sha256"],"MachineContractEvidence":["schema","owner","marker_ascii","source_bytes","source_sha256","candidate_count","candidate_lines","line_number","raw_row_bytes","raw_row_sha256","payload_bytes","payload_sha256","line_ending"],"ParsedMachineContract":["value","evidence"],"ByteSpan":["start","end"],"OwnedStatementPair":["assignment_span","validation_span","function_name"],"PreparedControllerSource":["source","source_sha256","pair"],"SealTargetIdentity":["path","byte_count","sha256","device","inode"]},"required_public_methods":{"MachineContractEvidence":["to_mapping"],"SealTargetIdentity":["as_mapping"]},"runtime_ast_contract":{"runtime_and_negative_fixture_parse_calls_are_disjoint":true,"unknown_owner_attribute_rejected":true,"alias_escape_rejected":true,"dynamic_getattr_vars_dict_reflection_rejected":true,"opaque_validated_seal_gate_not_introspected":true,"git_success_field":"exit_code","forbidden_runtime_attribute":"returncode","read_exact_file_requires_live_root_binding":true,"literal_root_rejected":true},"root_chain_contract":{"pure_in_memory":true,"pre_post_directory_identity_exact":true,"every_file_identity_root_equals_pre":true,"every_file_path_exact_direct_child":true,"device_inode_mode_and_sibling_escape_negatives":true},"lifecycle_contract":{"all_effects_injected_callbacks":true,"conformance_before_effect_callbacks":true,"success_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"failure_terminal_attempted_once":true,"seal_dominates_admission":true,"valid_fail_admission_preserves_primary_error":true,"retry":0,"fallback":0},"test_contract":{"dedicated_test_methods":14,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_controller_conformance","focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","baseline_full_tests":741,"expected_full_tests_after_exact_14_methods":755,"compileall_command":".venv/bin/python -m compileall -q src tests","codegraph_sync_required":true,"git_diff_check_required":true},"execution_budgets":{"implementation_commits":1,"controller_processes":0,"external_controller_writes":0,"evidence_root_creates":0,"qualification_writes":0,"execution_result_appends":1,"test_invocations":4,"codegraph_sync":1,"retry":0,"fallback":0},"zero_budgets":{"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_controller_reads":0,"old_root_reads":0,"old_evidence_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_CONTROLLER_CONFORMANCE_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Activation、scope 与 immutable inputs

本PLAN只有Orchestrator创建activation commit后才可执行。Activation必须是
`102c625eb73cf49d7e14af12663f967397e28fa2`的direct child，subject和exact三路径
必须与machine row一致；commit后worktree/stage/untracked均为空。不得在同一activation
commit内预写其自身SHA，也不得为填充SHA而第二次修改PLAN。

Executer preflight从clean current HEAD读取full SHA，作为implementation commit的runtime
parent；随后必须证明该HEAD的parent、subject与exact changed paths逐项匹配machine row冻结的
activation object。任一不匹配在code edit与test前fail closed。该runtime HEAD只作为
implementation direct-parent identity，不增加新的授权或可变PLAN输入。

Executer只可写machine row的exact两个code/test paths。不得修改现有 preparation、
provenance I/O、machine-contract、validator、release、runner、docs、skill、wrapper或plan
owner。旧external controllers、roots、evidence及retained R3全部read/stat/list/execute/
import/repair/reuse/delete `0`。

## 2. 新 owner 的职责与禁止边界

新增`p7_retained_r3_controller_conformance.py`必须是pure in-memory owner。它以repo
现有accepted classes为schema source，使用`dataclasses.fields`取得current field tuples，
同时与machine row冻结tuple exact比较；任何新增、缺失、重排或类型owner漂移均fail
closed。只允许`MachineContractEvidence.to_mapping`与`SealTargetIdentity.as_mapping`两个
冻结public methods。内部validated seal gate只能opaque传递，不得反射或读取其属性。

Public API须保持最小且exact覆盖以下能力：

1. stable-code exception；
2. immutable conformance requirements/report types；
3. runtime controller AST analyzer；
4. pure-in-memory root identity-chain validator；
5. injected-callback lifecycle requirements/result types及executor。

具体public名字可由Executer在上述单一owner内选择，但dedicated test必须冻结`__all__`
exact集合，禁止出现manifest、validator、eligibility、release、network、device、camera、
Ray、strip、formal或scientific authority。

Runtime analyzer每次只接受一份runtime `bytes`并独立UTF-8 decode/AST parse/compile。
Negative fixture必须由独立调用、独立AST、独立result/error对象验证，禁止拼接、嵌入或
以whole-module text count参与runtime acceptance。Analyzer须将accepted owner-call的
direct assignment绑定到exact return type，枚举该name的attribute use；unknown field、
unbound result、alias escape、dynamic `getattr`、`vars`、`__dict__`或reflection全部拒绝。
`GitLedger.exit_code`是唯一process success field；runtime `returncode`必须拒绝。

所有`read_exact_file` runtime calls必须显式使用同一live `DirectoryIdentity` assigned
name作为`root=`；缺失root、literal root、不同root name或alias均拒绝。Pure-memory chain
validator须证明pre/post root全等、每个`FileIdentity.root`全等、path为exact direct child，
并在device、inode、mode和sibling/escape drift上fail closed；不得自己lstat/open/read。

Lifecycle executor只组合injected callbacks。Conformance必须先于任何effect callback；
success exact顺序为machine row。任一primary phase失败后terminal与terminal seal各最多
一次；seal成功才可admission一次，admission后重新抛原primary；seal失败则admission为0。
不得实现retry、fallback、第二root/process或任何实际I/O。

## 3. Dedicated regression surface

Dedicated test exact `14` methods，至少覆盖：

1. 九个accepted owner schemas与两个public methods exact；
2. `GitLedger.exit_code` runtime-positive；
3. isolated `GitLedger.returncode` negative被拒且不污染positive report；
4. unknown attribute及unbound owner result拒绝；
5. alias、`getattr`、`vars`、`__dict__`、reflection拒绝；
6. root-bound `read_exact_file` positive；
7. rootless/literal/different-root AST negatives；
8. exact pre/read/post in-memory identity-chain positive；
9. device/inode/mode/sibling/escape in-memory negatives；
10. success lifecycle exact ordering/counts；
11. conformance/activation/root/input/evaluate各phase failure ordering；
12. terminal或seal failure阻止admission；
13. valid FAIL admission后保留原primary exception identity；
14. source/bytecode静态证明无forbidden I/O/import、无validator/release/science authority，
    并冻结exact public exports。

先跑targeted exact `14/14`，再跑focused全部通过，再运行compileall，再运行一次quiet
unbuffered full suite。当前baseline为`741`，新增exact 14 methods后必须为`755/755`；若
discovery count不是755，不得以“all pass”替代，须停下报告Planner。最后运行
`codegraph sync`与`git diff --check`。所有命令、exit、count、source/test SHA写入ER。

## 4. Commit、acceptance 与 stop

验证全部通过后只stage exact两个write paths，创建一个direct-child implementation commit，
subject exact `feat(p7): add retained controller conformance owner`。Commit前后均核对exact
paths；不得amend其他commit，不得push。Commit后focused tests再跑一次，计入第四次test
invocation，必须通过；在ER handoff前worktree/stage/untracked必须为空。

Acceptance要求：exact两路径、14/14 targeted、focused pass、compileall pass、755/755 full、
postcommit focused pass、CodeGraph sync、diff check、single commit与clean tree全部成立；
static ownership和所有zero budgets成立。Executer最后仅向ER追加一次handoff，最终
porcelain只允许`.agent-work/EXECUTION_RESULT.md`一个unstaged modification，stage与
untracked必须为空，然后停在Planner门。

P4成功也不授权external qualification、retained reads、real B2、manifest、canonical
validator、eligibility、release、网络或设备工作。后续integration必须由Planner另写新PLAN。

维护性判断：这是反复external controller漂移后的最小 enabling refactor；新模块只拥有
pure-in-memory conformance/composition，复用既有I/O与preparation owners，不建立平行
validator/release/scientific owner。14个dedicated regression methods和full suite保护边界。
