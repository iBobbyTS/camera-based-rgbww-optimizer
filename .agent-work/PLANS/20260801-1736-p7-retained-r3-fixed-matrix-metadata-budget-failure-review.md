# P7 retained-R3 Option B：fixed-matrix activation metadata budget failure 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FIXED-MATRIX-PREWRITE-SELF-HASH-CORRECTIVE-V1`

**Activation：** `6e6b90583b2be94bdfc26e0e26c93e8e205832ef`

**Evidence child：** none

**Planner 决定：** `REJECTED_ACTIVATION_METADATA_READ_BUDGET_EXCEEDED_ZERO_WRITE_NO_EVIDENCE_CHILD`

## 1. Reviewed scope、topology 与 evidence quality

Planner读取project skill、activation committed PLAN/FULL/ER、当前worktree状态和Git topology，独立核验activation subject、direct parent、ordered changed paths与committed identities。未读取fixed report/seal或其root，未运行controller、selector、ledger、real self-check、canonical validator、test、CodeGraph、network或device路径。

Activation `6e6b90583b2be94bdfc26e0e26c93e8e205832ef`是`0309b66d2a7731325e495319915c548788f124f4`的direct child，subject exact `chore(plan): correct fixed matrix self-hash gate`，changed paths exact且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1726-p7-retained-r3-fixed-matrix-prewrite-self-hash-failure-review.md`

Activation committed identities：PLAN `19766` bytes / SHA-256 `d26b5b8191d9bb88688aa028704a7aa87b57a8a141f0a0db2e6f34882db73074`；FULL `470178` bytes / SHA-256 `173c1d941b68c5e5d98e092bc61105c97bb97f03be2f63f286f36d4bee893651`；ER `1561559` bytes / SHA-256 `6468ae28195ad5ae37bdb7cc4e821905b78467d2bca34b5bd0d8d9d061166b44`。Review开始时HEAD仍为activation且worktree clean；ER与activation object exact相同，没有evidence child或durable execution append。

## 2. Independent finding 与决定

Executer在sole local process内先运行`git rev-parse HEAD`，随后运行`git show -s --format=%P 6e6b90583b2be94bdfc26e0e26c93e8e205832ef`。两次均是activation metadata acquisition，因此`activation_metadata_reads`实际为`2`，超过PLAN预算`1`。首个预算gate正确fail closed；retry/fallback均为`0`。

Activation PLAN/FULL Git-object raw reads各成功`1`次，accepted PLAN/FULL parser也各成功`1`次，但这些成功不能修复先前metadata budget违约，也不授权继续读取fixed evidence或写ER。Report reads、seal reads、strict loads、matrix freeze/canonicalization、worktree ER read、ER patch render、`apply_patch` append均为`0`；controller、selector、ledger Git、real self-check、physical input、validator、production owner、lineage、eligibility、release、network、device与repository code/test effect均为`0`。

因此拒绝原fixed-matrix execution credit。该失败不是accepted parser、fixed report schema、boolean matrix、ledger-binding proof或exact-offset EOF gate的反证；这些下游gate根本未执行。Synthetic engineering attribution facts不接受；production owner、lineage、eligibility与release consumable继续为`false`；Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Exact successor

唯一successor是fixed-matrix activation metadata budget corrective。它保留原fixed-matrix合同，只把activation topology acquisition改为两条互不混计的冻结argv，并冻结总process预算`2`：

1. core metadata process exact argv：`[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,show,-s,--format=%H%x00%P%x00%s%x00,HEAD]`。只允许调用一次；stdout strict解析为HEAD、single parent、subject三个NUL-terminated fields，再消费Git唯一final LF。该进程同时且仅一次取得HEAD、parent、subject；禁止先行或补充`rev-parse`、第二个`show`、`log`或其他core metadata调用。
2. changed-path process exact argv：`[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,diff-tree,--no-commit-id,--name-only,-z,-r,HEAD]`。只允许调用一次；strict解析NUL-delimited ordered paths，要求terminal NUL、无empty/duplicate/extra path。它计入`activation_changed_path_metadata_processes=1`和`activation_git_metadata_processes_total=2`，不得误记为core metadata read，也不得漏记为Git metadata process。

两进程均固定stdin `/dev/null`、stdout/stderr pipes、cwd exact repo、shell false、text false、check false；exit必须0、stderr必须empty。任何启动、framing、decode或gate失败均零写停止，retry/fallback为0。其余合同保持：activation PLAN/FULL/ER Git-object raw reads各一次，worktree ER raw read一次；PLAN/FULL raw bytes在同一process直接进入accepted parsers各一次；current ER exact-offset tail gate；report/seal各raw-read及strict-load一次；top-level `$.matrix`冻结一次并验证18 rows boolean `match`与canonical hash；只验证`$.ledger_binding_proof.frozen_path="$.ledger_rows"`，禁止读取不存在的top-level `$.ledger_rows`；最后且仅最后一次`apply_patch`在physical EOF追加完整matrix handoff。

**Exact next reference：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1`

**Exact next activation parent：** `6e6b90583b2be94bdfc26e0e26c93e8e205832ef`

**Exact next activation subject：** `chore(plan): fix fixed matrix metadata budget`

**Exact next activation changed paths：** `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`、`.agent-work/PLANS/20260801-1736-p7-retained-r3-fixed-matrix-metadata-budget-failure-review.md`

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R2_C1_S1_C1_C1_C1_C1_C1_C1_C1_C1_C1_C1_FIXED_MATRIX_METADATA_BUDGET_CORRECTIVE_WAITING_PLANNER_REVIEW`

## 4. Required FULL updates（Orchestrator-owned）

- 将reviewed task状态改为`REJECTED_ACTIVATION_METADATA_READ_BUDGET_EXCEEDED_ZERO_WRITE_NO_EVIDENCE_CHILD`，记录activation `6e6b90583b2be94bdfc26e0e26c93e8e205832ef`、evidence `null`。
- 将唯一active task/reference切换为上述successor，active contract切换为`P7-TD-B-RETAINED-R3-OPTION-B-FIXED-MATRIX-METADATA-BUDGET-CORRECTIVE-V1`，并冻结exact two metadata argv及分项/总预算。
- 保持`real_self_check_owner_status`与`real_execution_status` blocked on fixed-matrix acceptance；不得解锁controller、real self-check、physical input或canonical validator。
- 保持original execution rejected、synthetic attribution未接受、`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator sole eligibility owner、false conclusion boundary及device authorization false。

维护性判断：successor不改代码，只把activation topology acquisition拆成两个命名清楚、可独立计数的Git metadata owner；其余parser、matrix、EOF和single-write边界不变，无后续代码清理建议。
