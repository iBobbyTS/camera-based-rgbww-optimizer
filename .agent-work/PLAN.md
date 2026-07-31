# REF-P7-25-R2-B2-P4-I1：repo-owner fresh synthetic integration qualification

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-I1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-REPO-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation
commit；activation后，Executer创建并运行唯一fresh external controller，在一个fresh root内只用
synthetic inputs证明accepted repo-owned conformance/composition owner可与现有provenance I/O和
terminal-seal owners正确集成。不得读取retained R3，不得进入real B2。

**唯一 Planner stop：**
`B2_P4_I1_REPO_OWNER_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1137-p7-retained-r3-b2-p4-v1-final-source-validation-review.md`。
bytes `6750`，SHA-256
`b65877571b2a57439f966d13b0519961b6c4d2dd9b7aeeb5c9ae664bea842b24`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_i1_repo_owner_fresh_synthetic_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-P4-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-REPO-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"c89b2914af44eb3d10f4dc8b347340d86abc5756","expected_subject":"chore(plan): activate p4 repo-owner integration qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1137-p7-retained-r3-b2-p4-v1-final-source-validation-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-REPO-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_owner":{"implementation_commit":"83bb193259fcf1de5b3f78798001e83496c2daae","source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"52fcdc73c69e367cd1b046b52d83ffc555a6d496","source_sha256":"94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"28a58c6051de378fbcc6485c316df9ff10d3a90c","test_sha256":"447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726","dedicated_test_methods":14,"final_full_tests":755,"final_full_evidence_commit":"c89b2914af44eb3d10f4dc8b347340d86abc5756"},"fresh_paths":{"controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-controller-c89b291.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-qualification-c89b291","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"runtime_source_analyzed_by_repo_owner_before_effect_callbacks":true,"negative_fixture_ast_domains_disjoint":true,"activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"synthetic_input_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json"],"all_reads_use_same_live_root_identity":true,"pre_post_root_identity_exact":true,"semantic_matrix_cases":16,"qualification_files":["integration-qualification.json","integration-qualification.sha256.json"],"terminal_files":["terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"lifecycle_semantics":{"conformance_is_pre_effect_gate":true,"conformance_failure_effect_attempts":0,"conformance_failure_terminal_attempts":0,"sealed_primary_phases":["activation","root","inputs","evaluate"],"sealed_primary_failure_terminal_attempts":1,"terminal_success_seal_attempts":1,"seal_success_admission_attempts":1,"valid_fail_admission_preserves_primary_error":true,"success_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"]},"execution_budgets":{"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"read_only_git_invocations":6,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"old_controller_reads":0,"old_root_reads":0,"old_evidence_reads":0,"accepted_c1_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_I1_REPO_OWNER_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、immutable owner 与 fresh-path gate

只有Orchestrator更新FULL并创建machine row冻结的activation commit后，Executer才可执行。
Activation必须是`c89b2914af44eb3d10f4dc8b347340d86abc5756`的direct child，subject与
exact三路径逐项相等，且activation后worktree/stage/untracked均为空。Executer不得修改PLAN、
FULL、archive、debug、GUIDE或RESEARCH。

Preflight先只读证明：current activation topology exact；implementation commit/parent/subject/
exact two paths保持accepted topology；current owner/test blobs、SHA与exact14 methods不漂移；
current FULL exact one active task/contract且retained status仍未验证未消费。任一不符时controller
source/root/process均为`0`，只append一次FAIL handoff后停下。

Frozen controller source和output root在开始时都必须完全不存在。已存在、symlink、wrong parent、
wrong filesystem object或mode drift均fail closed；禁止删、覆写、复用或改名。Source须exclusive创建
一次、physical mode exact `0600`，由accepted provenance owner exact读取一次并冻结bytes/SHA/device/
inode/mode；不得二读补hash。Root只可由`create_exclusive_root`创建一次，mode exact `0700`。

## 2. Runtime source and owner integration

唯一controller source必须是一个runtime domain；negative fixture只能以独立`bytes`值交给
`analyze_controller_source`的独立调用，不能拼入、exec或用whole-source字符串计数影响runtime
acceptance。外层launcher向controller注入首次source `FileIdentity`，在同一唯一Python process中
strict UTF-8、AST parse、builtin compile并dispatch。不得生成第二source、wrapper、child process或
alternate controller。

Lifecycle的`conformance` callback首先对实际dispatched source bytes调用accepted
`analyze_controller_source`。Runtime source须将所有owner calls direct-bind到单一name；六个
`run_read_only_git` results只能读取`exit_code/stdout/stderr`等accepted fields，`returncode` usage
exact `0`；所有`read_exact_file` calls必须显式使用同一个由`create_exclusive_root` direct assignment
产生的live `DirectoryIdentity` name作为`root=`。Analyzer未通过时是pre-effect failure：Git、root、
inputs、terminal、seal、admission全部attempt `0`，外层只把原stable code append到ER后停止。

Conformance通过后，activation callback运行exact六个allowlisted read-only Git owner calls，逐个要求
exact `GitLedger` type、`exit_code==0`、empty stderr和consistent current activation identity。
不得把这些calls扩张为retained/Git provenance replay。Root callback创建唯一fresh root。

Inputs callback只在fresh root写四个canonical synthetic JSON direct children，名字exact为machine
row；每个只含固定synthetic schema/id/hash/link字段，不得复制或推断retained、C1、candidate、release
payload。随后各由accepted `read_exact_file(..., root=root)` exact读取一次，logical JSON strict
decode；root在reads前后各由owner取得live identity，构造`RootIdentityChain`并要求
`validate_root_identity_chain` exact通过。不得读取accepted C1、retained R3或任何旧external root。

## 3. Exact 16-case evaluate matrix

Evaluate callback在内存中运行exact `16/16` cases，并把每个case id/status/stable code写入唯一
qualification payload：

1. actual runtime source analyzer positive；
2. isolated `GitLedger.exit_code` positive；
3. isolated `GitLedger.returncode` negative；
4. isolated unknown owner attribute negative；
5. isolated reflection/alias negative；
6. isolated rootless read negative；
7. isolated literal-root read negative；
8. isolated different-live-root read negative；
9. actual four-file root identity chain positive；
10. pre/post root drift negative；
11. file-root mismatch negative；
12. non-direct-child/sibling escape negative；
13. file device drift negative；
14. file mode drift negative；
15. in-memory primary-failure lifecycle preserves original exception after valid admission；
16. terminal/seal failure blocks admission。

每个negative必须匹配owner的exact stable code或exact exception identity；不能只断言“raised”。Matrix
外不运行额外case、test suite、count probe或manual fix。任一case不通过即是sealed primary failure，
不得retry/fallback。

## 4. Qualification, terminal lifecycle and admission

只有matrix `16/16`后才依次exclusive写：

1. `integration-qualification.json`及其`integration-qualification.sha256.json`；
2. `terminal-evidence.json`及其`terminal-evidence.sha256.json`；
3. seal验证成功后exact一次`execution-result-admission.json`。

所有artifact必须canonical JSON、mode `0600`、同一root direct child，并记录path/bytes/SHA/device/
inode/mode/root identity。Terminal target必须exact绑定qualification identity；terminal seal必须exact
绑定terminal identity；`validate_terminal_seal`返回的opaque gate不得被反射/序列化/读取属性，只能
传给一次admission callback。

Lifecycle语义是强制合同：conformance是pre-effect gate，失败时后续attempt全0；conformance成功后
仅`activation/root/inputs/evaluate`是sealed primary phases。Primary失败后terminal exact尝试1次；
terminal成功后seal exact尝试1次；seal成功后admission exact尝试1次；有效FAIL admission后仍重新
抛原primary。Success exact顺序为machine row，不得retry、fallback、第二root/process。

Process terminal后独立核对root中只能出现machine row列出的4 inputs、2 qualification artifacts、
2 terminal artifacts和1 admission artifact，共exact `9` files；所有strict parse/linkage/hash均通过。
Executer最后只append一次ER，记录source/root identities、six Git ledgers、16 cases、artifact identities、
lifecycle order/counters、process exit与全部zero budgets。最终porcelain只允许ER一个unstaged修改；
stage与untracked为空。

## 5. Acceptance and hard locks

Acceptance要求：accepted owner identity不漂移；唯一source/root/process；runtime analyzer对实际source
通过且negative fixtures分域；Git exact `6/6`；synthetic reads/root-chain exact；matrix `16/16`；
qualification/terminal/seal/admission exact links和physical identities全部通过；process exit `0`；
retry/fallback `0`；仅ER append。

本包通过也只证明repo owner可用于fresh synthetic external integration，不证明retained R3、real B2、
manifest或canonical eligibility。Accepted C1与retained reads、Git provenance replay、real B2、
subordinate manifest、canonical validator、eligibility、retained audit、全部release、network、device、
camera、Ray、strip、FORMAL、public analyzer、TD-C、sentinel及P8继续hard locked `0`。Planner验收并由
Orchestrator另行更新FULL之前不得进入任何下一阶段。

维护性判断：本包复用已验收的repo-owned conformance、preparation与provenance I/O owners，只增加
一次外置synthetic integration evidence，不新增repo代码或平行owner；职责边界保持清晰。
