from analysis_utils import *
import hashlib
from collections import defaultdict
B=Path('/mnt/data/audit_work');O=Path(__file__).parent
w=load(O/'white_per_point_results.json');n=load(O/'noise_and_model_diagnostics.json');h=load(O/'hsi_projection_diagnostics.json')
# Explicitly label limits reconstructed for the off-node diagnostic.
w['method']['threshold_provenance']={'w6':'exact experiment-spec analysis_contract.target_contracts; not one common Kelvin tolerance','w7':'25 K / 1 mired / 0.0005 Duv diagnostic reconstruction; W7 spec has no per-target tolerance table and original W8 generator was not retained. Reported 1/20 comes from W8 itself. Do not treat these as a newly validated off-grid tolerance contract.'}
(O/'white_per_point_results.json').write_text(json.dumps(w,ensure_ascii=False,indent=2))
for r in h['results']:
 if r['label']=='guide9-h0-s0-best':
  for s,v in r['sources'].items():
   if v.get('nearest_hue') is not None: v['unconstrained_optimizer_hue_diagnostic']=v['nearest_hue']
   v['nearest_hue']=None
   v['conditional_fixed_manifold_projection_95_intervals']=None;v['conditional_fixed_manifold_projection_sd']=None
   v['interval_warning']='SAT0 target has no meaningful Hue; strip solution lies on a cell boundary. No smooth local Gaussian H/S interval is reported.'
(O/'hsi_projection_diagnostics.json').write_text(json.dumps(h,ensure_ascii=False,indent=2))
obs=jlines(B/'supp/OBSERVATIONS.jsonl');mismatch=[o['observation_id'] for o in obs if o['source_label']=='guide10-white70-w6' and o.get('thermal_covariates') and o['thermal_covariates'].get('source_id')!=o['source_id']]
inputs=[]
for name in ['source-code.zip','guide10-complete-processed-evidence-20260922.zip','guide10-processed-evidence-supplement-20260922.zip','guide10-missing-dependencies-delta-20260922.zip']:
 p=Path('/mnt/data')/name;inputs.append({'name':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
findings=[
 {'id':'F01','conclusion':'White W6 36/70 point-estimate pass, no full best-capability demonstration','evidence':['base/guide10-white70-w8-final/guide10-white70-final-artifact.json','supp/replay/w6_w7_long_white_pair_replay.json']},
 {'id':'F02','conclusion':'W7 off-grid 20/20 exact nearest-node commands; 1/20 legacy pass, not validation of a continuous interpolator','evidence':['supp/replay/source/guide10_white70.py:554-569','supp/replay/w7_nearest_w6_command_comparison.json']},
 {'id':'F03','conclusion':'Legacy W7 LONG plan and executed branch are FAST 600/120, not LONG 1800/600; retain as additional FAST. First pair is split by roughly five hours.','evidence':['supp/replay/source/guide10_white70.py:572-585','supp/source-data/guide10-white70-w7/formal-20260921-long/experiment-spec.json','supp/source-data/guide10-white70-w7/formal-20260921-long-resume/experiment-spec.json','supp/source-data/guide10-white70-w7/formal-20260921-long-resume/guide9-h120-s50-batch1-evidence.json','supp/source-data/guide10-white70-w7/formal-20260921-long-resume/thermal-covariates.jsonl']},
 {'id':'F04','conclusion':'W5 candidate navigation omits mired; fallback channel sorted partly by name, +/-256/512 based on scalar error sign, not measured channel sensitivity; insufficient for optimality/quantization claims','evidence':['supp/replay/source/guide10_white70.py:396-430','delta/source-data/w5-white-lut-calibration/white-lut-calibration.json']},
 {'id':'F05','conclusion':'Eight remaining main HSI INT100 nodes not acquired; tested stable commands do not establish per-Hue maximum saturation','evidence':['supp/STATUS_MATRIX.json','supp/source-data/guide9-h120-s50-best','supp/source-data/guide9-h300-s50-best']},
 {'id':'F06','conclusion':'OBSERVATIONS W6 thermal join has source mismatch in 70 of 140 rows. Do not regress this index field; return to primitive capture/source/time identity','count':len(mismatch),'observation_ids':mismatch,'evidence':['supp/OBSERVATIONS.jsonl']},
 {'id':'F07','conclusion':'Current historical nearest-manifold H/S coordinates are numerical projections with large out-of-manifold residual, not Ray-equivalent gamut coverage','evidence':['hsi_projection_diagnostics.json','supp/source-data/ray-hsi-manifold-p6/ray-hsi-analysis.json']},
 {'id':'F08','conclusion':'Residual distributions across grid are not repeatability noise; conditional propagated intervals are not future operating prediction intervals','evidence':['white_per_point_results.json','noise_and_model_diagnostics.json']}
]
audit={'date':'2026-09-22','input_archives':inputs,'processed_package_integrity':load(B/'integrity.json'),'required_ten_dependencies':'all supplied, exact identities verified; no further export request','scope':'processed evidence and retained code; no re-decoding CR3, no device or network operations on user equipment','findings':findings,'white_summary':w['summary'],'HSI_new_guide10_grid_nodes_executed':0,'HSI_remaining_main_nodes':[[i,s] for i in [0,60,180,240] for s in [50,100]],'completed_true_GUIDE10_LONG_nodes':0,'progress_estimates_not_statistical_CI':{'white':{'point':65,'planning_range':[60,70],'total_milestones':8,'remaining_work_packages':4},'color':{'point':45,'planning_range':[40,50],'total_milestones':9,'remaining_work_packages':6}}}
(O/'GUIDE10_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
lines=[]
lines += ['# GUIDE10 审阅与 GUIDE11 研究记录','', '日期：2026-09-22。研究对象：Ray120c → 固定 Canon R6 III 观察者 → RGBWW 灯带。','',
 '## 结论','',
 '**本轮资料足以开展分析，不再要求第三轮补包。白光不能认定已到硬件能力极限；彩光不能认定全 Hue 覆盖稳定或已达到最大可达饱和度。需要 GUIDE11。**',
 '', '白光现状是“部分节点已接近目标，部分节点有明显系统残差，连续插值和真正的 LONG 验证尚未完成”；彩光现状是“Ray 目标拓扑与代表命令已测，剩余八个主节点未执行，尚无合格的全 Hue 覆盖图”。',
 '', '进度估计：白光 65%（规划范围 60–70%，总计 8 个主里程碑，剩余 4 个工作包）；彩光 45%（40–50%，总计 9 个主里程碑，剩余 6 个工作包）。这些是工作完成度估计，不是匹配精度、色域面积比例或统计置信区间。',
 '', '## 1. 数据基础与来源','',
 '基础包 196、补充包 2463、增量包 491 个 manifest 条目逐一核对大小和 SHA-256，均一致；10 个上轮指定冻结依赖已找到。对 W4 的同一 CR3 在 combined/original 两个视图出现的条目按物理身份去重，不把 280 行当成 280 张独立照片。',
 '', '本轮使用处理后的 patch statistics、逐帧特征、矩阵、命令、时序证据和代码；未重新解码 CR3。本轮不以丢失的原 W8 生成器为继续实验的门槛，必要数值直接重算。历史温度未记录的事实不能通过软件“补齐”。所有输入 ZIP 哈希、结论及证据定位见 `GUIDE10_AUDIT.json`。',
 '', '## 2. 白光：数值结果','',
 '误差定义始终是 strip − Ray，而不是相对标称菜单 Kelvin。Kelvin/Duv 为项目既有相机矩阵和近似色度模型的诊断坐标，不是光谱仪溯源值。CCT 与 mired 是同一个温度坐标的非线性变换，二者不作为两个独立的随机维度。',
 '', '| 数据 | 通过数 | 绝对 CCT 误差中位数 / P95 | 绝对 mired 误差中位数 / P95 | 绝对 Duv 误差中位数 / P95 |','|---|---:|---:|---:|---:|']
for g,label in [('w6','W6 最终70节点'),('w7','W7 最近节点非节点测试')]:
 s=w['summary'][g];d=s['error_distribution'];lines.append(f"| {label} | {s['point_pass_count']}/{s['count']} | {d['cct_K']['abs_median']:.2f} / {d['cct_K']['abs_p95']:.2f} K | {d['mired']['abs_median']:.3f} / {d['mired']['abs_p95']:.3f} | {d['duv']['abs_median']:.7f} / {d['duv']['abs_p95']:.7f} |")
lines += ['', 'W6 通过比例为 51.43%；W7 为 5%。这是指定离散测试集合的计数，不是随机抽样总体的成功率，不能给它套一个二项分布 CI 后声称覆盖了连续 CCT/GM 空间。W6 mired 带符号范围为 −42.389 到 +22.286，Duv 为 −0.00840286 到 +0.000584077。全网格误差分布明显具有异质性与长尾，不适合直接拟合一个正态“噪声”。','',
 '### 每个 CCT 行的离散通过数','', '| CCT 菜单值 | 5 个 GM 节点通过数 |','|---:|---:|']
rr=[x for x in w['points'] if x['group']=='w6']
for c in sorted({x['target']['cct'] for x in rr}):lines.append(f"| {c} | {sum(x['legacy_point_pass'] for x in rr if x['target']['cct']==c)}/5 |")
lines += ['', 'GM 节点为 raw 0、70、100、130、200；以 GM100 为中性，UI 的 ±1 不能与 raw 数字直接混用。Kelvin 容差沿用各节点实际合同，并不全是 ±25 K，存在 12.5 K 等局部收紧以及高色温特定容差。',
 '', '### 每点的不确定度','',
 '对 70 个 W6 节点、20 个 W7 点和 6 个追加 FAST 点，以冻结 Ray/strip 对角方差作为条件模型，每 source/pair 12000 次 Monte Carlo，经原白点公式传播。加速计算与原始 replay 的中心差异最大约 0.00057 K、0.0000065 mired；不是更换相机标定。逐点命令、误差、95% 边际区间、条件标准不确定度及来源 ID 全部在 `white_per_point_results.json`。',
 '', '这些区间假定旧冻结方差可迁移，**没有覆盖历史到当前的状态差异、长期温度、未测会话、模型误差或相机的绝对色度偏差**；不是完整预测区间。冻结方差是测量链的条件模型，不是已证明不可逾越的物理噪声底。',
 '', 'W6 条件标准不确定度：mired 中位数 0.243，范围 0.161–0.358；Duv 中位数 0.0000911，范围 0.0000590–0.0001182；Kelvin 中位数 4.55 K，范围 1.22–60.32 K。高 CCT 的 Kelvin 不确定度大，不等于色度或传感器噪声突然变差。',
 '', '在每节点三个指标的 Bonferroni 95% 联合箱诊断中，仅 15/70 的整个箱落在旧容差内。它是条件模型下的附加评估，不是全70点同时95%保证，也不替换历史99.73%门或构成最终认证。',
 '', '| W6 节点 | mired 误差 | 条件95%区间 | Duv 误差 | 条件95%区间 |','|---|---:|---:|---:|---:|']
for c in [1800,3200,5600,20000]:
 x=next(x for x in rr if x['target']=={'cct':c,'gm':100});e=x['errors'];ci=x['conditional_frozen_model_95_intervals'];lines.append(f"| {c}/GM100 | {e['mired']:+.3f} | [{ci['mired'][0]:+.3f}, {ci['mired'][1]:+.3f}] | {e['duv']:+.7f} | [{ci['duv'][0]:+.7f}, {ci['duv'][1]:+.7f}] |")
lines += ['', '### 1800/GM100：停止搜索不等于已经永久匹配','',
 '同一 R4095/G1197 命令，早期三次 mired 误差约为 −0.588、−0.397、−0.684，W6 变成 +1.712，追加 FAST 变成 +2.587。早期小批次通过不能代替跨会话稳定。三次旧确认的最大差仅约 0.287 mired，但长期误差中心已经改变；不能把后者当作更多独立微小噪声平均掉。当前保留其有界停止，不再重启 G 的无限微调。没有测得“相邻整数跨越互斥边界且不存在可行整数”，不得认定 12-bit 量化受限。',
 '', '## 3. 四处直接影响科学结论的实施问题','',
 '### W5 不是完整的 gate-aligned 求解','',
 '`supp/replay/source/guide10_white70.py` 396–430 行仍调用历史 CCT/Duv Jacobian 求解，未将 mired 门纳入优化目标；后续所谓 micro-step 选择第一个按边界状态和通道名称排序的自由通道，并根据 mired/Duv 的符号决定 ±256/512。通道的作用方向不能由变量名或误差符号推出。这些照片是有效命令测试，但不足以证明有用控制方向已被搜索完，更不能证明硬件到顶。旧 P2/P3 模型只能用于初值。',
 '', '### W7 没有测试真正连续插值','',
 '20 个灯带命令全部等于某个最近 W6 节点。代码 554–569 行按相对 Kelvin 距离与 GM 距离选一个 knot，直接复制命令。1/20 是这一最近节点策略的表现，不是双线性、mired×GM 或实际连续运行模型的表现。',
 '', '### 所谓 LONG 实际是 FAST','',
 '两个 LONG spec 保留 `cold_proxy_wait_s=600`、`requested_elapsed_s=120`，builder 572–585 行只换标签和点表。执行生成的 `guide9-h120-s50-batch1-evidence.json` 明确记录 `independent_reset_s=600`、`dwell_s=120`。运行代码与时序证据相符，没有执行1800/600协议。',
 '', '**GUIDE10 真正完成的 LONG 节点数为 0。** 12 张照片保留为追加 FAST；六组 `e_later−e_W6` 是会话差，不能叫热偏差。第一组 1800/GM100 的 Ray 与 strip 跨约五小时暂停，单独标记为长间隔比较，不能视为短时间 target-local pair。',
 '', 'W8 的 `fast_long_bias` 又是六个“LONG”残差本身的均值/范围，并非差中之差。补充包虽然已复算差中之差，但不能修复采集协议本身。追加 FAST 的 mired 差值依次为 +0.875、−0.092、−0.136、−0.0004、−0.218、−0.031；Duv 差值为 +3.67e−5、−1.06e−5、−2.88e−5、+1.34e−6、+4.01e−5、+8.39e−5。它们不构成统一热模型。',
 '', '### 汇总索引的 thermal join 不可直接分析','',
 f'W6 140 条索引中有 {len(mismatch)} 条的 `thermal_covariates.source_id` 与照片 source 不同。例如第一张 Ray 被挂上下一张 strip 的通道、负载与时序。逐帧颜色向量和白点 replay 不依赖这处错误，仍可保留；热回归必须回到原始 capture/source/sequence 身份。部分 runner 的 best-effort 时间原点也在120秒等待之后，不能把该4–6秒字段当作实际点亮总时长。',
 '', '## 4. 哪些噪声已知，哪些不能归因','',
 'P1 的两个历史日，各光源只有5次 paired repeat。以下是白块相机代理坐标的样本标准差，括号为近似 iid 正态假设下95% SD区间；n=5 无法自行验证分布或长期平稳。',
 '', '| 组 | CCT 标准差 K（95%区间） | mired 标准差（95%区间） | Duv 标准差（95%区间） |','|---|---:|---:|---:|']
for r in n['p1_groups']:
 vals=[]
 for k in ['cct_K','mired','duv']:
  z=r['metrics'][k];vals.append(f"{z['sd']:.5g} [{z['sd95CI'][0]:.5g}, {z['sd95CI'][1]:.5g}]")
 lines.append(f"| {r['day']} {r['source']} | "+' | '.join(vals)+' |')
lines += ['', 'Ray 的92特征强度 CV 中位数为0.757%/0.830%，strip 为0.0590%/0.0651%。这些 CV 包括整体亮度起伏，不等于颜色误差，更不等于纯传感器精度。上述白点/色度统计已经去除公共亮度尺度。',
 '', '已知的是特定命令/协议下的“相机+光源+测量链”合成波动。不能再独立加一份“相机噪声”，也不能给出“相机占20%、灯带热占80%”等未经辨识的方差占比。历史环境/接触温度没有记录，过去的精确温度成因不可追溯。未来可分离 burst、reset/cycle、session 三个统计层级；在没有独立稳定光源或温控干预的情况下，最内层仍可能同时包含传感器、PWM和驱动波动。',
 '', 'P3 的24个不同混光命令中，“各命令跨特征形状相对残差P95”的跨命令中位数为6.43%，P95为28.57%，最大62.77%。不要把这个指标与全特征整体RMSE混为一谈。它检验的是加法前向模型失配，而不是测量随机噪声。',
 '', 'W6 58维最优整体尺度相对残差的中位数约18.58%，P95约19.25%；所有颜色块共同响应的差异远比白点微小抖动大。它可能包含光谱×反射率、空间照明/散射和几何效应，不可直接冠名“CRI不足”。中性色块G响应相对白块的strip/Ray比值，在70点中位数分别为 block03 1.02334、block04 0.99536、block05 0.98842；有小幅非共同增益效应，但不足以仅凭该表分离原因。',
 '', '因此，“已优化到噪声地板”不成立：部分大误差是确定的算法/插值问题，部分是已观察到的会话变化；剩余材料响应不是本项目必须消除的显色指数目标。',
 '', '## 5. 彩光：稳定命令不等于稳定色域','',
 '13个主要INT100节点中，H0/S0、H120/S50/S100、H300/S50/S100已有代表性路线；其中高饱和两个路线仍含重复性/参考源限制，不能作为稳定饱和度上界。剩余H0/H60/H180/H240的S50、S100共8点明确未执行。',
 '', '| Hue | 当前证据 | 能否报告最大覆盖比例 |','|---:|---|---|',
 '| 0 红 | H0/S0仅为零饱和白，不是红色端点；S50/S100未测 | 不能；未测不写0% |',
 '| 60 黄 | S50/S100未测 | 不能 |',
 '| 120 绿 | S50与S25有稳定nonfaithful命令；S100操作重复性未解决 | 不能认定最大值 |',
 '| 180 青 | S50/S100未测 | 不能 |',
 '| 240 蓝 | S50/S100未测 | 不能 |',
 '| 300 洋红 | S50有稳定nonfaithful命令；S100参考重复性受限 | 不能认定最大值 |',
 '', '### 能算出来、但不能当色域比例的数值','',
 '用完整P6节点重新构造原始周期双线性流形，逐一搜索72个分片，按冻结58-feature方差加权求最近点。P6重复组按原实现使用各特征中位数，SAT0使用原共同特征上的合并方向和亮度尺度。不是理论HSL模型。结果如下。',
 '', '| 已测目标 | 最近历史P6 Hue | 最近历史P6 SAT | SAT条件95%投影区间 | 离流形58维单位向量距离 |','|---|---:|---:|---:|---:|']
for r in h['results']:
 if r['label']=='guide9-h0-s0-best':continue
 z=r['sources']['strip'];label={'guide9-h120-s50-best':'H120/S50','guide9-h120-s25-best':'H120/S25','guide9-h300-s50-best':'H300/S50'}[r['label']];ci=z['conditional_fixed_manifold_projection_95_intervals'][1]
 lines.append(f"| {label} | {z['nearest_hue']:.3f} | {z['nearest_sat']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] | {z['unit58_distance']:.5f} |")
lines += ['', '**上述置信区间只描述固定历史流形下、冻结测量方差所引起的数值投影变化，不能解释为真正Ray等效SAT或色域上限的置信区间。** 未包含目标流形误差、协议迁移、未测试命令或材料响应失配。区间很窄而模型很错完全可以同时发生。完整Hue条件区间、命令和每帧ID见 `hsi_projection_diagnostics.json`。',
 '', '对应 strip 离流形加权距离约1172、1228、1273；当次Ray自身相对历史P6的最近距离约42.0、46.0、32.4（使用同一诊断权重，不能直接当新正式gate）。Ray自身单位58维残差约0.0046–0.0067，strip约0.172–0.181。这不支持把当前灯带投影直接叫做“绿色覆盖47.25%、洋红覆盖48.27%”。',
 '', '补充区分：最大已测稳定SAT只是在已测试命令集合中的最大值；对真实未知的最大可达SAT，它通常只是一个可达下界。要声称连续覆盖0到某SAT，还要验证中间区间没有缺口与逆序，不能只测到一个高SAT点。',
 '', '## 6. GUIDE11 的科学纠偏','',
 '保留原RAW观察者、58维严格评价和所有既有科学负结果；新增并明确优先“中性块相机色度复制”这一产品层指标，58维材料/空间响应为并列报告及次级优化。它不把旧58维失败改成通过，而是避免将用户明确不要求的全色卡呈色一致变成唯一进度门。白光沿用原每点CCT/mired/Duv目标，不回归单一Kelvin指标。',
 '', '新路线先复用现成数据修正判据、候选和插值定义；再做有限的重复性辨识、剩余白光有界修正、真正插值留出与真实FAST/LONG对照。彩光直接完成剩余8点，在用户体验坐标上建立有界饱和度路线，保留旧58-feature对照结果，再完成周期/低SAT/非节点留出和INT可分离性。完整设计、预算和停止规则在 `11.GUIDE.md`。',
 '', '## 7. 外部方法依据与适用限制','',
 '外部文献只用于不确定度与统计设计，不替代项目实测。NIST Ohno说明白光色度需要CCT与Duv两个坐标；本项目并未因引用该文而获得绝对色度准确性。JCGM101用于通过非线性测量模型传播输入分布，JCGM102用于多输出联合分布。采用Monte Carlo不会自动补上遗漏的系统影响量。',
 '', '- NIST, Ohno, Practical Use and Calculation of CCT and Duv: https://www.nist.gov/publications/practical-use-and-calculation-cct-and-duv',
 '- BIPM, JCGM 101:2008: https://www.bipm.org/en/doi/10.59161/jcgm101-2008',
 '- BIPM, JCGM 102:2011: https://www.bipm.org/fr/doi/10.59161/jcgm102-2011',
 '', '本次新增产品容差、抽样数量与停止预算是Advisor提出的工程/实验设计选择，不是上述标准给出的视觉阈值或统计功效保证。',
 '', '## 8. 复算说明','',
 '`analysis_utils.py`、`analyze_white.py`、`analyze_noise.py`、`analyze_hsi.py`为只读分析脚本。依赖Python、NumPy、SciPy；按文件头的B路径指向解压目录。HSI脚本仅导入保留源码中的流形/RAW统计纯函数，不运行控制器。`build_report.py`整理输出。脚本读取本次上传证据，不连接设备、不改源数据。',
 '', '逐点JSON里的null、条件区间与未适用字段必须保持其含义，不能在本地展示层自动填成0、100%或“已稳定”。']
(O/'11.RESEARCH.md').write_text('\n'.join(lines),encoding='utf-8')
print('Report written',len(lines),'lines; thermal index mismatches',len(mismatch))
