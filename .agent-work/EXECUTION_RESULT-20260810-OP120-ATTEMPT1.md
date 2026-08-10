# OP120 attempt 1 — engineering-invalid chronology rejection

## Outcome

```text
science_delta = none
attempt = engineering_invalid
human_gate = false
advisor_gate = false
retry_after_substantive_fix = allowed
```

Attempt root:

`/Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-20260810-053413`

Session 1 completed four accepted captures and returned a fifth physical CR3.
The fifth capture, `004-s1-ray-a_after_b-t120`, was rejected before acceptance
because the runner compared its independent 120-second A dwell with an earlier A
visit and required the observed elapsed values to be globally increasing.

The retained fifth return passed sidecar association and Tier-B timing validation.
Its observed dwell was 126.90717891405802 seconds. The root stopped before Session
2 or Session 3. It remains immutable failed evidence and is not eligible for the
21-frame fit or pooling into another attempt.

## Safety closure

- Python cleanup: pass
- shell cleanup: pass
- independent all-off: pass
- strip five-channel zero: confirmed
- Ray intensity zero: confirmed
- residual experiment process: none
- acquisition checkpoint Git state: clean at `0ee42788b94f0ce3e70daae11edc7b17d6389941`

## Substantive correction

Observed chronology is now scoped to one contiguous `_ledger_groups()` command
occurrence. Independent repeated A visits no longer share a chronology accumulator;
real multi-timepoint points under one uninterrupted state still require strictly
increasing observed elapsed values.

Regression evidence:

```text
tests.test_p7_direct_r6
Ran 16 tests in 0.409s
OK
```

The next attempt must use a new root from Session 1 with zero pooled frames. The
run-level `retry=0` contract remains unchanged: there is no hidden reacquisition,
补拍, or overwrite within an attempt.
