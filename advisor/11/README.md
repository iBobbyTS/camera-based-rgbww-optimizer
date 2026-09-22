# RGBWW GUIDE10分析 / GUIDE11执行资料

先读11.RESEARCH.md看结论与证据，再读11.GUIDE.md决定实验；代码实现任务用CODEX_GUIDE11_IMPLEMENTATION_PROMPT.md。GUIDE只规定科学内容。

## 文件

- 11.GUIDE.md：新的科学路线、误差/置信度、有限采集与停止条件。
- 11.RESEARCH.md：GUIDE10审阅、主要数值、因果限制与外部方法来源。
- CODEX_GUIDE11_IMPLEMENTATION_PROMPT.md：最小实现纠偏，不重建工程治理框架。
- WHITE_POINTS.md：96组白光比较的易读表（70节点+20非节点+6追加FAST）。
- GUIDE10_AUDIT.json：输入哈希、证据定位、主要发现与结果摘要。
- white_per_point_results.json：逐点误差、命令、条件95%区间与源观测ID。
- noise_and_model_diagnostics.json：P1每组n=5的SD/CI/条件PI、P2/P3模型诊断。
- hsi_projection_diagnostics.json：历史58维流形的最近点诊断，不是最终SAT覆盖；SAT0不定义Hue。
- analysis_utils.py、analyze_white.py、analyze_noise.py、analyze_hsi.py、build_report.py：只读复算脚本。

## 口径

真GUIDE10 LONG节点为0；旧“LONG”12帧是600/120 FAST。白光36/70只表示固定网格点估计通过。彩光剩余八主节点未执行。不存在“未测=0%覆盖”或“条件投影区间=真实色域置信区间”的转换。

进度白光65%（规划范围60–70%），彩光45%（40–50%）；不是统计CI或色彩准确率。彩光2°/2SAT、SAT0 log色比0.01是GUIDE11提出的产品工程容差，不是人眼JND或既有测量结论。旧58维strict结果保留。

## 复算

Python 3 + NumPy + SciPy。将base/supp/delta/src四个解压目录放在共同工作目录，在脚本中修改B路径（默认/mnt/data/audit_work）；analyze_hsi.py的sys.path也需指向src/src。输入为本轮用户已经提供的四个ZIP。本包不再重复包含大型原始证据。

建议顺序：analyze_white.py → analyze_noise.py → analyze_hsi.py → build_report.py。单线程BLAS可减小大量小矩阵的线程开销。脚本不运行设备控制。WHITE_POINTS.md为本次冻结结果的阅读版。

MANIFEST.json绑定本包其余文件的大小与SHA-256；不包括manifest自身。历史源数据不被修改。
