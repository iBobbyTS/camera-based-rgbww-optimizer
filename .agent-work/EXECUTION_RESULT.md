# EXECUTION_RESULT

## Terminal status request

`STOPPED_FOR_ORCHESTRATOR_VISIBLE_TERMINAL_REPACKAGING_NOT_A_CANDIDATE_REJECTION`

- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1`
- Phase reached: `TARGETED_COMPLETE_BEFORE_FOCUSED`
- Planner stop requested: return to Orchestrator for visible-Terminal validation
  repackaging because measured validation duration makes the original
  under-10-minute packaging no longer credible.

This is a long-task packaging stop required by PLAN section 7. It is not a
candidate rejection, production-seam failure, scientific/formal failure,
device failure, GUIDE hard stop, or permission request. The implementation is
left intact for the next bounded package; it is not accepted or committed.

## Activation intake

- Branch: `main`
- Activation HEAD: `7214ff5eb797d2716d7b9d4bdb34324f5febe350`
- Activation tree: `d9dc5dcf0e2177a11f2b6651fe707fdca8b8ef6e`
- Sole parent: `f5e85bc4b2aca501725b239b8f7515513bacaee6`
- Subject: `docs(plan): activate Route A final code first`
- Exact activation changed paths:
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/EXECUTION_RESULT-20260804-1817.md`
  - `.agent-work/archived/FULL_PLAN_REFERENCE-20260804-1820.md`
  - `.agent-work/archived/PLAN-20260804-1817.md`
  - `.agent-work/archived/PLAN-20260804-1827.md`
- PLAN/FULL strict machine state at intake: active `1/1`, exact task
  `REF-G4-06-RAY-R6`, exact contract
  `G4-RAY-R6-FINAL-CODE-FIRST-FINAL-PACKAGE-REMINT-V1`; PLAN executable and
  FULL non-executable; required FULL subset exact.
- PLAN identity: `16498` bytes, SHA-256
  `197e404da2da194a3ea44aad2ef813f58cc0ce250b05aaba20c4ab502ec13afe`.
- FULL identity: `15183` bytes, SHA-256
  `b565ab837ee9584f6f8384a790166701991c205c690203c96238ab8411563d22`.

## Supervisor archive and accepted-tree restore

The rejected successor candidate remains recoverable and was not reused:

- Ref: `refs/archive/g4-06/source-successor-candidate-supervisor-superseded-20260804`
- Commit/tree/parent:
  `88185fceeed8630e5df35a83126df181bed0cd68` /
  `35d0a46c081a91e5c0f930924cde223ada59be15` /
  `f5e85bc4b2aca501725b239b8f7515513bacaee6`
- Subject: `archive(g4-06): preserve supervisor-superseded source successor candidate`
- Exact paths: the stage-gate source and its test file only.
- Archived source: `116366` bytes, SHA-256
  `a5ec111167fa20f34914a481face68e1d2c276688c74ead434d9effdc5e7b0d3`,
  blob `c35684a639ab8f40200f9ed5be6c1196ad08c568`.
- Archived test: `149152` bytes, SHA-256
  `a6107c9f3290a63921fd94911f729c9d69dffcfc59d9e841010d4e6ee0eb009d`,
  blob `da973e2748c2d814cb4b78354cea52e6e014458e`.
- Binary diff: `59839` bytes, SHA-256
  `eb907ac5b2059beed39646a0b181d43d1af37b96e25c3a9c35b12e64e7fbb9c2`.

The reviewed reverse diff was applied non-destructively with `apply_patch`.
Both restored files then matched HEAD byte-for-byte:

- source: `93155` bytes, SHA-256
  `406ac5c82ac9a098052a812af866f29083bdb2ee3fd5962964c8889100ef5d37`,
  blob `c12c4f19bfa422a1fe38378ed3ae243f7982e9aa`, mode `100644`;
- test: `130254` bytes, SHA-256
  `ff3964db91ba2bd19073be16eb4a45aa7ae81a96c2ff17cb54b108f4cf2915c3`,
  blob `a6f3432ba6ce00946901cf786bb67b26e8857356`, mode `100644`.

One bounded tooling correction occurred: the first `apply_patch` rejected
standard unified hunk headers and made no modification; the same reviewed
reverse diff was resubmitted with tool-compatible hunk headers and succeeded.
This is a patch-harness formatting correction, not a production seam failure.

## Implemented candidate and ownership

Maintainability preflight found that the change belongs in the existing
`_source_attestation_binding` -> `_committed_source_contract` ->
`_validate_descriptor_attestation_contract` ->
`validate_committed_source_attestation` owner path. No module, controller,
adapter, successor chain, second attestation, new schema, global override,
environment override, or `validate_current_sources=False` mode was introduced.

The candidate:

- admits exactly the existing preparation subject and the frozen final subject
  `fix(stage-gate): bind final package to immutable code snapshot`;
- adds a closed, ordered `code_child_blob_oids` declaration for the existing
  exact two paths to the existing binding and descriptor mirror;
- validates actual commit subject and exact paths against that immutable
  binding;
- validates each Git `ls-tree` blob OID before the existing mode, bytes,
  SHA-256, and current-file identity checks;
- preserves the single existing loader/launch attestation owner and the
  existing delegate-exactly-once production seam.

Observed diff before this stop was limited to the stage-gate source and its
test: overall `102` insertions and `9` deletions; production source accounting
was `34` insertions and `8` deletions, below the `150`-line soft cap.

Tests add the final-subject positive production-delegation case, exact declared
OID checks, missing OID rejection, and wrong OID rejection while preserving the
original preparation-subject behavior and existing topology/blob/history
negative matrices.

Final candidate source/test byte counts and SHA-256 values were not sampled
before the mandatory long-task stop. They must be recorded by the next
authorized package without changing the candidate first.

## Validation evidence and duration stop

- Compile command completed with exit `0`:
  `.venv/bin/python -m py_compile src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py tests/test_p7_td_b_r6_stage_gate.py`
- Targeted command completed with exit `0`:
  `.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_stage_gate`
- Targeted result: `47/47`, `OK`, `182.148s`.
- `git diff --check` was observed clean immediately after targeted completion.
- A preliminary `python3 -m unittest` attempt failed to import the editable
  package because system Python was used; it is not a PLAN validation and not a
  product/test failure.
- A preliminary `.venv/bin/python -m pytest` observation reported that pytest
  is not installed. It is not a PLAN validation, dependency installation was
  not attempted, and it is not a product/test failure.
- Focused integration was **not started**.
- Fresh full suite was **not started**.
- The earlier Supervisor-interrupted full remains
  `INTERRUPTED_UNPROVEN_NOT_REUSABLE`; it was not resumed, supplemented, or
  interpreted.
- CodeGraph had been synced after accepted-tree restoration and confirmed the
  existing sole owner path before implementation. Required post-change sync and
  query were **not run** because execution stopped before that validation phase.

The focused command must run the same measured 182-second stage-gate module
again plus two additional modules, followed by the required one fresh full
suite. At this evidence boundary it became reasonable to expect the original
package's total validation time to exceed 10 minutes. PLAN section 7 therefore
requires stopping before those commands and returning to Orchestrator for
visible-Terminal repackaging. No Codex-managed background validation remains.

## Zero-access and zero-effect counters

- External experiment/package/formal root access/read/stat/list/create: `0`
- Network/device/camera/Ray/strip/capture calls: `0/0/0/0/0/0`
- Release/retained-R3/formal-R6/analysis/TD-C consumption or execution:
  `0/0/0/0/0`
- Backend/final-zero/cleanup/formal-owner calls: `0/0/0/0`
- New experiment/package/formal roots: `0/0/0`
- New task IDs/corrective suffixes/controllers/adapters: `0/0/0/0`
- Git stage/commit/push/PR: `0/0/0/0`

PLAN, FULL, GUIDE, RESEARCH, and archives were not modified. No hardware,
release, formal, scientific, eligibility, or readiness claim is made.

## Orchestrator handoff

Repackage only the remaining validation and evidence-finalization work under
the visible-Terminal long-task rule. Preserve this exact candidate and the same
reference task; do not create a corrective suffix or revive the rejected
successor candidate. The future immutable code checkpoint subject remains:

`fix(stage-gate): bind final package to immutable code snapshot`

with exact commit paths:

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_p7_td_b_r6_stage_gate.py`

No future checkpoint or tree SHA is guessed.
