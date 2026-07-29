# REF-P7-25-C1 / Correct R3 pre-acquisition manifest contract and generate one successor release

**计划状态：** `executable_pure_offline_preacquisition_contract_correction`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-25-C1`

**Parent reference task：** `REF-P7-25`

**PLAN contract ID：** `P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3-C1`

**Package kind：** `bounded_pure_offline_unique_lineage_release_generation_correction`

**Expected HEAD：** `161094ffa2bf1f84ed1fc787e708e8c3463f10db`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3-C1","reference_task_id":"REF-P7-25-C1","parent_reference_task_id":"REF-P7-25","package_kind":"bounded_pure_offline_unique_lineage_release_generation_correction","expected_head":"161094ffa2bf1f84ed1fc787e708e8c3463f10db","expected_parent":"f37517af3ae25efb41f085904fd48f037980ed04","expected_tree":"6a69b2c7c1569352047500c44e25b337e4ff82aa","single_current_action":"persist_one_controller_identity_outside_the_absent_package_verify_exact_old_r2_manifest_then_generate_and_validate_one_r3_release","preacquisition_root_acquisition_cap":1,"package_root_acquisition_cap":1,"controller_source_build_cap":1,"controller_source_sha256_compute_cap":1,"controller_syntax_compile_cap":1,"controller_exec_cap":1,"old_r2_manifest_type_literals":["file","dir"],"old_r2_manifest_mode_json_type":"string","old_r2_manifest_payload_bytes":3577,"old_r2_manifest_payload_sha256":"ccf910b5d4a573f6681b4903e178023da0b9174122a04f9afa87853590303389","release_family":"p7-td-b-lineage-release-r3","production_qualification_cap":1,"release_generation_cap":1,"release_retry":0,"repair":0,"alternate_release_root":0,"second_controller":0,"second_release":0,"release_consumption":0,"repo_edits":0,"tests_rerun":0,"commit_authorized":false,"commit_cap":0,"device_access":0,"network_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"public_analyzer_access":0,"formal_execution_access":0,"td_c_access":0,"planner_stop_required":true}`

**当前唯一动作：** 先在独立的 fresh pre-acquisition evidence root 原子保留唯一 controller
source 与 identity；执行同一 compiled controller 一次，使用本 PLAN 的逐字节 schema 重放 old R2。
只有该 gate 通过才取得唯一 fresh package root、调用 production qualification 一次、生成并验证
唯一 `lineage-release-r3` family。

**唯一 Planner 停止点：** pre-acquisition evidence、controller identity/compile/exec、old-R2 manifest、
package acquisition、qualification、three-artifact release、public/fake/final/strict/terminal 任一失败，
立即保留 evidence 并停止；不得 repair、retry、alternate root/source 或第二 controller/release。
全部通过也停回 Planner，不消费 release，不进入设备、formal、analyzer 或 TD-C。

## 1. Rejection accepted and correction scope

Previous PLAN is rejected as：

```text
REJECTED_PREACQUISITION_OLD_R2_MANIFEST_SERIALIZATION_AMBIGUITY
```

Review archive：

```text
.agent-work/PLANS/
20260727-2103-p7-lineage-release-r3-preacquisition-manifest-review.md
SHA-256 =
  019bdb29d4aecfd5d59f645ee5505ea193fe24535756d4ea7ab2bdd8fc614c0b
```

Reviewed failure evidence：

```text
EXECUTION_RESULT §157 SHA-256 =
  e6efb9e075596480a037025dc774f95939cf9c0a950ed47febf2a3e15a188b7e
old failed controller build/SHA/compile/exec =
  1 / 1 / 1 / 1
old package acquisition =
  0
old qualification / generation / consumption =
  0 / 0 / 0
```

The old controller is consumed and may not be rerun. C1 authorizes one new controller/source and one
new exact root pair only. It changes no production/scientific policy.

## 2. Frozen Git, policy and lineage inputs

```text
HEAD =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
parent =
  f37517af3ae25efb41f085904fd48f037980ed04
tree =
  6a69b2c7c1569352047500c44e25b337e4ff82aa
```

Frozen owners：

```text
src/camera_based_rgbww_optimizer/optimization/
measure_p7_thermal_diagnostics.py
  a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47

src/camera_based_rgbww_optimizer/optimization/
p7_thermal_diagnostics.py
  87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90

tests/test_p7_thermal_diagnostics.py
  3f753743ef679b9db67bc2d54a1476fb38d262d836bbcd3358893e3f4079097f

config/hsi/p7-ray-td-b-exposure-policy-v2.json
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
```

Canonical setup：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
p7-td-b-canon-r2-setup-20260723-042002/setup-release.json
mode / bytes / SHA-256 =
  0644 / 633 /
  401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d
```

Planner lineage candidate：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/
p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json
mode / bytes / SHA-256 =
  0644 / 3039 /
  6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1
```

Accepted post-EQ evidence：

```text
validation =
  3bf2ee27dc53f8b0f919546c2cda7d6917b752d7041241ff3ab95ea7124b06b5
terminal =
  cb3cf3c23f7338f3e4d435029f46965ab8e53320fb747871d2f168c1d9f8934e
EQ manifest =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
selected shutter / policy =
  1/2500 /
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
```

All paths must be regular non-symlink and byte-exact. Production scope relative HEAD and staged
production changes must both be empty. Any mismatch stops before root acquisition.

## 3. Exact old-R2 manifest schema

Old R2 root：

```text
/Volumes/4T/temp/rgbww-optimizer/
p7-td-b-lineage-release-r2-r1/20260726T200000Z
```

### 3.1 Traversal and path owner

Use exactly：

```python
paths = sorted(
    OLD_R2_ROOT.rglob("*"),
    key=lambda path: path.relative_to(OLD_R2_ROOT).as_posix(),
)
```

- Exclude `OLD_R2_ROOT` itself.
- `path` is the exact case-sensitive `relative_to(...).as_posix()` string.
- Sorting is ascending Python `str` order on that path; do not sort serialized rows or filesystem
  native paths by another key.
- Use `lstat()` and never follow symlinks.
- Any symlink or type other than regular file/directory is a hard failure; do not serialize it.

### 3.2 Exact row objects and literals

For a regular file, construct exactly these five keys：

```python
{
    "path": relative_posix_path,             # JSON string
    "type": "file",                          # exact literal
    "mode": oct(stat.S_IMODE(st.st_mode)),   # JSON string, e.g. "0o600"
    "bytes": st.st_size,                     # JSON integer
    "sha256": sha256(file_bytes).hexdigest() # lowercase 64-char JSON string
}
```

Full first-file example：

```json
{"bytes":7252,"mode":"0o600","path":"authorized-release-run-contract.json","sha256":"145b9d43d0a49291d0604ad8a4a4c3d951de83bb42730f8591fee7249e31a9fb","type":"file"}
```

For a directory, construct exactly these three keys：

```python
{
    "path": relative_posix_path,             # JSON string
    "type": "dir",                           # exact literal; not "directory"
    "mode": oct(stat.S_IMODE(st.st_mode)),   # JSON string, e.g. "0o755"
}
```

Full first-directory example：

```json
{"mode":"0o755","path":"child-output","type":"dir"}
```

Field and null contract：

```text
file row:
  keys exactly bytes, mode, path, sha256, type after sort_keys
directory row:
  keys exactly mode, path, type after sort_keys
directory bytes and sha256:
  omitted, never null, never 0, never empty string
all rows:
  no owner/root/mtime/inode/device/uid/gid/link_target/extra/null fields
mode:
  JSON string from Python oct(); lowercase "0o" prefix, no zero padding
```

Last-file example：

```json
{"bytes":8051,"mode":"0o600","path":"wrapper-root/terminal-audit.json","sha256":"1904b3d163911ca90ec56e71dcc53195f83b62307c04062c43f4cf4a5afa2772","type":"file"}
```

### 3.3 Exact payload

The payload is the JSON array of rows itself—no top-level object/schema/count wrapper：

```python
payload = (
    json.dumps(
        rows,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )
    + "\n"
).encode("utf-8")
```

Exactly one final LF is included; no BOM, indentation, spaces or second LF.

Expected live replay：

```text
rows / files / dirs / symlinks / other =
  24 / 21 / 3 / 0 / 0
mode distribution =
  "0o600": 18 / "0o644": 3 / "0o755": 3
payload bytes =
  3577
payload SHA-256 =
  ccf910b5d4a573f6681b4903e178023da0b9174122a04f9afa87853590303389
first path =
  authorized-release-run-contract.json
last path =
  wrapper-root/terminal-audit.json
```

Before/after must rerun this exact owner and require row equality plus payload-byte equality.

## 4. Root identities and controller durability

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer

PREACQUISITION_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3-c1-preacquisition/20260727T2103

PACKAGE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3/
  lineage-release-161094f-c1-20260727T2103

CHILD_OUTPUT_ROOT =
  <PACKAGE_ROOT>/child-output

RELEASE_DIR =
  <CHILD_OUTPUT_ROOT>/lineage-release-r3
```

Preflight requires the four exact owned paths PREACQUISITION_ROOT, PACKAGE_ROOT, CHILD_OUTPUT_ROOT and
RELEASE_DIR absent and non-symlink. SAFE_PARENT must already be an ordinary directory.

The bootstrap owner must：

1. build one controller UTF-8 source value once;
2. compute its bytes/SHA-256 once;
3. acquire PREACQUISITION_ROOT exactly once, mode `0700`;
4. atomically/exclusively persist `controller-source.py` and
   `controller-source-identity.json`, mode `0600`, before compile/exec;
5. identity JSON records source path/bytes/SHA, PLAN/FULL/EXECUTION_RESULT-start hashes,
   expected roots, build/SHA counts=`1/1`, compile/exec planned caps=`1/1`, initial actual
   compile/exec counts=`0/0`, and zero boundaries;
6. syntax-compile the exact persisted bytes once;
7. execute exactly that compiled object once.

The controller must verify its live source file bytes/SHA against identity before old-R2 replay.
Actual compile/exec counts are recorded only in later progressive/terminal evidence; the immutable
pre-execution identity must not claim those actions already completed.
Thus any pre-package failure retains a verifiable source owner without precreating PACKAGE_ROOT.

PREACQUISITION_ROOT is evidence-only and never contains release output or authority. PACKAGE_ROOT remains
absent until the exact §3 old-R2 gate passes. Then the same controller acquires PACKAGE_ROOT once,
mode `0700`, and writes package evidence mode `0600`; owned directories are mode `0700`.

Failure never deletes/recreates either acquired root. Budgets：

```text
controller source build/SHA/compile/exec =
  1 / 1 / 1 / 1
preacquisition root / package root acquisition <=
  1 / 1
repair / retry / alternate source/root / second controller =
  0 / 0 / 0 / 0
```

## 5. Single production qualification

After PACKAGE_ROOT acquisition, persist process-start and invocation-consumed evidence before subprocess
start. Starting the subprocess consumes the sole qualification/release-generation budget regardless of exit.

Exact argv, cwd `/Users/ibobby/Projects/WLED-RGBWW`：

```text
.venv/bin/python
-m
camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics
--experiment-id
p7_td_b_command_switch_history_v1
--source
ray
--phase
formal
--output-dir
<CHILD_OUTPUT_ROOT>
--run-name
lineage-release-r3
--setup-release
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
p7-td-b-canon-r2-setup-20260723-042002/setup-release.json
--lineage-candidate
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/
p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json
--code-checkpoint
161094ffa2bf1f84ed1fc787e708e8c3463f10db
--qualify-lineage-release
```

```text
production qualification start/completion <= 1/1
release generation <= 1
retry / repair / alternate output / second release = 0
release consumption = 0
```

Nonzero/exception/partial output stops success validation. Read-only forensic accounting and truthful
failure sealing are allowed; no second child is allowed.

Qualification must derive the current changed-path ledger and require：

```text
sorted/deduplicated ledger
prohibited_paths = []
unclassified_paths = []
checkpoint/internal path/hash references exact
16 formal / 0 ambient
physical cap 24 / setup physical 2
statistic owner unsubtracted_no_ambient
statistics path normalized_per_second.trimmed_mean
```

## 6. Three-artifact release and validation

On child exit `0`, RELEASE_DIR contains exactly：

```text
current-lineage-candidate.json
resolved-formal-plan.json
setup-lineage-release.json
```

They must be regular non-symlink strict canonical JSON with no temp/nested/fourth artifact. Required：

```text
current candidate checkpoint =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
prohibited_paths =
  []
resolved status =
  execute_authorized
setup release schema/status =
  p7_td_b_setup_lineage_release_v2 / formal_plan_lineage_qualified
production_release_usable =
  true
```

Success order：

1. exact three-artifact/type/canonical audit;
2. exactly one independent public replay using production
   `validate_td_b_setup_lineage_release()`; the writer's internal validation is separately counted;
3. one fake consumer using the same validated release owner and documented `stage == "TD-B"`;
4. exact setup/candidate and old-R2 after replay with §3 byte equality;
5. one final audit;
6. one strict JSON/authority/path/secret audit over both evidence roots before terminal;
7. non-circular terminal summary last.

All mismatch/findings/parse/secret/unexpected-authority arrays must be empty. Final audit verifies
controller source identity, one controller/child, argv/cwd, three artifacts, validator/fake results,
input/R2 immutability and no residual process. Terminal references every prior canonical artifact by
path/bytes/SHA and records all counters.

`production_release_usable=true` remains provenance only. Release consumption is `0`.

## 7. Absolute zero boundary

```text
repo source/config/test/docs/skill/wrapper edits = 0
unit tests / compileall / wrapper tests = 0
commit / amend / stage / push = 0
device / network / DNS / hostname / .env = 0
camera / Ray / strip / all_off / cleanup / capture = 0
CR3 / NPY / nonzero light output = 0
release consumption = 0
public analyzer / predevice / Z0 / E2 / formal R6 / TD-C = 0
firmware / deployment = 0
```

No separate Human authorization is required for this offline release/provenance operation.

## 8. Handoff and acceptance

Append to `.agent-work/EXECUTION_RESULT.md`：

```text
dispatch hashes and frozen preflight
preacquisition/package roots and acquisition counters
controller source path/bytes/SHA and compile/exec counters
exact old-R2 schema replay before/after
qualification argv/cwd/start/return/counters
three release paths/bytes/SHA/schema/status
changed-path and policy results
internal/public/fake/final/strict/terminal results
zero boundaries and residual processes
```

Acceptance request：

```text
REF-P7-25-C1 = ACCEPTED
REF-P7-25 = ACCEPTED_RELEASE_GENERATED_UNCONSUMED
release family = p7-td-b-lineage-release-r3
release consumption = 0
```

Then stop at Planner. Do not modify `FULL_PLAN_REFERENCE.md` or enter a later stage.

## 9. 维护性判断

C1 only freezes one byte-level manifest owner and moves controller identity persistence before execution
without precreating the package. Production qualification, validator and release boundaries remain single;
no repo code or parallel execution framework is added.

---

# Planner review：REF-P7-25-C1 qualification hard failure

**Review date：** 2026-07-27

**Reviewed PLAN SHA-256：**
`0d6087d5ac421ffeeb79776f6eb8c72bd111c3058f6fd682e01bedaec3a0451c`

**Reviewed EXECUTION_RESULT SHA-256：**
`02762d01341af7d2f35a4e060987a619fba1b5321402b9fcada3a100f1b8ccdb`

**Decision：** `REF-P7-25-C1_REJECTED_CHANGED_PATH_POLICY`

## Independent acceptance of the hard-fail

- Corrected old-R2 manifest gate passes exact `24/21/3/0`、3577 bytes、SHA-256
  `ccf910b5d4a573f6681b4903e178023da0b9174122a04f9afa87853590303389`.
- Controller source/identity was retained before execution. Build/SHA/compile/exec are `1/1/1/1`;
  pre-acquisition/package acquisition are `1/1`; retry/repair/alternate/second controller are all `0`.
- The exact production qualification ran once as PID `68203`, completed once and exited `1`.
  `write_td_b_setup_lineage_release()` failed before current-candidate/release writes with
  `PermissionError: TD-B current lineage contains prohibited changes`.
- Independent live read-only replay from setup checkpoint
  `9c804abdeabbc5da18a66d0acf25a1f13128bc2d` to
  `161094ffa2bf1f84ed1fc787e708e8c3463f10db` produces 59 sorted changed paths and exactly two
  `prohibited_or_unreviewed` entries：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
tests/test_p7_td_b_r6_contract.py
```

- Candidate status is `ineligible_requires_new_setup`; release generation/consumption、internal/public
  validation、fake consumer、device/network/formal/analyzer all remain `0`.
- Old R2, setup, Planner candidate and accepted post-EQ inputs remain byte-exact. No retry or residual
  owned process exists. Failure terminal SHA-256 is
  `e63ddfeeb16255551352711f00e1c0d91c1bb167e145cba9ce253fdadc6571ac`.
- §158 contains a report-only typo for the prior review archive hash：
  `019bdb29b674...` is not the live archive hash. The actual immutable archive and active C1 PLAN bind
  `019bdb29d4aecfd5d59f645ee5505ea193fe24535756d4ea7ab2bdd8fc614c0b`.
  Package artifacts do not use the mistyped value, so it does not affect the hard-fail conclusion.

## Classification decision

No Advisor escalation is required. Commit `161094f` was already accepted by REF-P7-24 and contains exact
post-EQ policy finalization. The config blob and R6 contract-test blob are unchanged at current HEAD.
They may be recognized only through a new exact post-EQ lineage mapping gated by：

```text
accepted commit = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
accepted parent = f37517af3ae25efb41f085904fd48f037980ed04
accepted commit paths = exact three from REF-P7-24
config/test accepted blob hashes = exact
new checkpoint ancestry contains accepted commit
new checkpoint copies both accepted blobs byte-exact
```

Do not add prefixes/globs, do not classify arbitrary config/tests, do not remove the default
`prohibited_or_unreviewed` branch, and do not retry release in this package.

## Next branch

Issue exactly one `REF-P7-25-C2` pure-offline implementation package. Modify only the existing lineage
classification owner and its existing focused test file; prove failing-first, exact positive/negative
classification, focused/affected/full/static validation, one commit and one-shot evidence. Preserve both
failed R3 roots and the originally absent R3 root. Stop at Planner; a later PLAN alone may generate release.

维护性判断：production qualification correctly failed closed. The minimal correction adds one
commit-gated exact mapping inside the existing owner and tests it; no generic allowlist or new framework.
