# P7 retained-R3 Option B：D2-C1-R1-C1 activation-budget failure 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1-C1-EXACT-TYPED-PROJECTION-PROOF-V1`

**Activation：** `2aee4fe7f4c9bc20c3e419771211c0532f59459c`

**Evidence：** `231eeb13d3171c198e4fb0ac18efc3ea4566e5d4`

**Planner 决定：** `REJECTED_ACTIVATION_GOVERNANCE_ACQUISITION_BUDGET_VIOLATION_NO_TYPED_PROOF_CREDIT`

## 1. Reviewed scope、topology 与 evidence quality

Planner完整读取repo `AGENTS.md`、project skill、committed PLAN/FULL及ER至physical EOF，并从Git object独立核验activation/evidence topology、subjects、changed paths及ER exact suffix。未读取、stat、list、search、hash、复用或修复任何old/fresh source/root；未运行owner selector、18-row Git ledger、physical input、canonical validator、release、network或device。

Activation `2aee4fe7f4c9bc20c3e419771211c0532f59459c`是`12861cf73721a845e3fc2ad4b96858eb92726c5c`的direct child，subject exact `chore(plan): attribute immutable projection types`，changed paths exact且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1444-p7-retained-r3-d2-c1-r1-type-projection-review.md`

Evidence `231eeb13d3171c198e4fb0ac18efc3ea4566e5d4`是activation direct child，subject exact `chore(evidence): record exact typed projection proof`，changed path exact `.agent-work/EXECUTION_RESULT.md`。Review开始时HEAD exact evidence且worktree clean。

Evidence ER以activation ER为exact prefix；新增physical-EOF complete suffix为`5025` bytes、SHA-256 `7c84db25e9ca13f60f90ad66f02b248bd80f519a544dd7fb8b81106d6367ae58`，包含唯一heading、唯一strict JSON handoff wrapper并以LF结束。Committed PLAN/FULL/ER identities分别为：PLAN `13155` bytes、SHA-256 `9633f22a30995b0908a6f16f39ecba5ba8f938f32271a328203b8a8185369f3b`；FULL `458106` bytes、SHA-256 `1646c78de2155445c3ef64d738f88ada608233448697d931453f13f0ebf2192c`；ER `1518705` bytes、SHA-256 `ba9ab30650ffdba04b4f17c26dae934938a77bd8f22f9393a625ff2351fd8128`。

## 2. Independent finding 与 validation quality

Activation topology本身正确，但Executer的首个activation metadata Git process只取得head/parent，遗漏subject。控制器随后启动一个不在PLAN四进程合同内、也不能提供冻结activation changed paths语义的generic `git status` process。此时已消耗`total_governance_and_input_git_processes=2`，其中`unauthorized_git_processes=1`；retry/fallback固定为0，因此正确在activation gate fail closed。

Handoff对失败边界的自报与ER delta一致：`subject=null`、`changed_paths=null`，subject/changed-path gates均false；activation changed-path process、committed PLAN/FULL raw-byte process、PLAN/FULL parser call、evidence mapping、type walks、typed projections、canonical serializations及strict reload全部为0。四份ordered type counts/container paths为空，四份projection与round trip均未执行，original graph pre/post equality未评估。44项zero locks逐项为0；preterminal stdout一次、ER physical-EOF append一次、postappend operations 0。没有source/root/artifact、owner selector、18-row ledger、production owner、lineage、manifest truth、eligibility或release证据。

因此拒绝D2-C1-R1-C1 typed-proof credit。该失败不是accepted parser、type walker或projection recipe的反证；它只证明一次性controller没有遵守activation governance acquisition contract。不得将未执行的四图proof视为pass，也不得直接解锁18-row attribution。

## 3. Exact next branch

唯一successor为同一reference task的activation-governance acquisition corrective。它必须冻结四个且仅四个Git process的exact argv，禁止generic `git status`、`git log`、`git rev-parse`、`git ls-files`或任何额外Git调用：

1. `[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,show,-s,--format=%H%x00%P%x00%s%x00,<activation>]`，strict解析exact三个NUL-terminated fields，再去掉Git stdout唯一final LF；取得HEAD、single parent与subject。
2. `[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,diff-tree,--no-commit-id,--name-only,-z,-r,<activation>]`，strict UTF-8/NUL paths exact等于冻结三路径，拒绝empty、duplicate、missing terminal NUL或额外path。
3. `[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,show,<activation>:.agent-work/PLAN.md]`，stdout exact raw bytes直接交给accepted PLAN parser一次。
4. `[/usr/bin/git,-C,/Users/ibobby/Projects/WLED-RGBWW,show,<activation>:.agent-work/FULL_PLAN_REFERENCE.md]`，stdout exact raw bytes直接交给accepted FULL parser一次。

所有process须stdin `/dev/null`、stdout/stderr pipes、cwd exact repo、shell false、text false、check false；exit必须0、stderr必须empty。metadata stdout必须只有冻结NUL layout及一个final LF，changed paths必须NUL-delimited，不得decode PLAN/FULL raw bytes或经filesystem/worktree取得它们。任何process启动/parse/gate失败即failure handoff，无retry/fallback；不得用generic repository-state probe补救。

四个acquisition gates通过后，原typed proof合同保持不变：accepted parser各一次、evidence mapping各一次；四个original graphs按exact container/scalar type域做pre/post共8次ordered path walk；四次typed projection、canonical in-memory serialization、strict reload与snapshot equality；immutable mutation0。最后只允许一次preterminal handoff stdout和一次ER physical-EOF append，postappend operations 0。

仍禁止source/root/artifact、owner selector、18-row Git ledger、physical input、repository source/test、validator、production-owner/lineage/manifest/eligibility/release、network/device/camera/Ray/strip/formal。成功只证明typed projection boundary；无论PASS/FAIL均停Planner review。

**Exact next reference：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R1-C1`。

**Exact next activation parent：** `231eeb13d3171c198e4fb0ac18efc3ea4566e5d4`。

**Exact next activation subject：** `chore(plan): freeze typed proof acquisition`。

**Exact next activation changed paths：** `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`、`.agent-work/PLANS/20260801-1454-p7-retained-r3-d2-c1-r1-c1-activation-budget-failure-review.md`。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R1_C1_TYPED_PROJECTION_PROOF_WAITING_PLANNER_REVIEW`。

## 4. Required FULL updates（Orchestrator-owned）

- 将D2-C1-R1-C1状态改为`REJECTED_ACTIVATION_GOVERNANCE_ACQUISITION_BUDGET_VIOLATION_NO_TYPED_PROOF_CREDIT`并记录evidence commit `231eeb13d3171c198e4fb0ac18efc3ea4566e5d4`。
- 保持唯一active task/reference为D2-C1-R1-C1，但将active contract切换到activation-governance corrective V2，并写入上述exact four Git argv/budgets。
- `real_self_check_owner_status`与`real_execution_status`继续blocked on D2-C1-R1-C1 typed projection proof acceptance；不得解锁18-row attribution。
- 保持`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator sole eligibility owner及device authorization false。

维护性判断：successor只收紧一次性controller的Git acquisition boundary并复用既有accepted parser/typed projection合同；不改共享代码或production owner，新增复杂度限于四条可审计argv与严格stdout framing，无后续代码清理建议。
