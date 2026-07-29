# REF-P7-01 / Z0-R3-C1 editable-owner 首失败 Planner 验收归档

**验收时间：** `2026-07-25T19:19:51-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`70e57af6283899764c89172c82fe448035d20003eb76ad1dea2d8c26515f2295`

**Planner 决定：** `rejected_first_owner_failure; minimal_offline_c2_required`

**精确下一分支：** `P7-TD-B-Z0-R3-C2_OFFLINE_EDITABLE_OWNER_GATE`

## 1. 被审范围与停止点

Executor在唯一fresh offline root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r3-c1-offline/20260726T010648Z/`

建立package并运行driver恰好一次。source freeze、compile without bytecode与`zsh -n`通过；唯一runtime availability probe exit `0`，确认具名 `.venv/bin/python` symlink chain、resolved Python `3.13.2` binary、`aioesphomeapi 45.0.4`、production import origin及audit-hook零socket/DNS/connect/subprocess/write/secret-open。随后validator因probe value中的`project.direct_url=null`拒绝`editable project owner`，并按首失败规则停止；copy/terminal/accounting/lifecycle matrices均未启动。

这不是runtime/dependency缺失。停止后只读发现同venv ordinary non-symlink：

`/Users/ibobby/Projects/WLED-RGBWW/.venv/lib/python3.13/site-packages/__editable__.camera_based_rgbww_optimizer-0.1.0.pth`

bytes `38`、SHA-256 `59866e26af450f08ce4e5ac37cd4b27ce16dbb3096b90c52613bea0a0b8fbb41`，唯一内容行为 `/Users/ibobby/Projects/WLED-RGBWW/src` 加单个 LF，normalized target exact为repository `src`。production owner import origin同时exact指向该src tree。

## 2. Canonical evidence

| evidence | SHA-256 |
| --- | --- |
| `runtime-availability.json` | `7f04684e3562cd6d1015f18f6d51169fdf86456c6d13299b06146a70e16bfaa4` |
| `first-failure.json` | `bdf80b47494086a7151fede1be80dac2e0a3bca675077e2c3225b1475aad6da6` |
| `post-failure-audit.json` | `4b090f54d2832fe62885b30b6ac7a23e32644857e2fe44c9b684c21e7a6b99ff` |
| `zero-budget-audit.json` | `b38d22d077805b2953978ce5b6dddf4ee4282178927c44d17901cbbfdb151b85` |
| `validation-summary.json` | `4637b896aee8012c871f8fc860dfcc0e961c1e51258cfe2ddccf230dfdcd37df` |
| `source-manifest.json` | `18bdeb8d352c4cb69e0c4ea78d7d928223881001376a21cf5e3b0e1a998660ff` |
| `source/controller.py` | `b793592b0bd10116c349441f8aa180009fd62d7bbdced7b35c479a25034ec9ca` |
| `source/real_adapter.py` | `2c37162dd94805ce8c48035faf9b0a54e6243d4a82edd3218c8ca018986492d3` |
| `source/run_wrapper.zsh` | `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6` |

## 3. Planner 独立重放与 owner 判定

1. 上述9个files的bytes/SHA及structured JSON全部exact；failure boundary为`runtime_editable_project_owner_validation`，matrix count、device/network/install及residual process均为0。
2. `.pth`由Planner以lstat/no-follow重放：ordinary、non-symlink、nlink 1、bytes/hash exact，UTF-8单行加单个LF，normalized path exact `/Users/ibobby/Projects/WLED-RGBWW/src`，无第二行、import语句或extra path。
3. 同distribution的physical `direct_url.json`当前也是ordinary non-symlink，bytes `83`、SHA-256 `0119c826f52a69b122cd991f3970b5025941e92f0ac17bb738358f6b0b95f3f2`，strict value为 `dir_info.editable=true` 与 exact repository file URL。C1 probe记录的null是其读取/序列化结果，首次artifact不改写；C2不得再把单一metadata API返回当作唯一owner。
4. 合法editable owner应由direct-url或same-venv exact `.pth`提供，并始终与production import origin三方一致。两者同时存在时只有normalized repository root一致才可接受；冲突、extra owner/path或任一symlink必须fail closed。
5. HEAD exact `0387bcfa53e52ee7f99d5308886e2b7873fe49f5`。Planner未运行C1 source/matrices，未读取secrets、联网、安装、访问设备或修改production/Git。

## 4. Finding 状态与下一分支

`REV-Z0-R3-RUNTIME-007`保持Open，但runtime chain、Python、aio distribution、production origin与audit-hook子合同已取得有效通过证据；剩余首阻塞仅为editable owner classification。`REV-Z0-R3-TERMINAL-FIXTURE-008`与`REV-Z0-R3-SECRET-ACCOUNTING-009`尚未被C1执行验证，继续Open，不得视为失败或通过。

下一active PLAN只能做最小C2：从冻结C1 source修正editable gate，使其接受exact direct-url owner、exact same-venv `.pth` owner或两者一致组合；拒绝冲突、extra path、symlink及outside-repo。gate通过后才运行C1尚未消费的runtime propagation、copy、terminal、accounting和offline lifecycle matrices。不得访问network/device、安装依赖、运行real Z0或修改production。

无需Human修复环境，也不需要Advisor；问题是external editable metadata owner分类。

## 5. Orchestrator reference 建议

Planner不修改 `.agent-work/FULL_PLAN_REFERENCE.md`。建议把 `REF-P7-01` 当前子状态更新为 `P7-TD-B-Z0-R3-C2_OFFLINE_EDITABLE_OWNER_GATE`，保留三个REV Open及Z0/E2/formal锁。
