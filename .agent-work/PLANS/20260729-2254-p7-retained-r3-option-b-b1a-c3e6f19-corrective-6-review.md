# F19-C6 exact C2 terminal evidence-schema binding — Planner review archive

**Review time:** `2026-07-29T22:54:08-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-6-TERMINAL-SCHEMA`

**Decision:** `REJECTED_EXECUTION_SIDE_UNAUTHORIZED_WHOLE_RECORD_KEY_SET_ASSERTION`

## Reviewed scope and method

C6 was authorized to prove activation lineage, parse the committed PLAN and FULL once each through the committed
helper, validate the 12-entry owner ledger, verify the five immutable C2 artifacts, and parse the already-read C2
`terminal-evidence.json` bytes once. Its terminal crosscheck had to select manifest records by `path` and validation
records by `name`, then validate every field listed by the PLAN's record `field_schema` and `exact_fields`. Only after
that pre-edit gate passed could it edit the dedicated test and run one fresh fail-fast validation chain.

The Planner read AGENTS, the active PLAN/FULL, the single C6 execution-result append, and the frozen C2 terminal JSON.
It did not access C3-C6 evidence roots, candidate, retained R3, release, network, devices, camera, Ray or strip.

## Evidence and findings

- Activation lineage passed: child `3f6e7f1d954d886cdf26a90fb32a2254f66b2717`, direct parent
  `673de40fc78ecf8359dbb92d0fc3b830c2efdeb5`, exact subject
  `chore(plan): activate f19 terminal schema correction`, and changed path exactly `.agent-work/PLAN.md`.
- The committed helper was imported directly; PLAN/FULL calls were `1/1`, candidate counts were `1/1`, and helper
  SHA-256 was `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`.
- The exact owner ledger passed `12/12`. The five frozen C2 artifact identities, root `0700`, artifact modes `0600`,
  exact path set, regular/non-symlink checks and one-lstat/one-read discipline all passed.
- `terminal-evidence.json` was parsed once from the already-read bytes; no second read occurred. Top schema, both
  exact collection paths and lengths, dict record types, and the compileall manifest/validation selectors all passed.
- Controller, helper, dedicated test and C2 terminal identities were unchanged. Repository edits, C6 root/artifacts,
  compileall, targeted/focused/full tests, CodeGraph and diff check were all `0`.
- Retry/fallback were `0`. C3/C4/C5 access, candidate/R3/release, validator/eligibility, Git mutation, network,
  environment, devices and every scientific-stage call were `0`. Retained R3 stayed
  `RETAINED_UNVALIDATED_UNCONSUMED`.

## Contract interpretation and legal extra fields

The C6 `terminal_schema_contract.records[*].validation.field_schema` lists seven **required** fields:
`name`, `log`, `log_bytes`, `log_sha256`, `log_mode`, `invocation_count`, and `exit_code`. The prose contract says each
record is validated "按冻结 field schema" and the machine contract requires path-specific type/value checks. Neither
the machine contract nor prose requires the complete record key set to equal those seven keys.

Both immutable validation records also contain exactly one observed extra key:

| Selected validation record | Legal extra key | Actual builtin type | Binding effect |
| --- | --- | --- | --- |
| `name == "compileall"` | `argv` | `list` | none |
| `name == "targeted_unittest"` | `argv` | `list` | none |

`argv` is command metadata. It is not the selector, file binding, bytes/SHA/mode identity, invocation count, or exit
status owner. The artifact's already-proven whole-file bytes/SHA binds its presence and content, so ignoring `argv`
for the field-binding crosscheck does not weaken the immutable-evidence proof. The manifest records have no observed
extra keys, but C6 likewise did not authorize whole-object key-set equality there.

The runner added `set(record.keys()) == set(field_schema.keys())` (or equivalent), rejected the legal `argv`, and
failed before any listed field check. This assertion was not in PLAN and changed required-field subset validation
into an unauthorized closed-object schema.

## Decision and next branch

C6 is rejected because it did not reach the authorized test-only correction or fresh validation chain. Its failure
does not contradict activation, helper, owner-ledger, C2 identity, selector, cardinality or collection-schema proofs.

Propose `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7`, a minimal schema-subset corrective. It must freeze:

1. every listed `field_schema` key is required and must pass direct membership, exact builtin type identity, and exact
   value comparison against the corresponding `exact_fields` value;
2. record validation is a required-field subset operation, never whole-object exact key-set equality;
3. extra fields do not participate in selector or identity binding and must not cause rejection; the current frozen
   records' observed legal extra is `argv:list` for both validation rows;
4. the runner must not enumerate extras to create a second acceptance gate, infer bindings from extras, or inspect
   `argv` content; immutable file bytes/SHA already own the complete payload;
5. all previous single-read, exact-path, selector, cardinality, owner and zero-lock contracts remain unchanged.

After the gate passes, the next package retains the same one-file test-only lexical-local `run` correction and one
fresh fail-fast validation chain. This is an engineering/provenance issue; Advisor guidance and Human authorization
are not required.

## Residual risks and stop point

- C6 runner source was ephemeral, so its extra assertion is evidenced by the terminal report and exact failure point,
  not retained source. C7 removes ambiguity by making subset semantics and extra-field non-binding explicit.
- No implementation or scientific progress occurred in C6. Controller execution, B2, candidate/retained R3,
  release, validator/eligibility, FORMAL-R6, strip, public analyzer, TD-C, sentinel and P8 remain locked.
- Planner stop: `F19_CORRECTIVE_6_REVIEWED_WAITING_ORCHESTRATOR_C7_ALIGNMENT`.
