# REF-P7-25-R2-B2-C4-C1-C1：content-free dual-owner controller correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-C1-C1`

**预计时长：** `4–8 分钟`；纯离线，不属于预计超过10分钟的长任务。

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-DUAL-OWNER-CONTROLLER-CORRECTION-V1`

**当前唯一动作：** Executer 在一个 brand-new external root 运行一次 content-free
correction owner：只读取 C4-C1 的四个 durable physical artifacts 与冻结 C4-C1
controller 各一次，生成一个 corrected controller，精确修正 AST
ancestor/statement-scope containment 与 canonical-LF terminal seal plus strict
pre-ER gate，并以合成 negative matrix 资格化。不得读取任何 C4 V3 payload、V3
builder、C3/source/retained input，也不得执行 corrected controller real `main`。

**Planner stop：**
`B2_C4_C1_C1_DUAL_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`。

本文件当前 `execution_authorized=true`。它只授权上述一次 content-free correction
owner 及本 PLAN 明列的离线证据生命周期；不授权 corrected controller real
`main`、validator、release、网络或设备调用。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1152-p7-retained-r3-option-b-b2-c4-c1-dual-failure-review.md`
（bytes `7487`，SHA-256
`a842794607f17ecc0ede62f126eda7064b090eb50830e72df852ea075311c90c`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_c1_c1_dual_owner_controller_correction_plan_v1","reference_task_id":"REF-P7-25-R2-B2-C4-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-DUAL-OWNER-CONTROLLER-CORRECTION-V1","dispatch_state":"dispatchable_one_fresh_executer_after_plan_only_activation_commit","execution_authorized":true,"single_current_action":"content_free_dual_owner_controller_correction","activation_parent":"7119db934b526b6c0e0a8095d55909914bd4deda","activation_parent_freeze_pending":false,"activation_subject":"chore(plan): activate b2 c4 c1 c1 controller correction","activation_changed_paths":[".agent-work/PLAN.md"],"activation_additional_paths":0,"activation_commit_count":1,"activation_plan_blob_owner":"runtime_git_rev_parse_HEAD_colon_exact_plan_path","activation_plan_sha256_owner":"runtime_sha256_of_committed_plan_blob","activation_plan_worktree_must_equal_committed_blob":true,"activation_self_referential_expected_child_blob_or_plan_sha_forbidden":true,"programmatic_dispatch_head_reads":1,"second_dispatch_head_reads":0,"review_archive":{"path":".agent-work/PLANS/20260730-1152-p7-retained-r3-option-b-b2-c4-c1-dual-failure-review.md","bytes":7487,"sha256":"a842794607f17ecc0ede62f126eda7064b090eb50830e72df852ea075311c90c"},"rejected_c4_c1_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-byte-span-selector-df0020d-20260730T1745Z","rejected_terminal_sha256":"09b4add8bfb7daf931087aa2d6b2c752028682035b1ed6dcd4f305d4c468a7c0","invalid_terminal_seal_sha256":"8bc0fe09d02fb0cebbefb05554cef0f4f3b84cfb1403d5e8f01e6cf58be36ade","er_handoff_accepted":false,"c4_c1_artifact_reads_each":1,"c4_v3_payload_builder_reads":0,"frozen_c4_c1_controller":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-c1-byte-span-controller-v1.py","bytes":28701,"sha256":"ba05a533f76dec4e64519b1a76970c791521223c1936ff3cb856222218d45dac"},"future_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-c1-dual-owner-correction-ba05a53-20260730T1800Z","corrected_controller_generations":1,"corrected_controller_real_main_invocations":0,"negative_matrix":"16/16","canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"retry":0,"fallback":0,"planner_stop":"B2_C4_C1_C1_DUAL_OWNER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and authority boundary

1. C4-C1 is rejected as
   `REJECTED_DUAL_OWNER_AND_EVIDENCE_LIFECYCLE_FAILURE`.
   The selector stopped with exact `RuntimeError: faulty assignment owner` before
   corrected generation; the terminal seal is strict-JSON invalid because its
   final two bytes are literal `\\n`; the controller nevertheless appended ER.
2. The invalid seal and ER append are evidence-lifecycle violations. The ER
   entry is an unauthorized diagnostic observation, not a sealed handoff. It
   cannot advance C4-C1 or B2.
3. This is a bounded engineering correction, not a scientific branch. It needs
   neither Advisor guidance nor Human authorization. It may not reinterpret
   GUIDE, retained evidence, scientific inputs or eligibility.
4. One correction process owns both local repairs because both are necessary
   prerequisites for a trustworthy retry. The corrected controller still has
   two explicit semantic owners: statement-scope selection and terminal-seal/
   ER gating. It may add no production owner or alternate execution framework.
5. Executer may append ER only after the new package's own terminal seal is
   canonical, strictly reloaded and physically linked. PLAN/FULL/GUIDE/archive,
   repository production/test/docs/skill/wrapper paths, rejected physical
   artifacts and frozen controller are read-only.

## 2. Activation and immutable namespace

1. This package is executable exactly once by the activation commit being
   created now. Its subject is exact
   `chore(plan): activate b2 c4 c1 c1 controller correction`, its direct parent
   is frozen to `7119db934b526b6c0e0a8095d55909914bd4deda`, its exact changed path is
   `.agent-work/PLAN.md`, and additional paths are `0`.
2. At dispatch, Executer reads symbolic HEAD exactly once and derives the PLAN
   SHA-256 from that commit's PLAN blob, proving direct parent, subject, sole
   changed path, clean worktree, blob/worktree equality,
   `execution_authorized=true`, and unchanged Planner stop. No hand-transcribed
   child SHA, PLAN-embedded expected hash, or second HEAD read is permitted.
3. Exact future root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-c1-dual-owner-correction-ba05a53-20260730T1800Z`.
   It must be absent before one owner creates it mode `0700`. No precreation,
   reuse, repair, delete, rename, alternate root, retry, fallback, second owner
   or second corrected controller is allowed.
4. Executer may author exactly one disposable correction-owner script at
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-c1-c1-dual-owner-correction-v1.py`,
   freeze its bytes/hash before its sole invocation, and never invoke it again.
   The owner writes one corrected controller under the new root; corrected real
   `main` and any real C4/C4-C1 path remain uninvoked.
5. Any pre-root activation/cleanliness/root-absence mismatch stops before any
   frozen input read and produces no root or ER append.

## 3. Exact C4-C1 physical inputs

The rejected root receives one non-following lstat and one direct scandir,
proving exact four entries. The sole owner receives exactly one non-following
lstat, one `O_RDONLY|O_NOFOLLOW` open, one bounded read, before/after fstat and
lstat identity equality, one SHA-256 operation, and one strict parse attempt
for each:

| File | Bytes | SHA-256 | Required interpretation |
| --- | ---: | --- | --- |
| `progressive-00-root-created.json` | 645 | `3d6e1ba53f2d8cb8384684179d526c371df78732f158a7e55af4e64181323b03` | strict JSON valid; exact dispatch/root identity |
| `progressive-01-v3-failure-accepted.json` | 2256 | `f36acbe877a27b9c2e5f75d86c6566df600532edad35bfc41c649278de20aacf` | strict JSON valid; reported inputs/locks only |
| `terminal-evidence.json` | 962 | `09b4add8bfb7daf931087aa2d6b2c752028682035b1ed6dcd4f305d4c468a7c0` | strict JSON valid; exact failure/stop |
| `terminal-evidence.sha256.json` | 336 | `8bc0fe09d02fb0cebbefb05554cef0f4f3b84cfb1403d5e8f01e6cf58be36ade` | strict JSON must fail at extra data; bytes must end exact literal `\\n` |

The invalid seal may be diagnosed only from its exact in-memory bytes and the
strict parse failure. The owner must not strip, normalize, prefix-parse, repair,
rewrite, regenerate, copy-as-input or treat it as a target linkage. It writes
and durably reloads `progressive-01-c4c1-dual-failure-accepted.json` stating
`sealed_handoff=false`, `er_append_authorized=false`, both failure owners and
all downstream locks before reading the controller.

No C4 V3 root/file, V3 builder, C3/source/C1/C2/retained/decision input may be
opened, read, hashed, parsed, copied, mmaped or inferred as authorization. The
paths/hashes mentioned inside progressive evidence are inert provenance text.

## 4. One frozen C4-C1 controller read and exact transform boundary

Exact controller input:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-c1-byte-span-controller-v1.py`,
bytes `28701`, SHA-256
`ba05a533f76dec4e64519b1a76970c791521223c1936ff3cb856222218d45dac`,
regular non-symlink mode `0644`.

The owner gets one lstat/open/bounded-read/hash and before/after identity proof.
The same in-memory bytes may be decoded, tokenized and AST parsed once. No
import, execution, regex, literal-line anchor, first-match selection, mmap,
copy-as-input or second read may identify the changes.

The transform may alter only these AST-selected semantic regions and minimum
adjacent definitions/imports mechanically required by them:

### 4.1 AST ancestor and statement-scope owner

1. Select the sole `find_faulty` function and the sole structurally matching
   `containing` list-comprehension assignment already identified by the frozen
   predicates. Do not weaken those predicates.
2. Replace the direct-parent-is-function assumption with an ancestor-edge map
   that records parent node, field name and list index. Climb from the selected
   assignment to the nearest enclosing `FunctionDef`/`AsyncFunctionDef`, prove
   it is the sole function named `main`, and reject any intervening function or
   lambda scope.
3. Independently prove the assignment is a direct member of exactly one
   list-valued statement field of its immediate AST container. Select the
   cardinality validation only as the immediately following statement in that
   same list. Zero/multiple containers, no following statement, cross-field or
   cross-scope matches fail closed.
4. Preserve the existing structural error-string, iterator and target-base
   proofs. The returned assignment/validation must therefore belong to one
   exact nested statement scope under the sole `main`; no line/text fallback or
   direct-parent assumption remains.

### 4.2 Canonical LF seal writer and strict pre-ER gate

1. Select the sole `external_terminal_seal` definition and exactly its success
   and failure call sites plus the immediately dependent ER append blocks.
2. The child writer must serialize canonical JSON followed by exactly one byte
   `0x0a`. Its source must use an unambiguous LF construction such as
   `chr(10)`; nested raw-string backslash spelling is forbidden.
3. The parent must non-following-open and bounded-read the returned seal, prove
   identity/mode, strict-parse the full bytes, require exact canonical-byte
   equality including one LF, and validate target path, bytes, SHA-256,
   device and inode against the terminal identity. It returns a gate token only
   after every check succeeds.
4. Success and failure paths must both obtain that exact gate token before any
   ER file open or append. Terminal payloads must state
   `er_permission_before_validated_seal=false`; no pre-serialized claim may set
   permission true. Writer failure, strict reload failure or target mismatch
   must leave ER open/append counters `0/0` and propagate the hard failure.
5. There is one shared writer/validator/gate path. No success-only validator,
   catch-and-continue, fallback parser, whitespace stripping, old-seal repair,
   or duplicate ER path is allowed.

Write mode-`0600` `corrected-controller-v2.py` and its seal, then a sealed
`controller-transform-delta.json`. The delta binds input/output identities,
exact AST selectors and physical byte ranges, before/after normalized AST
hashes, import delta, helper/function cardinalities, call edges, both ER gate
dominance records, and complement byte equality. Every byte outside the exact
selected regions and required adjacent definitions/imports must be identical.
The corrected file must decode, tokenize, parse and compile in memory; real
`main` remains uninvoked.

## 5. Content-free `16/16` negative qualification

Load only the exact corrected selector/validator helper objects into an
isolated namespace with filesystem, Git, process, network, validator, release,
real-input and ER entry points disabled. The same callables referenced by the
corrected real path—not copies, shadows or monkeypatches—must pass deterministic
in-memory fixtures:

1. a faulty assignment directly in `main` selects its same-list validation;
2. a faulty assignment nested in `try.body` selects `main` plus that exact list;
3. a doubly nested statement container still selects the nearest statement
   list and sole enclosing `main`;
4. an assignment under a non-`main` function fails closed;
5. zero or multiple faulty assignments fail closed;
6. zero/multiple direct statement containers fail closed;
7. validation absent or not immediately adjacent in the same list fails closed;
8. crossing a nested function/lambda or statement-field boundary fails closed;
9. one exact canonical-LF seal with correct target linkage is accepted;
10. the observed literal-backslash-`n` suffix is rejected;
11. missing LF, CRLF and extra-LF encodings are each rejected;
12. parseable but noncanonical spacing/key order is rejected;
13. wrong path/bytes/SHA/device/inode target linkage is rejected;
14. corrected AST proves exactly two real ER paths and each is dominated by the
    shared validated-seal gate, with no pre-gate ER open;
15. an isolated harness using the same validator proves each invalid seal
    leaves ER open/append counters `0/0`, while one valid seal permits `1/1`;
16. repeated calls are deterministic/nonmutating and all C4 V3, builder,
    C3/source/retained/validator/release/network/device and corrected real-main
    counters remain zero.

Compound subcases in cases 5, 6, 7, 11, 13 and 15 must all pass; the matrix may
not collapse them into an unverified aggregate boolean. Write and seal
`dual-owner-negative-matrix.json`, then write and durably reload
`progressive-02-corrected-controller-qualified.json` binding exact `16/16`,
same-callable proofs, corrected identity and every zero lock.

## 6. Evidence lifecycle and budgets

All outputs use exclusive-create, canonical UTF-8/LF bytes, file fsync,
directory fsync, strict reload, mode `0600` and no-clobber:

1. `progressive-00-root-created.json`;
2. `progressive-01-c4c1-dual-failure-accepted.json`;
3. `corrected-controller-v2.py` and `corrected-controller-v2.sha256.json`;
4. `controller-transform-delta.json` and its seal;
5. `dual-owner-negative-matrix.json` and its seal;
6. `progressive-02-corrected-controller-qualified.json`;
7. `terminal-evidence.json` and `terminal-evidence.sha256.json`.

The correction package's own terminal seal must be produced by one external
physical-seal writer using exact canonical LF, then non-following-opened,
strictly reloaded, canonical-byte compared and target-linked by the parent
before ER permission becomes true. On any post-root exception, preserve all
prior bytes and attempt one truthful failure terminal plus that same seal/gate.
If terminal or seal persistence/gating fails, append no ER and perform no
repair, retry, fallback or alternate-root action.

Success budgets:

```text
correction owner process/invocation = 1/1
root create = 1
C4-C1 root lstat/scandir/direct entries = 1/1/4
C4-C1 four artifacts lstat/open/read/hash = 4/4/4/4
C4-C1 strict parse attempts = 4; valid parses = 3; expected rejects = 1
old seal repair/rewrite/regenerate/copy/normalization = 0/0/0/0/0
frozen controller lstat/open/read/hash/decode/tokenize/AST parse = 1/1/1/1/1/1/1
frozen controller import/execute/copy/mmap = 0/0/0/0
corrected controller generation/write/seal = 1/1/1
corrected controller parse/compile = 1/1
corrected controller real main/C4/C4-C1 invocations = 0/0/0
transform delta/seal = 1/1
negative matrix = 16/16
matrix summary/seal = 1/1
C4 V3 payload/builder and C3/source/C1/C2/retained/decision reads = 0
canonical validator/helper/consumer/replay = 0
eligibility/release = 0/0
retry/fallback/second owner/root/controller = 0/0/0/0/0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1 only after a valid terminal seal gate; otherwise 0
```

Tests, compileall, CodeGraph, repository imports, network/DNS/`.env`/
credentials, device/camera/Ray/strip/cleanup/capture, FORMAL/public analyzer/
TD-C/sentinel/P8, firmware/deployment are all zero.

Any activation/input/failure-interpretation/AST-scope/transform/matrix/budget/
persistence mismatch hard-fails. After one valid terminal seal plus at most one
authorized ER append, stop exact
`B2_C4_C1_C1_DUAL_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`.

## 7. Acceptance and future lock

Planner may accept this package only if independent replay proves the immutable
C4-C1 dual failure, exact single controller transform, ancestor plus same-list
statement-scope ownership, canonical-LF strict reload/linkage gating for both ER
paths, exact `16/16`, valid new terminal seal, and every lock/counter.

Acceptance qualifies only one disposable corrected controller. A later PLAN
must authorize a brand-new-root corrected C4-C1 attempt; it may not reuse or
repair the rejected root and may not infer permission to read C4 V3 payload or
builder from this correction. C4, B2/B3, retained R3, canonical validator,
eligibility, release consumption, devices, FORMAL-R6, strip, TD-C, sentinel and
P8 remain hard locked.

## 维护性判断

This package keeps the two defects at their existing disposable-controller
ownership boundaries: AST scope selection and evidence lifecycle gating. One
correction owner avoids parallel lifecycle machinery, while the exact transform
delta and shared-callable matrix prevent duplicate selectors or success/failure
seal drift. No production refactor is authorized or needed.
