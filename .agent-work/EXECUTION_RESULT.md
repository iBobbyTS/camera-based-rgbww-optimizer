# EXECUTION_RESULT

## Terminal status request

`READY_FOR_PLANNER_G4_06_FORMAL_HARD_FAIL_REVIEW`

- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1`
- Terminal disposition: `accepted_hard_failed_formal_attempt`
- Failed phase: `terminal_replay`
- Error code: `file_lstat_failed`
- Formal pass: `false`
- Cleanup safety status:
  `STRIP_ZERO_PROVEN_RAY_ZERO_UNPROVEN_CONNECTION_REFUSED`
- Planner stop:
  `RETURN_AFTER_TERMINAL_OR_FIRST_HARD_FAIL_EVIDENCE_FOR_G4_06_REVIEW`

The Supervisor-corrected production path was launched exactly once in a Human-
visible Terminal. No package pre-read occurred after reactivation. The tracked
wrapper started one child, but the attempt terminated before any capture with
`file_lstat_failed`. The repo-owned terminal finalizer sealed the same root as an
accepted hard-failed formal attempt.

Shell cleanup and independent final-zero both failed because Ray120c returned
`ConnectionRefusedError: [Errno 61] Connection refused`. ESPHome strip readback
proved all five channels zero. After proving both owned PIDs exited, the sole
PLAN-authorized safety-only `all_off --json` was invoked once; it again proved
strip zero but could not connect to Ray. No further cleanup, retry, launch,
package read, capture, or device action was attempted. Ray zero therefore remains
unproven and must not be inferred from the connection failure.

## Reactivation and non-package predevice gates

- Branch: `main`.
- Reactivation HEAD:
  `f2f5a9468f90e9952e4ebcbd2e365f117f4d123d`.
- Sole parent:
  `30ac42b049ef11d0f60d3467079bcd223fe6ee46`.
- Parent tree:
  `4b6af3623ba2ad528cbd26d4d6e693489378eb48`.
- Subject: `docs(plan): reactivate Ray R6 formal acquisition`.
- Exact changed paths:
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/EXECUTION_RESULT-20260804-2223.md`
  - `.agent-work/archived/PLAN-20260804-2223.md`
- Direct non-merge docs-only child: true.
- `src/`, `tests/`, `config/`, `advisor/`, `tmp/` changes in child: `0`.
- Worktree before launch delivery: clean.
- Old owned wrapper/formal process: absent.
- Active automation at reactivation: none, per Orchestrator intake attestation.
- Exact formal basename non-following absence gate: pass.
- Formal-root pre-create content/stat/list/read access: `0`.

Repo-owned PLAN/FULL strict parser passed:

- active count: `1/1`;
- active/current/canonical task: `REF-G4-06-RAY-R6`;
- contract:
  `G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1`;
- PLAN executable: true;
- FULL executable: false;
- FULL non-executable reference: true;
- FULL `g4_06_state` exactly equals PLAN `required_full_g4_06_state`;
- FULL top-level `supervisor_correction_ledger` exactly equals PLAN ledger;
- immutable code checkpoint/tree, final package binding and source-frozen flag:
  exact;
- FULL top-level device/formal/release authority: all false;
- package pre-read/describe/replay/prepare/probe caps: all `0`;
- production loader cap: `1`, with orchestration drift allowed.

Machine evidence:

`{"active":[1,1],"contract":"G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1","full_line":24,"package_preread_cap":0,"plan_line":15,"status":"PASS","supervisor_ledger_exact":true,"task":"REF-G4-06-RAY-R6"}`

GUIDE and runtime-owner SHA-256 gates passed:

| Path | SHA-256 |
|---|---|
| `advisor/4/4.GUIDE.md` | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py` | `f6c5f6e4e002863d34eb39a578b56e92a31ad70c907570d3537152d73030f8e3` |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py` | `4e38d97000f7e908fb56db5ac731e28182f7759f45b394881d66a1791a144e3e` |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83` |
| `tmp/run-p7-thermal-diagnostics.zsh` | `a82a6689e6fe4b4d403f3b84c8612cf79c7d35463cd89047ccbf9febd43d52df` |

No standalone package `describe`, replay, prepare, remint, probe, filesystem
read, stat, list, or validation was performed after reactivation and before
launch.

## Plain launch delivery

Fresh delivery directory, separate from the formal root:

`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-formal-launch-f2f5a9468f90-20260804T214000Z`

- mode: `0700`;
- device/inode: `16777244/3112915`;
- create count: `1`;
- reuse/repair/alternate: `0/0/0`.

Human-readable script:

`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-formal-launch-f2f5a9468f90-20260804T214000Z/launch.zsh`

- created once using `apply_patch`;
- bytes: `602`;
- SHA-256:
  `cd612d11f2e5d4843d08848cf2560b9c5ae82522b7bf352795d985c76073acb1`;
- mode: `0700`;
- device/inode: `16777244/3112920`;
- `/bin/zsh -n`: pass;
- Base64/encoded payload/eval/dynamic decoded source: `0`;
- semantic-controller logic: `0`;
- content: exact PLAN section 5 payload only.

## Visible Terminal launch

- Launch UTC: `2026-08-04T22:32:17Z`.
- Launch epoch: `1785882737`.
- AppleScript invocations: `1`.
- `do script` calls: `1`.
- Exact command:
  `/bin/zsh '/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-formal-launch-f2f5a9468f90-20260804T214000Z/launch.zsh'`.
- AppleScript front window id: `478`.
- Returned-tab TTY: `/dev/ttys010`.
- Front selected-tab TTY: `/dev/ttys002`.
- Readback mismatch: true; no retry or second AppleScript was attempted.
- Long-task owner binding uses the returned-tab TTY `/dev/ttys010`, not the
  different front selected tab.

The Terminal script performed the only atomic `mkdir -m 700` for the formal
root, then `exec`-replaced itself with the tracked wrapper. Package access was
left exclusively to the launched production chain. The Executer did not read
the package before, during, or after that chain.

## First sparse status check and terminal transition

At the first allowed status check, approximately t+42 seconds, canonical
parent-side wrapper state was already terminal:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r6-ac6145829dcf-20260804T214000Z.wrapper-state.json`

- check timestamp epoch: `1785882779`;
- bytes: `378`;
- SHA-256:
  `0c650f0eeb14a92d608cc2bb008efb8f01e65f65b254a44667e249d5a49e9559`;
- mode: `0600`;
- device/inode: `16777244/3112947`;
- status: `finished`;
- started at: `2026-08-04T22:32:18Z`;
- wrapper PID: `47221`, exited;
- child PID: `47238`, exited;
- wrapper/child exit: `1/1`;
- shell cleanup exit: `1`;
- signal: `null`.

Because the attempt was terminal at check 1, t+90 and t+180 checks were not
performed. No automation was requested or created. Liveness check counts are
`terminal=1`, `running=0`.

## Fresh formal root and exact failure inventory

Formal root:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r6-ac6145829dcf-20260804T214000Z`

- directory mode: `0700`;
- device/inode: `16777244/3112932`;
- root create: `1`;
- reuse/repair/resume/alternate: `0/0/0/0`;
- exact direct inventory: `9` regular files;
- directories, symlinks, special files, unbound extras: `0`.

| Artifact | Bytes | SHA-256 | Mode | Device/inode |
|---|---:|---|---:|---|
| `all-off-shell.exit-status.txt` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | `0600` | `16777244/3112941` |
| `all-off-shell.json` | 486 | `c86683cccba1c87457c2fe5e9f9e1b92c2bae119bf6710e0c3d04759de19dcfb` | `0600` | `16777244/3112938` |
| `all-off-shell.stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `0600` | `16777244/3112939` |
| `child-exit-status.txt` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | `0600` | `16777244/3112937` |
| `independent-final-zero.json` | 1061 | `afaf3050d6c8933b9a95da342e38117598d8a76bd748321572a053b7f618c726` | `0600` | `16777244/3112942` |
| `returned-summary.json` | 805 | `9e4211427cffa272f652b050d80de490628b3a3f3fe2b8ef132c0360856c3a1b` | `0600` | `16777244/3112943` |
| `terminal-audit.json` | 2026 | `66ba345f8f76cda181066561a90660620f65184c6a83420902b8e280ab8347c8` | `0600` | `16777244/3112944` |
| `terminal-seal.json` | 2125 | `ac329054306da9e99b302b564d899a5504809781ceafb3db6ad9aa4fb2b36dcd` | `0600` | `16777244/3112945` |
| `wrapper-result.json` | 382 | `81710bc635031aa330a1f8bde31f3a5d9905ee8f215a93d9455e12628f0d8598` | `0600` | `16777244/3112946` |

## Terminal audit, capture cutoff and cleanup

Terminal audit/seal evidence:

- terminal audit schema: `p7_td_b_r6_terminal_audit_v1`;
- terminal seal schema: `p7_td_b_r6_terminal_seal_v1`;
- terminal seal status: `FAIL`;
- terminal disposition: `accepted_hard_failed_formal_attempt`;
- failed phase: `terminal_replay`;
- error code: `file_lstat_failed`;
- formal pass: false;
- production launch: `1`;
- retry/alternate root: `0/0`;
- formal/setup/ambient/physical capture counts: `0/0/0/0`;
- strip nonzero call count: `0`;
- analysis call count: `0`;
- returned-summary status: `partial_or_invalid`;
- capture order exact: false because the accepted capture set is empty;
- first-fail cutoff: before slot `000-ray-a0-t600`;
- seventeenth capture: `0`.

Production-chain accounting:

- current formal launch: `1`;
- current child start: `1`;
- current production-loader budget consumed: `1`;
- current production loader returned an accepted binding: not evidenced before
  the terminal failure;
- second production-loader/package read: `0`;
- external semantic controller: `0`.

Cleanup evidence:

- Python cleanup: `unknown` in terminal seal;
- shell all-off invocation: `1`, exit `1`;
- shell all-off strip result: PASS, all five RGBWW channels zero;
- shell all-off Ray result: FAIL, connection refused;
- independent final-zero invocation: `1`, status `fail`, exit `1`;
- independent final-zero strip result: PASS, baseline and device snapshots all
  five channels zero;
- independent final-zero Ray result: FAIL, connection refused;
- Ray nonzero calls recorded by independent final-zero: `0`;
- strip nonzero calls recorded by independent final-zero: `0`.

Safety-only follow-up after proving PIDs exited:

```text
/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json
```

- invocation count: `1`;
- exit: `1`;
- wall time: `5.171756875s`;
- strip result: PASS, all five channels zero;
- Ray result: FAIL,
  `ConnectionRefusedError: [Errno 61] Connection refused`;
- capture/retry/root mutation: `0/0/0`;
- additional cleanup calls after this failure: `0`.

No credible Ray intensity-zero readback exists. The repository evidence proves
strip zero only.

## Cumulative ledger and hard locks

Pre-run ledger retained without reset:

- remint prepare/describe: `1/1`;
- prior strict standalone describe: `1`, exit `1`;
- prior formal attempt / production loader / formal root create: `0/0/0`;
- `package_integrity_failure_claimed=false`;
- `route_a_failure_claimed=false`.

This run adds:

- formal attempt / formal launch / formal root create: `1/1/1`;
- production owner child / production-loader budget: `1/1`;
- logical/physical captures: `0/0`;
- retry/repair/resume/alternate/second launch: `0/0/0/0/0`;
- second package read/remint/prepare/describe/replay: `0/0/0/0/0/0`.

Hard locks:

- `return_anchor_history=not_evaluated`;
- `g4_07_analyzer_call_count=0`;
- release consumption / retained R3 / old-root payload access: `0/0/0`;
- strip nonzero/formal: `0/0`;
- combined TD-B / TD-C: `0/0`;
- firmware/flash/deployment: `0/0/0`;
- Git stage/commit/push/PR: `0/0/0/0`;
- PLAN/FULL/source/test/config/GUIDE writes: `0`.

Only this live `.agent-work/EXECUTION_RESULT.md` was written in the repository.
The hard-failed formal result has not received Planner acceptance and does not
unlock G4-07 or any later stage.
