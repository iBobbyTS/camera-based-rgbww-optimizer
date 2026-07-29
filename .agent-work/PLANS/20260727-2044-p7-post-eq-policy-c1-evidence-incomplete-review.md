# REF-P7-24-C1 / Finalize selected C policy with replayable EQ manifest

**计划状态：** `executable_pure_offline_policy_finalization_continuation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-24-C1`

**Parent reference task：** `REF-P7-24`

**PLAN contract ID：** `P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-MANIFEST-C1`

**Package kind：** `bounded_pure_offline_config_code_tests_checkpoint_and_evidence`

**Expected starting HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-MANIFEST-C1","reference_task_id":"REF-P7-24-C1","parent_reference_task_id":"REF-P7-24","package_kind":"bounded_pure_offline_config_code_tests_checkpoint_and_evidence","expected_starting_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"replay_the_exact_planner_eq_family_manifest_v1_then_derive_finalize_validate_and_commit_the_selected_1_2500_policy_once","predecessor_decision":"REJECTED_PREEDIT_MANIFEST_SERIALIZATION_AMBIGUITY","qualification_manifest_schema":"planner_eq_family_manifest_v1","qualification_manifest_included_paths":"all_descendants_root_excluded","qualification_manifest_path_format":"relative_case_preserved_as_posix_no_normalization","qualification_manifest_row_sort":"python_unicode_codepoint_by_path","qualification_manifest_file_row_fields":["path","mode","type","bytes","sha256"],"qualification_manifest_directory_row_fields":["path","mode","type"],"qualification_manifest_type_literals":{"regular_file":"file","directory":"dir"},"qualification_manifest_mode_format":"python_oct_stat_s_imode_including_0o_prefix","qualification_manifest_directory_bytes_sha":"keys_omitted_not_null","qualification_manifest_symlink_policy":"lstat_detect_and_fail_closed_never_follow","qualification_manifest_other_policy":"fail_closed","qualification_manifest_json_sort_keys":true,"qualification_manifest_json_separators":[",",":"],"qualification_manifest_ensure_ascii":false,"qualification_manifest_allow_nan":false,"qualification_manifest_trailing_newline":false,"qualification_manifest_payload_bytes":7980,"qualification_manifest_entries":47,"qualification_manifest_files":42,"qualification_manifest_directories":5,"qualification_manifest_symlinks":0,"qualification_manifest_sha256":"41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9","accepted_eq_status":"qualified_1_2500","selected_state_c_nominal_shutter":"1/2500","selected_state_c_recorded_exposure_min_seconds":0.000387549084953174,"selected_state_c_recorded_exposure_max_seconds":0.000387549084953174,"source_edits":"minimal_existing_owner_only_if_required","config_edits":1,"test_edits":"required","docs_edits":0,"skill_edits":0,"wrapper_edits":0,"release_generation":0,"release_consumption":0,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"public_analyzer_access":0,"formal_r6_access":0,"td_c_access":0,"commit_authorized":true,"commit_cap":1,"amend":0,"push":0,"retry":0,"evidence_root_acquisition_cap":1,"planner_stop_required":true}`

**当前唯一动作：** 使用本PLAN冻结的`planner_eq_family_manifest_v1`逐字重放accepted EQ family；仅在digest
exact `41136…`后，派生并finalize state-C `1/2500` policy，完成最小existing-owner实现/tests、全量离线验证、
一个Git checkpoint和one-shot evidence seal。

**唯一 Planner 停止点：** manifest、qualification、policy、test/static、commit scope或evidence任一failure
立即stop；不得生成release、访问设备、运行public analyzer、formal R6、strip或TD-C。全部通过也必须stop回
Planner。

## 1. Rejected predecessor and preserved acceptance

```text
REF-P7-24 R1 =
  REJECTED_PREEDIT_MANIFEST_SERIALIZATION_AMBIGUITY
derive / edit / test / commit / evidence acquisition = 0
device / network / release / analyzer = 0
```

Review archive：

```text
.agent-work/PLANS/20260727-2026-p7-post-eq-manifest-contract-review.md
SHA-256 =
  e1de5d4f1dcfee552d1ff1c586b152d1c64df1894833cfd1040296fcb03627ba
```

Accepted predecessor remains：

```text
REF-P7-23 = ACCEPTED_QUALIFIED_1_2500
acceptance archive =
  .agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
acceptance archive SHA-256 =
  bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7
```

No Human or Advisor decision is required. This continuation corrects only Planner manifest serialization ambiguity.

## 2. Exact replayable EQ family manifest

```text
EQ_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-exposure-qual-r6-f37517a-20260727T1928
schema =
  planner_eq_family_manifest_v1
```

### 2.1 Included paths and types

Enumerate every descendant of EQ_ROOT with `Path.rglob("*")`; exclude EQ_ROOT itself. Use `lstat()` for every entry.

Allowed：

```text
regular file -> type literal "file"
directory    -> type literal "dir"
```

Any symlink or other filesystem type fails before serialization. Never follow a symlink. Validate EQ_ROOT itself
separately as a mode-`0700` real directory, but do not add a root row.

### 2.2 Path and row order

```python
relative = path.relative_to(EQ_ROOT).as_posix()
paths = sorted(paths, key=lambda path: path.relative_to(EQ_ROOT).as_posix())
```

No `resolve()`, Unicode normalization, case-folding, leading `./`, root prefix or directory trailing slash. Sorting is
Python string/Unicode code-point ordering of the case-preserved relative POSIX path.

### 2.3 Exact row schema

Directory row has exactly three fields：

```json
{"mode":"0o700","path":"prelaunch","type":"dir"}
```

Directory rows omit `bytes` and `sha256`; they are never `null`.

Regular file row has exactly five fields：

```json
{"bytes":1928,"mode":"0o644","path":"run/outer-result.json","sha256":"20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a","type":"file"}
```

Definitions：

```text
mode =
  oct(stat.S_IMODE(lstat_result.st_mode))
bytes =
  lstat_result.st_size integer
sha256 =
  lowercase hashlib.sha256(file_bytes).hexdigest()
```

### 2.4 Exact serializer

```python
payload = json.dumps(
    rows,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
).encode("utf-8")
```

One JSON array; no BOM and no trailing newline. `sort_keys=True` owns serialized object-key order; row-array order is
§2.2.

### 2.5 Frozen result

```text
entries / files / directories / symlinks / other =
  47 / 42 / 5 / 0 / 0
payload bytes =
  7980
first row =
  {"mode":"0o700","path":"prelaunch","type":"dir"}
last row =
  {"bytes":1928,"mode":"0o644","path":"run/outer-result.json",
   "sha256":"20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a",
   "type":"file"}
SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

This schema is deliberately distinct from the historical C3E2 manifest schema. Do not substitute C3E2
type/mode/directory-null semantics.

Compute before edit and after all work with the same owner/algorithm. Require row-for-row and payload-byte equality,
not only matching hash.

## 3. Exact qualification artifacts

```text
EQ_ROOT/run/outer-result.json
  SHA-256 20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
EQ_ROOT/run/candidate-1-outer-terminal.json
  SHA-256 6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
EQ_ROOT/run/candidate-1/candidate-result.json
  SHA-256 7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
EQ_ROOT/run/candidate-1/terminal-seal.json
  SHA-256 8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

Fresh derive only after §2 passes：

```text
owner status = qualified_1_2500
candidate launches / candidate-2 calls = 1 / 0
attempted / physical / accepted = 4 / 4 / 4
selected nominal shutter = 1/2500
recorded owner = Canon:ExposureTime
recorded seconds x4 = 0.000387549084953174
range min/max = 0.000387549084953174 / 0.000387549084953174
ratio = 0.9688727123829349
```

Require exact 58/58 features x4, finite, clipped0, near-noise0, valid-pixel gates, physical receipts/remote IDs,
cleanup/final-zero/seals, retry0 and candidate-2 zero. Never hand-enter selection before deriving these facts.

## 4. Frozen repository and pre-EQ policy

```text
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
pre-EQ policy =
  config/hsi/p7-ray-td-b-exposure-policy-v2.json
pre-EQ policy SHA-256 =
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
```

Orchestrator dispatch exact：

```text
C1_PLAN_SHA256
C1_FULL_SHA256
C1_EXECUTION_RESULT_START_SHA256
```

Verify HEAD, both review archives, pre-EQ policy and §3 artifacts before manifest replay/edit. Any mismatch stops.

Preserve：

```text
A = ray-h120-s100 / 1/5000 / exact_r5_frozen_plan
D = ray-h120-s50  / 1/6400 / exact_r5_frozen_plan
B = ray-h0-s0     / 1/8000 / exact_r5_frozen_plan
r5 frozen shutters =
  b49dd52ebc1eabc8ae6ae0e3713884e5e939428d0682e6d7234eea8c17626e71
observer / quality =
  b81d563eba1910286d879e560538dd497385e422c1bab762008c2b28a26fc4d9
feature IDs =
  4a37bf13a1dcfa6b652bd4ce6a7793aa8ac0344c293d1a7fc73ff7fad763ab86
operating envelope =
  7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
uncertainty =
  cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94
```

No threshold/feature/observer/covariance/coverage/no-ambient/ISO/aperture change.

## 5. Finalized policy contract

Edit existing：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
```

Derive and encode：

```text
r5_failure_class =
  state_specific_exposure_policy_failure_with_required_feature_observer_saturation
exposure_qualification_status = qualified_1_2500
selected_state_c_nominal_shutter = 1/2500
selected_state_c_recorded_exposure_range =
  owner Canon:ExposureTime
  min/max 0.000387549084953174 / 0.000387549084953174
states.C.status = qualified
states.C.formal_shutter = 1/2500
old_new_frame_combination = prohibited
```

Provenance references exact EQ_ROOT, four §3 artifacts, four capture IDs, schema
`planner_eq_family_manifest_v1`, manifest counts/payload bytes/hash and qualification checkpoint `f37517a`.

Keep nominal candidates `["1/2500","1/3200"]`. Do not claim settled state C, TD-B/history/formal pass, release usability
or product readiness.

`selected_policy_hash` is the external SHA-256 of final policy file bytes. Record it in post-EQ validation/checkpoint
evidence and EXECUTION_RESULT; do not self-embed the full-file hash in the same JSON.

## 6. Allowed implementation scope

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json = required
tests/test_p7_td_b_r6_contract.py = required
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py =
  existing policy schema/validation owner, allowed if needed
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py =
  existing EQ owner, allowed only if needed
```

Prefer config+tests if sufficient. No parallel runner/analyzer/release owner, generic framework, docs, skill or wrapper
edit.

## 7. Required tests and offline validation

Tests must cover：

```text
exact planner_eq_family_manifest_v1 positive digest 41136
directory field omission, 0o mode, type literals, sort/path/serializer rules
symlink/other/path escape/hash/content mutation fail closed
Branch A derives 1/2500 and four-value Canon range
4/4/4, candidate-2 zero, retry0 and cleanup/seals enforced
58-feature/physical/remote evidence enforced
A/D/B and frozen hashes cannot drift
selected policy hash equals final policy file SHA
no settled/TD-B/history/release/formal claim
raw readdir is sorted for exact-set checks; manifest order separate
```

Run：

```text
focused failing-first
focused post-fix
entire tests/test_p7_td_b_r6_contract.py
all affected focused suites
full unittest discovery with exact counts
compileall src/tests
all tracked shell wrapper syntax
public-validator positive/negative fixtures only; no public analyzer
CodeGraph sync and blast-radius
git diff --check
secret/path/stale-root/R5-R6 pooling scans
```

All tests use fakes/tempdirs. Device/network/.env/real cleanup adapters must be zero.

## 8. One checkpoint

After all precommit gates pass：

```text
stage only §6 required paths
git diff --cached --check
commit cap = 1
subject =
  feat(p7): finalize eq-r6 state-c exposure policy
amend / second commit / push / tag / PR = 0
```

No `.agent-work`, advisor, GUIDE, evidence or CR3 staging. Postcommit verify parent=`f37517a`, subject/paths, final policy
SHA, focused tests, diff check and EQ after-manifest exact before bytes. Failure stops without amend.

## 9. One-shot evidence

```text
EVIDENCE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017
expected = absent, non-symlink
acquisition / retry / repair / alternate / second generator =
  1 / 0 / 0 / 0 / 0
```

Exact 11：

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

Mode 0700/0600; strict sorted JSON, allow_nan false, one trailing newline; atomic exclusive writes; tmp0. Validation
references 01..09 and terminal references 01..10 by path/bytes/SHA; no self hash; mismatch arrays empty.

`02` and `09` must record exact manifest schema/rows/payload bytes/hash; row and payload equality required.
`selected_policy_hash` equals final policy SHA. All device/release/formal/analyzer counters zero.

## 10. Zero boundary and handoff

```text
device / network / DNS / hostname / .env = 0
camera / Ray / strip / cleanup / capture = 0
EQ/prelaunch/Terminal/liveness = 0
release generation/validation/consumption = 0
public analyzer / formal R6 / strip / TD-C = 0
firmware / deployment / EQ_ROOT writes = 0
```

Append full evidence and exact counts/hashes to EXECUTION_RESULT, then stop. Acceptance can unlock only later
`REF-P7-25`; this PLAN never creates or validates a lineage release.

## 11. 维护性判断

C1只把已接受EQ family的manifest serialization收敛为单一可重放合同，其余policy owner、tests、checkpoint与
stage locks保持不变。无需Advisor或架构重构。

---

## 12. Planner formal review — implementation accepted, evidence incomplete

**Review 时间：** 2026-07-27 20:44 America/Edmonton

Reviewed freeze：

```text
PLAN SHA-256 =
  fcda08d30e849ce5a75d6609e0ab0a2799e0847cc0fae666487c79923dfa9e84
FULL_PLAN_REFERENCE SHA-256 =
  c7c64294df5d64eb4ef94ff3ba6fcea9613f8873c22377126d31feb81f0630d7
EXECUTION_RESULT §155 SHA-256 =
  2681fadbfa1fe749b66d844adeec41504ecf3d553d620a5df95516d3d17cc496
```

Decision：

```text
REF-P7-24-C1 implementation = ACCEPTED
checkpoint 161094f = ACCEPTED
postcommit evidence = INCOMPLETE
REF-P7-24 overall = NOT YET ACCEPTED
next = REF-P7-24-C1E1 pure-offline evidence-only continuation
Advisor / Human decision required = false / false
```

Accepted checkpoint：

```text
commit =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
parent =
  f37517af3ae25efb41f085904fd48f037980ed04
tree =
  6a69b2c7c1569352047500c44e25b337e4ff82aa
subject =
  feat(p7): finalize eq-r6 state-c exposure policy
paths =
  config/hsi/p7-ray-td-b-exposure-policy-v2.json
  src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  tests/test_p7_td_b_r6_contract.py
path-list SHA-256 =
  fdd774e4686b3ebe45296880d6407666dd4ef6cc633e7f9cc891e62bd5480ac2
```

Exact committed files：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  Git blob e7b69daebedf85ed613d29a7b9c5c58e2b082aba
  SHA-256 c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681

src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  Git blob 8e47f74d240158ecc55b94604f373309b55df6ef
  SHA-256 87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90

tests/test_p7_td_b_r6_contract.py
  Git blob 4bc6a791972ad04693015961c0d43c57865305db
  SHA-256 10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23
```

Accepted implementation facts：

```text
planner_eq_family_manifest_v1 before/after = exact
rows/files/dirs/payload/hash = 47/42/5/7980/41136d0d...dca28e9
qualification artifacts and Branch A derive = exact
selected state C = 1/2500
recorded Canon range =
  0.000387549084953174 .. 0.000387549084953174
selected policy SHA-256 =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
formal plan owner status = selected_exposure_policy_non_executable
formal executable = false
```

Accepted recorded validation：

```text
failing-first = 13 run; 3 failures + 3 errors
initial post-fix focused = 13/13
final focused = 15/15
R6 contract = 66/66
affected suites = 139/139
full unittest discovery = 639/639
compileall = pass
tracked zsh syntax = 18/18
public qualification fixtures = 1 positive + 2 negative pass
CodeGraph sync/blast radius = pass
git diff --check = pass
secret/path/stale-root/pooling scans = pass
postcommit focused = 15/15
```

No test, source or config rerun is required for C1E1. The next package must consume these results with explicit
`recorded_evidence_consumed=true` and `rerun_in_c1e1=false`.

Evidence failure：

```text
parser input =
  assert stat_mode := oct(root.stat().st_mode & 0o777) == "0o700"
result =
  SyntaxError before any script statement executed
```

The walrus assignment was not parenthesized in an `assert`. Since Python rejected the entire stdin unit at parse time：

```text
evidence generator body executed = false
EVIDENCE_ROOT acquisition = 0
EVIDENCE_ROOT = absent
files / partial / tmp = 0 / 0 / 0
retry / repair / second generator / alternate root = 0
commit / amend / second commit = 1 / 0 / 0
device / network / release / formal / analyzer = 0
```

This does not invalidate the accepted commit or recorded tests, but the exact 11-file seal required by the PLAN is
missing. `REF-P7-25` remains locked.

Exact next branch：

1. freeze HEAD/tree/parent/three blobs and recorded validation above;
2. permit no source/config/test edit, commit, amend or test rerun;
3. freeze the exact evidence-generator source before execution;
4. syntax-compile/check that source without executing it or acquiring the root;
5. only if syntax check passes, execute that same byte-identical source once;
6. acquire the still-absent frozen root once, generate exact 11, independently audit it, append handoff and stop.
