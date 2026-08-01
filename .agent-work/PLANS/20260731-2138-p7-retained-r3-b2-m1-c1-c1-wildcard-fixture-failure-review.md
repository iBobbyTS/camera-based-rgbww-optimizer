# P7 retained-R3 Option B：M1-C1-C1 wildcard fixture failure review

**Planner review date：** `2026-07-31`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-C1-EXISTING-ROOT-IDENTITY-COUNT-CLOSURE-V1`

**Decision：**
`REJECTED_TARGETED_WILDCARD_NEGATIVE_SOURCE_CONSTRUCTION_FAILURE_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`

**Exact next branch：** `REF-P7-25-R2-B2-M1-C1-C1-C1`；仅纠正dedicated P4 test中的wildcard module-scope
source fixture，随后完整重放冻结验证链并停在Planner review。

## 1. Reviewed topology 与 immutable evidence

- Activation `77c96d6eec4d1881a82a678c84165dff03d6fb6e`是parent
  `c3018460a6748e447894d83cee5cc8c2851bd750`的direct child，subject exact
  `chore(plan): activate existing root identity count closure`；changed paths exact FULL/PLAN/上一archive三项。
- Rejected candidate `40d92acb77b32f370955d687c74c7ff7077f55e1`是activation direct child，actual subject
  `chore(p7): retain rejected existing root candidate`，changed paths exact下列四项；它不是active PLAN原冻结的implementation subject，因此除本次明确分类外也不能被误当成已验收implementation：
  - `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`；
  - `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`；
  - `tests/test_p7_retained_r3_controller_conformance.py`；
  - `tests/test_p7_retained_r3_provenance_io.py`。
- Candidate canonical binary patch SHA-256为
  `00eb408bb3fe4440a5589dacd9799247577ccd0c6dbc891c6ff693c5e9e5f683`；tree
  `f8ff6be0b0436947eb2eaae26914b55313ce442b`。
- Evidence `ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f`是candidate direct child，subject exact
  `chore(evidence): record existing root wildcard test failure`，changed path exact仅
  `.agent-work/EXECUTION_RESULT.md`。ER blob从`fc9e97fb076dbe013640833e85dbbcb00edeb20b`变为
  `22afac8a93932aed3241f38c0623452b12972bd8`；bytes/SHA-256从
  `1157555`/`923c2051617e7a744b62764b10a6259cb07ba3954760ea9e79813d4bdb85db6a`变为
  `1163313`/`24c93dca54ab0235f7c1b85fb89a084a59ccfcc03b2ed237b9ae7e697c3e7189`。
- Evidence commit没有改变candidate四路径；当前HEAD `ec782ab...` worktree clean。四路径当前blob分别为
  `07f89d15c8288e0d45c495d6d5737bc37427b769`、`d6d6cc628861baf8a95a09f13fa9204989693b5b`、
  `429ab49802f50e1e3743dffd09c7f72345a2c271`、`e7bd034d46fda2d24b1fc431e1bfc75f3f570f83`。

## 2. Validation quality 与 first failure

- Activation、required FULL subset、strict machine JSON、clean porcelain、pre-edit CodeGraph sync/query与source-backed
  method inventory `24/20/6/11`均通过。
- Candidate加入P3 public `read_existing_root`及P4 exact import/direct-call effect owner；新增methods exact P3 `4`、P4
  `5`，实际inventory `28/25/6/11`，targeted总数`53`。
- 唯一fresh targeted invocation exit `1`，exact `Ran 53 tests`；`52` pass、`1` failure、retry/fallback `0/0`。
- 唯一failure位于
  `test_23_existing_root_import_and_call_provenance_near_misses_rejected`的`wildcard` subtest：expected
  `existing_root_owner_import_invalid`，actual `source_parse_failed`。
- 独立source review确认根因：shared `runtime(body)`把`body`每行缩进到`def controller()`内；wildcard case因此把
  `from ... import *`放进function body。Python语法在P4 `_validate_existing_root_owner`执行前拒绝该source，故该case没有验证预期的
  wildcard import classifier。P4 classifier或stable expected error本身没有被该失败反证。
- 按PLAN immediate-stop执行：focused、compileall、full、post-edit CodeGraph、diff-check、implementation commit、postcommit targeted均为
  `0`。因此`52/53`不能证明four-path candidate可消费，也不能证明整个P3/P4 owner package完成。

## 3. Planner findings 与 acceptance boundary

1. 执行正确fail closed且没有retry；failure不是生产owner的新科学或架构问题，而是专用negative fixture source-domain错误。
2. 不能把wildcard expected code改为`source_parse_failed`，否则会弱化“P4 classifier主动识别wildcard owner import”的合同。
3. 不能修改P4 classifier来接受function-scope wildcard；Python本身不允许该source shape，修生产代码会把夹具错误扩散到owner边界。
4. 最小correction只需在现有test23内把wildcard specimen构造成UTF-8、Python可解析、module-scope
   `from ... import *`，其controller call仍位于function body；其他case、expected codes、生产source、P3 test与method inventory保持不变。
5. Candidate `40d92ac...`及evidence `ec782ab...`必须原样保留，不amend/rebase/regenerate；successor correction应以新的activation为parent，
   exact one test path、single commit。只有完整53/70/compileall/787、post-edit CodeGraph与postcommit53均通过并经独立Planner接受后，
   才能接受“candidate + fixture correction”的组合；测试修复本身不是验收。

## 4. Residual risks 与 hard locks

- 其余52个targeted methods只有单次运行的通过证据；focused/full与post-edit CodeGraph尚未执行，候选仍可能暴露独立失败。
- 新fixture必须显式证明module body首个相关node是wildcard `ast.ImportFrom`，不能使用regex、generic parser fallback、动态exec/import或修改
  analyzer输入含义。
- P3/P4 production owners、P3 dedicated test、其余P4 methods和assertions、P5/P7、M1 source/test、PLAN/FULL/archive/debug/GUIDE均不在
  successor写范围。
- Accepted C1与retained physical reads、external controller/root/process、Git provenance replay、real M1/B2、manifest/seal、canonical
  validator/callback、eligibility、retained audit/release、network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public
  analyzer/TD-C/sentinel/P8/firmware/deployment继续全部锁定为`0`。
- Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`；下一步无需Human或Advisor，因为它是pure-offline、single-test-fixture engineering
  correction，不命中高危设备授权或科学分支。

## 5. Next package acceptance outline

- Activation parent必须是当前evidence HEAD `ec782ab1e17b24e4feecd2b5b18b712ebfe1b55f`；subject exact
  `chore(plan): activate existing root wildcard fixture correction`；changed paths exact FULL/PLAN/本archive。
- Executer只可修改`tests/test_p7_retained_r3_controller_conformance.py`，保持method count `25`，只改变test23 wildcard fixture及其直接
  module-scope shape assertion；implementation subject exact `fix(p7): correct existing root wildcard fixture`。
- Candidate/evidence topology、four-path candidate blobs与three untouched candidate paths必须在edit前后冻结；rejected commits保持
  non-consumable。
- Fresh ordered validation：targeted `53/53`、focused `70/70`、compileall exit0、full `787/787`、post-edit CodeGraph sync/query exact
  `1/1`、diff-check、exact one-path commit、postcommit targeted `53/53`；retry/fallback `0/0`。
- 无论成功或失败，single ER EOF append后停在
  `B2_M1_C1_C1_C1_WILDCARD_FIXTURE_CORRECTION_WAITING_PLANNER_REVIEW`。

维护性判断：失败局限于一个negative fixture的source构造域；把wildcard import保持在module scope并保留controller call于function scope，是不新增
helper/framework、不改变生产owner、也不弱化stable classifier contract的最小修正。
