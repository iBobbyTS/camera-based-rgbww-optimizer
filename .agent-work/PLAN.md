# REF-P7-25-R2-B2-C4-C1：content-free byte-span statement-selector correction

**计划状态：** `PLANNER_COMPLETE_WAITING_ORCHESTRATOR_REVIEW`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-C1`

**预计时长：** `3–7 分钟`；纯离线，不属于预计超过10分钟的长任务。

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-BYTE-SPAN-STATEMENT-SELECTOR-CORRECTION-V1`

**当前唯一动作：** 在 Orchestrator 验收并通过一次 PLAN-only activation 后，
Executer 以一个 brand-new external root 执行一次 content-free correction：只读取
C4 V3 的五个 durable evidence 文件与冻结 builder 各一次，机械替换 line-only
statement containment 为 byte-span containment 的单一 helper，并以合成输入验证
同一 helper。不得读取 C3、真实 frozen source、C1/C2、retained 或 decision inputs，
不得调用 corrected builder 的 real `main`。

**Planner stop：**
`B2_C4_C1_BYTE_SPAN_SELECTOR_WAITING_PLANNER_REVIEW`。

本文件当前 `execution_authorized=false`。Orchestrator 必须先独立验收本 review、
更新 FULL 并整理提交；随后 Planner 只能以单独 PLAN-only commit 冻结 activation
parent/subject/changed-path 后，才可把本包切换为 `execution_authorized=true`。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1135-p7-retained-r3-option-b-b2-c4-v3-semantic-failure-review.md`
（bytes `5464`，SHA-256
`87551c8dba39c05606974f2d0696e935f970683ad4869ecade1407d7bcf8fd15`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_c1_byte_span_selector_plan_v1","reference_task_id":"REF-P7-25-R2-B2-C4-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-BYTE-SPAN-STATEMENT-SELECTOR-CORRECTION-V1","dispatch_state":"waiting_orchestrator_review","execution_authorized":false,"single_current_action":"content_free_byte_span_statement_selector_correction","activation_parent_freeze_pending":true,"activation_changed_paths":[".agent-work/PLAN.md"],"activation_additional_paths":0,"activation_commit_count":1,"review_archive":{"path":".agent-work/PLANS/20260730-1135-p7-retained-r3-option-b-b2-c4-v3-semantic-failure-review.md","bytes":5464,"sha256":"87551c8dba39c05606974f2d0696e935f970683ad4869ecade1407d7bcf8fd15"},"rejected_c4_v3_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r3-20260730T1730Z","rejected_c4_v3_builder":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-ast-span-successor-builder-v3.py","bytes":21474,"sha256":"df0020d9aa7c902cdd11bb6d5c52b80dabce01b31693808a60035a900dc68e37"},"c4_v3_evidence_reads_each":1,"c4_v3_builder_reads":1,"c3_source_c1_c2_retained_decision_reads":0,"future_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-byte-span-selector-df0020d-20260730T1745Z","corrected_builder_generations":1,"corrected_builder_real_main_invocations":0,"selector_matrix":"12/12","canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"retry":0,"fallback":0,"planner_stop":"B2_C4_C1_BYTE_SPAN_SELECTOR_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and authority boundary

1. C4 V3 is rejected as
   `REJECTED_TRANSFORM_PRECONDITION_LINE_ONLY_STATEMENT_CONTAINMENT`.
   Exact terminal/seal hashes are
   `6b88723d8fca83bb7836a1a9adf1b3ab72fd23fe8b5b8625d5a7e8d73253fbee`
   and
   `663a63e3191260d710abfb1bc831d13c7045408321c7fee1a504e8c48a9649d3`.
2. The durable `progressive-02-source-revalidated.json` proves accepted C3
   field interpretation, normalized AST hashes, byte-offset mapping and physical
   span hashes all passed. The subsequent builder block discarded those columns
   and byte spans and used line-only containment, then raised exact
   `RuntimeError: mkdir statement cardinality`.
3. C4-C1 is the minimal content-free engineering correction. It may neither
   reinterpret scientific guidance nor touch retained R3, real B2, canonical
   validator, release, network or devices. Advisor/Human authorization is not
   required.
4. C4-C1 may create only a corrected disposable builder and qualification
   evidence. It does not generate a controller successor, validate real C4,
   authorize B2/B3, or make retained R3 consumable.
5. Executer may append one post-seal handoff to ER. PLAN/FULL/GUIDE/archive,
   repository production/test/docs/skill/wrapper paths and frozen external
   inputs are read-only.

## 2. Activation and immutable namespace

1. Before execution, a later PLAN-only activation must freeze exact direct
   parent, subject, sole changed path `.agent-work/PLAN.md`, additional paths
   `0`, one commit, `execution_authorized=true`, and the unchanged final Planner
   stop. The activation child SHA is programmatically read once at dispatch and
   must not be hand-transcribed into its own blob.
2. Exact future root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-byte-span-selector-df0020d-20260730T1745Z`.
   It must be absent before one owner creates it mode `0700`. No precreation,
   alternate root, reuse, repair, delete, rename, retry, fallback, second owner,
   second corrected builder or root is allowed.
3. Executer may author one new disposable C4-C1 builder under
   `/Volumes/4T/temp/rgbww-optimizer`, freeze its bytes/hash, and invoke it once.
   It may not reuse a rejected builder as executable code; the V3 builder is an
   immutable content input only.
4. The pre-root dispatcher must prove the activation and clean worktree, read
   symbolic HEAD exactly once, and bind the active PLAN blob. Any mismatch
   stops before root/input access and produces no ER handoff.

## 3. Exact C4 V3 durable evidence inputs

The sole correction owner receives exactly one non-following lstat, one
`O_RDONLY|O_NOFOLLOW` open, one bounded read, one before/after fstat identity
check, one SHA-256 and one strict parse for each file:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `progressive-00-root-created.json` | 1558 | `8d4cff7212cf5c8615e411ee19dcb93ffa47664c294f8348796689277f75a219` |
| `progressive-01-c3-index-accepted.json` | 3830 | `cb78f46f84f832ff701059cf235b67c742e91062df0f12da24a3a4204bee29eb` |
| `progressive-02-source-revalidated.json` | 2563 | `2e94fa3740a8298349bc589808d28fa10e1b32a3fa84ee287d9432b1b077e56c` |
| `terminal-evidence.json` | 1869 | `6b88723d8fca83bb7836a1a9adf1b3ab72fd23fe8b5b8625d5a7e8d73253fbee` |
| `terminal-evidence.sha256.json` | 285 | `663a63e3191260d710abfb1bc831d13c7045408321c7fee1a504e8c48a9649d3` |

The root may receive one non-following lstat and one direct scandir proving the
exact five names above; no parent/sibling enumeration. The owner validates the
progressive stage chain, terminal physical linkage, exact source-revalidated
hash/cardinality payload, exact failure stage/error, all success-output zeros,
ER permission/linkage, and every retained/validator/release/device lock zero.
It writes and durably reloads `progressive-01-v3-failure-accepted.json` before
reading the builder.

C4 V3 root mutation, reopen, mmap, copy-as-input, repair, and any C3/source/C1/
C2/retained/decision access are forbidden.

## 4. One frozen V3 builder read and exact correction

Exact content input:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-ast-span-successor-builder-v3.py`,
bytes `21474`, SHA-256
`df0020d9aa7c902cdd11bb6d5c52b80dabce01b31693808a60035a900dc68e37`.

The owner gets one non-following lstat/open/bounded-read/hash with before/after
identity equality. The same in-memory bytes may be decoded, tokenized and AST
parsed once. It must structurally prove exactly one faulty block:

- an assignment to `containing` whose comprehension iterates direct
  `main_node.body`;
- its predicate compares only `lineno/end_lineno` to the selected `mkdir`;
- the immediately owning validation raises `mkdir statement cardinality` when
  the result is not one; and
- the block occurs after writing `progressive-02-source-revalidated.json` and
  before any successor write/generation counter.

No regex, literal-line anchor, first-match selection, import, execution or
second read may identify the correction site.

The corrected builder must replace only that structurally selected block plus
the minimum adjacent definitions required for one pure helper named
`_select_unique_main_statement_by_byte_span`. The helper receives a sequence of
already derived statement byte spans and one already derived target byte span;
selects only records satisfying
`statement_start <= target_start < target_end <= statement_end`; returns the
sole match; and fails closed on zero, multiple, reversed, negative or
non-integer bounds. The real transform path must derive each direct
`main_node.body` statement's start/end through the existing UTF-8 `bytepos`
mapping, pass the already accepted `mkdir` physical span into this same helper,
and use its sole returned AST statement. It may not fall back to line-only
containment, text search or a second selector.

No other root/input/hash/AST/span/transform/successor/lifecycle/matrix/terminal/
ER behavior may change. Imports may change only if mechanically required by
this helper; no new third-party dependency is allowed. The corrected builder is
canonical UTF-8, mode `0600`, parses and compiles in memory, but its `main` and
real C4 path are never invoked.

Write and seal `corrected-builder-v4.py`, then write and seal a canonical
`builder-transform-delta.json` binding source/corrected identities, exact AST
selector record, changed physical byte ranges, before/after normalized AST
hashes, import delta, sole-helper definition cardinality, and real-path call
edge to that helper. All bytes before and after the selected correction region
must be proven identical.

## 5. Content-free selector qualification

The exact helper object compiled from the corrected builder must be loaded into
an isolated namespace with filesystem, Git, process, network, device,
validator, release and real-input entry points disabled before any call. The
corrected builder's `main` and real transform path remain uninvoked.

One exact `12/12` matrix must prove:

1. corrected source has exactly one helper definition and one real-path call;
2. the old line-only selector block is absent exactly once, with no fallback;
3. one ordinary containing byte span returns the corresponding statement;
4. same-line adjacent statements select only the column-exact containing span;
5. a target nested within one top-level compound statement selects that owner;
6. multibyte UTF-8 bytes preceding a target do not turn character columns into
   byte offsets;
7. boundary equality at statement start/end is accepted only for non-empty
   target spans;
8. zero containing spans fail closed;
9. multiple containing spans fail closed;
10. reversed, negative, boolean or non-integer bounds fail closed;
11. repeated helper calls are deterministic and do not mutate inputs; and
12. every case leaves root/input/source/C3/retained/validator/release/network/
   device and corrected-builder-real-main counters at zero.

Fixtures are deterministic in-memory records only. They may not read C4 files
again or access any earlier evidence/source. The same callable used by the real
transform path—not a copied, shadowed or monkeypatched helper—must be exercised.
Write and seal `byte-span-selector-validation-summary.json`, then write and
durably reload `progressive-02-corrected-builder-qualified.json`.

## 6. Evidence lifecycle and budgets

All outputs use exclusive-create, canonical bytes, file fsync, directory fsync,
strict reload, mode `0600`, and no-clobber:

1. `progressive-00-root-created.json`;
2. `progressive-01-v3-failure-accepted.json`;
3. `corrected-builder-v4.py` and `corrected-builder-v4.sha256.json`;
4. `builder-transform-delta.json` and its seal;
5. `byte-span-selector-validation-summary.json` and its seal;
6. `progressive-02-corrected-builder-qualified.json`;
7. `terminal-evidence.json` and `terminal-evidence.sha256.json`.

On post-root exception, preserve prior evidence and write one truthful failure
terminal plus one non-self-attested physical seal. Terminal payload freezes its
own write counters before serialization; it must never be rewritten. ER
permission becomes true only after the seal writer returns and the exact link
is durably reloaded. Append ER exactly once after that point; persistence
failure permits no ER append, retry, repair, fallback or alternate root.

Success budgets:

```text
correction owner process/invocation = 1/1
root create = 1
C4 V3 root lstat/scandir/direct entries = 1/1/5
C4 V3 five inputs lstat/open/read/hash/parse = 5/5/5/5/5
V3 builder lstat/open/read/hash/decode/tokenize/AST parse = 1/1/1/1/1/1/1
V3 builder import/execute/copy/mmap = 0/0/0/0
corrected builder generation/write/seal = 1/1/1
corrected builder parse/in-memory compile = 1/1
corrected builder real main/real C4 invocation = 0/0
transform delta/seal = 1/1
selector matrix = 12/12
validation summary/seal = 1/1
C3/source/C1/C2/retained/decision reads = 0
canonical validator/helper/consumer/replay = 0
eligibility/release = 0/0
retry/fallback/second owner/root/corrected builder = 0/0/0/0/0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1, only after terminal seal
```

Tests, compileall, CodeGraph, repository imports, network/DNS/`.env`/
credentials, device/camera/Ray/strip/cleanup/capture, FORMAL/public analyzer/
TD-C/sentinel/P8, firmware/deployment are all zero.

Any activation/input/semantic selection/transform/matrix/budget/persistence
mismatch hard-fails. After one terminal seal and one ER append, stop exact
`B2_C4_C1_BYTE_SPAN_SELECTOR_WAITING_PLANNER_REVIEW`.

## 7. Acceptance and future lock

Planner may accept C4-C1 only if independent replay proves the exact V3 failure
chain, one minimal AST-selected builder correction, one shared byte-span helper,
the real-path structural call edge, unchanged surrounding builder bytes,
`12/12`, and all locks/counters.

Acceptance would qualify only a disposable corrected C4 builder. A later
Planner package must define a brand-new root and one actual corrected C4
attempt; it may not reuse the V3 root or infer permission to read C3/source.
Real B2, B3, retained R3, canonical validator, eligibility, release consumption,
devices, FORMAL-R6, strip, TD-C, sentinel and P8 remain hard locked.

## 维护性判断

The correction isolates one pure byte-span containment owner and validates the
same callable used by the future real transform. It does not add a production
owner or parallel lifecycle. The extra package is justified by the one-shot
input budgets: it proves the local selector repair without consuming real
source/C3 again, and a broader refactor is neither needed nor authorized.
