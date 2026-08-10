# PLAN-FULL — GUIDE 4 Ray history identification route

**性质：** 可由 Git 追踪、供 Human 与 agent 阅读的 non-executable scientific roadmap

**科学权威：** `advisor/4/4.GUIDE.md` + `advisor/4/R6_REVISION.md`

**当前分支：** `codex/guide4-science-path-v3`

**路线状态：** `R6_VECTOR_REANALYSIS_COMPLETE_WAITING_ADVISOR_SESSION_INDEPENDENCE_DEFINITION`

**唯一下一科学动作：** Advisor 冻结 session 独立起始/冷却条件后，执行一个新的、自包含的三 session / 21-frame cyclic order-balanced Ray-only history identification experiment

**当前设备边界：** Human 已明确本地有界 Ray/相机采集不需要单独授权；固件刷写、远程部署等高危操作仍禁止

本文件不是 production/test 输入、runtime 状态机、设备授权、release、lineage、stage-gate 或 hidden gate。设备动作必须由当前执行说明和 owning runner 精确限定。

---

## 1. 冻结科学状态

Ray R6 保持有效科学负结果：

```text
history_dependence_observed = true
R6 formal_pass = false
R6 reclassification = forbidden
history_origin =
  not_identifiable_between_cumulative_period_effect_and_predecessor_carryover
preferred_working_hypothesis =
  approximately_rank1 cumulative source-age/session-time drift
C-specific carryover = unproven
```

不得把唯一 `A0` vs `A_after_C` split 写成已证明的 C-specific hysteresis。R6 只能用于：

1. hypothesis generation；
2. 预冻结新的 common-whitened drift direction `v`。

R6 frame 不得进入新实验的 fit、coverage、pass/fail、covariance 或 frame selection。

继续冻结：

```text
strip TD-B = locked
combined TD-B = locked
TD-C = locked
reference epoch final classification = locked
sentinel / remaining 9 = locked
boundary / holdout / Gate-6 = locked
P8 / default LUT install = locked
```

---

## 2. 已完成：retained R6 read-only vector reanalysis

权威 artifact：

```text
.agent-work/evidence/R6_VECTOR_REANALYSIS-20260809.json
sha256 = 68df8420dbdeabe19eb314d212e63404c0a1f67a141863c6357756b0aa301918
analyzer commit = 71779fcec88d3ba8d36d8ed08292c7da1e9d2a97
source evidence ZIP sha256 =
  924303915131eb6fc8e9d00cd8231b8f8dd403e06399318e74e083ad277260dd
source bundle member =
  ADVISOR_HANDOFF-20260808-RAY-R6-HISTORY-FAIL/run
```

外置卷在本次 reanalysis 时未挂载。分析使用先前已通过 bundle manifest 验证的 byte-exact 小型证据；不读取 CR3、不重新采集、不改写原 `analysis.json`。

### 2.1 Common-whitened geometry

使用：

```text
ordered 58-feature unit shape
common covariance = 2 × frozen ray-within-state diagonal variance
```

结果：

```text
status = rank1_drift_hypothesis_supported
PCA rank = 3
PC1 explained variance = 0.9792670761283614
MDS positive rank = 3
MDS axis-1 explained variance = 0.9792670761283614
```

三个连续 difference-vector cosine：

| vectors | cosine |
| --- | ---: |
| `A0→A_after_D` vs `A_after_D→A_after_B` | `0.8182052864` |
| `A0→A_after_D` vs `A_after_B→A_after_C` | `0.9337227259` |
| `A_after_D→A_after_B` vs `A_after_B→A_after_C` | `0.8233821163` |

沿 frozen R6 drift direction 的 anchor projection 严格单调：

| anchor | projection | orthogonal residual | session elapsed s | source-on s |
| --- | ---: | ---: | ---: | ---: |
| `A0` | `0` | `0` | `612.6669` | `607.3993` |
| `A_after_D` | `4.0346508474` | `1.4075586189` | `1842.4832` | `1837.2156` |
| `A_after_B` | `8.8375784598` | `0.5649286217` | `3072.5758` | `3067.3082` |
| `A_after_C` | `11.3569242597` | `0.5710914156` | `4302.4466` | `4297.1791` |

```text
projection vs session elapsed Pearson r = 0.9931921824
projection vs source-on elapsed Pearson r = 0.9931921824
causal claim allowed = false
```

R6 drift direction：

```text
sha256 = bb707f600272968af656ba890535ebb161e0f45209249adde1aa72cdf3dfba57
orientation = A0 toward A_after_C positive
use = hypothesis generation and pre-registered projection only
```

D/B/C chronology direction 与该轴的 cosine 分别为：

```text
D = 0.6769789578
B = 0.5904605934
C = 0.3185435654
```

结论只允许：近 rank-1 累积 drift working hypothesis 获得支持。正交 residual 非零、单一顺序因果混淆仍存在；不能输出 C-carryover confirmed、operational-600 valid 或 R6 pass。

---

## 3. 已完成：最小直接 acquisition/analyzer 边界

在现有三个 owner 内完成，不创建 runtime/framework/package/governance 层：

- `p7_thermal_diagnostics.py`：新增一个 exact 3×3 / 21-frame scientific spec builder；
- `measure_p7_thermal_diagnostics.py`：复用现有 `execute_plan` 和真实 capture/command/cleanup mechanics；
- `analyze_p7_thermal_diagnostics.py`：新增该 experiment 的离线分类函数；直接消费新 root 和本计划第 2 节冻结的 `v` artifact。

fake-backend behavior tests 已证明：

1. exact 3 sessions 与 exact order；
2. 每 session 7 captures，总计 21；
3. 每个 Q 和 return A 都是 600 s；
4. session 开始和结束执行 all-off/zero cleanup；
5. session 内从首次 Ray on 到结束 cleanup 不发送 Ray-off；
6. strip 始终 zero/readback；
7. 真实 scheduler、capture、physical ledger、quality、cleanup 路径被复用；
8. retry=0、无 setup/ambient/frame selection；
9. R6 direction 只作为 immutable projection input，不把 R6 frame 混入新 fit；
10. analyzer 只输出五个预冻结分支之一。

新增 CLI 默认 dry-run 为 `device_locked`；真实执行必须同时提供
`--session-index` 和 Advisor 冻结后、当次实际观察到的 `--session-start-condition`。每个 session
由现有 shell wrapper 独立启动，因此拥有独立 Python/shell cleanup 和 run root。

Focused 行为验证：`12/12 passed`（新 5 项 + 未依赖外置卷的既有 R6 7 项）；
另一次完整 `DirectR6Tests` 得到 `12 passed / 2 errors`，两个 error 均是当前
`/Volumes/4T` 未挂载导致旧 strip/TD-C fixture 找不到 retained R1，未进入被改代码。
Compileall、dry-run exact 3-session inspection 与 `git diff --check` 通过。

不插入新的 readiness、review package、selector budget、candidate rejection 或 architecture boundary。

---

## 4. Advisor scientific decision boundary

Human 已明确：本地有界 Ray/相机采集无需单独授权；只有固件刷写、远程部署等
高危操作需要授权。本实验不包含这些高危操作，因而不再保留 Human token gate。

当前唯一未冻结项是三个“独立 session”的科学起始条件：

- session 间 Ray/strip off 多久；
- 是否沿用历史 `1800 s` cold proxy，或采用另一可复现条件；
- 起始条件由固定 wall-clock cooldown、温度/状态 readback，还是两者共同定义。

该选择会直接改变 cumulative source-age/session-time 与 predecessor carryover 的可识别性，
属于 measurement-science design，不是设备安全或普通工程参数，必须由 Advisor 冻结。

已冻结且无需再次决策的执行范围：

```text
experiment = GUIDE4-RAY-HISTORY-ORDER-BALANCED-3X3-V1
device = Ray120c + Canon camera; strip zero-only
sessions = 3
formal captures = 21
session launches = 3
retry = 0
per-state dwell = 600 s
Ray intensity = 100%
orders = DBC / CDB / BCD
cleanup = Python + shell all-off and zero readback per session
```

Advisor 决定前允许：代码、fake backend、离线测试、spec/hash、执行说明草案、
只读设备健康/zero 检查。决定前禁止创建 formal root 或启动 Ray/camera acquisition，
因为任意自选 cooldown 都可能破坏实验的因果解释。

---

## 5. 新实验预冻结合同

### 5.1 新实验身份

```text
experiment_id = GUIDE4-RAY-HISTORY-ORDER-BALANCED-3X3-V1
source = Ray only
new experiment root = one
session subroots = three
R6 pooling = false
R6 use = frozen drift direction only
```

### 5.2 Cyclic order-balanced design

```text
Session 1: D → B → C
Session 2: C → D → B
Session 3: B → C → D
```

每 session：

```text
A0@600
Q1@600 → A_after_Q1@600
Q2@600 → A_after_Q2@600
Q3@600 → A_after_Q3@600
```

```text
7 captures/session
3 sessions
21 formal/physical total
ambient/setup = 0/0
retry = 0
```

不拍 60/120/300；本实验不再询问 settled，只识别固定 operational 600 endpoint 下的 position 与 immediate predecessor effect。

### 5.3 Frozen measurement contract

- observer：Canon native-Bayer identity RAW；
- features：原顺序与 hash 的 58 features；
- uncertainty/common whitening/guarded joint coverage：冻结不变；
- clipping、near-noise、valid-pixel、finite 与 physical ledger：冻结不变；
- nominal shutters：A=`1/5000`、D=`1/6400`、B=`1/8000`、C=`1/2500`；
- Canon recorded seconds 只验证 setting consistency，容许既有 `1/8 EV` 以内编码差；
- commands/intensity：使用 R6 exact A/D/B/C Ray commands，100%；
- source isolation：strip 全程 five-channel zero；
- cleanup：每 session 正常、异常、signal 均 all-off，随后 readback；
- 不改 threshold、covariance、exposure 或 frame selection。

---

## 6. 预冻结分析

### 6.1 主响应

每 session 使用自己的 A0：

```text
delta[r,p] = common_whiten(A_after[r,p] - A0[r])
z[r,p] = frozen_R6_v · delta[r,p]
r_perp[r,p] = ||(I - vvT) delta[r,p]||
```

三个 delta 共享同一 A0，covariance/coverage 必须保留其相关性；不得把 9 个差值当独立样本。

### 6.2 Screening model

```text
return_anchor_delta =
  session + sequence_position + immediate_predecessor_state + residual
```

等价 scalar projection：

```text
z[r,p] = alpha_session[r] + pi_position[p] + kappa_predecessor[q] + epsilon[r,p]
```

设计是 3×3 cyclic Latin square；D/B/C 各自在 position 1/2/3 出现一次。模型只做 period vs carryover screening，不拟合 exponential、ODE、ARIMA、state-space correction，也不校正 R6。

Effect 是否可区分仅使用 frozen measurement covariance 与 guarded joint coverage。不得新增 p-value threshold、经验 cut、frame drop 或 data-dependent direction。

---

## 7. 五个预冻结科学分支

Analyzer 必须输出且只输出：

1. `period-only`
   - position effect ordered/separated；D/B/C adjusted carryover compatible；orthogonal residual compatible。
2. `C-carryover-only`
   - adjusted C carryover 与 D/B 可区分并跨 early/middle/late 复现；period compatible 或更小。
3. `mixed`
   - period 与 C carryover 均可区分。
4. `nonlinear/non-additive`
   - large state×position interaction、order-specific direction 或 orthogonal residual 不兼容 additive model。
5. `R6-not-reproduced`
   - period 与 C effect 均未超过 frozen coverage，三个 session 的 A returns 兼容。

任何 engineering invalid 都不是第六个科学分支；它必须 fail closed，保留 evidence，不自动 retry。

---

## 8. 完成与后续锁

21-frame experiment 获得完整、有效五分支分类后：

1. 停止设备推进；
2. 生成小型 Advisor review pack；
3. 在 Advisor review 前继续锁定 strip/combined/TD-C/sentinel/later stages；
4. Advisor review 决定是否以及如何改变后续 GUIDE 路线；
5. 不因 `period-only` 或 `R6-not-reproduced` 自动解锁 strip。

因此当前 PLAN-FULL 的最近可执行终点不是 strip，而是：

```text
complete_21_frame_order_balanced_Ray_history_classification
then_wait_for_Advisor_review
```

---

## 9. 执行顺序

```text
1. retained R6 vector reanalysis                         COMPLETE
2. freeze v + hashes + PLAN-FULL                        COMPLETE
3. minimal direct 3×3 spec/acquisition/analyzer code    COMPLETE
4. fake-backend behavior validation                     COMPLETE
5. Advisor freezes independent-session start condition REQUIRED BEFORE DEVICE
6. execute 3 sessions / 21 captures                     LOCKED
7. analyze to one of five branches                      LOCKED
8. Advisor review                                       LOCKED
```
