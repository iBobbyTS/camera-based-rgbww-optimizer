# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1 Planner review archive

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-IMMUTABLE-CANDIDATE-VALIDATION-ONLY-CLOSURE-V1`

**Reviewed stop:** `B2_P7_C1_C1_C1_C1_V1_C1_V1_IMMUTABLE_CANDIDATE_VALIDATION_ONLY_WAITING_PLANNER_REVIEW`

**Planner decision:** `REJECTED_PRE_GATE_INITIAL_CLEAN_SELF_CONTAMINATION_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`

## 1. Reviewed scope and frozen inputs

The package activated at commit
`56adae01902e9fde99270bc69db9cda5ee5afe53`, direct parent
`7d8a12178372ee34428665273086497da98f9099`, subject
`chore(plan): activate p7 outer plain validation closure`, with the exact paths:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260731-1808-p7-retained-r3-b2-p7-outer-plain-wrapper-failure-review.md`

The active package was validation-only over immutable candidate
`864f08cc5436519a37e41d553e49ebde4a3c8bb2`. Code/test writes,
implementation commits, CodeGraph, retry/fallback and all
external/retained/device effects were frozen at zero. The candidate remained
non-consumable pending a complete fresh regression sequence and independent
Planner review.

Frozen candidate identity:

- parent: `44fb7295f0f71030833476225350da01ce3c71d3`
- subject: `chore(p7): retain rejected outer plain nul candidate`
- exact paths:
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
  and `tests/test_p7_retained_r3_controller_domain_template.py`
- canonical binary diff SHA-256:
  `b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4`
- source blob/bytes/SHA-256:
  `5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5` / `19753` /
  `10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2`
- test blob/bytes/SHA-256:
  `d0f733426673aa9a57fcb1195ecea014f8c48062` / `27386` /
  `4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e`

## 2. Evidence and root cause

The wrapper used the required ordinary `pregate_exit` variable rather than a
zsh special parameter. The resulting seven-line EOF handoff at evidence commit
`045915dae74b14c9a56d6524d5573a5bdeade4d4` truthfully persisted exactly one
`PRE_GATE_LOGICAL_EXIT=1` marker. The complete ER identity at that commit is
bytes `1129765`, SHA-256
`954e378e23fd9dfc4f6bf0f50da765076db54d5c62030995207c983f674c76b3`.

The logical exit does not establish a candidate semantic failure. The wrapper
wrote the ER section header before the Python gate reached its initial-clean
porcelain assertion. That repository write made the worktree dirty, so the
gate rejected its own evidence append. This is deterministic execution
packaging self-contamination: the evidence writer ran before the invariant it
was meant to observe.

Targeted11, focused93, compileall and full778 were correctly not started.
Candidate source/test bytes were not changed, no implementation commit was
created, retry/fallback were zero, and no external or retained artifact route
was entered. Therefore this run supplies no negative evidence about candidate
`864f08c...`, but it also supplies no regression evidence that could make the
candidate consumable.

## 3. Validation quality and decision

The seven-line marker is sufficient to establish the wrapper's terminal result
and the ordering defect, but not to accept candidate validation. The package is
rejected at the pre-gate boundary. Candidate `864f08c...` remains immutable and
non-consumable; retained R3 remains unvalidated/unconsumed, and no integration,
validator, eligibility, release or device stage is unlocked.

This is not a scientific branch, code-owner defect, Human-authorization issue,
or reason to regenerate the candidate. It requires one subordinate
validation-only successor that changes only the ordering of transient evidence
collection and the single terminal ER append.

## 4. Exact successor branch

The successor must preserve candidate `864f08c...` and all code/test bytes:

1. code/test writes and implementation commits remain exact `0`;
2. an ER append descriptor may be opened in advance, but no byte may be written
   before the gate has independently proved initial clean and reached terminal;
3. preferably buffer all observations in memory, including the exact printed
   `PRE_GATE_LOGICAL_EXIT=<value>` line, then perform one EOF append only after
   the complete validation sequence reaches terminal;
4. on the success path, the one append must persist exact marker
   `PRE_GATE_LOGICAL_EXIT=0` once together with targeted `11/11`, focused
   `93/93`, compileall exit `0`, and unified full `778/778` results;
5. before that one append, every identity and clean-porcelain check must observe
   a repository untouched by the current execution;
6. if initial-clean itself fails, the Executer must not write ER and must return
   the failure directly; it may not contaminate the state it is diagnosing;
7. CodeGraph, implementation commit, postcommit test, retry/fallback,
   external/retained/device effects all remain exact `0`.

The gate marker must be genuinely captured from the owning Python command's
logical exit, printed once, retained in the in-memory terminal buffer, and
persisted verbatim in the sole successful EOF append. A predicted, inferred,
or prewritten marker is not evidence.

## 5. Residual risks and locks

The primary residual risk is another observer-induced dirty worktree if any
header, marker, temporary repository file, archive, debug note, PLAN, FULL, or
other byte is written before the terminal evidence append. Opening a file
descriptor is not a write; truncation, header emission, newline emission,
placeholder content, or any other byte is a write and is prohibited.

Old failed controller/root/evidence paths, retained R3, candidate payload,
Git provenance replay, real B2, subordinate manifest, canonical validator,
eligibility, retained audit, every release operation, network, DNS,
environment, credentials, device, camera, Ray, strip, cleanup, capture,
FORMAL, public analyzer, TD-C, sentinel, P8, firmware and deployment remain
hard locked at zero. No Human authorization or Advisor decision is required.

Maintenance assessment: the candidate remains inside the existing deterministic
template owner and dedicated test; the successor changes no production owner
and adds no abstraction or parallel execution path.
