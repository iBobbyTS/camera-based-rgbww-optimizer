# P7 retained-R3 B2 P4 runtime-token successor review and architecture reassessment

**Review date:** `2026-07-31`

**Reviewed reference task:**
`REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1-RUNTIME-TOKEN-FIXTURE-SEPARATION-CORRECTION-V1`

**Evidence commit:** `ec2dd705fbcf3349297fb141b732ebc9b61aaf94`

## Reviewed evidence

- Activation HEAD was `1bc089e04000abafa65fb8d65e131fe68f39ca3f`; the first and only outer Git invocation was the exact absolute `rev-parse HEAD` command required by the package.
- The fresh source was created once at the package-specific external path, read once, and retained with bytes `22752`, SHA-256 `3be4c1cb561b40b15531eb7bc0ad67657fc4a2398371a0d8d4adb8dfccc150e4`, mode `0600`.
- Runtime-token fixture separation itself succeeded: the forbidden attribute token was assembled outside the scanned runtime byte domain and did not self-inject into those bytes.
- The outer launcher used one `input=<exact frozen source bytes>` channel, omitted `stdin`, and started exactly one controller process.
- The source writer did not satisfy the frozen exclusive-writer contract: it used a patch plus mode change and did not prove `O_CREAT|O_EXCL|O_NOFOLLOW`, complete-write handling, file fsync, parent-directory fsync, or a returned immutable physical identity.
- The existing repo-owned `analyze_controller_source` ran once and rejected the actual runtime source before any effect with stable code `reflection_rejected`; generic primary/failure projection still used forbidden reflection syntax.
- Controller exit was `1`; root creation, Git6, four synthetic inputs, matrix16, qualification, terminal/seal/admission, retained reads, actual validator, eligibility, release, network and devices all remained `0`.
- Evidence commit `ec2dd70` changed only `.agent-work/EXECUTION_RESULT.md`, preserving the failed external artifact and reporting both independent rejection reasons.

## Planner decision

**Decision:** `REJECTED_PRE_EFFECT_REFLECTION_AND_SOURCE_WRITER_PROOF_GAP`.

The result is not an integration qualification. Token separation and single-input launching are useful partial observations, but the package fails both the repo analyzer gate and the explicit physical source-writer proof. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; real B2, canonical validation, eligibility, release consumption and every device/scientific stage remain locked.

No retry or repair of the failed source/root is authorized.

## Architecture reassessment

The I1 successor chain has now exposed repeated defects in disposable outer-controller composition rather than defects in the accepted scientific or retained-artifact contract:

1. extra outer Git inspection before source creation;
2. Markdown machine-row delimiter handling;
3. repeated outer status/Git-budget drift;
4. mutually exclusive `stdin` and `input` launcher arguments;
5. a self-referential forbidden-token matrix assertion;
6. forbidden reflection in the runtime source;
7. a source writer with no exclusive/no-follow/fsync proof.

Another one-off source patch would materially worsen the fragile state-machine and duplicated-envelope problem. The maintainability guardrail therefore requires an enabling repo-owned boundary before another synthetic integration is attempted.

The existing ownership boundaries are intentionally narrower:

- `p7_retained_r3_controller_preparation` owns deterministic pure byte composition and terminal preparation, and explicitly owns no filesystem or process operation;
- `p7_retained_r3_controller_conformance` is the sole AST/conformance and transport eligibility owner;
- `p7_retained_r3_provenance_io` owns physical file/root/read-only-Git facts and already provides the accepted no-follow read identity;
- the exact-five lifecycle owner owns phase ordering and terminal dominance, not source construction or launching.

Adding subprocess launching to any of those modules would blur an established boundary. The smallest maintainable correction is one new `p7_retained_r3_controller_runtime` module plus its dedicated test. It owns only the outer envelope: deterministic composition through the preparation owner, conformance delegation, exact exclusive raw-source persistence and identity proof, and one exact source-bytes subprocess launch. It must reuse the existing owners, expose their reports rather than reimplement them, and contain no PLAN-specific matrix, retained-artifact interpretation, canonical validator, eligibility, release or device behavior.

## Exact next branch

Create one bounded repo implementation package:
`REF-P7-25-R2-B2-P5` / `P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-REPO-OWNED-CONTROLLER-RUNTIME-OWNER-V1`.

Exact implementation paths:

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py`
2. `tests/test_p7_retained_r3_controller_runtime.py`

The package must prove no-reflection pre-effect rejection, exclusive source-writer semantics, single-input launcher semantics, token-domain separation through the sole existing analyzer, and deterministic source/report bytes. It must run targeted, focused, full-suite, compileall, CodeGraph sync, and post-commit targeted checks. It must not create or dispatch another external disposable controller and must not read retained/external evidence.

## Residual risks and locks

- This implementation does not itself qualify synthetic integration and does not make retained R3 consumable.
- A later fresh synthetic integration may use the accepted runtime owner only after separate Planner activation; it may not reconstruct the envelope in a generated controller script.
- Retained/candidate data, real B2, canonical validator, eligibility, release operations, network, environment, credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware and deployment remain exact zero.

**Planner stop:**
`B2_P5_REPO_OWNED_CONTROLLER_RUNTIME_OWNER_WAITING_ORCHESTRATOR_ACTIVATION`.

