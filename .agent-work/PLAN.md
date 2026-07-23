# P7-TD-B-F0B+FORMAL：Lineage Release 后连续完成 Ray/Strip TD-B

**计划状态：** `offline_lineage_fix_then_continuous_td_b_authorized`

**Planner 日期：** `2026-07-23`

**当前阶段：** `P7_TD_B_LINEAGE_RELEASE_AND_FORMAL_EXECUTION`

**当前唯一动作：** Executor 先离线实现、验证并提交 lineage-qualified setup release。只有新 release
可从旧 setup、新 checkpoint和当前 TD-B v2 plan独立重放，且 production preflight全部通过时，才在全新
目录依次完成 Ray formal 16张、Ray public analysis、strip formal 16张、strip public analysis、paired
finalizer和独立最终双零。

**唯一 Planner 停止点：** 整包完成后交回；或者任何离线、lineage、preflight、capture、analysis、ledger、
source isolation、wrapper、cleanup或final-zero hard failure后保存证据、确认双灯关闭并立即停止。禁止自动
重拍、重新setup或进入TD-C。

## 1. 已审归档与决定

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260723-1215-p7-td-b-f0a-review.md` | `4f66e2e5666dcdd8bccaa2568abe886bfdabb181530785909dc809025d95926a` |

冻结决定：

```text
F0A = accepted
old Canon setup = accepted and immutable
lineage candidate = accepted as eligible evidence
candidate production_release_usable = false
fresh setup = not required by current evidence
Ray formal must be a fresh complete 16-capture run
strip formal is conditional on structurally valid Ray
TD-B formal protocol = 16 formal / 0 ambient per source
native RAW policy = unsubtracted_no_ambient
600 s = Developer/Human operational dwell, not settled
```

旧失败Ray capture只作forensic，不计入未来16张，也不得修改旧run。

## 2. 权限与硬边界

项目`AGENTS.md`已规定计划内开关Ray120c和RGBWW灯带不需要单独人工授权。本计划明确允许以下exact
light/camera package，Executor不得再次询问相同授权：

```text
named experiment = p7_td_b_command_switch_history_v1
Ray formal = exactly 16 new CR3
strip formal = exactly 16 new CR3, only after structurally valid Ray
new setup = 0
new formal physical cap = 32 total
source intensity = Ray INT100 or frozen strip raw command
maximum operational dwell per command group = 600 s
```

允许脚本自行加载`.env`并访问remote health/config/v2 capture、Ray和ESPHome。禁止人工读取、打印、source
或持久化secret。

禁止：

- firmware compile/upload、remote deployment、依赖安装或破坏性硬件操作；
- 新setup、额外auto-exposure或旧capture复用；
- ambient capture；
- 修改600秒、recorded-exposure ratio、timing tier、58-feature、uncertainty、covariance或scientific门；
- 覆盖默认LUT/runtime config；
- TD-C、sentinel、remaining 9、boundary、holdout、Gate-6、P8或P6 requalification。

## 3. 冻结输入与旧证据

基础 checkpoint：

```text
setup checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
F0A checkpoint = 8b80c87939ee9aed31ce0dfaa08a5a936bdc56cb
```

冻结实验输入：

| 输入 | SHA-256 |
| --- | --- |
| `config/hsi/p7-operating-envelope-v2.json` | `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16` |
| `config/location/locations-20260714-211759.json` | `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| `config/hsi/strip-hsi-policy-v2-waiting.json` | `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| `config/hsi/ray-hsi-manifold.json` | `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| `config/channel/code-duty-curve.json` | `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |

旧setup目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-setup-20260723-042002
```

| Artifact | SHA-256 |
| --- | --- |
| `setup.json` | `2399b62cc310d525e88dcd1d6be81f08abf3c93daa35d54ca14d7023d9c1cd77` |
| `resolved-formal-plan.json` | `215aa359c162b3d154749753394a96a0adb80559d913a1d84b9063ee70ad92e3` |
| `setup-release.json` | `401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d` |

F0A lineage candidate：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/
  p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json
SHA-256 = 6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1
```

旧setup和candidate均不可直接传给production formal runner。

## 4. F0B Lineage Release 离线实现

### 4.1 新schema与单一owner

在现有`p7_thermal_diagnostics`、formal runner和public analyzer边界实现：

```text
p7_td_b_setup_lineage_release_v2
status = formal_plan_lineage_qualified
production_release_usable = true
```

不得建立平行runner/plan builder/analyzer。新release必须原子生成到：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/<timestamp>/
```

必须绑定并验证：

1. 旧`setup.json`、旧`setup-release.json`和F0A candidate的exact path/hash；
2. old checkpoint、F0A checkpoint和完成F0B后的current full checkpoint；
3. `git diff --name-only old..current`完整changed-path ledger；
4. 所有production diff只能属于F0A/F0B ambient、physical ledger、release validator或其tests/docs/skill；
5. `.agent-work`只能归类为Planner/Executor audit，不得影响production hash；
6. 五个冻结实验输入和remote-controller source hash未变；
7. 旧setup的2张Canon exposure、ratio、timing、cold proxy、cleanup和final-zero完整重放；
8. 从当前代码重新构建一个fresh unresolved Ray TD-B v2 plan，而不是修改旧resolved plan；
9. fresh plan严格为`16 formal / 0 ambient`、`unsubtracted_no_ambient`、当前58-feature和原schedule；
10. 只从旧canonical setup解析D shutter并生成fresh resolved plan；
11. fresh resolved plan的A/D/B/C shutter、schedule、commands、inputs和budget均通过public replay；
12. release绑定current checkpoint，旧release/candidate仍保持不可执行。

任何不确定或prohibited path输出`ineligible`，不得创建production-usable release。

### 4.2 Production trust boundary

`run_resolved_td_b_formal`只允许：

- legacy release在其原checkpoint运行；
- 新lineage release在其exact current checkpoint运行。

必须拒绝：

- 直接传candidate；
- 修改旧release/checkpoint；
- lineage release引用旧resolved plan；
- changed-path ledger缺项/重复/顺序或hash漂移；
- current HEAD、working tree production范围、setup/input hash或release owner漂移；
- release在Ray TD-B以外使用；
- `production_release_usable`缺失或false；
- release输出目录、引用路径或artifact为symlink。

### 4.3 必须覆盖的离线测试

至少覆盖：

1. exact retained setup + F0A candidate + current plan生成lineage release；
2. release public replay和fake production runner完整通过；
3. old resolved plan不能被直接rebind；
4. candidate不能冒充release；
5. prohibited source/control/config/remote path、missing diff、hash drift、checkpoint drift均拒绝；
6. fresh plan policy、ambient cap、formal cap、schedule、shutter、command或input篡改均拒绝；
7. release one-copy、same-content copy、symlink、outside-owner均拒绝；
8. TD-A/TD-C、legacy setup release和F0A forensic replay保持兼容；
9. fake Ray 16张production round-trip重算physical `setup 2 + formal 16 = 18`、accepted formal 16、
   ambient 0；
10. device/network/`.env`/camera/light/`all_off`副作用为0。

### 4.4 离线验证与checkpoint

保存到：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0b-offline/<timestamp>/
```

执行focused、完整suite、compileall、所有wrapper `zsh -n`、`git diff --check`、CodeGraph sync。保存logs、
negative matrix、fake production round-trip、release dry artifact和validation summary。

更新docs/skill并创建focused conventional commit。提交后：

- 取得current full 40-char checkpoint；
- production范围相对HEAD干净；
- 冻结input、remote source、旧setup/release/candidate hash不变；
- 用current checkpoint重新生成最终lineage release；
- public replay和fake production runner再次通过。

任一离线项失败：设备调用0，写`EXECUTION_RESULT.md`后停止。

## 5. 设备前E2门

只有第4节全部通过才可进入设备。E2必须保存到新目录并验证：

- current HEAD等于lineage release checkpoint；
- production范围clean，active PLAN/EXECUTION_RESULT dirty只限审计文件；
- 无无法证明ownership的camera/calibration/thermal/wrapper进程；
- 新Ray/strip run、logs、wrapper-state路径不存在且非symlink；
- `control.all_off`成功；
- strip name/MAC稳定、generation-bearing五通道全零；
- Ray independent readback intensity 0；
- remote health、authenticated config、v2 capability、RAW、ISO100、非空aperture；
- Ray node config、HSI/CCT set/readback可用；
- location和全部冻结hash准确；
- lineage release完整production replay；
- 旧失败run与setup evidence仍原样存在。

E2失败：保存evidence，执行Python/shell cleanup和独立双零后停止。

## 6. Ray TD-B Formal

使用全新run，production wrapper和lineage release。不得auto-expose或ambient：

```text
A = H120/S100/INT100, shutter 1/5000
D = H120/S50/INT100, shutter from retained canonical setup
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

要求：

- 每group命令一次并精确readback；transition先双关灯/读回；
- Ray亮时strip持续verified zero；
- 每张remote-v2、Canon:ExposureTime/recorded、ratio `0.8..1.2`、Tier A/B；
- CR3/sidecar非空，ID/hash/bytes可重放，`.npy=0`；
- `physical-returns.jsonl=16`，`captures.jsonl=16`，ambient=0；
- run cumulative physical=`setup 2 + formal 16 = 18`，不超过Ray cap24；
- Python/shell cleanup和独立双零通过。

启动后约3分钟只做一次健康检查，之后按完整schedule ETA使用当前thread单次heartbeat，不短间隔轮询。

若capture已返回后report/feature/timing失败，physical ledger必须保留；该run hard-invalid，停止且不启动strip。
若结构合法，即使analysis显示history dependence或nonstationarity warning，也执行Ray public analyzer并继续strip。

## 7. Strip TD-B Formal

仅在Ray acquisition、wrapper、cleanup、public analyzer结构全部合法时启动。使用current fresh strip plan，
不使用setup release、不auto-expose、不拍ambient：

```text
A: cw=518,  ww=0,    r=0,    g=4095, b=0;    shutter=1/320
D: cw=4095, ww=0,    r=0,    g=3118, b=13;   shutter=1/400
B: cw=4095, ww=4095, r=0,    g=1887, b=1535; shutter=1/500
C: cw=406,  ww=0,    r=4095, g=0,    b=1541; shutter=1/125
```

Chronology同Ray，恰好16张。Strip亮时Ray intensity始终独立读回0。要求
`physical-returns=16 / accepted formal=16 / ambient=0 / NPY=0`，并通过同样Canon、timing、owner、
wrapper、cleanup和独立双零门。

Strip hard-invalid时保存Ray合法analysis，但不生成paired scientific claim。

## 8. Analysis、Finalizer 与交接

两个source各自完成后运行public analyzer；它必须从plan、physical returns、accepted captures、
patch reports、covariates、commands、isolation、wrapper和cleanup独立重算，不信任自报counter。

两个source都结构合法时，paired finalizer原子生成：

```text
input-manifest.json
td-b-combined-analysis.json
EXPERIMENT_SUMMARY.md
independent-final-zero.json
```

Finalizer只能汇总，不重新拟合、不改变单源状态、不生成新operating envelope。600秒只可称
`operational_dwell_600`，不得称steady或settled。

Executor只更新`.agent-work/EXECUTION_RESULT.md`，不得修改本PLAN。交接包含commit、release/hash、
run/PID/TTY/logs、capture/ledger counts、analysis状态、wrapper exit、cleanup、final zero、artifact hash和
维护性判断。

完成后停止在Planner门。即使TD-B结构和科学分析均通过，也不自动解锁TD-C或后续阶段。
