# REF-P7-24 / Finalize selected state-C policy and create post-EQ checkpoint

**计划状态：** `executable_pure_offline_policy_finalization`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-24`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-R1`

**Package kind：** `bounded_pure_offline_config_code_tests_checkpoint_and_evidence`

**Expected starting HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-R1","reference_task_id":"REF-P7-24","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_pure_offline_config_code_tests_checkpoint_and_evidence","expected_starting_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"derive_and_finalize_the_selected_1_2500_state_c_policy_from_the_accepted_eq_family_validate_it_create_one_post_eq_checkpoint_and_stop","accepted_eq_status":"qualified_1_2500","selected_state_c_nominal_shutter":"1/2500","selected_state_c_recorded_exposure_min_seconds":0.000387549084953174,"selected_state_c_recorded_exposure_max_seconds":0.000387549084953174,"qualification_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928","qualification_outer_result_sha256":"20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a","qualification_candidate_result_sha256":"7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612","qualification_terminal_seal_sha256":"8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3","qualification_family_manifest_sha256":"41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9","source_edits":"minimal_existing_owner_only_if_required","config_edits":1,"test_edits":"required","docs_edits":0,"skill_edits":0,"wrapper_edits":0,"release_generation":0,"release_consumption":0,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"public_analyzer_access":0,"formal_r6_access":0,"td_c_access":0,"commit_authorized":true,"commit_cap":1,"amend":0,"push":0,"retry":0,"evidence_root_acquisition_cap":1,"planner_stop_required":true}`

**当前唯一动作：** 从已接受且保持只读的EQ-R6 `qualified_1_2500` family派生state-C selection，finalize
`config/hsi/p7-ray-td-b-exposure-policy-v2.json`，完成所需最小existing-owner code/tests、全量离线验证、一个新
explicit Git checkpoint及one-shot post-EQ evidence seal。

**唯一 Planner 停止点：** 任一frozen input、qualification evidence、policy invariant、test/static check、commit
scope或evidence seal失败立即stop并回Planner；不得生成release、访问设备、运行public analyzer、启动formal R6、
strip或TD-C。全部通过并创建一个checkpoint后也必须stop回Planner。

## 1. Accepted EQ decision and review archive

```text
REF-P7-23 = ACCEPTED_QUALIFIED_1_2500
candidate 1 = 4/4 accepted
candidate 2 call count = 0
attempted / physical / accepted = 4 / 4 / 4
```

Planner acceptance archive：

```text
.agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
SHA-256 =
  bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7
```

Reviewed inputs：

```text
accepted PLAN SHA-256 =
  9916f001e38dbdb224648ec1fe0a4c602a8a9d3bc945e98e1120238f69a3b848
accepted EXECUTION_RESULT SHA-256 =
  1ec2773e2a829d19d89c58b05c5b7488d43201291484664ed005ebb8aabd06d6
accepted FULL SHA-256 =
  e35415fd80decc511f7c9478312c984b04e15503786ab61821734db54ee2c523
```

Transparent residual is closed for EQ acceptance：

```text
REV-EQ-R6-AUX-ORDER-005 =
  NON_BLOCKING_REVIEW_TOOL_DEFECT_CLOSED_BY_INDEPENDENT_AUDIT
```

Do not modify the EQ family to “fix” raw directory enumeration order. Future helpers compare sorted exact sets and
separately validate canonical manifest `artifact_order`.

## 2. Frozen qualification evidence

Exact immutable family：

```text
EQ_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-exposure-qual-r6-f37517a-20260727T1928
```

Exact terminal owner artifacts：

```text
EQ_ROOT/run/outer-result.json
  SHA-256 =
    20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
EQ_ROOT/run/candidate-1-outer-terminal.json
  SHA-256 =
    6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
EQ_ROOT/run/candidate-1/candidate-result.json
  SHA-256 =
    7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
EQ_ROOT/run/candidate-1/terminal-seal.json
  SHA-256 =
    8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

Independent canonical family manifest：

```text
definition =
  sorted relative path, type, POSIX mode, file bytes and SHA-256
entries / files / symlinks =
  47 / 42 / 0
SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

Selected evidence：

```text
qualification status =
  qualified_1_2500
selected nominal shutter =
  1/2500
recorded exposure owner =
  Canon:ExposureTime
recorded exposure seconds x4 =
  0.000387549084953174
recorded exposure range =
  minimum 0.000387549084953174
  maximum 0.000387549084953174
recorded-to-nominal ratio =
  0.9688727123829349
```

Executer must fresh read all four capture records and derive these values. It must not manually enter `1/2500` or the
range without first proving owner status, 4/4 count, identical accepted feature sets, zero clipping/near-noise,
finite/valid-pixel gates, physical returns, remote IDs, cleanup/final-zero/seals, candidate-2 zero and retry zero.

EQ_ROOT is read-only. Compute a fresh before/after whole-family manifest around all edits/tests/evidence generation and
require exact equality to the frozen manifest above.

## 3. Frozen pre-EQ repository inputs

```text
starting HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Pre-EQ exposure policy：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
SHA-256 =
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
```

Frozen unchanged scientific hashes inside policy：

```text
r5_frozen_shutters_sha256 =
  b49dd52ebc1eabc8ae6ae0e3713884e5e939428d0682e6d7234eea8c17626e71
observer / quality policy =
  b81d563eba1910286d879e560538dd497385e422c1bab762008c2b28a26fc4d9
feature IDs =
  4a37bf13a1dcfa6b652bd4ce6a7793aa8ac0344c293d1a7fc73ff7fad763ab86
operating envelope =
  7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
uncertainty =
  cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94
```

A/D/B entries must remain byte-value exact：

```text
A cache/shutter/source = ray-h120-s100 / 1/5000 / exact_r5_frozen_plan
D cache/shutter/source = ray-h120-s50  / 1/6400 / exact_r5_frozen_plan
B cache/shutter/source = ray-h0-s0     / 1/8000 / exact_r5_frozen_plan
```

No threshold, feature, observer, covariance, joint coverage, no-ambient statistic, operating envelope, ISO or aperture
change is authorized.

Orchestrator dispatch must provide exact：

```text
POLICY_PLAN_SHA256
POLICY_FULL_SHA256
POLICY_EXECUTION_RESULT_START_SHA256
```

Any dynamic hash, HEAD, pre-EQ policy hash, review archive or qualification mismatch stops before edit.

## 4. Finalized policy contract

Edit the existing file only：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
```

Preserve its schema and frozen fields. Final state must encode at least：

```text
r5_failure_class =
  state_specific_exposure_policy_failure_with_required_feature_observer_saturation
exposure_qualification_status =
  qualified_1_2500
selected_state_c_nominal_shutter =
  1/2500
selected_state_c_recorded_exposure_range.owner =
  Canon:ExposureTime
selected_state_c_recorded_exposure_range.minimum_seconds =
  0.000387549084953174
selected_state_c_recorded_exposure_range.maximum_seconds =
  0.000387549084953174
old_new_frame_combination =
  prohibited
states.C.status =
  qualified
states.C.formal_shutter =
  1/2500
```

Qualification provenance must reference exact：

```text
EQ_ROOT
outer-result path/SHA-256
candidate-1-outer-terminal path/SHA-256
candidate-result path/SHA-256
terminal-seal path/SHA-256
four capture IDs
family manifest definition/count/SHA-256
qualification checkpoint =
  f37517af3ae25efb41f085904fd48f037980ed04
```

`nominal_candidates` remains `["1/2500","1/3200"]` as qualification history; formal selection is only `1/2500`.

Selected policy hash semantics：

```text
selected_policy_hash =
  SHA-256 of the final serialized
  config/hsi/p7-ray-td-b-exposure-policy-v2.json bytes
owner =
  post-EQ validation/checkpoint evidence
```

Do not put the full-file hash inside the same hashed JSON file. The one-shot validation summary and
`EXECUTION_RESULT.md` must record it as `selected_policy_hash`; later lineage release consumes that exact external
reference. If an existing code owner already defines a non-self-referential policy payload hash, preserve it under a
separately named field and test both semantics.

The final policy must not claim state C settled, TD-B pass, history compatibility, formal R6 pass or release usability.

## 5. Minimal implementation boundary

Allowed edit scope：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json = required
tests/test_p7_td_b_r6_contract.py = required focused coverage
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py =
  allowed only for the existing EQ/policy owner
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py =
  allowed only if the existing schema/validation owner requires it
```

No new parallel runner, analyzer, release owner or generic framework. Prefer one existing-owner helper that:

1. validates immutable qualification evidence and 4/4 Branch A;
2. derives shutter/range/provenance;
3. validates the finalized policy;
4. exposes the final file SHA as external `selected_policy_hash`.

If config plus tests can satisfy existing ownership without production source changes, do not add source code.
Any need to change scientific thresholds, feature IDs or selection rules stops for Planner/Advisor.

## 6. Required tests

Add meaningful focused tests covering at least：

```text
positive accepted Branch A finalizes C to 1/2500
selected shutter is derived from exact outer/candidate evidence
recorded range is derived from all four Canon:ExposureTime values
candidate count/candidate-2 call/4-4-4 accounting are enforced
58/58, finite, clipped0, near-noise0 and valid-pixel gates are enforced
physical CR3/sidecar/remote ID and terminal seal references are enforced
tampered or missing qualification artifact fails closed
wrong root/path/hash, symlink or outside-root evidence fails closed
non-pass cleanup/final-zero fails closed
A/D/B exact entries and frozen hashes cannot drift
old/new combination remains prohibited
formal shutter cannot be hand-entered contrary to selected evidence
selected policy hash equals final file SHA in validation evidence
no state-C settled, TD-B pass or history-compatibility claim is emitted
raw directory exact-set validation sorts enumeration;
manifest artifact_order remains a separate exact check
```

Tests must use temporary fixtures/fakes only. No real `.env`, network, device, camera, Ray, strip, cleanup or EQ call.

## 7. Required offline validation

Run in this order：

```text
focused failing-first for new/changed tests
focused post-fix tests
entire tests/test_p7_td_b_r6_contract.py
all directly affected focused suites
full unittest discovery; record exact tests/failures/errors/skips
compileall for src and tests
all tracked zsh/bash wrapper syntax
public validator positive and negative fixtures only
  (validator code path; never public analyzer and never live release)
CodeGraph sync and blast-radius query
git diff --check
secret scan
absolute path / stale root / R5-R6 pooling scan
```

Public validator fixtures must prove the finalized policy accepts exact qualification provenance and rejects:

```text
pending C
wrong shutter/range/hash
old R5 frame pooling
candidate-2 inconsistency
threshold/feature/A-D-B drift
self-authorizing release/formal claims
```

Record exact commands, exit codes and counts. Failing-first may fail only for the newly required behavior; unexpected
failure stops. Full suite must be entirely green before commit.

## 8. One explicit checkpoint

After all precommit gates pass：

```text
git add only allowed §5 paths
git diff --cached --check
commit cap = 1
subject =
  feat(p7): finalize eq-r6 state-c exposure policy
amend / second commit / tag / push / PR = 0
```

The commit must contain only required config/source/tests. No `.agent-work/**`, advisor, GUIDE, evidence root, CR3 or
other user changes may be staged.

After commit, verify once：

```text
HEAD parent = f37517af3ae25efb41f085904fd48f037980ed04
subject/body and exact changed paths
final policy file SHA-256 = selected_policy_hash
focused postcommit tests
git diff --check
EQ_ROOT fresh after-manifest = exact frozen before-manifest
```

Postcommit failure stops; no amend or second commit.

## 9. One-shot post-EQ evidence

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
EVIDENCE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017
expected start = absent and non-symlink
root acquisition cap = 1
retry / repair / alternate root / second generator = 0
```

One owner writes exact：

```text
01-frozen-inputs.json
02-eq-tree-before.json
03-qualification-audit.json
04-policy-before.json
05-policy-after.json
06-focused-tests.json
07-full-validation.json
08-commit-checkpoint.json
09-eq-tree-after.json
10-validation-summary.json
11-terminal-summary.json
```

Requirements：

```text
root mode 0700; files 0600
regular non-symlink; safe containment
strict sorted JSON; allow_nan=false; one trailing newline
atomic exclusive writes; tmp count 0
exact order/count 11
10 references 01..09 by path/bytes/SHA-256
11 references 01..10 by path/bytes/SHA-256
no self hash
all mismatch arrays = []
selected_policy_hash = final policy file SHA-256
EQ before/after manifests = exact frozen equality
device/network/release/formal/analyzer counters = 0
```

If evidence generation fails, retain the root and stop. Do not repair or create another root.

## 10. Zero-side-effect and stage locks

Entire package：

```text
device / network / DNS / hostname / .env read = 0
camera / Ray / strip / cleanup / final-zero call = 0
capture / CR3 / sidecar / NPY / TIFF creation = 0
EQ / prelaunch / visible Terminal / liveness = 0
public analyzer = 0
lineage release generation / validation / consumption = 0
formal R6 / strip stage / TD-C = 0
firmware / deployment = 0
EQ_ROOT writes = 0
```

Offline tests/fixtures must fail if they attempt any forbidden adapter.

## 11. Handoff and acceptance

Append to `.agent-work/EXECUTION_RESULT.md`：

```text
dispatch hashes and starting HEAD
accepted review archive/hash
EQ before/after manifest and exact qualification audit
policy before/after paths/bytes/SHA-256
derived selected shutter/range and provenance
selected_policy_hash
changed paths and implementation ownership
failing-first, focused, full and static validation exact results
commit hash/parent/subject/paths
evidence root exact 11 and validation/terminal hashes
all mismatch and zero-side-effect counters
decision request
```

Acceptance requires：

```text
REF-P7-24 = ACCEPTED
new explicit checkpoint = valid
selected policy = exact 1/2500 Branch A provenance
EQ_ROOT = immutable
all offline validation = pass
```

Then stop. Do not generate R3 lineage release. Only a later Planner PLAN may unlock `REF-P7-25`.

## 12. 维护性判断

本包把selection derivation、final policy validation和external selected-policy hash保持在现有EQ/policy owner边界，
只允许必要config/source/tests与一个checkpoint。它不新增execution/release/analyzer owner，复杂度由focused及
full validation覆盖；无需Advisor或架构重构。

---

## 13. Planner formal review — rejected before edit

**Review 时间：** 2026-07-27 20:26 America/Edmonton

Reviewed freeze：

```text
PLAN SHA-256 =
  2802210a9ad6804ed6a6868ddcb74a08252b05f2136c71d34f8f03d03befbaaa
FULL_PLAN_REFERENCE dispatch SHA-256 =
  edf07d0c74da0e834538e43c03cd2bb19746ab1731f00de496425bc96ac93407
EXECUTION_RESULT §154 SHA-256 =
  07ded055408c5014a204b88dbe5bb5bcfcecf794b8fc19a39477c5be648c3739
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Decision：

```text
REF-P7-24 R1 =
  REJECTED_PREEDIT_MANIFEST_SERIALIZATION_AMBIGUITY
accepted EQ Branch A = PRESERVE
selected policy finalization = NOT STARTED
device/live/release authority consumed = false
Human / Advisor decision required = false / false
next =
  bounded REF-P7-24 continuation with exact replayable manifest algorithm
```

Pre-edit facts passed：

```text
dynamic hashes / HEAD / review archive = exact
pre-EQ policy hash = exact
four qualification terminal artifact hashes = exact
family entries / files / symlinks = 47 / 42 / 0
CodeGraph owner = existing p7_thermal_diagnostics owner
```

Failure：

```text
PLAN supplied only:
  sorted relative path, type, POSIX mode, file bytes and SHA-256

PLAN omitted:
  exact row keys and type literals
  directory bytes/SHA omission versus null
  exact mode representation
  symlink/other behavior
  serializer flags and trailing newline
```

Executer correctly failed closed. Reusing the prior C3E2 manifest schema produced a different digest and common
variants could not establish which representation owned `41136…`. No accepted hash was presented as a fresh result.

Stop counters：

```text
derive / config / source / test edits = 0 / 0 / 0 / 0
tests / compileall / wrapper / validator = 0
commit / amend / push = 0 / 0 / 0
evidence root acquisition = 0
device / network / DNS / .env = 0
camera / Ray / strip / cleanup / capture = 0
release / public analyzer / formal R6 / TD-C = 0
EQ_ROOT writes = 0
retry / repair / alternate root = 0 / 0 / 0
```

### Planner independent manifest adjudication

Planner independently reproduced the previously frozen hash with an explicit, distinct schema：

```text
schema =
  planner_eq_family_manifest_v1
included =
  every descendant of EQ_ROOT; root itself excluded
entries / files / directories / symlinks / other =
  47 / 42 / 5 / 0 / 0
serialized payload bytes =
  7980
SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

Exact algorithm：

```python
paths = sorted(
    EQ_ROOT.rglob("*"),
    key=lambda path: path.relative_to(EQ_ROOT).as_posix(),
)
rows = []
for path in paths:
    st = path.lstat()
    # fail before serialization if symlink or non-regular/non-directory
    row = {
        "path": path.relative_to(EQ_ROOT).as_posix(),
        "mode": oct(stat.S_IMODE(st.st_mode)),
        "type": "dir" if stat.S_ISDIR(st.st_mode) else "file",
    }
    if row["type"] == "file":
        row["bytes"] = st.st_size
        row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(row)
payload = json.dumps(
    rows,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
).encode("utf-8")
digest = hashlib.sha256(payload).hexdigest()
```

Additional exact semantics：

```text
relative path = case-preserved as_posix; no resolve, NFC, case-fold, "./" or trailing slash
row order = Python Unicode code-point ordering of relative path
mode strings = oct(permission bits), e.g. "0o700" and "0o644"
type literals = "dir" and "file"
directory bytes/SHA keys = omitted, not null
file bytes = lstat st_size integer
symlink policy = lstat-detect and fail closed; never follow
other file type policy = fail closed
JSON document = one array, no BOM, no trailing newline
root mode = validated separately as 0700; root row excluded
```

First and last rows：

```json
{"mode":"0o700","path":"prelaunch","type":"dir"}
{"bytes":1928,"mode":"0o644","path":"run/outer-result.json","sha256":"20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a","type":"file"}
```

This algorithm reproduces `41136…` exactly. It is intentionally not the C3E2 schema, which uses a different type/mode/
directory-null representation. Future REF-P7-24 work must identify the schema by name and must not substitute or infer
another historical manifest format.

Exact next branch：archive this R1 package, then issue one bounded REF-P7-24 continuation preserving all policy,
test, one-commit, zero-device and release locks while replacing the ambiguous manifest prose with
`planner_eq_family_manifest_v1` above.
