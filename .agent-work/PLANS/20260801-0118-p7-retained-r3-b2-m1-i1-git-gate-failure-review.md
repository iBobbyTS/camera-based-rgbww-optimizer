# P7 retained-R3 Option B：M1-I1 synthetic integration Git gate failure review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-I1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-FRESH-SYNTHETIC-INTEGRATION-V1`

**Decision：** `REJECTED_CONTROLLER_GIT_COMMAND_DENIED`

**Exact next branch：** `REF-P7-25-R2-B2-M1-I1-C1`；只纠正 M1 generated controller 的
56 个 read-only Git argv，使其使用 P3 已有 canonical grammar，并在 M1 dedicated test 中逐项覆盖全部
56 个 shape。M1-I1 retry、retained validation 与所有 release/device route 继续锁定。

## 1. Topology 与 evidence integrity

- Activation `2f2899ac769d0ac30662b495dfbdfd06fe508282` 是
  `216946495c455c91d433c4e70b32c14b940428fa` 的 direct child，subject exact
  `chore(plan): activate real manifest synthetic integration`；changed paths exact 为 FULL、PLAN 与
  `.agent-work/PLANS/20260801-0101-p7-retained-r3-b2-m1-s1-canonical-json-acceptance-review.md`。
- Evidence `99bc4ec1710395fc54772343fc650daf7d29e7d4` 是 activation direct child，subject exact
  `chore(evidence): record real manifest synthetic Git gate stop`；changed path exact
  `.agent-work/EXECUTION_RESULT.md`，只新增一次 15 行 EOF append。
- ER after blob/bytes/SHA-256 exact：`036687214bf3fc59ce554d80f5907d806423b5ce` / `1214715` /
  `8df21eca2e480ff59fc14e169c16fe78bfe78101e7bec0feffc473a780ea159e`。Repository HEAD clean，
  implementation commit count为0。
- Fresh source、seven input roots/files及其path/device/inode/mode/bytes/SHA均已冻结在ER；output root不存在。
  它们是immutable failure evidence，本review未读取其物理内容，后继不得读取、复用、修改、删除、清理或重试。

## 2. Failure 与实际预算

Activation/accepted M1/P5 owner gate及fresh nine-target absence gate通过。P3创建 seven 0700 roots并各写一个
0600 canonical JSON direct child；M1 builder exact1，P5 runtime exact1，source create exact1，controller process
exact1。Controller在activation phase的第一条
`run_read_only_git(REPO_ROOT, ("git", "show", "-s", "--format=%H", GIT_TARGETS[0]))`
被P3 `_validate_git_argv`以`ProvenanceIOError("git_command_denied")`拒绝，process exit1，Git attempts/successes
`1/0`。Controller未进入output root、inputs、evaluate、terminal、seal或admission。

实际counts与ER一致：outer1、integration1、builder1、runtime1、controller1、source1、input root/write `7/7`、
output root/write `0/0`、retry/fallback `0/0`。Tests、compileall、CodeGraph、真实C1/retained、canonical validator、
eligibility、release、network、device与science route全部0。

## 3. Single-owner root cause

M1 `_GIT_LINES`生成exact56条同一家族argv：
`("git", "show", "-s", "--format=%H", GIT_TARGETS[index % 7])`。P3只接受五类冻结read-only grammar；其中
exact show grammar是：
`("git", "show", "-s", "--format=%H%x00%P%x00%s", SHA40)`。

Planner独立只读检查确认M1 seven targets是40位lowercase Git object IDs，56条按0..6循环exact8次；P3 accepted
show grammar对commit与blob object均read-only且返回成功。故唯一owner correction是在M1 generated command中把
format token改为P3 exact canonical show token。不得编辑P3、增加generic allowlist、增加第二Git runner、把validator
放宽为任意`git show`，或为failure root加入repair/reuse路径。

既有M1 test10只统计`run_read_only_git`与`.exit_code`各56次；test13的fake runner忽略argv，因此未证明56个shape
均会通过P3 grammar。后继应在同一dedicated test中逐项验证56条argv的exact family、target cycling和P3 owner acceptance，
而非只验证首条。

## 4. Decision 与 next branch

本次M1-I1不合格，也不证明real retained input、canonical eligibility或release。Accepted M1 owner
`c480c406...`仅保留为correction baseline；现状不得再次用于synthetic integration，直到后继 code/test correction被
Planner接受并由新的fresh activation另行规划。

后继只允许改：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`；
2. `tests/test_p7_retained_r3_real_manifest_domain_template.py`。

验证必须覆盖targeted13、focused83、compileall、full800、post-test maintenance-only `codegraph sync` no query、
exact two-path commit及postcommit targeted13。Executer只append ER一次并停Planner门。Fresh failure evidence、P3/P4/P5/P7、
PLAN/FULL/archive/debug、external paths/controller、retained/validator/release/network/device/formal全部保持只读或0。

该问题是工程command-contract seam，不需要Advisor scientific decision或Human危险设备授权。

维护性判断：修复留在M1唯一generated-command owner与其dedicated test；P3继续是唯一Git argv eligibility owner，
不新增runner、allowlist、scanner或兼容层。
