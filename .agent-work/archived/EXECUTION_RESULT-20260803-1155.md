# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_FIRST_SYNTHETIC_FIXTURE_IDENTITY_FAILURE`
- archived_at: `2026-08-03T11:55:24-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-02-PREDEVICE / first owner integration execution`
- source_checkpoint: `5e5ad9583346a0eba1f3da6f205fd073b73af8d7`
- original_body_bytes: `4236`
- original_body_sha256: `533ab8d992faeafacd13743a5b5eeef1c6b6c07255312c4f595c2bd74d455a38`
- terminal_disposition: `REJECTED_FIRST_ENGINEERING_FAILURE_SYNTHETIC_TEST_FIXTURE_CONTRACT_MISMATCH`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1155.md`
- exact_next_stop: `SAME_REF_G4_02_ONE_BOUNDED_SYNTHETIC_FIXTURE_IDENTITY_CORRECTION`
- historical_non_executable: `true`

该archive不授权execution、release consumption、durable root、device、formal、retry、stage entry、budget或commit。下方为逐字节
保留的reviewed ER body。

---

# REF-G4-02-PREDEVICE：owner integration首次执行结果

**状态：** `FAILED_SYNTHETIC_FIXTURE_CONTRACT_RETURN_FOR_PLANNER_REVIEW`

**PLAN contract：** `G4-PREDEVICE-CANONICAL-OWNER-INTEGRATION-V1`

**Reference task：** `REF-G4-02-PREDEVICE`

**Planner stop：** `RETURN_FOR_G4_02_PREDEVICE_OWNER_INTEGRATION_REVIEW`

## 1. Activation与intake

- branch：`main`
- activation HEAD：`5e5ad9583346a0eba1f3da6f205fd073b73af8d7`
- activation tree：`0f6dae8f127e35e6ebed99225add9a5ed2a8ca29`
- direct parent：`df261592fbafbf09bd6ce018d2a60de62996fab1`
- subject：`docs(plan): activate g4 predevice owner integration`
- activation path set、三个archive bytes/SHA/source-body SHA均与PLAN一致。
- repo-owned PLAN/FULL machine parser：active count `1/1`，active task均为
  `REF-G4-02-PREDEVICE`；intake时worktree clean。

初始archive checker曾把FULL archive的真实body marker
`<!-- ARCHIVED_SOURCE_BODY_START -->`误当成`---`分隔符而assert；只读检查确认archive identity及body hash exact后，归类为
checker假设错误，不是repository drift，随后才开始代码写入。

## 2. Maintainability preflight与实现

CodeGraph preflight确认既有owner边界：

- `p7_successor_lineage.py`：bundle schema、public/final/strict、cross-reference；
- `p7_retained_r3_provenance_io.py`：root/inventory/exact-file/canonical/same-target I/O；
- `p7_thermal_diagnostics.py`：policy、R6 plan、machine operational/lock contract。

新增的小型composition seam未修改上述owner或三个巨型P7模块，也未增加CLI、durable writer、release consumer或第二套serializer。
它将decoded immutable mapping通过既有`json_native_value`投影后再交给thermal exact validator。

已写文件：

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py` | 12066 | `0d6c529934b59a2faedf802bdd1e872a8c18085d055c4bfb1604e49032885be1` |
| `tests/test_p7_successor_predevice.py` | 19352 | `6d5ea7acf5289df5d5a1c33411b2559c69f603fc3fe08447174e7ecf7f24de52` |

## 3. 首次targeted结果与失败分类

执行exact命令：

```text
.venv/bin/python -m unittest tests.test_p7_successor_predevice -v
```

结果：`Ran 12 tests`，`FAILED (errors=12)`，exit `1`。所有错误均发生于共同`setUp`，尚未进入predevice oracle正向路径：

```text
camera_based_rgbww_optimizer.optimization.p7_successor_lineage.SuccessorLineageError:
eq_manifest_hash_drift
```

精确根因：synthetic fixture向production `build_successor_lineage_inputs`传入`b"x" * 7980`，但同时把expected manifest
SHA设为占位值`"c" * 64`。production successor owner正确拒绝了不一致的bytes/SHA。

分类：`FIRST_ENGINEERING_FAILURE_SYNTHETIC_TEST_FIXTURE_CONTRACT_MISMATCH`。

- 不是production owner/API failure；
- 不是source/policy/EQ scientific contract变化；
- 不是external bundle drift；
- 不是需要Advisor判断的科学分支；
- 最小后续修正应只让synthetic manifest SHA由同一fixture bytes计算，并保留production hash gate断言。

根据PLAN failure convergence，首次targeted失败后未在本包内修补，未运行focused/full/compileall/CodeGraph sync/diff final
validation，也未进行real-bundle调用；交回Planner决定是否给一次bounded correction。

## 4. External与authority ledger

```text
real G4-01 bundle read invocation = 0
durable/external predevice root creation = 0
release consumption = 0
retained R3 / R2 / other external payload access = 0 / 0 / 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits by Executer = 0
commit/amend/stage/push = 0
Terminal/background/automation = 0
```

`canonical_validator_success/eligibility/release_consumable/release_consumption_authorized`仍全部为`false`；retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`。未授予任何device、camera、Ray、strip、capture、formal R6或TD-C authority。

当前worktree只有PLAN允许的三个path：本文件与上述两个untracked implementation/test文件。请求Planner在唯一stop
`RETURN_FOR_G4_02_PREDEVICE_OWNER_INTEGRATION_REVIEW`验收失败分类；不得激活G4-03。
