# P7 retained-R3 Option B：M1-I1-S1 fresh synthetic integration acceptance review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-I1-S1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-S1-FRESH-SYNTHETIC-INTEGRATION-SUCCESSOR-V1`

**Reviewed PLAN identity：** bytes `17932`，SHA-256
`4891aa7bf9470caab8a3dc6c560d1595d99d658a10d705b06509a3c64f75bf50`。

**Decision：**
`ACCEPTED_COMPLETE_FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。

**Exact next branch：** `REF-P7-25-R2-B2-M1-R1`；只执行一个由新 activation full SHA 派生、
pure-offline、retry/fallback 0 的 fresh real-input manifest-only package。该包首次允许读取 accepted C1
四件套及其机械绑定的 original retained R3 三件套；canonical validator、eligibility、release、network 与
device 路线继续锁定。

## 1. Commit 与 evidence topology

- Activation `f925a2885ee2e282ece2e230cf752658ced2d273` 是
  `7d35542b4b3b24081f6652a5c4f9c15879d03055` 的 direct child，subject exact
  `chore(plan): activate fresh real manifest synthetic integration`，changed paths exact 为 FULL、PLAN 与
  `.agent-work/PLANS/20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md`。
- Evidence `0a7f718a8d49eb33974ce5f22f85dd8a00ea1110` 是 activation direct child，subject exact
  `chore(evidence): record fresh real manifest synthetic integration`，changed path exact
  `.agent-work/EXECUTION_RESULT.md`。
- Evidence commit 中 ER blob `d05873801a57e31a935076564cd9f54844482988`，bytes `1228395`，SHA-256
  `d4eaf1cad5174e2e0c0d64b0b2846ca59ca42e6a53960c11aa723aa3dac69e97`。其 parent ER prefix bytes/SHA-256
  exact `1219677` / `d481d69398dee667b77563b8c4aa086db8d3b297a666d54361749902fdfa9a37`，当前 ER
  byte-for-byte 以前者开头，single EOF delta `8718` bytes。
- Activation 所绑定 prior review archive bytes/SHA-256 exact `6186` /
  `d3a01adebc667447031ff1bb55f7f055c696fa74ce796d4f79f4728df2ad5764`；PLAN/FULL各只有一个 strict
  machine row，active task/contract一致。

Planner只读取 repository Git objects、PLAN/FULL/ER、accepted owner source与review archives；没有读取、stat、
list、glob或搜索本轮fresh external root、旧failure root、accepted C1 root或retained R3 root，没有重跑controller、
tests、CodeGraph、network或device operation。

## 2. Accepted owner 与 patch supersession

- M1 owner commit `0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8`、parent
  `f2b38c530a6cbac5c29d761036eb3cd2a159f3b9`、subject
  `fix(p7): align real manifest Git ledgers`、tree `26e10d77bd3d89ca80d6bdbef3561b3bce2a4f07`及exact two paths
  全部匹配。
- M1 source blob/bytes/SHA-256 exact `c0238fba753fc7608df1c352f336199fb6ebc105` / `23737` /
  `350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e`；dedicated test exact
  `ef8273e14853446c31b47f1f093a18bac43c6f64` / `22897` /
  `0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c`。
- Planner以冻结的 ordinary exact two-path `git diff --binary` 口径重算 M1 patch，再次得到 bytes/SHA-256
  exact `5874` / `6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca`。
  历史 ER 的 `4044c624...94c5`继续是non-authoritative superseded evidence mismatch，不被解释、修复或使用。
- P5 runtime owner commit `37f7d0021c7a81a9d6680815bc51c305cf807a7b` 的 source blob/bytes/SHA-256
  exact `075face6fd7453236affa303640b91eb16a42a9b` / `12320` /
  `07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2`。

## 3. Fresh integration acceptance

- Fresh namespace仅由 activation short SHA `f925a2885ee2`派生；source、output、seven inputs 的 non-following
  absence gate `9/9`，alternate/reuse/retry/fallback `0`。旧 M1-I1 failure evidence保持
  `IMMUTABLE_NO_READ_NO_REUSE_NO_MODIFY_NO_DELETE_NO_RETRY`。
- P3创建seven 0700 roots与seven exact-label canonical 0600 JSON direct children；post-controller audit证明7个
  roots/files/payloads/inodes/modes未变，每root只有exact one direct child。
- Accepted M1 builder、P5 runtime、controller process均exact1；builder产出typed bundle、template SHA-256
  `a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6`、artifact names5、lifecycle8、
  Git family56。Direct source patch、builder override、runtime dependency override、second builder/process均0。
- Controller process exit `0`；stderr bytes0/SHA-256 empty hash；stdout bytes/SHA-256 exact `71` /
  `495d98f75ac38100658f317d531fe4a824b7325671d8e6697dbaec4c01ecebba`，payload exact
  `{"artifact_count":5,"status":"sealed_subordinate_provenance_evidence"}`。Successful run证实 Git ledgers56、
  input reads7、output reload reads5。
- Source保持regular0600 same inode，bytes/SHA-256 `26273` /
  `bed352f8d1a2e9130335ab8b59d0d3c7146a17b93911af01466f0de3659c5cf3`。Output root保持same 0700
  directory，exact five 0600 canonical direct files，无extra/missing/symlink。
- Exact five identities全部冻结；manifest/manifest seal、terminal/terminal seal的target bytes/SHA linkage全部通过。
  Manifest schema/status exact，activation five-item、baseline twelve-item、C1 four rows、retained three rows与spec一致。
  Admission exact `admitted=true, eligibility=false, release_consumable=false`，无validator、production、release或
  device authorization claim。
- Owned exact-argv process scan exact1，residual process0；outer/integration/builder/runtime/controller/source/output budgets
  全部匹配，first failure `null`，retry/fallback0。

## 4. Locks、decision 与 residual risk

Repository code/test writes、tests/compileall/CodeGraph、implementation commit、旧failure evidence access、accepted C1或
retained physical reads、real B2、canonical validator/callback、eligibility emission、retained audit、release generation/
qualification/copy/consumption、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public
analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。

因此本次接受只证明accepted M1/P5/P3 owners可在fresh synthetic physical roots中完成exact sealed subordinate evidence。
它不验证original retained R3，不产生eligibility，也不使release consumable。M1-R1必须用新的activation-derived source/output root，
只读取accepted C1 exact four files和其机械绑定的exact three retained files；任何identity/hash/path/lifecycle mismatch均fail closed，
不得alternate、retry、repair、regenerate或进入B3。

M1-R1是Human-owned local lab中的pure-offline read-only evidence input与new external evidence output操作，不访问或控制设备，
不属于High-Risk Device Authorization；不需要Human授权。它也不改变色彩/测量科学分支，不需要Advisor决定。

## 维护性判断

接受结果继续由P3拥有physical I/O、M1拥有manifest domain、P5拥有runtime lifecycle；没有新增serializer、controller、validator、
allowlist或parallel evidence owner。M1-R1只组合这些accepted owners一次，无需额外重构。
