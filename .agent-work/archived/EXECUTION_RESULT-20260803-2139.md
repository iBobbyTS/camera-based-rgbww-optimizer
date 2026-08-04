# Archive record

- Archive status: `REVIEWED_REJECTED_HISTORICAL_NON_EXECUTABLE`
- Timestamp: `2026-08-03T21:39:09-0600`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-RAY-R6` Package A V2 phase-1 handoff
- Source checkpoint: `34092241057a3b51e8afe7a4ef8cea1178eb080d`
- Source bytes: `7840`
- Source SHA-256: `07d628de839a2140db0e2c8beffca9dbe75e79472d9b3ab431b7737d580ecd45`
- Terminal disposition: `REJECTED_SOURCE_ATTESTATION_CHILD_SUBJECT_UNREACHABLE`
- Evidence/index pointers: live candidate diff at the source checkpoint worktree; five selected synthetic tests independently passed, but the planned child subject remained unreachable through the descriptor attestation contract.
- Exact next branch: same `REF-G4-06-RAY-R6`; minimum source-attestation subject alignment and protective tests only.
- Historical declaration: `historical_non_executable`; this archive authorizes no execution, device access, release, retry, stage entry, budget, or commit.

## Archived source body

# REF-G4-06-RAY-R6 Package A V2 authority-contract phase-1 handoff

**Status:** `READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`

**Planner stop:** `RETURN_FOR_G4_06_PACKAGE_A_AUTHORITY_CONTRACT_TWO_PHASE_REVIEW`

本handoff只证明Package-A production CLI seam的future formal authority transition在synthetic环境可达；不宣称Package A已接受，不授权Package B、formal root/device/capture，也不表示hardware ready、formal/quality/history pass或G4-07 unlocked。

## 1. Activation intake

- branch：`main`
- activation HEAD：`34092241057a3b51e8afe7a4ef8cea1178eb080d`
- activation tree：`0926d0c1cd07dae1270148d69f74e279d38aab18`
- parent：`37a3866af0c9c79556690b1624b9e96468756c62`
- subject：`docs(plan): revise ray r6 authority contract seam`
- activation changed paths exact：FULL、PLAN、reviewed PLAN archive、reviewed ER archive。
- initial dirty exact为ER、measure、stage-gate、focused tests；SHA分别为：
  - ER `3708bbd1200cef8fda771d350536515326461aaac88ab98c0d828365bd4e2d52`
  - measure `babca565fafa7492a3fdcc7a498dc7d2be129367fe40118e489b5f0f7e11b02f`
  - stage-gate `db2e2a3e2b9f8881bd5bda3a31b1dcf56b63d31302e33c3d0162e294eaa664c9`
  - tests `ddc8debef5f0bdabdfa7dfa9fabc8424716bc6ceb71cb1dd6ff4cb8da8386c2b`
- PLAN/FULL strict parser：active `1/1`，task `REF-G4-06-RAY-R6`，engineering contract `G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V2`，canonical next同一task。

## 2. Maintainability and ownership

CodeGraph复核确认本修订只需收敛existing focused stage-gate machine validator。最终ownership：

- package、machine contract、Git attestation、future activation、runtime SHA/materialization继续唯一归`p7_td_b_r6_stage_gate.py`；
- measure只保留上一candidate的显式CLI parse和一次dispatch，本次没有再修改measure；
- narrow hook与real runner保持existing single owner/exact once；
- 未新增module、test module、controller、schema family、parallel serialization或authority owner；
- wrapper、thermal scientific owner、GUIDE/RESEARCH保持只读。

## 3. Authority transition implementation

Production validator现在严格区分：

1. engineering Package A contract：`G4-RAY-R6-PRODUCTION-CLI-LAUNCH-SEAM-PACKAGE-A-V2`。当前PLAN/FULL authority为false，必须返回`production_machine_contract_drift`，不得进入activation/materializer/backend；
2. future formal Package B contract：`G4-RAY-R6-FORMAL-ACQUISITION-PACKAGE-B-V1`。只有exact matching live PLAN authority与FULL non-authorizing mirror同时成立才可继续。

Exact Package-B PLAN authority为closed mapping，绑定：

- TD-B、Ray、TD-B stage、remote backend；
- formal execution/root/device/camera/Ray/capture=`true`；
- strip=`false`；
- exact formal root parent/basename/regex；
- logical16、physical16、launch1、retry0；
- release consumption与TD-C=`false`。

FULL要求：

- active/current-plan count均1、task/canonical next同一G4-06、active contract exact Package B；
- `executable=false`、`full_is_non_executable_reference=true`；
- 顶层device/camera/Ray/strip/formal/release/TD-C均false；
- nested `g4_06_state` exact标记`B_FORMAL_ACQUISITION`、authority owner为matching live PLAN only，并逐字段镜像PLAN formal bounds；G4-07仍false。

Machine authority在sealed package validation之后、C/L activation/materializer/backend之前验证。Package A不能生成authorized runtime；Package B exact state才可到达existing materializer与narrow hook。

## 4. Meaningful authority matrix

- current Package-A V2 exact synthetic machine state：negative，`production_machine_contract_drift`，factory/delegate/root create=`0`。
- actual live Package-A V2 repo machine state通过read-only direct validator复现同一negative结果。
- exact synthetic Package-B PLAN+FULL mirror：package → C/L attestation → activation → materializer → narrow hook → injected delegate PASS；factory/delegate each once，fake backend connect=`0`。
- 33个closed drift subcase全部pre-backend FAIL，包括：
  - PLAN formal/device/camera/Ray/capture false；
  - wrong source/backend、PLAN non-executable；
  - PLAN或FULL mirror authority missing/extra；
  - Package-A contract配true authority、任意第三contract、PLAN/FULL mismatch；
  - FULL nested mirror mismatch、FULL顶层自称device/formal/executable或丢失non-authorizing lock；
  - wrong task/count/canonical next/current-plan mirror；
  - retry、launch、logical、physical、root、strip、release、TD-C bounds扩张。
- existing inventory/hash/mode/terminal/semantic guard、per-commit C/L、expected runtime、kwargs exact-once、delegate exception no-retry、generic formal bypass与legacy CLI tests全部保留。
- real-topology source-bound regression：在旧descriptor code-owner后提交一个Package-A code child，再激活synthetic Package-B machine；old package命中`source_reference_drift`，没有把later child错误提升为code owner，factory/delegate=`0`。

## 5. Exact candidate diff and identities

相对activation HEAD：

- measure：`+72/-1`，`194256` bytes，SHA-256 `babca565fafa7492a3fdcc7a498dc7d2be129367fe40118e489b5f0f7e11b02f`
- stage-gate：`+247/-6`，`77738` bytes，SHA-256 `deb8073038b5d3126ef7a124195a8d2e1ecd298a1f3e94d6e90cd2b878f21553`
- focused tests：`+675/-23`，`88572` bytes，SHA-256 `040f338f6c3a4991c025f024599489b3decf0230cb34d1e1c7f6188b572433f4`
- ER：本handoff，不属于controlled code child。

Measure identity与V1 retained candidate一致；V2修订只改变stage-gate authority owner与focused tests。

## 6. Validation

- targeted stage-gate + selected legacy CLI：`42/42` PASS，`31.395s`。
- focused command：
  `.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract tests.test_p7_thermal_diagnostics tests.test_p7_successor_e2`
  → `224/224` PASS，`68.039s`。
- `.venv/bin/python -m compileall -q src tests`：PASS。
- `zsh -n tmp/run-p7-thermal-diagnostics.zsh`：PASS。
- repo-owned PLAN/FULL parser与actual Package-A negative probe：PASS。
- stage-gate device/camera/network control imports：`0`。
- `codegraph sync`：PASS；post-query确认machine gate位于backend factory前，authority logic未移入measure。
- `git diff --check`：PASS；dirty path set exact为ER与三candidate；protected paths无diff。
- final candidate唯一fresh full：`.venv/bin/python -m unittest discover -s tests` → `951/951` PASS，`203.123s`，exit `0`。
- full之后未修改semantic code，也未重复full。

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

请求Planner做Package-A V2 phase-1 review。若接受，请返回`READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`，由Orchestrator创建direct child：

- subject exact：`feat(stage-gate): route ray r6 formal launch owner`
- changed paths exact：measure、stage-gate、focused tests
- ER不得进入code child。

随后同一PLAN进入phase-2 read-only review。Package B仍未授权，必须由未来独立PLAN冻结与terminal accepted Package-A code checkpoint相容的source-bound package identity；不得消费旧G4-05 package或从本handoff直接执行formal。

