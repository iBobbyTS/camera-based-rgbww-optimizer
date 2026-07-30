# REF-P7-25-R2-B2-C4：deterministic pre-HEAD dispatch correction

**计划状态：** `EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4`

**预计时长：** `4–9 分钟`；纯离线，不属于预计超过10分钟的长任务。

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-AST-SPAN-SUCCESSOR-QUALIFICATION-V3`

**当前唯一动作：** Executer 以一个 `zsh -f` dispatch owner、一次 builder
invocation 和一个 brand-new external root 执行 C4 V3。pre-HEAD wrapper 使用
固定 ordinary variable 与 Python 纯内存 bytewise validator，不依赖任何 zsh
pattern option；随后仅生成并资格验证一个 disposable AST/span successor，写入
terminal seal 与一次 ER handoff 后停 Planner 验收。

**Planner stop：**
`B2_C4_AST_SPAN_SUCCESSOR_WAITING_PLANNER_REVIEW`。

本文件当前 `execution_authorized=true`，仅放行本 PLAN 精确定义的 C4 V3
offline qualification。real B2、retained-R3 access、validator、release、device
或 scientific operation 仍未放行。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1119-p7-retained-r3-option-b-b2-c4-v2-wrapper-selfcheck-failure-review.md`，bytes `5224`，SHA-256 `8ba3187e08f3af280f2c49d615683704c24eb77de2ae000debbcf40a33998c25`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_ast_span_successor_plan_v3","reference_task_id":"REF-P7-25-R2-B2-C4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-AST-SPAN-SUCCESSOR-QUALIFICATION-V3","dispatch_state":"execution_authorized","execution_authorized":true,"single_current_action":"single_zsh_f_dispatch_and_builder_qualification_of_c4_v3_successor","activation_parent":"d7a63f1695de1856361ed5c5cebe926a5d66f40e","activation_parent_freeze_pending":false,"activation_subject":"chore(plan): reactivate b2 c4 deterministic dispatch","activation_changed_paths":[".agent-work/PLAN.md"],"activation_additional_paths":0,"activation_commit_count":1,"programmatic_dispatch_head_reads":1,"second_dispatch_head_reads":0,"dispatch_plan_sha256_owner":"sha256_of_exact_plan_blob_at_programmatic_dispatch_head","hand_transcribed_child_sha":false,"review_archive":{"path":".agent-work/PLANS/20260730-1119-p7-retained-r3-option-b-b2-c4-v2-wrapper-selfcheck-failure-review.md","bytes":5224,"sha256":"8ba3187e08f3af280f2c49d615683704c24eb77de2ae000debbcf40a33998c25"},"superseded_unused_roots":["/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-20260730T1700Z","/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r2-20260730T1710Z"],"c3_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c3-source-structure-da90556-20260730T1645Z","c3_input_reads_each":1,"source":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py","bytes":29841,"sha256":"da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4","new_read_budget":1},"future_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r3-20260730T1730Z","dispatch_wrapper_self_checks":"8/8","shell_pattern_option_dependencies":0,"dynamic_shell_variable_names":0,"builder_invocations":1,"successor_generation":1,"successor_real_b2_invocations":0,"content_free_shared_lifecycle_matrix":"12/12","c1_c2_retained_decision_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"retry":0,"fallback":0,"planner_stop":"B2_C4_AST_SPAN_SUCCESSOR_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and authority boundary

1. C4 V2 is rejected as `REJECTED_PRE_HEAD_WRAPPER_SELFCHECK_FAILURE`.
   Its only `zsh -f` invocation exited `42` in self-check case one because
   `[a-z_][a-z0-9_]#` depended on shell pattern-option semantics that were not
   enabled. Self-check was `0/6`; HEAD read/emission, builder/root/C3/source/
   successor/terminal/ER counts are all zero.
2. A standalone C4 corrective stage is not required. The failure is isolated
   to the pre-HEAD wrapper and can be corrected as C4 V3 by one later PLAN-only
   activation with a fixed ordinary variable and a Python pure-memory bytewise
   validator. V3 may not depend on any shell pattern option.
3. C3 is accepted only as
   `ACCEPTED_EXACT_SOURCE_STRUCTURE_INDEX_ONLY`. Its archive and physical
   evidence prove the frozen source has one unambiguous top-level `main`, one
   exact predicate, one main guard and one `main` mkdir candidate, and that the
   content-free selector matrix is `12/12`.
4. C3 terminal payload counters `terminal_writes=0` and
   `terminal_seal_writes=0` are accepted as the truthful pre-write snapshot.
   The separately returned physical terminal/seal and exact hash link prove
   returned existence `1/1`; rewriting the terminal would be circular.
5. C4 is an offline engineering/provenance qualification. It does not select a
   scientific branch, touch hardware, consume retained R3, invoke real B2, or
   call the canonical validator. Advisor/Human authorization is not required.
6. C4 may create only a disposable successor and evidence under the future
   root. Repository production/test/docs/skill/wrapper/GUIDE/FULL/archive paths
   remain read-only. Executer may append only the final handoff to ER after the
   terminal seal.

## 2. Activated dispatch and immutable root

1. Activation direct parent is exact
   `d7a63f1695de1856361ed5c5cebe926a5d66f40e`; subject is exact
   `chore(plan): reactivate b2 c4 deterministic dispatch`; changed paths are
   exact `.agent-work/PLAN.md`, additional paths `0`, activation commit count
   `1`. The child SHA is not hand-transcribed into its own PLAN blob: the
   corrected wrapper captures the programmatic dispatch HEAD once and owns the
   exact PLAN-blob SHA-256 at that HEAD, avoiding circular self-identity while
   proving the direct-child topology, sole changed path,
   `execution_authorized=true`, and final review stop
   `B2_C4_AST_SPAN_SUCCESSOR_WAITING_PLANNER_REVIEW`.
2. Activation freezes only the actual parent, programmatically owned child and
   PLAN blob identity, dispatch state, and final review stop. It does not widen
   inputs, budgets, transforms, matrices, roots, locks, or successor authority.
3. The corrected dispatch must be one `zsh -f` owner. It contains one
   statically written ordinary variable named exactly `dispatch_head_value`.
   No external, generated, or dynamically expanded variable name may reach
   `typeset`, assignment, indirection, or `eval`. Before any symbolic HEAD read,
   an embedded Python pure-memory validator must pass an exact `8/8` matrix
   through the same byte-validation/accounting path: accept the exact allowed
   name; reject `safe_local_value`; reject `status`; reject `pipestatus`; accept
   one lowercase 40-hex line; reject uppercase/malformed length; reject zero or
   multiple lines; and prove exactly one output event. It may inspect only
   injected bytes and in-memory counters and may not access filesystem, Git,
   builder, root, C3, source, network, or devices.
4. Exact future root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r3-20260730T1730Z`.
   It must be absent immediately before one builder creates it mode `0700`.
   No precreation, alternate root, reuse, repair, delete, rename, retry,
   fallback, second builder, or second successor is allowed.
5. Executer may author one new disposable builder under
   `/Volumes/4T/temp/rgbww-optimizer`, freeze its bytes/SHA before one
   invocation, and may not read or reuse the rejected C2/C3 builders as source.
6. After the self-check passes, the same wrapper executes exactly one
   `git rev-parse HEAD`, captures its stdout into the ordinary local variable
   `dispatch_head_value`, sends its bytes through the same Python validator,
   binds the returned exact value to activated direct-child topology and exact
   PLAN blob, emits that value exactly once, and passes the same in-memory value
   to the sole builder. It may not use `setopt`, `extendedglob`, `kshglob`,
   `bareglobqual`, `shglob`, any shell glob operator for validation, dynamic
   variable assignment, `eval`, or any zsh special/read-only parameter. It may
   not perform a second HEAD read, transcribe/reconstruct the value, retry the
   wrapper, use fallback capture, or launch an alternate dispatch.
7. Both V1 and V2 roots listed in `superseded_unused_roots` are accepted only as
   reported unused (`root creates=0`). They must remain unprobed, uncreated,
   unreused, undeleted and unrenamed; neither is evidence or a fallback
   namespace.

## 3. Exact accepted C3 inputs

After durable `progressive-00-root-created.json`, the sole builder must perform
one non-following root `lstat`, one direct `scandir`, and prove the exact nine
C3 entries recorded in the accepted archive. It then receives exactly one
non-following `lstat`, one `O_RDONLY|O_NOFOLLOW` open, one bounded read, one
before/after `fstat` identity check, one SHA-256 and one strict parse for each of
these six content inputs:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `source-structure-index.json` | 143133 | `b353f7664071ab4f2c83b34405be6dc1209b5f94a299aaeb04c095012743d4d4` |
| `source-structure-index.sha256.json` | 563 | `7c7ea37c16320d2f56912f91b2949b90e80bd3f5b75c6e98495428258c86abf8` |
| `ast-selector-validation-summary.json` | 11115 | `8251e1961e7900f3bbb0c1778c052b068e2cd8e472320b14b78ef3a3ad098d36` |
| `ast-selector-validation-summary.sha256.json` | 536 | `faef3be5d6bfd430b53c6ab020279c9988f3655fe65ad4606990b4d2376b1e06` |
| `terminal-evidence.json` | 5407 | `7861d271789a99cc0e52d03b320d37235ebebe5fb76403ecf2513c5744c07726` |
| `terminal-evidence.sha256.json` | 542 | `301962e4004f39208d012871beab76ae0491dee939fd2abbbd273c26f3858777` |

The three progressives may receive direct-entry metadata observation only;
their content read/open/hash budgets are zero because their exact hashes are
already bound by the accepted terminal. The builder must validate all three
seals, `12/12`, source identity, selector cardinalities and ambiguity flags,
`normalized_ast_include_attributes=false`, span mapping status, terminal
status/stop, and all C3 lock zeros. It must write and durably reload
`progressive-01-c3-index-accepted.json` before source access.

Forbidden C3 access includes parent/sibling enumeration, any C3 mutation,
reopening an input, mmap/copy, and using the index as authority for anything
beyond this exact frozen source.

## 4. One frozen source read and semantic revalidation

Exact source:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py`,
bytes `29841`, SHA-256
`da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4`.

The builder gets exactly one non-following lstat/open/bounded-read/hash with
before/after identity equality. The same in-memory bytes may be decoded,
tokenized and parsed. It must independently recompute and match the C3 module,
top-level-main, main-body, exact-predicate, main-guard and mkdir AST/span hashes
before transforming. No regex, line-string anchor, first candidate, source
reread, import, execution, copy-as-input, or direct text search may select a
transform location.

The builder must reject unless the accepted selectors are still exactly
unambiguous (`main=1`, exact predicate `1`, guard `1`, mkdir in main `1`) and
every selected physical byte span hashes to the accepted index. It then writes
and durably reloads `progressive-02-source-revalidated.json`.

## 5. Minimal AST/span successor transform

The builder may generate exactly one successor source inside the future root.
The transformation must be derived from AST node identity and accepted physical
span boundaries, not from matching source text. It may change only:

1. one module-level lifecycle-owner definition needed to provide post-root
   terminal/seal/ER gating; and
2. the selected top-level `main` post-root region beginning only after the
   accepted `.mkdir(...)` call returns, so that the real path delegates to that
   same owner.

Everything before and including root creation remains byte-identical. Module
imports may change only by the minimum imports mechanically required by the
single lifecycle owner. No CLI option, retained path, expected hash, manifest
science/provenance predicate, canonical validator call, eligibility rule,
release behavior, or `__main__` entry semantics may change.

The lifecycle owner must be the sole owner of post-root progressive output,
success terminal, failure terminal, terminal seal, and “ER exposure permitted”
state. Its terminal payload is frozen before its writer and therefore records
self terminal/seal writes as pre-write zero; the separate seal binds the
returned physical terminal and states `terminal_write_returned=true` while
remaining `not_self_attested`. It must never rewrite a terminal to manufacture
post-return self counters.

The successor must be canonical UTF-8, mode `0600`, parse successfully, and be
sealed by `successor-source.sha256.json`. A canonical
`transform-delta.json` must bind source/successor bytes+SHA, exact AST selector
records consumed, insertion/replacement spans, before/after normalized AST
hashes, unchanged prefix hash through root mkdir, changed byte ranges, import
delta, and structural call edge from the real `main` to the sole lifecycle
owner. Its seal is non-self-attested.

No successor is written until all source/index checks pass. The frozen rejected
source and C3 root remain unchanged.

## 6. Content-free shared-lifecycle qualification

The sole successor may be compiled in memory for qualification and loaded only
into an isolated child namespace whose filesystem/network/device/validator/
release entry points are replaced before any call. The successor's real CLI
entry point and real B2 path are never invoked.

One exact `12/12` matrix must prove the lifecycle callable object reached by the
transformed real `main` is the same object exercised by fixtures—not a copied,
shadow, fixture-only, monkeypatched replacement, or parallel owner:

1. AST call-edge from exact top-level real `main` resolves to the sole owner;
2. exactly one lifecycle-owner definition and one real-main delegation exist;
3. bytes before/through real root mkdir are unchanged;
4. success writes progressives before terminal, then terminal, then seal;
5. failure immediately after root creation preserves the root progressive and
   writes one truthful failure terminal plus one seal;
6. failure during accepted-input validation preserves earlier evidence and
   seals the exact stage/error;
7. failure during manifest/index work cannot expose ER permission;
8. terminal writer failure exposes neither seal nor ER permission;
9. terminal-seal writer failure exposes no ER permission and never invents a
   seal or rewrites terminal;
10. successful physical terminal/seal linkage alone sets ER permission once;
11. repeated owner entry, second terminal, clobber, retry and fallback all fail
    closed;
12. success and every failure case leave retained/validator/release/network/
    device counters at zero and preserve the truthful pre-write self counters.

Fixtures use brand-new child directories beneath the C4 root, deterministic
in-memory records, injected local writers and failure points only. They may not
read C1/C2/C3/source/retained inputs again. Each case records expected/actual
ordered events, exact returned-write counts, pre-write payload counters,
physical seal linkage, ER permission, exception stage and lock zeros.

The builder writes and seals `shared-lifecycle-validation-summary.json`, then
writes and durably reloads `progressive-03-successor-qualified.json`. The
successor is qualification-only and is not a B2 output, validator input,
eligible release, repository source, or reusable authority until a later
Planner review explicitly accepts it.

## 7. Root lifecycle, terminal, and budgets

All work after root creation is enclosed by one external evidence owner using
exclusive-create, canonical bytes, file fsync, directory fsync, strict reload,
mode `0600`, and no-clobber for:

1. `progressive-00-root-created.json`;
2. `progressive-01-c3-index-accepted.json`;
3. `progressive-02-source-revalidated.json`;
4. `successor-controller.py`;
5. `successor-source.sha256.json`;
6. `transform-delta.json` and its seal;
7. `shared-lifecycle-validation-summary.json` and its seal;
8. `progressive-03-successor-qualified.json`;
9. `terminal-evidence.json`;
10. `terminal-evidence.sha256.json`.

On any post-root exception, preserve prior files and write exactly one
`hard_failure_waiting_for_planner` terminal with exact stage/error/counters,
then one physical terminal seal. ER is appended exactly once only after the
terminal-seal writer returns and its link is reloaded. Persistence failure means
no ER append, rewrite, repair, retry, fallback, second root or pass claim.

Success budgets:

```text
builder process/invocation = 1/1
C4 root create = 1
C3 root lstat/scandir/direct entries = 1/1/9
C3 six inputs lstat/open/read/hash/parse = 6/6/6/6/6
C3 progressive content reads = 0
source lstat/open/read/hash/decode/tokenize/AST parse = 1/1/1/1/1/1/1
source import/execute/copy-as-input/text-regex selection = 0/0/0/0
successor generation/write/seal = 1/1/1
transform delta/seal = 1/1
successor in-memory compile = 1
successor real-main structural delegation proof = 1
successor real B2/CLI/retained invocation = 0/0/0
shared lifecycle matrix = 12/12
validation summary/seal = 1/1
C1/C2/retained/decision-source reads = 0
canonical validator/helper/consumer/replay calls = 0
eligibility/release = 0/0
retry/fallback/second builder/second root/second successor = 0/0/0/0/0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1, only after terminal seal
```

Tests, compileall, CodeGraph, repository imports, network/DNS/`.env`/
credentials, device/camera/Ray/strip/cleanup/capture, FORMAL/public analyzer/
TD-C/sentinel/P8, firmware/deployment are all zero.

Any dispatch/input/index/source/transform/matrix/budget/persistence mismatch
hard-fails with no retry or later-stage entry. After one terminal seal and one
ER append, stop exact `B2_C4_AST_SPAN_SUCCESSOR_WAITING_PLANNER_REVIEW`.

## 8. Acceptance and future lock

Planner may accept C4 only if independent replay proves:

- all accepted C3 inputs and seals were exact and read only within budget;
- one source read matched every accepted AST/span selector;
- the successor delta is mechanically limited to the sole owner, minimum
  imports, and real-main post-root delegation while the through-mkdir prefix is
  byte-identical;
- the transformed real main and all fixtures resolve to the same owner;
- matrix is `12/12`, failure ordering is fail-closed, and terminal/seal/ER
  ordering is non-circular;
- all retained/validator/eligibility/release/device/scientific locks are zero.

Even acceptance authorizes no real B2. The next Planner package must consume
the accepted successor plus C1 path-owner evidence and define a new bounded
content-reading B2 invocation. B3, eligibility, release consumption, devices,
FORMAL-R6, strip, TD-C, sentinel and P8 remain hard locked.

## 维护性判断

C4 keeps semantic selection in the accepted C3 AST index and requires exactly
one lifecycle owner shared by real-main structure and fixtures. The successor
remains disposable and offline, so this package introduces no production owner
or parallel execution framework. Follow-up cleanup is unnecessary unless C4
reveals that the existing controller cannot express the single-owner boundary
without a broader refactor; that would return to Orchestrator, not Advisor.
