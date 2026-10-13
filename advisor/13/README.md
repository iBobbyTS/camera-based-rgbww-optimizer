# RGBWW GUIDE13（2026-10-12）

本包包含GUIDE12原包及补包的独立审阅、逐点数值、GUIDE13科学路线、Agent实现提示和阶段结束交付要求。未操作相机/Ray/灯带，未修改任何历史采集数据；新增候选只作建议，不是已验证输出。

## 先读

- `13.GUIDE.md`：活动科学合同、实验/预算/停止条件、满幅阶段边界。
- `13.RESEARCH.md`：原报告与复算差异、源码证据、方法与局限。
- `REVIEW_TABLES.md`：70白光节点、N2区间、14彩光目标、主层恢复、LONG与环境的完整表。
- `AGENT_IMPLEMENTATION_PROMPT.md`：实现纠偏，不引入新治理层。
- `DATA_PACKAGE_REQUIREMENTS.md`：阶段结束必须提交什么及如何离线验收。
- `experiment_targets.json`：下一轮建议固定请求，需在模型/实拍前核查未作为已知留出用过。
- `data/`：机器可读复算结果；各项条件/CI/PI范围与来源身份。
- `replay/`：复核脚本，只读处理后输入。不是设备执行器。

## 核心结论

白光38/70是点估计分类，不是38个带预测保证的节点；实际超差数29而非19。白光运行时mired权重配反，70/70节点恒等失败。彩光10张全局near-noise候选的主白块有效，不能据secondary58失败宣称色域到顶。H300/S50切向算错，原H/S量尺未合格；彩光运行时错误钳制S0/高SAT。已有真实满幅、独立strip确认、三会话噪声设计和较好的若干直接色比匹配均保留，不从头重做。

白光工作进度约75%（规划70–80）；满幅彩光约60%（规划55–65），各8个主里程碑，剩余4/5工作包；不是通过率、色域覆盖、统计区间或后续Advisor轮数。详细规划权重见`progress_estimate.json`。

## 输入身份与复现

原包：`GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip`

SHA-256 `3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500`；37300305字节；1115个非自身成员。

增量：`GUIDE12-EVIDENCE-COMPLETION-20261012.zip`

SHA-256 `85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc`；15417622字节；4999个非自身成员。

分别解压为BASE与COMPLETION，不把一份覆盖另一份。Python依赖numpy、scipy；所需项目白点与纯运行时模块由COMPLETION/source/src提供。调用：

```bash
python COMPLETION/replay/validate_completion_package.py BASE COMPLETION
# 上一步的原作者数值相等阈值可能因跨平台最近点搜索触发N2数值差，先检查输出，不修改科学容差。
python replay/review_guide12.py BASE COMPLETION data
python replay/review_primary_gate.py BASE COMPLETION data
python replay/build_review_tables.py .
```

原作者报告10/10；本环境严格执行是9/10（N2约3.97e-6 K的数值等式差），其他范围核查通过。本审阅全部白点配对最大差≤0.0013 K、≤1e-5 mired，Duv约机器精度；显著小于科学容差，但不能称逐位相同。`data/review_integrity.json`完整保留这个区别。

本包中CI/PI的所有正态、独立、参考平稳、参数迁移假设均是条件，不是证明。单观测/单协议对比不伪造方差；H/S映射不合格时最大SAT及其CI为null并给下一实验路径，不填0%。

本包不包含原始CR3，也没有直接对其字节重新哈希；使用原包和本地Agent导出的哈希/统计链。无需重传已提供的基础输入。
