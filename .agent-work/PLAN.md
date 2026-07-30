# REF-P7-25-R2-B2-C4-P1-C1：exact provenance preparation correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_PURE_OFFLINE_CORRECTION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-C1-EXACT-PREPARATION-CORRECTION-V1`

**当前唯一动作：** 在已提交的 repo-owned retained-R3 preparation owner 及其
dedicated test 内，关闭 exact target 类型、唯一函数 owner、validated-gate
深层不可变、malformed replacement typed failure 和静态 import guard 缺口；完成
全部离线验证并形成一个 exact-two-path focused successor commit。

**唯一 Planner stop：**
`B2_C4_P1_C1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**Reviewed P1 archive：**
`.agent-work/PLANS/20260730-1232-p7-retained-r3-option-b-b2-c4-p1-implementation-review.md`
（bytes `5748`，SHA-256
`d6e905dec784ec09dd4f72c28d90fb86a76ef65561650ebce6f186b03886180d`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p1_c1_exact_preparation_correction_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-C1-EXACT-PREPARATION-CORRECTION-V1","dispatch_state":"dispatchable_after_orchestrator_activation_review","execution_authorized":true,"pure_offline":true,"single_current_action":"close_exact_identity_owner_immutability_and_typed_failure_findings","implementation_parent":"ce096155227d4f24f1d6659550319aaf335d014b","exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py","tests/test_p7_retained_r3_controller_preparation.py"],"canonical_validator_remains_sole_eligibility_owner":true,"historical_artifact_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"device_operations":0,"commit_budget":1,"commit_subject":"fix(p7): harden retained r3 preparation invariants","required_gates":["targeted","focused","full","compileall","codegraph_sync","diff_check","exact_two_path_commit","postcommit_targeted"],"failure_branch":"bounded_p1_c1_review_stop","planner_stop":"B2_C4_P1_C1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Frozen start and authorization boundary

The retained implementation commit is exactly
`ce096155227d4f24f1d6659550319aaf335d014b`, direct parent
`aa0baf80aa7c83fe094ce139c5a14d04f13c67dd`, with exact two new paths and
source/test SHA-256 values frozen in the review archive. The Orchestrator may
commit this PLAN/archive and the existing truthful ER append before dispatch.

Before editing, the Executer must:

1. record the dispatch-time full HEAD as `implementation_parent`;
2. require a clean worktree;
3. require `ce096155...` is an ancestor and its exact two blobs retain the
   archived SHA-256 identities;
4. require the active PLAN task/contract IDs above;
5. stop without editing if any condition differs.

This PLAN authorizes only local source/test correction, offline checks, one
focused commit and one truthful ER append. It does not authorize package roots,
historical controller/evidence reads, retained R3, validator, eligibility,
release, analyzer, network or device operations.

## 2. Exact scope and required corrections

Only these two implementation paths may change:

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py
tests/test_p7_retained_r3_controller_preparation.py
```

No export, runner, validator, wrapper, docs, skill, config, PLAN, FULL reference
or archive may be changed by the Executer. The ER append is outside the focused
implementation commit.

### 2.1 Type-exact seal target linkage

- Validate an exact key set of `path`, `bytes`, `sha256`, `device`, `inode`.
- For every field require exact runtime type and exact value against
  `SealTargetIdentity`; Python equality alone is insufficient.
- Reject bool-for-int, integral float-for-int, numeric/string coercion, missing
  and extra fields. Keep canonical serialization/reload requirements unchanged.
- Add behavioral tests for each type-substitution class and extra fields.

### 2.2 Unique regular-function owner

- Traverse the complete AST ancestor chain through explicit parent edges.
- Accept exactly one enclosing regular `FunctionDef` and no `AsyncFunctionDef`
  or `Lambda` owner boundary.
- Reject zero regular owners and two-or-more nested regular owners. Do not return
  only the nearest owner.
- Preserve valid statement nesting inside one owner (`if`, `for`, double nested)
  and same-immediate-list adjacency.
- Add a public-path regression where an assignment/validation pair inside a
  regular function nested in another regular function is rejected as ambiguous.

### 2.3 Deeply immutable validated gate

- Convert the strict-reloaded JSON payload into an immutable recursive snapshot
  before constructing the callback-visible validated gate: mappings, lists and
  any nested combinations must not remain mutable or share caller-owned mutable
  containers.
- Preserve JSON scalar types and exact target binding.
- Prove callback-visible attempts to mutate outer and nested payload state fail,
  and that the target identity cannot change after gate creation.

### 2.4 Stable typed malformed-replacement failure

- Validate every replacement entry is exactly `SourceReplacement` before any
  attribute dereference or sorting.
- Malformed entries must raise `ControllerPreparationError` with a stable code,
  not `AttributeError`, `TypeError` or another incidental exception.
- Preserve deterministic ordering, overlap/range checks and parse+compile output
  validation.

### 2.5 Accurate static import guard

- Update the dedicated static test so `ImportFrom` checks the root of
  `node.module`, while `Import` checks alias roots.
- Keep direct-I/O call detection and the large-literal/nested-program guard.
- The test must continue to prove the current helper imports/calls no filesystem,
  process, environment, Git, network, camera, device, release or validator owner.

Do not redesign the API, add a third module, integrate historical C4, or create
a parallel validator/eligibility owner.

## 3. Ordered validation gates

Run each gate once, in this order. Retry/fallback are `0`; any failure stops the
package without repair/rerun/commit continuation.

1. targeted dedicated suite:

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_r3_controller_preparation.py' -v
   ```

2. related focused suites, once each:

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_r3_exact_five_controller.py' -v
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_release_audit.py' -v
   ```

3. full suite:

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
   ```

4. compileall:

   ```sh
   .venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests
   ```

5. `codegraph sync` at repository root;
6. `git diff --check`, with implementation path union exactly the two frozen
   paths and no third path.

Record exact commands, exit codes and exact test counts. Do not access external
evidence to perform these gates.

## 4. Focused successor commit and postcommit gate

After all precommit gates pass:

1. stage exactly the two implementation paths;
2. require staged paths equal the exact sorted two-path set;
3. create exactly one commit with subject
   `fix(p7): harden retained r3 preparation invariants`;
4. require its direct parent equals the recorded dispatch-time
   `implementation_parent` and `ce096155...` remains an ancestor;
5. require the commit's changed paths equal the exact two paths;
6. do not amend, rebase or create a second commit;
7. rerun the targeted suite exactly once against committed bytes;
8. require `git diff --check` and zero implementation-scope drift.

If the commit or postcommit gate fails, preserve any created commit and stop for
Planner review; do not repair in this execution.

## 5. Required handoff

Append one bounded section to `.agent-work/EXECUTION_RESULT.md` containing:

- task/contract, dispatch parent and successor full SHA;
- exact changed paths, subject and ce096155 ancestry proof;
- concise fixes for REV-P1-001 through REV-P1-004 and the static guard;
- each gate command, exit code and exact count;
- compileall, CodeGraph, diff and static results;
- explicit zero counters for historical C4/retained-R3 reads, external
  controller, validator, eligibility, release, analyzer, network, `.env`, device,
  camera, Ray, strip, cleanup, capture, formal, TD-C, sentinel and P8;
- residual maintainability judgment and exact Planner stop.

Do not edit either plan file or archives. Stop at
`B2_C4_P1_C1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW` regardless of pass
or fail. A passing correction still does not authorize C4 integration, real B2,
retained-R3 audit, B3, eligibility, release consumption or device work.

## 6. Hard locks and failure branch

Do not read, import, compile, execute, repair or reuse any historical C4 external
source/builder/root/artifact, retained-R3 candidate/artifact, release evidence or
Advisor payload. Do not invoke the canonical validator, emit eligibility, create/
validate/consume a release, run public analyzer, access network/credentials or
touch any device/camera/light/formal/science route.

Any precondition, implementation, gate, commit or postcommit failure stops at the
unique Planner stop and returns for a bounded review. No same-execution repair,
retry, fallback, alternate root or additional commit is permitted.

## 维护性判断

The correction remains within one pure helper and its dedicated regression owner.
It hardens exact provenance semantics without widening production, validator or
eligibility ownership. No follow-up refactor is authorized in this package.
