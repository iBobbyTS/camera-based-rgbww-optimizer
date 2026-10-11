# GUIDE12 C12-3 暂停与恢复指令（2026-10-11 09:05 本机时间冻结）

## 一句话版

> 继续 C12-3：执行 `.agent-work/guide12/GUIDE12-C123-RESUME.md` 里的恢复流程。

## 暂停时状态（已全部落盘）

- **C12-2 完整收官**（提交 `56dde57`）：13/13 请求判定——8 合格
  （S0 + 全部五 S50 + 黄 H60/S100），5 gamut_limited（红/绿/青/蓝四角
  径向饱和度缺口；品红 H300/S100 切向锁死）。结果文档：
  `.agent-work/guide12/GUIDE12-C122-RESULT-20261009.md`。
- **C12-3 已实现未采数**：S25 六请求扩展提交于 `c05caa0`
  （Ray 快门 P6 (hue,20) 锚点同规则转移；9 测试全过）。
  H0/S25 块 1 于 09:00 启动后按用户暂停指令终止：**0 捕获**、
  残根已删、设备已确认零态（Ray intensity 0；灯带 kill 时有命令
  驻留残留 r4095，已手动 all_off 清零并读回验证 generation 607）。
- Git HEAD `c05caa0`，工作树干净。

## 恢复流程（用户说"继续"即可）

1. 三设备只读探测（Ray get-cct / 相机桥 health / ESPHome 状态订阅）。
2. 确认 Git 工作树干净（HEAD 应为 `c05caa0` 或其后代）。
3. 启动 H0/S25 块 1（**runner 独占一条后台命令**，候选 JSON 已在
   `D:/rgbww-optimizer/guide12-c122/derived/c122-h0s25-block1-candidates.json`）：
   ```
   cd C:/Users/iBobb/Projects/WLED-RGBWW && .venv/Scripts/python.exe -m camera_based_rgbww_optimizer.optimization.measure_guide12_c122 --hue 0 --sat 25 --block-index 1 --candidates-json D:/rgbww-optimizer/guide12-c122/derived/c122-h0s25-block1-candidates.json --execute --allow-device-control --output-dir D:/rgbww-optimizer/guide12-c122 --run-name formal-c122-h0s25-b1 > D:/rgbww-optimizer/guide12-c122/formal-c122-h0s25-b1-launch.log 2>&1
   ```
4. 三次间隔 65 秒活性检查后交看门狗（后台任务完成通知）。
5. 之后按 C12-2 成熟流程逐请求推进：H0/S25 → H60/S25 → H120/S25 →
   H180/S25 → H240/S25 → H300/S25（探针→步进/内插→确认 ×3，
   判定用径向/切向二维门；每个请求 ≤8/12 唯一命令）。

## 剩余路线

C12-3 六个 S25 → 每 Hue 覆盖表（58 层、s_best_tested、
validated_samples 语言）→ C12-4 周期模型 + 10 新留出（30+≤18 帧）→
C12-5 收口 → GUIDE12-COMPLETE-PROCESSED-EVIDENCE zip。
W12-2 可选纠偏分支（12 节点预算）仍待用户/Advisor 决定。
