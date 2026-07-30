# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10：C9 draft baseline preservation gate

**计划状态：** `NON_EXECUTABLE_ORCHESTRATOR_ALIGNMENT_REQUIRED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-10-DRAFT-BASELINE`

**唯一当前动作：** Orchestrator亲自分类并提交C9遗留的exact source/config未验证草稿，更新
`FULL_PLAN_REFERENCE.md`冻结C9 rejection与C10 baseline，再交新的Planner pass编写C10 executable package。
本PLAN不授权Executer、测试、compileall、CodeGraph、candidate、retained R3、release或任何设备操作。

**C9 review archive：**
`.agent-work/PLANS/20260729-2357-p7-retained-r3-option-b-b1a-c3e6f19-corrective-9-review.md`，SHA-256
`0463db1e302bb4a672845c8e98239aafc0a51928868dad734f69a2db11a47c3e`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_10_draft_baseline_gate_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-10-DRAFT-BASELINE","dispatch_state":"non_executable_orchestrator_alignment_required","single_current_action":"orchestrator_preserve_exact_c9_drafts_and_align_c10","reviewed_head":"bc13f50dfab9c2724d883befb2988f11548ccbe6","draft_commit":{"required_parent":"bc13f50dfab9c2724d883befb2988f11548ccbe6","subject":"chore(p7): preserve unvalidated governance successor draft","changed_paths":["config/hsi/p7-governance-lineage-successor-v1.json","src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py"],"commit_count":1,"validation_claim":false},"draft_identities":{"config":{"state":"ignored_untracked_force_add_exact_path_only","blob":"46acad9b1992196cbcdb381718ea9b2dfda31e3b","bytes":2574,"sha256":"7ff96378e76c5b450c44db55d5b5eee922afe084bb0ea37d837a6f12db928795"},"source":{"baseline_blob":"ccb8558b585abcb5d6b439fabbbeb865949dda57","working_blob":"6d274d59b60dcd38b26cb14d092bb7cd31d30d2e","bytes":191641,"sha256":"7030305c1a4b5e829fc8966880e80139a9e2a345453e7cf2766651c0039525f1"},"test":{"state":"unchanged_not_in_draft_commit","blob":"16e91ee1e1fac64062c511b96f2f320b7ee6c806","bytes":194978,"sha256":"7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a"}},"c9_terminal":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/20260730T001500Z/terminal-evidence.json","sha256":"b5cb63fdbe9f51c22f582616eb7494b845ca55122575da415a96a501a4da5847","reusable":false},"next_executable_branch":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10-IMPLEMENT-AND-VALIDATE","fresh_validation":{"new_root_required":true,"c9_root_reuse":false,"formal_chain_invocations_per_item":1,"retry":0,"fallback":0},"locks":{"executer_dispatch":0,"compileall":0,"tests":0,"codegraph":0,"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_10_BASELINE_WAITING_ORCHESTRATOR"}`

## 1. C9 review decision

C9整体判定为`REJECTED_FORMAL_COMPILEALL_CONSUMED_BEFORE_IMPLEMENTATION_COMMIT`。唯一compileall在implementation
commit前运行，且argv缺少PLAN冻结的`tests/test_p7_thermal_diagnostics.py`。由于正式链每项预算为1且retry/fallback为0，C9不能重跑、
不能继续commit，也不能把该syntax green解释为正式验证。

C9 fresh root及其中所有artifact均已消费，只读保留；不得复用、补写、重建或把其结果计入C10。C9 terminal exact为：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/20260730T001500Z/terminal-evidence.json
SHA-256 b5cb63fdbe9f51c22f582616eb7494b845ca55122575da415a96a501a4da5847
```

## 2. Orchestrator exact draft-preservation commit

Orchestrator须从当前activation HEAD `bc13f50dfab9c2724d883befb2988f11548ccbe6`亲自创建一个且仅一个draft-preservation
commit：

- direct parent exact为上述HEAD；
- subject exact为`chore(p7): preserve unvalidated governance successor draft`；
- changed paths exact为：
  1. `config/hsi/p7-governance-lineage-successor-v1.json`；
  2. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`；
- config因`config/hsi/*`规则被ignore，只可对上述exact path执行force-add；不得force-add目录、glob或任何其他ignored config；
- commit bytes必须等于machine contract冻结的blob/bytes/SHA；
- `tests/test_p7_thermal_diagnostics.py`不得stage或修改；
- `.agent-work/EXECUTION_RESULT.md`、本PLAN、review archive与未来FULL更新不得混入draft commit；
- 不运行compileall、test、CodeGraph或其它验证命令；此commit只表示保留未验证草稿，不表示实现通过。

若任一draft identity漂移、出现第三个staged path或parent不符，Orchestrator停止并重新交Planner，不得自行接受变化。

## 3. Orchestrator governance alignment

Draft commit成功后，Orchestrator更新且只由自己更新`FULL_PLAN_REFERENCE.md`：

- 将C9标记为上述rejection并记录review archive、terminal及preserved-draft commit；
- 将C10标为等待fresh Planner executable package；
- 保留旧AGENTS policy freeze、workflow manifest、public-default successor payload与canonical eligibility owner；
- 保留所有R3/release/device/scientific locks及`RETAINED_UNVALIDATED_UNCONSUMED`状态。

随后Orchestrator以focused governance commit提交exact review state；最小路径集为
`.agent-work/EXECUTION_RESULT.md`、本PLAN、本review archive与`FULL_PLAN_REFERENCE.md`。不得把其它源码、测试、config或无关用户修改混入。
提交后worktree须clean，再启动新的Planner pass；不得直接dispatch Executer。

## 4. 下一C10 executable package必须冻结的合同

新的Planner从clean preserved-draft baseline编写唯一
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10-IMPLEMENT-AND-VALIDATE` package：

1. 明确冻结preserved config/source commit、blob与SHA，冻结仍未修改的test baseline；
2. 至少新增C9要求的positive case与完整negative matrix；
3. 精确列出successor implementation commit的direct parent、subject、changed paths及before identities；不得使用可选路径、generic allowlist或
   隐式扩大scope；
4. 若Planner审查发现source/config草稿还需修正，须把每个待改路径精确纳入successor implementation commit；否则只允许test路径；
5. implementation commit完成并验证后，才在brand-new `0700` root运行完整formal chain。compileall、targeted、focused、full、CodeGraph与
   diff-check每项最多一次，fail-fast，retry/fallback为0；C9的compileall不得计入也不得复用；
6. full suite必须exit 0，且C8十个ambient-governance失败case及新successor cases全部通过；focused green不得覆盖full failure；
7. terminal/evidence继续使用C8已验收的single-fd exclusive-create日志owner，并在最后seal；若预计超过10分钟，使用AGENTS规定的
   visible Terminal、三次稀疏liveness与automation流程。

## 5. 持续硬锁与停止点

本包及下一离线C10均不授权candidate path probe/read/build、retained R3 path probe/read/copy/repair、canonical retained validator、
eligibility emission、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、
public analyzer、TD-C、sentinel或P8。旧governance payload不得改写、复制或重建。Retained R3继续为
`RETAINED_UNVALIDATED_UNCONSUMED`。

这是工程provenance与执行生命周期问题，不需要Advisor科学决策或Human高风险设备授权。

**Planner stop：** `F19_CORRECTIVE_10_BASELINE_WAITING_ORCHESTRATOR`。
