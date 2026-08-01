# P7 retained-R3 Option B：D2-C1-R1 JSON-native projection 失败验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1-JSON-NATIVE-KIND-DISPATCHED-ATTRIBUTION-V1`

**Activation：** `07556fbc02a79c75cffab72749a35d84233ddb17`

**Evidence：** `12861cf73721a845e3fc2ad4b96858eb92726c5c`

**Planner 决定：** `REJECTED_PRECONTRACT_PLAN_VALUE_EXACT_TYPE_UNATTRIBUTED_NO_OWNER_OR_LINEAGE_CONCLUSION`

## 1. Reviewed scope、topology 与 evidence quality

Planner完整读取repo `AGENTS.md`、project skill、committed PLAN/FULL及ER最后完整section至physical EOF；用Git object、CodeGraph公开source和accepted parser对committed raw bytes做独立核验。未读取、stat、list、search、hash、复用或修复任何旧/fresh source/root，未运行owner selector、18-row Git ledger、physical inputs、canonical validator、release、network或device。

Activation `07556fbc02a79c75cffab72749a35d84233ddb17`是`7ac01b0d9a4be711ef96f82ebfe1da730667243c`的direct child，subject exact `chore(plan): canonicalize immutable machine row values`，changed paths exact且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1430-p7-retained-r3-d2-c1-json-native-review.md`

Evidence `12861cf73721a845e3fc2ad4b96858eb92726c5c`是activation direct child，subject exact `chore(evidence): record JSON-native kind-dispatched attribution`，changed path exact `.agent-work/EXECUTION_RESULT.md`。Review开始时HEAD exact evidence且worktree clean。

ER最后完整section含前导分隔LF的complete suffix为`4402` bytes、SHA-256 `29714973ffa1c46df9c6af8f62e09735f990f5e3ef19f2aa8122e1992cc85fad`，到physical EOF以exact LF结束。Handoff是一行strict JSON wrapper；activation/parser/archive/owner identity gates均通过，但没有fresh source/root、artifact、18-row或owner/Git-lineage evidence可供内容验收。

## 2. Independent type attribution 与 failure finding

Accepted parser owner `agent_work_machine_contract._deep_freeze`的公开语义是：exact JSON `dict`递归转为`types.MappingProxyType`，exact JSON `list`递归转为`tuple`，JSON scalar原值保留；strict loader已拒绝duplicate key与nonfinite constant。它不产生`frozenset`、set、bytes、Path、dataclass或任意自定义容器。`MachineContractEvidence.to_mapping()`则明确返回JSON-native `dict`，其中`candidate_lines`为`list`。

Planner对activation中committed PLAN/FULL raw bytes各读取、accepted parse一次并只遍历immutable graph type/path，得到：

- PLAN `.value`：`mappingproxy=46`、`tuple=49`、`bool=22`、`int=125`、`str=289`；不存在`None`、float或其他类型；root exact `mappingproxy`。
- FULL `.value`：`mappingproxy=1`、`bool=11`、`int=1`、`str=149`；不存在tuple、`None`、float或其他类型；root exact `mappingproxy`。
- PLAN/FULL `.evidence.to_mapping()`各自都是root exact `dict`，内部仅`list=1`、`int=6`、`str=7`。
- 所有mapping key均源自JSON object并为exact `str`；所有tuple均源自JSON array。Parser source identity为`9414` bytes、SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`、Git blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`。

Executer在`plan_value_json_native_projection`第一次调用即抛exact `TypeError: non-json-native value`。由于handoff未记录first forbidden type的type name/path，也未保留projection implementation identity，现有evidence不能区分controller是误拒绝root `mappingproxy`、nested `tuple`还是错误的type dispatch。上一PLAN虽然写了泛化的“ANY_MAPPING”语义，却未把accepted parser实际可产生的exact container types与一条可重放的typed traversal contract冻结为机器合同；因此不得再次盲目放行同类完整18-row运行。

失败严格发生在precontract：fresh source write/compile/invoke、fresh root create、contract/artifact writes、4次Git file acquisition、18次selector与18次ledger Git process、report/preterminal/terminal全部为0；retry/fallback均0。33项zero locks全部为0，retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`，production owner、lineage、manifest truth、eligibility与release结论均不存在。

## 3. Decision、residual risks 与 exact next branch

D2-C1-R1拒绝。唯一successor先执行pure read-only、pre-effect、bounded exact-type attribution与typed projection proof，不运行18-row diagnostic。它只能从activation committed PLAN/FULL raw bytes各取得一次并调用accepted parser各一次；随后以path-aware recursive walker验证exact类型域：parser `.value`只允许`MappingProxyType`、tuple、`NoneType`、bool、int、float、str，mapping key必须exact str、float必须finite；evidence mapping只允许dict、list及相同scalar域。`frozenset`及任何其他类型一律fail closed并记录first path/type，不得fallback。

Typed projection规则必须exact冻结：`MappingProxyType -> dict`递归且保留insertion order，`tuple -> list`递归，evidence中的dict/list分别递归复制为dict/list；`None`/bool/int/finite-float/str原值保留；任何其他类型、non-string key或nonfinite float拒绝。Projection不得修改、替换或alias parser immutable graph；projection前后对original graph重复type-path摘要必须相同。四个projection在内存完成canonical JSON serialization、strict reload与snapshot equality后即停，不创建任何fresh source/root/artifact，不运行owner/Git ledger。

Successor只允许把type-path counts、container paths、first forbidden type（成功时null）、四次projection与canonical round-trip结果、counters/zero locks作为单一canonical handoff追加ER physical EOF。成功仅证明typed projection boundary可供后续独立Planner包冻结，不证明18-row comparator、production owner、manifest truth、lineage、eligibility或release。

**Exact next reference：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1-C1`。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R1_C1_TYPED_PROJECTION_PROOF_WAITING_PLANNER_REVIEW`。

## 4. Required FULL updates（Orchestrator-owned）

- 将D2-C1-R1状态改为`REJECTED_PRECONTRACT_PLAN_VALUE_EXACT_TYPE_UNATTRIBUTED_NO_OWNER_OR_LINEAGE_CONCLUSION`并记录evidence commit `12861cf73721a845e3fc2ad4b96858eb92726c5c`。
- 将唯一active task/contract切换到上述`...D2-C1-R1-C1` typed projection proof；`active_task_count=1`。
- `real_self_check_owner_status`与`real_execution_status`改为blocked on D2-C1-R1-C1 acceptance。
- 保持`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator sole eligibility owner及device authorization false。

维护性判断：下一包只验证accepted parser与一次性controller之间的exact typed projection边界，不修改共享parser或production owner；通过小而可重放的type-path evidence阻止继续在大型diagnostic中复制模糊容器规则，无代码清理需求。
