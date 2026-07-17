# Stage 6 执行计划：Ray120c Camera-Observer HSI Match

**计划状态：** active

**Planner 完成日期：** 2026-07-17

**当前 `HEAD`：** `ecf47d722e6f9e7c2c09b0d7fd3e3429e7d38ad5`

**当前活动阶段：** Stage 6 / P7 INT100 strip HSI

**当前阶段状态：** `planner_complete_waiting_for_executor_offline_correction`

**下一条唯一动作：** Executor 只执行第 6 节 Phase A 的离线纠偏；在 Phase A 全部验收前不得访问相机、Ray120c 或 ESPHome。

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
3. `advisor/1/1.GUIDE.md` 与本文件顶部记录的最新 Advisor 结论；
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
- 改变 `faithful`、full-scale gamut 或 INT 产品语义；
- 把任何失败写成物理色域不可达；
- 回退 P6、重拍 106 点 Ray 网络或改用理论 HSL/HSV；
- 进入 P8；
- 安装或覆盖任何默认 LUT；
- commit、push 或创建 PR，除非用户另行明确要求。

### 1.3 高风险停止点

只有以下情况交还 Planner/Advisor：

1. Phase A 无法从冻结数据得到可校准、正定且稳定的联合 uncertainty artifact；
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
| P7 代码 | 模块边界可保留 | 做局部纠偏，不架构重写 |

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

阶段内状态必须互斥且保留原始原因：

```text
faithful
unconfirmed
measurement_unreachable
uncertainty_unresolved
solver_budget_exhausted
reference_drift
boundary_bracketed_at_full_scale
```

状态解释：

- `faithful`：在冻结 joint coverage + guard band 下通过，并完成规定的 settled confirmations；
- `unconfirmed`：本轮未证明 faithful，但没有足够证据归入其他状态；
- `measurement_unreachable`：冻结 RAW/exposure 包络内无法得到合法 58-feature；
- `uncertainty_unresolved`：重复帧显示冻结噪声模型可能低估，或结果落入决策 guard band；
- `solver_budget_exhausted`：合法测量存在，但冻结轮数内没有得到可确认候选；
- `reference_drift`：当前 Ray 锚点超出冻结 P6 coverage；
- `boundary_bracketed_at_full_scale`：只表示 INT100、full-scale active-channel policy 下已建立 faithful 下界和非-faithful 上界，并完成 scale-relaxed 诊断。

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
- 新增 `config/hsi/strip-hsi-uncertainty.json`：冻结 uncertainty artifact；
- 后续新增 `config/hsi/rgbww-hsi-int100-fullscale-candidate.json`：只有 P7 holdout 完成后生成候选，Gate-6 前不安装。

不要创建平行采集框架，也不要复制 remote capture、RAW observer、bounded least-squares 或 all-off。

### 5.2 Uncertainty artifact 最低字段

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

## 6. Phase A：离线纠偏

**授权范围：** `offline_only`

**完成状态：** `code_complete_waiting_for_sentinel`

**禁止：** `/health`、`/v1/config`、`/v1/capture`、Ray、ESPHome、真实 all-off 调用。

### A0. 定向预检

- [ ] 读取本计划、00-CONTRACT、GUIDE、skill、README；
- [ ] `git status --short`，记录并保留已有改动；
- [ ] 确认没有活动 calibration process，但不探测设备；
- [ ] CodeGraph 定位 P7 五个模块、P1 repeatability、P6 analyzer 和 shared capture adapter；
- [ ] 计算所有冻结输入 hash，发现 drift 时停止，不静默更新本计划中的 hash；
- [ ] 检查当前 `config/hsi/strip-hsi-pilot.json` 仍只是旧 13 点离线草案。

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

- [ ] `evaluate_hsi_observation()` 改为读取冻结 uncertainty evaluator，不再接收默认为零的三个 strip 3-sigma；
- [ ] 保留 Hue/SAT/orthogonal 数值作为报告与词典序方向；
- [ ] `feasible` 只由 joint guarded decision 决定；
- [ ] solver 排序优先：状态有效、Hue excess、SAT excess、joint score、orthogonal/shape、连续性；
- [ ] SAT0 的排序删除 Hue；
- [ ] feedback samples 保存 artifact hash、target kind、joint score、coverage/guarded limits；
- [ ] confirmation 失败仍触发 thermal rebase，但不得更新 uncertainty；
- [ ] 达到冻结轮数仍未确认时返回 `solver_budget_exhausted`，不自动增加轮数。

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

---

## 7. Phase B：实机前检查

只有 Phase A 通过且当前存在明确 named-experiment 实机授权时才能执行。

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

## 8. Phase C：四点 Sentinel

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

### 8.4 Sentinel 自动放行条件

只有同时满足以下条件，Executor 才可不等待 Advisor 而进入剩余 9 点：

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

### 8.5 Sentinel 分支

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

---

## 9. Phase D：剩余九点与合并分析

### 9.1 前提

- Sentinel=`S-PASS`；
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
- 非-faithful full-scale 点的 3072/必要 2048 诊断；
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
- 每个主 Hue 至少有一个可继续建立 faithful 范围的有效测量；
- 非-faithful 点已完成 scale-relaxed 诊断或明确列为待诊断；
- 不要求 13/13 SAT100 都 faithful。

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

1. 若 S100 full-scale faithful，记录范围上限 100，不需构造超界点；
2. 若 S50 faithful、S100 非-faithful，以 `[50,100]` 为初始 bracket；
3. 若 S50 非-faithful，从 P6 实测 SAT20、SAT5 方向向下寻找非零 faithful 下界；SAT0 Hue 未定义，不能作为 Hue-specific faithful 下界；
4. 每个新 boundary target 使用 5 confirmations；
5. 在 full-scale 下做整数 SAT 二分/定向加密，直到上下界相邻或无未测整数；
6. 每个 full-scale 非-faithful 上界必须做 3072，必要时 2048 诊断；
7. 保存 active-set、white fraction、condition、sensitivity 和边界原因；
8. 边界不单调或相邻 Hue 急变时只做定向加点，不用平滑覆盖真实状态。

### 10.3 边界成立条件

`boundary_bracketed_at_full_scale` 必须同时有：

- 同 Hue 非零 SAT 的 full-scale faithful 下界；
- 同 Hue full-scale 非-faithful 上界；
- 上下界均为合法测量；
- 边界点 5 confirmations；
- scale-relaxed 3072，必要时 2048 诊断；
- reference anchors 和双 cleanup 通过；
- 未发生 uncertainty model drift。

如果降低 max_code 后 faithful，明确写：

```text
boundary_cause = full_scale_active_channel_policy
physical_gamut_inference = prohibited
```

如果 3072/2048 都不 faithful，只能写当前观察与策略组合未解决，不能写物理不可达或 `hue_unreachable`。

### 10.4 边界阶段出口

- 六个主 Hue 都有 faithful 范围；
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

SAT 使用预先冻结规则：在每个 Hue 的已验证 faithful 范围内交替选取约 35% 和 65% 的范围位置；不得观察 holdout 后改点。若某 Hue 范围过窄，使用其 faithful bracket 中点并记录规则结果。

#### 0/360 周期对

```text
H1
H359
```

使用两侧都在 faithful 范围内的同一 SAT；这两个点同时作为 wrap 高曲率专门 holdout，使用 5 confirmations。

至少八个非训练点。六扇区普通点 3 confirmations；H1/H359 和任何接近 boundary 的点 5。

### 11.3 Holdout 执行规则

- 每 session 使用同样 pre/post Ray anchors；
- holdout 命令只来自冻结候选插值；
- validation run 内禁止 probe、feedback、重新优化或改 boundary；
- 任一失败完整保留，不用定向补点替换原 holdout；
- 若要修候选，原 holdout 失效，必须生成新候选 hash 和全新 holdout set/run。

### 11.4 Holdout 通过条件

全部满足：

- 至少六个扇区 non-node target 均 `faithful`；
- H1/H359 均 `faithful`；
- H1/H359 的观测均 faithful，且候选通过 holdout 前冻结的数值周期连续性门；
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

1. frozen uncertainty artifact、输入 hash、Monte Carlo/guard-band 报告；
2. sentinel、remaining、combined 13 点分析；
3. 所有 reference anchor 和 drift 结论；
4. 六 Hue 的 `s_exact_max_int100_fullscale` 与 scale-relaxed 诊断；
5. full-scale 候选及 hash；
6. 六扇区、0/360、高曲率 holdout；
7. 每点 Hue/SAT/orthogonal/joint score；
8. 3/5 confirmation 和 uncertainty spread check；
9. active channel、WW/CW contribution、condition/sensitivity；
10. command/source-isolation audit；
11. 全部失败、不可测、unconfirmed 和 solver budget 状态；
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

- `faithful` 和 `gamut_compressed_int100_fullscale` 公开语义；
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
| `unconfirmed` | 不是 boundary | 视阶段而定 | scale-relaxed 诊断、建立 bracket | 写物理不可达 |
| source/readback audit fail | invalid | 否 | 修代码、新目录完整重跑 | 拼接部分通过点 |
| Python/shell cleanup 缺失 | invalid | 否 | 立即 recovery all-off | 假设灯已关 |
| 3072/2048 faithful | policy diagnostic | 可按阶段继续 | 标 full-scale policy effect | 写物理 gamut |
| holdout fail | candidate fail | 否 | `repeat_targeted_stage_6` 决策 | validation run 内优化 |

---

## 15. Executor 状态更新模板

每完成一个 Phase 或发生一次真实失败，立即更新本文件，不要等阶段末：

```text
current_phase = A | B | C | D | E | F | gate_6
stage_status = in_progress | code_complete_waiting_for_sentinel_authorization |
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
current_phase = A
stage_status = planner_complete_waiting_for_executor_offline_correction
current_head = ecf47d722e6f9e7c2c09b0d7fd3e3429e7d38ad5
worktree_state = dirty; preserve all existing P1-P7 and advisor changes
authorization = offline_only for the next action; hardware must be rechecked before Phase B
uncertainty_artifact = not_created
code_checkpoint = not_created
run_dir = none
analysis = P6 frozen; P7 real measurement none
branch = advisor-approved sentinel_4_then_9
next_action = implement Phase A only
```

---

## 16. Stage 6 完成定义

Stage 6 只有在以下全部完成后才可写 `pass`：

- uncertainty artifact 在实拍前冻结；
- joint 99.73% coverage 和 guard band 通过离线校准；
- sentinel 四点按分支通过；
- remaining 九点完成；
- 13 点都有有效结果，失败没有被删除；
- 各主 Hue 有 faithful 范围；
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
