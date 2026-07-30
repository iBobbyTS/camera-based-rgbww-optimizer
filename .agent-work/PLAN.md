# REF-P7-25-R2-B2-C4-P2-C1：pretest scope gate correction

**计划状态：** `EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P2-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C1-PRETEST-SCOPE-GATE-CORRECTION-V1`

**当前唯一动作：** 保留现有未跟踪 integration test 的精确字节，使用一个可审计、
NUL-safe 的 tracked-plus-untracked Git classification owner 修正 pretest singleton
scope gate；gate 通过后从首次 targeted test 继续原 P2 尚未执行的 ordered gates。
不得重新创建、编辑或提前 stage 该测试，不得重跑已通过的 preconditions。

**唯一 Planner stop：**
`B2_C4_P2_C1_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1303-p7-retained-r3-option-b-b2-c4-p2-pretest-gate-failure-review.md`，
bytes `6333`，SHA-256
`a4f584e8de4a92e034424fd8d801a50ec32837f51e0530c499c8b9e453a41857`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_c1_pretest_scope_gate_correction_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C1-PRETEST-SCOPE-GATE-CORRECTION-V1","execution_authorized":true,"dispatch_state":"ready_after_orchestrator_activation_commit","single_current_action":"validate_preserved_untracked_singleton_then_resume_unrun_p2_gates","preserved_test":{"path":"tests/test_p7_retained_r3_controller_integration.py","bytes":13147,"sha256":"106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d","git_state":"untracked_regular_file","edit_budget":0,"recreate_budget":0},"scope_owner":"nul_safe_tracked_plus_untracked_union_without_intent_to_add","orchestrator_activation":{"expected_base":"e45cf6a70204d87a5b4b47f19149e80e087cb634","required_subject":"chore(plan): activate retained r3 pretest gate correction","test_must_remain_exact_untracked":true,"implementation_parent":"full_activation_commit_sha_frozen_at_dispatch"},"exact_changed_paths":["tests/test_p7_retained_r3_controller_integration.py"],"implementation_commit_subject":"test(p7): qualify retained r3 controller composition","historical_c4_reads":0,"retained_r3_reads":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"commit_budget":1,"retry_budget":0,"planner_stop":"B2_C4_P2_C1_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and bounded correction

The reviewed P2 result is
`REJECTED_GATE_DEFECT_IMPLEMENTATION_NOT_EVALUATED`. The test implementation
did not fail: no test was invoked. The failed gate required ordinary
`git diff --name-only` to list a newly created untracked path, which Git does not
do. Ordinary `git diff --check` likewise does not inspect that untracked file.

P2-C1 changes only the observation contract:

- tracked index/worktree paths and untracked paths are classified separately
  with NUL-delimited Git output and combined as an exact set;
- the sole untracked file is validated by lstat, bytes, SHA-256 and a no-index
  whitespace check without `git add -N`;
- after this corrected gate, execution resumes at the original first targeted
  test and retains all subsequent P2 requirements and budgets.

This package must not repair test behavior speculatively. If the first targeted
test fails, preserve the exact file, append one truthful failure handoff and
stop. No retry or edit is authorized.

## 2. Frozen preserved implementation and activation topology

The preserved implementation path is exactly:

```text
tests/test_p7_retained_r3_controller_integration.py
```

At Planner review it is an untracked regular file, bytes `13147`, SHA-256
`106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`.
It must remain byte-for-byte unchanged through activation, the corrected gate,
all precommit tests and CodeGraph. Its edit, recreation, delete/restore,
formatter and generation budgets are all `0`.

Orchestrator activation must have exact parent
`e45cf6a70204d87a5b4b47f19149e80e087cb634` and exact subject
`chore(plan): activate retained r3 pretest gate correction`. The activation may
commit only Orchestrator/Planner-owned planning and evidence metadata required
to cleanly activate this correction; it must not stage or commit the test or
change any production/test source. Immediately after activation, the test must
still be the exact sole untracked path and the tracked/index worktree must be
clean. The full activation SHA is the immutable implementation parent.

The following already-passed P2 facts are accepted evidence and must not be
re-executed:

- activation/precondition check of the original P2 parent;
- PLAN/FULL/input SHA/accepted-commit ancestry preflight;
- initial clean-worktree check;
- creation of the integration test.

The accepted production/test owners remain read-only at their frozen committed
identities:

| Path | Required SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

These hashes are frozen inputs, not a license to rerun the previous full
preflight. A mismatch observed incidentally is a hard stop, not a repair branch.

## 3. Corrected pretest scope owner

Before any test, perform this gate exactly once without modifying the index:

1. Read the current HEAD once and require the frozen Orchestrator activation
   topology and active P2-C1 machine contract. Do not repeat the superseded P2
   FULL/input/precondition suite.
2. Use `lstat` without following symlinks and require the preserved path to be a
   regular file with exact bytes and SHA-256 from section 2.
3. Parse `git status --porcelain=v1 -z --untracked-files=all` as NUL-delimited
   bytes. Require exactly one record, `?? ` plus the exact test path. Reject
   renames, quoting ambiguity, additional records and any tracked/index change.
4. Independently parse `git diff --name-only -z --` and
   `git diff --cached --name-only -z --`; require both tracked sets empty. Parse
   `git ls-files --others --exclude-standard -z --`; require its untracked set
   to equal the exact singleton test. The union must equal the singleton and the
   classifications must be disjoint.
5. Run
   `git diff --no-index --check -- /dev/null tests/test_p7_retained_r3_controller_integration.py`
   once. Because the file is new, require exit `1` with no whitespace-error
   output. Any other exit or diagnostic fails closed. Do not use ordinary
   `git diff --check` as evidence for the untracked content.

`git add -N`, intent-to-add, staging, stash, checkout, reset, clean, formatter,
content rewrite and alternate scope commands are prohibited at this gate. On a
mismatch, append one truthful P2-C1 failure handoff without editing the test and
stop.

## 4. Frozen integration behavior

The preserved test must still substantively exercise the actual public APIs of
the existing exact-five lifecycle and accepted preparation owner. Acceptance
requires observable assertions for:

1. success composition with exact callback order, five materializations,
   prepared-source identity, canonical terminal target validation, immutable
   gate payload, synthetic validator call and one post-seal ER admission;
2. preparation failure before all lifecycle/terminal/ER callbacks;
3. one pre-terminal lifecycle failure, later-phase suppression, exactly one
   canonical failure terminal and ER admission only after target validation;
4. wrong type or value in the seal target failing before ER with no fallback;
5. no import/call of the real canonical validator, retained/release owner,
   filesystem/process/network/environment or device owner.

The callback field named `canonical_validator` must remain an inline in-memory
exact-bool stub. Its invocation count is recorded separately; actual canonical
validator import/call count remains `0`. The test must not reproduce either
production owner implementation.

## 5. Zero budgets and hard locks

The original P2 preconditions and source creation already occurred once; their
rerun budgets are `0`. This correction has retry/fallback/edit/recreation
budgets `0`.

| Operation | Remaining budget |
| --- | ---: |
| corrected pretest scope gate | 1 |
| new targeted test, precommit | 1 |
| existing two-owner combined suite | 1 |
| focused retained-controller group | 1 |
| full unittest suite | 1 |
| compileall | 1 |
| CodeGraph sync | 1 |
| implementation commit | 1 |
| new targeted test, postcommit | 1 |
| test edit/recreate/delete-restore/formatter | 0 |
| amend/rebase/fixup/second commit | 0 |
| historical C3/C4/failed-root reads | 0 |
| retained R3 candidate/artifact reads | 0 |
| real B2/controller dispatch | 0 |
| actual canonical validator import/call | 0 |
| eligibility emission/consumer | 0 |
| lineage/release create/validate/replay/consume | 0 |
| external root or temporary evidence file | 0 |
| network, DNS, `.env`, credentials | 0 |
| device/camera/Ray/strip/cleanup/capture/FORMAL | 0 |
| public analyzer, TD-C, sentinel, P8, firmware/deployment | 0 |

This remains a local sub-10-minute code/test package. Visible Terminal,
automation, device authorization and Advisor input are not implicated.

## 6. Ordered continuation gates

After section 3 passes, execute exactly once in this order. Any failure stops
without test repair, retry, fallback or commit:

1. Run the new integration test alone:
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration -v`.
2. Run the two existing owner suites together:
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation -v`.
3. Run the focused group once:
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_release_audit -v`.
4. Run the full suite once:
   `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v`.
5. Run compileall once:
   `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests`.
6. Run `codegraph sync` once and require success. Recompute lstat/bytes/SHA and
   the corrected tracked-plus-untracked gate; the test must still be the exact
   unchanged singleton. Repeat the no-index whitespace check once as this
   post-validation scope check, not as a retry.
7. Freeze implementation parent full SHA, absent-before/new-after Git blob OIDs,
   file SHA-256 and canonical binary Git patch SHA-256. Only now run
   `git add -- tests/test_p7_retained_r3_controller_integration.py`. Require the
   staged NUL-delimited path set to equal the singleton, unstaged path set empty,
   `git diff --cached --check` success, and the staged blob/patch identities to
   match the frozen values.
8. Create exactly one commit with subject
   `test(p7): qualify retained r3 controller composition` and a concise detail
   describing existing-owner callback composition.
9. Verify exact direct parent, subject, singleton tree change, absent-before and
   after blob, file and patch identities, plus zero implementation drift. Run
   the new targeted test alone once as the sole postcommit test.
10. Append one truthful P2-C1 handoff to `.agent-work/EXECUTION_RESULT.md`.
    Record preserved identity, corrected union classification, every ordered
    count/result, synthetic-stub and actual-validator counts, commit identity,
    explicit zero budgets and the unique stop. Do not edit PLAN/FULL/archive.

If a precommit gate fails, do not stage or commit. If staging, commit or
postcommit verification fails, do not amend, repair or create a second commit.
In every terminal branch, preserve the test/commit state, append at most one
truthful handoff and stop.

## 7. Acceptance and stop

Planner may accept P2-C1 only if:

- activation preserved the exact untracked test and the corrected NUL-safe
  tracked-plus-untracked singleton gate passed without intent-to-add;
- the test remained at exact bytes/SHA until its one authorized staging step;
- all substantive integration behaviors in section 4 passed through both real
  public owners;
- targeted, owner, focused, full, compileall, CodeGraph, diff/staging and
  postcommit gates passed at exact budgets;
- the child has the frozen parent, exact subject, singleton tree change and
  exact file/blob/patch identities;
- actual validator, eligibility, release, historical, retained, network,
  device and external-root counters remain zero;
- one ER handoff records the unique stop
  `B2_C4_P2_C1_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

Success unlocks only Orchestrator review for the next provenance-bound C4
package. It does not unlock retained R3, real B2, the canonical validator,
eligibility, release consumption or device/scientific work.

## 维护性判断

The correction changes no implementation and adds no owner. It replaces an
inapplicable Git observation with one explicit path-classification boundary,
then reuses the original validation sequence. No follow-up refactor is needed.
