# P7 retained-R3 B2 P5 repo-owned runtime owner review

**Review time:** `2026-07-31T15:37:45-0600`

**Reviewed reference task:** `REF-P7-25-R2-B2-P5`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-REPO-OWNED-CONTROLLER-RUNTIME-OWNER-V1`

**Implementation commit:** `37f7d0021c7a81a9d6680815bc51c305cf807a7b`

**Evidence commit:** `2cb1f2c6538d44d9bf002a570e2852b763feae07`

## 1. Frozen scope and repository reality

Planner independently reviewed the clean `main` worktree at evidence HEAD `2cb1f2c6538d44d9bf002a570e2852b763feae07`.
The activation commit is exact:

- commit `099d1ad833c3e73b7dc157f5786ad66bb6718f5e`;
- direct parent `ec2dd705fbcf3349297fb141b732ebc9b61aaf94`;
- subject `chore(plan): activate p5 controller runtime owner`;
- exact changed paths FULL, PLAN and
  `.agent-work/PLANS/20260731-1521-p7-retained-r3-b2-p4-runtime-token-successor-architecture-review.md`.

The implementation is one exact two-path commit with direct parent equal to the activation commit and subject
`feat(p7): own retained controller runtime`:

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py` — blob
   `075face6fd7453236affa303640b91eb16a42a9b`, bytes `12320`, SHA-256
   `07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2`;
2. `tests/test_p7_retained_r3_controller_runtime.py` — blob
   `a6aa7d7caf015e2eb858830dc89aaedaeb51aafa`, bytes `12021`, SHA-256
   `66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782`.

Evidence commit `2cb1f2c` changes only `.agent-work/EXECUTION_RESULT.md`, adding one truthful 16-line P5 handoff.
No source/test edit occurred after implementation commit and the worktree was clean at review start.

## 2. Intent, ownership and critical path reviewed

The accepted intent is one narrow outer runtime envelope, not a retained validator or a second controller framework. Planner traced the
critical path end to end:

`ControllerRuntimeRequest` → `prepare_controller_source` → existing `analyze_controller_source` exact once → exclusive
`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW` mode-`0600` complete write → descriptor identity/file fsync/close → no-follow parent
descriptor identity/fsync → existing `read_exact_file` exact readback → exact-one `subprocess.run(input=verified bytes,
shell=False, check=False)` → immutable `exit_code` report.

The owner boundary is accepted:

- preparation remains the deterministic strict-UTF-8/AST/compile and byte-replacement owner;
- conformance remains the sole AST/reflection/transport/forbidden-attribute analyzer;
- provenance I/O remains the no-follow physical readback owner;
- lifecycle, PLAN/FULL parsing, retained interpretation, canonical validation, eligibility, release and devices are absent;
- the new module does not contain regex/token/path/generic allowlists, a second analyzer, a second lifecycle, a retained schema or a
  PLAN-specific matrix.

The source persistence path is fail closed for existing targets, symlinks, incomplete/no-progress writes, fsync/close/parent failures,
mode/type/identity/readback/hash drift. It neither rewrites nor deletes a failed target and never launches before conformance,
persistence and readback all pass. The launcher has one input channel, no `stdin` key, one process, no retry and converts the process
boundary's `returncode` into the repo report's truthful `exit_code`; forbidden `.returncode` remains rejected inside controller source.

## 3. Regression and validation evidence

The dedicated surface contains exact six meaningful methods:

1. deterministic immutable bytes/report plus strict UTF-8, AST and compile;
2. existing-analyzer reflection rejection before every write/read/process effect, counters `1/0/0/0`;
3. exact flags/mode, partial-write and EINTR recovery, file-close-parent fsync ordering, identity/readback;
4. existing/symlink/no-progress/file+parent-fsync/readback-drift fail-closed matrix with launch `0` and preserved originals;
5. exact-one launcher mapping, bytes stdout/stderr, immutable exit report, invalid result and launch exception without retry;
6. positive `GitLedger.exit_code`, existing-owner-only forbidden attribute/reflection rejection and static import/export/ownership
   boundary.

The ordered Executer validation is internally consistent with the committed topology:

- targeted `6/6`, exit `0`, `OK`;
- focused runtime/preparation/conformance/provenance-I/O/integration `76/76`, exit `0`, `OK`;
- exact new-module compileall exit `0`;
- unique full suite unified session `19758`, `767/767`, `Ran 767 tests in 158.159s`, exit `0`, final `OK`;
- `codegraph sync` exact once, `Already up to date`, and one owner query confirming the critical call path and no lifecycle/second
  analyzer;
- `git diff --check`, staged diff, exact method/path gates passed;
- postcommit targeted `6/6`, exit `0`, `OK`.

Planner did not rerun tests or any external operation. Independent read-only source and CodeGraph review corroborated the ownership,
ordering and commit/hash claims. The test-owned files were limited to temporary directories under
`/Volumes/4T/temp/rgbww-optimizer` and cleaned by test lifecycle; they are not a synthetic external dispatch.

## 4. Findings and decision

No actionable `Must Fix`, `Should Fix` or `Needs Decision` finding remains. Baseline correctness, failure atomicity, filesystem/process
trust boundary, architecture/single-owner discipline, validation integrity and AI-authored scope drift lenses were reviewed. No reset
event occurred.

**Planner decision:** `ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER`.

This accepts the P5 implementation as mergeable/current and closes the repeated disposable source-writer/launcher architecture gap.
It does not accept a synthetic integration, does not read or validate retained R3, and does not emit eligibility or make any release
consumable. Retained status remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## 5. Residual risk and exact next branch

The runtime owner has only unit/focused/full validation; it has not yet driven the complete external synthetic Git6/four-input/
matrix16/exact9/terminal lifecycle. That operational integration is the sole material residual risk before returning to the B2/B3
provenance route.

Exact next branch:

- reference `REF-P7-25-R2-B2-P5-I1`;
- contract
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-I1-REPO-RUNTIME-FRESH-SYNTHETIC-INTEGRATION-V1`;
- one fresh source/root/process only, using `execute_controller_runtime` as the exclusive source preparation, conformance,
  persistence/readback and process-launch owner;
- no handwritten external source writer/reader/launcher, no second analyzer/classifier and no parallel lifecycle;
- retained/candidate reads, real B2, canonical validator, eligibility, release, network and devices remain exact zero.

All failure branches preserve fresh evidence, use retry/fallback/second source/root/process `0`, append one truthful ER record and stop
at Planner review. A successful synthetic qualification proves only the repo runtime consumer route; it cannot itself unlock retained
consumption.

**Planner stop:** `B2_P5_ACCEPTED_WAITING_ORCHESTRATOR_P5_I1_ACTIVATION`.

维护性判断：P5 把反复漂移的 source persistence/process launch 收敛到唯一 owner，保留 preparation、conformance、provenance-I/O
与 lifecycle 的既有职责。六个回归和完整套件覆盖该高风险边界；下一步应只做一次 fresh consumer integration，不再新增抽象或一次性 writer/launcher。
