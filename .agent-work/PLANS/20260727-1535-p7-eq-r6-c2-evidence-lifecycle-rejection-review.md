# REF-P7-23-C2 / EQ-R6 single prelaunch owner correction

**计划状态：** `executable_pure_offline_code_correction`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C2`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-PRELAUNCH-OWNER-CORRECTION`

**Package kind：** `bounded_pure_offline_code_and_test`

**Expected HEAD：** `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-PRELAUNCH-OWNER-CORRECTION","reference_task_id":"REF-P7-23-C2","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_pure_offline_code_and_test","expected_head":"93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8","single_current_action":"implement_and_validate_one_production_eq_r6_prelaunch_owner_with_fake_adapters_only","human_eq_r6_confirmation_preserved":true,"human_eq_r6_confirmation_consumed":false,"source_edits_authorized":true,"test_edits_authorized":true,"exact_edit_allowlist":["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_contract.py"],"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"single_focused_commit_authorized":true,"device_access":"forbidden","network_access":"forbidden","dns_access":"forbidden","env_access":"forbidden","backend_real_access":"forbidden","camera_real_access":"forbidden","ray_real_access":"forbidden","strip_real_access":"forbidden","light_access":"forbidden","real_all_off_access":"forbidden","real_capture_cap":0,"real_eq_root_creation_authorized":false,"eq_r6_launch_authorized":false,"release_generation_authorized":false,"release_consumption_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"public_analyzer_authorized":false,"retry":0,"planner_stop_required":true}`

**当前唯一动作：** 只在existing measurement runner中新增一个single production EQ-R6 prelaunch owner及其CLI
入口，并只在existing focused test file中用fake/injected camera、Ray、strip、cleanup、final-zero和subprocess
adapters覆盖success/failure contracts。完成fresh tests、focused commit与immutable offline evidence后停止。

**唯一 Planner 停止点：** C2 focused commit和offline terminal evidence完成，或任一preflight、implementation、
test、secret、root、artifact、hash、commit或evidence检查失败时，立即在
`.agent-work/EXECUTION_RESULT.md` 追加handoff并停止交Planner。不得访问真实network、`.env`、device、camera、
Ray、strip或light；不得创建真实EQ family、运行EQ、dispatch Terminal、capture、生成/消费release或进入后续stage。

## 1. REF-P7-23 review decision

Reviewed：

```text
PLAN SHA-256 =
  08a67a07e4df19a5ecb5bd6a909db1ebb95169909968a7c53083cc5a9d550475
EXECUTION_RESULT SHA-256 =
  a0b94720f8d89f245f9ad0ae78968f5c2baa74c46bee828ce01a2088e6a9461f
Orchestrator FULL SHA-256 =
  7bbeeca5a574f42d3fbe145650475b1847fb8045a2a4388e12e29af464de7245
HEAD =
  93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
```

Decision：

```text
REF-P7-23 live execution = REJECTED_PRELAUNCH_OWNER_ABSENT
Human exact EQ-R6 confirmation = preserved and unconsumed
real FAMILY/PRELAUNCH/RUN creation = 0
dispatch / Terminal / EQ launch = 0
next = REF-P7-23-C2 pure-offline correction
Advisor decision = not required
```

Executer在device/network/.env access前确认production缺少single prelaunch owner并fail closed，符合计划安全
边界。该失败是ordinary local orchestration/evidence implementation缺口，不改变Advisor的shutter、
quality、budget或科学branch。

Reviewed PLAN archive：

```text
.agent-work/PLANS/20260727-1507-p7-eq-r6-prelaunch-owner-failure-review.md
SHA-256 8466fa3fcfc468c379da9797a51b59fa0f5d234431019ccca7d9d9042cc11c24
```

## 2. Authorization boundary

本PLAN是pure offline code correction：

```text
real device/network/DNS/.env/backend/camera/Ray/strip/light = 0
real Python/shell all_off/final-zero = 0
real CR3/NPY/TIFF = 0
real EQ family/PRELAUNCH/RUN = 0
Terminal dispatch / outer / candidate = 0
release/formal R6/strip stage/TD-C/public analyzer = 0
retry/relaunch = 0
```

所有设备行为只能由fake/injected adapters执行。测试必须安装fail-fast guards，任何未注入的socket、
URL opener、`.env` read、真实backend construction、subprocess all-off、Ray/ESPHome或capture调用立即使测试
失败。

Human exact confirmation继续冻结但本包不消费：

> 我确认进入 EQ-R6：先运行 1/2500，仅在 clipping-only 失败时运行 1/3200；最多 8 张 CR3、retry 0、每档 A600+C600，并执行双 cleanup、final-zero 和 terminal seal。

C2通过不等于EQ-R6获准启动。必须由Planner验收C2、Orchestrator更新FULL并另写新的single live PLAN。

## 3. Exact edit and commit allowlist

只允许修改：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

禁止修改：

```text
.agent-work/PLAN.md
.agent-work/FULL_PLAN_REFERENCE.md
advisor/
docs/
.agents/skills/
config/
tmp/run-p7-thermal-diagnostics.zsh
all other src/ and tests/ paths
```

允许测试在 `/Volumes/4T/temp/rgbww-optimizer` 下创建自动清理的temporary fake roots。不得在repo `tmp/`
或system `/tmp` 写scratch。

完成全部pre-commit validation后，允许一个focused commit：

```text
fix(p7): add eq-r6 prelaunch owner
```

只stage上述两个allowlisted files；不得 `git add -A`、amend、rebase、push或建PR。commit后必须重新核对
exact committed path set并运行第9节post-commit checks。

## 4. Frozen inputs and preflight

| Input | Frozen value |
|---|---|
| HEAD | `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8` |
| measurement runner SHA-256 | `7738b73b37f389fde998eb4911efd74d1a40370181866af93736c0544894b938` |
| thermal contract SHA-256 | `34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3` |
| focused test SHA-256 | `01a185e6d68bf0acef9db4f19362a6b316b8d4f063dc80a3844fcff6500e9877` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |
| exposure policy SHA-256 | `9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2` |
| GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| reviewed FULL SHA-256 | `7bbeeca5a574f42d3fbe145650475b1847fb8045a2a4388e12e29af464de7245` |

执行前必须：

1. 记录当前PLAN SHA-256；
2. 核对HEAD与上述source/test/config/wrapper hashes；
3. 核对staged paths为空；
4. 核对allowlist外production/test/docs/skill/wrapper/config相对HEAD无本轮新增diff；
5. 核对真实family仍不存在：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445`；
6. 对真实family parent chain只做 `lstat/stat`，不得DNS、network、`.env`或device probe；
7. 冻结C1E1 evidence root与§139 handoff的before manifest；
8. 运行CodeGraph relevant symbol/blast-radius preflight。

任一不符停止，不得先编辑再解释。

## 5. Production prelaunch owner

### 5.1 Ownership and placement

在measurement runner现有EQ-R6 helper/outer owner附近建立一个cohesive private helper group和一个公开模块
entry function，例如：

```text
run_td_b_eq_r6_prelaunch(...)
```

只有该function拥有prelaunch state machine、stage ordering、canonical artifact writing、failure seal和
launch handoff。`main()`只验证CLI contract并调用该owner；不得在CLI、Executer脚本、wrapper或测试中复制
第二套流程。

为测试可注入：

```text
camera backend factory
Ray readiness callable
Python cleanup callable
shell cleanup subprocess callable
independent final-zero callable
clock / PID if required
```

production defaults必须复用现有：

- `camera_remote.create_camera_backend(... remote ...)`；
- backend `connect`、`resolve_capture_settings`、`read_shutter_current_and_choices`；
- `ray120c.get_hsi`；
- `all_off.turn_everything_off`；
- independent strip `verified_light(0,0,0,0,0)` + Ray zero/readback +
  `hsi_source_evidence.validate_both_off`；
- strict JSON atomic/exclusive writer和existing frozen curve/policy owners。

不得新增root-level CLI wrapper、新module、parallel runner、new credential loader或new device abstraction。

### 5.2 New CLI mode

在existing mutually exclusive EQ mode中新增：

```text
--eq-r6-prelaunch
```

未来production invocation contract固定为：

```text
--execute
--allow-device-control
--eq-r6-prelaunch
--experiment-id p7_td_b_command_switch_history_v1
--source ray
--phase formal
--output-dir <exact FAMILY>
--run-name prelaunch
--code-checkpoint <exact full lowercase HEAD>
--human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend remote
```

owner必须derive：

```text
PRELAUNCH = <output-dir>/prelaunch
RUN = <output-dir>/run
```

CLI hard reject：

- missing `--execute`、`--allow-device-control`、checkpoint或exact Human authorization；
- experiment/source/phase/backend drift；
- simultaneous orchestrate/single-candidate/setup/release/lineage modes；
- non-default env/base-url override for this exact mode；
- unknown or extra prelaunch-affecting state；
- unsafe/existing/symlink/path-escaping FAMILY/PRELAUNCH/RUN。

C2只测试该CLI，严禁真实调用它。CLI测试必须注入owner/adapters并证明real dependencies=0。

### 5.3 Root acquisition

production owner在任何backend construction、`.env`、network或device call之前：

1. validate full lowercase checkpoint/current tree；
2. validate absolute FAMILY/PRELAUNCH/RUN关系；
3. `lstat` every existing parent；拒绝symlink/non-directory；
4. 要求FAMILY、PRELAUNCH、RUN全部fresh；
5. exclusive创建FAMILY和PRELAUNCH，mode `0700`；
6. `RUN`保持absent。

root rejection发生在canonical ownership acquisition之前时，必须no mutation、adapter calls0、dispatch0并
raise明确类型；由于没有safe canonical root，不能伪造terminal pass。

成功取得PRELAUNCH后，所有semantic/backend/cleanup failure都必须走第7节exact failure seal。不得删除、
清空、重建、rename或same-root second run。

### 5.4 Ordered stages

owner取得safe PRELAUNCH后，严格按：

```text
1 frozen inputs and source hashes
2 exact offline EQ-R6 plan and live-output contract
3 camera readiness
4 Ray readiness
5 Python cleanup
6 shell cleanup
7 independent final-zero
8 terminal decision and launch handoff
9 manifest
```

Camera readiness：

```text
backend_name == remote
v2_capture_capability exact
connect exactly once
resolve_capture_settings(iso=None, aperture=None, image_format="RAW") exactly once
resolved ISO/aperture non-empty
resolved image_format == RAW
capture_with_timing callable
read_shutter_current_and_choices exactly once
choices contain 1/2500 and 1/3200
capture calls = 0
settings writes = 0
```

Ray readiness只调用 `get_hsi` exactly once并验证response/data schema；不得set非零。

即使camera或Ray readiness失败，仍必须按顺序各attempt一次Python cleanup、shell cleanup和independent
final-zero。一个cleanup失败不得阻止后续cleanup/final-zero。

Shell cleanup production default必须以argv-list、`shell=False`启动独立 `zsh` child，再由该child
`exec` existing `.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json`；不得把token、
Ray override或`.env`内容放入argv。owner必须strict parse stdout、记录return code，并将stderr仅作
secret-safe/redacted accounting。

Independent final-zero必须与前两个cleanup function owner不同，验证：

```text
strip generation strictly advances and five channels are zero
Ray zero command succeeds
fresh Ray readback intensity == 0
validate_both_off passes
```

## 6. Secret boundary

Production prelaunch owner：

- 不接受camera token或Ray secret CLI argument；
- camera token只可被existing backend从default project `.env`读入process memory；
- Human-classified public Ray shared default继续合法，不得删除、脱敏或误报为private secret；
- `AMARAN_OPENAPI_SECRET` override若存在是private runtime value；
- 不得serialize/repr/log/hash/prefix/suffix/length任何camera token或private Ray override；
- backend config object、request headers、authorization/token fields不得进入artifact；
- exception message、stdout/stderr、adapter response在写artifact前必须drop或deterministically redact sensitive
  values/keys；
- canonical artifacts、printed CLI result和launch handoff必须secret-free。

Fake secret tests至少注入：

```text
camera token sentinel
private Ray override sentinel
sentinel in exception message
sentinel in shell stdout/stderr
token/authorization/secret/password key names
```

所有PRELAUNCH bytes、captured stdout/stderr、launch argv及handoff扫描结果必须0 match。测试使用显式
fake env mapping（不得读取真实process environment）证明public Ray default仍可构造合法settings且不被代码
删除或当成missing credential。

## 7. Exact nine-artifact seal

成功取得PRELAUNCH后，canonical writer只能按exact顺序atomic exclusive-write：

```text
01 frozen-inputs.json
02 offline-plan.json
03 camera-readiness.json
04 ray-readiness.json
05 all-off-python.json
06 all-off-shell.json
07 independent-final-zero.json
08 prelaunch-terminal.json
09 prelaunch-manifest.json
```

合同：

- root mode `0700`，files mode `0600`；
- regular non-symlink files，resolved within PRELAUNCH；
- strict UTF-8 JSON object、sorted keys、`allow_nan=False`、single trailing newline；
- temporary file与target同目录，atomic replace，完成后 `.tmp` count0；
- first-write exclusive；拒绝overwrite、second owner和same-root repair；
- 每个stage记录 `attempted/pass/fail/not_attempted`、call count和safe exception type；
- 不记录未发生的call，不把command attempt冒充readback pass；
- `prelaunch-terminal.json`引用01–07的path/bytes/SHA-256；
- terminal status只可能 `pass` 或 `fail`；
- pass要求camera/Ray/readiness、Python/shell cleanup、independent final-zero全pass；
- terminal内嵌secret-free launch handoff，见第8节；
- manifest最后写，只引用01–08；不自哈希；
- terminal/manifest不形成循环引用；
- root最终canonical JSON count exact `9`。

Camera failure时Ray artifact必须truthful `not_attempted`，但三种cleanup仍attempted。任一primary/cleanup/
final-zero/evidence/secret check失败都必须terminal `fail`、dispatch-ready false、outer launch count0。

若filesystem使terminal/manifest本身无法写入，不得返回pass；保留已写progressive evidence并raise hard
failure。测试至少覆盖single stage writer failure不会出现false pass或遗留被误认的complete manifest。

## 8. Launch-dispatch handoff

prelaunch owner本身不得dispatch。只有all stages与secret scan pass时，
`prelaunch-terminal.json.launch_handoff` 才可包含：

```text
ready_for_dispatch = true
dispatch_count = 0
outer_launch_count = 0
exact RUN path
exact checkpoint
exact Human authorization ID
secret-free outer argv list
canonical argv SHA-256
```

outer argv必须等价于冻结production command：

```text
.venv/bin/python
-m
camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics
--execute
--allow-device-control
--eq-r6-orchestrate
--experiment-id
p7_td_b_command_switch_history_v1
--source
ray
--phase
formal
--output-dir
<FAMILY>
--run-name
run
--code-checkpoint
<checkpoint>
--human-authorization
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend
remote
```

不得包含 `--remote-env-file`、`--remote-base-url`、token或Ray key。handoff只准备future live PLAN消费，
不得调用subprocess/Terminal/outer/wrapper/candidate。任一fail状态必须
`ready_for_dispatch=false`且不提供可执行argv。

## 9. Required fake/adversarial tests

### 9.1 Positive exact path

至少证明：

```text
camera factory/connect/resolve/shutter-read = 1/1/1/1
camera capture/capture_with_timing invocation = 0
Ray get_hsi = 1
Ray nonzero set = 0
Python cleanup = 1
shell cleanup = 1
independent final-zero = 1
outer/wrapper/candidate/Terminal dispatch = 0
RUN creation = 0
exact artifacts/order/count = 9
terminal = pass
launch handoff ready = true, dispatch_count = 0
```

### 9.2 Readiness matrix

逐项fresh fake case：

```text
camera factory Exception / KeyboardInterrupt / SystemExit
camera connect Exception / KeyboardInterrupt / SystemExit
backend name drift
v2 capability missing/drift
resolve settings missing/malformed/non-RAW
capture_with_timing missing/noncallable
shutter choices missing 1/2500
shutter choices missing 1/3200
Ray get_hsi Exception / KeyboardInterrupt / SystemExit
Ray response missing data/malformed
```

每项证明capture0、dispatch0；取得PRELAUNCH后的case必须三种cleanup各1并terminal fail。camera fail后的
Ray calls0；Ray fail前camera readiness已pass。

### 9.3 Cleanup/final-zero matrix

逐项fresh fake case：

```text
Python cleanup fail / KeyboardInterrupt / SystemExit
shell cleanup nonzero / malformed JSON / Exception / KeyboardInterrupt / SystemExit
final-zero strip non-generation-bearing
final-zero strip nonzero
final-zero Ray nonzero
final-zero validate_both_off failure
final-zero Exception / KeyboardInterrupt / SystemExit
primary + Python cleanup failure
primary + shell cleanup failure
primary + final-zero failure
all three cleanup owners fail
```

每项attempt accounting truthful，后续cleanup不被前一failure跳过，terminal fail，launch handoff locked。

### 9.4 Root and artifact matrix

至少覆盖：

```text
relative/path escape
symlink parent
FAMILY exists
PRELAUNCH exists
RUN exists
second invocation
artifact symlink/existing target
atomic writer failure
manifest reference bytes/hash drift
terminal reference drift
extra JSON artifact
malformed/nonfinite JSON
wrong mode/path escape
```

root rejection必须adapter calls0、filesystem mutation0；post-acquisition failure不得false pass。

### 9.5 CLI/handoff and secret matrix

覆盖第5.2节所有CLI rejection、exact positive injected call、outer argv exact order/hash、no dispatch、
camera/Ray/private exception/shell-output secret sentinels、sensitive key names及public Ray default preservation。

### 9.6 Existing regressions

必须fresh运行并保留exact command-level counts：

```text
new C2 targeted methods
all tests in tests/test_p7_td_b_r6_contract.py
all tests covering measure_p7_thermal_diagnostics and production wrapper
full unittest discover
python compileall changed measurement runner
zsh -n tmp/run-p7-thermal-diagnostics.zsh
git diff --check
CodeGraph sync + changed-symbol/blast-radius inspection
```

Baseline：

```text
pre-C2 EQ contract = 49/49
pre-C2 focused = 161/161
pre-C2 full = 622/622
```

不得少于baseline、不得failure/skip增加。重叠selection按command分别报告，不把重复测试相加冒充unique
coverage。

## 10. Focused commit and post-commit validation

全部第9节pre-commit checks通过后：

1. `git diff --check`；
2. staged path exact等于第3节两个files；
3. 创建唯一focused commit `fix(p7): add eq-r6 prelaunch owner`；
4. 验证commit parent为expected HEAD；
5. 验证commit path set exact，无plan/docs/skill/wrapper/config；
6. post-commit fresh运行new C2 targeted methods、全部EQ contract tests、compileall、wrapper syntax；
7. 验证production/test相对新HEADclean且staged empty；
8. 不amend/rebase/push。

若commit或post-commit失败，停止并保留truthful state，不得隐式第二commit。

## 11. Immutable offline evidence package

只有implementation、full validation、focused commit和post-commit checks全部通过后，才可创建一次：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2-offline/c2-93e72b8-20260727T1507
```

创建前必须absent/non-symlink且父链safe。一个one-shot offline evidence owner按exact顺序exclusive-write：

```text
01 frozen-inputs.json
02 implementation-manifest.json
03 positive-prelaunch-matrix.json
04 readiness-negative-matrix.json
05 cleanup-baseexception-matrix.json
06 root-atomic-artifact-matrix.json
07 secret-absence-cli-handoff-matrix.json
08 regression-results.json
09 codegraph-audit.json
10 side-effect-accounting.json
11 validation-summary.json
12 terminal-summary.json
```

Evidence root mode `0700`、files `0600`、strict JSON、atomic exclusive、regular non-symlink。validation引用01–10，
不得自哈希；terminal引用01–11，root JSON count exact12，terminal self hash只由handoff外部记录。

必须在01与10/11中记录before/after：

```text
real FAMILY remains absent
C1E1 root whole-tree unchanged
reviewed §139 source inputs unchanged except exact allowlisted commit
network/.env/device/camera/Ray/strip/light/real-all-off/capture/EQ/release calls = 0
fake adapter calls separately labeled
```

测试temporary roots不得纳入canonical evidence root；生成evidence后不得same-root repair、second generator或
alternative root。

## 12. Acceptance contract

C2只有同时满足以下才可请求Planner接受：

1. exact two-file commit，parent/HEAD/path/message正确；
2. single production prelaunch owner与`--eq-r6-prelaunch`入口存在；
3. real dependencies在owner内且均有injection seam；
4. checkpoint/root safety在backend construction前；
5. exact camera -> Ray -> Python -> shell -> final-zero ordering；
6. success与所有post-acquisition semantic/BaseException paths均形成truthful terminal decision；
7. exact nine canonical prelaunch artifacts/order/count/atomic/mode/hash合同；
8. failure不能产生ready handoff；
9. pass handoff exact outer argv且dispatch/outer calls0；
10. camera/private Ray secrets在artifacts/stdout/stderr/argv中0 match；
11. Human-classified public Ray default保留；
12. fake matrix和existing regressions全部pass，无baseline回退；
13. real side-effect counters全部0；
14. real EQ FAMILY仍absent；
15. immutable C2 validation/terminal evidence完整且hash闭合。

任何一项失败都只能报告 `C2_REJECTED_OR_INCOMPLETE`；不得说EQ ready或直接进入live。

## 13. Executer handoff and stop

只向 `.agent-work/EXECUTION_RESULT.md` 追加：

- PLAN/FULL/GUIDE/HEAD与pre/post commit hashes；
- exact changed/committed path set；
- CodeGraph pre/post blast-radius；
- each fake matrix actual counts/results；
- exact artifact/order/secret/root assertions；
- pre/post commit test commands和counts；
- side-effect accounting；
- C2 evidence root、validation/terminal path/bytes/SHA-256；
- real FAMILY absence和historical before/after；
- residual risks与exact Planner decision request。

然后停止。不得修改PLAN/FULL、不得运行new live prelaunch、不得dispatch EQ。

## 14. 维护性判断

本修复触及device-facing preflight、secret boundary、filesystem evidence和failure state，因此采用single owner、
injected adapters与adversarial tests。虽然measurement runner较大，但EQ-R6 outer/candidate ownership已集中
在该文件；将prelaunch helper group紧邻该边界，比新增parallel module或现场脚本更能保持单一state owner。
只允许局部private helpers，不建立第二framework。测试覆盖normal、failure、BaseException、root、atomic、
secret与CLI boundaries；C2后暂不建议架构重构，除非第三个实验复用同一prelaunch state machine。

---

## 15. Planner review — 2026-07-27

### 15.1 Reviewed inputs

```text
PLAN SHA-256 =
  0b75cf6449200764fb200c2d48bba7b047358f1bb4d62823790df068867f60fd
EXECUTION_RESULT SHA-256 =
  e0bb8bb080b81c0bd8323599ff9b3c9df6ed6461964ca6d9f7e5c5fff3d37d40
Orchestrator FULL SHA-256 =
  0ff5aa2d8488fc30fa84803d85cdbe6d4c77ae9c4bd86905bd7d6c4fb6d1a41e
commit / HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
commit parent =
  93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
commit subject =
  fix(p7): add eq-r6 prelaunch owner
```

Committed paths exact：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

Fresh checks reported：

```text
new targeted = 6/6
EQ contract = 55/55
focused = 167/167
full = 628/628
compileall / wrapper syntax / diff check / CodeGraph = pass
real side effects = 0
real EQ FAMILY = absent
```

C2 evidence：

```text
root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2-offline/c2-93e72b8-20260727T1507
canonical JSON count = 12
validation SHA-256 =
  f32690b06f1392ceedf6c301e8a2cb23ee5e2183367b475058a96fb92029cb78
terminal SHA-256 =
  a5b533095aa88e19cd6dae60c403f2ef53557ce697e635f55a57eea0a5e528a7
```

### 15.2 Acceptance-blocking finding

`REV-EQ-R6-C2-001`：

```text
pre_acquisition_container_missing_stop = 1
pre_acquisition_stop_created_canonical_root = false
canonical_root_acquisitions = 1
reported retry = 0
```

本PLAN的unique Planner stop规定任一root/evidence检查失败都必须立即handoff；§11又要求创建前父链safe、
one-shot evidence owner，且§11末尾禁止second generator。第一次evidence owner已执行pre-acquisition并因
容器父目录缺失停止，这就是一次root/evidence check failure。随后创建容器并再次运行owner，即使第一次没有
取得canonical root或写artifact，仍然是stop后的第二次generator invocation。

因此：

- `canonical_root_acquisitions=1`不能证明`generator_invocations=1`；
- `retry=0`与truthful lifecycle不一致；
- 12个artifact内容、测试green和real side effects0不能修复one-shot owner provenance；
- 旧root不得same-root补写、改counter或重新解释为pass。

### 15.3 Decision

```text
REF-P7-23-C2 = REJECTED_EVIDENCE_OWNER_RESTART_AFTER_STOP
REV-EQ-R6-C2-001 = OPEN
implementation commit 0f36671 = retained immutable candidate
Human exact EQ-R6 confirmation = preserved and unconsumed
device/live prelaunch/EQ = locked
Advisor escalation = not required
next = REF-P7-23-C2E1 minimal pure-offline evidence lifecycle correction
```

本裁决只拒绝C2 package acceptance，不要求回滚已提交代码。C2E1必须使用一个父目录已经存在且safe的直接
canonical root、一个owner process、一次generator invocation、一次root acquisition，重新形成独立terminal
seal。C2E1接受前不得把代码测试green解释为live readiness。
