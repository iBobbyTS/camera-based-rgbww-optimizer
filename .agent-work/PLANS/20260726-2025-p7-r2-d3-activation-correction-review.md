# REF-P7-04 / R2-D3 activation-correction Planner review

**Review decision:** `rev_d2_001_closed_but_release_readiness_rejected`

**Reviewed PLAN SHA-256:** `582a04e69f8dfa4e91afe3af0cd6f4497b0b2e0ffc492e546c62b7f207dc215a`

**Reviewed root:**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r2-d3-offline-activation-correction/20260726T170000Z`

## Accepted scope

- `REV-D2-001` closed：real CLI只接受一个regular/non-symlink run-contract path；gate直接读取canonical
  `.agent-work/PLAN.md`，要求且只解析一个`PLAN_MACHINE_CONTRACT`和一个`D3_RELEASE_ACTIVATION_BINDING`。
- Gate动态校验actual PLAN path/bytes/SHA；无D2/D3 PLAN hash常量、无separate plan JSON authority。
- Positive copied Markdown PLAN与real-shape in-memory contract fingerprint/trace一致；current D3 PLAN和non-authorizing template均
  pre-child reject。
- Final matrix `103/103`，SHA-256
  `50f77a446e62e98720131c93ec69fe78b30aa1c38922bf05844ff805d6178477`：activation/pre-child `62/62`，
  terminal/output/public equivalent `41/41`。
- Initial `101/103` SHA-256
  `ae0cf6cd36f57fb9c87ea8cca60d81bbec1fec70a22800c5c6d237f8af77b2c3`完整保留；两例均为driver把正确
  `:malformed`结果误期待为`:duplicate_or_malformed`，只修oracle后final通过。
- Validation SHA-256 `3409ccbadda0eb63760d757571a7ed0f06097deb0a564a42e1df8038ce6d4825`；final audit
  findings空，SHA-256 `08c482886233cffcc428da46fcda401704b12919e69d074bc4bcfd45e8817454`；strict D3 `15/15`
  加D2 `2/2`，SHA-256 `a756c3b15eda80a460d1c40e5da1ad60b2af6a3f877da7bb646d1168b88f3f1c`。
- Exact-path authority只分类D2两个历史fake release和D3一个fake release；unexpected true `0`、real authority true `0`、
  authorized real contract artifacts `0`。
- D1/R2/D2/legacy/candidate/adapters/PLAN/HEAD-parent immutable；production writer/import/call/invocation `0`、future release `0/1`、
  device/network/live/formal `0`。

## Rejection finding

### REV-D3-001 — real-mode evidence is hardcoded as fixture/zero-invocation

`candidate/d3-terminal-owner.py` correctly distinguishes gate/audit authority source, but the operational evidence written around the real child
does not：

- line 61 always calls public validation with `classification='fixture_only_non_authorizing'`，including when
  `fixture_plan_path is None` and real CLI executes production argv；
- activation trace line 42 and terminal audit line 75 always persist `production_release_invocations: 0`；
- real CLI line 92 can call `subprocess.run(contract['argv'])` once, so a real child start would make the retained trace/audit false；
- terminal audit also always writes `release_generation_authorized:false`，losing the exact later-PLAN/run-contract generation authorization
  that allowed the child while correctly needing to keep consumption/device/live/formal false。

The fake matrix cannot expose this contradiction because its only positive uses `fixture_plan_path` and an injected child。Therefore D3 closes
the activation-hash defect but is not safe evidence owner for the one real offline release invocation。

## Decision and next branch

Do not generate the release。Issue one D4 pure-offline real-mode evidence correction：copy-derive D3 owners，make classification and invocation
accounting mode-aware/progressive，preserve fixture0 and all D3 gate/terminal/output/public semantics，then stop for Planner review。

D4 must not create an authorized real contract or call production。Future release remains `0/1`。Human has lifted the old global device pause，
but release eligibility/generation still does not authorize release consumption、device、network、live or formal execution；firmware/deployment/
destructive operations remain Human-authorized only。

建议Orchestrator将`REV-D2-001`标记closed、增加`REV-D3-001`并保持REF-P7-04/D4 current；release invocation继续locked `0/1`。

维护性判断：activation gate ownership可接受；D4仅修正terminal owner的mode-aware evidence state，不改production或scientific contract。
