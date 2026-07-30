# REF-P7-25-R2-B2-C4-P2：repo-owned controller integration qualification

**计划状态：** `EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-INTEGRATION-QUALIFICATION-V1`

**当前唯一动作：** 新增一个专用、纯 synthetic 的 integration test owner，直接组合
现有 exact-five callback lifecycle 与 accepted controller-preparation helper，证明
source preparation、terminal seal、exact target validation 与 ER gate 可以在现有 owner
边界内 fail closed；不得新增 production adapter、generated external controller、第二
validator 或 eligibility owner。

**唯一 Planner stop：**
`B2_C4_P2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**上一 gate archive：**
`.agent-work/PLANS/20260730-1253-p7-retained-r3-option-b-b2-c4-p1-c1-orchestrator-gate-archive.md`
（bytes 和 SHA-256 由本次 Planner 完成后冻结在本 PLAN 第 2 节；Orchestrator 激活前必须
独立复算一致）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_integration_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-INTEGRATION-QUALIFICATION-V1","execution_authorized":true,"dispatch_state":"ready_after_orchestrator_activation_commit","single_current_action":"add_one_pure_synthetic_existing_owner_integration_qualification_test","architecture_decision":"existing_exact_five_callbacks_directly_compose_accepted_preparation_helper_no_adapter","orchestrator_activation":{"expected_base":"3458b4b60c49328703a6e2bc95a62f33e13cdfe8","required_subject":"chore(plan): activate retained r3 integration qualification","implementation_parent":"full_activation_commit_sha_frozen_at_dispatch"},"accepted_preparation_commit":"4678a3e6f93704912952776bc11fa2b0945d80b1","exact_changed_paths":["tests/test_p7_retained_r3_controller_integration.py"],"implementation_commit_subject":"test(p7): qualify retained r3 controller composition","historical_c4_reads":0,"retained_r3_reads":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"commit_budget":1,"retry_budget":0,"planner_stop":"B2_C4_P2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Frozen architecture decision

CodeGraph current-source evidence shows that no new adapter is justified:

- `p7_retained_r3_exact_five_controller.ExactFiveControllerCallbacks` already
  injects the fixed acquire/materialize/gate/commit/manifest/validator/terminal
  sequence, enforces exact-bool pass results, seals every pre-terminal failure
  once and owns no consumer/eligibility/device/release surface.
- accepted
  `p7_retained_r3_controller_preparation` already owns the AST-edge statement
  selector, deterministic byte replacement, canonical JSON plus exact LF,
  exact path/bytes/SHA/device/inode target validation, deep immutable seal gate
  and ER callback admission only after seal validation.
- A callback supplied by a caller can invoke those pure helper APIs directly;
  neither owner needs runtime I/O or a new orchestration state machine.

P2 therefore adds exactly one dedicated integration qualification test and no
production code. A test-only path is substantive here: it must execute the real
public APIs of both owners together, verify ordered cross-owner behavior and
prove the failure boundaries below. Assertions that merely restate fixtures or
only execute code are not acceptable.

## 2. Frozen repository inputs and activation topology

The Orchestrator activation commit must have exact parent
`3458b4b60c49328703a6e2bc95a62f33e13cdfe8` and exact subject
`chore(plan): activate retained r3 integration qualification`. At dispatch, its
full SHA becomes the immutable implementation parent. If HEAD does not match
that topology, PLAN/FULL machine-contract identity, or a clean implementation
scope, stop before editing.

Committed implementation inputs are read only from Git, not copied from the
worktree or any external controller:

| Path | Required SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

The accepted preparation commit is
`4678a3e6f93704912952776bc11fa2b0945d80b1`; the activation commit must retain
it as an exact ancestor. The archive identity for this transition is:

- path:
  `.agent-work/PLANS/20260730-1253-p7-retained-r3-option-b-b2-c4-p1-c1-orchestrator-gate-archive.md`;
- bytes: `3403`;
- SHA-256:
  `22fdef333af39fe13719cc06951f285071d932a6da20b3de35b06e03681df6ab`.

Orchestrator must independently recompute the two values above before committing
activation. No PLAN content may change without another Planner review.

## 3. Exact implementation scope

Only create:

```text
tests/test_p7_retained_r3_controller_integration.py
```

Do not modify either production owner, their existing dedicated tests, package
exports, docs, skill, wrapper, GUIDE, FULL, PLAN, archives or any other path.
The new test must use only in-memory synthetic bytes and deterministic fake
identities. It must not read any historical/external evidence root, retained R3
artifact or runtime secret.

The test owner must exercise at least these behaviors through the actual public
APIs:

1. **Success composition:** prepare an in-memory controller source containing
   one uniquely owned adjacent assignment/validation pair; execute one prepared
   exact-five lifecycle; have injected callbacks consume the prepared source,
   create a canonical terminal payload with a synthetic exact
   `SealTargetIdentity`, validate it, and admit exactly one synthetic ER callback
   only after the lifecycle's synthetic validator callback and terminal seal.
   Assert the exact callback order, five materialize calls, one terminal, one ER
   gate, prepared source SHA, target identity and immutable gate payload.
2. **Preparation failure:** malformed/ambiguous in-memory source must fail before
   lifecycle dispatch; every lifecycle callback count, terminal count and ER
   callback count remains zero.
3. **Lifecycle failure:** one injected pre-terminal phase must fail; the existing
   lifecycle must stop later phases and invoke terminal exactly once. The failure
   terminal must still pass canonical serialization and exact-target validation
   before the synthetic ER callback is admitted; it must not become eligibility.
4. **Seal-target tamper:** wrong type or value in any one target field must fail
   closed before the ER callback; no workaround or fallback terminal is allowed.
5. **Ownership/static boundary:** imports and runtime calls in the integration
   test must not import or invoke the real canonical validator, retained-release
   consumer, filesystem/process/network/environment/device/camera/Ray/strip
   owner. The callback named `canonical_validator` is an in-memory synthetic
   exact-bool stub only; assert it is invoked once on success, while actual
   canonical-validator import/call count remains zero.

Do not reproduce either module's implementation inside the test. Small local
fixture builders and callback fakes are allowed only to connect public APIs and
record observable order/counts.

## 4. Zero budgets and hard locks

All budgets are cumulative for this package; retry/fallback is `0`:

| Operation | Budget |
| --- | ---: |
| historical C3/C4 source/evidence/root reads | 0 |
| old failed-root inspect/repair/reuse | 0 |
| retained R3 candidate/artifact reads | 0 |
| real B2/controller dispatch | 0 |
| actual canonical validator import/call | 0 |
| eligibility emission/consumer | 0 |
| lineage/release create/validate/replay/consume | 0 |
| network, DNS, `.env`, credential access | 0 |
| device/camera/Ray/strip/cleanup/capture/FORMAL | 0 |
| public analyzer, TD-C, sentinel, P8 | 0 |
| external output root or temporary evidence file | 0 |
| implementation commit | 1 |
| amend/rebase/fixup/second commit | 0 |

The synthetic callback bearing the lifecycle field name `canonical_validator`
does not consume the actual-validator budget: it must be an inline, in-memory
stub with no validator import or eligibility surface. Any need for a historical
C3/C4 artifact, retained input, actual validator, second production path or new
adapter is a contradiction; stop and return to Orchestrator rather than widening
scope or asking Advisor/Human.

This package is expected to remain below 10 minutes, so it uses the normal local
execution owner. Visible Terminal, automation and long-task polling are not
authorized.

## 5. Ordered execution and validation gates

Execute exactly once in this order; any failure stops the package with no edit,
test or commit retry:

1. Parse the single PLAN machine contract and FULL machine state. Require FULL
   `active_task_count=1`, `active_task=REF-P7-25-R2-B2-C4-P2`, matching
   `active_plan_contract_id`, retained status
   `RETAINED_UNVALIDATED_UNCONSUMED`, P1-C1 accepted/provenance-bound status and
   canonical validator sole-owner state. Verify activation topology, clean
   implementation scope, exact committed input hashes and accepted-commit
   ancestry.
2. Create the exact one test path with the behaviors in section 3. Before tests,
   require `git diff --name-only` to equal that singleton path and
   `git diff --check` to pass.
3. Run the new integration test alone once.
4. Run the two existing owner suites together once:
   `tests.test_p7_retained_r3_exact_five_controller` and
   `tests.test_p7_retained_r3_controller_preparation`.
5. Run the focused retained-controller group once: the new integration test,
   the two suites above and `tests.test_p7_retained_release_audit`.
6. Run the full unittest suite once.
7. Run compileall once over `src/camera_based_rgbww_optimizer` and `tests`.
8. Run CodeGraph sync once and require success. Recheck singleton path and
   `git diff --check`.
9. Freeze implementation parent full SHA, exact singleton changed-path set,
   absent-before/new-after Git blob OIDs, new-file SHA-256, canonical binary Git
   patch SHA-256 and exact subject. Create exactly one commit with subject
   `test(p7): qualify retained r3 controller composition` and a concise detail
   explaining existing-owner callback composition.
10. Verify the child has the frozen parent, exact subject, exact singleton tree
    change, after blob/file/patch identities and no implementation drift. Rerun
    the new integration test alone once as the sole postcommit test.
11. Append one truthful handoff to `.agent-work/EXECUTION_RESULT.md` only after
    terminal validation. Record all identities, ordered gate counts/results,
    explicit zero-budget counters, actual-validator call count `0`, synthetic
    validator-stub count, commit SHA and the unique stop. Do not edit PLAN/FULL
    or any archive.

`EXECUTION_RESULT.md` is evidence-only and is excluded from the implementation
commit/path set. If any precommit gate fails, do not commit. If commit or
postcommit verification fails, do not amend, repair or make a second commit;
record the exact terminal state if the seal gate permits and stop.

## 6. Acceptance criteria and failure branches

Planner may accept P2 only if all of the following are independently reviewable:

- exact activation and one-child topology; exact singleton implementation path,
  blob/file/patch identities and subject;
- substantive success, preparation-failure, lifecycle-failure, target-tamper
  and static-boundary integration tests through both existing public owners;
- new targeted, existing-owner, focused, full, compileall, CodeGraph, diff and
  postcommit gates each pass at their exact invocation budgets;
- actual canonical validator/eligibility/release/historical/retained/network/
  device/external-root counters all remain zero;
- the canonical validator remains the sole eligibility owner and no production
  adapter, external generated controller or parallel execution framework exists;
- one valid ER handoff records the unique stop
  `B2_C4_P2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

Failure routes are exact:

- architecture/input/FULL/topology contradiction: stop pre-edit and return to
  Orchestrator;
- implementation or validation failure before commit: preserve the one-path
  diff, append a sealed failure handoff if permitted, and wait for Planner;
- commit/postcommit mismatch: preserve immutable commit evidence, no amend or
  second commit, and wait for Planner;
- scientific interpretation and Human device authorization are not implicated.

P2 acceptance unlocks only the Orchestrator's next provenance-bound C4 package.
It does not unlock retained R3, the actual canonical validator, eligibility,
release consumption or any device work.

## 7. Stop and handoff

After exactly one success or failure attempt, stop at
`B2_C4_P2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW` and hand
the implementation/evidence identities to Planner. Planner must archive this
package before rewriting PLAN; Orchestrator alone may update FULL.

## 维护性判断

This package adds only one dedicated cross-owner test and reuses the existing
fixed lifecycle plus accepted pure preparation owner. Ownership remains
separate and explicit: lifecycle sequencing stays in exact-five, source/seal/ER
admission stays in preparation, and eligibility stays exclusively in the
canonical validator. No cleanup refactor is recommended.
