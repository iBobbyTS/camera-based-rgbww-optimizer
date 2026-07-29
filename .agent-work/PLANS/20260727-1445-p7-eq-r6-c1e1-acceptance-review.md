# REF-P7-23-C1E1 / C1 immutable evidence seal correction

**计划状态：** `executable_pure_offline_evidence_only`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C1E1`

**Parent reference task：** `REF-P7-23-C1`

**PLAN contract ID：** `P7-TD-B-EQ-R6-C1-EVIDENCE-SEAL-CORRECTION`

**Package kind：** `bounded_offline_evidence_only`

**Expected HEAD：** `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-C1-EVIDENCE-SEAL-CORRECTION","reference_task_id":"REF-P7-23-C1E1","parent_reference_task_id":"REF-P7-23-C1","package_kind":"bounded_offline_evidence_only","expected_head":"93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8","single_current_action":"replay_and_seal_c1_candidate_evidence_in_one_new_root","human_eq_r6_confirmation_preserved":true,"source_edits_authorized":false,"test_edits_authorized":false,"commit_authorized":false,"device_access":"forbidden","network_access":"forbidden","env_access":"forbidden","backend_access":"forbidden","camera_access":"forbidden","ray_access":"forbidden","strip_access":"forbidden","light_access":"forbidden","real_all_off_access":"forbidden","real_capture_cap":0,"real_eq_root_creation_authorized":false,"release_generation_authorized":false,"release_consumption_authorized":false,"eq_r6_launch_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 只读冻结 C1 implementation candidate及历史roots，先在内存中验证canonical artifact
order与summary/seal计数合同，fresh重跑必要的injected tests；全部通过后仅创建一个新的unique evidence root，
一次性写入truthful matrices、validation summary与terminal seal。

**唯一 Planner 停止点：** 新root terminal seal完成，或任一preflight/test/order/write/hash/immutability检查
失败时立即停止，在 `.agent-work/EXECUTION_RESULT.md` 追加handoff交Planner。不得修改代码/测试、提交、
修补旧root、访问设备、启动EQ、生成release或进入后续stage。

## 1. C1 review decision

Reviewed C1：

- PLAN SHA-256：
  `e8d809fae33ad2f0dc9bc0490f27c317d230c843770b3a67b5ebcca99fec36a4`
- EXECUTION_RESULT §137 SHA-256：
  `0b76df7de274245408176027cd75b06b6c51621b646de8519959061e3e8f99a9`
- Orchestrator stable active-C1E1 FULL SHA-256：
  `20911abe2e6cea9243317303d78f1a50a6d9a28a0d60baca37247f79bbb51261`
- 本次 FULL hash 更新仅记录 orchestration transition；不扩展设备、EQ、capture、release、source edit、
  commit、权限、budget、root或后续stage边界。
- review archive：
  `.agent-work/PLANS/20260727-1424-p7-eq-r6-c1-evidence-failure-review.md`
- archive SHA-256：
  `0a8c208eb32e94ce4777d9a8cf8a81f0110356532bf30e879f31023fd6d1bcc5`

Decision：

```text
REF-P7-23-C1 = REJECTED_TERMINAL_EVIDENCE_ABSENT
implementation commit 93e72b8 = retained immutable candidate
REV-EQ-R6-C0-001/002 = candidate-fixed, closure pending C1E1 seal
```

C1代码测试通过但固定root为空，validation/terminal不存在；implementation pass不得冒充evidence seal pass。
C1E1是ordinary evidence-owner correction，不需要Advisor。

Human exact EQ-R6确认继续有效，但本PLAN不授权任何真实执行。

## 2. Frozen code and evidence inputs

| Input | Frozen value |
|---|---|
| HEAD / C1 candidate commit | `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8` |
| commit parent | `57985fa74301e26d097c96e69e52661714fea7b3` |
| commit message | `fix(p7): bind eq-r6 runtime and final zero` |
| measurement runner SHA-256 | `7738b73b37f389fde998eb4911efd74d1a40370181866af93736c0544894b938` |
| thermal contract SHA-256 | `34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3` |
| focused test SHA-256 | `01a185e6d68bf0acef9db4f19362a6b316b8d4f063dc80a3844fcff6500e9877` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |
| applicable GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| project skill SHA-256 | `c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607` |
| C0 validation SHA-256 | `aca05551c26f512799cb2de0eea2342d30ace04360a71ac29b29fe0e56d541a2` |
| C0 terminal SHA-256 | `a33aa0ec87a37ae98cde1d5762acd65e0513a57fd04babea84735728ae5f9a6b` |

Exact C1 commit path set：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

任何commit metadata、path、blob/source hash不符均立即停止；不得“修复”代码。

## 3. Historical roots immutable contract

### 3.1 Failed empty C1 root

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1-offline/eq-r6-c1-57985fa-20260727T1401
```

Frozen initial facts：

```text
exists = true
regular directory = true
symlink = false
mode = 0700
top-level entries = 0
regular files = 0
JSON files = 0
validation-summary = absent
terminal-summary = absent
empty-root canonical manifest SHA-256 =
  52378315a05a2b72d990aeace832287ce3a5dfe28c2ab1b37abe72ac43f2abf9
```

该digest的canonical owner固定为：schema `empty_root_manifest_v1`；absolute/resolved path、device、inode、
mode、directory/symlink flags、`entries=[]`、top-level/file/JSON三个zero counts；sorted-key compact
JSON、`allow_nan=False`、不含末尾newline后计算SHA-256。before/after必须以同一owner重算并exact相等。

全程只允许 `lstat/stat/read/list/hash`。禁止delete、rename、chmod、touch、write、补artifact、same-root rerun
或作为新evidence owner。

### 3.2 Accepted C0 evidence root

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c0-offline/eq-r6-c0-98de1a9-20260727T1324
```

执行前后对其完整tree生成sorted manifest：

```text
relative path
file type
bytes
SHA-256 for every regular file
symlink target if any
directory mode
```

before与after必须byte-equivalent；至少重新验证上表C0 validation/terminal hashes。不得写入C0 root。

### 3.3 New C1E1 root

唯一允许的新canonical root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424
```

创建前必须不存在、非symlink，父链均为regular non-symlink directories。只能创建一次；创建后禁止删除、
清空、重建、第二次generator或另建替代root。

## 4. Pre-root in-memory gate

在创建新root前，一个one-shot in-memory owner必须先完成：

1. 核对第2、3节所有hash/commit/root facts；
2. 核对staged paths为空且production/test/wrapper/docs/skill相对HEAD无diff；
3. 冻结historical before manifests；
4. 验证下面canonical artifact name/order与实际writer order完全相等；
5. 验证summary计数规则，不允许artifact自哈希循环；
6. 运行第5节所有tests/checks，输出与case results先保存在process memory；
7. 再次核对source/test hashes与historical roots未变。

只有1–7全部通过才可创建新root。若test或code defect出现，停止并请求Planner另开code correction；不得在
C1E1编辑source/test。

允许使用stdin/heredoc中的一次性Python evidence owner；不得把generator写入repo或历史root。测试临时fixture
必须使用 `/Volumes/4T/temp/rgbww-optimizer` 下自动清理的noncanonical temporary directories，不能命名成
或冒充C1E1 canonical root。

## 5. Required fresh replay

### 5.1 Runtime binding

fresh运行：

- `test_runtime_binding_entry_rejects_each_pid_and_argv_drift`
- `test_runtime_binding_seal_rejects_wrapper_child_root_and_candidate_drift`
- `test_exact_runtime_binding_passes_entry_and_terminal_seal`

matrix必须逐项记录实际结果：

```text
entry 8:
  outer_pid
  wrapper_pid
  runner_pid
  argv_append
  argv_duplicate
  argv_remove
  argv_reorder
  argv_replace

seal 4:
  wrapper_pid
  child_pid
  run_dir
  candidate_runner_pid

positive:
  exact entry + seal binding pass
```

每个negative case都必须由fresh production validator/orchestrator调用支持，不能只引用C1 handoff文字。
entry cases记录adapter calls=0；seal cases记录fake final-zero calls=1、candidate2 launches=0。

### 5.2 Final-zero/BaseException

fresh运行：

- `test_outer_final_zero_and_failure_evidence_cover_all_exit_paths`

matrix逐项记录：

```text
run_runtime_error
run_keyboard_interrupt
run_system_exit
subprocess_nonzero
missing_wrapper_result
malformed_wrapper_result
tampered_wrapper_pid
missing_candidate_result
tampered_launch_ledger
seal_reference_failure
final_zero_runtime_error
final_zero_keyboard_interrupt
primary_and_final_zero_failure
```

每项必须记录 `final_zero_calls=1`、outer terminal/failure存在、outer result absent、candidate2=0，以及
expected/actual exception type；SystemExit必须记录code 7。

### 5.3 Regression/static

至少运行：

```text
all tests in tests/test_p7_td_b_r6_contract.py
post-commit targeted four C1 methods
all tests covering measure_p7_thermal_diagnostics and production wrapper
full unittest discover
python compileall for frozen measurement runner
zsh -n tmp/run-p7-thermal-diagnostics.zsh
git diff --check
CodeGraph sync + relevant changed-symbol/blast-radius inspection
```

Baseline：

```text
C1 focused = 161/161
C1 full = 622/622
C1 post-commit targeted = 4/4
C1 post-commit EQ contract = 49/49
```

C1E1不得少于baseline或出现新failure。若因test selection重叠，summary必须分别记录command级totals，
不得把同一测试重复相加成“unique tests”。

## 6. Canonical artifact order

actual writer必须按以下exact顺序exclusive-write：

```text
01 frozen-inputs.json
02 historical-roots-before.json
03 implementation-candidate-manifest.json
04 runtime-binding-adversarial-matrix.json
05 final-zero-baseexception-matrix.json
06 regression-results.json
07 side-effect-accounting.json
08 codegraph-audit.json
09 historical-roots-after.json
10 strict-json-preterminal-audit.json
11 validation-summary.json
12 terminal-summary.json
```

创建root前，以一个literal ordered name list同时驱动order assertion与writer；禁止另写一份不同顺序的
planned list。`historical-roots-after.json` 写入前必须重做旧roots manifest并证明与before exact相等。

所有JSON：

- atomic/exclusive create，regular non-symlink，mode固定；
- UTF-8、strict JSON、`allow_nan=False`、末尾单一newline；
- 不包含secret、token、private override或 `.env` 内容；
- 写后立即read/strict-parse/hash，任何失败即hard stop且不修补。

## 7. Truthful summary and non-circular seal

### 7.1 Preterminal audit

`strict-json-preterminal-audit.json` 只审计01–09：

```text
audited_count = 9
parsed_count = 9
mismatches = []
```

它不得提前声称validation/terminal已解析。

### 7.2 Validation summary

`validation-summary.json`：

- `artifacts`只列01–10的absolute path/bytes/SHA-256；
- `indexed_preterminal_count=10`；
- 不列自身hash，不列terminal；
- 分开记录implementation tests、fresh evidence replay与seal状态；
- 记录runtime `12/12 + positive`、final-zero `13/13`的case-level truth；
- 记录command totals、unique/overlap semantics；
- `REV-EQ-R6-C0-001/002`只能写
  `candidate_fix_replayed_waiting_for_terminal_seal`，不能提前写closed；
- `mismatch` arrays全部基于真实检查；
- `this_package_executed_eq_r6=false`；
- `human_confirmation_preserved=true`；
- `commit_created=false`。

### 7.3 Terminal summary

`terminal-summary.json` 最后写：

- 引用01–11各自path/bytes/SHA-256，`sealed_artifact_count_excluding_self=11`；
- strict-parse validation summary后才写，并记录其schema/status/hash；
- terminal自身不在自己的sealed list中，不记录自己的SHA；
- 明确：

```text
terminal_self_count = 1
terminal_self_sha256_in_document = false
root_json_count_after_terminal = 12
```

- 只有此时才可将两项finding写为 `closed_by_replay_and_terminal_seal`；
- status只有所有tests、historical immutability、zero counters、preterminal audit、validation与terminal write
  全通过时才为pass。

terminal写完后，one-shot owner必须read/strict-parse全部12 JSON并计算terminal外部SHA；结果只写入
EXECUTION_RESULT handoff，不回写任何artifact。这样避免self-hash悖论。

任何count/hash/order错误：保持root原状，报告失败，不重跑、不补写、不另建root。

## 8. Zero-side-effect contract

真实调用全部必须为0：

```text
network / DNS / hostname / .env
backend construction / device / camera / Ray / strip
real all_off / final-zero / nonzero light
CR3 / NPY / TIFF capture
real EQ root / visible Terminal / EQ-R6
release generation / qualification / consumption
formal R6 / strip stage / TD-C / public analyzer
firmware / deployment / retry / relaunch
```

fresh tests中的final-zero、CR3、sidecar均必须是injected fake/temp fixture并单独计数。通过forbidden counters、
process args和artifact scan证明；不能只写“未观察到”。

## 9. No-code/no-commit contract

本包：

```text
source edits = 0
test edits = 0
wrapper/docs/skill edits = 0
git stage = 0
git commit/amend/rebase = 0
push/PR = 0
```

执行前后HEAD必须保持 `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`，第2节source hashes与commit
tree不变。若evidence replay暴露新code defect，只记录evidence并停回Planner，不得现场修复。

## 10. Executer handoff

仅向 `.agent-work/EXECUTION_RESULT.md` 追加：

- frozen preflight与historical before/after manifests摘要；
- exact fresh test commands/totals/case matrices；
- zero-side-effect counters；
- canonical order、12个artifact refs；
- validation SHA与external terminal SHA；
- HEAD/source/test unchanged proof；
- `REV-EQ-R6-C0-001/002` closure candidate；
- Planner decision request。

必须明确：

```text
C1E1 did not execute EQ-R6
no code commit was created
Human confirmation remains preserved
device execution remains Planner-locked
next decision belongs to Planner
```

维护性判断：C1E1不改代码，只修复证据生成顺序与seal语义；使用一个ordered owner和非循环summary规则，
避免再建立平行evidence index。若fresh replay发现实现问题，应回到独立code correction，而不是把逻辑塞进
evidence generator。

---

## Planner review：REF-P7-23-C1E1 accepted

**Review 时间：** 2026-07-27 14:45（America/Edmonton）

**Reviewed PLAN SHA-256：**
`704881fad58c6acc59361e560c32e8e1720a98b66d93ef9020c6e2b92bf45372`

**Reviewed EXECUTION_RESULT SHA-256：**
`e12bc1ec790a3106dc3d16ab14d1280d6698da7810fb9beff9ee3946cf117509`

**Orchestrator review FULL SHA-256：**
`250185852b4911432ba5378ee275c2d75f2d69a34cbd23f68ce771f673517252`

### Accepted evidence

Canonical root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424
```

Key artifacts：

- `validation-summary.json` SHA-256：
  `b670f74df58d81a952dcd1628be098449e841bedbe1ee29226922e6c13ad1703`
- `terminal-summary.json` SHA-256：
  `7e9ec5ea118dd8b67c83f213913e03fc7e2765154c86c8c6b4c98e75c3e2b680`

Planner独立只读重放确认：

```text
canonical JSON = exact 12 regular non-symlink files
validation indexed preterminal = 10/10, all bytes/hash exact
terminal sealed artifacts excluding self = 11/11, all bytes/hash exact
terminal self count = 1
terminal self hash in document = false
root JSON after terminal = 12
strict preterminal JSON = 9/9
runtime negative = 12/12 pass
runtime positive entry+seal = pass
final-zero/BaseException = 13/13 pass
fresh C1 methods = 4/4
EQ contract = 49/49
focused = 161/161
full = 622/622
historical C0 and failed-empty-C1 before/after manifests = exact equal
failed empty-root digest = 52378315a05a2b72d990aeace832287ce3a5dfe28c2ab1b37abe72ac43f2abf9
all mismatches = []
real device/network/env/backend/camera/light/all_off/capture/EQ/release = 0
HEAD unchanged = 93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
new commit = 0
```

### Planner decision

```text
REF-P7-23-C1E1 = ACCEPTED_COMPLETE
REF-P7-23-C1 = ACCEPTED_COMPLETE through C1E1 sealed evidence
REV-EQ-R6-C0-001 = CLOSED
REV-EQ-R6-C0-002 = CLOSED
implementation commit 93e72b8 = accepted as EQ-R6 execution candidate
```

C1E1把implementation tests与evidence seal正确分离，summary/terminal不存在self-hash循环；C0/C1历史
roots未被修改。无需Advisor进一步决定。

### Residual risks and locks

- accepted只证明runner、runtime binding、failure cleanup与offline evidence合同；不证明真实设备ready、
  exposure qualified或scientific result；
- Human exact confirmation仍有效，范围仅为1/2500与clipping-only条件下1/3200、最多8 CR3、retry0、
  每档A600+C600及完整cleanup/seal；
- release、full R6、strip、TD-C、public analyzer、firmware/deployment仍锁定；
- 真实EQ必须使用新root、单一visible Terminal outer launch和后续automation review，不能复用任何offline root；
- 任一predevice、cleanup、readback、quality、ledger或terminal failure均hard stop且不得retry。

### Exact next branch

```text
REF-P7-23
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
one real bounded EQ execution
single outer launch
physical CR3 cap = 8
retry = 0
```

Planner将active PLAN改写为唯一实际EQ-R6 package。该package直接消费已归档Human确认，不再重复询问；
完成或失败后必须停回Planner，禁止自动进入release、full R6、strip或TD-C。
