# P7 retained-R3 Option B：D1-R1 Git object diagnostic 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-D1-R1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-D1-R1-FIXED-BOUNDARY-GIT-OBJECT-DIAGNOSTIC-V1`

**Planner 决定：** `ACCEPTED_COMPLETE_ROLLBACK_CHECKPOINT_NOT_FILE_OWNER`

## 1. Review boundary 与 topology

- review depth：`Medium`；范围为activation `af6301577d38945a75a98a3b2da880168edaf320`、evidence `febdb9d1d9a13edc1f3a1af8cc4b56670fdf7d38`、committed PLAN、fresh D1-R1 root/source及其六个canonical artifacts。未读取R4 preparation、manifest、C1或retained artifact内容，未调用real self-check owner、canonical validator、eligibility或release。
- activation是`21cd061b39bcaeb7676ffe9152bab84517580efd` direct child，subject exact `chore(plan): retry real manifest Git object diagnostic`，changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1110-p7-retained-r3-b3-c3-c4-r5-r1-c1-d1-precontract-review.md`。
- evidence是activation direct child，subject exact `chore(evidence): record fixed-boundary Git object diagnostic`，changed path exact`.agent-work/EXECUTION_RESULT.md`。

## 2. Independent physical evidence review

- fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-git-object-diagnostic-r5-r1-c1-d1-r1-af6301577d38` mode `0700`，inventory exact6；六件artifact均mode `0600`、strict JSON、target seal的bytes/hash与实际target一致。
- contract bytes/SHA-256 `2197` / `41755e729d198ee890988c8b756453f4aa1a4779bf0817728082e464988e9acd`；report `5329` / `fa4ab64ebb256aa67f1d5e0809dee14db3125c0376379e97bb7d9f808440b653`；terminal `164` / `316aeba9b62f67019b0e8275ac3112d4e8f1d59f1ff3535cfe79dca1e7ece432`。三个seal文件自身SHA-256分别为`3923200a7ad1be342bd792fd2ccc876df9afedca2d4c75a734e2ba9373855770`、`873594f453c8ae4f6e9cd4433af7cb10154ca587ed99c1b1df607f68882903ca`、`9dcc22c3d86750d945831683cc6dd5e258b23b78a0dc244ad830a687a0158acc`。
- exact10 Git argv均exit `0`、stderr bytes `0`且empty SHA；三commit均存在且是commit。rollback tree有287 entries且两个exact audit paths都不存在；repair parent tree有289 entries并持有source/test before blobs `57aded4a77219d1966bb4303331ec1e4a29f2e1c` / `f55cb67be8e4a9dcee3e5e3208c8b946eb38f247`；repair child tree有460 entries并持有after blobs `b3daada521d3eec98ac0ac8382a8846546aaf780` / `c1ec87913783cba4cc4322729d2222986953b1f0`。
- 四次blob stdout bytes/SHA分别为`36640/82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a`、`42164/48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8`、`24715/e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900`、`30841/c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f`，与冻结OID/content SHA完全一致。
- terminal status `PASS`，classification exact `ROLLBACK_CHECKPOINT_NOT_FILE_OWNER`。package validation与independent assertions先通过；随后仅display formatter因`mappingproxy is not JSON serializable`报错。没有diagnostic/Git rerun或evidence mutation，且本次review重算的physical identities仍一致，因此该展示层异常不构成package失败。

## 3. Decision 与 owner correction finding

D1-R1诊断接受，Git attribution credit为true；real self-check、manifest facts、canonical eligibility和release consumability credit仍全部false。retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

`REV-R5-R1-C1-D1-R1-001`（Must Fix / Agent-Fixable）：现有subordinate owner把source seam的before commit错误绑定为rollback checkpoint `32b9e67...`，而physical Git事实证明该commit不拥有source或test path。两个seam的exact file owners都应是repair parent `9303aa2...`的before bytes和repair child `3e2ebed...`的after bytes；rollback checkpoint只保留commit existence及rollback provenance，不再作为任一file owner。`_file_map`的expected rows、seam pairs以及`required_real_manifest_git_argv`的两组seam rev-parse/diff commit pairs必须一起修正，并由dedicated tests覆盖rollback path absence、两个path共同的parent/child owner及18-ledger order。

## 4. 唯一下一分支

唯一下一分支为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R1`：先在exact owner/test两路径内完成上述typed semantic correction，跑targeted `12`、focused `53`、full `822`、compileall、CodeGraph和diff checks并创建单一implementation commit；只有这些门全部通过后，才从该implementation commit派生全新source/root，继承accepted fixed-boundary parser、JSON-native/P3 failure lifecycle、R4 preparation、manifest `5`、C1 `4`、retained `3` physical reads，执行corrected exact8 in-memory Git acquisitions、required argv check1、owner1/18 ordered ledgers及sealed report/terminal。

旧payload不得修复/regenerate，任何旧source/root不得复用。canonical validator、eligibility、release、network与全部device surface保持0；本分支不需要Advisor科学决策或Human设备授权。

维护性判断：修复位于既有subordinate self-check单一owner及其dedicated test，消除错误commit角色而不新增owner、filesystem/process authority或eligibility路径。
