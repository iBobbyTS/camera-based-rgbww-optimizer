# P7-R1 Terminal ownership and remote aperture closure

## Resolved failures

- A wrapper started from the Codex shell remained in that shell's process group and disappeared before any command or capture. Independent recovery proved strip generation `13 → 14`, five channels zero, and Ray intensity zero.
- An oversized AppleScript inline command was truncated before execution. Replacing it with the short `tmp/launch-hsi-reference-repeatability-terminal.zsh` entrypoint made Terminal own the launcher, wrapper, PGID, and TTY.
- The first Terminal-owned formal run failed at zero CR3 because P7-R1 inherited local aperture `4` while the remote camera exposed only `implicit auto`. Passing `iso=None, aperture=None` to the shared remote capture builder fixed the producer boundary.

## Verification

- Terminal shell, wrapper, and child were independently visible on `ttys004` with a Terminal-owned process group.
- The remote-setting regression, R1 wrapper tests, and related camera/RAW tests passed `59/59`; the full suite passed `434/434`.
- The fresh retry completed all 82 logical captures and both cleanup layers. No further launcher or remote-aperture failure occurred.

The failed zero-capture directories remain immutable evidence and were not spliced into the successful run.
