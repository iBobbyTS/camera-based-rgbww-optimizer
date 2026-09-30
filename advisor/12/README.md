# RGBWW GUIDE12 交付包

日期：2026-09-29。主题：审阅GUIDE11，推进Ray100%与灯带实际max PWM4095的相机光色复制。

## 文件入口

- `12.GUIDE.md`：科学实验、判定、有限预算、停止条件、满幅约束与阶段结束交付要求。
- `12.RESEARCH.md`：附件结果审阅、错误/限制的证据位置、统计方法与外部参考。
- `REVIEW_TABLES.md`：70白节点、9采用命令、20插值点、N1区间、4个LONG对照、8彩色确认与Ray自反解数值。
- `CODEX_GUIDE12_IMPLEMENTATION_PROMPT.md`：最小实现纠偏，不另建工程治理框架。
- `GUIDE12_DATA_PACKAGE_REQUIREMENTS.md`：阶段结束一次性完整处理后证据包合同。
- `data/review_recomputed.json`：主复算输出，全精度数值和物理身份。
- `data/white_results.json`、`uncertainty_results.json`、`color_results.json`：按主题拆分的相同结果。
- `data/uncertainty_and_actions.json`：可实验解决、历史不可恢复、当前设计不可分离和目标外范围的逐项处置。
- `data/hue_coverage_status.json`：六个主Hue的当前覆盖资格与直接误差；未建立不写0%。
- `reproduce_review.py`：直接从完整GUIDE11 ZIP或解压目录重算；需要numpy/scipy及包内source快照，无设备/网络/RAW解码。

## 复算

```bash
python reproduce_review.py \
  --evidence GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip \
  --out replayed-review.json
```

在本次环境，目录输入与ZIP输入的主JSON逐值完全一致。报告对原生RAW小型统计的审阅不等于重新解码了原始CR3；RAW哈希与原文件一致性采用导出器记录，Advisor独立检查的是ZIP/成员哈希和数值推导。

## 读数规则

误差为strip−Ray，GM沿用raw-GM（100为中性），K/mired/Duv是本项目相机代理坐标。色比百分比不是饱和度覆盖率。小样本条件CI/PI不是对任何环境的无条件保证。70点混合账面43/70不是新的70节点独立认证。规划完成度白光约70%、彩光约50%也不是颜色精度或统计CI。

## 核心决定

既有数据已经足以进行正式审阅，不再索要补包。保留有效观测，纠正单位、差分、原生RAW平台输入、SAT0与逆映射、实际满幅、独立确认和时序解释。GUIDE12不启动低INT阶段，也不宣称硬件物理最优。
