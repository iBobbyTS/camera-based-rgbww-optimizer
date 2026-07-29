# REF-P7-22 / Human EQ-R6 stage checkpoint

**计划状态：** `human_confirmation_required_no_execution`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-22`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-HUMAN-CHECKPOINT`

**Package kind：** `human_scientific_stage_checkpoint`

**Current checkpoint HEAD：** `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-HUMAN-CHECKPOINT","reference_task_id":"REF-P7-22","package_kind":"human_scientific_stage_checkpoint","checkpoint_head":"98de1a91c264d4b72c4a97fc499ae7d39a67dacc","single_current_action":"wait_for_explicit_human_eq_r6_stage_confirmation","human_confirmation_required":true,"human_confirmation_satisfied":false,"executer_dispatch_authorized":false,"device_access":"forbidden","network_access":"forbidden","env_access":"forbidden","camera_access":"forbidden","light_access":"forbidden","all_off_access":"forbidden","root_creation_authorized":false,"release_generation_authorized":false,"release_consumption_authorized":false,"eq_r6_authorized":false,"formal_r6_authorized":false,"strip_authorized":false,"td_c_authorized":false,"commit_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 向 Human 呈交下面的 exact `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6` stage边界并等待
明确确认或拒绝。

**Planner stop point：** Human明确回复之前立即停止。不得委派 Executer、创建 root、访问设备、运行 cleanup、
生成release或写 `REF-P7-23` execution package。

## 1. Completed pre-EQ gate

- C1 acceptance archive：
  `.agent-work/PLANS/20260727-1309-p7-r6-pre-eq-c1-acceptance-review.md`，SHA-256
  `35e0e49aaa91f438602346cb70af46efdfd520e1a1a508b393dc1ddc37940470`。
- Reviewed C1 PLAN SHA-256：
  `e1baa5877e4d6b74b50dce92e7fa06e11af684bcb6f60bed985fd0f991e270f2`。
- Terminal EXECUTION_RESULT SHA-256：
  `aa08b4ba9a2b5301880fa4097d3d557d22817b5bc63f54e4a88e4533907a2807`。
- Orchestrator review-state FULL SHA-256：
  `5fff0f9a11f4b1bdff6e25919f6f9c702458dd77ba360b6ebf73210063cb71c9`。
- Applicable GUIDE SHA-256：
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`。
- Accepted checkpoint：
  `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`，parent
  `1e3b107b8fbfe97bae5624ef638c4883a0faee1d`。

Planner已接受并完成：

```text
REF-P7-18-C1
REF-P7-18
REF-P7-19
REF-P7-20
REF-P7-21
```

这只证明 pre-EQ code/config、fake contracts、evidence owner与checkpoint通过；不证明 state C exposure
qualified、scientific settled、TD-B pass、device ready或 release可用。

## 2. Human confirmation requested

请求 Human 只确认是否允许进入以下一个 stage：

```text
experiment_id = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
purpose = qualify fixed state-C shutter for a later full Ray R6
source = Ray120c only
strip = generation-bearing zero throughout
formal = 0
ambient = 0
retry = 0
maximum candidates = 2
maximum physical CR3 = 8
```

这是 4.GUIDE 要求的分阶段科学 checkpoint。虽然项目规则规定 active PLAN内普通 bounded light操作本身
不需要危险操作授权，Advisor仍明确要求在 pre-EQ gate后由 Human单独确认是否进入这个新实验阶段。
因此 Human此前的一般性“允许调用设备”“Wi-Fi已恢复”或“恢复 Planner/Executer循环”不能替代本次确认。

## 3. Exact candidate order and budget

Candidate 1：

```text
nominal shutter = 1/2500
capture IDs =
  000-ray-c2500-t60
  001-ray-c2500-t120
  002-ray-c2500-t300
  003-ray-c2500-t600
physical cap = 4
```

分支：

- `4/4` quality pass：选择 `1/2500`，candidate 2调用0；
- 任一已返回 capture **仅因 clipping** failure：立即结束 candidate 1，不补剩余slot；完成双源zero/
  cleanup/seal后才允许 candidate 2；
- low-signal、nonfinite、valid-pixel、metadata、source isolation、readback或cleanup任一failure：立即停止，
  candidate 2调用0。

Candidate 2仅在上述 clipping-only分支允许：

```text
nominal shutter = 1/3200
capture IDs =
  004-ray-c3200-t60
  005-ray-c3200-t120
  006-ray-c3200-t300
  007-ray-c3200-t600
physical cap = 4
```

- `4/4` quality pass：选择 `1/3200`；
- 任一 required failure：`exposure_window_unresolved`并停止；
- 禁止 `1/4000`、`1/5000`、自动搜索、auto exposure、weak reacquire、现场增加candidate或retry。

两档合计最大：

```text
setup physical CR3 = 8
formal CR3 = 0
ambient CR3 = 0
retry = 0
```

## 4. Exact light sequence and duration

每个 candidate是独立 sequence：

```text
verify strip generation-bearing zero
-> Ray A = H120/S100/INT100 for 600 s, no capture
-> A to C = H300/S100/INT100
-> C captures at requested 60/120/300/600 s
-> Ray off
-> Python cleanup
-> shell cleanup
-> independent final-zero readback
-> terminal seal
```

每档约有 `A 600s + C 600s = 1200s`（约20分钟）连续灯光窗口，另加命令/readback/capture/cleanup
开销。若两档均按合法分支运行，是两条独立 sequence，最大约 `2400s`（约40分钟）灯光窗口，另加开销。
Candidate 1进入 candidate 2前必须先完成双源generation-bearing zero与完整cleanup/seal。

Ray与strip不得同时非零。strip全程为0；qualification不采A图、不计算TD-B history、不证明state C settled。

## 5. Quality and evidence boundary

未来 `REF-P7-23` execution PLAN必须逐 capture要求：

```text
58/58 required features
clipped_fraction == 0.0 for every required feature
near-noise / finite / valid-pixel pass
recorded Canon:ExposureTime present
existing nominal/recorded ratio gate pass
Ray command/readback pass
strip generation/readback zero
source isolation pass
CR3/sidecar path/bytes/SHA and remote IDs
physical return persisted before post-processing
chronology/timing/accounting pass
```

Observer、features、threshold、covariance、joint coverage、no-ambient statistic、A/D/B shutters与600秒
transient语义均不改变。

## 6. Future execution safety if Human confirms

Human确认只解锁 Planner编写一个新的 exact `REF-P7-23` PLAN；当前文件本身仍不授权执行。新 PLAN必须：

- 在
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/`
  下冻结一个不存在、非symlink、绑定checkpoint和timestamp的unique root；
- 冻结 exact checkpoint/policy/GUIDE/PLAN hashes与两个candidate IDs；
- 使用 visible macOS Terminal，因为单档运行预计超过10分钟；
- 定义单一launch、PID/ledger、三次稀疏liveness与Orchestrator automation；
- 无条件执行 Python cleanup、shell cleanup、independent final-zero和terminal seal；
- 任一失败保留progressive/physical/terminal evidence并停止；
- 不自动生成successor release、不启动full R6、strip或TD-C。

本 checkpoint不授权 firmware、flash、remote deployment、destructive hardware、R6 formal、strip、TD-C、
release或任何更宽 shutter/intensity/duration范围。

## 7. Explicit Human response boundary

若 Human同意，应明确表达等价于：

```text
我确认只进入 P7-TD-B-RAY-C-EXPOSURE-QUAL-R6：
按 1/2500 -> 仅clipping时1/3200、最多8张CR3、retry0、每档A600+C600、
双cleanup/final-zero/terminal-seal边界执行。
本确认不授权 full R6、strip、TD-C、release或更快shutter。
```

若 Human拒绝或要求改 candidate、预算、强度、duration、source或科学合同，Planner必须停止并按变化类型
回 Advisor/Human decision，不得自行修改。

## 8. Current prohibitions

Human明确确认且 Planner另写/验收 `REF-P7-23` PLAN前：

```text
Executer dispatch = 0
root creation = 0
device/network/.env/camera/Ray/strip/light/all_off = 0
capture/CR3 = 0
release generation/qualification/consumption = 0
EQ-R6 launch = 0
formal R6/strip/TD-C = 0
commit = 0
```

维护性判断：本文件只保存 staged Human checkpoint与未来运行边界，不新增代码、runner或evidence owner；
下一步取决于Human是否明确确认该单一EQ-R6 stage。

---

## Planner review：Human checkpoint 已满足，但真实 EQ-R6 owner 尚不存在

**Review 时间：** 2026-07-27 13:24（America/Edmonton）

**Reviewed PLAN SHA-256：**
`0c6530260eb60e052a4cd08fc65bab1e50dcac51846f543c6d238fd0c25a896f`

**Human 原文确认：**

> 我确认进入 EQ-R6：先运行 1/2500，仅在 clipping-only 失败时运行 1/3200；最多 8 张 CR3、retry 0、每档 A600+C600，并执行双 cleanup、final-zero 和 terminal seal。

### Review method 与证据

- Human 的确认逐项覆盖本 checkpoint 冻结的 candidate order、clipping-only 分支、physical cap、retry、
  每档时长与 cleanup/seal，因此 `REF-P7-22` 判定为 `ACCEPTED_COMPLETE`。
- 当前 HEAD：
  `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`；parent：
  `1e3b107b8fbfe97bae5624ef638c4883a0faee1d`。
- applicable GUIDE：
  `advisor/4/4.GUIDE.md`，SHA-256
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`。
- Orchestrator FULL review input SHA-256：
  `8ae0344a638e92cbf5207cb78a1858f73315d0aaf071350c650bd211ec3f46f8`。
- terminal Executer handoff SHA-256：
  `aa08b4ba9a2b5301880fa4097d3d557d22817b5bc63f54e4a88e4533907a2807`。
- accepted pre-EQ archive：
  `.agent-work/PLANS/20260727-1309-p7-r6-pre-eq-c1-acceptance-review.md`，SHA-256
  `35e0e49aaa91f438602346cb70af46efdfd520e1a1a508b393dc1ddc37940470`。
- Planner 使用 CodeGraph 与源码/CLI/wrapper 静态核对发现：
  - `build_td_b_eq_r6_plan()` 明确返回 `status=offline_contract_only` 与 `executable=False`；
  - `validate_td_b_eq_r6_plan()` 只接受该 exact non-executable contract；
  - `run_td_b_eq_r6_fake()` 是唯一 EQ-R6 scheduler，并明确只接受 injected fake owners；
  - production CLI 的 `--execute` 不存在 EQ-R6 mode，只会进入既有 setup/formal runner；
  - production wrapper 能记录 child exit 与 shell cleanup，但不存在把 candidate 1 与 conditional candidate 2
    分成两个各自完整 cleanup/final-zero/terminal-seal sequence 的 live EQ owner。

### Planner decision

`REF-P7-22` 的 Human checkpoint 已完成；但 `REF-P7-23` 不能直接判为 device-executable。
若直接派发，会把 offline-only contract 交给不识别 EQ-R6 的通用 formal/setup runner，无法证明 exact
candidate branch、每档独立 lifecycle、physical cap 与 terminal seal。

因此 exact next branch 是：

```text
REF-P7-23-C0
P7-TD-B-EQ-R6-LIVE-RUNNER-PREEXEC-CORRECTION
pure offline
device/network/.env/camera/light/all_off = 0
```

该 correction 只建立并离线验证复用现有 thermal/camera/physical-return/wrapper owners 的真实 EQ-R6
入口与生命周期。修复通过 Planner 验收后，若实验范围、candidate、预算、强度与时长均未改变，
本 archive 中的 Human 确认可由后续 `REF-P7-23` PLAN 直接消费，不得要求 Human 重复批准同一 stage。

### Residual locks

- correction 完成前，EQ-R6 device launch、root creation、network、`.env`、camera、Ray、strip与真实
  `all_off` 全部为0；
- successor release、full Ray R6、strip、TD-C、public R5 analyzer、firmware、deployment仍锁定；
- correction 不得改变 observer、58-feature owner、quality thresholds、A/D/B shutters、C candidate
  order、600秒语义、8 CR3 cap或retry 0；
- correction 失败必须停回 Planner，不得以 fake tests通过替代真实入口的结构证明，也不得现场补写
  launcher后立即访问设备。

### Exact next branch

Planner 将 active PLAN 改写为唯一 pure-offline `REF-P7-23-C0` correction package。Executer完成代码、
测试、wrapper lifecycle fake/adversarial evidence与focused commit后必须停止，交 Planner验收；不得
在同一 package 中启动 EQ-R6。
