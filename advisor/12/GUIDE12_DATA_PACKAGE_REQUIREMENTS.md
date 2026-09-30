# GUIDE12 阶段结束交付合同

日期：2026-09-29。与 `12.GUIDE.md` 第9节共同生效。目标是让Advisor直接复算科学结果，不再逐轮索要已经拍过的数据；不建立新的运行时治理系统。

## 1. 交付形式与包内可复现范围

交付一个 `GUIDE12-COMPLETE-PROCESSED-EVIDENCE-<实际结束日期>.zip`，加一份同日期报告MD。所有路径相对ZIP根；原D盘/Mac路径只作为来源字段。结束日期据实填写，不沿用本GUIDE日期。

目录建议：

```text
README.md
FINAL-REPORT.md
MANIFEST.json
RUN_INDEX.json
OBSERVATIONS.jsonl
RAW_INDEX.jsonl
COMMANDS.jsonl
PAIRINGS.json
MISSING_OR_UNIDENTIFIABLE.json
runs/<run_alias>/...
measurements/<run_alias>/<capture>.patch-statistics.json
raw-small/<raw_hash>.json
matrices/<matrix_id>.json
models/white-final-lut.json
models/white-runtime-model.json
models/ray-hsi-map.json
models/strip-hsi-command-model.json
models/uncertainty-model.json
results/white-nodes.json
results/white-holdouts.json
results/white-fast-long.json
results/hsi-targets.json
results/hue-coverage.json
results/ray-self-inverse-holdouts.json
results/repeatability.json
results/ambient-sensitivity.json
source/...
config/...
replay/reproduce.py
replay/expected-results.json
replay/validation.json
```

不用照搬目录名建立新抽象层；但以下内容和逻辑必须完整。设备原RAW、视频、JPG、缓存、大数组可以不入ZIP；**所有被计算实际使用的小型数值不得遗漏**，尤其patch统计不是媒体排除项。`.env`、密钥、访问令牌、私有连接凭据不入包。

## 2. 物理身份、运行与观测账本

一张物理照片以重算RAW SHA-256为主身份，`run_alias+capture_id`为逻辑键；重复视图只能引用同一物理身份，不增加n。记录原路径、当前保留路径、字节数、SHA-256、sidecar身份、matrix_id。原始丢失则记录实际状态，不伪造已重算hash。

所有启动、失败、被拒、恢复前缀/后缀、诊断、环境帧与physical-return孤儿均列出。OBSERVATIONS须覆盖所有物理返回，包括特征提取前失败；这类记录measurement=null且明确原因，不能因不进入accepted ledger而消失。

每帧至少给出：源、CCT/GM或H/S/INT标签、用户GM与raw-GM的明确对应、capture角色、实验/会话/周期/burst/block编号、预定训练/选择/验证/留出角色、是否实际被采用、原始质量结果及后续重分类、measurement相对路径、实际曝光、物理照片身份。任何别名映射需要可验证的文件hash，不能仅靠同名。

RUN_INDEX保存所有相关根的起止、执行commit/dirty、计划及实际状态、capture计数、失败类别、暂停/重启、清理结果和旧路径别名。代码checkpoint是provenance，不是运行许可状态机。

## 3. 命令、满幅和物理隔离证据

逐命令保留：请求五通道坐标、是否linearized还是raw PWM、duty转换曲线版本、转换后payload、apply后的设备snapshot、readback、对应capture IDs、起止时钟。Ray分别保存菜单百分比与API数值，证明有效参考为100%；API1000不得与1000%混淆。

运行时若有主亮度、限流、功率预算、自动降额等已有可读字段，一并导出；不可读则明确hardware未观测，不凭某个请求码推断实际电流或光通量。

`fullscale_actual`只能从相应capture前最后有效apply/readback确定。计划max4095、请求max4095、实际max4095分别字段；未知读回不能默认为true。旧非满幅/低INT帧原样保留但`current_stage_eligible=false`。不能放大命令后继续认证原照片。

每张源观测前另一源为零的证据须可定位。结束时all-off不能替代拍摄时隔离。自动恢复/重新设置后须有本次capture前的证据。

## 4. RAW处理后数值：能不读CR3复算

保留全部24色块、全部CFA平面、原阈值、rejected指标、ROI/掩膜版本，而不只保存通过的58个最终数。逐平面导出原始码/black-corrected/曝光归一化域的统计、n、均值、trimmed mean、min/max、分位数、variance、MAD、nonfinite/near-noise/clipped计数及分母。

额外保存native RAW rail诊断：有效white level及来源、距离white level至少0/1/2DN的计数、最亮平台的码值/数量、原生全帧与ROI分开。渲染RGB曝光画像另标域、rawpy postprocess参数/版本，不得命名为原生RAW饱和。

逐RAW小文件保存实际MakerNote曝光、ISO/光圈、快门类型/模式已有元数据、black levels、white levels、pattern/size、`rgb_xyz_matrix`、软件版本及分析所需camera-neutral输入。矩阵可内容去重，但每帧必须有引用。

若某个分析器仍读取其他RAW属性，先列入依赖图并导出该数值，再允许排除RAW本体。不能在replay中悄悄回原盘读RAW。

## 5. 实际时间、环境与协议

计划reset/dwell、apply开始/完成、readback完成、source-on、exposure起点、返回时间分别记录时钟域/估计方法/不确定度。不能把计划值填作实际值；进程间单调时钟不可直接相减，优先同一域或有记录的映射。

导出thermal/history已有字段：前命令、off时长、load/duty历史、source/command age、会话起点、源先后、协议先后、暂停时段。缺失写null和原因。

all-off要有对应曝光、几何、前后关系和actual zero。导出各主CFA的环境敏感性及传播界，背景影响判断不能只给全帧均值或Ray的一个百分比。环境温度/照度有真实记录才填；不能用日期/等待秒数推造温度。

FAST/LONG以实际事件和源状态认定。一个等待很久的暂停不是LONG。每个协议差能追到4个源观测/其重复；实际命令不同的两个协议不能称同命令对照。

## 6. 误差、模型与搜索信息

### 白光

每节点及每留出保存：请求、实际PWM、Ray白点、strip白点、**有符号物理单位误差**、容差、无量纲绝对E分量、E最大值、估计角色、独立n与burst n、CI/PI和适用条件、置信判定、fullscale、同块配对身份、变更前后命令、停止原因。

物理误差字段绝不从归一化字段直接赋值。mired从同一CCT计算；各统计量源与符号一致。节点本底没有数据就不能用Ray−Ray=0补齐。

LUT、运行时插值函数、参数、knot、face切换、duty与整数化顺序、请求到最终payload的测试向量必须完整。留出测量的实际payload须等于被验证版本的函数输出。

### 彩光

Ray映射导出完整数值（而不是外置路径），各锚点的真实H/S/INT、源观测身份、epoch、协议、训练/验证角色、SAT0来源。不能含CCT白光聚合冒充HSI S0。保存真正独立Ray自反解留出：输入z、真实菜单、预测H/S、误差、残差、多解候选、局部Jacobian/奇异值、联合区间及映射离散误差。

每strip命令保存直接Δz、色比误差百分比、有效的Ray等效H/S、Hue/饱和度短缺、主层与58层分开、inverse唯一性、fullscale、独立重复和停止原因。色比百分比不是色域覆盖百分比。

每Hue分别保存`s_best_tested`及其命令/CI、`validated_samples`、`model_supported_intervals`、`covered_intervals`及其保证条件、`search_upper_request`和未搜索范围。没有合格逆映射或命令就填null与原因，不用0表示未建立；SAT0没有Hue，不能作为每Hue有效lower的自动证明。

### 搜索

导出全部实际测过的候选而非仅最佳：命令、原生质量、目标前后Ray、基点、可行方向、Δu/Δresponse、Jacobian版本/秩、预测与实际改善、trust ratio、face、取整、选择角色与独立确认。被rail污染的候选不能进入导数；无效观测仍保留其失败身份和消耗预算。

“best tested”只对已测集合有意义。“practical convergence”需测试方向/测量可分辨改善依据。“physical maximum”本阶段不输出。

## 7. 区间与分布合同

每个数字给出单位、estimand、样本/独立周期数、分组、配对关系、条件。至少分开：设计网格上的实测误差分布、源短时散布、cycle/session散布、均值CI、下一独立操作PI、模型/协议系统偏移。

区间导出计算输入、公式/模型、自由度、协方差/正则化、源级共享项系数、MC seed/sample count、联合覆盖方法、尾部/正态假设及转移资格。若用Monte Carlo，它只能传播已纳入的输入分布，不是证明所有干扰已经测清。

small n、模型无转移支持、未拍独立确认、映射不可辨识等情况，CI/PI字段允许null，但必须同时给已能识别的数值范围、原因、是否在本轮额外风险预算内解决、或已经固定的采用限制。历史不可恢复和当前硬件结构性不可辨识不再次列成“待补包”。

## 8. 可复现源码与本地结束校验

包括实际生成候选/插值/分析/报告的源码及参数，依赖所需的小型旧输入、配置与矩阵。标准库/第三方库给版本；不需要整个git史或工程日志山。source snapshot不得只有最后一个adapter而缺核心函数。

manifest逐成员列相对路径、bytes、SHA-256和来源；排除manifest自身的自引用hash但说明这一规则。报告ZIP字节/hash由最终实际ZIP生成，不使用上一次构建缓存。

在新的临时目录，从解压包独立运行replay，至少验证：

1. 全成员完整性与physical identity去重/未关联返回对账；
2. 全white点有符号单位、E、选择/确认分离；
3. 全实际满幅/100%资格；
4. 原生rail与其他主层质量；
5. 所有Ray自反解留出和SAT0来源；
6. 全最终节点直接配对误差、CI/PI代表性复算及数值一致性；
7. 同命令FAST/LONG实际时序和差中之差；
8. 运行时输出与实拍payload一致，训练/留出/重复身份无偷换。

CCT优化算法跨平台可能存在微小数值差异；预声明数值容差须远小于产品误差门，报告最大实际差。不能为了获得逐位diff0改变观测，也不能用很大的数值容差隐藏单位或代数错误。

## 9. 最终报告必须回答的六项

白光与彩光分别回答：实测支持的精度与未来操作范围；误差/噪声的数值与区间；尚可改善的有效方向和停止依据；每Hue的等效覆盖与逆映射资格；实际采用/不采用区域；本轮科学问题完成度与满幅产品认证完成度。

给出总预计主里程碑、剩余工作包及规划百分比，但明确不是准确率或统计CI。不要用tests pass、工作树干净、run complete代替科学结果。若结果改变初衷，应显式标明改变的是哪一个目标或假设，不能静默换指标。
