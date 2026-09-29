# GUIDE11 完整处理后证据包导出结果（2026-09-29）

按 `GUIDE11_REVIEW_INPUT_REQUEST_20260929`（GUIDE11_EVIDENCE_EXPORT_PROMPT.md）
完成的纯离线补齐导出。未运行任何新实验、未触碰设备/相机/Ray/灯带、未修改任何历史
科学结果；所有导出来自既有文件与既有 RAW 的只读数值提取。

## 交付物

- ZIP：`.agent-work/guide11/GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip`
- 字节数：19,570,627
- SHA-256：`5c348c023027e96b149edf41b4654d26b2dfc26e868add29f3b5e8243f9d5e65`
- 成员数：1730（含 MANIFEST.json 自身；manifest 按约定不含自引用哈希）
- 外部校验记录：`tmp/GUIDE11-EVIDENCE-EXPORT-VALIDATION-20260929.json`（overall=pass）
- 打包/校验脚本：`tmp/export_guide11_evidence_stage1_copy_20260929.py`、
  `tmp/export_guide11_evidence_stage2_raw_20260929.py`、
  `tmp/export_guide11_evidence_stage3_index_20260929.py`、
  `tmp/validate_guide11_evidence_export_20260929.py`
- 解包 staging（保留供复核）：`D:/rgbww-optimizer/tmp/guide11-evidence-export-20260929/stage/`

## 计数对账

- 导出运行根 51（formal 28、diagnostic 5、dry 12、guide9 依赖 6），另有组级 launch 日志与
  恢复前检查文件。
- 物理照片：472 张（按重算 RAW SHA-256 去重），逻辑观测行 472，root+capture_id 复合键
  无碰撞、无跨根内容重复；ray 行 240、strip 行 232。
- 哈希核对：472/472 与采集时账本记录一致（0 失配）；全部 CR3 共享同一 rawpy
  rgb_xyz_matrix（矩阵按内容去重为 1 个，帧经 matrix_id 引用）。
- patch-statistics：30 个含 captures 根全量保留（含 rejected/质量字段/全部 24 色块），
  19 行无统计（诊断根在特征提取前失败，physical-returns 仍证明拍过照）。
- strip 命令满幅账本：216 行（requested_payload + apply 后 device_snapshot + readback），
  其中 136 行实际 PWM 达 4095；历史非满幅/低 INT 行原样保留。

## 关键事实（详见包内 replay/）

- W2 新鲜 Ray：49 行全部导出 primitive+白点；25 个选择节点中恰好 9 条命令按命令匹配进
  冻结 LUT（= 声明的 nodes_updated_from_w2=9）；该 9 条命令的独立 FAST 确认在 30 根
  438 条命令行范围内逐条 `not_acquired`。两种误差口径（vs 同块新鲜 Ray / vs W1 历史
  Ray）分开列出，原选择结果未改。
- C3 SAT0 行：18 次 N1 白光 Ray 聚合，复算 z_spread=1.5471225257714007 与冻结值逐位
  一致；真 Ray HSI H0/S0/INT100 观测单独导出（与 C3 SAT0 锚距离 0.430），未回灌冻结锚。
- C3 生成器输入可用性：h120-s25 与 h300-s100 两根在本机无 captures/measurements
  （h120-s25 完整数据在旧 guide10 补充包内），冻结 C3 网格相应没有 h120/s25、h300/s100
  单元——如实记录，未补造。
- W4 实际时序：FAST 复位 600s/驻留 120s→观测曝光时刻 124.7–125.8s；LONG 复位
  1800s/驻留 600s→观测 604.6–605.9s；FAST 全部先于 LONG（首命令 UTC 08:53 vs
  10:52）。替代了脚本内硬编码文字。
- 环境光：GUIDE11 根内无 ambient/dark 拍摄（`not_acquired`）；温度/照度协变量全为
  null（`not_recorded`）；未用 Ray 单通道变化推断灯带环境贡献。
- 旧包“声称存在却缺失”的 `GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json`：本地在
  （构建脚本生成于 zip 旁但当时未压入 zip），zip_sha256 与交付 zip 一致，已按
  exported_existing 收入新包并注明该事实。
- replay：1 白光（W2 选择帧 block_06 + 导出矩阵 → CCT/Duv/mired）与 1 彩光（C4 目标
  planes → z → 配对 Ray 残差）仅用包内数值复算，与冻结 derived 差值全部为 0.0；帧曝光
  画像与 derived 存储的分类/饱和比交叉核对一致。

## 未做 / 不可恢复短表

- 9 条 W2 采纳命令的独立 FAST 确认：未做（not_acquired，附全范围搜索证据）。
- GUIDE11 期间环境光/all-off/dark 照片：未拍（not_acquired）。
- 环境温度/照度记录：未记录（not_recorded）。
- h120-s25、h300-s100 的 G9 原始根数据：本机不可用（前者在旧补充包内可解析，
  available_in_prior_package；后者仅 cleanup 文件）。
- 未生成任何 GUIDE12 内容；未修改颜色/曝光/统计门；未为导出补拍任何照片。
