# REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1 activation row failure review

**归档时间：** `2026-07-31T14:26:16-0600`

**Planner decision：** `REJECTED_DISPOSABLE_CONTROLLER_COMPOSITION`

**Reviewed reference：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-OUTER-PREFLIGHT-OWNER-CORRECTION-V1`

**Reviewed PLAN identity：** bytes `14244`，SHA-256
`0d22a6820284a15bd3b10daed80f5d7622a80eb2aa7c8589e449fa45e0a111ea`；完整 executable contract 保存在
`809eb85a3402b348079d0bd000bd7c1c9518acb1:.agent-work/PLAN.md`。

## 1. Reviewed scope and evidence

Activation `809eb85a3402b348079d0bd000bd7c1c9518acb1` exact 匹配 direct parent
`32899a26f36fbb73c3ab32d95da011b26d0a403a`、subject `chore(plan): correct p4 synthetic outer preflight` 与 exact paths
`.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`、
`.agent-work/PLANS/20260731-1410-p7-retained-r3-b2-p4-c1-c1-c1-i1-outer-git-failure-review.md`。唯一 ER append 由 evidence
commit `169e786d724c2f7064906957272b35096f7cc43a` 保存；其 direct parent 是该 activation，subject
`chore(evidence): record p4 activation row failure`，changed path exact only `.agent-work/EXECUTION_RESULT.md`。当前 ER bytes
`1056145`、SHA-256 `39df2352d34c852f26edbf0de14a27c9c79a24388f11cd6ee2a3affe168ebe7d`。

Executer 的唯一 outer `git rev-parse HEAD` exit `0`，stdout exact activation full SHA 加 LF，额外 outer Git `0`。Fresh source
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-controller-809eb85.py` 以 exclusive/no-follow
方式成功创建一次并保留：bytes `29371`、device `16777240`、inode `2227983`、mode `0600`。Accepted source read exact once；同一
in-memory bytes 完成 strict UTF-8、AST parse、builtin compile 与唯一 process dispatch。Source writer 在文件已成功 fsync/stat 后因 final
report 缺少 `json` import 自身 nonzero；文件未重写。由于 source read budget 已用尽，没有再读 source 求 hash，证据诚实保留该 gap。

Repo analyzer/embedded transport report 实际通过：analyzer `1`、external classifier `0`、bound results `18`、effect bindings `14`、fixture
bindings `4`、shared-root reads `7`、exact root-chain composition/validation `1/1`、effect transport empty。失败发生于 activation callback：
controller 自行实现的 machine-row parser 要求 raw Markdown line 直接以 `FULL_PLAN_MACHINE_STATE=` / `PLAN_MACHINE_CONTRACT=` 开头，未处理
authoritative row 的外层反引号，因而 stable primary `machine_row_count`。Controller-owned Git6 在该点尚未开始。

Lifecycle 随后调用 terminal；pre-root 状态没有 qualification target，local callback 抛 `qualification_target_missing`，repo lifecycle 最终外显
`ControllerConformanceError: terminal_failed`。异常链仍可辨认 primary/secondary，但没有一个明确的 structured primary machine record，secondary
也不应遮蔽 primary。这是 successor 必须纠正的 evidence lifecycle gap。

Fresh root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-qualification-809eb85` absent；Git6、root、four inputs、
matrix16、qualification、terminal artifacts、seal/admission、exact9 分别为 `0`。Process exact `1`，retry/fallback/second source/root/process
全部 `0`。旧 source/root/evidence、retained R3/candidate、Git replay、real B2、validator、eligibility、release、network/device 与所有 later-stage
域均为 `0`。

## 2. Findings and decision

`REV-P4-I1-C1-ROW-001` accepted：external controller 的 Markdown machine-row parsing 与 authoritative row grammar drift。Repo
`parse_plan_machine_contract` / `parse_full_plan_machine_state` 证明 canonical marker/suffix 是 leading backtick + marker、trailing backtick + LF；但把这两个
repo owner call 直接放入 actual source 会把冻结的 bound results 从 `18` 增至 `20`。因此 successor 使用父任务允许的另一条 exact route：只对两个 frozen
marker 各匹配一行，严格剥离一个 leading/trailing backtick 与 LF 后 strict JSON；不得形成 generic parser 或新增 owner binding。

`REV-P4-I1-C1-WRITER-002` accepted：source writer final report 漏 import `json`。虽然不破坏已创建 immutable source，也不改变本轮 primary，successor
必须在 fresh writer 中修复，避免成功写入被错误报告为 launcher failure。

`REV-P4-I1-C1-LIFECYCLE-003` accepted：pre-root primary 缺少 structured machine evidence，terminal callback 又以 missing qualification target 产生
secondary failure。Successor 必须在不写 root/artifacts 的 pre-root branch 保存 canonical structured primary，并让 terminal/seal/admission 的 in-memory
failure branch 完成后由 lifecycle 重抛 original primary；不得再调用 target-dependent terminal writer或产生 `qualification_target_missing`。

因此 I1-C1 被拒绝，不能报 synthetic qualification pass，也不能读取 retained R3、进入 real B2、canonical validator、eligibility 或 release。失败仅在
disposable source/controller composition；accepted repo analyzer、18 bindings、Git6、same-root4、matrix16、exact9 与科学合同均不得放宽。

## 3. Exact next branch

唯一 successor 是 `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1`：
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-MACHINE-ROW-AND-PRE-ROOT-EVIDENCE-CORRECTION-V1`。

它创建完全 fresh source/root，old I1-C1 source/root 不得读取、修复、删除、复用或再运行。Controller 对 activation 文件 exact bytes 只实现两个 frozen
marker 的 strict Markdown delimiter strip：leading backtick + marker、trailing backtick + LF、candidate exact one、strict UTF-8/JSON；不得使用原错误的
bare-marker match，也不得形成 generic machine-row parser。Fresh source writer 必须正确 import `json` 并成功报告唯一 exclusive write。

Pre-root failure 必须产生 canonical JSON machine line，至少包含 phase、primary exception type、stable code 与 repo parser evidence（若 applicable）；terminal、
seal、admission 走无文件的 in-memory failure envelope，并最终重抛原 primary。它不得访问 qualification target，也不得把 primary 转成
`qualification_target_missing` / `terminal_failed`。Success path 仍严格写 exact9。

## 4. Residual risks and locks

Fresh synthetic qualification 尚未成功完成，因此 retained R3 仍是 `RETAINED_UNVALIDATED_UNCONSUMED`。Successor 通过也只证明 synthetic
integration；所有 old evidence、retained/candidate、real B2、validator、eligibility、release、network/device/scientific/later-stage 域继续 hard locked。

维护性判断：本 finding 将 disposable parsing 收窄为两个 frozen marker 的 exact delimiter contract，避免触动 repo analyzer 的 18-binding owner surface；不改
生产代码/测试，不新增 generic parser、parallel analyzer、transport classifier 或 lifecycle framework。
