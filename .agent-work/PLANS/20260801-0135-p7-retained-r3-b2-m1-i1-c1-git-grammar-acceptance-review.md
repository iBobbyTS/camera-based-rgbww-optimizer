# P7 retained-R3 Option B：M1-I1-C1 Git grammar correction acceptance review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-I1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-C1-GIT-GRAMMAR-CORRECTION-V1`

**Decision：** `ACCEPTED_COMPLETE_GIT_GRAMMAR_CORRECTION_WITH_PLANNER_PATCH_IDENTITY_SUPERSESSION`

**Exact next branch：** `REF-P7-25-R2-B2-M1-I1-S1`；只运行一个由新 activation full SHA 派生、
pure-offline、retry/fallback 0 的 fresh synthetic integration。旧 M1-I1 failure source/root 全部继续 immutable
no-read/no-reuse/no-modify/no-delete/no-retry；M1-R1、真实 retained、validator、release 与设备路线仍锁定。

## 1. Commit 与 evidence topology

- Activation `f2b38c530a6cbac5c29d761036eb3cd2a159f3b9` 是
  `99bc4ec1710395fc54772343fc650daf7d29e7d4` 的 direct child，subject exact
  `chore(plan): activate real manifest Git grammar correction`；changed paths exact 为 FULL、PLAN 与
  `.agent-work/PLANS/20260801-0118-p7-retained-r3-b2-m1-i1-git-gate-failure-review.md`。
- Candidate `0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8` 是 activation direct child，subject exact
  `fix(p7): align real manifest Git ledgers`，tree
  `26e10d77bd3d89ca80d6bdbef3561b3bce2a4f07`；changed paths exact：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` 与
  `tests/test_p7_retained_r3_real_manifest_domain_template.py`。
- Evidence `7d35542b4b3b24081f6652a5c4f9c15879d03055` 是 candidate direct child，subject exact
  `chore(evidence): record real manifest Git grammar validation`，changed path exact ER。ER old prefix blob/bytes/SHA
  `036687230e3a4d3e9ff5311748371261c12c1912` / `1214715` /
  `8df21eca2e480ff59fc14e169c16fe78bfe78101e7bec0feffc473a780ea159e`；本轮 EOF delta exact `16` lines。
  Final ER blob/bytes/SHA为 `d8f601d28c8da4885accc1ff15a40252ae675049` / `1219677` /
  `d481d69398dee667b77563b8c4aa086db8d3b297a666d54361749902fdfa9a37`。

## 2. Exact diff 与 authoritative patch finding

Candidate diff仅完成计划内三类变化：M1 `_GIT_LINES`的单一format token由`--format=%H`改为P3既有
`--format=%H%x00%P%x00%s`；更新由该token变化导致的template golden；在既有test10/test13补齐全部56条argv
shape、0..6循环8次、public P3 owner eligibility与ledger assertions。P3/P4/P5/P7均未改；无第三路径、generic
allowlist、第二runner、retry、fallback、normalizer、private validator复制或新增test method。

Planner以仓库历史同类记录使用的binary-safe口径独立重算：

`git diff --binary f2b38c530a6cbac5c29d761036eb3cd2a159f3b9 0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8 -- src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py tests/test_p7_retained_r3_real_manifest_domain_template.py`

输出 exact `5874` bytes，SHA-256
`6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca`。以candidate first parent、
`git show --binary --format=`及`git diff-tree -p --binary --no-commit-id`重算也得到同一bytes/hash。因此ER所写
`4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5`不是命令/范围变体，属于单字段evidence
mismatch，不可继续作为canonical patch identity。

该mismatch不改变Git对象中的exact two-path diff、final blobs、代码行为或测试结果；Planner现以独立可重放的上述命令、
bytes与hash supersede ER该单字段，并将`6b26e493...a5ca`作为后继唯一authoritative M1 patch identity。ER其余字段继续
authoritative；不得修改或追加旧ER来“修复”该字段。

## 3. Final owners 与 regression surface

- Final M1 module blob/bytes/SHA：`c0238fba753fc7608df1c352f336199fb6ebc105` / `23737` /
  `350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e`；template golden exact
  `a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6`。
- Final dedicated-test blob/bytes/SHA：`ef8273e14853446c31b47f1f093a18bac43c6f64` / `22897` /
  `0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c`。
- Existing test method inventory保持exact13。Test10逐条解析56个generated calls并验证exact five-item argv、P3 format
  token与target index；test13记录56个actual argv，通过public `run_read_only_git`配合in-memory completed result，逐条
  断言target cycle、ledger argv、exit0与stderr empty。没有直接调用private validator，也未启动真实Git subprocess。
- Ordered validation record闭合：targeted `13/13 OK`、focused `83/83 OK`、compileall exit0、full discovery
  `800/800 OK`、postcommit targeted `13/13 OK`；test invocations4、compileall1、retry/fallback0。仅在precommit四项全绿后
  maintenance `codegraph sync` exact1/exit0，query0；`git diff --check`通过。

## 4. Locks、decision 与 successor

Correction没有读取、stat、list、glob、search、复用、修改、删除旧 M1-I1 fresh failure evidence；synthetic integration、
controller、external roots、真实C1/retained、Git provenance replay、canonical validator/callback/eligibility、retained audit、
release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/
firmware/deployment全部exact0。故本工程correction无需Advisor scientific decision或Human危险设备授权。

Planner接受candidate作为新的M1 generated-command owner，但它仍不具有retained eligibility或release consumability。后继必须使用
全新activation-derived source/output/seven synthetic input roots，先做exact absence gate，再组合accepted M1 builder与P5 runtime
各一次。旧failure paths绝不读取或复用。Success label只能是
`FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`；pass/fail均只append ER一次并停Planner门，不得自动进入
M1-R1。

维护性判断：M1仍是唯一generated-command owner，P3仍是唯一read-only Git eligibility owner；本次接受不新增owner、runner、
allowlist或兼容层。唯一证据偏差已由Planner以可重放Git-object命令显式supersede，无需改代码或重写历史ER。
