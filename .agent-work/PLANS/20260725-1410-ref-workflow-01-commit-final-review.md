# REF-WORKFLOW-01 exact commit finalization Planner验收归档

**验收时间：** `2026-07-25T14:10:01-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`b1e8b381f0448efd016a55117fb4ccc4bccbf52e95fe0eb8532b0f8c63c76362`

**Planner决定：** `accepted_exact_commit; REF-WORKFLOW-01_complete`

**精确下一分支：** `HUMAN_OR_ORCHESTRATOR_PRIORITY_SELECTION_WAIT`

## 被审范围与结果

被审PLAN只授权机械验证13个已验收paths、一次explicit staging与一次focused commit，不允许文件编辑、tests/module/compile/
CodeGraph、network/device或P7恢复。Executor创建commit：

`3f8fb5c2f046ad5c75eab200005331acd5f2cc27`

并在commit后追加`.agent-work/EXECUTION_RESULT.md`第46节返回Planner门。

## Planner独立核验

1. commit parent exact为`8cd04d847d42ff5c7bcf7501f46be97cbbef429d`；subject为
   `fix(workflow): clarify local calibration context`，body exact为
   `Remove the built-in Ray credential default and document the user-owned local calibration boundary.`。
2. `git diff-tree --no-commit-id --name-status -r`恰好13项：8 modified、5 added，无extra/missing/duplicate；统计为
   `400 insertions / 211 deletions`。
3. commit tree中13项全部mode `100644`；Planner逐项live读取commit blob，bytes与SHA-256均exact匹配被审PLAN冻结表：

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `.agents/skills/camera-based-rgbww-optimizer/SKILL.md` | 4678 | `4619c131e1e733b9a9763312dfa463fecd45db80f7ea95476f2bbae4e46aa159` |
| `AGENTS.md` | 13909 | `a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5` |
| `docs/README.md` | 71254 | `38518c0c8d7524d17a036852f1854f757d1afc0f1b0100d1f21541b75d86a302` |
| `docs/engineering/p7-td-b-contract-history.md` | 4346 | `972ec515978f064a7339f7a2cbf028e794109c7d79cc95355456537e1c05c2c2` |
| `docs/local-lab-connection-boundary.md` | 2807 | `c33e78bc0b0fb23352a37b75c347d1a602a85d674e601d1c113c5712a823c84e` |
| `src/camera_based_rgbww_optimizer/control/camera_remote.py` | 34204 | `8fbe882c686606eda28e72c9b5d270681142bec262ff3f7f2fd4f7fe7657d097` |
| `src/camera_based_rgbww_optimizer/control/esphome.py` | 12538 | `0a5b6258fe3ea8519f697c4351eac9ac4243bbbabe0d30530f4c30564c972872` |
| `src/camera_based_rgbww_optimizer/control/local_lab_context.py` | 328 | `8c94d96b1dc9f9a959ee4988a89e80a68ac27faa2f132bf2d3aaed95a2bcd193` |
| `src/camera_based_rgbww_optimizer/control/ray120c.py` | 25132 | `16bc57834885a813e7b990b213513fb19ea7bd3ad935f59cd2ce44cd38b61c5d` |
| `tests/test_all_off.py` | 4013 | `1ef519f2098caed526df03f53eed9f4fe0e87cf24296246b4c1f40a71128258f` |
| `tests/test_local_lab_context.py` | 1152 | `81964d6bf13e6dace447f2d1686386f6128af2f9295f9e0184e99d870b256ea7` |
| `tests/test_project_context_docs.py` | 2042 | `1b5622d659d42ec29807e6fec4f1ec68d1e52bc83ba227ab4edffb60b7ac9e39` |
| `tests/test_ray120c.py` | 8430 | `b411e854effc0b21af05ba81671dccdd66e919429d1116b5d4fa10c9df30e956` |

4. 13个live working-tree files与commit blobs逐项SHA相同；相对new HEAD无authorized-path diff。HEAD exact为commit，index为空，
   remaining `git diff --check`通过。
5. current unrelated status仍只包含既有`.agent-work` PLAN/FULL/EXECUTION_RESULT/debug/review archive工作；与pre-stage ownership相比，
   仅13个authorized implementation paths按预期从dirty/untracked变为committed。无unrelated path被stage、commit、revert或删除。
6. `EXECUTION_RESULT.md`第46节hash为
   `6fbcbeea2d5e3a4b23862be18849d8ad78f019897e50574b77253add3f1e25b3`，记录stage `1`、commit `1`，implementation/docs/
   skill/test edits与test/module/compile/CodeGraph executions均`0`；push/tag/branch/PR、network/device/credential/secret reads、camera/
   Ray/strip/nonzero/Z0/E2/capture/formal/firmware/deployment全部`0`。
7. Planner本次只读Git objects、working-tree hashes、status与交接；未执行implementation/tests、访问network/device或创建commit。

## 验收决定与残余状态

接受exact commit，`REF-WORKFLOW-01`完成。此前验收的实现结论保持：focused `51/51`，skill `41300 -> 4678`，old exact credential
current count `0`；full `557/559`的两个errors为frozen committed HEAD上的TD-B lineage baseline coupling，不属于workflow regression。

完成表示仓库已移除Ray built-in credential default并准确记录Human-owned local calibration context；它只能降低possible platform
misclassification，不能保证平台分类结果，也不改变平台policy。

Human尚未重新排序实验工作。P7 lineage baseline debt、Z0-R2-C1及两个open engineering findings继续paused；本review不授权或自动恢复
P7、Z0、E2、device、formal或later stages。下一active PLAN必须是明确Human/Orchestrator priority-selection等待门；选择新reference后再由
Planner另写一个single executable package。
