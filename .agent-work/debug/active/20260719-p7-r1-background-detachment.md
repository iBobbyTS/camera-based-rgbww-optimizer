# P7-R1 background detachment failure

## Observed branch

- D0 completed successfully at checkpoint `e8c6af203c0292cebe8d6a9d004824cba7d7f0b7` before the R1 attempt.
- R1 preflight passed and independently confirmed strip zero plus Ray intensity zero before and after its read-only checks.
- The formal wrapper wrote a valid adjacent running state with wrapper PID `48221` and child PID `48228`; the child wrote the exact authorized `plan.json` and a `run.json` with all counters zero.
- Both processes disappeared when the Codex terminal command ended. The run remained `running`; no `commands.jsonl`, `captures.jsonl`, CR3, Python cleanup, shell cleanup, wrapper result, or failure artifact was produced.
- The first launcher PID `45774` died before entering the wrapper and is retained separately; it created no run directory and performed no experiment call.

## Evidence-backed cause

- The retry wrapper was still in process group `48066`, owned by the launching Codex terminal command. `nohup` protected only against hangup; it did not detach the wrapper from the terminal executor's process-group cleanup.
- The absence of wrapper signal/finalization artifacts shows the process was removed outside the wrapper's handled INT/TERM/HUP path.
- This is a launch-ownership failure, not a measurement, camera, readback, scope, or physical-budget failure. Nevertheless the PLAN explicitly requires fail-closed handling when a process disappears while `run.json` remains running.

## Safety recovery

- No formal command or capture occurred: logical/formal/physical counts are `0/0/0`, with no commands, captures, or CR3.
- Independent recovery `all_off` succeeded for ESPHome and Ray.
- A generation-bearing verified strip-zero transition advanced generation `13 → 14` with the stable `bedroom-rgbww-strip` / `E0:8C:FE:63:C9:40` identity and all five channels zero.
- Independent Ray CCT readback reported intensity `0`.
- The failed run is retained intact at `/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/p7-r1-20260719-062500` and must not be spliced or resumed.

## Decision needed

Planner must decide whether the zero-command/zero-capture launch-ownership failure consumed the one complete R1 acquisition authorization. If a new run is authorized, use an OS-owned launch mechanism such as a dedicated Terminal or `launchctl` service and prove a different session/process-group owner before the five-minute health check. Do not reuse the failed run directory.

## Resumed Terminal launch pass

- The resumed goal explicitly permits launching through macOS Terminal so Codex shell lifecycle management does not own the experiment process.
- The first AppleScript `do script` attempt embedded the entire preflight and wrapper command. Terminal received only a truncated prefix ending at `camera...`, remained at a shell continuation prompt, and created no preflight/run artifact. No device command executed.
- Root cause appears to be the oversized inline Terminal command boundary, not Terminal process ownership.
- The minimal correction is `tmp/launch-hsi-reference-repeatability-terminal.zsh`: Terminal receives only one short absolute script path; the script records Terminal-shell/launcher PID, PGID and TTY, runs the frozen read-only/off preflight, and then `exec`s the already-tested formal wrapper. Preflight failure has its own independent all-off trap; after successful handoff, the formal wrapper remains the sole experiment cleanup owner.

## Terminal-owned run reached the formal runner

- The short launcher succeeded: Terminal shell PID `48758` on `ttys003` owned wrapper PID `48898` in a distinct PGID, and child PID `49142` was not tied to a Codex command process group.
- Preflight passed with a clean checkout, both all-off responses successful, remote health/config readable, and Ray HSI/CCT intensity zero.
- The formal run failed before its first ambient CR3 because `run_targeted_reference_repeatability()` inherited local-camera defaults `iso="100"` and `aperture="4"`, while the current remote config exposes aperture choices only `Unknown value 0c00` and `implicit auto`.
- Evidence is zero high output and zero physical capture: run counters are `0/0/0`, the two command rows are both-off, no CR3 exists, and Python plus shell cleanup both succeeded. Wrapper exit correctly retained child `1`, cleanup `0`, wrapper `1`.
- The shared remote capture path already defines the correct convention: callers pass `iso=None, aperture=None` so `RemoteCameraBackend.resolve_capture_settings()` resolves the current remote values. P7-R1 alone omitted those two arguments.
- Minimal fix: pass `iso=None, aperture=None` from the P7-R1 runtime and add a regression asserting the remote runtime delegates those values to the shared capture builder. No exposure, capture-budget, source, or measurement contract changes.
