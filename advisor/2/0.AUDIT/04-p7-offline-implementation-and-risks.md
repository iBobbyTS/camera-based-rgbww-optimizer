# P7 离线实现、验证和实拍前风险

## 1. 当前实现范围

### 1.1 Ray 目标流形

`measurement/ray_hsi_manifold.py` 已实现：

- 校验冻结 P6 run/analysis/hash；
- 读取 accepted native-Bayer feature；
- 计算所有目标共同可靠的 58-feature 交集；
- pooled SAT0 direction 和 Hue-dependent brightness scale；
- periodic Hue 与分段 SAT 插值；
- `target_at(hue, sat)`；
- 将候选 feature 反算为局部 Hue、SAT 和 orthogonal residual。

SAT=0 时 Hue 未定义，目标函数不会把任意 Hue 差异当成错误。

### 1.2 HSI 目标函数

`optimization/hsi_objective.py` 已实现词典序：

1. 是否满足所有 hard gate；
2. Hue 超出容差的部分；
3. SAT 超出容差的部分；
4. orthogonal shape；
5. shape P90/maximum；
6. 命令连续性。

它只接受冻结的 58 个 required feature。弱信号 feature 按 P1 规则重拍，混合质量、裁切、非有限和像素数失败不能降级。

### 1.3 五通道反馈

`optimization/hsi_feedback.py` 已实现：

- 一个 active channel 固定为 4095；
- 初始命令加四个自由通道 probe；
- 通用 box-constrained lexicographic local step；
- Broyden 更新；
- 测量拒绝时按 `1.0/0.5/0.25` 回退；
- 两次 settled confirmation；
- failed confirmation 后 thermal rebase；
- 不复用 CCT secant，因为 HSI 坐标不是单轴 CCT。

### 1.4 Pilot runner 和 analyzer

`optimization/measure_strip_hsi_pilot.py` 已实现：

- remote camera 和最新 location；
- 冻结 manifold/P2 basis/observer/hash；
- P2 piecewise basis 仅生成 seed；
- Ray 每张前显式 off；
- strip 每张后显式 off；
- 每目标独立自动曝光 cache；
- `1.25x` bounded weak-signal reacquire；
- Python cleanup。

`tmp/run-strip-hsi-pilot.zsh` 提供独立 shell `trap` cleanup。

`optimization/analyze_strip_hsi_pilot.py` 已实现：

- 13 个 target row 完整性；
- CR3 非空、recorded exposure、无 `.npy`/failure；
- Python/shell cleanup；
- SAT50/SAT100 的初始 gamut bracket；
- `faithful`、`unconfirmed` 和 `measurement_unreachable` 分离；
- 不自动冻结 Gate-6。

## 2. 当前 13 点 pilot

配置：`config/hsi/strip-hsi-pilot.json`

目标：

- SAT0：`H0/S0`；
- Hue：`0,60,120,180,240,300`；
- SAT：`50,100`；
- INT：`100`；
- 合计 13 点。

每点最多：

- 12 轮反馈；
- probe step 256；
- 单轮最大 step 768；
- 两次 60 秒 settled confirmation；
- failed confirmation 后可重建 Jacobian；
- 每个候选保持至少一个通道为 4095。

Dry-run：

`tmp/strip-hsi-pilot-offline/p7-pilot-dryrun-v1/plan.json`

所有 seed 均满足 full-scale 约束，但 P2 seed-only 的预测 relative RMSE 仍大约为 `18%..27%`。因此不能期待大多数点从 seed 直接通过；相机闭环会承担主要工作。

## 3. 离线验证状态

已经完成：

- manifold 插值和周期边界测试；
- SAT0 Hue undefined 测试；
- HSI objective 和 feature 拒绝测试；
- feedback、backtrack、confirmation/rebase 测试；
- fake runner 的 strip-only、Ray-off 和双 cleanup；
- fake 13 点 analyzer；
- wrapper 语法和 dry-run。

2026-07-17 本审计前重新执行的 P7 聚焦测试：`12/12` 通过。

尚未完成：

- 真实灯带 P7 capture；
- 当前全部工作区的最终完整测试和明确计数；
- 真实 Hue/SAT 收敛曲线；
- 真实 strip HSI 重复性；
- `s_exact_max(h)`；
- 随机留出；
- P8 INT。

## 4. 实拍前必须纠偏的风险

### 4.1 Strip 重复性尚未进入验收

`evaluate_hsi_observation()` 已预留：

- `strip_hue_three_sigma_degrees`
- `strip_sat_three_sigma_percent`
- `strip_shape_three_sigma`

但默认均为 `0.0`，当前 runner 没有传入有 provenance 的非零值。实际 tolerance 主要来自 Ray 流形重复性。

后果：

- 可能把测量极限内的真实匹配误判为 `unconfirmed`；
- 后续若看到不收敛才临时放宽，会形成数据后定阈值；
- `faithful` 的统计含义不完整。

P1 white-state strip repeatability 可以提供全局噪声下限，但不能未经转换就当作所有高饱和 HSI 点的 Hue/SAT 误差。需要 advisor 冻结组合方法。

### 4.2 完整 13 点成本过高

每点至少包含 initial、四个 probe、反馈和 settled repeats；measurement rejection、backtrack 和 thermal rebase 会继续增加 captures。13 点最坏可能达到数百张，且两次确认各等待 60 秒。

在没有真实 sentinel 收敛证据前直接长跑，可能重复 P4 的高成本 retry 模式。

### 4.3 Analyzer 的 command audit 还不完整

runner 和 fake 测试会记录/检查 Ray off 与 strip command，但正式 analyzer 当前主要验证 capture、measurement 和 cleanup，没有把 `commands.jsonl` 的每组顺序、Ray-on 禁止和唯一 strip-on 作为 hard gate。

这是可直接修复的代码完整性问题，不需要 advisor 选择算法，但必须在真实 run 前补齐。

### 4.4 Pilot 只能给初始 bracket

SAT50 或 SAT100 未通过，可能由以下原因造成：

- 目标真实不可达；
- seed 太差或局部 Jacobian 不足；
- 轮数/step 不合适；
- 热态漂移；
- strip 重复性未计入容差；
- RAW feature 在允许曝光包络内不可观测。

因此 pilot 的 `unconfirmed` 不能直接写成 `hue_unreachable` 或精确 gamut 边界。

### 4.5 计划状态文字有少量过时

总控 PLAN 的部分摘要仍写成“开始 P6 离线实现”，而真实状态已经是 P6 complete、Stage 6 active。执行低级模型前应同步状态，避免其重跑 P6 或误解 P7 已实拍。

## 5. 当前维护性判断

总体模块边界合理：Ray 流形、目标函数、反馈、runner 和 analyzer 分离，并复用现有 bounded solver、RAW observer、remote backend 和 cleanup。当前不需要大重构。

最小修复应集中在：

1. 单一、可追溯的 strip uncertainty 输入；
2. analyzer command audit；
3. sentinel 子集执行能力；
4. 对以上路径补回归测试；
5. 完整测试和代码检查点。

