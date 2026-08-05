# EXECUTION_RESULT archive — G4-06 Section 2 final qualification

- Archive status: `REVIEWED_ACCEPTED_SECTION_2_QUALIFIED_NON_GREEN_HISTORICAL_NON_EXECUTABLE`
- Archive timestamp UTC: `2026-08-05T05:15:25Z`
- Original ER bytes: `5439`
- Original ER SHA-256: `53a7aaa7bf00b39e6ae6dfd10ecb7e34bc8aac9ce3da275b0d0166edf889967f`
- Planner decision: `ACCEPTED_SECTION_2_QUALIFIED_NON_GREEN`
- Full green: `false`
- Planner stop: `RETURN_FOR_ORCHESTRATOR_SECTION_2_EXACT_CODE_COMMIT_AND_TWO_CLEAN_REVIEWS`
- Archive authority: `historical_non_executable`

## G4-06 Section 2 frozen-candidate final qualification handoff

`RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_FINAL_QUALIFICATION_REVIEW`

- Contract: `G4-R6-LARGE-CHANGE-SECTION-2-FROZEN-CANDIDATE-FINAL-QUALIFICATION-V1`
- Stable task/section: `REF-G4-06-REPLACEMENT-PACKAGE` /
  `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`
- Disposition: `QUALIFIED_NON_GREEN_EXACT_GOVERNANCE_LINEAGE_BASELINE`
- Full green: no
- Commit: none

## Activation and frozen candidate

Activation `4e94594c117cd684e76b3607815f340cd2ca5919` was verified as the
direct non-merge child of `1f7556d36049c33bd4f99412d945db02fe448fa8`
with parent tree `813d90d31fa4a4650ef4ccde338f64db30eaaada`, subject
`docs(plan): qualify section 2 frozen candidate`, and exactly the eight
PLAN-listed governance paths. PLAN/FULL/PLAN-FULL machine state and reviewed
archive identities matched. The implementation candidate remained dirty,
unstaged and byte-identical throughout qualification:

| owner | bytes | SHA-256 | worktree blob | numstat |
| --- | ---: | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | 99962 | `0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0` | `6f7a7756687f669c067c253a5d5a30f84b5d6075` | `102+/90-` |
| `tests/test_p7_td_b_r6_stage_gate.py` | 146189 | `540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352` | `65e54f1594ed39c2be641124de71b946858c1e6b` | `123+/140-` |

Source/test writes during final qualification: `0/0`. Other implementation
writes: `0`. `git diff --check` passed before both qualification commands.

## Focused final qualification

Exact invocation:

`PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest tests.test_p7_td_b_r6_stage_gate`

Result: `Ran 51 tests in 329.308s`, exit `0`, `OK`. This is the sole
post-correction stage-gate focused invocation. No failure/error occurred and no
edit followed it.

## Valid full collection

- Exact argv evidence:
  `/usr/bin/env PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p test_*.py`
- Forbidden `-t`: absent
- Visible Terminal PID / TTY: `27393` / `/dev/ttys002`
- Token: `g4-r6-section2-valid-full-20260805-b73d91f4`
- Flat evidence prefix:
  `/Volumes/4T/temp/rgbww-optimizer/g4-r6-section2-valid-full-20260805-b73d91f4`
- UTC start/end: `2026-08-05T04:53:27Z` /
  `2026-08-05T05:01:34Z`
- Exit: `1`
- Log: `31889 bytes / 481 lines`
- Log SHA-256:
  `e71af39fc5e43d4f6affbe324c1742b4eeefbeb7a5e46883562a930f282dedea`
- Terminal summary: `Ran 979 tests in 487.070s` /
  `FAILED (failures=2, errors=8)`
- Effective collection: yes, `979 > 0`
- Retry/redispatch: `0`
- Sparse liveness checks: exactly `3`, all `ALIVE`
- Wake automation: Orchestrator-created and subsequently deleted

The eight errors and two failures are exactly the previously attributed
`test_p7_thermal_diagnostics` governance-lineage group. Each traceback reaches
the existing rejection `ValueError: TD-B governance successor path identity
differs: AGENTS.md`; the two failures are assertion-message mismatches caused by
that same earlier rejection. Exact test identities:

1. `test_agents_policy_lineage_rejects_wrong_bytes_owner_and_provenance`
2. `test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`
3. `test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`
4. `test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`
5. `test_lineage_release_rejects_candidate_and_resolved_plan_tampering`
6. `test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`
7. `test_public_default_successor_lineage_layers_historical_and_current_owners`
8. `test_public_default_successor_manifest_fails_closed_on_exact_drift`
9. `test_recovery_head_fails_closed_and_historical_policy_remains_replayable`
10. `test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift`

There is no changed-owner, stage-gate or terminal failure/error, and no
additional failure/error. Therefore the valid full collection satisfies the
PLAN's exact qualified-baseline branch. It is `qualified non-green`, never
`full green`.

## Preserved invalid invocation

The prior command
`.venv/bin/python -m unittest discover -s tests -t .` remains immutable
history: exit `1`, collected tests `0`, output SHA-256
`192c78c880e975096c5f4fe40292ad9c14c1c865cff1714c2fc2ba4d9e908703`.
Its classification remains
`PLANNER_COMMAND_HARNESS_CONTRACT_ERROR_BEFORE_COLLECTION`; it is not a
production semantic failure, full-test failure or valid-full retry. It was not
rerun or overwritten.

## Inherited evidence and zero effects

- targeted initial/final: `8/8 PASS`, `1/1 PASS`
- bounded correction: `1`, test-fixture projection-contract copy only
- terminal focused: `6/6 PASS`
- thermal focused: same `79 pass / 2 fail / 8 error` governance baseline
- compile / CodeGraph / exact scope and machine checks: pass
- source/test/other implementation writes in final qualification: `0/0/0`
- package prepare/describe/root selection/root creation: `0`
- old package/formal root access: `0`
- device/network/camera/Ray/strip/capture effects: `0`
- release consumption/formal execution/G4-07/TD-C: `0`
- commits/pushes/PRs: `0`

Planner review independently confirmed the exact terminal argv/seal, all ten
non-green test identities, the absence of additional changed-owner/stage-gate/
terminal failures, and frozen candidate bytes/SHA/blob/numstat. The result is
accepted only as `ACCEPTED_SECTION_2_QUALIFIED_NON_GREEN`.
