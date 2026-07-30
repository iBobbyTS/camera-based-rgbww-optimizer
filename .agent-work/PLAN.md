# REF-P7-25-R2-B2-C4-P1：repo-owned controller preparation owner

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_PURE_OFFLINE_IMPLEMENTATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-REPO-OWNED-PREPARATION-V1`

**当前唯一动作：** 新增一个 repo-owned、pure、typed 的 retained-R3
controller-preparation helper 及其 dedicated test，完成全部离线验证并形成一个
exact-two-path focused commit；不得集成或执行任何历史 controller。

**唯一 Planner stop：**
`B2_C4_P1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**Superseded architecture-stop archive：**
`.agent-work/PLANS/20260730-1217-p7-retained-r3-option-b-b2-c4-p1-architecture-route-review.md`
（bytes `4072`，SHA-256
`0a7d4a537de43de2369ead2fa4a83438d4ee3e3ad037f4f955e6b825857b258a`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p1_repo_owned_preparation_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-REPO-OWNED-PREPARATION-V1","dispatch_state":"dispatchable_after_orchestrator_activation_review","execution_authorized":true,"pure_offline":true,"single_current_action":"implement_test_validate_and_commit_repo_owned_controller_preparation_owner","exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py","tests/test_p7_retained_r3_controller_preparation.py"],"expected_initial_path_state":"both_absent","direct_io_allowed_in_helper":false,"canonical_validator_remains_sole_eligibility_owner":true,"old_external_owner_reuse":false,"historical_artifact_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"device_operations":0,"commit_budget":1,"commit_subject":"feat(p7): add retained r3 controller preparation owner","required_gates":["targeted","focused","full","compileall","codegraph_sync","diff_check","exact_two_path_commit","postcommit_targeted"],"failure_branch":"bounded_p1_correction_waiting_planner_review","planner_stop":"B2_C4_P1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Frozen start and authorization boundary

At planning time the worktree was clean at
`253567fe9c92a43046d46a07e21752d8f30f7a23`, and both target paths were absent.
The Orchestrator may commit this PLAN/archive before dispatch. Therefore the
Executer must, before editing:

1. record the dispatch-time full HEAD as `implementation_parent`;
2. require a clean worktree;
3. require both exact target paths still absent;
4. require the active PLAN reference task and contract ID above;
5. stop without editing if any condition differs.

This PLAN authorizes only local repository source/test work, offline tests,
CodeGraph sync, one focused commit and an `EXECUTION_RESULT.md` handoff. It does
not authorize a package/evidence root, external controller, retained evidence,
release, validator, analyzer, network or device operation.

## 2. Exact repository scope

The only files that may be created or changed by the implementation commit are:

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py
tests/test_p7_retained_r3_controller_preparation.py
```

No package export, production runner, validator, audit helper, wrapper, docs,
skill, config, PLAN, FULL reference or archive may be changed by the Executer.
The Executer may append its truthful handoff to
`.agent-work/EXECUTION_RESULT.md`; that Planner evidence append is not part of
the implementation commit.

Before implementation, use CodeGraph to inspect the repo-owned convention in
`p7_retained_r3_exact_five_controller` and its dedicated test. The new helper
must be a separate, narrow source-preparation owner rather than expanding the
canonical lineage validator or introducing a second eligibility owner.

## 3. Pure helper contract

Implement the smallest typed boundary that proves all of the following without
direct I/O:

### 3.1 AST/source preparation

- Parse supplied source bytes/text with Python AST and preserve an explicit
  parent-edge map.
- Locate the unique enclosing function owner through ancestor edges; reject
  cross-function, lambda, async/alternate owner, zero-owner and multiple-owner
  ambiguity.
- Require the target assignment and its cardinality/validation statement to be
  adjacent members of the same immediate AST list field. A direct-parent
  `FunctionDef` assumption is forbidden.
- Select/replace by validated UTF-8 byte spans, including same-line columns and
  non-ASCII prefixes; reject invalid, reversed, overlapping, out-of-range,
  zero-match or multiple-match spans.
- If the helper emits prepared source, it must be deterministic and must pass
  both `ast.parse` and `compile` before it can be returned. Do not generate or
  embed another large/nested one-shot Python program.

### 3.2 Canonical terminal bytes and linkage

- Canonical JSON is UTF-8, duplicate-key/non-finite rejecting on strict reload,
  deterministically serialized, and terminated by exactly one byte `LF`.
- Reject literal `\\n`, CRLF, missing LF, extra LF, invalid UTF-8,
  noncanonical key/spacing/number representation and bytes that do not
  round-trip to the same canonical payload.
- Model target identity explicitly with exact path, bytes, SHA-256, device and
  inode fields. A valid seal must link to all expected target fields; any wrong,
  absent or rebound field rejects the gate.
- Hashing/parsing/serialization may operate only on caller-supplied in-memory
  values. The helper must not stat, open, read, write, rename or fsync paths.

### 3.3 ER gate dominance

- Represent successful seal validation with a typed, non-forgeable-in-normal-use
  gate/result object created only by the validation path.
- Success and failure terminal flows must both require that valid gate before an
  injected ER callback can be invoked.
- Invalid terminal bytes, canonical mismatch, target mismatch, callback setup
  error before the gate, or seal-validation failure must leave ER callback call
  count at `0`.
- The helper must preserve the primary exception/result semantics; a callback
  must not turn a rejected seal into success.

The module may import pure standard-library facilities such as `ast`,
`dataclasses`, `hashlib`, `json` and typing helpers. Direct filesystem, Git,
subprocess, socket/network, environment, camera, device, release, validator or
analyzer imports/calls are forbidden.

## 4. Dedicated regression contract

The dedicated test file must assert behavior, not merely execute lines. At a
minimum cover:

1. direct, nested and double-nested valid AST ownership;
2. cross-function, lambda, async/alternate, zero and multiple owner rejection;
3. same-list adjacency success and different-list/non-adjacent rejection;
4. same-line columns, UTF-8 byte offsets, boundary spans, overlap, reversed,
   out-of-range, zero and multiple matches;
5. deterministic prepared output plus `ast.parse` and `compile` success;
6. canonical success with exactly one final LF;
7. literal-backslash-n, CRLF, missing/extra LF, invalid UTF-8,
   duplicate-key, non-finite and noncanonical JSON rejection;
8. wrong path, bytes, SHA-256, device or inode rejection;
9. valid success-terminal and failure-terminal ER callback sequencing;
10. invalid-seal paths with ER callback count exactly `0`;
11. static source assertion that the helper has no direct I/O or forbidden
    imports and does not contain a nested large generated program.

Tests must use only synthetic in-memory fixtures. They must not read old C4
controllers/artifacts, retained R3 or release evidence.

## 5. Ordered validation gates

Run each gate once in this order; retry and fallback are `0`. Record exact
command, exit code and test count in `EXECUTION_RESULT.md`.

1. **Targeted:**

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_r3_controller_preparation.py' -v
   ```

2. **Related focused:** run the targeted command plus each existing related
   suite exactly once:

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_r3_exact_five_controller.py' -v
   .venv/bin/python -m unittest discover -s tests -p 'test_p7_retained_release_audit.py' -v
   ```

3. **Full suite:**

   ```sh
   .venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
   ```

4. **Compile:**

   ```sh
   .venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests
   ```

5. **CodeGraph:** run `codegraph sync` at repository root and require success.
6. **Repository checks:** run `git diff --check`; require the unstaged/staged
   implementation path set to equal the exact two-path set and no other path.

Any gate failure stops immediately. Do not repair during the same execution,
rerun a failed gate, relax a test, add a third path or continue to commit.

## 6. Focused commit and postcommit gate

Only after all precommit gates pass:

1. stage exactly the two implementation paths;
2. require the staged path set equals the exact sorted two-path set;
3. create exactly one commit with exact subject
   `feat(p7): add retained r3 controller preparation owner`;
4. require the commit parent equals the recorded `implementation_parent`;
5. require the commit changed-path set equals the exact two paths and each is a
   new regular repository file;
6. require no amend, rebase, second commit or unrelated staged change;
7. rerun the targeted command exactly once against committed bytes;
8. run `git diff --check` and require no implementation-scope worktree drift.

If commit creation or any postcommit check fails, preserve the commit if one was
created, do not amend it, and stop for Planner review.

## 7. Required handoff

Append one bounded section to `.agent-work/EXECUTION_RESULT.md` containing:

- reference task, contract ID, implementation parent and child full SHA;
- exact changed paths and commit subject;
- concise API/ownership description;
- dedicated test case inventory;
- each precommit/postcommit command, exit code and exact test count;
- compileall, CodeGraph sync and diff-check results;
- static forbidden-I/O/import result;
- explicit zero counters for old C4/retained-R3 reads, external controller,
  canonical validator, eligibility, release, public analyzer, network, `.env`,
  device, camera, Ray, strip, cleanup, capture and formal;
- residual maintainability judgment and exact Planner stop.

Do not edit either plan file or any archive. After the handoff, stop at
`B2_C4_P1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW`; P1 success does not
authorize C4 integration, real B2, retained-R3 audit, B3, eligibility, release
consumption or device work.

## 8. Failure branches and hard locks

On any precondition, implementation, test, static, CodeGraph, diff, commit or
postcommit failure, append truthful failure facts if possible and stop at the
same unique Planner stop. The next package, if any, is a bounded P1 correction;
the failed external-owner chain must remain closed.

Throughout this package, do not read, import, compile, execute, repair or reuse:

- any C4, C4-C1 or C4-C1-C1 external source, builder, root or artifact;
- retained-R3 candidates/artifacts or any release/evidence root;
- Advisor decision payloads or historical GUIDE evidence not already frozen in
  this PLAN.

Do not invoke the canonical lineage validator, emit eligibility, create/validate/
consume a release, run the public analyzer, access network/`.env`/credentials or
touch any device, camera, Ray, strip, cleanup, capture, FORMAL-R6, TD-C, sentinel
or P8 route.

## 维护性判断

This package creates one narrow pure owner and one dedicated regression owner;
it does not modify production execution, validation or eligibility boundaries.
The callback/seal API must stay small and typed, with historical integration
deferred to a separate provenance-bound package after Planner acceptance.
