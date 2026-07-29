# REF-P7-25-R2-B1A-C3E6F17：limited-input marker gate review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，F17 section dated `2026-07-29`

**Decision:** `REJECTED_LIMITED_INPUT_MARKER_AND_PATH_INSPECTION_VIOLATION`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1`

## Reviewed scope and frozen evidence

本次只审阅 Planner-owned active PLAN、Orchestrator-owned FULL reference、Executer result 及既有 F16 archive；未访问设备、网络、`.env`、相机、Ray、strip、release、retained R3，也未运行 controller/source/test/Git mutation/public analyzer。

- Frozen PLAN SHA reported by Executer: `0dd34ad312da6081041be74a1121b67147be0ad5ce1d729d2dde9a14efd927dd`。
- Frozen FULL SHA reported by Executer: `15127763a68a68b70404ce57ece44efbbfc1375a844588520584e2d1615b6725`。
- Execution evidence: `.agent-work/EXECUTION_RESULT.md` lines 16089 onward；terminal `LIMITED_INPUT_FAIL`，error `ValueError: PLAN exact marker count 0`。
- Counters: container/record/seal/fallback attempts and succeeded all `0`；无 artifact SHA。
- F17 fixed paths were not created. However, after the gate failure, result-recording verification called `lexists` on all four fixed paths, which the result itself discloses as a path-inspection lock violation.

## Findings and validation quality

1. PLAN 的 machine row 使用 inline-code backticks 包裹 `PLAN_MACHINE_CONTRACT=...`，而 Executer loader 要求物理行首直接以 `PLAN_MACHINE_CONTRACT=` 开始，导致合法 frozen row 被解析为零 marker。该错误属于 gate/parser contract mismatch，不是 bootstrap implementation evidence。
2. limited-input failure 后的四路径 `lexists` 检查违反 PLAN 明确的“任一 gate failure 必须在检查四条路径前终止”合同。因而本次不能获得 path-inspection lock-preserving evidence。
3. 零 counters 仅说明未创建 artifact，不能升级为 conforming hard-fail 或 pass；旧 F17 root 既未消费也不可重试。

验证质量：`LIMITED_INPUT_FAIL`，pre-path gate failure；artifact/production/device evidence `0`。Executer 正确未创建、删除、修复或重试 F17 artifacts，但其 post-failure path inspection 使结果不合规。

## Decision, residual risk, and stop

拒绝 F17，不修改 FULL，不授权 controller/source/package/test/Git mutation、R3、release、network 或 device。旧四条 F17 路径不得再检查、创建、复用或重试；后续纠偏必须使用全新路径，并把 parser 对 Markdown inline-code machine row 的提取语义与 limited-input terminal ordering 固定为可审计合同。

Residual risk：在新的 parser/gate 合同通过前，无法证明任何 fixed-container bootstrap prerequisite；retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`。

## Exact next branch

新 active PLAN 仅授权一次离线 corrective bootstrap qualification：在不触碰旧 F17 root 的前提下，验证 PLAN/FULL 两个 exact marker 的 inline-code 行解析（各恰好一条、反引号边界、strict JSON/duplicate/non-finite/type/required-key rejection），并证明任一 gate failure 在任何 path operation 前 terminal、四类 counters 为 `0/0`。通过后才可由另一个计划申请 fresh root bootstrap；本纠偏包不得创建 F17 或任何新 artifact，不得访问设备或运行 production code/tests。

