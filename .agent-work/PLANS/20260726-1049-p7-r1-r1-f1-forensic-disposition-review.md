# P7 R1-R1 F1 forensic disposition review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `4c42e318ba46fae10d3319ebb569dabd36baed5656e93a62ba2036d4b28a681a`

**Reference task：** `REF-P7-04`

**Decision：** `accepted_historical_run_rejected_new_offline_harness_branch`

## 1. Independent verification

Forensic root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-qualification-r1-r1-f1-offline-forensic-disposition/20260726T110000Z`。

Disposition SHA-256 `37eadc3c2275b161a46b23cee1b5d73ec69b654152fe5c8eb25c28b1803e621a`；validation log SHA-256
`ffe9baebb9c466a56e954d49aff8ddc6e569282b3ea2aef89e26a5966a3365d9`；strict JSON pass。

Direct owner contract 要求 child 返回后立即持久化的 regular/non-symlink child-status artifact。Frozen six-file tree 中
candidate 为 0；post-audit exact `child_exit=null`、owner
`not_persisted_due_zsh_readonly_status_assignment`。

Owners 分类正确：wrapper exit、stdout/stderr、evidence presence/content、post-audit均只是 indirect evidence；argv、
preflight、timestamps、residual process state 对历史 child exit non-probative；later fake matrix 只证明未来 accounting contract。

四项 disposition exact：

```text
child_exit = indeterminate
qualification_run_acceptance = rejected
evidence_artifact = retained_unaccepted_failure_evidence
retry_authorized = false
```

Scope-aware scan 正确：generated output banned hits 0；preflight historical setup-lineage-release path 是 exact retained
input provenance，不能追溯接受 run。

Immutability：frozen run 6/6、canonical 23/23、C1 correction 391/391、tracked source/tests 119/119 before/after exact；
tree hashes与§113一致。Residual 0、cached/diff clean、所有 invocation/release/live/device budgets 0。PLAN SHA保持；
FULL execution-end SHA `0ac46d1a68eb3666018772eae414ca623235ad2cc70a194b4855d823cc69b311`，均只读。

## 2. Acceptance and residual risk

F1 **接受**；R1-R1 历史 run 继续 rejected，不能补证、改写或重试。Residual risk 是：accepted C1 只验证 fake-child
harness；未来若需新的 evidence invocation，必须先把同一 accounting/scan contract 精确绑定到 real adapter command，
再以新的 run ID、独立预算和 evidence rationale 发布，不能称为 R1-R1 retry。

Human“暂时不得启动灯、相机或任何设备测试”继续冻结。

## 3. Exact next branch

现有证据足以决定下一纯离线 evidence-engineering 分支，无需 Advisor 科学判断。发布
`P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R2-H1-OFFLINE-REAL-HARNESS-PREPARATION`：
只生成未来 R2 的 real-command harness candidate/contract，并用 injected fake children 做 protective matrix；不调用
production adapter。Future run ID 固定为 R2，future max budget 1，独立理由是取得 directly-owned child exit 以替代不可
接受的 R1-R1；本 H1 包 invocation budget 为 0。

## 4. Suggested Orchestrator reference update

- F1 标为 accepted/complete；
- R1-R1 保持 rejected/consumed，不恢复预算；
- 两个 C1 harness findings保持 closed；
- REF-P7-04 current action 切换为 R2-H1 offline real-harness preparation；
- 所有 live/device/formal routes 继续 `PAUSED_BY_HUMAN_PRIORITY`。

维护性判断：F1 只做不可变证据分类；下一包仍为外置 harness preparation，不改production或设备路径，无需重构。
