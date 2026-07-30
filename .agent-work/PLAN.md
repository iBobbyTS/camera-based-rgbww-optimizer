# REF-P7-25-R2-B2：corrected exact-path modern manifest seal

**计划状态：** `EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2`（接受
`REF-P7-25-R2-B2-C1` 后返回的唯一分支）

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3`

**预计时长：** `2–6 分钟`；不得运行tests/full/synthetic或任何设备任务，不属于预计超过10分钟的长任务。

**当前唯一动作：** Executer以一个本地Python controller、一次invocation和一个brand-new external root，先验证并消费C1 exact
path-owner index及其双seal，再对index解析出的三个exact retained artifacts各执行一次non-following lstat/open/read/hash，重算完整现代
accepted Git/provenance baseline，exclusive-create并durably seal唯一subordinate immutable v2 manifest、manifest seal、terminal及terminal
seal；随后只向`.agent-work/EXECUTION_RESULT.md` append一次并停Planner验收。

**Planner stop：** `B2_CORRECTED_MANIFEST_SEALED_WAITING_PLANNER_REVIEW`。成功也不得运行B3、canonical validator、eligibility、release、
设备或scientific route。

**C1 review archive：**
`.agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md`，bytes
`7795`，SHA-256
`d9fdec1891c9e251df2fa264eda615abbabe5d6b0a9bde2be67b650652917f34`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_corrected_path_manifest_plan_v3","reference_task_id":"REF-P7-25-R2-B2","accepted_corrective_task_id":"REF-P7-25-R2-B2-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3","dispatch_state":"execution_authorized","execution_authorized":true,"single_current_action":"single_controller_consume_exact_c1_index_and_seal_corrected_subordinate_manifest","activation_parent":"4587389e7ea8c0a0bfe7bb9edb70bc0712f5d182","activation_subject":"chore(plan): activate corrected b2 manifest seal","activation_changed_paths":[".agent-work/PLAN.md"],"activation_additional_paths":0,"activation_commit_count":1,"programmatic_dispatch_head_reads":1,"second_dispatch_head_reads":0,"dispatch_plan_sha256_owner":"sha256_of_exact_plan_blob_at_programmatic_dispatch_head","hand_transcribed_child_sha":false,"review_archive":{"path":".agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md","bytes":7795,"sha256":"d9fdec1891c9e251df2fa264eda615abbabe5d6b0a9bde2be67b650652917f34"},"accepted_path_owner_index":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/path-owner-index.json","bytes":12195,"sha256":"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35","resolved_paths":3},"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-corrected-manifest-b189117-20260730T1600Z","controller_invocations":1,"per_c1_evidence_lstat_open_read_hash":1,"per_retained_artifact_lstat_open_read_hash":1,"retained_artifacts":3,"manifest_writes":1,"manifest_seal_writes":1,"terminal_writes":1,"terminal_seal_writes":1,"canonical_validator_calls":0,"retry":0,"fallback":0,"planner_stop":"B2_CORRECTED_MANIFEST_SEALED_WAITING_PLANNER_REVIEW"}`

## 1. C1 acceptance and authority boundary

1. C1 is accepted only as path-owner and direct-entry type evidence. Its exact
   archive is the one named above. It does not validate retained artifact
   content and does not emit eligibility, consumability, release authority,
   device authority, or formal authority.
2. Exact accepted C1 evidence root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z`.
   Execution must consume these exact four immutable evidence files;
   each gets exactly one non-following lstat, one `O_RDONLY|O_NOFOLLOW` open,
   one read, and one SHA-256 computation:

   | File | Bytes | SHA-256 |
   | --- | ---: | --- |
   | `path-owner-index.json` | `12195` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` |
   | `path-owner-index.sha256.json` | `682` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` |
   | `terminal-evidence.json` | `13455` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` |
   | `terminal-evidence.sha256.json` | `772` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` |

3. The controller must strict duplicate-key/non-finite parse and canonical-byte
   verify all four; independently recompute both seal links; require exact
   schemas/statuses; require chain `3`, entry cardinality `10+1+3=14`, resolved
   path cardinality `3`, artifact-content counters all zero, and terminal
   lifecycle `index pre-write (0,0,0,0) -> terminal pre-write (1,1,0,0) ->
   terminal seal terminal_write_returned=true/self-not-attested`.
4. Resolved artifact paths must be derived from the accepted index and must
   equal the exact paths in section 4. The rejected B2 source path, basename
   fallback, directory search/listing, alternate root, sibling/parent
   enumeration, glob, walk, and path substitution are forbidden.
5. Retained state remains `RETAINED_UNVALIDATED_UNCONSUMED` until a later
   canonical owner says otherwise. This B2 package is subordinate provenance
   only and cannot make that decision.

## 2. Activated dispatch, single controller, and brand-new root

1. Activation direct parent is exact
   `4587389e7ea8c0a0bfe7bb9edb70bc0712f5d182`; subject is exact
   `chore(plan): activate corrected b2 manifest seal`; changed paths are exact
   `.agent-work/PLAN.md`, additional paths `0`, activation commit count `1`.
   Executer must read symbolic HEAD exactly once and verify from Git objects
   that the programmatic dispatch HEAD is that parent's direct child with the
   exact subject/path topology. The exact active PLAN SHA-256 is derived
   non-circularly from the `.agent-work/PLAN.md` blob at that programmatic
   dispatch HEAD and must equal working bytes; no PLAN-embedded expected hash,
   hand-transcribed child SHA, or second HEAD read is allowed.
2. Worktree must be clean before root creation. If not, stop before any evidence
   or retained-artifact access; Executer may not commit, repair, or clean it.
3. Exact brand-new root:
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-corrected-manifest-b189117-20260730T1600Z`.
   It must be absent immediately before the sole controller creates it once with
   mode `0700`. No precreation, reuse, rename, delete, repair, timestamp
   fallback, second root, or second controller is allowed.
4. One local Python controller process/invocation owns all reads, checks,
   canonical writers, fsyncs, and terminal evidence. Its exact source bytes and
   SHA-256 must be frozen before invocation and recorded; source must not be
   added to the repository.
5. `.agent-work/PLAN.md`, FULL, GUIDE, archives, source, tests, config, docs,
   skill, and wrappers are read-only. The only post-terminal repository change
   is one append to `.agent-work/EXECUTION_RESULT.md`; implementation edit and
   Git commit are `0/0`.

## 3. Exact modern accepted-integration baseline

The controller must recompute all facts from complete Git object IDs, never
trust self-reported manifest fields. For every named commit it binds full SHA,
direct parent, tree, exact subject, exact sorted changed paths, raw LF path
ledger SHA-256, before/after blob OIDs, blob bytes/SHA-256, canonical
binary-safe per-path patch SHA-256, and combined patch SHA-256. Any abbreviated
SHA, missing/extra path, or identity drift fails closed.

### 3.1 Historical helper and exact 181-path integration

- Historical helper v1 commit:
  `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; direct parent and rollback
  checkpoint `32b9e670ff3bbea0cd1505528c2ca87c2935446c`; exact subject
  `fix(p7): validate retained release terminal counts`; disposition
  `retained_release_audit_prerequisite_v1_superseded_before_real_validation`.
  Record `accepted_history=true`, `terminal_validation_prerequisite=false`,
  `superseded_by_exact_v2_repair=true`, `eligible_successor=false`,
  `release_consumable=false`, and `device_or_formal_authority=none`.
- Integration commit:
  `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`; parent exact `9303aa22...`;
  subject `chore(orch): consolidate p7 evidence and workflow state`; changed
  path count `181`; raw LF ledger SHA-256
  `9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`.
- Only these two selected paths receive scientific-audit-prerequisite
  classification:
  1. `src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py`,
     after SHA-256
     `48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8`,
     category `retained_release_validation_prerequisite_code`, scope
     `retained_R3_schema_validation_and_terminal_count_audit`;
  2. `tests/test_p7_retained_release_audit.py`, after SHA-256
     `c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f`,
     category `retained_release_validation_prerequisite_test`, scope
     `exact_helper_schema_owner_terminal_and_replay_regression`.
- Bind selected before/after identities, per-path patch digests, and selected
  combined patch. Record every other 179 path individually with disposition
  `present_in_commit_not_authorized_by_this_manifest`. Generic path, basename,
  directory, glob, descendant, prefix, or future-blob authorization is banned.

### 3.2 Exact canonical-seam integration chain

| Commit | Direct parent | Exact subject | Exact changed paths |
| --- | --- | --- | --- |
| `0682cd8763516dfb19a8e1ad48c53cb9934b9d19` | `4316d0ce84fea8e9c87f90069567a82238e7a733` | `fix(p7): validate exact governance lineage successor` | governance config; `p7_thermal_diagnostics.py`; dedicated test |
| `ba816216af9d37397873e054f44dbb7eea0f9b10` | `c0c51d9bc340da40ab5e95027e999962d2bd723e` | `fix(p7): separate historical lineage checkpoint ownership` | `p7_thermal_diagnostics.py`; dedicated test |
| `a9a817137969d9d2692fdd0b244d08e26e8a025d` | `d4f97a63e304cd78ebe26930907024805ce25102` | `test(p7): align canonical lineage classification expectations` | dedicated test only |
| `3a14fe0bd663250dd48c65e71f1a6550df89267f` | `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53` | `fix(p7): exclude root Finder metadata from EQ evidence` | `p7_thermal_diagnostics.py`; R6 contract test |
| `7c31c1be26274955686e9214a14bb29d1adc77b5` | `fb8647f45029614afdfd4114c3d987a29bfbec14` | `fix(p7): bind post-eq validation successor` | `p7_thermal_diagnostics.py`; dedicated test |

The exact path spellings for the first three rows are those frozen by Git and
the accepted modern B2 baseline: governance config is
`config/hsi/p7-governance-lineage-successor-v1.json`; production source is
`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`;
dedicated test is `tests/test_p7_thermal_diagnostics.py`; R6 contract test is
`tests/test_p7_td_b_r6_contract.py`. No additional path is allowed.

Governance payload current and commit-qualified SHA-256 must be
`69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`,
strict JSON object. Historical post-EQ owner is commit
`161094ffa2bf1f84ed1fc787e708e8c3463f10db`, parent
`f37517af3ae25efb41f085904fd48f037980ed04`, subject
`feat(p7): finalize eq-r6 state-c exposure policy`, exact paths governance
policy/source/R6 test, LF ledger
`fdd774e4686b3ebe45296880d6407666dd4ef6cc633e7f9cc891e62bd5480ac2`,
and after hashes respectively
`c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`,
`87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90`,
`10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23`.
Only `3a14fe0...`'s R6 test inherits
`accepted_post_eq_exposure_policy_validation`; its source is provenance-only.
`build_td_b_setup_release_lineage_candidate` remains the sole eligibility
owner and must not be imported or called.

## 4. C1-derived retained artifacts: exact one-read immutability

After validating all four C1 evidence files, derive and require these exact
absolute paths in index order:

1. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/current-lineage-candidate.json`,
   expected bytes `9819`, SHA-256
   `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0`;
2. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/resolved-formal-plan.json`,
   expected bytes `15137`, SHA-256
   `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b`;
3. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/setup-lineage-release.json`,
   expected bytes `1567`, SHA-256
   `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e`.

Each artifact has exact `lstat/open/read=1/1/1`: non-following lstat regular
non-symlink; `O_RDONLY|O_NOFOLLOW` open; before fstat; exactly one
`os.read(fd, lstat_size + 1)`; require exact byte count and expected SHA;
after fstat; close. Bind lstat/before/after mode, uid, gid, dev, inode, size,
mtime_ns, ctime_ns and equality. No second lstat/open/read, parsing, mmap, copy,
repair, rewrite, rename, regeneration, directory listing, or content use is
allowed. This proves byte provenance only, not semantic validation.

## 5. Decision and scientific source bindings

Each source gets one regular/non-symlink lstat, one no-follow open/read, and
exact SHA check:

- `advisor/4/4.GUIDE.md` SHA-256
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`;
- `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json`
  SHA-256 `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`;
- `/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt`
  SHA-256 `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`.

Engineering-governance evidence must be replayed only from exact Git object
`3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c:AGENTS.md`: blob OID exact
`58bfacb5fc46fcb42bf643d12974063533a684eb`, file SHA-256 exact
`604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0`.
Controller must use read-only Git plumbing to verify commit-qualified path,
blob OID, bytes hash, and these four exact governance semantics:

1. Advisor owns color science, measurement science, and scientific branch guidance;
2. Orchestrator owns implementation, provenance, execution packaging, and Git route;
3. only an unresolved scientific branch or a high-risk device operation requires a stop for Advisor/Human input;
4. GUIDE and Advisor evidence remain immutable to this package.

Within the `3e2ebed...` 181-path ledger, `AGENTS.md` must retain disposition
`present_in_commit_not_authorized_by_this_manifest`. It is non-selected
governance evidence only and must not be promoted to a scientific-audit
prerequisite, generic allowlist entry, eligibility input, or release authority.

## 6. Manifest schema, persistence, and physical terminal seal

Create exactly one
`retained-r3-audit-provenance-manifest-v2.json`, schema
`p7_retained_r3_audit_provenance_manifest_v2`, status
`sealed_subordinate_provenance_evidence`, scope
`validation_only_subordinate_provenance_evidence`. Top-level keys exact:
`schema,status,created_at_utc,scope,authority,source_decisions,rollback,path_owner_index,historical_helper_v1,integration_commit_3e2,accepted_integration_chain,governance_manifest,post_eq_lineage,retained_r3_source,controller,read_budget`.

`path_owner_index` must bind all four C1 files, exact index schema/status/hash,
three exact resolved paths, chain/cardinality facts, zero-content counters, and
the accepted Planner archive. `authority` must state
`eligibility_authority=false`, `eligibility_emitted=false`,
`canonical_validator_called=false`, `retained_r3_validated=false`,
`consumable=false`, `release_generation=false`, `release_copy=false`,
`release_consumption=false`, `production_runtime=false`,
`device_authority=none`, and `formal_authority=none`. Rollback is exact
`32b9e670ff3bbea0cd1505528c2ca87c2935446c` / `32b9e67`. No eligible,
validated, production-release-usable, authorization, or consumption claim may
appear.

All JSON is UTF-8, sorted keys, compact separators, `ensure_ascii=false`,
`allow_nan=false`, one LF. A shared no-clobber writer uses
`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`, complete write, file fsync,
close, directory fsync, then a fresh read-only strict reload and canonical-byte
equality check. No rewrite/repair/replace/relocation.

Write in exact order:

1. manifest;
2. `retained-r3-audit-provenance-manifest-v2.sha256.json`, binding physical
   manifest relative path/bytes/SHA/schema/status and root identity;
3. `terminal-evidence.json`, schema
   `p7_retained_r3_option_b_b2_corrected_terminal_v3`, success status
   `pass_waiting_for_planner` or truthful hard-failure status, containing all
   dispatch/input/Git/artifact/read/write/lock counters and the pre-terminal
   physical-write snapshot;
4. `terminal-evidence.sha256.json`, schema
   `p7_retained_r3_option_b_b2_corrected_terminal_seal_v3`, created only after
   terminal writer return, binding physical terminal identity and
   `terminal_write_returned=true`, while explicitly recording that the seal
   does not self-attest its own return.

Manifest seal后发生错误不得修改manifest/seal；只能写一次truthful terminal
及terminal seal后停止。任何 existing target、partial write、reload mismatch
或fsync error均hard failure且无repair。

## 7. Self-check, exact budgets, locks, and handoff

Before retained artifact access, run the original modern B2 exact memory-only
`12/12` matrix: positive skeleton; duplicate-key rejection; non-finite
rejection; wrong schema; wrong status; abbreviated/wrong commit; missing/extra
chain path; 181-ledger drift; selected third path; generic authorization;
retained hash/identity drift; authority escalation. Add C1 evidence/schema/seal
checks within the same controller but do not increase this frozen 12-case
matrix by silently relabeling test credit. No production validator/helper,
fake retained file, or second root.

Successful execution exact budgets:

```text
controller process/invocation = 1/1
evidence root create = 1
C1 evidence lstat/open/read/hash = 4/4/4/4 (exact one per file)
retained artifact count = 3
per retained artifact lstat/open/read/hash = 1/1/1/1
artifact parse/mmap/copy/repair/regenerate = 0/0/0/0/0
self/negative checks = 12/12
manifest/manifest-seal/terminal/terminal-seal writes = 1/1/1/1
retry/fallback/second root/alternate path/search/listing = 0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1
```

Canonical retained validator, retained audit helper, consumer, replay,
eligibility emission, release generation/qualification/copy/consumption,
tests, compileall, focused, full, synthetic, CodeGraph, and Git mutation are all
zero. Network, DNS, `.env`, credentials, device, camera, Ray, strip, cleanup,
capture, CR3, NPY, FORMAL-R6, public analyzer, TD-C, sentinel, P8, firmware,
and deployment are all zero.

Any dispatch/root/C1 evidence/schema/seal/path/Git/source/artifact/hash/
immutability/budget/persistence mismatch fails closed with no retry, fallback,
second root, substitute path, repair, or later-stage entry. Terminal seal durable
后只向`.agent-work/EXECUTION_RESULT.md` append exactly once并停止；不得修改
PLAN/FULL/archive/GUIDE或提交。Planner stop exact
`B2_CORRECTED_MANIFEST_SEALED_WAITING_PLANNER_REVIEW`。B2即使通过也只解锁
Planner/Orchestrator考虑B3；不得自行运行canonical validator、emit eligibility、
consume release或进入设备/scientific阶段。

## 维护性判断

本计划复用唯一C1 sealed path owner并保持canonical validator为唯一eligibility owner；
没有新增repository abstraction、path discovery或平行validation owner。复杂度只增加在一次性
C1 evidence ingestion与non-circular terminal seal，覆盖了旧stale-path和pre-write counter缺口，
无需架构重构。
