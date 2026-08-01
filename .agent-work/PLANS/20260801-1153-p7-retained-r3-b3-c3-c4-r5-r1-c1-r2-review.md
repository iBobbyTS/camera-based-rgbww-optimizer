# P7 retained-R3 Option B：R5-R1-C1-R2 Planner 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-CONTEXT-BOUND-CORRECTED-GIT-PROVENANCE-REAL-MANIFEST-SELF-CHECK-V1`

**Reviewed PLAN identity：** bytes `19334`；SHA-256 `33de8dcb4d5d001e2d9795236d7e2888a3086fbb76bae0451a9a0a0600464399`。

## 1. 冻结输入与证据身份

- activation commit：`5b0d7259c1c6a1211f8981ea0d41ac0832a7e7c6`；parent `66ecbcf31cf016bd3dc4611ba47cf62ca7b599ee`；subject exact `chore(plan): retry corrected real Git provenance owner`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1143-p7-retained-r3-b3-c3-c4-r5-r1-c1-r1-s1-acceptance.md`。
- evidence commit：`89099740bc0b4fa8babc3be233a5f53ab3d697b2`；parent exact activation；subject exact `chore(evidence): record context-bound corrected real self-check`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- ER before/after blob：`7d74326d262695be15300269263f829a73a1f62c` → `d09feebfb5f46f559a0b643ff59ffa58e806592b`。
- ER after：bytes `1444645`；SHA-256 `b88756516378f152795d7a78876305b8b3b6de881bf66eafd303c0b19463bf55`。
- canonical handoff schema：`p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_activation_failure_result_v1`；physical EOF section完整，closing fence位于physical EOF。

## 2. 执行事实

activation metadata、changed-path、archive identity及clean pre-edit status gates均通过。Executer随后再次以bare `FULL_PLAN_MACHINE_STATE=`作为line prefix搜索committed FULL，而真实machine row以Markdown opening backtick开头；因此候选数量不为1，并以`FULL_PLAN_MACHINE_STATE_EXACT_BOUNDARY_NOT_UNIQUE`在required subset比较前hard fail。

失败发生在任何owner source/test identity读取、bounded context extraction、CodeGraph discovery、apply_patch、测试、compileall、CodeGraph sync、implementation commit及fresh real-self-check之前。对应事实均为：

- source/test reads `0/0`，source/test writes `0/0`；
- targeted/focused/full/compileall/CodeGraph/diff/commit全部`0`；
- fresh source/root、physical input reads、Git acquisitions、required argv、owner calls、owner ledgers与output writes全部`0`；
- retry/fallback、old-root reads、old payload repair/regeneration全部`0`；
- canonical validator、eligibility、release copy/generation/qualification/consumption全部`0`；
- network、device、camera、Ray、strip、cleanup、formal、public analyzer全部`0`；
- retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

Executer以complete last-section-heading-to-physical-EOF策略完成唯一ER append；postappend operations为`0`。该封存足以证明R2 zero-effect terminal handoff，但不产生任何implementation、real-self-check、manifest、eligibility或release credit。

## 3. Planner findings 与决定

**Decision：** `REJECTED_R2_ACCEPTED_COMPLETE_PHYSICAL_EOF_ZERO_EFFECT_HANDOFF`。

R2未完成其唯一实现/real-self-check动作，因此不得接受。R2的失败不是科学分支问题，也不需要Advisor；不是设备操作，也不需要Human授权。

同类external one-off FULL/PLAN parser已经至少三次在bare marker、Markdown wrapper或固定边界假设上退化。继续为单次controller手写另一套parser会扩大脆弱并行ownership。Planner接受Orchestrator的工程决策：先建立并验证repo-owned、纯函数、validation-only machine-row parser owner；后续R2 successor只能调用该accepted helper，不得再内嵌hand-written parser。

CodeGraph验收预检发现仓库已有唯一owner `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`及dedicated test `tests/test_agent_work_machine_contract.py`。因此下一包应强化这两个既有路径，而不是新增第二套并行parser module：保留既有PLAN/FULL入口，新增接受完整text和literal marker的通用API，严格验证Markdown wrapper/backtick/LF/JSON object合同，并把返回值改为deep immutable mapping。

## 4. Residual risks 与 exact next branch

- 现有owner固定入口只能处理预置marker，且`ParsedMachineContract.value`内部仍为mutable dict/list；尚未满足通用literal marker与deep immutable返回合同。
- 现有suffix检查没有显式冻结whole-line backticks exact `2`，必须以dedicated negative matrix覆盖embedded/extra backticks、bare/unwrapped、multiline、duplicate、trailing text、CRLF/EOF-no-LF。
- 新helper不得拥有filesystem I/O、runner/subprocess、canonical validator、eligibility或release authority；不得新增writer。
- active FULL、PLAN activation与Git commit由Orchestrator管理；Planner不修改FULL，Executer不修改FULL/PLAN/archive。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1`，唯一repo-owned parser owner implementation package。P1被Planner独立接受前，R2 successor、real artifacts、old roots、self-check owner、validator、eligibility、release、network与device继续锁定。
