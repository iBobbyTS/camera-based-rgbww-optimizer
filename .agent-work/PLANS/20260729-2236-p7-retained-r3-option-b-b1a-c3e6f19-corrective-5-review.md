# F19-C5 exact C2 evidence-identity binding — Planner review archive

**Review time:** `2026-07-29T22:36:50-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-5-EVIDENCE-IDENTITY`

**Decision:** `REJECTED_EXECUTION_SIDE_UNFROZEN_TERMINAL_SCHEMA_CARDINALITY_ASSUMPTION`

## Reviewed scope and method

C5 was authorized to parse committed PLAN/FULL through the committed helper exactly once each, prove the exact
12-entry field ledger, bind the five immutable C2 artifacts to PLAN-owned expected bytes/SHA values and current
actual bytes/SHA values, cross-check the C2 terminal manifest and validation records, then make only the dedicated
test's lexical-local `run` correction and run one fresh fail-fast validation chain. C3/C4 evidence, controller,
candidate, retained R3, release and all device/scientific paths remained locked.

The Planner independently read the active PLAN/FULL and the single C5 execution-result append. It accessed only the
allowed C2 five-artifact root, recalculated its exact path set, modes, bytes and SHA-256 values, and parsed the C2
activation, pre-validation and terminal JSON. It did not access C3/C4, candidate, retained R3 or release paths.

## Evidence and findings

- Activation lineage passed: child `361d92fe2df68e0cdc7c648940bc749e0cefb48d`, direct parent
  `fce0a150451cbdcac1027224086374746bcfd698`, subject
  `chore(plan): activate f19 c2 evidence identity correction`, changed path exactly `.agent-work/PLAN.md`, initial
  porcelain clean.
- Helper calls were PLAN `1` and FULL `1`; candidate counts were `1/1`; committed helper SHA-256 was
  `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`.
- Exact field-owner ledger passed `12/12`; the retained state remained
  `RETAINED_UNVALIDATED_UNCONSUMED` and the candidate contract remained Orchestrator-verified.
- C2 root mode was `0700`, exact path set passed, and all five artifacts were regular non-symlink mode `0600`.
  Their expected and actual identities all passed:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `activation-gate.json` | 3243 | `cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c` |
| `pre-validation.json` | 670 | `16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2` |
| `compileall.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `targeted_unittest.log` | 3108 | `60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48` |
| `terminal-evidence.json` | 2519 | `41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6` |

- C5 stopped before repository edit and fresh-root creation: helper/test/controller edits `0`, implementation diff
  paths empty, C5 root/artifacts `0`, and every validation command `0`.
- Controller, helper and dedicated test identities were unchanged. C3/C4 access, candidate/R3/release,
  validator/eligibility, manifest, Git mutation, network, environment and every device/scientific counter were `0`;
  retry/fallback were `0`.

## Exact C2 terminal schema and root cause

The active PLAN required a cross-check of compileall/targeted identities in the C2 terminal manifest and validation
record. It did not require a recursive count of two identical JSON objects or two locations with the same field
names. The immutable C2 `terminal-evidence.json` stores the two views with intentionally different schemas:

- manifest entry: `artifact_manifest_before_terminal`, exactly one object selected by `path == <log name>`, with
  identity at `bytes` and `sha256` (and mode at `mode`);
- validation record: `validation`, exactly one object selected by `name == <command name>`, with file binding at
  `log`, identity at `log_bytes` and `log_sha256` (and mode at `log_mode`).

For `compileall.log`, these exact paths both bind bytes `0` and SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. For `targeted_unittest.log`, they both bind
bytes `3108` and SHA-256 `60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48`.
The C5 runner instead required two recursively discovered locations carrying one common complete bytes/SHA shape,
reported only one, and failed. That repetition/cardinality inference was not frozen by PLAN and does not reflect the
actual C2 schema. The already-proven parsed-PLAN identity plus current actual identity is sufficient for the five-file
integrity gate; the exact two-view cross-check additionally proves the terminal file bindings without requiring
schema homogeneity.

## Decision and next branch

C5 is rejected because it did not reach the authorized test-only correction or validation chain. The failure does
not contradict the C2 evidence identities and does not authorize repairing, regenerating or rewriting C2.

Propose `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6`, a minimal evidence-schema corrective. It must freeze the exact JSON
paths, selectors, cardinality and field names above for compileall and targeted only. The runner must parse the
already-read `terminal-evidence.json` once, select exactly one manifest row and one validation row per command, and
compare those path-specific fields to the one parsed-PLAN expected identity and the already-computed actual identity.
Recursive occurrence counting, duplicate-shape inference, generic searching and a second C2 file read are forbidden.
After the gate passes, the package retains the same one-file test-only lexical-local correction and one fresh
fail-fast validation chain.

This is an engineering/provenance issue. Advisor guidance and Human authorization are not required. Orchestrator must
align FULL to C6, organize and commit the reviewed state, and request a fresh Planner activation before dispatch.

## Residual risks and stop point

- C5 runner source was not retained, so review proves the assumption from its terminal report rather than source;
  C6 closes the ambiguity by freezing exact JSON paths and rejecting occurrence-count inference.
- C5 made no implementation or scientific progress. B2, controller execution, candidate/retained R3, release,
  validator/eligibility, FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.
- Planner stop: `F19_CORRECTIVE_5_REVIEWED_WAITING_ORCHESTRATOR_C6_ALIGNMENT`.
