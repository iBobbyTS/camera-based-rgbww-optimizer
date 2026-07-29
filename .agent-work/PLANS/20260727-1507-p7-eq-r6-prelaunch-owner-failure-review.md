# REF-P7-23 / EQ-R6 state-C exposure qualification

**计划状态：** `executable_real_bounded_device_package`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6`

**Package kind：** `single_launch_real_eq_r6`

**Expected HEAD：** `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6","reference_task_id":"REF-P7-23","package_kind":"single_launch_real_eq_r6","expected_head":"93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8","single_current_action":"preflight_then_launch_exactly_one_real_eq_r6_outer_owner","human_eq_r6_confirmation_satisfied":true,"human_authorization_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6","local_lab_device_scope":true,"device_access":"authorized_exactly_as_bounded_here","network_access":"local_lab_endpoints_only","env_access":"private_runtime_consumption_only","camera_access":"readiness_then_max_8_cr3","ray_access":"bounded_a600_c600_and_cleanup","strip_access":"zero_only","light_access":"authorized_exactly_as_bounded_here","real_all_off_access":"authorized","real_capture_cap":8,"formal_capture_cap":0,"ambient_capture_cap":0,"retry":0,"candidate_1_nominal_shutter":"1/2500","candidate_2_nominal_shutter":"1/3200","candidate_2_unlock":"candidate_1_first_failure_exactly_clipping_only_and_candidate_1_terminal_seal_pass","unique_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445/run","visible_macos_terminal_required":true,"single_outer_launch":true,"release_generation_authorized":false,"release_consumption_authorized":false,"formal_r6_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"public_analyzer_authorized":false,"source_edits_authorized":false,"test_edits_authorized":false,"commit_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 在冻结输入、fresh root、私密配置、相机/Ray只读能力与双源全零预检全部通过后，
只在一个可见 macOS Terminal 窗口中启动一次 production EQ-R6 outer owner。outer owner按冻结合同先运行
`1/2500`；仅当 candidate 1 的首个失败集合精确等于 `{"clipping"}` 且其完整cleanup/final-zero/seal通过时，
才由同一outer owner自动运行 `1/3200`。Executer只做三次稀疏、只读liveness检查；若仍运行，交回
Orchestrator建立automation；terminal后做最终只读审计。

**唯一 Planner 停止点：** preflight失败、launch失败、runtime hard failure，或EQ-R6写出terminal evidence后，
立即在 `.agent-work/EXECUTION_RESULT.md` 追加完整handoff并停止交Planner验收。不得retry、重新dispatch、
在同root续跑、手工启动candidate 2、运行public analyzer、生成/消费release、启动full R6、strip、combined TD-B
或TD-C，也不得修改本PLAN或 `FULL_PLAN_REFERENCE.md`。

## 1. C1E1 review decision

Reviewed package：

- reviewed PLAN SHA-256：
  `704881fad58c6acc59361e560c32e8e1720a98b66d93ef9020c6e2b92bf45372`
- reviewed EXECUTION_RESULT SHA-256：
  `e12bc1ec790a3106dc3d16ab14d1280d6698da7810fb9beff9ee3946cf117509`
- reviewed Orchestrator FULL SHA-256：
  `250185852b4911432ba5378ee275c2d75f2d69a34cbd23f68ce771f673517252`
- C1E1 validation：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424/validation-summary.json`
- validation SHA-256：
  `b670f74df58d81a952dcd1628be098449e841bedbe1ee29226922e6c13ad1703`
- C1E1 terminal：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424/terminal-summary.json`
- terminal SHA-256：
  `7e9ec5ea118dd8b67c83f213913e03fc7e2765154c86c8c6b4c98e75c3e2b680`

Planner独立复核：

```text
canonical JSON artifacts = exact 12
strict JSON = 9/9
runtime-binding negative cases = 12/12
final-zero/BaseException cases = 13/13
EQ contract suite = 49/49
focused suite = 161/161
full suite = 622/622
historical root mismatches = []
real network/device/env/camera/Ray/strip/capture/all_off side effects = 0
```

Decision：

```text
REF-P7-23-C1E1 = ACCEPTED
REF-P7-23-C1 = ACCEPTED_THROUGH_C1E1
REV-EQ-R6-C0-001 = CLOSED
REV-EQ-R6-C0-002 = CLOSED
commit 93e72b8 = accepted execution checkpoint
next = REF-P7-23 exact real EQ-R6
```

Review archive：

```text
.agent-work/PLANS/20260727-1445-p7-eq-r6-c1e1-acceptance-review.md
SHA-256 d78c3321f989e75f4f22bfd35e099e5c4dab025ee3e76a2b3b908318aa1e190e
```

## 2. Human authorization and hard scope

Human exact confirmation已满足且继续有效，不得重复询问：

> 我确认进入 EQ-R6：先运行 1/2500，仅在 clipping-only 失败时运行 1/3200；最多 8 张 CR3、retry 0、每档 A600+C600，并执行双 cleanup、final-zero 和 terminal seal。

该确认只授权本PLAN的单次EQ-R6：

```text
candidate 1 = nominal 1/2500
candidate 2 = nominal 1/3200, clipping-only conditional
source = Ray only
strip = generation-bearing verified zero only
physical CR3 cap = 8
formal = 0
ambient = 0
retry / recapture / relaunch = 0
```

这是Human自有本地摄影与照明实验室内的相机、Ray120c和
`bedroom-rgbww-strip.local` 操作。按项目规则，bounded light on/off、zero cleanup、只读设备能力/状态检查
无需另行Human授权；本PLAN已精确限定target、强度、时长、隔离、退出和恢复路径。

未授权且必须保持锁定：

- firmware upload/flash、remote deployment、破坏性硬件变更；
- 超出A/C状态、100% intensity或本PLAN时长的灯光操作；
- 第三档shutter、auto-exposure、weak reacquire、重复capture或第二次outer launch；
- release生成/消费、full R6、strip stage、combined TD-B、TD-C；
- public analyzer；
- source/test/docs/skill/wrapper修改或Git commit。

## 3. Frozen inputs

| Input | Frozen value |
|---|---|
| HEAD | `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8` |
| GUIDE | `advisor/4/4.GUIDE.md` |
| GUIDE SHA-256 | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| reviewed FULL SHA-256 | `250185852b4911432ba5378ee275c2d75f2d69a34cbd23f68ce771f673517252` |
| reviewed EXECUTION_RESULT SHA-256 | `e12bc1ec790a3106dc3d16ab14d1280d6698da7810fb9beff9ee3946cf117509` |
| exposure policy | `config/hsi/p7-ray-td-b-exposure-policy-v2.json` |
| exposure policy SHA-256 | `9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2` |
| measurement runner SHA-256 | `7738b73b37f389fde998eb4911efd74d1a40370181866af93736c0544894b938` |
| thermal contract SHA-256 | `34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3` |
| focused test SHA-256 | `01a185e6d68bf0acef9db4f19362a6b316b8d4f063dc80a3844fcff6500e9877` |
| production wrapper SHA-256 | `2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5` |
| project skill SHA-256 | `c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607` |

Source paths：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
tmp/run-p7-thermal-diagnostics.zsh
```

Executer开始前必须记录本PLAN的当前SHA-256和Orchestrator更新后的当前
`.agent-work/FULL_PLAN_REFERENCE.md` SHA-256。FULL变化只能是Orchestrator对C1E1 accepted、REF-P7-23 active
的状态过渡；它不扩展任何授权、budget、root或stage。任一冻结production/config/test/wrapper/GUIDE/skill
hash或HEAD不符即停止，不得自行纠偏。

## 4. Exact root ownership

唯一root family：

```text
FAMILY=/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445
PRELAUNCH=$FAMILY/prelaunch
RUN=$FAMILY/run
```

执行前：

- `FAMILY`、`PRELAUNCH`、`RUN`必须全部不存在且非symlink；
- `/Volumes/4T/temp/rgbww-optimizer`及其父链必须是regular non-symlink directories；
- 只允许创建一次 `FAMILY`；
- preflight只可创建 `PRELAUNCH`，创建后 `RUN`仍必须不存在；
- production outer owner是 `RUN` 的唯一创建owner；
- 禁止同root续跑、删除重建、rename替换、第二个timestamp root、alternative root或symlink；
- evidence的所有resolved paths必须留在 `FAMILY` 内。

## 5. Prelaunch gate

一个前台one-shot prelaunch owner按下列顺序运行。除明确的本地lab只读连接、zero/off外，不得产生任何
设备副作用；不得capture。

### 5.1 Offline freeze

先完成：

1. 核对第3节全部hash和HEAD；
2. 核对staged production/config/test/wrapper paths为空，且这些路径相对HEAD无diff；
3. 记录当前PLAN/FULL/EXECUTION_RESULT/GUIDE/archive path、bytes、SHA-256；
4. 核对root family fresh和父链；
5. 从production builder在内存中生成exact offline EQ-R6 plan并验证；
6. 验证 `formal=0`、`ambient=0`、physical cap8、retry0、两档shutter和8个exact capture IDs；
7. 验证production outer CLI、wrapper、runner、launch ledger和terminal seal owners存在且hash冻结；
8. 验证没有任何release、full-R6、strip-source、TD-C或public-analyzer调用路径被加入本launch。

Exact plan：

```text
experiment_id = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
source = ray
strip = zero only

candidate 1:
  000-ray-c2500-t60
  001-ray-c2500-t120
  002-ray-c2500-t300
  003-ray-c2500-t600

candidate 2:
  004-ray-c3200-t60
  005-ray-c3200-t120
  006-ray-c3200-t300
  007-ray-c3200-t600
```

### 5.2 Private runtime configuration

- project `.env`只可由现有camera backend在process memory中消费；
- `.env`必须是regular non-symlink file，resolved path在repo内；
- 只记录required variable是否存在的boolean和backend kind；不得记录value、长度、hash、prefix或suffix；
- camera token不得出现在argv、Terminal command、process listing、JSON、JSONL、Markdown或logs；
- Ray使用代码中已记录为public shared default的key，或process环境中现有合法override；不得把override值
  写入任何argv/artifact/log；
- 不得复制、脱敏后再落盘，或以“公开默认值”为理由把camera私密token写入evidence；
- prelaunch和terminal阶段都要对argv/artifacts做secret absence扫描，扫描结果只能是boolean/count。

### 5.3 Camera read-only readiness

在任何light on之前，使用现有remote-v2 backend和默认project `.env`：

1. `connect`成功；
2. backend identity/capability为formal remote-v2 owner；
3. `capture_with_timing` callable；
4. RAW image format已配置；
5. recorded settings/readback可用；
6. shutter choices同时包含nominal `1/2500`和`1/3200`。

只允许health/config/capability/settings readback；不得capture、不得写settings、不得触发shutter。

### 5.4 Ray read-only readiness

只调用现有Ray `get_hsi`/等价readback一次，验证本地lab endpoint可达、response schema合法。不得在此步骤
set非零。

### 5.5 Double-source zero gate

按固定顺序：

1. Python `all_off`：strip五通道全零；Ray intensity 0；
2. shell独立 `all_off`：strip五通道全零；Ray intensity 0；
3. independent final-zero：重新readback并验证strip generation-bearing全零、Ray intensity 0；
4. 调用现有 `validate_both_off`/同一冻结owner。

strip必须有generation-bearing readback；Ray必须有command/readback。任何cleanup/readback不完整、超时、
schema drift或非零均fail closed。

### 5.6 Prelaunch evidence

只在5.1–5.5全部通过后，atomic写入 `PRELAUNCH`：

```text
frozen-inputs.json
offline-plan.json
camera-readiness.json
ray-readiness.json
all-off-python.json
all-off-shell.json
independent-final-zero.json
prelaunch-terminal.json
prelaunch-manifest.json
```

每项至少记录path、bytes、SHA-256、timestamp、owner和truthful call/attempt counts。manifest不得自哈希；
terminal引用前八项，manifest最后写。所有JSON strict parse、regular file、non-symlink、resolved within
`PRELAUNCH`。写后立即核对source hashes和 `RUN=absent`。

任一prelaunch步骤失败：

- 仍尽力依次执行Python cleanup、shell cleanup、independent final-zero；
- 写truthful failure/terminal evidence到 `PRELAUNCH`；
- 不创建 `RUN`，不launch Terminal；
- stop交Planner，不得retry或新建root。

## 6. Exact production launch

prelaunch terminal pass后，只允许一次macOS Terminal `do script` dispatch。不得使用Codex-managed background
process、`nohup`、`&`、pipeline、`tee`、二层launcher或手工candidate wrapper。Terminal中执行exact：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW && exec .venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-orchestrate \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445 \
  --run-name run \
  --code-checkpoint 93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8 \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

不得添加 `--remote-env-file`、`--remote-base-url`、camera token、Ray key或任何其它argument。`exec`使Terminal
shell让位给唯一outer Python owner。

Executer必须在 `PRELAUNCH/launch-dispatch.json` 中exclusive-write：

```text
dispatch_count = 1
dispatch_timestamp
Terminal window/tab identifier
exact command SHA-256
outer PID when observed
FAMILY and RUN
checkpoint
secret_absent = true
retry = 0
```

不得记录secret值。若dispatch API返回不确定，也按已attempted处理：不得第二次dispatch。

## 7. Runtime owner and scientific contract

### 7.1 One outer owner

production outer owner必须：

- 唯一创建 `RUN` 和 `RUN/live-plan.json`；
- 唯一决定candidate 1后是否进入candidate 2；
- 每candidate只调用一次production wrapper；
- candidate wrapper启动一个runner；
- `launch-ledger.json`绑定outer PID、wrapper PID、runner PID、exact child argv、RUN、checkpoint及冻结source hashes；
- 不允许Executer手工调用candidate mode或wrapper。

Candidate 1 launch ledger首次出现后，Executer只读核对owner关系；不修改ledger。

### 7.2 Exact A-to-C sequence

每个实际启动的candidate：

```text
verify strip zero
A = H120/S100/INT100 for 600 s, no capture
switch directly A -> C
C = H300/S100/INT100
capture C at 60 s
capture C at 120 s
capture C at 300 s
capture C at 600 s
Ray off
verify both sources zero
```

资格帧使用formal相同native RAW measurement path，但每张都必须标记setup/non-formal；不得采A、ambient、
strip或历史frame，不得进入P6 compatibility。

### 7.3 Budget and attempts

```text
candidate 1 physical cap = 4
candidate 2 physical cap = 4
outer physical cap = 8
formal = 0
ambient = 0
scientific retry = 0
recapture = 0
outer relaunch = 0
```

每个slot最多一次capture调用。camera backend内部若记录transport attempt，必须truthful落盘，但不得把它
解释为允许第二次slot capture。CR3一经remote physical return，必须先持久化physical ledger，随后才可decode/
quality processing；即使后处理失败也不得漏记returned CR3/sidecar。

### 7.4 Per-frame quality

每个实际returned capture必须证明：

```text
58/58 exact required features available
clipped_fraction == 0.0 for every required feature
near-noise fraction <= 0.05
all required values finite
valid pixel count >= 29000
recorded Canon exposure present
nominal/recorded exposure ratio gate pass
Ray command/readback pass
strip generation/readback zero
source isolation pass
timing and physical-return evidence pass
```

不得删feature、改threshold、fallback statistic、auto-exposure、weak reacquire、shutter search或old/new pooling。

### 7.5 Candidate branch

Candidate 1：

- 4/4 pass：`qualified_1_2500`，candidate 2 launch count必须0；
- 首个bad slot的failure set精确为 `{"clipping"}`：立即停止candidate 1剩余slots；只有Python cleanup、
  shell cleanup、independent final-zero、terminal seal全部pass后，同一outer owner才可自动启动candidate 2；
- low-signal、nonfinite、valid-pixel、metadata、source-isolation、readback、timing、physical-ledger、cleanup、
  owner或任何mixed failure：`run_invalid`，candidate 2保持0。

Candidate 2：

- 4/4 pass：`qualified_1_3200`；
- 任一required quality failure：`exposure_window_unresolved`；
- engineering/metadata/isolation/readback/cleanup/owner/evidence failure：`run_invalid`。

不允许 `1/4000`、`1/5000`、第三档或自动搜索。

### 7.6 All-path cleanup

每个attempted candidate无论正常、quality fail、exception、signal或wrapper failure，都必须：

1. runner Python finally `all_off`；
2. wrapper shell trap `all_off`；
3. outer independent final-zero readback；
4. outer candidate terminal；
5. candidate terminal seal（只有完整evidence才能pass）。

candidate 1 clipping-only到candidate 2之间同样不得省略。

## 8. Sparse liveness and automation handoff

预计运行超过10分钟。Executer launch后只做三次稀疏、只读liveness检查：

```text
check 1: about +60 s
check 2: about +300 s
check 3: about +540 s
```

允许小幅调度偏差，但不得为凑时间增加check。每次只允许：

- 对同一outer PID执行 `kill -0`/`ps`；
- 只读列出 `RUN` 内progressive artifacts；
- 只读检查candidate 1 launch ledger、wrapper/runner PID和exact argv；
- 读取已有JSON/JSONL的末端状态。

禁止额外device/network probe、camera call、Ray/strip readback、public analyzer、向进程发signal或写运行root。

若任一次已terminal，直接进入第10节。若三次后仍运行，Executer在
`.agent-work/EXECUTION_RESULT.md` 追加intermediate handoff：

```text
outer PID
Terminal window/tab identifier
FAMILY / RUN
start timestamp
candidate 1 launch-ledger path/bytes/SHA-256
observed wrapper and runner PIDs
three liveness timestamps/results
estimated completion window:
  one candidate = launch + about 25 min
  two candidates = launch + about 50 min
```

然后停止本轮。Orchestrator按项目规则创建automation，后续只读监控同一PID/root；不得dispatch/retry。
automation若仍运行，只做稀疏重唤醒；terminal时交Executer完成第10节最终只读审计，再交Planner。

## 9. Failure branches and rescue boundary

### 9.1 Before dispatch

offline、configuration、readiness、zero、artifact或root gate任一失败：按5.6 cleanup并停止。dispatch count=0。

### 9.2 Dispatch uncertain or before launch ledger

若Terminal dispatch已attempted但outer/ledger不可确认：

- dispatch count固定1，不得再次dispatch；
- 只读检查唯一Terminal和process ownership；
- 若确认process不存在或terminal incomplete，执行一次外部rescue shell `all_off`，随后一次independent final-zero；
- evidence写入 `PRELAUNCH/rescue/`，不得伪造进 `RUN`；
- stop交Planner。

### 9.3 Runner/wrapper/outer terminal failure

- 若runner/wrapper已写cleanup evidence，先只读验证；
- 若owned process消失且terminal/cleanup不完整，只允许一次外部rescue shell `all_off`和一次independent
  final-zero，写入 `FAMILY/rescue/`；
- 不得kill不属于本package的PID；
- 不得重启outer、candidate、wrapper或单slot capture；
- 若无法取得generation-bearing strip zero或Ray intensity 0 proof，记录hard failure并立即告知Human/Planner，
  不得以command-return代替readback。

### 9.4 Evidence integrity failure

path escape、symlink、missing hash/bytes/remote IDs、PID/argv drift、ledger mutation、counter mismatch、
strict JSON failure、secret presence、cleanup/final-zero failure均为 `run_invalid`/hard failure。不得在原root修补。

## 10. Terminal read-only audit

outer不再运行后，Executer只读审核；禁止public analyzer和任何设备probe。至少验证：

1. 同一outer PID已terminal，owned wrapper/runner残留process=0；
2. `RUN/outer-result.json`与 `RUN/outer-failure.json`恰有一个适用terminal owner；
3. candidate launch count为1或2，candidate 2只满足clipping-only unlock；
4. 每candidate的outer/wrapper/runner PID、exact argv和launch ledger一致；
5. 每candidate存在并通过适用的：
   - `candidate-plan.json`
   - `candidate-result.json`
   - `all-off-python.json`
   - `all-off-shell.json`
   - `wrapper-result.json`
   - `independent-final-zero.json`
   - `terminal-seal.json`
   - `candidate-N-outer-terminal.json`
6. 每张physical return都有CR3与sidecar path、bytes、SHA-256及remote IDs；
7. attempted calls、physical returned、accepted、formal、ambient、retry、candidate launches计数相互一致；
8. 每张accepted frame满足第7.4节exact quality；
9. candidate 1 clipping stop没有额外slot，candidate 2不存在未授权launch；
10. source isolation、chronology、A600/C60/120/300/600语义正确；
11. Python cleanup、shell cleanup、independent final-zero均有双源proof；
12. 所有canonical evidence为regular non-symlink file，resolved within `RUN`；
13. strict JSON parse、path/bytes/SHA-256引用闭合；
14. argv/artifacts/logs不含camera token或private override；
15. `FAMILY`全tree canonical manifest写到 `PRELAUNCH/final-readonly-audit.json`，不得修改 `RUN`；
16. HEAD、source/config/wrapper hashes和production/staged scope仍与第3节一致。

终态只能报告：

```text
qualified_1_2500
qualified_1_3200
exposure_window_unresolved
run_invalid / hard failure
```

Executer不得自行把qualified结果写入successor exposure policy；那是Planner验收后
`REF-P7-24` 的独立package。

## 11. Executer handoff

向 `.agent-work/EXECUTION_RESULT.md` 追加：

- PLAN/FULL/GUIDE/HEAD与所有冻结source hashes；
- Human authorization ID和exact bounds；
- root freshness、resolved paths和prelaunch evidence refs/hashes；
- Terminal dispatch count、command hash、window/tab、outer PID；
- 三次liveness或early-terminal事实；
- outer/candidate terminal classification；
- complete launch/attempt/physical/accepted/formal/ambient/retry counters；
- CR3/sidecar physical ledger与quality summary；
- cleanup/final-zero/terminal-seal refs/hashes；
- residual process count和secret scan；
- final read-only audit path/hash；
- exact Planner decision request。

执行者必须停止；不得修改 `.agent-work/PLAN.md` 或
`.agent-work/FULL_PLAN_REFERENCE.md`。Planner验收后才可决定：

```text
qualified -> REF-P7-24
exposure_window_unresolved -> REF-P7-37 / Advisor
run_invalid ordinary code defect -> possible REF-P7-36 offline-only
other hard failure -> bounded Planner/Human decision
```

## 12. Validation and commit boundary

本package不修改production/test/docs/skill/wrapper，因此不要求重跑C1E1离线测试；prelaunch必须核对其已冻结
证据和source hashes。允许为evidence owner执行strict JSON、hash、manifest、process ownership和
`git diff --check`。不得运行public analyzer。

不授权Git commit。Executer只追加 `EXECUTION_RESULT.md` 及外置evidence；plan/reference ownership不变。

## 13. 维护性判断

本PLAN复用已冻结的single outer owner、candidate wrapper、physical ledger、cleanup与terminal seal边界，
不引入新生产抽象或并行执行路径。运行复杂度由一个outer state owner控制，测试基线为
`49/49`、`161/161`、`622/622`；当前无需架构重构。若真实执行暴露ordinary engineering defect，应另开
最小offline correction并保留本root只读，不能在本package内热修。

---

## 14. Planner review — 2026-07-27

### 14.1 Reviewed inputs

```text
PLAN SHA-256 =
  08a67a07e4df19a5ecb5bd6a909db1ebb95169909968a7c53083cc5a9d550475
EXECUTION_RESULT SHA-256 =
  a0b94720f8d89f245f9ad0ae78968f5c2baa74c46bee828ce01a2088e6a9461f
Orchestrator FULL SHA-256 =
  7bbeeca5a574f42d3fbe145650475b1847fb8045a2a4388e12e29af464de7245
HEAD =
  93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
handoff =
  EXECUTION_RESULT.md §139
```

Orchestrator与Planner确认：

```text
unique FAMILY exists = false
PRELAUNCH exists = false
RUN exists = false
dispatch count = 0
Terminal launch count = 0
real EQ launch count = 0
new device/network readiness probes = 0
Human exact confirmation consumed = false
```

### 14.2 Finding

Production CLI已有 `--eq-r6-orchestrate` 与 `--eq-r6-single-candidate`，但没有本PLAN §5所要求的：

- single prelaunch/readiness owner；
- camera -> Ray -> Python cleanup -> shell cleanup -> independent final-zero 的冻结顺序；
- exact nine-artifact canonical writer；
- all-path failure terminal seal；
- secret-free launch-dispatch handoff。

若Executer在现场拼装heredoc或额外probe，会形成第二套高风险device/evidence state owner，并绕过测试、
atomic writer与failure sealing边界。Executer按要求在任何device/network/.env访问或dispatch前fail closed，
行为正确。

### 14.3 Decision

```text
REF-P7-23 live execution = REJECTED_PRELAUNCH_OWNER_ABSENT
EQ-R6 scientific contract = unchanged
Human exact confirmation = preserved and unconsumed
real root / launch budget = unconsumed
Advisor escalation = not required
next = REF-P7-23-C2 pure-offline prelaunch-owner correction
```

本次不是 `qualified_*`、`exposure_window_unresolved` 或真实measurement `run_invalid`；不得进入
`REF-P7-24`、`REF-P7-36`、`REF-P7-37`，也不得绕过prelaunch直启outer。

### 14.4 Residual risk and exact next branch

C2必须只在现有measurement runner及其focused tests内建立一个production prelaunch owner，以fake adapters
证明readiness、ordered cleanup、final-zero、root ownership、atomic exact-nine evidence、secret absence与
launch handoff。C2真实network、`.env`、device、light、capture、EQ与release调用必须全部为0。C2及其
immutable offline evidence被Planner接受前，REF-P7-23 real route保持锁定。
