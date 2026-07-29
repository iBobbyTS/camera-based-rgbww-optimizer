# REF-P7-25 / Generate and validate successor TD-B lineage release R3

**计划状态：** `executable_pure_offline_release_generation_and_validation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-25`

**PLAN contract ID：** `P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3`

**Package kind：** `bounded_pure_offline_unique_lineage_release_generation`

**Expected HEAD：** `161094ffa2bf1f84ed1fc787e708e8c3463f10db`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3","reference_task_id":"REF-P7-25","package_kind":"bounded_pure_offline_unique_lineage_release_generation","expected_head":"161094ffa2bf1f84ed1fc787e708e8c3463f10db","expected_parent":"f37517af3ae25efb41f085904fd48f037980ed04","expected_tree":"6a69b2c7c1569352047500c44e25b337e4ff82aa","single_current_action":"generate_and_validate_one_unique_p7_td_b_lineage_release_r3_family","release_family":"p7-td-b-lineage-release-r3","release_generation_cap":1,"production_qualification_cap":1,"release_retry":0,"second_release":0,"alternate_release_root":0,"release_consumption":0,"source_edits":0,"config_edits":0,"test_edits":0,"docs_edits":0,"skill_edits":0,"wrapper_edits":0,"commit_authorized":false,"commit_cap":0,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"public_analyzer_access":0,"formal_execution_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"planner_stop_required":true}`

**当前唯一动作：** 在唯一 fresh R3 package 内，以一个 external controller 调用 production
lineage qualification CLI 恰好一次，生成唯一 `lineage-release-r3` 三 artifact family；随后执行
一次 public validation、一次 fake consumer、一次 final audit、一次 strict JSON audit，并封存
terminal evidence。

**唯一 Planner 停止点：** preflight、package acquisition、production qualification、三 artifact、
public validator、fake consumer、old-R2 immutability、final/strict audit 或 terminal seal 任一失败立即
fail closed；保留现有 evidence，禁止 repair、retry、alternate root 或第二 release。全部通过也停回
Planner，不消费 release，不进入 predevice/device/formal/analyzer/TD-C。

## 1. Planner acceptance and unlock

REF-P7-24-C1E1、REF-P7-24 与 checkpoint `161094f` 已接受完成。

Review archive：

```text
.agent-work/PLANS/20260727-2052-p7-post-eq-policy-c1e1-acceptance-review.md
SHA-256 =
  6dd605a8d5f142d8fb50cc9a40020e6a816cc116581cccb414459f6c91cc1762
```

Accepted evidence：

```text
post-EQ validation summary =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017/
  10-validation-summary.json
SHA-256 =
  3bf2ee27dc53f8b0f919546c2cda7d6917b752d7041241ff3ab95ea7124b06b5

post-EQ terminal summary =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017/
  11-terminal-summary.json
SHA-256 =
  cb3cf3c23f7338f3e4d435029f46965ab8e53320fb747871d2f168c1d9f8934e

EQ family manifest =
  planner_eq_family_manifest_v1
  47 entries / payload 7980 bytes
SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9

selected shutter / policy =
  1/2500 /
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
```

This PLAN authorizes only offline release generation and validation. A successful release remains
unconsumed and is not device/formal authorization.

## 2. Frozen checkpoint and production owners

```text
HEAD =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
parent =
  f37517af3ae25efb41f085904fd48f037980ed04
tree =
  6a69b2c7c1569352047500c44e25b337e4ff82aa
subject =
  feat(p7): finalize eq-r6 state-c exposure policy
```

Frozen production owner hashes：

```text
src/camera_based_rgbww_optimizer/optimization/
measure_p7_thermal_diagnostics.py
  a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47

src/camera_based_rgbww_optimizer/optimization/
p7_thermal_diagnostics.py
  87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90

tests/test_p7_thermal_diagnostics.py
  3f753743ef679b9db67bc2d54a1476fb38d262d836bbcd3358893e3f4079097f
```

Each owner hash above must be checked against the actual file. Any mismatch stops before package
acquisition; do not continue on a near match.

Selected policy：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
SHA-256 =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
```

Exact Git checkpoint, all owner hashes, no staged production changes, and no source/config/test/docs/
skill/wrapper diff relative to HEAD are hard preconditions. Any mismatch stops.

## 3. Frozen lineage inputs

Canonical setup：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
p7-td-b-canon-r2-setup-20260723-042002/setup-release.json
mode / bytes =
  0644 / 633
SHA-256 =
  401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d
```

Accepted Planner lineage candidate：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/
p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json
mode / bytes =
  0644 / 3039
SHA-256 =
  6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1
```

Both inputs must remain regular, non-symlink, byte-exact before and after the package.

The production qualification must derive the current changed-path ledger from the canonical setup
checkpoint to exact HEAD `161094f`. It must use the current production policy owner; do not copy an
old R2 changed-path count or mutate candidate/release JSON. Requirements：

```text
ledger sorted and deduplicated
all entries classified by the current policy
prohibited_paths = []
unclassified_paths = []
checkpoint / internal references = exact
formal count = 16
ambient count = 0
physical cap = 24
setup physical count = 2
statistic owner = unsubtracted_no_ambient
statistics path = normalized_per_second.trimmed_mean
```

Any qualification mismatch is a terminal hard failure. No local policy fallback is authorized.

## 4. Immutable predecessor R2

Historical R2 root：

```text
/Volumes/4T/temp/rgbww-optimizer/
p7-td-b-lineage-release-r2-r1/20260726T200000Z
```

Before package acquisition, build a read-only manifest by recursively sorting relative POSIX paths.
For regular files include type/mode/bytes/SHA-256; for directories include type/mode; reject symlink
or other types. Serialize rows as：

```python
(json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
```

Frozen expected result：

```text
entries / files / directories / symlinks =
  24 / 21 / 3 / 0
payload bytes =
  3595
payload SHA-256 =
  f7e1ad901c1a107a9d5e92d798c9f82ae759b0b665822dccd0654012b534b172
```

Repeat after terminal generation and require row equality plus payload-byte equality. R2 is read-only;
do not validate by rewriting or touching it.

## 5. Unique package and release family

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer

PACKAGE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3/lineage-release-161094f-20260727T2052

CHILD_OUTPUT_ROOT =
  <PACKAGE_ROOT>/child-output

RELEASE_DIR =
  <CHILD_OUTPUT_ROOT>/lineage-release-r3
```

Preflight requires PACKAGE_ROOT, CHILD_OUTPUT_ROOT and RELEASE_DIR all absent and non-symlink.
Acquire PACKAGE_ROOT exactly once with exclusive semantics and mode `0700`. Package files are regular
non-symlink mode `0600`; owned directories mode `0700`. Never delete, truncate, rename, recreate or
switch to another root after acquisition.

One external controller under PACKAGE_ROOT owns lifecycle state, the single production subprocess,
progressive evidence, validation ordering and terminal seal. Helpers may parse or validate, but no
second controller/parallel owner may call production qualification or create a release family.

Controller source may be created once before invocation, but must be SHA-recorded, syntax-compiled once,
and executed once. Syntax failure stops before production qualification; source repair or second
controller is prohibited.

## 6. Exact production qualification invocation

Immediately before the child start, persist a process-start/consumption marker. Reaching subprocess
start consumes the sole budget regardless of exit.

Exact argv：

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

Run from `/Users/ibobby/Projects/WLED-RGBWW`, with inherited environment unopened and no network/device
probe. Capture stdout/stderr to package logs without parsing them as authority.

Budgets：

```text
production qualification start/completion <= 1/1
release generation <= 1
retry / repair / alternate root / second release = 0
release consumption = 0
```

Nonzero exit, exception, missing result, partial output or unexpected stdout stops further qualification
and release creation. The controller may still perform read-only forensic accounting and write a truthful
failure terminal summary, but must not run success validators.

## 7. Three-artifact release contract

On child exit `0`, RELEASE_DIR must contain exactly：

```text
current-lineage-candidate.json
resolved-formal-plan.json
setup-lineage-release.json
```

All three must be regular, non-symlink, strict canonical JSON and internally hash/path/checkpoint bound.
No fourth file, temp file, nested directory or alternate family is allowed.

Required status facts：

```text
current candidate =
  current checkpoint 161094f
  prohibited_paths []

resolved formal plan =
  execute_authorized
  16 formal / 0 ambient
  physical cap 24 / setup physical 2
  selected policy SHA c9080d18...68681

setup lineage release =
  schema p7_td_b_setup_lineage_release_v2
  status formal_plan_lineage_qualified
  production_release_usable true
  checkpoint 161094f
```

`production_release_usable=true` is an internal provenance result only. This PLAN keeps release
consumption and all live execution at zero.

## 8. Validators, fake consumer and terminal ordering

Success validation order is fixed：

1. inspect exact three-artifact cardinality/type/mode/canonical JSON;
2. make exactly one independent public-replay call to
   `validate_td_b_setup_lineage_release()` against the generated release and frozen expected
   setup/Planner candidate/current checkpoint;
3. run one fake consumer through the same validated release owner; it must consume the returned resolved
   plan and assert only documented fields, including `stage == "TD-B"`—never `stage == "formal"`;
4. verify setup/candidate and old R2 before/after immutability;
5. run one final audit;
6. run one strict JSON/authority/path/secret audit;
7. write non-circular terminal summary last.

The production writer's mandatory internal validation belongs to the one qualification call and is not
the independent public replay. Thus expected validation accounting is one internal production validation
plus one controller-owned public replay; the controller must not make a second public-replay call. The
public replay and fake consumer must share one release path/reference owner. No copied validator, second
generated release, direct field patch, automatic fallback or acceptance-by-summary is allowed.

Final audit must independently verify：

```text
dynamic PLAN/FULL/EXECUTION_RESULT-start hashes
HEAD/parent/tree and frozen owner hashes
single controller and single child invocation
exact argv/cwd and consumed budget
three release artifacts and internal references
public validator + fake consumer pass
old R2 and frozen inputs unchanged
no residual owned process
all mismatch/findings arrays empty
```

Strict audit must parse every pre-terminal package JSON regular file, reject NaN/Infinity/literal repair artifacts,
classify every `production_release_usable=true` and authorization-like hit by exact path, scan for secret
material and repository-relative/path-policy violations, and report：

```text
parse_errors = []
unexpected_authority_hits = []
secret_hits = []
path_policy_findings = []
```

The terminal summary references every prior canonical package artifact by path/bytes/SHA-256 and never
self-references. It records release generation `1`, consumption `0`, retry `0`, validator counts,
old-R2 equality and every zero-side-effect counter.

## 9. Absolute boundaries

```text
repo source/config/test/docs/skill/wrapper edits = 0
unit tests / compileall / tracked wrapper tests = 0
commit / amend / stage / push = 0
second package / release / qualification invocation = 0
release consumption = 0
device / network / DNS / hostname / .env = 0
camera / Ray / strip / all_off / cleanup / capture = 0
CR3 / NPY / nonzero light output = 0
public analyzer / predevice / Z0 / E2 / formal R6 / TD-C = 0
firmware / deployment / destructive hardware operation = 0
```

This offline release operation does not require separate Human authorization under AGENTS.md. That does
not broaden any device or formal scope.

## 10. Handoff and acceptance request

Append to `.agent-work/EXECUTION_RESULT.md`：

```text
dynamic dispatch hashes
frozen checkpoint/owner/input checks
old R2 before/after manifest and equality
package/controller source identity and single-root proof
exact argv/cwd/start/return and invocation counters
three release artifact paths/bytes/SHA/schema/status
changed-path counts and prohibited/unclassified arrays
public/fake/final/strict results
terminal summary path/bytes/SHA
zero boundaries and residual process result
```

Acceptance request：

```text
REF-P7-25 = ACCEPTED_RELEASE_GENERATED_UNCONSUMED
release family = p7-td-b-lineage-release-r3
release consumption = 0
```

Then stop at Planner. Do not write a predevice/device/formal command and do not update
`FULL_PLAN_REFERENCE.md`.

## 11. 维护性判断

本包不改 repo 实现；它复用 production qualification 与 public validator，只由一个 external
controller拥有 invocation、progressive evidence和terminal seal。Release generation 与 consumption/
device/formal authority继续分离；无需新增 production 抽象。

---

# Planner review：REF-P7-25 pre-acquisition failure

**Review date：** 2026-07-27

**Reviewed PLAN SHA-256：**
`41b0d7628c35c41f124a8e23814e7c0aaf2c51d609e1da78eb97c450de1b6899`

**Reviewed EXECUTION_RESULT SHA-256：**
`e6efb9e075596480a037025dc774f95939cf9c0a950ed47febf2a3e15a188b7e`

**Decision：**
`REJECTED_PREACQUISITION_OLD_R2_MANIFEST_SERIALIZATION_AMBIGUITY`

## Independent findings

- §157 matches the frozen PLAN and stop boundary. The only controller source was built, SHA-computed,
  syntax-compiled and executed once; the assertion failed at old-R2 manifest verification before package
  acquisition.
- `PACKAGE_ROOT`、`CHILD_OUTPUT_ROOT` and `RELEASE_DIR` remain absent. Qualification start/completion、
  release generation/consumption、internal/public validation、fake consumer、final/strict audit and
  terminal seal all remain `0`.
- Retry/repair/alternate source/second controller/alternate root/second release are all `0`; repo edits、
  tests、Git mutation、network/device/camera/light/capture/formal/analyzer are all `0`.
- Old R2 live replay confirms 24 rows：21 regular files、3 directories、0 symlinks/other. The failed
  controller selected directory type literal `"dir"` and mode strings from
  `oct(stat.S_IMODE(...))`, producing `3577` UTF-8 bytes and SHA-256
  `ccf910b5d4a573f6681b4903e178023da0b9174122a04f9afa87853590303389`.
- The reviewed PLAN required `type/mode` fields but did not freeze the directory type literal. A
  semantically plausible `"directory"` literal instead produces `3595` bytes and
  `f7e1ad901c1a107a9d5e92d798c9f82ae759b0b665822dccd0654012b534b172`.
  The 18-byte difference is exactly six extra ASCII bytes across three directory rows.
- Mode itself was also underspecified at the JSON value/type boundary even though the implementation
  used `oct()`. The correction must freeze mode as JSON string literals such as `"0o600"`/`"0o755"`,
  not integers or `"0600"`.
- Because the controller source identity was planned to be persisted only after package acquisition,
  its pre-acquisition failure left no owner artifact. The correction must not run or even build the
  controller before acquisition. A separate deterministic read-only preflight verifies old R2 first;
  only after it passes may the package be acquired and the controller source/identity be persisted before
  compile/exec.

## Decision and next branch

Reject this invocation as a Planner contract defect. Release-generation budget remains unconsumed because
the production qualification subprocess never started, but the consumed controller may not be retried
under this PLAN.

Issue exactly one `REF-P7-25-C1` pure-offline correction. It freezes the complete manifest row schema,
literal types, omissions, sort/path/newline/serializer and expected `3577`/
`ccf910b5...3389`; performs a pre-acquisition verifier before controller construction; then preserves all
single qualification, single release, immutable R2, validation, zero-device and Planner-stop boundaries.

维护性判断：失败来自 Planner evidence schema，不是 production/release owner。Correction only
clarifies serialization and lifecycle ordering; no repo implementation or architecture change is needed.
