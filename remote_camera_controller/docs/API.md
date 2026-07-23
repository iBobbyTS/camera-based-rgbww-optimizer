# Canon EOS R6 Mark III Camera Bridge API

服务地址：`http://ibobby-rpi-4.local:8088`

除 `GET /health` 和 `GET /v1/API.md` 外，接口都需要 Bearer Token。本文件不包含实际 Token；请从调用端安全注入：

```http
Authorization: Bearer <R6_CAMERA_TOKEN>
```

接口完全同步：没有任务创建、轮询、状态查询或单独下载接口。所有拍摄固定为 RAW，禁止 Bulb，下载成功后不在相机卡上保留原片；树莓派只在 `/run` 临时目录短暂保存 CR3，读入内存后立即删除，也不持久化应用请求日志。

## `GET /health`

无需认证。用于确认 HTTP 服务可达。

```json
{"status":"ok"}
```

## `GET /v1/API.md`

无需认证。返回本 API 文档，响应带 `Cache-Control: no-store`。

## `GET /v1/config`

读取相机当前 ISO、光圈、快门和格式，以及相机当时暴露的可选值。

```bash
curl -H "Authorization: Bearer $R6_CAMERA_TOKEN" \
  http://ibobby-rpi-4.local:8088/v1/config
```

响应示例：

```json
{
  "iso": {"current": "100", "choices": ["Auto", "100", "125"]},
  "aperture": {
    "current": "implicit auto",
    "choices": ["Unknown value 0c00", "implicit auto"]
  },
  "shutter_speed": {"current": "1/125", "choices": ["1/60", "1/125", "1/250"]},
  "image_format": {"current": "RAW", "fixed": "RAW"}
}
```

`choices` 是当前机身、镜头和拍摄模式实际提供的值。调用方必须使用其中的精确字符串。

## `POST /v1/capture`

兼容接口。可选地设置 ISO、光圈和快门，然后在同一个请求内拍摄；成功时直接返回 CR3 二进制数据。

```bash
curl --fail --output photo.cr3 \
  -H "Authorization: Bearer $R6_CAMERA_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "iso": "100",
    "aperture": "implicit auto",
    "shutter_speed": "1/125"
  }' \
  http://ibobby-rpi-4.local:8088/v1/capture
```

成功响应仍为：

```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="r6-YYYYMMDD-HHMMSS.cr3"
Cache-Control: no-store
X-Capture-ID: <uuid>
X-Request-ID: <uuid>
```

## `POST /v2/capture`

使用与 `/v1/capture` 完全相同的可选 JSON 设置并立即拍摄，但成功响应为 `multipart/mixed`：第一部分是 `remote_capture_result_v2` JSON metadata，第二部分是 CR3。两部分通过同一个 `capture_id`、`request_id`、CR3 SHA-256 和字节数关联。

```bash
curl --fail --output capture.multipart \
  -H "Authorization: Bearer $R6_CAMERA_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"iso":"100","aperture":"implicit auto","shutter_speed":"1/125"}' \
  http://ibobby-rpi-4.local:8088/v2/capture
```

响应头：

```http
Content-Type: multipart/mixed; boundary=<boundary>
Cache-Control: no-store
X-Capture-ID: <uuid>
X-Request-ID: <uuid>
X-Capture-Metadata-Schema: remote_capture_result_v2
```

metadata 核心结构：

```json
{
  "schema": "remote_capture_result_v2",
  "capture_id": "...",
  "request_id": "...",
  "timing_quality": "best_effort_gphoto2",
  "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
  "cr3": {
    "sha256": "...",
    "byte_count": 123456,
    "content_type": "image/x-canon-cr3"
  },
  "gphoto2": {
    "driver_event_type": null,
    "event_sequence": [],
    "request_received_monotonic_ns": 0,
    "capture_call_started_monotonic_ns": 0,
    "capture_call_returned_monotonic_ns": 0,
    "camera_event_observed_monotonic_ns": null,
    "file_added_observed_monotonic_ns": null,
    "download_started_monotonic_ns": 0,
    "download_completed_monotonic_ns": 0,
    "cr3_saved_observed_monotonic_ns": 0,
    "clock_domain": "bridge_monotonic"
  },
  "recorded_exposure": {
    "seconds": 0.0078125,
    "source": "Canon:ExposureTime",
    "status": "recorded"
  },
  "exposure_start_estimate": {
    "timestamp_monotonic_ns": 0,
    "clock_domain": "bridge_monotonic",
    "method": "gphoto_capture_return_minus_recorded_exposure",
    "status": "weak_estimate",
    "uncertainty_ms": null,
    "uncertainty_basis": "unknown"
  },
  "network_observation": {
    "request_id": "...",
    "response_or_event_round_trip_ms": null,
    "uncertainty_ms": null,
    "uncertainty_basis": "unknown"
  }
}
```

### 时序语义

- 所有 `*_monotonic_ns` 都属于 `bridge_monotonic` 时钟域，不能直接和客户端 monotonic 时钟比较。
- `recorded_exposure` 只以 ExifTool 读取的 Canon MakerNote `Canon:ExposureTime` 为权威；标准 EXIF `ExposureTime`、请求快门值和 bridge 自行扫描到的 TIFF 字段都不会作为 fallback。
- ExifTool 不可用、Canon MakerNote 缺失或数值无效时，`recorded_exposure` 返回 `{"seconds":null,"source":null,"status":"unavailable"}`，并禁止用该曝光时间生成 estimate。
- 明确的 driver/camera `file_added` 或 `capture_complete` event 加上可信 recorded exposure 才能生成 `gphoto_event_minus_recorded_exposure`；它仍是 `estimated_not_absolute`。
- 当前 CLI 兼容路径观察到 capture result return、且 CR3 有 recorded exposure 时，只生成 `gphoto_capture_return_minus_recorded_exposure`，状态是 `weak_estimate`。
- 只有 request/download/write 时间、recorded exposure 缺失、或顺序不可信时，estimate 为 `null` / `unavailable`。
- request、HTTP response、download complete、文件名或 CR3 写盘时间绝不会被当成 exposure-start。
- bridge 无法从服务端单独测出完整网络 RTT，因此当前 RTT 和 uncertainty 均为 `null`，不会写入乐观常数。
- 新 metadata 没有证明绝对 exposure-start，不会把 `actual_exposure_start_capability` 设为 true，也不会自动改变 P7/TD-A 的门禁。

## 拍摄请求字段

`/v1/capture` 和 `/v2/capture` 请求体字段均为可选字符串：

| 字段 | 含义 |
| --- | --- |
| `iso` | 必须精确匹配 `GET /v1/config` 的 `iso.choices` |
| `aperture` | 必须精确匹配 `aperture.choices` |
| `shutter_speed` | 必须精确匹配 `shutter_speed.choices`，且禁止 `Bulb` |

空请求体也可以拍摄：服务保留相机现有曝光设置，但仍强制 RAW。

## 错误响应

错误体统一为：

```json
{"error":"错误代码"}
```

| HTTP | 错误代码 | 含义 |
| --- | --- | --- |
| 400 | `bulb_not_allowed` | 请求试图设置 `Bulb` |
| 400 | `invalid_iso` / `invalid_aperture` / `invalid_shutter_speed` | 值不是当前相机可选项，或字段类型不正确 |
| 400 | `unknown_setting` | 请求包含不支持的设置字段 |
| 401 | `unauthorized` | 缺少或错误的 Bearer Token |
| 409 | `camera_busy` | 已有相机操作正在进行 |
| 409 | `camera_in_bulb_mode` | 相机当前为 Bulb，且请求没有提供非 Bulb 快门值恢复 |
| 500 | `camera_capture_internal_error` / `capture_metadata_invalid` | capture 或 metadata 内部失败 |
| 502 | `camera_config_failed` / `camera_capture_failed` | 相机通信、配置或拍摄失败 |
| 504 | `camera_config_timeout` / `camera_capture_timeout` | 相机操作超时 |

所有相机操作是串行的。收到 `camera_busy` 时，请在调用端短暂等待后重新发起完整请求。
