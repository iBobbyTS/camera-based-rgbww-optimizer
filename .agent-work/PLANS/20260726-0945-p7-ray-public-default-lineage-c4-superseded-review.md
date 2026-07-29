# P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-C4 waiting review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `85fce5a4882278db8011b89c7bc65e6073ce8beb3bfb3672ea8b23834b3cf481`

**Reference task：** `REF-P7-04`

**Decision：** `superseded_by_orchestrator_offline_guidance_not_a_failure`

## 1. State

C4 是明确的 offline waiting/no-op gate，不是执行失败。新的 Orchestrator 指导确认 Human 允许继续离线计算，
因此 C4 被 supersede；Human“暂时不得启动灯、相机或任何设备测试”仍持续，未解除设备/live pause。

C3 preparation 仍被接受：

- preparation SHA-256 `db02ee0f1da8cfb274d2a63392e934e6d05ce1af52f9f6d5ceeb9d2f6b5520b2`，状态
  `prepared_waiting_for_planner`；
- candidate 仅为 `eligible_waiting_for_planner`，不是 release/readiness；
- 当前 HEAD `52a7168cd2510e9730e30101fc8fbf6f6d8153c1`，canonical artifacts 不变，所有 live budgets 为 0。

## 2. Runner safety assessment

现有 `write_td_b_setup_lineage_release`/`--qualify-lineage-release` 的 owner 会写出
`production_release_usable=true` setup-lineage release，因此不能直接消费 C3 preparation 作为本次“只生成
qualification evidence、不生成 release”的授权路径。该事实不是当前代码 bug，而是新的 bounded adapter/contract
correction 前置条件。

## 3. Exact next branch

发布唯一离线纠偏：`P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-C5-OFFLINE-QUALIFICATION-EVIDENCE-ADAPTER`。
它只建立显式 evidence-only owner，验证 C3 preparation/layered candidate，产出 `qualification_evidence`（禁止
release fields/usable status），并加入 strict negative tests；不得执行 qualification、写 release、访问设备或
调用任何 live owner。Human pause 继续冻结。

维护性判断：需在现有 lineage qualification owner 旁增加明确的 evidence-only 分支，并锁定 release/evidence
边界；先以 protective tests 为前置，避免复用会写 release 的旧 CLI 路径。无需泛化重构。
