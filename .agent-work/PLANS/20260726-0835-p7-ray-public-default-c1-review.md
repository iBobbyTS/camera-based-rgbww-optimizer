# P7-TD-B-RAY-PUBLIC-DEFAULT-C1 Planner review

**Review 时间：** 2026-07-26T08:35:17-0600

**Reference task：** `REF-P7-04`

**Reviewed contract：** `P7-TD-B-RAY-PUBLIC-DEFAULT-C1`

**Decision：** `implementation_accepted_lineage_remains_fail_closed`

## 1. Reviewed scope and method

Planner 独立读取并交叉核对：

- reviewed PLAN SHA-256
  `ec602ea4f139e0c960178ec8b3ad6551bb600645d519cb537f9f68e81d593ce6`；
- `.agent-work/EXECUTION_RESULT.md` 第 101 节；
- commit `e7ccdda672b7d5902d81627ff98268160ff141cd` 及其 parent
  `a87b09fc4a701a76e5214d6ff6d3a4e3de090521`；
- exact 7-file commit diff、文件 bytes/hash、production owner、测试和文档合同；
- 当前 Orchestrator-owned `FULL_PLAN_REFERENCE.md`，review 时 SHA-256
  `e4429d7441b25060c95571eaea96a5cfe81eec12a4253b1c9f16e089c19d2407`；
- 两个 frozen TD-B lineage test 的独立重放。

Planner 未访问设备、网络、hostname、`.env`、launchd 或 Terminal，未运行 live、cleanup、capture、
analyzer、setup 或 formal，也未修改 `FULL_PLAN_REFERENCE.md`。

## 2. Implementation acceptance

实现符合 PLAN 的冻结语义：

- exact public default 为 `9veqiL0G0EUOviwzL1prPc0iGIGUJtbzSaPYQfgfyxM=`；它只按 Human 决定与
  repo history 被分类为 public shared protocol default，不伪称由外部 vendor 文档、协议规范或安全审计验证；
- 环境键缺失使用 default；合法 explicit override 精确优先；显式空值、非 strict base64、解码后非 32 bytes
  均由同一 validator fail closed，绝不 fallback；
- `OpenAPISettings.secret` 为 `repr=False`，CLI 不接受 `--secret`，private override 不进入 argv、repr、
  stdout/stderr、artifact、logs 或 docs；
- `generate_token`、CLI settings 与 `all_off` 复用同一 resolution/validation owner；既有 command payload、
  timeout、映射和 cleanup/off 语义未被扩大；
- `docs/local-lab-connection-boundary.md`、`docs/README.md` 与项目 skill 持久化了上述 Human-classified
  public-default/optional-override/nondisclosure 边界，并明确不是 external-vendor validation claim。

Commit subject 为 `fix(ray120c): restore public protocol default`；binary diff SHA-256
`cb9e1c5e485fdfc61b0b00928202d94649093e2344eaed22968f7bae12a85f28`。范围精确为：

```text
.agents/skills/camera-based-rgbww-optimizer/SKILL.md
docs/README.md
docs/local-lab-connection-boundary.md
src/camera_based_rgbww_optimizer/control/ray120c.py
tests/test_all_off.py
tests/test_project_context_docs.py
tests/test_ray120c.py
```

文件 SHA-256 与 Executor 第 101 节全部一致。`.agent-work`、CodeGraph、GUIDE、wrapper 和其他用户/agent
改动均未进入 commit。

## 3. Validation quality

接受的实现证据：focused `26/26`、cleanup regression `99/99`、postcommit focused `26/26`、compileall、
18 个 wrapper syntax、negative scan、`git diff --check` 与 CodeGraph sync 均通过。

TD-B 为 `71/73`，full suite 为 `567/569`；两者都**不是完整绿色**。唯一两个 errors 精确为：

1. `test_current_head_lineage_accepts_exact_human_policy_freeze`
2. `test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift`

Planner 独立重放这两个用例，得到 `Ran 2 tests`、`FAILED (errors=2)`、无 test failure；两项均为：

```text
ValueError: TD-B workflow path hash or diff differs: docs/local-lab-connection-boundary.md
```

这不是 public-default 实现缺陷，而是旧 frozen workflow manifest 仍绑定该 PLAN-authorized 文档的旧
blob/diff，按设计拒绝新 HEAD。Planner 接受实现，但不接受旧 lineage/release 对新 checkpoint 的有效性，
也不会篡改旧 artifact 或把 `71/73`、`567/569` 报成绿色。

## 4. Findings and residual risks

- `REV-P7-PUBLIC-DEFAULT-LINEAGE-001` — **open / fail closed**：新 HEAD 的 exact workflow provenance 尚未
  建立；旧 setup lineage release、checkpoint 和 formal authorization 不得继承。
- 没有发现新的 production、credential disclosure、CLI、cleanup、docs/skill 或 commit-scope finding。
- Executor 声明的 device/network/hostname/`.env`/launchd/Terminal/live/formal 调用均为 `0`，并与代码测试
  类型、artifact 叙述和 commit scope 一致；本 review 也保持这些计数为 `0`。

## 5. Latest Human pause

冻结最新 Human 决定：暂时不得启动灯、相机或任何设备测试，直到 Human 明确恢复。只允许离线计算、代码、
测试、文档、证据重放与 lineage 工作。该决定覆盖较早的 probe、zero-only、Ray、strip、camera、capture、
cleanup、formal 或其他设备放行；public-default commit、未来 lineage correction/release 或旧 readiness 均不能
被解释为恢复设备授权。

Human pause 的当前 Orchestrator source 是 `.agent-work/FULL_PLAN_REFERENCE.md` 第 2.1 节；review 时该文件
SHA-256 为 `e4429d7441b25060c95571eaea96a5cfe81eec12a4253b1c9f16e089c19d2407`。

## 6. Decision and exact next branch

`P7-TD-B-RAY-PUBLIC-DEFAULT-C1` 的代码、测试、文档、skill 与 focused commit **接受**。下一唯一分支是
`P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-C1` 纯离线 checkpoint/provenance correction：建立新 HEAD 的 exact、
versioned successor lineage manifest/owner，保留旧 manifest/release 不变并通过 adversarial tests 证明不能宽化。

该下一包不得 qualification、创建 release、消费旧 release、probe、zero-only、Ray、strip、camera、capture、
actual `all_off`、Terminal 或 formal。完成后停 Planner，再由 Planner 判断是否发布独立 offline qualification。

## 7. Suggested FULL status update

建议 Orchestrator 在验收本 archive 后：

- 将 `P7-TD-B-RAY-PUBLIC-DEFAULT-C1` 标为 implementation complete/accepted；
- 将 `REF-P7-04` 当前 action 切到 `P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-C1`，状态
  `ACTIVE_OFFLINE_LINEAGE_CORRECTION`；
- 记录 `REV-P7-PUBLIC-DEFAULT-LINEAGE-001` 为唯一开放 finding；
- 将所有 device/live/formal 子路由继续标为 `PAUSED_BY_HUMAN_PRIORITY`，直到显式 Human restore；
- 不把旧 lineage release 或旧 formal authorization 标为适用于 `e7ccdda...`。

维护性判断：实现继续由既有 Ray settings/token owner 单点管理，下一步只需 exact versioned lineage
successor 与负例保护；无需配置服务或架构重构。
