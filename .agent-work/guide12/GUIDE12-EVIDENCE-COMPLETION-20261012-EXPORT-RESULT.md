# GUIDE12 证据补齐导出结果（2026-10-12）

增量包：`.agent-work/guide12/GUIDE12-EVIDENCE-COMPLETION-20261012.zip`
- 字节数 `15417622`，成员 `4999`（不含 MANIFEST 自身），CRC/逐成员 SHA-256 校验通过
- ZIP SHA-256 `85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc`
- 原包引用：`GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip`
  （SHA-256 `3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500`，1115 成员）。
  增量包不覆盖、不替代原包；两者合并审阅。

## 实际补了什么

1. **批次1 全部 16 帧**（3 个根：formal-b1-20260929-r1 13 帧、white-reverse 1 帧、
   white-corrected 2 帧）：完整处理后统计（17 份新 measurements 成员，含 4 张
   all-off 环境帧、触顶/近噪拒绝帧、反向臂与修正臂）、原始 captures/commands/
   physical-returns/spec/quality/isolation/thermal 账本、sidecar、failure 与
   recovery-note、`b1-exposure-qualification-20260930.json` 与其分析器脚本。
2. **N2 出光诊断**：diag-ray-emission-20261003（4 帧，A/B/C/D 小 JSON 回执全含，
   RAW 载荷按哈希引用）、diag-ray-precheck-20261003b/20261004、w123/c122 两个
   precheck CR3 的哈希身份；另补 3 个原包未索引的 formal 失败根
   （formal-n2-hsi-ladder 0 帧 ValueError、-h240-r3 1 帧被拒且无 captures.jsonl、
   session1-r3 0 帧 KeyError）与 58 个 dry 计划根、154 份 launch 日志——
   RUN_INDEX_COMPLETE 共 221 项，全部标注 class/in_base/failure 真实状态。
3. **原始逐帧账本**：152 个原包根 + 上述新根的 runs/<campaign>/<root>/ 原字节
   文件（captures.jsonl 保留完整 plan_step/capture 对象，含 n2_state_key/
   n2_cycle_index/n2_burst_role、candidate_tag/candidate_role/probe 通道、
   timing_evidence、capture 前 ray_zero/strip_zero 隔离标志）；OBSERVATIONS_
   COMPLETE.jsonl 1068 行；两条只在原包 measurements 出现的缺失观测已按
   failure.json 恢复为 rejected 身份，未提升为 accepted；PAIRINGS.json 给出
   152 个运行中每条 strip 帧的相邻 Ray 帧配对与强度。
4. **RAW 身份链修复**：RAW_INDEX_COMPLETE.jsonl 1076 行——1068 条物理返回
   （acquisition 哈希 = 本次离线重算哈希 = 统计内 source.sha256，三源全等，
   零不可读）+ 8 条诊断/预检载荷（无物理账本，回执或哈希登记）。原包 1051
   份统计全部保留对应关系；新增 17 份（批次1 16 + h240-r3 1）。物理返回与
   统计零缺口。1076 个 RAW 全部离线重读，矩阵逐帧提取：唯一矩阵 1 个
   （matrices/mtx_*.json），每帧经 matrix_id 引用。
5. **源码闭合**：52 个包文件按包路径置于 source/src/camera_based_rgbww_optimizer/
   （white_calibration_common、bounded_least_squares、p7_thermal_diagnostics、
   measure_raw_observer_validation、control/measurement 层、全部 measure_guide12*
   入口与候选 JSON 读取实现；其中 8 个与原包平铺成员字节相同，已在
   DEPENDENCY_STATUS 标注 already_in_base_package）；冻结 config（含
   raw-observer.json）、pyproject、导出/校验脚本随包。
6. **派生分析输入**：w12/c122 等各 campaign derived 目录中与原包不同字节的
   191 个文件（候选-提案链、solver 证据、fullscale 投影、budget 账本、
   c122-next 提案、p6/predicted-raw-max 等）。

## 未做 / 不可恢复（真实终态，见 MISSING_OR_UNIDENTIFIABLE.json）

- 环境温度未记录（thermal-covariates 有 357 类协变量但 ambient_temperature_c
  全空；未用等待时间推算）。正式帧 ISO/光圈未入账本（仅诊断回执含 iso=100、
  aperture=implicit auto）。w123/c122 precheck 目录无 sidecar JSON。
- C12-2/3 会话内两点内插的按键级生成器未存档（original_generator_not_retained）：
  保留证据为 derived 候选/提案链、结果文档判定表与原包冻结公式
  （analyze_c12_2_block、analyze_c12_4 hue_basis）。
- 三个孤儿进程事故中删除的零捕获存根根：无数据损失，不重建假运行。
- 无 hash_mismatch、无 not_located_after_search、无 physical_return_without_
  patch_statistics。

## 最终计数

照片：1068 物理返回 + 8 诊断载荷 = **1076**，全部可读、重哈希、矩阵提取。
配对组：**152** 个运行（OBSERVATIONS_COMPLETE 1068 行 = 原包 1049 + 批次1 16
+ h240-r3 恢复 1 + 2 条被拒恢复）。运行根索引 **221**（formal 158 / diagnostic
5 / dry 58）。

## 离线 replay 范围与结果（replay/validate_completion_package.py）

在新临时目录解压原包+增量后运行，全程无 D: 盘路径、无设备。**10/10 PASS，
零 replay_discrepancy**：
1. 双包逐成员 SHA 校验（1115 + 4999）；
2. 统计对应与真实哈希去重（1051+17；三源哈希链全等）；
3. 13 个彩光采用命令追溯（选择帧与 confirm1-3 分离，13/13 满幅通道 4095）；
4. 499 条 formal Ray 帧全部 100% 强度、562 条 strip 帧隔离标志全覆盖；
5. W12-2 节点 3200/100 E 复算（用包内矩阵+源码，偏差 0.0）；
6. N2 white_1800_100 配对差+会话 CI（df=2, t=4.303）复算（偏差 0.0）；
7. W12-4 3200/100 FAST/LONG 差中之差复算（偏差 0.0）；
8. 6 组彩光采用样本直接 Δz 复算（n=4，全部在 ±0.004 内）；
9. W12-3 运行时插值向量与 C12-4 周期模型命令 vs 实拍命令（0 失配；10/10
   holdout 命令、13/13 采用命令在账本中实际执行）；
10. 批次1 曝光资格化 + all-off 环境敏感性复算（选定帧与 A/on 比率偏差 0.0；
    red 类无合格档，与原结论一致）。

详细输出：`GUIDE12-EVIDENCE-COMPLETION-20261012-VALIDATION.json`。

## 使用的导出/校验脚本

`tmp/scan_guide12_completion_raw_20261012.py`（RAW 哈希+矩阵扫描）、
`tmp/build_guide12_completion_package_20261012.py`（增量打包；原
`tmp/build_guide12_package_20261012.py` 保持原样保留，便于核对空 RAW 索引
与根遗漏成因：physical-returns 的 cr3_* 字段在顶层而非 capture 内、
CAMPAIGNS 未含 guide12-batch1、glob 仅 formal-* 且要求 captures.jsonl 存在）、
`tmp/validate_guide12_completion_20261012.py`（包内 replay/）。

本次为纯离线导出：无设备/相机/Ray/灯带操作，无新实验，未修改任何原结果。
