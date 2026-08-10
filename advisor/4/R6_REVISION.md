# Advisor 科学决定

```text
science_delta = accepted_valid_ray_r6_history_negative

history_dependence_observed = true
history_mechanism =
  not_identifiable_due_to_previous_state_vs_sequence_position_confounding

primary_working_hypothesis =
  approximately_rank1_cumulative_source_age_or_session_time_drift

c_specific_C_carryover =
  plausible_but_not_demonstrated

analysis_model =
  period_effect_plus_immediate_predecessor_carryover_screening_model

next_scientific_action =
  offline_vector_reanalysis_then_self_contained_order_balanced_Ray_history_experiment

strip = locked
combined_TD_B = locked
TD_C = locked
sentinel_and_later = locked

device_authorization = none
```

---

## 1. `A0` 与 `A_after_C` 不能解释成已经证明的 C 特异 history effect

当前结果证明的是：

```text
A 在固定 600 秒观察点不具有无条件、与运行历史无关的唯一中心
```

但没有证明：

```text
C 是造成该偏移的唯一原因
```

原因是 `C` 同时处于序列最后位置。以下两个因素在当前设计中完全混淆：

1. 前一状态是 `C=H300/S100`；
2. `A_after_C` 是整段连续运行中最晚的 A anchor，具有最大的累计 source-on time 和 session elapsed time。

而且六个 pairwise score 呈现出很强的**有序、近一维漂移**特征。由你提供的数值直接计算：

| 路径                                  |    分段距离之和 |      直接距离 |   直接/分段 |
| ----------------------------------- | --------: | --------: | ------: |
| `A0 → A_after_D → A_after_B`        |  `9.2849` |  `8.8556` | `0.954` |
| `A0 → A_after_B → A_after_C`        | `11.5447` | `11.3713` | `0.985` |
| `A_after_D → A_after_B → A_after_C` |  `7.7009` |  `7.3853` | `0.959` |

也就是说，三个 return anchor 更像沿着：

```text
A0
→ A_after_D
→ A_after_B
→ A_after_C
```

持续移动，而不是在 C 后突然跳到一个独立分支。

若暂时把六个 score 视为同一 whitened Euclidean metric，四点 classical MDS 的第一轴约解释 **97.9%** 的几何方差，坐标顺序也是单调的：

```text
A0 < A_after_D < A_after_B < A_after_C
```

由于实际 pair 使用的 diagonal variance 和 guarded limit 有极小差别，这个 `97.9%` 只能作为诊断证据，不能当作正式统计门。但它明显提高了“累积 thermal age / session-time drift”相对于“C 独有 hysteresis”的先验可信度。

另外，D、B、C 三个状态的 chronology trend 都高于 `4.0`，说明整个序列仍处于时间依赖状态；600 秒一直只是人工选择的 operational transient，不是 steady-state。

因此当前准确状态应改为：

```text
return_anchor_history_compatibility = fail

history_dependence_observed = true

history_effect_origin =
  not_identifiable_between:
    - cumulative_source_age_or_session_time
    - immediate_previous_state_carryover
    - their_interaction

operational_endpoint_600_unconditional_valid = false

operational_endpoint_600_conditioned_on_history =
  not_evaluable
```

不应写成：

```text
C_specific_history_effect = true
Ray_H300S100_causes_hysteresis = true
```

---

## 2. 当前应采用的模型：先用“period + carryover”筛选，不直接拟合复杂热模型

### 2.1 物理解释层

可以把 Ray 内部状态抽象成一个不可直接观测的 thermal/history state：

[
x_{k+1}=F_{q_k}(x_k)
]

[
f_A=\mu_A+H_Ax_k+\epsilon
]

其中：

* (x_k)：驱动、LED、扩散结构、壳体等共同形成的潜在热状态；
* (q_k)：此前经历的 A、D、B、C 状态；
* (F_q)：不同命令对潜在状态的推进；
* (f_A)：返回 A 后的 58-feature observation。

这只是合理的物理框架。当前数据不足以识别：

* 状态维度；
* 时间常数；
* 每个命令的 thermal equilibrium；
* A 的 recovery curve；
* 是否存在多个热时间常数。

因此**不批准现在就拟合 exponential、ODE、ARIMA 或多状态 thermal correction**。JCGM 允许对 drift 和动态测量建立时间模型，但也要求模型具有适用的数据范围，并评估其充分性；相邻时间观测本身也通常相关，不能按独立样本处理。([BIPM][1])

### 2.2 当前可识别的统计筛选模型

下一轮只使用：

[
\delta_{r,p}
============

\pi_p+\kappa_{q(r,p)}+\epsilon_{r,p}
]

其中：

* (r)：独立 session/run；
* (p\in{1,2,3})：状态在序列中的位置；
* (q\in{D,B,C})：立即前一状态；
* (\pi_p)：累计时间/thermal age/period effect；
* (\kappa_q)：前一状态的 immediate carryover；
* (\delta_{r,p})：`A_after_q - A0` 的 whitened 58-feature 差。

该模型的目标不是给 R6 做 correction，而是把两个此前混淆的解释分开：

```text
period effect
vs
previous-state carryover
```

R6 不能通过拟合该模型后重新变成 pass。此前 Advisor 已明确：thermal/time covariate 可以用于状态定义和诊断，但不能在同一数据上拟合后吸收失败。

---

## 3. 先做一次离线矢量复核，但它不能替代新实验

在任何新科学运行之前，应从 retained R6 的实际 58-feature vector 完成以下只读分析：

1. 使用一个固定的 common whitening matrix，重新计算四个 A anchor 的完整矢量差；
2. 检查：

   * `A0→Dreturn`
   * `Dreturn→Breturn`
   * `Breturn→Creturn`
     三个向量的 cosine；
3. 对四个 anchor 做 PCA/MDS，记录第一轴解释比例；
4. 冻结一个 R6-derived drift direction：

[
v=
\operatorname{normalize}
\left(
\operatorname{PC1}
\left[
W^{1/2}f_{A0},
W^{1/2}f_{AD},
W^{1/2}f_{AB},
W^{1/2}f_{AC}
\right]
\right)
]

5. 对每个 anchor 差报告：

   * 沿 (v) 的投影；
   * 与 (v) 正交的 residual；
   * 与实际 session elapsed、累计 source-on time 的关系；
   * 与 D/B/C 各自 dominant chronology direction 的关系。

该分析只能输出：

```text
rank1_drift_hypothesis_supported | unsupported
```

不能输出：

```text
C_carryover_confirmed
operational_600_valid
R6_pass
```

因为单一的 `D→B→C` 顺序存在结构性混淆，任何事后回归都无法凭数学手段创造缺失的 counterfactual。

---

## 4. 最小有界科学实验：自包含的 3×3 顺序平衡 Ray history experiment

### 4.1 决定

需要新的 Ray history experiment。仅改变分析模型不足以识别原因。

但这不是重拍 R6，也不是扩大原 16-frame run。它应是一个新的、只回答 history attribution 的自包含实验。

为遵守当前禁止跨 root pooling 的约束，R6 仅作为：

```text
hypothesis-generation evidence
and pre-registration source for drift direction v
```

不得进入新实验的模型拟合、pass/fail 或 covariance。

### 4.2 三个独立顺序

新实验内部自行完成一个 3×3 cyclic order-balanced design：

```text
Session 1: D → B → C
Session 2: C → D → B
Session 3: B → C → D
```

这样 D、B、C 各自在：

```text
position 1
position 2
position 3
```

恰好出现一次。

一个额外顺序仍无法充分解除 state 与 period 的混淆；三个顺序是最小完整平衡集合。

### 4.3 每个 session 的科学采样

每个 session 只测 600 秒 endpoint：

```text
A0 @ 600

Q1 @ 600
A_after_Q1 @ 600

Q2 @ 600
A_after_Q2 @ 600

Q3 @ 600
A_after_Q3 @ 600
```

每个 session：

```text
7 captures
```

完整新实验：

```text
3 sessions × 7 = 21 Ray captures
```

不再拍 D/B/C 的 `60/120/300`，因为：

* 它们已经证明 `time_dependent_within_600=true`；
* 本实验不再询问“是否 settled”；
* 唯一问题是固定 operational endpoint 下，A return 的偏移由 position 还是 predecessor state决定。

该 21-frame 设计是新的科学实验建议，不是本回复直接授予的设备执行权限。

---

## 5. 新实验的预冻结分析

### 5.1 主响应

使用 R6 冻结、但不与新数据混合的 drift direction (v)：

[
z_{r,p}
=======

v^T
W^{1/2}
\left(
f_{A,r,p}-f_{A0,r}
\right)
]

同时计算正交残差：

[
r_{\perp,r,p}
=============

\left|
(I-vv^T)
W^{1/2}
\left(
f_{A,r,p}-f_{A0,r}
\right)
\right|
]

使用每个 session 自己的 `A0` 消除 session baseline，但分析 covariance 必须考虑：同一 session 的三个差值共享同一张 `A0`，因而彼此相关。

### 5.2 筛选模型

[
z_{r,p}
=======

\alpha_r+\pi_p+\kappa_{q(r,p)}+\epsilon_{r,p}
]

* (\alpha_r)：session effect；
* (\pi_p)：position/cumulative-time effect；
* (\kappa_q)：D/B/C carryover。

不增加新阈值；effect 是否可区分继续使用冻结 measurement covariance 和 guarded joint coverage。

NIST 的 drift-elimination方法要求近似线性漂移和等时间间隔；本设计不假定能够“消除”当前 drift，而是通过顺序平衡直接估计离散 period effect，因此不得称为 ABBA correction。([NIST][2])

---

## 6. 预先冻结的五个科学分支

### 分支 A：主要是累计 thermal age / period effect

条件结构：

```text
pi_1, pi_2, pi_3 show ordered separation
kappa_D, kappa_B, kappa_C mutually compatible
orthogonal residual acceptable
```

结论：

```text
history_model =
  cumulative_source_age_or_session_time

C_specific_carryover = false_at_detectable_level
```

产品语义：

```text
600 s after command switch
```

仍不足以唯一规定 Ray 输出，还必须同时规定：

```text
cumulative source age / period position
```

不能继续使用一个无 thermal-age 条件的 Ray target center。

### 分支 B：C 特异 carryover

条件结构：

```text
adjusted kappa_C differs from kappa_D and kappa_B
effect reproduces when C occurs early, middle and late
period effect compatible with zero or clearly smaller
```

结论：

```text
history_model =
  immediate_previous_state_carryover

C_specific_carryover = demonstrated
```

这意味着固定的、history-free 600 秒单一 LUT 语义不成立；后续科学模型至少必须包含 previous-state class。

### 分支 C：两者同时存在

```text
period effect significant
and
C carryover significant
```

结论：

```text
history_model =
  mixed_cumulative_age_and_state_specific_carryover
```

此时简单的固定 dwell 或单一 previous-state correction 都不充分。

### 分支 D：additive model 被拒绝

若出现：

```text
large state × position interaction
large orthogonal residual
different drift direction by order
```

结论：

```text
history_model =
  nonlinear_latent_state_required
```

只有此分支才有依据设计更完整的 state-space / recovery-curve 实验；当前不预先授权。

### 分支 E：R6 split 未复现

若新实验中 period 与 C effect 均未超过冻结门，且三个 session 的 A returns 兼容：

```text
R6_history_negative =
  valid_single-run_anomaly_not_generalized
```

R6 仍保持原始 formal fail，不改写；但不能据它安装永久 history model。

---

## 7. Strip、combined 与 TD-C 继续锁定

决定：

```text
strip = locked
combined_operational_600 = locked
TD_C = locked
```

原因不是工程门，而是 Ray reference 目前不存在一个已证明的、无条件唯一的 600 秒中心。此时运行 strip 会使：

```text
strip error
+
Ray cumulative-age drift
+
Ray previous-state carryover
```

不可分离。

TD-C 是 Ray/strip source comparison，不是用来识别 Ray 内部历史机制的实验。提前运行 TD-C 只会把 unresolved Ray reference effect 错记为 source difference。

这也与 GUIDE 4 的既有分支完全一致：完整 Ray acquisition 即使 `16/16 quality pass`，只要 return-anchor history fail，就必须 `stop_history_model_required`，新 strip 继续 blocked；combined gate 失败则 TD-C 继续锁定。 

继续保持：

```text
reference epoch final classification = locked
four-point sentinel = locked
remaining 9 = locked
boundary / holdout / Gate-6 = locked
P8 = locked
default LUT installation = locked
```

---

## 可直接交给 Planner 的 exact decision

```text
Advisor accepts Ray R6 as a valid scientific negative.

Do not classify the sole A0-vs-A_after_C failure as demonstrated
C-specific hysteresis.

Current classification:
  history_dependence_observed = true
  history_origin =
    not_identifiable_between_cumulative_period_effect_and_predecessor_carryover
  preferred_working_hypothesis =
    approximately_rank1 cumulative source-age/session-time drift
  C-specific carryover = unproven

First perform a read-only vector reanalysis of the retained R6 anchors:
  common whitening,
  difference-vector cosine,
  PCA/MDS rank,
  projection onto a frozen R6 drift direction,
  orthogonal residual,
  relation to elapsed/source-on time.
This analysis must not correct, reclassify or pass R6.

Analysis alone cannot resolve the causal confounding.

The minimum self-contained scientific identification experiment is a
three-session cyclic order-balanced Ray-only experiment:

  session 1: D -> B -> C
  session 2: C -> D -> B
  session 3: B -> C -> D

Each session captures only:
  A0@600,
  Q1@600, A_after_Q1@600,
  Q2@600, A_after_Q2@600,
  Q3@600, A_after_Q3@600.

Total new scientific observations:
  21 Ray captures.

R6 is hypothesis-generation evidence only and must not be pooled into the
new experiment's fit or pass/fail result.

Analyze the new experiment with:
  return_anchor_delta =
    session + sequence_position + immediate_predecessor_state + residual,
using the frozen observer, 58 features, uncertainty and guarded coverage.
No threshold, covariance, exposure or frame-selection change is permitted.

Classify the result as:
  period-only,
  C-carryover-only,
  mixed,
  nonlinear/non-additive,
  or R6-not-reproduced.

Until that classification is complete and reviewed:
  strip remains locked,
  combined TD-B remains locked,
  TD-C remains locked,
  sentinel and all later stages remain locked.

This scientific decision does not itself authorize device acquisition.
```

[1]: https://www.bipm.org/documents/20126/2071204/JCGM_GUM_6_2020.pdf "Guide to the expression of uncertainty in measurement - Part 6: Developing and using measurement models"
[2]: https://www.itl.nist.gov/div898/handbook/mpc/section3/mpc3312.htm "2.3.3.1.2. Bias caused by instrument drift"
