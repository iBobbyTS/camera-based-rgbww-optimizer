# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED_G4_02_DURABLE_OFFLINE_ORACLE`
- archived_at: `2026-08-03T12:59:06-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-02-PREDEVICE / repo-owned-name durable package`
- source_checkpoint: `79b8f03e65107e1d62f8de3b33ffb31d3413e185`
- original_body_bytes: `6457`
- original_body_sha256: `2e70137282284223f4fc842684183448989b54a05bede8d8355e6344632b2cf9`
- terminal_disposition: `ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1259.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_TERMINAL_FULL_UPDATE_AND_FOCUSED_COMMIT_G4_03_PLANNING_ONLY`
- historical_non_executable: `true`

该archive不授权release consumption、device、formal、G4-03 execution、retry、stage entry、budget或commit。下方逐字节保留
reviewed ER body。

---

# REF-G4-02-PREDEVICE：repo-owned artifact-name durable package handoff

**状态：** `DURABLE_OFFLINE_ORACLE_PASS_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-REPO-OWNED-NAMES-V3`

**Reference task：** `REF-G4-02-PREDEVICE`

**Planner stop：** `RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`

## 1. 结论

V3 intake、pre-call gates、repo-owned artifact-name tuple assertions、唯一 production persist 和唯一 independent replay
全部通过。Durable offline oracle package已经由production owner写入冻结的fresh root，并由repo-owned replay owner独立
重放为`pass`。

本结果只构成`REF-G4-02-PREDEVICE`的non-authorizing candidate evidence。Executer不授予canonical validator
success、eligibility或release consumable；这些只能由Planner review和Orchestrator状态更新决定。Release consumption和全部
device/formal authority继续为false。

## 2. V3 intake

- PLAN/FULL strict machine parser：PASS。
- PLAN/FULL contract：
  `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-REPO-OWNED-NAMES-V3`。
- PLAN/FULL active task：`REF-G4-02-PREDEVICE`，count `1/1`。
- dirty path set：冻结的9 paths exact一致。
- durable root pre-call：`os.path.lexists(...) = false`。
- production candidate：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py
  24232 bytes
  4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81
```

- test candidate：

```text
tests/test_p7_successor_predevice.py
  29738 bytes
  44ac81ae18ae0a8f041d53837c4c7d6c4e867cf4761c616bfb640117550d4cfa
```

- reviewed archives：

```text
.agent-work/archived/PLAN-20260803-1249.md
  11968 bytes / 534952f547a4cf5c0302e7cc97c355098dab426eb27fff09e487f96d5e4ad39d
  body: 10990 bytes / 3b04cb4d1a0977f64f750eef1d73a3fb2614914dee6c93a2fb518af991810e9d
.agent-work/archived/EXECUTION_RESULT-20260803-1249.md
  6882 bytes / 2a04d70deeecbe9beacbec43d991dfcf9d3496603f24287c99eb0c23da235e61
  body: 5901 bytes / bea5eb5e277942834a48a1811b736d4287039b8c5f4477a0aa07665cc897c8e6
```

## 3. Inherited fresh validation与pre-call复核

按V3 PLAN继承同一execution内且经Planner review接受的fresh evidence：

```text
targeted = 18/18 PASS
focused = 133/133 PASS
full = 864/864 PASS
full_seconds = 146.475
compileall = PASS
codegraph sync = PASS
codegraph explore = PASS
git diff --check = PASS
```

本V3没有重跑上述suite。Persist前再次核验：

```text
production bytes/SHA-256 = exact
test bytes/SHA-256 = exact
git diff --check = PASS
durable root lexists = false
```

V3 code edits：`0`；test edits：`0`。

## 4. Repo-owned artifact-name construction

Thin caller只import并消费：

```text
camera_based_rgbww_optimizer.optimization.p7_successor_lineage.ARTIFACT_NAMES
```

Caller中的artifact filename literal count：`0`。Caller只冻结五组ordered `(bytes, sha256)` facts，并执行：

```text
len(repo_owned_names) == len(facts) == 5 = PASS
zip(repo_owned_names, facts, strict=True) = PASS
tuple(constructed item names) == repo_owned_names = PASS
tuple(constructed bytes/SHA facts) == frozen facts = PASS
```

Assertions全部在persist调用前完成。没有定义、复制、替换、fallback或从archive/ER解析artifact名称；没有生成JSON/
seal bytes，没有实现filesystem或validator owner。

## 5. Durable package identities

Root：

```text
path   /Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z
device 16777244
inode  2495492
mode   0700
```

Artifacts：

```text
predevice-oracle-result.json
  device 16777244
  inode  2495493
  mode   0600
  bytes  3186
  sha256 78fa982b7f318734afc158324b968ee71ff41b5ce7b91e27d6eabc0f60bc40d9

terminal-seal.json
  device 16777244
  inode  2495494
  mode   0600
  bytes  1114
  sha256 39456ca3379df45cae0ca5337bf6d24d2040e6581dcd074b8ebf12d39b87e68e
```

上述root/artifact均由production owner创建与持久化；thin caller没有直接filesystem write。Persist成功后仅把返回的
package对象交给repo-owned replay一次，没有手工读取或解释payload。

## 6. Closed replay result

```text
schema = g4_successor_predevice_evidence_replay_v1
status = pass
result_status = pass
artifact_count = 2
independent_replay_calls = 1
retry = 0
release_consumption = 0
root identity = exact package root identity
artifact identities = exact package result/terminal identities
```

Call ledger：

```text
persist_successor_predevice_evidence attempts = 1
evaluate_successor_predevice entries <= 1
durable root create calls <= 1
replay_successor_predevice_evidence calls = 1
retry = 0
alternate root count = 0
```

## 7. Proposal与effective authority

Production result通过其closed validation，可以提交以下candidate proposal给Planner：

```text
proposed canonical_validator_success = true
proposed eligibility = true
proposed release_consumable = true
proposed release_consumption_authorized = false
scope = exact_g4_01_release_only_waiting_planner_and_orchestrator
```

Replay证明当前effective authority仍为：

```text
canonical_validator_success = false
eligibility = false
release_consumable = false
release_consumption_authorized = false
retained_r3_status = RETAINED_UNVALIDATED_UNCONSUMED
device_authorized = false
camera_authorized = false
ray_authorized = false
strip_authorized = false
capture_authorized = false
formal_r6_authorized = false
td_c_authorized = false
```

## 8. Exact zero ledger与locks

```text
release consumption = 0
retained R3 access = 0
legacy R2 access = 0
other external experiment payload access = 0
device access = 0
network access = 0
camera access = 0
Ray access = 0
strip access = 0
capture access = 0
formal R6 access = 0
TD-C access = 0
firmware access = 0
deployment access = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits by Executer = 0
commit/stage/push = 0
```

EQ root未遍历。`REF-G4-03-REAL-ZERO-READINESS`仍locked；Executer未创建task suffix、alternate root、PLAN或
commit。

## 9. Planner decision request

请Planner review：

1. exact root/artifact identities与closed replay result；
2. repo-owned artifact-name derivation及single-attempt/no-retry contract是否满足；
3. 是否接受candidate proposal并把`REF-G4-02-PREDEVICE`置于terminal accepted disposition；
4. 是否归档本PLAN/ER并返回Orchestrator，让Orchestrator决定FULL状态和唯一下一包。

Executer已到达唯一Planner stop，不会消费release或进入G4-03。
