# F19 exact-five controller preparation failure — Planner review archive

**Review time (UTC):** `2026-07-30T03:15:59Z`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CONTROLLER-PREPARATION`

**Verdict:** `REJECTED_DEDICATED_STATIC_TEST_FALSE_POSITIVE`

## Reviewed scope and method

Planner independently reviewed the active `PLAN.md`, Orchestrator-owned
`FULL_PLAN_REFERENCE.md`, the single F19 `EXECUTION_RESULT.md` append, the two
new untracked implementation paths, and only the frozen F19 preparation evidence
root:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-preparation-offline`

The review did not read or stat retained R3, candidate payloads, lineage release,
release consumers, canonical validator inputs, devices, camera, Ray, strip,
network, environment or later-stage paths. It did not rerun the F19 controller,
compileall, unit tests, CodeGraph sync, public analyzer or any Git mutation.
Read-only Git, SHA-256, strict-JSON, source AST and diff-structure checks were used.

## Frozen dispatch identity

- Dispatch HEAD: `1b38baa28e80c164656215500657031608c9692c`.
- Direct parent: `2457844a5f0f1c9c279348dd4d5b5e2c5b4f393b`.
- Subject: `chore(plan): activate f19 controller preparation`.
- HEAD changed-path set: exactly `.agent-work/PLAN.md`.
- Reviewed PLAN SHA-256: `a641fce40be077fb50bb47d69e1ba8dc17e8d6077a000bb1f47f3f60f68fb45b`.
- Reviewed FULL SHA-256: `05d9d3458d71a176ffd197aeb46fdf812a7b34e226ee62fc3aa5094d67f6adc6`.
- Dispatch porcelain SHA-256 was the empty digest
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Accepted bootstrap record SHA-256:
  `56fb1c806db56ce7f68240c1a35b4443dc4c41806bd4bb3107e85a095a8ecf97`.
- Accepted bootstrap seal SHA-256:
  `568a32cab44be41322f51be3e812a044e3976c7689a2ffd8b49fad2ab379cca4`.
- Candidate contract was used only as opaque identity
  `3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225`.

The dispatch/bootstrap artifact independently reports the accepted fixed container
as the same device/inode, mode `0700`, empty, with fallback absent by `lstat`.
PLAN/FULL were each parsed once by the committed machine-contract helper. All
pre-edit absence gates passed before the evidence root or implementation paths
were created.

## Frozen implementation and evidence identity

The exact repository diff path set at terminal was:

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py`
2. `tests/test_p7_retained_r3_exact_five_controller.py`

| Path | bytes | SHA-256 |
| --- | ---: | --- |
| controller source | `13477` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| dedicated test | `13268` | `579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647` |

Evidence root mode is `0700`. Every present artifact is a regular non-symlink
file with mode `0600`:

| Artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `00-dispatch-and-bootstrap-replay.json` | `1920` | `b4f6557fbc7a3a8dc1718c472900ea4d24045a9da6373a62b984889d2a32ffaa` |
| `01-controller-source-identity.json` | `981` | `3feba60353c1307a5809c86f1b2a1607574e27345109580632e120176b00cc00` |
| `02-targeted.log` | `2887` | `ea1c8715a6cf27c66e6ad038803b9af85331561fbd90e254ced492bd3ff82ba7` |
| `06-validation-summary.json` | `1919` | `8c1d2090611e3c08c8028384a2d766d96a373752798d695f31175fcb0979bcfe` |
| `07-terminal-summary.json` | `4157` | `7ec1b83244b5b6ee6119baaeb0feb1bff12bbfff38e9af68411017bd28560e46` |

The five JSON artifacts strictly parsed. Missing `03` through `05` are truthful:
the targeted gate failed, so focused/full/CodeGraph/diff-check never began. The
single final ER line has schema
`f19-controller-preparation-execution-result-v1`, terminal `FAIL`, and SHA-256
`95abd6219a2ee8e31a79258ea8410f99c3c0e42ec6772e7863503b3817079ff2`.

## Command and budget review

- compileall: exactly one invocation, exit `0`.
- targeted dedicated unittest: exactly one invocation, `11` run, `10` passed,
  `1` assertion failure, `0` errors, exit `1`.
- focused, full, CodeGraph sync and `git diff --check`: `0` invocations after
  the first nonzero gate.
- retry and fallback: `0`.
- source/test edits: exactly the two PLAN-authorized new paths.
- stage and commit: `0/0`.
- controller execution, candidate payload reads, retained-R3 reads, manifest
  writes, canonical-validator calls, eligibility emissions and release calls:
  all `0`.
- network, env, device, camera, Ray, strip, cleanup, formal and public analyzer:
  all `0`.

The command ordering and stop behavior conform to PLAN. The result cannot be
accepted because the targeted gate is nonzero, but no downstream or safety
budget was widened.

## Root-cause decision

The sole failing assertion is in
`test_static_source_and_bytecode_have_no_direct_io_or_forbidden_imports`. Its
AST predicate puts every `ast.Name` and every `ast.Attribute` call into one set,
then globally prohibits the bare string `run`. The production module defines a
lexically local callback helper named `run` inside
`execute_prepared_exact_five_controller` and invokes that local function nine
times. Those calls therefore match the test even though they are not
`subprocess.run`.

Independent AST classification establishes:

- imported roots are only `__future__`, `dataclasses`, `re`, `types`, `typing`
  and the existing machine-contract helper;
- there is no `os`, `pathlib`, `subprocess`, socket, network, device, release or
  Git import;
- all nine `run` call sites are `ast.Name` calls resolving to the nested local
  helper;
- there is no `ast.Attribute` call named `run`, `Popen`, `system`, `read_text`,
  `read_bytes`, `write_text`, `write_bytes`, `unlink` or `mkdir`;
- there is no builtin `open` call.

Therefore this is a dedicated-test false positive, not a controller API,
subprocess, direct-filesystem, Git, release or device boundary violation.
Renaming the production-local helper would encode a faulty test assumption into
production and create avoidable source drift. The smallest correct repair is
test-only and must distinguish name lookup from attribute lookup and bytecode
opcode class.

## Exact next branch

After Orchestrator updates FULL and freezes a new activation lineage, create
exactly one successor:

`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1`

Its repository edit path is exactly:

`tests/test_p7_retained_r3_exact_five_controller.py`

The controller source must remain byte-identical at SHA-256
`746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`.
The failed dedicated-test baseline remains frozen at SHA-256
`579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647`.
The failed evidence root and all five artifacts above are immutable and must not
be reused, repaired, rewritten or deleted.

The test-only correction must:

1. continue rejecting direct builtin `open` calls;
2. continue rejecting filesystem/subprocess method attributes including
   `read_*`, `write_*`, `unlink`, `mkdir`, `system`, `run` and `Popen`;
3. classify AST `Name` and `Attribute` calls separately so a lexically local
   `Name("run")` is not treated as `subprocess.run`;
4. classify bytecode global/name loads separately from attribute/method loads so
   `LOAD_FAST run` is not treated as a subprocess call;
5. explicitly prove the local `run` definition/calls remain nested under the
   controller execution owner, rather than weakening the direct-I/O check to a
   string absence test.

The successor may use one fresh corrective evidence root, one test edit, one
compileall and one each of targeted, focused, full, CodeGraph sync and diff-check
in fail-fast order, all with retry `0`. It must preserve all candidate,
retained-R3, manifest, validator, eligibility, release, network and device locks.
It stops at Planner review and must not commit or enter real controller execution.

## Residual risk and proposed Orchestrator update

- Mark F19 preparation as `REJECTED_DEDICATED_STATIC_TEST_FALSE_POSITIVE`.
- Activate only F19-CORRECTIVE-1 after rebinding FULL/PLAN SHA and Git lineage.
- Preserve `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`.
- Preserve the controller source as uncommitted, byte-frozen output pending the
  corrective test and full validation chain.
- Do not infer candidate, canonical-validator, eligibility, release, B2 or device
  authorization from this review.

**Planner stop:** `F19_FAILURE_REVIEWED_WAITING_ORCHESTRATOR_CORRECTIVE_1_ACTIVATION`.

**Maintenance judgment:** The correction stays within the existing dedicated
static regression owner and avoids production churn; no new controller,
filesystem, validator or execution abstraction is warranted.
