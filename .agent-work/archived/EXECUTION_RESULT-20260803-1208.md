# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED_G4_02_PREDEVICE_OWNER_INTEGRATION`
- archived_at: `2026-08-03T12:08:53-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-02-PREDEVICE / bounded fixture correction and real read-only observation`
- source_checkpoint: `5e5ad9583346a0eba1f3da6f205fd073b73af8d7`
- original_body_bytes: `6076`
- original_body_sha256: `b516b9246ebaf404da94f4873e05d498619c324b477fb8d266e3a2e5dea82e3c`
- terminal_disposition: `ACCEPTED_G4_02_PREDEVICE_OWNER_INTEGRATION_AND_REAL_READ_ONLY_OBSERVATION`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1208.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_FOCUSED_CODE_TEST_DOCS_COMMIT_BEFORE_DURABLE_PREDEVICE_PACKAGE`
- historical_non_executable: `true`

该archive不授权durable package、release consumption、device、formal、retry、stage entry、budget或commit。下方为逐字节
保留的reviewed ER body。

---

# REF-G4-02-PREDEVICE：bounded fixture correction执行结果

**状态：** `IMPLEMENTED_VALIDATED_REAL_READ_ONLY_OBSERVATION_RETURN_FOR_PLANNER_REVIEW`

**PLAN contract：** `G4-PREDEVICE-BOUNDED-SYNTHETIC-FIXTURE-IDENTITY-CORRECTION-V2`

**Reference task：** `REF-G4-02-PREDEVICE`

**Planner stop：** `RETURN_FOR_G4_02_PREDEVICE_BOUNDED_FIXTURE_CORRECTION_REVIEW`

## 1. Continuation intake

- branch：`main`
- activation HEAD/tree：`5e5ad9583346a0eba1f3da6f205fd073b73af8d7` /
  `0f6dae8f127e35e6ebed99225add9a5ed2a8ca29`
- repo-owned PLAN/FULL parser：contract exact
  `G4-PREDEVICE-BOUNDED-SYNTHETIC-FIXTURE-IDENTITY-CORRECTION-V2`，active count `1/1`，task exact
  `REF-G4-02-PREDEVICE`。
- dirty ownership：与PLAN列出的7 paths exact，无额外dirty path。
- preserved production candidate：12066 bytes /
  `0d6c529934b59a2faedf802bdd1e872a8c18085d055c4bfb1604e49032885be1`。
- pre-correction test：19352 bytes /
  `6d5ea7acf5289df5d5a1c33411b2559c69f603fc3fe08447174e7ecf7f24de52`。
- `PLAN-20260803-1155.md`：14650 bytes /
  `b4f4e9b97997cace61a4baa975e58592d3cf71b4fb044ac9ca4c234b1293538a`；source body 13688 bytes /
  `ac8540ee89308a4061dbdfd244feabd2294d649d9d8e848cd7e40448dc5b1acd`。
- `EXECUTION_RESULT-20260803-1155.md`：5201 bytes /
  `70ae665da1d8f191eb205b932c2db2a2021aec8abfead250346e818f8d52ef26`；source body 4236 bytes /
  `533ab8d992faeafacd13743a5b5eeef1c6b6c07255312c4f595c2bd74d455a38`。

两个intake checker曾分别错误假设FULL machine键名为`contract_id`、archive使用旧body marker；repo-owned parser、actual schema及
archive `---` separator证明均是只读checker假设错误，不是repository drift。更正checker后所有intake identity exact通过。

## 2. 唯一bounded correction

只修改`tests/test_p7_successor_predevice.py`的共享synthetic fixture identity：

```python
EQ_MANIFEST_BYTES = b"x" * EQ_BYTES
EQ_SHA256 = hashlib.sha256(EQ_MANIFEST_BYTES).hexdigest()
```

两处builder输入均改用同一`EQ_MANIFEST_BYTES`。未mock或绕过production hash owner，未改变其他test语义。修正后测试文件：

```text
19429 bytes
eb90e55026a1c4bd927c80ab80f198346eb23ac97122eb52dabf914f99c1c509
```

Production candidate保持byte-exact不变，未发生production API edit。

## 3. Fresh validations

| validation | result |
| --- | --- |
| `.venv/bin/python -m unittest tests.test_p7_successor_predevice -v` | PASS，12/12，exit 0 |
| focused exact four-module unittest command | PASS，127/127，exit 0 |
| `.venv/bin/python -m unittest discover -s tests -v` | PASS，858/858，exit 0，156.565s |
| `.venv/bin/python -m compileall -q src tests` | PASS，exit 0 |
| `codegraph sync` | PASS，exit 0，2 changed files / 72 nodes |
| `codegraph explore "p7_successor_predevice ownership call paths and validators"` | PASS，exit 0 |
| `git diff --check` | PASS，exit 0 |

Negative matrix覆盖并通过：historical/retained marker；source head/checkpoint/tree；policy/EQ refs；auto/weak reacquire；capture
swap/missing/duplicate/resume；pooling/origin/cross-root；600/steady/locks；inventory/symlink/mode/size/hash/canonical/identity；validator
immediate failure/no fallback。Existing successor `eq_manifest_hash_drift` negative gate在focused/full中继续通过。

CodeGraph确认seam继续只组合现有owners：successor拥有bundle/public/final/strict，provenance拥有root/inventory/exact read/canonical/
same-target，thermal拥有policy/R6/machine semantics；没有新增serializer、writer、controller或device/process owner。

## 4. Exact G4-01 real-bundle single read-only call

在所有pre-real gates通过后，只对PLAN冻结路径调用`evaluate_successor_predevice`一次；exit 0，未重跑：

```text
bundle = /Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release
bundle device/inode/mode = 16777244 / 2478933 / 0700
public = public_descriptor_semantic_pass
final_replay / strict / lineage = pass / pass / pass
public / final / strict call counts = 1 / 1 / 1
artifact_count = 5
R6 executable / logical / physical / setup / ambient / launch / retry = false / 16 / 16 / 0 / 0 / 1 / 0
state shutters A/D/B/C = 1/5000 / 1/6400 / 1/8000 / 1/2500
old_new_frame_combination = prohibited
operational = 600 / selected_fixed_time_transient_not_proven_steady / not_demonstrated
locks = strip blocked / TD-C blocked / sentinel true / P8 true
```

五个artifact bytes/SHA、source HEAD/checkpoint/tree、policy path/bytes/SHA、EQ reference bytes/SHA均与PLAN冻结值exact。Oracle未遍历
EQ root，未读取retained R3、R2或其他external payload。

Proposal仅为Planner/Orchestrator待审建议：

```text
canonical_validator_success = true
eligibility = true
release_consumable = true
release_consumption_authorized = false
scope = exact_g4_01_release_only_waiting_planner_and_orchestrator
```

本包effective authority保持：canonical validator success、eligibility、release consumable、release consumption authorization以及
device/camera/Ray/strip/capture/formal R6/TD-C全部`false`；retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`。

## 5. Scope与zero ledger

最终dirty classification仍为PLAN冻结的7 paths：Planner/Orchestrator-owned PLAN、FULL与两个1155 archives；Executer-owned
production candidate、test与本ER。除test fixture和ER外，本V2 Executer未修改任何文件。

```text
real G4-01 bundle production-owner invocation = 1
durable/external predevice root creation = 0
release consumption = 0
retained R3 / R2 / other external payload access = 0 / 0 / 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
production API edits = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits by Executer = 0
commit/amend/stage/push = 0
Terminal/background/automation = 0
```

请求Planner在唯一stop `RETURN_FOR_G4_02_PREDEVICE_BOUNDED_FIXTURE_CORRECTION_REVIEW`验收owner integration与read-only
observation。不得在本结果上直接建立durable root或激活G4-03；若接受，先由Orchestrator建立focused clean checkpoint。
