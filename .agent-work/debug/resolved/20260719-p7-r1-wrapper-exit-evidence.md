# P7-R1 long-task wrapper exit evidence

## Frozen scope

- Offline-only local hardening of `tmp/run-hsi-reference-repeatability.zsh` under PLAN section 4.4.1.
- Preserve the exact R1 measurement, policy, solver, capture, source, and high-output budgets.
- Do not access `.env`, network, ESPHome, Ray, camera, `all_off`, or any execute path during this repair.

## Confirmed root cause

- Direct `wait` under `set -e` could skip retained exit evidence when the child failed.
- Cleanup stderr was merged into its JSON output and `|| true` discarded the cleanup exit code.
- INT, TERM, and HUP all collapsed to `128`, so the wrapper could not prove which signal ended the run.
- The previous test checked only broad cleanup behavior and did not reconstruct PID, path, three-layer exit, atomic-write, or no-secret contracts.

## Implemented boundary

- The wrapper keeps its long-task ownership local; no cross-wrapper framework was introduced.
- Adjacent atomic state records the experiment, absolute run directory, wrapper/child PIDs, runner/wrapper logs, UTC start, and running/finished status without violating the runner's empty-directory precondition.
- Run-owned artifacts separately retain child exit, shell-cleanup JSON/stderr/exit, received signal, and final wrapper result.
- Final exit priority is signal `128+n`, then child failure, then cleanup-only `70`, then success; signal forwarding waits for Python finally before shell cleanup.
- EXIT/INT/TERM/HUP all converge on cleanup exactly once.

## Verification

- Six fake-only paths pass: success, child exit 7, cleanup exit 9 mapped to 70, SIGINT 130, SIGTERM 143, and SIGHUP 129.
- Focused D0/R1/device/all-off tests: `36/36` pass in `20.544s`.
- Full suite: `432/432` pass in `146.058s`.
- `compileall src tests`, five P6/P7 wrapper syntax checks, `git diff --check`, and `codegraph sync` pass.
- Exact authorized R1 dry-run at `tmp/hsi-reference-repeatability-offline/executor-authorized-scope-20260719-001154-dry` reconstructs 82 logical captures, 30 Ray, 50 strip, two ambient, physical cap 250, five frozen strip commands, three Ray states, all frozen input hashes, and zero device/network/environment calls.
- No real device, network, `.env`, `all_off`, camera, Ray, or execute call occurred.
