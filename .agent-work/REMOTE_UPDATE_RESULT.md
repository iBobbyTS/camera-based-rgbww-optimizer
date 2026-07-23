# Remote Camera Bridge 更新结果：gphoto2 最佳可观测时序

**结果状态：** `completed_with_offline_and_non_camera_runtime_validation`

**执行日期：** 2026-07-19

## 1. 范围与决策边界

本次仅更新 `ibobby-rpi-4.local` 上的 remote camera bridge/API，实现 gphoto2/libgphoto2 当前路径能够提供的 best-effort 时序数据。

冻结语义保持不变：

```text
timing_quality = best_effort_gphoto2
exposure_start_status = estimated_not_absolute | weak_estimate | unavailable
formal_p7_eligibility = unchanged_requires_later_planner_advisor_decision
actual_exposure_start_capability = not_claimed
td_a = locked
```

未修改 `.agent-work/PLAN.md`、P7 timing gate、settling、observer、58-feature、uncertainty、GUIDE、Ray 或 ESPHome 代码。

## 2. 部署结果

远端目录：`/home/ibobby/r6-camera-bridge`

systemd 服务：`r6-camera-bridge.service`

部署后状态：

```text
active
enabled
```

远端源码提交：

```text
baseline = f6f24b1
update = 22f2a2bc05af3296a4caa90578b8cffcf8796181
subject = feat(camera-bridge): add best-effort capture timing
```

提交统计：

```text
7 files changed, 1199 insertions(+), 65 deletions(-)
```

主要文件：

- `r6_camera_bridge.py`：保留 v1 binary，新增 v2 multipart、CLI 输出时序观察、标准 EXIF fallback、同步清理和安全响应。
- `r6_timing.py`：时序模型、顺序/单位验证、Tier A/B/C 估计、CR3 hash/ID 关联校验。
- `API.md`：版本兼容和 schema 文档；继续通过无需认证的 `GET /v1/API.md` 公开。
- `GPHOTO2_EVENT_CAPABILITY.md`：目标 CLI/driver 能力矩阵。
- `BEST_EFFORT_TIMING_SAMPLE.json`：离线 Tier B 示例。
- `tests/`：完全离线 fake-gphoto2/bridge 测试。

## 3. API 契约

### 兼容路径

`POST /v1/capture` 继续返回同步 CR3 binary：

```text
Content-Type: application/octet-stream
```

旧 client 无需修改即可继续保存 CR3。

### 新路径

`POST /v2/capture` 使用同一 JSON 设置契约并同步拍摄，返回：

```text
Content-Type: multipart/mixed
part 1 = application/json / remote_capture_result_v2
part 2 = image/x-canon-cr3
```

metadata 和 CR3 通过以下字段 fail-closed 关联：

- `capture_id`
- `request_id`
- `cr3.sha256`
- `cr3.byte_count`

公开文档：`http://ibobby-rpi-4.local:8088/v1/API.md`

## 4. 可观测能力结论

当前 `--capture-image-and-download` CLI 路径安全观察：

- bridge request received；
- capture command started；
- CLI `New file is in location` 的到达时间，分类为 `capture_result_path_observed`；
- CLI `Saving file as` 的到达时间；
- capture/download process returned；
- bridge 观察到单个 CR3 的时间；
- CR3 标准 EXIF `ExposureTime`，不需要新增系统包。

当前没有把 CLI 的 `New file...` 文本重命名成 driver `file_added`。没有观测到或证明：

- shutter-open；
- 绝对 exposure-start；
- `gp_camera_wait_for_event()` 的目标 driver `file_added`；
- driver `capture_complete`；
- 可审计的网络 RTT 或保守 uncertainty bound。

因此当前实际实现的最高预期等级是：

```text
Tier B = gphoto_capture_return_minus_recorded_exposure / weak_estimate
```

如果 CLI marker 或 recorded exposure 缺失，则为 Tier C `unavailable`。Tier A 算法只在明确的 driver/camera event 输入存在时启用，并由离线 fake event 测试覆盖。

## 5. 离线测试

远端命令：

```bash
cd /home/ibobby/r6-camera-bridge
/home/ibobby/r6-camera-bridge/.venv/bin/python -m compileall -q \
  r6_camera_bridge.py r6_timing.py tests
/home/ibobby/r6-camera-bridge/.venv/bin/python -m unittest discover -s tests -v
/home/ibobby/r6-camera-bridge/.venv/bin/python -m json.tool \
  BEST_EFFORT_TIMING_SAMPLE.json >/dev/null
```

结果：

```text
13 tests run
13 passed
0 failed
```

覆盖：

1. fake file-added Tier A estimate；
2. capture return Tier B estimate；
3. request/download-only Tier C unavailable；
4. missing/nominal exposure 不生成 estimate；
5. 负值、错误单位、逆序、非单调全部拒绝；
6. CR3 hash、capture ID、request ID mismatch fail closed；
7. download/write/filename 不伪装为 exposure-start；
8. network observation 不改变 raw event/estimate；
9. v1 binary 与 v2 multipart 兼容；
10. token、`.env`、serial、内部路径不进入响应；
11. fake-gphoto2 CLI 输出只保留 event type 和安全摘要；
12. 内建 CR3 标准 EXIF ExposureTime fallback；
13. sample JSON 语法验证。

测试未读取项目 `.env`，未调用真实相机、Ray、ESPHome 或 `all_off`。

## 6. 部署后非相机验证

已验证：

```text
GET /health = 200 {"status":"ok"}
GET /v1/API.md = 200，包含 v2 schema 和非绝对时序声明
POST /v2/capture without token = 401
GET /v1/config without token = 401
remote git status = clean
/run/r6-camera-bridge regular files = 0
service directory *.cr3/*.log files = 0
```

未执行 authenticated capture，因此没有本轮 best-effort timing 实机样本；这是 `REMOTE_UPDATE_PLAN.md` 的真实设备禁令所要求的停止边界。交付的 `BEST_EFFORT_TIMING_SAMPLE.json` 明确是离线 fake-gphoto2 Tier B 示例。

## 7. 结论

远端 bridge 已提供可审计、版本化、与 CR3 强关联的 best-effort 时序 metadata，同时保留原 v1 同步 binary 合同、RAW-only、防 Bulb、不保留相机卡原片、树莓派不持久化 CR3/应用日志的约束。

本更新没有证明绝对 exposure-start，没有把任何 estimate 升级为 actual，也没有改变 P7/TD-A 的 formal eligibility。
