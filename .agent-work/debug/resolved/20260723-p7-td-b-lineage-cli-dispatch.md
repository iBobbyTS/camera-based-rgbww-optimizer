# P7 TD-B Lineage CLI Dispatch

## 状态

`resolved_offline_waiting_for_planner`: CLI dispatch regression is fixed and verified; production formal was not retried.

## 已确认证据

- Lineage release validation and E2 passed at checkpoint `3db7ae25efab74cc800d87ac0a97aead0990ecc1`.
- The exact Ray formal wrapper was invoked at:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-20260723-172000`.
- Runner failed before backend construction, command application, or camera capture with:
  `PermissionError: TD-B execute plan is locked until TD-A passes`.
- The failure came from `main()` building an unresolved execution plan before dispatching the supplied setup release.
- Retained physical CR3 and camera capture counts are zero.
- Python/outer shell cleanup both exited zero; Ray and strip were independently set/read as off in the E2 run and wrapper cleanup.

## 根因假设

When `--setup-release` is present, the release is the authoritative resolved-plan owner. The CLI must not enforce the unresolved TD-B prerequisite gate for the unused generic plan before calling `run_resolved_td_b_formal`.

## 下一步

Commit `b38caa4` dispatches the exact setup release before constructing an unresolved plan. Focused `64/64`, full `545/545`, compileall, wrapper syntax, diff-check, and CodeGraph passed. Regenerate a lineage release at the new checkpoint only after Planner accepts the failed run and offline repair; do not reuse the old release or automatically retry hardware.
