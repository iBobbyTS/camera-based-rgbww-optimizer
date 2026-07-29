# REF-P7-25-R2-B1A-C3E6F16 review / PLAN machine-row label mismatch

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F16-CONTEXT-CLOSED-BOOTSTRAP-V1`

**Decision:** `rejected_prebootstrap_plan_row_label_mismatch`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17`

## Reviewed scope and method

F16 authorized one context-closed, pure-offline fixed-container bootstrap using exactly four fresh
paths. The direct Executer had to make the bootstrap Python process its first tool call; that process
could read only current PLAN raw bytes, the unique FULL machine row and F16 section, and shared Git
metadata after limited-input validation. Controller, tests, Git mutation, retained R3, release,
network and devices were all locked at zero.

The reviewed PLAN froze FULL SHA-256
`d9bd8b3273b946be18fc686dca6a364bc2dbe2785fef822b65215ff1242cd407`, carried one exact
backtick-wrapped `PLAN_MACHINE_CONTRACT` row, required the unique FULL
`FULL_PLAN_MACHINE_STATE` row, and matched the FULL activation subset `12/12` before dispatch.

## Terminal evidence and independent checks

The terminal handoff is `.agent-work/EXECUTION_RESULT.md` section
`REF-P7-25-R2-B1A-C3E6F16 terminal handoff`. The Executer recorded:

- terminal `LIMITED_INPUT_PRECONDITION_FAILED`;
- frozen PLAN SHA-256
  `51591d29c675dee3c5137c5478981770915b68bd1c729d5bec9ebbc5032c4746`;
- frozen FULL SHA-256
  `d9bd8b3273b946be18fc686dca6a364bc2dbe2785fef822b65215ff1242cd407`;
- `ValueError: PLAN_MACHINE_STATE row lacks JSON object` before dispatch verification;
- container, record, seal and fallback attempts/succeeded all `0/0`;
- retry, reuse, rewrite and alternate path all `0`;
- controller, tests, Git mutation, R3, release, network, DNS, environment, credential, device,
  camera, Ray, strip, cleanup, capture, analyzer, FORMAL, firmware and deployment all `0`.

Planner independently proved the reviewed PLAN contains exactly one
`PLAN_MACHINE_CONTRACT={...}` line and no `PLAN_MACHINE_STATE={...}` line. Thus the limited-input
loader searched for a non-contract label even though the authoritative serialized JSON object was
present and valid under the exact PLAN marker. This is a dispatcher/parser token error, not a
malformed PLAN JSON object or FULL activation mismatch.

Planner also independently applied `lstat` to the four fixed F16 paths and found all absent:

1. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f16-offline`
2. `/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.json`
3. `/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.seal.json`
4. `/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.fallback.json`

Shared HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; staged paths are zero.
Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## Decision quality and residual risk

F16 is rejected at the first limited-input gate. It produced no bootstrap evidence and cannot be
retried, repaired or reused. The absent paths do not make the old package consumable; they only
prove all filesystem budgets remained unspent.

The next package must use four fresh F17 paths and preserve all one-shot and zero-budget semantics.
Its PLAN must name both serialized owners without aliasing:

- PLAN row marker: exact `PLAN_MACHINE_CONTRACT=`;
- FULL row marker: exact `FULL_PLAN_MACHINE_STATE=`.

The direct bootstrap loader must parse the JSON substring following each exact marker and must
reject zero, multiple, malformed, duplicate-key or non-finite objects. It must not search for or
invent `PLAN_MACHINE_STATE`. A limited-input/dispatch failure must again occur before any path
inspection and leave every attempt count at zero. F17 requires no Advisor scientific guidance or
Human device authorization.

## Stop

Archive and reject F16. Orchestrator must activate F17 in FULL before dispatch. F17 pass would still
establish only one empty sealed prerequisite; controller, retained R3, eligibility and release stay
locked behind later packages.
