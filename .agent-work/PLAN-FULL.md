# PLAN-FULL — GUIDE 5 science-first route

**性质：** Git 可追踪的科学路线记录；仅供 Human、Advisor 与 agent 阅读，不是
production/test 输入、runtime 状态机、设备授权或 hidden gate。

**科学权威：** `advisor/5/5.GUIDE.md` 与 `advisor/5/5.RESEARCH.md`（本轮 Advisor
文件 SHA-256 已由提交记录验证）。

**上游完成状态：** GUIDE 4 Ray COLD600 V3 已被接受为有效科学证据；原报告中的
`nonlinear/non-additive` 已由 Advisor 明确拒绝为过强分类，原始
`analysis.json` 保持不可变。

**当前路线状态：** `TD_C_CORE_CORRECTED_REANALYSIS_THEN_FAST_B_C_HOLDOUT`

**当前下一步：** 保持已完成的 TD-C core acquisition 与旧 `analysis.json` 不变，
生成 corrected derived analysis；若精确通过，只执行新的 FAST B/C endpoint holdout。
legacy expansion、solver sentinel 和 later stages 继续锁定。

<!-- FEATURE-CONTEXT:GUIDE5-TD-C-FAST-ENDPOINT-HOLDOUT -->
## GUIDE5-TD-C-FAST-ENDPOINT-HOLDOUT — Advisor 纠偏与最小后续动作

**Advisor 决定：** 接受 TD-C core 8 帧；旧 `analysis.json` 保持不可变但其 estimand
语义不得沿用。先生成 source-specific contrast covariance 的 derived artifact；通过后
只解锁 `GUIDE5_TD_C_FAST_ENDPOINT_HOLDOUT_B_C_V1`。

| 要求 | 验收证据 |
| --- | --- |
| Ray/strip/paired/order 使用各自 contrast covariance | derived artifact 与精确 score regression |
| difference limit 从 source-level unit observation Monte Carlo 生成 | 实现测试拒绝 difference-center helper 路径 |
| A offset 非零不是 pre-solver failure | refined classification + diagnostic-only zero result |
| B/C 四 session、8/8、0 ambient、FAST reset600/op120 | canonical spec 与 fake-backend scheduler test |
| holdout 只检验 repeatability 与 independent synthesis agreement | endpoint analyzer behavior tests |
| legacy expansion、solver、sentinel/later 禁止 | spec/CLI rejection tests；PLAN locks |

最小端到端结果：不可变 core-v2.1 精确通过后，执行一次新的 8-frame B/C endpoint
holdout，分析后回 Advisor，不自动进入 solver。

允许结构变化：只扩展现有 `p7_thermal_diagnostics.py` protocol builder、现有
measurement CLI/runner、现有 analyzer 与对应 `test_p7_direct_r6.py` 行为测试；不得
新增 runtime/framework/owner。

<!-- SECTION:S01 -->
### S01 — TD-C core source-specific derived contrasts

- 权威：本轮 Advisor exact decision。
- 依赖：已接受的 8-frame core root 和不可变 `analysis.json`。
- 允许编辑：`analyze_p7_thermal_diagnostics.py`、`test_p7_direct_r6.py`。
- 排除：采集、原 artifact 修改、variance/feature/coverage 改动、solver。
- covariance：Ray pair=`2ΣR`；strip pair=`2ΣS_A`；paired offset pair=
  `2(ΣR+ΣS_A)`；order mean contrast=`ΣR+ΣS_A`；absolute mean offset=
  `(ΣR+ΣS_A)/4`。所有 limit 必须从 source-level unit observations 做 Monte Carlo，
  不得以 difference vector 作为 unit center。
- 验收：四个 max score 分别复现 `4.7728227800 / 5.3379311421 /
  5.7765306838 / 3.2538875744` 且 pass；absolute score 非零且仅 diagnostic；derived
  artifact 写入独立路径。
- review：一次有材料价值的 bounded review（统计 estimand/covariance 语义）。

<!-- SECTION:S02 -->
### S02 — FAST B/C endpoint holdout

- 权威：本轮 Advisor exact decision；仅在 S01 通过后执行。
- 依赖：core-v2.1、combined FAST coordinate canonical artifact。
- 允许编辑：`p7_thermal_diagnostics.py`、`measure_p7_thermal_diagnostics.py`、
  `analyze_p7_thermal_diagnostics.py`、`test_p7_direct_r6.py` 与一个现有风格 wrapper。
- 排除：legacy 1800/t_formal expansion、ambient、solver/probe/command adjustment、
  sentinel/later stages。
- 验收：四 session 精确为 B Ray→strip、C strip→Ray、B strip→Ray、C Ray→strip；
  每 source `reset600→D120→A120→Q120→capture`；8/8/0；analyzer gate 为 B/C
  paired-offset consistency + independent synthesis agreement，不 gate zero offset；
  `retry=0` 禁止同一 run 内隐藏重采。
- synthesis：`d_new_q - (mean_d_A_core + mean_local_q_combined)`；formal residual
  covariance 必须等于新两-session endpoint mean、core 四-session A mean、combined
  local-coordinate state mean三项独立 covariance之和；新 endpoint 不得回填或重拟合
  core/combined artifact。
- review：一次有材料价值的 bounded review（设备顺序与测量科学 gate）。

计划复核状态：`APPROVED_AFTER_BOUNDED_CORRECTION`。

## 1. 不可变科学合同

```text
observer = Canon native-Bayer identity RAW
features = frozen ordered 58 features (R/G1/G2/B)
quality / clipping / near-noise / finite / coverage = frozen
covariance / pair variance / guarded limits = frozen
exposure and frame selection = frozen
source isolation = frozen
P6 topology = full_periodic_2d_HB
SAT0 Hue = undefined
R6 = valid scientific negative; no reclassification; no pooling
steady / settled / cold-equilibrium claim = prohibited
```

两个正式包络：

```text
fast_op120_reset600_v1
  reset_class = human_bounded_reset_600
  reset/off proxy <= 600 s
  initial precondition <= 120 s
  state-to-capture dwell <= 120 s

long_op600_reset1800_v1
  reset/off proxy = 1800 s
  state-to-capture dwell = 600 s
  holdout only; not fit/covariance/threshold input
  required long sessions = 2; maximum = 3
```

两种包络的中心和误差不得合并；不得把热偏移扩入随机 covariance。

## 2. A1 — analyzer-v2（已完成）

已在现有 COLD600 V3 root 上离线运行一次派生 analyzer，未重采集，未修改原
`analysis.json`：

```text
derived = /Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-cold600-v3-20260810-081551/analysis-v2-common-reentry-derived.json
sha256 = 3f23ed6c949217c104121b43e20300e21b0a70a60349f80ffeb95844797d9986
classification = common_warm_reentry_shift
legacy_classification = nonlinear/non-additive
common_warm_reentry_score = 14.846865020488382
common_warm_reentry_guarded_limit = 9.543878618146513
additive_model_rejected = false
period_main_effect_detected = false
predecessor_main_effect_detected = false
nonlinear_interaction_demonstrated = false
orthogonal_to_frozen_r6_direction_detected = true
r6_rank1_direction_transfer = rejected
r6_frames_pooled = false
```

`orthogonal_to_frozen_r6_direction_detected` 仅表示旧 R6 PC1 无法迁移到当前 fast
协议，不再触发非加性分类。原始 COLD600 `analysis.json` SHA-256：
`0628736473668cceee9657f3a6770663e53728a3bb4ce10a871770bbf6c9136b`。

## 3. A2 — fast Ray target artifact（已完成）

已从 21 条 retained COLD600 capture ledger 离线派生：

```text
config/hsi/ray-fast-op120-targets-v1.json
sha256 = d1c4bcfb4fd268daa711dc11bd2d2119b9e07ce6d238df1d90702ccc996f8b40
```

精确成员：

```text
A / H120-S100 = 9 个 A_after_D/B/C warm-return captures
A0             = 3 个 initial captures，明确排除
D / H120-S50  = 3 个 direct captures
B / H0-S0      = 3 个 direct captures
C / H300-S100  = 3 个 direct captures
```

该 artifact 只支持四个直接状态，不外推完整 P6 manifold；继续使用冻结 covariance，
不得从 3 或 9 个样本估计新 covariance。

## 4. B — strip-only fast history（已完成，S-A2）

A1 canonical 输出为 `common_warm_reentry_shift` 且证据检查已通过，当前已解锁。
GUIDE5 中额外的 Human authorization 要求与 AGENTS.md 的授权优先级冲突，按
AGENTS.md 不构成停止门；高危操作仍按高风险授权条款执行。

```text
experiment_id = GUIDE5-STRIP-HISTORY-ORDER-BALANCED-3X3-OP120-RESET600-V1
source = strip only
Ray = zero throughout
orders = DBC / CDB / BCD
sessions = 3
captures per session = 7
total = 21
reset proxy = 600 s
dwell = 120 s
solver = prohibited
retry = 0
```

每 session：`A0@120 → Q1@120 → A_after_Q1@120 → Q2@120 → A_after_Q2@120 → Q3@120 → A_after_Q3@120`。
使用冻结 retained A/D/B/C strip commands and hashes；all-off/zero cleanup 必须在
正常、异常和 signal 路径执行。

分支：`common_warm_reentry_shift` 或 `no_history_effect_detected` 可接受 strip
fast-history model；`additive_period_or_carryover_effect`、
`interaction_or_nonadditive_unresolved` 或 measurement failure 均在 combined 之前
回 Advisor。

### B 结果（2026-08-10）

三个 order-balanced session 已完成 `21/21`，quality、physical return、wrapper
和 cleanup 全部通过。冻结 analyzer-v2 输出 `underpowered_or_unclassified`，其
SHA-256 保持
`7f1325fed769cbfe03623e7a76ffc155ea46ed03c60c8db36dbef8c1c3aea9d6`。
Advisor 确认 v2 错把 treatment-coded baseline-cell intercept 当作 balanced common
effect。修正后的只读 analyzer-v3 输出：

```text
artifact = /Volumes/4T/temp/rgbww-optimizer/guide5-strip-history-3x3-op120-reset600-20260810-2141/analysis-v3-strip-common-and-session-derived.json
sha256 = 0e8ad4eabd5acbb8ef6a6cbcf7fa3fde2fee8d13ad6cdf3c58446325461ea58e
guide5_parent_branch = S-A
classification = common_warm_reentry_shift_with_session_block_heterogeneity
balanced common score / guard = 13.5891110356185 / 9.561891733668457
session3-session2 score / guard = 9.950862478050007 / 9.561711294035568
```

strip fast-history structure conditional accepted；不冻结 global cross-session warm center，
不要求新的 strip acquisition。未来 combined comparison 使用 local warm anchors 并将
session 作为 blocking factor。完整证据见
`.agent-work/GUIDE5-STRIP-HISTORY-V3-RESULT.md`。

## 5. C — paired fast-vs-long Ray bridge（已完成并接受）

与 B 使用独立 root，不并行；不训练 fast target，不改变 covariance。该实验是有界
Ray/相机采集，不属于 AGENTS.md 定义的高危操作。

```text
states = C (H300/S100) and B (H0/S0)
C pair = FAST then LONG
B pair = LONG then FAST
FAST = reset600, A/Q/A dwell120
LONG = reset1800, A/Q/A dwell600
required = 4 mini-sessions / 12 captures / 2 long sessions
maximum = 6 mini-sessions / 18 captures / 3 long sessions
```

只报告 fast-vs-long 的 Q center、A-return、common-bias 与 state-dependent-bias；
long 数据保持 holdout。结果分为 `thermal_bias_not_detected`、
`common_protocol_bias_detected`、`state_dependent_protocol_bias_detected` 或
`validation_inconclusive`。前三类不自动否定 fast envelope，最后一类保持 combined 锁定。

Advisor 接受 12/12 acquisition 为 valid holdout。原 v1 保持不可变，新增只读 v2：

```text
artifact = /Volumes/4T/temp/rgbww-optimizer/guide5-ray-fast-long-bridge-20260810-194802/analysis-v2-fast-long-local-anchor-derived.json
sha256 = 08f7eaf6f94914e675d56353a9ad8b240215fcda92b3cbfe54ab122564b83511
classification = state_dependent_Q_center_protocol_bias_detected_on_B_C_holdout
B local-anchor = compatible
C local-anchor = detected
B-vs-C local-anchor = detected
FAST/LONG pooling = prohibited
common transfer / covariance inflation / extrapolation beyond B/C = prohibited
```

## 6. D — combined TD-B FAST local-coordinate（已完成，canonical pass）

```text
artifact = /Volumes/4T/temp/rgbww-optimizer/guide5-ray-fast-long-bridge-20260810-194802/p7-combined-fast-history-coordinate-v1.json
sha256 = adc3b59a0bbc1334ca7eb0f89e11a6850dd06b61bafafeccaef9e53791d1537a
coordinate = (Q_strip-A_after_Q_strip)-(Q_ray-A_after_Q_ray)
cells = 9 matched FAST cells
source captures = 42
LONG inputs = 0
session / position / additive residual = pass
evidence identity / no pooling = pass
classification = fast_local_anchor_coordinate_compatible_for_paired_source_comparison
```

state terms 被保留为之后 solver 处理的 strip-Ray mismatch，不在零点门禁中。

## 7. E — TD-C core（已完成，等待 Advisor）

```text
sessions = 4
orders = Ray→strip / strip→Ray / Ray→strip / strip→Ray
per source warm precondition = both-off reset600 → same-source D120 → same-source A120
formal capture = A_warm_after_D only
total captures = 8
steady claim = false
```

只检验 within-session strip-Ray difference 可重复性、source order effect 和 absolute
warm-A cross-source anchor。结果：

```text
root = /Volumes/4T/temp/rgbww-optimizer/guide5-td-c-core-20260812-151638-noambient-fix
accepted / physical = 8 / 8
quality / wrapper / cleanup / final zero = pass / pass / pass / pass
analysis = analysis.json
analysis sha256 = a4f4303b391c6eca5bf4a59fd1e95bf1b505b28bad4eda1c081f5d54d98a6aa0
status = td_c_core_pass_waiting_for_planner
within_session_compatibility = pass
balanced_order_effect = pass
stable_center = pass
warm_A_cross_source_anchor = pass
td_c_expansion_locked = true
```

采集后 analyzer 暴露旧 aperture provenance equality gate，已作为普通 harness defect
修复并由 24 个 direct-path tests 验证；保留的 8 帧未修改、未重采集。完整交接见
`.agent-work/ADVISOR_HANDOFF-20260812-GUIDE5-TD-C-CORE.md`。现在回 Advisor；不得进入
expansion 或 solver。

## 8. 后续锁与禁止事项

TD-C core 执行期间继续锁定：

```text
TD-C expansion
solver sentinel / remaining 9 / boundary / holdout / Gate-6 / P8
default/runtime LUT install
```

禁止：重复 Ray 3×3 fast acquisition、复杂 thermal/state-space correction、合并
fast/long 数据、平均 A0 与 warm returns、改变 observer/features/covariance/guard/
exposure/frame selection、把 R6 PC1 transfer failure写成 nonlinear interaction。

## 9. 执行与停止条件

- 普通代码/测试问题在当前 worktree 直接修复，不创建新的架构层或治理门槛。
- 每个实验使用独立外置 root；raw CR3/图像/measurement 不入 Git，manifest、hash、
  quality、analysis、cleanup 和报告可追踪。
- 设备任务超过 10 分钟使用 visible Terminal、三次 liveness 检查与 automation。
- strip history 的 Advisor gate 已由 `OPTION_3_CORRECT_THE_COMMON_CONTRAST`
  解除；analyzer-v3 exact 数值已复核，paired Ray bridge 已解锁。
- combined TD-B 已 canonical pass；TD-C core 已条件解锁；TD-C expansion、solver、
  sentinel 和 later stages仍保持锁定。

## 10. 交付要求

完成 TD-C core 后向 Advisor 提交：bridge-v2 分类、combined canonical artifact、
四 session 的 8/8 capture/quality/cleanup/hash、within-session/order/warm-anchor 结果，
以及 expansion/solver/later locks。
