# REF-P7-24-C1E1 / Seal accepted post-EQ policy checkpoint evidence

**计划状态：** `executable_pure_offline_evidence_only_continuation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-24-C1E1`

**Parent reference task：** `REF-P7-24`

**PLAN contract ID：** `P7-TD-B-EQ-R6-POST-EQ-POLICY-EVIDENCE-SEAL-C1E1`

**Package kind：** `bounded_pure_offline_postcommit_evidence_only`

**Expected HEAD：** `161094ffa2bf1f84ed1fc787e708e8c3463f10db`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-POST-EQ-POLICY-EVIDENCE-SEAL-C1E1","reference_task_id":"REF-P7-24-C1E1","parent_reference_task_id":"REF-P7-24","package_kind":"bounded_pure_offline_postcommit_evidence_only","expected_head":"161094ffa2bf1f84ed1fc787e708e8c3463f10db","expected_parent":"f37517af3ae25efb41f085904fd48f037980ed04","expected_tree":"6a69b2c7c1569352047500c44e25b337e4ff82aa","single_current_action":"syntax_compile_one_runtime_frozen_generator_then_execute_that_same_compiled_source_once_and_audit_exact_11_evidence","implementation_checkpoint_accepted":true,"recorded_evidence_consumed":true,"tests_rerun":0,"source_edits":0,"config_edits":0,"test_edits":0,"docs_edits":0,"skill_edits":0,"wrapper_edits":0,"commit_authorized":false,"commit_cap":0,"amend":0,"push":0,"generator_source_build_cap":1,"generator_source_sha256_compute_cap":1,"generator_syntax_compile_cap":1,"generator_exec_cap":1,"evidence_root_acquisition_cap":1,"independent_evidence_audit_cap":1,"retry":0,"repair":0,"alternate_root":0,"second_generator":0,"policy_sha256":"c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681","qualification_manifest_schema":"planner_eq_family_manifest_v1","qualification_manifest_sha256":"41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9","release_generation":0,"release_validation":0,"release_consumption":0,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"public_analyzer_access":0,"formal_r6_access":0,"td_c_access":0,"planner_stop_required":true}`

**当前唯一动作：** 保留accepted checkpoint `161094f`及全部recorded validation；构造一次runtime-frozen
evidence-generator source，先仅`compile()`做不执行语法检查，再对同一个compiled code object执行一次，取得仍
absent的唯一root并写exact 11，最后做一次独立只读audit。

**唯一 Planner 停止点：** frozen Git/blob/policy/recorded evidence、generator source identity、syntax compile、
root acquisition、exact-11 generation或independent audit任一failure立即stop；不得修复source、第二次compile/
exec、alternate root、edit、test rerun、commit、release或设备访问。全部通过也停回Planner。

## 1. C1 review decision

```text
REF-P7-24-C1 implementation = ACCEPTED
checkpoint = ACCEPTED
postcommit evidence = INCOMPLETE
REF-P7-24 overall = pending C1E1 seal
```

Review archive：

```text
.agent-work/PLANS/20260727-2044-p7-post-eq-policy-c1-evidence-incomplete-review.md
SHA-256 =
  e827403640b5316817b673ffcb3232b3a8c77c874d0c92a26fae104454f46f0f
```

Reviewed C1 inputs：

```text
C1 PLAN SHA-256 =
  fcda08d30e849ce5a75d6609e0ab0a2799e0847cc0fae666487c79923dfa9e84
C1 EXECUTION_RESULT SHA-256 =
  2681fadbfa1fe749b66d844adeec41504ecf3d553d620a5df95516d3d17cc496
C1 FULL SHA-256 =
  c7c64294df5d64eb4ef94ff3ba6fcea9613f8873c22377126d31feb81f0630d7
```

Prior generator never parsed, so its invocation did not enter root acquisition. C1E1 is a new Planner package, but
permits evidence work only; it does not reopen implementation or validation.

## 2. Frozen checkpoint and files

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

Exact changed paths, ordered：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

Path-list SHA-256, with LF after every line：

```text
fdd774e4686b3ebe45296880d6407666dd4ef6cc633e7f9cc891e62bd5480ac2
```

Exact committed blobs and file hashes：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  blob e7b69daebedf85ed613d29a7b9c5c58e2b082aba
  SHA-256 c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681

src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  blob 8e47f74d240158ecc55b94604f373309b55df6ef
  SHA-256 87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90

tests/test_p7_td_b_r6_contract.py
  blob 4bc6a791972ad04693015961c0d43c57865305db
  SHA-256 10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23
```

All three files must be byte-exact with HEAD and clean relative to HEAD. Staged changes must be zero. Other
Human/Planner `.agent-work/**` state may exist but cannot be modified, staged or committed by Executer.

## 3. Recorded implementation and validation — consume, do not rerun

Record every item below as：

```text
recorded_evidence_consumed = true
source = EXECUTION_RESULT §155 and C1 review archive
rerun_in_c1e1 = false
```

Accepted recorded facts：

```text
planner_eq_family_manifest_v1 before/after =
  47 entries / 42 files / 5 directories / 0 symlinks
  payload 7980 bytes
  SHA-256 41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
  row and payload equality = true

qualification status / selected shutter =
  qualified_1_2500 / 1/2500
attempted / physical / accepted =
  4 / 4 / 4
recorded Canon range =
  0.000387549084953174 .. 0.000387549084953174

failing-first =
  13 run; 3 failures + 3 errors
post-fix initial/final focused =
  13/13 and 15/15
R6 contract =
  66/66
affected suites =
  139/139
full unittest discovery =
  639/639
compileall =
  pass
tracked zsh syntax =
  18/18
public qualification fixtures =
  1 positive + 2 negative pass
CodeGraph / git diff / secret-path-stale-pooling scans =
  pass
postcommit focused =
  15/15
```

C1E1 must not run unit tests, compileall, wrappers, public validator fixtures, CodeGraph, secret/path scans or
`git diff --check` as implementation validation. A final document-only `git diff --check` is Planner-owned after
handoff, not Executer authorization.

## 4. Frozen immutable qualification inputs

```text
EQ_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-exposure-qual-r6-f37517a-20260727T1928
manifest schema =
  planner_eq_family_manifest_v1
manifest rows/payload/hash =
  47 / 7980 /
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

Exact owner artifacts：

```text
run/outer-result.json
  20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
run/candidate-1-outer-terminal.json
  6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
run/candidate-1/candidate-result.json
  7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
run/candidate-1/terminal-seal.json
  8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

Fresh read-only manifest before/after the generator is required using the exact C1 algorithm; it is an immutable-input
audit, not a test rerun. Rows and serialized payload must be byte-identical.

## 5. Dynamic handoff and preflight

Orchestrator dispatch provides exact：

```text
C1E1_PLAN_SHA256
C1E1_FULL_SHA256
C1E1_EXECUTION_RESULT_START_SHA256
```

One local read-only preflight validates dynamic hashes, §1 archive, HEAD/parent/tree/subject, exact three paths/blobs/
file hashes, policy SHA, EQ owner hashes, evidence root absence and zero staged production changes.

Any mismatch stops. No checkout/reset/revert/edit/stage/commit is allowed.

## 6. Runtime-frozen generator source and syntax-only gate

The Executer may build the generator source exactly once as one UTF-8 Python `str`/`bytes` value inside a controller
process. Before any `exec()` or root creation：

1. encode once as UTF-8 and compute `generator_source_sha256`;
2. record byte count and SHA in controller output/handoff memory;
3. call exactly once：

```python
code = compile(
    generator_source,
    "<p7-post-eq-policy-c1e1-generator>",
    "exec",
    flags=0,
    dont_inherit=True,
    optimize=0,
)
```

4. confirm EVIDENCE_ROOT remains absent after compile;
5. execute exactly the returned `code` object once with a fresh namespace.

The source string must not be rebuilt, patched, re-decoded from different bytes or substituted after its SHA is
computed. The SHA recorded in `01-frozen-inputs.json`, `10-validation-summary.json`,
`11-terminal-summary.json` and EXECUTION_RESULT must be identical.

The generator must use ordinary assignment for the root mode check：

```python
stat_mode = oct(stat.S_IMODE(root.stat().st_mode))
assert stat_mode == "0o700"
```

Unparenthesized walrus in `assert` is prohibited. Syntax compile cap=`1`; a SyntaxError or any compile failure stops
while root remains absent. It does not authorize a corrected second source.

This syntax gate compiles only the generator source and does not import/run production code, tests, device adapters or
the generator body.

## 7. Sole generator execution and root

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
EVIDENCE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017
expected before compile and exec =
  absent and non-symlink
```

Only the compiled code object from §6 may acquire it：

```text
source build / syntax compile / exec = 1 / 1 / 1
root acquisition = 1
retry / repair / alternate root / second generator = 0
```

Acquire with exclusive absent-root semantics under SAFE_PARENT and mode `0700`. Never delete, truncate or recreate the
root on failure.

## 8. Exact 11 artifacts

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

Semantics：

```text
01 = dispatch, generator SHA, checkpoint/blobs, zero boundary
02 / 09 = fresh planner_eq_family_manifest_v1 rows/payload metadata
03 = accepted EQ qualification audit
04 = pre-EQ policy from parent f37517a, hash 9e5ec953...60ec2
05 = final policy at HEAD, selected_policy_hash c9080d18...68681
06 = recorded failing-first/focused/R6/affected results; no rerun
07 = recorded full/static/public-fixture results; no rerun
08 = accepted commit/tree/parent/paths/blobs
10 = references 01..09
11 = references 01..10 and terminal counters
```

Every recorded validation item explicitly states `recorded_evidence_consumed=true` and `rerun_in_c1e1=false`.

File contract：

```text
root mode 0700; files mode 0600
regular non-symlink; safe containment
strict sorted JSON
json.dumps(..., sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2)
one trailing LF; no BOM
atomic exclusive write; temp files removed before terminal
exact order/count = 11
```

References：

```text
10 references exact 01..09 path/bytes/SHA-256; no self
11 references exact 01..10 path/bytes/SHA-256; no self
all mismatch arrays = []
selected_policy_hash =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
EQ rows and payload before/after = byte-identical
```

Failure after acquisition retains the root and stops; no repair or second root.

## 9. Independent read-only audit

After generator returns once, run one independent local read-only audit. It may parse/hash/stat only and must verify：

```text
exact 11 names/order and no extra/tmp
root/files mode and no symlink
strict canonical JSON plus one LF
01 generator source byte count/SHA and frozen inputs
02/09 exact manifest schema, rows, payload bytes/hash/equality
03 exact qualification owner facts
04/05 parent/final policy hashes and selected_policy_hash
06/07 recorded provenance and rerun=false
08 commit/parent/tree/paths/blobs
10 and 11 references and no self-reference
all mismatch arrays empty
zero-side-effect counters
```

Audit does not rewrite artifacts. Any mismatch stops; it does not permit generator retry.

## 10. Absolute no-edit/no-rerun boundary

```text
source/config/test/docs/skill/wrapper edits = 0
tests / compileall / wrapper syntax rerun = 0
public validator / CodeGraph / scans rerun = 0
commit / amend / stage / second commit / push = 0
EQ_ROOT writes = 0
device / network / DNS / hostname / .env = 0
camera / Ray / strip / cleanup / capture = 0
release generation / validation / consumption = 0
public analyzer / formal R6 / strip / TD-C = 0
firmware / deployment = 0
```

Only evidence root writes after syntax success are allowed.

## 11. Handoff and acceptance

Append to EXECUTION_RESULT：

```text
dynamic hashes and frozen checkpoint/blob checks
generator source bytes/SHA, compile result, root absent-after-compile proof
single exec/root acquisition counters
exact 11 paths/bytes/SHA
validation and terminal SHA
independent audit results
recorded evidence sources and rerun=false
EQ before/after manifest equality
all zero/no-edit counters
decision request
```

Acceptance request：

```text
REF-P7-24-C1E1 = ACCEPTED
REF-P7-24 = ACCEPTED
checkpoint 161094f = ACCEPTED_COMPLETE
```

Then stop. `REF-P7-25` lineage release remains locked until Planner accepts this seal and writes a separate PLAN.

## 12. 维护性判断

C1E1不修改实现或重跑验证，只将accepted checkpoint封装为syntax-first、single-exec、one-root evidence seal。
Generator source identity与编译/执行分离消除parser failure重演，无新增production/release owner。

---

# Planner 验收：REF-P7-24-C1E1 / REF-P7-24

**验收时间：** 2026-07-27

**Reviewed PLAN SHA-256：**
`38426334baf91adca596822bf99259910cd269f723790e10761bb09164aaba2a`

**Reviewed EXECUTION_RESULT SHA-256：**
`f4ee370bef23eacb71e2d3a6e2aa420a91cb6e5d7d32dcb5f070fed5940df057`

**Decision：**
`REF-P7-24-C1E1_ACCEPTED_REF-P7-24_ACCEPTED_CHECKPOINT_161094F_COMPLETE`

## 独立验收证据

- §156 与 sealed root
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-post-eq-policy-r1-offline-f37517a-20260727T2017`
  一致。root 是 mode `0700` ordinary directory；exact 11 files 均为 mode `0600` regular
  non-symlink，名称、顺序、bytes 与 SHA-256 exact，无 extra/tmp。
- 11 份 JSON 全部严格解析，且逐文件等于
  `json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2) + "\n"`。
  `10-validation-summary.json` exact 引用 `01..09`，SHA-256
  `3bf2ee27dc53f8b0f919546c2cda7d6917b752d7041241ff3ab95ea7124b06b5`；
  `11-terminal-summary.json` exact 引用 `01..10`，SHA-256
  `cb3cf3c23f7338f3e4d435029f46965ab8e53320fb747871d2f168c1d9f8934e`；
  均不 self-reference，mismatches 均为空。
- Generator source exact `20737` bytes，SHA-256
  `e30470cb5bd24551922437a5e3a6f3093e077307c8124fc49396f6ab2a834fa7`。
  source build/SHA/compile/exec/root/audit 均 `1`；retry/repair/alternate root/second generator
  均 `0`。
- EQ before/after manifest 均为 `planner_eq_family_manifest_v1`，47 entries、42 files、
  5 directories、0 symlinks，serialized payload `7980` bytes、SHA-256
  `41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9`；
  rows 与 payload byte equality 均 true。
- Qualification 仍为 `qualified_1_2500`，candidate launches `1`、candidate-2 `0`，
  attempted/physical/accepted `4/4/4`，58 features 全通过，quality mismatch `[]`，
  cleanup/final-zero/terminal seal pass。
- Selected policy SHA-256
  `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`。
  `06/07` 明确 recorded evidence consumed、C1E1 rerun false。
- Live Git 复核为 HEAD
  `161094ffa2bf1f84ed1fc787e708e8c3463f10db`、parent
  `f37517af3ae25efb41f085904fd48f037980ed04`、tree
  `6a69b2c7c1569352047500c44e25b337e4ff82aa`；exact three paths/blobs/file hashes
  与 `01/08` 一致。
- Source/config/test/docs/skill/wrapper edits、test/static rerun、commit/amend/stage/push、
  EQ writes、release、device/network/`.env`、camera/light/capture/formal/analyzer/TD-C
  均为 `0`。

## 决定与下一分支

接受 C1E1 evidence seal、REF-P7-24 与 checkpoint `161094f`。Post-EQ policy 已完整封存，
不再需要 corrective package。

REF-P7-25 现解锁为唯一下一包：纯离线生成并验证新的 `p7-td-b-lineage-release-r3`
family。必须使用 fresh unique root，generation `1/1`、retry `0`；旧 R2 whole-tree
before/after byte-exact；public/final/strict validators、fake consumer、single shared owner
与 three-artifact terminal seal 全通过。该包不得消费 release，也不得进入 device、formal、
public analyzer 或 TD-C；无论成功或失败均停回 Planner。

维护性判断：C1E1 只补齐 immutable evidence seal；接受结果不新增实现复杂度。下一包复用既有
qualification/shared-owner 边界，不建立平行 production owner。
