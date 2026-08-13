# PLAN — GUIDE5 TD-C exact-context decomposition v3 (offline)

## 当前目标

按 Advisor 最新决定，只完成离线 v3 分解；不得启动任何设备采集。

- endpoint、TD-C core、Ray/strip FAST history 是唯一允许输入；R6 输入数必须为 0。
- 旧 v2 residual-minus-anchor 结果不再用于科学门禁。
- 从 primitive source observations 生成 exact D→A→B cross-source pre/post 对比，
  序列化 observation coefficients、shared-observation cancellation、source-level
  Monte Carlo guard 与 identity error。
- v3 未通过结构和证据检查前，`GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1` 保持锁定。

当前离线 artifact：

```text
/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328/analysis-v3-exact-context-anchor-decomposition-v1.json
schema = guide5_td_c_fast_endpoint_exact_context_decomposition_v3
classification = partially_valid_not_gate_complete
r6_input_count = 0
```

v3 本轮结果显示 B pre/post synthesis residual 与 B-minus-C residual 均为
`fail`，B anchor-direction contrast 为 `pass`；这只是当前冻结数据上的离线
分解结果，不等于 B physical endpoint bias，也不解锁实拍。`identity_error` 仅作
代数一致性诊断，不替代 Advisor 的科学解释。

## 历史路线目标

1. 保持 TD-C core 原 `analysis.json` 不变，生成 source-specific covariance 的
   `analysis-v2.1-td-c-core-contrasts-derived.json`。
2. 只有 derived artifact 精确复现 Advisor 指定的四类 pass 和预期非零 A offset 后，
   才建立并执行 `GUIDE5_TD_C_FAST_ENDPOINT_HOLDOUT_B_C_V1`。
3. endpoint holdout 完成后回 Advisor；solver、sentinel 和 later stages全程锁定。

## 离线纠偏

- Ray pair covariance：`2*Sigma_R`。
- strip A pair covariance：`2*Sigma_S_A`。
- paired offset pair covariance：`2*(Sigma_R+Sigma_S_A)`。
- 两种 order 各 2 session 的 mean contrast covariance：`Sigma_R+Sigma_S_A`。
- absolute A offset covariance：`(Sigma_R+Sigma_S_A)/4`，zero compatibility 仅诊断。
- limit 由 source-level unit observation Monte Carlo 生成；禁止把 difference vector
  传给 unit-observation helper。
- 原 observer、58 features、variance、coverage、frame 和 exposure 不变。

## Endpoint holdout

```text
sessions = B Ray→strip / C strip→Ray / B strip→Ray / C Ray→strip
per source = reset600 → D120 → A120 → Q120 → capture Q → off
formal / physical / ambient = 8 / 8 / 0
retry = 0
steady claim = false
```

Gate 仅为 state-specific paired-offset repeatability，以及新 B/C absolute offset 对
`core_A_absolute_offset + combined_local_state_coordinate` 的独立 holdout agreement。
pre-solver strip-Ray offset 不与零做 pass/fail gate。

## 停止边界

- corrected core 若不能复现 Advisor 指定结构：`ADVISOR_GATE_REQUIRED`。
- endpoint acquisition 或 analysis 完成：打包 derived 数据、代码与文档，
  `ADVISOR_GATE_REQUIRED`。
- 不运行 legacy 1800 s / t_formal expansion，不运行 solver/sentinel/later stages。
