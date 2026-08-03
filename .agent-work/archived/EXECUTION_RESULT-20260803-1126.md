# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED_G4_01_FRESH_SUCCESSOR_RELEASE`
- archived_at: `2026-08-03T11:26:18-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-01-SUCCESSOR-LINEAGE / fresh successor release v2 generation and validation`
- source_checkpoint: `779c7d9572d991f82076c892ec8198a059bbe44e`
- original_body_bytes: `9317`
- original_body_sha256: `7fdd375928f5af1da81ffd429b8f2a1750fe44ea458609cc49160d7a32fd4cd0`
- terminal_disposition: `ACCEPTED_G4_01_SUCCESSOR_RELEASE_GENERATED_VALIDATED_NON_AUTHORIZING_UNCONSUMED`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1126.md`
- external_evidence_family: `/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z`
- exact_next_stop: `RETURN_ORCHESTRATOR_ARCHIVE_FULL_RETIRE_G4_01_AND_PREPARE_G4_02_PLANNING`
- historical_non_executable: `true`

该archive只证明G4-01 fresh successor candidate已生成并完成offline public/final/strict validation；它不授权release
consumption、eligibility、device、camera、Ray、strip、formal R6、TD-C、retry、stage entry、budget或commit。下方为逐字节
保留的reviewed Executer handoff body。

---

# REF-G4-01-SUCCESSOR-LINEAGE：fresh successor release v2 handoff

**状态：** `SUCCESS_CANDIDATE_NON_AUTHORIZING_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V2`

**Reference task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Planner stop：** `RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_V2_REVIEW`

## 1. Result与credit边界

唯一fresh successor family与其single production `release` child已由accepted repo-owned production defaults成功生成。
Compose内部public/final/strict各exactly once并全部通过；post-compose只做一次returned-identity驱动的non-semantic
read-only audit。

该结果只表示一个`candidate_non_authorizing` bundle的离线identity/semantic replay通过。它不表示release usable、
production ready、hardware ready、eligibility、consumption authorization或formal pass；不自行解锁G4-02。

## 2. Activation、source与machine contract

```text
activation HEAD = 779c7d9572d991f82076c892ec8198a059bbe44e
activation tree = 1ead5268917612d1232543b1a7eca28788f3980c
parent = fbc3b166b81f0ea7eee79fdacb37a958e1cbd03c
subject = docs(plan): activate g4 fresh release after seam fix
branch = main
pre-execution worktree = clean
production source staged / unstaged / untracked / clean = false / false / false / true
```

Activation changed-path set exact：

```text
.agent-work/EXECUTION_RESULT.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/PLAN.md
.agent-work/archived/EXECUTION_RESULT-20260803-1111.md
.agent-work/archived/PLAN-20260803-1111.md
```

`build_successor_lineage_inputs`内部production default `provenance.read_git_source_identity`证明
HEAD/checkpoint/tree exact并绑定clean source。Repo-owned parser在执行前后返回：

```text
PLAN/FULL contract = G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V2
PLAN/FULL active count = 1 / 1
active task = REF-G4-01-SUCCESSOR-LINEAGE
canonical next = REF-G4-01-SUCCESSOR-LINEAGE
```

## 3. Reviewed archive replay

| archive | bytes | SHA-256 | body bytes | body SHA-256 |
| --- | ---: | --- | ---: | --- |
| `.agent-work/archived/PLAN-20260803-1111.md` | 6464 | `b49dafbda43d561d8932f508ac836f14ebd4de0952fcb55f4ee7af97234a40ad` | 5480 | `514db1c07677910f8dc00ff4cb09f6d458358f3a02a10089c58c17e92cc9d3bc` |
| `.agent-work/archived/EXECUTION_RESULT-20260803-1111.md` | 2087 | `02151d66e914a7b22376af8353a4a6f82bfa71571089af806f33b4ad0bbf7bca` | 1105 | `7274408e90d8fa9676b50a1fd54f2ef0f8e7ee8de39906e3d63708cda78a211d` |

两个archive均为regular non-symlink，metadata/body replay exact。Accepted EQ与post-EQ archives亦分别以
25296/`bf48528e...03f7`和17030/`6dd605a8...1762`通过identity检查。

## 4. Frozen owner、policy与EQ evidence

Owner/test/delegate hashes exact：

| path | SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py` | `8485755619ee6cee11845ff0ca698a8fff0906ff42537b3039ce5b8358fc1555` |
| `tests/test_p7_successor_lineage.py` | `8d825cdaddf5135435c45d4752ac0478436a05904f602799f4e40155d7665af7` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608` |
| `tests/test_p7_retained_r3_provenance_io.py` | `21f47535106937f2f99acdece8b3fb5c6717e1f9900f974e60b0f744163d34c6` |
| `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | `14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1` |

Successor/test相对accepted seam checkpoint `a8e006e40822a5e1f8782be923e5b2a6f17f4a96`无diff；provenance/test相对
accepted owner checkpoint `2e8eeb59bac43bb437bbfcd3a266fca924e2ceae`无diff。

Production input facts：

```text
policy path = /Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json
policy bytes = 4065
policy SHA-256 = c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
EQ root = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
manifest schema = planner_eq_family_manifest_v1
entries/files/directories/symlinks/other = 47/42/5/0/0
manifest payload bytes = 7980
manifest SHA-256 = 41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
qualification/status/shutter = qualified_1_2500 / qualified_1_2500 / 1/2500
candidate launch/candidate2/attempted/physical/accepted/retry = 1/0/4/4/4/0
```

Operator显式调用`build_planner_eq_family_manifest`exactly once。Production-default EQ audit内部按既有owner合同
必要地re-derive manifest一次；按Orchestrator确认的cap解释，记录为：top-level invocation `1`、internal owner
re-derivation `1`、overall production derivations `2`。没有wrapper、cache、fake、adapter或retry。

`build_successor_lineage_inputs`exactly once且所有owner/delegate使用production defaults；它在UTC/root0状态通过：

```text
R6 status = selected_exposure_policy_non_executable
C shutter = 1/2500
formal logical / physical = 16 / 16
setup / ambient / launch / retry = 0 / 0 / 1 / 0
old/new pooling = prohibited
machine locks = strip/TD-C/sentinel/P8 unchanged
```

## 5. Unique family与root identities

Build完整通过后exactly once采样UTC：

```text
timestamp = 20260803T172055Z
FAMILY_ROOT = /Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z
BUNDLE_ROOT = /Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release
```

两个path均absent-before。Container保持`0755`，没有冒充safe parent。Production
`create_exclusive_root`exactly once创建family，compose内部`create_exclusive_direct_child`exactly once创建release：

```text
family device/inode/mode = 16777244 / 2478932 / 0700
family direct children = [release]
bundle device/inode/mode = 16777244 / 2478933 / 0700
```

未创建alternate family、parallel release或临时artifact。

## 6. Five artifact identities

Production order exact：

| artifact | bytes | SHA-256 | mode |
| --- | ---: | --- | --- |
| `frozen-inputs.json` | 5047 | `8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8` | `0600` |
| `r6-formal-plan.json` | 899 | `dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b` | `0600` |
| `release-descriptor.json` | 2024 | `6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452` | `0600` |
| `validation-summary.json` | 432 | `07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07` | `0600` |
| `terminal-seal.json` | 808 | `d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850` | `0600` |

Returned root/file identities驱动的单次audit证明：每项regular non-symlink、same target、bytes/SHA/mode exact、canonical
JSON decode成功；inventory只有上述五项，无extra/tmp。Inventory lexical order为
`frozen-inputs, r6-formal-plan, release-descriptor, terminal-seal, validation-summary`，而artifact production/order contract
仍为表中五项顺序。

## 7. Compose、validator与cross-artifact result

```text
compose invocations = 1
public / final / strict = 1 / 1 / 1
public status = public_descriptor_semantic_pass
final replay = pass; artifact_count = 5
strict validation = pass; artifact_count = 5
descriptor status = candidate_non_authorizing
terminal status = sealed_non_authorizing_pending_independent_replay
```

Source HEAD/checkpoint/tree、policy reference、EQ manifest reference与R6 plan全部和§2/§4 exact一致。Terminal references
exact first four artifacts且无terminal self-reference。Final/strict均只由compose内部调用，外层没有第二validator。

Authority across descriptor/summary/terminal保持：

```text
retained_r3_status = RETAINED_UNVALIDATED_UNCONSUMED
release_consumable = false
release_consumption_authorized = false
eligibility = false
device_authorized = false
formal_r6_authorized = false
```

## 8. Validation inheritance、repo diff与zero ledger

Accepted seam validation因source/test hashes byte-exact而继承：targeted `47/47`、focused `115/115`、full
`846/846`、compile/static/CodeGraph/diff PASS。本docs/external-artifact package没有改code/test，故full suite、compile、
CodeGraph sync invocation均为0。

Production invocation前后均证明owner/test/config/GUIDE/RESEARCH无diff；PLAN/FULL/archive未改。写ER前worktree clean，
`git diff --check` PASS；最终tracked diff应只有`.agent-work/EXECUTION_RESULT.md`。

```text
top-level manifest / internal re-derive / build inputs = 1 / 1 / 1
UTC sample / family root / bundle root / compose = 1 / 1 / 1 / 1
retry / fallback / repair / alternate root = 0 / 0 / 0 / 0
release consumption / retained R3 / legacy release = 0 / 0 / 0
other external experiment root access = 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
code/test/config/docs/skill edits = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits = 0
commit/amend/stage/push = 0
background process / Terminal long task / automation = 0 / 0 / 0
```

## 9. Planner decision request

请Planner在唯一stop `RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_V2_REVIEW`验收这个exact
`candidate_non_authorizing` fresh release，并决定同一`REF-G4-01-SUCCESSOR-LINEAGE`是否已满足GUIDE lineage release gate。
不得由本ER自动设eligibility/consumable、消费release、解锁G4-02或授权任何device/formal stage。
