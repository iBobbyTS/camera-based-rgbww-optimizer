# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1 Planner review archive

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-DEFERRED-ER-APPEND-IMMUTABLE-VALIDATION-CLOSURE-V1`

**Reviewed stop:** `B2_P7_C1_C1_C1_C1_V1_C1_V1_C1_DEFERRED_ER_APPEND_IMMUTABLE_VALIDATION_WAITING_PLANNER_REVIEW`

**Planner decision:** `REJECTED_GATE_HARNESS_MARKDOWN_MACHINE_ROW_REGEX_DEFECT_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`

## 1. Reviewed scope and frozen inputs

The validation-only package activated at commit
`30aa4f281f6fe2fb825ba2240cfce779fdba47e4`, direct parent
`045915dae74b14c9a56d6524d5573a5bdeade4d4`, subject
`chore(plan): activate p7 deferred er append validation closure`, with the exact
three paths:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260731-1819-p7-retained-r3-b2-p7-pregate-append-order-failure-review.md`

The active package kept candidate
`864f08cc5436519a37e41d553e49ebde4a3c8bb2` immutable. Its parent, subject and
exact two-path set remained frozen, as did the canonical binary diff, source
and test identities, canonical template identity and exact-spec replacement
identity recorded in the reviewed PLAN. Code/test writes, implementation
commits, CodeGraph, retry/fallback and every external/retained/device effect
were exact zero.

The activation HEAD remained
`30aa4f281f6fe2fb825ba2240cfce779fdba47e4` and the worktree remained clean.
There was no current-run ER append or evidence commit. The unchanged ER was
bytes `1129765`, SHA-256
`954e378e23fd9dfc4f6bf0f50da765076db54d5c62030995207c983f674c76b3`.

## 2. Evidence source and gate result

Because the Executer correctly produced no ER byte for this rejected package,
the evidence source is the same Executer terminal's source-backed diagnostic,
reviewed together with the unchanged activation HEAD and the committed PLAN/FULL
rows. The diagnostic stopped at gate line 155:

```python
assert plan_match and full_match
```

Both values were `None`. Before that line, the candidate semantic, activation
and identity checks; source/test AST and compile checks; `_plain` physical
NUL/LF/CR checks; public negative/positive boundary; canonical template and
replacement checks; exact matrix/test checks; and runnable lifecycle checks
had passed. Fresh targeted, focused, compileall and full-suite invocations were
therefore correctly held at zero. External effects were zero.

The committed machine rows are not bare marker lines. Each is a Markdown inline
code row with one leading backtick before `PLAN_MACHINE_CONTRACT=` or
`FULL_PLAN_MACHINE_STATE=` and one trailing backtick after the JSON object.
The failed gate regex expected bare marker-plus-JSON lines, so it could not match
either authoritative row. Current files contain exactly one PLAN machine row
and exactly one FULL machine row.

## 3. Validation quality and decision

The failure is a gate-harness domain defect, not candidate semantic evidence.
It occurred after all preceding candidate gates passed and before any regression
test was invoked. No candidate byte may be repaired, regenerated or reclassified
from this result.

The package is rejected because it did not complete the required fresh gate and
regression sequence. Candidate `864f08c...` remains immutable and
non-consumable; retained R3 remains unvalidated/unconsumed. No integration,
canonical validator, eligibility, release or device stage is unlocked. This is
an offline engineering validation issue and requires neither Advisor scientific
direction nor Human device authorization.

## 4. Exact successor branch

Authorize one subordinate validation-only successor over the same immutable
candidate. It must change no code/test bytes and create no implementation commit.
Its only harness correction is to match the exact committed Markdown line
domain:

- PLAN pattern: `^\`PLAN_MACHINE_CONTRACT=(\{[^\r\n]*\})\`$`
- FULL pattern: `^\`FULL_PLAN_MACHINE_STATE=(\{[^\r\n]*\})\`$`

The leading `^`, literal opening backtick, exact marker, captured one-line JSON
object, literal trailing backtick and terminal `$` are all required. The gate
must require exactly one match in the PLAN and exactly one match in FULL, then
decode those captured JSON objects strictly. It must not add a generic Markdown
parser, permissive path, alternate marker form, fallback, row repair or row
regeneration.

The successor must preserve delayed evidence ordering: all observations stay in
memory, initial clean and the full validation sequence must reach terminal
before any ER byte, and the success path performs one EOF append containing the
real `PRE_GATE_LOGICAL_EXIT=0` marker exactly once. If initial clean fails, ER
writes remain zero; if a later stage fails, no retry or repair is permitted.

After a fresh gate logical exit `0`, run exactly once and in order:

1. targeted domain-template suite, exact `11/11`;
2. focused six-module suite, exact `93/93`;
3. compileall, exit `0`;
4. unified full suite, exact `778/778`;
5. final candidate identities and clean-porcelain checks;
6. one delayed EOF append, then stop for Planner review.

Implementation commit, postcommit testing, CodeGraph sync/query, retry/fallback,
external controller/root, retained reads, validator, release and device effects
remain exact zero.

## 5. Residual risks and locks

The primary residual risk is accepting a looser regex that matches a malformed,
duplicated or non-Markdown row. Exact delimiters plus strict one-row cardinality
are therefore part of the acceptance contract. The other residual risk is
reintroducing observer-induced worktree dirtiness; the deferred ER byte-ordering
contract remains unchanged.

Old failed controller/root/evidence paths, retained R3, candidate payload, Git
provenance replay, real B2, subordinate manifest, canonical validator,
eligibility, retained audit, all release work, network, DNS, environment,
credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public
analyzer, TD-C, sentinel, P8, firmware and deployment remain hard locked zero.

Maintenance assessment: the successor changes only the ephemeral validation
harness expression. It adds no production/test owner, serializer, helper,
fallback or parallel execution path.
