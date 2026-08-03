# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_PARTIAL_PASS_STATIC_HARNESS_FALSE_NEGATIVE`
- archived_at: `2026-08-03T10:19:04-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-01-SUCCESSOR-LINEAGE / G4-SUCCESSOR-LINEAGE-TEST-CONTRACT-REACHABILITY-CONVERGENCE-V1`
- source_checkpoint: `4568e794e97e79121c32f63164849804a3273e33`
- original_body_bytes: `7426`
- original_body_sha256: `7db482cf3e6e43be8fbe129359f1401b0ff533025041657453514ecc369e8b2a`
- terminal_disposition: `TEST_CONTRACT_GREEN_VALIDATION_INCOMPLETE_STATIC_HARNESS_IMPORTFROM_ALIAS_FALSE_NEGATIVE`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1019.md`
- evidence_pointer: `/Volumes/4T/temp/rgbww-optimizer/g4-01-validation-log-m6zcTT`
- exact_next_branch: `same REF-G4-01-SUCCESSOR-LINEAGE; validation-only static/full/CodeGraph/diff closure; no code/test edits`
- historical_non_executable: `true`

该archive不授权execution、retry、device、release、stage entry、budget或commit。下方为逐字节保留的reviewed ER body；
原始命令、计数、日志identity与first-failure观察不改写。

---

# REF-G4-01-SUCCESSOR-LINEAGE：test-contract convergence 单次执行 handoff

**状态：** `STOPPED_FIRST_VALIDATION_FAILURE_NO_RETRY`

**PLAN contract：** `G4-SUCCESSOR-LINEAGE-TEST-CONTRACT-REACHABILITY-CONVERGENCE-V1`

**Reference task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Planner stop：** `RETURN_FOR_G4_01_TEST_CONTRACT_REACHABILITY_REVIEW`

## 1. Activation / machine intake

```text
HEAD = 4568e794e97e79121c32f63164849804a3273e33
parent = 00978e859699fea6ffc51313c95711a24c647c01
branch = main
subject = docs(plan): activate g4 lineage test contract convergence
activation changed-path set =
  .agent-work/EXECUTION_RESULT.md
  .agent-work/FULL_PLAN_REFERENCE.md
  .agent-work/PLAN.md
  .agent-work/archived/EXECUTION_RESULT-20260803-1002.md
  .agent-work/archived/PLAN-20260803-1002.md
initial worktree = clean
PLAN/FULL active count = 1/1
contract = G4-SUCCESSOR-LINEAGE-TEST-CONTRACT-REACHABILITY-CONVERGENCE-V1
canonical task = REF-G4-01-SUCCESSOR-LINEAGE
```

Archive identities matched PLAN：

```text
.agent-work/archived/PLAN-20260803-1002.md
  SHA-256 = 3f4caca3e89e1d62ec22a7757c09ead3fceba4a7c449cdf26eda9e50966eee4e
.agent-work/archived/EXECUTION_RESULT-20260803-1002.md
  SHA-256 = e36536cea45cf6203ec1d666e6a8719fd4997631884d44a25bd99bfda9ff7c59
```

Machine intake使用inline exact embedded-row JSON parse并验证合同/task/count；未声称它替代尚未运行的post-validation
repo-owned closure检查。

## 2. Historical object restore

只读Git object验证通过：

```text
ref = refs/archive/g4-01-third-failure-20260802-2351
commit = 1346aeef1aff1387741f142257f1f481e45dd9af
parent = 7f2a016dbf648f07e53dc3d04a28d9746f68ddaa
tree = 6bd9d790b1d676d06e4a7d149aef791592be8a1d
subject = chore(audit): preserve rejected g4 lineage candidate
```

通过`apply_patch`恢复exact四路径；restore后四个initial SHA均与PLAN冻结值一致。随后只修改
`tests/test_p7_successor_lineage.py`：

- 未同步benign frozen-input tamper分别使用fresh final/strict root，exact断言
  `descriptor_reference_drift`；
- secret/historical各自通过topological canonical persistence重建frozen、plan、descriptor、summary、terminal，逐级更新
  preterminal/descriptor/terminal references，terminal最后写且不自引用；
- final/strict分别在fresh root exact断言`secret_material_prohibited`与
  `historical_input_prohibited`；未使用OR regex，未mock validator语义。

失败冻结时final identities：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
  SHA-256 = a944cc8d6186f8659848e89f30388f4a5112e18ed2dc6ea6fa1aec50ff95ff33
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py
  SHA-256 = 38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608
tests/test_p7_successor_lineage.py
  SHA-256 = bf2c3f36e5df7f78b4e607181bb8194bd6d589979ff9022af4060c69640780e4
tests/test_p7_retained_r3_provenance_io.py
  SHA-256 = 21f47535106937f2f99acdece8b3fb5c6717e1f9900f974e60b0f744163d34c6
```

因此production两文件与provenance test最终仍为exact frozen SHA；只有successor test在restore后改变。

## 3. Validation sequence

所有命令日志位于fresh offline log root：

```text
/Volumes/4T/temp/rgbww-optimizer/g4-01-validation-log-m6zcTT
```

该目录仅为validation log，不是release或experiment root。

| Step | Result | Count / detail | Log bytes | Log SHA-256 |
| --- | --- | --- | ---: | --- |
| machine intake | `PASS` / exit 0 | PLAN/FULL `1/1` | 291 | `6492cbc8f87f66805296baedf35a38289f37536399cf00336c254d33276514e3` |
| CodeGraph pre-query | exit 0 | pre-edit owner/blast-radius query；不构成post-sync closure | 25378 | `f6cf19d63343d431274fb2b936bf20fb12384d04197bad0f9af70a0900cc3990` |
| historical object intake | `PASS` / exit 0 | commit/ref/tree/four blobs/four SHA | 1101 | `cb82714d0d48ac61331c4ef99fc59dbabc27cbc7656ca52828960c43ce4ce676` |
| restore identity | `PASS` / exit 0 | four frozen SHA exact | 838 | `0056c23b3754fd0a53d76a59c511cbb2e243b762984fcdd05294c675b7d16e0f` |
| prevalidation scope | `PASS` / exit 0 | immutable three SHA exact；successor test only mutable | 828 | `dc3c14cd83d847d2a48d8d1fbfa9406c3b64d5774193d7a83fdfa3964d30a996` |
| targeted | `PASS` / exit 0 | 45 discovered, 45 passed, 0 skipped/fail/error | 8648 | `8fb07a329195f9a64ed6c7a40f46e5ec8e98b8323dec9f4f77c27adc67621994` |
| focused/integration | `PASS` / exit 0 | 83 discovered, 83 passed, 0 skipped/fail/error | 18175 | `9840bc9a53f97cf1b6550e02e0b4d75d0bcadaa19393f1a6ce797705ef135cd7` |
| compile exact four paths | `PASS` / exit 0 | `compileall -q` | 141 | `d3b98943ab8adc4d3c291ed47ac2f306a64c34261d4b58fc5e1383892ce19188` |
| AST/import static | **`FAIL` / exit 1** | first failure；后续全部停止 | 232 | `cbb267afa5d63b1448fc03e6d11f59f0ab88208bfa63c20f57f3d8695fd7b060` |

### First failure

Static command在确认五个public seam callable后，对AST import集合执行delegate ownership assertion时触发裸
`AssertionError`。该检查只收集`ImportFrom.module`，没有把
`from camera_based_rgbww_optimizer... import p7_* as ...`的alias name加入集合，因此对
`p7_retained_r3_provenance_io` / `p7_thermal_diagnostics`的字符串归属断言不可满足。

这是validation harness failure，不是targeted/focused runtime failure；但PLAN规定任一static失败后：

```text
no test-after-fix
no retry
no fallback
stop subsequent validations
```

Executer因此没有修改static命令、代码或测试，也没有重跑。

## 4. 因first failure未运行

- full suite：未运行；没有继承旧836/836或827/827；
- accepted EQ fixture：未读取（full suite未启动）；
- `codegraph sync`与post-sync successor→provenance/thermal query：未运行；
- `git diff --check`、两个untracked add的no-index whitespace check、final protected-path no-diff：未运行；
- stage、commit、amend、push：均未执行。

当前candidate不能请求acceptance；targeted/focused/compile绿不覆盖static failure与未运行的full/CodeGraph/diff gate。

## 5. Changed paths 与 authority counters

当前worktree在写本handoff后只应包含PLAN授权的五路径：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py
tests/test_p7_successor_lineage.py
tests/test_p7_retained_r3_provenance_io.py
.agent-work/EXECUTION_RESULT.md
```

```text
real release root acquisition/generation/validation/consumption = 0
retained R3 / legacy release access = 0
accepted EQ fixture access = 0
other external experiment payload access = 0
synthetic temporary roots = test-only under /Volumes/4T/temp/rgbww-optimizer, fixture-reclaimed
device/network/camera/Ray/strip/capture/formal R6/TD-C = 0
firmware/deployment = 0
PLAN/FULL/GUIDE/RESEARCH/archive mutation by Executer = 0
corrective task/new experiment root = 0
commit by Executer = 0
```

## 6. 唯一 Planner review request

```text
REF-G4-01-SUCCESSOR-LINEAGE remains unfinished
test-contract fixtures and targeted/focused/compile evidence are green
static validation harness failed before full/CodeGraph/diff closure
request = RETURN_FOR_G4_01_TEST_CONTRACT_REACHABILITY_REVIEW
release/device/formal = still locked
```

Planner/Orchestrator需审查first-failure disposition；Executer不提出下一包、不修复、不重跑，也不把candidate称为accepted owner。
