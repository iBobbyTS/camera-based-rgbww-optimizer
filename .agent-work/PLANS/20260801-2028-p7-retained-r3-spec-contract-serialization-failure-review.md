# P7 retained-R3 Option B：spec-contract serialization failure review

**Planner decision：** `ACCEPTED_TRUTHFUL_UNSEALED_FAIL_CLOSED_LIFECYCLE_REJECTED_SEALED_SPEC_AND_COMPLETE_CONTRACT_CREDIT`

**Reviewed activation：** `d399c1a1c7af781d15a7705c2118f87e2239c278`；parent `253eaa4a23db1e7c9862606b8212e41c71371b22`；subject `chore(plan): complete real self-check spec contract`；changed paths exact FULL、PLAN、1859 archive。

**Reviewed evidence：** `39ca883dd4d75ac03f47cd4567b1fbe9c365a35c`，只改 `.agent-work/EXECUTION_RESULT.md`。

## 1. Evidence identity

- Activation ER：bytes `1613221`，SHA-256 `bdf94f8ab1b1f8fc45acd7d96cc09642cc10474bcb0c9fcb2a978cf0126cc97e`，blob `418e18c14574d55eb00b1d7c29eff66419eff01b`。
- Evidence ER：bytes `1618285`，SHA-256 `803a023422bf20c096c218498e44f7196d6bc99aa8504ff4e8110592b9448abd`，blob `9c031663d67cdf8d91d2d56fba327a58ff12f8de`。
- Evidence以activation为exact prefix；唯一EOF suffix bytes `5064`，SHA-256 `ac09f30859c1d08369c79c77fcb5c309e16cfce1a3824b14a7fc00f4fefe4e79`。
- Fresh source `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-real-manifest-spec-contract-d399c1a1c7af.py`：regular、non-symlink、`0600`、bytes `14566`、SHA-256 `e91fb6b2a60eeda001743ae8b56bb69b6b01da5470a49a60dab5b58fb5d6049f`。
- Fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-real-manifest-spec-contract-d399c1a1c7af-output`：directory、non-symlink、`0700`，failure后为空。

## 2. Accepted facts

Activation topology、PLAN/FULL accepted parser、required FULL subset、冻结accepted PLAN及6个允许repo source/test identity全部通过。`.value`与`.evidence`通过公开接口取得；14 physical inputs、old external roots、owner、tests、validator、release、network/device及retry/fallback全部为`0`。

按公开字段顺序在memory中到达首个missing field：`baseline.human_governance_override`，公开type `str`、field index `10`。允许的`61c33604...` `typed_baseline`未提供其value；test fixture不具authority。该事实只能作为本次未封存失败的可信执行观察，不是sealed contract。

## 3. Rejected credit

在首个artifact write前，controller把`.evidence.to_mapping()`中仍含nested `mappingproxy`的tree直接交给`json.dumps`，触发`TypeError: Object of type mappingproxy is not JSON serializable`。因此contract、seal、terminal均未创建，writes `0/0/0`；不得授予sealed-spec、complete-contract、owner、production-owner、lineage、eligibility或release-consumable credit。

## 4. Next branch

唯一下一分支是纯离线JSON-native projection纠偏：递归机械投影公开`Mapping`/tuple与JSON scalar，重新运行fresh diagnostic，并只允许输出sealed `FIRST_MISSING_SPEC_FIELD`或complete contract。不得猜测或直接补`human_governance_override`，不得读取physical inputs/old roots、调用owner、改production/test、跑tests、validator/release或设备操作。

Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`；FORMAL-R6、TD-C、sentinel与P8继续锁定。无科学分支，不需要Advisor；无设备操作，不需要Human授权。

维护性判断：下一包只修controller边界上的机械JSON-native投影，不新增adapter module、owner或production抽象。
