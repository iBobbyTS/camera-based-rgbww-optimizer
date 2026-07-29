# REF-P7-01 / Z0-R3 runtime hard-failure Planner 验收归档

**验收时间：** `2026-07-25T19:01:06-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`8f182b8bd384c2230d89fbddc7d5769aef34d3db1274b8df5fc56a3af10fe127`

**Planner 决定：** `rejected_valid_hard_failure; offline_runtime_and_evidence_correction_required`

**精确下一分支：** `P7-TD-B-Z0-R3-C1_OFFLINE_RUNTIME_EVIDENCE_CORRECTION`

## 1. 被审范围与停止点

Executor 在唯一 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r3/20260726T005105Z/`

完成唯一 no-device self-check：fake matrix `17/17`、binary-copy regression `7/7`，随后运行 real wrapper 恰好一次。五个具名 stage 的 attempt/call/result cardinality均为 `5/5/5`，但全部在 `/usr/bin/python3` 内调用 production `verified_light` 时以 `ModuleNotFoundError: No module named 'aioesphomeapi'` 失败。production source先在 `async_verified_light` 函数体 import `aioesphomeapi`，之后才调用 `_load_api_encryption_key`；因此异常发生在 hostname resolution、network connect、device API和production secret load前。

child finally、shell EXIT trap及independent finalizer的所有具名cleanup slots均已执行；wrapper/finalizer exit均为 `1`，owned residual process为 `0`。Executor未切换runtime、未重试、未使用IP fallback/standalone probe，也未进入E2/formal。

## 2. Canonical evidence

| evidence | SHA-256 |
| --- | --- |
| `pre-device-pass.json` | `f5a455a3390b2545fa3f8b6d2a63da052d9d9309e0acf67d3807e3380eaa2803` |
| `lineage-classification.json` | `520fa75b557ca862a739116aa12c2fb138db852e3343e4b97f23fb4fe3636348` |
| `driver-result.json` | `3c7c0af40a6f3b05121f758a27604471ff14f084a4f9872c573f2147540c14ad` |
| `terminal-seal.json` | `0788356b1f666dd7b6eb18d863196d622b662e9e4689873a74023d8e746a8b2f` |
| `post-execution-audit.json` | `ec44c4c36cad16344cd5662d4f28e6f11101084f28f08fa1593729bee500e57c` |
| `zero-budget-audit.json` | `42992a5d065b83986e10d98cf9681c3bb356381d30561ce5dbd26dbedf39b589` |
| `validation-summary.json` | `1fd26f992dee5aeba107fac451b1b72d52e8e5f6397731e4cee401396ea039c0` |
| `source/controller.py` | `aba4ab485a8035446eb7ccc927c03cbb9f31d928ac18794a4dd3080961064a36` |
| `source/run_wrapper.zsh` | `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6` |
| `source/real_adapter.py` | `c2bc28683a1e789f1945164471f6693f48c79dd3c6dcdb1b7e36d1f0e37fc186` |

## 3. Planner 独立重放

1. 逐项重算上述10个hash并strict parse structured JSON；全部exact。五个stage result均为 `raised_failure`、response `null`、error class `ModuleNotFoundError`，message具名 `aioesphomeapi`。
2. production owner仍为ordinary non-symlink，bytes `12538`、SHA-256 `0a5b6258fe3ea8519f697c4351eac9ac4243bbbabe0d30530f4c30564c972872`。源码顺序确认为函数体 `import aioesphomeapi` 后才构造payload并调用 `_load_api_encryption_key`，所以本轮production secret load attempt/success实际为 `0/0`。
3. 项目文档指定runtime `.venv/bin/python` 当前存在，解析至 `/Users/ibobby/miniconda3/bin/python3.13`，Python `3.13.2`，resolved binary bytes `6095216`、SHA-256 `0c90ae5d966a4a356f5e80ded47bdbc7264f781916f45f879b77747ef3cb803c`。离线 `find_spec`/distribution metadata确认 `aioesphomeapi 45.0.4` 位于该venv，project package也解析到当前repository source。`/usr/bin/python3` 为Python `3.9.6`，两者均不可定位；因此不是Human环境blocker，而是external controller runtime selection defect。
4. terminal seal把self-check刻意构造的两个symlink负例 `selfcheck/copy/source-symlink/src`、`selfcheck/copy/destination-symlink/copy` 计入全局 `nonregular`。它们是具名expected-negative fixture，不应进入canonical ordinary-file mismatch；但也不得被follow或推广为任意symlink许可。
5. zero-budget把 `production_secret_loads` 按5个calls保守记为5，和异常边界冲突；accepted real adapter自己的secret identity no-follow read/hash确为5。首次artifact保持不改，Z0-R3仍然hard-fail。
6. HEAD exact `0387bcfa53e52ee7f99d5308886e2b7873fe49f5`；本review未访问network/hostname/device、未打开secrets、未运行cleanup/Z0/E2/formal、未安装依赖或修改production/Git。

## 4. Findings

### `REV-Z0-R3-RUNTIME-007` — Open

real wrapper继承Planner/Executor启动时的 `/usr/bin/python3`，没有冻结项目runtime，也没有在device gate前验证production dependency importability。corrective owner必须只接受具名 `.venv/bin/python`，记录symlink chain、resolved binary identity、Python version、`aioesphomeapi` distribution/module identity及production owner origin；任何缺失或漂移在network/device前fail closed。禁止fallback到system Python、PATH search、安装依赖或联网。

### `REV-Z0-R3-TERMINAL-FIXTURE-008` — Open

terminal owner把计划内negative symlink fixture与canonical evidence混为同一policy。corrective owner必须把两个exact fixture路径作为独立 no-follow `planned_negative_fixture` 分类，记录lstat/readlink identity并从ordinary canonical inventory排除；unknown path/target/type/multiplicity drift仍fail closed，source/PLAN/runtime/production/secrets边界继续禁止symlink例外。

### `REV-Z0-R3-SECRET-ACCOUNTING-009` — Open

production secret load不能从assigned call数推导。corrective owner必须分别记录adapter secret identity read attempt/success、production import attempt/success、production secret load attempt/success；production load事件须绑定实际 `_load_api_encryption_key` 入口/返回，不得记录secret value。import failure应严格得到load `0/0`；load failure为 `1/0`；load success后下游失败仍为 `1/1`。

## 5. 下一分支、授权与 Advisor 判断

下一 active PLAN只能运行一次纯离线corrective package：冻结并验证现有 `.venv` runtime，无网络、无安装、无device/hostname、无production change；纠偏planned fixture terminal classification与secret accounting并运行adversarial matrices。若具名runtime或dependency不存在，必须写Human/environment blocker并停，不得安装或fallback。

本次是external execution/evidence ownership问题，没有科学统计、实验方向或GUIDE冲突，不需要Advisor。任何新的real device run必须等corrective result由Planner接受后另写fresh Z0 PLAN；E2/formal继续锁定。

## 6. Orchestrator reference 建议

Planner不修改 `.agent-work/FULL_PLAN_REFERENCE.md`。建议Orchestrator把Z0-R3记录为valid runtime hard-failure，打开上述三个REV，将 `REF-P7-01` 当前子状态改为 `P7-TD-B-Z0-R3-C1_OFFLINE_RUNTIME_EVIDENCE_CORRECTION`，并保持 `REF-P7-02`、E2与formal锁定。
