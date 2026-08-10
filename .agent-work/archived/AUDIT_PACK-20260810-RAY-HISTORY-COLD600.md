# AUDIT PACK — GUIDE 4 Ray history COLD600 V3

日期：2026-08-10  
用途：提交 Advisor 审阅，不授权任何后续设备实验。

## 结论摘要

三 session 的 cyclic order-balanced Ray-only identification 已完整完成：每个
session 7/7，合计 21/21。所有质量、physical ledger、Python/shell cleanup、
wrapper exit 和最终 Ray/strip zero 检查通过。冻结 direct analyzer 只运行一次，
输出：

```text
status = classified_waiting_advisor_review
classification = nonlinear/non-additive
period_detected = false
C_carryover_detected = false
other_state_effect_detected = false
large_orthogonal_residual = true
additive_model_rejected = false
all_return_deltas_compatible_with_zero = false
r6_frames_pooled = false
```

这表示返回锚点差异不能由预冻结的
`session + sequence_position + immediate_predecessor_state` 加性模型完整解释，
但没有证明周期效应、C 特异 carryover 或任何单一因果来源。R6 仍是有效科学负结果，
没有被重分类或混入本次拟合。当前 gate 为 `ADVISOR_GATE_REQUIRED`；strip、combined
TD-B、TD-C、sentinel 及后续阶段全部保持锁定。

## 权威输入

- `advisor/4/4.GUIDE.md`
- `advisor/4/R6_REVISION.md`
- `.agent-work/PLAN-FULL.md`
- `.agent-work/evidence/R6_VECTOR_REANALYSIS-20260809.json`
- `.agent-work/ADVISOR_HANDOFF-20260810-RAY-HISTORY-COLD600.md`

R6 vector artifact SHA-256：

```text
artifact = 68df8420dbdeabe19eb314d212e63404c0a1f67a141863c6357756b0aa301918
direction = bb707f600272968af656ba890535ebb161e0f45209249adde1aa72cdf3dfba57
```

## 实验身份与执行合同

```text
experiment_id = GUIDE4-RAY-HISTORY-ORDER-BALANCED-3X3-OP120-COLD600-V3
root = /Volumes/4T/temp/rgbww-optimizer/guide4-ray-history-3x3-op120-cold600-v3-20260810-081551
orders = session 1: D→B→C; session 2: C→D→B; session 3: B→C→D
captures = A0, Q1/A_after_Q1, Q2/A_after_Q2, Q3/A_after_Q3
formal captures = 7 per session, 21 total
operational dwell = 120 s
between-session cold proxy = 600 s
Ray intensity = 100%
strip = zero throughout
retry = 0
```

120 s dwell 与 600 s cold proxy 均为 Human 为节省时间和用电作出的明确决定，并
接受额外热误差；不作 settled/steady-state 声明。

## Session 汇总

| session | order | captures | quality | cleanup | cold proxy | quality SHA-256 |
|---:|---|---:|---|---|---:|---|
| 1 | D→B→C | 7/7 | pass | Python pass + shell 0 | 600 s | `3615cae8a4e79230ced28be4a36258960d497baf7bcd9df484dcb82cf283385b` |
| 2 | C→D→B | 7/7 | pass | Python pass + shell 0 | 600 s | `bbe77f48d2305a94b79059e532263c0549992b3e7fa10448f6617c4781138f1e` |
| 3 | B→C→D | 7/7 | pass | Python pass + shell 0 | 600 s | `3aae4e608269f9a3c125a904843828363b871119276627709ee2e972e0a2c3c1` |

每个 session 的 `run.json` 为 complete/cleanup pass，`wrapper-result.json` 为
complete/exit 0，captures 与 physical-returns 均为 7 行。外置根中的 camera/、
measurements/ 原始及派生大文件未纳入本包；本包只带小型可审计记录。

## 分析方法与结果

分析使用冻结的 observer、58 features、common whitening、uncertainty、guarded
coverage 和下式：

```text
return_anchor_delta = session + sequence_position + immediate_predecessor_state + residual
```

R6 只作为预冻结 drift direction 投影输入，`r6_frames_pooled=false`。所有冻结
period/carryover contrasts 的 guarded decision 均为 `compatible_with_zero`；但
orthogonal residual 被标记为 large，故选择 `nonlinear/non-additive` 分支。该分支
只说明当前加性 screening 不足以解释数据，不指定新的模型，也不允许事后改阈值、
协方差、曝光或 frame selection。

完整 analyzer 输出在包内 `analysis/analysis.json`，其 SHA-256 为：

```text
0628736473668cceee9657f3a6770663e53728a3bb4ce10a871770bbf6c9136b
```

## 安全与复现状态

- 独立 post-run all-off：ESPHome 五通道均为 0，Ray intensity 为 0。
- 无 firmware flash、remote deployment、strip 输出或后续 stage 操作。
- acquisition Git checkpoint：`afa4318`，run metadata `dirty=false`。
- 仓库当前提交记录包含本 pack 的报告与 Advisor handoff；原始 payload 仍在外置
  根，未进入 Git 或 ZIP。

## 请 Advisor 回答

1. `nonlinear/non-additive` 是否足以作为科学分类接受？
2. 在不把它误写为 C-carryover 的前提下，下一项最小辨识实验是什么？
3. 是否允许解锁 strip/combined TD-B，还是继续维持现有锁？
4. 是否需要增加观测或修改科学模型；若需要，请明确不可变更的 observer、58
   features、uncertainty、coverage、exposure 与 frame-selection 约束。

Advisor 审阅完成前，Orchestrator 不继续设备采集或后续 GUIDE 阶段。
