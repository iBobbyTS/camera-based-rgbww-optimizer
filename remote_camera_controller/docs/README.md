# Remote Camera Controller 文档

本目录记录 Raspberry Pi 上 Canon R6 III bridge 的接口和能力边界。

## 文档索引

- [API.md](API.md)：`/health`、`/v1/config`、`/v1/capture`、`/v2/capture` 的请求/响应契约。
- [GPHOTO2_EVENT_CAPABILITY.md](GPHOTO2_EVENT_CAPABILITY.md)：当前 gphoto2/libgphoto2 CLI 路径可安全声明的事件矩阵。
- [BEST_EFFORT_TIMING_SAMPLE.json](BEST_EFFORT_TIMING_SAMPLE.json)：不接触相机的 Tier B metadata 样例。

## 语义边界

当前 bridge 提供的是 `best_effort_gphoto2` 时序。`capture_result_path_observed`、download、进程返回和 CR3 本地观察时间都不会被伪装成 shutter-open 或绝对 exposure-start。recorded exposure 只接受 Canon MakerNote `Canon:ExposureTime`；标准 EXIF 不作为 fallback。没有 driver/camera event 证据时，最高只能是带可信 recorded exposure 的 Tier B `weak_estimate`；缺失必要事件或 Canon 曝光时间时返回 Tier C `unavailable`。

metadata 不包含 token、`.env`、相机序列号或远端内部文件路径。真实设备样本需要单独的人类/Planner 授权，本归档不以离线样例解锁 P7 或 TD-A。
