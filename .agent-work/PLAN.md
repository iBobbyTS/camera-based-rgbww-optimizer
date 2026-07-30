# REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL：C13 acceptance commit 与 lineage seal

**计划状态：** `ORCHESTRATOR_ACTION_ONLY_NO_EXECUTER_DISPATCH`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13`

**Planner decision：** `C13_ACCEPTED`

**C13 review archive：** `.agent-work/PLANS/20260730-0218-p7-retained-r3-option-b-b1a-c3e6f17-corrective-13-review.md`；SHA-256 `e5e8ae9bfc9d02b3653e269e47e888a21fecc1c88260c0221a059782ca3a14cb`。

## 唯一 current package

Orchestrator 亲自验收本次 Planner handoff，更新其独占的 `.agent-work/FULL_PLAN_REFERENCE.md`，整理当前 worktree，并创建一个 focused C13 acceptance/lineage commit。不得 dispatch Executer；不得把本包解释为 retained R3、bootstrap、eligibility、release 或设备工作的授权。

本包只允许 Orchestrator：

1. 只读复核 C13 review archive、当前 PLAN、ER 的唯一 C13 terminal row、两条 implementation path 与 Git ledger。
2. 在 FULL 中把 C13 implementation 标为 Planner accepted，并把 active task 切换到本 lineage-seal task或随后明确的仍锁定门；必须继续记录 `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator call `0`、eligibility emission `0`。
3. 按 AGENTS 的 worktree ownership 要求，提交当前离散成果：
   - `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
   - `tests/test_agent_work_machine_contract.py`
   - `.agent-work/EXECUTION_RESULT.md`
   - `.agent-work/PLANS/20260730-0218-p7-retained-r3-option-b-b1a-c3e6f17-corrective-13-review.md`
   - `.agent-work/PLAN.md`
   - `.agent-work/FULL_PLAN_REFERENCE.md`
4. commit 前运行 repository-wide `git diff --check`，核对 staged set 与上面 exact six-path set 完全相等；不得吸收其他 dirty path。若发现未知改动，Orchestrator 必须亲自分类并按 AGENTS 分离整理，不得 reset/clean 或留给后续角色。
5. commit 后记录 full commit SHA、direct parent、exact changed-path set、六条 committed blob identity 与 worktree/staged clean ledger，再回到 Planner/Orchestrator 门决定后续独立 package。

## Frozen accepted identities

- C13 dispatch activation HEAD：`fd1fe095f59b9accf008c95eeba73fbf6e778030`
- dispatch direct parent：`df1cdffb27699da7feac54379a8581cff9e85392`
- accepted PLAN source SHA-256：`e99aad6853026a6c60a4c30e25c6bdda0356bc0ebbe0b730f63c8ddedd1d0b16`
- accepted FULL source SHA-256：`e1c81dbd63c33292845b43a6e719914d1149a709e8017f97cd315a6139d66a56`
- helper SHA-256/blob：`743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f` / `5c581f9b502bcab1809b6a61a082a47f4150e09f`
- dedicated test SHA-256/blob：`32c0d47cfcdfa49ecad2a4976f401021f0ff1bef947eab705a8c89836b2f5a19` / `c9589947e876920f0cbd2fe7e113592e3cd390e1`
- Executer targeted：`11/11`，exit `0`
- Planner independent targeted：`11/11`，exit `0`
- Executer/Planner no-write compile：通过
- retained R3：`RETAINED_UNVALIDATED_UNCONSUMED`

## 硬锁与 failure branch

- 本 PLAN 不授权实现修改、测试重跑、canonical validator、real retained-R3 audit、bootstrap、manifest、consumer、release consumption、网络、DNS、`.env`、设备、相机、Ray、strip、cleanup、capture、FORMAL、TD-C、sentinel、P8 或 public analyzer。
- 不允许改写 C13 helper/test/ER/archive 的 accepted bytes；identity 漂移必须 fail closed，并由 Orchestrator 建立新的 bounded corrective package，不得原地修复后继续 seal。
- 不允许 amend/rebase/reset/clean；目标 commit 的 direct parent 必须是当前 C13 dispatch activation HEAD `fd1fe095f59b9accf008c95eeba73fbf6e778030`。
- 本包不命中高风险设备授权，也不需要 Advisor 科学决策。

**唯一 stop：** `C13_LINEAGE_SEAL_TERMINAL_WAITING_PLANNER_OR_ORCHESTRATOR_NEXT_PACKAGE`。

**维护性判断：** C13 已将反复漂移的临时 scanner 收敛为单一 pure-bytes validation owner；本包只固化 Git/provenance lineage，不增加运行时或实验控制复杂度。
