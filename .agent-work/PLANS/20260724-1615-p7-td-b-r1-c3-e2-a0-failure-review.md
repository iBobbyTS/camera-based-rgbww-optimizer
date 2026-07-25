# P7-TD-B-F0B-R1-C3-E2-A0 Planner 失败验收归档

**归档时间：** `2026-07-24T16:15:53-0600`

**验收对象：** 当前 `fa6c95d` lineage release 的一次 bounded E2 preflight。

**审查基线：** HEAD `fa6c95dbf79f4c0828e8633560d2828e3646204b`；活动 PLAN SHA-256
`34fd1079fad55346c60de95627f83a69fbc5da8d32603b896be7cd862c91512b`；`AGENTS.md` SHA-256
`38f0055689dd4da913c03b95e384294bdee1d59ed54e9c966764cf3ff8f1fd28`。

**审查深度：** Medium execution/evidence boundary。独立读取 E2 summary、child/wrapper source、主 failure JSON、artifact
repair、Python/shell cleanup、independent final zero、全部文件 hashes 与进程状态；使用 CodeGraph 对比 repository-owned
checkpoint/tree validation 与现有 cleanup/root ownership pattern。未访问 remote、相机或设备，也未重跑 E2。

## 审查结论

- 本次 E2 接受为合法的 `bounded_e2_failure`，不接受为 E2 pass。唯一授权 run 已被消费，Executor 正确未 retry、未进入
  formal。
- 主 preflight 在 workspace check 的第一个 Git 命令即失败；release、remote health/config、backend/camera、Ray
  preflight 与 strip preflight 均未到达。capture、CR3、NPY、formal、public analyzer、Ray nonzero 与 strip nonzero 均为 `0`。
- 失败后的允许 cleanup 确实访问 Ray/ESPHome 零状态 owner：Python cleanup、child final zero、shell cleanup 与独立 final
  zero 全部通过。strip exact identity 为 `bedroom-rgbww-strip` / `E0:8C:FE:63:C9:40`，generation
  `1->2->3->4->5`，五通道全零；Ray intensity `0`；无残留 E2 进程。
- 失败不是 Git 仓库、release 或设备问题。外置 child 错误使用 `Path(__file__).parents[4]` 推导 repository root；外置 run
  depth 与 repo identity 无关，`git rev-parse HEAD` 因此 exit `128`。
- 同一一次性 harness 还存在第二个独立缺陷：child 与 wrapper 的 JSON writer 使用字面量 `"\\n"`，生成不可 strict-parse
  的 JSON。离线 repair 仅把尾部 backslash-n 改为真实 newline，并保留原始 bytes/hash；Planner 从 repaired bytes 重构
  原始尾字节后，两份 SHA-256 均精确匹配 repair artifact。
- 当前 E2 缺少冻结、fake-tested 的稳定 harness owner。只修 magic parent index 或在旧 run 内改脚本重跑会重复同类风险。
- 不需要 Advisor。根因是执行/evidence ownership，不改变 release、shutter、58-feature、quality、schedule、budget 或科学
  策略。

## Executor 证据

- run：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-fa6c95d-undefined`。
- execution summary：`e2-execution-summary.json`，bytes `4733`，SHA-256
  `12e41cd773c9ea955b4251c300ebdfcaf4fbaceadb6162be6f8c456535b63414`。
- repaired main evidence：`e2-preflight.json`，bytes `3915`，SHA-256
  `33f51ac0b5040ac179bc8ebd9af19b83371a1158c04cd68f9af41a10f25fa404`。
- wrapper process：`wrapper-process.json`，bytes `315`，SHA-256
  `80a12a4255e7c0a02db42d153a40f97d1dd49ea00e2518123e17b0b3d7d4a90b`。
- artifact repair：`e2-artifact-repair.json`，bytes `1044`，SHA-256
  `365e500286671166c6ec9e7f0d9b711fbbb19cc2b806cdbef8d9c98ecf39fa97`。
- shell cleanup：`all-off-shell.json`，SHA-256
  `5a50282a5d1cb8ab3b6c6f043bc1ef94f1a9ce4fb6d175c360c84056d87c711d`；stderr empty hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。
- independent final zero：`independent-final-zero.json`，SHA-256
  `00d02b5e0e27abbb6bac5eada674ef94df918c01f0fce343061aeec01ac76c8c`；stderr empty。
- frozen one-off source hashes：`e2_preflight.py`
  `66e5c4e6d5b540fb3a45a5d489e0db4c48f710d49f3e2b97ac4e2ae8c6ad0871`；`e2-wrapper.zsh`
  `e4f0c060171dec868c4a12ac2badbea5cee04a3d908bb57b55b45fb41919abab`；`final_zero.py`
  `21ec888fb39a8795bdcfba27b9fbbc167f16a665c1289b9bf7c201ebe3c50f2e`。

## Planner findings

### REV-E2-ROOT-001 — Must Fix / Agent-Fixable

外置 child 以自身 path depth 推导 repository root，违反 repo identity ownership。纠偏必须从 PLAN 冻结的 explicit
canonical project-root 参数取得 root，并验证 `git rev-parse --show-toplevel`、HEAD、staged 与 production-scope diff；
外置 source/run path 不得参与 root 计算，也不得换成另一个 magic parent index、隐式 cwd 或未验证硬编码。

### REV-E2-JSON-002 — Must Fix / Agent-Fixable

child 与 wrapper evidence writer 写入字面量 backslash-n，导致核心 JSON 初始不可解析。纠偏必须使用 atomic strict JSON
writer 和真实 newline；success、child failure、wrong-root、signal、cleanup failure 的所有 JSON 均需首次落盘即可 strict
parse，禁止依赖 post-run repair。

### REV-E2-OWNER-003 — Must Fix / Agent-Fixable

当前 E2 harness 是未经过 fake/runtime regression 的一次性外置代码，root 与 serialization 两个缺陷均来自该 owner
缺失。为保持 `fa6c95d` release 不漂移，本轮不改 production paths；但必须在全新外置 offline correction root 中建立
单一冻结 harness、source hash manifest、外置深度回归与 fake-only roundtrip，并由下一次 E2 exact 复用。旧失败 run
保持 forensic-only，不得原地修改或执行。

## 决定、残余风险与精确下一分支

- E2 execution：`accepted_as_valid_pre_device_hard_failure_not_e2_pass`。
- cleanup/final-zero：接受；artifact repair：只接受为 forensic salvage，不接受为未来正常 writer 行为。
- current release：未被读取或修改，仍保持已接受状态；本次失败不要求新 setup 或新 lineage release。
- 下一分支：`P7-TD-B-F0B-R1-C3-E2-C1_OFFLINE_HARNESS_CORRECTION`。
- C1 仅离线创建/验证 frozen external harness；device、network、`.env`、real Ray/ESPHome、E2 retry、formal、production
  edits、stage 与 commit 均为 `0`。
- C1 被 Planner 接受后，Planner 才能另写一次 fresh E2 retry 计划。根据当前 `AGENTS.md`，该 bounded E2 retry 不需要
  额外 Human authorization，但不得自动执行或进入 formal。
- strip、TD-C、sentinel、remaining、boundary、holdout、Gate-6 与 P8 继续锁定。

