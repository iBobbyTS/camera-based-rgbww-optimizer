# F19-C3 Planner review：activation field-owner KeyError

**Review date：** `2026-07-29T22:03:06-06:00`

**Reviewed reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-3-BYTECODE-OWNER`

**Planner verdict：** `REJECTED_PRE_EDIT_FIELD_OWNER_KEYERROR`

## 1. 冻结输入

- activation HEAD：`9b1f55c7fbb34e002b7cd7559d36142ac2d173f2`
- direct parent：`6358476029ef07f74e4513d5667d2439bb4f281c`
- subject：`chore(plan): activate f19 local-run bytecode correction`
- changed paths：仅 `.agent-work/PLAN.md`
- reviewed PLAN SHA-256：`7f77d41a661e3c5599c4a81e1e7d07e52d79d6b2197adbf51f09da8c5d079e81`
- frozen FULL SHA-256：`e57b37b6a0fb7fb11d26f111fb579f1b7692c275b557ee9d705fa44fdb10ecb4`
- appended EXECUTION_RESULT SHA-256：`9ad496d0e3a2c83cc9acd22afa6e7e3feab0a1615675161e657cae14144143e7`
- helper blob/SHA-256：`5c581f9b502bcab1809b6a61a082a47f4150e09f` / `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`
- controller blob/SHA-256：`45097745bcc48aa1312b06fc07c6c910a4529325` / `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`
- dedicated test blob/SHA-256：`3cff60484e70db003409268f3365d7275dd53ab5` / `e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6`
- immutable C2 root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline`
- intended fresh C3 root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-3-offline`

## 2. 执行结果与独立重放

Executer在initial clean gate后，从committed helper直接调用
`parse_plan_machine_contract`一次、`parse_full_plan_machine_state`一次。随后执行源读取不存在的FULL顶层键
`candidate_contract`，触发`KeyError`并在任何external root、repo edit或validation command之前停止。

Planner用相同committed helper对committed PLAN/FULL bytes各独立解析一次，确认：

- PLAN/FULL candidate count均为`1`，owner分别为`PLAN`/`FULL`，source SHA与冻结值一致；
- FULL顶层存在且类型精确为：
  - `active_task: str`
  - `active_plan_contract_id: str`
  - `retained_r3_status: str`
  - `candidate_machine_contract_sha256: str`
  - `candidate_contract_orchestrator_verified: bool`
- FULL顶层不存在`candidate_contract`；
- PLAN的`frozen_full`仅拥有active task/contract、retained status、verified flag、path/SHA/count；不存在
  `candidate_contract`，也不存在`candidate_machine_contract_sha256`；
- candidate identity digest只由FULL顶层`candidate_machine_contract_sha256`拥有，PLAN不得猜测nested object；
- candidate scientific/eligibility payload仍禁止读取，本次只验证machine-state field identity。

## 3. 预算与不可变边界

- helper direct calls：PLAN `1`，FULL `1`
- EXECUTION_RESULT append：`1`
- fresh C3 root created / artifacts：`0 / 0`
- C2 evidence accesses：`0`
- test edits / controller edits / implementation diff paths：`0 / 0 / []`
- compileall / targeted / focused / full / CodeGraph / diff-check calls：全部`0`
- retry / fallback：`0 / 0`
- candidate、retained R3、release path probes/reads：全部`0`
- controller、validator、eligibility、manifest、Git mutation、network、env、device、camera、Ray、strip、cleanup、
  FORMAL、public analyzer、TD-C、sentinel、P8：全部`0`
- retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

Git diff在review开始时精确且仅为EXECUTION_RESULT单行append；controller、dedicated test与helper保持上述committed
blob/SHA。fresh C3 root独立确认仍不存在。

## 4. Findings 与决定

`REV-F19-C3-001`（blocking，accepted）：PLAN只要求Executer验证冻结字段，却没有把每个字段的唯一owner、
JSON path和精确type逐项机器化。Executer自行假设`FULL.value["candidate_contract"]`嵌套对象，造成pre-edit
`KeyError`。这不是helper、controller、测试、R3或科学合同缺陷。

因此C3不接受为test correction完成；其fail-closed结果接受为可信失败证据。下一包必须是唯一最小
field-owner corrective：先冻结并逐项验证PLAN/FULL field owner/path/type，明确禁止任何未列键、alias、nested
candidate object或推断；gate通过后继续同一个C3 test-only修复目标与完整fresh validation chain。

## 5. 下一分支

- proposed reference task：`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4`
- proposed contract：`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER`
- 先由Orchestrator把FULL active task/contract/status对齐C4并提交；随后Planner冻结activation lineage/FULL hash后才可
  dispatch一个新的Executer。
- C4不得修改helper、controller或production；唯一实现编辑仍是dedicated test的local `run`
  `STORE_FAST`/`LOAD_FAST` owner修复。
- 必须使用新的fresh C4 root；C2保持唯一允许只读的旧external evidence，C3 root不得创建、复用或探测。
- B2、real controller、candidate/retained R3/release、validator、eligibility、设备与后续科学阶段继续锁定。

无需Advisor：问题属于execution contract字段owner，不是色彩/测量科学分支。无需Human：没有高危设备操作。

**维护性判断：** 下一包只把既有helper返回对象的字段owner机器化，不新增parser、fallback或production抽象；
controller与eligibility owner维持不变。
