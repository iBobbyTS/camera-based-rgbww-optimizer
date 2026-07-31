# REF-P7-25-R2-B2-R2-C1-C1-C1 source-root binding qualification review

**Planner review date:** `2026-07-31`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-ACTIVATION-BINDING-LOGICAL-MODE-QUALIFICATION-V1`

**Reviewed active PLAN identity:** bytes `16591`, SHA-256
`5da0f6e58fb011a32caecb43894553fe211f33a3860b64ecb7f72202048c71d7`.

**Decision:**
`REJECTED_BOUNDED_B2_R2_C1_C1_C1_SOURCE_ROOT_IDENTITY_UNBOUND_CORRECTION_REQUIRED`

## 1. Reviewed scope and immutable evidence

Planner independently reviewed the committed active PLAN, its matching committed
Executer handoff, the unique controller source, the fresh output root and its exact
five direct-child artifacts, plus activation/evidence Git topology. Planner did not
rerun or modify the controller/evidence, read the accepted C1 source files outside
the sealed package, read retained R3, retry real B2, replay retained Git provenance,
call the canonical validator, emit eligibility, perform release work, or access any
network/device/scientific route.

The activation commit is
`f9fc752fad1d0d48d2797f3d27a49ccf70cf24ec`, direct parent
`e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd`, subject
`chore(plan): activate b2 activation binding correction qualification`, with exact
changed paths `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and
`.agent-work/PLANS/20260731-1026-p7-retained-r3-b2-r2-c1-c1-activation-metadata-failure-review.md`.
The evidence commit is `486ae9274c3a670463b8bcece258fcb22ec7cc97`, its direct
child, with subject `chore(evidence): record b2 activation qualification result`
and sole changed path `.agent-work/EXECUTION_RESULT.md`.

The immutable controller is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-controller-e3a776e-20260731T1626Z.py`,
bytes `19630`, SHA-256
`e18a8824f30ecfa4ee8a5fc6dbf64c174035323dca23fddabaae7298a48b86c5`,
device `16777240`, inode `2218000`, mode `0600`.

The immutable output root is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-qualification-e3a776e-20260731T1626Z`,
device `16777240`, inode `2218004`, mode `0700`. Its exact five artifacts are:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `c1-c1-c1-activation-binding-qualification.json` | `9770` | `20fae6a7b43b5a249e6579a861af85c9ca91f3d85779f50d6dbce04c7e9986ab` |
| `c1-c1-c1-activation-binding-qualification.sha256.json` | `464` | `a4462e9ee2abf38f06bddcce8022d3474a00a5b9cedac46e5f9552d8c5b525bd` |
| `terminal-evidence.json` | `2525` | `6dfd2d78d26797dd330c13b4b89317e093cafeb40fb0e5b38abe93fa78e4aa21` |
| `terminal-evidence.sha256.json` | `416` | `ef30fa3ec0728c64f95d679134ce1dad988168f57616830f9f1e3ecc7a67737d` |
| `execution-result-admission.json` | `1382` | `a27769143f69b7401487869d82905b6a25c876897d2008f20cf76bff48e3fc19` |

The five-piece path set, file modes, qualification and terminal seal targets, and
admission-to-terminal/seal identities are internally exact. The reported current
activation head, parent, subject, path set and six Git ledgers also agree with Git.
These valid sub-results do not cure the source-root ownership omission below.

## 2. Findings

### REV-B2-R2-C1-C1-C1-001 — Must Fix: source root identity was a literal, not a runtime-owned DirectoryIdentity

The controller declares the accepted C1 source-root path as a constant, then reads
each of its four named files using `read_exact_file(SOURCE_ROOT + "/" + name, ...)`
without passing the helper's `root` argument. It never constructs an accepted
`DirectoryIdentity`, never performs an explicit source-root `lstat`, and never asks
the accepted provenance-I/O owner to compare the live root identity with the frozen
device `16777240`, inode `2188341`, mode `0700` tuple.

The qualification payload's `source_root` object is instead constructed from the
same hard-coded path/device/inode/mode literals. Correct literal values are not
physical evidence. They cannot prove that the directory observed during execution
was the frozen accepted source root.

### REV-B2-R2-C1-C1-C1-002 — Must Fix: direct-child and root-drift gates were bypassed

The accepted helper's `read_exact_file(..., root=DirectoryIdentity(...))` path first
re-lstats and compares the root, then enforces an exact lexical absolute direct-child
relationship before opening the file. Because all four controller calls omitted
`root`, both gates were bypassed. Individual file path/device/inode/mode/bytes/SHA
checks therefore do not satisfy PLAN sections 2 and 5, which require the frozen
source root and direct-child/pre-post identity boundary.

The successor must capture and validate the real source-root identity before the
first C1 read, pass that exact `DirectoryIdentity` as `root=` on every C1 file read,
and validate the same directory identity after the fourth read. Qualification,
terminal and admission must persist the observed pre/post root identities and prove
that every returned `FileIdentity.root` equals the frozen root. A literal-only
source-root record, a rootless read, or a raw path-prefix test must fail closed.

### REV-B2-R2-C1-C1-C1-003 — Preserve the independently valid subcontracts

The active activation tuple is correctly sourced from current full `HEAD`; calls
2-6 reuse it, and the parent/subject/path set are exact. The physical/logical mode
mapping, existing 20 semantic cases, output-root lifecycle, qualification/terminal
seals and one admission callback are internally consistent. The successor must
preserve those contracts without reading or repairing this rejected source/root.
It may add only the bounded source-root/direct-child cases and physical root
observations needed to close findings 001-002.

## 3. Validation quality and residual risk

Planner recomputed the controller and five artifact SHA-256 values, verified exact
root/file stat identities, inspected all five JSON payloads, checked seal/admission
linkage, and verified activation/evidence commit parentage and changed paths. The
review also inspected the current accepted provenance-I/O owner: `root=` is the
only public `read_exact_file` route that invokes exact root identity and direct-child
checks. The rejected controller did not use it.

Consequently the run is retained as an immutable rejected qualification, not as
proof that the accepted C1 source-root boundary is stable. Retained R3 remains
unvalidated and unconsumed. Real B2, subordinate manifest, canonical validator,
eligibility, release and all device/scientific routes remain locked.

## 4. Decision and next branch

Reject as
`REJECTED_BOUNDED_B2_R2_C1_C1_C1_SOURCE_ROOT_IDENTITY_UNBOUND_CORRECTION_REQUIRED`.
The sole next branch is `REF-P7-25-R2-B2-R2-C1-C1-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-SOURCE-ROOT-DIRECT-CHILD-QUALIFICATION-V1`.

It is one fresh pure-offline qualification. It preserves single-source activation,
logical mode, the original 20 cases, root-first output, terminal seal and admission,
and adds only exact source-root pre/post identity, root-bound reads and bounded
negative root/direct-child cases. It must not read/rerun the rejected controller,
read/reuse/repair its output root, read retained R3, retry real B2, replay retained
Git provenance, write a subordinate manifest, call the canonical validator, emit
eligibility, perform release work, or access network/device/scientific routes.

Passing the successor only qualifies this controller composition. It does not
authorize real B2 or any later stage.

**Proposed FULL transition:** mark `REF-P7-25-R2-B2-R2-C1-C1-C1` as
`REJECTED_SOURCE_ROOT_IDENTITY_UNBOUND`; add
`REF-P7-25-R2-B2-R2-C1-C1-C1-C1` as the sole task waiting for Orchestrator
activation; set
`repair_v2_status=R2_C1_C1_C1_REJECTED_SOURCE_ROOT_BINDING_C1_ACTIVE`; preserve
`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`; keep real B2 retry, retained
reads, manifest, validator, eligibility, release and every device/scientific route
locked.

## 5. Planner self-check and handoff

- replacement PLAN contains exactly one strict-JSON `PLAN_MACHINE_CONTRACT` row;
- the row identifies one next task, one contract and one Planner stop;
- archive and PLAN are the only Planner-owned changes;
- FULL, ER, GUIDE and RESEARCH remain unchanged;
- `git diff --check` passes;
- no stage, commit, controller execution, rejected-evidence mutation, accepted-C1
  file read, retained read, manifest, validator, release, network or device action
  occurred.

Orchestrator must independently review this archive/PLAN, update FULL, create the
exact activation commit, and only then dispatch a fresh Executer. Planner stops at
`B2_R2_C1_C1_C1_C1_SOURCE_ROOT_BINDING_QUALIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：缺陷仍局限于一次性外置 controller 的目录身份绑定；下一包复用现有
provenance owner 的 `DirectoryIdentity`/root-bound read 路径，不修改生产 owner，也不
引入平行 validator 或 release 语义。
