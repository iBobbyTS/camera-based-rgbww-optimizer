# Archive record

- Archive status: `REVIEWED_ACCEPTED_HISTORICAL_NON_EXECUTABLE`
- Timestamp: `2026-08-03T22:09:27-0600`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-RAY-R6` Package A V2 phase-1 handoff and controlled-child phase-2 identity
- Source checkpoint at review: `23a20f0b5e2840c568031aef536803ebe473567b`
- Source bytes: `8230`
- Source SHA-256: `7f87856ed2524fa595af56dcc6180e67e46ec10a523b177a1c20d5023b5dfdfa`
- Terminal disposition: `ACCEPTED_PACKAGE_A_V2_SOURCE_ATTESTED_PRODUCTION_LAUNCH_SEAM`
- Evidence/index: controlled child direct parent `2ed23fea80c900f8d4e9dacb53fcb533fdd03b44`, tree `2f4ef783f69f59a652badde1e88aafbdce80dc2f`, exact subject and three-path set; phase-1 fresh full `953/953` inherited because committed/current semantic bytes are identical.
- Exact next stop: waiting Orchestrator FULL transition and a separate Package B Planner pass; no Package B/formal/device authority is granted here.
- Historical declaration: `historical_non_executable`; this archive authorizes no Package B, device, formal root, release, retry, stage entry, budget, or commit.

## Archived source body

# REF-G4-06-RAY-R6 Package A V2 source-attestation convergence handoff

**Status:** `READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`

**Planner stop:** `RETURN_FOR_G4_06_PACKAGE_A_TWO_PHASE_REVIEW`

本 handoff 只证明 Package-A production CLI seam、future Package-B authority transition及其 committed-source attestation 在 synthetic/offline 环境可达且 fail closed；不宣称 Package A 已接受，不授权 Package B、formal root/device/capture，也不表示 hardware ready、formal/quality/history pass 或 G4-07 unlocked。

## 1. Activation intake

- branch：`main`
- activation HEAD：`2ed23fea80c900f8d4e9dacb53fcb533fdd03b44`
- activation tree：`9272a5869b3d500862b5338a3bc0f5611c062623`
- parent：`34092241057a3b51e8afe7a4ef8cea1178eb080d`
- subject：`docs(plan): align ray r6 attestation subject`
- activation changed paths exact：FULL、PLAN、reviewed ER archive `EXECUTION_RESULT-20260803-2139.md`、reviewed PLAN archive `PLAN-20260803-2139.md`。
- initial dirty exact 为 ER、measure、stage-gate、focused tests；SHA-256 分别为：
  - ER `07d628de839a2140db0e2c8beffca9dbe75e79472d9b3ab431b7737d580ecd45`
  - measure `babca565fafa7492a3fdcc7a498dc7d2be129367fe40118e489b5f0f7e11b02f`
  - stage-gate `deb8073038b5d3126ef7a124195a8d2e1ecd298a1f3e94d6e90cd2b878f21553`
  - tests `040f338f6c3a4991c025f024599489b3decf0230cb34d1e1c7f6188b572433f4`
- PLAN/FULL strict parser：active `1/1`，task `REF-G4-06-RAY-R6`，engineering contract `G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V2`，canonical next 为同一 task。

## 2. Maintainability and ownership

CodeGraph preflight及post-query确认本修订仍只收敛 existing focused stage-gate owner：

- package、machine contract、Git attestation、future activation、runtime SHA/materialization唯一归 `p7_td_b_r6_stage_gate.py`；
- `ALLOWED_CODE_CHILD_SUBJECT` 的唯一生产字面值为 `feat(stage-gate): route ray r6 formal launch owner`；
- measure只保留 retained candidate 的显式 CLI parse 和一次 dispatch，本轮未修改measure，SHA保持冻结；
- narrow hook与real runner保持existing single owner/exact once；
- 未新增module、test module、controller、schema family、parallel serialization或authority owner；
- wrapper、thermal scientific owner、GUIDE/RESEARCH保持只读。

## 3. Authority transition and source attestation

Production validator严格区分：

1. engineering Package A contract：`G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V2`。当前 PLAN/FULL authority 为 false，必须返回 `production_machine_contract_drift`，不得进入 activation/materializer/backend；
2. future formal Package B contract：`G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1`。只有 exact matching live PLAN authority与FULL non-authorizing mirror同时成立才可继续。

Exact Package-B PLAN authority为closed mapping，绑定 TD-B、Ray、TD-B stage、remote backend；formal execution/root/device/camera/Ray/capture=`true`；strip=`false`；exact formal root parent/basename/regex；logical16、physical16、launch1、retry0；release consumption与TD-C=`false`。

FULL继续要求 executable=false、top-level authority=false和exact nested mirror。Machine authority在sealed package validation之后、C/L activation/materializer/backend之前验证；Package A不能生成authorized runtime，Package B exact state才可到达existing materializer与narrow hook。

Committed-source attestation收敛为 exact A→C→L topology：

- C必须是descriptor attestation parent A的direct child；
- C subject exact 为 `feat(stage-gate): route ray r6 formal launch owner`；
- C changed paths exact 为 measure、stage-gate、focused tests；
- descriptor中的三个source reference必须与C committed blob的bytes、SHA-256及mode `100644`逐项一致；
- L必须是C的direct orchestration child，且changed paths全部位于 `.agent-work/`；
- per-commit ledger必须与A→C→L拓扑完全一致。

旧字面值 `feat(stage-gate): accept ray r6 launch owner` 即使复用同一parent和完全相同的code tree，也必须在backend前以 `committed_source_subject_drift` 拒绝。旧descriptor subject语义必须以 `committed_source_descriptor_semantic_drift` 拒绝；descriptor建立后出现later code child时仍以 `source_reference_drift` 拒绝，不会漂移选择新的code owner。

## 4. Meaningful synthetic matrix

- current Package-A V2 exact synthetic machine state：negative，`production_machine_contract_drift`，factory/delegate/root create=`0`；actual live Package-A V2 repo machine state通过read-only direct validator复现相同结果。
- exact synthetic Package-B PLAN+FULL mirror：package → C/L attestation → activation → materializer → narrow hook → injected delegate PASS；factory/delegate each once，fake backend connect=`0`。
- 33个closed authority drift subcase全部pre-backend FAIL，覆盖 authority missing/extra/mismatch、wrong contract/task/count/source/backend/root/bounds，以及FULL自授权、retry/launch/logical/physical/strip/release/TD-C扩张。
- exact subject/topology正向、同tree旧subject负向、旧descriptor和later-child负向、Package A负向、Package B正向及33-case matrix均通过。
- existing inventory/hash/mode/terminal/semantic guard、per-commit C/L、expected runtime、kwargs exact-once、delegate exception no-retry、generic formal bypass与legacy CLI覆盖均保留。

## 5. Exact candidate diff and identities

相对activation HEAD：

- measure：`+72/-1`，`194256` bytes，SHA-256 `babca565fafa7492a3fdcc7a498dc7d2be129367fe40118e489b5f0f7e11b02f`
- stage-gate：`+248/-7`，`77744` bytes，SHA-256 `35dc455ac0b84d88a5bb827585c37aee9bcc3cdc4a551bc13c6779b5567fc500`
- focused tests：`+782/-25`，`93530` bytes，SHA-256 `d461eb1a427e8534096c1bdbd73c490727c917bb9add2becf8166ec6773e620b`
- ER：本handoff，不属于controlled code child。

Measure identity与先前retained candidate一致；本轮只改变stage-gate exact subject owner与focused tests。

## 6. Validation

- exact subject/topology targeted set：`6/6` PASS，`12.999s`。
- full stage-gate suite：`36/36` PASS，`35.226s`。
- focused command：`.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_p7_successor_e2` → `226/226` PASS，`75.445s`。
- `.venv/bin/python -m compileall -q src tests`：PASS。
- `zsh -n tmp/run-p7-thermal-diagnostics.zsh`：PASS。
- repo-owned PLAN/FULL parser与actual Package-A negative probe：PASS。
- stage-gate device/camera control imports：`0`。
- `codegraph sync`：PASS；post-query exit `0`，确认exact subject literal仍由stage-gate单点拥有。
- candidate唯一fresh full：`.venv/bin/python -m unittest discover -s tests` → `953/953` PASS，`192.745s`，exit `0`。
- full之后未修改semantic code，也未重复full；其后只更新本ER并执行只读/doc checks。

## 7. Side-effect and authority counters

- accepted G4-05 real root access=`0`；production/formal root access/create=`0/0`。
- real backend factory/connect=`0/0`；network/device/camera/Ray/strip/capture/nonzero light=`0`。
- activation/materializer calls from current Package-A negative path=`0/0`；backend/delegate=`0/0`。
- synthetic Package-B positive fake factory/delegate each=`1` per path；fake backend connect=`0`。
- invalid authority/source-bound paths factory/delegate/root create均=`0`。
- release/retained R3/old payload/firmware/deployment/TD-C=`0`。
- task suffix/new task/new module/controller/root=`0`。
- stage/commit/push/PR=`0`。

## 8. Phase-1 disposition request

请求Planner做Package-A V2 phase-1 review。若接受，请返回 `READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`，由Orchestrator创建direct child：

- subject exact：`feat(stage-gate): route ray r6 formal launch owner`
- changed paths exact：measure、stage-gate、focused tests
- ER不得进入code child。

随后同一PLAN进入phase-2 read-only review。Package B仍未授权，必须由未来独立PLAN冻结与terminal accepted Package-A code checkpoint相容的source-bound package identity；不得消费旧G4-05 package或从本handoff直接执行formal。

