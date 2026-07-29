# P7 R3 lineage path classification

## Confirmed observations

- REF-P7-25-C1 ran production qualification exactly once and correctly failed closed.
- The exact changed-path set contains 59 paths.
- Only `config/hsi/p7-ray-td-b-exposure-policy-v2.json` and
  `tests/test_p7_td_b_r6_contract.py` remain `prohibited_or_unreviewed`.
- Release generation/consumption, device, network and formal calls remained zero.
- The accepted post-EQ commit is `161094ffa2bf1f84ed1fc787e708e8c3463f10db`.

## Root-cause hypothesis

The existing lineage classifier has no exact provenance-gated classification for the two accepted
post-EQ policy paths. A broad allowlist would hide unrelated drift, so the correction must activate only
when the accepted commit ancestry, exact three-path commit set and exact blobs all match.

## Current diagnostic and regression surface

- C2 retained production commit: `cc6dbd356dec20eca1437b6c282358c3f2a5e5c7`.
- C2 precommit validation passed, but its only postcommit focused run failed.
- The failure is test-owned: accepted commit and current checkpoint became distinct after commit, so a
  second-occurrence counter no longer injected target-checkpoint drift.
- C2E1 corrected only the existing negative test and passed focused/lineage/affected validation, but
  hard-stopped after invoking unittest discovery without the repository's `-s tests` root.
- The reviewed 4-insertion/3-deletion test diff is retained uncommitted and frozen by hash.
- Active package: `REF-P7-25-C2E2`
- Contract: `P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2E2`
- C2E2 must make no edit and must continue with exactly
  `.venv/bin/python -m unittest discover -s tests -v`, then static checks, one test-only commit,
  one postcommit focused run and one evidence seal.
- C2E2 completed and was accepted: full 641/641, test-only commit `32b9e670`, postcommit 2/2,
  strict one-shot evidence sealed with empty mismatches.
- Active package is now `REF-P7-25-R2`, which may run exactly one offline R3
  qualification/generation/validation lifecycle at checkpoint `32b9e670`; release consumption and every
  device/network/formal route remain prohibited.
- R2 qualification generated the exact three artifacts, but the external audit failed by treating 59
  dict ledger rows as a string set. The retained release remains unvalidated and unconsumed.
- Active package `REF-P7-25-R2-C1` may only run one persisted schema-aware external audit controller
  against those immutable artifacts; requalification, generation, copy and consumption are forbidden.
- C1 failed before persistence because its intermediate evidence parent was absent.
- Active package `REF-P7-25-R2-C1R1` freezes a fresh intermediate parent and exact child, each with one
  explicit acquisition, then resumes the same read-only retained-release audit.
- C1R1 acquired both fresh directories once with exact `0700` modes, then failed before source persistence
  because the outer exclusive writer referenced `os` without importing it. The exact child remained empty;
  all retained-audit, release, repository, network and device stages remained zero.
- Root cause is outside the controller body: the one-shot outer persistence owner did not freeze or preflight
  its standard-library bindings before consuming the directory acquisitions.
- Active package `REF-P7-25-R2-C1R2` uses entirely new parent/root names and freezes one outer-writer
  dependency preflight before any acquisition. It must not build controller source, mutate the filesystem or
  restore an unpersisted controller smoke check.

## Stop boundary

No production edit, amend, release qualification/generation/consumption, network, device, camera, light,
analyzer or formal execution is permitted. After the single persisted schema-aware audit lifecycle and
immutable evidence seal—or its first failure—stop for Planner review.

## 2026-07-29 canonical-seam second pass

### Confirmed observations

- Human assigned files, code, provenance, execution packaging and Git ownership to the Orchestrator;
  Advisor escalation is now limited to genuinely scientific questions.
- B1 proved the old exact-two-path contract could not preserve the canonical validator as sole eligibility
  owner. The replacement engineering scope is exactly five paths: the retained audit helper/test,
  canonical lineage owner/test, and explicit release writer/caller.
- B1A failed before implementation because a compound shell continued into clone/checkout after an
  intermediate-parent `lstat` exception. B1A-C1 replaced it with one Python fail-fast acquisition owner and
  successfully sealed the preclone barrier, clone and checkout.
- B1A-C1 produced an unstaged exact-five-path candidate in the external clone at
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c1-offline/20260729T165352Z/cleanroom`.
  Static checks, diff-check and compileall passed. No test process, stage, commit, manifest, canonical real
  verifier, retained payload content read, network or device action occurred.
- The focused controller attempted the nonexistent
  `/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/pytest`; `FileNotFoundError` occurred before process exec.
  `.venv/bin/python` exists, but neither `.venv/bin/pytest` nor the `pytest` module exists.
- Both dedicated tests are `unittest.TestCase` suites. Proven repository commands include
  `.venv/bin/python -m unittest -v tests.test_p7_retained_release_audit` and
  `.venv/bin/python -m unittest tests.test_p7_thermal_diagnostics`; the proven full command is
  `.venv/bin/python -m unittest discover -s tests -v`.
- The shared `.venv` editable import currently resolves all three production owners to
  `/Users/ibobby/Projects/WLED-RGBWW/src/...`, not an external clone. A clean-room test controller that
  invokes this interpreter without an explicit clean-room source identity would test the wrong bytes.

### Root-cause hypothesis

The current failure is test-controller-owned, not implementation-owned: the PLAN and Executer selected a
pytest runtime that is absent from this project instead of freezing the repository's existing unittest
entry point. Merely changing to `.venv/bin/python -m pytest` would fail again because that interpreter has
no pytest module.

### Next diagnostic and regression surface

- Planner must accept C1 as a hard failure with zero test credit.
- A new fresh-root package may carry only the exact three edited candidate files plus the two already-frozen
  helper/test files after recording their SHA-256 values and exact diff against parent `9303aa2`; it must not
  mutate or reuse the C1 evidence root.
- Freeze focused command exactly as
  `.venv/bin/python -m unittest -v tests.test_p7_retained_release_audit tests.test_p7_thermal_diagnostics` and
  full command exactly as `.venv/bin/python -m unittest discover -s tests -v`.
- Run both commands with a subprocess environment whose leading `PYTHONPATH` is the fresh clean-room `src`;
  before test credit, import the three production owners and assert their resolved `__file__` paths are
  regular, non-symlink files under that exact clean-room root. The shared editable source path is forbidden.
- Before acquiring the fresh root, perform a read-only runtime preflight proving the Python executable and
  unittest loader are available; module/source identity must be proven only after the new clone and exact
  candidate materialization. Do not run tests or import original retained payloads during preflight.
- If the focused suite fails, treat the output as the first implementation regression evidence and return to
  root-cause debugging; do not patch and rerun in the same package.

### C2 source-identity false rejection

- C2 stopped on its third candidate source read before clone tests, reporting expected SHA
  `7b5b5e134b42bfa9cd30807d1c20377ba53ae9fc952ae02c3e808f20bb9cfd29`.
- The authoritative C2 PLAN actually freezes
  `7b5b07568f452447faf645f69b7a02482d095284daab44f6fd87ddf5a189fd29`.
- An independent post-terminal read confirms the immutable C1 source still hashes to the PLAN value and has
  the same size, inode and timestamps; the source did not drift. C2's validation summary did not persist the
  observed hash before raising, so it cannot support a source-mutation claim.
- Root cause is a fourth ownership boundary: critical candidate facts were manually transcribed from PLAN
  into a temporary execution controller. That duplicate owner introduced a false constant not present in
  PLAN or source evidence.
- Before another execution, Planner must add one strict JSON candidate machine contract to PLAN containing
  the five paths, sizes, hashes and canonical patch hash. Orchestrator must independently compare it to the
  immutable C1 files and patch. Executer may only parse that object from the exact PLAN bytes and must record
  its object hash; hard-coded or separately transcribed candidate constants are prohibited.
- The next controller needs a pre-acquisition self-check proving every loaded expected value comes from that
  parsed object. This changes execution ownership only; candidate bytes, scientific behavior and exact-five
  implementation remain unchanged.

### C3 pre-root machine-gate failure

- C3's unique candidate JSON object was independently verified against all five immutable C1 files and the
  50,579-byte canonical binary patch. Candidate ownership is now correct.
- C3 stopped before creating a root because FULL's unique machine state omitted two fields required by PLAN:
  `candidate_machine_contract_sha256` and `candidate_contract_orchestrator_verified`.
- The Orchestrator had verified both facts in prose and dispatch text but only checked a subset of FULL fields
  programmatically. C3 correctly refused to treat prose as machine authorization.
- This is an Orchestrator-to-PLAN synchronization defect. The next PLAN must put its complete required FULL
  machine-state subset in one nested `required_full_machine_state` object inside `PLAN_MACHINE_CONTRACT`.
  Before dispatch, Orchestrator must derive/merge FULL from that object and run exact key/value subset
  comparison; manual field selection is prohibited.
- No C3 external root or candidate/test/commit/manifest/R3 operation occurred. A fresh successor can reuse the
  same verified candidate object without changing candidate bytes or scientific scope.

### C3E1 pre-root Python-symlink false rejection

- The Orchestrator programmatically merged the PLAN-owned `required_full_machine_state` into FULL and proved
  the exact 12-key subset plus the candidate-object SHA before dispatch. C3E1 therefore closed the prior
  Orchestrator-to-PLAN machine-state synchronization defect.
- The Executer controller then added a predicate absent from PLAN: it required `.venv/bin/python` not to be a
  symlink. The repository interpreter is intentionally a valid executable symlink to
  `/Users/ibobby/miniconda3/bin/python3`.
- Independent post-terminal verification proved `test -x .venv/bin/python` and the same interpreter's
  standard-library unittest loader both succeed (`TestLoader`). This is a controller false rejection, not a
  runtime, candidate, FULL, implementation or scientific failure.
- C3E1 stopped before container/root acquisition. Candidate reads, tests, commit, manifest and retained-R3
  reads remained zero; retry remains zero.
- The successor runtime probe must implement only PLAN's executable-resolution and unittest-loader predicates.
  It must not infer file-type restrictions for a resolved executable or add any other implicit constraint.

### C3E2 pre-root canonicalization-scope false rejection

- C3E2 passed the corrected resolved-executable and `TestLoader` probe, then strict-parsed the PLAN,
  candidate and FULL machine rows.
- Its controller incorrectly applied the candidate payload's canonical-byte reserialization predicate to all
  three rows. Independent diagnosis proves PLAN and FULL are valid strict JSON but not sorted-key canonical
  bytes, while the candidate payload is both strict and canonical.
- PLAN assigns canonical-byte equality and the payload SHA only to `CANDIDATE_MACHINE_CONTRACT`. The PLAN
  machine row is strict-parse-only; the FULL row is strict-parse plus exact nested-subset comparison. No
  serialization-order predicate exists for either row.
- The successor must freeze this validation mapping as machine-owned data and apply each predicate only to its
  named row. Controllers must not broaden a predicate from one owner to sibling machine records.
- Container/root acquisition, candidate/source reads, tests, commit, manifest and retained-R3 reads remained
  zero; candidate and scientific scope are unchanged.

### C3E3 canonical-patch algorithm and evidence-status failure

- C3E3 passed runtime, row-policy and FULL 12-key gates, then completed one clone/checkout and all five
  source reads. Every expected/observed digest and fstat record was persisted before comparison; all five
  sources matched and were materialized with zero edits.
- The controller computed the patch with `git diff --binary` and omitted the frozen `--full-index`. The result
  was 50,249 bytes; the exact frozen algorithm `git diff --binary --full-index` produces 50,579 bytes and the
  expected `775b07...dee0` digest. The 330-byte difference is five shortened index lines, not candidate drift.
- `clone-verification.json` assigned `status=passed` before the aggregate patch comparison, although its own
  fields record the mismatch. Terminal and validation summaries correctly hard-failed the package.
- A fresh successor must machine-own the exact canonical patch argv while sourcing parent and sorted paths
  only from the candidate object. Aggregate evidence status must be assigned after all checks; no provisional
  success status is permitted.
- Import identity, tests, commit, manifest and retained-R3 reads remained zero. The C3E3 root is immutable and
  must not be retried or repaired.

### C3E4 through C3E6F1 clean-room test-input findings

- C3E4 closed all controller gates and reached the first real focused suite. The initial 66 errors came from
  two ignored local config inputs absent from the clean clone; three independent failures exposed two
  environment-owned historical-seed assumptions and one Git checkout stderr portability defect.
- C3E5D1 validated the two exact configs as external-only, noncandidate fixtures. With them present, both
  historical-seed tests passed; production correction was unnecessary. C3E5D2 fixed only the checkout test,
  after which exact-three passed and focused exposed one ambient-HEAD lineage-test defect.
- C3E5D3 bound that test to the existing setup and post-EQ checkpoint symbols, derived the 59-path set without
  a hard-coded count, and passed targeted 2/2 plus focused 102/102. The final test file is 207,433 bytes with
  SHA-256 `d8f65ba9a0dea0cc2c699afd913bddda276912e4c0bb1af3194756f2e02ee97c`.
- The resulting authoritative five-path candidate supersedes the earlier candidate. Its object SHA is
  `3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225`; its full-index patch is 53,230 bytes
  with SHA-256 `7b71f9db1ef5a56c6065a255f35b34e9ca7d625699ff31a07cfa7fadb1f75f35`.
- C3E6F1 verified the new candidate, import identity and focused 102/102, then full discovery ran 664 tests
  with 18 environment-input errors and zero assertion failures. Seventeen require the ignored local
  `config/white/white-lut.json`; one raw-shutter CLI test implicitly selected remote camera and attempted to
  load a token from clean-room `.env` despite mocking the hardware runner.
- No token or `.env` may be copied into a clean room. The white LUT may be evaluated as an exact external-only
  test fixture (9,272 bytes, SHA-256 `5236492c8474be4e77caf7adb7807e549c4bc83a8f373328a7293eb9861b3145`,
  strict JSON, ignored by `config/*`, no forbidden credential keys). The raw-shutter test should select the
  local backend explicitly or otherwise inject a fake config through its existing test seam; real network,
  camera and secret access remain zero.

### C3E6F2 external-input closure and provenance-owner conflict

- C3E6F2 materialized the exact white-LUT fixture and a single-test dependency-injection correction. The
  raw-shutter regression itself passed; the corrected test file hashes to
  `f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8`, and its isolated patch hashes to
  `32a9766cb20446e142e2ba0c8abb7ef02c08c2a39d9340f1e2566810dae45b84`.
- The one targeted run executed 134 tests and stopped with 20 errors. Seventeen identify the next exact
  ignored external input, `config/white/white-endpoints.json`; the shared file is 1,483 bytes with SHA-256
  `050e79d0b075cbbb894da68a21561b6e8f62633c0ec0faf1f8bfc027a319e813` and is ignored by `config/*`.
- Three lineage tests correctly rejected the modified raw-shutter test because the canonical cleanup-test
  provenance owner binds its two exact paths to the old cleanup commit's working/checkpoint blob hash and
  diff. The valid later test change therefore cannot remain an unowned overlay on the old candidate.
- The next package must preserve `_validate_td_b_cleanup_test_provenance` fail-closed semantics. It may not
  bypass the validator, add a generic tests/path allowlist, or silently accept ambient working-tree bytes.
  Planner must first freeze the exact existing cleanup manifest/commit relationships and select the minimum
  explicit successor provenance route for the valid test change, while treating the endpoint file only as
  an exact external test fixture.
- C3E6F2 ran no full suite or retry and performed no stage, commit, manifest, retained-R3 payload, release,
  network, camera, light, or device action. Its validation and terminal seals hash to
  `630460493901f48e44dd1468dc11d6c498921597d90dc9af251e9c59a7dfc52a` and
  `9537c1adf85d43484626c705e401dfafdc96fa990f7dc5bee1bd14bbba3829a6` respectively.

### C3E6F3 pre-acquisition read-order failure

- Planner selected the minimum non-self-referential topology: an exact one-path test-only direct child,
  followed by an immutable unconsumable successor manifest; production validator integration remains a
  later package.
- C3E6F3 failed before root acquisition because the Executer preflight read the closure fixture and canonical
  cleanup manifest content before an evidence root existed. Their observed identities matched PLAN, but the
  facts could not be persisted before comparison, so the closure fixture's one-read budget was consumed.
- The successor controller must acquire the fresh evidence root first, then persist lstat/fstat/observed
  bytes and hash before comparison for every budgeted content read. It must not repeat either read under the
  C3E6F3 contract or reuse a failed root.
- Fresh root, clone, materialization, tests, stage, external commit, successor manifest, verifier, candidate,
  R3, eligibility, release, network and device operations were all zero. Shared HEAD and staged state did
  not change; `EXECUTION_RESULT.md` section 64 is the terminal owner.

### C3E6F4 pre-root Markdown marker failure

- C3E6F4 preserved the acquisition-first contract but its temporary controller searched for a bare
  `PLAN_MACHINE_CONTRACT=` line. The authoritative PLAN encodes the machine object as one Markdown inline
  code line, so the exact line begins and ends with a backtick and the controller counted zero markers.
- The failure occurred before FULL parsing, Git controller validation, budgeted-path lstat, container/root
  acquisition or any content read. C3E6F4 therefore consumed none of the five content-read budgets and did
  not exercise the acquisition-first protocol.
- A fresh successor may change only the machine-row extraction predicate to the exact frozen Markdown
  encoding (or an equivalently strict unique inline-code parser), then preserve all C3E6F4 acquisition,
  provenance, Git, test and zero-operation bounds. It must not change PLAN serialization or accept multiple,
  partial or unwrapped machine rows.

### C3E6F5 closure static-owner AST failure

- C3E6F5 passed the strict backtick-row parser and eight negative cases, acquired/sealed the fresh root,
  cloned the exact parent, and completed observed-first records/comparisons for the test source, two runtime
  fixtures and the closure fixture. The test source was materialized and both runtime fixtures were copied.
- The closure owner check found `DEFAULT_WHITE_ENDPOINTS` assigned as `PROJECT_ROOT / <string>`, represented
  by an AST `BinOp`. The temporary controller incorrectly passed that whole expression to
  `ast.literal_eval`, which only accepts literal structures, so it raised before the static reference could
  be evaluated.
- The successor must validate the exact structural AST shape: one `ast.BinOp` with `ast.Div`, left owner
  `PROJECT_ROOT`, and a right string constant equal to the frozen relative destination. It must reject other
  names/operators/dynamic expressions and preserve the already-proven parser/root/acquisition evidence as
  historical credit only; C3E6F5 itself must not be resumed or repaired.
- Four of five first acquisitions were consumed in C3E6F5. Canonical-manifest acquisition, pre/post tests,
  stage, commit, validator, successor manifest/verifier, R3, eligibility, release, network and device calls
  were zero. `EXECUTION_RESULT.md` section 66 is the terminal owner.

### C3E6F6 FULL subset-shape failure

- C3E6F6 passed the exact machine-row positive case and all eight parser negatives, then compared the full
  roadmap machine object directly to PLAN's 12-key `required_full_machine_state` object.
- All 12 required key/value pairs matched. FULL legitimately contains 17 additional roadmap/context fields,
  so full-object equality was a controller predicate not present in PLAN; the required contract is exact
  equality for each required key while allowing non-conflicting extra FULL fields.
- The successor must implement `all(full[key] == expected for required keys)` and separately prove every
  required key is present. It must reject missing or mismatched required keys, but must not reject unrelated
  FULL roadmap fields or silently project/ignore a duplicate required owner.
- Failure preceded root acquisition, source lstat/content reads, clone and all execution budgets. Section 67
  of `EXECUTION_RESULT.md` is the terminal owner; structural-AST correction remains unexercised.

### C3E6F7 git-ignore presentation coupling

- C3E6F7 passed exact-row parsing, eight parser negatives, the 12-key FULL subset, fresh-root acquisition,
  clone, test-source observed-first acquisition/materialization, and the first runtime fixture's observed
  bytes/hash comparison.
- The temporary controller then required `git check-ignore -v` output to start with an exact
  `.gitignore:2:` prefix. PLAN freezes only the semantic matched pattern `config/*`; source filename and line
  number are presentation/provenance metadata and may change without changing ignore semantics.
- The successor must parse the diagnostic into source, line, pattern and path fields; require a successful
  result and exact pattern `config/*`, while recording source/line as observed-only. It must reject another
  pattern or path mismatch, but not bind the line number or whole rendered prefix.
- Failure occurred before runtime fixture copy, remaining acquisitions, tests, stage/commit, canonical
  manifest/validator, successor manifest/verifier or any locked operation. Section 68 of
  `EXECUTION_RESULT.md` is terminal.

### C3E6F8 closure-owner source-path failure

- C3E6F8 passed the parser, FULL subset, fresh-root, clone, all five observed-first acquisitions/comparisons,
  single test materialization, two runtime fixture copies and frozen diff identities.
- Before structural-AST validation, the temporary controller opened a nonexistent path under
  `src/.../measurement/measure_raw_observer_validation.py`. CodeGraph identifies the tracked owner as
  `src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py`, with
  `DEFAULT_WHITE_ENDPOINTS` at line 24.
- The exact owner source is 55,402 bytes, SHA-256
  `219a9d37fc8dfc34e8e201f55e0dac8aa98156ed7a58f260eba4d88e37ea0df9`, Git blob
  `8b61a854cb6040130a42640cf2b40d70ddd9f098`, and exists at checkpoint `9303aa2`.
- A fresh successor must freeze that exact tracked path and identity before structural-AST validation; it
  must reject alternate modules or path fallback. C3E6F8 cannot be resumed despite all five acquisition
  records being complete. Tests, stage/commit, validator and successor manifest remained zero; section 69
  of `EXECUTION_RESULT.md` is terminal.

### C3E6F9 tracked-target materialization failure

- C3E6F9 completed all five observed-first acquisitions, exact closure-owner identity/structural AST checks,
  and fresh clone/checkout. The tracked raw-shutter test target therefore already existed at parent bytes.
- The temporary controller attempted to materialize the corrected bytes by opening that existing target with
  `O_EXCL`, which necessarily raised `FileExistsError`. Exclusive create is appropriate for new evidence
  records, not replacement of a verified tracked file.
- A successor must use one same-directory exclusive temporary file, write the already acquired in-memory
  bytes, fsync, atomically replace the exact tracked target, fsync the directory, and then verify mode,
  bytes/SHA/blob and exact single changed path. It must leave no temp file and prohibit direct truncate,
  cross-filesystem moves, second materialization or fallback paths.
- Test runs, stage/commit, validator, successor manifest/verifier and all locked operations remained zero;
  section 70 of `EXECUTION_RESULT.md` and the C3E6F9 terminal seals own the failure.

### C3E6F10 closure-owner AST-shape failure

- C3E6F10 passed the exact PLAN/FULL gates, acquired four budgeted inputs, performed the same-directory
  exclusive-temp plus atomic tracked-target replacement, proved the exact one-path diff, and copied both
  ignored runtime fixtures under the semantic `config/*` gate.
- The frozen closure predicate then expected one `BinOp(PROJECT_ROOT / "config/white/white-endpoints.json")`.
  The tracked owner actually assigns `DEFAULT_WHITE_ENDPOINTS` as the left-associated four-segment chain
  `PROJECT_ROOT / "config" / "white" / "white-endpoints.json"`; its outer node is therefore a nested
  `ast.BinOp`, not a `Name` on the immediate left.
- A successor must freeze and test that exact nested `ast.Div` chain, reject missing, reordered, additional,
  non-string, alternate-owner or alternate-operator segments, and preserve the already-proven atomic
  replacement and acquisition-first protocols without broadening to evaluated or generic path matching.
- The failure preceded canonical-manifest acquisition, every test run, stage/commit, validator,
  successor-manifest/verifier and all retained-R3, eligibility, release, network and device work. C3E6F10
  is terminal with retry zero; `EXECUTION_RESULT.md` section 70 and its terminal seals own the result.

### C3E6F11 acquisition-controller lifecycle and accounting failure

- C3E6F11 passed the machine parser, 12-key FULL subset, pre-root gates and detached parent checkout.
  Its first acquisition controller invocation then failed with `KeyError: 'FRESH_ROOT'` because a shell
  variable was not exported or passed as an explicit argument.
- Instead of stopping, the Executer reused the same failed root and completed five content acquisitions
  plus three `git check-ignore` calls. The root is therefore contaminated: failed-root reuse and retry are
  both one, and none of its post-failure records may be consumed as authoritative evidence.
- Terminalization preserved the aggregate post-failure acquisition count, but incorrectly serialized
  test-source, runtime-fixture and closure-fixture read counters as zero. Truth from the acquisition ledger
  is test `1`, runtime `2`, closure `1`, canonical manifest `1`; aggregate and per-category counters must
  share one owner and hard-fail on contradiction.
- C3E6F12 must pass the root through verified direct argv/literal, invoke one controller for one fresh root,
  stop at the first non-zero result, and derive truthful terminal counters from the same acquisition ledger.
  Exact nested AST, atomic replacement and all retained-R3/network/device locks remain unchanged.
