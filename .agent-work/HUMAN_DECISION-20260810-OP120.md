# Human decision — operational state-to-capture dwell 120 s

On 2026-08-10, Human changed the current Ray history experiment and future
similar color/state-to-capture waits from 600 seconds to 120 seconds to reduce
elapsed time and power consumption. Human explicitly accepts the additional
thermal error introduced by the shorter operational dwell.

This decision applies only to new acquisitions. Retained R6 and the interrupted
600-second 3x3 root remain historical evidence with their original timing and
must not be pooled into the new 120-second fit.

The decision does not claim settling or steady state and does not alter the
frozen observer, 58 features, uncertainty, covariance, guarded coverage,
exposure, frame selection, cyclic orders, session count, cleanup, or the
existing 3600-second between-session cold proxy.

Canonical machine-readable record:
`config/hsi/p7-human-dwell-policy-v1.json`.

Subsequent Human decision `HUMAN_DECISION-20260810-COLD600.md` supersedes this
record's 3600-second between-session cold proxy for new acquisitions. The 120
second operational dwell decision remains in force.

Interrupted historical root:
`/Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-20260810-015022`.

- Session 1 completed 7/7 under the superseded 600-second contract.
- Session 2 was intentionally stopped after 2/7; wrapper received TERM and
  shell cleanup exited 0.
- Independent post-stop all-off confirmed strip five-channel zero and Ray
  intensity zero.
- None of these frames is eligible for the new 120-second analysis.
