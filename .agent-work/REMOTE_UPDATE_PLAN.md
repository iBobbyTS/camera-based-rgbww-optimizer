# Remote Camera Bridge 更新计划：gphoto2 最佳可观测时序

**文档状态：** `ready_for_remote_agent`

**记录范围：** 仅记录 remote camera bridge/API 的开发任务，不修改当前 P7 GUIDE、实验目标或
`PLAN.md` 的实验门禁。

## 0. 决策归属（必须保留）

本文件中的关键决策由 **Developer/Human 本轮明确做出**，不是 Planner 擅自改变实验合同：

```text
decision_owner = Developer/Human
planner_action = record_and_consume_only
advisor_escalation = deferred
guide_progress = not_blocked
```

开发者决策如下：

1. 远程 bridge 只实现 gphoto2/libgphoto2 能提供的最佳可观测数据；不保证它是绝对正确的
   exposure-start，也不得把近似值伪装成绝对真值。
2. 本轮可以改 remote camera bridge/API 的返回契约；不要求修改 gphoto2 上游库本身。
3. 本轮不自动修改 P7 的 timing 合同，不把新数据自动标记为
   `actual_exposure_start_capability=true`，不自动解锁 TD-A。
4. GUIDE 的推进暂不因该开发任务阻塞。等 GUIDE 完成后，或出现下一个超出开发者决定范围的
   阻塞点，再把问题交给 Advisor。

Planner 不得把以上决策重述为 Planner 自主批准的实验方向，也不得在本文件之外扩大授权。

## 1. 背景与当前证据

当前能力审计：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline-r0b/actual-exposure-start-capability-audit.json
sha256 = 0abac8e03f1ed39a6657e606edd7aff675ef04b8058f1a1f1cb123aee906cdcc
status = api_capability_absent_advisor_decision_required
```

现有本地 client 的 remote capture result 只有 CR3 文件和下载层信息；当前 bridge 没有提供
曝光事件时间、时钟域或误差界限。当前 P7 的正式 exposure-start 门禁仍保持锁定，本文件只为
开发一个可审计的 best-effort 数据源。

gphoto2 官方能力边界：

- `gp_camera_capture()` 返回 capture 操作产生的文件路径，不是标准化的 shutter-open 时间；
- `gp_camera_wait_for_event()` 的公共事件主要是 timeout、file-added 和 folder-added；
- `--capture-image-and-download` 在 capture 后下载文件；
- gphoto2 文档明确提示，从收到拍摄信号到相机实际拍摄可能需要约 50ms 到数秒。

参考：

- [libgphoto2 camera API](http://gphoto.github.io/doc/api/gphoto2-camera_8h.html)
- [gphoto2 CLI reference](http://gphoto.github.io/doc/manual/ref-gphoto2-cli.html)

## 2. 非目标与硬限制

远程 agent 不得：

- 宣称 `request_start`、HTTP response、download complete、filename timestamp 或 CR3 写盘时间
  等于 exposure-start；
- 在没有 camera/driver event 证据时构造 fake timestamp；
- 修改 P7 的 `±2s/±5s` gate、settling 算法、observer、58-feature、uncertainty、GUIDE 或
  `PLAN.md`；
- 因为新 API 有返回字段就自动宣称 TD-A 可执行；
- 在本任务范围内访问 `.env`、真实设备、真实相机、Ray、ESPHome 或调用 `all_off`；
- 直接部署、刷写或重启 remote camera 服务，除非 Developer 另行给出明确的部署授权。

本任务的输出语义必须是：

```text
timing_quality = best_effort_gphoto2
exposure_start_status = estimated_not_absolute
formal_p7_eligibility = unchanged / requires later Planner-Advisor decision
```

## 3. 远程 bridge 需要实现的时序采集

### 3.1 保留原始事件，不只保存一个估计值

每次 capture 使用唯一 `capture_id`/`request_id`，在 bridge 侧记录可获得的原始时间点：

```text
bridge_request_received_monotonic_ns
gphoto_capture_call_started_monotonic_ns
gphoto_capture_call_returned_monotonic_ns
camera_event_observed_monotonic_ns|null
camera_event_type|null
file_added_observed_monotonic_ns|null
download_started_monotonic_ns|null
download_completed_monotonic_ns
cr3_saved_monotonic_ns|null
```

实际字段以 bridge 使用的 gphoto2 binding 为准；不存在的字段必须为 `null`，不得填近似值。

事件记录要求：

- 保留原始 event type 和 event payload 的安全摘要；
- 明确事件是 driver 返回、file-added notification 还是本地 I/O 事件；
- 记录事件顺序，拒绝倒序和负 duration；
- 所有 bridge monotonic 时间必须标明 `clock_domain=bridge_monotonic`；
- 若 bridge 同时能获得 UTC，记录 UTC 及其来源，但不能省略 clock domain。

### 3.2 生成 best-effort 估计，但必须显式标注方法

优先级从高到低：

**Tier A：driver/camera event 可用**

如果目标 camera driver 提供了可重复解释的 capture-complete 或 file-added 事件：

```text
event_time = bridge 观察到该事件的 monotonic 时间
exposure_seconds = CR3 MakerNote/EXIF 中的 recorded exposure
exposure_start_estimate = event_time - exposure_seconds
```

该值必须标记为：

```text
method = gphoto_event_minus_recorded_exposure
status = estimated_not_absolute
```

不得称为 `actual_exposure_start`，除非以后由 Advisor/Planner 根据验证证据另行批准。

**Tier B：只有 capture call return 可用**

可以记录：

```text
capture_return_estimate = gphoto_capture_call_returned - recorded_exposure
method = gphoto_capture_return_minus_recorded_exposure
status = weak_estimate
```

该值只能用于诊断延迟分布，不能直接作为 P7 formal timing evidence。

**Tier C：只有 request/download 时间可用**

只保留 raw timestamps，设置：

```text
exposure_start_estimate = null
status = unavailable
```

不得从 request 或 download 时间推导曝光开始。

### 3.3 误差与网络延迟记录

有线网络可以使网络延迟较小，但不能默认为零。bridge 至少记录：

```text
network_observation = {request_id, response_or_event_round_trip_ms|null}
uncertainty_ms = null_or_conservative_bound
uncertainty_basis = measured|driver_documented|unknown
```

如果无法建立保守误差界限，`uncertainty_ms` 必须为 `null`，而不是写入乐观常数。

## 4. API 返回契约

### 4.1 兼容性

保留现有 CR3 binary capture 的兼容路径，同时增加版本化 timing metadata。推荐优先使用：

- sidecar JSON endpoint；或
- multipart response；或
- 明确版本的 JSON envelope。

不建议把复杂 JSON 塞进未版本化的单个 HTTP header。无论采用何种传输方式，CR3 与 metadata
必须通过同一个 `capture_id`、CR3 SHA-256 和 request ID 关联。

### 4.2 建议 schema

```json
{
  "schema": "remote_capture_result_v2",
  "capture_id": "...",
  "cr3": {
    "sha256": "...",
    "byte_count": 123456,
    "content_type": "image/x-canon-cr3"
  },
  "gphoto2": {
    "driver_event_type": "file_added",
    "event_sequence": [],
    "request_received_monotonic_ns": 0,
    "capture_call_started_monotonic_ns": 0,
    "capture_call_returned_monotonic_ns": 0,
    "file_added_observed_monotonic_ns": 0,
    "download_completed_monotonic_ns": 0
  },
  "recorded_exposure": {
    "seconds": 0.001,
    "source": "Canon:ExposureTime",
    "status": "recorded"
  },
  "exposure_start_estimate": {
    "timestamp_monotonic_ns": 0,
    "clock_domain": "bridge_monotonic",
    "method": "gphoto_event_minus_recorded_exposure",
    "status": "estimated_not_absolute",
    "uncertainty_ms": null
  }
}
```

字段名可以由远程 agent 按现有服务风格调整，但以下语义不可改变：来源、时钟域、方法、
不确定度和缺失值必须显式表达。

### 4.3 旧 client 兼容

- 旧 client 仍能保存 CR3；
- 新 metadata 缺失时不能伪造旧字段；
- local client 后续消费时应将 Tier A/B/C 映射为不同 provenance，不得统一映射成
  `actual_exposure_start`；
- metadata 与 CR3 SHA-256 不匹配时，整个 capture metadata fail closed。

## 5. 测试与验证

远程 agent 必须提供离线 fake-gphoto2/bridge 测试，至少覆盖：

1. file-added event 正常路径，生成 Tier A estimate；
2. capture return 无 file-added event，生成 Tier B estimate；
3. 只有 request/download 时间，生成 Tier C unavailable；
4. CR3 recorded exposure 缺失或为 nominal fallback 时，不生成 Tier A estimate；
5. event 顺序逆序、时间为负、单位错误、非单调 monotonic 值全部拒绝；
6. metadata 与 CR3 hash、capture ID、request ID 不匹配全部拒绝；
7. 不把 filename、HTTP response、download 或 write time 伪装成 exposure-start；
8. 网络 RTT 只进入 observed/uncertainty 字段，不改变 raw event time；
9. 旧 binary response 和新 metadata response 的兼容性；
10. token、`.env`、相机序列号及内部路径不出现在 API 返回或日志中。

验证命令和结果由远程 agent 记录在其交接文件中。默认测试必须是 offline-only，不访问真实
camera、bridge、`.env` 或灯光设备。

## 6. 交接物与责任边界

远程 agent 完成后必须交付：

- bridge/API 修改的 source commit 和 diff summary；
- API schema 文档及版本兼容说明；
- gphoto event 能力矩阵（目标 camera/driver、可得到的 event、不可得到的 event）；
- fake-gphoto2 测试结果；
- 一份 best-effort timing sample，明确所有时间点、方法、clock domain 和不确定度；
- 明确声明：没有证明绝对 exposure-start；
- `.agent-work/REMOTE_UPDATE_RESULT.md`，记录完成、失败或能力缺口。

远程 agent 可以决定实现细节（endpoint 形式、内部函数、日志格式），但不能决定：

- 把 estimate 升级为 actual；
- 修改 P7 timing gate 或 GUIDE；
- 修改 `PLAN.md`；
- 是否进入 TD-A 或进行部署/实机测试。

## 7. 停止与升级规则

当前不阻塞 GUIDE。远程 agent 遇到以下情况才停止并写交接，不自行扩展：

- gphoto2/目标 driver 没有比 request/return/download 更好的事件；
- 无法为 estimate 给出可审计的 clock domain 或误差界限；
- 需要相机固件、硬件触发、photodiode、flash-sync 或修改 P7 timing 合同；
- 需要真实设备、remote API 部署、`.env` 或灯光操作授权；
- 需要改变 GUIDE、observer、feature、uncertainty 或 formal acceptance。

升级顺序：

1. 先由 Developer 处理本文件范围内的实现选择；
2. GUIDE 完成后，或出现上述开发者不能决定的阻塞点，再交 Advisor；
3. Advisor/Planner 未明确放行前，TD-A、TD-B、TD-C、sentinel 和后续实机任务保持原锁定。

## 8. 当前状态

```text
remote_update_plan = ready_for_remote_agent
best_available_source = gphoto2/libgphoto2 event and capture timing
absolute_exposure_start = not_claimed
guide = not_blocked
advisor = deferred_until_guide_complete_or_new_decision_blocker
td_a = locked
real_device_calls = forbidden_in_this_plan
```
