# REF-P7-01 / Z0-R3-C4 accounting oracle Planner 验收归档

**验收时间：** `2026-07-25T20:15:35-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`749a8369fc47b81da03ec1731e7396ed9091beb2f6b1f0de7354d30aeb5683a2`

**Planner 决定：** `accepted_terminal_subscope; rejected_overall_at_accounting_oracle_and_fail_stop; minimal_c5_required`

**精确下一分支：** `P7-TD-B-Z0-R3-C5_OFFLINE_ACCOUNTING_ORACLE_AND_MATRIX_FAIL_STOP`

## 1. 被审范围与决定

Executor在唯一fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r3-c4-offline/20260726T020549Z/`

运行driver一次。C4授权的terminal row durability `6/6`、15-case progressive matrix、short socket proof/classifier rejection/identity cleanup全部通过。随后首次完整消费冻结accounting matrix，得到`12/13`；唯一失败`load-not-called`的event counts完全正确，错误来自oracle把除`complete-success`外所有primary cases都要求outcome=failure。

driver还在accounting fail后继续运行historical与lifecycle，再统一检查status，违反首失败即时停止。historical `5/5`、lifecycle `17/17`结果自身有效但属于post-failure consumption，不能使C4通过，也不替代C5按正确顺序重新运行。terminal seal未启动。

## 2. Accepted C4 terminal/runtime/source evidence

| evidence | result | SHA-256 |
| --- | --- | --- |
| `source-manifest.json` | C4 delta exact | `59fb80f72fd794125c8b53669eea054744b5ecdbc65a32261afdd5e9d4d83d7b` |
| `runtime-identity-replay.json` | frozen runtime identities exact | `7d1de3989e0dde57eac96ca3d505ff973afd190da2985b6658e1e4c7e73ae173` |
| `terminal-row-durability-matrix.json` | `6/6` | `0d8a78028fc29d2854d35eb685821464cb29572a11a2eff87e8c7a2d3053de9e` |
| `terminal-negative-matrix.json` | `15/15`, 15 attempts +15 results | `03ec35cca357484ff245ea26bf72759aba8e2f48a196b79b8b712fbbe8797592` |

terminal socket attempt SHA-256 `c88df090f3baad33e18e25b4b888674e38379d9ce8d51806be32205cb99e8b49`；result SHA-256 `4714257cbdb77aacbb1fa51f640a4cd813e25108e67a7bd4d5e090c8ee9c8412`。它证明relative `bind("src")`、absolute `S_ISSOCK`、classifier fail closed、cwd restore、exact device/inode/type cleanup与final absent，network operations为0。

## 3. Failure 与post-failure evidence

| evidence | SHA-256 |
| --- | --- |
| `accounting-matrix.json` | `3b7de081fb9c1beecdf12d2260aa949af7f85218e2ace9ce10ebc294da7fd9bf` |
| `historical-accounting-replay.json` | `2eb681d989f6bcea13dea57a87defa015680469a386e77cc68017a7a19738fce` |
| `offline-lifecycle-matrix.json` | `39fb48bb48f4f1fe6aa6eb3372f72dc82d063a0e5fee48a49fbc3bd3a4136a7e` |
| `first-failure.json` | `ce699aa29d655a1f3c0a5d1863bb95b2253d730ea46b09a05dfeecfd90addaf5` |
| `post-failure-audit.json` | `d2f766852c2b8150c4076b3a4f7cc7ee887532e9f2cc63dade1eb53bcd1dc44d` |
| `zero-budget-audit.json` | `06f9abb0d7fed0afc15d41616b5fba115d50f068b1a7bd1a571813c9d66bbb45` |
| `validation-summary.json` | `45191f84861985d0e6957e91900139f9722b84beefcd337beb63c1e055ad4104` |

## 4. Planner 独立重放

1. 上述10个artifacts与terminal 30 row files全部bytes/SHA、strict JSON exact；terminal summary确认为disk-recomputed `15/15`，无missing/extra/failed。
2. `load-not-called` events为adapter identity attempt/success、production import attempt/success；六项counts exact `(1,1,1,1,0,0)`，outcome=`success`、error=null、secret leak=false。fake verified function有意不调用loader并正常返回，故success正是expected behavior。
3. 冻结pass公式为 `((name == "complete-success") == (outcome == "success"))`，错误地将`load-not-called`要求为failure。正确oracle必须按每个primary case显式声明expected counts与expected outcome。
4. driver顺序确认为先构造accounting、historical、lifecycle，再统一检查；因此accounting failure没有阻止后两者执行。C5需在每matrix返回后立即检查，不允许先调用下一个owner。
5. historical post-failure结果为adapter/import/load `5/5,5/5,0/0`；lifecycle `17/17`且residual 0。C5应fresh重跑两者，不能仅引用post-failure结果作为最终pass。
6. device、network、hostname、secret、install、real Z0/E2/formal/Git均为0。HEAD exact；Planner未执行source/matrix或修改production/Git。

## 5. Finding 与下一分支

`REV-Z0-R3-C3-TERMINAL-SOCKET-012`与`REV-Z0-R3-C3-TERMINAL-PROGRESS-013` Closed。新findings：

### `REV-Z0-R3-C4-ACCOUNTING-ORACLE-014` — Open

primary accounting cases必须分别冻结expected outcome：`before-entry`、`adapter-read-failure`、`import-failure`、`load-failure`、`downstream-failure`为failure；`load-not-called`与`complete-success`为success。counts与outcome同时exact且无leak才pass；尤其load-not-called必须是`success + load 0/0`。

### `REV-Z0-R3-C4-MATRIX-FAIL-STOP-015` — Open

driver必须在accounting、historical、lifecycle每个matrix返回后立即检查。任一fail先封存该matrix/failure evidence并停止，后续matrix调用次数exact 0。需synthetic negative matrix证明accounting fail阻止historical/lifecycle，historical fail阻止lifecycle，以及all-pass保持exact顺序。

C5只可修改accounting expected-outcome oracle、driver matrix-boundary fail-stop及其测试/schema。C4 terminal/runtime/source owners、editable/copy/validator、adapter/wrapper全部冻结且不得重跑。C5按顺序运行accounting，再fresh historical、fresh lifecycle，最后seal。

无需Human或Advisor；这是external offline oracle与控制流问题。

## 6. Orchestrator reference 建议

Planner不修改 `.agent-work/FULL_PLAN_REFERENCE.md`。建议把当前子状态改为 `P7-TD-B-Z0-R3-C5_OFFLINE_ACCOUNTING_ORACLE_AND_MATRIX_FAIL_STOP`，关闭terminal REV、打开两个C4 REV并保持real Z0/E2/formal锁定。
