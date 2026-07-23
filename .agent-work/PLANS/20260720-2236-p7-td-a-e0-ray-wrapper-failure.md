# P7 TD-A E0 与 Ray Wrapper 失败验收归档

**归档时间：** `2026-07-20T22:36:32-0600`

**被验收 PLAN SHA-256：**
`805053e7dafb42f16f896e1b1d68d76c9d66be222676bd97a51f0a3b1b925e47`

**Planner 决定：** `rejected_to_bounded_offline_correction`

**精确下一分支：** `P7_TD_A_W0_WRAPPER_RUNTIME_OFFLINE_CORRECTION`

## 1. 被验收范围

本次验收覆盖以下已经执行或已经审阅的部分：

1. TD-A E0 production completion gate；
2. 实机前离线进入门与 exact Ray/strip dry plan；
3. 实机 preflight、双灯关闭与 generation-bearing strip readback；
4. Ray TD-A wrapper 的首次正式启动和 hard-invalid 停止；
5. 失败后的 shell cleanup、独立 recovery 和零采集证据；
6. Human 一次性 TD-A 授权是否被消费的 Planner 判定。

本次没有验收或解锁 strip TD-A、paired finalizer 的真实输入、TD-B、TD-C、sentinel、remaining 9、
boundary、holdout、Gate-6、P8、默认配置安装、firmware 或 remote deployment。

## 2. 已接受实现与方法

E0 的核心实现接受并冻结：

- 单源 analyzer 解析 Python cleanup、shell cleanup、run cleanup、wrapper result 和两个 exit-status
  文件，任一缺失或失败均 fail closed；
- 双源 `analyze_td_a_pair` 重新分析 Ray/strip 两个 source，重放 source、input、timing、capture、
  cleanup 和 wrapper 合同；
- 双源判定只允许 `td_a_pass` 或 `settling_not_demonstrated_by_600`，且 `600 s` 仅为验证点；
- combined 输出原子写入，默认 `config/hsi/p7-operating-envelope-v1.json` 保持不变；
- R0D 的 experiment/source-scoped shutter ledger 和 remote ISO/aperture/RAW provenance 继续有效。

接受提交：

```text
d5cc596 feat(p7): finalize td-a completion evidence
6e4d108 docs(p7): record td-a e0 evidence
```

Ray wrapper 失败与恢复证据提交：

```text
ae98e1c docs(p7): record td-a ray wrapper failure
```

## 3. 验证质量

Executor E0 证据：

```text
focused = 67/67 pass
full suite = 486/486 pass
compileall = pass
all tmp/*.zsh zsh -n = pass
git diff --check = pass
CodeGraph sync = pass
```

Planner 独立复验：

```text
focused = 67/67 pass
full suite = 486/486 pass, 107.951 s
zsh minimal runtime reproduction = fail as expected with read-only variable: status
artifact hashes = pass
remaining calibration/control process = none observed
```

E0 汇总：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-e0/validation-summary.json
sha256 = ca994c9bb189451909306627fdf99376957edf876383937f3b58e85c9a3c4461
```

通过测试不能覆盖当前 wrapper 缺陷：`zsh -n` 只检查语法，现有 thermal wrapper 测试只检查静态
源码片段，没有执行正式 wrapper 的真实 zsh 状态机。

## 4. 实机进入与安全证据

离线进入证据：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-entry-20260721-040137/offline-entry.json
sha256 = 0eafb358b69936390e65535aba9ebfcf51572345f01161a42a7952362085ca2f
```

实机 preflight：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-entry-20260721-040137/device-preflight.json
sha256 = d9cfe1183233084f1dbbad932dfb82da9d066a1693962f05f8b7bd6cd6d0b57c
```

Preflight 证明 remote v2 capability、ISO `100`、aperture `implicit auto`、RAW、Ray intensity `0`、
strip identity 稳定且五通道全零。没有 capture、auto-exposure 或非零 probe。

失败 run：

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-ray-20260721-040137

plan.json sha256 = dcbbc250f4a48311ebabbb4ff0b4ec5c77d1631708d49eaa522fc447d2d78f77
run.json sha256 = 37f2b0e02e47f06e39fe1d69c6b4b72aa14a74dcf934e713b7b5624b195f2eed
isolation-gates.jsonl sha256 = 6391db7b3be69b3a4119a4773d644549fe6e50b318252f6fdc65db08c031baea
wrapper log sha256 = bc0e618f19ed2a1cc0956e3efb1bf7ce6bfb7d0e5a898deb0ae69e9f201552ad
```

失败发生在第一次 `cold_proxy_wait_s=1800`：

```text
command = 0
capture = 0
CR3 = 0
formal = 0
ambient = 0
strip run = not created
automatic retry = false
```

最终关闭证据：

```text
all-off-shell.json sha256 = e41c9caa98137b314a88d55a1ec276aca40044e00a350c7f39b46fd236179391
recovery-all-off.json sha256 = 98f083771475c80b09465e82ee7fe01ab0a5bc999e5b8397ed01108327d28c8f
```

两份证据均确认 strip 五通道全零、Ray intensity `0`。失败 run 必须永久保留，不得复用、补写为
complete 或删除以改善结论。

## 5. Planner Findings

### `P7-TD-A-W0-001` Must Fix / Agent-Fixable

正式 wrapper 在两个可达位置声明 zsh 只读特殊参数 `status`：

```text
tmp/run-p7-thermal-diagnostics.zsh:38  local status="$2"
tmp/run-p7-thermal-diagnostics.zsh:83  local final_exit status
```

因此首次 `write_json` 和 EXIT finalizer 都会失败，无法生成可信 wrapper completion evidence。最小
修复是改用非保留局部变量，并对正式 wrapper 增加真实 zsh runtime round-trip；不允许只补静态断言
或继续依赖 `zsh -n`。

### `P7-TD-A-W0-002` Should Fix / Agent-Fixable

活动 PLAN 的 combined artifact hard gate 要求 `input-manifest.json`，但当前
`analyze_td_a_pair` 只写 `td-a-combined-analysis.json` 与 `EXPERIMENT_SUMMARY.md`。若只修 wrapper，
完成真实 Ray/strip 后仍会在证据合同处再次阻塞。本项必须在同一离线纠偏包中完成，并通过独立 hash/
owner 重放和原子写入测试。

## 6. Human 授权判定

Planner 冻结以下消费边界：

```text
acquisition_authorization_consumption_boundary
= first_successful_nonzero_source_command
```

本次只执行了离线进入、设备 preflight、all-off、零状态 readback 和一个仍处于首次冷却等待的 child；
没有成功发送 Ray 或 strip 的非零 source command，也没有 capture。因此：

```text
p7_td_a_cold_settling_v1 authorization = not_consumed
current availability = suspended_pending_W0_planner_acceptance
```

这不是对新的设备操作授权。Executor 只能执行下一份 PLAN 的纯离线纠偏；修复通过后必须停止交还
Planner。只有 Planner 再次归档验收并在新 PLAN 中恢复该既有授权，Executor 才能重新执行 TD-A，且
必须使用全新 run 目录。

## 7. 残余风险

- wrapper 真实成功、child 非零、cleanup 非零、INT、TERM、HUP 六条路径尚未由 thermal wrapper
  production source 自身执行验证；
- `input-manifest.json` schema、原子写入和 tamper replay 尚未实现；
- 真实 TD-A science data 仍为零，settling 结论完全未知；
- preflight 只证明当时设备状态，不能复用于未来 TD-A 重启时跳过新的 preflight；
- `600 s` 仍不能自动解释为 steady；TD-B/C 和全部后续阶段继续锁定。

## 8. 精确下一分支

Executor 只能执行 `P7_TD_A_W0_WRAPPER_RUNTIME_OFFLINE_CORRECTION`：

1. 最小修复 thermal wrapper 的 zsh 保留变量；
2. 对同一正式 wrapper 增加六路径真实 runtime 测试；
3. 补齐 paired finalizer `input-manifest.json` 及 tamper/atomic/default-config 回归；
4. 完成 focused/full/compileall/all-wrapper-syntax/diff/CodeGraph 验证；
5. 更新 `EXECUTION_RESULT.md` 后停止交还 Planner。

该分支的设备、网络、`.env`、remote API、相机、Ray、ESPHome、`all_off`、CR3 和 heartbeat 均必须为
零。
