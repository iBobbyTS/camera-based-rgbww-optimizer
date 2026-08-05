# EXECUTION_RESULT archive — G4-06 Section 1 durable OSError regression

- Archive status: `REVIEWED_ACCEPTED_SECTION_1_CANDIDATE_HISTORICAL_NON_EXECUTABLE`
- Archive timestamp UTC: `2026-08-05T03:45:28Z`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-REPLACEMENT-PACKAGE` / `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`
- Source checkpoint: `6a5e2836b802940c3b58803a7a88b565b6050d37`
- Source tree: `2485772afb1ddff8c2d6c7546bfac0b8c45c515d`
- Original source bytes: `3994`
- Original source SHA-256: `87b3298d4f942edcf52ccc3221e203b71b00566fb02dde4d3cbeb95989830259`
- Terminal disposition: `ACCEPTED_SECTION_1_DURABLE_OSERROR_REGRESSION_QUALIFIED_PENDING_ORCHESTRATOR_CHECKPOINT`
- Evidence pointer: `.agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md`
- Exact next stop: `RETURN_FOR_ORCHESTRATOR_SECTION_1_CHECKPOINT_AND_TWO_CLEAN_REVIEWS`
- Archive authority: `historical_non_executable`; this archive authorizes no edit, test rerun, commit, package root, prepare/describe, device, formal, release, retry, Section 2, or stage entry.

## Frozen original live EXECUTION_RESULT body

# EXECUTION_RESULT

## Terminal handoff

`READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_DURABLE_REGRESSION_REVIEW`

- Contract: `G4-R6-LARGE-CHANGE-SECTION-1-DURABLE-OSERROR-REGRESSION-V1`
- Task/section: `REF-G4-06-REPLACEMENT-PACKAGE` / `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`
- Unique stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_DURABLE_REGRESSION_REVIEW`
- Commit: none; Section 2 remains locked.

## Activation and frozen input

- Branch/HEAD: `codex/g4-r6-owner-alignment-large-change` /
  `6a5e2836b802940c3b58803a7a88b565b6050d37`.
- Direct parent/tree: `e48cc084a6f4ebdf61c26c1b426d64522030e791` /
  `48949ce15427a014075c9ff641513152a79f657c`.
- Subject and paths: `docs(plan): activate section 1 durable regression correction`;
  exact eight authorized orchestration/archive/debug paths.
- PLAN/FULL active `1/1`, matching contract/section; FULL and PLAN-FULL non-executable.
- Frozen source before/after: `99811` bytes, SHA-256
  `2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11`,
  blob `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4`, numstat `96+/1-`.
- Production source write count: `0`.
- Test input: `144723` bytes, SHA-256
  `2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17`,
  blob `efe7a16ff415b6e1397c8d11865423314662a82c`, numstat `198+`.

## Durable regression and final identity

Only `tests/test_p7_td_b_r6_stage_gate.py` changed. New durable test
`test_accepted_engineering_ancestry_oserror_has_stable_code` patches
`subject.subprocess.run` only for the accepted-engineering ancestry query,
raises `OSError`, and requires exact
`committed_source_engineering_ancestry_query_failed`; other subprocess calls
delegate to the saved real function. Existing returncode-2 and nonancestor
coverage remains in `test_accepted_engineering_git_failure_matrix`.

| path | final bytes | SHA-256 | blob | numstat |
| --- | ---: | --- | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `99811` | `2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11` | `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4` | `96+/1-` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `145652` | `891ccbdf3a3b3f62083ea680d8ddce56b6b65c15c40bb5722b95953e729ce056` | `9b8f5781f175bae1fc93cd398b8bf362c0da20e2` | `214+` |

- Final production/test changed lines: `311` (`310+/1-`), within expected
  `300–320` and below hard cap `330`.
- Source/test write counts: `0/1`; other code/test corrections: `0`.

## Validation

- Affected durable OSError plus retained returncode-2/nonancestor matrix:
  `2/2` pass, `3.023s` (`3.297s` wrapper), exit `0`.
- Final-candidate focused suite, exactly once:
  `tests.test_p7_td_b_r6_stage_gate` -> `51/51` pass, `275.430s`
  (`275.566s` wrapper), exit `0`.
- Final two-file compile: pass, `0.109s`, exit `0`.
- Scratch roots: Python `TemporaryDirectory` under
  `/Volumes/4T/temp/rgbww-optimizer`, auto-cleaned.
- Full discovery count: `0`.
- CodeGraph: sync `Synced 1 changed files` (test only); query confirmed the
  durable test targets `validate_committed_source_attestation` while production
  source identity remains frozen.
- Exact scope/numstat/machine and `git diff --check`: pass.
- PLAN/FULL/PLAN-FULL/archives/GUIDE/RESEARCH/config/tmp and every other
  production/test path: unchanged relative to activation HEAD.

## Zero-access/effect ledger

- Historical stash/rejected branch or commit read/apply/pop/drop/branch/copy/
  cherry-pick counts: all `0`.
- Package-root select/check/create, prepare/describe, old package/root access,
  device, network, camera, Ray, strip, capture, cleanup, formal, release,
  analysis, G4-07 and TD-C counts: all `0`.
- No scientific, quality, readiness, eligibility or release claim was produced.

## Planner request

Review the final uncommitted Section 1 candidate. Acceptance may return it to
Orchestrator for the exact two-path commit and two consecutive independent
clean xhigh reviews; this handoff does not authorize either action.
