# P7 retained-R3 Option B：D1 Git acquisition attribution diagnostic 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-GIT-ACQUISITION-ATTRIBUTION-DIAGNOSTIC-V1`

**Activation：** `8867f152fd81e842431cd8c087bb18510d809d90`

**Evidence：** `519d15bf2334e60774b14568cf379a055847f681`

**Planner 决定：** `ACCEPTED_COMPLETE_ORDERED_8_ROW_GIT_TRANSPORT_ATTRIBUTION_ONLY`

## 1. Reviewed scope、topology 与 immutable boundary

Planner完整读取AGENTS、project skill、committed PLAN、FULL roadmap与machine state、被归档PLAN及ER physical EOF handoff，并只读核验本轮exact fresh diagnostic source/root。未读取任何旧failed/synthetic source/root、被reviewed失败real-self-check root、14个physical inputs或retained R3 payload；未调用owner、tests、validator、release、network或device。

Activation `8867f152fd81e842431cd8c087bb18510d809d90`是`c7792cbc7cfe9730b295885bead9e5f726f6136d`的direct child，subject exact `chore(plan): diagnose real self-check Git stdout`，changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1340-p7-retained-r3-r2-r1-c2-s1-c1-r1-git-stdout-review.md`。Evidence `519d15bf2334e60774b14568cf379a055847f681`是activation direct child，subject exact `chore(evidence): record Git stdout attribution diagnostic`，changed path exact `.agent-work/EXECUTION_RESULT.md`。Review时HEAD为evidence且worktree clean。

ER最后完整level-2 section为`2026-08-01 P7 retained-R3 Option B R2-R1-C2-S1-C1-R1-D1 Git acquisition attribution diagnostic physical EOF handoff`；从heading至physical EOF bytes `11042`、SHA-256 `11d58f6f4edfd23d5382da3915e46085acc5ad845849c3094c6e33fa9f86bc1`，closing fence后exact LF结束。

## 2. Exact six evidence 与 seal closure

Fresh source为`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-git-acquisition-attribution-r1-d1-8867f152fd81-source.py`，mode `0600`，bytes `14880`，SHA-256 `ae9ded3f429c9d69015f90505b6a4852d8737af6a55e914c457a1987db4aa4a6`，terminal记录pre/post identity相同。Fresh root为同basename去除`-source.py`，mode `0700`；inventory exact six且每件mode `0600`：

- contract payload `2092` / `d868a3b7389ad335832de227a0cf1814d48d0ffa22b77f38afc211382a4208a6`；seal `177` / `b0ed1146e6df601e557a2920c4cb563f5c628d302cca303a12278f5a8a7618cd`；
- attribution payload `7982` / `15f24d0e08d0cda3c0a0b5ecaf62935ebcb83349f3d13cc79ef17b83e9c45588`；seal `186` / `0fb9c5a96ee20822e69fe770049d893d4969734d9f100c47b81afb779670b897`；
- terminal payload `1773` / `12f99c59e6557618b638082d63e13d9a1dc09d7dbbdc3b17a36e1a81e4985da5`；seal `175` / `75e673f82076b6a657387efa15c261a0b0d511b9012b1b76881d759ac63c049c`。

Planner独立以duplicate-key/nonfinite fail-closed loader及exact canonical re-encode核验六件套，`6/6 PASS`；三份seal的target、bytes与SHA-256逐字绑定对应payload。Contract绑定activation、archive、PLAN/FULL parser evidence及source initial identity；terminal绑定contract/report及两份seal、source post identity、row count与actual counters。

## 3. Ordered 8-row attribution acceptance

Attribution report保留index `1..8`及四组重复事实，不缓存、不去重、不set-collapse。每行cwd exact `/Users/ibobby/Projects/WLED-RGBWW`，argv与PLAN冻结literal相同；actual exit `0`、stderr bytes `0`及empty SHA均与expected一致，stdout bytes、SHA-256和blob OID也逐字段一致。四种file identity分别为：

- repair parent helper：`36640` / `82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a` / `57aded4a77219d1966bb4303331ec1e4a29f2e1c`；
- repair child helper：`42164` / `48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8` / `b3daada521d3eec98ac0ac8382a8846546aaf780`；
- repair parent test：`24715` / `e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900` / `f55cb67be8e4a9dcee3e5e3208c8b946eb38f247`；
- repair child test：`30841` / `c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f` / `c1ec87913783cba4cc4322729d2222986953b1f0`。

Terminal status exact `sealed_git_acquisition_attribution_all_match`，`all_match=true`，authority仅`diagnostic_only`，eligibility与release consumable均false；Git attempts/processes `8/8`，owner calls、retry、fallback为`0`。全部21个terminal zero locks独立核验为0，包括physical input、self-check owner、repository code/test、tests、validator、eligibility、release、network与device。

因此D1只获得ordered 8-row controller Git transport attribution信用；它没有运行或通过real self-check，也没有证明owner内部18-row expectation正确。

## 4. Residual risk 与 exact next branch

上一real self-check在owner内部以`git_stdout_mismatch`停止且未封存owner ledger，因此D1的8个file acquisition全match仍无法定位18-row中哪个owner expectation与actual Git stdout不一致。被reviewed失败root继续immutable no-read/no-stat/no-list/no-search/no-reuse；不得重试该root或real self-check owner。

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2`。它使用accepted repository owner的bounded `_expected_stdout` selector path与synthetic/injected spec，仅诊断exact 18 rows：逐行冻结argv、repo path、owner expected kind/selection source及actual Git input attribution，继续到完整matrix并seal。不得调用`run_real_manifest_self_check`、读取14个physical inputs/任何failed root、调用validator/release/device或修改production/test。

若row 7或其他row mismatch，下一Planner只可基于首个及完整mismatch matrix决定bounded provenance correction；D2本身不得修复、重试owner或授予manifest/eligibility/release信用。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_OWNER_EXPECTATION_ATTRIBUTION_WAITING_PLANNER_REVIEW`。

维护性判断：D1证明controller transport正确；下一包复用既有owner selector并以一次性synthetic/injected evidence隔离expectation来源，不新增production abstraction或第二eligibility owner。
