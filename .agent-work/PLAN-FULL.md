# PLAN-FULL — GUIDE 5 science-first route

**性质：** Git 可追踪的科学路线记录；仅供 Human、Advisor 与 agent 阅读，不是
production/test 输入、runtime 状态机、设备授权或 hidden gate。

**科学权威：** `advisor/5/5.GUIDE.md` 与 `advisor/5/5.RESEARCH.md`（本轮 Advisor
文件 SHA-256 已由提交记录验证）。

**上游完成状态：** GUIDE 4 Ray COLD600 V3 已被接受为有效科学证据；原报告中的
`nonlinear/non-additive` 已由 Advisor 明确拒绝为过强分类，原始
`analysis.json` 保持不可变。

**当前路线状态：** `READY_FOR_NEXT_SCIENTIFIC_ACTION`

**当前下一步：** 从以下两个已冻结的有界设备实验中选择一个执行；依据 AGENTS.md
的 Human-authorization precedence，二者均不需要额外 Human authorization：

1. `GUIDE5-STRIP-HISTORY-ORDER-BALANCED-3X3-OP120-RESET600-V1`
2. `GUIDE5-RAY-FAST-LONG-BRIDGE-OP120-OP600-RESET600-RESET1800-V1`

两者不得并行，必须使用独立 root；Orchestrator 可直接按当前 GUIDE/PLAN 的边界执行。

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

## 4. B — strip-only fast history（已解锁）

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
和 cleanup 全部通过。冻结 analyzer-v2 输出
`underpowered_or_unclassified`：所有 additive contrast 均 compatible with zero，
但 raw return deltas 不 compatible with zero；该分类不在 GUIDE5 S-A 至 S-E
枚举中。当前为 `ADVISOR_GATE_REQUIRED`，精确证据与问题见
`.agent-work/ADVISOR_HANDOFF-20260810-GUIDE5-STRIP-HISTORY.md`。在 Advisor
分类前，不执行 paired Ray bridge、combined TD-B、TD-C、sentinel 或 later stage。

## 5. C — paired fast-vs-long Ray bridge（已解锁）

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

## 6. 后续锁与禁止事项

在 B、C 均完成并向 Advisor 回报前继续锁定：

```text
combined TD-B
TD-C
solver sentinel / remaining 9 / boundary / holdout / Gate-6 / P8
default/runtime LUT install
```

禁止：重复 Ray 3×3 fast acquisition、复杂 thermal/state-space correction、合并
fast/long 数据、平均 A0 与 warm returns、改变 observer/features/covariance/guard/
exposure/frame selection、把 R6 PC1 transfer failure写成 nonlinear interaction。

## 7. 执行与停止条件

- 普通代码/测试问题在当前 worktree 直接修复，不创建新的架构层或治理门槛。
- 每个实验使用独立外置 root；raw CR3/图像/measurement 不入 Git，manifest、hash、
  quality、analysis、cleanup 和报告可追踪。
- 设备任务超过 10 分钟使用 visible Terminal、三次 liveness 检查与 automation。
- 只有明确的 `HUMAN_GATE_REQUIRED` 或 `ADVISOR_GATE_REQUIRED` 才停止路线；当前
  没有任一 gate。高危操作授权缺失时才进入 `HUMAN_GATE_REQUIRED`。

## 8. 交付要求

完成 B/C 后向 Advisor 提交：v2 分类、fast target 路径/hash、strip 分类、bridge
分类、所有 root/quality/cleanup/hash，以及 combined/TD-C/later locks。Advisor 决定
后续 combined comparison 的 exact warm-precondition protocol。
