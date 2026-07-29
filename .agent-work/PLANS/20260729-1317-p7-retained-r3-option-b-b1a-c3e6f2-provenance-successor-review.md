# REF-P7-25-R2-B1A-C3E6F2 review / hermetic input and cleanup-provenance successor boundary

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F2-HERMETIC-TEST-CORRECTION-V1`

**Decision:** `rejected_targeted_external_input_and_exact_provenance_owner`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F3`

## Reviewed scope

C3E6F2 was authorized to create one fresh clean room from
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, materialize the exact five-path
candidate identified by candidate SHA-256
`3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225`,
copy three exact ignored fixtures, edit only
`tests/test_measure_raw_shutter_response.py`, and run one import gate, one
targeted suite and—only after targeted success—one full suite.

Production edits, stage, commit, manifest, original-R3 reads, retained audit,
eligibility, release consumption, network, DNS, `.env`, credentials, devices,
camera, Ray, strip, cleanup, capture, analyzer, FORMAL, firmware and deployment
were prohibited.

## Independently verified evidence

Evidence root:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f2-offline/
  20260729T190914Z
```

The fresh clone remains detached at the exact parent with six unstaged paths:
the candidate five plus the one authorized test correction. Staged paths are
zero and `git diff --check` passes.

The following gates are accepted:

- PLAN/FULL `12/12` machine subset;
- exact canonical candidate object;
- five source reads and exact five-path materialization;
- 53,230-byte binary full-index candidate patch SHA-256
  `7b71f9db1ef5a56c6065a255f35b34e9ca7d625699ff31a07cfa7fadb1f75f35`;
- three exact fixture source reads and copies;
- three clean-room production import identities;
- a single test-only edit with no production path change.

The corrected test file facts are:

- before: 18,751 bytes, SHA-256
  `3d7473335b96a320c1fcbef8a07e4dd6b2e42a0c37801d280f6852d2aeff3112`,
  Git blob `b6178d564a7bfdb5a218e5dddcfb0ebfbdd2bc59`;
- after: 19,184 bytes, SHA-256
  `f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8`,
  Git blob `124b6adb449e8b93b478ce3e1facbae8437c5b53`;
- canonical cleanup-provenance diff algorithm `git diff <old> <new> -- <path>`
  produces 1,650 bytes and SHA-256
  `32a9766cb20446e142e2ba0c8abb7ef02c08c2a39d9340f1e2566810dae45b84`;
- the unrelated binary full-index representation is 1,716 bytes and SHA-256
  `dd70fa31ab4c2db590086eded424730c0888a945b287aeeca478e7016c099f02`.

The persisted edit record proves the test patches
`camera_remote.create_camera_backend` to return
`mock.sentinel.camera_backend`, asserts the factory once, retains the runner
once assertion and proves the runner receives the same backend. It adds no
credential literal and does not change production behavior.

The exact targeted invocation ran 134 tests once and returned 20 errors with
no recorded assertion failure. Full discovery correctly remained at zero.

Evidence hashes:

- `test-correction.patch`:
  `32a9766cb20446e142e2ba0c8abb7ef02c08c2a39d9340f1e2566810dae45b84`
- `test-correction.json`:
  `4f53e4e25cd1286ded2ba46b0a4dbc7d076dae686c5c22dee38d446d405daae8`
- `targeted.stderr`:
  `9b1119512db1bd2db5dd82b6cf4ed3129e2a0a5ed4e4c2df8de77d0a5f8c8760`
- `targeted-summary.json`:
  `b91154f5cf6dfa403c6d5ee78f1bb83702bf86a89e2114c12a6ed4f2f39bb0f0`
- `validation-summary.json`:
  `630460493901f48e44dd1468dc11d6c498921597d90dc9af251e9c59a7dfc52a`
- `terminal-summary.json`:
  `9537c1adf85d43484626c705e401dfafdc96fa990f7dc5bee1bd14bbba3829a6`

Retry, full, stage, commit, manifest, retained-R3 reads, audit, eligibility,
release and all prohibited environment/device counters remained zero. Shared
HEAD and staged paths remained unchanged. The rejected root is terminal and
must not be repaired or reused.

## Failure 1: fourth exact local input

Seventeen raw-observer errors advanced past the supplied white LUT and failed
on `config/white/white-endpoints.json`. Independent inspection proves:

- regular, non-symlink file;
- 1,483 bytes;
- SHA-256
  `050e79d0b075cbbb894da68a21561b6e8f62633c0ec0faf1f8bfc027a319e813`;
- strict JSON object with top-level keys `created_at`, `measurement`,
  `ray_endpoint_matches`, `version`, `white_range`;
- recursive key scan finds no secret/token/password/credential/API-key field;
- untracked and ignored by exact `config/*`;
- statically named by `measure_raw_observer_validation.DEFAULT_WHITE_ENDPOINTS`
  and project documentation.

The raw-observer test helper supplies its own baseline LUT, location and
observer files. Its only unconditional project-root inputs are the already
frozen default white LUT, this white-endpoints file and the existing default
code-duty curve. Therefore this fourth ignored fixture exhausts the currently
demonstrable raw-observer external-input closure; no broad config-directory
copy is permitted.

## Failure 2: canonical cleanup-test provenance

Three P7 lineage tests correctly rejected the changed raw-shutter test. The
canonical owner is:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-cleanup-test-provenance-c1/
  20260727T020000Z/cleanup-test-provenance-manifest.json
```

It is 2,641 bytes with SHA-256
`753f00f15a9c40dd0e3a0c34773f063a2cd44605d7c1f5507f375d87f56ea0d0`.
It binds exact cleanup-test commit
`0c878cbf3c7d94dadef2a64446c08ba01931a0d2` and exactly two test paths. The
raw-shutter entry binds the current hash `3d747333...3112`, Git diff SHA-256
`70b61355...00ca`, exact fake-Ray-secret cleanup-test scope and no extra paths.

`_validate_td_b_cleanup_test_provenance()` validates manifest owner/hash/schema,
the exact two-path set, canonical old/new commits, working bytes, final
checkpoint bytes and per-path diff. The lineage classifier calls it only when
one of those exact paths appears. This is a correct exact owner, not a generic
tests allowlist.

The new backend-injection correction is a legitimate later change with a new
scope. Updating the existing manifest or silently changing its constants would
rewrite history. Putting the test edit and a validator that binds the resulting
commit SHA in one commit would be self-referential: changing the validator to
name the commit changes that same commit.

## Minimal legal provenance topology

The smallest non-self-referential route is two-level:

1. create one external-cleanroom, test-only direct-child prerequisite commit
   from `9303aa22...` containing exactly the proven raw-shutter test edit;
2. after that full child SHA exists, seal one new immutable single-path
   cleanup-test successor manifest binding the canonical owner, full child and
   parent commits, before/after blob OIDs and SHA-256 values, exact ordinary Git
   diff SHA-256, scope, rollback, zero extra paths and false release/eligibility
   authority;
3. keep this prerequisite explicitly unconsumable; the current canonical
   validator must still reject it;
4. only a later exact candidate commit may extend the canonical production
   validator/test seam to recognize that exact successor commit and manifest,
   delegate only the raw-shutter path, preserve the chart-response path under
   the original manifest, and retain fail-closed behavior for neighboring test
   paths or any drift.

This mirrors the repository's existing canonical-owner/successor delegation
pattern and avoids a generic path allowlist. It is an Orchestrator-owned
engineering/Git decision under Human governance source
`conversation://human/2026-07-29/orchestrator-engineering-owner`, SHA-256
`52394bcd3fa819fcb83c82c50a89d0b9c4aaa53a41eca18bb953c174787b259d`.
No Advisor or Human authorization is required.

## Planner decision

C3E6F2 is rejected. It receives fixture, candidate, import and exact test-edit
credit but no targeted/full/commit/manifest/audit/eligibility/release credit.

The successor C3E6F3 may execute only level 1 and 2 of the topology above:

- one fresh clone at parent `9303aa22...`;
- stable single read of the proven corrected test source and exact one-path
  materialization;
- stable identity validation of the fourth white-endpoints fixture without
  copying or running raw-observer tests;
- exact two existing fixtures only for the raw-shutter test runtime;
- one precommit raw-shutter module test, one exact one-path commit, one
  postcommit raw-shutter module test;
- one expected-negative call proving the old canonical cleanup validator still
  rejects the child;
- one immutable single-path successor manifest and one independent verifier;
- no candidate five materialization, production edit, full suite, original-R3
  read, eligibility, release or device work.

Whether and how a later candidate commit binds this manifest remains a separate
Planner package after C3E6F3 terminal review.

## Residual risks

- Full clean-room discovery remains unpassed.
- The test-only prerequisite child SHA and manifest SHA do not exist until
  C3E6F3 succeeds.
- The candidate production validator has not yet been extended to the new exact
  successor owner.
- Original retained R3 remains
  `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete; activate only C3E6F3 after Orchestrator
reviews and synchronizes its required FULL machine state.
