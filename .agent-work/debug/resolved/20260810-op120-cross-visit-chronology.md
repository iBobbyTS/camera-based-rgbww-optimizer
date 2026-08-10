# OP120 cross-visit chronology false rejection

## Confirmed failure

- Root: `/Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-20260810-053413`
- Session 1 accepted 4/7 captures and retained a fifth physical CR3.
- Capture `004-s1-ray-a_after_b-t120` was rejected with
  `non-increasing observed chronology` although its Tier-B observed dwell was
  finite, non-negative, and 126.90717891405802 seconds for a requested 120-second
  dwell.
- Python cleanup, shell cleanup, independent all-off, strip zero, and Ray zero
  passed. No Session 2 or 3 was started.

## Root cause

`execute_plan()` stored the last observed elapsed time by
`timing_sequence_identity`. Repeated A anchors share that scientific identity even
though `_ledger_groups()` executes each A visit as a separate command/readback and
starts a new dwell clock. Equal requested dwell visits may therefore have valid,
non-monotonic observed values across visits.

The strict observed-chronology check belongs to one contiguous ledger group only,
where requested elapsed points increase under one uninterrupted command. It must
not compare separate state visits.

## Verified fix

The chronology accumulator is now keyed by the current contiguous ledger-group
occurrence rather than the scientific state identity.

Regression coverage proves:

1. A Ray-history session with separate 120-second A visits and non-monotonic
   observed dwell across visits passes.
2. A true multi-timepoint group with non-increasing observed dwell inside the same
   uninterrupted command still fails.
3. Tier, provenance, finite/non-negative timing, physical-return, quality, and
   cleanup checks remain unchanged.

Verification:

```text
.venv/bin/python -m unittest tests.test_p7_direct_r6
Ran 16 tests
OK

.venv/bin/python -m compileall -q src tests
exit 0

git diff --check
exit 0

codegraph sync
Already up to date
```

The failed root remains immutable. A corrected attempt must start from a new root,
Session 1, with no pooled frames.
