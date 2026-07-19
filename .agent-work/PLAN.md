# Stage 6 后续执行计划：Device Readback 至 Gate-6

**计划状态：** active

**Planner 决策日期：** 2026-07-18

**历史归档：** `.agent-work/PLANS/20260718-2210.md`

**已验收代码检查点：** `bb4554a9afd0ff8b5356766335ed232e7daa6e08`

**已验收交接检查点：** `1f9a5881b1021619eb0c8b12df1058e03d42a50e`

**当前阶段：** P7-D0 / `p7_strip_state_readback_preflight`

**当前状态：** `firmware_uploaded_waiting_for_d0_rerun_authorization`

**本次授权解释：** 用户先授权并完成 generation-bearing WebUI firmware 编译，随后于 2026-07-18 明确要求“开始刷写”。该新增授权仅覆盖把第 3.9 节已核验的 OTA artifact 上传到 exact target `bedroom-rgbww-strip.local`、刷写前后关灯以及零输出 device-state 验证；Executor 不得重复询问 firmware upload 授权。它不包含低输出 D0 重跑、相机访问、真实 CR3、P7-R1、sentinel-v2 或其他高输出实验。

**下一条唯一动作：** Planner 复验第 3.10 节的 OTA、零输出 readback 和双关灯证据，再决定是否向用户申请重新执行 exact `p7_strip_state_readback_preflight`。Executor 不得自动重试 D0 或启动 P7-R1。

---

## 1. Executor 合同

### 1.1 必读顺序

1. 本文件全文；
2. `.agent-work/PLAN/00-CONTRACT.md`；
3. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
4. `docs/README.md` 中 remote camera、ESPHome verified state、P6/P7 和双关灯章节；
5. 归档计划 `.agent-work/PLANS/20260718-2210.md` 的第 8.7.25、8.7.44、8.7.47 节；只有需要历史理由时再读取其他归档章节；
6. `git status --short --branch`，保留全部现有改动；
7. 使用 CodeGraph 定位即将修改的符号与调用路径，再读取 CodeGraph 未覆盖的 JSON、Markdown 和 wrapper。

### 1.2 角色边界

Executor 可以：

- 完成当前已授权阶段的代码、测试、dry-run 和一次真实 preflight；
- 修复当前阶段暴露的确定性代码问题，并使用新 run 目录重试；
- 更新 docs、项目 skill、本计划状态和 debug 记录；
- 按仓库 Git 规则形成聚焦提交，但不得 push 或创建 PR。

Executor 不可以：

- 把本次“可以继续”解释为 firmware upload、P7-R1 或高输出授权；
- 手工读取、打印、source 或持久化 `.env`、ESPHome key 或 remote camera token；
- 修改 58-feature、RAW observer、coverage、guard band、P6 manifold、solver budget 或 target set；
- 覆盖任何默认 LUT；
- 为通过 gate 删除失败样本、放宽阈值或拼接不同 run；
- 在本计划标记的 Planner/Advisor 停止点自动继续。

### 1.3 已冻结事实

| 项目 | 冻结值 |
| --- | --- |
| Location | `config/location/locations-20260714-211759.json` / `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80` |
| Ray manifold | `config/hsi/ray-hsi-manifold.json` / `20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34` |
| Waiting v2 policy | `config/hsi/strip-hsi-policy-v2-waiting.json` / `db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4` |
| P7 target config | `config/hsi/strip-hsi-pilot-v2.json` / `8a7a2d3616365e46617ca5d7b7898c9480c1a9599b9135e808ceaab30fc62215` |
| Code-duty curve | `config/channel/code-duty-curve.json` / `0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911` |
| Offline firmware config | `firmware/esphome/bedroom-rgbww-strip-common.yaml` / `deaf0a0717130b60805e3beddb9fa3b59e0f8695d8a22d4f2997859235082ab0` |
| R0K readiness | `tmp/strip-hsi-pilot-offline/p7-r0k-v9-20260718-final/offline-readiness-r0k-final.json` / `b2755ca011510737fff55ab68443aad4a160a8d6fd3e660828c0f0cd7221d576` |
| Ordinary solver cap | 2 starts；每 start 8 feedback、2 rebases、2 confirmation groups；`54 logical / 67 physical` |
| n=5 solver cap | `62 logical / 75 physical` |
| P7-R1 cap | 82 logical；82..170 no-weak physical；82..250 permitted；absolute cap 250 |
| Product policy | INT=100；full-scale active-channel policy；不得称为无条件物理色域 |

R0K 已经通过 Planner 验收。不得继续审计或重写 exhaustion contract，除非当前阶段出现新的可复现回归。

---

## 2. 授权矩阵

| 动作 | 当前是否授权 | 说明 |
| --- | --- | --- |
| 离线实现 preflight module/tests/wrapper | 是 | 当前唯一实现任务 |
| ESPHome 低输出 readback preflight 重跑 | 否 | 原授权已由失败 run 消耗；刷写授权不包含 D0 重跑 |
| Ray120c 关灯命令 | 是 | 仅 intensity=0 与 cleanup，不得点亮 |
| Python/shell `all_off` | 是 | preflight 安全路径 |
| 相机 remote health/config/capture | 否 | 当前阶段不需要相机 |
| 读取 `.env` | 否 | 当前 module 不得加载；后续相机脚本自行加载 |
| firmware compile | 是，已完成 | 用户于 2026-07-18 明确要求“开始编译”；仅 WebUI candidate，不含上传 |
| firmware install | 否 | 不得安装或升级依赖 |
| firmware upload | 是，已完成 | exact WebUI OTA artifact → `bedroom-rgbww-strip.local`；前后关灯及零输出验证通过，不含 D0 重跑 |
| `p7_targeted_reference_repeatability_v2` | 否 | 必须在 preflight 经 Planner 验收后另行授权 |
| `p7_sentinel_4_v2` | 否 | 需 P7-R1 通过和新的高输出授权 |
| remaining 9 / boundary / holdout / P8 | 否 | 继续锁定 |

---

## 3. P7-D0：Strip Device-State Readback Preflight

### 3.1 目标与非目标

目标：证明当前真实 ESPHome 设备暴露 generation-bearing `rgbww_commanded_state`，每次命令后能获得比 baseline 更新且五通道完全一致的独立 snapshot，并证明重复相同命令仍递增 generation。

非目标：

- 不测试相机、RAW、曝光、颜色或亮度；
- 不证明 firmware 已正确编译；
- 不刷写 firmware；
- 不运行任何高输出；
- 不放行 P7-R1。

### 3.2 先实现正式执行面

当前仓库已有 `control.esphome.verified_light()`，但没有独立 preflight module/wrapper。Executor 应新增：

```text
src/camera_based_rgbww_optimizer/control/strip_state_readback_preflight.py
tests/test_strip_state_readback_preflight.py
tmp/run-strip-state-readback-preflight.zsh
```

不得在 root 增加兼容脚本，不得复制 `verified_light()` 的协议解析。新 module 只编排现有 `verified_light`、Ray off 和 `control.all_off`。

CLI 合同：

```text
python -m camera_based_rgbww_optimizer.control.strip_state_readback_preflight \
  (--dry-run | --execute) \
  [--allow-device-control] \
  [--named-experiment p7_strip_state_readback_preflight] \
  --output-dir PATH \
  --run-name NAME
```

要求：

1. `--dry-run` 与 `--execute` 互斥且必须二选一；
2. execute 同时要求 `--allow-device-control` 和 exact `--named-experiment p7_strip_state_readback_preflight`；
3. dry-run 不 import/construct aioesphome client、不调用 Ray/ESPHome/all_off、不读取 `.env`；
4. 不提供任意通道值参数，避免 Executor/用户绕过冻结低输出命令；
5. 默认设备 identity 仍为 `bedroom-rgbww-strip`，不得静默接受其他设备；
6. 所有 JSON 使用原子 replace；JSONL 只 append；异常必须写 `failure.json`。

### 3.3 冻结命令与序列

低输出命令冻结为 calibration bypass 的 raw PWM：

```text
argument order (cw, ww, r, g, b) = (8, 16, 24, 32, 48)
device payload = red=24, green=32, blue=48, warm_white=16, cold_white=8
curve_path = None
max physical PWM = 48
```

必须传 `curve_path=None`。不得通过 code-duty curve 映射，否则输入 code 48 不再保证 physical PWM 小于等于 64。

正式顺序固定：

1. 安装 Python finally 与 wrapper shell trap；
2. 调用一次 `control.all_off`，保存 `preflight-all-off.json`，验证 Ray response 为 intensity 0；
3. `verified_light(0,0,0,0,0, curve_path=None)`，记录 `startup_zero`；
4. `verified_light(8,16,24,32,48, curve_path=None)`，记录 `low_first`；
5. 重复完全相同调用，记录 `low_repeat`；
6. `verified_light(0,0,0,0,0, curve_path=None)`，记录 `main_zero`；
7. Python finally 无条件调用 `control.all_off` 并写 `all-off-python.json`；
8. Python finally 在 all-off 后再尝试一次 verified zero，写 `final-zero.json`；即使该读回失败，也必须保留 all-off 结果并让 run 进入安全未知分支；
9. Python 退出后 shell trap 无条件调用 `control.all_off --json`，写 `all-off-shell.json`。

五次 verified transition（startup zero、low first、low repeat、main zero、final zero）必须满足：

- `schema_version=1`；
- `device_state_entity.object_id=rgbww_commanded_state`；
- identity name 精确为 `bedroom-rgbww-strip`，MAC 非空且五次一致；
- 每次 `device_snapshot.generation > baseline_snapshot.generation`；
- 本次 observed generation 严格大于上一次 observed generation；
- requested payload、observed payload 与冻结 step 完全一致；
- `low_repeat` 即使 payload 相同，generation 仍必须递增；
- `main_zero` 和 `final_zero` 五通道全零。

### 3.4 Artifact 合同

Dry-run 和 execute 都使用全新目录。正式根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/
```

每个 run 至少包含：

```text
plan.json
run.json
transitions.jsonl
preflight-all-off.json
final-zero.json
all-off-python.json
all-off-shell.json
failure.json                 # 仅失败时
<run-name>.runner.log        # run 目录相邻
<run-name>.wrapper.log       # 若 wrapper 记录 stdout/stderr
```

`plan.json` 在任何设备调用前冻结：experiment id、device identity、五个 transition、raw-PWM 命令、最大 PWM、`curve_path=null`、超时、Python/shell cleanup 和零 camera/CR3 声明。

`run.json` 至少记录：status、start/finish、completed transition count、first/last generation、device identity、failure branch 和 cleanup summary。禁止记录 API key、secrets 内容或 `.env`。

### 3.5 必须新增的测试

1. dry-run 生成精确五步计划且零设备调用；
2. execute 缺少 consent 或 exact experiment id 时拒绝且零设备调用；
3. fake backend 的五次成功 transition，包含重复命令 generation 递增；
4. identity name/MAC 漂移拒绝；
5. 缺 entity、重复 entity、旧 generation、通道不符、timeout 均 fail closed；
6. 任一主步骤异常仍执行 Python cleanup；
7. final verified zero 失败时状态为 `cleanup_state_unknown`，不写 pass；
8. shell wrapper 在正常、Python exception、INT/TERM/HUP 都执行一次 trap cleanup；
9. frozen command 的 raw payload 最大值确实为 48，且 module 不加载 curve；
10. artifact 不含 secret/token 字段。

离线检查：

```bash
.venv/bin/python -m unittest tests.test_strip_state_readback_preflight tests.test_esphome_state tests.test_all_off
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m compileall -q src tests
zsh -n tmp/run-strip-state-readback-preflight.zsh
git diff --check
codegraph sync
```

所有检查通过后先运行一次 dry-run，并人工/程序审计 `plan.json`；dry-run 不得创建网络连接或灯光调用。

### 3.6 实机执行

不得从当前 shell 直接调用 module execute；只能使用 wrapper：

```bash
RUN_DIR="/Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/p7-strip-state-readback-preflight-$(date +%Y%m%d-%H%M%S)"
tmp/run-strip-state-readback-preflight.zsh "$RUN_DIR"
```

Wrapper 必须：

- 在启动 child 前安装 EXIT/INT/TERM/HUP trap；
- 保存 child PID、runner log、wrapper log 和启动时间；
- 前台等待短 preflight 完成，不创建 heartbeat；
- signal 时先传递给 child、等待 child cleanup，再执行 shell all-off；
- 不调用相机、不生成 CR3、不访问 remote camera API。

### 3.7 D0 验收与分支

`D0-PASS`：

- run complete；五次 transition 全部通过；
- generation 全局严格递增；
- device identity 一致；
- 两次 low payload 完全相同且 raw PWM 最大 48；
- main/final zero 全零；Ray 保持 intensity 0；
- Python/shell cleanup 均两步成功；
- 无 failure、CR3、`.npy` 或 secret；
- 更新本计划证据后停止，交还 Planner。

`D0-FIRMWARE-MISSING`：缺少 generation-bearing entity 或 required services。保留 run/failure/cleanup，停止。不得安装 ESPHome CLI、编译或刷写；向 Planner 报告当前 firmware diff、目标设备和 recovery 方案，等待用户单独授权。

`D0-DEVICE/IDENTITY`：连接、expected name、MAC、entity duplication 或 timeout 失败。保留证据并双关灯；不得改为宽松 identity。

`D0-READBACK`：generation、payload 或 repeated-command 语义不符。标 run invalid，双关灯并停止；不得把 command acknowledgement 当 snapshot。

`D0-CLEANUP-UNKNOWN`：Python 或 shell cleanup 缺失/失败，或 final zero 无法确认。立即再执行一次 recovery `control.all_off` 并保存独立证据；安全状态仍不确定时明确通知用户，不得继续。

`D0-CODE`：实现/测试错误。只允许离线修复；若实机已启动，先完成双关灯，使用全新 run 目录重试。

任何分支都不得在同一任务自动进入第 4 节。

### 3.8 P7-D0 Executor 实机结果（2026-07-18）

```text
executor_verdict = fail_waiting_for_planner
implementation_checkpoint = eb226bd
plan_split_checkpoint = 2e3192b
named_experiment = p7_strip_state_readback_preflight
run_dir = /Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/p7-strip-state-readback-preflight-20260718-223408
primary_branch = D0-FIRMWARE-MISSING
safety_branch = D0-CLEANUP-UNKNOWN
passed_transitions = 0
failed_transitions = 2
low_output_command_attempted = false
camera_calls = 0
cr3 = 0
npy = 0
firmware_compile_or_upload = 0
```

Executor 已完成独立 module、测试、shell wrapper、dry-run 审计和唯一一次授权实机 preflight。离线验证为 focused D0/ESPHome/all-off `17/17`、full suite `432/432`（`143.567s`）、`compileall`、wrapper `zsh -n`、`git diff --check` 与 `codegraph sync` 全部通过。Dry-run 只有 `plan.json/run.json`，五步顺序、重复低输出 payload、`curve_path=null`、最大 raw PWM 48 与零设备/相机调用均通过审计。

正式 run 在第一步 `startup_zero` 即由现有 `control.esphome.verified_light()` fail closed：当前真实设备没有唯一的 generation-bearing `rgbww_commanded_state` entity。Python finally 后的 `final_zero` 得到相同错误，因此没有任何 verified transition 通过，也没有发送 `(8,16,24,32,48)` 低输出命令。`failure.json` 同时保留：

- primary failure：`D0-FIRMWARE-MISSING` / `RGBWW device-state entity is missing or duplicated`；
- cleanup failure：final verified zero 无法建立独立 snapshot，故安全分支为 `D0-CLEANUP-UNKNOWN`。

preflight、Python finally、shell trap 和一次独立 recovery 共四份 all-off evidence 均包含 ESPHome 五通道全零 acknowledgement 与 Ray `intensity=0` 成功响应；recovery CLI exit 为 0。由于 installed firmware 不提供独立 readback entity，不能把 command acknowledgement 升格为 snapshot，安全状态仍按 unknown 报告。run 内无 CR3、`.npy`、secret/token 字段，runner PID `31476` 已退出。

关键 artifact：

```text
run.json sha256 = 250bb03b0259e527f7201a54ec9338b60c2169ac1c2cc2d5c02899acab237553
failure.json sha256 = 94030b34ec7258386f750f96cc317cc3b71e4043ebc2360b56ab3c8903d053b8
transitions.jsonl sha256 = e45d08c13318f6d3d79807cae2529616ddd86b855904155f14ee5799f99c1fab
all-off-python.json sha256 = bbb1ee50f05ab028d9da97b084ba9cbcbe9d76830ef0f0893d952f69d50c51c8
all-off-shell.json sha256 = b373aad2db50db933122f9d7f63f818c43914755ad195f712493e344b30b4f71
recovery-all-off.json sha256 = a1387d5e207f4318bce4ed57c93265ecb39b0692a060bd43d8b7ef727c1c313f
```

仓库所需 generation-bearing firmware diff 已存在于 `a380dfe63c732ddf126e8aa396a41b2985da4713`：它把 boot、`set_rgbww_12bit` 和 `all_off` 统一到 `apply_rgbww_12bit`，新增 `rgbww_state_generation`、diagnostic text sensor `rgbww_commanded_state`，并在每次包括相同命令的 apply 后递增 generation/publish 五通道 JSON。当前文件 hash 仍为冻结的 `deaf0a0717130b60805e3beddb9fa3b59e0f8695d8a22d4f2997859235082ab0`，工作区无 firmware diff。实机证据只能证明 installed target 没有暴露恰好一个可用的冻结 entity，不能从同一错误进一步区分缺失或重复。恢复方案只能是：Planner/用户单独授权对目标 `bedroom-rgbww-strip` 执行 firmware compile/upload，明确保留现有 OTA recovery 路径，然后使用全新 run 目录重新执行 D0。尽管当前 `.venv` 已有 ESPHome `2026.5.2`，本轮未运行 compile、install 或 upload。

启动外层 shell 在 wrapper 后打印了字面 `WRAPPER_EXIT=0`，没有捕获真实 `$?`；该行不能作为 wrapper exit evidence。正式 `runner.log`、`run.json` 和 `failure.json` 均明确记录失败，shell trap artifact 已生成。该调用证据缺口不影响 firmware/readback 结论，但必须保留，重跑 D0 时应显式记录 wrapper exit code。

本阶段在此停止。P7-R1、sentinel-v2、remaining 9、boundary、holdout、Gate-6 和 P8 继续锁定，不需要 Advisor 介入。

### 3.9 Generation-bearing firmware 编译结果（2026-07-18）

用户明确要求“开始编译”后，Executor 只执行了 WebUI candidate 的本地编译：

```text
command = .venv/bin/python -m esphome compile firmware/esphome/bedroom-rgbww-strip-webui.yaml
esphome = 2026.5.2
input common sha256 = deaf0a0717130b60805e3beddb9fa3b59e0f8695d8a22d4f2997859235082ab0
verified run = tmp/firmware-compile/webui-20260718-230656-verified
exit = 0
RAM = 46512 / 327680 bytes (14.2%)
Flash = 893343 / 1835008 bytes (48.7%)
firmware.ota.bin = 893744 bytes / c24a60463d37314b0c041188ec2d55dbb1be19614fb512a5a619308137cbcbc0
firmware.factory.bin = 959280 bytes / ed8c868277e4a8ac0315365f308576f8e8a55a1ea5f09c2e82df7f7927fe2ffc
```

编译使用已有 ESPHome/PlatformIO 环境，没有执行依赖安装。第一次完整编译本体成功，但记录 shell 误用 zsh 只读变量 `status`，外层退出为 1；该日志保留在前一个 run 目录，不作为正式退出证据。随后使用修正后的记录变量做增量复编，得到上述 `exit=0`、持续落盘日志、artifact size 和 SHA-256。

截至本节的编译步骤，没有执行 `esphome run`、`esphome upload`、设备连接、灯光命令或 D0 重跑；当时新 candidate 尚未安装。后续用户另行批准并完成的 OTA 与零输出验证记录在第 3.10 节。

### 3.10 Generation-bearing firmware OTA 结果（2026-07-18）

用户明确要求“开始刷写”后，Executor 使用第 3.9 节已核验 WebUI artifact 对 exact target 执行了一次 OTA：

```text
command = .venv/bin/python -m esphome upload firmware/esphome/bedroom-rgbww-strip-webui.yaml --device bedroom-rgbww-strip.local
run = tmp/firmware-upload/webui-20260718-232524
resolved target = 192.168.0.74:3232
artifact = firmware.bin / 893744 bytes
artifact sha256 = c24a60463d37314b0c041188ec2d55dbb1be19614fb512a5a619308137cbcbc0
upload = OTA successful
upload exit = 0
```

安全与恢复证据：

- OTA 前 `control.all_off`：ESPHome 五通道全零、Ray intensity 0，二者均成功；
- OTA 后显式 `control.all_off`：ESPHome 五通道全零、Ray intensity 0，二者均成功；
- 新固件零输出 independent readback：exact name `bedroom-rgbww-strip`、MAC `E0:8C:FE:63:C9:40`、entity `rgbww_commanded_state`、generation `2 -> 3`、requested/observed 五通道全零；
- EXIT trap `control.all_off`：ESPHome 与 Ray 均成功，shell cleanup exit `0`；
- 未调用相机、未产生 CR3、未发送任何非零灯带或 Ray 命令。

这证明 generation-bearing firmware 已安装、Native API 可重新连接且零输出 readback/cleanup 正常；它不等于完整 D0-PASS，因为冻结的 raw PWM 最大 48 序列尚未在新固件上重跑。原 D0 实机失败证据继续保留为历史，当前后续分支改为等待 Planner/用户单独授权全新目录的 D0 重跑。

---

## 4. P7-R1：Targeted Reference/Repeatability（锁定）

### 4.1 解锁条件

必须全部满足：

1. D0-PASS 经 Planner 验收；
2. 用户另行明确授权 exact named experiment `p7_targeted_reference_repeatability_v2`；
3. 若 D0 要求 firmware upload，upload 已另行授权、完成并重新通过 D0；
4. 当前 checkout、R0K readiness、location/manifold/observer/basis/hash 未漂移；
5. 新 session 重新执行 all-off、remote health/config、Ray get/readback 与 source isolation preflight。

本次“可以继续”不满足第 2 条。

### 4.2 冻结协议

正式顺序：

```text
start ambient
Ray block A
strip block A
strip block B
Ray block B
end ambient
Python cleanup
shell cleanup
```

每张正式 measurement：独立 `off -> 1 s -> exact source on -> verified readback -> 60 s -> capture -> off`。

Ray 30 张：H0/S0、H120/S100、H300/S100；A/B 两 block，每 state 各 5 次。每 state 独立曝光 cache，B 从同 state A cache 恢复；strip 始终全零。

Strip 50 张：冻结旧 sentinel 的 H0/S0@4095、H120/S100@4095、H120/S50@4095、H300/S100@4095、H0/S0@3072 exact commands；A/B 两 block，每 command 各 5 次。每 command 独立曝光 cache，Ray 始终 intensity 0。

计数：82 logical（30 Ray + 50 strip + 2 ambient）；80 formal；82..170 no-weak physical；82..250 permitted；absolute cap 250；最长 60-second settling 总计 9600 秒。额外 auto-exposure/weak CR3 不得补足或替换 formal sample。

只能通过 `tmp/run-hsi-reference-repeatability.zsh` 启动；remote camera 和 `.env` 只由正式脚本读取。禁止手工拼接 block 或复用失败 run。

### 4.3 R1 分支与停止点

- `R-PASS`：reference center/repeatability、strip 四类 variance、coverage/guard 全部可冻结。Finalizer 仍只写 `calibrated_waiting_for_planner`、`formal_capture_eligible=false`；停止并交还 Planner。
- `R-REFERENCE-EPOCH`：current Ray 稳定但偏离 P6 center。不得同 run 重拟合；交还 Planner/Advisor 决定新自然日复测或新 epoch。
- `R-REFERENCE-UNSTABLE`：block 或 pre/post 不稳定。检查热状态、几何、曝光、remote 和供电；修复前不得 sentinel。
- `R-STRIP-CLASS-HIGH`：只允许逐 plane 提高相应 class variance；有趋势、双峰、非有限或单帧支配时为 `uncertainty_unresolved`。
- `R-MEASUREMENT/CODE/SAFETY`：整个 run invalid；双关灯、保留证据、修复后全新目录完整重跑。

R1 完成后必须由 Planner 验收并冻结 v2 artifact/hash。不得自动进入 sentinel-v2。

---

## 5. Sentinel-v2 四点（锁定）

### 5.1 解锁条件

- R-PASS 与正式 v2 artifact 经 Planner 验收；
- 用户另行授权 exact `p7_sentinel_4_v2` 和计划内有界高输出；
- 新 session 的设备、camera、Ray、all-off preflight 全部通过。

### 5.2 冻结目标

```text
H0/S0
H120/S100
H120/S50
H300/S100
```

Pre Ray anchors：H0/S0、H120/S100、H300/S100，各 3 次独立 settled capture。Post anchor：H120/S100，3 次。普通 target 3 confirmations；任何 boundary/scale-relaxed 诊断 5 confirmations。

正式 full-scale policy：INT100、max_code=4095、至少一 active channel 固定 4095。普通 target cap `54 logical / 67 physical`；结果只能使用冻结状态集，不得按观察结果增加 starts/rounds/rebases/captures。

SAT0 不执行 Hue gate。每点分别保存：

```text
hsi_coordinate_equivalent
observer_equivalent
color_rendering_residual
```

### 5.3 Sentinel 停止点

完成四点、analysis、commands/source audit、CR3/recorded exposure、零 `.npy` 和双 cleanup 后必须停止交还 Planner。即使 4/4 coordinate equivalent，也不得自动执行 remaining 9。

任一 `reference_drift`、`uncertainty_unresolved`、`measurement_unreachable`、solver budget、readback、source isolation 或 cleanup failure 均保留具体状态，不得调整 artifact 或阈值后续跑。

---

## 6. Remaining 9 与 13 点合并（锁定）

### 6.1 解锁条件

只有 sentinel-v2 经 Planner 明确放行，且用户另行授权 remaining 9 后执行。

Remaining target 固定为：

```text
H0/S50, H0/S100
H60/S50, H60/S100
H180/S50, H180/S100
H240/S50, H240/S100
H300/S50
```

普通点 3 confirmations；需要 scale-relaxed 诊断时 5。每 session 使用同样的 Ray anchors、source isolation、recorded exposure 与双 cleanup，不复用 sentinel 曝光 cache。

### 6.2 Combined analyzer

新增/使用纯离线 combined analyzer，输入 sentinel 与 remaining 的不可变 run/hash，要求同一 v2 policy/manifold/location/observer/basis/code checkpoint，且恰好 13 个不重复 target。

输出：

```text
p7-int100-fullscale-13-analysis.json
```

进入 boundary 的最低条件：

- 13/13 均有合法、可审计 target row；
- 无 reference drift 或 uncertainty unresolved；
- 每个主 Hue 至少有一个可建立 coordinate-equivalent 范围的非零 SAT 测量；
- full-scale 未确认点已完成 3072、必要时 2048 诊断或明确列为待诊断；
- observer/color-rendering evidence 均保留。

Combined 结果是高风险 Planner 停止点，不得自动进入 boundary。

---

## 7. Full-Scale SAT Boundary（锁定）

边界名称只能是：

```text
s_exact_max_int100_fullscale(h)
```

它不是灯带无条件物理色域。

每个主 Hue：

1. S100 coordinate equivalent 时上限记 100；
2. S50 pass、S100 未确认时 bracket `[50,100]`；
3. S50 未确认时从 P6 实测 S20/S5 方向寻找非零下界；SAT0 不可作 Hue-specific 下界；
4. 新 boundary target 一律 5 confirmations；
5. 整数 SAT 二分/定向加密到相邻整数；
6. full-scale 未确认上界必须做 max_code=3072，必要时 2048；
7. 保存 active-set、white fraction、condition、sensitivity 和原因；
8. 不单调或相邻 Hue 急变时只定向加点，不平滑掉实测状态。

降低 max_code 后通过时：

```text
boundary_cause = full_scale_active_channel_policy
physical_gamut_inference = prohibited
```

六主 Hue 均有范围、必要 bracket 完整并通过 Planner 验收后，才允许候选阶段。

---

## 8. INT100 Candidate 与 Holdout（锁定）

### 8.1 候选

离线生成但不安装：

```text
config/hsi/rgbww-hsi-int100-fullscale-candidate.json
```

第一版保持 Hue 周期分段线性、SAT 单调分段线性；边界外压缩到 `s_exact_max_int100_fullscale(h)`；五通道约束 0..4095 并保持 full-scale active-channel policy。记录全部输入/run hash、active-set switch、boundary table、interpolation policy、`absolute_brightness_matched=false`、`installed=false`。

冻结 holdout 前以 0.5 degree 网格审计 H0..360：command(0) 与 command(360) 逐通道 bit-exact；seam step 不得超过非 seam first-difference 的预冻结 `median + 3*MAD`（MAD=0 时使用非 seam maximum）。门槛写入 candidate/plan 后不得重算。

### 8.2 Holdout

至少八个非训练点：

- 六扇区 Hue：30、90、150、210、270、330；SAT 按冻结规则交替选其已验证范围约 35%/65%，普通点 3 confirmations；
- 周期对 H1/H359，使用两侧都在范围内的同一 SAT，5 confirmations，同时作为高曲率 holdout。

Holdout 命令只来自冻结 candidate；禁止 probe、feedback、重新优化或观察结果后改点。任一失败保留，candidate 修改后原 holdout 失效，必须新 hash、新 plan、新 run。

全部 coordinate、reference、uncertainty、command/CR3/exposure/cleanup 门通过后，仍不安装 candidate，进入 Gate-6。

---

## 9. Gate-6 与 Advisor 停止点

Gate-6 交接包必须包含：

1. 正式 v2 reference/repeatability/coverage artifact 与 hash；
2. sentinel、remaining、combined 13 点分析；
3. 所有 Ray anchors 与 drift 结论；
4. 六 Hue `s_exact_max_int100_fullscale` 和 3072/2048 诊断；
5. 未安装的 full-scale candidate/hash；
6. 六扇区、0/360、高曲率 holdout；
7. 所有 commands、CR3、recorded exposure、无 `.npy`、Python/shell cleanup 审计；
8. 完整测试、compileall、wrapper syntax、diff-check、CodeGraph 状态；
9. remaining risks：observer-equivalence、color-rendering residual、absolute brightness 未匹配。

状态更新为：

```text
current_phase = GATE_6
stage_status = at_decision_gate
next_action = advisor_review_gate_6
```

Advisor 明确决定前不得进入 P8、三维 INT 网络、安装或覆盖默认配置。

---

## 10. 通用失败与安全合同

| 事件 | 必须动作 | 禁止动作 |
| --- | --- | --- |
| source/readback mismatch | 立即 off、保留证据、run invalid | 重试到偶然通过后删失败 |
| reference drift | 停止并交还 Planner/Advisor | 同 run 重拟合 P6 |
| uncertainty unresolved | 保留 confirmations，停止 | 用同组帧重估 sigma 或放宽 guard |
| measurement unreachable | 在冻结 1.25x envelope 内按计划处理 | 扩曝光、删 feature |
| solver budget exhausted | 保留 best valid 和完整 ledger | 增加预算继续当前 run |
| Python cleanup 缺失 | 立即 recovery all-off | 假设 shell 会处理 |
| shell cleanup 缺失 | 立即 recovery all-off 并保存独立证据 | 宣称安全已确认 |
| 进程消失但 run=running | recovery all-off、failure evidence | 拼接后续结果 |
| firmware/API 缺失 | 停止并申请单独 upload 授权 | 自动安装、编译或刷写 |
| candidate/holdout 失败 | 保留原 holdout，回 Planner | validation 内优化 |

所有可点亮 strip 的 Python runner 必须 `finally` 关 strip 和 Ray；所有正式 shell wrapper 必须使用 EXIT/INT/TERM/HUP trap 再关一次。专用 light-on 工具不属于本计划执行面。

---

## 11. Executor 状态模板

每个高风险阶段完成或失败后更新本文件：

```text
current_phase = P7_D0 | P7_R1 | SENTINEL_V2 | REMAINING_9 | BOUNDARY | HOLDOUT | GATE_6
stage_status = implementation_in_progress | running | pass_waiting_for_planner |
               fail_waiting_for_planner | blocked_waiting_for_authorization | at_decision_gate
current_head =
worktree_state =
authorization =
run_dir =
runner_pid_tty =
input_hashes =
capture_counts =
analysis =
failure_evidence =
cleanup_evidence =
tests =
branch =
next_action =
```

### 当前值

```text
current_phase = P7_D0
stage_status = fail_waiting_for_planner
current_head = eb226bd implementation checkpoint; documentation-only D0 result handoff is its successor
worktree_state = clean after committing this D0 result handoff; preserve all prior work
authorization = exact p7_strip_state_readback_preflight consumed; no firmware compile/upload/camera/P7-R1/high-output authorization
run_dir = /Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/p7-strip-state-readback-preflight-20260718-223408
input_hashes = section 1.3
capture_counts = passed transitions 0; failed startup_zero/final_zero 2; low raw PWM command not attempted; CR3 0; NPY 0
analysis = current device lacks unique rgbww_commanded_state; primary D0-FIRMWARE-MISSING and safety D0-CLEANUP-UNKNOWN
failure_evidence = failure.json @ 94030b34ec7258386f750f96cc317cc3b71e4043ebc2360b56ab3c8903d053b8; outer launch did not preserve real wrapper exit code
cleanup_evidence = preflight/Python/shell/recovery all-off each report ESPHome zero acknowledgement plus Ray intensity 0; final independent zero unavailable; safety remains unknown
tests = focused 17/17; full 432/432 in 143.567s; compileall, wrapper syntax, diff-check and CodeGraph pass
branch = D0_FIRMWARE_MISSING_AND_CLEANUP_UNKNOWN
next_action = Planner reviews section 3.8 and decides whether to request separate firmware compile/upload authorization; no automatic retry or P7-R1
```
