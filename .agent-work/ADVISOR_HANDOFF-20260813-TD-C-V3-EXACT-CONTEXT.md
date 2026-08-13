# Advisor Handoff — GUIDE5 TD-C exact-context decomposition v3

## 当前请求

请审阅 `guide5_td_c_fast_endpoint_exact_context_decomposition_v3`，并决定是否
可以将 `GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1` 提交 Human 进行执行授权，或应
保持 B 采集锁定并改写科学路线。

本轮没有设备访问、没有新采集、没有修改任何既有 parent artifact。

## 科学背景与约束

Advisor 最新决定将此前 decomposition 标记为
`PARTIALLY_VALID_NOT_GATE_COMPLETE`：不能把 residual 解释为 B/C physical
endpoint bias；Ray-only R6 anchor 及其 `2Σ_R` covariance 不得继续用于该判断。
本轮改用 FAST、cross-source、exact `D→A→B` context，并从 primitive source
observations 做 Monte Carlo。C validation、solver、sentinel 和 later stages
保持锁定。

## v3 输入与输出

唯一输入：

- 接受的 8-observation TD-C endpoint root；
- immutable TD-C core corrected analysis；
- immutable Ray/strip FAST history and combined coordinate artifacts。

输出：

`/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328/analysis-v3-exact-context-anchor-decomposition-v1.json`

属性：

- schema：`guide5_td_c_fast_endpoint_exact_context_decomposition_v3`
- status：`offline_derived_no_parent_refit`
- classification：`partially_valid_not_gate_complete`
- `r6_input_count = 0`
- old v2 artifact remains unchanged and is not used as a gate.

## 结果

| contrast | score | guarded limit | decision |
|---|---:|---:|---|
| B exact pre synthesis residual | 1681.9585012901 | 9.6022729131 | fail |
| B exact post synthesis residual | 1680.5654109127 | 9.5625860610 | fail |
| B anchor direction | 2.8927944105 | 9.5618317255 | pass/compatible |
| B-minus-C synthesis residual | 21.5722311246 | 9.5104544589 | fail |

`identity_error = 0.0008349557`，即 `e_post - e_pre - h_B` 的数值残差，来自
浮点归一化；primitive coefficient cancellation 已序列化。每个 contrast 都
包含 observation identity、coefficient、source-level Monte Carlo seed/sample
count/coverage，并标记 `difference_center_used=false`。

这些结果不证明 B physical bias、C-specific bias 或 anchor direction；它们只表明
当前 exact-context synthesis transfer 仍未通过，且 B anchor-direction contrast
本身没有被检测到。

## 请 Advisor 明确回答

1. v3 的 exact-context estimand、共享 observation cancellation 和 Monte Carlo
   结果是否足以把当前路线分类为 `B_local_coordinate_transfer_unresolved`？
2. 在 pre/post synthesis residual 均 fail 且 anchor-direction compatible 的
   情况下，是否仍允许执行 B pre/post 12-observation experiment，还是应停止并
   重新定义不依赖 synthesis transfer 的实验？
3. 如果允许，正式实验名称应采用中性的
   `GUIDE5_TD_C_FAST_B_PREPOST_TRANSFER_V1`，还是保留
   `GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1`？

仓库内的安全代码修复不能回答这些问题，因为它们是实验 estimand、科学解释和
后续分支选择，而不是实现错误。

## 证据范围

ZIP 不包含 CR3/RAW/DNG、TIFF/JPEG/PNG、NPY/NPZ、decoded arrays、firmware、
build/cache、credentials 或其他大载荷；原始载荷仍保留在外置盘原路径中。
