# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16：retained metadata-boundary validation-only successor

**计划状态：** `PLANNER_REVIEWED_WAITING_ORCHESTRATOR`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-16-RETAINED-METADATA-BOUNDARY-VALIDATION`

**唯一当前动作：** Orchestrator验收C15 rejection、更新FULL并提交reviewed state；随后Planner只可将该exact reviewed-state
commit冻结为PLAN-only activation parent并把本包转为Executer-authorized。当前不得dispatch Executer、运行validation或执行
任何后续工作。

**C15 review archive：**
`.agent-work/PLANS/20260730-0837-p7-retained-r3-option-b-b1a-c3e6f19-corrective-15-review.md`，bytes `5301`，SHA-256
`f1a5f7300248aa74176c363f0d128bfb2214890572a16019b3d4e2ca5464afd3`；Orchestrator须独立复算。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_16_retained_validation_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-16-RETAINED-METADATA-BOUNDARY-VALIDATION","dispatch_state":"planner_reviewed_waiting_orchestrator","execution_authorized":false,"single_current_action":"orchestrator_review_full_update_and_reviewed_state_commit","activation":{"required_parent":"TO_BE_FROZEN_AFTER_ORCHESTRATOR_REVIEW","subject":"chore(plan): activate f19 corrective 16","changed_paths":[".agent-work/PLAN.md"],"additional_paths":0,"commit_count":1},"retained_implementation":{"commit":"3a14fe0bd663250dd48c65e71f1a6550df89267f","parent":"431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53","subject":"fix(p7): exclude root Finder metadata from EQ evidence","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_contract.py"],"additional_paths":0,"commit_count":1},"repository_mutations":{"source_edits":0,"test_edits":0,"config_edits":0,"implementation_commits":0},"validation":{"compileall":1,"targeted_selector_count":6,"focused_modules":["tests.test_p7_td_b_r6_contract","tests.test_p7_thermal_diagnostics","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"full_suite":1,"codegraph_sync":1,"diff_check":1,"retry":0,"fallback":0},"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_16_TERMINAL_WAITING_PLANNER"}`

## 1. C15 decision与保留实现

C15以`REJECTED_PREVALIDATION_EVIDENCE_ORDER`结束。实现提交
`3a14fe0bd663250dd48c65e71f1a6550df89267f`的parent、subject与exact source+test两路径拓扑均通过，但编辑/commit发生在
brand-new C15 root与before-identity artifact创建之前；因此由parent重建的before identity不能冒充pre-edit freeze。C15的
compileall、targeted、focused、full、CodeGraph与diff调用均为`0`，retry/fallback `0/0`。

C16必须保留该实现提交，不得amend、cherry-pick、rebase、重做、编辑或创建新implementation commit。C16只证明：在验证开始
之前，从immutable Git objects得到的parent-before与retained-commit-after identities、exact commit topology及完整验证结果。

## 2. Planner activation gate（当前尚未授权）

Orchestrator完成reviewed-state commit后，Planner必须独立验证工作区clean，将该commit full SHA冻结为activation direct parent，
并仅修改本PLAN中的状态、machine contract与exact parent。Activation commit subject必须exact为
`chore(plan): activate f19 corrective 16`，changed paths exact `.agent-work/PLAN.md`，additional `0`，commit count `1`。

Executer controller启动时从clean worktree一次programmatic执行`git rev-parse --verify HEAD^{commit}`，冻结结果为dispatch HEAD；
second HEAD read与human-transcribed child SHA均为`0`。它必须验证dispatch commit direct parent、subject、PLAN-only path set，
任一不符须在创建root、读取retained identity或运行validation前hard-fail。

## 3. Immutable retained topology与identity contract

在任何validation调用前，controller必须programmatically验证：

- retained commit exact `3a14fe0bd663250dd48c65e71f1a6550df89267f`；
- direct parent exact `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`；
- subject exact `fix(p7): exclude root Finder metadata from EQ evidence`；
- changed paths exact：
  `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`与
  `tests/test_p7_td_b_r6_contract.py`；additional paths `0`、commit count `1`；
- canonical binary patch SHA-256 exact
  `018cf00c4e452673f4303ce528fbea2c0b6667e8dc691f5ff44c6968603412de`。

Identity必须从commit-qualified Git object读取，不得从ambient working-tree bytes推断：

| path | parent-before blob / bytes / SHA-256 | retained-after blob / bytes / SHA-256 |
| --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | `efcb4b05877e857b47eebcb3d7e07dbf5979698f` / `193853` / `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64` | `2d65c51200688e71dacc531e2e99b1240b4649d5` / `193918` / `d81a504c3eb2df654f493bd8cfa94189a4cb6673c0ef24fb9c183834a0bac93e` |
| `tests/test_p7_td_b_r6_contract.py` | `4bc6a791972ad04693015961c0d43c57865305db` / `102435` / `10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23` | `3a2397d8d02ff85388c4a5dfb87333721871dbcb` / `104738` / `77ef59ccee5eee34d85658aadf7a6ce40f413fee9b8395cd11fb82145df27104` |

Evidence必须明确记录`derived_prevalidation_from_git_objects=true`与`recorded_before_historical_edit=false`；不得使用
`pre_edit_freeze=true`或任何等价误述。Working tree同路径必须与retained-after identities一致，否则在validation前fail closed。

## 4. Brand-new C16 evidence root与artifact lifecycle

Executer只可在prefix
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-16-offline/`下以一个冻结UTC
child name exclusive-create mode `0700` root。若exact child已存在立即hard-fail；不得删除、复用、改名或读取C15及更早
execution roots。Root count `1`、retry `0`、fallback `0`。

Root创建后、任何validation调用前，必须把第3节的topology与identity结果写入single-owner
`prevalidation-git-object-freeze.json`：`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`、single fd、flush/fsync/close、mode
`0600`、strict JSON reload与digest。该artifact须同时记录Git命令argv/exit、exact object spec、bytes/hash计算方法及上述两个
truth labels。失败须terminal seal并停止，不得改写或fallback。

每个validation log也须single owner、exclusive/no-follow、mode `0600`，在digest前flush/fsync/close；terminal strict JSON最后
exclusive-create、fsync、reload、digest与seal。

## 5. Exact one-shot validation chain

Targeted命令必须按下列exact顺序包含`6`个selector，每项只出现一次：

1. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_ignores_only_root_regular_ds_store`
2. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_does_not_hide_unsafe_or_nested_ds_store`
3. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_exact_family_manifest_matches_frozen_digest_and_qualification`
4. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_serializer_and_unsafe_types_fail_closed`
5. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_qualification_rejects_wrong_root_and_artifact_hash_drift`
6. `tests.test_p7_td_b_r6_contract.EqFamilyManifestTests.test_manifest_rejects_other_filesystem_types`

Prevalidation freeze成功后，在同一C16 root依序执行，每项exactly once、fail-fast：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_td_b_r6_contract.py`；exit `0`；
2. `.venv/bin/python -m unittest -v <上方exact 6 selectors>`；`6/6`、exit `0`；
3. `.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_agent_work_machine_contract tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_release_audit`；exit `0`；
4. `.venv/bin/python -m unittest discover -s tests -v`；exit `0`；
5. `codegraph sync`；exit `0`；
6. `git diff --check 431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53..3a14fe0bd663250dd48c65e71f1a6550df89267f`与
   `git diff --check`作为同一item各调用一次且均exit `0`；前者changed paths必须exact source+test，后者在ER append前必须empty。

不得用targeted/focused green替代full suite。既有full suite约三分钟，本包预计小于10分钟；若dispatch前估算超过10分钟，须
遵守Human可见macOS Terminal、三次稀疏liveness与automation规则，不得拆分规避。

## 6. Immutable owners、locks与acceptance

`build_planner_eq_family_manifest`仍是唯一family manifest owner；`audit_td_b_eq_r6_qualification`仍是唯一canonical
eligibility owner。`TD_B_EQ_R6_MANIFEST_SHA256`必须保持
`41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9`，四项artifact SHA、accepted root、qualification
checkpoint与所有scientific fields不得改。不得生成eligibility或消费release。

Acceptance必须同时满足：activation gate、retained topology、prevalidation Git-object identity freeze、working tree after identity、
compileall、targeted `6/6`、focused、full、CodeGraph及两项diff全部green；validation调用各`1`，retry/fallback `0/0`，ER append
`1`。任何失败均fail-fast进入Planner门，不得重试。

Candidate、retained R3、canonical retained validator、eligibility emission、release generation/qualification/consumption、network、
`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel与P8全部为`0`。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。本包是offline provenance validation，不需要Advisor或Human授权。

## 7. Terminal、ER与停止点

Terminal至少记录activation与retained topology、programmatic HEAD、root/FD lifecycle、prevalidation freeze identity、truth labels、
exact selector argv、各validation call/exit/log identity、repo diff、retry/fallback和全部locks。Terminal seal后只可向
`.agent-work/EXECUTION_RESULT.md`append一次；不得编辑PLAN/FULL/archive、重写旧ER、stage或commit ER。

成功也只回到Planner验收门，不得解锁retained-R3、release、FORMAL或设备阶段。

**Planner stop：** `F19_CORRECTIVE_16_TERMINAL_WAITING_PLANNER`。
