# G4 R6 owner-alignment large-change workflow

## Status

- State: `active_waiting_orchestrator_section_1_activation`
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
| `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING` | `WAITING_ACTIVATION` | none | `0/2` |
| `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY` | `LOCKED` | none | `0/2` |

Section 1 owns only the closed accepted-engineering checkpoint binding,
descriptor projection and read-only Git validator seam. It cannot switch package
task/FULL projection or access a package root. Section 2 remains locked until an
accepted Section 1 commit has two consecutive independent clean reviews.

## Next action

Orchestrator independently reviews PLAN-FULL and the Section 1 PLAN, updates
FULL to the required active Section 1 machine state, and creates the exact
orchestration-only activation commit. Only then may one GPT-5.6 Sol medium
Executer implement Section 1.
