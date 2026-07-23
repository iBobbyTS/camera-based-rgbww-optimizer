# gphoto2 / Canon R6 Mark III Event Capability Matrix

本矩阵描述当前 bridge 使用的 gphoto2 2.5.32 / libgphoto2 2.5.34 CLI 路径能够安全声明的能力；它不是相机固件或 libgphoto2 所有潜在 binding 的能力声明。

| 信号 | 当前路径 | API 表达 | 是否可推导 estimate |
| --- | --- | --- | --- |
| bridge 收到 HTTP 请求 | 可观测 | `request_received_monotonic_ns` | 否 |
| 启动 `--capture-image-and-download` | 可观测 | `capture_call_started_monotonic_ns` | 否 |
| CLI 报告 `New file is in location` | 可观测，安全摘要，不返回相机路径 | `capture_call_returned_monotonic_ns`；event type=`capture_result_path_observed` | 仅 Tier B；不是 driver `file_added` |
| `gp_camera_wait_for_event()` driver `file_added` | 当前 CLI 兼容路径未观测/未验证 | `file_added_observed_monotonic_ns=null` | 否；离线 fake 测试覆盖未来明确事件输入的 Tier A 算法 |
| driver `capture_complete` | 当前目标路径未观测/未验证 | `camera_event_observed_monotonic_ns=null` | 否 |
| shutter-open / exposure-start | gphoto2 公共 capture API 不直接提供 | 不提供 `actual_exposure_start` | 否 |
| CLI 报告开始保存本地文件 | 可观测，安全摘要 | `download_started_monotonic_ns` | 否 |
| capture/download 进程返回 | 可观测 | `download_completed_monotonic_ns` | 否 |
| bridge 发现单个 CR3 | 可观测，不返回内部路径 | `cr3_saved_observed_monotonic_ns` | 否 |
| CR3 recorded exposure | 随 bridge 部署的 ExifTool 只读取 Canon MakerNote `Canon:ExposureTime`；缺失或失败即 fail-closed，标准 EXIF 不作为 fallback | `recorded_exposure` | 只作为 Tier A/B 的曝光时长输入 |
| 网络 RTT / 保守误差界限 | 服务端单边无法建立 | `null`, basis=`unknown` | 不改变 raw event time |

结论：当前已部署实现的最高可用等级预计是 Tier B `weak_estimate`；如果 CLI 没有及时暴露 capture result marker 或 CR3 缺少 recorded exposure，则为 Tier C `unavailable`。没有证据支持绝对 exposure-start，P7 formal eligibility 保持不变。
