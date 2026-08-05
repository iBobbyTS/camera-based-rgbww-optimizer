# G4 R6 owner-alignment large-change workflow

## Status

- State: `section_1_bounded_durable_oserror_regression_waiting_activation`
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
| `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING` | `BOUNDED_DURABLE_OSERROR_REGRESSION_WAITING_ACTIVATION` | none | `0/2` |
| `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY` | `LOCKED` | none | `0/2` |

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
