# P7 R1-R1-C1 accounting/scan correction review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `c79641fba67f445abb70e30fc8f8e3aec0d86a433c6d9d5fbff7f0e10a7f9942`

**Reference task：** `REF-P7-04`

**Decision：** `accepted_findings_closed_no_retrospective_run_acceptance`

## 1. Independent verification

Correction root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-qualification-r1-r1-c1-offline-accounting-scan/20260726T104000Z`。

Final summary status `offline_correction_ready_waiting_for_planner`，SHA-256
`9e9979406616067434ec8aa0312ebc68b34346b35e19114ec0a6a6bffc120d36`。Candidate harness 使用非保留
`child_rc` 并在 post-processing 前原子持久化；validator 分离 child/wrapper/post status，missing/malformed/out-of-range/
duplicate/symlink/tampered status 均 result-unknown fail closed。

Final fake matrix `24/24`，包含显式 wrong-schema；strict JSON audit `243/243`，SHA-256
`28df7914cd1499a81285abf4ff98bb81985c5d44cb32ff1199412ce96b2c8b4e`。首轮 23/23 以
`validation-summary-v1-preserved.json` 保留，SHA-256
`230476461e60b3e245795612bbd7ffc799fa793bfa2ce75a02282728583acdda`，未被宣称为完整终态。

三 scope scanner 正确区分 generated output、wrapper metadata 与 input provenance；exact retained historical release
reference 仅在 path/bytes/hash/schema/owner/read-only purpose 全部匹配时允许，其错误变体与输出复制均 fail closed。

Frozen R1-R1 六文件与 canonical 23 artifacts before/after exact，mismatch 0、residual 0、cached empty、tracked scope clean；
zsh syntax、Python compile、diff check 均通过；所有 prohibited budgets 为 0。

## 2. Finding closure and governance

- `REV-P7-R1-R1-EXIT-ACCOUNTING-001` **closed for corrected harness contract**。
- `REV-P7-R1-R1-SCAN-SCOPE-002` **closed for corrected scan oracle**。

Closure 不具追溯效力：frozen R1-R1 的 child exit 仍未持久化，无法从 evidence presence、stdout、stderr、wrapper exit
或 correction fake matrix 推断。R1-R1 仍为 rejected hard failure；唯一 invocation 1/1 已消费，correction 不授权 retry。

Human“暂时不得启动灯、相机或任何设备测试”继续冻结。本 review 使用 FULL SHA-256
`5d98b67fbb3fb37401bfad729d180f969b38dadb2a62e5093af5ad0f5b6f740f`。

## 3. Exact next branch

发布 `P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R1-R1-F1-OFFLINE-FORENSIC-DISPOSITION`：
只读枚举 frozen run 的全部可用 exit/evidence owners，产生明确 `child_exit_indeterminate_not_acceptable` disposition；
不得通过 shell/process heuristics 恢复缺失 exit，不得调用 adapter 或请求 retry。若未来需要新 invocation，必须是新的
run ID、独立预算和明确科学/证据理由，经后续 Planner/Orchestrator决定，不属于本包。

维护性判断：纠偏集中在外置 harness 与 scan oracle，production serializer未变；findings可关闭但历史 run不可补证，
无需架构重构。
