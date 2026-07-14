# Ray120c 相机观察者匹配后续实施计划

**计划状态：** 活动计划，等待用户批准后执行
**编写日期：** 2026-07-13
**当前提交：** `4f6df67 feat(camera): support pluggable auto-exposure meters`
**上游设计：** `advisor/1/1.RESEARCH.md`、`advisor/1/1.PLAN.md`
**当前阶段：** P0，先补齐测量验证分析和安全运行器，不立即扫描设备
**计划使用对象：** 能完成明确编码和实验步骤，但不应自行发明阈值、跨越实验门或扩大范围的执行模型

---

## 0. 计划目标

本计划把后续工作拆成两条按顺序推进、彼此独立验收的产品线：

1. **CCT/GM 相机观察者匹配**
   - 输入为 `1800..20000 K`、Ray raw GM `0..200`。
   - 输出为 RGBWW 五通道 `0..4095` 线性目标代码。
   - 先保证中性白点不退化，再优化彩色色块和留出目标。
   - 最终候选必须完成 70/70 节点和非节点插值点的独立热态验证。

2. **Ray HSI 相机观察者匹配**
   - 输入为 `Hue 0..360`、`Sat 0..100`、`Intensity 0..100`。
   - 先实测 Ray 目标流形，再优化灯带。
   - 对不可达颜色显式返回 gamut 状态，不伪装成精确复制。
   - Hue 必须周期连续，SAT 和 INT 的数值响应必须由实测决定。

本项目只能声称固定 Canon R6 Mark III、固定镜头、固定 RAW 链、固定色卡和固定几何下的相机观察者匹配。不得声称光谱、CRI、TLCI、SSI、TM-30、人眼、其他相机或绝对照度一致。

---

## 1. 当前事实和不可回退的基线

执行模型开始任何工作前，必须确认以下事实仍成立；若路径或提交发生变化，先更新本节，不得静默替换：

- 当前代码提交为 `c68ac87`。
- 原生 Bayer 测量器已经存在：
  - `src/camera_based_rgbww_optimizer/measurement/raw_mosaic_patches.py`
  - CLI：`python -m camera_based_rgbww_optimizer.measurement.raw_mosaic_patches`
  - 直接读取 `raw_image_visible`，不做 demosaic、白平衡或 gamma。
  - 输出 `R/G1/G2/B`，可选 `G=(G1+G2)/2`。
  - 支持曝光归一化、ambient/dark 扣除、裁剪/噪声诊断和 JSON-only 输出。
- 当前 RAW 观察者配置为 `config/camera/raw-observer.json`。
  - `maximum_clipped_fraction` 仍为 `null`。
  - `maximum_near_noise_floor_fraction` 仍为 `null`。
  - 因此报告必须保持 `pending_thresholds`，不能当作优化验收证据。
  - `combine_green=true` 只是暂定值，不是已经实测确认的 G1/G2 结论。
- 当前 Canon 样本为 RGGB：`raw_pattern=[[0,1],[3,2]]`、`color_desc=RGBG`。
- Canon CR3 的 `camera_white_level_per_channel` 可能明显不可信；现有代码会在不可信时回退到全局 `white_level=16383`。不得删除该回退，除非新样本和测试证明应修改。
- 当前正式 WW/CW 端点仍来自 `config/white/white-endpoints.json`：
  - WW 对应 Ray 命令约 `2931K / GM176`。
  - CW 对应 Ray 命令约 `7702K / GM160`。
  - 这些是 Ray 命令坐标，不是光谱仪绝对 CCT。
- 当前默认 `config/white/white-lut.json` 仍是旧 4x3 LUT，不得覆盖。
- 当前最佳 70 点候选仍是：
  `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`
- 当前最佳候选只完成了最高风险 10 点的最终 60 秒 off/on 独立复测，不能声称最终 70/70 已复测。
- 当前白点验收继续沿用：
  - `abs(Duv error) < 0.0005`
  - CCT 容差为至少 `25K`，高 CCT 使用 `1 mired` 对应的 Kelvin 容差。
- 当前完整测试基线为 `159/159` 通过。

---

## 2. 执行模型的强制工作规则

### 2.1 每次开始前

1. 读取本文件全部内容，不得只读当前阶段。
2. 读取 `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`。
3. 读取 `docs/README.md` 中对应命令和安全约束。
4. 运行 `git status --short`，保留用户未提交改动，不得 reset、checkout 或删除。
5. 仓库有 `.codegraph/`，定位代码时必须先用 CodeGraph，再读未覆盖的配置或文档。
6. 检查是否存在正在运行的校准进程；若存在，不得并发启动第二个硬件任务。
7. 只在用户明确要求实机执行后连接设备。仅批准计划或仅要求写代码，不等于批准实机高亮度扫描。

### 2.2 每个阶段的完成定义

一个阶段只有同时满足以下条件才可标为完成：

- 代码任务完成。
- 有意义的单元测试完成。
- 离线检查通过。
- 该阶段要求的实拍数据完成。
- 分析文件给出明确 `pass`、`conditional_pass` 或 `fail`。
- 所有失败样本仍在索引中，没有手工删除来改善结果。
- 双灯关闭并有 Python 层与 shell 层的关灯记录。
- 本文件的“执行进度”已更新真实路径和结论。

只完成代码时，状态写成 `code_complete_waiting_for_measurement`，不得写成 `complete`。

### 2.3 禁止提前实现的内容

- P1 没有确认 RAW 线性、重复性和 G1/G2 策略前，不实现正式五通道基底求解。
- P2 没有得到实拍基底前，不实现依赖其具体维度或权重的 multipatch 求解器。
- P3 加法性没有结论前，不把 `y=Bu` 当成最终真值。
- P4 12 点 A/B 没通过前，不重算完整 70 点。
- P5 CCT 链没有形成明确结论前，不启动 Ray HSI 大网格。
- P6 没确认 Ray HSI 流形分支前，不写灯带 HSI 插值模型。
- 不得先写固定的 RAW/Hue/SAT 数值阈值，再用数据为它辩护。
- 不得覆盖默认 LUT、端点文件或现有最佳 70 点候选。

### 2.4 测试和提交规则

每个代码阶段至少运行：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
git diff --check
codegraph sync
```

- 如果完整测试因沙箱不能绑定 `127.0.0.1` 失败，应在允许本地回环端口的环境重跑；不得把该错误写成产品失败。
- 不得自动 commit、push 或开 PR。只有用户明确说“提交”时才提交。
- 每个阶段建议独立提交，但提交边界服从用户指令，不为追求提交拆分而改写用户工作区。

---

## 3. 所有硬件运行的统一安全合同

### 3.1 光源隔离

每一张正式照片必须满足“只亮一个光源”：

1. 拍 Ray 前，先关闭灯带并确认调用成功，再开启 Ray。
2. Ray 拍摄完成后，立即把 Ray intensity 设为 `0`。
3. 确认 Ray 关闭后，才允许开启灯带。
4. 灯带拍摄完成后立即 `all_off`，不能依赖下一个状态覆盖当前状态。
5. 任何读回不一致、调用超时或光源状态不确定都直接停止批次。

### 3.2 Python 层清理

所有可能点亮设备的 runner 必须：

- 使用 `try/finally`。
- `finally` 中调用 `camera_based_rgbww_optimizer.control.all_off.turn_everything_off` 或等价公共入口。
- strip 关灯失败时仍继续尝试 Ray 关灯，Ray 失败时仍保留 strip 结果。
- 把结果写入 `all-off-python.json`。
- 正常退出、异常、KeyboardInterrupt 都走同一清理路径。
- 不得为正式校准传 `--leave-ray-on`。

### 3.3 shell 层清理

所有实机命令必须放入独立 shell wrapper；最小结构如下：

```zsh
#!/bin/zsh
set -euo pipefail

RUN_DIR="${1:?run dir required}"
mkdir -p "$RUN_DIR"

cleanup() {
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$RUN_DIR/all-off-shell.json" 2>&1 || true
}

trap cleanup EXIT INT TERM HUP

.venv/bin/python -m camera_based_rgbww_optimizer.optimization.<runner> \
  --output-dir "$RUN_DIR" \
  <其余参数>
```

要求：

- wrapper 放在 `tmp/`，不得放根目录。
- Python runner 和 shell trap 都必须关灯，不能只保留其中一层。
- 后台运行时，重定向日志必须发生在后台 shell 内。
- “观察 5 分钟”表示确认进程持续推进且无错误，然后停止轮询；绝不表示 5 分钟后终止任务。

### 3.4 高输出约束

- `--allow-high-output` 只在 dry-run 计划、通道范围、关灯路径都确认后使用。
- 单通道首次验证仍从低输出开始；正式 25/50/100% 基底扫描只有在通道顺序和热安全已确认后执行。
- 正式白光和 HSI 候选可保持至少一个通道 `4095`，但低码值加法性样本不强制满足该条件。
- 任何异常发热、亮度波动或电源不稳定都停止，不得靠增加迭代次数掩盖。

---

## 4. 统一运行目录和可恢复记录

### 4.1 目录结构

每次运行使用新的不可复用目录：

```text
tmp/<phase>/<YYYYMMDD-HHMMSS>-<name>/
  run.json
  plan.json
  commands.jsonl
  captures.jsonl
  measurements/
    <capture-id>.patch-statistics.json
  camera/
    *.cr3
  analysis.json
  failure.json                 # 仅失败时
  all-off-python.json
  all-off-shell.json
  EXPERIMENT_SUMMARY.md
```

禁止：

- 在旧运行目录覆盖文件。
- 用同一 capture ID 重拍并覆盖旧 CR3。
- 把试拍、探针、冷态帧和正式确认帧混成同一验收集合。
- 保存 `.npy` 作为长期产物。

### 4.2 `run.json` 最低字段

```json
{
  "schema_version": 1,
  "run_id": "...",
  "phase": "P1",
  "status": "planned|running|complete|failed|interrupted",
  "started_at": "...",
  "finished_at": null,
  "git_commit": "...",
  "git_dirty": false,
  "inputs": {
    "location_config": {"path": "...", "sha256": "..."},
    "raw_observer_config": {"path": "...", "sha256": "..."},
    "code_duty_curve": {"path": "...", "sha256": "..."},
    "baseline_lut": {"path": "...", "sha256": "..."}
  },
  "software": {},
  "devices": {},
  "safety": {},
  "retry_of": null
}
```

### 4.3 JSONL 记录要求

`commands.jsonl` 每行记录：

- command ID、时间、source、mode、目标值、五通道命令。
- 前一个设备状态。
- off/on 时间、settle 时间、计划用途。
- `probe|training|confirmation|validation|anchor|ambient` 标签。
- 设备读回和是否一致。

`captures.jsonl` 每行记录：

- capture ID、command ID、CR3 路径和 SHA-256。
- ISO、光圈、快门、曝光缓存来源。
- Ray/strip 哪一个亮，另一个的关灯确认。
- thermal state、repeat index、attempt index。
- 对应 patch-statistics 路径和质量状态。

### 4.4 失败和恢复

- 硬件运行失败后，旧运行目录只追加 `failure.json` 和关灯结果，不继续写正式帧。
- 重试创建新目录，并在 `retry_of` 指向旧 run ID。
- 仅离线分析失败可在同一目录重跑分析，但必须保留旧 `analysis-<timestamp>.json`。
- 候选命令发生任何变化后，旧确认帧不再是新候选的验证证据。

共享 provenance helper 只有在三个 runner 出现相同逻辑后才抽取。若开始 P0 时 CodeGraph 已发现三个独立实现，则先加回归测试，再抽到 `utils/experiment_records.py`；否则先保持 P0 runner 内部实现，避免提前构造框架。

---

## 5. 总阶段图和硬门

| 阶段 | 内容 | 进入条件 | 退出条件 |
|---|---|---|---|
| P0 | 离线分析器、原生 RAW 曝光计、安全 runner | 当前提交存在 | dry-run 和合成测试通过 |
| P1 | RAW 重复性、曝光线性、G1/G2、质量门槛 | P0 通过且用户批准实机 | 测量链 `pass` 或明确 `fail` |
| P2 | 五通道多档经验基底 | P1 `pass` | 单一/分段基底分支确定 |
| P3 | 随机混合加法性 | P2 有可用基底 | 主模型/初值模型/回退闭环分支确定 |
| P4 | 4x3 CCT multipatch A/B | P3 分支确定 | 12 点是否值得扩展有明确结论 |
| P5 | 14x5 全局 CCT/GM 和最终验证 | P4 全部门槛通过 | 安装或保留旧候选的结论完成 |
| P6 | Ray HSI 黑箱表征 | CCT 链已闭环 | HSI 流形分支确定 |
| P7 | 灯带 HSI 候选和 gamut | P6 模型确定 | INT=100 候选通过 |
| P8 | HSI INT 维度 | P7 通过 | 强度可分离或修正层确定 |
| P9 | CCT/HSI 最终独立验证 | 候选冻结 | 安装、回滚和审计完成 |

任何阶段 `fail` 都不能自动进入下一阶段。`conditional_pass` 必须按该阶段指定的受限路径继续，不能按 `pass` 处理。

---

## 6. P0：下一次先做的离线工程

**本阶段不连接相机、Ray 或 ESPHome。**

### 6.1 新增纯分析模块

新增：

```text
src/camera_based_rgbww_optimizer/measurement/raw_observer_analysis.py
tests/test_raw_observer_analysis.py
```

公共函数至少包括：

1. `collect_patch_plane_features(reports, statistic=...)`
   - 验证 schema、patch 名、CFA plane 和 location hash 一致。
   - 默认使用 ambient-subtracted `trimmed_mean_per_second`。
   - 缺失 ambient 时显式标记，不能悄悄改用未扣除值。
2. `analyze_repeatability(reports)`
   - 每个 patch-plane 计算 mean、median、MAD、standard deviation、CV、P95 range。
   - 同时输出全局 P50/P90/P95/max。
3. `analyze_exposure_linearity(exposure_groups, repeatability)`
   - 对每个 patch-plane 比较不同曝光的归一化响应。
   - 输出相对残差、线性斜率、是否单向漂移。
   - 门槛来自实测 repeatability，不能内置项目结论。
4. `analyze_green_consistency(reports)`
   - 输出 G1/G2 比例、相对差、随 patch/曝光/光源/时间的变化。
5. `recommend_quality_thresholds(...)`
   - 只生成候选配置和理由，不直接改 `config/camera/raw-observer.json`。
6. `write_analysis_json(...)`
   - `allow_nan=False`，所有空值写 `null`。

合成测试必须覆盖：

- 重复性稳定与异常值。
- 三档曝光完全线性。
- 只有最短曝光偏离。
- 全部曝光单向非线性。
- G1/G2 完全一致。
- G1/G2 固定比例但不等于 1。
- G1/G2 随光源变化。
- patch 或 plane 集合不一致。
- ambient 缺失。
- NaN、零信号和 JSON 序列化。

### 6.2 原生 RAW 自动曝光计

当前 `camera_gphoto2.auto_expose_capture` 默认依赖 demosaic 解码统计。P1 需要 native mosaic 指标且不保留 `.npy`。实施顺序：

1. 先用 CodeGraph 阅读 `auto_expose_capture` 当前完整调用路径和测试。
2. 新增小型结果结构，例如 `RawExposureMeterResult`：
   - `exposure_metric`
   - `raw_visible_max`
   - `plane_max`
   - `clipped_fraction`
   - `low_signal_fraction`
   - `quality_status`
3. 在 `raw_mosaic_patches.py` 或相邻 measurement 模块实现 `meter_raw_exposure(raw_file, regions, config)`。
4. 给 `auto_expose_capture` 增加可选 `meter_fn`，默认值保持旧行为；不得破坏 location picker、location checker 和现有白光 runner。
5. native runner 传入 `meter_fn`，试拍只保留必要统计并删除试拍 CR3；最终 CR3 保留。
6. 如果改造现有自动曝光 API 会显著扩大影响面，则不改公共 API，先在 P1 runner 内实现独立 bounded shutter search；但必须复用现有 shutter candidate/选择函数，不复制快门算法。

分支：

- **A：可用可选 `meter_fn` 保持兼容。** 采用此方案并补现有默认路径回归测试。
- **B：现有 dataclass/流程强耦合 DecodeResult。** 在 camera 模块新增通用 `ExposureMeasurement` 协议，再由旧 decoder adapter 和新 raw meter adapter 实现；先保护旧测试。
- **C：改造会影响大量现有硬件 runner 且无法离线证明兼容。** 暂不改 camera 公共 API，在 P1 runner 中实现局部 native search，并在计划进度里记录技术债；不得无测试重写旧自动曝光。

### 6.3 P1 安全运行器

新增：

```text
src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py
tests/test_measure_raw_observer_validation.py
```

要求：

- `--dry-run` 只生成 `plan.json`，不能导入后就调用设备。
- 依赖函数可注入，以便单测 fake camera、fake Ray、fake strip。
- 默认锚点为 Ray `5600K / GM100 / INT100`。
- 灯带锚点必须显式读取外置最佳 70 点 LUT，不能走默认 4x3。
- 分别保存 Ray 和 strip 快门缓存。
- 支持配对重复数、曝光 bracket、重复数、ambient、flat-field 和输出目录。
- 每个 capture filename 包含 source、purpose、exposure、repeat、attempt。
- Python `finally` 双关灯。
- 输出符合第 4 节运行合同。

建议 CLI：

```text
--baseline-lut PATH
--location-config PATH
--raw-observer-config PATH
--anchor-cct 5600
--anchor-gm 100
--paired-repeats 5
--linearity-factors 0.5,1,2
--linearity-repeats 3
--off-seconds 1
--settle-seconds 60
--output-dir PATH
--allow-high-output
--dry-run
```

### 6.4 P0 验收

- [ ] 新增分析模块和测试。
- [ ] 原生 RAW 自动曝光路径不生成持久 `.npy`。
- [ ] 旧自动曝光、location UI、白光校准测试全部通过。
- [ ] P1 runner dry-run 计划包含完整配对、bracket、ambient 和 cleanup。
- [ ] fake 硬件异常时 Python cleanup 仍调用 strip 和 Ray 两路。
- [ ] 完整测试、`git diff --check`、CodeGraph sync 通过。
- [ ] 更新 `docs/README.md` 和项目 skill。

P0 完成后停止并向用户报告，不自行开始实机 P1，除非用户同一条指令已明确要求实机执行。

---

## 7. P1：验证 RAW 测量链并确定门槛

### 7.1 实机前检查

按顺序执行；任一步失败都进入“连接失败分支”：

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_gphoto2 detect
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c node-config
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-cct
```

说明：

- `all_off` 同时验证 ESPHome 和 Ray 的可达性；必须检查 JSON 中两路结果，不只看退出码。
- Ray 当前若不在 CCT mode，`get-cct` 可能失败。此时用 `node-config` 证明连接，再由 runner 设置锚点并读回，不把 mode 不同误判为离线。
- 相机只做 detect，不拍照。

### 7.2 冻结基线

运行器开始后先写入：

- 当前 Git commit 和 dirty 状态。
- 最佳 70 点候选、默认 4x3、端点、location、code-duty curve、raw observer config 的 SHA-256。
- rawpy、LibRaw、gphoto2 版本。
- 相机 model/port、匿名设备 ID、镜头/焦距、ISO、光圈。
- Ray node config、固件/app/OpenAPI 信息。
- ESPHome 设备名和固件信息。

如果要跟踪 `config/baselines/...`，先为具体文件增加精确 `.gitignore` 例外；不得放开整个 `config/`。

### 7.3 采集顺序

1. 双灯全关，拍 ambient/dark。
2. Ray 5600/GM100：auto-expose，保存 Ray 快门缓存。
3. strip 5600/GM100：用最佳 70 点显式 LUT 点亮，独立 auto-expose，保存 strip 快门缓存。
4. 完成 5 组 Ray/strip 配对重复：
   - 每次 source 切换前先全关 1 秒。
   - 上命令后 60 秒再拍。
   - 顺序交替，避免所有 Ray 拍完再拍 strip。
5. 对 Ray 和 strip 分别做三档曝光：`0.5x, 1x, 2x` 基准快门，覆盖 4 倍范围。
6. 每档至少 3 次，使用平衡顺序 `1x, 0.5x, 2x, 2x, 0.5x, 1x...`，避免时间顺序与曝光单调相关。
7. 拍一张 flat-field/扩散板基线；若没有可重复的平场材料，记录 `not_available`，不得用色卡白块冒充完整平场。
8. 双灯全关并保存两层 cleanup 结果。

### 7.4 线性与重复性计算

对每个可靠 patch-plane：

```text
z = ambient_subtracted_trimmed_mean / exposure_seconds
relative_residual = (z - robust_center_across_exposures) / robust_center
```

门槛来源：

- 同曝光重复产生 `sigma_repeat`。
- 曝光间残差用 `3 * sigma_repeat` 判断。
- 只使用未裁剪、有效像素足够且不在噪声底的样本。
- 不允许用删除最差曝光的方式直接宣告通过；删除必须进入下面的受限分支。

### 7.5 P1 分支决策

#### 分支 A：全部通过

条件：

- 可靠 patch-plane 没有超过 `3 sigma_repeat` 的系统性曝光趋势。
- Ray 和 strip 均成立。
- 锚点 5 次重复无单向时间漂移。
- ROI、元数据、光源隔离均完整。

动作：

1. 进入 G1/G2 分支。
2. 生成质量门槛候选配置。
3. 用户确认后更新 `config/camera/raw-observer.json` 的 null 阈值和 validation provenance。
4. P1 标记 `pass`，允许进入 P2。

#### 分支 B：只有最短或最长曝光失败，中间重叠区通过

动作：

1. 把失败曝光标为 `outside_valid_exposure_envelope`，保留数据。
2. 收窄允许快门 envelope。
3. 在新边界补拍一档确认，不重拍全部重复。
4. 若新边界通过，P1 可标 `conditional_pass`，后续 runner 必须强制该 envelope。
5. 若补拍仍失败，转分支 D。

#### 分支 C：只有个别 patch/plane 失败

先分类：

- 持久高亮/反光：将该 patch 标成训练排除但保留验证诊断；不得移动 ROI 来隐藏反光。
- 仅某颜色通道接近黑位：为该状态使用弱通道曝光，不丢弃整个 patch。
- 持久坏点导致极低裁剪率：记录持久像素位置，再决定是否允许极小非零裁剪阈值。
- ROI 越界或位置不对：停止，运行 location checker；若几何移动，创建新 location JSON，不覆盖旧文件。

处理后重新分析。若可靠特征仍覆盖所有中性目标和足够的彩色色块，可 `conditional_pass`；否则转分支 D。

#### 分支 D：广泛非线性或 Ray/strip 行为不同

动作：

1. 不设置正式质量门槛。
2. 不进入 P2。
3. 检查：PWM 与快门拍频、电源压降、相机裁剪、黑位、热漂移、ambient、镜头/几何。
4. 若只在 strip 出现，优先测试不同快门是否与 PWM 同步；不要先改 RAW 算法。
5. 若 Ray 和 strip 都出现，优先查相机/RAW/曝光链。
6. 修复后创建新 run，旧 run 保持 `fail`。

#### 分支 E：锚点随时间漂移超过重复性门槛

动作：

1. 判断是 Ray、strip 还是环境共同漂移。
2. strip 漂移：增加预热或调整 off/on 协议，再完整重跑 P1。
3. Ray 漂移：确认风扇/功率模式和预热时间，再完整重跑。
4. 两者同向漂移：查环境光、相机温度、几何和 ambient。
5. 不允许用更宽阈值吸收漂移。

#### 分支 F：连接、读回或关灯失败

动作：

1. 立即停止采集。
2. Python cleanup 和 shell trap 各执行一次。
3. 记录最后已知状态和错误。
4. 人工确认灯具状态；未确认前不得重启。
5. 新连接测试通过后使用新 run 目录重试。

### 7.6 G1/G2 分支

先按 patch、曝光、source、repeat、时间比较 G1/G2：

#### G-A：G1/G2 在重复性内等于 1

- 保留 `combine_green=true`。
- 合并方式为算术平均。
- 在 analysis 中保存“差异不超过重复性”的证据。

#### G-B：G1/G2 为稳定固定比例，但显著不等于 1

- 不直接简单平均。
- 从独立校准集估计固定比例校正，不能用后续优化目标拟合该比例。
- 新增配置字段记录 correction 和来源 run/hash。
- 校正后再合并 G，并用留出重复验证。
- 校正验证通过后进入 P2；失败转 G-C。

#### G-C：G1/G2 随 patch、source、曝光或空间显著变化

- 设置 `combine_green=false`。
- 后续特征维度固定为 `P x 4`。
- 不拟合一个全局比例来掩盖依赖关系。
- P2/P3/P4 所有模型和测试都必须支持四平面。

#### G-D：结果处于边界，证据不足

- 增加独立重复或跨日重复。
- 在结论前保持四平面，四平面是保守默认。
- 不因为减少维度更方便就选择合并。

### 7.7 质量门槛写入规则

分析器只生成 `raw-observer-candidate.json`。写回正式配置前必须：

- 给出每个阈值对应的数据分布。
- 说明会拒绝哪些 patch-plane。
- 确保黑块等 diagnostic-only patch 不影响优化整体状态。
- 保留最少有效像素结构门槛。
- 把 validation status 从 pending 改为带 run ID/hash 的 validated 状态。
- 更新 docs 和 skill。

---

## 8. P2：五通道多档经验基底

### 8.1 代码任务

仅在 P1 `pass` 或允许的 `conditional_pass` 后新增：

```text
src/camera_based_rgbww_optimizer/optimization/measure_chart_response_basis.py
src/camera_based_rgbww_optimizer/measurement/chart_response_basis.py
tests/test_measure_chart_response_basis.py
tests/test_chart_response_basis.py
```

测量 runner 负责设备和记录；measurement 模块只负责纯数据拟合。不得把设备调用塞进矩阵分析模块。

### 8.2 采样计划

- 通道：`cw, ww, r, g, b`。
- 线性目标档位：25%、50%、100%。
- 对应目标代码：`1024, 2048, 4095`。
- 必须经过当前 code-duty curve；不得用 `--no-curve`，因为模型坐标是校正后的线性目标代码。
- 每状态 3 次独立 off/on 60 秒确认。
- 主状态共 `5 x 3 x 3 = 45`。
- 每 8 到 12 个状态插入固定 5600/GM100 strip 锚点。
- 顺序用固定 seed 的平衡随机或拉丁方，seed 写进 `plan.json`。
- 保存前一个状态和总目标负载。

曝光：

- 每通道 100% 先确定保护曝光。
- 每通道 25% 确定弱信号曝光。
- 同一正式状态的重复必须固定快门。
- 若一档曝光不能同时覆盖高反射和低反射 patch，允许同一状态拍保护/弱信号两张，但合并策略必须在拟合前固定。

### 8.3 基底拟合

1. 根据 P1 G 分支选择 3 或 4 CFA plane。
2. 按固定训练 patch 列表拼接向量。
3. ambient 扣除并按曝光归一化。
4. 对重复使用 robust center，方差进入 feature weight。
5. 每个档位生成 `B_level`，形状为 `(feature_count, 5)`。
6. 将列除以目标线性输出比例，比较形状而不是绝对亮度。
7. 输出 SVD、rank、condition number、列夹角、bootstrap 置信区间。
8. 输出每个 feature 的权重、拒绝原因和 provenance。

### 8.4 P2 分支

#### B-A：三档列形状差异不超过重复性

- 合并为单一线性基底 `B`。
- 每通道保留亮度 scale 和置信区间。
- 进入 P3。

#### B-B：只有某些通道随档位稳定变化

- 对这些通道使用低/中/高分段基底。
- 段间只做线性或形状保持插值，不用高阶多项式。
- 其他稳定通道仍用单列。
- 写明 `level_dependent_channels`，进入 P3 的 conditional path。

#### B-C：列高度共线、rank 不足或 condition number 很大

- 不把求解结果解释为唯一通道解。
- 基底仍可作为正则化初值。
- 后续求解增加 RGB/white 先验和邻点连续性。
- 报告最相似的通道列和不可辨识方向。
- 可以进入 P3，但状态为 `conditional_pass_rank_deficient`。

#### B-D：重复本身不稳定或档位变化无规律

- 停止，不进入 P3。
- 检查热态、电源、PWM、曝光和位置。
- 不用复杂模型拟合随机漂移。
- 修复后完整重跑 P2。

---

## 9. P3：随机混合加法性验证

### 9.1 代码任务

新增：

```text
src/camera_based_rgbww_optimizer/optimization/measure_chart_basis_mixtures.py
src/camera_based_rgbww_optimizer/measurement/chart_basis_validation.py
tests/test_chart_basis_validation.py
tests/test_measure_chart_basis_mixtures.py
```

### 9.2 24 个命令的固定覆盖

用固定 seed 生成并把最终明确命令写入 `plan.json`，不能运行时临时随机：

- 5 个单通道主导加弱副通道样本。
- 5 个 white+RGB 双/三通道样本。
- 5 个高总负载、多通道接近上限样本。
- 5 个当前 70 点 LUT 附近、极暖、极冷和高 GM 样本。
- 4 个低/中码值 Latin-hypercube 样本。

每点 2 次独立 off/on，合计 48 个正式状态；固定锚点仍每 8 到 12 个状态插入。

### 9.3 分析

对每个样本比较实测 `y` 与基底预测 `Bu`：

- 加权相对残差。
- 噪声协方差归一化残差。
- 中性色和有色色块残差。
- chroma 残差方向。
- 与总负载、时间、前一状态、active set、码值区间的相关性。

默认判定建议：

- `>=80%` 样本不高于约 `2x` 重复性底噪。
- P95 不高于约 `3x` 重复性底噪。
- 没有跨重复稳定出现的固定 chroma/Hue 方向误差。
- 残差不随总负载单调恶化。

若 70% 到 80% 之间或相关性处于边界，先增加重复，不直接选择模型。

### 9.4 P3 分支

#### M-A：线性模型通过

- `B` 作为主前向模型和求解初值。
- 最终仍需实拍闭环确认。
- 进入 P4。

#### M-B：只在特定档位失败

- 使用 P2 分段基底。
- 在失败档位补充 6 到 12 个定向混合留出点。
- 留出通过后进入 P4 conditional path。

#### M-C：残差与总负载稳定相关

- 先确认不是电源/热问题。
- 若硬件稳定，可拟合一个最小总负载修正项。
- 修正项必须在独立留出混合上显著改善；否则删除修正项。
- 不允许直接加入大量通道交互项。

#### M-D：某些通道组合有稳定系统误差

- 最多增加有物理证据的局部 interaction/分段项。
- 使用训练/留出分离，留出不改善则回退。
- 模型复杂度和适用范围写入 basis config。

#### M-E：广泛不可预测

- 明确标记 `forward_model_seed_only`。
- 不进行全局开环求解。
- P4 只能把 multipatch 目标加入现有局部 Jacobian 实拍闭环。
- 保留当前白点算法，不因模型失败废弃现有 LUT。

---

## 10. P4：4x3 CCT multipatch 先导 A/B

### 10.1 固定目标

```text
CCT: 1800, 3200, 5600, 20000
GM raw: 0, 100, 200
总计: 12 points
```

每点同轮采集：

1. Ray 实测目标。
2. 当前最佳 70 点 LUT 命令。
3. 新 multipatch 候选命令。
4. 两种 strip 命令各两次独立 off/on 60 秒确认。

### 10.2 求解器代码边界

建议新增：

```text
src/camera_based_rgbww_optimizer/optimization/multipatch_objective.py
src/camera_based_rgbww_optimizer/optimization/multipatch_solver.py
src/camera_based_rgbww_optimizer/optimization/measure_cct_multipatch_pilot.py
tests/test_multipatch_objective.py
tests/test_multipatch_solver.py
tests/test_measure_cct_multipatch_pilot.py
```

不要直接把试验逻辑塞进 `measure_white_lut.py`。先让 pilot 独立，P4 通过后再抽取共享 capture/feedback 边界。

现有 `white_lut_feedback._solve_box_constrained_least_squares` 是小维度 active-bound 枚举。新求解器若需要同样语义：

1. 先给现有行为补完整回归测试。
2. 抽到 `optimization/bounded_least_squares.py`。
3. 现有白点 feedback 和新 solver 都调用同一实现。
4. 不复制一份略有不同的 bounds/clipping 代码。

### 10.3 词典序目标

严格按顺序，不能用一个加权总分允许后项抵消前项：

1. 中性 patch RAW chroma 进入硬门槛。
2. 当前 CCT/Duv 门槛通过。
3. 在前两项可行域内最小化彩色色块稳健误差。
4. 再最小化留出 patch 误差。
5. 再考虑邻点连续性、RGB 软先验、headroom 和敏感度。

模型包含允许的全局亮度比例 `k>=0`，以匹配光色而非绝对亮度。命令约束：

```text
0 <= u_j <= 1
max(u) = 1
```

通过枚举 active channel 保证 `max(u)=1`，不要先无约束求解再 clipping。

### 10.4 训练/留出冻结

- 所有可靠 neutral patch 都用于一级硬目标。
- 黑块只作诊断。
- 有色 patch 在优化前按固定规则分成 training 和 holdout，规则写入 config/hash。
- 不得看结果后重新选择留出 patch。
- 若有额外材质，作为第二层 holdout；没有则明确记录。

### 10.5 P4 分支

#### C-A：12 点全部通过并稳定改善

条件：

- 12/12 点两次确认均满足中性 RAW 和 CCT/Duv 门槛。
- 白点对当前候选非劣。
- training 与 holdout 的平均、P90、最坏误差改善超过配对重复性。
- 没有明显命令跳变或只靠大量 RGB 换来小于噪声的改善。

动作：冻结 pilot 权重和目标定义，进入 P5。P5 不允许根据最终验证结果继续调 pilot 权重。

#### C-B：白点通过，但有色/留出改善不超过噪声

- 保留当前 70 点候选。
- multipatch 只作为诊断和验收报告。
- 不进入完整 70 点重算。
- 可以结束 CCT 新算法路线，转 HSI 前需记录此结论。

#### C-C：有色误差改善，但白点越界

- 判定求解目标实现错误或硬约束不足。
- 不放宽当前白点门槛。
- 修正词典序/可行域后只重跑 12 点。
- 连续两版仍失败则停止该路线。

#### C-D：只在 1800/20000 或极端 GM 失败

- 检查 basis 外推、gamut、active channel 和 RGB 先验。
- 若目标不可达，输出明确 `unreachable`，不得靠放宽门槛伪装。
- 可做一次只针对极端点的模型修正，但修正后必须重跑完整 12 点。

#### C-E：两次确认不一致

- 优先判定热态/漂移，不先改 solver。
- 失败确认成为新 thermal base，重建局部 Jacobian。
- 冷态样本不得继续进入 active secant 窗口。
- 稳定后完整重跑受影响点的两次确认。

#### C-F：前向模型 P3 为 seed-only

- 用模型只生成初值。
- 实拍反馈目标扩展为 neutral + multipatch residual。
- 仍保留现有 bounded Jacobian、Broyden、secant 和 thermal rebase。
- 若高维反馈无法稳定估计，退回白点反馈并把 multipatch 仅用于候选排序。

---

## 11. P5：完整 14x5 CCT/GM

### 11.1 进入条件

只有 P4 分支 C-A 才进入。其他分支不得创建完整候选。

目标网格：

```text
CCT: 1800, 2000, 2300, 2700, 3200, 3800, 4500,
     5000, 5600, 6500, 8000, 10000, 14000, 20000
GM:  0, 70, 100, 130, 200
```

### 11.2 Ray 目标采集

- 每个节点 Ray 同会话实拍，不用命令数字代替目标。
- 至少两次配对；极端 CCT 和低 CCT GM 塌缩区增加第三次。
- 固定锚点穿插。
- 保存 native multipatch 向量、协方差和近似 CCT/Duv。

### 11.3 全局求解

变量为 70 个五通道命令，加每点允许的亮度 scale。目标包含：

- 数据项。
- CCT 方向按真实坐标距离加权的二阶平滑。
- GM 方向二阶平滑。
- 交叉方向平滑。
- RGB 软先验。
- active-channel 连续性和命令敏感度。

依赖分支：

#### GLOB-A：允许新增 SciPy 依赖

- 推荐路径。
- 在修改 `pyproject.toml` 前向用户说明新依赖。
- 使用有 bounds 的成熟优化器和明确 Jacobian；保存 solver 版本、终止原因和 KKT/残差指标。
- PCHIP/周期样条也可复用 SciPy。

#### GLOB-B：不允许新增 SciPy

- 使用 NumPy 的分块坐标求解加平滑投影。
- 每轮先逐点 bounded solve，再做平滑 proximal/projection，再重新投影到 bounds 和 active-channel 约束。
- 输出必须标明 `approximate_block_coordinate_solution`，不得声称全局最优。
- 用小型 synthetic grid 验证目标单调下降和约束不破坏。

### 11.4 实拍闭环

保留已验证策略：

- 两次独立确认。
- off 1 秒，上命令 60 秒。
- 确认失败成为 thermal base。
- 连续 secant 预测失准触发 rebase。
- 冷态样本不进入热态 active window。
- 所有历史样本留在 provenance。

### 11.5 插值 A/B

至少比较：

- Kelvin bilinear。
- mired x GM。
- per-channel shape-preserving。
- Ray 实测目标轨迹插值。

至少 20 个非节点留出点，覆盖低 CCT、高 CCT、GM 中点、2300K 塌缩区和 active-set 边界。

分支：

- 某方法在留出实拍上显著更优且连续：选该方法。
- 多方法差异不超过重复性：保留 Kelvin bilinear，优先简单和现有兼容性。
- 方法局部优劣不同：允许分区策略，但必须在边界检查命令和观测连续性。
- 所有方法留出失败：增加必要节点或回到全局平滑，不能安装。

### 11.6 70/70 最终验证

候选冻结后，独立新 run：

- 70/70 节点全部 off/on 60 秒。
- 每点至少两次，风险点三次。
- 顺序随机或分块平衡。
- 最少 20 个插值留出点。
- 固定锚点监控。
- 验证 run 内绝不再优化。

若任何节点失败：

1. 当前 candidate 标记失败，不安装。
2. 单独分析失败点并生成新 candidate 版本。
3. 先定向复核失败点。
4. 新 candidate 一旦改变，最终仍需重新完整 70/70 验证；旧通过帧不能拼成新 candidate 的 70/70。

### 11.7 安装分支

只有全部满足才安装：

- 70/70 和插值留出通过。
- multipatch 优于当前候选，白点不退化。
- provenance 完整。
- 默认 LUT 备份、hash 和回滚命令明确。
- 全测试通过。

否则保留旧默认和当前外置候选，并在总结中明确未安装原因。

---

## 12. P6：Ray HSI 黑箱表征

只有 CCT 路线形成明确“安装新候选”或“保留旧候选”的闭环结论后开始。

### 12.1 代码

```text
src/camera_based_rgbww_optimizer/optimization/measure_ray_hsi_manifold.py
src/camera_based_rgbww_optimizer/measurement/ray_hsi_analysis.py
tests/test_ray_hsi_analysis.py
tests/test_measure_ray_hsi_manifold.py
```

本阶段只控制 Ray，不控制 strip。仍需 shell/Python 双关灯。

### 12.2 SAT=0

Hue：`0,60,120,180,240,300`，SAT=0，每点两次；一个 Hue 做 5 次。

分支：

- Hue 影响不超过重复性：合并为一个 zero-sat anchor。
- Hue 影响超过 `3 sigma` 且重复：保留 Hue-dependent SAT=0 曲线。
- 影响不稳定：查 Ray mode/readback/热态，不选择模型。

### 12.3 HSI 与 RGB 端点

比较 Ray RGB R/G/B/C/M/Y 与 HSI 对应 Hue、SAT100：

- 若仅全局 scale 不同，可共享方向模型但保留 mode scale。
- 若 chroma 路径不同，HSI 和 RGB 必须独立建模。
- 若有白通道迹象，记录但不推测 Ray 内部 PWM。

### 12.4 粗网格

- Hue：`0..330` 每 30 度。
- SAT：`5,20,50,80,95,100`。
- INT=100。
- 共 73 个基础状态，加锚点和重复。

### 12.5 流形分支

#### H-A：近似可分离

条件建议：至少 90% 中间 SAT 节点的 affine 正交残差不高于约 `2x` 重复性底噪，且无系统 Hue 区域偏差。

动作：

- 保存 zero-sat anchor。
- Hue 使用周期端点曲线。
- 每 Hue 的 SAT 使用单调曲线。

#### H-B：存在稳定二维弯曲

- 使用完整周期二维 `t(h,s)`。
- 只在高曲率区域自适应加点。
- 不强制标准 HSV/HSL 几何。

#### H-C：只有局部异常

- 先重拍异常点。
- 重复后仍异常才加密节点。
- 不用单次异常决定二维模型。

#### H-D：Ray 读回与命令不一致或状态漂移

- 立即停止并关灯。
- 不拟合该 run。
- 修复通信/模式/热态后新 run 重测。

---

## 13. P7：灯带 HSI 候选和 gamut

### 13.1 求解优先级

1. Hue 误差。
2. Ray 等效 SAT 进度误差。
3. neutral/multipatch 误差。
4. 命令连续和 0/360 周期连续。
5. 白通道软先验。
6. headroom、功耗和敏感度。

不能只优化整体 RAW RMSE。

### 13.2 首轮节点

- 使用 P6 已测粗网格。
- 经验基底生成初值，实拍反馈修正。
- 保存 CW/WW/R/G/B、white/rgb sensor fraction、active channel、condition number 和 sensitivity。

### 13.3 `s_exact_max(h)`

每个 Hue 从低 SAT 向上搜索：

- 最后一个精确可达点。
- 第一个超门槛点。
- 边界附近二分或加密。
- 保存边界通道和原因。

分支：

- 请求 SAT 在边界内：`faithful`。
- 请求 SAT 超边界：Hue-preserving compression，并返回 `gamut_clipped=true`。
- Hue 本身不可保持：返回 `hue_unreachable`，不得只报 SAT 压缩。
- 边界不平滑：增加 Hue 节点或检查 active-set 切换，不能直接平滑掉真实不可达区。

### 13.4 插值

- Hue 优先周期 cubic 或周期分段插值。
- SAT 优先单调 PCHIP 或分段线性。
- 插值后检查 0..4095、gamut、active set 和 0/360。
- 若插值命令预测失败，可改为插值 Ray 目标后重新求解，但必须评估运行成本和确定性。

P7 只有 INT=100 的节点与随机留出通过后才进入 P8。

---

## 14. P8：HSI INT 强度维度

测试 INT：`100,50,20,5`，覆盖 SAT0、R/G/B/C/M/Y、SAT50、最难 Hue、white-heavy 和 RGB-only 点。

比较：

```text
t(h,s,I) ~= alpha(I,h,s) * t(h,s,100)
```

分支：

### I-A：颜色与强度可分离

- HSI 色彩 LUT 只保留 INT100。
- 用一维 Ray 相对强度曲线缩放。
- 再经过各通道 code-duty 反查。
- 在 INT5 验证量化和 PWM 色偏。

### I-B：仅低强度偏色

- 增加 `1,5,10,25,50,100` 稀疏修正。
- 优先 per-channel correction，不扩成均匀三维 LUT。

### I-C：Hue/SAT 与 INT 广泛耦合

- 使用稀疏局部修正层并自适应加点。
- 若数据量不可控，缩小产品承诺到 INT100 或受限 INT 范围，明确报告。

默认亮度语义为“复制 Ray 相对强度曲线，允许 Ray100 与 strip100 存在全局比例”。若未来要求绝对照度，必须另立测量计划。

---

## 15. P9：最终独立验证和安装

### 15.1 CCT 验证

- 完整 70 节点。
- 至少 20 个非节点。
- 极端 CCT、GM 塌缩区、active-set 边界。
- 同日和跨日。
- 训练色卡和留出目标。

### 15.2 HSI 验证

- 粗节点和至少 50 个未训练随机点。
- 0/360、SAT0/2/5、SAT90/95/100。
- 每个 `s_exact_max` 两侧。
- 多个 INT 和跨日。

### 15.3 统计报告

必须同时报告：

- P50/P90/P95/max，不只平均值。
- 重复性和置信区间。
- training 与 holdout。
- 同日与跨日。
- 所有失败点。
- CCT 的 RAW、Duv、CCT/mired、multipatch、RGB/white 贡献。
- HSI 的 Hue、SAT progress、正交误差、gamut、white fraction 和 INT 色偏。

### 15.4 最终分支

- **全部通过：** 备份默认配置，安装候选，写 hash 和回滚命令，再做代表命令和关灯 smoke test。
- **节点通过、插值失败：** 不安装，增加节点或更换插值后重新独立验证。
- **同日通过、跨日失败：** 不安装，先解决环境/热态或给出会话校准限制。
- **CCT 通过、HSI 失败：** 允许只交付 CCT，HSI 保持实验状态；两个配置不得捆绑安装。
- **HSI 部分 gamut 不可达但压缩稳定：** 可交付带显式 gamut 状态的 HSI，不得宣称全域精确复制。
- **安全记录不完整或最终关灯未确认：** 整个验证 run 无效。

---

## 16. 执行进度

执行模型每完成一个实际步骤就更新，不得最后一次性全勾选。

### 已完成

- [x] 现有白点-only 14x5 候选和热态修复。
- [x] 原生 Bayer `R/G1/G2/B` patch statistics。
- [x] ambient subtraction、位置缩放、JSON-only 输出。
- [x] 合成测试和已有 CR3 离线 smoke test。

### 当前下一步 P0

- [x] `raw_observer_analysis.py`。
- [x] repeatability/linearity/G1G2 合成测试。
- [x] native RAW exposure meter。
- [x] 可选 `meter_fn` 自动曝光路径，旧 decoder 默认路径保持不变。
- [x] `measure_raw_observer_validation.py` immutable dry-run 计划和测试。
- [x] `measure_raw_observer_validation.py` fake-device 执行和 Python cleanup 测试。
- [x] 文档和 skill 更新。
- [x] 完整离线验证。
- [ ] 向用户报告并等待实机批准。

### 后续硬门

- [ ] P1 RAW 测量链。
- [ ] P2 五通道基底。
- [ ] P3 随机混合。
- [ ] P4 12 点 A/B。
- [ ] P5 70 点 CCT/GM。
- [ ] P6 Ray HSI。
- [ ] P7 strip HSI。
- [ ] P8 INT。
- [ ] P9 最终验证。

### 每次更新必须填写

```text
最新阶段：
状态：not_started | code_complete_waiting_for_measurement | running | pass | conditional_pass | fail
最新提交：
运行目录：
分析文件：
分支选择：
未解决问题：
下一条唯一动作：
```

---

### 2026-07-14 P1.2 更新

```text
最新阶段：P1 RAW observer measurement
状态：fail
最新提交：b02bfc7 fix(measurement): redact P1 camera provenance
运行目录：/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6
分析文件：/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6/analysis.json
分支选择：7.5-D。v6 完成 31/31，provenance、source isolation、两层 cleanup、G1/G2 均完整，但未裁剪的 0.5x/1x/1.5x 曝光仍呈系统性跨快门残差（Ray P95 1.458%，strip P95 1.133%），远高于重复性。v7 受限诊断进一步显示 strip 在 1/60 相对 1/80 稳定低约 4.64%，Ray 也存在较小但系统的 shutter response。
未解决问题：区分相机实际快门响应与 strip 电源/驱动响应；离线重算已排除 ambient（对每个档位中位影响不超过 0.000063%）和普通跨 run 热漂移。未设置正式 quality thresholds，P2 不得开始。
下一条唯一动作：只用 v6/v7 已保存 RAW 做离线分布与顺序诊断，形成能区分原因的下一次有界实拍设计；当地时间 05:00 后不得开始实拍。
```

---

## 17. 计划归档规则

当 P9 完成，或用户明确终止整个路线时：

1. 确保本文件进度和最终分支真实完整。
2. 创建 `.agent-work/PLANS/`（若不存在）。
3. 将本文件移动为 `.agent-work/PLANS/{YYYYMMDD-HHMM}.md`。
4. 不保留第二份活动 `PLAN.md`。
5. 只有用户明确要求时才提交归档文件。

在上下文压缩、任务恢复或换模型后，必须重新读取本文件；不得凭聊天摘要跳过硬门。
