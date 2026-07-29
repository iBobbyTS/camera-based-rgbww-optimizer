# P7 evidence-only qualification R1 preflight checkpoint review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `e8c45e2ac688b165a2c5c3b234d7bd2ea01293f91b3ccce7e62588b264a124af`

**Reference task：** `REF-P7-04`

**Decision：** `preflight_stop_accepted_checkpoint_contract_correction_required`

## 1. Correct stop and independent replay

Executor 在 process invocation 前停止，qualification evidence invocation budget 为 `0/1`；未创建 output root、evidence、
release 或 live/device artifact。该停止正确且不消耗 one-run budget。

PLAN exact command 要求 `--code-checkpoint 1e3b107b8fbfe97bae5624ef638c4883a0faee1d`，但 C3-R1 preparation 的
`audit_current_head` 与 production constant `TD_B_QUALIFICATION_AUDIT_CHECKPOINT` 均为
`52a7168cd2510e9730e30101fc8fbf6f6d8153c1`。

Planner 独立调用 `_validate_td_b_qualification_preparation_r1`：

- `code_checkpoint=1e3b107...` → `ValueError: TD-B qualification preparation schema/status/checkpoint differs`；
- `code_checkpoint=52a7168...` → pass，返回 audit current head `52a7168...`。

因此原 PLAN 将 adapter execution HEAD 与 evidence audit checkpoint 混为同一个 CLI 字段。照原 argv 会浪费唯一
run；Executer 也不得擅自改传 52a。冻结 finding：`REV-P7-EVIDENCE-QUALIFICATION-CHECKPOINT-001` — **open**。

## 2. Frozen semantics

- Adapter execution HEAD/parent：`1e3b107b8fbfe97bae5624ef638c4883a0faee1d` /
  `52a7168cd2510e9730e30101fc8fbf6f6d8153c1`；它标识实际执行的 adapter bytes。
- Preparation audit HEAD/parent：`52a7168cd2510e9730e30101fc8fbf6f6d8153c1` /
  `e7ccdda672b7d5902d81627ff98268160ff141cd`；它是 C3-R1 validator 和 CLI `--code-checkpoint` 的现有语义。
- 当前精确关系为 one-hop：adapter execution parent == preparation audit HEAD。不得放宽为任意 descendant。

## 3. Next branch

发布 `P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R1-C1-CHECKPOINT-CONTRACT` 纯离线外部
command-contract correction：建立 versioned artifact，分别冻结 execution/audit checkpoints、one-hop ancestry、adapter
commit diff/path/file hashes、C3-R1 path/hash/schema 和 corrected argv semantics；负例拒绝字段交换、任意 descendant、
wrong parent/head 和传 execution HEAD 作为 audit checkpoint。

该包不得运行 evidence invocation、修改 production/tests、生成/消费 release 或进入 live/device。Human 设备暂停持续。
本 review 使用 FULL SHA-256 `d3a7b3a0d137a27326ad70ebc5a7f869ccdfc22fdc19bb16dba01aa87e2e59ad`。

维护性判断：问题是 PLAN/CLI checkpoint 字段语义混淆，不是 adapter release isolation 缺陷；先用 versioned exact
command contract 修复即可，无需改 production 或架构。
