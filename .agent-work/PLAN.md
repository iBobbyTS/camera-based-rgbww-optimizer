# REF-P7-25-R2-B2-P4-C1：repo-owned transport-domain correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-TRANSPORT-DOMAIN-OWNER-CORRECTION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation commit；activation后，
Executer只在现有conformance owner及其dedicated test两个repo paths内实现、验证并提交一个bounded successor。
Accepted owner必须在同一次runtime-source analysis中输出exact transport-domain report；不得生成或读取external
controller/root，不得再次实现one-off AST classifier。

**唯一 Planner stop：**
`B2_P4_C1_TRANSPORT_DOMAIN_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1308-p7-retained-r3-b2-p4-i1-c1-c1-fixture-classification-failure-review.md`，
bytes `9916`，SHA-256 `7a88cc6e889772c70da6c8ca09e747034c675724f9a1fb16f2cfa3f291f2c947`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_transport_domain_owner_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-TRANSPORT-DOMAIN-OWNER-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"781e410c43774c20da9f00e8c9e0f5bfd27b1f66","expected_subject":"chore(plan): activate p4 transport domain owner correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1308-p7-retained-r3-b2-p4-i1-c1-c1-fixture-classification-failure-review.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","activation_head_must_match_frozen_activation_tuple":true,"expected_subject":"fix(p7): own retained controller transport domains","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_controller_conformance.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-TRANSPORT-DOMAIN-OWNER-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_controller_conformance.py"],"accepted_baseline":{"implementation_commit":"83bb193259fcf1de5b3f78798001e83496c2daae","implementation_parent":"5f2483c319b395b2aef2a43f4827b4c150f3f3fd","source_blob_oid":"52fcdc73c69e367cd1b046b52d83ffc555a6d496","source_sha256":"94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7","test_blob_oid":"28a58c6051de378fbcc6485c316df9ff10d3a90c","test_sha256":"447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726","dedicated_test_methods":14,"focused_tests":70,"full_tests":755,"full_evidence_commit":"c89b2914af44eb3d10f4dc8b347340d86abc5756"},"reviewed_failure":{"activation_commit":"53df8ca0611b05819e500c9376c6f150b48511cd","evidence_commit":"697f9f1800a91442695f23d551a8d1a5f5cb9624","debug_commit":"781e410c43774c20da9f00e8c9e0f5bfd27b1f66","stable_code":"live_owner_transport:drift_root:Call","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-i1-c1-c1-controller-972f824.py","source_bytes":32216,"source_sha256":"a9d982f88bc75ef09e029ce4311a46f3e9f59264fed86c98e1bb5fc284122010","accepted_analyzer_status":"PASS","accepted_analyzer_bound_results":18,"failed_fixture_shape":"FileIdentity(root=drift_root)","effect_attempts":0,"root_absent":true,"immutable_no_read":true},"transport_owner_contract":{"single_ast_owner":"analyze_controller_source","single_parse_binding_pass":true,"report_type":"ControllerTransportReport","report_embedded_in":"ControllerConformanceReport.transport","binding_domains":["effect_owned","pure_fixture"],"effect_origin":"non_constructor_owner_call","fixture_origin":"direct_exact_owner_dataclass_constructor","classification_by_variable_name":false,"classification_by_path":false,"generic_call_allowlist":false,"report_fields":["effect_bindings","fixture_bindings","fixture_constructor_edges","root_chain_compositions","root_chain_validations","effect_transport_uses"],"effect_transport_uses_on_pass":0,"fixture_to_exact_constructor_edge_allowed":true,"effect_to_fixture_constructor_edge_allowed":false,"effect_alias_allowed":false,"effect_container_allowed":false,"effect_generic_helper_argument_allowed":false,"effect_callback_or_closure_return_allowed":false,"exact_root_chain_exception":{"constructor":"RootIdentityChain","named_fields":["before","files","after"],"files_container":"tuple_literal","direct_validator":"validate_root_identity_chain","effect_identity_grouping":true},"external_transport_ast_classifier_allowed":false,"deterministic_sorted_immutable_report":true},"regression_contract":{"new_test_methods":6,"exact_method_names":["test_15_transport_report_classifies_effect_and_fixture_bindings","test_16_fixture_file_root_composition_is_not_live_transport","test_17_effect_identity_cannot_masquerade_as_fixture","test_18_effect_alias_container_and_generic_helper_transport_rejected","test_19_exact_root_identity_chain_composition_only_exception","test_20_transport_report_is_deterministic_and_exports_exact"],"case11_positive":"FileIdentity(root=drift_root)","effect_negative_kinds":["alias","container","generic_helper_argument","callback_return","closure_return"],"exact_root_chain_positive":true,"near_miss_root_chain_negatives":true,"stable_error_codes_required":true},"test_contract":{"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_controller_conformance","targeted_expected":20,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract","focused_expected":76,"full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","baseline_full_tests":755,"new_test_methods":6,"full_expected":761,"compileall_command":".venv/bin/python -m compileall -q src tests","codegraph_sync_required":true,"git_diff_check_required":true,"postcommit_targeted_expected":20},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"failed_source_reads":0,"failed_root_reads":0,"accepted_c1_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_TRANSPORT_DOMAIN_OWNER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation, exact scope and immutable baseline

Orchestrator activation必须以clean HEAD
`781e410c43774c20da9f00e8c9e0f5bfd27b1f66`为direct parent，subject与exact三路径必须匹配machine row。
Activation后worktree/stage/untracked必须clean；FULL必须exact一个active task/contract，保留candidate hash、retained
state、Orchestrator verification、dispatch true和device authorization false。任一gate不匹配即stop，不得改code/test。

Executer以activation runtime HEAD作为唯一implementation parent，先冻结existing two files的blob/SHA并与machine row
accepted baseline一致。写路径exact为现有source和dedicated test；不得新增module、fixture file、wrapper、doc或artifact。
不得读取failed external source/root来推断实现；committed ER、archive、PLAN及debug的冻结事实已足够。

Maintainability gate：现有module已拥有owner schemas、AST parse/bindings、root-chain validation与lifecycle composition，
transport classification属于同一semantic boundary；应扩展该owner，而不是新增service或external classifier。若实现需要第三
repo path、generic plugin registry、path/callee allowlist或复制第二AST traversal owner，必须在edit前stop回Planner。

## 2. Single-owner transport report

在现有 `analyze_controller_source` 的同一次strict UTF-8 parse/compile、parents map、binding registry和attribute/root-read
analysis中加入transport provenance；不得让caller对source再次AST parse或扫描。新增frozen
`ControllerTransportReport`，并作为 `ControllerConformanceReport.transport` 返回。Report及其所有nested fields必须是
deterministic sorted tuples，不含mutable collection、AST node、path object或live owner object。

Report exact fields：

- `effect_bindings`：所有non-constructor owner call直接绑定的name/type/call provenance；
- `fixture_bindings`：exact owner dataclass constructor直接绑定的name/type provenance；
- `fixture_constructor_edges`：pure fixture name进入另一个exact owner constructor的direct field edge；
- `root_chain_compositions`：exact `RootIdentityChain` direct binding及named before/files/after names；
- `root_chain_validations`：该chain direct传给exact `validate_root_identity_chain`的配对；
- `effect_transport_uses`：accepted report必须exact empty；发现prohibited use时先以stable code fail closed，不返回PASS。

Domain只能由call provenance和exact AST shape决定，不能由变量名、path literal、function/callback名字或generic callee
allowlist决定。Non-constructor owner call result属于effect-owned live domain；直接exact owner dataclass constructor result属于
pure-fixture domain。`DirectoryIdentity(...)`直接构造的`drift_root`进入
`FileIdentity(..., root=drift_root)`是合法fixture constructor edge，必须报告而非拒绝。任何effect-owned name进入fixture
constructor必须stable reject，防止以constructor伪装live transport。

Effect-owned identity仍可进行accepted字段读取/比较、existing exact shared-root `read_exact_file(root=<live root>)`和
inline plain field projection；不得成为第二alias、ordinary list/tuple/set/dict/container元素、subscript/attribute assignment
value、generic helper/call argument、callback return或closure return。不得通过comprehension、lambda、`*args`、`**kwargs`、
reflection或opaque indirection逃逸。每类negative必须返回明确stable code，不能只依赖generic exception。

唯一effect identity grouping exception是direct assigned
`RootIdentityChain(before=<direct effect root>, files=(<direct effect files>...), after=<direct effect root>)`：callee、named
fields、tuple literal和direct names都必须exact；该chain只可direct传给一次
`validate_root_identity_chain(chain_name)`。Positional/extra/missing fields、list files、nested helper、wrong validator、alias、
container或unvalidated chain均stable reject。禁止generic path/call allowlist。Existing opaque terminal-seal规则继续原样由
owner处理，不因本patch放宽。

External consumers之后只能调用 `analyze_controller_source` 并比较embedded transport report；本包不得创建consumer，
但source/test中必须以static assertion防止公开或内部出现第二个transport analyzer入口。

## 3. Exact six-method regression surface

在existing 14 methods后新增exact六个method，方法名与machine row完全一致：

1. `test_15...`：一个source同时含effect calls与fixture constructors，report按provenance exact分类且prohibited空；
2. `test_16...`：复现required `drift_root = DirectoryIdentity(...)`、
   `drift_file = FileIdentity(..., root=drift_root)`，assert fixture edge exact且不被记为effect transport；
3. `test_17...`：effect root被送入fixture `FileIdentity` constructor必须stable reject，证明不能masquerade；
4. `test_18...`：以subTest分别验证effect alias、container、generic helper argument、callback return、closure return均按
   exact stable code拒绝；不得只断言raised；
5. `test_19...`：exact immutable RootIdentityChain composition+direct validator PASS；positional/list/missing/extra/
   wrong-validator/alias near misses逐项stable reject；
6. `test_20...`：同bytes两次analysis report完全相同、tuple/frozen结构与exact exports成立，并静态证明module只有
   `analyze_controller_source`一个transport analysis owner。

不得删除、合并或重命名原14 methods；test method总数exact `20`。测试必须验证report内容和stable codes，不能只执行
代码。不得为了迎合计数添加空断言或重复方法。

## 4. Ordered validation, commit and evidence

Edits完成后按序exact各一次：

1. targeted command，必须exit `0`且`20/20`；
2. focused command，existing baseline 70加六方法，必须exit `0`且`76/76`；
3. compileall command，exit `0`；
4. unique unbuffered full command，actual baseline 755加六方法，必须完整terminal `761/761`、`OK`、failures/errors `0`；
5. `codegraph sync` exact一次并确认index current，随后focused query证明single transport owner与source/test call path；
6. `git diff --check`及path set检查，diff exact两个write paths，stage仍为空。

任一失败立即stop，不得retry、fallback、第二full、count probe、临时fix或partial commit。Full预计约三分钟，整个package
under 10 minutes，不使用visible Terminal/automation。

全部通过后只stage exact两个paths，创建一个implementation commit，direct parent为activation runtime HEAD，subject exact
`fix(p7): own retained controller transport domains`。Commit changed paths必须exact two，禁止amend/rebase/merge/tag/push。
Commit后worktree/stage/untracked必须clean，再运行machine row exact postcommit targeted一次，必须`20/20`。最后Executer只向
ER append一次，记录before/after/final blob OID与SHA、report API、stable-code matrix、四次test invocation完整exit/count、
compileall、CodeGraph、diff/commit topology及全部zero budgets；append后porcelain只允许ER一个unstaged modification。

## 5. Acceptance, locks and stop

Acceptance要求：activation exact；two-path scope；single AST owner；report domains/fields exact；case-11 fixture PASS；effect
masquerade及alias/container/helper/return negatives exact reject；唯一RootIdentityChain exception exact；no generic allowlist；
existing14+new6=`20` methods；targeted `20/20`、focused `76/76`、full `761/761`、compileall、CodeGraph、diff与postcommit
targeted全部通过；single exact commit；clean tree；ER sole append。

本包通过只修复repo conformance owner，不自动证明synthetic consumer、retained R3、real B2或eligibility。External
controller/source/root写读、failed source/root、accepted C1、retained artifact、Git provenance replay、real B2、subordinate
manifest、canonical validator、eligibility、retained audit、全部release、network/DNS/environment/credentials、device/camera/
Ray/strip/cleanup/capture、FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment继续hard locked `0`。Planner验收并由
Orchestrator更新FULL前不得规划或运行consumer integration。

维护性判断：本包触及shared AST/conformance owner，风险集中在classification provenance与exact exceptions；修改仍严格
限制于现有owner和专属测试，不新增并行owner或I/O依赖。六个meaningful regression methods及761 full suite覆盖source of
truth、false-positive复现、真实transport negatives和唯一composition exception；通过后无需进一步架构重构。
