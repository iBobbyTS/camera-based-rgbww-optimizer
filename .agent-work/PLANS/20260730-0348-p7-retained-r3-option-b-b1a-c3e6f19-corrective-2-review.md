# F19-C2 helper-owned test correction review

**Planner review UTC：** `2026-07-30T03:48:11Z`

**Reviewed reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-2-HELPER-GATE`

**Verdict：** `REJECTED_TEST_ONLY_FALSE_POSITIVE_STORE_FAST_LOCAL_BINDING`

## 1. Reviewed scope and method

Planner reviewed the committed active PLAN at HEAD
`99a741e74e72e4e0200c8dcb0e952d08124b7f13`, the Orchestrator-owned FULL reference,
the single Executer append in `.agent-work/EXECUTION_RESULT.md`, the dedicated test diff,
the frozen controller source around `execute_prepared_exact_five_controller`, and only the
C2 evidence root:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline`

Planner did not run the controller, tests or validator; did not read candidate, retained-R3
or release paths/payloads; and did not access network, environment credentials or devices.

## 2. Gate, identity and validation evidence

The activation/helper gate is accepted:

- actual child/parent: `99a741e74e72e4e0200c8dcb0e952d08124b7f13` /
  `5d6fa3d8e317a7f176c2849781bc47f3d97f3c25`;
- activation changed path: exactly `.agent-work/PLAN.md`;
- committed helper calls: PLAN `1`, FULL `1`;
- helper candidate counts: PLAN `1`, FULL `1`;
- frozen FULL SHA-256:
  `6932a0e9d6b0bf30e07afe3f4aadd8314ce26b43e167a2a3b20f849369147751`;
- retained status: `RETAINED_UNVALIDATED_UNCONSUMED`;
- candidate-contract flag: `true`.

The implementation path set is exactly the dedicated test. Controller source stayed byte-exact:

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647` | `e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6` |

Validation stopped fail-fast after:

- compileall: one invocation, exit `0`;
- targeted unittest: one invocation, `11` run, `10` pass, `1` failure, `0` errors;
- focused/full unittest, CodeGraph and diff-check: zero invocations;
- retry/fallback: `0`.

## 3. Root cause and bytecode-owner decision

The one failure is a false positive in the new dedicated static regression, not a controller
defect. The controller defines exactly one lexical nested local function named `run` directly
inside `execute_prepared_exact_five_controller`, then calls that local helper from the same
function. Python therefore legitimately emits both:

- `STORE_FAST run` in `execute_prepared_exact_five_controller` when binding the nested function;
- `LOAD_FAST run` in the same owner for local-helper call sites.

The C2 test already proves by AST that there is exactly one `def run`, it is directly nested in
the execute function, and every `Name("run")` call is owned by that execute function. It separately
rejects forbidden imports, global/name loads and attribute/method loads. Its final assertion is
incorrect only because it permits `LOAD_FAST` but excludes the legitimate definition-time
`STORE_FAST`.

The next test must permit the exact owner/opcode set
`{("execute_prepared_exact_five_controller", "STORE_FAST"),
("execute_prepared_exact_five_controller", "LOAD_FAST")}` and reject every other owner or opcode
for argval `run`. It must continue rejecting `LOAD_GLOBAL run`, `LOAD_NAME run`, `LOAD_ATTR run`,
`LOAD_METHOD run`, subprocess-like attribute calls, forbidden imports and direct I/O. No generic
path/callee allowlist, string-absence replacement or controller rename is accepted.

## 4. Evidence integrity and zero-lock audit

The C2 root is mode `0700`; all five artifacts are regular mode `0600` and remain the immutable
old evidence for the next package:

| Artifact | SHA-256 |
| --- | --- |
| `activation-gate.json` | `cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c` |
| `pre-validation.json` | `16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2` |
| `compileall.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `targeted_unittest.log` | `60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48` |
| `terminal-evidence.json` | `41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6` |

Controller calls/edits, candidate/R3 reads, validator calls, eligibility emission, manifest writes,
commits/stages, release/network/env/device/camera/Ray/strip/cleanup/formal/public-analyzer calls are
all `0`. These counters and the unchanged controller identity support rejection without consuming
any later-stage authorization.

## 5. Decision and exact next branch

C2 is rejected. The smallest next branch is
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3`, a dedicated-test-only correction that starts from current
test SHA `e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6`, preserves controller
SHA `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`, creates only the absent
fresh root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-3-offline`,
and runs the complete compile/targeted/focused/full/CodeGraph/diff-check chain exactly once and
fail-fast with retry `0`.

The Orchestrator must first align FULL to C3 and commit the current C2 evidence/test work. A fresh
Planner activation pass must then freeze that aligned FULL and activation lineage before any
Executer dispatch. No Advisor or Human decision is required: this is a local test-semantics issue,
not color/measurement science or a dangerous device operation.

**Residual risk：** C3 is not dispatchable until Orchestrator FULL alignment and a subsequent
Planner activation commit. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; real controller,
validator, release consumption and B2 remain locked.

**Planner stop：** `F19_CORRECTIVE_2_REJECTED_WAITING_ORCHESTRATOR_FULL_ALIGNMENT`.
