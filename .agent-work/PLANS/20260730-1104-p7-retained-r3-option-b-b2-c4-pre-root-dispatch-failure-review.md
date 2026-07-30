# REF-P7-25-R2-B2-C4 pre-root dispatch failure review

**Planner decision:** `REJECTED_PRE_ROOT_DISPATCH_WRAPPER_FAILURE`

**Review date:** `2026-07-30`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-AST-SPAN-SUCCESSOR-QUALIFICATION-V1`

**Reviewed PLAN:** `.agent-work/PLAN.md`, bytes `16780`, SHA-256
`d3cf1d2827b7d6fe367b4e3e4934f674588b6d6575c5e848e3a6dfbe6e865b8e`.

**Activation topology:** commit
`cb90244c92d75225d1624a59d1b976757e45994d`, direct parent
`b4a3ad513f3bbca55f0c38c08fde2d3aa06aa29b`, subject
`chore(plan): activate b2 c4 ast span successor`, exact changed paths
`[".agent-work/PLAN.md"]`.

## Reviewed result

The sole permitted `git rev-parse HEAD` completed, but the same frozen zsh
dispatch script then attempted to assign the command result to zsh's special
read-only parameter `status`. zsh stopped with `read-only variable: status`
before it emitted the captured dispatch value or invoked the builder.

The unrecoverable dispatch value is not reconstructed from a later read.
Observed budgets for this invocation are:

```text
symbolic HEAD reads = 1
second symbolic HEAD reads = 0
dispatch value emitted = 0
builder invocations = 0
future root creates = 0
C3/source/successor reads or writes = 0
retained/decision/validator/release/device/network operations = 0
EXECUTION_RESULT appends = 0
```

Because no post-failure physical artifact or ER handoff was authorized or
created, this review is limited to the exact pre-root dispatch facts reported
to the Planner and the independently verified activation topology. It does not
claim an independently replayable dispatch record, builder evidence, source
identity, or C4 qualification result.

## Decision

The execution is rejected. It proves no part of C4's input, transform,
shared-lifecycle matrix, terminal lifecycle, or acceptance criteria. It also
does not consume the builder/root budget because the builder was never invoked
and the original future root was never created.

The fault is a local deterministic shell-wrapper naming defect, not a defect in
C4's accepted C3 inputs, science-free transform, matrix, or evidence owner.
An independent C4-C1 qualification package would add a parallel owner without
improving the boundary. The smallest successor is therefore a PLAN-only
reactivation of the same C4 package with a frozen shell-safe pre-root dispatch
contract.

Although the original future root is reported absent and therefore unused, it
is permanently superseded. The successor uses a brand-new root so the lost
first dispatch value cannot be confused with a later independently frozen
dispatch. The original root must not be probed, created, reused, deleted,
renamed, or represented as evidence.

## Exact next branch

`REF-P7-25-R2-B2-C4` remains the reference task. Before execution, an exact
PLAN-only direct-child activation must freeze:

1. one `zsh -f` dispatch owner with no assignment to `status` or any other zsh
   special/read-only parameter;
2. content-free self-check fixtures executed before the sole symbolic HEAD
   read;
3. exactly one `git rev-parse HEAD`, captured into a shell-safe local variable,
   validated as one lowercase 40-hex commit, compared with the activation
   identity, and emitted exactly once before builder invocation;
4. no second HEAD read, transcription, recovery, fallback, alternate dispatch,
   or wrapper retry;
5. one brand-new C4 root while preserving every C3/source input, transform,
   `12/12` matrix, lifecycle, lock, and acceptance condition from the rejected
   package.

Until the Orchestrator reviews this archive and a later PLAN-only activation
sets `execution_authorized=true`, the next package is non-executable. Real B2,
B3, retained R3, canonical validator, eligibility, release, devices,
FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.

## Residual risk and stop

The main residual risk is another pre-root shell portability failure. The
frozen self-check and restricted variable namespace address that risk without
touching C4 semantics. Any self-check, capture, validation, output, activation,
or topology mismatch must stop before builder invocation and may not recover
the dispatch value with a second HEAD read.

Planner stop:
`B2_C4_DISPATCH_FAILURE_REVIEWED_WAITING_PLAN_ONLY_ACTIVATION`.

## 维护性判断

The correction remains within the pre-root dispatch wrapper and introduces no
new repository module, scientific rule, provenance owner, or execution
framework. C4's single external builder and single lifecycle owner remain the
only owners after dispatch.
