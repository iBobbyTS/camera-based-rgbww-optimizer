# Stage 6 P7-R1 本轮审计包

## 目的

这是 2026-07-19 提交给 Advisor 的新一轮材料。上一轮 Advisor 基线和 GUIDE 保留在
`advisor/2/0.AUDIT/` 与 `advisor/2/1.GUIDE.md`，本目录不覆盖上一轮文件。

本轮补充已完成的 P0-R 至 P7-R1 工作、实际方法、证据质量和当前阻塞原因。文档整理与复核期间
没有调用相机、Ray120c、ESPHome、`.env` 或 `all_off`。

## 文件导航

1. [01-p7-r1-completed-method-and-quality.md](01-p7-r1-completed-method-and-quality.md)：按 GUIDE 汇总阶段完成映射、P7-R1 方法、证据、质量分级和决策问题。
2. [02-advisor-decision-request.md](02-advisor-decision-request.md)：给 Advisor 的最小决策请求和禁止事项。

## 当前结论

| 项目 | 结论 | 状态 |
| --- | --- | --- |
| P0-R 至 P6 | 作为冻结输入继续有效 | 不需要整体返工 |
| P7 离线实现 | runner、evaluator、analyzer、evidence contract 和双 cleanup 已完成 | 离线通过 |
| P7-D0 | generation/readback 低输出 preflight 通过 | 已验收 |
| P7-R1 acquisition | `82 logical / 80 formal / 105 physical CR3`，selected CR3 全部非空 | 通过 |
| P7-R1 numerical gate | `uncertainty_unresolved` + `R-REFERENCE-UNSTABLE` | 阻塞 |
| Candidate | `formal_capture_eligible=false` | 不得安装/进入产品 |
| Sentinel、remaining 9、boundary、holdout、P8 | 继续锁定 | 等待新 GUIDE |

## 质量判断

本轮不是无效采集：CR3、曝光、source isolation、readback、ownership、budget ledger、Python
cleanup、shell cleanup 和 wrapper exit 均有证据。失败发生在冻结的 repeatability/reference
stability gate，不能通过删首帧、修改 threshold/covariance/guard 或改变 58-feature 来消除。

