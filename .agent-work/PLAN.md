# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17：post-EQ validation exact subordinate successor

**计划状态：** `EXECUTER_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-17-POST-EQ-VALIDATION-SUCCESSOR`

**唯一当前动作：** Executer从本PLAN activation commit的clean dispatch HEAD启动exact一次C17 controller，在brand-new evidence root内完成pre-edit freeze、exact source+dedicated-test implementation commit及第6节的一次性验证链；terminal seal与ER append后立即停止在Planner验收门。

**C16 review archive：**
`.agent-work/PLANS/20260730-0852-p7-retained-r3-option-b-b1a-c3e6f19-corrective-16-review.md`，bytes `5055`，SHA-256
`394223de840fcdeeaeda645cac9835c453d71ac758839122b7b6df5c16a16cc2`；Orchestrator须独立复算。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_17_post_eq_validation_successor_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-17-POST-EQ-VALIDATION-SUCCESSOR","dispatch_state":"executer_authorized","execution_authorized":true,"single_current_action":"execute_exact_once_c17_post_eq_validation_successor_controller","review_archive":{"path":".agent-work/PLANS/20260730-0852-p7-retained-r3-option-b-b1a-c3e6f19-corrective-16-review.md","bytes":5055,"sha256":"394223de840fcdeeaeda645cac9835c453d71ac758839122b7b6df5c16a16cc2"},"c16":{"dispatch_head":"7f2ce2393eaa0f4ed42d891ae666faccb422d445","terminal_sha256":"53372a9d08ed8f30c5f2f471c15cabf0f7fe9c432ce070a1d23a2ec30db7566a","decision":"rejected_focused_post_eq_validation_successor_missing"},"activation":{"required_parent":"e9d38824ac2ddb84dca3350f6792f4183a1b565b","subject":"chore(plan): activate f19 corrective 17","changed_paths":[".agent-work/PLAN.md"],"additional_paths":0,"commit_count":1},"implementation":{"changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"commit_count":1,"subject":"fix(p7): bind post-eq validation successor"},"subordinate_successor":{"commit":"3a14fe0bd663250dd48c65e71f1a6550df89267f","parent":"431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53","subject":"fix(p7): exclude root Finder metadata from EQ evidence","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_contract.py"],"paths_lf_sha256":"cf2edd153dbd6c49caa9efc65b793521055d1358079d5dc70ad84df319b8011e","canonical_binary_patch_sha256":"018cf00c4e452673f4303ce528fbea2c0b6667e8dc691f5ff44c6968603412de","classification_path":"tests/test_p7_td_b_r6_contract.py","classification":"accepted_post_eq_exposure_policy_validation"},"validation":{"compileall":1,"targeted_selector_count":5,"focused_modules":["tests.test_p7_td_b_r6_contract","tests.test_p7_thermal_diagnostics","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"full_suite":1,"codegraph_sync":1,"diff_check":1,"retry":0,"fallback":0},"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_17_TERMINAL_WAITING_PLANNER"}`

## 1. C16 decision与冻结根因

C16以`REJECTED_FOCUSED_POST_EQ_VALIDATION_SUCCESSOR_MISSING`结束。它的activation、retained C15 commit topology、Git-object prevalidation freeze、compileall与exact targeted `6/6`均合规；focused suite运行`193`项后出现`1`项failure与`2`项error，故full、CodeGraph与diff依fail-fast保持`0`。Retry/fallback为`0/0`，所有锁定操作为`0`。

Authoritative terminal：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-16-offline/20260730T144754Z/terminal-evidence.json`

bytes `7577`、mode `0600`、SHA-256
`53372a9d08ed8f30c5f2f471c15cabf0f7fe9c432ce070a1d23a2ec30db7566a`。

三项失败同根：现有post-EQ owner正确地验证历史accepted commit
`161094ffa2bf1f84ed1fc787e708e8c3463f10db`的exact blobs，但对classified validation path同时要求current checkpoint与working tree仍等于历史SHA
`10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23`。合法retained C15 commit `3a14fe0...`已把该path精确改为
`77ef59ccee5eee34d85658aadf7a6ce40f413fee9b8395cd11fb82145df27104`。两项正常测试因此报`checkpoint blob differs`；duplicates负例被同一前置漂移遮蔽。这是工程provenance seam，不是科学分支，不需要Advisor或Human授权。

## 2. Planner activation gate（已授权）

Planner已独立验证工作区clean，并将Orchestrator reviewed-state commit
`e9d38824ac2ddb84dca3350f6792f4183a1b565b`冻结为activation direct parent。本PLAN只可创建exact一个PLAN-only activation commit：

- subject exact `chore(plan): activate f19 corrective 17`；
- changed paths exact `.agent-work/PLAN.md`；
- additional paths `0`、commit count `1`；
- activation前后worktree均须clean；提交成功后Executer获得第3至第8节的exact一次执行授权。

Executer controller须从clean worktree一次programmatic执行`git rev-parse --verify HEAD^{commit}`冻结dispatch HEAD；second HEAD read与human-transcribed child SHA均为`0`。它须在创建root、读取实现文件或运行任何validation前验证activation direct parent、subject、PLAN-only path set；任一不符立即hard-fail。

## 3. Immutable historical owner与exact subordinate successor

### 3.1 不可弱化的历史accepted owner

现有`TD_B_POST_EQ_POLICY_*`与`_validate_td_b_post_eq_policy_lineage`仍必须验证历史accepted commit：

- commit `161094ffa2bf1f84ed1fc787e708e8c3463f10db`；
- parent `f37517af3ae25efb41f085904fd48f037980ed04`；
- subject `feat(p7): finalize eq-r6 state-c exposure policy`；
- exact三路径、path-ledger digest与每个historical commit-qualified blob SHA全部保持不变；
- `config/hsi/p7-ray-td-b-exposure-policy-v2.json`仍须在checkpoint与working tree等于历史accepted SHA
  `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`。

不得删除、替换、跳过或把历史commit-object验证改成ambient working-tree验证；不得改旧payload、旧commit、旧manifest、旧artifact SHA或canonical candidate builder。

### 3.2 唯一允许的subordinate successor binding

在同一post-EQ lineage owner边界内新增一个immutable exact subordinate successor layer，只绑定：

- commit `3a14fe0bd663250dd48c65e71f1a6550df89267f`；
- direct parent `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`；
- subject `fix(p7): exclude root Finder metadata from EQ evidence`；
- exact sorted changed paths：
  1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
  2. `tests/test_p7_td_b_r6_contract.py`
- additional paths `0`、commit count `1`；
- exact LF path-ledger SHA-256
  `cf2edd153dbd6c49caa9efc65b793521055d1358079d5dc70ad84df319b8011e`；
- exact selected canonical binary patch SHA-256
  `018cf00c4e452673f4303ce528fbea2c0b6667e8dc691f5ff44c6968603412de`。

Commit-qualified before/after identities必须全部验证：

| path | parent-before blob / bytes / SHA-256 | successor-after blob / bytes / SHA-256 | per-path binary diff SHA-256 |
| --- | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | `efcb4b05877e857b47eebcb3d7e07dbf5979698f` / `193853` / `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64` | `2d65c51200688e71dacc531e2e99b1240b4649d5` / `193918` / `d81a504c3eb2df654f493bd8cfa94189a4cb6673c0ef24fb9c183834a0bac93e` | `7948c6d4bfa74617717f6a9fb6fd50fa1f392f805892e70e1e181928b6d01075` |
| `tests/test_p7_td_b_r6_contract.py` | `4bc6a791972ad04693015961c0d43c57865305db` / `102435` / `10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23` | `3a2397d8d02ff85388c4a5dfb87333721871dbcb` / `104738` / `77ef59ccee5eee34d85658aadf7a6ce40f413fee9b8395cd11fb82145df27104` | `0ae363872c7db9ae0bd79ae855f31b91e5bdc4f3176d3fac013d9bd53cf540d4` |

Successor validation必须要求`new_checkpoint`同时包含historical accepted commit与该exact successor commit。Successor source path仅用于证明exact commit topology和blob provenance，绝不能因该layer获得classification。唯一延续的classification是exact：

`tests/test_p7_td_b_r6_contract.py` → `accepted_post_eq_exposure_policy_validation`

该validation path的checkpoint Git object与working regular non-symlink file必须等于successor-after SHA `77ef59...`。不得接受任意当前blob、任意descendant、近邻test/source/config、glob、prefix、generic path allowlist、额外classification或自动fallback。

`build_td_b_setup_release_lineage_candidate`保持唯一canonical candidate/eligibility owner。Subordinate helper只能返回上述one-path mapping供原post-EQ owner使用，不得emit eligibility、读取release/R3、改变candidate schema或绕过changed-path duplicate/repository-relative validation。

## 4. Exact implementation scope与pre-edit evidence

Activation通过后，Executer只可编辑：

1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
2. `tests/test_p7_thermal_diagnostics.py`

Additional paths `0`。不得编辑`tests/test_p7_td_b_r6_contract.py`、config、GUIDE、PLAN、FULL、archive或旧ER。只可创建一个implementation commit，subject exact：

`fix(p7): bind post-eq validation successor`

在首次读取/编辑这两个implementation paths前，Executer须先在prefix
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-17-offline/`
下exclusive-create一个brand-new UTC child root（mode `0700`），并以single-owner exclusive/no-follow fd创建`pre-edit-freeze.json`（mode `0600`）。Freeze须记录dispatch/activation topology、allowed paths的working bytes/hash/blob、Git status、上述historical/successor immutable facts与command argv/exit；flush/fsync/close后strict JSON reload与digest。不得从parent事后重建并声称pre-edit freeze。

实现后仅stage exact两个allowed paths并创建exact一个commit。Implementation child SHA必须由controller在commit成功后programmatically读取并记录，不得预抄。须验证direct parent为activation commit、subject、exact two-path topology、additional `0`、before/after blob identities及canonical binary patch digest，并写入exclusive `postcommit-topology.json`后才可运行validation。任一失败terminal seal并停止；不得amend、retry、fallback、cherry-pick、rebase或创建第二commit。

## 5. Required implementation behavior与tests

实现须保持单一post-EQ owner，并以immutable constants/mapping描述第3.2节exact facts；不得创建第二candidate builder或通用lineage framework。Dedicated tests至少覆盖：

1. exact successor commit/parent/subject/two-path set/path digest/selected与per-path patch digest、before/after blob OID/bytes/SHA全部通过；
2. historical accepted commit的exact三path blob验证仍运行且不可弱化；
3. only exact validation path继承原classification，successor source path与nearby paths不获classification；
4. wrong ancestry、commit、parent、subject、path set/order/count、path digest、patch digest、before/after blob OID/bytes/SHA分别fail closed；
5. checkpoint validation blob drift、working bytes drift、symlink、non-file分别fail closed；
6. duplicates与non-repository-relative changed paths仍由canonical builder以原语义拒绝，不被lineage precheck遮蔽；
7. helper不读取candidate/R3/release，不emit eligibility，canonical builder仍是唯一eligibility owner。

Exact targeted selectors按以下顺序各出现一次：

1. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_post_eq_validation_successor_binds_exact_commit_and_only_validation_path`
2. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_post_eq_validation_successor_rejects_topology_blob_and_working_drift`
3. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_current_head_lineage_accepts_exact_human_policy_freeze`
4. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`
5. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_post_eq_policy_lineage_fails_closed_without_widening`

## 6. Exact one-shot validation chain

Implementation commit topology通过后，依序执行，每项exactly once、fail-fast：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`；exit `0`；
2. `.venv/bin/python -m unittest -v <第5节exact 5 selectors>`；`5/5`、exit `0`；
3. `.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_agent_work_machine_contract tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_release_audit`；exit `0`；
4. `.venv/bin/python -m unittest discover -s tests -v`；exit `0`；
5. `codegraph sync`；exit `0`；
6. `git diff --check <activation-commit>..<implementation-commit>`与`git diff --check`作为同一item各调用一次且均exit `0`；前者changed paths exact source+dedicated test，后者在ER append前须为空。

不得用targeted/focused green替代full suite。预计总时长小于10分钟；若dispatch前合理估算超过10分钟，须使用Human可见macOS Terminal、三次稀疏liveness与automation工作流，不得拆分规避。

## 7. Artifact lifecycle、locks与failure branches

每个validation log必须single-owner `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`、mode `0600`、single fd、flush/fsync/close后digest。Terminal strict JSON最后exclusive-create、fsync、strict reload、digest与seal，记录activation、pre-edit freeze、implementation topology、所有exact successor facts、test matrices、commands/exits/log identities、Git status、retry/fallback与全部locks。

Root count `1`、implementation commit count `1`、retry `0`、fallback `0`。任何precondition、edit、commit、topology、test或seal失败均fail-fast进入同一Planner门；不得修补artifact、复用root、重跑失败命令或开始另一corrective branch。Terminal seal后只append ER一次，不得stage/commit ER或编辑PLAN/FULL。

Candidate、retained R3、canonical retained validator、eligibility emission、release generation/qualification/consumption、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel与P8全部为`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 8. Acceptance与停止点

Planner只在以下全部成立时接受C17 implementation：activation与implementation topology exact；pre-edit与postcommit evidence lifecycle合规；historical owner未弱化；exact subordinate successor所有commit/path/blob/patch facts通过；one-path classification无扩张；negative matrices有效；compileall、targeted `5/5`、focused、full、CodeGraph与两项diff全部green；所有调用各`1`；retry/fallback `0/0`；ER append `1`；全部locks `0`。

即使全部green，也只回到Planner验收门；不得解锁retained-R3 validator、eligibility、release、FORMAL或设备阶段。

**Planner stop：** `F19_CORRECTIVE_17_TERMINAL_WAITING_PLANNER`。
