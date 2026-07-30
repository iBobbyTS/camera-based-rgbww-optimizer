# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-13：programmatic HEAD validation-only recovery

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-13`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-13-PROGRAMMATIC-HEAD-VALIDATION`

**唯一当前动作：** Orchestrator只读复核C12 decision，更新其独占的
`.agent-work/FULL_PLAN_REFERENCE.md`，整理并提交reviewed state，然后冻结一个exact PLAN-only
activation topology。此版PLAN不授权Executer dispatch、root创建、测试、CodeGraph、Git mutation、
candidate/R3/release/device或后续阶段。

**C12 review archive：**
`.agent-work/PLANS/20260730-0749-p7-retained-r3-option-b-b1a-c3e6f19-corrective-12-review.md`，
bytes `6082`，SHA-256
`488e6953cd153109a14f3102a57bd2e40dc6d4f3ae2bcf05b545054d4f37ee20`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_13_orchestrator_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-13","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-13-PROGRAMMATIC-HEAD-VALIDATION","dispatch_state":"waiting_orchestrator_alignment","single_current_action":"orchestrator_review_full_update_and_activation_topology_freeze","review_archive":{"path":".agent-work/PLANS/20260730-0749-p7-retained-r3-option-b-b1a-c3e6f19-corrective-12-review.md","bytes":6082,"sha256":"488e6953cd153109a14f3102a57bd2e40dc6d4f3ae2bcf05b545054d4f37ee20"},"retained_test_commit":{"commit":"a9a817137969d9d2692fdd0b244d08e26e8a025d","parent":"d4f97a63e304cd78ebe26930907024805ce25102","subject":"test(p7): align canonical lineage classification expectations","changed_paths":["tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"disposition":"retained_canonical_classification_expectation_v1_pending_validation","consumable":false,"eligibility":false},"retained_production":{"commit":"ba816216af9d37397873e054f44dbb7eea0f9b10","disposition":"retained_historical_checkpoint_seam_v1_pending_validation","consumable":false,"eligibility":false},"successor_constraints":{"repository_edits":0,"implementation_commits":0,"human_transcribed_expected_child_sha":0,"programmatic_dispatch_head_binding_required":true,"brand_new_root_required":true,"retry":0,"fallback":0},"c12_er_supersession":{"old_recorded_precommit_sha256":"4f557d6d0d9cdcc2fdd7a48e7c968d6284e5d21ef9e9d65f96394be49e0f03a9","authoritative_precommit_sha256":"5821ab5d2b4d25cf218933c208b128854149150473c604a24131262ec0b6361a","old_er_rewrite_count":0,"required_successor_er_append_supersession":true},"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_13_WAITING_ORCHESTRATOR_ALIGNMENT"}`

## 1. C12审查结论

C12 test-only commit的actual topology已由Planner独立核验：

- child `a9a817137969d9d2692fdd0b244d08e26e8a025d`；
- parent `d4f97a63e304cd78ebe26930907024805ce25102`；
- subject `test(p7): align canonical lineage classification expectations`；
- changed path exact `tests/test_p7_thermal_diagnostics.py`，additional `0`；
- before/after blob分别为`126ee9b36b4c6165cd96e0a9856b7e59580a001e`与
  `e04c68f27eadda7d271fc449f6b6d4a673f2a8b3`；
- committed test bytes `216054`，SHA-256
  `4eb823d5dfe22b95a172f4920b077285b50ad174b4a4c9cdda9fd7751dc164a5`；
- canonical binary patch SHA-256
  `546ef9de7ec338906b736a8cb981cfead7d807e17102182e84eda92e8e6e6d86`。

C12唯一失败是controller将actual child手抄成
`a9a8171b80b4d6ace1319b4032588152bf2b6a0d`。Postcommit controller `1/1`、exit `1`；compileall、
targeted、focused、full、CodeGraph和diff均为`0`。因此test commit仅保留为pending validation，不能报为
validated或consumable。

## 2. Evidence与append-only纠偏

C12 authoritative evidence：

- root：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-12-offline/20260730T074500Z`；
- precommit freeze：bytes `1171`、mode `0600`、SHA-256
  `5821ab5d2b4d25cf218933c208b128854149150473c604a24131262ec0b6361a`；
- terminal：bytes `3155`、mode `0600`、SHA-256
  `b412d9d5ca7d9a044945b3cfc71a8deb96f1e6bf99733f18323240a82c560c84`。

ER旧append将precommit SHA错记为
`4f557d6d0d9cdcc2fdd7a48e7c968d6284e5d21ef9e9d65f96394be49e0f03a9`。旧ER和C12 artifacts不得
改写；未来C13 terminal与ER只能append新字段显式supersede为权威SHA
`5821ab5d2b4d25cf218933c208b128854149150473c604a24131262ec0b6361a`。

## 3. Orchestrator必须冻结的可执行后继

Orchestrator对C12 review与FULL完成对齐后，下一Planner activation版须冻结：

1. exact reviewed-state parent、PLAN-only activation subject/path/commit count；
2. reviewed-state与activation child的完整Git topology；
3. retained test commit、source、config及其exact blobs/bytes/SHA；
4. C12 review archive的exact bytes/SHA；
5. brand-new C13 root prefix；
6. exact 13 targeted selectors、四个focused modules与one-shot validation命令；
7. programmatic dispatch HEAD owner：同一controller从Git直接取得一次full lowercase HEAD，冻结为
   `dispatch_head`，后续所有topology比较只消费该冻结值，禁止caller/controller手抄或再次拼接expected child；
8. repository edits `0`、stage `0`、implementation commit `0`、retry/fallback `0`与所有锁。

可执行后继不得修改test/source/config/旧payload，不得amend/rebase/cherry-pick或创建validation commit。
Activation PLAN commit属于Planner工作流拓扑，不计为implementation commit。

## 4. 预期validation-only链

Orchestrator对齐后的可执行PLAN应要求Executer在brand-new root内依次一次、fail-fast运行：

1. activation、reviewed-state与retained test commit topology/identity gate；
2. `.venv/bin/python -m compileall -q`覆盖immutable source与retained test；
3. C12相同exact 13-selector targeted unittest；
4. focused四模块 unittest：`tests.test_p7_thermal_diagnostics`、
   `tests.test_agent_work_machine_contract`、`tests.test_p7_retained_r3_exact_five_controller`、
   `tests.test_p7_retained_release_audit`；
5. `.venv/bin/python -m unittest discover -s tests -v`；
6. `codegraph sync`；
7. frozen baseline至dispatch HEAD以及working tree的两个`git diff --check`。

每个log仍须单一exclusive fd owner；terminal strict JSON最后seal。任一nonzero立即停止，不能重试、
fallback、第二root、repo edit或implementation commit。成功只证明retained source/test/config与完整suite在
dispatch HEAD上通过，仍不能自行访问candidate/R3或产生eligibility。

## 5. 硬锁与停止点

Candidate probe/read/build、retained R3 probe/read/copy/repair、canonical retained validator、eligibility
emission、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、
cleanup、FORMAL-R6、public analyzer、TD-C、sentinel和P8全部为`0`。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

本包不涉及科学分支或高危设备操作，不需要Advisor或Human授权。当前不得dispatch Executer；必须先由
Orchestrator完成FULL对齐与reviewed-state commit，再由Planner写入exact executable activation contract。

**Planner stop：** `F19_CORRECTIVE_13_WAITING_ORCHESTRATOR_ALIGNMENT`。
