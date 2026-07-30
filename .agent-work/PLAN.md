# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15：EQ-R6 non-evidence macOS metadata boundary

**计划状态：** `WAITING_ORCHESTRATOR_REVIEWED_STATE`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-15-EQ-R6-METADATA-BOUNDARY`

**唯一当前动作：** Orchestrator验收C14 Planner review、更新其独占的
`.agent-work/FULL_PLAN_REFERENCE.md`，并将C14 ER、review archive、本C15 PLAN与FULL整理为一个focused
reviewed-state commit；然后由Planner在clean reviewed-state parent上补写exact PLAN-only activation topology。当前状态
不授权Executer编辑、测试、创建root、提交或执行下述implementation；activation未完成前必须停止。

**C14 review archive：**
`.agent-work/PLANS/20260730-0825-p7-retained-r3-option-b-b1a-c3e6f19-corrective-14-review.md`，
bytes `5792`，SHA-256
`febe5afa8dd3d4597ecafcc1778c73181a14ba3b91877813afbb5909a7a13685`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_15_eq_r6_metadata_boundary_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-15-EQ-R6-METADATA-BOUNDARY","dispatch_state":"waiting_orchestrator_reviewed_state","execution_authorized":false,"single_current_action":"orchestrator_review_full_update_and_focused_reviewed_state_commit","review_archive":{"path":".agent-work/PLANS/20260730-0825-p7-retained-r3-option-b-b1a-c3e6f19-corrective-14-review.md","bytes":5792,"sha256":"febe5afa8dd3d4597ecafcc1778c73181a14ba3b91877813afbb5909a7a13685"},"c14":{"dispatch_head":"d61accd5b1eac975874a128db949fddb594d34e8","terminal_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/20260730T141613Z/terminal-evidence.json","terminal_sha256":"0439ff6136737d41b168409a113f7df12e0794638eed39777cdfdf6f8b27e8fe","decision":"rejected_full_suite_eq_r6_manifest_metadata_drift"},"future_activation":{"required":true,"required_parent":"planner_must_freeze_after_orchestrator_review","changed_paths":[".agent-work/PLAN.md"],"additional_paths":0,"commit_count":1,"initial_clean_required":true},"implementation":{"changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_contract.py"],"additional_paths":0,"commit_count":1,"scope":"exact_root_ds_store_metadata_boundary_only"},"immutable":{"accepted_root_rewrites":0,"manifest_sha256":"41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9","artifact_hash_rewrites":0,"canonical_eligibility_owner":"audit_td_b_eq_r6_qualification"},"validation":{"compileall":1,"targeted_selector_count":6,"focused_modules":["tests.test_p7_td_b_r6_contract","tests.test_p7_thermal_diagnostics","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"full_suite":1,"codegraph_sync":1,"diff_check":1,"retry":0,"fallback":0},"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_15_TERMINAL_WAITING_PLANNER"}`

## 1. C14 decision与冻结根因

C14不得验收为validation green：compileall、exact targeted `13/13`与focused `125/125`通过，但完整套件运行
`687`项后有`2`项失败，CodeGraph与diff因fail-fast未运行。Authoritative terminal为：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/20260730T141613Z/terminal-evidence.json`

其bytes `9185`、mode `0600`、SHA-256
`0439ff6136737d41b168409a113f7df12e0794638eed39777cdfdf6f8b27e8fe`。替代Executer的pre-root no-op不是retry
evidence；C14 retry/fallback仍为`0/0`。

失败根因冻结为accepted EQ-R6 root顶层新增的普通Finder metadata：

- accepted root exact：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928`；
- relative path exact：`.DS_Store`；
- type：regular file；mode `0644`；bytes `6148`；
- SHA-256：`c1249bc621a24778654848bfca63249d4e79c6f9bf93bb3b0337fe53e33541b6`；
- manifest counters从`(47,42,5,0,0,7980)`变为`(48,43,5,0,0,8119)`；
- 第二个artifact-drift负例仅因同一manifest drift被提前截断。

该`.DS_Store`不是资格artifact。不得删除、修改、chmod、移动或重建它来取得green；accepted root、C14 root、四个
canonical artifacts与所有旧evidence必须只读。

## 2. Orchestrator review与后续activation gate

在任何Executer dispatch前，Orchestrator必须先：

1. 验收C14 review决定与本C15 branch；
2. 更新其独占的FULL reference；
3. 将当前dirty worktree按AGENTS要求分类整理并创建一个focused reviewed-state commit；
4. 留下clean worktree，并将exact commit、parent、subject与changed paths交回Planner。

Planner随后只可修改`.agent-work/PLAN.md`，把本节替换为exact reviewed-state parent与exact PLAN-only activation
commit合同，创建一个PLAN-only activation commit并核验commit前后clean。Executer不得消费
`waiting_orchestrator_reviewed_state`状态，不得预测或手抄activation child SHA；activation后dispatch HEAD必须由controller
一次programmatic `git rev-parse --verify HEAD^{commit}`读取并冻结，second read与human-transcribed expected child SHA均为`0`。

## 3. Exact implementation scope

Activation通过后，Executer只可编辑两个路径：

1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
2. `tests/test_p7_td_b_r6_contract.py`

Additional paths `0`。只可创建一个implementation commit，建议subject exact为
`fix(p7): exclude root Finder metadata from EQ evidence`。不得编辑config、GUIDE、PLAN、FULL、archive、旧ER、
accepted root或任何外置evidence；ER只可在terminal seal后append一次且不得stage。

实现必须保持`build_planner_eq_family_manifest`为唯一family manifest owner，并满足：

- 只将root-relative path exact等于`.DS_Store`的regular file分类为非证据macOS metadata；
- 必须先对每个path执行现有`lstat`安全分类；`.DS_Store`若为symlink、directory或unsupported type不得被忽略，须按
  现有fail-closed边界拒绝或进入manifest造成drift；
- 仅在确认其为regular file且relative exact为`.DS_Store`后，才可在rows、entries、files与payload序列化前跳过；
- 禁止使用basename-only、suffix、glob、prefix、substring或generic path allowlist；`nested/.DS_Store`、`._*`、
  `.Spotlight-V100`及其他未知文件不得被忽略；
- 不得读取、解析或依赖`.DS_Store`payload，也不得将其bytes/hash/mode绑定为资格输入；
- 原47-entry证据rows、ordering、payload与SHA必须byte-exact不变；不得更新
  `TD_B_EQ_R6_MANIFEST_SHA256 = 41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9`；
- `TD_B_EQ_R6_ARTIFACT_SHA256`四项、qualification checkpoint、accepted root constant及所有scientific fields均不得改；
- `audit_td_b_eq_r6_qualification`仍是唯一canonical eligibility/qualification owner；不得新增fallback、第二owner、
  auto-repair、artifact regeneration或eligibility emission路径。

## 4. Meaningful dedicated tests

Dedicated test路径必须新增或强化以下真实行为；测试不得修改真实accepted root：

1. `test_manifest_ignores_only_root_regular_ds_store`：在mode `0700`临时root建立基线证据，添加root regular
   `.DS_Store`后manifest的rows、counters、payload和SHA与基线完全相等；改变其payload后仍相等，证明它不成为
   eligibility input。
2. `test_manifest_does_not_hide_unsafe_or_nested_ds_store`：root `.DS_Store` symlink必须以symlink错误fail closed；
   `nested/.DS_Store`必须继续出现在rows并改变manifest，而不是被宽泛basename过滤。
3. 现有`test_exact_family_manifest_matches_frozen_digest_and_qualification`必须在真实只读accepted root存在顶层
   `.DS_Store`时恢复原`47/42/5/0/0/7980`与冻结SHA，并完成qualification。
4. 现有`test_qualification_rejects_wrong_root_and_artifact_hash_drift`必须先通过family manifest gate，再准确到达
   `artifact drifted`负例。
5. 现有serializer、symlink与unsupported filesystem type负例继续通过；未知regular file仍进入manifest，不能被
   新metadata边界隐藏。

## 5. Brand-new C15 evidence root与commit topology

Executer只能在prefix
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-15-offline/`
下以一个冻结UTC child name exclusive-create mode `0700` root。若exact child已存在立即hard-fail；不得删除、复用、
改名或读取C14/C13/C12 execution roots。Root count `1`，retry `0`，fallback `0`。

实现前冻结两个allowed paths的blob/bytes/SHA；实现后核验working diff exact two paths、additional `0`，再创建exact one
implementation commit。Commit后核验direct parent是activation child、subject exact、changed-path set exact two paths；
任何不符fail closed。每个log必须single owner以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`单fd承载stdout/stderr，
flush/fsync/close后digest；artifact须regular、non-symlink、mode `0600`。

## 6. Exact targeted与one-shot validation chain

Targeted命令必须恰好按顺序包含以下`6`个selector，每项只出现一次：

1. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_ignores_only_root_regular_ds_store`
2. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_does_not_hide_unsafe_or_nested_ds_store`
3. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_exact_family_manifest_matches_frozen_digest_and_qualification`
4. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_serializer_and_unsafe_types_fail_closed`
5. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_qualification_rejects_wrong_root_and_artifact_hash_drift`
6. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_rejects_other_filesystem_types`

Implementation commit topology通过后，在同一C15 root依次运行，每项exactly once、fail-fast：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_td_b_r6_contract.py`；exit `0`；
2. `.venv/bin/python -m unittest -v <上方exact 6 selectors>`；`6/6`、exit `0`；
3. `.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_agent_work_machine_contract tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_release_audit`；exit `0`；
4. `.venv/bin/python -m unittest discover -s tests -v`；exit `0`；
5. `codegraph sync`；exit `0`；
6. `git diff --check <activation_parent>..<implementation_commit>`与`git diff --check`作为同一item各调用一次且均exit
   `0`；前者changed paths必须恰为activation PLAN path加exact source/test implementation paths，后者在ER append前必须empty。

不得用targeted/focused green替代full suite。既有full suite约三分钟，本包预计小于10分钟；若dispatch前重新估算超过
10分钟，须遵守Human可见macOS Terminal、三次稀疏liveness与automation流程，不得拆分命令规避。

## 7. Terminal、ER与停止点

Terminal strict JSON必须最后exclusive-create、fsync、reload、digest与seal，至少记录activation/implementation topology、
programmatic frozen HEAD、root/FD lifecycle、before/after identities、exact metadata classification、冻结manifest/artifact hashes、
6-selector argv、compileall/targeted/focused/full/CodeGraph/diff calls/exits/log identities、repo diff、retry/fallback与所有locks。

Terminal seal后只可向`.agent-work/EXECUTION_RESULT.md`append一次C15结果，记录terminal path/bytes/SHA、validation counts与
Planner decision request。不得编辑PLAN/FULL、重写旧ER或stage/commit ER。

Candidate、retained R3、canonical retained validator、eligibility emission、release generation/qualification/consumption、
network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel与P8全部为`0`。
Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。本包是offline provenance engineering纠偏，不需要Advisor或Human
授权；成功也只回到Planner验收门，不得解锁后续阶段。

**Planner stop：** `F19_CORRECTIVE_15_TERMINAL_WAITING_PLANNER`。
