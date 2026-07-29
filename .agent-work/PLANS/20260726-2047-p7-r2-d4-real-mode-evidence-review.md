# REF-P7-04 / R2-D4 real-mode evidence Planner review

**Review decision:** `rev_d3_001_semantics_present_but_real_owner_not_verified`

**Reviewed PLAN SHA-256:** `96a697be6aa4d4c06a57e2299625ddfc4da3a2967ef1e6d9baafd33a7064098f`

**Reviewed root:**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r2-d4-offline-real-mode-evidence-correction/20260726T180000Z`

## Accepted evidence

- D3-equivalent regression `103/103`，SHA-256
  `748f9202e3c752754ff4c233ae596ea2f5dcd4dec5ff705c43007b2f72b76683`；activation/pre-child `62/62`及
  terminal/output/public `41/41`语义保留。
- Mode/progressive matrix `27/27`，SHA-256
  `d57e3378e2525b643ca39876c1622877dec17a646bc58c0866cf4be278eebf24`；设计上的mode/classification/scope/
  monotonic counter字段满足D4合同。
- Initial views-not-separated evidence完整保留并superseded；其summary内容hash与final相同，但evidence trees和disposition分别记录。
- Validation SHA-256 `82a769fc2ce3d6b6f085757ddf8bfd47cdcba8f8c926c607256d82f075a2292b`；final audit
  findings空，SHA-256 `1a10113002ee578a54277beb5ef38f8b692abf58942dc985cb258e7cccd407c5`；strict D4
  `52/52`加historical exact files，SHA-256 `4bc234cf42b05e205c077da4db8039094786ea4c88c17acb813cb8f7d87ce7b2`。
- Exact-path authority scan无global/directory allowlist；unexpected true `0`、real authority `0`、authorized real contract `0`。
- Production import/call/invocation `0`、future release `0/1`、device/network/live/formal `0`；frozen inputs immutable。

## Rejection finding

### REV-D4-001 — passing tests exercise a parallel simulator, not `_execute_real`

The desired D4 semantics appear in `_execute_real` source, but the dynamic evidence does not verify that owner：

- `run-d4-policy-matrix.py` lines 49–65 sends child0/nonzero/exception、writer-failure and five-view cases to
  `simulate_real_policy()`；
- `simulate_real_policy()` lines 96–132 independently implements its own state transitions and writes test-only views；
- `_execute_real()` lines 156–182 is dynamically called only once with the non-authorizing template, which exits at pre-child0；
- production boundary is otherwise checked only by AST/literal count。No injected child、writer or public validator traverses the actual real state
  machine after gate acceptance。

Consequently `_execute_real` could regress in counter transitions、writer failure handling、classification or view sealing while all 27 cases
remain green。This is a parallel owner/test oracle and does not close release-readiness acceptance for `REV-D3-001`。

Additionally, real `run_contract_fact` currently retains only schema/status/future_plan rather than the exact persisted contract path/bytes/SHA；
the next correction must make the actual authority artifact independently replayable before any production child starts。

## Decision and next branch

Do not generate the release。Issue one D5 pure-offline real-path verification package：remove/bypass the parallel simulator as acceptance
authority，introduce a single shared real execution state machine with owned production and test-only adapters，and dynamically exercise that same
owner with injected child/writer/public outcomes while actual production remains0。

Future release remains `0/1`。Human global device pause remains lifted，but release generation does not authorize release consumption、device、
network、live or formal；firmware/deployment/destructive operations remain Human-authorized only。

建议Orchestrator保留`REV-D3-001`为partially closed/not release-ready，新增`REV-D4-001`并使REF-P7-04/D5 current；release继续
locked `0/1`。

维护性判断：D5应删除测试平行状态机，让测试和CLI共用同一owner；这是最小必要维护性修复，不改production/scientific contract。
