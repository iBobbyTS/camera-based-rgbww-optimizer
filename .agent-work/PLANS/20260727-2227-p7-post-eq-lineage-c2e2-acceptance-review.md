# REF-P7-25-C2E2 / Retained checkpoint-drift validation acceptance review

**Review date：** 2026-07-27

**Reviewed reference task：** `REF-P7-25-C2E2`

**Reviewed PLAN contract：** `P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2E2`

**Reviewed PLAN SHA-256：**
`300fcc5eebb5064d97199777c471a7b5895b832b2737be6e7e9979925463f7f9`

**Reviewed FULL SHA-256：**
`b36d86c3c8d2c7275a46572cecd13d04341153772986d3547e0fe9d0a7374ea8`

**Reviewed EXECUTION_RESULT SHA-256：**
`c87843eb65e222b7fd2325a66f883292bc5995c948a041f4baac514c10c07447`

**Decision：** `REF-P7-25-C2E2_ACCEPTED`

## 1. Reviewed scope and implementation method

C2E2 was the bounded pure-offline continuation of C2E1. It was allowed to consume only the exact retained
`tests/test_p7_thermal_diagnostics.py` diff, run the correct full-discovery command, commit that reviewed
test-only change once, run one postcommit focused gate, and acquire one evidence root. Additional edits,
release generation/consumption, device/network access and later-stage execution were prohibited.

The retained test seam binds the injected drift to the exact target-checkpoint
`git show <checkpoint>:<mapped_path>` command, delegates all other subprocess calls to the original owner,
asserts exactly one injection, and reaches the production `checkpoint blob differs` failure branch.

## 2. Independent evidence review

Accepted checkpoint：

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
parent =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
tree =
  494b24c70b8cd5c3a4e06f82de3511b3d63dd0a9
subject =
  test(p7): bind post-eq checkpoint drift injection
changed paths exact =
  tests/test_p7_thermal_diagnostics.py
```

The production correction remains commit
`cc6dbd356dec20eca1437b6c282358c3f2a5e5c7`; C2E2 adds only the independent test checkpoint.

Validation：

```text
correct full discovery = 641/641 pass
compileall / git diff --check / static scans = pass
CodeGraph sync / focused owner exploration = pass
postcommit focused = 2/2 pass
target drift injection = exactly 1
actual production branch = checkpoint blob differs
staged changes = 0
```

Evidence root：

```text
/Volumes/4T/temp/rgbww-optimizer/
p7-td-b-post-eq-lineage-classification-c2e2-offline/20260727T2213
```

Canonical evidence：

```text
root entries = 12 regular / 0 symlink / 0 other
root / artifact modes = 0700 / 0600
strict JSON = 11/11
terminal prior references = 11/11
all mismatch arrays = empty
controller build/persist/SHA/compile/exec/root acquisition = 1/1/1/1/1/1
retry/repair/alternate root = 0/0/0
```

Primary hashes：

```text
09-validation-summary.json =
  cfc19da24d8988c5e78ab726faa85b1baa669dc9ce7cc6d30de65355123b3d0e
10-terminal-summary.json =
  68f524a9c645426376275341e8428b23c2db706f439ae5938e4ea0ed9b79f929
controller-source.py =
  24ecec133186d665d687950321e658aaede4107648789d5686d60142cfdd47a3
```

The two C1 roots remained byte-identical under the exact corrected serializer. Rejected C2/C2E1 roots
remained absent. No production/config/docs/skill/wrapper edit occurred in C2E2.

## 3. Zero-boundary acceptance

```text
repeat C2E1 gates = 0
release qualification/generation/validation/consumption = 0/0/0/0
release retry/second release = 0/0
device/network/DNS/hostname/.env = 0/0/0/0/0
camera/Ray/strip/all_off/cleanup/capture = 0/0/0/0/0/0
CR3/NPY/nonzero output = 0/0/0
public analyzer/predevice/Z0/E2/formal R6/TD-C = 0/0/0/0/0/0
firmware/deployment = 0/0
residual owned process = 0
```

## 4. Planner decision

```text
REF-P7-25-C2E2 = ACCEPTED
production lineage correction cc6dbd3 = ACCEPTED
test-only checkpoint 32b9e67 = ACCEPTED
REF-P7-25 = UNLOCKED_FOR_ONE_FRESH_R3_RELEASE_ATTEMPT
```

No Advisor or Human decision is required. The accepted result authorizes only a new Planner package; it
does not itself authorize release generation, release consumption, device access or later-stage entry.

## 5. Exact next branch

Create one `REF-P7-25-R2` pure-offline package. It must reuse the corrected C1 pre-acquisition/controller
and old-R2 manifest ownership model, but use fresh absent roots and checkpoint
`32b9e670ff3bbea0cd1505528c2ca87c2935446c`. It may run production qualification/generation once and then
public validation, fake consumption simulation, final audit, strict audit and terminal seal once. It must
leave the successful release unconsumed and stop at Planner. Any failure is terminal for the package:
retry, repair, alternate root, second controller or second release remain prohibited.

Device, network, DNS, `.env`, camera, Ray, strip, cleanup, capture, public analyzer, formal R6 and TD-C
remain zero and locked.

## 6. Residual risks and maintainability

The next production qualification is the first live proof that the exact accepted commit-gated mapping
classifies the new checkpoint's full lineage ledger without widening the generic policy. The release must
therefore remain fail-closed and unconsumed until Planner accepts its three-artifact family and evidence.

The accepted implementation preserves one production lineage owner and adds only a test-owned drift seam.
No new abstraction, parallel policy owner or cleanup work is required.
