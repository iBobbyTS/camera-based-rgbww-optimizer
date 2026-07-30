# REF-P7-25-R2-B2：现代 accepted-integration immutable manifest seal

**计划状态：** `EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-MODERN-MANIFEST-SEAL-V2`

**预计时长：** `2–6 分钟`；本包不得运行测试/full/synthetic，不属于预计超过10分钟的长任务。

**唯一当前动作：** Executer以一个本地Python controller、一次invocation和一个brand-new external root，重算并绑定
accepted Git/provenance baseline及原retained-R3三件套的byte identity，exclusive-create、durably seal唯一
`retained-r3-audit-provenance-manifest-v2.json`，写独立hash seal与terminal，然后只向
`.agent-work/EXECUTION_RESULT.md` append一次交接并停Planner验收。

**Planner stop：** `B2_MANIFEST_SEALED_WAITING_PLANNER_REVIEW`；成功也不得运行B3、canonical validator、eligibility、release、
设备或scientific route。

**前序transition archive：**
`.agent-work/PLANS/20260730-0927-p7-retained-r3-option-b-b2-orchestrator-transition-review.md`，bytes `3107`，SHA-256
`6e9d4be889262848b7266dce05d6d940fd17a4711a346d03d385324614b9892f`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_modern_manifest_seal_plan_v2","reference_task_id":"REF-P7-25-R2-B2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-MODERN-MANIFEST-SEAL-V2","dispatch_state":"execution_authorized","execution_authorized":true,"single_current_action":"single_controller_single_root_seal_subordinate_exact_provenance_manifest_v2","dispatch_parent":"995633a3f671acf50f4cbbaa0837ae357ca2d41f","root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-modern-manifest-995633a-20260730T0932Z","manifest_name":"retained-r3-audit-provenance-manifest-v2.json","manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","controller_invocations":1,"root_creations":1,"repo_implementation_edits":0,"repo_implementation_commits":0,"canonical_validator_calls":0,"retained_artifact_count":3,"per_retained_artifact":{"lstat":1,"open":1,"read":1},"full_suite_calls":0,"synthetic_audit_calls":0,"retry":0,"fallback":0,"er_appends":1,"planner_stop":"B2_MANIFEST_SEALED_WAITING_PLANNER_REVIEW"}`

## 1. Frozen dispatch、owner与root

1. 当前activation的direct parent必须为
   `995633a3f671acf50f4cbbaa0837ae357ca2d41f`；该parent只归档transition review。Executer开始时只允许一次
   `git rev-parse HEAD`，并验证dispatch HEAD是该parent的direct child、subject exact
   `chore(plan): activate modern b2 manifest seal`、changed paths exact `.agent-work/PLAN.md`、additional `0`，且
   staged/unstaged/untracked均为`0`。
2. 唯一root exact：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-modern-manifest-995633a-20260730T0932Z`。
   执行前必须absent；不得改名、复用、删除、repair、fallback或创建第二root。controller以一次`os.mkdir(mode=0700)`创建，
   lstat/fstat验证regular directory、non-symlink、owner与mode，并fsync root及parent directory。
3. 只允许一个本地Python controller process/invocation。允许controller调用只读Git plumbing；禁止第二controller、shell/Python retry、
   手工补写artifact或在失败后继续。Controller source bytes必须在dispatch前固定一次SHA-256，并写入terminal与manifest；不得把source
   加入repository或创建Git commit。
4. `.agent-work/FULL_PLAN_REFERENCE.md`、GUIDE、archive与本PLAN均只读；Executer不得编辑、归档或重写它们。Repository唯一允许的
   变更是terminal完成后向`.agent-work/EXECUTION_RESULT.md` append一次；B2 implementation/code/test/config/doc edit及Git commit均为`0`。

## 2. Exact accepted integration baseline

Controller不得信任manifest中的自报字段；须从本repository的完整Git object ID独立重算commit、direct parent、tree、subject、exact sorted
changed paths、LF path-ledger SHA-256、每路径before/after blob OID、bytes、SHA-256、canonical binary-safe per-path patch SHA-256及
combined patch SHA-256，并把结果完整写入manifest。任何missing/extra path、prefix SHA、parent/subject/tree/blob/bytes/hash/patch漂移均
fail closed。

### 2.1 Historical helper与181-path integration

- helper v1 commit exact `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`，parent/release checkpoint exact
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`，subject exact
  `fix(p7): validate retained release terminal counts`，disposition exact
  `retained_release_audit_prerequisite_v1_superseded_before_real_validation`。
- Manifest必须显式记录：`accepted_history=true`、`terminal_validation_prerequisite=false`、
  `superseded_by_exact_v2_repair=true`、`eligible_successor=false`、`release_consumable=false`、
  `device_or_formal_authority="none"`。9303不可消费。
- integration commit exact `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`，parent exact `9303aa22...a2e`，subject exact
  `chore(orch): consolidate p7 evidence and workflow state`。其完整changed-path ledger必须count `181`且raw LF bytes SHA-256 exact
  `9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`。
- 只允许下列selected paths具有本manifest的scientific-audit-prerequisite classification：
  1. `src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py`；after SHA-256
     `48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8`；category
     `retained_release_validation_prerequisite_code`；scope
     `retained_R3_schema_validation_and_terminal_count_audit`。
  2. `tests/test_p7_retained_release_audit.py`；after SHA-256
     `c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f`；category
     `retained_release_validation_prerequisite_test`；scope
     `exact_helper_schema_owner_terminal_and_replay_regression`。
- 对selected两路径重算并绑定commit-qualified before/after blob OID、bytes、SHA-256、per-path patch及selected combined patch。
  另外179条路径必须逐条写入exact path及disposition
  `present_in_commit_not_authorized_by_this_manifest`；不得generic allowlist、glob、basename、future-descendant、prefix或directory授权。

### 2.2 Canonical seam accepted integration chain

按下列exact顺序重算并绑定每个commit的full SHA、direct parent、tree、subject、exact changed paths以及第2节规定的全部Git facts；遗漏、
额外semantic path或identity漂移立即hard failure：

| Commit | Direct parent | Exact subject | Exact changed paths |
| --- | --- | --- | --- |
| `0682cd8763516dfb19a8e1ad48c53cb9934b9d19` | `4316d0ce84fea8e9c87f90069567a82238e7a733` | `fix(p7): validate exact governance lineage successor` | `config/hsi/p7-governance-lineage-successor-v1.json`; `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`; `tests/test_p7_thermal_diagnostics.py` |
| `ba816216af9d37397873e054f44dbb7eea0f9b10` | `c0c51d9bc340da40ab5e95027e999962d2bd723e` | `fix(p7): separate historical lineage checkpoint ownership` | `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`; `tests/test_p7_thermal_diagnostics.py` |
| `a9a817137969d9d2692fdd0b244d08e26e8a025d` | `d4f97a63e304cd78ebe26930907024805ce25102` | `test(p7): align canonical lineage classification expectations` | `tests/test_p7_thermal_diagnostics.py` |
| `3a14fe0bd663250dd48c65e71f1a6550df89267f` | `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53` | `fix(p7): exclude root Finder metadata from EQ evidence` | `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`; `tests/test_p7_td_b_r6_contract.py` |
| `7c31c1be26274955686e9214a14bb29d1adc77b5` | `fb8647f45029614afdfd4114c3d987a29bfbec14` | `fix(p7): bind post-eq validation successor` | `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`; `tests/test_p7_thermal_diagnostics.py` |

Canonical governance payload exact path
`config/hsi/p7-governance-lineage-successor-v1.json`必须从commit-qualified/current bytes各独立验证为SHA-256
`69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`，strict JSON object reload，并原样绑定；不得修改或生成替代payload。

Historical post-EQ owner须另行绑定commit `161094ffa2bf1f84ed1fc787e708e8c3463f10db`、parent
`f37517af3ae25efb41f085904fd48f037980ed04`、subject `feat(p7): finalize eq-r6 state-c exposure policy`、exact三路径
`config/hsi/p7-ray-td-b-exposure-policy-v2.json`、`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`、
`tests/test_p7_td_b_r6_contract.py`及LF ledger SHA-256
`fdd774e4686b3ebe45296880d6407666dd4ef6cc633e7f9cc891e62bd5480ac2`。三条historical after SHA-256须依次为
`c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`、
`87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90`、
`10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23`。Exact validation successor只允许
`3a14fe0...`中的`tests/test_p7_td_b_r6_contract.py`继承
`accepted_post_eq_exposure_policy_validation`；其source为provenance-only。Canonical candidate builder
`build_td_b_setup_release_lineage_candidate`继续是唯一eligibility owner；B2不得import/call它。

## 3. Decision与scientific source bindings

Manifest必须绑定并由controller各执行一次regular-file/non-symlink identity、single open/read、SHA-256验证：

- `advisor/4/4.GUIDE.md` = `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；
- `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json`
  = `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`；
- `/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt`
  = `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`。

另绑定Human engineering-governance override URI
`conversation://human/2026-07-29/orchestrator-engineering-owner`、SHA-256
`52394bcd3fa819fcb83c82c50a89d0b9c4aaa53a41eca18bb953c174787b259d`及结论：Advisor仅拥有色彩/测量科学指导，
Orchestrator拥有文件、代码、provenance、execution packaging与Git路线。本包不修改GUIDE或Advisor evidence。

## 4. 原retained R3三件套：exact one-read immutability

Source root exact：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-161094f-c1-20260727T2103`。
禁止列举目录、glob、basename fallback、copy、repair、rewrite、rename、regenerate或消费。只可对下列三个exact absolute path分别执行：

1. `current-lineage-candidate.json`，expected SHA-256
   `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0`；
2. `resolved-formal-plan.json`，expected SHA-256
   `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b`；
3. `setup-lineage-release.json`，expected SHA-256
   `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e`。

每个原artifact预算exact：`lstat=1`、`open=1`、`read=1`。顺序必须是lstat regular/non-symlink → `O_RDONLY|O_NOFOLLOW` open →
before fstat → exact one `os.read(fd, lstat_size + 1)` → verify returned bytes count等于size且SHA匹配 → after fstat → close。Manifest绑定
lstat/before-fstat/after-fstat的mode、uid、gid、dev、inode、size、mtime_ns、ctime_ns与一致性结论。不得第二次lstat/open/read；任一漂移
hard-fail。这只是byte provenance与immutability observation，不得解析为audit、调用helper/consumer/replay/validator或声称validated。

## 5. Manifest exact schema、authority与persistence

Manifest top-level keys exact：
`schema,status,created_at_utc,scope,authority,source_decisions,rollback,historical_helper_v1,integration_commit_3e2,accepted_integration_chain,governance_manifest,post_eq_lineage,retained_r3_source,controller,read_budget`。

- `schema` exact `p7_retained_r3_audit_provenance_manifest_v2`；`status` exact
  `sealed_subordinate_provenance_evidence`；`scope` exact `validation_only_subordinate_provenance_evidence`。
- `authority`必须显式包含且全部为false/none：`eligibility_authority=false`、`eligibility_emitted=false`、
  `canonical_validator_called=false`、`retained_r3_validated=false`、`consumable=false`、`release_generation=false`、
  `release_copy=false`、`release_consumption=false`、`production_runtime=false`、`device_authority="none"`、
  `formal_authority="none"`。
- `rollback` exact full checkpoint `32b9e670ff3bbea0cd1505528c2ca87c2935446c`及short label `32b9e67`。
- Manifest禁止任何`eligible=true`、`candidate_eligible`、`production_release_usable`、`validated`、`authorized`或可消费暗示。

Serialization必须为UTF-8、sorted keys、compact separators、`ensure_ascii=false`、`allow_nan=false`、exact single LF EOF。以
`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`、mode0600创建，写完整bytes、file fsync、close、directory fsync；随后以新的只读fd strict
duplicate-key/non-finite-reject reload，验证canonical reserialization byte-identical、schema/keyset/status/authority及独立SHA-256。不得
rewrite、repair、replace、relocate或第二manifest。

同root再分别exclusive-create mode0600：

- `retained-r3-audit-provenance-manifest-v2.sha256.json`：只绑定manifest exact relative path、bytes、SHA-256、schema/status与
  root identity；strict reload、fsync并禁止clobber；
- `terminal-evidence.json`：schema exact `p7_retained_r3_option_b_b2_terminal_v2`；成功status exact
  `pass_waiting_for_planner`，包含dispatch/root/controller、所有input/Git/artifact/read/write/self-check counters、manifest与seal identities、
  zero locks及`planner_stop=B2_MANIFEST_SEALED_WAITING_PLANNER_REVIEW`。失败status exact `hard_failure_waiting_for_planner`，记录首个错误、
  已消费预算与未执行预算；已seal manifest/terminal不得修改。

所有JSON writer统一O_EXCL、0600、file+directory fsync、strict reload与canonical byte equality。Manifest seal后任何错误只能写一次terminal并停；
不得篡改manifest以适配结果。

## 6. Controller self-check、negative matrix与预算

读取任何原retained artifact前，controller须在memory-only fixtures运行exact `12/12` self/negative checks，且不创建额外root/file：

1. canonical positive manifest skeleton通过；2. duplicate key拒绝；3. NaN/Infinity拒绝；4. wrong schema拒绝；5. wrong status拒绝；
6. abbreviated/wrong commit拒绝；7. missing/extra chain path拒绝；8. 181 ledger count/hash drift拒绝；9. selected第三路径拒绝；
10. 179-path generic authorization拒绝；11. retained artifact hash/identity drift拒绝；12. eligibility/consumable/device/formal authority非false/none拒绝。

这些是schema/self-consistency负例，不是B3 synthetic audit，不得import production validator/helper或写fake retained payload。

预算上限也是exact验收值：controller process/invocation `1/1`；root create `1/1`；manifest/hash-seal/terminal各`1/1`；self-check
`12/12`；原artifact `3`且各`lstat/open/read=1/1/1`；repo implementation edit/commit `0/0`；retry/fallback `0/0`；canonical
validator、helper real audit、consumer、replay、eligibility emission、release generation/qualification/copy/consumption、full、focused、targeted、
synthetic、CodeGraph均`0`。PLAN/FULL各最多一次controller input read；其余source reads按第2–4节exact named inputs，不得search/glob。

## 7. 硬锁、失败分支与Executer交接

- Network、DNS、`.env`、credential、device、camera、Ray、strip、cleanup、capture、FORMAL-R6、public analyzer、TD-C、sentinel、P8、
  firmware与deployment全部为`0`。本pure-offline包无需Advisor或Human授权。
- 任一dispatch/root/source/Git/JSON/schema/self-check/read-budget/artifact identity/hash/persistence/reload/fsync/authority check失败，立即fail closed；
  不得retry、fallback、second root、second manifest、修复、重写、删除或进入B3。Retained R3保持
  `RETAINED_UNVALIDATED_UNCONSUMED`，logical rollback仍为`32b9e67`。
- Terminal durable后才可向`.agent-work/EXECUTION_RESULT.md` append exactly once，绑定PLAN SHA-256、dispatch HEAD、root、controller source
  SHA、terminal/manifest/seal path+bytes+SHA、Git/artifact/self-check counters、所有locks与明确Planner decision request。不得在ER中声称B2
  accepted、R3 validated、eligible或consumable。
- Executer完成ER append后立即停止，不改PLAN/FULL/archive/GUIDE，不创建commit。Planner将独立只读复算并接受或拒绝；只有Planner接受后
  Orchestrator才可更新FULL并考虑签发B3。
