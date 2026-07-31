# REF-P7-25-R2-B2-R2-C1 pre-root linkage qualification failure review

**Planner review date:** `2026-07-31`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LINKAGE-FAILURE-ADMISSION-PHYSICAL-SEAL-QUALIFICATION-V1`

**Reviewed active PLAN identity:** bytes `14880`, SHA-256
`fbb2db676c0c076625e0f3e4ec3e45286ba3f1e903fe4109f19ad8952e4972c8`.

**Decision:**
`REJECTED_BOUNDED_B2_R2_C1_LOGICAL_MODE_REPRESENTATION_AND_PRE_ROOT_LIFECYCLE_CORRECTION_REQUIRED`

## 1. Reviewed scope and immutable evidence

Planner reviewed the committed active PLAN, the sole matching Executer handoff in
`.agent-work/EXECUTION_RESULT.md`, the retained controller source, the absent frozen
output root, and the two commits which activated and recorded this package. No
controller rerun, root reuse, repair, overwrite, retained-R3 read, real-B2 retry,
manifest, validator, release, network, device or scientific operation occurred.

The activation topology is exact:

- activation HEAD `1bd06c4a0279f51546cf22c38581e2ab411c67d1`;
- parent `b74944fb0bd5ffa064ba1ac92ae390fff7e008dc`;
- subject `chore(plan): activate real b2 linkage correction qualification`;
- changed paths exactly `.agent-work/FULL_PLAN_REFERENCE.md`,
  `.agent-work/PLAN.md`, and
  `.agent-work/PLANS/20260731-0948-p7-retained-r3-real-b2-r2-manifest-failure-review.md`.

The evidence commit topology is exact:

- evidence HEAD `ebaddb5795720cc446f70ea1d32dfcb40cbae27a`;
- parent `1bd06c4a0279f51546cf22c38581e2ab411c67d1`;
- subject `chore(evidence): record b2 linkage qualification failure`;
- changed path exactly `.agent-work/EXECUTION_RESULT.md`.

The immutable controller source is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-linkage-qualification-controller-b74944f-20260731T0948Z.py`,
bytes `21241`, mode `0600`, device `16777240`, inode `2217832`, independently
recomputed SHA-256
`fa1dbb4b470cc946e9fddd036c6d1faa54f6f857e66e06d94c75fd0b01c982c2`.
The frozen output root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-linkage-qualification-b74944f-20260731T0948Z`
is absent. It must remain absent; the source must not be rewritten or rerun.

The Executer handoff is internally consistent with a pre-root hard failure:
controller process `1`, exit `1`, C1 physical reads `4/4`, matrix `0/17`, root
creation `0/1`, qualification/seal `0/0`, terminal/seal `0/0`, ER admission `0`,
retry/fallback/second root/second process `0/0/0/0`. Since failure preceded root
creation, no package artifact exists. This is a valid FAIL conclusion but not a
qualified correction.

## 2. Exact accepted C1 logical representation

Planner performed a bounded read-only inspection of the three accepted C1 payloads
which own the direct linkage records. It did not enumerate or follow retained paths.
The four logical target records are exact as follows:

```json
{"bytes":12195,"mode":"0600","relative_path":"path-owner-index.json","schema":"p7_retained_r3_path_owner_index_v1","sha256":"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35","status":"path_owner_resolved_waiting_for_planner"}
{"bytes":12195,"mode":"0600","relative_path":"path-owner-index.json","sha256":"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"}
{"bytes":682,"mode":"0600","relative_path":"path-owner-index.sha256.json","sha256":"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"}
{"bytes":13455,"mode":"0600","relative_path":"terminal-evidence.json","schema":"p7_retained_r3_b2_c1_path_owner_terminal_v1","sha256":"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763","status":"pass_waiting_for_planner"}
```

For every logical record, `mode` is JSON string `"0600"`. It is not JSON integer
`384`, string `"0o600"`, or string `"600"`. Physical descriptor identity remains
separately represented by integer mode `0o600`, device and inode. The logical owner
therefore requires one explicit, local conversion from proven physical integer mode
to four-digit lowercase octal text, equivalent to `format(mode, "04o")`, before
exact key/type/value comparison. This is representation mapping, not coercive
acceptance: only the resulting exact string `"0600"` is eligible.

## 3. Findings

### REV-B2-R2-C1-001 — Must Fix: physical integer mode was compared as logical JSON mode

The controller's `identity_record` returns `"mode": file_identity.mode`. The accepted
provenance-I/O owner exposes `FileIdentity.mode` as Python integer `384`. The first
real-chain comparison expects this synthesized record to equal the accepted index
seal's direct `index` record, whose `mode` is string `"0600"`. All preceding
`relative_path`, `bytes`, `sha256`, `schema` and `status` values match, but the mode
type/value pair is `int 384` versus `str "0600"`; `exact_record` therefore raises
`RuntimeError:index_seal_identity` deterministically at the first record.

This is not C1 evidence drift and not a scientific issue. The old PLAN froze exact
keys but did not freeze the logical mode JSON type/format, while the Executer copied
the physical representation directly. The successor must freeze the exact accepted
logical string representation and reject integer, bool, prefixed, shortened,
case-altered, padded or otherwise alternate spellings. It must not change C1 files or
the provenance-I/O owner's physical identity type.

### REV-B2-R2-C1-002 — Must Fix: logical qualification ran before evidence-root acquisition

The controller performs all four C1 reads and calls `run_matrix` before
`create_exclusive_root`. Consequently this representation defect occurred after
valuable bounded reads but before any progressive/terminal artifact could exist.
The PLAN required the root after static/compile/preflight and required valid sealed
FAIL evidence to reach ER admission; C1 semantic qualification is not static source,
contract, Git or root preflight. The implementation order failed that evidence
lifecycle contract.

The successor must complete source/contract/FULL/Git static preflight, then acquire
its one fresh root before any C1 file read or semantic matrix. Any later C1 read,
decode, linkage or matrix failure must write one FAIL terminal, independently seal
it, validate the seal, emit one matching admission, and only then append the handoff.
Failure to acquire the root itself remains a pre-root failure with admission zero.

### REV-B2-R2-C1-003 — Preserve previously accepted correction boundaries

The predecessor findings `REV-B2-R2-001/002/003` remain required: schema-specific
direct linkage rather than recursive generic identity, seal-dominant PASS/FAIL ER
admission, and authoritative 64-character physical terminal-seal SHA with rejection
of the malformed handoff value. This failure does not invalidate those boundaries;
it only shows that their qualification controller did not encode accepted C1 mode
representation exactly.

## 4. Validation quality and residual risk

The exact controller source SHA, source stat identity, absent output root and both
commit topologies were independently verified. The direct logical records were
read from accepted C1 canonical payloads and compared with controller lines
`96-125`; no retained path or artifact was opened. The failure localization is exact
at field, type and representation level.

No qualification artifact exists, so the corrected direct-linkage, negative matrix,
failure admission and physical-seal identity behavior remain unproven. Real B2 has
still not read retained R3 or replayed Git provenance, so subordinate manifest and
canonical-validator eligibility remain entirely untested and locked.

## 5. Decision and next branch

Reject this result as
`REJECTED_BOUNDED_B2_R2_C1_LOGICAL_MODE_REPRESENTATION_AND_PRE_ROOT_LIFECYCLE_CORRECTION_REQUIRED`.
The sole next executable branch is `REF-P7-25-R2-B2-R2-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LOGICAL-MODE-AND-FAIL-EVIDENCE-QUALIFICATION-V1`.

It is one fresh pure-offline qualification. It may read the exact four accepted C1
files once, validate the frozen logical `"0600"` representation, run an in-memory
direct-linkage/mode-drift/failure-admission matrix, and persist a sealed terminal and
admission. It may not read or rerun the rejected controller, use the absent root,
read retained R3, retry real B2, replay Git provenance, write a subordinate manifest,
call the canonical validator, emit eligibility, perform release work, or access any
network/device/scientific route.

Passing this successor only qualifies composition for a later fresh real-B2 Planner
package. It does not authorize real B2 or any later stage.

**Proposed FULL transition:** mark `REF-P7-25-R2-B2-R2-C1` as
`REJECTED_LOGICAL_MODE_REPRESENTATION_AND_PRE_ROOT_LIFECYCLE_DEFECT`; add
`REF-P7-25-R2-B2-R2-C1-C1` as the sole task waiting for Orchestrator activation;
keep retained R3 `RETAINED_UNVALIDATED_UNCONSUMED`, and keep real B2 retry,
retained reads, manifest, validator, eligibility, release and all device/scientific
work locked.

## 6. Planner self-check

- replacement PLAN contains exactly one `PLAN_MACHINE_CONTRACT` row and it parses as
  strict JSON;
- the row identifies exactly one next task `REF-P7-25-R2-B2-R2-C1-C1`, one
  contract and one Planner stop;
- archive and PLAN are the only Planner-owned worktree changes; FULL, ER, GUIDE and
  RESEARCH are unchanged;
- `git diff --check` passes;
- no stage, commit, controller execution, old-controller/root read, retained read,
  Git provenance replay, manifest, validator, release, network or device action was
  performed by Planner.

## 7. Planner handoff

Orchestrator must independently review this archive and the replacement active PLAN,
update the Orchestrator-owned FULL reference, create the exact activation commit, and
dispatch a fresh Executer only after a clean activation topology is proven. Planner
stops at `B2_R2_C1_C1_LOGICAL_MODE_QUALIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：问题限定在一次性外置 composition controller 对 accepted C1 schema
的表示映射及证据生命周期顺序；不应修改生产 owner，也不应新增长期平行 validator。
