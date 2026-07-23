# Remote Camera Controller

Canon EOS R6 Mark III 远程相机 bridge 的源码归档与离线验证子项目。

当前归档与远端 `/home/ibobby/r6-camera-bridge` 的已部署源码同步。

## 内容

- `r6_camera_bridge.py`：Flask/Gunicorn HTTP bridge，运行在连接相机的 Raspberry Pi 上。
- `r6_timing.py`：best-effort gphoto2 时序 metadata、校验与 Tier A/B/C 估计逻辑。
- `tests/`：不访问真实相机、灯光设备或项目 `.env` 的离线 fake-gphoto2 测试。
- `deploy/r6-camera-bridge.service`：远端 systemd 服务单元归档。
- `docs/`：API、gphoto2 能力边界和离线时序样例。

这不是主项目 Python package 的 import 路径；它保存的是远端 bridge 服务本身。主项目的相机调用仍通过 `camera_based_rgbww_optimizer.control.camera_remote` 访问 bridge API。

## 远端运行边界

- 目标主机：`ibobby-rpi-4.local`
- 远端服务目录：`/home/ibobby/r6-camera-bridge`
- 服务端口：`8088`
- `POST /v1/capture` 保留同步 CR3 二进制兼容接口。
- `POST /v2/capture` 返回同步 `multipart/mixed`，包含 `remote_capture_result_v2` metadata 和 CR3。
- 相机端固定 RAW、拒绝 Bulb；下载成功后不保留相机卡原片。
- CR3 仅在远端 `/run` 临时目录短暂存在；服务不持久化 CR3 或应用请求日志。
- CR3 曝光时间只信任 ExifTool 读取的 Canon MakerNote `Canon:ExposureTime`；该字段或 ExifTool 不可用时返回 `unavailable`，不回退到标准 EXIF。
- 时序字段属于 bridge monotonic 时钟域；当前实现只声明 best-effort，不声明绝对 exposure-start，也不会改变 P7/TD-A 门禁。

## 离线验证

需要 Python 3.13 环境和 [requirements.txt](requirements.txt) 中的依赖（远端服务的 `.venv` 已满足）：

```bash
cd remote_camera_controller
python -m pip install -r requirements.txt
python -m compileall -q r6_camera_bridge.py r6_timing.py tests
python -m unittest discover -s tests -v
```

离线测试覆盖 v1 兼容、v2 multipart、Canon MakerNote 权威字段、缺失字段 fail-closed、时序层级、顺序/单位校验、CR3 hash/ID 关联和敏感信息过滤。

## 文档

- [API 文档](docs/API.md)
- [gphoto2 能力矩阵](docs/GPHOTO2_EVENT_CAPABILITY.md)
- [离线时序样例](docs/BEST_EFFORT_TIMING_SAMPLE.json)

不要在本目录保存真实 CR3、token、`.env` 或运行日志；测试也不应调用真实相机。
