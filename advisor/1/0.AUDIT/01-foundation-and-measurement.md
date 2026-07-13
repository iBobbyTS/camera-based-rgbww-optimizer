# 基础设施与测量链审计

## 1. 初始控制方案：stock WLED

项目最初把 GL-C-211WL 当作 stock WLED `0.15.1` 五通道模拟灯使用。设备报告总线类型 `TYPE_ANALOG_5CH`，GPIO 为 `[19,18,17,16,4]`，PWM 频率 `19531Hz`，但 stock WLED API 实际暴露的是 `RGB + W + CCT`，不是任意独立 `RGB+WW+CW`。

早期评估过四条路径：

| 路径 | 尝试/判断 | 结论 |
| --- | --- | --- |
| stock WLED JSON | 用 `W=WW+CW`、`CCT=255*CW/(WW+CW)` 反算 | 只能表达受约束的白通道组合，命令仍是 8-bit，不适合完整五维优化 |
| Tasmota | 研究 `SetOption68` 和 PWM 能力 | 没有同设备实机成功证据，控制模型也不如专用 API 清晰 |
| 自定义 ESP-IDF | 评估直接 LEDC 和自建 API | 精度最高，但首轮刷机与恢复风险更高，未作为第一步 |
| ESPHome | 采用五路 LEDC + 自定义 Native API action | 成为正式方案 |

## 2. ESPHome 五通道方案

最终固件选择 ESP32 LEDC `19531Hz`、12-bit 码值 `0..4095`，通过 `set_rgbww_12bit` 接受五个整数，并提供 `all_off`。输入整数在固件内钳制后用 `value/4095.0f` 设置 duty；没有使用 float16，因为它无法精确表示全部 12-bit 整数。

重要尝试和结果：

- No-WebUI 固件完成编译、刷写和实机验证：可启动、联网、响应 Native API `6053` 和 OTA `3232`。
- WebUI 版本编译成功，但历史记录中没有硬件刷写验证；端口 80 不通并不表示设备离线，可能只是运行 No-WebUI 版本。
- 固件内置普通 Wi-Fi、fallback AP、captive portal、OTA 和 API 加密配置；真实密钥只存在忽略文件。
- 早期通道测量发现白通道 GPIO/命名映射需要交换，提交 `ce9362b` 修正 GPIO；合并响应数据时保留 `cw -> ww`、`ww -> cw` 的来源别名，避免静默篡改历史数据。
- 项目后来把设备名从 `wled-bedroom-rgbww` 统一为 `bedroom-rgbww-strip`，Python 包也从根目录脚本迁入 `src/camera_based_rgbww_optimizer/`。

当前 Python 调用顺序固定为 `light(cw, ww, r, g, b)`，再映射到 ESPHome 的 `cold_white, warm_white, red, green, blue`。全零命令调用 `all_off`，不是普通非零 service。

## 3. Ray120c 控制

Ray120c 使用 Amaran Desktop OpenAPI v2，经 `ws://127.0.0.1:33782` 控制。已确认的命令范围：

- CCT：`1800..20000K`
- intensity raw：`0..1000`，`1000` 为 100%
- GM raw：`0..200`，`100` 为中性
- HSI/HSL：Hue `0..360`、Saturation `0..100`
- RGB：每通道 `0..255`

早期曾把 GM 误认为只需较窄或单侧范围，后来明确正式白光必须覆盖完整 `0..200`。端点与 LUT 实验均固定 Ray 100% 亮度。

## 4. Canon RAW 采集链

2026-06-05 验证的主机链为：

- Canon EOS R6 Mark III，USB PTP
- `gphoto2 2.5.32` / `libgphoto2 2.5.34`
- RAW/CR3，ISO 100，光圈 4，快门自动调整
- `rawpy`/LibRaw 线性 16-bit camera RGB

测量解码固定关闭相机/自动白平衡、自动增亮和非线性 gamma。LibRaw 已处理 RAW 黑白电平，项目不再二次减黑。

自动曝光经历的主要改进：

1. 最初只按整图最大值调整，跨 Ray 高亮和灯带低亮场景不稳定。
2. 增加快门候选、饱和回退、暗部提升、拍摄次数上限和失败时保留最佳可用帧。
3. 增加基于定位 JSON 的色卡区域测光，避免背景和标尺主导曝光。
4. 删除试拍文件，只保留最终 RAW；正式白光测量中的 `.npy` 解码也在统计后删除。
5. Ray 与灯带改为两套独立快门缓存。Ray 通常需要约 `1/2500..1/3200`，灯带通常更慢；不能从当前相机状态或另一光源的快门继续。
6. macOS `ptpcamerad`/`icdd` 会抢占 PTP。包装器现在对 USB claim 和 kernel-driver-detach 错误杀掉本用户 Image Capture 进程并重试一次。

2026-06-07 的首次五分钟色温观察脚本成功完成控制窗口和最终双灯关闭，但相机记录在 `1800/5600/20000K` 处因 `CaptureSettings` 缺少 `to_jsonable` 报错，因此它证明了设备调度/清理，不构成有效色温数据。

## 5. 色卡定位与可视预览

定位工具从简单 UI 演进为本地 Web UI，并先后尝试：

- 手工多边形；
- OpenCV ColorChecker/MCC；
- 网格线和投影回退；
- 自动检测后人工修正；
- 保存标准 24 色块名称和角色。

曾出现两个实质问题：

1. Picker 显示的是线性 `.npy` 预览，而 Checker 走 `dcraw_emu`，两者视觉不一致。
2. OpenCV 或回退检测返回越界四边形，UI 仍直接显示。

第一轮修复统一使用 `dcraw_emu`，但 Canon CR3 的 full RAW 重建明显偏洋红；最终改为默认提取 CR3 内嵌 `JpgFromRaw`，使 Finder、相机和 UI 视觉一致，`dcraw_emu` 只作为显式回退。所有自动检测结果在显示前检查边界。

当前正式定位文件：`config/location/locations-20260709-012045.json`。用户确认前一日色卡定位没有问题，后续手拍 RAW 也继续使用该文件。

## 6. 五通道响应和 code-duty 曲线

通道测量流程在全关环境拍摄固定 ambient 帧，再从 code `4095` 向下扫到 `8`，按快门秒数归一化并减 ambient。两次来源 run 合并后得到：

- 五个通道；
- 每通道 19 个 code 点；
- 总计 95 条测量；
- 完整覆盖 `4095,3072,2048,...,12,8`；
- 生成 `config/channel/code-duty-curve.json`。

第一次 CW 来源 run 的 JSON 状态仍是 `running`，但其有效样本在确认通道别名后被合并；第二次 WW/R/G/B run 为 `complete`。因此合并文件可用于当前线性化，但审计上不能把两个源 run 都称作完整结束。

控制模块默认把输入视为目标线性亮度 code，并通过测得的 code-duty 曲线反查 PWM duty。用户后来要求 CCT 轴直接按 Kelvin 插值；当前白光 LUT 控制在 CCT 上做 Kelvin 线性插值，GM 仍做线性插值，强度百分比再线性缩放五通道命令。

## 7. 安全机制的演进

早期设备脚本仅依赖单层退出逻辑，实际运行中多次需要手工确认灯是否关闭。最终形成以下约束：

- Python 测量函数在 `finally` 中关闭 Ray 和灯带。
- shell runner 使用 `trap cleanup EXIT HUP INT TERM` 再关闭一次。
- `all_off` 即使一个设备失败也继续关闭另一个设备。
- Ray 当前读数异常时，off 命令使用合法 CCT/GM fallback。
- 专门的 `white_lut` 应用命令是唯一有意保持灯带亮起的白光工具。
- 最终实机优化后再次显式调用 `all_off`，并检查无残留优化进程。

