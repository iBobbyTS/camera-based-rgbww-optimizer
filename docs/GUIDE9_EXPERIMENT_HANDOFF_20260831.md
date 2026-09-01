# GUIDE9 实验交接报告

生成日期：2026-08-31

本报告供另一台电脑上的 Codex 接管使用，记录当前仓库能够确认的状态、
已接受的科学结果、可恢复边界和本地实验室连接方法。报告生成时外置实验盘
没有挂载，因此 /Volumes/4T 下的实验根目录只作为保留路径引用，未在本次
交接中读取或改写。

## 1. 当前仓库状态

- 仓库：/Users/ibobby/Projects/WLED-RGBWW
- 分支：codex/guide4-science-path-v3
- HEAD：5bcb0cbcfb76770e3d2eeebca9b5cd49e79dbd30
- HEAD subject：fix(guide9): rebuild probe shutter ledger
- 工作树：报告生成时干净。
- 最近修复：从过滤后的 19 个节点 capture plan 推导实际 shutter keys，避免旧的全局 shutter ledger 在执行前误报不匹配。
- 当前没有可用的 /Volumes/4T 挂载；旧任务的 Terminal/Python PID 80901/80902 在本机已不存在。对应 automation 已删除。这个删除不是实验失败结论，也不是数据删除。

## 2. 当前执行边界

当前任务是 GUIDE9_WHITE70_LOCAL_NODE_CORRECTION 的 19 节点、无历史
local Jacobian 探针批次。它不是新的全局模型训练，也不是 HSI 色域扩展。

目标节点（CCT/GM）为：

~~~
2000/0, 2000/70, 2000/130, 2000/200,
2300/0, 2700/200,
3800/0, 3800/70, 3800/130,
4500/100, 4500/130,
5000/70, 5000/100,
6500/130, 6500/200,
8000/0, 8000/70, 10000/70, 20000/130
~~~

每个节点 6 个观测：一个 Ray reference、一个 strip base，以及四个独立的
非 active channel +256 probe；若 base 通道已经是 4095，该 probe 使用 -256。
预期总量为 19 x 6 = 114 个 formal/physical observations：Ray 19、strip 95、
ambient 0、in-run retry 0。

每个 capture 使用节点自身冻结的 Ray/strip shutter、reset600、dwell120；
不做 solver、不做 global refit、不修改 default LUT。目标根目录是：

~~~
/Volumes/4T/temp/rgbww-optimizer/guide9-white70-no-jac-probes-20260829/20260829-19-node-probes-rerun7
~~~

本次交接前的运行说明给出的身份是：启动时间 2026-08-29 18:39 MDT、
checkpoint 5bcb0cb、wrapper PID 80901、Python PID 80902。由于外置盘
未挂载，不能判断该根是 complete、failed、超时还是被中断。重新挂载后
必须先读 run.json 和失败/清理证据，再决定恢复或新建唯一的新 root；不得
按 PID 不存在就重拍，也不得覆盖旧 root。

## 3. 重新挂载后的首要检查

在另一台电脑上把同一块外置盘挂载到 /Volumes/4T，然后在仓库根目录执行：

~~~
git checkout codex/guide4-science-path-v3
git status --short --branch
ROOT=/Volumes/4T/temp/rgbww-optimizer/guide9-white70-no-jac-probes-20260829/20260829-19-node-probes-rerun7
test -d "$ROOT"
sed -n '1,240p' "$ROOT/run.json"
test -f "$ROOT/failure.json" && sed -n '1,240p' "$ROOT/failure.json" || true
wc -l "$ROOT/captures.jsonl" "$ROOT/physical-returns.jsonl" 2>/dev/null || true
~~~

还要检查 quality*、cleanup*、all-off-*、wrapper-state.json、source-isolation*
和 run.json 中的 accepted_formal_count。完成的判据是：

~~~
run.json status=complete
accepted_formal_count=114
quality pass
source-isolation pass
Python cleanup pass
shell cleanup pass
Ray intensity=0
strip 五通道=0
~~~

如果这些证据成立，只运行一次冻结的 local-probe analyzer，然后按结果为 19
个节点各自生成一个 candidate，进入 paired validation。若 root 是失败或中断，
保留已完成 prefix，只从第一个缺失 capture 恢复；只有无法无歧义恢复时才新建
root。不要重拍已接受 capture，不要把失败/污染根混入分析。

## 4. 已接受的科学进展

### H120/S100、H120/S50、H120/S25

- H120/S100 scale-age 搜索已关闭：scale 2048 的 FAST/LONG 重复性通过，
  scale 4095 的 FAST 通过但 LONG 失败，交互分数 11.1009；未把差异命名为
  特定物理热因果。
- H120/S50 为 stable_nonfaithful，H120/S25 没有得到 faithful lower endpoint。
- 13-node HSI grid、boundary、Gate-6、P8 和 LUT 安装均保持锁定。

### H0/S0 与 H300

- H0/S0 的 Ray bracket 和 strip repeatability 通过，分类为
  H0_S0_stable_nonfaithful；这不是物理 gamut 结论。
- 一次 H300 诊断是在 Ray 断电时完成的，作为历史 invalid-condition evidence，
  不得作为科学输入。Ray 恢复供电后重新完成的诊断为
  R-C / H300_S100_reference_repeatability_unresolved，pair score
  20.6931277037 > 9.6325691794。
- H300/S50 Batch 1 的 Ray bracket 通过；最低 direct-score command 是
  CW192/WW4095/R2495/G0/B2559，direct score 1659.5267137795。
- H300/S50 best-repeat 的 Ray bracket 和 strip repeatability 通过，但 direct
  score 仍约 1659.86/1659.25，分类为 H300_S50_stable_nonfaithful。

### 白光路线

- White12 representative：24/24 采集和 cleanup 通过，只有 5600K/GM200
  通过严格 paired white-point gate，11 个节点进入 local correction。
- 保留历史 Jacobian 的节点经过局部校正和二次确认后，已有 5 个节点通过。
- 原 70-node FAST-DIRECT 的三个 root 离线合并为恰好 140 个唯一 capture
  (000..139)；冻结分析为 11/70 pass、59/70 需要 node-local correction。
- 无历史 Jacobian 的旧 36-observation 路线曾因 Ray 断电中断：前 24 条 accepted
  prefix 可恢复；capture 25 的 5600/GM0 Ray reference 为 near-noise，后续
  诊断也为 dark RAW。rejected dark/diagnostic frames 不得进入白光分析。Ray
  供电恢复后，只能补齐缺失 block，不能重拍前 24 条。

## 5. 已知工程问题及恢复边界

此前无 Jacobian 启动尝试出现过三类工程问题，均不是科学结论：

1. 旧 wrapper 在空 captures.jsonl 上先做 post-capture 验证，触发
   FileNotFoundError；已在 9a5cffd 修正。
2. 复用非空 run directory 触发 FileExistsError；不可恢复的尝试必须使用
   唯一的新 run name，不能覆盖旧 root。
3. rerun5/rerun6 在过滤后的 19 节点计划上仍使用全局 shutter ledger，触发
   PermissionError: thermal diagnostic frozen shutters differ from experiment capture steps；
   HEAD 5bcb0cb 已改为由实际过滤后的 capture steps 重建 ledger。

正确处理方式是：保留 root 和日志，在当前工作树修普通实现，通过有意义的行为
测试，再恢复可恢复 prefix 或启动唯一新 root。不要把 selector、重试次数、review
数量或旧 automation 当作科学停止门槛。

## 6. Amaran Desktop / Ray120c 连接方法

### 6.1 软件安装和物理配对

1. 在新 Mac 安装与芯片匹配的 amaran Desktop App。官方页面提供 Apple
   Silicon 和 Intel macOS 下载项：
   https://eu.amarancreators.com/pages/amaran-app-download
2. 启动 Amaran Desktop，用邮箱验证码或已有 Sidus Link 账号登录。
3. 给 Ray120c 接通电源，打开 macOS Bluetooth；如设备被其他主机占用，先在
   Ray120c 菜单执行 Bluetooth Reset/BT Reset，再在 Desktop 的 Device
   Management 点击 Add Devices，选择 Ray120c 并确认配对。
4. 在 Desktop 设备列表确认目标灯具在线。Desktop 负责 Bluetooth；仓库 Python
   不直接连接 Bluetooth。

官方配对帮助明确要求打开 Bluetooth、必要时执行 BT Reset、点击 Add Devices、
选择灯具并确认配对：
https://help.amarancreators.com/en/amaran-desktop-app/pairing-guide

### 6.2 本仓库使用的本地 API

仓库连接的不是 Ray 的局域网地址，而是本机 Amaran Desktop 暴露的 OpenAPI
v2 WebSocket：

~~~
URL      ws://127.0.0.1:33782
node_id 40165-560387
client_id 1
~~~

src/camera_based_rgbww_optimizer/control/ray120c.py 是唯一 Ray 控制 owner，
支持 set-cct/get-cct、set-hsi/get-hsi、set-rgb/get-rgb 和 node-config。
代码为每个请求生成 AES-256-GCM token；默认共享协议值已经在代码中冻结并通过
测试，报告不重复写出 secret。

如果新版本 Desktop 使用不同端口或节点 ID，只在运行进程环境中覆盖：

~~~
export AMARAN_WS_URL=ws://127.0.0.1:33782
export AMARAN_NODE_ID=40165-560387
export AMARAN_CLIENT_ID=1
export AMARAN_TIMEOUT=3
~~~

可选的 AMARAN_OPENAPI_SECRET 只能作为进程环境变量提供，不能放进 argv、Git、
日志、JSON 或交接报告；没有明确需要时不要设置它。当前 owner 不从项目 .env
读取这个 Ray secret，也不会把它打印出来。

### 6.3 只读连接验证

先确认 Desktop 进程监听端口（nc 只做端口级检查，不等同于协议成功）：

~~~
lsof -nP -iTCP -sTCP:LISTEN | rg -i 'amaran|33782'
nc -vz 127.0.0.1 33782
~~~

然后在仓库根目录执行两个只读请求：

~~~
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c node-config
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c get-cct
~~~

成功标准是 WebSocket 握手成功、返回对应 request_id、响应 code 为 0，且
get-cct 返回的节点与 Desktop 当前选中的 Ray120c 一致。失败时先检查 Desktop
是否保持运行、设备是否在线、节点 ID 是否正确、端口是否改变；不要直接改协议，
也不要把 API command success 当成物理发光证据。

### 6.4 控制语义和清理

- CCT/G-M 使用 set-cct；CCT 范围 1800..20000 K，原始 GM 范围 0..200，
  强度原始范围 0..1000。
- HSI 使用 set-hsi；实验中的 H120/S100 表示 hue=120、sat=100，但不能
  绕过 GUIDE 冻结的 shutter、dwell、source-isolation 和 capture 计划。
- 每次正式 Ray capture 前必须保存 set response、立即 readback、post-capture
  readback 和强度证据；strip capture 前必须保存 Ray intensity 0 的 readback。
- 手动中断或异常后执行：

~~~
.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --ray-timeout 5
~~~

该命令同时把 ESPHome RGBWW 五通道设为 0，并把 Ray intensity 设为 0。清理证据
和最后一次独立 readback 要保存在对应 run root；不能只凭 Desktop 界面显示状态
声称已经关闭。

## 7. 另一台电脑的项目准备

~~~
cd /Users/ibobby/Projects/WLED-RGBWW
.venv/bin/python -m pip install -e .
.venv/bin/python -m camera_based_rgbww_optimizer.control.ray120c node-config
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote health --json
.venv/bin/python -m camera_based_rgbww_optimizer.control.camera_remote config --json
~~~

还需要安装仓库文档列出的系统工具：Homebrew gphoto2、exiftool 和 dcraw_emu。
正式相机采集继续使用 remote camera bridge，而不是把本地 gphoto2 当成新的正式
后端；相机 bridge 的 base URL/token 只放在进程环境或本地 .env，不要提交。

连接检查通过后，Codex 应回到第 3 节先检查 rerun7；不要因为看不到旧 PID 就
重启，也不要在没有读取 run.json、cleanup 和 source-isolation 证据前运行 analyzer。

## 8. 当前锁定项

在 19-node probe analyzer 和后续 paired validation 完成前，保持：

- 不做 global refit；
- 不改 default LUT；
- 不重拍或池化成功的历史 capture；
- 不使用断电 Ray 或缺少 capture-level Ray-zero evidence 的污染 strip frames；
- 不进入 interpolation holdout、13-node HSI grid、full boundary、Gate-6、P8 或
  LUT 安装；
- 不通过放宽 near-noise、clipping、58-feature、covariance 或 coverage 门槛让节点
  通过；
- 不把 API command success 当成物理发光证据，必须结合 capture-bound readback、
  RAW quality 和 source-isolation evidence。

## 9. 接管完成条件

另一台电脑的 Codex 完成以下检查后，才算接管成功：

~~~
repository checkout and HEAD recorded
Amaran Desktop installed, logged in and Ray120c paired
local WebSocket node-config/get-cct read-only checks pass
camera_remote health/config checks pass
external disk mounted and rerun7 root inspected
run status and accepted-capture count classified
Ray/strip final zero and Git status recorded
next action selected without pooling or duplicate capture
~~~

本报告只提供交接上下文，不授权刷写固件、远程部署、破坏性硬件修改或扩大
实验范围。普通的、当前 GUIDE 已选定的灯光开关和相机采集仍按项目 AGENTS.md
的低风险边界执行；高风险动作仍需 Human 明确授权。

