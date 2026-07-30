# F19 Corrective-15 Planner Review

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-15-EQ-R6-METADATA-BOUNDARY`

**Review date：** `2026-07-30`

**Decision：** `REJECTED_PREVALIDATION_EVIDENCE_ORDER`

## Reviewed scope and method

本次只读审查active PLAN、C15 terminal seal、`.agent-work/EXECUTION_RESULT.md`的单次C15 append，以及Git中
activation与implementation commit的parent、subject、changed-path set和两个允许路径的before/after blob。未运行
controller、compileall、测试、CodeGraph、diff validation、retained-R3 validator、release、网络、设备、相机、Ray、strip、
cleanup、formal或public analyzer；未修改生产代码、测试、FULL、ER或外置证据。

审查时HEAD为`3a14fe0bd663250dd48c65e71f1a6550df89267f`，仅
`.agent-work/EXECUTION_RESULT.md`为dirty path。C15 active PLAN bytes `13017`、SHA-256
`c721820041cd73bc2a40290bb63e6f60c2c2cccc6bb44da17b3fbf51fa121c59`。

## Authoritative evidence

- Root：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-15-offline/20260730T143516Z`，
  mode `0700`。
- Terminal：同root下`terminal-evidence.json`，bytes `3693`、mode `0600`、strict JSON可解析、SHA-256
  `507747e10989e4acd57274a013d512c21015a7bd05607deba17a3a61716a406e`。
- Programmatic dispatch HEAD：`431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`；read count `1`、second read `0`、
  human-transcribed expected child SHA count `0`。
- Activation commit direct parent `15c8a8416333b655fa09351eec2bcab8f198580d`，subject exact
  `chore(plan): activate f19 corrective 15`，changed path exact `.agent-work/PLAN.md`。
- Retained implementation commit `3a14fe0bd663250dd48c65e71f1a6550df89267f`，direct parent exact
  `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`，subject exact
  `fix(p7): exclude root Finder metadata from EQ evidence`，changed paths exact：
  `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`与
  `tests/test_p7_td_b_r6_contract.py`，additional paths `0`，commit count `1`。
- Canonical binary patch SHA-256：
  `018cf00c4e452673f4303ce528fbea2c0b6667e8dc691f5ff44c6968603412de`。
- Source before（implementation parent）：blob `efcb4b05877e857b47eebcb3d7e07dbf5979698f`、bytes `193853`、SHA-256
  `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`；after：blob
  `2d65c51200688e71dacc531e2e99b1240b4649d5`、bytes `193918`、SHA-256
  `d81a504c3eb2df654f493bd8cfa94189a4cb6673c0ef24fb9c183834a0bac93e`。
- Test before（implementation parent）：blob `4bc6a791972ad04693015961c0d43c57865305db`、bytes `102435`、SHA-256
  `10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23`；after：blob
  `3a2397d8d02ff85388c4a5dfb87333721871dbcb`、bytes `104738`、SHA-256
  `77ef59ccee5eee34d85658aadf7a6ce40f413fee9b8395cd11fb82145df27104`。
- Validation calls（compileall/targeted/focused/full/CodeGraph/diff）全部`0`；retry/fallback `0/0`；ER append `1`。
- Candidate、retained R3、canonical validator、eligibility、release、network、`.env`、device、camera、Ray、strip、
  cleanup、formal、public analyzer、TD-C、sentinel与P8调用全部`0`。Retained R3保持
  `RETAINED_UNVALIDATED_UNCONSUMED`。

## Finding and decision

C15实现提交的Git拓扑与exact两路径边界均符合PLAN，terminal也诚实记录了失败；但Executer先完成编辑与commit，后创建
C15 root并记录before identities。由implementation parent重建出的before blob是可验证的历史Git事实，却不是PLAN要求的
pre-edit freeze。C15因此不能宣称满足证据顺序，也没有运行任何验证链，必须以
`REJECTED_PREVALIDATION_EVIDENCE_ORDER`结束。

该缺口不要求丢弃或重做`3a14fe0...`。C16应把它作为immutable retained implementation：在任何validation调用前创建
brand-new root，从其direct parent Git tree派生before identity、从retained commit Git tree派生after identity，并明确标注
`derived_prevalidation_from_git_objects=true`、`recorded_before_historical_edit=false`。这样既不伪称历史时序，也可对保留提交
执行完整one-shot验证。

残余风险是controller再次把“prevalidation Git-object freeze”误写成“pre-edit freeze”，或从working tree而非exact commit
object取identity。C16必须以commit-qualified `git ls-tree`/`git show`为owner，先seal identity artifact，再运行验证；source、
test、config与旧证据均不可编辑。

这是offline provenance engineering问题，不需要Advisor科学指导或Human设备授权。

## Exact next branch

下一分支唯一为`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16` validation-only successor。Orchestrator先验收本review、更新
FULL并创建focused reviewed-state commit；Planner随后只把该commit冻结为PLAN-only activation parent并授权Executer。
Executer不得编辑或创建implementation commit，只可在brand-new C16 root验证retained `3a14fe0...`的exact拓扑、从Git对象
冻结before/after identities，然后依次运行compileall、exact targeted 6、focused、full、CodeGraph与diff one-shot链并停止在
Planner门。所有retained-R3、release、设备及后续阶段继续锁定。
