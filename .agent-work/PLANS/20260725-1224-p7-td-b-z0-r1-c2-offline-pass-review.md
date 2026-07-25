# P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C2 offline correction Planner 验收归档

**验收时间：** `2026-07-25T12:24:48-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`c056fd40de61de20f3927484762b58c983491f6e43a2104ff048e3bf2f5f8728`

**Planner 决定：** `accepted_offline_harness_correction; four_review_ids_closed`

**精确下一分支：** `P7-TD-B-F0B-R1-C3-E2-R1-Z0-R2_ONE_REAL_ZERO_ONLY_GATE`

## 被审范围与结果

被审 PLAN 只允许在一个 fresh external offline root 修复 source hygiene、mechanical PLAN identity 与真实 injected
wrapper lifecycle，不允许 fresh/real Z0、production import、secrets、hostname、network 或 device。Executor 在：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-c2-offline/20260725T181230Z`

完成 source hygiene `10/10`、identity `14/14`、actual child/zsh trap/post-wrapper lifecycle `18/18`。最终状态为
`offline_z0_harness_correction_pass_waiting_for_planner`；未运行 Z0 或任何外部设备操作。

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `validation-summary.json` | 4087 | `63ef3caaf8636366d0bb5dd047e6f32693b4a9fb6893df1afe5191279fe5bd35` |
| `source-manifest.json` | 781 | `24524e8a17f7e4dd1f2d87cb4a9a5b2931d288049a8798fb3082499e3b01d6ce` |
| `compile-preflight.json` | 1061 | `8928e72a1743701419ecfaa346d9d61d50dfecadfde8b64fb7dd297fb73877c2` |
| `plan-freeze.json` | 714 | `bdbf1babf3193d8f3244f41c41143c1b638b540488623c39e52b50664f5feedf` |
| `lifecycle-matrix.json` | 123816 | `24e995ec6ad8bd862784ec89689d9a2466d4925135dbadf71d4f2c8b24c86db7` |
| `terminal-summary.json` | 102700 | `832425e1ba10ab881a3693ca49639167efe3bbe62a08b8baf9ceb8c558faf1d9` |
| `terminal-metadata.json` | 1469 | `57f1eb0bb71216a465eb08a3a8cdbfa637d50d5452364278b676f93a8eb9ab50` |
| `.agent-work/EXECUTION_RESULT.md` at review | 158639 | `69f7d7c834275a3164dfc15e57de50041f827f148d27dcee74b0469cb91bf0d4` |

## Planner 独立重放

1. direct hashes 与 Executor 交接一致；terminal summary 的 527 个 canonical artifacts 全部 live path/bytes/SHA-256
   匹配，mismatch `0`。
2. correction root 中全部 `453/453` JSON strict parse、真实 newline；source entries 恰为 `harness.py` 与
   `run_wrapper.zsh`，actual source bytecode/`__pycache__` 为 `0`。
3. compile evidence 明确 `python_execution=0`、Python compile pass、zsh `-n` exit `0`、stdout/stderr `0/0`；source
   manifest 在 preflight 前后 device/inode/mtime/bytes/hash 全等。
4. source-hygiene 10 cases 覆盖 exact inventory、`__pycache__`、`.pyc`、unknown、file/parent symlink、missing、bytes/inode
   mutation 与 manifest tamper；所有负例在 identity/lifecycle calls 前 fail closed。
5. identity 14 cases 覆盖 mutation/inode、PLAN/parent symlink、outside-root、missing/FIFO/directory、contract
   missing/duplicate、reference/package/head drift、freeze/source binding tamper；production import/secrets/network/device 为 `0`。
6. lifecycle 有 explicit 18 cases，每 case 恰好 `5 attempt + 5 result + 5 adapter-call`，总数 `90/90/90`；每个 result
   的 attempt path/hash live binding 通过，stage multiplicity 与自动 retry 均正确。
7. full success 五次 returned-success；primary/Python/child/shell/independent failure、watchdog unknown 和六个 response drift
   subcases均 fail closed。SIGINT/SIGTERM/SIGHUP 的 child/wrapper exits 分别为 `130/143/129`，trap count 均 `1`；signal
   precedence 为 `143`，independent finalizer 均在 wrapper 完全退出后开始。
8. C1 与 Z0-R1 roots before/after manifests byte-identical；silent sealer logs `0/0` bytes；repair/unexpected symlink/source/
   production drift均为空。HEAD 为 `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`。
9. 本次 Planner review 未 import/compile correction source，未读取 secrets/`.env`，未解析 hostname 或访问 network/device，
   未执行 Z0、E2、capture、formal、analyzer、stage、commit 或 release 操作。

## Findings 与处置

### `REV-Z0-R1-PLAN-ID-001` — Closed

current PLAN bytes/hash 不再手填；no-follow fd mechanical freeze 与 independent replay覆盖内容、inode/device/mtime和唯一
machine contract，mutation/tamper均 fail closed。

### `REV-Z0-R1-WRAPPER-SIGNAL-002` — Closed

真实 zsh wrapper 持久化 exact signal name/code，并证明 INT/TERM/HUP `128+n` 与 signal-over-child/cleanup precedence。

### `REV-Z0-R1-MATRIX-003` — Closed

matrix 实际启动 child、zsh wrapper、EXIT trap 和 post-wrapper independent finalizer；90 stage bundles 来自真实 control flow，
不是直接合成 aggregate。

### `REV-Z0-R1-C1-SOURCE-HYGIENE-004` — Closed

source 预检为 compile-only/no execution，所有 Python process 禁止 bytecode，explicit two-file source inventory 与污染负例通过。

## 验收决定、残余风险与下一分支

四个 offline harness findings 均由独立 replay 关闭，接受 C2。该接受不证明 hostname/ESPHome reachable 或 strip 当前为零，
也不授权 E2/formal。首次 Z0-R1 在 pre-device gate 失败，real wrapper与五个 ESPHome semantic attempts均为 `0`；因此 exact
zero-only real gate 尚未消费。

下一份 PLAN 可单独放行一次 fresh Z0-R2：在 fresh root 机械冻结新 PLAN与已接受 C2 evidence，先运行 final-source no-device
self-check，全部通过后才按五个 assigned zero-only stages各调用一次 exact production `verified_light`。无论 pass/fail均回
Planner；不得同包进入 E2。无需 Advisor 或 Human 危险操作授权。
