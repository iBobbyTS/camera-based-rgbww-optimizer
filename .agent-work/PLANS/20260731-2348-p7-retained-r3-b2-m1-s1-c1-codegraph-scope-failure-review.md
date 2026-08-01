# P7 retained-R3 Option B：M1-S1-C1 pre-edit CodeGraph scope failure review archive

**归档状态：** `REJECTED_PRE_EDIT_CODEGRAPH_SEMANTIC_SCOPE_MISMATCH`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-DEDICATED-FIXTURE-CORRECTION-V1`

**Reviewed activation：** `0895921fc0a4d959b8d06ad218f70340e341197a`

**Evidence HEAD：** `850537007233a1517962afbef26e8e40e4782ad2`

## 1. Reviewed scope and immutable topology

Planner只读审核active PLAN、`.agent-work/EXECUTION_RESULT.md`、activation/evidence commits及上一份targeted-failure archive；未重跑
CodeGraph、tests、compileall，也未读取retained R3、candidate physical inputs或external roots。

Activation `0895921fc0a4d959b8d06ad218f70340e341197a`是
`5567837b1bbe3fdd368f0c8cbddd21c19a436e40`的direct child，subject exact
`chore(plan): activate real manifest fixture correction`，changed paths exact为FULL、PLAN与
`.agent-work/PLANS/20260731-2337-p7-retained-r3-b2-m1-s1-targeted-failure-review.md`。该archive bytes `24194`、
SHA-256 `f0da8a83f4694aa04fb846495e26dcc895136cdc1851e027fbc5b83d15bdd38e`。

Evidence commit `850537007233a1517962afbef26e8e40e4782ad2`是activation direct child，subject exact
`chore(evidence): record real manifest CodeGraph scope stop`，只修改`.agent-work/EXECUTION_RESULT.md`。Activation与evidence之间没有
code/test commit。

Rejected M1-S1 candidate保持：

- candidate `cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf`；parent
  `84b3458765849f9c50515067788af365006cef68`；tree
  `ff424f29e6a7a95349500ce356669a754d9ffa14`；
- changed paths exact为
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`与
  `tests/test_p7_retained_r3_real_manifest_domain_template.py`；
- production blob/bytes/SHA-256 = `84fcd755225af39eb89459146de282392367b70b` / `23352` /
  `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d`；
- dedicated test blob/bytes/SHA-256 = `05db407f9fd6c67bf359f1874cff2f9baaf9564f` / `17413` /
  `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af`；
- candidate仍为`consumable=false`。

## 2. Validation quality and first failure

Activation/topology/FULL-PLAN machine gates通过。Pre-edit `codegraph sync`恰好一次，exit `0`，输出`Already up to date`。随后唯一允许的
`codegraph explore` query也exit `0`，但报告`Found 21 symbols across 1 file`，只返回旧文件
`tests/test_p7_retained_r3_controller_domain_template.py`。

该输出没有实际回显以下PLAN所需语义面：

1. 新production module
   `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`及
   `build_real_manifest_domain_template`；
2. 新dedicated test中的
   `test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes`和
   `test_13_generated_compile_fake_success_failure_and_negative_authority_surface`；
3. P3 existing-root/canonical-I/O owner symbols；
4. P4 static provenance/root-chain/lifecycle owner symbols；
5. P5 runtime request/composition/execution owner symbols。

因此该query无法建立“两个targeted失败仅来自test fixture/assertion”的source-backed结论，也无法排除production finding。PLAN规定的
`query_before_test_read_or_edit`语义门没有满足；即使进程exit `0`也不能升级为合格CodeGraph evidence。

Executer正确以first failure `pre_edit_codegraph_semantic_scope_mismatch` fail closed。Dedicated test read/edit `0/0`；production/test writes `0`；
targeted/focused/full/postcommit tests `0/0/0/0`；compileall `0`；post-edit CodeGraph `0/0`；stage/commit `0/0`；retry/fallback `0/0`。
ER只做一次EOF append。全部retained/validator/release/network/device/science locks保持`0`。

## 3. Planner decision

Decision：`REJECTED_PRE_EDIT_CODEGRAPH_SEMANTIC_SCOPE_MISMATCH`。

拒绝原因只在execution-package query contract，而不是production或test语义。旧单个自然语言query的路由结果不可预测，实际命中同名旧test文件；继续读取或编辑
dedicated test会违反pre-edit evidence gate。不得复用activation `0895921...`，不得把exit0当作semantic coverage。

M1-S1原targeted findings仍保持原判：

- test07 collision fixture必须从第一条完整identity出发，只替换为第二条expected label，使path/root/device/inode/mode保持自洽后expect
  `path_collision`；
- test13必须使用AST exact import/module/alias/callable-token authority assertion，不能对完整source做裸substring scan；合法package
  `camera_based_rgbww_optimizer`不得因包含字符序列`camera`而失败。

本次没有新production finding，因此上述one-path、two-method语义纠偏不得扩大、弱化或改写。

## 4. Exact successor branch

Exact next branch：`REF-P7-25-R2-B2-M1-S1-C1-C1`。

Contract：
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-CODEGRAPH-SCOPE-CORRECTION-V1`。

Fresh successor只修正pre/post-edit CodeGraph证据合同：每轮先exact一次sync，再执行5个固定、逐文件、逐symbol query；每个query必须exit0并实际回显
指定文件路径和每个指定symbol。Pre-edit必须达到query group `5/5`且required path/symbol coverage `24/24`，否则test read/edit/tests/commit均0并停止。
Post-edit使用相同5组query，仍须`5/5`与`24/24`。

五组固定surface为：

1. M1 production：`RealManifestDomainTemplateSpec`、`RealManifestDomainTemplateBundle`、
   `build_real_manifest_domain_template`；
2. M1 dedicated test：class `RealManifestDomainTemplateTests`及exact test07/test13；
3. P3：`read_existing_root`、`canonical_json_bytes`、`create_exclusive_root`、
   `persist_canonical_json`、`read_exact_file`、`run_read_only_git`；
4. P4：`analyze_controller_source`、`_validate_existing_root_owner`、
   `validate_root_identity_chain`、`execute_controller_lifecycle`；
5. P5：`ControllerRuntimeRequest`、`compose_controller_source`、`execute_controller_runtime`。

Coverage计数`24`按3+3+6+4+3 = 19个symbols，加5个对应文件路径分别计数。Query output可以包含CodeGraph为call path返回的额外相关source，但不得用相邻文件、
同名旧test或summary推断替代任一required path/symbol的实际文本回显。不得在missing/stale/wrong-route时补发第6个query、fallback到grep/raw read、修改query后重试，
或继续执行。

通过pre-edit gate后，唯一允许write path仍是
`tests/test_p7_retained_r3_real_manifest_domain_template.py`，且只允许原test07/test13 semantic correction。验证链仍为targeted13、focused83、
compileall、full800、post-edit CodeGraph 5/5 + coverage24/24、exact one-path commit、postcommit targeted13；tests exact4、compileall1、CodeGraph
sync2/query10、retry/fallback0。M1-I1、retained、validator、release、network、device及scientific routes继续hard locked。

## 5. Residual risk and maintainability

Residual risk：修正后的test07/test13仍可能在targeted阶段揭示真实production defect；此时按原fail-fast branch保留one-path diff、不得同包第二次纠偏。另一个风险是
CodeGraph对精确file+symbol请求仍可能不给完整verbatim source；新合同将其变成可判定的missing-coverage failure，而不是允许模糊推断。

维护性判断：本次只调整execution evidence query的确定性，不改变production owner、test semantics或模块结构；5个窄query按现有P3/P4/P5职责分组，避免新增
generic scanner或平行authority owner，无需重构。
