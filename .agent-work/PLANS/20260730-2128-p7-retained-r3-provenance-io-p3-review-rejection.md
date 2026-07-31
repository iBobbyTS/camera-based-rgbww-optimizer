# REF-P7-25-R2-B2-P3 Planner review archive

**Review time:** `2026-07-30T21:28:28-0600`

**Reviewed task:** `REF-P7-25-R2-B2-P3`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-V1`

**Decision:** `REJECTED_BOUNDED_P3_C1_REQUIRED`

**Exact next branch:** `REF-P7-25-R2-B2-P3-C1` — harden non-following capability and
root/target binding, then complete the missing negative matrix. Real B2 remains locked.

## Reviewed scope and method

The active package authorized exactly one generic repo-owned provenance I/O helper and its dedicated
test. It required exclusive `0700` root creation, non-following exact reads, strict canonical JSON,
exclusive `0600` durable persistence and reload, immutable target/root linkage, and an exact read-only
Git argv grammar. It prohibited retained-artifact reads, eligibility, release, network, device and
scientific work.

Planner independently used CodeGraph before source inspection, read the active PLAN, FULL reference
read-only, Executer handoff, both commits and both target files, and recomputed commit topology, changed
paths, blobs, file bytes/SHA-256 and canonical patch SHA-256. No tests, external evidence, validator,
release or device operation were invoked during review.

## Evidence and independently verified facts

- Activation commit: `f80c0cf65f922d20796588862b081272162f1e4c`, parent
  `38cd2452433d449ab0b6476f3336d92ca19d9143`, subject exact
  `chore(plan): activate retained r3 provenance io`, exact three activation paths.
- Implementation commit: `77b9e85c1064cb6ba8d3a8fe0932b7eae488c945`, direct parent activation commit,
  subject exact `feat(p7): add retained r3 provenance io boundary`, exact two target paths.
- Production file: bytes `17505`, SHA-256
  `b1ea702fedaaf085c2f32850fc78c05ac54253a143c327a3280b34b804e3824d`, blob
  `4b28a480f642548314424e0465f6fc27add9d9f1`.
- Dedicated test: bytes `18617`, SHA-256
  `a86333e3daba4c7c9544a43edea0aea6ed879e0da2462d45fcbe7b150b748c9f`, blob
  `a1a3bbbe44be0ed4bcd50e1c5af1bc30dd450e7f`.
- Canonical binary patch SHA-256:
  `137350258741caa9609fb08f88f45669bbe4d103218ec0d8201f8e043c3c43cf`.
- Evidence commit: `96b1feb7ebf2b9f8f65c0aafce24ccaa7f26e39c`, direct parent implementation
  commit, exact path `.agent-work/EXECUTION_RESULT.md`.
- Executer recorded targeted `18/18`, focused `65/65`, full `735/735`, compileall, CodeGraph,
  precommit checks and postcommit targeted as passed exactly once; retries and fallbacks `0`.
- Executer recorded all machine-contract zero budgets as `0`; no contrary repository evidence was
  found. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.
- Worktree and stage were clean at review start; `git diff --check` passed.

## Planner findings

### REV-P3-001 — non-following filesystem capability silently degrades

The helper uses `getattr(os, "O_NOFOLLOW", 0)` for exact reads and target creation, and uses the same
zero fallback plus `getattr(os, "O_DIRECTORY", 0)` for root-directory fsync. The active PLAN required
those exact non-following/directory capabilities. If a capability is missing or invalid, the current
owner silently drops it rather than failing closed. This is incompatible with a generic provenance
boundary even though the current macOS runtime exposes the flags.

Required correction: centralize and validate the required flags before any open, emit stable typed
errors when unavailable, and add invocation-level tests proving exact flags and pre-open rejection.

### REV-P3-002 — public root linkage does not prove direct-child containment

`read_exact_file(..., root=...)` revalidates the root identity but does not require the target path to
be a safe direct child of that root. It can therefore return a `FileIdentity` carrying an unrelated
root identity for a file elsewhere. `require_same_target` only compares already-constructed values and
cannot repair this false linkage. This violates the package's physical target/root linkage purpose.

Required correction: when `root` is supplied, require an absolute, lexically exact direct-child target
under `root.path` before lstat/open; reject outside, nested, dot/parent and alternate-spelling paths
without performing file open. Persist/reload must continue to use that same gate.

### REV-P3-003 — required negative matrix is incomplete

The 18 tests are meaningful but do not prove all explicit PLAN cases. Missing or insufficiently
isolated cases include: exact open flags and missing flag capability; close exactly once on a failing
read; general target-open failure; persisted target device/inode drift; root-open/root-fsync/root-close
failure; reload lstat/open/read/decode failure while preserving the created target; and direct-child
root linkage rejection. The success test proves two fsyncs and three closes occur only on success; it
does not prove the required failure branches.

Required correction: add dedicated behavioral cases with stable error codes, call ordering/counts and
physical-target preservation assertions. Do not replace these with source-token-only assertions.

## Validation quality and residual risk

The executed test layers and topology evidence are strong and are retained as prerequisite evidence,
but green suites cannot close behaviors that the dedicated matrix never exercised. The remaining risk
is localized to one high-risk filesystem boundary and its test owner; no architecture expansion is
needed.

P3 is not accepted, real B2 is not unlocked, and the implementation commit is retained as a rejected
candidate ancestor. P3-C1 must use exactly the same production/test paths, one successor repair commit,
targeted/focused/full/compileall/CodeGraph/precommit/postcommit validation, zero retry/fallback and the
same offline lock-zero boundary.

## Planner decision and Orchestrator recommendation

Planner decision: `REJECTED_BOUNDED_P3_C1_REQUIRED`.

Recommend Orchestrator update `REF-P7-25-R2-B2-P3` to
`REJECTED_NONFOLLOW_ROOT_LINKAGE_AND_NEGATIVE_MATRIX_GAPS`, create
`REF-P7-25-R2-B2-P3-C1` as the sole next reference task, and keep
`REF-P7-25-R2-B2-R2`, real B2/B3/B4, validator, eligibility, release and device routes locked.
