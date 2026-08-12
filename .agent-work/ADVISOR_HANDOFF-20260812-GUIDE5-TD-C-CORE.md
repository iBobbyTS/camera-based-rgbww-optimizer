# Advisor handoff — GUIDE5 TD-C core

## 请求

请复核已完成的 TD-C core 科学结果，并决定下一科学分支。当前明确保持
TD-C expansion、solver、sentinel 和 later stages 锁定；本交接不请求新采集授权。

## Acquisition identity

```text
root = /Volumes/4T/temp/rgbww-optimizer/guide5-td-c-core-20260812-151638-noambient-fix
experiment_id = p7_td_c_balanced_source_comparison_v1
acquisition git checkpoint = 7ba81b3e55f06f7e4427442b65e63fd8ea66849b
orders = Ray→strip / strip→Ray / Ray→strip / strip→Ray
per-source precondition = reset600 → D120 → A120 → capture
accepted formal = 8/8
physical CR3 = 8/8
ambient = 0
quality = pass
wrapper exit = 0
Python cleanup = pass
shell cleanup = pass
Ray final zero = pass
strip final zero = pass
```

Retained evidence hashes:

```text
analysis.json          a4f4303b391c6eca5bf4a59fd1e95bf1b505b28bad4eda1c081f5d54d98a6aa0
run.json               74423b19dbd0f6d7c0148bc24ddaa30b031767be6d05ad019b9bbeb97a8cfb3e
quality.json           727eacfa7897681d1c435ebd28e80f9137ad69fa060c2c64d2667666a8610a86
captures.jsonl         9354c116fdd37a2613b9d5adf597a30946688b84d4accd15e5c12d562f26651d
physical-returns.jsonl 6f819c723258a65ea128192fedff4dca6d11784115a4af47191495f0bf8e9080
```

## Direct analysis result

```text
schema = p7_thermal_diagnostic_analysis_v2
status = td_c_core_pass_waiting_for_planner
direct_artifact_validation = pass
capture_count = 8
comparison_design = order_balanced_paired_comparison_not_classic_abba
warm_precondition = reset600_then_D120_then_A120
within_session_compatibility = pass
balanced_order_effect = pass
stable_center = pass
warm_A_cross_source_anchor = pass
ambient_trend = not_required
current_stable_center_vs_p6 = locked_not_part_of_guide5_td_c_core
failure_branches = []
td_c_expansion_locked = true
```

## Analyzer recovery boundary

采集本身一次完成。首次 analyzer 调用在进入科学计算前被旧工程门禁拒绝：计划
aperture projection 为 `f/4`，远程 capture backend 在 run 与 8 个 frame 中统一报告
`implicit auto`。该问题分类为 `ENGINEERING_OR_HARNESS_FAILURE`，并未改变或否定
8 个 observation。

修复提交 `3304da6439b4746757f324302040565ae25cd902` 复用既有严格 reconciliation：
只接受 planned `f/4` 对 runtime `implicit auto`，并继续要求 owner、ISO、RAW 和每帧
capture settings 完全一致。direct-path test module `24/24` pass。随后从同一 retained
root 生成上述 analysis；没有重采集、池化、改变 observer/features/covariance/guard/
exposure/frame selection 或进入后续阶段。

## Scientific delta and exact Advisor question

```text
science_delta = accepted_valid_td_c_core
gate = ADVISOR_GATE_REQUIRED
question = Given the passing order-balanced TD-C core under the frozen fast envelope,
           what is the next scientifically permitted branch, while expansion, solver,
           sentinel and later stages remain locked until this review?
```
