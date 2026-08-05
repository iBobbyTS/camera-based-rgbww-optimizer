# EXECUTION_RESULT archive — G4-06 large-change Section 2 candidate

- Archive status: `REVIEWED_SEMANTICALLY_ACCEPTABLE_FINAL_QUALIFICATION_INCOMPLETE_HISTORICAL_NON_EXECUTABLE`
- Archive timestamp UTC: `2026-08-05T04:35:59Z`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-REPLACEMENT-PACKAGE` / `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`
- Source checkpoint: `1f7556d36049c33bd4f99412d945db02fe448fa8`
- Source tree: `813d90d31fa4a4650ef4ccde338f64db30eaaada`
- Original source bytes: `7743`
- Original source SHA-256: `f88479ccd88ff3ba66a87ee694ccee50f4c0d5da6f74e1bc23ad91435554c659`
- Terminal disposition: `SEMANTICALLY_ACCEPTABLE_PENDING_FROZEN_CANDIDATE_FINAL_QUALIFICATION`
- Evidence pointers: `.agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md`, full terminal seal paths recorded below
- Exact next stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_FINAL_QUALIFICATION_REVIEW`
- Archive authority: `historical_non_executable`; this archive authorizes no edit, commit, package/root, prepare/describe, device, formal, release, invalid-command retry, or later-stage entry.

## Frozen reviewed execution evidence

Activation `1f7556d36049c33bd4f99412d945db02fe448fa8` was the exact direct
non-merge child of Section 1 checkpoint
`5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74`, with the ten PLAN-frozen
orchestration/archive/review paths and no source/test path.

The candidate remained inside the existing source/test owners:

| path | bytes | SHA-256 | worktree blob | numstat |
| --- | ---: | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `99962` | `0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0` | `6f7a7756687f669c067c253a5d5a30f84b5d6075` | `102+/90-` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `146189` | `540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352` | `65e54f1594ed39c2be641124de71b946858c1e6b` | `123+/140-` |

Total changed lines were `455 < 500`. Targeted initial `8/8` passed. The sole
stage-gate focused invocation observed one alternate-fixture construction error;
the one bounded correction added the missing `projection_contract` copy only,
and the exact failed test then passed `1/1`. Terminal focused passed `6/6`.
Thermal focused reproduced the previously attributed ten-test governance-
lineage baseline (`2 failures + 8 errors`) outside the authorized owners.
Compile, CodeGraph and scope/diff/machine checks passed. All package/root/
device/network/formal/release effects remained zero.

The invalid full command and immutable terminal evidence were:

- command: `.venv/bin/python -m unittest discover -s tests -t .`;
- script: `/Volumes/4T/temp/rgbww-optimizer/run-g4-r6-section2-full-discovery-20260805-a91c5e2d.zsh`;
- evidence root: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-section2-full-discovery-20260805-a91c5e2d`;
- PID / TTY: `62893` / `/dev/ttys002`;
- start/end: `2026-08-05T04:30:07Z` / `2026-08-05T04:30:07Z`;
- exit `1`, output `1263` bytes / `21` lines, SHA-256
  `192c78c880e975096c5f4fe40292ad9c14c1c865cff1714c2fc2ba4d9e908703`;
- failure: `ImportError: Start directory is not importable` before collection;
- collected tests: `0`.

This was a Planner command/harness contract defect. It is not a production
semantic failure, valid full-test failure, Human/Advisor blocker, full retry or
consumption of the one effective full-collection budget. It must remain visible
in every continuation handoff.

## Frozen original live EXECUTION_RESULT body

# EXECUTION_RESULT

## G4-06 large-change Section 2 candidate handoff

`RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW`

- Contract: `G4-R6-LARGE-CHANGE-SECTION-2-REPLACEMENT-PACKAGE-ALIGNMENT-V1`
- Stable task: `REF-G4-06-REPLACEMENT-PACKAGE`
- Section: `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`
- Candidate disposition: `VALIDATION_NON_GREEN_FULL_DISCOVERY_STARTUP_FAILURE_NO_RETRY`
- Commit created: no

## Activation and immutable-input proof

- Activation: `1f7556d36049c33bd4f99412d945db02fe448fa8`
- Direct sole parent: `5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74`
- Parent tree: `656fee670f289b0a20fea1a8c015762afd44a5c0`
- Activation tree: `813d90d31fa4a4650ef4ccde338f64db30eaaada`
- Subject: `docs(plan): activate section 2 replacement package alignment`
- Exact activation paths: the ten paths frozen in PLAN; source/test excluded.
- Intake worktree: clean.
- PLAN/FULL/PLAN-FULL strict parser agreement passed for one active replacement
  package task, Section 2 active state and non-executable FULL/PLAN-FULL.
- Section 1 source/test bytes, SHA-256 and blobs matched PLAN exactly:
  `99811 / 2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11 /
  76c8821c915c58e7ad5cdb0133bf2940b51fd1f4` and
  `145652 / 891ccbdf3a3b3f62083ea680d8ddce56b6b65c15c40bb5722b95953e729ce056 /
  9b8f5781f175bae1fc93cd398b8bf362c0da20e2`.
- Review bytes/hashes matched `6472 / 7217d110...c18096` and
  `6067 / 05c9f220...e4a1`; recorded dispositions were `CLEAN_MERGEABLE`.

## Maintainability preflight and implementation

CodeGraph status was current before edit. File/symbol inspection confirmed the
existing stage-gate owner already owns task identity, machine projection,
descriptor/provenance serialization, committed-child topology, package
persistence and pre-effect validation; the existing test owner covers it. No
adapter, controller, schema family, CLI, helper, persistence owner or root owner
was added.

The candidate:

1. binds package task/contract to `REF-G4-06-REPLACEMENT-PACKAGE` /
   `G4-R6-REPLACEMENT-PACKAGE-OWNER-V1`;
2. keeps future formal task distinct as `REF-G4-06-REPLACEMENT-R6`;
3. replaces completed prerequisite projection with accepted engineering
   identity, exact replacement-package state, retained R3 status and thirteen
   authority bits all false;
4. preserves descriptor-reference precedence, secret/historical guards,
   persistence/replay/inventory/seals and pre-effect ordering;
5. permits only the direct non-merge child subject
   `fix(stage-gate): align replacement package owner`, exact two owner paths,
   candidate blobs and linear `.agent-work/`-only descendants.

## Candidate identities and scope

| path | bytes | SHA-256 | worktree blob | numstat |
| --- | ---: | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | 99962 | `0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0` | `6f7a7756687f669c067c253a5d5a30f84b5d6075` | `102+/90-` |
| `tests/test_p7_td_b_r6_stage_gate.py` | 146189 | `540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352` | `65e54f1594ed39c2be641124de71b946858c1e6b` | `123+/140-` |

Total changed lines are `455`, below the `500` hard cap. Exact implementation
scope contained only the two owners. `git diff --check` passed. Candidate child
checkpoint/tree are deliberately absent before Planner acceptance.

## Behavior and failure matrix

| boundary | observed result | stable failure / effects |
| --- | --- | --- |
| positive package identity, distinct future task, unfinished FULL | pass | all authority false |
| old `REF-G4-06-RAY-R6` / old contract | rejected | `machine_contract_drift`; zero root/downstream calls |
| future task collapsed into package task | rejected | `machine_contract_drift`; zero root effects |
| completed/archived prerequisite projection | rejected | `machine_contract_drift`; zero root effects |
| missing/wrong accepted engineering identity | rejected | `machine_contract_drift`; zero root effects |
| retained status or replacement state drift | rejected | `machine_contract_drift`; zero root effects |
| each of thirteen authority bits true | rejected | `machine_contract_drift`; zero root effects |
| wrong child parent/tree/subject/path/blob, merge/nonancestor | rejected | dedicated `committed_source_*` codes; zero effects |
| source/test or non-`.agent-work/` post-child descendant | rejected | `committed_source_post_child_path_drift` |
| descriptor reference drift precedence | pass | reference drift precedes semantic guards |
| reference-consistent secret/historical value | pass | specialized secret/historical codes preserved |
| persistence/replay/inventory/terminal/failure seals | all focused cases passed except one corrected fixture construction error | no production root/backend/device effect |

## Validation ledger

| invocation | count / duration | exit | result |
| --- | --- | ---: | --- |
| targeted initial (8 named behavior tests) | `8 / 61.371s` | 0 | pass |
| stage-gate focused, sole invocation | `51 / 294.932s` | 1 | one fixture error: alternate plan omitted new projection contract |
| targeted final after bounded correction | `1 / 6.038s` | 0 | exact failed test passed |
| terminal focused | `6 / 0.591s` | 0 | pass |
| thermal focused | `89 / 23.191s` | 1 | `2 failures + 8 errors`, existing governance-lineage `AGENTS.md` identity group |
| compile changed owners | two files | 0 | pass |
| CodeGraph sync | once | 0 | already up to date |
| CodeGraph owner query | once | 0 | no ownership move or new parallel owner introduced |
| exact scope/machine/diff audit | once | 0 | pass |

Bounded correction count is `1/1`; it added the missing
`projection_contract` copy to the existing alternate-root test fixture. No
production correction or second focused invocation occurred. The thermal
non-green group is outside the two authorized owners and matches the previously
attributed ten-test governance-lineage group; it was not modified or retried.

## Sole full-discovery terminal seal

- Exact command: `.venv/bin/python -m unittest discover -s tests -t .`
- Launch: direct plain zsh script in visible macOS Terminal via `osascript`.
- Script: `/Volumes/4T/temp/rgbww-optimizer/run-g4-r6-section2-full-discovery-20260805-a91c5e2d.zsh`
- Validation root: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-section2-full-discovery-20260805-a91c5e2d`
- Token: `g4-r6-section2-full-discovery-20260805-a91c5e2d`
- PID / TTY: `62893` / `/dev/ttys002`
- UTC start/end: `2026-08-05T04:30:07Z` / `2026-08-05T04:30:07Z`
- Exit: `1`
- Output: `1263 bytes / 21 lines`
- Output SHA-256: `192c78c880e975096c5f4fe40292ad9c14c1c865cff1714c2fc2ba4d9e908703`
- Exact failure: `ImportError: Start directory is not importable:
  '/Users/ibobby/Projects/WLED-RGBWW/tests'` before test collection.

The run completed before liveness check 2. Per PLAN, collection occurred once;
checks 2/3 and further polling were skipped. Full retry count is `0/0` and no
automation was created. This is neither full green nor qualified non-green: no
full test identities were collected, so the candidate returns for Planner
review with the raw startup failure preserved.

## Zero-access and zero-effect ledger

- old/rejected branch or stash reads/applies: `0`
- legacy package/formal root access: `0`
- package prepare/describe/root selection/root creation: `0`
- production output-root creation/delegate/backend calls: `0`
- device/network/camera/Ray/strip/capture effects: `0`
- release consumption/formal execution/G4-07/TD-C: `0`
- commits/pushes/PRs: `0`
- validation scratch roots: `1` (full-discovery seal only; not a package,
  formal or experiment root)

Planner stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW`.
