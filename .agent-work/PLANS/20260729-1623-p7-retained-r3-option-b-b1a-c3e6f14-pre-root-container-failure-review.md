# REF-P7-25-R2-B1A-C3E6F14 review / frozen-controller pre-root container hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F14-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**PLAN snapshot SHA-256:**
`bd767aae9406608d5c8e2beda1a5db19b5fde1498ac6ae612c4777c0917524e9`

**Decision:** `rejected_pre_root_container_absent_hard_failure`

**Proposed unique successor:**
`REF-P7-25-R2-B1A-C3E6F15` — `pre_controller_fixed_container_creation_owner_correction`

## Reviewed scope and frozen execution method

This review covers only F14's one-shot, pure-offline frozen-controller replay.  The reviewed
method was: exact token-only materialization of the final F13 controller; static qualification;
then one caller passing one absent timestamp candidate as the sole positional root argument to
one controller.  The reviewed PLAN required any post-qualification non-zero terminal to stop at
Planner, with no controller rewrite, re-import, re-execution, retry, alternate root, or caller
restart.

The controller's F14 root acquisition contract first evaluates
`lstat_identity(CONTAINER)`.  It does not authorize the caller to create either the fixed package
container or the candidate root.

## Evidence reviewed

| Evidence | SHA-256 | Planner finding |
| --- | --- | --- |
| controller qualification record | `8a2b62c3766da149694221ef0dd07b21310ded7677c4e2e5628315cf4fb0210a` | pass; exact F13-to-F14 token replacement, one materialization, no execution/import/root |
| qualification seal | `e0266eccb8ab2e47a139c2babf413095afc7dff3a841f6ccc01681fab4a31d2b` | file/directory fsync, strict reload, independent hash all recorded |
| pre-root fallback terminal | `7d313f7a3d67b09ca4d8b5b90fb0c6e92e26634e96b262ea67c7248a1131351d` | terminal is truthful and terminalization completed |

Qualification proved source bytes/SHA `72892` /
`7025ed677ae5dc8de2f83e12c4f68bd669ff86948e0660e7d7f7daa1b0e0383a`, target bytes/SHA
`72892` / `04ab53b01bdc2ca25206164987c31b8308a091c2b5328c9f0c26a3fa93632ad0`, old token counts
`0/0`, new counts `6/28`, other-byte changes `0`, and UTF-8 AST parse count `1`.

The sole invocation then terminated before fresh-root acquisition with:

```text
FileNotFoundError: /Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f14-offline
```

The missing fixed package container makes `lstat_identity(CONTAINER)` fail before any candidate
root can be acquired.  This is a packaging/ownership contradiction, not a qualification success
or an execution success.

## Validation quality and accounting

- controller invocations `1`; fresh roots `0`; candidate-root creation `false`;
  retry `0`; failed-root reuse `0`; controller rewrite after qualification `0`;
  terminalization failure `null`;
- clone/checkout, all five budgeted acquisitions, materialization, fixtures, AST-owner validation,
  pre/post/full tests, stage, external commit, canonical validation, successor manifest and
  verifier: all `0`;
- candidate/R3/audit/eligibility/consumer/release and device/network/DNS/env/credential/camera/
  Ray/strip/cleanup/capture/analyzer/FORMAL/firmware/deployment: all `0`;
- shared HEAD remained `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; shared staged paths remained
  `0`; retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`, rollback
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

## Planner finding and disposition

**Rejected.**  Qualification itself is accepted as evidence, but the F14 package is rejected
because its sole controller reached a required pre-root gate with a nonexistent fixed container.
The PLAN's terminal rule means the caller correctly stopped; qualification pass cannot substitute
for a fresh-root execution, and this package produced no child, manifest, eligibility evidence or
release authority.

The F14 controller, its candidate root, and its fallback terminal are immutable historical
evidence.  They must not be repaired, reused, imported, executed again, or treated as an input to
candidate validation, eligibility, retained-R3 release, or device work.

## Exact next branch and residual risks

I propose that the Orchestrator add exactly one new blocked corrective reference task,
`REF-P7-25-R2-B1A-C3E6F15`, owned by a dedicated **pre-controller fixed-container bootstrap
owner**.  Before any new controller is started, that owner must create and verify the exact fixed
package container (absolute path, directory/non-symlink identity, permissions, emptiness/allowed
contents and durable seal).  It must not create a timestamp candidate root.  A later separately
frozen controller package may consume only that sealed bootstrap evidence; it may not reuse or
rerun F14.

This is Orchestrator-owned execution packaging.  No Advisor scientific decision or Human device
authorization is needed.  Until FULL records the successor's ID, owner, bounds, evidence and stop
point, no executable package can be written.

**Planner stop:** archive complete; active PLAN is rewritten as a non-executable Planner stop
awaiting the required FULL update.  R3 release, network/device access, and every controller run
remain forbidden.

**Maintainability judgment:** the failure exposes one missing lifecycle owner at the package
container boundary; isolate it as a dedicated bootstrap responsibility rather than weakening the
frozen controller or duplicating root-creation logic.
