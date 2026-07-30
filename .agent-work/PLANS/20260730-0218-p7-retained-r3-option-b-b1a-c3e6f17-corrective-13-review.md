# C13 exact machine-contract scanner owner — Planner review archive

**Review 时间：** `2026-07-30`

**Reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-13`

**Planner 决定：** `ACCEPT`

## Reviewed scope

C13 只创建以下两条 validation-only implementation path，并向 `.agent-work/EXECUTION_RESULT.md` append 一条 terminal evidence：

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- `tests/test_agent_work_machine_contract.py`

未修改 PLAN、FULL、GUIDE、RESEARCH、debug 或既有 archive；无 staged path。retained R3、candidate、release、canonical validator、consumer、bootstrap、网络、环境变量及全部设备路径均未访问。

## Implementation method

实现将重复出现的临时 machine-row scanner 收敛为单一 repository-owned pure-bytes helper。PLAN/FULL parser 各自冻结 owner 与 marker；只接受 exact built-in `bytes`；要求物理行首唯一 candidate、exact backtick+LF、UTF-8 strict、strict JSON object；duplicate keys、non-finite constants、错误 suffix、CRLF、非 object 与非 exact bytes 均 fail closed。helper 不接受 path、marker、callback、validator 或 eligibility 参数，也不拥有任何 eligibility 结论。

dedicated `unittest` 覆盖 owner separation、source/raw-row/payload identity、候选数量与行号、行尾/前缀、UTF-8/JSON、nested duplicate keys、non-finite constants、JSON value/type 保真、非 bytes 输入和 validation-only public surface。

## Executer evidence

`.agent-work/EXECUTION_RESULT.md` 中唯一 `C13_IMPLEMENTATION_RESULT` strict-JSON object 报告：

- terminal：`PASS`
- dispatch PLAN SHA-256：`e99aad6853026a6c60a4c30e25c6bdda0356bc0ebbe0b730f63c8ddedd1d0b16`
- frozen FULL SHA-256：`e1c81dbd63c33292845b43a6e719914d1149a709e8017f97cd315a6139d66a56`
- dispatch activation HEAD：`fd1fe095f59b9accf008c95eeba73fbf6e778030`
- direct parent：`df1cdffb27699da7feac54379a8581cff9e85392`
- activation commit changed paths：仅 `.agent-work/PLAN.md`
- helper：7230 bytes，SHA-256 `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`，blob `5c581f9b502bcab1809b6a61a082a47f4150e09f`
- test：9820 bytes，SHA-256 `32c0d47cfcdfa49ecad2a4976f401021f0ff1bef947eab705a8c89836b2f5a19`，blob `c9589947e876920f0cbd2fe7e113592e3cd390e1`
- targeted test：`11/11`，exit `0`
- no-write compile：exit `0`
- helper replay：PLAN/FULL candidate 各 `1`，owner、source/raw-row/payload SHA 与 frozen fields 完整
- implementation creations `2`、ER appends `1`；retry/fallback/Git mutation/artifact/external path/retained R3/release/candidate/network/env/device/camera/Ray/strip/formal/public analyzer/canonical validator/eligibility emission 全部 `0`

## Planner independent validation

Planner 独立完成以下只读/允许验证：

1. lineage：HEAD `fd1fe095f59b9accf008c95eeba73fbf6e778030`，direct parent `df1cdffb27699da7feac54379a8581cff9e85392`，HEAD changed path 严格只有 `.agent-work/PLAN.md`；committed/current PLAN SHA 均为 `e99aad...0b16`，FULL SHA 为 `e1c81d...6a56`。
2. exact scope：HEAD 中两条 implementation path 都 absent；当前 dirty set 严格为 ER append 加两条新 implementation path；staged set 为空。
3. identity：独立重算两条文件 bytes、SHA-256 与 `git hash-object --no-filters` blob OID，均与 ER 的 after/final identity 一致且稳定。
4. source review：helper 无 path I/O、环境、subprocess、network/device、retained audit、canonical validator、payload repair 或 eligibility owner；公开 parser 仅有单一 `source` 参数。
5. targeted test 独立运行：`11/11`，exit `0`；未重跑 broader/full suite。
6. no-write `compile(..., 'exec')`：通过；未生成 bytecode。
7. ER strict JSON：唯一 C13 row 可严格解析，无 duplicate key/non-finite constant；字段、禁用预算和 stop 均满足 PLAN。
8. replay：独立调用 helper 解析当前 PLAN/FULL，逐项重算 source/raw-row/payload bytes 和 SHA；C13 task/contract、`RETAINED_UNVALIDATED_UNCONSUMED` 与 `candidate_contract_orchestrator_verified=true` 一致。
9. `git diff --check --` 限定两条实现路径通过。

Planner 的第一个只读证据脚本曾因把 PLAN 未要求写入 ER replay object 的 `marker_ascii` 错当成 ER 必填字段而产生一次本地 `KeyError`。该脚本没有写入、未触发设备/外部路径，也未重跑 Executer；修正 Planner 断言后 evidence audit 通过，不构成实现或 Executer failure。

## Findings and decision

没有发现违反 C13 acceptance contract 的实现缺陷或证据缺口。测试断言验证真实 fail-closed 行为，helper 的 owner 与 canonical eligibility validator 边界清晰。C13 implementation 接受。

该接受只证明 scanner helper 与 dedicated tests 满足 validation-only 合同；不等于 retained R3 审计、bootstrap、manifest、canonical eligibility validation 或 release consumption 已解锁/通过。

## Residual risks and exact next branch

- retained R3 状态继续为 `RETAINED_UNVALIDATED_UNCONSUMED`。
- canonical lineage validator 继续是唯一 eligibility owner，调用次数仍为 `0`。
- 当前 implementation、test、ER append、本 archive 与重写后的 PLAN 尚待 Orchestrator 亲自整理和提交，并由 Orchestrator 更新 FULL 状态/commit lineage。
- 唯一 next branch：`REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL`，仅允许 Orchestrator 进行 C13 acceptance commit/lineage seal；不得 dispatch Executer，不得直接进入 retained R3、bootstrap、eligibility、release 或设备工作。

**Planner stop：** `C13_ACCEPTED_WAITING_ORCHESTRATOR_LINEAGE_SEAL`。
