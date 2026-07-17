# 范围、冻结基线与当前状态

## 1. 当前仓库状态

- 仓库：`/Users/ibobby/Projects/WLED-RGBWW`
- 分支：`main`
- 审计时 `HEAD`：`ecf47d722e6f9e7c2c09b0d7fd3e3429e7d38ad5`
- 工作区：dirty；包含 P1-P7 的计划、代码、测试和文档，不应把本审计理解为只描述 `HEAD`。
- 当前阶段：Stage 6，P7 离线实现完成、等待纠偏和真实灯带 pilot。
- 默认 `config/white/white-lut.json` 仍为旧 4x3 LUT，未被本轮工作覆盖。

当前工作区中的未提交工作较大。开始下一轮实拍前，应在纠偏修复、完整测试、`git diff --check` 和 CodeGraph sync 后形成一个明确代码检查点；本审计本身不授予提交或安装权限。

## 2. 固定观察者和可声明范围

本项目当前只证明以下固定链路下的相机观察者匹配：

- Canon EOS R6 Mark III；
- 当前固定镜头、机位、色卡和空间几何；
- Canon CR3 原生 Bayer；
- 不做 demosaic、白平衡、gamma 或自动增亮；
- `R/G1/G2/B` 四平面独立；
- Ray120c 作为相对参考光源；
- 灯带与 Ray 分时拍摄，不同时亮。

当前结果不能声明：

- 光谱恢复或光谱仪等级 CCT；
- CRI、TLCI、SSI、TM-30 一致；
- 人眼绝对同色；
- 其他相机或其他拍摄几何通用；
- Ray100 与 strip100 的绝对照度一致；
- HSI/RGB 模式共享同一颜色端点。

## 3. 冻结输入

### 3.1 新实验点位

- 路径：`config/location/locations-20260714-211759.json`
- SHA-256：`21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`
- 所有新实拍必须使用该文件；旧点位仅用于复算对应历史 CR3。

### 3.2 Remote 相机

- 新实验只使用 `RemoteCameraBackend` 和 `r6-camera-bridge`。
- API 文档：`http://ibobby-rpi-4.local:8088/v1/API.md`
- URL/Token 由项目脚本读取 `.env`。
- 执行模型和文档不得读取、展开、打印或持久化 `.env` 内容。
- 本地 gphoto2 只保留兼容和单元测试用途。

### 3.3 RAW 观察者

- 配置：`config/camera/raw-observer.json` v2。
- 响应模型：identity。
- 曝光包络：每源自动曝光的 `1.0x..1.25x`。
- 四平面：`R/G1/G2/B`，`combine_green=false`。
- clipped/nonfinite 不允许；near-noise 上限 `0.05`；每平面至少 29000 个有效像素。
- 弱信号只能在冻结包络内重拍，不能通过放宽阈值或删除 feature 保留。

### 3.4 P2 五通道基底

- 实验：`/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935`
- `basis-analysis.json` SHA-256：`5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1`
- 用途：只生成闭环初值；不得作为最终全局真值。

### 3.5 Ray HSI 流形

- 配置：`config/hsi/ray-hsi-manifold.json`
- 审计时 SHA-256：`20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34`
- Gate-5：`full_periodic_2d_HB`
- 运行目录：`/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/p6-ray-hsi-remote-20260717-0403-retry1`

### 3.6 既有白光候选

- 路径：`/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`
- 状态：当前最佳 white-only 70 点候选。
- 限制：只有最高风险 10 点完成最终 60 秒 off/on 独立复测，不能声称最终 70/70 独立验证。
- 策略：保留外置文件，不覆盖默认 LUT。

## 4. 强制安全合同

后续任何真实运行必须继续满足：

1. 同一时间只有 Ray、strip 或 ambient 之一；
2. 相机 trial 和正式 capture 复用同一个 remote backend；
3. 每个 run 使用新目录，不覆盖失败样本；
4. CR3 和 recorded exposure 必须保留；不保存 `.npy`；
5. Python `finally` 和 shell `trap` 都调用双灯关闭；
6. 运行完成或失败后都保留 `all-off-python.json`、`all-off-shell.json`；
7. 高输出运行必须有明确目标集合、上限和恢复路径；
8. 不在后台并发启动第二个相机或灯具任务。

