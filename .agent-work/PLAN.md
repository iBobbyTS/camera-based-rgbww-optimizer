# REF-P7-25-R2-B2-P7-I1：accepted-owner fresh synthetic integration qualification

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P7-I1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-ACCEPTED-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator审核本PLAN、同步其独占FULL，并以当前clean HEAD
`9d8573fd4155851adc6e71b3b0ccc50365f6f6d3`为direct parent创建exact activation commit。Activation完成且worktree clean后，Executer只运行一次fresh pure-offline integration：用activation HEAD派生一个从未存在的source/root，构造一个immutable
`ControllerDomainTemplateSpec`，调用accepted P6/P7 builder exact once，再把其`runtime_request`交给accepted P5 runtime exact once。不得重试旧P5-I1、恢复一次性external controller或进入retained/validator/release/device路线。

**唯一 Planner stop：**
`B2_P7_I1_ACCEPTED_OWNER_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md`；bytes `3290`，SHA-256
`e892edcbf301d9222969318970cd5999411df8a07308af9e54686b83319a2d84`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_i1_accepted_owner_fresh_synthetic_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-P7-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-ACCEPTED-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"9d8573fd4155851adc6e71b3b0ccc50365f6f6d3","expected_subject":"chore(plan): activate p7 synthetic integration","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-ACCEPTED-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p7_status":"ACCEPTED_COMPLETE_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_OWNER","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":true,"p7_candidate_consumable_scope":"FUTURE_PURE_OFFLINE_SYNTHETIC_INTEGRATION_INPUT_ONLY","p7_synthetic_integration_qualified":false,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_owners":{"runtime":{"commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","parent":"099d1ad833c3e73b7dc157f5786ad66bb6718f5e","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","test_blob":"a6aa7d7caf015e2eb858830dc89aaedaeb51aafa","test_sha256":"66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782","entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime.execute_controller_runtime"},"builder":{"commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","parent":"478d8c52e4a21d6628219e27b88b507d736f3aca","entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_domain_template.build_controller_domain_template"},"runnable_template":{"commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","parent":"44fb7295f0f71030833476225350da01ce3c71d3","source_blob":"5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5","source_sha256":"10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2","test_blob":"d0f733426673aa9a57fcb1195ecea014f8c48062","test_sha256":"4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e"}},"builder_frozen_spec":{"reference_task_id":"REF-P7-25-R2-B2-P6","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1","activation_commit":"94ad1c7bf7353480766418a2cffbbf3f581899be","activation_parent":"4af057e0cd5f62d18a02cf02e088c1f293bddc4d","activation_subject":"chore(plan): activate p6 domain template owner","activation_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1549-p7-retained-r3-b2-p5-i1-domain-template-gap-review.md"],"runtime_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","runtime_parent":"099d1ad833c3e73b7dc157f5786ad66bb6718f5e","runtime_source_blob_oid":"075face6fd7453236affa303640b91eb16a42a9b","runtime_source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","runtime_test_blob_oid":"a6aa7d7caf015e2eb858830dc89aaedaeb51aafa","runtime_test_sha256":"66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782","repo_root":"/Users/ibobby/Projects/WLED-RGBWW","process_argv":["/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python","-"]},"fresh_paths":{"activation_sha_source":"outer_head_stdout","activation_short_sha_length":12,"source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-source-{activation_short_sha}.py","root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-root-{activation_short_sha}","must_be_absent_before_owner_creation":true,"failed_path_reuse":false,"source_retention":"immutable_durable_evidence","root_retention":"immutable_durable_evidence"},"invocations":{"outer_read_only_git":1,"builder":1,"runtime":1,"runtime_composition":1,"existing_analyzer":1,"source_create":1,"source_readback":1,"controller_process":1,"root_create":1,"controller_git_ledgers":6,"same_root_input_writes":4,"same_root_input_reads":4,"semantic_matrix_cases":16,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"success_contract":{"expected_bound_results":18,"effect_bindings":14,"fixture_bindings":4,"controller_root_reads":7,"artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"artifact_count":9,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"stdout_envelope":{"artifact_count":9,"status":"repo_owned_runnable_domain_template_candidate_waiting_for_planner_review"},"stderr_bytes":0,"process_exit_code":0,"success_label":"FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE"},"failure_contract":{"primary_failure_dominates":true,"second_source":0,"second_root":0,"second_process":0,"retry":0,"fallback":0,"repair":0,"delete":0,"reuse":0,"preserve_returned_source":true,"preserve_created_root_and_partial_artifacts":true,"er_append_only_after_runtime_terminal_or_typed_exception":true,"stop":"B2_P7_I1_ACCEPTED_OWNER_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"},"zero_budgets":{"outer_source_writer":0,"outer_source_reader":0,"outer_source_launcher":0,"dependency_overrides":0,"second_writer":0,"second_analyzer":0,"second_classifier":0,"second_serializer":0,"parallel_lifecycle":0,"code_writes":0,"test_writes":0,"production_writes":0,"implementation_commits":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_query":0,"git_stage":0,"git_commit":0,"old_p5_i1_source_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"archive":{"path":".agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md","bytes":3290,"sha256":"e892edcbf301d9222969318970cd5999411df8a07308af9e54686b83319a2d84"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_I1_ACCEPTED_OWNER_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate、initial clean 与唯一外层HEAD

Activation commit必须满足machine row的direct parent、subject和exact three changed paths；完成后worktree必须clean。FULL必须把本reference/contract设为唯一active，保持retained
`RETAINED_UNVALIDATED_UNCONSUMED`、三个accepted owner状态、P7 candidate consumable scope、synthetic integration尚未qualified、Executer dispatched true与device authorization false。

Executer在任何fresh path、Python import或integration effect前，严格提取PLAN/FULL各唯一一条literal backtick-wrapped machine row并strict JSON decode，校验上述activation与FULL state。第一条且controller外唯一Git命令必须是：

```text
/usr/bin/git rev-parse HEAD
```

它必须exit `0`、stderr empty、stdout为activation full SHA加single LF；该success也证明dispatch时HEAD正是activation commit。取其前12个lowercase hex派生唯一source/root。除这个HEAD读取外，outer Git invocation为0；activation后的clean porcelain由Orchestrator在dispatch前冻结并交接，Executer不得增加第二Git命令来重验。

Source/root exact parent均为`/Volumes/4T/temp/rgbww-optimizer`，不得alternate spelling、symlink path、escape、旧root或旧source。Outer不得先行创建、打开、读取、修复或删除它们：source的O_EXCL成功与root的exclusive create成功分别是initial absence的effect-owner证明；如任一路径已存在，owner必须fail closed，且不得换名、retry或复用。

## 2. 唯一immutable spec、builder与runtime调用

Outer只允许构造一个frozen `ControllerDomainTemplateSpec`，字段exact取自machine row：

- builder reference/contract固定为accepted P6 public contract，而不是把新P7-I1 activation伪装成P6 provenance；
- P6 activation固定为`94ad1c7bf7353480766418a2cffbbf3f581899be`、parent
  `4af057e0cd5f62d18a02cf02e088c1f293bddc4d`、subject及exact three paths；
- runtime固定为P5 owner `37f7d002...`、parent、source/test blob OID与SHA；
- `source_path`/`output_root`为本次activation-derived fresh paths；`repo_root` exact
  `/Users/ibobby/Projects/WLED-RGBWW`；`process_argv` exact
  `('/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python', '-')`。

调用`build_controller_domain_template(spec)` exact once。不得手写、patch、regenerate或serialize第二份template/request；不得修改bundle。随后把exact
`bundle.runtime_request`传给`execute_controller_runtime` exact once，`dependencies`不得override。Outer不得直接调用`compose_controller_source`、`analyze_controller_source`、source open/write/chmod/read、`subprocess.run/Popen`或任何第二owner。

Accepted runtime必须独占完成compose1、existing analyzer1、0600 O_EXCL/O_NOFOLLOW source create1、fsync/parent identity、exact readback1与process1；process的sole stdin input必须是verified source bytes，`shell=False`、`check=False`。Outer只消费immutable
`ControllerRuntimeReport`或typed `ControllerRuntimeError`，只用`report.process.exit_code/stdout/stderr`，不得反射raw `returncode`。

## 3. Generated controller success contract

Generated controller只能复用模板已绑定的repo owners。其activation phase运行accepted `run_read_only_git` exact Git6：P6 activation commit、metadata、paths，以及P5 runtime metadata、paths、binary patch。不得追加Git、raw CompletedProcess判断、generic allowlist或第二transport classifier。

Conformance/activation成功后，使用accepted provenance I/O owner创建single 0700 physical root；root before/after保持同一device/inode/mode。写入四个0600 canonical JSON inputs并各做same-root exact read：

1. `synthetic-plan.json`；
2. `synthetic-full.json`；
3. `synthetic-lineage.json`；
4. `synthetic-seal.json`。

四个identity组成唯一`RootIdentityChain(before, files=(four direct identities), after)`并验证。Semantic matrix必须exact `16/16` true；不得新增analyzer/classifier。Success lifecycle exact：

```text
conformance -> activation -> root -> inputs -> evaluate -> terminal -> terminal_seal -> admission
```

Final root exact九个artifact：four inputs加`integration-qualification.json`、其SHA sidecar、`terminal-evidence.json`、其SHA sidecar及`execution-result-admission.json`。Qualification先于terminal，terminal先于seal，seal先于admission；sidecar绑定exact target bytes/SHA，admission only after sealed terminal。

Controller stdout必须是single canonical JSON success envelope（exact artifact count `9`与machine row status），stderr empty、exit_code `0`。Success只能标记
`FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`；不得称retained validated、eligible、release usable或real B2 admitted。

## 4. Terminal evidence、retention 与 failure branches

Runtime为同步owner；返回report或抛出typed exception即唯一controller process已terminal，不得另做process probe。Source一旦由runtime创建即保留为immutable durable evidence；root一旦由controller创建即保留其全部partial/final artifacts。Success和failure均禁止删除、repair、rename、reuse或自动清理这些paths；后续Planner只可在stop后做独立只读审计，不得重执行。

- Builder在effect前失败：source/root/process均0，保留typed builder code，直接stop。
- Runtime composition/conformance在source前失败：root/process0，记录typed primary，direct stop。
- Source persistence/readback/launch失败：保留已创建source及可取得的physical identity；root只在controller实际启动后才可能存在；second source/process0。
- Controller root前失败：保留process exit/stdout/stderr与primary；root/artifacts0，不得用terminal-missing覆盖primary。
- Root后失败：保留same root与所有已有artifacts；existing lifecycle terminal handling不得用seal/admission错误覆盖原primary。
- 任一count/path/hash/mode/identity/Git6/matrix/lifecycle/stdout/stderr/exit discrepancy：hard fail，retry/fallback/second source/root/process均0。

Executer在runtime终止前不得向ER写任何bytes。Terminal后仅允许`.agent-work/EXECUTION_RESULT.md` single EOF append，记录activation SHA、fresh paths、builder/runtime call counts、bundle template/replacement hashes、runtime source identity/report、process exit/stdout/stderr hashes、controller Git6/same-root4/matrix16/lifecycle/exact9的真实到达程度、primary failure或success label、retained path disposition与全部zero budgets。无法从report证明的计数必须写`unproven`，不得推断成pass。ER append后立即停在Planner stop；不得自行做artifact forensic read、retry或进入后续route。

## 5. Acceptance criteria

Planner只在以下全部成立时接受：

1. activation/unique machine rows/first-and-sole outer Git exact；dispatch前clean；
2. fresh source/root由activation前12位派生且owner creation前不存在；旧paths读取0；
3. immutable spec1、builder1、runtime1，dependency override0；
4. P5 runtime独占compose/analyzer/source O_EXCL write/readback/process各1；outer writer/read/launcher0；
5. source regular 0600、physical identity/bytes/SHA exact；controller process terminal且无residual owned process；
6. controller Git6、single physical root before/after、same-root four writes/reads、matrix16/16；
7. qualification→terminal→seal→admission与final exact9 artifacts成立；
8. stdout single canonical envelope、stderr empty、exit_code0；
9. retry/fallback/second source/root/process、第二writer/analyzer/classifier/serializer/lifecycle全0；
10. ER pre-terminal bytes0、terminal后single EOF append1；source/root被保留且未复用；
11. 所有hard locks保持0。

本包预计低于10分钟，不要求visible Terminal或automation。它是pure-offline integration，code/test/production writes、implementation commit、test、compileall及CodeGraph均为0；不得为了“额外确信”自行扩大验证范围。

## 6. Hard locks and stop

Retained R3/candidate payload、real B2、subordinate manifest、canonical validator、eligibility、retained audit、release generation/qualification/copy/consumption、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer、TD-C、sentinel、P8、firmware/deployment全部exact `0`。这些锁不需要Advisor或Human checkpoint；它们表示本包不得进入相邻路线。

无论success或failure，Executer append一次ER后必须停在：

`B2_P7_I1_ACCEPTED_OWNER_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`

Planner随后只读验收fresh source/root/progressive/terminal evidence；只有Planner接受且Orchestrator更新FULL后，才可能规划retained-validation successor。

维护性判断：本包不改repo代码或测试，只组合P5 runtime、P6 deterministic builder与P7 runnable template三个既有owner；source I/O、semantic analysis、lifecycle和artifact persistence仍由各自单一owner承担，没有新增平行writer、classifier或controller framework。
