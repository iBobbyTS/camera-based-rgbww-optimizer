# REF-P7-25-R2-B1A-C3E1 / Python symlink pre-root false-rejection review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E1-MACHINE-ACTIVATION-V1`

**Decision：**
`ACCEPTED_PRE_ROOT_FALSE_REJECTION_CONTROLLER_EXCEEDED_PLAN_PREDICATE`

## 1. Evidence

唯一execution evidence为`.agent-work/EXECUTION_RESULT.md`第55节；不存在external C3E1 package：

```text
reviewed PLAN SHA-256 =
  20b9ad12f7955ac0234b1d0259ed0312444e675fa4ec75299f8931b2893b31f3
reviewed FULL SHA-256 =
  6d6539a4fcb064497ddc34ff4996b225460cfdf1c0c01d4e05ec8faa0f2babc4
EXECUTION_RESULT.md after §55 SHA-256 =
  99d1ed512b86e95e24b718dd32a888e075788e159fe3041797445848b2af2a12
```

C3E1 controller在pre-root probe中拒绝`.venv/bin/python`是symlink，没有运行unittest loader probe。Root/container、FULL
subset credit、candidate load、clone/source/test/commit/manifest/R3 reads全部0；shared source/index/HEAD/PLAN/FULL未由
Executer修改。

## 2. Independent runtime verification

Planner独立只读验证：

```text
requested path = /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python
requested path is symlink = true
requested path executable = true
resolved executable = /Users/ibobby/miniconda3/bin/python3
stdlib unittest loader probe output = TestLoader
probe exit = 0
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
C3E1 fixed container = absent
```

PLAN只要求`Python executable + unittest loader`，未要求入口path non-symlink。Controller擅加non-symlink predicate，导致
false rejection。该run不构成runtime unavailable、candidate invalid、FULL activation invalid或science failure。

## 3. Successor contract

Fresh successor必须冻结真正的runtime predicate：requested path可为symlink；只要求它可执行、`resolve(strict=True)`得到
可执行目标，并由requested path成功启动`-B` stdlib unittest loader probe。禁止`is_symlink=false`、`lstat` symlink拒绝或
其他未写入PLAN的前置条件。

其余machine-driven FULL subset、唯一candidate object及SHA、source comparison-before-raise、candidate edit0、clean-room
PYTHONPATH/import identity、focused/full unittest各一次、retry0、single commit/manifest、original R3 three-hash与zero side-effect
合同不变。无Advisor/Human gate。

建议Orchestrator将FULL machine active task/contract更新为successor，并从successor PLAN nested
`required_full_machine_state`程序化merge；retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

