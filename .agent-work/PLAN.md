# REF-P7-25-R2-B2-C3：content-free source-structure index

**计划状态：** `EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C3`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C3-CONTENT-FREE-SOURCE-STRUCTURE-INDEX-V1`

**预计时长：** `2–6 分钟`；纯离线，不属于预计超过10分钟的长任务。

**当前唯一动作：** Orchestrator 审查本 PLAN 后，仅可用一个新的 PLAN-only activation commit 冻结 dispatch；激活后，Executer 可调用一次新的 external index builder，在一个 brand-new root 中重新获得一次 rejected controller source read budget，生成 immutable AST/source-structure index 与 content-free selector matrix，并 durably seal C3 evidence。C3 不生成、修改或运行 successor。

**Planner stop：**
`B2_C3_SOURCE_STRUCTURE_INDEX_WAITING_PLANNER_REVIEW`。

本文件当前 `execution_authorized=true`。Executer 只可执行本 PLAN 冻结的一次 C3 content-free source-structure index；不得生成、修改或运行 successor，不得读取 C1/retained/decision sources，不得进入 B2/B3、调用 canonical validator、产生 eligibility/release，或进入任何设备/scientific route。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1039-p7-retained-r3-option-b-b2-c2-controller-correction-failure-review.md`，bytes `10555`，SHA-256 `8ba91dfb19458fc234b600bb9c39ed78624e6ab121df4b8b28265cc878f12728`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c3_source_structure_index_plan_v1","reference_task_id":"REF-P7-25-R2-B2-C3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C3-CONTENT-FREE-SOURCE-STRUCTURE-INDEX-V1","dispatch_state":"execution_authorized","execution_authorized":true,"single_current_action":"build_immutable_ast_source_structure_index_without_transforming_or_executing_successor","activation_parent":"3b5b242e033284fae47f9ba2e3b457330cfb4dff","activation_subject":"chore(plan): activate b2 c3 source structure index","activation_changed_paths":[".agent-work/PLAN.md"],"activation_additional_paths":0,"activation_commit_count":1,"programmatic_dispatch_head_reads":1,"second_dispatch_head_reads":0,"dispatch_plan_sha256_owner":"sha256_of_exact_plan_blob_at_programmatic_dispatch_head","hand_transcribed_child_sha":false,"review_archive":{"path":".agent-work/PLANS/20260730-1039-p7-retained-r3-option-b-b2-c2-controller-correction-failure-review.md","bytes":10555,"sha256":"8ba91dfb19458fc234b600bb9c39ed78624e6ab121df4b8b28265cc878f12728"},"source":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py","bytes":29841,"sha256":"da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4","new_read_budget":1},"c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c2-controller-correction-da90556-20260730T1621Z","progressive_sha256":"7e72b76432d815c6040656b2e9d61092677437e3464c8a9e53bca6aba453b0d0","terminal_sha256":"56bf421941259015d02531369dc21e6e1184468e2246cb7adec49e99b992ce48","terminal_seal_sha256":"b3624e6c948afce349534461e54864dd19590489f3b454293a3af3b0f49db101","read_budget_each":1,"mutation":0},"future_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c3-source-structure-da90556-20260730T1645Z","builder_invocations":1,"source_structure_indexes":1,"selector_matrix":"12/12","successor_generation":0,"successor_invocations":0,"c1_evidence_reads":0,"retained_artifact_reads":0,"decision_source_reads":0,"retry":0,"fallback":0,"planner_stop":"B2_C3_SOURCE_STRUCTURE_INDEX_WAITING_PLANNER_REVIEW"}`

## 1. Review decision and authority boundary

1. C2 is rejected as
   `REJECTED_SOURCE_TRANSFORM_ANCHOR_UNPROVEN_WITH_CORRECTION_ROOT_FAILURE_LIFECYCLE_ACCEPTED`.
   It durably proved its correction-root failure lifecycle, but it failed before
   successor generation, patching, or either content-free matrix.
2. The exact source-shape cause is not durable evidence. C2 stored only
   `main anchor count`, not the match count or structural candidates. Planner
   did not reopen the already consumed source and will not infer whether the
   cause was annotation, multiline syntax, decorators, nesting, or cardinality.
3. The C2 builder's `ExactPostRootLifecycle` fixture helper was never invoked;
   its matrix is `0/8`. Its attempted text transformation also did not connect
   that helper to the future real `main` body. Only the builder/correction-root
   progressive→terminal→seal→ER ordering is accepted as physically proven.
4. C3 is discovery-only. It freezes semantic source structure and validates an
   AST selector against synthetic in-memory sources. It does not select an
   experimental/scientific branch, transform source, generate a successor,
   run real inputs, emit eligibility, or consume a release.
5. This is an Orchestrator-owned offline engineering/provenance question. No
   unresolved color/measurement science or dangerous device operation exists;
   Advisor/Human authorization is not required.

## 2. Activation and immutable root

1. Orchestrator must first commit the reviewed ER/archive/PLAN/FULL state. Then
   Planner may change only `.agent-work/PLAN.md` in one direct-child activation
   commit with exact subject
   `chore(plan): activate b2 c3 source structure index`.
2. The activated PLAN must freeze the exact parent and child, preserve the sole
   changed path and additional-path count `0`, set
   `dispatch_state=execution_authorized`, `execution_authorized=true`, and set
   the current stop to `B2_C3_SOURCE_STRUCTURE_INDEX_WAITING_PLANNER_REVIEW`.
   It may not alter C3 scope, budgets, root, inputs, matrices, or locks.
3. Executer must read symbolic HEAD exactly once and derive the exact PLAN blob
   bytes/SHA from that programmatic dispatch commit. No hand-transcribed child
   SHA, PLAN-embedded expected blob SHA, second HEAD read, alternate dispatch,
   or commit by Executer is allowed.
4. Worktree must be clean before root creation. If not, stop before any C2
   evidence or source access; Executer may not clean or commit.
5. Exact future root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c3-source-structure-da90556-20260730T1645Z`.
   It must be absent immediately before one builder creates it mode `0700`.
   No precreation, alternate timestamp/root, reuse, delete, rename, repair,
   retry, fallback, second root, or second builder is allowed.
6. Executer may author one disposable builder source outside the repository
   under `/Volumes/4T/temp/rgbww-optimizer`, freeze its bytes/SHA before its
   single invocation, and invoke it once. Repository implementation/test/docs/
   skill/wrapper/GUIDE/FULL/archive/PLAN paths remain read-only.

## 3. Frozen predecessor inputs and exact budgets

After root creation and durable `progressive-00-root-created.json`, the sole
builder may consume these inputs only:

### 3.1 C2 lifecycle evidence

Each gets exactly one non-following `lstat`, one `O_RDONLY|O_NOFOLLOW` open, one
bounded read, before/after `fstat` identity comparison, and one SHA-256:

1. `progressive-00-root-created.json`, expected bytes `1062`, SHA-256
   `7e72b76432d815c6040656b2e9d61092677437e3464c8a9e53bca6aba453b0d0`;
2. `terminal-evidence.json`, expected bytes `1607`, SHA-256
   `56bf421941259015d02531369dc21e6e1184468e2246cb7adec49e99b992ce48`;
3. `terminal-evidence.sha256.json`, expected bytes `455`, SHA-256
   `b3624e6c948afce349534461e54864dd19590489f3b454293a3af3b0f49db101`.

All must parse as strict canonical JSON; the seal must bind the exact physical
terminal bytes/hash/schema/status and preserve its non-self-attestation. The C2
root may receive one non-following directory `lstat` and one direct `scandir`
proving its exact three-file set. No file or directory is mutated. After these
checks, write and durably reload `progressive-01-c2-evidence-validated.json`.

### 3.2 Rejected controller source

Exact path:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py`,
expected bytes `29841`, SHA-256
`da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4`.

It receives one newly explicit non-following `lstat`, one
`O_RDONLY|O_NOFOLLOW` open, one bounded read, one before/after `fstat` identity
comparison, and one SHA-256. The same in-memory bytes may be decoded, tokenized,
parsed with `ast.parse`, indexed, and source-span hashed; no second filesystem
read is permitted. The source is never imported, compiled for execution,
executed, copied, rewritten, patched, or serialized into an output.

Forbidden reads/access counts remain exact zero:

- C1 index/seals/terminal artifacts and their directories;
- all retained-R3 artifacts and their parent/sibling directories;
- GUIDE, Advisor attachment/decision sources, release inputs;
- canonical validator/helper/consumer/replay and production imports;
- rejected C2 builder reread as an input; earlier failed-root access;
- network, DNS, `.env`, credentials, device, camera, Ray, strip, cleanup,
  capture, CR3/NPY, FORMAL, public analyzer, TD-C, sentinel, P8;
- tests, compileall, CodeGraph, release generation/copy/consumption.

## 4. Immutable AST/source-structure index

The builder must parse the frozen in-memory source without executing it and
write one canonical `source-structure-index.json`. Discovery must complete and
record candidate cardinalities even when they are zero or greater than one; it
must not select the first candidate or fail merely because a prior textual
cardinality assumption was wrong.

The index must bind:

1. source path, bytes, SHA-256, device/inode, before/after open-file identity,
   decode/AST/tokenize success, Python AST version, and no-execution counters;
2. every `FunctionDef` or `AsyncFunctionDef` named `main`, including semantic
   scope path, top-level flag, node kind, decorators count, argument/return AST
   hashes, `lineno/col_offset/end_lineno/end_col_offset`, exact byte-span bytes
   and SHA-256, and parent-node kind;
3. every exact semantic call candidate equivalent to
   `contains(index, expected_paths)`—callee/argument node kinds, keyword count,
   enclosing scope, positions, normalized AST hash, and exact source-span hash;
4. every module-level or nested `if` candidate semantically comparing
   `__name__` with string `__main__`, including operand order, scope, body/else
   statement counts, positions, normalized AST hash, and exact span hash;
5. for each `main` candidate, an ordered body outline containing statement
   index, AST node kind, positions, normalized AST hash, exact span hash,
   descendant `Try`/handler counts, and call-node fingerprints;
6. all `.mkdir(...)` call candidates inside each `main`, recording receiver AST
   hash, positional/keyword shape, enclosing statement index, positions, and
   span hash without assuming the receiver name;
7. constant filename occurrences relevant to progressive, terminal, and seal
   persistence as hashes plus enclosing call/statement descriptors; raw source
   text or complete string payloads must not be emitted;
8. one `selector_assessment` reporting candidate counts and unambiguous/ambiguous
   booleans for each selector. These booleans are evidence only and do not grant
   transformation authority.

All normalized AST dumps used for hashing must set `include_attributes=false`;
all exact source spans must additionally bind physical byte offsets and hashes
so formatting boundaries are not lost. The builder must validate that every
recorded span reparses or maps back to the indexed AST node as applicable.

After writing and strict-reloading the index, write a separate canonical
`source-structure-index.sha256.json` binding its bytes/hash/schema/source hash,
with `index_write_returned=true` and
`index_seal_self_write_return=not_self_attested`.

## 5. Content-free AST selector matrix

The same builder must use only in-memory synthetic Python strings, never the
real source path, for at least these exact `12/12` selector cases:

1. plain top-level `def main():` is indexed;
2. return-annotated top-level `def main() -> int:` is indexed;
3. multiline `main` signature is indexed;
4. decorated top-level `main` is indexed with decorator metadata;
5. a nested `main` plus one top-level `main` are distinguished by scope;
6. two top-level `main` definitions are reported ambiguous, not first-selected;
7. an async top-level `main` is recorded as `AsyncFunctionDef`, not sync main;
8. exact `contains(index, expected_paths)` call is identified semantically;
9. extra/missing/reordered predicate arguments do not qualify as the exact call;
10. single- and double-quoted `__main__` guards are semantically equivalent;
11. reversed `"__main__" == __name__` operand order is recorded explicitly;
12. multiline/keyword `.mkdir(...)` calls are indexed by AST, not line regex.

Each case must assert candidate counts, scope/top-level classification, node
kinds, positions/span hashes where relevant, and ambiguity behavior. Write one
canonical `ast-selector-validation-summary.json` and one non-self-attested
`ast-selector-validation-summary.sha256.json`. No fixture directory or source
file is needed; synthetic strings stay in memory and are not execution inputs.

After both index seals and selector-summary seals return, write and durably
reload `progressive-02-structure-index-sealed.json`.

## 6. Single correction-root lifecycle and evidence

Immediately after successful root creation, all later C2-evidence reads, source
read/indexing, selector matrix, index/summary/seal writes, terminal, and ER
exposure must be enclosed by one lifecycle owner. It must use exclusive-create,
canonical bytes, file fsync, directory fsync, strict reload, and no-clobber for:

1. `progressive-00-root-created.json`;
2. `progressive-01-c2-evidence-validated.json`;
3. `source-structure-index.json`;
4. `source-structure-index.sha256.json`;
5. `ast-selector-validation-summary.json`;
6. `ast-selector-validation-summary.sha256.json`;
7. `progressive-02-structure-index-sealed.json`;
8. `terminal-evidence.json`;
9. `terminal-evidence.sha256.json`.

On any exception after root creation, preserve earlier files unchanged and
write one truthful `hard_failure_waiting_for_planner` terminal with exact
failing stage, exception type/message, counters, root/source/C2 evidence
identities, last durable stage, and all lock zeros, then one physical terminal
seal. Success status is `pass_waiting_for_planner`. Terminal schema:
`p7_retained_r3_option_b_b2_c3_source_structure_terminal_v1`; seal schema:
`p7_retained_r3_option_b_b2_c3_source_structure_terminal_seal_v1`.

ER payload may become visible only after terminal-seal writer return. Executer
must verify the physical terminal/seal link immediately before exactly one ER
append. If progressive, terminal, or seal persistence fails, no ER append,
invented seal, pass claim, rewrite, repair, retry, or fallback is permitted.

Success budgets:

```text
builder process/invocation = 1/1
C3 root create = 1
C2 root lstat/scandir/direct entries = 1/1/3
C2 evidence lstat/open/read/hash/parse = 3/3/3/3/3
rejected controller lstat/open/read/hash = 1/1/1/1
source decode/tokenize/AST parse/index = 1/1/1/1
source import/compile-for-execution/execute/copy/patch = 0/0/0/0/0
source structure index/index seal = 1/1
AST selector matrix = 12/12
selector summary/summary seal = 1/1
successor generation/patch/real invocation/content-free invocation = 0/0/0/0
C1 evidence reads = 0
retained artifact/directory access = 0
decision-source access = 0
retry/fallback/second builder/second root = 0/0/0/0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1, only after terminal seal
```

Canonical validator/helper/consumer/replay, eligibility, release, tests,
compileall, focused/full/synthetic repo tests, CodeGraph, network/DNS/`.env`/
credentials, device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/
TD-C/sentinel/P8, firmware/deployment are all zero.

Any dispatch/input/source/index/matrix/budget/persistence mismatch hard-fails
with no retry, fallback, second root, repair, or later-stage entry. After durable
C3 terminal seal and sole ER append, stop exact
`B2_C3_SOURCE_STRUCTURE_INDEX_WAITING_PLANNER_REVIEW`.

## 7. Acceptance and future lock

Planner may accept C3 only if it independently proves:

- the C2 failure evidence chain is exact and unchanged;
- the rejected source received exactly one newly authorized read and was never
  imported, executed, copied, transformed, or patched;
- the index records all semantic candidates and exact byte-span/AST hashes
  without regex-based first-match selection;
- discovery completion is independent of candidate cardinality;
- selector fixtures pass `12/12`, including annotations, multiline syntax,
  decorators, nesting, ambiguity, async, predicate, guard, and mkdir cases;
- index, summary, terminal, and all seals are physical, canonical, linked, and
  non-circular;
- all C1/retained/decision/validator/release/device/scientific and successor
  operation counters are zero.

Even a C3 pass only freezes source-structure evidence. It does not prove or
authorize a successor transformation, resolved-record behavior, successor
lifecycle matrix, real-main lifecycle integration, real B2 invocation, B3,
validator, eligibility, release, device work, FORMAL-R6, strip, TD-C, sentinel,
or P8. A later Planner package must consume the accepted structure index and
define one AST-based minimal transform that routes both content-free fixtures
and the real post-root path through the same lifecycle owner.

## 维护性判断

本纠偏把“发现源结构”和“修改源结构”拆开：C3 只建立单一 AST/index owner，并复用已被物理证明的 correction-root terminal persistence 模式，不再依赖脆弱的文本 regex anchor。它不修改 production/test owner、不新增 eligibility/scientific owner，也不形成平行执行框架；后续 transform 必须消费本 index 并保持一个真实/fixture 共用的 lifecycle owner。
