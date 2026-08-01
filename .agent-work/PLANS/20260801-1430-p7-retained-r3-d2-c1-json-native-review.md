# P7 retained-R3 Option B：D2-C1 immutable machine value JSON boundary 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-KIND-DISPATCHED-OWNER-EXPECTATION-ATTRIBUTION-V1`

**Activation：** `5030c6b7baf544e324df17a984aade60b6d6d533`

**Evidence：** `7ac01b0d9a4be711ef96f82ebfe1da730667243c`

**Planner 决定：** `REJECTED_PRECONTRACT_IMMUTABLE_MACHINE_VALUE_NOT_JSON_NATIVE_NO_ATTRIBUTION_CONCLUSION`

## 1. Reviewed scope、topology 与 evidence quality

Planner完整读取repo `AGENTS.md`、project skill、committed PLAN、ER最后完整section至physical EOF，以及FULL的machine row、task table和D2-C1 section；并用Git、CodeGraph与accepted parser source独立核对Executer handoff。未读取、stat、list、search、hash或复用失败fresh source/root，也未读取14个physical inputs、retained R3或任何更早failed/synthetic/D1/D2/real-self-check root；未调用real owner、validator、release、network或device。

Activation `5030c6b7baf544e324df17a984aade60b6d6d533`是`4bef083645b71e7cd13645ebd4eee78d9672ff24`的direct child，subject exact `chore(plan): correct owner expectation comparator dispatch`，changed paths exact且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1413-p7-retained-r3-d2-kind-dispatch-review.md`

Evidence `7ac01b0d9a4be711ef96f82ebfe1da730667243c`是activation direct child，subject exact `chore(evidence): record kind-dispatched owner attribution`，changed path exact `.agent-work/EXECUTION_RESULT.md`。Review开始时HEAD exact evidence且worktree clean。Activation归档identity `6276` bytes / SHA-256 `4055f6283092c825408b4343e783722e17ba04f74d9457c8427ecf0fd0ce0c78`通过。

ER最后完整section含前导分隔LF的complete suffix为`3702` bytes、SHA-256 `1fb3e42070f05d551f9cda225fe7e991f81e3ac767b344c70216a8fc3263bee0`，到physical EOF以exact LF结束。Handoff是一行strict JSON wrapper；activation/parser/archive/owner gate、failure phase、counters、zero locks与proof scope结构完整，但没有fresh artifact或18-row evidence可供内容验收。

## 2. Independent failure finding

Accepted parser owner的`_deep_freeze`将每层JSON object转换为`MappingProxyType`、array转换为tuple；`ParsedMachineContract.value`因此是不可变`Mapping`而非JSON-native dict。`MachineContractEvidence.to_mapping()`则明确返回deterministic JSON-serializable dict。D2-C1一次性controller在首个contract payload canonical serialization前将immutable parser value直接送入`json.dumps`，触发exact `TypeError: Object of type mappingproxy is not JSON serializable`。

该失败发生在fresh root创建后、首个contract write前：contract artifacts `0`、Git file acquisitions `0`、selector calls `0`、ledger Git attempts/processes `0`、report/preterminal/terminal writes `0`、canonical reloads `0`。因此本轮没有18-row comparator事实、first mismatch、owner-selector结论或Git-lineage结论；fresh source initial/post identity也未进入handoff。失败root与source必须永久视为immutable rejected evidence，successor不得读、stat、list、search、hash、复用或修复。

全部`31`项zero locks均为`0`，包括old roots、physical inputs、real owner entrypoints、owner ledger、repository source/test reads或writes、tests、compileall、CodeGraph、implementation commit、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal、public analyzer以及Executer对PLAN/FULL/archive的写入。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Decision、residual risks 与 exact next branch

D2-C1 execution拒绝，原因仅是一次性controller未跨越immutable-to-JSON boundary；不修改accepted shared parser、owner selector、repository production code或tests。Successor必须保留parser返回的immutable `.value`作为semantic gate source，另外以本地fail-closed recursive projection产生JSON-native snapshot：Mapping只接受str key并按原序投影为dict，tuple投影为list，`None`/bool/int/finite-float/str原值保留，其他类型拒绝；`.evidence.to_mapping()`也必须通过同一canonical JSON preflight。投影不得回写或替换parser owner value。

完整contract payload必须在fresh root创建和任何artifact/Git/selector effect前于内存完成strict canonical serialization与strict reload equality；只有该preflight通过才创建fresh root并write+seal contract。随后才允许按前一PLAN冻结的相同synthetic spec、四次Git file acquisition、18个owner selector调用、18个literal Git argv与kind-only comparators完成全新diagnostic。Retry/fallback均为`0`；不得只续跑失败点、读取失败root或复用其source。

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1`。它只可形成冻结synthetic spec下kind-dispatched subordinate diagnostic结论，不得形成production owner、manifest truth、lineage、eligibility或release结论，也不得调用real self-check owner、physical inputs、canonical validator、release、network、device、camera、Ray、strip、cleanup、formal或public analyzer。

Successor仍须在terminal落盘前从内存输出并flush唯一`PRETERMINAL_HANDOFF_JSON=`，包含source initial/post、root、six intended artifact identities、完整有序18-row matrix、first mismatch、counters及zero locks；terminal后不得为了handoff读取root。最后仅以一次complete-last-section-to-physical-EOF extraction和一次`apply_patch`追加ER canonical handoff；append为最后副作用。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R1_JSON_NATIVE_ATTRIBUTION_WAITING_PLANNER_REVIEW`。

维护性判断：影响仅限一次性offline controller的immutable/JSON serialization边界；共享parser与production owner保持单一所有权，不新增repository helper、validator或API，回归证据由fresh precontract gate与完整18-row rerun覆盖，无后续代码清理需求。
