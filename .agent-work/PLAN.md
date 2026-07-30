# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12：canonical classification expectation correction

**计划状态：** `READY_FOR_PLAN_ONLY_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-12-CANONICAL-CLASSIFICATION-EXPECTATION`

**唯一当前动作：** 以exact reviewed-state parent
`739e6d8fcb32fe417fc83fd69f004d9b875dd5c6`创建一个PLAN-only activation commit；Executer仅可在
该activation child上纠正exact一个测试文件中的canonical classification期望，创建唯一test-only
implementation commit，在brand-new C12 root各运行一次完整验证链并停止在Planner验收门。不得修改
production/config，不得访问candidate、retained R3、release、设备或科学阶段。

**C11 review archive：**
`.agent-work/PLANS/20260730-0734-p7-retained-r3-option-b-b1a-c3e6f19-corrective-11-review.md`，
bytes `6690`，SHA-256
`7082943b652a9687a28928285a12e3a138e64cb4f7da672abc13a8cc6894aa98`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_12_canonical_classification_expectation_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-12-CANONICAL-CLASSIFICATION-EXPECTATION","dispatch_state":"ready_for_plan_only_activation_commit","single_current_action":"align_canonical_classification_test_expectation_then_validate","review_archive":{"path":".agent-work/PLANS/20260730-0734-p7-retained-r3-option-b-b1a-c3e6f19-corrective-11-review.md","bytes":6690,"sha256":"7082943b652a9687a28928285a12e3a138e64cb4f7da672abc13a8cc6894aa98"},"activation":{"required_parent":"739e6d8fcb32fe417fc83fd69f004d9b875dd5c6","subject":"chore(plan): activate f19 classification expectation correction","changed_paths":[".agent-work/PLAN.md"],"additional_paths":0,"commit_count":1,"initial_clean_required":true},"retained_production":{"commit":"ba816216af9d37397873e054f44dbb7eea0f9b10","parent":"c0c51d9bc340da40ab5e95027e999962d2bd723e","subject":"fix(p7): separate historical lineage checkpoint ownership","disposition":"retained_historical_checkpoint_seam_v1_pending_test_only_validation","consumable":false,"eligibility":false},"implementation":{"direct_parent":"exact_activation_child_at_dispatch","subject":"test(p7): align canonical lineage classification expectations","changed_paths":["tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"production_edit_count":0,"config_edit_count":0,"commit_count":1,"baseline_test":{"blob_oid":"126ee9b36b4c6165cd96e0a9856b7e59580a001e","bytes":214729,"sha256":"9c6c721ebb5cb24b9aff79d36d4853b1935a55e0dfb38b32e64afcbad1b7d7ff"}},"immutable_production":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","blob_oid":"efcb4b05877e857b47eebcb3d7e07dbf5979698f","bytes":193853,"sha256":"0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64","rewrite_count":0},"immutable_config":{"path":"config/hsi/p7-governance-lineage-successor-v1.json","blob_oid":"a08ea362c7cd33bfc0fd5277ca1f0f524958ad71","bytes":2571,"sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","rewrite_count":0},"c11_er_supersession":{"old_recorded_bytes":{"precommit_freeze":1073,"postcommit_topology":1895,"targeted_log":5427},"authoritative_bytes":{"precommit_freeze":1227,"postcommit_topology":1842,"targeted_log":5512},"old_er_rewrite_count":0,"required_c12_er_append_supersession":true},"targeted_selector_count":13,"focused_modules":["tests.test_p7_thermal_diagnostics","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-12-offline/","formal_chain_invocations_per_item":1,"retry":0,"fallback":0,"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_12_TERMINAL_WAITING_PLANNER"}`

## 1. Activation gate与冻结身份

本PLAN首先只授权Orchestrator创建并核验一个PLAN-only activation commit：

- direct parent exact：`739e6d8fcb32fe417fc83fd69f004d9b875dd5c6`；
- subject exact：`chore(plan): activate f19 classification expectation correction`；
- changed path exact：`.agent-work/PLAN.md`；additional path `0`；commit count `1`；
- parent与commit后worktree均须clean；dispatch HEAD必须是该activation child的full lowercase SHA。

Reviewed-state parent的subject为`chore(orch): align f19 classification expectation correction`，其
parent为`ba816216af9d37397873e054f44dbb7eea0f9b10`。C11 review archive必须继续匹配上方exact
path/bytes/SHA，且当前FULL必须匹配committed blob
`79b90615b7d8416750fe1a2a156a8a56ec77094e`、bytes `229563`、SHA-256
`145eb1ed34878c4f1e6602e6e7465fcddb39a53f5a11d5c6ab3f8f2ebbdb9755`。

Executer在创建root、编辑、测试、stage或commit前，必须独立验证activation topology、committed
PLAN bytes、clean worktree，以及本PLAN冻结的source/test/config blob、bytes和SHA。任一不符只向
ER append一次失败记录并停止。C11 root及其中artifact禁止读取、复用、补写、修复或计入C12；C11
artifact的权威身份只能消费本PLAN与review archive已冻结的值。

## 2. Immutable owner与唯一测试修改

下列路径必须byte-exact不变，不得编辑、stage或commit：

- `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`：blob
  `efcb4b05877e857b47eebcb3d7e07dbf5979698f`，bytes `193853`，SHA-256
  `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`；
- `config/hsi/p7-governance-lineage-successor-v1.json`：blob
  `a08ea362c7cd33bfc0fd5277ca1f0f524958ad71`，bytes `2571`，SHA-256
  `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`。

唯一允许修改的路径是`tests/test_p7_thermal_diagnostics.py`，baseline blob
`126ee9b36b4c6165cd96e0a9856b7e59580a001e`、bytes `214729`、SHA-256
`9c6c721ebb5cb24b9aff79d36d4853b1935a55e0dfb38b32e64afcbad1b7d7ff`。只允许修改
`test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`及为同一语义必需的局部测试代码：

1. 用canonical accepted subset构建candidate，断言status为
   `eligible_waiting_for_planner`且`prohibited_paths=[]`；
2. 用full ambient changed set构建candidate，断言returned paths与输入一一对应、sorted、unique，
   且每项classification与canonical classification owner一致；
3. 断言accepted与prohibited分类均被真实保留；当prohibited非空时full-set status为
   `ineligible_requires_new_setup`，其`prohibited_paths`与canonical truth一致；
4. 不得硬编码`59`、`265`或任何ambient path总数。

C11新增historical checkpoint regression、current HEAD subordinate/working-drift覆盖、两个governance
successor dedicated tests，以及canonical builder唯一eligibility-owner断言必须保留。旧policy、workflow、
public-default payload与canonical validators必须逐字节不变；不得新增generic allowlist、修复/再生成旧payload、
修改classification owner或建立第二eligibility owner。

## 3. Exact test-only implementation commit

Activation gate通过后创建brand-new mode `0700` C12 root；在prefix下选择并冻结唯一UTC命名child，
若该exact path已存在立即hard-fail，不得删除、复用或改选第二root。

测试编辑完成后，commit前冻结baseline/working test bytes与SHA、before/after blob、exact one-path
changed set，以及`git diff --binary <activation-child> -- tests/test_p7_thermal_diagnostics.py`的
canonical patch SHA-256。只允许一个implementation commit：

- direct parent exact为dispatch时核验的activation child；
- subject exact：`test(p7): align canonical lineage classification expectations`；
- changed path exact：`tests/test_p7_thermal_diagnostics.py`；additional path `0`；
- commit count `1`；不得amend、rebase、第二commit或fallback。

Commit后必须独立验证child/parent/subject/path set、before/after blob、committed test SHA与canonical
patch全等于precommit freeze，并再次核验source/config及所有旧payload未变。任一不符fail closed，不得
修复后重试或把该commit描述为validated。

## 4. Exact 13-selector targeted gate

Targeted命令必须恰好包含下列`13`个完整selector，顺序如下，不得增加、减少、alias或拆分运行：

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

## 5. Fresh one-shot validation chain

Implementation topology验证通过后，在同一brand-new root依次运行以下每项恰好一次；任一nonzero立即
停止后续项，retry `0`、fallback `0`：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`；
2. `.venv/bin/python -m unittest -v <上节按原顺序展开的exact 13 selectors>`；必须`13/13`、exit `0`；
3. `.venv/bin/python -m unittest -v tests.test_p7_thermal_diagnostics tests.test_agent_work_machine_contract tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_release_audit`；exit `0`；
4. `.venv/bin/python -m unittest discover -s tests -v`；exit `0`；
5. `codegraph sync`；exit `0`；
6. `git diff --check <activation-child>..HEAD`与`git diff --check`作为同一item；两者均exit `0`。

不得用targeted/focused green替代full suite。既有full suite约两分钟，当前预计不超过10分钟；若
Executer重新估算超过10分钟，必须使用Human可见macOS Terminal、三次稀疏liveness与automation流程，
不得拆分规避。

## 6. Evidence、C11 supersession与ER

每个log必须由单一owner以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr共用fd，
child退出后flush/fsync/close再digest；不得预创建后reopen、使用second fd或shell redirection。所有artifact
必须regular、non-symlink、mode `0600`。Terminal strict JSON最后exclusive-create并seal，至少记录：

- activation与implementation完整topology、pre/post identities、one-path patch SHA；
- source/test/config before/after blob、bytes、SHA与immutable核验；
- exact 13 selector argv、focused/full/CodeGraph/diff每项calls/exit/log bytes/SHA/mode；
- accepted-subset与full-set canonical classification断言结果；
- fail-fast、retry/fallback、全部zero locks及retained R3状态；
- C11 discrepancy supersession：ER旧记录`1073/1895/5427`不得改写，权威artifact bytes分别为
  `1227/1842/5512`；对应权威SHA仍为
  `6cb3e2d87d642a9c3202d9d8ab82b845999cb4b5b4d1b696170208b1fcc8be60`、
  `f0a4bdcf001b43c369d6a76a9db56bc3a91cb93ac51f4100f9a62b6ccf5328cb`、
  `5af2ab0eb70a0547f6a509572b69ad1578fc664741a4ffdd01dcf0f85a70c75a`。

Terminal seal后只向`.agent-work/EXECUTION_RESULT.md`append一次C12结果；append必须显式
`supersedes_c11_manual_byte_counts=true`并同时记录old/authoritative值。不得重写旧ER、C11 terminal或
任何旧artifact。Append前除ER外worktree必须clean，append后只允许ER dirty。

## 7. 硬锁与停止点

Candidate probe/read/build、retained R3 probe/read/copy/repair、canonical retained validator、eligibility
emission、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、
cleanup、FORMAL-R6、public analyzer、TD-C、sentinel和P8全部为`0`。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

本包不涉及科学分支或高危设备操作，不需要Advisor或Human授权。成功仅表示test-only纠正和完整验证
等待Planner验收；不得进入candidate、R3、release或后续阶段。失败不得retry、fallback、自行改PLAN或
扩大scope。

**Planner stop：** `F19_CORRECTIVE_12_TERMINAL_WAITING_PLANNER`。
