"""Generate readable tables from the Advisor reanalysis JSON, not hand counts.
Usage: python build_review_tables.py PACKAGE_DIR
"""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
P=Path(sys.argv[1]);D=P/'data'
def ld(n):return json.loads((D/n).read_text(encoding='utf-8'))
def f(x,n=6):
 if x is None:return '不可估计'
 return f'{x:.{n}g}'
def ci(a,n=6):return '—' if a is None else '['+', '.join(f(x,n)for x in a)+']'
def vec(a,n=6):return '('+', '.join(f(x,n)for x in a)+')'
W=ld('white_nodes.json');N=ld('noise_analysis.json');C=ld('color_confirmations.json');G=ld('primary_secondary_gate_audit.json');A=ld('map_and_gate_audit.json');E=ld('environment_and_protocol.json');S=ld('color_search_and_quality.json');I=ld('interpolation_audit.json')
lines=['# GUIDE12逐点复核数值表','', '日期2026-10-12。所有差为strip−Ray；白点是项目原相机代理量。计算脚本、源包身份与假设见README/RESEARCH及data。', '', '## 1. 70节点：点估计与独立证据', '', '三个分量顺序固定为K、mired、Duv。raw-GM100=中性；raw-GM0/200对应用户端GM两端，转换保留控制器约定。单次验证不自动借用未验证的方差，故其CI/PI为空。参考失败点的数值仅描述，不作为认证。', '', '| 节点 | 实际PWM (CW,WW,R,G,B) | 配对数/有效数 | 描述平均误差 (K,mired,Duv) | 原点判定 |', '|---|---|---:|---|---|']
for x in W['nodes']:
 d=x['descriptive_mean_error_including_reference_limited'];cmd=x['command'];lines.append(f"| {x['node']} | {tuple(cmd[c]for c in ('cw','ww','r','g','b'))} | {x['observed_pairs']}/{x['valid_pairs']} | {vec(list(d.values()))} | {x['original_verdict']} |")
lines+=['','原机器计数38点通过、29超差、3参考受限；这不是38个带未来预测保证的点。16个变更节点除3200/0可复用同命令N2六循环外，其余15个未满3个独立验证。','', '### 多于一次有效配对的条件区间', '', '假设固定命令与协议下这些循环近似独立正态；n=2/df=1非常宽，不代表已验证跨会话分布。数值的有限位四舍五入不能替代判断原值。3200/0另有N2分析，优先同时看第2节。','', '| 节点 | 分量 | 均值 | SD [SD条件95%CI] | 均值95%CI | 下一同条件循环95%PI |','|---|---|---:|---|---|---|']
for x in W['nodes']:
 st=x['conditional_statistics_valid_pairs']
 if st['n']<2:continue
 for k,component in enumerate(W['components']):lines.append(f"| {x['node']} | {component} | {f(st['mean'][k])} | {f(st['sd'][k])} {ci(st['sd_ci95'][k])} | {ci(st['mean_ci95'][k])} | {ci(st['next_pi95'][k])} |")
lines+=['','## 2. N2：会话与循环','', '每白光状态3会话×2循环。均值CI的独立单位为会话；“下一会话均值PI”预测两循环会话均值；单次新会话操作PI来自随机截距矩估计并使用df=2 t，只有近似条件解释，不是精确已校准的95%覆盖。', '', '| 状态 | 分量 | 均值 | 会话均值95%CI | 下一会话均值95%PI | 近似下一新会话单循环95%PI |','|---|---|---:|---|---|---|']
for x in N['states']:
 st=x['session_mean_statistics']
 for i,k in enumerate(N['components']):lines.append(f"| {x['state']} | {k} | {f(x['mean'][i])} | {ci(st['mean_ci95'][i])} | {ci(st['next_pi95'][i])} | {ci(x['approx_next_individual_operation_PI95'][i])} |")
lines+=['','### 分量估计（统计分组，不是物理来源份额）','','| 状态 | 分量 | 会话内循环SD | SD的条件95%CI | 会话间SD矩估计 | 保守会话间SD条件区间 |','|---|---|---:|---|---:|---|']
for x in N['states']:
 for i,k in enumerate(N['components']):lines.append(f"| {x['state']} | {k} | {f(x['within_cycle_sd'][i])} | {ci(x['within_cycle_sd_ci95'][i])} | {f(x['between_session_sd_moment'][i])} | {ci(x['between_session_sd_conservative_ci95'][i])} |")
lines+=['','### 约40秒burst的原始时间趋势','','| 状态/源 | 实际源曝光时刻(s) | 首末差(K,mired,Duv) |','|---|---|---|']
for x in N['bursts']:lines.append(f"| {x['state']}/{x['source']} | {vec(x['observed_elapsed_s'])} | {vec(x['last_minus_first'])} |")
lines+=['','这些首末差各只有一条序列；无法估计可外推的趋势CI。每条序列的样本SD及条件区间保留JSON，但不能称纯相机噪声。','', '### 恢复的N2蓝光主层', '', '仅使用原已选完整的三个会话；旧secondary58 near-noise结论不变。未匹配的控制命令不等于最终蓝光采用命令。']
nb=G['N2_blue_recovered_primary_analysis']
lines+=['','| 分量 | 平均Δz | 会话均值95%CI | 下一会话均值95%PI | 会话内SD [95%CI] |','|---|---:|---|---|---|']
for i,k in enumerate(('ln(R/G)','ln(B/G)')):lines.append(f"| {k} | {f(nb['mean_dz'][i])} | {ci(nb['session_mean_ci95'][i])} | {ci(nb['next_session_mean_pi95'][i])} | {f(nb['within_cycle_sd'][i])} {ci(nb['within_cycle_sd_ci95'][i])} |")
lines+=['','## 3. 14个彩光目标：三次确认、共享Ray不确定度','','以下不含选择帧。CI是块内参考平稳、独立高斯reset的Welch工作区间，计入共享Ray均值协方差；它不是未来任意会话PI，也未包含H/S模型误差。不要将这些log色比区间转换成未经验证的SAT CI。', '', '| 目标 | 确认数/参考块数 | Δln(R/G) [条件95%CI] | Δln(B/G) [条件95%CI] | R/G与B/G相对误差% |','|---|---:|---|---|---|']
for x in C['colors']:
 mu=x['mean_dz_confirm_only'];cv=x['shared_Ray_mean_ci95_working'];lines.append(f"| {x['target']} | {x['independent_confirmations']}/{x['independent_confirmation_blocks']} | {f(mu[0])} {ci(cv[0])} | {f(mu[1])} {ci(cv[1])} | {vec(x['relative_ratio_error_percent'],5)} |")
lines+=['','### 彩光实际采用命令与并列材料响应','','58相对L2使用原58维、最优整体尺度，仅描述多材料/空间响应差，不作为主层新通过门。','','| 目标 | PWM (CW,WW,R,G,B) | 58相对L2中位 |','|---|---|---:|']
for x in C['colors']:lines.append(f"| {x['target']} | {tuple(x['actual_command'][k]for k in ('cw','ww','r','g','b'))} | {f(x['material58_relative_L2_descriptive']['median'])} |")
lines+=['','## 4. 被总quality排除、主块实际合法的10张候选','','这些是开发/候选观察，没有独立确认方差，CI不适用；不能用像素数制造循环置信度。完整四平面统计、原质量与原始路径在primary_secondary_gate_audit.json。','','| 目标 | 标签 | 主层/全局 | Δz (r,b) | 实际PWM (CW,WW,R,G,B) |','|---|---|---|---|---|']
for x in G['primary_valid_global_rejected']:
 rr=next(v for v in S[x['target']]['rows']if v['run']==x['run']and v['capture_id']==x['capture_id']);lines.append(f"| {x['target']} | {x['tag']} | 4/4 accepted / {x['global_quality']} | {vec(rr['dz'])} | {tuple(x['command'][k]for k in ('cw','ww','r','g','b'))} |")
lines+=['','### 五个S100角实际搜索维度','','命令差秩不是光学Jacobian秩；某个命令不在max4095集合时只能作为历史方向，不能认证满幅。','','| 目标 | 物理唯一命令含拒绝 | 命令差秩 | 明确探针通道 |','|---|---:|---:|---|']
for lab in ('0/100','120/100','180/100','240/100','300/100'):
 x=S[lab];lines.append(f"| {lab} | {x['unique_commands_including_rejected']} | {x['measured_command_difference_rank']} | {x['probed_channels']} |")
lines+=['','## 5. 原Ray逆映射与H300算术','','原12点留出Hue绝对误差中位9.25°、最大65.5°；经验P95=49°；SAT最大14pp、经验P95=13.175pp。经验分位数不是置信上界。12/12原反解多解，不能依据这个模型认证H/S百分比。','','H300/S50原正交近似公式重放（不作为真实H/S估计）：']
h=A['H300_S50_report_formula_only'];lines += [f"\nΔz={vec(h['mean_dz'])}；径向={f(h['radial_pp'])}pp；切向={f(h['tangential_z'])}；按原0.0184/°得到{f(h['hue_deg_if_using_report_0p0184'])}°，非原报告0.38°。"]
lines+=['','## 6. LONG：每点只有一对协议观察','','Δ=(strip−Ray)LONG−(strip−Ray)FAST。每状态只有一对，无法从这些值构造有数据支持的未来协议PI；源顺序、period与协议仍未完全分离。','','| 点 | ΔK | Δmired | ΔDuv | Ray ΔK | strip ΔK |','|---|---:|---:|---:|---:|---:|']
for x in E['long_original']['points']:
 d=x['Delta_protocol'];p=x['per_source'];lines.append(f"| {x['point']} | {f(d['cct_K'])} | {f(d['mired'])} | {f(d['duv'])} | {f(p['ray_LONG_minus_FAST']['cct_K'])} | {f(p['strip_LONG_minus_FAST']['cct_K'])} |")
lines+=['','## 7. 环境敏感性：局部点估计，不是确定物理占比','','不同all-off/on快门的归一化、黑/读噪以及仅两个时点使其不能充当全局环境上界；GUIDE13补必要的同设置对照。','','| all-off档 | 对应on样本 | A/on (R,G1,G2,B) | Δz敏感性(r,b) |','|---|---|---|---|']
for x in E['batch1_original']['all_off']:
 r=x['A_over_on_ratio'];z=x['z_on_minus_z_on_minus_A'];lines.append(f"| {x['shutter']} | {x['paired_on_capture']} | {vec([r[k]for k in ('R','G1','G2','B')])} | {vec([z['log_R_over_G'],z['log_B_over_G']])} |")
lines+=['','## 8. 不可输出的伪精度与下一实验对应','','逐Hue最大Ray等效SAT及CI目前均未建立，因为计量模型/搜索资格未完成；不是六个Hue都覆盖0%。各Hue的直接数值已在上表与JSON中，C13-A/B/C负责把计量与可达性问题分开解决。对白光n=1点、单次环境/协议对比不捏造CI；W13-B/D给出确认、转移或有限不采用的终态。','', '确定性错误（计数、权重、内积、代码端点）不需要也不存在采样置信区间。所有建议候选仍待新照片验证。']
(P/'REVIEW_TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
# Current per-Hue state, never fill unknown coverage with zero.
hues=[]
for h in range(0,360,60):
 known=[x for x in C['colors']if x['target'].startswith(str(h)+'/')and x['target']!='0/0']
 hues.append({'hue':h,'tested_confirmed_target_SAT':[int(x['target'].split('/')[1])for x in known], 'max_Ray_equivalent_SAT':None,'max_SAT_ci95':None,'reason':'map_unqualified_and_bounded_search_not_physical_upper_bound','direct_observation_file':'color_confirmations.json','highest_request_search_file':'color_search_and_quality.json','next_experiment':'C13-A local two-column Ray Jacobian + C13-B valid-primary bounded face search + C13-C coverage','S100_primary_window': 'existing_primary_valid_observations_available','do_not_interpret_as_zero_coverage':True})
(D/'hue_coverage_status.json').write_text(json.dumps({'hues':hues,'scope':'Ray INT100, actual strip max4095, camera/block06, FAST','current_direct_confirmed_targets_including_S0':14,'continuous_intervals_certified':[]},ensure_ascii=False,indent=2))
print('Tables written',len(lines),'lines')
