# P7 retained-R3 Option B：P1-C1-R1 evidence-owner targeted failure Planner 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-EXACT-BYTES-IMMUTABLE-EXPECTATION-CORRECTION-V1`

## 1. 冻结 topology 与 evidence identity

- activation commit：`1dcde91f4eefd449e7f9739f590ff2f5789f0a57`；parent `aea9ce3769dea41348d739ee92b36fa2f47889a5`；subject exact `chore(plan): retry immutable parser correction with exact bytes`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1212-p7-retained-r3-b3-c3-c4-r5-r1-c1-activation-bytes-review.md`。
- evidence commit：`4b512ecb3b5caf34c25decb45f967f466c3b8909`；parent exact activation；subject exact `chore(evidence): record exact-bytes immutable parser correction`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- committed ER：bytes `1456629`；SHA-256 `bfe26818953b0e21b47c3fb40083a27903951e697f27242e339c0745d5ba0c7e`；blob `7821055cc48dfaa9d1fd016600a646775ed31a06`。最后handoff heading occurrence exact `1`，末节bytes `4289`，文件以LF结束。
- activation exact-bytes gate、archive identity、required FULL subset与preserved dirty identity均通过。source保持bytes `9414`、SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`、blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`。
- 本轮test-only patch后test为bytes `14278`、SHA-256 `a0d2a2298790e236fd6a58f393a62b25e44b487512077a3aeb4fb59fc333be2a`、blob `fce0395317f4ec1b2d75d918890eadf6694a3abf`。当前worktree exact two modified paths，无第三路径。

## 2. 执行事实与 validation quality

Executer按合同用raw Git bytes调用repo-owned PLAN/FULL parser，未做bytes到text转换；两次parser调用与FULL required subset comparison均通过。随后一次test-only patch加入recursive JSON semantic assertion adapter，生产source/parser owner write为`0`，deep-immutable `MappingProxyType`/tuple返回与独立container-type/mutation断言保持不变。

唯一targeted suite实际运行`15` tests，`14` pass、`1` fail；失败位于`test_generic_parser_supports_custom_marker_and_legacy_wrappers_delegate`的整份evidence mapping相等断言。Planner独立对照production owner逻辑确认：generic API从literal marker推导owner为`PLAN_MACHINE_CONTRACT`，legacy PLAN wrapper显式owner为`PLAN`；这两个owner有意不同。两者marker、source identity、candidate、line、row/payload hashes和line ending应相同，但测试错误要求包括owner在内的整份mapping相等。

失败后按fail-fast停止；focused/full、compileall、CodeGraph sync/post-query、diff/status、implementation commit与postcommit targeted均为`0`。没有real artifact、old root、self-check owner、validator、eligibility、release、network或device访问。

ER handoff先发生一次`AttributeError_list_has_no_decode`的heading-index内存处理错误，随后第二次heading-index读取成功，故实际reads `2` 超过预算 `1`。该偏差被canonical handoff如实记录；成功读取仍取得完整最后level-2 heading至physical EOF suffix，唯一apply_patch逐字重放该suffix并追加新节，append为最后副作用且postappend operations `0`。Orchestrator提交后Planner独立核对物理EOF、唯一heading和prefix延续成立。因此该偏差不破坏hand-off原子性或证据身份，不需要另建supersession；但不得把超预算记为合规成功。

## 3. Planner findings 与决定

**Decision：** `REJECTED_P1_C1_R1_COMPLETION_ACCEPTED_PHYSICAL_EOF_HANDOFF_DIRECT_TEST_ONLY_SUCCESSOR`。

P1-C1-R1不得获得implementation、focused/full validation或commit credit，因为targeted未全通过。保留当前exact two-path dirty diff：production source已经冻结且后续write必须为`0`；dedicated test只需一次bounded correction，把generic与legacy evidence的owner分别断言为`PLAN_MACHINE_CONTRACT`和`PLAN`，然后比较移除owner后的其余exact evidence fields。不得把两个owner强行统一，不得放宽production API，不得删除legacy wrapper owner distinction，也不得添加serializer、custom equality或parallel parser。

ER read budget偏差是已封存的执行偏差，不构成独立supersession前置条件。下一包仍必须使用一次完整末节到physical EOF的读取/append；若再次超预算或任一步失败，立即封存真实失败，retry/fallback为`0`。

这是测试/工程合同纠偏，不是色彩或测量科学问题，不需Advisor；设备与网络继续锁定，不需Human设备授权。

## 4. Residual risks 与 exact next branch

- 当前exact two-path实现尚未通过targeted/focused/full/compileall/CodeGraph及postcommit targeted，不可获得实现接受或R2解锁信用。
- 新测试必须既冻结distinct owner，也冻结其余evidence exact equality，避免用宽泛语义比较掩盖source/payload identity漂移。
- activation必须以evidence commit `4b512ecb3b5caf34c25decb45f967f466c3b8909`为parent，并保留当前exact two dirty identities；Orchestrator提交docs时不得误stage source/test。
- P1-C1-R1-C1验收前，R2 successor、real self-check owner、canonical validator、eligibility与release消费均继续硬锁。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1`，唯一distinct evidence-owner test correction与完整validation package。Planner stop为`B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_C1_EVIDENCE_OWNER_TEST_CORRECTION_WAITING_PLANNER_REVIEW`。

维护性判断：下一包只修正dedicated test对generic/legacy evidence owner的错误期望；production single parser owner、deep immutability和legacy wrapper边界均不变，不需架构重构。
