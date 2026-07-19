# Stage 6 执行计划：Ray120c Camera-Observer HSI Match

**计划状态：** active

**Planner 最新决策日期：** 2026-07-18

**当前复验检查点：** `bb4554a9afd0ff8b5356766335ed232e7daa6e08`

**当前活动阶段：** Stage 6 / P7-R0K guarded physical pre-capture contract 离线收口

**当前阶段状态：** `offline_complete_waiting_for_planner_acceptance`

**下一条唯一动作：** Planner 复验第 8.7.46 节的 P7-R0K v9 readiness 与实现检查点。Executor 不得自行继续 `p7_strip_state_readback_preflight`、`p7_targeted_reference_repeatability_v2`、sentinel-v2 或任何后续阶段。在 Planner 另行明确授权前，不得连接设备、生成真实 CR3、读取 `.env`、执行真实 all-off、刷写 firmware、重跑 sentinel、执行 remaining 9、boundary、holdout、P8 或安装任何 LUT。

**上游依据：**

- `advisor/1/1.RESEARCH.md`
- `advisor/1/1.GUIDE.md`
- 用户在 2026-07-17 转述的本轮 Advisor 结论；该结论包含 `sentinel_4_then_9`、联合 99.73% coverage、full-scale policy 边界和 `keep_p8_locked_until_p7_holdout`，若与旧 GUIDE 文本冲突，以本轮结论和本计划为准。
- `.agent-work/PLAN/00-CONTRACT.md`
- `advisor/2/0.AUDIT/`

---

## 1. Executor 使用合同

### 1.1 必读顺序

每次恢复任务必须按顺序读取：

1. 本文件全文；
2. `.agent-work/PLAN/00-CONTRACT.md` 全文；
3. `advisor/1/1.GUIDE.md`、本文件顶部记录的最新 Advisor 结论和第 8.7 节的本轮覆盖决定；
4. `.agent-work/PLAN/06-STRIP-HSI.md`，仅作历史设计背景；与本文件冲突时以本文件为准；
5. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
6. `docs/README.md` 的 P6/P7、remote camera、RAW observer 和双关灯章节；
7. `git status --short`，保留全部已有改动；
8. 使用 CodeGraph 定位将修改的符号和调用路径，再读取 CodeGraph 未覆盖的 JSON、Markdown 和 shell wrapper。

### 1.2 Planner 与 Executor 边界

本文件已经完成算法方向和实验分支设计。Executor 可以自行完成：

- 当前阶段内的代码实现、单元测试、dry-run、确定性 bug 修复；
- 在获得当前有效实机授权后执行本计划明确列出的 named experiment；
- 普通网络 busy、弱信号重拍、局部 solver/rebase 和证据整理；
- 仅在本计划明确允许的分支内继续下一批次。

Executor 不得自行决定：

- 放宽 RAW observer、曝光包络、联合 coverage 或 guard band；
- 改变第 8.7 节冻结的 coordinate/observer/full-scale gamut 或 INT 产品语义；
- 把任何失败写成物理色域不可达；
- 回退 P6、重拍 106 点 Ray 网络或改用理论 HSL/HSV；
- 进入 P8；
- 安装或覆盖任何默认 LUT；
- commit、push 或创建 PR，除非用户另行明确要求。

### 1.3 高风险停止点

只有以下情况交还 Planner/Advisor：

1. P7-R0/P7-R1 无法得到可校准、正定且稳定的 v2 uncertainty/reference/repeatability artifact；
2. 需要改变 58-feature、identity RAW、`1.0x..1.25x` 或 `R/G1/G2/B`；
3. Sentinel 不满足第 8.5 节的自动放行条件；
4. 边界诊断需要新的产品语义或无法区分测量、求解和 full-scale policy；
5. P7 holdout 完成并到达 Gate-6；
6. 任何安装、P8、最终候选冻结或默认配置覆盖请求。

普通代码错误不得提前交还；修复后使用新 run 目录，保留失败证据。

---

## 2. 已冻结事实，不得返工

| 范围 | 冻结决定 | Executor 行为 |
| --- | --- | --- |
| P0-R | 新实拍统一 remote camera；`.env` 只由脚本读取 | 不回退 local gphoto2，不读取或输出 `.env` |
| P1 | identity RAW，per-source `1.0x..1.25x`，G-C 四平面 | 不安装 response correction，不合并 G1/G2 |
| P2 | B-B 分档五通道基底 | 只生成 seed，不当作全局真值 |
| P3 | M-E / `forward_model_seed_only` | 必须依赖实拍闭环，不增加全局 load/interaction 模型 |
| P4 | `keep_white_lut_diagnostic_only; stop_before_p5` | 不重算 CCT multipatch 70 点 |
| White LUT | 保留外置 white-only 70 点候选 | 不覆盖 `config/white/white-lut.json` |
| P6 | 106/106 完成；Gate-5=`full_periodic_2d_HB` | 不重拍，不回退 affine/HSL/HSV |
| P7 代码 | Ray 流形、uncertainty、objective、feedback、runner、analyzer 的所有权边界可保留 | 允许按 8.7 修改 target/solver 内部数学结构；禁止平行框架或重拟合 P6 |

### 2.1 冻结输入

- Location：`config/location/locations-20260714-211759.json`
  - SHA-256：`21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`
- RAW observer：`config/camera/raw-observer.json`
  - identity、四平面、`1.0x..1.25x`
- P2 basis：
  - `/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json`
  - SHA-256：`5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1`
- P6 run：
  - `/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/p6-ray-hsi-remote-20260717-0403-retry1`
  - `run.json` SHA-256：`1c208227e453992a443a782f57693d56adaa3752271f88254dd2a370d7d3a357`
  - `plan.json` SHA-256：`63f4b6127d94969a168d0c2894deff7b0e2c235d333dac8b2f2421fb220a20ce`
  - `ray-hsi-analysis.json` SHA-256：`39dc23229be42615669ae843773c1f04972802b54635ccf36b7ee2287d53e034`
- P6 frozen manifold：`config/hsi/ray-hsi-manifold.json`
  - 审计时 SHA-256：`20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34`
- P1 strip repeatability 来源：
  - `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/p1-d1-remote-full-1-16000-20260714-235121`
  - `/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/p1-d2-cross-day-holdout-20260715-2300-retry2`
  - 只使用各 run 内同状态重复的中心化 residual，不把跨日中心差当随机重复性。
- 当前最佳 white-only 70 点：
  - `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`
  - 仅保留，不安装。

### 2.2 P6 模型合同

- SAT0 共享颜色方向，但保留 Hue-dependent brightness scale；
- HSI 与 RGB endpoints 独立；
- Hue 使用周期分段线性，`360 == 0`；
- SAT 使用无过冲分段线性；
- 目标坐标使用冻结的 58 个共同 accepted native-Bayer feature；
- 不匹配绝对亮度；
- 高曲率区域：wrap `330..90` 的 SAT20/50/80/95，以及 Hue `240..330` 的 SAT20/50/80。

---

## 3. 本阶段可声明范围

P7 所有产物必须显式限定为：

```text
observer = fixed Canon R6 Mark III native Bayer
geometry = locations-20260714-211759
raw_response = identity
exposure_envelope = per-source 1.0x..1.25x
ray_intensity = 100
strip_policy = INT100 + full-scale active-channel
absolute_brightness_matched = false
```

允许的产品字段：

```text
s_exact_max_int100_fullscale(h)
boundary_bracketed_at_full_scale
gamut_compressed_int100_fullscale
```

禁止写成：

```text
physical_gamut
spectral_match
human_visual_match
universal_HSL
absolute_Ray_brightness_match
```

第 8.6 节以前的 `faithful` 是 v1 历史字段。新 run 禁止继续使用这个无限定词状态；目标复制、完整 observer 等价和失败原因必须分开记录。

新 run 的主状态必须互斥且保留原始原因：

```text
hsi_coordinate_equivalent
hsi_coordinate_unconfirmed
measurement_unreachable
uncertainty_unresolved
solver_budget_exhausted
reference_drift
boundary_bracketed_at_full_scale
```

另有独立证据字段，不得与主状态合并：

```text
observer_equivalent = true | false | unresolved
color_rendering_residual
reference_repeatability = pass | unresolved | fail
reference_center_compatibility = pass | unresolved | fail
```

状态解释：

- `hsi_coordinate_equivalent`：Hue/SAT 局部坐标在冻结的联合 99.73% region + guard band 内通过，并完成规定的 settled confirmations；SAT0 不检查 Hue；
- `hsi_coordinate_unconfirmed`：本轮未证明 HSI coordinate equivalent，但没有足够证据归入其他状态；
- `measurement_unreachable`：冻结 RAW/exposure 包络内无法得到合法 58-feature；
- `uncertainty_unresolved`：重复帧显示冻结噪声模型可能低估，或结果落入决策 guard band；
- `solver_budget_exhausted`：合法测量存在，但冻结轮数内没有得到可确认候选；
- `reference_drift`：当前 Ray block mean 与冻结 P6 exact-node center 不兼容，或当前会话 pre/post block 不兼容；
- `boundary_bracketed_at_full_scale`：只表示 INT100、full-scale active-channel policy 下已建立 coordinate-equivalent 下界和未确认上界，并完成 scale-relaxed 诊断。

`observer_equivalent=true` 只在完整 58-feature 的严格统计等价 region 通过时成立。`hsi_coordinate_equivalent` 可以在 `observer_equivalent=false` 时成立，但必须同时公开 `color_rendering_residual`；这表示复制 Ray 的 HSI Hue/SAT 路径，不表示跨材质光谱或完整显色等价。

Stage 6 不生成 `hue_unreachable` 或“物理不可达”结论。

---

## 4. 全局安全与数据合同

### 4.1 设备和光源

1. 新实拍只用 `RemoteCameraBackend`；
2. 每张 capture 前先 strip off，再 Ray off；
3. Ray frame：确认 strip off 后设置 Ray、精确 readback、capture、Ray off；
4. Strip frame：确认 Ray off 后设置 strip、capture、strip off；
5. ambient frame：两灯都 off；
6. Ray 和 strip 分别维护曝光 cache；不同 Ray HSI state 和不同 strip target 不共享 cache；
7. 每次捕获都记录 requested state、readback、source、purpose、previous state 和 exposure provenance；
8. 所有运行必须同时有 Python `finally` 和 shell `trap` 双关灯；
9. 不保存 `.npy`，保留非空 CR3、measurement JSON、commands/captures JSONL；
10. 任何 source-isolation 不确定、readback mismatch 或 cleanup 缺失都使整个 run 无效。

### 4.2 正式确认

每张正式 confirmation 必须独立执行：

```text
all sources off
wait 1 s
reapply exact command
wait 60 s
capture
source off
```

- 普通 pilot 点：3 张；
- boundary、scale-relaxed 诊断、Gate-6 候选、高曲率/近极限点：5 张；
- 3/5 张只用于检验冻结模型是否明显低估和证明重复通过；
- 同一 run 内不得据确认帧重估 sigma、重拟合 covariance 或放宽 guard band。

### 4.3 长任务

- 正式任务从独立 Terminal/进程启动，不依赖 Codex PTY；
- wrapper 在启动前 `cd` 到项目根；
- shell `trap` 覆盖 `EXIT INT TERM HUP`；
- 启动后做一次约 3 分钟健康检查；
- 长任务使用当前 thread 的单次 heartbeat，按预计完成时间唤醒；
- 禁止短间隔轮询、`sleep` 占用主线程或并发第二个硬件任务；
- 进程消失而 run 仍 running/缺 cleanup 时，立即独立 `all_off` 并保存 recovery 证据。

---

## 5. 代码所有权和计划产物

### 5.1 保留的模块边界

- `measurement/ray_hsi_manifold.py`：冻结 Ray 目标和实际 inverse/evaluator；
- 新增 `measurement/hsi_uncertainty.py`：输入分布、regularization、Monte Carlo、coverage/guard band；
- `optimization/hsi_objective.py`：joint decision 与词典序报告；
- `optimization/hsi_feedback.py`：有界局部反馈、probe、Broyden、rebase；
- `optimization/measure_strip_hsi_pilot.py`：target set、reference anchor、capture、安全、状态；
- `optimization/analyze_strip_hsi_pilot.py`：run/command/coverage/gamut 分支分析；
- `tmp/run-strip-hsi-pilot.zsh`：shell 双关灯；
- `config/hsi/strip-hsi-pilot.json`：实验政策；
- `config/hsi/strip-hsi-uncertainty.json`：v1 历史 artifact，必须保留原文件和 hash，只能复现第 8.6 节；
- 后续新增 `config/hsi/strip-hsi-uncertainty-v2.json`：只有第 8.7 节离线验收和定向实拍校准均通过后才能冻结；不得原位覆盖 v1；
- 后续新增 `config/hsi/rgbww-hsi-int100-fullscale-candidate.json`：只有 P7 holdout 完成后生成候选，Gate-6 前不安装。

不要创建平行采集框架，也不要复制 remote capture、RAW observer、bounded least-squares 或 all-off。

### 5.2 Uncertainty artifact 最低字段

以下字段描述 v1 历史 artifact；新 v2 除保留 provenance 外，必须按第 8.7.4--8.7.6 节拆分 reference、coordinate、observer 和 repeatability regions，不得复制 v1 的单一 `[Hue,SAT,orth]` joint region。

`config/hsi/strip-hsi-uncertainty.json` 至少包含：

```text
schema_version
status = offline_frozen_before_measurement
observer_scope
58 feature ids and SHA-256
all input paths and SHA-256
within-run repeat group ids/counts
feature transform = exposure-normalized then unit shape
regularization type and parameters
ray_repeatability_component
strip_repeatability_floor_component
interpolation_component by region/target kind
combined covariance recipe
Monte Carlo seed/sample count/convergence
SAT0 output dimensions
nonzero-SAT output dimensions
joint score definition
99.73% coverage limit
guard-band derivation and guarded acceptance limit
reference-drift region
confirmation policies 3/5
no post-measurement threshold update policy
```

### 5.3 Run 产物

每个真实 run 至少包含：

```text
plan.json
run.json
captures.jsonl
commands.jsonl
reference-anchors.jsonl
target-results.jsonl
coverage-evaluations.jsonl
failure.json when failed
all-off-python.json
all-off-shell.json
analysis.json
EXPERIMENT_SUMMARY.md
```

---

## 6. Phase A-v1：首次离线纠偏（历史）

**授权范围：** `offline_only`

**完成状态：** `pass_then_superseded_by_section_8_7`

本节记录 sentinel 前冻结的 v1 实现和证据。第 8.6 节暴露 reference endpoint 数值退化和 target 语义不成立后，本节不得再作为新实拍的放行依据；后续实现以第 8.7 节为准。

**禁止：** `/health`、`/v1/config`、`/v1/capture`、Ray、ESPHome、真实 all-off 调用。

### A0. 定向预检

- [x] 读取本计划、00-CONTRACT、GUIDE、skill、README；
- [x] `git status --short`，记录并保留已有改动；
- [x] 确认没有活动 calibration process，但不探测设备；
- [x] CodeGraph 定位 P7 五个模块、P1 repeatability、P6 analyzer 和 shared capture adapter；
- [x] 计算所有冻结输入 hash，未发现 drift；
- [x] 确认旧 13 点离线草案并将其纠偏为冻结的 `sentinel_4_then_9` schema v2。

### A1. 构造 58-feature 输入不确定度

实现单一 `hsi_uncertainty` 模块，不把 covariance 逻辑散入 objective/runner。

#### A1.1 统一变换

对 Ray 和 strip 的每个合法 measurement：

1. 严格按 frozen feature id 顺序提取 58 个值；
2. 使用已有 exposure-normalized、ambient-subtracted值；
3. 形成 58 维向量；
4. 单位范数归一化，与 `RayHsiManifold.coordinate()` 完全一致；
5. 所有重复性只在同 source、同 state、同 run 内中心化；
6. 不把不同 Hue/SAT、不同 strip command 或跨日中心漂移当随机噪声。

#### A1.2 三个组成项

总输入 covariance 只由以下三项组成：

```text
Sigma_match = Sigma_ray + Sigma_strip_floor + Sigma_interpolation
```

- `Sigma_ray`：P6 同 Ray state 独立 repeats 的 unit-shape residual；
- `Sigma_strip_floor`：P1 两个自然日 run 内同 strip state repeats 的 unit-shape residual，先分别中心化再 pool；
- `Sigma_interpolation`：P6 流形插值交叉验证 residual；
- 相机噪声已经包含在 Ray/strip 实拍重复性中，禁止添加第四个 camera-noise 项。

Reference drift 使用：

```text
Sigma_reference = Sigma_ray_frozen_center + Sigma_ray_current_capture + Sigma_interpolation
```

不得混入 strip component。

#### A1.3 正则化

58 维样本不足，不允许直接求完整样本 covariance 或直接求逆。

第一版固定采用**CFA-plane block-isotropic diagonal regularization**，不让 Executor 在多种 covariance estimator 中自行选择：

1. 对每个 component、每个 `R/G1/G2/B` plane，收集所有 within-group centered residual scalar；
2. `s_mad = median(abs(residual)) / 0.6744897501960817`；
3. `dof_plane = sum_group((n_group - 1) * valid_feature_count_in_plane)`，`s_rms = sqrt(sum(residual^2) / dof_plane)`；
4. `v_plane = max(s_mad^2, s_rms^2, 1e-12)`；
5. 同一 CFA plane 内的全部 feature 使用该 `v_plane`，不同 plane 独立，所有 off-diagonal 固定为零；
6. 每个 component 至少需要两个独立 repeat/CV group，且每个 plane 的自由度为正，否则 Phase A fail；
7. 输出每个 feature 的 raw sample variance、每 plane 的 MAD/RMS/final variance、group count 和 degrees of freedom，供审计；
8. 禁止求逆或保存未经正则化的 58 维样本 covariance。

该选择有意牺牲 feature-level correlation，以避免小样本高维 covariance 病态。不得为此新增大型依赖。若无法离线证明正定、稳定和 deterministic，标记 `uncertainty_model_blocked` 并交还 Planner。

#### A1.4 插值误差

- P7 13 个 pilot 节点如果恰好是 P6 实测网格节点，`Sigma_interpolation=0`；SAT0 pooled-zero 模型残差单独保留；
- 非节点、boundary 和 holdout 必须加入插值项；
- 用 P6 实测网格做离线交叉验证：
  - 交替 Hue 节点由相邻周期 Hue 预测；
  - 内部 SAT 节点由上下 SAT 预测；
  - regular 区和 Gate-5 高曲率区分层；
- 对目标使用所属区域的保守 regularized residual，不把全局平均用于高曲率区；
- 记录 exact-node、regular-interpolation、high-curvature-interpolation 三种 target kind。

### A2. Monte Carlo 联合 coverage 和 guard band

依据 JCGM 100/101/102 的原则，通过**实际** `RayHsiManifold.coordinate()` 与 objective evaluator 传播，不使用一阶 Hue/SAT 线性近似替代。

官方参考：

- `https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf`
- `https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf`
- `https://www.bipm.org/documents/20126/2071204/JCGM_102_2011_E.pdf`
- guard band/conformity：`https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf`

#### A2.1 输出向量

非零 SAT：

```text
z = [abs(hue_error_degrees), abs(sat_error_percent), orthogonal_residual]
```

SAT0：

```text
z = [abs(sat_error_percent), orthogonal_residual]
```

SAT0 禁止生成或检查 Hue gate；报告中的 Hue 必须为 `undefined/null`。

#### A2.2 单一联合判定

1. 从 `Sigma_match` 生成固定 seed 的 Monte Carlo null samples；
2. 把扰动加入目标 58-feature 向量并单位归一化；
3. 每个 sample 通过真实 inverse/evaluator 得到 `z`；
4. 对每个输出分量计算 `scale_j = max(q_0.6827(z_j), 1e-12)`；
5. 定义唯一 scalar：`joint_score = max_j(z_j / scale_j)`；
6. `coverage_limit = q_0.9973(joint_score_null)`；
7. 禁止把 Hue/SAT/shape 各自 3-sigma 后简单 AND；
8. 基础 Monte Carlo 使用每批 50000、至少 200000、最多 1000000 个 sample；累计 `coverage_limit` 连续三批相对变化低于 1% 才算收敛；
9. 固定 seed、批次、样本数、分位数算法和 convergence 结果写入 artifact。

每种 `target_kind` 和 evaluator 输出维度分别校准；不得把 SAT0 的二维 region、普通非零 SAT、regular interpolation 和 high-curvature interpolation 共用一个 limit。未来 boundary SAT 的 region 由冻结 covariance recipe、固定 seed 派生，生成的 target-specific limit/hash 在 capture 前写入 plan。

#### A2.3 Guard band

- guard band 必须在任何 P7 实拍前冻结；
- 对输入 repeat/CV groups 分层有放回 bootstrap 200 次；每次使用固定派生 seed 和 20000 个 Monte Carlo sample，重新得到 `coverage_limit_b`；
- `guarded_acceptance_limit = q_0.05({coverage_limit_b})`，即 bootstrap coverage limit 的单侧 95% 保守下界；
- 最终 `faithful` 必须满足 guarded limit；
- 位于 guarded limit 与 unguarded coverage limit 之间时标记 `uncertainty_unresolved`；
- 超过 coverage limit 时为非-faithful，但具体是 `unconfirmed`、`solver_budget_exhausted` 还是其他状态由阶段证据决定；
- artifact 必须保存 bootstrap 方法、seed、replicate count 和选择的单侧置信水平。

如果 bootstrap replicate 中任何 required plane 失去有效 group，丢弃该 replicate并记录；有效 replicate 少于 180/200 时 Phase A fail，不得降低 replicate 数通过。

#### A2.4 离线校准自检

- null Monte Carlo 的 empirical joint coverage 应与 99.73% 一致到预设数值容差；
- SAT0 测试必须证明 Hue 完全不参与 score；
- exact node 与插值 node 使用不同 uncertainty component；
- reference region 不得包含 strip variance；
- 任一 covariance 非有限、非正定、样本数不足或高分位不收敛：Phase A fail，不允许写正式 frozen artifact。

### A3. Objective 与 solver 接入

- [x] `evaluate_hsi_observation()` 改为读取冻结 uncertainty evaluator，不再接收默认为零的三个 strip 3-sigma；
- [x] 保留 Hue/SAT/orthogonal 数值作为报告与词典序方向；
- [x] `feasible` 只由 joint guarded decision 决定；
- [x] solver 排序优先：状态有效、Hue excess、SAT excess、joint score、orthogonal/shape、连续性；
- [x] SAT0 的排序删除 Hue；
- [x] feedback samples 保存 artifact hash、target kind、joint score、coverage/guarded limits；
- [x] confirmation 失败仍触发 thermal rebase，但不得更新 uncertainty；
- [x] 达到冻结轮数仍未确认时返回 `solver_budget_exhausted`，不自动增加轮数。

### A4. Target set、reference anchor 和确认策略

修改现有 runner，不创建新 runner：

```text
target_set = sentinel | remaining | boundary | holdout
```

#### A4.1 Sentinel 四点

```text
H0/S0
H120/S100
H120/S50
H300/S100
```

#### A4.2 Remaining 九点

```text
H0/S50
H0/S100
H60/S50
H60/S100
H180/S50
H180/S100
H240/S50
H240/S100
H300/S50
```

两组并集必须严格等于原 13 点，不能重复或漏点。每个 plan 写 target set、目标列表、父 run/hash 和 expected combined grid。

#### A4.3 当前会话 Ray anchors

每个真实 P7 acquisition session 在任何 strip candidate 前依次捕获：

```text
H0/S0
H120/S100
H300/S100
```

session 末再捕获：

```text
H120/S100
```

要求：

- strip 始终 off；
- Ray 命令后 exact readback；
- 每个 Ray state 独立曝光 cache；
- 与冻结 P6 target 用 `Sigma_reference` joint region 比较；
- 任一 pre-anchor 超出 unguarded 99.73% region：`reference_drift`，在点亮 strip 前停止；
- post-anchor 超出 region：整个 run 标为 `reference_drift`，target 结果仅作诊断，不得进入 Gate-6；
- 同一 run 不重拟合 P6、不移动 target center、不更新 Ray variance。

#### A4.4 Confirmations

- 普通 sentinel/remaining 节点：3；
- boundary、scale-relaxed、holdout 中高曲率/0-360、Gate-6 candidate：5；
- target metadata 必须在采集前写明 confirmation count，运行时不得因结果好坏减少；
- 每张都必须独立 off/on 60 秒；
- frozen spread check 若显示模型低估，状态为 `uncertainty_unresolved`，不得用这 3/5 张重估 artifact。

Frozen confirmation 判定固定为：

1. 3/5 张每一张的 match `joint_score` 都必须小于等于该 target 的 `guarded_acceptance_limit`；
2. uncertainty artifact 预先分别为 `n=3`、`n=5` 模拟独立 strip captures，使用 `2 * Sigma_strip_floor` 计算所有 pairwise unit-shape difference，并取该组最大 pairwise score；
3. 分别冻结 `repeat_spread_limit_3` 和 `repeat_spread_limit_5` 的联合 `q=0.9973`；
4. 实拍 3/5 张的最大 pairwise score 超出对应 limit 时为 `uncertainty_unresolved`；
5. 不对实拍 confirmation 求新 variance，不把平均后通过替代逐张通过。

### A5. Full-scale 与 scale-relaxed 诊断

- 正式 product policy：`max_code=4095` 且至少一个 active channel 固定 4095；
- 非-faithful full-scale 点在写成边界前，必须同 Hue/SAT 运行 `max_code=3072`；
- 3072 仍不能区分时，可按 plan 运行 `max_code=2048`；
- scale-relaxed 点仍保持“至少一个 active channel=max_code”；
- scale-relaxed 只作诊断，不进入 INT、不写入 full-scale runtime LUT；
- 降尺度后 faithful：证明的是 full-scale mixing policy 边界，不是物理色域边界；
- 3072/2048 都未证明 faithful：保持 `unconfirmed` 或其他具体状态，不得写物理不可达。

### A6. Analyzer 和 command audit

Analyzer 必须把以下作为 hard gate：

- declared target set 完整且无额外 target；
- parent/uncertainty/manifold/location/observer/basis hash 一致；
- 每个 capture 有非空 CR3、measurement JSON 和 recorded exposure；
- 无 `.npy`；
- Python/shell cleanup 各两步且均 `ok=true`；
- `commands.jsonl` 每个 capture group 顺序合法；
- 不存在 Ray 与 strip 同时 on；
- Ray command/readback 精确一致；
- strip requested/response 一致；
- reference anchors 完整；
- confirmation 数等于预声明 3 或 5；
- uncertainty artifact hash 在 run 内不变；
- 任一审计失败使 run invalid，不进入数值聚合。

Analyzer 不再使用旧字段：

```text
boundary_below_50_or_hue_unreachable
s_exact_max
gamut_clipped
```

改为 full-scale scoped 字段，并保留所有非-faithful 状态。

### A7. 测试矩阵

至少新增或更新：

1. 58-feature 顺序/hash；
2. within-run center，禁止跨日 center 当 noise；
3. Ray/strip/interpolation covariance 组合且 camera noise 不重复；
4. diagonal CFA-plane shrinkage 正定、确定性和低样本分支；
5. exact node interpolation=0、regular/high-curvature 非节点有不同项；
6. Monte Carlo 固定 seed 和 convergence；
7. empirical joint 99.73% coverage；
8. 三项独立 3-sigma AND 不再作为 feasibility；
9. SAT0 无 Hue gate；
10. guard band 在实拍后不可变；
11. reference region 不含 strip covariance；
12. sentinel/remaining 恰好 4+9=13；
13. pre/post Ray anchors 和 readback mismatch；
14. 3/5 confirmations、独立 off/on 60 秒；
15. confirmation 不更新 sigma；
16. 七种状态互斥；
17. solver budget 不自动扩张；
18. max_code 4095/3072/2048 active-channel 约束；
19. command/source-isolation audit；
20. Python/shell cleanup；
21. dry-run 不加载 `.env`、不联网、不调用设备；
22. combined 13 点 analyzer、boundary 和 holdout synthetic branches。

### A8. 离线验收与代码检查点

执行：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q src tests
zsh -n tmp/run-strip-hsi-pilot.zsh
git diff --check
codegraph sync
```

然后生成全新的 dry-run 和：

```text
tmp/strip-hsi-pilot-offline/<id>/plan.json
tmp/strip-hsi-pilot-offline/<id>/uncertainty-validation.json
tmp/strip-hsi-pilot-offline/<id>/offline-readiness.json
```

`offline-readiness.json` 记录：

- 当前 `HEAD`；
- worktree diff SHA-256；
- 所有冻结输入 hash；
- uncertainty artifact hash；
- full test count/exit status；
- compileall、wrapper syntax、diff-check、CodeGraph 状态；
- dry-run 无设备调用断言；
- 唯一下一动作=`run_sentinel_4`。

若用户没有明确要求 commit，代码检查点只记录 hash，不提交。

Phase A 全部通过后，把本文件状态更新为：

```text
current_phase = B
stage_status = code_complete_waiting_for_sentinel_authorization
next_action = preflight_and_run_sentinel_4
```

### A9. Phase A 执行结果（2026-07-18）

```text
status = pass
uncertainty_artifact = config/hsi/strip-hsi-uncertainty.json
uncertainty_artifact_sha256 = cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94
formal_run_dir = tmp/hsi-uncertainty-formal/p7-phase-a-20260717-2048-retry3
offline_checkpoint = tmp/strip-hsi-pilot-offline/p7-phase-a-final-20260718-040551
offline_readiness = pass
full_test_suite = 345 tests, exit 0
compileall = pass
wrapper_syntax = pass
git_diff_check = pass
codegraph_sync = pass
device_calls = 0
capture_count = 0
next_action = wait_for_named_experiment_authorization_then_run_sentinel_4
```

后台托管审计：正式 artifact 确定性成功写入两次；`launchctl submit` 的 keepalive 又启动了第 3 次冗余计算。Executor 停止冗余进程、保留 `redundant-run-interruption.json` 与 `post-stop-safety-audit.json`，并补充 Python `SIGTERM/SIGHUP` finally 路径及 shell 先记安全证据的回归覆盖。artifact 在停止前后 hash 未变化。

---

## 7. Phase B-v1：首次 Sentinel 实机前检查（历史）

本节已执行完毕，对应授权已经消费。不得据此再次连接设备；P7-R1 和 sentinel-v2 必须使用第 8.7 节的新 named experiment、全新 preflight 和全新 run 目录。

### 7.1 已消费的 Planner 验收与授权（2026-07-17）

```text
planner_acceptance = pass
authorization = named_experiment
experiment_id = p7_sentinel_4
authorized_scope = Phase B preflight + Phase C sentinel_4 + 计划内有界高输出
authorized_target_set = sentinel
authorized_targets = H0/S0, H120/S100, H120/S50, H300/S100
authorized_reference_anchors = pre H0/S0, H120/S100, H300/S100; post H120/S100
authorized_max_code = 4095; 仅按既定失败分支允许 3072/2048 scale-relaxed 诊断
excluded_scope = remaining 9, boundary, holdout, Gate-6 自动选择, P8, LUT 安装或默认配置覆盖
```

验收证据：

- `config/hsi/strip-hsi-uncertainty.json` SHA-256 为 `cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94`，状态为 `offline_frozen_before_measurement`；
- manifold、location、observer、P2 basis 与 Phase A 记录的冻结 hash 一致；
- Planner 复跑完整测试 `345/345` 通过，`compileall`、两个 wrapper 的 `zsh -n`、`git diff --check` 和 `codegraph sync` 通过；
- Planner 独立 dry-run：`tmp/strip-hsi-pilot-offline/p7-planner-acceptance-20260717/plan.json`，严格为四点、普通点各 3 次确认、remote backend、三前一后 Ray anchors 与 Python/shell 双 cleanup；
- 验收阶段未读取 `.env`、未访问 remote camera、Ray120c 或 ESPHome，未执行真实 all-off，也未产生 CR3 或 `.npy`；
- 验收时未发现遗留 calibration/uncertainty runner 进程。

该授权只有在冻结 artifact、代码检查点和输入 hash 未漂移时有效。任一 Phase B 检查失败时授权自动停止在 preflight，不得开始拍摄；必须保存证据并确认双灯关闭。

顺序固定：

1. 确认无 calibration/相机进程和无活动 heartbeat；
2. 运行共享 `control.all_off`，保存 preflight 结果；
3. remote `health`；
4. remote authenticated `config`，由脚本读取 `.env`；
5. Ray node-config/get-current-state；
6. ESPHome 可达性和全通道零状态；
7. 再次双灯 off；
8. 校验 location、observer、basis、manifold、uncertainty、pilot config、wrapper 和 worktree hash；
9. dry-run target set 必须是 sentinel 四点；
10. 创建全新外置 run 目录，不在正式目录预写 PID/preflight 文件；
11. 使用独立 Terminal 启动 wrapper；
12. 3 分钟健康检查后创建单次 heartbeat。

任一步失败：不实拍或立即停止，按失败合同保存证据和双关灯。

---

## 8. Phase C-v1：首次四点 Sentinel（历史）

### 8.1 Run 目录

```text
/Volumes/4T/temp/rgbww-optimizer/strip-hsi-pilot/p7-sentinel-4-<timestamp>
```

### 8.2 采集顺序

1. ambient；
2. pre Ray anchors：H0/S0、H120/S100、H300/S100；
3. 若 anchor 均在 frozen reference coverage 内，执行 strip sentinel；
4. strip H0/S0；
5. strip H120/S100；
6. strip H120/S50；
7. strip H300/S100；
8. 对需要的非-faithful S100 做 3072，必要时 2048 诊断；
9. post Ray anchor：H120/S100；
10. Python cleanup；
11. shell cleanup；
12. 离线 analyzer。

采集顺序可以为热平衡做预先冻结的排列，但 target 集、每点 confirmations 和首尾 anchors 不得变；最终顺序必须写入 `plan.json`。

### 8.3 每点结果

每点必须输出：

- target Hue/SAT/INT/policy；
- 58-feature target hash；
- basis seed 和 predicted residual；
- active channel；
- 全部 probe/feedback/backtrack/rebase；
- joint score、coverage/guarded limit；
- Hue/SAT/orthogonal 报告值；
- confirmation 3/5 张及 frozen spread check；
- selected command；
- white/rgb sensor contribution；
- condition/sensitivity；
- 七种状态之一；
- scale-relaxed diagnostics。

### 8.4 Sentinel v1 自动放行条件（历史，不得复用）

以下条件只解释第 8.6 节为什么没有自动放行。第 8.7 节已覆盖本条；任何新 sentinel 均必须重新经过 Planner 验收和明确 named-experiment 授权。

1. pre/post Ray anchors 全部通过，无 `reference_drift`；
2. run、CR3、recorded exposure、command audit、双 cleanup 全部有效；
3. H0/S0=`faithful`；
4. H120/S50=`faithful`，证明中间 SAT 路径可工作；
5. H120/S100 与 H300/S100 中至少一个在 full-scale 下 `faithful`；
6. 另一个若 full-scale 非-faithful，必须有合法测量、稳定 best candidate，并在预声明 3072 或 2048 诊断下 `faithful`；该诊断只证明 full-scale policy 影响，不提前声明 SAT boundary；
7. 四点都没有 `measurement_unreachable`、`uncertainty_unresolved` 或 `solver_budget_exhausted`；
8. confirmation 没有显示 uncertainty 明显低估；
9. Jacobian/feedback 没有连续失准且未被 rebase 解释；
10. captures/round、运行时间和失败率足以支持剩余 9 点。

### 8.5 Sentinel v1 分支（历史）

#### S-PASS

满足 8.4：

- 冻结 sentinel analysis/hash；
- 更新本计划；
- 进入 Phase D；
- 不改 uncertainty、轮数、guard band 或 target 语义。

#### S-CODE-REPEAT

出现明确代码、provenance、命令审计或可复现实现 bug：

- 保留失败 run；
- 确认双关灯；
- 离线补回归测试并修复；
- 全套测试；
- 使用新目录完整重跑四点；
- 不只重跑通过点。

#### S-REFERENCE-DRIFT

任一 anchor 超出 coverage：

- 立即停止并双关灯；
- 标记整个 run `reference_drift`；
- 不重拟合 P6；
- 不继续 remaining；
- 交还 Planner/Advisor决定是否另日重复或重新表征 Ray。

#### S-UNCERTAINTY

出现 `uncertainty_unresolved`：

- 不在同一 run 重估 sigma；
- 停止 remaining；
- 只允许设计新的定向 repeatability 实验；
- 交还 Planner/Advisor。

#### S-MEASUREMENT

出现 `measurement_unreachable`：

- 不扩大 `1.25x`；
- 保留 rejected feature 和 capture；
- 停止 remaining；
- 交还 Planner/Advisor决定缩小 feature/范围或另做测量设计。

#### S-SOLVER

出现 `solver_budget_exhausted` 或 scale-relaxed 也无法证明闭环工作：

- 不在同一 run 增加轮数；
- 分析 seed、active channel、Jacobian condition、step/backtrack 和 rebase；
- 若是普通代码错误走 S-CODE-REPEAT；
- 若需改变 solver/目标架构则交还 Planner/Advisor。

### 8.6 Sentinel 实机结果（2026-07-18）

```text
run_dir = /Volumes/4T/temp/rgbww-optimizer/strip-hsi-pilot/p7-sentinel-4-20260717-223108-retry2
run_status = complete
capture_count = 100 CR3 / 100 recorded-exposure measurements
command_count = 399
reference_anchors = 3 pre + 1 post
failure_json = absent
npy_count = 0
python_cleanup = pass; ESPHome five-channel zero + Ray intensity 0
shell_cleanup = pass; ESPHome five-channel zero + Ray intensity 0
input_validation = 7/7
source_isolation = pass
requested_response_consistency = pass
analysis = analysis.json @ 5416dfcae4ea1f4114d1757a0d253b059677a984f728a7f10a8dd81cd265e043
faithful_points = 0/4
H0/S0 = solver_budget_exhausted; full-scale joint 150.901 > guarded 5.645
H0/S0@3072 = uncertainty_unresolved; repeat spread 22.964 > 4.372
H120/S100 = uncertainty_unresolved; repeat spread 6.657 > 4.397
H120/S50 = uncertainty_unresolved; repeat spread 4.721 > 4.397
H300/S100 = uncertainty_unresolved; repeat spread 8.822 > 4.397
automatic_release = false
branch = S-UNCERTAINTY + S-SOLVER
```

Analyzer 的机械审计报告 `reference_drift=false`，但非零 SAT reference calibration 的 SAT component scale 被下限夹到 `1e-12`，使 coverage limit 膨胀到约 `1.9388843165e11`。因此三个非零 anchor 的 `within_reference_coverage=true` 不能作为有信息量的无漂移证明；SAT0 anchor 的有限门槛仍有信息量。修改该 reference region、统计 floor 或输出维度会改变实拍前冻结的 uncertainty/reference policy，Executor 不得用本 run 后验调整，必须交还 Planner/Advisor。

证据摘要：

- `EXPERIMENT_SUMMARY.md`：同一 run 目录；
- `run.json` SHA-256：`2a6cf9147c322b1a0913d059007150d0b05ca2491e6aa620e11522616fed422b`；
- `plan.json` SHA-256：`02d2dfa913ce5983cabc777b975a8b0323151ea56ce307eaf763b42ae93e92bf`；
- Python cleanup SHA-256：`9382ac8158b6c721971733d71c64b51043f9fa474a4c8444041a6020ebd91f14`；
- shell cleanup SHA-256：`3ba1586be9a203596a40a0800b7487ab114451ae9b0f788b5b5d2afa10c51090`。

在 Planner/Advisor 新决定前，禁止 remaining 9。不得把任何点写成物理 gamut、不得据 confirmation 更新 sigma、不得在同一 run 增加 solver 轮数，也不得进入 P8。

### 8.7 Planner/Advisor 覆盖决定：P7-R0 / P7-R1（2026-07-18）

本节是第 3、5、6、7、8.4、8.5 节中所有 v1 uncertainty、reference、`faithful` 和 solver acceptance 文本的最新覆盖决定。Executor 不得把新旧规则混用。

#### 8.7.1 结论与当前 run 处置

```text
planner_decision = redesign_before_more_measurement
allow_target_architecture_change = yes, within existing module boundaries
allow_solver_architecture_change = yes, offline-first and bounded
allow_more_rounds_in_existing_run = no
allow_fit_from_sentinel_confirmations = no
allow_remaining_9 = no
allow_p8 = no
current_sentinel_gate6_eligibility = invalid
current_sentinel_use = diagnostic_holdout_only
next_stage = P7-R0_offline_v2
authorization = offline_only
```

第 8.6 节 run 的机械完整性、100 张 CR3、命令审计和双关灯证据仍有效，不删除、不改写。它不能进入 Gate-6，原因不是事后正式宣判四个点均 `reference_drift`，而是 v1 reference gate 对非零 SAT 没有信息量，因而该 session 没有可信的“与冻结 P6 兼容”证明。新 v2 规则冻结后，本 run 只能作为完全独立的诊断 holdout，不能用于拟合 covariance、scale、coverage、guard band、产品阈值或 solver budget。

#### 8.7.2 本轮证据和方向判断

对第 8.6 节 confirmation 直接在冻结顺序的 58-feature unit-shape 空间计算最大 pairwise L2：

| 点 | max pairwise L2 | 到 Ray target 的稳定距离 |
| --- | ---: | ---: |
| H0/S0 @4095 | 0.0002897 | 约 0.17338 |
| H0/S0 @3072 | 0.0013620 | 0.17228..0.17349 |
| H120/S100 @4095 | 0.0004392 | 0.16979..0.17014 |
| H120/S50 @4095 | 0.0003922 | 0.17092..0.17117 |
| H300/S100 @4095 | 0.0022908 | 0.18014..0.18056 |

P1 两日 strip repeatability 的 direct pairwise L2 max 分别约 `0.0007726`、`0.0007764`，P95 分别约 `0.0007375`、`0.0007716`。因此：

- H120/S100 与 H120/S50 比 P1 floor 更稳定，v1 的 `uncertainty_unresolved` 是 nonlinear output-coordinate 放大造成的 false positive；
- H300/S100 与 H0/S0@3072 的局部变化确实高于 P1 white-state floor，必须由预声明的定向 repeatability 实验表征；
- 五点到 Ray target 的 58-feature 距离稳定在约 `0.17..0.18`，而 v1 orthogonal noise scale 约 `0.0011`；v1 joint score 约 150 几乎完全由跨光源 color-rendering residual 主导，单纯增加 solver 轮数不能跨越两个数量级。

当前 Ray anchor 到冻结 P6 exact-state 样本中心的 direct L2 约 `0.00749..0.00880`；P6 内部同状态 pairwise 证据约为：H0/S0 最大 `0.00196`、H120/S100 `0.000473`、H300/S100 `0.003755`。使用既有 `2*Sigma_ray` 做的简单 direct-feature 诊断得到当前 anchor score `16.7..21.7`，而相应 99.73% limit 约 `4.0`。这不是可用于追溯判定的 v2 正式门，但足以证明不能接受 v1 的 `reference_drift=false`。

SAT100 null Monte Carlo 中，冻结 inverse 的 SAT 输出因为 `[0,100]` clipping 有约 `71.24%` 恰好为零，导致 `q0.6827(abs(SAT error))=0`；v1 把 scale 夹为 `1e-12` 后产生约 `1.94e11` 的 coverage limit。该退化是 endpoint 坐标结构问题，不是增加 Monte Carlo 样本或换 seed 可以解决的问题。

#### 8.7.3 冻结新的目标语义

P7 的首要产品目标按 GUIDE 恢复为复制 Ray 的观测 Hue/SAT 路径，完整 58-feature 等价作为更严格且独立的证据：

1. `hsi_coordinate_equivalent`：只对 target-local Hue/SAT coordinate 做联合 99.73% + guard-band acceptance；SAT0 仅 SAT/neutral coordinate，不执行 Hue gate；
2. `observer_equivalent`：对完整 58-feature direct residual 做严格联合 region；它不得被删除或用 Hue/SAT pass 替代；
3. `color_rendering_residual`：保存 target tangent 正交补上的 raw L2、whitened score、per-plane/per-patch 摘要；作为 solver 第三优先级和公开诊断，但当前阶段不作为 `hsi_coordinate_equivalent` 的 hard gate；
4. 禁止再输出无前缀的 `faithful`。下游 `s_exact_max_int100_fullscale(h)` 与 boundary 只基于 `hsi_coordinate_equivalent` 建立，并同时携带 `observer_equivalent` 和 color-rendering evidence；
5. 不新增主观 Hue/SAT 产品容差。coordinate acceptance 仍由 capture 前冻结、独立校准的 measurement region 决定；若以后需要视觉容差，必须再次交还 Advisor，不能由 Executor自行设定。

这是基于新实拍证据对旧 joint Hue/SAT/orth hard gate 的明确覆盖，不是隐藏或删除 0.17..0.18 的显色差异。

#### 8.7.4 Reference calibration v2

Reference gate 不再通过 `RayHsiManifold.coordinate()` 的 `[Hue,SAT,orth]` 输出判定。对每个 exact anchor state `s`：

```text
u = unit_shape(ordered_58_features)
mu_p6_s = frozen P6 exact-state empirical center
delta_center = mean(u_current_block) - mu_p6_s
delta_session = mean(u_post_block) - mean(u_pre_block)
```

必须分别校准和报告两个 direct-feature statistic：

- `reference_center_compatibility`：P6 center 与当前 pre/post block mean 是否兼容；
- `reference_repeatability`：当前 pre/post block 是否相互兼容且 block 内 repeatability 是否稳定。

实现合同：

1. 使用 frozen 58-feature 顺序、unit-shape 和 CFA-plane block-isotropic diagonal regularization；不得求病态完整样本 covariance；
2. exact anchor 使用 P6 原始 exact-state repeated measurements 的经验中心，不通过 manifold interpolation 产生中心；exact-node interpolation component 为零；
3. P6 和当前 block 必须各自在 state/block 内中心化后估计 within-state covariance；跨 session center shift 是被检测量，禁止吸收到 variance；
4. mean-difference covariance 按独立均值的 `Sigma_p6/n_p6 + Sigma_current/n_current` 组合；pre/post 使用 `Sigma_pre/n_pre + Sigma_post/n_post`；不加入 strip covariance，也不额外重复加入 camera noise；
5. statistic 固定为 direct 58-feature regularized whitened norm，并通过 unit-normalization 后的实际 Monte Carlo 路径校准，不使用逆 HSI 坐标近似；
6. 每个 anchor state 分别给出 guarded 与 unguarded 99.73% limit：小于 guarded 为 `pass`，guarded 与 unguarded 之间为 `unresolved`，超过 unguarded 为 `fail/reference_drift`；
7. artifact 必须区分 within-session repeatability 与 frozen-center compatibility，不能用稳定但已漂移的 current center 让自己通过；
8. 未来正式 P7 session 的 pre anchors 每 state 至少 3 次独立 off/on settled captures，post 至少再次拍 H120/S100 3 次；单帧 anchor 禁止放行；
9. 同一 acquisition run 内任何失败都不得重拟合 P6、移动 center 或创建新 epoch。

#### 8.7.5 Strip repeatability v2

Confirmation spread gate 改在 direct 58-feature unit-shape 空间工作，不再对 nonlinear `[Hue,SAT,orth]` 输出做 pairwise spread：

```text
d_ij = unit_shape(x_i) - unit_shape(x_j)
Sigma_pair_class = 2 * max_per_plane(Sigma_P1_floor, Sigma_targeted_class)
T_repeat = regularized_whitened_norm(d_ij)
group_score_n = max_all_pairs(T_repeat)
```

Monte Carlo 必须分别模拟 `n=3`、`n=5` 并冻结 group maximum 的 99.73%/guarded limits。P1 仍是不能降低的 strip noise floor；定向数据只能逐 plane 提高相应 class 的 component，不能让 floor 变小。

v2 至少分四类：

```text
neutral_fullscale
mid_sat_fullscale
sat100_fullscale
neutral_scale_relaxed
```

SAT100 的 H120/H300 command 分别中心化，class variance 逐 CFA plane 取两者和 P1 floor 的保守最大值；禁止把两者 center 差当 noise。当前 sentinel confirmations 不参与拟合，只用于 v2 完成后的 holdout replay。

#### 8.7.6 非零 SAT endpoint-safe evaluator

冻结 P6 artifact 和 observed manifold 不重拟合。新增 target-local evaluator，和全局 inverse 分工：

- 全局 `RayHsiManifold.coordinate()` 继续用于导航、可视化和粗报告；
- acceptance 使用冻结 target 附近的局部 tangent basis；Hue 为周期 central tangent；内部 SAT 为双侧 tangent；SAT100 使用指向最近较低实测 SAT 节点的 one-sided tangent，但输出保持 signed/unclipped；
- SAT0 使用 neutral/radial coordinate，Hue 始终 undefined；
- 正交补 residual 形成独立 `color_rendering_residual`，不得重新塞回 coordinate joint gate；
- component scale 使用 endpoint-safe signed output 的 `q0.6827(abs(error))` 或等价 RMS；具体二选一必须由 deterministic synthetic/null tests 固定，不能按实拍结果选择；
- artifact generation 遇到任一 required scale 非有限或小于数值可辨识阈值时必须 hard fail。删除 `max(scale, 1e-12)` 这种让病态 region 继续生成的逃生路径。

局部 evaluator 的实现公式固定为：

```text
r = unit_shape(observation) - unit_shape(target)
J = [du/dh, du/ds]                       # SAT0 只保留 du/ds
W = inverse(regularized diagonal Sigma_match)
delta = solve(J^T W J, J^T W r)          # signed, never clipped to HSI bounds
r_orth = r - J delta
```

- `du/dh` 使用冻结 P6 相邻实测 Hue 节点的周期 central secant，单位为 feature/degree；
- 内部 SAT 的 `du/ds` 使用相邻实测 SAT 节点双侧 secant；SAT100 使用最近较低实测 SAT 到 100 的 one-sided secant，单位为 feature/percent；
- Hue error 报告为最短周期 signed degree；SAT error 允许越过 0/100 的 signed local value，禁止 clamp；
- `Sigma_match = Sigma_ray + Sigma_strip_class + Sigma_interpolation`；相机噪声已包含在前两项中，不新增独立 camera component；
- coordinate region 通过同一 evaluator 的 Monte Carlo `delta` 校准；observer region 对 direct `r` 校准；`r_orth` 只进入 color-rendering evidence/solver tie-break；
- 每个 target 保存 `cond(J^T W J)`。非有限或超过离线 synthetic test 冻结的 condition limit 时标 `uncertainty_unresolved`，不得退回 clipped global inverse 获得 pass；
- Hue/SAT tangent step、condition limit、regularization、MC seed/样本数和 scale estimator 全部写入 v2 artifact，并在任何新 capture 前固定。

Executor 首选 signed local tangent + `q0.6827(abs(error))`。只有离线 null test 仍证明分布退化时，才可在同一离线阶段改用预先记录的 RMS 方案，并在交还 Planner 时明确报告；不得自行进入实拍。

#### 8.7.7 允许的 solver/target 改造边界

允许修改 `hsi_objective.py`、`hsi_feedback.py` 和现有 runner/analyzer 的内部求解合同，也允许在既有 manifold 模块暴露只读 tangent/evaluation helper；不允许创建平行 manifold、采集框架或重拟合 P6。

允许：

1. objective 词典序固定为：合法 measurement、coordinate guarded excess、Hue/SAT signed local error、directional color-rendering residual、连续性/headroom/sensitivity；
2. solver 使用 whitened directional 58-feature residual 或 tangent/orthogonal projection，禁止只给 Jacobian 一个无方向的 orthogonal scalar norm；
3. 离线评估 P2 保存的全部五个 active-channel seed；正式 runner 最多使用多少 distinct-face starts 和总 capture budget，必须由 replay 报告提出并在新 named experiment 前由 Planner 冻结；
4. 在尚未 feasible 时，也允许依据 prediction error、Jacobian condition 或连续两次 bracket/secant 失准触发 deterministic rebase；
5. 保留 bounded step、backtrack、command limits、active-channel/full-scale policy 和每次实拍前冻结的总轮数；
6. 使用第 8.6 节完整 trace 做离线 replay/反事实分析，但不得把它用于 acceptance calibration。

禁止：

- 只把 `max_rounds` 调大后重拍；
- 为让旧点通过而调 threshold、guard band、feature set、observer 或 exposure envelope；
- 引入无法解释的 learned black-box forward model；
- 删除或隐藏 color-rendering residual；
- 将 top-K multi-start 变成无界搜索；
- 在新实拍中观察结果后增加 start、probe、round 或改变 objective。

#### 8.7.8 P7-R0：Executor 纯离线实施清单

授权仅为 `offline_only`。按顺序完成：

1. 保留 v1 artifact/hash 和第 8.6 节 run 原样；实现 schema v2 reader/writer，不覆盖 v1；
2. 实现 direct-feature reference center/repeatability evaluator及 block-mean covariance；
3. 实现 direct-feature confirmation spread 和四类 covariance 路由；在没有 P7-R1 数据时 artifact 状态只能是 `waiting_for_targeted_measurement`，不得伪造正式 limit；
4. 实现 endpoint-safe local coordinate、SAT0 无 Hue、observer/coordinate/color-rendering 三层输出；
5. 更新 objective、feedback、runner、analyzer 的状态和 provenance；旧 run analyzer 必须保持可复现，或显式使用 `--policy-version v1`；
6. 实现有界 multi-seed/rebase 架构，但只做 synthetic 与第 8.6 节 trace replay，不调用设备；输出每点 predicted/actual step、Jacobian condition、rebase 原因、各 seed/face、预计 capture budget；
7. 生成新的 named-experiment dry-run schema：`p7_targeted_reference_repeatability_v2`，但不得启动；
8. 更新 README、project skill 和本计划执行状态，不改默认 LUT；
9. 运行 full unit suite、compileall、所有相关 wrapper `zsh -n`、`git diff --check`、`codegraph sync`；
10. 生成 `tmp/strip-hsi-pilot-offline/p7-r0-v2-<timestamp>/offline-readiness.json`，记录全部输入/hash、测试数、无设备调用断言、v1 replay、v2 synthetic coverage、旧 sentinel holdout replay 和 proposed real capture budget。

必须新增的回归覆盖至少包括：

- SAT100 null 不再出现 zero-scale artifact，required scale 退化时 hard fail；
- SAT0 永远没有 Hue gate；Hue 0/360 tangent 周期一致；
- reference evaluator 不含 strip covariance，cross-session center shift 不被吸入 within-state covariance；
- repeated block mean 的 `1/n` covariance 缩放正确；
- current center compatible、guard-band unresolved、reference drift 三个 synthetic 分支；
- direct pairwise spread 的 n=3/n=5 maximum 和四类路由；
- P1 floor 只能保持或提高；
- `hsi_coordinate_equivalent` 与 `observer_equivalent` 可得到不同结果，且 residual 不丢失；
- v1 run 可复现且不会被 v2 重新判为正式通过；
- multi-seed/rebase 有严格 start/round/capture 上限；
- dry-run 不加载 `.env`、不联网、不调用 camera/Ray/ESPHome/all_off。

P7-R0 完成后必须停止并交还 Planner。即使测试全部通过，也没有 P7-R1 实机授权。

#### 8.7.9 P7-R1：定向 reference/repeatability named experiment 草案

只有 P7-R0 经 Planner 验收且用户另行明确授权 `p7_targeted_reference_repeatability_v2` 后才能执行。该授权不得从已消费的 `p7_sentinel_4` 继承。

正式 measurement 固定为两个 block；每张均为独立 `off -> 1 s -> exact command -> 60 s -> capture -> off`：

运行顺序固定为：start ambient -> Ray block A -> strip block A -> strip block B -> Ray block B -> end ambient -> Python cleanup -> shell cleanup。只允许在各 block 内使用下述预冻结循环顺序，禁止把 Ray A/B 相邻拍完而失去 session drift 诊断。

**Ray reference，30 张正式 measurement：**

- states：H0/S0、H120/S100、H300/S100；
- block A 与 block B 各 state 5 次，共 `3 * 5 * 2 = 30`；
- 每个 block 内使用预先冻结的循环平衡顺序；
- 每 state 独立曝光 cache，block B 从同 state 的 block A cache 恢复；strip 始终为零。

**Strip repeatability，50 张正式 measurement：**

- commands：第 8.6 节 selected H0/S0@4095、H120/S100@4095、H120/S50@4095、H300/S100@4095、H0/S0@3072；
- 只从 frozen `target-results.jsonl` 按 hash 提取 exact five-channel command，不运行 solver、不改 command；
- block A 与 block B 各 command 5 次，共 `5 * 5 * 2 = 50`；
- 每个 block 内使用预先冻结的五阶循环平衡顺序；
- 每 command 独立曝光 cache，block B 从同 command 的 block A cache 恢复；Ray 始终 intensity 0。

runner 另拍 block 起止所需 ambient frame，数量和 auto-exposure probe 上限必须在 dry-run `plan.json` 中明确；上述 `30+50` 是进入统计的正式 measurement 数，不能用 probe/ambient 补足。整个 run 保留 remote camera、recorded exposure、source isolation、readback、无 `.npy` 和 Python/shell 双 cleanup 合同。

#### 8.7.10 P7-R1 分支

`R-PASS`：三个 Ray state 的 block 内 repeatability、pre/post stability 和 P6 center compatibility 全部在 guarded limit 内；五个 strip command 均有合法 10 repeats；v2 regularization/coverage 收敛；冻结新 v2 artifact/hash，运行旧 sentinel 作为 holdout，但不得把旧 run 升级为 Gate-6 pass。交还 Planner 决定并授权新的四点 sentinel-v2。

`R-REFERENCE-EPOCH`：current Ray pre/post 稳定，但任一 state 与 P6 center 超出 unguarded limit。标记 `reference_epoch_shift`，不得在本 run 重拟合 P6。停止 P7；Planner/Advisor决定另一个自然日重复 P7-R1，或建立新的 Ray epoch。仅三个 anchor 不能自动更新完整 P6 manifold。

`R-REFERENCE-UNSTABLE`：block 内或 pre/post 不稳定。停止 HSI 求解，检查热状态、几何、曝光 provenance、remote capture 和供电；保留所有样本。修复前不得新 sentinel。

`R-STRIP-CLASS-HIGH`：Ray reference 通过，但某 strip class 明显高于 P1 floor。允许 v2 对该 class 逐 plane 采用更保守方差；若 Monte Carlo/guard 仍稳定且 10 repeats 无趋势，可继续。若存在 block trend、双峰、非有限 feature 或方差由单个异常帧支配，标 `uncertainty_unresolved` 并交还 Planner，不能用无限增大 covariance 自动通过。

`R-MEASUREMENT/CODE/SAFETY`：任何 measurement、source/readback、remote、provenance、cleanup 失败使整个 run 无效；按失败合同保留证据、确认双关灯、修复后使用全新目录完整重跑，禁止拼接两个 run 的 block。

#### 8.7.11 新 sentinel-v2 的放行边界

只有 `R-PASS`、v2 artifact 已冻结、P7-R0/R1 全套检查通过且 Planner 再次验收后，才能请求新的 `p7_sentinel_4_v2` 授权。新 sentinel 必须完整重跑四点，不复用第 8.6 节结果；pre 三个 Ray anchor 各 3 repeats，post H120/S100 3 repeats；solver start/round/capture budget 在 capture 前冻结。

新自动放行条件以后续 Planner 写入的 sentinel-v2 条款为准。在该条款出现前，Executor 即使得到四个 `hsi_coordinate_equivalent` 也必须停止，不能直接执行 remaining 9。

#### 8.7.12 P7-R0 Executor 离线实施结果（2026-07-18）

```text
status = ready_for_planner_review
device_calls = 0
policy_v2 = config/hsi/strip-hsi-policy-v2-waiting.json
policy_v2_sha256 = db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4
policy_v2_status = waiting_for_targeted_measurement
formal_capture_eligible = false
v1_replay = byte-identical; analysis SHA-256 5416dfcae4ea1f4114d1757a0d253b059677a984f728a7f10a8dd81cd265e043
v2_synthetic_coverage = pass_synthetic_only_not_formal_limits
old_sentinel_holdout_groups = 5; Gate-6 eligibility false
p7_r1_draft = 30 Ray + 50 strip + 2 ambient; execution unauthorized
full_unit_suite = 367 passed
```

实现保持 v1 reader/analyzer，并要求旧 run 显式使用 `--policy-version v1`；v2 使用独立 schema/read/write，不覆盖 v1 artifact。新增 direct-feature reference center/repeatability、block-mean `1/n` covariance、四类 direct confirmation spread、P1 floor 保守路由、signed endpoint-safe tangent、三层 equivalence/residual 输出和 required-scale hard fail。Solver 接收 directional residual，支持有限 distinct-face multi-seed、prediction/Jacobian rebase 和严格总 capture 上限。

旧 sentinel replay 只作完全独立 holdout，未拟合 covariance、scale、limit、guard 或 budget。Direct spread 使用 P1 floor 仅输出诊断 score，因 P7-R1 尚未完成，所有 group decision 仍为 `waiting_for_targeted_measurement`。四点 local tangent condition 约为 SAT0 `1.0`、H120/S100 `2.908`、H120/S50 `2.292`、H300/S100 `3.387`，离线未见局部坐标病态；但这不能代替 P7-R1 reference epoch 与定向 repeatability 证据。

Executor 给 Planner 的 solver budget 提案是：最多 `2` 个 distinct active-face starts，每 start `8` feedback rounds、最多 `2` 次 rebase、`3` confirmations，严格上限 `48 captures/target`。这是 replay 提案，不是新实拍冻结值；Planner 必须接受或修改后再授权。

主要证据：

- `tmp/strip-hsi-pilot-offline/p7-r0-v2-20260718-090507/p7-r0-v2-replay-final.json` @ `e7a1c98dd7292acba9be7ef876795d802c07ada2852080f5fcddeca6301cb559`；
- `tmp/strip-hsi-pilot-offline/p7-r0-v2-20260718-090507/p7-r1-draft/plan.json` @ `8bd3daf61fab16f453a2e307c55d028480491cb5f073657a2c6a895d61045259`；
- `tmp/strip-hsi-pilot-offline/p7-r0-v2-20260718-090507/offline-readiness.json` @ `a81bc4ba64d962e672f49319536bff2d93bb728d930944fdee28da4109d710c3`。

本节完成后必须停止并交还 Planner。P7-R1、新 sentinel、remaining 9、boundary、holdout 与 P8 继续锁定。

#### 8.7.13 Planner 对 P7-R0 的验收决定（2026-07-18）

```text
decision = reject_for_formal_capture
mathematical_direction = accepted_with_offline_corrections
next_phase = P7-R0B
device_authorization = none
p7_r1_authorization = none
sentinel_v2_authorization = none
```

P7-R0 当前不能被验收为 P7-R1 的实拍前检查点，但不要求推翻已完成的 v2 工作。以下部分接受并保留：

- v1 reader/analyzer 和 byte-identical legacy replay；
- v2 waiting artifact 与 v1 artifact 分离，且 `formal_capture_eligible=false`；
- endpoint SAT100 signed one-sided tangent、SAT0 禁止 Hue gate、required scale 为零时 hard fail；
- direct reference/repeatability、58-feature 分离和 30 Ray + 50 strip + 2 ambient 的 P7-R1 采集形状；
- 旧 sentinel 只作独立 holdout，不参与拟合或 Gate-6；
- 当前证据 hash、`367/367` 测试结果和零设备调用声明。

Planner 独立复核通过 `367/367` 测试、`compileall`、wrapper `zsh -n` 与 `git diff --check`。这些结果只证明现有单元合同和语法完整，不覆盖下列 formal-path 缺口：

1. 正式 `measure_strip_hsi_pilot` 仍调用 v1 `evaluate_hsi_observation` 与单 seed `run_hsi_feedback`；v2 evaluator/multiseed 目前只有测试调用，正式 result status 也仍是 v1 集合。
2. `measure_hsi_reference_repeatability` 只允许 `--dry-run`，尚无真实采集路径、双 cleanup wrapper、分析器或 finalizer；在冻结统计规则前不得授权采集 82 张计划样本。
3. `48 captures/target` 不是状态机的可证明最坏上限。primary/backtrack rejection 和重复 confirmation 都会额外消费 capture；达到总上限时当前 multiseed 直接抛 `RuntimeError`，没有返回带 best-valid sample 的 `solver_budget_exhausted`。
4. v2 实测 evaluator 用 target-specific `guarded_limit` 判断 coordinate feasibility，但 solver 的 predicted objective 把 raw normalized coordinate norm 与硬编码 `1.0` 比较，预测排序与正式验收尺度不一致。
5. 当前 replay 只对旧 trace 拟合 affine predictor，再静态输出 2/8/2/48；它没有重放新的 multiseed 状态机，不能证明两 starts 的收益或预算完整性，其误差指标还混合 Hue、SAT 和 feature residual 的不同单位。
6. `plane_block_regularize` 取 CFA plane 内最大 feature variance，未复用计划中的 within-group center + MAD/RMS block regularization，也没有冻结 trend、双峰、异常帧主导的 `R-STRIP-CLASS-HIGH` 审计分支。
7. synthetic coverage 尚未校准 coordinate joint 99.73% region/guard band，也未检验 empirical coordinate coverage；因此只能保留 `pass_synthetic_only_not_formal_limits`，不能升级为 formal policy。

以上是实现和验收合同缺口，不需要本轮再次请求 Advisor 改变数学方向。只有 P7-R0B 无法用冻结 GUIDE 解决、需要改变 58-feature 语义、联合 coverage 定义或 target/solver 架构时，才重新交还 Advisor。

#### 8.7.14 Planner 冻结的 solver 预算设计

原提案中的三个结构上限接受：

```text
max_distinct_face_starts = 2
max_logical_rounds_per_start = 8
max_rebases_per_start = 2
```

原 `48 captures/target` 驳回，改为以下可逐项审计的预算。这里的 `logical observation` 是 solver 请求的一次有效测量机会；`physical CR3` 是相机实际落盘次数，包括自动曝光和有界 weak-signal reacquire。

```text
max_feedback_capture_attempts_per_start = 8
max_confirmation_groups_per_start = 2
ordinary_confirmation_captures_per_group = 3
boundary_confirmation_captures_per_group = 5
rebase_probe_count = 4  # all-or-none
max_autoexposure_physical_captures_per_target = 10
max_weak_signal_reacquire_physical_captures_per_target = 4
```

预算规则：

- 一个 feedback round 内的 primary、0.5 backtrack、0.25 backtrack 均分别消费 `max_feedback_capture_attempts_per_start`，不能把三个 physical captures 记成一个 round；预算耗尽后不得继续 backtrack。
- 每次 rebase 必须在剩余预算足够完成全部四个 probe 时才开始；不允许留下 partial Jacobian。
- 每个 start 独立保留自己的初始、probe、feedback、rebase 和 confirmation 预算；第一个 start 不能消费第二个 start 的保留预算。
- final verification 必须消费 confirmation-group 预算；solver 返回后不得追加未声明的隐藏 captures。
- 同一 target 只允许一个 target-specific auto-exposure cache。自动曝光最多 10 张，其中第一张同时计入 solver 的 initial logical observation，因此 physical overhead 最多为 `10 - 1 = 9`。
- weak-signal reacquire 在两个 starts 之间共享全局最多四张；不得通过切换 start 重置。
- reference/ambient captures 不计入 per-target cap，但必须在 experiment plan 中独立列出并计数。

普通 sentinel/pilot 点的上限：

```text
per_start_logical = 1 initial + 4 probes + 8 feedback attempts
                    + 2 * 4 rebase probes + 2 * 3 confirmations
                  = 27
per_target_logical = 2 * 27 = 54
per_target_physical_cr3 = 54 + 9 autoexposure overhead + 4 reacquire = 67
```

边界、Gate-6 candidate、接近极限点及 holdout 使用 5 张 confirmation 时：

```text
per_start_logical_n5 = 1 + 4 + 8 + 2 * 4 + 2 * 5 = 31
per_target_logical_n5 = 2 * 31 = 62
per_target_physical_cr3_n5 = 62 + 9 + 4 = 75
```

`54/67` 和 `62/75` 是 hard caps，不是目标拍摄量。达到任一逻辑或物理上限必须返回结构化 `solver_budget_exhausted`，至少保存 target、start、phase、各子预算消费、best valid sample、best command、最后有效 objective 和 rejection evidence；禁止抛出未转换的 `RuntimeError`。Runner 必须同时执行 logical-observation 与 physical-CR3 两层计数。

上述预算作为 P7-R0B 的实现合同已获 Planner 接受，但尚未成为实拍冻结值。只有状态机、replay、exhaustion 测试和 formal runner 接线再次通过 Planner 复验后，才可随 named-experiment authorization 一起冻结。

#### 8.7.15 P7-R0B 唯一离线纠偏阶段

Executor 必须按 A-D 顺序执行；任何一项失败都停在离线阶段，不得跳到 P7-R1。

##### A. 接通 formal v2 路径

1. 正式 runner/analyzer 必须按显式 policy version 分派 evaluator、solver、result statuses 与 provenance；v1 只允许显式 legacy replay，禁止静默默认回退。
2. waiting/candidate v2 policy 必须 hard-reject formal sentinel；只有 Planner 后续明确接受的 frozen formal artifact 才能被 runner 使用。
3. 正式 v2 路径调用 `evaluate_hsi_observation_v2` 和 bounded multiseed solver，并输出 `faithful`、`unconfirmed`、`measurement_unreachable`、`uncertainty_unresolved`、`solver_budget_exhausted`、`reference_drift`、`boundary_bracketed_at_full_scale` 等互斥状态。
4. pre/post reference 必须按计划保存 repeat blocks，不能退化为单张 anchor；SAT0 不输出 Hue decision。
5. analyzer 必须核对 policy/hash、manifold/hash、feature order、budget declaration/consumption、source isolation、recorded exposure 和 cleanup provenance。

##### B. 修正 solver 状态机、尺度和 replay

1. 实现第 8.7.14 节的 per-start sub-budget、global physical budget、all-or-none rebase、second-start reservation 和结构化 exhaustion。
2. predicted coordinate residual 必须使用与实际 evaluator 相同的 target-specific guarded region；可把 residual 除以 frozen guarded limit，或向 predicted objective 显式传入同一 region，禁止继续硬编码无语义的 `1.0`。
3. 增加 rejected primary/backtracks、反复进入 confirmation、partial-rebase prevention、first-start exhaustion、second-start reservation、autoexposure/reacquire physical cap 和 best-valid exhaustion 的测试。
4. replay 必须实际驱动 proposed multiseed state machine 重放旧 trace；缺少未拍 command 时明确记 `trace_support_missing`，不得插值伪造 observation。Replay 只验证状态迁移、单位一致性和预算 accounting，不宣称证明实机收敛。
5. 所有 replay prediction error 必须在 v2 normalized coordinate/rendering 空间报告，禁止把 degree、percent 和 raw feature residual 合并为一个无量纲阈值。

##### C. 完成 v2 calibration/finalization 算法

1. 在 synthetic fixtures 上实现并验证 coordinate joint 99.73% coverage region、bootstrap guard band、observer/reference direct region 和 n=3/n=5 repeatability decision；同一噪声源不得重复计数。
2. block/state variance 必须复用或扩展 `regularize_groups` 的 within-group centering 与 per-CFA-plane MAD/RMS regularization；禁止用单个 feature maximum 代替整个稳健估计流程。
3. 在采集前冻结 trend、双峰、非有限 feature、单异常帧主导、effective sample shortage 和 bootstrap instability 的审计阈值。任一触发都返回 `uncertainty_unresolved`，不得靠无限增大 covariance 自动通过。
4. P7-R1 analyzer/finalizer 只能生成 `calibrated_waiting_for_planner` candidate，且 `formal_capture_eligible=false`。Executor 不得自行把 candidate 改为 frozen/formal；只有后续 Planner 验收能生成或批准正式 artifact/hash。
5. synthetic report 必须分别给出 empirical coordinate/reference/observer coverage、Monte Carlo seed、sample count、guard calculation 和 failure branch；不得只输出 direct-feature limit。

##### D. 离线实现完整 P7-R1 执行面，但不得运行

1. 把现有 30 Ray + 50 strip + 2 ambient dry-run 扩展为真实 remote-backend runner、analyzer、finalizer 和 shell wrapper；只实现代码与 fake backend 测试，不连接设备。
2. 远程凭据由脚本/backend 自行加载 `.env`，代码、日志、plan 和测试输出不得读取后打印 secret。
3. 使用共享 capture adapter、recorded exposure、原子 CR3 落盘、零 `.npy`、严格 source isolation/readback、Python `finally` 与 shell `trap` 双关灯。
4. 正常完成必须严格得到计划内 82 个 logical reference/repeatability captures；自动曝光/reacquire 的额外 physical captures 必须独立审计，不能改写 82 的统计样本数。
5. Analyzer/finalizer 必须预先实现 `R-PASS`、`R-REFERENCE-EPOCH`、`R-REFERENCE-UNSTABLE`、`R-STRIP-CLASS-HIGH`、`uncertainty_unresolved`、capture/source/readback/cleanup failure 分支；不得等实拍后再定义阈值。
6. 生成新的 dry-run plan、offline-readiness、policy candidate schema 和所有 SHA-256；dry-run 必须证明 remote-only、82 张统计样本、额外物理上限、双 cleanup 和 formal-ineligible candidate。

P7-R0B 交还 Planner 前必须同时满足：

- full suite、`compileall`、全部相关 wrapper `zsh -n`、`git diff --check`、`codegraph sync` 通过；
- v1 legacy replay 仍 byte-identical；
- v2 formal runner/analyzer 路径有 integration test，不再只有 isolated unit calls；
- 第 8.7.14 节的普通与 n=5 hard caps 均有 exact-boundary 和 one-over-boundary 测试；
- synthetic joint coverage/failure branches 和 P7-R1 fake backend 成功/失败/cleanup branches 有行为断言；
- 新 readiness 明确列出所有尚未实测的统计量，不能把 synthetic 值标成 formal；
- Executor 更新本计划证据后停止，交还 Planner 复验。

在 Planner 复验并由用户另行授权之前，`p7_targeted_reference_repeatability_v2`、P7-R1、新 sentinel、remaining 9、boundary、holdout 与 P8 全部保持锁定。

#### 8.7.16 P7-R0B Executor 离线纠偏结果（2026-07-18）

```text
status = offline_complete_waiting_for_planner_acceptance
device_calls = 0
p7_r1_execution = not_run_not_authorized
goal = Blocked
```

Executor 已按 8.7.15 A-D 完成纯离线纠偏，并在此停止：

- formal runner 现在要求显式 `policy_version`；v1 只保留 legacy replay，v2 formal sentinel 对 waiting/candidate policy hard reject。旧 `config/hsi/strip-hsi-pilot.json` 及 sentinel 输入 hash `ca5cb49d...` 保持不变，v2 使用独立 `config/hsi/strip-hsi-pilot-v2.json` @ `8a7a2d3616365e46617ca5d7b7898c9480c1a9599b9135e808ceaab30fc62215`；
- v2 formal integration 已接通 `evaluate_hsi_observation_v2`、two-distinct-face multiseed、target-specific guarded scale、repeat blocks、v2 status/provenance 和 analyzer audit；waiting/candidate artifact 不能进入 formal runner；
- solver budget 由独立状态对象所有。普通点 exact cap 为 `54 logical / 67 physical CR3`，n=5 为 `62 / 75`；primary/0.5/0.25 各消费 feedback attempt，rebase 四 probe all-or-none，两个 starts 独立保留预算。耗尽返回结构化 `solver_budget_exhausted`，保留 best-valid sample/command/objective/rejection evidence，不再抛裸 budget `RuntimeError`；
- predicted coordinate residual 和 evaluator 均使用同一 target/class-specific guarded limit；prediction error 分开报告 guarded-normalized coordinate 与 whitened rendering，不再混合 degree、percent 和 raw feature residual；
- replay 真实驱动 proposed multiseed 状态机。旧 trace 每个四点均明确得到 `trace_support_missing`（各使用 9 logical observations、4 个 unsupported commands），不插值或伪造 observation；v1 replay 继续 byte-identical，SHA-256 `5416dfca...`；
- v2 calibration/finalizer 使用 within-group centering、per-CFA-plane MAD/RMS regularization、coordinate/observer/reference/repeatability 分离的 99.73% MC/guard。采集前 audit 阈值已写入代码/candidate schema，覆盖 trend、双峰、非有限 feature、单帧方差主导、effective sample shortage 与 bootstrap instability；任一分支 fail closed 为 `uncertainty_unresolved`；
- P7-R1 已实现 remote-only runner、shared native-RAW capture adapter、recorded exposure、atomic CR3、source isolation/readback、weak reacquire audit、Python finally、shell trap、analyzer 和 formal-ineligible `calibrated_waiting_for_planner` finalizer。fake backend 成功、失败和 cleanup 分支均有行为断言；真实 runner 未启动；
- P7-R1 dry-run 仍严格为 30 Ray + 50 strip + 2 ambient = 82 logical captures。8 个 exposure cache miss、每 miss 最多 12 张 physical、最多 80 张 bounded weak reacquire，使声明的 absolute physical hard cap 为 250；统计样本数始终固定 80，额外 physical CR3 不补足或改写 formal sample；
- `config/hsi/strip-hsi-policy-v2-waiting.json` 仍为 `waiting_for_targeted_measurement` / `formal_capture_eligible=false`，SHA-256 仍为 `db9ebef1...`。Executor 没有生成或批准 frozen formal policy。

最终离线证据目录：

```text
tmp/strip-hsi-pilot-offline/p7-r0b-v2-20260718-101555-final
```

证据与 SHA-256：

- `p7-r0b-v2-replay-final.json` @ `6b8862d5850053e4ad3d7c7e96da073bb7e521ad767e1f38b7ad9a23b30d4606`；
- `p7-r1-draft/plan.json` @ `be17c55815a7fca3e14cecfc30c33bd87eb9a263d5ead4662a10389865462f35`；
- `offline-readiness.json` @ `8441e1d594356e7d3f01befcea949506c55f9d00dd87be45553898d40663f05a`；
- `full-suite.log` @ `21ba98d0d190770952b27cb19970ba3d4254961404610ed210e310251a188bcb`。

验证结果：full suite `380/380`（72.037 s）通过；`compileall`、四个相关 wrapper `zsh -n`、`git diff --check`、`codegraph sync` 全部通过。聚焦 P7-R0B 测试 `52/52` 通过。全程未加载 `.env`，未调用网络、camera、Ray、ESPHome 或 all_off。

仍未实测且必须由 P7-R1 提供的数据：当前 epoch 的 Ray center compatibility、pre/post reference repeatability、四个 strip class variance、新 sentinel-v2 convergence，以及 remaining/boundary/holdout 行为。Synthetic 数值没有被标成 formal。

本节完成后必须交还 Planner。Planner 需复验 A-D、接受或拒绝 P7-R0B，并决定是否另行授权 exact named experiment `p7_targeted_reference_repeatability_v2`。在此之前 P7-R1 execution、新 sentinel、remaining 9、boundary、holdout 与 P8 继续锁定；Advisor 不需要介入，除非 Planner 认为必须改变 58-feature、联合 coverage 或 solver/target 架构。

#### 8.7.17 Planner 对 P7-R0B 的复验决定（2026-07-18）

```text
decision = reject_for_named_experiment_authorization
preserve_completed_work = true
next_phase = P7-R0C
solver_caps_54_67_and_62_75 = unchanged
p7_r1_250_physical_cap = proposed_not_frozen
p7_targeted_reference_repeatability_v2 = not_authorized
advisor_escalation = not_required
```

Planner 独立核对全部交接 hash，并复跑 full suite `380/380` 通过。另以纯离线 deterministic fixtures 复现两个未被测试覆盖的错误：

- 一个未确认 face 的单帧误差更小、另一个 face 已完整确认时，multiseed 返回 `unconfirmed` 并选择未确认 face；
- H120/S100 与 H300/S100 各自完全稳定时，只因它们属于同一 `sat100_fullscale` class，当前 audit 把两个不同中心拼接后产生约 `1.33e6` 的伪 trend score，并返回 `uncertainty_unresolved`。

因此 `380/380` 是当前测试基线，不是 P7-R0B formal acceptance。以下阻塞项必须修复：

1. `analyze_strip_hsi_pilot` 仍在入口 hard-reject 非 legacy-v1 run，CLI 也只允许 `--policy-version v1`；其 target/anchor/combined audit 继续读取 `uncertainty_artifact`、`uncertainty_artifact_sha256`、`feedback.best` 和单帧 anchor evaluation，无法分析 v2 runner 实际产生的 `policy_v2_artifact`、`policy_artifact_sha256`、multiseed result 和 repeat-block analysis。现有 v2 integration test 只执行 runner，没有调用 analyzer。
2. Multiseed 的最终选择在所有 best samples 上排序，没有先选择 `goal_confirmed=true` 的 attempt。已确认结果必须优先于任何未确认单帧结果。
3. Confirmation 遇到第一张合法但不满足 coordinate gate 的图就提前返回，不能形成预声明的 n=3/n=5 完整 group；若 solver 从未出现 feasible sample，也没有对 best-valid command 执行最终 confirmation group。这违反“普通点 3 张、边界点 5 张”和 final verification 必须消费既有 confirmation-group budget 的合同。
4. `audit_repeatability_groups` 虽然用 within-group residual 估 covariance，却用未按 group 中心化的跨 command/state 矩阵计算 trend、bimodal 和 single-frame dominance。不同 HSI target 的产品中心被错误当成噪声或漂移，直接污染 `R-STRIP-CLASS-HIGH` 分支。
5. P7-R1 analyzer 没有读取 `commands.jsonl`，却直接声明 source isolation/readback pass。Weak-signal reacquire 会覆盖逻辑 record 中的原始 rejected capture，record 仍保存第一次 readback，reacquire 的独立 command/readback、原始 CR3/report 和 selected-attempt provenance 不完整；reacquire 前也没有完整执行预声明的 `off -> 1 s -> on -> 60 s`。
6. P7-R1 的 250 physical CR3 只在 capture 完成后按 counter 检查；analyzer 不从 retained attempt/auto-exposure evidence 重算 physical count，也不验证 `<=250`、weak reacquire `<=80` 或 run counter 与实际证据一致。因此 250 只能保留为提案，不能随本次验收冻结。
7. P7-R1 fake finalizer test只断言写出 formal-ineligible candidate，没有断言 `R-PASS`、`R-REFERENCE-EPOCH`、`R-REFERENCE-UNSTABLE`、`R-STRIP-CLASS-HIGH` 和 `uncertainty_unresolved` 的确定性分支。交接中“全部分支已有行为断言”不成立。

这些都是既定架构内的实现和验收缺口，不要求改变 58-feature、联合 coverage 或 solver/target 语义，因此本轮不交还 Advisor。P7-R0B 已正确完成的 waiting-policy fail-closed、target-specific guarded scale、structured budget evidence、old-trace `trace_support_missing`、remote/fake R1 执行骨架和双 cleanup 必须保留，不得重写。

#### 8.7.18 P7-R0C 唯一离线收口阶段

P7-R0C 只允许修改上述阻塞路径及其测试/文档。`54/67`、`62/75`、2 starts、8 feedback attempts/start、2 rebases/start、2 confirmation groups/start 的预算数学保持不变；若修复需要增加这些上限，立即停止并交还 Planner。

##### A. 正式 v2 analyzer 闭环

1. 为 `analyze_strip_hsi_pilot` 增加显式 `policy_version` dispatch。v1 只允许显式 legacy replay；v2 只接受 `plan.measurement.policy_version=v2` 且 frozen/formal-eligible policy hash 与 plan 完全一致。禁止任何静默回退。
2. 复用 capture、command、cleanup、input-hash 基础 audit，但为 v2 单独解析：
   - `inputs.policy_v2_artifact` 与 objective `policy_artifact_sha256`；
   - multiseed 的 `selected_result`、`best_valid_sample`、attempt budgets 和 physical budget；
   - `reference-pre-analysis.json`/`reference-post-analysis.json` 的三张 repeat blocks、center compatibility 和 pre/post stability；
   - `hsi_coordinate_equivalent`、`observer_equivalent`、`color_rendering_residual` 三层输出；
   - 互斥 result status、n=3/n=5 confirmation spread、source/readback、recorded exposure、零 `.npy` 与双 cleanup。
3. v2 sentinel analyzer 不得沿用 v1 `within_reference_coverage` 单帧 anchor 字段，不得读取 v1 `feedback.best` 或 `uncertainty_artifact`。
4. Combined analyzer 的 shared policy key 必须随版本选择，并拒绝不同 policy hash/version 的 sentinel 与 remaining 拼接。现阶段只用 fake runs 验证，不执行 remaining。
5. 新 integration test 必须：生成 formal-eligible fake v2 policy -> build plan -> execute fake sentinel -> 写 fake shell cleanup -> 调用 v2 analyzer -> 验证四点、12 anchors、预算、三层输出和 policy provenance。另加 waiting/candidate、hash drift、缺 cleanup、错误 confirmation 数和 command sequence 的拒绝测试。

##### B. Solver 确认语义和选择优先级

1. Multiseed 若存在任一 `goal_confirmed=true` attempt，只能在 confirmed attempts 中按 objective 排序；只有不存在 confirmed attempt 时，才在 best-valid samples 中选择。Overall status 必须由“是否存在 confirmed attempt”决定，不能由未确认 best sample 反向覆盖。
2. 一个 confirmation group 一旦开始，所有**可测**的 n=3/n=5 captures 必须采完后再判 group pass/fail；一张合法但 coordinate fail 的图不能提前结束 group。Measurement rejection、physical exhaustion 或安全失败可以中止，但必须保存 partial-group evidence 和明确状态。
3. Solver 正常结束而尚未确认时，只要存在 best-valid sample 且还有 confirmation-group budget，必须对 best-valid command 执行一个完整 final-verification group；它使用现有第二组预算，不得追加隐藏预算。
4. 若两组 confirmation 都已消费、没有 valid sample 或 measurement 已不可达，返回相应 `solver_budget_exhausted`/`measurement_unreachable`/`unconfirmed`，保留 best-valid evidence；不得增加第三组。
5. 新测试至少覆盖：未确认低误差 face vs 已确认高误差 face、首张 confirmation fail 仍收满 n、从未 feasible 仍执行 final group、partial group measurement rejection、两组耗尽、n=3/n=5 exact cap 和 one-over。修复后 hard caps 必须仍精确为 `54/67` 与 `62/75`。

##### C. Repeatability audit 必须按 state/command/block 去中心

1. Covariance、trend、bimodal 和 single-frame dominance 都只能使用同 state/command、同 block 内中心化 residual；不得把 H120 与 H300、不同 strip command 或 A/B 中心偏移直接当随机残差。
2. 每个 Ray state 和每个 strip command 独立执行 audit；`sat100_fullscale` 可以在各 command 去中心后 pool residual 估 class covariance，但 audit failure 必须保留 command/block provenance。
3. 每个 block 内按真实 capture chronology 检查 trend，禁止按排序后的 group id 伪造时间轴。A/B block center shift 作为独立 stability statistic 报告，不吸收到 within-block covariance。
4. 增加 regression：H120/S100 与 H300/S100 中心显著不同但各自稳定时必须 pass；任一 command 内真实 trend、双峰、单帧主导或 A/B shift 时必须命中预声明分支。
5. 不得根据新 synthetic 结果修改 `AUDIT_THRESHOLDS`；若现有阈值在正确中心化后仍不可辨识，停止并交还 Planner。

##### D. P7-R1 物理证据、source audit 和 hard cap

1. 每个 logical capture 必须保留 base attempt 及可选 weak-reacquire attempt 的完整 provenance：CR3/report、physical count、command/readback、off/on settling、quality rejection、是否 selected_for_formal。可以使用 nested attempts 或独立 `capture-attempts.jsonl`，但 `captures.jsonl` 仍严格为 82 个 logical rows。
2. Weak reacquire 必须重新执行 `both_off -> 1 s -> exact source command/readback -> 60 s -> capture -> both_off`，并使用自己的 capture id；不得用第一次 readback 代替 reacquire readback。
3. Runner 在调用 shared capture adapter 前传入剩余 physical budget，使 auto-exposure 无法越过 global cap；分别冻结 base/logical、auto-exposure 和 weak-reacquire counters。任何耗尽在下一次 physical capture 前 fail closed。
4. Analyzer 必须读取 `commands.jsonl` 和 attempt evidence，逐 logical/attempt 验证 source isolation、exact readback、recorded exposure、CR3 非空、零 `.npy`，并重算 physical count；重算值必须等于 `run.json`，且 total `<=250`、weak reacquire `<=80`、auto-exposure cache miss 恰为不超过 8。
5. 250 仍是 absolute proposal，不是预计拍摄量。新 readiness 必须同时报告 logical 82、formal 80、expected physical range、absolute 250 和按现有 dry-run 估算的最长 60-second settling 时间。Planner 下次复验后才决定冻结、收紧或拒绝该上限。
6. Fake tests必须覆盖一次成功 weak reacquire、reacquire readback mismatch、base/reacquire 原始证据保留、auto-exposure one-over pre-reject、counter mismatch analyzer rejection、commands tamper、Python cleanup failure 与 shell cleanup failure。

##### E. R1 finalizer 分支与交接

1. 为 `R-PASS`、`R-REFERENCE-EPOCH`、`R-REFERENCE-UNSTABLE`、`R-STRIP-CLASS-HIGH`、`uncertainty_unresolved` 各增加一个 deterministic analyzer/finalizer test，并断言 candidate 始终 `formal_capture_eligible=false`。
2. 非 `R-PASS` 分支可以保留诊断 candidate，但不得标成可冻结；analysis 必须列出阻塞分支和失败 state/command。
3. 保持 P6 manifold、v1 artifact、waiting policy 和旧 sentinel evidence hash 不变；legacy v1 replay 必须继续 byte-identical。
4. 生成新的 P7-R0C readiness、v2 fake sentinel analysis、P7-R1 dry-run 和 hash。Readiness 必须如实把 250 标为 `proposed_not_frozen`，不得再次声明 formal analyzer/branches 已通过，除非上述 integration/branch tests 实际存在并通过。

P7-R0C 交还 Planner 前必须通过：full suite、focused P7 tests、`compileall`、所有相关 wrapper `zsh -n`、`git diff --check` 和 `codegraph sync`。Executor 完成后停止；不得自动运行 health/config/all_off 或任何 named experiment。

在 Planner 再次验收前，Goal 继续保持 `Blocked`；`p7_targeted_reference_repeatability_v2`、新 sentinel、remaining 9、boundary、holdout 与 P8 全部锁定。

#### 8.7.19 P7-R0C Executor 离线收口结果（2026-07-18）

```text
status = offline_complete_waiting_for_planner_acceptance
device_calls = 0
p7_r1_execution = not_run_not_authorized
p7_r1_250_physical_cap = proposed_not_frozen
goal = Blocked
```

Executor 已按 8.7.18 A-E 完成纯离线纠偏并停止：

- `analyze_strip_hsi_pilot` 现在必须显式 dispatch `--policy-version v1|v2`。v1 仍是 legacy replay；v2 独立验证 frozen/formal-eligible policy path/hash、multiseed `selected_result`、per-start/target logical budget、physical budget、12 张 reference anchors、pre/post repeat analysis、n=3/n=5 confirmation group、互斥 result status，以及 `hsi_coordinate_equivalent` / `observer_equivalent` / `color_rendering_residual` 三层结果。Combined analyzer 按版本选择 shared policy key，拒绝 mixed version/hash；
- multiseed 先在 `goal_confirmed=true` attempts 中选择，只有没有 confirmed attempt 时才比较 best-valid。Confirmation group 一旦开始会收满所有可测 n=3/n=5 captures；measurement rejection 保留 partial group。Solver 正常未确认且仍有 declared group 时，对 best-valid command 执行 final verification；不得超过每 start 两组；
- `54/67`、`62/75`、2 starts、8 feedback attempts/start、2 rebases/start、2 confirmation groups/start 均未改变。Exact/one-over、n=3/n=5、confirmed-first、完整/partial group、never-feasible final verification 和两组耗尽均有回归覆盖；
- repeatability covariance、trend、bimodal 与 single-frame dominance 现在只消费同 state/command/block 去中心 residual。Trend 使用 block 内真实 chronology；H120/S100 与 H300/S100 的不同产品中心不再产生伪 trend。每个 command 单独 audit，A/B block center shift 作为独立 stability statistic 和 command provenance 报告；冻结阈值未修改；
- P7-R1 的 `captures.jsonl` 仍严格为 82 logical rows；新增 append-only `capture-attempts.jsonl`，每个 logical 保留 base 与可选 weak-reacquire attempt 的 CR3/report、physical count、command/readback、settling contract、quality rejection 和 selected-attempt provenance。Weak reacquire 使用独立 capture id，完整重新执行 off/1s/on/readback/60s/capture/off；
- runner 在调用 shared capture adapter 前传入 global/auto remaining budget，并分开记录 base、auto-exposure、cache-miss、weak-reacquire 和 total counters。Analyzer 读取 `commands.jsonl` 与 attempt evidence，逐 attempt 审计 source isolation、exact readback、recorded exposure、nonempty CR3、零 `.npy`，独立重算全部 physical counters 并与 `run.json`、`<=250`、weak `<=80`、cache miss `<=8` 比对；
- R1 分支选择对 `R-PASS`、`R-REFERENCE-EPOCH`、`R-REFERENCE-UNSTABLE`、`R-STRIP-CLASS-HIGH`、`uncertainty_unresolved` 均有 deterministic test；candidate 始终 `calibrated_waiting_for_planner` / `formal_capture_eligible=false`，analysis 保留 failed state/command/region；
- fake tests 覆盖 formal v2 sentinel analyzer、waiting/hash/cleanup/confirmation/command drift、成功 weak reacquire、reacquire readback mismatch、原始 attempt 保留、auto-exposure pre-reject、counter mismatch、commands tamper、Python cleanup failure 和 shell cleanup failure。

最终离线证据目录：

```text
tmp/strip-hsi-pilot-offline/p7-r0c-v2-20260718-final
```

证据与 SHA-256：

- `p7-r0c-v2-replay.json` @ `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；
- `p7-r1-draft/plan.json` @ `addaec533bd755df99c8349758a2fc52855d5704950ec422bb5943bbb756e47d`；
- `v2-fake-sentinel-analysis.json` @ `91058d2c28d075769f8078a7fed2718aec1dbc5149f919a0ef3b229651fe50a1`；
- `offline-readiness.json` @ `806cd77ddb067faa32eb1f33f203ca274bb0e14ad66fe0965570a0e2a2f217bf`；
- `full-suite.log` @ `61951a9e4c3f55e49e4a988a312a8c29f133f822cc6f8dd31d6132e3fcae0cde`。

验证结果：focused P7 `79/79` 通过；full suite `395/395`（81.545 s）通过；`compileall`、四个相关 wrapper `zsh -n`、`git diff --check`、`codegraph sync` 全部通过。全程未加载 `.env`，未调用网络、camera、Ray、ESPHome、health/config 或 all_off。

P7-R1 dry-run 仍为 82 logical / 80 formal。按现有 adapter contract 的 expected physical range 为 `82..170`，absolute proposal 为 `250`，最坏 60-second settling 为 `9600 s`。`250` 在 readiness 中明确为 `proposed_not_frozen`，必须由 Planner 下次复验决定冻结、收紧或拒绝。

仍未实测：当前 epoch Ray center compatibility、真实 pre/post stability、四个 strip class variance、新 sentinel-v2 convergence、remaining/boundary/holdout。Synthetic/fake evidence 不得标成 formal empirical pass。

本节完成后交还 Planner。Planner 接受或拒绝 P7-R0C，并另行决定是否授权 exact named experiment `p7_targeted_reference_repeatability_v2`。在此之前所有设备路径、新 sentinel、remaining 9、boundary、holdout 与 P8 继续锁定；Advisor 不需要介入，除非必须改变 58-feature、联合 coverage 或 solver/target 架构。

#### 8.7.20 Planner 对 P7-R0C 的复验决定（2026-07-18）

```text
decision = reject_for_named_experiment_authorization
preserve_completed_work = true
next_phase = P7-R0D
solver_caps_54_67_and_62_75 = accepted_unchanged
p7_r1_absolute_physical_cap = frozen_at_250
p7_r1_baseline_range_without_weak_reacquire = 82..170
p7_targeted_reference_repeatability_v2 = not_authorized
advisor_escalation = not_required
goal = Blocked
```

Planner 以当前 `HEAD=b4779036d9bc9610e967fa5d9514a39463034551` 为验收对象，核对五个交接 artifact hash 均与 8.7.19 一致，并独立复跑 full suite：`395/395`，`129.051 s`，exit 0。该测试结果确认当前基线稳定，但以下两个 formal evidence contract 仍可被确定性反例绕过，因此不能放行实机：

1. **`R0C-REV-001`：formal v2 analyzer 的 budget/status audit 仍依赖 target row 自报值。**
   - 相关实现：`optimization/analyze_strip_hsi_pilot.py::_validate_v2_target_evidence`。
   - 当前只检查 logical/physical 数字不超过上限，没有从 `captures.jsonl`、sample observation capture ID、measurement rejection、confirmation group 和 physical event ledger 重算，也没有验证 `result_status` 与 confirmed/spread/feedback status 的语义关系。
   - Planner 离线反例 A：fake v2 sentinel 实际保留 29 条 capture rows，把首目标的 target-level logical/physical 及 selected start logical 自报值统一改为 `0` 后，analyzer 仍返回 `budget_audit=pass`、`ready_for_sentinel_branch`。
   - Planner 离线反例 B：把一个 `goal_confirmed=true` 的首目标行改写为 `result_status=gamut_status=unconfirmed` 后，analyzer 仍返回 `ready_for_sentinel_branch`、`blocking_count=0`。
   - 影响：落盘 target result、budget 或状态映射发生 runner bug/证据漂移时，formal analyzer 不能 fail closed；8.7.18 A 所称“完整审计”尚未成立。

2. **`R0C-REV-002`：P7-R1 exact readback/source/physical audit 仍验证内部自洽，而非冻结 plan 真值。**
   - 相关实现：`optimization/measure_hsi_reference_repeatability.py::both_off/acquire` 与 `optimization/analyze_hsi_reference_repeatability.py::_audit_capture_contract`。
   - Analyzer 只比较 command event readback 与 attempt readback 是否相等，没有把 Ray readback 与 `plan_step.state`、strip response 与冻结 command/curve payload 比较；`both_off` 只检查事件名首尾，不验证返回 payload 为五通道零/Ray intensity 零，也不拒绝同一 attempt 内的异源或多余 on event。
   - `base_physical_cr3_count`、logical/formal completed counters、auto-exposure 总量/单 cache-miss 上限没有全部从 retained evidence 重算并与 `run.json` 比较。存在 weak reacquire 时，analyzer 也必须证明被选中的一定是通过质量门的 reacquire，而不是已经记录 weak-only rejection 的 base。
   - Planner 离线反例：把一个冻结计划 H0/S0 Ray attempt 的 command event、attempt 和 logical row readback 一致改成 H1，同时把 `base_physical_cr3_count` 从 82 改成 181，`_audit_capture_contract` 仍返回 `source_isolation_and_readback=pass`。
   - 影响：错误设备状态、错误选择 attempt 或计数漂移可能进入 reference/repeatability calibration；8.7.18 D 所称“独立重算全部 physical counters/exact readback”尚未成立。

以下 P7-R0C 成果通过本轮 Planner 复验并冻结保留，不得在 P7-R0D 重写：

- v1/v2 显式 analyzer dispatch 与 waiting/candidate hard rejection；
- confirmed-first multiseed；完整 n=3/n=5 confirmation group；best-valid final verification；
- `54/67`、`62/75`、2 starts、8 feedback attempts/start、2 rebases/start、2 confirmation groups/start；
- state/command/block 去中心的 repeatability、真实 chronology trend 与独立 A/B shift；
- append-only base/reacquire attempt 骨架、remote-only runner、Python/shell 双 cleanup；
- `R-PASS`、`R-REFERENCE-EPOCH`、`R-REFERENCE-UNSTABLE`、`R-STRIP-CLASS-HIGH`、`uncertainty_unresolved` 分支矩阵；
- P6、v1、waiting policy、旧 sentinel evidence 与 replay hash。

Planner 对 P7-R1 physical budget 的决定：

```text
logical captures                     = 82
auto-exposure cache misses           = 8
maximum physical per cache miss      = 12
extra auto-exposure physical CR3     = 8 * (12 - 1) = 88
maximum one-shot weak reacquires     = 80
absolute hard cap                    = 82 + 88 + 80 = 250
```

因此 `250` 从 `proposed_not_frozen` 改为 **Planner-frozen absolute hard cap**，不是预计拍摄量，也不得增加。`82..170` 只能命名为 `baseline_physical_range_without_weak_reacquire`；包含 weak reacquire 的允许范围是 `82..250`。最长 60 秒 settling 仍为 `9600 s`。冻结上限不等于授权执行；只有 P7-R0D evidence audit 验收后，Planner 才能另行授权 exact named experiment。

上述问题是既定 58-feature、coverage、solver/target 架构内的实现合同缺口，不需要 Advisor 决策。Goal 继续保持 `Blocked`。

#### 8.7.21 P7-R0D 唯一离线收口阶段

P7-R0D 只允许修复 `R0C-REV-001/002` 及其行为测试、readiness、docs/skill/本计划状态。不得修改联合 coverage 数学、repeatability 阈值、58-feature、solver 预算、target 语义、P6 manifold 或任何 frozen artifact。

##### A. Formal v2 analyzer 必须从原始证据重建 target 事实

1. 对每个 target 建立 capture/command/sample/attempt 索引；sample observation 中的 `capture_id` 必须唯一指向同 target、同 source、同 phase 的 `captures.jsonl` 行，且 requested strip command 必须与 sample command 完全一致。对 12 个 reference anchors 同样从 plan target 重建 expected Ray HSI readback，并把 `reference-anchors.jsonl`、capture 与 command event 一一关联。不得只相信 row 内 `logical_observations_used`、`physical_budget` 或 anchor analysis 的 pass 字段。
2. 从 retained capture 与 auto-exposure audit 重算 target physical CR3：
   - fixed capture 为 1；auto-exposure 必须由 `trials + final + rejected_finals` 结构重算，不能只相信 `capture_count`；
   - weak reacquire 单独计数，base 与 reacquire 都保留；
   - 重算值必须等于 `HsiPhysicalBudget.events` 逐项求和及 `physical_cr3_used`，并分别满足 auto/weak/total cap；
   - target 下所有 capture 必须被某个 solver observation 或明确的 bounded reacquire/exhaustion evidence 消费，禁止孤儿 capture。
3. 重建每个 start 的 logical ledger：sample、measurement rejection、started confirmation group、probe/rebase/feedback phase 和 pre-capture exhaustion 必须能解释 `consumed` 各项；sum 必须等于 per-start/target logical count。任何缺失、重复、越界或无法解释的 observation 均拒绝。
4. 对**所有 starts**而不只是 selected start 审计 confirmation：
   - `confirmed|failed` group 必须恰好 n=3/n=5，sample index 有效且所有 command 等于 candidate command；
   - partial group 只能由明确 measurement rejection、physical exhaustion 或安全失败中止，capture 数与证据一致；
   - 每 start 最多两组，confirmed attempt 必须优先选择；`selected_result`、`best_valid_sample`、`selected_command` 和 multiseed overall status 必须从 attempts 重新推导。
5. 从 selected result、confirmation spread 和 feedback status 重新推导唯一 `result_status`：
   - `faithful` 必须是 confirmed 且 spread pass；
   - confirmed 与 `unconfirmed|solver_budget_exhausted|measurement_unreachable` 不能并存；
   - spread fail 或 coordinate `unresolved|uncertainty_unresolved` 必须进入 `uncertainty_unresolved`；
   - analyzer 不得把语义不一致 target 标为 ready。
6. Formal P7 的 source/off/readback event 也必须复用 B.1 的共享 validator；reference anchor readback、strip requested command、首次与末次 off response 任一不一致均拒绝。
7. `target_evidence_validation.budget_audit/status_exclusivity/confirmation_group_audit` 只有在上述重建全部通过后才能写 `pass`；报告需同时输出自报值与重算值，便于 Planner 对照。

##### B. P7-R1 runner/analyzer 必须验证冻结 plan，而非日志内部自洽

1. 为 source command/off response 建立一个共享、窄职责 validator，供 formal P7 与 P7-R1 的 runner/analyzer 使用；不要在四处复制略有差异的条件。它必须：
   - Ray HSI readback 精确匹配 plan `hue/sat/intensity`；
   - strip response 精确匹配 plan 五通道 command 或同一 frozen curve 生成的 payload；
   - `both_off` 的 strip response 必须为全零 payload，Ray response 必须明确显示 intensity 0；
   - event grammar 必须恰为 `both_off -> one expected source_on/readback -> both_off`，ambient 只能有两个 `both_off`；拒绝异源 on、重复 on、未知/孤儿 command event。
2. Runner 在任何 on/settling/capture 前验证第一次 `both_off` response；capture 后的 `both_off` 也必须验证并落盘。任一 mismatch 进入 failure evidence 和 Python cleanup，shell trap 保持不变。
3. Analyzer 必须从 `plan_step` 重新构造 expected Ray/strip state，不接受 event 与 attempt 一起被一致改错。Base 与 weak reacquire 都独立验证 exact command/readback/off/on/off。
4. 存在 weak reacquire 时：base 必须保留 weak-only quality rejection且 `selected_for_formal=false`；reacquire 必须 `selected_for_formal=true`、无 quality rejection、recorded exposure/58 features 合法，logical row capture/readback/feature provenance 必须指向 reacquire。无 reacquire 时只能选择通过质量门的 base。
5. 从 retained attempts 与详细 auto-exposure audit 重算并逐一比对 `run.json`：
   - `logical_captures_completed`、`formal_captures_completed`；
   - `physical_cr3_count`、`base_physical_cr3_count`；
   - `auto_exposure_cache_miss_count`、`auto_exposure_physical_cr3_count`；
   - `weak_signal_reacquire_count`、`weak_signal_reacquire_physical_cr3_count`。
6. 同时验证每次 auto-exposure `<=12`、总 auto physical `<=96`、cache miss `<=8`、weak count/physical `<=80`、total `<=250`。Runner 的 pre-call remaining budget 和 analyzer 的 post-run recomputation 必须独立成立。
7. 更新 schema/readiness 名称：
   - `baseline_physical_range_without_weak_reacquire = [82,170]`；
   - `permitted_physical_range_with_weak_reacquire = [82,250]`；
   - `maximum_total_physical_cr3 = 250`；
   - `absolute_cap_status = planner_frozen`；
   - `maximum_60_second_settling_seconds = 9600`。

##### C. 必须新增的 deterministic 反例测试

以下每项都必须先证明当前 `b477903` 会错误接受或缺少保护，再断言修复后 fail closed：

1. fake v2 sentinel 实际有 capture evidence，但 target/self-reported logical 与 physical 同时改成 0；analyzer 必须拒绝。
2. `goal_confirmed=true` 与 row `result_status=unconfirmed`；analyzer 必须拒绝。
3. 未 selected start 的 malformed/超额/错误 command confirmation group；analyzer 必须拒绝。
4. sample `capture_id` 指向另一 target、重复 capture、孤儿 capture、auto-exposure audit count 与结构不一致；逐项拒绝。
5. Formal v2 reference anchor 的 command/anchor/logical readback 一致改成错误 Hue/SAT，或首次/末次 off response 非零；analyzer 必须按冻结 plan 拒绝。
6. P7-R1 计划 H0/S0，但 command/attempt/logical readback 一致改成 H1/S0；analyzer 必须按冻结 plan 拒绝。
7. P7-R1 strip response 与 attempt 自洽但不等于 frozen command/payload；拒绝。
8. 非零 `both_off` response、Ray attempt 混入 strip-on、重复 source-on、孤儿 command event；逐项拒绝，runner mismatch 路径仍执行 Python cleanup。
9. `base_physical_cr3_count`、logical/formal counter、auto total、单 cache miss、weak 或 total 任一 one-over/mismatch；逐项拒绝，adapter one-over 仍在调用前拒绝。
10. weak reacquire 后错误选择已 rejected base，或 reacquire 自身质量/recorded exposure/readback 不合法；拒绝并保留两次 attempt 证据。
11. 保留成功路径：82 logical/80 formal、无 weak 与一次 weak 两种 fake run 均通过 analyzer/finalizer，candidate 仍 `formal_capture_eligible=false`。

##### D. 验证、交接与停止条件

1. 复跑 focused P7、full suite、`compileall`、四个 P7 wrapper `zsh -n`、`git diff --check`、`codegraph sync`。
2. 重新生成 P7-R0D fake formal-v2 analysis、P7-R1 dry-run 与 offline-readiness；不得复用或覆盖 R0C 证据目录。
3. Readiness 必须明确：solver/repeatability 已接受；formal evidence audit 是本轮新增；250 为 Planner-frozen hard cap；真实 reference/repeatability 统计仍未测；named experiment 仍未授权。
4. Executor 完成后更新本节证据、当前状态和唯一下一动作，然后停止并交还 Planner。不得自动 health/config/all_off、不得创建 real run 目录、不得调用设备或网络。
5. 若严格 source/off response 无法由现有 API 返回值证明，停止并把具体字段/缺口交还 Planner；不得把“命令调用未抛异常”写成 exact readback。只有该情况可能需要 Planner 决定是否增加显式 device-state query；仍不需要 Advisor，除非必须改变测量/solver/coverage 语义。

P7-R0D 验收前 Goal 继续保持 `Blocked`；`p7_targeted_reference_repeatability_v2`、新 sentinel、remaining 9、boundary、holdout 与 P8 全部锁定。

#### 8.7.22 P7-R0D Executor 离线收口结果（2026-07-18）

```text
status = offline_complete_waiting_for_planner_review
named_experiment_authorized = false
device_or_network_calls = 0
focused_tests = 31/31
full_suite = 402/402 in 99.519 s
```

已完成 `R0C-REV-001/002` 的既定架构内收口：

- 新增共享窄职责 source evidence validator。Formal v2 与 P7-R1 runner/analyzer 均验证首次/末次 strip 五通道零与 Ray intensity zero，并严格要求 ambient 为 `both_off -> both_off`、单源 attempt 为 `both_off -> exact source_on/readback -> both_off`；异源、重复、未知和孤儿 event fail closed。
- Formal v2 analyzer 从 `captures.jsonl`、sample observation、confirmation group、measurement rejection、command event、auto-exposure 结构与 physical event ledger 重建每个 target 的 logical/physical/status/selection。报告同时输出 self-reported 与 recomputed 值；修改计数为零、confirmed/status 冲突、重复 capture ID、auto audit 漂移和 anchor 共同篡改均被 deterministic tests 拒绝。
- P7-R1 analyzer 逐 logical capture 对照冻结 `plan.captures`，从 retained report 重算 58 features，从 `trials + final + rejected_finals` 重算 auto physical，验证 base/reacquire selection，并重算 logical/formal/base/auto/weak/total 全部 run counters。Runner 在 on/capture 前与 capture 后即时验证并落盘 off response；mismatch 仍进入 Python cleanup。
- P7-R1 schema 冻结为 `baseline_physical_range_without_weak_reacquire=[82,170]`、`permitted_physical_range_with_weak_reacquire=[82,250]`、`maximum_total_physical_cr3=250`、`absolute_cap_status=planner_frozen`、`maximum_60_second_settling_seconds=9600`。冻结上限不构成执行授权。

Retained evidence（全新目录，未复用 R0C）：

```text
run_dir = tmp/strip-hsi-pilot-offline/p7-r0d-v2-20260718-final-verified
p7-r0d-v2-replay.json = 69914a5f99eac880ab290804cb79592b8e879ee3ab2cb9ba4ccb0210ab4bd988
p7-r1-dry-run/plan.json = 42e748299e70ea2ee90d59bdecaf00f3c77b1cf08c0980450b2b6762a62927fd
v2-fake-sentinel-analysis.json = 72acbfb7a6ef63af2d3ec1ac888eccc6d932a46db61267bc40a26fa613e2057f
offline-readiness.json = f7f53dbbb21d7262ee7ef7e6b7c83d25f2310522b0c534e42ac024d45604aff0
```

验证通过：focused P7 `31/31`；full suite `402/402`（`99.519 s`）；`compileall`；四个 P7 wrapper `zsh -n`；`git diff --check`；`codegraph sync`。Fake formal analysis 为 `ready_for_sentinel_branch` 只表示离线 runner/analyzer integration 通过，不是实测 sentinel 或 named experiment 放行。当前 epoch reference compatibility、pre/post stability、四类 strip variance、新 sentinel-v2 convergence 与后续阶段仍未实测。

本节完成后停止并交还 Planner。Goal 继续保持 `Blocked`；Advisor 不需要介入，除非 Planner 判断必须改变 58-feature、联合 coverage 或 solver/target 架构。

#### 8.7.23 P7-R0D Planner 复验结论（2026-07-18）

```text
planner_verdict = reject
reviewed_checkpoint = 27a68cfb3a7d48e3cfbb620bb1575adf3e003e51
reviewed_readiness_sha256 = f7f53dbbb21d7262ee7ef7e6b7c83d25f2310522b0c534e42ac024d45604aff0
device_or_network_calls = 0
named_experiment_authorized = false
```

`27a68cf` 的提交边界、readiness hash 和既有 `31/31` focused tests 均可复现，但这些测试没有覆盖完整的冻结证据合同。Planner 对 retained fake run 做独立一致篡改后，确认以下 fail-open；因此不得接受 `raw_evidence_reconstruction_fake_integration_pass`，也不得执行 P7-R1：

1. **R0D-REV-001，Critical，strip 并无设备状态 readback。** `control.esphome.async_light()` 在 `execute_service()` 后返回本机刚构造的 payload；当前 firmware 没有导出五通道状态或 generation。`hsi_source_evidence.validate_strip_response()` 接受这个本地 payload，并把它报告为 exact response。它只能证明请求已发送且调用未抛异常，不能证明设备当前状态；这正好触发 8.7.21-D.5 的停止条件。
2. **R0D-REV-002，High，confirmed 状态仍信任自报布尔值。** 把唯一 confirmation group 改为 `failed`、保留 `goal_confirmed=true` 并同步 feasible count 后，formal v2 analyzer 仍输出 `ready_for_sentinel_branch`。`faithful` 尚未由 confirmation groups 唯一反推。
3. **R0D-REV-003，High，physical 子预算仍可由 row 自行放宽。** 把首个 auto-exposure 的结构重算为 11 CR3，同时把 row 的 `autoexposure_cap` 从冻结的 10 改成 11，analyzer 仍通过。hard cap 虽对照 plan，但 auto/weak cap 没有全部对照冻结 solver budget。
4. **R0D-REV-004，High，capture owner 与 RAW feature provenance 不完整。** 同一 capture 可同时作为 sample 和 measurement rejection 被重复消费；sample `observation.feature_values` 可与其 patch-statistics report 不同；两种篡改都仍输出 ready。因 objective/feasible 也未从 report features 通过正式 v2 evaluator 重算，faithful 结论仍可脱离 RAW evidence。
5. **R0D-REV-005，High，P7-R1 没有验证完整有序 plan。** 在 82 条 logical rows 中删除第二个 ambient plan step，并用第一个 ambient row/attempt/commands 重复填充，总数仍为 82 时，正式 analyzer 输出 `calibrated_waiting_for_planner`。当前只验证每条 row 能在 plan 中找到，没有验证 capture IDs 与顺序恰好等于完整 frozen plan。

以上是证据归属、状态机审计和设备控制边界问题，不改变 58-feature、联合 coverage、P6 manifold、solver/target 架构或冻结预算；本轮不需要 Advisor。若后续发现必须改变上述测量数学或 solver 语义，再单独交还 Advisor。

#### 8.7.24 P7-R0E 唯一离线收口阶段

P7-R0E 只允许修复 `R0D-REV-001..005`、行为测试、readiness、docs/skill 和本计划状态。允许离线修改 formal/R1 analyzer、共享 source-evidence 边界、ESPHome host client 与 firmware 配置，但**不得刷写 firmware、连接设备、读取 `.env`、访问网络或创建真实 run**。不得修改联合 coverage 数学、阈值、58-feature、P6 manifold、solver rounds/starts/rebases、`54/67`、`62/75`、R1 `82..250` 或 target 集。

##### A. Formal v2 必须完成真正的 RAW-to-status 重建

1. `target-results.jsonl` 顺序必须逐项等于 `plan.targets`；不能只比较 target set。只有这样才能按 runner 规则重建每个 target 的 `previous_command`。
2. 建立全 run capture-owner table。每个 target capture 必须且只能归属于一个 sample、一个 measurement rejection，或一对有明确 weak-only base/reacquire provenance 的 bounded reacquire evidence；sample/rejection 间重复、两个 rejection 重复、跨 target、错误 source/phase/purpose、未知 owner 均 fail closed。
3. 对每个 sample 从其 capture 的 `patch_statistics` 调用 `required_hsi_features_from_report()` 重算严格有序的 58 features；与 `sample.observation.feature_values` 不一致即拒绝。不得把 sample 内 feature map 当原始事实。
4. 加载 plan 冻结的 Ray manifold 与 v2 policy，按 runner 使用的 target、repeatability class、command、`previous_command`、max_code 调用现有 `evaluate_hsi_observation_v2()`。逐 sample 比较重算 residual/objective：类别、状态、feasible、hash、command continuity 必须精确一致；有限浮点只允许预声明的极小数值比较容差，禁止重新分类或放宽 gate。
5. 对每个 start 从 confirmation groups 反推 `derived_goal_confirmed`：只有存在一个合法 `confirmed` group，且恰有 n=3/n=5 个互不重复、同 command、重算 objective feasible 的 samples 时才为 true。`result.goal_confirmed`、`result.status`、multiseed status、selected start 与 row status 必须全部等于重算值；没有 confirmed group 时绝不能得到 `faithful`。
6. 从 confirmed group 的重算 feature samples，使用冻结 class variance/limit 重算 `confirmation_spread`；不得相信 row 内 decision。spread fail/unresolved 与 coordinate unresolved 按既有 frozen 状态表推导，不能改状态语义。
7. `hard_cap`、`autoexposure_cap`、`weak_reacquire_cap` 必须逐项等于 `plan.targets[*].solver_budget`。再从 `trials + final + rejected_finals` 和 owner table重算 events/subtotals；任何 row 自行抬高 cap、单项超限、重复 physical owner 或结构/总数不一致均拒绝。
8. `target_evidence_validation` 报告新增 capture-owner、feature-provenance、objective-replay、confirmation-derived-status、frozen-sub-budget 五项；只有全部通过才允许总体 `pass`。

##### B. P7-R1 必须逐项等于完整 frozen plan

1. `captures.jsonl` 的 `(capture_id, plan_step)` 序列必须与 `plan.captures` bit-for-bit 同序同长；capture ID 必须唯一。禁止以重复 plan step 替代缺失 step。
2. attempt ID 必须唯一；每个 logical ID 恰有一个 base，最多再有一个紧随其后的 weak reacquire。attempt/command key 集必须与完整 capture plan 精确对应，不得只比较去重后的 set。
3. Base 的 source、auto-exposure policy、exposure key、state/command/block/repeat/formal flags 全部从 plan step 重建；详细 auto audit、selected attempt、feature report、weak-only rejection 和全部 run counters继续按 8.7.21-B 验证。
4. 新增缺 step + 重复另一 step、重复 capture ID、乱序、缺 base、重复 attempt ID、把 planned auto miss 改成 fixed、以及 ambient 重复替换的 deterministic fail-closed tests。

##### C. 区分请求 payload 与设备报告状态

1. 保留现有 `control.esphome.light()` 的 command-only 兼容语义；其返回值必须命名/记录为 `requested_payload` 或 `command_acknowledgement`，禁止再称 readback。
2. 在 firmware 中增加原子、可订阅的五通道 device-state snapshot，并包含每次 `set_rgbww_12bit`/`all_off` 后单调递增的 generation。boot 必须初始化并发布全零。该状态代表“设备报告的 commanded PWM state”，不宣称测得电流、PWM 波形或光输出。
3. host 侧新增窄职责 verified API：动作前先取得 baseline generation，执行 service 后等待 generation 严格增加且五通道恰等于映射后的 expected payload；缺 entity、旧 generation、超时、任一通道不符均 fail closed。不得用本地 `_build_payload()` 结果冒充 snapshot。
4. Formal P7 与 P7-R1 runner 只能注入 verified API；command evidence 必须同时保存 requested payload 和独立 device snapshot provenance。共享 validator 只接受明确的 device-state schema，拒绝旧 bare payload。
5. fake backend 必须把 requested state 与 simulated device state 分开；新增“请求正确但设备状态旧/错误”的测试，证明本地 echo 无法通过。所有 mismatch 仍进入 Python cleanup，wrapper 的 shell trap 不变。
6. 如果当前 ESPHome/aioesphomeapi 无法实现动作前后 generation snapshot，Executor 停止并记录具体 API 缺口；不得降级为 command acknowledgement。该控制边界仍由 Planner 决定，不需要改变测量数学。

##### D. R0E 必测反例与验证

1. 逐项固化本节五个 Planner repro，修复前证明 `27a68cf` 接受，修复后断言拒绝。
2. Formal 新增：无 confirmed group 但布尔值 true、sample/rejection 重复 owner、rejection/rejection 重复、RAW feature mismatch、objective/feasible/status 同步伪造、auto/weak cap 抬高、confirmation spread 伪造。
3. R1 新增：ambient duplicate replacement、任一 plan step 缺失/乱序、duplicate capture/attempt、auto policy 漂移、selected provenance 漂移。
4. Device-state 新增：bare payload、stale generation、generation 倒退、通道 mismatch、missing entity、subscribe timeout、重复设置同值但 generation 未增加；全部 fail closed。成功 fake path需证明 generation 增加且 snapshot 来源独立。
5. 复跑 focused P7、full suite、`compileall`、firmware config/compile 的**纯离线可用检查**、四个 P7 wrapper `zsh -n`、`git diff --check`、`codegraph sync`。若 firmware compile 需要下载依赖，记录 blocked，不得联网补装。
6. 使用全新目录生成 fake formal-v2、P7-R1 fake/dry-run 与 `offline-readiness.json`。Readiness 必须明确 `device_state_readback = offline_fake_only`、真实 firmware 尚未刷写/验证、named experiment 未授权。

##### E. R0E 离线出口

- 所有反例 fail closed、成功 fake 通过且离线检查完成：`offline_complete_waiting_for_planner_review`，停止并交还 Planner；
- 设备状态 API 在离线层面不可实现：`blocked_device_state_contract`，保留技术缺口并交还 Planner；
- 任何 solver/coverage/feature 数学必须改变：停止并交还 Planner，再决定是否请 Advisor；
- 无论哪个出口，均不得自动调用 health/config/all_off、刷 firmware 或启动 P7-R1。

#### 8.7.25 设备状态 readback 的独立实机门

R0E 离线验收通过后，也**不能**直接授权 P7-R1。必须先由用户另行明确授权 exact named preflight：

```text
p7_strip_state_readback_preflight
```

该 preflight 与 `p7_targeted_reference_repeatability_v2` 是两个独立授权：

1. 若需要刷写新 firmware，先报告固件 diff、目标设备和 recovery 路径，取得明确 firmware-upload 授权；未授权则不刷写。
2. 通过独立 wrapper 执行，Ray 全程保持 off；先验证 boot/off snapshot，再使用一组各通道不同且 `max PWM <= 64` 的低输出五通道命令，重复同一命令一次以验证 generation 仍递增，最后回到全零。
3. 每次保存 requested payload、baseline generation、device snapshot、设备 identity 和时间；任何 mismatch/timeout 立即停止。
4. Python finally 与 shell trap 都调用 all-off；结束后再读取全零 snapshot。若读回失败，仍执行 recovery all-off，并把结果标为安全状态未知，禁止继续。
5. preflight 通过后停止并交还 Planner。只有 Planner 接受该 device-state evidence，用户再单独授权 `p7_targeted_reference_repeatability_v2`，才允许执行 P7-R1；不得合并授权或自动串行。

---

#### 8.7.26 Executor P7-R0E 离线执行结果（2026-07-18）

```text
current_phase = P7_R0E
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = a380dfe63c732ddf126e8aa396a41b2985da4713
worktree_state = dirty(本节及 P7-R0E 实现，保留 Planner 既有修改)
authorization = offline_only; p7_targeted_reference_repeatability_v2 未授权
run_dir = tmp/strip-hsi-pilot-offline/p7-r0e-v3-20260718-final
analysis = P7-R0E 五个 fail-open 已在离线 analyzer/fake backend 中 fail closed；fake formal-v2 通过；R1 dry-run 仍 formal_capture_eligible=false
completed_steps = verified ESPHome API + generation-bearing firmware schema; strict source evidence validator; v2 RAW/58-feature/objective/confirmation/owner/sub-budget replay; R1 exact plan/order audit; readiness artifact
failure_evidence = firmware CLI 未安装，无法进行 ESPHome compile；仅完成自定义 tag YAML 结构检查，未联网补依赖
cleanup_evidence = fake mismatch/timeout tests 均 fail closed 并验证 disconnect；四个 wrapper zsh -n 通过；本轮未调用设备、网络、.env、firmware upload 或真实 all_off
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0E_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = 交还 Planner 验收；若接受，另行申请 p7_strip_state_readback_preflight，仍不得自动授权 P7-R1
```

Evidence:

- `offline-readiness-v4.json` SHA-256 `149a5c009d13010a2cdd31c6dff7f9a45c73a732e7dcf61925c739db16604ad2`（fake formal run 的 policy path 已保留在新 artifact 目录外的 retained 文件）。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `ff9b9da3078daa279274c4b4a5da0defb360d6a2d2e934dbf68373469839b8df`。
- focused P7/device suite `37/37`；full suite `408/408`；`compileall`、四个 wrapper `zsh -n`、`git diff --check`、`codegraph sync` 通过。
- firmware compile 状态保持 `blocked_tool_missing_esphome_cli`；结构解析不是 firmware compile，也不构成刷写或实机 readback 证据。

Gate remains `Blocked`: no named experiment, no device preflight, and no P7-R1 execution authorization is inferred from this offline result.

#### 8.7.27 P7-R0E Planner 复验结论（2026-07-18）

```text
planner_verdict = reject
reviewed_checkpoint = 2cbfe1377a74e7dc9cb3925b9d2ff565e0ed1e9f
reviewed_readiness_sha256 = 149a5c009d13010a2cdd31c6dff7f9a45c73a732e7dcf61925c739db16604ad2
device_or_network_calls = 0
named_experiment_authorized = false
```

R0E 的五个原有 fail-open 均已被独立重放验证为拒绝，generation-bearing fake device-state 路径也按预期拒绝 bare payload、旧 generation 和 channel mismatch。但仍存在一个会改变 solver 账本的证据漏洞：向 start 的 `measurement_rejections` 添加

```json
{"phase":"feedback-0","evidence":{}}
```

并同步自报 logical count/budget 后，formal v2 analyzer 仍返回 `ready_for_sentinel_branch`。该 rejection 没有 capture owner、没有质量拒绝证据，也没有明确的 pre-capture budget exhaustion 结构，却被当作一个合法 logical observation 计入。因而 R0E 仍不能验收，`p7_strip_state_readback_preflight` 和 `p7_targeted_reference_repeatability_v2` 均保持锁定。

该问题属于证据合同完整性，不改变 58-feature、coverage、P6 manifold、solver 或预算数学；不需要 Advisor。固件 compile 工具缺失仍是另一个独立事实，不得用 fake API 测试替代真实 firmware compile/readback。

#### 8.7.28 P7-R0F 唯一离线修复阶段

##### A. 明确区分两类 rejection

1. `measurement_rejected` 必须包含非空 `evidence.capture_ids`；每个 ID 必须存在于 retained captures、属于同一 target/source/phase、尚未被 sample/rejection/weak-base owner 消费，并经过共享 owner table 唯一认领。
2. `measurement_rejected` 的 evidence 必须包含冻结 schema 所需的 rejection reason、command/phase 和 quality evidence；空 mapping、缺 `capture_ids`、未知 status、跨 target 或仅同步修改 logical count 均拒绝。
3. 只有真正发生在 capture 之前的预算耗尽，才允许没有 `capture_ids`。它必须使用独立的 `pre_capture_exhaustion` schema，至少包含 `status=solver_budget_exhausted`、`sub_budget`、`phase`、`requested_physical_cr3`、当前各 physical counters 和明确的 `capture_attempted=false`；它不消费 capture owner，也不能伪装成 measurement quality rejection。
4. 从 samples、rejections 和 pre-capture exhaustion evidence 重算 logical ledger；`len(samples)+len(rejections)` 仍必须等于 start ledger，但每个 rejection 的类别和 owner 必须可审计。`measurement_unreachable`、`solver_budget_exhausted`、`unconfirmed` 和 `faithful` 的既有状态语义不变。

##### B. 必测反例

在修复前保留并证明 `2cbfe13` 接受，修复后全部 fail closed：

1. 空 `evidence`；
2. 缺失 `capture_ids`；
3. `capture_ids=[]`；
4. capture ID 重复占用或 sample/rejection 交叉占用；
5. quality rejection 伪装成 `pre_capture_exhaustion`；
6. 合法 physical budget exhaustion 的无 capture evidence 成功通过；
7. 弱信号 rejection 缺少 base/reacquire 两次 capture 或质量证据；
8. 与此前 R0D 五类篡改组合后的 logical/status/physical counter 一致伪造。

##### C. 离线出口

1. 只修改 formal analyzer、共享 evidence schema、测试、readiness、docs/skill 和本计划；不得改 firmware、solver、coverage 或执行接口。
2. 生成全新 fake formal-v4、R1 dry-run 和 readiness artifact；不覆盖 R0E 证据。
3. 复跑 focused、full suite、compileall、wrapper `zsh -n`、`git diff --check`、CodeGraph；ESPHome CLI 缺失继续明确记录为 `blocked_tool_missing_esphome_cli`，不得联网安装。
4. 只有空 rejection 及其变体全部拒绝、合法 pre-capture exhaustion 通过、既有五类反例仍拒绝，才可写 `offline_complete_waiting_for_planner_review` 并交还 Planner。
5. R0F 通过也不产生任何实机授权；下一唯一高风险动作仍是用户明确授权的 `p7_strip_state_readback_preflight`，且必须先解决 firmware compile 门禁。

#### 8.7.29 Executor P7-R0F 离线执行结果（2026-07-18）

```text
current_phase = P7_R0F
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = 2cbfe13 (待本轮 focused commit)
worktree_state = dirty(Planner R0F decision plus offline analyzer/docs/tests)
authorization = offline_only; p7_strip_state_readback_preflight and p7_targeted_reference_repeatability_v2 locked
run_dir = tmp/strip-hsi-pilot-offline/p7-r0f-v4-20260718-final
analysis = empty/missing/duplicate/forged measurement rejection evidence now fail closed; explicit pre_capture_exhaustion schema validates; fake formal-v4 and R1 dry-run generated
completed_steps = rejection schema validator; owner/phase/source/quality checks; pre-capture exhaustion contract; required regression matrix; docs/skill update; readiness artifact
failure_evidence = firmware CLI remains unavailable; YAML structure check only, no firmware compile or flash
cleanup_evidence = focused 38/38; full 409/409; compileall, four wrapper zsh -n, git diff --check and codegraph sync pass; no device/network/.env/real all_off calls
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0F_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = Planner review only; no real preflight or named experiment inferred
```

Evidence:

- `offline-readiness-r0f.json` SHA-256 `a760710064eb901c1cda64d16c0b6ab9e474973c8a8e5b5daf96147088095d14`。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `a1609cff00e83c01c23b89f40b9526124041436d060c52ff215ba34f15e3239f`。
- ESPHome compile remains `blocked_tool_missing_esphome_cli`; fake device-state tests are not firmware/readback evidence.

Gate remains `Blocked`: R0F completion does not authorize `p7_strip_state_readback_preflight` or `p7_targeted_reference_repeatability_v2`.

#### 8.7.30 P7-R0F Planner 复验结论与 P7-R0G（2026-07-18）

```text
planner_verdict = reject
reviewed_checkpoint = 5dfb73423d5366377bd020ff23ba163e1ea7de3c
reviewed_readiness_sha256 = a760710064eb901c1cda64d16c0b6ab9e474973c8a8e5b5daf96147088095d14
device_or_network_calls = 0
named_experiment_authorized = false
```

R0F 的空/缺失/重复 measurement rejection 反例均已拒绝；但 pre-capture exhaustion 仍只是字段形状校验，没有从 start budget 和 retained capture ledger 独立重建。对 fake formal-v4 做如下篡改后 analyzer 仍返回 `blocked_for_planner_review`，而不是拒绝：

- 把 confirmation group 改成 partial、附加 `capture_attempted=false` 的 exhaustion；
- 任意修改 exhaustion `phase`、`physical_cr3_used` 和 auto/weak counters；
- 额外加入 `capture_ids`，与 `capture_attempted=false` 语义矛盾。

这允许伪造 solver exhaustion 状态和当前物理计数，仍可影响 target 分支。R0F 因此不能验收；设备 preflight 与 P7-R1 继续锁定。该问题仍是证据/账本完整性，不需要 Advisor。

##### P7-R0G 必须完成的离线修复

1. `budget_exhaustion` 必须与同一 start 的 `result.budget.exhaustion`（或正式 runner 生成的等价字段）逐字段一致；缺失、只写 top-level、或两处不一致均拒绝。
2. 由 samples、合法 measurement rejection 和每个 capture 的 physical audit 重算该 start 的 logical/physical/auto/weak counters；exhaustion 中的当前计数必须逐项相等，不能接受任意非负整数。
3. 从 `HsiStartBudget` 冻结 limits 与 consumed ledger 独立推导 `sub_budget`、下一次 phase 和 exhaustion 原因；phase 不得是任意字符串，也不能和已经完成的 capture phase 冲突。
4. `capture_attempted=false` 时，exhaustion evidence 不得含 `capture_ids`，且不得存在对应的 retained CR3；若 runner 在预算检查前写入 `both_off` 审计，只能记录为未产生 capture 的 setup event，不能被计入 physical owner。
5. 正常 measurement rejection、合法 pre-capture exhaustion、solver budget exhausted with best-valid sample 三种路径分别建 fake fixture，状态和 owner 账本必须互不混淆。
6. 新增反例：top-level-only exhaustion、budget.exhaustion 缺失、phase drift、counter one-over/under、capture IDs 与 `capture_attempted=false` 冲突、已产生 CR3 仍自报 false，以及 partial group 与 exhaustion 不一致。
7. 保留并重跑 R0D 五类与 R0F rejection schema 反例；只有所有伪造 exhaustion fail closed、合法 exhaustion 通过，才可生成全新 readiness 并交还 Planner。
8. 仍不得安装 firmware、使用 ESPHome CLI、连接设备或申请任何实机授权；固件 compile 缺口继续单独记录。

#### 8.7.31 Executor P7-R0G 离线执行结果（2026-07-18）

```text
current_phase = P7_R0G
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = 27d9f90fcd0e9fd6b2bbfe824424fc3c6e8b36bc
worktree_state = dirty(Planner R0G decision plus offline analyzer/tests/PLAN)
authorization = offline_only; p7_strip_state_readback_preflight and p7_targeted_reference_repeatability_v2 locked
run_dir = tmp/strip-hsi-pilot-offline/p7-r0g-v5-20260718-final
analysis = pre-capture exhaustion now binds to start budget exhaustion, recomputed per-start physical/auto/weak ledger, phase/sub-budget and capture_attempted=false; fake formal-v5 passed
completed_steps = per-start owner assignment; retained capture physical reconstruction; duplicated exhaustion ledger equality; phase/category consistency; forged counter/phase/capture-id regressions; R0D/R0F suites retained
failure_evidence = firmware CLI remains unavailable; YAML structure check only, no firmware compile or flash
cleanup_evidence = focused 38/38; full 409/409; compileall, four wrapper zsh -n, git diff --check and codegraph sync pass; zero device/network/.env/real all_off calls
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0G_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = Planner review only; no real preflight or named experiment inferred
```

Evidence:

- `offline-readiness-r0g.json` SHA-256 `2f35388a58743ac927d6dfff19af5975a79e4689e70616e4991c6105a5d7ef2c`。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `17e23687ed32bf0aa42e47f670c1e0e8de70defdf86fea6d145edd3f4c06387b`。
- ESPHome compile remains `blocked_tool_missing_esphome_cli`; fake device-state tests are not firmware/readback evidence.

Gate remains `Blocked`: R0G completion does not authorize `p7_strip_state_readback_preflight` or `p7_targeted_reference_repeatability_v2`.

#### 8.7.32 P7-R0G Planner 复验结论与 P7-R0H（2026-07-18）

```text
planner_verdict = reject
reviewed_checkpoint = 69698c18a1021214fd95751612396dc49ede402f
implementation_checkpoint = 27d9f9000b825459a6754b0699284bc84a61c47b
reviewed_readiness_sha256 = 2f35388a58743ac927d6dfff19af5975a79e4689e70616e4991c6105a5d7ef2c
device_or_network_calls = 0
named_experiment_authorized = false
```

R0G 已修复此前的任意 counter、capture-id 和 duplicated exhaustion ledger 篡改，但仍允许以下伪造：将 `sub_budget` 改成 `feedback_attempts`、`initial_probes` 或 `rebase_probes`，使用相应 phase 前缀，而对应 category 实际尚未达到冻结上限。`_phase_matches_sub_budget()` 对这些显式 category 只检查字符串前缀，没有检查 consumed 是否达到 category limit；同一 start 的 `budget.limits` 也未逐项与 frozen target solver budget 对照。fake analyzer 因此仍返回 `blocked_for_planner_review`，而非拒绝。

这仍是证据/账本完整性问题，不改变 solver、coverage、P6 manifold 或预算数学，不需要 Advisor。设备状态 preflight、firmware compile 和 P7-R1 继续锁定。

#### 8.7.33 P7-R0H 唯一离线修复阶段

1. 对 `initial`、`initial_probes`、`feedback_attempts`、`rebase_probes`、`confirmation_captures` 五类 exhaustion，均从 frozen `declared.solver_budget` 和实际 `budget.consumed` 独立推导 category limit；只有 `consumed >= limit` 才能接受对应 `sub_budget`。
2. 每个 start 的 `budget.limits` 必须与 target 的 frozen `solver_budget` 完全一致；不得使用 retained row 自报 limits 作为信任根。
3. `budget.exhaustion` 与 top-level `budget_exhaustion` 必须双向一致：一方存在而另一方缺失也拒绝；两者字段、start index、phase、sub-budget、counters 必须完全一致。
4. 对 `logical_observations` exhaustion，继续验证 category consumed、下一 phase 和所有 counters；对显式 category 不得只做 prefix 检查。
5. 新增 deterministic 反例：category 未耗尽但 phase 前缀匹配、limits 抬高、limits 降低、consumed one-under/one-over、top-level-only、nested-only、错误 category 与错误 phase 组合；合法五类 exhaustion 各至少一个 fake success path。
6. 保留 R0D、R0F、R0G 全部反例；生成全新 fake formal-v6、R1 dry-run/readiness，不能覆盖既有证据。
7. 复跑 focused/full suite、compileall、wrapper `zsh -n`、`git diff --check`、CodeGraph；ESPHome CLI 缺失继续记录，不联网补装。
8. 只有五类 category 的伪造 exhaustion 全部 fail closed 且合法路径通过，才可交还 Planner；仍不得连接设备、读取 `.env`、刷写 firmware、执行 preflight 或 P7-R1。

#### 8.7.34 Executor P7-R0H 离线执行结果（2026-07-18）

```text
current_phase = P7_R0H
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = d3b3531b2ed774b56b7fc5c57e65d556c543043d
worktree_state = dirty(Planner R0H decision plus offline analyzer/tests/PLAN)
authorization = offline_only; p7_strip_state_readback_preflight and p7_targeted_reference_repeatability_v2 locked
analysis = explicit category exhaustion now requires consumed >= frozen category limit; each start budget.limits equals frozen target solver_budget; dual exhaustion ledger remains mandatory
completed_steps = category limit derivation for all five categories; logical exhaustion retained; limits tamper and one-under/one-over regressions; fake formal-v6 and R1 dry-run/readiness generated
failure_evidence = firmware CLI remains unavailable; YAML structure check only, no firmware compile or flash
cleanup_evidence = focused 39/39; full 410/410; compileall, four wrapper zsh -n, git diff --check and codegraph sync pass; zero device/network/.env/real all_off calls
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0H_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = Planner review only; no real preflight or named experiment inferred
```

Evidence:

- `offline-readiness-r0h.json` SHA-256 `c03d11cd0c631d1454d548b5ad39493d681c0c02a2a2d02b34ae0a02d089c57c`。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `b74f26d0a6f311eecfbe22b43c7edd6f459f231bf35a00d9bd300bffcd31298d`。
- ESPHome compile remains `blocked_tool_missing_esphome_cli`; fake device-state tests are not firmware/readback evidence.

Gate remains `Blocked`: R0H completion does not authorize `p7_strip_state_readback_preflight` or `p7_targeted_reference_repeatability_v2`.

#### 8.7.35 P7-R0H Planner 复验结论（2026-07-18）

```text
planner_verdict = reject
finding = R0H-REV-001
reviewed_checkpoint = 140d40eebe85d36ebe1b4b97cf9a0bc242367c68
implementation_checkpoint = d3b353143aab30889b0b82cc1e26feaa0de8ca1d
reviewed_readiness_sha256 = c03d11cd0c631d1454d548b5ad39493d681c0c02a2a2d02b34ae0a02d089c57c
device_or_network_calls = 0
named_experiment_authorized = false
```

R0H 已通过本轮独立复验并应保留的部分：每个 start 的 `budget.limits` 已与 frozen target `solver_budget` 精确比较；五类显式 category exhaustion 已同时检查 phase prefix 与 `consumed >= frozen category limit`；`budget.consumed` 仍从 retained samples/rejections 重建。readiness 文件 SHA-256 与 Executor 报告一致。本轮没有连接设备、网络、读取 `.env` 或调用灯光。

`R0H-REV-001`：双 exhaustion ledger 仍是单向检查。formal analyzer 先读取 top-level `result.budget_exhaustion`；当它为 `None`/缺失时直接跳过后续校验，没有拒绝非空的 `result.budget.exhaustion`。独立 deterministic replay 在未改动任何 capture、command、RAW feature、objective、status 或 frozen limits 的正常 `goal_confirmed` attempt 中，仅写入一个伪造的 nested `budget.exhaustion`，analyzer 仍返回：

```text
status = ready_for_sentinel_branch
target_evidence_validation.budget_audit = pass
```

这违反第 8.7.33 节的“双向一致”合同，也允许一个已确认成功的 start 暗藏互相矛盾的 exhaustion 事实。现有 R0H 测试覆盖 top-level -> nested、helper 级 category one-under，但没有覆盖 nested-only 的 full-analyzer formal integration 反例；readiness 因此不能作为 P7-R1 前检查点。

该问题仍属于 formal evidence/ledger 完整性，不改变 58-feature、联合 coverage、solver/target 架构、P6 manifold 或冻结预算数学，不需要 Advisor 介入。R0H 的有效修复必须保留，不得回退。

#### 8.7.36 P7-R0I 唯一离线修复阶段

P7-R0I 只允许修复 `R0H-REV-001`、补齐 exhaustion formal integration fixtures/tests，并更新 readiness、docs/skill 和本计划状态。不得修改 solver starts/rounds/rebases、`54/67`、`62/75`、`82..250`、联合 coverage、58-feature、P6 manifold、target 集或设备协议。

1. 对每个 start 同时读取 `result.budget_exhaustion` 与 `result.budget.exhaustion`，在任何 early-continue 或 status derivation 之前执行对称校验：两者同时为 `None`/缺失才表示无 exhaustion；一方为 mapping 时另一方也必须为 mapping 且完整 JSON 精确相等；nested-only、top-level-only、空 dict、非 mapping 和字段差异全部 fail closed。
2. 任一 exhaustion mapping 存在时，该 start 的 `result.status` 必须严格为 `solver_budget_exhausted`，`goal_confirmed=false`，且不得存在 `confirmed` confirmation group。反向也必须成立：`result.status=solver_budget_exhausted` 必须有两份相同 ledger。一个未选中的 exhausted start 可以与另一个 confirmed start 共存，但 multiseed overall/selection/status 必须继续从全部 starts 重建，不得把 attempt status 直接提升为 row status。
3. 对通过对称校验的 mapping 继续复用 R0H 的 retained-capture counters、frozen `budget.limits`、reconstructed `consumed`、phase/sub-budget 和 `capture_attempted=false` 校验；不得建立第二套 category limit 逻辑，也不得信任 readiness 或 row 自报 `budget_audit`。
4. 增加 full-analyzer deterministic 反例，至少包括：正常 faithful/goal-confirmed attempt 的 nested-only forged exhaustion、top-level-only、两份 mapping 字段不一致、nested 空 dict、exhaustion 与 `goal_confirmed`/confirmed group 共存、`solver_budget_exhausted` status 但两份 ledger 缺一份。每个反例都必须从全新 formal fake run 进入公开 `analyze_strip_hsi_pilot(..., policy_version="v2")`，并断言抛出具体 `ValueError`；只直接测试 private helper 不算完成。
5. 补齐第 8.7.33 节尚未得到 formal integration 证明的合法路径：至少构造一个完整、可审计、包含实际 retained sample/rejection ledger 的合法 pre-capture exhaustion run，使公开 analyzer 接受；五类 category 可以共享 fixture 参数化，但每类都必须经过公开 analyzer。合法 exhausted start 的 category 必须真实达到 frozen limit，下一 phase 与 sub-budget 相符，双 ledger 相同，且 capture/counter owner 无 orphan。
6. 为合法 fixture 再做 `consumed one-under`、category one-over、错误 next phase、错误 sub-budget 和 frozen limits drift 反例。one-over 必须由 analyzer 的 per-category upper-bound 校验拒绝，不能只依赖总 logical cap 偶然拒绝；所有 category 的 `0 <= consumed <= frozen limit` 都要从 retained phase ledger重建后逐项验证。
7. 生成全新 `fake-formal-v7-run`、analysis、R1 dry-run 和 `offline-readiness-r0i.json`，不得覆盖 R0H 或更早证据。Readiness 必须列出上述 public-analyzer integration case 名称与结果，不能用 helper test 数量代替。
8. 复跑 focused P7/device suite、full suite、`compileall`、四个 wrapper `zsh -n`、`git diff --check` 与 `codegraph sync`。ESPHome CLI 仍缺失时只记录 `blocked_tool_missing_esphome_cli`，不得联网安装、刷写或访问设备。
9. 完成后 Goal 继续 `Blocked` 并交还 Planner。即使 R0I 全部通过，也不自动授权 `p7_strip_state_readback_preflight`、`p7_targeted_reference_repeatability_v2`、新 sentinel、remaining 9、boundary、holdout 或 P8。

#### 8.7.37 Executor P7-R0I 离线执行结果（2026-07-18）

```text
current_phase = P7_R0I
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = 60b07108f43a8ebbd52e2bb8a608b7b66ca0771e
worktree_state = dirty(Planner R0I decision plus analyzer/integration fixtures/readiness/docs/PLAN)
authorization = offline_only; all device and named-experiment gates locked
run_dir = tmp/strip-hsi-pilot-offline/p7-r0i-v7-20260718-final
analysis = public analyzer now rejects asymmetric/empty/mismatched exhaustion ledgers and confirmed/status conflicts; five legal category exhaustion fixtures pass; one-under/over and phase/sub-budget drift fail closed
completed_steps = symmetric early ledger validation; exhaustion/status/confirmation equivalence; per-category upper bounds; full public integration fixtures; fake formal-v7, R1 dry-run and readiness
failure_evidence = ESPHome CLI remains unavailable; no firmware compile/flash/device readback
cleanup_evidence = focused 42/42; full 413/413; compileall, four wrapper zsh -n, git diff --check and codegraph sync pass; zero device/network/.env/real all_off calls
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0I_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = Planner review only; no real preflight or named experiment inferred
```

Evidence:

- `offline-readiness-r0i.json` SHA-256 `d45fc5880e0a515539d7f5c5280c4f985536c3f772b6d065a0858284c8146e78`。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `c65e020966a07a6a2507b100863db416c26cc82d19a6cd198dd8d3a2a3c95f1a`。
- Readiness records all named public-analyzer accepted/rejected integration cases; ESPHome compile remains `blocked_tool_missing_esphome_cli`.

Gate remains `Blocked`: R0I completion does not authorize device preflight, P7-R1, new sentinel, remaining, boundary, holdout or P8.

#### 8.7.38 P7-R0I Planner 复验结论（2026-07-18）

```text
planner_verdict = reject
finding = R0I-REV-001, R0I-REV-002
reviewed_checkpoint = 719d28abb39d690945a77ef253ded3e6d1135ef2
implementation_checkpoint = 60b071021fd95c9007b3e697547b942adcad4bc8
reviewed_readiness_sha256 = d45fc5880e0a515539d7f5c5280c4f985536c3f772b6d065a0858284c8146e78
device_or_network_calls = 0
named_experiment_authorized = false
```

R0I 修复本身应保留：top-level/nested ledger 已在 per-start 主循环早期对称校验；exhaustion 与 `solver_budget_exhausted`/`goal_confirmed=false`/无 confirmed group 绑定；每类 `consumed` 已从 retained phases 重建并受 frozen upper bound 约束。上一轮 nested-only 反例现已由公开 analyzer 拒绝。readiness SHA-256 与 Executor 报告一致；Planner 独立复跑 `test_measure_strip_hsi_pilot + test_hsi_feedback + test_hsi_budget` 共 `33/33` 通过。

但 R0I 所称“五类合法 exhaustion public integration”是由测试 helper 直接拼装 `target-results.jsonl`、额外造出 partial confirmation group 和完整 exhaustion 字段，不是正式 `run_hsi_feedback_multiseed()` 与 `measure_strip_hsi_pilot` 实际产物。生产 round-trip 存在两个确定性不一致：

1. `R0I-REV-001`：用正式 solver 触发 `feedback_attempts` exhaustion 时，实际 top-level/nested ledger 只有 `status/start_index/phase/sub_budget`，`confirmation_attempts=[]`；没有 analyzer 强制的 `pre_capture_exhaustion`、`capture_attempted`、requested/physical/auto/weak counters。它先被“必须存在 final-verification group”拒绝，即使放宽该项也会被 exhaustion schema 拒绝。
2. `R0I-REV-002`：`feedback_capture()` 将 `HsiPhysicalBudgetExhausted` 作为 `measurement_rejected` 返回，multiseed 产物是 top-level physical exhaustion mapping、nested `budget.exhaustion=null`、`confirmation_attempts=[]`。R0I 的对称校验会直接拒绝正式 runner 自己生成的结果。并且 physical budget 是 target-wide，而 analyzer 目前只按 start 重算 counters，scope 未冻结。

此外，测试中声明为“合法”的五类 category 并不都能由当前状态机自然发出：fresh start 只消费一次 `initial`，initial probes 只建立一组，confirmation 先受 group reservation 管理；`HsiStartBudget` 还可能发出 `confirmation_groups`、`rebases`、`logical_observations`。在没有 production reachability 证明前，手工令五类都 pass 不能作为 formal 合同。

因此 `413/413` 证明现有 synthetic 合同内部一致，但没有证明 producer/consumer 一致，R0I 不能作为实机 preflight 或 P7-R1 前检查点。这仍是 runner/persistence/analyzer 证据边界问题，不改变 58-feature、联合 coverage、solver 数学、target 或冻结预算，不需要 Advisor。

#### 8.7.39 P7-R0J 唯一离线修复阶段

P7-R0J 只负责把正式 producer 与 formal analyzer 的 exhaustion 合同收敛，并以 runner-produced round-trip 取代手工成功 fixture。必须保留 R0I 的对称校验、status 绑定、category upper bounds 和全部 fail-closed 反例；不得修改 starts/rounds/rebases、`54/67`、`62/75`、`82..250`、58-feature、联合 coverage、P6 manifold、target 集或设备协议。

1. 先从 `run_hsi_feedback()` 的所有 `require_budget()`、`HsiStartBudget.consume/reserve_*()`、`HsiPhysicalBudgetExhausted` 和 multiseed catch 分支生成 exhaustibility matrix。每个 `sub_budget` 必须标记 `production_reachable`、`guarded_unreachable` 或 `fatal_accounting_error`，并列出触发调用点、capture 是否开始、counter scope 与正式 status。禁止继续假定测试 helper 中五类都可达。
2. 冻结两种 evidence origin，不得混用 counter scope：logical/start exhaustion 使用 `counter_scope=start`，由同 start 的 retained samples/rejections/captures 重建；physical target exhaustion 使用 `counter_scope=target`，由 target `physical_budget.events` 与 retained captures 重建。两者都必须明确 `capture_attempted`、requested/produced physical CR3、phase、sub-budget、start index，并在持久化前生成完全一致的 top-level/nested mapping。
3. canonical enrichment 必须位于正式 runner 拥有全部事实的单一边界；solver 不得伪造它看不到的 physical counters，analyzer 也不得调用 producer helper 作为信任根。允许在 `measure_strip_hsi_pilot` 的 result finalization 边界实现一个窄 helper，并由 analyzer独立重算验证；不得在测试 helper、readiness builder 和 analyzer 各自复制 schema 生成逻辑。
4. logical pre-capture exhaustion 必须证明预算检查发生在 `capture_observation_fn` 前，因此 `capture_attempted=false`、produced CR3 为 0；已完成的同-start captures 仍须计入 current counters。没有 confirmation group 的真实 early exhaustion 必须能作为结构化结果被 analyzer 审计，不能为了满足 analyzer 人工插入 partial group。
5. physical pre-capture denial（例如 remaining=0）必须保留 requested count 但证明没有新 CR3。若 `capture_step_fn` 已实际生成 CR3 后才发现 `physical_count > remaining`，不得伪装为 pre-capture exhaustion：该 run 必须 fail closed 为 `physical_budget_accounting_violation`，保留 CR3/attempt/failure 证据并走 Python/shell cleanup。正式 capture path 应在调用前传递并执行 remaining bound，避免正常路径产生事后超限。
6. 用真实 production functions 生成至少三类 round-trip fixtures：`feedback_attempts` logical exhaustion、一个实际可达的 confirmation/group/logical exhaustion、physical pre-capture denial。fixture 必须经正式 fake backend runner 写出 `run.json/captures.jsonl/commands.jsonl/target-results.jsonl`，随后调用公开 `analyze_strip_hsi_pilot(..., policy_version="v2")`；禁止测试先读取再手改 target row 作为成功路径。
7. 对 exhaustibility matrix 中 `guarded_unreachable` 的 sub-budget，增加 producer 行为测试证明状态机不会发出；formal analyzer 收到伪造值时必须拒绝。对每个 `production_reachable` 值，至少一个 runner-produced success path 与 one-under/phase drift/counter scope drift 反例。保留 R0D-R0I 全部篡改测试。
8. 增加真实 producer schema 回归断言：任何 `result.status=solver_budget_exhausted` 离开 formal runner 前，两份 ledger 均非空且相等；正常/confirmed result 两份均为空；不得再出现当前 production 的 top-only physical ledger或缺 pre-capture provenance 的 sparse logical ledger。
9. 生成全新 `fake-formal-v8-run`、analysis、R1 dry-run 与 `offline-readiness-r0j.json`，列出 exhaustibility matrix 和 runner-produced round-trip case；不得覆盖 R0I 证据。复跑 focused/full、`compileall`、四个 wrapper `zsh -n`、`git diff --check` 与 `codegraph sync`。
10. 全程 offline-only：不得访问设备、网络、`.env`、真实 all-off、安装/刷写 firmware。完成后 Goal 继续 `Blocked` 并交还 Planner；R0J 通过也不自动授权 preflight、P7-R1、新 sentinel 或后续阶段。

#### 8.7.40 Executor P7-R0J 离线执行结果（2026-07-18）

```text
current_phase = P7_R0J
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = b0af5bf7b0a8db32f0f8de7beac28e7ab487eec6
worktree_state = dirty(Planner R0J decision plus producer/runner/analyzer/tests/readiness/docs/debug)
authorization = offline_only; all device and named-experiment gates locked
run_dir = tmp/strip-hsi-pilot-offline/p7-r0j-v8-20260718-final
analysis = sparse production exhaustion is canonicalized once at runner finalization; logical uses start counters, physical denial target counters; feedback exhaustion persisted and accepted by public analyzer; post-capture overrun is fatal
completed_steps = exhaustibility matrix; canonical dual ledger enrichment; early no-confirmation exhaustion audit; target/start scope validation; production solver-runner-public analyzer fixture; physical producer schema; fatal accounting test; fake formal-v8/readiness
failure_evidence = ESPHome CLI remains unavailable; no firmware compile/flash/device readback
cleanup_evidence = focused 60/60; full 417/417; compileall, four wrapper zsh -n, git diff --check and codegraph sync pass; zero device/network/.env/real all_off calls
physical_budget = absolute 250 Planner-frozen; baseline 82..170; permitted 82..250
branch = P7_R0J_OFFLINE_COMPLETE_WAITING_PLANNER
next_action = Planner review only; no real preflight or named experiment inferred
```

Evidence:

- `offline-readiness-r0j.json` SHA-256 `4db40dd3c1548d8820c8c83679799174c560dd896ccbb2da61290b782b0f5178`。
- `v2-replay.json` SHA-256 `bdf83510473eb5afb1591ceb09d6169be4107e8e0bb9efd5ff5fc41b84b63aaa`；R1 dry-run plan SHA-256 `4e654bb707b4bcf87953eda5ea9d32dc94b321bf632a8097ed7bf0adfa3f8e37`。
- Readiness includes the exhaustibility matrix and named production round-trip cases; R0I manual five-category success fixture is removed.
- ESPHome compile remains `blocked_tool_missing_esphome_cli`.

Gate remains `Blocked`: R0J completion does not authorize device preflight, P7-R1, new sentinel, remaining, boundary, holdout or P8.

#### 8.7.41 P7-R0J Planner 复验结论（2026-07-18）

```text
planner_verdict = reject
finding = R0J-REV-001, R0J-REV-002, R0J-REV-003
reviewed_checkpoint = 84577a40c24685f57b6c11b5872918c80b5d65cc
implementation_checkpoint = b0af5bf756c84468680ceb4cb0a581eb94766429
reviewed_readiness_sha256 = 4db40dd3c1548d8820c8c83679799174c560dd896ccbb2da61290b782b0f5178
device_or_network_calls = 0
named_experiment_authorized = false
```

R0J 应保留的实现：canonical enrichment 已位于正式 runner finalization；logical/physical counter scope 已区分；真实 feedback/backtrack exhaustion 已完成 runner persistence -> public analyzer round-trip；post-capture overrun 现在以 `physical_budget_accounting_violation` 失败并保留 failure/cleanup 证据。readiness hash 与报告一致；Planner 独立复跑 P7 analyzer/feedback/budget focused suite `37/37` 通过。

以下三项仍阻塞验收：

1. `R0J-REV-001`：`EXHAUSTIBILITY_MATRIX` 只被 readiness builder、docs/skill 和矩阵单测读取，正式 canonicalizer 与 analyzer 均不使用它。独立篡改 replay 将矩阵标记为 `guarded_unreachable` 的 `initial` exhaustion 写成 internally consistent 双 ledger 后，public analyzer 仍返回 `ready_for_sentinel_branch` 且 `budget_audit=pass`。矩阵因此不是所声明的 source of truth。
2. `R0J-REV-002`：矩阵本身错误地把 `confirmation_groups` 标为 `guarded_unreachable`。使用未修改的 production `run_hsi_feedback_multiseed()`，令两组 confirmation 均失败后，第三次 `confirm()` reservation 会稳定产生 `sub_budget=confirmation_groups`、`phase=confirm-2`、两组 retained failed evidence。当前 analyzer 的 `_phase_matches_sub_budget()` 不支持该值，所以 canonicalized production output 仍不能 round-trip。
3. `R0J-REV-003`：physical target case 只经过 solver -> private canonicalizer -> private `_validate_pre_capture_exhaustion()`，没有按第 8.7.39-6 条经过 formal runner persistence 和公开 analyzer。readiness 也只写 `producer_canonical_schema_pass`，不能替代这一缺失门禁。

因此 `417/417` 仍没有覆盖真实可达性集合和完整 physical public round-trip。问题限定在 formal contract/reachability enforcement，不改变 solver budget 数值、coverage、58-feature 或设备协议，不需要 Advisor。

#### 8.7.42 P7-R0K 唯一离线修复阶段

P7-R0K 只允许修复 exhaustibility contract 的可执行性、可达性分类和缺失 round-trip。必须保留 R0J canonical finalization、start/target scope、post-capture fatal accounting、R0I 对称 ledger 与全部历史反例；不得调整任何冻结预算、solver 行为目标、uncertainty、P6 manifold、target 或设备接口。

1. 将 `EXHAUSTIBILITY_MATRIX` 从文档型 dict 改为正式 producer/analyzer 共同读取的 schema contract。它只定义允许的 origin/scope/status/phase family，不提供或相信 observed counters；runner 用它拒绝不允许持久化的 sparse producer value，analyzer 用它独立拒绝 `guarded_unreachable` 与 `fatal_accounting_error` 被伪装成 `solver_budget_exhausted`。readiness 必须序列化同一个对象，不得复制。
2. 矩阵必须按 **path** 而不是仅按 `sub_budget` 建模，因为 `physical_cr3` 同时存在 pre-capture denial（正式 `solver_budget_exhausted`）和 post-capture overrun（fatal accounting）两条路径。每条 path 使用稳定 ID，至少冻结 `sub_budget`、trigger point、classification、origin、counter scope、capture_attempted、formal status 和 phase pattern。
3. 把 production 可复现的 `confirmation_groups` / `confirm-2` 修正为 `production_reachable`、`logical_start`、`counter_scope=start`。formal analyzer 必须验证 `confirmation_groups_started` 已达到 frozen group limit、前两组结构完整且未 confirmed、下一 phase 恰为下一 group reservation；不得把它降级成 `confirmation_captures`。
4. 重新审计全部 `HsiStartBudget._exhaust()` 调用点。每个 matrix path 必须有 production state-machine test：`production_reachable` 由真实 `run_hsi_feedback()`/multiseed 触发；`guarded_unreachable` 证明正常控制流无法触发，并在 public analyzer 注入时拒绝；fatal path 必须形成 run failure 而非 target result。禁止用直接修改 `target-results.jsonl` 作为 success proof。
5. 新增至少两个完整 logical public round-trip：既有 `feedback_attempts` 与新增 `confirmation_groups`。两者都必须经正式 fake runner 生成 capture/command/target-result evidence，再由公开 analyzer 接受为结构有效的 exhausted attempt；若同 target 另一个 start confirmed，overall selection 仍按冻结 confirmed-first 规则。
6. 新增 physical pre-capture denial 的完整 formal runner -> persisted JSONL -> public analyzer round-trip。必须在 frozen target physical cap 下产生 target-scoped ledger，证明 requested > 0、produced=0、capture_attempted=false、target counters 等于 retained captures；不允许只调用 private canonicalizer/validator。
7. 增加确定性反例：exact-limit `initial`、`initial_probes`、`rebase_probes`、`confirmation_captures`、`rebases`、`logical_observations` 和 `weak_reacquire` 若仍分类为 guarded，public analyzer 均必须拒绝；`autoexposure` 或 post-capture `physical_cr3` 不得出现在 completed target row。matrix classification、origin、scope、phase pattern 任一 drift 均拒绝。
8. post-capture accounting fixture 继续验证 run/failure/Python cleanup，并额外验证 produced CR3 路径在 failure evidence 中可定位且文件非空；shell wrapper 语法与 trap 保持不变。不得把 orphan capture 填入正常 target owner ledger。
9. 生成全新 `fake-formal-v9-run`、analysis、R1 dry-run 与 `offline-readiness-r0k.json`，明确列出每条 path 的 production trigger 或 rejection test。复跑 focused/full、`compileall`、四个 wrapper `zsh -n`、`git diff --check` 与 `codegraph sync`。
10. 全程 offline-only。完成后 Goal 继续 `Blocked` 并交还 Planner；R0K 通过也不自动授权设备 preflight、P7-R1、新 sentinel 或后续阶段。

#### 8.7.43 P7-R0K Executor 分支交还（2026-07-18）

```text
executor_status = blocked_for_planner
branch = R0K-EXEC-BRANCH-001
implementation_checkpoint = 16f47c1f63b2431db88130d1f19f4456466ec91d
device_or_network_calls = 0
named_experiment_authorized = false
```

R0K 的 logical path contract 已取得实质进展：`EXHAUSTIBILITY_MATRIX` 改为 stable path ID schema，正式 runner canonicalizer、public analyzer、readiness 和测试读取同一个对象；真实 `run_hsi_feedback_multiseed()` 已触发 `confirmation_groups` / `confirm-2`，并完成正式 fake runner persistence -> public analyzer 回环；既有 feedback exhaustion 回环继续通过；伪造 guarded `initial` 已被 public analyzer 拒绝。post-capture overrun 现在写入 fatal path ID，failure evidence 可定位非空 CR3，并保留 Python cleanup。

但第 8.7.42-6 条出现必须由 Planner 选择的合同分支。冻结普通点预算满足：

```text
logical cap = 54
physical cap = 54 + (10 - 1) + 4 = 67
```

用实际 `HsiStartBudget`/`HsiPhysicalBudget` 状态机把两个 start 的所有 category、首个 auto-exposure 10 CR3 和 4 次 weak reacquire 全部用满后，确定性结果为：

```text
logical_per_target = 54 / 54
physical_used = 67 / 67
physical_remaining = 0
next logical reservation = false
next exhaustion sub_budget = feedback_attempts
capture callback reached = false
```

也就是说，physical cap 只能与 logical cap 同时用满；第 55 次 capture request 之前，solver 的 `HsiStartBudget.consume()` 已先拒绝，正式 runner 的 `capture_source()` 不会抵达 pre-capture physical check。n=5 的 `62/75` 同构。因此当前 `physical.pre_capture_denial=production_reachable` 与实际 producer 顺序不一致，无法诚实完成 formal runner -> persisted JSONL -> public analyzer success round-trip。禁止用 patched solver 额外调用第 55 次 callback 或手工 target row 伪造 production proof。

Planner 需二选一：

1. 将 `physical.pre_capture_denial` 冻结为 `guarded_unreachable`，R0K 以 public analyzer 拒绝该伪造路径、以及 post-capture physical/auto/weak fatal accounting 作为正式门禁；或
2. 明确授权新的 target-scoped capture producer trigger，使 physical pre-denial 可在正式 runner 中发生。该选择会改变 runner/solver target 架构，按既有边界可能需要 Advisor。

在 Planner 决策前，Executor 不继续构造 physical success fixture，不生成 v9 readiness/交接 artifact，也不执行 P7-R1 或设备 preflight。最终 focused budget/feedback/P7 suite 为 `40/40` 通过，`compileall`、四个 wrapper `zsh -n`、`git diff --check` 与 `codegraph sync` 通过。Goal 保持 `Blocked`。

#### 8.7.44 P7-R0K physical reachability Planner 决定（2026-07-18）

```text
planner_verdict = accept_branch_1
physical.pre_capture_denial = guarded_unreachable
new_target_scoped_producer = rejected
advisor_required = false
reviewed_checkpoint = 6735f12271b1577b5c3c6fc57e572a009ce3ee1b
implementation_checkpoint = 16f47c1f63b2431db88130d1f19f4456466ec91d
device_or_network_calls = 0
named_experiment_authorized = false
```

Planner 接受第 8.7.43 节的可达性证明，并冻结以下解释：

1. 普通点 `67 = 54 + (10 - 1) + 4`，n=5 点 `75 = 62 + (10 - 1) + 4`。额外 physical 容量只覆盖首个 logical observation 的最多 10 张 auto-exposure CR3（其中 1 张已计入 logical observation）和最多 4 张 weak reacquire；不存在未绑定 logical observation 的正式 target capture。
2. 每次 solver observation 都先执行 `HsiStartBudget.consume/reserve_*()`，成功后才调用 `capture_observation_fn -> capture_source()`。因此在两个 start 的 logical category/cap 用满后，下一请求必然先成为 start-scoped logical exhaustion，不能到达 `capture_source()` 的 physical remaining precheck。
3. 为了让审计矩阵中的一条路径“可达”而新增 target-scoped producer，会让审计合同反向改变 solver/runner 架构，并引入当前实验协议不需要的额外捕获状态。没有测量或产品需求支持该复杂度，故明确拒绝。
4. `capture_source()` 的 remaining precheck 可以保留为 defense-in-depth，但在冻结 formal runner 中属于 `guarded_unreachable`。若未来控制流意外抵达该分支，runner 必须 fail closed；不得把它持久化成 completed target 的 `solver_budget_exhausted` success evidence。
5. `physical.post_capture_overrun`、`physical.autoexposure_overrun` 和 `physical.weak_reacquire_overrun` 继续是 `fatal_accounting_error`。已经产生 CR3 的超限不得被降格为 pre-capture denial，也不得进入正常 target owner ledger。

Planner 独立复跑 `tests.test_measure_strip_hsi_pilot`、`tests.test_hsi_feedback`、`tests.test_hsi_budget`，结果 `40/40` 通过。该结果验证 R0K 已完成的 executable matrix、`confirmation_groups/confirm-2` public round-trip 和 fatal evidence 路径；它不替代第 8.7.45 节尚需完成的 guarded classification 回归和 full suite。该决定只解决离线合同分支，不构成 R0K 最终验收，也不授权任何设备操作。

#### 8.7.45 P7-R0K 唯一离线收口动作

Executor 只能完成以下 offline-only 工作，然后交还 Planner：

1. 将 `EXHAUSTIBILITY_MATRIX["physical.pre_capture_denial"]` 冻结为 `classification=guarded_unreachable`、`formal_status=not_emitted`；保留稳定 path ID、trigger point、origin、target scope、`capture_attempted=false` 和 phase family，禁止删除防御性 precheck。
2. runner canonicalizer 必须拒绝把该 path 持久化为 `solver_budget_exhausted`；public analyzer 必须拒绝伪造的双 ledger，即使 `physical_cr3_used` 恰等于 hard cap、requested 为正、produced 为 0 且其他字段内部一致。拒绝应来自共享 path contract，再由 analyzer 独立 counter audit 补强，不能硬编码特定 fixture。
3. 为普通 n=3 和边界/holdout n=5 各增加一个确定性 production-state-machine test。测试必须同时用满两个 starts 的 frozen logical categories、首轮 auto-exposure 和 weak reacquire physical allowance，并证明下一次 solver request 在调用 capture callback 前得到 logical exhaustion；分别断言 `54/67` 与 `62/75`。禁止 patched solver、额外 callback、直接改 target row 或只测 `HsiPhysicalBudget.record()`。
4. 保留并复验两个 `production_reachable` logical round-trip：`logical.feedback_attempts` 与 `logical.confirmation_groups`。矩阵中所有其他 guarded path 均不得由 formal completed target 发出；所有 post-capture physical path 继续形成 run-level fatal failure和 cleanup evidence。
5. 删除或改写任何仍声称 physical pre-capture formal success round-trip 必须存在的测试、readiness 文案、docs、skill 和 debug 条目；不得删除历史 R0J/R0K 分支证据。将当前 active debug 记录在收口后移入 resolved，并写明 Planner 冻结理由。
6. 生成全新 `fake-formal-v9-run`、公开 analysis、R1 dry-run 和 `offline-readiness-r0k-final.json`。readiness 必须列出每个 stable path 的最终 classification 与证据类型，并明确：physical pre-capture 只有 producer-unreachability + runner/analyzer rejection proof，不得声称 production success round-trip。
7. 复跑 focused/full suite、`compileall`、四个 wrapper `zsh -n`、`git diff --check` 与 `codegraph sync`。交接必须提供 readiness 路径/hash、focused/full 数量、当前 HEAD/worktree，并明确零设备、零网络、零 `.env`、零真实灯光调用。
8. 完成后状态写为 `offline_complete_waiting_for_planner_acceptance`，Goal 继续 `Blocked`。不得自动执行 `p7_strip_state_readback_preflight`、P7-R1、sentinel-v2、remaining 9、boundary、holdout 或 P8；这些门禁仍需 Planner 后续复验和用户另行实机授权。

#### 8.7.46 P7-R0K Executor 离线收口交接（2026-07-18）

```text
executor_status = offline_complete_waiting_for_planner_acceptance
implementation_checkpoint = bb4554a9afd0ff8b5356766335ed232e7daa6e08
readiness = tmp/strip-hsi-pilot-offline/p7-r0k-v9-20260718-final/offline-readiness-r0k-final.json
readiness_sha256 = b2755ca011510737fff55ab68443aad4a160a8d6fd3e660828c0f0cd7221d576
fake_formal_analysis_sha256 = d83d31c56b18a9b9845107b01e3e450bace685f9efcf40d0283227f8adb04fae
v2_replay_sha256 = 2209a6d5eaabc166cf8bb1339f562a63a5d483bd18137254ea9dca6a42b3e22d
p7_r1_dry_plan_sha256 = 11b7df5693494c75f76e0daf1d4b7734eccdeabe78fa59440102189242c7f7ab
device_or_network_calls = 0
env_reads = 0
real_light_or_all_off_calls = 0
named_experiment_authorized = false
```

Executor 已按 Planner 第 8.7.44 节的分支完成第 8.7.45 节全部 offline-only 工作：

1. 共用 `EXHAUSTIBILITY_MATRIX` 已将 `physical.pre_capture_denial` 冻结为 `guarded_unreachable/not_emitted`；runner canonicalizer 和 public analyzer 都按共享 path contract 拒绝伪造的 completed-target 双 ledger。没有新增 target-scoped producer，也没有构造 physical success fixture。
2. 普通 n=3 和边界/holdout n=5 的 production state-machine test 分别用满两个 start 的 frozen logical categories、首轮 auto-exposure 与 weak reacquire allowance，并证明下一次正式 solver request 在 capture callback 前先触发 logical exhaustion；审计数分别为 `54/67` 与 `62/75`。
3. `logical.feedback_attempts` 和 `logical.confirmation_groups` 两条 production round-trip 继续通过正式 solver -> runner persisted JSONL -> public analyzer；其余 guarded path 均由 public analyzer 拒绝。physical、auto-exposure 和 weak-reacquire 的 post-capture 超限继续形成 run-level fatal accounting failure，保留已产生 CR3 与 cleanup evidence。
4. 全新 v9 离线交接包含 fake formal run、公开 analysis、v2 replay、R1 dry-run 与 schema-v3 readiness。fake formal run 共有 29 张隔离 `.cr3`，无 `.npy`；公开 analysis 为 v2、4 个点，three-layer/objective/capture-owner audit 均为 pass。R1 dry-run 仍为 30 Ray + 50 strip、250 CR3 绝对上限且 `not_authorized_for_execution`。Python 与 shell fake all-off evidence 的 ESPHome/Ray 步骤均为 pass。
5. 验证通过：focused budget/feedback/P7/readiness `43/43`；full suite `423/423`（`139.434s`）；`compileall`；四个实际存在的 P6/P7 wrapper `zsh -n`；`git diff --check`；`codegraph sync`。v8 曾记录但当前不存在的两个临时 sentinel wrapper 未被虚报，v9 改为实际存在的 Ray manifold、HSI uncertainty、strip pilot 与 reference/repeatability wrapper。
6. active debug 记录已移入 resolved，docs 与项目 skill 已同步 Planner 冻结语义。实现提交为 `bb4554a9afd0ff8b5356766335ed232e7daa6e08`。

本节只表示 P7-R0K 离线实现完成并等待 Planner 验收，不构成 named-experiment 放行。Goal 保持 `Blocked`；`p7_strip_state_readback_preflight`、P7-R1、sentinel-v2、remaining 9、boundary、holdout 和 P8 全部继续锁定。

## 9. Phase D：剩余九点与合并分析

**当前锁定：** 本节尚未授权。只有第 8.7.11 节的新 sentinel-v2 经 Planner 明确写入放行决定后，本节才恢复有效；旧 `S-PASS` 不再是入口。

### 9.1 前提

- Sentinel-v2 满足后续 Planner 冻结的 `S-V2-PASS`；
- reference/repeatability v2 artifact、代码检查点和 solver budget 已冻结；
- uncertainty artifact、代码检查点和所有 frozen hash 未变化；
- 新 session 重新执行 Phase B；
- 不复用 sentinel 曝光 cache。

### 9.2 Run 目录

```text
/Volumes/4T/temp/rgbww-optimizer/strip-hsi-pilot/p7-remaining-9-<timestamp>
```

### 9.3 采集

- pre Ray anchors 三点；
- remaining 九点；
- 非-coordinate-equivalent full-scale 点的 3072/必要 2048 诊断；
- post H120/S100 anchor；
- Python/shell 双 cleanup；
- analyzer。

每个普通点 3 confirmations；scale-relaxed 诊断 5。任一 `reference_drift`、`uncertainty_unresolved` 或安全审计失败使本 run 无效，并按 Sentinel 同名分支停止。

### 9.4 合并 13 点

新增纯离线 combined analyzer，输入：

- sentinel run/hash；
- remaining run/hash；
- 同一 uncertainty/manifold/location/observer/basis/code checkpoint；
- 两个 session 的 anchor 和 cleanup；
- 恰好 13 个不重复 target。

输出：

```text
p7-int100-fullscale-13-analysis.json
```

不得把两个不同 artifact/hash 的 run 拼接。Combined analysis 必须保留每点原始状态，不能用 interpolation 填掉失败点。

进入边界阶段的最低条件：

- 13/13 都有有效、可审计 target row；
- 无 `reference_drift` 或 `uncertainty_unresolved`；
- 每个主 Hue 至少有一个可继续建立 coordinate-equivalent 范围的有效测量；
- 非-coordinate-equivalent 点已完成 scale-relaxed 诊断或明确列为待诊断；
- 不要求 13/13 SAT100 都 coordinate equivalent；
- 每点均保留独立 `observer_equivalent` 和 `color_rendering_residual`，不得因 coordinate pass 删除显色差异。

不满足时停止并交还 Planner/Advisor，不进入 P8。

---

## 10. Phase E：full-scale SAT 边界

### 10.1 边界名称

只允许：

```text
s_exact_max_int100_fullscale(h)
```

它不等于灯带物理色域。

### 10.2 搜索规则

对每个主 Hue：

1. 若 S100 full-scale `hsi_coordinate_equivalent`，记录范围上限 100，不需构造超界点；
2. 若 S50 coordinate equivalent、S100 未确认，以 `[50,100]` 为初始 bracket；
3. 若 S50 未确认，从 P6 实测 SAT20、SAT5 方向向下寻找非零 coordinate-equivalent 下界；SAT0 Hue 未定义，不能作为 Hue-specific 下界；
4. 每个新 boundary target 使用 5 confirmations；
5. 在 full-scale 下做整数 SAT 二分/定向加密，直到上下界相邻或无未测整数；
6. 每个 full-scale 非-coordinate-equivalent 上界必须做 3072，必要时 2048 诊断；
7. 保存 active-set、white fraction、condition、sensitivity 和边界原因；
8. 边界不单调或相邻 Hue 急变时只做定向加点，不用平滑覆盖真实状态。

### 10.3 边界成立条件

`boundary_bracketed_at_full_scale` 必须同时有：

- 同 Hue 非零 SAT 的 full-scale coordinate-equivalent 下界；
- 同 Hue full-scale 未确认上界；
- 上下界均为合法测量；
- 边界点 5 confirmations；
- scale-relaxed 3072，必要时 2048 诊断；
- reference anchors 和双 cleanup 通过；
- 未发生 uncertainty model drift。

如果降低 max_code 后 coordinate equivalent，明确写：

```text
boundary_cause = full_scale_active_channel_policy
physical_gamut_inference = prohibited
```

如果 3072/2048 都未证明 coordinate equivalent，只能写当前观察与策略组合未解决，不能写物理不可达或 `hue_unreachable`。

### 10.4 边界阶段出口

- 六个主 Hue 都有 coordinate-equivalent 范围；
- 所需 boundary 均 bracket 到整数 SAT；
- full-scale 与 scale-relaxed 原因分开；
- 生成候选 `s_exact_max_int100_fullscale` 表；
- 才能进入 Phase F。

---

## 11. Phase F：INT100 full-scale 候选与 holdout

### 11.1 候选生成

离线生成但不安装：

```text
config/hsi/rgbww-hsi-int100-fullscale-candidate.json
```

第一版保持可审计：

- Hue 周期分段线性；
- SAT 单调分段线性；
- full-scale 边界外先映射到 `s_exact_max_int100_fullscale(h)`；
- 五通道插值后执行 0..4095 约束和 full-scale active-channel policy；
- 保存 active-set switch；
- 不先上 cubic/PCHIP 掩盖节点不足；
- 不调用相机反馈生成 holdout 命令。

在冻结 holdout plan 前，对候选做确定性周期数值审计：

1. 在每个待验证 SAT 上以 0.5° 采样 `H=0..360`；
2. `command(0)` 与 `command(360)` 必须逐通道 bit-exact；
3. 计算所有相邻 Hue 的 normalized command L1 first difference；
4. 以所有非 seam first difference 的 `median + 3 * MAD` 作为预先冻结的 seam continuity limit；若 MAD 为零则使用非 seam maximum；
5. `359.5→360/0` 和 `0→0.5` 两条 seam step 都不得超过该 limit；
6. limit、采样网格和结果写入 candidate 与 holdout plan，holdout 后不得重算门槛。

候选必须记录：

- 所有训练/boundary run hash；
- uncertainty/manifold/location/observer/basis hash；
- command grid；
- boundary table；
- interpolation policy；
- runtime status semantics；
- `absolute_brightness_matched=false`；
- `installed=false`。

### 11.2 Holdout 冻结规则

在任何 holdout capture 前写入不可变 plan。至少包含：

#### 六个 Hue 扇区非节点

基础 Hue：

```text
30, 90, 150, 210, 270, 330
```

SAT 使用预先冻结规则：在每个 Hue 的已验证 coordinate-equivalent 范围内交替选取约 35% 和 65% 的范围位置；不得观察 holdout 后改点。若某 Hue 范围过窄，使用其 coordinate-equivalent bracket 中点并记录规则结果。

#### 0/360 周期对

```text
H1
H359
```

使用两侧都在 coordinate-equivalent 范围内的同一 SAT；这两个点同时作为 wrap 高曲率专门 holdout，使用 5 confirmations。

至少八个非训练点。六扇区普通点 3 confirmations；H1/H359 和任何接近 boundary 的点 5。

### 11.3 Holdout 执行规则

- 每 session 使用同样 pre/post Ray anchors；
- holdout 命令只来自冻结候选插值；
- validation run 内禁止 probe、feedback、重新优化或改 boundary；
- 任一失败完整保留，不用定向补点替换原 holdout；
- 若要修候选，原 holdout 失效，必须生成新候选 hash 和全新 holdout set/run。

### 11.4 Holdout 通过条件

全部满足：

- 至少六个扇区 non-node target 均 `hsi_coordinate_equivalent`；
- H1/H359 均 `hsi_coordinate_equivalent`；
- H1/H359 的观测均 coordinate equivalent，且候选通过 holdout 前冻结的数值周期连续性门；
- 全部点保存 `observer_equivalent` 与 `color_rendering_residual`；observer false 不得被 coordinate pass 隐藏；
- 高曲率 holdout 通过；
- 无 reference drift、uncertainty unresolved、measurement unreachable；
- 所有 target 达到预声明 3/5 confirmations；
- command audit、CR3、recorded exposure、无 `.npy`、双 cleanup 全部通过；
- 候选 hash 在整个 run 不变。

任一 holdout 失败：

- 保留原验证结果；
- 不进入 P8；
- 分析是否需要局部节点、插值策略或产品范围修订；
- 到 `repeat_targeted_stage_6` 决策，不自动重跑到通过。

---

## 12. Gate-6 交接包

P7 holdout 通过后，不进入 P8。状态更新为：

```text
current_phase = gate_6
stage_status = at_decision_gate
next_action = advisor_review_gate_6
```

交接包至少包含：

1. frozen v2 uncertainty/reference/repeatability artifact、输入 hash、Monte Carlo/guard-band 报告；
2. sentinel、remaining、combined 13 点分析；
3. 所有 reference anchor 和 drift 结论；
4. 六 Hue 的 `s_exact_max_int100_fullscale` 与 scale-relaxed 诊断；
5. full-scale 候选及 hash；
6. 六扇区、0/360、高曲率 holdout；
7. 每点 local Hue/SAT coordinate score、observer-equivalence score、color-rendering residual；
8. 3/5 confirmation 和 uncertainty spread check；
9. active channel、WW/CW contribution、condition/sensitivity；
10. command/source-isolation audit；
11. 全部失败、不可测、coordinate-unconfirmed 和 solver budget 状态；
12. Python/shell/recovery all-off；
13. 完整测试、compileall、diff-check、CodeGraph；
14. 未安装、默认 LUT 未改变的确认；
15. 推荐 Gate-6 出口。

允许的 Gate-6 出口：

```text
freeze_candidates_for_stage_7
repeat_targeted_stage_6
restrict_product_range
stop_hsi_route
```

Advisor 在 Gate-6 冻结：

- `hsi_coordinate_equivalent`、`observer_equivalent`、`color_rendering_residual` 和 `gamut_compressed_int100_fullscale` 公开语义；
- 支持的 Hue/SAT/full-scale 范围；
- 候选 hash；
- 是否允许进入 P8；
- P8 的 Ray INT 与 strip scale 语义；
- P9 验证矩阵。

---

## 13. P8 锁

决定固定为：

```text
keep_p8_locked_until_p7_holdout
```

在 Gate-6 明确批准前禁止：

- Ray `INT=50/20/5` capture；
- strip HSI INT 网络；
- `I-A/I-B/I-C` 选择；
- 三维 HSI LUT；
- 运行时 INT correction；
- 把 3072/2048 full-scale 诊断误称为 Ray INT 实验。

P7 内的 `max_code=3072/2048` 只用于区分 full-scale active-channel policy，不改变 Ray INT=100。

---

## 14. 失败处理总表

| 事件 | 当前 run | 是否继续下一批 | 允许动作 | 禁止动作 |
| --- | --- | --- | --- | --- |
| `reference_drift` | invalid for Gate-6 | 否 | 双关灯、保留锚点、交还 Advisor | 同 run 重拟合 P6 |
| `uncertainty_unresolved` | diagnostic only | 否 | 定向 repeatability 计划 | 用确认帧更新 sigma |
| `measurement_unreachable` | 保留完整证据 | 否，除非本计划另有明确处理 | 只在 1.25x 内重拍 | 扩曝光、删 feature |
| `solver_budget_exhausted` | 保留 best valid | 否 | 离线分析/有测试修 bug | 同 run 加轮数 |
| `hsi_coordinate_unconfirmed` | 不是 boundary | 视阶段而定 | scale-relaxed 诊断、建立 bracket | 写物理不可达 |
| source/readback audit fail | invalid | 否 | 修代码、新目录完整重跑 | 拼接部分通过点 |
| Python/shell cleanup 缺失 | invalid | 否 | 立即 recovery all-off | 假设灯已关 |
| 3072/2048 coordinate equivalent | policy diagnostic | 可按阶段继续 | 标 full-scale policy effect并保留 observer residual | 写物理 gamut |
| holdout fail | candidate fail | 否 | `repeat_targeted_stage_6` 决策 | validation run 内优化 |

---

## 15. Executor 状态更新模板

每完成一个 Phase 或发生一次真实失败，立即更新本文件，不要等阶段末：

```text
current_phase = A_v1 | B | C_v1 | P7_R0 | P7_R1 | sentinel_v2 | D | E | F | gate_6
stage_status = in_progress | code_complete_waiting_for_sentinel_authorization |
               planner_decision_complete_waiting_for_executor_offline_implementation |
               offline_complete_waiting_for_planner_acceptance |
               planner_acceptance_pass_named_experiment_authorized |
               running | at_branch | pass | fail | at_decision_gate
current_head =
worktree_state = clean | dirty(...)
authorization = offline_only | device_probe | named_experiment | commit | install
uncertainty_artifact = path + sha256
code_checkpoint = head + diff_sha256
run_dir =
runner_pid_tty =
analysis =
input_hashes =
completed_steps =
failure_evidence =
cleanup_evidence =
branch =
next_action =
```

### 当前初始值

```text
current_phase = P7_R0K
stage_status = offline_complete_waiting_for_planner_acceptance
current_head = bb4554a9afd0ff8b5356766335ed232e7daa6e08 implementation checkpoint; documentation-only PLAN handoff is its successor
worktree_state = clean after committing this PLAN handoff; preserve bb4554a/16f47c1/6735f12/84577a4/b0af5bf and all prior P1-P7, Phase A and advisor evidence
authorization = offline_only; named_experiment:p7_sentinel_4 consumed; p7_targeted_reference_repeatability_v2 not authorized; no authorization for P7_R1/sentinel_v2/remaining/boundary/holdout/P8
uncertainty_artifact_v1 = config/hsi/strip-hsi-uncertainty.json @ cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94; immutable diagnostic evidence
uncertainty_artifact_v2 = config/hsi/strip-hsi-policy-v2-waiting.json @ db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4; status waiting_for_targeted_measurement; formal_capture_eligible=false
code_checkpoint = bb4554a9afd0ff8b5356766335ed232e7daa6e08 freezes guarded physical precheck, n3/n5 producer preemption, shared runner/analyzer rejection and fatal produced-CR3 paths
run_dir = tmp/strip-hsi-pilot-offline/p7-r0k-v9-20260718-final; offline fake evidence only
analysis = offline-readiness-r0k-final.json @ b2755ca011510737fff55ab68443aad4a160a8d6fd3e660828c0f0cd7221d576; ready_for_planner_review, not experiment authorization
completed_steps = Phase A-v1 + Phase B + authorized sentinel_4 capture/audit + P7-R0/R0B/R0C + P7-R0D/R0E/R0F/R0G/R0H/R0I/R0J/R0K offline closure; no real calls in R0K
failure_evidence = none in R0K final offline closure; physical pre-capture success evidence intentionally absent because Planner froze guarded_unreachable; firmware compile remains tool-blocked; P7-R1/sentinel-v2 remain unauthorized
cleanup_evidence = focused 43/43; full 423/423 in 139.434s; compileall, four existing wrapper zsh -n, git diff --check and codegraph sync pass; fake Python/shell ESPHome/Ray cleanup steps pass; zero device/network/.env/real all-off calls
physical_budget = absolute 250 Planner-frozen; baseline without weak reacquire 82..170; permitted with weak reacquire 82..250; maximum 60-second settling 9600 s
branch = P7_R0K_GUARDED_PHYSICAL_PRECAPTURE_CONTRACT
next_action = Planner independently reviews section 8.7.46 and checkpoint bb4554a; no hardware or named experiment is authorized
```

---

## 16. Stage 6 完成定义

Stage 6 只有在以下全部完成后才可写 `pass`：

- reference/repeatability v2 artifact 在新 sentinel 实拍前冻结，v1 仅保留历史证据；
- coordinate、observer、reference 和 repeatability 的各自 joint 99.73% coverage/guard band 通过离线校准且语义不混用；
- sentinel-v2 四点按新分支通过；
- remaining 九点完成；
- 13 点都有有效结果，失败没有被删除；
- 各主 Hue 有 hsi-coordinate-equivalent 范围，并保留 observer/color-rendering 结果；
- 必要 full-scale boundary 和 3072/2048 诊断完成；
- `s_exact_max_int100_fullscale` 命名和范围正确；
- 候选未安装；
- 六扇区 non-node、0/360、高曲率 holdout 全部通过；
- 所有 session 无 reference drift；
- 所有 CR3/recorded exposure/commands/cleanup 审计通过；
- 全套测试、compileall、wrapper syntax、diff-check、CodeGraph 通过；
- Gate-6 交接包完整；
- Advisor 明确给出 Gate-6 出口。

在此之前不得把 P7 写成实机完成，也不得进入 P8。
