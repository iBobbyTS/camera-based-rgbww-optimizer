# 全局执行合同

**适用范围：** `.agent-work/PLAN/01-REMOTE-AND-P1.md` 至 `07-FINAL-VALIDATION.md` 的全部工作。

执行模型在开始任一阶段前必须先完整读取本文件，再读取当前阶段文件和 `.agent-work/PLAN.md` 的状态。这里的安全、数据、远程访问、测试和提交规则优先于阶段文件中的局部步骤。除非高级模型明确修订本合同，否则低级模型不得放宽。

本文件不是独立执行阶段，不产生“完成”状态。阶段切换和高级模型决策门统一记录在 `.agent-work/PLAN.md`。

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

从 2026-07-14 起，所有新实拍实验必须通过 `r6-camera-bridge` 远程控制相机；本地 gphoto2 路径仅保留兼容和单元测试用途，不再用于生成新的项目验收数据。所有新实验固定使用 `config/location/locations-20260714-211759.json`，旧点位只允许用于复算其对应的历史 CR3，不能混入新 run。

---

## 1. 当前事实和不可回退的基线

执行模型开始任何工作前，必须确认以下事实仍成立；若路径或提交发生变化，先更新本节，不得静默替换：

- 当前基线提交为 `ecf47d7`；开始执行前必须以 `git rev-parse HEAD` 更新，不得把本行当作提交授权。
- 当前唯一允许用于新采集的点位为 `config/location/locations-20260714-211759.json`：
  - SHA-256：`21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`。
  - 图像尺寸 `4320x2880`，24 个色块，`orientation_degrees=180`。
  - 该文件由远程相机采集生成；新 run 必须同时记录路径和 hash。
  - 任一 runner、meter、文档命令或 skill 仍默认 `locations-20260709-012045.json` 或更早文件，都必须先离线迁移并补测试。历史 analysis 保留其原 location hash，不得重写 provenance。
- 远程相机 API 文档固定为 `http://ibobby-rpi-4.local:8088/v1/API.md`。服务为同步 API：`GET /health` 无需认证，`GET /v1/config` 和 `POST /v1/capture` 使用 Bearer Token，成功 capture 直接返回 CR3，不存在异步任务或轮询接口。
- 远程访问配置存放在项目 `.env`。只允许项目脚本通过 `camera_remote.load_remote_camera_config()` 或 `RemoteCameraBackend.from_environment()` 加载；执行模型不得 `cat`、`sed`、`grep`、`source`、`env`、`printenv`、日志输出或以 `--token`/shell 参数展开 `.env` 和 Token。
- 原生 Bayer 测量器已经存在：
  - `src/camera_based_rgbww_optimizer/measurement/raw_mosaic_patches.py`
  - CLI：`python -m camera_based_rgbww_optimizer.measurement.raw_mosaic_patches`
  - 直接读取 `raw_image_visible`，不做 demosaic、白平衡或 gamma。
  - 输出 `R/G1/G2/B`，可选 `G=(G1+G2)/2`。
  - 支持曝光归一化、ambient/dark 扣除、裁剪/噪声诊断和 JSON-only 输出。
- 当前 RAW 观察者配置为 `config/camera/raw-observer.json` v2。
  - Gate-1 采用 identity RAW，仅允许每源自动曝光相对因子 `1.0x..1.25x`。
  - `maximum_clipped_fraction=0.0`、`maximum_near_noise_floor_fraction=0.05`、`maximum_nonfinite_fraction=0.0`、`minimum_valid_pixels_per_plane=29000`。
  - G1/G2 归入 G-C，`combine_green=false`；后续固定使用 `R/G1/G2/B` 四平面。
  - 冻结多项式 response candidate 未安装，因为它把 boundary 最差 feature 从 `2.903` 提高到 `3.182 sigma_repeat`。
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
- remote backend 提交前的完整离线测试基线为 `219/219` 通过；执行 P0-R 后必须记录新的完整测试总数，不能继续把 219 当作当前结论。
- CR3 实际曝光必须由共享入口 `measurement.recorded_exposure` 解析：`Canon:ExposureTime` 优先，标准 EXIF 次之，显示快门只能作为带 `fallback_nominal` 状态的降级值。
- v6/v7 已从所有保留 CR3 完整重算，输出分别为：
  - `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6/analysis-recorded-exposure-v1.json`
  - `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-035100-p1-exposure-diagnostic-v7/analysis-recorded-exposure-v1.json`
- 两份重算分别有 `31/31`、`27/27` 使用 `Canon:ExposureTime`，无 nominal fallback。P1 仍未通过，原因已从“疑似 strip shutter/PWM”收窄为“高信号 RAW shape residual”。
- 当前 June 6 code-duty archive 的原始 run/CR3 已丢失，不能按 recorded exposure 修复。现有 `config/channel/code-duty-curve.json` 只允许兼容既有闭环白 LUT，不得作为 P2 绝对基底或亮度证据。

---

## 2. 执行模型的强制工作规则

### 2.1 每次开始前

1. 读取 `.agent-work/PLAN.md`、本文件和当前阶段文件全部内容，不得只读状态摘要。
2. 读取 `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`。
3. 读取 `docs/README.md` 中对应命令和安全约束。
4. 运行 `git status --short`，保留用户未提交改动，不得 reset、checkout 或删除。
5. 仓库有 `.codegraph/`，定位代码时必须先用 CodeGraph，再读未覆盖的配置或文档。
6. 检查是否存在正在运行的校准进程；若存在，不得并发启动第二个硬件任务。
7. 只在用户明确要求实机执行后连接设备。仅批准计划或仅要求写代码，不等于批准实机高亮度扫描。
8. 读取远程 API 合同时只访问 `http://ibobby-rpi-4.local:8088/v1/API.md`；不得为“确认配置”而直接读取 `.env`。
9. 新实验命令必须显式传 `--camera-backend remote` 和最新 `--location-config`，即使 CLI 默认值已经迁移；运行记录不得依赖不可见默认值。
10. 远程 camera config、capture 和自动曝光必须复用同一个 `RemoteCameraBackend` 实例；不得在并行线程或第二个进程中同时访问相机。

### 2.2 每个阶段的完成定义

一个阶段只有同时满足以下条件才可标为完成：

- 代码任务完成。
- 有意义的单元测试完成。
- 离线检查通过。
- 该阶段要求的实拍数据完成。
- 分析文件给出明确 `pass`、`conditional_pass` 或 `fail`。
- 所有失败样本仍在索引中，没有手工删除来改善结果。
- 双灯关闭并有 Python 层与 shell 层的关灯记录。
- `.agent-work/PLAN.md` 的当前状态已更新真实路径和结论。

只完成代码时，状态写成 `code_complete_waiting_for_measurement`，不得写成 `complete`。

### 2.3 禁止提前实现的内容

- P1 没有确认 RAW 线性、重复性和 G1/G2 策略前，不实现正式五通道基底求解。Gate-1 已于 2026-07-16 以 conditional pass 解锁 P2。
- P2 没有得到实拍基底前，不实现依赖其具体维度或权重的 multipatch 求解器。
- P3 加法性没有结论前，不把 `y=Bu` 当成最终真值。
- P4 12 点 A/B 没通过前，不重算完整 70 点。
- P5 CCT 链没有形成明确结论前，不启动 Ray HSI 大网格。
- P6 没确认 Ray HSI 流形分支前，不写灯带 HSI 插值模型。
- 不得先写固定的 RAW/Hue/SAT 数值阈值，再用数据为它辩护。
- 不得覆盖默认 LUT、端点文件或现有最佳 70 点候选。
- 不得用本地 gphoto2 新拍数据补远程 run，也不得在同一 run 中混用 `local`/`remote` camera backend。
- 不得把 Token 写入 `plan.json`、`run.json`、命令日志、异常文本、测试 fixture 或提交；只记录 backend 名、base URL、API 路径和匿名化服务信息。
- 不得直接用带 Authorization header 的 `curl` 代替项目脚本；认证请求必须由脚本加载 `.env` 并发送。

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

### 3.5 远程相机合同

- 所有新采集使用 `camera_based_rgbww_optimizer.control.camera_remote.RemoteCameraBackend`；本地 `LocalCameraBackend` 仅用于兼容和测试。
- backend 从进程环境优先、项目 `.env` 次之读取 base URL 和 Token。正式 wrapper 不传 `--token`，不 `source .env`，不复制 Token 到子进程参数。
- 实机前先通过项目脚本调用无认证 `GET /health`，再通过同一脚本调用认证 `GET /v1/config`。两者的 base URL 都由脚本配置解析获得，shell 不自行读取 `.env`。health 通过但 config 失败时，按认证/相机占用失败处理，不能宣称相机可用。
- `GET /v1/config` 返回的 ISO、光圈和快门 choice 是当时唯一合法值。runner 必须精确使用返回字符串；当前远程镜头可能只提供 `implicit auto` 光圈，禁止硬编码本地路径的 `4`。
- `POST /v1/capture` 是同步请求并直接返回 CR3。每次只允许一个在途请求；不得创建任务、轮询状态或另行下载。
- `409 camera_busy` 只允许由 `camera_remote` 以有界次数重试完整请求。持续 busy、401、502 或 504 都停止当前 run，写 failure，执行双层关灯；不得无限重试。
- 禁止 Bulb。remote response 必须先写同目录临时文件，非空、完整关闭响应并 `os.replace` 后才登记 capture 成功；失败的 `.part` 必须删除。
- 相机端和树莓派不会保留第二份 CR3；本机成功落盘的 CR3 是唯一正式原片。写入 `captures.jsonl` 前必须确认文件存在、非空并计算 SHA-256。
- 自动曝光搜索的每一帧也通过同一个 remote backend；Ray 与 strip 继续使用两路独立快门缓存。远程化不能改变曝光目标、recorded exposure 解析和只亮一个光源的约束。
- 所有依赖相机的 runner 都要支持注入 backend 以便离线 fake 测试；不得在模块 import、plan 构建或 `--dry-run` 时加载 `.env` 或访问网络。

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
    "location_config": {
      "path": "config/location/locations-20260714-211759.json",
      "sha256": "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"
    },
    "raw_observer_config": {"path": "...", "sha256": "..."},
    "code_duty_curve": {"path": "...", "sha256": "..."},
    "baseline_lut": {"path": "...", "sha256": "..."}
  },
  "software": {},
  "devices": {
    "camera": {
      "backend": "remote",
      "base_url": "http://ibobby-rpi-4.local:8088",
      "api_document": "http://ibobby-rpi-4.local:8088/v1/API.md",
      "credentials": "loaded_by_script_not_recorded"
    }
  },
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
- `camera_backend=remote`、remote endpoint path、HTTP attempt 数和最终状态；不得记录 Authorization header 或 Token。

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
| P0-R | 新点位冻结、remote backend 接入全部实验 runner | remote backend 基础实现存在 | 全部离线测试、remote fake 集成和 dry-run 通过 |
| P1 | RAW 重复性、曝光线性、G1/G2、质量门槛 | P0-R 通过且用户批准远程实机 | 测量链 `pass` 或明确 `fail` |
| P2 | 五通道多档经验基底 | P1 `pass` | 单一/分段基底分支确定 |
| P3 | 随机混合加法性 | P2 有可用基底 | 主模型/初值模型/回退闭环分支确定 |
| P4 | 4x3 CCT multipatch A/B | P3 分支确定 | 12 点是否值得扩展有明确结论 |
| P5 | 14x5 全局 CCT/GM 和最终验证 | P4 全部门槛通过 | 安装或保留旧候选的结论完成 |
| P6 | Ray HSI 黑箱表征 | CCT 链已闭环 | HSI 流形分支确定 |
| P7 | 灯带 HSI 候选和 gamut | P6 模型确定 | INT=100 候选通过 |
| P8 | HSI INT 维度 | P7 通过 | 强度可分离或修正层确定 |
| P9 | CCT/HSI 最终独立验证 | 候选冻结 | 安装、回滚和审计完成 |

任何阶段 `fail` 都不能自动进入下一阶段。`conditional_pass` 必须按该阶段指定的受限路径继续，不能按 `pass` 处理。

### 5.1 执行角色

- **执行模型：** 完成当前阶段内已经定义的编码、测试、采集、分析、确定性重试和证据整理。不要因普通测试失败、可复现代码错误或阶段内已有明确处理规则而提前交还。
- **高级模型：** 只在阶段末决策门，或出现本合同 5.2 的高风险例外时介入；负责审阅证据、纠偏假设并选择下一阶段/回退路径。
- **用户：** 单独批准任何实机操作、高输出扫描、依赖变更、默认配置安装、提交和 push。高级模型的技术放行不替代用户授权。

### 5.2 允许提前中断的高风险例外

阶段内部原则上连续执行。只有以下情况可在阶段末之前中断并请求高级模型决策：

1. 需要修改公开验收阈值、统计口径、训练/留出边界或产品承诺。
2. 需要选择新的响应修正、非线性模型、额外交互项、依赖或数据维度，且当前阶段没有预先批准该分支。
3. 数据 provenance 不完整、location/hash 不匹配、训练与留出污染，继续会使实验结论无效。
4. 两个既定诊断分支给出互相冲突的结论，或现有数据不能区分会导致不同后续架构的假设。
5. 任何安全失败、设备状态不确定、双关灯不能确认、异常发热或电源异常。
6. 将候选安装为默认配置、覆盖基线、扩大到显著更昂贵的完整网格或开始新的产品线。

不属于提前中断理由：普通单测失败、格式错误、已知 API 适配问题、可在本阶段既定分支内修复的 bug、一次网络 busy、一次无效 capture。执行模型应修复、重试并保留证据。

### 5.3 阶段交接包

每个阶段到达决策门时，执行模型必须更新 `.agent-work/PLAN.md` 并提交一个不超过两页的交接摘要，至少包含：

- 当前 commit/dirty 状态和实际改动文件。
- 运行目录、输入 hash、分析文件和所有失败样本。
- 测试命令与通过/失败数量。
- 阶段出口判定及支持/反对证据。
- 未解决问题，且区分“会改变路线”和“可延后技术债”。
- 推荐分支、至少一个备选分支、各自成本和风险。
- 下一阶段第一条可执行命令；未获放行前不得执行。

高级模型必须明确写出 `approved_next_stage`、`repeat_current_stage`、`rollback_to_stage` 或 `stop_route` 之一，执行模型才能跨阶段。

---

## 17. 计划归档规则

当 P9 完成，或用户明确终止整个路线时：

1. 确保 `.agent-work/PLAN.md` 的状态、各阶段交接和最终分支真实完整。
2. 创建 `.agent-work/PLANS/{YYYYMMDD-HHMM}/`（若不存在）。
3. 将 `.agent-work/PLAN.md` 和整个 `.agent-work/PLAN/` 目录作为一个不可拆分计划包移动到该归档目录。
4. 不保留第二份活动 `PLAN.md` 或活动 `PLAN/` 阶段目录。
5. 只有用户明确要求时才提交归档文件。

在上下文压缩、任务恢复或换模型后，必须重新读取本文件；不得凭聊天摘要跳过硬门。
