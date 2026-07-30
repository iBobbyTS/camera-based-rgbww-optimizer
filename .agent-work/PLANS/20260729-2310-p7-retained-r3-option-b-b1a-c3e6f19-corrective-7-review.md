# F19-C7 schema-subset 与 validation log lifecycle — Planner review archive

**Review time:** `2026-07-29T23:10:46-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-7-SCHEMA-SUBSET`

**Decision:** `REJECTED_VALIDATION_LOG_EXCLUSIVE_CREATE_THEN_NOCLOBBER_REOPEN_CONFLICT`

## Reviewed scope and method

C7 was authorized to validate activation lineage, parse the committed PLAN and FULL exactly once through the
committed helper, verify the exact 12-entry field ledger, prove the five immutable C2 artifact identities, and apply
required-field-subset semantics to the already-read C2 terminal JSON. After all pre-edit gates passed, it could retain
one dedicated-test correction and run one fresh fail-fast validation chain in a new C7 evidence root.

The Planner read AGENTS, the active PLAN/FULL, the single C7 execution-result append, the C7 terminal/evidence, and
the dedicated-test diff. It independently compared current controller/helper/test bytes with the frozen identities.
It did not access C3-C6 evidence roots, retained R3, candidate, release, network, devices, camera, Ray, strip, cleanup,
formal or public analyzer.

## Evidence and findings

- Activation lineage passed: child `2aff2aa9a1ad05e3c404ccb5893893190645bc6d`, direct parent
  `f61d08a19c5cc12a5c464d5ec6064884b1c6f4d9`, exact subject
  `chore(plan): activate f19 schema subset correction`, and changed path exactly `.agent-work/PLAN.md`.
- Committed PLAN/FULL helper calls were `1/1`; their candidate counts were `1/1`. The exact field-owner ledger passed
  `12/12` with membership, builtin-type identity and exact-value comparison.
- All five C2 identities passed: root `0700`, exact five-path set, regular/non-symlink files, artifact modes `0600`,
  bytes/SHA matches, and one `lstat` plus one bytes read per artifact. The C2 terminal bytes were reused for one JSON
  parse with no second file read.
- Required-field-subset crosscheck passed. Selector cardinalities were exactly one; listed fields passed exact
  membership/type/value checks; whole-record key sets were not compared, extras were not enumerated, and extra
  values were neither read nor used for inference.
- The only repository implementation diff is
  `tests/test_p7_retained_r3_exact_five_controller.py`. It preserves the AST lexical-owner proof and narrows `run`
  bytecode ownership to `execute_prepared_exact_five_controller` with exactly `STORE_FAST` and `LOAD_FAST`; global,
  name, attribute and method load prohibitions remain intact. This is the authorized semantic correction.
- Current dedicated-test SHA-256 is
  `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`. C7 terminal records this exact value.
  Controller and helper remain byte-exact at
  `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` and
  `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f` respectively.
- C7 root is
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-7-offline`, mode `0700`.
  It contains the exact nine expected regular `0600` artifacts. Terminal is strict JSON, sealed last, 3977 bytes,
  SHA-256 `85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369`.

## Failure interpretation

The validation owner exclusively created `compileall.log` at mode `0600`, then invoked a shell redirection that tried
to reopen the same path while zsh `noclobber` was active. That reopen was rejected before Python started. Therefore:

- compileall wrapper attempts: `1`, wrapper exit: `1`;
- actual compileall process invocations: `0`;
- targeted, focused, full, CodeGraph and diff-check invocations: all `0`;
- retry/fallback: `0`.

The unused log placeholders contain the terminal-not-run marker and do not prove command execution. The failure is a
local evidence-lifecycle ownership defect, not a test failure and not a scientific result.

## Execution-result identity discrepancy

The append-only C7 execution-result row reports dedicated-test after SHA
`48b0cb295538481998a79896db4fc53d8e4fa12f807a04b67620e54946eb2c38`. That value contradicts both the immutable C7
terminal and the current file bytes, which independently agree on
`19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`.

The old terminal and old execution-result append must not be rewritten. The next fresh package must emit one new
append-only superseding record that identifies the erroneous field/value, cites the immutable C7 terminal identity,
and binds the retained current test bytes before validation.

## Decision and exact next branch

C7 is rejected because no validation command ran. The schema, C2 identity, test edit and frozen-source gates are
accepted as prerequisites for the next package; the test edit must be preserved byte-exact rather than repeated.

Propose `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8`, a minimal validation-log-owner corrective:

1. preserve current test bytes at SHA-256
   `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` and preserve controller/helper bytes;
2. use a fresh C8 root only; C7 is read-only for exact terminal identity, while C3-C6 and retained/candidate/release
   paths remain forbidden;
3. create each validation log exactly once with exclusive semantics and mode `0600`, keep that same open file
   descriptor as the sole log owner, and route child stdout/stderr to it without reopening the path;
4. close/fsync the descriptor before identity calculation; do not combine an exclusive-create pre-step with later
   shell path redirection; fail closed on creation, descriptor or child-launch error;
5. run the same ordered fail-fast validation chain at most once per command, with retry/fallback `0`;
6. seal a new terminal artifact last and append a new superseding ER record on PASS or FAIL without altering C7.

## Validation quality, locks and residual risk

The C7 evidence strongly proves the gate and lifecycle failure, but it contains no test execution evidence. All
controller/candidate/R3/validator/eligibility/release/Git stage-or-commit/network/environment/device/camera/Ray/strip/
cleanup/formal/public-analyzer/TD-C/sentinel/P8 counters remain `0`; retained R3 stays
`RETAINED_UNVALIDATED_UNCONSUMED`.

No Advisor scientific decision or Human high-risk authorization is required. The next branch is offline validation
plumbing only. Controller execution, B2, retained-R3 consumption and all later scientific/device stages remain locked.

**Planner stop:** `F19_CORRECTIVE_7_REVIEWED_WAITING_ORCHESTRATOR_C8_ALIGNMENT_AND_ACTIVATION`.
