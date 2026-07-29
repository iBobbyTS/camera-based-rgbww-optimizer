# REF-P7-25-R2-BR / Advisor stop superseded review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-CANONICAL-SEAM-CONFLICT-ADVISOR-STOP`

**Review decision：** `ACCEPTED_AS_HISTORICAL_NEGATIVE_FINDING_AND_SUPERSEDED_BY_HUMAN_ENGINEERING_GOVERNANCE`

## 1. Reviewed scope and evidence

本次 review 归档旧的 non-executable Advisor stop。其冻结输入为：

```text
reviewed PLAN SHA-256 =
  f8609c525dea6e5b39a3a1ef449e60adc520ef143171f7ae7d4e9844206281bf
reviewed HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
B1 review archive =
  .agent-work/PLANS/20260729-0917-p7-retained-r3-option-b-b1-contract-conflict-review.md
B1 review archive SHA-256 =
  d4d960cebb313a6c89336d83a60686c3e1f4931ceee106e422ec8ffa972fe1ef
B1 validation evidence SHA-256 =
  363967849eedbf2c6e7051e8bdadb720f887e72dec3556a24f8218fecb699576
B1 terminal evidence SHA-256 =
  d741b3d7a287a9b7662a3f82deb830cda3bfac90ecba30e747a1b4ee23b87746
```

B1 的负面技术发现仍被接受：旧 source 没有 subordinate manifest 的 canonical-validator
ingestion/recompute seam；只改 helper 与 helper test 无法同时满足 canonical validator 唯一 eligibility owner。

## 2. Superseding decision

Human 2026-07-29 已明确：Advisor 只负责色彩科学和测量科学，Orchestrator 负责文件、代码、provenance、
execution packaging 与 Git topology。该决定已写入当前 `AGENTS.md` 与
`.agent-work/FULL_PLAN_REFERENCE.md`，因此旧 PLAN 将工程路径矛盾升级给 Advisor 的 stop 不再适用。

这不是对 B1 evidence 的否定，而是 route owner 的纠正：

```text
old route = wait for Advisor to choose repository path/topology
new route = Orchestrator freezes minimal exact engineering seam
scientific contract change = none
high-risk device operation = none
Advisor blocker = none
Human authorization blocker = none
```

## 3. Preservation and residual risks

共享 worktree 的现有 helper/helper-test bytes 保持不变且 unstaged：

```text
src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
  SHA-256 = 48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8
  numstat = +186/-33
tests/test_p7_retained_release_audit.py
  SHA-256 = c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f
  numstat = +159/-0
```

`9303aa2` 继续标记为
`retained_release_audit_prerequisite_v1_superseded_before_real_validation`，不可消费。原 retained R3
继续为 `RETAINED_UNVALIDATED_UNCONSUMED`。风险集中在：新增 seam 必须保持 canonical validator 单一 owner、
manifest 不得自授权、共享 dirty worktree 不得被 clean/stash/reset/revert，以及 seal 后不得修补 manifest。

## 4. Exact next branch

下一分支是 `REF-P7-25-R2-B1A`：在 external clean-room 从 exact parent `9303aa2` 建立一次
five-path integration commit，完成 focused/full tests 后 seal 唯一 subordinate provenance manifest，并在
Planner stop 前保持 real retained audit、eligibility、release consumption、network、device 和 FORMAL 全部为零。

本归档不授权执行；执行授权只来自随后重写的 `.agent-work/PLAN.md`。

