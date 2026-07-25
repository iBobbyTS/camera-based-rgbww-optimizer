# P7-TD-B-F0B-R1-C3-E2-R1 Planner 失败验收归档

**归档时间：** `2026-07-25T09:56:15-0600`

**验收对象：** C1 通过后唯一一次 fresh bounded E2 retry。

**审查基线：** HEAD `fa6c95dbf79f4c0828e8633560d2828e3646204b`；被审 active PLAN SHA-256
`9067bfbad39c7e3218b1ca1f832e9ac0a6a6f8f702cffa3dee90a321d9142a90`；exact lineage release SHA-256
`1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529`。

**审查深度：** High execution/evidence boundary。独立读取 package source、source manifest、self-check、pre-device gate、
real child/wrapper、raw cleanup/final-zero logs、finalizer 和 summary；逐个重算 JSON、source、canonical inventory、旧
artifacts 与 workspace。使用 CodeGraph 对比 repository ESPHome hostname/default owner 和既有 generation-bearing zero
contract。未访问网络、`.env`、remote、相机、Ray 或 ESPHome，未重跑 package。

## 审查结论

- 本次执行接受为合法 `bounded_e2_failure`，不接受为 E2 pass。no-device self-check 通过后唯一 real E2 已消费，Executor
  正确未 retry、capture、formal 或进入后续阶段。
- byte-exact C1 root/release gate 通过；failure 发生于首个 real strip zero 的 hostname resolution。错误为
  `ResolveTimeoutAPIError: Timeout while resolving IP address for ['bedroom-rgbww-strip.local']`。
- 同一 resolution timeout 出现在 primary strip zero、Python cleanup strip owner、child final zero、shell cleanup strip
  owner 和 independent final zero。当前 run 没有取得任何 strip generation-bearing snapshot，因此不能证明 strip 最终全零，
  E2 必须 hard-fail。
- shell cleanup retained stdout 独立证明 Ray `set_cct` 成功，CCT/GM/intensity 为 `5600/100/0`；Ray shell cleanup zero
  接受。不得把 Ray zero 外推为 strip zero。
- 同一 checkpoint 的前一 E2 cleanup 曾通过相同默认 hostname，并取得 exact name/MAC/state object 与 generation
  `4->5`。因此当前证据只证明本次 `.local` resolution 不可达；它不能区分暂时 mDNS 故障、fixture/Wi-Fi 离线或其他本地
  reachability 状态，也不能证明 production code regression。
- 不需要 Advisor。当前问题属于 local reachability 与 execution evidence ownership，不改变 TD-B 科学策略。

## Executor evidence

- run root：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1/e2-fa6c95d-20260725T152859Z`。
- execution summary：`e2-execution-summary.json`，bytes `47906`，SHA-256
  `63599437885c25c040f91001d7f2de5341d1389406c0d5e57febab72c39701a8`。
- execution source manifest：bytes `4346`，SHA-256
  `64ead10f96f0d846a841d8bd65841468d9ff4296af7938f0821f44fb08e3a8af`；`14/14` listed sources
  live bytes/hash 匹配，其中 package sources `9`、C1 sources `5`。
- no-device self-check：bytes `4951`，SHA-256
  `d045f17101a3bf4298488deb71d9a4e358b8f1ba6fc521f381a0d8c140234a89`；`6/6 pass`，real calls `0`。
- pre-device audit：bytes `560`，SHA-256
  `be639501272d214bf979331748c75034219983e08749cedf3233df8856efd3b7`；source/release/workspace/process gates pass。
- root/release gate：bytes `2848`，SHA-256
  `63eac30211d5b208cf64fbfa120017b99f703411f0e4eaec875320eda82944a0`。
- child result：bytes `6431`，SHA-256
  `9535e0279e4c3b835d9820c45534d985d9e331ced98ddac98f9717cdac0807ef`。
- wrapper process：bytes `3887`，SHA-256
  `cc6e9360e9f430e637dce92b09276186c28cc74fdd3d62fc406207c3b400a2ec`；wrapper exit `1`，cleanup/final-zero
  each invoked once。
- shell cleanup raw stdout：bytes `645`，SHA-256
  `a76aabff5799945d10f60ea5c4269a8b26374f72631eace992688415d1ee9dc0`。
- independent final zero：bytes `290`，SHA-256
  `eb8a6c224feb7b746e8ff46902df74f8582a018124f4353c30d8fafa093b964e`。

## 独立验证质量

- correction root 的 JSON `59/59` strict parse，均以真实 newline 结尾；source manifest `14/14` live bytes/hash 匹配。
- C1、旧 E2 和 release before/after manifests byte-identical；HEAD exact，staged 与
  `src/tests/docs/.agents/skills/tmp` diff 为空，`git diff --check` 通过。
- CR3/NPY、camera capture、Ray/strip nonzero、formal、public analyzer、firmware/deployment/destructive change 均为 `0`；
  无残留 owned wrapper/child process。
- summary 的 canonical inventory 有 `139/140` live bytes/hash 匹配。唯一 mismatch 为
  `logs/finalizer.stdout.log`：summary 在 finalizer 输出前记录 empty bytes/hash，finalizer 写完 summary 后又打印
  `bounded_e2_failure\n`，live bytes `19`、SHA-256
  `37c07449f3ab252ae78e920ee0eaa80d1115615d23290b7dd2d71ab59cdc0d93`。该漂移不改变 failure 结论，但不满足
  terminal evidence seal。

## Planner findings

### REV-E2R1-HOST-001 — Open / Reachability-dependent

`bedroom-rgbww-strip.local` 在本次所有 ESPHome attempts 中 resolution timeout。不得将 hostname 换成未冻结 IP、跳过
generation-bearing owner，或仅凭历史 zero 宣告当前安全。离线 evidence 纠偏通过后，先运行独立、零输出、一次性的
hostname/ESPHome reachability gate；若仍失败，再由 Human 检查 fixture power、Wi-Fi 与本机 local-network/mDNS 环境。
这不是 firmware 或危险设备操作，不需要 Human authorization。

### REV-E2R1-PROG-002 — Must Fix / Agent-Fixable

real child 只在 remote、Ray 和 strip 全部成功后一次性写 `primary`。strip DNS failure 导致已完成的 remote health/config、
capability、Ray node/CCT detail 全部丢失。每个 stage 必须在下一 owner 前原子持久化 attempt 与 redacted result；后续失败
不得擦除既有 evidence。cleanup/final-zero 的 strip 和 Ray owners 也必须 failure-isolated，strip failure 不得阻止 Ray
attempt/result 落盘。

### REV-E2R1-ATTEMPT-003 — Must Fix / Agent-Fixable

`RealOwners.strip_zero()` 只在 `verified_light()` 成功返回后增加 `esphome_calls`，remote/Ray counters 也在多个调用全部成功后
才增加。本次至少五个 ESPHome attempts 最终被报告为 `esphome_calls=0`。后续必须使用 attempt-before-call ledger，并从
artifact 重建每个 owner/stage 的 `attempted/succeeded/failed`；禁止用“成功返回次数”冒充 call attempts，final summary
不得只保留 forbidden counters。

### REV-E2R1-SEAL-004 — Must Fix / Agent-Fixable

finalizer 在 inventory 自己仍打开的 stdout 后才打印 status，造成 summary 内 canonical hash 立即陈旧。终态 sealer 必须
只 inventory 已关闭的 producer artifacts；自身 stdout/stderr 必须是明确 noncanonical 且不得承载 evidence，或保持静默。
summary 写入后不得再修改任何 listed artifact；独立 metadata/audit 必须重算 `N/N` path/bytes/hash 并检出模拟 post-seal
mutation。

## 决定、残余风险与精确下一分支

- E2-R1：`accepted_as_valid_hostname_reachability_hard_failure_not_e2_pass`。
- 唯一 fresh E2 已消费；当前不授权 retry、hostname probe、device access 或 formal。
- current lineage release、C1、旧 E2、production checkpoint 均未漂移；不要求新 setup 或 release。
- 下一分支：`P7-TD-B-F0B-R1-C3-E2-R1-C2_OFFLINE_PROGRESSIVE_EVIDENCE_CORRECTION`。
- C2 只离线修复 progressive stage evidence、attempt accounting、failure-isolated zero owners 与 terminal seal，并通过
  fake failure matrix；network、`.env`、设备、real cleanup、E2 retry、production edits、stage 与 commit 均为 `0`。
- C2 被 Planner 接受后，下一步是单独的 hostname/ESPHome zero-only reachability gate，不是直接重跑完整 E2。该 gate
  通过后仍需 Planner 决定是否有新的 E2 authorization。
- Ray TD-B formal、strip、TD-C、sentinel、remaining、boundary、holdout、Gate-6 与 P8 继续锁定。
