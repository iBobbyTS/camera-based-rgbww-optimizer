# EXECUTION_RESULT archive metadata

- archive_status: `REVIEWED_BASE64_LAUNCHER_COMMAND_SEAL_FAILURE`
- archive_timestamp_utc: `2026-08-04T19:42:05Z`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- applicable_task: `REF-G4-06-RAY-R6`
- reviewed_scope: `BASE64_APPLESCRIPT_VISIBLE_TERMINAL_LAUNCHER_AND_COMMAND_SEAL_HARNESS`
- source_checkpoint: `4c77fe46e9d755467f262fc63ac8e329c8847ff3`
- source_body_bytes: `12900`
- source_body_sha256: `ccae1bca2ac1cfce5fd174b4753abed4e8df35e2b2f663791d7f7a936b5d9007`
- terminal_disposition: `REJECTED_BASE64_LAUNCHER_HARNESS_ONLY_CANDIDATE_PRESERVED`
- canonical_failure: `BASE64_EMBEDDED_COMMAND_SEAL_JSON_TRANSCRIPTION_INVALID`
- candidate_source_sha256: `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83`
- candidate_test_sha256: `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e`
- validation_summary: `targeted 47/47 and compile inherited; focused/CodeGraph/full zero`
- root_summary: `old root 0700 with empty 0600 seal only; retained immutable; not reused or read again`
- production_test_failure_increment: `0/0`
- exact_next_branch: `REF-G4-06-RAY-R6 / G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1 / DIRECT_PLAIN_ZSH_VISIBLE_TERMINAL_VALIDATION`
- stop: `RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`
- historical_non_executable: `true`

This archive does not authorize execution, launcher replay, old-root access, device
access, release consumption, retry, formal work, or commit.

---
# EXECUTION_RESULT

## Terminal status request

`READY_FOR_PLANNER_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_VALIDATION_FAILURE_REVIEW`

- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1`
- Current phase:
  `FINAL_CODE_CANDIDATE_VISIBLE_TERMINAL_REMAINING_VALIDATION`
- Failure classification:
  `PRE_VALIDATION_VISIBLE_TERMINAL_LAUNCHER_IDENTITY_AND_COMMAND_SEAL_PACKAGING_FAILURE`
- Candidate disposition:
  `PRESERVED_UNACCEPTED_UNREJECTED_NO_CANDIDATE_FAILURE_EVIDENCE`
- Planner stop: `RETURN_FOR_G4_06_ROUTE_A_FINAL_CODE_CANDIDATE_REVIEW`

This is a pre-validation launcher/seal packaging failure. It is not a
candidate production-seam failure, test failure, scientific/formal/device
failure, GUIDE hard stop, release result, or candidate acceptance/rejection.
No validation command started and no candidate evidence changed.

## Human authority and activation intake

The live PLAN recorded the current Human decision
`ALLOW_OSASCRIPT_OR_APPLESCRIPT` for one Human-visible macOS Terminal
`activate` plus one `do script` and window/tab/TTY readback. That authority did
not permit a second invocation, retry, resume, alternate root, file I/O by
AppleScript, or device/network action.

Activation intake passed before launch:

- Branch: `main`
- HEAD: `4c77fe46e9d755467f262fc63ac8e329c8847ff3`
- Sole parent: `11c64bffab0745babe9723784ad506610c03178d`
- Subject: `docs(plan): activate Route A Terminal validation`
- Exact activation paths:
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/PLAN-20260804-1925.md`
- Repo-owned strict parser: PLAN/FULL active `1/1`, same task
  `REF-G4-06-RAY-R6`, same contract, PLAN executable, FULL
  `executable=false`, FULL non-executable reference true, and required FULL
  subset exact.
- PLAN parser source: `13960` bytes, SHA-256
  `a8df10656cbd9f18c7102e0dfdaa4a565362cfe8ec72cad9e52952647599a466`;
  one machine row at line `18`.
- FULL parser source: `15407` bytes, SHA-256
  `63a5d83f2f31bfde297fae4aa9b6dc4b7bbded95dff53ef5945ba787e855d7b3`;
  one machine row at line `24`.

## Frozen candidate and inherited validation

The pre-launch candidate gate passed:

- Source: `94324` bytes, SHA-256
  `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83`.
- Test: `133201` bytes, SHA-256
  `479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e`.
- Exact numstat: source `+35/-8`; test `+67/-1`.
- Exact pre-launch dirty scope: those two candidate paths only.
- Candidate writes in this continuation: `0`.
- Inherited targeted: `47/47`, `182.148s`, exit `0`; not rerun.
- Inherited compile: exit `0`; not rerun.

The Terminal shell failed before any validation command and performed no
repository write. The candidate therefore remained unchanged from the exact
pre-launch identity. No candidate production/test conclusion is inferred from
the packaging failure.

## Launcher construction and sole AppleScript invocation

The initial in-memory launcher construction attempted to use an unavailable
JavaScript `btoa` global and stopped before calling any tool or `osascript`:

`ReferenceError: btoa is not defined`

This consumed zero invocation budget and made no file or UI change. Per
Orchestrator direction it was treated as a pre-launch encoding-harness
correction. A custom ASCII/base64 encoder and decoder then proved byte-exact
round trips for the shell payload, command-seal template, and AppleScript
payload before the only actual invocation.

- Unique launch token used in the sole `do script` command:
  `g4-route-a-4c77fe46e9d7-msf25zmf-100f4309`
- `/usr/bin/osascript` invocations: `1`
- AppleScript operations: one `activate`, one `do script`, one attempted
  window/tab/TTY identity readback.
- Invocation exit: `1`
- Exact launcher error:

  `31014:31063: execution error: launched tab identity not found in front window (-2700)`

The error occurred after `do script`, so a Terminal shell was likely launched,
but AppleScript returned no reliable window/tab/TTY identity. No identity was
guessed or reconstructed. The PLAN therefore required immediate failure with
no second AppleScript invocation.

## Minimal launcher-payload diagnostics

The payloads were assembled inside one ephemeral V8 tool isolate. That isolate
ended after the sole `osascript` invocation, and neither full payload was
persisted to an authorized evidence file. The conversation retains the source
construction logic but not the expanded base64-bearing strings as independently
addressable byte objects. Therefore the following requested identities are
unavailable and must not be guessed:

- exact expanded AppleScript source bytes: `UNRECOVERABLE_NOT_PERSISTED`;
- exact expanded AppleScript source SHA-256: `UNRECOVERABLE_NOT_PERSISTED`;
- exact expanded Terminal shell payload bytes: `UNRECOVERABLE_NOT_PERSISTED`;
- exact expanded Terminal shell payload SHA-256:
  `UNRECOVERABLE_NOT_PERSISTED`.

Before invocation, the custom ASCII/base64 encoder and decoder did prove exact
in-memory round trips for the expanded AppleScript, shell, and seal-template
strings. That proves encoding equality at launch construction time, but it does
not provide a recoverable post-failure byte count or digest and is not presented
as one.

The minimal retained AppleScript identity-readback source shape was:

```applescript
tell application "Terminal"
activate
set launchedTab to do script "<single base64-bearing zsh command>"
delay 2
set launchedTTY to tty of launchedTab
set launchedWindow to front window
set launchedIndex to 0
repeat with tabIndex from 1 to count of tabs of launchedWindow
  if tty of item tabIndex of tabs of launchedWindow is launchedTTY then
    set launchedIndex to tabIndex
    exit repeat
  end if
end repeat
if launchedIndex is 0 then error "launched tab identity not found in front window"
return (id of launchedWindow as text) & "|" & (launchedIndex as text) & "|" & launchedTTY & "|" & "<launch token>"
end tell
```

Angle-bracket fields above are intentional redactions of expanded values that
were not persisted; the snippet is sufficient to reconstruct the observed
identity bug. It selected `front window` after `do script`, then required the
returned tab's TTY to be found among that front window's tabs. The exact
`-2700` error proves that this search completed with `launchedIndex = 0`; it
does not prove whether the returned tab belonged to a different window, the
front window changed during the two-second delay, or another Terminal identity
condition occurred.

The retained shell setup order, before any validation command, was:

```zsh
set -eu
umask 077
mkdir -- "$validation_root"
shell_tty=$(/usr/bin/tty)
seal_template_b64="<expanded seal template>"
identity_code="$(printf %s '<encoded identity code>' | /usr/bin/base64 -D)"
machine_code="$(printf %s '<encoded machine code>' | /usr/bin/base64 -D)"
query_text="$(printf %s '<encoded CodeGraph query>' | /usr/bin/base64 -D)"
/usr/bin/python3 -c '<seal writer code>' "$seal_template_b64" "$$" "$shell_tty" > "$seal_path"
: > "$stdout_path"
: > "$stderr_path"
write_validation_exit() { ... }
trap write_validation_exit EXIT
(
  # fail-closed validation order 1 through 8
) > "$stdout_path" 2> "$stderr_path"
```

Thus the exclusive root was created first; shell TTY and in-memory command
inputs were derived second; the command seal was redirected and written third;
stdout/stderr files, the EXIT trap, and all validation steps came only after a
successful seal writer.

The exact retained command-seal writer argv/source was:

```zsh
/usr/bin/python3 -c 'import base64,datetime,json,sys; d=json.loads(base64.b64decode(sys.argv[1])); d["shell_pid"]=int(sys.argv[2]); d["shell_tty"]=sys.argv[3]; d["started_at_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat(); print(json.dumps(d,sort_keys=True,separators=(",",":")))' "$seal_template_b64" "$$" "$shell_tty" > "$seal_path"
```

The zero-byte seal is explained by ordinary shell redirection semantics: the
shell created/truncated `command-seal.json` before starting the writer command,
and the writer did not produce stdout successfully.

Human subsequently supplied the original visible-Terminal trace. That trace is
authoritative observed evidence for this launcher attempt and supersedes the
earlier `UNKNOWN` exact-cause statement:

- the base64-decoded shell did run in the visible Terminal;
- the command-seal writer ran under Xcode Python `3.9`;
- its `json.loads` failed with the exact error:

  `JSONDecodeError: Expecting ':' delimiter: line 1 column 2487 (char 2486)`

- the Terminal then returned to its prompt without entering validation.

Canonical root-cause classification:

`BASE64_EMBEDDED_COMMAND_SEAL_JSON_TRANSCRIPTION_INVALID`

This evidence proves that the embedded command-seal JSON presented to
`json.loads` was syntactically invalid at character `2486`; it does not restore
the complete expanded payload bytes or SHA-256, because those byte strings were
not persisted. The earlier evidence statement `SEAL_WRITER_EXITED_BEFORE_STDOUT`
remains true as the effect boundary, while its exact cause is no longer
`UNKNOWN`.

Human's explicit engineering correction directive for the next packaging pass
is:

`直接把脚本放在临时目录执行，不要用base64`

Accordingly, any later authorized attempt must use a directly stored script in
the authorized temporary directory and must not reconstruct, replay, or embed
this base64 transport. This handoff does not itself create that script or
authorize another launch.

No diagnostic reconstruction was executed, no payload was relaunched, and no
second AppleScript, Terminal command, seal writer, validation, retry, resume, or
alternate root was attempted.

## Exact reserved-root evidence

Before launch, a non-following check proved the exact reserved path absent:

`/Volumes/4T/temp/rgbww-optimizer/g4-route-a-terminal-validation-7214ff5eb797-20260804T184848Z`

After the failed launcher readback, one bounded forensic read of this exact
reserved path showed that the launched shell reached exclusive root creation
and command-seal redirection, then failed before producing a seal or installing
the validation logging/trap sequence:

- Root: present directory, mode `0700`.
- Exact inventory: one file only.
- `command-seal.json`: regular file, mode `0600`, `0` bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `validation.stdout.log`: absent.
- `validation.stderr.log`: absent.
- `validation.exit`: absent.
- Parsed command seal: unavailable because the file is empty.
- Sealed PID: unavailable.
- Sealed TTY: unavailable.
- Sealed launch token: unavailable.
- AppleScript window/tab/TTY identity: unavailable.

The partial root is retained immutable as failure evidence. It was not cleaned,
deleted, overwritten, completed, resumed, or reused, and no alternate root was
created. Future work must not treat it as a fresh validation root.

## Validation order and zero-start evidence

Because command-seal creation did not complete, all PLAN validation steps
remained not started:

- Candidate identity step 1 starts/runs: `0/0`
- Focused integration starts/runs: `0/0`
- Post-focused identity/diff starts/runs: `0/0`
- CodeGraph sync/query: `0/0`
- Strict machine/scope/authority step starts/runs: `0/0`
- Fresh full-suite starts/runs: `0/0`
- Liveness checks: `0`
- Terminal process PID/TTY-bound ownership proof: unavailable
- Full retry count: `0`
- Previous interrupted full reused: `false`

No success, failure, count, duration, or readiness result is claimed for any
unstarted validation.

## Counters and authority boundary

- AppleScript invocations: `1/1`
- Terminal `do script` launches: `1/1` likely effected before readback failure
- Retry/resume/alternate launch: `0/0/0`
- Alternate root: `0`
- Candidate/source/test writes: `0`
- Git stage/commit/push/PR: `0/0/0/0`
- Other external experiment/package/formal root access: `0`
- Network/device/backend/camera/Ray/strip/capture calls: `0/0/0/0/0/0/0`
- Release/retained-R3/formal-R6/analysis/TD-C consumption or execution:
  `0/0/0/0/0`
- Formal owner/root/device effects: `0/0/0`

PLAN, FULL, GUIDE, RESEARCH, archives, source, and tests were read-only. Only
this live execution handoff was modified after failure.

## Planner and Orchestrator handoff

Planner should review this failure without rejecting the frozen candidate or
incrementing its production failure count. The failure is in the visible
Terminal launcher/tab-identity plus pre-validation command-seal packaging
boundary. Return to Orchestrator ownership reassessment before any new action.

Do not retry or resume the shell, invoke AppleScript again under this PLAN,
reuse or clean the partial root, create an alternate root, run validation in a
Codex background process, or create a corrective task suffix. No future code
checkpoint or tree SHA is guessed.
