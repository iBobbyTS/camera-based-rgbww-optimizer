# EXECUTION_RESULT archive — Section 2 terminal rejection

**Archive status:** `REVIEWED_TERMINAL_REJECTED`

**Timestamp:** `2026-08-05T07:16:00-06:00`

**Reviewed scope:** `REF-G4-06-REPLACEMENT-PACKAGE` / `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Source checkpoint:** `632cc869f6bec314fb176ca9c6c55f7b1094992f`

**Terminal disposition:** `REJECTED_FINAL_FULL_MASS_REGRESSION_COMMITTED_SOURCE_CANDIDATE_BLOB_DRIFT`

**Classification:** `SECTION_2_SAME_BOUNDARY_THIRD_SUBSTANTIVE_CONVERGENCE_FAILURE`

**Historical execution attribute:** `historical_non_executable`

**Exact stop:** `SECTION_2_ENGINEERING_CONVERGENCE_STOP_SUPERVISOR_REVIEW_REQUIRED`

**Allowed next action:** `WAIT_FOR_SUPERVISOR_ENGINEERING_ARCHITECTURE_DECISION`

## Planner terminal review

The completed final collection ran 982 tests and exited 1 with 4 failures and
219 errors; retry was 0. Its log SHA-256 is
`6d57da77e5d8afe690787b74aae4cbc8e8fd8998672acfa49fef68cb621b5222`.
The flat evidence prefix is
`/Volumes/4T/temp/rgbww-optimizer/g4-r6-s2-final-snapshot-full-20260805T065009Z-632cc86`;
the `.seal`, `.exit`, `.count`, `.sha256` and independently computed log
hash agree.

This result is not the permitted qualified non-green baseline and is not a
scientific, device or formal result. The engineering root cause is the commit
sequencing/attestation topology: the workflow runs the full suite before the
final implementation commit, while the validator simultaneously requires the
candidate to already have its final committed blob and subject identity. This
result, the earlier AUTH/PROV repair, and the topology-subject repair are the
third substantive convergence failure at the same Section 2 boundary.

Fail closed: no fourth repair, full-suite rerun, candidate acceptance, package
prepare/describe/root work, formal attempt, release consumption, or device,
network, camera, Ray, strip or capture access is authorized. No corrective
suffix or next executable package is created. The exact next branch is a
non-executable wait for Supervisor engineering architecture direction.

## Frozen source identity

- Source owner/type: Executer / `.agent-work/EXECUTION_RESULT.md`
- Original bytes: `5833`
- Original SHA-256: `173b69a9d325681adc7c5cfedb52396bc5e0c3b2a698a755bd4226d33cf58cfb`

## Frozen original EXECUTION_RESULT

# EXECUTION_RESULT

## G4-R6 Section 2 final snapshot topology repair

`RETURN_FOR_G4_06_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_TERMINAL_REVIEW`

- Contract: `G4-R6-LARGE-CHANGE-SECTION-2-FINAL-SNAPSHOT-TOPOLOGY-REPAIR-V1`
- Stable task/section: `REF-G4-06-REPLACEMENT-PACKAGE` /
  `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`
- Activation: `632cc869f6bec314fb176ca9c6c55f7b1094992f`, direct single-parent child
  of `75d327729fdc479b6f9305e4e4a5ca3628fe2346`, subject
  `docs(plan): activate section 2 final snapshot topology repair`.
- Activation changed paths: exact twelve governance paths frozen by PLAN.
- Base tree/source/test identities, two review hashes and four archive hashes:
  `PASS` against the live PLAN machine contract before editing.
- Active finding repaired: `REV-S2-REPAIR-R2-001` only.
- Preserved closed findings: `REV-S2-AUTH-001`, `REV-S2-PROV-001`.
- New task/suffix/root/module/schema/controller/adapter/owner: `0`.
- Package/formal/device/network/camera/Ray/strip/capture/release access or
  effects: `0`.
- Commit/push/PR: `0`.

## Candidate identity and topology

- Sole production accepted subject:
  `fix(stage-gate): bind final package to immutable code snapshot`.
- `ALLOWED_CODE_CHILD_SUBJECT` is the single direct alias of the existing
  literal `FINAL_CODE_SNAPSHOT_SUBJECT`; old subject acceptance, tuple/set,
  fallback, legacy alias and alternate validator count are all `0`.
- Positive synthetic Git topology uses an independent test literal for the
  final subject and current two committed blobs.
- Old subject literal `fix(stage-gate): align replacement package owner`
  fails at `source_attestation_binding_drift` before root/backend effects.
- Old direct-child blob set with the final subject fails at
  `committed_source_candidate_blob_drift` against current candidate references,
  before root/backend effects.
- Source: `101182` bytes, SHA-256
  `f4f13a62d110da9865132a9508128a5619ff5b8b163fb66ec29ca19bc264e5c9`,
  worktree blob `c0bc951f4643fb3fe9f4b19d59f13f84e0186266`, numstat `1+/1-`.
- Test: `155812` bytes, SHA-256
  `06fea3128167fb50b2f9ff3bd4b7cc2a24830e66bcae07ce05429d0271409882`,
  worktree blob `5211dcf60e9b9d7e06431df6fc15f049bfb3f5ed`, numstat `72+/8-`.
- Total changed lines: `82`, within expected `40..140` and below hard stop
  `200`.
- Bounded implementation/test correction count: `1/1`. The old-blob test's
  first exact invocation exposed a synthetic index based on the later
  orchestration descendant and therefore reached
  `committed_source_changed_paths_drift`; the bounded correction rebased that
  synthetic index on `source_checkpoint` before writing exactly two old blobs.

## Validation evidence

- Exact positive topology: `1/1 PASS` in `2.195s`.
- Exact old-subject negative: `1/1 PASS` in `0.367s`.
- Exact old-blob negative before bounded correction: `1/1 FAIL` at the
  synthetic `committed_source_changed_paths_drift` harness boundary; no
  production change or external effect.
- Single affected group after the bounded correction: `5/5 PASS` in `36.513s`,
  covering positive, old-subject, old-blob, AUTH literal-alias guard and PROV
  cross-binding guard.
- Complete `tests.test_p7_td_b_r6_stage_gate`: `54/54 PASS` in `304.957s`.
- Complete `tests.test_p7_td_b_r6_terminal`: `6/6 PASS` in `0.580s`.
- In-memory compile of both changed files: `2/2 PASS`.
- CodeGraph: one required query completed before editing; one required sync
  completed after editing (`Already up to date`).
- Strict activation/machine/scope/single-subject/independent-oracle/line-budget
  checks: `PASS`.
- `git diff --check`: `PASS`.
- One strict-check harness attempt misparsed the first porcelain status line
  after applying `strip()`; the corrected NUL-delimited read passed and caused
  no repository edit or semantic validation retry.

## Completed final full collection evidence

- Classification: `NEW_FINAL_SNAPSHOT_CANDIDATE_COLLECTION_NOT_RETRY`.
- Token: `g4-r6-s2-final-snapshot-full-20260805T065009Z-632cc86`.
- Flat plain wrapper:
  `/Volumes/4T/temp/rgbww-optimizer/g4-r6-s2-final-snapshot-full-20260805T065009Z-632cc86.zsh`.
- Flat evidence siblings: `.log`, `.pid`, `.tty`, `.exit`, `.count`,
  `.sha256`, `.seal` under `/Volumes/4T/temp/rgbww-optimizer`.
- Exact command:
  `PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p 'test_*.py'`.
- Forbidden `-t`: absent. Retry: `0`. New directory root: `0`. Base64: absent.
- PID: `56333`. TTY: `/dev/ttys016`.
- Started: `2026-08-05T06:52:18Z`. Finished: `2026-08-05T06:56:44Z`.
- Effective collection: `982` tests in `265.291s`; exit `1` with exactly
  `4 failures + 219 errors`.
- Log SHA-256:
  `6d57da77e5d8afe690787b74aae4cbc8e8fd8998672acfa49fef68cb621b5222`;
  the `.seal`, `.sha256` and independent log hash agree.
- The dominant failure boundary is
  `committed_source_candidate_blob_drift`, repeated across the full result.
- Disposition: this is **not** the PLAN-allowed qualified non-green result,
  because it is not the exact prior governance-lineage-only `2 failures + 8
  errors` group and includes topology/stage-gate-related errors. It is not full
  green and is not accepted.
- This collection is not a scientific result, device result, formal result,
  package-usability result or release authorization. Package/formal/device/
  network/camera/Ray/strip/capture/release access and effects remain `0`.
- No retry, redispatch, test execution, source/test edit or commit occurred in
  this evidence-finalization pass.

Stop at
`RETURN_FOR_G4_06_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_TERMINAL_REVIEW`.

Disposition request: Planner must perform terminal review of the completed
non-qualifying full collection and select the next bounded branch; Executer
makes no acceptance claim.
