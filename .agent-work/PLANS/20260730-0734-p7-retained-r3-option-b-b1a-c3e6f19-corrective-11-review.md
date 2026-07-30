# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11 Planner review

**Review date:** `2026-07-30`

**Verdict:** `REJECTED_TARGETED_AMBIENT_FULL_SET_EXPECTATION_ONLY`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-11-HISTORICAL-CHECKPOINT-SEAM`

## Reviewed scope and authoritative evidence

- Activation commit: `c0c51d9bc340da40ab5e95027e999962d2bd723e`, parent
  `2226624b0b3437de4f6c510d460ced7f4553c6c1`, subject
  `chore(plan): activate f19 historical checkpoint correction`, exact changed path
  `.agent-work/PLAN.md`.
- Implementation commit: `ba816216af9d37397873e054f44dbb7eea0f9b10`, parent
  `c0c51d9bc340da40ab5e95027e999962d2bd723e`, subject
  `fix(p7): separate historical lineage checkpoint ownership`.
- Implementation exact changed paths:
  `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` and
  `tests/test_p7_thermal_diagnostics.py`; additional paths `0`.
- Canonical implementation binary patch SHA-256:
  `b3e51862bd4ab11e07da7448a931bebabfa0bdf6d13bd69f1ba0f5d7cf5c3088`.
- Committed source SHA-256:
  `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`.
- Committed test SHA-256:
  `9c6c721ebb5cb24b9aff79d36d4853b1935a55e0dfb38b32e64afcbad1b7d7ff`.
- Immutable config SHA-256 remained
  `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`.
- Fresh root:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-11-offline/20260730T081500Z`, mode `0700`.
- Terminal evidence:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-11-offline/20260730T081500Z/terminal-evidence.json`,
  bytes `7115`, mode `0600`, SHA-256
  `43fbf748d847b434f4661933c113b21a84f1f20d10d8415c28e096149686953a`.
- Precommit freeze: bytes `1227`, SHA-256
  `6cb3e2d87d642a9c3202d9d8ab82b845999cb4b5b4d1b696170208b1fcc8be60`.
- Postcommit topology: bytes `1842`, SHA-256
  `f0a4bdcf001b43c369d6a76a9db56bc3a91cb93ac51f4100f9a62b6ccf5328cb`.
- Targeted log: bytes `5512`, mode `0600`, SHA-256
  `5af2ab0eb70a0547f6a509572b69ad1578fc664741a4ffdd01dcf0f85a70c75a`.

The sealed terminal and the artifact files are authoritative. The C11 append in
`EXECUTION_RESULT.md` manually records precommit, postcommit and targeted bytes as `1073`, `1895`
and `5427`; those three byte counts are superseded by the terminal/artifact values above. Their
paths and SHA-256 values are correct. No old evidence or ER bytes may be rewritten.

Planner ran no tests, compile, CodeGraph, Git mutation, candidate, retained-R3, release, network,
environment, device, camera, Ray, strip, cleanup, formal or public-analyzer operation.

## Validation quality and findings

Activation and implementation topology, exact two-path scope, immutable config, sealed artifacts,
fail-fast and zero locks are internally consistent. Compileall ran once and exited `0`. Targeted
unittest ran the exact `13` selectors once: `12` passed, `1` failed, errors `0`. Retry and fallback
were `0`; focused, full discovery, CodeGraph and diff checks correctly remained at `0`.

The successful selectors establish the intended production correction within targeted scope:

- historical qualification checkpoint validation uses checkpoint bytes and performs zero ambient
  working-governance-owner reads and zero subordinate governance calls;
- current HEAD validates the legacy payload first, calls the governance subordinate exactly once,
  and fails closed on working governance drift;
- the existing canonical candidate builder remains the sole eligibility owner;
- both dedicated governance-successor tests and the other historical/current lineage regressions
  remain green.

The sole failure is a Planner contract error in
`test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`. The test correctly removed the
ambient path-count snapshot and verifies one-to-one paths plus canonical classifications, but then
incorrectly requires the full ambient changed-path candidate to have status
`eligible_waiting_for_planner` and `prohibited_paths=[]`. The canonical builder truthfully returns
`ineligible_requires_new_setup` because that full ambient set contains unclassified/prohibited
paths. Changing production to satisfy this assertion would weaken the canonical eligibility owner
and is forbidden.

## Decision and retained implementation disposition

C11 as a whole is rejected because the required targeted gate is nonzero and the later validation
chain did not run. Nevertheless, production source commit `ba816216af9d37397873e054f44dbb7eea0f9b10`
is accepted as `retained_historical_checkpoint_seam_v1_pending_test_only_validation`. Its source
bytes must remain unchanged in the next package. This does not make the retained R3, a release, or
any candidate eligible or consumable.

The only next modification path is `tests/test_p7_thermal_diagnostics.py`. Its corrected regression
must separately prove:

1. the canonical accepted subset is `eligible_waiting_for_planner` with no prohibited paths;
2. the full ambient changed set is returned one-to-one, sorted and unique, with each classification
   exactly equal to the canonical owner;
3. accepted and prohibited classifications are represented truthfully, and the full-set status is
   `ineligible_requires_new_setup` when prohibited paths are nonempty;
4. no assertion hard-codes the ambient total path count.

No production/config/payload change, generic allowlist, old payload regeneration, candidate/R3
access, release operation, Advisor guidance or Human authorization is justified.

## Exact next branch and stop

Next branch: `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12`, an offline test-only canonical
classification expectation correction. Orchestrator must first review this decision, update
`FULL_PLAN_REFERENCE.md`, organize and commit the reviewed state, and freeze the exact PLAN-only
activation topology.

C12 must use a brand-new root under
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-12-offline/`.
It gets one implementation commit changing only `tests/test_p7_thermal_diagnostics.py`, followed by
one invocation per validation item: compileall, the same exact 13 targeted selectors, the same four
focused modules, full unittest discovery with exit `0`, `codegraph sync`, and both diff checks as
one item. Retry/fallback are `0`; any nonzero stops later items.

Candidate/retained R3/canonical retained validator/eligibility emission/release/network/`.env`/
device/camera/Ray/strip/cleanup/formal/public analyzer/TD-C/sentinel/P8 remain locked at `0`.
Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

Planner stop: `F19_CORRECTIVE_12_WAITING_ORCHESTRATOR_ALIGNMENT`.
