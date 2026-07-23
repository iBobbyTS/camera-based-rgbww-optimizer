# P7 TD-A Wrapper Runtime Failure

**状态：** `resolved_by_960484e`

**Planner 验收：** `2026-07-21 accepted`

## Original Failure

- Production wrapper：`tmp/run-p7-thermal-diagnostics.zsh`。
- `write_json()` 曾声明 `local status="$2"`。
- `finalize()` 曾声明 `local final_exit status`。
- zsh 的 `status` 是只读特殊参数，正式 Ray run 在首次 cold proxy 等待期间失败。
- 失败时 command、capture、CR3 均为零；strip 未启动，shell cleanup 和独立 recovery 均成功。
- `zsh -n` 无法发现该运行时错误，旧 thermal wrapper 测试只做静态源码断言。

## Original Evidence

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-ray-20260721-040137

wrapper log sha256 = bc0e618f19ed2a1cc0956e3efb1bf7ce6bfb7d0e5a898deb0ae69e9f201552ad
plan.json sha256 = dcbbc250f4a48311ebabbb4ff0b4ec5c77d1631708d49eaa522fc447d2d78f77
run.json sha256 = 37f2b0e02e47f06e39fe1d69c6b4b72aa14a74dcf934e713b7b5624b195f2eed
isolation ledger sha256 = 6391db7b3be69b3a4119a4773d644549fe6e50b318252f6fdc65db08c031baea
shell cleanup sha256 = e41c9caa98137b314a88d55a1ec276aca40044e00a350c7f39b46fd236179391
recovery sha256 = 98f083771475c80b09465e82ee7fe01ab0a5bc999e5b8397ed01108327d28c8f
```

## Resolution

提交 `960484e1107cbcfb3304075a5ac54a0fbe6a382e`：

- `write_json()` 改用 `result_status`；
- `finalize()` 改用 `final_status`；
- production wrapper exact bytes 通过 success、child failure、cleanup failure、INT、TERM、HUP 六条
  真实 zsh runtime 路径；
- runner/cleanup 各调用一次，exit/status/signal exact，零残留 process；
- paired finalizer 同时补齐 `input-manifest.json` 和 retained-byte replay，避免下一次真实 TD-A 在
  combined artifact gate 再次阻塞。

Validation：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/
  p7-td-a-w0-20260721-054106/validation-summary.json
sha256 = 94ce883c689fed4dc43f1ce1db0396fe41f11846d167604fa9cc8a6c017647af

Executor focused = 48/48
Executor full = 493/493
Planner focused = 48/48
Planner full = 493/493
```

Planner 归档：

```text
.agent-work/PLANS/20260721-0009-p7-td-a-w0.md
```

## Authorization Result

```text
consumption boundary = first successful nonzero source command
observed successful nonzero source command in failed run = 0
authorization = not_consumed
W0 acceptance = existing exact TD-A authorization restored in next PLAN
```

下一次 TD-A 必须使用全新目录和新的 preflight；旧失败 run 永久保留，不复用或改写。
