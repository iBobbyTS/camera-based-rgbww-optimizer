# REF-P7-25-R2-B2-P4-I1-C1：alias-safe fresh synthetic integration correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-I1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-ALIAS-SAFE-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation commit；
activation后，Executer创建并运行唯一fresh external controller，以accepted repo owner对最终runtime source
执行pre-effect conformance，并用direct/nonlocal live bindings及plain-projection state完成synthetic integration
qualification。不得读取或修复失败P4-I1 source/root，不得读取retained R3，不得进入real B2。

**唯一 Planner stop：**
`B2_P4_I1_C1_ALIAS_SAFE_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1232-p7-retained-r3-b2-p4-i1-owner-alias-failure-review.md`。
bytes `9294`，SHA-256
`92b16d030788cec2f85002465d659316fa4b375ece63ba8defbb24504ed46ba9`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_i1_c1_alias_safe_fresh_synthetic_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-P4-I1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-ALIAS-SAFE-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"f1b64db91365baf1980f6150be9b03350565136f","expected_subject":"chore(plan): activate p4 alias-safe integration qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1232-p7-retained-r3-b2-p4-i1-owner-alias-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-I1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-I1-C1-ALIAS-SAFE-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_owner":{"implementation_commit":"83bb193259fcf1de5b3f78798001e83496c2daae","implementation_parent":"5f2483c319b395b2aef2a43f4827b4c150f3f3fd","implementation_subject":"feat(p7): add retained controller conformance owner","source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"52fcdc73c69e367cd1b046b52d83ffc555a6d496","source_sha256":"94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"28a58c6051de378fbcc6485c316df9ff10d3a90c","test_sha256":"447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726","dedicated_test_methods":14,"final_full_tests":755,"final_full_evidence_commit":"c89b2914af44eb3d10f4dc8b347340d86abc5756"},"reviewed_failure":{"evidence_commit":"d822b2303072a7179ecd1f3ff245b2cacdece80a","debug_commit":"f1b64db91365baf1980f6150be9b03350565136f","stable_code":"owner_alias_escape","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-controller-c89b291.py","source_bytes":20586,"source_sha256":"8c4cb131ed97bc38f5ff72947000d3b7932574759483b4172cd9fbfd992ea904","source_mode":"0600","source_device":16777240,"source_inode":2224706,"processes":1,"exit_code":1,"conformance_attempts":1,"effect_attempts":0,"root_absent":true,"immutable_no_read":true},"fresh_paths":{"controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-controller-f1b64db.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-qualification-f1b64db","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_owner_analysis_before_effects":true,"owner_call_result_direct_binding_only":true,"plain_projection_transport_ast_assertion":true,"cross_callback_live_transport":"explicit_nonlocal_direct_names","mutable_state_plain_projections_only":true,"callback_returns_plain_projections_only":true,"live_owner_object_container_writes":0,"live_owner_alias_assignments":0,"opaque_gate_container_writes":0,"negative_fixture_ast_domains_disjoint":true,"activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"synthetic_input_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json"],"all_reads_use_same_direct_live_root_name":true,"pre_post_root_identity_exact":true,"semantic_matrix_cases":16,"qualification_files":["integration-qualification.json","integration-qualification.sha256.json"],"terminal_files":["terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"lifecycle_semantics":{"conformance_is_pre_effect_gate":true,"conformance_failure_effect_attempts":0,"conformance_failure_terminal_attempts":0,"sealed_primary_phases":["activation","root","inputs","evaluate"],"sealed_primary_failure_terminal_attempts":1,"terminal_success_seal_attempts":1,"seal_success_admission_attempts":1,"valid_fail_admission_preserves_primary_error":true,"success_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"]},"execution_budgets":{"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"read_only_git_invocations":6,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"failed_controller_reads":0,"failed_root_reads":0,"old_controller_reads":0,"old_root_reads":0,"old_evidence_reads":0,"accepted_c1_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_I1_C1_ALIAS_SAFE_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、immutable owner 与 fresh-path gate

只有Orchestrator更新FULL并创建machine row冻结的activation commit后，Executer才可执行。Activation必须
是`f1b64db91365baf1980f6150be9b03350565136f`的direct child，subject与exact三路径逐项相等，
且activation后worktree/stage/untracked均为空。Executer不得修改PLAN、FULL、archive、debug、GUIDE、
RESEARCH、code或test。

Unique process的activation callback用accepted `run_read_only_git` exact六次证明current activation
topology、exact changed paths、initial clean worktree以及accepted implementation/source/test identities；每个
result direct-bind到不同name，要求exact `GitLedger`、`exit_code==0`、empty stderr。不得用`returncode`，
不得通过tuple/list/dict/object field或第二variable保存live ledger；mutable state只能保存由allowlisted fields
即时构造的plain argv/exit/stdout-hash projections。任一不符按sealed primary failure处理，且root/inputs/
matrix为零。

失败P4-I1 source/root及一切旧external source/root/evidence禁止读取、lstat、hash、repair、delete、rename、
reuse或rerun。其identity只可从active PLAN machine row记录进handoff。新的controller source和output root
在开始时必须完全不存在；已存在、symlink、wrong parent、wrong object或mode drift均fail closed，不得删除
或覆盖。

Fresh source须exclusive创建一次、mode exact `0600`，由accepted provenance owner exact读取一次并冻结
bytes/SHA/device/inode/mode。外层launcher不得二读补hash；同一in-memory `FileIdentity.data`在唯一process内
strict UTF-8 decode、AST parse、builtin compile并dispatch。Root只由`create_exclusive_root`创建一次、mode
exact `0700`，其return value direct-bind到唯一explicit live name。

## 2. Alias-safe runtime source boundary

Actual runtime source是唯一positive domain。Lifecycle `conformance` callback必须首先对exact dispatched
in-memory source bytes调用accepted `analyze_controller_source`；通过前activation Git、root、inputs、
evaluate、terminal、seal及admission attempts全部为 `0`。Report须证明：

- 每个`create_exclusive_root`、`read_exact_file`、`run_read_only_git`及其它accepted owner call都由simple
  assignment直接绑定到唯一name；无owner result unbound、rebound或alias assignment；
- 所有`read_exact_file(..., root=...)`都显式引用同一个由`create_exclusive_root` direct assignment产生的
  live `DirectoryIdentity` name；
- owner attribute accesses只使用accepted fields/public methods，`returncode`、reflection、unknown attribute、
  opaque gate introspection均为零；
- actual source自身通过strict parse/compile，且report SHA与首次source `FileIdentity.sha256` exact相等。

Accepted report之后、任何effect之前，再对同一个already-parsed actual AST执行bounded transport assertion：
report列出的bound/opaque names不能作为container constructor/mutator argument、subscript/attribute assignment
value、callback return value或普通call argument。只允许owner-field attribute projection、shared `root=` live
name、`RootIdentityChain`的exact before/files/after immutable composition，以及opaque gate原name传给
admission。该assertion只冻结本external source的composition形状，不复制owner schema/method判断；失败仍
属于conformance pre-effect failure。

跨callback需要的live `DirectoryIdentity`、`FileIdentity`、qualification/terminal identities及opaque terminal
gate必须保留在明确的enclosing direct names中；赋值callback使用显式`nonlocal`后仍将owner call直接赋给
该唯一name。禁止把live object放入dict/list/set/tuple、object attribute、closure factory return、callback
return或另一变量。Callback传给lifecycle result的返回值只可为plain projection。

唯一mutable projection state只可含str/int/bool/None以及由allowlisted owner fields立即构造的plain
tuple/list/dict；不得含owner dataclass、opaque gate、memoryview、callable、exception或任何live identity。
在conformance callback内须对state初值做递归plain-type断言；每次callback写入后重复断言，terminal payload
也记录`live_owner_container_writes=0`与`owner_alias_assignments=0`。

Negative fixtures必须作为独立`bytes`值分别交给accepted analyzer，不能exec、import、拼接到actual source，
也不能用whole-source substring/occurrence counting影响actual positive。Fixture中的owner calls只存在于其独立
AST domain；actual positive report的bindings/attributes/root_reads单独冻结。

## 3. Root, inputs and exact 16-case matrix

Conformance通过后activation运行exact六个Git owner calls；随后root callback创建唯一fresh root。Inputs
callback在该root写四个canonical synthetic JSON direct children，名字exact为machine row。Payload只含固定
synthetic schema/id/hash/link fields，不得复制或推断retained、accepted C1、candidate或release payload。

四个files各由accepted `read_exact_file(..., root=<same direct live root name>)` exact读取一次，每个result
direct-bind到不同live name。Root在reads前后取得的identity都必须保持direct names；构造
`RootIdentityChain`后由`validate_root_identity_chain` exact通过。只有allowlisted identity fields的plain
projections可进入mutable state；live file/root objects仅由其direct/nonlocal names持有。

Evaluate callback运行exact `16/16` cases，并冻结每个case id/status/stable code：

1. actual dispatched runtime source analyzer positive，SHA与首次source identity一致；
2. isolated `GitLedger.exit_code` positive；
3. isolated `GitLedger.returncode` negative → `git_returncode_rejected`；
4. isolated unknown owner attribute/unbound result negative；
5. isolated owner alias/reflection/opaque introspection negative；
6. isolated rootless read negative；
7. isolated literal-root read negative；
8. isolated different-live-root read negative；
9. actual four-file root identity chain positive；
10. pre/post root drift negative → `root_identity_drift`；
11. file-root mismatch negative → `file_root_mismatch`；
12. non-direct-child/sibling escape negative → `file_not_direct_child`；
13. file device drift negative → `file_device_mismatch`；
14. file mode drift negative → `file_mode_mismatch`；
15. in-memory primary-failure lifecycle完成valid admission后保持original exception identity；
16. terminal/seal failure阻止admission并返回accepted stable lifecycle code。

每个negative须匹配exact stable code或exact exception identity，不能只断言raised。Root-negative cases只用
already-held identities及pure in-memory replacement，不得额外lstat、create/read owner root。Matrix外不得运行
额外case、test suite、count probe、manual source fix或second analyzer domain。任一case失败即sealed primary
failure，retry/fallback均为零。

## 4. Qualification, terminal lifecycle and admission

Matrix `16/16`后才依次exclusive写：

1. `integration-qualification.json`及`integration-qualification.sha256.json`；
2. `terminal-evidence.json`及`terminal-evidence.sha256.json`；
3. seal验证成功后exact一次`execution-result-admission.json`。

所有artifact必须canonical JSON、mode `0600`、同一root direct child，记录path/bytes/SHA/device/inode/
mode/root identity。Qualification须包含actual source conformance report、六个Git plain projections、四个input
plain projections、root chain、16 cases、direct/nonlocal transport assertions和全部counter。Terminal target
exact绑定qualification identity；terminal seal exact绑定terminal identity。

`validate_terminal_seal`的opaque gate direct-bind到一个明确nonlocal name；禁止反射、序列化、属性读取、
存入mutable state或alias，只能原name传给一次admission callback。Admission完成后也不得把gate写入ER；
ER只记录admission artifact的physical/plain identity。

Lifecycle语义保持：conformance是pre-effect gate，失败时后续attempt全零；conformance成功后仅
`activation/root/inputs/evaluate`是sealed primary phases。Primary failure后terminal attempt exact `1`；
terminal成功后seal exact `1`；seal成功后admission exact `1`；有效FAIL admission后仍重新抛原primary。
Success顺序exact为machine row。Process terminal后独立核对root中只能有4 inputs、2 qualification、2 terminal
与1 admission共exact `9` files；所有strict JSON/hash/linkage/root identities通过。

Executer最后只append一次ER，记录source/root identities、actual analyzer report、direct binding names、plain
state type audit、six Git projections、16 cases、artifact identities、lifecycle order/counters、process exit及所有
zero budgets。最终porcelain只允许ER一个unstaged modification；stage与untracked为空。

## 5. Acceptance and hard locks

Acceptance要求：accepted owner identity不漂移；唯一fresh source/root/process；actual final source在effects前
通过owner analyzer；owner calls direct-bound、跨callback仅explicit nonlocal direct names、mutable state与
callback returns均为plain projections；live owner/opaque container writes和aliases exact `0`；negative fixtures
分域；Git `6/6`；synthetic reads/root chain exact；matrix `16/16`；qualification/terminal/seal/admission links与
physical identities全部通过；root exact 9 files；process exit `0`；retry/fallback `0`；仅ER append。

本包通过也只证明repo owner可完成alias-safe fresh synthetic external integration，不证明retained R3、real
B2、manifest或canonical eligibility。失败P4-I1 source/root、其它旧controller/root/evidence、accepted C1、
retained reads、Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained
audit、全部release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、
FORMAL、public analyzer、TD-C、sentinel、P8、firmware及deployment继续hard locked `0`。Planner验收并由
Orchestrator更新FULL之前不得进入下一阶段。

维护性判断：本包不修改repo owner或新增抽象，只纠正外置controller的ownership transport。Direct live
names、plain projection state及原16-case matrix把owner/lifecycle边界显式化，复杂度局限在一次性synthetic
integration source内，无需架构重构。
