# REF-P7-25-R2-B2-P6-C1-C1-C1-V1：deterministic validation-only closure review

**Planner 日期：** 2026-07-31

**Reviewed reference：** `REF-P7-25-R2-B2-P6-C1-C1-C1-V1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-V1-DETERMINISTIC-VALIDATION-CLOSURE-V1`

**Planner decision：**
`ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL`。

Candidate `48b3979d6c0df5f488cd500597e26dc4c38877dd` 现在可作为 P6 deterministic
domain-template builder owner 消费；该接受只覆盖其冻结 builder、composition 和 static conformance 合同，不把它
表述为已经通过 fresh synthetic integration，也不使 retained R3 可消费。

## 1. Frozen inputs and topology

- Review evidence HEAD：`74dddff36d02d908934a9b65db018169f9966b8e`，direct parent
  `e8a4d1e26d47ddd106de68b66107271a27d9f548`，subject
  `chore(evidence): record p6 validation closure`，changed path exact
  `.agent-work/EXECUTION_RESULT.md`。
- Activation：`e8a4d1e26d47ddd106de68b66107271a27d9f548`，direct parent
  `2fc509b02fd8be0fee05653e5875709f0d05a141`，subject
  `chore(plan): activate p6 validation harness closure`，changed paths exact FULL、PLAN 和
  `.agent-work/PLANS/20260731-1634-p7-retained-r3-b2-p6-c1-c1-c1-harness-failure-review.md`。
- Reviewed active PLAN SHA-256：
  `9b2158d3fbf0a2aa9362960231b3b23a3ec58daa51fd979c7bfb2c63d6ce288f`。
- Prior archive：bytes `6389`，SHA-256
  `db6545c82e4be051c4536d0cd2e47fcf8f0f6b4f3ff62c5117f59a4ffec3c6ad`。
- Candidate：`48b3979d6c0df5f488cd500597e26dc4c38877dd`，direct parent
  `478d8c52e4a21d6628219e27b88b507d736f3aca`，subject
  `chore(p7): retain rejected p6 c1 c1 c1 guard candidate`，changed path exact dedicated test，
  numstat `2/2`，canonical binary diff SHA-256
  `96a38decb6664fec7f5744f568ddad86b7c206d969452a458ddff854881da781`。
- Source blob `a1e196664840bc340be789829b8cf0826c9ec7f4`，bytes `13918`，SHA-256
  `56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`。
- Test blob `eb943384817996b96e332c83f618ba82cf210d4a`，bytes `12992`，SHA-256
  `6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc`。

## 2. Validation quality

Executer handoff and committed evidence record:

- unique deterministic AST gate：pass；exact-name class/test08 selection，`ast.walk(selected_test08)`，
  exact one literal `generated_calls`，only added names `RuntimeError`、`type`；
- fresh targeted `8/8`，exit `0`，`OK`；
- fresh focused `90/90`，exit `0`，`OK`；
- exact compileall：exit `0`；
- unique full suite session `63344`：`775/775`，exit `0`，`OK`；
- CodeGraph query `1`、sync `0`；
- code/test writes `0`、implementation commit `0`、retry/fallback `0/0`；
- external controller/source/root/process、synthetic integration、old evidence、retained/candidate payload、
  validator、eligibility、release、network、device、camera、Ray、strip、cleanup、FORMAL 和 later stages全部 `0`。

Planner independently rechecked activation/candidate/evidence topology，candidate binary diff、source/test blob/bytes/SHA，
以及 exact test08 AST/import inventory；worktree在 review开始时 clean。Evidence足以关闭此前 validation-harness
`StopIteration`，且没有把旧 green test当作本包 fresh validation。

## 3. Acceptance boundary

P6 的 accepted owner职责为：effect-free spec校验、canonical template bytes、exact replacement bytes、
`ControllerRuntimeRequest` composition，以及 existing analyzer 下的 exact 18 bindings / 14 effects / 4 fixtures /
7 reads static shape。Candidate `48b3979...` 的两名字修正是该 accepted source/test identity的一部分。

本决定不接受 synthetic integration，不读取 retained R3，不运行 canonical validator，不产生 eligibility，不生成或
消费 release，也不授权设备、相机、Ray、strip 或 scientific stage。

## 4. New independent finding and residual risk

在选择下一包时，Planner对 accepted builder的 generated source做了 integration-readiness source review，确认尚有
独立于 P6 acceptance 的 runnable-contract residual：

1. generated source load `REPO_ROOT`、`ACTIVATION_COMMIT`、`RUNTIME_COMMIT`、`RUNTIME_PARENT`、
   `RUNTIME_PATHS`、`OUTPUT_ROOT`，但未从 replacement contract派生这些运行绑定；
2. generated source调用 `persist_canonical_json`，但没有导入该 owner；
3. `phase_conformance`、`phase_activation`、`phase_root`、`phase_inputs`、`phase_evaluate`、
   `phase_terminal`、`phase_terminal_seal`、`phase_admission` 未定义；
4. 没有 `controller()` process entrypoint；
5. root创建后先 read未创建的 four inputs / qualification / terminal / admission，再 persist，顺序不满足
   existing provenance owner的 exclusive-persist/read合同；现有 `persist_canonical_json` 参数也传入 path string而非
   frozen `DirectoryIdentity`。

这些缺口没有否定 P6 frozen builder/static-conformance acceptance，但阻塞真正 fresh synthetic integration。直接签发
external source/root/process会成为已知必败的 disposable effect，因此本 review选择先做一个 repo-owned exact two-path
runnable-contract correction，而不是进入 P5-I1。

## 5. Exact next branch

- Reference：`REF-P7-25-R2-B2-P7`
- Contract：
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-REPO-OWNED-RUNNABLE-DOMAIN-TEMPLATE-CORRECTION-V1`
- Exact paths：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py` 与
  `tests/test_p7_retained_r3_controller_domain_template.py`。
- Scope：pure repo correction only；冻结完整运行绑定、exact owner imports、single guarded controller entrypoint、
  lifecycle callbacks和 persist-before-read/root-bound phase ordering；无 external source/root/process。
- Required validation：targeted `11/11`、focused `93/93`、compileall、unique full `778/778`、CodeGraph
  sync/query、exact two-path implementation commit、postcommit targeted `11/11`。
- Stop：`B2_P7_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_CORRECTION_WAITING_PLANNER_REVIEW`。

维护性判断：接受的 runtime owner与domain-template owner继续保持单一职责；下一包只修现有 template owner及其
dedicated test，不新增第三个 controller framework或平行 lifecycle owner。
