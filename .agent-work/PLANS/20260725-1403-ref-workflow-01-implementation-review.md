# REF-WORKFLOW-01 / WORKFLOW-LOCAL-LAB-CONTEXT-R1 Planner验收归档

**验收时间：** `2026-07-25T14:03:03-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`da05e560d00024a4cd7205c014a76fd7b11fb8b2f0569cac04b522fa5ea9e5c1`

**Planner决定：** `accepted_implementation_with_frozen_head_baseline_exception; commit_pending`

**精确下一分支：** `REF-WORKFLOW-01_EXACT_REVIEWED_DIFF_COMMIT_FINALIZATION`

## 被审范围与结果

被审PLAN授权一个严格offline code/docs/skill package：移除Ray120c production-looking credential default，建立三个control CLI共用的
user-owned local-lab context owner，集中本地连接边界，并把P7历史细节从project skill迁到按需engineering note。Executor完成13个
授权paths的实现与验证，但因full suite `557/559`保留两个TD-B lineage errors，依原PLAN full-green gate未stage或commit并返回Planner。

Evidence root：

`/Volumes/4T/temp/rgbww-optimizer/workflow-local-lab-context-r1/20260725T195112Z`

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `validation-summary.json` | 1590 | `5f273d4ead876e45493042a24f63881a16423e9f49f3ed16640f0bf2c10bee53` |
| `logs/focused-r2.stderr.log` | 150 | `b930c1c153c7d9176e7983326928b6932065cc8f55fd66c533cea089edeb42cf` |
| `logs/full-r2.stderr.log` | 6803 | `9c71b2f71ab338667eb7dda1161e988cff1ea11f25afaecffb7d0c19fc24f4c0` |
| `logs/full-r2.stdout.log` | 4145 | `08182efa6348fad541bcd56dface23f15192da89001b2e3803f587f31b5aa278` |
| `logs/static-audit.json` | 279 | `a461484112b68efa1c95c178e2026c5535b2a966e400b971f58c6f82a9bd6388` |
| `logs/leak-audit.json` | 137 | `d8c63b627112f5ff1b8a77683716de31dcc458c6f1e013caf07d3032c6107a2f` |
| `logs/codegraph-sync.stdout.log` | 2648 | `1aed90cec4e39f362899eb84dd4bb3fc7e02d924d24eeb9976617245e5f9beb3` |
| `.agent-work/EXECUTION_RESULT.md` at review | 167219 | `6abcb71d9eedbb78a5b3b6f42fe65fdcb5a5988cd67fbb0122105986a3f042f9` |

## Planner独立验收

1. `validation-summary.json` direct hash、contract、expected HEAD与交接一致；focused rerun log为`51/51`、exit `0`。compileall、三个
   module help、CodeGraph sync、static/leak audit和`git diff --check`的recorded exits均为`0`。
2. current skill为`4678` bytes（baseline `41300`），保留Scope、roles/ownership、core safety/runtime、routine entry points和
   progressive routing；P7 detail迁到`docs/engineering/p7-td-b-contract-history.md`且明确paused/not authorization。README与skill均链接
   central `docs/local-lab-connection-boundary.md`。
3. live AST/content replay确认current authorized source/tests/docs/skill/AGENTS中旧exact credential count `0`，
   `DEFAULT_OPENAPI_SECRET` assignment count `0`，`generate_token` positional defaults `0`。`OpenAPISettings.secret`required、
   `repr=False`；single `_decode_secret`执行strict base64/exact 32-byte validation；CLI无secret option。
4. 三个live help artifacts均exit `0`，包含同一user-owned local photography/lighting calibration context和各自RGBWW/camera/Ray action；
   Ray help不读取credential。CodeGraph确认`cli_description`单一owner被三个CLI调用。
5. tests仅从`bytes(range(32))`runtime编码fake key；focused覆盖missing/empty/malformed/wrong-length、required token argument、repr
   redaction、help和docs/skill structure。leak audit的current/evidence hits均为空，未记录实际environment value。
6. actual authorized implementation为13 paths，均在PLAN allowlist；未修改protocol、payload、timeout、device cleanup或scientific
   runner。hostname/network/device/camera/Ray/strip/nonzero/Z0/E2/capture/formal/firmware/deployment/actual credential reads均为`0`。
7. HEAD保持`8cd04d847d42ff5c7bcf7501f46be97cbbef429d`，index为空；未stage、commit、push。Planner本次只读source/evidence，未执行
   tests、implementation、network/device或Git mutation。

## Full-suite两个errors的独立归因

失败tests为：

1. `test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`；
2. `test_lineage_release_rejects_candidate_and_resolved_plan_tampering`。

两者都先用`git rev-parse HEAD`取得committed `8cd04d8`，再调用`write_td_b_setup_lineage_release()`。该owner固定从TD-B setup
checkpoint `9c804ab`到传入committed HEAD计算changed paths，并在任何本workflow逻辑或test断言前因prohibited lineage抛
`PermissionError`。

Planner只读`git diff --name-only 9c804ab..8cd04d8`确认committed range已包含`AGENTS.md`修改和
`.agent-work/FULL_PLAN_REFERENCE.md`新增；TD-B lineage allowlist不含这两项。current workflow implementation仍是unstaged working-tree
diff，不能影响上述commit-to-commit calculation。stack trace也只经过lineage writer/candidate gate，不经过Ray、shared context、help或
本包docs/tests。

因此这两个errors是frozen HEAD上既有TD-B lineage allowlist/checkpoint coupling，不是本实现regression。它们应在Human已暂停的P7
路径中作为独立baseline test debt处理；不应要求本最高优先级workflow package修改P7 production/tests，也不阻止接受本实现。

## 决定、残余风险与下一分支

接受13-path implementation与全部本scope validation；把full-suite `557/559`记录为causally independent baseline exception。由于原PLAN
明确在full-green后才commit，Executor正确保留index/commit为0；当前任务仍需一个精确commit-only finalization才能完成。

下一active PLAN只能：冻结本归档验收的13个path hashes，验证working tree没有drift、index为空、static/leak/diff evidence仍一致，仅
stage这13项并创建一个focused commit；不得改代码/docs、重跑full suite、修P7 lineage、stage `.agent-work`/Orchestrator/user work或
访问network/device。P7 baseline errors与Z0 findings保持paused，不由该commit解锁。
