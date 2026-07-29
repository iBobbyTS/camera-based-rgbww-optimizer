# REF-P7-23-C2E1 / C2 one-shot evidence lifecycle correction

**计划状态：** `executable_pure_offline_evidence_only`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C2E1`

**Parent reference task：** `REF-P7-23-C2`

**PLAN contract ID：** `P7-TD-B-EQ-R6-C2-ONE-SHOT-EVIDENCE-CORRECTION`

**Package kind：** `bounded_pure_offline_evidence_only`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-C2-ONE-SHOT-EVIDENCE-CORRECTION","reference_task_id":"REF-P7-23-C2E1","parent_reference_task_id":"REF-P7-23-C2","package_kind":"bounded_pure_offline_evidence_only","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"fresh_replay_and_seal_c2_candidate_with_exactly_one_evidence_owner_invocation","human_eq_r6_confirmation_preserved":true,"human_eq_r6_confirmation_consumed":false,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"device_access":"forbidden","network_access":"forbidden","dns_access":"forbidden","env_access":"forbidden","backend_access":"forbidden","camera_access":"forbidden","ray_access":"forbidden","strip_access":"forbidden","light_access":"forbidden","real_all_off_access":"forbidden","real_capture_cap":0,"real_eq_root_creation_authorized":false,"eq_r6_launch_authorized":false,"release_generation_authorized":false,"release_consumption_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"public_analyzer_authorized":false,"evidence_owner_invocation_cap":1,"canonical_root_acquisition_cap":1,"retry":0,"planner_stop_required":true}`

**当前唯一动作：** 只读冻结commit `0f36671a`、旧C2 root、C1E1 root与真实EQ family；随后只启动一次
one-shot offline evidence owner。该owner在同一process中fresh重放C2 targeted/regression checks，全部通过后
直接在已存在且safe的 `/Volumes/4T/temp/rgbww-optimizer` 下取得一个canonical root一次，并按exact顺序
写入12个immutable JSON artifacts。

**唯一 Planner 停止点：** 任一preflight、test、owner launch、parent/root、artifact、hash、immutability或
terminal检查失败，立即在 `.agent-work/EXECUTION_RESULT.md` 追加handoff并停止。不得创建缺失container后
重试，不得第二次invoke owner、第二次取得root、same-root repair或alternative root。terminal成功也必须
停止交Planner；不得访问设备或解锁live prelaunch/EQ。

## 1. C2 review decision

Reviewed：

```text
PLAN SHA-256 =
  0b75cf6449200764fb200c2d48bba7b047358f1bb4d62823790df068867f60fd
EXECUTION_RESULT SHA-256 =
  e0bb8bb080b81c0bd8323599ff9b3c9df6ed6461964ca6d9f7e5c5fff3d37d40
Orchestrator FULL SHA-256 =
  0ff5aa2d8488fc30fa84803d85cdbe6d4c77ae9c4bd86905bd7d6c4fb6d1a41e
commit / HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Code/test candidate facts：

```text
commit parent = 93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
commit subject = fix(p7): add eq-r6 prelaunch owner
commit path count = 2
new targeted = 6/6
EQ contract = 55/55
focused = 167/167
full = 628/628
real side effects = 0
real FAMILY = absent
```

Acceptance blocker：

```text
first evidence-owner pre-acquisition stop = 1
reason = missing noncanonical container parent
canonical artifacts on first stop = 0
container then created = true
later evidence-owner execution = true
canonical root acquisitions = 1
reported retry = 0
```

PLAN要求任一root/evidence检查失败立即stop，且one-shot owner、second generator0。第一次pre-acquisition
已经是owner invocation；stop后创建container并再次执行，属于第二generator。`canonical_root_acquisitions=1`
不等于`generator_invocations=1`。

Decision：

```text
REF-P7-23-C2 = REJECTED_EVIDENCE_OWNER_RESTART_AFTER_STOP
REV-EQ-R6-C2-001 = OPEN
implementation commit 0f36671 = retained immutable candidate
Human confirmation = preserved and unconsumed
live prelaunch/EQ/device = locked
Advisor decision = not required
next = REF-P7-23-C2E1
```

Review archive：

```text
.agent-work/PLANS/20260727-1535-p7-eq-r6-c2-evidence-lifecycle-rejection-review.md
SHA-256 20108a74fcc2eea169e317f69a475da2963039fd93f9a8e780548d7697858b14
```

## 2. Pure-offline boundary

本包真实调用全部必须为0：

```text
network / DNS / hostname / .env
real backend construction / device / camera / Ray / strip / light
real Python all_off / zsh-child all_off / independent final-zero
capture / CR3 / NPY / TIFF
real EQ FAMILY / PRELAUNCH / RUN
Terminal dispatch / outer / wrapper / candidate
release generation / consumption
formal R6 / strip stage / TD-C / public analyzer
firmware / deployment / commit / retry / relaunch
```

只允许运行fake/injected tests、hash/manifest/static checks和one-shot evidence writer。Human exact EQ-R6确认
仍未消费；C2E1通过也不自动授权live。

## 3. Frozen implementation candidate

| Input | Frozen value |
|---|---|
| HEAD / candidate commit | `0f36671a351d537f204e8bc20849ac83e7e57c2b` |
| commit parent | `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8` |
| measurement runner SHA-256 | `b58fb6c314dcf3ad17241690ffa66cd1b0bb01776321d438af2dd318a79f2ccb` |
| focused test SHA-256 | `240c30d894c911a82a0c46193672900e470454c299e6d53f12386a003b201dff` |
| thermal contract SHA-256 | `34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3` |
| exposure policy SHA-256 | `9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |
| GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| rejected C2 validation SHA-256 | `f32690b06f1392ceedf6c301e8a2cb23ee5e2183367b475058a96fb92029cb78` |
| rejected C2 terminal SHA-256 | `a5b533095aa88e19cd6dae60c403f2ef53557ce697e635f55a57eea0a5e528a7` |

Exact commit path set：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

任一HEAD、commit metadata/path或frozen hash不符，停止。不得编辑或新commit。

## 4. Immutable historical inputs

### 4.1 Rejected C2 evidence root

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2-offline/c2-93e72b8-20260727T1507
```

它必须保持read-only。C2E1 owner在开始和结束时生成完整sorted tree manifest：

```text
relative path
file type
mode
bytes
SHA-256 for regular files
symlink target if any
```

before/after必须exact相等，并重新验证其12个JSON、validation/terminal hashes与
`pre_acquisition_container_missing_stop=1`。不得改counter、补artifact、rename或删除。

### 4.2 Accepted C1E1 evidence root

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424
```

同样生成before/after whole-tree manifest并要求exact相等。

### 4.3 Real EQ family

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445
```

before/after必须absent，且访问仅限 `lstat`。不得创建其parent family。

## 5. Canonical C2E1 root

唯一允许的新root直接位于已存在safe parent下：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2e1-0f36671-20260727T1535
```

固定parent：

```text
/Volumes/4T/temp/rgbww-optimizer
```

在调用owner前，Executer只读验证：

- parent及其全部父链已存在、是regular directories、不是symlink；
- exact root不存在且不是symlink；
- 不需要也不允许创建intermediate container；
- staged paths为空，production/test相对HEAD clean；
- 当前PLAN/FULL/EXECUTION_RESULT/archives hashes已记录。

如果parent/root/preflight任一失败：stop。不得修复parent后再invoke owner。

## 6. Exactly one owner invocation

允许一个stdin/heredoc形式的ephemeral Python owner，但不得写入repo或保存为第二generator。Executer只能
launch该owner一次：

```text
evidence_owner_process_invocations = 1
canonical_root_acquisitions = 1
second_generator = 0
retry = 0
alternative_root = 0
```

该同一process必须：

1. 重新验证第3–5节；
2. 创建一个scratch temporary directory于
   `/Volumes/4T/temp/rgbww-optimizer`，明确标记noncanonical并在finally删除；
3. 设置child `TMPDIR`到该scratch，禁止repo `tmp/`与system `/tmp`；
4. fresh运行第7节全部checks并在memory中保存command、exit、count和sanitized output；
5. 再次验证source hashes、historical roots和real FAMILY；
6. 只有1–5全部pass才exclusive创建exact C2E1 root，mode `0700`；
7. 按第8节exact顺序一次写入；
8. terminal完成后退出，不得再打开canonical files作写入。

若owner在任何阶段失败：

- 保留truthful stdout/stderr和已写progressive evidence；
- 不删除或重建canonical root；
- 不第二次调用owner；
- stop交Planner。

Subprocess tests、compileall、CodeGraph命令不是generator invocation；但它们只能由该single owner process
发起，不能在失败后由Executer单独补跑并继续seal。

## 7. Fresh replay

### 7.1 Exact C2 targeted methods

fresh运行以下6个methods，必须 `6/6`：

```text
test_positive_prelaunch_has_exact_order_modes_counts_and_no_dispatch
test_injected_prelaunch_never_reaches_real_dependency_owners
test_readiness_negative_matrix_seals_failure_and_runs_all_cleanups
test_cleanup_and_final_zero_baseexception_matrix_is_all_path
test_root_atomic_and_manifest_validation_fail_closed_matrix
test_cli_handoff_and_secret_absence_matrix
```

### 7.2 Regression commands

fresh运行：

```text
all tests in tests/test_p7_td_b_r6_contract.py
focused tests covering measure_p7_thermal_diagnostics, wrapper and analyzer
full unittest discover
python compileall frozen measurement runner
zsh -n tmp/run-p7-thermal-diagnostics.zsh
git diff --check
CodeGraph sync + run_td_b_eq_r6_prelaunch/main/blast-radius inspection
```

Minimum exact baselines：

```text
targeted = 6/6
EQ contract = 55/55
focused = 167/167
full = 628/628
```

不得failure/skip增加或count回退。command selection重叠分别报告，不相加冒充unique tests。

所有测试必须使用fake/injected adapters；owner必须记录real side effects0。测试或CodeGraph失败立即stop，
不创建canonical root。

## 8. Exact evidence artifact order

Owner只能按以下顺序atomic exclusive-write：

```text
01-frozen-inputs.json
02-rejected-c2-root-before.json
03-implementation-candidate-manifest.json
04-fresh-targeted-replay.json
05-fresh-regression-results.json
06-rejected-c2-matrix-replay.json
07-lifecycle-and-side-effect-accounting.json
08-codegraph-audit.json
09-historical-roots-after.json
10-strict-json-preterminal-audit.json
11-validation-summary.json
12-terminal-summary.json
```

Contract：

- root mode `0700`；files mode `0600`；
- regular non-symlink、resolved within exact root；
- UTF-8 strict JSON object、sorted keys、`allow_nan=False`、single trailing newline；
- same-directory temporary、atomic replace、tmp count0；
- exclusive first-write，无overwrite；
- writer order与上表exact相等；
- 02记录rejected C2与C1E1 before manifests；
- 06逐项重放旧C2 matrices与12 JSON引用，但明确旧terminal non-authorizing；
- 07必须truthful记录：

```text
prior_C2_generator_invocations >= 2
prior_C2_canonical_root_acquisitions = 1
current_C2E1_owner_invocations = 1
current_C2E1_canonical_root_acquisitions = 1
current_C2E1_pre_acquisition_stops = 0
current_C2E1_retry = 0
real side effects all zero
real FAMILY absent
```

- 09记录rejected C2、C1E1、real FAMILY after并与before exact比较；
- 10只审计01–09，strict JSON count `9/9`；
- 11只索引01–10，indexed count10，不自哈希、不引用terminal；
- 12只引用01–11，sealed count11，不含self hash；
- terminal写后canonical root JSON count exact12；
- terminal external SHA-256只由handoff记录，不回写root。

## 9. Independent post-terminal audit

Owner退出后，Executer只读一次：

1. lstat exact root与12 paths；
2. strict parse `12/12`；
3. verify exact names/order/modes/path containment；
4. recompute bytes/SHA-256 references；
5. verify validation/terminal non-circular counts；
6. verify current owner invocation/acquisition/retry lifecycle；
7. verify rejected C2/C1E1 before-after exact；
8. verify real FAMILY absent；
9. verify production/test clean、staged empty、HEAD unchanged；
10. scan artifacts/outputs for private camera/Ray sentinel leakage；
11. verify real side effects0。

发现任何mismatch只能报告failure；不得回写或重跑。

## 10. Acceptance contract

C2E1只有同时满足以下才可请求Planner接受：

1. commit `0f36671`与exact two-file hashes/path set未变；
2. fresh `6/55/167/628`与static checks全部pass；
3. rejected C2 root明确标为non-authorizing且before/after immutable；
4. C1E1 root before/after immutable；
5. direct safe parent预检一次通过，无container creation；
6. owner invocation exact1；
7. canonical root acquisition exact1；
8. pre-acquisition stop0、retry0、second generator0、alternative root0；
9. exact 12 artifacts/order/mode/strict JSON/hash/seal；
10. real side effects全部0、real FAMILY absent；
11. independent post-terminal audit mismatch arrays全部空；
12. Human confirmation仍preserved/unconsumed。

通过时可：

```text
REF-P7-23-C2E1 = ACCEPTED
REF-P7-23-C2 = ACCEPTED_THROUGH_C2E1
REV-EQ-R6-C2-001 = CLOSED_BY_NEW_ONE_SHOT_SEAL
```

任何一项失败均为 `C2E1_REJECTED_OR_INCOMPLETE`，不得解锁live route。

## 11. Handoff and stop

向 `.agent-work/EXECUTION_RESULT.md` 追加：

- frozen hashes与owner exact command SHA-256；
- owner process invocation count/PID/exit；
- scratch path lifecycle；
- root acquisition/retry/second-generator accounting；
- exact test commands/counts；
- historical before/after manifests；
- artifact path/bytes/SHA-256/order；
- validation/terminal external SHA-256；
- independent audit results；
- real side-effect counters与real FAMILY absence；
- exact Planner decision request。

然后停止。不得修改PLAN/FULL、source/test、旧root或commit；不得运行live prelaunch/EQ。

## 12. 维护性判断

C2E1不修改生产代码，只修复offline evidence generation lifecycle。它使用一个process、一个direct root、
一个literal artifact order和非循环validation/terminal seal，不新增生产抽象或device path。fresh regression
继续覆盖single prelaunch owner的正常、BaseException、root、atomic与secret边界；无需Advisor或架构重构。

---

## 13. Planner review — 2026-07-27

### 13.1 Reviewed inputs

```text
PLAN SHA-256 =
  362202a7b355c607a9defdad6572087665cea4d05e95cbc6e429bf781e812bf5
EXECUTION_RESULT SHA-256 =
  8a76643cc9a153e0d2c33d19ccae389ba5a9e538b2d01c04328110aa6ef7f934
Orchestrator FULL SHA-256 =
  4d4fe8ce7e9e0b03d9258d050b04c631f1fbdc31be087b6f93a7074a2bca87d9
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
handoff =
  EXECUTION_RESULT.md §141
```

Lifecycle：

```text
preflight command attempts = 1
preflight exit = 1
evidence owner invocations = 0
canonical root acquisitions = 0
canonical artifact writes = 0
retry / second generator / alternative root = 0
real side effects = 0
planned C2E1 root = absent
```

### 13.2 Finding

`REV-EQ-R6-C2E1-001`：

Executer自行从hash description推导了两个不存在的路径：

```text
wrong:
  src/camera_based_rgbww_optimizer/optimization/thermal_diagnostics.py
  config/p7-td-b-ray-c-exposure-policy-v2.json

exact:
  src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  config/hsi/p7-ray-td-b-exposure-policy-v2.json
```

首个read-only preflight command因此exit1。PLAN要求任一preflight failure立即stop且不得修正后继续；
Executer正确停止，没有invoke owner或创建root。本次是Planner冻结输入缺少exact path mapping导致的离线
执行歧义，不是code/test/scientific failure。

Orchestrator独立验证exact paths：

```text
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
```

### 13.3 Decision

```text
REF-P7-23-C2E1 = REJECTED_PREFLIGHT_PATH_MAPPING_FAILURE
REV-EQ-R6-C2E1-001 = OPEN
implementation commit 0f36671 = retained immutable candidate
Human confirmation = preserved and unconsumed
device/live prelaunch/EQ = locked
Advisor escalation = not required
next = REF-P7-23-C2E2 exact-path evidence-only successor
```

C2E2必须冻结所有输入的exact repo paths、hashes和可逐字执行的preflight command；不得让Executer通过
basename、hash description、glob或搜索推导路径。C2E1 planned root保持absent。
