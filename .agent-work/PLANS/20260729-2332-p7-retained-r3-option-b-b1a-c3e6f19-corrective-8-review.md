# F19-C8 validation log single-owner 与 full-suite lineage drift — Planner review archive

**Review time:** `2026-07-29T23:32:22-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER`

**Decision:** `REJECTED_FULL_SUITE_AMBIENT_GOVERNANCE_LINEAGE_DRIFT`

## Reviewed scope and method

C8 was authorized to preserve the accepted C7 pre-gates and committed F19 controller/helper/test bytes, use a fresh
root, give every validation log one exclusive-open file descriptor, run the exact fail-fast validation chain once, and
emit a terminal seal plus one ER record that supersedes the C7 dedicated-test SHA error.

The Planner read AGENTS, active PLAN/FULL, the C8 ER record, the C8 terminal, all started C8 artifacts and
`full_unittest.log`. It used current committed source and Git history only to classify the ten full-suite failures. It
did not read C8-unstarted artifacts, C2-C7 payloads, retained R3, candidate, release, network, devices, camera, Ray,
strip, cleanup, formal or public analyzer, and it did not rerun any test or validation command.

## Evidence lifecycle acceptance

- Activation lineage is exact: child `70f1b17990e12522ee876e1d99abdadf1addd6a2`, direct parent
  `2d817465dbd0974d2cc455f7b99be79f1e62bab4`, subject
  `chore(plan): activate f19 validation log owner correction`, changed path exactly `.agent-work/PLAN.md`, and the
  pre-execution worktree was clean.
- Fresh root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-8-offline` is mode `0700`.
  All seven started artifacts are regular, non-symlink and mode `0600`.
- The four started validation logs each have exactly one exclusive open with
  `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`; stdout and stderr share that descriptor; reopen, second-fd and shell
  redirection counts are all zero; fsync/close use the same descriptor and digest occurs after close.
- `compileall.log`: 0 bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `targeted_unittest.log`: 2155 bytes, SHA-256
  `883169f30a676e58dd60c726a346afa573cf9f76b31297b51fcf45d9ba1d82c0`.
- `focused_unittest.log`: 8049 bytes, SHA-256
  `8b6b045b2ad742de31ef781ec1ce3054ed38ee23812d03c8cc5316fe3e61ba68`.
- `full_unittest.log`: 150463 bytes, SHA-256
  `289bb7275acfd7e3d4016cdff767999c53ef1b62565999a0e00bde5e087e9c2e`.
- Terminal is strict JSON, sealed last, 11518 bytes, SHA-256
  `0556b76ea31bd747e169190c93723b7431807fd63a74792725fc5f55c27cbb43`, mode `0600`.
- Fail-fast is correct: CodeGraph sync and `git diff --check` were never started and their log paths are absent;
  retry/fallback are `0`.
- Before the ER append, repository changed paths were empty. Controller/helper/dedicated-test edit counts are zero;
  after the run, the only worktree change is `.agent-work/EXECUTION_RESULT.md`.

## Validation result

- compileall: exit `0`, invocation `1`.
- targeted unittest: `11/11`, exit `0`, invocation `1`.
- focused unittest: `43/43`, exit `0`, invocation `1`.
- full unittest: `684` tests in `124.790s`, exit `1`, with exactly `failures=1, errors=9`.
- CodeGraph sync and diff check: invocation `0` because full unittest stopped the fail-fast chain.

All ten failures are in `tests/test_p7_thermal_diagnostics.py` and share two deterministic lineage guards:

1. one error raises `TD-B AGENTS current bytes differ` because the frozen
   `TD_B_AGENTS_CURRENT_SHA256=a035e695...c8a5` no longer equals current committed `AGENTS.md`
   SHA-256 `604b10be...07a0`;
2. eight errors and one assertion failure are pre-empted by
   `TD-B public-default successor hash or diff differs: .agents/skills/camera-based-rgbww-optimizer/SKILL.md`.
   The frozen e7ccdda skill bytes are SHA-256 `c8dd57a2...9607`, while current committed bytes are
   `3a77c8a0...81e`.

The assertion failure expected a later `owner differs` error, but the earlier skill-lineage guard fails first. There
are no fixture setup errors, import errors, missing dependencies, test-discovery errors or malformed command errors.

## Root-cause classification

This is `REPOSITORY_AMBIENT_KNOWN_GOVERNANCE_LINEAGE_DRIFT`, not an F19 regression:

- commit `3e2ebed chore(orch): consolidate p7 evidence and workflow state` changed exactly the relevant governance
  semantics in `AGENTS.md` and `.agents/skills/camera-based-rgbww-optimizer/SKILL.md` after their older exact lineage
  freezes;
- that commit did not touch the F19 controller, machine-contract helper or dedicated test;
- current F19 identities remain byte-exact: controller
  `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`, helper
  `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`, and dedicated test
  `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`;
- the exact F19 targeted suite and the wider focused lineage/controller suite are green.

The focused greens show the F19 change is locally sound, but they cannot override the mandatory full-suite failure.
C8 therefore cannot be accepted as a completed validation chain.

## C7 supersession and locks

C8 terminal and ER agree on the C7 supersession: old ER value
`48b0cb295538481998a79896db4fc53d8e4fa12f807a04b67620e54946eb2c38` is superseded by authoritative terminal and
committed-test value `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`; C7 terminal identity is preserved as
3977 bytes, SHA-256 `85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369`, mode `0600`, with no old-record rewrite.

All candidate/R3/validator/eligibility/manifest/release/network/environment/device/camera/Ray/strip/cleanup/formal/
public-analyzer/TD-C/sentinel/P8 counters remain `0`. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

## Decision and next branch

C8's evidence lifecycle, supersession record, committed F19 bytes and local test results are accepted as immutable
prerequisites, but C8 overall is rejected because the required full suite is nonzero.

The next branch must be an Orchestrator-aligned, bounded engineering provenance correction for the two legitimate
post-freeze governance-file changes. It must preserve the historical AGENTS policy freeze and e7ccdda public-default
successor evidence instead of rewriting old payloads, add an exact successor/current-owner layer for the authorized
`3e2ebed` governance changes, and then run a fresh validation chain. Exact repository/artifact scope and Git topology
are Orchestrator-owned and must be frozen before any Executer dispatch.

No scientific interpretation is involved and no device operation is requested, so neither Advisor guidance nor Human
high-risk authorization is required.

**Planner stop:** `F19_CORRECTIVE_8_REVIEWED_WAITING_ORCHESTRATOR_C9_PROVENANCE_ALIGNMENT`.
