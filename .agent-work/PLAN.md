# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1：marker parsing / limited-input gate 纠偏

**计划状态：** `active_executable_limited_input_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1`

**Superseded task:** `REF-P7-25-R2-B1A-C3E6F17`（已拒绝；不得重试其 root 或四固定路径）

**只读 FULL SHA-256：** `15127763a68a68b70404ce57ece44efbbfc1375a844588520584e2d1615b6725`

**Reviewed archive：** `.agent-work/PLANS/20260729-1755-p7-retained-r3-option-b-b1a-c3e6f17-limited-input-review.md`

## 唯一动作

Executer 仅进行一次本地、离线、无副作用的 corrective qualification，修复并验证 bootstrap loader 对当前 Markdown inline-code machine rows 的语义：

- PLAN 只接受恰好一条反引号包裹且内容前缀为 `PLAN_MACHINE_CONTRACT=` 的物理行，并截取 marker 后至结束反引号前的 JSON bytes。
- FULL 只接受恰好一条反引号包裹且内容前缀为 `FULL_PLAN_MACHINE_STATE=` 的物理行；不得把 `PLAN_MACHINE_STATE=` 当 alias。
- 两个 loader 均拒绝零/多 marker、缺失或错位反引号、malformed/duplicate-key/non-finite JSON、非 object、错误类型或 required-key mismatch。
- gate 失败必须在任何 `lexists`/`lstat`/mkdir/open/path inspection 前 terminal；不得检查、创建、删除或复用旧 F17 路径，也不得创建任何 artifact。

允许读取：当前 PLAN raw bytes、FULL 唯一 machine row 与 F17 section、shared Git metadata。禁止读取 ER、archive、controller/source、candidate、fixture、canonical content、tests、retained R3、release、网络、`.env` 或设备。

## 预算、证据与验收

本包不得运行 production controller/source/test/Git mutation/public analyzer，不得访问相机、Ray、strip、release 或 retained R3；所有 artifact/path operations、fallback、retry、reuse、rewrite、alternate path 均必须为 `0`。Executer 只向 `.agent-work/EXECUTION_RESULT.md` append 一次结果并停止。

必须记录：纠偏 loader 读取的 raw input SHA、marker extraction/strict JSON rejection case ledger、首次失败阶段、证明 path-operation counter 为 `0/0` 的本地记录，以及旧 F17 root 未触碰的声明（不得通过再次检查路径来证明）。不得声称 bootstrap、release、eligibility 或任何授权已成立。

## Planner stop

纠偏结果返回后立即停止。Planner 下一轮先归档本包并根据证据决定 REJECT 或是否另立 fresh-root bootstrap 计划；不得在本包内进入 bootstrap、controller、R3、release、network 或 device。
