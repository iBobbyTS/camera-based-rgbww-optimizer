# 给本地 Codex：执行 GUIDE11 的最小实现纠偏

先阅读 `11.GUIDE.md`、`11.RESEARCH.md` 和 `GUIDE10_AUDIT.json`，再按科学工作包推进。不要新建通用框架，不调用/模仿 sectioned-feature-development，不创建新的lineage、readiness、review-budget或release状态机。普通bug在当前工作树内修好；保存一份简短计划与每个科学里程碑结果即可。

本次数据已经足够分析，不再做“完整审计包整理”任务，不重新采P1/P2/P3/P6，不追索已明确丢失的W8生成器。

## 一次性修正现有实现

1. 核对当前代码与 `supp/replay/source/guide10_white70.py` 的差异，只修仍存在的实际问题。
   - W5约396–430行：历史求解只使用CCT/Duv，fallback按通道名称选自由通道并猜±256/512。改成GUIDE11定义的全容差导航，优先消费已有真实成对观测的响应；历史Jacobian只当初值。不得把函数/字段改名后继续遗漏mired。
   - W7约554–569行：最近节点直接复制只能叫nearest-node diagnostic。运行时真正的mired×GM插值必须作为同一个函数被控制器和验证计划使用；把每个新留出请求及实际五通道命令写入结果。
   - W7 LONG约572–585行：必须真实设置1800秒off、600秒on，并确认实际runner不再走写死600/120的旧GUIDE9分支。不是改标签。对目前12张错误标签的照片建立不可变派生重分类，保留原root。
2. 修正 `OBSERVATIONS.jsonl` thermal join：使用物理照片身份/capture_id+source+sequence，不仅使用state_id。W6目前70/140行source不匹配。不要基于这个汇总字段回归温度、负载或时间效应；回到原始capture和事件。
3. 时间记录拆开：实际source-on、target-command、readback、等待完成、capture request/曝光best-effort。不能在等待120秒之后开始计时，再把4–6秒当成整个on时长。无法精确测曝光开始则保留best-effort及误差范围，不伪造精确值。
4. W8报告改为由真实输入重算：逐点命令、误差、阈值来源、repeat数、selection/validation身份、条件区间/预测区间、未适用原因。FAST–LONG必须计算差中之差，并且先验证两边实际协议。没有LONG输入就输出 `true_LONG_observations=0`，不是计算一个名字叫thermal_bias的数。
5. 增加中性块色度产品层，保留旧58-feature计算和原始负结果。两个层级使用不同字段：不得将新的产品层通过映射成旧strict=true，不得删原特征或把旧方差放大到通过。
6. 完成P6当前锚点自检与多解检查。历史58维最近点不能直接作为有效SAT覆盖。SAT0 Hue必须是not_applicable；区间无效时用明确状态和原因，不自动填0。
7. 核对当前设备授权入口：计划builder不能仅靠写 `human_authorization_verified=true` 自行授予设备权限。沿用现有用户授权机制，不新增治理框架。

## 只补与这些问题直接相关的行为测试

- 同一个请求经runtime与验证计划得到完全相同的插值命令；chosen non-node不是静默nearest-copy。
- 用注入时钟/设备callback验证FAST和LONG真实关/开/等待顺序不同；标LONG但执行600/120必须拒绝该科学标签。
- 误差方向冲突样例：CCT/Duv改善但mired越界时不能被选为通过；相邻量化与256/512步长语义不混淆。
- thermal join不跨source；shared-Ray与同一CR3别名不重复计数。
- 保留opposite-source-zero和实际cleanup；SAT0不做Hue gate；产品层通过不等于旧58维通过；区间缺项不变成0。

完成上述针对性测试，再跑一次现有相关回归。不得为了反复双review/clean streak暂停科学进度；末次代码变更后重跑受影响测试即可。fake backend必须复用真实scheduler，不能只写预期pass文件。

## 科学推进

按GUIDE11的N1、W1–W4、C1–C6准备具体实验。离线工作可自行完成；每次设备批次仍使用用户授权。保持明确预算，不重开1800/GM100及已关闭绿色/洋红S100搜索，不因一个Hue不稳定阻断其他Hue。

可复用本包Python脚本中的只读公式及数值作为回归参考，但不硬编码期望分数替代计算。脚本默认解压路径为 `/mnt/data/audit_work`，在本机调整B路径；HSI脚本也需要指向当前/保留源码路径。

最终交付要直接回答：哪些点主光色已满足、哪些稳定最佳近似、哪些操作受限；每个Hue目前能支持的SAT区间而不只是一个最大点；下一次使用的误差分布与预测区间。不要再次仅回复“GUIDE11 complete，等待安装”。
