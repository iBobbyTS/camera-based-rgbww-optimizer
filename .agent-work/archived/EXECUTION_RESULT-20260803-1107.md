# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED_JSON_NATIVE_INTEGRATION_SEAM`
- archived_at: `2026-08-03T11:07:54-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-01-SUCCESSOR-LINEAGE / G4-SUCCESSOR-LINEAGE-JSON-NATIVE-PROJECTION-CORRECTION-V1`
- source_checkpoint: `796f69aa9a011903a56da8bb60d45cc6ad10a2bd`
- original_body_bytes: `7849`
- original_body_sha256: `66897e61cd546e34ab023b0d18bca812f9d4f5dffb8ec33278f30749e693631d`
- terminal_disposition: `ACCEPTED_JSON_NATIVE_PROJECTION_INTEGRATION_SEAM_ONLY_NO_RELEASE_CREDIT`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1107.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_FOR_FOCUSED_CODE_TEST_CHECKPOINT_AND_SAME_G4_01_FRESH_RELEASE_REPLAN`
- historical_non_executable: `true`

该archive不授权release generation/consumption、root creation、device、formal、retry、stage entry、budget或commit。下方为
逐字节保留的reviewed ER body；test/log/hash/zero-side-effect evidence不改写。

---

# REF-G4-01-SUCCESSOR-LINEAGE：JSON-native projection correction handoff

**状态：** `IMPLEMENTED_VALIDATED_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-SUCCESSOR-LINEAGE-JSON-NATIVE-PROJECTION-CORRECTION-V1`

**Reference task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Planner stop：** `RETURN_FOR_G4_01_JSON_NATIVE_PROJECTION_CORRECTION_REVIEW`

## 1. Result

同一`REF-G4-01-SUCCESSOR-LINEAGE`内的首次bounded correction已完成。Composition owner现在在strict decode与
top-level `Mapping` gate之后，exactly once调用既有
`provenance.json_native_value(decoded_policy)`。得到的同一个ordinary `dict/list`对象依次交给production
`validate_policy_fn`与`build_r6_plan_fn`，并作为`frozen["policy_contract"]`的输入；最终
`SuccessorLineageInputs`仍由既有`_freeze`变成immutable mappingproxy/tuple output。

未使用shallow `dict()` compatibility、JSON round-trip、parallel adapter/controller或新helper/module；未修改
provenance owner或thermal巨型模块。

## 2. Activation与machine contract

Activation intake全部通过：

```text
HEAD = 796f69aa9a011903a56da8bb60d45cc6ad10a2bd
tree = 321c0f472fd1df814e56e26f9f6a7a98439bd256
parent = b2ec3b0807841bb2e42ca928ce65615d4a704f9f
subject = docs(plan): activate g4 json-native seam correction
branch = main
worktree before execution = clean
```

Activation changed paths exact：

```text
.agent-work/EXECUTION_RESULT.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/PLAN.md
.agent-work/archived/EXECUTION_RESULT-20260803-1057.md
.agent-work/archived/PLAN-20260803-1057.md
```

Repo-owned parsers在执行前后均证明：

```text
PLAN/FULL contract = G4-SUCCESSOR-LINEAGE-JSON-NATIVE-PROJECTION-CORRECTION-V1
PLAN/FULL active task count = 1 / 1
active task = REF-G4-01-SUCCESSOR-LINEAGE
canonical next = REF-G4-01-SUCCESSOR-LINEAGE
```

## 3. Reviewed archive replay

| archive | bytes | SHA-256 | body bytes | body SHA-256 |
| --- | ---: | --- | ---: | --- |
| `.agent-work/archived/PLAN-20260803-1057.md` | 20233 | `f8daec91b1c41b6a4686511869c18be3b1feea06291e6b88a118e61701d16f7d` | 19179 | `8ee8f364b3f551df024295b631ad3768efbb6b2dfd66593a196dfb8e062f9f10` |
| `.agent-work/archived/EXECUTION_RESULT-20260803-1057.md` | 8260 | `9f446dbfdef2040147db504a61c85f92ca95f718be52e1fb1cc377c74a8aab8e` | 7208 | `90b791591cabba8423489ea46a420552df226e9389e5c0650f06f3ba9536028e` |

Archive均为regular non-symlink，metadata与body replay exact。上一zero-root failure未改写为release attempt或科学失败。

## 4. Maintainability与CodeGraph preflight

CodeGraph在修改前确认single owner chain：

```text
decode owner = provenance.decode_strict_json_bytes
native projection owner = provenance.json_native_value
consumer owners = thermal.validate_td_b_exposure_policy_v2 / thermal.build_td_b_r6_formal_plan
composition owner = successor.build_successor_lineage_inputs
```

缺陷位于composition seam；直接修改thermal巨型P7模块会错误扩大owner边界，因此保持其byte-exact不变。既有
provenance native projection是persistence/serialization单一source of truth，也保持不变。

## 5. Exact implementation diff

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
  +8 / -5
  26438 bytes
  SHA-256 8485755619ee6cee11845ff0ca698a8fff0906ff42537b3039ce5b8358fc1555
tests/test_p7_successor_lineage.py
  +92 / -0
  24526 bytes
  SHA-256 8d825cdaddf5135435c45d4752ac0478436a05904f602799f4e40155d7665af7
```

Production behavior：

1. `decoded_policy = decode_policy_fn(...)`保留immutable decoded value；既有non-Mapping
   `policy_not_object` precedence不变。
2. `native_policy = provenance.json_native_value(decoded_policy)`在builder内显式出现exactly once。
3. `validate_policy_fn(native_policy)`与`build_r6_plan_fn(native_policy)`收到exact同一个对象。
4. `policy_contract`复用该对象；不存在第二次显式projection。
5. `_freeze`输出仍为mappingproxy/nested tuple，输入decoded object未改变。

## 6. Required regression evidence

新增真实行为回归覆盖：

- 使用tracked exact absolute
  `/Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json`，4065 bytes，
  SHA-256 `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`；
- `read_exact_file_fn`、`decode_policy_fn`、`validate_policy_fn`、`build_r6_plan_fn`均保留production defaults；只用
  bounded clean-source、EQ audit与machine-status fakes隔离Git/EQ/device；
- real policy seam通过，C=`1/2500`、capture count `16`、formal logical/physical=`16/16`、plan
  `executable=false`、policy path/bytes/SHA exact；
- immutable nested mappingproxy/tuple input只投影一次；validator与plan builder获得exact同一ordinary `dict`对象，
  nested sequence为`list`；
- original decoded input type/content不变；returned policy contract仍为mappingproxy/nested tuple且mutation抛
  `TypeError`；其JSON-native语义与原输入相等；
- AST assertion证明builder内显式`provenance.json_native_value` call count exact `1`。

现有source/policy/EQ drift、old-route、R6 drift、integrity/reference、error precedence、terminal-last与failure-seal
测试均继续通过。

## 7. Validation ledger

所有授权检查均只运行一次，无失败后重试：

| check | exact result |
| --- | --- |
| targeted：successor + provenance owner | `47/47 PASS` |
| focused：successor + provenance + `test_p7_td_b_r6_contract` | `115/115 PASS` |
| compile changed source/test | `PASS`，两文件in-memory compile |
| AST/static | `PASS`，显式projection=1、same-object consumers exact、forbidden imports absent |
| full unittest discovery | `846/846 PASS` |
| static discovery count（不执行tests） | `846` |
| CodeGraph sync | `PASS`，exactly once，2 changed files / 109 nodes |
| CodeGraph query | `PASS`，decode → native projection → validate/build → frozen contract，无parallel owner |
| `git diff --check` | `PASS` |
| added secret/historical markers | `ABSENT` |

Full suite详细`-v`输出超过tool展示预算，但foreground process成功terminal；未重跑。Exact count由同一当前tree的
`unittest.defaultTestLoader.discover('tests').countTestCases()`只加载统计为846，没有执行第二次full suite。

## 8. Protected scope与zero-authority ledger

相对activation HEAD，最终允许的tracked diff path只应为：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py
tests/test_p7_successor_lineage.py
.agent-work/EXECUTION_RESULT.md
```

下列路径保持无diff：

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
config/
advisor/4/4.GUIDE.md
advisor/4/4.RESEARCH.md
.agent-work/PLAN.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/archived/
all other tests/source
```

Zero counters：

```text
release family/root generation = 0
public/final/strict real validator invocation = 0/0/0
release consumption / retained R3 / legacy release = 0/0/0
external experiment root access = 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
commit/amend/stage/push by Executer = 0
corrective task ID / new root = 0/0
background process / Terminal long task / automation = 0/0/0
```

## 9. Planner decision request

请Planner在唯一stop
`RETURN_FOR_G4_01_JSON_NATIVE_PROJECTION_CORRECTION_REVIEW`验收本bounded correction。成功只表示
JSON-native projection owner seam candidate可接受；不得把它表述为release generation/validation、G4-01 terminal
completion、G4-02 unlock、eligibility、hardware readiness或formal authorization。后续仍须由Orchestrator独立审查、
focused commit并为同一`REF-G4-01-SUCCESSOR-LINEAGE`委派新的fresh release generation package。
