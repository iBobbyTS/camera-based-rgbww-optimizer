# F19-C9 governance lineage successor precommit validation-order failure — Planner review archive

**Review time:** `2026-07-29T23:57:46-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-9-GOVERNANCE-LINEAGE`

**Decision:** `REJECTED_FORMAL_COMPILEALL_CONSUMED_BEFORE_IMPLEMENTATION_COMMIT`

## Reviewed scope and method

C9 was authorized to create an exact subordinate governance-provenance manifest and validator, commit exactly three
implementation paths once, verify that implementation commit, then run the six-step fail-fast validation chain once
in a fresh evidence root. The chain's first command was explicitly postcommit compileall of both the production source
and its dedicated test module.

The Planner read AGENTS, the project skill, active PLAN, the C9 section of FULL, the appended C9 ER record, terminal
evidence and current Git/source/config/test state. It did not run tests, compileall, CodeGraph or any Git/controller
validation command; it did not read candidate, retained R3, release, network, environment, devices, camera, Ray,
strip, cleanup, formal or public-analyzer state. The source diff and ignored config file were inspected only to freeze
their current bytes and disposition; their behavior was not accepted.

## Accepted activation and terminal lifecycle facts

- Activation is exact: `bc13f50dfab9c2724d883befb2988f11548ccbe6` has direct parent
  `d12b0cec3b66afbf26eedadf34a938222b488a88`, exact subject
  `chore(plan): activate f19 governance lineage successor correction`, and changed path exactly
  `.agent-work/PLAN.md`.
- Fresh root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/20260730T001500Z`
  is mode `0700` and is permanently consumed by this failed attempt.
- Terminal evidence is regular, non-symlink, mode `0600`, 2030 bytes, SHA-256
  `b5cb63fdbe9f51c22f582616eb7494b845ca55122575da415a96a501a4da5847`.
- There was no stage or implementation commit. The test file remained byte-exact to activation baseline.
- After the failure, no test, focused suite, full suite, CodeGraph sync or diff-check command ran, and retry/fallback
  remained zero.
- Candidate, retained R3, canonical retained validator, eligibility, release, network, `.env`, device, camera, Ray,
  strip, cleanup, formal, public analyzer, TD-C, sentinel and P8 counters remained zero. Retained R3 remains
  `RETAINED_UNVALIDATED_UNCONSUMED`.

## Rejection basis

The only compileall invocation occurred during precommit development:

```text
.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
```

This violates two exact C9 conditions:

1. PLAN section 6 permits the formal validation chain only after the exact implementation commit has been created
   and its topology verified;
2. the frozen compileall argv includes both
   `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` and
   `tests/test_p7_thermal_diagnostics.py`, but the consumed invocation omitted the test path.

Because each validation item had budget one and retry/fallback were zero, the command could not be rerun under C9.
The later validations correctly remained at zero. A successful precommit syntax check cannot substitute for the
required postcommit command and does not validate the uncommitted implementation.

## Preserved but unaccepted draft baseline

The following bytes are preserved solely to avoid losing work and to give the Orchestrator an exact dirty-worktree
classification. They are not accepted as correct, complete, tested or eligible:

- ignored/untracked `config/hsi/p7-governance-lineage-successor-v1.json`: 2574 bytes, Git blob
  `46acad9b1992196cbcdb381718ea9b2dfda31e3b`, SHA-256
  `7ff96378e76c5b450c44db55d5b5eee922afe084bb0ea37d837a6f12db928795`;
- modified `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`: 191641 bytes, working Git
  blob `6d274d59b60dcd38b26cb14d092bb7cd31d30d2e`, SHA-256
  `7030305c1a4b5e829fc8966880e80139a9e2a345453e7cf2766651c0039525f1`;
- unchanged `tests/test_p7_thermal_diagnostics.py`: 194978 bytes, committed Git blob
  `16e91ee1e1fac64062c511b96f2f320b7ee6c806`, SHA-256
  `7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a`.

The source draft contains 302 inserted and 6 removed lines relative to the activation baseline. No test was added,
so no production semantics or negative matrix can be accepted. The config draft is intentionally ignored by the
repository's broad `config/hsi/*` rule and therefore requires an explicit exact-path force-add if the Orchestrator
preserves it in Git; that force-add must not widen to any other ignored config.

## Decision and exact next branch

C9 is rejected. Its evidence and formal validation budget cannot be reused. The next branch is
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10` with a two-step ownership boundary:

1. Orchestrator personally preserves the exact current source/config draft bytes in one focused, explicitly
   unvalidated two-path commit, then updates FULL and commits the C9 review/ER/PLAN/FULL governance state. It must
   not include the unchanged test, any other ignored config or any unrelated path. No test or validation command is
   part of this preservation step.
2. A fresh Planner pass freezes a clean C10 executable package from that preserved baseline. C10 must add the
   dedicated tests in a new exact implementation successor commit, permit production/config correction only if the
   Planner freezes those exact paths and before-identities, and run the complete formal validation chain exactly once
   in a brand-new root. No C9 artifact, log, invocation result or root may count toward C10.

The old policy/workflow/public-default payloads and canonical eligibility owner remain unchanged. This is an
engineering provenance correction, not a scientific branch or high-risk device operation; Advisor and Human
authorization are not required.

**Planner stop:** `F19_CORRECTIVE_9_REVIEWED_WAITING_ORCHESTRATOR_C10_BASELINE_PRESERVATION`.
