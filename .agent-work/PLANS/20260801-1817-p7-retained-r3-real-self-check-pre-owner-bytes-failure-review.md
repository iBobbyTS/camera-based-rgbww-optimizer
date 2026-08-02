# P7 retained-R3 Option B：fresh real self-check pre-owner bytes failure 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1-R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FIXED-MATRIX-ACCEPTED-FRESH-REAL-SELF-CHECK-DISPOSITION-V1`

**Activation：** `992b04d0bc7c90ea2d5fef57d7f01c3e82dcd8cd`

**Evidence child：** `a61cd46958e1b97d70015064dcbdcfe121672e4d`

**Planner 决定：** `ACCEPTED_PRE_OWNER_FAILURE_LIFECYCLE_REJECTED_REAL_SELF_CHECK_EXECUTION`

## 1. Reviewed scope、topology 与 evidence quality

Planner读取project skill、active committed PLAN、activation/evidence Git topology、evidence child中的ER physical-EOF append、唯一fresh controller source及唯一fresh evidence root四件套。未读取、stat、list或search任何旧failed source/root、原14个retained-R3 physical inputs或retained payload；未调用owner、canonical validator、test、CodeGraph、release、network或device路径。

Activation `992b04d0bc7c90ea2d5fef57d7f01c3e82dcd8cd`是`a7b9e1139ab8723c7cca3cd800b65b3c35308857`的direct child，subject exact `chore(plan): run fresh real self-check disposition`。Evidence `a61cd46958e1b97d70015064dcbdcfe121672e4d`是activation direct child，subject exact `chore(evidence): record fresh real self-check disposition`，changed path仅`.agent-work/EXECUTION_RESULT.md`。

Evidence ER保持activation ER bytes为exact prefix，在true physical EOF新增`4825` bytes，suffix SHA-256 `43939cb70cdce195185f01b632bcff6b018c3ba6e1531ba22aae0678e581bcf0`。Fresh source `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-fixed-matrix-real-self-check-disposition-992b04d0bc7c.py`前后均为`12992` bytes / SHA-256 `81f258673e78094d633672659d76312779273184083e6875773213289cdbd5a0` / mode `0600`。

Fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-fixed-matrix-real-self-check-disposition-992b04d0bc7c-output`为mode `0700`且exact inventory仅四件：

1. `00-execution-contract.json`：`3786` bytes，SHA-256 `f8d2079d9ed210dfe14a5acef3d8cafa316280394ecba1d0cd26158fcd90daed`，mode `0600`。
2. `00-execution-contract.sha256.json`：`308` bytes，SHA-256 `b726c448932f09713bebcf52f51cc6f3e76d9c9cbe01c4a4ad6d71b3490658dc`，mode `0600`。
3. `01-terminal-summary.json`：`2907` bytes，SHA-256 `48259ef8c9bf47c322470f6b2f59279478d3d785c5151f9743c94bfd01fd3ccc`，mode `0600`。
4. `01-terminal-summary.sha256.json`：`306` bytes，SHA-256 `f45db6396ae4b50f204cb75adee87ee385a4df1f226a1888011a66755d0424a6`，mode `0600`。

Planner独立strict JSON解析并核验两枚seal逐字绑定target path、bytes、SHA-256及mode，均通过；inventory无extra/missing artifact。该证据足以验收failure lifecycle，但不构成owner self-check、production owner、lineage、eligibility或release credit。

## 2. Independent finding 与决定

Fresh controller在pre-owner active PLAN/FULL contract gate调用accepted parsers时传入`Path.read_text()`的decoded `str`；accepted parser要求exact source `bytes`，因此首个失败为：code `PRE_OWNER_GATE_FAILURE`，stage `pre_owner_gate`，type `MachineContractValidationError`，message `source_not_exact_bytes`，row `null`。

失败发生在任何原physical input acquisition之前：verified identities `0/14`，`input_before=[]`，`input_after=[]`，`inputs_unchanged=false`；原14个input path没有被controller读取、写入、copy、repair、regenerate、list或stat。Owner未resolve/调用，complete ordered Git ledger `[]`、count `0`。Owner calls attempted/returned `0/0`，retry `0`，fallback `0`，success report `0`，owned processes empty `true`。

Repository code/test writes、tests、CodeGraph、canonical validator、production-owner conclusion、lineage、eligibility、release、network、device、camera、Ray、strip、cleanup、formal、public analyzer、PLAN/FULL/archive writes及implementation commit均为`0`。Production owner、lineage、eligibility、release consumable均为`false`；retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

因此Planner接受本次fail-closed terminal与evidence lifecycle，但拒绝原计划的real self-check execution：owner并未运行，不能授予任何scientific/production/lineage/eligibility/release credit。问题是execution packaging中的exact raw-byte parser binding，现有production/test不需要修改。

## 3. Exact successor

唯一successor是pre-owner accepted-parser exact-byte binding corrective，并在修正后执行唯一一次新的fresh pure-offline disposition：

1. 新controller必须从activation Git objects各exact读取PLAN/FULL raw bytes一次，并把同一未经decode、normalize、拼接或重编码的`bytes`对象直接传给`parse_plan_machine_contract`与`parse_full_plan_machine_state`；禁止`read_text()`、`.decode()`或controller自建JSON/Markdown parser。Parser成功后只消费accepted `.value`。
2. Controller source必须是全新activation-short12派生路径；fresh evidence root也必须是全新activation-short12派生目录，二者此前不存在，禁止复用失败source/root。失败source/root只能以本archive冻结identity引用，不得读取、stat、list、search或复用。
3. Pre-owner gate成功后，才按active PLAN冻结的physical group order和14个exact path/bytes/SHA读取原immutable inputs；不得copy、repair、rewrite、regenerate或替换payload。
4. Current repo-owned `camera_based_rgbww_optimizer.optimization.p7_retained_release_audit.run_real_manifest_self_check`仅调用exact一次；owner call attempted budget `1`、retry `0`、fallback `0`。必须保存完整有序owner Git ledger；无论owner pass或failure，均seal exact terminal、counters、zero locks、owned-process状态与authority boundary。
5. ER只允许在physical EOF append一次完整handoff；Executer不得改PLAN/FULL/archive或commit。Canonical validator、eligibility、release consumption、device、FORMAL-R6、strip、TD-C、sentinel及P8继续锁定。

**Exact next reference：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1-C1-C1-R1-C1`

**Exact next activation parent：** `a61cd46958e1b97d70015064dcbdcfe121672e4d`

**Exact next activation subject：** `chore(plan): correct real self-check parser byte binding`

**Exact next activation changed paths：** `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`、`.agent-work/PLANS/20260801-1817-p7-retained-r3-real-self-check-pre-owner-bytes-failure-review.md`

**Exact next Planner stop：** `FRESH_REAL_SELF_CHECK_PARSER_BYTE_BINDING_CORRECTIVE_WAITING_PLANNER_REVIEW`

## 4. Required FULL updates（Orchestrator-owned）

- 记录activation `992b04d0bc7c90ea2d5fef57d7f01c3e82dcd8cd`、evidence `a61cd46958e1b97d70015064dcbdcfe121672e4d`及决定`ACCEPTED_PRE_OWNER_FAILURE_LIFECYCLE_REJECTED_REAL_SELF_CHECK_EXECUTION`。
- 将唯一active task/reference切换为上述successor，active contract切换为`P7-TD-B-RETAINED-R3-OPTION-B-FRESH-REAL-SELF-CHECK-PARSER-BYTE-BINDING-CORRECTIVE-V1`。
- 冻结exact raw-byte parser binding、全新source/root模板、owner exact-one、retry/fallback zero、failure/success terminal与全部zero locks。
- 保持fixed matrix只获synthetic engineering attribution；real self-check仍未完成，retained R3未验证/未消费，canonical validator仍是sole eligibility owner，所有false conclusion及device lock不变。

维护性判断：successor只修正controller对既有accepted parser的输入类型，不改production/test或新增parser owner；职责边界清晰，无需架构重构。
