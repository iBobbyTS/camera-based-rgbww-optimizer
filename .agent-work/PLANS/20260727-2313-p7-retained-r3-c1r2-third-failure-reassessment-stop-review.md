# REF-P7-25-R2-C1R2 third-failure ownership reassessment stop review

**Planner decision：** `REJECTED_OUTER_WRITER_PREFLIGHT_FALSE_REJECTION`

**Review time：** 2026-07-27 23:13 MDT

**Reviewed reference task：** `REF-P7-25-R2-C1R2`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-RELEASE-AUDIT-ADAPTER-C1R2`

**Exact next branch：**
`PLANNER_STOP_RETAINED_R3_EVIDENCE_CONTROLLER_OWNERSHIP_REASSESSMENT`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
parent =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
tree =
  494b24c70b8cd5c3a4e06f82de3511b3d63dd0a9
subject =
  test(p7): bind post-eq checkpoint drift injection

reviewed PLAN SHA-256 =
  b2995a3402b1691239e4879b9b9e0c41015fc24a62772f8bc424c085d649bf1b
reviewed FULL_PLAN_REFERENCE SHA-256 =
  14b891429b1f3698a840b1d94eacad22e247e57b755a44c3f09795cd463e8b43
reviewed EXECUTION_RESULT SHA-256 =
  c8c5326841f97511fbf5700d75713439d44cee37a91cb4c6befc3df42e35ba76
predecessor review archive SHA-256 =
  e779fe09129870924a8c19f0dd65fb8f809ffa05d485d56f28bfd2754bea9df5
```

Planner independently confirmed the Git identity, no staged path, no production-scope worktree drift, the
absence of both proposed C1R2 directories, and the exact hashes of the retained three-artifact release
family. Existing `.agent-work` and Advisor worktree changes were treated as Human/Orchestrator-owned and
preserved.

This review did not edit `FULL_PLAN_REFERENCE.md`, `EXECUTION_RESULT.md`, GUIDE, production, config, tests,
docs, skills or wrappers.

## 2. Reviewed execution and evidence quality

The Executer froze the required outer imports and invoked the dependency preflight exactly once before any
directory acquisition or controller construction：

```text
outer writer dependency preflight attempt/pass = 1/0
controller source build at preflight completion = 0
filesystem mutation during preflight = 0
unpersisted controller smoke check = 0
```

The reported failed bindings were：

```json
["Path","stat.S_IMODE","stat.S_ISDIR","stat.S_ISREG"]
```

These bindings were present and usable. The preflight rejected them because it imposed
implementation-specific `__module__` equality on `pathlib.Path` and `stat.S_*`, beyond the PLAN's required
identity, callability and constant semantics. This is a false rejection in the external preflight owner, not
evidence that the retained release or public validator is invalid.

The pre-acquisition stop was correctly enforced：

```text
intermediate parent attempt/success = 0/0
exact child root attempt/success = 0/0
source build/SHA/persist/identity/compile/exec = 0/0/0/0/0/0
internal/public/fake/final/strict/terminal = 0/0/0/0/0/0
alternate owner/root/source/controller = 0/0/0/0
```

No C1R2 artifact or terminal seal exists because the failure preceded the first permitted filesystem
mutation. The current `EXECUTION_RESULT.md` handoff, the absent paths and exact retained artifact hashes
provide sufficient evidence to accept the failure facts, but not to validate the release.

## 3. Retained-release disposition and absolute locks

The retained exact release remains：

```text
path =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/
  lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3
status = RETAINED_UNVALIDATED_UNCONSUMED

current-lineage-candidate.json SHA-256 =
  3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0
resolved-formal-plan.json SHA-256 =
  cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b
setup-lineage-release.json SHA-256 =
  0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e
```

Qualification, release generation, retry, repair, copy and consumption remained zero. Retained/historical
evidence writes, repository production/config/test/docs/skill/wrapper edits, tests, compileall, CodeGraph,
Git operations, device/network/DNS/`.env`, camera/Ray/strip/cleanup/capture, CR3/NPY/nonzero output, public
analyzer, formal, TD-C, firmware and deployment all remained zero. Residual owned process count was zero.

No successor may treat the retained family as validated authority or consume it while this stop is active.

## 4. Three-failure ledger

The same external evidence-controller ownership boundary has now failed three consecutive corrective
packages：

| package | failure owner | consumed lifecycle | release disposition |
| --- | --- | --- | --- |
| `C1` | missing intermediate-parent acquisition contract | source build/SHA and failed child-root attempt | unchanged / unvalidated / unconsumed |
| `C1R1` | outer exclusive writer referenced missing `os` binding | parent/root acquisition and source build | unchanged / unvalidated / unconsumed |
| `C1R2` | dependency preflight used invalid `__module__` equality | one preflight attempt only | unchanged / unvalidated / unconsumed |

The individual failures are local, but their sequence demonstrates that the one-shot controller's source,
writer, dependency predicate and filesystem owner remain split across ad-hoc external launcher code. A
fourth narrow correction would repeat the same unstable ownership pattern and is prohibited by the
second-pass-debugging three-failure reassessment threshold.

## 5. Planner findings

### REV-R3-C1R2-001 — false preflight rejection

The failure predicate tested interpreter metadata that the required semantics did not promise. The
execution correctly stopped, but the package cannot be accepted because no retained-release audit ran.

### REV-R3-C1R2-002 — external controller ownership is not yet stable enough for another one-shot package

Parent/root acquisition, canonical persistence, dependency validation and controller construction have
failed at three adjacent boundaries without entering the retained audit. The next decision must establish
one testable owner before another fresh evidence root or retained-release access is authorized.

### REV-R3-C1R2-003 — no scientific or dangerous-device decision is implicated

The blocked question is an offline engineering ownership decision. Current Advisor guidance is sufficient,
and no device, firmware, deployment, light-output or formal authorization is requested. Advisor escalation
is not required. Human authorization under the project's High-Risk Device Authorization rules is also not
required unless a later proposal broadens into a dangerous operation or changes scientific/release
semantics.

## 6. Decision and explicit stop

```text
REF-P7-25-R2-C1R2 = REJECTED_OUTER_WRITER_PREFLIGHT_FALSE_REJECTION
REF-P7-25 = BLOCKED_ON_EVIDENCE_CONTROLLER_OWNERSHIP_REASSESSMENT
retained release = RETAINED_UNVALIDATED_UNCONSUMED
C1R3 executable package = PROHIBITED
next = PLANNER_STOP_RETAINED_R3_EVIDENCE_CONTROLLER_OWNERSHIP_REASSESSMENT
```

Planner must not generate or release C1R3. Orchestrator must first record this rejected branch and select one
minimal engineering ownership direction. Only after that selection may Planner design a new, separately
reviewable offline implementation package.

## 7. Minimal ownership reassessment options

### Option A — repo-owned retained-release audit helper（Planner recommendation）

Create a small repository-owned offline helper that singly owns safe parent/root acquisition, exclusive
canonical JSON/source persistence, semantic dependency checks and the schema-aware retained-release audit.
Add focused fake-filesystem and negative tests before it can access the retained package. A later execution
package would call the tested helper rather than embedding a new source/writer in an ad-hoc launcher.

This option creates a durable single source of truth for a high-risk error-handling/evidence boundary and is
the preferred maintainability route.

### Option B — fixed repo-owned controller builder before any retained access

First authorize a pure-offline design/test package that introduces one fixed controller builder plus its
outer writer contract and adversarial lifecycle tests. That package must not acquire a release evidence
root or read the retained release. Only after its implementation is committed and independently reviewed
may a separate package instantiate it once against the retained release.

This is narrower than Option A, but keeps more orchestration in the launcher and therefore carries higher
future duplication risk.

Orchestrator may choose A or B, or ask the Human for product-level preference. No additional Human
authorization is required for either bounded offline engineering option. A broader option that changes
release meaning, validation criteria, scientific policy or dangerous-device scope requires a new decision
at the appropriate Human/Advisor boundary.

## 8. Residual risks and acceptance gate for future planning

- The retained release is not validated and cannot unlock formal/device work.
- All C1/C1R1/C1R2 paths and counters are historical evidence only.
- Another ad-hoc controller predicate, import patch or fresh-root audit package is not an acceptable next
  branch.
- Future planning requires an explicit Orchestrator ownership selection, a named single owner, regression
  tests for all three observed failures, and a separate Planner review before retained-package access.
- Release qualification/regeneration/consumption and all device/formal routes remain locked.

## 9. 维护性判断

The third failure confirms an unclear ownership boundary rather than a production or scientific defect.
Stopping before C1R3 avoids another parallel external lifecycle. Option A offers the clearest long-term
boundary with one repo-owned helper and focused tests; Option B is acceptable only if its builder/writer
contract is likewise singular and fully regression-tested.
