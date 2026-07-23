# P7-TD-B-F0A：Ambient 策略与物理返回账本离线纠偏

**计划状态：** `offline_correction_authorized`

**Planner 日期：** `2026-07-23`

**当前阶段：** `P7_TD_B_FORMAL_CAPTURE_CONTRACT_CORRECTION`

**当前唯一动作：** Executor 只在离线环境中修复 TD-B formal capture 的 experiment-aware ambient
策略、physical-return ledger 和 setup-release checkpoint lineage，并完成 retained first-capture replay、
全套回归、文档和 focused commit。

**唯一 Planner 停止点：** 上述离线包全部完成并提交后交回 Planner；或者任何合同、重放、测试、证据或
checkpoint 门失败后保留证据并停止。本计划不授权设备、网络、`.env`、相机、灯光、`all_off` 或新 CR3。

## 1. 已审归档

已完成、失败和已审内容均已归档，不得在 active PLAN 中重新展开：

| 归档 | SHA-256 |
| --- | --- |
| `.agent-work/PLANS/20260723-0705-p7-td-b-ray-ambient-ledger-failure-review.md` | `64fbec36c286aafd1fb79f63a3620501fbe52b1649b80a67a3207b987f459bb9` |

Planner 决定：

```text
Canon-only setup = accepted and immutable
Ray formal run = valid hard-invalid evidence
TD-B formal protocol = 16 formal / 0 ambient per source
TD-B native RAW policy = un-subtracted, ambient is forbidden
old first Ray CR3 = forensic replay input only
actual failed-package physical count = setup 2 + Ray returned 1 = 3
accepted formal count = 0
old run.json undercount = retained legacy evidence; do not rewrite
old setup release direct reuse after code change = prohibited
Advisor escalation = not required for this implementation defect
```

旧 setup、Ray run、CR3、sidecar、failure、cleanup 和 recovery evidence 必须原样保留。不得把旧 Ray
capture 改写为成功 formal observation，也不得把它计入未来正式 16 张预算。

## 2. 权限与硬边界

本包是纯离线代码纠偏。允许：

- 修改现有 P7 thermal plan/runner/analyzer 和共享 native RAW capture owner；
- 修改相应测试、`docs/README.md` 和项目 skill；
- 读取 retained JSON/CR3/sidecar 进行离线 replay；
- 在 `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/<timestamp>/` 写证据；
- 创建一个 focused conventional commit。

禁止：

- 读取或加载 `.env`；
- 构造真实 remote backend，访问网络或设备；
- 调用相机、Ray120c、ESPHome 或 `all_off`；
- 创建任何新真实 CR3；
- 修改 firmware、remote controller、冻结实验输入、ratio/timing/feature/uncertainty 阈值；
- 重新 finalizer、覆盖或修补旧 setup/release/run；
- 重跑 Ray formal、启动 strip、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6 或 P8。

## 3. 必读输入与冻结证据

Executor 开始前读取：

1. 本文件；
2. 上述归档第 9 节；
3. `.agent-work/EXECUTION_RESULT.md` 第 27 节；
4. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
5. `docs/README.md` 的 P7 thermal/setup/capture ledger 章节；
6. CodeGraph 中 production capture -> native report -> retained ledger 调用路径。

冻结 checkpoint 与 evidence：

```text
base checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
setup run =
  /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-setup-20260723-042002
Ray failed run =
  /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-ray-20260723-045514
Ray first CR3 SHA-256 =
  2cf5d680d694eb9c0d2e36bf8144dcf2f1fe02cd902bc4c202cf92ce1a699608
Ray first sidecar SHA-256 =
  9952bf79094d7d93b21a9864e841359d0195c423c3dc8464e0250231bc1721ee
```

五个实验输入 hash、Canon-only remote source hash及旧 evidence hash必须保持归档所列值。

## 4. F0A 实现合同

### 4.1 Experiment-aware ambient policy

在现有 shared native RAW capture owner中增加显式、窄范围的 ambient policy，不建立平行 capture
framework：

```text
require_preceding_ambient
unsubtracted_no_ambient
```

要求：

1. 默认值必须保持 `require_preceding_ambient`，确保 P1、TD-A、TD-C和历史调用不发生静默改变；
2. 只有冻结的 TD-B v2 formal phase可选择 `unsubtracted_no_ambient`；
3. TD-B plan、runner和public analyzer必须共同冻结、持久化并重放该 policy；
4. `unsubtracted_no_ambient` 路径不得寻找、伪造或减去 ambient RAW；
5. TD-B若出现 ambient step或ambient owner，必须 fail closed；
6. 非 TD-B caller尝试选择该 policy必须 fail closed；
7. policy缺失、未知、plan/run/report不一致必须在正式 accepted observation前拒绝；
8. legacy v1 replay保持原有语义，不回写新 claim。

### 4.2 Physical-return ledger 与 accepted-measurement ledger

把物理副作用与正式测量接受拆成两个明确账本：

```text
physical_returned_cr3_count
accepted_formal_count
accepted_ambient_count
```

要求：

1. remote backend返回且当前 run拥有唯一、非空 CR3后，立即原子记录 physical-return evidence；
2. 此记录必须先于 sidecar association、recorded exposure、RAW report、feature、timing、covariate和
   `captures.jsonl` accepted row；
3. sidecar/report/feature/timing后续失败时，保留 CR3 path、size、SHA-256、capture/request ID（若已获得）、
   failure stage和physical count；
4. physical cap按已返回 CR3执行；不得因为 report失败而允许多拍；
5. accepted formal/ambient只在完整验收后增加；
6. 失败写 `run.json`/`failure.json` 时必须由 retained physical ledger重建当前 run的真实计数；
7. 不得通过事后扫描任意目录或成功 `captures.jsonl` 行推断 physical count；
8. setup ledger和formal ledger的 owner保持分离；lineage汇总可验证 cumulative `setup 2 + formal N`，
   但不能让 setup图进入formal aggregate。

### 4.3 Retained first-capture forensic replay

使用旧 Ray 首张 CR3/sidecar做纯离线 replay：

- hash、byte count、capture/request ID、Canon recorded exposure、Tier B timing和location/input owner必须匹配；
- 使用 TD-B `unsubtracted_no_ambient` 路径成功生成 native RAW report和冻结58-feature；
- replay结果必须明确 `forensic_only=true`、`accepted_formal=false`、`reusable_capture=false`；
- 不修改旧run，不生成旧run的`captures.jsonl`，不把结果用于科学aggregate；
- 篡改 CR3、sidecar、policy、source、state、command、shutter、input hash或owner时fail closed。

### 4.4 Setup-release checkpoint lineage candidate

实现只读、可审计的 lineage qualification candidate，不覆盖旧release：

1. 输入旧 canonical setup/release、旧 checkpoint和新 F0A checkpoint；
2. 验证旧 setup全部 retained evidence、hash、Canon exposure、ratio、timing、cleanup和cold proxy；
3. 验证代码变化范围只包含 F0A允许的 formal report/ledger/tests/docs/skill owner；
4. 验证 setup producer、auto-exposure选择、remote parser、Canon recorded exposure、camera settings、
   setup预算和setup finalizer语义未改变；
5. 输出新的独立 `setup-release-lineage-candidate.json`，状态只能是：

```text
eligible_waiting_for_planner
ineligible
```

6. candidate不得被production runner直接当成release使用，不得自动解锁实机；
7. 无法证明精确变化范围或任一旧证据漂移时输出`ineligible`并交Planner，不得要求自动fresh setup。

## 5. 回归与对抗性测试

至少覆盖：

1. TD-B v2 `16 formal / 0 ambient` 生产fake round-trip可使用un-subtracted report；
2. 默认caller仍要求preceding ambient；
3. TD-A/TD-C ambient ledger和subtraction保持不变；
4. TD-B出现ambient、unknown policy、policy drift或非TD-B选择no-ambient均拒绝；
5. CR3成功返回后在sidecar、recorded exposure、report、feature、timing、covariate各阶段注入失败，physical
   count均准确且accepted count不增加；
6. 空/重复/跨run CR3、hash/size/ID冲突不增加合法physical ledger；
7. physical cap one-under/at-limit/one-over在camera request前正确拒绝；
8. exact旧首张capture forensic replay成功且不产生accepted observation；
9. forensic篡改矩阵全部fail closed；
10. setup 2 + formal returned 1 / accepted 0 的 synthetic regression重现正确；
11. lineage candidate对允许diff为eligible，对setup/remote/parser/config/budget变化为ineligible；
12. public analyzer从retained ledger独立重算，不信任自报counter；
13. fake wrapper success/failure/signal仍保存双cleanup和真实exit；
14. 所有负例的device/network/`.env`/`all_off`调用均为0。

测试不能只调用helper；至少一组必须走：

```text
production plan
-> fake backend physical return
-> native RAW report
-> runner persistence
-> public analyzer replay
```

## 6. 离线验证与证据

证据根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/<timestamp>/
```

至少保存：

- `focused.log`
- `full-suite.log`
- `compileall.log`
- `wrapper-syntax.log`
- `negative-case-matrix.json`
- `retained-first-capture-replay.json`
- `physical-ledger-roundtrip.json`
- `setup-release-lineage-candidate.json`
- `validation-summary.json`
- 每个artifact的SHA-256

执行：

```zsh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest \
  tests.test_p7_thermal_diagnostics \
  tests.test_analyze_p7_thermal_diagnostics \
  tests.test_measure_raw_observer_validation \
  tests.test_camera_remote -v

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q src tests
for wrapper in tmp/*.zsh; do zsh -n "$wrapper"; done
git diff --check
codegraph sync
```

更新`docs/README.md`和项目skill，写明TD-B无ambient subtraction、physical-return早于measurement
acceptance、旧capture仅forensic以及lineage candidate不等于设备授权。

完成后创建一个focused conventional commit。提交后复核：

- 新full checkpoint为40字符；
- production范围相对新HEAD干净；
- 五个冻结实验输入和remote-controller文件hash不变；
- retained旧evidence hash不变；
- offline artifact可从新checkpoint重放；
- device/network/`.env`/camera/Ray/ESPHome/`all_off`/new CR3均为0。

## 7. 交接与后续硬锁

Executor只更新`.agent-work/EXECUTION_RESULT.md`，不得修改本文件。交接必须包含：

- implementation commit；
-变更owner和关键合同；
- focused/full/check结果；
- evidence路径与hash；
- forensic replay结论；
- physical/accepted ledger结论；
- lineage candidate状态和原因；
-零设备副作用声明；
-维护性判断。

F0A即使全部通过也不自动授权设备。Planner必须先验收并归档本计划，再决定：

```text
lineage eligible -> 是否放行全新Ray TD-B formal 16，再按结构结果决定strip
lineage ineligible -> 是否需要fresh bounded setup
```

在新active PLAN前，Ray重跑、strip、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6、P8、
P6 requalification、firmware、remote deployment和默认LUT/runtime安装全部锁定。
