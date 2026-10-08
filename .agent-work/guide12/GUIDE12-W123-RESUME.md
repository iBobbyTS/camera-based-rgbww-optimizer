# GUIDE12 W12-3 启动指令（备用，用户说"启动"即可复制粘贴）

## 一句话版

> 启动 W12-3：执行 `.agent-work/guide12/GUIDE12-W123-RESUME.md` 里的启动流程。

## 完整版（直接粘贴给助手）

> 继续 GUIDE12 W12-3 插值留出实验。按
> `.agent-work/guide12/GUIDE12-W123-RESUME.md` 执行：
> 1. 三设备只读探测（ESPHOME/Ray node-config/相机桥 health）；
> 2. Ray 出光预检（CCT 5600/gm100 @20% 约 6 秒，1 帧 RAW 域判读，max>2000 为通过；
>    上次断电后 API 解耦的教训）；
> 3. 确认 Git 工作树干净（HEAD 应为 bf7edce 或其后代）；
> 4. 启动（后台 + 启动日志 + 三次间隔 65 秒活性检查）：
>    ```
>    cd C:/Users/iBobb/Projects/WLED-RGBWW && .venv/Scripts/python.exe -m camera_based_rgbww_optimizer.optimization.measure_guide12_w123 --include-s0-reference --output-dir D:/rgbww-optimizer/guide12-w123 --run-name formal-w123-holdout --execute --allow-device-control > D:/rgbww-optimizer/guide12-w123/formal-w123-holdout-launch.log 2>&1
>    ```
> 5. 完成后（预计 ~8.5 小时）：核验 run.json/quality.json，跑离线分析
>    （同点 strip−Ray 误差 + 20 请求判定），写结果文档并提交。

## 背景状态（2026-10-08 本机时间 11:50 冻结）

- W12-3 已全部实现并提交（`bf7edce`）：冻结插值函数（mired×raw-GM 双线性 +
  满幅投影 + 整数化次序冻结）、20 个非节点请求坐标（含 5350/105、6050/160
  覆盖历史失败结构）、43 帧计划（S0-C 参考 + 18 对 + 2 冷端三明治）、
  CLI/运行器/校验器/34 项行为测试全过。
- 本次按用户指令在初始冷却期终止（零捕获），三设备确认零态
  （Ray intensity 0、灯带全零 generation 3），残根已删，工作树干净。
- 剩余路由：W12-3 运行+分析 → W12-4 LONG 复验（16+8 帧）→ C12-2..5 →
  最终证据包。W12-2 可选纠偏分支（12 节点预算）默认失败区收口。
- S0 会话表：A、B 已采；C 由本运行的 `--include-s0-reference` 搭载。
