# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED_G4_03_SEALED_FAIL_EVIDENCE`
- archived_at: `2026-08-03T13:57:06-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-03-ZERO-READINESS / sealed-fail root and implementation handoff`
- source_checkpoint: `e64cdaf309ac623f978e1c8aa08988707aa0c344`
- original_body_bytes: `10375`
- original_body_sha256: `110285565248da6e0fd0b9e200d88454ba156413a357afaaaa55763d8392b753`
- terminal_disposition: `ACCEPTED_G4_03_SEALED_FAIL_RAY_CONTROLLER_UNREACHABLE_FINAL_ZERO_UNPROVEN`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1357.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_FAIL_CLOSED_FULL_UPDATE_AND_FOCUSED_COMMIT`
- historical_non_executable: `true`

该archive是失败证据的正式review record；它不表示G4-03 PASS、hardware ready、Ray zero proven、G4-04 unlocked，
也不授权retry、alternate root、service启动、device/release/formal操作。下方逐字节保留reviewed ER body。

---

# REF-G4-03-ZERO-READINESS：Executer handoff

**状态：** `SEALED_FAIL_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-ZERO-READINESS-SINGLE-OWNER-V1`

**Reference task：** `REF-G4-03-ZERO-READINESS`

**Planner stop：** `RETURN_FOR_G4_03_ZERO_READINESS_REVIEW`

## 1. 结论

唯一一次真实前台 wrapper 已执行并以 exit `20` 结束。fresh root 已成功独占创建并完整冻结为14项、0700/0600、canonical evidence package；terminal seal 为
`sealed_fail_waiting_planner_review`。主阶段在首次 Ray zero 调用命中
`ConnectionRefusedError: [Errno 61] Connection refused`，endpoint为冻结的
`ws://127.0.0.1:33782`。随后Python finally、shell cleanup和independent-final-zero中的Ray zero也均因同一连接拒绝失败。

strip的三次repo-owned independent verified-zero全部成功，identity稳定，observed generation依次为`2`、`3`、`5`，五通道均为零；shell cleanup中的strip off也成功。Ray最终状态无法证明为零，camera readiness因前序Ray失败未调用。因此本结果不是G4-03 PASS candidate，不授予G4-04、release consumption、formal R6或TD-C权限。

按PLAN的real retry `0`和alternate root `0`约束，Executer未重试、未换root、未修设备或controller、未修改候选实现，也未进入后续阶段。

## 2. Activation与machine contract intake

- 执行HEAD：`e64cdaf309ac623f978e1c8aa08988707aa0c344`
- branch：`main`
- direct parent：`5d05cc14286af0f96b9021401f44d3c72a348911`
- activation subject：`docs(plan): activate g4 zero readiness`
- activation changed paths exact：
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/EXECUTION_RESULT-20260803-1316.md`
  - `.agent-work/archived/PLAN-20260803-1316.md`
- repo-owned PLAN/FULL strict parser：PASS；contract
  `G4-ZERO-READINESS-SINGLE-OWNER-V1`；active task/count为
  `REF-G4-03-ZERO-READINESS` / `1`，PLAN与FULL一致。
- canonical next：`REF-G4-03-ZERO-READINESS`。
- retained R3：`RETAINED_UNVALIDATED_UNCONSUMED`；本包access/consumption均为`0`。
- reviewed PLAN archive：bytes `8895`，SHA-256
  `5eb3d0076f27fafcd69a8794511f29ac23798894abe92a5a0332f0f53966d88b`；body bytes `7943`，body SHA-256
  `6f53b21bc5c2469c76a6b4fc59a81da89d7170870d6b524f2785eb35d8884e36`。
- reviewed ER archive：bytes `2439`，SHA-256
  `b25a380efaf685057e0c90573eea30854ffafb7c5116d4af06bc92a27a4400fc`；body bytes `1489`，body SHA-256
  `43b03d563998659ce5a0b1c196426a7057f89935458d9b49e5e1f65a898e06f6`。
- intake时工作树干净；fresh root及symlink均不存在。

## 3. Repo-owned owner、tests与wrapper

本包新增且仅新增一个composition owner、一个行为测试文件和一个tracked wrapper：

| path | bytes | SHA-256 |
|---|---:|---|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py` | 28288 | `fea119e6a49825cf5858732c5a27dd0187020b70bc6fa5d6e8e2b3c428dacc8c` |
| `tests/test_p7_successor_zero_readiness.py` | 16311 | `5e2efcbab079b46ca18e874ee5d684a73586517b58560d793d4bff6fc060a6b7` |
| `tmp/run-g4-zero-readiness.zsh` | 2969 | `13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a` |

Ownership/maintainability gate：PASS。

- public surface exact：`ZeroReadinessError`、`execute_zero_readiness`、
  `finalize_zero_readiness`、`main`；dependency injection仅为private
  `_RuntimeDependencies`。
- 复用`esphome.verified_light`、`ray120c.set_cct/get_cct/get_node_config`、
  `camera_remote` health/config owner、`hsi_source_evidence.validate_both_off`、
  `control.all_off`和retained provenance I/O owner；未创建平行device、serialization、persistence或source-isolation semantic owner。
- owner AST中没有直接导入`json/os/stat/subprocess/urllib/socket`，也没有直接
  `open/read_text/read_bytes/write_text/write_bytes`；wrapper只拥有四个0600 sibling scratch，前台运行并在EXIT/INT/TERM/HUP trap中调用repo-owned all-off，最终移除scratch。
- 三个巨型P7模块均未修改；没有god-object扩张或无关重构。
- CodeGraph sync：PASS，added `2` files / `100` nodes；query确认新owner到上述repo-owned底层owner的调用边。

## 4. Offline validation

- targeted：`8/8` PASS，`0.041s`，一次调用；未使用bounded correction。
- focused：`245/245` PASS，`59.094s`，一次调用。
- full suite：`872/872` PASS，`158.297s`，一次调用。
- `.venv/bin/python -m compileall -q src tests`：PASS。
- `zsh -n tmp/run-g4-zero-readiness.zsh`：PASS。
- `git diff --check`：PASS。
- runtime frozen identity preflight：curve owner与Ray settings owner读取成功；Ray URL/node/client exact为PLAN冻结值；未输出credential。
- real gate前HEAD/branch/machine contract未漂移，root `lexists=0`。

## 5. 唯一真实执行与chronology

命令仅执行一次：

```text
zsh tmp/run-g4-zero-readiness.zsh /Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-5d05cc14286a-20260803T191648Z
```

chronology：

1. root exclusive acquisition成功，写`frozen-inputs.json`。
2. main strip verified-zero成功：observed generation `2`。
3. main Ray zero在冻结localhost controller上连接拒绝；main primary失败。
4. camera health/config和source isolation未调用。
5. Python finally strip verified-zero成功：observed generation `3`；Ray zero连接拒绝。
6. child exit `20`。
7. shell trap运行；strip all-off成功，Ray all-off连接拒绝；shell cleanup exit `1`。
8. independent final strip verified-zero成功：baseline generation `4`、observed generation `5`；Ray zero连接拒绝，因此第二次source-isolation validation未发生。
9. wrapper result与terminal seal写入；wrapper最终exit `20`；四个sibling scratch均已移除。

redacted endpoint/identity：

- strip：`bedroom-rgbww-strip.local:6053`，expected/device name
  `bedroom-rgbww-strip`；MAC仅存在root证据中，本handoff不重复明文。
- Ray：`ws://127.0.0.1:33782`，node `40165-560387`，client `1`；连接拒绝，没有Ray state readback。
- camera：冻结为`http://ibobby-rpi-4.local:8088`和
  `remote_v2_capture_timing_v1`，但实际调用数为`0`。

最终call ledger：

```text
strip_verified_zero=3
strip_shell_zero=1
strip_nonzero=0
ray_set_zero=4
ray_get_cct=0
ray_get_node_config=0
ray_nonzero=0
camera_health_get=0
camera_config_get=0
camera_capture=0
camera_config_write=0
source_isolation_validation=0
release_consumption=0
formal_r6=0
td_c=0
```

`ray_set_zero=4`为四次受PLAN约束的intensity-zero尝试；全部在controller connection层失败，不是非零调用。没有capture、非零light、config write、release consumption、formal或TD-C调用。

## 6. Frozen root与artifact identity

root：

```text
path=/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-5d05cc14286a-20260803T191648Z
device=16777244
inode=2501768
mode=0700
inventory_count=14
```

exact inventory及identity：

| artifact | device | inode | mode | bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| `all-off-shell.exit-status.txt` | 16777244 | 2501779 | 0600 | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| `all-off-shell.json` | 16777244 | 2501777 | 0600 | 317 | `5a995f8c76898416e6096f4833475124428dad1451ef809e33d7c7f9c06ac0f2` |
| `all-off-shell.stderr.log` | 16777244 | 2501778 | 0600 | 54 | `dd5bb9263c3887df927111beb4855bcc6e460ec7856ff0f8ad4815d5787ad994` |
| `camera-readiness.json` | 16777244 | 2501772 | 0600 | 145 | `3a77b2dccd3a7b09b58e96de95c69e195527038647e7a39200fde66a31052397` |
| `frozen-inputs.json` | 16777244 | 2501769 | 0600 | 879 | `55db6fa3f73352491bb65dc1c3d707cc152960bdcd25f776eaafcbb1a688d99e` |
| `independent-final-zero.json` | 16777244 | 2501781 | 0600 | 1204 | `fff678e273816c3ac56d250e5f91b1a011965ab991342ef32c6af4475f5b58ef` |
| `python-finally-zero.json` | 16777244 | 2501774 | 0600 | 1241 | `ab90337ffab3bc9fcb3213f7ed1e815452541987b07fd844736d379061656e9f` |
| `ray-readiness.json` | 16777244 | 2501771 | 0600 | 145 | `c72f7ad866e99bbecfe7bbeb21e4594b4e6a04621295e0f45a8a7f56cf9e222a` |
| `runner.log` | 16777244 | 2501782 | 0600 | 77 | `2c5bd59640e5597c8f86cfd4a367d1633346ff1c793c46b490772a2cf431a5dd` |
| `source-isolation.json` | 16777244 | 2501773 | 0600 | 145 | `fbfbe0c67547ba08d2649586542a264a8332bb6e4818450f16e21848138a9107` |
| `strip-readiness.json` | 16777244 | 2501770 | 0600 | 666 | `335d8732bbb01b3a5ddc1a3339b1aae17eb0452c63f133b44444d8015c91b763` |
| `terminal-seal.json` | 16777244 | 2501785 | 0600 | 2937 | `cc11b85ec69c94a44b6a0dcc4b46e001387938d1fc6765b284c56523b09be4a6` |
| `wrapper-result.json` | 16777244 | 2501784 | 0600 | 584 | `c735958932cfa208ea3f229768ab314e4abd15f80170f029932e0ba2815cbf71` |
| `wrapper.log` | 16777244 | 2501783 | 0600 | 120 | `26f151a4b172b3c68c62b23e174d504da1729d18926126ee78061142978c4aef` |

terminal seal引用此前13项artifact且`terminal_self_reference=false`。全部JSON由repo-owned canonical decoder重读成功；root mode为0700，artifact mode均为0600，inventory exact且没有临时文件。

## 7. Exit、zero与残留状态

- child exit：`20`
- shell cleanup exit：`1`
- wrapper status：`child_failed`
- wrapper exit：`20`
- terminal status：`sealed_fail_waiting_planner_review`
- retry：`0`
- alternate root：`0`
- strip final zero：**已独立证明**，generation `5`，五通道均为零。
- Ray final zero：**未能证明**；所有zero attempt均在localhost controller连接层被拒绝。不得把“未证明”解释为非零，也不得宣称硬件ready。
- owned child/wrapper/all-off进程：`0`；只读进程扫描只看见扫描命令自身。
- sibling scratch：`0`。
- automation/Terminal/background task：未创建。

## 8. Planner decision request

请Planner按当前PLAN验收并先归档PLAN/ER。精确失败边界是：冻结Ray controller endpoint
`ws://127.0.0.1:33782`在唯一真实包的main、Python finally、shell cleanup与independent-final-zero均拒绝连接，导致Ray zero/readiness与combined source-isolation不可证明；camera stage未到达。

Executer没有权限重启/替换controller、重跑同一root、创建alternate root或释放G4-04。后续是fail-stop、Human环境恢复后新授权包，还是其他工程处置，由Planner审查并交Orchestrator决定；本handoff不生成corrective task ID。
