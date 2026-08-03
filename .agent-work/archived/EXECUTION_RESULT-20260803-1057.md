# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_ZERO_ROOT_REPRESENTATION_SEAM`
- archived_at: `2026-08-03T10:57:45-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-01-SUCCESSOR-LINEAGE / G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V1`
- source_checkpoint: `b2ec3b0807841bb2e42ca928ce65615d4a704f9f`
- original_body_bytes: `7208`
- original_body_sha256: `90b791591cabba8423489ea46a420552df226e9389e5c0650f06f3ba9536028e`
- terminal_disposition: `REJECTED_ZERO_ROOT_JSON_NATIVE_REPRESENTATION_SEAM_BOUNDED_CORRECTION`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1057.md`
- exact_next_stop: `SAME_FLAT_REF_G4_01_BOUNDED_JSON_NATIVE_PROJECTION_CORRECTION`
- historical_non_executable: `true`

该archive不授权release generation/consumption、root creation、device、formal、retry、stage entry、budget或commit。下方为
逐字节保留的reviewed ER body；zero-root counters、first-failure evidence与authority zeros不改写。

---

# REF-G4-01-SUCCESSOR-LINEAGE：fresh successor release generation failure handoff

**状态：** `FAIL_CLOSED_ZERO_ROOT_POLICY_VALIDATOR_NATIVE_TYPE_CONTRACT`

**Reference task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**PLAN contract：** `G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V1`

**Planner stop：** `RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_REVIEW`

## 1. Terminal disposition

Activation/source/archive/owner identity preflight通过；在任何UTC采样、external root创建或production
`build_successor_lineage_inputs`调用之前，accepted policy的PLAN-required strict decode + production validation seam
fail closed：

```text
ValueError: in-memory TD-B exposure policy differs from the repository owner
```

Policy file identity本身精确匹配。失败来自production owner之间的JSON-native representation contract：
`provenance.decode_strict_json_bytes`返回冻结的`mappingproxy`/nested tuple representation；
`thermal.validate_td_b_exposure_policy_v2`只做`dict(policy) != owner`的shallow conversion，因此nested frozen
mapping/sequence与owner loader返回的ordinary dict/list不相等。当前successor input测试注入fixture validator，未覆盖这条
production-default integration seam。

本PLAN不授权bounded correction、retry、fallback、repair或alternate root，因此没有创建release。该故障是普通
serialization/validation owner integration问题，不是scientific contradiction，不需要Advisor解释，也不需要Human高危授权。

## 2. Activation与clean source evidence

```text
activation HEAD = b2ec3b0807841bb2e42ca928ce65615d4a704f9f
activation tree = 266148f0aa88cb1b752707ab9febe367174f47a6
parent = 8b8f50c10dec5864c204e90d33cb39468b45ce51
subject = docs(plan): activate g4 fresh successor release
branch = main
source staged / unstaged / untracked / clean = false / false / false / true
```

Activation changed-path set exact：

```text
.agent-work/EXECUTION_RESULT.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/PLAN.md
.agent-work/archived/EXECUTION_RESULT-20260803-1041.md
.agent-work/archived/PLAN-20260803-1041.md
```

`provenance.read_git_source_identity(repo_root, activation HEAD)`成功绑定HEAD/checkpoint/tree与clean ledger，未绕过
production Git owner。

## 3. PLAN/FULL与archive replay

Repo-owned machine parsers返回：

```text
PLAN contract = G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V1
PLAN active count / task / executable = 1 / REF-G4-01-SUCCESSOR-LINEAGE / true
FULL contract = G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V1
FULL active count / task = 1 / REF-G4-01-SUCCESSOR-LINEAGE
FULL canonical next = REF-G4-01-SUCCESSOR-LINEAGE
```

Reviewed archive identity/body replay均精确：

| path | bytes | SHA-256 | body bytes | body SHA-256 |
| --- | ---: | --- | ---: | --- |
| `.agent-work/archived/PLAN-20260803-1041.md` | 6744 | `31861823a47cb72812e371bc564a893985af5ca7c7634eb4c0ec08f7506ead82` | 5700 | `742f3d4e27e984b2dc635ecc6e56fec4cd3b967a8787523de298eed1cc562093` |
| `.agent-work/archived/EXECUTION_RESULT-20260803-1041.md` | 2191 | `6781033283ad533f078fde23994bf8dbf9e5b1ddc5fff2efc195604ed18dbb2b` | 1149 | `caae77f59091a9a36a0077bb4b2b25e998f0fba5488d66154f21f5d92d74be23` |

Accepted archive identities亦精确：

```text
.agent-work/PLANS/20260727-2052-p7-post-eq-policy-c1e1-acceptance-review.md
  17030 bytes / 6dd605a8d5f142d8fb50cc9a40020e6a816cc116581cccb414459f6c91cc1762
.agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
  25296 bytes / bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7
```

## 4. Frozen owner/policy/EQ checks

Activation tree上的accepted owner/test/delegate/GUIDE hashes全部精确；四个owner/test paths相对
`2e8eeb59bac43bb437bbfcd3a266fca924e2ceae`为empty diff：

| path | SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py` | `a944cc8d6186f8659848e89f30388f4a5112e18ed2dc6ea6fa1aec50ff95ff33` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608` |
| `tests/test_p7_successor_lineage.py` | `bf2c3f36e5df7f78b4e607181bb8194bd6d589979ff9022af4060c69640780e4` |
| `tests/test_p7_retained_r3_provenance_io.py` | `21f47535106937f2f99acdece8b3fb5c6717e1f9900f974e60b0f744163d34c6` |
| `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` | `14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1` |
| `advisor/4/4.GUIDE.md` | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |

Policy production identity read成功：

```text
path = /Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json
bytes = 4065
SHA-256 = c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
strict decoded top type = mappingproxy
production validator result = FAIL (exact ValueError above)
```

Accepted EQ root只做no-follow root identity/mode preflight：exact path、real directory、non-symlink、mode `0700`。
因为policy seam先失败，未调用`thermal.build_planner_eq_family_manifest`，未运行production EQ audit，未遍历、复制、
修改EQ payload，也未访问任何其他external root。

## 5. Invocation与root counters

```text
UTC timestamp samples = 0
family root acquisition = 0
bundle root acquisition = 0
FAMILY_ROOT created = false
BUNDLE_ROOT created = false
EQ manifest builder = 0
production build_successor_lineage_inputs = 0
production compose_successor_lineage_bundle = 0
public / final / strict = 0 / 0 / 0
retry / fallback / repair / alternate root = 0 / 0 / 0 / 0
artifact count = 0
```

因此没有五artifact identity、candidate descriptor或terminal seal可验收；这不是failed release root，而是
zero-root input-owner stop。

## 6. Authority与validation state

FULL machine state保持：

```text
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
eligibility = false
release consumable = false
release consumption authorized = false
device authorized = false
formal R6 authorized = false
```

未进行release consumption、retained R3/legacy release读取、device/network/camera/Ray/strip/capture、formal R6、
public experiment analyzer、TD-C、firmware或deployment操作。没有后台进程、Terminal long task或automation。

代码/test/config/GUIDE/RESEARCH/PLAN/FULL/archive均未修改。Inherited accepted validation仍为targeted 45/45、
focused 83/83、full 844/844、compile/static/CodeGraph/diff scope PASS，证据位于
`.agent-work/archived/{PLAN,EXECUTION_RESULT}-20260803-1033.md`；本次source tree未改，未重跑full suite。

## 7. Planner decision request

请Planner在唯一stop `RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_REVIEW`拒绝本次fresh release execution result，并把
exact ordinary-engineering decision交回Orchestrator：需要在同一`REF-G4-01-SUCCESSOR-LINEAGE`内修复
strict-decoder frozen representation与production policy validator的JSON-native equality seam，并补充保留production
defaults的integration regression test。不得创建corrective suffix、不得生成新root、不得解锁G4-02或任何设备/formal阶段。
