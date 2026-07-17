# Advisor 决策请求与后续分支

## 1. 请求范围

请 advisor 只对本文件 D1-D5 给出决定。除非发现具体证据错误，不需要重审 P1-P6，不需要重拍 Ray-only 106 点，也不要提前设计完整三维 HSI LUT。

## 2. D1：P7 验收不确定性

### 需要决定

如何把 Ray 目标重复性、相机噪声和 strip 重复性组合成以下三个 hard gate：

- Hue 3-sigma tolerance；
- Ray-equivalent SAT 3-sigma tolerance；
- orthogonal shape 3-sigma tolerance。

### 推荐方案

采用两层不确定性：

1. **优化期间的预冻结下限**
   - Ray 部分继续由 P6 重复样本经局部流形 inverse/Jacobian 推导；
   - strip 部分由 P1 同几何、同 RAW observer、同曝光包络下的 scale-removed feature covariance 提供保守噪声下限；
   - 两源独立项按 quadrature 合成，不取简单最大值，也不直接相加；
   - 所用输入文件和 hash 写入 P7 plan。
2. **最终分类的局部复核**
   - 对候选命令做至少三张独立 60 秒 off/on settled capture；
   - 用同命令的局部坐标散布检查预冻结下限是否低估；
   - 若局部噪声显著更高，当前点标记 `uncertainty_unresolved`，不能在同一 run 内临时扩大门槛并宣布 faithful；
   - 需要新的定向 repeatability run 或 advisor 复核。

### 不推荐

- 继续把 strip 三项 tolerance 留为零；
- 直接把 P1 white feature CV 当 Hue 度数；
- 看到点不通过后按该点误差反推阈值；
- 用两张 confirmation 既估计噪声又证明通过，且没有预冻结下限。

Advisor 输出应明确选择：`approve_two_layer_uncertainty`、`approve_alternative_with_formula` 或 `request_targeted_repeatability_only`。

## 3. D2：Pilot 是否先做 sentinel

### 推荐决定

先运行 3 点 sentinel，而不是直接启动全部 13 点：

1. `H0/S0`：验证 pooled zero、白通道参与和 SAT0 Hue undefined；
2. `H120/S100`：P6/P2 中相对稳定的高饱和点，用来证明闭环基本可工作；
3. `H300/S100`：高曲率、P6 repeatability 较差且 seed 误差较高的压力点。

每点保留与正式 pilot 相同的：

- remote/location/hash；
- full-scale active-channel 约束；
- probe 和 feedback；
- frozen uncertainty；
- 60 秒 settled repeats；
- 双关灯和命令审计。

### Sentinel 放行条件

- 三点都没有 source-isolation、recorded exposure 或质量合同错误；
- 至少稳定点 `H120/S100` 收敛并通过局部重复性；
- SAT0 不出现 Hue 错误参与求解；
- 困难点即使不 faithful，也能给出可解释的 best valid candidate 和稳定 bracket；
- Jacobian 预测方向没有连续失准；
- 实际 captures/round 和总耗时处于可接受范围。

分支：

- 全部满足：继续剩余 10 点；
- 只有算法/审计错误：保留 run，离线修复后新目录重跑 3 点；
- 测量不可观测：先做定向 exposure/repeatability 诊断，不扩大完整网络；
- 广泛不收敛：advisor 复核 solver/feature coordinate，不进入 13 点。

Advisor 输出应明确选择：`sentinel_3_then_10` 或说明批准完整 13 点的理由。

## 4. D3：`faithful`、`unconfirmed` 和物理 gamut

### 推荐内部语义

- `faithful`：候选在冻结 uncertainty 下通过 Hue、SAT、orthogonal 三项，并通过独立 settled repeat；
- `unconfirmed`：当前预算/算法未证明 faithful，不代表物理不可达；
- `measurement_unreachable`：冻结 observer/exposure 包络内无法获得合法 feature，不代表灯带物理不可达；
- `boundary_bracketed`：已有一个 faithful 下界和一个非-faithful 上界；
- `hue_unreachable`：在足够低 SAT 仍不能保持 Hue，并已排除测量/求解问题；
- `gamut_compressed`：请求 SAT 超过已验证 `s_exact_max(h)`，运行时回退到 faithful 边界。

### `s_exact_max(h)` 的最小证明

1. 同 Hue 至少一个 faithful SAT 下界；
2. 至少一个稳定非-faithful SAT 上界；
3. 在 bracket 内二分或定向加密；
4. 边界候选有 settled repeat；
5. 记录 active-set 切换、敏感度和边界原因；
6. 不用 spline 平滑抹掉真实不连续。

Advisor 输出应确认上述术语，或给出替代字段和产品含义。

## 5. D4：何时进入 P8 INT

推荐保持现有门：

- 13 个 INT100 pilot 点完成；
- 所有主 Hue 至少有一个 faithful 范围；
- 需要的 `s_exact_max(h)` 已 bracket/搜索；
- 0/360 周期留出通过；
- 随机非节点 Hue/SAT holdout 通过；
- 运行时 gamut 语义已冻结。

在此之前不实现 `INT=50/20/5`，也不建立均匀三维 LUT。

Advisor 输出应选择：`keep_p8_locked_until_p7_holdout`，或明确允许提前采样的诊断性 INT 点及其非产品用途。

## 6. D5：允许执行模型自行修复的项目

建议 advisor 明确授权低级执行模型在不再次停顿的情况下完成：

- 将 strip uncertainty artifact/hash 接入 plan 和 objective；
- 增加 3 点 sentinel target selection；
- analyzer 强制 command/source-isolation audit；
- 同步 PLAN/README/skill 状态；
- 补单元测试、完整测试、compileall、wrapper syntax、diff-check、CodeGraph sync；
- 在已有设备授权仍有效时运行 3 点 sentinel，并按 D2 分支处理普通代码错误。

以下事项仍需停在高级决策门：

- 改变 observer threshold 或曝光包络；
- 把 unconfirmed 改成物理不可达；
- 改变 full-scale/绝对亮度产品语义；
- 进入 P8；
- 冻结 Gate-6 候选；
- 覆盖默认 LUT 或安装运行时配置。

## 7. 建议 Advisor 回复格式

```text
D1 uncertainty:
- decision:
- formula/artifact:
- confirmation count:

D2 pilot staging:
- decision:
- sentinel targets:
- pass/fail branch changes:

D3 gamut semantics:
- faithful:
- unconfirmed:
- measurement_unreachable:
- s_exact_max proof:

D4 P8 lock:
- decision:

D5 executor authority:
- approved autonomous fixes:
- mandatory stop conditions:
```

## 8. 推荐的唯一下一动作

在 advisor 给出 D1-D5 决定前，不启动 P7 实拍。允许只读检查和文档整理。收到决定后，执行模型先完成离线修复和全套验证，再运行 3 点 sentinel；不得直接启动完整 13 点或 P8。

