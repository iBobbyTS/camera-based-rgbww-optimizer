# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14：retained source topology validation recovery

**计划状态：** `READY_FOR_PLAN_ONLY_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-14-SOURCE-TOPOLOGY-VALIDATION`

**唯一当前动作：** Orchestrator以exact reviewed-state parent
`5e55c3f8e3d5c862f05d317cdccc57b453b4e4d0`创建一个PLAN-only activation commit，subject exact为
`chore(plan): activate f19 retained topology validation`；随后Executer在该activation child上以programmatic
single-read/freeze方式取得dispatch HEAD，在brand-new C14 root对retained source/test/config运行一次fail-fast完整验证链，
append terminal与ER证据后停止在Planner验收门。Executer不得编辑、stage或提交任何implementation路径。

**C13 review archive：**
`.agent-work/PLANS/20260730-0804-p7-retained-r3-option-b-b1a-c3e6f19-corrective-13-review.md`，
bytes `4434`，SHA-256
`c2018931bdb35e6424829177b0111a831bfbeab46f44ba7c69e5f7259f87f924`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_14_source_topology_validation_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-14-SOURCE-TOPOLOGY-VALIDATION","dispatch_state":"ready_for_plan_only_activation_commit","single_current_action":"programmatic_dispatch_head_retained_topology_validation_only","review_archive":{"path":".agent-work/PLANS/20260730-0804-p7-retained-r3-option-b-b1a-c3e6f19-corrective-13-review.md","bytes":4434,"sha256":"c2018931bdb35e6424829177b0111a831bfbeab46f44ba7c69e5f7259f87f924"},"reviewed_state":{"commit":"5e55c3f8e3d5c862f05d317cdccc57b453b4e4d0","parent":"88d46061a50f0e8a89b2a6cc51ca9399d75f4347","subject":"chore(orch): align f19 retained topology recovery"},"activation":{"required_parent":"5e55c3f8e3d5c862f05d317cdccc57b453b4e4d0","subject":"chore(plan): activate f19 retained topology validation","changed_paths":[".agent-work/PLAN.md"],"additional_paths":0,"commit_count":1,"initial_clean_required":true,"dispatch_head_owner":"controller_git_rev_parse_single_read_freeze","human_transcribed_expected_child_sha":0,"second_dispatch_head_read":0},"retained_production_commit":{"commit":"ba816216af9d37397873e054f44dbb7eea0f9b10","parent":"c0c51d9bc340da40ab5e95027e999962d2bd723e","subject":"fix(p7): separate historical lineage checkpoint ownership","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"one_path_assertion_forbidden":true},"retained_source":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","blob_oid":"efcb4b05877e857b47eebcb3d7e07dbf5979698f","bytes":193853,"sha256":"0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64","disposition":"retained_historical_checkpoint_seam_v1_pending_validation","consumable":false,"eligibility":false},"retained_test":{"commit":"a9a817137969d9d2692fdd0b244d08e26e8a025d","parent":"d4f97a63e304cd78ebe26930907024805ce25102","subject":"test(p7): align canonical lineage classification expectations","changed_paths":["tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"blob_oid":"e04c68f27eadda7d271fc449f6b6d4a673f2a8b3","bytes":216054,"sha256":"4eb823d5dfe22b95a172f4920b077285b50ad174b4a4c9cdda9fd7751dc164a5","canonical_patch_sha256":"546ef9de7ec338906b736a8cb981cfead7d807e17102182e84eda92e8e6e6d86","disposition":"retained_canonical_classification_expectation_v1_pending_validation","consumable":false,"eligibility":false},"retained_config":{"commit":"0682cd8763516dfb19a8e1ad48c53cb9934b9d19","path":"config/hsi/p7-governance-lineage-successor-v1.json","blob_oid":"a08ea362c7cd33bfc0fd5277ca1f0f524958ad71","bytes":2571,"sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","rewrite_count":0},"execution_scope":{"repository_implementation_edits":0,"staged_paths":0,"implementation_commits":0,"plan_or_full_edits":0,"er_append_count":1,"brand_new_root_count":1,"fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/","targeted_selector_count":13,"focused_modules":["tests.test_p7_thermal_diagnostics","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"formal_chain_invocations_per_item":1,"retry":0,"fallback":0},"c12_er_supersession":{"authoritative_c13_append_complete":true,"c14_new_supersession_append":0},"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_14_TERMINAL_WAITING_PLANNER"}`

## 1. Exact PLAN-only activation topology

Orchestrator只可创建并核验一个activation commit：

- direct parent exact：`5e55c3f8e3d5c862f05d317cdccc57b453b4e4d0`；
- parent subject exact：`chore(orch): align f19 retained topology recovery`；
- parent direct parent：`88d46061a50f0e8a89b2a6cc51ca9399d75f4347`；
- activation subject exact：`chore(plan): activate f19 retained topology validation`；
- changed path exact：`.agent-work/PLAN.md`；additional paths `0`；commit count `1`；
- commit前与commit后worktree均须clean。

该activation commit属于Planner工作流拓扑，不是implementation commit。不得在同一commit包含ER、FULL、archive、
source、test、config或其他路径。不得amend、rebase、cherry-pick或创建第二activation commit。

Executer dispatch后，controller必须以一次Git读取直接取得当前full lowercase 40-character HEAD并冻结为
`dispatch_head`；允许的等价命令是`git rev-parse --verify HEAD^{commit}`。该值只读取一次，之后activation child、
baseline diff上界与所有topology比较都必须消费同一个冻结值；caller、wrapper、controller、terminal writer与ER不得
手抄、截断、拼接、预测或第二次读取expected child SHA。若single read不是完整lowercase commit SHA，立即fail closed。

在root创建、测试或ER append前，controller须以冻结的`dispatch_head`核验：其direct parent、subject、exact one-path
changed set与上方activation合同完全一致；worktree clean；review archive与committed FULL仍匹配当前已冻结状态。
任一不符只写terminal failure并向ER append一次，不得继续。

## 2. Corrected retained production topology

Retained production commit必须按whole-commit exact topology核验，禁止再推导为source-only commit：

- child exact：`ba816216af9d37397873e054f44dbb7eea0f9b10`；
- direct parent exact：`c0c51d9bc340da40ab5e95027e999962d2bd723e`；
- subject exact：`fix(p7): separate historical lineage checkpoint ownership`；
- exact changed-path set按下列顺序归一化比较：
  1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
  2. `tests/test_p7_thermal_diagnostics.py`
- additional paths `0`。

Controller不得断言、记录或暗示`ba81621…`是one-path commit，不得只从source path反推whole-commit changed set，
也不得用generic allowlist、substring、prefix或path-count-only判断替代exact two-path equality。该whole-commit topology
通过后，才可继续分别核验当前retained source/test/config identities。

## 3. Retained source/test/config exact identities

以下三个路径均为immutable validation inputs；Executer的编辑、stage、commit、rewrite、repair与regeneration均为`0`：

1. Retained source path
   `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`必须在`ba816216…`与冻结的
   `dispatch_head`中保持blob `efcb4b05877e857b47eebcb3d7e07dbf5979698f`，bytes `193853`，SHA-256
   `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`。
2. Retained test commit `a9a817137969d9d2692fdd0b244d08e26e8a025d`，direct parent
   `d4f97a63e304cd78ebe26930907024805ce25102`，subject
   `test(p7): align canonical lineage classification expectations`，exact changed path
   `tests/test_p7_thermal_diagnostics.py`、additional `0`。当前test blob
   `e04c68f27eadda7d271fc449f6b6d4a673f2a8b3`，bytes `216054`，SHA-256
   `4eb823d5dfe22b95a172f4920b077285b50ad174b4a4c9cdda9fd7751dc164a5`；canonical binary patch
   SHA-256 `546ef9de7ec338906b736a8cb981cfead7d807e17102182e84eda92e8e6e6d86`。
3. Retained config provenance commit `0682cd8763516dfb19a8e1ad48c53cb9934b9d19`。Config path
   `config/hsi/p7-governance-lineage-successor-v1.json`，blob
   `a08ea362c7cd33bfc0fd5277ca1f0f524958ad71`，bytes `2571`，SHA-256
   `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`。

Controller在root创建前必须从committed `dispatch_head`与working tree分别核验三路径的blob、bytes、SHA，并核验
`ba81621…` whole-commit topology、test commit topology与test patch SHA；全部通过后才可创建root。旧policy、workflow、
public-default payload、canonical classification owner、canonical candidate builder与旧manifest必须byte-exact不变。
不得新增generic allowlist、第二eligibility owner或任何validation commit。

## 4. Brand-new C14 root与调用预算

Root prefix exact为：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/`。
Controller只可在prefix下用一个冻结UTC child name exclusive-create一个mode `0700` root。若exact path已存在，
立即hard-fail；不得删除、复用、改名、选择第二root或读取C13/C12/C11及任何旧execution root。Root count `1`，
retry `0`，fallback `0`。

每个validation log必须由一个owner通过`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr
共用该single fd；child退出后flush/fsync/close再digest。不得先预创建后reopen、使用第二fd或shell redirection。
Artifacts须regular、non-symlink、mode `0600`。每个命令只调用一次；任一gate或命令nonzero立即停止所有后续项。

## 5. Exact 13-selector targeted gate

Targeted命令必须恰好包含以下`13`个完整selector，顺序固定，不得增加、减少、alias、拆分或二次运行：

1. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_agents_policy_lineage_rejects_wrong_bytes_owner_and_provenance`
2. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_current_head_lineage_accepts_exact_human_policy_freeze`
3. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`
4. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_lineage_release_rejects_candidate_and_resolved_plan_tampering`
5. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`
6. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_public_default_successor_lineage_layers_historical_and_current_owners`
7. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_public_default_successor_manifest_fails_closed_on_exact_drift`
8. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_qualification_evidence_adapter_is_release_isolated`
9. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_qualification_evidence_adapter_rejects_preparation_drift`
10. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift`
11. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`
12. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`
13. `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_public_default_successor_historical_checkpoint_ignores_working_owner`

## 6. One-shot validation chain

Activation、programmatic dispatch HEAD、corrected two-path production topology与三项retained identity gate通过后，
在同一brand-new root依次运行；每项exactly once、fail-fast：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`；exit `0`；
2. `.venv/bin/python -m unittest -v <上一节按原顺序展开的exact 13 selectors>`；必须`13/13`、exit `0`；
3. `.venv/bin/python -m unittest -v tests.test_p7_thermal_diagnostics tests.test_agent_work_machine_contract tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_release_audit`；exit `0`；
4. `.venv/bin/python -m unittest discover -s tests -v`；exit `0`；
5. `codegraph sync`；exit `0`；
6. `git diff --check 5e55c3f8e3d5c862f05d317cdccc57b453b4e4d0..<frozen_dispatch_head>`与
   `git diff --check`作为同一validation item，各调用一次且均exit `0`。第一个diff的changed path只能是exact
   `.agent-work/PLAN.md`，第二个必须只允许尚未append ER前的empty working tree；该item必须在ER append前运行。

不得以compileall、targeted或focused green替代full suite。既有full suite约两分钟，预计本包不超过10分钟；
若Executer在dispatch前基于当前环境重新估算超过10分钟，必须使用Human可见macOS Terminal、三次稀疏liveness、
automation与goal blocked流程，不得拆分命令规避。

## 7. Terminal seal、C12 supersession与ER

Terminal strict JSON必须最后exclusive-create、fsync、reload、digest与seal，至少记录：

- programmatic HEAD owner调用数`1`、冻结`dispatch_head`，且human-transcribed/second-read counts均`0`；
- reviewed-state、activation、`ba81621…` exact two-path topology及retained test/source/config exact identities；
- brand-new root identity、mode、single-fd lifecycle与artifact identities；
- exact 13 selector argv，以及compileall/targeted/focused/full/CodeGraph/diff的calls、exit、log bytes、SHA、mode；
- repository implementation edits `0`、staged paths `0`、implementation commits `0`、retry/fallback `0`；
- 所有硬锁调用数`0`与retained R3状态；
- C12 evidence supersession已由C13权威ER append完成：C14只引用该事实，新增supersession append count `0`，不得
  重复或改写C13/C12 ER记录及其旧artifacts。

Terminal seal后只向`.agent-work/EXECUTION_RESULT.md`append一次C14结果。Append必须记录terminal path/bytes/SHA、
exact validation counts与Planner decision request；不得重写旧ER、任何旧terminal/artifact或旧root。Append前worktree必须
clean；append后只允许ER dirty。Executer不得stage或commit ER，由Planner/Orchestrator后续验收整理。

## 8. 硬锁与停止点

Candidate probe/read/build、retained R3 probe/read/copy/repair、canonical retained validator、eligibility
emission、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、
cleanup、FORMAL-R6、public analyzer、TD-C、sentinel和P8全部为`0`。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

本包是offline validation-only工程纠偏，不涉及科学分支或高危设备操作，不需要Advisor或Human授权。即使完整链成功，
也只证明retained source/test/config在activation dispatch HEAD上通过验证并等待Planner验收；不得访问candidate/R3、
运行canonical retained validator、产生eligibility、消费release或进入后续阶段。失败不得retry、fallback、自行改PLAN或扩大scope。

**Planner stop：** `F19_CORRECTIVE_14_TERMINAL_WAITING_PLANNER`。
