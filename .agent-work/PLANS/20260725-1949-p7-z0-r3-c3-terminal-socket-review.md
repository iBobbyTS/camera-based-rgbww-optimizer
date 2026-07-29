# REF-P7-01 / Z0-R3-C3 terminal-negative socket 首失败 Planner 验收归档

**验收时间：** `2026-07-25T19:49:34-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`57606b34337827d5f048ffd1c04fb24ba82d57a43d3ffefbe2eded23450798d0`

**Planner 决定：** `accepted_c3_authorized_subscope; rejected_overall_at_inherited_terminal_socket_producer; minimal_c4_required`

**精确下一分支：** `P7-TD-B-Z0-R3-C4_OFFLINE_TERMINAL_SOCKET_AND_PROGRESSIVE_ROWS`

## 1. 被审范围与决定

Executor在唯一fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r3-c3-offline/20260726T013852Z/`

运行driver一次。C3授权的editable case29 short-relative socket producer、37-case progressive rows和row durability均通过；live runtime/editable owner及copy regression也通过。随后首次消费继承的terminal planned-negative matrix时，其独立`socket-substitution` producer仍对长absolute path执行AF_UNIX bind，抛 `OSError: AF_UNIX path too long`。socket entry未创建，matrix summary未写；accounting、historical、offline lifecycle与terminal seal均未启动。整包不能接受为complete，但C3具名已通过sub-evidence可冻结，不要求重跑。

## 2. Accepted C3 sub-evidence

| evidence | result | SHA-256 |
| --- | --- | --- |
| `source-manifest.json` | allowed C3 delta exact | `96cd674f19f60451846857adf0b13c87080366ddef5f08427afc6d85e48b83ce` |
| `row-durability-matrix.json` | `3/3` | `924f0094124999e3a1be6f151bf8c0bb34356299017470fdb71d50b1765c223b` |
| `editable-owner-matrix.json` | `37/37`, 37 attempts + 37 results, disk recompute | `857201cca07c2b9fb1779b06dee852d00ae27080aa0130ce38fb3cff04c205f3` |
| `runtime-availability.json` | exact venv/aio/owners/audit-hook zero | `473d6cbc3ce9fccf7b0d1e442bd27477f415bb07f207173c188c62d0406cb652` |
| `runtime-freeze.json` | Python 3.13.2 chain exact | `a001d4d1e5ca4d1a3e1a1bd3159f11e09899e0c904a3c77cdd6b9a7169b76fba` |
| `copy-regression.json` | `7/7` | `0aad223c0e3546a9705fb61765a4b69fa85e16062481b0ce90c8f9acfabb455e` |
| `planned-negative-registration.json` | exact two symlinks, follow 0 | `0790c571ba5f4bb104504129909e756bf54fdf3952f4e8caddcdd8ee146fd29a` |

case29 attempt SHA-256 `805bd50c6c8eb8dd84cb94259d7192bbe1c9798e2d3f9688f7513e54fec5c229`；result SHA-256 `c9417152ae030987a6e6c012b256f1c13f23819cc200924da060d408851f69fb`。它证明relative basename bytes `51`、bind/type proof/validator rejection/cleanup各exact一次，cwd恢复且final absent，connect/listen/accept/send/recv/DNS/network均为0。

## 3. Failure evidence

| evidence | SHA-256 |
| --- | --- |
| `first-failure.json` | `539eaa3f6f470426657b2872e04874fe1bc892009fcd968638400ca3837d071b` |
| `post-failure-audit.json` | `4f17234d841c18cf71f218b9b710a65e9c618b57f3cb2b355ed1f006ef0a37d3` |
| `zero-budget-audit.json` | `409654f8bfb0d04eda0cef02139dab8fdf1221933dc4ca4ed37771b38e3ec7c2` |
| `validation-summary.json` | `d247bb06971cf890e84a2de900f364ce7e65bc404b962c1be58ee82a2a97eb4e` |

## 4. Planner 独立重放

1. 上述11个artifact hashes与strict JSON全部exact；editable full summary、row durability、runtime/copy/registration statuses与Executor报告一致。
2. editable rows exact为37 attempt +37 result；case29 socket entry已清理、final absent。C3 source controller SHA-256 `8da8d84b4b99ffc468092e07bd703a5a777ed23ceeda16d605b239251a3db396`；adapter/wrapper保持C2 byte-exact。
3. terminal function直接执行 `held_socket.bind(str(source_path))`，source_path为深层absolute path；异常在`c1_classify_tree()`前。terminal summary absent，failure substitution root中socket filesystem entry absent。
4. terminal matrix planned case set为15：canonical two、6个synthetic policy cases、4个type substitution cases与4个allowlist/follow leakage cases。rows仍只在内存，首失败导致已完成terminal cases没有独立rows。
5. C3 package/driver/rerun=`1/1/0`；terminal socket constructor/absolute bind success/entry=`1/0/0`。device/network/DNS/secret/install/real Z0/E2/formal/Git均为0，owned residual为0。
6. HEAD exact `0387bcfa53e52ee7f99d5308886e2b7873fe49f5`。Planner未运行source/matrix、未创建socket、未联网/安装/访问device或修改production/Git。

## 5. Finding 与下一分支

`REV-Z0-R3-C2-SOCKET-FIXTURE-010`与`REV-Z0-R3-C2-MATRIX-PROGRESS-011`在editable owner范围内Closed。新finding：

### `REV-Z0-R3-C3-TERMINAL-SOCKET-012` — Open

terminal `socket-substitution` producer必须复用已证明的parent-cwd + short relative basename模式，在恢复cwd后对exact absolute entry no-follow `lstat`并证明`S_ISSOCK`；冻结validator仍须fail closed；close后仅按exact device/inode/type unlink，最终absent，connect/listen/network为0。

### `REV-Z0-R3-C3-TERMINAL-PROGRESS-013` — Open

terminal 15 cases必须逐case写exclusive immutable attempt/result rows，producer/validator/cleanup异常也先写失败result与partial disk aggregate再停止；full/partial summary从disk exact case set重算，不得依赖内存rows。

下一C4只可修改terminal negative socket producer及terminal matrix row/aggregate owner。C3 editable semantics/validator/case set/rows、runtime owners、copy evidence、adapter与wrapper全部冻结。通过terminal matrix后才运行未消费的accounting/historical/lifecycle/seal。

无需Human或Advisor；这是external terminal negative fixture portability/evidence durability问题。

## 6. Orchestrator reference 建议

Planner不修改 `.agent-work/FULL_PLAN_REFERENCE.md`。建议把当前子状态改为 `P7-TD-B-Z0-R3-C4_OFFLINE_TERMINAL_SOCKET_AND_PROGRESSIVE_ROWS`，关闭两个editable REV、打开两个terminal REV并保持real Z0/E2/formal锁定。
