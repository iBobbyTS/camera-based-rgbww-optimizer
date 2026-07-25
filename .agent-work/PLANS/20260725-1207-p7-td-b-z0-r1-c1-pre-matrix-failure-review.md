# P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C1 pre-matrix hard-failure Planner 验收归档

**验收时间：** `2026-07-25T12:07:38-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`15cdfa3455817b4b69d964b4cdc131b16f9696ce45cda97d5b62e2bc0193c90f`

**Planner 决定：** `accepted_as_valid_pre_matrix_hard_failure; no_review_id_closed`

**精确下一分支：** `P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C2_OFFLINE_SOURCE_HYGIENE_AND_HARNESS_CORRECTION`

## 被审范围与结果

被审 PLAN 只允许在一个 fresh external offline root 修正 PLAN identity 与实际 wrapper lifecycle，不允许 fresh/real Z0、
production import、secrets、hostname、network 或 device。Executor 创建：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-c1-offline/20260725T175533Z`

mechanical PLAN freeze 成功后，Executor 为单独预检 `plan_identity` owner 而 import external `source/harness.py`；Python 在
source root 生成 `source/__pycache__/harness.cpython-313.pyc`。正式 source-manifest owner 要求 source entries 全是普通文件，
在 matrix 前以 `ValueError: source invalid: source/__pycache__` fail closed。旧 root 未修补、删除或重跑；identity/lifecycle
matrix 均未开始。

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `validation-summary.json` | 1952 | `59472a77c8dcf8aa5ae1e93b83257fcd00e84bd9de6b60bbf3f19ef0ad69fc62` |
| `plan-freeze.json` | 714 | `4157073c687234005618740f5e96038dddc3de9f00c9870ca8a27b430dc0179c` |
| `hard-failure.json` | 795 | `ac80c428aa67595581f0ac3681ab6dd6497fd4fc1b072b57c79ceb9a131e0d3c` |
| `terminal-summary.json` | 2173 | `3575a75fe5f27ee85e7f29648f094bab1fea4642e81c8e4a11d8a585fc90b6ca` |
| `terminal-metadata.json` | 669 | `823ff190d8425f94e1d3177302304b265ffbc17939c0fc5229281df886f5ce09` |
| `frozen/failed-root-before.json` | 1371 | `2e230418e91ef778d2e7c2c60952a97b130db7630d4d5b3c71f1fa231659a741` |
| `frozen/failed-root-after.json` | 1371 | `2e230418e91ef778d2e7c2c60952a97b130db7630d4d5b3c71f1fa231659a741` |
| `.agent-work/EXECUTION_RESULT.md` at review | 152994 | `ff74d9075d4d8ec4d73712af14910bec861c61e3a67abf118ad4c57c9aad07c6` |

## Planner 独立重放

1. correction root 中有 14 个普通文件、6 个目录、symlink `0`；污染 entry 恰为
   `source/__pycache__/harness.cpython-313.pyc`，bytes `62045`。
2. build stderr 的完整 traceback 在 `source_manifest()` 对 `source/__pycache__` 执行 `is_file()` 检查时抛出 exact
   `ValueError`；该调用位于两个 matrix 之前。
3. `plan-freeze.json` 从同一 fd 机械记录 active PLAN bytes `11523`、SHA-256
   `15cdfa3455817b4b69d964b4cdc131b16f9696ce45cda97d5b62e2bc0193c90f`、inode/device/mtime、machine contract 与
   HEAD `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`，字段与被审 PLAN 一致。
4. terminal summary 的 10 个 canonical artifacts live bytes/SHA-256 replay `10/10`，mismatch `0`；7 个 JSON strict
   parse、真实 newline，symlink/repair artifacts 均为 `0`，sealer stdout/stderr 为 `0` bytes。
5. identity cases、lifecycle cases、per-case stage sum 与 sealed stage count 全为 `0`。这只证明 matrix 未消费，不能关闭
   `REV-Z0-R1-PLAN-ID-001`、`REV-Z0-R1-WRAPPER-SIGNAL-002` 或 `REV-Z0-R1-MATRIX-003`。
6. 上一 Z0-R1 root before/after 仍为相同 8-file manifest；HEAD、production scope 和 Planner-owned files 无执行期漂移。
7. 本次 Planner review 未 import/compile correction source，未读取 secrets/`.env`，未解析 hostname 或访问 network/device，
   未执行 matrix、correction、Z0、E2、capture、formal、analyzer、stage、commit 或 release 操作。

## Finding 与决定

### `REV-Z0-R1-C1-SOURCE-HYGIENE-004` — Correction required

根因是 preflight 通过 import 执行待冻结 source，使验证本身改变 source inventory。`__pycache__` 不是可忽略 temporary file：
它是未声明 executable-derived artifact，source owner 正确 fail closed。不得通过删除污染、忽略 glob 或把 `__pycache__` 加入
允许列表修复。

下一包必须同时：

- Python 语法预检只读源码并调用 `compile(..., mode="exec")`，不得 import/exec/runpy/loader；
- 所有 Python subprocess 显式设置 `PYTHONDONTWRITEBYTECODE=1`，并在 Python 入口设置 `sys.dont_write_bytecode=True` 作为
  defense-in-depth；
- source manifest 使用显式、immutable exact file inventory，拒绝额外 file/directory/symlink；
- 用 fake source fixture 覆盖 `__pycache__` directory、`.pyc`、unknown file、symlink、source mutation 等污染负例；
- 在 source freeze 后和每个 matrix/terminal phase 前后重放 exact inventory，任何污染 fail closed。

## 验收决定、残余风险与下一分支

本结果满足 active PLAN 的 fail-closed 停止点，接受为 valid pre-matrix failure；PLAN identity 与 wrapper correction 尚未被
验证。C1 package budget 已消费，禁止修改、删除、复用或重跑该 root。

唯一下一包仍为纯离线 external harness correction，先关闭 source-hygiene finding，再运行原计划的 identity/lifecycle
matrices。即使通过也必须回 Planner；fresh Z0、E2、设备和 formal 不得同包启动。无需 Advisor 或 Human 授权。
