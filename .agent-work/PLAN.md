# PLAN — GUIDE5 TD-C corrected contrasts and FAST B/C endpoint holdout

## 目标

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
