# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11：historical-checkpoint and ambient-HEAD seam correction

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT_AND_PLAN_ONLY_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-11-HISTORICAL-CHECKPOINT-SEAM`

**唯一当前动作：** Orchestrator先验收C10 rejection、更新只读FULL并把review/PLAN/ER整理为focused commit；随后Planner只冻结一个PLAN-only activation commit。Executer在该activation child上仅修改exact source/test两路径，纠正历史checkpoint不应读取ambient working bytes以及ambient HEAD测试不得冻结瞬时路径总数两个接缝，创建唯一corrective commit，在brand-new C11 root各运行一次完整验证链并停在Planner门。不得访问candidate、retained R3、release、设备或科学阶段。

**C10 review archive：** `.agent-work/PLANS/20260730-0715-p7-retained-r3-option-b-b1a-c3e6f19-corrective-10-review.md`，SHA-256 `5e9eedd2adcfb284ee26991fc247c5a465d0b5587dafaa792d0e5e273a37826d`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_11_historical_checkpoint_seam_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-11-HISTORICAL-CHECKPOINT-SEAM","dispatch_state":"waiting_orchestrator_alignment_and_plan_only_activation","single_current_action":"correct_historical_checkpoint_and_ambient_head_seams_then_validate","retained_base":{"commit":"0682cd8763516dfb19a8e1ad48c53cb9934b9d19","parent":"4316d0ce84fea8e9c87f90069567a82238e7a733","subject":"fix(p7): validate exact governance lineage successor","disposition":"retained_unaccepted_governance_successor_implementation_base_v1","consumable":false,"eligibility":false},"activation":{"required_parent":"orchestrator_reviewed_state_commit_to_be_frozen_before_dispatch","subject":"chore(plan): activate f19 historical checkpoint correction","changed_paths":[".agent-work/PLAN.md"],"commit_count":1,"initial_clean_required":true},"implementation":{"direct_parent":"exact_activation_child_at_dispatch","subject":"fix(p7): separate historical lineage checkpoint ownership","commit_count":1,"changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"baseline":{"source_sha256":"54fc156df262043e1fbd51901e988e45f08d5bf8d9c8dec41d3bce7ca26b5008","test_sha256":"7475aea66270c4f462be38be60707f506a64bf5bc5d886985a3995a684ee6d20"}},"immutable_config":{"path":"config/hsi/p7-governance-lineage-successor-v1.json","sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","rewrite_count":0},"historical_qualification_checkpoint":"52a7168cd2510e9730e30101fc8fbf6f6d8153c1","historical_public_default_owner":"e7ccdda672b7d5902d81627ff98268160ff141cd","governance_successor":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-11-offline/","formal_chain_invocations_per_item":1,"retry":0,"fallback":0,"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_11_TERMINAL_WAITING_PLANNER"}`

## 1. Orchestrator alignment与activation gate

当前PLAN不是执行授权。Orchestrator须先核对C10 terminal/targeted evidence、C10 implementation exact三路径与本review archive，更新`FULL_PLAN_REFERENCE.md`并亲自整理、提交dirty reviewed state。Planner随后须把machine contract中的activation `required_parent`替换成该clean reviewed-state commit的full SHA，并只创建一个PLAN-only activation commit：

- subject exact：`chore(plan): activate f19 historical checkpoint correction`；
- changed path exact：`.agent-work/PLAN.md`；additional path `0`；
- direct parent exact为冻结后的reviewed-state commit；
- commit后worktree clean，dispatch HEAD为该activation child的full lowercase SHA。

Executer在fresh root、编辑、测试、stage或commit前验证activation topology、committed PLAN bytes、clean worktree，以及retained base `0682cd8763516dfb19a8e1ad48c53cb9934b9d19`的parent、subject、exact三路径和source/test/config SHA。任一不符只append一次ER并停止。

C10 root及其中所有artifact已消费，禁止读取、复用、补写、修复或计入C11。

## 2. Retained base与immutable owner边界

`0682cd8763516dfb19a8e1ad48c53cb9934b9d19`仅作为未验收实现基础保留，不是eligible或consumable结果。C11不得amend、rebase、重写或声称C10通过。

下列config必须byte-exact保持SHA-256 `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`，不得stage或commit：

- `config/hsi/p7-governance-lineage-successor-v1.json`。

旧AGENTS policy freeze、workflow path manifest、public-default successor manifest及其canonical validators全部保持逐字节和fail-closed语义。新governance subordinate仍不得emit eligibility；`build_td_b_setup_release_lineage_candidate`仍是唯一eligibility owner。不得新增generic path allowlist、修复/再生成旧payload或分类额外路径。

## 3. Exact source correction

只在`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`修正`_validate_td_b_public_default_successor_lineage`的working-owner gate：

1. 继续严格解析full lowercase requested checkpoint，并fail closed解析当前Git `HEAD`；不得接受abbreviated/invalid checkpoint。
2. 继续从immutable public-default manifest独立验证commit/parent、entry schema/path set、old/current blob bytes及binary diff。
3. 对历史requested checkpoint，只验证该requested/historical checkpoint中的exact path bytes；不得读取或比较ambient working path bytes。特别是qualification checkpoint `52a7168cd2510e9730e30101fc8fbf6f6d8153c1`包含public-default owner但早于governance successor，必须可在当前工作树下重放。
4. 只有requested checkpoint解析为当前Git `HEAD`时才要求当前working owner。若HEAD已包含governance successor，旧payload先完成验证，然后由`_validate_td_b_governance_lineage_successor`验证working/checkpoint bytes与exact two-path overlap；不得用新hash fallback旧payload。
5. 历史checkpoint分支不得调用subordinate governance validator；当前governance HEAD必须调用一次。任何Git failure、owner/hash/diff/ancestry drift仍fail closed。

不得修改其他production owner或引入并行lineage framework。

## 4. Exact test correction与regression matrix

只在`tests/test_p7_thermal_diagnostics.py`修改/补充覆盖：

- `test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`不得再断言ambient HEAD changed-path总数为`59`、`265`或任何瞬时常量。它必须证明返回值sorted且unique，full candidate的exact path set与输入changed paths一一相等、每项classification与canonical classification owner一致、status仍为`eligible_waiting_for_planner`且`prohibited_paths=[]`；exact两项post-EQ mapping与accepted blob SHA断言保留。
- 新增或扩展明确的historical-checkpoint test：在working skill read被设为hard failure/漂移的条件下，qualification checkpoint `52a7168...`仍只以checkpoint bytes通过public-default lineage验证，并证明governance subordinate未调用。
- current HEAD positive仍须证明旧payload先验证、subordinate exact调用一次、working governance bytes漂移fail closed且canonical builder owner不变。
- 保留C10两个dedicated successor tests及其完整negative matrix；不得用mock跳过manifest、old payload或Git事实验证。

## 5. Exact corrective commit

通过activation/pre-edit gates后创建brand-new mode `0700` C11 root；路径若存在立即hard-fail，不得另选、复用或删除。编辑后在commit前冻结source/test working bytes、SHA、before/after blobs、exact sorted changed paths和`git diff --binary <activation-child> -- <exact-two-paths>` SHA。

只允许一个implementation commit：

- direct parent exact为activation child；
- subject exact为`fix(p7): separate historical lineage checkpoint ownership`；
- changed paths exact为source/test两路径；additional path `0`；
- commit count `1`，不得amend/rebase/第二commit/fallback。

Commit后独立验证full child/parent/subject/path set/blob/SHA/canonical patch全部等于precommit freeze，且immutable config和旧payload SHA均未变。

## 6. Fresh one-shot validation与evidence

在同一brand-new C11 root依次运行，每项恰好一次，任一nonzero立即停止后续项；retry/fallback `0`：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`；
2. targeted unittest：C10原十二个selector，加上本包新增的historical-checkpoint regression selector（若复用已有selector，则terminal必须列出其精确覆盖断言）；
3. focused unittest：`tests.test_p7_thermal_diagnostics`、`tests.test_agent_work_machine_contract`、`tests.test_p7_retained_r3_exact_five_controller`、`tests.test_p7_retained_release_audit`；
4. `.venv/bin/python -m unittest discover -s tests -v`，exit必须为`0`；
5. `codegraph sync`，exit必须为`0`；
6. `git diff --check <activation-child>..HEAD`与`git diff --check`作为同一item，两者均exit `0`。

Targeted原十二个selector必须继续使用`tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.<method>`，包括两个governance successor cases、C8十个ambient governance regression cases。不得减少selector来取得green。

每个log必须由单一owner以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr共用fd，child后flush/fsync/close再digest；artifact均regular、non-symlink、mode `0600`。Terminal strict JSON最后exclusive-create并seal，记录activation/corrective topology、pre/post identities、历史与current-HEAD branch ledger、每项exact argv/calls/exit/log bytes/SHA/mode、fail-fast、zero locks与retained状态。最后ER只append一次；append前除ER外clean，append后只允许ER dirty。

完整suite此前约两分钟，当前预计不超过10分钟；若Executer重新估算超过10分钟，必须使用Human可见macOS Terminal、三次稀疏liveness与automation流程，不得拆分规避。

## 7. 硬锁与停止点

Candidate probe/read/build、retained R3 probe/read/copy/repair、canonical retained validator、eligibility、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel和P8全部为`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

成功只表示C11代码和完整测试等待Planner验收；不得进入R3、release或后续阶段。失败不得重试、fallback、自行改PLAN或扩大scope。

**Planner stop：** `F19_CORRECTIVE_11_TERMINAL_WAITING_PLANNER`。
