# P7 checkpoint-command contract C1 review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `512baf340dd4319e942e215a8c0f8f2b9ecf4450d86562beffc554ad36240f22`

**Reference task：** `REF-P7-04`

**Decision：** `accepted_checkpoint_finding_closed_corrected_one_run_unlocked`

## 1. Independent evidence

Contract artifact：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-evidence-qualification-r1-c1-checkpoint-contract/20260726T101711Z/checkpoint-command-contract.json`，
mode `0600`，bytes `16675`，SHA-256
`9947048b32627fbe3501456cab6064b2180f4ed0a946c76b9498da61301c897d`。

Schema/status exact：`p7_td_b_evidence_qualification_r1_checkpoint_command_contract_v1` /
`command_contract_ready_waiting_for_planner`。Checkpoint fields exact：

- execution `1e3b107b8fbfe97bae5624ef638c4883a0faee1d / 52a7168cd2510e9730e30101fc8fbf6f6d8153c1`；
- audit `52a7168cd2510e9730e30101fc8fbf6f6d8153c1 / e7ccdda672b7d5902d81627ff98268160ff141cd`；
- CLI semantics/value `preparation_audit_head / 52a7168cd2510e9730e30101fc8fbf6f6d8153c1`。

One-hop relation exact true，`arbitrary_descendant_allowed=false`。Validator preflight：52a pass，1e3 返回 frozen
checkpoint error。Adapter commit subject/3 paths/diff/file hashes和C3-R1 path/mode/bytes/hash/schema/status均精确。

Negative matrix `31/31` fail closed；canonical before/after 23 unique paths exact unchanged；cached index empty、scoped
worktree clean，所有 invocation/release/live/device budgets 为 0。

## 2. Finding closure and safety

`REV-P7-EVIDENCE-QUALIFICATION-CHECKPOINT-001` **closed**。CLI `--code-checkpoint` 在此 adapter 中明确表示
preparation audit checkpoint；adapter execution HEAD 由独立 exact preflight 与 one-hop contract 控制，不接受任意 descendant。

Human“暂时不得启动灯、相机或任何设备测试”继续冻结。本 review 使用 FULL SHA-256
`79e3587c107b16456feae9cbffc82dfb222c0d330b5ef2fe5a5ea4dab3a0aa39`，FULL 只读。

## 3. Exact next branch

重新发布 `P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R1-R1`：只允许运行一次 evidence-only CLI，
preflight actual HEAD exact 1e3 且 contract one-hop exact，argv `--code-checkpoint` 必须传 52a。Release mode/generation/
consumption、retry、live/device/formal 均为 0。

维护性判断：versioned contract 已明确两个 checkpoint owner并拒绝 descendant 放宽；corrected run无需改代码或架构。
