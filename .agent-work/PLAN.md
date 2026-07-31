# REF-P7-25-R2-B2-P4-I1-C1-C1：field-only fresh synthetic integration correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-I1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-C1-FIELD-ONLY-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation commit；activation
后，Executer创建并运行唯一fresh external controller。Final source必须先通过accepted repo analyzer，再通过
bounded field-transport gate；只有两个pre-effect gates都通过后，才可执行原synthetic Git/root/inputs/
16-case/lifecycle qualification。不得读取或修复失败P4-I1-C1 source/root，不得读取retained R3或进入real B2。

**唯一 Planner stop：**
`B2_P4_I1_C1_C1_FIELD_ONLY_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1252-p7-retained-r3-b2-p4-i1-c1-transport-failure-review.md`，bytes `8654`，
SHA-256 `b6a15ca203f9f79188c200ac0b20c4b2e638c6d2b82a781afe8ca644882bcf54`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_i1_c1_c1_field_only_fresh_synthetic_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-P4-I1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-C1-FIELD-ONLY-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"972f82465fa5d9671dba12a0570103bd1b9fb6af","expected_subject":"chore(plan): activate p4 field-only transport correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1252-p7-retained-r3-b2-p4-i1-c1-transport-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-I1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-C1-FIELD-ONLY-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_owner":{"implementation_commit":"83bb193259fcf1de5b3f78798001e83496c2daae","implementation_parent":"5f2483c319b395b2aef2a43f4827b4c150f3f3fd","implementation_subject":"feat(p7): add retained controller conformance owner","source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"52fcdc73c69e367cd1b046b52d83ffc555a6d496","source_sha256":"94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"28a58c6051de378fbcc6485c316df9ff10d3a90c","test_sha256":"447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726","dedicated_test_methods":14,"final_full_tests":755,"final_full_evidence_commit":"c89b2914af44eb3d10f4dc8b347340d86abc5756"},"reviewed_failure":{"activation_commit":"30e913d96d7485de64548dfbeff0f2e47619e903","evidence_commit":"0fd144ab2749ce731e36926e140b6723f7a44122","debug_commit":"972f82465fa5d9671dba12a0570103bd1b9fb6af","stable_code":"live_owner_container_write","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-controller-f1b64db.py","source_bytes":33510,"source_sha256":"de2038f4d520febb0984e6b8ff6a73c293a46503ee1d6f07118036343aff2f29","source_mode":"0600","source_device":16777240,"source_inode":2225015,"processes":1,"exit_code":1,"accepted_analyzer_attempts":1,"accepted_analyzer_bound_results":18,"transport_gate_attempts":1,"transport_gate_occurrences":16,"effect_attempts":0,"root_absent":true,"immutable_no_read":true},"fresh_paths":{"controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-c1-controller-972f824.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-c1-qualification-972f824","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_owner_analysis_before_effects":true,"expected_bound_results":18,"bounded_transport_gate_after_owner_analysis_before_effects":true,"owner_call_result_direct_binding_only":true,"cross_callback_live_transport":"explicit_nonlocal_direct_names","git_ledger_checks_unrolled":6,"git_ledger_field_projections_unrolled":6,"input_identity_field_projections_unrolled":4,"artifact_identity_field_projections_unrolled":9,"generic_live_projection_helper_calls":0,"live_owner_artifact_collections":0,"live_owner_object_container_writes":0,"live_owner_alias_assignments":0,"opaque_gate_container_writes":0,"transport_exact_identity_composition":{"constructor":"RootIdentityChain","fields":["before","files","after"],"immutable":true,"validator":"validate_root_identity_chain"},"transport_exact_seal_calls":{"target_identity_direct":true,"validate_terminal_seal_direct":true,"opaque_gate_original_name_to_admission_only":true},"mutable_state_plain_projections_only":true,"callback_returns_plain_projections_only":true,"negative_fixture_ast_domains_disjoint":true,"activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"synthetic_input_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json"],"all_reads_use_same_direct_live_root_name":true,"pre_post_root_identity_exact":true,"semantic_matrix_cases":16,"qualification_files":["integration-qualification.json","integration-qualification.sha256.json"],"terminal_files":["terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"lifecycle_semantics":{"conformance_is_pre_effect_gate":true,"owner_analysis_precedes_transport_gate":true,"gate_failure_effect_attempts":0,"gate_failure_terminal_attempts":0,"sealed_primary_phases":["activation","root","inputs","evaluate"],"sealed_primary_failure_terminal_attempts":1,"terminal_success_seal_attempts":1,"seal_success_admission_attempts":1,"valid_fail_admission_preserves_primary_error":true,"success_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"]},"execution_budgets":{"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"read_only_git_invocations":6,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"failed_controller_reads":0,"failed_root_reads":0,"old_controller_reads":0,"old_root_reads":0,"old_evidence_reads":0,"accepted_c1_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_I1_C1_C1_FIELD_ONLY_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Frozen activation and source ownership

Orchestrator activation必须以current clean HEAD
`972f82465fa5d9671dba12a0570103bd1b9fb6af`为direct parent，subject exact为machine row，changed paths
exact为FULL、PLAN与本轮review archive。Activation后worktree必须clean；FULL必须只有本task/contract active，
保留candidate hash与retained状态，并显式记录Orchestrator verification、Executer dispatch true及device
authorization false。任一preflight不匹配即stop，不得创建external source/root。

Fresh source/root必须先确认均absent。Source exclusive创建一次、mode `0600`，由accepted provenance owner exact
读取一次；同一首次 `FileIdentity.data`完成strict UTF-8 decode、AST parse、builtin compile与唯一process
dispatch。Outer launcher不得二读补hash或修复source。Root只由accepted `create_exclusive_root`创建一次、mode
`0700`，return value direct-bind唯一live name。

## 2. Two exact pre-effect gates

Lifecycle `conformance` callback先对exact dispatched in-memory source运行accepted
`analyze_controller_source`。报告须PASS并冻结exact `18` bound results、source SHA、owner fields/methods、attribute
uses与root reads；所有owner call results unique direct-bound，shared root reads引用同一direct root name，
`returncode`、reflection、unknown attributes、unbound/alias results与opaque introspection均为零。

Accepted analyzer通过后，对same already-parsed AST运行bounded transport gate；两个gate通过前Git/root/inputs/
evaluate/terminal/seal/admission attempts必须全零。Transport gate必须证明：

- 六个 `run_read_only_git` calls、success checks与plain dict projections逐项展开；不得用tuple/list/comprehension/
  loop收集或运输live ledger；
- 每个input与artifact identity direct binding后，在同一callback中以explicit accepted fields立即构造plain dict；
  不得先放入collection，不得传入`projection(identity)`或任何generic helper；
- 除exact owner-required形状外，bound live name不得成为普通call argument、container constructor/mutator
  argument、subscript/attribute assignment value、callback return、closure return或second alias；
- 唯一identity grouping exception是immutable
  `RootIdentityChain(before=<direct root>, files=(<direct files>...), after=<direct root>)`及其direct
  `validate_root_identity_chain` call；必须按callee和named field exact匹配，不得实现generic path/call allowlist；
- seal阶段只允许repo-required target identity direct construction/use、`validate_terminal_seal`的exact direct call，
  以及其opaque gate原name传给唯一admission callback；opaque gate不可introspect、serialize、alias或进入container；
- 跨callback live owner仅保留在explicit enclosing direct names并用`nonlocal`直接赋值；mutable state与callback
  returns只能含递归plain projection。每次state写入后都运行recursive plain-type assertion。

Negative fixtures是independent bytes/AST domains，只交给各自analyzer/gate调用；不得exec、拼接actual source或
参与actual whole-source occurrence counting。任一gate失败即pre-effect hard failure，terminal attempts仍为零；
controller exit非零并保留source immutable，retry/fallback/第二source/root/process为零。

## 3. Effects and exact 16-case matrix

两个gate通过后activation才运行exact六个read-only Git owner calls。每个ledger以`exit_code == 0`与empty
stderr独立验证，并立即写入只含argv/cwd/exit_code/stdout/stderr hashes的plain dict；六个dict可随后组成plain
list。Root callback创建唯一fresh root。Inputs callback写四个canonical synthetic JSON direct children，payload
仅含固定synthetic schema/id/hash/link fields，不复制或推断retained、accepted C1、candidate或release payload。

四个files各由accepted `read_exact_file(..., root=<same direct live root name>)` exact读取一次。每个identity逐项
验证并立即inline field-project。Reads前后root identities保持direct names；exact immutable
`RootIdentityChain(before, files, after)`由repo validator通过。不得额外lstat/read/count probe。

Evaluate callback运行原exact `16/16` cases并冻结case id/status/stable code：

1. actual dispatched source analyzer positive、18 bindings及SHA exact；
2. isolated `GitLedger.exit_code` positive；
3. isolated `GitLedger.returncode` negative → `git_returncode_rejected`；
4. isolated unknown owner attribute/unbound result negative；
5. isolated alias/reflection/opaque introspection negative；
6. isolated rootless read negative；
7. isolated literal-root read negative；
8. isolated different-live-root read negative；
9. actual four-file root identity chain positive；
10. pre/post root drift negative → `root_identity_drift`；
11. file-root mismatch negative → `file_root_mismatch`；
12. non-direct-child/sibling escape negative → `file_not_direct_child`；
13. file device drift negative → `file_device_mismatch`；
14. file mode drift negative → `file_mode_mismatch`；
15. in-memory primary-failure lifecycle在valid admission后保持original exception identity；
16. terminal/seal failure阻止admission并返回accepted stable lifecycle code。

每个negative匹配exact stable code或exception identity，不能只断言raised。Root negatives仅用already-held
identities与pure in-memory replacement，不额外调用I/O owner。Matrix外不得加case、test suite、count probe、
manual source fix或second analyzer domain。任一case失败即sealed primary failure，retry/fallback为零。

## 4. Qualification, terminal seal and ER admission

Matrix `16/16`后才exclusive写：四个inputs既有文件之外，
`integration-qualification.json`及其seal、`terminal-evidence.json`及其seal、最后
`execution-result-admission.json`，root总数exact `9`。所有文件canonical JSON、mode `0600`、同一root direct
children，记录path/bytes/SHA/device/inode/mode/root identity。Qualification记录两个gate报告、unrolled six Git
plain projections、four input projections、root chain、16 cases、field-only transport assertions及全部counter。

Terminal target exact绑定qualification identity；terminal seal exact绑定terminal identity。Opaque gate direct
bind唯一nonlocal name且只传给exact一次admission callback。Admission后不把gate写入ER，只记录admission
artifact plain physical identity。

Lifecycle success order exact为machine row。Accepted analyzer/transport failure不进入terminal；其后仅
`activation/root/inputs/evaluate`是sealed primary phases。Primary failure后terminal attempt exact `1`；terminal
成功后seal exact `1`；seal成功后admission exact `1`；valid FAIL admission后仍重新抛original primary error。

Process terminal后独立验证root exact9 files、strict JSON/hash/linkage/root identities、source/root identities、
counter与process exit `0`。Executer只append一次ER，记录actual gate reports、18 bindings、unrolled projections、
16 cases、artifact identities、lifecycle/counters及全部zero budgets。最终porcelain仅ER一个unstaged modification，
stage和untracked为空。

## 5. Acceptance, locks and stop

Acceptance要求：accepted owner identity不漂移；唯一fresh source/root/process；actual final bytes依次通过accepted
analyzer与bounded field-transport gate；18 bindings；六个Git、四个inputs、九个artifacts逐项direct binding后
inline projection；generic live projection helper、live collection/container writes、aliases与opaque writes均为
`0`；唯一RootIdentityChain/seal shape exceptions exact；negative domains分离；Git `6/6`；root chain与matrix
`16/16`；exact9 files；terminal/seal/admission全部链接；process exit `0`；retry/fallback `0`；仅ER append。

本包通过只证明repo owner可完成field-only fresh synthetic integration。失败P4-I1-C1 source/root、其它旧
controller/root/evidence、accepted C1、retained reads、Git provenance replay、real B2、subordinate manifest、
canonical validator、eligibility、retained audit、全部release、network、DNS、environment、credentials、device、
camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware及deployment继续
hard locked `0`。Planner验收并由Orchestrator更新FULL前不得进入下一阶段。

维护性判断：本包不修改repo owner或新增抽象，只把外置controller transport收敛为逐项field projection；唯一
composition例外精确对应既有RootIdentityChain与seal owners，复杂度局限在一次性synthetic source。
