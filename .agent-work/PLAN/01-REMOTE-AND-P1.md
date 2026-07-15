# 阶段 1：远程采集链与 RAW 测量有效性

**覆盖原阶段：** P0、P0-R、P1

**进入条件：** 当前活动阶段为 `stage_1`；已读取 `00-CONTRACT.md`；代码工作无需设备，实拍另需用户明确授权。

**阶段目标：** 先完成 remote backend 和最新点位迁移，再用远程相机证明 RAW 重复性、曝光响应与 G1/G2 策略足以支撑后续模型。

**不得跨越：** P1 未经高级模型审阅为 `pass` 或允许的 `conditional_pass`，不得开始五通道基底。

## 执行顺序

1. 完成 P0/P0-R 尚未完成的代码、测试、文档和 dry-run；不联机。
2. 更新总控状态为 `code_complete_waiting_for_measurement`，等待用户实机授权。
3. 获授权后按 P1-D1 先跑 5 张 remote preflight；按本文件既定阈值处理一次确定性 target 调整。
4. preflight 通过后运行同配置完整 31 张 P1；不得跳到 P1-D 或 P2。
5. 完成 recorded-exposure、total/global-scale/shape、repeatability 和 G1/G2 分析，保留所有失败样本。
6. 形成阶段交接包并停止，不自行写入正式质量阈值，不进入阶段 2。

## 高级模型决策门 Gate-1

高级模型只在下列证据齐全后决策：

- remote backend、最新 location hash、密钥脱敏和双 cleanup 均已验证。
- Ray/strip 各自的 non-reference shape residual 与 `3 sigma_repeat` 对比完整。
- recorded exposure 全部为 `recorded`，无 nominal fallback。
- G1/G2 属于 G-A、G-B、G-C 或 G-D 的证据和建议明确。
- 质量阈值仍为 candidate，未擅自写入正式配置。

允许出口：`approve_stage_2`、`repeat_stage_1_D1`、`approve_cross_day_D2`、`run_strip_only_D3`、`stop_route`。任何 response correction、阈值放宽或正式配置写回都必须在此门由高级模型明确批准。

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
- 正式执行必须构造并复用 `RemoteCameraBackend`，不得回退本地相机；remote config/capture 失败时不得自动尝试 gphoto2。
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
--location-config config/location/locations-20260714-211759.json
--raw-observer-config PATH
--camera-backend remote
--remote-env-file .env
--remote-timeout 120
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
- [ ] P1 runner dry-run 固定 remote backend 和最新 location path/hash，且不读取 `.env`。
- [ ] fake 硬件异常时 Python cleanup 仍调用 strip 和 Ray 两路。
- [ ] 完整测试、`git diff --check`、CodeGraph sync 通过。
- [ ] 更新 `docs/README.md` 和项目 skill。

P0 完成后停止并向用户报告，不自行开始实机 P1，除非用户同一条指令已明确要求实机执行。

### 6.5 P0-R：远程相机与新点位迁移

**本阶段只写代码、单元测试和 dry-run，不访问 `/health`、`/v1/config`、`/v1/capture`、Ray 或 ESPHome。**

基础能力已经存在于 `control/camera_remote.py`，并由 location picker/checker 使用；但优化 runner 仍有本地相机调用和旧点位默认值。必须先完成以下迁移，不能直接把 P1 wrapper 改个命令名就开始采集。

#### 6.5.1 固定最新点位

1. 将以下模块中面向新实验的 `DEFAULT_LOCATION_CONFIG` 或 auto-exposure metering 默认值改为 `config/location/locations-20260714-211759.json`：
   - `measurement/raw_mosaic_patches.py`
   - `optimization/measure_raw_observer_validation.py`
   - `optimization/measure_raw_shutter_response.py`
   - `optimization/measure_white_lut.py`
   - `optimization/measure_white_endpoints.py`
   - `optimization/measure_channel_response.py`
2. 更新 `docs/README.md` 和 `.agents/skills/camera-based-rgbww-optimizer/SKILL.md` 中所有“当前/正式/新运行”命令。旧点位只能留在明确标注为历史复算的示例里。
3. 增加测试，断言每个正式 runner 的默认 location 路径是新文件；同时要求正式 wrapper 仍显式传路径。
4. `build_*_plan` 写入点位 hash；执行前重新计算并与计划值比较，不一致直接停止。
5. 不修改历史 JSON、CR3、analysis 内记录的旧路径和 hash。

#### 6.5.2 增加无拍摄远程探测入口

给 `camera_remote` 增加两个只读子命令：

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote health --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote config --json
```

要求：

- 两个命令都由脚本内部解析 base URL；`config` 还加载 Token。CLI 不要求 `--token`，输出不包含 Token。
- `health` 只调用 `GET /health`；`config` 只调用 `GET /v1/config`。两者都不拍照、不改变设置。
- `health` 输出 backend、base URL 和服务状态；`config` 输出 backend、base URL、model、当前 ISO/光圈/快门/RAW 和 choice 数量。
- 401、409、502、504 使用稳定的非零退出码和脱敏错误；`camera_busy` 仍使用已有有界重试。
- 保留现有直接 capture CLI 的兼容行为；若改为 subcommand parser，旧无 subcommand 调用必须有回归测试或清晰迁移错误。
- 用 fake opener 测试 health 成功/失败，以及 config 成功、缺 Token、401、busy 后成功、持续 busy 和输出脱敏；测试不得读取真实 `.env`。

#### 6.5.3 把 backend 注入实验 runner

按 CodeGraph 实际调用路径逐个迁移，不复制自动曝光算法：

1. P1 `measure_raw_observer_validation` 先接入 `CameraBackend`/backend factory，这是下一次实机的硬阻塞项。
2. P1-D `measure_raw_shutter_response` 接入同一接口，但只有计划 7.5-D3 被触发时才实机调用。
3. 白端点、白 LUT、channel response 以及后续新增的 P2-P9 runner 都使用相同接口。
4. CLI 统一暴露：

```text
--camera-backend local|remote
--remote-env-file PATH       # 默认项目 .env；只传路径，不读取或记录内容
--remote-base-url URL        # 可选；通常不传
--remote-timeout SECONDS
```

正式 wrapper 必须显式 `--camera-backend remote`；不得暴露或使用 `--remote-token`。保留 local backend 是兼容要求，但它不能出现在新实验 run 中。

runner 构造一次 `RemoteCameraBackend.from_environment()` 并传给所有 `auto_expose_capture`/固定快门 capture。连接返回的 model/URL 写入 provenance，Token 永不进入对象序列化。Ray/strip 两路 exposure cache 语义保持不变。

#### 6.5.4 dry-run 和测试矩阵

至少覆盖：

- `--dry-run --camera-backend remote` 不读取 `.env`、不打开网络、不调用灯具。
- fake remote config 的 `implicit auto` 光圈可正常通过；本地默认光圈 `4` 不得泄漏到 remote 请求。
- 自动曝光全部 trial 和最终 capture 都走传入的同一 backend。
- `camera_busy` 后恢复不会重复登记 capture；持续失败会写 failure 并执行 Python 双关灯。
- 下载为空、下载中断和原子替换失败不会留下正式 CR3/`.part` 或成功记录。
- remote CR3 仍由本机 rawpy/native mosaic 测量，recorded exposure 仍来自 CR3。
- plan/run/captures/exception/log 全文扫描不含测试 Token。
- 最新点位的 24 块、4320x2880、hash 被计划冻结。
- fake runner 中任何异常仍先后尝试 strip 和 Ray 两路关灯。

P0-R 验收：

- [ ] 全部正式采集 runner 有 remote backend 入口，P1 不再硬编码本地 gphoto2。
- [ ] 所有新实验默认点位迁移到 `locations-20260714-211759.json`。
- [ ] `camera_remote health --json` 和 `config --json` 可离线 fake 测试且不泄露密钥。
- [ ] P1 5 张 preflight dry-run 明确写出 `camera_backend=remote`、新点位路径/hash、5 个 capture 和双 cleanup。
- [ ] 完整测试、`git diff --check`、CodeGraph sync 通过。
- [ ] 状态标为 `code_complete_waiting_for_measurement` 后停止；没有用户新的实机授权不得访问设备。

---

## 7. P1：验证 RAW 测量链并确定门槛

### 7.1 实机前检查

只有 P0-R 全部验收后才按顺序执行；任一步失败都进入“连接失败分支”：

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote health --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote config --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c node-config
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-cct
```

说明：

- `all_off` 同时验证 ESPHome 和 Ray 的可达性；必须检查 JSON 中两路结果，不只看退出码。
- `camera_remote health --json` 由脚本解析 base URL 后调用无认证 `GET /health`；只证明 bridge HTTP 服务可达，不证明认证、相机连接或可拍摄。
- `camera_remote config --json` 由脚本加载 `.env` 并调用认证 `GET /v1/config`，只读且不拍照。不得用 shell 展开 Token 后自行 curl `/v1/config`。
- 不再运行本地 `camera_gphoto2 detect` 作为项目相机在线证据；它检测的是本机 USB 路径，与后续远程采集链不同。
- Ray 当前若不在 CCT mode，`get-cct` 可能失败。此时用 `node-config` 证明连接，再由 runner 设置锚点并读回，不把 mode 不同误判为离线。
- 相机只做 health/config，不拍照，也不修改曝光设置。

### 7.2 冻结基线

运行器开始后先写入：

- 当前 Git commit 和 dirty 状态。
- 最佳 70 点候选、默认 4x3、端点、location、code-duty curve、raw observer config 的 SHA-256。
- rawpy、LibRaw 和 remote backend 代码版本。
- 相机 backend=`remote`、bridge base URL/API 文档 hash、model、匿名设备 ID、镜头/焦距、ISO、光圈、快门 choices；不记录 Token。
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

从 2026-07-14 起，`exposure_seconds` 必须来自 CR3 recorded exposure；任何
`fallback_nominal` 或缺失 exposure provenance 的报告都不能用于 P1 验收。

同时必须拆开两种误差，不能把它们混成一个 P95：

```text
response_ratio[f,e] = z[f,e] / z[f,reference]
global_scale[e] = median_f(response_ratio[f,e])
shape_residual[f,e] = response_ratio[f,e] / global_scale[e] - 1
```

- `global_scale` 是某个曝光档整体共同的亮度比例。P4 允许每个目标有全局 `k`，因此它不等同于颜色 shape 失败；但 P2 绝对强度/基底仍必须单独处理它。
- `shape_residual` 是去掉全局 scale 后的 patch/CFA 差异，属于颜色观察者链的硬证据。
- 汇总必须同时给全部 center 和 `non_reference` center。参考档残差按定义为零，不能用这些零值稀释 P95。
- 必须按 CFA plane、patch、信号水平查看 shape，不能只报告总体 P95。

门槛来源：

- 同曝光重复产生 `sigma_repeat`。
- 曝光间残差用 `3 * sigma_repeat` 判断。
- 只使用未裁剪、有效像素足够且不在噪声底的样本。
- 不允许用删除最差曝光的方式直接宣告通过；删除必须进入下面的受限分支。
- `3 * sigma_repeat` 表示统计上可检测的系统误差，不自动等于工程不可用。若未来要引入独立工程容差，必须先做下游 multipatch 灵敏度和独立跨日留出验证；当前阶段仍不得自行放宽。

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

#### 分支 D0：旧报告尚未按 CR3 recorded exposure 重算

动作：

1. 运行 `analyze_raw_observer_validation RUN_DIR --recompute-recorded-exposure`。
2. 必须确认冻结的 location/observer-config hash 仍匹配。
3. 必须确认 `normalization.exposure_provenance.status_counts` 只有 `recorded`，且每张报告都有来源。
4. 保留原 `analysis.json`，只读取新的 `analysis-recorded-exposure-v1.json`。
5. 重算前禁止 P1-D；requested shutter 误差不能用新的设备扫描掩盖。

v6/v7 已完成 D0，不得重复重算来制造新版本文件，除非分析 schema 再变化。

#### 分支 D1：recorded exposure 修复了大误差，但仍有高信号 shape residual

这是当前分支。先做一个独立 5 张预检 run，不直接跑 31 张完整 P1：

```bash
RUN_DIR=/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/<new-preflight-run>
tmp/run-raw-observer-validation.zsh "$RUN_DIR" \
  --baseline-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  --camera-backend remote \
  --location-config config/location/locations-20260714-211759.json \
  --target-max 19661 \
  --linearity-factors 0.5,1,1.5 \
  --paired-repeats 5 \
  --linearity-repeats 3 \
  --preflight-only
```

预检计划必须与以下离线计划同构：

- `tmp/raw-observer-validation/offline/p1-recorded-exposure-low-signal-preflight-dryrun-20260714/plan.json`
- 共 5 张：ambient 1、Ray/strip baseline auto exposure 各 1、Ray/strip `1.5x` 最长 bracket 各 1。
- `measurement.camera_auto_exposure.target_max=19661`。
- `measurement.preflight_only=true`。

预检完成后运行默认分析器。新报告已经按 recorded exposure 归一化，不需要 `--recompute-recorded-exposure`。读取 `analysis.json.preflight.sources` 并按以下分支执行：

- 任一 source `maximum_clipped_fraction > 0`：预检失败。计算新的 target candidate `floor(old_target * 0.40 / observed_trimmed_max)`，再乘 `0.9` 安全系数，限制为至少 `8192`；新建 run，不复用目录。
- 任一 source `maximum_black_corrected_normalized_trimmed_mean > 0.45`：同上降低 target，哪怕 clipped fraction 为零也不能继续。
- 任一 source `maximum_near_noise_floor_fraction > 0`：检查具体 patch/plane。若只出现在弱通道，优先保持 target 并按 7.5-C 分类；若广泛出现，target 过低，不得直接跑完整 P1。
- 任一 source `missing_metrics_plane_count > 0`：代码/报告失败，停止并修复，不得人工估计。
- 两源均无裁剪、无广泛 noise-floor，且最大 trimmed signal `<=0.45`：预检通过，才允许创建完整 P1 run。

`19661` 是由现有 `0.47..0.55` baseline 和 `0.59..0.87` 长 bracket 反推的起点，不是写入配置的质量阈值。

完整 P1 必须使用与通过预检完全相同的 remote backend、`--target-max`、LUT、location、observer config、ISO/remote aperture 和 factors，计划模板为：

- `tmp/raw-observer-validation/offline/p1-recorded-exposure-low-signal-full-dryrun-20260714/plan.json`
- 共 31 张：ambient 1、baseline 2、paired repeats 10、linearity brackets 18。

完整 P1 分析后：

- recorded exposure 缺失或 fallback：run 无效，修元数据链后新建 run。
- total residual 失败但 shape 在 `3 sigma_repeat` 内，且只剩稳定 global scale：记录为“颜色观察者链候选通过、绝对强度链未通过”，仍不得进入 P2，先重测 code-duty/basis。
- shape 在 Ray 和 strip 均不超过 `3 sigma_repeat`：继续 7.6 G1/G2 分支。
- shape 仍在高信号区同向失败：不要再降 target 反复试到通过；转 D2，要求跨日留出后才允许响应修正。
- 只有 strip shape 失败：才恢复下面的 P1-D source diagnostic。

#### 分支 D2：低信号完整 P1 仍显示跨光源相机响应曲线

1. 不修改原生 RAW 值，不立即安装 response correction。
2. 用一天的数据拟合单调响应候选，另一天完整 P1 只做 holdout；训练和验证不能来自同一个 run。
3. 候选至少保证 `g(0)=0`、全域一阶导数为正，并输出系数、训练范围、越界策略和 hash。
4. 同时比较“降低曝光 envelope”与“response correction”两个分支对 non-reference shape P95、最大值和 sigma 的改善。
5. 只有跨日 holdout 改善且不恶化低信号/任一 CFA plane，才提出正式配置 schema；执行模型不得自行写入 `raw-observer.json`。

当前仅有同日探索：`g(y)=y*(1+a*y+b*y^2)` 在 v6->v7 和 v7->v6 留出上把 P95 shape 分别降至约 `0.1068%`、`0.1858%`。这只证明方向可研究，不是安装证据。

#### 分支 D3：只有 strip 仍异常时的 P1-D

仅在 D1 完整低信号 P1 显示 Ray shape 通过、strip shape 失败时，才运行 `measure_raw_shutter_response`：

1. Ray 默认 `1%`，strip 默认 `20%`；任何提高都要先做最长快门裁剪预检。
2. 连续点亮后使用相同 `1/100,1/80,1/60,1/50` 序列，每档六帧。
3. 分析必须检查 recorded exposure provenance、裁剪排除、global shutter scale 和 shape residual。
4. 两源同样复现则返回 D2；只 strip 复现才检查电源/驱动/负载；个别 patch/plane 转 7.5-C。
5. P1-D 无论结果如何都不能替代一个新的完整 P1 pass。

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
