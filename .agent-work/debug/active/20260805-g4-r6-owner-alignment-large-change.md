# G4 R6 owner-alignment large-change workflow

## Status

- State: `section_2_frozen_candidate_final_qualification_waiting_activation`
- Stable reference task: `REF-G4-06-REPLACEMENT-PACKAGE`
- Branch: `codex/g4-r6-owner-alignment-large-change`
- PLAN-FULL sections: `2`
- Current section: `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`
- Package/root/device/formal/release authority: none

## Frozen cause and rejected input

The ordinary candidate reached a historical 305 changed lines, stopped
incomplete/unvalidated, and is preserved only on branch
`codex/g4-r6-owner-alignment-rejected-305` commit
`1f28b4c04a0ca20888dd5a996af53fc2f3dd0faf`. It may be read only as failure and
contract evidence. It must not be cherry-picked, copied or treated as production
truth.

## Section ledger

| section | status | commit | clean reviews |
| --- | --- | --- | --- |
| `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING` | `ACCEPTED_COMMITTED_TWO_CLEAN_REVIEWS` | `5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74` | `2/2` |
| `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY` | `SEMANTICALLY_ACCEPTABLE_FINAL_QUALIFICATION_WAITING_ACTIVATION` | none | `0/2` |

Section 1 owns only the closed accepted-engineering checkpoint binding,
descriptor projection and read-only Git validator seam. It cannot switch package
task/FULL projection or access a package root. Section 2 remains locked until an
accepted Section 1 commit has two consecutive independent clean reviews.

## Section 1 execution evidence

- Activation and all read-only identity/machine/CodeGraph preflights passed.
- One independently derived single-owner candidate was written only to the two authorized source/test paths.
- Observed numstat first reached `109+/1-` source plus `118+` test (228 changed lines), then `106+/1-` plus `114+` (221 changed lines). These observations breached the exact `220` hard cap before tests.
- Subsequent mechanical compaction left a live `105+/1-` plus `114+` (220), but the earlier observed breach is immutable execution evidence and cannot be reset by formatting.
- Orchestrator stopped the Executer before targeted/focused tests or post-candidate CodeGraph sync. No package, root, device, network, capture, formal or release effect occurred.

Root-cause status: the closed prerequisite seam still appears technically coherent, but its first-pass expression exceeded the frozen section budget. The uncommitted candidate is not accepted production truth and must be reviewed fail-closed.

Planner disposition: this is one sizing/PLAN-contract failure and zero semantic
production failures. The atomic Section 1 boundary is retained; its next fresh
PLAN should use expected 200–260 changed lines and hard stop 300. The current
draft must be path-scoped into a named historical stash by Orchestrator and must
never be applied or copied into the fresh implementation.

Orchestrator created historical stash
`b62eddd7563af43a20fd66a4960bae386f9ed54e`, parent
`e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e`, exact two paths and numstat
`105+/1-` plus `114+`. Source/tests are clean. The stash and rejected branch are
forbidden inputs for the fresh Executer: read/apply/pop/drop/branch/copy counts
must remain zero.

## Next action

Fresh V2 activation `e48cc084a6f4ebdf61c26c1b426d64522030e791`
passed every identity/machine/CodeGraph preflight. A new Executer independently
implemented the closed accepted-engineering binding/descriptor/read-only Git
seam from the clean accepted source without reading the forbidden stash or
rejected branch. The frozen candidate is `96+/1-` source plus `198+` tests,
`295` total changed lines; targeted `15/15`, focused `50/50`, final affected
probe `1/1`, compile, CodeGraph and diff/scope checks pass. Harness corrections
remain `0`; package/root/device/network/formal/release effects remain zero.

State: `READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`.
Planner must review before Orchestrator may commit or begin the two-clean-review
loop. Section 2 remains locked.

Planner review rejects final qualification while preserving the candidate as
unaccepted correction input. Ownership, closed shapes, Git validation,
descriptor precedence and zero-effect ordering are accepted for this limited
purpose. The focused `50/50` result predates the late ancestry OSError mapping;
the one-off `1/1` probe is not a durable repository regression, and current test
source covers returncode 2 but not raised `OSError`. The same Section 1 must add
that durable assertion and re-run the affected test plus one focused suite before
commit consideration. Section 2 stays locked.

Orchestrator accepted that single validation finding for a same-task,
same-section bounded correction. The current source identity is frozen at
99811 bytes / SHA-256
`2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11` /
blob `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4`; source writes and semantic
changes are forbidden. The current test identity is 144723 bytes / SHA-256
`2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17` /
blob `efe7a16ff415b6e1397c8d11865423314662a82c`. Only that existing test owner
may add the durable raised-`OSError` regression while preserving returncode-2
and nonancestor cases. Final expected changed lines are 300–320 with hard cap
330; focused final-candidate invocation cap is one and full discovery stays
zero. Section 2 remains locked.

The bounded durable-regression pass completed on activation
`6a5e2836b802940c3b58803a7a88b565b6050d37`. Production source had zero writes
and retained its frozen identity. The existing test owner added one durable
raised-`OSError` ancestry regression while preserving returncode-2 and
nonancestor cases. Final candidate size is `311` changed lines (`96+/1-` source,
`214+` tests). Affected tests pass `2/2`, the single final-candidate focused
suite passes `51/51`, and compile/CodeGraph/scope/diff checks pass. Full
discovery and all package/root/device/network/formal/release effects remain
zero.

State: `READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_DURABLE_REGRESSION_REVIEW`.
Section 2 remains locked pending Planner acceptance, Orchestrator commit and
the required two consecutive independent clean xhigh reviews.

Planner accepted the final uncommitted candidate as
`ACCEPTED_SECTION_1_DURABLE_OSERROR_REGRESSION_QUALIFIED_PENDING_ORCHESTRATOR_CHECKPOINT`.
The reviewed PLAN and ER are frozen at
`.agent-work/archived/PLAN-20260805-0345.md` and
`.agent-work/archived/EXECUTION_RESULT-20260805-0345.md`. Live PLAN is now a
non-executable terminal stop. Orchestrator must verify the exact identities,
create the exact two-owner-path checkpoint, and obtain two consecutive
independent clean xhigh reviews. Section 2 remains locked until all three gates
are recorded.

Orchestrator recorded Section 1 checkpoint
`5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74`, tree
`656fee670f289b0a20fea1a8c015762afd44a5c0`, and two independent clean
reviews. FULL and PLAN-FULL agree on `READY_FOR_SECTION_2_PLANNER_PASS`.
Planner issued one same-task executable Section 2 package covering only the
existing stage-gate/test owners, replacement task/FULL projection/future child
topology, focused validation and PLAN-FULL's sole full discovery. It awaits the
exact version-controlled activation docs checkpoint; package/root/device/formal/
release authority remains zero.

## Section 2 execution handoff

Activation `1f7556d36049c33bd4f99412d945db02fe448fa8` passed exact parent,
subject, ten-path, machine-contract and immutable Section 1 identity checks. The
Executer changed only the existing stage-gate/test owners, binding the
replacement package task/contract, distinct future formal task, unfinished-only
FULL projection, all-false authority map and exact future code-child topology.
Final candidate size is `455` changed lines (`102+/90-` source,
`123+/140-` tests), below the `500` hard cap. Candidate worktree blobs are
`6f7a7756687f669c067c253a5d5a30f84b5d6075` and
`65e54f1594ed39c2be641124de71b946858c1e6b`.

Targeted behavior passed `8/8`. The sole stage-gate focused run found one
alternate-root fixture omission; the single authorized bounded correction added
the new projection contract to that fixture, and its exact final targeted test
passed `1/1`. Terminal passed `6/6`. Thermal reproduced the independently
attributed governance-lineage baseline group (`2 failures + 8 errors`, all at
`AGENTS.md` identity). Compile, CodeGraph sync/query, scope/machine and diff
checks passed.

The sole visible-Terminal full discovery used PID `62893`, TTY `/dev/ttys002`,
token/root `g4-r6-section2-full-discovery-20260805-a91c5e2d`, and exited before
collection with `ImportError: Start directory is not importable` for the repo
`tests` directory. Output SHA-256 is
`192c78c880e975096c5f4fe40292ad9c14c1c865cff1714c2fc2ba4d9e908703`.
Retry cap is zero, so it was not rerun. Package/formal/device/network/release
effects and commits remain zero.

State: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW` with
`VALIDATION_NON_GREEN_FULL_DISCOVERY_STARTUP_FAILURE_NO_RETRY`.

## Section 2 Planner review and final qualification continuation

Planner accepts the candidate semantics provisionally and rejects only final
qualification. The source/test identities are frozen at source 99962 bytes /
SHA-256 `0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0` /
blob `6f7a7756687f669c067c253a5d5a30f84b5d6075`, and test 146189 bytes /
SHA-256 `540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352` /
blob `65e54f1594ed39c2be641124de71b946858c1e6b`. Production and test writes are
now zero.

The failed full command is preserved as immutable validation history, but it is
a Planner command/harness-contract defect rather than a production semantic or
full-suite failure: `unittest discover -s tests -t .` requires the repository's
non-package `tests/` directory to be importable and exited before collecting any
test. It consumed zero effective full collections and does not authorize a
retry of that invalid command. No Human or Advisor decision is implicated.

Reviewed PLAN and ER are archived at
`.agent-work/archived/PLAN-20260805-0435.md` (SHA-256
`0f73e25257ae85a081431745d815adcedcb673ab074713121e20c9243abd8ad5`) and
`.agent-work/archived/EXECUTION_RESULT-20260805-0435.md` (SHA-256
`5684e33970ad776c1cc3d14867e2688fbbd0a4513b02bbb0b6cc436845c4ad8f`).
The same stable task and Section 2 continue without a corrective suffix, new
package or new root. The only remaining qualification is one post-correction
stage-gate focused invocation and one effective repository full discovery using
the canonical non-`-t` command. Trusted targeted, terminal, thermal, compile and
CodeGraph evidence must not be repeated. Any non-green full result is acceptable
only if it is exactly the already attributed two failures plus eight errors,
with every first failing frame at the pre-existing governance-lineage
`AGENTS.md` identity boundary and no changed-owner regression.

State: `SECTION_2_FROZEN_CANDIDATE_FINAL_QUALIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.
