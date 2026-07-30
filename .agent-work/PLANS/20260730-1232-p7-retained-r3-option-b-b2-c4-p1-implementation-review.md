# REF-P7-25-R2-B2-C4-P1 implementation review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-C4-P1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-REPO-OWNED-PREPARATION-V1`

**Reviewed PLAN identity:** bytes `11953`, SHA-256
`a15fd78a0d7bcc614400da1fab0529e3edf140d9c3000f2b068f1e8961f789b2`.

**Planner decision:** `REJECTED_BOUNDED_P1_CORRECTION_REQUIRED`.

**Exact next branch:** `REF-P7-25-R2-B2-C4-P1-C1`, a pure offline
exact-two-path corrective commit. C4 integration, real B2, retained-R3 audit,
B3, eligibility, release consumption and device work remain locked.

## 1. Reviewed scope and implementation method

The Executer created exactly the two authorized regular repository files:

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py
tests/test_p7_retained_r3_controller_preparation.py
```

The focused implementation commit is
`ce096155227d4f24f1d6659550319aaf335d014b`, with exact parent
`aa0baf80aa7c83fe094ce139c5a14d04f13c67dd`, exact subject
`feat(p7): add retained r3 controller preparation owner`, and no third path.
The source/test blob SHA-256 values independently match the committed worktree
bytes:

- helper: `e60a0e10519a8c8a609acc45170b142bc7aa49484016de4319f7979e6a1def06`;
- dedicated test: `6c0bb5f6b699767e1779466fa54f066076acea81df3afddd59612dd6450ebe2b`.

The helper follows the requested pure in-memory shape: typed AST edges and byte
spans, canonical terminal serialization, target linkage, internal validated
gate and injected ER callback. It does not import or call filesystem, process,
network, device, release or canonical-validator owners. The existing canonical
lineage validator remains the sole eligibility owner.

## 2. Evidence and validation quality

The sole P1 handoff in `.agent-work/EXECUTION_RESULT.md` reports:

- targeted `17/17`, exit `0`, precommit and postcommit;
- related focused `11/11` and `21/21`, exit `0`;
- full suite `708/708`, exit `0`;
- compileall, CodeGraph sync and both diff checks exit `0`;
- exact one commit and exact two changed paths;
- historical controller/retained-R3/validator/eligibility/release/network/device
  operations all `0`.

Planner did not rerun tests or access external evidence. Independent read-only
review used Git topology/blob checks, CodeGraph source/call inspection, committed
source/test inspection and `git diff --check`. The only pre-review worktree drift
was the truthful unstaged Executer append to `.agent-work/EXECUTION_RESULT.md`.

This is strong execution evidence, but green tests do not close untested
fail-open identity and ownership cases.

## 3. Planner findings

### REV-P1-001 — exact target linkage is value-equal but not type-exact

`validate_terminal_seal` compares the parsed target dict with the expected dict
using ordinary Python dict equality. JSON `true` equals integer `1`, and JSON
`123.0` equals integer `123`; therefore `bytes`, `device` or `inode` can change
JSON type while passing the purported exact five-field linkage. The dedicated
test varies values but does not cover bool/float substitutions. Provenance target
identity must compare exact key set, exact field types and exact values.

### REV-P1-002 — nested regular functions do not reject multiple owners

`_regular_function_owner` returns the first `FunctionDef` ancestor. An assignment
inside a nested regular function has both inner and outer regular-function
ancestors, yet is accepted. This contradicts the PLAN requirement to establish
one unique enclosing regular-function owner and reject multiple-owner ambiguity.
The current “multiple” test covers multiple assignments, not multiple enclosing
function owners. Statement nesting inside `if`/`for` remains valid; nested
function ownership must fail closed.

### REV-P1-003 — the validated gate payload is only shallowly immutable

`_ValidatedSealGate` freezes the dataclass and wraps only the outer payload dict.
Nested dict/list values, including the linked `target`, remain mutable through
the callback-visible gate. This permits post-validation mutation of the object
that represents seal acceptance. Recursively freeze JSON containers or expose
an immutable typed snapshot, and prove mutation attempts cannot alter it.

### REV-P1-004 — malformed replacement entries can escape the typed error owner

`replace_byte_spans` sorts entries by `item.span.start` before it verifies every
entry is a `SourceReplacement`. A malformed caller-supplied sequence can raise
`AttributeError` during sorting instead of the helper's stable fail-closed
`ControllerPreparationError`. Validate entry types before dereference/sort and
cover this case.

The dedicated static import assertion also derives imported names incorrectly
for `ImportFrom` nodes by inspecting aliases rather than `node.module`. The
current helper is independently clean, so this is not an active forbidden import,
but the correction must make the guard accurately detect forbidden `from ...`
imports.

## 4. Residual risks and acceptance boundary

No evidence suggests production execution, eligibility ownership, retained-R3
bytes or devices were touched. The defects are confined to the new helper and
its dedicated test and can be corrected without widening scope. Until a focused
successor closes them, P1 is not accepted as an exact provenance preparation
boundary and cannot be bound into C4 integration.

The next Planner package must permit only those same two paths, one successor
commit directly parented by `ce096155...`, meaningful regression additions,
the original validation gates and a Planner review stop. It must not execute or
read historical controllers/evidence.

## 5. Exact stop

`B2_C4_P1_REJECTED_C1_WAITING_EXECUTION`
