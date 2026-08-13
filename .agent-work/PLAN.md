# PLAN — GUIDE6 direct target-local HSI INT100

## 当前状态

`v4-corrected/analysis-v4-exact-context-sign-corrected-derived.json` 已按 GUIDE6 生成；旧 v3
保留为 immutable historical evidence。v4 的 scientific classification 为：

```text
B_local_coordinate_transfer_unresolved_with_anchor_direction_compatible
```

v4 结果不再作为新的 Advisor gate：

- B exact pre residual：`24.341350574998774`，fail；
- B exact post residual：`24.37011085295253`，fail；
- B anchor direction：`2.8927944104915984`，pass/compatible；
- B-minus-C residual：`21.57223112462142`，fail；
- `max_abs(post - pre - h_B) <= 1e-12`，`L2 <= 1e-12`。

canonical v4 artifact SHA-256：
`81d967834e51a8481bacb6bbb36ff9e8685b7f86a3383f3a8c4bd0bb547d5b40`

## 已关闭的路线

- 跨 experiment 的 `core A absolute offset + local coordinate` synthesis：永久禁止；
- `GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1`：`deferred_diagnostic_only`，不进入
  active device path；
- B pre/post 两个 variant：`deferred_diagnostic_only`；
- C anchor decomposition、solver sentinel、P8 和后续阶段：保持锁定，直到本路线
  的预定义分支解锁。

## 唯一 active next action：H120/S100 direct target-local block

实验 ID：`GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-V1`

计划 builder：`build_direct_plan(p7_td_c_balanced_source_comparison_v1,
variant="guide6-direct-target-local-h120-s100")`

当前状态：`human_authorization_pending`，`formal_capture_eligible=false`。
本文件只整理 Human 授权请求，不代表已授权或已启动。

目标块：`H120/S100/INT100`，FAST envelope，reset/off proxy `600 s`，每个 command
或 precondition dwell `120 s`，不声称 steady/settled，ambient `0`。

流程：

1. Ray verified zero；Ray reset 600 s；`D(H120/S50) 120 s → A(H120/S100) 120 s
   → Q(H120/S100) 120 s → capture Ray Q_before → Ray off`；
2. Strip verified Ray zero；strip reset 600 s 一次；`D 120 s → A 120 s → candidate
   Q 120 s → capture strip candidate`；
3. strip all zero；Ray reset 600 s；重复 `D → A → Q`，capture Ray Q_after；
4. cleanup、source isolation、Ray before/after compatibility 和 strip base drift
   evidence 必须完整。

本 block 的比较只使用同一 target block 的 direct Ray target 与 strip candidate：
`e_q(u)=f_strip,q(u)-f_Ray,q`。禁止读取任何其他 experiment 的 absolute synthesis
结果来替代 Ray target。

Human 需要明确授权的范围仅为：启动该 bounded H120/S100 direct target-local
block，包含 Ray/strip light control、camera capture、600 s reset proxy、120 s
dwell 和正常/异常 cleanup；不包含固件刷写、远程部署、solver sentinel 或后续阶段。

## 预定义后续分支

- S-PASS：H120/S100 与 H120/S50 measurement valid；H0/S0、H300/S100 按 GUIDE6
  预定义规则完成；Ray brackets、drift、cleanup 均通过后，自动进入 13-node INT100；
- S-SOLVER-RETRY：核心点 measurement-valid 但 solver fail；一次 offline review，
  一次同合同新 root repeat；再次失败才是 `ADVISOR_GATE_REQUIRED`；
- S-MEASUREMENT：冻结 observer envelope 内无合法曝光；一次 bounded exposure
  diagnosis，仍无合法曝光则 `ADVISOR_GATE_REQUIRED`；
- S-REFERENCE：Ray before/after bracket failure；允许一次新 root repeat，第二次
  failure 为 `ADVISOR_GATE_REQUIRED`；
- 普通实现错误直接在当前 worktree 修复并恢复可复现结果，不构成停止门。

## 禁止事项

不得改 observer、58 features、CFA、exposure envelope、covariance、coverage、
threshold、P6 topology、SAT0/HSI-RGB semantics 或 Human reset/dwell ceilings；不得
把 solver failure、measurement failure 或 `unconfirmed` 宣称为物理 gamut；不得
进入 P8、final LUT install 或 runtime installation。

## 证据与复现

源实现、测试、v4 artifact、v3 artifact、parent evidence 和 GUIDE6 均保持 Git/外置
盘原路径可追溯。raw CR3/RAW/DNG、图像、decoded arrays、build/firmware/cache 不进
Git；只保留小型 manifest、hash、quality、analysis、cleanup 和报告。
