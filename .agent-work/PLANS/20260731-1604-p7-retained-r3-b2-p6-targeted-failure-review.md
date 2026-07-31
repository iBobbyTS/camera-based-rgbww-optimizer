# REF-P7-25-R2-B2-P6：repo-owned deterministic controller domain-template owner

**计划状态：** REVIEWED_REJECTED_TARGETED_FAILURE

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1

**Planner decision：** P5-I1 execution at evidence commit 4af057e0cd5f62d18a02cf02e088c1f293bddc4d is
REJECTED_PRE_EFFECT_CANONICAL_DOMAIN_TEMPLATE_NOT_FROZEN。Outer HEAD exact
0ca09a53b0bdb9f7a99ee6dee27420f7517ea702，所有 fresh effects 为 0；失败没有消耗 source/process/root budget，也没有触及 retained R3。
缺口是 active PLAN 只给 semantic counts，没有 canonical bytes、repo-owned builder、exact 18-binding tuple 或 single-root-chain reconstructible
shape。该缺口属于 Orchestrator-owned engineering contract，不需要 Advisor 或 Human 决策。

**当前唯一动作：** Orchestrator 审核、更新 FULL，并以
4af057e0cd5f62d18a02cf02e088c1f293bddc4d 为 direct parent 创建 activation commit。Activation 后，Executer 只新增 exact
domain-template builder 与 dedicated tests 两个路径，证明它能 deterministic 地输出 immutable template/replacement/runtime-request inputs，
且 composed bytes 被现有 canonical analyzer接受为 exact 18 bindings、Git6、single physical root/same-root4、matrix16、exact9/lifecycle source
shape。不得启动 external controller 或读取 retained/old evidence。

**唯一 Planner stop：**
B2_P6_REPO_OWNED_DETERMINISTIC_DOMAIN_TEMPLATE_WAITING_PLANNER_REVIEW。

**本轮新归档：**
.agent-work/PLANS/20260731-1549-p7-retained-r3-b2-p5-i1-domain-template-gap-review.md；bytes 19160，SHA-256
65cdb8326a4f02656ccfd25fd962b2a19721d97bda4fb4b504398cbf04d24b91。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p6_repo_owned_deterministic_domain_template_v1","reference_task_id":"REF-P7-25-R2-B2-P6","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"4af057e0cd5f62d18a02cf02e088c1f293bddc4d","expected_subject":"chore(plan): activate p6 domain template owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1549-p7-retained-r3-b2-p5-i1-domain-template-gap-review.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"feat(p7): own retained controller domain template","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P6","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"builder_contract":{"entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_domain_template.build_controller_domain_template","input_type":"ControllerDomainTemplateSpec","output_type":"ControllerDomainTemplateBundle","output_fields":["template_source","template_sha256","replacement_statement","replacement_sha256","runtime_request","expected_bound_results","expected_artifact_names","expected_lifecycle_order"],"frozen_dataclasses":true,"pure_in_memory":true,"assignment_name":"ACTIVATION_CONTRACT","validation_function":"require_activation_contract","placeholder_assignments":1,"adjacent_validation_calls":1,"canonical_python_literal":true,"runtime_request_type":"ControllerRuntimeRequest","generic_payload":false},"canonical_source_contract":{"strict_utf8":true,"ast_parse":true,"builtin_compile":true,"existing_analyzer_calls_in_tests":1,"expected_bound_results":18,"effect_bindings":14,"fixture_bindings":4,"root_reads":7,"root_chain_compositions":1,"root_chain_validations":1,"effect_transport_uses":0,"controller_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"single_physical_root":true,"root_create_calls":1,"root_before_name":"root_identity","root_after_name":"root_identity","same_root_input_reads":4,"semantic_matrix_cases":16,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"retry":0,"fallback":0},"regression_contract":{"new_test_methods":8,"targeted_expected":8,"focused_expected":90,"full_baseline":767,"full_expected":775,"postcommit_targeted_expected":8},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"codegraph_queries":1,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"runtime_owner_edits":0,"conformance_owner_edits":0,"provenance_owner_edits":0,"lifecycle_owner_edits":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P6_REPO_OWNED_DETERMINISTIC_DOMAIN_TEMPLATE_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 exact scope

Activation commit 必须满足 machine row 的 exact parent、subject、three-path set，之后 porcelain clean。FULL 只允许 P6/本 contract active，
保留 candidate hash/verification 与 retained R3 状态 RETAINED_UNVALIDATED_UNCONSUMED；device authorization false。

Executer 只可新增：

1. src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py
2. tests/test_p7_retained_r3_controller_domain_template.py

不得修改现有 runtime、preparation、conformance、provenance-I/O、lifecycle、validator、retained helper 或任何第三 code/test path。若 exact paths 已存在、
activation drift、worktree 非 clean、或 direct implementation 会要求第三路径，立即 fail closed 写 ER，不得自行扩大 scope。

## 2. Ownership 与 immutable public API

新增模块是 pure domain construction owner，不是 effect/runtime owner。必须导出且仅导出：

- ControllerDomainTemplateError：stable code 的 fail-closed exception；
- ControllerDomainTemplateSpec：frozen typed input，只接受本 package reconstructing 所需的 exact strings/SHAs/path/argv；禁止 Mapping、Any、
  arbitrary payload 或 generic path allowlist；
- ControllerDomainTemplateBundle：frozen output，字段 exact 为 template_source、template_sha256、replacement_statement、
  replacement_sha256、runtime_request、expected_bound_results、expected_artifact_names、expected_lifecycle_order；
- build_controller_domain_template(spec)：唯一 public builder。

Builder 复用现有 ControllerRuntimeRequest 类型，但不调用 execute_controller_runtime、compose_controller_source、analyze_controller_source 或任何
filesystem/process function。template/replacement/runtime_request 全部为 bytes/tuple/frozen dataclass ownership；identical spec 必须得到 byte-for-byte
identical bundle。Bundle 内 runtime_request 必须 exact 使用 assignment_name ACTIVATION_CONTRACT、validation_function
require_activation_contract、spec source_path、以及项目 .venv Python 加 "-" 的 exact tuple argv。

Spec 至少逐字段冻结：reference task/contract；activation full SHA/direct parent/subject/exact activation path tuple；accepted runtime implementation
commit/parent/source blob+SHA/test blob+SHA；source path、output root、repo root与 process argv。所有 SHA/OID、absolute exact path、NUL/LF、tuple、
duplicate/order、artifact-name drift均 stable reject。Builder不得接收 retained payload、candidate payload、eligibility/release/device字段。

## 3. Canonical template 与 replacement contract

模块内只有一个 canonical template bytes owner。Template strict UTF-8、AST parse、builtin compile；含唯一 list-level assignment：

ACTIVATION_CONTRACT = (("placeholder", True),)

其下一条同-list statement必须 exact为 require_activation_contract(ACTIVATION_CONTRACT)。不得有第二 assignment/call、alias、dynamic marker、
reflection、eval/exec/getattr/setattr/vars/dir/globals/locals、.returncode 或 self-referential forbidden-token literal。

Replacement statement必须是单一 ACTIVATION_CONTRACT = <canonical immutable Python literal> 加单一 LF。Literal只允许 exact scalar与嵌套
tuple-of-pairs/tuple；mapping keys按 UTF-8 bytes稳定排序，bool 不得退化为 int，禁止 float/None/set/list/dict runtime mutability。Replacement
exact冻结 spec facts及 P6 counters/budgets；输出 bytes/count/SHA必须 deterministic。Tests通过现有 prepare_controller_source/compose_controller_source
证明 placeholder exact once、adjacent validator exact、替换后 bytes/hash stable；builder本身不重写 external source。

## 4. Exact 18-binding 与 single physical root source shape

Canonical template必须被现有 analyze_controller_source 直接接受，且 dedicated golden assertion冻结整个
ControllerConformanceReport.bound_results tuple，不只断言长度。Exact totals：

- bound results 18；
- effect bindings 14；
- fixture bindings 4；
- root_reads 7，全部绑定同一个 direct live root_identity；
- root-chain composition/validation exact 1/1；
- effect_transport_uses exact empty。

Effect 14由 exact GitLedger 6、create_exclusive_root 的 root_identity 1、read_exact_file 的 same-root FileIdentity 7构成。Fixture 4只能是
direct exact owner dataclass constructors，用于 pure in-memory matrix/terminal target，且 golden test冻结每个 variable name、owner type、constructor
callee与所有 fixture constructor edges。不得通过 alias/container/generic helper/callback return/closure return传 effect identities。

Single physical root strategy必须 exact：

RootIdentityChain(
    before=root_identity,
    files=(synthetic_plan_identity, synthetic_full_identity,
           synthetic_lineage_identity, synthetic_seal_identity),
    after=root_identity,
)

然后 direct exact once validate_root_identity_chain(root_chain)。before/after是同一个 create_exclusive_root effect binding，不得第二次 create、
不得伪造 after identity、不得用 list/generator/helper、不得把 chain返回或另存 alias。四 input read与其余三个 read全部使用
root=root_identity 的 direct keyword。

Git source shape exact six run_read_only_git direct bindings：activation HEAD、parent、subject、activation exact paths、accepted runtime ancestry/two paths、
accepted runtime/test blobs+committed bytes hashes。只检查 GitLedger.exit_code；无 CompletedProcess、.returncode、extra Git或generic ledger container。

## 5. Matrix16、exact9 与 lifecycle source inventory

Builder不执行 controller，但 template必须包含唯一 reconstructible source inventory，dedicated AST/golden tests冻结：

- semantic matrix case labels exact 16且无重复；actual conformance report、Git6、same-root4、single-root-chain、source/replacement identity、artifact set与
  lifecycle/admission顺序均有真实 boolean predicate，不允许常量 True、只计数不验值或自指 forbidden token；
- exact artifact tuple UTF-8 sorted/固定为 synthetic-plan.json、synthetic-full.json、synthetic-lineage.json、synthetic-seal.json、
  integration-qualification.json、integration-qualification.sha256.json、terminal-evidence.json、terminal-evidence.sha256.json、
  execution-result-admission.json；不得第十 artifact、alternate name或generic filename；
- input writes4、qualification writes2、terminal writes2、admission write1；artifact reads exact7；root final count9；
- 唯一 lifecycle调用复用现有 execute_controller_lifecycle，success order exact
  conformance→activation→root→inputs→evaluate→terminal→terminal_seal→admission，retry/fallback 0；
- terminal canonical bytes、target/hash sidecar linkage与admission只复用现有 preparation/provenance/lifecycle primitives；不得复制 analyzer、
  filesystem owner、subprocess launcher、canonical JSON writer、seal validator或第二 lifecycle；
- top-level success/failure envelope只描述 synthetic controller qualification，严禁 retained validated/eligible/release usable语义。

Template imports/calls必须来自现有 runtime-adjacent owners；builder测试以 AST/call inventory证明无 os.open/write/chmod/read、Path.write/read、
subprocess.run/Popen、第二 analyzer/classifier、generic parser或手写 physical identity。P6仅冻结 source ownership，不运行该 source。

## 6. Dedicated exact eight tests

Dedicated test class必须 exact八个 test_* methods，命名与行为：

1. test_01_identical_spec_builds_frozen_byte_exact_bundle
2. test_02_placeholder_replacement_is_unique_adjacent_and_canonical
3. test_03_runtime_request_inputs_are_exact_and_compose_without_effect
4. test_04_existing_analyzer_accepts_golden_eighteen_binding_report
5. test_05_single_physical_root_chain_and_seven_reads_have_exact_shape
6. test_06_git6_matrix16_exact9_and_lifecycle_inventory_is_frozen
7. test_07_invalid_specs_and_literal_values_fail_closed_with_stable_codes
8. test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner

Tests必须验证 FrozenInstanceError、exact bytes/SHA、AST compile、full golden bound/effect/fixture/root tuple、negative spec matrix、exact exports/call inventory。
不得用只检查 substring/count而不冻结相关 AST/value的弱断言；不得运行 generated source、创建 external source/root/process，临时测试 effects为0。

## 7. Ordered validation、commit 与 evidence

按顺序且无 retry/fallback：

1. targeted：
   .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template
   exact 8/8、OK；
2. focused：
   .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract
   exact 90/90、OK；
3. compileall exact new module/test；
4. unique full：
   PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
   exact 775/775、OK，记录唯一 unified session、exit与终行；
5. codegraph sync exact once，然后 query builder→ControllerRuntimeRequest/prepare/analyzer test path与无 effect/lifecycle duplicate；
6. git diff --check、exact two-path gate、eight-method gate；
7. 创建唯一 commit，subject exact feat(p7): own retained controller domain template，changed paths exact two；
8. postcommit targeted exact 8/8；
9. 只向 EXECUTION_RESULT.md EOF append一次完整 handoff。实现 commit后 ER dirty是允许的，PLAN/FULL/archive/debug/GUIDE/RESEARCH保持不变。

Handoff必须记录 activation、implementation commit/parent/subject/path set、两个 blob/bytes/SHA、public API、template/replacement hashes、golden exact
18-binding report、single-root shape、matrix/artifact/lifecycle inventory、全部命令/session/exit/count、CodeGraph、zero budgets与 stop。

## 8. Acceptance、failure branches与 hard locks

Acceptance全部满足：exact two paths；pure deterministic builder；immutable bundle/runtime request；placeholder/replacement exact；existing analyzer接受 full
golden 18/14/4/7、effect transport empty；single root before=after exact name、same-root4、chain1/validator1；Git6/matrix16/exact9/lifecycle source inventory；
targeted8、focused90、compileall、unique full775、CodeGraph、diff/path/method gates、single commit、postcommit8全部通过。

任何 source/analyzer/golden inventory/test/full/CodeGraph/path/commit失败均 fail closed：不放宽 expected counts，不修改现有 owner，不加第三路径，不运行
external source/controller/root，不 retry/fallback。保留代码与证据，append ER后停在唯一 Planner stop。

旧 failed controllers/roots/evidence、retained R3/candidate、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、
retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、
sentinel、P8、firmware、deployment全部 hard locked 0。本包通过只证明 canonical domain-template owner ready；不得自行进入 fresh integration。

## 9. Planner review（2026-07-31）

- 审核对象：activation `94ad1c7bf7353480766418a2cffbbf3f581899be`；rejected candidate
  `3ca70bcee00a89535210d5b9ff9c33850bd58fb7`；failure evidence `957538e491fd94f04e13c20f3020f476e79e384b`。
- Path gate：candidate changed paths exact 为本计划授权的 source/test 两个路径；Orchestrator 已将该 candidate 明确提交为
  non-consumable，未把失败实现误报为可消费 owner。
- Validation：targeted exact `8` tests，但 exit `1`、failures `1`、errors `4`；因此 focused、compileall、full、CodeGraph、
  acceptance commit 与 postcommit targeted 均未发生。
- Finding 1：replacement bytes 带四个 leading spaces，而既有 preparation owner 只替换 assignment AST span、保留 source line prefix；
  composed source 因双重缩进触发 `prepared_source_invalid` / `IndentationError`。
- Finding 2：test 08 全局禁止字符串 `retained`，错误命中 mandatory module docstring、contract/reference IDs、owner/archive paths；
  该断言没有证明 imports/calls/generated runtime semantic boundary，属于测试合同误设。
- Decision：`REJECTED_TARGETED_REPLACEMENT_INDENT_AND_STATIC_ASSERTION_CONTRACT`。缺陷局限于 exact two paths，可由一个
  bounded P6-C1 correction 修复；无需 Advisor、Human、第三 code/test path、external controller、retained read 或任何设备操作。
- Residual lock：retained R3 继续为 `RETAINED_UNVALIDATED_UNCONSUMED`；P6-C1 通过也只解锁 Planner review，不自动进入
  synthetic integration、validator、eligibility、release 或设备阶段。
