# Advisor Handoff — GUIDE6 H120/S100 Solver Retry

## Gate

`ADVISOR_GATE_REQUIRED`

GUIDE6 的 S-SOLVER-RETRY 分支已完成规定的离线 solver-coordinate review，并完成一次同科学合同的新 root repeat。两次 measurement-valid acquisition 均通过 Ray bracket、quality、cleanup 和 source isolation，但 target-local strip-versus-Ray contrast 均失败，因此不能继续进入 13-node grid、B pre/post、cross-experiment synthesis、solver sentinel 或 P8。

## 需要 Advisor 回答的科学问题

在保持 frozen observer、58 features、coverage、阈值、协方差、曝光和 H120/S100 协议不变的前提下，target-local strip candidate 相对同一 block Ray target 的重复失败应如何解释和处理？请明确下一条 GUIDE 分支：

1. 是否接受为有效的 target-local measurement negative；或
2. 是否允许一个新的、明确区分科学假设的实验；或
3. 是否需要修改科学 estimand/solver 坐标（不得由 Orchestrator 擅自修改）。

## 两次独立 root 结果

### Root 1 — S-REFERENCE 后的 repeat

`/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-075000-qualified-strip-1over1600-reference-repeat`

- acquisition：9/9 formal，0 ambient，retry=0
- quality：pass
- cleanup：pass；Ray intensity=0；strip 五通道=0
- Ray A before/after bracket：score `2.1121714859`，guard `9.5429188403`，pass
- target-local contrast：score `80.2851456563`，guard `9.4766596373`，fail
- classification：`guide6_s_solver_retry_required`

### Root 2 — S-SOLVER-RETRY repeat

`/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-080000-qualified-strip-1over1600-solver-repeat`

- acquisition：9/9 formal，0 ambient，retry=0
- quality：pass
- cleanup：pass；Ray intensity=0；strip 五通道=0
- Ray A before/after bracket：score `1.7267699100`，guard `9.5429188403`，pass
- target-local contrast：score `80.8620601083`，guard `9.4766596373`，fail
- classification：`guide6_s_solver_retry_required`

两次均为同一科学边界的实质性重复失败；不是代码异常、selector 错误、采集不完整或设备安全失败。

## 复核与实现边界

- 离线 review：`.agent-work/guide6-solver-coordinate-review-20260814.md`
- 分析器修复提交：`27163622dcdccc6e3293fa11872769d3fcbf7cad`
- review 记录提交：`ab1d30a8792097e8a325786bab1f5899b6c40593`
- GUIDE6：`advisor/6/6.GUIDE.md`
- 执行计划：`.agent-work/PLAN.md`、`.agent-work/PLAN-FULL.md`
- 分析器：`src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py`
- 行为测试：`tests/test_p7_direct_r6.py`

分析器未改变 observer、feature、threshold、covariance、frame selection 或 scientific protocol；旧 root 和本次 root 均保留在外置盘，未覆盖。

## 排除项

ZIP 不包含 CR3/RAW/DNG、TIFF/JPEG/PNG、NPY/NPZ、固件、build output、cache、credentials 或其他大载荷。原始数据仍保留在上述外置盘绝对路径；ZIP 仅包含派生 JSON/日志摘要及复核所需代码、测试和文档。

## 期望 Advisor 输出

请给出一个明确的科学 disposition 和下一步 protocol/analysis contract。除非明确批准新的科学边界，以下均保持 locked：13-node INT100、B pre/post、cross-experiment absolute synthesis、solver sentinel、P8。
