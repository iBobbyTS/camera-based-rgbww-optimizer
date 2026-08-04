# EXECUTION_RESULT archive metadata

- archive_status: `REVIEWED_DIRECT_SCRIPT_VALIDATION_FOCUSED_FAILURE`
- archive_timestamp_utc: `2026-08-04T20:02:11Z`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- applicable_task: `REF-G4-06-RAY-R6`
- reviewed_scope: `DIRECT_SCRIPT_VISIBLE_TERMINAL_VALIDATION_THROUGH_FOCUSED_FAILURE`
- source_checkpoint: `96d18dd24d649519d1759ac05b66e5ca97501539`
- source_body_bytes: `9460`
- source_body_sha256: `6ceb5fff59298b081592f900643b88040557dcc251480e86876bde7c19a3899e`
- terminal_disposition: `ONE_FOCUSED_ONLY_COMMITTED_SOURCE_BLOB_REFERENCE_INTEGRATION_SEAM`
- canonical_error: `committed_source_candidate_blob_drift`
- harness_disposition: `ACCEPTED_REUSABLE_DIRECT_SCRIPT_PACKAGING_EVIDENCE_CURRENT_SCRIPT_ROOT_IMMUTABLE_NOT_REUSED`
- focused_result: `202 tests / 102.948s / 149 error instances / one repeated seam`
- downstream_validation: `post-focused CodeGraph full all zero`
- candidate_source_sha256: `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83`
- candidate_test_sha256: `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e`
- candidate_disposition: `PRESERVED_UNACCEPTED_UNREJECTED_PENDING_BOUNDED_CORRECTION`
- exact_next_branch: `REF-G4-06-RAY-R6 / G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1 / SINGLE_BLOB_REFERENCE_DIAGNOSTIC_CORRECTION_AND_FINAL_VALIDATION`
- stop: `RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`
- historical_non_executable: `true`

This archive does not authorize execution, current-root reuse, device access,
release consumption, retry, formal work, or commit.

---
# EXECUTION_RESULT

## Terminal status request

`READY_FOR_PLANNER_G4_06_ROUTE_A_DIRECT_SCRIPT_VALIDATION_FAILURE_REVIEW`

- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1`
- Phase: `FINAL_CODE_CANDIDATE_DIRECT_SCRIPT_VISIBLE_TERMINAL_VALIDATION`
- Terminal branch: `FOCUSED_FAILED_FULL_NOT_STARTED`
- Candidate disposition:
  `PRESERVED_UNACCEPTED_UNREJECTED_PENDING_PLANNER_FAILURE_REVIEW`
- Planner stop: `RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`

The Human-directed plain-script launcher and command seal succeeded. The exact
focused integration command then failed. This is validation evidence for the
current frozen candidate, not a launcher/seal failure, scientific/formal/device
failure, GUIDE hard stop, release result, or hardware-readiness claim. No
correction, retry, resume, alternate root, third launcher attempt, or full suite
was run.

## Activation and machine intake

- Branch: `main`
- HEAD: `96d18dd24d649519d1759ac05b66e5ca97501539`
- Sole parent: `4c77fe46e9d755467f262fc63ac8e329c8847ff3`
- Subject: `docs(plan): activate direct Terminal script validation`
- Exact activation paths:
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/EXECUTION_RESULT-20260804-1942.md`
  - `.agent-work/archived/PLAN-20260804-1942.md`
- Repo-owned strict parser: PLAN/FULL active `1/1`, same task and contract,
  PLAN executable, FULL `executable=false`, FULL non-executable reference true,
  required FULL subset exact.
- PLAN source: `15991` bytes, SHA-256
  `a599ea5b297e327cadf79e2fda6b217aa1514c3846c64a0b786f8fbec2641971`;
  one machine row at line `21`.
- FULL source: `15457` bytes, SHA-256
  `86018eb8458ac22eb2a067330022798afe963d8190c5e1c9000b06bece9b3612`;
  one machine row at line `24`.

The exact new direct-script path and new validation root were both proven
absent using non-following checks before materialization. The rejected old
partial root was not read, statted, listed, described, modified, cleaned, or
reused.

## Frozen candidate and inherited validation

- Source: `94324` bytes, SHA-256
  `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83`.
- Test: `133201` bytes, SHA-256
  `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e`.
- Exact numstat: source `+35/-8`; test `+67/-1`.
- Candidate writes by this continuation: `0`.
- Inherited targeted: `47/47`, `182.148s`, exit `0`; not rerun.
- Inherited compile: exit `0`; not rerun.

Candidate bytes/SHA and numstat passed before script creation, at script startup,
at validation step 1, and at all three liveness boundaries. They remained exact
when the Terminal process ended.

## Direct script materialization

Human correction followed:

`直接把脚本放在临时目录执行，不要用base64`

Exact script:

`/Volumes/4T/temp/rgbww-optimizer/g4-route-a-direct-terminal-4c77fe46e9d7-20260804T194205Z.zsh`

- Creation owner: Executer `apply_patch`.
- Plain UTF-8, LF-only, trailing LF present.
- No encoded payload transport, dynamic decoded source, or `eval`.
- Bytes: `18676`.
- SHA-256:
  `804ee45d35ecad359701cf15eb4f2e9e17722b04cbe84d873ebb330b562310b1`.
- Initial mode after materialization: `0644`.
- `/bin/zsh -n <exact-script>`: exit `0`.
- Final launch mode: `0600`.
- Bytes/SHA/UTF-8/LF identity after chmod: unchanged.
- Script self-delete or post-launch rewrite: `0`.

The script directly contains literal zsh commands and Python heredocs. Startup
validated its own regular-file identity and the candidate, exclusively created
the new root, immediately established stdout/stderr/exit, installed the EXIT
trap, wrote the command seal using literal Python data plus argv and
`json.dump`, and validated the exact four-file inventory before focused tests.

## Sole direct-script AppleScript launch

- Historical rejected launcher attempt count: `1`.
- Direct-script correction attempt count: `1/1`.
- This PLAN's `/usr/bin/osascript` invocation count: `1/1`.
- AppleScript operations: one Terminal `activate`, one `do script`, direct
  returned-tab TTY readback, immediate front-window id readback.
- `do script` command:
  `/bin/zsh '/Volumes/4T/temp/rgbww-optimizer/g4-route-a-direct-terminal-4c77fe46e9d7-20260804T194205Z.zsh'`
- AppleScript exit: `0`.
- Front window id: `62300`.
- Returned-tab TTY: `/dev/ttys020`.
- Launch token:
  `g4-route-a-direct-4c77fe46e9d7-20260804T194205Z`.
- Sealed shell PID: `38797`.
- Sealed shell TTY: `/dev/ttys020`.
- Sealed start time: `2026-08-04T19:51:43.464050+00:00`.

Window/TTY/token readback matched the seal. No tab enumeration or comparison,
second AppleScript, third launcher attempt, Codex validation owner, or
background validation owner was used.

## Exact validation root and command seal

Validation root:

`/Volumes/4T/temp/rgbww-optimizer/g4-route-a-direct-terminal-validation-4c77fe46e9d7-20260804T194205Z`

- Root: regular directory, mode `0700`, exclusively created by the Terminal
  script.
- Inventory was and remains the exact four allowed files.
- All four files are regular, non-symlink, mode `0600`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `command-seal.json` | 3587 | `d9ac8b0a08abdea8641c12a487262a383c4148cc1177b16a80c2c2be1007c93d` |
| `validation.stdout.log` | 5451 | `b085fe9de8b5424b05e289234619679fdf525e36a9b6b3201360c8406c76ab5c` |
| `validation.stderr.log` | 334104 | `08cb24535f816e1ed1fb331a9ca5c29c501944bb155c840b5557c6575e882309` |
| `validation.exit` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |

The seal is canonical JSON with schema
`g4_route_a_direct_terminal_validation_command_seal_v1`, exact activation,
candidate and script identities, eight ordered commands, PID/TTY/token,
single-launch and zero-retry counters, and exact output paths. The terminal
exit file contains exact text `1\n`.

The direct script and root are retained as immutable harness/validation
evidence. They were not cleaned, deleted, overwritten, resumed, or reused.

## Three sparse liveness checks

All checks bound the same token, PID `38797`, TTY `/dev/ttys020`, exact script
identity and candidate identity.

1. Check 1: process alive, elapsed `00:41`; seal/stdout/stderr/exit sizes
   `3587/5052/107/0`; exact process command
   `/bin/zsh <exact-direct-script>`.
2. Check 2: process alive, elapsed `01:21`; sizes
   `3587/5052/5571/0`; logs monotonic and candidate/script unchanged.
3. Check 3: process terminated before the check; final sizes
   `3587/5451/334104/2`; exit `1\n`; candidate/script unchanged.

Because the process completed before the third live boundary, no automation or
additional polling was created.

## Validation order and failure result

Seal/inventory step 0 passed, and its begin/end markers are present. Candidate
identity/diff step 1 passed, and its begin/end markers are present.

Focused integration step 2 ran exactly once with exact argv:

```text
.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics
```

Result:

- started: `2026-08-04T19:51:43Z`;
- tests run: `202`;
- duration: `102.948s`;
- terminal summary: `FAILED (errors=149)`;
- overall sequence exit: `1`;
- repeated error boundary observed in the trace:
  `committed_source_candidate_blob_drift`;
- focused END-success marker: absent, as required by fail-closed execution.

The error trace shows synthetic stage-gate fixture construction reaching the
existing `validate_committed_source_attestation` owner and raising
`StageGateError("committed_source_candidate_blob_drift")`. This handoff records
the observed boundary without diagnosing or repairing it.

Because focused failed:

- post-focused candidate step 3: not started;
- `git diff --check` step 4: not started;
- `codegraph sync` step 5: not started;
- CodeGraph query step 6: not started;
- strict machine/scope/authority step 7: not started;
- fresh full step 8: not started;
- full-suite retries: `0`;
- previous interrupted full reused: `false`.

No offline focused failure is expressed as release, formal, scientific,
hardware, eligibility, or readiness evidence.

## Scope and zero effects

- Candidate/source/test writes: `0`.
- PLAN/FULL/GUIDE/RESEARCH/archive writes: `0`.
- Git stage/commit/push/PR: `0/0/0/0`.
- Old partial root access: `0`.
- Existing external experiment/package/formal root access: `0`.
- Network/device/backend/camera/Ray/strip/capture calls: `0/0/0/0/0/0/0`.
- Release/retained-R3/formal-R6/analysis/TD-C consumption or execution:
  `0/0/0/0/0`.
- Formal owner/root/device effects: `0/0/0`.
- Retry/resume/alternate root/third launcher: `0/0/0/0`.

Focused tests used their existing auto-cleaned synthetic temporary-fixture
mechanisms only. They did not access or consume an existing experiment,
package, release, device, or formal root.

## Planner handoff

Planner should review the exact focused failure and decide the bounded next
engineering disposition. The candidate is not accepted, and this Executer does
not diagnose, repair, rerun, create a successor/corrective task, or infer a
scientific/formal branch. The direct launcher and seal are successful evidence;
the validation failure is downstream at the committed candidate blob boundary.

Do not run a third launcher attempt, retry/resume this root, run the full suite,
or modify the candidate under this completed PLAN. No future checkpoint or tree
SHA is guessed.
