# P7-TD-B-CANON-R2：Canon-only setup 重试并连续完成 Ray/Strip TD-B

**计划状态：** `one_additional_setup_then_continuous_td_b_authorized`

**Planner 日期：** `2026-07-22T21:51:53-0600`

**当前阶段：** `P7_TD_B_CANON_RECORDED_EXPOSURE_RECOVERY`

**当前唯一动作：** Executor 以 Git checkpoint `9c804abdeabbc5da18a66d0acf25a1f13128bc2d` 完成
checkpoint/remote/双灯 preflight，然后在全新目录执行一次额外的 Ray H120/S50 setup。只有每张新图均由
`Canon:ExposureTime` 提供可信 recorded exposure、canonical setup/release完整且双层 cleanup通过时，才在
同一连续工作包中完成 Ray TD-B、Ray public analysis、strip TD-B、strip public analysis、paired finalizer
和独立最终双零。

**唯一 Planner 停止点：** 整个 Ray/strip TD-B包完成；或者任一 preflight、setup、timing、provenance、
source isolation、budget、formal、analysis、wrapper、cleanup或final-zero hard failure后保存证据并停止。不得
进入 TD-C 或任何后续阶段。

## 1. 上轮验收与归档

已完成和已审内容全部归档：

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260722-2151-p7-td-b-setup-exposure-source-failure-review.md` | `d9a3fa75ea44c971b037d1e5813d3631c512e1b3268ae66f92a50b53edd2bf61` |

冻结验收决定：

```text
PATH-R1 = accepted
old setup = valid failed-closed evidence
old setup reuse/rewrite = prohibited
finalizer 0.8..1.2 ratio gate = unchanged
root cause = old remote bridge recorded-exposure extraction bug
Canon-only remote correction = accepted
Advisor escalation = not required
one additional setup = explicitly authorized
successful setup = continue Ray -> strip without ordinary Planner stop
```

旧失败 run必须原样保留：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-173504
```

它的两张 CR3和sidecar只作为失败/root-cause证据；不得修 sidecar、重新 finalizer、拼入新 setup或formal。

## 2. Human 授权与禁止项

Human 本轮明确要求“完成plan修改，放行executer继续”。本计划把该授权严格限定为：

```text
named experiment = p7_td_b_command_switch_history_v1
new setup count = exactly one additional bounded run
setup physical cap = 8 CR3
Ray formal = exactly 16 CR3, conditional on valid setup
strip formal = exactly 16 CR3, conditional on structurally valid Ray run
combined new-run physical range = 33..40 CR3
```

项目 `AGENTS.md` 也明确计划内开关两灯不需要重复人工批准。Executor可直接消费本计划，不得再次询问相同
设备权限。脚本可自行读取 `.env`；禁止人工读取、打印、source或持久化 secret。

禁止 firmware compile/upload、remote redeploy、依赖安装、破坏性硬件动作、手工额外 capture和本计划外
灯光命令。远程 bridge 已部署，本包只验证并使用，不再修改或部署。

## 3. 冻结 checkpoint、输入和远程能力

### 3.1 Git 与源码

整个 setup -> Ray -> strip连续包都必须保持：

```text
HEAD = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
```

冻结 remote controller源码：

| 文件 | SHA-256 |
| --- | --- |
| `remote_camera_controller/r6_camera_bridge.py` | `bf9bbfd162a2b12ebd065c4c7ba977fe00637ff59757b544c49c92eea6474d18` |
| `remote_camera_controller/r6_timing.py` | `e847f80962a93354cd50824dffae5460cc1c2fb6de4acd5dc09d0a4ca38014f0` |
| `remote_camera_controller/deploy/r6-camera-bridge.service` | `913145b0130ef1a07a4d4bfeefe09feb621d123725320f15a2d35b96228dcc45` |
| `remote_camera_controller/deploy/exiftool-wrapper` | `0668b821a966f429455cd741acfeec0a9e72f7c7fdc1d8fd47f45b95497ffb00` |

`r6_camera_bridge.py` 只能调用 ExifTool `-Canon:ExposureTime`；`r6_timing.py` 只能接受
`Canon:ExposureTime`。缺字段、ExifTool失败、非有限值或错误source必须为 unavailable/fail closed。

Planner-owned `PLAN.md`、archives和Executor-owned `EXECUTION_RESULT.md`可保持dirty；以下生产范围相对
HEAD必须干净：

```text
src/
tests/
docs/
.agents/skills/
tmp/run-p7-thermal-diagnostics.zsh
remote_camera_controller/
config/
```

从 preflight到paired finalizer之间不得commit、checkout或改变HEAD。若HEAD或生产范围变化，停止且不访问设备。

### 3.2 冻结实验输入

| 输入 | SHA-256 |
| --- | --- |
| `config/hsi/p7-operating-envelope-v2.json` | `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16` |
| `config/location/locations-20260714-211759.json` | `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| `config/hsi/strip-hsi-policy-v2-waiting.json` | `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| `config/hsi/ray-hsi-manifold.json` | `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| `config/channel/code-duty-curve.json` | `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |

受信 prerequisite仍必须 canonicalize为：

```text
/Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-operating-envelope-v2.json
sha256 = 7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
```

### 3.3 Remote 修复证据的用途

Human提供的 remote-development handoff已证明：

```text
remote ExifTool = 13.50
service = active/running
remote offline suite = 15/15 pass
requested test shutter = 1/6400
Canon recorded exposure = 0.000153798956285995 s ~= 1/6501.995
recorded/nominal ratio = 0.984313
source/status = Canon:ExposureTime / recorded
timing = Tier B weak_estimate
```

该单张图只是非正式 capability probe，不计入 setup或formal，不得复用。Remote API没有暴露deployed source
hash，因此最终信任必须由本地frozen source加上**每张新 capture的运行时sidecar门**共同建立。

## 4. 进入设备前的 E1 门

Executor先读取本文件、上述归档第8节、`EXECUTION_RESULT.md` 第26节、项目skill和P7 docs，然后执行：

1. 确认HEAD、生产范围clean和六个冻结文件hash；
2. 确认旧失败 run、CR3、sidecar、failure和cleanup evidence仍存在且hash不变；
3. 确认没有无法证明ownership的camera/calibration/thermal/wrapper进程；
4. 运行focused P7 thermal/analyzer/remote-client测试；不得为本地缺失Flask联网安装依赖；
5. `compileall`、所有 `tmp/*.zsh` 的 `zsh -n`、`git diff --check`；代码未变化时不要求新commit；
6. 保存E1 preflight artifact和所有hash到全新目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-canon-r2-preflight/<timestamp>/
```

任何离线E1失败：写 `EXECUTION_RESULT.md` 并停止，设备调用为0。

E1通过后，脚本自行加载 `.env`，按顺序验证：

- `control.all_off`成功，Ray independent readback intensity 0；
- strip `bedroom-rgbww-strip` name/MAC稳定、generation-bearing五通道全零；
- remote `/health`、authenticated config、v2 capability、RAW、ISO 100、非空 aperture；
- Ray node config、HSI/CCT set/readback可用；
- location仍为最新冻结文件；
- 新setup run、logs、wrapper-state路径均不存在且不经symlink。

设备preflight失败：Python/shell cleanup、独立双零、保留evidence后停止，不重试setup。

## 5. 唯一额外 setup

### 5.1 Owner、目录和命令

必须使用全新run identity，例如：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-canon-r2-setup-<timestamp>
```

只通过 production outer orchestrator与 `tmp/run-p7-thermal-diagnostics.zsh`启动，传入：

```text
code checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
prerequisite = config/hsi/p7-operating-envelope-v2.json
Ray = H120/S50/INT100
strip = all five channels zero
historical seed = 1/6400, seed_only
target_max = 19661
accepted_min ratio = existing auto-exposure 0.85
min shutter = 1/16000
max shutter = 25
physical cap = 8 CR3
adapter = retained remote-v2 only
```

旧run、remote capability probe或旧CR3均不得作为attempt 1。

### 5.2 每张 capture 的强制 Canon 门

每个trial、rejected-final和selected-final必须同时满足：

```text
recorded_exposure.status = recorded
recorded_exposure.source = Canon:ExposureTime
recorded_exposure.seconds = finite and > 0
0.8 <= recorded_seconds / requested_nominal_seconds <= 1.2
timing tier = tier_a or tier_b
timing method = recognized gphoto2 estimate
absolute_exposure_start = false
CR3 nonempty + exact SHA-256/byte count/capture ID/request ID association
sidecar nonempty + exact owner/hash
NPY = 0
```

即使当前通用remote-v2 parser为兼容旧artifact仍识别 `EXIF:ExposureTime`，本次P7-R2人工/程序交接门也只
接受 `Canon:ExposureTime`。出现 `EXIF:ExposureTime`、unknown、unavailable、错误ratio或Tier C时，必须在
formal前fail closed；不得因为数值恰好接近而放行。

第9张请求必须在相机调用前拒绝。所有setup CR3/sidecar保留，但全部排除formal 58-feature、repeatability、
history aggregate和covariance。

### 5.3 Finalization与1800秒 cold proxy

Setup capture结束立即双关灯并独立zero readback，然后完成独立monotonic 1800秒off wait。Wait不可与Ray
formal A0的600秒合并。

必须从retained evidence重建并验证：

```text
setup-provisional.json
setup-attempts.json
wrapper-result.json
wrapper-observed-exit.json
all-off-python.json
all-off-shell.json
independent-final-zero.json
setup.json
resolved-formal-plan.json
setup-release.json
```

只有child/shell/wrapper exit均0、双cleanup、final zero、Canon source、ratio、owner/hash、physical ledger和
cold proxy全部通过，canonical setup/release才合法。

这是本计划最后一次setup权限。任何setup/preflight/finalization失败后不得第三次setup，即使0 capture；执行
cleanup/recovery、删除heartbeat并交Planner。

## 6. Setup通过后的连续formal包

### 6.1 总顺序与预算

Setup合法后不等待普通Planner验收，继续：

```text
Ray TD-B formal 16
-> Ray public analysis
-> strip TD-B formal 16
-> strip public analysis
-> paired finalizer
-> independent final both-zero
-> Planner stop
```

| Package | Formal | Setup | Ambient | New physical |
| --- | ---: | ---: | ---: | ---: |
| Ray | 16 | 1..8 | 0 | 17..24 |
| strip | 16 | 0 | 0 | 16 |
| combined | 32 | 1..8 | 0 | 33..40 |

每张formal CR3也必须为remote-v2、`Canon:ExposureTime/recorded`、requested/recorded ratio `0.8..1.2`、
Tier A/B、nonempty、ID/hash/byte-count可重放且无NPY。任一失败为hard-invalid。

### 6.2 Ray schedule

```text
A = H120/S100/INT100, shutter 1/5000
D = H120/S50/INT100, shutter only from new canonical setup
B = H0/S0/INT100, shutter 1/8000
C = H300/S100/INT100, shutter 1/2000
```

恰好16张：

```text
A0 at 600
D at 60/120/300/600
A return at 600
B at 60/120/300/600
A return at 600
C at 60/120/300/600
A return at 600
```

每个group只设命令一次并精确readback；transition先双关灯/读回再开新状态。Ray亮时strip始终verified zero。
Formal不得auto-expose。

Ray acquisition只要结构、capture、timing、owner、source isolation、ledger和cleanup合法，就执行public
analysis；即使科学状态为history-dependent/nonstationarity warning也继续strip。Hard-invalid、measurement
failure或cleanup uncertainty则停止。

### 6.3 Strip schedule

```text
A: cw=518,  ww=0,    r=0,    g=4095, b=0;    shutter=1/320
D: cw=4095, ww=0,    r=0,    g=3118, b=13;   shutter=1/400
B: cw=4095, ww=4095, r=0,    g=1887, b=1535; shutter=1/500
C: cw=406,  ww=0,    r=4095, g=0,    b=1541; shutter=1/125
```

Chronology与Ray完全相同，恰好16张。Strip亮时Ray intensity始终独立读回0；每个transition保存generation、
identity、requested raw command和readback。Formal不得auto-expose。

## 7. Timing、长任务和cleanup

- 600秒来自Developer/Human operational dwell上限，不是steady-state；所有settle字段保持null；
- nominal `60/120/300/600`只用于调度，分析使用Tier A/B finite/nonnegative observed elapsed；
- 不使用proximity gate，不声称absolute exposure-start；
- 每run只解析一次camera settings并注入全部capture；
- 每个command group内chronology严格递增；
- 每个setup/formal run都有独立PID/PPID/PGID/TTY、logs、wrapper-state和exit evidence；
- 启动后只做一次约3分钟健康检查，然后用当前task的稀疏一次性heartbeat按ETA恢复，不短轮询；
- Python `finally`和shell EXIT/INT/TERM/HUP trap均无条件关两灯；每个run后再独立确认strip全零与Ray 0；
- 缺任一cleanup证据立即执行recovery并停止；结束回答不得杀后台任务。

## 8. 最终交接与硬锁

两个source都结构合法时，paired finalizer只能汇总public analyses、input/setup/physical ledger、wrapper/cleanup
和final zero，原子生成：

```text
input-manifest.json
td-b-combined-analysis.json
EXPERIMENT_SUMMARY.md
independent-final-zero.json
```

不得重新拟合、改变单源状态、生成新operating envelope或自动解锁后续阶段。

Executor只向 `.agent-work/EXECUTION_RESULT.md` 写入E1、setup、Ray、strip、paired目录和hash，remote source、
recorded exposure source/ratio、PID/exit、capture counts、analysis status和cleanup结果；不得修改本PLAN。

硬锁：

- 不允许第三次setup或任何formal重跑；
- 不允许900/1200秒扩展或把600秒称为settled；
- 不允许修改ratio门、timing tier、uncertainty、covariance、feature或threshold来通过；
- 不允许TD-C、sentinel、remaining、boundary、holdout、Gate-6、P8；
- 不允许P6 requalification、firmware、remote redeploy或默认LUT/runtime安装；
- 不允许把setup/history failure升级为physical gamut/physically unreachable；
- 不允许覆盖或删除任何旧失败run/evidence。

完成本PLAN不自动授权下一阶段。Planner复验时必须先归档本文件，再写唯一下一工作包。

---

## 9. Planner 验收附录（2026-07-23T07:05:07-0600）

### 9.1 已审范围与证据质量

本归档保留的 active PLAN 原始 SHA-256：

```text
855a019520462c3b6900c06ce126d4a53171142ab10f71a5e5e9562557b5778f
```

Planner 复核了 `.agent-work/EXECUTION_RESULT.md` 第 27 节、setup canonical/release/public replay、
Ray formal run、首张 retained CR3/sidecar、failure/run、Python/shell cleanup、独立 recovery 和残留进程。
关键 evidence hash 与交接一致：

```text
setup.json                         2399b62cc310d525e88dcd1d6be81f08abf3c93daa35d54ca14d7023d9c1cd77
resolved-formal-plan.json          215aa359c162b3d154749753394a96a0adb80559d913a1d84b9063ee70ad92e3
setup-release.json                 401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d
setup-public-replay.json           625ec24bc8c4c879c06f859b31185bb73f70cbf0fc0aa9fb61965e3824004ca7
Ray failure.json                   c9933f6513ef260db920eea99ac85099e93b6c4ff9df71502027ede1a71a3303
Ray run.json                       7e370a675160f70078a00a0962ea878e5ede6466b666331269963c052a17fc2b
Ray first CR3                     2cf5d680d694eb9c0d2e36bf8144dcf2f1fe02cd902bc4c202cf92ce1a699608
Ray first sidecar                 9952bf79094d7d93b21a9864e841359d0195c423c3dc8464e0250231bc1721ee
all-off-python.json               ef631348a4181ec92a793a7ff4e9eaee67bf4b76c97e28067ed5ea20657e3965
all-off-shell.json                ff1951142132b7cb9d2a5203a7b565f081737138186ff296180ea57d3182c55e
wrapper-result.json               da9a976c4e3bebc19d979c4f4e29bc296ef150d42e468c5e78b9f38740154c3f
independent-recovery-zero.json     759a9a2768b72b9a559b764f9077caa647b81c0ec904b9e0b8834c09e6b870c0
ray-hard-invalid-summary.json      e4a0eeafbadebd4fc8307b2739c72dfa454c154115655cdeeb586467c02daa6e
```

当前无残留 P7 thermal/wrapper 进程。Ray run 中恰有一张非空 CR3、零 `.npy`、无
`captures.jsonl`；这与“相机副作用成功，但 measurement/report 尚未被接受”的失败位置一致。

### 9.2 Setup 验收

新的 Canon-only setup 通过且应作为有效 setup evidence 保留：

```text
setup physical CR3 = 2
recorded source = Canon:ExposureTime, 2/2
recorded/requested ratio = 0.9843133202303679, 2/2
timing = Tier B recognized gphoto2 method, 2/2
cold proxy = 1800.0010467909742 s
child/shell/wrapper exit = 0/0/0
Python/shell/final-zero = pass
canonical setup/release/public replay = pass
```

Setup 数据本身无需重拍或重新拟合。原 release 与 checkpoint
`9c804abdeabbc5da18a66d0acf25a1f13128bc2d` 绑定；后续代码修复后不能直接把旧 release 交给 production
runner。是否可建立严格、只读、可重放的 checkpoint lineage requalification，必须先在离线包中证明并由
Planner 再验收；不得覆盖原 setup/release。

### 9.3 Ray formal 验收与根因

Ray formal 是有效的 hard-invalid 运行，不是相机、曝光、source isolation 或 cleanup 损坏：

```text
first planned step = Ray A / H120/S100/INT100 / nominal t600
remote capture = success
recorded source/status = Canon:ExposureTime / recorded
recorded/requested ratio = 0.968872712382935
best-effort observed elapsed = 604.7503857329721 s
report failure = non-ambient capture requires the preceding ambient capture
completed formal = 0
ambient = 0
strip = not started
automatic retry = false
cleanup/recovery = pass
```

冻结的 TD-B 协议是每个 source `16 formal / 0 ambient`。因此不增加 ambient，也不改变 formal/physical
预算。根因是通用 `build_native_raw_capture_step_fn` 默认把所有 non-ambient capture 都送入需要“最近
ambient”的报告路径，TD-B runner没有提供显式 experiment-aware ambient policy。

第二个根因是 physical owner 过晚：CR3/sidecar 已由 remote backend 原子落盘，但
`_write_native_capture_report` 先抛错，`raw_capture()` 未返回，外层 `execute_plan.retain_capture()` 无法
观察该物理副作用。正确账本应为：

```text
setup physical = 2
Ray formal returned physical = 1
actual cumulative physical = 3
accepted formal = 0
accepted ambient = 0
```

旧 `run.json physical_cr3_count=2` 是已保留的 legacy undercount evidence；不得原地修改。修复后必须在
CR3 成功返回并成为当前 run 的 retained owner时先落 physical ledger，再执行 sidecar、recorded exposure、
RAW report、feature、timing和covariate验收。

### 9.4 Planner 决定

```text
Canon-only setup = accepted, preserve unchanged
Ray formal run = accepted as hard-invalid evidence
TD-B ambient policy = forbidden; un-subtracted native RAW analysis
TD-B formal/ambient budget = retain 16/0 per source
old Ray CR3 = forensic regression input only, never a successful formal observation
physical total for failed package = 3
strip formal = remains unconsumed and locked
automatic Ray retry = prohibited
old setup release direct reuse after code change = prohibited
Advisor escalation = not required for this implementation defect
next work = pure offline P7-TD-B-F0A correction and release-lineage qualification
```

本次原实机授权已经在 hard failure 分支结束。F0A 不包含任何设备权限；即使离线测试通过，也不得自动
重跑 Ray、启动 strip、重新 setup或调用 `all_off`。

### 9.5 残余风险与唯一下一分支

- 通用 native RAW capture owner 被 P1、TD-A/TD-C 和 TD-B 共享；不能把 ambient 全局改成 optional。
- Physical 账本必须从实际 capture-return side effect建立，不能依赖报告成功、事后目录扫描或
  `captures.jsonl` 成功行推断。
- Setup release checkpoint lineage 若不能证明代码变化只影响 formal report/ledger，必须 fail closed并由
  Planner决定是否需要 fresh setup。
- 旧 Ray CR3 的离线成功分析只能证明修复路径可处理该 RAW，不能恢复原 chronology、改写旧 run或减少未来
  formal预算。

唯一下一分支：

```text
P7-TD-B-F0A
  -> freeze experiment-aware ambient policy
  -> split physical-return ledger from accepted-measurement ledger
  -> replay exact failed first-capture boundary
  -> build waiting-for-Planner setup-release lineage candidate or fail closed
  -> focused/full validation and focused commit
  -> Planner stop with zero device access
```
