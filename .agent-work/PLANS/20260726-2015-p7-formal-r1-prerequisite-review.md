# Planner 验收归档：P7-TD-B-FORMAL-R1 prerequisite gate

**审查日期：** 2026-07-26 20:15

**审查范围：** `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r1-prereq/20260726T200000Z/`

## 证据

- 离线 prerequisite gate 恰好执行 `1` 次并 hard-stop。
- 当前 HEAD `0387bcfa53e52ee7f99d5308886e2b7873fe49f5` 下没有
  `production_release_usable=true` 且 checkpoint exact 的 release。
- 历史 `fa6c95d` release 以及 mismatch fixtures 均被明确拒绝；setup、resolved formal
  plan、physical ledger 未被继续消费。
- 设备、相机、Ray、setup、formal、public analyzer、retry、release rebuild、Git 均为 `0`。
- prerequisite SHA-256：`ce0907c692ec280d80c9ae4656b01b61da0d9a076ae55afe816c97bef61b0005`。
- terminal SHA-256：`b981aa373fdae841f8aa5551b5868777f5774fa062211ac8d770f18b2b2ed356`。
- validation SHA-256：`446a36020b2e5cdd9be3c3b0878a4cc9b0027917b425db4d37e3f122fa0f09e9`。

## 决定

拒绝 FORMAL-R1 直接进入 formal，但接受其 fail-closed 结果。根据当前 GUIDE 的
TD-B v2 lineage 条款，允许发布一个新的、纯离线的 lineage-release qualification 包：
先只读重放 immutable legacy setup/release，生成并审查 changed-path ledger 与
`production_release_usable=false` 的 candidate；candidate 被 Planner 接受后，才可
运行独立 qualification 生成当前 HEAD 的 v2 release。该 release 仍不授权 formal；
必须由后续 Planner 重新验收 exact release 后另发 formal PLAN。

GUIDE 对此路线、候选状态、旧 release 不可执行和当前 clean checkpoint 绑定均已明确，
不需要 Advisor 决策；Advisor 只有在 replay 发现 changed path 涉及 camera/remote parsing、
setup semantics、frozen inputs、budget、command、shutter 或 cleanup 时才介入科学分支。

**下一分支：** `REF-P7-04` bounded offline lineage-release qualification；禁止设备访问、
相机/Ray/formal、重试和自动消费历史 release。

