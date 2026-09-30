# 给本地Agent：GUIDE12 实现纠偏与推进

任务依据为 `12.GUIDE.md`；这是实验项目，不调用SFD/工程架构治理流程。不新建通用runtime、lineage/release资格体系、人工逐步Advisor状态机。现有运行器/分析入口能复用就复用；普通错误在当前工作树修复。设备执行仍须Human对具体实验授权，本Prompt不等于授权。

## 先离线完成的确定性修正

**1. 白光secant。** `guide11.py:build_w2_*` 中A=`u−u0`，B必须=`r(u)−r(u0)`。先固定唯一基点观测，再构造差，不以循环中“最后一个同命令帧”随意改基点。另存基点误差。记录命令差秩、输出可辨识秩、有效face、奇异值。现有25节点输入全秩1，仅支持该已测方向，禁止宣传成完整自由度已搜索。

提供最小确定性回归例：`r(u)=a*u+b`，b非零，正确导数必须与b无关；不能通过忽略b使测试通过。共享参考、配对差和代数抵消也用数值测试，不用源码字符串匹配代替行为。

**2. W2同块目标与独立确认。** 导入49条真正配对Ray，不再跳过Ray行。每候选连接同一个目标/候选block的参考，存在前后括界时记录组合权重与共享关系。历史W1目标只作单独对照。9个已采用命令独立确认状态为not_acquired，禁止把选择帧或不同命令留出当确认。

**3. W8单位。** `recompute_w8_guide11_20260928.py` 的W2分支不能将`e_gates`直接赋给`e_cct_K/e_mired/e_duv`。从两个白点重建有符号误差，分别保存`error_signed`、`tolerance`、`abs_normalized_error`。测试每个分量的恒等式及单位。旧artifact只读，新artifact清楚注明修正。

**4. 原生RAW资格。** 对所有已有输入先生成raw-rail审计，不只修红色单点。主C1 B1的24/32 strip帧白块存在上限平台；这些帧不再作导数/选择/方差输入。保留他们的测量统计和失败身份。新质量门按GUIDE12前瞻规则执行；`frame_exposure_profile`改名/标域为rendered RGB profile，不得与native RAW clipping混用，辅助图像过曝不能单独推翻主RAW合法性。

覆盖回归例：white=16383、整块16382、variance=0不能成为有效色度观测；原生不过曝但camera-WB后RGB过曝要区分两类；near-noise与saturation方向不可倒置。不新增“删掉不满意feature再通过”的fallback。

**5. 满幅约束。** 主求解器在至少一个actual-PWM=4095的face上求解，而不是无约束步之后逐通道clip。候选、确认、插值、模型压缩后的实际最终payload均检测。linearized/duty/raw坐标分开，4095需要apply/readback证据，不从上层名义值推断。没有readback标unknown，不默认true。

任何旧non-fullscale帧原样保留并隔离当前阶段。不得修改它的command后复用照片。无新的INT50/20/5或3072/2048运行；旧C5只是历史。

**6. Ray映射。** C3的SAT0仅来自真实HSI S0/INT100，不得来自N1 CCT/GM集合。保留原错误模型作诊断。先运行“Ray→inverse→自己的H/S标签”的真实误差测试；原nearest/second-nearest anchor ratio不是这个测试。保存所有可能的逆解、Jacobian/病态性、联合区域、模型数值与训练/留出身份。S0不返回一个看似精确的Hue。不要用原粗1pp SAT网格去证明0.5pp误差预算。

只更换SAT0还不是完整修复：高SAT的P6路径、missing anchors与局部非线性仍需真实Ray留出验证。不能把`within_c1_anchor_envelope`或比最坏失败例更好当产品pass。

**7. 覆盖字段。** `s_best_tested`计算实际等效SAT，不是通过的请求tier。`covered_intervals`须有内部留出/误差界；不存在有效lower时不要自动填(0,25)。没有有效映射写null/map_unqualified，不能写0%。所有数字与置信区间都记录适用范围及direct residual。

**8. 时序/噪声。** 分开planned与observed，时钟域明确。FAST/LONG差中之差只能连接同命令、正确协议的源观测。N2区分session/cycle/burst，保留共享Ray协方差。零/极小样本SD不能宣称硬件噪声下限；模型PI不可由不适用组强行池化。

## 科学实施顺序

先生成修正后的只读审计与候选计划；曝光/all-off/N2优先解决可观测性。白光、彩光两线按GUIDE12自主推进，单点有界失败不阻断另一线。每个batch列清问题、unique-command与physical预算、实际fullscale、参考和停止分支，再请求Human设备授权。不要把全部预算机械拼成一次无人值守长跑。

最终命令/运行时函数先冻结，后独立确认。处理需要新观测的问题时照实新增实验，不把它伪装成补齐历史数据；历史未记温度或相机/PWM结构性不可分离一次写清，不反复求gate。

## 验证与交付

只为上面确定性行为和真实输入增加必要测试，允许正常修bug，不设“最多修一次普通实现”的终止规则。源码检查不能代替真实输入数值replay，测试通过也不称科学通过。

按 `GUIDE12_DATA_PACKAGE_REQUIREMENTS.md` 一次交付完整处理后证据；包括错误/拒绝输入、原生RAW小数值、全部patch统计、实际命令读回、时序、完整模型、分组区间输入及对应源码。原RAW可不打包，但replay不得偷偷回原盘读取。最终manifest排除自身哈希，逐成员验证后再输出ZIP hash。

最终人类回报用科学结果开头：哪些目标被支持、哪些仅有界近似、预测区间、各Hue真实覆盖、未采用域和下一步。不要用“工作树干净/无运行任务/complete”替代这些结论。
