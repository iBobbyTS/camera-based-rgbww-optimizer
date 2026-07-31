# REF-P7-25-R2-B2-P4-C1-C1-C1-I1：repo-owned fresh synthetic integration qualification

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-REPO-OWNED-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator 先独立审核本 PLAN、更新 FULL 并以
`fd040d45b1ba604186b4c1e092ba16ab8beed4a6` 为 direct parent 创建 exact activation commit；activation 后，
Executer 创建并运行唯一 fresh external controller/source/root/process。Controller 只调用既有 repo-owned
`analyze_controller_source`，并直接消费 `ControllerConformanceReport.transport`；禁止实现第二 AST classifier。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_I1_REPO_OWNED_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1356-p7-retained-r3-b2-p4-c1-c1-c1-synthetic-integration-activation.md`，bytes `4443`，
SHA-256 `34d52df2fb7eaae07ef1e6b0901fcaeddfb5abc111f5010fedf614d0c93237a1`。Orchestrator activation 前必须把该
exact identity 记录进 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_i1_repo_owned_fresh_synthetic_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-REPO-OWNED-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"fd040d45b1ba604186b4c1e092ba16ab8beed4a6","expected_subject":"chore(plan): activate p4 repo-owned synthetic integration","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1356-p7-retained-r3-b2-p4-c1-c1-c1-synthetic-integration-activation.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-REPO-OWNED-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_transport_owner":{"implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"1868ad4b4446defcc6d8187ea21d18ccf128fa31","source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"25eafb91d7794d4510c9d7da34f1d8666ab1ff55","test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","dedicated_test_methods":20,"targeted_tests":20,"focused_tests":76,"full_tests":761,"truthful_provenance_closure_commit":"baa14d15bfcef7463f23a1a3186741c9c9704a76","orchestrator_acceptance_commit":"fd040d45b1ba604186b4c1e092ba16ab8beed4a6"},"fresh_paths":{"activation_short_sha_source":"runtime_activation_commit_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_analyzer_calls":1,"negative_fixture_analyzer_calls":"exactly_as_required_by_semantic_matrix","external_transport_ast_classifier_calls":0,"embedded_transport_report_consumed":true,"expected_bound_results":18,"effect_transport_uses_on_pass":0,"direct_nonlocal_effect_bindings":true,"inline_plain_field_projection":true,"generic_live_projection_helper_calls":0,"live_owner_collections":0,"live_owner_container_writes":0,"live_owner_aliases":0,"exact_root_identity_chain":true,"activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"synthetic_input_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json"],"all_reads_use_same_live_root_identity":true,"pre_post_root_identity_exact":true,"semantic_matrix_cases":16,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"lifecycle_semantics":{"conformance_is_pre_effect_gate":true,"conformance_failure_effect_attempts":0,"conformance_failure_terminal_attempts":0,"sealed_primary_phases":["activation","root","inputs","evaluate"],"sealed_primary_failure_terminal_attempts":1,"terminal_success_seal_attempts":1,"seal_success_admission_attempts":1,"valid_fail_admission_preserves_primary_error":true,"success_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"]},"execution_budgets":{"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"read_only_git_invocations":6,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_C1_C1_I1_REPO_OWNED_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、fresh paths 与 one-read/one-process boundary

Orchestrator activation 必须 exact 匹配 machine row。Activation 后 worktree 必须 clean；FULL 只能有本 task/contract
active，并保持 retained/candidate 状态、Orchestrator verification、Executer dispatch true 与 device authorization false。
任一不符立即 stop，source/root/process attempts 全零。

唯一 outer preflight 读取 activation HEAD 一次并要求它是 expected activation commit；取其 full SHA 的前七位小写 hex 为
`activation_short_sha`，把 machine row 的两个 template 各替换一次，得到本轮不可变 exact source/root path，并在任何写入前记录到
controller handoff。两 path 都必须 absent，parent 必须是预期 `/Volumes/4T/temp/rgbww-optimizer`、不得 symlink/escape；任一已存在或异常即
fail closed，不得改名、删除、复用、fallback 或生成第二 path。

Source 以 `O_CREAT|O_EXCL|O_NOFOLLOW` exact 创建一次、mode `0600`；由 accepted `read_exact_file` exact读取一次。
同一首次 `FileIdentity.data` 完成 strict UTF-8 decode、AST parse、builtin compile 与唯一 process dispatch；不得二读、rewrite、repair、
template rerender 或启动第二 process。Root 只能由 accepted `create_exclusive_root` 创建一次、mode `0700`，其 live
`DirectoryIdentity` direct-bind 到唯一 name。

## 2. Single repo-owned conformance and transport report

Lifecycle `conformance` callback 对 exact dispatched bytes 调用既有 `analyze_controller_source` exact一次。不得在 external source、
launcher 或 postflight 中创建、复制、简化或补丁式实现任何 AST transport walker/classifier；不得调用 `ast.walk` 来再次判断 live transport。
External consumer 只能验证并消费返回的 immutable `ControllerConformanceReport` 与 embedded
`ControllerTransportReport` fields：

- source SHA exact，owner fields/public methods exact，bound results exact `18`；
- `transport.effect_bindings` 与 `transport.fixture_bindings` 由 repo owner 按 call provenance给出；
- pure in-memory fixture edges、exact root-chain compositions/validations 直接来自 embedded report；
- `transport.effect_transport_uses == ()`；
- actual source中的effect owner results只能unique direct binding，跨callback仅explicit enclosing direct names加`nonlocal`；
- 每个live identity direct binding后只能读取accepted fields并在同一callback inline构造plain dict；不得先进入tuple/list/dict/set、
  generic projection helper、alias、callback/closure return；plain projections之后才可组成plain containers；
- exact `RootIdentityChain(before=<direct root>, files=(<direct files>...), after=<direct root>)`及direct
  `validate_root_identity_chain` 是唯一 live grouping shape；opaque terminal gate只以原direct name传给唯一admission callback，不得反射、
  序列化、读属性、alias或入container。

Negative fixture source只作为独立`bytes`传给同一个 repo analyzer 的16-case matrix调用；不得拼入、exec或影响actual source report。
Actual conformance失败是pre-effect hard failure：Git/root/inputs/evaluate/terminal/seal/admission attempts全部为`0`，保留 source immutable，
process exit非零，retry/fallback/second source/root/process为`0`。

## 3. Git6、same-root four reads 与 exact RootIdentityChain

Conformance通过后，activation callback才调用accepted `run_read_only_git` exact六次，repo cwd exact为当前仓库，argv exact为：

1. `git rev-parse --verify <activation-full-sha>^{commit}`；
2. `git show -s --format=%H%x00%P%x00%s <activation-full-sha>`；
3. `git diff-tree --no-commit-id --name-only -r -z <activation-full-sha>`；
4. `git rev-parse <activation-full-sha>:.agent-work/FULL_PLAN_REFERENCE.md`；
5. `git rev-parse <activation-full-sha>:.agent-work/PLAN.md`；
6. `git rev-parse <activation-full-sha>:.agent-work/PLANS/20260731-1356-p7-retained-r3-b2-p4-c1-c1-c1-synthetic-integration-activation.md`。

每个 `GitLedger` direct-bind独立name，要求 exact type、`exit_code==0`、empty stderr与expected stdout；只读取 accepted fields并
inline投影为plain dict。不得使用`returncode`、live ledger collection、generic helper或扩大为 retained/Git provenance replay。

Root callback创建唯一fresh root。Inputs callback以accepted canonical writer exclusive写exact四个direct children：
`synthetic-plan.json`、`synthetic-full.json`、`synthetic-lineage.json`、`synthetic-seal.json`。Payload只含固定synthetic
schema/id/hash/link fields，不复制或推断retained、candidate、release或旧evidence payload。

四个文件各由accepted `read_exact_file(..., root=<same live root name>)` exact读取一次；每个FileIdentity逐项验证并立即
inline field-project。Reads前后root identities保持direct names，构造唯一 exact immutable
`RootIdentityChain(before=..., files=(four direct names), after=...)`并由`validate_root_identity_chain` exact一次通过。
不得额外lstat/read/count probe。

## 4. Exact 16-case semantic matrix

Evaluate callback运行exact `16/16` meaningful cases并记录case id、status与exact stable code/exception identity：

1. actual dispatched source analyzer positive：SHA、18 bindings、embedded transport report与effect transport empty exact；
2. isolated `GitLedger.exit_code` positive；
3. isolated `GitLedger.returncode` negative → `git_returncode_rejected`；
4. isolated unknown owner attribute/unbound result negative；
5. isolated alias/reflection/opaque introspection negative；
6. isolated rootless read negative；
7. isolated literal-root read negative；
8. isolated different-live-root read negative；
9. actual four-file root identity chain positive；
10. pre/post root drift negative → `root_identity_drift`；
11. pure in-memory `FileIdentity(root=drift_root)` file-root mismatch negative → `file_root_mismatch`，且repo transport report把它分类为fixture edge；
12. non-direct-child/sibling escape negative → `file_not_direct_child`；
13. file device drift negative → `file_device_mismatch`；
14. file mode drift negative → `file_mode_mismatch`；
15. in-memory primary-failure lifecycle在valid admission后保持original exception identity；
16. terminal/seal failure阻止admission并返回accepted stable lifecycle code。

每个negative必须匹配exact stable code或exact exception identity，不能只断言raised。Root negatives只用already-held identities与pure
in-memory replacements，不得额外调用I/O owner。Matrix外不得加case、test suite、count probe、manual source fix、second analyzer
owner或external classifier。任一case失败即sealed primary failure，retry/fallback为零。

## 5. Exact9 artifacts、progressive/terminal/seal/admission lifecycle

Matrix `16/16`后，root中只能按顺序出现 machine row 的exact9 names：四个inputs；
`integration-qualification.json`与`integration-qualification.sha256.json`；
`terminal-evidence.json`与`terminal-evidence.sha256.json`；最后`execution-result-admission.json`。
所有文件canonical JSON、mode `0600`、same root direct child，并记录path/bytes/SHA/device/inode/mode/root identity。

`integration-qualification.json`是progressive qualification evidence，必须包含actual conformance report、embedded transport report、
Git6 plain projections、four input projections、root chain、16 cases、lifecycle counters与全部zero budgets；其seal exact绑定qualification
physical identity。Terminal target exact绑定qualification identity，terminal seal exact绑定terminal physical identity。Opaque gate direct-bind
唯一nonlocal name并只传给exact一次admission callback；admission只记录plain physical identities，不序列化gate。

Lifecycle success order exact为machine row。Conformance失败不进入terminal；其后只有`activation/root/inputs/evaluate`是sealed primary
phases。Primary failure后terminal attempt exact`1`；terminal成功后seal exact`1`；seal成功后admission exact`1`；valid FAIL admission后仍重新抛
original primary error。Terminal或seal失败必须阻止admission并保留primary与seal failure identity。

Process terminal后只读核对exact9 names、strict JSON/hash/linkage/root identities、source/root identity、Git6、16 cases、lifecycle/counters与
exit。Executer最终只append一次`.agent-work/EXECUTION_RESULT.md`，记录exact source/root paths、source physical identity、activation full/short
SHA、repo reports、artifacts/hashes、process result与所有zero budgets；不得改旧ER。最终porcelain只能有ER一个unstaged modification，stage与
untracked必须为空。

## 6. Acceptance, failure branches, hard locks and stop

Acceptance要求：activation/owner/file identities exact；一个fresh source/root/process；source one-write/one-read；root one-create；actual runtime
source analyzer exact一次且无第二 classifier；18 bindings与embedded transport report exact、effect transport empty；direct/nonlocal live bindings、inline plain
projection、exact RootIdentityChain；Git`6/6`；same-root synthetic reads`4/4`；matrix`16/16`；exact9 artifacts；terminal/seal/admission链接与
physical identities全部通过；process exit`0`；retry/fallback`0`；仅ER append。

任何preflight/source/conformance失败：root及全部root artifacts必须absent，terminal attempts`0`。任何activation/root/inputs/evaluate失败：保留已写
progressive evidence，执行一次fail terminal/seal/admission lifecycle并重新抛primary；不得修复、删除、重用root、重跑或补造缺失artifact。任何terminal/
seal/admission失败：保留所有physical evidence与双重failure identity，exit非零。所有分支都在唯一Planner stop结束。

本包通过只证明repo-owned transport report可完成fresh synthetic integration，不自动解锁retained或real B2。所有旧失败controller/source/root/
evidence读取、retained R3/candidate、Git retained provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained
audit、全部release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、
sentinel、P8、firmware及deployment均hard locked `0`。Planner验收并由Orchestrator更新FULL前不得进入下一阶段。

维护性判断：本包不改repo code/test、不新增parallel owner；external controller只消费现有single analyzer的immutable report，并复用provenance I/O与
terminal lifecycle owners。复杂度局限在一次性synthetic composition，16-case与exact9 evidence覆盖owner、filesystem和failure lifecycle边界。
