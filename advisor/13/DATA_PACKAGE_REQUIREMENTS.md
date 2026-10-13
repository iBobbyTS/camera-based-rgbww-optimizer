# GUIDE13 阶段结束证据包合同

本文件与13.GUIDE.md同时生效。目标是让Advisor在没有用户D盘、设备、原始CR3载荷的环境中复核每个结论；不是再建立多层发布治理。

## 1. 交付形态与输入关闭

提交一个完整处理后ZIP及两个外部文件：

- `GUIDE13-COMPLETE-PROCESSED-EVIDENCE-<date>.zip`
- `...-MANIFEST.json`：ZIP大小、SHA-256、非自身成员计数。
- `...-VALIDATION.json`：离线重放结果与真实失败项，不硬写PASS。

可以依赖本次已经提供的两个GUIDE12包，必须在`BASE_PACKAGES.json`中绑定精确SHA与成员路径。不重复复制相同字节；新增或变化的依赖入包。解包后不访问D:、/Volumes、网络或设备。

ZIP内`MANIFEST.json`枚举全部非自身成员的相对路径、字节数、SHA；排除自身自引用。CRC和成员哈希分别检查。不得因为文件名含raw、bulk、patch-statistics而排除处理后统计。

历史文件只读。任何回溯重分析写新derived并标`reanalysis`，不能改原quality、命令、时间或结论。未做/未记录/丢失/旧包已存在各有独立状态，不把它们都写成`missing=[]`。

## 2. 必须包含的内容

| 路径/文件 | 必需信息 |
|---|---|
| `README.md`, `FINAL_REPORT.md` | 原目标、当前满幅/协议范围、决定、进度；报告所有数值来自同一最终机器表 |
| `RUN_INDEX.json` | 全部formal、diagnostic、dry、失败、恢复、零捕获根；不要依赖有captures才扫描 |
| `runs/<id>/` | 原字节spec、run、captures、commands、physical-returns、quality、isolation、thermal/time、failure/recovery、cleanup、launch log及相应config快照 |
| `OBSERVATIONS.jsonl` | 每个物理返回一行；根ID+capture ID、physical hash、真实角色、全部plan_step/采集对象、质量、统计/矩阵路径 |
| `RAW_INDEX.jsonl` | 采集账本哈希、本次离线重哈希、byte_count、保留原路径/当前路径、sidecar、matrix_id；不上传CR3载荷也不可全部null |
| `measurements/` | 所有照片的24色块×R/G1/G2/B完整统计，含失败/被拒/环境；没产生统计的物理返回单独说明原原因 |
| `raw-small/`, `matrices/` | 原生black/white level、尺寸/CFA描述、实际MakerNote曝光、所用rgb_xyz_matrix、ROI/observer身份、参数/版本；每帧引用矩阵 |
| `PRIMARY_SECONDARY_QUALITY.jsonl` | 主block_06、secondary58、曝光、参考、隔离、满幅各自资格及原因，不能只留总布尔值 |
| `PAIRINGS.json` | 每个strip与确切Ray before/after、权重、共享组、单独参考/邻近参考区分，不能按文件名猜 |
| `COMMAND_IDENTITY.jsonl` | 请求、转换前后、实际PWM apply/readback、满幅通道、code-duty变换顺序、控制侧版本、是否已实际拍摄 |
| `SEARCH_LEDGER.json` | 每目标历史/本轮唯一命令、候选角色、实际face、有效方向、预算、预测/实测改善、停止理由；同命令跨root不能重复计unique |
| `source/` | 实际执行的模块、脚本、被导入小依赖、候选生成器/局部线性计算，不只最后analyzer；记录commit与dirty为证据，不作运行授权 |
| `models/` | 白光最终PWM LUT、实际运行时函数与参数、Ray前向/逆向、各局部J/协方差/适用域、实际彩光函数与S0/高SAT/压缩端点 |
| `results/` | 全部候选、确认、留出、环境、时间、误差、噪声分量、CI/PI、失败区；不能只有norm/通过数 |
| `replay/` | 完整离线重放脚本，依赖版本、输入路径、种子、数值容差、输出；包括最小科学反例测试 |
| `DEPENDENCIES.json` | 每个最终数字/模型的直接父输入与生成器；丢失的按键级生成器如实标记，不让临时新脚本冒充历史生成器 |
| `MISSING_OR_UNIDENTIFIABLE.json` | 每项对应已查范围、状态、影响、当前可报告量及不可外推内容；无必要重复索要历史温度 |

包内不得包含.env、凭据、token、SSH key、浏览器会话或无关用户文件。不要把设备控制权限、后台自动运行脚本当重放依赖。

## 3. 数值和统计最小字段

每个白光节点/非节点：用户CCT/GM与raw编码、实际命令、Ray/strip各自白点、signed K/mired/Duv、各自容差、E、n及独立单位、每组差向量、均值/SD/min/max、均值CI、未来PI、联合判定、参考漂移、模型迁移依据。

每个彩光目标：请求H/S、实际PWM、源级z、确认Δz、完整2×2协方差、实际H/S及多解集合、局部J完整矩阵/奇异值/每列来源、映射误差、联合H/S区间、ΔH/ΔS、secondary58诊断、停止理由。未合格映射下H/S为null并说明直接z已测、何种未来判别已做；不得用旧长割线填数。

每个Hue：`validated_samples`逐条唯一ID、`s_best_tested`及区间/命令/适用范围、`search_upper_request`、连续区间及其独立支持、压缩策略。样本数、观测数、参数坐标数严格分开；S0只算一个无彩目标。

每个interval有：`estimand`、`level`、`method`、`independent_unit`、`n_cycles`、`n_blocks`、`n_sessions`、`df`、假设、是边际或联合、应用域、`applicable`、缺少的偏差项。PI必须标未来是单次循环还是会话均值；不要只改字段名。共享Ray/环境/模型参数在源级抽样一次后复用，不能给每个strip虚构独立参考。

每个模型实测/预测区间区分：候选、拟合、独立确认、原留出已转开发、新留出。参考标签进入拟合后不能继续当全新的模型自检。

## 4. 摄影与原生质量字段

保存各主平面min/max/分位数/截尾均值/方差/MAD、valid pixels、near-noise比例、clipped/near-rail比例、white_rail_plateau、原生white level与保护距离。渲染图的饱和只作附加画像，不能替代CFA资格。

ISO、光圈需要区分请求值、桥返回值、RAW/EXIF测量值。`implicit auto`不是数值光圈，也不证明自动光圈真的变化；不存在的EXIF不补造。若值已经在嵌套capture对象中，索引提取应恢复，不写全空。

实际曝光起点、source_on、reset、前态、顺序、会话分隔、UTC和单调钟域均保留。不能用名义120/600替代实际值；计时器或bridge重启要标注钟域变化。

## 5. 最小离线验收矩阵

1. 两/多包成员身份闭合，物理哈希去重与逻辑索引对应。
2. 所有被采用/确认/引用的帧均能落到统计、矩阵、实际命令、隔离和时序；rejected也有真实身份。
3. 全70白光节点的源白点、signed误差、有效数、分类和置信字段重算，报告与JSON计数一致。
4. 所有彩光采用命令的3确认与选择分离、共享Ray分组、Δz/协方差复算。
5. 恢复的主层near-noise反例：block_06四平面有效但secondary58失败，主量仍能进入主层；主块真实失败反例仍被拒绝。
6. 白光70节点恒等、相邻两侧、GM边界、单调权重和max4095；实际实拍命令与运行时输出一致。
7. 彩光S0、已验证S100端点、0/360、低SAT非静默钳制、requested/realized标签，固定同Hue的轨迹检验。
8. 真实局部J与非正交反例：模拟非正交坐标时必须使用矩阵逆/受约束反解，不能通过90°旋转蒙混；H300旧算术反例必须暴露。
9. N2/新确认按独立会话/循环复算CI与PI，字段上下界自洽；相机噪声不双计，选择帧不计确认。
10. LONG时序、源差、差中之差和参考关系；all-off与on设置一致性及敏感性；不自动产生温度占比。
11. 逐Hue最大已测SAT必须回到原命令与合格映射；不能把“18pp短缺”在量尺不合格时转成82%覆盖。
12. 最終报告中的百分比区分点通过率、工作进度、覆盖率、模型置信度；不可由`complete`填100%。

整数命令、ID、n和哈希必须精确一致。数值重放容差建议K=0.01、mired=1e-4、Duv=1e-9、z=1e-9，另验证这些容差远小于产品判定余量；不要用某平台非线性argmin最后几位的差异当硬件失败。跨越判定边缘时保留两侧差并单独复核，不静默修改科学容差。随机MC固定算法/种子并留样本或完整参数，声明采样误差。

## 6. 打包结束条件

从新的临时目录解压包及明确基础包，完成上述重放后才生成最终manifest。测试只读、零设备/网络。报告写真实PASS/FAIL/NOT_APPLICABLE与原因；不能先写PASS再跑检验。

若计算输入确实未保留，给出精确终态和受影响结论，不补造、不重拍冒充历史。导出任务本身不启动任何实验。数据完整不等于科学通过；科学失败也可以是完整可审阅包。
