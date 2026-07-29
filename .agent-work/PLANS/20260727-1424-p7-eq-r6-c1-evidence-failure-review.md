# REF-P7-23-C1 / EQ-R6 runtime binding 与 final-zero correction

**计划状态：** `executable_pure_offline_correction`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C1`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-RUNTIME-BINDING-AND-FINAL-ZERO-CORRECTION`

**Package kind：** `bounded_offline_implementation_and_validation`

**Expected parent HEAD：** `57985fa74301e26d097c96e69e52661714fea7b3`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-RUNTIME-BINDING-AND-FINAL-ZERO-CORRECTION","reference_task_id":"REF-P7-23-C1","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_offline_implementation_and_validation","expected_parent_head":"57985fa74301e26d097c96e69e52661714fea7b3","single_current_action":"repair_eq_r6_runtime_binding_and_all_outer_final_zero_paths","human_eq_r6_confirmation_preserved":true,"device_access":"forbidden","network_access":"forbidden","env_access":"forbidden","camera_access":"forbidden","ray_access":"forbidden","strip_access":"forbidden","light_access":"forbidden","real_all_off_access":"forbidden","real_capture_cap":0,"real_eq_root_creation_authorized":false,"release_generation_authorized":false,"release_consumption_authorized":false,"eq_r6_launch_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"focused_commit_authorized":true,"planner_stop_required":true}`

**当前唯一动作：** 基于已提交的 C0 owner，只修复 launch ledger 的 exact runtime identity/argv绑定、
terminal seal 的 wrapper/child ownership关联，以及 outer owner所有失败路径的 best-effort independent
final-zero与failure terminal evidence；使用全 injected fresh adversarial tests证明失败关闭。

**唯一 Planner 停止点：** 完成两项修复、新一次性offline evidence root、focused/full/static验证与一个
focused commit后立即停止，在 `.agent-work/EXECUTION_RESULT.md` 追加handoff交Planner验收。不得启动
EQ-R6、visible Terminal、设备、真实cleanup、capture、release或后续stage。

## 1. C0 review decision

Reviewed C0 PLAN：

- SHA-256：
  `8779e9312a471da87eeb4324d29aea37f03e8eacb83ed85ae8e79d68d0b5a043`
- EXECUTION_RESULT §136 SHA-256：
  `d9113e4216a34cb69827f2b6846e6ebcbc6378c51d2d5fe1fdd2d81976c93900`
- Orchestrator stable active-C1 FULL SHA-256：
  `a5dd25566a458233feb6d1d04569e5abfd7e5b360dc1a49d7cf5e821610d74da`
- 本次 FULL hash 更新仅记录 orchestration transition；不扩展设备、EQ、capture、release、权限、
  budget、root或后续stage边界。
- rejection archive：
  `.agent-work/PLANS/20260727-1401-p7-eq-r6-c0-rejection-review.md`
- rejection archive SHA-256：
  `804245bb5886fef09f99d44654d9c1779e114a4388e752504ec92264bb3b8f1e`

Decision：

```text
REF-P7-23-C0 = REJECTED_ACCEPTANCE_BLOCKING
REV-EQ-R6-C0-001 = open
REV-EQ-R6-C0-002 = open
```

C0 commit `57985fa74301e26d097c96e69e52661714fea7b3` 及其通过的实现不撤销、不rebase。
C1是 ordinary code correction，不需要Advisor改变科学方向。

Human exact EQ-R6确认仍有效：

- confirmation archive：
  `.agent-work/PLANS/20260727-1324-p7-eq-r6-human-checkpoint-live-owner-review.md`
- SHA-256：
  `9a8f959d9a471a9226a26ac829272665df88f8c6a0ffe70a690fb9cef88138a6`

C1不改变candidate、shutter、强度、时长、budget或branch；若C1通过，后续无需向Human重复请求同一确认。

## 2. Frozen inputs 与 preflight

| Input | Frozen value |
|---|---|
| parent HEAD/C0 commit | `57985fa74301e26d097c96e69e52661714fea7b3` |
| parent | `98de1a91c264d4b72c4a97fc499ae7d39a67dacc` |
| applicable GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| measurement runner SHA-256 | `cd6519367cb150028df74f3bf8924fce862f40371ff5ca4f2680f546621abefa` |
| thermal contract SHA-256 | `34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3` |
| focused EQ test SHA-256 | `d73d5bf4ffec73b17381a60ccdba3b6ddd9f564480b2bfd655b69497a7af758a` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |
| project skill SHA-256 | `c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607` |
| C0 validation SHA-256 | `aca05551c26f512799cb2de0eea2342d30ace04360a71ac29b29fe0e56d541a2` |
| C0 terminal SHA-256 | `a33aa0ec87a37ae98cde1d5762acd65e0513a57fd04babea84735728ae5f9a6b` |

首次改动前必须fail closed确认：

1. HEAD等于 expected parent；
2. 上述source/test/wrapper/GUIDE/C0 evidence hashes全部相等；
3. staged paths为空；
4. existing unrelated dirty/untracked PLAN/FULL/EXECUTION_RESULT/advisor/archive work保持原样，不得stage、
   修改、恢复或重排；
5. 新correction root不存在，且父级不是symlink：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1-offline/eq-r6-c1-57985fa-20260727T1401
```

任一不符：不改代码、不创建commit，记录mismatch并停回Planner。

## 3. Exact scope 与 ownership

仅允许修改：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

不得修改：

- `p7_thermal_diagnostics.py` scientific/live activation contract；
- production wrapper、camera backend、physical-return owner、all_off owner；
- docs/skill/project policy；
- PLAN、FULL、GUIDE/RESEARCH、EXECUTION_RESULT history或既有archives。

修复必须保持：

```text
1/2500 -> clipping-only才1/3200
candidate IDs/order = C0 exact values
per candidate = A600 + C60/120/300/600
physical cap = 4 each / 8 total
formal = 0
ambient = 0
retry/relaunch = 0
58 features / all quality gates unchanged
```

若两文件内无法在不复制wrapper/camera/cleanup owner的情况下完成，停回Planner；不得扩大scope。

## 4. REV-EQ-R6-C0-001：exact runtime binding

### 4.1 Ledger schema and expected values

`_validate_td_b_eq_r6_launch_ledger` 必须接收并核对调用方已知的expected runtime values，至少包括：

```text
expected_outer_pid
expected_wrapper_pid
expected_child/runner_pid
expected exact child argv
```

允许使用canonical immutable binding digest，但digest input必须完整覆盖上述四项、candidate index/root、
checkpoint与source hashes；不能仅验证digest格式。

要求：

- PID必须是non-bool positive int且与expected逐值相等；
- argv必须是ordered list of exact strings，与expected length/order/value完全相等；
- append/remove/reorder/duplicate任意“安全”flag也必须reject；
- argv中的private/secret规则继续保留；
- ledger必须明确绑定runner child PID，使 wrapper result的child ownership可验证；
- ledger仍exclusive write、不可覆盖；不得以mtime、权限位或“文件只读”代替内容binding。

### 4.2 Two validation points

同一exact validator/binding owner必须在两处执行：

1. **candidate device entry前：** 在任何backend construction、strip/Ray/camera/all_off adapter前，使用
   current outer PID、current parent wrapper PID、current runner PID和current exact child argv验证；
2. **terminal seal前：** 使用outer owner冻结的expected outer PID/exact argv，以及
   `wrapper-result.json`/candidate result中的wrapper与child ownership再次验证。

任一验证失败：

```text
device adapter calls = 0 if failure is at candidate entry
terminal seal status != pass
candidate 2 launch = 0
outer result cannot be success
```

### 4.3 Wrapper/child ownership in terminal seal

terminal owner必须严格验证现有production wrapper result schema及至少以下关系：

```text
wrapper-result.wrapper_pid == launch-ledger.wrapper_pid
wrapper-result.child_pid == launch-ledger.child/runner_pid
candidate-result runtime child PID == wrapper-result.child_pid
candidate-result runtime wrapper PID == launch-ledger.wrapper_pid
launch-ledger.outer_pid == expected outer PID
launch-ledger.argv == expected exact child argv
wrapper-result.run_dir == exact candidate root
```

missing、null、bool-as-int、wrong type、wrong PID、wrong run_dir、wrong argv、extra/missing key、malformed JSON、
symlink或hash/tamper均fail closed。terminal seal必须包含或引用可重放的runtime binding及canonical hashes。

## 5. REV-EQ-R6-C0-002：all-path best-effort final-zero

### 5.1 Unconditional attempt boundary

每个已经attempted launch的candidate，outer owner都必须在控制流离开该candidate前恰好尝试一次
`final_zero_fn()`，包括：

- `run_fn`正常0/nonzero返回；
- `run_fn`抛 `Exception`；
- `run_fn`抛 `KeyboardInterrupt`、`SystemExit`或其他`BaseException`；
- wrapper-result missing/malformed/tampered/symlink；
- child/wrapper PID ownership mismatch；
- candidate result、shell cleanup或launch ledger missing/malformed/tampered；
- `_seal_eq_candidate`解析、reference、validation或write failure；
- final-zero自身抛任意`BaseException`。

不得把final-zero放在任何wrapper artifact presence/validity check之后的可跳过branch。

### 5.2 Durable failure evidence

outer root必须使用atomic、fail-closed owner持久化每次attempt：

```text
candidate index
launch attempted
wrapper return/exception if known
final-zero attempted = true
final-zero status/evidence or exact exception type/message
primary failure
seal failure
candidate 2 remained locked
recorded_at
```

若candidate subroot缺失、是symlink或不可信，不得跟随它写证据；改由outer-owned deterministic failure
artifact保存final-zero与terminal failure。若subroot安全，可同时写canonical candidate artifact，但outer evidence
必须足以证明attempt。

无论 final-zero成功还是失败，只要primary wrapper/artifact/seal失败：

- 写failure terminal artifact；
- 写/更新outer-failure；
- 不写success outer-result；
- 不解锁candidate 2；
- 重新抛出失败。

### 5.3 BaseException semantics

允许临时catch `BaseException` 只为完成best-effort final-zero和持久化failure evidence。完成后：

- `KeyboardInterrupt`、`SystemExit`及原始BaseException必须保持非成功并重新抛出，不得转换为return 0；
- ordinary primary failure不得被final-zero pass覆盖；
- final-zero failure不得被primary success覆盖；
- primary与final-zero同时失败时两者都要记录，不能丢失primary；
- evidence write failure也不能产生success；
- candidate 2 attempted launch count必须为0。

## 6. Fresh adversarial tests

不得只更新旧断言名称或matrix文案。必须真实调用production validators/orchestrator并断言：

### 6.1 Runtime binding matrix

从一个原本合法的ledger分别单变量tamper：

```text
outer_pid = another positive int
wrapper_pid = another positive int
child/runner_pid = another positive int
argv append safe flag
argv duplicate existing safe flag
argv remove element
argv reorder two elements
argv replace value with another safe value
wrapper-result.wrapper_pid drift
wrapper-result.child_pid drift
wrapper-result.run_dir drift
candidate-result runtime PID drift
```

每个case均必须在对应entry/seal处reject；entry类case所有device adapters为0，seal类casecandidate2 launch为0。
另测 exact valid binding在candidate entry与seal两次通过。

### 6.2 Final-zero failure matrix

至少逐case fresh root测试：

```text
run_fn raises RuntimeError
run_fn raises KeyboardInterrupt
run_fn raises SystemExit(7)
subprocess return nonzero
missing wrapper-result
malformed wrapper-result JSON
tampered wrapper-result PID
missing candidate-result
tampered launch ledger
seal reference/hash failure
final_zero_fn raises RuntimeError
final_zero_fn raises KeyboardInterrupt
primary failure + final_zero failure
```

每个已launch case必须断言：

```text
final_zero_calls == 1
durable final-zero attempt evidence exists
failure terminal artifact exists
outer-failure exists
outer-result absent/non-success
candidate-2 launch count == 0
raised type/status remains non-success
```

`KeyboardInterrupt`/`SystemExit`case必须证明原type/exit code未被吞掉。

### 6.3 Regression

必须继续通过：

- candidate 1 4/4 pass不启动candidate 2；
- clipping-only在first seal之后只启动一次candidate 2；
- non-clipping、cleanup、final-zero、seal failure阻止candidate 2；
- physical-return-before-processing与sidecar failure retention；
- CLI mode isolation；
- existing setup/formal/release behavior；
- production wrapper real zsh fake runtime roundtrip。

## 7. Validation and truth requirements

至少执行并记录：

```text
new runtime-binding targeted tests
new all-path final-zero targeted tests
full tests/test_p7_td_b_r6_contract.py
all tests covering measure_p7_thermal_diagnostics and production wrapper
full pytest suite
python compileall for touched Python
zsh -n tmp/run-p7-thermal-diagnostics.zsh
strict JSON parse of every new evidence JSON
git diff --check
CodeGraph sync + changed-symbol/blast-radius audit
```

C0 reported `124/124` focused与`618/618` full是baseline；C1不得新增failure。所有matrix case的
`status=pass`必须能映射到真实fresh test name、expected、actual与call counters；不能用宽泛旧测试冒充
PID/argv/final-zero覆盖。

## 8. Zero-side-effect budget

```text
network calls = 0
.env reads = 0
real backend construction/calls = 0
device/camera/Ray/strip calls = 0
real all_off/final-zero calls = 0
nonzero light output = 0
CR3/NPY/TIFF capture = 0
real EQ root/visible Terminal launch = 0
release generation/qualification/consumption = 0
formal R6/strip/TD-C/public analyzer = 0
firmware/deployment = 0
retry/relaunch = 0
```

必须由injected forbidden counters证明为0；fake `final_zero_fn` calls单独计数，不得误报为真实all_off。

## 9. New evidence root

只允许创建一次：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1-offline/eq-r6-c1-57985fa-20260727T1401
```

至少包含：

```text
frozen-inputs.json
implementation-manifest.json
runtime-binding-adversarial-matrix.json
final-zero-baseexception-matrix.json
regression-results.json
side-effect-accounting.json
strict-json-audit.json
codegraph-audit.json
validation-summary.json
terminal-summary.json
```

`validation-summary.json` 必须记录：

- C0 finding IDs与各自closed/open状态；
- 每个matrix的真实case/test/actual/counters；
- parent/new HEAD、actual changed/committed paths；
- focused/full/static totals；
- canonical artifact absolute path、bytes、SHA-256；
- mismatch arrays；
- real EQ/device/network/env/camera/light/all_off/capture/release均0；
- `human_confirmation_preserved=true`；
- `this_package_executed_eq_r6=false`。

C0 root与artifact严格只读。新root首次落盘后不得修补、重建或第二次运行；若summary/matrix有误，报告失败并
停回Planner。

## 10. Focused commit

全部验证通过后创建：

```text
fix(p7): bind eq-r6 runtime and final zero
```

要求：

- parent exact为 `57985fa74301e26d097c96e69e52661714fea7b3`；
- commit paths只能是第3节两个允许文件中实际修改者；
- 不stage PLAN/FULL/EXECUTION_RESULT/archives/advisor或任何unrelated dirty/untracked path；
- commit前记录staged paths与blob hashes；commit后验证parent/message/path set；
- commit后重跑new targeted、完整EQ focused、`zsh -n`、`git diff --check`及CodeGraph sync；
- 不push、不建PR、不生成release。

实现或验证失败时不得创建部分成功commit。

## 11. Executer handoff

Executer仅向 `.agent-work/EXECUTION_RESULT.md` 追加：

- frozen preflight；
- exact code changes与ownership说明；
- 两组fresh adversarial matrices及call counters；
- focused/full/static/CodeGraph结果；
- zero-side-effect counters；
- new root及canonical hashes；
- commit SHA/parent/message/path set；
- `REV-EQ-R6-C0-001/002` closure evidence；
- residual risk与Planner decision request。

handoff必须明确：

```text
C1 did not execute EQ-R6
Human confirmation remains preserved
device execution remains Planner-locked
next decision belongs to Planner
```

维护性判断：C1只修复现有 measurement runner内部的runtime binding与outer failure-finalization边界，
不新增runner、wrapper、camera或cleanup owner。测试必须覆盖PID/argv逐字段重绑定和BaseException清理矩阵；
若需要改scientific contract或复制production wrapper，应停止而不是扩展实现。

---

## Planner review：REF-P7-23-C1 rejected，code candidate retained

**Review 时间：** 2026-07-27 14:24（America/Edmonton）

**Reviewed PLAN SHA-256：**
`e8d809fae33ad2f0dc9bc0490f27c317d230c843770b3a67b5ebcca99fec36a4`

**Reviewed EXECUTION_RESULT：**
`.agent-work/EXECUTION_RESULT.md` §137，SHA-256
`0b76df7de274245408176027cd75b06b6c51621b646de8519959061e3e8f99a9`

**Orchestrator review FULL SHA-256：**
`ecbe023eba7e5e8eee92515dfc51d23cc0fcb4a3f6307a102775d064a2ddc4c6`

### Implementation candidate

C1 commit：

```text
commit = 93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
parent = 57985fa74301e26d097c96e69e52661714fea7b3
message = fix(p7): bind eq-r6 runtime and final zero
paths =
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  tests/test_p7_td_b_r6_contract.py
```

Committed SHA-256：

```text
measurement runner = 7738b73b37f389fde998eb4911efd74d1a40370181866af93736c0544894b938
focused test = 01a185e6d68bf0acef9db4f19362a6b316b8d4f063dc80a3844fcff6500e9877
```

Reported validation quality：

```text
runtime binding matrix = 12/12 pass
final-zero/BaseException matrix = 13/13 pass
focused = 161/161 pass
full = 622/622 pass
post-commit targeted = 4/4 pass
post-commit EQ contract = 49/49 pass
compileall / zsh -n / diff-check / CodeGraph = pass
```

这些结果针对 C0 findings建立了实质修复候选：

- `REV-EQ-R6-C0-001`：expected outer/wrapper/runner PID与ordered exact argv在entry/seal双重绑定；
- `REV-EQ-R6-C0-002`：每个attempted candidate所有 `BaseException`/artifact/seal路径恰好一次
  best-effort final-zero并保留failure evidence。

代码边界集中在既有measurement runner与focused tests，没有修改scientific contract、wrapper、camera或
cleanup owner。Planner允许保留commit作为下一证据包的immutable implementation candidate；不得revert、
amend、rebase或重做相同代码。

### Terminal evidence failure

PLAN冻结的唯一C1 root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1-offline/eq-r6-c1-57985fa-20260727T1401
```

Planner独立只读复核：

```text
exists = true
type = regular directory
symlink = false
mode = 0700
top-level entry count = 0
file count = 0
JSON count = 0
validation-summary.json = absent
terminal-summary.json = absent
```

Empty-root canonical manifest使用
`empty_root_manifest_v1`、absolute/resolved path、device/inode、mode、type/symlink flags、空entries及三个
zero counts，以sorted-key compact JSON计算；SHA-256为
`52378315a05a2b72d990aeace832287ce3a5dfe28c2ab1b37abe72ac43f2abf9`。

生成器在创建root后、写任何JSON前，因in-memory canonical order将
`codegraph-audit.json` 放在 `strict-json-audit.json` 前，而planned order相反，以
`planned order mismatch` hard-fail。Executer正确遵守same-root不可修补合同：没有删除、补写、重跑或
另建root。

因此 implementation tests与 evidence seal必须分开判断。C1缺少required matrices、validation summary、
terminal summary、strict JSON seal与canonical hashes；不得把测试通过或空root写成package pass。

### Planner decision

```text
REF-P7-23-C1 = REJECTED_TERMINAL_EVIDENCE_ABSENT
implementation commit 93e72b8 = retained candidate, not yet accepted for device use
REV-EQ-R6-C0-001/002 = candidate-fixed, closure pending sealed evidence
```

这是ordinary offline evidence-owner correction，不需要Advisor科学决定。Human exact EQ-R6确认继续有效，
但设备与EQ execution仍锁定。

### Residual locks

- 失败C1 root必须保持empty、只读观察，不得删除、chmod、touch、补写或重建；
- C0 evidence roots与artifacts保持不变；
- 不得revert/amend/rebase C1 commit；
- 下一包不得修改scientific/device code；若fresh replay发现新code defect，立即停回Planner另开code package；
- device、network、`.env`、backend、camera、Ray、strip、real all_off/final-zero、capture、EQ、
  release、formal R6、strip stage与TD-C均为0；
- C1E1完成前，不得将两项finding标记closed或启动真实EQ-R6。

### Exact next branch

```text
REF-P7-23-C1E1
P7-TD-B-EQ-R6-C1-EVIDENCE-SEAL-CORRECTION
pure offline evidence-only
code parent/head = 93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
```

C1E1先在内存/临时非canonical scratch中验证canonical order owner，再创建一个新的unique root一次；
重跑必要的fresh injected tests，生成truthful matrices、validation summary与terminal seal，并以before/after
manifest证明失败C1 empty root仍empty、C0 roots immutable。若只形成证据，不需要新code commit。
