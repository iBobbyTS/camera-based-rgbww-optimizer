# REF-P7-25-R2-O3-C1 / CodeGraph target-gate review

**Planner decision：** `REJECTED_CODEGRAPH_TARGET_EVIDENCE_UNPROVEN`

**Planner date：** 2026-07-28 01:07 MDT

**Reviewed reference task：** `REF-P7-25-R2-O3-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-HELPER-COMMIT-LINEAGE-OWNER-O3-C1`

**Exact next branch：** `REF-P7-25-R2-O3-C1R1`

## 1. Frozen review inputs

```text
HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  72b60f8b76b523ad6c5c282f39e9bae8dbcd661f1380e5d05e6cb90cee066626
reviewed EXECUTION_RESULT SHA-256 =
  5d729974087f68eb5a756ab35ba452f04d7a0c4eb46d3e0bef08b2a1a22ffb11
reviewed FULL_PLAN_REFERENCE SHA-256 =
  09beef5b88ccb62a34e4c4560925105f7c0bfcea2318b8989239ac6dcdf428dc
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
```

The unique 21-field `FULL_PLAN_MACHINE_STATE` matched O3-C1. HEAD and staged
state matched. The retained helper/test diffs remained byte-identical,
unstaged and unaccepted.

## 2. Accepted carry-forward Git proof

The read-only Git proof completed within the package and may be carried into
the corrective continuation without rerunning it：

```text
setup checkpoint =
  9c804abdeabbc5da18a66d0acf25a1f13128bc2d
release checkpoint =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
helper commit / HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e

setup -> release changed paths = 59
setup -> helper changed paths = 61
release checkpoint is direct parent of helper = true
exact helper path set and exact +2 delta =
  src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
  tests/test_p7_retained_release_audit.py
```

Git inspection also recorded that neither path belongs to the current
production/validation allowlists or successor/workflow/cleanup/post-EQ exact
classification maps. That result is diagnostic carry-forward context, not a
substitute for the PLAN-mandated CodeGraph owner proof.

## 3. Rejected CodeGraph gate

The single authorized CodeGraph read query was consumed, but its response was
routed to：

```text
src/camera_based_rgbww_optimizer/optimization/
  measure_p7_thermal_diagnostics.py
```

It did not return the requested target：

```text
src/camera_based_rgbww_optimizer/optimization/
  p7_thermal_diagnostics.py
```

Consequently the response did not establish the current classification
symbols/owner maps and candidate fallback from the target's verbatim source.
The Executer correctly did not retry and did not use Git/source reasoning as a
replacement. O3-C1 therefore failed its explicit ownership-proof gate.

## 4. Evidence and operation disposition

```text
O3-C1 evidence root creation = 0
canonical JSON / fsync / reload / independent seal = 0
CodeGraph read query / retry = 1 / 0
CodeGraph sync = 0
repository edits / tests / compileall = 0 / 0 / 0
stage / commit / amend / push / PR = 0 / 0 / 0 / 0 / 0
helper / validator / consumer / replay / synthetic owner = 0
retained source reads / real audit root = 0 / 0
qualification / generation / retry / repair / copy / consumption = 0
network / DNS / .env / device / camera / Ray / strip / cleanup / capture = 0
CR3 / NPY / nonzero / predevice / Z0 / E2 / analyzer / formal / TD-C = 0
firmware / deployment = 0
```

The planned root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1/20260728T0058`
remains absent. No Advisor-decision evidence was sealed.

## 5. Decision and exact next branch

```text
REF-P7-25-R2-O3-C1 =
  REJECTED_CODEGRAPH_TARGET_EVIDENCE_UNPROVEN
helper correction acceptance = 0
retained audit credit = 0
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

`REF-P7-25-R2-O3-C1R1` is a one-query evidence continuation only. It carries
the completed Git proof without rerunning it, permits exactly one targeted
CodeGraph read query naming the exact owner file and required symbols, and may
create a new evidence root only if that response includes the target file's
verbatim current source with no stale warning. A second wrong route, stale
response or incomplete symbol set is a hard stop with no retry.

Successful sealing still stops at both Planner and Advisor gates. It does not
accept the two-file diff, choose a lineage owner, authorize a policy edit, or
unlock synthetic/real retained audit.

## 6. Residual decision

Advisor must decide whether the exact helper commit receives a
provenance-backed lineage classification and which owner carries it. Until
then, changing only the stale `59` assertion remains prohibited because the
candidate would still be ineligible.

## 7. 维护性判断

The corrective package changes no production boundary. It preserves Git proof
as immutable evidence while requiring the designated CodeGraph owner source,
preventing an accidental test-only widening of lineage policy.
