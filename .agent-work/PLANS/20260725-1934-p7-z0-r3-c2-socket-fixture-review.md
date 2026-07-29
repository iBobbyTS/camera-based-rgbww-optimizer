# REF-P7-01 / Z0-R3-C2 AF_UNIX fixture 首失败 Planner 验收归档

**验收时间：** `2026-07-25T19:34:22-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`fd5b6dc013e17cbe7d01813ad9b02d006ac631a169ed7dfab44ddc4811f43a29`

**Planner 决定：** `rejected_fixture_producer_failure; minimal_offline_c3_required`

**精确下一分支：** `P7-TD-B-Z0-R3-C3_OFFLINE_SHORT_SOCKET_AND_PROGRESSIVE_ROWS`

## 1. 被审范围与停止点

Executor在唯一fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r3-c2-offline/20260726T012448Z/`

建立package并运行driver一次。freeze、source delta、compile without bytecode与`zsh -n`通过；adapter/wrapper与C1 byte-exact。driver在live runtime gate前执行editable adversarial matrix，创建到第29个case `pth-socket` 时，将完整absolute fixture pathname传给macOS `AF_UNIX.bind()`，以 `OSError: AF_UNIX path too long` 首失败并停止。

socket constructor曾创建，但bind未成功；case目录中没有socket filesystem entry，validator未取得socket lstat evidence。这不是editable validator acceptance错误、runtime失败、network/device调用或dependency缺失。live availability probe、runtime propagation、copy、terminal、accounting、historical replay、lifecycle与seal均未启动。

## 2. Canonical evidence

| evidence | SHA-256 |
| --- | --- |
| `first-failure.json` | `e071f45ebb2a5462c62fa3b60ba33dd90c7c636918ae4dc3d95f5537aa521e16` |
| `post-failure-audit.json` | `26e812eafe8af7c7fb85e58023f92727dedf09fabbf44bdde0612ea4b69c634a` |
| `zero-budget-audit.json` | `569be3c8e2da2e701530dc82b952c1e987dfc51a0d2f1603f88ab64524173faa` |
| `validation-summary.json` | `9cc8cae5e1694e615a840b3b356476d1a6ade9e99e134f156d48be89f385b2ce` |
| `source-manifest.json` | `36d17f9c45ae8ca3984dea850c0dcc7e41c89f3de30f94263eb62ae8e6a6abc4` |
| `source/controller.py` | `446a480f4d4fbbff17f0be3620887be721cb725516989bd7a834800eaae3226d` |
| `source/real_adapter.py` | `2c37162dd94805ce8c48035faf9b0a54e6243d4a82edd3218c8ca018986492d3` |
| `source/run_wrapper.zsh` | `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6` |

## 3. Planner 独立重放

1. 上述8个files的bytes/SHA与structured JSON全部exact。failure boundary为`editable_fixture_matrix_pth_socket_path_construction`，package/driver/rerun为`1/1/0`。
2. case 29只包含ordinary parent directories；expected `.pth` socket path absent。matrix summary `editable-owner-matrix.json` absent，和post-failure `editable_matrix_summary_written=false`一致。
3. source在case分支直接执行 `held.bind(str(pth))`，其中`pth`是深层absolute path；异常发生在validator之前。AF_UNIX fixture只用于本地filesystem type负例，constructor不等于network call，connect/listen/send均为0。
4. 29个case directories虽已创建，但rows只保存在进程内存，异常导致前28个case没有独立immutable rows；因此不能报告任何accepted matrix pass count。
5. C1 named `9/9`、old Z0-R3 named `25/25`保持；live owner reads、runtime probe、production import、secret、network/device及后续matrix全部为0；residual process为0。
6. HEAD exact `0387bcfa53e52ee7f99d5308886e2b7873fe49f5`。Planner未执行source/matrix、未创建socket、未联网/安装/访问device或修改production/Git。

## 4. Finding 与下一分支

### `REV-Z0-R3-C2-SOCKET-FIXTURE-010` — Open

fixture producer必须在case parent内以短relative pathname bind AF_UNIX socket，可用保存cwd dir-fd、`chdir(parent)`、`bind(short_name)`、`fchdir`恢复的单进程owner；随后对最终absolute entry执行no-follow `lstat`并证明`S_ISSOCK`，validator完成后close并unlink exact fresh fixture。不得connect/listen或把短路径逻辑用于live owner。

### `REV-Z0-R3-C2-MATRIX-PROGRESS-011` — Open

editable matrix必须每case在执行前写immutable attempt row，完成或异常后写immutable terminal row；unexpected producer exception也须先落失败row和当前terminal aggregate再传播到package stop。最终summary由exact expected case set逐项读取/重算，不得依赖内存rows或把missing case算pass。

`REV-Z0-R3-RUNTIME-007`、`REV-Z0-R3-TERMINAL-FIXTURE-008`、`REV-Z0-R3-SECRET-ACCOUNTING-009`仍Open且本轮未消费。下一C3只可修上述两个机械owner，editable validator语义、adapter、wrapper及其他matrix不变；修复后fresh运行一次完整C2序列。

无需Human或Advisor；这是external test-fixture portability与evidence durability问题。

## 5. Orchestrator reference 建议

Planner不修改 `.agent-work/FULL_PLAN_REFERENCE.md`。建议把当前子状态改为 `P7-TD-B-Z0-R3-C3_OFFLINE_SHORT_SOCKET_AND_PROGRESSIVE_ROWS`，记录两个新REV并保持real Z0/E2/formal锁定。
