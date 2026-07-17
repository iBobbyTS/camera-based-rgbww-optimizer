# 阶段 2：五通道经验基底与加法性

**覆盖原阶段：** P2、P3

**进入条件：** Gate-1 明确 `approve_stage_2`，并在总控状态中记录 P1 采用的 G1/G2、曝光 envelope 和质量阈值。

**阶段目标：** 用实拍确定五通道基底的维度、档位依赖、可辨识性和随机混合预测能力。

**不得跨越：** 未经高级模型选择主模型/seed-only/分段分支，不得实现 CCT multipatch pilot。

## 执行顺序

1. 实现并离线验证 P2 runner 与纯分析模块。
2. 获用户实机授权后完成五通道三档基底采集与分析；阶段内按既定 B-A..B-D 规则补充诊断。
3. 在 P2 允许继续的分支上实现 P3，并完成固定 24 命令、48 状态的加法性验证。
4. 对 rank、condition number、档位依赖、总负载和通道组合残差形成统一报告。
5. 到达 Gate-2 后停止；不得提前编写 P4 求解器来迎合某个模型结论。

## 高级模型决策门 Gate-2

这是前向模型架构选择门。高级模型必须在以下出口中明确选择：

- `linear_basis_primary`：P2 B-A 且 P3 M-A。
- `piecewise_basis_primary`：档位依赖经留出验证，采用 B-B/M-B。
- `rank_deficient_regularized_seed`：基底只作带先验初值。
- `load_or_interaction_correction`：仅在独立留出显著改善后批准最小修正项。
- `forward_model_seed_only`：P3 M-E，P4 只用实拍闭环。
- `repeat_or_stop_stage_2`：重复不稳定或模型无可验证价值。

决策必须冻结 feature 维度、basis schema、训练 patch、留出 patch 和允许的模型复杂度；阶段 3 不得自行改变。

---

## 8. P2：五通道多档经验基底

P2 到 P9 的所有相机操作无条件继承 2.1、3.5 和 6.5 的 remote backend、新点位及密钥边界。后续章节出现“拍摄/实拍/相机”时均指远程同步 capture；不得因为章节未重复 `--camera-backend remote` 就改用本地 gphoto2。

### 8.1 代码任务

仅在 P1 `pass` 或允许的 `conditional_pass` 后新增：

```text
src/camera_based_rgbww_optimizer/optimization/measure_chart_response_basis.py
src/camera_based_rgbww_optimizer/measurement/chart_response_basis.py
tests/test_measure_chart_response_basis.py
tests/test_chart_response_basis.py
```

测量 runner 负责设备和记录；measurement 模块只负责纯数据拟合。不得把设备调用塞进矩阵分析模块。

2026-07-16 离线实现状态：

- 已实现 `measure_chart_response_basis.py`、`chart_response_basis.py`、独立离线 analyzer 和 `tmp/run-chart-response-basis.zsh`。
- dry-run 固定为 58 张：ambient 1、五通道保护/弱曝光基线 10、anchor 基线 1、正式状态 45、anchor check 1。
- runner 强制 remote、最新 location、code-duty curve、identity RAW、四平面和 `1.0x..1.25x` exposure envelope；复用 P1 的 backend/native RAW/recorded-exposure/源隔离/Python cleanup，并另有 shell trap。
- 分析输出 level-specific basis、SVD/rank/condition、列夹角、bootstrap CI、feature weight、质量拒绝和跨档位 shape；不自动选择 B 分支。
- dry-run：`tmp/chart-response-basis/offline/p2-basis-offline-20260716-005428/plan.json`。
- 完整测试 `264/264` 通过；等待实机 P2。

2026-07-16 实机结果：

- run：`/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935`。
- 启动时间 `2026-07-16T06:59:35Z`，完成时间 `2026-07-16T08:25:24Z`；runner/wrapper log 为 run 同名 `.runner.log`/`.wrapper.log`。
- 实机前 all-off、remote health/config、Ray node-config/get-cct 全部通过；两灯读回关闭。
- 58/58 capture、CR3 和 measurement JSON 完整；全部 CR3 非空，58/58 使用 recorded exposure，无 `.npy` 或 `failure.json`。
- command 记录没有 `ray_on`，所有 strip capture 前均有 `ray_off`；Python 与 shell cleanup 均确认 ESPHome 五通道为 0、Ray intensity 为 0。
- 分析文件：run 下 `basis-analysis.json`。缺失的单通道低信号 cell 不再删除整条 feature：同通道其他档位可用时仅以 weight=0.25 填补矩阵诊断，三档均不可测时记为 censored zero/weight=0；两类 cell 都不进入跨档 shape 比较。
- 92 个 feature 的三档 basis 均 rank=5，condition number 为 `121.676/125.304/124.881`；最接近列始终为 CW/WW，夹角 `18.28..18.34` 度。
- 锚点 global scale 为 `1.000145`，shape drift P95=`0.001585`；重复 CV 多数低于 `0.2%`，R 在 4095 档 P95=`1.158%`。
- 所有通道均有稳定跨档 shape 差异超过重复性；例如 R 1024->4095 shape P95=`4.10%`、P95=`5.85 sigma`，CW/WW/G/B 也各有大于 3 sigma 的 feature。
- **高级模型分支：B-B。** `level_dependent_channels=[cw,ww,r,g,b]`，P3 使用 1024/2048/4095 三档线性或形状保持插值。condition 约 125 不构成 rank deficient，但基底在 P3 通过前只作带正则的物理预测，不解释为高精度唯一通道解。

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

2026-07-16 离线实现状态：

- 已实现 P3 runner、纯 measurement analyzer、冻结 basis/hash 的分析 CLI、shell 双关灯 wrapper 和针对性测试。
- 固定 24 个唯一命令覆盖 `dominant_with_weak=5`、`white_rgb=5`、`high_load=5`、`lut_nearby=5`、`latin_hypercube=4`；seed 只改变采集顺序，不改变命令集合。
- 每点两次独立 off/on；ambient 1、强/弱曝光基线 2、anchor baseline 1、正式 48、anchor check 3，共 55 张。
- P3 输入冻结 P2 `basis-analysis.json`，强制 location hash、remote、identity RAW、四 CFA plane、1.0x..1.25x envelope 和 rank-5 三档 basis。
- 分析按每通道码值在 1024/2048/4095 的 normalized column 间线性插值；P2 imputed/censored cell 的低/零权重传递到 P3 residual。
- 输出绝对响应、去 global scale 的 shape residual、P2/P3 联合 sigma、neutral/chromatic、plane、category、active-set、load 和 order 诊断；不自动选择 M 分支。
- 完整离线测试 `275/275`、compileall、diff-check 和 CodeGraph sync 通过；dry-run 为 `tmp/chart-basis-mixtures/offline/p3-mixtures-offline-20260716-0833/plan.json`。
- 首次实机目录 `p3-additivity-20260716-0245` 错把 preflight/PID 放在正式目录内，被共享 executor 的非空目录保护在 capture/点灯前拒绝；失败证据保留，shell 与 recovery all-off 均成功。
- retry1：`/Volumes/4T/temp/rgbww-optimizer/chart-basis-mixtures/p3-additivity-20260716-0245-retry1`，wrapper PID `27427`，P2 basis SHA-256=`5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1`。
- retry1 三分钟健康检查：PPID=1，capture/CR3/measurement 各 1，无 failure/.npy；第一张 strip 曝光基线记录 `ray_off -> off_wait -> strip_on -> settled -> capture_requested`。当前-thread 完成检查 heartbeat=`p3`。
- retry1 已于 `2026-07-16T10:13:39Z` 正常完成，`run.json status=complete`、capture `55/55`、无 `failure.json`，Python/shell cleanup 均存在。用户随后取消 heartbeat `p3` 并暂停项目；额外 `all-off-pause-confirmation.json` 再次确认 ESPHome 五通道为 0、Ray intensity 为 0。尚未执行 P3 离线分析或 Gate-2 裁决。

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

### 9.5 2026-07-16 P3 结果与 Gate-2

- run：`/Volumes/4T/temp/rgbww-optimizer/chart-basis-mixtures/p3-additivity-20260716-0245-retry1`；55/55 capture、55/55 recorded exposure、48 个正式 mixture、无空 CR3/`.npy`/failure，Ray 从未开启，双 cleanup 与暂停后的额外 all-off 均成功。
- 分析：run 下 `basis-validation.json`，SHA-256=`e1f70ffdc4831cc38ee1e2976c12a0ce386142871daa6ee7a77af7756ebd5cfe`；冻结 P2 basis SHA-256=`5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1`。
- 真实重复的 `previous_state` 不同，离线 analyzer 已修正为只校验稳定 context，并单独保留每次重复前态；已补回归测试。
- 24 点没有任何一点达到“至少 80% feature <=2 sigma”；sample shape P95 中位=`6.4318%`、总体 P95=`28.5676%`、最差=`62.7689%`，sigma P95 中位=`141.31`。
- 类别 shape P95：white+RGB 约 `5.16%`、high-load `13.56%`、Latin-hypercube `15.02%`、LUT-nearby `15.65%`、dominant+weak `56.32%`。
- shape P95 与总负载相关性仅 `-0.0736`、与顺序相关性 `0.1842`，不支持简单 load correction；误差跨类别和 active set 广泛存在。
- 四次锚点相对首帧最终 global scale=`0.99385`，去 scale shape P95=`0.2807%`，远小于 mixture 误差，排除整场热漂移/位置漂移作为主因。
- **Gate-2：M-E / `forward_model_seed_only`。** 不批准全局开环模型、load correction 或大量 interaction 项；P2 basis 仅可生成 P4 初值。P4 必须走 C-F，保留现有 bounded Jacobian、Broyden、secant 和 thermal rebase 的实拍闭环。

---
