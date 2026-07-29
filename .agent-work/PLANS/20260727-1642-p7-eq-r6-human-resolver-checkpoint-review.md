# REF-P7-23-H1 / Human environment checkpoint

**计划状态：** `blocked_awaiting_human_environment_fact`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-H1`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-HUMAN-RESOLVER-CHECKPOINT-H1`

**Package kind：** `human_checkpoint_only_non_executable`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-HUMAN-RESOLVER-CHECKPOINT-H1","reference_task_id":"REF-P7-23-H1","parent_reference_task_id":"REF-P7-23","package_kind":"human_checkpoint_only_non_executable","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"await_one_current_human_environment_fact_for_same_stack_mdns_or_stable_explicit_address","executer_dispatch_authorized":false,"planner_dispatch_authorized":false,"device_access":0,"network_access_by_codex":0,"resolver_probe_by_codex":0,"cleanup_access":0,"capture":0,"nonzero_output":0,"eq_dispatch":0,"retry":0,"code_edits_authorized":false,"commit_authorized":false,"human_eq_confirmation_preserved":true,"human_eq_confirmation_consumed":false,"planner_stop_required":true}`

**当前唯一动作：** 等待Human提供一个当前、可复核的连接事实：要么project `.venv`内与production相同的
`aioesphomeapi` resolver现在能解析`bedroom-rgbww-strip.local`，要么该fixture有Human确认的稳定显式
IP及其router/static-assignment来源。

**唯一 Planner 停止点：** Human给出第4节A或B任一合格事实后，Planner重新验收并另写一个新PLAN；在此之前
保持blocked。不得dispatch Executer、运行Codex resolver/device probe、改代码、冻结历史IP或发起第三次device attempt。

## 1. Repeated failure review

```text
REF-P7-23 = rejected at live prelaunch
REF-P7-23-R1 = rejected at fresh zero-only prelaunch
REV-EQ-R6-LIVE-001 = BLOCKED_ON_HUMAN_ENVIRONMENT_CHECKPOINT
```

两次fresh production attempts共同事实：

```text
camera readiness = pass
Ray readiness = pass
bedroom-rgbww-strip.local = ResolveTimeoutAPIError
Python cleanup = attempted once, fail
shell cleanup = attempted once, fail
independent final-zero = attempted once, fail
RUN / Terminal / dispatch / candidate / capture / CR3 / nonzero = 0
extra probe / retry / repair = 0
Human EQ confirmation consumed = false
```

R1 review archive：

```text
.agent-work/PLANS/20260727-1621-p7-eq-r6-zero-reachability-r1-failure-review.md
SHA-256 70872074187d0db1618bc527bd5040d8cfdf70ff62dd2fb3faf6e9aed06b8242
```

Persistent debug note：

```text
.agent-work/debug/active/20260725-p7-td-b-e2-r1-hostname-and-progressive-evidence.md
SHA-256 0b9e6fa9e4a540bee753b29c09316fd4b1210a13fbd0577bcbdcd171b6e9c786
```

## 2. Why no third attempt or code correction

连续两个fresh root都在同一个production resolver boundary失败。evidence lifecycle本身完整，因此：

```text
automatic third prelaunch = forbidden
another zero-only gate before Human fact = forbidden
pure-offline forensic replay = no new decision value
```

现有single source of truth已经支持：

```python
CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_HOST
```

并在连接时继续冻结：

```text
expected_name = bedroom-rgbww-strip
port = 6053
```

因此无需增加IP fallback、平行client、安全墙或硬编码地址。缺少的是Human-owned环境事实，不是实现入口。

## 3. Historical ping is insufficient

Human先前报告：

```text
ping bedroom-rgbww-strip.local
-> 192.168.0.74
```

该结果只证明当时user shell/OS resolver可用；它早于本次连续两个production
`aioesphomeapi.host_resolver.async_resolve_host` timeout。Planner不会把`192.168.0.74`自动解释为当前、
稳定、可冻结的fixture地址。

## 4. Human checkpoint — choose A or B

Human只需完成A或B之一并把结果发回当前task。不要提供任何API key、token或`.env`内容。

### A. Same-stack current mDNS proof

确认fixture已通电、连接当前local lab Wi-Fi后，在Human自己的macOS Terminal中从repo root只运行一次：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW
.venv/bin/python - <<'PY'
import asyncio
import json

from aioesphomeapi.host_resolver import async_resolve_host

async def main() -> None:
    rows = await async_resolve_host(
        ["bedroom-rgbww-strip.local"],
        6053,
        timeout=30.0,
    )
    print(json.dumps(
        [
            {
                "family": row.family,
                "type": row.type,
                "proto": row.proto,
                "sockaddr": list(row.sockaddr),
            }
            for row in rows
        ],
        sort_keys=True,
        separators=(",", ":"),
    ))

asyncio.run(main())
PY
```

该命令只做与production相同library stack的hostname resolution；不读取project `.env`或ESPHome key，不连接
6053、不发送zero/nonzero命令，也不消费EQ确认。

Human回传：

```text
执行时间与时区
exit code
完整单行stdout，或完整exception type/message
```

A通过要求：

```text
exit = 0
stdout = non-empty JSON array
至少一个sockaddr host为当前local address
```

### B. Stable explicit address proof

如果`.local`仍不能解析，但Human已在router或fixture配置中确认stable assignment，可回传：

```text
current IPv4 or IPv6 address
来源 = router DHCP reservation / static assignment / equivalent stable owner
确认该assignment属于bedroom-rgbww-strip
确认地址当前有效的时间与时区
```

单次ping观察、历史lease、临时DHCP地址或猜测不满足B。IP本身可记录；不要回传Wi-Fi密码、ESPHome
encryption key或router credentials。

后续PLAN可用现有
`CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_HOST=<Human-confirmed stable address>`入口，并继续由
`expected_name=bedroom-rgbww-strip` fail closed。当前H1不授权使用该入口。

## 5. Branches after Human response

```text
A pass:
  Planner可写一个新的fresh-root bounded activation/reachability package；
  是否继续用.local由新PLAN冻结。

B pass:
  Planner可写一个新的fresh-root package；
  exact explicit address以runtime environment input冻结，不改source，不hard-code。

A fail and no B:
  route remains blocked；
  Human先修复fixture power/Wi-Fi/local-network/mDNS，再请求新的checkpoint。
```

任何分支都不自动授权capture、EQ dispatch、retry或复用旧FAMILY。

## 6. Zero execution boundary

本active PLAN没有Executer package。必须保持：

```text
Codex network / DNS / resolver / device calls = 0
camera / Ray / strip / cleanup / final-zero = 0
capture / CR3 / nonzero / EQ = 0
new external root / artifact = 0
source/test/docs/skill/wrapper/config edit = 0
commit = 0
Human EQ confirmation = preserved and unconsumed
```

Orchestrator只向Human呈现本checkpoint并等待回复；不得把H1交给Executer运行。

## 7. 维护性判断

该checkpoint遵循现有host environment入口和expected-name身份owner，避免为外部mDNS状态新增fallback、
硬编码IP或第三次盲试。当前不需要Advisor科学决策或代码重构；需要Human提供一个当前环境事实。

---

## 8. Planner review（2026-07-27 16:42 MDT）

Human first reported current ordinary ping success, then ran the exact H1-A project `.venv` command. The command
returned to the shell with a traceback at:

```text
list(row.sockaddr)
TypeError: 'IPv4Sockaddr' object is not iterable
```

The H1 literal output acceptance (`exit=0` plus JSON stdout) was not met. However, the failure is in the
Planner-authored formatter after the environment fact was already established:

```text
async_resolve_host awaited without ResolveTimeoutAPIError
rows comprehension entered
at least one row existed
row.sockaddr was IPv4Sockaddr
```

Offline, network-free API contract inspection confirmed:

```text
IPv4Sockaddr dataclass fields = address, port
IPv6Sockaddr dataclass fields = address, port, flowinfo, scope_id
AddrInfo dataclass fields = family, type, proto, sockaddr
```

Decision：

```text
REF-P7-23-H1 = ACCEPTED_CORE_ENVIRONMENT_FACT
H1-A JSON formatting criterion = INVALIDATED_BY_PLANNER_COMMAND_BUG
same-stack resolver returned non-empty rows = proven
stable explicit IP branch B = not needed
Human repeat network probe = not required
Human EQ confirmation = preserved and unconsumed
REV-EQ-R6-LIVE-001 = READY_FOR_ZERO_ONLY_RECOVERY_GATE
next = REF-P7-23-R2
```

The missing exact address/time/zero exit does not undermine the narrow fact H1 was created to establish. It does mean
the next package cannot jump directly to live EQ: it must first obtain a fresh generation-bearing strip zero and full
cleanup/final-zero seal through the existing production owner.
