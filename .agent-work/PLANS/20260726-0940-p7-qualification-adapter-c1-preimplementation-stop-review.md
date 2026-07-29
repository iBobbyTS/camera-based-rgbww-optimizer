# P7 qualification-evidence adapter C1 pre-implementation stop review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `309fb0e685483052154670cdaff722e0e2232d745bee5f05e9215b3d36ef6229`

**Reference task：** `REF-P7-04`

**Decision：** `blocked_by_frozen_preparation_provenance_contradiction`

## 1. Execution state

Executer 在修改代码前停止；production source、tests、canonical manifest/release、stage/commit、qualification、release、
device/live 均为 0。该 stop 符合 fail-closed contract，不是 adapter implementation failure。

## 2. Independent replay finding

Frozen C3 preparation：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-ray-public-default-lineage-c3-offline-preparation/20260726T092247Z/qualification-preparation.json`，
SHA-256 `db02ee0f1da8cfb274d2a63392e934e6d05ce1af52f9f6d5ceeb9d2f6b5520b2`。

其 `input_index.successor_manifest` 同时记录：

- canonical path `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-ray-public-default-lineage-c1/20260726T144421Z/successor-workflow-manifest.json`；
- SHA-256 `6915c68cbb9436a8aa96ee5384751be6f9405c6f5330d19112cab2b77e898cd3`；
- `commit=52a7168cd2510e9730e30101fc8fbf6f6d8153c1`；
- `parent_commit=a87b09fc4a701a76e5214d6ff6d3a4e3de090521`。

独立解析该 canonical manifest 的 exact bytes/hash 后，manifest 自身实际记录
`commit=e7ccdda672b7d5902d81627ff98268160ff141cd`、
`parent_commit=a87b09fc4a701a76e5214d6ff6d3a4e3de090521`。因此 C3 将“被审计的 current HEAD”与“successor artifact
自身 owner commit”混入同一 ambiguous `commit` 字段。

Current adapter PLAN 要求 strict layered provenance、拒绝 mutated/stale input；若接受该 C3 artifact 会破坏
failure oracle。冻结 finding：`REV-P7-C3-PREPARATION-PROVENANCE-001` — **open / fail closed**。

## 3. Decision and next branch

当前 adapter C1 被前置 evidence contradiction 阻塞并归档；不得开始 production adapter changes。下一唯一分支为
`P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-C3-R1-OFFLINE-PREPARATION-EVIDENCE-CORRECTION`：保留 frozen C3 artifact
不变，新建 versioned preparation artifact，明确区分：

- `artifact_owner_commit/artifact_owner_parent`：从 canonical successor manifest exact bytes 读取，必须为
  `e7ccdda.../a87b09f...`；
- `audit_current_head/audit_current_parent`：当前被审计 checkpoint，必须为
  `52a7168.../e7ccdda...`。

新增 copied/temp negative matrix，拒绝 owner/current 字段交换、ambiguous legacy `commit`、path/hash/manifest bytes
矛盾、stale/non-descendant current HEAD 和 release-like status。不得重写 C3、production、tests、release、PLAN/FULL；
不得 qualification、release、device/live。

Human“暂时不得启动灯、相机或任何设备测试”持续冻结。本 review 使用 FULL SHA-256
`b22b8440a3ef140870dc40dc5c84cb766d4de38216012fc5ddfa563272f141a6`，FULL 保持只读。

维护性判断：根因是外部 preparation schema 字段语义混淆，不是 production lineage owner 缺陷；用 versioned
append-only artifact 与负例矩阵纠正即可，无需架构重构。
