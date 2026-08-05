# EXECUTION_RESULT archive — G4-06 large-change Section 1 V2 candidate

- Archive status: `REVIEWED_REJECTED_DURABLE_OSERROR_REGRESSION_MISSING_HISTORICAL_NON_EXECUTABLE`
- Archive timestamp UTC: `2026-08-05T03:20:01Z`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-REPLACEMENT-PACKAGE` / `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING` V2
- Source checkpoint: `e48cc084a6f4ebdf61c26c1b426d64522030e791`
- Source tree: `48949ce15427a014075c9ff641513152a79f657c`
- Original source bytes: `6803`
- Original source SHA-256: `5affd333d9696fa0c23dcdd645439f5e5eae14c60aa0940a62ea4d4f63946631`
- Terminal disposition: `REJECTED_VALIDATION_QUALIFICATION_MISSING_DURABLE_ANCESTRY_SUBPROCESS_OSERROR_REGRESSION`
- Evidence pointer: `.agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md`
- Exact next stop: `RETURN_FOR_ORCHESTRATOR_SECTION_1_DURABLE_OSERROR_REGRESSION_PLAN`
- Archive authority: `historical_non_executable`; this archive authorizes no candidate edit, test rerun, commit, package root, prepare/describe, device, formal, release, retry, or stage entry.

## Frozen original live EXECUTION_RESULT body

# EXECUTION_RESULT

## Terminal handoff

`READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`

- Stable task: `REF-G4-06-REPLACEMENT-PACKAGE`
- Section: `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`
- Contract: `G4-R6-LARGE-CHANGE-SECTION-1-ACCEPTED-ENGINEERING-BINDING-V2`
- Unique stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`
- Section 2: locked and not executed
- Commit created by Executer: no

## Activation and freshness

- Branch: `codex/g4-r6-owner-alignment-large-change`
- Activation HEAD: `e48cc084a6f4ebdf61c26c1b426d64522030e791`
- Exact parent: `e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e`
- Parent tree: `e855f57b1ffb4a140f6123b5c8f3be8d9fed06fe`
- Subject: `docs(plan): reactivate owner alignment section 1`
- Activation topology: direct non-merge child; exact eight orchestration/debug/archive paths matched PLAN.
- Initial worktree: clean.
- PLAN/FULL: active `1/1`, matching task/contract/section; FULL and PLAN-FULL non-executable.
- PLAN-FULL: `14174` bytes, SHA-256 `ac64beaf817de2f620316303772196c156975eec088a3d5e463439b749574d1e`.
- Reviewed PLAN archive: `14701` bytes, SHA-256 `b4bb653a7ddaa121d4c4c2f2ccaa49249d73fe7fe35f70f1664613ef129aa035`.
- Reviewed ER archive: `5378` bytes, SHA-256 `9a7efee123b0aa16c9c746693fcd788b7ef53179057833b6efca0f3239093983`.
- Accepted engineering checkpoint/tree/parent/subject/two paths/two blobs matched read-only Git.

### Rejected-input ledger

- Historical stash read/apply/pop/drop/branch/copy count: `0/0/0/0/0/0`.
- Rejected branch/commit read/copy/cherry-pick count: `0/0/0`.
- No command addressed either forbidden ref.
- Prior sizing failures / semantic production failures remain `1 / 0`.

## Candidate

The existing stage-gate owner now carries one closed accepted-engineering
prerequisite seam:

1. exact accepted subject and two-path constants;
2. mandatory checkpoint/tree/direct-parent/subject/path/OID binding fields;
3. the same closed object in the committed-source descriptor contract;
4. read-only Git checks for tree, direct parent, subject, exact paths, blobs,
   query failures and ancestry to the verified parent;
5. synthetic real-Git positive and fail-closed negative coverage.

`TASK_ID`, `FUTURE_TASK_ID`, `_projection`, prerequisite projection, schema
family, CLI, package/persistence/root behavior and code-child topology are
unchanged. No new owner/module/controller/adapter/runner was added.

### Production/test identity

| path | before bytes / SHA-256 / blob | after bytes / SHA-256 / blob | numstat |
| --- | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `94324` / `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83` / `d47c2ab2655d3e5ec2d425cb225d628d31fd32f2` | `99811` / `2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11` / `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4` | `96+ / 1-` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `133201` / `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e` / `f41d1aa44056efed3e51847f25d3186b769664fd` | `144723` / `2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17` / `efe7a16ff415b6e1397c8d11865423314662a82c` | `198+ / 0-` |

- Total production/test changed lines: `295` (`294+ / 1-`), below hard cap `300`.
- Hard-cap remainder: `5`; no later compaction was used to revoke a breach.
- Source writes/test writes/semantic candidates: `1/1/1`.
- Ordinary harness corrections: `0/1`.

## Behavior/error matrix

Positive proof binds the exact synthetic accepted checkpoint, tree, direct
parent, subject, ordered two paths and ordered path/OID rows, projects the same
descriptor object, retains the existing code-child topology and leaves the
output root absent.

Negative probes passed for:

- missing/extra binding keys;
- reordered/duplicate paths and missing/reordered OID rows;
- missing/extra/mismatched descriptor object;
- wrong Git tree, direct parent, subject, changed-path set and blob OID;
- path-query failure and ancestry-query failure;
- a valid but non-ancestor accepted-engineering commit;
- unchanged existing descriptor-reference precedence;
- reference-consistent secret/historical semantic guards;
- code-child parent/subject/path/blob/lineage and per-commit post-child drift.

Stable accepted-engineering codes exercised include
`committed_source_engineering_tree_drift`,
`committed_source_engineering_parent_drift`,
`committed_source_engineering_subject_drift`,
`committed_source_engineering_paths_drift`,
`committed_source_engineering_blob_drift`,
`committed_source_engineering_paths_query_failed`,
`committed_source_engineering_ancestry_query_failed` and
`committed_source_engineering_lineage_drift`.

## Validation ledger

- Initial exact-new tests: `3/3` pass, `10.348s`.
- Updated exact-new tests after nonancestor probe: `3/3` pass, `10.715s`.
- Final targeted attestation/precedence group: `15/15` pass, `55.275s`.
- Unique focused invocation
  `PYTHONPATH=<repo> TMPDIR=<fresh> .venv/bin/python -P -B -m unittest tests.test_p7_td_b_r6_stage_gate`:
  `50/50` pass, `257.527s` (`257.701s` wrapper duration).
- Final affected ancestry/query probe: `1/1` pass, `1.964s`.
- Final two-file `py_compile`: pass, `0.081s`.
- A preliminary shell cleanup launcher was rejected before process creation by
  tool safety; no scratch/test executed and it did not consume a harness correction.
- All actual scratch directories were created and auto-cleaned through Python
  `TemporaryDirectory` under `/Volumes/4T/temp/rgbww-optimizer`.
- Full unittest discovery invocations: `0` (forbidden in Section 1).
- `codegraph sync`: `Already up to date`.
- Post-sync CodeGraph query: binding -> descriptor -> read-only Git validator
  remains one owner; persistence/root creation remains separate and unchanged.
- `git diff --check`: pass.
- Final PLAN/FULL/PLAN-FULL machine consistency: pass (`1/1`, matching Section 1,
  FULL/PLAN-FULL non-executable, all authority locks false).
- Exact changed-path subset before this handoff: the two owner paths only.
- PLAN/FULL/PLAN-FULL/GUIDE/RESEARCH/config/tmp and every other source/test path:
  unchanged relative to activation HEAD.

## Effect/authority ledger

All counts are zero: package-root select/check/create, public prepare/describe,
old package/root access, device, network, camera, Ray, strip, capture, cleanup,
formal, release, analysis, G4-07 and TD-C. No external payload was read and no
scientific result or readiness/eligibility credit was produced.

## Planner decision request

Review the uncommitted closed Section 1 candidate against the live PLAN. If
accepted, return it to Orchestrator for the exact focused commit and mandatory
two consecutive independent clean xhigh code-review passes. Do not unlock or
execute Section 2 from this handoff alone.
