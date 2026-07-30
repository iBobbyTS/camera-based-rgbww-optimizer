# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10 Planner review

**Review date:** `2026-07-30`

**Verdict:** `REJECTED_TARGETED_AMBIENT_HEAD_AND_HISTORICAL_CHECKPOINT_SEAMS`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-10-GOVERNANCE-LINEAGE`

## Reviewed scope and frozen evidence

- Activation commit: `4316d0ce84fea8e9c87f90069567a82238e7a733`, parent
  `6a912cb68f80ef701552d3c822e612aefa1fb75a`, subject
  `chore(plan): activate f19 governance successor validation`, exact changed path
  `.agent-work/PLAN.md`.
- Implementation commit: `0682cd8763516dfb19a8e1ad48c53cb9934b9d19`, parent
  `4316d0ce84fea8e9c87f90069567a82238e7a733`, subject
  `fix(p7): validate exact governance lineage successor`.
- Implementation exact changed paths:
  `config/hsi/p7-governance-lineage-successor-v1.json`,
  `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`, and
  `tests/test_p7_thermal_diagnostics.py`; additional paths `0`.
- Canonical implementation binary patch SHA-256:
  `1ab8c656539ad4742e5f89da15e6ffdaeb63fe9e36aca785b955ac17c9fa3d82`.
- Committed file SHA-256 values: config
  `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`, source
  `54fc156df262043e1fbd51901e988e45f08d5bf8d9c8dec41d3bce7ca26b5008`, test
  `7475aea66270c4f462be38be60707f506a64bf5bc5d886985a3995a684ee6d20`.
- Fresh root:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-10-offline/20260730T125622Z`, mode `0700`.
- Terminal evidence:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-10-offline/20260730T125622Z/terminal-evidence.json`,
  bytes `5703`, mode `0600`, SHA-256
  `644439af182a007e88e6978aaecc8c6ec2e820add732c56b9e74716bce6bcbd5`.
- Targeted log:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-10-offline/20260730T125622Z/targeted.log`,
  bytes `6752`, mode `0600`, SHA-256
  `1b5f065935731e831e46354873b0a0e20944cc286f47fdceeeaf0ece9824751c`.

Planner performed no test, compile, CodeGraph, candidate, retained-R3, release, network,
environment, device, camera, Ray, strip, cleanup, formal or public-analyzer invocation.

## Validation quality and findings

The activation and implementation topology, exact three-path scope, manifest ownership record,
single-FD artifacts and zero locks are internally consistent. Compileall ran once and exited `0`.
Targeted unittest ran once, with `12` selectors: `9` passed, `1` failed and `2` errored. Retry and
fallback were `0`; fail-fast correctly left focused, full, CodeGraph and both diff checks at `0`.

The two new dedicated successor tests both passed:

- `test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`;
- `test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`.

They provide useful but incomplete evidence that the subordinate manifest is exact, fail closed,
does not emit eligibility, and preserves the existing canonical candidate builder as eligibility
owner. C10 nevertheless cannot pass because the required validation chain did not reach a green
targeted gate.

The three failing selectors are bounded engineering/test seams rather than scientific failures:

1. `test_post_eq_policy_lineage_classifies_only_exact_accepted_paths` hard-codes
   `len(changed_paths) == 59`. At the C10 ambient HEAD the actual sorted unique changed-path result is
   `265`. The full candidate still reports `eligible_waiting_for_planner` and no prohibited paths;
   a snapshot cardinality is not the lineage acceptance invariant and will continue to drift as
   reviewed plan archives are added.
2. `test_qualification_evidence_adapter_is_release_isolated` and
   `test_qualification_evidence_adapter_rejects_preparation_drift` validate the historical
   qualification checkpoint `52a7168cd2510e9730e30101fc8fbf6f6d8153c1`. That checkpoint contains
   public-default owner `e7ccdda672b7d5902d81627ff98268160ff141cd` but predates governance
   successor `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`. The current implementation
   therefore selects the historical checkpoint correctly, but still compares the working current
   skill bytes against the old public-default SHA. A historical qualification audit must validate
   bytes at its requested checkpoint and must not consume unrelated working-tree current bytes.

There is no basis to rewrite the accepted immutable old policy/workflow/public-default payloads,
widen a generic allowlist, access retained R3, or request Advisor/Human guidance.

## Decision and retained implementation disposition

`0682cd8763516dfb19a8e1ad48c53cb9934b9d19` is retained as
`retained_unaccepted_governance_successor_implementation_base_v1`. It is not validation-complete,
not consumable, and cannot emit eligibility or authorize release. Its config manifest and the two
new dedicated tests are accepted only as the starting bytes for a bounded C11 corrective; this is
not acceptance of C10 as a whole.

The next exact modification scope is only:

1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`;
2. `tests/test_p7_thermal_diagnostics.py`.

The config path must remain byte-exact at SHA-256
`69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`.
The source correction must separate a historical requested-checkpoint audit from a current working
owner audit without weakening the immutable public-default payload checks or the current governance
successor check. The test correction must replace the ambient `59` snapshot with semantic
assertions tying the candidate's exact paths/classifications to the dynamically obtained sorted
unique changed-path set, while retaining the exact two-path post-EQ classification assertions.

## Exact next branch and stop

Next branch: `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11`, an offline two-path
historical-checkpoint/ambient-HEAD seam correction. Orchestrator must first review this decision,
update `FULL_PLAN_REFERENCE.md`, organize and commit the reviewed state, then freeze a PLAN-only
activation topology. Executer must use a brand-new C11 root under
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-11-offline/`.

The C11 validation chain gets exactly one invocation per item, retry/fallback `0`: compileall;
targeted C10 twelve selectors plus dedicated historical-checkpoint/ambient-path semantic coverage;
the same focused four-module suite; full unittest discovery with exit `0`; `codegraph sync`; and the
two diff checks as one item. Any nonzero stops later items. Candidate/retained R3/canonical retained
validator/eligibility/release/network/`.env`/device/camera/Ray/strip/cleanup/formal/public analyzer/
TD-C/sentinel/P8 remain locked at `0`; retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

Planner stop: `F19_CORRECTIVE_11_WAITING_ORCHESTRATOR_ALIGNMENT`.
