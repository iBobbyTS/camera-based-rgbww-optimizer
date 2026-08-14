# GUIDE6 S-SOLVER-RETRY 离线坐标复核

日期：2026-08-14

## 输入

- Root：`/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-075000-qualified-strip-1over1600-reference-repeat`
- 分析：`analysis.json`
- 协议：`GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-V1`
- 合同：600 s reset proxy、D120、A120、Q120、1/1600 strip shutter、9 formal、0 ambient、retry=0

## 结果

- 9/9 acquisition、quality、cleanup、source isolation 均通过。
- Ray A before/after bracket：pass，score `2.1121714859`，guard `9.5429188403`。
- target-local strip-vs-Ray contrast：fail，score `80.2851456563`，guard `9.4766596373`。
- 结论：measurement valid，但 solver coordinate 未通过；没有证据表明失败来自 Ray reference、曝光 envelope、设备安全或采集不完整。

## 复核边界

本次只复核冻结的 target-local 坐标及其既有 guarded contrast。没有修改 observer、feature、threshold、covariance、frame selection、曝光或协议，也没有把失败重分类为科学 negative。下一步是一次完全相同科学合同的新 root；若再次出现同一 solver failure，才进入 `ADVISOR_GATE_REQUIRED`。
