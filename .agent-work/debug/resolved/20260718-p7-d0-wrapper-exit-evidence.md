# P7-D0 wrapper exit evidence

## Frozen scope

- Offline-only P7-D0 wrapper repair under PLAN section 3.12; no device, network, `.env`, all-off, or module `--execute` calls.
- Preserve the five-step raw-PWM sequence and all device/solver contracts.
- Required evidence: atomic child, shell cleanup, signal, and final wrapper exit artifacts with cleanup exactly once.

## Confirmed root cause

- The production wrapper ended with direct `wait "$child_pid"` under `set -e`, so a nonzero child could terminate the shell before exit evidence was written.
- Shell cleanup used `2>&1 || true`, merging stderr into JSON and erasing the cleanup exit code.
- The old regression test asserted only cleanup-once and broadly zero/nonzero wrapper status; it did not reconstruct any frozen exit-code contract.

## Regression evidence

- The original wrapper test passed before repair, demonstrating the audit blind spot.
- The replacement six-case fake test initially exposed two zsh-specific implementation errors: local `path` overwrote zsh's tied `$path`/`$PATH`, and local `status` collided with zsh's read-only `$status`.
- Renaming those locals to `target_path` and `result_status` produced a passing focused six-case test.

## Verification

- Focused D0/device/all-off tests: `17/17` pass.
- Full suite: `432/432` pass in `168.035s`.
- Compileall, five relevant wrapper syntax checks, diff check, and CodeGraph sync pass.
- Module dry-run writes five frozen steps with maximum raw PWM `48`, `curve_path=null`, and `device_calls_performed=false`.
- No wrapper or module execute path, device, network, `.env`, or all-off call was used.
