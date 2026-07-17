# 阶段 3：4x3 CCT Multipatch 先导

**覆盖原阶段：** P4

**进入条件：** Gate-2 已冻结前向模型分支、feature/patch 集和目标层级。

**阶段目标：** 只用 12 点回答 multipatch 是否在不损害白点的情况下产生超出重复性噪声的稳定改善。

**不得跨越：** 这是从 12 点扩大到完整 70 点前最重要的成本与方向门；执行模型绝不自行扩网格。

**Gate-2 冻结输入（2026-07-16）：**

- 出口：`forward_model_seed_only`，P4 固定走 C-F；禁止把 P2 basis 当全局真值。
- basis artifact：`/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935/basis-analysis.json`，SHA-256=`5024dcf3c14146b5750db6de21040c7745c62b955a63f97c4b86128b83a1b6c1`。
- feature 维度固定为 `block_02..block_24 x R/G1/G2/B = 92`；block_01 black 只作诊断，不进入优化。
- neutral 硬门固定使用 block 02..06；有色 training 固定为 block `07,09,10,12,13,15,16,18,19,21,23`，holdout 固定为 block `08,11,14,17,20,22,24`。不得看 P4 结果后换组。
- 允许复杂度：basis seed + 现有局部 bounded Jacobian/Broyden/secant/thermal rebase + multipatch residual。禁止全局开环求解、简单 load correction、未留出验证的 interaction 展开和高阶多项式。
- P3 证据：24 点 shape P95 中位 `6.43%`、0/24 达到 80% feature <=2 sigma；最终 anchor shape P95 `0.281%`，因此失败来自混合不可加而非整场漂移。

## 执行顺序

1. 按冻结分支实现独立 pilot objective/solver/runner 和合成测试。
2. dry-run 审计通过并获用户实机授权后完成 12 点同轮 A/B。
3. 任何 solver 修正只按 C-C/C-E 的既定规则重跑完整 12 点；不得只挑通过点拼结果。
4. 汇总白点、training、holdout、重复性、命令连续性、RGB 使用和不可达点。
5. 形成 Gate-3 交接包后停止，不创建 70 点候选。

## 高级模型决策门 Gate-3

允许出口：

- `expand_to_70`：仅 C-A，12/12 两次确认、白点非劣且 training/holdout 改善超过重复性。
- `retain_white_only_end_cct_route`：C-B，multipatch 无工程收益。
- `repeat_pilot_after_objective_fix`：C-C，词典序/约束实现错误。
- `revise_extreme_gamut_model_then_repeat_12`：C-D，只允许一次定向模型修正后重跑全部 12 点。
- `thermal_repeat`：C-E。
- `stop_route`：连续失败或证据不足。

只有高级模型写出 `expand_to_70`，阶段 4 才可开始。

---

## 10. P4：4x3 CCT multipatch 先导 A/B

### 10.1 固定目标

```text
CCT: 1800, 3200, 5600, 20000
GM raw: 0, 100, 200
总计: 12 points
```

每点同轮采集：

1. Ray 实测目标。
2. 当前最佳 70 点 LUT 命令。
3. 新 multipatch 候选命令。
4. 两种 strip 命令各两次独立 off/on 60 秒确认。

### 10.2 求解器代码边界

建议新增：

```text
src/camera_based_rgbww_optimizer/optimization/multipatch_objective.py
src/camera_based_rgbww_optimizer/optimization/multipatch_solver.py
src/camera_based_rgbww_optimizer/optimization/measure_cct_multipatch_pilot.py
tests/test_multipatch_objective.py
tests/test_multipatch_solver.py
tests/test_measure_cct_multipatch_pilot.py
```

不要直接把试验逻辑塞进 `measure_white_lut.py`。先让 pilot 独立，P4 通过后再抽取共享 capture/feedback 边界。

现有 `white_lut_feedback._solve_box_constrained_least_squares` 是小维度 active-bound 枚举。新求解器若需要同样语义：

1. 先给现有行为补完整回归测试。
2. 抽到 `optimization/bounded_least_squares.py`。
3. 现有白点 feedback 和新 solver 都调用同一实现。
4. 不复制一份略有不同的 bounds/clipping 代码。

### 10.3 词典序目标

严格按顺序，不能用一个加权总分允许后项抵消前项：

1. 中性 patch RAW chroma 进入硬门槛。
2. 当前 CCT/Duv 门槛通过。
3. 在前两项可行域内最小化彩色色块稳健误差。
4. 再最小化留出 patch 误差。
5. 再考虑邻点连续性、RGB 软先验、headroom 和敏感度。

模型包含允许的全局亮度比例 `k>=0`，以匹配光色而非绝对亮度。命令约束：

```text
0 <= u_j <= 1
max(u) = 1
```

通过枚举 active channel 保证 `max(u)=1`，不要先无约束求解再 clipping。

### 10.4 训练/留出冻结

- 所有可靠 neutral patch 都用于一级硬目标。
- 黑块只作诊断。
- 有色 patch 在优化前按固定规则分成 training 和 holdout，规则写入 config/hash。
- 不得看结果后重新选择留出 patch。
- 若有额外材质，作为第二层 holdout；没有则明确记录。

### 10.4.1 离线实现状态（2026-07-16）

- `config/camera/cct-multipatch-pilot.json` 已冻结 4x3 grid、neutral/training/holdout、白点门槛和局部 solver 参数，当前 SHA-256=`75f642f261355a4b564263e363ac9791a370b53dd97dcb382571980b1f9ae5da`。
- `multipatch_objective.py` 使用非负全局亮度比例，并输出严格词典序 rank；neutral 或 white-point 越界时，training/holdout 改善不能抵消硬门失败。
- `multipatch_solver.py` 对 neutral/white/training/holdout 前缀生成有界候选并按词典序选择；active channel 始终固定为 `4095`，不使用 solve-then-clip。
- 小维度 box-constrained least squares 已抽到共享模块，现有 white feedback 与 P4 共用。
- `measure_cct_multipatch_pilot.py --dry-run` 只读取冻结 artifact/config 并生成 12 点、84 张正式 A/B 协议；dry-run 证据：`tmp/cct-multipatch-pilot/p4-runner-preflight-20260716/plan.json`。
- runner、安全路径和新增测试完成后的完整测试为 `295/295`；离线缺口已经在 10.4.2 收口。

### 10.4.2 实拍状态（2026-07-16）

- 上述 runner 缺口已补齐；正式 CLI 仅允许 `--execute --allow-high-output --camera-backend remote`，启动时复验全部冻结 SHA，RAW report 直接生成 92 feature 和白点，不保存 `.npy`。
- 候选只有在 neutral/white 硬门通过且词典序严格优于同轮 baseline center 时才确认；无法改善的点仍补两张 settled final verification，供 C-B/C-D 判断。
- `tmp/run-cct-multipatch-pilot.zsh` 提供独立 shell trap；当前环境不能保留脱离 exec 树的 nohup 子进程，正式 retry 由持久 PTY session 承载 wrapper，Python finally 与 shell trap 不变。
- 最近 run：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260716-165518-retry5`；已失败并完成双 cleanup，原 Automation `p4-retry5` 已删除，目前没有活动 P4 进程或 heartbeat。
- `analyze_cct_multipatch_pilot` 已在运行期间离线完成：强制 12 点、recorded exposure、零 `.npy`、双 cleanup，并把 settled candidate 对 baseline center 的 training/holdout mean/P90/worst 改善与同轮 `3 sigma` 重复性分开报告；只输出 Gate-3 证据，不自动选分支。
- retry5 失败目录必须保留；修复通过完整离线验证后只能用全新 retry6 目录重跑。

### 10.4.3 retry4 低信号分支（2026-07-16）

- retry4 在首点 baseline 后按质量门停止：`block_24::B` near-noise fraction=`0.07119`，冻结上限=`0.05`；91/92 feature accepted，无裁切、非有限或像素数失败。
- run 保留 3 个非空 CR3、3 个 recorded-exposure measurement、`failure.json`、零 `.npy`，Python/shell cleanup 与恢复 all-off 均成功。
- 按 P1 合同没有放宽 observer 阈值或删掉 holdout feature。只有 status included、像素数/非有限/裁切均通过且纯 near-noise 超标时，runner 才在验证过的 `1.0..1.25x` envelope 内补拍一次；其他拒绝以及补拍仍失败会保留证据并关灯。
- shared native capture adapter 现在对任何显式 `exposure_factor` 使用相机支持的 fixed bracket，不再把该语义绑死到 P1 purpose 名称。完整测试 `300/300`。

### 10.4.4 retry5 极端参考不可观测分支（2026-07-16）

- retry5 完成 `1800K/gm0`：26 个 feedback sample，前四次 settled confirmation 失败后 thermal rebase，第五次以两张 settled capture 确认；最终命令 `cw=72, ww=3866, r=4095, g=42, b=95`。
- 第二点 `1800K/gm100` 的 Ray 参考在自动曝光 `1/4000` 时有 3 个 B feature 纯弱信号；`1.25x` 重拍 `1/3200` 后只剩 neutral 硬门 `block_02::B`，near-noise fraction=`0.23951`，仍显著高于冻结 `0.05`。继续加曝光会越过 P1 的 `1.0x..1.25x` 可信包络，因此禁止继续曝光、放宽阈值或使用被拒数据。
- retry5 保留 54 个非空 CR3、54 个 recorded-exposure patch report、零 `.npy`；`failure.json` 为 `RejectedOptimizationFeaturesError`。Python/shell cleanup 均确认 ESPHome 与 Ray 关闭。
- 该失败属于 C-D 的测量不可观测证据，不是 solver 或目标可达性的证明。runner 现在只对“Ray 参考在一次 `1.25x` 补拍后仍纯弱信号”写入 `measurement_unreachable` target row 并继续；混合、裁切、非有限、像素数失败仍终止并双关灯。
- Gate-3 analyzer 保留 12 行完整性要求，但只对 evaluable points 做数值聚合；任何 `measurement_unreachable` 都强制 C-A=false，并报告不可观测点是否仅位于极端 CCT 及 continuity 被省略的边。默认 LUT、feature split、质量阈值和曝光包络均未改变。
- 新增纯弱信号继续、混合质量失败 fail-fast 和 analyzer 聚合/continuity 回归；完整测试 `303/303`、compileall、`git diff --check` 和 CodeGraph sync 通过。
- retry6：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260716-184129-retry6`，wrapper PID=`66447`、Python PID=`66450`、PTY session=`48974`、启动时间=`2026-07-16T18:41:34Z`、Automation ID=`p4-retry6`。3 分钟检查为 2 个非空 CR3/recorded report、无 failure/.npy，ambient -> 双关 -> Ray -> off -> 双关 -> strip 的隔离顺序正确；后台继续运行。
- retry6 在上一轮结束后被执行环境连同 Codex PTY 回收，未执行 trap；发现时 run stale-running、无 Python/shell cleanup，最后 command 为 strip on。独立恢复 `all_off` 两路成功，证据写入 `all-off-recovery.json`；run 标记 `interrupted`/`ExecutionEnvironmentProcessReaped`，过期 Automation 已删除。该目录只作失败证据。
- retry7 改由 macOS Terminal `/dev/ttys001` 独立承载 wrapper：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260716-184900-retry7`，wrapper PID=`73293`、Python PID=`73359`、启动时间=`2026-07-16T18:48:48Z`、Automation ID=`p4-retry7`。3 分钟检查为 3 个非空 CR3/recorded report、无 failure/.npy，进程与 source isolation 正常。
- retry7 在 `19:33Z` 安全失败：`1800K/gm0` complete，`1800K/gm100` 为 Ray-reference `measurement_unreachable`；`1800K/gm200` 的 strip baseline 在 `1.25x` 后仍有 `block_10::B=17.381%`、`block_24::B=23.334%` near-noise，因 runner 尚未把 baseline 不可观测降级而退出。57/57 CR3/report 非空、零 `.npy`，Python/shell 双 cleanup 两路成功，Automation 已删除。
- runner 现在也把补拍后仍纯弱信号的 strip baseline 记录为 `measurement_unreachable(stage=strip_baseline)` 并继续；candidate feedback 以及任何混合/裁切/非有限/像素数失败仍 fail-fast。新增回归后完整测试 `304/304`、compileall、diff-check、CodeGraph sync 通过；沙箱内 loopback 4 项权限错误已在允许 loopback 的同一套测试中复核通过。
- retry8：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260716-212822-retry8`，独立 Terminal tty=`/dev/ttys001`，wrapper PID=`15461`、Python PID=`15537`、启动时间=`2026-07-16T21:28:47Z`、Automation ID=`p4-retry8`。3 分钟检查为 3 个非空 CR3/recorded report、无 failure/.npy，source isolation 正常；后台继续运行。
- retry8 在 10/12 target row 后安全失败：6 complete，4 measurement-unreachable（`1800/gm100` Ray、`1800/gm200` baseline、`5600/gm100` Ray、`5600/gm200` Ray）；到 `20000/gm100` 的 `candidate_feedback-3` 时，`block_12::R` 在 1.25x 后 near-noise=`0.09355`，旧行为把单个候选拒绝升级为整轮失败。166/166 CR3/report 非空、零 `.npy`，Python/shell 双 cleanup 成功，Automation 已删除。
- feedback 现在把补拍后纯弱信号候选作为无效 trust-region step：记录证据后依次测试从当前合法命令到请求命令的 `0.5`、`0.25` 回退，只有合法观测进入 samples/Jacobian；全拒绝则保留最佳合法命令并走 final verification。settled confirmation 拒绝按失败确认处理并允许 thermal rebase；setup/probe/final verification 不可测则目标行记 `measurement_unreachable`。混合质量错误仍 fail-fast。
- 信任域回退、拒绝样本隔离、confirmation rejection 和 runner unreachable 既有分支的完整测试为 `306/306`；compileall、`git diff --check`、CodeGraph sync 通过。
- retry9：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260717-000819-retry9`，独立 Terminal tty=`/dev/ttys001`，wrapper PID=`82852`、Python PID=`82965`、启动时间=`2026-07-17T00:08:42Z`、Automation ID=`p4-retry9`。3 分钟检查为 3 个非空 CR3/recorded report、无 failure/.npy，source isolation 正常；后台继续运行。

### 10.5 P4 分支

#### C-A：12 点全部通过并稳定改善

条件：

- 12/12 点两次确认均满足中性 RAW 和 CCT/Duv 门槛。
- 白点对当前候选非劣。
- training 与 holdout 的平均、P90、最坏误差改善超过配对重复性。
- 没有明显命令跳变或只靠大量 RGB 换来小于噪声的改善。

动作：冻结 pilot 权重和目标定义，进入 P5。P5 不允许根据最终验证结果继续调 pilot 权重。

#### C-B：白点通过，但有色/留出改善不超过噪声

- 保留当前 70 点候选。
- multipatch 只作为诊断和验收报告。
- 不进入完整 70 点重算。
- 可以结束 CCT 新算法路线，转 HSI 前需记录此结论。

#### C-C：有色误差改善，但白点越界

- 判定求解目标实现错误或硬约束不足。
- 不放宽当前白点门槛。
- 修正词典序/可行域后只重跑 12 点。
- 连续两版仍失败则停止该路线。

#### C-D：只在 1800/20000 或极端 GM 失败

- 检查 basis 外推、gamut、active channel 和 RGB 先验。
- 若目标不可达，输出明确 `unreachable`，不得靠放宽门槛伪装。
- 可做一次只针对极端点的模型修正，但修正后必须重跑完整 12 点。

#### C-E：两次确认不一致

- 优先判定热态/漂移，不先改 solver。
- 失败确认成为新 thermal base，重建局部 Jacobian。
- 冷态样本不得继续进入 active secant 窗口。
- 稳定后完整重跑受影响点的两次确认。

#### C-F：前向模型 P3 为 seed-only

- 用模型只生成初值。
- 实拍反馈目标扩展为 neutral + multipatch residual。
- 仍保留现有 bounded Jacobian、Broyden、secant 和 thermal rebase。
- 若高维反馈无法稳定估计，退回白点反馈并把 multipatch 仅用于候选排序。

### 10.6 Gate-3 最终决定（2026-07-17）

- 最终 run：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260717-000819-retry9`；12/12 target row，7 complete、5 measurement-unreachable，192/192 CR3/report 非空且 recorded exposure，零 `.npy`/failure，Python/shell 双 cleanup 成功，command audit 无 source-isolation violation。
- `gate3-analysis.json` 显示 7 个 evaluable 点的 training/holdout mean、P90、maximum 改善全部超过同轮 `3 sigma`，且所有 evaluable 点白点非劣；但 `1800/gm100`、`1800/gm200`、`5600/gm100`、`5600/gm200`、`20000/gm200` 不可观测，其中包含内部 `5600/gm100`，不是仅极端 CCT/GM 的 C-D。
- `3200/gm0`、`5600/gm0`、`20000/gm0` 的 settled neutral hard gate 失败；`5600/gm0` 同时白点越界。location 的 180° `standard_index_formula=25-block_index` 已复核，`block_02..06` 正确对应标准 neutral 23..19，不是 patch 编号错误。
- 决定：`Gate-3=keep_white_lut_diagnostic_only; stop_before_p5`。不改冻结 feature/quality threshold，不用被拒数据，不扩到 P5 70 点；保留当前外置 white-only 70 点候选，multipatch 仅作为诊断证据。
- 衔接 Gate-4：`retain_previous_candidate; approve_stage_5`。不安装或覆盖默认 LUT；允许进入 Ray-only HSI 表征，strip HSI 仍锁定到 Gate-5。

---
