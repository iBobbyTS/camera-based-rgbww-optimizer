# REF-P7-25-R2-B2-C2：content-free controller 与 failure lifecycle 纠偏

**计划状态：** `PLANNER_COMPLETE_WAITING_ORCHESTRATOR_REVIEW`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C2-CONTENT-FREE-CONTROLLER-LIFECYCLE-CORRECTION-V1`

**预计时长：** `3–8 分钟`；纯离线，不属于预计超过10分钟的长任务。

**当前唯一动作：** 在 Orchestrator 独立接受失败 review、更新 FULL 并由 Planner 另行做一次 PLAN-only activation 后，Executer 才可用一次本地 builder invocation，在一个 brand-new external correction root 中消费冻结的失败 controller source，生成一个 immutable successor controller；仅用 content-free in-memory fixtures 与 correction-root 内的 injected-writer fixtures 验证 exact resolved-record owner、progressive failure terminal/seal 和 seal-before-ER sequencing，然后 durably seal C2 evidence 并 append 一次 ER。

**当前 Planner stop：**
`B2_CORRECTED_FAILURE_REVIEWED_WAITING_ORCHESTRATOR_REVIEW`。

**未来 C2 execution stop：**
`B2_C2_CONTROLLER_CORRECTION_WAITING_PLANNER_REVIEW`。

本文件当前 `execution_authorized=false`。不得据此创建 root、写 builder/source、运行 self-check，或执行任何 controller。只有未来 exact PLAN-only activation commit 把状态改为 `EXECUTION_AUTHORIZED` 并冻结 dispatch parent/subject/path topology 后，Executer 才可执行一次。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1021-p7-retained-r3-option-b-b2-corrected-manifest-failure-review.md`，bytes `9782`，SHA-256 `9317f2953b39cab6d847728fb14e69516481376283fc90b4a2b8fee0dbb39ed0`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c2_controller_correction_plan_v1","reference_task_id":"REF-P7-25-R2-B2-C2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C2-CONTENT-FREE-CONTROLLER-LIFECYCLE-CORRECTION-V1","dispatch_state":"waiting_orchestrator_review","execution_authorized":false,"single_current_action":"build_and_validate_content_free_successor_controller_and_failure_lifecycle","activation":"pending_future_plan_only_commit","review_archive":{"path":".agent-work/PLANS/20260730-1021-p7-retained-r3-option-b-b2-corrected-manifest-failure-review.md","bytes":9782,"sha256":"9317f2953b39cab6d847728fb14e69516481376283fc90b4a2b8fee0dbb39ed0"},"rejected_controller":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py","bytes":29841,"sha256":"da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4"},"failed_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-corrected-manifest-b189117-20260730T1600Z","expected_direct_entries":0,"reuse":false},"future_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c2-controller-correction-da90556-20260730T1621Z","builder_invocations":1,"successor_real_input_invocations":0,"c1_evidence_reads":0,"retained_artifact_reads":0,"decision_source_reads":0,"retry":0,"fallback":0,"planner_stop":"B2_C2_CONTROLLER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Review decision and authority boundary

1. Reviewed B2 V3 is rejected as
   `REJECTED_C1_RESOLVED_PATH_STRUCTURE_AND_FAILURE_LIFECYCLE_MISMATCH`.
   The frozen controller incorrectly required the entire three-path array to
   occur as one JSON node and had only a success persistence path; its outer
   exception handler printed stderr and re-raised.
2. The failed invocation safely stopped after exact C1 evidence read/hash
   `4/4/4/4`, before retained access, self matrix, manifest, terminal, seal,
   ER append, validator, release, devices, or scientific stages. Its empty root
   is immutable failed-run evidence and must not be reused, deleted, renamed,
   repaired, or populated.
3. C1 remains accepted only as path/type ownership evidence; it is neither
   eligibility nor artifact-content validation. Retained state remains
   `RETAINED_UNVALIDATED_UNCONSUMED`.
4. C2 is an external controller-source and lifecycle correction only. It may
   not run corrected B2 against real inputs and cannot unlock B3, canonical
   validator, eligibility, release, devices, FORMAL-R6, strip, TD-C, sentinel,
   or P8.
5. This is an Orchestrator-owned engineering/provenance question. No unresolved
   color/measurement science and no dangerous device operation are present;
   Advisor/Human authorization is not required.

## 2. Frozen inputs and zero-content boundary

After future activation, the sole builder may consume exactly these inputs:

1. Rejected controller source:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py`,
   expected bytes `29841`, SHA-256
   `da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4`.
   It gets exactly one non-following `lstat`, one
   `O_RDONLY|O_NOFOLLOW` open, one bounded read, one before/after `fstat`
   identity comparison, and one SHA-256 computation.
2. Failed root metadata only: exact path in the machine contract. It gets one
   non-following directory `lstat` and one direct `scandir`; it must remain
   mode `0700`, inode `2188351`, and have zero direct entries. No child path is
   opened and the directory is not mutated.
3. Active PLAN/Git dispatch metadata required by the future activation. The
   builder may use read-only Git plumbing to prove exact activation parent,
   subject, sole changed path `.agent-work/PLAN.md`, active PLAN blob hash, and
   clean worktree before root creation.

Forbidden inputs and access counts are exact zero:

- all four C1 evidence files, including lstat/open/read/hash/parse;
- all three retained-R3 artifacts and their parent/sibling directories;
- GUIDE, Advisor attachment/decision evidence, release decision sources;
- canonical validator/helper/consumer/replay and production imports;
- network, DNS, `.env`, credentials, devices, camera, Ray, strip, cleanup,
  capture, CR3/NPY, FORMAL, public analyzer, TD-C, sentinel, P8;
- tests, compileall, CodeGraph, release generation/copy/consumption;
- rejected-root reuse/repair and basename/glob/walk/search fallback.

The existing accepted C1 review archive and this PLAN freeze semantic test
fixtures; they do not authorize reading the C1 payload again. Any future real
B2 invocation needs a newly explicit one-time C1 evidence read budget in a new
PLAN after C2 acceptance.

## 3. Brand-new correction root and single builder

1. Exact future root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c2-controller-correction-da90556-20260730T1621Z`.
   It must be absent immediately before one builder creates it mode `0700`.
   No precreation, alternate timestamp/root, reuse, delete, rename, repair,
   second root, retry, fallback, or second builder is allowed.
2. Executer may author one disposable builder source outside the repository and
   under `/Volumes/4T/temp/rgbww-optimizer`; freeze its exact bytes/SHA before
   the single invocation. The builder and output successor are evidence, not
   repository production code.
3. The builder owns input read, exact source transformation, syntax compile,
   content-free self-checks, fixture subprocesses, canonical no-clobber writes,
   fsyncs, strict reloads, correction terminal, and terminal seal.
4. Repository source/tests/config/docs/skills/wrappers/GUIDE/FULL/archives/PLAN
   are read-only. After the physical C2 terminal seal, Executer may append one
   C2 handoff to `.agent-work/EXECUTION_RESULT.md`; implementation edit and Git
   commit remain `0/0`.

## 4. Exact successor-controller correction

The builder must emit one
`p7-td-b-b2-corrected-controller-successor.py` by mechanically modifying only
the following two semantic regions of the rejected source. It must also emit a
binary-safe `successor-controller.patch` binding old/new source hashes and
showing no other behavior drift.

### 4.1 Exact resolved-record owner

Replace `contains(index, expected_paths)` as the path-owner predicate with one
named helper that extracts only record-shaped nodes and proves all of these:

1. exactly three candidate resolved records exist, no fourth candidate;
2. each candidate is a dictionary with an exact absolute `path` string;
3. the candidate path multiset equals the three PLAN-frozen exact absolute
   paths, each exactly once—no duplicate, missing, extra, abbreviated, relative,
   basename-only, prefix, glob, parent/sibling, or substitute path;
4. every candidate has exact
   `content_identity=not_observed_by_this_package` and
   `current_content_validated=false`;
5. unknown extra key/value content may not grant authority; nested unrelated
   dictionaries or strings may not be counted as resolved records;
6. after proving the exact record set, later artifact processing uses the
   PLAN-frozen three-path order. It does not infer read order from dictionary
   traversal, generic substring membership, or filesystem discovery.

The helper must fail closed on wrong type, duplicate record, duplicate path,
missing/extra record, wrong sentinel fields, path hidden only in an unrelated
node, a synthetic whole-list node without valid records, and bool/int aliasing.
It must not parse or validate retained artifact content.

### 4.2 Single post-root terminal lifecycle owner

Restructure the successor so that successful root creation immediately enters
one lifecycle owner enclosing all subsequent C1, retained, decision, Git,
manifest, and terminal work. The successor must define exact immutable
progressive stages written with no-clobber/canonical/fsync/reload semantics:

1. `progressive-00-root-created.json` after root identity is verified;
2. `progressive-01-inputs-validated.json` only after all future input identity
   checks return;
3. `progressive-02-artifacts-validated.json` only after future retained byte
   provenance returns;
4. `progressive-03-manifest-sealed.json` only after manifest and manifest-seal
   writers return.

On any exception after root creation, the lifecycle owner must:

- preserve all earlier files unchanged;
- capture the exact failing stage, exception type/message, actual counters,
  root and source identities, last durable progressive stage, and all locked
  operation zeros;
- write exactly one truthful `terminal-evidence.json` with status
  `hard_failure_waiting_for_planner`;
- after terminal writer return, write exactly one
  `terminal-evidence.sha256.json` binding physical bytes/hash/schema/status,
  `terminal_write_returned=true`, and
  `terminal_seal_self_write_return=not_self_attested`;
- expose an ER handoff payload only after terminal-seal writer return.

Success uses the same owner and physical ordering, with status
`pass_waiting_for_planner`. The ER append owner must verify the physical
terminal/seal link immediately before its sole append. If progressive,
terminal, or seal persistence itself fails, it must never claim pass, never
invent a seal, never append ER, never rewrite/repair/replace an existing file,
and must exit nonzero. Stderr alone is diagnostic and not acceptance evidence.

The source must retain all existing C1/retained/decision/Git identities,
modern baseline computation, manifest schema, eligibility locks, and later-stage
locks byte-for-byte outside these two correction regions except mechanical
imports/counters/fixture entry-point wiring required by this contract.

## 5. Content-free validation matrix

The successor may be invoked only in a dedicated
`--content-free-self-check` mode. This mode must reject any real C1/retained
path arguments, never enter real `main()`, and use only in-memory JSON objects
plus fixture directories below the C2 root. At least these `18/18` behavioral
cases must pass:

### Resolved-record cases (`10/10`)

1. positive three-record fixture with each path in a separate record;
2. valid records in unrelated nesting still yield the frozen order;
3. old synthetic whole-list-only representation is rejected;
4. duplicate record rejected;
5. duplicate path plus missing path rejected;
6. fourth candidate record rejected;
7. missing sentinel field rejected;
8. wrong `content_identity` rejected;
9. `current_content_validated=true` rejected;
10. basename/prefix/unrelated-node path authorization rejected.

### Lifecycle cases (`8/8`)

11. post-root path-schema failure writes failure terminal then seal and exposes
    exactly one ER payload;
12. future input-stage injected failure preserves root progressive stage and
    writes failure terminal/seal;
13. artifact-stage injected failure preserves prior stages and writes failure
    terminal/seal;
14. post-manifest-seal injected failure leaves manifest/seal unchanged and
    writes failure terminal/seal;
15. terminal-writer injection yields no seal and no ER payload;
16. terminal-seal-writer injection preserves terminal and yields no ER payload;
17. duplicate/existing target yields no rewrite/repair and no ER payload;
18. success path orders progressive stages, terminal, seal, then one ER payload.

Fixtures must verify exact file sets, canonical bytes, schemas/statuses, hashes,
counter snapshots, return ordering, no-clobber behavior, unchanged-file hashes,
and ER exposure count. They may not call real Git beyond dispatch verification,
real C1/retained/decision sources, validator/helper, release, or devices.

## 6. C2 evidence, budgets, and terminal seal

The builder must exclusive-create and durably verify these canonical JSON/text
artifacts under the C2 root:

1. `p7-td-b-b2-corrected-controller-successor.py`;
2. `successor-controller.patch`;
3. `content-free-validation-summary.json`;
4. `terminal-evidence.json`, schema
   `p7_retained_r3_option_b_b2_c2_controller_correction_terminal_v1`;
5. `terminal-evidence.sha256.json`, schema
   `p7_retained_r3_option_b_b2_c2_controller_correction_terminal_seal_v1`.

Terminal success status is `pass_waiting_for_planner`; any builder failure uses
truthful `hard_failure_waiting_for_planner` when terminal persistence remains
possible. The terminal must bind activation/PLAN/source/builder/successor/patch,
failed-root metadata, exact fixture results, output identities, counters and
locks. The seal is created only after terminal writer return and must bind
physical terminal bytes/SHA/schema/status plus non-self-attestation.

Success budgets:

```text
builder process/invocation = 1/1
C2 root create = 1
rejected controller lstat/open/read/hash = 1/1/1/1
failed-root lstat/scandir/direct entries = 1/1/0
C1 evidence lstat/open/read/hash/parse = 0/0/0/0/0
retained artifact/directory access = 0
decision-source access = 0
successor real-input invocation = 0
successor content-free invocation = 1
resolved-record checks = 10/10
lifecycle checks = 8/8
successor/patch/validation/terminal/terminal-seal writes = 1/1/1/1/1
retry/fallback/second builder/second root = 0/0/0/0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1, only after terminal seal
```

Canonical validator/helper/consumer/replay, eligibility, release, tests,
compileall, focused/full/synthetic, CodeGraph, network/DNS/`.env`/credentials,
device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8,
firmware/deployment are all zero.

Any input/root/source/patch/fixture/budget/persistence mismatch hard-fails with
no retry, fallback, second root, repair, or later-stage entry. After durable C2
terminal seal and one ER append, stop exact
`B2_C2_CONTROLLER_CORRECTION_WAITING_PLANNER_REVIEW`.

## 7. Acceptance and future lock

Planner may accept C2 only if it independently proves:

- the old over-strong whole-list predicate no longer owns resolved paths;
- the successor has one exact record-semantic owner and passes `10/10` cases;
- every post-root body failure routes through the single failure terminal owner;
- terminal/seal persistence failures cannot expose ER or success;
- lifecycle fixtures pass `8/8` with exact physical ordering and unchanged-file
  hashes;
- source diff is limited to the two declared semantic regions and necessary
  fixture/counter wiring;
- all forbidden read/call/device/release counters are zero;
- C2 terminal and seal are physical, canonical, linked, and non-circular.

Even a C2 pass only returns to Planner/Orchestrator. A future new B2 PLAN must
freeze a new root, successor source identity, and explicit new C1/retained read
budgets before one real invocation. C2 itself does not authorize that retry or
unlock B3.

## 维护性判断

该纠偏保持在一次性 external controller 内，不修改 production/test owner，也不新增 eligibility 或 scientific owner。它把路径语义收敛到单一 resolved-record helper，把 post-root persistence 收敛到单一 terminal lifecycle owner，并以 18 个行为 fixture 覆盖真实失败边界。后续无需架构重构；只有 C2 被独立接受后才能重新规划一次真实 B2。
