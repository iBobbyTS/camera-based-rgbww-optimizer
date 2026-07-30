# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12：canonical classification expectation correction

**计划状态：** `AWAITING_ORCHESTRATOR_ALIGNMENT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-12-CANONICAL-CLASSIFICATION-EXPECTATION`

**唯一当前动作：** Orchestrator只读审查C11 rejection，更新
`.agent-work/FULL_PLAN_REFERENCE.md`，整理并提交reviewed state，然后冻结一个PLAN-only
activation topology。当前PLAN不授权Executer编辑、测试、创建evidence root、提交或执行任何
candidate、R3、release、设备及后续阶段工作。

**C11 review archive：**
`.agent-work/PLANS/20260730-0734-p7-retained-r3-option-b-b1a-c3e6f19-corrective-11-review.md`；
SHA-256由Orchestrator在reviewed-state commit前独立冻结并写入activation PLAN。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_12_canonical_classification_expectation_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-12-CANONICAL-CLASSIFICATION-EXPECTATION","dispatch_state":"awaiting_orchestrator_alignment","single_current_action":"orchestrator_freeze_reviewed_state_and_activation_topology","retained_production":{"commit":"ba816216af9d37397873e054f44dbb7eea0f9b10","parent":"c0c51d9bc340da40ab5e95027e999962d2bd723e","subject":"fix(p7): separate historical lineage checkpoint ownership","source_path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","source_sha256":"0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64","disposition":"retained_historical_checkpoint_seam_v1_pending_test_only_validation","consumable":false,"eligibility":false},"proposed_implementation":{"changed_paths":["tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"production_edit_count":0,"config_edit_count":0,"commit_count":1,"subject":"test(p7): align canonical lineage classification expectations"},"immutable_config":{"path":"config/hsi/p7-governance-lineage-successor-v1.json","sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","rewrite_count":0},"fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-12-offline/","formal_chain_invocations_per_item":1,"retry":0,"fallback":0,"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_12_WAITING_ORCHESTRATOR_ALIGNMENT"}`

## 1. Planner decision

C11判定为`REJECTED_TARGETED_AMBIENT_FULL_SET_EXPECTATION_ONLY`。Compileall `1/1`通过；
targeted `13`个selector中`12`通过、`1`失败、error `0`。失败仅来自Planner错误要求full
ambient changed set为eligible且prohibited为空；canonical owner实际正确返回
`ineligible_requires_new_setup`并列出unclassified/prohibited paths。Fail-fast、retry `0`、
fallback `0`和全部设备/R3/release锁均保持。

C11 production source修复已获得historical/current seam targeted覆盖，下一包冻结其bytes，
只允许修正一个测试文件。不得通过修改production、config、canonical builder、分类owner或
旧payload来满足错误断言。

Terminal evidence及artifact实值为权威：precommit bytes `1227`、postcommit bytes `1842`、
targeted bytes `5512`。ER中对应手工值`1073`、`1895`、`5427`仅作append-only supersession，
其路径与SHA正确；不得改写ER或旧evidence。

## 2. Orchestrator必须冻结的activation合同

Orchestrator alignment后，activation PLAN必须冻结：

- reviewed-state commit full SHA及clean worktree；
- C11 review archive的path、bytes和SHA-256；
- PLAN-only activation commit的exact parent、subject、唯一changed path及commit count `1`；
- retained production source/test/config current bytes与SHA；
- C12 test-only implementation exact parent、subject、唯一changed path及commit count `1`；
- brand-new C12 root规则、one-shot validation链、ER discrepancy supersession方式与全部zero locks。

在上述exact合同写入activation PLAN且activation commit独立验证前，不得dispatch Executer。

## 3. 下一包唯一允许的测试纠正

只允许修改`tests/test_p7_thermal_diagnostics.py`中的
`test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`及为同一语义所必需的局部测试
代码。不得修改production/config/其他测试文件，不得新增通用allowlist。

纠正必须分别覆盖：

1. 使用canonical accepted subset构建candidate，断言status为
   `eligible_waiting_for_planner`且`prohibited_paths=[]`；
2. 使用full ambient changed set构建candidate，断言returned paths与输入一一对应、sorted、
   unique，且每项classification与canonical classification owner一致；
3. 断言accepted与prohibited分类均被真实保留，full-set status依据prohibited非空为
   `ineligible_requires_new_setup`，返回的`prohibited_paths`与canonical truth一致；
4. 不得硬编码`59`、`265`或任何ambient path总数。

C11新增historical checkpoint测试、current HEAD subordinate/working-drift测试、两个governance
successor dedicated tests及canonical builder唯一eligibility owner断言必须保留。

## 4. 下一包验证与evidence下限

Executer activation PLAN必须要求brand-new mode `0700` C12 root；存在即hard-fail，不得复用、
删除或改选。测试编辑后冻结before/after blob、working SHA、exact one-path binary patch；创建唯一
implementation commit，随后独立核验child/parent/subject/path/blob/SHA/patch完全一致。

在同一root依次运行，每项恰好一次，任一nonzero立即停止：

1. compileall：production source与test path；
2. targeted：C11 exact 13 selectors，不增不减；
3. focused：`tests.test_p7_thermal_diagnostics`、`tests.test_agent_work_machine_contract`、
   `tests.test_p7_retained_r3_exact_five_controller`、`tests.test_p7_retained_release_audit`；
4. `.venv/bin/python -m unittest discover -s tests -v`，exit `0`；
5. `codegraph sync`，exit `0`；
6. commit-range与working-tree两个`git diff --check`作为同一item，均exit `0`。

Logs继续使用单一fd exclusive-create/no-follow owner，terminal strict JSON最后seal，ER只append一次。
不得把narrow targeted green当作完整验收。

## 5. 硬锁与停止点

Candidate probe/read/build、retained R3 probe/read/copy/repair、canonical retained validator、
eligibility emission、release qualification/generation/copy/consumption、network、`.env`、device、
camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel、P8全部为`0`。
Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

本PLAN当前不授权执行。无科学分支或高危设备操作，不需要Advisor或Human。

**Planner stop：** `F19_CORRECTIVE_12_WAITING_ORCHESTRATOR_ALIGNMENT`。
